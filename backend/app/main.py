import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import RequestIDMiddleware, ExceptionHandlerMiddleware
from app.api.v1 import content, students, questions, tracing, tutor, speech, auth

settings = get_settings()
logger = get_logger("app")


def create_app() -> FastAPI:
    setup_logging()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Adaptive Multimodal Learning & Assessment Platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware (order matters: last added = first executed)
    application.add_middleware(ExceptionHandlerMiddleware)
    application.add_middleware(RequestIDMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    application.include_router(auth.router, prefix=settings.API_V1_PREFIX)
    application.include_router(content.router, prefix=settings.API_V1_PREFIX)
    application.include_router(students.router, prefix=settings.API_V1_PREFIX)
    application.include_router(questions.router, prefix=settings.API_V1_PREFIX)
    application.include_router(tracing.router, prefix=settings.API_V1_PREFIX)
    application.include_router(tutor.router, prefix=settings.API_V1_PREFIX)
    application.include_router(speech.router, prefix=settings.API_V1_PREFIX)

    @application.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "edumind"}

    @application.get("/")
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": "0.1.0",
            "docs": "/docs",
            "api": settings.API_V1_PREFIX,
        }

    @application.on_event("startup")
    async def startup():
        logger.info("EduMind starting up...")

    @application.on_event("shutdown")
    async def shutdown():
        logger.info("EduMind shutting down...")

    return application


app = create_app()
