"""Security middleware: rate limiting, prompt injection filter, headers, error sanitization."""
import re
import time
from collections import defaultdict

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.utils import logger

# ============================================================
# Rate Limiting — per-IP sliding window, 20 req/min for AI endpoints
# ============================================================
AI_ENDPOINTS = {
    "/api/review", "/api/review/stream", "/api/chat",
    "/api/clarify", "/api/confirm", "/api/execute",
    "/api/stream", "/api/analyze", "/api/progressive",
}
RATE_LIMIT = 20
RATE_WINDOW = 60

_ip_buckets: dict[str, list[float]] = defaultdict(list)


def _cleanup_buckets():
    now = time.time()
    expired = [
        ip for ip, times in _ip_buckets.items()
        if all(now - t > RATE_WINDOW for t in times)
    ]
    for ip in expired:
        del _ip_buckets[ip]


def check_rate_limit(ip: str, path: str) -> bool:
    if path not in AI_ENDPOINTS:
        return True
    _cleanup_buckets()
    now = time.time()
    window_start = now - RATE_WINDOW
    _ip_buckets[ip] = [t for t in _ip_buckets[ip] if t > window_start]
    if len(_ip_buckets[ip]) >= RATE_LIMIT:
        return False
    _ip_buckets[ip].append(now)
    return True


# ============================================================
# Prompt Injection Filter — Chinese + English patterns
# ============================================================
INJECTION_PATTERNS = [
    # English variants
    (re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)", re.I),
     "检测到指令覆盖尝试。"),
    (re.compile(r"system\s*(prompt|message|instruction|command)", re.I),
     "检测到系统指令访问尝试。"),
    (re.compile(r"you\s+are\s+now\s+(a\s+)?(hacker|evil|malicious|unethical|jailbreak)", re.I),
     "检测到角色劫持尝试。"),
    (re.compile(r"forget\s+(everything|all|your)\s+(you|training|instructions)", re.I),
     "检测到记忆清除尝试。"),
    (re.compile(r"pretend\s+(you\s+are|to\s+be)", re.I),
     "检测到伪装指令。"),
    (re.compile(r"new\s+(system\s+)?(prompt|instruction)", re.I),
     "检测到新指令注入尝试。"),
    (re.compile(r"override\s+(system\s+)?(prompt|instruction|rules)", re.I),
     "检测到指令覆盖尝试。"),
    (re.compile(r"(give|tell|show)\s+(me|us)\s+(your|the)\s+(system\s+)?(prompt|instructions|rules)", re.I),
     "检测到系统指令请求。"),
    # Chinese variants
    (re.compile(r"(忽略|忘记|无视)\s*(所有|之前|上面|一切)?\s*(指令|规则|提示|要求|设定|配置)"),
     "检测到中文指令覆盖尝试。"),
    (re.compile(r"(系统|新的|新)\s*(指令|提示|设定|规则|配置)"),
     "检测到中文系统指令访问。"),
    (re.compile(r"(你现在是|你现在扮演|你假装|你假装是)"),
     "检测到中文角色劫持。"),
    (re.compile(r"(不要|别|禁止)\s*(遵守|遵循|按照)\s*(之前|原来|系统)"),
     "检测到中文规则绕过。"),
    (re.compile(r"(泄露|透露|告诉|说出|输出)\s*(你的|系统)?\s*(提示词|指令|设定|prompt|规则|配置)"),
     "检测到中文指令窃取。"),
    (re.compile(r"(重新|重置|修改|更改)\s*(设定|角色|身份|规则|配置)"),
     "检测到中文角色重置。"),
]

INJECTION_PREFIXES = [
    "SYSTEM:", "system:", "System:",
    "USER:", "User:",
    "ASSISTANT:", "Assistant:", "assistant:",
]

MAX_INPUT_LENGTH = 2000


def check_injection(text: str) -> str | None:
    """Check input for prompt injection. Returns error message if detected, None if safe."""
    if not text or not text.strip():
        return None

    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]

    stripped = text.strip()
    for prefix in INJECTION_PREFIXES:
        if stripped.startswith(prefix):
            return f"输入包含不被允许的内容。请使用正常的提问方式。"

    for pattern, message in INJECTION_PATTERNS:
        if pattern.search(text):
            return f"输入包含不被允许的内容。请使用正常的提问方式。"

    return None


# Security headers added to all responses
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' https://fanshuyang.top; "
        "font-src 'self';"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}


def log_api_usage(ip: str, endpoint: str, status_code: int, duration_ms: float):
    """Log AI API usage for cost and abuse monitoring."""
    if endpoint in AI_ENDPOINTS:
        logger.info(
            f"API_USAGE ip={ip} endpoint={endpoint} "
            f"status={status_code} duration={duration_ms:.0f}ms"
        )


# ============================================================
# FastAPI Middleware
# ============================================================
class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        start = time.time()

        # 1. Rate limiting
        if not check_rate_limit(ip, path):
            return JSONResponse(
                status_code=429,
                content={"detail": "请求过于频繁，请稍后再试。（每分钟最多 20 次 AI API 调用）"},
            )

        # 2. Prompt injection check on POST body text fields
        body_bytes = None
        if request.method == "POST":
            body_bytes = await request.body()
            try:
                body = __import__("json").loads(body_bytes)
                for field in [
                    "description", "prompt", "message", "context",
                    "query", "action_type", "action_detail",
                ]:
                    if field in body and isinstance(body[field], str):
                        error = check_injection(body[field])
                        if error:
                            logger.warning(f"Injection blocked: ip={ip} field={field}")
                            return JSONResponse(status_code=400, content={"detail": error})
            except Exception:
                pass  # Not JSON — let endpoint handle

            # Re-inject body so downstream can read it
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive

        # 3. Process request, catch unhandled errors
        try:
            response = await call_next(request)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unhandled error on {path}: {e}")
            duration = (time.time() - start) * 1000
            log_api_usage(ip, path, 500, duration)
            return JSONResponse(
                status_code=500,
                content={"detail": "服务器内部错误，请稍后重试。"},
            )

        # 4. Add security headers
        for header, value in SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)

        # 5. Log usage
        duration = (time.time() - start) * 1000
        log_api_usage(ip, path, response.status_code, duration)

        return response
