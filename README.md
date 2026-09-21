# 🚗💡 DA AUTOLIGHT AI — Auto-Reply Chatbot

> **Vibe Coder Guide** — written for a total beginner. No fluff, just the exact steps you need.
>
> **Always kept up to date** by the IDE agent after every code change session.

---

## 👥 Tim Developer (Multi-machine)

Project ini dikerjakan oleh **lebih dari satu orang** (Calvin, Audya), di **laptop/IDE yang berbeda**, kadang gantian kadang paralel. Beberapa aturan wajib supaya tidak saling menimpa pekerjaan:

- **Selalu `git pull` sebelum mulai kerja**, dan sebelum minta agent lanjutkan development. Kalau tidak, Anda mungkin kerja di atas versi file yang sudah usang.
- **`.venv` selalu dibuat sendiri per laptop** (tidak pernah di-commit ke git). Wajar kalau versi Python persisnya beda (3.11/3.12/3.13), yang penting minimal Python 3.11+.
- **`.env` isinya SATU untuk seluruh tim** (Telegram token, Gemini key, Supabase — milik bot/bisnis, bukan per-orang) — di-share antar developer secara offline (bukan lewat git, karena berisi secret), bukan dibuat ulang masing-masing. Lihat detail di bagian "Shared setup" di bawah.
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

| Date       | Session Summary                                                                                                                                                                                                                                                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-09-16 | **Session 1:** Generated all foundation `.md` files (README, .env.example, docs/, .specs/)                                                                                                                                                                                                                                          |
| 2026-09-16 | **Session 2:** Restructured to monorepo. Created `backend/`, `frontend/`, `database/` skeleton. Added WhatsApp RAG Phase 2 rules to `tech_stack.md`. Updated `design.md` to reflect new paths.                                                                                                                              |
| 2026-09-18 | **Session 3:** Consolidated multiple specification and documentation files (`design.md`, `requirements.md`, `bot_flow.md`, `product_data.md`, `tech_stack.md`) into a single master context file (`docs/PROJECT_CONTEXT.md`) to save AI token usage. Removed redundant files.                                             |
| 2026-09-19 | **Session 4 & 5 (Audya):** Filled in `.env.example` with Supabase template, then wrote ALL Phase 1 backend Python code (`config.py`, `session_store.py`, `telegram_client.py`, `llm_client.py`, `handoff_logger.py`, `state_machine.py`, `webhook.py`, `main.py`, system prompt, product data). TASK-001–013 done. |
| 2026-09-21 | **Session 6 (Calvin):** Fixed `pip install` failure — `backend/.venv` was built with Python 3.7 (too old for FastAPI 0.111.0). Recreated venv with Python 3.12. All dependencies installed successfully. Added multi-developer workflow rules.                                                                                   |

---

## ✅ What Needs To Be Done RIGHT NOW (Human Developer Tasks)

> Complete these steps before the next agent session writes any Python code.

### 🔑 Shared setup (Telegram token, Gemini key, `.env`) — DO NOT DUPLICATE

**Telegram Bot Token dan Gemini API Key adalah milik SATU bisnis/bot, bukan per-orang.** Kalau
Audya membuat token/key sendiri, itu jadi bot Telegram / project Gemini yang BERBEDA, dan testing
antara Calvin & Audya jadi tidak sinkron (dua bot berbeda, harga/respons bisa beda konfigurasi).

- Calvin sudah punya Telegram Bot Token, Gemini API Key, dan `.env` terisi.
- Calvin akan mengirim FILE `.env` yang sudah terisi ke Audya secara **offline** (chat pribadi,
  bukan lewat git/commit — karena `.env` berisi secret dan sudah benar di-`.gitignore`).
- **Audya tinggal:** taruh file `.env` yang diterima itu ke `backend/.env` di laptopnya sendiri.
  Tidak perlu buka BotFather atau Google AI Studio sendiri.
- Kalau nanti butuh bot Telegram testing terpisah (misal supaya Calvin & Audya bisa test
  bersamaan tanpa saling ganggu conversation state), baru itu alasan sah untuk buat token kedua
  — tapi itu keputusan yang harus didiskusikan dulu, bukan default.

### 💻 Per-machine setup (WAJIB masing-masing, tidak bisa di-share)

