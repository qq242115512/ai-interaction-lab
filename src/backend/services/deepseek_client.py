import json

import httpx

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

from services.prompts import DEEPSEEK_CHAT_PROMPT, DEEPSEEK_REVIEW_PROMPT
from services.utils import logger, parse_json_response, retry_with_backoff


async def _call_deepseek(messages, max_tokens, temperature=0.7, timeout=120.0):
    """Core DeepSeek API call with configurable params."""
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


async def generate_review(visual_analysis: dict, dimensions: list[str]) -> dict:
    """Generate design review based on GLM-4V visual analysis."""
    user_message = f"""以下是 UI 设计截图的结构化分析：
```json
{json.dumps(visual_analysis, ensure_ascii=False, indent=2)}
```

学生选择的评审维度：{", ".join(dimensions)}

请针对以上维度生成评审报告。"""

    messages = [
        {"role": "system", "content": DEEPSEEK_REVIEW_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # First attempt with normal temperature
    try:
        content = await retry_with_backoff(lambda: _call_deepseek(messages, 8192, 0.7))
        return parse_json_response(content)
    except (ValueError, json.JSONDecodeError) as e:
        logger.warning(f"First review parse failed, retrying with temp=0.3: {e}")
        # Retry with lower temperature for more stable output
        try:
            content = await _call_deepseek(messages, 8192, 0.3, 180.0)
            return parse_json_response(content)
        except Exception as e2:
            logger.error(f"Review retry also failed: {e2}")
            raise
    except Exception:
        raise


async def chat_reply(session_context: dict, user_message: str) -> dict:
    """Generate a follow-up chat reply with compact context."""
    review = session_context.get("review", {})
    chat_history = session_context.get("chat_history", [])

    dim_summaries = []
    for dim in review.get("dimensions", [])[:6]:
        dim_summaries.append({
            "name": dim.get("name", ""),
            "score": dim.get("score", 0),
            "summary": dim.get("summary", "")[:80],
        })

    recent_history = chat_history[-12:] if len(chat_history) > 12 else chat_history

    compact_context = json.dumps({
        "overall_score": review.get("overall_score", 0),
        "dimension_summaries": dim_summaries,
        "recent_chat": recent_history,
    }, ensure_ascii=False, indent=2)

    messages = [
        {"role": "system", "content": DEEPSEEK_CHAT_PROMPT},
        {"role": "user", "content": f"评审摘要：\n```json\n{compact_context}\n```\n\n学生的追问：{user_message}"},
    ]

    try:
        content = await retry_with_backoff(lambda: _call_deepseek(messages, 1024, 0.7, 60.0))
        return parse_json_response(content)
    except (ValueError, json.JSONDecodeError) as e:
        logger.warning(f"Chat parse failed, retrying with temp=0.3: {e}")
        content = await _call_deepseek(messages, 1024, 0.3, 60.0)
        return parse_json_response(content)
    except Exception as e:
        logger.error(f"DeepSeek chat failed: {e}")
        raise
