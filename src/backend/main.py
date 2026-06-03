import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import review, chat, stream, patterns, agent_system
from services.utils import setup_logging, cleanup_old_sessions, logger
from middleware.security import SecurityMiddleware

setup_logging()

app = FastAPI(title='设计引路人 API', version='0.5.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://fanshuyang.top', 'https://www.fanshuyang.top',
                   'http://localhost:8080', 'http://localhost:3000', 'http://127.0.0.1:8080'],
    allow_credentials=False,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type'],
)

app.add_middleware(SecurityMiddleware)

app.include_router(review.router, prefix='/api')
app.include_router(chat.router, prefix='/api')
app.include_router(stream.router, prefix='/api')
app.include_router(patterns.router, prefix='/api')
app.include_router(agent_system.router, prefix='/api')

chat.sessions = review.sessions
stream.sessions = review.sessions

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
    cleaned = cleanup_old_sessions(review.sessions)
    return {'status': 'ok', 'version': '0.5.1', 'sessions': len(review.sessions)}
