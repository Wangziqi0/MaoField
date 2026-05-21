#!/usr/bin/env python3
"""
launch_dppl_bridge.py — D-PPL 桥 verify 之 9070XT 端 launch script

D21 (2026-05-21) 7B13 sub-agent (D-PPL 桥 verify launch 准备 sub-agent) 写, 9070XT 端 跑.

mode:
  - pilot: 1 seed × 1 gen × 1 α × 2 path = 2 tuple, ~30-60 min
  - main:  N seed × N gen × N α × 2 path = 4*10*2*2 = 160 tuple, ~3-4 天

路径 B (gen-(n-1) 主 model 作 EMA proxy):
  D_n^{code,proxy-EMA} := KL(q^{θ_{n-1}} || p^{θ_n}) on val batch (next-token, mask padding)

路径 C (current vs gen-0 base 之 KL):
  D_n^{code,gen0-anchor} := KL(q^{θ_0} || p^{θ_n}) on val batch

数学 严格度 caveat: L2 form-borrow tier (B 是 EMA proxy via gen-(n-1), C 是 gen-0 anchor;
真 L1 严 需 路径 A re-train EMA SGD replay)

D-1 binding (9070XT zero-context sub-agent 之 纪律):
  - 不擅自 declare P0★-F close
  - 仅 surface raw D_code 数字
  - 数字 全 jsonl-traced (D-1 纪律 1)
  - 占位符禁令: unverified 数字 标 [?] OR skip

用法 (9070XT 端):
  python3 launch_dppl_bridge.py --mode pilot --alpha 10.0 --seed 1 --gen 5 --paths B,C ...
  python3 launch_dppl_bridge.py --mode main  --alphas 0.0,10.0 --seeds 1,2,3,4 --gens 0,1,...,9 --paths B,C ...
"""
import argparse
import gc
import json
import os
import shlex
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# -----------------------------------------------------------------------------
# Constants (binary lock per paper §3.2 + chain log first-line print)
# -----------------------------------------------------------------------------
VAL_DATASET_NAME = "wikitext"
VAL_DATASET_CONFIG = "wikitext-2-raw-v1"
VAL_DATASET_SPLIT = "validation"
TOKENIZER_NAME = "facebook/opt-125m"  # OPT-125M chain main model

# -----------------------------------------------------------------------------
# Utils
# -----------------------------------------------------------------------------
def utc_now() -> str:
    """ISO-8601 UTC timestamp (D-1 纪律 5 实时日期)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_jsonl(path: Path, entry: dict) -> None:
    """Append entry to jsonl, flush 之 (crash-safe)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def log_print(msg: str, log_file: Optional[Path] = None) -> None:
    """Print + log file (mtime update 让 watchdog 知道 alive)."""
    ts = utc_now()
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())


def rsync_push(src: str, dst: str, log_file: Optional[Path] = None) -> bool:
    """rsync push src → dst, 返 success bool. 不 raise (避免 main 阻塞)."""
    cmd = ["rsync", "-avz", src, dst]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            log_print(f"rsync push ✓: {src} → {dst}", log_file)
            return True
        else:
            log_print(f"rsync push ✗ rc={result.returncode}: {result.stderr[:500]}", log_file)
            return False
    except subprocess.TimeoutExpired:
        log_print(f"rsync push timeout > 300 sec: {src}", log_file)
        return False
    except Exception as e:
        log_print(f"rsync push exception: {e}", log_file)
        return False


