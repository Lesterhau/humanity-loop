# Scout Mesh — Indonesian civic complaint board displays unrelated banking-support solicitations

**Review date:** 2026-10-27 UTC  
**Cell:** `se-asia-id-civic` (Southeast Asia / Indonesian / civic access and digital public infrastructure)  
**Owner:** Humanity Loop main worker / Scout Owner  
**Decision:** `verified_candidate` for a narrowly scoped *public-content moderation / service-trust* review, **not** verified fraud, a cyber vulnerability, an institutional failure to answer complaints, or actual beneficiary harm.  
**Action level:** Tier-0 public research only. No outreach, form submission, security testing, spending, agent activation, or public campaign.

## Reproducible public-source observation

1. **Primary local-government source:** Tulang Bawang Regency's population and civil-registration service (`Disdukcapil`) publishes a public [complaint form and complaint list](https://sikeptemen.tulangbawangkab.go.id/main/pengaduan). Its own form notice says the complaint list is public and warns users **not** to include national identity numbers, family-card numbers, or other personal data in their complaint text. The page visibly includes older answered complaints as well as later entries marked `Belum Terjawab` (not answered *on the public board*). That label alone does not establish that the agency failed to help someone through other channels.
2. **Specific unrelated entries still present in the public page retrieved October 27, 2026:** Complaint numbers **#419 and #420**, both dated May 5, and **#423**, dated May 13, display ostensibly bank-support/QLola token-recovery instructions directing readers toward WhatsApp contacts. These are unrelated to civil-registration complaints; one entry's displayed sender claims to be a bank-service channel. The page output masks portions of the phone strings. **Do not copy or republish any phone string or complainant identity.** A separate May 3 entry **#414** offers loan-cancellation WhatsApp guidance, another off-topic banking/finance post.
3. **Independent product-owner cross-check:** [Bank Rakyat Indonesia's official QLola information](https://www.bri.co.id/web/guest/id/qlola) confirms QLola is a real BRI business-banking service and directs users seeking QLola assistance to BRI relationship managers, branches, or its published official contact channel. This supports the conclusion that an unrelated government complaint-board post is **not an authoritative banking-support instruction**. It does not prove the posted WhatsApp contacts are fraudulent or unaffiliated with BRI.

**Exact observed issue:** Unrelated financial-service guidance, including apparent customer-support personas and contact prompts, remains visible in an official government *civil-registration* complaint list months after posting. This is a narrow **content-moderation and trust-boundary concern**. It is **not** proof that the government authored or endorsed the content, that readers followed it, or that money or data were lost.

## Why this may matter

A person navigating an official service site may mistake user-submitted text for vetted public guidance. The same page hosts requests about civil-registration records and access to public benefits. Mixing unrelated bank-token guidance into that surface could confuse readers and increase social-engineering exposure. This is a **plausible risk**, not a measured incident.

**Existing safeguards and owners:** The agency explicitly warns against posting personal data; some displayed contact strings are masked; the form includes a CAPTCHA; the agency has a public complaint-list status display. These are partial mitigations, and this review did not inspect the moderation backend, security controls, or any individual user's records. The appropriate owner of the page content is the local Disdukcapil website maintainer, not Humanity Loop or BRI.

## Novelty / duplication

Humanity Loop's October 26 Indonesian Scout examined the national SP4N-LAPOR! coordination agreement and a separate Cilacap pilot, concluding `no_signal`; October 25 reviewed the Batin Tikal municipal complaint link. Those are different systems and defects. A canonical GitHub search for `Tulang Bawang QLola` and issue search for `Tulang Bawang` returned no existing Humanity Loop match at review time. This is a **new candidate within the existing cell**, not a seventh Scout or a new agent.

## STEEP+, TIPPO, Three Horizons and falsification

- **STEEP+:** Social = user trust in official channels; Technological = user-generated public complaint content and moderation; Economic = potential banking-support confusion; Political/institutional = responsibility for local public service channels; Legal/ethical = privacy, accurate service attribution and avoidance of unverified accusations; Values = trustworthy access for residents.
- **TIPPO:** Trend = increasing digital civic-service access; Issue = unvetted off-topic guidance on a government complaint board; Plan = no agency moderation plan verified; Projection = clearer moderation could reduce confusion, not quantified; Obstacles = unknown moderation policy, backend access and off-platform resolution.
- **Three Horizons:** H1 public complaint board with warning/CAPTCHA; H2 proportionate off-topic moderation and clear source labels; H3 trustworthy, accessible, auditable citizen-service routing.
- **Futures Triangle:** Push = digital service publication; Pull = residents reliably finding official help; Weight = public comment history and mixed agency/user-authored content.
- **Cross-impact:** Better moderation could reduce confusing solicitations but must avoid hiding genuine grievances or erasing evidence of agency responsiveness. A narrowly scoped intervention should preserve legitimate complaint rights.
- **Falsification / reversal:** An independently verified current page without these entries, proof they were removed, a maintainer explanation establishing legitimate context, or evidence that the text is not publicly visible to ordinary users would narrow or retire this candidate. A third-party crawler rendering alone is not proof of reach or user harm.

## Decision and bounded next step

**`verified_candidate`** for one factual, non-accusatory *content-moderation review*; not yet an external report or accepted fix. **Next action:** Scout Owner to verify the specific entries remain visible in an ordinary browser and identify the legitimate official maintainer feedback route; if confirmed and not already reported, prepare **one** short, neutral, human-reviewable notice asking the agency to assess off-topic financial-service posts and whether its moderation/privacy notice needs strengthening. No contacts with complainants, bank impersonation accusations, bulk messaging, credential testing or direct changes to the third-party site.

**Next review:** 2026-11-03, or sooner upon a substantive verified agency response. **Stale threshold:** 2026-11-10. No public correction, agency contact, user benefit, node adoption, or independent specialist execution is claimed.
