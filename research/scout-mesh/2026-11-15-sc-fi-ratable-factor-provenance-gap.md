# South Carolina Family Independence: current ratable-factor provenance check (2026-11-15 UTC)

Status: READ-ONLY PUBLIC-SOURCE RESEARCH; not an agency correction, benefit determination, or upstream code submission.

## Official-source evidence

1. South Carolina regulation 114-1140(A)(3) says the Department of Social Services sets the FI ratable reduction **annually** based on appropriations and expected caseload, may adjust it within the fiscal year, and makes the need standard, payment standard, and ratable reduction available at its Columbia state office. This means the percentage cannot be inferred as a permanently fixed statutory constant. Official regulations: https://www.scstatehouse.gov/coderegs/Chapter%20114.pdf (section 114-1140).
2. Regulation 114-1140(A)(4)-(7) requires whole-dollar rounding down and no payment below $10 before adjustments, while preserving recipient status and excluding zero-payment months from the time limit. Section 114-1150(E) prescribes (need standard minus countable income) times the ratable reduction. Same official regulations.
3. A historical DSS-hosted Family Independence manual (Volume 41) describes the same deficit-times-percentage-of-need calculation, with a supplemental-payment caveat. Historical manual: https://dss.sc.gov/resource-library/manuals/fi_manual_v41.pdf . Its age means it cannot authenticate a 2026 rate.

## Verification boundary

The current FY2026/FY2027 DSS-issued rate sheet or effective-dated current policy-manual table was **not directly obtained** during this check. Public third-party pages assert a 40.46% factor and disagree on benefit amounts; those assertions are NOT primary-source verification. The 0.4046 value used in the preceding hypothetical regression illustration therefore remains **unverified for its applicable effective date**, and must be a fixture parameter rather than a claimed current legal constant. A correct test must distinguish the legal rounding/threshold order (verified in regulation) from the fiscal-year rate (not yet verified).

## Next unchecked action

Obtain the effective-dated DSS FI need-standard/payment-standard/ratable-reduction table or a direct official written publication; record its fiscal-year applicability and any midyear adjustment. Only then pin numeric fixtures against PolicyEngine issue #10497 and execute code tests with qualified review. No contact or filing authorized/performed.

No real payment error, beneficiary impact, upstream correction, external communication, Foundry use, or production mutation established.
