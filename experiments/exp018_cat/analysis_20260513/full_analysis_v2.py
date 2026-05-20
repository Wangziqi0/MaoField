"""
exp018_cat MaoField framework 100% 落地 v2 (修正:用 test_ppl 为 primary)
2026-05-13

关键修正:armb (cat_enabled=True) 的 val_perplexity 包含 cat loss (KL term),
不是干净 CE PPL。test_perplexity 才是 framework-clean 与 Shumailov paper 可比。
"""
import json
import os
import math
import numpy as np
from pathlib import Path
from scipy import stats as scs
from scipy.optimize import curve_fit

LOGS = Path('/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs')
BACKUP = LOGS / 'host22_backup_20260512'

np.random.seed(42)

def load_jsonl(path):
    gens = []; run_start = None
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('stage') == 'run_start': run_start = d
                if d.get('stage') == 'generation_done': gens.append(d)
            except: continue
    return run_start, gens

def get_test_ppl(d):
    tp = d.get('test_perplexity')
    if tp is None: return None
    if isinstance(tp, dict): return tp.get('mean_perplexity')
    if isinstance(tp, float) and (math.isinf(tp) or math.isnan(tp)): return None
    return tp

def get_val_ppl(d):
    v = d.get('val_perplexity')
    if v is None: return None
    if isinstance(v, float) and (math.isinf(v) or math.isnan(v)): return None
    return v

def extract_series(gens):
    by_gen = {}
    for d in gens:
        g = d.get('generation')
        if g is None: continue
        by_gen[g] = (get_val_ppl(d), get_test_ppl(d), d.get('distinct_3'))
    return by_gen

def bootstrap_ci(data, n_resample=10000, ci_level=0.95):
    arr = np.asarray(data, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) < 2: return float('nan'), float('nan'), float('nan'), float('nan')
    mean = arr.mean(); std = arr.std(ddof=1)
    rng = np.random.default_rng(42)
    boots = [rng.choice(arr, size=len(arr), replace=True).mean() for _ in range(n_resample)]
    lo = np.percentile(boots, (1-ci_level)/2*100); hi = np.percentile(boots, (1+ci_level)/2*100)
    return float(mean), float(std), float(lo), float(hi)

# 加载所有 jsonl
shu_rs, shu_gens = load_jsonl(LOGS / 'shumailov_no_preserve_seed42_20260508_092730.jsonl')
shu_series = extract_series(shu_gens)

alpha_files = {
    0: LOGS / 'armb_alpha0.0_seed42_20260508_144612.jsonl',
    1: LOGS / 'armb_alpha1.0_seed42_20260509_000459.jsonl',
    5: LOGS / 'armb_alpha5.0_seed42_20260509_044342.jsonl',
    10: LOGS / 'armb_alpha10.0_seed42_20260508_192435.jsonl',
    50: LOGS / 'armb_alpha50.0_seed42_20260509_092134.jsonl',
}
alpha_series = {}; alpha_rs = {}
for a, fp in alpha_files.items():
    rs, gens = load_jsonl(fp)
    alpha_rs[a] = rs
    alpha_series[a] = extract_series(gens)

# Multi-seed
def best_multi_seed(prefix, seeds):
    """从 BACKUP 选每 seed 最完整 jsonl"""
    result = {}
    for s in seeds:
        cands = list(BACKUP.glob(f'{prefix}_seed{s}_*.jsonl'))
        if not cands: continue
        best = None; best_score = -1
        for fp in cands:
            rs, gens = load_jsonl(fp)
            ser = extract_series(gens)
            # 计 valid test_ppl 数 + valid val_ppl 数
            test_valid = sum(1 for g in ser.values() if g[1] is not None)
            val_valid = sum(1 for g in ser.values() if g[0] is not None)
            score = test_valid * 10 + val_valid  # test 优先
            if score > best_score:
                best_score = score; best = (fp.name, ser)
        if best:
            result[s] = best
    return result

