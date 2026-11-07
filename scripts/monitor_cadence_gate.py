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
        return age < timedelta(0) or age >= INTERVAL
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return True
