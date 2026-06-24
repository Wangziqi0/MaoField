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
NULL_TESTS_CONTRACT_VERSION = "2026-06-24.fail_closed.v1"
RANK_SHADOW_HARD_FAIL = 0.10
RANK_SHADOW_STRICT_MIN = 0.25
RANDOM_NULL_MIN_DRAWS = 1000
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
NULL_KILL_PRIORITY = [
    "invalid_artifact",
    "killed_by_noise_floor",
    "killed_by_rank1_shadow",
    "killed_by_random_axis",
    "killed_by_coarsening",
    "insufficient_artifact",
]
COMMON_NULL_REQUIRED_KEYS = [
    "test_id",
    "contract_version",
    "computed_from",
    "schema_id",
    "weights_source",
    "parameters",
    "metrics",
    "thresholds",
    "stat_name",
    "primary_value",
    "null_distribution_summary",
    "empirical_p_or_quantile",
    "pass",
    "kill_verdict_if_fail",
    "reasons",
    "notes",
    "required_fields",
    "failure_behavior",
    "no_checkpoint_loaded_by_checker",
    "no_model_inference_by_checker",
    "no_training",
    "no_new_loss",
]
NULL_TEST_SPECS = {
    "matched_mean_slope": {
        "stat_name": "matched_residual_stability_after_global_mean_and_q4_slope",
        "kill_verdict": "killed_by_rank1_shadow",
        "fine_reason": "absorbed_by_mean_or_q4_slope",
        "required_metrics": [
            "global_mean",
            "q4_slope",
            "direction_alignment",
            "sign_consistency",
            "matched_z",
        ],
    },
    "random_equal_size_partition": {
        "stat_name": "true_tokenpos_axis_vs_equal_size_random_partitions",
        "kill_verdict": "killed_by_random_axis",
        "fine_reason": "true_axis_not_better_than_equal_size_random_axis",
        "required_metrics": ["n_draws", "true_axis_stat", "true_axis_quantile"],
        "min_draws": RANDOM_NULL_MIN_DRAWS,
    },
    "within_q_position_shuffle": {
        "stat_name": "q_local_position_label_shuffle_drop",
        "kill_verdict": "killed_by_random_axis",
        "fine_reason": "position_labels_do_not_matter_within_q",
        "required_metrics": ["n_draws", "true_stat", "shuffle_quantile", "median_drop_ratio"],
        "min_draws": RANDOM_NULL_MIN_DRAWS,
    },
    "bad_axis_audit_block_id": {
        "stat_name": "audit_block_id_bad_axis_control",
        "kill_verdict": "killed_by_random_axis",
        "fine_reason": "known_bad_axis_creates_comparable_signal",
        "required_metrics": ["true_axis_stat", "bad_axis_stat", "bad_axis_ratio_to_true"],
    },
    "same_dimension_random_subspace": {
        "stat_name": "true_9d_interaction_subspace_vs_random_9d_subspaces",
        "kill_verdict": "killed_by_random_axis",
        "fine_reason": "true_subspace_not_distinguishable_from_random_subspace",
        "required_metrics": [
            "ambient_dim",
            "candidate_dim",
            "n_draws",
            "true_subspace_stat",
            "true_subspace_quantile",
        ],
        "min_draws": RANDOM_NULL_MIN_DRAWS,
        "expected_dims": {"ambient_dim": CELL_COUNT, "candidate_dim": INTERACTION_DIMENSION},
    },
    "coarsen_refine_naturality": {
        "stat_name": "coarsening_projection_naturality_defect",
        "kill_verdict": "killed_by_coarsening",
        "fine_reason": "partition_artifact_or_naturality_failure",
        "required_metrics": ["max_relative_defect", "direction_retention_min"],
    },
    "principal_angle_stability": {
        "stat_name": "heldout_residual_subspace_principal_angle_stability",
        "kill_verdict": "insufficient_artifact",
        "fine_reason": "killed_by_subspace_instability",
        "required_metrics": ["median_max_angle_deg", "worst_max_angle_deg", "angle_quantile"],
    },
    "gluing_sanity": {
        "stat_name": "local_overlap_obstruction_after_nuisance_expansion",
        "kill_verdict": "killed_by_coarsening",
        "fine_reason": "gluing_mismatch_absorbed_by_local_nuisance",
        "required_metrics": [
            "obs_value",
            "obs_after_local_nuisance_expansion",
            "absorbed_by_local_nuisance",
        ],
    },
}


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


def required_null_names() -> list[str]:
    return list(NULL_TEST_SPECS)


