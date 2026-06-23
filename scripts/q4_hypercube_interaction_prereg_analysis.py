#!/usr/bin/env python3
"""Future-only q4 x token-position interaction prereg analysis gate.

This script consumes a provenance-checked future aggregate only. It does not
load checkpoints, run inference, train, generate a full panel, or authorize a
new loss. Its strongest possible verdict is
`eligible_for_next_design_review_only`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
DEFAULT_SCHEMA = REPO / "docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json"
EXPECTED_AGGREGATE_SCHEMA_ID = "q4_tokenpos4_interaction_full_panel_20260623"
EXPECTED_HYPERCUBE_SCHEMA_ID = "q4_tokenpos4_hypercube_20260623"
EXPECTED_Q4_SCHEMA_ID = "freq_q4_audit_targets_20260622"
EXPECTED_SEEDS = [1, 2, 3, 4, 42]
EXPECTED_GENERATIONS = list(range(10))
EXPECTED_ROW_COUNT = len(EXPECTED_SEEDS) * len(EXPECTED_GENERATIONS)
CELL_COUNT = 16
INTERACTION_DIMENSION = 9
ALLOWED_VERDICTS = [
    "invalid_artifact",
    "killed_by_noise_floor",
    "killed_by_random_axis",
    "killed_by_rank1_shadow",
    "killed_by_coarsening",
    "insufficient_artifact",
    "eligible_for_next_design_review_only",
]
BLOCKED_CLAIMS = [
    "interaction_field_observed",
    "hypercube_residual_observed",
    "residual_field_observed",
    "LOSO_passed",
    "F3_positive",
    "glass_box_broken",
    "training_authorized",
    "new_loss_authorized",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def finite_float(value: Any, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return out


def flatten_4x4(value: Any, name: str) -> list[float]:
    if isinstance(value, list) and len(value) == 4 and all(isinstance(row, list) for row in value):
        flat = [item for row in value for item in row]
    else:
        flat = value
    if not isinstance(flat, list) or len(flat) != CELL_COUNT:
        raise ValueError(f"{name} must be a length-16 list or 4x4 nested list")
    return [finite_float(item, name) for item in flat]


def load_schema_weights(schema_path: Path) -> tuple[str, list[float]]:
    schema = load_json(schema_path)
    schema_id = schema.get("hypercube", {}).get("schema_id", "")
    cells = schema.get("hypercube", {}).get("cells", [])
    if schema_id != EXPECTED_HYPERCUBE_SCHEMA_ID:
        raise ValueError(f"unexpected hypercube schema_id {schema_id!r}")
    ordered = sorted(cells, key=lambda item: (int(item["slice_id"]), int(item["position_bin"])))
    weights = [finite_float(item["weight"], "schema weight") for item in ordered]
    total = sum(weights)
    if total <= 0:
        raise ValueError("schema weights must have positive sum")
    return schema_id, [weight / total for weight in weights]


def additive_design() -> np.ndarray:
    rows = []
    for q_id in range(4):
        for b_id in range(4):
            rows.append(
                [1.0]
                + [1.0 if q_id == q else 0.0 for q in range(3)]
                + [1.0 if b_id == b else 0.0 for b in range(3)]
            )
    return np.asarray(rows, dtype=float)


def weighted_project_additive(k: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = additive_design()
    sqrt_w = np.sqrt(weights)
    beta = np.linalg.lstsq(x * sqrt_w[:, None], k * sqrt_w, rcond=None)[0]
    fit = x @ beta
    return fit, k - fit


def weighted_norm(vector: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(float(np.sum(weights * vector * vector)))


def validate_metadata(data: dict[str, Any], schema_id: str, schema_weights: list[float]) -> list[str]:
    errors = []
    if "slice_rows" in data and "rows" not in data:
        errors.append("old q4 rare/freq aggregate is not accepted as q4 x tokenpos4 full-panel input")
    required = [
        "artifact_kind",
        "aggregate_schema_id",
        "repo_head",
        "builder_script_sha256",
        "raw_jsonl_sha256",
        "axis_definitions",
        "source_only_weights",
        "rows",
    ]
    for key in required:
        if key not in data:
            errors.append(f"missing top-level field: {key}")
    if errors:
        return errors
    if data.get("artifact_kind") != "maofield_q4_tokenpos4_interaction_full_panel_aggregate":
        errors.append("artifact_kind mismatch")
    if data.get("aggregate_schema_id") != EXPECTED_AGGREGATE_SCHEMA_ID:
        errors.append("aggregate_schema_id mismatch")
    axis = data.get("axis_definitions", {})
    if axis.get("hypercube_schema_id") != schema_id:
        errors.append("axis_definitions.hypercube_schema_id mismatch")
    if axis.get("q4_schema_id") != EXPECTED_Q4_SCHEMA_ID:
        errors.append("axis_definitions.q4_schema_id mismatch")
    if axis.get("token_position_axis") != "B_tokenpos4":
        errors.append("axis_definitions.token_position_axis must be B_tokenpos4")
    try:
        weights = flatten_4x4(data["source_only_weights"], "source_only_weights")
    except Exception as exc:
        errors.append(str(exc))
        return errors
    total = sum(weights)
    if total <= 0:
        errors.append("source_only_weights must have positive sum")
    normalized = [weight / total for weight in weights]
    max_diff = max(abs(left - right) for left, right in zip(normalized, schema_weights))
    if max_diff > 1e-12:
        errors.append(f"source_only_weights do not match schema weights, max diff {max_diff:.3g}")
    for digest_field in ("builder_script_sha256", "raw_jsonl_sha256"):
        value = str(data.get(digest_field, ""))
        if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value.lower()):
            errors.append(f"{digest_field} must be a lowercase sha256 hex digest")
    return errors


def normalize_rows(rows: Any) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(rows, list):
        return [], ["rows must be a list"]
    normalized = []
    errors = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"rows[{idx}] must be an object")
            continue
        if "F3_slice_gap" in row and "cell_mean_logprob" not in row:
            errors.append("old rare/freq aggregate rows are not accepted")
            continue
        try:
            counts = flatten_4x4(row["cell_counts"], "cell_counts")
            means = flatten_4x4(row["cell_mean_logprob"], "cell_mean_logprob")
            variances = flatten_4x4(row.get("cell_var_logprob", [None] * CELL_COUNT), "cell_var_logprob")
            if any(count <= 0 for count in counts):
                raise ValueError("cell_counts must all be positive")
            if any(var < 0 for var in variances):
                raise ValueError("cell_var_logprob must be non-negative")
            normalized.append(
                {
                    "seed": int(row["seed"]),
                    "generation": int(row["generation"]),
                    "checkpoint_identity": row.get("checkpoint_identity", {}),
                    "cell_counts": counts,
                    "cell_mean_logprob": means,
                    "cell_var_logprob": variances,
                }
            )
        except Exception as exc:
            errors.append(f"rows[{idx}]: {exc}")
    return normalized, errors


def validate_full_panel_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors = []
    if len(rows) != EXPECTED_ROW_COUNT:
        errors.append(f"expected {EXPECTED_ROW_COUNT} checkpoint rows, got {len(rows)}")
    got = {(row["seed"], row["generation"]) for row in rows}
    expected = {(seed, gen) for seed in EXPECTED_SEEDS for gen in EXPECTED_GENERATIONS}
    missing = sorted(expected - got)
    extra = sorted(got - expected)
    if missing:
        errors.append(f"missing seed/generation rows: {missing[:10]}")
    if extra:
        errors.append(f"unexpected seed/generation rows: {extra[:10]}")
    return errors


def interaction_statistics(rows: list[dict[str, Any]], weights: list[float]) -> dict[str, Any]:
    w = np.asarray(weights, dtype=float)
    residuals = []
    norms = []
    noise_floors = []
    for row in sorted(rows, key=lambda item: (item["seed"], item["generation"])):
        k = np.asarray(row["cell_mean_logprob"], dtype=float)
        _, residual = weighted_project_additive(k, w)
        residuals.append(residual)
        norms.append(weighted_norm(residual, w))
        variances = np.asarray(row["cell_var_logprob"], dtype=float)
        counts = np.asarray(row["cell_counts"], dtype=float)
        noise = math.sqrt(float(np.sum(w * variances / counts)))
        noise_floors.append(noise)
    matrix = np.vstack([residual * np.sqrt(w) for residual in residuals])
    singular = np.linalg.svd(matrix, compute_uv=False)
    sigma2_ratio = None
    if len(singular) > 1 and singular[0] > 0:
        sigma2_ratio = float(singular[1] / singular[0])
    return {
        "object": "I_i = Pi_{A_perp,w} K_i",
        "ambient_dimension": CELL_COUNT,
        "strict_additive_dimension": 7,
        "interaction_dimension": INTERACTION_DIMENSION,
        "interaction_norm_summary": {
            "min": float(np.min(norms)),
            "median": float(np.median(norms)),
            "max": float(np.max(norms)),
        },
        "noise_floor_summary": {
            "min": float(np.min(noise_floors)),
            "median": float(np.median(noise_floors)),
            "max": float(np.max(noise_floors)),
        },
        "interaction_to_noise_median_ratio": (
            float(np.median(norms) / np.median(noise_floors))
            if np.median(noise_floors) > 0
            else None
        ),
        "weighted_uncentered_singular_values": singular.tolist(),
        "weighted_uncentered_sigma2_over_sigma1": sigma2_ratio,
    }


def required_nulls(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    nulls = data.get("null_tests", {})
    if not isinstance(nulls, dict):
        return [], ["null_tests must be an object"]
    required = [
        "matched_mean_slope",
        "random_equal_size_partition",
        "within_q_position_shuffle",
        "bad_axis_audit_block_id",
        "same_dimension_random_subspace",
        "coarsen_refine_naturality",
        "principal_angle_stability",
        "gluing_sanity",
    ]
    missing = [name for name in required if name not in nulls]
    return required, missing


def verdict_from_checks(metadata_errors: list[str], row_errors: list[str], null_missing: list[str], stats: dict[str, Any] | None) -> tuple[str, list[str]]:
    if metadata_errors or row_errors:
        return "invalid_artifact", metadata_errors + row_errors
    if stats is None:
        return "insufficient_artifact", ["no interaction statistics computed"]
    ratio = stats.get("interaction_to_noise_median_ratio")
    sigma2_ratio = stats.get("weighted_uncentered_sigma2_over_sigma1")
    if ratio is not None and ratio <= 1.0:
        return "killed_by_noise_floor", ["median interaction norm is at or below estimated noise floor"]
    if sigma2_ratio is not None and sigma2_ratio < 0.10:
        return "killed_by_rank1_shadow", ["singular spectrum is too close to a rank-1 scalar shadow"]
    if null_missing:
        return "insufficient_artifact", [f"missing preregistered null test: {name}" for name in null_missing]
    return "eligible_for_next_design_review_only", [
        "all required provenance fields, rows, statistics, and null-test result blocks are present",
        "this is not a scientific claim and still requires strict review",
    ]


def empty_result(reason: str, schema_path: Path) -> dict[str, Any]:
    return {
        "generated_utc": utc_now(),
        "script": "scripts/q4_hypercube_interaction_prereg_analysis.py",
        "schema_path": str(schema_path),
        "final_verdict": "insufficient_artifact",
        "allowed_verdicts": ALLOWED_VERDICTS,
        "blocked_claims": BLOCKED_CLAIMS,
        "reasons": [reason],
        "no_checkpoint_loaded": True,
        "no_model_inference": True,
        "no_training": True,
        "no_new_loss": True,
    }


def analyze_aggregate(aggregate_path: Path, schema_path: Path) -> dict[str, Any]:
    schema_id, schema_weights = load_schema_weights(schema_path)
    data = load_json(aggregate_path)
    if not isinstance(data, dict):
        return {
            "generated_utc": utc_now(),
            "aggregate_path": str(aggregate_path),
            "aggregate_sha256": sha256_file(aggregate_path),
            "final_verdict": "invalid_artifact",
            "reasons": ["aggregate root must be a JSON object"],
            "allowed_verdicts": ALLOWED_VERDICTS,
            "blocked_claims": BLOCKED_CLAIMS,
        }
    metadata_errors = validate_metadata(data, schema_id, schema_weights)
    rows, row_errors = normalize_rows(data.get("rows", []))
    row_errors.extend(validate_full_panel_rows(rows))
    stats = None
    if not metadata_errors and not row_errors:
        stats = interaction_statistics(rows, schema_weights)
    _, null_missing = required_nulls(data)
    verdict, reasons = verdict_from_checks(metadata_errors, row_errors, null_missing, stats)
    return {
        "generated_utc": utc_now(),
        "script": "scripts/q4_hypercube_interaction_prereg_analysis.py",
        "aggregate_path": str(aggregate_path),
        "aggregate_sha256": sha256_file(aggregate_path),
        "schema_path": str(schema_path),
        "schema_sha256": sha256_file(schema_path),
        "final_verdict": verdict,
        "reasons": reasons,
        "allowed_verdicts": ALLOWED_VERDICTS,
        "blocked_claims": BLOCKED_CLAIMS,
        "row_count": len(rows),
        "interaction_statistics": stats,
        "missing_null_tests": null_missing,
        "no_checkpoint_loaded": True,
        "no_model_inference": True,
        "no_training": True,
        "no_new_loss": True,
    }


def template(schema_path: Path) -> dict[str, Any]:
    schema_id, schema_weights = load_schema_weights(schema_path)
    return {
        "artifact_kind": "maofield_q4_tokenpos4_interaction_full_panel_aggregate",
        "aggregate_schema_id": EXPECTED_AGGREGATE_SCHEMA_ID,
        "repo_head": "<git head used by the future aggregate builder>",
        "builder_script_sha256": "<sha256 of future aggregate builder script>",
        "raw_jsonl_sha256": "<sha256 of raw token-level panel or manifest digest>",
        "axis_definitions": {
            "hypercube_schema_id": schema_id,
            "q4_schema_id": EXPECTED_Q4_SCHEMA_ID,
            "cell_set": "Q_freq4 x B_tokenpos4",
            "token_position_axis": "B_tokenpos4",
            "position_bin_policy": "min(3, (token_pos - 1) * 4 // 63)",
        },
        "source_only_weights": schema_weights,
        "rows": [
            {
                "seed": EXPECTED_SEEDS[0],
                "generation": EXPECTED_GENERATIONS[0],
                "checkpoint_identity": {"path": "<future checkpoint identity only, no loading here>"},
                "cell_counts": ["<positive count>"] * CELL_COUNT,
                "cell_mean_logprob": ["<finite mean>"] * CELL_COUNT,
                "cell_var_logprob": ["<non-negative variance>"] * CELL_COUNT,
            }
        ],
        "null_tests": {
            "matched_mean_slope": "<future result block>",
            "random_equal_size_partition": "<future result block>",
            "within_q_position_shuffle": "<future result block>",
            "bad_axis_audit_block_id": "<future result block>",
            "same_dimension_random_subspace": "<future result block>",
            "coarsen_refine_naturality": "<future result block>",
            "principal_angle_stability": "<future result block>",
            "gluing_sanity": "<future result block>",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aggregate", type=Path, help="future provenance-checked q4 x tokenpos4 aggregate")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--out", type=Path, help="optional JSON output path")
    parser.add_argument("--emit-template", action="store_true", help="print the expected future aggregate shape")
    args = parser.parse_args()

    if args.emit_template:
        result = template(args.schema)
    elif args.aggregate is None:
        result = empty_result("no future full-panel aggregate was provided", args.schema)
    else:
        result = analyze_aggregate(args.aggregate, args.schema)

    if args.out:
        write_json(args.out, result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
