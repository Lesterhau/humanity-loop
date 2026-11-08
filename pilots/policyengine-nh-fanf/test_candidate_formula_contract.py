"""Offline import-level contract tests of the actual NH FANF candidate formula.

Runs without policyengine-us by stubbing only model_api names. This is NOT a
PolicyEngine integration test: its registry, `defined_for` gating, effective
parameter dates, and downstream calculations are not exercised.

Usage: python -m unittest -v test_candidate_formula_contract.py
Requires numpy and PyYAML, no network or model calls.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent


def load_candidate():
    # The production module uses `from policyengine_us.model_api import *`.
    # Keep the stub explicit so an unrelated installed package cannot change
    # what this narrowly scoped offline test actually exercises.
    model_api = types.ModuleType("policyengine_us.model_api")
    model_api.__all__ = ["Variable", "SPMUnit", "USD", "MONTH", "max_", "min_", "where", "np"]
    model_api.Variable = type("Variable", (), {})
    model_api.SPMUnit = type("SPMUnit", (), {})
    model_api.USD = "USD"
    model_api.MONTH = "MONTH"
    model_api.max_ = np.maximum
    model_api.min_ = np.minimum
    model_api.where = np.where
    model_api.np = np
    pkg = types.ModuleType("policyengine_us")
    pkg.__path__ = []
    old_pkg = sys.modules.get("policyengine_us")
    old_api = sys.modules.get("policyengine_us.model_api")
    try:
        sys.modules["policyengine_us"] = pkg
        sys.modules["policyengine_us.model_api"] = model_api
        spec = importlib.util.spec_from_file_location("nh_fanf_candidate_under_test", ROOT / "nh_fanf.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.nh_fanf
    finally:
        for key, old in (("policyengine_us", old_pkg), ("policyengine_us.model_api", old_api)):
            if old is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = old


class CandidateFormulaContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = load_candidate()

    def compute(self, standard, income, minimum_grant=10):
        def spm_unit(variable, period):
            return {"nh_fanf_payment_standard": standard,
                    "nh_fanf_countable_income": income}[variable]
                parameters = lambda period: types.SimpleNamespace(
            gov=types.SimpleNamespace(states=types.SimpleNamespace(
                nh=types.SimpleNamespace(dhhs=types.SimpleNamespace(
                    fanf=types.SimpleNamespace(minimum_grant=minimum_grant)
                ))
            ))
        )
        return self.candidate.formula(spm_unit, "2025-01", parameters)

    def test_dated_minimum_parameter_yaml(self):
        parameter_file = ROOT / "policyengine_us/parameters/gov/states/nh/dhhs/fanf/minimum_grant.yaml"
        data = yaml.safe_load(parameter_file.read_text(encoding="utf-8"))
        self.assertEqual(next(v for k, v in data["values"].items() if str(k) == "2021-12-17"), 10)
        self.assertEqual(data["metadata"]["unit"], "currency-USD")

    def test_vectorized_override_proves_parameter_used(self):
        np.testing.assert_array_equal(self.compute(
            np.array([14.99, 15.99]), np.array([0, 0]), minimum_grant=15
        ), [0, 15])

    def test_six_eligible_yaml_fixtures_call_real_candidate(self):
        fixtures = yaml.safe_load((ROOT / "nh_fanf.yaml").read_text(encoding="utf-8"))
        self.assertEqual(len(fixtures), 7)
        checked = 0
        for case in fixtures:
            # Ineligibility is enforced by PolicyEngine's `defined_for` engine,
            # NOT by the formula. Do not pretend the stub tests that contract.
            if not case["input"]["nh_fanf_eligible"]:
                continue
            with self.subTest(case=case["name"]):
                self.assertEqual(float(self.compute(
                    case["input"]["nh_fanf_payment_standard"],
                    case["input"]["nh_fanf_countable_income"])),
                    float(case["output"]["nh_fanf"]))
                checked += 1
        self.assertEqual(checked, 6)

    def test_vectorized_monthly_grants_and_exact_boundary(self):
        standard = np.array([1332.5, 1332.5, 1332.5, 110.99, 109.99, 753.0, 753.0])
        income = np.array([750.0, 1327.0, 1322.5, 100.0, 100.0, 753.0, 800.0])
        actual = self.compute(standard, income)
        np.testing.assert_array_equal(actual, [582, 0, 10, 10, 0, 0, 0])

    def test_do_not_round_payment_standard_first(self):
        self.assertEqual(float(self.compute(1332.50, 750)), 582.0)
        self.assertEqual(float(self.compute(1332.50, 1322.50)), 10.0)

    def test_fractional_near_ten_boundary(self):
        self.assertEqual(float(self.compute(110.00, 100.01)), 0.0)
        self.assertEqual(float(self.compute(110.00, 100.00)), 10.0)
        self.assertEqual(float(self.compute(110.99, 100.00)), 10.0)

    def test_current_upstream_formula_differs_on_reported_cases(self):
        # The current upstream formula (read from its public main branch) is
        # min_(max_(payment_standard - countable_income, 0), payment_standard).
        # Reproducing its arithmetic here is NOT executing upstream's package.
        def upstream(standard, income):
            return np.minimum(np.maximum(standard - income, 0), standard)
        self.assertEqual(float(upstream(1332.50, 750.00)), 582.50)
        self.assertEqual(float(self.compute(1332.50, 750.00)), 582.00)
        self.assertEqual(float(upstream(1332.50, 1327.00)), 5.50)
        self.assertEqual(float(self.compute(1332.50, 1327.00)), 0.00)

    def test_metadata_keeps_declarative_eligibility_gate(self):
        self.assertEqual(self.candidate.defined_for, "nh_fanf_eligible")
        self.assertEqual(self.candidate.definition_period, "MONTH")


if __name__ == "__main__":
    unittest.main()