> Ini beda laptop, beda instalasi Python, jadi setiap orang wajib melakukan ini sendiri.
> **Begitu SEMUA kolom di bawah ✅, section checklist ini akan dihapus dari README** oleh agent
> supaya tidak menumpuk — tapi tetap tercatat permanen di `CHANGELOG.md` siapa yang menyelesaikan
> apa dan kapan.

| Step | What to do                                                             | Calvin                                                        | Audya           |
| ---- | ---------------------------------------------------------------------- | ------------------------------------------------------------- | --------------- |
| 1    | Verify Python 3.11+ installed (`py -0p`)                             | ✅ Done (Python 3.12.4, confirmed by Calvin)                  | ⬜ Not done yet |
| 5    | Create venv +`pip install -r requirements.txt` (inside `backend/`) | ✅ Done (venv recreated with Python 3.12, all deps installed) | ⬜ Not done yet |

> **How to update this table:** whoever finishes a step tells the agent in their prompt
> (e.g. "Ini Audya, saya sudah selesai Step 1 dan 5"), and the agent flips `⬜ Not done yet`
> to `✅ Done` for that person's column. Do not mark the other person's column.

#### Commands for Steps 1 & 5 (run these on YOUR OWN machine)

```powershell
# STEP 1 — check Python version (need 3.11+)
py -0p
# If you have multiple versions, use the specific one, e.g.:
py -3.12 --version

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

### 🌐 Additional per-machine setup

#### STEP 6 — Install ngrok (for local testing)

ngrok creates a public HTTPS tunnel to your local machine so Telegram can reach it.

1. Go to: **https://ngrok.com/download**
2. Download for Windows → extract `ngrok.exe` anywhere on your computer.
3. Sign up for a free account at ngrok.com → copy your **authtoken**.
4. Run once to register:

```powershell
ngrok config add-authtoken <your-authtoken>
```

---

#### STEP 7 — (Future) WhatsApp Chat Export for Phase 2

This does NOT need to be done now. When Phase 2 begins, you will need to export past WhatsApp conversations with real DA AUTOLIGHT customers:

1. Open any customer chat in WhatsApp.
2. Tap **⋮ (three dots)** → **More** → **Export Chat** → **Without Media**.
3. Save each `.txt` file into: `backend/data/whatsapp_exports/`
4. Aim for **50–100 real customer interactions** for a strong tone-matching database.

> See `docs/tech_stack.md` → Section 10 for the full RAG rules and strict data boundary.

---

## 🚀 Running the Bot

> Phase 1 Python code is DONE (TASK-001–013). Next step is local testing (TASK-014–019) — see below.
> You still need: (a) Python + venv set up on YOUR machine (Steps 1 & 5), (b) the shared `backend/.env`
> file received from Calvin and placed in your `backend/` folder, (c) a Supabase project with the
> `sessions` table created (Audya added Supabase as the session store — see
> `backend/app/supabase_client.py` and `backend/app/session_store.py` for the required schema).

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

1. **Calvin** kirim file `backend/.env` yang sudah terisi ke Audya secara offline (chat pribadi, bukan git).
2. **Audya** taruh file itu di `backend/.env` di laptopnya, lalu selesaikan Step 1 & 5 (Python + venv) sendiri — lihat checklist di atas.
3. Buat project Supabase + tabel `sessions` (schema ada di `backend/app/session_store.py` dan `backend/app/supabase_client.py`) — ini kebutuhan baru yang tidak ada di rencana awal (awalnya sesi disimpan in-memory, Audya mengubahnya ke Supabase). Tambahkan `SUPABASE_URL` dan key-nya ke `.env` yang di-share.
4. Jalankan server, test lewat ngrok + Telegram end-to-end.

## 💬 Prompt Harian Anda (Pakai Ini Setiap Mulai Sesi Baru — SELAMANYA, Tidak Perlu Diubah)

> **Untuk Calvin ATAU Audya:** Template ini SENGAJA tidak menyebut nomor step/task/session
> tertentu, karena angka-angka itu berubah terus setiap fase project. Template ini menyuruh
> agent membaca file yang benar dan mengikuti prosedur yang benar — apapun isi filenya saat itu.
> Copy-paste persis, isi `[NAMA]`, tambahkan catatan kalau perlu, lalu kirim ke agent.

```text
Ini [Calvin/Audya]. Saya mau lanjutkan development.

