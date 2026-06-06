"""Shared utilities: JSON parsing, retry, logging."""
import json
import logging
import time

logger = logging.getLogger("design-mentor")


def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(handler)
    logger.setLevel(level)


def parse_json_response(raw: str) -> dict:
    """Robust JSON extraction from AI model responses.

    Handles: markdown fences, trailing text, nested objects.
    """
    text = raw.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Remove markdown fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove opening fence (possibly with language tag)
        lines = lines[1:]
        # Remove closing fence
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # Try again after fence removal
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fallback: extract JSON object using brace matching
    start = text.find("{")
    if start == -1:
        raise ValueError(f"无法从 AI 响应中提取 JSON。原始内容前 200 字符: {raw[:200]}")

    # Find matching closing brace
    depth = 0
    end = -1
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if end == -1:
        raise ValueError(f"无法找到匹配的 JSON 结束括号。原始内容前 200 字符: {raw[:200]}")

    json_str = text[start:end]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}。提取的内容前 200 字符: {json_str[:200]}")


async def retry_with_backoff(fn, max_retries=2, base_delay=1.0):
    """Call async fn with exponential backoff on failure."""
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
    raise last_err


def sanitize_error(e: Exception) -> str:
    """Return a user-safe error message. Never expose API keys or stack traces."""
    msg = str(e)
    # Mask potential key leaks
    if "sk-" in msg.lower() or "bearer" in msg.lower():
        return "API 认证失败，请检查 API Key 配置。"
    # Truncate long messages
    if len(msg) > 300:
        msg = msg[:300] + "..."
    return msg


# Session cleanup: remove sessions older than this many seconds
SESSION_TTL_SECONDS = 3600  # 1 hour


def cleanup_old_sessions(sessions: object) -> int:
    """Remove expired sessions. Delegates to store.cleanup() if available.
    Returns count of removed sessions."""
    if hasattr(sessions, "cleanup"):
        return sessions.cleanup()
    # Fallback for plain dict sessions (legacy)
    now = time.time()
    expired = [
        sid for sid, s in sessions.items()
        if now - s.get("_created_at", now) > SESSION_TTL_SECONDS
    ]
    for sid in expired:
        del sessions[sid]
    if expired:
        logger.info(f"Cleaned up {len(expired)} expired sessions")
    return len(expired)
