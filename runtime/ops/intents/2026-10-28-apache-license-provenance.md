# INTEND — clarify Apache-2.0 licensing scope and provenance boundaries

- Date: 2026-10-28 UTC.
- Actor: Humanity Loop main worker, authorized by owner's 2026-10-28 decision in issue #32.
- Target: create `LICENSE-SCOPE.md` in the canonical public Humanity Loop repository. No copyright assignment, new legal entity, external distribution, or third-party communication.
- Risk: Tier 1 public project documentation; rights-sensitive. Existing owner approval is Apache-2.0 for eligible original material only.
- Evidence/preflight: root `LICENSE` and README independently fetched after commits `e1567ae` and `e1f8590`; normalized root license text matched SPDX Apache-2.0; recursive repository tree showed 381 tracked blobs, two SVG assets and no vendored `node_modules` directory; `mcp-server/package-lock.json` lists 86 dependency entries with separate licenses; representative first-party source files had no embedded third-party license headers. These checks do NOT prove complete authorship or clear every embedded third-party excerpt.
- Intended scope statement: clarify that Apache-2.0 covers only eligible original material and rights actually held by Ryan Lester; dependencies, external-source excerpts/data, third-party code, branding/trademarks and assets of unverified provenance are not silently relicensed. Keep licensing/provenance exceptions open for case-by-case review. The LLC is the operator, not the copyright assignee.
- Verification: independently fetch the created `LICENSE-SCOPE.md` and confirm exact exclusions, then update issue #31 only if the write succeeds. Do not claim third-party provenance is fully cleared or OSS directory eligibility solely from the root license.
- Stop/rollback: if GitHub write is blocked by safety checks, stop and retain read-only findings; if the text overstates rights, correct through a separately reviewed change.
