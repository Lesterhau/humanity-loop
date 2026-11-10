# NYC ACCESS NYC HEAP multilingual 2026–27 application-status mismatch — public-source review

**Review date:** 2026-11-10 UTC  
**Status:** verified mismatch in publicly retrieved city-owned page text; **unsent** editorial correction candidate; human/browser and translation review pending.  
**Scope:** NYC Home Energy Assistance Program (HEAP) Regular and Heating Equipment Repair & Replacement (HERR), not an eligibility determination, website penetration test, or claim of beneficiary harm.

## Official current baseline

1. [ACCESS NYC English HEAP program page](https://access.nyc.gov/programs/home-energy-assistance-program-heap/), marked **Last Updated November 2, 2026**, says **2026–27 Regular HEAP opened November 2, 2026**, **Emergency HEAP opens January 4, 2027**, and **HERR opened October 1, 2026 for income-eligible homeowners of all ages**.
2. [NYC HRA notice republished by Brooklyn Community Board 4](https://www.nyc.gov/site/brooklyncb4/news/news.page), under **November 2026 / “2026-2027 Home Energy Assistance Program (HEAP) Regular Component Opening Date Update,”** confirms Regular HEAP opened November 2, with a **planned April 16, 2027 end or earlier exhaustion of funds**; online ACCESS HRA and paper applications by mail, fax, or in person are described. This is a scheduled closing date, not a guarantee of funds.
3. [NYC HRA community-partner guidance](https://home4.nyc.gov/site/hra/partners/community-updates.page), section **“HEAP Heating Equipment Repair and Replacement (HERR) and Clean & Tune Opening”**, expressly states **October 1, 2026** opening and **eligible homeowners of any age** for 2026–27; 2025–26 HERR was restricted to age 60+. Its adjacent historical note saying Regular had not yet opened should not override the separate Nov 2 notice.

## Same city website: language-specific differences

Each linked ACCESS NYC translated page, in the publicly retrieved text, still says the **2025–26 Regular HEAP application period is closed** rather than explaining that **2026–27 Regular HEAP is open**. The same pages describe **2025–26 HERR as closed** and limit the program to **homeowners aged 60+**, while the English page and NYC HRA 2026–27 update say HERR is **open to eligible homeowners of all ages**.

| Locale / exact official URL | Regular HEAP wording retrieved | HERR wording retrieved | Displayed last-update date |
|---|---|---|---|
| [Spanish /es/](https://access.nyc.gov/es/programs/home-energy-assistance-program-heap/) | “Las solicitudes para la temporada de calefacción de invierno 2025-2026 ya están cerradas” | 2025–26 closed; homeowners 60+ | 11 junio 2026 |
| [Polish /pl/](https://access.nyc.gov/pl/programs/home-energy-assistance-program-heap/) | “Termin składania wniosków na sezon grzewczy 2025–2026 upłynął” | 2025–26 closed; homeowners 60+ | 11 czerwca 2026 |
| [Russian /ru/](https://access.nyc.gov/ru/programs/home-energy-assistance-program-heap/) | “Завершился прием заявлений на отопительный сезон 2025-2026 гг.” | 2025–26 closed; homeowners 60+ | 11.06.2026 |
| [Bengali /bn/](https://access.nyc.gov/bn/programs/home-energy-assistance-program-heap/) | “2025-2026 শীতকালীন হিটিং সিজনের আবেদন গ্রহণ বন্ধ হয়ে গেছে” | 2025–26 closed; homeowners 60+ | June 11, 2026 |
| [Traditional Chinese /zh-hant/](https://access.nyc.gov/zh-hant/programs/home-energy-assistance-program-heap/) | “2025-2026 冬季供暖季申請現已截止” | 2025–26 closed; homeowners 60+ | 2026-06-11 |

**Two bounded information-access defects:**

- **Opening status:** These five translations can leave a current applicant with the misleading impression that there is no open Regular HEAP application, despite the 2026–27 program being open.
- **HERR eligibility and availability:** The translated pages retain the prior 60+ restriction and closed status, potentially discouraging otherwise eligible homeowners younger than 60 from seeking the 2026–27 HERR benefit.

The statements that the **old 2025–26 season closed** are not literally false; the defect is that these public program pages omit the now-open **2026–27** program and retain superseded age guidance. The 2026 summer cooling benefit being closed is not identified as an error.

## Retrieval limits / independent verification gate

- Public web reader opened the exact six official ACCESS NYC URLs and the two city cross-checks on Nov 10. The reader reports English page crawled today; Spanish, Polish, Russian ~6 days earlier; Traditional Chinese ~3 days earlier; Bengali ~one month earlier. Thus the text and displayed last-update dates are independently available but **do not prove an uncached, ordinary-browser response from the live origin at this instant**.
- Separate direct Python HTTPS requests to ACCESS NYC from the worker's container failed at the network connection layer; no HTTP response was obtained. This is **not evidence the public site is down**.
- No human user session, translation-editor review, current application submission, individual outcome or causal harm was tested. Only these five translated pages were checked, **not all eleven** advertised translations.
- No outreach, publication to agency channels, production mutation or paid model call was made.

## Unsent, neutral editorial correction proposal (for qualified NYC translation review)

“Please synchronize the HEAP program page across all supported languages with the current English version and HRA policy: 2026–27 Regular HEAP applications opened November 2, 2026; 2026–27 HERR and Clean & Tune opened October 1, 2026; HERR is available to eligible homeowners regardless of age this season; Emergency HEAP is not yet open and is scheduled to open January 4, 2027. Keep the funding-exhaustion qualification, current application routes, and other eligibility conditions. Verify every translation, including the age-limit change, before publishing.”

**Next unchecked step:** By **2026-11-12 UTC**, perform independent ordinary-browser checks of Spanish and at least one additional language plus current English, confirm whether the live rendered pages still differ, then obtain qualified benefits-policy and language editorial review. Only after separate owner authorization consider a single targeted factual notice to the NYC ACCESS NYC editorial team. If already corrected, document a no-longer-current finding without claiming Humanity Loop caused the change.

**Classification:** evidence-backed, review-only public-information correction candidate. No verified applicant impact, agency receipt, fix, independent contributor or volunteer hours.
