#!/usr/bin/env python3
"""Source-grounded, cross-border review *candidates* for G3/G4.

All input is operator-supplied untrusted text. No network, account access,
model call, file writes, task claims, approval, or remote verification occurs.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import ipaddress
import re
import urllib.parse
from typing import Any

MAX_OBSERVATIONS = 6
MAX_EXCERPT_CHARS = 700
LANGUAGE_RE = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z]{2,8})?$")
CASE_RE = re.compile(r"^OT-[0-9]{3}$")
ALLOWED_METHODS = {"public_text_retrieval", "public_browser", "official_pdf_text"}
SAFE_STATUSES = {"candidate", "source_blocked", "uncertain"}
SENSITIVE_KEYS = {"access_token", "api_key", "password", "secret", "session", "authorization"}


def utc_timestamp(value: Any, *, now: datetime | None = None) -> datetime:
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError("invalid_observation_time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid_observation_time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError("timestamp_must_be_utc")
    if parsed > (now or datetime.now(timezone.utc)):
        raise ValueError("future_observation_refused")
    return parsed


def public_https(url: Any) -> str:
    if not isinstance(url, str) or not 1 <= len(url) <= 800:
        raise ValueError("invalid_public_url")
    if any(ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError("control_character_in_source_url")
    if "#" in url:
        raise ValueError("fragment_in_source_url_forbidden")
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host or parsed.username or parsed.password:
        raise ValueError("public_https_required")
    if host == "localhost" or host.endswith((".local", ".internal", ".localhost", ".test")):
        raise ValueError("nonpublic_source_forbidden")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("numeric_source_host_forbidden")
    if any(key in k.lower() for k,_ in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
           for key in SENSITIVE_KEYS):
        raise ValueError("secret_bearing_url_forbidden")
    return url


def arithmetic_check(item: Any, *, source_count: int) -> dict[str, Any]:
    if not isinstance(item, dict) or set(item) != {
        "kind", "source_index", "part", "whole", "claimed_percent"
    } or item["kind"] != "percentage":
        raise ValueError("unsupported_arithmetic_claim")
    index = item["source_index"]
    if type(index) is not int or not (0 <= index < source_count):
        raise ValueError("missing_arithmetic_source")
    try:
        part, whole, claimed = [Decimal(str(item[k])) for k in ("part","whole","claimed_percent")]
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid_arithmetic_numbers") from exc
    if any(not v.is_finite() for v in (part,whole,claimed)):
        raise ValueError("invalid_arithmetic_numbers")
    if whole <= 0 or part < 0 or part > whole or claimed < 0 or claimed > 100:
        raise ValueError("invalid_arithmetic_range")
    expected = (part * 100 / whole).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    mismatch = abs(expected - claimed) > Decimal("0.1")
    return {
        "source_index": index,
        "kind": "percentage",
        "part": str(part), "whole": str(whole),
        "claimed_percent": str(claimed),
        "calculated_percent_1dp": str(expected),
        "arithmetic_status": "discrepancy_candidate" if mismatch else "agrees_arithmetically",
        "interpretation": "math only: does not establish the underlying count, data provenance, or a public error",
        "independent_source_verification": False,
    }


def validate_source_packet(raw: Any, task: dict[str, Any], *,
                           now: datetime | None = None) -> dict[str, Any]:
    """Validate input shape and consistency, NOT whether a source was fetched."""
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise ValueError("unsupported_source_packet")
    if raw.get("task_id") != task.get("task_id"):
        raise ValueError("packet_task_mismatch")
    if not all(k in task for k in ("case_id", "country", "languages")):
        raise ValueError("task_jurisdiction_not_declared")
    if any(raw.get(k) != task[k] for k in ("case_id", "country", "languages")):
        raise ValueError("packet_jurisdiction_mismatch")
    case_id, country = raw.get("case_id"), raw.get("country")
    if not isinstance(case_id, str) or not CASE_RE.fullmatch(case_id):
        raise ValueError("invalid_case_id")
    if not isinstance(country, str) or not re.fullmatch(r"[A-Z]{2}",country):
        raise ValueError("invalid_country")
    languages = raw.get("languages")
    if not isinstance(languages, list) or not 1 <= len(languages) <= 3:
        raise ValueError("invalid_languages")
    if any(not isinstance(x,str) or not LANGUAGE_RE.fullmatch(x) for x in languages):
        raise ValueError("invalid_languages")
    if len(set(languages)) != len(languages):
        raise ValueError("duplicate_language")
    if raw.get("tier") != 0 or type(raw.get("tier")) is not int:
        raise ValueError("tier0_only")
    if raw.get("external_actions") is not False or raw.get("consent_to_publish") is not False:
        raise ValueError("no_external_actions_or_publication")
    if raw.get("review_state") != "pending_independent_review":
        raise ValueError("review_not_preapproved")
    if raw.get("fixture_only") not in (True,False) or type(raw.get("fixture_only")) is not bool:
        raise ValueError("fixture_flag_required")
    observations = raw.get("observations")
    if not isinstance(observations,list) or not 1 <= len(observations) <= MAX_OBSERVATIONS:
        raise ValueError("invalid_observations")
    listed_urls = set(task.get("public_source_urls", []))
    if not listed_urls:
        raise ValueError("task_source_urls_required")
    normalized = []
    for obs in observations:
        if not isinstance(obs,dict) or set(obs) != {
            "source_url","observed_at_utc","method","language","status","excerpt","review_question"
        }:
            raise ValueError("invalid_observation_fields")
        url = public_https(obs["source_url"])
        if url not in listed_urls:
            raise ValueError("source_not_approved_in_task")
        method, language, status = obs["method"],obs["language"],obs["status"]
        if method not in ALLOWED_METHODS:
            raise ValueError("unsupported_observation_method")
        if language not in languages or status not in SAFE_STATUSES:
            raise ValueError("language_or_status_invalid")
        utc_timestamp(obs["observed_at_utc"], now=now)
        excerpt, question=obs["excerpt"],obs["review_question"]
        if not isinstance(excerpt,str) or not 10 <= len(excerpt) <= MAX_EXCERPT_CHARS:
            raise ValueError("invalid_observation_excerpt")
        if not isinstance(question,str) or not 12 <= len(question) <= 350:
            raise ValueError("invalid_review_question")
        if any(x in excerpt.lower() for x in ("-----begin private key-----", "bearer eyj", "api_key=", "password=")):
            raise ValueError("sensitive_excerpt_forbidden")
        normalized.append(dict(obs))
    checks=raw.get("arithmetic_checks",[])
    if not isinstance(checks,list) or len(checks)>3:
        raise ValueError("invalid_arithmetic_checks")
    computed=[arithmetic_check(x, source_count=len(normalized)) for x in checks]
    if any(c["arithmetic_status"]=="discrepancy_candidate" for c in computed) and not normalized:
        raise ValueError("missing_source_provenance")
    return {
        "schema_version": 1,
        "task_id":task["task_id"],"case_id":case_id,"country":country,
        "languages":languages,"fixture_only":raw["fixture_only"],
        "review_state":"pending_independent_review",
        "source_claim_status":"operator_supplied_not_independently_verified",
        "externally_verified":False,"eligible_for_win_ledger":False,
        "external_actions":0,"model_calls":0,"new_schedulers":0,
        "observations":normalized,"arithmetic_checks":computed,
        "language_competence_required":any(x.split("-",1)[0]!="en" for x in languages),
        "note":"Source snippets and timestamps are untrusted operator inputs. Arithmetic checks verify math only. Independent public-source and qualified-language review are prerequisites for accepted outcomes.",
    }
