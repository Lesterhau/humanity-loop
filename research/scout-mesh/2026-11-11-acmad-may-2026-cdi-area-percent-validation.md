# ACMAD Africa Drought Advisory: May 2026 CDI percentage integrity check

**Observed:** 2026-11-11 UTC. **Type:** external public-interest, read-only climate-data quality verification. **Status:** verified anomalous *published percentages*; underlying geospatial raster, correct replacement values, and downstream effects **not verified**. **Permission:** Tier-0 public-source reading, offline arithmetic and a public-safe internal Humanity Loop receipt only. No agency contact or external publication.

## Original ACMAD sources and non-duplication

- [Official ACMAD bulletin index](https://ada.acmad.org/api/main/bulletins/) co-lists **two** entries dated **22 May 2026**, both labeled *Drought Bulletin May 2026*. Neither index summary distinguishes their underlying dekad.
- [May bulletin A, `africa-drought-bulletin-may`](https://ada.acmad.org/api/main/bulletins/africa-drought-bulletin-may/), [original ACMAD PDF](https://ada.acmad.org/media/bulletins/pdfs/bulletin_2026_05_6J4kfaK.pdf): PDF page 1 explicitly identifies **2026/4/Dekad 11**. Continental CDI Watch/Warning/Alert **12.6/3.3/1.9%** (total **17.8%**).
- [May bulletin B, `africadrought-bulletin`](https://ada.acmad.org/api/main/bulletins/africadrought-bulletin/), [original ACMAD PDF](https://ada.acmad.org/media/bulletins/pdfs/bulletin_2026_05_Y0ipnMw.pdf): PDF page 1 explicitly identifies **2026/4/Dekad 21**. Continental CDI Watch/Warning/Alert **10.6/3.9/0.0%** (total **14.5%**).
- [European Commission JRC CDI definition](https://doi.org/10.2905/JRC.9QA0Z6R) describes Watch, Warning and Alert as spatial drought classes; [US drought.gov explanation](https://www.drought.gov/data-maps-tools/combined-drought-indicator-cdi) independently describes the same three CDI classes. This does **not** establish ACMAD's implementation/denominator, which requires confirmation.

**Important temporal distinction:** 17.8% vs 14.5% and the presence/absence of continental Alert are **not** by themselves a contradiction: the two PDF data periods differ by 10 days. Their common catalog date/title without a dekad label is a provenance/interpretability problem, not proof of an erroneous forecast.

## Reproduced country-level anomalies in the official HTML CDI tables

| Source/data period | Country | Watch (%) | Warning (%) | Alert (%) | Arithmetic sum (%) | Finding |
|---|---|---:|---:|---:|---:|---|
| Dekad 11 | Madagascar | 128.2 | 87.7 | 17.6 | **233.5** | Watch alone exceeds 100; total exceeds 100 |
| Dekad 11 | São Tomé and Príncipe | **589.1** | 0.0 | 0.0 | **589.1** | Watch alone exceeds 100 |
| Dekad 21 | Madagascar | **131.9** | **125.9** | 0.0 | **257.8** | Both Watch and Warning individually exceed 100 |
| Dekad 11 control | Angola | 52.7 | 11.4 | 11.2 | 75.3 | No bounds violation in selected row |
| Dekad 21 control | Côte d'Ivoire | 3.5 | 17.4 | 0.0 | 20.9 | No bounds violation in selected row |
| Dekad 21 control | Senegal | 15.7 | 0.0 | 0.0 | 15.7 | No bounds violation in selected row |

The **Dekad 21 executive summary and its PDF** say **257.9%** of Madagascar is affected by overlapping categories, while the published CDI table adds to **257.8%**; the 0.1 percentage-point difference could be independent rounding, but either number cannot represent a unique proportion of a country's land area. The same executive summary separately describes **42.2%** of Madagascar in Warning, whereas the visible CDI table says **125.9%**. The bulletin's own research section acknowledges that CDI drought extent above 100% warrants methodological investigation. **These observations support a published metric/label integrity defect, not a reconstructed correct drought estimate.**

A category reported as a percentage of *country area* must be between 0 and 100, even if categories overlap. The categories' combined total might exceed 100 if deliberately overlapping measures were used, but **128.2%, 131.9%, 125.9%, and 589.1% individual category coverage** cannot be explained by overlap alone. Possible denominator, land-mask, unit, area aggregation, or data export problems are **hypotheses**, not findings.

## Executable, limited regression

[Offline Python regression](../../runtime/foundry-fallback/2026-11-11-acmad-cdi-area-qa.py) transcribes the six exact source rows, uses decimal arithmetic, rejects any category outside 0–100 and category sums exceeding 100.15 (0.15 percentage-point three-class rounding allowance), and includes positive controls. Executed with Python 3 on 2026-11-11: **9/9 assertions PASS**, with the three anomalous country-period rows flagged and all three controls unflagged. **The test is a source-stamped snapshot, not a live web scraper or a raster audit.** An ordinary runtime fetch of ACMAD failed due to DNS in the execution container; official HTML and both PDFs were independently readable via public web access. No data corrections or deployments performed.

## Human-review-only editorial clarification (French; UNSENT)

> Deux bulletins ACMAD intitulés « May 2026 », datés du 22 mai 2026, correspondent en réalité aux décades 11 et 21 d'avril. Nous suggérons d'indiquer cette période dans la liste publique. Les tableaux CDI présentent des pourcentages de superficie nationale supérieurs à 100 % pour Madagascar et São Tomé-et-Príncipe. Avant toute interprétation ou correction chiffrée, merci de vérifier les dénominateurs, masques géographiques, unités, classes et versions des données, puis de publier, le cas échéant, un erratum daté.

This is a **draft for qualified climate-data editorial review**, not a sent request, confirmed agency response, or correction.

## 10th-Man / falsification and limits

- **Alternative:** categories might use a non-country denominator, or table percentages might be mislabeled as area percentages. In that case the public label and summary remain misleading, but the underlying CDI could be valid. Request denominator and raw cell-count/area metadata before diagnosing the algorithm.
- **Alternative:** two May bulletins could intentionally be distinct dekadal products, not duplicate revisions; the PDF dates support that. Do not select one as authoritative without a documented revision/period rule.
- **Falsifier:** if an official source shows these values are *not* country-area shares and documents an appropriate index scaling, revise the classification from numeric error to insufficient labeling/definition.
- **Unknown:** original gridded CDI values, spatial masks, whether a corrected bulletin exists elsewhere, whether users relied on these percentages, and any real environmental or beneficiary impact.
- **No causation/impact claim:** No outside institution contacted; no source corrected; no outside contributor, AI specialist, or public-health outcome verified.

**Next unchecked, by 2026-11-18 UTC:** Obtain ACMAD methodology and data dictionary for country CDI shares, review original raster/area denominator for both dekads, verify any revised bulletins and the catalog's dekad presentation in an ordinary browser; obtain qualified scientific/editorial review before separately authorized factual outreach. Avoid repeating this text-only arithmetic review absent new data.
