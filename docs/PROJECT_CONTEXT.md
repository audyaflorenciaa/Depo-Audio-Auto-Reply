# DA AUTOLIGHT AI — Master Project Context

> **FOR AI AGENT:** This is the SINGLE gateway file you need to read to understand the entire project. Do not search for other fragmented markdown files. All requirements, design, tech stack, flows, and product data are consolidated here.

---

## 1. Requirements

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


---

## 2. Design & Architecture

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


---

## 3. Tech Stack Reference

# DA AUTOLIGHT AI — Tech Stack Reference

> Detailed reference for the technology decisions, integration patterns, and deployment architecture.

---

## 1. Technology Decision Summary

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| **Language** | Python | 3.11+ | Mature ecosystem for AI/API integrations |
| **Web Framework** | FastAPI | 0.111+ | Async-first, auto Swagger docs, production-grade |
| **AI Engine** | Gemini 1.5 Flash | Latest | See decision rationale below |
| **Bot Platform** | Telegram Bot API | v7+ | Phase 1 testing; proven for automation |
| **Session Storage** | In-memory dict | — | Development; upgrade to Redis for production |
| **Session Storage (Prod)** | Redis | 7+ | Future — persistent, expirable session state |
| **Deployment** | uvicorn | 0.29+ | ASGI server for FastAPI |
| **Tunneling (Dev)** | ngrok | Latest | Expose localhost to Telegram webhook |
| **Environment Vars** | python-dotenv | 1.0+ | Load `.env` into environment |

---

## 2. AI Engine: Gemini 1.5 Flash — Decision Rationale

### Why not Llama 3 via Groq?

| Evaluation Criteria | Gemini 1.5 Flash | Llama 3 (Groq) | Winner |
|---|---|---|---|
| Structured JSON output | Native (`response_mime_type`) | Requires prompt engineering | Gemini |
| Instruction-following strictness | Very High (System instruction separation) | Good, but looser | Gemini |
| Latency | ~500ms avg | ~300ms avg | Groq (marginal) |
| Context window | 1M tokens | 128K tokens | Gemini |
| Free tier | 15 req/min, 1M tokens/day | 30 req/min | Comparable |
| Multimodal (future product images) | Native vision | Text only | Gemini |
| Hallucination guardrails | Excellent with grounding | Moderate | Gemini |
| Google ecosystem integration | Native | N/A | Gemini |

**Verdict:** Gemini 1.5 Flash wins on every dimension that matters for this use-case:
strict JSON state tracking, native structured output, and 1M token context to hold the entire product catalogue.

### How Gemini is used in this system

1. **System Instruction** (not a user message): Contains the full FSM rules, all guardrails, and the product data.
2. **User Turn**: The customer's message.
3. **Model Turn**: Gemini responds with a structured JSON object:

```json
{
  "next_state": "S5",
  "bot_message": "...",
  "extracted_entities": {
    "car_brand": "Toyota",
    "car_year": 2020,
    "goal": "FUNCTION"
  },
  "handoff": false,
  "handoff_reason": null
}
```

4. The FastAPI server parses this JSON, updates the session, and sends `bot_message` to Telegram.

---

## 3. FastAPI Server Architecture

### Entry Point: `app/main.py`

```python
from fastapi import FastAPI
app = FastAPI(title="DA AUTOLIGHT AI Bot")

# Routes registered:
# POST /webhook/{secret_path}  — Telegram sends updates here
# GET  /health                 — Health check endpoint
# GET  /docs                   — Auto-generated Swagger UI
```

### Request Flow

```
Telegram User sends message
         |
         v
Telegram API (sends POST to our webhook URL)
         |
         v
FastAPI: POST /webhook/{secret}
         |
         v
webhook.py: parse Update object, extract chat_id + message_text
         |
         v
state_machine.py: load session, determine current state
         |
         v
llm_client.py: build prompt with system instruction + chat history
         |
         v
Gemini 1.5 Flash API: returns JSON response
         |
         v
state_machine.py: parse JSON, update session state & entities
         |
         v
webhook.py: send bot_message back to Telegram via sendMessage API
         |
         v
(If handoff=true): write handoff log, stop AI replies
```

---

## 4. Telegram Bot API Integration

### Webhook vs. Polling

We use **Webhooks** (not polling). 

