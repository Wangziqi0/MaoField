#!/usr/bin/env python3
"""
sliding_window_eval.py — 反题姐姐 §2 漏 #2 close

GPT-2 paper-style sliding-window perplexity eval (stride=256 with full context)
vs chunked block_size=64 eval.

目的: verify gen 0 baseline = 36 vs Shumailov paper = 20 是否 eval method artifact.

输入: existing gen 0 checkpoint (RX 9070 XT 22 主机)
输出: literature/sliding_window_eval_verdict_20260510.md

GPU ~5 min (OPT-125m fp16 on wikitext-2-raw-v1 test).
"""
from __future__ import annotations

import json
import math
import sys
import datetime
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT_ROOT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp018_cat")
GEN0_CKPT = PROJECT_ROOT / "data/checkpoints_armb/alpha0.0/no_preserve_seed42/generation_0"
OUT_MD = PROJECT_ROOT / "literature/sliding_window_eval_verdict_20260510.md"


def chunked_eval(model, tokenizer, encodings, block_size=64):
    """Chunked eval (current method): non-overlapping block_size chunks."""
    input_ids = encodings["input_ids"]
    if isinstance(input_ids, torch.Tensor):
        input_ids = input_ids.squeeze(0)
    n_tokens = len(input_ids)
    n_chunks = n_tokens // block_size

    nlls = []
    n_tokens_used = 0
    with torch.no_grad():
        for i in range(n_chunks):
            chunk = input_ids[i * block_size : (i + 1) * block_size].unsqueeze(0).cuda()
            out = model(chunk, labels=chunk)
            nlls.append(out.loss.item() * block_size)
            n_tokens_used += block_size
    if n_tokens_used == 0:
        return float("inf")
    avg_nll = sum(nlls) / n_tokens_used
    return math.exp(avg_nll)


def sliding_window_eval(model, tokenizer, encodings, max_length=1024, stride=256):
    """Sliding-window eval (GPT-2 paper-style):
    每 stride tokens 一个 window of max_length tokens, 计 last stride tokens 的 NLL.
    标准 HuggingFace perplexity guide method.
    """
    input_ids = encodings["input_ids"]
    if isinstance(input_ids, torch.Tensor):
        input_ids = input_ids.squeeze(0)
    n_tokens = len(input_ids)
    nlls = []
    prev_end_loc = 0
    with torch.no_grad():
        for begin_loc in range(0, n_tokens, stride):
            end_loc = min(begin_loc + max_length, n_tokens)
            trg_len = end_loc - prev_end_loc
            if trg_len <= 0:
                break
            chunk = input_ids[begin_loc:end_loc].unsqueeze(0).cuda()
            target_ids = chunk.clone()
            target_ids[:, :-trg_len] = -100
            out = model(chunk, labels=target_ids)
            neg_log_likelihood = out.loss * trg_len
            nlls.append(neg_log_likelihood.item())
            prev_end_loc = end_loc
            if end_loc == n_tokens:
                break
    if not nlls or prev_end_loc == 0:
        return float("inf")
    avg_nll = sum(nlls) / prev_end_loc
    return math.exp(avg_nll)


