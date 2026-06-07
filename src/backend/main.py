import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from middleware.metrics import ACTIVE_SESSIONS, PrometheusMiddleware, metrics_endpoint
from middleware.security import SecurityMiddleware
from routers import agent_system, chat, patterns, review, stream
from services.utils import logger, setup_logging

setup_logging()

app = FastAPI(title='设计引路人 API', version='0.5.2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://fanshuyang.top', 'https://www.fanshuyang.top',
                   'http://localhost:8080', 'http://localhost:3000', 'http://127.0.0.1:8080'],
    allow_credentials=False,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
)

app.add_middleware(SecurityMiddleware)
app.add_middleware(PrometheusMiddleware)  # Community standard: Prometheus metrics

app.include_router(review.router, prefix='/api')
app.include_router(chat.router, prefix='/api')
app.include_router(stream.router, prefix='/api')
app.include_router(patterns.router, prefix='/api')
app.include_router(agent_system.router, prefix='/api')

# Session store: SQLite persistence replaces in-memory dict (community standard)
from services.session_store import store

review.store = store
chat.store = store
stream.store = store


@app.middleware('http')
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    if request.url.path != '/api/health':
        logger.info(f'{request.method} {request.url.path} -> {response.status_code} ({elapsed:.1f}s)')
    return response


@app.get('/api/health')
async def health():
    store.cleanup()
    return {
        'status': 'ok',
        'version': '0.5.2',
        'sessions': len(store),
    }


@app.get('/metrics')
async def metrics(request: Request):
    """Prometheus metrics endpoint — community standard observability."""
    ACTIVE_SESSIONS.set(len(store))
    return await metrics_endpoint(request)


@app.post('/api/health')
async def log_frontend_error(request: Request):
    """Collect frontend JS errors via POST /api/health.
    Nginx only routes specific paths to port 8080 — /api/log goes to catch-all (3001).
    So we reuse /api/health for error collection."""
    try:
        body = await request.json()
        msg = str(body.get('message', ''))[:500]
        page = str(body.get('page', ''))[:200]
        line = body.get('line', '')
        col = body.get('col', '')
        logger.warning(f'[CLIENT ERROR] {msg} | page={page} | line={line}:{col}')
    except Exception:
        logger.warning('[CLIENT ERROR] <unparseable>')
    return {'status': 'logged'}
