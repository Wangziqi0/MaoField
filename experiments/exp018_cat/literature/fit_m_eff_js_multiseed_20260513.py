#!/usr/bin/env python3
"""
Multi-seed m_eff refit v2 — 修正 lower bound issue.

模型: log(P_n) = log(P_eq) + A * exp(-m_eff * n)
fit window: 从 peak (gen 2) 开始 fit, 让 envelope 真在 decay phase, gen 0/1 是 spike-up phase 不属 relaxation regime.
"""
import json, math, os, glob
from pathlib import Path
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import t as student_t

LOG_DIR = Path("/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/host22_backup_20260512")

def load_run(jsonl_path):
    ppl = {}
    with open(jsonl_path) as fp:
        for ln in fp:
            ln = ln.strip()
            if not ln: continue
            d = json.loads(ln)
            if d.get("stage") != "generation_done": continue
            g = int(d["generation"])
            p = float(d.get("test_perplexity", float("nan")))
            ppl[g] = p
    gens = sorted(ppl)
    return np.array(gens), np.array([ppl[g] for g in gens])

def exp_recovery(n, log_Peq, A, m_eff):
    return log_Peq + A * np.exp(-m_eff * n)

def fit_run(gens, ppls, start_gen=2):
    """Fit from gen=start_gen (peak) onward, capturing decay envelope.
    Removes spike-up phase (gen 0 baseline + gen 1 spike-up).
    Wider log_Peq lower bound to avoid hitting boundary.
    """
    n = gens.astype(float)
    logp = np.log(ppls)
    mask = (n >= start_gen) & np.isfinite(logp)
    n_f, logp_f = n[mask], logp[mask]
    if len(n_f) < 4:
        return None
    p0 = [3.8, 1.0, 0.3]
    bounds = ([1.0, 0.0, 0.001], [5.5, 5.0, 5.0])
    try:
        popt, pcov = curve_fit(exp_recovery, n_f, logp_f, p0=p0, bounds=bounds, maxfev=20000)
    except Exception as e:
        return {"error": str(e)}
    resid = logp_f - exp_recovery(n_f, *popt)
    rss = float(np.sum(resid**2))
    perr = np.sqrt(np.diag(pcov))
    return {
        "n_used": int(len(n_f)),
        "log_Peq": float(popt[0]),
        "A": float(popt[1]),
        "m_eff": float(popt[2]),
        "m_eff_se": float(perr[2]),
        "rss": rss,
    }

print("=" * 78)
print("Multi-seed m_eff refit v2 — fit from peak (gen 2) onward (decay regime only)")
print("=" * 78)

runs_alpha0 = sorted(glob.glob(str(LOG_DIR / "armb_alpha0.0_seed*.jsonl")))
print(f"\nα=0 multi-seed runs found: {len(runs_alpha0)}\n")

results = []
for path in runs_alpha0:
    name = os.path.basename(path)
    seed = name.split("seed")[1].split("_")[0]
    gens, ppls = load_run(path)
    print(f"--- α=0 seed={seed} ---")
    print(f"  gen 0..9 ppl: " + " ".join(f"{p:.2f}" for p in ppls))
    r = fit_run(gens, ppls, start_gen=2)
    if r and "error" not in r:
        Peq = math.exp(r["log_Peq"])
        print(f"  fit (n>=2): log(P_eq)={r['log_Peq']:.4f} (P_eq={Peq:.2f}), "
              f"A={r['A']:.4f}, m_eff={r['m_eff']:.4f} ± {r['m_eff_se']:.4f}, "
              f"RSS={r['rss']:.5f}, n_used={r['n_used']}")
        results.append({"seed": int(seed), **r})
    else:
        print(f"  fit failed: {r}")
    print()

m_effs = np.array([r["m_eff"] for r in results])
mean = float(np.mean(m_effs))
std = float(np.std(m_effs, ddof=1))
se = std / np.sqrt(len(m_effs))
df = len(m_effs) - 1
t_crit = student_t.ppf(0.975, df) if df > 0 else float("nan")
ci_lo = mean - t_crit * se
ci_hi = mean + t_crit * se

print("=" * 78)
print(f"N={len(m_effs)} multi-seed (α=0 seed 1/2/3/4) m_eff fit:")
print(f"  Per-seed m_eff: {[f'{m:.4f}' for m in m_effs]}")
print(f"  Mean = {mean:.4f}")
print(f"  SD  = {std:.4f}")
print(f"  SE  = {se:.4f}")
print(f"  95% CI (df={df}) = [{ci_lo:.4f}, {ci_hi:.4f}]")
print()
print(f"  vs 5/9 lock 0.2120 — Δ = {mean-0.212:+.4f} (z={(mean-0.212)/se:.2f})")
print(f"  vs Shumailov anchor 0.252 — Δ = {mean-0.252:+.4f}")
print(f"  vs Borji anchor mid 0.18 — Δ = {mean-0.18:+.4f}")
print(f"  vs ln 2 = 0.6931 — Δ = {mean-0.6931:+.4f}")
print("=" * 78)

# === J_S empirical fit ===
print("\n\n" + "=" * 78)
print("J_S empirical fit — Shumailov-style baseline early-stage drift")
print("=" * 78)
print()
print("Definition: J_S = d D_n / d n at gen 0+ — collapse 自然 drift rate")
print("Method: D_n = log(P_n) - log(P_0), J_S = slope of D from gen 0 to peak.")
print()

# 对每个 α=0 run, fit J_S 多种估计 (3 种方法 robustness)
js_results_method1 = []  # slope gen 0->1
js_results_method2 = []  # slope gen 0->2 (to peak)
js_results_method3 = []  # mean dD/dn over gen 0-3 (early collapse phase)
for r_idx, path in enumerate(runs_alpha0):
    name = os.path.basename(path)
    seed = name.split("seed")[1].split("_")[0]
    gens, ppls = load_run(path)
    logp = np.log(ppls)
    D_n = logp - logp[0]   # D_0 = 0
    js1 = D_n[1] - D_n[0]
    js2 = (D_n[2] - D_n[0]) / 2.0
    js3 = float(np.mean(np.diff(D_n[:4])))  # mean rate gen 0->3
    js_results_method1.append(js1)
    js_results_method2.append(js2)
    js_results_method3.append(js3)
    print(f"  seed={seed}: D_n[0..9] = " + " ".join(f"{d:.3f}" for d in D_n))
    print(f"    J_S^(1) (slope 0->1) = {js1:.4f} nat/gen")
    print(f"    J_S^(2) (slope 0->2 peak) = {js2:.4f} nat/gen")
    print(f"    J_S^(3) (mean rate 0->3) = {js3:.4f} nat/gen")

print()
print("Multi-seed N=4 statistics:")
for label, arr in [("J_S^(1) slope 0->1", js_results_method1),
                   ("J_S^(2) slope 0->2", js_results_method2),
                   ("J_S^(3) mean 0->3", js_results_method3)]:
    a = np.array(arr)
    m, s = a.mean(), a.std(ddof=1)
    se_ = s/np.sqrt(len(a))
    print(f"  {label}: mean = {m:.4f}, SD = {s:.4f}, SE = {se_:.4f}, "
          f"95% CI = [{m - student_t.ppf(0.975, len(a)-1)*se_:.4f}, "
          f"{m + student_t.ppf(0.975, len(a)-1)*se_:.4f}]")

print()
print(f"vs 5/9 paper §3.6 placeholder J_S = 0.075 nat/generation")
print("=" * 78)
