import uuid
import json
import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from models.schemas import ReviewResponse
from services.glmv_client import analyze_image
from services.deepseek_client import generate_review
from services.utils import sanitize_error, cleanup_old_sessions, logger
from config import MAX_IMAGE_SIZE_MB, ALLOWED_IMAGE_TYPES

router = APIRouter()

sessions: dict[str, dict] = {}


@router.post("/review", response_model=ReviewResponse)
async def review_design(
    image: UploadFile = File(...),
    dimensions: str = Form(...),
):
    # Validate image type
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的图片格式：{image.content_type}。请上传 PNG/JPG/WebP。",
        )

    image_bytes = await image.read()
    if len(image_bytes) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"图片过大，请上传不超过 {MAX_IMAGE_SIZE_MB}MB 的文件。",
        )

    # Parse and validate dimensions
    try:
        dims = json.loads(dimensions)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="评审维度格式错误。")

    if not dims or not isinstance(dims, list):
        raise HTTPException(status_code=400, detail="请至少选择一个评审维度。")

    valid_dims = ["信息架构", "视觉层级", "可用性", "色彩系统", "版式设计", "无障碍"]
    for d in dims:
        if d not in valid_dims:
            raise HTTPException(status_code=400, detail=f"无效的评审维度：{d}")

    # Step 1: GLM-4V visual analysis
    try:
        visual_analysis = await analyze_image(image_bytes, image.content_type)
        logger.info(f"Visual analysis complete, found {len(visual_analysis.get('components', []))} components")
    except Exception as e:
        logger.error(f"Visual analysis failed: {e}")
        raise HTTPException(status_code=502, detail=f"视觉分析失败，请稍后重试。")

    # Step 2: DeepSeek design review
    try:
        review_data = await generate_review(visual_analysis, dims)
        logger.info(f"Review generated, overall_score={review_data.get('overall_score')}")
    except Exception as e:
        logger.error(f"Review generation failed: {e}")
        raise HTTPException(status_code=502, detail=f"评审生成失败，请稍后重试。")

    # Store session with timestamp for TTL cleanup
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "visual_analysis": visual_analysis,
        "review": review_data,
        "chat_history": [],
        "dimensions": dims,
        "_created_at": time.time(),
    }

    # Cleanup old sessions periodically
    cleanup_old_sessions(sessions)

    return ReviewResponse(
        session_id=session_id,
        overall_score=review_data.get("overall_score", 0),
        dimensions=review_data.get("dimensions", []),
    )
