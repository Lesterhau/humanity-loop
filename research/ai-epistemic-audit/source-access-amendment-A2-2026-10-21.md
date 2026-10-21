# Prospective source-access amendment A2 — 2026-10-21

## Observed new tool capability before collecting cases
The newly connected TinyFish Fetch tool can extract the original @grok post text, author and X publication date **without signed-in cookies**. Tested only on previously excluded older public URL `https://x.com/grok/status/2039856296308957331`, whose X page itself confirms `@grok`, Apr 3 2026 and exact content; it is NOT part of the study corpus. TinyFish profile has **no signed_in_sites**. The preceding zero-case v1/A1 logs remain unchanged.

## Prospectively locked search before candidate collection
- Keep original date window **2026-07-23 through 2026-10-20 inclusive**, same 8 topic strata, 12+4 slots, source/adjudication/approval gates.
- Use **TinyFish public `search`** once per topic in the pre-registered stratum order; no login, API secrets, social posting, paid browser agent, monitoring or automation. Search with exact initial query strings below, `include_domains:"x.com"`, `after_date:"2026-07-23"`, `before_date:"2026-10-21"`, `page:0`. Dates in returned search metadata are *candidate hints*, never independent proof.
1. `site:x.com/grok/status climate`
2. `site:x.com/grok/status vaccine`
3. `site:x.com/grok/status nuclear`
4. `site:x.com/grok/status GMO`
5. `site:x.com/grok/status photosynthesis`
6. `site:x.com/grok/status "plate tectonics"`
7. `site:x.com/grok/status orbital`
8. `site:x.com/grok/status aspirin`
- Freeze first up-to-10 returned ranks per stratum; record all eligible/ineligible in returned order, without replacing empty search results or changing topic terms to get a desired outcome.
- For ranked candidate direct URLs, use TinyFish **read-only `fetch_content`**, independently confirm X canonical URL `https://x.com/grok/status/<id>`, author `@grok`, publicly presented original text and explicit published_date in required window. Exclude `x.com/i/grok/share`, unrelated authors, inaccessible texts and missing/out-of-window dates. Preserve only necessary short excerpts and public URLs, not entire user conversations.
- If search yields no date-qualified verifiable results, record `source_collection_blocked`, not a biased accuracy estimate. Do **not** broaden terms/time windows in this study without a future prospective amendment.
- Never post, reply, quote, contact users, change X account, create recurring monitor or use a paid automation agent for this read-only pilot.

This amendment changes **only the search/fetch provider**, not research hypothesis, selection rules, population definition, scoring or safety constraints. A data access improvement is not a license for post-hoc cherry-picking.
