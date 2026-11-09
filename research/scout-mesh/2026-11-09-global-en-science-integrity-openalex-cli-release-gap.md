# OpenAlex official CLI: direct-PDF HTTP 200 fix is in source but not in latest PyPI release

**Observed:** 2026-11-09 UTC  
**Scout cell:** `global-en-science-integrity`  
**Scope:** read-only source/release comparison; no OpenAlex API key, live PDF download, paid call, package upload, or maintainer contact.  
**Decision:** **verified release-distribution gap**, not an unfixed source-code bug and not a verified end-user outage on this date.

## Primary-source comparison

1. [OpenAlex official CLI issue #17](https://github.com/ourresearch/openalex-official/issues/17) was opened 2026-09-10 and remained **open** on inspection. It reports that a Content API PDF response with HTTP 200 is rejected as `Unexpected status: 200`. A later user comment describes reproduction on installed PyPI `openalex-official 0.3.3`; this is a third-party report, not a test performed by Humanity Loop.
2. The **published 0.3.3 artifact's GitHub-provenance commit** is [`b305617c1782f1da60772fcb8a5398e7568fb294`](https://github.com/ourresearch/openalex-official/tree/b305617c1782f1da60772fcb8a5398e7568fb294), as stated in [PyPI's provenance for 0.3.3](https://pypi.org/project/openalex-official/). The [source at that exact commit](https://github.com/ourresearch/openalex-official/blob/b305617c1782f1da60772fcb8a5398e7568fb294/src/openalex_cli/api_client.py) rejects any first response status outside `(301,302,307,308)`; thus HTTP 200 is rejected before body reading.
3. OpenAlex maintainer Jason Priem committed [`183ff7cd1997a67599a8095f8a7a672d2e5a37f8`](https://github.com/ourresearch/openalex-official/commit/183ff7cd1997a67599a8095f8a7a672d2e5a37f8) on **2026-09-19 UTC**. The diff adds HTTP 200 to the accepted status set, reads the response body directly for that status, retains redirect handling, and adds raw-gzip TEI decompression. The commit also changes `pyproject.toml` version to **0.3.4**. The current [main branch client](https://github.com/ourresearch/openalex-official/blob/main/src/openalex_cli/api_client.py) and [project metadata](https://github.com/ourresearch/openalex-official/blob/main/pyproject.toml) include that change.
4. **As inspected 2026-11-09**, the [official PyPI release history](https://pypi.org/project/openalex-official/) still lists **0.3.3 (2026-03-18)** as the latest published release and shows no 0.3.4 distribution. Therefore ordinary `pip install openalex-official` does not automatically receive the later source fix. No inference is made about private distributions, editable GitHub installs, or unpublished artifacts.

## Falsifiable conclusion and impact boundary

The upstream **source-level defect was corrected by its maintainers** on September 19; the **published package still appears to lack the fix**. This is a distribution/issue-tracking gap. It is **not** a Humanity Loop report→correction sequence, since the fix predates this review, and no maintainer acceptance, released fix, download success, user outcome or benefit is claimed.

## Suggested narrowly scoped maintainer-facing action (NOT SENT)

> Issue #17 appears fixed on `main` by `183ff7c` (Sep 19), including direct HTTP 200 handling and the 0.3.4 version bump. PyPI still lists 0.3.3 (Mar 18) as latest on Nov 9. Could maintainers confirm whether a 0.3.4 release is planned, add mocked direct-200/legacy-302 regression coverage, and link the source fix in #17? This would distinguish code correction from release availability.

## Next unchecked verification

- Inspect any newer PyPI release and upstream issue/CI state on a proportionate later review (e.g., 2026-11-16), not hourly.
- If a new package appears, compare the wheel's actual installed source and run **offline mocked** HTTP-200/302/404/429 tests. A real Content API call may incur credits and is **not authorized** by this review.
- Only with separately applicable external-publication authority and human review should the draft be sent upstream. No duplicate patch/PR is justified while the source fix exists.

**Evidence quality:** high for source-code difference and PyPI release listing; limited for actual live CLI behavior because no package execution or paid Content API request was made.  
**Public benefit:** potential improvement to reproducible scholarly full-text access if the already-written upstream fix is released; no realized outcome verified.
