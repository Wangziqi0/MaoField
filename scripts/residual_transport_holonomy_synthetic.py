#!/usr/bin/env python3
"""Zero-GPU synthetic harness for residual transport / holonomy definitions.

This script does not read MaoField aggregates, load checkpoints, run inference,
train, or authorize a new loss. It only checks that the report(23) finite
scale-lattice residual transport objects can be implemented on toy finite
tables with positive and negative controls.
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


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def grid_weights(nq: int, nb: int) -> np.ndarray:
    weights = np.ones(nq * nb, dtype=float)
    return weights / weights.sum()


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


def weighted_project(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    sqrt_w = np.sqrt(weights)
    coef = np.linalg.lstsq(basis * sqrt_w[:, None], v * sqrt_w, rcond=None)[0]
    return basis @ coef


def residual(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return v - weighted_project(v, basis, weights)


def weighted_norm(v: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(float(np.sum(weights * v * v)))


def coarsen_matrix(
    nq: int,
    nb: int,
    q_groups: list[list[int]],
    b_groups: list[list[int]],
    fine_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[int, int]]:
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
    coarse_weights_arr = np.asarray(coarse_weights, dtype=float)
    coarse_weights_arr = coarse_weights_arr / coarse_weights_arr.sum()
    return np.vstack(rows), coarse_weights_arr, (len(q_groups), len(b_groups))


def q_groups(nq: int) -> list[list[int]]:
    if nq == 4:
        return [[0, 1], [2, 3]]
    if nq == 2:
        return [[0, 1]]
    raise ValueError(f"unsupported nq={nq}")


def b_groups(nb: int) -> list[list[int]]:
    if nb == 4:
        return [[0, 1], [2, 3]]
    if nb == 2:
        return [[0, 1]]
    raise ValueError(f"unsupported nb={nb}")


def q_only_groups(nq: int, nb: int) -> tuple[list[list[int]], list[list[int]]]:
    return q_groups(nq), [[b] for b in range(nb)]


def b_only_groups(nq: int, nb: int) -> tuple[list[list[int]], list[list[int]]]:
    return [[q] for q in range(nq)], b_groups(nb)


def interaction_field(nq: int, nb: int, second_direction: bool = False) -> np.ndarray:
    q = np.linspace(-1.0, 1.0, nq)
    b = np.linspace(-1.0, 1.0, nb)
    field = np.outer(q, b)
    if second_direction:
        field = field + 0.65 * np.outer(np.array([1.0, -1.0, -1.0, 1.0])[:nq], b * b - np.mean(b * b))
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
    fine_shape: tuple[int, int],
    coarse_shape: tuple[int, int],
    c: np.ndarray,
    coarse_weights: np.ndarray,
    fine_basis: np.ndarray,
    coarse_basis: np.ndarray,
    fine_weights: np.ndarray,
) -> dict[str, Any]:
    del fine_shape, coarse_shape
    left = c @ residual(v, fine_basis, fine_weights)
    right = residual(c @ v, coarse_basis, coarse_weights)
    defect = left - right
    denom = max(weighted_norm(left, coarse_weights), weighted_norm(right, coarse_weights), 1e-12)
    return {
        "absolute_defect_norm": weighted_norm(defect, coarse_weights),
        "relative_defect_norm": weighted_norm(defect, coarse_weights) / denom,
    }


def scale_square_holonomy(v: np.ndarray) -> dict[str, Any]:
    w44 = grid_weights(4, 4)
    p44 = additive_design(4, 4)
    cq44, w24, _ = coarsen_matrix(4, 4, *q_only_groups(4, 4), w44)
    cb44, w42, _ = coarsen_matrix(4, 4, *b_only_groups(4, 4), w44)
    cb24, w22_a, _ = coarsen_matrix(2, 4, *b_only_groups(2, 4), w24)
    cq42, w22_b, _ = coarsen_matrix(4, 2, *q_only_groups(4, 2), w42)
    if not np.allclose(w22_a, w22_b):
        raise ValueError("coarse square weights disagree")

    # Natural nuisance: additive at every scale. This should commute up to
    # numerical noise for these product-weight toy tables.
    p24 = additive_design(2, 4)
    p42 = additive_design(4, 2)
    p22 = additive_design(2, 2)
    rq_first = cb24 @ residual(cq44 @ residual(v, p44, w44), p24, w24)
    rb_first = cq42 @ residual(cb44 @ residual(v, p44, w44), p42, w42)
    natural_h = weighted_norm(rq_first - rb_first, w22_a)

    # Bad intermediate nuisance deliberately absorbs a q-by-bgroup interaction
    # on only one branch. This is a toy model of a non-functorial nuisance
    # choice: the two paths no longer mean the same quotient operation.
    extra24 = np.asarray(
        [
            -1.0,
            -1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            -1.0,
            -1.0,
        ],
        dtype=float,
    )
    p24_bad = np.column_stack([p24, extra24])
    p42_bad = p42
    rq_bad = cb24 @ residual(cq44 @ residual(v, p44, w44), p24_bad, w24)
    rb_bad = cq42 @ residual(cb44 @ residual(v, p44, w44), p42_bad, w42)
    bad_h = weighted_norm(rq_bad - rb_bad, w22_a)
    return {
        "test_id": "scale_square_holonomy",
        "natural_square_holonomy_norm": natural_h,
        "bad_nuisance_square_holonomy_norm": bad_h,
        "pass": natural_h < 1e-10 and bad_h > 1e-6,
        "interpretation": (
            "natural additive/product coarsening commutes; deliberately non-functorial "
            "intermediate nuisance creates path-dependent residuals"
        ),
    }


def nuisance_functoriality_digest(v: np.ndarray) -> dict[str, Any]:
    w44 = grid_weights(4, 4)
    c, w22, _ = coarsen_matrix(4, 4, q_groups(4), b_groups(4), w44)
    natural = edge_defect(
        v,
        (4, 4),
        (2, 2),
        c,
        w22,
        additive_design(4, 4),
        additive_design(2, 2),
        w44,
    )
    bad = edge_defect(
        v,
        (4, 4),
        (2, 2),
        c,
        w22,
        additive_design(4, 4),
        additive_design(2, 2, include_q=True, include_b=False),
        w44,
    )
    return {
        "test_id": "nuisance_functoriality_digest",
        "natural_relative_defect_norm": natural["relative_defect_norm"],
        "bad_nuisance_relative_defect_norm": bad["relative_defect_norm"],
        "pass": natural["relative_defect_norm"] < 1e-10 and bad["relative_defect_norm"] > 1e-6,
        "interpretation": (
            "edge defects kill claims when the nuisance model is not compatible "
            "with coarsening"
        ),
    }


def singular_ratio(vectors: np.ndarray, weights: np.ndarray) -> tuple[list[float], float | None]:
    matrix = vectors * np.sqrt(weights)[None, :]
    singular = np.linalg.svd(matrix, compute_uv=False)
    ratio = None
    if len(singular) > 1 and singular[0] > 0:
        ratio = float(singular[1] / singular[0])
    return singular.tolist(), ratio


def rank1_angle_vacuity_guard() -> dict[str, Any]:
    w = grid_weights(4, 4)
    one = interaction_field(4, 4)
    two = interaction_field(4, 4, second_direction=True)
    rank1_vectors = np.vstack([scale * one for scale in [0.7, 1.0, 1.3, 1.6]])
    multidirectional_vectors = np.vstack([one, two, one - 0.5 * two, 0.4 * one + two])
    rank1_sv, rank1_ratio = singular_ratio(rank1_vectors, w)
    multi_sv, multi_ratio = singular_ratio(multidirectional_vectors, w)
    return {
        "test_id": "rank1_angle_vacuity_guard",
        "rank1_singular_values": rank1_sv,
        "rank1_sigma2_over_sigma1": rank1_ratio,
        "multidirectional_singular_values": multi_sv,
        "multidirectional_sigma2_over_sigma1": multi_ratio,
        "floor": RANK_SHADOW_FLOOR,
        "pass": (rank1_ratio or 0.0) < 1e-10 and (multi_ratio or 0.0) >= RANK_SHADOW_FLOOR,
        "rank1_verdict": "killed_by_rank1_shadow",
        "multidirectional_verdict": "eligible_for_synthetic_design_review_only",
    }


def orthonormal_basis(vectors: np.ndarray, weights: np.ndarray, dim: int) -> np.ndarray:
    matrix = vectors * np.sqrt(weights)[None, :]
    _, _, vt = np.linalg.svd(matrix, full_matrices=False)
    return vt[:dim] / np.sqrt(weights)[None, :]


def weighted_projection_energy(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> float:
    projected = weighted_project(v, basis.T, weights)
    denom = weighted_norm(v, weights)
    if denom == 0:
        return 0.0
    return weighted_norm(projected, weights) / denom


def random_same_dim_angle_gap(seed: int, draws: int) -> dict[str, Any]:
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
    quantile = float(np.mean(random_arr <= true_capture))
    return {
        "test_id": "random_same_dim_angle_gap",
        "draws": draws,
        "true_subspace_capture_ratio": true_capture,
        "random_capture_mean": float(np.mean(random_arr)),
        "random_capture_p95": float(np.quantile(random_arr, 0.95)),
        "true_capture_quantile": quantile,
        "pass": true_capture > float(np.quantile(random_arr, 0.95)) and quantile >= 0.95,
        "interpretation": "a toy true subspace must beat random same-dimension subspaces",
    }


def run(seed: int, draws: int) -> dict[str, Any]:
    base = mixed_field_with_main_effects()
    tests = [
        scale_square_holonomy(base),
        nuisance_functoriality_digest(base),
        rank1_angle_vacuity_guard(),
        random_same_dim_angle_gap(seed=seed, draws=draws),
    ]
    return {
        "artifact_kind": "maofield_residual_transport_holonomy_synthetic_harness",
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
        "strongest_allowed_verdict": "synthetic_harness_only_no_maofield_claim",
        "blocked_claims": [
            "transport_field_observed",
            "holonomy_field_observed",
            "interaction_field_observed",
            "quotient_residual_field_observed",
            "glass_box_broken",
            "training_authorized",
            "new_loss_authorized",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output JSON path")
    parser.add_argument("--seed", type=int, default=20260624)
    parser.add_argument("--random-draws", type=int, default=1000)
    args = parser.parse_args()
    if args.random_draws < 100:
        raise SystemExit("--random-draws must be at least 100 for a useful random-subspace smoke")
    write_json(args.out, run(seed=args.seed, draws=args.random_draws))


if __name__ == "__main__":
    main()
