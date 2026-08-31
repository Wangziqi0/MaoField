from __future__ import annotations
from pathlib import Path
import json
import os
import secrets
from .analysis import analyze_run
from .assignment import build_private_ledger, derive_keys, encrypt_ledger
from .canonical import canonical_json_bytes, sha256_bytes
from .custody import atomic_new, dpapi_protect
from .formal_return import build_formal_return
from .provider_adapter import dispatch, load_api_key
from .schedule import load_schedule
from .state_machine import run_schedule


def run_formal(
    package_root: Path,
    schedule_path: Path,
    formal_pi_adoption_path: Path,
    run_root: Path,
    output_zip: Path,
) -> dict:
    adoption_bytes = formal_pi_adoption_path.read_bytes()
    adoption = json.loads(adoption_bytes)
    required = {
        "formal_execution_authorized": True,
        "provider_calls_authorized": 18156,
        "production_roots_authorized": 1,
        "retries": 0,
        "automatic_next_round": False,
    }
    for key, value in required.items():
        if adoption.get(key) != value:
            raise RuntimeError(f"FORMAL_ADOPTION:{key}")
    if run_root.exists() or output_zip.exists():
        raise RuntimeError("FORMAL_ROOT_OR_OUTPUT_EXISTS")
    run_root.mkdir(parents=True)
    root_secret = secrets.token_bytes(32)
    keys = derive_keys(
        root_secret,
        adoption["candidate_zip_sha256"],
        sha256_bytes(adoption_bytes),
        adoption["pi_nonce_hex"],
    )
    ledger = build_private_ledger(keys)
    public_binding = {
        "candidate_zip_sha256": adoption["candidate_zip_sha256"],
        "formal_pi_adoption_sha256": sha256_bytes(adoption_bytes),
        "schedule_sha256": sha256_bytes(schedule_path.read_bytes()),
    }
    envelope = encrypt_ledger(ledger, keys["evidence"], public_binding)
    atomic_new(run_root / "PRIVATE_ASSIGNMENT.encrypted.json", canonical_json_bytes(envelope))
    atomic_new(run_root / "ASSIGNMENT_KEY.dpapi", dpapi_protect(keys["evidence"], "MaoField GLM53 assignment key"))
    atomic_new(run_root / "ANALYSIS_KEY.dpapi", dpapi_protect(keys["world_main"], "MaoField GLM53 analysis key"))
    api_key = load_api_key()
    def adapter(body, metadata):
        return dispatch(body, api_key, provider_authorized=True)
    completion = run_schedule(
        schedule_path,
        run_root,
        keys,
        ledger,
        adapter,
        provider_authorized=True,
    )
    analysis_root = run_root / "ANALYSIS"
    result = analyze_run(run_root, keys["world_main"], analysis_root)
    binding = {
        "adoption_sha256": sha256_bytes(adoption_bytes),
        "completion": completion,
        "result_sha256": sha256_bytes((analysis_root / "FORMAL_RESULT.json").read_bytes()),
        "automatic_next_round": False,
    }
    return build_formal_return(output_zip, run_root, analysis_root, binding)
