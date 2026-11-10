# Humanity Loop — first-contributor intake alerts

**Owner direction (November 8, 2026):** After publicly inviting 3–5 friends to participate, the owner specifically asked whether Humanity Loop will report when people complete tasks.  Do not interpret a friend commenting on Facebook as a registered or completed node.  The existing hourly worker is the only approved scheduled coordinator: **no new scheduler, paid webhook, email provider, or social posting**.

## Truth and lifecycle

Actual registration, claim, submission and independent review have distinct states.  A newly arrived `hl_control.node_submissions` row in `quarantined` means **received and awaiting review**, never "completed and accepted."  Only a reviewed `accepted` status can be counted as an accepted contribution, and an accepted contribution does not establish downstream adoption or public benefit.

An hourly polling loop is **not** an instant push notification.  Automation delivery is subject to task execution and user notification settings.  It must not promise instant alerts or reveal participant names, token hashes, raw answers, private host transcripts, or any individual health/sensitive record.

## One bounded read-only check at the start of each existing hourly worker run

If the connected production Supabase query capability is available, read only **aggregate** rows from the canonical project `jxtcccrlnhkcjfnwlfea`:

```sql
select
  (select count(*) from hl_control.contributor_nodes) as registrations,
  (select count(*) from hl_control.node_submissions) as all_submissions,
  (select count(*) from hl_control.node_submissions where status = 'quarantined') as awaiting_review,
  (select count(*) from hl_control.node_submissions where status = 'accepted') as accepted,
  (select count(*) from hl_control.node_submissions where status = 'rejected') as rejected,
  (select count(*) from hl_control.node_work_items
    where status = 'open' and risk_tier = 0 and expires_at > now()) as available_tier0;
```

Read latest previously reported aggregate milestone in [issue #33](https://github.com/Lesterhau/humanity-loop/issues/33) or the existing worker's own latest verified result.  Compare cumulative **all_submissions** and **accepted**; falling `awaiting_review` alone is not acceptance.  If a new submission appears, report to the owner: "A new contribution was submitted and is awaiting independent review" + current aggregate counts.  If `accepted` has genuinely increased, report the new accepted count separately, after verifying source/independent reviewer receipts.  For rejection, alert only if it materially needs owner action.  Otherwise **no notification** just because an unchanged count was read again.

Cumulative counts are a pragmatic zero-new-storage dedup baseline.  If the worker cannot confidently determine whether a change is new, report **UNKNOWN / cannot verify milestone**; do not notify repeatedly or claim completion.  If production Supabase is inaccessible in the scheduled environment, report that blocker **once**, point to this document and issue #33, and request the specific connection authorization needed; do not work around credentials or send information to unapproved services.

**After new submission:** use [REVIEWER-RUNBOOK.md](REVIEWER-RUNBOOK.md) when present on `main`.  A qualified human must independently check the original public sources, work scope and evidence before any approved acceptance action.  Avoid any status writes by the scheduled worker and leave `quarantined` unchanged pending review.  Don't use a public GitHub issue comment to store the contributor's actual work or personal identifiers.

## While waiting for volunteers

Keep doing one novel, mission-useful authorized job each run: benefits-code regression, independent source-backed external problem, or useful safety fix.  The alert check should take a few seconds of read-only work, not consume the whole hourly iteration.  No artificial deadlines or "no new node" spam.

## November 9, 2026 — new AI-optional manual reports

**Separate intake lane, distinct from nodes:** The friend-beta site now offers a single low-risk public-source observation via `https://humanity-loop.vercel.app/try`. It asks volunteers using any AI, or no AI, to email a brief report to the existing verified supervised AgentMail inbox `mother.humanityloop@agentmail.to`, subject `Humanity Loop - One-time public-page check` (and the original legacy subject `Humanity Loop - One-time ChatGPT public-page check` so earlier messages remain discoverable), or send it privately to the owner. This is a MANUAL, UNREVIEWED report, not a registered node, quarantined node submission, accepted outcome or human volunteer-hour claim.

**Existing hourly worker only, if its connected tools permit**: Read the inbox's **message metadata only**, filtered by the exact subject and messages arriving after launch on 2026-11-09. If a new qualifying message is found, notify the owner **once** with a safe count and generic disposition: "A manual ChatGPT public-page check arrived and needs private review." Deduplicate using the latest previously observed message ID / UTC receipt; if provenance is unavailable, mark the notification as possibly duplicate, do not assume fresh. Do not copy sender names, addresses, body text or any private evidence into GitHub comments, public issue trackers, marketing, or automation descriptions.

Manual review: ask a separate person to inspect the source URL and the human-confirmed observation using the [REVIEWER-RUNBOOK.md](REVIEWER-RUNBOOK.md) standards; reject invented claims and sensitive content. If a real public correction opportunity emerges, obtain owner approval before external contacts or publication. A "no issue found" or inaccessible page is a valid negative result. Do not move manual reports into `hl_control.node_submissions` or artificially increase node counters.

If the scheduled worker does **not** have access to the inbox plugin, record `manual_inbox_monitor_not_connected` once and do not pretend to monitor; the owner can check inbox manually or ask an authorized ChatGPT session to do so. No new scheduler, email forwarding, outgoing reply, paid model, or background polling provider is authorized.
