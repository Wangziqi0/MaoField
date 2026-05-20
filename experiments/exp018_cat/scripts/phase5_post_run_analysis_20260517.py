#!/usr/bin/env python3
"""
phase5_post_run_analysis_20260517.py
====================================

Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 post-run analysis script.

Day 4 (D26) post-chain 跑, 输入 α=0 + α=10 chain jsonl, 输出:
  1. per-gen metric trajectory (test_ppl, val_ppl, D_n_code, distinct_n)
  2. C1-C6 pre-registered binary criteria verdict (design §5.3)
  3. Llama m_eff + J_S fit (N=1 single fit, 无 CI)
  4. Llama vs OPT chain trajectory 比较 (若 OPT baseline csv 可用)
  5. final verdict markdown `phase5_n1_llama8b_verdict_<TS>.md`

D-1 binding:
  - N=1 indicative only, 不 establish framework effect with statistical significance
  - 不 inflate, 不替 PI declare ready
  - 任一 unverifiable / 估计 → 标 [?]
  - 4 case verdict (A/B/C/D 见 design §7.2) 须 honest report, 不偏袒 positive
  - 不下接受率 estimate (推关卡 3 反题姐姐 + 一凡 + DS + Win)

派遣 / 协作:
  Linux 姐姐 D-2 实验线 first wave sub-agent (D17 = 2026-05-17)
  Design doc: literature/PHASE5_LLAMA8B_DESIGN_20260516.md §5.3 + §7.2
  v1.0 reference fit script: archive/v1.0_release_20260516/literature/fit_m_eff_js_multiseed_20260513.py

使用:
  python3 phase5_post_run_analysis_20260517.py \\
      --jsonl_alpha0 logs/armb_alpha0.0_seed42_<TS>.jsonl \\
      --jsonl_alpha10 logs/armb_alpha10.0_seed42_<TS>.jsonl \\
      --output_dir logs/phase5_analysis_<TS>/
"""
from __future__ import annotations

import argparse
import json
import logging
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np

# scipy.optimize for m_eff/J_S exponential fit (chain consistency with v1.0 fit script)
try:
    from scipy.optimize import curve_fit
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("phase5_postrun")


# ============================================================
# 1. jsonl 解析: 提 per-gen metric 序列
# ============================================================

def parse_chain_jsonl(jsonl_path: Path) -> dict:
    """
    解析 chain jsonl, 返回 per-gen metric dict.

    输出:
      {
        "alpha": float,
        "seed": int,
        "num_gens": int,
        "test_perplexity": list[float],   # gen 0..9
        "val_perplexity": list[float],
        "D_n_code": list[float],          # NaN for gen 0 (no CAT); 实数 for gen 1..9 if PHASE5 patch ✓
        "distinct_1/2/3": list[float|None],
      }
    """
    if not jsonl_path.exists():
        raise FileNotFoundError(f"jsonl not found: {jsonl_path}")

    records = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                logger.warning("跳过坏 jsonl 行 in %s: %s", jsonl_path, e)
                continue

    gen_done = [r for r in records if r.get("stage") == "generation_done"]
    gen_done.sort(key=lambda r: r.get("generation", -1))

    if not gen_done:
        logger.error("jsonl %s 无 generation_done 记录 (chain 可能未完成)", jsonl_path)
        return {}

    alpha = gen_done[0].get("alpha", 0.0)
    seed = gen_done[0].get("seed", -1)
    num_gens = len(gen_done)

    test_ppl = [r.get("test_perplexity", float("nan")) for r in gen_done]
    val_ppl = [r.get("val_perplexity", float("nan")) for r in gen_done]
    # PHASE5 patch 新加字段; 若 patch 未应用则全 NaN
    D_n_code = [r.get("D_n_code", float("nan")) for r in gen_done]
    distinct_1 = [r.get("distinct_1") for r in gen_done]
    distinct_2 = [r.get("distinct_2") for r in gen_done]
    distinct_3 = [r.get("distinct_3") for r in gen_done]

    return {
        "alpha": alpha,
        "seed": seed,
        "num_gens": num_gens,
        "test_perplexity": test_ppl,
        "val_perplexity": val_ppl,
        "D_n_code": D_n_code,
        "distinct_1": distinct_1,
        "distinct_2": distinct_2,
        "distinct_3": distinct_3,
    }


