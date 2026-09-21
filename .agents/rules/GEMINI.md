# Agent Rules — DA AUTOLIGHT AI Bot

These rules apply to every AI agent session working on this project.
Follow them strictly. No exceptions.

This project has TWO human developers working on DIFFERENT machines: **Calvin** and **Audya**.
Whichever one of them you are talking to, and whichever AI agent/IDE you are, these rules are
identical and mandatory. Do not skip steps because "the other developer's agent probably already
did it" — always verify yourself, in your own session.

---

## 0. SESSION START PROTOCOL (do this FIRST, every single session, no exceptions)

Run these steps IN ORDER before doing anything else the human asked for:

1. **Identify the developer.** If the human's prompt does not state their name (Calvin or
   Audya), ASK before doing any file-modifying work.
2. **Check git state.** Run `git status` and `git fetch origin` (or `git pull` if safe — see
   Rule 8.2). If there are unpulled remote changes, PULL THEM NOW, before reading any project
   files, so you are not working from a stale copy. If pulling would conflict with uncommitted
   local changes, STOP and tell the human — do not force it.
3. **Read `CHANGELOG.md`** — specifically the top-most (highest `Session N`) entries and the
   "What The Agent Will Do Next" section at the bottom. This tells you exactly what the previous
   session (by either developer) did and what is supposed to happen next.
4. **Read `README.md`** — specifically the "What Needs To Be Done RIGHT NOW" checklist and
   "Tahap Kita Saat Ini" section. This tells you the human setup status and current project stage.
5. **Cross-check task status** in `.specs/01_foundation/tasks.md` against what CHANGELOG.md
   claims. If they disagree (e.g. CHANGELOG says a task is done but the checkbox is unchecked,
   or vice versa), flag this to the human — do not silently pick one as truth.
6. **Verify the CURRENT developer's own machine setup** (Rule 3.1) by asking them directly if
   it has not been confirmed in this session or a previous one under their name. Never assume
   Steps 1-5 are done for a developer just because their code changes are in the repo — writing
   code and having a working local Python/venv/`.env` are NOT the same thing.
7. Only after steps 1-6 are done, proceed with whatever the human actually asked for this session.

If any step above reveals a contradiction, inconsistency, or something that looks broken
(duplicate session numbers, a checklist that doesn't match reality, etc.), tell the human
BEFORE proceeding, and propose a fix.

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

### 7.2b Shared credentials vs. per-machine setup — do not confuse these

Not everything in "Steps 1-5" is per-developer. Split them correctly:

- **Shared, done ONCE for the whole team:** Telegram Bot Token, Gemini API Key, Supabase
  URL/key, and the resulting filled-in `.env` file. These belong to the bot/business, not to an
  individual developer. If a second developer creates their OWN Telegram token or Gemini key,
  that creates a SEPARATE bot / project — testing between developers would no longer be
  consistent. The correct flow: one developer obtains these once, then hands the actual `.env`
  file to the other developer OUT OF BAND (e.g. private chat, encrypted transfer) — never via
  git, since `.env` holds secrets and is gitignored by design.
- **Per-machine, done by EACH developer separately:** Python 3.11+ installation and creating
  their own local `.venv` + `pip install -r requirements.txt`. These cannot be shared because
  they depend on each person's own operating system and file paths.
- If a human asks you to help a new developer get set up, tell them clearly which category each
  step falls into — do not tell a new developer to go make their own Telegram bot or Gemini key
  unless the team has explicitly decided to run separate bots for parallel testing.

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
- When resolving a conflict that mixes two entries together (e.g. one entry's bullet points
  bleeding into another's), re-separate them cleanly with correct headings — do not leave merged
  content ambiguous about which developer/session it belongs to.
- After resolving ANY merge conflict in `CHANGELOG.md`, re-check session numbers for duplicates
  across the WHOLE file (not just the conflicted section) and renumber if needed, per Rule #6.

---

## 8. Git workflow: always push directly to `origin master`

- This project does NOT use feature branches. Both Calvin and Audya commit and push directly
  to `master`. Do not create a new branch unless the human explicitly asks for one.
- Before pushing: `git pull` (or `git fetch` + merge/rebase) first, to catch any changes the
  other developer already pushed. Resolve conflicts per Rule 7.4 if they occur.
- Stage only the files relevant to the current session's changes (`git add <specific files>`),
  never blanket `git add .` unless you have reviewed `git status` and confirmed every changed
  file belongs in this commit.
- Only commit/push when the human explicitly asks you to (e.g. "add commit push", "push ke
  master"). Do not push automatically at the end of every session.
- Use a short, descriptive commit message summarizing the session's actual changes.
- After pushing, you do not need to open a pull request — direct push to `master` is the agreed
  workflow for this project.

---

## 9. Verifying Steps 1-5 (per-developer setup) — be strict about this

This has caused real confusion before (a developer's setup status was assumed instead of
confirmed). Follow this strictly:

- You may ONLY mark a Step 1-5 checkbox as "✅ Done" for a developer if THAT developer said so
  themselves in a prompt during a session with you or was directly verified by you running a
  command in a live terminal session with them (e.g. you personally ran `python --version` and
  saw the result on their machine, in their session).
- Having written or committed Python code is NOT proof that Steps 1-5 are done — a developer
  could have written code without ever running it locally, or someone else could have written
  it for them.
- If a developer's status is unconfirmed, the checklist MUST show "⬜ Not done yet" or
  "❓ Not verified", never "✅ Done", no matter how much other evidence suggests it's probably fine.
- If you are Audya's agent and you see Calvin's column already marked ✅, or vice versa — trust
  that mark (a prior agent already confirmed it directly with that person), but never mark or
  edit the OTHER developer's column yourself. Only ever edit the column for the developer you
  are currently talking to.

---
