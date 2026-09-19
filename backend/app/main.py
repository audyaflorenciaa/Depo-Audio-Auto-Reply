"""
DA AUTOLIGHT AI — FastAPI Entry Point

Creates the FastAPI application, registers routes, and configures
logging. Run with: uvicorn app.main:app --reload --port 8000
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.webhook import router as webhook_router

# ── Configure logging ──────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


# ── Application lifespan (startup / shutdown) ──────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on server startup and shutdown."""
    logger.info("=" * 60)
    logger.info("🚀 DA AUTOLIGHT AI Bot starting up...")
    logger.info(f"   Environment : {settings.APP_ENV}")
    logger.info(f"   Port        : {settings.APP_PORT}")
    logger.info(f"   Gemini Model: {settings.GEMINI_MODEL}")
    logger.info(f"   Supabase    : {settings.SUPABASE_URL[:40]}...")
    logger.info(f"   Webhook     : /webhook/{'*' * 6} (secret hidden)")
    logger.info("=" * 60)
    yield
    logger.info("👋 DA AUTOLIGHT AI Bot shutting down.")


# ── Create FastAPI app ─────────────────────────────────────────
app = FastAPI(
    title="DA AUTOLIGHT AI Bot",
    description="Telegram bot for DA AUTOLIGHT automotive lighting workshop.",
    version="0.1.0",
    lifespan=lifespan,
)

# ── Register routes ────────────────────────────────────────────
app.include_router(webhook_router)


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}
