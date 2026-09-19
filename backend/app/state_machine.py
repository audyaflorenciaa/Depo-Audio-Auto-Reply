"""
DA AUTOLIGHT AI — State Machine Module

The brain of the bot. Orchestrates the full message processing pipeline:
  1. Load session from Supabase
  2. Check if conversation is in HANDOFF state (skip if so)
  3. Build chat history for Gemini
  4. Call Gemini for a structured JSON response
  5. Update session with new state and extracted entities
  6. If handoff, log the handoff event
  7. Send bot message back to Telegram
"""

import logging

from app.session_store import get_session, save_session
from app.llm_client import generate_response, LLMError
from app.telegram_client import send_message
from app.handoff_logger import log_handoff

logger = logging.getLogger(__name__)


async def process_message(chat_id: int, user_text: str) -> None:
    """
    Process a single incoming user message end-to-end.

    Args:
        chat_id: Telegram chat ID of the user.
        user_text: The text message sent by the user.
    """
    # ── Step 1: Load session ───────────────────────────────────
    session = get_session(chat_id)

    # ── Step 2: Check if already handed off ────────────────────
    if session.state == "S9":
        logger.info(
            f"chat_id={chat_id} is in HANDOFF state. Ignoring message."
        )
        return

    # ── Step 3: Append user message to history ─────────────────
    session.message_history.append(
        {"role": "user", "parts": [user_text]}
    )

    # ── Step 4: Call Gemini ─────────────────────────────────────
    try:
        llm_result = await generate_response(session.message_history)
    except LLMError as e:
        logger.error(f"LLM error for chat_id={chat_id}: {e}")
        await send_message(
            chat_id,
            "Maaf, terjadi kesalahan sistem. Silakan coba lagi dalam "
            "beberapa saat 🙏",
        )
        return

    # ── Step 5: Parse and update session ───────────────────────
    bot_message = llm_result.get("bot_message", "")
    next_state = llm_result.get("next_state", session.state)
    entities = llm_result.get("extracted_entities", {})
    is_handoff = llm_result.get("handoff", False)
    handoff_reason = llm_result.get("handoff_reason")

    # Update state
    old_state = session.state
    session.state = next_state

    # Update extracted entities (only if provided / non-null)
    if entities.get("car_brand"):
        session.car_brand = entities["car_brand"]
    if entities.get("car_model"):
        session.car_model = entities["car_model"]
    if entities.get("car_year"):
        session.car_year = entities["car_year"]
    if entities.get("goal"):
        session.goal = entities["goal"]

    # Append model response to history
    session.message_history.append(
        {"role": "model", "parts": [bot_message]}
    )

    logger.info(
        f"chat_id={chat_id}: {old_state} → {next_state}"
        f"{' [HANDOFF]' if is_handoff else ''}"
    )

    # ── Step 6: Handle handoff ─────────────────────────────────
    if is_handoff:
        session.state = "S9"
        session.handoff = True
        session.handoff_reason = handoff_reason
        log_handoff(chat_id, session, handoff_reason or "Unknown reason")

    # ── Step 7: Save session to Supabase ───────────────────────
    save_session(chat_id, session)

    # ── Step 8: Send reply to Telegram ─────────────────────────
    if bot_message:
        await send_message(chat_id, bot_message)
