# Humanity Loop Hourly Log Migration Prompt

Use this only if the current hourly-worker chat needs to be replaced.

Copy and paste exactly into the replacement chat:

> **Migrate the Humanity Loop hourly worker to this chat. Treat https://github.com/Lesterhau/humanity-loop/blob/main/AUTOMATION-PROMPT.md as canonical. Inspect the existing Humanity Loop hourly automation first. Disable the old worker only when necessary to avoid duplicate hourly runs, then recreate it here at the same hourly cadence. Verify the new worker is active before declaring migration complete. Do not alter unrelated scheduled tasks.**

Important:
- The hourly worker's **full instructions live in `AUTOMATION-PROMPT.md`**.
- Do not run two hourly workers at once.
- Verify the replacement before archiving the old hourly log.
