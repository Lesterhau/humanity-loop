#!/usr/bin/env python3
"""Offline, source-stamped QA of selected ACMAD May 2026 CDI percentage rows.

Fixtures transcribed from two official HTML tables on 2026-11-11 UTC.
No live fetch, raster inspection, or corrected-coverage calculation.
"""
from decimal import Decimal

SOURCES = {
    "2026-04-dekad11": {
        "url": "https://ada.acmad.org/api/main/bulletins/africa-drought-bulletin-may/",
        "rows": {
            "Madagascar": ("128.2", "87.7", "17.6"),
            "Sao Tome and Principe": ("589.1", "0.0", "0.0"),
            "Angola": ("52.7", "11.4", "11.2"),
        },
    },
    "2026-04-dekad21": {
        "url": "https://ada.acmad.org/api/main/bulletins/africadrought-bulletin/",
        "rows": {
            "Madagascar": ("131.9", "125.9", "0.0"),
            "Côte d'Ivoire": ("3.5", "17.4", "0.0"),
            "Senegal": ("15.7", "0.0", "0.0"),
        },
    },
}

CATEGORIES = ("Watch", "Warning", "Alert")
ROUNDING_ALLOWANCE = Decimal("0.15")  # 3 x 0.05 percentage points


def check_row(values):
    numbers = tuple(Decimal(x) for x in values)
    findings = []
    for name, value in zip(CATEGORIES, numbers):
        if value < 0 or value > 100:
            findings.append(f"{name} outside [0,100]: {value}%")
    total = sum(numbers)
    if total > Decimal(100) + ROUNDING_ALLOWANCE:
        findings.append(f"Watch+Warning+Alert = {total}% (>100% plus rounding tolerance)")
    return findings


def run_checks():
    return {
        period: {country: check_row(values) for country, values in source["rows"].items()}
        for period, source in SOURCES.items()
    }


def test_expected_findings():
    report = run_checks()
    assert len(report["2026-04-dekad11"]["Madagascar"]) == 2
    assert len(report["2026-04-dekad11"]["Sao Tome and Principe"]) == 2
    assert len(report["2026-04-dekad21"]["Madagascar"]) == 3
    assert report["2026-04-dekad11"]["Angola"] == []
    assert report["2026-04-dekad21"]["Côte d'Ivoire"] == []
    assert report["2026-04-dekad21"]["Senegal"] == []
    assert check_row(("33.3", "33.3", "33.4")) == []
    assert check_row(("33.35", "33.35", "33.35")) == []
    assert check_row(("-0.1", "1.0", "0.0"))
    return report


if __name__ == "__main__":
    report = test_expected_findings()
    for period, rows in report.items():
        print(f"{period} | {SOURCES[period]['url']}")
        for country, findings in rows.items():
            print(f"  {country}: " + ("; ".join(findings) if findings else "PASS (selected row only)"))
    print("9/9 offline assertions PASS; original raster/methodology NOT verified")
