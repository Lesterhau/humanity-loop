# Humanity Loop — Claude and Perplexity zero-cash handoff

**Status: protocol drafted, NOT a verified live connection.** See [#56](https://github.com/Lesterhau/humanity-loop/issues/56). As of November 5, 2026, the existing private advisory inbox holds dated October 29 Claude/GPT/Gemini snapshots; it does not provide streaming access to Claude or Perplexity account chats.

## One receipt, one owner, one disposition

Use the existing authorized Instinct-mediated private GitHub repository `Lesterhau/instinct-advisory-inbox`, under `humanity-loop/inbox/`. Do not write to unrelated private folders, and never copy secrets, account emails, private beneficiary details or unredacted conversation logs. If the agent lacks explicit GitHub write permission, it must produce a **draft for owner/Instinct to submit**; a chat response is not an accepted delivery.

Each newly delivered public-safe JSON receipt must contain:
```json
{
  "schema_version": 1,
  "project": "humanity-loop",
  "source_provider": "claude-or-perplexity",
  "source_agent": "case-steward-or-scout",
  "observed_at_utc": "2026-11-05T00:00:00Z",
  "run_id": "unique-provider-run-id",
  "case_or_task_id": "existing-humanity-loop-case-or-scout-cell",
  "primary_evidence_urls": ["https://example.gov/verified-public-page"],
  "observation": "one factual, redacted summary",
  "uncertainty": "what cannot be verified",
  "proposed_next_action": "specific permitted next check",
  "consent_scope": "read-only-public-sources",
  "new_cash_spend": 0,
  "approval_state": "not_authorized",
  "result_status": "proposed"
}
```
The example above is a schema illustration, **not a real contribution**; source URL must be replaced with an actual checked link.

Proposed destinations, only once authorized to write in the private inbox:
- `humanity-loop/inbox/HL-CLAUDE-CASE-STEWARDSHIP-<UTCdate>-<runid>.json`
- `humanity-loop/inbox/HL-PERPLEXITY-SCOUT-<UTCdate>-<runid>.json`

## Instructions to give the existing Claude Case Steward

Read current Humanity Loop public governing documents and the last accepted case state. Choose one genuinely due previously reported case (not new arbitrary claims). Search primary public sources; report exact current URL, source timestamp, observation, contradiction, next due check and uncertainty. No external outreach, private account access, form submission, metered API use or paid upgrade. Produce one JSON receipt with the schema above. Use only the already authorized private GitHub inbox route if actually permitted; otherwise return the full draft to the owner/Instinct without claiming delivery.

## Instructions to give Perplexity Scout (owner-controlled only)

Within a genuinely available no-new-cash consumer quota, discover one high-value Tier-0 public-source correction or neglected service-access lead that is NOT already logged. Check original official sources and one independent cross-reference; separate evidence from inference. Stop on quota or purchase prompts, no new paid Computer tasks or API. Produce one JSON receipt under the schema above; deliver through an already authorized relay only, otherwise return a draft.

## Original ChatGPT hourly worker's receiving contract

1. Read private inbox commit metadata when actually available. Only a **new** dated Claude or Perplexity receipt qualifies; old Oct 29 advisory files do not.
2. Validate schema, official URLs, claims, project scope, no sensitive content, duplicate hash/run ID and prior case state.
3. Produce an **acknowledgment/disposition** `accepted_for_review` / `needs_evidence` / `duplicate` / `rejected`; these are not authorizations to contact anyone or spend credits. Record in allowed public-safe ops issue or private receipt ledger if explicitly authorized; otherwise give owner a bounded draft.
4. Recheck on a later worker run to ensure no second action on the same receipt. A verified live connection requires one fresh, source-read-back receipt from EACH provider and one deduplicated acknowledgment. Until then label integration `UNVERIFIED`.
