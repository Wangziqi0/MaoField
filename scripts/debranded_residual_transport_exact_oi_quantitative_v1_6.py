#!/usr/bin/env python3
"""Exact rational v1.6 support for the quantitative OI norm companion.

This script is synthetic-only. It uses fractions.Fraction to verify the 2x2
arithmetic for the principal-angle OI formula. It is not proof authority; the
mathematical claim is carried by the analytic finite-dimensional proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from fractions import Fraction
from pathlib import Path


def frac_s(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def two_by_two_quantitative_values(a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> dict:
    r1 = a + b
    r2 = c + d
    s1 = a + c
    s2 = b + d
    tau = a * d - b * c
    denom = r1 * r2 * s1 * s2
    rho_sq = tau * tau / denom
    oi_sq = rho_sq * (1 - rho_sq)
    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "r1": r1,
        "r2": r2,
        "s1": s1,
        "s2": s2,
        "tau": tau,
        "denominator": denom,
        "rho_squared": rho_sq,
        "oi_operator_norm_squared": oi_sq,
    }


def serial_values(values: dict) -> dict:
    return {key: frac_s(value) for key, value in values.items()}


def build_certificate() -> dict:
    witness = two_by_two_quantitative_values(
        Fraction(1, 11),
        Fraction(2, 11),
        Fraction(3, 11),
        Fraction(5, 11),
    )
    product_control = two_by_two_quantitative_values(
        Fraction(1, 6),
        Fraction(1, 3),
        Fraction(1, 6),
        Fraction(1, 3),
    )
    old_artifact_norm_sq = Fraction(61, 177408)
    ratio_to_old_artifact = witness["oi_operator_norm_squared"] / old_artifact_norm_sq

    checks = {
        "witness_strictly_positive": all(witness[key] > 0 for key in ["a", "b", "c", "d"]),
        "witness_probability_sum_one": sum(witness[key] for key in ["a", "b", "c", "d"]) == 1,
        "witness_tau_exact": witness["tau"] == Fraction(-1, 121),
        "witness_rho_squared_exact": witness["rho_squared"] == Fraction(1, 672),
        "witness_oi_operator_norm_squared_exact": witness["oi_operator_norm_squared"] == Fraction(671, 451584),
        "old_v1_4_fixed_witness_norm_squared_exact": old_artifact_norm_sq == Fraction(61, 177408),
        "operator_norm_not_fixed_witness_norm": witness["oi_operator_norm_squared"] != old_artifact_norm_sq,
        "operator_to_fixed_witness_ratio_exact": ratio_to_old_artifact == Fraction(121, 28),
        "product_control_tau_zero": product_control["tau"] == 0,
        "product_control_rho_squared_zero": product_control["rho_squared"] == 0,
        "product_control_oi_squared_zero": product_control["oi_operator_norm_squared"] == 0,
    }

    return {
        "artifact": "exact_oi_quantitative_v1_6_20260707",
        "date": "2026-07-07 CST",
        "status": "synthetic_only_exact_fraction_support",
        "evidence_boundary": {
            "mode_b_maofield_status": "insufficient_artifact",
            "proof_authority": "analytic finite-dimensional proof in FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md",
            "not_authorized": [
                "maofield_empirical_positive_result",
                "full_panel",
                "checkpoint_loading",
                "model_inference",
                "training",
                "new_loss",
                "observed_residual_field",
                "observed_interaction_field",
                "broad_projection_theory",
                "proof_by_json",
            ],
        },
        "formula": {
            "two_by_two_rho_squared": "(ad-bc)^2 / ((a+b)(c+d)(a+c)(b+d))",
            "two_by_two_oi_squared": "rho^2 * (1-rho^2)",
        },
        "witness_table": {
            "w": [["1/11", "2/11"], ["3/11", "5/11"]],
            "values": serial_values(witness),
        },
        "normalization_guard": {
            "v1_6_operator_norm_squared": frac_s(witness["oi_operator_norm_squared"]),
            "v1_4_fixed_witness_artifact_norm_squared": frac_s(old_artifact_norm_sq),
            "ratio_v1_6_to_v1_4": frac_s(ratio_to_old_artifact),
            "interpretation": "operator norm after input normalization is not the same quantity as one fixed witness output norm",
        },
        "product_control_table": {
            "w": [["1/6", "1/3"], ["1/6", "1/3"]],
            "values": serial_values(product_control),
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": "fractions.Fraction",
            "random_draws": 0,
        },
    }


def write_markdown(certificate: dict, path: Path, json_name: str, json_sha: str) -> None:
    checks = certificate["checks"]
    witness = certificate["witness_table"]["values"]
    guard = certificate["normalization_guard"]
    product = certificate["product_control_table"]["values"]

    lines = [
        "# Exact Quantitative OI Norm Support v1.6",
        "",
        "Date: 2026-07-07 CST",
        "",
        "Status: synthetic-only exact rational support for the v1.6",
        "quantitative OI norm companion. This is not a MaoField empirical",
        "result and is not proof authority.",
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
        "Mode B MaoField empirical status:",
        "",
        "```text",
        "insufficient_artifact",
        "```",
        "",
        "The mathematical claim is carried by the analytic finite-dimensional",
        "proof in `FORMAL_NOTE_V1_6_QUANTITATIVE_OI_NORM_20260707.md`, not by",
        "this JSON/Markdown support artifact.",
        "",
        "## Exact Checks",
        "",
    ]
    for name, passed in checks.items():
        lines.append(f"- `{name}`: {'pass' if passed else 'fail'}")

    lines.extend([
        "",
        "Overall:",
        "",
        "```text",
        f"all_checks_passed={certificate['all_checks_passed']}",
        "```",
        "",
        "## v1.3 Witness Table",
        "",
        "```text",
        "w = (1/11) [[1,2],",
        "            [3,5]]",
        f"tau = {witness['tau']}",
        f"rho^2 = {witness['rho_squared']}",
        f"(OI^op_N_add)^2 = {witness['oi_operator_norm_squared']}",
        "```",
        "",
        "## Normalization Guard",
        "",
        "```text",
        f"v1.6 operator norm squared = {guard['v1_6_operator_norm_squared']}",
        f"v1.4 fixed witness artifact norm squared = {guard['v1_4_fixed_witness_artifact_norm_squared']}",
        f"ratio = {guard['ratio_v1_6_to_v1_4']}",
        "```",
        "",
        "These are different quantities. The v1.6 value is an operator norm",
        "after input normalization. The v1.4 value is the output norm of one",
        "fixed witness.",
        "",
        "## Product Control",
        "",
        "```text",
        "w = [[1/6, 1/3],",
        "     [1/6, 1/3]]",
        f"tau = {product['tau']}",
        f"rho^2 = {product['rho_squared']}",
        f"(OI^op_N_add)^2 = {product['oi_operator_norm_squared']}",
        "```",
        "",
        "## Forbidden Upgrades",
        "",
        "Do not use this support artifact to claim empirical positives,",
        "observed residual fields, broad projection theory, or proof by JSON.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build exact quantitative OI v1.6 support artifacts.")
    parser.add_argument("--output-dir", required=True, help="directory for JSON and Markdown outputs")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "exact_oi_quantitative_v1_6_20260707.json"
    md_path = out_dir / "EXACT_OI_QUANTITATIVE_V1_6_20260707.md"

    certificate = build_certificate()
    json_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    json_sha = sha256_file(json_path)
    write_markdown(certificate, md_path, json_path.name, json_sha)
    print(f"json={json_path}")
    print(f"json_sha256={json_sha}")
    print(f"markdown={md_path}")
    print(f"all_checks_passed={certificate['all_checks_passed']}")


if __name__ == "__main__":
    main()
