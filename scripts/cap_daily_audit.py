#!/usr/bin/env python3
"""Run the Humanity Loop CAP Daily Audit without AppDeploy runtime credits."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

SOURCE_URL = "https://api.weather.gov/alerts/active"
USER_AGENT = "HumanityLoop-CAPAudit/1.0 (https://github.com/Lesterhau/humanity-loop)"
MAX_ALERTS = 250
MAX_FINDINGS = 400


def as_text(value: Any) -> str:
    return "" if value is None else str(value)


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def add_finding(
    out: list[dict[str, Any]],
    base: dict[str, str],
    severity: str,
    title: str,
    detail: str,
    now: str,
) -> None:
    out.append(
        {
            **base,
            "severity": severity,
            "title": title,
            "detail": detail,
            "status": "open",
            "firstSeen": now,
        }
    )


def audit_feature(feature: dict[str, Any], now: str) -> list[dict[str, Any]]:
    p = feature.get("properties") or {}
    if not isinstance(p, dict):
        p = {}

    alert_id = as_text(feature.get("id") or p.get("id") or p.get("@id"))
    sender = as_text(p.get("sender") or p.get("senderName"))
    event = as_text(p.get("event"))
    sent = as_text(p.get("sent") or p.get("effective"))
    base = {
        "alertId": alert_id,
        "sender": sender,
        "event": event,
        "sent": sent,
        "sourceUrl": alert_id or SOURCE_URL,
    }

    headline = as_text(p.get("headline"))
    description = as_text(p.get("description"))
    instruction = as_text(p.get("instruction"))
    area_desc = as_text(p.get("areaDesc"))
    expires = as_text(p.get("expires"))
    severity = as_text(p.get("severity"))
    certainty = as_text(p.get("certainty"))
    urgency = as_text(p.get("urgency"))

    findings: list[dict[str, Any]] = []

    if not alert_id:
        add_finding(
            findings,
            base,
            "error",
            "Missing alert identifier",
            "The public alert record does not expose a stable identifier.",
            now,
        )
    if not event:
        add_finding(
            findings,
            base,
            "error",
            "Missing event type",
            "Recipients may not be able to identify the hazard type.",
            now,
        )
    if not severity or not certainty or not urgency:
        add_finding(
            findings,
            base,
            "error",
            "Missing core CAP classification",
            "Severity, certainty, and urgency should be present for a usable CAP info block.",
            now,
        )
    if not headline:
        add_finding(
            findings,
            base,
            "warning",
            "Missing headline",
            "A short human-readable headline improves rapid comprehension.",
            now,
        )
    if not description:
        add_finding(
            findings,
            base,
            "warning",
            "Missing description",
            "The alert may lack enough context for recipients to understand the hazard.",
            now,
        )
    if not instruction and urgency.lower() == "immediate":
        add_finding(
            findings,
            base,
            "warning",
            "Immediate alert has no action instruction",
            "An immediate alert without a clear instruction may leave recipients unsure what action to take.",
            now,
        )
    if not area_desc:
        add_finding(
            findings,
            base,
            "warning",
            "Missing human-readable target area",
            "Recipients may have difficulty knowing whether the alert applies to them.",
            now,
        )

    expires_dt = parse_time(expires)
    sent_dt = parse_time(sent)
    if expires_dt is not None and sent_dt is not None and expires_dt <= sent_dt:
        add_finding(
            findings,
            base,
            "error",
            "Expiration does not follow sent/effective time",
            "The alert appears to expire before or when it becomes effective.",
            now,
        )

    if instruction:
        sentences = [s.strip() for s in re.split(r"[.!?]+", instruction) if s.strip()]
        max_words = max((len(s.split()) for s in sentences), default=0)
        if max_words > 30:
            add_finding(
                findings,
                base,
                "advisory",
                "Long sentence in instruction",
                f"At least one instruction sentence has {max_words} words; shorter sentences may reduce cognitive load during emergencies.",
                now,
            )

    return findings


def fetch_active_alerts() -> list[dict[str, Any]]:
    request = Request(
        SOURCE_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/geo+json, application/json",
        },
    )
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"NWS alerts fetch failed: {response.status}")
        data = json.load(response)

    features = data.get("features") or []
    if not isinstance(features, list):
        raise RuntimeError("NWS alerts response does not contain a feature list")
    return [f for f in features[:MAX_ALERTS] if isinstance(f, dict)]


def build_report(features: list[dict[str, Any]], now: str) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for feature in features:
        findings.extend(audit_feature(feature, now))

    findings = findings[:MAX_FINDINGS]
    counts = Counter(item["severity"] for item in findings)
    return {
        "schemaVersion": 1,
        "runAt": now,
        "source": SOURCE_URL,
        "alertsChecked": len(features),
        "findingsCount": len(findings),
        "bySeverity": {
            "error": counts.get("error", 0),
            "warning": counts.get("warning", 0),
            "advisory": counts.get("advisory", 0),
        },
        "findings": findings,
    }


def write_report(report: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    latest = output_dir / "latest.json"
    run_date = report["runAt"][:10]
    archive = runs_dir / f"{run_date}.json"
    latest.write_text(payload, encoding="utf-8")
    archive.write_text(payload, encoding="utf-8")
    return latest, archive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="runtime/cap-daily-audit",
        help="Directory for the latest report and dated run receipts.",
    )
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    features = fetch_active_alerts()
    report = build_report(features, now)
    latest, archive = write_report(report, Path(args.output_dir))

    print(
        json.dumps(
            {
                "status": "ok",
                "runAt": report["runAt"],
                "alertsChecked": report["alertsChecked"],
                "findingsCount": report["findingsCount"],
                "bySeverity": report["bySeverity"],
                "latest": str(latest),
                "archive": str(archive),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
