from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.v1.router import api_router
from backend.app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Dairy Analytics Dashboard API",
        version="0.1.0",
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()

