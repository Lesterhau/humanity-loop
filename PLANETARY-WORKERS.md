# Planetary Systems Workers — Live Runtime

Humanity Loop's Planetary Systems division is live as a bounded Foundry specialist layer.

## Worker topology

Parent:
- `foundry_chatgpt_hourly`

Always warm:
- `planetary_accountant` — Planetary Impact Accountant

Demand-activated / reserve:
- `planetary_compute_water` — AI compute + data-center energy/water
- `planetary_grid_energy` — grid, storage, transmission, flexibility, zero-carbon generation
- `planetary_carbon_methane` — methane, carbon removal, industrial decarbonization
- `planetary_ocean_coral` — ocean/coastal/coral resilience
- `planetary_minerals_circularity` — critical minerals, reuse, substitution, circularity

Each worker is a child of the bounded Foundry scheduler and inherits its permission/tool/budget ceiling. Reserve specialists are activated only when a queued task needs them.

## Evidence gate

Planetary work requires:
- lifecycle evidence proportionate to the claim;
- explicit additionality assessment;
- measurable outcome metrics;
- uncertainty ranges;
- separate treatment of carbon, water, materials, biodiversity, reliability, cost, and community burden;
- no offset/net-positive claim from speculative benefits;
- falsifiable next review or closure criteria.

## Review ledger

Live table:
`hl_control.planetary_reviews`

Each review records:
- source Scout signal when applicable;
- assigned Planetary workers;
- lifecycle evidence;
- additionality;
- expected benefit;
- environmental cost;
- non-fungible tradeoffs;
- measurable outcome metrics;
- SCALE / HOLD / REALLOCATE / REJECT / RESEARCH decision;
- next review.

## First real review

Source:
Scout Mesh signal `97cf7dfc-d6f1-48bd-b7f2-b63db3acdb4e` on water-free high-density AI cooling.

Assigned:
- `planetary_compute_water`
- `planetary_accountant`

Decision:
**RESEARCH / do not scale from prototype evidence.**

Reason:
The evidence establishes active validation and prototypes, but does not establish full-system lifecycle superiority, production reliability, or net environmental benefit.

Required outcome measurements include:
- water per unit of useful compute;
- total cooling-system energy;
- full-system efficiency;
- working-fluid leakage/GWP/toxicity;
- material burden;
- failure/reliability rate;
- retrofit material/capital requirement;
- production deployments beyond demonstrations.

The compute/water specialist returned to reserve after the review.

## Humanity Loop self-footprint gate

Live function:
`hl_control.planetary_self_footprint_snapshot()`

It summarizes observed `hl_control.usage` records and returns telemetry coverage plus an expansion rule.

Current verified state at division launch:
- usage records: 0
- telemetry: insufficient
- expansion rule: `HOLD_ENVIRONMENTAL_CLAIMS_AND_AVOID_UNBOUNDED_EXPANSION`

This is intentionally conservative. A zero recorded footprint is **not** interpreted as zero real footprint.

Once telemetry exists, the accountant uses `ENVIRONMENTAL-BREAK-EVEN.md` and `scripts/environmental_break_even.py` to compare marginal resource cost with evidence-discounted attributable benefit.

If marginal environmental cost exceeds plausible benefit—or the missing-data range can reverse the decision—the accountant recommends HOLD/REALLOCATE rather than expansion.

## Operating cadence

At least daily:
1. inspect self-footprint telemetry coverage;
2. flag missing/partial usage data;
3. inspect due Planetary reviews;
4. activate the smallest required reserve specialist;
5. apply lifecycle/additionality/non-fungibility rules;
6. return specialist to reserve after the bounded task unless recurring workload justifies warm status.

Scout Mesh escalations may create Planetary reviews, but a weak signal does not become an environmental claim by default.