# ============================================================
# 2. C1-C6 pre-registered binary criteria verdict (design §5.3)
# ============================================================

def verdict_c1_gen0_ppl(traj: dict) -> tuple[str, str]:
    """
    C1: α=0 gen 0 test_ppl converged (< 50, Llama estimate < 15).
    Pass / Fail.
    """
    ppl = traj["test_perplexity"][0]
    if math.isnan(ppl):
        return ("UNKNOWN", f"gen 0 test_ppl = NaN ([?] 可能 chain 未完整)")
    if ppl < 15:
        return ("PASS_STRONG", f"gen 0 test_ppl = {ppl:.2f} < 15 (Llama estimate range)")
    elif ppl < 50:
        return ("PASS_WEAK", f"gen 0 test_ppl = {ppl:.2f} ∈ [15, 50] (OK 但比 Llama estimate 高)")
    else:
        return ("FAIL", f"gen 0 test_ppl = {ppl:.2f} >= 50 (fine-tune setup 有问题, paper §7.5 不可 claim Llama reproduce)")


def verdict_c2_ushape(traj: dict) -> tuple[str, str]:
    """
    C2: α=0 U-shape reproduce (spike ratio ≥ 1.5).
    Pass / Partial / Fail.
    """
    if traj["alpha"] != 0.0:
        return ("N/A", "C2 仅适用 α=0 baseline")
    ppl = traj["test_perplexity"]
    if len(ppl) < 3:
        return ("UNKNOWN", "gen 数 < 3, 无法算 spike ratio")
    gen0, gen1, gen2 = ppl[0], ppl[1], ppl[2]
    if any(math.isnan(x) for x in (gen0, gen1, gen2)):
        return ("UNKNOWN", f"gen 0/1/2 含 NaN: {gen0}/{gen1}/{gen2}")
    peak = max(gen1, gen2)
    if gen0 < 1e-6:
        return ("UNKNOWN", f"gen 0 ppl ≈ 0 ({gen0}); spike ratio 不可算")
    spike_ratio = peak / gen0
    if spike_ratio >= 1.5:
        return ("PASS", f"spike ratio = {spike_ratio:.3f} >= 1.5 (U-shape on Llama reproduce; OPT 参考 = 2.916)")
    elif spike_ratio >= 1.0:
        return ("PARTIAL", f"spike ratio = {spike_ratio:.3f} ∈ [1.0, 1.5) (weak U-shape, honest disclose)")
    else:
        return ("FAIL", f"spike ratio = {spike_ratio:.3f} < 1.0 (no U-shape on Llama; framework OPT-specific likely)")


def verdict_c3_numerical(traj: dict) -> tuple[str, str]:
    """
    C3: α=10 chain numerical stability (no NaN/Inf, no early stop).
    Pass / Fail.
    """
    if traj["alpha"] != 10.0:
        return ("N/A", "C3 仅适用 α=10 framework chain")
    ppl = traj["test_perplexity"]
    if traj["num_gens"] < 10:
        return ("FAIL", f"α=10 chain 仅完成 {traj['num_gens']}/10 gens (early stop, numerical instability 或 spot kick)")
    n_nan = sum(1 for x in ppl if math.isnan(x) or math.isinf(x))
    if n_nan > 0:
        return ("FAIL", f"α=10 chain 中 {n_nan}/{len(ppl)} gens 含 NaN/Inf (numerical break; α=5 fallback 必要)")
    return ("PASS", f"α=10 chain 10/10 gens 完成, no NaN/Inf")