def null_metric(block: dict[str, Any], name: str) -> Any:
    metrics = block.get("metrics", {})
    if isinstance(metrics, dict) and name in metrics:
        return metrics[name]
    params = block.get("parameters", {})
    if isinstance(params, dict) and name in params:
        return params[name]
    summary = block.get("null_distribution_summary", {})
    if isinstance(summary, dict) and name in summary:
        return summary[name]
    return None


def validate_null_tests(data: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "contract_version": data.get("null_tests_contract_version"),
        "expected_contract_version": NULL_TESTS_CONTRACT_VERSION,
        "required": required_null_names(),
        "present": [],
        "passed": [],
        "missing": [],
        "schema_errors": [],
        "invalid_errors": [],
        "failed": [],
    }
    if data.get("null_tests_contract_version") != NULL_TESTS_CONTRACT_VERSION:
        summary["schema_errors"].append(
            f"null_tests_contract_version must be {NULL_TESTS_CONTRACT_VERSION!r}"
        )
    nulls = data.get("null_tests", {})
    if not isinstance(nulls, dict):
        summary["schema_errors"].append("null_tests must be an object")
        summary["missing"] = required_null_names()
        return summary
    for name, spec in NULL_TEST_SPECS.items():
        block = nulls.get(name)
        if block is None:
            summary["missing"].append(name)
            continue
        summary["present"].append(name)
        schema_error_start = len(summary["schema_errors"])
        invalid_error_start = len(summary["invalid_errors"])
        if not isinstance(block, dict):
            summary["schema_errors"].append(f"{name}: block must be an object")
            continue
        missing_keys = [key for key in COMMON_NULL_REQUIRED_KEYS if key not in block]
        if missing_keys:
            summary["schema_errors"].append(f"{name}: missing required keys {missing_keys}")
            continue
        if block.get("test_id") != name:
            summary["schema_errors"].append(f"{name}: test_id must equal {name!r}")
        if block.get("contract_version") != NULL_TESTS_CONTRACT_VERSION:
            summary["schema_errors"].append(
                f"{name}: contract_version must be {NULL_TESTS_CONTRACT_VERSION!r}"
            )
        if block.get("schema_id") != EXPECTED_AGGREGATE_SCHEMA_ID:
            summary["schema_errors"].append(
                f"{name}: schema_id must be {EXPECTED_AGGREGATE_SCHEMA_ID!r}"
            )
        if block.get("stat_name") != spec["stat_name"]:
            summary["schema_errors"].append(f"{name}: stat_name mismatch")
        for guard in (
            "no_checkpoint_loaded_by_checker",
            "no_model_inference_by_checker",
            "no_training",
            "no_new_loss",
        ):
            if block.get(guard) is not True:
                summary["invalid_errors"].append(f"{name}: {guard} must be true")
        weights_source = block.get("weights_source")
        if not isinstance(weights_source, dict):
            summary["schema_errors"].append(f"{name}: weights_source must be an object")
        elif weights_source.get("outcome_independent") is not True:
            summary["invalid_errors"].append(
                f"{name}: weights_source must be outcome-independent"
            )
        computed_from = block.get("computed_from")
        if not isinstance(computed_from, dict):
            summary["schema_errors"].append(f"{name}: computed_from must be an object")
        elif computed_from.get("raw_jsonl_sha256") != data.get("raw_jsonl_sha256"):
            summary["invalid_errors"].append(f"{name}: computed_from.raw_jsonl_sha256 mismatch")
        for object_key in (
            "parameters",
            "metrics",
            "thresholds",
            "primary_value",
            "null_distribution_summary",
            "empirical_p_or_quantile",
            "failure_behavior",
        ):
            if not isinstance(block.get(object_key), dict):
                summary["schema_errors"].append(f"{name}: {object_key} must be an object")
        if not isinstance(block.get("required_fields"), list):
            summary["schema_errors"].append(f"{name}: required_fields must be a list")
        if not isinstance(block.get("reasons"), list):
            summary["schema_errors"].append(f"{name}: reasons must be a list")
        null_summary = block.get("null_distribution_summary", {})
        if isinstance(null_summary, dict):
            if not isinstance(null_summary.get("method"), str) or not null_summary.get("method"):
                summary["schema_errors"].append(f"{name}: null_distribution_summary.method missing")
            if null_summary.get("direction") not in (
                "higher_is_better",
                "lower_is_better",
                "two_sided",
            ):
                summary["schema_errors"].append(
                    f"{name}: null_distribution_summary.direction invalid"
                )
        metrics = block.get("metrics", {})
        if isinstance(metrics, dict):
            missing_metrics = [
                metric for metric in spec["required_metrics"] if metric not in metrics
            ]
            if missing_metrics:
                summary["schema_errors"].append(
                    f"{name}: missing required metrics {missing_metrics}"
                )
        kill = block.get("kill_verdict_if_fail")
        if not isinstance(kill, dict):
            summary["schema_errors"].append(f"{name}: kill_verdict_if_fail must be an object")
            final_verdict = None
        else:
            final_verdict = kill.get("final_verdict")
            if final_verdict not in ALLOWED_VERDICTS or final_verdict == "eligible_for_next_design_review_only":
                summary["schema_errors"].append(f"{name}: invalid kill_verdict_if_fail.final_verdict")
            elif final_verdict != spec["kill_verdict"]:
                summary["schema_errors"].append(
                    f"{name}: kill verdict must be {spec['kill_verdict']!r}"
                )
        if "min_draws" in spec:
            n_draws = null_metric(block, "n_draws")
            if not isinstance(n_draws, int) or n_draws < int(spec["min_draws"]):
                summary["schema_errors"].append(
                    f"{name}: n_draws must be an integer >= {spec['min_draws']}"
                )
        dims = spec.get("expected_dims", {})
        if isinstance(metrics, dict):
            for metric, expected in dims.items():
                if metrics.get(metric) != expected:
                    summary["invalid_errors"].append(
                        f"{name}: {metric} must be {expected}, got {metrics.get(metric)!r}"
                    )
        if name == "gluing_sanity" and isinstance(metrics, dict):
            if not isinstance(metrics.get("absorbed_by_local_nuisance"), bool):
                summary["schema_errors"].append(
                    "gluing_sanity: absorbed_by_local_nuisance must be boolean"
                )
        passed = block.get("pass")
        if not isinstance(passed, bool):
            summary["schema_errors"].append(f"{name}: pass must be boolean")
        elif not passed:
            summary["failed"].append(
                {
                    "name": name,
                    "final_verdict": final_verdict or spec["kill_verdict"],
                    "fine_reason": kill.get("fine_reason", spec["fine_reason"])
                    if isinstance(kill, dict)
                    else spec["fine_reason"],
                    "reasons": block.get("reasons", []),
                }
            )
        elif (
            len(summary["schema_errors"]) == schema_error_start
            and len(summary["invalid_errors"]) == invalid_error_start
        ):
            summary["passed"].append(name)
    return summary


