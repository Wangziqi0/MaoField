#!/usr/bin/env python3
"""Fail-fast negative smokes for the MaoField q4 panel generator.

This runner verifies invalid-artifact paths only. It does not load
checkpoints, train, call backward, generate text, or implement a full panel.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
PYTHON = Path("/home/amd/venv/bin/python")
GENERATOR = REPO / "experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py"
SCHEMA = REPO / "docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json"
OUT_JSON = REPO / "experiments/exp020_metric_stress_test/panel_primary_20260622/negative_smoke_20260622.json"
OUT_MD = REPO / "docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_NEGATIVE_SMOKE_20260622.md"
TMP = Path("/tmp/maofield_q4_negative_smoke_20260622")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def short(text: str, limit: int = 1600) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit // 2] + "\n...[truncated]...\n" + text[-limit // 2 :]


def make_schema(name: str, mutator: Callable[[dict[str, Any]], None]) -> Path:
    data = load_json(SCHEMA)
    mutator(data)
    path = TMP / f"{name}.json"
    write_json(path, data)
    return path


def run_generator(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    env["TOKENIZERS_PARALLELISM"] = "false"
    cmd = [str(PYTHON), str(GENERATOR), *args]
    return subprocess.run(cmd, cwd=REPO, env=env, text=True, capture_output=True)


def negative_case(name: str, args: list[str], expected_text: str) -> dict[str, Any]:
    proc = run_generator(args)
    combined = proc.stdout + "\n" + proc.stderr
    passed = proc.returncode != 0 and expected_text in combined
    return {
        "name": name,
        "expected_failure": True,
        "status": "pass" if passed else "fail",
        "returncode": proc.returncode,
        "expected_text": expected_text,
        "matched_expected_text": expected_text in combined,
        "stdout_tail": short(proc.stdout),
        "stderr_tail": short(proc.stderr),
    }


def wording_guard() -> dict[str, Any]:
    checks = [
        (
            "fixed true " + "wikitext" + " eval",
            [REPO / "experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py"],
        ),
        (
            "eval " + "blocks",
            [REPO / "experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py"],
        ),
        (
            "eval " + "target",
            [REPO / "experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py"],
        ),
        (
            'verdict = "' + 'survive"',
            [REPO / "scripts/math_turn_loso_audit.py"],
        ),
        (
            "存活" + " 3 泛函",
            [REPO / "experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py"],
        ),
    ]
    hits: list[dict[str, str]] = []
    for pattern, paths in checks:
        needle = pattern.lower()
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if needle in text.lower():
                hits.append({"pattern": pattern, "path": str(path.relative_to(REPO))})
    return {
        "name": "wording_guard",
        "status": "pass" if not hits else "fail",
        "hits": hits,
    }


def write_markdown(result: dict[str, Any]) -> None:
    lines = [
        "# MaoField q4 Panel Negative Smoke Record",
        "",
        f"> Generated on node36 at {result['generated_at']}.",
        "> This is an invalid-artifact smoke record, not a full panel result.",
        "",
        "## Boundary",
        "",
        "- No checkpoint was loaded.",
        "- No training, backward pass, optimizer step, text generation, or new loss was run.",
        "- These tests only verify that bad schema/provenance inputs fail.",
        "",
        "## Result",
        "",
        f"- Overall status: **{result['overall_status']}**",
        f"- Generator: `{result['generator']}`",
        f"- Schema: `{result['schema']}`",
        "",
        "## Cases",
        "",
        "| case | expected failure | status | matched text |",
        "|---|---|---|---|",
    ]
    for case in result["cases"]:
        lines.append(
            "| {name} | {expected} | {status} | `{text}` |".format(
                name=case["name"],
                expected="yes" if case.get("expected_failure") else "no",
                status=case["status"],
                text=case.get("expected_text", ""),
            )
        )
    guard = result["wording_guard"]
    lines.extend(
        [
            "",
            "## Wording Guard",
            "",
            f"- Status: **{guard['status']}**",
            f"- Hits: `{len(guard['hits'])}`",
            "",
            "## Claim Boundary",
            "",
            "This record does not approve full panel generation. It only closes",
            "the first fail-fast negative-smoke requirement from report (6).",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)

    wrong_split = make_schema(
        "wrong_source_split",
        lambda data: data["source"].__setitem__("source_split", "validation"),
    )
    source_hash_bad = make_schema(
        "source_hash_mismatch",
        lambda data: data["source"].__setitem__("input_ids_sha256", "0" * 64),
    )
    q4_bins_bad = make_schema(
        "q4_bin_size_mismatch",
        lambda data: data["primary_schema"]["bin_sizes"].__setitem__(
            0, int(data["primary_schema"]["bin_sizes"][0]) + 1
        ),
    )

    cases = [
        negative_case(
            "expected_schema_hash_mismatch",
            [
                "--manifest-only",
                "--out-dir",
                str(TMP / "expected_schema_hash_mismatch"),
                "--expected-schema-sha256",
                "0" * 64,
            ],
            "schema_sha256 mismatch",
        ),
        negative_case(
            "expected_builder_hash_mismatch",
            [
                "--manifest-only",
                "--out-dir",
                str(TMP / "expected_builder_hash_mismatch"),
                "--expected-builder-sha256",
                "0" * 64,
            ],
            "builder_script_sha256 mismatch",
        ),
        negative_case(
            "wrong_source_split",
            [
                "--manifest-only",
                "--schema",
                str(wrong_split),
                "--out-dir",
                str(TMP / "wrong_source_split_out"),
            ],
            "schema source_split must be train",
        ),
        negative_case(
            "source_hash_mismatch",
            [
                "--manifest-only",
                "--schema",
                str(source_hash_bad),
                "--out-dir",
                str(TMP / "source_hash_mismatch_out"),
            ],
            "input_ids_sha256 mismatch",
        ),
        negative_case(
            "q4_bin_size_mismatch",
            [
                "--manifest-only",
                "--schema",
                str(q4_bins_bad),
                "--out-dir",
                str(TMP / "q4_bin_size_mismatch_out"),
            ],
            "q4 bin sizes mismatch",
        ),
    ]
    guard = wording_guard()
    overall = "pass" if all(c["status"] == "pass" for c in cases) and guard["status"] == "pass" else "fail"
    result = {
        "artifact_kind": "maofield_q4_panel_negative_smoke",
        "artifact_version": "2026-06-22.d622.negative_smoke.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generator": str(GENERATOR.relative_to(REPO)),
        "schema": str(SCHEMA.relative_to(REPO)),
        "no_checkpoint_loaded": True,
        "no_training": True,
        "no_backward": True,
        "no_optimizer_step": True,
        "no_new_loss": True,
        "no_text_generation": True,
        "overall_status": overall,
        "cases": cases,
        "wording_guard": guard,
    }
    write_json(OUT_JSON, result)
    write_markdown(result)
    print(json.dumps({"overall_status": overall, "json": str(OUT_JSON), "md": str(OUT_MD)}, indent=2))
    if overall != "pass":
        sys.exit(1)


if __name__ == "__main__":
    main()
