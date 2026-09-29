# Evidence Integrity Sentinel

**Category:** Scientific integrity  
**Status:** Live  
**URL:** https://evidence-integrity-sentinel-uip4nx.v2.appdeploy.ai/

## Plain-English purpose

When a scientific paper is retracted, later reviews and guidelines may still cite it.

Evidence Integrity Sentinel finds those downstream documents so a qualified human can check whether the retraction changes anything important.

It does **not** assume that every paper citing a retracted study is wrong.

### Why it matters

Scientific corrections do not automatically propagate through every later paper, guideline, or evidence summary that used the original work. This tool helps identify places worth re-checking.

## Technical function

Flags downstream evidence products that may warrant human reassessment after source-paper retraction.

## Guardrail

A downstream work citing a retracted paper is not automatically invalid. The tool identifies candidates for human review.

## Replication

Use open retraction and citation data. Preserve DOI/source provenance. Optimize precision before expanding coverage.
