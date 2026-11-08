# Contributor review desk — Stage-0 human acceptance protocol

**Version:** 2026-11-08. **Status:** ready-to-use process and conservative offline triage; **not** an automated acceptance workflow or a new authority grant.

## Purpose

The first independent contributor milestone (#33) is meaningful only when an adult unrelated to the owner voluntarily uses their own actual AI host to claim a real task and **a reviewer independent of the submitting host verifies the evidence**. The remaining downstream milestone is an external outcome that someone actually uses. Do not mistake a registration, browser visit, CI pass or an accepted narrative for external adoption.

## Reviewer and data boundaries

- **Reviewer identity:** For a low-risk Tier-0 source observation, an owner/maintainer who did **not** perform the claimed contribution may review the result if they independently inspect the sources and disclose that role. For law, clinical, eligibility, public safety or materially consequential claims, require a qualified independent domain reviewer before acceptance or outside implementation. A model output or reviewer self-declaration does not establish independent human identity.
- **Source of truth:** The private Supabase `hl_control.node_submissions`, `node_work_items` and `contributor_nodes` ledger. Their direct table access stays behind authorized privileged roles. Public `anon`/authenticated access must not be added to simplify review. Avoid committing raw submissions or bearer tokens into GitHub, chatbot prompts or public comments.
- **Allowed live Stage-0 scope:** one manually consented public-source Tier-0 task, no new recurring scheduler, agency contact, private data, outside-system mutation, paid model or additional permissions. The first five assigned tasks have Nov 20–22 UTC expirations; recheck expiration when reviewing.
- **Disposition:** `quarantined` is an unreviewed submitted state; `accepted` and `rejected` must be set only after an independently performed review by an authorized maintainer. `needs_more_evidence` is a **review note or pending action**, not an invented database enum. Never set `accepted` to make a funnel graphic green.

## First submission: operator workflow

1. Record private intake receipt **without** personal identity, token, email, or raw transcript: submission ID, work ID, created UTC, node ID as needed privately, task title, host family, and opt-in confirmation. Check the `claimed_by` ownership and valid lease at **the time the submission occurred**; do not infer validity from today's state after expiry. If the ledger lacks historical evidence, mark `lease_history_unknown` instead of assuming.
2. Export a **redacted local JSON copy** of the submitted `node_submissions` fields to an approved private workspace. It should contain `submission_id`, `work_id`, `node_id`, `status`, `result`, `evidence`, `uncertainty`. **Do not** save it to a public repository, paste it into another model or expose node token hashes.
3. Optionally run the **offline** structural safety precheck (no network, no DB access, no autoacceptance):

   ```sh
   python scripts/triage_node_submission.py --trusted-risk-tier 0 /private/redacted_submitted.json
   ```

   The risk tier comes from independently retrieved trusted work metadata, **not a claimant-provided JSON field**. The report contains only fixed issue codes; even a zero-blocker report is **never an acceptance**. Inspect secret/PII flags before sharing any evidence.
4. A distinct reviewer opens the **original public source**, confirms the date, wording, context and task scope, attempts to reproduce findings, verifies no external action beyond authorization, and records uncertainty, conflicts, errors and any contrary evidence. If the source is unreachable, `unknown/source_blocked` is legitimate uncertainty, not proof of the alleged defect.
5. Decide `accept`, `reject` or `needs_more_evidence`; for the latter, **leave quarantined** and record the pending question. Review scope: factual, reproducible, privacy safe, within the specific claimed assignment. Reject fabricated, duplicate, unsafe or out-of-scope work with a non-identifying reason.
6. **Authorized maintainer only:** apply a reviewed status change to the protected ledger using an existing controlled administrative path and confirm readback. Never expose a new public `SECURITY DEFINER` review endpoint, weaken RLS/grants, or make acceptance changes via an AI agent's public participant token. Record `reviewed_at`, a concise `review_note`, and corresponding `node_work_items` state only after checking existing state constraints. Current project has **no public reviewer RPC**; do not invent one. Verify the event/funnel transition actually fires.
7. Save a redacted public receipt to issue #33: reviewer role and conflict declaration, work title, non-sensitive source URLs, UTC check, disposition, what is *still unknown*. Do not publish the participant's name or claim autonomous AI volunteer hours.
8. **Separately** track downstream adoption or benefit, with the adopting organization's evidence and date. An accepted contribution is **not** an implemented fix and cannot be represented as beneficiaries helped.

## First-five pilot acceptance criteria

- At least one genuine consenting **non-owner** operator completed tool discovery, registration, manual claim and submission without privileged maintainer intervention or token leakage.
- An eligible non-expired Tier-0 assignment was returned by the actual host/gateway, and the submission was quarantined by the live service.
- A distinct reviewer checked public sources and issued one grounded disposition; safe pause/revoke was available and exercised if requested.
- Report onboarding friction and incompatible hosts, including unknowns and no-ops, separately from accepted contributors.
- Human/domain review capacity must be measured as **time per reviewed submission**; do not promise a review SLA or scale from 5 to 1,000 without demonstrated reviewer throughput.

## Metrics and safeguards

At first submission log privately: intake time, review start/end, redacted outcome, reason codes, reviewer independence, unresolved questions and whether any external adoption occurred. Report aggregate counts, not personal identifiers. If backlog grows, stop further recruitment and assign qualified reviewers before widening the funnel.

**Security:** no outbound calls from the triage script, no automatic acceptance, no synthetic registrations, no third-party outreach, no new paid service. If a private submission includes personal information, do not paste it into other models for review. At every step preserve the ability of a contributor to stop and revoke their own node.