# -----------------------------------------------------------------------------
# Model + tokenizer + val batch (lazy import torch, transformers, datasets)
# -----------------------------------------------------------------------------
def reproduce_val_batch(val_seed: int, val_subset_size: int, val_max_length: int,
                        batch_size: int, log_file: Optional[Path]):
    """
    Reproduce chain main run 之 val batch (per train_one_generation.py line 158-162).

    binary mirror:
      val_subset = val_dataset.shuffle(seed=seed).select(range(val_subset_size))
      build_val_loader_for_kl(val_subset, tokenizer, batch_size=8, max_length=64)

    return: list of (input_ids tensor, attention_mask tensor) per batch
    """
    from datasets import load_dataset
    from transformers import AutoTokenizer
    import torch

    log_print(f"reproduce_val_batch: seed={val_seed}, subset_size={val_subset_size}, "
              f"max_length={val_max_length}, batch_size={batch_size}", log_file)

    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    ds = load_dataset(VAL_DATASET_NAME, VAL_DATASET_CONFIG, split=VAL_DATASET_SPLIT)
    ds_shuf = ds.shuffle(seed=val_seed).select(range(min(val_subset_size, len(ds))))

    def tokenize_fn(ex):
        return tokenizer(
            ex["text"],
            max_length=val_max_length,
            padding="max_length",
            truncation=True,
        )

    ds_tok = ds_shuf.map(tokenize_fn, batched=False, remove_columns=["text"])

    # binary verify 第一 sample 之 shape
    first = ds_tok[0]
    assert len(first["input_ids"]) == val_max_length, f"val batch tokenize 之 length 不 = {val_max_length}"
    log_print(f"val batch reproduce ✓ n_samples={len(ds_tok)}, first 之 len(input_ids)={len(first['input_ids'])}",
              log_file)

    # 拆 batch
    batches = []
    for i in range(0, len(ds_tok), batch_size):
        batch_slice = ds_tok[i : i + batch_size]
        input_ids = torch.tensor(batch_slice["input_ids"], dtype=torch.long)
        attention_mask = torch.tensor(batch_slice["attention_mask"], dtype=torch.long)
        batches.append((input_ids, attention_mask))

    log_print(f"val batch 拆 之 n_batches = {len(batches)}", log_file)
    return batches, tokenizer


def load_model(ckpt_path: str, dtype_str: str, log_file: Optional[Path]):
    """Load OPT-125M from checkpoint dir (含 model.safetensors), put on GPU, eval mode."""
    import torch
    from transformers import AutoModelForCausalLM

    if dtype_str == "fp32":
        dtype = torch.float32
    elif dtype_str == "fp16":
        dtype = torch.float16
    else:
        raise ValueError(f"unknown dtype {dtype_str}")

    log_print(f"load_model ckpt={ckpt_path} dtype={dtype_str}", log_file)
    model = AutoModelForCausalLM.from_pretrained(ckpt_path, torch_dtype=dtype)
    model = model.cuda()
    model.eval()
    return model


def compute_kl_q_to_p(model_p, model_q, batches, log_file: Optional[Path]) -> tuple:
    """
    Compute KL(q || p) on val batches, mirror src/contradiction_loss.py compute_kl q_to_p direction.

    binary form:
      logits_p = model_p(input_ids, attention_mask).logits  # current model
      logits_q = model_q(input_ids, attention_mask).logits  # reference model (no grad)
      log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
      log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)
      q = log_q.exp()
      kl_per_pos = (q * (log_q - log_p)).sum(dim=-1)  # [B, T-1]
      mask = attention_mask[:, 1:].float()
      kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)

    return: (kl_scalar_float, n_tokens_int)
    """
    import torch
    import torch.nn.functional as F

    model_p.eval()
    model_q.eval()

    kl_accum = 0.0
    mask_accum = 0.0

    with torch.no_grad():
        for batch_idx, (input_ids, attention_mask) in enumerate(batches):
            input_ids = input_ids.cuda()
            attention_mask = attention_mask.cuda()

            logits_p = model_p(input_ids=input_ids, attention_mask=attention_mask).logits
            logits_q = model_q(input_ids=input_ids, attention_mask=attention_mask).logits

            log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
            log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)

            q = log_q.exp()  # 不 grad, in no_grad context
            kl_per_pos = (q * (log_q - log_p)).sum(dim=-1)  # [B, T-1]

            mask = attention_mask[:, 1:].float()
            kl_accum += (kl_per_pos * mask).sum().item()
            mask_accum += mask.sum().item()

    kl_scalar = kl_accum / max(mask_accum, 1.0)
    return float(kl_scalar), int(mask_accum)


