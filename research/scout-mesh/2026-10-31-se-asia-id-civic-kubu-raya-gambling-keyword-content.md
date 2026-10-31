# Scout Mesh — Kubu Raya government information site shows unrelated gambling-keyword content (review candidate)

**Cell:** `se-asia-id-civic` — Southeast Asia / Indonesian / civic access and digital public infrastructure  
**Source review completed:** 2026-10-31T22:38:41Z (UTC; research observation, not a site-server timestamp)  
**Decision:** `verified_candidate` — observable public-page content anomaly, **not** a verified intrusion, compromise, credential leak, malicious redirect, or beneficiary outcome.  
**Owner:** Humanity Loop main worker / Scout lane. **Action authority:** Tier-0 read-only public-source review; any outreach must be separately reviewed and deduplicated.

## INTEND / safety boundary

Assess whether Indonesian digital-public-service information has a specific, independently visible, nonduplicative public-interest problem. Read only publicly indexed official pages. Do not test security controls, enumerate endpoints, follow gambling links, scan for vulnerabilities, access private data, or publish allegations about responsible individuals. This report is a cautious site-content quality flag, not a security incident determination.

## Public-source observations

1. **Kubu Raya Regency Communication and Informatics Department official homepage**, https://kominfo.kuburaya.go.id/ — a same-day public text retrieval on October 31, 2026 displayed two prominent links labelled `slot gacor` (a gambling-related search term) immediately above the regular navigation. Their link targets were **different Indonesian government subdomains**, not ordinary links to Kubu Raya civic information. The page also showed current October 31 local news and regular government menus. This observation establishes unexpected link labels and unrelated destinations in the retrieved page, not who inserted them or whether the destination pages are malicious.
2. **Kubu Raya department article, October 15, 2026**, https://kominfo.kuburaya.go.id/data-dtsen-tidak-sesuai-masyarakat-bisa-ajukan-sanggah-melalui-kanal-resmi — a separately retrieved public page reproduced the same two `slot gacor` navigation links above an otherwise ordinary article about social-benefits data appeals. This suggests a shared page-template issue rather than a typo unique to one article, but no server-side diagnosis was performed.
3. **Search-indexed category page**, https://kominfo.kuburaya.go.id/category/pojok-it?page_hal=5 — search results indexed about two months earlier included a gambling-promotional page headed `Slot Demo ! Link Game Slot Gacor Online...` on the same official host. **Historical index evidence only:** its current live state was not independently established and it may be stale.
4. **Legitimate public-service context and possible mitigations:** Indonesia's Ministry of Communication and Digital explicitly identified social-assistance data corrections and appeal mechanisms as an ongoing priority (September 3, 2026), https://djtpd.komdigi.go.id/berita/dirjen-mira-tayyiba-digitalisasi-bansos-harus-bisa-koreksi-data-yang-keliru . The Kubu Raya article itself points to official appeal channels. The gambling-keyword links are distinct from these legitimate civic-service channels.

## Novelty / falsification / proportionality

- GitHub issue search in the Humanity Loop repository for `kuburaya`, `gambling`, and `SEO spam` returned no existing case at review time. This is **internal** deduplication only; external reports or maintainer awareness were not established.
- The anomaly is independently observable on two distinct same-day public page fetches, with an older search-index signal. The likely user-facing concern is **confusing unrelated promotional-looking links on an official government information service**, not a proven security breach.
- Alternate explanations include authorized but ill-advised content, accidental template content, third-party insertion, stale cached/indexed content, or unauthorized alteration. Without maintainer confirmation or direct live browser comparison, do **not** select one explanation.
- Reversal test: ordinary current browser renders without these links, or site maintainer verifies a legitimate reason, would downgrade/close the candidate. A confirmed owner correction of the exact links after a documented report would permit a narrowly phrased report→correction statement, not causation.
- This is a public-content review, not a vulnerability disclosure or authorization for penetration testing.

## Next bounded action

**Responsible owner:** Humanity Loop main worker / Case Steward intake, with the site operator as actual fixing authority. First verify the current page in a separate ordinary browser and identify the government department's genuine CSIRT/TTIS or official secure reporting channel. If still present, prepare **one** concise, neutral, private factual notice describing the two public-page observations without visiting or spreading promotional destinations. Confirm no prior notice before sending. Do not post a public accusation, send mass messages, or claim the department acknowledged/fixed anything. Recheck after owner response or within seven days (2026-11-07), whichever comes first.

## Outcome accounting

**One source-reviewed Scout candidate.** No contact, institutional acknowledgement, fix, site compromise, registration, adoption, or beneficiary impact established. This file is only an evidence record; a separate independently read-back database completion receipt is required to count this cell as completed. Legacy Scout claim timestamps remain irrelevant to completion.