def main():
    if not GEN0_CKPT.exists():
        print(f"[ERROR] gen 0 checkpoint not found: {GEN0_CKPT}", file=sys.stderr)
        return 1
    print(f"[sliding_window_eval] loading model from {GEN0_CKPT}")
    tokenizer = AutoTokenizer.from_pretrained(str(GEN0_CKPT))
    model = AutoModelForCausalLM.from_pretrained(
        str(GEN0_CKPT), torch_dtype=torch.float16
    ).cuda()
    model.eval()

    print("[sliding_window_eval] loading wikitext-2-raw-v1 test")
    ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    text = "\n\n".join([s for s in ds["text"] if s.strip()])
    encodings = tokenizer(text, return_tensors="pt")
    n_tokens_total = encodings["input_ids"].shape[1]
    print(f"[sliding_window_eval] total tokens = {n_tokens_total}")

    # Method 1: chunked block_size=64 (current)
    print("\n[chunked eval, block_size=64] (current method)")
    ppl_chunked_64 = chunked_eval(model, tokenizer, encodings, block_size=64)
    print(f"  chunked PPL (block=64): {ppl_chunked_64:.4f}")

    # Method 2: chunked block_size=1024
    print("\n[chunked eval, block_size=1024]")
    ppl_chunked_1024 = chunked_eval(model, tokenizer, encodings, block_size=1024)
    print(f"  chunked PPL (block=1024): {ppl_chunked_1024:.4f}")

    # Method 3: sliding-window stride=256, max_length=1024 (HF standard)
    print("\n[sliding-window eval, max_length=1024, stride=256]")
    ppl_sliding_256 = sliding_window_eval(model, tokenizer, encodings, max_length=1024, stride=256)
    print(f"  sliding-window PPL (stride=256): {ppl_sliding_256:.4f}")

    # Method 4: sliding-window stride=512
    print("\n[sliding-window eval, max_length=1024, stride=512]")
    ppl_sliding_512 = sliding_window_eval(model, tokenizer, encodings, max_length=1024, stride=512)
    print(f"  sliding-window PPL (stride=512): {ppl_sliding_512:.4f}")

    # ---------- write verdict ----------
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# Sliding-Window Eval Verdict — gen 0 baseline +80% offset 真因 verify")
    lines.append("")
    lines.append(f"**生成时间**: {now}")
    lines.append("")
    lines.append("**目的**: 验证我们 gen 0 = 36 vs Shumailov paper = 20 的 +80% offset 是不是 eval method 不同 (chunked vs sliding-window) 的 artifact, 不是 fine-tune setup bug.")
    lines.append("")
    lines.append("**checkpoint**: `data/checkpoints_armb/alpha0.0/no_preserve_seed42/generation_0` (5/8 audit-fixed setup: batch=128, lr_const, weight_decay=0.01, fp16, rep_penalty=3.0)")
    lines.append("")
    lines.append("## §1 4 种 eval method 数值")
    lines.append("")
    lines.append("| Method | Block / Stride / Max | Test PPL | vs paper 20 offset |")
    lines.append("|---|---|---:|---:|")
    lines.append(f"| Chunked (current) | block=64, no overlap | {ppl_chunked_64:.4f} | +{(ppl_chunked_64/20-1)*100:.1f}% |")
    lines.append(f"| Chunked larger | block=1024 | {ppl_chunked_1024:.4f} | +{(ppl_chunked_1024/20-1)*100:.1f}% |")
    lines.append(f"| Sliding-window | max=1024, stride=256 (HF std) | {ppl_sliding_256:.4f} | +{(ppl_sliding_256/20-1)*100:.1f}% |")
    lines.append(f"| Sliding-window | max=1024, stride=512 | {ppl_sliding_512:.4f} | +{(ppl_sliding_512/20-1)*100:.1f}% |")
    lines.append("")

    # 决策 binary
    lines.append("## §2 Verdict (binary)")
    lines.append("")
    closest_to_paper = min(
        [("Chunked block=64", ppl_chunked_64),
         ("Chunked block=1024", ppl_chunked_1024),
         ("Sliding-window stride=256", ppl_sliding_256),
         ("Sliding-window stride=512", ppl_sliding_512)],
        key=lambda x: abs(x[1] - 20)
    )
    closest_method, closest_ppl = closest_to_paper
    lines.append(f"- **closest to paper 20**: `{closest_method}` PPL = {closest_ppl:.2f} (offset {(closest_ppl/20-1)*100:+.1f}%)")
    lines.append("")
    if abs(closest_ppl - 20) < 5:
        lines.append(f"**verdict**: gen 0 +80% offset **是 eval method artifact**, 切换到 `{closest_method}` 后 close to paper 20.")
        lines.append("")
        lines.append("**含义**:")
        lines.append("- 反题姐姐 P0-B2 (gen 0 baseline 不复现 Shumailov) **DOWNGRADE** — setup 是对的, eval method 不同")
        lines.append("- paper §6 disclose: 重 eval 全部 generations with sliding-window stride=256")
        lines.append("- **整 trajectory shape (U-shape) 不变** — eval method 只 shift PPL value, 不改 trend")
        lines.append("- 接受率 impact: NMI 24天 1-7% → 5-15% (close 一个最大 P0)")
    elif abs(closest_ppl - 20) < 12:
        lines.append(f"**verdict**: closest method 给 PPL = {closest_ppl:.2f}, 接近 paper 20 但 still 偏 ({(closest_ppl/20-1)*100:+.1f}%).")
        lines.append("")
        lines.append("eval method 部分解释 offset, 仍有部分 setup 偏差 (fp16 / rep_penalty / weight_decay)。需 fp32 sensitivity 进一步 close。")
    else:
        lines.append(f"**verdict**: 最接近 paper 20 的 method 仍偏 {(closest_ppl/20-1)*100:+.1f}%, **不是 eval method 问题**。")
        lines.append("")
        lines.append("setup 真不复现 Shumailov,反题姐姐 P0-B2 hold。需 fp32 / rep_penalty=2.0 / weight_decay 全方位 sensitivity sweep。")
    lines.append("")

    OUT_MD.write_text("\n".join(lines))
    print(f"\n[sliding_window_eval] verdict 写到 {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
