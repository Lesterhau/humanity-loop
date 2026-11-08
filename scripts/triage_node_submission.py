#!/usr/bin/env python3
"""Fail-closed, OFFLINE pre-review triage for a Humanity Loop node submission.

Triage is not acceptance, identity verification, independent source checking,
legal/health/policy review, or a database action. This script never connects
to Supabase or the internet and deliberately omits source/secret content from
its JSON report. Do not commit raw participant submissions to this repository.
"""
import argparse
import ipaddress
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qsl, urlsplit
from uuid import UUID


SECRET_PATTERN = re.compile(
    r"(?i)\b(?:bearer\s+[a-z0-9_.-]{16,}|sk-[a-z0-9_-]{12,}|"
    r"(?:password|api[_-]?key|node[_-]?token|access[_-]?token)"
    r"\s*[:=]\s*[^\s,;\"'}]{8,})"
)
EMAIL_PATTERN = re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")
SENSITIVE_QUERY_KEYS = {
    "access_token", "api_key", "apikey", "authorization", "auth",
    "bearer", "password", "secret", "session", "token",
}


def _valid_uuid(value):
    if not isinstance(value, str):
        return False
    try:
        return bool(UUID(value))
    except (ValueError, AttributeError):
        return False


def _url_flags(url):
    """Return fixed safety reason codes; NEVER return source URL or query values."""
    flags = []
    if not isinstance(url, str) or len(url) > 2048:
        return ["invalid_source_url"]
    try:
        parts = urlsplit(url)
    except ValueError:
        return ["invalid_source_url"]
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        return ["invalid_source_url"]
    if parts.username or parts.password:
        flags.append("credentials_in_source_url")
    hostname = parts.hostname.lower()
    if hostname in {"localhost", "host.docker.internal"} or hostname.endswith(
        (".local", ".internal", ".localhost", ".test", ".invalid")
    ):
        flags.append("nonpublic_source_url")
    try:
        ip = ipaddress.ip_address(hostname)
        if not ip.is_global:
            flags.append("nonpublic_source_url")
    except ValueError:
        pass
    try:
        query_keys = {k.lower() for k, _ in parse_qsl(parts.query, keep_blank_values=True)}
    except ValueError:
        flags.append("invalid_source_url")
    else:
        if query_keys & SENSITIVE_QUERY_KEYS:
            flags.append("sensitive_query_in_source_url")
    return flags


def triage(record, *, trusted_risk_tier=None):
    """Return reason-code-only triage; never mark a contribution accepted."""
    blockers, warnings = set(), set()
    if not isinstance(record, dict):
        return {"status": "human_review_required", "accepted": False,
                "blockers": ["invalid_record_structure"], "warnings": []}

    if record.get("status") != "quarantined":
        blockers.add("not_quarantined")
    for field in ("submission_id", "node_id", "work_id"):
        if not _valid_uuid(record.get(field)):
            blockers.add(f"missing_or_invalid_{field}")
    if not isinstance(record.get("result"), dict) or not record["result"]:
        blockers.add("missing_structured_result")
    if trusted_risk_tier is None:
        warnings.add("risk_tier_not_verified")
    elif trusted_risk_tier != 0:
        blockers.add("outside_tier0_review_scope")

    evidence = record.get("evidence")
    source_urls = []
    if not isinstance(evidence, list) or not evidence:
        warnings.add("no_evidence_objects")
    else:
        for item in evidence[:50]:
            if isinstance(item, str):
                source_urls.append(item)
            elif isinstance(item, dict):
                for key in ("url", "source_url", "final_url"):
                    if key in item:
                        source_urls.append(item[key])
            else:
                warnings.add("unstructured_evidence_item")
        if len(evidence) > 50:
            warnings.add("evidence_truncated_for_triage")
    if not source_urls:
        warnings.add("no_source_urls")
    for url in source_urls:
        for issue in _url_flags(url):
            blockers.add(issue)

    data_as_text = json.dumps(record, ensure_ascii=False, default=str)
    if SECRET_PATTERN.search(data_as_text):
        blockers.add("possible_secret_in_submission")
    if EMAIL_PATTERN.search(data_as_text):
        warnings.add("possible_personal_data_review")
    if not isinstance(record.get("uncertainty"), str) or not record["uncertainty"].strip():
        warnings.add("uncertainty_not_explained")

    # Never accept evidence just because it parses. Access/auth, task validity,
    # independent content confirmation, and actual reviewer identity require
    # separate privileged/human checks that this tool cannot perform.
    warnings.update({
        "claim_and_lease_not_verified",
        "source_content_not_independently_verified",
        "reviewer_independence_not_verified",
    })
    return {
        "status": "human_review_required",
        "accepted": False,
        "blockers": sorted(blockers),
        "warnings": sorted(warnings),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Local private redacted submission JSON path or '-' for stdin")
    parser.add_argument("--trusted-risk-tier", type=int, choices=[0, 1, 2, 3],
                        default=None, help="Risk tier independently read from trusted work ledger")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        record = json.loads(raw)
    except (OSError, ValueError, UnicodeError) as exc:
        # No exception message: file paths and raw inputs may contain secrets.
        print(json.dumps({"status": "human_review_required", "accepted": False,
                          "blockers": ["input_unavailable_or_invalid_json"], "warnings": []}))
        return 2
    print(json.dumps(triage(record, trusted_risk_tier=args.trusted_risk_tier), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
