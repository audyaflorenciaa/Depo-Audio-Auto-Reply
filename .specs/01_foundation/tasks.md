# Spec 01 — Foundation: Build Tasks

> **Purpose:** Step-by-step checklist for building the Phase 1 foundation.
> Complete tasks in order. Do NOT skip ahead.

---

## Phase 1A — Project Scaffolding

- [x] **TASK-001:** Create the full folder structure as defined in `docs/PROJECT_CONTEXT.md`.
  - Create: `app/`, `app/prompts/`, `app/data/`, `docs/`, `.specs/01_foundation/`, `handoff_log/`, `tests/`
  - Create placeholder `__init__.py` in: `app/`, `tests/`
  - Create `.gitkeep` in: `handoff_log/`

- [x] **TASK-002:** Create `.gitignore`.
  - Must ignore: `.env`, `__pycache__/`, `*.pyc`, `handoff_log/*.json`, `.venv/`, `*.egg-info/`

- [x] **TASK-003:** Create `requirements.txt` with pinned versions:
  ```
  fastapi==0.111.0
  uvicorn[standard]==0.29.0
  httpx==0.27.0
  google-generativeai==0.7.0
  python-dotenv==1.0.1
  pydantic==2.7.0
  ```

- [x] **TASK-004:** Copy `docs/PROJECT_CONTEXT.md (Product Data section)` into `app/data/product_data.md` (the bot's internal copy).

---

## Phase 1B — Configuration

- [x] **TASK-005:** Implement `app/config.py`.
  - Load all env vars from `.env`.
  - Expose a `settings` singleton object.
  - Raise `ValueError` with clear message if `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, or `WEBHOOK_SECRET_PATH` are missing or empty.
  - Test: import `settings` in a Python REPL and confirm it loads correctly.

---

## Phase 1C — Session Store

- [x] **TASK-006:** Implement `app/session_store.py`.
  - Define `Session` Pydantic model with all fields from `docs/PROJECT_CONTEXT.md`.
  - Implement `get_session(chat_id: int) -> Session`.
  - Implement `save_session(chat_id: int, session: Session) -> None`.
  - Test: Create a session, save it, retrieve it, verify values.

---

## Phase 1D — Telegram Client

- [x] **TASK-007:** Implement `app/telegram_client.py`.
  - Implement `async send_message(chat_id, text, parse_mode="HTML")`.
  - Uses `httpx.AsyncClient`.
  - Logs success and failure. Does not raise on failure.
  - Test: Manually call `send_message` with your real bot token and your own Telegram `chat_id` to verify it sends.

---

## Phase 1E — LLM Client

- [x] **TASK-008:** Write `app/prompts/system_prompt.md`.
  - Must include: FSM state definitions, exact message templates, all 10 guardrail rules, JSON output schema.
  - Must NOT include the price list directly (it will be appended at runtime).
  - Reference: `docs/PROJECT_CONTEXT.md` for state definitions and guardrails.

- [x] **TASK-009:** Implement `app/llm_client.py`.
  - On module import, load `system_prompt.md` and `app/data/product_data.md` from disk.
  - Concatenate them into a single system instruction string.
  - Implement `async generate_response(chat_history: list[dict]) -> dict`.
  - Configure `GenerativeModel` with `temperature=0.1`, `response_mime_type="application/json"`.
  - Parse response text as JSON. Raise `ValueError` if not valid JSON.
  - Test: Send a mock user message and print the returned dict.

---

## Phase 1F — State Machine

- [x] **TASK-010:** Implement `app/state_machine.py`.
  - Implement `async process_message(chat_id: int, user_text: str) -> None`.
  - Logic sequence as defined in `docs/PROJECT_CONTEXT.md` Section 2.
  - Handle `handoff=true` case: set state, call `handoff_logger.log()`, do NOT call Gemini again.
  - If state is already `S9: HANDOFF`, immediately return without calling Gemini.
  - Test: Simulate 3 messages (greeting, car info, goal) and verify state progresses correctly.

---

## Phase 1G — Handoff Logger

- [x] **TASK-011:** Implement `app/handoff_logger.py`.
  - `log_handoff(chat_id, session, reason) -> None`
  - Creates directory `handoff_log/` if it does not exist.
  - Writes a JSON file: `handoff_log/{chat_id}_{YYYYMMDD_HHMMSS}.json`.
  - File must contain: `chat_id`, `trigger_reason`, `state_at_handoff`, `last_10_messages`, `car_brand`, `car_year`, `goal`.
  - Test: Call `log_handoff` with mock data and verify the file is created correctly.

---

## Phase 1H — FastAPI Server & Webhook

- [x] **TASK-012:** Implement `app/webhook.py`.
  - Define `POST /webhook/{secret_path}` endpoint.
  - Validate secret path. Return 403 if wrong.
  - Parse body as `TelegramUpdate` Pydantic model.
  - Extract `chat_id` and `text`. If `text` is None, send "Maaf, saya hanya bisa memproses pesan teks 😊" and return.
  - Call `state_machine.process_message()` inside a `try/except` block. Log all exceptions. Always return `{"ok": True}` (HTTP 200).

- [x] **TASK-013:** Implement `app/main.py`.
  - Create FastAPI app with title "DA AUTOLIGHT AI Bot".
  - Add `GET /health` route returning `{"status": "ok", "version": "0.1.0"}`.
  - Include router from `webhook.py`.
  - Add startup log confirming server is running.

---

## Phase 1I — Local Testing

- [x] **TASK-013b:** Create the `sessions` table in Supabase (SQL Editor). Schema is documented
  in `backend/app/session_store.py`'s docstring, and also in `README.md` / `CHANGELOG.md`
  (Session 8). Done by Calvin on 2026-09-21 (ran with RLS off, using the service key which
  bypasses RLS anyway — fine for backend access). Verified live: table is reachable, 0 rows.

- [x] **TASK-014:** Install dependencies: `pip install -r requirements.txt` (done for Calvin's
  machine in Session 8; Audya still needs to do this on her own machine).

- [x] **TASK-015:** Create `.env` from `.env.example` and fill in real values. (Done for Calvin;
  shared `.env` handed to Audya offline — she needs to place it in her `backend/` folder.)

- [x] **TASK-016:** Run the server: `uvicorn app.main:app --reload --port 8000`
  - Confirmed `/health` returns `{"status": "ok", "version": "0.1.0"}`. Server started cleanly,
    logged startup info showing Supabase URL and Gemini model loaded correctly. Verified live on
    Calvin's machine, 2026-09-21.

- [ ] **TASK-017:** Start ngrok: `ngrok http 8000`
  - Copy the HTTPS forwarding URL.

- [ ] **TASK-018:** Register Telegram webhook:
  ```
  https://api.telegram.org/bot{TOKEN}/setWebhook?url={NGROK_URL}/webhook/{SECRET_PATH}
  ```
  - Confirm response: `{"ok": true}`

- [ ] **TASK-019:** End-to-end test on Telegram.
  - Open your bot in Telegram.
  - Send `/start` or any message.
  - Verify: bot replies with the official DA AUTOLIGHT greeting.
  - Send: "Toyota Avanza 2020"
  - Verify: bot acknowledges car and asks about goal.
  - Send: "fungsi" (or "1")
  - Verify: bot sends the Foglamp price list.
  - Send: "mau booking"
  - Verify: bot triggers handoff message.
  - Check: `handoff_log/` directory contains a new `.json` file.

---

## Phase 1J — Tests

- [ ] **TASK-020:** Write `tests/test_state_machine.py`.
  - Test: first message → state S1 (greeted).
  - Test: providing car info → state S3.
  - Test: saying "fungsi" → state S5.
  - Test: saying "mau booking" → state S9 (handoff).

- [ ] **TASK-021:** Write `tests/test_webhook.py`.
  - Test: correct secret path → 200 OK.
  - Test: wrong secret path → 403 Forbidden.
  - Test: missing `message.text` → 200 OK + polite reply.

---

## Definition of Done (Phase 1)

The foundation is complete when:

- [ ] The FastAPI server starts without errors.
- [ ] The Telegram webhook is registered and verified.
- [ ] A real Telegram conversation completes the full 5-step flow (greeting → car info → goal → price list → handoff).
- [ ] The bot never invents prices not in `product_data.md`.
- [ ] A handoff log file is written on any handoff trigger.
- [ ] All tests in `tests/` pass.

---

## Phase 2 (Future) — Car Model → Lamp Size Compatibility Database

> **Status: PLANNED, NOT STARTED.** Decided by Calvin (2026-09-21): this is the chosen direction
> (Option B — a real compatibility lookup) over the simpler "always ask the customer" fallback.
> Do not build this until Phase 1 (local testing + basic conversation flow) is fully working.
> Until this exists, Phase 1's bot should ask the customer for their lamp size directly and
> hand off to a human staff member if the customer doesn't know it — this remains the Phase 1
> behavior in the meantime.

- [ ] **TASK-022:** Collect a small starter dataset (not the full catalogue) of car model → lamp
  size mappings from DA AUTOLIGHT staff, e.g.:
  ```
  Toyota Avanza (all years)   -> Foglamp 3 inch
  Honda Brio                  -> Foglamp 2 inch
  ```
  Start with ~5-10 common models seen in the shop, not an exhaustive list. This requires input
  from staff who know the actual installs — the agent cannot invent this data.

- [ ] **TASK-023:** Decide where this data lives (likely a new file, e.g.
  `backend/app/data/car_compatibility.md` or a Supabase table, similar pattern to `sessions`) —
  to be designed once the starter dataset exists and its shape is known.

- [ ] **TASK-024:** Update `state_machine.py` / `system_prompt.md` so the bot checks this data
  first; if the customer's car IS found, recommend the matching size; if NOT found, fall back to
  asking the customer directly, and hand off if they don't know — same safety behavior as Phase 1.

- [ ] **TASK-025:** Expand the dataset over time as staff provide more car models. This is
  expected to grow gradually, not be complete on day one.