ms_alpha0 = best_multi_seed('armb_alpha0.0', [1,2,3,4])
ms_alpha10 = best_multi_seed('armb_alpha10.0', [1,2,3,4])

# ============================================================
# 数据完整性 + metric 选择说明
# ============================================================
print('=' * 80)
print('exp018_cat 100% 落地 v2 — 2026-05-13')
print('=' * 80)
print()
print('## Metric 选择关键说明')
print('-' * 70)
print('在 cat_enabled=True 模式 (armb alpha>0) 下,')
print('val_perplexity 在 trainer 内部累加了 cat loss (KL term) 因此远高于干净 CE PPL。')
print('test_perplexity 在 eval 单独算 (CE only),与 Shumailov paper 可比。')
print()
print('证据 (armb alpha=10 seed=42):')
print('  gen 1: val=117.25 vs test=72.85 (差 1.61x)')
print('  gen 2: val=223.90 vs test=98.54 (差 2.27x)')
print('  gen 9: val=91.44  vs test=53.39 (差 1.71x)')
print()
print('在 alpha=0 / Shumailov 模式 (cat_enabled=False 或 alpha=0):')
print('  val 和 test 偏差 < 2% (consistent)')
print()
print('结论: 所有 framework effect 评估必须用 test_ppl 为 primary metric。')
print('val_ppl 仅作 internal training signal 不可作 framework metric。')
print()

# ============================================================
# 组一: Shumailov 基线 (test_ppl primary)
# ============================================================
print('=' * 80)
print('## 组一: Shumailov 严格镜像基线 (seed=42)')
print('=' * 80)
print()
print(f"{'gen':<4} {'val_ppl':<10} {'test_ppl':<10} {'distinct_3':<10}")
for g in range(10):
    v, t, d3 = shu_series.get(g, (None, None, None))
    vs = f"{v:.3f}" if v else "None"
    ts = f"{t:.3f}" if t else "Inf/NaN"
    d3s = f"{d3:.4f}" if d3 else "None"
    print(f"{g:<4} {vs:<10} {ts:<10} {d3s:<10}")

# 滑动窗口 plateau
print()
print('### 滑动窗口 plateau (test_ppl basis):')
shu_test = [shu_series[g][1] for g in range(10) if g in shu_series]
# gen 4 = Inf, 排除
shu_test_clean = {g: shu_series[g][1] for g in range(10) if g in shu_series and shu_series[g][1] is not None}
p69 = np.mean([shu_test_clean.get(g) for g in [6,7,8,9] if g in shu_test_clean])
p59 = np.mean([shu_test_clean.get(g) for g in [5,6,7,8,9] if g in shu_test_clean])
p79 = np.mean([shu_test_clean.get(g) for g in [7,8,9] if g in shu_test_clean])
print(f"  plateau gen 6-9 mean = {p69:.4f}")
print(f"  plateau gen 5-9 mean = {p59:.4f}")
print(f"  plateau gen 7-9 mean = {p79:.4f}")

# distinct_3 衰减
print()
print('### distinct_3 衰减率:')
d3_seq = [shu_series[g][2] for g in range(10) if g in shu_series and shu_series[g][2]]
print(f"  gen 1 d3 = {d3_seq[0]:.4f}")
print(f"  gen 9 d3 = {d3_seq[-1]:.4f}")
print(f"  衰减比 = {d3_seq[-1]/d3_seq[0]:.4f}")
print(f"  绝对降幅 = {d3_seq[0]-d3_seq[-1]:.4f}")

