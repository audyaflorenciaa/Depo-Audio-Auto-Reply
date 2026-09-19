"""
DA AUTOLIGHT AI — Handoff Logger Module

Writes handoff events to disk as JSON files when the bot
cannot handle a conversation and passes it to a human.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

# Resolve handoff log directory relative to backend/
_LOG_DIR = Path(__file__).resolve().parent.parent / settings.HANDOFF_LOG_DIR


def log_handoff(chat_id: int, session, reason: str) -> None:
    """
    Write a handoff event to a JSON file.

    Args:
        chat_id: The Telegram chat ID.
        session: The Session object at time of handoff.
        reason: Human-readable reason for the handoff.
    """
    try:
        # Ensure directory exists
        _LOG_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc)
        filename = f"{chat_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = _LOG_DIR / filename

        # Take last 10 messages from history
        last_messages = session.message_history[-10:]

        handoff_data = {
            "chat_id": chat_id,
            "trigger_reason": reason,
            "state_at_handoff": session.state,
            "car_brand": session.car_brand,
            "car_model": session.car_model,
            "car_year": session.car_year,
            "goal": session.goal,
            "last_10_messages": last_messages,
            "timestamp": timestamp.isoformat(),
        }

        filepath.write_text(
            json.dumps(handoff_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        logger.warning(
            f"HANDOFF logged for chat_id={chat_id}: {reason} → {filepath.name}"
        )

    except Exception as e:
        logger.error(f"Failed to write handoff log for chat_id={chat_id}: {e}")
