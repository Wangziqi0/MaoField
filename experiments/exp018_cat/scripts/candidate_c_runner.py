#!/usr/bin/env python3
"""
candidate_c_runner.py — Candidate C (D22) outer loop chain training runner

D-3 反映论 instantiate (D22 Linux 姐姐 DIRECTIVE_D22_CANDIDATE_C_AUTO_LAUNCH):
- N=6 seed × 3 α × 10 gen = 180 chain training run
- per gen 末尾 capture 4 axis multi-layer instrument (A1 PPL + A2 anisotropy +
  A3 attention 头熵 + A6 EMA L2 散度) → jsonl 之 raw 数字 only

binding 严守:
- D-1 五条纪律 + D-3.7 PI 主权 binding: 不 declare Pearson r / paradigm shift /
  P0★-F close / 严格度 tier — 仅 surface raw 数字
- D-1 纪律 1 占位符禁令: 任何 fail 之 axis = None (jsonl), 不 best-case inflate
- D-1 纪律 4 子协作者验证: per chain training run 之 rsync push 7B13 (第二认识通道)
- paper v8 cat_arm_b.yaml 严守不动 (block_size=64, batch_size=8, AdamW, lr=2e-5,
  fp16, 10 gen per seed, 5 epoch no_preserve)
- attn_implementation="eager" 之 train_one_generation.py line 102-108 之 explicit
  add (避 SDPA output_attentions=True silent fallback)

usage:
  # pre-flight self-test (CPU mode + tiny scope)
  python scripts/candidate_c_runner.py \\
      --pre-flight --device cpu \\
      --seeds 42 --alphas 10 --gens 2 \\
      --output-dir /tmp/dppl_bridge_verify/output/candidate_c_preflight

  # main run (GPU + full N=6 × α=3 × gen=10 = 180 chain run)
  python scripts/candidate_c_runner.py \\
      --seeds 42,1337,2024,7,137,271 \\
      --alphas 0,5,10 \\
      --gens 10 \\
      --output-dir /tmp/dppl_bridge_verify/output/candidate_c \\
      --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import torch

# add src/ to path
EXP_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = EXP_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from config import load_config, resolve_path, CATYamlConfig
from data_pipeline import (
    load_wikitext2,
    tokenize_and_block,
    build_mixed_generation_dataset as _build_mixed,
)
from train_one_generation import fine_tune_one_generation, CATConfig
from generate_synthetic import generate_synthetic_dataset
from metrics import compute_perplexity_on_dataset
from multi_layer_hook import MultiLayerHook, MultiLayerHookConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("candidate_c_runner")


# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
def utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rsync_push(src: str, dst: str, log_file: Optional[Path] = None) -> bool:
    """rsync push src → dst. 不 raise (避免 main 阻塞). 返 success bool."""
    cmd = ["rsync", "-avz", src, dst]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            logger.info("rsync push ✓: %s → %s", src, dst)
            return True
        else:
            logger.warning("rsync push ✗ rc=%d: %s", result.returncode, result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        logger.warning("rsync push timeout > 300 sec: %s", src)
        return False
    except Exception as e:
        logger.warning("rsync push exception: %s", e)
        return False


def parse_csv_int(s: str) -> list[int]:
    return [int(x.strip()) for x in s.split(",") if x.strip()]


def parse_csv_float(s: str) -> list[float]:
    return [float(x.strip()) for x in s.split(",") if x.strip()]


def load_done_set(jsonl_path: Path) -> set[tuple[int, float, int]]:
    """load (seed, alpha, gen) tuples from existing jsonl (resume)."""
    done: set[tuple[int, float, int]] = set()
    if not jsonl_path.exists():
        return done
    try:
        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("event") == "chain_gen_done":
                    s = rec.get("seed")
                    a = rec.get("alpha")
                    g = rec.get("gen")
                    if s is not None and a is not None and g is not None:
                        done.add((int(s), float(a), int(g)))
    except Exception as e:
        logger.warning("load_done_set 失败: %s", e)
    return done


# -----------------------------------------------------------------------------
# 单 chain (seed, α) 之 10 gen run
# -----------------------------------------------------------------------------
def run_one_chain(
    *,
    seed: int,
    alpha: float,
    n_gens: int,
    cfg,
    cat_yaml: CATYamlConfig,
    device: str,
    output_dir: Path,
    jsonl_path: Path,
    pre_flight: bool,
    train_blocks,
    val_blocks,
    test_blocks,
    tokenizer,
    hook: MultiLayerHook,
    done_set: set[tuple[int, float, int]],
    rsync_target: Optional[str],
    pre_flight_train_size: int,
    pre_flight_val_size: int,
    pre_flight_test_size: int,
) -> int:
    """跑 (seed, alpha) 之 0..n_gens-1 之 gen. 返 n_done."""
    n_done = 0

    # 单 chain output base
    chain_base = output_dir / f"checkpoints" / f"alpha{alpha}" / f"no_preserve_seed{seed}"
    chain_base.mkdir(parents=True, exist_ok=True)

    # condition (no_preserve)
    condition = next(c for c in cfg.self_iteration.conditions if c.name == "no_preserve")
    epochs_per_gen = condition.epochs_per_generation if not pre_flight else 1

    # build CATConfig (alpha=0 → CAT disabled)
    cat_cfg = CATConfig(
        enabled=alpha > 0,
        alpha=alpha,
        kl_update_every=cat_yaml.kl_update_every,
        val_subset_size=cat_yaml.val_subset_size,
        val_max_length=cat_yaml.val_max_length,
        beta_model=cat_yaml.beta_model,
        beta_kl=cat_yaml.beta_kl,
        lambda_1=cat_yaml.lambda_1,
        lambda_2=cat_yaml.lambda_2,
        lambda_3=cat_yaml.lambda_3,
        enable_grad_norm_monitor=cat_yaml.enable_grad_norm_monitor,
        T_2_form=getattr(cat_yaml, "T_2_form", "relu_dpp"),
        kl_history_K=getattr(cat_yaml, "kl_history_K", 1),
        m_eff=getattr(cat_yaml, "m_eff", 1.0),
    )

    # gen 0..n_gens-1
    gen0_dir = chain_base / "generation_0"

    for g in range(n_gens):
        if (seed, alpha, g) in done_set:
            logger.info("[resume] skip seed=%d alpha=%g gen=%d (已 done)", seed, alpha, g)
            continue

        gen_dir = chain_base / f"generation_{g}"
        prev_gen_dir = chain_base / f"generation_{g-1}" if g > 0 else None

        t_start = time.time()
        caveats: list[str] = []

        try:
            # --- prepare train_dataset 之 gen ---
            if g == 0:
                gen_train_ds = train_blocks
            else:
                # gen ≥ 1: synthetic from prev_gen
                try:
                    synth_ds = generate_synthetic_dataset(
                        model_path=str(prev_gen_dir),
                        tokenizer_id=cfg.model.hf_id,
                        real_train_blocks=train_blocks,
                        num_beams=cfg.generation.num_beams,
                        prompt_length=cfg.generation.prompt_length,
                        max_new_tokens=cfg.generation.max_new_tokens,
                        batch_size=(
                            cfg.generation.per_device_generation_batch_size
                            if not pre_flight else 4
                        ),
                        fp16=cfg.fine_tune.fp16 and device != "cpu",
                        repetition_penalty=cfg.generation.repetition_penalty,
                    )
                except Exception as e:
                    logger.warning("generate_synthetic failed seed=%d α=%g g=%d: %s",
                                   seed, alpha, g, e)
                    caveats.append(f"generate_synthetic_fail:{e}")
                    synth_ds = train_blocks.select(range(min(64, len(train_blocks))))

                if pre_flight:
                    synth_ds = synth_ds.select(range(min(pre_flight_train_size, len(synth_ds))))

                gen_train_ds = _build_mixed(
                    real_train=train_blocks,
                    synthetic_train=synth_ds,
                    original_fraction=condition.original_data_fraction,
                    seed=seed + g,
                )

            # --- fine_tune ---
            base_model_path = (
                cfg.model.hf_id if g == 0 else str(gen0_dir)
            )
            # gen 0 之 没 prior model → CAT disabled
            cat_for_this_gen = None if g == 0 else cat_cfg

            # pre_flight 之 fp16 在 CPU 不 work, 强制 False
            fp16_use = cfg.fine_tune.fp16 and device != "cpu"

            # batch size override 之 pre_flight
            bs_use = (
                cfg.fine_tune.per_device_train_batch_size
                if not pre_flight else min(4, cfg.fine_tune.per_device_train_batch_size)
            )

            result = fine_tune_one_generation(
                base_model_path=base_model_path,
                train_dataset=gen_train_ds,
                val_dataset=val_blocks,
                tokenizer_id=cfg.model.hf_id,
                output_dir=gen_dir,
                epochs=epochs_per_gen,
                learning_rate=cfg.fine_tune.learning_rate,
                per_device_train_batch_size=bs_use,
                gradient_accumulation_steps=cfg.fine_tune.gradient_accumulation_steps,
                weight_decay=cfg.fine_tune.weight_decay,
                warmup_ratio=cfg.fine_tune.warmup_ratio,
                lr_scheduler_type=cfg.fine_tune.lr_scheduler_type,
                fp16=fp16_use,
                gradient_checkpointing=cfg.fine_tune.gradient_checkpointing,
                seed=seed,
                logging_steps=cfg.fine_tune.logging_steps,
                cat_config=cat_for_this_gen,
            )
            val_loss = float(result.val_loss)
            a1_ppl = math.exp(val_loss) if (val_loss < 20 and math.isfinite(val_loss)) else float("inf")

            # --- multi-layer 4 axis capture (post fine-tune) ---
            # reload model from saved gen_dir 之 eval mode 之 attn_implementation=eager
            try:
                cap_model = AutoModelForCausalLM.from_pretrained(
                    str(gen_dir),
                    torch_dtype=torch.float32,
                    attn_implementation="eager",
                )
                cap_model.to(device).eval()
            except Exception as e:
                logger.warning("reload model fail seed=%d α=%g g=%d: %s",
                               seed, alpha, g, e)
                caveats.append(f"reload_model_fail:{e}")
                cap_model = None

            # A6 reframe: 之 cat_trainer ema_model 在 trainer destruct 后 已 inaccessible,
            # candidate C D22 之 first cycle 之 之 a6 reframe 为 "per-layer L2 drift from
            # gen 0 baseline" (paper v8 §3.5 之 D^code 之 retrospective form 之 per-layer
            # extension). gen 0 自己 之 reference vs itself = zero list, 之 之 honest.
            # gen ≥ 1 之 reference = reload gen0_dir 之 model.
            # honest disclose: 之 之 cat_trainer 内部 EMA state 之 measurement 之 future
            # enhancement candidate (D-1 纪律 5 错误 surface — 不 silent 修正).
            ema_model_for_a6 = None
            if g >= 1 and gen0_dir.exists():
                try:
                    ema_model_for_a6 = AutoModelForCausalLM.from_pretrained(
                        str(gen0_dir),
                        torch_dtype=torch.float32,
                        attn_implementation="eager",
                    )
                    ema_model_for_a6.to(device).eval()
                    caveats.append("a6_reframed_as_drift_from_gen0_baseline")
                except Exception as e:
                    logger.warning("reload gen0 for a6 fail: %s", e)
                    caveats.append(f"a6_reload_gen0_fail:{e}")
                    ema_model_for_a6 = None
            elif g == 0:
                caveats.append("a6_gen0_self_reference_zero_list_expected")

            # val subset 256 之 之 之 sample 之 之 之 之 hook 之 forward
            val_subset_size = (
                cat_yaml.val_subset_size if not pre_flight else min(16, len(val_blocks))
            )
            val_max_length = cat_yaml.val_max_length

            # 之 prepare val_input_ids + attention_mask
            val_subset = val_blocks.shuffle(seed=seed).select(
                range(min(val_subset_size, len(val_blocks)))
            )
            val_input_ids = torch.stack(
                [torch.tensor(b["input_ids"]) for b in val_subset]
            )
            val_attention_mask = torch.stack(
                [torch.tensor(b["attention_mask"]) for b in val_subset]
            )

            # 之 capture 之 batch by batch (avoid OOM)
            a2_acc: list[list[float]] = []
            a3_acc: list[list[list[float]]] = []
            a6_val: list[float] = [float("nan")] * 12
            n_tokens_eval = 0

            if cap_model is not None:
                bs_cap = 8 if not pre_flight else min(4, val_input_ids.size(0))
                for i in range(0, val_input_ids.size(0), bs_cap):
                    batch_ids = val_input_ids[i:i+bs_cap]
                    batch_mask = val_attention_mask[i:i+bs_cap]
                    try:
                        hook_cfg = MultiLayerHookConfig(
                            val_subset_size=val_subset_size,
                            val_max_length=val_max_length,
                            batch_size=bs_cap,
                            device=device,
                        )
                        local_hook = MultiLayerHook(hook_cfg)
                        out_dict = local_hook.capture_per_gen(
                            model=cap_model,
                            ema_model=ema_model_for_a6,
                            val_input_ids=batch_ids,
                            val_attention_mask=batch_mask,
                        )
                        a2_acc.append(out_dict["a2_anisotropy_per_layer"])
                        a3_acc.append(out_dict["a3_attn_entropy_per_layer_head"])
                        # a6 之 之 model-level, 不 batch-dependent, 仅 取 一次 之 之 之
                        if i == 0:
                            a6_val = out_dict["a6_ema_l2_per_layer"]
                        n_tokens_eval += int(batch_mask.sum().item())
                    except Exception as e:
                        logger.warning("hook capture fail batch %d: %s", i, e)
                        caveats.append(f"hook_capture_fail_batch_{i}:{e}")

            # 之 average a2 + a3 across batches
            def _mean_list_axis0(lst: list[list[float]]) -> list[float]:
                if not lst:
                    return [float("nan")] * 12
                arr = torch.tensor(lst, dtype=torch.float64)
                m = arr.mean(dim=0).tolist()
                return m

            def _mean_list_layer_head(lst: list[list[list[float]]]) -> list[list[float]]:
                if not lst:
                    return [[float("nan")] * 12 for _ in range(12)]
                arr = torch.tensor(lst, dtype=torch.float64)  # [B_chunks, 12, 12]
                m = arr.mean(dim=0).tolist()
                return m

            a2_mean = _mean_list_axis0(a2_acc)
            a3_mean = _mean_list_layer_head(a3_acc)

            # release cap_model + ema_model_for_a6
            del cap_model
            if ema_model_for_a6 is not None:
                del ema_model_for_a6
            if torch.cuda.is_available() and device != "cpu":
                torch.cuda.empty_cache()

            # --- write jsonl ---
            elapsed = time.time() - t_start
            n_tokens_train = (
                len(gen_train_ds) * cfg.dataset.block_size
                if gen_train_ds is not None else 0
            )

            entry = {
                "ts": utc_iso(),
                "event": "chain_gen_done",
                "seed": int(seed),
                "alpha": float(alpha),
                "gen": int(g),
                "a1_ppl": float(a1_ppl) if math.isfinite(a1_ppl) else None,
                "a2_anisotropy": a2_mean,
                "a3_attn_entropy": a3_mean,
                "a6_ema_divergence": a6_val,
                "val_loss": float(val_loss) if math.isfinite(val_loss) else None,
                "n_tokens_train": int(n_tokens_train),
                "n_tokens_eval": int(n_tokens_eval),
                "elapsed_sec": float(elapsed),
                "ckpt_path": str(gen_dir),
                "caveats": caveats,
            }

            with jsonl_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                f.flush()
            n_done += 1
            logger.info(
                "chain_gen_done seed=%d α=%g gen=%d a1_ppl=%.3f elapsed=%.1fs",
                seed, alpha, g, a1_ppl, elapsed
            )

            # rsync push (per gen)
            if rsync_target:
                rsync_push(str(jsonl_path), rsync_target)

        except Exception as e:
            tb = traceback.format_exc()
            logger.error("chain_gen_fail seed=%d α=%g g=%d: %s\n%s",
                         seed, alpha, g, e, tb)
            err_entry = {
                "ts": utc_iso(),
                "event": "chain_gen_fail",
                "seed": int(seed),
                "alpha": float(alpha),
                "gen": int(g),
                "error": str(e),
                "traceback": tb[:5000],
                "caveats": caveats + ["chain_gen_exception"],
            }
            with jsonl_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(err_entry, ensure_ascii=False) + "\n")
                f.flush()
            if rsync_target:
                rsync_push(str(jsonl_path), rsync_target)
            # pre-flight 之 fail 之 之 之 immediately escalate
            if pre_flight:
                raise

    return n_done


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Candidate C outer loop chain training runner")
    parser.add_argument("--seeds", type=str, default="42,1337,2024,7,137,271")
    parser.add_argument("--alphas", type=str, default="0,5,10")
    parser.add_argument("--gens", type=int, default=10)
    parser.add_argument("--config", type=str, default="configs/cat_arm_b.yaml")
    parser.add_argument("--output-dir", type=str,
                        default="/tmp/dppl_bridge_verify/output/candidate_c/")
    parser.add_argument("--rsync-target", type=str,
                        default="amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/candidate_c/")
    parser.add_argument("--no-rsync", action="store_true",
                        help="disable rsync push (debug)")
    parser.add_argument("--pre-flight", action="store_true",
                        help="tiny scope: 之 之 之 之 之 train/val/test truncate, epochs=1, batch_size=4")
    parser.add_argument("--device", type=str, default="cuda",
                        choices=["cuda", "cpu"])
    parser.add_argument("--resume", action="store_true",
                        help="skip 已 done (seed, alpha, gen) per output jsonl")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = output_dir / f"candidate_c_{timestamp}.jsonl"
    # 之 之 resume 之 之 之 之 之 latest jsonl
    if args.resume:
        existing = sorted(output_dir.glob("candidate_c_*.jsonl"))
        if existing:
            jsonl_path = existing[-1]
            logger.info(">>> RESUME: 用 existing jsonl=%s", jsonl_path)

    seeds = parse_csv_int(args.seeds)
    alphas = parse_csv_float(args.alphas)

    logger.info("=" * 60)
    logger.info("candidate_c_runner — D22 first cycle")
    logger.info("seeds=%s alphas=%s n_gens=%d device=%s pre_flight=%s",
                seeds, alphas, args.gens, args.device, args.pre_flight)
    logger.info("output_dir=%s", output_dir)
    logger.info("jsonl_path=%s", jsonl_path)
    logger.info("rsync_target=%s", args.rsync_target if not args.no_rsync else "(disabled)")
    logger.info("=" * 60)

    # load config
    cfg_path = resolve_path(args.config)
    cfg = load_config(cfg_path)
    if cfg.cat is None or not cfg.cat.enabled:
        logger.error("yaml cat section missing 或 enabled=false; abort")
        return 1
    cat_yaml = cfg.cat

    # device sanity
    if args.device == "cuda" and not torch.cuda.is_available():
        logger.error("--device cuda 之 但 torch.cuda.is_available()=False; abort")
        return 1
    device = args.device

    # load + tokenize dataset
    tokenizer = AutoTokenizer.from_pretrained(cfg.model.hf_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    raw_ds = load_wikitext2(
        hf_id=cfg.dataset.hf_id,
        hf_config=cfg.dataset.hf_config,
        cache_dir=resolve_path(cfg.dataset.cache_dir),
    )
    train_blocks = tokenize_and_block(raw_ds["train"], tokenizer, cfg.dataset.block_size)
    val_blocks = tokenize_and_block(raw_ds["validation"], tokenizer, cfg.dataset.block_size)
    test_blocks = tokenize_and_block(raw_ds["test"], tokenizer, cfg.dataset.block_size)

    # pre-flight 之 truncate
    pre_flight_train_size = 32
    pre_flight_val_size = 32
    pre_flight_test_size = 16
    if args.pre_flight:
        logger.info("pre-flight: 截 train→%d, val→%d, test→%d",
                    pre_flight_train_size, pre_flight_val_size, pre_flight_test_size)
        train_blocks = train_blocks.select(
            range(min(pre_flight_train_size, len(train_blocks))))
        val_blocks = val_blocks.select(
            range(min(pre_flight_val_size, len(val_blocks))))
        test_blocks = test_blocks.select(
            range(min(pre_flight_test_size, len(test_blocks))))

    # build hook (cfg-shared)
    hook_cfg = MultiLayerHookConfig(
        val_subset_size=cat_yaml.val_subset_size if not args.pre_flight else 16,
        val_max_length=cat_yaml.val_max_length,
        batch_size=8 if not args.pre_flight else 4,
        device=device,
    )
    hook = MultiLayerHook(hook_cfg)

    # resume done set
    done_set: set[tuple[int, float, int]] = set()
    if args.resume:
        done_set = load_done_set(jsonl_path)
        logger.info(">>> RESUME: %d (seed, α, gen) tuples 已 done, 之 skip", len(done_set))

    rsync_target = None if args.no_rsync else args.rsync_target

    # write run_start
    start_entry = {
        "ts": utc_iso(),
        "event": "run_start",
        "seeds": seeds,
        "alphas": alphas,
        "n_gens": args.gens,
        "device": device,
        "pre_flight": args.pre_flight,
        "config_path": str(cfg_path),
        "jsonl_path": str(jsonl_path),
        "rsync_target": rsync_target,
    }
    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(start_entry, ensure_ascii=False) + "\n")

    if rsync_target:
        rsync_push(str(jsonl_path), rsync_target)

    # outer loop
    total_done = 0
    total_target = len(seeds) * len(alphas) * args.gens

    for seed in seeds:
        for alpha in alphas:
            logger.info(">>> chain start seed=%d alpha=%g", seed, alpha)
            n_done = run_one_chain(
                seed=seed,
                alpha=alpha,
                n_gens=args.gens,
                cfg=cfg,
                cat_yaml=cat_yaml,
                device=device,
                output_dir=output_dir,
                jsonl_path=jsonl_path,
                pre_flight=args.pre_flight,
                train_blocks=train_blocks,
                val_blocks=val_blocks,
                test_blocks=test_blocks,
                tokenizer=tokenizer,
                hook=hook,
                done_set=done_set,
                rsync_target=rsync_target,
                pre_flight_train_size=pre_flight_train_size,
                pre_flight_val_size=pre_flight_val_size,
                pre_flight_test_size=pre_flight_test_size,
            )
            total_done += n_done

            # progress snapshot (per chain, 之 之 之 之 之 之 之 之 n_done % 10 之 之 之 之)
            if total_done > 0 and total_done % 10 == 0:
                snap_path = output_dir / f"progress_snapshot_{total_done}.md"
                with snap_path.open("w", encoding="utf-8") as f:
                    f.write(f"# candidate_c progress snapshot — n_done={total_done} / {total_target}\n\n")
                    f.write(f"timestamp: {utc_iso()}\n")
                    f.write(f"jsonl: {jsonl_path}\n")
                if rsync_target:
                    rsync_push(str(snap_path), rsync_target)

    # write run_end
    end_entry = {
        "ts": utc_iso(),
        "event": "run_end",
        "n_done": total_done,
        "n_target": total_target,
    }
    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(end_entry, ensure_ascii=False) + "\n")

    if rsync_target:
        rsync_push(str(jsonl_path), rsync_target)

    logger.info("=" * 60)
    logger.info("candidate_c_runner 完成: n_done=%d / n_target=%d", total_done, total_target)
    logger.info("jsonl=%s", jsonl_path)
    logger.info("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
