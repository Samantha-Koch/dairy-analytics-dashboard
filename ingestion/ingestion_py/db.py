from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@dataclass(frozen=True)
class DbConfig:
    database_url: str


def load_db_config() -> DbConfig:
    # Allow running from repo root or from `ingestion/`
    load_dotenv()
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required. Set it in environment or ingestion/.env (see ingestion/.env.example)."
        )

    return DbConfig(database_url=database_url)


def get_engine() -> Engine:
    cfg = load_db_config()
    return create_engine(cfg.database_url, future=True)

