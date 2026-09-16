# Spec 01 — Foundation: Design

> **Purpose:** Define the monorepo folder structure, module responsibilities, data contracts, and design decisions for the foundation layer.
>
> **Last updated:** 2026-09-16 — Restructured to monorepo layout (backend / frontend / database separation).

---

## Changelog

| Date | Change |
|---|---|
| 2026-09-16 | Initial design document created (flat structure) |
| 2026-09-16 | Refactored to monorepo. `backend/` isolated. `frontend/` and `database/` stubs added. WhatsApp RAG Phase 2 stubs documented. |

---

## What To Do Next

- [ ] Human developer: complete manual setup steps in `README.md` (BotFather, Gemini key, .env)
- [ ] Human developer: initialize Python venv inside `backend/` (see README.md Step 5)
- [ ] Agent: write `backend/app/` Python source files (tasks defined in `tasks.md`)
- [ ] Agent: write `backend/app/prompts/system_prompt.md` (LLM system instruction)

---

## 1. Monorepo Folder Structure

```
Depo Audio Auto-Reply/              ← Workspace root (git root)
│
├── backend/                        ← Python FastAPI bot server
│   ├── app/                        ← Application source code (written in Phase 1)
│   │   ├── __init__.py
│   │   ├── main.py                 ← FastAPI app factory & lifespan startup
│   │   ├── config.py               ← Load & validate all env vars at startup
│   │   ├── webhook.py              ← POST /webhook/{secret} route handler
│   │   ├── state_machine.py        ← FSM logic: state transitions, handoff checks
│   │   ├── llm_client.py           ← Gemini 1.5 Flash API wrapper
│   │   ├── session_store.py        ← In-memory session CRUD (Phase 1)
│   │   ├── telegram_client.py      ← Telegram Bot API HTTP wrapper
│   │   ├── handoff_logger.py       ← Write handoff events to disk
│   │   │
│   │   ├── prompts/
│   │   │   └── system_prompt.md    ← LLM system instruction (loaded at startup)
│   │   │
│   │   └── data/
│   │       └── product_data.md     ← Internal copy of price list (injected into prompt)
│   │
│   ├── handoff_log/                ← Auto-created; stores handoff .json files
│   │   └── .gitkeep
│   │
│   ├── tests/                      ← Unit and integration tests
│   │   ├── __init__.py
│   │   ├── test_state_machine.py
│   │   └── test_webhook.py
│   │
│   ├── requirements.txt            ← Python dependencies (Phase 1 + Phase 2 stubs)
│   ├── .env.example                ← Template for ALL environment variables
│   ├── .env                        ← YOUR secrets (gitignored — never commit)
│   └── .gitignore                  ← Backend-specific ignores
│
├── frontend/                       ← [FUTURE] Admin dashboard (React/Next.js)
│   └── .gitkeep
│
├── database/                       ← [FUTURE] Supabase schema & migrations
│   └── .gitkeep
│
├── docs/                           ← Human-readable documentation (shared)
│   ├── product_data.md             ← Master product catalogue (source of truth)
│   ├── bot_flow.md                 ← FSM diagram, state messages, guardrails
│   └── tech_stack.md               ← Technology decisions, architecture, Phase 2 RAG rules
│
├── .specs/                         ← Engineering specifications
│   └── 01_foundation/
│       ├── requirements.md         ← What the system must do (FR & NFR)
│       ├── design.md               ← THIS FILE — monorepo structure & contracts
│       └── tasks.md                ← Step-by-step build checklist
│
├── .gitignore                      ← Root-level ignores (global)
├── .env.example                    ← Root-level env template (mirrors backend/.env.example)
└── README.md                       ← Vibe Coder setup guide (always kept up to date)
```

---

## 2. Module Responsibilities

> All Python modules live inside `backend/app/`.

### `backend/app/main.py`
- Creates the FastAPI application instance.
- Registers all routes (webhook, health check).
- Handles application **lifespan**: loads `system_prompt.md` and `product_data.md` into memory on startup.
- Ensures required env vars are present before the server starts (fails fast).

### `backend/app/config.py`
- Uses `python-dotenv` + `os.getenv` to load all env vars from `backend/.env`.
- Exposes a single `settings` singleton imported by all other modules.
- Raises `ValueError` with a clear, descriptive message if any required var is missing or empty.

### `backend/app/webhook.py`
- Defines the `POST /webhook/{secret_path}` route.
- Validates `secret_path` against `settings.WEBHOOK_SECRET_PATH` → returns HTTP 403 if wrong.
- Parses the incoming `Update` JSON using a Pydantic model.
- Calls `state_machine.process_message()` inside a try/except.
- **Always returns HTTP 200** to Telegram (prevents retry loops).

### `backend/app/state_machine.py`
- The brain of the bot.
- `process_message(chat_id, user_text) -> None`:
  1. Loads session from `session_store`.
  2. If state is `S9: HANDOFF` → returns immediately (human has taken over).
  3. Builds conversation history for Gemini.
  4. Calls `llm_client.generate_response()`.
  5. Parses JSON response.
  6. Updates session (new state, extracted entities).
  7. If `handoff=true` → calls `handoff_logger.log()`, sets state to `S9`.
  8. Calls `telegram_client.send_message()` with `bot_message`.

