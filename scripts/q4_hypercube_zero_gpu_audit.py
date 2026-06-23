#!/usr/bin/env python3
"""Zero-GPU feasibility audit for the q4 x token-position hypercube candidate.

This script reads existing raw JSONL smoke artifacts only. It does not load
checkpoints, run inference, train, call backward, generate a full panel, or
authorize a new loss. Its strongest possible verdict is `formal_prereg_only`.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
from collections import Counter, defaultdict
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
    "flat_token_index",
    "target_token_id",
    "target_count_audit_blocks",
    "slice_id",
    "token_logprob",
    "neg_logprob",
}
BLOCKED_CLAIMS = [
    "LOSO passed",
    "F3 positive",
    "mean-null vector field survives",
    "residual field observed",
    "glass box broken",
    "training authorized",
    "new loss authorized",
    "full panel approved",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def token_position_bin(token_pos: int) -> int:
    if token_pos < 1 or token_pos > 63:
        raise ValueError(f"token_pos out of range: {token_pos}")
    return min(3, (token_pos - 1) * 4 // 63)


def load_raw_rows(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = []
    errors = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            try:
                row = json.loads(line)
                missing = sorted(REQUIRED_FIELDS - set(row))
                if missing:
                    raise ValueError(f"missing required fields: {missing}")
                rows.append(row)
            except Exception as exc:
                errors.append({"line": line_no, "error": str(exc)})
                if len(errors) >= 10:
                    break
    return rows, errors


def weighted_rank(basis: np.ndarray, weights: np.ndarray, tol: float = 1e-10) -> int:
    scaled = basis * np.sqrt(weights[:, None])
    return int(np.linalg.matrix_rank(scaled, tol=tol))


def nuisance_dimensions(weights: np.ndarray) -> dict[str, Any]:
    q = 4
    b = 4
    n = q * b
    const = np.ones((n, 1), dtype=float)
    v_q_raw = np.asarray([-1.5, -0.5, 0.5, 1.5], dtype=float)
    q_weights = np.asarray(
        [sum(weights[q_id * b + b_id] for b_id in range(b)) for q_id in range(q)],
        dtype=float,
    )
    v_q = v_q_raw - float(np.sum(q_weights * v_q_raw))
    v_q = v_q / math.sqrt(float(np.sum(q_weights * v_q * v_q)))
    lifted_slope = np.asarray([v_q[idx // b] for idx in range(n)], dtype=float)[:, None]
    pos_effects = []
    for b_id in range(b - 1):
        vec = np.zeros(n, dtype=float)
        for idx in range(n):
            if idx % b == b_id:
                vec[idx] = 1.0
        vec = vec - float(np.sum(weights * vec))
        pos_effects.append(vec)
    mandatory_basis = np.column_stack([const, lifted_slope] + pos_effects)

    q_effects = []
    for q_id in range(q - 1):
        vec = np.zeros(n, dtype=float)
        for idx in range(n):
            if idx // b == q_id:
                vec[idx] = 1.0
        vec = vec - float(np.sum(weights * vec))
        q_effects.append(vec)
    strict_basis = np.column_stack([const] + q_effects + pos_effects)
    mandatory_rank = weighted_rank(mandatory_basis, weights)
    strict_rank = weighted_rank(strict_basis, weights)
    return {
        "ambient_dimension": n,
        "mandatory_nuisance_basis": [
            "constant cell mean mode",
            "locked q4 slope lifted across token-position bins",
            "centered pure token-position main effects",
        ],
        "mandatory_nuisance_rank": mandatory_rank,
        "mandatory_residual_dimension": n - mandatory_rank,
        "strict_additive_basis": [
            "constant cell mean mode",
            "centered q4 frequency main effects",
            "centered token-position main effects",
        ],
        "strict_additive_rank": strict_rank,
        "strict_additive_residual_dimension": n - strict_rank,
    }


def summarize_raw_file(path: Path, schema: dict[str, Any], min_cell_count: int) -> dict[str, Any]:
    rows, errors = load_raw_rows(path)
    if errors:
        return {"path": str(path), "status": "invalid_artifact", "row_errors": errors}
    if not rows:
        return {"path": str(path), "status": "invalid_artifact", "reason": "empty raw JSONL"}

    schema_ids = sorted({row["schema_id"] for row in rows})
    source_splits = sorted({row["source_split"] for row in rows})
    checkpoint_pairs = sorted({(int(row["seed"]), int(row["generation"])) for row in rows})
    if len(checkpoint_pairs) != 1:
        return {
            "path": str(path),
            "status": "invalid_artifact",
            "reason": "raw file must contain exactly one seed-generation pair",
            "checkpoint_pairs": checkpoint_pairs,
        }

    q4_pos_counts: Counter[tuple[int, int]] = Counter()
    q4_block_counts: Counter[tuple[int, int]] = Counter()
    cell_sums: defaultdict[tuple[int, int], float] = defaultdict(float)
    for row in rows:
        slice_id = int(row["slice_id"])
        pos_bin = token_position_bin(int(row["token_pos"]))
        block_id = int(row["audit_block_id"])
        token_logprob = float(row["token_logprob"])
        if not math.isfinite(token_logprob):
            return {"path": str(path), "status": "invalid_artifact", "reason": "non-finite logprob"}
        q4_pos_counts[(slice_id, pos_bin)] += 1
        q4_block_counts[(slice_id, block_id)] += 1
        cell_sums[(slice_id, pos_bin)] += token_logprob

    q = 4
    b = 4
    matrix = [[int(q4_pos_counts[(q_id, b_id)]) for b_id in range(b)] for q_id in range(q)]
    flat_counts = [matrix[q_id][b_id] for q_id in range(q) for b_id in range(b)]
    weights = np.asarray(flat_counts, dtype=float) / float(sum(flat_counts))
    cell_means = [
        cell_sums[(q_id, b_id)] / q4_pos_counts[(q_id, b_id)]
        for q_id in range(q)
        for b_id in range(b)
    ]
    block_counts = list(q4_block_counts.values())
    empty = [
        f"q{q_id}_pos{b_id}"
        for q_id in range(q)
        for b_id in range(b)
        if q4_pos_counts[(q_id, b_id)] == 0
    ]
    return {
        "path": str(path),
        "status": "parsed",
        "seed": checkpoint_pairs[0][0],
        "generation": checkpoint_pairs[0][1],
        "schema_ids": schema_ids,
        "expected_schema_id": schema["hypercube"]["axes"][0]["source_schema_id"],
        "schema_id_pass": schema_ids == [schema["hypercube"]["axes"][0]["source_schema_id"]],
        "source_splits": source_splits,
        "source_split_pass": source_splits == ["train"],
        "n_rows": len(rows),
        "q4_tokenpos4_occupancy": matrix,
        "q4_tokenpos4_empty_cells": empty,
        "q4_tokenpos4_min_cell_count": int(min(flat_counts)),
        "q4_tokenpos4_max_cell_count": int(max(flat_counts)),
        "q4_tokenpos4_sparse_cell_threshold": min_cell_count,
        "q4_tokenpos4_passes_occupancy_gate": bool(not empty and min(flat_counts) >= min_cell_count),
        "q4_audit_block128_min_cell_count": int(min(block_counts)) if block_counts else None,
        "q4_audit_block128_max_cell_count": int(max(block_counts)) if block_counts else None,
        "audit_block_id_as_primary_axis": "rejected_sparse_high_dimensional_axis",
        "cell_mean_logprob_summary": {
            "min": float(np.min(cell_means)),
            "median": float(np.median(cell_means)),
            "max": float(np.max(cell_means)),
        },
        "nuisance_dimensions": nuisance_dimensions(weights),
    }


def final_verdict(file_summaries: list[dict[str, Any]]) -> tuple[str, list[str]]:
    reasons = []
    if not file_summaries:
        return "invalid_artifact", ["no raw JSONL files matched input glob"]
    for item in file_summaries:
        if item["status"] != "parsed":
            reasons.append(f"{item['path']}: {item.get('reason', item['status'])}")
            continue
        for key in ("schema_id_pass", "source_split_pass", "q4_tokenpos4_passes_occupancy_gate"):
            if not item[key]:
                reasons.append(f"{item['path']}: failed {key}")
    if reasons:
        return "invalid_artifact", reasons
    return "formal_prereg_only", [
        "q4 x token_pos4 cells are non-empty in existing smoke raw rows",
        "this is not a full panel and does not support a scientific claim",
    ]


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# MaoField q4 Hypercube Zero-GPU Audit",
        "",
        f"- Final verdict: `{result['final_verdict']}`",
        f"- Schema: `{result['schema_path']}`",
        f"- Raw glob: `{result['raw_glob']}`",
        f"- Raw files: `{len(result['raw_files'])}`",
        "",
        "## Boundary",
        "",
        "This audit reads existing smoke raw JSONL rows only. It does not load",
        "checkpoints, run inference, train, generate a full panel, or authorize a",
        "new loss. Its strongest possible conclusion is formal preregistration",
        "feasibility.",
        "",
        "## Verdict Reasons",
        "",
    ]
    for reason in result["verdict_reasons"]:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            "## Occupancy",
            "",
        ]
    )
    for item in result["file_summaries"]:
        lines.extend(
            [
                f"### `{Path(item['path']).name}`",
                "",
                f"- Status: `{item['status']}`",
            ]
        )
        if item["status"] == "parsed":
            lines.extend(
                [
                    f"- Seed/generation: `{item['seed']}` / `{item['generation']}`",
                    f"- q4 x token_pos4 min cell count: `{item['q4_tokenpos4_min_cell_count']}`",
                    f"- q4 x token_pos4 max cell count: `{item['q4_tokenpos4_max_cell_count']}`",
                    f"- audit_block_id primary-axis decision: `{item['audit_block_id_as_primary_axis']}`",
                    "",
                    "```text",
                    json.dumps(item["q4_tokenpos4_occupancy"], ensure_ascii=False),
                    "```",
                ]
            )
    lines.extend(
        [
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
    parser.add_argument("--output-prefix", default="Q4_HYPERCUBE_ZERO_GPU_AUDIT_20260623")
    parser.add_argument("--min-cell-count", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schema = load_json(args.schema)
    raw_files = [Path(path) for path in sorted(glob.glob(args.raw_glob))]
    summaries = [
        summarize_raw_file(path, schema, args.min_cell_count)
        for path in raw_files
    ]
    verdict, reasons = final_verdict(summaries)
    result = {
        "artifact_kind": "maofield_q4_hypercube_zero_gpu_audit",
        "artifact_version": "2026-06-23.d623.zero_gpu_audit.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "schema_path": str(args.schema),
        "schema_id": schema["hypercube"]["schema_id"],
        "raw_glob": args.raw_glob,
        "raw_files": [str(path) for path in raw_files],
        "file_summaries": summaries,
        "final_verdict": verdict,
        "verdict_reasons": reasons,
        "strongest_allowed_statement": (
            "The q4 x token_pos4 hypercube is eligible only for formal "
            "preregistration review, not scientific interpretation."
        )
        if verdict == "formal_prereg_only"
        else None,
        "blocked_claims": BLOCKED_CLAIMS,
    }
    json_path = args.outdir / f"{args.output_prefix}.json"
    md_path = args.outdir / f"{args.output_prefix}.md"
    write_json(json_path, result)
    write_markdown(result, md_path)
    print(json.dumps({"final_verdict": verdict, "json": str(json_path), "md": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