def highest_priority_null_failure(failed: list[dict[str, Any]]) -> tuple[str, list[str]]:
    by_verdict: dict[str, list[dict[str, Any]]] = {}
    for item in failed:
        by_verdict.setdefault(str(item.get("final_verdict")), []).append(item)
    for verdict in NULL_KILL_PRIORITY:
        if verdict in by_verdict:
            reasons = [
                f"{item['name']} failed: {item.get('fine_reason', 'null test failed')}"
                for item in by_verdict[verdict]
            ]
            return verdict, reasons
    return "insufficient_artifact", ["one or more null tests failed"]


def verdict_from_checks(
    metadata_errors: list[str],
    row_errors: list[str],
    null_summary: dict[str, Any],
    stats: dict[str, Any] | None,
) -> tuple[str, list[str]]:
    if metadata_errors or row_errors:
        return "invalid_artifact", metadata_errors + row_errors
    if stats is None:
        return "insufficient_artifact", ["no interaction statistics computed"]
    ratio = stats.get("interaction_to_noise_median_ratio")
    sigma2_ratio = stats.get("weighted_uncentered_sigma2_over_sigma1")
    if null_summary["invalid_errors"]:
        return "invalid_artifact", null_summary["invalid_errors"]
    if null_summary["missing"]:
        return "insufficient_artifact", [
            f"missing preregistered null test: {name}" for name in null_summary["missing"]
        ]
    if null_summary["schema_errors"]:
        return "insufficient_artifact", null_summary["schema_errors"]
    if ratio is not None and ratio <= 1.0:
        return "killed_by_noise_floor", ["median interaction norm is at or below estimated noise floor"]
    if sigma2_ratio is not None and sigma2_ratio < RANK_SHADOW_STRICT_MIN:
        threshold_note = (
            f"below hard rank-1 shadow floor {RANK_SHADOW_HARD_FAIL}"
            if sigma2_ratio < RANK_SHADOW_HARD_FAIL
            else f"below strict design-review floor {RANK_SHADOW_STRICT_MIN}"
        )
        return "killed_by_rank1_shadow", [
            f"weighted sigma2/sigma1={sigma2_ratio:.6g} is {threshold_note}"
        ]
    if null_summary["failed"]:
        return highest_priority_null_failure(null_summary["failed"])
    return "eligible_for_next_design_review_only", [
        "all required provenance fields, rows, statistics, and structured null-test result blocks are present and pass",
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
    try:
        data = load_json(aggregate_path)
    except FileNotFoundError:
        result = empty_result(f"aggregate path does not exist: {aggregate_path}", schema_path)
        result["aggregate_path"] = str(aggregate_path)
        return result
    except json.JSONDecodeError as exc:
        return {
            "generated_utc": utc_now(),
            "aggregate_path": str(aggregate_path),
            "final_verdict": "invalid_artifact",
            "reasons": [f"aggregate is not valid JSON: {exc}"],
            "allowed_verdicts": ALLOWED_VERDICTS,
            "blocked_claims": BLOCKED_CLAIMS,
            "no_checkpoint_loaded": True,
            "no_model_inference": True,
            "no_training": True,
            "no_new_loss": True,
        }
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
    null_summary = validate_null_tests(data)
    verdict, reasons = verdict_from_checks(metadata_errors, row_errors, null_summary, stats)
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
        "null_test_summary": null_summary,
        "no_checkpoint_loaded": True,
        "no_model_inference": True,
        "no_training": True,
        "no_new_loss": True,
    }


