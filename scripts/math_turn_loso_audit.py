#!/usr/bin/env python3
"""Zero-GPU audit gate for MaoField's math-turn candidate.

This script consumes existing high-order aggregate JSON only. It does not
load checkpoints, create new bins, or claim that the proposed mean-null vector
field has been validated. Its job is to decide whether the current aggregate
F1/F3 artifact is enough to justify moving beyond the negative synthesis.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


METRICS = ["F1_var", "F1_tail", "F3_slice_gap"]
DEFAULT_INPUT = (
    "experiments/exp020_metric_stress_test/"
    "highorder_ppl_20260618/highorder_result.json"
)
DEFAULT_OUTDIR = "docs/infra/math_turn_20260622"


def design_matrix(mean_lp: np.ndarray, gen: np.ndarray, include_gen: bool) -> np.ndarray:
    cols = [np.ones_like(mean_lp)]
    for degree in range(1, 6):
        cols.append(mean_lp**degree)
    if include_gen:
        cols.append(gen)
        cols.append(gen**2)
    return np.column_stack(cols)


def fit_predict(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray) -> np.ndarray:
    coef, *_ = np.linalg.lstsq(x_train, y_train, rcond=None)
    return x_test @ coef


def cv_r2(
    y: np.ndarray,
    mean_lp: np.ndarray,
    gen: np.ndarray,
    seeds: np.ndarray,
    include_gen: bool,
) -> float:
    preds = np.empty_like(y, dtype=float)
    for seed in sorted(set(seeds.tolist())):
        test = seeds == seed
        train = ~test
        x_train = design_matrix(mean_lp[train], gen[train], include_gen)
        x_test = design_matrix(mean_lp[test], gen[test], include_gen)
        preds[test] = fit_predict(x_train, y[train], x_test)
    sse = float(np.sum((y - preds) ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    if sst == 0:
        return float("nan")
    return 1.0 - sse / sst


def permutation_pvalue(
    y: np.ndarray,
    mean_lp: np.ndarray,
    gen: np.ndarray,
    seeds: np.ndarray,
    observed_delta: float,
    n_perm: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    deltas = []
    for _ in range(n_perm):
        permuted_gen = rng.permutation(gen)
        base = cv_r2(y, mean_lp, permuted_gen, seeds, include_gen=False)
        plus = cv_r2(y, mean_lp, permuted_gen, seeds, include_gen=True)
        deltas.append(plus - base)
    arr = np.array(deltas, dtype=float)
    # One-sided: how often a shuffled generation label helps at least as much.
    p = (float(np.sum(arr >= observed_delta)) + 1.0) / (len(arr) + 1.0)
    return {
        "n_perm": int(n_perm),
        "mean": float(np.mean(arr)),
        "sd": float(np.std(arr, ddof=0)),
        "p_one_sided": float(p),
    }


def loso_audit(rows: list[dict[str, Any]], n_perm: int, seed: int) -> dict[str, Any]:
    mean_lp = np.array([r["mean_lp"] for r in rows], dtype=float)
    gen = np.array([r["gen"] for r in rows], dtype=float)
    seeds = np.array([r["seed"] for r in rows], dtype=float)
    rng = np.random.default_rng(seed)

    out: dict[str, Any] = {}
    for metric in METRICS:
        y = np.array([r[metric] for r in rows], dtype=float)
        base = cv_r2(y, mean_lp, gen, seeds, include_gen=False)
        plus = cv_r2(y, mean_lp, gen, seeds, include_gen=True)
        delta = plus - base
        out[metric] = {
            "model_a": "poly5(mean_lp)",
            "model_b": "poly5(mean_lp)+gen+gen^2",
            "cv_r2_model_a": float(base),
            "cv_r2_model_b": float(plus),
            "delta_r2": float(delta),
            "permutation_null": permutation_pvalue(
                y, mean_lp, gen, seeds, delta, n_perm, rng
            ),
            "passes_weak_loso_delta_gate": bool(delta >= 0.02),
        }
    return out


def matched_mean_audit(rows: list[dict[str, Any]], tolerances: list[float]) -> dict[str, Any]:
    mean_lp = np.array([r["mean_lp"] for r in rows], dtype=float)
    gen = np.array([r["gen"] for r in rows], dtype=float)
    out: dict[str, Any] = {}

    for metric in METRICS:
        y = np.array([r[metric] for r in rows], dtype=float)
        metric_out: dict[str, Any] = {}
        for tol in tolerances:
            signs = []
            slopes = []
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    d_mean = mean_lp[i] - mean_lp[j]
                    d_gen = gen[i] - gen[j]
                    if abs(d_mean) >= tol or d_gen == 0:
                        continue
                    d_y = y[i] - y[j]
                    if d_y == 0:
                        continue
                    signs.append(1.0 if math.copysign(1.0, d_y) == math.copysign(1.0, d_gen) else 0.0)
                    slopes.append(float(d_y / d_gen))
            n = len(signs)
            if n:
                frac = float(np.mean(signs))
                z = float((frac - 0.5) / math.sqrt(0.25 / n))
                mean_slope = float(np.mean(slopes))
                stable = bool(max(frac, 1.0 - frac) >= 0.70 and abs(z) >= 2.58)
            else:
                frac = float("nan")
                z = float("nan")
                mean_slope = float("nan")
                stable = False
            metric_out[str(tol)] = {
                "n_pairs": int(n),
                "frac_same_sign_as_delta_gen": frac,
                "z_vs_half": z,
                "mean_slope_per_delta_gen": mean_slope,
                "passes_stability_gate": stable,
            }
        out[metric] = metric_out
    return out


def rank_residual_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    # The existing artifact only has rare/freq aggregate slices, so this is a
    # diagnostic placeholder rather than the proposed J>=4 mean-null field.
    rare = np.array([r["F3_slice_rare"] for r in rows], dtype=float)
    freq = np.array([r["F3_slice_freq"] for r in rows], dtype=float)
    k = np.column_stack([rare, freq])
    weights = np.array([0.5, 0.5], dtype=float)
    mean_mode = k @ weights
    u = k - mean_mode[:, None]
    centered = u - np.mean(u, axis=0, keepdims=True)
    singular = np.linalg.svd(centered, compute_uv=False)
    if len(singular) < 2 or singular[0] == 0:
        ratio = 0.0
    else:
        ratio = float(singular[1] / singular[0])
    return {
        "available_slices": ["F3_slice_rare", "F3_slice_freq"],
        "status": "diagnostic_only_two_slice_aggregate",
        "singular_values": [float(x) for x in singular],
        "sigma2_over_sigma1": ratio,
        "passes_rank_gate": False,
        "reason": (
            "The current highorder_result.json has only rare/freq aggregate "
            "slice means. This cannot certify the proposed fixed J>=4 "
            "mean-null vector field."
        ),
    }


def summarize_verdict(loso: dict[str, Any], matched: dict[str, Any], rank: dict[str, Any]) -> dict[str, Any]:
    f3_loso = loso["F3_slice_gap"]["passes_weak_loso_delta_gate"]
    f3_matched = all(
        item["passes_stability_gate"]
        for item in matched["F3_slice_gap"].values()
    )
    rank_pass = bool(rank["passes_rank_gate"])

    if f3_loso and f3_matched and rank_pass:
        verdict = "eligible_for_next_design_review_only"
    elif not f3_loso:
        verdict = "killed"
    else:
        verdict = "insufficient_artifact"

    return {
        "verdict": verdict,
        "allowed_claim": (
            "Current aggregate high-order artifact supports at most a weak "
            "F3 lead. It does not authorize training a new vector-field loss."
        ),
        "blocked_claims": [
            "LOSO passed as primary artifact",
            "mean-null vector field validated as a primary artifact",
            "glass box broken",
            "F3 is a positive finding",
        ],
        "gate_summary": {
            "f3_loso_delta_gate": bool(f3_loso),
            "f3_matched_mean_all_tolerances": bool(f3_matched),
            "rank_residual_gate": bool(rank_pass),
        },
        "next_step": (
            "If PI approves, build a raw-logprob/checkpoint mode with fixed "
            "pre-registered slices and write a new primary JSON before any "
            "training implementation."
        ),
    }


def write_markdown(result: dict[str, Any], path: Path) -> None:
    verdict = result["final_verdict"]
    loso = result["loso"]
    matched = result["matched_mean"]
    rank = result["rank_residual"]

    lines = [
        "# MaoField Math-Turn Zero-GPU Audit Verdict",
        "",
        f"- Generated: `{result['generated_at_note']}`",
        f"- Input: `{result['input']}`",
        f"- Verdict: **{verdict['verdict']}**",
        "",
        "## Boundary",
        "",
        "This audit consumes the existing aggregate `highorder_result.json` only.",
        "It does not create new bins, load checkpoints, or prove the proposed",
        "mean-null vector KL field.",
        "",
        "## LOSO Delta",
        "",
        "| metric | CV-R2 poly5(mean_lp) | CV-R2 + gen | delta | perm p | weak gate |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for metric in METRICS:
        item = loso[metric]
        lines.append(
            "| {metric} | {a:.4f} | {b:.4f} | {d:+.4f} | {p:.4f} | {gate} |".format(
                metric=metric,
                a=item["cv_r2_model_a"],
                b=item["cv_r2_model_b"],
                d=item["delta_r2"],
                p=item["permutation_null"]["p_one_sided"],
                gate="pass" if item["passes_weak_loso_delta_gate"] else "fail",
            )
        )

    lines.extend([
        "",
        "## Matched-Mean Gate",
        "",
        "| metric | tol | pairs | frac sign(delta F)=sign(delta gen) | z | stable gate |",
        "|---|---:|---:|---:|---:|---|",
    ])
    for metric in METRICS:
        for tol, item in matched[metric].items():
            lines.append(
                "| {metric} | {tol} | {n} | {frac:.3f} | {z:+.2f} | {gate} |".format(
                    metric=metric,
                    tol=tol,
                    n=item["n_pairs"],
                    frac=item["frac_same_sign_as_delta_gen"],
                    z=item["z_vs_half"],
                    gate="pass" if item["passes_stability_gate"] else "fail",
                )
            )

    lines.extend([
        "",
        "## Rank/Residual Gate",
        "",
        f"- Status: `{rank['status']}`",
        f"- Available slices: `{', '.join(rank['available_slices'])}`",
        f"- sigma2/sigma1: `{rank['sigma2_over_sigma1']:.6g}`",
        f"- Gate: `{'pass' if rank['passes_rank_gate'] else 'fail'}`",
        f"- Reason: {rank['reason']}",
        "",
        "## Final",
        "",
        f"- Allowed claim: {verdict['allowed_claim']}",
        f"- Next step: {verdict['next_step']}",
        "",
        "Blocked claims:",
    ])
    for claim in verdict["blocked_claims"]:
        lines.append(f"- {claim}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--outdir", default=DEFAULT_OUTDIR)
    parser.add_argument("--n-perm", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260622)
    args = parser.parse_args()

    root = Path.cwd()
    input_path = (root / args.input).resolve()
    outdir = (root / args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    rows = data["rows"]
    loso = loso_audit(rows, args.n_perm, args.seed)
    matched = matched_mean_audit(rows, [0.02, 0.04])
    rank = rank_residual_audit(rows)
    verdict = summarize_verdict(loso, matched, rank)

    result = {
        "generated_at_note": "2026-06-22 node36; rerun script for exact wall time",
        "input": str(input_path),
        "n_rows": len(rows),
        "seeds": sorted({r["seed"] for r in rows}),
        "gens": sorted({r["gen"] for r in rows}),
        "loso": loso,
        "matched_mean": matched,
        "rank_residual": rank,
        "final_verdict": verdict,
    }

    json_path = outdir / "math_turn_loso_audit_result_20260622.json"
    md_path = outdir / "MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(result, md_path)

    print(json.dumps(verdict, indent=2, ensure_ascii=False))
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
