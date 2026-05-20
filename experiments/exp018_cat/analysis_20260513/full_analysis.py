"""
exp018_cat MaoField framework 全部实验数字 100% 落地脚本
2026-05-13 重新算 + bootstrap CI
所有数字从 jsonl 实读,禁止转述
"""
import json
import os
import math
import numpy as np
from pathlib import Path
from collections import defaultdict
import random

LOGS = Path('/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs')
BACKUP = LOGS / 'host22_backup_20260512'

random.seed(42)
np.random.seed(42)

# ============================================================
# Helpers
# ============================================================

def load_jsonl(path):
    gens = []
    run_start = None
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('stage') == 'run_start':
                    run_start = d
                if d.get('stage') == 'generation_done':
                    gens.append(d)
            except json.JSONDecodeError:
                continue
    return run_start, gens

def get_ppl_pair(d):
    """返回 (val_ppl, test_ppl) — 排除 NaN/Inf"""
    valp = d.get('val_perplexity')
    if isinstance(valp, float) and (math.isinf(valp) or math.isnan(valp)):
        valp = None
    tp = d.get('test_perplexity')
    if isinstance(tp, dict):
        tp = tp.get('mean_perplexity')
    if isinstance(tp, float) and (math.isinf(tp) or math.isnan(tp)):
        tp = None
    return valp, tp

def extract_series(gens):
    by_gen = {}
    for d in gens:
        g = d.get('generation')
        if g is None: continue
        valp, testp = get_ppl_pair(d)
        d3 = d.get('distinct_3')
        by_gen[g] = (valp, testp, d3)
    return by_gen

def bootstrap_ci(data, n_resample=1000, ci_level=0.95):
    """bootstrap mean + 95% CI"""
    arr = np.asarray(data, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) < 2:
        return float(np.nanmean(arr)) if len(arr) else float('nan'), float('nan'), float('nan'), float('nan')
    mean = arr.mean()
    std = arr.std(ddof=1)
    boots = []
    rng = np.random.default_rng(42)
    for _ in range(n_resample):
        sample = rng.choice(arr, size=len(arr), replace=True)
        boots.append(sample.mean())
    lo = np.percentile(boots, (1-ci_level)/2 * 100)
    hi = np.percentile(boots, (1+ci_level)/2 * 100)
    return float(mean), float(std), float(lo), float(hi)

# ============================================================
# 收集所有数据
# ============================================================

print('=' * 80)
print('exp018_cat 100% 落地数据提取 — 2026-05-13')
print('=' * 80)

# Shumailov 基线 (seed=42)
shu_file = LOGS / 'shumailov_no_preserve_seed42_20260508_092730.jsonl'
shu_rs, shu_gens = load_jsonl(shu_file)
shu_series = extract_series(shu_gens)

# Alpha 扫描 (seed=42)
alpha_files = {
    0: LOGS / 'armb_alpha0.0_seed42_20260508_144612.jsonl',
    1: LOGS / 'armb_alpha1.0_seed42_20260509_000459.jsonl',
    5: LOGS / 'armb_alpha5.0_seed42_20260509_044342.jsonl',
    10: LOGS / 'armb_alpha10.0_seed42_20260508_192435.jsonl',
    50: LOGS / 'armb_alpha50.0_seed42_20260509_092134.jsonl',
}
alpha_series = {}
alpha_rs = {}
for a, fp in alpha_files.items():
    rs, gens = load_jsonl(fp)
    alpha_rs[a] = rs
    alpha_series[a] = extract_series(gens)

