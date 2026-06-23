#!/usr/bin/env python3
"""Generate MaoField q4 raw-logprob panel artifacts.

This script is intentionally narrow:
- manifest-only verifies the locked schema and fixed train-block hashes;
- one-checkpoint-smoke runs a single CPU fp32 forward pass;
- optional expected-hash arguments fail fast on provenance drift;
- full-panel-dry-run verifies the exact 5x10 checkpoint plan without inference;
- full-panel requires an explicit PI approval token before inference.

It does not train, update weights, call backward, generate text, or create a
new loss.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


REPO = Path("/media/amd/raid1/canonical/projects/MaoField")
SRC = REPO / "experiments/exp018_cat/src"
sys.path.insert(0, str(SRC))

from data_pipeline import load_wikitext2, tokenize_and_block  # noqa: E402


DEFAULT_SCHEMA = (
    REPO
    / "docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json"
)
DEFAULT_OUT_DIR = REPO / "experiments/exp020_metric_stress_test/panel_primary_20260622"
DEFAULT_RAW_DIR = Path("/media/amd/raid1/canonical/wip/maofield_panel_primary_20260622/raw")
DEFAULT_OLD_RESULT = (
    REPO
    / "experiments/exp020_metric_stress_test/highorder_ppl_20260618/highorder_result.json"
)
DEFAULT_BUILDER_SCRIPT = REPO / "scripts/build_panel_schema_20260622.py"
GENERATOR_SCRIPT = Path(__file__).resolve()
CHECKPOINT_ROOT = REPO / "experiments/exp018_cat/data/checkpoints_armb/alpha0.0"
SEEDS = [1, 2, 3, 4, 42]
GENERATIONS = list(range(10))
BATCH_SIZE = 32
FULL_PANEL_APPROVAL_TOKEN = "PI_APPROVED_Q4_FULL_PANEL"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def git_output(args: list[str]) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True).strip()


def git_head() -> str:
    return git_output(["git", "rev-parse", "HEAD"])


def git_status_short() -> str:
    return git_output(["git", "status", "--short", "--branch"])


def checkpoint_path(seed: int, generation: int) -> Path:
    return CHECKPOINT_ROOT / f"no_preserve_seed{seed}" / f"generation_{generation}"


def expected_checkpoints() -> list[dict[str, Any]]:
    rows = []
    for seed in SEEDS:
        for generation in GENERATIONS:
            path = checkpoint_path(seed, generation)
            model_path = path / "model.safetensors"
            rows.append(
                {
                    "seed": seed,
                    "generation": generation,
                    "checkpoint_path": str(path.relative_to(REPO)),
                    "model_safetensors_path": str(model_path.relative_to(REPO)),
                    "exists": model_path.exists(),
                }
            )
    return rows


def require_all_checkpoints(rows: list[dict[str, Any]]) -> None:
    missing = [row for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError(
            "missing expected checkpoints: "
            + ", ".join(row["model_safetensors_path"] for row in missing)
        )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def repo_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def provenance_hashes(schema_path: Path) -> dict[str, str]:
    return {
        "schema_sha256": sha256_file(schema_path),
        "builder_script_sha256": sha256_file(DEFAULT_BUILDER_SCRIPT),
        "generator_script_sha256": sha256_file(GENERATOR_SCRIPT),
    }


def build_blocks_and_targets(schema: dict[str, Any]) -> dict[str, Any]:
    source = schema["source"]
    if source["source_split"] != "train":
        raise ValueError("schema source_split must be train")

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
    target_frequencies = np.array([count_map[token] for token in target_ids], dtype=np.int64)

    hashes = {
        "input_ids_sha256": sha256_json(input_ids),
        "target_ids_sha256": sha256_json(target_ids),
        "target_counts_sha256": sha256_json(target_counts),
    }
    for key, got in hashes.items():
        expected = source[key]
        if got != expected:
            raise ValueError(f"{key} mismatch: got {got}, expected {expected}")

    primary = schema["primary_schema"]
    if primary["status"] != "locked":
        raise ValueError("primary schema is not locked")
    if primary["empty_bins"]:
        raise ValueError(f"primary schema has empty bins: {primary['empty_bins']}")

    edges = np.array(primary["edges"], dtype=np.int64)
    slice_ids = np.searchsorted(edges, target_frequencies, side="right")
    bin_sizes = np.bincount(slice_ids, minlength=int(primary["q"])).astype(int).tolist()
    if bin_sizes != primary["bin_sizes"]:
        raise ValueError(f"q4 bin sizes mismatch: got {bin_sizes}, expected {primary['bin_sizes']}")

    block_ids: list[int] = []
    token_positions: list[int] = []
    for block_id, row in enumerate(input_ids):
        for token_pos in range(1, len(row)):
            block_ids.append(block_id)
            token_positions.append(token_pos)

    return {
        "tokenizer": tokenizer,
        "blocks": blocks,
        "input_ids": input_ids,
        "target_ids": np.array(target_ids, dtype=np.int64),
        "target_frequencies": target_frequencies,
        "slice_ids": slice_ids.astype(np.int64),
        "block_ids": np.array(block_ids, dtype=np.int64),
        "token_positions": np.array(token_positions, dtype=np.int64),
        "hashes": hashes,
    }


def base_manifest(
    schema_path: Path,
    schema: dict[str, Any],
    source_data: dict[str, Any],
    hashes: dict[str, str],
    args: argparse.Namespace,
) -> dict[str, Any]:
    head = git_head()
    return {
        "artifact_kind": "maofield_panel_primary_manifest",
        "artifact_version": "2026-06-22.d622.generator.v3",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "repo_head": head,
        "artifact_generation_repo_head": head,
        "expected_repo_head": args.expected_repo_head,
        "expected_repo_head_status": "pass" if args.expected_repo_head else "not_provided",
        "provenance_note": (
            "repo_head is the artifact-generation commit. The git commit that "
            "records this manifest may be later; compare both explicitly in "
            "review bundles."
        ),
        "dirty_state_note": git_status_short(),
        "schema_path": repo_display_path(schema_path),
        "schema_sha256": hashes["schema_sha256"],
        "schema_builder_path": repo_display_path(DEFAULT_BUILDER_SCRIPT),
        "builder_script_sha256": hashes["builder_script_sha256"],
        "generator_script_path": repo_display_path(GENERATOR_SCRIPT),
        "generator_script_sha256": hashes["generator_script_sha256"],
        "source_split": schema["source"]["source_split"],
        "input_ids_sha256": source_data["hashes"]["input_ids_sha256"],
        "target_ids_sha256": source_data["hashes"]["target_ids_sha256"],
        "target_counts_sha256": source_data["hashes"]["target_counts_sha256"],
        "checkpoint_root": str(CHECKPOINT_ROOT.relative_to(REPO)),
        "seeds": SEEDS,
        "generations": GENERATIONS,
        "device": args.device,
        "dtype": args.dtype,
        "batch_size": args.batch_size,
        "no_training": True,
        "no_backward": True,
        "no_optimizer_step": True,
        "no_new_loss": True,
        "no_text_generation": True,
        "schema_status": schema["status"],
        "primary_schema_id": schema["primary_schema"]["schema_id"],
        "primary_q4_edges": schema["primary_schema"]["edges"],
        "primary_q4_bin_sizes": schema["primary_schema"]["bin_sizes"],
        "q8_lock_status": schema["sensitivity_candidates"][0]["status"],
        "claim_policy": schema["claim_policy"],
        "gate_status": {
            "data_source_gate": "pass",
            "schema_freeze_gate": "pass",
            "full_panel_generated": False,
            "training_authorized": False,
        },
    }


def enforce_expected_hashes(args: argparse.Namespace, hashes: dict[str, str]) -> None:
    checks = {
        "schema_sha256": args.expected_schema_sha256,
        "builder_script_sha256": args.expected_builder_sha256,
        "generator_script_sha256": args.expected_generator_sha256,
    }
    for key, expected in checks.items():
        if expected is None:
            continue
        got = hashes[key]
        if got != expected:
            raise ValueError(f"{key} mismatch: got {got}, expected {expected}")


def enforce_runtime_args(args: argparse.Namespace) -> None:
    if args.device != "cpu":
        raise ValueError("only --device cpu is allowed for the q4 audit panel")
    if args.dtype != "float32":
        raise ValueError("only --dtype float32 is allowed for the q4 audit panel")
    if args.batch_size != BATCH_SIZE:
        raise ValueError(f"batch_size must stay locked at {BATCH_SIZE}")
    if args.full_panel and args.full_panel_approval_token != FULL_PANEL_APPROVAL_TOKEN:
        raise PermissionError(
            "full panel requires --full-panel-approval-token "
            f"{FULL_PANEL_APPROVAL_TOKEN}"
        )
    if args.expected_repo_head is not None and git_head() != args.expected_repo_head:
        raise ValueError(
            f"repo_head mismatch: got {git_head()}, expected {args.expected_repo_head}"
        )


@torch.no_grad()
def get_logprob_arrays(model: torch.nn.Module, blocks: Any) -> np.ndarray:
    chunks: list[torch.Tensor] = []
    for start in range(0, len(blocks), BATCH_SIZE):
        ids = torch.tensor(blocks[start : start + BATCH_SIZE]["input_ids"], dtype=torch.long)
        logits = model(input_ids=ids).logits.float()
        logp = torch.log_softmax(logits, dim=-1)
        lp = logp[:, :-1, :].gather(-1, ids[:, 1:].unsqueeze(-1)).squeeze(-1)
        chunks.append(lp.reshape(-1).cpu())
    return torch.cat(chunks).numpy()


def load_model(path: Path) -> torch.nn.Module:
    if not (path / "model.safetensors").exists():
        raise FileNotFoundError(f"checkpoint missing model.safetensors: {path}")
    return AutoModelForCausalLM.from_pretrained(path, dtype=torch.float32).to("cpu").eval()


def weighted_projection(k: np.ndarray, weights: np.ndarray) -> dict[str, Any]:
    d_value = float(np.sum(weights * k))
    u = k - d_value
    v_raw = np.array([-1.5, -0.5, 0.5, 1.5], dtype=float)
    v_center = v_raw - float(np.sum(weights * v_raw))
    norm = math.sqrt(float(np.sum(weights * v_center**2)))
    if norm <= 0:
        raise ValueError("primary projection norm is zero")
    v = v_center / norm
    p_value = float(np.sum(weights * v * u))
    return {
        "mean_mode_D": d_value,
        "u_values": [float(x) for x in u],
        "projection_weights_v": [float(x) for x in v],
        "primary_projection_P": p_value,
    }


def aggregate_smoke(
    lp: np.ndarray,
    source_data: dict[str, Any],
    schema: dict[str, Any],
    seed: int,
    generation: int,
) -> dict[str, Any]:
    slice_ids = source_data["slice_ids"]
    q = int(schema["primary_schema"]["q"])
    rows = []
    n_total = int(len(lp))
    means = []
    weights = []
    for slice_id in range(q):
        mask = slice_ids == slice_id
        vals = lp[mask]
        n = int(vals.size)
        weight = float(n / n_total)
        mean = float(np.mean(vals))
        means.append(mean)
        weights.append(weight)
        rows.append(
            {
                "schema_id": schema["primary_schema"]["schema_id"],
                "seed": seed,
                "generation": generation,
                "slice_id": slice_id,
                "n_tokens": n,
                "weight": weight,
                "mean_logprob": mean,
                "var_logprob": float(np.var(vals)),
                "k_value": mean,
                "k_value_type": "target_logprob_mean",
            }
        )
    projection = weighted_projection(np.array(means, dtype=float), np.array(weights, dtype=float))
    for row, u_value in zip(rows, projection["u_values"]):
        row["mean_mode_D"] = projection["mean_mode_D"]
        row["u_value"] = u_value

    return {
        "schema_id": schema["primary_schema"]["schema_id"],
        "seed": seed,
        "generation": generation,
        "n_tokens": n_total,
        "global_mean_lp": float(np.mean(lp)),
        "global_ppl": float(math.exp(-float(np.mean(lp)))),
        "global_var_lp": float(np.var(lp)),
        "slice_rows": rows,
        **projection,
    }


def old_reproduction_check(
    lp: np.ndarray,
    source_data: dict[str, Any],
    seed: int,
    generation: int,
    old_result_path: Path,
) -> dict[str, Any]:
    if not old_result_path.exists():
        return {"status": "missing_old_result", "path": str(old_result_path)}
    old = load_json(old_result_path)
    match = next(
        (r for r in old["rows"] if int(r["seed"]) == seed and int(r["gen"]) == generation),
        None,
    )
    if match is None:
        return {"status": "missing_old_row", "seed": seed, "generation": generation}

    freq = source_data["target_frequencies"]
    lo = float(np.percentile(freq, 20))
    hi = float(np.percentile(freq, 80))
    rare = freq <= lo
    high = freq >= hi
    tau = float(old["tau"])
    got = {
        "mean_lp": float(np.mean(lp)),
        "F1_var": float(np.var(lp)),
        "F1_tail": float(np.mean(lp < tau)),
        "F3_slice_rare": float(np.mean(lp[rare])),
        "F3_slice_freq": float(np.mean(lp[high])),
        "F3_slice_gap": float(np.mean(lp[high]) - np.mean(lp[rare])),
    }
    diffs = {key: float(got[key] - float(match[key])) for key in got}
    abs_diffs = {key: abs(val) for key, val in diffs.items()}
    return {
        "status": "pass" if all(v <= 1e-5 for v in abs_diffs.values()) else "fail",
        "tolerance_abs": 1e-5,
        "tau_from_old_result": tau,
        "rare_threshold": lo,
        "freq_threshold": hi,
        "computed": got,
        "expected_old_row": {key: match[key] for key in got},
        "diffs": diffs,
        "abs_diffs": abs_diffs,
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def write_raw_jsonl(
    path: Path,
    lp: np.ndarray,
    source_data: dict[str, Any],
    schema: dict[str, Any],
    seed: int,
    generation: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for idx, val in enumerate(lp):
            row = {
                "schema_id": schema["primary_schema"]["schema_id"],
                "seed": seed,
                "generation": generation,
                "source_split": schema["source"]["source_split"],
                "audit_block_id": int(source_data["block_ids"][idx]),
                "token_pos": int(source_data["token_positions"][idx]),
                "flat_token_index": idx,
                "target_token_id": int(source_data["target_ids"][idx]),
                "target_count_audit_blocks": int(source_data["target_frequencies"][idx]),
                "slice_id": int(source_data["slice_ids"][idx]),
                "token_logprob": float(val),
                "neg_logprob": float(-val),
            }
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def run_manifest_only(args: argparse.Namespace, manifest: dict[str, Any]) -> Path:
    path = args.out_dir / "manifest_only_20260622.json"
    manifest = {
        **manifest,
        "run_mode": "manifest_only",
        "full_panel_generated": False,
        "one_checkpoint_smoke": False,
    }
    write_json(path, manifest)
    return path


def full_panel_paths(args: argparse.Namespace) -> dict[str, Path]:
    return {
        "plan": args.out_dir / f"{args.panel_id}_plan.json",
        "manifest": args.out_dir / f"{args.panel_id}_manifest.json",
        "aggregate": args.out_dir / f"{args.panel_id}_aggregate.json",
        "summary": args.out_dir / f"{args.panel_id}_summary.json",
        "raw_dir": args.raw_dir / args.panel_id,
    }


def run_full_panel_dry_run(args: argparse.Namespace, manifest: dict[str, Any]) -> Path:
    rows = expected_checkpoints()
    require_all_checkpoints(rows)
    paths = full_panel_paths(args)
    plan = {
        **manifest,
        "artifact_kind": "maofield_q4_full_panel_plan",
        "run_mode": "full_panel_dry_run",
        "panel_id": args.panel_id,
        "checkpoint_count": len(rows),
        "expected_checkpoints": rows,
        "raw_dir": str(paths["raw_dir"]),
        "full_panel_generated": False,
        "no_checkpoint_loaded": True,
        "approval_token_required_for_full_panel": FULL_PANEL_APPROVAL_TOKEN,
        "gate_status": {
            **manifest["gate_status"],
            "checkpoint_enumeration": "pass",
            "full_panel_dry_run": "pass",
        },
    }
    write_json(paths["plan"], plan)
    return paths["plan"]


def run_full_panel(
    args: argparse.Namespace,
    manifest: dict[str, Any],
    schema: dict[str, Any],
    source_data: dict[str, Any],
) -> dict[str, Path]:
    rows = expected_checkpoints()
    require_all_checkpoints(rows)
    paths = full_panel_paths(args)
    paths["raw_dir"].mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    aggregate_rows: list[dict[str, Any]] = []
    panel_records: list[dict[str, Any]] = []
    reproduction_statuses: list[str] = []

    for item in rows:
        seed = int(item["seed"])
        generation = int(item["generation"])
        ckpt = checkpoint_path(seed, generation)
        model = load_model(ckpt)
        lp = get_logprob_arrays(model, source_data["blocks"])
        del model
        if len(lp) != schema["source"]["n_next_token_positions"]:
            raise ValueError(f"logprob length mismatch for seed={seed} gen={generation}: {len(lp)}")

        aggregate = aggregate_smoke(lp, source_data, schema, seed, generation)
        reproduction = old_reproduction_check(lp, source_data, seed, generation, args.old_result)
        raw_path = paths["raw_dir"] / f"seed{seed}_generation{generation}_token_panel.jsonl"
        write_raw_jsonl(raw_path, lp, source_data, schema, seed, generation)
        raw_hash = sha256_file(raw_path)

        aggregate["raw_jsonl_path"] = str(raw_path)
        aggregate["raw_jsonl_sha256"] = raw_hash
        aggregate["checkpoint_path"] = str(ckpt.relative_to(REPO))
        aggregate["old_aggregate_reproduction"] = reproduction
        aggregate_rows.append(aggregate)
        reproduction_statuses.append(reproduction["status"])
        panel_records.append(
            {
                **item,
                "raw_jsonl_path": str(raw_path),
                "raw_jsonl_sha256": raw_hash,
                "old_aggregate_reproduction_status": reproduction["status"],
            }
        )

    aggregate_doc = {
        "artifact_kind": "maofield_q4_full_panel_aggregate",
        "artifact_version": "2026-06-23.d623.full_panel.v1",
        "panel_id": args.panel_id,
        "schema_id": schema["primary_schema"]["schema_id"],
        "row_count": len(aggregate_rows),
        "seeds": SEEDS,
        "generations": GENERATIONS,
        "rows": aggregate_rows,
        "claim_boundary": {
            "full_panel_result_only": True,
            "does_not_authorize_training": True,
            "does_not_establish_glass_box": True,
        },
    }
    write_json(paths["aggregate"], aggregate_doc)

    summary = {
        "artifact_kind": "maofield_q4_full_panel_summary",
        "panel_id": args.panel_id,
        "row_count": len(aggregate_rows),
        "elapsed_s": round(time.time() - t0, 3),
        "all_old_aggregate_reproductions_pass": all(
            status == "pass" for status in reproduction_statuses
        ),
        "reproduction_status_counts": dict(Counter(reproduction_statuses)),
        "aggregate_path": str(paths["aggregate"]),
        "raw_dir": str(paths["raw_dir"]),
    }
    write_json(paths["summary"], summary)

    full_manifest = {
        **manifest,
        "run_mode": "full_panel",
        "panel_id": args.panel_id,
        "checkpoint_count": len(rows),
        "expected_checkpoints": rows,
        "panel_records": panel_records,
        "aggregate_path": str(paths["aggregate"]),
        "aggregate_sha256": sha256_file(paths["aggregate"]),
        "summary_path": str(paths["summary"]),
        "summary_sha256": sha256_file(paths["summary"]),
        "raw_dir": str(paths["raw_dir"]),
        "elapsed_s": summary["elapsed_s"],
        "full_panel_generated": True,
        "one_checkpoint_smoke": False,
        "gate_status": {
            **manifest["gate_status"],
            "checkpoint_enumeration": "pass",
            "full_panel_generated": "pass",
            "old_aggregate_reproduction_all_rows": (
                "pass" if summary["all_old_aggregate_reproductions_pass"] else "fail"
            ),
        },
    }
    write_json(paths["manifest"], full_manifest)
    return {
        "manifest": paths["manifest"],
        "aggregate": paths["aggregate"],
        "summary": paths["summary"],
    }


def run_one_checkpoint_smoke(
    args: argparse.Namespace,
    manifest: dict[str, Any],
    schema: dict[str, Any],
    source_data: dict[str, Any],
) -> dict[str, Path]:
    ckpt = checkpoint_path(args.seed, args.generation)
    t0 = time.time()
    model = load_model(ckpt)
    lp = get_logprob_arrays(model, source_data["blocks"])
    del model

    if len(lp) != schema["source"]["n_next_token_positions"]:
        raise ValueError(f"logprob length mismatch: {len(lp)}")

    aggregate = aggregate_smoke(lp, source_data, schema, args.seed, args.generation)
    reproduction = old_reproduction_check(lp, source_data, args.seed, args.generation, args.old_result)
    raw_path = (
        args.raw_dir
        / f"smoke_seed{args.seed}_generation{args.generation}_token_panel.jsonl"
    )
    write_raw_jsonl(raw_path, lp, source_data, schema, args.seed, args.generation)

    smoke_manifest = {
        **manifest,
        "run_mode": "one_checkpoint_smoke",
        "seed": args.seed,
        "generation": args.generation,
        "checkpoint_path": str(ckpt.relative_to(REPO)),
        "raw_jsonl_path": str(raw_path),
        "raw_jsonl_sha256": sha256_file(raw_path),
        "elapsed_s": round(time.time() - t0, 3),
        "one_checkpoint_smoke": True,
        "full_panel_generated": False,
        "reproduction_gate": reproduction,
        "gate_status": {
            **manifest["gate_status"],
            "one_checkpoint_smoke": "pass",
            "old_aggregate_reproduction": reproduction["status"],
        },
    }

    manifest_path = args.out_dir / f"one_checkpoint_smoke_seed{args.seed}_gen{args.generation}_manifest.json"
    aggregate_path = args.out_dir / f"one_checkpoint_smoke_seed{args.seed}_gen{args.generation}_aggregate.json"
    write_json(manifest_path, smoke_manifest)
    write_json(aggregate_path, aggregate)
    return {
        "manifest": manifest_path,
        "aggregate": aggregate_path,
        "raw_jsonl": raw_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--old-result", type=Path, default=DEFAULT_OLD_RESULT)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--one-checkpoint-smoke", action="store_true")
    parser.add_argument("--full-panel-dry-run", action="store_true")
    parser.add_argument("--full-panel", action="store_true")
    parser.add_argument("--expected-schema-sha256")
    parser.add_argument("--expected-builder-sha256")
    parser.add_argument("--expected-generator-sha256")
    parser.add_argument("--expected-repo-head")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--dtype", default="float32")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--panel-id", default="q4_full_panel_20260623")
    parser.add_argument("--full-panel-approval-token")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--generation", type=int, default=0)
    args = parser.parse_args()
    modes = [
        args.manifest_only,
        args.one_checkpoint_smoke,
        args.full_panel_dry_run,
        args.full_panel,
    ]
    if sum(bool(mode) for mode in modes) != 1:
        parser.error(
            "choose exactly one of --manifest-only, --one-checkpoint-smoke, "
            "--full-panel-dry-run, or --full-panel"
        )
    if args.seed not in SEEDS:
        parser.error(f"seed must be one of {SEEDS}")
    if args.generation not in GENERATIONS:
        parser.error(f"generation must be one of {GENERATIONS}")
    return args


def main() -> None:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    args = parse_args()
    enforce_runtime_args(args)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    hashes = provenance_hashes(args.schema)
    enforce_expected_hashes(args, hashes)
    schema = load_json(args.schema)
    source_data = build_blocks_and_targets(schema)
    manifest = base_manifest(args.schema, schema, source_data, hashes, args)

    if args.manifest_only:
        path = run_manifest_only(args, manifest)
        print(path)
        return

    if args.full_panel_dry_run:
        path = run_full_panel_dry_run(args, manifest)
        print(path)
        return

    if args.full_panel:
        paths = run_full_panel(args, manifest, schema, source_data)
        for path in paths.values():
            print(path)
        return

    paths = run_one_checkpoint_smoke(args, manifest, schema, source_data)
    for path in paths.values():
        print(path)


if __name__ == "__main__":
    main()
