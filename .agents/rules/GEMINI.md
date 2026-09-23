# Agent Rules — DA AUTOLIGHT AI Bot

These rules apply to every AI agent session working on this project.
Follow them strictly. No exceptions.

This project has TWO human developers working on DIFFERENT machines: **Calvin** and **Audya**.
Whichever one of them you are talking to, and whichever AI agent/IDE you are, these rules are
identical and mandatory. Do not skip steps because "the other developer's agent probably already
did it" — always verify yourself, in your own session.

---

## 0. SESSION START PROTOCOL (do this FIRST, every single session, no exceptions)

> This protocol is written generically on purpose — it never names a specific step number,
> task number, or file path that will go stale. It describes HOW to read the project's tracking
> files, not what they currently contain. This protocol does not change between project phases.

Run these steps IN ORDER before doing anything else the human asked for:

1. **Identify the developer.** If the human's prompt does not state their name (Calvin or
   Audya), ASK before doing any file-modifying work.
2. **Check git state.** Run `git status` and `git fetch origin` (or `git pull` if safe — see
   Rule 8). If there are unpulled remote changes, PULL THEM NOW, before reading any project
   files, so you are not working from a stale copy. If pulling would conflict with uncommitted
   local changes, STOP and tell the human — do not force it.
3. **Read `CHANGELOG.md`** — find the entry with the HIGHEST `Session N` number (not necessarily
   the topmost entry — order is not always strictly chronological, see the file's own header
   note) and read the "What The Agent Will Do Next" section at the bottom. This tells you exactly
   what the previous session (by either developer) did and what is supposed to happen next.
4. **Read `README.md`** — read the ENTIRE "What Needs To Be Done RIGHT NOW" section as it
   currently exists (its structure may change between phases — sometimes a checklist table,
   sometimes plain steps, sometimes nothing if all setup is done) and the "Tahap Kita Saat Ini"
   section. This tells you the human setup status and current project stage, whatever form it's
   currently in.
5. **Cross-check task status**: find the CURRENT active spec/task file (check the `.specs/`
   folder for the most recent phase folder — it may no longer be `01_foundation` once that phase
   is complete) and compare its checkboxes against what CHANGELOG.md claims. If they disagree,
   flag this to the human — do not silently pick one as truth.
6. **Verify the CURRENT developer's own machine/setup status** by asking them directly if it has
   not been confirmed in THIS session. Never assume any setup step is done for a developer just
   because their code changes are in the repo — writing code and having a working local
   environment are NOT the same thing. (See Rule 9 for strict verification rules.)
7. Only after steps 1-6 are done, proceed with whatever the human actually asked for this session.

