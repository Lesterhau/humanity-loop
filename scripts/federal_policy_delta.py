#!/usr/bin/env python3
"""Credit-independent detector for Humanity Loop Federal Policy Delta.

This worker detects and preserves visible changes in selected official federal
sources. It does not make legal conclusions. Neutral legal/evidence review is a
separate Humanity Loop stage after a delta is detected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from difflib import unified_diff
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

USER_AGENT = "HumanityLoop-PolicyDelta/1.0 (https://github.com/Lesterhau/humanity-loop)"
MAX_TEXT = 180_000
MAX_EXCERPT = 8_000
MAX_DIFF = 20_000

SOURCES = [
    {"key": "white-house", "name": "White House presidential actions", "branch": "Executive", "url": "https://www.whitehouse.gov/presidential-actions/"},
    {"key": "congress", "name": "Congress.gov legislation", "branch": "Legislative", "url": "https://www.congress.gov/"},
    {"key": "fda", "name": "Food and Drug Administration", "branch": "Executive agency", "url": "https://www.federalregister.gov/agencies/food-and-drug-administration"},
    {"key": "dod", "name": "Department of Defense", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/defense-department"},
    {"key": "state", "name": "Department of State", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/state-department"},
    {"key": "dhs", "name": "Department of Homeland Security", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/homeland-security-department"},
    {"key": "usda", "name": "Department of Agriculture", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/agriculture-department"},
    {"key": "commerce", "name": "Department of Commerce", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/commerce-department"},
    {"key": "education", "name": "Department of Education", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/education-department"},
    {"key": "energy", "name": "Department of Energy", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/energy-department"},
    {"key": "hhs", "name": "Department of Health and Human Services", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/health-and-human-services-department"},
    {"key": "hud", "name": "Department of Housing and Urban Development", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/housing-and-urban-development-department"},
    {"key": "interior", "name": "Department of the Interior", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/interior-department"},
    {"key": "transportation", "name": "Department of Transportation", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/transportation-department"},
    {"key": "treasury", "name": "Department of the Treasury", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/treasury-department"},
    {"key": "doj", "name": "Department of Justice", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/justice-department"},
    {"key": "va", "name": "Department of Veterans Affairs", "branch": "Executive department", "url": "https://www.federalregister.gov/agencies/veterans-affairs-department"},
]


class VisibleTextParser(HTMLParser):
    BLOCKED = {"script", "style", "noscript", "svg", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.block_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.BLOCKED:
            self.block_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCKED and self.block_depth:
            self.block_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.block_depth and data.strip():
            self.parts.append(data)


def normalize_html(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    text = " ".join(parser.parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_TEXT]


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


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def snapshot_path(root: Path, key: str) -> Path:
    return root / "snapshots" / f"{key}.json"


def load_snapshot(root: Path, key: str) -> dict[str, Any] | None:
    path = snapshot_path(root, key)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_snapshot(root: Path, source: dict[str, str], text: str, captured_at: str) -> dict[str, Any]:
    record = {
        **source,
        "hash": digest(text),
        "capturedAt": captured_at,
        "excerpt": text[:MAX_EXCERPT],
    }
    path = snapshot_path(root, source["key"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def compact_diff(old: str, new: str) -> str:
    old_chunks = re.split(r"(?<=[.!?])\s+", old)
    new_chunks = re.split(r"(?<=[.!?])\s+", new)
    diff = "\n".join(
        unified_diff(
            old_chunks,
            new_chunks,
            fromfile="older",
            tofile="newer",
            lineterm="",
            n=2,
        )
    )
    return diff[:MAX_DIFF]


def run(root: Path) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    changes: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    baselines = 0

    for source in SOURCES:
        try:
            text = fetch_text(source["url"])
            new_hash = digest(text)
            previous = load_snapshot(root, source["key"])

            if previous is None:
                save_snapshot(root, source, text, now)
                baselines += 1
                continue

            if previous.get("hash") == new_hash:
                continue

            candidate = {
                "source": source["name"],
                "sourceKey": source["key"],
                "branch": source["branch"],
                "url": source["url"],
                "detectedAt": now,
                "olderCapturedAt": previous.get("capturedAt"),
                "olderHash": previous.get("hash"),
                "newerHash": new_hash,
                "olderExcerpt": previous.get("excerpt", ""),
                "newerExcerpt": text[:MAX_EXCERPT],
                "textDiff": compact_diff(previous.get("excerpt", ""), text[:MAX_EXCERPT]),
                "reviewStatus": "needs-neutral-human-or-agent-review",
                "legalConclusion": None,
            }
            changes.append(candidate)
            save_snapshot(root, source, text, now)
        except Exception as exc:
            failures.append(
                {
                    "sourceKey": source["key"],
                    "source": source["name"],
                    "url": source["url"],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    receipt = {
        "schemaVersion": 1,
        "runAt": now,
        "sourcesConfigured": len(SOURCES),
        "baselinesCreated": baselines,
        "changesDetected": len(changes),
        "failuresCount": len(failures),
        "changes": changes,
        "failures": failures,
        "note": "Detection only. A delta is not a legal finding and must be neutrally reviewed before publication or escalation.",
    }

    root.mkdir(parents=True, exist_ok=True)
    latest = root / "latest-run.json"
    latest.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

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
    parser.add_argument("--output-dir", default="runtime/federal-policy-delta")
    args = parser.parse_args()

    receipt = run(Path(args.output_dir))
    print(
        json.dumps(
            {
                "status": "ok" if receipt["failuresCount"] == 0 else "partial",
                "runAt": receipt["runAt"],
                "sourcesConfigured": receipt["sourcesConfigured"],
                "baselinesCreated": receipt["baselinesCreated"],
                "changesDetected": receipt["changesDetected"],
                "failuresCount": receipt["failuresCount"],
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["failuresCount"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
