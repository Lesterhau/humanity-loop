#!/usr/bin/env python3
"""One-shot, allowlisted public HTML snapshot for Humanity Loop G3/G4 evidence.

Without --allow-live-get this module cannot make an external request.
Live mode performs ONE bounded HTTPS GET of a compile-time allowlisted
public source, with a pinned DNS-selected global IP, valid TLS hostname,
no proxies, redirects, cookies, credentials, model calls or scheduled work.

A snapshot is a machine-acquired source observation, NOT an independently
reviewed claim, outside correction, accepted contribution or public benefit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
from html.parser import HTMLParser
import http.client
import ipaddress
import json
from pathlib import Path
import re
import socket
import ssl
import sys
from typing import Any, Callable
from urllib.parse import urlsplit

from foundry_lite import validate_task

# Independent maintenance of this list must be reviewed through a PR.
# No arbitrary URLs from issue comments, task packets, or model outputs.
ALLOWED_CASE_URLS = {
    "OT-013": "https://city.lums.edu.pk/what-we-do/city-research/dare-rc/",
}
ALLOWED_HOSTS = {"city.lums.edu.pk"}
MAX_BYTES = 1_500_000
MAX_CHARS = 450_000
CONNECT_TIMEOUT_SECONDS = 6
MAX_SOURCE_EXCERPT_CHARS = 240
ALLOWED_CONTENT_TYPES = {"text/html"}
EXPECTED_INDICATORS = {
    "OT-013": {
        "headline_103": r"\b103\s*\(0\.2%\)",
        "narrative_117": r"\b84\s+of\s+the\s+117\s+schools\b",
        "narrative_81_6": r"\b81\.6%",
        "district_count_117": r"\b117\s+compounding\s+Priority\s+1.{0,5}2\s+schools",
    },
}


class PublicHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "noscript", "svg", "template"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "noscript", "svg", "template") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and data.strip():
            self.blocks.append(data.strip())


def normalized_visible_text(raw: bytes, *, encoding: str = "utf-8") -> str:
    try:
        html = raw.decode(encoding, errors="strict")
    except (LookupError, UnicodeError) as exc:
        raise ValueError("source_encoding_not_supported") from exc
    parser = PublicHTML()
    parser.feed(html)
    normalized = re.sub(r"\s+", " ", " ".join(parser.blocks)).strip()
    if len(normalized) > MAX_CHARS:
        raise ValueError("source_visible_text_too_large")
    return normalized


def validate_target(case: str, raw_task: dict[str, Any]) -> str:
    task = validate_task(raw_task)
    if case not in ALLOWED_CASE_URLS:
        raise ValueError("case_not_source_allowlisted")
    source_url = ALLOWED_CASE_URLS[case]
    if task.get("case_id") != case or task.get("country") != "PK" or task.get("languages") != ["en"]:
        raise ValueError("case_country_language_mismatch")
    if task.get("public_source_urls") != [source_url]:
        raise ValueError("task_exact_source_not_approved")
    parsed = urlsplit(source_url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS or parsed.username or parsed.password:
        raise ValueError("source_allowlist_invalid")
    if parsed.port not in (None, 443) or parsed.fragment or parsed.query:
        raise ValueError("source_url_parameters_forbidden")
    return source_url


def global_ips(hostname: str, *, resolver: Callable[..., Any] = socket.getaddrinfo) -> list[str]:
    responses = resolver(hostname, 443, type=socket.SOCK_STREAM)
    ips: list[str] = []
    if not responses:
        raise ValueError("source_dns_unavailable")
    for entry in responses:
        if entry[0] not in (socket.AF_INET, socket.AF_INET6):
            raise ValueError("unrecognized_dns_address_family")
        address = entry[4][0]
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            # Refuse mixed public/private answers; no accidental internal requests.
            raise ValueError("source_dns_private_address")
        if address not in ips:
            ips.append(address)
    return ips


class IPPinnedHTTPSConnection(http.client.HTTPSConnection):
    """Connect the one DNS-checked numeric IP, validate TLS for the original host."""
    def __init__(self, hostname: str, chosen_ip: str, *, timeout: int) -> None:
        super().__init__(hostname, 443, timeout=timeout, context=ssl.create_default_context())
        self.pinned_ip = chosen_ip

    def connect(self) -> None:
        sock = socket.create_connection((self.pinned_ip, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except Exception:
            sock.close()
            raise


def one_public_html_get(url: str, *, resolver=socket.getaddrinfo,
                        connection_factory=IPPinnedHTTPSConnection) -> tuple[bytes, str]:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("source_not_allowlisted")
    ips = global_ips(parsed.hostname, resolver=resolver)
    connection = connection_factory(parsed.hostname, ips[0], timeout=CONNECT_TIMEOUT_SECONDS)
    try:
        # One GET, never follow 3xx; the connection has no proxy, cookie jar,
        # client credentials or remote-command execution surface.
        path = parsed.path or "/"
        if parsed.query:
            raise ValueError("source_query_forbidden")
        connection.request("GET", path, headers={
            "Accept": "text/html",
            "Accept-Encoding": "identity",
            "User-Agent": "HumanityLoopReadOnlyEvidence/1.0 (+https://github.com/Lesterhau/humanity-loop)",
            "Connection": "close",
        })
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError("source_http_non_200")
        media_type = response.getheader("Content-Type", "").split(";", 1)[0].strip().lower()
        if media_type not in ALLOWED_CONTENT_TYPES:
            raise ValueError("source_non_html_response")
        announced_size = response.getheader("Content-Length")
        if announced_size and (not announced_size.isdecimal() or int(announced_size) > MAX_BYTES):
            raise ValueError("source_response_too_large")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("source_response_too_large")
        if not raw:
            raise ValueError("source_empty_response")
        return raw, media_type
    finally:
        connection.close()


def source_snapshot(case: str, raw_task: dict[str, Any], *,
                    allow_live_get: bool, get=None,
                    observed_at: datetime | None = None) -> dict[str, Any]:
    source = validate_target(case, raw_task)
    if not allow_live_get:
        raise ValueError("live_public_get_requires_explicit_opt_in")
    observed_at = observed_at or datetime.now(timezone.utc)
    if observed_at.tzinfo is None or observed_at.utcoffset() != timezone.utc.utcoffset(observed_at):
        raise ValueError("observation_time_must_be_utc")
    raw, content_type = (get or one_public_html_get)(source)
    if not isinstance(raw, bytes) or not 0 < len(raw) <= MAX_BYTES:
        raise ValueError("source_response_too_large_or_invalid")
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("source_non_html_response")
    text = normalized_visible_text(raw)
    indicators: dict[str, Any] = {}
    for name, pattern in EXPECTED_INDICATORS[case].items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        indicators[name] = {
            "observed_in_visible_html": bool(match),
            "source_excerpt": (
                text[max(0, match.start()-60): min(len(text), match.end()+110)][:MAX_SOURCE_EXCERPT_CHARS]
                if match else None
            ),
        }

    percent = re.search(
        r"\b(?P<part>\d+)\s+of\s+the\s+(?P<whole>\d+)\s+schools\b"
        r"[^.]{0,250}?\((?P<claimed>\d+(?:\.\d+)?)%\)", text, flags=re.IGNORECASE,
    )
    arithmetic: dict[str, Any] | None = None
    if percent:
        part, whole, claimed = (Decimal(percent.group(k)) for k in ("part", "whole", "claimed"))
        if whole > 0 and 0 <= part <= whole and 0 <= claimed <= 100:
            computed = (part * 100 / whole).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            arithmetic = {
                "numerator": str(part), "denominator": str(whole),
                "source_claim_percent": str(claimed),
                "computed_percent_1dp": str(computed),
                "arithmetic_discrepancy_candidate": abs(computed - claimed) > Decimal("0.1"),
                "underlying_cohort_truth_verified": False,
            }

    return {
        "schema_version": 1, "record_type": "direct_public_html_snapshot",
        "case_id": case, "country": raw_task["country"], "languages": raw_task["languages"],
        "source_url": source, "retrieval_method": "one_explicit_direct_https_get",
        "observed_at_utc": observed_at.isoformat().replace("+00:00", "Z"),
        "http_status": 200, "content_type": content_type,
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_bytes": len(raw), "visible_text_chars": len(text),
        "indicators": indicators, "arithmetic": arithmetic,
        "model_calls": 0, "appdeploy_credits_used": 0,
        "external_write_actions": 0, "scheduled": False,
        "independently_reviewed": False, "confirmed_public_correction": False,
        "eligible_for_win_ledger": False,
        "review_required": "Reopen and independently confirm the original public source, context, underlying cohort and qualified local analysis; the raw hash is only a reproducibility handle.",
        "limitations": "This machine retrieved one public HTML response. It did not run a browser, audit underlying datasets, validate localization, contact the institution or establish real-world public benefit.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, choices=sorted(ALLOWED_CASE_URLS))
    parser.add_argument("--task", required=True, help="Exact previously approved Tier-0 task manifest")
    parser.add_argument("--allow-live-get", action="store_true", help="Authorize one public URL GET only")
    parser.add_argument("--output", required=True, help="New local JSON receipt path; existing files are refused")
    args = parser.parse_args(argv)
    try:
        task_path = Path(args.task)
        if task_path.stat().st_size > 12_000:
            raise ValueError("task_file_too_large")
        task = json.loads(task_path.read_text(encoding="utf-8"))
        target = Path(args.output)
        # Check output constraints BEFORE any network activity, and still open
        # exclusively afterward to prevent clobbering a concurrent receipt.
        if target.is_symlink():
            raise ValueError("output_symlink_refused")
        if target.exists():
            raise ValueError("output_already_exists")
        result = source_snapshot(args.case, task, allow_live_get=args.allow_live_get)
        with target.open("x", encoding="utf-8") as file:
            json.dump(result, file, indent=2, ensure_ascii=False)
            file.write("\n")
        print(json.dumps({"status":"snapshot_ready_for_independent_review",
                          "case_id":args.case,"output":str(target),
                          "independently_reviewed":False,"raw_sha256":result["raw_sha256"]}))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, http.client.HTTPException,
            ssl.SSLError, socket.timeout) as exc:
        # No raw web content, session detail or arbitrary exception text in logs.
        if isinstance(exc,ValueError) and str(exc).startswith(("source_", "live_", "case_", "task_", "observation_", "output_")):
            reason = str(exc)
        else:
            reason = "network_or_local_validation_blocked"
        print("SOURCE SNAPSHOT BLOCKED: " + reason, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
