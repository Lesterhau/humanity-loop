#!/usr/bin/env python3
"""Offline regressions for the credit-free Evidence Integrity metadata backup."""
import unittest

from evidence_integrity_backup import candidate_kind, extract_retractions, scan, merge_review_queue, CROSSREF


RETRACTION = {
    "message": {"items": [
        {"DOI": "10.1000/retraction-notice", "update-to": [
            {"DOI": "10.1000/retracted-original", "type": "retraction"}]}
    ]}
}
ARTICLE = {"resultList": {"result": [{"source": "MED", "id": "1234", "title": "Retracted article"}]}}
CITATIONS = {
    "hitCount": 1,
    "citationList": {"citation": [
        {"source": "MED", "id": "5678",
         "title": "Systematic review of a question",
         "pubTypeList": {"pubType": ["Systematic Review"]}}
    ]}
}


def lookup(*, crossref=RETRACTION, article=ARTICLE, citations=CITATIONS, failure=None):
    def fetch(url):
        if url == CROSSREF:
            return crossref
        if "/rest/search?" in url:
            if failure == "search":
                raise RuntimeError("Europe PMC temporary unavailable")
            return article
        if "/citations?" in url:
            if failure == "citations":
                raise RuntimeError("Europe PMC timeout")
            return citations
        raise AssertionError("Unexpected lookup: " + url)
    return fetch


class EvidenceIntegrityBackupTests(unittest.TestCase):
    def test_extract_only_explicit_retraction_relationship(self):
        items = {"message": {"items": [
            {"DOI": "10.1000/notice", "update-to": [
                {"type": "correction", "DOI": "10.1000/ignored"},
                {"type": "retraction", "DOI": "10.1000/RETRACTED"},
                {"type": "retraction", "DOI": "10.1000/retracted"}]}
        ]}}
        self.assertEqual(extract_retractions(items), [("10.1000/retracted", "10.1000/notice")])

    def test_real_candidate_is_triage_only(self):
        report, state = scan(fetch=lookup(), now="2026-10-20T20:00:00Z")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["candidateFindingsCount"], 1)
        self.assertEqual(report["candidateFindings"][0]["status"], "unreviewed")
        self.assertIsNone(report["clinicalConclusions"])
        self.assertFalse(report["nativeAppDeployStateSynced"])
        self.assertIn("10.1000/retracted-original", state["seenDois"])

    def test_same_doi_is_deduplicated(self):
        _, state = scan(fetch=lookup(), now="2026-10-20T20:00:00Z")
        report, again = scan(fetch=lookup(), previous=state, now="2026-10-21T20:00:00Z")
        self.assertEqual(report["candidateFindingsCount"], 0)
        self.assertEqual(report["newRetractionsChecked"], 0)
        self.assertEqual(again["seenDois"], state["seenDois"])

    def test_citation_failure_not_marked_seen_and_is_retryable(self):
        failed, prior = scan(fetch=lookup(failure="citations"))
        self.assertGreater(failed["failuresCount"], 0)
        self.assertEqual(prior["seenDois"], [])
        recovered, state = scan(fetch=lookup(), previous=prior)
        self.assertEqual(recovered["status"], "ok")
        self.assertEqual(recovered["candidateFindingsCount"], 1)
        self.assertEqual(len(state["seenDois"]), 1)

    def test_unindexed_doi_retries_without_falsely_claiming_source_failure(self):
        report, state = scan(fetch=lookup(article={"resultList": {"result": []}}))
        self.assertEqual(report["status"], "limited")
        self.assertEqual(report["failuresCount"], 0)
        self.assertEqual(report["coverageGapsCount"], 1)
        self.assertEqual(report["coverageGaps"][0]["stage"], "not_indexed")
        self.assertEqual(state["seenDois"], [])

    def test_truncated_citation_response_retries(self):
        truncated = dict(CITATIONS)
        truncated["hitCount"] = 1400
        report, state = scan(fetch=lookup(citations=truncated))
        self.assertEqual(report["candidateFindingsCount"], 0)
        self.assertEqual(state["seenDois"], [])
        self.assertGreater(report["failuresCount"], 0)

    def test_no_retractions_is_not_fabricated_failure(self):
        report, state = scan(fetch=lookup(crossref={"message": {"items": []}}))
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["failuresCount"], 0)
        self.assertEqual(state["seenDois"], [])

    def test_crossref_failure_preserves_previous_state(self):
        def no_connection(_):
            raise RuntimeError("Crossref temporarily unavailable")
        old = {"seenDois": ["10.1000/old"], "findingKeys": ["10.1000/old|MED|42"]}
        report, state = scan(fetch=no_connection, previous=old)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(state["seenDois"], old["seenDois"])
        self.assertEqual(state["findingKeys"], old["findingKeys"])

    def test_publication_types_and_titles_are_leads_only(self):
        self.assertEqual(candidate_kind({"title": "Practice guideline", "source": "MED"})[0],
                         "Possible guideline")
        self.assertEqual(candidate_kind({"title": "Something else", "source": "MED",
                                         "pubTypeList": {"pubType": ["Meta-Analysis"]}})[0],
                         "Meta-analysis")
        self.assertIsNone(candidate_kind({"title": "Research article", "source": "MED"}))



    def test_review_queue_retains_existing_leads_and_owner_review_status(self):
        original={"schemaVersion":1,"items":[{"retractedDoi":"10.1000/old","citingSource":"MED","citingId":"42","status":"under-review"}]}
        candidate={"retractedDoi":"10.1000/new","citingSource":"MED","citingId":"7","status":"unreviewed"}
        a=merge_review_queue(original,[candidate],"2026-10-20T22:00:00Z")
        b=merge_review_queue(a,[candidate],"2026-10-21T22:00:00Z")
        self.assertEqual(len(a["items"]),2)
        self.assertEqual(len(b["items"]),2)
        self.assertEqual(b["items"][0]["status"],"under-review")
        self.assertEqual(b["items"][1]["detectedAt"],"2026-10-20T22:00:00Z")


if __name__ == "__main__":
    unittest.main()
