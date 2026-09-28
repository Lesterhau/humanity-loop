#!/usr/bin/env python3
"""Deterministic verification tests for environmental_break_even.py."""
import math
import unittest
from unittest.mock import patch

from environmental_break_even import HORIZONS, recommendation, simulate


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

    def test_recommendation_thresholds(self):
        def result(p):
            return {"payback_probability": {"1y": p}}
        base = result(0.50)
        self.assertEqual(recommendation(base, result(0.60)), "SCALE")
        self.assertEqual(recommendation(base, result(0.50)), "HOLD")
        self.assertEqual(recommendation(base, result(0.40)), "REALLOCATE")


if __name__ == "__main__":
    unittest.main()