def null_test_template(name: str, spec: dict[str, Any], raw_jsonl_sha256: str) -> dict[str, Any]:
    return {
        "test_id": name,
        "contract_version": NULL_TESTS_CONTRACT_VERSION,
        "computed_from": {
            "raw_jsonl_sha256": raw_jsonl_sha256,
            "aggregate_schema_id": EXPECTED_AGGREGATE_SCHEMA_ID,
            "source": "future full-panel aggregate only",
        },
        "schema_id": EXPECTED_AGGREGATE_SCHEMA_ID,
        "weights_source": {
            "kind": "source_only_weights",
            "outcome_independent": True,
        },
        "parameters": {
            "preregistered": True,
            "n_draws": spec.get("min_draws"),
        },
        "metrics": {
            metric: f"<future {metric}>"
            for metric in spec["required_metrics"]
        },
        "thresholds": {
            "pass_rule": "<future preregistered threshold>",
            "multiplicity_adjustment": "<none | holm | maxT | preregistered_other>",
        },
        "stat_name": spec["stat_name"],
        "primary_value": {
            "field_or_formula": "<future machine-readable statistic path or formula>"
        },
        "null_distribution_summary": {
            "method": "<future source-only null construction>",
            "n_draws": spec.get("min_draws"),
            "statistic": spec["stat_name"],
            "direction": "higher_is_better",
            "quantiles": {
                "p05": "<finite number>",
                "p50": "<finite number>",
                "p90": "<finite number>",
                "p95": "<finite number>",
                "p99": "<finite number>",
            },
            "mean": "<finite number or null>",
            "sd": "<finite number or null>",
            "multiplicity_adjustment": "<none | holm | maxT | preregistered_other>",
            "random_seed_or_manifest": "<future seed or manifest digest>",
            "provenance": ["<source-only field list>"],
        },
        "empirical_p_or_quantile": {
            "type": "<upper_quantile | lower_tail | two_sided | ratio>",
            "value": "<finite number>",
        },
        "pass": "<future boolean>",
        "kill_verdict_if_fail": {
            "final_verdict": spec["kill_verdict"],
            "fine_reason": spec["fine_reason"],
        },
        "reasons": [],
        "notes": "Design-only future null-test block; notes cannot override pass=false.",
        "required_fields": spec["required_metrics"],
        "failure_behavior": {
            "missing": "insufficient_artifact",
            "malformed": "invalid_artifact",
            "pass_false": spec["kill_verdict"],
        },
        "no_checkpoint_loaded_by_checker": True,
        "no_model_inference_by_checker": True,
        "no_training": True,
        "no_new_loss": True,
    }


def template(schema_path: Path) -> dict[str, Any]:
    schema_id, schema_weights = load_schema_weights(schema_path)
    raw_jsonl_sha256 = "<sha256 of raw token-level panel or manifest digest>"
    return {
        "artifact_kind": "maofield_q4_tokenpos4_interaction_full_panel_aggregate",
        "aggregate_schema_id": EXPECTED_AGGREGATE_SCHEMA_ID,
        "null_tests_contract_version": NULL_TESTS_CONTRACT_VERSION,
        "repo_head": "<git head used by the future aggregate builder>",
        "builder_script_sha256": "<sha256 of future aggregate builder script>",
        "raw_jsonl_sha256": raw_jsonl_sha256,
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
            name: null_test_template(name, spec, raw_jsonl_sha256)
            for name, spec in NULL_TEST_SPECS.items()
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
