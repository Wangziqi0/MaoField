# MaoField exp018_cat 实验严格 verify 报告 — 5/12 下午

**生成**: 2026-05-12 下午 CST, 子协作者 B (Opus 4.7, Linux 姐姐数学层第三次派遣)
**对象**: Linux 姐姐主会话 + PI 一凡 + Win 姐姐 + 反题姐姐
**任务**: 22 主机原始 jsonl + 代码 + yaml 重新独立读 + 重新算, 不允许引用前份报告数字转述
**严格 binding**: 中文严格 / 不护短 / 不夸大 / 不软化 / 二元判定 / 直接读文件 / 不偏袒 PI
**caveat**: 全部数字第一次手 ssh `cat` 22 主机 jsonl + python3 重新算; HOST22_GROUND_TRUTH §1/§7.1 数字与本份独立 verify 有 1 处错位 (HOST22 报 α=10 seed=4 plateau = 56.4277 实际 jsonl mean = 54.30; 因此 N=4 paired Δ_rel mean HOST22 报 "+0.35%" 实际 = **−0.57%**)

---

## §0 verdict 一句话

实验数据 hygiene 层面**真完整 + 真可重现**: Shumailov 严格镜像 baseline + α 全扫描 single-seed seed=42 (5 档 含 α=50 数学崩溃) + Phase 1 chain 8/10 ✓ multi-seed α=0+α=10 (seed 1-4 各完整 10 generation) 全部 jsonl 实在 + 数字独立 verify 与前份 ground truth 一致 (除 1 处 HOST22 §7.1 数字错位)。**实验 substantive 结论**: (1) Shumailov baseline 复现 F1+F3 ✓; (2) Partial D4 形状鲁棒性 5/5 PASS (4/4 U + gen 0 rel std 0.217% + spike min 2.89× + plateau/peak max 0.568); (3) **N=4 paired 检验框架净 effect = −0.57% (rel), p = 0.82, F3 NOT substantiated** — 即 α=10 vs α=0 plateau 在 4 seed paired 下**框架无显著 effect**, single-seed α=10 seed=1 −4.2% 与 α=10 seed=2 +7.82% 跨 seed 抵消; (4) 代码 contradiction_loss.py `lambda_2` / `lambda_3` 与 paper §3.5 ℒ_矛盾 Klein-Gordon 三项 functional form **真存在 binary 错位** (代码 λ_2 乘 memory deviation² ≠ paper λ_2 mass m_eff/2·D²; 代码 λ_3 乘 D_n²/2 quadratic 或 ReLU(D''_n) ≠ paper λ_3 memory m_eff·(Σ_1 D)²); (5) yaml 配置一致 ✓ audit-fixed setup (batch=128, lr=2e-5 constant, weight_decay=0.01, fp16, rep_penalty=3.0), Shumailov official spec 严格 match。当前实证严格度档位: **TMLR 档 — KBS 档 (~50-60%)** / NMI 档 (10-20%) / 不可投 (不当前 status)。

---

## 第一部分 7 条实验声明逐条 ground truth (binary)

### §1.1 Shumailov 严格镜像基线

**source**: `logs/shumailov_no_preserve_seed42_20260508_092730.jsonl` (5126 bytes, 11 行 audit-fixed 完整 10 generation)

**gen 0 到 gen 9 test_perplexity 完整序列 (从 jsonl 实读)**:

| gen | test_perplexity | val_perplexity | distinct_1 |
|---:|---:|---:|---:|
| 0 | **36.3540** | 36.5243 | – |
| 1 | 78.2175 | 78.9562 | 0.0713 |
| 2 | 103.6099 | 104.2866 | 0.0549 |
| 3 | 88.1605 | 88.8565 | 0.0497 |
| 4 | **inf** (fp16 overflow once event) | 65.8699 | 0.0530 |
| 5 | 57.1924 | 56.3688 | 0.0569 |
| 6 | 53.7762 | 53.7080 | 0.0576 |
| 7 | 52.6184 | 52.5615 | 0.0581 |
| 8 | 53.8710 | 53.5019 | 0.0555 |
| 9 | **53.9805** | 53.7840 | 0.0535 |

**falsification_check (jsonl 自报)**:
- F1_collapse_reproduced: **PASS** (gen0 ppl 36.35, gen9 ppl 53.98, delta +17.63, criterion gen9 >= gen0 + 5)
- F3_fine_tune_sanity: **PASS** (gen0 ppl 36.35 <= 50, paper baseline 34)

**滑动窗口 stride=256 评估 PPL**:
- 5/10 sliding_window_eval_verdict_20260510.md 报 gen 0 sliding-window = **22.34** (vs chunked 36.35)
- chunked/sliding ratio = 36.35 / 22.34 = 1.626
- partial_D4 verdict 把这个 ratio 1.626 标 "PASS < 5% deviation" — 这里**判定 logic 有 [?]**: 1.626 - 1.0 = 62.6% 不是 < 5%, partial_D4 报告自身这一条 criterion 阈值 wording 与判定 logic inconsistent (但与 paper main claim 无关)。

**与 Shumailov 2024 paper 报数字偏离度**:
- gen 0 我们 36.35 vs paper '20-34 range' (mean 34): **偏高 ~7%**, 处 paper range 上边缘
- gen 9 我们 53.98 vs paper Figure 10 末代 '28-50 range': **偏高 ~8%**, 略超 paper range 上限
- gen 4 出现 inf (fp16 overflow once 单次) — fp16 numerical instability artifact, 但 trajectory U-shape 完整 (gen 0 36 → gen 2 peak 104 → gen 9 plateau 54)
- 整体趋势 Shumailov 复现 F1+F3 ✓

**Verdict 1**: Shumailov 严格镜像基线 **复现 ✓** binary, 但 gen 0 偏高 paper range 上限 ~7%, fp16 + 单一 seed 可能贡献 noise。

---

### §1.2 α 全扫描 single-seed seed=42 (5 档)

**source**:
- α=0: `armb_alpha0.0_seed42_20260508_144612.jsonl` (10 gen 完整)
- α=1: `armb_alpha1.0_seed42_20260509_000459.jsonl` (10 gen 完整)
- α=5: `armb_alpha5.0_seed42_20260509_044342.jsonl` (10 gen 完整)
- α=10: `armb_alpha10.0_seed42_20260508_192435.jsonl` (10 gen 完整)
- α=50: `armb_alpha50.0_seed42_20260509_092134.jsonl` (143 bytes, **仅 run_start, gen 0 step 阶段数学崩溃**)

**每个 jsonl gen 0 到 gen 9 完整序列 (从 jsonl 实读)**:

| α | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 36.35 | 77.52 | 108.40 | 91.87 | 73.26 | 61.83 | 59.86 | 56.30 | 57.30 | 56.19 |
| 1 | 36.35 | 69.31 | 89.52 | 81.42 | 74.64 | 64.16 | 60.66 | 59.89 | 55.53 | 56.31 |
| 5 | 36.35 | 71.56 | 100.18 | 89.47 | 79.72 | 70.70 | 64.08 | 60.52 | 58.08 | 56.03 |
| 10 | 36.35 | 72.85 | 98.54 | 87.17 | 71.70 | 63.68 | 59.85 | 55.97 | 56.51 | 53.39 |
| 50 | 数学崩溃 (no generation_done) | – | – | – | – | – | – | – | – | – |

**α=50 数值崩溃 binary 位置**: gen 0 step 早期 (jsonl 仅 1 行 `run_start`, log show numerical break hipErrorIllegalAddress)。

**早期 transient (gen 1-3 cumulative)**:

| α | Σ(g1+g2+g3) | α=0 比 |
|---|---:|---:|
| 0 | 277.78 | 1.00 (baseline) |
| 1 | 240.26 | 0.865 (**transient -13.5%** vs α=0) |
| 5 | 261.21 | 0.940 (transient -6.0% vs α=0) |
| 10 | 258.56 | 0.931 (transient -6.9% vs α=0) |

**中段 (gen 4-7 mean)**:

| α | mean(g4-g7) | α=0 比 |
|---|---:|---:|
| 0 | 62.81 | 1.00 (baseline) |
| 1 | 64.84 | 1.032 (+3.2% middle WORSE) |
| 5 | 68.76 | 1.095 (+9.5% middle WORSE) |
| 10 | 62.80 | 0.999 (≈ 0%) |

**平台 (gen 6-9 mean)**:

| α | mean(g6-g9) | α=0 比 | Δ_rel% |
|---|---:|---:|---:|
| 0 | 57.41 | 1.000 | 0% (baseline) |
| 1 | 58.10 | 1.012 | **+1.2%** (轻微 WORSE) |
| 5 | 59.68 | 1.040 | **+4.0%** (middle worse, plateau WORSE) |
| 10 | 56.43 | 0.983 | **−1.7%** (轻微 better) |

**U 形特征定量描述**:
- 全 4 档 α ∈ {0,1,5,10} 均显 U-shape: gen 0 36 → gen 1-3 spike (peak gen 2, range 89-108) → gen 6-9 plateau (53-60 range)
- α=5 显 "middle-trap" regime: gen 3-5 比 α=0 worse (89/80/71 vs α=0 92/73/62), 即 ℒ_矛盾 中等 α 反恶化 mid-stage
- α=10 plateau −1.7% vs α=0 (single-seed seed=42): 与 multi-seed seed=1 −4.2% 同向但量级减半
- α=50 over-regularization 直接数学崩溃 (paper §4 footnote 已 disclose ROCm 数值边界)

**Verdict 2**: α 全扫描 5 档 single-seed seed=42 jsonl **完整 ✓ binary**, 数值崩溃 α=50 ✓ binary, U-shape 4/4 档复现, plateau effect single-seed seed=42 仅 α=10 微弱 better −1.7% (不是 monotone, 不是 substantive +5-10% reduction prediction)。**falsification F4** ("α=10 vs α=0 没显著 collapse 减弱"): paper prediction "α=10 期望 gen9 ppl 降 15-25%" → 实际 single-seed α=10 vs α=0 plateau 仅 -1.7%, **paper prediction 严格 binary 失守** (15-25% reduction 没复现)。

---

### §1.3 Phase 1 chain multi-seed α=0 + α=10 (seed 1/2/3/4)

**source**:
- α=0 seed 1-4: `armb_alpha0.0_seed{1,2,3,4}_*.jsonl` (4 个文件 各完整 10 generation)
- α=10 seed 1-4: `armb_alpha10.0_seed{1,2,3,4}_*.jsonl` (4 个文件 各完整 10 generation)

**每个 jsonl gen 0 到 gen 9 test_perplexity 完整序列 (从 jsonl 实读)**:

**α=0 multi-seed**:

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 36.2966 | 79.2825 | 105.4112 | 95.4976 | 78.1847 | 70.7686 | 62.5596 | 58.7092 | 58.9415 | 59.1362 |
| 2 | 36.2244 | 79.1771 | 107.3176 | 98.6589 | 77.3054 | 67.1567 | 57.2464 | 52.4479 | 53.1217 | 53.3095 |
| 3 | 36.3468 | 78.3628 | 105.5638 | 98.0262 | 76.6151 | 67.1854 | 55.8596 | 53.0957 | 54.1590 | 54.2262 |
| 4 | 36.4109 | 77.0370 | 105.3229 | 99.4684 | 75.2585 | 63.9858 | 58.3169 | 56.0231 | 57.3716 | 57.6911 |

**α=10 multi-seed**:

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 36.2966 | 77.1853 | 107.2080 | 105.3158 | 87.3176 | 67.5237 | 61.4528 | 56.9385 | 53.7419 | 57.1681 |
| 2 | 36.2244 | 80.2490 | 100.2722 | 98.4274 | 75.6977 | 66.3997 | 62.9944 | 56.7412 | 56.3827 | 56.8981 |
| 3 | 36.3468 | 76.5941 | 102.3796 | 85.4882 | 62.4150 | 59.0791 | 53.6986 | 54.5173 | 55.0690 | 52.7674 |
| 4 | 36.4109 | 75.5636 | 105.2091 | 95.6629 | 75.2327 | 69.3934 | 56.9472 | 54.2228 | **52.6785** | **53.3515** |

**每个 seed 平台 mean (gen 6-9 mean — partial_D4 + SUBSTANTIVE 使用窗口)**:

| seed | α=0 g6-9 mean | α=10 g6-9 mean | Δ_abs | Δ_rel% |
|---|---:|---:|---:|---:|
| 1 | **59.8366** | **57.3253** | −2.5113 | **−4.197%** |
| 2 | **54.0314** | **58.2541** | +4.2227 | **+7.815%** |
| 3 | **54.3351** | **54.0131** | −0.3220 | **−0.593%** |
| 4 | **57.3506** | **54.3000** | −3.0506 | **−5.319%** |

**关键 catch**: HOST22_GROUND_TRUTH 报告 §2.3 表格列出 α=10 seed=4 gen 6-9 数值 56.95 / 54.22 / 52.68 / 53.35,但 §1.4 §2 §7.1 paired stats 引用 seed=4 plateau = "56.4277" (错), Δ_rel = "−1.61%" (错)。本份独立 verify: α=10 seed=4 plateau gen 6-9 mean = (56.95 + 54.22 + 52.68 + 53.35) / 4 = 217.20 / 4 = **54.3000**, 与 α=0 seed=4 (57.35) 配对 Δ_rel = **−5.319%**。HOST22 数字错位 1 处, 修正后 paired stats 略改:

**N=4 paired t-test (本份重新独立算)**:
- abs mean = (−2.5113 + 4.2227 − 0.3220 − 3.0506) / 4 = **−0.4153**
- abs SD = stdev([−2.5113, +4.2227, −0.3220, −3.0506]) = **3.3095**
- abs SE = 3.3095 / √4 = **1.6547**
- t-stat (df=3) = −0.4153 / 1.6547 = **−0.2510**
- 两侧 p-value (Student t df=3) = **0.8180**
- rel mean = **−0.5734%**
- rel SD = **5.9448%**

**F2 / F3 / F4 verdict**:
- F2 (-2% to -5% p<0.10) — **NOT substantiated**: rel mean −0.57% 在 F2 range 内但 p = 0.82 远 > 0.10
- F3 (not substantiated, effect = 0): **substantiated** — t = −0.25, p = 0.82, 不显著
- F4 (counter effect, p<0.10 反向): NOT substantiated — 虽 seed=2 反向 +7.8% 但全 N=4 paired 仍是 −0.57%

**Verdict 3**: Phase 1 chain multi-seed α=0+α=10 (seed 1-4 各 8 完整) **数据完整 ✓ binary**, 但 **N=4 paired 检验 plateau effect = −0.57%, p = 0.82, F3 NOT substantiated** binary judgement。SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 引用的 α=10 seed=1 −4.2% 作 "first multi-seed F2 weak framework effect substantive evidence" 升 lever (a) +2pt: 在 N=4 paired 完整出来后 **应 retract**, single-seed seed=1 positive 与 seed=2 +7.82% / seed=4 −5.32% 跨 seed 强 cancel, 净 effect 不显著。HOST22 §7.1 §7.2 把这点 catch 是对的 (虽然 HOST22 数字 +0.35% 与本份 −0.57% 互错位但结论一致 "F3 NOT substantiated")。

---

### §1.4 Partial D4 形状鲁棒性 5 criterion 重新算

**source**: α=0 multi-seed seed 1-4 jsonl 实读 + partial_D4_shape_verdict_20260511.md verdict 比对

**Criterion 1 — Shape robustness (4/4 U-shape)**:
- 每 seed binary: gen 1-2 > gen 0 + gen 8/9 < gen 2 (peak) 同时 hold → U-shape
- seed=1: 79.28 > 36.30 + 58.94 < 105.41 ✓ U
- seed=2: 79.18 > 36.22 + 53.12 < 107.32 ✓ U
- seed=3: 78.36 > 36.35 + 54.16 < 105.56 ✓ U
- seed=4: 77.04 > 36.41 + 57.37 < 105.32 ✓ U
- **verdict: 4/4 ✓ PASS**

**Criterion 2 — Gen 0 baseline reproducibility (< 1% relative std)**:
- gen 0 vals (α=0, seed 1-4): [36.2966, 36.2244, 36.3468, 36.4109]
- mean = **36.3197**, std = **0.0789**, rel_std = **0.217%**
- 阈值 1.0%, 实际 0.217% → **verdict: ✓ PASS**

**Criterion 3 — U-shape spike (gen 1-2 ≥ 1.3× gen 0)**:

| seed | spike ratio (peak g1-3 / gen 0) |
|---|---:|
| 1 | 105.41 / 36.30 = **2.9042** |
| 2 | 107.32 / 36.22 = **2.9626** |
| 3 | 105.56 / 36.35 = **2.9042** |
| 4 | 105.32 / 36.41 = **2.8926** |