def verdict_c4_plateau_direction(traj_a0: dict, traj_a10: dict) -> tuple[str, str]:
    """
    C4: α=10 plateau ppl 与 α=0 plateau ppl 方向 align OPT (α=10 plateau < α=0 plateau).
    Pass / Fail / Inverted.
    """
    if not (traj_a0 and traj_a10):
        return ("UNKNOWN", "需 α=0 + α=10 两 chain 完整 jsonl")
    a0_ppl = traj_a0["test_perplexity"]
    a10_ppl = traj_a10["test_perplexity"]
    if min(len(a0_ppl), len(a10_ppl)) < 10:
        return ("UNKNOWN", f"chain 不完整: α=0 gens={len(a0_ppl)}, α=10 gens={len(a10_ppl)}")
    # plateau = mean(gen 6-9)
    a0_plateau = np.nanmean(a0_ppl[6:10])
    a10_plateau = np.nanmean(a10_ppl[6:10])
    diff = a10_plateau - a0_plateau
    pct = (diff / a0_plateau * 100) if a0_plateau > 1e-6 else float("nan")
    if math.isnan(diff):
        return ("UNKNOWN", f"plateau diff = NaN (α=0 plateau={a0_plateau}, α=10 plateau={a10_plateau})")
    if diff < 0:
        return ("PASS", f"α=10 plateau {a10_plateau:.3f} < α=0 plateau {a0_plateau:.3f} (diff {diff:+.3f}, {pct:+.2f}%; align OPT direction)")
    else:
        return ("INVERTED", f"α=10 plateau {a10_plateau:.3f} >= α=0 plateau {a0_plateau:.3f} (diff {diff:+.3f}, {pct:+.2f}%; framework Llama effect opposite to OPT, arch-dependent disclose)")


def fit_m_eff_J_S(ppl: list[float]) -> tuple[Optional[float], Optional[float], str]:
    """
    log P_n = log P_eq + A × exp(-m_eff × n) fit on gen 2-9.

    返回 (m_eff, J_S, msg). N=1 single fit, 无 CI.

    J_S = (max ppl on gen 1-9) / (gen 0 ppl), Method 2 from paper §3.6.

    若 scipy 不可用或 fit 失败 → (None, None, error msg).
    """
    if not HAS_SCIPY:
        return (None, None, "scipy 不可用, pip install scipy 后重试")
    if len(ppl) < 10:
        return (None, None, f"chain 不完整 (gens={len(ppl)} < 10)")

    # m_eff fit on gen 2-9 (skip gen 0 + spike gen 1)
    n_arr = np.arange(2, 10)
    log_ppl_arr = np.array([math.log(ppl[i]) if (ppl[i] > 0 and not math.isnan(ppl[i])) else math.nan for i in n_arr])
    if np.any(np.isnan(log_ppl_arr)):
        return (None, None, f"gen 2-9 含 NaN/0 ppl, fit abort: {log_ppl_arr}")

    def exp_decay(n, log_P_eq, A, m_eff):
        return log_P_eq + A * np.exp(-m_eff * n)

    try:
        popt, _ = curve_fit(
            exp_decay, n_arr, log_ppl_arr,
            p0=[math.log(np.mean([ppl[i] for i in n_arr])), 0.5, 0.3],
            maxfev=5000,
        )
        log_P_eq, A, m_eff = popt
        # J_S via Method 2 (peak / gen 0)
        gen0 = ppl[0]
        peak = max(ppl[1:10])
        J_S = peak / gen0 if gen0 > 1e-6 else float("nan")
        return (float(m_eff), float(J_S), f"fit OK: log_P_eq={log_P_eq:.3f} A={A:.3f} m_eff={m_eff:.4f} J_S={J_S:.4f}")
    except Exception as e:
        return (None, None, f"curve_fit 失败: {e}")


