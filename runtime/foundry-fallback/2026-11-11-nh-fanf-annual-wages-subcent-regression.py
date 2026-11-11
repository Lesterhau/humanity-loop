"""Standalone, source-shaped NH FANF arithmetic review (NOT PolicyEngine Simulation).

Sources:
https://github.com/PolicyEngine/policyengine-us/issues/10517
https://github.com/PolicyEngine/policyengine-us/blob/main/policyengine_us/variables/gov/states/nh/dhhs/fanf/income/nh_fanf_countable_earned_income.py
https://gc.nh.gov/rules/state_agencies/he-w600.html
No personal data or actual benefits decisions.
"""
from decimal import Decimal, ROUND_FLOOR
from math import floor


def hypothetical(annual_wages: str, payment_standard: str):
    annual = Decimal(annual_wages)
    standard = Decimal(payment_standard)
    monthly = annual / Decimal(12)
    eligible_countable = monthly * Decimal("0.8")
    benefit_countable = monthly * Decimal("0.5")
    raw = max(Decimal(0), min(standard - benefit_countable, standard))
    exact_whole = int(raw.to_integral_value(rounding=ROUND_FLOOR))
    exact = exact_whole if exact_whole >= 10 else 0
    float_raw = float(standard) - float(annual) / 12 * 0.5
    cents_candidate = floor(round(float_raw, 2))
    direct_candidate = floor(float_raw)
    return eligible_countable, raw, exact, cents_candidate, direct_candidate


def main():
    eligibility, raw, exact, cents, direct = hypothetical("12000.10", "1022")
    assert eligibility < Decimal(1022)
    assert Decimal(521) < raw < Decimal(522)
    assert (exact, cents, direct) == (521, 522, 521)
    print("2024 hypothetical annual wages $12,000.10:")
    print(f"  eligibility countable ~{eligibility}")
    print(f"  unrounded benefit ~{raw}")
    print(f"  Decimal floor={exact}, prior cents candidate={cents}, direct float floor={direct}")

    _, raw2, exact2, cents2, direct2 = hypothetical("12000.00", "1022")
    assert raw2 == Decimal(522)
    assert (exact2, cents2, direct2) == (522, 522, 522)
    print("Even-dollar annual wages control: PASS")

    assert Decimal("1129.61") - Decimal("211.61") == Decimal(918)
    assert floor(1129.61 - 211.61) == 917
    print("Independent exact-integer binary-float underfloor case: reproduced")
    print("PASS: isolated arithmetic only; full engine conversion not verified")


if __name__ == "__main__":
    main()
