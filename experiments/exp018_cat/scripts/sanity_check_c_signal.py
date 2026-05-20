#!/usr/bin/env python3
"""
SNLI sanity check — 验证 candidate (e) 的 c_i = -<u_i, v_i> 在 frozen OPT-125m / GPT-2 base
上是否真有 contradiction discriminative power (L3 漏洞验证).

binding: 数学教授 sub-agent §6 L3 — 如果 contradiction-pair vs entailment-pair 的 c_i 差距
< 1σ, candidate (e) 65% partial isomorphism 要降到 30%, 可能重选 candidate.

输出:
- logs/sanity_check_c_signal_<model>_<timestamp>.json — c_i 数据 + 统计 verdict
- figures/sanity_check_c_signal_<model>.png — histogram

跑法:
  python sanity_check_c_signal.py --model facebook/opt-125m
  python sanity_check_c_signal.py --model gpt2

需要: HF_ENDPOINT=https://hf-mirror.com (中国网络访问 HF)
"""
import argparse
import json
import logging
import time
from pathlib import Path
from datetime import datetime

import numpy as np
import torch
import torch.nn.functional as F
from datasets import load_dataset
from transformers import AutoModel, AutoTokenizer
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def embed_segment(model, tokenizer, text: str, device: str, max_length: int = 64):
    """对单段文本算 mean-pooled hidden state embedding (last layer)."""
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        padding=False,
    ).to(device)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    hidden = outputs.hidden_states[-1]  # [1, L, d]
    mask = inputs["attention_mask"].unsqueeze(-1).float()  # [1, L, 1]
    pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)  # [1, d]
    return F.normalize(pooled, dim=-1).squeeze(0)


def compute_c(model, tokenizer, premise: str, hypothesis: str, device: str):
    """算 c = -<u, v> for (premise, hypothesis) pair."""
    u = embed_segment(model, tokenizer, premise, device)
    v = embed_segment(model, tokenizer, hypothesis, device)
    return float(-(u * v).sum().item())