| Mode | How it works | When to use |
|---|---|---|
| **Polling** | Bot asks Telegram "any new messages?" every few seconds | Development/testing |
| **Webhook** | Telegram calls your server when a message arrives | Production & ngrok testing |

Webhooks are more efficient and production-appropriate.

### Setting the Webhook

```bash
curl -X POST "https://api.telegram.org/bot{TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-domain.com/webhook/{SECRET_PATH}"}'
```

### Sending a Reply

```python
import httpx

async def send_message(chat_id: int, text: str, token: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)
```

### Relevant Telegram API Endpoints Used

| Endpoint | Purpose |
|---|---|
| `POST /setWebhook` | Register our server URL |
| `GET /getWebhookInfo` | Check webhook status |
| `POST /sendMessage` | Send reply to user |
| `DELETE /deleteWebhook` | Remove webhook (switch to polling) |

---

## 5. Session State Management

### Phase 1: In-Memory (Development)

```python
# app/session_store.py
sessions: dict[int, dict] = {}  # chat_id -> session dict
```

Simple, no dependencies. Lost on server restart. Fine for development.

### Phase 2: Redis (Production)

```python
import redis.asyncio as redis

r = redis.Redis(host='localhost', port=6379)

async def get_session(chat_id: int) -> dict:
    data = await r.get(f"session:{chat_id}")
    return json.loads(data) if data else new_session()

async def save_session(chat_id: int, session: dict):
    await r.setex(f"session:{chat_id}", 86400, json.dumps(session))
    # 86400 seconds = 24 hours TTL
```

---

## 6. Gemini Integration

### Library

```bash
pip install google-generativeai
```

### Basic Usage Pattern

```python
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config=genai.types.GenerationConfig(
        response_mime_type="application/json",  # Force JSON output
        temperature=0.1,   # Low temperature = strict, less creative
        max_output_tokens=1024,
    )
)

response = model.generate_content(contents=chat_history)
result = json.loads(response.text)  # Always valid JSON
```

### Temperature Setting

We use **temperature = 0.1** (very low). This minimises randomness and hallucination,
making the model behave more like a deterministic rule-follower than a creative writer.

---

## 7. Environment Configuration

All secrets and configuration are loaded from `.env` via `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
APP_PORT = int(os.getenv("APP_PORT", 8000))
WEBHOOK_SECRET_PATH = os.getenv("WEBHOOK_SECRET_PATH")
HANDOFF_LOG_DIR = os.getenv("HANDOFF_LOG_DIR", "handoff_log")
```

---

## 8. Deployment Architecture

### Local Development

```
[Your Machine]
  uvicorn (port 8000)
       |
  ngrok tunnel
       |
  Telegram API (webhook)
```

### Production (Recommended Path)

```
[Cloud VM / VPS]
  uvicorn (port 8000)
       |
  nginx (reverse proxy, SSL termination)
       |
  Your domain (HTTPS required by Telegram)
       |
  Telegram API (webhook)
```

Recommended cloud providers for a small bot: **Railway**, **Render**, or **DigitalOcean** (cheapest to start).

---

## 9. Python Dependencies (`backend/requirements.txt`)

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
httpx==0.27.0
google-generativeai==0.7.0
python-dotenv==1.0.1
pydantic==2.7.0
```

Phase 2 additions (commented out in `requirements.txt` until needed):

```
redis==5.0.4
supabase==2.5.0
langchain==0.2.0
langchain-google-genai==1.0.6
chromadb==0.5.0
```

---

## 10. Phase 2: WhatsApp RAG Integration

> **Status: PLANNED — Do not implement until Phase 1 is complete and in production.**
>
> This section defines the architecture and strict rules for integrating WhatsApp chat history
> as a Retrieval-Augmented Generation (RAG) source for tone and conversation style matching.

### 10.1 Data Source

- WhatsApp chat history will be exported as raw `.txt` files directly from the WhatsApp mobile app.
- These files will be stored in: `backend/data/whatsapp_exports/` (gitignored — may contain PII).
- Each export represents a real past customer interaction handled by a human DA AUTOLIGHT staff member.

**How to export from WhatsApp (Human Task):**
1. Open the WhatsApp chat you want to export.
2. Tap the **three dots (⋮)** menu in the top right → tap **More**.
3. Tap **Export Chat**.
4. Select **Without Media** (we only need the text).
5. Save the `.txt` file and move it into `backend/data/whatsapp_exports/`.
6. Repeat for each conversation you want to include.

> **Volume target:** A minimum of **50–100 robust customer interactions** is recommended to build
> a vector database with sufficient coverage of tone variety, objection types, and conversation flows.

---

### 10.2 Embedding Purpose (STRICT BOUNDARY)

The vector embeddings generated from WhatsApp `.txt` files are used for **one purpose only**:

| Allowed (RAG retrieval FROM WhatsApp exports) | Forbidden |
|---|---|
| Human tone and language style (casual Indonesian) | Quoting prices |
| Conversation flow patterns (how staff guide customers) | Stock availability |
| Handling objections (e.g., "mahal ya?", "bisa dicicil?") | Product specifications |
| Polite closing phrases and trust-building sentences | Booking confirmations |

**Why this boundary exists:** WhatsApp chat history may contain outdated prices, informal negotiations,
or one-off deals that must NEVER be quoted to new customers. The structured `docs/product_data.md`
is the only authoritative source for any price information.

---

### 10.3 Strict Data Boundary Rule (Enforced at Prompt Level)

```
RULE: The bot is STRICTLY FORBIDDEN from quoting any price, stock level,
or product specification retrieved from WhatsApp .txt embeddings.

