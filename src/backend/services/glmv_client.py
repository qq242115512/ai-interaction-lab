import base64

import httpx

from config import GLM_API_KEY, GLM_BASE_URL

from services.prompts import GLMV_SYSTEM_PROMPT
from services.utils import logger, parse_json_response, retry_with_backoff


async def analyze_image(image_bytes: bytes, content_type: str) -> dict:
    """Send image to GLM-4V, get structured visual analysis as dict."""
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{content_type};base64,{image_b64}"

    async def _call():
        payload = {
            "model": "glm-4v",
            "messages": [
                {"role": "system", "content": GLMV_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": data_url}},
                        {"type": "text", "text": "请分析这张 UI 设计截图，输出结构化 JSON。"},
                    ],
                },
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{GLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {GLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    try:
        content = await retry_with_backoff(_call)
        return parse_json_response(content)
    except Exception as e:
        logger.error(f"GLM-4V analysis failed: {e}")
        raise