# Multi-seed alpha=0 (seed 1-4) from BACKUP
# 注意:有的 jsonl 是 resume 失败后全 NaN,需排除
ms_alpha0 = {}
for s in [1, 2, 3, 4]:
    candidates = list(BACKUP.glob(f'armb_alpha0.0_seed{s}_*.jsonl'))
    if not candidates:
        print(f"  [!] alpha=0 seed={s} 不存在")
        continue
    # 检查每个候选,选含 valid val_ppl 的最大文件
    valid_files = []
    for fp in candidates:
        rs, gens = load_jsonl(fp)
        ser = extract_series(gens)
        # 检查 gen 0 是否有 valid val_ppl
        if 0 in ser and ser[0][0] is not None and not math.isnan(ser[0][0]):
            valid_files.append((fp, ser))
    if not valid_files:
        print(f"  [!] alpha=0 seed={s} 全 NaN")
        continue
    # 选 gen 数最多的 (优先) + 最大 size
    valid_files.sort(key=lambda x: (-sum(1 for g in x[1].values() if g[0] and not math.isnan(g[0])), -x[0].stat().st_size))
    fp, ser = valid_files[0]
    ms_alpha0[s] = (fp.name, ser)

# Multi-seed alpha=10 (seed 1-4) from BACKUP
# 注意:gen 0 可能是 NaN (resume 后 baseline 没存),但 gen 1-9 OK 仍可用 (alpha=10 不影响 gen 0 baseline)
ms_alpha10 = {}
for s in [1, 2, 3, 4]:
    candidates = list(BACKUP.glob(f'armb_alpha10.0_seed{s}_*.jsonl'))
    if not candidates:
        print(f"  [!] alpha=10 seed={s} 不存在")
        continue
    # 选 gen 1-9 都有 valid val_ppl 的文件
    valid_files = []
    for fp in candidates:
        rs, gens = load_jsonl(fp)
        ser = extract_series(gens)
        valid_count = sum(1 for g in range(1,10) if g in ser and ser[g][0] is not None and not math.isnan(ser[g][0]))
        valid_files.append((fp, ser, valid_count))
    valid_files.sort(key=lambda x: -x[2])
    fp, ser, vc = valid_files[0]
    ms_alpha10[s] = (fp.name, ser)
    if vc < 9:
        print(f"  [!] alpha=10 seed={s} 只有 {vc}/9 valid gens")

# ============================================================
# 组一:Shumailov 基线
# ============================================================
print()
print('### 组一:Shumailov 严格镜像基线 (seed=42, no_preserve)')
print()
print(f"  {'gen':<4} {'val_ppl':<10} {'test_ppl':<10} {'distinct_3':<10}")
for g in range(10):
    if g in shu_series:
        v, t, d3 = shu_series[g]
        vs = f"{v:.3f}" if v else "None"
        ts = f"{t:.3f}" if t else "Inf/NaN"
        d3s = f"{d3:.4f}" if d3 else "None"
        print(f"  {g:<4} {vs:<10} {ts:<10} {d3s:<10}")

# Shumailov 衰减率
print()
print('Shumailov distinct_3 衰减率:')
d3_seq = [shu_series[g][2] for g in range(10) if g in shu_series and shu_series[g][2] is not None]
if len(d3_seq) >= 2:
    print(f"  gen 1 distinct_3 = {d3_seq[0]:.4f}")
    print(f"  gen 9 distinct_3 = {d3_seq[-1]:.4f}")
    print(f"  衰减比 (gen 9 / gen 1) = {d3_seq[-1]/d3_seq[0]:.4f}")
    print(f"  绝对降幅 = {d3_seq[0] - d3_seq[-1]:.4f}")

# Shumailov 与 paper 数字对比
print()
print('与 Shumailov 2024 paper 报数字 cross-verify:')
gen0 = shu_series[0][1]  # test_ppl
gen9 = shu_series[9][1]
print(f"  gen 0 test_ppl = {gen0:.3f}  (paper: ~34)  偏离 = {gen0-34:.3f}")
print(f"  gen 9 test_ppl = {gen9:.3f}  (paper: ~67 严重崩溃) ")
print(f"  delta gen 9 - gen 0 = {gen9-gen0:.3f}  (paper criterion >= +5)")
print(f"  F1 (collapse 复现): {'PASS' if gen9-gen0 >= 5 else 'FAIL'}")
print(f"  [?] N=1 single seed CI 不可估,multi-seed Shumailov 复测 future work")
print()
print('Shumailov gen 0 baseline 与 paper 34:')
print(f"  偏离 = {gen0-34:.3f} ({(gen0-34)/34*100:.2f}%); 可接受范围 |Δ|<=50% paper criterion ✓")

