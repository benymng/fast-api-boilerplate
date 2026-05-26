import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.config import get_settings
from app.database import Base, engine

logger = logging.getLogger(__name__)


def init_db(max_retries: int = 5, retry_delay_seconds: int = 2) -> None:
    """Create tables for local development.

    For production apps, replace this with Alembic migrations in your deploy flow.
    """
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables are ready")
            return
        except Exception:
            if attempt == max_retries:
                logger.exception("Database initialization failed")
                raise

            logger.warning(
                "Database initialization failed on attempt %s/%s; retrying in %s seconds",
                attempt,
                max_retries,
                retry_delay_seconds,
            )
            time.sleep(retry_delay_seconds)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {
            "message": f"Welcome to {settings.app_name}",
            "docs": "/docs",
            "health": "/health",
        }

    @app.get("/health", tags=["system"])
    async def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()

__all__ = ["app", "create_app"]
