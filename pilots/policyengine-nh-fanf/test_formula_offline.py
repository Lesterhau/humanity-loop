"""Pure offline arithmetic tests; NOT a PolicyEngine integration run."""
from decimal import Decimal, ROUND_FLOOR
import unittest


def grant(payment_standard, income, eligible=True):
    if not eligible:
        return Decimal(0)
    standard = Decimal(str(payment_standard))
    value = min(max(standard - Decimal(str(income)), Decimal(0)), standard)
    rounded = value.to_integral_value(rounding=ROUND_FLOOR)
    return rounded if rounded >= 10 else Decimal(0)


class FANFRuleTests(unittest.TestCase):
    def test_fractional(self): self.assertEqual(grant('1332.50', 750), 582)
    def test_under_ten(self): self.assertEqual(grant('1332.50', 1327), 0)
    def test_exact_ten(self): self.assertEqual(grant('1332.50', '1322.50'), 10)
    def test_just_over_ten(self): self.assertEqual(grant('110.99', 100), 10)
    def test_just_under_ten(self): self.assertEqual(grant('109.99', 100), 0)
    def test_zero(self): self.assertEqual(grant(753, 753), 0)
    def test_negative(self): self.assertEqual(grant(753, 800), 0)
    def test_whole_dollar(self): self.assertEqual(grant(1022, 400), 622)
    def test_defensive_negative_income_cannot_exceed_standard(self): self.assertEqual(grant('100.99', -50), 100)
    def test_ineligible(self): self.assertEqual(grant(1022, 0, False), 0)
    def test_below_round_threshold(self): self.assertEqual(grant('19.999', 10), 0)
    def test_above_round_threshold(self): self.assertEqual(grant('20.000', 10), 10)
    def test_no_nearest_dollar_round(self): self.assertEqual(grant('10.99', 0), 10)


if __name__ == '__main__':
    unittest.main()