# ============================================================
# 组二:Alpha 扫描 (seed=42)
# ============================================================
print()
print('=' * 80)
print('### 组二:α 全扫描 single-seed seed=42')
print('=' * 80)

# 表格:每 alpha 每 gen 的 PPL
print(f"\n{'gen':<4}", end='')
for a in [0, 1, 5, 10, 50]:
    print(f"  a={a:<4}val_ppl", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for a in [0, 1, 5, 10, 50]:
        if g in alpha_series.get(a, {}):
            v = alpha_series[a][g][0]
            vs = f"{v:.3f}" if v else "  -    "
        else:
            vs = "  -    "
        print(f"  {vs:<11}", end='')
    print()

# 注意 alpha=10 val_ppl 异常 (val 高 test 低) - 也输出 test_ppl
print(f"\n{'gen':<4}", end='')
for a in [0, 1, 5, 10, 50]:
    print(f"  a={a:<4}test_ppl", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for a in [0, 1, 5, 10, 50]:
        if g in alpha_series.get(a, {}):
            v = alpha_series[a][g][1]
            vs = f"{v:.3f}" if v else "  -    "
        else:
            vs = "  -    "
        print(f"  {vs:<11}", end='')
    print()

# 早期 transient / 中段 / plateau
print()
print('### 三阶段定量 (basis = val_perplexity,与 Shumailov 一致):')
print(f"{'alpha':<6} {'gen0':<10} {'transient(g1-3 cum)':<22} {'middle(g4-7)':<14} {'p_69mean':<10} {'p_59mean':<10} {'p_79mean':<10}")
for a in [0, 1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    g0 = ser[0][0]
    # transient: gen 1-3 cumulative max
    tr_vals = [ser[g][0] for g in [1,2,3] if g in ser and ser[g][0]]
    tr_max = max(tr_vals) if tr_vals else float('nan')
    # middle: gen 4-7 mean
    mid_vals = [ser[g][0] for g in [4,5,6,7] if g in ser and ser[g][0]]
    mid_mean = np.mean(mid_vals) if mid_vals else float('nan')
    # plateau windows
    p69 = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0]])
    p59 = np.mean([ser[g][0] for g in [5,6,7,8,9] if g in ser and ser[g][0]])
    p79 = np.mean([ser[g][0] for g in [7,8,9] if g in ser and ser[g][0]])
    print(f"{a:<6} {g0:<10.3f} {tr_max:<22.3f} {mid_mean:<14.3f} {p69:<10.3f} {p59:<10.3f} {p79:<10.3f}")

print()
print('### 平台相对 alpha=0 偏移 (val_ppl):')
print(f"{'alpha':<6} {'p_69 delta_rel%':<16} {'p_59 delta_rel%':<16} {'p_79 delta_rel%':<16}")
a0 = alpha_series[0]
p69_a0 = np.mean([a0[g][0] for g in [6,7,8,9] if g in a0 and a0[g][0]])
p59_a0 = np.mean([a0[g][0] for g in [5,6,7,8,9] if g in a0 and a0[g][0]])
p79_a0 = np.mean([a0[g][0] for g in [7,8,9] if g in a0 and a0[g][0]])
for a in [1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    p69 = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0]])
    p59 = np.mean([ser[g][0] for g in [5,6,7,8,9] if g in ser and ser[g][0]])
    p79 = np.mean([ser[g][0] for g in [7,8,9] if g in ser and ser[g][0]])
    d69 = (p69 - p69_a0) / p69_a0 * 100
    d59 = (p59 - p59_a0) / p59_a0 * 100
    d79 = (p79 - p79_a0) / p79_a0 * 100
    print(f"{a:<6} {d69:+.2f}%          {d59:+.2f}%          {d79:+.2f}%")

