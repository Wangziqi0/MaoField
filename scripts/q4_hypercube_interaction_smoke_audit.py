#!/usr/bin/env python3
"""Zero-GPU smoke audit for the q4 x token-position interaction field.

This script reads existing raw JSONL smoke artifacts only. It does not load
checkpoints, run inference, train, generate a full panel, or authorize a new
loss. Its strongest possible verdict is `smoke_conjecture_only`.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
DEFAULT_SCHEMA = REPO / "docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json"
DEFAULT_RAW_GLOB = (
    "/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw/"
    "smoke_seed*_generation*_token_panel.jsonl"
)
DEFAULT_OUTDIR = REPO / "docs/infra/math_turn_20260622"

REQUIRED_FIELDS = {
    "schema_id",
    "seed",
    "generation",
    "source_split",
    "audit_block_id",
    "token_pos",
    "slice_id",
    "token_logprob",
}
BLOCKED_CLAIMS = [
    "LOSO passed",
    "F3 positive",
    "mean-null vector field survives",
    "residual field observed",
    "hypercube residual observed",
    "glass box broken",
    "training authorized",
    "new loss authorized",
    "full panel approved",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def token_position_bin(token_pos: int) -> int:
    if token_pos < 1 or token_pos > 63:
        raise ValueError(f"token_pos out of range: {token_pos}")
    return min(3, (token_pos - 1) * 4 // 63)


def schema_weights(schema: dict[str, Any]) -> np.ndarray:
    cells = schema["hypercube"]["cells"]
    ordered = sorted(cells, key=lambda item: (int(item["slice_id"]), int(item["position_bin"])))
    weights = np.asarray([float(item["weight"]) for item in ordered], dtype=float)
    weights = weights / float(np.sum(weights))
    return weights


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


def weighted_norm(x: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(float(np.sum(weights * x * x)))


def weighted_corr(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    denom = weighted_norm(x, weights) * weighted_norm(y, weights)
    if denom == 0.0:
        return float("nan")
    return float(np.sum(weights * x * y) / denom)


def parse_raw_file(path: Path, expected_schema_id: str, weights: np.ndarray) -> dict[str, Any]:
    counts = np.zeros((4, 4), dtype=int)
    sums = np.zeros((4, 4), dtype=float)
    schema_ids: set[str] = set()
    source_splits: set[str] = set()
    checkpoint_pairs: set[tuple[int, int]] = set()
    row_count = 0

    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            row = json.loads(line)
            missing = sorted(REQUIRED_FIELDS - set(row))
            if missing:
                raise ValueError(f"{path}:{line_no}: missing fields {missing}")
            schema_ids.add(str(row["schema_id"]))
            source_splits.add(str(row["source_split"]))
            checkpoint_pairs.add((int(row["seed"]), int(row["generation"])))
            q_id = int(row["slice_id"])
            b_id = token_position_bin(int(row["token_pos"]))
            token_logprob = float(row["token_logprob"])
            if not math.isfinite(token_logprob):
                raise ValueError(f"{path}:{line_no}: non-finite token_logprob")
            counts[q_id, b_id] += 1
            sums[q_id, b_id] += token_logprob
            row_count += 1

    if len(checkpoint_pairs) != 1:
        raise ValueError(f"{path}: expected one seed/generation pair, got {checkpoint_pairs}")
    if sorted(schema_ids) != [expected_schema_id]:
        raise ValueError(f"{path}: schema mismatch got {sorted(schema_ids)} expected {expected_schema_id}")
    if sorted(source_splits) != ["train"]:
        raise ValueError(f"{path}: source_split mismatch got {sorted(source_splits)}")
    if np.any(counts == 0):
        raise ValueError(f"{path}: empty q4 x token_pos4 cells")

    cell_means = (sums / counts).reshape(-1)
    weighted_mean = float(np.sum(weights * cell_means))
    mean_null = cell_means - weighted_mean
    additive_fit, interaction = weighted_project_additive(cell_means, weights)
    interaction_norm = weighted_norm(interaction, weights)
    mean_null_norm = weighted_norm(mean_null, weights)
    additive_fit_norm = weighted_norm(additive_fit - weighted_mean, weights)
    seed, generation = sorted(checkpoint_pairs)[0]
    return {
        "path": str(path),
        "filename": path.name,
        "raw_sha256": sha256_file(path),
        "seed": seed,
        "generation": generation,
        "n_rows": row_count,
        "occupancy_q_by_tokenpos4": counts.astype(int).tolist(),
        "weighted_mean_logprob": weighted_mean,
        "cell_mean_logprob_q_by_tokenpos4": (sums / counts).tolist(),
        "mean_null_norm": mean_null_norm,
        "additive_main_effect_norm": additive_fit_norm,
        "interaction_residual_norm": interaction_norm,
        "interaction_to_mean_null_ratio": (
            interaction_norm / mean_null_norm if mean_null_norm else float("nan")
        ),
        "_interaction_vector": interaction.tolist(),
    }


def interaction_summary(file_summaries: list[dict[str, Any]], weights: np.ndarray) -> dict[str, Any]:
    vectors = [np.asarray(item["_interaction_vector"], dtype=float) for item in file_summaries]
    pairwise = []
    for i, left in enumerate(file_summaries):
        for j in range(i + 1, len(file_summaries)):
            right = file_summaries[j]
            pairwise.append(
                {
                    "left": left["filename"],
                    "right": right["filename"],
                    "weighted_interaction_correlation": weighted_corr(vectors[i], vectors[j], weights),
                }
            )
    matrix = np.vstack([vec * np.sqrt(weights) for vec in vectors])
    singular = np.linalg.svd(matrix, compute_uv=False)
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    centered_singular = np.linalg.svd(centered, compute_uv=False)
    unweighted_matrix = np.vstack(vectors)
    unweighted_singular = np.linalg.svd(unweighted_matrix, compute_uv=False)
    return {
        "pairwise_weighted_correlations": pairwise,
        "weighted_uncentered_singular_values": singular.tolist(),
        "weighted_uncentered_sigma2_over_sigma1": (
            float(singular[1] / singular[0]) if len(singular) > 1 and singular[0] else None
        ),
        "weighted_centered_singular_values": centered_singular.tolist(),
        "weighted_centered_sigma2_over_sigma1": (
            float(centered_singular[1] / centered_singular[0])
            if len(centered_singular) > 1 and centered_singular[0]
            else None
        ),
        "unweighted_uncentered_singular_values": unweighted_singular.tolist(),
        "unweighted_uncentered_sigma2_over_sigma1": (
            float(unweighted_singular[1] / unweighted_singular[0])
            if len(unweighted_singular) > 1 and unweighted_singular[0]
            else None
        ),
    }


def public_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if not key.startswith("_")}


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# MaoField q4 Hypercube Interaction Smoke Audit",
        "",
        f"- Final verdict: `{result['final_verdict']}`",
        f"- Schema: `{result['schema_path']}`",
        f"- Raw files: `{len(result['raw_files'])}`",
        "",
        "## Boundary",
        "",
        "This audit reads existing smoke raw JSONL rows only. It does not load",
        "checkpoints, run inference, train, generate a full panel, authorize a new",
        "loss, or establish a scientific result.",
        "",
        "## Interaction Object",
        "",
        "For each smoke checkpoint, this audit forms a 4 x 4 cell-mean logprob",
        "matrix over `Q_freq4 x B_tokenpos4`, then subtracts the weighted additive",
        "subspace spanned by a constant term, q4 frequency main effects, and",
        "token-position main effects. The residual is a smoke-only interaction",
        "field candidate.",
        "",
        "## Per-File Summary",
        "",
    ]
    for item in result["file_summaries"]:
        lines.extend(
            [
                f"### `{item['filename']}`",
                "",
                f"- Seed/generation: `{item['seed']}` / `{item['generation']}`",
                f"- Mean-null norm: `{item['mean_null_norm']:.12g}`",
                f"- Interaction residual norm: `{item['interaction_residual_norm']:.12g}`",
                f"- Interaction / mean-null ratio: `{item['interaction_to_mean_null_ratio']:.6f}`",
                "",
            ]
        )
    lines.extend(["## Cross-Smoke Shape", ""])
    for pair in result["interaction_summary"]["pairwise_weighted_correlations"]:
        lines.append(
            "- `{left}` vs `{right}`: `{corr:.6f}`".format(
                left=pair["left"],
                right=pair["right"],
                corr=pair["weighted_interaction_correlation"],
            )
        )
    lines.extend(
        [
            "",
            "- Weighted uncentered singular values: `"
            + json.dumps(result["interaction_summary"]["weighted_uncentered_singular_values"])
            + "`",
            "- Weighted uncentered sigma2/sigma1: `"
            + str(result["interaction_summary"]["weighted_uncentered_sigma2_over_sigma1"])
            + "`",
            "- Weighted row-centered sigma2/sigma1: `"
            + str(result["interaction_summary"]["weighted_centered_sigma2_over_sigma1"])
            + "`",
            "- Unweighted uncentered sigma2/sigma1: `"
            + str(result["interaction_summary"]["unweighted_uncentered_sigma2_over_sigma1"])
            + "`",
            "",
            "## Verdict",
            "",
            "The interaction pattern is reproducible as a small smoke-derived",
            "calculation, but this is not a full panel and cannot support a",
            "scientific or philosophical claim. The low uncentered sigma2/sigma1",
            "also warns that the three-smoke pattern is close to one dominant shape.",
            "",
            "Missing controls before promotion: random equal-size token-position",
            "partition controls, within-q token-position shuffle controls, bad-axis",
            "controls, cell variance/noise modeling, held-out seed tests, and",
            "generation-block leave-out tests.",
            "",
            "## Blocked Claims",
            "",
        ]
    )
    for claim in result["blocked_claims"]:
        lines.append(f"- `{claim}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--raw-glob", default=DEFAULT_RAW_GLOB)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--output-prefix", default="Q4_HYPERCUBE_INTERACTION_SMOKE_AUDIT_20260623")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schema = load_json(args.schema)
    weights = schema_weights(schema)
    expected_schema_id = schema["hypercube"]["axes"][0]["source_schema_id"]
    raw_files = [Path(path) for path in sorted(glob.glob(args.raw_glob))]
    if not raw_files:
        raise SystemExit(f"no raw files matched {args.raw_glob}")
    summaries_with_vectors = [
        parse_raw_file(path, expected_schema_id=expected_schema_id, weights=weights)
        for path in raw_files
    ]
    summary = interaction_summary(summaries_with_vectors, weights)
    file_summaries = [public_summary(item) for item in summaries_with_vectors]
    result = {
        "artifact_kind": "maofield_q4_hypercube_interaction_smoke_audit",
        "artifact_version": "2026-06-23.d623.interaction_smoke.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "schema_path": str(args.schema),
        "schema_sha256": sha256_file(args.schema),
        "schema_id": schema["hypercube"]["schema_id"],
        "raw_glob": args.raw_glob,
        "raw_files": [str(path) for path in raw_files],
        "weight_source": "hypercube_schema_q4_tokenpos4_20260623.json source-only cell weights",
        "additive_nuisance_space": [
            "constant cell mean",
            "q4 frequency main effects",
            "token-position main effects",
        ],
        "file_summaries": file_summaries,
        "interaction_summary": summary,
        "final_verdict": "smoke_conjecture_only",
        "strongest_allowed_statement": (
            "Existing smoke raw rows reproduce a small interaction-field calculation, "
            "but this is not a full-panel result and is only eligible as a conjectural "
            "math direction / future audit candidate."
        ),
        "blocked_claims": BLOCKED_CLAIMS,
        "missing_controls_before_promotion": [
            "random equal-size token-position partition controls",
            "within-q token-position shuffle controls",
            "bad-axis controls beyond existing sparse audit_block_id rejection",
            "cell variance/noise model",
            "held-out seed tests",
            "generation-block leave-out tests",
            "PI-approved 16-cell full-panel aggregate",
        ],
    }
    json_path = args.outdir / f"{args.output_prefix}.json"
    md_path = args.outdir / f"{args.output_prefix}.md"
    write_json(json_path, result)
    write_markdown(result, md_path)
    print(json.dumps({"final_verdict": result["final_verdict"], "json": str(json_path), "md": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
