#!/usr/bin/env python3
"""Offline, privacy-minimal pre-review of ONE human-assisted public-page report.

This is *not* an independent review, acceptance, identity attestation, legal
assessment, consent grant, government contact, or write to a production ledger.
Use only a privately prepared, redacted summary; never feed it raw email.
No network calls, telemetry, persistent files, or third-party libraries.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from triage_node_submission import _url_flags, SECRET_PATTERN, EMAIL_PATTERN

MAX_INPUT_BYTES = 32_768
ALLOWED_OUTCOMES = {"no_issue_found", "possible_issue", "unable_to_verify"}
ALLOWED_WEB_ACCESS = {"live", "limited", "blocked", "not_used", "unknown"}
ALLOWED_TRUSTED_ORIGINS = {"owner_test", "outside_email", "unknown"}
ALLOWED_SOURCE_CHECKS = {"independently_checked", "not_checked", "conflicting"}
ALLOWED_FIELDS = {
    "task_type", "outcome", "human_checked", "source_urls",
    "observation", "limitations", "web_access", "source_check",
}


def triage(record: object, *, trusted_origin: str = "unknown") -> dict:
    """Return fixed reason codes only, never the report or sender details."""
    blockers: set[str] = set()
    warnings: set[str] = set()
    if trusted_origin not in ALLOWED_TRUSTED_ORIGINS:
        blockers.add("invalid_trusted_origin")
        trusted_origin = "unknown"

    if not isinstance(record, dict):
        blockers.add("invalid_record")
        record = {}

    extras = set(record) - ALLOWED_FIELDS
    if extras:
        warnings.add("unexpected_or_private_fields_not_used")
    if "email" in record or "sender" in record or "origin" in record:
        warnings.add("sender_provenance_must_be_checked_privately")

    if record.get("task_type") != "public_page_check":
        blockers.add("wrong_task_type")
    outcome = record.get("outcome")
    if not isinstance(outcome, str) or outcome not in ALLOWED_OUTCOMES:
        blockers.add("invalid_outcome")
    human_checked = record.get("human_checked")
    if not isinstance(human_checked, bool):
        blockers.add("human_check_flag_required")
        human_checked = False
    web_access = record.get("web_access")
    if not isinstance(web_access, str) or web_access not in ALLOWED_WEB_ACCESS:
        warnings.add("web_access_not_classified")
    source_check = record.get("source_check", "not_checked")
    if not isinstance(source_check, str) or source_check not in ALLOWED_SOURCE_CHECKS:
        blockers.add("source_check_invalid")
        source_check = "not_checked"

    sources = record.get("source_urls")
    if not isinstance(sources, list) or not (1 <= len(sources) <= 10):
        blockers.add("source_urls_missing_or_too_many")
        sources = []
    for item in sources:
        for flag in _url_flags(item):
            blockers.add(flag)
    observation = record.get("observation")
    if not isinstance(observation, str) or not observation.strip() or len(observation) > 2500:
        blockers.add("observation_missing_or_oversized")
    limitations = record.get("limitations")
    if not isinstance(limitations, str) or not limitations.strip() or len(limitations) > 2500:
        warnings.add("limitations_missing_or_oversized")

    # The raw JSON is inspected only in local memory; the output never embeds it.
    try:
        raw = json.dumps(record, ensure_ascii=False, default=str)
    except (TypeError, ValueError, OverflowError):
        blockers.add("unserializable_report")
        raw = ""
    if SECRET_PATTERN.search(raw):
        blockers.add("possible_secret_present")
    if EMAIL_PATTERN.search(raw):
        warnings.add("possible_personal_data_present")

    if outcome == "possible_issue":
        if not human_checked:
            blockers.add("human_confirmation_missing_for_issue")
        if source_check != "independently_checked":
            warnings.add("independent_source_review_required")
    elif outcome == "no_issue_found":
        if not human_checked:
            warnings.add("negative_finding_not_human_checked")
    elif outcome == "unable_to_verify":
        warnings.add("inconclusive_test_not_a_source_defect")
        if human_checked:
            warnings.add("unable_outcome_conflicts_with_human_check")

    if web_access in {"limited", "blocked"}:
        warnings.add("model_access_limitation_not_public_site_failure")
    if source_check == "conflicting":
        blockers.add("source_conflict_needs_manual_resolution")
    if trusted_origin == "owner_test":
        warnings.add("owner_test_not_independent_participant")
    elif trusted_origin == "outside_email":
        warnings.add("email_origin_not_authenticated_identity")
    else:
        warnings.add("report_origin_unverified")

    warnings.update({
        "reviewer_independence_not_verified",
        "real_world_adoption_not_verified",
    })
    return {
        "status": "human_review_required",
        "accepted": False,
        "registered_node": False,
        "public_benefit_verified": False,
        "origin_class": trusted_origin,
        "outcome_class": outcome if isinstance(outcome, str) and outcome in ALLOWED_OUTCOMES else "invalid",
        "blockers": sorted(blockers),
        "warnings": sorted(warnings),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Private redacted JSON file path, or '-' for stdin")
    parser.add_argument(
        "--trusted-origin", choices=sorted(ALLOWED_TRUSTED_ORIGINS),
        default="unknown",
        help="Operator-checked inbox provenance, NEVER a user-submitted JSON field",
    )
    args = parser.parse_args(argv)
    try:
        if args.input == "-":
            raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        else:
            with open(args.input, "rb") as file:
                raw = file.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("size cap exceeded")
        record = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({
            "status": "human_review_required", "accepted": False,
            "registered_node": False, "public_benefit_verified": False,
            "origin_class": "unknown", "outcome_class": "invalid",
            "blockers": ["input_unavailable_invalid_or_oversized"], "warnings": []
        }, sort_keys=True))
        return 2
    print(json.dumps(triage(record, trusted_origin=args.trusted_origin), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
