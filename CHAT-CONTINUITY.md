# Humanity Loop Chat Continuity

This file exists so Humanity Loop can survive a full, corrupted, archived, or replaced ChatGPT conversation without rebuilding the project from memory.

## Canonical truth order

When restarting any Humanity Loop chat, use sources in this order:

1. **GitHub canonical repo** — architecture, governance, live project state, ledgers, failures, prompts.
2. **Undermind workspace** — persistent research programs, deep literature searches, evidence notes.
3. **AgentMail MOTHER inbox** — external correspondence and operational replies.
4. **Current automation state** — active scheduled workers and cadence.
5. **ChatGPT past-chat memory/history** — useful context, but never the sole source of truth.

Chat history is working memory. GitHub/Undermind are institutional memory.

## Branch-chat reconciliation

Branched or parallel Humanity Loop chats are working-memory surfaces, not separate sources of authority. When a branch contains a material decision, completed external action, new permission, new account state, blocker, or verified outcome, promote it into the canonical repo during the same active session when practical. Do not leave important branch-only state waiting for a later manual merge.

When branch state conflicts with GitHub, independently verify the current external state before updating canonical files. A shared-chat link is useful for human review but is not the continuity mechanism.

## Mandatory bootstrap files

A new Humanity Loop master chat should read these first:

- `README.md`
- `PROJECT-STATE.md`
- `PROTOCOL.md`
- `ARCHITECTURE.md`
- `GOVERNANCE.md`
- `OPERATIONS.md`
- `AUTOMATION-PROMPT.md`
- `PENDING-ACTIONS.md`
- `WIN-LEDGER.md`
- `ACTION-LEDGER.md`
- `ROLE-CATALOG.md`
- `FOUNDRY-RUNTIME.md`
- `TOOLING.md`
- `MULTI-MODEL.md`
- `AMPLIFIER-CONNECTOR.md`
- `TRANSITION-BARRIERS.md`
- `SOCIAL-DISTRIBUTION.md`
- `EXECUTION-PRINCIPLES.md`

Then read any domain file relevant to the immediate task.

## Master chat bootstrap prompt

If the current command-center chat becomes full, start a normal new ChatGPT conversation and send only:

> **Resume Humanity Loop as the master command-center. Treat https://github.com/Lesterhau/humanity-loop as canonical. Read CHAT-CONTINUITY.md and PROJECT-STATE.md first, then the mandatory bootstrap files they name. Reconcile active automations, GitHub, Undermind, AgentMail, and live apps before acting. Do not make me restate prior architecture or decisions. Summarize only material blockers/drift, then continue operating from current state.**

That is enough. Do not paste the old conversation.

## Hourly worker continuity

The hourly worker's full operating instructions live in `AUTOMATION-PROMPT.md`, not in its chat history.

Every hourly cycle should:
- read `AUTOMATION-PROMPT.md`;
- read `PROJECT-STATE.md`;
- commit meaningful outcomes/failures to durable state;
- avoid relying on previous chat turns for mission-critical context.

Therefore, if the hourly log chat becomes full, **the work itself should not be lost**.

### Hourly log migration prompt

Start a new normal chat and send:

> **Migrate the Humanity Loop hourly worker to this chat. Treat https://github.com/Lesterhau/humanity-loop/blob/main/AUTOMATION-PROMPT.md as canonical. Inspect the existing Humanity Loop hourly automation first. Disable the old worker only when necessary to avoid duplicate hourly runs, then recreate it here at the same hourly cadence. Verify the new worker is active before declaring migration complete. Do not alter unrelated scheduled tasks.**

The migration must follow:
1. inspect current Humanity Loop automation;
2. preserve its schedule/title/prompt intent;
3. prevent duplicate simultaneous workers;
4. create/activate replacement;
5. verify replacement is active;
6. only then disable/remove obsolete worker if still needed.

## What must be durable before a chat ends

Important chat-only decisions should be promoted into GitHub before they can become critical dependencies.

At minimum, durable state must contain:
- architecture/governance decisions;
- approved user-asset permissions;
- live-app URLs/IDs;
- active automation purpose;
- unresolved blockers;
- external-action failures;
- verified wins;
- current social/MOTHER strategy;
- current model/tool integrations;
- major rejected/dead-end ideas;
- next high-priority engineering milestone.

## Chat saturation warning protocol

If ChatGPT warns that a Humanity Loop chat is full or should be replaced:

1. **Do not delete the chat.**
2. Commit any unpromoted material decision into GitHub.
3. Refresh `PROJECT-STATE.md`.
4. For the master chat, open a new chat and use the Master bootstrap prompt above.
5. For the hourly log, migrate the scheduled worker using the Hourly log migration prompt above.
6. Archive the old thread only after the new thread is verified.
7. Never rely on a shared-link export as the continuity mechanism.

## Why this exists

ChatGPT Memory may use past chats, but it does not retain or retrieve every detail on every turn. Humanity Loop therefore assumes conversations are replaceable interfaces rather than permanent databases.
