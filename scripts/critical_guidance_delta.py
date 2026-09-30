#!/usr/bin/env python3
"""Credit-independent detector for Humanity Loop Critical Guidance Delta.

This stage preserves authoritative medication-safety page changes. It does not
classify a change as clinically material and does not provide medical advice.
Detected deltas require verification against the official source before action.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

USER_AGENT = "HumanityLoop-GuidanceDelta/1.0 (https://github.com/Lesterhau/humanity-loop)"
MAX_TEXT = 180_000
MAX_DIFF_LINES = 30

SOURCES = [
    {
        "key": "who-medical-alerts",
        "name": "WHO Medical Product Alerts",
        "authority": "World Health Organization",
        "url": "https://www.who.int/teams/regulation-prequalification/incidents-and-SF/full-list-of-who-medical-product-alerts",
        "purpose": "Substandard and falsified medical-product alerts with international public-health significance.",
    },
    {
        "key": "fda-drug-safety",
        "name": "FDA Drug Safety Communications",
        "authority": "U.S. Food and Drug Administration",
        "url": "https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications",
        "purpose": "New medicine safety issues, warnings, labeling changes, and risk communications.",
    },
    {
        "key": "ema-prac",
        "name": "EMA PRAC Safety Highlights",
        "authority": "European Medicines Agency",
        "url": "https://www.ema.europa.eu/en/committees/pharmacovigilance-risk-assessment-committee-prac",
        "purpose": "Safety signals, reviews, and risk-management highlights from the EU pharmacovigilance committee.",
    },
]


class VisibleTextParser(HTMLParser):
    BLOCKED = {"script", "style", "noscript", "svg", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.block_depth = 0
        self.lines: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.BLOCKED:
            self.block_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCKED and self.block_depth:
            self.block_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.block_depth:
            return
        line = re.sub(r"\s+", " ", data).strip()
        if line:
            self.lines.append(line)


def normalize_html(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    return "\n".join(parser.lines)[:MAX_TEXT]


def fetch_text(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=45) as response:
        if response.status >= 400:
            raise RuntimeError(f"HTTP {response.status}")
        raw = response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    text = normalize_html(raw)
    if not text:
        raise RuntimeError("empty normalized text")
    return text


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def diff_excerpt(previous: str, current: str) -> str:
    old_lines = previous.splitlines()
    new_lines = current.splitlines()
    old_set = set(old_lines)
    new_set = set(new_lines)
    removed = [line for line in old_lines if line not in new_set][:MAX_DIFF_LINES]
    added = [line for line in new_lines if line not in old_set][:MAX_DIFF_LINES]
    return "\n".join(
        [
            "REMOVED FROM PRIOR VERSION:",
            *[f"- {line}" for line in removed],
            "",
            "ADDED IN CURRENT VERSION:",
            *[f"+ {line}" for line in added],
        ]
    )[:14_000]


def snapshot_path(root: Path, key: str) -> Path:
    return root / "snapshots" / f"{key}.json"


def load_snapshot(root: Path, key: str) -> dict[str, Any] | None:
    path = snapshot_path(root, key)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_snapshot(root: Path, source: dict[str, str], text: str, now: str) -> None:
    record = {
        **source,
        "fingerprint": fingerprint(text),
        "normalizedText": text,
        "lastChecked": now,
    }
    path = snapshot_path(root, source["key"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(root: Path) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    changes: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    baselines = 0
    checked = 0

    for source in SOURCES:
        try:
            current = fetch_text(source["url"])
            checked += 1
            current_fp = fingerprint(current)
            prior = load_snapshot(root, source["key"])

            if prior is None:
                save_snapshot(root, source, current, now)
                baselines += 1
                continue

            if prior.get("fingerprint") != current_fp:
                changes.append(
                    {
                        "sourceKey": source["key"],
                        "sourceName": source["name"],
                        "authority": source["authority"],
                        "sourceUrl": source["url"],
                        "detectedAt": now,
                        "oldFingerprint": prior.get("fingerprint", ""),
                        "newFingerprint": current_fp,
                        "evidenceDiff": diff_excerpt(prior.get("normalizedText", ""), current),
                        "materiality": "unreviewed",
                        "severity": "unreviewed",
                        "verificationStatus": "needs-independent-source-review",
                        "medicalAdvice": None,
                    }
                )
                save_snapshot(root, source, current, now)
        except Exception as exc:
            failures.append(
                {
                    "sourceKey": source["key"],
                    "sourceName": source["name"],
                    "sourceUrl": source["url"],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    receipt = {
        "schemaVersion": 1,
        "runAt": now,
        "sourcesConfigured": len(SOURCES),
        "sourcesChecked": checked,
        "baselinesCreated": baselines,
        "changesDetected": len(changes),
        "failuresCount": len(failures),
        "changes": changes,
        "failures": failures,
        "verificationRule": "A detected page delta is triage only. Verify the official source and evidence before any clinical, regulatory, or safety action.",
    }

    root.mkdir(parents=True, exist_ok=True)
    (root / "latest-run.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if changes or failures:
        events = root / "events"
        events.mkdir(parents=True, exist_ok=True)
        stamp = now.replace(":", "").replace("-", "")
        (events / f"{stamp}.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="runtime/critical-guidance-delta")
    args = parser.parse_args()

    receipt = run(Path(args.output_dir))
    print(
        json.dumps(
            {
                "status": "ok" if receipt["failuresCount"] == 0 else "partial",
                "runAt": receipt["runAt"],
                "sourcesChecked": receipt["sourcesChecked"],
                "baselinesCreated": receipt["baselinesCreated"],
                "changesDetected": receipt["changesDetected"],
                "failuresCount": receipt["failuresCount"],
            },
            sort_keys=True,
        )
    )
    return 2 if receipt["failuresCount"] == receipt["sourcesConfigured"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