Sebelum mengerjakan apapun, ikuti SESSION START PROTOCOL (Rule #0 di .agents/rules/GEMINI.md):

1. GIT: Cek `git status` dan `git fetch origin`. Kalau ada perubahan remote yang belum saya
   pull, tarik dulu (atau beri tahu saya jika ada konflik) — jangan kerja di atas file usang.

2. BACA CHANGELOG.md: baca entry dengan Session N tertinggi (bukan yang paling atas — urutan
   tampilan tidak selalu kronologis), dan baca section "What The Agent Will Do Next" di bagian
   paling bawah file. Itu adalah rencana kerja saat ini.

3. BACA README.md: baca SELURUH isi section "What Needs To Be Done RIGHT NOW" apapun bentuknya
   saat ini (checklist, tabel, paragraf — bisa berubah bentuk antar fase), dan section
   "Tahap Kita Saat Ini". Jangan asumsikan struktur section ini sama seperti sesi sebelumnya.

4. CROSS-CHECK: cocokkan klaim di CHANGELOG.md dengan checkbox aktual di
   `.specs/01_foundation/tasks.md` (atau spec folder fase berikutnya jika `01_foundation` sudah
   selesai semua). Kalau ada yang tidak sinkron, beri tahu saya SEBELUM lanjut — jangan pilih
   salah satu sebagai asumsi benar.

5. VERIFIKASI SAYA SENDIRI: kalau ada checklist/status setup yang menyebut nama saya, tanyakan
   LANGSUNG ke saya apakah itu masih akurat — jangan anggap sudah selesai hanya karena ada kode
   atau file terkait di repo. Saya yang paling tahu status laptop saya sendiri.

6. BARU SETELAH 1-5: lanjutkan sesuai rencana di "What The Agent Will Do Next", ATAU kerjakan
   instruksi tambahan saya di bawah ini kalau ada.

7. DI AKHIR SESI: kalau ada file yang berubah, update CHANGELOG.md (entry baru, nomor Session
   lanjutan dari yang tertinggi, dengan nama saya), update README.md kalau status setup/tahap
   project berubah, dan update checkbox task di file spec yang relevan. Kalau saya minta
   push, jalankan `git add` (file spesifik saja) + `git commit` + `git push origin master`.

[opsional — isi salah satu atau lebih kalau relevan:]
- Step/setup yang baru saya selesaikan: ...
- Ada perubahan permintaan / fitur baru / keputusan baru: ...
- Saya mau fokus ke bagian tertentu dulu: ...
- Push ke master setelah selesai: [ya/tidak]
```

**Kenapa template ini tidak akan pernah usang:** tidak ada satupun baris di atas yang menyebut
"Step 1-5", "TASK-0XX", atau nomor Session tertentu. Semuanya berupa INSTRUKSI CARA MEMBACA file
(CHANGELOG.md, README.md, file spec), bukan isi spesifik dari file itu. Isi file-file itu akan
terus berubah sepanjang project, tapi cara agent membacanya tetap sama. Detail SOP lengkap selalu
ada di `.agents/rules/GEMINI.md` Rule #0 — kalau README ini dan GEMINI.md Rule #0 berbeda, ikuti
GEMINI.md karena itu sumber kebenaran (source of truth) untuk perilaku agent.

> ⚠️ **Untuk Audya:** kalau bot/agent IDE Anda belum pernah baca `.agents/rules/GEMINI.md`, minta dia baca file itu secara eksplisit di awal sesi pertama Anda. File itu berisi SOP wajib (termasuk Session Start Protocol Rule #0) yang harus diikuti supaya CHANGELOG dan README tidak berantakan lagi seperti kemarin.

Full task list: [`.specs/01_foundation/tasks.md`](.specs/01_foundation/tasks.md) *(path ini akan berubah kalau fase berikutnya punya folder spec baru — cek folder `.specs/` untuk yang terbaru)*

---

## 📞 Human Handoff

When the bot triggers a handoff, it will:

1. Send the customer a polite hold message.
2. Log the conversation to `backend/handoff_log/` as a JSON file.
3. Stop AI auto-reply for this `chat_id` until manually reset.
4. *(Phase 2)* Notify staff via a Telegram group ping.