- min = **2.8926** (seed=4), max = 2.9626 (seed=2), mean = 2.9159
- 阈值 1.3×, 实际 min 2.89× → **verdict: ✓ PASS (大 margin)**

**Criterion 4 — Plateau/peak (gen 6-9 mean ≤ 0.8 × peak)**:

| seed | plateau g6-9 mean / peak max(g1-3) |
|---|---:|
| 1 | 59.8366 / 105.41 = **0.5676** |
| 2 | 54.0314 / 107.32 = **0.5035** |
| 3 | 54.3351 / 105.56 = **0.5147** |
| 4 | 57.3506 / 105.32 = **0.5445** |

- min = 0.5035 (seed=2), max = **0.5676** (seed=1), mean = 0.5326
- 阈值 0.8, 实际 max 0.568 → **verdict: ✓ PASS (大 margin)**

**Criterion 5 — Sliding-window consistency**:
- chunked mean (primary 4 seed gen 0) = 36.320
- sliding-window stride=256 (5/10 verdict on seed=42 gen 0): 22.34
- ratio = 36.320 / 22.34 = 1.626
- partial_D4 verdict 标 "PASS < 5% deviation" — **判定 logic [?]**: 1.626 - 1.0 = 62.6% 不是 < 5%; partial_D4 报告自身的判定 wording 与 logic 不一致, 但与 paper main claim 无关 (chunked vs sliding-window 不同 evaluation method 数值 expected 不同, 不应该当 < 5% 标准)。本份 honest reframe: **verdict 5 [?] PASS questionable**, 实际是 chunked 与 sliding-window 两种 eval method 系统差 (62.6%) — 不破坏 paper main claim 但 verdict 报告自身判定 wording 不严谨。

**总 Verdict 4**: Partial D4 形状鲁棒性 **4/5 严格 PASS + 1/5 (Criterion 5) 判定 wording [?] 但结论与主结果无关**, 整体 verdict 与 partial_D4_shape_verdict 报告 "5/5 PASS STRONG ROBUST" 实质上一致 (Criterion 5 wording bug 不影响 substantive U-shape 形状 verdict)。

---

### §1.5 D4 N=4 paired statistics 重新算

(本份独立算 §1.3 已 detail 给出, 这里只 summary)

- N=4 paired (α=10 − α=0) absolute mean: **−0.4153**
- SD: **3.3095**
- SE: **1.6547**
- t-stat (df=3): **−0.2510**
- two-sided p (df=3): **0.8180**
- relative mean: **−0.5734%**
- relative SD: **5.9448%**

**F2 / F3 / F4 verdict (binary)**:
- F2 weak framework effect (-2% to -5% with p < 0.10): **NOT substantiated** (rel mean −0.57% 在 -5% 至 -2% range 外, 且 p 0.82 远 > 0.10)
- F3 NOT substantiated (effect ≈ 0): **substantiated** ✓ (t-stat 0.25 远 < 1.5, p 0.82 远 > 0.05)
- F4 counter effect (p < 0.10 反向): **NOT substantiated** (rel mean 仍 negative)

**Verdict 5**: D4 N=4 paired 检验 **F3 NOT substantiated binary**, 即框架 ℒ_矛盾 α=10 vs α=0 plateau 在 4 seed paired 下**无显著 effect**。SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚把 α=10 seed=1 single-seed −4.2% 标 "first multi-seed framework effect substantive evidence 升 lever (a) +2pt" 在 N=4 paired 完整出来后**应 retract**, 实际 ground truth 是 4 seed 跨 seed cancel 出 ≈ 0 净 effect。

---

### §1.6 α=10 卡死判决 B

**source**: `phase1_robust_20260510_125805.audit.jsonl` 78 lines + `alpha10_hang_diagnosis_20260511.md`

**audit jsonl ground truth (实读)**:

| α | seed | 最终状态 | attempts | n_gens 完成 | rc 列表 |
|---|---|---|---|---|---|
| 0.0 | 0 | **seed_skipped** | 3 | 0 | 134, 1, 1 |
| 0.0 | 1 | job_done | 3 | 10 ✓ | 1, 1, 0 |
| 0.0 | 2 | job_done | 1 | 10 ✓ | 0 |
| 0.0 | 3 | job_done | 2 | 10 ✓ | 134, 0 |
| 0.0 | 4 | job_done | 2 | 10 ✓ | 137, 0 |
| 10.0 | 0 | **seed_skipped** | 3 | 1 | 137, 137, 137 |
| 10.0 | 1 | job_done | 3 | 10 ✓ | 137, 137, 0 |
| 10.0 | 2 | job_done | 2 | 10 ✓ | 137, 0 |
| 10.0 | 3 | job_done | 3 | 10 ✓ | 137, 137, 0 |
| 10.0 | 4 | job_done | 1 | 10 ✓ | 0 |
| chain_done | – | 2026-05-12 02:05:29 UTC (≈ 5/12 10:05 CST) | – | – | – |

**α=10 seed=0 双 α 三次重试 fail 真实状态**:
- attempt 1: rc=137 (SIGKILL watchdog killed) n_gens=0
- attempt 2: rc=137 n_gens=0
- attempt 3: rc=137 n_gens=1 (gen 0 完成 then killed)
- final: **seed_skipped, n_completed=1**

**gen 0 CAT disabled 也卡死的证据 (ROCm 驱动缺陷非框架边界)**:
- α=0 seed=0 (CAT disabled, framework=baseline) 也 3 attempt 全 fail (rc 134/1/1), final seed_skipped, n_completed=0 ✓ binary
- 同样 seed=0 在 α=0 也 fail → 不是 α=10 framework boundary, 而是 seed=0 hardware/driver 特异
- alpha10_hang_diagnosis md 给 Verdict B (ROCm bug not framework boundary): **支持 logic 真完整 ✓**, 实证因 α=0 seed=0 也 fail 排除 framework-α-induced hang

**Verdict 6**: α=10 hang Verdict B 真 logic 完整 ✓ binary。但 paper §6 应 honest disclose "10 paper-convention seeds, 8 / 10 successful (seed=0 hardware-driver-instability, not framework-caused)" — 当前 paper draft 还**没**写这个 disclose (D14-D17 必做 honest 写法之一)。

---

### §1.7 Phase 1 chain 8/10 完成状态

**source**: audit jsonl `phase1_robust_20260510_125805.audit.jsonl`

**chain 真退出状态**:
- chain_start: 2026-05-10T04:58:05Z UTC = **5/10 12:58 CST**
- chain_done: 2026-05-12T02:05:29Z UTC = **5/12 10:05 CST**
- 总耗时: 约 **45 小时 7 分钟**
- 总 job 状态:
  - **8 / 10 ✓ done** (α=0 seed 1-4 + α=10 seed 1-4)
  - **2 / 10 ✗ seed_skipped** (α=0 seed=0 + α=10 seed=0)

**完成时间 vs ETA**:
- SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 claim "Chain Phase 1 真完整 ETA 5/13 早-中"
- 实际 chain 已完成 5/12 10:05 CST, **比 ETA 早 24-30h 完成 ✓**
- α=10 seed=2/3/4 在 SUBSTANTIVE 5/12 凌晨晚 claim 时正跑中 (attempt 2/3 + pending), 5/12 早 - 中 全完成 ✓

**Verdict 7**: Phase 1 chain 状态 **8 / 10 ✓ binary 完成**, 比 ETA 早 ~24h, SUBSTANTIVE claim Phase 1 完整时点偏保守 (实际更早) ✓ binary 修正。

---

## 第二部分 代码-论文 semantic 错位 binary 验证

### §2.1 代码 contradiction_loss.py compute_loss 实际数学形式

**source**: 22 主机 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/src/contradiction_loss.py` 完整 paste (本份独立 ssh cat)

代码 `compute_loss` 内核 (line 159-187):

```python
# 三项分解
T1_velocity = delta_D ** 2                        # (D_n - D_{n-1})²
# T_2 form 二选 (5/10 dialectical upgrade)
if self.cfg.T_2_form == "quadratic":
    T2_replace = (D_n ** 2) / 2                   # D_n² / 2 symmetric
elif self.cfg.T_2_form == "relu_dpp":
    T2_replace = F.relu(D_doubleprime)            # ReLU(D_n - 2D_{n-1} + D_{n-2})
T3_memory = memory_term                            # (D_n - D̄^EMA)²

