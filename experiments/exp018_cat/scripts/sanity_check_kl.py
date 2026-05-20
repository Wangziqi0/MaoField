#!/usr/bin/env python3
"""
sanity_check_kl.py — candidate (b) KL signal binary gate

binding (数学教授 sub-agent §4): candidate (b) KL 二阶差分 + EMA fallback 必先验证
KL signal 在 frozen base LM 上真有 collapse-related discriminative power.

Protocol A: Synthetic Collapse Trajectory Check
- frozen θ_0, 在 wikitext-2 train (200 句) 上做人为过拟合 fine-tune
  (lr=1e-3, 10× normal, 100 step, batch 4)
- 每 5 step 算 D_n = KL(p_θ_n || p_θ_{n-5}) on wikitext-2 valid 256 句
- 同时 measure perplexity on val
- Pass: D_n 总变化 ≥ 5× 初始 fluctuation + 与 ppl correlation r > 0.7

Protocol B: Random Perturbation Sensitivity
- frozen θ_0
- θ_ε = θ_0 + ε * ξ, ξ ~ N(0, I), ε ∈ {1e-4, 1e-3, 1e-2, 1e-1}
- D(ε) = KL(p_θ_ε || p_θ_0) on val 256 句
- Pass: log D vs log ε 线性 fit slope ∈ [1.7, 2.3] (Fisher 二次预测 slope=2)

双 Protocol pass → candidate (b) viable, 可作 main session 主 3 arm 实验 training loss
单 Protocol fail → candidate (b) 同构度下调 5-10pt; 双 fail → fallback candidate (d) monitoring

跑法:
  python sanity_check_kl.py --model facebook/opt-125m
  python sanity_check_kl.py --model gpt2

需要: HF_ENDPOINT=https://hf-mirror.com
"""
from __future__ import annotations

import argparse
import json
import logging
import time
import copy
from pathlib import Path
from datetime import datetime

import numpy as np
import torch
import torch.nn.functional as F
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def load_val_subset(tokenizer, n_examples: int = 256, max_length: int = 64):
    """加载 wikitext-2 valid 子集 + tokenize."""
    ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
    # 过滤短句
    ds = ds.filter(lambda x: len(x["text"].strip()) >= 30)
    if len(ds) > n_examples:
        ds = ds.shuffle(seed=42).select(range(n_examples))
    encoded = []
    for ex in ds:
        enc = tokenizer(ex["text"], truncation=True, max_length=max_length, padding=False, return_tensors="pt")
        if enc["input_ids"].shape[1] >= 8:
            encoded.append(enc)
    return encoded


def compute_kl_on_val(model_p, model_q, val_encoded, device: str, kl_direction: str = "q_to_p"):
    """
    算 model_p vs model_q 在 val_encoded 上的平均 next-token KL.

    kl_direction:
      - "p_to_q": KL(p || q) mode-seeking (用于 forward training loss)
      - "q_to_p": KL(q || p) mode-covering, 对 collapse 更敏感 (推荐 sanity check 用)
    """
    model_p.eval()
    model_q.eval()
    total_kl = 0.0
    total_tokens = 0
    with torch.no_grad():
        for enc in val_encoded:
            ids = enc["input_ids"].to(device)
            mask = enc["attention_mask"].to(device)
            logits_p = model_p(ids, attention_mask=mask).logits
            logits_q = model_q(ids, attention_mask=mask).logits
            log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
            log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)
            if kl_direction == "p_to_q":
                p = log_p.exp()
                kl_pos = (p * (log_p - log_q)).sum(dim=-1)  # [1, T-1]
            elif kl_direction == "q_to_p":
                q = log_q.exp()
                kl_pos = (q * (log_q - log_p)).sum(dim=-1)
            else:
                raise ValueError(f"Unknown kl_direction {kl_direction}")
            valid = mask[:, 1:].float()
            total_kl += (kl_pos * valid).sum().item()
            total_tokens += valid.sum().item()
    return total_kl / max(total_tokens, 1)


def compute_perplexity(model, val_encoded, device: str):
    """算 model 在 val_encoded 上的 perplexity."""
    model.eval()
    total_nll = 0.0
    total_tokens = 0
    with torch.no_grad():
        for enc in val_encoded:
            ids = enc["input_ids"].to(device)
            mask = enc["attention_mask"].to(device)
            outputs = model(ids, attention_mask=mask, labels=ids)
            seq_len = mask.sum().item()
            total_nll += outputs.loss.item() * (seq_len - 1)
            total_tokens += seq_len - 1
    return float(np.exp(total_nll / max(total_tokens, 1)))


