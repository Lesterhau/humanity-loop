#!/usr/bin/env python3
"""Read-only PolicyEngine-US parameter compatibility probe for NH FANF.

Run *only* inside the disposable, pinned upstream CI checkout after overlaying
the review-only proposed NH FANF parameter. No outside APIs or applicant data.
"""
from policyengine_us import CountryTaxBenefitSystem

EXPECTED_EFFECTIVE = "2021-12-17"
HISTORICAL = ("2019-01-01", "2020-01-01", "2021-01-01", "2021-12-16")
RECENT = ("2021-12-17", "2022-01-01", "2025-01-01", "2026-01-01")

system = CountryTaxBenefitSystem()
unavailable = []
for date in HISTORICAL + RECENT:
    try:
        value = system.parameters(date).gov.states.nh.dhhs.fanf.minimum_grant
        print(f"DATE {date}: NH_FANF_MINIMUM={value}")
    except Exception as error:
        # Do not mistake an exception for proof of old legal policy. This is
        # purely a model parameter-access finding, not a benefit determination.
        print(f"DATE {date}: UNAVAILABLE ({type(error).__name__})")
        unavailable.append(date)

print("HISTORICAL_UNAVAILABLE=", ",".join(d for d in HISTORICAL if d in unavailable) or "none")
print("RECENT_UNAVAILABLE=", ",".join(d for d in RECENT if d in unavailable) or "none")
if any(d in unavailable for d in RECENT):
    raise SystemExit("Unexpected current-date parameter failure; cannot call integration safe")
print("Probe does NOT validate laws before", EXPECTED_EFFECTIVE)
