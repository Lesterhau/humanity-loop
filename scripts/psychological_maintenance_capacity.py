#!/usr/bin/env python3
"""Scenario calculator for stepped psychological-maintenance infrastructure.

This is a planning model, not a clinical cost-effectiveness estimate.
Default costs and participation rates are illustrative assumptions and must be
replaced with local data before policy/implementation decisions.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Tier:
    name: str
    participation_rate: float
    unit_cost_usd: float
    nonspecialist_hours: float
    specialist_hours: float


DEFAULT_SCENARIOS = {
    "low": [
        Tier("tier0_universal_access", 0.10, 0.50, 0.00, 0.00),
        Tier("tier1_selective_guided", 0.02, 10.00, 0.25, 0.00),
        Tier("tier2_task_shared", 0.005, 50.00, 3.00, 0.10),
        Tier("tier3_collaborative_specialist", 0.002, 200.00, 1.50, 2.00),
    ],
    "base": [
        Tier("tier0_universal_access", 0.20, 2.00, 0.00, 0.00),
        Tier("tier1_selective_guided", 0.04, 30.00, 0.50, 0.05),
        Tier("tier2_task_shared", 0.01, 125.00, 4.00, 0.25),
        Tier("tier3_collaborative_specialist", 0.005, 500.00, 2.00, 3.00),
    ],
    "high": [
        Tier("tier0_universal_access", 0.35, 5.00, 0.00, 0.00),
        Tier("tier1_selective_guided", 0.08, 60.00, 0.75, 0.10),
        Tier("tier2_task_shared", 0.025, 250.00, 6.00, 0.50),
        Tier("tier3_collaborative_specialist", 0.01, 1000.00, 3.00, 5.00),
    ],
}


def validate(tiers):
    total = 0.0
    for t in tiers:
        if not 0 <= t.participation_rate <= 1:
            raise ValueError(f"invalid participation rate for {t.name}")
        if min(t.unit_cost_usd, t.nonspecialist_hours, t.specialist_hours) < 0:
            raise ValueError(f"negative input for {t.name}")
        total += t.participation_rate
    if total > 1:
        raise ValueError("tier participation rates sum above 100%; model assumes mutually exclusive annual highest tier")
    return tiers


def model(population, tiers, productive_hours_per_fte=1200.0):
    validate(tiers)
    if population <= 0:
        raise ValueError("population must be positive")
    if productive_hours_per_fte <= 0:
        raise ValueError("productive_hours_per_fte must be positive")

    rows = []
    total_cost = 0.0
    nonspecialist_hours = 0.0
    specialist_hours = 0.0

    for t in tiers:
        participants = population * t.participation_rate
        cost = participants * t.unit_cost_usd
        n_hours = participants * t.nonspecialist_hours
        s_hours = participants * t.specialist_hours
        total_cost += cost
        nonspecialist_hours += n_hours
        specialist_hours += s_hours
        rows.append({
            **asdict(t),
            "participants": participants,
            "annual_cost_usd": cost,
            "annual_nonspecialist_hours": n_hours,
            "annual_specialist_hours": s_hours,
        })

    return {
        "population": population,
        "tiers": rows,
        "annual_cost_usd": total_cost,
        "annual_cost_per_capita_usd": total_cost / population,
        "nonspecialist_fte": nonspecialist_hours / productive_hours_per_fte,
        "specialist_fte": specialist_hours / productive_hours_per_fte,
        "productive_hours_per_fte": productive_hours_per_fte,
        "assumption_warning": (
            "Scenario assumptions only. Unit costs, participation, intensity, wages, "
            "supervision, infrastructure, and local care pathways must be localized."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=float, default=1_000_000)
    parser.add_argument("--scenario", choices=DEFAULT_SCENARIOS, default="base")
    parser.add_argument("--productive-hours-per-fte", type=float, default=1200.0)
    args = parser.parse_args()

    result = model(
        args.population,
        DEFAULT_SCENARIOS[args.scenario],
        args.productive_hours_per_fte,
    )
    result["scenario"] = args.scenario
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
