# 🚗💡 DA AUTOLIGHT AI — Auto-Reply Chatbot

> **Vibe Coder Guide** — written for a total beginner. No fluff, just the exact steps you need.
>
> **Always kept up to date** by the IDE agent after every code change session.

---

## 👥 Tim Developer (Multi-machine)

Project ini dikerjakan oleh **lebih dari satu orang** (Calvin, Audya), di **laptop/IDE yang berbeda**, kadang gantian kadang paralel. Beberapa aturan wajib supaya tidak saling menimpa pekerjaan:

- **Selalu `git pull` sebelum mulai kerja**, dan sebelum minta agent lanjutkan development. Kalau tidak, Anda mungkin kerja di atas versi file yang sudah usang.
- **Setiap orang punya `.venv` dan `.env` sendiri**, lokal di laptop masing-masing — ini TIDAK pernah di-commit ke git (lihat `.gitignore`). Wajar kalau versi Python persisnya beda (3.11/3.12/3.13), yang penting minimal Python 3.11+.
- **Selalu sebutkan nama Anda di prompt** ("Ini Calvin..." atau "Ini Audya...") supaya agent bisa mencatatnya di `CHANGELOG.md` dengan benar dan kita tidak bingung siapa mengerjakan apa.
- Kalau `CHANGELOG.md` atau `README.md` konflik saat `git pull`/merge (karena dua orang menambah entry di waktu yang berdekatan), **jangan hapus entry orang lain** — gabungkan keduanya, urutkan berdasarkan tanggal/waktu.

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

| Date       | Session Summary                                                                                                                                                                                                                                                                                 |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-09-16 | **Session 1:** Generated all foundation `.md` files (README, .env.example, docs/, .specs/)                                                                                                                                                                                              |
| 2026-09-16 | **Session 2:** Restructured to monorepo. Created `backend/`, `frontend/`, `database/` skeleton. Added WhatsApp RAG Phase 2 rules to `tech_stack.md`. Updated `design.md` to reflect new paths.                                                                                  |
| 2026-09-18 | **Session 3:** Consolidated multiple specification and documentation files (`design.md`, `requirements.md`, `bot_flow.md`, `product_data.md`, `tech_stack.md`) into a single master context file (`docs/PROJECT_CONTEXT.md`) to save AI token usage. Removed redundant files. |
| 2026-09-19 | **Session 4 & 5 (Audya):** Filled in `.env.example` with Supabase template, then wrote ALL Phase 1 backend Python code (`config.py`, `session_store.py`, `telegram_client.py`, `llm_client.py`, `handoff_logger.py`, `state_machine.py`, `webhook.py`, `main.py`, system prompt, product data). TASK-001–013 done. |
| 2026-09-21 | **Session 6 (Calvin):** Fixed `pip install` failure — `backend/.venv` was built with Python 3.7 (too old for FastAPI 0.111.0). Recreated venv with Python 3.12. All dependencies installed successfully. Added multi-developer workflow rules.                                                                                      |

---

## ✅ What Needs To Be Done RIGHT NOW (Human Developer Tasks)

> Complete these steps before the next agent session writes any Python code.
>
> ⚠️ **Steps 1–5 are PER-MACHINE.** Each developer has their own laptop, their own Python
> installation, and their own local `.venv`/`.env` (never committed to git — see `.gitignore`).
> One person finishing these steps does NOT mean the other person is done. Track each person's
> status separately in the checklist below. **Once BOTH Calvin and Audya have checked off all
> of Steps 1–5, this whole section can be deleted from the README** — the agent will do that
> automatically the next time it updates this file, once both columns are ✅.

### Setup Checklist (per developer, per machine)

| Step | What to do | Calvin | Audya |
|---|---|---|---|
| 1 | Verify Python 3.11+ installed (`python --version` or `py -0p` to list versions) | ❓ Not verified (3.12.4 seen once, not reconfirmed by Calvin) | ⬜ Not done yet |
| 2 | Get Telegram Bot Token from @BotFather | ❓ Not verified (plausible value in `.env`, not confirmed by Calvin) | ⬜ Not done yet |
| 3 | Get Gemini API Key from https://aistudio.google.com/ | ❓ Not verified (plausible value in `.env`, not confirmed by Calvin) | ⬜ Not done yet |
| 4 | Create `backend/.env` from `.env.example`, fill in real values | ❓ Not verified (file exists, values not confirmed real) | ⬜ Not done yet |
| 5 | Create venv + install deps (see commands below) | ❓ Not verified (venv was recreated + installed successfully in one session, not reconfirmed since) | ⬜ Not done yet |

> **Calvin dan Audya:** kolom di atas ditandai "Not verified" sampai masing-masing dari Anda
> mengonfirmasi ulang secara eksplisit ke agent di sesi Anda sendiri. Agent tidak akan menandai
> ✅ Done hanya berdasarkan riwayat sesi lama atau karena ada kode di repo.

> **How to update this table:** whoever finishes a step tells the agent in their prompt
> (e.g. "Ini Audya, saya sudah selesai Step 1 dan 2"), and the agent flips `⬜ Not done yet`
> to `✅ Done` for that person's column. Do not mark the other person's column — only the
> agent updates this table, based on what each human reports.

#### Commands for Steps 1–5 (run these on YOUR OWN machine)