def main():
    parser = argparse.ArgumentParser(description="SNLI sanity check for candidate (e)")
    parser.add_argument("--model", type=str, default="facebook/opt-125m",
                        help="HF model id (默认 OPT-125m, Shumailov paper 用的同一 model)")
    parser.add_argument("--num-pairs", type=int, default=100,
                        help="每个 label 取多少对 (默认 100 contradiction + 100 entailment)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-base", type=str, default="logs",
                        help="json 输出目录")
    parser.add_argument("--figures-dir", type=str, default="figures")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info("device=%s model=%s num_pairs=%d", device, args.model, args.num_pairs)

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    logger.info("加载 SNLI val split...")
    snli = load_dataset("stanfordnlp/snli", split="validation")
    # SNLI label: 0=entailment, 1=neutral, 2=contradiction, -1=no consensus
    contra_examples = [x for x in snli if x["label"] == 2][:args.num_pairs]
    entail_examples = [x for x in snli if x["label"] == 0][:args.num_pairs]
    logger.info("contradiction=%d entailment=%d", len(contra_examples), len(entail_examples))

    if len(contra_examples) < 10 or len(entail_examples) < 10:
        logger.error("SNLI 样本不足 (need ≥10 each label), abort")
        return 1

    logger.info("加载 model %s + tokenizer (frozen, eval mode)", args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModel.from_pretrained(args.model, torch_dtype=torch.float32).to(device)
    model.eval()

    logger.info("计算 c_i (contradiction pairs)...")
    c_contra = []
    t0 = time.time()
    for i, ex in enumerate(contra_examples):
        c = compute_c(model, tokenizer, ex["premise"], ex["hypothesis"], device)
        c_contra.append(c)
        if (i + 1) % 20 == 0:
            logger.info("  contra %d/%d", i + 1, len(contra_examples))

    logger.info("计算 c_i (entailment pairs)...")
    c_entail = []
    for i, ex in enumerate(entail_examples):
        c = compute_c(model, tokenizer, ex["premise"], ex["hypothesis"], device)
        c_entail.append(c)
        if (i + 1) % 20 == 0:
            logger.info("  entail %d/%d", i + 1, len(entail_examples))

    elapsed = time.time() - t0
    logger.info("耗时 %.1fs (per pair %.2fs)", elapsed, elapsed / (len(c_contra) + len(c_entail)))

    # 统计
    c_contra = np.array(c_contra)
    c_entail = np.array(c_entail)
    mean_contra, std_contra = c_contra.mean(), c_contra.std()
    mean_entail, std_entail = c_entail.mean(), c_entail.std()
    pooled_std = np.sqrt((c_contra.var() + c_entail.var()) / 2)
    sigma_separation = (mean_contra - mean_entail) / pooled_std if pooled_std > 0 else 0.0
    t_stat, p_val = stats.ttest_ind(c_contra, c_entail, equal_var=False)
    cohens_d = (mean_contra - mean_entail) / pooled_std if pooled_std > 0 else 0.0

    # binary verdict (按数学教授 §6 L3)
    verdict_passed = sigma_separation >= 1.0
    isomorphism_estimate = "65%" if verdict_passed else "30%"

    logger.info("=" * 60)
    logger.info("SNLI sanity check 结果:")
    logger.info("  contradiction c_i: mean=%.4f std=%.4f n=%d", mean_contra, std_contra, len(c_contra))
    logger.info("  entailment c_i:    mean=%.4f std=%.4f n=%d", mean_entail, std_entail, len(c_entail))
    logger.info("  σ-separation: %.3f (≥1.0 通过)", sigma_separation)
    logger.info("  Cohen's d: %.3f (≥0.5 中等效应, ≥0.8 大效应)", cohens_d)
    logger.info("  Welch t-test: t=%.3f p=%.4e", t_stat, p_val)
    logger.info("  binary verdict: %s", "PASS ✓" if verdict_passed else "FAIL ✗")
    logger.info("  candidate (e) isomorphism: %s", isomorphism_estimate)
    logger.info("=" * 60)
    if verdict_passed:
        logger.info("可继续 implementation: contradiction_loss.py + train_one_generation.py")
    else:
        logger.info("⚠️  candidate (e) 在 %s 上没判别力", args.model)
        logger.info("    fallback: 重选 candidate (b) KL 二阶差分 + EMA history")

    # 落盘 json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = args.model.replace("/", "_")
    output_dir = Path(args.output_base)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"sanity_check_c_signal_{safe_model}_{timestamp}.json"
    record = {
        "task": "SNLI sanity check for candidate (e) c_i = -<u_i, v_i>",
        "binding": "数学教授 sub-agent §6 L3 漏洞验证",
        "model": args.model,
        "num_pairs": args.num_pairs,
        "seed": args.seed,
        "device": device,
        "elapsed_seconds": elapsed,
        "c_contradiction": {
            "mean": float(mean_contra),
            "std": float(std_contra),
            "n": len(c_contra),
            "values": c_contra.tolist(),
        },
        "c_entailment": {
            "mean": float(mean_entail),
            "std": float(std_entail),
            "n": len(c_entail),
            "values": c_entail.tolist(),
        },
        "sigma_separation": float(sigma_separation),
        "cohens_d": float(cohens_d),
        "welch_t_stat": float(t_stat),
        "welch_p_value": float(p_val),
        "verdict_passed": bool(verdict_passed),
        "verdict_threshold": "sigma_separation >= 1.0",
        "isomorphism_estimate": isomorphism_estimate,
        "next_action": (
            "可继续 implementation contradiction_loss.py" if verdict_passed
            else "fallback 重选 candidate (b) KL 二阶差分 + EMA history"
        ),
    }
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    logger.info("json 落盘 %s", json_path)

    # 画 histogram (matplotlib 不强制, 失败不影响 verdict)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        figures_dir = Path(args.figures_dir)
        figures_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        bins = np.linspace(min(c_contra.min(), c_entail.min()),
                           max(c_contra.max(), c_entail.max()), 30)
        ax.hist(c_entail, bins=bins, alpha=0.6, label=f"entailment (n={len(c_entail)})", color="#3b82f6")
        ax.hist(c_contra, bins=bins, alpha=0.6, label=f"contradiction (n={len(c_contra)})", color="#ef4444")
        ax.axvline(mean_entail, color="#1e40af", linestyle="--", label=f"entail mean {mean_entail:.3f}")
        ax.axvline(mean_contra, color="#991b1b", linestyle="--", label=f"contra mean {mean_contra:.3f}")
        ax.set_xlabel("$c_i = -\\langle u_i, v_i\\rangle$ (cosine of mean-pooled embeddings)")
        ax.set_ylabel("count")
        ax.set_title(
            f"SNLI sanity check: c_i discriminative power on {args.model}\n"
            f"σ-sep={sigma_separation:.2f}, Cohen's d={cohens_d:.2f}, "
            f"verdict={'PASS' if verdict_passed else 'FAIL'}"
        )
        ax.legend()
        fig.tight_layout()
        fig_path = figures_dir / f"sanity_check_c_signal_{safe_model}.png"
        fig.savefig(fig_path, dpi=120)
        logger.info("figure 落盘 %s", fig_path)
    except Exception as e:
        logger.warning("matplotlib 画图失败: %s (verdict 不受影响)", e)

    return 0 if verdict_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
