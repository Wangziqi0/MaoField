from __future__ import annotations
from pathlib import Path
import json
from collections import Counter

EXPECTED_COUNTS = {
    "BEHAVIOR": 15360,
    "STRUCTURE": 1280,
    "ACTION_SIBLING": 1280,
    "ORDINARY_CONTROL": 192,
    "STRUCTURE_CRITERION": 32,
    "CANARY": 12,
}
EXPECTED_TOTAL = 18156


def load_schedule(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    validate_schedule(rows)
    return rows


def validate_schedule(rows: list[dict]) -> None:
    if len(rows) != EXPECTED_TOTAL:
        raise ValueError("SCHEDULE_TOTAL")
    if [row["attempt"] for row in rows] != list(range(1, EXPECTED_TOTAL + 1)):
        raise ValueError("SCHEDULE_ATTEMPT_SEQUENCE")
    if Counter(row["channel"] for row in rows) != Counter(EXPECTED_COUNTS):
        raise ValueError("SCHEDULE_CHANNEL_COUNTS")
    for row in rows:
        required = {"attempt", "channel", "stratum", "superblock", "opaque_slot", "turn"}
        if set(row) != required:
            raise ValueError("SCHEDULE_ROW_SCHEMA")
    behavior = [row for row in rows if row["channel"] == "BEHAVIOR"]
    first_sealed = next(i for i, row in enumerate(behavior) if row["stratum"] == "SEALED32")
    if any(row["stratum"] != "MAIN96" for row in behavior[:first_sealed]):
        raise ValueError("MAIN96_ORDER")
    if any(row["stratum"] != "SEALED32" for row in behavior[first_sealed:]):
        raise ValueError("SEALED32_ORDER")
    if first_sealed != 96 * 20 * 6:
        raise ValueError("MAIN96_ATTEMPT_COUNT")
