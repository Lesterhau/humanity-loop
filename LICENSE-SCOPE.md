# Humanity Loop — Apache-2.0 scope and provenance boundaries

**Status:** Public licensing clarification, 2026-10-28. This is a bounded provenance review, not a certification that every historical file has been individually cleared.

## Owner decision and grant

Ryan Lester has authorized release under the [Apache License, Version 2.0](LICENSE) **only for original Humanity Loop material for which he holds the necessary rights**. This can include original project source code, tests, schemas, protocols, specifications, and original portions of documentation and research commentary. No rights are granted beyond those actually held by the licensor. Material that cannot legally be licensed by the project is not made Apache-2.0 merely by appearing beside a root `LICENSE` file.

**Copyright/operation:** Copyright © 2026 Ryan Lester, to the extent copyright subsists and is owned by him. RL Perspectives, LLC operates the project; the public brand is RL Perspectives. The Apache release is **not** a transfer or assignment of copyright to the LLC. See [governance checkpoint #32](https://github.com/Lesterhau/humanity-loop/issues/32).

## Exclusions and separate rights

- **Third-party packages and dependencies:** Packages referenced by `mcp-server/package.json` and `mcp-server/package-lock.json` remain subject to their own licenses. The lockfile includes MIT, Apache-2.0, LGPL-3.0-or-later, ISC, BSD-3-Clause, 0BSD, CC-BY-4.0 and compound license expressions. An Apache root license does not relicense those packages or replace their obligations.
- **External-source content and public records:** Third-party quotations, journal/paper excerpts, government or agency material, externally authored correspondence, API/feed data, screenshots, archived snapshots, external code examples and linked websites retain their own rights or public-domain status. Only independently original Humanity Loop commentary or arrangement is within this project's grant, if otherwise eligible. Factual findings and public URLs are not assertions of copyright ownership.
- **Names, marks and graphics:** Apache-2.0 §6 does not grant trademark rights. The Humanity Loop and RL Perspectives names, logos, identity marks and the SVG icon assets in `plugin/humanity-loop/assets/` are **not affirmatively cleared for separate reuse** by this review; obtain an explicit rights determination before republishing them as brand assets.
- **Unverified contributions:** A contributor may license only work they have authority to contribute. Do not import proprietary code, unlicensed third-party media, private user information or sensitive credentials. Existing project material that was AI-assisted is offered only to the extent any enforceable, transferable rights actually exist; the project makes no blanket claim of copyright in AI-generated output.

## What was checked

On 2026-10-28, a read-only inspection of the GitHub default-branch recursive tree found **381 tracked blobs**, including original-looking source/test files, documentation and runtime records, **two SVG assets**, and no checked-in `node_modules` or vendored dependency directory. The `mcp-server/package-lock.json` inventory listed **86 dependency entries** with their own license metadata (plus the root project entry). Representative `scripts/` and `mcp-server/` source headers were checked for embedded license/copyright notices; no third-party license headers were found in the sampled files. The root `LICENSE` was compared to SPDX's Apache-2.0 reference after whitespace normalization and matched the standard terms. The README independently confirms the owner/operating-entity distinction.

**Limits:** This is not a complete file-by-file authorship audit, a determination of all contributors' rights, a trademark clearance, a warranty that no third-party text is embedded in documents, or legal advice. A missing copyright header does not prove ownership. Source-code imports do not themselves mean third-party code has been copied into the repository. Retain original attribution and any separate license notices.

## Contributor and distribution guidance

Reuse eligible original project material under Apache-2.0, preserve required notices, and follow the license's attribution/change-notice terms. For a file with ambiguous origin, external-source content, graphics, or conflicting license metadata, **pause reuse of that file** and raise a specific provenance question in [issue #31](https://github.com/Lesterhau/humanity-loop/issues/31). Do not present the ChatGPT plugin, autonomous Foundry, or contributor-node adoption as independently verified because a source license now exists.

Before a new directory submission or distribution package, check that directory's current criteria, the exact included files and any dependency/asset obligations. Directory listing is not a node installation, completed contribution or beneficiary impact.