# -----------------------------------------------------------------------------
# Per-tuple compute (one (alpha, seed, gen, path) tuple)
# -----------------------------------------------------------------------------
def compute_one_tuple(ckpt_root: str, alpha: float, seed: int, gen: int, path: str,
                      val_seed: int, val_subset_size: int, val_max_length: int,
                      batch_size: int, dtype_str: str, log_file: Optional[Path]) -> dict:
    """
    Compute D^code for one (alpha, seed, gen, path) tuple.

    path:
      - "B": KL(model_{gen-1} || model_{gen}) — gen-(n-1) main as EMA proxy
      - "C": KL(model_0 || model_{gen}) — gen-0 base anchor

    return: dict 含 D_code value + n_tokens + elapsed + 任何 caveat
    """
    import torch

    t_start = time.time()
    log_print(f"compute_one_tuple: α={alpha}, seed={seed}, gen={gen}, path={path}", log_file)

    # binary verify checkpoint dir
    ckpt_current = f"{ckpt_root}/alpha{alpha}/no_preserve_seed{seed}/generation_{gen}"
    if not Path(ckpt_current).exists():
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"ckpt_current 不存在: {ckpt_current}",
        }

    # path B: gen-(n-1) main model 作 EMA proxy
    if path == "B":
        if gen == 0:
            # gen 0 之 EMA proxy 缺失 (无 gen-(-1) state), skip OR 用 OPT-125M base
            # 本 script 决策: skip gen=0 path B, 写 entry 标 caveat
            return {
                "ts": utc_now(),
                "event": "tuple_skipped",
                "alpha": alpha, "seed": seed, "gen": gen, "path": path,
                "reason": "gen=0 之 path B 缺 gen-(-1) state, skip per brief §4.2",
            }
        ckpt_ref = f"{ckpt_root}/alpha{alpha}/no_preserve_seed{seed}/generation_{gen - 1}"

    # path C: gen-0 base anchor
    elif path == "C":
        ckpt_ref = f"{ckpt_root}/alpha{alpha}/no_preserve_seed{seed}/generation_0"
        if gen == 0:
            # gen=0 之 path C: KL(model_0 || model_0) = 0 trivially
            # 仍跑, ballpark verify pipeline numerical = 0 ± epsilon
            pass
    else:
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"unknown path {path}",
        }

    if not Path(ckpt_ref).exists():
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"ckpt_ref 不存在: {ckpt_ref}",
        }

    # Reproduce val batch (per chain main run 之 seed)
    try:
        batches, _ = reproduce_val_batch(
            val_seed=val_seed,
            val_subset_size=val_subset_size,
            val_max_length=val_max_length,
            batch_size=batch_size,
            log_file=log_file,
        )
    except Exception as e:
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"reproduce_val_batch fail: {e}",
            "traceback": traceback.format_exc()[:1000],
        }

    # Load 2 models
    try:
        model_p = load_model(ckpt_current, dtype_str, log_file)  # current (gen=n)
        model_q = load_model(ckpt_ref, dtype_str, log_file)      # reference (gen=n-1 OR gen=0)
    except Exception as e:
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"load_model fail: {e}",
            "traceback": traceback.format_exc()[:1000],
        }

    # Compute KL(q || p)
    try:
        kl_scalar, n_tokens = compute_kl_q_to_p(model_p, model_q, batches, log_file)
    except Exception as e:
        # cleanup before return
        del model_p, model_q
        gc.collect()
        torch.cuda.empty_cache()
        return {
            "ts": utc_now(),
            "event": "tuple_error",
            "alpha": alpha, "seed": seed, "gen": gen, "path": path,
            "error": f"compute_kl fail: {e}",
            "traceback": traceback.format_exc()[:1000],
        }

    # Cleanup VRAM (binary, 避免 main run 之 cumulative leak)
    del model_p, model_q
    gc.collect()
    torch.cuda.empty_cache()

    elapsed = time.time() - t_start

    # Caveat detection
    caveats = []
    if not (1e-6 <= kl_scalar <= 1e+2):
        caveats.append(f"D_code 之 ballpark 异常 ({kl_scalar:.4e}), 期望 [1e-6, 1e+2]")
    if dtype_str == "fp16":
        caveats.append("dtype fp16, 数值 drift caveat [?]")

    entry = {
        "ts": utc_now(),
        "event": "tuple_done",
        "alpha": alpha,
        "seed": seed,
        "gen": gen,
        "path": path,
        f"D_code_path_{path}": kl_scalar,
        "n_tokens": n_tokens,
        "elapsed_sec": round(elapsed, 2),
        "dtype": dtype_str,
        "val_seed": val_seed,
        "val_subset_size": val_subset_size,
        "val_max_length": val_max_length,
        "ckpt_current": ckpt_current,
        "ckpt_ref": ckpt_ref,
        "caveats": caveats,
    }
    log_print(f"tuple done: α={alpha} seed={seed} gen={gen} path={path} "
              f"D_code={kl_scalar:.4e} n_tokens={n_tokens} elapsed={elapsed:.1f}s",
              log_file)
    return entry


