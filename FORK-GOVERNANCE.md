# Fork Lineage & Canonical Identity

Public forks are expected and usually useful.

A fork is a separate repository controlled by its owner. It does not alter the canonical Humanity Loop repository.

## Notification

The canonical repository uses GitHub's `fork` event to record newly created public forks in the Fork Watch issue.

## Review posture

When a fork appears, Humanity Loop may:
- inspect public changes;
- compare key governance and architecture files;
- identify improvements worth bringing upstream;
- record public lineage;
- clarify which repository is canonical.

Different design choices are not treated as harmful by default.

## Limits

Humanity Loop cannot edit another owner's repository without permission.

If a public fork takes a different direction, the canonical project can respond by improving its own implementation, documenting differences, or clarifying project identity.

## Files worth comparing

When useful, compare:
- PROTOCOL.md
- GOVERNANCE.md
- ARCHITECTURE.md
- ROLE-CATALOG.md
- OPENNESS-SECURITY.md
- OPERATIONS.md

Avoid continuous high-cost monitoring of inactive forks.

## Canonical identity

As adoption grows, distinguish the official project through:
- an official domain;
- canonical GitHub repository/organization;
- signed or versioned releases;
- official MCP registry listing;
- published provenance and safety baseline;
- brand/trademark policy if later warranted.

Open code enables learning and replication. Canonical identity tells people which implementation is maintained by the original project.


## Detached copies / copycats

GitHub fork monitoring does not detect someone who copies Humanity Loop files into a brand-new unrelated repository instead of using GitHub's fork mechanism.

Periodically search public GitHub for distinctive canonical phrases / file signatures from:
- PROTOCOL.md
- GOVERNANCE.md
- ARCHITECTURE.md
- REPLICATION-PROMPT.md

When a likely detached copy is found:
- record the repository and public lineage evidence;
- compare governance/safety-critical differences;
- distinguish legitimate reuse from misleading claims of canonical status;
- do not assume harmful intent merely because attribution, branding, or governance differs;
- use canonical identity/provenance mechanisms when clarification is needed.

This is a discovery problem, not permission to interfere with another repository.
