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

### 2026-09-23 — Session 13 (Full docs update: rate limit + deprecation findings, session wrap-up) — by Calvin

**What was done:**
- Consolidated all findings from Session 12 (see below) into `README.md`, `CHANGELOG.md`, and
  `.specs/01_foundation/tasks.md` so both Calvin and Audya have a single clear record before
  Calvin stops working for this session.
- Verified README's per-machine checklist status is accurate for both developers: Calvin's Steps
  1/5/6 remain ✅ (unchanged this session), Audya's remain ⬜ (still not reported by her). No
  discrepancy found — this was double-checked at the human's explicit request.
- Confirmed with Calvin: next planning direction is to **explore free/cheaper alternative LLM
  providers, specifically Chinese models** (DeepSeek, Qwen, Kimi/Moonshot, GLM/Zhipu were named as
  examples) as a way around Gemini's restrictive 5 req/min free tier. This is NOT decided or
  started — purely a stated future direction, logged in tasks.md "Known Issues" section so it
  isn't lost.

**Files Created/Modified:**
- `.specs/01_foundation/tasks.md` <- MODIFIED (TASK-017/018/019 marked done with detailed caveats;
  added "Known Issues / Blockers Carried Forward" section documenting the rate limit problem,
  Gemini model deprecation pattern, and the alternative-LLM exploration plan)
- `CHANGELOG.md` <- MODIFIED (this entry + Session 12 below)
- `README.md` <- MODIFIED (added a prominent "Known Issues" section, updated AI Engine section to
  reflect Gemini 1.5 Flash is retired, noted future exploration of Chinese model alternatives)

**README Human Steps Status:**
- Shared setup — ✅ Done.
- Per-machine setup (Calvin) — ✅ Done (Python, venv, ngrok all previously verified).
- Per-machine setup (Audya) — ⬜ STILL not done/reported. Re-confirmed accurate this session, not
  just carried over blindly.
- Local server + Supabase — ✅ Done, working.
- ngrok tunnel + webhook registration — ✅ Done, working (but URL is temporary/random, must repeat
  next session).
- **Full end-to-end conversation test — ⚠️ NOT completed** due to the Gemini rate limit issue
  discovered this session. This is the main open item for the next session.

---

### 2026-09-23 — Session 12 (End-to-end test run: found Gemini model deprecation + rate limiting) — by Calvin

**What was done:**
- Ran the full local test stack together for the first time: `uvicorn` + `ngrok http 8000`
  simultaneously, registered the Telegram webhook, and had Calvin send real messages from Telegram.
- First real message (`/start`) triggered `Gemini API call failed: 404 models/gemini-1.5-flash is
  not found`. Diagnosed: **`gemini-1.5-flash`, the exact model this project's spec was designed
  around, is completely retired by Google as of this session's date.** Ran `genai.list_models()`
  against Calvin's API key to see what's actually available — the list has moved on to Gemini
  2.5/3.x generations entirely; nothing in the 1.5 family remains.
- Tried `gemini-2.5-flash` as a same-tier replacement — also failed, with an even more telling
  error: `404 ... no longer available to new users. Please update your code to use
  models/gemini-3.6-flash`. Google's error message directly pointed to the replacement, so used it.
- Set `GEMINI_MODEL=gemini-3.6-flash` in `backend/.env`. Confirmed this model works via a direct
  isolated test call (bypassing the bot) — it returned successfully. Restarted `uvicorn` to pick
  up the new `.env` value (note: `--reload` only watches `.py` files, NOT `.env` — a manual
  restart is required after any `.env` change).
- Retested from Telegram: bot now replies with CORRECT CONTENT (verified: the exact official
  DA AUTOLIGHT greeting text, and the correct follow-up question asking for car brand/year) — so
  the FSM logic, prompt engineering, and Telegram/Supabase integration are all confirmed working.
  However, replies took 60-90+ seconds, triggering Telegram's own webhook read-timeout, which is
  why the human initially saw "terjadi kesalahan sistem" fallback messages, and later saw delayed
  replies arrive out of order.
