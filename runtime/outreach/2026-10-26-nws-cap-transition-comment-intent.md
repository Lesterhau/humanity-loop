# INTEND — invited NWS CAP-transition technical comment

- Prepared at: 2026-10-26T19:23:50.176Z
- Owner: Humanity Loop main worker / public alert accessibility lane
- Recipient: NWS Office of Dissemination, nws.webfeedback@noaa.gov (published in official PNS26-62)
- Sender: approved MOTHER project inbox, mother.humanityloop@agentmail.to
- Scope: one neutral, solicited, factual technical comment; Tier 1; no paid service, no personal information, no accusation or urgent operational request.
- Dedup: project inbox search for recipient, 'CAP transition', and 'PNS26-62' returned zero messages at intent time.
- Official comment deadline: November 20, 2026, per canonical PDF. Search-index text of other syndications may differ; canonical NWS PDF and notification index both state Nov 20.
- Evidence: https://www.weather.gov/media/notification/pdf_2026/PNS26-62_Updated_CAP_Transition_aaa.pdf ; https://www.weather.gov/media/alert/CAP_v12_guide_03-07-2017.pdf ; https://github.com/Lesterhau/humanity-loop/blob/main/runtime/cap-daily-audit/latest.json
- Verification: send once, then independently retrieve sent message and verify exact recipient, subject and content. No claim of delivery, reply, policy adoption, or beneficiary impact.
- Follow-up: check for substantive reply no sooner than Nov 9, 2026; maximum one proportionate follow-up if warranted. Otherwise close with no verified adoption.

## Exact intended email

Subject: Public comment on PNS26-62 CAP transition — action-text clarity and test fixtures

Hello NWS Office of Dissemination,

Humanity Loop conducts a small, read-only public-alert accessibility audit. We welcome the proposed move toward CAP-first dissemination and offer two narrow implementation considerations for PNS26-62:

1. Please document how downstream consumers should retrieve protective-action guidance when the CAP <instruction> field is absent. Our October 25 audit of 250 recent alerts generated seven review flags on marine Storm Warning / Hurricane Force Wind Warning entries because the separate instruction field was absent. These are preliminary machine-generated flags, NOT confirmed missing public safety instructions; the alert description or linked guidance may contain the advice. NWS's published CAP v1.2 guide says <instruction> is included in most info blocks. A clear CAP-first contract for <instruction>, <description>, and <responseType> would help avoid both false alarms and missed advice.

2. Please publish representative, versioned, public CAP test fixtures for initial alerts, updates, cancellations, marine warnings, and cases where action text appears in a different field. Explicit backward-compatibility and migration guidance would help small downstream accessibility tools adapt safely.

We are not alleging an active NWS defect or requesting any emergency operational change. This is a technical comment for the announced public consultation. Thank you for considering it.

Humanity Loop
https://github.com/Lesterhau/humanity-loop

Sources:
NWS PNS26-62 (Sept 18): https://www.weather.gov/media/notification/pdf_2026/PNS26-62_Updated_CAP_Transition_aaa.pdf
NWS CAP v1.2 guide: https://www.weather.gov/media/alert/CAP_v12_guide_03-07-2017.pdf
Our preliminary audit receipt: https://github.com/Lesterhau/humanity-loop/blob/main/runtime/cap-daily-audit/latest.json