def protocol_a_synthetic_collapse(model_id: str, device: str, output_dir: Path):
    """Protocol A: 人为过拟合 fine-tune 看 D_n 是否 monotone 上升 + 与 ppl correlation."""
    logger.info("=" * 60)
    logger.info("Protocol A: Synthetic Collapse Trajectory Check on %s", model_id)
    logger.info("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    val_encoded = load_val_subset(tokenizer, n_examples=256)
    logger.info("val set 加载 %d 句", len(val_encoded))

    # 加载 train 子集（200 句作 over-fit 数据）
    train_ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    train_ds = train_ds.filter(lambda x: len(x["text"].strip()) >= 30).shuffle(seed=42).select(range(200))
    train_encoded = []
    for ex in train_ds:
        enc = tokenizer(ex["text"], truncation=True, max_length=64, padding="max_length", return_tensors="pt")
        train_encoded.append(enc)

    # 加载 model + 保留 reference checkpoint
    logger.info("加载 %s", model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to(device)
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)  # 10× normal lr 故意 over-fit

    # 保留早期 checkpoint 作 reference (D_n = KL(p_θ_n || p_θ_{n-5}))
    snapshots = {}
    snapshots[0] = copy.deepcopy(model).eval()

    # baseline measurements
    initial_ppl = compute_perplexity(model, val_encoded, device)
    logger.info("initial perplexity: %.4f", initial_ppl)

    # fine-tune 100 step, 每 5 step 测 D_n + ppl
    history = {"step": [0], "ppl": [initial_ppl], "kl_to_ref5": [0.0]}
    batch_size = 4
    n_steps = 100
    measure_every = 5
    t0 = time.time()

    for step in range(1, n_steps + 1):
        batch_idx = (step - 1) % len(train_encoded)
        batch_end = min(batch_idx + batch_size, len(train_encoded))
        batch = train_encoded[batch_idx:batch_end]
        if not batch:
            continue
        ids_list = [b["input_ids"].to(device) for b in batch]
        mask_list = [b["attention_mask"].to(device) for b in batch]
        ids = torch.cat(ids_list, dim=0)
        mask = torch.cat(mask_list, dim=0)
        labels = ids.clone()
        labels[mask == 0] = -100

        model.train()
        outputs = model(ids, attention_mask=mask, labels=labels)
        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % measure_every == 0:
            # D_n 用 5 step 前的 snapshot 作 reference (延迟 5 step)
            ref_step = max(0, step - 5)
            if ref_step not in snapshots and step > 5:
                # 5 step 前应该有 snapshot 但没有, skip
                pass
            ref_model = snapshots.get(ref_step, snapshots[0])
            kl_now = compute_kl_on_val(model, ref_model, val_encoded, device, kl_direction="q_to_p")
            ppl_now = compute_perplexity(model, val_encoded, device)
            history["step"].append(step)
            history["ppl"].append(ppl_now)
            history["kl_to_ref5"].append(kl_now)
            logger.info("step=%d ppl=%.4f KL_to_ref5=%.6f", step, ppl_now, kl_now)
            # 每 5 step 保存 snapshot
            snapshots[step] = copy.deepcopy(model).eval()
            # 限制 snapshot 数量（保留最近 3 个）
            if len(snapshots) > 3:
                oldest = min(snapshots.keys())
                if oldest != 0:
                    del snapshots[oldest]

    elapsed = time.time() - t0
    logger.info("Protocol A 跑 %.1fs", elapsed)

    # 分析
    kl_values = np.array(history["kl_to_ref5"][1:])  # 排除初始 0
    ppl_values = np.array(history["ppl"][1:])
    initial_fluctuation = kl_values[:3].std() if len(kl_values) >= 3 else 0.001
    total_change = kl_values[-1] - kl_values[0] if len(kl_values) >= 2 else 0
    ratio_change_to_fluctuation = abs(total_change) / max(initial_fluctuation, 1e-9)

    if len(kl_values) > 3:
        correlation = np.corrcoef(kl_values, ppl_values)[0, 1]
    else:
        correlation = 0.0

    pass_change = ratio_change_to_fluctuation >= 5.0
    pass_correlation = correlation > 0.7
    pass_a = pass_change and pass_correlation

    logger.info("=" * 60)
    logger.info("Protocol A 结果:")
    logger.info("  KL[step=5] = %.6f", kl_values[0] if len(kl_values) else 0)
    logger.info("  KL[step=100] = %.6f", kl_values[-1] if len(kl_values) else 0)
    logger.info("  total change / initial fluctuation = %.2f (≥5.0 pass)", ratio_change_to_fluctuation)
    logger.info("  KL-ppl correlation = %.4f (>0.7 pass)", correlation)
    logger.info("  Protocol A: %s", "PASS ✓" if pass_a else "FAIL ✗")
    logger.info("=" * 60)

    return {
        "protocol": "A_synthetic_collapse",
        "model": model_id,
        "history": history,
        "ratio_change_to_fluctuation": float(ratio_change_to_fluctuation),
        "kl_ppl_correlation": float(correlation),
        "pass_change": bool(pass_change),
        "pass_correlation": bool(pass_correlation),
        "pass_protocol_a": bool(pass_a),
        "elapsed_seconds": elapsed,
    }


def protocol_b_random_perturbation(model_id: str, device: str, output_dir: Path):
    """Protocol B: 参数扰动 sensitivity, KL ∝ ε² Fisher 二阶预测."""
    logger.info("=" * 60)
    logger.info("Protocol B: Random Perturbation Sensitivity on %s", model_id)
    logger.info("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    val_encoded = load_val_subset(tokenizer, n_examples=256)
    logger.info("val set 加载 %d 句", len(val_encoded))

    logger.info("加载 %s (frozen)", model_id)
    model_ref = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to(device)
    model_ref.eval()

    # 拉一份 perturbed copy
    model_pert = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32).to(device)
    model_pert.eval()

    epsilons = [1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1]
    kl_values = []
    t0 = time.time()
    torch.manual_seed(42)

    # 生成统一的 random direction (不同 ε reuse 同一个 ξ)
    direction = []
    with torch.no_grad():
        for p in model_ref.parameters():
            direction.append(torch.randn_like(p))

    for eps in epsilons:
        # 重置 perturbed = ref + eps * direction
        with torch.no_grad():
            for p_pert, p_ref, d in zip(model_pert.parameters(), model_ref.parameters(), direction):
                p_pert.data.copy_(p_ref.data + eps * d)
        kl = compute_kl_on_val(model_pert, model_ref, val_encoded, device, kl_direction="q_to_p")
        kl_values.append(kl)
        logger.info("eps=%.4e  KL=%.6e", eps, kl)

    elapsed = time.time() - t0
    logger.info("Protocol B 跑 %.1fs", elapsed)

    # log-log fit slope
    log_eps = np.log(epsilons)
    log_kl = np.log(np.maximum(kl_values, 1e-12))
    if len(log_kl) >= 3 and np.isfinite(log_kl).all():
        slope, intercept, r_val, p_val, std_err = stats.linregress(log_eps, log_kl)
    else:
        slope, intercept, r_val, p_val = 0.0, 0.0, 0.0, 1.0

    pass_b = 1.7 <= slope <= 2.3 and r_val > 0.95

    logger.info("=" * 60)
    logger.info("Protocol B 结果:")
    logger.info("  log-log slope = %.3f (Fisher 二阶预测 = 2.0, pass [1.7, 2.3])", slope)
    logger.info("  R² = %.4f (>0.95 pass)", r_val ** 2)
    logger.info("  Protocol B: %s", "PASS ✓" if pass_b else "FAIL ✗")
    logger.info("=" * 60)

    return {
        "protocol": "B_random_perturbation",
        "model": model_id,
        "epsilons": epsilons,
        "kl_values": kl_values,
        "log_log_slope": float(slope),
        "log_log_r": float(r_val),
        "log_log_r_squared": float(r_val ** 2),
        "log_log_intercept": float(intercept),
        "pass_protocol_b": bool(pass_b),
        "elapsed_seconds": elapsed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="facebook/opt-125m")
    parser.add_argument("--output-base", type=str, default="logs")
    parser.add_argument("--protocols", type=str, default="A,B",
                        help="comma list of A,B")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("device=%s model=%s protocols=%s", device, args.model, args.protocols)

    output_dir = Path(args.output_base)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = args.model.replace("/", "_")

    results = {"model": args.model, "timestamp": timestamp, "device": device}

    if "A" in args.protocols:
        results["protocol_a"] = protocol_a_synthetic_collapse(args.model, device, output_dir)
    if "B" in args.protocols:
        results["protocol_b"] = protocol_b_random_perturbation(args.model, device, output_dir)

    # binary verdict
    pass_a = results.get("protocol_a", {}).get("pass_protocol_a", False) if "A" in args.protocols else None
    pass_b = results.get("protocol_b", {}).get("pass_protocol_b", False) if "B" in args.protocols else None

    if pass_a is not None and pass_b is not None:
        if pass_a and pass_b:
            verdict = "PASS_BOTH"
        elif pass_a or pass_b:
            verdict = "PASS_PARTIAL"
        else:
            verdict = "FAIL_BOTH"
    elif pass_a is not None:
        verdict = "PASS_A_ONLY" if pass_a else "FAIL_A_ONLY"
    elif pass_b is not None:
        verdict = "PASS_B_ONLY" if pass_b else "FAIL_B_ONLY"
    else:
        verdict = "NO_PROTOCOL_RUN"

    results["verdict"] = verdict
    logger.info("=" * 60)
    logger.info("=== FINAL VERDICT for %s: %s ===", args.model, verdict)
    logger.info("=" * 60)

    json_path = output_dir / f"sanity_check_kl_{safe_model}_{timestamp}.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info("json 落盘 %s", json_path)

    if verdict == "PASS_BOTH":
        return 0
    elif "PASS" in verdict:
        return 1
    else:
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
