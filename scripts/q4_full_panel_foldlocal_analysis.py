#!/usr/bin/env python3
"""Fold-local q4 analysis gate for a future MaoField full panel.

This script consumes a q4 full-panel aggregate only. It does not read old
rare/freq aggregate rows, load checkpoints, train, call backward, or authorize a
new loss. Its strongest possible verdict is `eligible_for_next_design_review_only`.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
EXPECTED_SCHEMA_ID = "freq_q4_audit_targets_20260622"
EXPECTED_SEEDS = [1, 2, 3, 4, 42]
EXPECTED_GENERATIONS = list(range(10))
EXPECTED_ROW_COUNT = len(EXPECTED_SEEDS) * len(EXPECTED_GENERATIONS)
TOLERANCES = [0.02, 0.04]
VERDICTS = {
    "invalid_artifact",
    "killed",
    "insufficient_artifact",
    "eligible_for_next_design_review_only",
}
DEFAULT_INPUT = (
    REPO
    / "experiments/exp020_metric_stress_test/panel_primary_20260622/"
    "q4_full_panel_20260623_aggregate.json"
)
DEFAULT_OUTDIR = REPO / "docs/infra/math_turn_20260622"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_float(value: Any) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"non-finite value: {value!r}")
    return out


def design_matrix(d_values: np.ndarray, generations: np.ndarray, include_generation: bool) -> np.ndarray:
    cols = [np.ones_like(d_values)]
    for degree in range(1, 6):
        cols.append(d_values**degree)
    if include_generation:
        cols.append(generations)
        cols.append(generations**2)
    return np.column_stack(cols)


def fit_predict(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray) -> np.ndarray:
    coef, *_ = np.linalg.lstsq(x_train, y_train, rcond=None)
    return x_test @ coef


def cv_predictions(
    y: np.ndarray,
    d_values: np.ndarray,
    generations: np.ndarray,
    seeds: np.ndarray,
    include_generation: bool,
) -> np.ndarray:
    preds = np.empty_like(y, dtype=float)
    for seed in EXPECTED_SEEDS:
        test = seeds == seed
        train = ~test
        x_train = design_matrix(d_values[train], generations[train], include_generation)
        x_test = design_matrix(d_values[test], generations[test], include_generation)
        preds[test] = fit_predict(x_train, y[train], x_test)
    return preds


def cv_r2(y: np.ndarray, preds: np.ndarray) -> float:
    sse = float(np.sum((y - preds) ** 2))
    sst = float(np.sum((y - np.mean(y)) ** 2))
    if sst == 0:
        return float("nan")
    return 1.0 - sse / sst


def one_sided_permutation_pvalue(
    y: np.ndarray,
    d_values: np.ndarray,
    generations: np.ndarray,
    seeds: np.ndarray,
    observed_delta: float,
    n_perm: int,
    rng: np.random.Generator,
) -> dict[str, Any]:
    if n_perm <= 0:
        return {"n_perm": 0, "p_one_sided": None, "status": "skipped"}
    deltas = []
    for _ in range(n_perm):
        permuted = rng.permutation(generations)
        base = cv_r2(y, cv_predictions(y, d_values, permuted, seeds, False))
        plus = cv_r2(y, cv_predictions(y, d_values, permuted, seeds, True))
        deltas.append(plus - base)
    arr = np.asarray(deltas, dtype=float)
    p = (float(np.sum(arr >= observed_delta)) + 1.0) / (len(arr) + 1.0)
    return {
        "n_perm": int(n_perm),
        "mean_delta": float(np.mean(arr)),
        "sd_delta": float(np.std(arr)),
        "p_one_sided": float(p),
        "status": "computed",
    }


def normalize_rows(data: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not isinstance(data, dict) or "rows" not in data:
        return [], {
            "status": "invalid_artifact",
            "reason": "input must be a dict with a rows list from q4 full-panel aggregate",
        }
    rows = data["rows"]
    if not isinstance(rows, list):
        return [], {"status": "invalid_artifact", "reason": "rows must be a list"}
    if rows and "F3_slice_gap" in rows[0] and "u_values" not in rows[0]:
        return [], {
            "status": "invalid_artifact",
            "reason": "old rare/freq aggregate rows are not accepted as q4 full-panel input",
        }

    norm = []
    errors = []
    for idx, row in enumerate(rows):
        try:
            slice_rows = row["slice_rows"]
            u_values = [safe_float(x) for x in row["u_values"]]
            if len(u_values) != 4 or len(slice_rows) != 4:
                raise ValueError("q4 rows must have exactly four slices")
            weights = [safe_float(item["weight"]) for item in slice_rows]
            k_values = [safe_float(item["mean_logprob"]) for item in slice_rows]
            norm.append(
                {
                    "seed": int(row["seed"]),
                    "generation": int(row["generation"]),
                    "schema_id": row["schema_id"],
                    "D": safe_float(row["mean_mode_D"]),
                    "P": safe_float(row["primary_projection_P"]),
                    "u": u_values,
                    "k": k_values,
                    "weights": weights,
                    "projection_weights_v": [
                        safe_float(x) for x in row["projection_weights_v"]
                    ],
                }
            )
        except Exception as exc:
            errors.append({"row_index": idx, "error": str(exc)})
    if errors:
        return [], {"status": "invalid_artifact", "row_errors": errors[:10]}
    return norm, {"status": "parsed"}


def validate_full_panel(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != EXPECTED_ROW_COUNT:
        return {
            "status": "invalid_artifact",
            "reason": f"expected {EXPECTED_ROW_COUNT} q4 rows, got {len(rows)}",
        }
    got_pairs = {(row["seed"], row["generation"]) for row in rows}
    expected_pairs = {(seed, gen) for seed in EXPECTED_SEEDS for gen in EXPECTED_GENERATIONS}
    missing = sorted(expected_pairs - got_pairs)
    extra = sorted(got_pairs - expected_pairs)
    schema_ids = sorted({row["schema_id"] for row in rows})
    if missing or extra:
        return {
            "status": "invalid_artifact",
            "missing_pairs": missing,
            "extra_pairs": extra,
        }
    if schema_ids != [EXPECTED_SCHEMA_ID]:
        return {
            "status": "invalid_artifact",
            "reason": "schema_id mismatch",
            "schema_ids": schema_ids,
            "expected_schema_id": EXPECTED_SCHEMA_ID,
        }
    return {"status": "pass", "row_count": len(rows)}


def arrays(rows: list[dict[str, Any]]) -> dict[str, np.ndarray]:
    ordered = sorted(rows, key=lambda row: (row["seed"], row["generation"]))
    return {
        "seeds": np.asarray([row["seed"] for row in ordered], dtype=int),
        "generations": np.asarray([row["generation"] for row in ordered], dtype=float),
        "D": np.asarray([row["D"] for row in ordered], dtype=float),
        "P": np.asarray([row["P"] for row in ordered], dtype=float),
        "U": np.asarray([row["u"] for row in ordered], dtype=float),
        "weights": np.asarray(ordered[0]["weights"], dtype=float),
        "v": np.asarray(ordered[0]["projection_weights_v"], dtype=float),
    }


def loso_gate(arr: dict[str, np.ndarray], n_perm: int, rng: np.random.Generator) -> dict[str, Any]:
    y = arr["P"]
    base_preds = cv_predictions(y, arr["D"], arr["generations"], arr["seeds"], False)
    plus_preds = cv_predictions(y, arr["D"], arr["generations"], arr["seeds"], True)
    base = cv_r2(y, base_preds)
    plus = cv_r2(y, plus_preds)
    delta = plus - base
    return {
        "target": "primary_projection_P",
        "model_a": "poly5(D)",
        "model_b": "poly5(D)+generation+generation^2",
        "cv_r2_model_a": float(base),
        "cv_r2_model_b": float(plus),
        "delta_r2": float(delta),
        "weak_delta_threshold": 0.02,
        "permutation_p_one_sided_threshold": 0.10,
        "permutation_null": one_sided_permutation_pvalue(
            y, arr["D"], arr["generations"], arr["seeds"], delta, n_perm, rng
        ),
        "passes_weak_loso_delta_gate": bool(delta >= 0.02),
    }


def fold_local_residuals(arr: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    targets = np.column_stack([arr["P"], arr["U"]])
    residuals = np.empty_like(targets, dtype=float)
    for seed in EXPECTED_SEEDS:
        test = arr["seeds"] == seed
        train = ~test
        x_train = design_matrix(arr["D"][train], arr["generations"][train], True)
        x_test = design_matrix(arr["D"][test], arr["generations"][test], True)
        for col in range(targets.shape[1]):
            residuals[test, col] = targets[test, col] - fit_predict(
                x_train, targets[train, col], x_test
            )
    return residuals[:, 0], residuals[:, 1:]


def corr(a: np.ndarray, b: np.ndarray) -> float | None:
    if np.std(a) == 0 or np.std(b) == 0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def nuisance_gate(arr: dict[str, np.ndarray], residual_p: np.ndarray, residual_u: np.ndarray) -> dict[str, Any]:
    covariates = {
        "D": arr["D"],
        "generation": arr["generations"],
        "generation2": arr["generations"] ** 2,
    }
    raw_corrs: dict[str, Any] = {"P": {}, "u": []}
    residual_corrs: dict[str, Any] = {"P": {}, "u": []}
    for name, values in covariates.items():
        raw_corrs["P"][name] = corr(arr["P"], values)
        residual_corrs["P"][name] = corr(residual_p, values)
    for idx in range(4):
        raw_item = {}
        residual_item = {}
        for name, values in covariates.items():
            raw_item[name] = corr(arr["U"][:, idx], values)
            residual_item[name] = corr(residual_u[:, idx], values)
        raw_corrs["u"].append(raw_item)
        residual_corrs["u"].append(residual_item)
    return {
        "method": "fold-local least-squares residualization on held-out seed",
        "nuisance_basis": ["poly5(D)", "generation", "generation^2"],
        "raw_correlations": raw_corrs,
        "residual_correlations": residual_corrs,
        "passes_fold_locality_gate": True,
    }


def pair_signs(values: np.ndarray, d_values: np.ndarray, generations: np.ndarray, tol: float) -> list[float]:
    signs = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if abs(float(d_values[i] - d_values[j])) >= tol:
                continue
            dg = float(generations[i] - generations[j])
            dy = float(values[i] - values[j])
            if dg == 0 or dy == 0:
                continue
            signs.append(math.copysign(1.0, dy / dg))
    return signs


def matched_mean_gate(arr: dict[str, np.ndarray]) -> dict[str, Any]:
    out = {}
    for tol in TOLERANCES:
        successes = []
        fold_details = []
        insufficient = False
        for seed in EXPECTED_SEEDS:
            train = arr["seeds"] != seed
            test = arr["seeds"] == seed
            train_signs = pair_signs(arr["P"][train], arr["D"][train], arr["generations"][train], tol)
            test_signs = pair_signs(arr["P"][test], arr["D"][test], arr["generations"][test], tol)
            if not train_signs or not test_signs:
                insufficient = True
                direction = None
                fold_successes: list[float] = []
            else:
                direction = 1.0 if float(np.mean(train_signs)) >= 0 else -1.0
                fold_successes = [1.0 if sign == direction else 0.0 for sign in test_signs]
                successes.extend(fold_successes)
            fold_details.append(
                {
                    "held_out_seed": int(seed),
                    "train_pairs": len(train_signs),
                    "test_pairs": len(test_signs),
                    "fold_local_direction": direction,
                    "test_stable_fraction": (
                        float(np.mean(fold_successes)) if fold_successes else None
                    ),
                }
            )
        n = len(successes)
        if n:
            frac = float(np.mean(successes))
            z = float((frac - 0.5) / math.sqrt(0.25 / n))
            passed = bool(frac >= 0.70 and abs(z) >= 2.58 and not insufficient)
        else:
            frac = None
            z = None
            passed = False
        out[str(tol)] = {
            "n_heldout_pairs": n,
            "stable_fraction_threshold": 0.70,
            "z_threshold": 2.58,
            "stable_fraction": frac,
            "z_vs_half": z,
            "insufficient_pairs": insufficient,
            "passes_stability_gate": passed,
            "folds": fold_details,
        }
    return out


def centered(matrix: np.ndarray) -> np.ndarray:
    return matrix - np.mean(matrix, axis=0, keepdims=True)


def singular_summary(matrix: np.ndarray) -> dict[str, Any]:
    vals = np.linalg.svd(centered(matrix), compute_uv=False)
    ratio = 0.0 if len(vals) < 2 or vals[0] == 0 else float(vals[1] / vals[0])
    amplitude = float(np.sqrt(np.mean(centered(matrix) ** 2)))
    return {
        "singular_values": [float(x) for x in vals],
        "sigma2_over_sigma1": ratio,
        "rms_centered_amplitude": amplitude,
    }


def bootstrap_amplitude_p90(
    matrix: np.ndarray,
    seeds: np.ndarray,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> float:
    unique = np.asarray(EXPECTED_SEEDS)
    amps = []
    for _ in range(n_bootstrap):
        chosen = rng.choice(unique, size=len(unique), replace=True)
        idx = np.concatenate([np.where(seeds == seed)[0] for seed in chosen])
        amps.append(singular_summary(matrix[idx])["rms_centered_amplitude"])
    return float(np.percentile(amps, 90))


def rank_noise_gate(
    arr: dict[str, np.ndarray],
    residual_u: np.ndarray,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> dict[str, Any]:
    actual = singular_summary(residual_u)
    rank1_u = arr["P"][:, None] * arr["v"][None, :]
    mean_only_u = np.zeros_like(residual_u)
    rank1 = singular_summary(rank1_u)
    mean_only = singular_summary(mean_only_u)
    seed_p90 = bootstrap_amplitude_p90(residual_u, arr["seeds"], n_bootstrap, rng)
    rank1_p90 = bootstrap_amplitude_p90(rank1_u, arr["seeds"], n_bootstrap, rng)
    floor = 2.0 * max(seed_p90, rank1_p90)
    rank_pass = bool(actual["sigma2_over_sigma1"] >= 0.25)
    amplitude_pass = bool(actual["rms_centered_amplitude"] > floor)
    rank1_control_passes = bool(rank1["sigma2_over_sigma1"] >= 0.25)
    mean_only_control_passes = bool(mean_only["rms_centered_amplitude"] > floor)
    return {
        "actual_residual_u": actual,
        "rank1_control": rank1,
        "mean_only_control": mean_only,
        "sigma2_over_sigma1_min": 0.25,
        "noise_floor_seed_bootstrap_p90": seed_p90,
        "noise_floor_rank1_control_p90": rank1_p90,
        "residual_amplitude_floor": floor,
        "passes_rank_gate": rank_pass,
        "passes_amplitude_gate": amplitude_pass,
        "rank1_control_passes_rank_gate": rank1_control_passes,
        "mean_only_control_passes_amplitude_gate": mean_only_control_passes,
        "passes_rank_noise_gate": bool(
            rank_pass
            and amplitude_pass
            and not rank1_control_passes
            and not mean_only_control_passes
        ),
    }


def multiplicity_gate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    schema_ids = sorted({row["schema_id"] for row in rows})
    passed = schema_ids == [EXPECTED_SCHEMA_ID]
    return {
        "allowed_primary_schema": EXPECTED_SCHEMA_ID,
        "observed_schema_ids": schema_ids,
        "q8_allowed_as_primary": False,
        "old_top_bottom_masks_allowed_as_primary": False,
        "passes_multiplicity_gate": passed,
    }


def verdict_from_gates(
    validation: dict[str, Any],
    loso: dict[str, Any],
    matched: dict[str, Any],
    rank_noise: dict[str, Any],
    multiplicity: dict[str, Any],
) -> str:
    if validation["status"] != "pass" or not multiplicity["passes_multiplicity_gate"]:
        return "invalid_artifact"
    if any(item["insufficient_pairs"] for item in matched.values()):
        return "insufficient_artifact"
    if not loso["passes_weak_loso_delta_gate"]:
        return "killed"
    if not all(item["passes_stability_gate"] for item in matched.values()):
        return "killed"
    if not rank_noise["passes_rank_noise_gate"]:
        return "killed"
    return "eligible_for_next_design_review_only"


def write_markdown(result: dict[str, Any], path: Path) -> None:
    verdict = result["final_verdict"]
    lines = [
        "# MaoField q4 Full-Panel Fold-Local Analysis",
        "",
        f"- Final verdict: `{verdict}`",
        f"- Input: `{result['input']}`",
        f"- Row count: `{result['validation'].get('row_count')}`",
        "",
        "## Boundary",
        "",
        "This script analyzes a q4 full-panel aggregate only. It does not load",
        "checkpoints, train, call backward, generate text, or authorize a new loss.",
        "",
    ]
    if verdict == "invalid_artifact" and "loso" not in result:
        lines.extend(
            [
                "## Artifact Rejection",
                "",
                "The input did not parse as a valid q4 full-panel aggregate.",
                "",
                "```json",
                json.dumps(result["validation"], indent=2, ensure_ascii=False),
                "```",
                "",
                "## Claim Boundary",
                "",
                "No scientific claim is licensed by an invalid artifact.",
            ]
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    lines.extend(
        [
        "## Gate Summary",
        "",
        f"- LOSO weak delta gate: `{result['loso']['passes_weak_loso_delta_gate']}`",
        "- Matched-mean gates: `"
        + json.dumps(
            {key: item["passes_stability_gate"] for key, item in result["matched_mean"].items()},
            sort_keys=True,
        )
        + "`",
        f"- Rank/noise gate: `{result['rank_noise']['passes_rank_noise_gate']}`",
        f"- Multiplicity gate: `{result['multiplicity']['passes_multiplicity_gate']}`",
        "",
        "## Claim Boundary",
        "",
        "Even `eligible_for_next_design_review_only` does not authorize training,",
        "a new loss, F3-positive wording, mean-null-survival wording, or glass-box",
        "wording.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def synthetic_full_panel() -> dict[str, Any]:
    weights = np.asarray([1374, 2581, 2020, 2089], dtype=float)
    weights = weights / np.sum(weights)
    v_raw = np.asarray([-1.5, -0.5, 0.5, 1.5], dtype=float)
    v = v_raw - float(np.sum(weights * v_raw))
    v = v / math.sqrt(float(np.sum(weights * v**2)))
    rows = []
    for seed_index, seed in enumerate(EXPECTED_SEEDS):
        for generation in EXPECTED_GENERATIONS:
            d_value = -3.4 + 0.04 * generation + 0.01 * seed_index
            nuisance = 0.15 * generation * v / 9.0
            residual = 0.05 * np.sin((generation + 1) * np.asarray([1.0, 2.0, 3.0, 4.0]))
            residual = residual - float(np.sum(weights * residual))
            u = nuisance + residual
            k = d_value + u
            p_value = float(np.sum(weights * v * u))
            rows.append(
                {
                    "schema_id": EXPECTED_SCHEMA_ID,
                    "seed": seed,
                    "generation": generation,
                    "mean_mode_D": float(d_value),
                    "primary_projection_P": p_value,
                    "projection_weights_v": [float(x) for x in v],
                    "u_values": [float(x) for x in u],
                    "slice_rows": [
                        {
                            "schema_id": EXPECTED_SCHEMA_ID,
                            "seed": seed,
                            "generation": generation,
                            "slice_id": idx,
                            "n_tokens": int(round(weight * 8064)),
                            "weight": float(weight),
                            "mean_logprob": float(k[idx]),
                        }
                        for idx, weight in enumerate(weights)
                    ],
                }
            )
    return {
        "artifact_kind": "synthetic_q4_full_panel_for_script_self_test",
        "schema_id": EXPECTED_SCHEMA_ID,
        "rows": rows,
    }


def run_analysis(data: Any, input_label: str, args: argparse.Namespace) -> dict[str, Any]:
    rows, parse = normalize_rows(data)
    if parse["status"] != "parsed":
        return {
            "input": input_label,
            "parse": parse,
            "validation": parse,
            "final_verdict": "invalid_artifact",
            "blocked_claims": blocked_claims(),
        }
    validation = validate_full_panel(rows)
    if validation["status"] != "pass":
        return {
            "input": input_label,
            "parse": parse,
            "validation": validation,
            "final_verdict": "invalid_artifact",
            "blocked_claims": blocked_claims(),
        }

    arr = arrays(rows)
    rng = np.random.default_rng(args.seed)
    loso = loso_gate(arr, args.n_perm, rng)
    residual_p, residual_u = fold_local_residuals(arr)
    nuisance = nuisance_gate(arr, residual_p, residual_u)
    matched = matched_mean_gate(arr)
    rank_noise = rank_noise_gate(arr, residual_u, args.n_bootstrap, rng)
    multiplicity = multiplicity_gate(rows)
    verdict = verdict_from_gates(validation, loso, matched, rank_noise, multiplicity)
    assert verdict in VERDICTS
    return {
        "input": input_label,
        "generated_at_note": "node36; rerun script for exact wall time",
        "parse": parse,
        "validation": validation,
        "loso": loso,
        "nuisance": nuisance,
        "matched_mean": matched,
        "rank_noise": rank_noise,
        "multiplicity": multiplicity,
        "final_verdict": verdict,
        "strongest_allowed_statement": (
            "The q4 fixed-train-block logprob panel is eligible for next design review only."
            if verdict == "eligible_for_next_design_review_only"
            else None
        ),
        "blocked_claims": blocked_claims(),
    }


def blocked_claims() -> list[str]:
    return [
        "LOSO passed",
        "F3 positive",
        "mean-null vector field survives",
        "glass box broken",
        "training authorized",
        "new loss authorized",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--output-prefix", default="q4_full_panel_foldlocal_analysis")
    parser.add_argument("--n-perm", type=int, default=200)
    parser.add_argument("--n-bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_test:
        data = synthetic_full_panel()
        input_label = "synthetic_full_panel_self_test"
    else:
        data = load_json(args.input)
        input_label = str(args.input)

    result = run_analysis(data, input_label, args)
    json_path = args.outdir / f"{args.output_prefix}.json"
    md_path = args.outdir / f"{args.output_prefix}.md"
    write_json(json_path, result)
    write_markdown(result, md_path)
    print(json.dumps({"final_verdict": result["final_verdict"], "json": str(json_path), "md": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
