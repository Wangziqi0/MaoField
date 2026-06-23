#!/usr/bin/env python3
"""Build a zero-GPU q4 x token-position hypercube preregistration schema.

This script does not load checkpoints, run model inference, train, or create a
new loss. It preserves the locked q4 frequency axis and adds only one
outcome-independent candidate axis: coarse token position buckets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from transformers import AutoTokenizer


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
SRC = REPO / "experiments/exp018_cat/src"
sys.path.insert(0, str(SRC))

from data_pipeline import load_wikitext2, tokenize_and_block  # noqa: E402


DEFAULT_Q4_SCHEMA = (
    REPO
    / "docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json"
)
DEFAULT_OUT = REPO / "docs/infra/math_turn_20260622/hypercube_schema_q4_tokenpos4_20260623.json"
TOKEN_POS_BINS = 4


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def token_position_bin(token_pos: int, n_next_positions: int, n_bins: int = TOKEN_POS_BINS) -> int:
    if token_pos < 1 or token_pos > n_next_positions:
        raise ValueError(f"token_pos out of range: {token_pos}")
    return min(n_bins - 1, (token_pos - 1) * n_bins // n_next_positions)


def token_position_bins(n_next_positions: int, n_bins: int = TOKEN_POS_BINS) -> list[dict[str, Any]]:
    out = []
    for bin_id in range(n_bins):
        positions = [
            pos
            for pos in range(1, n_next_positions + 1)
            if token_position_bin(pos, n_next_positions, n_bins) == bin_id
        ]
        out.append(
            {
                "position_bin": bin_id,
                "token_pos_min": min(positions),
                "token_pos_max": max(positions),
                "n_positions_per_block": len(positions),
            }
        )
    return out


def build_source_arrays(q4_schema: dict[str, Any]) -> dict[str, Any]:
    source = q4_schema["source"]
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    raw = load_wikitext2(source["dataset_id"], source["dataset_config"])
    tokenizer = AutoTokenizer.from_pretrained(source["tokenizer_id"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    blocks = tokenize_and_block(
        raw[source["source_split"]],
        tokenizer,
        int(source["block_size"]),
    ).select(source["audit_block_indices"])

    input_ids = [list(row) for row in blocks["input_ids"]]
    target_ids = [int(token) for row in input_ids for token in row[1:]]
    target_counts = sorted((int(token), int(count)) for token, count in Counter(target_ids).items())
    count_map = dict(target_counts)
    target_frequencies = np.asarray([count_map[token] for token in target_ids], dtype=np.int64)

    hashes = {
        "input_ids_sha256": sha256_json(input_ids),
        "target_ids_sha256": sha256_json(target_ids),
        "target_counts_sha256": sha256_json(target_counts),
    }
    mismatches = {
        key: {"got": got, "expected": source[key]}
        for key, got in hashes.items()
        if got != source[key]
    }
    if mismatches:
        raise ValueError(f"source hash mismatch: {json.dumps(mismatches, indent=2)}")

    primary = q4_schema["primary_schema"]
    edges = np.asarray(primary["edges"], dtype=np.int64)
    slice_ids = np.searchsorted(edges, target_frequencies, side="right").astype(np.int64)
    bin_sizes = np.bincount(slice_ids, minlength=int(primary["q"])).astype(int).tolist()
    if bin_sizes != primary["bin_sizes"]:
        raise ValueError(f"q4 bin sizes mismatch: got {bin_sizes}, expected {primary['bin_sizes']}")

    token_positions = []
    for row in input_ids:
        for token_pos in range(1, len(row)):
            token_positions.append(token_pos)
    return {
        "input_ids": input_ids,
        "target_ids": target_ids,
        "target_frequencies": target_frequencies,
        "slice_ids": slice_ids,
        "token_positions": np.asarray(token_positions, dtype=np.int64),
        "hashes": hashes,
    }


def build_schema(q4_schema_path: Path) -> dict[str, Any]:
    q4_schema = load_json(q4_schema_path)
    source = q4_schema["source"]
    source_arrays = build_source_arrays(q4_schema)
    n_next_positions = int(source["block_size"]) - 1
    pos_bins = np.asarray(
        [
            token_position_bin(int(pos), n_next_positions, TOKEN_POS_BINS)
            for pos in source_arrays["token_positions"]
        ],
        dtype=np.int64,
    )

    q = int(q4_schema["primary_schema"]["q"])
    occupancy = np.zeros((q, TOKEN_POS_BINS), dtype=int)
    for slice_id, pos_bin in zip(source_arrays["slice_ids"], pos_bins):
        occupancy[int(slice_id), int(pos_bin)] += 1

    cells = []
    for slice_id in range(q):
        for pos_bin in range(TOKEN_POS_BINS):
            count = int(occupancy[slice_id, pos_bin])
            cells.append(
                {
                    "slice_id": slice_id,
                    "position_bin": pos_bin,
                    "cell_id": f"q{slice_id}_pos{pos_bin}",
                    "n_tokens": count,
                    "weight": count / int(source["n_next_token_positions"]),
                }
            )

    return {
        "artifact_kind": "maofield_q4_hypercube_schema",
        "artifact_version": "2026-06-23.d623.hypercube_schema.v1",
        "status": "formal_prereg_candidate_zero_gpu_only",
        "created_date": "2026-06-23",
        "created_by": "scripts/build_hypercube_schema_20260623.py",
        "no_checkpoint_loaded": True,
        "no_model_inference": True,
        "no_training": True,
        "no_new_loss": True,
        "strongest_allowed_verdict": "formal_prereg_only",
        "inherited_q4_schema_path": str(q4_schema_path.relative_to(REPO)),
        "inherited_q4_schema_sha256": sha256_file(q4_schema_path),
        "source": {
            **source,
            "input_ids_sha256": source_arrays["hashes"]["input_ids_sha256"],
            "target_ids_sha256": source_arrays["hashes"]["target_ids_sha256"],
            "target_counts_sha256": source_arrays["hashes"]["target_counts_sha256"],
        },
        "hypercube": {
            "schema_id": "q4_tokenpos4_hypercube_20260623",
            "role": "zero_gpu_prereg_feasibility_candidate",
            "cell_set": "Q_freq4 x B_tokenpos4",
            "axes": [
                {
                    "axis_id": "Q_freq4",
                    "source_field": "slice_id",
                    "source_schema_id": q4_schema["primary_schema"]["schema_id"],
                    "n_bins": q,
                    "role": "locked_existing_frequency_axis",
                },
                {
                    "axis_id": "B_tokenpos4",
                    "source_field": "token_pos",
                    "n_bins": TOKEN_POS_BINS,
                    "assignment_policy": (
                        "position_bin = min(3, (token_pos - 1) * 4 // 63), "
                        "where token_pos is the next-token position in a 64-token block"
                    ),
                    "role": "outcome_independent_candidate_secondary_axis",
                    "bins": token_position_bins(n_next_positions, TOKEN_POS_BINS),
                },
            ],
            "cells": cells,
            "occupancy": {
                "matrix_q_by_tokenpos4": occupancy.astype(int).tolist(),
                "n_cells": int(q * TOKEN_POS_BINS),
                "empty_cells": [
                    cell["cell_id"] for cell in cells if int(cell["n_tokens"]) == 0
                ],
                "min_cell_count": int(occupancy.min()),
                "max_cell_count": int(occupancy.max()),
            },
        },
        "mandatory_nuisance_space": {
            "ambient_dimension": int(q * TOKEN_POS_BINS),
            "basis": [
                "constant cell mean mode 1_C",
                "locked q4 frequency slope lifted as v_Q tensor 1_B",
                "all centered pure token-position main effects 1_Q tensor g_B",
            ],
            "dimension": 1 + 1 + (TOKEN_POS_BINS - 1),
            "residual_dimension": int(q * TOKEN_POS_BINS - (1 + 1 + (TOKEN_POS_BINS - 1))),
        },
        "strict_additive_nuisance_space": {
            "basis": [
                "constant cell mean mode 1_C",
                "all centered q4 frequency main effects",
                "all centered token-position main effects",
            ],
            "dimension": 1 + (q - 1) + (TOKEN_POS_BINS - 1),
            "residual_dimension": int(q * TOKEN_POS_BINS - (1 + (q - 1) + (TOKEN_POS_BINS - 1))),
        },
        "forbidden_axes_for_primary_v1": [
            "seed",
            "generation",
            "fold",
            "token_type_without_preregistered_source_only_map",
            "baseline_surprise_without_preregistered_baseline_source",
            "post_hoc_result_selected_axis",
        ],
        "claim_policy": {
            "may_support": [
                "formal preregistration feasibility",
                "cell occupancy and sparsity no-go checks",
                "fixed nuisance-space definition before any new outcome review",
            ],
            "must_not_support": [
                "LOSO passed",
                "F3 positive",
                "mean-null vector field survives",
                "residual field observed",
                "glass box broken",
                "training authorized",
                "new loss authorized",
                "full panel approved",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q4-schema", type=Path, default=DEFAULT_Q4_SCHEMA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    schema = build_schema(args.q4_schema)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
