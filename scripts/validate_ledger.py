#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
schema_required = {"id","date","category","status","scope","action","outcome","replicable"}

lines = (root / "actions.jsonl").read_text(encoding="utf-8").splitlines()
seen = set()

for number, line in enumerate(lines, start=1):
    if not line.strip():
        continue
    item = json.loads(line)
    missing = schema_required - item.keys()
    if missing:
        raise SystemExit(f"line {number}: missing required keys: {sorted(missing)}")
    if item["id"] in seen:
        raise SystemExit(f"line {number}: duplicate action id {item['id']}")
    seen.add(item["id"])

print(f"validated {len(seen)} Humanity Loop actions")
