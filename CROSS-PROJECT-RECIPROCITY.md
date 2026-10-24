# Humanity Loop ↔ Morrow: bounded reciprocal improvement

**Effective October 22, 2026.** Owner-authorized reciprocal process. Two repositories, two separate missions, **no shared runtime authority**.

- Humanity Loop: public-interest project, this PUBLIC repository.
- Morrow Engine: owner's PRIVATE commercial project. Never copy its proprietary source, internal plans, opportunities, documents, private logs, business intelligence, prompts or credentials into Humanity Loop.
- Morrow may separately inspect Humanity Loop's published files. Humanity Loop's automated public workflow **does not fetch or authenticate to Morrow**.
- The reusable inputs on this side are the owner's **explicitly approved generic principles**: bounded reversible experiments, explicit intent/test/verify/record, claim-vs-completion distinction, backoff after failure, privacy and spending boundaries, avoiding duplicate schedulers, and transparent outcome accounting. These are not a disclosure of private Morrow implementation.
- Any additional specific Morrow-derived proposal must first be sanitized and explicitly approved for publication **before** it enters this repository. There is no implicit cross-project read, write, or automatic approval.

## How this side actually operates

This repo reuses **the existing hourly Ops Sentinel GitHub Actions schedule**: `.github/workflows/ops-sentinel.yml`. A very small local-only script `scripts/reciprocal_audit.js` checks whether a weekly receipt is due. If so it inspects only five **allowlisted public Humanity Loop files**. It compares explicit process invariants with current operating instructions and writes `runtime/reciprocal-audit/latest.json`.

- No second ChatGPT task, no extra cron, no clone/fetch of Morrow, no personal account access, no third-party API requests or model inference, no payment.
- A weekly receipt should be generated at the first scheduled or manually dispatched Ops Sentinel run **at least seven days after the last receipt**. GitHub schedules can skip/delay; never imply precise weekly timing without observed run dates.
- Five deterministic regression tests and the audit use Node's built-in modules; audit failure must not prevent Ops Sentinel's independent watchdog.
- The output holds **one bounded candidate at a time** and describes a justified action or honestly says no change is warranted. It does **not** edit production code or external services without independently scoped authorization and tests.
- The existing Ops Sentinel write permissions are reused solely to persist these public receipts. No Morrow token or new secret may be inserted.
- A public receipt or CI pass establishes only technical process evidence, **not reciprocal learning, institutional impact or independent agent execution**.

## Execute → verify → commit

For any candidate produced by the weekly script, the existing main Humanity Loop worker or authorized specialist must:

1. Check whether a parallel task or issue already owns the same defect, and whether it is currently important.
2. Select **one reversible internal improvement** with small blast radius, no spending and a checkable rollback.
3. Preserve an intent record; make the smallest allowed change; run relevant deterministic tests and independent readback.
4. Write the corresponding actual change or hold to canonical state with exact commit/run links. Do not count a plan or issue as execution.
5. If the candidate is no longer important or all invariants pass, record **no-op with evidence** instead of inventing a change. Scheduled audits cannot force improvement opportunities into existence.

**Initial first-cycle tangible improvement:** The previously documented native AppDeploy status contradicted three earlier unqualified `enabled` assertions in `AUTOMATION-PROMPT.md`. Commit `0823d8c963ecd593e035819291b883814f343232` replaced those claims with accurate **last-verified Oct20 disabled** facts and mandatory live rechecks. This prevents an hourly worker from using stale declarations to spawn duplicate work. It is a technical documentation/decision-quality fix, **not a public-interest outcome**.

The pending case-delegation improvement should transfer repetitive SSA/VA/WIC checks into a named steward lane, with due dates and summary receipts. No Claude worker is claimed installed or scheduled until its separate platform schedule has been proven. Start Claude using its **documented hourly schedule**, with a low-cost check and substantive rereviews no more often than every four hours per case unless new evidence or urgency justifies it; see `CLAUDE-CASE-STEWARD.md`. A separate Claude schedule is NOT yet configured or independently confirmed.

## First verified audit → actual fix (October 22)

The existing Ops Sentinel workflow's [run #77](https://github.com/Lesterhau/humanity-loop/actions/runs/39874749564) successfully completed six `test_reciprocal_audit.js` cases, performed its existing watchdog checks, and saved the [first bounded audit receipt](runtime/reciprocal-audit/latest.json), `2026-10-22T23:54:00Z`. The receipt selected `case-delegation-absent`, explicitly `status: not-executed`; this was a proposed action, not an automatically completed change.