Prices MUST ALWAYS be retrieved from: docs/product_data.md
Stock MUST ALWAYS be marked as: "not available in Phase 1"
```

This rule must be encoded in:
1. The system prompt (`backend/app/prompts/system_prompt.md`) — as an explicit guardrail.
2. The RAG retrieval logic (`backend/app/rag_client.py` — Phase 2 module) — with a post-retrieval filter that strips any text containing currency symbols or price patterns (e.g., `Rp`, numeric ranges).

---

### 10.4 Phase 2 Tech Stack Additions

| Component | Technology | Purpose |
|---|---|---|
| Embedding model | `gemini-embedding-exp-03` | Convert WhatsApp text chunks to vectors |
| Vector database | ChromaDB (local) | Store and query embeddings; zero ops cost |
| RAG framework | LangChain | Orchestrate retrieval pipeline |
| Storage | `backend/data/vector_db/` | Persisted ChromaDB index (gitignored) |

### 10.5 Phase 2 RAG Pipeline (Planned Architecture)

```
[Human exports WhatsApp .txt]
         |
         v
[Preprocessing script: clean_exports.py]
  - Remove phone numbers, timestamps, media placeholders
  - Split into conversation chunks (per customer interaction)
         |
         v
[Embedding: gemini-embedding-exp-03]
  - Each chunk → 768-dim vector
         |
         v
[ChromaDB: backend/data/vector_db/]
  - Persisted locally
         |
         v
[At runtime: RAG retrieval in llm_client.py]
  - User message → query ChromaDB for top-3 similar conversation chunks
  - Retrieved chunks appended to Gemini system context as "tone examples"
  - Gemini uses tone examples to mirror DA AUTOLIGHT staff's communication style
```


---

## 4. Conversation Flow & State Machine

# DA AUTOLIGHT AI — Conversation Flow & State Machine

> This document defines the **complete conversation tree**, all valid state transitions,
> guardrail rules, and the human handoff trigger conditions.

---

## 1. State Machine Overview

The bot operates as a **strict finite-state machine (FSM)**. It does not hold a free-form conversation.
Every message from the user either advances the state forward, triggers clarification, or triggers handoff.

### State Definitions

| State ID | Name | Description |
|---|---|---|
| `S0` | `IDLE` | No conversation active yet |
| `S1` | `GREETED` | Bot sent the greeting; waiting for customer's first intent |
| `S2` | `GATHERING_CAR_INFO` | Asking for car brand and year |
| `S3` | `CAR_INFO_CONFIRMED` | Car brand and year captured |
| `S4` | `GOAL_ASSESSMENT` | Asking Function vs. Aesthetics preference |
| `S5` | `RECOMMENDATION_FUNCTION` | Customer wants function; showing Foglamp prices |
| `S6` | `RECOMMENDATION_AESTHETICS` | Customer wants aesthetics; showing Headlamp prices |
| `S7` | `RECOMMENDATION_BOTH` | Customer wants both; showing combo recommendation |
| `S8` | `FOLLOWUP` | Customer has follow-up question within scope |
| `S9` | `HANDOFF` | Conversation handed off to human staff |
| `S10` | `CLOSED` | Conversation completed |

---

## 2. State Transition Diagram

```
[S0: IDLE]
    |
    | User sends ANY message (first contact)
    v
