# CAP Clarity Check

**Category:** Prevention / safety  
**Status:** Live  
**URL:** https://cap-clarity-check-0jbjid.v2.appdeploy.ai/

## Plain-English purpose

Emergency-alert systems use a standardized machine-readable format called **CAP: Common Alerting Protocol**.

CAP Clarity Check reviews an alert file **before publication** and looks for mistakes that could make the message:
- technically invalid;
- confusing or incomplete;
- badly targeted geographically;
- missing required action details;
- inaccessible to some audiences;
- inconsistent across language versions.

Think of it as a **pre-flight safety check for emergency alerts**.

### Example

Before an agency sends a wildfire evacuation alert, the tool can flag that the alert has no usable instruction, an invalid timestamp, a malformed geographic area, or language/accessibility problems.

It does **not** rewrite the emergency order or invent what people should do.

## Technical function

Browser-only pre-publication CAP 1.2 linter for structural, actionability, targeting, language, and accessibility risks.

## Guardrails

- Alert content does not leave the browser.
- The tool does not rewrite emergency instructions.
- It does not invent protective actions.
- Heuristics are labeled separately from CAP compliance checks.

## Replication

A replicator should preserve the privacy-first browser-only model and keep compliance checks distinct from operational heuristics.