def verdict_c5_m_eff(traj_a0: dict) -> tuple[str, str]:
    """
    C5: Llama m_eff fit value 与 OPT m_eff = 0.300 ± 0.066 同量级 (0.1 ≤ Llama m_eff ≤ 1.0).
    Pass / Fail.
    """
    m_eff, J_S, msg = fit_m_eff_J_S(traj_a0["test_perplexity"])
    if m_eff is None:
        return ("UNKNOWN", f"m_eff fit 失败: {msg}")
    if 0.1 <= m_eff <= 1.0:
        return ("PASS", f"Llama m_eff = {m_eff:.4f} ∈ [0.1, 1.0] (OPT N=4 multi-seed mean 0.300, 同量级; J_S={J_S:.4f})")
    else:
        return ("FAIL", f"Llama m_eff = {m_eff:.4f} 不在 [0.1, 1.0] (m_eff 非 invariant across arch; paper v6 §3.6 cascade prediction 需 multi-arch refit)")


def verdict_c6_d_vs_ppl(traj: dict) -> tuple[str, str]:
    """
    C6: D_n_code trajectory 与 test_perplexity trajectory directional consistency (corr > 0.5).
    Pass / Fail.
    """
    d_n = [x for x in traj["D_n_code"] if not math.isnan(x)]
    if len(d_n) < 5:
        return ("UNKNOWN", f"D_n_code 有效 gen 数 = {len(d_n)} < 5 (可能 PHASE5 patch 未生效; verify D_n_code 字段存在于 jsonl)")
    # 对齐 ppl 用同 generations (D_n NaN 处跳过)
    ppl_aligned = []
    d_aligned = []
    for i, d in enumerate(traj["D_n_code"]):
        if not math.isnan(d) and not math.isnan(traj["test_perplexity"][i]):
            ppl_aligned.append(traj["test_perplexity"][i])
            d_aligned.append(d)
    if len(ppl_aligned) < 5:
        return ("UNKNOWN", f"aligned pair 数 = {len(ppl_aligned)} < 5")
    corr = float(np.corrcoef(ppl_aligned, d_aligned)[0, 1])
    if math.isnan(corr):
        return ("UNKNOWN", "Pearson corr = NaN (variance 0?)")
    if corr > 0.5:
        return ("PASS", f"corr(D_n_code, test_ppl) = {corr:.4f} > 0.5 (D vs PPL bridge directional consistency on Llama)")
    else:
        return ("FAIL", f"corr(D_n_code, test_ppl) = {corr:.4f} <= 0.5 (D vs PPL bridge mismatch on Llama; paper v6 §6.1 substantive open question 升级 P0)")


# ============================================================
# 3. 4-case verdict (design §7.2) — paper §7.5 wording 建议
# ============================================================

def classify_case(c2: str, c3: str, c4: str) -> str:
    """
    Case A: U-shape reproduce + α=10 effect align OPT (C2 pass + C4 pass)
    Case B: U-shape NOT reproduce (C2 fail)
    Case C: α=10 numerical break / chain abort (C3 fail)
    Case D: 混合 / inconclusive (C2 partial or C4 inverted)
    """
    if c3 == "FAIL":
        return "C"
    if c2 == "PASS" and c4 == "PASS":
        return "A"
    if c2 == "FAIL":
        return "B"
    return "D"