[S1: GREETED]
    |  Bot sends official greeting (verbatim, no changes)
    |  Bot asks: "Ada yang bisa dibantu?"
    |
    | User responds (any intent)
    v
[S2: GATHERING_CAR_INFO]
    |  Bot asks: "Boleh tahu mobil apa dan tahun berapa?"
    |
    | User provides car brand + year
    v
[S3: CAR_INFO_CONFIRMED]
    |  Bot confirms: "Oke, untuk [Brand] tahun [Year]..."
    |
    | Immediately transitions to →
    v
[S4: GOAL_ASSESSMENT]
    |  Bot asks: Function vs. Aesthetics question
    |
    |--[User says FUNCTION]---------> [S5: RECOMMENDATION_FUNCTION]
    |                                      |
    |--[User says AESTHETICS]-------> [S6: RECOMMENDATION_AESTHETICS]
    |                                      |
    |--[User says BOTH]-------------> [S7: RECOMMENDATION_BOTH]
    |                                      |
    |--[User is unclear/off-script]-> [S9: HANDOFF]
    
[S5 / S6 / S7] --> [S8: FOLLOWUP] if user asks in-scope follow-up
[S5 / S6 / S7 / S8] --> [S9: HANDOFF] if user asks out-of-scope, wants to book, or is unpredictable
[S5 / S6 / S7 / S8] --> [S10: CLOSED] if user says thank you / goodbye
```

---

## 3. Exact Bot Messages Per State

### S1 — Official Greeting (VERBATIM — DO NOT MODIFY)

```
👋 Halo! Terima kasih sudah menghubungi DA AUTOLIGHT (Depo Audio).

📩 Jam operasional: 09.00 – 17.00 WIB
❌ Libur setiap hari SELASA (2 minggu sekali).

❓️ Untuk konsultasi offline bisa langsung datang ke workshop kami di Jakarta Timur.
💡 Bisa test cahaya langsung sampai benar-benar yakin sebelum pemasangan!

INSTAGRAM: https://www.instagram.com/variasi_depoaudio
TIKTOK: https://www.tiktok.com/@depoaudio_variasi
LOKASI: https://share.google/J1MXaIoQOvzN5qjmT

Ada yang bisa dibantu?
```

> **Rule:** This message must be sent character-for-character on first contact.
> The bot must not paraphrase, shorten, or translate it.

---

### S2 — Car Info Gathering

**Bot message:**
```
Boleh tahu mobil apa dan tahun berapa, Kak? 😊
Contoh: Toyota Avanza 2020, Honda Jazz 2018, dll.
```

**Entities to extract:**
- `car_brand` (string) — e.g., "Toyota", "Honda", "Mitsubishi"
- `car_year` (integer) — e.g., 2019
- `car_model` (string, optional) — e.g., "Avanza", "Pajero"

**Validation:**
- Year must be a plausible car year (1990–2026). Reject anything outside this range.
- If the user gives only the brand without the year (or vice versa), ask again specifically for what is missing.

---

### S3 — Car Info Confirmed

**Bot message (template — fill in extracted values):**
```
Oke, untuk [car_brand] [car_model] tahun [car_year] ya 👍

Sekarang, boleh tahu tujuannya apa?
```
Then immediately ask the goal question (transition to S4).

---

### S4 — Goal Assessment

**Bot message:**
```
Tujuan upgrade lampunya untuk apa nih, Kak?

1️⃣ FUNGSI — Ingin penerangan jalan yang lebih terang dan aman
2️⃣ ESTETIKA — Ingin tampilan lebih keren (demon eyes, DRL, variasi warna)
3️⃣ KEDUANYA — Ingin terang sekaligus keren

Ketik 1, 2, atau 3 ya 😊
```

**Intent mapping:**
- Keywords for FUNCTION: "terang", "jelas", "safety", "fungsi", "hujan", "kabut", "1", "function", "bright"
- Keywords for AESTHETICS: "keren", "gaya", "estetika", "demon", "RGB", "warna", "tampilan", "2", "aesthetics", "look"
- Keywords for BOTH: "keduanya", "dua-duanya", "both", "3"

---

### S5 — Recommendation: FUNCTION (Foglamp)

**Bot message:**
```
Untuk fungsi penerangan, kami rekomendasikan FOGLAMP! 💡