If any step above reveals a contradiction, inconsistency, or something that looks broken
(duplicate session numbers, a checklist that doesn't match reality, etc.), tell the human
BEFORE proceeding, and propose a fix.

### 0.1 End-of-session checklist (do this before finishing, if you changed any files)

1. Update `CHANGELOG.md` per Rule #1 (new entry, correct global session number, developer name).
2. Update `README.md` ONLY if the human-facing setup status or current project stage actually
   changed (Rule #3) — never touch it otherwise.
3. Update checkboxes in whichever spec/task file is currently active (Rule #4).
4. If the human asked you to commit/push, follow Rule #8 exactly (stage specific files, pull
   first, push directly to `origin master`).

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
- List whatever per-machine setup steps are CURRENTLY relevant in README.md's "What Needs To Be
  Done RIGHT NOW" section (the exact steps change over time — do not copy an old list, look at
  what's actually there right now), one line per step per developer, each as
  [Done / Not done yet / Not verified].
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

Before writing any code or running any commands that need a working local environment:

1. Read whatever "What Needs To Be Done RIGHT NOW" (or equivalent) section currently exists in
   `README.md`.
2. Check if the CURRENT developer (the one you're talking to) has completed the prerequisites
   listed there for their own machine.
3. If they have NOT completed the steps, DO NOT write/run code that depends on them. Instead:
   - Tell the human which step they need to complete first
   - Update `CHANGELOG.md` with current session note
   - Stop

If the human's steps are complete (confirmed by them, per Rule #9), proceed.

---

## 3. Update README.md ONLY when human steps change

The README.md "What Needs To Be Done RIGHT NOW" section describes steps for the human developer.
- If you complete a coding phase and the human's NEXT action changes, update that section.
- If nothing about the human's action changes, DO NOT touch README.md.
- Never rewrite the tone or style of README.md — keep it plain English, beginner-friendly.

### 3.1 Per-developer setup checklists (any phase, any steps)

Whenever README.md has a setup checklist that is genuinely per-machine (see Rule 7.2b for what
qualifies), track it with one column per developer (Calvin, Audya) — regardless of what the
steps are called or numbered in that phase of the project.

- Only flip a person's checkbox from `⬜ Not done yet` to `✅ Done` when THAT SPECIFIC PERSON
  tells you in their prompt that they finished it. Never mark a step done for a person who
  didn't report it, even if the other person's machine already works.
- Never mark a step done just because code/files related to it exist — machine-local setup
  cannot be verified from git state; you can only trust what each human says about their own
  machine, or what you directly checked via terminal ON A LIVE SESSION with that person.
- Once ALL developers have ✅ on ALL steps in a given checklist, collapse/delete that whole
  checklist section from README.md in your next edit to that file, to avoid clutter — but only
  after logging it as done in `CHANGELOG.md` first, so the history isn't lost.
- If a NEW developer joins the project later, re-add a checklist table with a column for them,
  for whatever setup is still relevant at that time.
- This rule applies to ANY future setup checklist the project ever needs (e.g. a new API key,
  a new local dependency, a new tool) — not just the original Phase 1 setup.

---

## 4. Track task completion in the active spec/task file

Whichever task checklist file is currently active (e.g. `.specs/01_foundation/tasks.md`, or a
later phase's equivalent file once that exists):
- Change `- [ ]` to `- [x]` for each task as soon as it's completed.
- Do this immediately after completing each task, not at the end of the session.
- If a new phase folder is created under `.specs/`, this rule applies to that file too — it is
  not tied to the name "01_foundation" specifically.

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

Not every setup item is per-developer. Split them correctly, in ANY phase of the project:

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
- **ngrok is ALSO per-machine** (a special case worth calling out): unlike Telegram/Gemini/
  Supabase, ngrok holds no shared business secret — but it's still not shareable, because it
  tunnels `localhost` on ONE specific machine to the internet. A tunnel started on Calvin's
  laptop is useless for testing a server running on Audya's laptop. Each developer needs their
  OWN ngrok installation AND their own ngrok account/authtoken (free tier accounts typically
  allow only one active tunnel at a time — sharing one account between two people testing
  simultaneously will cause conflicts/disconnects). Do not treat ngrok as a "shared secret" just
  because it involves an account and a token — categorize it as per-machine setup.
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

## 9. Verifying any per-developer setup status — be strict about this

This has caused real confusion before (a developer's setup status was assumed instead of
confirmed). Follow this strictly, for ANY per-machine setup step at ANY point in the project:

- You may ONLY mark a setup checkbox as "✅ Done" for a developer if THAT developer said so
  themselves in a prompt during a session with you, or was directly verified by you running a
  command in a live terminal session with them (e.g. you personally ran `python --version` and
  saw the result on their machine, in their session).
- Having written or committed code related to a setup step is NOT proof that step is done — a
  developer could have written code without ever running it locally, or someone else could have
  written it for them.
- If a developer's status is unconfirmed, the checklist MUST show "⬜ Not done yet" or
  "❓ Not verified", never "✅ Done", no matter how much other evidence suggests it's probably fine.
- If you are Audya's agent and you see Calvin's column already marked ✅, or vice versa — trust
  that mark (a prior agent already confirmed it directly with that person), but never mark or
  edit the OTHER developer's column yourself. Only ever edit the column for the developer you
  are currently talking to.

---
