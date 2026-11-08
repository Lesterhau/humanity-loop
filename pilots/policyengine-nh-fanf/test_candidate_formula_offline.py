"""Offline unit tests that execute the real proposed nh_fanf.formula.

The PolicyEngine model API is stubbed only for elementary scalar arithmetic.
Passing is NOT a substitute for PolicyEngine-US integration, vectorized types,
parameter effective dates, historical simulations, or independent policy review.
"""
import importlib.util
import math
from pathlib import Path
import sys
import types
import unittest


api = types.ModuleType("policyengine_us.model_api")
api.Variable = type("Variable", (), {})
api.SPMUnit = type("SPMUnit", (), {})
api.USD = "USD"
api.MONTH = "MONTH"
api.max_ = max
api.min_ = min
api.where = lambda decision, yes, no: yes if decision else no
api.np = types.SimpleNamespace(floor=math.floor)
sys.modules.setdefault("policyengine_us", types.ModuleType("policyengine_us"))
sys.modules["policyengine_us.model_api"] = api

path = Path(__file__).parent / "nh_fanf.py"
spec = importlib.util.spec_from_file_location("_humanity_loop_nh_fanf_candidate", path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def candidate(payment_standard, countable_income):
    variables = {
        "nh_fanf_payment_standard": payment_standard,
        "nh_fanf_countable_income": countable_income,
    }
    return module.nh_fanf.formula(lambda name, period: variables[name], "2025-01", None)


class CandidateActualFormulaTests(unittest.TestCase):
    def test_zero_income(self):
        self.assertEqual(candidate(753, 0), 753)

    def test_partial_whole_dollar(self):
        self.assertEqual(candidate(1022, 400), 622)

    def test_fractional_floor(self):
        self.assertEqual(candidate(1332.5, 750), 582)

    def test_small_grant_disallowed(self):
        self.assertEqual(candidate(1332.5, 1327), 0)

    def test_exact_threshold(self):
        self.assertEqual(candidate(1332.5, 1322.5), 10)

    def test_fractional_at_threshold(self):
        self.assertEqual(candidate(110.99, 100), 10)

    def test_below_threshold(self):
        self.assertEqual(candidate(109.99, 100), 0)

    def test_above_payment_standard(self):
        self.assertEqual(candidate(753, 800), 0)

    def test_fractional_non_nearest_round(self):
        self.assertEqual(candidate(10.99, 0), 10)

    def test_no_negative_grant(self):
        self.assertEqual(candidate(5, 100), 0)


if __name__ == "__main__":
    unittest.main()
