"""Isolated NH FANF arithmetic regression. NOT a PolicyEngine Simulation test."""
import unittest
import numpy as np

def original(payment_standard, countable_income):
    benefit = max(payment_standard - countable_income, 0)
    return min(benefit, payment_standard)

def candidate(payment_standard, countable_income, minimum_grant=10):
    benefit = max(payment_standard - countable_income, 0)
    capped_benefit = min(benefit, payment_standard)
    rounded_grant = np.floor(np.round(capped_benefit, 2))
    return float(rounded_grant if rounded_grant >= minimum_grant else 0)

class TestNewHampshireFANF(unittest.TestCase):
    def test_arithmetic_cases(self):
        cases = [(1332.5,750,582),(1332.5,1327,0),(1332.5,1322.5,10),
                 (1332.5,1322.51,0),(1332.5,1322.49,10),(1332.5,1332.5,0),
                 (1332.5,1332.51,0),(1332.5,0,1332),(1000,999.99,0),
                 (1000,989.99,10),(1022,637.5,384),(753,400,353)]
        for standard,income,expected in cases:
            with self.subTest(standard=standard,income=income):
                self.assertEqual(candidate(standard,income),expected)
    def test_original_regression_sensitivity(self):
        self.assertEqual(original(1332.5,750),582.5)
        self.assertEqual(original(1332.5,1327),5.5)
        self.assertNotEqual(original(1332.5,750),candidate(1332.5,750))
        self.assertNotEqual(original(1332.5,1327),candidate(1332.5,1327))

if __name__ == "__main__":
    unittest.main(verbosity=2)
