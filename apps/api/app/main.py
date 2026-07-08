from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, questions, rulebooks
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="5-tiao-qu API",
        version="0.1.0",
        description="Board game rulebook ingestion and citation-first RAG API.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(rulebooks.router, prefix="/rulebooks", tags=["rulebooks"])
    app.include_router(questions.router, prefix="/questions", tags=["questions"])
    return app


app = create_app()