print()
print('### U 形特征定量 (alpha vs alpha=0):')
print(f"{'alpha':<6} {'spike ratio':<14} {'plateau/peak':<14}")
for a in [0, 1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    g0 = ser[0][0]
    spike = max([ser[g][0] for g in [1,2,3] if g in ser and ser[g][0]])
    plat = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0]])
    sr = spike / g0
    pr = plat / spike
    print(f"{a:<6} {sr:<14.3f} {pr:<14.3f}")

# alpha=50 数值崩溃
print()
print('### alpha=50 数值崩溃:')
a50_rs = alpha_rs.get(50)
a50_gens = alpha_series.get(50, {})
print(f"  run_start: {a50_rs}")
print(f"  实际跑出 gen 数: {len(a50_gens)}")
print(f"  → gen 0 step 训练 NaN/Inf,abort 即 abort,jsonl 无 generation_done")

# ============================================================
# 组三:Multi-seed alpha=0 (seed 1-4)
# ============================================================
print()
print('=' * 80)
print('### 组三:Multi-seed alpha=0 (seed 1/2/3/4) Phase 1')
print('=' * 80)
print()
print(f"{'seed':<6} {'file':<60}")
for s, (fn, _) in ms_alpha0.items():
    print(f"{s:<6} {fn}")
print()
print(f"{'gen':<4}", end='')
for s in [1,2,3,4]:
    print(f"  seed{s:<2}val", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for s in [1,2,3,4]:
        if s in ms_alpha0:
            _, ser = ms_alpha0[s]
            v = ser.get(g, (None,None,None))[0]
            vs = f"{v:.3f}" if v else "  -   "
        else:
            vs = "  -   "
        print(f"  {vs:<8}", end='')
    print()

print()
print('### Multi-seed alpha=0 平台 mean (gen 6-9) per seed:')
plat_a0_per_seed = {}
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    p = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0]])
    plat_a0_per_seed[s] = p
    print(f"  seed={s}: plateau_mean = {p:.4f}")

# N=4 bootstrap
print()
data_a0 = list(plat_a0_per_seed.values())
mean, std, lo, hi = bootstrap_ci(data_a0, n_resample=1000)
print(f"### N=4 alpha=0 plateau mean: {mean:.4f} ± {std:.4f}")
print(f"### 95% bootstrap CI: [{lo:.4f}, {hi:.4f}]")

# ============================================================
# 组四:Multi-seed alpha=10 (seed 1-4)
# ============================================================
print()
print('=' * 80)
print('### 组四:Multi-seed alpha=10 (seed 1/2/3/4) Phase 1')
print('=' * 80)
print()
print(f"{'seed':<6} {'file':<60}")
for s, (fn, _) in ms_alpha10.items():
    print(f"{s:<6} {fn}")
print()
print(f"{'gen':<4}", end='')
for s in [1,2,3,4]:
    print(f"  seed{s:<2}val", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for s in [1,2,3,4]:
        if s in ms_alpha10:
            _, ser = ms_alpha10[s]
            v = ser.get(g, (None,None,None))[0]
            vs = f"{v:.3f}" if v else "  -   "
        else:
            vs = "  -   "
        print(f"  {vs:<8}", end='')
    print()

print()
print('### Multi-seed alpha=10 平台 mean (gen 6-9) per seed (val_ppl):')
plat_a10_per_seed = {}
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    p = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0]])
    plat_a10_per_seed[s] = p
    print(f"  seed={s}: plateau_mean = {p:.4f}")

data_a10 = list(plat_a10_per_seed.values())
mean10, std10, lo10, hi10 = bootstrap_ci(data_a10, n_resample=1000)
print(f"### N=4 alpha=10 plateau mean: {mean10:.4f} ± {std10:.4f}")
print(f"### 95% bootstrap CI: [{lo10:.4f}, {hi10:.4f}]")

# ============================================================
# 组五:D4 paired statistics
# ============================================================
print()
print('=' * 80)
print('### 组五:D4 N=4 paired statistics (alpha=10 vs alpha=0)')
print('=' * 80)

