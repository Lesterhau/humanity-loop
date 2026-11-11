"""Review-only NH FANF arithmetic precision challenge, not a PolicyEngine integration.

Primary rule: https://gc.nh.gov/rules/state_agencies/he-w600.html
Upstream issue: https://github.com/PolicyEngine/policyengine-us/issues/10517
No real household data or benefit determinations.
"""
from decimal import Decimal, ROUND_FLOOR
import numpy as np

SEED = 20261111
N = 100_000


def compute(standard, income, strategy):
    cap = np.minimum(np.maximum(standard - income, 0), standard)
    if strategy == "direct":
        whole = np.floor(cap)
    elif strategy == "cents":
        whole = np.floor(np.round(cap, 2))
    elif strategy == "precision9":
        whole = np.floor(np.round(cap, 9))
    else:
        raise ValueError(strategy)
    return np.where(whole >= 10, whole, 0)


def exact_decimal(standard, income):
    a, b = Decimal(str(standard)), Decimal(str(income))
    cap = min(max(a - b, Decimal(0)), a)
    whole = cap.to_integral_value(rounding=ROUND_FLOOR)
    return int(whole) if whole >= 10 else 0


def run():
    examples = [
        (1129.61, 211.61, 918),
        (2453.66, 1048.66, 1405),
        (2067.47, 1318.47, 749),
        (1332.5, 750, 582),
        (1332.5, 1327, 0),
        (1332.5, 1322.5, 10),
        (20, 10.001, 0),
        (21, 10.001, 10),
        (100.99, -50, 100),
        (1000, 999.99, 0),
    ]
    for standard, income, expected in examples:
        assert exact_decimal(standard, income) == expected
        assert int(compute(standard, income, "precision9")) == expected
    assert int(compute(1129.61, 211.61, "direct")) == 917
    assert int(compute(20, 10.001, "cents")) == 10
    print("Ten hand-selected cases: provisional precision9 candidate 10/10 match Decimal oracle")

    rng = np.random.default_rng(SEED)
    for places in (2, 3, 4):
        scale = 10 ** places
        standards_i = rng.integers(scale, 3000 * scale, size=N, dtype=np.int64)
        incomes_i = rng.integers(0, 3000 * scale, size=N, dtype=np.int64)
        incomes_i[:500] = -rng.integers(scale, 1000 * scale, size=500)
        standards = standards_i / scale
        incomes = incomes_i / scale
        exact_cap_i = np.minimum(np.maximum(standards_i - incomes_i, 0), standards_i)
        exact_whole = exact_cap_i // scale
        expected = np.where(exact_whole >= 10, exact_whole, 0)
        mismatches = {}
        for strategy in ("direct", "cents", "precision9"):
            actual = compute(standards, incomes, strategy)
            mismatches[strategy] = int(np.count_nonzero(actual != expected))
        assert mismatches["precision9"] == 0, mismatches
        print(f"{places}-decimal synthetic inputs, n={N}: mismatches vs integer oracle {mismatches}")

    print("PASS: 300,000 deterministic synthetic comparisons; not proof of all valid inputs")


if __name__ == "__main__":
    run()
