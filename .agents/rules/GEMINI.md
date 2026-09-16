# Agent Rules — DA AUTOLIGHT AI Bot

These rules apply to every AI agent session working on this project.
Follow them strictly. No exceptions.

---

## 1. ALWAYS update CHANGELOG.md after any code or doc changes

At the end of every session where you created, modified, or deleted files:

1. Open `CHANGELOG.md`
2. Add a new entry at the top of the Session Log with this exact format:

```
### YYYY-MM-DD — Session N (Short Description)

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

3. Update the "What The Agent Will Do Next" section at the bottom to reflect the CURRENT next steps.

If you did NOT change any files, do NOT add an entry. Zero-touch sessions do not get logged.

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
Number sessions sequentially per day: Session 1, Session 2, etc.
If two sessions happen on the same date, they both get logged separately.

---
