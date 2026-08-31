from __future__ import annotations
from pathlib import Path
import hashlib
import json
import re
from .assignment import build_private_ledger, derive_keys
from .canonical import sha256_bytes
from .provider_adapter import dispatch
from .schedule import load_schedule

UPPER_HEX_64 = re.compile(r"^[0-9A-F]{64}$")


def validate_build_only(package_root: Path, schedule_path: Path, pi_template_path: Path) -> dict:
    schedule = load_schedule(schedule_path)
    template = json.loads(pi_template_path.read_text(encoding="utf-8"))
    failures = []
    if template.get("provider_calls_authorized") != 0:
        failures.append("PROVIDER_AUTHORITY_NONZERO")
    if template.get("production_roots_authorized") != 0:
        failures.append("ROOT_AUTHORITY_NONZERO")
    if template.get("automatic_next_round") is not False:
        failures.append("AUTOMATIC_NEXT_ROUND")
    # Root-independent assignment vectors; fixed test material is not a production secret.
    keys = derive_keys(b"R" * 32, "A" * 64, "B" * 64, "C" * 64)
    ledger = build_private_ledger(keys)
    try:
        dispatch(b"{}", "NOT_A_REAL_KEY", provider_authorized=False)
        failures.append("PROVIDER_FAIL_CLOSED_MISSING")
    except RuntimeError as exc:
        if str(exc) != "PROVIDER_CALL_NOT_AUTHORIZED_BUILD_ONLY":
            failures.append("PROVIDER_WRONG_FAILURE")
    return {
        "schema": "maofield.glm53.pre_root_build_only_validation.v2",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "schedule_rows": len(schedule),
        "assignment_main": len(ledger["behavior_main"]),
        "assignment_sealed": len(ledger["behavior_sealed"]),
        "assignment_siblings": len(ledger["siblings"]),
        "provider_calls": 0,
        "production_roots": 0,
        "automatic_next_round": False,
    }
