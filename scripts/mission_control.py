#!/usr/bin/env python3
"""Humanity Loop outcome-first mission gate.

Offline, read-only selector. Rejects invented win counts and gates. Produces ONE
due public-source check, not a new schedule or autonomous external write.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlsplit

MILESTONES = ("G1", "G2", "G3", "G4", "G5")
STATES = {"active", "not_started", "blocked", "achieved"}
CASE_STATES = {"pending_external_publication", "ready_for_review", "closed"}
REQUIRED_ROLES = ("source_url", "next_due_utc", "next_action", "id", "last_contact_utc")


def utc_date(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp_not_string")
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid_timestamp") from exc
    if date.tzinfo is None or date.utcoffset() != timezone.utc.utcoffset(date):
        raise ValueError("timestamp_not_utc")
    return date


def ledger_win_ids(text: str) -> list[str]:
    return re.findall(r"^## (WIN-\d{3,})\b", text, flags=re.MULTILINE)


def validate_and_select(config: dict[str, Any], win_ledger: str,
                        *, now: datetime) -> dict[str, Any]:
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError("unrecognized_schema")
    if now.tzinfo is None:
        raise ValueError("naive_now_forbidden")
    utc_date(config.get("updated_utc"))
    end = config.get("end_state")
    if not isinstance(end, dict) or not isinstance(end.get("acceptance"), dict):
        raise ValueError("missing_end_state")
    acceptance = end["acceptance"]
    for attr in ("verified_outcomes_per_rolling_28_days",
                 "independently_checked_regions", "reviewed_languages",
                 "consecutive_days_operating_without_owner_manual_steps"):
        if type(acceptance.get(attr)) is not int or acceptance[attr] < 1:
            raise ValueError("invalid_finish_line")
    if acceptance.get("unapproved_spend_usd") != 0 or acceptance.get("unapproved_high_risk_actions") != 0:
        raise ValueError("safety_budget_floor_relaxed")
    baseline = config.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("ledger") != "WIN-LEDGER.md":
        raise ValueError("missing_baseline_ledger")
    utc_date(baseline.get("verified_at_utc"))
    wins = ledger_win_ids(win_ledger)
    if len(wins) != len(set(wins)):
        raise ValueError("duplicate_win_id")
    if type(baseline.get("verified_outcomes")) is not int or baseline["verified_outcomes"] != len(wins):
        raise ValueError("win_count_mismatch")
    stages = config.get("milestones")
    if not isinstance(stages, list) or [x.get("id") for x in stages if isinstance(x, dict)] != list(MILESTONES):
        raise ValueError("milestone_sequence_invalid")
    active = [x for x in stages if x.get("status") == "active"]
    if len(active) != 1:
        raise ValueError("require_one_active_gate")
    achieved = set()
    for index, stage in enumerate(stages):
        if stage.get("status") not in STATES:
            raise ValueError("invalid_gate_state")
        if stage.get("prerequisites") != ([] if index == 0 else [stages[index-1]["id"]]):
            raise ValueError("broken_prerequisite_chain")
        if stage.get("independent_volunteer_required") is not False:
            raise ValueError("external_volunteer_is_blocking")
        if stage.get("status") == "achieved":
            if not isinstance(stage.get("proof_urls"), list) or not stage["proof_urls"]:
                raise ValueError("achieved_gate_missing_proof")
            if set(stage["prerequisites"]) - achieved:
                raise ValueError("achieved_without_prerequisite")
            if stage["id"] == "G1" and len(wins) < stage.get("target_outcomes", 10**6):
                raise ValueError("outcome_gate_without_external_win")
            achieved.add(stage["id"])
        if stage.get("status") == "active" and set(stage["prerequisites"]) - achieved:
            raise ValueError("active_gate_before_prerequisite")
    # Development work can happen in parallel; RELEASE acceptance remains sequential.
    # Treat readiness as independently testable artifacts, not achieved outcome gates.
    parallel_readiness = []
    for stage in stages[2:]:
        dev = stage.get("development")
        if not isinstance(dev, dict):
            raise ValueError("parallel_development_missing")
        if dev.get("status") not in {"not_started", "scoped", "in_progress", "ready_for_acceptance_review"}:
            raise ValueError("invalid_development_state")
        if dev.get("release_claimed") is not False:
            raise ValueError("premature_release_claim")
        artifacts = dev.get("evidence_artifacts")
        if not isinstance(artifacts, list) or not artifacts or any(
            not isinstance(x, str) or not x or x.startswith("/") or ".." in x.split("/")
            for x in artifacts
        ):
            raise ValueError("invalid_development_artifacts")
        if not isinstance(dev.get("next_verifiable_result"), str) or len(dev["next_verifiable_result"]) < 20:
            raise ValueError("development_has_no_next_test")
        if stage["id"] == "G3" and dev.get("complete_eight_stage_model_runs_independently_reviewed") != 0:
            raise ValueError("invented_model_acceptance")
        if stage["id"] == "G4" and dev.get("independently_verified_non_us_outcomes") != 0:
            raise ValueError("invented_international_outcome")
        if stage["id"] == "G5" and dev.get("acceptance_metrics_all_met") is not False:
            raise ValueError("invented_global_readiness")
        parallel_readiness.append({
            "gate": stage["id"], "gate_status": stage["status"],
            "development_status": dev["status"],
            "artifact_count_not_an_outcome": len(artifacts),
            "next_test": dev["next_verifiable_result"],
            "release_accepted": stage["status"] == "achieved",
        })
    policy = config.get("operating_rules", {}).get("parallel_track_policy")
    if not isinstance(policy, dict) or policy.get("development_is_allowed_before_prerequisites") is not True:
        raise ValueError("parallel_build_policy_missing")
    if policy.get("release_gate_completion_still_requires_prerequisites") is not True:
        raise ValueError("gate_precedence_bypassed")
    if policy.get("allowed_parallel_tracks") != ["G3", "G4", "G5"]:
        raise ValueError("parallel_track_scope_changed")
    if policy.get("no_new_scheduled_workers") is not True:
        raise ValueError("new_schedulers_not_authorized")
    rules = config.get("operating_rules")
    if not isinstance(rules, dict) or rules.get("wip_case_limit") != 2:
        raise ValueError("wip_limit_changed_without_review")
    if rules.get("independent_volunteer_blocking") is not False:
        raise ValueError("dependency_on_volunteer")
    if rules.get("routine_external_contact") is None:
        raise ValueError("contact_boundary_missing")
    cases = config.get("focus_cases")
    if not isinstance(cases, list) or len(cases) > 2 or len(cases) < 1:
        raise ValueError("invalid_case_wip")
    ids = []
    runnable = []
    future = []
    for case in cases:
        if not isinstance(case, dict) or any(k not in case for k in REQUIRED_ROLES):
            raise ValueError("case_missing_field")
        if not isinstance(case["id"], str) or not re.fullmatch(r"OT-\d{3}",case["id"]):
            raise ValueError("invalid_case_id")
        ids.append(case["id"])
        if case.get("status") not in CASE_STATES:
            raise ValueError("invalid_case_state")
        url = urlsplit(case["source_url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("unsafe_public_source")
        if case.get("do_not_count_as_win") is not True:
            raise ValueError("unverified_case_claimed_as_win")
        if case.get("contact_limit_exhausted") is not True:
            raise ValueError("unsupervised_repeat_contact")
        if not isinstance(case["next_action"], str) or len(case["next_action"]) < 70:
            raise ValueError("unclear_action")
        due = utc_date(case["next_due_utc"])
        last = utc_date(case["last_contact_utc"])
        if last > due:
            raise ValueError("review_due_before_last_contact")
        if case["status"] != "closed":
            (runnable if due <= now else future).append((due,case))
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate_case")
    runnable.sort(key=lambda item:(item[0],item[1]["id"]))
    future.sort(key=lambda item:(item[0],item[1]["id"]))
    result = {
        "validated": True, "status": "due" if runnable else "wait_for_due_or_new_evidence",
        "end_state_target_not_claimed": True,
        "active_gate": active[0]["id"],
        "verified_win_records": len(wins),
        "focus_case_count": len(cases),
        "external_volunteers_required": False,
        "new_model_calls": 0, "new_scheduled_jobs": 0,
        "can_autocontact_institutions": False,
        "parallel_readiness": parallel_readiness,
        "parallel_build_does_not_advance_release_gates": True,
    }
    if runnable:
        case = runnable[0][1]
        result.update({"case_id": case["id"], "due_at":case["next_due_utc"],
                       "source_url":case["source_url"],
                       "next_action":case["next_action"],"action_type":"read_only_primary_source_check",
                       "risk_tier":0})
    else:
        result["next_due_at"] = future[0][0].isoformat() if future else None
        result["next_action"] = ("No further routine email. If substantive incoming reply or independently "
                                 "verified source change is seen, re-evaluate a focus case; otherwise remain idle. "
                                 "Do not manufacture a scout lead or mark a draft as public benefit.")
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--control",default="ops/mission-control.json")
    p.add_argument("--win-ledger",default="WIN-LEDGER.md")
    p.add_argument("--at",help="Optional UTC ISO timestamp for deterministic testing")
    args=p.parse_args(argv)
    try:
        now=utc_date(args.at) if args.at else datetime.now(timezone.utc)
        cfg=json.loads(Path(args.control).read_text(encoding="utf-8"))
        wins=Path(args.win_ledger).read_text(encoding="utf-8")
        result=validate_and_select(cfg,wins,now=now)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print("MISSION GATE BLOCKED: "+str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
