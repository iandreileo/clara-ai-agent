from fastapi import FastAPI
from fastapi.requests import Request
import time
from app.core.utils.logging import logger
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.services.chat_service import ChatService
from app.api.v1.endpoints.chat import router as chat_router
from app.api.default.health import router as health_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    contact={
        "name": settings.PROJECT_AUTHOR,
        "email": settings.PROJECT_EMAIL
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_HOSTS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_service = ChatService()

app.include_router(
    chat_router,
    prefix=f"{settings.API_VERSION_STR}/chat",
    tags=["chat"]
)

app.include_router(
    health_router,
    prefix=f"{settings.API_VERSION_STR}/health",
    tags=["health"]
)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request to {request.url.path} completed in {duration:.2f} seconds")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)