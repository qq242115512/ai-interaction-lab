"""
Prometheus metrics middleware and endpoint.
Community standard: Prometheus + Grafana observability stack.

Exposes:
  - http_requests_total (counter) — total requests by method, path, status
  - http_request_duration_seconds (histogram) — request latency
  - api_calls_total (counter) — AI API calls by provider, model
  - active_sessions (gauge) — current session count
"""

import time

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.requests import Request
from starlette.responses import Response

# ── Metrics definitions ──────────────────────────────────────

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

HTTP_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

API_CALLS = Counter(
    "api_calls_total",
    "Total external AI API calls",
    ["provider", "model", "status"],
)

ACTIVE_SESSIONS = Gauge(
    "active_sessions",
    "Current number of active review sessions",
)


# ── FastAPI middleware ────────────────────────────────────────

class PrometheusMiddleware:
    """ASGI middleware that records HTTP metrics for every request."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.time()
        path = scope.get("path", "/")

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status = str(message["status"])
                method = scope.get("method", "GET")
                HTTP_REQUESTS.labels(method=method, path=path, status=status).inc()
                duration = time.time() - start
                HTTP_DURATION.labels(method=method, path=path).observe(duration)
            await send(message)

        await self.app(scope, receive, send_wrapper)


# ── Metrics endpoint ─────────────────────────────────────────

async def metrics_endpoint(request: Request) -> Response:
    """Prometheus /metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
