"""Pure, no-network cadence gate for public-source Critical Guidance checks.

The schedule can wake twice as often as the target cadence, but this
check only authorizes a scan when the durable prior receipt is sufficiently
old. Missing, invalid and future-dated receipts fail safe by permitting a
read-only scan, not by claiming a healthy monitor.
"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

INTERVAL = timedelta(hours=5)
PARTIAL_RETRY_INTERVAL = timedelta(hours=3)

def receipt_coverage_complete(data: object) -> bool:
    """Validate evidence of complete source coverage, not just cron success."""
    if not isinstance(data, dict):
        return False
    configured = data.get("sourcesConfigured")
    checked = data.get("sourcesChecked")
    failures = data.get("failuresCount")
    detail = data.get("failures")
    return (
        type(configured) is int and configured > 0 and
        type(checked) is int and checked == configured and
        type(failures) is int and failures == 0 and
        isinstance(detail, list) and len(detail) == 0
    )

def scan_due(receipt_file: Path, event_name: str, now=None) -> bool:
    if event_name in {"workflow_dispatch", "push"}:
        return True  # owner/manual or source change; no automatic publication
    if event_name != "schedule":
        return False
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    try:
        data = json.loads(receipt_file.read_text(encoding="utf-8"))
        last = datetime.fromisoformat(data["runAt"].replace("Z", "+00:00"))
        if last.tzinfo is None:
            return True
        age = now - last
        if age < timedelta(0):
            return True
        # Incomplete source checks need another bounded attempt; do not treat
        # a partial receipt as successful coverage for the full five hours.
        threshold = INTERVAL if receipt_coverage_complete(data) else PARTIAL_RETRY_INTERVAL
        return age >= threshold
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return True
