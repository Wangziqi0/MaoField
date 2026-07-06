#!/usr/bin/env python3
"""Exact rational v1.5 certificate for GQ-FCR.

This script is synthetic-only. It uses fractions.Fraction to verify a finite
two-chart overlap-gauge quotient certificate without floating point arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from fractions import Fraction
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]


def diag(v):
    return [[v[i] if i == j else Fraction(0, 1) for j in range(len(v))] for i in range(len(v))]


def matmul(a, b):
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def matvec(a, v):
    return [sum(row[j] * v[j] for j in range(len(v))) for row in a]


def mat_sub(a, b):
    return [
        [a[i][j] - b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def inverse(a):
    n = len(a)
    aug = [list(a[i]) + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [
                    aug[row][j] - factor * aug[col][j]
                    for j in range(2 * n)
                ]
    return [row[n:] for row in aug]


def gram_matrix(basis, weights):
    n = len(weights)
    k = len(basis)
    return [
        [sum(weights[r] * basis[i][r] * basis[j][r] for r in range(n)) for j in range(k)]
        for i in range(k)
    ]


def projection_matrix(basis, weights):
    """Weighted orthogonal projection onto span(basis)."""
    n = len(weights)
    k = len(basis)
    gram = gram_matrix(basis, weights)
    gram_inv = inverse(gram)
    proj = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            proj[r][c] = sum(
                basis[i][r] * gram_inv[i][j] * basis[j][c] * weights[c]
                for i in range(k)
                for j in range(k)
            )
    return proj, gram, gram_inv


def projection_coordinates(basis, weights, gram_inv, vector):
    """Coordinates of the weighted projection onto span(basis)."""
    rhs = [weighted_dot(vector, basis_vector, weights) for basis_vector in basis]
    return [
        sum(gram_inv[i][j] * rhs[j] for j in range(len(rhs)))
        for i in range(len(rhs))
    ]


def weighted_dot(u, v, weights):
    return sum(weights[i] * u[i] * v[i] for i in range(len(weights)))


def norm_sq(v, weights):
    return weighted_dot(v, v, weights)


def frac_s(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def vec_s(v):
    return [frac_s(x) for x in v]


def mat_s(a):
    return [vec_s(row) for row in a]


def all_zero(v):
    return all(x == 0 for x in v)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_control(name, mismatch, basis, weights, gram_inv, projection, complement):
    projected_gauge = matvec(projection, mismatch)
    quotient_residual = matvec(complement, mismatch)
    coeffs = projection_coordinates(basis, weights, gram_inv, mismatch)
    return {
        "name": name,
        "s_1_row_major": vec_s(mismatch),
        "s_2_row_major": vec_s([Fraction(0, 1)] * len(mismatch)),
        "raw_mismatch_row_major": vec_s(mismatch),
        "gauge_coefficients_for_basis": vec_s(coeffs),
        "projected_gauge_component_row_major": vec_s(projected_gauge),
        "quotient_residual_row_major": vec_s(quotient_residual),
        "delta_squared": frac_s(norm_sq(quotient_residual, weights)),
    }


def build_certificate():
    labels = ["q1_b1", "q1_b2", "q2_b1", "q2_b2"]
    weights = [Fraction(1, 4)] * 4
    one = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]
    q = [Fraction(-1, 1), Fraction(-1, 1), Fraction(1, 1), Fraction(1, 1)]
    b = [Fraction(-1, 1), Fraction(1, 1), Fraction(-1, 1), Fraction(1, 1)]
    checkerboard = [Fraction(1, 1), Fraction(-1, 1), Fraction(-1, 1), Fraction(1, 1)]
    basis = [one, q, b]

    ident = eye(4)
    zero = [[Fraction(0, 1) for _ in range(4)] for _ in range(4)]
    weights_matrix = diag(weights)

    projection, gram, gram_inv = projection_matrix(basis, weights)
    complement = mat_sub(ident, projection)
    enlarged_basis = [one, q, b, checkerboard]
    enlarged_projection, enlarged_gram, enlarged_gram_inv = projection_matrix(enlarged_basis, weights)
    enlarged_complement = mat_sub(ident, enlarged_projection)

    m_plus = [Fraction(1, 1), Fraction(2, 1), Fraction(3, 2), Fraction(5, 2)]
    m_minus = checkerboard

    positive = build_control("m_plus_additive_absorbed", m_plus, basis, weights, gram_inv, projection, complement)
    negative = build_control("m_minus_checkerboard_obstruction", m_minus, basis, weights, gram_inv, projection, complement)

    enlarged_residual = matvec(enlarged_complement, m_minus)
    negative_inner_products = {
        "one": frac_s(weighted_dot(m_minus, one, weights)),
        "q": frac_s(weighted_dot(m_minus, q, weights)),
        "b": frac_s(weighted_dot(m_minus, b, weights)),
    }

    checks = {
        "weights_strictly_positive": all(w > 0 for w in weights),
        "gauge_gram_invertible": bool(gram_inv),
        "projection_idempotent": matmul(projection, projection) == projection,
        "projection_weighted_self_adjoint": matmul(weights_matrix, projection) == matmul(transpose(projection), weights_matrix),
        "complement_annihilates_gauge_basis": all(all_zero(matvec(complement, vector)) for vector in basis),
        "positive_control_coefficients_exact": positive["gauge_coefficients_for_basis"] == ["7/4", "1/4", "1/2"],
        "positive_control_residual_zero": positive["quotient_residual_row_major"] == ["0", "0", "0", "0"],
        "positive_control_delta_squared_zero": positive["delta_squared"] == "0",
        "negative_control_orthogonal_to_gauge": negative_inner_products == {"one": "0", "q": "0", "b": "0"},
        "negative_control_residual_equals_mismatch": negative["quotient_residual_row_major"] == vec_s(m_minus),
        "negative_control_delta_squared_one": negative["delta_squared"] == "1",
        "enlarged_gauge_gram_invertible": bool(enlarged_gram_inv),
        "enlarged_gauge_projection_is_identity": enlarged_projection == ident,
        "enlarged_gauge_absorbs_checkerboard": all_zero(enlarged_residual),
        "gauge_monotonicity_exact": norm_sq(enlarged_residual, weights) <= Fraction(1, 1),
    }

    return {
        "artifact": "exact_gq_fcr_v1_5_20260706",
        "date": "2026-07-06 CST",
        "status": "synthetic_only_exact_fraction_certificate",
        "evidence_boundary": {
            "strongest_allowed_verdict": "definitions_and_exact_certificate_viable_only",
            "mode_b_maofield_status": "insufficient_artifact",
            "not_authorized": [
                "broad_sheaf_theory",
                "broad_consistency_radius_theory",
                "broad_contextuality_theory",
                "broad_dependent_input_anova_theory",
                "broad_noncommuting_projection_theory",
                "maofield_empirical_positive_result",
                "full_panel",
                "checkpoint_loading",
                "model_inference",
                "training",
                "new_loss",
                "observed_residual_field",
                "observed_transport_field",
                "observed_holonomy_field",
                "glass_box_broken",
                "paper_ready_or_peer_reviewed_claim",
            ],
        },
        "carrier_manifest_1": {"name": "I_1", "labels": labels},
        "carrier_manifest_2": {"name": "I_2", "labels": labels},
        "overlap_manifest_12": {"name": "O_12", "labels": labels},
        "restriction_matrices_row_major": {
            "rho_1": mat_s(ident),
            "rho_2": mat_s(ident),
        },
        "weights_row_major": vec_s(weights),
        "gauge_basis_row_major": {
            "one": vec_s(one),
            "q": vec_s(q),
            "b": vec_s(b),
        },
        "gauge_gram_matrix_row_major": mat_s(gram),
        "gauge_gram_inverse_row_major": mat_s(gram_inv),
        "projection_matrix_row_major": mat_s(projection),
        "complement_projection_matrix_row_major": mat_s(complement),
        "positive_control": positive,
        "negative_control": {
            **negative,
            "weighted_inner_products_with_gauge_basis": negative_inner_products,
        },
        "enlarged_gauge_monotonicity_check": {
            "enlarged_basis_row_major": {
                "one": vec_s(one),
                "q": vec_s(q),
                "b": vec_s(b),
                "checkerboard": vec_s(checkerboard),
            },
            "enlarged_gauge_gram_matrix_row_major": mat_s(enlarged_gram),
            "enlarged_projection_matrix_row_major": mat_s(enlarged_projection),
            "delta_squared_m_minus_original_gamma": "1",
            "delta_squared_m_minus_enlarged_gamma": frac_s(norm_sq(enlarged_residual, weights)),
        },
        "gauge_transfer_matrices_row_major": None,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": "fractions.Fraction",
            "random_draws": 0,
        },
    }


def write_markdown(certificate, path, json_name, json_sha):
    checks = certificate["checks"]
    pos = certificate["positive_control"]
    neg = certificate["negative_control"]
    mono = certificate["enlarged_gauge_monotonicity_check"]
    lines = [
        "# Exact GQ-FCR Certificate v1.5",
        "",
        "Date: 2026-07-06 CST",
        "",
        "Status: synthetic-only exact rational certificate for the v1.5",
        "Gauge-Quotiented Finite Consistency Radius formal note. This is not a",
        "MaoField empirical result and is not a broad consistency-radius, sheaf,",
        "contextuality, ANOVA, or projection-theory claim.",
        "",
        "## Artifact",
        "",
        "```text",
        json_name,
        f"sha256={json_sha}",
        "```",
        "",
        "## Boundary",
        "",
        "Allowed ceiling:",
        "",
        "```text",
        certificate["evidence_boundary"]["strongest_allowed_verdict"],
        "```",
        "",
        "Mode B MaoField empirical status:",
        "",
        "```text",
        certificate["evidence_boundary"]["mode_b_maofield_status"],
        "```",
        "",
        "## Exact Definition Checked",
        "",
        "```text",
        "Delta^2_12(s_1,s_2; Gamma_12)",
        "  = min_{gamma in Gamma_12} ||rho_1 s_1 - rho_2 s_2 - gamma||^2_w",
        "  = ||(I - P_Gamma)(rho_1 s_1 - rho_2 s_2)||^2_w",
        "```",
        "",
        "All arithmetic is exact `fractions.Fraction`; JSON stores rationals as",
        "strings. In the controls, `I_1 = I_2 = O_12`, `rho_1 = rho_2 = I`,",
        "and `s_2 = 0`, so each raw mismatch is `s_1`.",
        "",
        "## Exact Checks",
        "",
    ]
    for name, passed in checks.items():
        lines.append(f"- `{name}`: {'pass' if passed else 'fail'}")
    lines.extend([
        "",
        f"All checks passed: `{str(certificate['all_checks_passed']).lower()}`",
        "",
        "## Positive Control",
        "",
        "```text",
        "m_plus = ['1', '2', '3/2', '5/2']",
        f"gauge coefficients [one,q,b] = {pos['gauge_coefficients_for_basis']}",
        f"(I-P_Gamma)m_plus = {pos['quotient_residual_row_major']}",
        f"Delta^2(m_plus; Gamma) = {pos['delta_squared']}",
        "```",
        "",
        "## Negative Control",
        "",
        "```text",
        "m_minus = ['1', '-1', '-1', '1']",
        f"weighted inner products = {neg['weighted_inner_products_with_gauge_basis']}",
        f"(I-P_Gamma)m_minus = {neg['quotient_residual_row_major']}",
        f"Delta^2(m_minus; Gamma) = {neg['delta_squared']}",
        "```",
        "",
        "## Gauge Monotonicity Witness",
        "",
        "```text",
        "Gamma' = span{one, q, b, checkerboard}",
        f"Delta^2(m_minus; Gamma) = {mono['delta_squared_m_minus_original_gamma']}",
        f"Delta^2(m_minus; Gamma') = {mono['delta_squared_m_minus_enlarged_gamma']}",
        "```",
        "",
        "## Interpretation",
        "",
        "`Delta^2 = 0` certifies compatibility modulo the declared overlap gauge.",
        "A stronger statement about realized gauge-adjusted local sections requires",
        "extra local gauge parameter spaces and overlap transfer maps. This",
        "certificate does not include or claim that stronger data.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Build exact GQ-FCR v1.5 artifacts.")
    parser.add_argument(
        "--out-json",
        default="docs/infra/debranded_residual_transport/exact_gq_fcr_v1_5_20260706.json",
    )
    parser.add_argument(
        "--out-md",
        default="docs/infra/debranded_residual_transport/EXACT_GQ_FCR_V1_5_20260706.md",
    )
    args = parser.parse_args()

    certificate = build_certificate()
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    json_sha = sha256_file(out_json)
    write_markdown(certificate, out_md, out_json.name, json_sha)
    print(f"wrote {out_json} sha256={json_sha}")
    print(f"wrote {out_md}")
    print(f"all_checks_passed={certificate['all_checks_passed']}")
    raise SystemExit(0 if certificate["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
