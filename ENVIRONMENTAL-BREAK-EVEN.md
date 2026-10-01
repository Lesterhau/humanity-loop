# Environmental Break-Even & Compute Scaling

Humanity Loop should pursue environmental impact aggressively, but scale should be governed by a **net-impact model**, not by either extreme:
- "never compute because computing has a footprint";
- "compute without limit because future benefits might save the planet."

## Environmental accounting is a vector

Track at least:
- electricity (kWh);
- operational carbon (kg CO2e, with uncertainty);
- cooling water (liters, location-sensitive);
- hardware/material burden where estimable;
- additional infrastructure impacts.

Do not collapse water, carbon, biodiversity, and materials into one fake universal number unless a decision model explicitly states the conversion assumptions.

## Own-footprint function

Let:

- C_r(t) = cumulative Humanity Loop cost for resource r through time t.
- B_r(t) = cumulative environmental benefit attributable to Humanity Loop for resource r.
- a_i = attribution fraction for intervention i.
- q_i = evidence-quality/confidence discount.
- d_i = durability/additionality factor.

Then:

B_r(t) = Σ_i [ gross_benefit_(i,r,t) × a_i × q_i × d_i ]

Net_r(t) = B_r(t) - C_r(t)

For carbon, break-even is:

t*_CO2 = inf { t : Net_CO2(t) ≥ 0 }

Water and ecosystem effects should usually have their own break-even conditions because geography and ecological context matter.

## Exponential-growth model

If a simplified intervention portfolio produces environmental benefit at instantaneous rate:

b(t) = b0 × exp(g_b t)

and compute/resource cost grows at:

c(t) = c0 × exp(g_c t)

then cumulative benefit and cost are:

B(T) = b0/g_b × [exp(g_b T) - 1]

C(T) = c0/g_c × [exp(g_c T) - 1]

for nonzero growth rates.

The payback time T* solves B(T*) = C(T*).

Key implication:
- if benefit learning/scaling persistently grows faster than resource cost, early investment can rationally be net-positive despite an initial deficit;
- if resource cost grows at least as fast and the benefit rate never catches up, "future exponential impact" is not a rescue argument.

Use numerical root-finding and Monte Carlo uncertainty once real telemetry exists.

## Evidence-discounted payback probability

Because both footprint and future impact are uncertain, estimate a distribution rather than one T*.

Track:

P(T* ≤ H)

for decision horizons H such as 90 days, 1 year, 3 years, and 10 years.

Scale compute when added capacity materially increases expected environmental benefit and the probability of eventual payback remains credible.

If repeated evidence shifts the payback distribution outward, reallocate compute toward higher-yield projects rather than simply shutting down Humanity Loop.

## Mandatory productive fallback

An hourly worker should not no-op merely because no brand-new project clears a high threshold.

If there is no new high-impact action, use the cycle to advance the highest-value existing backlog:
1. planetary/environmental research or engineering;
2. validation/replication of live work;
3. unknown-unknown scouting;
4. maintenance that prevents project failure;
5. capability/tool improvement;
6. evidence synthesis;
7. contributor/network infrastructure.

The system may still avoid wasteful duplicate searches. "Always productive" does not mean "always burn maximum tokens."

## Escalation model

Compute expansion should be treated like investment.

For a proposed additional unit of compute ΔC, estimate:

ROI_env = E[discounted attributable environmental benefit from ΔC] / E[environmental cost of ΔC]

Scale where marginal ROI_env is high, subject to safety/resource budgets.

## Initial engineering task

Build a telemetry calculator that:
- records observable API/model/task usage;
- estimates low/mid/high electricity and water ranges;
- estimates carbon under several grid-intensity scenarios;
- attributes avoided compute from caching/skipped duplication;
- records verified environmental benefits from interventions;
- Monte Carlo simulates break-even distributions;
- produces scale-up/reallocation recommendations without claiming false precision.


## Calculator v0.2 implementation

The reference calculator at `scripts/environmental_break_even.py` now supports both direct daily-energy inputs and task/model telemetry:

- tasks per day;
- energy per task;
- model energy multiplier;
- avoided-compute fraction from caching/deduplication;
- initial active-agent count;
- daily agent-count growth;
- benefit scaling elasticity;
- grid carbon intensity;
- cooling-water intensity;
- attribution, evidence-quality, additionality, and durability discounts.

Outputs include:
- p10/median/p90 annual task, energy, carbon, and water bands;
- cumulative 90-day / 1-year / 3-year / 10-year footprint bands;
- carbon payback distribution and horizon probabilities;
- marginal carbon ROI for added compute;
- marginal water-use deltas kept as a separate resource dimension;
- SCALE / HOLD / REALLOCATE signals;
- an explicit non-fungibility warning.

The implementation intentionally does not convert water, materials, biodiversity, and carbon into a single score. Additional resource dimensions should be added as separate vectors when credible telemetry exists.
