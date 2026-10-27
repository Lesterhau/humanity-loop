#!/usr/bin/env python3
"""Credit-free, triage-only backup for Humanity Loop Evidence Integrity Sentinel.

Reads public Crossref retraction metadata and Europe PMC citation links.
Writes candidate leads for HUMAN verification. No clinical/legal conclusions,
no email, no external writes besides the canonical GitHub runtime receipts.
This does NOT sync with the separate AppDeploy database/UI.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

ROOT = Path("runtime/evidence-integrity-backup")
CROSSREF = ("https://api.crossref.org/works?"
            "filter=update-type%3Aretraction&sort=updated&order=desc&rows=25"
            "&mailto=mother.humanityloop%40agentmail.to")
USER_AGENT = "HumanityLoop-EvidenceIntegrityBackup/0.1 (mailto:mother.humanityloop@agentmail.to)"
MAX_DOIS = 15
MAX_CITATIONS = 1000


def get_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    # One bounded retry for transient upstream server failures; never retry rate limits
    # or a response with Retry-After. The caller still fails closed and preserves
    # unprocessed DOIs if the provider remains unavailable.
    for attempt in range(2):
        try:
            with urlopen(request, timeout=25) as response:
                return json.load(response)
        except HTTPError as exc:
            if (attempt == 1 or exc.code not in (502, 503, 504)
                    or (exc.headers and exc.headers.get("Retry-After"))):
                raise
            time.sleep(2)
    raise AssertionError("Unreachable retry state")


def candidate_kind(citation: dict) -> tuple[str, str] | None:
    types = " ".join((citation.get("pubTypeList") or {}).get("pubType") or []).lower()
    title = (citation.get("title") or "").lower()
    if citation.get("source") == "HIR":
        return "Clinical guideline", "Europe PMC HIR source"
    for term, label in (("practice guideline", "Clinical guideline"),
                        ("guideline", "Clinical guideline"),
                        ("meta-analysis", "Meta-analysis"),
                        ("systematic review", "Systematic review"),
                        ("review", "Review")):
        if term in types:
            return label, "Publication type matched"
    for term, label in (("guideline", "Possible guideline"),
                        ("meta-analysis", "Possible meta-analysis"),
                        ("meta analysis", "Possible meta-analysis"),
                        ("systematic review", "Possible systematic review"),
                        ("consensus", "Possible consensus/review")):
        if term in title:
            return label, "Title keyword only; needs human verification"
    return None


def extract_retractions(data: dict) -> list[tuple[str, str]]:
    items = (data.get("message") or {}).get("items") or []
    if not isinstance(items, list):
        raise ValueError("Crossref items must be a list")
    found = {}
    for work in items:
        if not isinstance(work, dict):
            raise ValueError("Invalid Crossref work")
        for update in (work.get("update-to") or []):
            if not isinstance(update, dict):
                raise ValueError("Invalid Crossref update")
            doi = update.get("DOI")
            if update.get("type") == "retraction" and isinstance(doi, str) and doi.strip():
                found.setdefault(doi.strip().lower(), str(work.get("DOI") or ""))
    return list(found.items())[:MAX_DOIS]


def scan(fetch=get_json, previous=None, now=None) -> tuple[dict, dict]:
    previous = previous or {}
    seen = list(previous.get("seenDois") or [])
    known = set(seen)
    finding_keys = set(previous.get("findingKeys") or [])
    timestamp = now or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    failures = []
    coverage_gaps = []
    findings = []
    checked = 0
    citation_count = 0
    new_processed = []
    try:
        candidates = extract_retractions(fetch(CROSSREF))
    except Exception as exc:
        candidates = []
        failures.append({"stage": "crossref", "reason": str(exc)[:240]})

    for doi, notice_doi in candidates:
        if doi in known:
            continue
        try:
            search_url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
                          + urlencode({"query": 'DOI:"' + doi + '"',
                                       "format": "json", "resultType": "core", "pageSize": 1}))
            results = (fetch(search_url).get("resultList") or {}).get("result") or []
            if not results:
                # Not finding a DOI in Europe PMC is not proof it has no downstream impact.
                coverage_gaps.append({"stage": "not_indexed", "doi": doi,
                                      "reason": "No Europe PMC match; scientific coverage limited; retry later"})
                continue
            record = results[0]
            source, ident = record.get("source"), record.get("id")
            if not source or not ident:
                raise ValueError("Europe PMC record lacks source/id")
            citations_url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/"
                             + quote(str(source), safe="") + "/" + quote(str(ident), safe="")
                             + "/citations?format=json&pageSize=1000")
            response = fetch(citations_url)
            listing = response.get("citationList") or {}
            citations = listing.get("citation") or []
            if not isinstance(citations, list):
                raise ValueError("Malformed Europe PMC citation list")
            hit_count = int(response.get("hitCount") or listing.get("hitCount") or len(citations))
            if hit_count > len(citations):
                raise ValueError("Europe PMC citations truncated; require pagination before marking seen")
            checked += 1
            citation_count += len(citations)
            for citation in citations:
                if not isinstance(citation, dict):
                    continue
                kind = candidate_kind(citation)
                if kind is None or not citation.get("source") or not citation.get("id"):
                    continue
                key = "|".join((doi, str(citation["source"]), str(citation["id"])))
                if key in finding_keys:
                    continue
                finding_keys.add(key)
                findings.append({
                    "retractedDoi": doi,
                    "noticeDoi": notice_doi,
                    "citingSource": str(citation["source"]),
                    "citingId": str(citation["id"]),
                    "citingTitle": str(citation.get("title") or "")[:500],
                    "candidateType": kind[0],
                    "reason": kind[1],
                    "europePmcUrl": ("https://europepmc.org/article/"
                                     + quote(str(citation["source"]), safe="") + "/"
                                     + quote(str(citation["id"]), safe="")),
                    "status": "unreviewed",
                })
            known.add(doi)
            new_processed.append(doi)
        except HTTPError as exc:
            failures.append({"stage": "europepmc_http", "doi": doi,
                             "reason": f"HTTP {exc.code}: Europe PMC metadata lookup unavailable"})
            if exc.code in (429, 502, 503, 504):
                # Shared service pressure/outage: avoid hammering the provider for every DOI.
                # This DOI and all unvisited DOIs stay unmarked and retry on a later run.
                break
            continue
        except Exception as exc:
            failures.append({"stage": "citation_lookup", "doi": doi, "reason": str(exc)[:240]})
            # Crucial: failed DOI is NOT marked seen, so the next run can retry.
            continue

    next_seen = (seen + new_processed)[-600:]
    state = {"schemaVersion": 1, "seenDois": next_seen,
             "findingKeys": sorted(finding_keys)[-3000:], "updatedAt": timestamp}
    report = {
        "schemaVersion": 1, "runAt": timestamp,
        "status": ("failed" if failures and not checked and not new_processed else
                   "partial" if failures else "limited" if coverage_gaps else "ok"),
        "source": "Crossref retraction notices + Europe PMC citation metadata",
        "sourceLimit": {"crossrefRows": 25, "newDoisPerRun": MAX_DOIS,
                        "citationsPerDoi": MAX_CITATIONS},
        "newRetractionsChecked": checked, "citationsExamined": citation_count,
        "candidateFindingsCount": len(findings), "candidateFindings": findings,
        "failuresCount": len(failures), "failures": failures,
        "coverageGapsCount": len(coverage_gaps), "coverageGaps": coverage_gaps,
        "clinicalConclusions": None,
        "notice": ("Triage only. Incomplete citation coverage is possible. "
                   "Candidate citations are not proof that any guideline or review "
                   "relies on invalid evidence. Human source-level validation required."),
        "nativeAppDeployStateSynced": False,
    }
    return report, state


def merge_review_queue(existing: dict, candidates: list[dict], detected_at: str) -> dict:
    items = list(existing.get("items") or [])
    keys = {(f.get("retractedDoi"), f.get("citingSource"), f.get("citingId")) for f in items}
    for finding in candidates:
        key = (finding.get("retractedDoi"), finding.get("citingSource"), finding.get("citingId"))
        if key not in keys:
            items.append({**finding, "detectedAt": detected_at})
            keys.add(key)
    return {"schemaVersion": 1,
            "description": "Unreviewed citation candidates, not verified clinical or misconduct findings",
            "items": items[-500:]}


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    state_path = ROOT / "state.json"
    try:
        previous = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        previous = {}
    report, state = scan(previous=previous)
    queue_path = ROOT / "review-queue.json"
    try:
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        queue = {"schemaVersion": 1, "items": []}
    merged_queue = merge_review_queue(queue, report["candidateFindings"], report["runAt"])
    # Preserve the candidate queue before marking DOIs fully seen.
    queue_path.write_text(json.dumps(merged_queue, indent=2) + "\n", encoding="utf-8")
    # State changes only after successful, fully checked DOI lookups.
    (ROOT / "latest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "newRetractionsChecked": report["newRetractionsChecked"],
                      "candidateFindingsCount": report["candidateFindingsCount"],
                      "failuresCount": report["failuresCount"],
                      "coverageGapsCount": report["coverageGapsCount"]}))


if __name__ == "__main__":
    main()
