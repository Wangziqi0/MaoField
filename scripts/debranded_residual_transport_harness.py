#!/usr/bin/env python3
"""Seven-block zero-GPU harness for finite weighted residual transport.

This script starts the debranded mathematics direction on toy finite systems.
It does not read MaoField aggregates, load checkpoints, run inference, train,
or authorize a new loss.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


RANK_SHADOW_FLOOR = 0.25


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def normalize(weights: np.ndarray) -> np.ndarray:
    weights = np.asarray(weights, dtype=float).reshape(-1)
    if np.any(weights <= 0):
        raise ValueError("weights must be positive")
    return weights / float(np.sum(weights))


def weighted_norm(v: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(float(np.sum(weights * v * v)))


def weighted_project(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    basis = np.asarray(basis, dtype=float)
    v = np.asarray(v, dtype=float).reshape(-1)
    sqrt_w = np.sqrt(weights)
    coef = np.linalg.lstsq(basis * sqrt_w[:, None], v * sqrt_w, rcond=None)[0]
    return basis @ coef


def residual(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.asarray(v, dtype=float).reshape(-1) - weighted_project(v, basis, weights)


def additive_design(nq: int, nb: int, include_q: bool = True, include_b: bool = True) -> np.ndarray:
    rows: list[list[float]] = []
    for q_id in range(nq):
        for b_id in range(nb):
            row = [1.0]
            if include_q:
                row.extend(1.0 if q_id == q else 0.0 for q in range(max(0, nq - 1)))
            if include_b:
                row.extend(1.0 if b_id == b else 0.0 for b in range(max(0, nb - 1)))
            rows.append(row)
    return np.asarray(rows, dtype=float)


def product_from_marginals(weights: np.ndarray, nq: int, nb: int) -> np.ndarray:
    table = weights.reshape(nq, nb)
    q = table.sum(axis=1)
    b = table.sum(axis=0)
    return np.outer(q, b).reshape(-1)


def grid_weights(nq: int, nb: int) -> np.ndarray:
    return np.full(nq * nb, 1.0 / (nq * nb), dtype=float)


def coarsen_matrix(
    nq: int,
    nb: int,
    q_groups: list[list[int]],
    b_groups: list[list[int]],
    fine_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    rows = []
    coarse_weights = []
    for q_group in q_groups:
        for b_group in b_groups:
            idx = [q * nb + b for q in q_group for b in b_group]
            weight_sum = float(np.sum(fine_weights[idx]))
            row = np.zeros(nq * nb, dtype=float)
            row[idx] = fine_weights[idx] / weight_sum
            rows.append(row)
            coarse_weights.append(weight_sum)
    return np.vstack(rows), normalize(np.asarray(coarse_weights, dtype=float))


def interaction_field(nq: int, nb: int, second_direction: bool = False) -> np.ndarray:
    q = np.linspace(-1.0, 1.0, nq)
    b = np.linspace(-1.0, 1.0, nb)
    field = np.outer(q, b)
    if second_direction:
        q2 = np.array([1.0, -1.0, -1.0, 1.0], dtype=float)[:nq]
        b2 = b * b - np.mean(b * b)
        field = field + 0.65 * np.outer(q2, b2)
    return field.reshape(-1)


def mixed_field_with_main_effects() -> np.ndarray:
    interaction = interaction_field(4, 4, second_direction=True).reshape(4, 4)
    q_main = np.linspace(-0.6, 0.6, 4)[:, None]
    b_main = np.array([-0.9, -0.2, 0.3, 1.1])[None, :]
    q_block = np.array([-1.0, -1.0, 1.0, 1.0])[:, None]
    b_block = np.array([-1.0, -1.0, 1.0, 1.0])[None, :]
    coarse_block_interaction = 0.75 * (q_block @ b_block)
    return (interaction + q_main + b_main + coarse_block_interaction).reshape(-1)


def edge_defect(
    v: np.ndarray,
    c: np.ndarray,
    coarse_weights: np.ndarray,
    fine_basis: np.ndarray,
    coarse_basis: np.ndarray,
    fine_weights: np.ndarray,
) -> dict[str, float]:
    left = c @ residual(v, fine_basis, fine_weights)
    right = residual(c @ v, coarse_basis, coarse_weights)
    defect = left - right
    denom = max(weighted_norm(left, coarse_weights), weighted_norm(right, coarse_weights), 1e-12)
    absolute = weighted_norm(defect, coarse_weights)
    return {
        "absolute_defect_norm": absolute,
        "relative_defect_norm": absolute / denom,
    }


def block_non_product_weighted_projection() -> dict[str, Any]:
    nq, nb = 2, 3
    observed = normalize(np.array([[0.10, 0.05, 0.20], [0.25, 0.08, 0.32]]))
    product = product_from_marginals(observed, nq, nb)
    basis = additive_design(nq, nb)
    k = np.array([0.2, -0.4, 1.0, -0.8, 0.7, 0.1], dtype=float)
    r_observed = residual(k, basis, observed)
    r_product = residual(k, basis, product)
    diff = weighted_norm(r_observed - r_product, observed)
    max_abs_error = float(np.max(np.abs(observed - product)))
    return {
        "test_id": "non_product_weighted_projection",
        "observed_minus_product_max_abs": max_abs_error,
        "residual_difference_norm_under_observed_weight": diff,
        "pass": max_abs_error > 1e-3 and diff > 1e-3,
        "interpretation": (
            "positive non-product weights change the weighted projection residual; "
            "current legal language is projection residual, not canonical product Hoeffding"
        ),
    }


def block_edge_defect() -> dict[str, Any]:
    v = mixed_field_with_main_effects()
    w44 = grid_weights(4, 4)
    c, w22 = coarsen_matrix(4, 4, [[0, 1], [2, 3]], [[0, 1], [2, 3]], w44)
    natural = edge_defect(v, c, w22, additive_design(4, 4), additive_design(2, 2), w44)
    bad = edge_defect(
        v,
        c,
        w22,
        additive_design(4, 4),
        additive_design(2, 2, include_q=True, include_b=False),
        w44,
    )
    return {
        "test_id": "edge_defect",
        "natural_relative_defect_norm": natural["relative_defect_norm"],
        "bad_nuisance_relative_defect_norm": bad["relative_defect_norm"],
        "pass": natural["relative_defect_norm"] < 1e-10 and bad["relative_defect_norm"] > 1e-6,
        "interpretation": "edge defects detect nuisance/coarsening incompatibility",
    }


def block_square_holonomy() -> dict[str, Any]:
    v = mixed_field_with_main_effects()
    w44 = grid_weights(4, 4)
    p44 = additive_design(4, 4)
    cq44, w24 = coarsen_matrix(4, 4, [[0, 1], [2, 3]], [[0], [1], [2], [3]], w44)
    cb44, w42 = coarsen_matrix(4, 4, [[0], [1], [2], [3]], [[0, 1], [2, 3]], w44)
    cb24, w22_a = coarsen_matrix(2, 4, [[0], [1]], [[0, 1], [2, 3]], w24)
    cq42, w22_b = coarsen_matrix(4, 2, [[0, 1], [2, 3]], [[0], [1]], w42)
    if not np.allclose(w22_a, w22_b):
        raise ValueError("coarse square weights disagree")
    p24 = additive_design(2, 4)
    p42 = additive_design(4, 2)
    q_first = cb24 @ residual(cq44 @ residual(v, p44, w44), p24, w24)
    b_first = cq42 @ residual(cb44 @ residual(v, p44, w44), p42, w42)
    natural_h = weighted_norm(q_first - b_first, w22_a)
    extra24 = np.array([-1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0], dtype=float)
    p24_bad = np.column_stack([p24, extra24])
    q_bad = cb24 @ residual(cq44 @ residual(v, p44, w44), p24_bad, w24)
    b_bad = b_first
    bad_h = weighted_norm(q_bad - b_bad, w22_a)
    return {
        "test_id": "square_holonomy",
        "natural_square_holonomy_norm": natural_h,
        "bad_nuisance_square_holonomy_norm": bad_h,
        "pass": natural_h < 1e-10 and bad_h > 1e-6,
        "interpretation": "compatible projected paths close; non-functorial nuisance opens holonomy",
    }


def singular_ratio(vectors: np.ndarray, weights: np.ndarray) -> tuple[list[float], float | None]:
    matrix = vectors * np.sqrt(weights)[None, :]
    singular = np.linalg.svd(matrix, compute_uv=False)
    ratio = None
    if len(singular) > 1 and singular[0] > 0:
        ratio = float(singular[1] / singular[0])
    return singular.tolist(), ratio


def block_rank_shadow_guard() -> dict[str, Any]:
    w = grid_weights(4, 4)
    one = interaction_field(4, 4)
    two = interaction_field(4, 4, second_direction=True)
    rank1_vectors = np.vstack([scale * one for scale in [0.7, 1.0, 1.3, 1.6]])
    multi_vectors = np.vstack([one, two, one - 0.5 * two, 0.4 * one + two])
    rank1_sv, rank1_ratio = singular_ratio(rank1_vectors, w)
    multi_sv, multi_ratio = singular_ratio(multi_vectors, w)
    return {
        "test_id": "rank_shadow_guard",
        "rank1_singular_values": rank1_sv,
        "rank1_sigma2_over_sigma1": rank1_ratio,
        "multidirectional_singular_values": multi_sv,
        "multidirectional_sigma2_over_sigma1": multi_ratio,
        "floor": RANK_SHADOW_FLOOR,
        "pass": (rank1_ratio or 0.0) < 1e-10 and (multi_ratio or 0.0) >= RANK_SHADOW_FLOOR,
        "interpretation": "rank-1 templates are killed; two-direction toy residual clears the design floor",
    }


def orthonormal_basis(vectors: np.ndarray, weights: np.ndarray, dim: int) -> np.ndarray:
    matrix = vectors * np.sqrt(weights)[None, :]
    _, _, vt = np.linalg.svd(matrix, full_matrices=False)
    return vt[:dim] / np.sqrt(weights)[None, :]


def weighted_projection_energy(v: np.ndarray, basis_rows: np.ndarray, weights: np.ndarray) -> float:
    projected = weighted_project(v, basis_rows.T, weights)
    denom = weighted_norm(v, weights)
    return 0.0 if denom == 0 else weighted_norm(projected, weights) / denom


def block_random_subspace_guard(seed: int, draws: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    weights = grid_weights(4, 4)
    one = interaction_field(4, 4)
    two = interaction_field(4, 4, second_direction=True)
    train = np.vstack([one, two, one + 0.25 * two])
    heldout = 0.75 * one - 0.5 * two
    true_basis = orthonormal_basis(train, weights, dim=2)
    true_capture = weighted_projection_energy(heldout, true_basis, weights)
    random_capture = []
    for _ in range(draws):
        random_basis = orthonormal_basis(rng.normal(size=(2, 16)), weights, dim=2)
        random_capture.append(weighted_projection_energy(heldout, random_basis, weights))
    random_arr = np.asarray(random_capture, dtype=float)
    p95 = float(np.quantile(random_arr, 0.95))
    quantile = float(np.mean(random_arr <= true_capture))
    return {
        "test_id": "random_subspace_guard",
        "draws": draws,
        "true_subspace_capture_ratio": true_capture,
        "random_capture_mean": float(np.mean(random_arr)),
        "random_capture_p95": p95,
        "true_capture_quantile": quantile,
        "pass": true_capture > p95 and quantile >= 0.95,
        "interpretation": "named toy subspace must beat random same-dimensional subspaces",
    }


def block_gluing_absorption() -> dict[str, Any]:
    weights = grid_weights(2, 2)
    nuisance = additive_design(2, 2)
    absorbed = np.array([1.0, 2.0, 1.5, 2.5], dtype=float)
    obstruction = np.array([1.0, -1.0, -1.0, 1.0], dtype=float)
    absorbed_residual = residual(absorbed, nuisance, weights)
    obstruction_residual = residual(obstruction, nuisance, weights)
    absorbed_norm = weighted_norm(absorbed_residual, weights)
    obstruction_norm = weighted_norm(obstruction_residual, weights)
    return {
        "test_id": "gluing_absorption",
        "absorbed_mismatch_residual_norm": absorbed_norm,
        "obstruction_mismatch_residual_norm": obstruction_norm,
        "pass": absorbed_norm < 1e-10 and obstruction_norm > 0.5,
        "interpretation": "overlap mismatch inside nuisance is absorbed; checkerboard mismatch survives",
    }


def projection_matrix(basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    w = np.diag(weights)
    gram = basis.T @ w @ basis
    return basis @ np.linalg.pinv(gram) @ basis.T @ w


def operator_norm(mat: np.ndarray) -> float:
    return float(np.linalg.svd(mat, compute_uv=False)[0])


def block_commutator_obstruction() -> dict[str, Any]:
    weights = grid_weights(2, 2)
    nuisance = np.ones((4, 1), dtype=float)
    q = projection_matrix(nuisance, weights)
    p = np.eye(4) - q
    good_t = np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    bad_t = np.diag([1.0, 1.3, 0.7, 1.8])
    good_norm = operator_norm(p @ good_t - good_t @ p)
    bad_norm = operator_norm(p @ bad_t - bad_t @ p)
    return {
        "test_id": "commutator_obstruction",
        "good_operator_commutator_norm": good_norm,
        "bad_operator_commutator_norm": bad_norm,
        "pass": good_norm < 1e-10 and bad_norm > 1e-3,
        "interpretation": "operators preserving nuisance quotient commute; nuisance-leaking operators do not",
    }


def run(seed: int, draws: int) -> dict[str, Any]:
    tests = [
        block_non_product_weighted_projection(),
        block_edge_defect(),
        block_square_holonomy(),
        block_rank_shadow_guard(),
        block_random_subspace_guard(seed=seed, draws=draws),
        block_gluing_absorption(),
        block_commutator_obstruction(),
    ]
    return {
        "artifact_kind": "debranded_residual_transport_synthetic_harness_v0",
        "created_utc": utc_now(),
        "seed": seed,
        "random_draws": draws,
        "boundary": {
            "synthetic_only": True,
            "no_maofield_data_read": True,
            "no_checkpoint_loaded": True,
            "no_model_inference": True,
            "no_training": True,
            "no_new_loss": True,
            "not_evidence_of_observed_field": True,
        },
        "tests": tests,
        "all_synthetic_controls_pass": all(bool(test["pass"]) for test in tests),
        "strongest_allowed_verdict": "definitions_and_harness_viable_only",
        "blocked_claims": [
            "residual_field_observed",
            "interaction_field_observed",
            "quotient_residual_field_observed",
            "transport_field_observed",
            "holonomy_field_observed",
            "glass_box_broken",
            "training_authorized",
            "new_loss_authorized",
        ],
    }


def render_summary(result: dict[str, Any], json_path: Path) -> str:
    lines = [
        "# Debranded Residual Transport Synthetic Harness v0",
        "",
        "Date: 2026-06-25 CST",
        "",
        "## Boundary",
        "",
        "This is a zero-GPU toy harness for the debranded mathematics direction.",
        "It is not a MaoField empirical result and does not authorize training,",
        "checkpoint loading, full-panel generation, or a new loss.",
        "",
        "Strongest allowed verdict:",
        "",
        "```text",
        result["strongest_allowed_verdict"],
        "```",
        "",
        "## Artifact",
        "",
        "```text",
        str(json_path),
        "```",
        "",
        "## Seven Blocks",
        "",
    ]
    for test in result["tests"]:
        status = "pass" if test["pass"] else "FAIL"
        lines.append(f"- `{test['test_id']}`: {status}")
    lines.extend(
        [
            "",
            "All synthetic controls passed:",
            "",
            "```text",
            str(result["all_synthetic_controls_pass"]).lower(),
            "```",
            "",
            "## Key Metrics",
            "",
            "```text",
        ]
    )
    metric_keys = [
        "observed_minus_product_max_abs",
        "residual_difference_norm_under_observed_weight",
        "natural_relative_defect_norm",
        "bad_nuisance_relative_defect_norm",
        "natural_square_holonomy_norm",
        "bad_nuisance_square_holonomy_norm",
        "rank1_sigma2_over_sigma1",
        "multidirectional_sigma2_over_sigma1",
        "true_subspace_capture_ratio",
        "random_capture_p95",
        "absorbed_mismatch_residual_norm",
        "obstruction_mismatch_residual_norm",
        "good_operator_commutator_norm",
        "bad_operator_commutator_norm",
    ]
    for test in result["tests"]:
        for key in metric_keys:
            if key in test:
                lines.append(f"{test['test_id']}.{key} = {test[key]:.12g}")
    lines.extend(
        [
            "```",
            "",
            "## Interpretation",
            "",
            "The operator definitions are executable on small finite weighted",
            "systems and the seven kill controls have toy positive and negative",
            "cases. This supports continuing formalization only.",
            "",
            "Blocked interpretations:",
            "",
            "```text",
            "\n".join(result["blocked_claims"]),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output JSON path")
    parser.add_argument("--summary-md", type=Path, help="Optional markdown summary path")
    parser.add_argument("--seed", type=int, default=20260625)
    parser.add_argument("--random-draws", type=int, default=2000)
    args = parser.parse_args()
    if args.random_draws < 200:
        raise SystemExit("--random-draws must be at least 200")
    result = run(seed=args.seed, draws=args.random_draws)
    write_json(args.out, result)
    if args.summary_md:
        write_text(args.summary_md, render_summary(result, args.out))


if __name__ == "__main__":
    main()
