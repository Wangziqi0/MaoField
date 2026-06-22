#!/usr/bin/env python3
"""Build the D622 MaoField fixed-train-block panel slice schema.

This script does not load checkpoints and does not run model inference. It
only reconstructs the fixed audit blocks used by the existing high-order
logprob audit and writes a schema JSON for later panel generation.
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


TOKENIZER_ID = "facebook/opt-125m"
DATASET_ID = "wikitext"
DATASET_CONFIG = "wikitext-2-raw-v1"
SOURCE_SPLIT = "train"
BLOCK_SIZE = 64
N_CTX = 128
QUANTILE_METHOD = "nearest"
ASSIGNMENT_POLICY = "np.searchsorted(edges, frequency, side='right')"


def sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_quantile_schema(freq: np.ndarray, q: int) -> dict[str, Any]:
    quantiles = [i / q for i in range(1, q)]
    edges = np.quantile(freq, quantiles, method=QUANTILE_METHOD).astype(int)
    bin_ids = np.searchsorted(edges, freq, side="right")
    sizes = np.bincount(bin_ids, minlength=q).astype(int).tolist()
    empty_bins = [i for i, n in enumerate(sizes) if n == 0]
    return {
        "q": q,
        "quantiles": quantiles,
        "edges": edges.tolist(),
        "assignment_policy": ASSIGNMENT_POLICY,
        "bin_sizes": sizes,
        "empty_bins": empty_bins,
        "min_frequency": int(freq.min()),
        "max_frequency": int(freq.max()),
        "status": "locked" if not empty_bins else "not_locked_empty_bin",
    }


def build_schema() -> dict[str, Any]:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    raw = load_wikitext2(DATASET_ID, DATASET_CONFIG)
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    blocks = tokenize_and_block(raw[SOURCE_SPLIT], tokenizer, BLOCK_SIZE).select(range(N_CTX))
    input_ids = [list(row) for row in blocks["input_ids"]]
    target_ids = [token for row in input_ids for token in row[1:]]
    target_counts = sorted((int(token), int(count)) for token, count in Counter(target_ids).items())
    count_map = dict(target_counts)
    frequencies = np.array([count_map[int(token)] for token in target_ids], dtype=np.int64)

    q4 = build_quantile_schema(frequencies, 4)
    q8 = build_quantile_schema(frequencies, 8)
    if q4["empty_bins"]:
        raise RuntimeError(f"primary q4 schema has empty bins: {q4['empty_bins']}")

    return {
        "artifact_kind": "maofield_panel_slice_schema",
        "artifact_version": "2026-06-22.d622.schema.v1",
        "status": "locked_primary_q4__q8_sensitivity_not_locked",
        "created_date": "2026-06-22",
        "created_by": "scripts/build_panel_schema_20260622.py",
        "schema_scope": "content-defined; git head intentionally excluded from schema hash",
        "no_checkpoint_loaded": True,
        "no_model_inference": True,
        "no_training": True,
        "source": {
            "dataset_id": DATASET_ID,
            "dataset_config": DATASET_CONFIG,
            "source_split": SOURCE_SPLIT,
            "tokenizer_id": TOKENIZER_ID,
            "block_size": BLOCK_SIZE,
            "audit_block_indices": list(range(N_CTX)),
            "n_audit_blocks": N_CTX,
            "n_next_token_positions": len(target_ids),
            "n_unique_target_tokens": len(target_counts),
            "input_ids_sha256": sha256_json(input_ids),
            "target_ids_sha256": sha256_json(target_ids),
            "target_counts_sha256": sha256_json(target_counts),
        },
        "target_token_counts": target_counts,
        "primary_schema": {
            "schema_id": "freq_q4_audit_targets_20260622",
            "role": "primary",
            "can_trigger_strongest_verdict": True,
            "frequency_reference": "target_count_audit_blocks",
            "quantile_algorithm": {
                "library": "numpy",
                "function": "quantile",
                "method": QUANTILE_METHOD,
                "tie_policy": "frequency ties are kept together by edge assignment",
                "edge_inclusivity": "right side via searchsorted(..., side='right')",
                "empty_bin_policy": "abort",
            },
            **q4,
        },
        "sensitivity_candidates": [
            {
                "schema_id": "freq_q8_audit_targets_20260622",
                "role": "sensitivity_only",
                "can_trigger_strongest_verdict": False,
                "lock_decision": (
                    "not locked because the preregistered edge policy creates an empty bin; "
                    "do not change the policy after seeing this fact"
                ),
                **q8,
            }
        ],
        "generator_policy": {
            "must_load_schema": True,
            "must_verify_source_hashes": True,
            "forbidden_fallbacks": [
                "changing quantile method",
                "changing tie policy",
                "changing edge inclusivity",
                "changing empty-bin policy",
                "choosing bins from panel outcomes",
            ],
            "invalid_artifact_if": [
                "source_split is not train",
                "input_ids_sha256 mismatch",
                "target_ids_sha256 mismatch",
                "target_counts_sha256 mismatch",
                "schema is missing",
                "primary schema has an empty bin",
            ],
        },
        "claim_policy": {
            "strongest_allowed_verdict": "eligible_for_next_design_review_only",
            "forbidden_claims": [
                "LOSO passed",
                "F3 positive",
                "mean-null vector field survives",
                "glass box broken",
                "training authorized",
                "new loss authorized",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO
        / "docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json",
    )
    args = parser.parse_args()

    schema = build_schema()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=False) + "\n")
    print(args.out)


if __name__ == "__main__":
    main()
