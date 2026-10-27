#!/usr/bin/env python3
"""Offline regressions for the credit-free Evidence Integrity metadata backup."""
import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from evidence_integrity_backup import candidate_kind, extract_retractions, scan, merge_review_queue, get_json, CROSSREF


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

    def test_seen_crossref_prefix_does_not_hide_unseen_doi(self):
        # Crossref returns 25 rows, but the first 16 may already be recorded.
        works = []
        for i in range(17):
            works.append({"DOI": f"10.1000/notice-{i}", "update-to": [
                {"DOI": f"10.1000/original-{i}", "type": "retraction"}]})
        previous = {"seenDois": [f"10.1000/original-{i}" for i in range(16)]}
        report, state = scan(
            fetch=lookup(crossref={"message": {"items": works}}),
            previous=previous, now="2026-10-27T23:00:00Z")
        self.assertEqual(report["newRetractionsChecked"], 1)
        self.assertEqual(report["candidateFindingsCount"], 1)
        self.assertIn("10.1000/original-16", state["seenDois"])

    def test_limit_counts_unseen_attempts_not_total_crossref_rows(self):
        works = []
        for i in range(18):
            works.append({"DOI": f"10.1000/notice-{i}", "update-to": [
                {"DOI": f"10.1000/original-{i}", "type": "retraction"}]})
        previous = {"seenDois": ["10.1000/original-0", "10.1000/original-1"]}
        report, state = scan(
            fetch=lookup(crossref={"message": {"items": works}}),
            previous=previous, now="2026-10-27T23:00:00Z")
        self.assertEqual(report["newRetractionsChecked"], 15)
        self.assertEqual(report["candidateFindingsCount"], 15)
        self.assertIn("10.1000/original-16", state["seenDois"])
        self.assertNotIn("10.1000/original-17", state["seenDois"])

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

    def test_upstream_503_stops_batch_and_preserves_unchecked_dois(self):
        two_retractions = {"message": {"items": [
            {"DOI": "10.1000/notice-one", "update-to": [
                {"DOI": "10.1000/retracted-one", "type": "retraction"}]},
            {"DOI": "10.1000/notice-two", "update-to": [
                {"DOI": "10.1000/retracted-two", "type": "retraction"}]},
        ]}}
        requests = []

        def unavailable(url):
            requests.append(url)
            if url == CROSSREF:
                return two_retractions
            raise HTTPError(url, 503, "Service Unavailable", None, None)

        report, state = scan(fetch=unavailable, now="2026-10-24T12:00:00Z")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["failuresCount"], 1)
        self.assertEqual(report["failures"][0]["stage"], "europepmc_http")
        self.assertEqual(len(requests), 2)  # One Crossref call, only one Europe PMC call.
        self.assertEqual(state["seenDois"], [])
        self.assertEqual(report["candidateFindingsCount"], 0)

    def test_transient_503_retries_once_and_recovers(self):
        url = "https://example.org/metadata"
        transient = HTTPError(url, 503, "Service Unavailable", None, None)
        with patch("evidence_integrity_backup.urlopen",
                   side_effect=[transient, io.BytesIO(b'{"ok": true}')]) as fetch, \
             patch("evidence_integrity_backup.time.sleep") as sleep:
            self.assertEqual(get_json(url), {"ok": True})
        self.assertEqual(fetch.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_persistent_503_stops_after_one_retry(self):
        url = "https://example.org/metadata"
        transient = HTTPError(url, 503, "Service Unavailable", None, None)
        with patch("evidence_integrity_backup.urlopen", side_effect=transient) as fetch, \
             patch("evidence_integrity_backup.time.sleep") as sleep:
            with self.assertRaises(HTTPError):
                get_json(url)
        self.assertEqual(fetch.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_429_is_not_retried(self):
        url = "https://example.org/metadata"
        limited = HTTPError(url, 429, "Too Many Requests", None, None)
        with patch("evidence_integrity_backup.urlopen", side_effect=limited) as fetch, \
             patch("evidence_integrity_backup.time.sleep") as sleep:
            with self.assertRaises(HTTPError):
                get_json(url)
        self.assertEqual(fetch.call_count, 1)
        sleep.assert_not_called()

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
