#!/usr/bin/env python3
"""
plot_collapse_curve.py — paper §4.1 reference baseline figure 生成

输入: logs/shumailov_*.jsonl (collapse curve generation 0-9 perplexity + distinct-n)
输出: figures/collapse_curve_strict_vs_partial.png (双面板 figure)
       figures/collapse_curve_data.csv (paper 写作时引用)

binding (paper-faithful replication):
- 主曲线 = strict-mirror (batch=128, lr=2e-5, scheduler=constant, repetition_penalty=3.0)
- 旁证 = partial-mirror (batch=32, scheduler=linear, no repetition_penalty)
- paper 报 plateau = 12.5-50% above first model — 用横线标出 reference range

用法:
  python plot_collapse_curve.py
"""
import argparse
import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def extract_curve(records: list[dict]) -> dict:
    gens = sorted([r for r in records if r.get("stage") == "generation_done"],
                  key=lambda r: r["generation"])
    return {
        "gen": [r["generation"] for r in gens],
        "test_ppl": [r["test_perplexity"] if not (isinstance(r["test_perplexity"], float)
                                                  and np.isinf(r["test_perplexity"])) else np.nan
                     for r in gens],
        "val_ppl": [r["val_perplexity"] for r in gens],
        "distinct_1": [r.get("distinct_1") for r in gens],
        "distinct_2": [r.get("distinct_2") for r in gens],
        "distinct_3": [r.get("distinct_3") for r in gens],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-jsonl", type=str,
                        default="logs/shumailov_no_preserve_seed42_20260508_092730.jsonl",
                        help="strict-mirror baseline jsonl path")
    parser.add_argument("--partial-jsonl", type=str,
                        default="logs/shumailov_no_preserve_seed42_20260507_200657.jsonl",
                        help="partial-mirror baseline jsonl path")
    parser.add_argument("--figures-dir", type=str, default="figures")
    parser.add_argument("--data-dir", type=str, default="results")
    args = parser.parse_args()

    figures_dir = Path(args.figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    # ---------- 加载两条曲线 ----------
    logger.info("加载 strict-mirror %s", args.strict_jsonl)
    strict = extract_curve(load_jsonl(Path(args.strict_jsonl)))
    logger.info("加载 partial-mirror %s", args.partial_jsonl)
    partial = extract_curve(load_jsonl(Path(args.partial_jsonl)))

    gen0_strict = strict["test_ppl"][0]
    gen0_partial = partial["test_ppl"][0]

    # paper plateau range = 12.5-50% above gen 0
    paper_low_strict = gen0_strict * 1.125
    paper_high_strict = gen0_strict * 1.50

    # ---------- 双面板 figure ----------
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # 左 panel: perplexity curve
    ax = axes[0]
    ax.plot(strict["gen"], strict["test_ppl"], "o-", color="#dc2626",
            linewidth=2, markersize=7, label="strict-mirror (Zenodo official)")
    ax.plot(partial["gen"], partial["test_ppl"], "s--", color="#2563eb",
            linewidth=1.5, markersize=6, alpha=0.7, label="partial-mirror (sub-agent default)")
    ax.axhline(gen0_strict, color="#6b7280", linestyle=":", alpha=0.5,
               label=f"gen 0 baseline = {gen0_strict:.2f}")
    ax.axhspan(paper_low_strict, paper_high_strict, alpha=0.15, color="#10b981",
               label=f"paper plateau range\n(12.5-50% above gen 0: {paper_low_strict:.1f}-{paper_high_strict:.1f})")
    ax.set_xlabel("Generation index $n$ (self-iteration step)")
    ax.set_ylabel("Test perplexity")
    ax.set_title("OPT-125m self-iteration collapse curve\n(replication of Shumailov et al. 2024 Nature)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(0, 10))

    # 右 panel: distinct-n (mode coverage)
    ax = axes[1]
    # strict-mirror: distinct_3 单调衰减 = paper "rare events 消失" pattern
    valid_idx = [i for i, d in enumerate(strict["distinct_3"]) if d is not None]
    ax.plot([strict["gen"][i] for i in valid_idx],
            [strict["distinct_3"][i] for i in valid_idx], "o-", color="#dc2626",
            linewidth=2, markersize=7, label="strict-mirror distinct_3")
    valid_idx_p = [i for i, d in enumerate(partial["distinct_3"]) if d is not None]
    ax.plot([partial["gen"][i] for i in valid_idx_p],
            [partial["distinct_3"][i] for i in valid_idx_p], "s--", color="#2563eb",
            linewidth=1.5, markersize=6, alpha=0.7, label="partial-mirror distinct_3")
    ax.set_xlabel("Generation index $n$")
    ax.set_ylabel("distinct_3 (trigram diversity ratio)")
    ax.set_title("Mode coverage decay\n(strict-mirror reproduces paper trend)")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(0, 10))

    fig.tight_layout()
    fig_path = figures_dir / "collapse_curve_strict_vs_partial.png"
    fig.savefig(fig_path, dpi=150)
    fig.savefig(figures_dir / "collapse_curve_strict_vs_partial.pdf")
    logger.info("figure 落盘 %s + .pdf", fig_path)

    # ---------- 数据 csv (paper 写作时直接引用) ----------
    csv_path = data_dir / "collapse_curve_data.csv"
    with csv_path.open("w") as f:
        f.write("generation,strict_test_ppl,strict_distinct_3,partial_test_ppl,partial_distinct_3\n")
        for i in range(10):
            sp = strict["test_ppl"][i] if i < len(strict["test_ppl"]) else None
            sd = strict["distinct_3"][i] if i < len(strict["distinct_3"]) else None
            pp = partial["test_ppl"][i] if i < len(partial["test_ppl"]) else None
            pd = partial["distinct_3"][i] if i < len(partial["distinct_3"]) else None
            f.write(f"{i},{sp},{sd},{pp},{pd}\n")
    logger.info("data csv 落盘 %s", csv_path)

    # ---------- summary print ----------
    logger.info("=" * 60)
    logger.info("strict-mirror baseline (paper §4.1 主曲线):")
    logger.info("  gen 0 ppl = %.2f (paper: 34, 差 %.1f%%)", gen0_strict,
                100 * (gen0_strict - 34) / 34)
    logger.info("  gen 9 ppl = %.2f (+%.1f%% above gen 0)",
                strict["test_ppl"][-1],
                100 * (strict["test_ppl"][-1] - gen0_strict) / gen0_strict)
    logger.info("  paper plateau range (12.5-50%% above): %.1f - %.1f",
                paper_low_strict, paper_high_strict)
    logger.info("  我们 plateau 在 paper range 内: %s",
                "✓" if paper_low_strict <= strict["test_ppl"][-1] <= paper_high_strict else "✗")
    logger.info("  distinct_3: gen 1 = %.3f → gen 9 = %.3f (衰减 %.1f%%)",
                strict["distinct_3"][1] or 0,
                strict["distinct_3"][-1] or 0,
                100 * (1 - (strict["distinct_3"][-1] or 0) / (strict["distinct_3"][1] or 1)))


if __name__ == "__main__":
    main()
