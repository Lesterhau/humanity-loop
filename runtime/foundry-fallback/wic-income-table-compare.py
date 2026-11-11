#!/usr/bin/env python3
"""Offline public WIC income-table crosswalk; no scraping or eligibility decisions.

Usage: python wic-income-table-compare.py canonical.json local.json
Both JSON files require `source_url`, `period`, and `rows` (household size ->
periodic income fields). Monetary fields are compared as exact decimal amounts.
"""
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ("hourly", "weekly", "biweekly", "monthly", "annual")


def money(value):
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value).replace("$", "").replace(",", "").strip())
    except InvalidOperation as exc:
        raise ValueError(f"Invalid monetary amount: {value!r}") from exc


def compare(canonical, local):
    if not canonical.get("source_url") or not local.get("source_url"):
        raise ValueError("Both inputs need a source_url")
    if not canonical.get("period") or canonical["period"] != local.get("period"):
        raise ValueError("Matching, nonempty guideline periods are required")
    expected = canonical.get("rows", {})
    observed = local.get("rows", {})
    if not isinstance(expected, dict) or not isinstance(observed, dict):
        raise ValueError("rows must be a household-size-to-values object")
    findings = []
    for size, fields in observed.items():
        if size not in expected:
            findings.append({"size": size, "status": "no_baseline"})
            continue
        for field in FIELDS:
            if field not in fields or field not in expected[size]:
                continue  # Missing data is not proof of disagreement.
            a, b = money(expected[size][field]), money(fields[field])
            if a is not None and b is not None and a != b:
                findings.append({"size": size, "field": field,
                                 "canonical": str(a), "observed": str(b),
                                 "difference": str(b - a), "status": "mismatch"})
    return findings


def self_test():
    baseline = {"source_url": "https://www.michigan.gov/mdhhs/", "period": "2026-27",
                "rows": {"7": {"hourly": "44.50", "weekly": 1781,
                               "biweekly": 3561, "monthly": 7715, "annual": 92574}}}
    county = {"source_url": "https://www.oaklandcountymi.gov/", "period": "2026-27",
              "rows": {"7": {"hourly": "44.55", "weekly": 1781,
                             "biweekly": 3651, "monthly": 7715, "annual": 92574}}}
    result = compare(baseline, county)
    assert [(x["field"], x["difference"]) for x in result] == [
        ("hourly", "0.05"), ("biweekly", "90")], result
    assert compare(baseline, baseline) == []
    try:
        compare(baseline, {**county, "period": "2025-26"})
    except ValueError:
        pass
    else:
        raise AssertionError("Period mismatch must be rejected")
    print("PASS: mismatch, clean-control and year-mismatch assertions")


def main(argv):
    if argv == ["--self-test"]:
        self_test()
        return 0
    if len(argv) != 2:
        print("Usage: wic-income-table-compare.py canonical.json local.json | --self-test", file=sys.stderr)
        return 2
    a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in argv)
    findings = compare(a, b)
    print(json.dumps({"canonical_source": a["source_url"], "local_source": b["source_url"],
                      "period": a["period"], "findings": findings}, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
