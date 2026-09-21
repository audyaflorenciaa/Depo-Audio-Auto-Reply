# Agent Rules — DA AUTOLIGHT AI Bot

These rules apply to every AI agent session working on this project.
Follow them strictly. No exceptions.

---

## 1. ALWAYS update CHANGELOG.md after any code or doc changes

At the end of every session where you created, modified, or deleted files:

1. Open `CHANGELOG.md`
2. Add a new entry at the top of the Session Log with this exact format:

```
### YYYY-MM-DD — Session N (Short Description) — by <Developer Name>

**What was done:**
- bullet list of what you did

**Files Created/Modified:**
- `path/to/file` <- reason

**README Human Steps Status:**
- STEP 1 (Python) — [Done / Not done yet / Not verified]
- STEP 2 (Telegram token) — [Done / Not done yet / Not verified]
- STEP 3 (Gemini API Key) — [Done / Not done yet / Not verified]
- STEP 4 (.env file) — [Done / Not done yet / Not verified]
- STEP 5 (venv + pip install) — [Done / Not done yet / Not verified]
- STEP 6 (ngrok) — [Done / Not done yet / Not verified]
```

The `<Developer Name>` MUST be the name the human tells you in their prompt for this session
(e.g. "Calvin" or "Audya"). If the human does not state their name in the prompt, ASK before
writing the entry — do not guess or leave it blank. This is required because this project has
multiple developers working on different machines, sometimes in parallel.

3. Update the "What The Agent Will Do Next" section at the bottom to reflect the CURRENT next steps.

If you did NOT change any files, do NOT add an entry. Zero-touch sessions do not get logged.

**Session numbering with multiple developers:** Session numbers are GLOBAL and sequential across
ALL developers, not per-person. Look at the highest Session N currently in the log (regardless of
who wrote it) and increment by 1. Do not restart numbering per developer.

---

## 2. Cross-check your plan against README.md human steps

Before writing any Python code or running any commands:

1. Read `README.md` sections: "What Needs To Be Done RIGHT NOW"
2. Check if the human has completed the prerequisite steps (Python, .env, ngrok etc.)
3. If the human has NOT completed the steps, DO NOT write code. Instead:
   - Tell the human which README step they need to complete first
   - Update `CHANGELOG.md` with current session note
   - Stop

If the human's steps are complete, proceed with coding.

---

## 3. Update README.md ONLY when human steps change

The README.md "What Needs To Be Done RIGHT NOW" section describes steps for the human developer.
- If you complete a coding phase and the human's NEXT action changes, update that section.
- If nothing about the human's action changes, DO NOT touch README.md.
- Never rewrite the tone or style of README.md — keep it plain English, beginner-friendly.

### 3.1 Per-developer setup checklist (Steps 1-5)

Steps 1-5 in README.md are tracked in a table with one column per developer (Calvin, Audya)
because each step is done locally on each person's own machine (Python install, `.env`, `.venv`).

- Only flip a person's checkbox from `⬜ Not done yet` to `✅ Done` when THAT SPECIFIC PERSON
  tells you in their prompt that they finished it. Never mark a step done for a person who
  didn't report it, even if the other person's machine already works.
- Never mark a step done just because code/files related to it exist — machine-local setup
  (Python, .env, .venv) cannot be verified from git state; you can only trust what each human
  says about their own machine, or what you directly checked via terminal ON A LIVE SESSION with
  that person.
- Once ALL developers have ✅ on ALL of Steps 1-5, collapse/delete the whole checklist table and
  the "Commands for Steps 1-5" section from README.md in your next edit to that file, to avoid
  clutter. Keep Step 6 (ngrok) and Step 7 (WhatsApp export, Phase 2) as they are not yet done.
- If a NEW developer joins the project later, re-add the checklist table with a column for them.

---

## 4. Track task completion in .specs/01_foundation/tasks.md

When you complete a TASK (TASK-001 through TASK-021):
- Change `- [ ]` to `- [x]` for that task.
- Do this immediately after completing each task, not at the end.

---

## 5. Token efficiency rules

To keep AI costs low:
- Read a file only when you need to modify it.
- Do NOT re-read files you already read in the same session unless you need to confirm a change.
- Do NOT rewrite entire files when you only need to update a section.
- Do NOT generate code that is not in the current task list.
- Ask the human to clarify before doing exploratory work that touches many files.

---

## 6. What counts as a "session"

A session = one continuous conversation with the AI agent.
Each new chat window = new session.
Number sessions sequentially GLOBALLY (see Rule #1) across all developers and all days.
If two sessions happen on the same date, they both get logged separately.

---

## 7. Multiple developers, multiple machines (Calvin & Audya)

This project is worked on by more than one human developer, on different machines, sometimes
at overlapping times (parallel work), sometimes taking turns. Follow these rules to avoid
losing track of context or causing git conflicts:

### 7.1 Always identify the developer

- Every human prompt that starts or continues a work session SHOULD state the developer's name
  (e.g. "Ini Calvin, lanjutkan..." or "Audya di sini, saya mau...").
- If the name is missing and this is the first message of a session, ASK for it before doing
  any file-modifying work. Read-only questions (explaining code, answering "what does X do")
  do not require asking.
- Use the stated name in the CHANGELOG entry (Rule #1) and nowhere else — do not add name tags
  to code comments or other files.

### 7.2 Before starting any work: pull first

- At the start of every session, if the workspace is a git repo, check `git status` and
  recommend (or run, if asked) `git pull` BEFORE making any file changes. This prevents working
  on a stale copy of `CHANGELOG.md`, `README.md`, or code that the other developer already changed.
- If `git pull` reports local uncommitted changes that would conflict, stop and tell the human
  instead of forcing the pull.

### 7.3 Machine differences are expected and fine

- Each developer's machine may have a different Python installation path, OS, or even a
  different Python 3.11+ minor version. This is normal. Never assume the other developer's
  environment matches yours.
- `.venv/` is NEVER committed and must be created independently on each machine
  (see README setup steps). `.env` is NEVER committed either — each developer fills in their
  own copy, and both may hold different real secrets (e.g. different Telegram test bots)
  during development.
- If you (the agent) change `requirements.txt`, call this out clearly in the CHANGELOG so the
  other developer knows they need to re-run `pip install -r requirements.txt` on their machine.

### 7.4 Merge conflict risk in CHANGELOG.md / README.md

- Because entries are inserted at the top of `CHANGELOG.md`, two developers working in parallel
  on different branches/machines can create a git merge conflict here. This is expected — resolve
  by keeping BOTH entries (one per developer/session), ordered by timestamp, never delete the
  other developer's entry to resolve a conflict.
- Same rule applies to the README "Changelog (Agent Sessions)" table and "Tahap Kita Saat Ini" section.

---
