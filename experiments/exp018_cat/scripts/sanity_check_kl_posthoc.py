#!/usr/bin/env python3
"""
sanity_check_kl_posthoc.py — candidate (b) KL signal post-hoc 验证

binding: Protocol A 设计 bug (synthetic over-fit fine-tune ≠ self-iteration collapse).
正确 sanity 是用已存 strict-mirror baseline 10 个 generation checkpoint 做 post-hoc 分析:

D_n = KL(p_θ_n || p_θ_{n-1}) on wikitext-2 val 256 句

期望 (collapse signature):
- D_n 在 gen 0→1 大 (model 受 synthetic data 强污染), 然后逐步降到 plateau
- D_n series 与 perplexity series correlation ≥ 0.5 (collapse 强度 indicator)
- D'_n / D''_n 三项分解有 non-trivial 信号

PASS criterion (修正):
- D_n series 平均 ≥ 0.5 nat (KL 真有非平凡 dynamic range)
- D_n 与 collapse intensity (gen ppl - gen0 ppl) correlation |r| ≥ 0.5
- D_n[0]/D_n.min() ≥ 5 (range ≥ 5×)

跑法:
  python sanity_check_kl_posthoc.py \\
    --checkpoint-base data/checkpoints_official/no_preserve_seed42 \\
    --baseline-jsonl logs/shumailov_no_preserve_seed42_20260508_092730.jsonl
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import torch
import torch.nn.functional as F
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def load_val_subset(tokenizer, n_examples: int = 256, max_length: int = 64):
    ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="validation")
    ds = ds.filter(lambda x: len(x["text"].strip()) >= 30)
    if len(ds) > n_examples:
        ds = ds.shuffle(seed=42).select(range(n_examples))
    encoded = []
    for ex in ds:
        enc = tokenizer(ex["text"], truncation=True, max_length=max_length, padding=False, return_tensors="pt")
        if enc["input_ids"].shape[1] >= 8:
            encoded.append(enc)
    return encoded


def compute_kl_pair(model_p, model_q, val_encoded, device: str):
    """KL(q || p) mode-covering on val_encoded."""
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
            q = log_q.exp()
            kl_pos = (q * (log_q - log_p)).sum(dim=-1)
            valid = mask[:, 1:].float()
            total_kl += (kl_pos * valid).sum().item()
            total_tokens += valid.sum().item()
    return total_kl / max(total_tokens, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-base", type=str,
                        default="data/checkpoints_official/no_preserve_seed42")
    parser.add_argument("--baseline-jsonl", type=str,
                        default="logs/shumailov_no_preserve_seed42_20260508_092730.jsonl")
    parser.add_argument("--n-generations", type=int, default=10)
    parser.add_argument("--tokenizer-id", type=str, default="facebook/opt-125m")
    parser.add_argument("--output-base", type=str, default="logs")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    output_dir = Path(args.output_base)
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    val_encoded = load_val_subset(tokenizer, n_examples=256)
    logger.info("val 加载 %d 句", len(val_encoded))

    # 加载 baseline ppl curve
    baseline_records = []
    with open(args.baseline_jsonl) as f:
        for line in f:
            line = line.strip()
            if line:
                baseline_records.append(json.loads(line))
    gen_ppl = {}
    for r in baseline_records:
        if r.get("stage") == "generation_done":
            gen_ppl[r["generation"]] = r.get("test_perplexity", float("inf"))
    logger.info("baseline ppl curve: %s", {k: f"{v:.2f}" if isinstance(v, float) and not np.isinf(v) else "inf"
                                            for k, v in gen_ppl.items()})

    # 算 D_n = KL(p_θ_n || p_θ_{n-1}) for n=1..9
    D_series = []
    base = Path(args.checkpoint_base)
    prev_model = None
    cur_model = None

    for n in range(args.n_generations):
        ckpt_path = base / f"generation_{n}"
        if not ckpt_path.exists():
            logger.warning("missing %s", ckpt_path)
            break
        logger.info("加载 generation_%d from %s", n, ckpt_path)
        # 释放前一个 model
        if prev_model is not None:
            del prev_model
            torch.cuda.empty_cache()
        prev_model = cur_model
        cur_model = AutoModelForCausalLM.from_pretrained(str(ckpt_path), torch_dtype=torch.float32).to(device)
        cur_model.eval()

        if prev_model is not None:
            kl = compute_kl_pair(cur_model, prev_model, val_encoded, device)
            D_series.append({"n": n, "D_n": kl, "test_ppl": gen_ppl.get(n)})
            logger.info("  D_%d = KL(p_θ_%d || p_θ_%d) = %.6f, test_ppl=%.2f",
                        n, n, n-1, kl, gen_ppl.get(n, -1))

    if len(D_series) < 3:
        logger.error("D_series too short, need ≥ 3 generations")
        return 2

    # 分析
    D_values = np.array([d["D_n"] for d in D_series])
    ppl_values = np.array([d["test_ppl"] if d["test_ppl"] is not None and not np.isinf(d["test_ppl"]) else np.nan
                           for d in D_series])

    D_mean = float(D_values.mean())
    D_std = float(D_values.std())
    D_max_min_ratio = float(D_values.max() / max(D_values.min(), 1e-9))

    # collapse intensity = ppl_n - ppl_0
    ppl_0 = gen_ppl.get(0, 36.35)
    collapse_intensity = ppl_values - ppl_0
    valid_mask = ~np.isnan(collapse_intensity)
    if valid_mask.sum() >= 3:
        correlation_with_collapse = float(np.corrcoef(D_values[valid_mask], collapse_intensity[valid_mask])[0, 1])
    else:
        correlation_with_collapse = 0.0

    pass_dynamic_range = D_mean >= 0.5 and D_max_min_ratio >= 5.0
    pass_correlation = abs(correlation_with_collapse) >= 0.5
    verdict_pass = pass_dynamic_range and pass_correlation

    logger.info("=" * 60)
    logger.info("Post-hoc KL sanity check 结果:")
    logger.info("  D_n series: min=%.4f max=%.4f mean=%.4f std=%.4f", D_values.min(), D_values.max(), D_mean, D_std)
    logger.info("  D_max/D_min ratio = %.2f (≥5.0 pass)", D_max_min_ratio)
    logger.info("  D_mean = %.4f nat (≥0.5 pass)", D_mean)
    logger.info("  D_n vs collapse intensity correlation = %.4f (|r|≥0.5 pass)", correlation_with_collapse)
    logger.info("  binary verdict: %s", "PASS ✓" if verdict_pass else "FAIL ✗")
    logger.info("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"sanity_check_kl_posthoc_{timestamp}.json"
    record = {
        "task": "candidate (b) KL post-hoc sanity check on strict-mirror baseline",
        "checkpoint_base": str(base),
        "baseline_jsonl": args.baseline_jsonl,
        "n_generations_analyzed": len(D_series),
        "D_series": D_series,
        "D_mean": D_mean,
        "D_std": D_std,
        "D_max_min_ratio": D_max_min_ratio,
        "correlation_with_collapse": correlation_with_collapse,
        "pass_dynamic_range": bool(pass_dynamic_range),
        "pass_correlation": bool(pass_correlation),
        "verdict_pass": bool(verdict_pass),
    }
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    logger.info("json 落盘 %s", json_path)

    return 0 if verdict_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