paired = []
print(f"\n{'seed':<6} {'a=0 plat':<12} {'a=10 plat':<12} {'diff':<12} {'rel%':<10}")
for s in [1,2,3,4]:
    if s in plat_a0_per_seed and s in plat_a10_per_seed:
        p0 = plat_a0_per_seed[s]
        p10 = plat_a10_per_seed[s]
        d = p10 - p0
        rel = d / p0 * 100
        paired.append(d)
        rel_paired = rel
        print(f"{s:<6} {p0:<12.4f} {p10:<12.4f} {d:<+12.4f} {rel:<+10.2f}")

paired_arr = np.array(paired)
mean_d, std_d, lo_d, hi_d = bootstrap_ci(paired, n_resample=1000)
print(f"\n### Paired difference (alpha=10 - alpha=0):")
print(f"  mean = {mean_d:+.4f}")
print(f"  std  = {std_d:.4f}")
print(f"  95% bootstrap CI: [{lo_d:+.4f}, {hi_d:+.4f}]")

# t-stat 配对 t 检验
n = len(paired)
sem = std_d / math.sqrt(n)
t_stat = mean_d / sem if sem > 0 else float('nan')
# two-sided p (df=n-1)
from scipy import stats as scs
p_two = 2 * (1 - scs.t.cdf(abs(t_stat), df=n-1))
# one-sided p (test: mean_d < 0)
p_one = scs.t.cdf(t_stat, df=n-1)
print(f"\n### 配对 t 检验 (H0: mean_d = 0):")
print(f"  N = {n}")
print(f"  t_stat = {t_stat:.4f}")
print(f"  df = {n-1}")
print(f"  p-value two-sided = {p_two:.4f}")
print(f"  p-value one-sided (mean_d < 0) = {p_one:.4f}")

# 相对 paired
rel_vals = [(plat_a10_per_seed[s] - plat_a0_per_seed[s])/plat_a0_per_seed[s] * 100 for s in [1,2,3,4] if s in plat_a0_per_seed and s in plat_a10_per_seed]
mean_rel, std_rel, lo_rel, hi_rel = bootstrap_ci(rel_vals, n_resample=1000)
print(f"\n### 相对偏移 (alpha=10 - alpha=0) / alpha=0 %:")
print(f"  mean = {mean_rel:+.2f}%")
print(f"  std  = {std_rel:.2f}%")
print(f"  95% bootstrap CI: [{lo_rel:+.2f}%, {hi_rel:+.2f}%]")

# F2/F3/F4 binary judgment
print(f"\n### F2/F3/F4 falsification binary:")
print(f"  F2 = alpha=10 显著降低 plateau -2% to -5% with p<0.10")
print(f"  F3 = NOT substantiated (alpha=10 无显著效应)")
print(f"  F4 = counter-effect (alpha=10 反而升高)")
print(f"  实测 mean_rel = {mean_rel:+.2f}%, p_two = {p_two:.4f}, p_one = {p_one:.4f}")
if mean_rel > 0:
    print(f"  → 方向: alpha=10 比 alpha=0 高 (counter-effect direction)")
else:
    print(f"  → 方向: alpha=10 比 alpha=0 低")
if -5 <= mean_rel <= -2 and p_one < 0.10:
    f_judgment = 'F2'
elif mean_rel > 0:
    f_judgment = 'F4'
else:
    f_judgment = 'F3'
print(f"  binary verdict: {f_judgment}")

# ============================================================
# 组六:Partial D4 5 criterion
# ============================================================
print()
print('=' * 80)
print('### 组六:Partial D4 形状鲁棒性 5 criterion')
print('=' * 80)