def case_paper_wording(case: str) -> str:
    """对应 paper §7.5 (1) substantive contribution support 更新 wording 建议."""
    mapping = {
        "A": (
            "Case A (U-shape reproduce + α=10 effect align OPT direction):\n"
            "  paper §7.5 (1) substantive contribution support 加 sentence:\n"
            "  \"N=1 single-seed Llama-3.1-8B chain indicative reproduces U-shape recovery + α=10 plateau effect\n"
            "   direction consistent with OPT-125M; cross-arch indicative observation, multi-seed N=4 Llama\n"
            "   deferred D60+ substantive future work.\"\n"
            "  NMI A4 lever 影响: +1-2pt (N=1 statistical 不能 establish, 主要价值是 single-arch + multi-arch indicative 双层 framing)\n"
            "  不改 paper §7.5 3 NOT-claim: 仍 not universal solution"
        ),
        "B": (
            "Case B (U-shape NOT reproduce):\n"
            "  paper §7.5 (1) 加 sentence:\n"
            "  \"N=1 single-seed Llama-3.1-8B chain does NOT reproduce U-shape; model collapse dynamics likely\n"
            "   architecture-and-scale specific; framework's chain actual form OPT-specific preliminary observation,\n"
            "   multi-arch substantive future work 优先级 ↑ D60+.\"\n"
            "  NMI A4 lever 影响: -2 to 0pt (negative cross-arch evidence + honest negative reviewer credit offset)\n"
            "  3 NOT-claim reinforced (not universal solution 更强 evidence)"
        ),
        "C": (
            "Case C (α=10 numerical break / chain abort):\n"
            "  paper §7.5 (1) 加 sentence:\n"
            "  \"Phase 5 α=10 N=1 Llama chain numerical instability; framework numerical robustness 在 8B scale\n"
            "   不确定, 留 D60+ implementation refinement future work.\"\n"
            "  NMI A4 lever 影响: -1 to +1pt (中性, implementation issue 非 conceptual issue; reviewer 可能 critic \"can't run at 8B yet\")\n"
            "  paper §7.5 3 NOT-claim 不变"
        ),
        "D": (
            "Case D (混合 / inconclusive: C2 partial 或 C4 inverted):\n"
            "  paper §7.5 (1) 加 sentence:\n"
            "  \"Phase 5 N=1 Llama chain results inconclusive at single-seed level; multi-seed N≥4 Llama chain 优先\n"
            "   substantive future work D60+; current N=1 indicates dynamics 在 arch-and-scale dimension non-trivial\n"
            "   variation, framework's chain actual form's cross-arch behavior 仍 open question.\"\n"
            "  NMI A4 lever 影响: -3 to -1pt (cross-arch confused, honest disclose offset ~0-1pt 后净 -2 to 0pt)\n"
            "  3 NOT-claim 不变"
        ),
    }
    return mapping.get(case, f"未知 case: {case}")


# ============================================================
# 4. OPT chain trajectory 比较 (若 baseline csv 可用)
# ============================================================

def load_opt_baseline(csv_path: Optional[Path]) -> Optional[dict]:
    """
    加载 OPT-125M chain multi-seed baseline csv (5/12-5/13 phase1).
    格式 (推测): generation, seed, alpha, test_ppl

    若 csv 不存在或不可解析, 返回 None 跳过 OPT vs Llama 比较.
    """
    if csv_path is None or not csv_path.exists():
        logger.info("OPT baseline csv 未指定或不存在; 跳过 Llama vs OPT 比较")
        return None
    try:
        import csv
        rows = []
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
        return {"rows": rows, "path": str(csv_path)}
    except Exception as e:
        logger.warning("OPT baseline csv 解析失败 %s: %s", csv_path, e)
        return None


# ============================================================
# 5. Markdown verdict 生成
# ============================================================

