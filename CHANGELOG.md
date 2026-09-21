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

> Entries before Session 4 predate the multi-developer naming convention (Rule #7 in
> `.agents/rules/GEMINI.md`) and do not have a `— by <Name>` tag. From Session 4 onward,
> every entry includes it.

---

### 2026-09-21 — Session 4 (Venv Fix — Python 3.7 → 3.12) — by Calvin

**What was done:**
- Diagnosed `pip install -r requirements.txt` failure: the existing `backend/.venv` was created with Python 3.7.6 (from `C:\Users\ASUS\AppData\Local\Programs\Python\Python37`), which is too old for `fastapi==0.111.0` and other pinned Phase 1 dependencies.
- Found Python 3.12.4 already installed on the machine (`C:\Users\ASUS\AppData\Local\Programs\Python\Python312`).
- Deleted the broken `backend/.venv` and recreated it using `py -3.12 -m venv .venv`.
- Installed all `requirements.txt` dependencies successfully into the new venv (verified: `fastapi-0.111.0`, `uvicorn-0.29.0`, `google-generativeai-0.7.0`, `pydantic-2.7.0`, etc. all installed without version conflicts).

- Added multi-developer workflow rules (Rule #7 in `.agents/rules/GEMINI.md`): developer name tagging in CHANGELOG entries, `git pull` before starting work, per-machine setup expectations, merge conflict handling for `CHANGELOG.md`/`README.md`.
- Converted README Steps 1-5 into a per-developer checklist table (Calvin vs. Audya columns), since these are machine-local setup steps and Audya has not completed them yet on her machine. Added GEMINI.md rule 3.1 governing how/when to update this table and when to remove it (only once ALL developers are done).
- Rewrote the README "Next Prompt" section into one consistent daily template usable by either developer at any project stage.

**Files Created/Modified:**
- `backend/.venv/` <- RECREATED (deleted old Python 3.7 venv, created new Python 3.12 venv)
- `.agents/rules/GEMINI.md` <- MODIFIED (added Rule #7 multi-developer workflow, Rule #3.1 per-developer checklist handling)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (added Team Developer section, converted Steps 1-5 to per-developer checklist table, rewrote Next Prompt as a reusable daily template)

**README Human Steps Status:**
- STEP 1 (Python) — Done (Python 3.12.4 confirmed working, used for venv)
- STEP 2 (Telegram BotFather token) — Likely done (`TELEGRAM_BOT_TOKEN` in `.env` has a plausible length, value not inspected)
- STEP 3 (Gemini API Key) — Likely done (`GEMINI_API_KEY` in `.env` has a plausible length, value not inspected)
- STEP 4 (Create `.env`) — Done (`backend/.env` exists and is filled in)
- STEP 5 (Python venv + pip install) — Done (venv recreated with Python 3.12, all dependencies installed)
- STEP 6 (Install ngrok) — Not done yet (not verified — human should confirm)

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

**Next session goal:** Write Phase 1 Python code in `backend/app/`

Order of implementation:
1. `backend/app/config.py` — env var loader (TASK-005)
2. `backend/app/session_store.py` — in-memory sessions (TASK-006)
3. `backend/app/telegram_client.py` — Telegram API wrapper (TASK-007)

**PREREQUISITE (Human must do first):**
- STEP 1, 2, 3, 4, 5 appear complete (see status above).
- STEP 6 (ngrok) still needs human confirmation — not required to start writing code, only required before end-to-end webhook testing (TASK-017/018).
- The human should activate the recreated venv in their own terminal: `.\.venv\Scripts\Activate.ps1` (run from `backend/`).

Full task checklist: `.specs/01_foundation/tasks.md`

---
