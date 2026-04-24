from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _load_env() -> None:
    # Load from current working directory (common local usage)
    load_dotenv()

    # Also load from repo root so `uvicorn backend.app.main:app` works
    # regardless of where it is executed from.
    repo_root = Path(__file__).resolve().parents[3]
    load_dotenv(repo_root / ".env")


_load_env()


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("ENVIRONMENT", "dev")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    database_url: str = os.getenv("DATABASE_URL", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

