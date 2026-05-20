#!/usr/bin/env python3
"""
yaml_setup_hash.py — caveat 2: verify 5/9 chain α=0 seed 0/1 数据可否 stack 进 5 seed Phase 1

提取 yaml 中 setup-affecting 字段, 算 hash, 比对 5/9 chain run 的 yaml setup vs 当前 yaml setup.
match → 5/9 数据可 stack as legit seed=0/1 entries
mismatch → 5/9 数据排除 (or 重跑)

用 5/9 jsonl 中的 model_path 推断当时的 setup (通过 backup yaml 或 archive)。
但 5/9 yaml 已被覆盖 — 我们只能用 git history 或 hash from 当前 jsonl metadata。

Pragmatic approach: 比 5/9 chain 与 5/10 robust chain 的 cat_arm_b.yaml setup hash。
若 hash 同 (没改 framework 字段) → stack OK。
若 hash 不同 → 排除 5/9 数据。

usage:
  python scripts/yaml_setup_hash.py configs/cat_arm_b.yaml
  python scripts/yaml_setup_hash.py configs/cat_arm_b.yaml.backup_pre_fp32_*
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp018_cat")

# Setup-affecting fields (changes invalidate trajectory comparability)
SETUP_FIELDS = [
    "model.dtype",
    "model.hf_id",
    "dataset.hf_id",
    "dataset.hf_config",
    "dataset.block_size",
    "fine_tune.optimizer",
    "fine_tune.learning_rate",
    "fine_tune.per_device_train_batch_size",
    "fine_tune.gradient_accumulation_steps",
    "fine_tune.weight_decay",
    "fine_tune.warmup_ratio",
    "fine_tune.lr_scheduler_type",
    "fine_tune.fp16",
    "generation.strategy",
    "generation.num_beams",
    "generation.do_sample",
    "generation.prompt_length",
    "generation.max_new_tokens",
    "generation.per_device_generation_batch_size",
    "generation.repetition_penalty",
    "self_iteration.num_generations",
    # condition_no_preserve.epochs_per_generation: nested, handled separately
]


def extract_value(yaml_dict, dotted_path):
    """Extract value at 'a.b.c' from nested dict."""
    parts = dotted_path.split(".")
    v = yaml_dict
    for p in parts:
        if isinstance(v, dict) and p in v:
            v = v[p]
        else:
            return None
    return v


def setup_hash(yaml_path):
    with open(yaml_path) as f:
        d = yaml.safe_load(f)
    extracted = {}
    for field in SETUP_FIELDS:
        extracted[field] = extract_value(d, field)
    # Special: no_preserve epochs
    conds = d.get("self_iteration", {}).get("conditions", [])
    for c in conds:
        if c.get("name") == "no_preserve":
            extracted["no_preserve.epochs_per_generation"] = c.get("epochs_per_generation")
            extracted["no_preserve.original_data_fraction"] = c.get("original_data_fraction")
    # Hash
    canon = json.dumps(extracted, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]
    return h, extracted


def main():
    if len(sys.argv) < 2:
        # Default: compare current vs backup
        targets = sorted([
            PROJECT_ROOT / "configs/cat_arm_b.yaml",
        ] + list((PROJECT_ROOT / "configs").glob("cat_arm_b.yaml.backup_*")))
    else:
        targets = [Path(p) for p in sys.argv[1:]]

    print(f"=== Setup hash on {len(targets)} yaml files ===\n")
    hashes = {}
    for p in targets:
        if not p.exists():
            print(f"  {p.name}: NOT FOUND")
            continue
        h, extracted = setup_hash(p)
        hashes[p.name] = (h, extracted)
        print(f"  {p.name}")
        print(f"    setup_hash = {h}")

    print(f"\n=== Setup hash comparison ===")
    if len(hashes) >= 2:
        baseline_name = list(hashes.keys())[0]
        baseline_h = hashes[baseline_name][0]
        for name, (h, extracted) in hashes.items():
            same = "✓ SAME" if h == baseline_h else "✗ DIFFERENT"
            print(f"  {name}: {h} {same} (vs {baseline_name[:30]})")

    # Detail current
    if hashes:
        print(f"\n=== Field detail ({list(hashes.keys())[0]}) ===")
        for k, v in hashes[list(hashes.keys())[0]][1].items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
