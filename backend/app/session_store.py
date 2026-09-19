"""
DA AUTOLIGHT AI — Session Store Module

Manages per-user conversation sessions. Sessions are persisted in a
Supabase table called `sessions` so they survive server restarts.

Supabase table schema (create this in Supabase SQL Editor):
────────────────────────────────────────────────────────────
CREATE TABLE sessions (
    chat_id       BIGINT PRIMARY KEY,
    state         TEXT NOT NULL DEFAULT 'S0',
    car_brand     TEXT,
    car_model     TEXT,
    car_year      INTEGER,
    goal          TEXT,
    handoff       BOOLEAN NOT NULL DEFAULT FALSE,
    handoff_reason TEXT,
    message_history JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
────────────────────────────────────────────────────────────
"""

import json
import logging
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from app.supabase_client import supabase

logger = logging.getLogger(__name__)


# ── Session Pydantic Model ─────────────────────────────────────
class Session(BaseModel):
    """Represents a single user's conversation session."""

    chat_id: int
    state: str = "S0"
    car_brand: Optional[str] = None
    car_model: Optional[str] = None
    car_year: Optional[int] = None
    goal: Optional[str] = None  # "FUNCTION" | "AESTHETICS" | "BOTH"
    handoff: bool = False
    handoff_reason: Optional[str] = None
    message_history: list[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── CRUD Functions ─────────────────────────────────────────────

def get_session(chat_id: int) -> Session:
    """
    Retrieve an existing session from Supabase, or create a new one
    if no session exists for this chat_id.
    """
    try:
        result = (
            supabase.table("sessions")
            .select("*")
            .eq("chat_id", chat_id)
            .execute()
        )

        if result.data and len(result.data) > 0:
            row = result.data[0]
            # Parse message_history — Supabase returns it as a JSON string or list
            msg_history = row.get("message_history", [])
            if isinstance(msg_history, str):
                msg_history = json.loads(msg_history)

            return Session(
                chat_id=row["chat_id"],
                state=row.get("state", "S0"),
                car_brand=row.get("car_brand"),
                car_model=row.get("car_model"),
                car_year=row.get("car_year"),
                goal=row.get("goal"),
                handoff=row.get("handoff", False),
                handoff_reason=row.get("handoff_reason"),
                message_history=msg_history,
                created_at=row.get("created_at", datetime.now(timezone.utc)),
                updated_at=row.get("updated_at", datetime.now(timezone.utc)),
            )
        else:
            # No existing session — create a fresh one
            logger.info(f"New session created for chat_id={chat_id}")
            session = Session(chat_id=chat_id)
            save_session(chat_id, session)
            return session

    except Exception as e:
        logger.error(f"Error loading session for chat_id={chat_id}: {e}")
        # Fallback: return a fresh in-memory session so the bot doesn't crash
        return Session(chat_id=chat_id)


def save_session(chat_id: int, session: Session) -> None:
    """
    Upsert (insert or update) the session into Supabase.
    Uses Supabase's upsert to handle both new and existing sessions.
    """
    try:
        data = {
            "chat_id": chat_id,
            "state": session.state,
            "car_brand": session.car_brand,
            "car_model": session.car_model,
            "car_year": session.car_year,
            "goal": session.goal,
            "handoff": session.handoff,
            "handoff_reason": session.handoff_reason,
            "message_history": json.dumps(
                session.message_history, ensure_ascii=False
            ),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        supabase.table("sessions").upsert(data).execute()
        logger.debug(f"Session saved for chat_id={chat_id}, state={session.state}")

    except Exception as e:
        logger.error(f"Error saving session for chat_id={chat_id}: {e}")
