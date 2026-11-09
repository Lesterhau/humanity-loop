"""Dependency-free source-list regression for PolicyEngine-US issue #9952.

Run from PolicyEngine-US repository root:
  python /path/to/2026-11-09-policyengine-taxsim-tfica-regression.test.py
Or set TAXSIM_TFICA_SOURCE to the absolute source-file path.

This does NOT execute PolicyEngine's Simulation engine or NBER TAXSIM.
"""

import ast
import os
from pathlib import Path
import unittest

SOURCE = Path(os.environ.get(
    "TAXSIM_TFICA_SOURCE",
    "policyengine_us/variables/contrib/taxsim/taxsim_tfica.py",
))
FEDERAL_COMPONENTS = (
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
)


def source_adds(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "taxsim_tfica":
            for statement in node.body:
                if isinstance(statement, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "adds"
                    for target in statement.targets
                ):
                    return tuple(ast.literal_eval(statement.value))
    raise AssertionError("taxsim_tfica.adds not found")


def source_sum(components, values):
    return round(sum(values.get(component, 0) for component in components), 2)


class FederalOnlyTFICATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adds = source_adds(SOURCE)

    def test_only_employee_federal_and_self_employment_components(self):
        self.assertEqual(self.adds, FEDERAL_COMPONENTS)
        self.assertNotIn("employee_payroll_tax", self.adds)
        self.assertNotIn("employee_state_payroll_tax", self.adds)
        self.assertNotIn("employer_social_security_tax", self.adds)

    def test_california_60000_wages_no_state_sdi(self):
        values = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 0, 0)))
        values.update(employee_payroll_tax=5370, employee_state_payroll_tax=780)
        self.assertEqual(source_sum(self.adds, values), 4590)

    def test_new_york_60000_wages_no_state_premiums(self):
        values = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 0, 0)))
        values.update(employee_payroll_tax=4880.40, employee_state_payroll_tax=290.40)
        self.assertEqual(source_sum(self.adds, values), 4590)

    def test_texas_60000_wages_unchanged(self):
        values = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 0, 0)))
        values.update(employee_payroll_tax=4590, employee_state_payroll_tax=0)
        self.assertEqual(source_sum(self.adds, values), 4590)

    def test_self_employment_tax_remains_included(self):
        values = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 0, 1530)))
        values.update(employee_payroll_tax=4590, employee_state_payroll_tax=0)
        self.assertEqual(source_sum(self.adds, values), 6120)

    def test_additional_medicare_tax_remains_included(self):
        values = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 90, 0)))
        values.update(employee_payroll_tax=4590, employee_state_payroll_tax=0)
        self.assertEqual(source_sum(self.adds, values), 4680)

    def test_state_premium_changes_do_not_change_federal_output(self):
        base = dict(zip(FEDERAL_COMPONENTS, (3720, 870, 0, 0)))
        values_a = dict(base, employee_payroll_tax=4590, employee_state_payroll_tax=0)
        values_b = dict(base, employee_payroll_tax=5790, employee_state_payroll_tax=1200)
        self.assertEqual(source_sum(self.adds, values_a), source_sum(self.adds, values_b))


if __name__ == "__main__":
    unittest.main()
