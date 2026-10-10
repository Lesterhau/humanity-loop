# Humanity Loop: Operations Sentinel

## What it is

This is a smoke alarm, not another artificial-intelligence manager. GitHub runs it automatically once an hour, even if this ChatGPT conversation or the Hourly Worker disappears.

It checks three saved results: daily weather/emergency-alert review (CAP), daily federal-policy change review, and six-hour medical-guidance change review. It also checks for the Hourly Worker's short 'I ran' note. Missing notes mean the worker is **unverified**, not necessarily broken.

If there is a problem, it opens or updates **one** GitHub issue called `[Ops Sentinel] Humanity Loop needs maintenance attention`. If the monitored data recovers, it closes that specific issue. There are no automated emails to agencies, no spending, no schedule changes, and no restarting Foundry. All it has permission to do is read saved evidence and manage that dedicated GitHub issue.

## Where to click

1. [Click here to see whether Ops Sentinel ran](https://github.com/Lesterhau/humanity-loop/actions/workflows/ops-sentinel.yml). Each run has a green check for success or a red X for failure.
2. [Click here to look for an Ops Sentinel warning](https://github.com/Lesterhau/humanity-loop/issues?q=is%3Aissue+is%3Aopen+Ops+Sentinel). Open the issue and follow its **What to do** section.
3. [Click here to read the last saved status](https://github.com/Lesterhau/humanity-loop/blob/main/runtime/ops-sentinel/latest.json). The first full scheduled run must produce the file; a missing file before then is not proof of failure.
4. [Click here for the restart instructions](https://github.com/Lesterhau/humanity-loop/blob/main/CHAT-CONTINUITY.md).

## If ChatGPT disappears

Open the Ops Sentinel GitHub Actions page above first. If its latest run is green, the independent scanner is running. That alone does **not** mean all Humanity Loop activity is succeeding. Check for open Sentinel issues and current receipts.

If a warning exists, use the issue to direct a new AI assistant or a human developer. When ChatGPT is available again, write: `Resume Humanity Loop from the GitHub CHAT-CONTINUITY.md, PROJECT-STATE.md, and open Ops Sentinel issue. Verify live state before changing anything.`

## How alerts reach you

The watchdog uses GitHub issues, not ChatGPT notifications. To receive GitHub emails, open your GitHub profile image (top right) -> **Settings** -> **Notifications**, review email notification settings; also open the Humanity Loop repo and select **Watch** -> **Custom** -> **Issues** (if available). Check you actually receive a test notification. Being assigned an issue may notify you depending on your GitHub settings. We have **not** independently tested email delivery.

## Limits (important)

- A green 'Ops Sentinel' run is only evidence these checks ran. It does not prove successful model execution inside AppDeploy Foundry.
- The Hourly Worker must explicitly write `runtime/ops/hourly-worker.json`; a missing heartbeat becomes a warning after the rollout grace period (October 11, 2026, 09:00 UTC).
- A heartbeat is self-reported. Verified output should include a date and direct link to the independently confirmed result.
- If GitHub Actions itself is down, this watchdog may not run. The GitHub Actions page and notifications are the second check.
- Future improvements: add an authorized read-only Foundry/Supabase monitor and independent end-to-end test; never publish service-role tokens or privileged credentials.

## What we're deliberately not doing

We are not paying for another AI agent, spinning up another Foundry executor, or choosing between duplicate scanners without preserving their data. A separate supervisor AI could still hallucinate and fail along with the worker; a simple independent program establishes a firmer floor.
