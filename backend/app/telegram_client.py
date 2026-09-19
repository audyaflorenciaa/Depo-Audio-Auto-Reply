"""
DA AUTOLIGHT AI — Telegram Client Module

Sends messages to Telegram users via the Bot API.
Uses httpx for async HTTP requests.
"""

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_TELEGRAM_API = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"


async def send_message(
    chat_id: int,
    text: str,
    parse_mode: str = "HTML",
) -> None:
    """
    Send a text message to a Telegram user.

    - Retries once on network timeout.
    - Logs errors but does NOT raise — the bot must stay alive.
    """
    url = f"{_TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    for attempt in range(2):  # max 2 attempts (initial + 1 retry)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload)

            if response.status_code == 200:
                logger.info(
                    f"Message sent to chat_id={chat_id} "
                    f"(length={len(text)} chars)"
                )
                return
            else:
                logger.warning(
                    f"Telegram API returned {response.status_code} for "
                    f"chat_id={chat_id}: {response.text}"
                )
                return  # Don't retry on non-timeout HTTP errors

        except httpx.TimeoutException:
            if attempt == 0:
                logger.warning(
                    f"Timeout sending to chat_id={chat_id}, retrying..."
                )
            else:
                logger.error(
                    f"Timeout sending to chat_id={chat_id} after retry."
                )

        except Exception as e:
            logger.error(
                f"Error sending message to chat_id={chat_id}: {e}"
            )
            return  # Don't retry on unexpected errors