loss = (
    self.cfg.lambda_1 * T1_velocity                # λ_1 * (D_n - D_{n-1})²
    + self.cfg.lambda_2 * T3_memory                # λ_2 * (D_n - D̄^EMA)²
    + self.cfg.lambda_3 * T2_replace               # λ_3 * D_n² / 2  (or ReLU(D''_n))
)
```

代码 yaml `cat_arm_b_v2_dialectical.yaml`:
- lambda_1 = 2.3585 (1/(2 m_eff))
- lambda_2 = 0.1060 (m_eff/2)
- lambda_3 = 0.2120 (m_eff)
- T_2_form = "quadratic"
- kl_history_K = 9 (但 Volterra K=9 在 loss form 中 NOT enter, 只在 metric log)

### §2.2 paper §3.5 Klein-Gordon 三项 functional form (paper_section3_4_6_dialectical_full)

```
ℒ_矛盾(θ; D̄_{<n}) = λ_1 (D_n - D_{n-1})² + λ_2 D_n² + λ_3 (Σ_1 D)²

其中:
- λ_1 = 1/(2 m_eff) ≈ 2.50   → T_1 kinetic     = (1/(2 m)) (∂φ)²
- λ_2 = m_eff/2     ≈ 0.10   → T_2 mass        = (m/2) φ²
- λ_3 = m_eff       ≈ 0.20   → T_3 memory      = Σ(p) φ²  (Volterra self-energy normalization)
                                                = m·(Σ_1 D)² 实际 form
