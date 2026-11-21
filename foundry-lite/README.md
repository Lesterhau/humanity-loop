# Foundry Lite — manual zero-AppDeploy-credit execution

**Implemented source + offline tests; a real local-Ollama eight-role model run has not yet been verified.** This is an optional local adapter over existing FoundryControlPlane and budget-governor components, not a second scheduled worker or a replacement for consented outside nodes.

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

The runner uses eight logically distinct stages from the existing control-plane contract: scout, verify, assign, build_act, dissent, safety, revision and outcome. The strict first-line verifier/governor gates fail closed. Eight roles using the **same local model** are NOT eight independent AI models. One capped text output per stage (up to 256 predicted tokens), at most eight model calls and a maximum 240-second wall-clock limit. No model tools or source-fetching capability. Model-generated source claims remain UNVERIFIED. A complete cycle has status draft_review_pending, never accepted or public benefit.

## GitHub fallback without a scheduler

A new manual-only GitHub Actions workflow performs offline fixture validation and uploads a preflight receipt. It has workflow_dispatch only, no cron, no credentials, no model and no production task claims. GitHub free public-runner compute is not an unlimited GPU inference host.

## Safety

- The fixture's operator_approved true approves **only an offline local demonstration**. It is not authorization to register an outside contributor, access personal data or claim a task in the production Supabase ledger.
- All task descriptions and model outputs are untrusted. Text-only local generation has no executable tools, but its outputs still need independent human checking.
- No active-active Foundry, new worker, scheduled LLM inference, vendor credentials, third-party writes, production task lease, unreviewed public impact, or automatic external communication.
- GitHub/Render can host docs and deterministic checks. Ollama is a compute engine; Python and GitHub are not free GPU hosting.
- Current AppDeploy account reserve policy remains in force, including 350 credits minimum and no automatic paid fallback.

## Acceptance

1. Offline tests and GitHub CI pass.
2. A voluntary operator runs one capped local model cycle and supplies a review packet.
3. An independent human checks source claims and accepts/rejects the output.
4. Only then consider a dedicated inference adapter (e.g. Cloudflare Workers AI Free, if accessible), after enforcing a real quota and canonical atomic lease.
5. Before worldwide rollout, verify privacy and retention terms, source-language coverage, regional constraints, opt-in consent, reviewer capacity and abuse handling.

Reference docs: [Foundry portability](../FOUNDRY-PORTABILITY.md) · [Safety acceptance](../FOUNDRY-SAFETY-ACCEPTANCE.md) · [P1 Foundry issue](https://github.com/Lesterhau/humanity-loop/issues/14).