Foglamp dipasang di bawah bumper dan memberikan penerangan jarak dekat yang lebar, 
sehingga tekstur jalan lebih terlihat jelas — sangat bagus untuk berkendara malam atau hujan.

Berikut pilihan Foglamp kami:

--- FOGLAMP 3 INCH ---
PRO7:
• P7.F30 = Rp 2.600.000 (Putih)
• P 735 F SE = Rp 2.800.000 (Putih) ⭐ BEST SELLER
• P 735 FX = Rp 2.950.000 (Putih + Laser)
• P 735 F-3C Apps = Rp 3.250.000 (3 Warna, kontrol via Apps)
• P 755 F = Rp 3.700.000 (Putih sedikit Kuning)

UPS WAYMAKER:
• UPS UF-3 (1 Warna) = Rp 2.350.000 ⭐ BEST SELLER
• UPS UF-3 (3 Warna) = Rp 2.650.000
• UPS Waymaker F75 (Dual Laser) 3 Warna = Rp 3.000.000
• UPS Waymaker F55 3 Warna + Demon RGB = Rp 2.700.000

AES:
• Fx 3 inch 1 Warna = Rp 2.200.000
• Fx 3 inch 3 Warna = Rp 2.300.000
• Fx 3 inch Single Laser = Rp 2.400.000
• Fx 3 inch Double Laser = Rp 2.500.000

DA AUTOLIGHT (In-House):
• 3 inch 1 warna = Rp 1.800.000
• 3 inch 3 warna = Rp 1.900.000

--- FOGLAMP 2 INCH ---
PRO7:
• P 735F-M = Rp 2.600.000
• P 735FX-M (Laser) = Rp 2.900.000
• P735F-M 3C (3 Warna) = Rp 3.150.000

UPS WAYMAKER:
• UF-2 1 Warna = Rp 2.350.000 ⭐ BEST SELLER
• UF-2 3 Warna = Rp 2.500.000

AES:
• FX 2 Inch 1 Warna = Rp 2.200.000
• FX 2 Inch 3 Warna = Rp 2.300.000
• FX 2 Inch Single Laser = Rp 2.400.000
• FX 2 Inch Double Laser = Rp 2.500.000

*Semua harga sudah termasuk pemasangan, leveling, dan relay highbeam.

Ada yang mau ditanyakan soal produk di atas? 😊
Atau kalau mau langsung ke workshop, boleh test cahayanya dulu sebelum beli!
```

---

### S6 — Recommendation: AESTHETICS (Headlamp)

**Bot message:**
```
Untuk tampilan keren, kami rekomendasikan HEADLAMP upgrade! ✨

Headlamp memberikan tampilan OEM yang premium — terlihat seperti bawaan pabrik kelas atas,
dengan opsi Demon Eyes, DRL, dan variasi warna.

Berikut pilihan Headlamp kami:

--- HEADLAMP 3 INCH ---
PRO7:
• P 730 RV = Rp 3.500.000
• P 730 SL = Rp 3.500.000 (Khusus Pajero 2016+ & Fortuner GR)
• P 750 RV = Rp 4.500.000
• P 770 SV = Rp 5.200.000
• P 770 SL = Rp 5.500.000 (Khusus Pajero 2016+ & Fortuner GR)
• P 7RBX = Rp 5.500.000
• P 7MRX = Rp 7.500.000

UPS WAYMAKER:
• S500 V2 = Rp 4.300.000
• S600 = Rp 4.450.000 (Double Laser)
• SL850 = Rp 4.750.000 (Khusus Pajero 2016+ & Fortuner GR)
• G600 = Rp 4.850.000 (Pure Laser)

Harga Terjangkau:
• WST 3 Inch = Rp 2.650.000
• AES Bi-Laser Premium = Rp 3.200.000
• Kuro Raijin R65 = Rp 3.500.000

--- HEADLAMP 2 INCH ---
PRO7:
• P71MX = Rp 2.500.000/set
• P72MX = Rp 3.000.000/set
• P73MX = Rp 3.500.000/set

UPS WAYMAKER:
• SQ 300 = Rp 2.500.000/set
• SQ 600 = Rp 2.750.000/set
• SQ 800 = Rp 3.250.000/set

