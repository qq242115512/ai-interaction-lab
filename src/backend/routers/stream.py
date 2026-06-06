"""Streaming SSE endpoint for real-time review progress."""
import json
import time
import uuid

import httpx

from config import ALLOWED_IMAGE_TYPES, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MAX_IMAGE_SIZE_MB
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from services.glmv_client import analyze_image
from services.prompts import DEEPSEEK_REVIEW_PROMPT
from services.utils import cleanup_old_sessions, logger, parse_json_response

router = APIRouter()
# Community standard: SQLite-backed session storage (was: dict)
from services.session_store import store

sessions = store


async def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/review/stream")
async def review_stream(
    image: UploadFile = File(...),
    dimensions: str = Form(...),
):
    # Validate image
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, detail=f"不支持的图片格式：{image.content_type}。请上传 PNG/JPG/WebP。")

    image_bytes = await image.read()
    if len(image_bytes) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, detail=f"图片过大，请上传不超过 {MAX_IMAGE_SIZE_MB}MB 的文件。")

    try:
        dims = json.loads(dimensions)
    except json.JSONDecodeError:
        raise HTTPException(400, detail="评审维度格式错误。")

    if not dims or not isinstance(dims, list):
        raise HTTPException(400, detail="请至少选择一个评审维度。")

    valid_dims = ["信息架构", "视觉层级", "可用性", "色彩系统", "版式设计", "无障碍"]
    for d in dims:
        if d not in valid_dims:
            raise HTTPException(400, detail=f"无效的评审维度：{d}")

    async def event_stream():
        t_start = time.time()

        # Step 1: GLM-4V visual analysis
        yield await _sse_event("status", {"step": "visual", "message": "正在识别设计元素..."})
        try:
            visual_analysis = await analyze_image(image_bytes, image.content_type)
            logger.info(f"Visual analysis done, {len(visual_analysis.get('components', []))} components")
        except Exception as e:
            logger.error(f"Visual analysis failed: {e}")
            yield await _sse_event("error", {"message": "视觉分析失败，请稍后重试。"})
            return
        yield await _sse_event("status", {"step": "visual_done", "message": "设计元素识别完成"})

        # Step 2: DeepSeek streaming review
        yield await _sse_event("status", {"step": "review", "message": "正在生成评审报告..."})

        user_message = f"""以下是 UI 设计截图的结构化分析：
```json
{json.dumps(visual_analysis, ensure_ascii=False, indent=2)}
```

学生选择的评审维度：{", ".join(dims)}

请针对以上维度生成评审报告。"""

        accumulated = ""
        try:
            async with httpx.AsyncClient(timeout=180.0) as client, client.stream(
                "POST",
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": DEEPSEEK_REVIEW_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 8192,
                    "stream": True,
                },
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                accumulated += content
                                yield await _sse_event("chunk", {"text": content})
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
        except Exception as e:
            logger.error(f"DeepSeek streaming failed: {e}")
            yield await _sse_event("error", {"message": "评审生成失败，请稍后重试。"})
            return

        # Step 3: Parse final result
        yield await _sse_event("status", {"step": "parsing", "message": "正在整理评审报告..."})
        try:
            review_data = parse_json_response(accumulated)
        except Exception as e:
            logger.warning(f"Stream parse failed: {e}, retrying with non-streaming fallback...")
            yield await _sse_event("status", {"step": "retry", "message": "正在用备用方式重新生成..."})
            try:
                from services.deepseek_client import generate_review
                review_data = await generate_review(visual_analysis, dims)
            except Exception as e2:
                logger.error(f"Fallback review also failed: {e2}")
                yield await _sse_event("error", {"message": "评审结果解析失败，请重试。"})
                return

        # Store session
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "visual_analysis": visual_analysis,
            "review": review_data,
            "chat_history": [],
            "dimensions": dims,
            "_created_at": time.time(),
        }
        cleanup_old_sessions(sessions)

        elapsed = time.time() - t_start
        yield await _sse_event("done", {
            "session_id": session_id,
            "overall_score": review_data.get("overall_score", 0),
            "dimensions": review_data.get("dimensions", []),
            "elapsed_seconds": round(elapsed, 1),
        })

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )
