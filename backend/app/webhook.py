"""
DA AUTOLIGHT AI — Webhook Route Module

Defines the POST /webhook/{secret_path} endpoint that Telegram
sends updates to. Validates the secret, parses the payload,
and dispatches to the state machine.
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.config import settings
from app.state_machine import process_message

logger = logging.getLogger(__name__)

router = APIRouter()


# ── Pydantic models for Telegram payload ───────────────────────

class TelegramChat(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    message_id: int
    text: Optional[str] = None
    chat: TelegramChat


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None


# ── Webhook endpoint ───────────────────────────────────────────

@router.post("/webhook/{secret_path}")
async def telegram_webhook(secret_path: str, request: Request):
    """
    Receive Telegram webhook updates.

    - Validates the secret path.
    - Parses the Telegram Update payload.
    - Dispatches to the state machine.
    - ALWAYS returns 200 OK to prevent Telegram retry loops.
    """
    # ── Validate secret ────────────────────────────────────────
    if secret_path != settings.WEBHOOK_SECRET_PATH:
        logger.warning(f"Webhook called with wrong secret: {secret_path}")
        raise HTTPException(status_code=403, detail="Forbidden")

    # ── Parse payload ──────────────────────────────────────────
    try:
        body = await request.json()
        update = TelegramUpdate(**body)
    except Exception as e:
        logger.error(f"Failed to parse Telegram update: {e}")
        return {"ok": True}  # Still return 200

    # ── Check if there's a message ─────────────────────────────
    if update.message is None:
        logger.debug("Update has no message (edited_message, etc.). Skipping.")
        return {"ok": True}

    chat_id = update.message.chat.id
    user_text = update.message.text

    # ── Handle non-text messages ───────────────────────────────
    if user_text is None:
        logger.info(f"Non-text message from chat_id={chat_id}. Sending polite reply.")
        from app.telegram_client import send_message
        await send_message(
            chat_id,
            "Maaf, saya hanya bisa memproses pesan teks 😊"
        )
        return {"ok": True}

    # ── Process the message ────────────────────────────────────
    try:
        await process_message(chat_id, user_text)
    except Exception as e:
        logger.error(
            f"Unhandled error processing message from chat_id={chat_id}: {e}",
            exc_info=True,
        )

    # Always return 200 to Telegram
    return {"ok": True}