*Semua harga sudah termasuk pemasangan, poles mika, rakit soket, relay, selongsong kabel, solasi bakar, dan leveling laser.

Untuk inspirasi tampilan, cek IG & TikTok kami ya! 😍
📸 Instagram: https://www.instagram.com/variasi_depoaudio
🎵 TikTok: https://www.tiktok.com/@depoaudio_variasi

Ada pertanyaan lanjutan? 😊
```

---

### S9 — Human Handoff

**Trigger conditions (any of the following):**
1. Customer asks about a service not in the product list (e.g., wiring, sound system, other mods).
2. Customer wants to make a booking or appointment.
3. Customer asks for a discount or negotiation.
4. Customer provides a car that needs special compatibility check.
5. Customer's intent is ambiguous after 2 clarification attempts.
6. Customer sends inappropriate or non-automotive content.
7. Customer explicitly asks to speak to a human/staff.

**Bot message:**
```
Baik, saya akan sambungkan dengan tim kami untuk membantu lebih lanjut 🙏

Mohon tunggu sebentar ya, Kak. Tim kami akan segera merespons.

Atau bisa langsung hubungi kami / datang ke workshop di Jakarta Timur 😊
📍 https://share.google/J1MXaIoQOvzN5qjmT
```

**System action after handoff message:**
1. Set conversation state to `S9: HANDOFF`.
2. Write handoff log entry (timestamp, user ID, last 10 messages, trigger reason).
3. Stop AI auto-reply for this conversation (human takes over).
4. (Future) Ping the staff Telegram group with the customer's details.

---

## 4. Guardrail Rules

These rules are **non-negotiable** and must be enforced at the prompt level:

| Rule # | Rule |
|---|---|
| G1 | The bot MUST NEVER invent or estimate a price not in `product_data.md`. |
| G2 | The bot MUST NEVER promise stock availability (not yet implemented). |
| G3 | The bot MUST NEVER offer discounts or negotiate prices. |
| G4 | The bot MUST NEVER skip states (e.g., go from S1 directly to S5). |
| G5 | The bot MUST send the exact greeting text in S1, verbatim. |
| G6 | The bot MUST ask for car brand and year before giving any recommendation. |
| G7 | If unsure about a customer's intent after 2 tries, the bot MUST trigger handoff. |
| G8 | The bot MUST NOT answer general questions about cars, insurance, registration, etc. |
| G9 | All prices quoted must be copied exactly from `product_data.md`. |
| G10 | If a customer's car model has a special note (e.g., Pajero 2016+), bot must mention it. |

---

## 5. Session & Context Management

- Each Telegram user (`chat_id`) has an independent session.
- Session state is stored in memory (Redis in production, in-memory dict in development).
- Session data structure:

```json
{
  "chat_id": 123456789,
  "state": "S4",
  "car_brand": "Mitsubishi",
  "car_model": "Pajero Sport",
  "car_year": 2019,
  "goal": null,
  "handoff_reason": null,
  "message_history": [],
  "created_at": "2026-09-16T14:00:00+07:00",
  "updated_at": "2026-09-16T14:05:00+07:00"
}
```

- Sessions expire after **24 hours** of inactivity. Returning users start from S1.

---

## 6. Out-of-Scope Topics (Always Trigger Handoff)

- Car audio / sound systems
- Car window tinting
- Car wrapping / vinyl
- Engine or mechanical work
- Car insurance
- Price negotiations / discounts
- Booking appointments (Phase 1 — no booking system yet)
- Anything not related to automotive lighting products listed in `product_data.md`


---

## 5. Product Data & Price Lists

# DA AUTOLIGHT — Product Data & Price Lists

> **SOURCE OF TRUTH** — The bot is ONLY allowed to quote prices and product information from this file.
> It must NEVER invent, estimate, or interpolate prices that are not listed here.
> Last updated: September 2026.

---

## 📍 Workshop Info

- **Workshop Name:** DA AUTOLIGHT (Depo Audio)
- **Location:** Jakarta Timur (East Jakarta)
- **Operating Hours:** 09.00 – 17.00 WIB
- **Closed:** Every TUESDAY (every 2 weeks / 2 minggu sekali)
- **Instagram:** https://www.instagram.com/variasi_depoaudio
- **TikTok:** https://www.tiktok.com/@depoaudio_variasi
- **Google Maps:** https://share.google/J1MXaIoQOvzN5qjmT

---

## 🔦 Lamp Category Overview

Automotive lighting at DA AUTOLIGHT is divided into **3 main categories**:

| # | Category | Description |
|---|---|---|
| 1 | **Headlamp** | Primary vehicle lighting (OEM look) |
| 2 | **Foglamp** | Fog/support light mounted below the bumper |
| 3 | **Miniprojie** | Additional spotlight lamp |

---

## Category 1: HEADLAMP

**Role:** Primary vehicle lighting — OEM look.

**Advantages:**
- Wide, dense, and focused light beam
- Widest illumination coverage
- OEM look — appears factory-standard

**Available sizes:** 3 inch, 2.5 inch, 1.5 inch

---

### HEADLAMP — 3 INCH Bi-LED

> All prices below **include installation**, mirror polishing, socket-to-socket wiring, relay setup, cable sheathing, heat-shrink solder on every joint, and laser levelling.

#### Brand: PRO7

| Model | Price (IDR) | Notes |
|---|---|---|
| P 730 RV | Rp 3.500.000 | — |
| P 730 SL | Rp 3.500.000 | Khusus Pajero 2016+ dan Fortuner GR |
| P 750 RV | Rp 4.500.000 | — |
| P 770 SV | Rp 5.200.000 | — |
| P 770 SL | Rp 5.500.000 | Khusus Pajero 2016+ dan Fortuner GR |
| P 7RBX | Rp 5.500.000 | — |
| P 7MRX | Rp 7.500.000 | — |

#### Brand: UPS WAYMAKER

| Model | Price (IDR) | Notes |
|---|---|---|
| S500 V2 | Rp 4.300.000 | — |
| S600 | Rp 4.450.000 | Double laser |
| SL850 | Rp 4.750.000 | Khusus Pajero 2016+ dan Fortuner GR |
| G600 | Rp 4.850.000 | Pure Laser |

#### Affordable Options

| Model | Price (IDR) | Notes |
|---|---|---|
| WST 3 Inch | Rp 2.650.000 | — |
| AES Bi-Laser Premium | Rp 3.200.000 | — |
| Kuro Raijin R65 | Rp 3.500.000 | — |

---

### HEADLAMP — 2 INCH Bi-LED

> All prices include installation, relay (individual for low beam & high beam), mirror polishing, cable sheathing, heat-shrink solder, and solder joints.

#### Brand: PRO7

| Model | Price (IDR) |
|---|---|
| P71MX | Rp 2.500.000/set |
| P72MX | Rp 3.000.000/set |
| P73MX | Rp 3.500.000/set |

#### Brand: UPS WAYMAKER

| Model | Price (IDR) |
|---|---|
| SQ 300 | Rp 2.500.000/set |
| SQ 600 | Rp 2.750.000/set |
| SQ 800 | Rp 3.250.000/set |

---

## Category 2: FOGLAMP

**Role:** Low-mounted fog/support light for improved road surface visibility.

**Advantages:**
- Quick and easy installation
- Clearer illumination at low range
- Road texture more visible (safety advantage)

**Available sizes:** 3 inch, 2 inch

---

### FOGLAMP — 3 INCH Bi-LED

> All prices include installation, levelling, and relay for high beam.

#### Brand: PRO7

| Model | Price (IDR) | Notes |
|---|---|---|
| P7.F30 | Rp 2.600.000 | White |
| P 735 F SE | Rp 2.800.000 | White — **BEST SELLER** |
| P 735 FX | Rp 2.950.000 | White + Laser |
| P 735 F-3C Apps | Rp 3.250.000 | 3-colour app-controlled |
| P 755 F | Rp 3.700.000 | Warm white (slightly yellow) |

#### Brand: UPS WAYMAKER

| Model | Price (IDR) | Notes |
|---|---|---|
| UPS UF-3 (1 Colour) | Rp 2.350.000 | **BEST SELLER** |
| UPS UF-3 (3 Colour) | Rp 2.650.000 | — |
| UPS Waymaker F75 | Rp 3.000.000 | Dual Low Beam Laser, 3 colour |
| UPS Waymaker F55 | Rp 2.700.000 | 3 colour + Demon RGB |

#### Brand: AES

| Model | Price (IDR) | Notes |
|---|---|---|
| Fx 3 inch 1 Colour | Rp 2.200.000 | — |
| Fx 3 inch 3 Colour | Rp 2.300.000 | — |
| Fx 3 inch Single Laser | Rp 2.400.000 | — |
| Fx 3 inch Double Laser | Rp 2.500.000 | — |

#### Brand: DA AUTOLIGHT (In-House)

| Model | Price (IDR) | Notes |
|---|---|---|
| 3 inch 1 Colour | Rp 1.800.000 | Best-value entry option |
| 3 inch 3 Colour | Rp 1.900.000 | — |

> **Bracket Adaptor Foglamp:** Rp 150.000
> (Required for: Avanza New, Rush, Raize, Veloz, Sienta, and similar models)

---

### FOGLAMP — 2 INCH Bi-LED

> All prices include installation, high beam relay, cable sheathing, cable socket connector, and heat-shrink solder.

#### Brand: PRO7

| Model | Price (IDR) | Notes |
|---|---|---|
| P 735F-M | Rp 2.600.000 | — |
| P 735FX-M (Laser) | Rp 2.900.000 | — |
| P735F-M 3C | Rp 3.150.000 | 3 colour |

#### Brand: UPS WAYMAKER

| Model | Price (IDR) | Notes |
|---|---|---|
| UF-2 1 Colour | Rp 2.350.000 | **BEST SELLER** |
| UF-2 3 Colour | Rp 2.500.000 | — |

#### Brand: AES

| Model | Price (IDR) | Notes |
|---|---|---|
| FX 2 Inch 1 Colour | Rp 2.200.000 | — |
| FX 2 Inch 3 Colour | Rp 2.300.000 | — |
| FX 2 Inch Single Laser | Rp 2.400.000 | — |
| FX 2 Inch Double Laser | Rp 2.500.000 | — |

---

## Category 3: MINIPROJIE (Spotlight / Additional Lamp)

**Role:** Extra focused spotlight for rain, fog, and storm conditions.

**Special Feature: LIFETIME WARRANTY**

**Variants:** 1-mata (1 lens), 2-mata (2 lens), 3-mata (3 lens)

---

### MINIPROJIE — PRO7

> All prices include installation, levelling, relay set for individual high beam and low beam, cable sheathing, heat-shrink solder on all joints.

#### Series TX (Full Set = 4 pcs)

| Model | Price (IDR) |
|---|---|
| MP 1 TX | Rp 2.800.000 |
| MP 1 TX-S | Rp 2.800.000 |
| MP 2 TX | Rp 4.200.000 |
| MP 3 TX | Rp 5.400.000 |

#### Series TX (Half Set = 2 pcs)

| Model | Price (IDR) |
|---|---|
| MP 1 TX | Rp 1.500.000 |
| MP 1 TX-S | Rp 1.500.000 |
| MP 2 TX | Rp 2.400.000 |
| MP 3 TX | Rp 3.000.000 |

#### Series 9 (Older Generation)

| Model | Price (IDR) |
|---|---|
| Mp 9.2 | Rp 1.800.000 |
| Mp 9.3 | Rp 2.400.000 |

#### Series 7

| Model | Price (IDR) |
|---|---|
| Mp 7.3 | Rp 2.100.000 |

---

### MINIPROJIE — KURO RAIJIN

| Model | Price (IDR) | Notes |
|---|---|---|
| Kuro Raijin 1 Lens-Slim (4 pcs) | Rp 2.600.000 | — |
| Kuro Raijin 1 Lens-Slim (2 pcs) | Rp 1.400.000 | — |
| Kuro Raijin 2 Lens (2 pcs) | Rp 1.950.000 | — |

---

## 📌 Bot Recommendation Logic

Use this table to map customer **Goal** to the correct product category:

| Customer Goal | Primary Recommendation | Secondary Suggestion |
|---|---|---|
| **Function** (bright road visibility) | **Foglamp** (start with best seller) | Miniprojie (extra spotlight) |
| **Aesthetics** (looks, demon eyes, style) | **Headlamp** (custom look) | Foglamp with Demon RGB or 3-colour |
| **Both** | Headlamp + Foglamp combo | Miniprojie as add-on |

---

## 📌 Walk-in Consultation Note

> "Kalau bingung mampir aja, boleh kok main dulu ke workshop untuk test cahaya dan konsultasi. Ga harus langsung beli 😁🙏"
> (Feel free to drop by the workshop to test the lights and consult. No purchase required!)

This message should always be included when the customer seems hesitant or asks for more information.


---