- Diagnosed the slowness: timed a raw, isolated `generate_content()` call outside the whole bot
  stack — took 26 seconds for a ONE-WORD reply. Tried several other flash-family models to compare
  and one attempt (`gemini-flash-latest`) failed outright with `429 Quota exceeded ... limit: 5
  ... model: gemini-3.8-flash ... retry in 32s`. **Root cause: Calvin's Gemini API key is on the
  free tier, hard-capped at 5 requests/minute per model.** All the back-and-forth model-switching
  during troubleshooting (by both Calvin and the agent) ate into that quota repeatedly, compounding
  the appearance of slowness — but the underlying limit (5/min) would make this unusable for a
  real customer conversation regardless, since a normal chat easily needs more than 5 LLM calls
  within a few minutes.
- Did not complete the full TASK-019 flow (car info → goal → price → handoff) due to the rate
  limit making further testing impractical this session. Stopped testing to avoid burning more
  quota, and to bring the issue back to Calvin for a decision on how to proceed.
- Cleaned up: stopped the `uvicorn` and `ngrok` background processes at the end of the session
  (Calvin explicitly said they were done working for now).

**Files Created/Modified:**
- `backend/.env` <- MODIFIED (`GEMINI_MODEL` changed twice: `gemini-1.5-flash` → `gemini-2.5-flash`
  → `gemini-3.6-flash`, the last one being the one that currently works)
- `CHANGELOG.md` <- MODIFIED (this entry, written together with Session 13 above)

**README Human Steps Status:** (see Session 13 above — combined into one accurate summary)

---

### 2026-09-21 — Session 11 (ngrok authtoken fixed, tunnel verified working) — by Calvin

**What was done:**
- **Security note:** Calvin's first authtoken was pasted into chat, so the agent advised rotating
  it immediately (regenerate in the ngrok dashboard). Calvin did this before providing the new one.
- First attempt to run `ngrok config add-authtoken` failed with `ERROR: unknown version '3'.
  valid versions are: [1 2]` — a leftover/corrupted `ngrok.yml` config file (likely from a prior
  ngrok install attempt) had an incompatible config schema version. Fixed by deleting
  `%LOCALAPPDATA%\ngrok\ngrok.yml` and letting ngrok regenerate it fresh.
