#!/usr/bin/env python3
"""Deterministic verification tests for environmental_break_even.py."""
import unittest

from environmental_break_even import HORIZONS, marginal_carbon_roi, recommendation, simulate


def fixed_cfg(daily_kwh=5.0, kg_per_kwh=1.0, daily_benefit=20.0, initial_debt=150.0):
    return {
        "daily_kwh": daily_kwh,
        "kg_co2e_per_kwh": kg_per_kwh,
        "liters_water_per_kwh": 0.0,
        "daily_gross_carbon_benefit_kg": daily_benefit,
        "benefit_scale_elasticity": 1.0,
        "attribution": 1.0,
        "evidence_quality": 1.0,
        "additionality": 1.0,
        "durability": 1.0,
        "initial_carbon_debt_kg": initial_debt,
    }


class BreakEvenTests(unittest.TestCase):
    def test_known_payback_is_exactly_ten_days(self):
        out = simulate(fixed_cfg(), n=32, seed=7)
        self.assertEqual(out["median_payback_days"], 10.0)
        self.assertEqual(out["never_payback_probability"], 0.0)
        for horizon in HORIZONS:
            self.assertEqual(out["payback_probability"][horizon], 1.0)

    def test_never_payback_when_benefit_below_cost(self):
        out = simulate(fixed_cfg(daily_kwh=5.0, kg_per_kwh=1.0, daily_benefit=4.0), n=32, seed=7)
        self.assertIsNone(out["median_payback_days"])
        self.assertEqual(out["never_payback_probability"], 1.0)
        for horizon in HORIZONS:
            self.assertEqual(out["payback_probability"][horizon], 0.0)

    def test_task_model_usage_and_agent_growth_are_supported(self):
        cfg = fixed_cfg(daily_kwh=1.0)
        cfg.pop("daily_kwh")
        cfg["task_usage"] = {
            "tasks_per_day": 100,
            "kwh_per_task": 0.01,
            "model_energy_multiplier": 1.2,
            "avoided_compute_fraction": 0.25,
        }
        cfg["agent_growth"] = {"initial_agents": 2, "daily_rate": 0.001}
        out = simulate(cfg, n=16, seed=3)
        self.assertGreater(out["annual_task_volume"]["median"], 0)
        self.assertGreater(out["annual_energy_kwh"]["median"], 0)
        self.assertIn("10y", out["cumulative_footprint"])
        self.assertIn("water_use_liters", out["cumulative_footprint"]["1y"])

    def test_non_fungibility_is_explicit(self):
        out = simulate(fixed_cfg(), n=8, seed=1)
        self.assertIn("separate decision dimensions", out["non_fungibility_note"])

    def test_marginal_roi_and_recommendation_thresholds(self):
        def result(p, cost=100.0, benefit=100.0):
            return {
                "payback_probability": {"1y": p},
                "annual_carbon_cost_kg": {"median": cost},
                "annual_attributable_carbon_benefit_kg": {"median": benefit},
            }
        base = result(0.50, 100, 100)
        scale = result(0.60, 110, 125)
        hold = result(0.50, 110, 109)
        reallocate = result(0.40, 120, 105)
        self.assertGreater(marginal_carbon_roi(base, scale), 1.0)
        self.assertEqual(recommendation(base, scale), "SCALE")
        self.assertEqual(recommendation(base, hold), "HOLD")
        self.assertEqual(recommendation(base, reallocate), "REALLOCATE")


if __name__ == "__main__":
    unittest.main()
