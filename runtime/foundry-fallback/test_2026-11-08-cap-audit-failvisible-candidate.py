"""Run after applying the companion review-only patch to scripts/cap_daily_audit.py.

Offline synthetic fixtures only. No NWS HTTP, production mutation, or model calls.
From repo root: python -m unittest -v runtime/foundry-fallback/test_2026-11-08-cap-audit-failvisible-candidate.py
"""
from __future__ import annotations
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2] / 'scripts' / 'cap_daily_audit.py'
spec = importlib.util.spec_from_file_location('hl_cap_candidate', SOURCE)
assert spec and spec.loader
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)

class FakeResponse(io.BytesIO):
    status = 200
    def __enter__(self): return self
    def __exit__(self, *args): self.close()

def fetch(payload, status=200):
    r = FakeResponse(json.dumps(payload).encode('utf-8'))
    r.status = status
    with patch.object(cap, 'urlopen', return_value=r) as mock:
        result = cap.fetch_active_alerts_with_coverage()
        mock.assert_called_once()
        return result

class FailVisibleCAPTests(unittest.TestCase):
    def test_250_valid_records_complete_response(self):
        rows = [{'id': f'urn:test:{i}', 'properties': {'status': 'test'}} for i in range(250)]
        alerts, coverage = fetch({'features': rows})
        self.assertEqual(len(alerts), 250)
        self.assertEqual(coverage['coverageStatus'], 'response_complete')
        self.assertEqual(coverage['recordsNotInspected'], 0)
        self.assertEqual(coverage['sourceRecordsReturned'], 250)

    def test_251st_record_marks_partial(self):
        rows = [{'id': f'urn:test:{i}'} for i in range(251)]
        alerts, coverage = fetch({'features': rows})
        self.assertEqual(len(alerts), 250)
        self.assertEqual(coverage['recordsNotInspected'], 1)
        self.assertEqual(coverage['recordsBeyondLimit'], 1)
        self.assertEqual(coverage['coverageStatus'], 'partial')
        report = cap.build_report(alerts, '2026-11-08T23:00:00Z', coverage)
        self.assertEqual(report['coverageStatus'], 'partial')
        self.assertEqual(report['alertsChecked'], 250)
        self.assertEqual(report['sourceRecordsReturned'], 251)

    def test_missing_features_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'feature list'):
            fetch({'type': 'FeatureCollection'})

    def test_null_features_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'feature list'):
            fetch({'features': None})

    def test_non_object_top_level_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'feature list'):
            fetch([{'id': 'x'}])

    def test_invalid_records_counted_even_beyond_cap(self):
        rows = [{'id': f'urn:test:{i}'} for i in range(250)] + [None]
        alerts, coverage = fetch({'features': rows})
        self.assertEqual(len(alerts), 250)
        self.assertEqual(coverage['invalidSourceRecords'], 1)
        self.assertEqual(coverage['recordsNotInspected'], 1)
        self.assertEqual(coverage['coverageStatus'], 'partial')

    def test_invalid_within_cap_does_not_fake_full_scan(self):
        alerts, coverage = fetch({'features': [{'id': 'one'}, 'invalid', {'id': 'two'}]})
        self.assertEqual([x['id'] for x in alerts], ['one', 'two'])
        self.assertEqual(coverage['invalidSourceRecords'], 1)
        self.assertEqual(coverage['recordsNotInspected'], 1)
        self.assertEqual(coverage['coverageStatus'], 'partial')

    def test_next_page_marked_partial_even_with_short_response(self):
        _, coverage = fetch({'features': [{'id': 'one'}], 'pagination': {'next': 'https://api.weather.gov/alerts?cursor=example'}})
        self.assertTrue(coverage['hasNextPage'])
        self.assertEqual(coverage['coverageStatus'], 'partial')

    def test_empty_list_is_valid_response(self):
        alerts, coverage = fetch({'features': []})
        self.assertEqual(alerts, [])
        self.assertEqual(coverage['coverageStatus'], 'response_complete')

    def test_non_200_http_fails(self):
        with self.assertRaisesRegex(RuntimeError, '503'):
            fetch({'features': []}, status=503)

    def test_findings_limit_is_reported(self):
        rows = [{'id': f'urn:test:{i}', 'properties': {}} for i in range(150)]
        report = cap.build_report(rows, '2026-11-08T23:00:00Z', {'coverageStatus': 'response_complete'})
        self.assertEqual(report['findingsCount'], cap.MAX_FINDINGS)
        self.assertGreater(report['findingsGenerated'], cap.MAX_FINDINGS)
        self.assertEqual(report['findingsNotReported'], report['findingsGenerated'] - cap.MAX_FINDINGS)

    def test_legacy_list_only_signature_preserved(self):
        with patch.object(cap, 'urlopen', return_value=FakeResponse(b'{"features":[{"id":"x"}]}')):
            self.assertEqual(cap.fetch_active_alerts(), [{'id': 'x'}])

    def test_write_report_preserves_existing_schema_and_coverage(self):
        report = cap.build_report([], '2026-11-08T23:00:00Z', {'coverageStatus': 'partial', 'sourceRecordsReturned': 251, 'recordsNotInspected': 1})
        with tempfile.TemporaryDirectory() as tmp:
            latest, archive = cap.write_report(report, Path(tmp))
            self.assertTrue(archive.exists())
            data = json.loads(latest.read_text())
            self.assertEqual(data['schemaVersion'], 1)
            self.assertEqual(data['coverageStatus'], 'partial')
            self.assertEqual(data['recordsNotInspected'], 1)

if __name__ == '__main__': unittest.main()
