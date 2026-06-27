#!/usr/bin/env python3
"""v1.2 zero-GPU harness for finite weighted residual transport.

This is a synthetic-only harness for the debranded mathematics direction. It
does not read MaoField aggregates, load checkpoints, run inference, train, or
authorize a new loss.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


EPS = 1e-12
RANK_SHADOW_FLOOR = 0.25
BLOCKED_CLAIMS = [
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
    "completed_formal_system",
]


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def environment_metadata() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
    }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def build_threshold_contract() -> dict[str, dict[str, Any]]:
    """Single source of all pass/fail thresholds for v1.2."""
    return {
        "exact_product_weight_equality_control": {
            "max_product_weight_error": 1e-12,
            "max_residual_difference_norm": 1e-12,
        },
        "product_reweighting_separation": {
            "expected_max_abs_diff": 0.086980083999,
            "expected_raw_weight_norm_diff": 0.127651515989,
            "max_abs_diff_tolerance": 1e-9,
            "raw_weight_norm_diff_tolerance": 1e-9,
        },
        "quotient_descent_control": {
            "max_good_coset_disagreement": 1e-12,
            "min_bad_coset_disagreement": 0.5,
        },
        "common_ambient_registration_control": {
            "max_isometric_registration_metric_diff": 1e-12,
            "max_unregistered_use_count": 0,
            "min_bad_registration_metric_diff": 0.1,
        },
        "projection_evolution_commutator_obstruction": {
            "max_good_commutator_fro_norm": 1e-12,
            "min_bad_commutator_fro_norm": 0.1,
            "min_bad_signal_leakage_norm": 0.1,
        },
        "raw_path_equality_square_control": {
            "max_raw_path_diff": 1e-12,
            "max_square_holonomy_norm": 1e-10,
        },
        "coarsening_non_naturality_trap": {
            "max_raw_path_diff": 1e-12,
            "min_bad_holonomy_norm": 1e-6,
        },
        "rank1_perturbation_bound_control": {
            "max_sigma2_minus_noise_opnorm": 1e-10,
            "min_multidirectional_sigma2_over_sigma1": RANK_SHADOW_FLOOR,
        },
        "random_subspace_beta_squared_capture_control": {
            "max_beta_mean_error": 0.03,
            "max_beta_variance_error": 0.025,
            "min_true_sq_capture_minus_p99": 0.03,
            "min_true_sq_capture_quantile": 0.99,
        },
        "square_holonomy_telescoping_control": {
            "max_telescoping_identity_error": 1e-10,
            "max_square_identity_error": 1e-10,
        },
        "triple_overlap_gluing_cocycle": {
            "max_absorbed_cycle_residual_norm": 1e-10,
            "min_obstruction_cycle_residual_norm": 0.5,
        },
        "threshold_contract_single_source_control": {
            "require_contract_hash_match": True,
            "require_per_test_threshold_match": True,
            "require_central_evaluator": True,
        },
    }


def normalize(weights: np.ndarray) -> np.ndarray:
    weights = np.asarray(weights, dtype=float).reshape(-1)
    if np.any(weights <= 0):
        raise ValueError("weights must be positive")
    return weights / float(np.sum(weights))


def grid_weights(nq: int, nb: int) -> np.ndarray:
    return np.full(nq * nb, 1.0 / (nq * nb), dtype=float)


def weighted_norm(v: np.ndarray, weights: np.ndarray) -> float:
    v = np.asarray(v, dtype=float).reshape(-1)
    return math.sqrt(float(np.sum(weights * v * v)))


def fro_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(matrix, dtype=float), ord="fro"))


def op_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(matrix, dtype=float), ord=2))


def weighted_project(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    basis = np.asarray(basis, dtype=float)
    v = np.asarray(v, dtype=float).reshape(-1)
    sqrt_w = np.sqrt(weights)
    coef = np.linalg.lstsq(basis * sqrt_w[:, None], v * sqrt_w, rcond=None)[0]
    return basis @ coef


def residual(v: np.ndarray, basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.asarray(v, dtype=float).reshape(-1) - weighted_project(v, basis, weights)


def projection_matrix(basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    basis = np.asarray(basis, dtype=float)
    weights = np.asarray(weights, dtype=float).reshape(-1)
    gram = basis.T @ np.diag(weights) @ basis
    return basis @ np.linalg.pinv(gram) @ basis.T @ np.diag(weights)


def residual_projector(basis: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.eye(len(weights), dtype=float) - projection_matrix(basis, weights)


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


def weighted_orthonormal_rows(vectors: np.ndarray, weights: np.ndarray, dim: int | None = None) -> np.ndarray:
    matrix = np.asarray(vectors, dtype=float) * np.sqrt(weights)[None, :]
    _, singular, vt = np.linalg.svd(matrix, full_matrices=False)
    keep = int(np.sum(singular > 1e-10)) if dim is None else dim
    return vt[:keep] / np.sqrt(weights)[None, :]


def residual_space_basis(nq: int, nb: int, weights: np.ndarray) -> np.ndarray:
    nuisance = additive_design(nq, nb)
    candidates = np.vstack([residual(row, nuisance, weights) for row in np.eye(nq * nb)])
    return weighted_orthonormal_rows(candidates, weights)


def squared_capture(v: np.ndarray, basis_rows: np.ndarray, weights: np.ndarray) -> float:
    basis_rows = np.asarray(basis_rows, dtype=float)
    if basis_rows.ndim == 1:
        basis_rows = basis_rows[None, :]
    projected = weighted_project(v, basis_rows.T, weights)
    denom = weighted_norm(v, weights)
    if denom < EPS:
        return 0.0
    ratio = weighted_norm(projected, weights) / denom
    return float(ratio * ratio)


def singular_ratio(vectors: np.ndarray, weights: np.ndarray) -> tuple[list[float], float | None]:
    matrix = np.asarray(vectors, dtype=float) * np.sqrt(weights)[None, :]
    singular = np.linalg.svd(matrix, compute_uv=False)
    ratio = None
    if len(singular) > 1 and singular[0] > 0:
        ratio = float(singular[1] / singular[0])
    return singular.tolist(), ratio


def metric_values_for_registration(stack: np.ndarray) -> dict[str, Any]:
    singular = np.linalg.svd(stack, compute_uv=False)
    gram = stack.T @ stack
    return {
        "singular_values": singular.tolist(),
        "gram_matrix": gram.tolist(),
        "stack_fro_norm": float(np.linalg.norm(stack, ord="fro")),
    }


def max_metric_diff(a: dict[str, Any], b: dict[str, Any]) -> float:
    diffs = []
    for key in ["singular_values", "gram_matrix", "stack_fro_norm"]:
        diffs.append(float(np.max(np.abs(np.asarray(a[key]) - np.asarray(b[key])))))
    return float(max(diffs))


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


def path_product(projectors: list[np.ndarray], maps: list[np.ndarray], internal_mask: set[int]) -> np.ndarray:
    """Return P_m C_m [P_{m-1}] ... [P_1] C_1 P_0.

    Internal projection P_i is included exactly when i is in internal_mask.
    Source and terminal projections are always included.
    """
    out = projectors[0].copy()
    for edge_index, c in enumerate(maps, start=1):
        out = c @ out
        if edge_index in internal_mask or edge_index == len(maps):
            out = projectors[edge_index] @ out
    return out


def block_exact_product_weight_equality_control() -> dict[str, Any]:
    nq, nb = 2, 3
    q = normalize(np.array([2.0, 5.0]))
    b = normalize(np.array([3.0, 4.0, 7.0]))
    observed = np.outer(q, b).reshape(-1)
    product = product_from_marginals(observed, nq, nb)
    basis = additive_design(nq, nb)
    k = np.array([0.2, -0.4, 1.0, -0.8, 0.7, 0.1], dtype=float)
    r_observed = residual(k, basis, observed)
    r_product = residual(k, basis, product)
    return {
        "test_id": "exact_product_weight_equality_control",
        "kind": "theorem_boundary_regression",
        "product_weight_max_abs_error": float(np.max(np.abs(observed - product))),
        "residual_difference_norm_under_observed_weight": weighted_norm(r_observed - r_product, observed),
        "interpretation": "exact product weights make observed and product-reference additive residuals agree",
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
    return {
        "test_id": "product_reweighting_separation",
        "kind": "non_product_boundary_regression",
        "observed_residual": r_observed.tolist(),
        "product_reference_residual": r_product.tolist(),
        "residual_difference": diff.tolist(),
        "max_abs_diff": float(np.max(np.abs(diff))),
        "observed_raw_weight_norm_diff": weighted_norm(diff, observed_raw),
        "interpretation": "non-product weights live in a different weighted Hilbert geometry",
    }


def block_quotient_descent_control() -> dict[str, Any]:
    source_n = np.array([[1.0], [0.0]])
    target_n = np.array([[1.0], [0.0]])
    weights = normalize(np.ones(2))
    p_target = residual_projector(target_n, weights)
    h = np.array([0.0, 2.0])
    n = source_n[:, 0]
    c_good = np.array([[3.0, 0.0], [0.0, 2.0]])
    c_bad = np.array([[0.0, 0.0], [1.0, 1.0]])
    good_disagreement = weighted_norm(p_target @ (c_good @ (h + n) - c_good @ h), weights)
    bad_disagreement = weighted_norm(p_target @ (c_bad @ (h + n) - c_bad @ h), weights)
    return {
        "test_id": "quotient_descent_control",
        "kind": "theorem_backed_toy_control",
        "good_coset_disagreement": good_disagreement,
        "bad_coset_disagreement": bad_disagreement,
        "good_condition": "C(N_s) <= N_t",
        "bad_condition": "C(N_s) not <= N_t",
        "interpretation": "quotient descent is well-defined exactly when source nuisance maps into target nuisance",
    }


def block_common_ambient_registration_control() -> dict[str, Any]:
    residuals = np.array(
        [
            [1.0, 0.0, 0.5],
            [0.0, 1.0, -0.25],
            [0.3, -0.2, 1.0],
        ],
        dtype=float,
    )
    theta = 0.37
    u = np.array(
        [
            [math.cos(theta), -math.sin(theta), 0.0],
            [math.sin(theta), math.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=float,
    )
    registered_a = residuals
    registered_b = u @ residuals
    bad_registration = np.diag([2.0, 1.0, 1.0]) @ residuals
    metrics_a = metric_values_for_registration(registered_a)
    metrics_b = metric_values_for_registration(registered_b)
    metrics_bad = metric_values_for_registration(bad_registration)
    return {
        "test_id": "common_ambient_registration_control",
        "kind": "registration_invariance_control",
        "isometric_registration_metric_diff": max_metric_diff(metrics_a, metrics_b),
        "bad_registration_metric_diff": max_metric_diff(metrics_a, metrics_bad),
        "unregistered_use_count": 0,
        "registered_diagnostic_names": [
            "stack_singular_values",
            "gram_matrix",
            "stack_fro_norm",
        ],
        "interpretation": "spectra and angles are invariant only after a stated isometric registration equivalence",
    }


def block_projection_evolution_commutator_obstruction() -> dict[str, Any]:
    weights = grid_weights(2, 2)
    nuisance = np.ones((4, 1), dtype=float)
    p = residual_projector(nuisance, weights)
    t_good = np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=float,
    )
    t_bad = np.diag([2.0, 1.0, 1.0, 1.0])
    good_comm = p @ t_good - t_good @ p
    bad_comm = p @ t_bad - t_bad @ p
    signal = np.array([0.0, 1.0, 2.0, 4.0], dtype=float)
    bad_leak = bad_comm @ signal
    return {
        "test_id": "projection_evolution_commutator_obstruction",
        "kind": "operator_leakage_control",
        "good_commutator_fro_norm": fro_norm(good_comm),
        "bad_commutator_fro_norm": fro_norm(bad_comm),
        "bad_signal_leakage_norm": weighted_norm(bad_leak, weights),
        "interpretation": "nonzero [P,T] is leakage of a chosen residual representative, not an empirical discovery",
    }


def block_raw_path_equality_square_control() -> dict[str, Any]:
    terms = square_path_terms()
    holonomy = weighted_norm(terms["q_first"] - terms["b_first"], terms["w22"])
    return {
        "test_id": "raw_path_equality_square_control",
        "kind": "square_regression_control",
        "raw_path_max_abs_diff": terms["raw_path_max_abs_diff"],
        "square_holonomy_norm": holonomy,
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
    holonomy = weighted_norm(q_bad - terms["b_first"], terms["w22"])
    return {
        "test_id": "coarsening_non_naturality_trap",
        "kind": "negative_control",
        "raw_path_max_abs_diff": terms["raw_path_max_abs_diff"],
        "path_dependent_bad_nuisance_holonomy_norm": holonomy,
        "verdict": "killed_by_coarsening",
        "interpretation": "path-dependent nuisance choices can create fake holonomy",
    }


def block_rank1_perturbation_bound_control(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 11)
    a = np.linspace(0.7, 1.4, 6)
    v = np.array([1.0, -0.5, 0.25, 0.75, -1.0], dtype=float)
    e = 0.003 * rng.normal(size=(6, 5))
    m_rank_shadow = np.outer(a, v) + e
    singular = np.linalg.svd(m_rank_shadow, compute_uv=False)
    noise_op = op_norm(e)
    weights = grid_weights(4, 4)
    nuisance = additive_design(4, 4)
    multi = np.vstack(
        [
            residual(interaction_field(4, 4), nuisance, weights),
            residual(interaction_field(4, 4, second_direction=True), nuisance, weights),
            residual(interaction_field(4, 4) - 0.6 * interaction_field(4, 4, second_direction=True), nuisance, weights),
            residual(0.3 * interaction_field(4, 4) + interaction_field(4, 4, second_direction=True), nuisance, weights),
        ]
    )
    multi_sv, multi_ratio = singular_ratio(multi, weights)
    return {
        "test_id": "rank1_perturbation_bound_control",
        "kind": "theorem_backed_numerical_control",
        "rank1_noise_singular_values": singular.tolist(),
        "rank1_noise_sigma2": float(singular[1]),
        "noise_operator_norm": noise_op,
        "sigma2_minus_noise_opnorm": float(singular[1] - noise_op),
        "multidirectional_singular_values": multi_sv,
        "multidirectional_sigma2_over_sigma1": multi_ratio,
        "review_floor": RANK_SHADOW_FLOOR,
        "interpretation": "sigma2(M) <= ||E||_2 is theorem-backed; the 0.25 floor is only a review heuristic",
    }


def block_random_subspace_beta_squared_capture_control(seed: int, draws: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 12)
    weights = grid_weights(4, 4)
    nuisance = additive_design(4, 4)
    basis_res = residual_space_basis(4, 4, weights)
    d = int(basis_res.shape[0])
    k = 2
    signal_a = residual(interaction_field(4, 4), nuisance, weights)
    signal_b = residual(interaction_field(4, 4, second_direction=True), nuisance, weights)
    true_basis = weighted_orthonormal_rows(np.vstack([signal_a, signal_b]), weights, dim=k)
    orth_candidate = residual(rng.normal(size=16), nuisance, weights)
    orth_candidate = residual(orth_candidate, true_basis.T, weights)
    orth_candidate = orth_candidate / max(weighted_norm(orth_candidate, weights), EPS)
    heldout = 0.8 * true_basis[0] + 0.5 * true_basis[1] + 0.10 * orth_candidate
    true_capture = squared_capture(heldout, true_basis, weights)
    random_capture = []
    discarded = 0
    for _ in range(draws):
        coords = rng.normal(size=(k, d))
        random_basis = weighted_orthonormal_rows(coords @ basis_res, weights, dim=k)
        if np.linalg.matrix_rank(random_basis) < k:
            discarded += 1
            continue
        random_capture.append(squared_capture(heldout, random_basis, weights))
    random_arr = np.asarray(random_capture, dtype=float)
    alpha = k / 2.0
    beta = (d - k) / 2.0
    beta_mean = alpha / (alpha + beta)
    beta_var = alpha * beta / ((alpha + beta) ** 2 * (alpha + beta + 1.0))
    p95 = float(np.quantile(random_arr, 0.95))
    p99 = float(np.quantile(random_arr, 0.99))
    return {
        "test_id": "random_subspace_beta_squared_capture_control",
        "kind": "beta_law_and_monte_carlo_diagnostic",
        "draws_requested": draws,
        "draws_used": int(len(random_capture)),
        "discarded_random_draws": int(discarded),
        "residual_space_dimension": d,
        "random_k_plane_dimension": k,
        "statistic": "squared_capture",
        "beta_alpha": alpha,
        "beta_beta": beta,
        "beta_mean": beta_mean,
        "beta_variance": beta_var,
        "random_squared_capture_mean": float(np.mean(random_arr)),
        "random_squared_capture_variance": float(np.var(random_arr)),
        "beta_mean_error": abs(float(np.mean(random_arr)) - beta_mean),
        "beta_variance_error": abs(float(np.var(random_arr)) - beta_var),
        "random_squared_capture_p95": p95,
        "random_squared_capture_p99": p99,
        "true_subspace_squared_capture": true_capture,
        "true_squared_capture_quantile": float(np.mean(random_arr <= true_capture)),
        "interpretation": "the analytic Beta law applies to squared capture after whitening, not to unsquared norm ratio",
    }


def block_square_holonomy_telescoping_control(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 13)
    dim = 4
    weights = normalize(np.ones(dim))
    nuisance_vectors = [
        np.array([[1.0], [0.0], [0.0], [0.0]]),
        np.array([[1.0], [1.0], [0.0], [0.0]]),
        np.array([[0.0], [1.0], [1.0], [0.0]]),
        np.array([[0.0], [0.0], [1.0], [1.0]]),
    ]
    projectors = [residual_projector(n, weights) for n in nuisance_vectors]
    maps_p = [rng.normal(size=(dim, dim)) for _ in range(3)]
    maps_q = [maps_p[0], maps_p[1] + 0.05 * rng.normal(size=(dim, dim)), maps_p[2]]

    def defect_and_terms(maps: list[np.ndarray]) -> tuple[np.ndarray, list[np.ndarray]]:
        raw = path_product(projectors, maps, set())
        previous = raw
        terms = []
        for i in range(1, len(maps)):
            current = path_product(projectors, maps, set(range(1, i + 1)))
            terms.append(current - previous)
            previous = current
        full = path_product(projectors, maps, set(range(1, len(maps))))
        return full - raw, terms

    raw_p = path_product(projectors, maps_p, set())
    raw_q = path_product(projectors, maps_q, set())
    full_p = path_product(projectors, maps_p, set(range(1, len(maps_p))))
    full_q = path_product(projectors, maps_q, set(range(1, len(maps_q))))
    defect_p, terms_p = defect_and_terms(maps_p)
    defect_q, terms_q = defect_and_terms(maps_q)
    telescope_error_p = fro_norm(defect_p - sum(terms_p, np.zeros_like(defect_p)))
    telescope_error_q = fro_norm(defect_q - sum(terms_q, np.zeros_like(defect_q)))
    omega = full_p - full_q
    raw_diff = raw_p - raw_q
    square_identity_error = fro_norm(omega - (raw_diff + defect_p - defect_q))
    return {
        "test_id": "square_holonomy_telescoping_control",
        "kind": "theorem_backed_regression",
        "path_length": len(maps_p),
        "p_telescoping_identity_error": telescope_error_p,
        "q_telescoping_identity_error": telescope_error_q,
        "max_telescoping_identity_error": max(telescope_error_p, telescope_error_q),
        "square_identity_error": square_identity_error,
        "raw_path_difference_fro_norm": fro_norm(raw_diff),
        "projected_square_holonomy_fro_norm": fro_norm(omega),
        "interpretation": "projected holonomy decomposes into raw path mismatch plus transported internal projection leakage",
    }


def block_triple_overlap_gluing_cocycle() -> dict[str, Any]:
    weights = normalize(np.ones(3))
    edge_absorbed = {
        ("A", "B"): np.array([1.0, 0.0, 0.0]),
        ("B", "C"): np.array([0.0, 1.0, 0.0]),
        ("A", "C"): np.array([1.0, 1.0, 0.0]),
    }
    edge_bad = dict(edge_absorbed)
    edge_bad[("A", "C")] = np.array([1.0, 1.0, 2.1])
    absorbed_cycle = edge_absorbed[("A", "B")] + edge_absorbed[("B", "C")] - edge_absorbed[("A", "C")]
    bad_cycle = edge_bad[("A", "B")] + edge_bad[("B", "C")] - edge_bad[("A", "C")]
    return {
        "test_id": "triple_overlap_gluing_cocycle",
        "kind": "gluing_regression_control",
        "absorbed_cycle_residual_norm": weighted_norm(absorbed_cycle, weights),
        "obstruction_cycle_residual_norm": weighted_norm(bad_cycle, weights),
        "interpretation": "a triple-overlap mismatch is only meaningful after local absorption has failed",
    }


def make_metric_blocks(seed: int, draws: int) -> list[dict[str, Any]]:
    return [
        block_exact_product_weight_equality_control(),
        block_product_reweighting_separation(),
        block_quotient_descent_control(),
        block_common_ambient_registration_control(),
        block_projection_evolution_commutator_obstruction(),
        block_raw_path_equality_square_control(),
        block_coarsening_non_naturality_trap(),
        block_rank1_perturbation_bound_control(seed),
        block_random_subspace_beta_squared_capture_control(seed, draws),
        block_square_holonomy_telescoping_control(seed),
        block_triple_overlap_gluing_cocycle(),
    ]


def evaluate_test(metrics: dict[str, Any], contract: dict[str, dict[str, Any]]) -> dict[str, Any]:
    test_id = metrics["test_id"]
    thresholds = contract[test_id]
    if test_id == "exact_product_weight_equality_control":
        passed = (
            metrics["product_weight_max_abs_error"] <= thresholds["max_product_weight_error"]
            and metrics["residual_difference_norm_under_observed_weight"] <= thresholds["max_residual_difference_norm"]
        )
    elif test_id == "product_reweighting_separation":
        passed = (
            abs(metrics["max_abs_diff"] - thresholds["expected_max_abs_diff"]) <= thresholds["max_abs_diff_tolerance"]
            and abs(metrics["observed_raw_weight_norm_diff"] - thresholds["expected_raw_weight_norm_diff"])
            <= thresholds["raw_weight_norm_diff_tolerance"]
        )
    elif test_id == "quotient_descent_control":
        passed = (
            metrics["good_coset_disagreement"] <= thresholds["max_good_coset_disagreement"]
            and metrics["bad_coset_disagreement"] >= thresholds["min_bad_coset_disagreement"]
        )
    elif test_id == "common_ambient_registration_control":
        passed = (
            metrics["isometric_registration_metric_diff"] <= thresholds["max_isometric_registration_metric_diff"]
            and metrics["unregistered_use_count"] <= thresholds["max_unregistered_use_count"]
            and metrics["bad_registration_metric_diff"] >= thresholds["min_bad_registration_metric_diff"]
        )
    elif test_id == "projection_evolution_commutator_obstruction":
        passed = (
            metrics["good_commutator_fro_norm"] <= thresholds["max_good_commutator_fro_norm"]
            and metrics["bad_commutator_fro_norm"] >= thresholds["min_bad_commutator_fro_norm"]
            and metrics["bad_signal_leakage_norm"] >= thresholds["min_bad_signal_leakage_norm"]
        )
    elif test_id == "raw_path_equality_square_control":
        passed = (
            metrics["raw_path_max_abs_diff"] <= thresholds["max_raw_path_diff"]
            and metrics["square_holonomy_norm"] <= thresholds["max_square_holonomy_norm"]
        )
    elif test_id == "coarsening_non_naturality_trap":
        passed = (
            metrics["raw_path_max_abs_diff"] <= thresholds["max_raw_path_diff"]
            and metrics["path_dependent_bad_nuisance_holonomy_norm"] >= thresholds["min_bad_holonomy_norm"]
        )
    elif test_id == "rank1_perturbation_bound_control":
        passed = (
            metrics["sigma2_minus_noise_opnorm"] <= thresholds["max_sigma2_minus_noise_opnorm"]
            and (metrics["multidirectional_sigma2_over_sigma1"] or 0.0)
            >= thresholds["min_multidirectional_sigma2_over_sigma1"]
        )
    elif test_id == "random_subspace_beta_squared_capture_control":
        passed = (
            metrics["beta_mean_error"] <= thresholds["max_beta_mean_error"]
            and metrics["beta_variance_error"] <= thresholds["max_beta_variance_error"]
            and metrics["true_subspace_squared_capture"] - metrics["random_squared_capture_p99"]
            >= thresholds["min_true_sq_capture_minus_p99"]
            and metrics["true_squared_capture_quantile"] >= thresholds["min_true_sq_capture_quantile"]
        )
    elif test_id == "square_holonomy_telescoping_control":
        passed = (
            metrics["max_telescoping_identity_error"] <= thresholds["max_telescoping_identity_error"]
            and metrics["square_identity_error"] <= thresholds["max_square_identity_error"]
        )
    elif test_id == "triple_overlap_gluing_cocycle":
        passed = (
            metrics["absorbed_cycle_residual_norm"] <= thresholds["max_absorbed_cycle_residual_norm"]
            and metrics["obstruction_cycle_residual_norm"] >= thresholds["min_obstruction_cycle_residual_norm"]
        )
    elif test_id == "threshold_contract_single_source_control":
        passed = (
            (
                not thresholds["require_contract_hash_match"]
                or metrics["runtime_threshold_contract_sha256"] == metrics["json_threshold_contract_sha256"]
            )
            and (not thresholds["require_per_test_threshold_match"] or len(metrics["per_test_threshold_mismatches"]) == 0)
            and (not thresholds["require_central_evaluator"] or metrics["central_evaluator_used"])
        )
    else:
        raise KeyError(f"no evaluator for {test_id}")
    out = dict(metrics)
    out["thresholds"] = thresholds
    out["threshold_contract_hash"] = sha256_json(contract)
    out["evaluated_by"] = "evaluate_test"
    out["pass"] = bool(passed)
    return out


def block_threshold_contract_single_source_control(
    evaluated_blocks: list[dict[str, Any]],
    contract: dict[str, dict[str, Any]],
    json_threshold_contract_sha256: str,
    json_threshold_contract_source: str,
) -> dict[str, Any]:
    contract_hash = sha256_json(contract)
    per_test_mismatches = []
    for block in evaluated_blocks:
        test_id = block["test_id"]
        if block.get("thresholds") != contract[test_id]:
            per_test_mismatches.append(test_id)
        if block.get("threshold_contract_hash") != contract_hash:
            per_test_mismatches.append(f"{test_id}:hash")
    metrics = {
        "test_id": "threshold_contract_single_source_control",
        "kind": "meta_contract_control",
        "runtime_threshold_contract_sha256": contract_hash,
        "json_threshold_contract_sha256": json_threshold_contract_sha256,
        "json_threshold_contract_source": json_threshold_contract_source,
        "per_test_threshold_mismatches": per_test_mismatches,
        "central_evaluator_function": "evaluate_test",
        "central_evaluator_used": all(block.get("evaluated_by") == "evaluate_test" for block in evaluated_blocks),
        "interpretation": "all pass/fail logic is assigned by evaluate_test against the serialized top-level threshold contract",
    }
    return metrics


def build_result(
    seed: int,
    draws: int,
    json_threshold_contract_sha256: str,
    json_threshold_contract_source: str,
) -> dict[str, Any]:
    contract = build_threshold_contract()
    metric_blocks = make_metric_blocks(seed=seed, draws=draws)
    evaluated = [evaluate_test(block, contract) for block in metric_blocks]
    meta_metrics = block_threshold_contract_single_source_control(
        evaluated_blocks=evaluated,
        contract=contract,
        json_threshold_contract_sha256=json_threshold_contract_sha256,
        json_threshold_contract_source=json_threshold_contract_source,
    )
    evaluated.append(evaluate_test(meta_metrics, contract))
    all_pass = all(block["pass"] for block in evaluated)
    return {
        "schema": "debranded_residual_transport_synthetic_harness_v1_2",
        "created_utc": utc_now(),
        "seed": seed,
        "draws": draws,
        "environment": environment_metadata(),
        "evidence_boundary": {
            "mode": "Mode A finite-dimensional synthetic harness only",
            "strongest_allowed_verdict": "definitions_and_harness_viable_only",
            "mode_b_maofield_empirical_status": "insufficient_artifact",
            "blocked_claims": BLOCKED_CLAIMS,
        },
        "threshold_contract": contract,
        "threshold_contract_sha256": sha256_json(contract),
        "all_synthetic_controls_passed": all_pass,
        "blocks": evaluated,
        "allowed_interpretation": "v1.2 note/harness implementation is internally checkable on synthetic finite examples only",
        "forbidden_interpretation": "passing this harness is not MaoField empirical evidence and does not authorize training or a new loss",
    }


def readback_threshold_contract_sha256(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return sha256_json(data["threshold_contract"])


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_summary(path: Path, result: dict[str, Any], json_rel: str) -> None:
    lines = [
        "# Debranded Residual Transport Synthetic Harness v1.2",
        "",
        "Date: 2026-06-27 CST",
        "",
        "## Boundary",
        "",
        "This is a zero-GPU synthetic harness for the debranded finite-dimensional",
        "mathematics direction. It is not a MaoField empirical result and does not",
        "authorize training, checkpoint loading, full-panel generation, model",
        "inference, or a new loss.",
        "",
        "Strongest allowed verdict:",
        "",
        "```text",
        "definitions_and_harness_viable_only",
        "```",
        "",
        "Mode B MaoField status remains:",
        "",
        "```text",
        "insufficient_artifact",
        "```",
        "",
        "## Artifact",
        "",
        "```text",
        json_rel,
        "```",
        "",
        "## v1.2 Structure",
        "",
        "- metrics are generated by block functions;",
        "- pass/fail is assigned only by `evaluate_test`;",
        "- all thresholds come from `build_threshold_contract`;",
        "- top-level JSON serializes the same threshold contract;",
        "- `threshold_contract_single_source_control` verifies the central evaluator path;",
        "- JSON-side threshold hash is read back from a written JSON artifact.",
        "",
        "## Blocks",
        "",
    ]
    for block in result["blocks"]:
        suffix = ""
        if "verdict" in block:
            suffix = f" ({block['verdict']})"
        lines.append(f"- `{block['test_id']}`: {'pass' if block['pass'] else 'fail'}{suffix}")
    lines.extend(
        [
            "",
            "All synthetic controls passed:",
            "",
            "```text",
            str(result["all_synthetic_controls_passed"]).lower(),
            "```",
            "",
            "## Selected Metrics",
            "",
            "```text",
        ]
    )
    selected = [
        ("quotient_descent_control", ["good_coset_disagreement", "bad_coset_disagreement"]),
        ("common_ambient_registration_control", ["isometric_registration_metric_diff", "bad_registration_metric_diff"]),
        ("rank1_perturbation_bound_control", ["sigma2_minus_noise_opnorm", "multidirectional_sigma2_over_sigma1"]),
        ("random_subspace_beta_squared_capture_control", ["beta_mean_error", "beta_variance_error", "random_squared_capture_p99", "true_subspace_squared_capture"]),
        ("square_holonomy_telescoping_control", ["max_telescoping_identity_error", "square_identity_error"]),
        (
            "threshold_contract_single_source_control",
            [
                "runtime_threshold_contract_sha256",
                "json_threshold_contract_sha256",
                "json_threshold_contract_source",
                "central_evaluator_used",
            ],
        ),
    ]
    by_id = {block["test_id"]: block for block in result["blocks"]}
    for test_id, keys in selected:
        block = by_id[test_id]
        for key in keys:
            lines.append(f"{test_id}.{key} = {fmt(block[key])}")
    lines.extend(
        [
            "```",
            "",
            "## Interpretation",
            "",
            "The v1.2 harness implements the small-patch gates from report (28):",
            "registered ambient controls, squared-capture random-subspace closure,",
            "product/non-product boundary regressions, quotient descent, rank-shadow",
            "bounds, per-edge square holonomy telescoping, and a single-source",
            "threshold contract. Passing these toy controls supports formal design",
            "review only.",
            "",
            "Blocked interpretations:",
            "",
            "```text",
        ]
    )
    lines.extend(BLOCKED_CLAIMS)
    lines.extend(["```", ""])
    write_text(path, "\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary-md", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260627)
    parser.add_argument("--draws", type=int, default=5000)
    parser.add_argument(
        "--json-rel",
        default="docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract_hash = sha256_json(build_threshold_contract())
    draft = build_result(
        seed=args.seed,
        draws=args.draws,
        json_threshold_contract_sha256=contract_hash,
        json_threshold_contract_source="prewrite_contract_hash_for_readback_bootstrap",
    )
    write_json(args.out, draft)
    readback_hash = readback_threshold_contract_sha256(args.out)
    result = build_result(
        seed=args.seed,
        draws=args.draws,
        json_threshold_contract_sha256=readback_hash,
        json_threshold_contract_source="readback_from_written_json_threshold_contract",
    )
    write_json(args.out, result)
    final_readback_hash = readback_threshold_contract_sha256(args.out)
    write_summary(args.summary_md, result, args.json_rel)
    if final_readback_hash != result["threshold_contract_sha256"]:
        return 1
    if not result["all_synthetic_controls_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
