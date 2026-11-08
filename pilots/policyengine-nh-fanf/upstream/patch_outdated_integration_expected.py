#!/usr/bin/env python3
"""Narrow, audited compatibility edit of two obsolete NH FANF test expectations.

This edits only a disposable copy of PolicyEngine-US's integration.yaml in CI.
The original upstream repository is never written to or pushed.
Reference: PolicyEngine-US issue #10517, Cases 16 and 20 of #10251.
"""
from pathlib import Path
import sys


EXPECTED = {
    "Case 16": (
        "    # 1,332.50 - 750 = 582.50\n    nh_fanf: 582.50",
        "    # 1,332.50 - 750 = 582.50, rounded down under He-W 670.03(b)(3)\n    nh_fanf: 582",
    ),
    "Case 20": (
        "    # 1,022 - 637.50 = 384.50\n    nh_fanf: 384.50",
        "    # 1,022 - 637.50 = 384.50, rounded down under He-W 670.03(b)(3)\n    nh_fanf: 384",
    ),
}


def patch(content: str) -> str:
    for case, (old, new) in EXPECTED.items():
        if content.count(old) != 1 or content.count(new) != 0:
            raise ValueError(f"{case}: upstream test fixture changed; STOP, inspect manually")
        content = content.replace(old, new, 1)
    if content.count("nh_fanf: 582\n") != 1 or content.count("nh_fanf: 384\n") != 1:
        raise ValueError("unexpected grant fixture output after patch")
    return content


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: patch_outdated_integration_expected.py <isolated-upstream-integration.yaml>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    original = path.read_text(encoding="utf-8")
    updated = patch(original)
    path.write_text(updated, encoding="utf-8")
    print("Patched exactly two obsolete NH FANF expected grant outputs (Cases 16, 20).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
