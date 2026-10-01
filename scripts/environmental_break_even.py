#!/usr/bin/env python3
"""Humanity Loop environmental break-even calculator.

Decision-support simulation. Carbon, water, materials, and ecosystem effects remain
separate; this module does not manufacture a single "green score".
"""
from __future__ import annotations
import argparse, json, math, random, statistics
from pathlib import Path

HORIZONS = {"90d": 90, "1y": 365, "3y": 1095, "10y": 3650}


def triangular(rng, spec):
    if isinstance(spec, (int, float)):
        return float(spec)
    return rng.triangular(
        float(spec["low"]),
        float(spec["high"]),
        float(spec.get("mode", spec.get("mid", (spec["low"] + spec["high"]) / 2))),
    )


def q(xs, p):
    ys = sorted(xs)
    return ys[min(len(ys) - 1, max(0, int(p * (len(ys) - 1))))]


def band(xs):
    return {"p10": q(xs, .1), "median": q(xs, .5), "p90": q(xs, .9)}


def finite_median(xs):
    ys = [x for x in xs if math.isfinite(x)]
    return statistics.median(ys) if ys else None


def geom_sum(rate, days):
    if days <= 0:
        return 0.0
    if abs(rate) < 1e-12:
        return float(days)
    return ((1.0 + rate) ** days - 1.0) / rate


def sampled_usage(cfg, rng, scale):
    """Return baseline daily tasks and kWh plus an agent-growth rate.

    Backwards compatible: configs may still provide daily_kwh directly.
    """
    task_cfg = cfg.get("task_usage")
    growth_cfg = cfg.get("agent_growth", {})
    growth = triangular(rng, growth_cfg.get("daily_rate", 0.0))

    if task_cfg:
        tasks = triangular(rng, task_cfg["tasks_per_day"])
        kwh_per_task = triangular(rng, task_cfg["kwh_per_task"])
        model_multiplier = triangular(rng, task_cfg.get("model_energy_multiplier", 1.0))
        initial_agents = triangular(rng, growth_cfg.get("initial_agents", 1.0))
        avoided = triangular(rng, task_cfg.get("avoided_compute_fraction", 0.0))
        avoided = min(max(avoided, 0.0), 0.99)
        daily_kwh = tasks * kwh_per_task * model_multiplier * initial_agents * scale * (1.0 - avoided)
        daily_tasks = tasks * initial_agents * scale
    else:
        daily_kwh = triangular(rng, cfg["daily_kwh"]) * scale
        daily_tasks = triangular(rng, cfg.get("tasks_per_day", 0.0)) * scale

    return daily_tasks, daily_kwh, growth


def first_payback_day(initial_debt, daily_cost, cost_growth, daily_benefit, benefit_growth, max_days=3650):
    for day in range(1, max_days + 1):
        cost = initial_debt + daily_cost * geom_sum(cost_growth, day)
        benefit = daily_benefit * geom_sum(benefit_growth, day)
        if benefit >= cost:
            return float(day)
    return math.inf


