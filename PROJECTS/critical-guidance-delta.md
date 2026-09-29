# Critical Guidance Delta

**Category:** Information infrastructure  
**Status:** Live  
**URL:** https://critical-guidance-delta-y7nzmd.v2.appdeploy.ai/

## Plain-English purpose

Critical Guidance Delta watches official medication-safety pages and records when important guidance changes.

If an agency quietly changes a warning, contraindication, safety notice, or other medication guidance, the system preserves the old version and the new version so people can see exactly what changed and when.

### Why someone outside healthcare should care

Safety guidance can change without most people noticing. This project creates an auditable change history instead of relying on memory, screenshots, or a page's current wording.

## Technical function

Tracks material changes in authoritative medication-safety guidance while retaining raw evidence and source provenance.

## Guardrail

AI materiality classification is triage. It never deletes the underlying recorded page change.

## Replication

Start with a small number of authoritative sources. Preserve old/new evidence and deterministic fingerprints. Do not expand source coverage faster than signal quality can be measured.
