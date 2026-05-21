#!/usr/bin/env python3
"""
analyze_pearson.py — D-PPL 桥 verify main run 之 Pearson 分析 (7B13 端 跑)

D21 (2026-05-21) 7B13 sub-agent 写, 7B13 端 在 9070XT main run done 之后 跑 (rsync pulled main jsonl 之后).

input:
  - main_D21.jsonl: 9070XT 之 raw D_code values per (alpha, seed, gen, path) tuple
  - chain_logs jsonl (7B13 之 archive/v1.0_release_20260516/chain_logs/armb_alpha*.jsonl): D_paper source

output:
  - pearson_D24_summary.json: Pearson r + p + bootstrap CI 95% per (path, alpha, regime)
  - per-regime tier verdict (per design brief §6.1)

D-1 binding (7B13 sub-agent 之 严守):
  - 不擅自 declare P0★-F close — 仅 surface Pearson r 数字 + tier
  - 占位符禁令: any unverified 数字 标 [?]
  - 真 binary close 判定 由 关卡 3 反题 audit + 关卡 4 PI + DS + 反题 三方决

数学 严格度 caveat:
  - 路径 B + C 之 r 都是 L2 form-borrow tier (proxy form, 不是 true EMA)
  - r 高 ≠ paper §3.6.2 主定理 (2) fixed-point identification close (necessary 非 sufficient)
  - within-seed gen-axis correlation 严重, effective N < 80, hierarchical Pearson [?] 可推 sub-agent
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np


# -----------------------------------------------------------------------------
# Load D_code 数据 from 9070XT main jsonl
# -----------------------------------------------------------------------------
def load_dcode_from_main_jsonl(main_jsonl_path: Path) -> dict:
    """
    Parse main_D21.jsonl, return:
      {
        (alpha, seed, gen, path): {"D_code": float, "n_tokens": int, "caveats": [...]},
        ...
      }
    """
    out = {}
    with open(main_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("event") != "tuple_done":
                continue
            alpha = entry["alpha"]
            seed = entry["seed"]
            gen = entry["gen"]
            path = entry["path"]
            key = (alpha, seed, gen, path)
            d_code_key = f"D_code_path_{path}"
            if d_code_key in entry:
                out[key] = {
                    "D_code": entry[d_code_key],
                    "n_tokens": entry.get("n_tokens"),
                    "caveats": entry.get("caveats", []),
                    "elapsed_sec": entry.get("elapsed_sec"),
                }
    return out


# -----------------------------------------------------------------------------
# Load D_paper 数据 from chain log jsonl
# -----------------------------------------------------------------------------
def load_dpaper_from_chain_logs(chain_logs_dir: Path, alphas: list, seeds: list) -> dict:
    """
    Parse chain log jsonl 之 generation_done events, return:
      {
        (alpha, seed, gen): {"test_perplexity": float, "D_paper": log(PPL_n/PPL_0)},
        ...
      }
    """
    out = {}
    for alpha in alphas:
        for seed in seeds:
            # 例如 archive/v1.0_release_20260516/chain_logs/armb_alpha10.0_seed1_*.jsonl
            pattern = f"armb_alpha{alpha}_seed{seed}_*.jsonl"
            matches = list(chain_logs_dir.glob(pattern))
            if not matches:
                print(f"WARN: 没找到 chain log for alpha={alpha} seed={seed} pattern={pattern}",
                      file=sys.stderr)
                continue
            # 取 latest mtime 之 file (per chain 多次 retry pattern)
            chain_jsonl = max(matches, key=lambda p: p.stat().st_mtime)

            gen_to_ppl = {}
            with open(chain_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("event") == "generation_done":
                        gen = entry.get("generation")
                        ppl = entry.get("test_perplexity")
                        if gen is not None and ppl is not None:
                            gen_to_ppl[gen] = ppl

            # gen=0 之 PPL 作 anchor (D_paper = log(PPL_n / PPL_0))
            if 0 not in gen_to_ppl:
                print(f"WARN: 没找到 gen=0 之 PPL for alpha={alpha} seed={seed}", file=sys.stderr)
                continue
            ppl_0 = gen_to_ppl[0]

            for gen, ppl_n in gen_to_ppl.items():
                d_paper = float(np.log(ppl_n / ppl_0))
                key = (alpha, seed, gen)
                out[key] = {
                    "test_perplexity_n": ppl_n,
                    "test_perplexity_0": ppl_0,
                    "D_paper": d_paper,
                }
    return out


# -----------------------------------------------------------------------------
# Pearson + bootstrap CI
# -----------------------------------------------------------------------------
def pearson_with_bootstrap(x: np.ndarray, y: np.ndarray, n_bootstrap: int = 10000,
                           seed: int = 20260521) -> dict:
    """Compute Pearson r + bootstrap CI 95% + 2-sided p (Fisher-z approx)."""
    from scipy.stats import pearsonr

    if len(x) < 3 or len(y) < 3 or len(x) != len(y):
        return {
            "r": None,
            "p": None,
            "ci_lo": None,
            "ci_hi": None,
            "n": len(x),
            "caveat": "N < 3 OR shape mismatch, Pearson not computable",
        }

    # Scipy pearsonr (point estimate + p)
    r, p = pearsonr(x, y)

    # Bootstrap CI 95% (per design brief §5.2 step 3 之 N_bootstrap=10000)
    rng = np.random.default_rng(seed)
    N = len(x)
    r_boot = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, N, size=N)
        xb = x[idx]
        yb = y[idx]
        # 防 zero variance (all-same bootstrap)
        if xb.std() == 0 or yb.std() == 0:
            continue
        rb, _ = pearsonr(xb, yb)
        r_boot.append(rb)

    if len(r_boot) < n_bootstrap // 2:
        return {
            "r": float(r),
            "p": float(p),
            "ci_lo": None,
            "ci_hi": None,
            "n": int(N),
            "n_bootstrap_valid": len(r_boot),
            "caveat": "bootstrap 之 valid samples < n_bootstrap/2, CI 不 trustworthy",
        }

    ci_lo, ci_hi = np.percentile(r_boot, [2.5, 97.5])
    return {
        "r": float(r),
        "p": float(p),
        "ci_lo": float(ci_lo),
        "ci_hi": float(ci_hi),
        "n": int(N),
        "n_bootstrap": n_bootstrap,
        "n_bootstrap_valid": len(r_boot),
    }


def classify_tier(r: Optional[float], p: Optional[float], ci_lo: Optional[float]) -> str:
    """
    Classify Pearson 之 tier per design brief §6.1.

    Tier 之 NON-binary close P0★-F. 仅 sub-agent surface 之 reference, 一凡 + 反题三方 决.
    """
    if r is None:
        return "N/A — Pearson 不可 compute"
    if p is None or p > 0.05:
        return f"L2 marginal — p > 0.05 OR p N/A (r={r:.4f})"
    if r > 0.85 and ci_lo is not None and ci_lo > 0:
        return f"L2 form-borrow strong tier — r > 0.85, p < 0.05, CI excludes 0 (r={r:.4f})"
    elif r > 0.7:
        return f"L2 partial tier — 0.7 < r < 0.85, p < 0.05 (r={r:.4f})"
    elif r > 0.3:
        return f"L2 marginal — 0.3 < r < 0.7 (r={r:.4f}) — sub-agent 推 路径 A escalate consideration"
    else:
        return f"L2 fail — r < 0.3 (r={r:.4f}) — sub-agent 推 D60+ 路径 D rerun chain"


# -----------------------------------------------------------------------------
# Per-regime breakdown (full / plateau / transient)
# -----------------------------------------------------------------------------
PLATEAU_GENS = [5, 6, 7, 8, 9]  # per paper §3.6.5
TRANSIENT_GENS = [1, 2]          # per paper §3.6.6 L0 vacuous


def select_subset(dcode: dict, dpaper: dict, path: str, alphas: list,
                  gens: Optional[list] = None) -> tuple:
    """
    Select (x=D_code, y=D_paper) arrays for given path + alphas + (optional) gens subset.
    """
    xs, ys, keys = [], [], []
    for (a, s, g, p), v in dcode.items():
        if p != path:
            continue
        if a not in alphas:
            continue
        if gens is not None and g not in gens:
            continue
        key_paper = (a, s, g)
        if key_paper not in dpaper:
            continue
        d_code = v["D_code"]
        d_paper = dpaper[key_paper]["D_paper"]
        if d_code is None or d_paper is None:
            continue
        xs.append(d_code)
        ys.append(d_paper)
        keys.append((a, s, g, p))
    return np.array(xs), np.array(ys), keys


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="D-PPL bridge Pearson 分析 (7B13 端)")
    p.add_argument("--main-jsonl", type=Path, required=True,
                   help="9070XT 之 main_D21.jsonl path (rsync pulled 之 后)")
    p.add_argument("--chain-logs-dir", type=Path,
                   default=Path("/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/"
                                "archive/v1.0_release_20260516/chain_logs"))
    p.add_argument("--alphas", type=str, default="0.0,10.0")
    p.add_argument("--seeds", type=str, default="1,2,3,4")
    p.add_argument("--paths", type=str, default="B,C")
    p.add_argument("--output-json", type=Path, required=True)
    p.add_argument("--n-bootstrap", type=int, default=10000)
    p.add_argument("--bootstrap-seed", type=int, default=20260521)
    return p.parse_args()


def main():
    args = parse_args()

    alphas = [float(a) for a in args.alphas.split(",")]
    seeds = [int(s) for s in args.seeds.split(",")]
    paths = [p.strip() for p in args.paths.split(",")]

    # Load
    print(f"=== analyze_pearson.py start ===")
    print(f"main_jsonl: {args.main_jsonl}")
    print(f"chain_logs_dir: {args.chain_logs_dir}")

    dcode = load_dcode_from_main_jsonl(args.main_jsonl)
    print(f"loaded dcode: {len(dcode)} tuples")

    dpaper = load_dpaper_from_chain_logs(args.chain_logs_dir, alphas, seeds)
    print(f"loaded dpaper: {len(dpaper)} (alpha, seed, gen) tuples")

    # Per-path × per-alpha × per-regime Pearson
    result = {
        "ts": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input_main_jsonl": str(args.main_jsonl),
        "input_chain_logs": str(args.chain_logs_dir),
        "n_tuples_dcode": len(dcode),
        "n_tuples_dpaper": len(dpaper),
        "alphas": alphas,
        "seeds": seeds,
        "paths": paths,
        "n_bootstrap": args.n_bootstrap,
        "bootstrap_seed": args.bootstrap_seed,
        "results_by_path": {},
        "D_1_binding": {
            "tier_is_NOT_binary_close": "Pearson tier 仅 surface, 不 binary close P0★-F",
            "true_close_requires": "路径 A (re-train EMA) OR 路径 D (D60+ rerun with EMA save)",
            "necessary_not_sufficient": "high r 可 by spurious co-monotonic decay 而 achieve, "
                                       "不证 paper §3.6.2 main theorem fixed-point identification",
        },
    }

    for path in paths:
        path_result = {}

        # 全 (full): all alphas, all gens
        x, y, _ = select_subset(dcode, dpaper, path=path, alphas=alphas, gens=None)
        # exclude gen=0 之 path C tuple (D_code = 0 trivially, can dominate Pearson)
        # 注: 此 logic 是 sub-agent recommendation, 一凡 关卡 3 决是否 include gen=0
        full_stat = pearson_with_bootstrap(x, y, n_bootstrap=args.n_bootstrap,
                                            seed=args.bootstrap_seed)
        full_stat["tier"] = classify_tier(full_stat["r"], full_stat["p"], full_stat["ci_lo"])
        path_result["full"] = full_stat

        # Plateau (gen=5-9, per paper §3.6.5)
        x, y, _ = select_subset(dcode, dpaper, path=path, alphas=alphas, gens=PLATEAU_GENS)
        plateau_stat = pearson_with_bootstrap(x, y, n_bootstrap=args.n_bootstrap,
                                               seed=args.bootstrap_seed)
        plateau_stat["tier"] = classify_tier(plateau_stat["r"], plateau_stat["p"], plateau_stat["ci_lo"])
        path_result["plateau"] = plateau_stat

        # Transient (gen=1-2, per paper §3.6.6 L0 vacuous)
        x, y, _ = select_subset(dcode, dpaper, path=path, alphas=alphas, gens=TRANSIENT_GENS)
        transient_stat = pearson_with_bootstrap(x, y, n_bootstrap=args.n_bootstrap,
                                                 seed=args.bootstrap_seed)
        transient_stat["tier"] = classify_tier(transient_stat["r"], transient_stat["p"],
                                               transient_stat["ci_lo"])
        path_result["transient"] = transient_stat

        # Per alpha breakdown
        path_result["per_alpha"] = {}
        for alpha in alphas:
            x, y, _ = select_subset(dcode, dpaper, path=path, alphas=[alpha], gens=None)
            alpha_stat = pearson_with_bootstrap(x, y, n_bootstrap=args.n_bootstrap,
                                                 seed=args.bootstrap_seed)
            alpha_stat["tier"] = classify_tier(alpha_stat["r"], alpha_stat["p"], alpha_stat["ci_lo"])
            path_result["per_alpha"][str(alpha)] = alpha_stat

        result["results_by_path"][path] = path_result

    # Cross-path consistency check (per design brief §6.1 之 row 5: B vs C 之 r 差异 > 50% → escalate)
    if len(paths) >= 2 and "B" in paths and "C" in paths:
        r_B = result["results_by_path"]["B"]["plateau"]["r"]
        r_C = result["results_by_path"]["C"]["plateau"]["r"]
        if r_B is not None and r_C is not None:
            mean_r = (abs(r_B) + abs(r_C)) / 2
            diff_pct = abs(r_B - r_C) / max(mean_r, 1e-6) * 100
            result["cross_path_consistency"] = {
                "r_B_plateau": r_B,
                "r_C_plateau": r_C,
                "diff_pct": float(diff_pct),
                "verdict": (
                    "L2 inconsistency — B vs C 之 r 差异 > 50%, sub-agent 推 路径 A escalate"
                    if diff_pct > 50
                    else "L2 consistent — B vs C 之 r 差异 < 50%"
                ),
            }

    # Write output
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n=== Pearson 分析 done ===")
    print(f"output: {args.output_json}")
    print(f"\nKey 之 数字 surface (D-1 binding: 不 declare close, 仅 surface):\n")
    for path in paths:
        for regime in ("full", "plateau", "transient"):
            r = result["results_by_path"][path][regime].get("r")
            tier = result["results_by_path"][path][regime].get("tier", "N/A")
            n = result["results_by_path"][path][regime].get("n", 0)
            print(f"  path={path} regime={regime} N={n} | tier: {tier}")
    if "cross_path_consistency" in result:
        print(f"\n  cross-path consistency: {result['cross_path_consistency']['verdict']}")
    print()
    print("D-1 binding 之 提醒: Pearson r tier 仅 surface, 不 binary close P0★-F.")
    print("真 binary close 由 关卡 3 反题 audit + 关卡 4 PI + DS + 反题 三方决.")


if __name__ == "__main__":
    main()