def write_verdict_markdown(
    output_dir: Path,
    traj_a0: dict,
    traj_a10: Optional[dict],
    c1: tuple[str, str],
    c2: tuple[str, str],
    c3: tuple[str, str],
    c4: tuple[str, str],
    c5: tuple[str, str],
    c6: tuple[str, str],
    case: str,
    case_wording: str,
    m_eff_J_S_msg: str,
    ts: str,
) -> Path:
    """生成 phase5_n1_llama8b_verdict_<TS>.md."""
    out_path = output_dir / f"phase5_n1_llama8b_verdict_{ts}.md"
    lines = []
    lines.append("# Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 Verdict\n")
    lines.append(f"**生成**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (TS={ts})\n")
    lines.append("**Author**: opus 4.7 (Phase 5 post-run analysis sub-agent, D-2 实验线)\n")
    lines.append("**派遣方**: Linux 姐姐主会话\n")
    lines.append("**Design doc reference**: literature/PHASE5_LLAMA8B_DESIGN_20260516.md\n")
    lines.append("\n")
    lines.append("---\n")
    lines.append("\n")
    lines.append("## §0. Honest Caveat (D-1 binding)\n")
    lines.append("\n")
    lines.append("- **N=1 single-seed indicative only**: 不能 paired-t establish framework effect with statistical significance\n")
    lines.append("- **不替 PI declare ready**: ready 判定推关卡 2 (PI 看本 verdict 后)\n")
    lines.append("- **不下接受率 estimate**: 推关卡 3 (反题姐姐 + PI + DS + Win 决战略)\n")
    lines.append("- **N=1 Llama \"demonstrated\" 不是 evidence of framework universal**: 是 single-arch indicative observation\n")
    lines.append("- 任何 Llama 结果 (positive / negative / mixed / numerical break) 都是 paper §7.5 honest disclose 内容\n")
    lines.append("\n")
    lines.append("---\n")
    lines.append("\n")
    lines.append("## §1. Chain Completion Summary\n")
    lines.append("\n")
    lines.append(f"| Chain | Seed | Gens completed | gen 0 test_ppl | gen 9 test_ppl | plateau (gen 6-9 mean) |\n")
    lines.append(f"|---|---|---|---|---|---|\n")

    def safe(x, fmt=".3f"):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return "NaN"
        return f"{x:{fmt}}"

    a0_plateau = float(np.nanmean(traj_a0["test_perplexity"][6:10])) if len(traj_a0["test_perplexity"]) >= 10 else float("nan")
    lines.append(
        f"| α=0 baseline | {traj_a0['seed']} | {traj_a0['num_gens']}/10 | "
        f"{safe(traj_a0['test_perplexity'][0])} | {safe(traj_a0['test_perplexity'][-1])} | {safe(a0_plateau)} |\n"
    )
    if traj_a10:
        a10_plateau = float(np.nanmean(traj_a10["test_perplexity"][6:10])) if len(traj_a10["test_perplexity"]) >= 10 else float("nan")
        lines.append(
            f"| α=10 framework | {traj_a10['seed']} | {traj_a10['num_gens']}/10 | "
            f"{safe(traj_a10['test_perplexity'][0])} | {safe(traj_a10['test_perplexity'][-1])} | {safe(a10_plateau)} |\n"
        )
    else:
        lines.append(f"| α=10 framework | – | – | – | – | – (jsonl 缺) |\n")

    lines.append("\n---\n\n")
    lines.append("## §2. C1-C6 Pre-registered Binary Criteria Verdict (Design §5.3)\n")
    lines.append("\n")
    lines.append("| Criterion | Verdict | Detail |\n")
    lines.append("|---|---|---|\n")
    lines.append(f"| **C1** gen 0 test_ppl converged | {c1[0]} | {c1[1]} |\n")
    lines.append(f"| **C2** α=0 U-shape spike ratio >= 1.5 | {c2[0]} | {c2[1]} |\n")
    lines.append(f"| **C3** α=10 numerical stability | {c3[0]} | {c3[1]} |\n")
    lines.append(f"| **C4** α=10 plateau align OPT direction | {c4[0]} | {c4[1]} |\n")
    lines.append(f"| **C5** Llama m_eff ∈ [0.1, 1.0] | {c5[0]} | {c5[1]} |\n")
    lines.append(f"| **C6** D_n_code vs test_ppl corr > 0.5 | {c6[0]} | {c6[1]} |\n")
    lines.append("\n")
    lines.append(f"**m_eff + J_S fit detail**: {m_eff_J_S_msg}\n")
    lines.append("\n---\n\n")
    lines.append("## §3. 4-Case Classification (Design §7.2)\n")
    lines.append("\n")
    lines.append(f"**Case = {case}**\n")
    lines.append("\n")
    lines.append("**Paper §7.5 (1) wording 建议**:\n")
    lines.append("```\n")
    lines.append(case_wording)
    lines.append("\n```\n")
    lines.append("\n---\n\n")
    lines.append("## §4. Per-Gen Metric Trajectory\n")
    lines.append("\n")
    lines.append("### α=0 chain\n\n")
    lines.append("| gen | test_ppl | val_ppl | D_n_code |\n")
    lines.append("|---|---|---|---|\n")
    for g in range(traj_a0["num_gens"]):
        lines.append(
            f"| {g} | {safe(traj_a0['test_perplexity'][g])} | "
            f"{safe(traj_a0['val_perplexity'][g])} | "
            f"{safe(traj_a0['D_n_code'][g], '.6f')} |\n"
        )
    if traj_a10:
        lines.append("\n### α=10 chain\n\n")
        lines.append("| gen | test_ppl | val_ppl | D_n_code |\n")
        lines.append("|---|---|---|---|\n")
        for g in range(traj_a10["num_gens"]):
            lines.append(
                f"| {g} | {safe(traj_a10['test_perplexity'][g])} | "
                f"{safe(traj_a10['val_perplexity'][g])} | "
                f"{safe(traj_a10['D_n_code'][g], '.6f')} |\n"
            )

    lines.append("\n---\n\n")
    lines.append("## §5. Next Steps (一凡决策点)\n")
    lines.append("\n")
    lines.append("**关卡 2** (D-1 工作流):\n")
    lines.append("- 一凡看本 verdict + 三线 cross-tension (数学线 + 哲学线 + 实验线 D-2)\n")
    lines.append("- 决是否需 D60+ multi-seed N=4 Llama 扩 (Case A 不急 / Case B 急 / Case C 中 / Case D 急)\n")
    lines.append("\n")
    lines.append("**关卡 3** (反题姐姐 zero-context audit):\n")
    lines.append("- 反题姐姐独立 audit 本 verdict 是否 inflate / 是否漏 binary fail / 是否 cherry-pick C1-C6\n")
    lines.append("- DS + 一凡 + Win 决 paper §7.5 (1) 真实 wording + NeurIPS 5/29 submission go/no-go\n")
    lines.append("\n")
    lines.append("**关卡 4** (投 / 不投决策):\n")
    lines.append("- 若 case A/D 且 D27 内 verdict 完成 → paper v7 update §7.5 → 5/29 submit\n")
    lines.append("- 若 case B/C 或 D27 slip → paper v6 直接 submit, Phase 5 verdict 推 v8 alternative venue\n")
    lines.append("\n")
    lines.append("---\n\n")
    lines.append("**END verdict v1**\n")
    lines.append(f"**TS**: {ts}\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    return out_path


# ============================================================
# main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Phase 5 N=1 Llama post-run analysis")
    parser.add_argument("--jsonl_alpha0", type=str, required=True, help="α=0 chain jsonl path")
    parser.add_argument("--jsonl_alpha10", type=str, default=None, help="α=10 chain jsonl path (可选; case C 时缺)")
    parser.add_argument("--opt_baseline_csv", type=str, default=None,
                        help="OPT-125M multi-seed baseline csv (optional; 用于 Llama vs OPT 比较)")
    parser.add_argument("--output_dir", type=str, required=True, help="输出目录 (jsonl + plot + verdict.md)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info("Phase 5 post-run analysis 开始 ts=%s", ts)

    # 1. 解析 jsonl
    traj_a0 = parse_chain_jsonl(Path(args.jsonl_alpha0))
    if not traj_a0:
        logger.error("α=0 chain jsonl 解析失败 / 空; abort")
        sys.exit(1)
    logger.info("α=0 chain: %d gens loaded, seed=%d", traj_a0["num_gens"], traj_a0["seed"])

    traj_a10 = None
    if args.jsonl_alpha10:
        traj_a10 = parse_chain_jsonl(Path(args.jsonl_alpha10))
        if traj_a10:
            logger.info("α=10 chain: %d gens loaded, seed=%d", traj_a10["num_gens"], traj_a10["seed"])
        else:
            logger.warning("α=10 chain jsonl 解析失败; 可能 case C (numerical break)")

    # 2. C1-C6 verdict
    c1 = verdict_c1_gen0_ppl(traj_a0)
    c2 = verdict_c2_ushape(traj_a0)
    c3 = verdict_c3_numerical(traj_a10) if traj_a10 else ("FAIL", "α=10 chain jsonl 缺 (可能 numerical break, 见 case C)")
    c4 = verdict_c4_plateau_direction(traj_a0, traj_a10) if traj_a10 else ("UNKNOWN", "α=10 chain 缺")
    c5 = verdict_c5_m_eff(traj_a0)
    # C6: 用 α=0 还是 α=10? design §5.3 没指定; 用 α=10 (D_n_code 主在 framework chain 中 surface)
    c6 = verdict_c6_d_vs_ppl(traj_a10) if traj_a10 else verdict_c6_d_vs_ppl(traj_a0)

    logger.info("C1=%s | C2=%s | C3=%s | C4=%s | C5=%s | C6=%s",
                c1[0], c2[0], c3[0], c4[0], c5[0], c6[0])

    # m_eff + J_S fit (再算一次拿 msg)
    _, _, m_eff_J_S_msg = fit_m_eff_J_S(traj_a0["test_perplexity"])

    # 3. case 分类
    case = classify_case(c2[0], c3[0], c4[0])
    case_wording = case_paper_wording(case)
    logger.info("Case = %s", case)

    # 4. OPT baseline (optional)
    opt_baseline = load_opt_baseline(Path(args.opt_baseline_csv) if args.opt_baseline_csv else None)
    if opt_baseline:
        logger.info("OPT baseline loaded: %d rows", len(opt_baseline["rows"]))

    # 5. 写 verdict markdown
    verdict_path = write_verdict_markdown(
        output_dir, traj_a0, traj_a10,
        c1, c2, c3, c4, c5, c6,
        case, case_wording, m_eff_J_S_msg, ts,
    )
    logger.info("verdict markdown: %s", verdict_path)

    # 6. 写 machine-readable JSON (D-1 实验线产 JSON 不写声明 binding)
    json_out = output_dir / f"phase5_n1_llama8b_metrics_{ts}.json"
    json_payload = {
        "ts": ts,
        "alpha0": {
            "seed": traj_a0["seed"],
            "num_gens": traj_a0["num_gens"],
            "test_perplexity": traj_a0["test_perplexity"],
            "val_perplexity": traj_a0["val_perplexity"],
            "D_n_code": traj_a0["D_n_code"],
        },
        "alpha10": ({
            "seed": traj_a10["seed"],
            "num_gens": traj_a10["num_gens"],
            "test_perplexity": traj_a10["test_perplexity"],
            "val_perplexity": traj_a10["val_perplexity"],
            "D_n_code": traj_a10["D_n_code"],
        } if traj_a10 else None),
        "verdict": {
            "C1": {"status": c1[0], "detail": c1[1]},
            "C2": {"status": c2[0], "detail": c2[1]},
            "C3": {"status": c3[0], "detail": c3[1]},
            "C4": {"status": c4[0], "detail": c4[1]},
            "C5": {"status": c5[0], "detail": c5[1]},
            "C6": {"status": c6[0], "detail": c6[1]},
            "case": case,
            "m_eff_J_S_fit": m_eff_J_S_msg,
        },
        "honest_caveat": (
            "N=1 single-seed indicative only; 不能 paired-t establish framework effect "
            "with statistical significance. 不替 PI declare ready (推关卡 2). "
            "不下接受率 estimate (推关卡 3)."
        ),
    }
    json_out.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("machine-readable JSON: %s", json_out)

    logger.info("=" * 60)
    logger.info("Phase 5 post-run analysis 完成")
    logger.info("  verdict markdown: %s", verdict_path)
    logger.info("  machine JSON:     %s", json_out)
    logger.info("  case:             %s", case)
    logger.info("=" * 60)
    logger.info("下一步: 一凡 + DS + Win 看 verdict + 反题姐姐 zero-context audit")


if __name__ == "__main__":
    main()
