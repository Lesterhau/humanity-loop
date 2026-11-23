# Foundry Lite — manual zero-AppDeploy-credit execution

**Implemented source + offline tests; first real owner-run local Ollama attempt was reported November 21, 2026 and safely HELD at stage 2.** The model was `llama3.2:1b` on a Windows 10 HP EliteBook 820 G3 (i7-6600U, 16 GB physical RAM; 4.7 GB free before model load, approximately 0.1 GB afterward). The owner-provided Claude Code report records 2 runner model calls, about 21 seconds, a Scout refusal and `VERDICT = REJECT` at Verify. No useful eight-stage model draft, cloud fallback, public-site write, accepted contribution or public outcome. The local packet itself has not been independently examined by this maintainer; do not treat a client report as a verified 8-stage run. This is an optional local adapter over existing FoundryControlPlane and budget-governor components, not a second scheduled worker.

## Costs and controls

AppDeploy Foundry native cron stays OFF. This runner makes **no AppDeploy, Supabase, GitHub or third-party site writes** and needs **no paid inference keys**. Optional text inference is sent only to an operator-owned Ollama instance at http://127.0.0.1:11434. No public listener, remote API fallback or automatic retries. Local models use hardware, memory, disk, electricity and bandwidth; open-weight model licenses vary.

## Laptop readiness: one safe command before any download

The new `scripts/foundry_lite_doctor.py` inspects OS, Python version, physical RAM, free disk and whether the Ollama executable exists. By default **it makes no network requests or AI calls, downloads nothing, changes no files or schedules, and uses zero AppDeploy credits.** The optional `--check-local` switch makes a **loopback-only** Ollama GET to `127.0.0.1:11434/api/tags` to see which models are already installed (no inference).

**Windows / PowerShell, from the cloned repository:**

~~~powershell
py -3 scripts/foundry_lite_doctor.py
py -3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --mode inspect --output "$env:TEMP/foundry-lite-inspection.json"
~~~

**macOS or Linux / Terminal:**

~~~bash
python3 scripts/foundry_lite_doctor.py
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --mode inspect --output /tmp/foundry-lite-inspection.json
~~~

The first command is read-only diagnosis; the second is a zero-model local preflight. If Python, Ollama, or RAM is insufficient, **stop** and check before downloading models. No laptop setup is required to keep Humanity Loop's current public intake and CI running.

For a **later, expressly approved local model test** only:

1. Install the official [Ollama app](https://ollama.com/download) if missing and confirm available RAM/disk before selecting a local model. Small open-weight models may be more suitable on memory-constrained machines; don't assume the earlier Qwen3 4B suggestion fits.
2. Run `ollama list` to confirm which model is actually installed. `ollama pull <model-id>` is an **optional multi-gigabyte download**, not a free cloud-hosted service; only the laptop owner should choose to run it.
3. Run `py -3 scripts/foundry_lite.py ... --mode ollama --allow-local-model --model ACTUAL_INSTALLED_MODEL --output "$env:TEMP/foundry-lite-review-packet.json"` on Windows, or the analogous `python3` command on macOS/Linux. Full flags are documented below. Do not share a raw local review packet publicly until checked for sensitive material.

## Zero-model draft (recommended before another Ollama attempt)

The CLI now supports a **useful offline review checklist without ANY model**. It is a deterministic planning artifact from the supplied task scope, clearly labeled `offline_review_plan_only`: **no URLs fetched, no facts independently verified, no actual external impact**. This allows task scoping to proceed even if a 1B model refuses to speculate or the machine cannot run inference.

**Windows / PowerShell, from the downloaded repo:**

~~~powershell
py -3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --mode plan --output "$env:TEMP/foundry-lite-plan.json"
~~~

**macOS/Linux:**

~~~bash
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --mode plan --output /tmp/foundry-lite-plan.json
~~~

`plan` is separate from `inspect`, which still only checks permissions/inputs. It is not an Ollama test and does not satisfy the model-production acceptance gate.

## Why the verifier held on the first local run

The original `verify` model instruction said **reject without reliable evidence** but `scout` had no retrieval capability: a self-contradictory requirement for a task that only asked for a proposed review checklist. The first 1B model refused to invent a source check, and the verifier correctly held. This proves the safety stop but reveals a planning-vs-evidence design error.

**Repair:** `scout` must output one concrete `QUESTION:`, two or more `CHECK:` lines and `HUMAN_REVIEW: required` without claiming any web visit. No-action refusals stop immediately as `scout_no_actionable_proposal`. The `verify` and `safety` first-line gates continue to fail closed but can allow a **bounded draft** without pretending to verify any source. `PROCEED` and `GO` apply **only to drafting permission**; all evidence and public-benefit claims remain independently unverified. Reduced prior-stage context and a 2,048-token Ollama context aim to help small CPU models, but do not guarantee good output or fit on low-memory devices.

**No rerun recommended on the current laptop while memory remains nearly exhausted.** Don't pull a larger model to solve this. The source and offline tests can be developed on GitHub without spending AppDeploy credits or consuming the laptop's RAM.

## November 22–23 G3 proof: an actual machine-retrieved source can now become an offline review plan

A real **one-time** GitHub Actions run [#45087747120](https://github.com/Lesterhau/humanity-loop/actions/runs/45087747120) acquired the approved [LUMS CITY Pakistan public HTML page](https://city.lums.edu.pk/what-we-do/city-research/dare-rc/) at **2026-11-23T00:16:07Z** (November 22 Central). The [review-only original artifact](https://github.com/Lesterhau/humanity-loop/actions/runs/45087747120/artifacts/14779857530) was downloaded and read back. It reported HTTP 200, **95,675 bytes**, SHA-256 `5d6ec6ba6dd7e1eadcab550c040249aa049aacef20fcbdca756c52a470878a95`, the visible 103/117 values and **84/117 = 71.8%** versus the public 81.6% description. The original site's copy was separately corroborated through public web retrieval. Neither raw-page hash nor text retrieval independently validates the underlying study or an institution-made correction. [Durable public-safe receipt](../runtime/mission/2026-11-23-ot013-official-live-source-acceptance.md) and [machine JSON](../runtime/mission/2026-11-23-ot013-official-html-snapshot.json).

**Acquisition is strictly bounded:** `scripts/public_source_snapshot.py` performs **no networking by default**. `--allow-live-get` enables exactly one public GET to the compile-time allowlisted LUMS URL (Tier-0 Pakistan English task and URL must match), using public DNS checks, numeric-IP TLS hostname validation, no proxies, cookies, credentials, redirects, or broad web crawling. Only HTML is supported, capped at 1.5 MB. A second automatic check, task poll, AppDeploy call or unapproved model inference is not part of the workflow. The one-off live CI acceptance step was **removed** after its success, and ordinary PR/push CI is entirely offline.

**Offline handoff of that real saved observation to a bounded Foundry review plan:**

~~~bash
python3 scripts/public_source_handoff.py --task foundry-lite/fixtures/ot013-pk-climate-review.json --snapshot runtime/mission/2026-11-23-ot013-official-html-snapshot.json --output /tmp/ot013-source-candidate.json
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/ot013-pk-climate-review.json --source-packet /tmp/ot013-source-candidate.json --mode plan --output /tmp/ot013-review-plan.json
~~~

The first script checks the archived provenance shape, exact task/case/country/source, UTC timestamp, read-only flags and arithmetic before producing an **unreviewed** source candidate. The second constructs a human review checklist, **zero model calls, zero newly retrieved sources**. A JSON file can be forged by its holder: this handoff is a trusted-repository artifact plus review workflow, **not cryptographic remote attestation or independent academic review**. Neither step grants publication or official correction status.

A **separate opt-in only** GitHub Action, [G3 Official Source Snapshot](../.github/workflows/g3-official-source-snapshot-manual.yml), uses `workflow_dispatch`, a boolean confirmation, and requires no secrets. It performs one approved official-source GET **only when manually invoked**, then retains an unreviewed artifact for three days. It is not a cron or a global web crawler. For Windows, use `py -3` and a local output path such as `"$env:TEMP/ot013-source-candidate.json"` instead of `/tmp`.

**G3 remains unreleased** until full real-model inference, independent review, cost and canonical lease enforcement are demonstrated. **G4 remains unreleased** until an actual independently verified useful public outcome outside the United States, qualified regional review and applicable data controls exist.

## Parallel G3/G4: source-candidate review packets (offline, no credits)

This is the **first executable cross-country evidence preparation contract** for the optional Foundry runner. The packet is operator-supplied and contains a case ID, jurisdiction, language(s), exact task-approved HTTPS URLs, dated candidate observations, reviewer questions, and optional arithmetic checks. The runner validates country and language against the reviewed task manifest before creating a review plan or any local model prompt. A different country, fabricated future timestamp, private URL or unapproved action fails closed.

Two sample source packets are included and explicitly set `fixture_only: true`. They are **not** an independently verified source snapshot or accepted public-benefit outcome. The Pakistan packet records the public-page arithmetic candidate: 84/117 = **71.8%**, not the displayed 81.6%; this is math, not verification that 117 is the correct cohort. The Texas WIC packet requires human competence in **English and Spanish** to assess changes or legal meaning.

From the repository root, with Python 3.10+ (no Ollama required):

**Windows PowerShell**
~~~powershell
py -3 scripts/foundry_lite.py --input foundry-lite/fixtures/ot003-us-bilingual-review.json --source-packet foundry-lite/fixtures/ot003-us-bilingual-source-candidate.json --mode plan --output "$env:TEMP/ot003-review-plan.json"
py -3 scripts/foundry_lite.py --input foundry-lite/fixtures/ot013-pk-climate-review.json --source-packet foundry-lite/fixtures/ot013-pk-climate-source-candidate.json --mode plan --output "$env:TEMP/ot013-review-plan.json"
~~~

**macOS/Linux**
~~~bash
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/ot003-us-bilingual-review.json --source-packet foundry-lite/fixtures/ot003-us-bilingual-source-candidate.json --mode plan --output /tmp/ot003-review-plan.json
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/ot013-pk-climate-review.json --source-packet foundry-lite/fixtures/ot013-pk-climate-source-candidate.json --mode plan --output /tmp/ot013-review-plan.json
~~~

This produces local `offline_review_plan_only` files. No web retrieval is made, no private data are accepted, no inference runs, no GitHub/Supabase/AppDeploy external writes occur, and no independent verification is claimed. `--source-packet` is also accepted in the existing **manually approved** `--mode ollama` path, where the limited evidence candidate is explicitly included as *untrusted reference text*—not as proof the model fetched or validated a source.

For future *real* source evidence, do not flip `fixture_only` merely to pass a test. Retrieve the actual original public page, record exact visible source text, timestamp/method, obtain independent review and qualified language/context review as needed. The packet format and static validation cannot attest retrieval independently or remove human responsibility.

**Current readiness:** G3 and G4 **development in progress**, neither release gate achieved. Acceptance still requires real bounded inference with a reliable canonical lease and cost stop (G3) and an independently verified useful real-world outcome outside the U.S. (G4). See [Mission Control](../MISSION-CONTROL.md).

## From the repository root

Zero-model validation (no external HTTP, no AI inference):

~~~bash
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --output /tmp/foundry-lite-inspection.json
~~~

Expect status preflight_only, model_calls 0, appdeploy_credits_used 0. **This is not a completed Foundry run.**

Optional one-time local inference (only if your machine already has Ollama and an appropriate downloaded model):

~~~bash
ollama list
python3 scripts/foundry_lite.py --input foundry-lite/fixtures/public-onboarding-review.json --mode ollama --allow-local-model --model YOUR_ALREADY_INSTALLED_MODEL --max-seconds 180 --output /tmp/foundry-lite-review-packet.json
~~~

Ollama homepage: https://github.com/ollama/ollama . Confirm chosen model's hardware needs and license. Do not expose Ollama to the public internet.

The runner uses eight logically distinct stages from the existing control-plane contract: scout, verify, assign, build_act, dissent, safety, revision and outcome. The strict first-line verifier/governor gates fail closed on *draft permissibility*, not independently verified claims. Eight roles using the **same local model** are NOT eight independent AI models. One capped text output per stage (up to 256 predicted tokens), at most eight model calls and a maximum 240-second wall-clock limit. No model tools or source-fetching capability. Model-generated source claims remain UNVERIFIED. A complete cycle has status draft_review_pending, never accepted or public benefit.

## GitHub fallback without a scheduler

A new manual-only GitHub Actions workflow performs offline fixture validation and uploads a preflight receipt. It has workflow_dispatch only, no cron, no credentials, no model and no production task claims. GitHub free public-runner compute is not an unlimited GPU inference host.

## Safety

- The fixture's operator_approved true approves **only an offline local demonstration**. It is not authorization to register an outside contributor, access personal data or claim a task in the production Supabase ledger.
- All task descriptions and model outputs are untrusted. Text-only local generation has no executable tools, but its outputs still need independent human checking.
- No active-active Foundry, new worker, scheduled LLM inference, vendor credentials, third-party writes, production task lease, unreviewed public impact, or automatic external communication.
- GitHub/Render can host docs and deterministic checks. Ollama is a compute engine; Python and GitHub are not free GPU hosting.
- Current AppDeploy account reserve policy remains in force, including 350 credits minimum and no automatic paid fallback.

## Acceptance

1. Offline tests and GitHub CI pass; deterministic `plan` output can be used without Ollama.
2. A voluntary operator runs one capped local model cycle and supplies a review packet. The Nov 21 run stopped after the verifier; an eight-stage model-generated draft has not been achieved.
3. An independent human checks source claims and accepts/rejects the output.
4. Only then consider a dedicated inference adapter (e.g. Cloudflare Workers AI Free, if accessible), after enforcing a real quota and canonical atomic lease.
5. Before worldwide rollout, verify privacy and retention terms, source-language coverage, regional constraints, opt-in consent, reviewer capacity and abuse handling.

Reference docs: [Foundry portability](../FOUNDRY-PORTABILITY.md) · [Safety acceptance](../FOUNDRY-SAFETY-ACCEPTANCE.md) · [P1 Foundry issue](https://github.com/Lesterhau/humanity-loop/issues/14).