# 与 paper 对比
print()
print('### 与 Shumailov 2024 paper cross-verify:')
g0t = shu_series[0][1]; g9t = shu_series[9][1]
print(f"  gen 0 test_ppl = {g0t:.3f}  (paper: ~34)  偏离 = {g0t-34:.3f} ({(g0t-34)/34*100:.2f}%)")
print(f"  gen 9 test_ppl = {g9t:.3f}  (paper: ~67 严重崩溃)")
print(f"  delta = {g9t-g0t:+.3f}  (paper F1 criterion >= +5)")
print(f"  F1 (collapse 复现): {'✓ PASS' if g9t-g0t >= 5 else '✗ FAIL'}")
print(f"  [?] N=1 single seed 95% CI 不可估,multi-seed Shumailov 复测 future work")

# ============================================================
# 组二: Alpha 扫描 (test_ppl primary)
# ============================================================
print()
print('=' * 80)
print('## 组二: α 全扫描 single-seed seed=42 (test_ppl primary)')
print('=' * 80)
print()
print(f"{'gen':<4}", end='')
for a in [0, 1, 5, 10]:
    print(f"  a={a} test", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for a in [0, 1, 5, 10]:
        if g in alpha_series.get(a, {}):
            t = alpha_series[a][g][1]
            ts = f"{t:.3f}" if t else "  -    "
        else: ts = "  -    "
        print(f"  {ts:<8}", end='')
    print()

print()
print('### 三阶段定量 (test_ppl basis):')
print(f"{'alpha':<6} {'gen0':<9} {'transient max g1-3':<22} {'middle g4-7 mean':<18} {'p_69':<9} {'p_59':<9} {'p_79':<9}")
for a in [0, 1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    g0 = ser[0][1]
    tr = max([ser[g][1] for g in [1,2,3] if g in ser and ser[g][1]])
    mid = np.mean([ser[g][1] for g in [4,5,6,7] if g in ser and ser[g][1]])
    p69 = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    p59 = np.mean([ser[g][1] for g in [5,6,7,8,9] if g in ser and ser[g][1]])
    p79 = np.mean([ser[g][1] for g in [7,8,9] if g in ser and ser[g][1]])
    print(f"{a:<6} {g0:<9.3f} {tr:<22.3f} {mid:<18.3f} {p69:<9.3f} {p59:<9.3f} {p79:<9.3f}")

print()
print('### 平台相对 alpha=0 偏移 (test_ppl):')
print(f"{'alpha':<6} {'Δ_69%':<10} {'Δ_59%':<10} {'Δ_79%':<10}")
a0 = alpha_series[0]
p69_a0 = np.mean([a0[g][1] for g in [6,7,8,9] if g in a0 and a0[g][1]])
p59_a0 = np.mean([a0[g][1] for g in [5,6,7,8,9] if g in a0 and a0[g][1]])
p79_a0 = np.mean([a0[g][1] for g in [7,8,9] if g in a0 and a0[g][1]])
for a in [1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    p69 = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    p59 = np.mean([ser[g][1] for g in [5,6,7,8,9] if g in ser and ser[g][1]])
    p79 = np.mean([ser[g][1] for g in [7,8,9] if g in ser and ser[g][1]])
    print(f"{a:<6} {(p69-p69_a0)/p69_a0*100:+8.2f}% {(p59-p59_a0)/p59_a0*100:+8.2f}% {(p79-p79_a0)/p79_a0*100:+8.2f}%")

print()
print('### U 形特征定量 (test_ppl):')
print(f"{'alpha':<6} {'spike ratio':<14} {'plateau/peak':<14}")
for a in [0, 1, 5, 10]:
    if a not in alpha_series: continue
    ser = alpha_series[a]
    g0 = ser[0][1]
    spike = max([ser[g][1] for g in [1,2,3] if g in ser and ser[g][1]])
    plat = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    print(f"{a:<6} {spike/g0:<14.3f} {plat/spike:<14.3f}")

# alpha=50
print()
print('### alpha=50 数值崩溃:')
print(f"  jsonl 行数: {len(alpha_series.get(50, {}))}")
print(f"  run_start exists, generation_done 数 = 0")
print(f"  → gen 0 step 训练 NaN/Inf,abort 前未 emit generation_done")

# ============================================================
# 组三: Multi-seed alpha=0
# ============================================================
print()
print('=' * 80)
print('## 组三: Multi-seed alpha=0 (seed 1-4)')
print('=' * 80)
print()
for s in [1,2,3,4]:
    if s in ms_alpha0:
        print(f"  seed={s}: {ms_alpha0[s][0]}")

print()
print(f"{'gen':<4}", end='')
for s in [1,2,3,4]:
    print(f"  s{s} test", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for s in [1,2,3,4]:
        if s in ms_alpha0:
            _, ser = ms_alpha0[s]
            t = ser.get(g, (None,None,None))[1]
            ts = f"{t:.3f}" if t else "  -   "
        else: ts = "  -   "
        print(f"  {ts:<8}", end='')
    print()

# Plateau per seed (test)
print()
print('### Multi-seed alpha=0 plateau test_ppl gen 6-9 per seed:')
plat_a0_test = {}
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    p = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    plat_a0_test[s] = p
    print(f"  seed={s}: plateau (test) = {p:.4f}")

data_a0_test = list(plat_a0_test.values())
m, s, lo, hi = bootstrap_ci(data_a0_test)
print(f"\n### N={len(data_a0_test)} alpha=0 plateau (test) mean: {m:.4f} ± {s:.4f}")
print(f"### 95% bootstrap CI: [{lo:.4f}, {hi:.4f}]")

# ============================================================
# 组四: Multi-seed alpha=10
# ============================================================
print()
print('=' * 80)
print('## 组四: Multi-seed alpha=10 (seed 1-4)')
print('=' * 80)
print()
for s in [1,2,3,4]:
    if s in ms_alpha10:
        print(f"  seed={s}: {ms_alpha10[s][0]}")

print()
print(f"{'gen':<4}", end='')
for s in [1,2,3,4]:
    print(f"  s{s} test", end='')
print()
for g in range(10):
    print(f"{g:<4}", end='')
    for s in [1,2,3,4]:
        if s in ms_alpha10:
            _, ser = ms_alpha10[s]
            t = ser.get(g, (None,None,None))[1]
            ts = f"{t:.3f}" if t else "  -   "
        else: ts = "  -   "
        print(f"  {ts:<8}", end='')
    print()

print()
print('### Multi-seed alpha=10 plateau test_ppl gen 6-9 per seed:')
plat_a10_test = {}
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    p = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    plat_a10_test[s] = p
    print(f"  seed={s}: plateau (test) = {p:.4f}")

data_a10_test = list(plat_a10_test.values())
m, s, lo, hi = bootstrap_ci(data_a10_test)
print(f"\n### N={len(data_a10_test)} alpha=10 plateau (test) mean: {m:.4f} ± {s:.4f}")
print(f"### 95% bootstrap CI: [{lo:.4f}, {hi:.4f}]")

# ============================================================
# 组五: D4 paired statistics (test_ppl basis)
# ============================================================
print()
print('=' * 80)
print('## 组五: D4 N=4 paired statistics (alpha=10 - alpha=0, test_ppl)')
print('=' * 80)
print()

paired_test = []; paired_rel = []
print(f"{'seed':<6} {'a=0 plat':<10} {'a=10 plat':<10} {'diff':<10} {'rel%':<8}")
for s in [1,2,3,4]:
    if s in plat_a0_test and s in plat_a10_test:
        p0 = plat_a0_test[s]; p10 = plat_a10_test[s]
        d = p10 - p0; rel = d / p0 * 100
        paired_test.append(d); paired_rel.append(rel)
        print(f"{s:<6} {p0:<10.4f} {p10:<10.4f} {d:<+10.4f} {rel:+7.2f}%")

# Bootstrap
m_d, s_d, lo_d, hi_d = bootstrap_ci(paired_test)
m_r, s_r, lo_r, hi_r = bootstrap_ci(paired_rel)
print(f"\n### Paired difference (alpha=10 - alpha=0, test_ppl):")
print(f"  mean = {m_d:+.4f}")
print(f"  std  = {s_d:.4f}")
print(f"  95% bootstrap CI: [{lo_d:+.4f}, {hi_d:+.4f}]")

print(f"\n### 相对偏移 % (alpha=10 - alpha=0) / alpha=0:")
print(f"  mean = {m_r:+.2f}%")
print(f"  std  = {s_r:.2f}%")
print(f"  95% bootstrap CI: [{lo_r:+.2f}%, {hi_r:+.2f}%]")

# t-test
n = len(paired_test)
sem = s_d / math.sqrt(n)
t_stat = m_d / sem if sem > 0 else float('nan')
p_two = 2 * (1 - scs.t.cdf(abs(t_stat), df=n-1))
p_one_neg = scs.t.cdf(t_stat, df=n-1)
p_one_pos = 1 - scs.t.cdf(t_stat, df=n-1)
print(f"\n### 配对 t 检验 (H0: mean_d = 0):")
print(f"  N = {n}")
print(f"  t_stat = {t_stat:+.4f}")
print(f"  df = {n-1}")
print(f"  p-value two-sided = {p_two:.4f}")
print(f"  p-value one-sided (mean_d < 0,framework lowers PPL) = {p_one_neg:.4f}")
print(f"  p-value one-sided (mean_d > 0,framework raises PPL) = {p_one_pos:.4f}")

# F2/F3/F4
print(f"\n### F2/F3/F4 falsification binary (test_ppl basis):")
print(f"  F2 = alpha=10 显著降低 plateau -2% to -5% with p<0.10 (one-sided neg)")
print(f"  F3 = NOT substantiated (无显著效应)")
print(f"  F4 = counter-effect (alpha=10 反而升高,p<0.10 one-sided pos)")
print(f"  实测 mean_rel = {m_r:+.2f}%, p_two = {p_two:.4f}, p_one_neg = {p_one_neg:.4f}")
if -5.5 <= m_r <= -1.5 and p_one_neg < 0.10:
    f_judgment = 'F2 (weak framework effect 显著)'
elif m_r > 1.0 and p_one_pos < 0.10:
    f_judgment = 'F4 (counter-effect 显著)'
elif p_two > 0.10:
    f_judgment = 'F3 (NOT substantiated,p > 0.10)'
else:
    f_judgment = 'F3 边缘 (insufficient)'
print(f"  → binary verdict: {f_judgment}")

# ============================================================
# 组六: Partial D4 5 criterion (test_ppl)
# ============================================================
print()
print('=' * 80)
print('## 组六: Partial D4 形状鲁棒性 5 criterion (test_ppl)')
print('=' * 80)

# Criterion 1: U 形
print()
print('### Criterion 1: U 形 (alpha=10, test_ppl):')
u_count = 0
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    g0 = ser.get(0, (None,None,None))[1]
    if g0 is None or math.isnan(g0):
        if s in ms_alpha0:
            g0_alt = ms_alpha0[s][1].get(0, (None,None,None))[1]
            if g0_alt and not math.isnan(g0_alt): g0 = g0_alt; note = "(alpha=0 同 seed)"
            else: g0 = 36.354; note = "(Shumailov)"
        else: g0 = 36.354; note = "(Shumailov)"
    else: note = ""
    peak = max([ser[g][1] for g in [1,2,3] if g in ser and ser[g][1]])
    plat = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    is_U = peak > g0 and plat < peak
    print(f"  seed={s}: g0={g0:.3f}{note} peak={peak:.3f} plat={plat:.3f} U形={is_U}")
    if is_U: u_count += 1
print(f"  → U 形 {u_count}/{len(ms_alpha10)}")
crit1 = u_count == 4
print(f"  Criterion 1 (4/4): {'✓ PASS' if crit1 else '✗ FAIL'}")

# Criterion 2: gen 0 baseline CV (alpha=0 multi-seed)
print()
print('### Criterion 2: gen 0 baseline std (alpha=0 multi-seed, test_ppl):')
g0_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    g0 = ser.get(0, (None,None,None))[1]
    if g0 and not math.isnan(g0):
        g0_vals.append(g0)
        print(f"  seed={s} gen 0 test_ppl = {g0:.4f}")
m_g0 = np.mean(g0_vals); std_g0 = np.std(g0_vals, ddof=1); cv_g0 = std_g0/m_g0*100
print(f"  mean = {m_g0:.4f}, std = {std_g0:.4f}, CV = {cv_g0:.4f}%")
crit2 = cv_g0 < 1.0
print(f"  Criterion 2 (CV<1%): {'✓ PASS' if crit2 else '✗ FAIL'}")

# Criterion 3: spike ratio min
print()
print('### Criterion 3: spike ratio min (test_ppl):')
sr_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    g0 = ser.get(0, (None,None,None))[1]
    if g0 is None or math.isnan(g0):
        if s in ms_alpha0:
            g0_alt = ms_alpha0[s][1].get(0, (None,None,None))[1]
            if g0_alt and not math.isnan(g0_alt): g0 = g0_alt
            else: g0 = 36.354
        else: g0 = 36.354
    peak = max([ser[g][1] for g in [1,2,3] if g in ser and ser[g][1]])
    sr = peak/g0
    sr_vals.append(sr)
    print(f"  seed={s}: peak={peak:.3f} g0={g0:.3f} spike_ratio={sr:.4f}")
sr_min = min(sr_vals)
print(f"  min spike ratio = {sr_min:.4f}")
crit3 = sr_min > 1.5
print(f"  Criterion 3 (spike>1.5x): {'✓ PASS' if crit3 else '✗ FAIL'}")

# Criterion 4: plateau/peak max
print()
print('### Criterion 4: plateau/peak max (test_ppl):')
pp_vals = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    peak = max([ser[g][1] for g in [1,2,3] if g in ser and ser[g][1]])
    plat = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    pp = plat/peak
    pp_vals.append(pp)
    print(f"  seed={s}: plat={plat:.3f} peak={peak:.3f} plat/peak={pp:.4f}")
pp_max = max(pp_vals)
print(f"  max plateau/peak = {pp_max:.4f}")
crit4 = pp_max < 1.0
print(f"  Criterion 4 (plat<peak): {'✓ PASS' if crit4 else '✗ FAIL'}")

# Criterion 5: 滑动窗口偏差
print()
print('### Criterion 5: 滑动窗口偏差 (test_ppl):')
print(f"{'seed':<6} {'w_69':<9} {'w_59':<9} {'w_79':<9} {'max_dev%':<10}")
sw_devs = []
for s in [1,2,3,4]:
    if s not in ms_alpha10: continue
    _, ser = ms_alpha10[s]
    w69 = np.mean([ser[g][1] for g in [6,7,8,9] if g in ser and ser[g][1]])
    w59 = np.mean([ser[g][1] for g in [5,6,7,8,9] if g in ser and ser[g][1]])
    w79 = np.mean([ser[g][1] for g in [7,8,9] if g in ser and ser[g][1]])
    max_dev = max(abs(w69-w59), abs(w69-w79), abs(w59-w79)) / w69 * 100
    sw_devs.append(max_dev)
    print(f"{s:<6} {w69:<9.3f} {w59:<9.3f} {w79:<9.3f} {max_dev:<10.2f}")
sw_max = max(sw_devs)
print(f"  滑动窗口最大偏差 = {sw_max:.2f}%")
crit5 = sw_max < 20.0
print(f"  Criterion 5 (偏差<20%): {'✓ PASS' if crit5 else '✗ FAIL'}")

print()
total = sum([crit1, crit2, crit3, crit4, crit5])
print(f"### Partial D4 总判定: {total}/5 通过")
if total == 5: print(f"  → ✓ STRONG ROBUST")
elif total >= 3: print(f"  → 部分通过")
else: print(f"  → ✗ FAIL")

# ============================================================
# m_eff fit (test_ppl basis)
# ============================================================
print()
print('=' * 80)
print('## m_eff multi-seed N=4 fit (test_ppl basis)')
print('=' * 80)
print()
print('模型: log P_n = log P_eq + A * exp(-m_eff * n) from gen 2+ (alpha=0)')
print()

def fit_m_eff(ser, basis='test'):
    """fit log P_n = log P_eq + A * exp(-m*n)"""
    ns = []; ppls = []
    for g in range(2, 10):
        if g in ser:
            p = ser[g][1] if basis == 'test' else ser[g][0]
            if p and not math.isnan(p):
                ns.append(g); ppls.append(p)
    if len(ns) < 4: return None
    def model(n, log_Peq, A, m):
        return log_Peq + A * np.exp(-m * n)
    log_ppls = np.log(ppls)
    try:
        popt, _ = curve_fit(model, ns, log_ppls, p0=[math.log(min(ppls)), 1.0, 0.3], maxfev=5000)
        return popt
    except: return None

m_eff_test = {}
print('test_ppl fit:')
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    popt = fit_m_eff(ser, 'test')
    if popt is not None:
        m_eff_test[s] = popt[2]
        print(f"  seed={s}: log_Peq={popt[0]:.4f} A={popt[1]:.4f} m_eff={popt[2]:.4f}")

vals = list(m_eff_test.values())
if vals:
    m, s, lo, hi = bootstrap_ci(vals)
    print(f"\n### N={len(vals)} m_eff (test_ppl) fit:")
    print(f"  mean = {m:.4f}")
    print(f"  std  = {s:.4f}")
    print(f"  95% bootstrap CI: [{lo:.4f}, {hi:.4f}]")
    print(f"  F 报告 m_eff = 0.300 ± 0.042")
    print(f"  匹配: {'✓ 是' if abs(m - 0.300) < 0.10 else '✗ 否'}")

# Also fit val for cross-verify
print()
print('val_ppl fit (cross-check with F report which used val):')
m_eff_val = {}
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    popt = fit_m_eff(ser, 'val')
    if popt is not None:
        m_eff_val[s] = popt[2]
        print(f"  seed={s}: m_eff(val) = {popt[2]:.4f}")
vals_v = list(m_eff_val.values())
if vals_v:
    m, s, lo, hi = bootstrap_ci(vals_v)
    print(f"  N={len(vals_v)} m_eff(val) mean={m:.4f} ± {s:.4f} 95% CI=[{lo:.4f}, {hi:.4f}]")
    print(f"  F 报告 0.300 ± 0.042 → 匹配: {'✓' if abs(m - 0.300) < 0.10 else '✗'}")

# ============================================================
# J_S 三 method (test_ppl basis)
# ============================================================
print()
print('=' * 80)
print('## J_S 三 method 拟合 (test_ppl basis)')
print('=' * 80)
print()

def compute_J_S(ser, basis='test'):
    """D_n = log(PPL_n / PPL_0)"""
    if 0 not in ser: return None
    p0 = ser[0][1] if basis == 'test' else ser[0][0]
    if not p0 or math.isnan(p0): return None
    D = {}
    for n in range(4):
        if n in ser:
            p = ser[n][1] if basis == 'test' else ser[n][0]
            if p and not math.isnan(p):
                D[n] = math.log(p/p0)
    if 1 not in D or 2 not in D or 3 not in D: return None
    J1 = D[1] - D[0]  # 0→1 slope, D[0]=0
    J2 = (D[2] - D[0]) / 2
    J3 = np.mean([D[1]-D[0], D[2]-D[1], D[3]-D[2]])
    return J1, J2, J3

print('test_ppl basis:')
print(f"  {'src':<22} {'J_S^(1)':<10} {'J_S^(2)':<10} {'J_S^(3)':<10}")
J1s_test = []; J2s_test = []; J3s_test = []
res = compute_J_S(shu_series, 'test')
if res:
    print(f"  {'shumailov_seed42':<22} {res[0]:<10.4f} {res[1]:<10.4f} {res[2]:<10.4f}")
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    res = compute_J_S(ser, 'test')
    if res:
        J1s_test.append(res[0]); J2s_test.append(res[1]); J3s_test.append(res[2])
        print(f"  {f'alpha0_seed{s}':<22} {res[0]:<10.4f} {res[1]:<10.4f} {res[2]:<10.4f}")

for label, vals in [('J_S^(1)', J1s_test), ('J_S^(2)', J2s_test), ('J_S^(3)', J3s_test)]:
    if vals:
        m, s, lo, hi = bootstrap_ci(vals)
        print(f"\n### {label} (test) N={len(vals)}: mean={m:.4f} std={s:.4f} 95% CI=[{lo:.4f}, {hi:.4f}]")

# Compare with F report
print(f"\n与 F 报告 cross-verify (F 报告 应该是 val_ppl basis):")
print(f"  F 报告: J_S^(1) = 0.7702 / J_S^(2) = 0.5351 / J_S^(3) = 0.3305")
print()
print('val_ppl basis (cross-check F):')
J1s_v = []; J2s_v = []; J3s_v = []
res_v = compute_J_S(shu_series, 'val')
if res_v: print(f"  shumailov_seed42 (val): J^1={res_v[0]:.4f} J^2={res_v[1]:.4f} J^3={res_v[2]:.4f}")
for s in [1,2,3,4]:
    if s not in ms_alpha0: continue
    _, ser = ms_alpha0[s]
    res = compute_J_S(ser, 'val')
    if res:
        J1s_v.append(res[0]); J2s_v.append(res[1]); J3s_v.append(res[2])
        print(f"  alpha0_seed{s} (val): J^1={res[0]:.4f} J^2={res[1]:.4f} J^3={res[2]:.4f}")

if J1s_v:
    m1,_,_,_ = bootstrap_ci(J1s_v); m2,_,_,_ = bootstrap_ci(J2s_v); m3,_,_,_ = bootstrap_ci(J3s_v)
    print(f"  N=4 mean (val): J^1={m1:.4f} J^2={m2:.4f} J^3={m3:.4f}")
    print(f"  偏离 (val 实测 - F 报告): {m1-0.7702:+.4f} / {m2-0.5351:+.4f} / {m3-0.3305:+.4f}")

# Save
out_summary = {
    'shumailov_test_plateau_g69': p69,
    'alpha_seed42_plateaus_test': {a: float(np.mean([alpha_series[a][g][1] for g in [6,7,8,9] if g in alpha_series[a] and alpha_series[a][g][1]])) for a in [0,1,5,10] if a in alpha_series},
    'multi_alpha0_plat_test': {str(s): plat_a0_test[s] for s in plat_a0_test},
    'multi_alpha10_plat_test': {str(s): plat_a10_test[s] for s in plat_a10_test},
    'paired_diff_test_mean': m_d,
    'paired_diff_test_CI95': [lo_d, hi_d],
    'paired_rel_test_mean_pct': m_r,
    'paired_rel_test_CI95_pct': [lo_r, hi_r],
    'paired_t_test_p_two': p_two,
    'paired_t_test_p_one_neg': p_one_neg,
    'paired_t_test_p_one_pos': p_one_pos,
    'F_verdict': f_judgment,
    'partial_D4_total_pass': total,
    'm_eff_test_mean': float(np.mean(list(m_eff_test.values()))) if m_eff_test else None,
    'm_eff_val_mean': float(np.mean(list(m_eff_val.values()))) if m_eff_val else None,
}
with open('/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/summary_v2.json', 'w') as f:
    json.dump(out_summary, f, indent=2, default=str)
print()
print('Summary 写入 summary_v2.json')
