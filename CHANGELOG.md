# 📋 CHANGELOG — DA AUTOLIGHT AI Bot

> **For the AI Agent:** Update this file at the END of every session where code or docs were changed.
> Format strictly as shown below. Be concise. Every entry must have Date, What Changed, and Next Steps.
>
> **Multiple developers work on this project (Calvin, Audya) on different machines.**
> Every entry MUST include `— by <Name>`. Session numbers are global and sequential
> across all developers — do not restart numbering per person. Always `git pull` before
> starting work and before writing a new entry, to avoid basing your entry on a stale file.

---

## Session Log

> Entries are NOT always in strict top-to-bottom chronological order (some were merged from a
> parallel branch). Always check the `Session N` number and the date to determine actual order,
> not vertical position. Session 1-3 predate the multi-developer naming convention (Rule #7 in
> `.agents/rules/GEMINI.md`) and do not have a `— by <Name>` tag. From Session 4 onward, every
> entry includes it.

---

### 2026-09-21 — Session 6 (Venv Fix — Python 3.7 → 3.12) — by Calvin

**What was done:**
- Diagnosed `pip install -r requirements.txt` failure: the existing `backend/.venv` was created with Python 3.7.6 (from `C:\Users\ASUS\AppData\Local\Programs\Python\Python37`), which is too old for `fastapi==0.111.0` and other pinned Phase 1 dependencies.
- Found Python 3.12.4 already installed on the machine (`C:\Users\ASUS\AppData\Local\Programs\Python\Python312`).
- Deleted the broken `backend/.venv` and recreated it using `py -3.12 -m venv .venv`.
- Installed all `requirements.txt` dependencies successfully into the new venv (verified: `fastapi-0.111.0`, `uvicorn-0.29.0`, `google-generativeai-0.7.0`, `pydantic-2.7.0`, etc. all installed without version conflicts).
- Added multi-developer workflow rules (Rule #7 in `.agents/rules/GEMINI.md`): developer name tagging in CHANGELOG entries, `git pull` before starting work, per-machine setup expectations, merge conflict handling for `CHANGELOG.md`/`README.md`.
- Converted README Steps 1-5 into a per-developer checklist table (Calvin vs. Audya columns), since these are machine-local setup steps. Added GEMINI.md rule 3.1 governing how/when to update this table and when to remove it (only once ALL developers are done).
- Rewrote the README "Next Prompt" section into one consistent daily template usable by either developer at any project stage.

**Files Created/Modified:**
- `backend/.venv/` <- RECREATED (deleted old Python 3.7 venv, created new Python 3.12 venv)
- `.agents/rules/GEMINI.md` <- MODIFIED (added Rule #7 multi-developer workflow, Rule #3.1 per-developer checklist handling)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (added Team Developer section, converted Steps 1-5 to per-developer checklist table, rewrote Next Prompt as a reusable daily template)

**README Human Steps Status:**
- STEP 1-5 for Calvin — ❓ Not verified in THIS session (was seen working in a prior session, but
  per Rule #9 that is not sufficient — Calvin has not been asked to reconfirm in this session).
- STEP 1-5 for Audya — ⬜ Not done yet / not reported by Audya.
- STEP 6 (Install ngrok) — Not done yet (not verified — human should confirm)

**Note on session numbering:** This entry was renumbered from "Session 4" to "Session 6" after a
`git pull` revealed Audya had already pushed two sessions (renumbered below to Session 4 and 5)
under duplicate numbers ("Session 1" and "Session 2", clashing with the original Sept 16 entries).
Global sequential numbering (Rule #6/#7, GEMINI.md) was not yet known to whichever agent Audya
used at the time. Going forward, always check the highest existing Session N — from ANY developer
— before assigning a new number.

**Follow-up fix (same session, after human feedback):** Tightened `.agents/rules/GEMINI.md` with
a new Rule #0 (mandatory Session Start Protocol), Rule #8 (git workflow — always push directly to
`origin master`, no feature branches), and Rule #9 (strict verification requirements for Steps
1-5 — code existing in the repo is NOT proof of a working local setup). Updated README checklist
to mark Calvin's Steps 1-5 as "❓ Not verified" instead of "✅ Done", since it was not reconfirmed
in this session. This is intentional — the human explicitly said they are not yet sure and to
leave it as unverified rather than assume.

---

### 2026-09-19 — Session 4 (Setup Supabase ENV) — by Audya

**What was done:**
- Updated `backend/.env.example` and `.env.example` to include Supabase credentials template
- Created `.env` files in root and `backend/` from the template

**Files Created/Modified:**
- `backend/.env.example` <- MODIFIED (Uncommented Supabase section)
- `.env.example` <- MODIFIED (Updated template)
- `.env` <- NEW (Root environment variables)
- `backend/.env` <- NEW (Backend environment variables)
- `CHANGELOG.md` <- MODIFIED (this entry)

**README Human Steps Status:**
- STEP 1 (Python) — Not verified yet
- STEP 2 (Telegram BotFather token) — Not done yet
- STEP 3 (Gemini API Key) — Not done yet
- STEP 4 (Create `.env`) — Done (Template created, needs filling)
- STEP 5 (Python venv + pip install) — Not done yet
- STEP 6 (Install ngrok) — Not done yet

---

### 2026-09-19 — Session 5 (Full Backend Code Implementation) — by Audya

**What was done:**
- Wrote ALL Phase 1 backend Python modules (TASK-001 through TASK-013)
- Added Supabase as active dependency in `requirements.txt`
- Created config loader, Supabase client, session store (Supabase-backed)
- Created Telegram client, LLM client (Gemini), handoff logger
- Created state machine (FSM brain), webhook route, FastAPI main entry point
- Created system prompt with FSM rules, guardrails, and JSON schema
- Created product data file (source of truth for prices)
- Updated `.specs/01_foundation/tasks.md` to mark TASK-001–013 as done

**Files Created/Modified:**
- `backend/requirements.txt` <- MODIFIED (added supabase==2.5.0)
- `backend/app/__init__.py` <- NEW
- `backend/app/config.py` <- NEW (env var loader)
- `backend/app/supabase_client.py` <- NEW (Supabase connection)
- `backend/app/session_store.py` <- NEW (session CRUD via Supabase)
- `backend/app/telegram_client.py` <- NEW (Telegram API wrapper)
- `backend/app/llm_client.py` <- NEW (Gemini API wrapper)
- `backend/app/handoff_logger.py` <- NEW (handoff log writer)
- `backend/app/state_machine.py` <- NEW (FSM brain)
- `backend/app/webhook.py` <- NEW (POST /webhook route)
- `backend/app/main.py` <- NEW (FastAPI entry point)
- `backend/app/prompts/system_prompt.md` <- NEW (LLM instruction)
- `backend/app/data/product_data.md` <- NEW (price list)
- `.specs/01_foundation/tasks.md` <- MODIFIED (TASK-001–013 checked)
- `CHANGELOG.md` <- MODIFIED (this entry)

**README Human Steps Status:**
- STEP 1 (Python) — Not verified yet
- STEP 2 (Telegram BotFather token) — Not done yet
- STEP 3 (Gemini API Key) — Not done yet
- STEP 4 (Create `.env`) — Done (Template created, needs filling with real values)
- STEP 5 (Python venv + pip install) — Not done yet
- STEP 6 (Install ngrok) — Not done yet

---

### 2026-09-18 — Session 3 (Doc Consolidation)

**What was done:**
- Consolidated multiple fragmented specification and documentation files (`design.md`, `requirements.md`, `bot_flow.md`, `product_data.md`, `tech_stack.md`) into a single master context file (`docs/PROJECT_CONTEXT.md`)
- Deleted all redundant files to save AI token usage for future sessions
- Updated `tasks.md` to point to the new unified context file
- Updated `README.md` to guide the vibecoder on the exact next prompt and current status

**Files Created/Modified:**
- `docs/PROJECT_CONTEXT.md` <- NEW (Consolidated Master Spec)
- `.specs/01_foundation/design.md` <- DELETED (Merged)
- `.specs/01_foundation/requirements.md` <- DELETED (Merged)
- `docs/bot_flow.md` <- DELETED (Merged)
- `docs/product_data.md` <- DELETED (Merged)
- `docs/tech_stack.md` <- DELETED (Merged)
- `Depo Audio Data.md` <- DELETED (Redundant duplicate)
- `.specs/01_foundation/tasks.md` <- MODIFIED (updated references)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (updated Next Prompt section)

**README Human Steps Status:**
- STEP 1 (Python) — Not verified yet
- STEP 2 (Telegram BotFather token) — Not done yet
- STEP 3 (Gemini API Key) — Not done yet
- STEP 4 (Create `.env`) — Not done yet
- STEP 5 (Python venv + pip install) — Not done yet
- STEP 6 (Install ngrok) — Not done yet

---

### 2026-09-16 — Session 1 (Foundation Docs)

**What was done:**
- Generated all foundation `.md` files: `README.md`, `.env.example`, `docs/`, `.specs/`
- Set up project concept, bot flow, tech stack, and product data documentation

**Files Created/Modified:**
- `README.md` <- main beginner guide
- `.env.example`
- `docs/bot_flow.md`, `docs/product_data.md`, `docs/tech_stack.md`
- `.specs/01_foundation/requirements.md`, `design.md`, `tasks.md`

**README Human Steps Status:**
- STEP 1 (Python) — Not verified yet by human
- STEP 2 (Telegram BotFather token) — Not done yet
- STEP 3 (Gemini API Key) — Not done yet
- STEP 4 (Create `.env`) — Not done yet
- STEP 5 (Python venv + pip install) — Not done yet
- STEP 6 (Install ngrok) — Not done yet

**No Python code written yet.**

---

### 2026-09-16 — Session 2 (Monorepo Restructure)

**What was done:**
- Restructured project to monorepo format
- Created `backend/`, `frontend/`, `database/` folder skeleton
- Added WhatsApp RAG Phase 2 rules to `tech_stack.md`
- Updated `design.md` to reflect new monorepo paths
- Added `CHANGELOG.md` (this file) and `.agents/rules/GEMINI.md`

**Files Created/Modified:**
- `backend/` skeleton (`.env.example`, `.gitignore`, `requirements.txt`, `app/`)
- `frontend/` skeleton
- `database/` skeleton
- `docs/tech_stack.md` <- updated
- `.specs/01_foundation/design.md` <- updated paths
- `CHANGELOG.md` <- NEW (this file)
- `.agents/rules/GEMINI.md` <- NEW (agent rules)

**README Human Steps Status:**
- STEP 1 (Python) — Not verified yet by human
- STEP 2 (Telegram BotFather token) — Not done yet
- STEP 3 (Gemini API Key) — Not done yet
- STEP 4 (Create `.env`) — Not done yet
- STEP 5 (Python venv + pip install) — Not done yet
- STEP 6 (Install ngrok) — Not done yet

**No Python code written yet.**

---

## What The Agent Will Do Next

> *(Updated each session — the agent current game plan)*

**All Phase 1 Python code has been written (TASK-001 through TASK-013). ✅**

**PREREQUISITE (Human must do BEFORE testing):**
1. Create a Supabase project and create the `sessions` table (SQL provided in `session_store.py`)
2. Fill in `.env` with real credentials (Telegram token, Gemini API key, Supabase URL + key)
3. Set up Python virtual environment and run `pip install -r requirements.txt`
4. Install and start ngrok

**Next session goal:** Local testing (TASK-014 through TASK-019)
1. Install dependencies (`pip install -r requirements.txt`)
2. Start server (`uvicorn app.main:app --reload --port 8000`)
3. Verify `/health` endpoint
4. Register Telegram webhook via ngrok
5. End-to-end Telegram test

Full task checklist: `.specs/01_foundation/tasks.md`

---