```powershell
# STEP 1 — check Python version (need 3.11+)
py -0p
# If you have multiple versions, use the specific one, e.g.:
py -3.12 --version

# STEP 4 — create your .env (inside backend/ folder)
Copy-Item .env.example .env
# then open .env and fill in TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, WEBHOOK_SECRET_PATH
# generate a random secret path with:
python -c "import secrets; print(secrets.token_hex(16))"

# STEP 5 — create venv with Python 3.11+ (inside backend/ folder)
py -3.12 -m venv .venv          # use whichever 3.11+ version YOUR machine has
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> If you get a script execution error on `Activate.ps1`, run this first:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**After setup is done, every new terminal session just needs:**

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

(No need to reinstall — only re-run `pip install -r requirements.txt` if `requirements.txt` changes.)

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

## 🚀 Running the Bot

> Phase 1 Python code is DONE (TASK-001–013). Next step is local testing (TASK-014–019) — see below.
> You still need: (a) Steps 1–5 done on YOUR machine, (b) a Supabase project with the `sessions` table
> created (Audya added Supabase as the session store — see `backend/app/supabase_client.py` and
> `backend/app/session_store.py` for the required schema), (c) real values filled into `backend/.env`.

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

| Criteria               | Gemini 1.5 Flash   | Llama 3 (Groq)     |
| ---------------------- | ------------------ | ------------------ |
| Structured JSON output | Excellent (native) | Good (prompt only) |
| Instruction-following  | Very High          | Medium             |
| Context window         | 1M tokens          | 128K tokens        |
| Future vision support  | Yes                | No                 |
| **Verdict**      | **CHOSEN**   | —                 |

Temperature: `0.1` — treats the model as a rule-follower, not a creative writer.

---

## 🛡️ Safety Rules (Non-negotiable)

- The bot **never** invents prices.
- The bot **only** quotes from `docs/product_data.md`.
- If the customer asks anything outside the script → **Human Handoff** is triggered.
- All handoffs are logged to `backend/handoff_log/`.

---

## 📌 Tahap Kita Saat Ini (Current Stage)

**Tahap 2 sudah selesai:** Audya sudah menulis semua kode Python Phase 1 (TASK-001–013) — `config.py`, `session_store.py` (pakai Supabase, bukan in-memory dict), `telegram_client.py`, `llm_client.py`, `handoff_logger.py`, `state_machine.py`, `webhook.py`, `main.py`, system prompt, dan product data.

**Kita sekarang masuk Tahap 3: Local Testing** (TASK-014–019). Yang perlu dilakukan:
1. **Setiap developer** menyelesaikan Steps 1–5 di laptop masing-masing (lihat checklist di atas). Status Audya di checklist itu masih ditandai "Not done yet" — belum ada konfirmasi eksplisit dari Audya soal ini, meski dia sudah menulis kode. **Perlu dikonfirmasi ulang ke Audya.**
2. Buat project Supabase + tabel `sessions` (schema ada di `backend/app/session_store.py` dan `backend/app/supabase_client.py`) — ini kebutuhan baru yang tidak ada di rencana awal (awalnya sesi disimpan in-memory, Audya mengubahnya ke Supabase).
3. Isi `backend/.env` dengan kredensial asli (Telegram, Gemini, Supabase URL + key).
4. Jalankan server, test lewat ngrok + Telegram end-to-end.

## 💬 Prompt Harian Anda (Pakai Ini Setiap Mulai Sesi Baru)

> **Untuk Calvin ATAU Audya:** Ini adalah template yang SAMA untuk siapapun, kapanpun, di tahap manapun project ini. Copy-paste, isi `[NAMA]`, tambahkan catatan kalau perlu, lalu kirim ke agent.

```text
Ini [Calvin/Audya]. Saya mau lanjutkan development.

Ikuti SESSION START PROTOCOL di .agents/rules/GEMINI.md (Rule #0) sebelum mengerjakan apapun:
1. Cek git status/fetch — kalau ada perubahan yang belum saya pull, beri tahu saya dulu sebelum lanjut.
2. Baca CHANGELOG.md (entry terbaru + bagian "What The Agent Will Do Next").
3. Baca README.md (checklist Steps 1-5, dan "Tahap Kita Saat Ini").
4. Cocokkan status task di .specs/01_foundation/tasks.md — kalau ada yang tidak sinkron dengan CHANGELOG, beri tahu saya.
5. Tanyakan ke saya langsung status Steps 1-5 di kolom nama saya — JANGAN anggap sudah selesai hanya karena ada kode di repo.
6. Setelah semua itu, lanjutkan sesuai rencana "What The Agent Will Do Next", atau ikuti instruksi tambahan saya di bawah.

[opsional — isi salah satu atau lebih kalau relevan:]
- Step setup yang baru saya selesaikan: ...
- Ada perubahan permintaan / fitur baru: ...
- Saya mau fokus ke bagian tertentu dulu: ...
```

**Kenapa template ini selalu sama:** agent akan otomatis cari tahu detail teknis (task mana yang jalan, file mana yang perlu dibaca) dari `CHANGELOG.md` dan `.specs/01_foundation/tasks.md` sendiri. Anda tidak perlu hafal nomor `TASK-XXX` atau nama file spesifikasi setiap hari — cukup pastikan nama Anda dan poin 1-6 di atas selalu diikuti.

> ⚠️ **Untuk Audya:** kalau bot/agent IDE Anda belum pernah baca `.agents/rules/GEMINI.md`, minta dia baca file itu secara eksplisit di awal sesi pertama Anda. File itu berisi SOP wajib (termasuk Session Start Protocol Rule #0) yang harus diikuti supaya CHANGELOG dan README tidak berantakan lagi seperti kemarin.

Full task list: [`.specs/01_foundation/tasks.md`](.specs/01_foundation/tasks.md)

---

## 📞 Human Handoff

When the bot triggers a handoff, it will:

1. Send the customer a polite hold message.
2. Log the conversation to `backend/handoff_log/` as a JSON file.
3. Stop AI auto-reply for this `chat_id` until manually reset.
4. *(Phase 2)* Notify staff via a Telegram group ping.
