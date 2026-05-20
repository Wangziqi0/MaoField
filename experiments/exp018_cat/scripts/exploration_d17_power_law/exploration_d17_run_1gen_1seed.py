"""
exploration_d17_run_1gen_1seed.py — D-2 代码线 third wave (D17 = 2026-05-17)

throwaway exploration prototype: OPT-125M 1 gen 1 seed sanity check.

scope (binary)
--------------
- model: facebook/opt-125m (Phase 1 model, paper v8 §4 之 baseline)
- seed: 99 (不冲突 v1.0 release seed 0-4/42/1/2/3/4)
- α 二组: 0.0 (baseline, contradiction loss 关闭) + 10.0 (power-law variant)
- generations: 1 only (不 chain)
- block_size / batch / lr / dataset / config inherit from
  `archive/v1.0_release_20260516/configs/cat_arm_b.yaml`
- log per-step metric: test_ppl / train_loss / contradiction metrics (D_n / bar_D / T1/T2/T3)
- 不 multi-seed N≥4 (那是 D60+ paired comparison)

ballpark expected (binary 参 paper v8 §4.3 cite)
----------------------------------------------
- gen 0 test_ppl @ α=0 baseline: ~50-60 (Shumailov 2024 wikitext-2 OPT-125M strict-mirror reference)
- gen 0 test_ppl @ α=10 power-law: 期 same ballpark ±50% (因为 K=5 history buffer 在 gen 0 vacuous,
  power-law effect 大部分 step 退化为 cold-start identity, 接近 baseline 行为)
- 任何 NaN / OOM / cache miss → 标 [?] 失败 root cause, 不强行修

binding (D-1 五条 + prompt)
--------------------------
- 不动 v1.0 release archive 任何文件
- 不动 paper v8 final lock 任何文件
- N=1 indicative only, 不 establish framework effect, 不 statistical conclude
- 不 declare "signal found" / "structure 发现" / "framework α-effect 在 alternative form 成立"
- 标 [?] 任何 failure / unverifiable / GPU / cache 问题

执行 (本机 EPYC 7B13 503GB RAM CPU only)
---------------------------------------
- torch 2.11.0+cpu, cuda False, rocm None
- OPT-125M ~125M params × fp32 4 bytes = ~500MB, CPU 跑得动
- block_size=64 batch=128 → train step 数 (wikitext-2 train ~36k blocks): ~36000/128 = 281 steps/epoch
- CPU 单 epoch ~30-60 min estimate, 超 30 min budget → 必须 abbreviated: subset_size + epochs=1
  + per_device_train_batch_size 减到 8 + steps_cap 32 (smoke level, finite-vs-NaN check only)
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from datasets import load_dataset
from torch.utils.data import DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer

# 添加本目录到 sys.path 以 import exploration_d17_power_law_loss
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from exploration_d17_power_law_loss import (
    PowerLawContradictionConfig,
    PowerLawContradictionTracker,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("exp_d17_power_law")


def set_seed(seed: int) -> None:
    """统一 seed (torch + python random)."""
    import random as _random
    import numpy as _np
    _random.seed(seed)
    _np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    logger.info("set_seed: %d", seed)


def tokenize_and_block(dataset, tokenizer, block_size: int = 64, max_samples: int | None = None):
    """
    tokenize wikitext-2 + block into block_size chunks.

    简化版本 (v1.0 release data_pipeline 全功能太复杂, exploration scope 用 minimal subset):
    - 拼接 text → tokenize → 切 block_size chunks
    - return list of dict {input_ids, attention_mask, labels}
    """
    # 拼 text
    if max_samples is not None:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    # 过滤空行 + 拼成大 text
    texts = [t for t in dataset["text"] if t.strip()]
    big_text = "\n".join(texts)
    logger.info("dataset corpus size: %d chars from %d non-empty samples", len(big_text), len(texts))

    # tokenize
    enc = tokenizer(big_text, return_tensors=None, add_special_tokens=False)
    all_ids = enc["input_ids"]
    logger.info("total tokens: %d", len(all_ids))

    # 切 block_size chunks
    n_blocks = len(all_ids) // block_size
    blocks = []
    for i in range(n_blocks):
        chunk = all_ids[i * block_size:(i + 1) * block_size]
        blocks.append({
            "input_ids": torch.tensor(chunk, dtype=torch.long),
            "attention_mask": torch.ones(block_size, dtype=torch.long),
            "labels": torch.tensor(chunk, dtype=torch.long),
        })
    logger.info("blocked into %d chunks of size %d", len(blocks), block_size)
    return blocks


def collate_blocks(batch):
    """batch dict of tensors."""
    return {
        "input_ids": torch.stack([b["input_ids"] for b in batch]),
        "attention_mask": torch.stack([b["attention_mask"] for b in batch]),
        "labels": torch.stack([b["labels"] for b in batch]),
    }


def compute_test_ppl(model, test_blocks, device, max_eval_batches: int = 16) -> float:
    """简化 test perplexity 计算 (per-token CE 平均 exp)."""
    model.eval()
    loader = DataLoader(test_blocks, batch_size=8, shuffle=False, collate_fn=collate_blocks)
    total_loss = 0.0
    total_tokens = 0
    with torch.no_grad():
        for i, batch in enumerate(loader):
            if i >= max_eval_batches:
                break
            input_ids = batch["input_ids"].to(device)
            attn_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            out = model(input_ids=input_ids, attention_mask=attn_mask, labels=labels)
            n = attn_mask.sum().item()
            total_loss += out.loss.item() * n
            total_tokens += n
    if total_tokens == 0:
        return float("inf")
    avg_loss = total_loss / total_tokens
    ppl = math.exp(avg_loss) if avg_loss < 20 else float("inf")
    model.train()
    return ppl


def run_one_config(
    alpha: float,
    memory_form: str,
    seed: int,
    train_blocks,
    val_blocks,
    test_blocks,
    tokenizer,
    model_id: str = "facebook/opt-125m",
    n_steps: int = 32,
    batch_size: int = 8,
    lr: float = 2.0e-5,
    kl_update_every: int = 4,    # exploration 小 n_steps, 频次提高便于 surface
    log_every: int = 4,
    device: str = "cpu",
) -> dict:
    """
    跑一个 config (alpha + memory_form), 返回 ballpark metrics dict.

    binary log:
    - per-step train_loss (含 LM loss + α·contradiction loss 如果 α>0)
    - per-eval test_ppl (every log_every step + final)
    - contradiction metrics (D_n, bar_D, T1/T2/T3) 如果 alpha>0
    """
    set_seed(seed)
    logger.info(
        "[CONFIG] alpha=%.2f memory_form=%s seed=%d n_steps=%d batch_size=%d lr=%.1e kl_every=%d",
        alpha, memory_form, seed, n_steps, batch_size, lr, kl_update_every,
    )

    # load model fresh per config (binary: 隔离 config 间影响)
    logger.info("loading model %s ...", model_id)
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)
    model.to(device)
    logger.info("model loaded in %.1fs, on %s", time.time() - t0, device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    # contradiction tracker if alpha > 0
    tracker = None
    val_loader = None
    if alpha > 0:
        cfg = PowerLawContradictionConfig(
            memory_form=memory_form,
            power_law_alpha=1.0,
            power_law_K=5,
            kl_update_every=kl_update_every,
            beta_model=0.999,
            beta_kl=0.9,
            lambda_1=1.0, lambda_2=1.0, lambda_3=1.0,
            T_2_form="relu_dpp",
        )
        tracker = PowerLawContradictionTracker(cfg)
        tracker.init_ema_model(model)
        # val loader (cycle)
        val_loader = DataLoader(val_blocks, batch_size=8, shuffle=True, collate_fn=collate_blocks, drop_last=True)
        val_iter = iter(val_loader)

    # train loader
    train_loader = DataLoader(train_blocks, batch_size=batch_size, shuffle=True, collate_fn=collate_blocks, drop_last=True)
    train_iter = iter(train_loader)

    # initial test_ppl
    ppl_init = compute_test_ppl(model, test_blocks, device, max_eval_batches=8)
    logger.info("[STEP 0] initial test_ppl=%.3f", ppl_init)

    step_log = []
    contradiction_log = []

    model.train()
    for step in range(1, n_steps + 1):
        try:
            batch = next(train_iter)
        except StopIteration:
            train_iter = iter(train_loader)
            batch = next(train_iter)
        input_ids = batch["input_ids"].to(device)
        attn_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        out = model(input_ids=input_ids, attention_mask=attn_mask, labels=labels)
        lm_loss = out.loss

        # contradiction loss
        total_loss = lm_loss
        contra_metrics = None
        if alpha > 0 and step > 0 and step % kl_update_every == 0:
            try:
                vbatch = next(val_iter)
            except StopIteration:
                val_iter = iter(val_loader)
                vbatch = next(val_iter)
            vids = vbatch["input_ids"].to(device)
            vmask = vbatch["attention_mask"].to(device)
            try:
                contra_loss, contra_metrics = tracker.compute_loss(model, vids, vmask)
                total_loss = lm_loss + alpha * contra_loss
                contradiction_log.append({
                    "step": step,
                    "alpha": alpha,
                    "contra_loss": float(contra_loss.item()),
                    "metrics": contra_metrics,
                })
            except Exception as e:
                logger.warning("[STEP %d] contradiction loss compute FAILED: %s", step, e)

        total_loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        # EMA model update (mean teacher)
        if tracker is not None:
            tracker.update_ema_model(model)

        # log
        if step % log_every == 0 or step == n_steps:
            ppl_cur = compute_test_ppl(model, test_blocks, device, max_eval_batches=4)
            entry = {
                "step": step,
                "lm_loss": float(lm_loss.item()),
                "total_loss": float(total_loss.item()),
                "test_ppl": ppl_cur,
            }
            if contra_metrics is not None:
                entry["bar_D"] = contra_metrics["bar_D_used"]
                entry["D_n"] = contra_metrics["D_n"]
                entry["T3_memory"] = contra_metrics["T3_memory"]
                entry["history_len"] = contra_metrics["history_len"]
            logger.info(
                "[STEP %3d] lm_loss=%.4f total_loss=%.4f test_ppl=%.3f %s",
                step, entry["lm_loss"], entry["total_loss"], entry["test_ppl"],
                f"bar_D={entry.get('bar_D', 0):.4f} D_n={entry.get('D_n', 0):.4f}" if contra_metrics else "",
            )
            step_log.append(entry)

    # final eval
    ppl_final = compute_test_ppl(model, test_blocks, device, max_eval_batches=16)
    logger.info("[FINAL] alpha=%.2f memory_form=%s test_ppl_init=%.3f test_ppl_final=%.3f",
                alpha, memory_form, ppl_init, ppl_final)

    # cleanup
    del model
    if tracker is not None:
        del tracker

    return {
        "alpha": alpha,
        "memory_form": memory_form,
        "seed": seed,
        "n_steps": n_steps,
        "batch_size": batch_size,
        "lr": lr,
        "kl_update_every": kl_update_every,
        "test_ppl_init": ppl_init,
        "test_ppl_final": ppl_final,
        "step_log": step_log,
        "contradiction_log": contradiction_log,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, default="facebook/opt-125m")
    parser.add_argument("--seed", type=int, default=99)
    parser.add_argument("--n_steps", type=int, default=32)        # 极小 exploration smoke
    parser.add_argument("--batch_size", type=int, default=8)      # CPU 友好
    parser.add_argument("--lr", type=float, default=2.0e-5)
    parser.add_argument("--kl_update_every", type=int, default=4)
    parser.add_argument("--log_every", type=int, default=4)
    parser.add_argument("--max_train_samples", type=int, default=2000)   # subset, CPU 友好
    parser.add_argument("--max_val_samples", type=int, default=256)
    parser.add_argument("--max_test_samples", type=int, default=512)
    parser.add_argument("--output_jsonl", type=str,
                        default=str(THIS_DIR / "exploration_d17_results.jsonl"))
    parser.add_argument("--alpha_baseline", type=float, default=0.0)
    parser.add_argument("--alpha_powerlaw", type=float, default=10.0)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("=== exploration D17 power-law sanity check, device=%s ===", device)
    logger.info("torch=%s cuda_avail=%s", torch.__version__, torch.cuda.is_available())

    # load tokenizer + dataset (one-time)
    t0 = time.time()
    logger.info("loading tokenizer %s ...", args.model_id)
    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    logger.info("tokenizer loaded in %.1fs", time.time() - t0)

    t0 = time.time()
    logger.info("loading wikitext-2-raw-v1 ...")
    ds = load_dataset("wikitext", "wikitext-2-raw-v1")
    logger.info("dataset loaded in %.1fs (train=%d val=%d test=%d)",
                time.time() - t0, len(ds["train"]), len(ds["validation"]), len(ds["test"]))

    # tokenize + block
    logger.info("tokenize + block train (max_samples=%d) ...", args.max_train_samples)
    train_blocks = tokenize_and_block(ds["train"], tokenizer, block_size=64, max_samples=args.max_train_samples)
    logger.info("tokenize + block val (max_samples=%d) ...", args.max_val_samples)
    val_blocks = tokenize_and_block(ds["validation"], tokenizer, block_size=64, max_samples=args.max_val_samples)
    logger.info("tokenize + block test (max_samples=%d) ...", args.max_test_samples)
    test_blocks = tokenize_and_block(ds["test"], tokenizer, block_size=64, max_samples=args.max_test_samples)

    results = []

    # ============================================================
    # Run 1: alpha=0 baseline (contradiction loss off)
    # ============================================================
    logger.info("\n=== Run 1/2: alpha=%.2f (baseline, contradiction off) ===", args.alpha_baseline)
    r1 = run_one_config(
        alpha=args.alpha_baseline,
        memory_form="power_law",     # ignored when alpha=0
        seed=args.seed,
        train_blocks=train_blocks,
        val_blocks=val_blocks,
        test_blocks=test_blocks,
        tokenizer=tokenizer,
        model_id=args.model_id,
        n_steps=args.n_steps,
        batch_size=args.batch_size,
        lr=args.lr,
        kl_update_every=args.kl_update_every,
        log_every=args.log_every,
        device=device,
    )
    results.append(r1)

    # ============================================================
    # Run 2: alpha=10 power-law alternative form
    # ============================================================
    logger.info("\n=== Run 2/2: alpha=%.2f (power-law alternative form, K=5 α=1.0) ===", args.alpha_powerlaw)
    r2 = run_one_config(
        alpha=args.alpha_powerlaw,
        memory_form="power_law",
        seed=args.seed,
        train_blocks=train_blocks,
        val_blocks=val_blocks,
        test_blocks=test_blocks,
        tokenizer=tokenizer,
        model_id=args.model_id,
        n_steps=args.n_steps,
        batch_size=args.batch_size,
        lr=args.lr,
        kl_update_every=args.kl_update_every,
        log_every=args.log_every,
        device=device,
    )
    results.append(r2)

    # save results
    with open(args.output_jsonl, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    logger.info("results saved to %s", args.output_jsonl)

    # summary
    logger.info("\n=== SUMMARY (binary, ballpark only — N=1 indicative not verification) ===")
    for r in results:
        logger.info(
            "  alpha=%.2f memory_form=%s: test_ppl_init=%.3f → test_ppl_final=%.3f",
            r["alpha"], r["memory_form"], r["test_ppl_init"], r["test_ppl_final"],
        )

    delta = r2["test_ppl_final"] - r1["test_ppl_final"]
    logger.info(
        "\n  delta (alpha=%.0f power-law - alpha=%.0f baseline) test_ppl_final = %+.3f",
        args.alpha_powerlaw, args.alpha_baseline, delta,
    )
    logger.info(
        "  [BINARY SANITY] both finite? %s; in baseline ±50%%? %s",
        all(math.isfinite(r["test_ppl_final"]) for r in results),
        all(abs(r["test_ppl_final"] - r1["test_ppl_final"]) / max(r1["test_ppl_final"], 1) < 0.5 for r in results),
    )
    logger.info(
        "  [DISCLAIMER] N=1 gen 1 seed sanity check, NOT a verification. "
        "Does NOT establish framework α-effect in power-law form."
    )


if __name__ == "__main__":
    main()
