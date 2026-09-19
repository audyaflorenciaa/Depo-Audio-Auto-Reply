"""
DA AUTOLIGHT AI — Configuration Module

Loads all environment variables from .env and exposes them
through a single `settings` object. Raises ValueError on startup
if any required variable is missing or empty.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

# ── Load .env from the backend/ directory ──────────────────────
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    # Telegram
    TELEGRAM_BOT_TOKEN: str

    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Application
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    WEBHOOK_BASE_URL: str = "https://localhost"
    WEBHOOK_SECRET_PATH: str

    # Logging & Storage
    HANDOFF_LOG_DIR: str = "handoff_log"
    LOG_LEVEL: str = "INFO"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    @field_validator(
        "TELEGRAM_BOT_TOKEN",
        "GEMINI_API_KEY",
        "WEBHOOK_SECRET_PATH",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY",
        mode="before",
    )
    @classmethod
    def must_not_be_empty(cls, value: str, info) -> str:
        if not value or not value.strip():
            raise ValueError(
                f"❌ Environment variable '{info.field_name}' is required but "
                f"missing or empty. Check your .env file."
            )
        return value.strip()


def _load_settings() -> Settings:
    """Read env vars and build a validated Settings object."""
    return Settings(
        TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
        GEMINI_MODEL=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        APP_ENV=os.getenv("APP_ENV", "development"),
        APP_PORT=int(os.getenv("APP_PORT", "8000")),
        WEBHOOK_BASE_URL=os.getenv("WEBHOOK_BASE_URL", "https://localhost"),
        WEBHOOK_SECRET_PATH=os.getenv("WEBHOOK_SECRET_PATH", ""),
        HANDOFF_LOG_DIR=os.getenv("HANDOFF_LOG_DIR", "handoff_log"),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        SUPABASE_URL=os.getenv("SUPABASE_URL", ""),
        SUPABASE_SERVICE_KEY=os.getenv("SUPABASE_SERVICE_KEY", ""),
    )


# ── Singleton — import this from other modules ────────────────
settings = _load_settings()