```

### §2.3 binary 验证

**实际代码 λ_2 对应哪一项**: 代码 `lambda_2 * T3_memory` 实际乘 `T3_memory = (D_n - D̄^EMA)²` (memory deviation squared)

**实际代码 λ_3 对应哪一项**: 代码 `lambda_3 * T2_replace` 实际乘 `T2_replace = D_n²/2` (quadratic, 当前 yaml T_2_form="quadratic") 或 `ReLU(D''_n)` (旧 relu_dpp option)

**paper §3.5 写 λ_2 = mass term m_eff/2·D²**: 是 D_n² (单帧值平方, 不是 memory deviation²)

**paper §3.5 写 λ_3 = memory term m_eff·(Σ_1 D)²**: 是 累积差分平方 Σ_{k=1..K} χ(k) D_{n-k} 的平方, 不是 D_n²/2

**错位 binary 判定**:

| 代码 λ_i | 代码乘的 term | paper §3.5 λ_i | paper 应乘的 term | 匹配? |
|---|---|---|---|---|
| λ_1 = 2.3585 (kinetic 1/(2 m_eff)) | T1_velocity = (D_n − D_{n-1})² (velocity²) | λ_1 = 1/(2 m_eff) kinetic | (D_n − D_{n-1})² | ✓ 严格 isomorphic |
| **λ_2 = 0.1060 (mass m_eff/2)** | **T3_memory = (D_n − D̄^EMA)² (memory deviation²)** | **λ_2 = m_eff/2 mass** | **D_n² (mass)** | **✗ 错位** — 代码乘 memory deviation² ≠ paper 想要的 D_n² mass |
| **λ_3 = 0.2120 (memory m_eff)** | **T2_replace = D_n²/2 (quadratic) 或 ReLU(D''_n)** | **λ_3 = m_eff memory** | **(Σ_1 D)² 累积差分** | **✗ 错位** — 代码乘 D_n²/2 quadratic (恰好接近 paper λ_2 mass form 但系数 swap) 或 ReLU(D''_n) ReLU 单边二阶差分 (与 paper Σ_1 D 完全无关) |

**错位是真还是假 binary 判定**: **真存在 ✓ binary**

**具体错位形式**:
1. 代码 `lambda_2` 与 `lambda_3` 在 `compute_loss` 中 **乘的 term 与命名 swap**: 代码 λ_2 (注释 "mass") 实际乘 T3_memory; 代码 λ_3 (注释 "memory") 实际乘 T2_replace (quadratic 或 ReLU)
2. 代码 T2_replace = D_n²/2 (T_2_form="quadratic" 当前默认) 与 paper λ_2 mass = D_n² 形式接近 (但系数差 1/2)
3. 代码 T3_memory = (D_n − D̄^EMA)² 与 paper λ_3 (Σ_1 D)² **完全不匹配** — memory deviation² 与 累积差分² 是 2 个完全不同的数学 object
4. paper §3.7 写 "T_3 memory $m_{\mathrm{eff}}(\Sigma_1 D)^2$" + "T_3 在 generation n 不含 D_n, 仅含 D_{n-1}, ..., D_{n-K}", 这是 history sum squared form; 而代码 T3_memory 含 D_n (因 (D_n − D̄^EMA)² 含 D_n), 数学 object 形式 incompatible
5. paper §3.7 推论 "T_3 在主定理 (2)(3) transient 速率证明中 不 贡献 因 ∂T_3/∂D_n = 0" 依赖 paper T_3 = (Σ_1 D)² history-only form; 但代码 T3_memory 含 D_n 所以 ∂T3_memory/∂D_n ≠ 0, **paper 主定理 (2)(3) attribute 与代码实际 form 不一致**

**整体 isomorphism 评估**:
- 代码 docstring 自己 binding 说 "Σ_2-motivated loss with 25-40% structural correspondence" + "不允许 'Σ_2-isomorphic loss'" wording
- 当前 paper §3.5 / §3.7 写法是 Klein-Gordon Lagrangian 三项 standard form (用 mass + memory + kinetic), 但代码实际是 (velocity + memory deviation + D²/2 quadratic), **paper draft 与代码 not isomorphic**
- D14-D17 必做 3 项之一: **RLHF axis ℒ_矛盾^Hartree 显式推导** 必须 honest reconcile 代码与 paper form, 选 binary 路径之一:
  - 路径 A (改代码 match paper): 把 `lambda_2 * D_n²` (mass) + `lambda_3 * (Σ_1 D)²` (memory) form 重写 compute_loss, 然后 re-run Phase 1 chain ($50 cloud + 5-7 天)
  - 路径 B (改 paper match 代码): paper §3.5 重写 ℒ_矛盾 三项 functional form 为 (velocity + memory deviation + D²/2), 不用 Klein-Gordon Lagrangian wording, paper §3.7 主定理 (2)(3) attribute 重 derive
  - 路径 C (两者并存 disclose): paper §6 + §7.5 honest 写 "current implementation diverges from idealized Klein-Gordon form in 2 places; iteration M2 to reconcile" — 这是 §7.5 retract grandiosity 3 项必做之一

**Verdict 8**: 代码-论文 semantic 错位 **真存在 ✓ binary**, λ_2 / λ_3 同时 (i) 与 paper λ_i 命名 swap + (ii) functional form 完全不同的数学 object。 paper §7.5 retract grandiosity 必须 disclose 此 form gap, 不可继续 claim Σ_2-isomorphic 或 Klein-Gordon Lagrangian standard form。

---

## 第三部分 配置 yaml 一致性 binary 验证

### §3.1 实际配置参数 vs paper 描述对比

**source (本份独立 ssh cat 22 主机 5 个 yaml)**:

| 参数 | shumailov_official | cat_arm_b (旧 framework) | cat_arm_b_v2_dialectical (新) | sensitivity_fp32 | sensitivity_rep_pen_2 |
|---|---|---|---|---|---|
| model.dtype | float16 | float16 (5/10 ROLLBACK) | float16 | **float32** | float16 |
| fine_tune.lr | 2.0e-5 | 2.0e-5 | 2.0e-5 | 2.0e-5 | 2.0e-5 |
| fine_tune.batch | 128 | 128 | 128 | 128 | 128 |
| fine_tune.weight_decay | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| fine_tune.fp16 | true | true (5/10 ROLLBACK) | true | **false** | true |
| fine_tune.lr_scheduler | constant | constant | constant | constant | constant |
| generation.repetition_penalty | 3.0 | 3.0 | 3.0 | 3.0 | **2.0** |
| cat.alpha_scan | – | [0,1,5,10,50] | [0,1,5,10,20] | [0.0] | [0.0] |
| cat.beta_model | – | 0.999 (旧) | **0.999849** (m_eff 0.212) | 0.999 | 0.999 |
| cat.beta_kl | – | 0.9 (旧) | **0.8090** (m_eff 0.212) | 0.9 | 0.9 |
| cat.lambda_1 | – | 1.0 (旧) | **2.3585** (m_eff 0.212) | 1.0 | 1.0 |
| cat.lambda_2 | – | 1.0 (旧) | **0.1060** | 1.0 | 1.0 |
| cat.lambda_3 | – | 1.0 (旧) | **0.2120** | 1.0 | 1.0 |
| cat.T_2_form | – | – | **quadratic** | – | – |
| cat.kl_history_K | – | – | **9** | – | – |

**vs paper 描述**:
- paper §5.2 explicit cite: 5 epochs no_preserve / 10 epochs preserve_10pct / block_size=64 / 5-way beam search / output_size=match_original ✓ 全 match yaml
- paper §5.2 未明示项: optimizer / lr / batch_size / weight_decay / fp16 (subagent 默认 AdamW / 2e-5 / 8 / 0.01 / fp16)
- **yaml 与 paper-explicit 部分**: ✓ binary 全 match
- **yaml 与 paper-implicit 部分**: per_device_train_batch_size 在 audit-fixed = 128 (不是 sub-agent 默认 8, 与 effective batch 32 不一致), fp16 默认 (paper 未 明示)

### §3.2 5/8 audit-fixed 后实际 config 状态

**audit fix (5/8 09:17-27) 的具体改动**:
- batch_size: 8 (sub-agent 默认) → **128** (audit-fixed, train data 36k blocks 单 epoch ~281 step)
- lr_scheduler: linear (HF default) → **constant** (audit-fixed)
- repetition_penalty: paper §5.2 写 "2.0" → **3.0** (Shumailov official Zenodo code, audit 推 paper 2.0 是 typo)
- gradient_accumulation_steps: 4 (sub-agent 默认 effective batch 32) → **1** (audit-fixed, effective batch = 128)
- weight_decay: 0.01 ✓ unchanged

**audit fix rationale**:
- Shumailov official Zenodo repo (HF train_clm.py) 用 batch=128 + lr=2e-5 const + rep_penalty=3.0
- paper §5.2 prose 与 Zenodo code 之间有 typo 不一致, audit 推 Zenodo 是 source of truth
- 5/10 ROLLBACK to fp16: caveat "framework freeze D3-D4 binding" 即 5/9 chain 数据 stack 必须 same setup
- sensitivity_fp32_baseline.yaml + sensitivity_rep_penalty_2.yaml 是反题姐姐 §3 P0-B3/B4 push 的 sensitivity check 但**尚未实跑** (logs/ 无对应 jsonl)

**关键 binary 判定**:

| 维度 | yaml 实际 | paper 描述 | 一致? |
|---|---|---|---|
| Shumailov §5.2 explicit (5 epochs / block=64 / 5-beam / match_original / 2 conditions) | ✓ | paper-cite | ✓ binary |
| audit-fixed setup (batch=128, lr=2e-5 const, rep_pen=3.0, fp16) | ✓ | paper 未明示 / sub-agent 默认 | partial ✓ (paper-implicit 与 Shumailov Zenodo 一致) |
| cat_arm_b_v2_dialectical 三 λ + β | ✓ (m_eff=0.212 direct fit) | paper §3.5 Klein-Gordon λ_i | ✗ 二元错位 (λ_2 / λ_3 swap + functional form 不同) — 见 §2.3 |
| sensitivity_fp32 / rep_pen=2 sensitivity 实验 | **未跑** | 反题姐姐 P0-B3/B4 push | ✗ pending |

**Verdict 9**: yaml 配置与 paper-explicit 部分 **全 ✓ binary match**, 与 paper-implicit 部分 partial ✓ (Shumailov Zenodo source of truth), 但 **cat λ_i 与 paper §3.5 Klein-Gordon form 错位** (与 §2.3 同样的二元错位), 且 sensitivity_fp32 / sensitivity_rep_pen 反题姐姐 push 的 P0 sensitivity 实验**未实跑**, paper §6 disclose [?] pending。

---

## 第四部分 SUBSTANTIVE_TRAJECTORY 与 HOST22_GROUND_TRUTH cross-verify

### §4.1 SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 claim 数字 verdict

| Claim | 5/12 早 claim 数字 | 22 主机原始 jsonl 实读独立 verify | 误差 / Verdict |
|---|---|---|---|
| A: α=10 seed=1 plateau gen 6-9 mean = 57.32 | 57.32 | 本份 (61.4528+56.9385+53.7419+57.1681)/4 = **57.3253** | **≈ 0 ✓ 准** |
| A: α=0 seed=1 plateau gen 6-9 mean = 59.84 | 59.84 | 本份 (62.5596+58.7092+58.9415+59.1362)/4 = **59.8366** | **≈ 0 ✓ 准** |
| A: Δ = −4.2% | −4.197% | 本份 −4.197% | **≈ 0 ✓ 准** |
| B (隐含): α=10 seed=2 vs α=0 seed=2 反向 +7.82% | +7.82% | 本份 +7.815% | **≈ 0 ✓ 准** |
| C: D4 N=4 paired mean = −0.57%, p = 0.82 | −0.57%, p=0.82 | 本份 rel mean = **−0.5734%**, p = **0.8180** | **✓ 准** (HOST22 §1 §7.1 把这点错算 +0.35% / p=0.94, 与 SUBSTANTIVE claim 不一致, 但本份独立 verify 与 SUBSTANTIVE claim 一致, HOST22 错位 1 处 — α=10 seed=4 plateau) |
| D: Partial D4 5/5 PASS STRONG ROBUST | 5/5 PASS | 本份 4/5 PASS + 1/5 (Criterion 5 sliding-window) [?] judgement | **4/5 严格 PASS ✓ + 1/5 wording [?] 但 verdict 实质一致** |
| E: gen 0 std 0.22%, spike min 2.89×, plat/peak max 0.568 | 0.22% / 2.89× / 0.568 | 本份 **0.217% / 2.8926 / 0.5676** | **≈ 0 ✓ 准** |

### §4.2 关键 cross-verify catches

**Catch 1 (HOST22 错位修正)**: HOST22_GROUND_TRUTH 报告 §1 §7.1 给 N=4 paired abs mean = "+0.1166" + rel mean = "+0.354%" + p = "0.9407", 但本份独立 jsonl 实读 + python 重算:
- abs mean = **−0.4153**(HOST22 报 +0.1166 → 错位)
- rel mean = **−0.5734%**(HOST22 报 +0.354% → 错位 +0.927pt, 方向也反)
- p (df=3 two-sided) = **0.8180**(HOST22 报 0.9407 → 错位)
- t-stat = **−0.2510**(HOST22 报 +0.0807 → 错位)

**错位原因 (本份调查)**: HOST22 §2.3 表格 α=10 seed=4 trajectory 行 显示 "56.95 / 54.22 / 52.68 / 53.35" — 这与原始 jsonl 一致, 但 §1 §7.1 paired stats 部分 用了 seed=4 plateau = "56.4277" + Δ_rel "−1.61%" — 56.4277 不知出处, 实际 plateau g6-9 mean = (56.95 + 54.22 + 52.68 + 53.35) / 4 = **54.30**, 不是 56.43。HOST22 §1 §7.1 数字错位, 而 §2.3 表格数字对。**本份重新算后 N=4 paired 结论实际**与 SUBSTANTIVE claim "−0.57%, p=0.82" **完全一致** ✓。

**Catch 2 (paper §3.5 与代码错位真存在)**: HOST22 §4 §7.3 已 catch 代码-paper λ_2 / λ_3 form 错位, 本份 §2 独立 verify 确认 **真存在 ✓ binary**, 具体 form: (i) 代码 λ_2/λ_3 命名与 paper 命名 swap; (ii) 代码 T3_memory = (D_n−D̄^EMA)² 与 paper T_3 = (Σ_1 D)² 完全不同的数学 object。

**Catch 3 (Phase 1 chain 实际比 ETA 早 24h)**: HOST22 §6 catch 5/12 10:05 完成 vs SUBSTANTIVE ETA 5/13 早 — 本份独立 verify chain_done timestamp 2026-05-12T02:05:29Z UTC = 5/12 10:05 CST, **早 24-30h ✓ binary**。

**Catch 4 (Criterion 5 sliding-window judgement [?] wording inconsistency)**: HOST22 §7 caveat "verdict report 自身判定 logic [?] but consistent" 本份 §1.4 独立确认 — partial_D4 报告 "ratio 1.626 PASS < 5% deviation" wording 与实际 ratio - 1.0 = 62.6% 不 match, judgement wording 不严谨, 但与 paper main U-shape claim 无关。

### §4.3 哪些 claim 真 / 哪些 claim 偏 / 哪些 claim 错

| SUBSTANTIVE_TRAJECTORY claim | 本份独立 verify 结果 | 二元 |
|---|---|---|
| A: α=10 seed=1 −4.2% plateau (single-seed) | 数字 ✓ 准, 但 single-seed 引用作 "first multi-seed F2 weak framework effect" 在 N=4 paired ground truth 出来后 substantive 上**应 retract** | 数字 **真** / framing **错** |
| B: α=10 seed=2 +7.82% plateau (反例) | 数字 ✓ 准 | **真** |
| C: D4 N=4 paired −0.57%, p=0.82, F3 NOT substantiated | 本份独立算 **完全一致** −0.57% / p=0.82 | **真** |
| D: Partial D4 5/5 PASS STRONG ROBUST | 4/5 严格 + 1/5 wording [?] 但 verdict 一致 | **真** (verdict-level) |
| E: gen 0 std 0.22%, spike min 2.89×, plat/peak max 0.568 | 本份独立算完全一致 0.217% / 2.8926 / 0.5676 | **真** |
| NMI 17-23% lever (a) 升级 +20pt | 数据 ground 是 α=10 seed=1 single-seed −4.2%, N=4 paired ground truth 出来后**应 retract +2pt 升级**(撤回 "first multi-seed F2 weak framework effect") | **数据 ground 错 — 实际 N=4 F3 NOT substantiated** |
| NMI 17-23% lever (c)(d) 升级 +30pt / +40pt | 主要是哲学/概念 reframe ground (cybernetic homeostasis tier + dialectical 实践 novel content tier), 不直接依赖 framework empirical effect | **概念 ground robust, 但 lever 实际 +pt 需打折 — 因 lever (a) substantive 升级数据失败** |
| 真做 D14-D17 3 项必做后 NMI 24-34% | 假设 3 项 (Phase 5 N=1 + RLHF axis 显式推导 + §7.5 retract) 真做, lever (a) substantive 数据 ground 仍是 N=4 F3 NOT substantiated → 24-34% 偏 optimistic 约 5-8pt | **偏 optimistic** |

**整体 cross-verify**:
- SUBSTANTIVE 数字 5/5 关键数字 ✓ 准
- SUBSTANTIVE 升级 lever (a) framing 与 N=4 paired ground truth substantive 矛盾 — α=10 seed=1 single-seed positive 不应作 "first multi-seed F2 weak framework effect" 升级数据 ground
- HOST22 §7.1 数字 error 1 处 (seed=4 plateau 错算 56.43 实际 54.30) 反而**导致 HOST22 paired stats +0.35%** 误导 — 本份 ground truth recompute 与 SUBSTANTIVE claim −0.57% / p=0.82 **完全一致**

---

## 第五部分 当前实证严格度整体二元判定

### §5.1 实证 hygiene 维度

| 维度 | 状态 | binary |
|---|---|---|
| Shumailov 严格镜像 baseline jsonl (audit-fixed 完整 10 gen) | ✓ 真完整 1 个 | **真完整** |
| Shumailov 早期 (audit pre-fix 5/7) baseline jsonl (10 gen) | ✓ 真完整 1 个 | **真完整** (用于 audit 对照) |
| α 全扫描 single-seed seed=42 (α=0/1/5/10) 完整 10 gen | ✓ 真完整 4 个 | **真完整** |
| α=50 数值崩溃 (no generation_done) | ✓ disclose pending | **真崩溃 ✓** |
| Phase 1 chain multi-seed α=0 seed 1-4 完整 10 gen | ✓ 真完整 4 个 | **真完整** |
| Phase 1 chain multi-seed α=10 seed 1-4 完整 10 gen | ✓ 真完整 4 个 | **真完整** |
| α=0+α=10 seed=0 双 α 全 fail (ROCm bug, Verdict B) | ✓ 真 audit jsonl 实证 | **真 ✓** |
| chain_done 时戳 5/12 02:05 UTC | ✓ 真 | **真完整** |

**实验 hygiene 总判: ✓ 真完整 binary** — 19 个真有数据的 jsonl + 1 个 audit jsonl + 5 个 yaml + 1 个 Python 源文件全部 ground truth 验证一致 (除 HOST22 §7.1 数字错位 1 处, 本份独立 verify 修正)。

### §5.2 实证 substantive 维度

| 维度 | 状态 | binary |
|---|---|---|
| Shumailov baseline 复现 F1 collapse_reproduced + F3 fine_tune_sanity | ✓ PASS | **真复现** ✓ |
| α 全扫描 single-seed seed=42 4/5 档 PASS + α=50 数值崩溃 disclose | ✓ partial PASS (5/5 档 expected 是 PASS, α=50 paper §4 footnote disclose) | **真复现** ✓ |
| α=10 vs α=0 single-seed seed=42 plateau effect | −1.7% (实测) 远 < paper prediction "15-25% reduction" | **paper prediction 严格 binary 失守** F4 paper-prediction-falsification 实质上 hold |
| α=10 vs α=0 N=4 paired plateau effect | −0.57% rel mean, p = 0.82, F3 NOT substantiated | **framework empirical effect 不显著 binary** |
| Partial D4 5/5 PASS (4/5 严格 + 1/5 wording [?]) | shape robustness 真鲁棒 4/4 U + gen 0 rel std 0.22% + spike min 2.89× + plat/peak max 0.568 | **真鲁棒** ✓ |
| α=10 hang Verdict B (ROCm bug not framework boundary) | ✓ logic 完整 (α=0 seed=0 也 fail) | **真 ✓ binary** |
| 代码 λ_2 / λ_3 与 paper §3.5 Klein-Gordon form 错位 | ✓ 真存在 binary (code-paper form gap) | **真错位** ✗ paper claim Klein-Gordon Lagrangian form 严格 binary 失守 |
| sensitivity_fp32 / sensitivity_rep_pen 反题姐姐 P0-B3/B4 | **未实跑** | **未做** ✗ pending |
| Phase 2/3 dialectical α scan (D7-9+ 计划) | **未实跑** | **未做** ✗ pending |
| RLHF axis ℒ_矛盾^Hartree 显式推导 (D14-D17 必做之一) | **未做** | **未做** ✗ pending |
| Phase 5 N=1 Llama-8B + ℒ_矛盾 demonstrated result ($50 cloud) | **未做** | **未做** ✗ pending |
| §7.5 retract grandiosity (D14-D17 必做之一) | **未做** | **未做** ✗ pending |
| paper §6 disclose 代码-paper form 错位 | **未 disclose** | **未做** ✗ pending |

**实证 substantive 总判: 部分 ✓ + 关键 ✗ binary** — Shumailov baseline 复现 + Partial D4 shape robustness 真 substantive PASS, 但 (a) framework α=10 vs α=0 multi-seed paired effect 不显著 + (b) 代码-paper form 错位 + (c) sensitivity / Phase 2/3 / Phase 5 / RLHF axis / §7.5 retract 全 pending = 当前 substantive 状态 **不可claim "framework 真 demonstrated empirical effect"**, 只能 honest claim "Shumailov baseline 真复现 + U-shape 跨 seed 鲁棒 + framework α=10 vs α=0 N=4 paired effect not significant (p=0.82)"。

### §5.3 期刊档位二元判定

| 期刊档 | 当前实证严格度判定 | 接受率估算 |
|---|---|---|
| **Nature 系档 (NMI / Nature Machine Intelligence)** | **不可投 binary** | 5-15% 中位 ~10% |
| 理由 | (1) framework empirical effect N=4 paired 不显著 (F3 NOT substantiated), 不能 claim "demonstrated novel framework effect"; (2) 代码-paper form 错位 honest disclose 后 novelty 严重下降; (3) 缺 multi-architecture (只 OPT-125m) + 缺 multi-dataset (只 wikitext2) + 缺 Phase 5 demonstrated result; (4) Nature reviewer 看到 N=4 paired p=0.82 + code-paper form gap 大概率 reject in 1 round | (假设 D14-D17 3 项必做完成 + senior 加持 18-26%, 最 optimistic) |
| **TMLR / KBS Q1 档** | **可投 ✓ binary** | 45-65% 中位 ~55% |
| 理由 | (1) Shumailov baseline 真复现 + 4 seed multi-seed shape robustness 鲁棒 + α 扫描 5 档 jsonl 完整 = strong empirical hygiene; (2) 代码-paper form 错位 honest disclose 后 framework 还有 U-shape 跨 seed 鲁棒性 + Shumailov 复现 + α 扫描完整 substantive content; (3) TMLR no novelty bar (rigor-focused review), KBS Q1 一般接受 "rigorous negative / null result" 是 fit | (D14-D17 3 项必做完后 65-75%) |
| **TMLR 档 (no novelty bar)** | **可投 ✓ binary** | 60-75% 中位 ~67% |
| 理由 | TMLR 接受 "claims accurately supported by evidence" 是核心准则; 当前 framework empirical effect not significant 是 honest claim, 不是 framework demonstrated; 但 baseline 复现 + multi-seed robustness 是 hygienic contribution | |
| **arXiv 5/31 + Anthropic fellowship + cumulative parallel** | **可发可投 ✓ binary** | 80-90% cumulative ≥1 接受 by 12 月 |
| 理由 | 5 leg parallel (NeurIPS 2026 5/29 + TMLR + arXiv 5/31 + NMI B 6-12 月 + Anthropic fellowship) cumulative ≥1 接受 robust path | |

**整体二元判定**: **TMLR 档 — KBS 档 (~50-60%)** 是当前实证严格度 honest match, 不可走 Nature 系 single-leg (NMI 当前 5-15%, 真做 D14-D17 后 18-26%, 仍 < 30% 不能 "ready" per CLAUDE.md 规则 1)。

---

## 第六部分 多架构 + 多数据集 + Phase 5 N=1 启动状态

### §6.1 多架构状态

**当前实证范围**: facebook/opt-125m **单一 model 架构** (OPT-125m, 12 layers, 768 hidden dim, 125M params)
- paper claim "self-iteration 矛盾框架 framework" 但只在 OPT-125m 验证
- 没在 GPT-2 / Llama / Mistral / Pythia 等其他 architecture 验证
- 反题姐姐 P0-A1 一直 push "multi-arch generality" 但**未做**

**Phase 5 N=1 Llama-8B 状态**:
- SUBSTANTIVE 5/12 凌晨晚 标 D14-D17 必做 3 项之一 ($50 cloud 3-5 天)
- **当前状态**: 未启动, 22 主机 RX 9070XT 16GB 跑不动 Llama-8B fp16 (需要 ~16GB weight + activation + EMA model 双倍 ~32GB), 必须 cloud (e.g. RunPod A100 40GB)
- **binary**: ✗ **未启动**

### §6.2 多数据集状态

**当前实证范围**: wikitext-2-raw-v1 **单一 dataset**
- paper claim "self-iteration model collapse" 但只在 wikitext-2 验证
- 没在 c4 / openwebtext / pile / wikipedia / arXiv 等其他 dataset 验证
- 反题姐姐 P0-A2 一直 push "multi-dataset generality" 但**未做**

**binary**: ✗ **未启动**

### §6.3 Phase 5 N=1 启动状态 (D14-D17 必做之一)

- **未启动**: 未开始 cloud setup, 未上传 dataset, 未跑 Llama-8B + ℒ_矛盾 demonstrated result
- 真做 ETA 3-5 天 ($50 cost)
- **binary**: ✗ **未启动**

### §6.4 D14-D17 必做 3 项之一其他状态

| D14-D17 必做项 | 状态 |
|---|---|
| Phase 5 N=1 Llama-8B + ℒ_矛盾 demonstrated result ($50 cloud) | ✗ 未启动 |
| RLHF axis ℒ_矛盾^Hartree 显式推导 §3 | ✗ 未做 (paper §3.5 当前 Klein-Gordon form 但与代码错位; honest derivation 需要 path A/B/C 之一 binary 选) |
| §7.5 retract grandiosity (30 min) | ✗ 未做 |
| §7.1 4 候选 substantive 比较 | ✗ 未做 |
| 整合 v3 (含 5 项 reframe + α=10 multi-seed F2 verdict) | ✗ 未做 |
| Phase 1 chain Phase 1 真完整 | ✓ 已 5/12 10:05 完成 |

**整体 D14-D17 真启动状态: 1 / 6 ✓ ( Phase 1 chain), 5 / 6 ✗ pending**

---

## 第七部分 关键风险 flag + 给 Linux 姐姐主会话的硬数字

### §7.1 硬数字 ground truth (本份独立 verify, 可直接引用)

```
=== Shumailov 严格镜像 baseline (audit-fixed seed=42, 5/8 092730) ===
gen 0 = 36.3540
gen 9 = 53.9805
gen 0-9: 36.35 / 78.22 / 103.61 / 88.16 / inf / 57.19 / 53.78 / 52.62 / 53.87 / 53.98
plateau gen 6-9 mean (skip inf): 53.5615
F1 PASS (delta +17.63 >= +5), F3 PASS (gen0 36.35 <= 50)

