# Prospective source-discovery amendment A1 — October 21, 2026

**Applies only to public-source discovery after failed v1.0 discovery. It does NOT change topic strata, window, case eligibility, primary/secondary outcomes, per-post approval, or no-public-contact rules.**

## Reason documented before amended retrieval
The preregistered first search submitted all eight fixed `site:x.com/grok/status "<term>" "2026"` queries through a fast indexed engine in one batch. Its returned items had **no attributable per-query ranking**, and included unrelated X trending summaries and an account unrelated to @grok. The entire failure and 0 verified cases are preserved in `discovery-log-2026-10-21.json` commit `c3f2d7e8fc8be991a92a443338ffa682ffdbc4e3`. Since this is a source-retrieval failure rather than an outcome observation, source-query repair is prospectively allowed.

## New fixed secondary retrieval procedure
- Use a **separate independent search request per stratum**, sequentially in the original order, through a distinct public search system (web **slow** mode) and preserve the first up-to-10 displayed results for that stratum without reranking or ideological selection.
- Exact fallback queries (the only change is removing the quoted year):
  1. `site:x.com/grok/status climate`
  2. `site:x.com/grok/status vaccine`
  3. `site:x.com/grok/status nuclear`
  4. `site:x.com/grok/status GMO`
  5. `site:x.com/grok/status photosynthesis`
  6. `site:x.com/grok/status "plate tectonics"`
  7. `site:x.com/grok/status orbital`
  8. `site:x.com/grok/status aspirin`
- Publication dates **must still** independently fall within `2026-07-23T00:00:00Z` to `2026-10-21T00:00:00Z` exclusive. No fallback to earlier years.
- Each candidate must be directly publicly retrievable and attributed to `@grok` with original post text and date, not just snippet, quote/screenshot, archive claim or `x.com/i/grok/share`. Select first eligible claim in result order until target; record all exclusions.
- No further search expansions in this phase. Any more changes require another prospective amendment and retention of prior failures.
- A result without verifiable source text or date is `unverified`, **not an audit case**. Original research cohort is not a probability sample.
- No X posts/replies, private X credentials, auto-reply bots or billing changes.

This amendment is a transparently disclosed feasibility repair. If the secondary engine also cannot access original @grok answers, report the feasibility blocker and stop rather than fabricating corpus evidence.
