# Humanity Loop Prompts

This file is the quick-access prompt index for starting or migrating Humanity Loop chats.

Canonical supporting files:
- Master continuity rules: `CHAT-CONTINUITY.md`
- Hourly worker full operating instructions: `AUTOMATION-PROMPT.md`

## 1. Start a new Humanity Loop master chat

Paste this into a normal new ChatGPT conversation:

> **Resume Humanity Loop as the master command-center. Treat https://github.com/Lesterhau/humanity-loop as canonical. Read CHAT-CONTINUITY.md and PROJECT-STATE.md first, then the mandatory bootstrap files they name. Reconcile active automations, GitHub, Undermind, AgentMail, and live apps before acting. Do not make me restate prior architecture or decisions. Summarize only material blockers/drift, then continue operating from current state.**

Then verify:
- current automation state;
- pending failures;
- live apps;
- current project state;
- MOTHER/AgentMail;
- Undermind;
- latest GitHub ledger state.

## 2. Hourly worker canonical prompt

The hourly worker's full prompt is intentionally **not duplicated here**.

Canonical source:
https://github.com/Lesterhau/humanity-loop/blob/main/AUTOMATION-PROMPT.md

The scheduled task should be instructed to read that file at the start of every run.

This keeps the prompt maintainable in one place instead of allowing multiple copies to drift.

## 3. Migrate the hourly worker to a new chat

Paste this into the new destination chat:

> **Migrate the Humanity Loop hourly worker to this chat. Treat https://github.com/Lesterhau/humanity-loop/blob/main/AUTOMATION-PROMPT.md as canonical. Inspect the existing Humanity Loop hourly automation first. Disable the old worker only when necessary to avoid duplicate hourly runs, then recreate it here at the same hourly cadence. Verify the new worker is active before declaring migration complete. Do not alter unrelated scheduled tasks.**

Migration sequence:
1. inspect current Humanity Loop automation;
2. preserve schedule/title/prompt intent;
3. prevent duplicate workers;
4. create/activate replacement;
5. verify replacement;
6. only then disable/remove obsolete worker if still needed.

## 4. Before archiving an old master chat

1. Ensure important chat-only decisions are committed to GitHub.
2. Refresh `PROJECT-STATE.md` if needed.
3. Start the new master chat with prompt #1 above.
4. Confirm the new chat has reconciled current state.
5. Then archive the old master thread.

Do not rely on chat history as the only durable copy of Humanity Loop's operating instructions.
