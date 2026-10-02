#!/usr/bin/env python3
import unittest

from psychological_maintenance_capacity import DEFAULT_SCENARIOS, Tier, model


class PsychologicalMaintenanceCapacityTests(unittest.TestCase):
    def test_base_population_math(self):
        out = model(1_000_000, DEFAULT_SCENARIOS["base"], 1000)
        self.assertEqual(out["population"], 1_000_000)
        self.assertGreater(out["annual_cost_usd"], 0)
        self.assertGreater(out["nonspecialist_fte"], 0)
        self.assertGreater(out["specialist_fte"], 0)

    def test_linear_scaling(self):
        a = model(100_000, DEFAULT_SCENARIOS["base"])
        b = model(1_000_000, DEFAULT_SCENARIOS["base"])
        self.assertAlmostEqual(b["annual_cost_usd"], a["annual_cost_usd"] * 10)
        self.assertAlmostEqual(b["nonspecialist_fte"], a["nonspecialist_fte"] * 10)
        self.assertAlmostEqual(b["specialist_fte"], a["specialist_fte"] * 10)
        self.assertAlmostEqual(b["annual_cost_per_capita_usd"], a["annual_cost_per_capita_usd"])

    def test_invalid_participation_rejected(self):
        with self.assertRaises(ValueError):
            model(1000, [Tier("bad", 1.1, 1, 0, 0)])

    def test_overlapping_rates_rejected(self):
        with self.assertRaises(ValueError):
            model(1000, [
                Tier("a", .7, 1, 0, 0),
                Tier("b", .5, 1, 0, 0),
            ])

    def test_negative_inputs_rejected(self):
        with self.assertRaises(ValueError):
            model(1000, [Tier("bad", .1, -1, 0, 0)])


if __name__ == "__main__":
    unittest.main()