=== α 扫描 single-seed seed=42 ===
α=0:  plateau gen 6-9 mean = 57.41 (baseline)
α=1:  plateau gen 6-9 mean = 58.10  (Δ_rel +1.2%)
α=5:  plateau gen 6-9 mean = 59.68  (Δ_rel +4.0%)
α=10: plateau gen 6-9 mean = 56.43  (Δ_rel −1.7%)
α=50: gen 0 step 数学崩溃 (no generation_done)

=== Phase 1 chain multi-seed (4 seed each α) ===
α=0  seed=1 plateau gen 6-9 mean: 59.8366
α=0  seed=2 plateau gen 6-9 mean: 54.0314
α=0  seed=3 plateau gen 6-9 mean: 54.3351
α=0  seed=4 plateau gen 6-9 mean: 57.3506
α=10 seed=1 plateau gen 6-9 mean: 57.3253 (Δ_rel −4.197%)
α=10 seed=2 plateau gen 6-9 mean: 58.2541 (Δ_rel +7.815%)
α=10 seed=3 plateau gen 6-9 mean: 54.0131 (Δ_rel −0.593%)
α=10 seed=4 plateau gen 6-9 mean: 54.3000 (Δ_rel −5.319%)

=== N=4 paired t-test (本份独立算) ===
paired abs mean: -0.4153
paired abs SD:   3.3095
paired abs SE:   1.6547
t-stat (df=3):  -0.2510
two-sided p:     0.8180
paired rel mean: -0.5734%
paired rel SD:   5.9448%
F3 NOT substantiated (framework α=10 vs α=0 plateau effect not significant)

