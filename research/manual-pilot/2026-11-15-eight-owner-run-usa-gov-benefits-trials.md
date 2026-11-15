# November 15, 2026 — eight owner-run manual AI pilot reports: independent review and workflow fixes

**Status:** Internal pilot evaluation; not a contributor-node milestone, not an accepted real-world correction, not a basis for contacting an agency. No participant names, sender email addresses, mailbox message IDs, screenshots, secrets, personal benefit information, or verbatim private email bodies are published.

## Scope and provenance

Owner used the existing [`/try` manual public-page check](https://humanity-loop.vercel.app/try) with **eight distinct AI/model-host modes** and sent **eight messages** with the expected subject to the project's private inbox on **November 15, 2026, 16:19–17:19 UTC**. The aggregate is independently supported by the authorized AgentMail inbox metadata, and full message bodies were individually read and classified. These are **owner-run tests**, not eight outside friends or independent registered AI nodes.

The tasks concerned [USAGov Government benefits](https://www.usa.gov/benefits). The requested source was public information only; assistants were to avoid unsafe government-account interactions and disclose uncertainty. Two runs could not retrieve useful page content. Six produced short observations or honest negatives, but **none includes a verified first-hand human confirmation of an alleged defect** in the submitted material. Zero reports meet independent acceptance criteria as of this review.

## Eight distinct run outcomes (anonymized source summaries)

| Assistant / mode as labeled by owner | Report type | Evidence status / disposition |
| --- | --- | --- |
| Claude | Social Security benefits application guidance includes a further SSA.gov handoff, not a broken link | Some public page wording is source-confirmed. The possible user-friction hypothesis is not tested with real users; **unverified**, no acceptance |
| DeepSeek | Utility-help card and linked page appear consistent | Credible **negative finding**, not a verified defect; needs human verification |
| GLM via Perplexity | Two hub cards overlap in their descriptions of missing government payments | **Source-backed navigation-overlap observation**, unproven user confusion, no human check |
| Muse | Benefit finder link loads; its text reader could not inspect interactive first screen | **Tool-limited**, not a broken site or source error; manual verification outstanding |
| Grok | Wrong/missing payments page provides program contacts; automated Social Security locator returned an HTTP 403 | **No demonstrated page defect**; a crawler denial is not evidence that normal users cannot use the SSA locator |
| Gemini Task mode | Same overlapping missing-payment cards highlighted independently of GLM | **Source-backed navigation-overlap observation**, unproven user confusion, no human check |
| Gemini Chat mode | No live web retrieval; asked for pasted public page text | **Access blocked in this host mode**, not a finding on USAGov |
| Kimi instant | Returned only a thin shell, honestly requested public text from owner | **Access incomplete**, not a finding on USAGov |

## Source verification, independently performed November 15

1. [Official benefits hub](https://www.usa.gov/benefits) publishes both `Government checks and payments` (missing government checks, unexpected payments, paying the government) and `Where to report incorrect benefit payments` (missing or incorrect federal benefit payments). **The two link descriptions overlap**.
2. [Government checks and payments](https://www.usa.gov/government-checks-payments) includes guidance on lost/missing/stolen/expired payments and explicitly links users seeking assistance for Social Security, SNAP, TANF and VA payments to the [incorrect benefit payments](https://www.usa.gov/report-incorrect-benefit-payments) page. The two pages cover different but overlapping scopes. This provides a factual basis for a *possible* navigation-label refinement, **not** proof that visitors are confused or payments are mishandled.
3. [Benefit finder](https://www.usa.gov/benefit-finder) publishes an instruction to select benefit categories and shows selectable category options. A truncated AI text-reader output must not be interpreted as proof that the government site lacks a next step.
4. [Help with utility bills](https://www.usa.gov/help-with-utility-bills) explicitly includes energy/heating/cooling/weatherization (LIHEAP/WAP) and phone/internet (Lifeline), consistent with the hub-card description.
5. [Social Security benefits and how to apply](https://www.usa.gov/what-is-social-security) lists benefit types and sends readers to SSA.gov benefit pages. That is a real additional link hop but no objectively established navigation defect.

The official pages were checked through fresh independent source retrieval; the notes do **not** claim an independent human used a normal browser or that these exact versions will remain unchanged in the future.

## Reviewer decisions

- **Two browse-limited runs:** count as useful product-testing failure-mode evidence, not task-quality failures or public defects.
- **Two reports on the same subject:** deduplicate to ONE possible navigation hypothesis. Two model outputs reading the same public source are not two independent people, and agreement is not a user-impact measurement.
- **Two no-issue / limited-scope checks:** retain as negative/neutral, not as impact.
- **Social Security extra hop and benefit-finder first screen:** optional minor UX review only; no supported defect report yet.
- **External agencies:** **NO outreach**. The USAGov page has a [website issue form](https://www.usa.gov/site-issue-report-form), but its existence is not permission or justification to send an untested complaint.
- **Outcome attribution:** zero independently accepted third-party node contributions and zero downstream fixes from these eight manual trials. All eight originated with the project owner; different models are not independent *owners* or community participants.

## Root-cause improvements implemented with this review

1. Preserve browser honesty; never let the model claim it opened a page when the request was blocked or returned a shell.
2. If the model cannot browse, **offer a specific one-link human check** rather than asking a lay volunteer to paste an entire webpage and waiting indefinitely.
3. Require one short output even if the outcome is **no issue** or **couldn't verify**.
4. On the public site, offer three explicit human-selected results: personally checked/no issue; personally checked/possible issue; unable to verify. A visitor can generate a short subject-labeled email via their own mail app or copy the report for a private message, without an app account, tokens, external API or paid resources. No automatic email is sent.
5. Confirm that /status **only measures connected-network registrations/submissions**. The manual inbox is a separate track; avoid portraying all eight owner-run trials as external registered contributions.
6. Request an independent human first-hand browser check before treating "overlapping labels may be confusing" as a verified user-experience problem. Prefer a small pre-specified task with several people and record how they actually navigate.

## Next authorized gates

- Validate the new /try mobile interaction and compile/build tests in GitHub Actions.
- Await **genuine non-owner reports** to the private inbox or confidential direct owner handoff; preserve privacy and record reviewer disposition individually. Do not assume the seven interested Facebook commenters have completed anything.
- If real people independently demonstrate confusion between the two links, draft a specific non-accusatory suggestion and ask owner authorization before submitting to USAGov. Do not infer a defect from model consensus alone.
- Keep the PolicyEngine NH FANF full-program tested patch, Founder/Foundry safety, production GitHub branch protection, and verified adoption workstreams separate. This manual pilot does not expand risk permissions or enable model spending.