**Human-executed authorized follow-through in this project:** added the [Claude Case Steward configuration](CLAUDE-CASE-STEWARD.md) as a read-only setup contract (GitHub commit `2749a83695b5d6cfaab38d8a225dccedbf81f552`), and corrected the canonical [hourly operating instructions](AUTOMATION-PROMPT.md) with a named case lane (commit `867e9f8f85256eeaea78b632d5ad991d9ab9fb06`). [Resolution receipt](runtime/reciprocal-audit/resolutions/2026-10-22.json) independently records this technical repair. The Claude cadence was later refined to its actually documented built-in hourly schedule (rather than a nonexistent manual four-hour scheduler), with deep case reviews gated by due dates. **No external Claude worker is yet connected, scheduled, or independently proven to have performed this role.**

A single successful scheduled/triggered process run is **not evidence** of seven-day recurring reliability. Later runs must be verified by actual GitHub Actions job and `runtime/reciprocal-audit/latest.json` timestamps. This side has no private Morrow read/write access, so the ongoing reciprocal *learning* bridge still needs owner-approved sanitized method proposals to move from Morrow to public Humanity Loop.

## Risk-proportionate execution thresholds

- **Low:** public internal docs, tests, deterministic reversible fixes: proceed when inputs are known, tests pass, and a rollback exists.
- **Moderate:** live workflow/API changes: staged verification, narrow permissions, clear state, a durable result and rollback.
- **High:** spending, new credentials, wider permissions, public posting, sensitive data, external institutional effects: retain governing approvals; never reframe high-risk actions as internal work.
- Tool safety refusals are **not** debugging targets to bypass. Record one concrete blocker and an independently safe alternative, without retrying rejected operations across tools.

## Continuity and private-information boundary

Canonical files here: `CROSS-PROJECT-RECIPROCITY.md`, `scripts/reciprocal_audit.js`, `scripts/test_reciprocal_audit.js`, `runtime/reciprocal-audit/latest.json`, `AUTOMATION-PROMPT.md`, `PROJECT-STATE.md`.

Morrow's side runs under its **own** owner-approved private policies. A Morrow-side commit saying “weekly” is not evidence that the schedule ran; each side must verify its own workflow run and receipt. Do not accept circular self-attestation as an outcome. Future new chats/agents read these canonical public records without needing access to the other's private repository.


## Public methods integration — proposed October 24, 2026

The owner has approved and released generic reusable methods through the distinct **PUBLIC** repository [`Lesterhau/morrow-methods`](https://github.com/Lesterhau/morrow-methods). These are not the private Morrow Engine sources, and the public methods text does not confer execution authority.

This project's existing weekly audit now has a read-only, pinned public-source verifier:

- `scripts/public_methods_source.js` fetches exactly the public `METHODS.md` file at commit `f6fd07bac3eb42c5068d6d9c8e9dcc1e8e623109` from GitHub's raw public host; no access token or private source is used.
- The content is bounded to 32 KiB, the Git blob hash is checked against `b5378330d38a1e2d622d2270b8a457ad2924897c`, and redirects or unexpected HTTP status are rejected. A change upstream requires a separately reviewed re-pin.
- `scripts/reciprocal_audit.js` records only whether that public source was verified, its pinned commit, byte count and hash. The full document is never embedded in the generated public audit receipt, and no private Morrow data is requested.
- The verifier is called **only when the existing seven-day audit is due**, using the existing Ops Sentinel schedule. If public GitHub is unavailable or the content differs, status is `unverified`, and the original local Humanity Loop checks proceed independently. An unverified document is not adopted as an instruction.
- Regression tests mock HTTP requests: no test fetches private resources, and failing/tampered remote material never creates a false verification claim.

**Important limits:** Passing these integrity checks proves only that the selected public text matches the approved release; it does not certify that the methods are effective or authorize changing Humanity Loop policy. The existing human/automated governance boundaries remain authoritative. A green CI run does not prove that a live network fetch or real-world benefit occurred; inspect a later weekly receipt to establish the former. No new scheduler, account, secret, paid API or public-to-private sync is created.
