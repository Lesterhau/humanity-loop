#!/usr/bin/env python3
"""Offline G3 handoff: archived official HTML snapshot -> unreviewed Foundry packet.

This creates a source-bound *candidate*, never an independent attestation.
Only the previously reviewed OT-013 Pakistan case is supported. No network,
model inference, credentials, external writes or scheduler.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import json
from pathlib import Path
import re
import sys
from typing import Any

from foundry_lite import validate_task
from foundry_source_evidence import validate_source_packet
from public_source_snapshot import ALLOWED_CASE_URLS, MAX_BYTES

MAX_INPUT_BYTES = 16_000
REVIEW_QUESTIONS = (
    "On the original official public page, is the compounding count still 103, and does it refer to the same cohort as the later district narrative?",
    "On the original official public page, do the district narrative and associated chart still use 117 and 81.6, and what is the correct underlying cohort?"
)


def make_review_candidate(snapshot: Any, raw_task: Any,
                          *, now: datetime | None = None) -> dict[str, Any]:
    task = validate_task(raw_task)
    if not isinstance(snapshot,dict) or snapshot.get("schema_version") != 1:
        raise ValueError("invalid_snapshot")
    case=task.get("case_id")
    if case != "OT-013" or case not in ALLOWED_CASE_URLS:
        raise ValueError("handoff_case_not_approved")
    source=ALLOWED_CASE_URLS[case]
    if (task.get("country"),task.get("languages"),task.get("public_source_urls")) != ("PK",["en"],[source]):
        raise ValueError("handoff_task_context_mismatch")
    if (snapshot.get("case_id"),snapshot.get("country"),snapshot.get("languages"),
            snapshot.get("source_url")) != ("OT-013","PK",["en"],source):
        raise ValueError("handoff_snapshot_context_mismatch")
    if (snapshot.get("record_type") != "direct_public_html_snapshot" or
            snapshot.get("retrieval_method") != "one_explicit_direct_https_get" or
            snapshot.get("http_status") != 200 or
            snapshot.get("content_type") != "text/html"):
        raise ValueError("handoff_unrecognized_retrieval")
    digest=snapshot.get("raw_sha256")
    if not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest):
        raise ValueError("handoff_digest_invalid")
    size=snapshot.get("raw_bytes")
    if type(size) is not int or not 0 < size <= MAX_BYTES:
        raise ValueError("handoff_snapshot_size_invalid")
    for key,expected in [
        ("independently_reviewed",False),
        ("confirmed_public_correction",False),
        ("eligible_for_win_ledger",False),
        ("scheduled",False),
        ("external_write_actions",0),
        ("model_calls",0),
        ("appdeploy_credits_used",0),
    ]:
        if type(snapshot.get(key)) is not type(expected) or snapshot.get(key)!=expected:
            raise ValueError("handoff_must_be_unreviewed_read_only")
    timestamp=snapshot.get("observed_at_utc")
    if not isinstance(timestamp,str):
        raise ValueError("handoff_timestamp_invalid")
    try:
        observed=datetime.fromisoformat(timestamp.replace("Z","+00:00"))
    except ValueError as exc:
        raise ValueError("handoff_timestamp_invalid") from exc
    now=now or datetime.now(timezone.utc)
    if observed.tzinfo is None or observed.utcoffset()!=timezone.utc.utcoffset(observed) or observed>now:
        raise ValueError("handoff_timestamp_invalid")
    indicators=snapshot.get("indicators")
    if not isinstance(indicators,dict):
        raise ValueError("handoff_indicators_missing")
    observations=[]
    for key,question in zip(("headline_103","narrative_117"),REVIEW_QUESTIONS):
        item=indicators.get(key)
        if not isinstance(item,dict) or item.get("observed_in_visible_html") is not True:
            raise ValueError("handoff_required_text_unobserved")
        excerpt=item.get("source_excerpt")
        if not isinstance(excerpt,str) or not 10 <= len(excerpt) <= 240:
            raise ValueError("handoff_source_excerpt_invalid")
        observations.append({
            "source_url":source, "observed_at_utc":timestamp,
            "method":"public_text_retrieval","language":"en",
            "status":"candidate","excerpt":excerpt,"review_question":question
        })
    arithmetic=snapshot.get("arithmetic")
    if not isinstance(arithmetic,dict) or arithmetic.get("arithmetic_discrepancy_candidate") is not True:
        raise ValueError("handoff_no_arithmetic_discrepancy")
    if arithmetic.get("underlying_cohort_truth_verified") is not False:
        raise ValueError("handoff_underlying_truth_not_known")
    try:
        part,whole,claimed,computed=[
            Decimal(str(arithmetic[k])) for k in (
                "numerator","denominator","source_claim_percent","computed_percent_1dp"
            )
        ]
    except (InvalidOperation,KeyError,ValueError) as exc:
        raise ValueError("handoff_invalid_arithmetic") from exc
    if any(not v.is_finite() for v in (part,whole,claimed,computed)) or whole<=0:
        raise ValueError("handoff_invalid_arithmetic")
    expected=(part*100/whole).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
    if expected!=computed or abs(expected-claimed)<=Decimal("0.1"):
        raise ValueError("handoff_invalid_arithmetic")
    candidate={
        "schema_version":1,"task_id":task["task_id"],"case_id":case,
        "country":"PK","languages":["en"],"tier":0,
        "external_actions":False,"consent_to_publish":False,
        "review_state":"pending_independent_review",
        "fixture_only":False,
        "observations":observations,
        "arithmetic_checks":[{
            "kind":"percentage","source_index":1,
            "part":str(part),"whole":str(whole),"claimed_percent":str(claimed)
        }],
    }
    # This is intentionally STILL operator-submitted unverified context.
    validate_source_packet(candidate,task,now=now)
    return candidate


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task",required=True)
    parser.add_argument("--snapshot",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    try:
        source=Path(args.snapshot);task=Path(args.task);dest=Path(args.output)
        if dest.is_symlink() or dest.exists():
            raise ValueError("handoff_output_exists_or_symlink")
        if source.stat().st_size>MAX_INPUT_BYTES or task.stat().st_size>MAX_INPUT_BYTES:
            raise ValueError("handoff_input_too_large")
        packet=make_review_candidate(json.loads(source.read_text(encoding="utf-8")),
                                     json.loads(task.read_text(encoding="utf-8")))
        with dest.open("x",encoding="utf-8") as out:
            out.write(json.dumps(packet,indent=2,ensure_ascii=False)+"\n")
        print(json.dumps({
            "status":"source_candidate_pending_independent_review",
            "case_id":packet["case_id"],"observations":len(packet["observations"]),
            "model_calls":0,"external_actions":0,"independently_verified":False,
            "output":str(dest)
        }))
        return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        # Never print raw source snippets or internal host response text.
        reason=str(exc) if isinstance(exc,ValueError) and str(exc).startswith("handoff_") else "input_or_local_output_invalid"
        print("SOURCE HANDOFF BLOCKED: "+reason,file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
