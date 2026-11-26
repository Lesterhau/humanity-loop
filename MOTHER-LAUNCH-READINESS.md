# MOTHER launch readiness — finite release checkpoint

Owner-approved direction, November 25, 2026: MOTHER stays publicly quiet until blue check and launch readiness. **HOLD.** This is a proposed milestone between G4 and mature G5, not a claim of accepted G4/G5 or permission to post. Preserve the earlier mobile plugin release gate in MOTHER-X-LAUNCH.md unless the owner separately approves a revised launch policy.

## Deliver the smallest safe release

1. Closed beta: first accepted independent adult node, private consented Passport record; grow to five accepted nodes over at least two hosts. Invitation-bound admission is a required future control, not an implemented restriction. The current gateway cannot reserve a slot for an invitee. Do not open a new cohort before independent acceptance of that control; any existing limited pilot must retain its separate authorization and consent boundaries. No mass recruitment.
2. Controlled expansion: target 25 accepted independent nodes, staged toward 100 only when review/assignment capacity permits. Distinct consenting operators and actually reviewed contributions, not registrations.
3. Launch checkpoint: withstand a **synthetic 10,000-interest-request burst** in disposable isolated rehearsal. Interest does not equal an active node. Actual activation is capped by available reviewed tasks, review throughput, cost and operator-approved concurrent capacity. No real-person contact, production load test or paid resource in this rehearsal.
4. MOTHER public launch: only after explicit owner GO, all applicable evidence gates, real blue check, approved content and a safe intake route. Initial publication is human-reviewed and manually authorized. No automated replies without prior explicit written X approval. Long-term target 20k active nodes and 1k monthly recurring donors is G5-B, not required before first publication.

## The specific capacity gap

Repository source at e15ad3f8257187648a73decc235342be8e509ef2:
- mcp-server/app/join/page.tsx directly sends a visit telemetry request on mount and a registration request to the contributor gateway.
- mcp-server/app/api/mcp/route.ts and mcp-server/lib/contributor.ts also expose registration through that gateway.
- supabase/functions/contributor-node/index.ts invokes a per-fingerprint registration rate gate with a 60-minute window and 5 attempts. This is **not evidence of a global admission budget**. Do not substitute a UI-only cap.
- mcp-server/app/start/page.tsx offers no-account email intake and an existing Stripe support link. Neither a high-volume inbox SLA nor recurring payout/cancellation is proved by a link.
- No live capacity, privacy or payment acceptance was performed in this review.

Next implementation must use **one authoritative transactional admission decision** shared by the two registration paths. Reserve/release capacity atomically with registration (not a separate check-then-write), deduplicate retries without minting duplicate nodes, enforce consent and Tier-0, fail closed if unavailable; do not add credentials or new data collection before review. Preserve existing active nodes' pause/revoke and review access when new admission stops. Apply independent limits to incoming interest, registrations, active leases and unreviewed submissions. Use existing project/approved private storage only after privacy/deletion review; if not available, show a no-data capacity notice rather than collecting an unbounded list.

A synthetic burst rehearsal must distinguish accepted interest, retry, duplicate, deferred and rejected requests, demonstrate exact accounting and enforce no admission beyond the configured cap. No live stress test until separately authorized. Measure latency, write amplification, reviewer backlog and actual provider costs; establish numeric production caps from measured capacity, not guessed targets.

## X release boundaries

Official sources (checked Nov 25): https://help.x.com/en/managing-your-account/about-x-bluecheck ; https://help.x.com/en/rules-and-policies/x-automation ; https://help.x.com/en/using-x/automated-account-labels . Finalize profile before any separately approved Premium purchase; confirm actual displayed check and account eligibility. Blue check is not platform endorsement or automated-reply authorization. AI reply bots require prior written explicit X approval. Automated-account labeling and connection to a human-managed account apply to automated operation. No unsolicited automated engagement, mass tags or follower manipulation. Human-reviewed draft posts can be prepared privately without publication. Explicit approval is required to buy, connect, post or send an approval request.

## Exit criteria

The machine-readable checklist in ops/mother-launch-readiness.json is deliberately HOLD with no invented evidence. Each row needs real independent acceptance or documented owner-approved scope reconciliation (never waive safety, privacy, platform rules or spending authority). No paid support required to participate, and no badge sold. All gate statuses remain unchanged. A release decision is human-controlled, never a workflow trigger.
