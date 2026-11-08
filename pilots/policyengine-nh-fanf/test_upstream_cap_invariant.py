"""Offline candidate regression for PolicyEngine-US's existing benefit cap.

No PolicyEngine package or eligibility pipeline is invoked. A negative
countable-income value is a synthetic defensive stress test, NOT evidence
that real New Hampshire FANF households have negative countable income.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest

import numpy as np


class PreserveUpstreamCap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api = types.ModuleType("policyengine_us.model_api")
        api.Variable = type("Variable", (), {})
        api.SPMUnit = type("SPMUnit", (), {})
        api.USD = "USD"
        api.MONTH = "MONTH"
        api.max_ = np.maximum
        api.min_ = np.minimum
        api.where = np.where
        api.np = np
        api.__all__ = ["Variable", "SPMUnit", "USD", "MONTH", "max_", "min_", "where", "np"]
        pkg = types.ModuleType("policyengine_us")
        pkg.__path__ = []
        before = {key: sys.modules.get(key) for key in ("policyengine_us", "policyengine_us.model_api")}
        try:
            sys.modules["policyengine_us"] = pkg
            sys.modules["policyengine_us.model_api"] = api
            path = Path(__file__).resolve().parent / "nh_fanf.py"
            spec = importlib.util.spec_from_file_location("_candidate_cap_test", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cls.formula = staticmethod(mod.nh_fanf.formula)
        finally:
            for key, prior in before.items():
                if prior is None:
                    sys.modules.pop(key, None)
                else:
                    sys.modules[key] = prior

    def calculate(self, standard, income):
        return self.formula(lambda name, period: {"nh_fanf_payment_standard": standard,
                                                 "nh_fanf_countable_income": income}[name],
                            "2025-01", None)

    def test_negative_income_cannot_exceed_payment_standard(self):
        self.assertEqual(float(self.calculate(100.99, -50)), 100.0)

    def test_normal_fractional_case_preserved(self):
        self.assertEqual(float(self.calculate(1332.5, 750)), 582.0)

    def test_vector_mixed_input_cap_and_threshold(self):
        result = self.calculate(np.array([100.99, 1332.5, 110.99, 109.99]),
                                np.array([-50, 750, 100, 100]))
        np.testing.assert_array_equal(result, [100, 582, 10, 0])

    def test_zero_standard_cannot_pay(self):
        self.assertEqual(float(self.calculate(0, -20)), 0.0)


if __name__ == "__main__":
    unittest.main()
