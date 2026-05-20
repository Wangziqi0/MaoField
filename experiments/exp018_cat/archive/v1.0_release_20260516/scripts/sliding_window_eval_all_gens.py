#!/usr/bin/env python3
"""
sliding_window_eval_all_gens.py — 反题姐姐 §2 漏 #2 完整 close + paper §6 disclose

跑 sliding-window stride=256 (HF 标准) eval on **all 10 generation checkpoints**
of a given seed. 输出 trajectory: gen 0..9 sliding-window PPL.

vs 现 chunked block=64 eval, 验证整 trajectory shape:
- gen 0: chunked 36 → sliding 22 (paper match)
- gen 9: chunked 56 → sliding ? (predict 28-30 → paper monotone match)

usage:
  ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
    env HIP_VISIBLE_DEVICES=0 .venv/bin/python scripts/sliding_window_eval_all_gens.py --seed 0'

输出: literature/sliding_window_trajectory_seed{N}_<ts>.md
GPU ~5 min/gen × 10 gens = 50 min.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import datetime
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT_ROOT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp018_cat")
CKPT_BASE = PROJECT_ROOT / "data/checkpoints_armb/alpha0.0"


def chunked_eval(model, encodings, block_size=64):
    input_ids = encodings["input_ids"].squeeze(0) if isinstance(encodings["input_ids"], torch.Tensor) else encodings["input_ids"]
    n_tokens = len(input_ids)
    n_chunks = n_tokens // block_size
    nlls = []
    n_used = 0
    with torch.no_grad():
        for i in range(n_chunks):
            chunk = input_ids[i * block_size : (i + 1) * block_size].unsqueeze(0).cuda()
            out = model(chunk, labels=chunk)
            nlls.append(out.loss.item() * block_size)
            n_used += block_size
    if n_used == 0:
        return float("inf")
    return math.exp(sum(nlls) / n_used)


def sliding_window_eval(model, encodings, max_length=1024, stride=256):
    input_ids = encodings["input_ids"].squeeze(0) if isinstance(encodings["input_ids"], torch.Tensor) else encodings["input_ids"]
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
            nlls.append(out.loss.item() * trg_len)
            prev_end_loc = end_loc
            if end_loc == n_tokens:
                break
    if not nlls or prev_end_loc == 0:
        return float("inf")
    return math.exp(sum(nlls) / prev_end_loc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True, help="seed number (0,1,2,3,4 or 42)")
    parser.add_argument("--max-gens", type=int, default=10)
    args = parser.parse_args()

    seed_dir = CKPT_BASE / f"no_preserve_seed{args.seed}"
    if not seed_dir.exists():
        print(f"[ERROR] seed dir not found: {seed_dir}", file=sys.stderr)
        return 1

    print(f"[sliding_window all-gens] seed={args.seed} from {seed_dir}")

    # load wikitext-2 test once
    print("[loading wikitext-2-raw-v1 test]")
    ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    text = "\n\n".join([s for s in ds["text"] if s.strip()])

    # eval each generation_N
    rows = []
    tokenizer = None
    for n in range(args.max_gens):
        ckpt = seed_dir / f"generation_{n}"
        if not ckpt.exists():
            print(f"[gen {n}] checkpoint not found, skip")
            break
        print(f"\n[gen {n}] loading from {ckpt}")
        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained(str(ckpt))
            encodings = tokenizer(text, return_tensors="pt")
            print(f"[encodings] {encodings['input_ids'].shape[1]} tokens")
        model = AutoModelForCausalLM.from_pretrained(
            str(ckpt), torch_dtype=torch.float16
        ).cuda()
        model.eval()

        ppl_chunked_64 = chunked_eval(model, encodings, block_size=64)
        ppl_sliding_256 = sliding_window_eval(model, encodings, max_length=1024, stride=256)
        print(f"[gen {n}] chunked_64={ppl_chunked_64:.4f}  sliding_256={ppl_sliding_256:.4f}")
        rows.append({
            "gen": n,
            "ppl_chunked_64": ppl_chunked_64,
            "ppl_sliding_256": ppl_sliding_256,
        })

        del model
        torch.cuda.empty_cache()

    # write verdict
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_md = PROJECT_ROOT / f"literature/sliding_window_trajectory_seed{args.seed}_{ts}.md"
    out_jsonl = PROJECT_ROOT / f"logs/sliding_window_trajectory_seed{args.seed}_{ts}.jsonl"

    lines = []
    lines.append(f"# Sliding-Window Eval Trajectory — seed={args.seed}")
    lines.append("")
    lines.append(f"**生成**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**checkpoint base**: `{seed_dir}`")
    lines.append("")
    lines.append("## §1 Trajectory (chunked_64 vs sliding_256)")
    lines.append("")
    lines.append("| gen | chunked block=64 | sliding stride=256 | sliding/chunked |")
    lines.append("|---|---:|---:|---:|")
    for r in rows:
        ratio = r["ppl_sliding_256"] / r["ppl_chunked_64"] if r["ppl_chunked_64"] > 0 else float("nan")
        lines.append(f"| {r['gen']} | {r['ppl_chunked_64']:.2f} | {r['ppl_sliding_256']:.2f} | {ratio:.3f} |")
    lines.append("")

    # paper match check
    lines.append("## §2 Paper match check (sliding-window)")
    lines.append("")
    lines.append("Shumailov 2024 reports: gen 0 ≈ 20, gen 9 ≈ 28 (text §5.2 \"from 20 to 28 perplexity points\")")
    lines.append("")
    if rows:
        gen0_ppl = rows[0]["ppl_sliding_256"]
        gen9_ppl = rows[-1]["ppl_sliding_256"] if len(rows) >= 10 else None
        lines.append(f"- Our gen 0 sliding PPL = **{gen0_ppl:.2f}** (paper 20, offset {(gen0_ppl/20-1)*100:+.1f}%)")
        if gen9_ppl:
            lines.append(f"- Our gen 9 sliding PPL = **{gen9_ppl:.2f}** (paper 28, offset {(gen9_ppl/28-1)*100:+.1f}%)")
            ratio = gen9_ppl / gen0_ppl
            paper_ratio = 28 / 20
            lines.append(f"- Our gen9/gen0 ratio = **{ratio:.3f}** (paper {paper_ratio:.3f})")
    lines.append("")

    out_md.write_text("\n".join(lines))
    with out_jsonl.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    print(f"\n[done] verdict: {out_md}")
    print(f"[done] jsonl: {out_jsonl}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
