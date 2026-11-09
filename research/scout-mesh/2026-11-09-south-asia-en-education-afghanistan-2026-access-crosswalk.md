# Afghanistan education access: November 2026 official-indicator crosswalk and verification gate

**Scout cell:** `south-asia-en-education` | **Checked:** 2026-11-09 UTC | **Type:** new official evidence / service-access planning signal | **Risk:** Tier-0 public-source research only | **Status:** evidence baseline, NOT a completed intervention

## Why this matters

UNESCO and UNICEF jointly released the *Afghanistan Education Situation Report 2026* on **4 November 2026**. Their new figures describe overlapping but **non-interchangeable populations**: primary-age children outside *formal general education*, adolescent girls excluded from secondary schooling, children attending community classes, public-primary enrolment, and returnee children requiring support. Combining these counts into one purported “children out of education” total would double-count or conflate age groups and definitions. This crosswalk is designed for public-interest researchers and education programme planners checking claims before allocating support; it is not a grant award, operational programme, or assertion that any child has received help from Humanity Loop.

## Source-locked figures (do not sum across rows)

| Indicator | Official reported value | Population, time and interpretation | Verification limitation |
|---|---:|---|---|
| Outside **formal general education** | **53%** | Primary-school-age children; stated in 4 Nov 2026 release | Does **not** mean 53% receive no learning of any kind; denominator/method must be checked in full report |
| Girls denied secondary education since 2021 | **more than 2.6 million** | Adolescent girls affected by restrictions, as characterized in release | Do not add to primary-age 53%; different ages and reference periods |
| Community-driven classes | **about 5,300** | Operating by **October 2026** | Not a count of schools or a substitute for formal education |
| Community-class learners | **about 162,000**, **64% girls** | October 2026 snapshot; approximation | Do not infer exact unique learner identities or persistence; do not add to primary enrolment without deduplication |
| Public-primary enrolment | **about 6.6 million** | Enrolled in **2025**, approximately 560,000 above 2022 | Administrative enrollment is not attendance or proficiency; cannot subtract from 2024 total school-age population to derive out-of-school |
| School-age population | **about 10.4m (2019)** and **11.5m (2024)** | Broad school-age population, not specifically primary age | Different age scope than the 53% metric |
| Foundational learning | **less than half** of Grade 4 pupils met Grade 3 language minimum; **one in four** met Grade 3 math minimum | National assessment of **more than 55,000** pupils across 34 provinces | Sample/method and population representativeness need full-report verification |
| Returnee children needing education support | **more than 245,000** | By **September 2026**, alongside about 1.23m Afghan returnees that year | Need is not verified service delivery; do not assume all are out of school |
| Early childhood participation | **fewer than 1 in 100** | Children aged 3–4 in early-childhood education | Distinct cohort, not a primary enrollment estimate |

**Primary publication (directly read):** [UNICEF Afghanistan, 4 Nov 2026 joint release](https://www.unicef.org/afghanistan/press-releases/more-half-primary-school-age-children-afghanistan-outside-formal-education-unesco), independently mirrored as the same joint announcement by [UNESCO, 4 Nov 2026](https://www.unesco.org/en/articles/more-half-primary-school-age-children-afghanistan-outside-formal-education-unesco-and-unicef-warn). **Full underlying report catalog record (located, full contents not yet audited):** [UNESCO UNESDOC 2026 report](https://unesdoc.unesco.org/ark:/48223/pf0000399847). Two agencies publishing the same joint release are **not two independent underlying datasets**.

## Practical reusable screening checklist for any proposed education-access intervention

A local organization, independent evaluator, or potential funder can use these **non-identifying, aggregate** questions before claiming results:

1. **Target and denominator:** Which *specific* age group, district-level service area (only if publication is safe), formal/nonformal modality, baseline date, and inclusion criteria? Distinguish primary-age from adolescent girls and returnees.
2. **Access versus attendance:** Is the measure registration, verified attendance, learning participation, retention, or completed instruction? Record separate counts and dates; do not count classroom capacity as students reached.
3. **Learning quality:** What age-appropriate literacy/numeracy assessment and baseline/follow-up measure are used? Do not equate participation with improved proficiency.
4. **Equity and safety:** Can results be aggregated by gender, disability, and displacement status **without publishing identifiable minors, exact sensitive classroom locations, or participant rosters**? Is safeguarding and informed consent established?
5. **Counterfactual and attribution:** Could the same learners already be served by another program? What independent partner receipt verifies service delivery and prevents double counting?
6. **Implementation constraints:** Is there a legitimate, locally governed pathway for learning materials, trained educators, safe access, and follow-up? This document does not authorize contact, cross-border transfers, or unsupervised activity.
7. **Review:** Does a qualified human reviewer validate source interpretation, program safety, and evidence before a public claim or action?

**Reusable minimal outcome fields:** `period_start`, `period_end`, `age_cohort`, `learning_modality`, `eligible_population_definition`, `enrolled_aggregate`, `attended_aggregate`, `retained_aggregate`, `assessed_aggregate`, `proficiency_aggregate`, `evidence_url`, `independent_reviewer`, `privacy_review`. Never store child names, photos, coordinates or identifiable individual education records in a public receipt.

## Scout assessment and falsification

- **Novelty 0.65 / usefulness 0.75 / evidence quality 0.85** (heuristic, not a measured impact score). Fresh joint UN report with actionable distinctions; no independently verified local uptake.
- **STEEP+**: Social (education access), Technological (distance alternatives), Economic (resource scarcity), Environmental (displacement/emergencies), Political/Legal (restrictions on girls), Ethical/Values (non-discrimination and protection of minors), Demographic (cohort growth and returnees).
- **TIPPO**: Trend = constrained access and population pressure; Issue = primary-age formal exclusion and quality; Problem = service-delivery and measurement gaps; Possibility = independently evaluated safe community education support; Opportunity = standardized non-identifying measurement; no wild-card forecast asserted.
- **Three Horizons**: H1 restricted formal provision and existing community classes; H2 carefully reviewed support and data-quality methods; H3 restoration of inclusive formal education (normative goal, not a prediction).
- **Futures Triangle**: Push = population growth/returns; pull = universal education rights and improved learning; weight = restrictive policies, safety, limited investment. Cross-impact: displacement increases demand and strains learning quality.
- **Falsification/next check:** Read the full 2026 report's definitions and methods for the 53% estimate and community-education learner denominator; compare with any updated UNICEF education cluster response dataset. If the denominators or dates differ from this release interpretation, revise the crosswalk. Check whether a credible existing organization already publishes a more precise, privacy-safe comparable indicator table before proposing new infrastructure.
- **Decision:** retain as a public-interest source/indicator quality resource; **do not** infer a newly discovered government website defect, ask for donations, contact Afghan schools or individuals, or claim an independently delivered education outcome. **Next unchecked:** full-report methodology review and safe independent program-output evidence, if an authorized partner requests it.

**Execution boundary:** No outreach, personal data collection, model-costly Foundry, AppDeploy use, participant billing, production changes or third-party publishing.