# -----------------------------------------------------------------------------
# Resume-from-last-checkpoint logic (main run 之 watchdog hang kill 应对)
# -----------------------------------------------------------------------------
def load_done_tuples(jsonl_path: Path) -> set:
    """Read jsonl, return set of (alpha, seed, gen, path) tuples 之 已 done。"""
    done = set()
    if not jsonl_path.exists():
        return done
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("event") in ("tuple_done", "tuple_skipped"):
                done.add((
                    entry.get("alpha"),
                    entry.get("seed"),
                    entry.get("gen"),
                    entry.get("path"),
                ))
    return done


# -----------------------------------------------------------------------------
# Main entry
# -----------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="D-PPL 桥 verify launch script (D21)")
    p.add_argument("--mode", choices=["pilot", "main"], required=True)
    p.add_argument("--ckpt-root", required=True,
                   help="ckpt root (e.g., /home/amd/HEZIMENG/MaoField_static_backup_20260520/"
                        "experiments/exp018_cat/data/checkpoints_armb)")

    # pilot 之 single tuple args
    p.add_argument("--alpha", type=float, default=None, help="(pilot) single alpha")
    p.add_argument("--seed", type=int, default=None, help="(pilot) single seed")
    p.add_argument("--gen", type=int, default=None, help="(pilot) single gen")

    # main 之 list args
    p.add_argument("--alphas", type=str, default=None,
                   help="(main) comma-separated alphas, e.g., 0.0,10.0")
    p.add_argument("--seeds", type=str, default=None,
                   help="(main) comma-separated seeds, e.g., 1,2,3,4")
    p.add_argument("--gens", type=str, default=None,
                   help="(main) comma-separated gens, e.g., 0,1,...,9")

    # 共用
    p.add_argument("--paths", type=str, default="B,C",
                   help="comma-separated paths in {B, C}")
    p.add_argument("--val-seed", type=int, default=None,
                   help="val batch seed (default = chain seed)")
    p.add_argument("--val-subset-size", type=int, default=256)
    p.add_argument("--val-max-length", type=int, default=64)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--dtype", choices=["fp32", "fp16"], default="fp32")

    p.add_argument("--output-jsonl", type=Path, required=True)
    p.add_argument("--log-file", type=Path, default=None)

    # main 之 rsync push
    p.add_argument("--rsync-push-after-each-tuple", action="store_true",
                   help="(main) 每 tuple done 之后 rsync push 7B13")
    p.add_argument("--rsync-target", type=str, default=None,
                   help="(main) rsync target, e.g., amd@192.168.31.36:/path/")

    return p.parse_args()


def build_tuple_list(args) -> list:
    """Build tuples list per mode."""
    paths = [p.strip() for p in args.paths.split(",") if p.strip()]
    for p in paths:
        assert p in ("B", "C"), f"unknown path {p}, 仅 支持 B / C"

    if args.mode == "pilot":
        assert args.alpha is not None, "--alpha required for pilot"
        assert args.seed is not None, "--seed required for pilot"
        assert args.gen is not None, "--gen required for pilot"
        tuples = [(args.alpha, args.seed, args.gen, p) for p in paths]
    else:  # main
        assert args.alphas, "--alphas required for main"
        assert args.seeds, "--seeds required for main"
        assert args.gens, "--gens required for main"
        alphas = [float(a) for a in args.alphas.split(",")]
        seeds = [int(s) for s in args.seeds.split(",")]
        gens = [int(g) for g in args.gens.split(",")]
        tuples = [
            (a, s, g, p)
            for a in alphas
            for s in seeds
            for g in gens
            for p in paths
        ]
    return tuples


