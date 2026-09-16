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
