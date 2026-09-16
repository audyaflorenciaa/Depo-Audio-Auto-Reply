# 🚗💡 DA AUTOLIGHT AI — Auto-Reply Chatbot

> **Vibe Coder Guide** — written for a total beginner. No fluff, just the exact steps you need.
>
> **Always kept up to date** by the IDE agent after every code change session.

---

## 📋 What is this?

This is the backend bot for **DA AUTOLIGHT (Depo Audio)** — an automotive lighting workshop in East Jakarta. It is a Telegram chatbot that automatically:
1. Greets customers with DA AUTOLIGHT's official message.
2. Asks for their car brand and year.
3. Asks whether they want **function** (bright light) or **aesthetics** (demon eyes, style).
4. Recommends and quotes the **exact price** from our product catalogue — no hallucinations.
5. Hands off to a human staff if the conversation goes off-script.

---

## 🗂️ Monorepo Structure (Quick Overview)

```
Depo Audio Auto-Reply/
├── backend/           ← Python FastAPI bot (work happens here in Phase 1)
│   ├── app/           ← Bot source code (to be written next)
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/          ← [FUTURE] Admin dashboard
├── database/          ← [FUTURE] Supabase schema & migrations
├── docs/              ← Architecture & product documentation
└── .specs/            ← Engineering specifications & task checklists
```

---

## 📅 Changelog (Agent Sessions)

| Date | Session Summary |
|---|---|
| 2026-09-16 | **Session 1:** Generated all foundation `.md` files (README, .env.example, docs/, .specs/) |
| 2026-09-16 | **Session 2:** Restructured to monorepo. Created `backend/`, `frontend/`, `database/` skeleton. Added WhatsApp RAG Phase 2 rules to `tech_stack.md`. Updated `design.md` to reflect new paths. |

---

## ✅ What Needs To Be Done RIGHT NOW (Human Developer Tasks)

> Complete these steps before the next agent session writes any Python code.

### STEP 1 — Verify Python is installed

Open **PowerShell** and run:

```powershell
python --version
```

You should see `Python 3.11.x` or higher. If not, download from https://www.python.org/downloads/

---

### STEP 2 — Get your Telegram Bot Token (via BotFather)

1. Open Telegram → search for **`@BotFather`** → open the chat.
2. Send: `/newbot`
3. Name: `DA AUTOLIGHT AI`
4. Username: `DA_Autolight_bot` (must end in `bot`)
5. Copy the token BotFather gives you (format: `123456789:ABCDefGhIJKlmNoPQRsTUVwxYZ`)

> ⚠️ Never share this token. Anyone who has it can control your bot.

---

### STEP 3 — Get your Gemini API Key (Google AI Studio)

1. Go to: **https://aistudio.google.com/**
2. Sign in with your Google account.
3. Click **"Get API Key"** → **"Create API Key"** → select or create a project.
4. Copy the key (starts with `AIza...`)

> ⚠️ Keep this key secret. Usage costs money if someone else uses it.

---

### STEP 4 — Create your `.env` file

1. Open the `backend/` folder.
2. Copy `.env.example` → rename to `.env`
3. Fill in:

```
TELEGRAM_BOT_TOKEN=<paste your token from Step 2>
GEMINI_API_KEY=<paste your key from Step 3>
WEBHOOK_SECRET_PATH=<generate a random string — see below>
```

**Generate a random secret path** (run this in PowerShell):

```powershell
python -c "import secrets; print(secrets.token_hex(16))"
```

Copy the output and paste it as `WEBHOOK_SECRET_PATH`.

> `.env` is already in `.gitignore`. Never commit it.

---

### STEP 5 — Create and activate the Python virtual environment

Open PowerShell **inside the `backend/` folder**:

```powershell
# Navigate to backend folder
cd "c:\Users\ASUS\Documents\Depo Audio Auto-Reply\backend"

# Create virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# You should see (.venv) at the start of your prompt
# Now install dependencies
pip install -r requirements.txt
```

> If you get a script execution error, run this first:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### STEP 6 — Install ngrok (for local testing)

ngrok creates a public HTTPS tunnel to your local machine so Telegram can reach it.

1. Go to: **https://ngrok.com/download**
2. Download for Windows → extract `ngrok.exe` anywhere on your computer.
3. Sign up for a free account at ngrok.com → copy your **authtoken**.
4. Run once to register:

```powershell
ngrok config add-authtoken <your-authtoken>
```

---

### STEP 7 — (Future) WhatsApp Chat Export for Phase 2

This does NOT need to be done now. When Phase 2 begins, you will need to export past WhatsApp conversations with real DA AUTOLIGHT customers:

1. Open any customer chat in WhatsApp.
2. Tap **⋮ (three dots)** → **More** → **Export Chat** → **Without Media**.
3. Save each `.txt` file into: `backend/data/whatsapp_exports/`
4. Aim for **50–100 real customer interactions** for a strong tone-matching database.

> See `docs/tech_stack.md` → Section 10 for the full RAG rules and strict data boundary.

---

## 🚀 Running the Bot (After Code is Written)

> The Python application code has NOT been written yet. These commands will work after the agent writes Phase 1 code.

```powershell
# From the backend/ folder with .venv active:
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
ngrok http 8000
```

Copy the ngrok HTTPS URL, then register the Telegram webhook:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<NGROK_URL>/webhook/<WEBHOOK_SECRET_PATH>
```

---

## 🧠 AI Engine

**Gemini 1.5 Flash** (chosen over Llama 3 / Groq)

| Criteria | Gemini 1.5 Flash | Llama 3 (Groq) |
|---|---|---|
| Structured JSON output | Excellent (native) | Good (prompt only) |
| Instruction-following | Very High | Medium |
| Context window | 1M tokens | 128K tokens |
| Future vision support | Yes | No |
| **Verdict** | **CHOSEN** | — |

Temperature: `0.1` — treats the model as a rule-follower, not a creative writer.

---

## 🛡️ Safety Rules (Non-negotiable)

- The bot **never** invents prices.
- The bot **only** quotes from `docs/product_data.md`.
- If the customer asks anything outside the script → **Human Handoff** is triggered.
- All handoffs are logged to `backend/handoff_log/`.

---

## 📌 What The Agent Will Do Next (Phase 1 Code)

The next agent session will write these Python files in `backend/app/`:

1. `config.py` — environment variable loader
2. `session_store.py` — in-memory session management
3. `telegram_client.py` — Telegram Bot API wrapper
4. `prompts/system_prompt.md` — LLM system instruction
5. `llm_client.py` — Gemini 1.5 Flash integration
6. `state_machine.py` — conversation FSM brain
7. `handoff_logger.py` — handoff event logger
8. `webhook.py` — Telegram webhook endpoint
9. `main.py` — FastAPI server entry point

Full task list: [`.specs/01_foundation/tasks.md`](.specs/01_foundation/tasks.md)

---

## 📞 Human Handoff

When the bot triggers a handoff, it will:
1. Send the customer a polite hold message.
2. Log the conversation to `backend/handoff_log/` as a JSON file.
3. Stop AI auto-reply for this `chat_id` until manually reset.
4. *(Phase 2)* Notify staff via a Telegram group ping.