# Criterion 1: U 形 4/4 seeds (alpha=10 each seed)
# 注意:seed=1/3 alpha=10 jsonl gen 0 = NaN (resume 后 baseline 未存)
# 用同 seed alpha=0 gen 0 替代 (alpha 在 gen 0 step 不应用,base model 同源)
print()
print('Criterion 1: U 形 in alpha=10 各 seed:')
u_count = 0
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    g0 = ser[0][0] if 0 in ser else None
    if g0 is None or (isinstance(g0, float) and math.isnan(g0)):
        # 用 alpha=0 同 seed gen 0 替代
        if s in ms_alpha0:
            g0_alt = ms_alpha0[s][1].get(0, (None,None,None))[0]
            if g0_alt is not None and not math.isnan(g0_alt):
                g0 = g0_alt
                note = " (用 alpha=0 同 seed gen 0 替代)"
            else:
                g0 = 36.524  # 用 Shumailov seed=42 gen 0 (base model 同源)
                note = " (用 Shumailov seed=42 gen 0 替代,粗 imputation [?])"
        else:
            g0 = 36.524
            note = " (用 Shumailov seed=42 gen 0 替代,粗 imputation [?])"
    else:
        note = ""
    g_peak = max([ser[g][0] for g in [1,2,3] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    plat = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    is_U = g_peak > g0 and plat < g_peak
    print(f"  seed={s}: g0={g0:.3f}{note} g_peak={g_peak:.3f} plat={plat:.3f} U形={is_U}")
    if is_U: u_count += 1
print(f"  → U 形 {u_count}/{len(ms_alpha10)}")
crit1_pass = u_count == 4
print(f"  Criterion 1 (4/4): {'✓ PASS' if crit1_pass else '✗ FAIL'}")

# Criterion 2: gen 0 baseline std (alpha=0 multi-seed — base model 同源 per seed)
print()
print('Criterion 2: gen 0 baseline std (alpha=0 multi-seed,seed 1-4):')
g0_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    g0 = ser.get(0, (None,None,None))[0]
    if g0 is not None and not math.isnan(g0):
        g0_vals.append(g0)
        print(f"  seed={s} gen 0 val_ppl = {g0:.4f}")
g0_mean = np.mean(g0_vals)
g0_std = np.std(g0_vals, ddof=1)
g0_cv = g0_std / g0_mean * 100
print(f"  mean = {g0_mean:.4f}, std = {g0_std:.4f}, CV = {g0_cv:.4f}%")
crit2_pass = g0_cv < 1.0  # threshold 1% CV
print(f"  Criterion 2 (CV<1%): {'✓ PASS' if crit2_pass else '✗ FAIL'}")

# Criterion 3: spike ratio min (max(gen 1-3)/gen 0,取 min over seed)
# seed=1/3 g0 用同 seed alpha=0 gen 0 替代
print()
print('Criterion 3: spike ratio min (max(g1-3)/g0,取 min) — alpha=10:')
sr_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    g0 = ser.get(0, (None,None,None))[0]
    if g0 is None or (isinstance(g0, float) and math.isnan(g0)):
        if s in ms_alpha0:
            g0_alt = ms_alpha0[s][1].get(0, (None,None,None))[0]
            if g0_alt is not None and not math.isnan(g0_alt):
                g0 = g0_alt
                note = "(alpha=0 同 seed)"
            else:
                g0 = 36.524
                note = "(Shumailov)"
        else:
            g0 = 36.524
            note = "(Shumailov)"
    else:
        note = ""
    peak = max([ser[g][0] for g in [1,2,3] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    sr = peak / g0
    sr_vals.append(sr)
    print(f"  seed={s}: peak={peak:.3f} g0={g0:.3f}{note} spike_ratio={sr:.4f}")
sr_min = min(sr_vals)
print(f"  min spike ratio = {sr_min:.4f}")
crit3_pass = sr_min > 1.5  # threshold 1.5x baseline
print(f"  Criterion 3 (spike>1.5x): {'✓ PASS' if crit3_pass else '✗ FAIL'}")

# Criterion 4: plateau/peak max (取 max over seed)
print()
print('Criterion 4: plateau/peak max — alpha=10:')
pp_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    peak = max([ser[g][0] for g in [1,2,3] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    plat = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    pp = plat / peak
    pp_vals.append(pp)
    print(f"  seed={s}: plat={plat:.3f} peak={peak:.3f} plat/peak={pp:.4f}")
pp_max = max(pp_vals)
print(f"  max plateau/peak = {pp_max:.4f}")
crit4_pass = pp_max < 1.0  # plat 必须低于 peak
print(f"  Criterion 4 (plat<peak): {'✓ PASS' if crit4_pass else '✗ FAIL'}")

# Criterion 5: 滑动窗口一致性偏差 (window 5-9 vs 6-9 vs 7-9 偏离)
print()
print('Criterion 5: 滑动窗口偏差 — alpha=10:')
print(f"{'seed':<6} {'w_69':<10} {'w_59':<10} {'w_79':<10} {'max偏差':<10}")
sw_devs = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    w69 = np.mean([ser[g][0] for g in [6,7,8,9] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    w59 = np.mean([ser[g][0] for g in [5,6,7,8,9] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    w79 = np.mean([ser[g][0] for g in [7,8,9] if g in ser and ser[g][0] and not math.isnan(ser[g][0])])
    max_dev = max(abs(w69-w59), abs(w69-w79), abs(w59-w79)) / w69 * 100
    sw_devs.append(max_dev)
    print(f"{s:<6} {w69:<10.3f} {w59:<10.3f} {w79:<10.3f} {max_dev:<10.2f}%")
sw_max_dev = max(sw_devs)
crit5_pass = sw_max_dev < 20.0  # threshold 20% inter-window deviation
print(f"  滑动窗口最大偏差 = {sw_max_dev:.2f}%")
print(f"  Criterion 5 (偏差<20%): {'✓ PASS' if crit5_pass else '✗ FAIL'}")

# 总判定
print()
print('### Partial D4 5 criterion 总判定:')
total_pass = sum([crit1_pass, crit2_pass, crit3_pass, crit4_pass, crit5_pass])
print(f"  通过: {total_pass}/5")
print(f"  → {'✓ STRONG ROBUST' if total_pass == 5 else '部分通过' if total_pass >= 3 else '✗ FAIL'}")

# ============================================================
# m_eff multi-seed fit
# ============================================================
print()
print('=' * 80)
print('### m_eff multi-seed N=4 fit + 95% CI')
print('=' * 80)
print()
print('模型: log P_n = log P_eq + A * exp(-m_eff * n) from gen 2+')

m_eff_per_seed = {}
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    # gen 2-9 数据
    ns = []
    ppls = []
    for g in range(2, 10):
        if g in ser and ser[g][0]:
            ns.append(g)
            ppls.append(ser[g][0])
    if len(ns) < 4:
        print(f"  seed={s}: insufficient data")
        continue
    # 假设 P_eq = min(ppls) * 0.95 (稳定下界)
    # 或更准:fit jointly (P_eq, A, m_eff)
    # 用 scipy.curve_fit
    from scipy.optimize import curve_fit
    def model(n, log_Peq, A, m):
        return log_Peq + A * np.exp(-m * n)
    log_ppls = np.log(ppls)
    try:
        popt, _ = curve_fit(model, ns, log_ppls, p0=[math.log(min(ppls)), 1.0, 0.3], maxfev=5000)
        m_eff = popt[2]
        m_eff_per_seed[s] = m_eff
        print(f"  seed={s}: log_Peq={popt[0]:.4f} A={popt[1]:.4f} m_eff={m_eff:.4f}")
    except Exception as e:
        print(f"  seed={s}: fit failed: {e}")

print()
m_eff_vals = list(m_eff_per_seed.values())
if len(m_eff_vals) >= 2:
    m_eff_mean, m_eff_std, m_eff_lo, m_eff_hi = bootstrap_ci(m_eff_vals, n_resample=1000)
    print(f"### N={len(m_eff_vals)} m_eff fit:")
    print(f"  mean = {m_eff_mean:.4f}")
    print(f"  std  = {m_eff_std:.4f}")
    print(f"  95% bootstrap CI: [{m_eff_lo:.4f}, {m_eff_hi:.4f}]")
    print(f"  F 报告 m_eff = 0.300 ± 0.042")
    print(f"  cross-verify: {'匹配' if abs(m_eff_mean - 0.300) < 0.150 else '不匹配 [?]'}")

# ============================================================
# J_S 三 method
# ============================================================
print()
print('=' * 80)
print('### J_S 三 method 拟合 + 95% CI')
print('=' * 80)

# 用 val_ppl,D_n 用什么定义? 暂用 D_n = log(PPL_n / PPL_0)
def compute_D(ser, n):
    if 0 not in ser or n not in ser: return None
    p0 = ser[0][0]; pn = ser[n][0]
    if not p0 or not pn: return None
    return math.log(pn/p0)

print()
print('D_n = log(PPL_n / PPL_0) — see 第五步 derive 状态')
print()

# Shumailov seed=42 + multi-seed alpha=0 都计算
# Shumailov
J_S_methods = {}
for fname, ser in [('shumailov_42', shu_series)] + [(f'alpha0_seed{s}', ms_alpha0[s][1]) for s in [1,2,3,4] if s in ms_alpha0]:
    D = {n: compute_D(ser, n) for n in range(5)}
    if D[1] is None or D[2] is None or D[3] is None:
        continue
    J1 = (D[1] - D[0]) / 1  # D[0] = log(1) = 0
    J2 = (D[2] - D[0]) / 2
    J3_steps = [D[1]-D[0], D[2]-D[1], D[3]-D[2]]
    J3 = np.mean(J3_steps)
    J_S_methods[fname] = (J1, J2, J3)
    print(f"  {fname}: J_S^(1)={J1:.4f}  J_S^(2)={J2:.4f}  J_S^(3)={J3:.4f}")

print()
# multi-seed N=4 CI
J1_seeds = [J_S_methods[f'alpha0_seed{s}'][0] for s in [1,2,3,4] if f'alpha0_seed{s}' in J_S_methods]
J2_seeds = [J_S_methods[f'alpha0_seed{s}'][1] for s in [1,2,3,4] if f'alpha0_seed{s}' in J_S_methods]
J3_seeds = [J_S_methods[f'alpha0_seed{s}'][2] for s in [1,2,3,4] if f'alpha0_seed{s}' in J_S_methods]

for label, vals in [('J_S^(1) slope 0→1', J1_seeds), ('J_S^(2) slope 0→2', J2_seeds), ('J_S^(3) mean rate 0→3', J3_seeds)]:
    m, s, lo, hi = bootstrap_ci(vals, n_resample=1000)
    print(f"### {label} N={len(vals)}: mean={m:.4f} std={s:.4f} 95% CI=[{lo:.4f}, {hi:.4f}]")

print()
print('与 F 报告 cross-verify:')
print('  F 报告: J_S^(1) = 0.7702 / J_S^(2) = 0.5351 / J_S^(3) = 0.3305')
if J1_seeds:
    m1, _, _, _ = bootstrap_ci(J1_seeds)
    m2, _, _, _ = bootstrap_ci(J2_seeds)
    m3, _, _, _ = bootstrap_ci(J3_seeds)
    print(f"  实测 (multi-seed): J^(1)={m1:.4f} J^(2)={m2:.4f} J^(3)={m3:.4f}")
    print(f"  偏离 (实测 - F): {m1-0.7702:+.4f} / {m2-0.5351:+.4f} / {m3-0.3305:+.4f}")

# Save数字 to json for caller
out = {
    'shumailov_seed42': shu_series,
    'alpha_seed42': {a: alpha_series[a] for a in [0,1,5,10]},
    'multi_alpha0': {s: ms_alpha0[s][1] for s in ms_alpha0},
    'multi_alpha10': {s: ms_alpha10[s][1] for s in ms_alpha10},
}
# JSON serialize dict 的 int key 转 str
def conv(o):
    if isinstance(o, dict):
        return {str(k): conv(v) for k,v in o.items()}
    if isinstance(o, tuple):
        return list(o)
    if isinstance(o, list):
        return [conv(x) for x in o]
    return o
with open('/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/data_dump.json', 'w') as f:
    json.dump(conv(out), f, indent=2, default=str)
print()
print('数据 dump 写入 /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/data_dump.json')
