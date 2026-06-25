#!/usr/bin/env python3
"""v1 zero-GPU harness for finite weighted residual transport.

This is a synthetic-only harness for the debranded mathematics direction. It
does not read MaoField aggregates, load checkpoints, run inference, train, or
authorize a new loss.
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
EPS = 1e-12


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
    v = np.asarray(v, dtype=float).reshape(-1)
    return math.sqrt(float(np.sum(weights * v * v)))


def projection_matrix(basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    basis = np.asarray(basis, dtype=float)
    weights = np.asarray(weights, dtype=float).reshape(-1)
    gram = basis.T @ np.diag(weights) @ basis
    return basis @ np.linalg.pinv(gram) @ basis.T @ np.diag(weights)


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
    table = np.asarray(weights, dtype=float).reshape(nq, nb)
    q = table.sum(axis=1)
    b = table.sum(axis=0)
    return np.outer(q, b).reshape(-1) / float(np.sum(table))


def grid_weights(nq: int, nb: int) -> np.ndarray:
    return np.full(nq * nb, 1.0 / (nq * nb), dtype=float)


def coarsen_matrix(
    nq: int,
    nb: int,
    q_groups: list[list[int]],
    b_groups: list[list[int]],
    fine_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    rows: list[np.ndarray] = []
    coarse_weights: list[float] = []
    for q_group in q_groups:
        for b_group in b_groups:
            idx = [q * nb + b for q in q_group for b in b_group]
            weight_sum = float(np.sum(fine_weights[idx]))
            row = np.zeros(nq * nb, dtype=float)
            row[idx] = fine_weights[idx] / weight_sum
            rows.append(row)
            coarse_weights.append(weight_sum)
    return np.vstack(rows), normalize(np.asarray(coarse_weights, dtype=float))


def repeat_coarse(coarse: np.ndarray, q_factor: int, b_factor: int) -> np.ndarray:
    table = np.asarray(coarse, dtype=float)
    return np.repeat(np.repeat(table, q_factor, axis=0), b_factor, axis=1).reshape(-1)


def interaction_field(nq: int, nb: int, second_direction: bool = False) -> np.ndarray:
    q = np.linspace(-1.0, 1.0, nq)
    b = np.linspace(-1.0, 1.0, nb)
    field = np.outer(q, b)
    if second_direction:
        q2 = np.array([1.0, -1.0, -1.0, 1.0], dtype=float)[:nq]
        b2 = b * b - np.mean(b * b)
        field = field + 0.65 * np.outer(q2, b2)
    return field.reshape(-1)


def mixed_field_4x4() -> np.ndarray:
    interaction = interaction_field(4, 4, second_direction=True).reshape(4, 4)
    q_main = np.linspace(-0.6, 0.6, 4)[:, None]
    b_main = np.array([-0.9, -0.2, 0.3, 1.1])[None, :]
    q_block = np.array([-1.0, -1.0, 1.0, 1.0])[:, None]
    b_block = np.array([-1.0, -1.0, 1.0, 1.0])[None, :]
    coarse_block_interaction = 0.75 * (q_block @ b_block)
    return (interaction + q_main + b_main + coarse_block_interaction).reshape(-1)


def singular_ratio(vectors: np.ndarray, weights: np.ndarray) -> tuple[list[float], float | None]:
    matrix = np.asarray(vectors, dtype=float) * np.sqrt(weights)[None, :]
    singular = np.linalg.svd(matrix, compute_uv=False)
    ratio = None
    if len(singular) > 1 and singular[0] > 0:
        ratio = float(singular[1] / singular[0])
    return singular.tolist(), ratio


def weighted_orthonormal_rows(vectors: np.ndarray, weights: np.ndarray, dim: int | None = None) -> np.ndarray:
    matrix = np.asarray(vectors, dtype=float) * np.sqrt(weights)[None, :]
    _, singular, vt = np.linalg.svd(matrix, full_matrices=False)
    keep = int(np.sum(singular > 1e-10)) if dim is None else dim
    return vt[:keep] / np.sqrt(weights)[None, :]


def residual_space_basis(nq: int, nb: int, weights: np.ndarray) -> np.ndarray:
    nuisance = additive_design(nq, nb)
    candidates = np.vstack([residual(row, nuisance, weights) for row in np.eye(nq * nb)])
    return weighted_orthonormal_rows(candidates, weights)


def weighted_projection_energy(v: np.ndarray, basis_rows: np.ndarray, weights: np.ndarray) -> float:
    basis_rows = np.asarray(basis_rows, dtype=float)
    if basis_rows.ndim == 1:
        basis_rows = basis_rows[None, :]
    projected = weighted_project(v, basis_rows.T, weights)
    denom = weighted_norm(v, weights)
    return 0.0 if denom < EPS else weighted_norm(projected, weights) / denom


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
    denom = max(weighted_norm(left, coarse_weights), weighted_norm(right, coarse_weights), EPS)
    absolute = weighted_norm(defect, coarse_weights)
    return {
        "absolute_defect_norm": absolute,
        "relative_defect_norm": absolute / denom,
    }


def projected_path_apply(v: np.ndarray, steps: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> np.ndarray:
    current = np.asarray(v, dtype=float).reshape(-1)
    for c, source_basis, source_weights in steps:
        current = c @ residual(current, source_basis, source_weights)
    terminal_basis = steps[-1][1]
    terminal_weights = steps[-1][2]
    # The caller supplies a final identity edge when terminal projection is
    # needed; this helper keeps the step representation explicit.
    return residual(current, terminal_basis, terminal_weights)


def block_exact_product_weight_equality() -> dict[str, Any]:
    nq, nb = 2, 3
    q = normalize(np.array([2.0, 5.0]))
    b = normalize(np.array([3.0, 4.0, 7.0]))
    observed = np.outer(q, b).reshape(-1)
    product = product_from_marginals(observed, nq, nb)
    basis = additive_design(nq, nb)
    k = np.array([0.2, -0.4, 1.0, -0.8, 0.7, 0.1], dtype=float)
    r_observed = residual(k, basis, observed)
    r_product = residual(k, basis, product)
    weight_diff = float(np.max(np.abs(observed - product)))
    residual_diff = weighted_norm(r_observed - r_product, observed)
    return {
        "test_id": "exact_product_weight_equality_control",
        "product_weight_max_abs_error": weight_diff,
        "residual_difference_norm_under_observed_weight": residual_diff,
        "pass": weight_diff < 1e-12 and residual_diff < 1e-12,
        "interpretation": "when weights are exactly product-form, observed and product-reference projections agree",
    }


def block_product_reweighting_separation() -> dict[str, Any]:
    nq, nb = 2, 2
    observed_raw = np.array([1.0, 2.0, 3.0, 5.0], dtype=float)
    product_raw = np.array([12.0 / 11.0, 21.0 / 11.0, 32.0 / 11.0, 56.0 / 11.0], dtype=float)
    observed = normalize(observed_raw)
    product = normalize(product_raw)
    basis = additive_design(nq, nb)
    k = np.array([0.0, 1.0, 2.0, 6.0], dtype=float)
    r_observed = residual(k, basis, observed)
    r_product = residual(k, basis, product)
    diff = r_observed - r_product
    max_abs = float(np.max(np.abs(diff)))
    norm_diff = weighted_norm(diff, observed_raw)
    return {
        "test_id": "product_reweighting_separation",
        "observed_residual": r_observed.tolist(),
        "product_reference_residual": r_product.tolist(),
        "residual_difference": diff.tolist(),
        "max_abs_diff": max_abs,
        "observed_raw_weight_norm_diff": norm_diff,
        "expected_max_abs_diff_from_formal_note_v1": 0.086980083999,
        "expected_raw_weight_norm_diff_from_formal_note_v1": 0.127651515989,
        "pass": abs(max_abs - 0.086980083999) < 1e-9 and abs(norm_diff - 0.127651515989) < 1e-9,
        "interpretation": "product-reweighted Hoeffding lives in a different weighted Hilbert geometry",
    }


def block_outcome_derived_nuisance_invalidation() -> dict[str, Any]:
    weights = grid_weights(2, 2)
    k = np.array([1.0, -1.0, -1.0, 1.0], dtype=float)
    source_fixed_nuisance = np.ones((4, 1), dtype=float)
    invalid_outcome_nuisance = k[:, None]
    source_residual_norm = weighted_norm(residual(k, source_fixed_nuisance, weights), weights)
    invalid_residual_norm = weighted_norm(residual(k, invalid_outcome_nuisance, weights), weights)
    return {
        "test_id": "outcome_derived_nuisance_invalidation",
        "source_fixed_residual_norm": source_residual_norm,
        "outcome_derived_residual_norm": invalid_residual_norm,
        "verdict": "invalid_artifact",
        "pass": source_residual_norm > 0.5 and invalid_residual_norm < 1e-12,
        "interpretation": "choosing N=span(K) after seeing K kills the residual and invalidates the claim",
    }


def coarse_positive_signals() -> list[np.ndarray]:
    q = np.array([-1.0, 0.0, 1.0])
    b = np.array([-1.0, 0.0, 1.0])
    d1 = np.outer(q, b)
    d2 = np.outer(np.array([1.0, -2.0, 1.0]), b)
    q_main = np.array([-0.4, 0.1, 0.5])[:, None]
    b_main = np.array([0.7, -0.2, -0.5])[None, :]
    coeffs = [(1.0, 0.2), (0.3, 1.0), (-0.7, 0.8), (1.2, -0.5)]
    return [(a * d1 + bcoef * d2 + q_main + b_main).reshape(-1) for a, bcoef in coeffs]


def block_transport_stable_multidirectional_positive_control() -> dict[str, Any]:
    w66 = grid_weights(6, 6)
    c, w33 = coarsen_matrix(6, 6, [[0, 1], [2, 3], [4, 5]], [[0, 1], [2, 3], [4, 5]], w66)
    fine_basis = additive_design(6, 6)
    coarse_basis = additive_design(3, 3)
    defects = []
    coarse_residuals = []
    for coarse in coarse_positive_signals():
        fine = repeat_coarse(coarse.reshape(3, 3), q_factor=2, b_factor=2)
        defects.append(edge_defect(fine, c, w33, fine_basis, coarse_basis, w66)["relative_defect_norm"])
        coarse_residuals.append(residual(c @ fine, coarse_basis, w33))
    singular, ratio = singular_ratio(np.vstack(coarse_residuals), w33)
    return {
        "test_id": "transport_stable_multidirectional_positive_control",
        "max_edge_relative_defect_norm": float(np.max(defects)),
        "coarse_residual_singular_values": singular,
        "coarse_residual_sigma2_over_sigma1": ratio,
        "floor": RANK_SHADOW_FLOOR,
        "pass": float(np.max(defects)) < 1e-10 and (ratio or 0.0) >= RANK_SHADOW_FLOOR,
        "interpretation": "a source-fixed coarse-block toy field can survive natural coarsening with two residual directions",
    }


def square_path_terms() -> dict[str, Any]:
    v = mixed_field_4x4()
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
    p22 = additive_design(2, 2)
    q_first = residual(cb24 @ residual(cq44 @ residual(v, p44, w44), p24, w24), p22, w22_a)
    b_first = residual(cq42 @ residual(cb44 @ residual(v, p44, w44), p42, w42), p22, w22_a)
    raw_q = cb24 @ cq44
    raw_b = cq42 @ cb44
    return {
        "v": v,
        "w44": w44,
        "w24": w24,
        "w42": w42,
        "w22": w22_a,
        "p44": p44,
        "p24": p24,
        "p42": p42,
        "p22": p22,
        "cq44": cq44,
        "cb44": cb44,
        "cb24": cb24,
        "cq42": cq42,
        "q_first": q_first,
        "b_first": b_first,
        "raw_path_max_abs_diff": float(np.max(np.abs(raw_q - raw_b))),
    }


def block_raw_path_equality_square_control() -> dict[str, Any]:
    terms = square_path_terms()
    holonomy = weighted_norm(terms["q_first"] - terms["b_first"], terms["w22"])
    return {
        "test_id": "raw_path_equality_square_control",
        "raw_path_max_abs_diff": terms["raw_path_max_abs_diff"],
        "square_holonomy_norm": holonomy,
        "pass": terms["raw_path_max_abs_diff"] < 1e-12 and holonomy < 1e-10,
        "interpretation": "raw-equal compatible square paths close after registered projections",
    }


def block_coarsening_non_naturality_trap() -> dict[str, Any]:
    terms = square_path_terms()
    extra24 = np.array([-1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0], dtype=float)
    p24_bad = np.column_stack([terms["p24"], extra24])
    q_bad = residual(
        terms["cb24"]
        @ residual(terms["cq44"] @ residual(terms["v"], terms["p44"], terms["w44"]), p24_bad, terms["w24"]),
        terms["p22"],
        terms["w22"],
    )
    b_good = terms["b_first"]
    holonomy = weighted_norm(q_bad - b_good, terms["w22"])
    return {
        "test_id": "coarsening_non_naturality_trap",
        "raw_path_max_abs_diff": terms["raw_path_max_abs_diff"],
        "path_dependent_bad_nuisance_holonomy_norm": holonomy,
        "verdict": "killed_by_coarsening",
        "pass": terms["raw_path_max_abs_diff"] < 1e-12 and holonomy > 1e-6,
        "interpretation": "nonzero holonomy caused by a path-dependent nuisance choice is a trap, not a discovery",
    }


def block_rank1_plus_noise_floor_trap(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 1)
    weights = grid_weights(4, 4)
    nuisance = additive_design(4, 4)
    template = residual(interaction_field(4, 4), nuisance, weights)
    tiny_noise = np.vstack([residual(rng.normal(size=16), nuisance, weights) for _ in range(5)])
    rank1_noise = np.vstack([(0.8 + 0.2 * i) * template for i in range(5)]) + 1e-4 * tiny_noise
    multi = np.vstack(
        [
            residual(interaction_field(4, 4), nuisance, weights),
            residual(interaction_field(4, 4, second_direction=True), nuisance, weights),
            residual(interaction_field(4, 4) - 0.6 * interaction_field(4, 4, second_direction=True), nuisance, weights),
            residual(0.3 * interaction_field(4, 4) + interaction_field(4, 4, second_direction=True), nuisance, weights),
        ]
    )
    rank1_sv, rank1_ratio = singular_ratio(rank1_noise, weights)
    multi_sv, multi_ratio = singular_ratio(multi, weights)
    return {
        "test_id": "rank1_plus_noise_floor_trap",
        "rank1_noise_singular_values": rank1_sv,
        "rank1_noise_sigma2_over_sigma1": rank1_ratio,
        "multidirectional_singular_values": multi_sv,
        "multidirectional_sigma2_over_sigma1": multi_ratio,
        "floor": RANK_SHADOW_FLOOR,
        "verdict": "killed_by_rank1_shadow",
        "pass": (rank1_ratio or 0.0) < 0.01 and (multi_ratio or 0.0) >= RANK_SHADOW_FLOOR,
        "interpretation": "small noise around one template remains a rank-shadow artifact",
    }


def block_random_subspace_in_residual_space(seed: int, draws: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 2)
    weights = grid_weights(3, 3)
    nuisance = additive_design(3, 3)
    basis_res = residual_space_basis(3, 3, weights)
    signals = [residual(v, nuisance, weights) for v in coarse_positive_signals()[:3]]
    heldout = residual(coarse_positive_signals()[3], nuisance, weights)
    true_basis = weighted_orthonormal_rows(np.vstack(signals), weights, dim=2)
    true_capture = weighted_projection_energy(heldout, true_basis, weights)
    random_capture = []
    for _ in range(draws):
        coords = rng.normal(size=(2, basis_res.shape[0]))
        random_basis = weighted_orthonormal_rows(coords @ basis_res, weights, dim=2)
        random_capture.append(weighted_projection_energy(heldout, random_basis, weights))
    random_arr = np.asarray(random_capture, dtype=float)
    p95 = float(np.quantile(random_arr, 0.95))
    p99 = float(np.quantile(random_arr, 0.99))
    quantile = float(np.mean(random_arr <= true_capture))
    return {
        "test_id": "random_subspace_in_residual_space",
        "draws": draws,
        "residual_space_dimension": int(basis_res.shape[0]),
        "true_subspace_capture_ratio": true_capture,
        "random_capture_mean": float(np.mean(random_arr)),
        "random_capture_p95": p95,
        "random_capture_p99": p99,
        "true_capture_quantile": quantile,
        "pass": true_capture > p99 and quantile >= 0.99,
        "interpretation": "the random null is sampled inside N-perp after nuisance removal",
    }


def named_checkerboard_4x4() -> np.ndarray:
    q = np.array([-1.0, -1.0, 1.0, 1.0])[:, None]
    b = np.array([-1.0, -1.0, 1.0, 1.0])[None, :]
    return (q @ b).reshape(-1)


def one_dim_capture(signal: np.ndarray, direction: np.ndarray, weights: np.ndarray) -> float:
    basis = direction.reshape(1, -1)
    return weighted_projection_energy(signal, basis, weights)


def block_equal_cell_count_random_axes(seed: int, draws: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 3)
    weights = grid_weights(4, 4)
    nuisance = additive_design(4, 4)
    named = residual(named_checkerboard_4x4(), nuisance, weights)
    signal = residual(named_checkerboard_4x4() + np.linspace(-0.4, 0.4, 16), nuisance, weights)
    named_capture = one_dim_capture(signal, named, weights)
    random_capture = []
    for _ in range(draws):
        axis_a = np.array([-1.0] * 8 + [1.0] * 8)
        axis_b = np.array([-1.0] * 8 + [1.0] * 8)
        rng.shuffle(axis_a)
        rng.shuffle(axis_b)
        direction = residual(axis_a * axis_b, nuisance, weights)
        if weighted_norm(direction, weights) > EPS:
            random_capture.append(one_dim_capture(signal, direction, weights))
    random_arr = np.asarray(random_capture, dtype=float)
    p95 = float(np.quantile(random_arr, 0.95))
    p99 = float(np.quantile(random_arr, 0.99))
    quantile = float(np.mean(random_arr <= named_capture))
    return {
        "test_id": "equal_cell_count_random_axes",
        "draws": int(len(random_capture)),
        "named_axis_capture_ratio": named_capture,
        "random_equal_cell_axis_capture_mean": float(np.mean(random_arr)),
        "random_equal_cell_axis_capture_p95": p95,
        "random_equal_cell_axis_capture_p99": p99,
        "named_capture_quantile": quantile,
        "pass": named_capture > p99 and quantile >= 0.99,
        "interpretation": "a named toy axis must beat balanced random cell partitions",
    }


def block_within_axis_shuffle_and_bad_axis_controls(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 4)
    weights = grid_weights(4, 4)
    nuisance = additive_design(4, 4)
    signal = residual(named_checkerboard_4x4(), nuisance, weights)
    named_direction = residual(named_checkerboard_4x4(), nuisance, weights)
    shuffled_cells = named_checkerboard_4x4().copy()
    for q in range(4):
        idx = np.arange(q * 4, q * 4 + 4)
        shuffled_cells[idx] = shuffled_cells[idx][rng.permutation(4)]
    bad_axis = np.array([1.0 if i % 2 == 0 else -1.0 for i in range(16)], dtype=float)
    shuffled_direction = residual(shuffled_cells, nuisance, weights)
    bad_direction = residual(bad_axis, nuisance, weights)
    named_capture = one_dim_capture(signal, named_direction, weights)
    shuffled_capture = one_dim_capture(signal, shuffled_direction, weights)
    bad_axis_capture = one_dim_capture(signal, bad_direction, weights)
    return {
        "test_id": "within_axis_shuffle_and_bad_axis_controls",
        "named_capture_ratio": named_capture,
        "within_axis_shuffle_capture_ratio": shuffled_capture,
        "bad_axis_label_capture_ratio": bad_axis_capture,
        "pass": named_capture > 0.999 and shuffled_capture < 0.75 and bad_axis_capture < 0.25,
        "interpretation": "shuffled or bad labels fail to recover the source-fixed named toy direction",
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
        "verdict": "killed_by_gluing_absorption",
        "pass": absorbed_norm < 1e-10 and obstruction_norm > 0.5,
        "interpretation": "overlap mismatch inside nuisance is absorbed; checkerboard mismatch survives",
    }


def run(seed: int, draws: int) -> dict[str, Any]:
    tests = [
        block_exact_product_weight_equality(),
        block_product_reweighting_separation(),
        block_outcome_derived_nuisance_invalidation(),
        block_transport_stable_multidirectional_positive_control(),
        block_raw_path_equality_square_control(),
        block_coarsening_non_naturality_trap(),
        block_rank1_plus_noise_floor_trap(seed=seed),
        block_random_subspace_in_residual_space(seed=seed, draws=draws),
        block_equal_cell_count_random_axes(seed=seed, draws=draws),
        block_within_axis_shuffle_and_bad_axis_controls(seed=seed),
        block_gluing_absorption(),
    ]
    return {
        "artifact_kind": "debranded_residual_transport_synthetic_harness_v1",
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
            "full_panel_has_run",
            "sixteen_cell_full_panel_aggregate_exists",
            "residual_field_observed",
            "interaction_field_observed",
            "quotient_residual_field_observed",
            "transport_field_observed",
            "holonomy_field_observed",
            "glass_box_broken",
            "LOSO_passed",
            "F3_positive",
            "training_authorized",
            "new_loss_authorized",
        ],
    }


def render_summary(result: dict[str, Any], json_path: Path) -> str:
    lines = [
        "# Debranded Residual Transport Synthetic Harness v1",
        "",
        "Date: 2026-06-25 CST",
        "",
        "## Boundary",
        "",
        "This is a zero-GPU synthetic harness for the debranded mathematics",
        "direction. It is not a MaoField empirical result and does not authorize",
        "training, checkpoint loading, full-panel generation, model inference,",
        "or a new loss.",
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
        "## v1 Blocks",
        "",
    ]
    for test in result["tests"]:
        status = "pass" if test["pass"] else "FAIL"
        verdict = f" ({test['verdict']})" if "verdict" in test else ""
        lines.append(f"- `{test['test_id']}`: {status}{verdict}")
    lines.extend(
        [
            "",
            "All synthetic controls passed:",
            "",
            "```text",
            str(result["all_synthetic_controls_pass"]).lower(),
            "```",
            "",
            "## Selected Metrics",
            "",
            "```text",
        ]
    )
    metric_keys = [
        "product_weight_max_abs_error",
        "residual_difference_norm_under_observed_weight",
        "max_abs_diff",
        "observed_raw_weight_norm_diff",
        "source_fixed_residual_norm",
        "outcome_derived_residual_norm",
        "max_edge_relative_defect_norm",
        "coarse_residual_sigma2_over_sigma1",
        "raw_path_max_abs_diff",
        "square_holonomy_norm",
        "path_dependent_bad_nuisance_holonomy_norm",
        "rank1_noise_sigma2_over_sigma1",
        "multidirectional_sigma2_over_sigma1",
        "true_subspace_capture_ratio",
        "random_capture_p99",
        "named_axis_capture_ratio",
        "random_equal_cell_axis_capture_p99",
        "within_axis_shuffle_capture_ratio",
        "bad_axis_label_capture_ratio",
        "absorbed_mismatch_residual_norm",
        "obstruction_mismatch_residual_norm",
    ]
    for test in result["tests"]:
        for key in metric_keys:
            if key in test and test[key] is not None:
                lines.append(f"{test['test_id']}.{key} = {float(test[key]):.12g}")
    lines.extend(
        [
            "```",
            "",
            "## Interpretation",
            "",
            "The v1 harness adds exact product-weight equality, product-reweighting",
            "separation, source-fixed nuisance invalidation, transport-stable",
            "multidirectional structure, square no-go controls, rank/random-axis",
            "negative controls, and gluing absorption. Passing these toy controls",
            "supports formal design review only.",
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
    if not result["all_synthetic_controls_pass"]:
        raise SystemExit("one or more synthetic controls failed")


if __name__ == "__main__":
    main()
