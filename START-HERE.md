# Humanity Loop — Start Here

Use this file when opening a new ChatGPT conversation or replacing a full/archived Humanity Loop chat.

## New master chat

Paste this into a fresh normal ChatGPT conversation:

> **Resume Humanity Loop as the master command-center. Treat https://github.com/Lesterhau/humanity-loop as canonical. Read CHAT-CONTINUITY.md and PROJECT-STATE.md first, then the mandatory bootstrap files they name. Reconcile active automations, GitHub, Undermind, AgentMail, and live apps before acting. Do not make me restate prior architecture or decisions. Summarize only material blockers/drift, then continue operating from current state.**

## Replace / migrate the hourly worker chat

Paste this into the replacement chat:

> **Migrate the Humanity Loop hourly worker to this chat. Treat https://github.com/Lesterhau/humanity-loop/blob/main/AUTOMATION-PROMPT.md as canonical. Inspect the existing Humanity Loop hourly automation first. Disable the old worker only when necessary to avoid duplicate hourly runs, then recreate it here at the same hourly cadence. Verify the new worker is active before declaring migration complete. Do not alter unrelated scheduled tasks.**

## Canonical hourly instructions

Full hourly worker operating prompt:

- `AUTOMATION-PROMPT.md`

## Continuity/state files

Read first when restarting:

- `CHAT-CONTINUITY.md`
- `PROJECT-STATE.md`

## Rule of thumb

- Chat = working interface.
- GitHub / Undermind = institutional memory.
- Hourly log = telemetry.
- This repo is the canonical restart point.