def simulate(cfg, n=10000, seed=1, scale=1.0):
    rng = random.Random(seed)
    paybacks = []
    annual_tasks = []
    annual_kwh = []
    carbon_costs = []
    carbon_benefits = []
    water_costs = []
    cumulative = {
        h: {"carbon_cost_kg": [], "carbon_benefit_kg": [], "water_use_liters": [], "energy_kwh": []}
        for h in HORIZONS
    }

    for _ in range(n):
        daily_tasks, daily_kwh, agent_growth = sampled_usage(cfg, rng, scale)
        kg_per_kwh = triangular(rng, cfg["kg_co2e_per_kwh"])
        liters_per_kwh = triangular(rng, cfg["liters_water_per_kwh"])
        initial_debt = triangular(rng, cfg.get("initial_carbon_debt_kg", 0.0))

        daily_gross = triangular(rng, cfg["daily_gross_carbon_benefit_kg"])
        daily_gross *= scale ** triangular(rng, cfg.get("benefit_scale_elasticity", 1.0))

        discount = 1.0
        for key in ("attribution", "evidence_quality", "additionality", "durability"):
            discount *= triangular(rng, cfg[key])
        daily_benefit = daily_gross * discount

        benefit_agent_elasticity = triangular(rng, cfg.get("benefit_agent_elasticity", 1.0))
        benefit_growth = (1.0 + agent_growth) ** benefit_agent_elasticity - 1.0

        annual_energy = daily_kwh * geom_sum(agent_growth, 365)
        annual_tasks_count = daily_tasks * geom_sum(agent_growth, 365)
        annual_carbon_cost = initial_debt + annual_energy * kg_per_kwh
        annual_carbon_benefit = daily_benefit * geom_sum(benefit_growth, 365)
        annual_water = annual_energy * liters_per_kwh

        annual_tasks.append(annual_tasks_count)
        annual_kwh.append(annual_energy)
        carbon_costs.append(annual_carbon_cost)
        carbon_benefits.append(annual_carbon_benefit)
        water_costs.append(annual_water)

        paybacks.append(
            first_payback_day(
                initial_debt,
                daily_kwh * kg_per_kwh,
                agent_growth,
                daily_benefit,
                benefit_growth,
            )
        )

        for h, days in HORIZONS.items():
            energy = daily_kwh * geom_sum(agent_growth, days)
            cumulative[h]["energy_kwh"].append(energy)
            cumulative[h]["carbon_cost_kg"].append(initial_debt + energy * kg_per_kwh)
            cumulative[h]["water_use_liters"].append(energy * liters_per_kwh)
            cumulative[h]["carbon_benefit_kg"].append(daily_benefit * geom_sum(benefit_growth, days))

    return {
        "scale": scale,
        "uncertainty": "Monte Carlo p10/median/p90; input ranges are sampled independently unless encoded otherwise.",
        "annual_task_volume": band(annual_tasks),
        "annual_energy_kwh": band(annual_kwh),
        "annual_carbon_cost_kg": band(carbon_costs),
        "annual_attributable_carbon_benefit_kg": band(carbon_benefits),
        "annual_water_use_liters": band(water_costs),
        "cumulative_footprint": {
            h: {metric: band(values) for metric, values in metrics.items()}
            for h, metrics in cumulative.items()
        },
        "payback_probability": {h: sum(x <= d for x in paybacks) / n for h, d in HORIZONS.items()},
        "never_payback_probability": sum(math.isinf(x) for x in paybacks) / n,
        "median_payback_days": finite_median(paybacks),
        "non_fungibility_note": (
            "Carbon, water, materials, and biodiversity are separate decision dimensions. "
            "No cross-resource conversion is implied by this calculator."
        ),
    }


def marginal_carbon_roi(base, expanded):
    benefit_delta = (
        expanded["annual_attributable_carbon_benefit_kg"]["median"]
        - base["annual_attributable_carbon_benefit_kg"]["median"]
    )
    cost_delta = expanded["annual_carbon_cost_kg"]["median"] - base["annual_carbon_cost_kg"]["median"]
    if cost_delta <= 0:
        return math.inf if benefit_delta > 0 else 0.0
    return benefit_delta / cost_delta


def recommendation(base, expanded):
    b = base["payback_probability"]["1y"]
    e = expanded["payback_probability"]["1y"]
    roi = marginal_carbon_roi(base, expanded)

    if e >= max(.6, b + .05) and roi > 1.0:
        return "SCALE"
    if e < b - .05 or roi < 0.8:
        return "REALLOCATE"
    return "HOLD"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", type=Path)
    ap.add_argument("--samples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text())

    runs = {str(s): simulate(cfg, args.samples, args.seed, s) for s in (1.0, 1.1, 1.5, 2.0)}
    base = runs["1.0"]
    for s in ("1.1", "1.5", "2.0"):
        runs[s]["marginal_carbon_roi_vs_base"] = marginal_carbon_roi(base, runs[s])
        runs[s]["marginal_water_delta_liters_vs_base"] = (
            runs[s]["annual_water_use_liters"]["median"] - base["annual_water_use_liters"]["median"]
        )
        runs[s]["recommendation_vs_base"] = recommendation(base, runs[s])

    print(json.dumps({"model": "HL environmental break-even v0.2", "runs": runs}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