### `backend/app/llm_client.py`
- Wraps the `google-generativeai` SDK.
- On module load: reads `system_prompt.md` + `product_data.md` → concatenates into a single system instruction string.
- `async generate_response(chat_history: list[dict]) -> dict`:
  - Configures `GenerativeModel` with `temperature=0.1`, `response_mime_type="application/json"`.
  - Calls `model.generate_content()`.
  - Returns parsed JSON dict.
  - Raises `LLMError` on failure.

### `backend/app/session_store.py`
- In-memory dict: `_store: dict[int, Session]`.
- `get_session(chat_id: int) -> Session` — returns existing session or initialises a new one.
- `save_session(chat_id: int, session: Session) -> None`.
- `Session` is a Pydantic model (see data contracts below).

### `backend/app/telegram_client.py`
- `async send_message(chat_id, text, parse_mode="HTML") -> None`
- Uses `httpx.AsyncClient` to call `api.telegram.org/bot{TOKEN}/sendMessage`.
- Retries once on network timeout. Logs errors but does not raise (bot must stay alive).

### `backend/app/handoff_logger.py`
- `log_handoff(chat_id, session, reason) -> None`
- Creates `handoff_log/` directory if it does not exist.
- Writes: `handoff_log/{chat_id}_{YYYYMMDD_HHMMSS}.json`.
- File contains: `chat_id`, `trigger_reason`, `state_at_handoff`, `last_10_messages`, `car_brand`, `car_year`, `goal`.

### `backend/app/prompts/system_prompt.md`
- The authoritative LLM system instruction file.
- Contains: FSM state definitions, exact verbatim bot messages, all 10 guardrail rules, JSON output schema.
- **Product data is NOT stored here** — it is appended at runtime from `backend/app/data/product_data.md`.
- Editing this file changes the bot's behaviour without touching Python code.

---

## 3. Data Contracts

### Session Model (Pydantic)

```python
class Session(BaseModel):
    chat_id: int
    state: str = "S0"            # Current FSM state ID (S0–S10)
    car_brand: str | None = None
    car_model: str | None = None
    car_year: int | None = None
    goal: str | None = None      # "FUNCTION" | "AESTHETICS" | "BOTH"
    handoff: bool = False
    handoff_reason: str | None = None
    message_history: list[dict] = []  # [{role: "user"|"model", parts: [text]}]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Gemini Response Schema (JSON)

The LLM must always return a JSON object matching this exact schema:

```json
{
  "next_state": "S5",
  "bot_message": "Untuk fungsi penerangan, kami rekomendasikan FOGLAMP! ...",
  "extracted_entities": {
    "car_brand": "Toyota",
    "car_model": "Avanza",
    "car_year": 2020,
    "goal": "FUNCTION"
  },
  "handoff": false,
  "handoff_reason": null
}
```

- All fields are required.
- `extracted_entities` values default to `null` if not yet captured.
- `handoff_reason` must be a descriptive string if `handoff: true`, else `null`.

### Telegram Update Model (Pydantic)

```python
class TelegramMessage(BaseModel):
    message_id: int
    text: str | None = None
    chat: dict  # contains "id" (the chat_id integer)

class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None
```

---

## 4. Design Decisions

### Decision 1: Why JSON mode for Gemini?
`response_mime_type="application/json"` forces Gemini to always return valid JSON. This eliminates free-text parsing and prevents the model from appending conversational text outside the schema. It is the single most important reliability mechanism.

### Decision 2: Why load system prompt from a `.md` file?
Prompt engineering is iterative. Loading from a file means prompts can be edited and git-tracked without touching Python code. Non-engineers can adjust bot behaviour by editing markdown.

### Decision 3: Why in-memory sessions in Phase 1?
Zero operational complexity during development. No Redis needed. The trade-off (sessions lost on restart) is acceptable while the bot is not in production.

### Decision 4: Why always return HTTP 200 to Telegram?
Telegram retries delivery on non-200 responses, causing infinite retry loops on errors. Always returning 200 and handling errors internally prevents this.

### Decision 5: Why secret path in webhook URL?
Telegram's free tier does not support webhook signature verification. A secret token in the URL path is the simplest effective defence against unauthorised POSTs.

### Decision 6: Why a monorepo structure?
`backend/`, `frontend/`, and `database/` have fundamentally different toolchains (Python, Node.js, SQL). Separating them prevents dependency conflicts and makes it clear which part of the stack each file belongs to while keeping everything in one versioned repository.

---

## 5. Phase 2 Stubs (Do Not Build Yet)

The following are documented here so the Phase 1 architecture does not conflict with them.

### WhatsApp RAG Pipeline
- Input: `.txt` files from WhatsApp chat exports, stored in `backend/data/whatsapp_exports/`
- Process: Embed using Gemini embedding model → store in ChromaDB at `backend/data/vector_db/`
- Usage: Semantic retrieval of **tone**, **conversation flow**, and **objection handling** patterns ONLY.
- Strict boundary: RAG embeddings MUST NOT be used to quote prices. Prices always come from `docs/product_data.md`.

### Supabase Integration
- `database/` will hold SQL schema migrations for: product inventory, session persistence, staff management.

### Admin Dashboard
- `frontend/` will hold a Next.js admin dashboard for: live conversation monitoring, handoff queue, inventory CRUD.
