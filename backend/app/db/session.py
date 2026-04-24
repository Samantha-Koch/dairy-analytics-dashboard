from __future__ import annotations

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings


def _get_database_url() -> str:
    if settings.database_url:
        return settings.database_url

    raise RuntimeError(
        "DATABASE_URL is required. "
        "Set it in the container environment or in a repo-root .env file."
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(_get_database_url(), future=True)


@lru_cache(maxsize=1)
def get_sessionmaker():
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
        future=True,
    )


# Prefer `get_sessionmaker()` in new code. Keeping a name here is convenient,
# but it must not force a DB connection or require env vars at import time.
SessionLocal = sessionmaker(autoflush=False, autocommit=False, future=True)

