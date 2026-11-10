#!/usr/bin/env python3
"""PolicyEngine-US #10512 source-list regression (isolated, stdlib only).

Usage:
  python regression.py                   # candidate source-list; expected PASS
  python regression.py --pre             # original source-list; expected FAIL
  python regression.py path/to/sources.yaml  # actual upstream checkout file

This checks list-based arithmetic and fixture invariants, NOT PolicyEngine
Simulation, tax liability, YAML schema validation, or upstream CI.
"""
from pathlib import Path
import re
import sys
import unittest

ORIGINAL = '''values:
  2021-01-01:
    - ia_net_income
    - ia_pension_exclusion
    - ia_reportable_social_security
  2023-01-01:
    - ia_taxable_income_consolidated
    - taxable_income_deductions
    - qualified_business_income_deduction
'''
FIXED = ORIGINAL.replace('    - qualified_business_income_deduction\n', '')

# Inputs deliberately pin aggregate deductions (already inclusive of QBI).
CASES = [
    ('2024 with QBI', 2024, dict(ia_taxable_income_consolidated=5718.79,
      taxable_income_deductions=17979.70, qualified_business_income_deduction=1429.70), 23698.49),
    ('2024 zero QBI', 2024, dict(ia_taxable_income_consolidated=8000,
      taxable_income_deductions=14600, qualified_business_income_deduction=0), 22600),
    ('2023 with QBI', 2023, dict(ia_taxable_income_consolidated=9000,
      taxable_income_deductions=17000, qualified_business_income_deduction=2000), 26000),
    ('2022 legacy', 2022, dict(ia_net_income=1000,
      ia_pension_exclusion=200, ia_reportable_social_security=300), 1500),
]

def parse_lists(text):
    lists = {}
    year = None
    for line in text.splitlines():
        if line.startswith('metadata:'):
            break
        match = re.fullmatch(r'  (\d{4})-\d{2}-\d{2}:', line)
        if match:
            year = int(match.group(1))
            lists[year] = []
        elif year is not None and re.fullmatch(r'    - [A-Za-z_]+', line):
            lists[year].append(line.strip()[2:])
    return lists

class IowaSourceListTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = parse_lists(TEXT)

    def test_no_duplicate_qbi_2023_plus(self):
        self.assertEqual(self.sources[2023],
            ['ia_taxable_income_consolidated', 'taxable_income_deductions'])

    def test_legacy_source_list_unchanged(self):
        self.assertEqual(self.sources[2021],
            ['ia_net_income', 'ia_pension_exclusion', 'ia_reportable_social_security'])

    def test_four_pinned_arithmetic_scenarios(self):
        for label, year, inputs, expected in CASES:
            with self.subTest(label=label):
                source_year = max(y for y in self.sources if y <= year)
                result = sum(inputs.get(name, 0) for name in self.sources[source_year])
                self.assertAlmostEqual(result, expected, places=2)

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    TEXT = ORIGINAL if arg == '--pre' else (Path(arg).read_text() if arg else FIXED)
    unittest.main(argv=[sys.argv[0]], verbosity=2)