def main():
    args = parse_args()
    log_file = args.log_file
    output_jsonl = args.output_jsonl

    log_print(f"=== D-PPL bridge launch script start ===", log_file)
    log_print(f"mode: {args.mode}", log_file)
    log_print(f"D-1 binding: zero-context, 不 inflate, 不 declare P0★-F close", log_file)
    log_print(f"args: {vars(args)}", log_file)

    # 真实今日日期 binary verify (D-1 纪律 5)
    log_print(f"real date verify: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", log_file)

    # Build tuples list
    tuples = build_tuple_list(args)
    log_print(f"total tuples: {len(tuples)}", log_file)

    # Resume logic (main only)
    if args.mode == "main":
        done_set = load_done_tuples(output_jsonl)
        log_print(f"resume from output_jsonl: {len(done_set)} done tuples", log_file)
        tuples = [t for t in tuples if t not in done_set]
        log_print(f"remaining tuples: {len(tuples)}", log_file)

    # Write run_start event
    write_jsonl(output_jsonl, {
        "ts": utc_now(),
        "event": "run_start",
        "mode": args.mode,
        "args": vars(args),
        "n_tuples_total": len(tuples) + (len(load_done_tuples(output_jsonl)) if args.mode == "main" else 0),
        "n_tuples_remaining": len(tuples),
    })

    # default val_seed = chain seed (per pilot 之 single seed OR main 之 per-tuple seed)
    val_seed_arg = args.val_seed

    # Iterate tuples
    n_done = 0
    n_error = 0
    for tup in tuples:
        alpha, seed, gen, path = tup

        # val_seed = chain seed (per tuple), 除非 user override
        val_seed = val_seed_arg if val_seed_arg is not None else seed

        # Compute
        try:
            entry = compute_one_tuple(
                ckpt_root=args.ckpt_root,
                alpha=alpha,
                seed=seed,
                gen=gen,
                path=path,
                val_seed=val_seed,
                val_subset_size=args.val_subset_size,
                val_max_length=args.val_max_length,
                batch_size=args.batch_size,
                dtype_str=args.dtype,
                log_file=log_file,
            )
        except Exception as e:
            entry = {
                "ts": utc_now(),
                "event": "tuple_error",
                "alpha": alpha, "seed": seed, "gen": gen, "path": path,
                "error": f"compute_one_tuple raised: {e}",
                "traceback": traceback.format_exc()[:2000],
            }
            log_print(f"tuple error: {entry['error']}", log_file)

        write_jsonl(output_jsonl, entry)

        if entry.get("event") == "tuple_done":
            n_done += 1
        elif entry.get("event") == "tuple_error":
            n_error += 1

        # rsync push after each tuple (main 之 idempotent)
        if args.rsync_push_after_each_tuple and args.rsync_target:
            rsync_push(str(output_jsonl), args.rsync_target, log_file)
            if log_file is not None:
                rsync_push(str(log_file), args.rsync_target, log_file)

    # Write run_done event
    write_jsonl(output_jsonl, {
        "ts": utc_now(),
        "event": "run_done",
        "n_tuples_done_this_session": n_done,
        "n_tuples_error_this_session": n_error,
    })

    log_print(f"=== D-PPL bridge launch script done ===", log_file)
    log_print(f"n_done: {n_done}, n_error: {n_error}", log_file)

    # Final rsync push
    if args.rsync_push_after_each_tuple and args.rsync_target:
        rsync_push(str(output_jsonl), args.rsync_target, log_file)
        if log_file is not None:
            rsync_push(str(log_file), args.rsync_target, log_file)

    sys.exit(0 if n_error == 0 else 1)


if __name__ == "__main__":
    main()
