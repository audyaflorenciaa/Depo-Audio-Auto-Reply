# Spec 01 — Foundation: Requirements

> **Scope:** This specification covers only the foundational layer of DA AUTOLIGHT AI.
> Goal: A working FastAPI server that accepts Telegram webhook messages and returns a bot reply.

---

## 1. Functional Requirements

### FR-01: FastAPI Server Initialization
- The system SHALL expose a FastAPI HTTP server.
- The server SHALL start successfully with `uvicorn app.main:app`.
- The server SHALL expose a `GET /health` endpoint that returns `{"status": "ok"}`.

### FR-02: Telegram Webhook Endpoint
- The server SHALL expose a `POST /webhook/{secret_path}` endpoint.
- The endpoint SHALL accept Telegram's `Update` JSON payload.
- The `secret_path` MUST be validated against the `WEBHOOK_SECRET_PATH` env variable.
- If the secret is wrong, the endpoint SHALL return HTTP 403 Forbidden.
- The endpoint SHALL return HTTP 200 OK to Telegram immediately (even if processing fails), to prevent Telegram from retrying.

### FR-03: Message Parsing
- The system SHALL extract `chat_id` and `message.text` from the incoming `Update` payload.
- Non-text messages (photos, stickers, etc.) SHALL be handled gracefully — the bot sends a polite "text only" response.

### FR-04: Session Management
- The system SHALL maintain a per-user session keyed by `chat_id`.
- In Phase 1, sessions SHALL be stored in-memory (a Python dictionary).
- Sessions SHALL contain: `state`, `car_brand`, `car_model`, `car_year`, `goal`, `handoff`, `message_history`.
- Sessions SHALL be initialised with state `S0: IDLE` on first contact.

### FR-05: LLM Integration
- The system SHALL call Gemini 1.5 Flash for every user message (after session is loaded).
- The system instruction SHALL be loaded from `app/prompts/system_prompt.md` at startup.
- Product data SHALL be loaded from `app/data/product_data.md` and injected into the system instruction.
- Gemini SHALL be called with `response_mime_type="application/json"` to enforce structured output.
- Temperature SHALL be set to `0.1`.

### FR-06: State Machine Logic
- The system SHALL parse Gemini's JSON response to extract `next_state` and `bot_message`.
- The session state SHALL be updated to `next_state` after each response.
- Extracted entities (car_brand, car_year, goal) SHALL be written to session.

### FR-07: Telegram Reply
- The system SHALL send `bot_message` back to the user via Telegram's `sendMessage` API.
- The reply SHALL use `parse_mode="HTML"` to support basic formatting.

### FR-08: Human Handoff
- If Gemini returns `"handoff": true`, the system SHALL:
  1. Send the handoff message to the user.
  2. Set the session state to `S9: HANDOFF`.
  3. Write a handoff log file to the `handoff_log/` directory.
  4. Stop calling Gemini for this `chat_id` until the session is reset.

### FR-09: Environment Variable Loading
- All secrets SHALL be loaded from a `.env` file via `python-dotenv`.
- The server SHALL fail to start with a clear error message if required env vars are missing.

---

## 2. Non-Functional Requirements

### NFR-01: Response Time
- The bot SHALL respond to a user message within **5 seconds** under normal conditions.
- Gemini API timeout SHALL be set to **10 seconds**.

### NFR-02: Reliability
- The webhook endpoint SHALL never crash on malformed input — it must catch all exceptions and return HTTP 200 to Telegram.
- All exceptions SHALL be logged with the full traceback.

### NFR-03: Security
- The webhook path SHALL include a secret token to prevent unauthorised POSTs.
- API keys SHALL never be logged or exposed in error messages.

### NFR-04: Observability
- All state transitions SHALL be logged (INFO level) with `chat_id` and `state`.
- Handoff events SHALL be logged (WARNING level) with the trigger reason.
- Gemini API errors SHALL be logged (ERROR level).

### NFR-05: Portability
- The system SHALL run on Python 3.11+ on Windows, macOS, and Linux without modification.

---

## 3. Out of Scope for Phase 1

- Booking / appointment scheduling
- Stock management / inventory
- Redis session storage (in-memory only in Phase 1)
- Staff notification system (Telegram group ping)
- Image / multimedia handling
- Analytics dashboard
- Multi-language support
- Rate limiting