- Second authtoken provided by Calvin turned out to be truncated (copy-paste issue, missing the
  tail end of the token) — ngrok rejected it with `ERR_NGROK_105` ("does not look like a proper
  authtoken"). Calvin re-copied the FULL token from the dashboard and it was accepted.
- After the authtoken was accepted, `ngrok http 8000` still failed with `ERR_NGROK_121`: the
  winget-installed ngrok binary (v3.3.1) was too old — Calvin's ngrok account requires agent
  version 3.20.0+. Fixed by running `ngrok update`, which auto-updated the binary to v3.39.11.
- Verified live: `ngrok http 8000` successfully started a tunnel and printed a public HTTPS URL
  (`https://nonrotating-telaesthetic-jayceon.ngrok-free.dev` — NOTE: ngrok free tier URLs are
  RANDOM and change every time the tunnel restarts, unless on a paid plan with a reserved domain).
  Tunnel was stopped immediately after since no server was running on port 8000 yet — this was
  purely a connectivity/auth test, not a real webhook test.
- TASK-017 (start ngrok, get a working tunnel) is now functionally proven to work end-to-end.
  Registering the Telegram webhook (TASK-018) and the full conversation test (TASK-019) are next.

**Files Created/Modified:**
- (local machine only, no repo files changed by the fixes themselves): `%LOCALAPPDATA%\ngrok\ngrok.yml`
  recreated with a valid authtoken.
- `CHANGELOG.md` <- MODIFIED (this entry)

**README Human Steps Status:**
- Step 6 (ngrok) — ✅ Done for Calvin: installed, updated to a compatible version, authtoken
  registered, tunnel verified working live. Not started for Audya.

---

### 2026-09-21 — Session 10 (ngrok installed, clarified per-machine vs shared) — by Calvin

**What was done:**
- Re-confirmed via live terminal check (`Get-Command ngrok`) that ngrok was still NOT installed,
  consistent with Session 9's finding — no contradiction found during Session Start Protocol.
- Installed `ngrok.exe` (v3.3.1) via `winget install ngrok.ngrok`. Verified the binary works by
  running `ngrok version` directly (using its full winget install path, since the current shell's
  PATH hadn't picked up the change yet — winget itself warned this requires a new terminal).
- Clarified and documented an important distinction the human asked about: **ngrok is per-machine
  setup, not shared like Telegram/Gemini/Supabase credentials.** Even though ngrok involves an
  account and an authtoken (which might look "shared-secret-like"), it cannot actually be shared
  usefully between developers — a tunnel only exposes `localhost` on the ONE machine it runs on.
  Recommended each developer create their OWN ngrok account/authtoken (free tier typically allows
  only one active tunnel at a time, so sharing one account risks conflicts if both test at once).
  Added this as an explicit rule in `.agents/rules/GEMINI.md` (Rule 7.2b) so future agent sessions
  (including Audya's) categorize it correctly without re-asking.
- Guided Calvin through the remaining manual steps (browser sign-up for an authtoken) — could not
  be automated. Waiting on Calvin to complete `ngrok config add-authtoken <token>` before TASK-017
  (start the tunnel) can proceed.

**Files Created/Modified:**
- `.agents/rules/GEMINI.md` <- MODIFIED (Rule 7.2b: documented ngrok as per-machine, not shared)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (Step 6 now includes a winget install option, explicit per-machine/
  per-account warning, and added a Step 6 row to the per-developer checklist table)

**README Human Steps Status:**
- Shared setup (Telegram token, Gemini key, Supabase URL/key in `.env`) — ✅ Done.
- Per-machine setup (Python 3.11+, venv) — ✅ Done for Calvin. ⬜ Not done/reported by Audya.
- Supabase `sessions` table — ✅ Done, verified live.
- Step 6 (ngrok) — ⬜ Partially done for Calvin: `ngrok.exe` installed and verified working via
  terminal, but authtoken NOT yet added (requires Calvin's browser sign-up — pending). Not started
  for Audya.

---

### 2026-09-21 — Session 9 (Supabase table created, server verified locally) — by Calvin

**What was done:**
- Ran the SQL Session Start Protocol found: Calvin executed `CREATE TABLE sessions (...)` in the
  Supabase SQL Editor (with RLS off — fine since the backend uses `SUPABASE_SERVICE_KEY`, which
  bypasses RLS regardless). Verified live from the terminal: the table is now reachable via
  `supabase.table('sessions').select('*')`, returns 0 rows (expected, empty table). TASK-013b done.
- Ran `uvicorn app.main:app --reload --port 8000` — server started cleanly, no errors. Startup
  log confirmed Supabase URL, Gemini model, and webhook secret path all loaded correctly from
  `.env`. TASK-014 through TASK-016 confirmed done on Calvin's machine.
- Checked `GET /health` — returned `{"status": "ok", "version": "0.1.0"}` as specified.
- Checked for `ngrok` on Calvin's machine — NOT installed yet (`ngrok` command not found).
  TASK-017/018 (ngrok tunnel + webhook registration) cannot proceed until Calvin installs it
  (README Step 6 — manual step, requires browser sign-up, cannot be automated). Server was
  stopped after the `/health` check to avoid leaving it running unnecessarily.

**Files Created/Modified:**
- `.specs/01_foundation/tasks.md` <- MODIFIED (TASK-013b, TASK-014, TASK-015, TASK-016 marked done)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (updated current stage: Supabase table done, server verified, ngrok is
  now the next blocker)

**README Human Steps Status:**
- Shared setup (Telegram token, Gemini key, Supabase URL/key in `.env`) — ✅ Done.
- Per-machine setup (Python 3.11+, venv) — ✅ Done for Calvin (re-verified this session via a live
  server run). ⬜ Still not done/reported by Audya.
- Supabase `sessions` table — ✅ Done, verified live this session.
- Step 6 (ngrok) — ⬜ NOT installed on Calvin's machine yet — confirmed via `Get-Command ngrok`,
  not an assumption. This is now the blocker for TASK-017/018/019 (webhook registration + full
  end-to-end Telegram test).

---

### 2026-09-21 — Session 8 (Fix venv missing `supabase`, wrong SUPABASE_URL, discovered `sessions` table missing) — by Calvin

**What was done:**
- Verified Calvin's `.env`/venv status directly (per Rule #9): `backend/.venv` exists, Python
  3.12.4 confirmed working. `backend/.env` has TELEGRAM_BOT_TOKEN, GEMINI_API_KEY,
  WEBHOOK_SECRET_PATH, SUPABASE_URL, SUPABASE_SERVICE_KEY all filled with real-looking values.
  `WEBHOOK_BASE_URL` is still a placeholder (expected — it's only known after ngrok starts).
- Found root-level `.env` (not `backend/.env`) still has a placeholder `SUPABASE_SERVICE_KEY` —
  confirmed via reading `backend/app/config.py` that this file is NEVER read by the app (it loads
  `backend/.env` specifically via `Path(__file__).resolve().parent.parent / ".env"`). Root `.env`
  is effectively dead/unused; left as-is, not a blocker.
- Ran `pip install -r requirements.txt` in `backend/.venv` and found the `supabase` package was
  missing (venv was created/installed before Audya added `supabase==2.5.0` to
  `backend/requirements.txt`). Installed successfully.
- Found `SUPABASE_URL` in `backend/.env` had an incorrect trailing `/rest/v1/` path — the
  `supabase-py` client library appends this itself, so having it in the URL caused a double-path
  error (`PGRST125: Invalid path specified`). Fixed by stripping the suffix, leaving just
  `https://stnwwfjlalhurvvqoqwo.supabase.co`.
- After the URL fix, connected successfully to the Supabase project, but discovered the
  `sessions` table does not exist yet (`PGRST205: Could not find the table 'public.sessions'`).
  This answers Calvin's earlier "I don't know" on whether the Supabase table was created — it
  was NOT. The Supabase *project* exists and credentials are valid; only the *table* is missing.
- Discussed with Calvin: the bot currently has NO car-model-to-lamp-size compatibility data
  (e.g. "Toyota Avanza → 3 inch foglamp"). `product_data.md` only has price tables by inch size
  and brand, not by car model. **Calvin decided:** build a real car-model → size compatibility
  database (Option B), not just "always ask the customer" — but as a FUTURE phase, starting with
  a small example dataset (~5-10 models) from staff, not the full catalogue on day one. Logged as
  TASK-022 through TASK-025 in `.specs/01_foundation/tasks.md` under a new "Phase 2 (Future)"
  section. Until that data exists, Phase 1's bot still asks the customer directly and hands off
  if unknown — that behavior is unchanged for now.
- **Calvin decided NOT to run the Supabase `sessions` table SQL today** — deferred to a future
  session. Logged as TASK-013b (blocking task, not done) instead of executing it immediately.

**Files Created/Modified:**
- `backend/.venv/` <- MODIFIED (installed `supabase==2.5.0` and its dependencies, previously missing)
- `backend/.env` <- MODIFIED (fixed `SUPABASE_URL`: removed incorrect `/rest/v1/` suffix)
- `.specs/01_foundation/tasks.md` <- MODIFIED (added TASK-013b for the Supabase table creation;
  added a new "Phase 2 (Future)" section with TASK-022 through TASK-025 for the car compatibility database)
- `CHANGELOG.md` <- MODIFIED (this entry)
- `README.md` <- MODIFIED (documented the Supabase table SQL as a deferred next step, not done today)

**README Human Steps Status:**
- Shared setup (Telegram token, Gemini key, Supabase URL/key in `.env`) — ✅ Done, values present
  in `backend/.env` and verified loadable by `config.py`.
- Per-machine setup (Python 3.11+, venv) — ✅ Confirmed for Calvin this session (venv verified
  live, Python 3.12.4). ⬜ Still not done/reported by Audya.
- Supabase `sessions` table does not exist yet (TASK-013b) — confirmed NOT done, and intentionally
  deferred by Calvin, not an oversight. Local testing (TASK-014+) stays blocked until it's created.

---

### 2026-09-21 — Session 7 (Clarify shared vs per-machine setup) — by Calvin

**What was done:**
- Clarified with the human (Calvin) that Steps 1-5 were incorrectly treated as ALL per-developer.
  In reality: Telegram Bot Token, Gemini API Key, and `.env` values belong to ONE bot/business,
  not one per developer — creating separate tokens would fragment testing into two different
  bots. Only Python installation and venv creation are genuinely per-machine.
- Confirmed Calvin has completed Step 1 (Python 3.11+) and Step 5 (venv + deps) — marked ✅ Done.
- Restructured README.md checklist into two sections: "Shared setup" (Telegram token / Gemini key
  / `.env` — done once by Calvin, then the `.env` file itself is handed to Audya offline/out-of-band,
  never through git) and "Per-machine setup" (Python + venv — genuinely separate per laptop).
- Updated "Tahap Kita Saat Ini" to reflect this: Audya's next actions are (a) receive `.env` from
  Calvin offline, (b) do her own Python/venv setup, (c) add Supabase credentials to the shared `.env`.

**Files Created/Modified:**
- `README.md` <- MODIFIED (split Steps 1-5 into "shared" vs "per-machine" sections, updated checklist and current stage)
- `CHANGELOG.md` <- MODIFIED (this entry)

**README Human Steps Status:**
- Shared (Telegram token, Gemini key, `.env` template) — ✅ Done by Calvin, to be handed to Audya offline.
- Step 1 (Python 3.11+) — ✅ Done for Calvin. ⬜ Not done yet for Audya.
- Step 5 (venv + pip install) — ✅ Done for Calvin. ⬜ Not done yet for Audya.
- Step 6 (ngrok) — Not done yet (either developer).

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
**Calvin's local environment is fully verified end-to-end: venv, `.env`, Supabase, server, ngrok,
Telegram webhook. Bot logic/content confirmed CORRECT (greeting + car question worked). ✅**

**🔴 TOP PRIORITY BLOCKER — must be resolved before any more real testing:**
**Gemini free-tier rate limit (5 requests/minute) makes the bot unusable for real conversations.**
See `.specs/01_foundation/tasks.md` → "Known Issues" section for full details. Next session should
start by deciding one of:
1. Upgrade to a paid Gemini plan, OR
2. **Research and possibly switch to a more generous alternative LLM provider — Calvin specifically
   mentioned wanting to explore Chinese models (DeepSeek, Qwen, Kimi/Moonshot, GLM/Zhipu, etc.) for
   their free tiers.** This has NOT been researched yet — no provider has been chosen, no code
   changes have been made toward this. If pursued, expect to need to rework `llm_client.py`
   (different SDK) and re-verify structured/JSON output support for whichever provider is picked.

**ALSO CARRY FORWARD:**
- `gemini-1.5-flash` (original spec's model) and `gemini-2.5-flash` (first fallback) are BOTH
  fully retired by Google now. Currently using `gemini-3.6-flash` in `backend/.env` as a stopgap —
  if switching LLM providers, this whole question becomes moot anyway.
- TASK-019's full flow (car info → goal → price recommendation → handoff) was NOT completed —
  only greeting + car-brand question were verified. Needs a full re-run once the rate limit issue
  is resolved (whichever way that goes).
- ngrok's free-tier URL is random per restart — re-register the webhook (TASK-018) every session.

**DECIDED — Phase 2 (Future), not started (TASK-022 through TASK-025):**
- Car model → lamp size compatibility database. Start with a small example dataset (~5-10 models)
  from DA AUTOLIGHT staff, not the full catalogue. Until this exists, Phase 1's bot keeps asking
  the customer directly for their lamp size and hands off if they don't know. See
  `.specs/01_foundation/tasks.md` for the full breakdown.

**AUDYA STILL NEEDS TO:**
1. Receive `backend/.env` from Calvin (already sent, per Calvin — Audya should confirm receipt).
   NOTE: the `.env` she receives will need her to ALSO update `GEMINI_MODEL` if the model changes
   again, or if the LLM provider changes entirely.
2. Complete her own Python 3.11+ + venv + ngrok setup (with her OWN ngrok account) on her machine,
   then report back.

**Next session goal:** Resolve the LLM rate-limit/provider question FIRST, then re-run the full
TASK-019 conversation flow test (car info → goal → price → handoff) before considering Phase 1 done.

Full task checklist: `.specs/01_foundation/tasks.md`

---