=== α=0 multi-seed (seed 1-4) baseline ===
gen 0 mean:  36.3197
gen 0 std:   0.0789
relative std: 0.217%
spike ratio min: 2.8926 (seed=4)
spike ratio max: 2.9626 (seed=2)
plateau/peak min: 0.5035 (seed=2)
plateau/peak max: 0.5676 (seed=1)
4/4 U-shape

=== Phase 1 chain audit jsonl ===
chain_start: 2026-05-10T04:58:05Z UTC (5/10 12:58 CST)
chain_done:  2026-05-12T02:05:29Z UTC (5/12 10:05 CST)
elapsed: ~45h 7min
8/10 jobs ✓ done, 2/10 seed_skipped (α=0 seed=0 + α=10 seed=0, 共 3 attempt 全 watchdog killed)
```

### §7.2 关键风险 flag

**Flag 1 [P0]**: SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 NMI 17-23% claim **数据 ground 真有 substantive gap**:
- Lever (a) +20pt 升级中 +2pt 是 "α=10 seed=1 first multi-seed F2 weak framework effect"
- N=4 paired ground truth = mean −0.57%, p=0.82 (F3 NOT substantiated)
- 该 +2pt 升级**应 retract**, NMI 修订 → 14-19% (降 3-5pt)
- 真做 D14-D17 3 项必做后 (Phase 5 N=1 + RLHF axis 显式推导 + §7.5 retract): 修订 NMI 20-28% (降 4-6pt vs SUBSTANTIVE 24-34%)
- 加 senior 合作者: 修订 NMI 30-40% (vs SUBSTANTIVE 34-45%)
- 整体: SUBSTANTIVE 17-23% **偏 optimistic 3-5pt**, honest range = **14-19%**

**Flag 2 [P0]**: 代码 contradiction_loss.py λ_2 / λ_3 与 paper §3.5 ℒ_矛盾 Klein-Gordon Lagrangian form **真二元错位 binary**:
- 代码 λ_2 (注释 "mass m_eff/2") 实际乘 T3_memory = (D_n − D̄^EMA)² (memory deviation²)
- 代码 λ_3 (注释 "memory m_eff") 实际乘 T2_replace = D_n²/2 (quadratic) 或 ReLU(D''_n)
- paper §3.5 λ_2 = m_eff/2 应乘 D_n² (mass)
- paper §3.5 λ_3 = m_eff 应乘 (Σ_1 D)² (memory history sum)
- paper §3.7 主定理 (2)(3) attribute "T_3 在 transient 速率证明中 不 贡献 因 ∂T_3/∂D_n = 0" 依赖 paper T_3 = (Σ_1 D)² history-only form; 但代码 T3_memory 含 D_n 所以 ∂T3_memory/∂D_n ≠ 0, **paper 主定理 (2)(3) 数学证明与代码 not isomorphic**
- D14-D17 RLHF axis ℒ_矛盾^Hartree 显式推导必须选 path A (改代码 match paper) / B (改 paper match 代码) / C (并存 disclose), 不可继续 claim Klein-Gordon Lagrangian standard form

**Flag 3 [P1]**: N=4 sample size 太小, paired t-test power 不足:
- N=4 + SD 3.3 / 5.94% → 检测 effect size 0.5σ 需要 N≈30
- 即 framework 真实 effect 即使是 −2% 或 +2% 也可能 N=4 检测不到
- paper §6 应 disclose "N=4 paired test underpowered; larger multi-seed (N ≥ 8-10) needed in future work"
- D14-D17 之后 D18-D24 可启动 N=8-10 paired (但 ROCm watchdog seed=0 fail 风险持续)

**Flag 4 [P1]**: α=10 seed=0 双 α seed=0 全 fail (audit jsonl 实证 rc=137 watchdog killed) 与 framework 无关 (alpha10_hang_diagnosis Verdict B = ROCm bug), 但 paper §6 应 honest disclose "10 paper-convention seeds attempted, 8 / 10 successful (seed=0 hardware-driver-instability, not framework-caused)" — 当前 paper draft 还**没**写这个 disclose。

**Flag 5 [P1]**: sensitivity_fp32_baseline.yaml + sensitivity_rep_penalty_2.yaml 反题姐姐 §3 P0-B3/B4 push **未实跑**:
- P0-B3 (rep_penalty=2.0 vs 3.0 sensitivity): paper §5.2 prose 写 "2.0" vs Zenodo code "3.0", audit 推 typo; 跑 rep_penalty=2.0 single-seed α=0 verify trajectory 是 monotone collapse 还是 U-shape 可二元判定 audit 对不对
- P0-B4 (fp16 vs fp32 sensitivity): 验证 gen 0 baseline = 36 是否 fp16 numerics artifact (paper 报 34)
- 这 2 个 sensitivity 真做后 (~12-20h GPU) paper §6 可 disclose "audit 推 paper 2.0 是 typo, fp32 复测 gen 0 = X (与 fp16 36 相差 Y%)", 增加 hygiene robustness

**Flag 6 [P2]**: Partial D4 Criterion 5 sliding-window vs chunked ratio 1.626 不是 "< 5% deviation" — verdict 报告自身判定 wording 与 logic 不一致:
- chunked eval 与 sliding-window eval 是 2 个不同 evaluation method, 数值 expected 系统差
- 把 1.626 / 1.0 = 62.6% 差当 "< 5% deviation" PASS 是 wording bug
- 但与 paper main U-shape claim 无关
- D14-D17 可顺手改 partial_D4_shape_verdict_20260511.md §3 Criterion 5 wording

**Flag 7 [P2]**: HOST22_GROUND_TRUTH 报告 §1 §7.1 N=4 paired stats 错位 1 处:
- HOST22 报 abs mean = "+0.1166", rel mean = "+0.354%", p = "0.9407", t = "+0.0807"
- 实际 (本份独立 verify) abs mean = −0.4153, rel mean = **−0.5734%**, p = **0.8180**, t = **−0.2510**
- 错位来自 α=10 seed=4 plateau 数字错算 (HOST22 §1 §7.1 用 56.4277 实际 jsonl 54.30)
- HOST22 §2.3 表格数字对, 但 §1 §7.1 paired stats 数字错
- 本份独立 verify **修正后与 SUBSTANTIVE_TRAJECTORY claim "−0.57% / p = 0.82" 完全一致** ✓
- HOST22 应 update §1 §7.1 数字 (本份已 disclosed)

### §7.3 真实 NMI 接受率 honest reconsidered

| 状态 | NMI combined 中位 | 修订原因 |
|---|---|---|
| SUBSTANTIVE 5/12 凌晨晚 claim | 17-23% (中位 ~20%) | take α=10 seed=1 single-seed positive 作 first multi-seed F2 evidence + 5 项 reframe |
| **HOST22 5/12 晚修订 (但数字错位)** | 10-15% (中位 ~12%) | catch N=4 paired 不显著 (但 HOST22 算成 +0.35% 与 SUBSTANTIVE −0.57% 反向, 实际不影响 verdict) |
| **本份独立 verify ground truth 修订** | **14-19% (中位 ~16%)** | (1) N=4 paired ground truth = −0.57%, p=0.82 (F3 NOT substantiated) → lever (a) +2pt 撤回; (2) Partial D4 5/5 PASS + Shumailov baseline 复现 + 5 项 reframe 概念 ground 保留; (3) 代码-paper form 错位 disclose 后 novelty 下降 ~3-5pt |
| + D14-D17 真做 3 项必做 (Phase 5 N=1 + RLHF axis 显式推导 + §7.5 retract + 代码-paper form 错位 disclose) | **22-30% (中位 ~26%)** | Phase 5 N=1 + form gap honest disclose substantive 升, 主要靠概念 reframe ground 不靠 framework empirical effect |
| + 资深合作者加持 | **30-40% (中位 ~35%)** | Tier 1 boundary territory, 仍未达 NMI ready 标准 (规则 4 接受率 ≥ 30% 才说 ready) |

**含义**: SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 NMI 17-23% claim **偏 optimistic 约 3-4pt** (HOST22 数字错位但 verdict 方向对, 本份独立 ground truth 修订 14-19%)。**真做 D14-D17 3 项必做 + 资深合作者 = 30-40%** 才 reach NMI ready boundary territory (规则 4 ≥ 30%)。当前 NMI **不可投** (5-15% 中位, 远 < 30%)。

**Recommendation**: 走 TMLR + KBS Q1 + arXiv 5/31 + Anthropic fellowship + NeurIPS 2026 5/29 cumulative 5 leg parallel = cumulative ≥1 接受 by 12 月 **80-90%**, 不 single-leg NMI gamble。

---

## §8 文件 cross-ref

- **本份**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/EXP_RIGOROUS_VERIFY_20260512.md`
- 第一次派遣 ground truth report: `GROUND_TRUTH_INVENTORY_20260512.md`
- 第二次派遣 22 主机 ground truth report: `HOST22_GROUND_TRUTH_20260512.md` (本份独立 verify catch §7.1 数字错位 1 处)
- SUBSTANTIVE 主 synthesis: `SUBSTANTIVE_TRAJECTORY_20260512.md`
- Partial D4 verdict (22 主机原始): `partial_D4_shape_verdict_20260511.md` (Criterion 5 wording [?])
- α=10 hang diagnosis (22 主机原始): `alpha10_hang_diagnosis_20260511.md`
- Sliding-window verdict (22 主机原始): `sliding_window_eval_verdict_20260510.md`
- Paper §3-§4-§6 dialectical full (主稿 v1, λ Klein-Gordon form): `paper_section3_4_6_dialectical_full_20260509.md`
- Paper §3-§4-§5-§6 REVISION (5/10 凌晨, λ_3 option-β χ exp form): `paper_section3_4_5_6_REVISION_20260510.md`
- Paper first-principles 重写 (5/11 凌晨, Q3 反映论 + 4 reframe): `paper_first_principles_rewrite_20260511.md`
- 5/9 三 agent 7 P0 verdict: `THREE_AGENT_VERDICT_SYNTHESIS_20260509.md`
- 22 主机 contradiction_loss.py 完整代码: 本报告 §2.1 paste 关键段, 完整文件在 22 主机 `src/contradiction_loss.py`
- 22 主机 yaml 5 个完整文件: `configs/{shumailov_baseline, shumailov_official, cat_arm_b, cat_arm_b_v2_dialectical, sensitivity_fp32_baseline, sensitivity_rep_penalty_2}.yaml`
- 22 主机 audit jsonl: `logs/phase1_robust_20260510_125805.audit.jsonl`
- 22 主机 backup jsonl (已 scp 到 36 server): `logs/host22_backup_20260512/`

—— Linux 姐姐数学层第三次派遣子协作者 B (Opus 4.7), 2026-05-12 下午 CST
