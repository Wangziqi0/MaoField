# exp018_cat MaoField framework 实验层 100% 落地 verify 报告

**日期**: 2026-05-13
**子协作者**: Claude opus 4.7 (1M context) — 数学 verify 角色
**任务**: 重新读 22 主机 + 本机 backup 全部 jsonl,重新算 framework 全部实验数字 + bootstrap CI,不允许引用前份报告数字转述
**完成度**: 6 task 全部完成,所有数字从 jsonl 实读
**关键修正**: F2 → F3 (verdict 倒转,详见第二节 / 组五)

---

## 0. Metric 选择关键决定 (影响 verdict 倒转)

**严重 finding**:在 `cat_enabled=True` 模式 (armb alpha > 0) 下,`val_perplexity` 与 `test_perplexity` 差异显著 (1.5×-2.3×),原因是 trainer 在 val phase 把 cat loss (KL 矛盾约束) 一起累加入 ppl 计算;`test_perplexity` 在独立 eval phase 算 (纯 CE),才是与 Shumailov paper 可比的 framework-clean metric。

**证据 (armb alpha=10 seed=42 单 seed jsonl 实读)**:
| gen | val_ppl | test_ppl | val/test 比 |
|-----|---------|----------|------------|
| 1   | 117.249 | 72.846   | 1.61× |
| 2   | 223.904 | 98.543   | 2.27× |
| 9   | 91.438  | 53.387   | 1.71× |

**对比 alpha=0 / Shumailov (cat_enabled=False)**:val 与 test 偏差 < 2%,一致。

**结论**:
- **所有 framework effect 评估必须用 test_ppl 为 primary metric**
- `val_ppl` 仅用作 internal training signal,不作 framework metric

旧的 F 报告 / 主 agent 估计 (用 val_ppl 算 paired) 给出 mean +14.45% F4 counter-effect — **错指标**。
用 test_ppl 算 paired (本报告):mean -0.57% 与 p=0.82 → **F3 NOT substantiated**

---

## 1. jsonl manifest (22 主机 + 本机 backup)

### 22 主机 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/` 完整 jsonl (≥5 gens)

| 文件 | size (B) | 行数 | gens | 用途 |
|-----|---------|------|------|------|
| `shumailov_no_preserve_seed42_20260508_092730.jsonl` | 5126 | 11 | 10 | 组一 Shumailov 基线 |
| `shumailov_no_preserve_seed42_20260507_200657.jsonl` | 5057 | 11 | 10 | 较旧版,本报告用最新 |
| `armb_alpha0.0_seed42_20260508_144612.jsonl` | 4800 | 11 | 10 | 组二 alpha=0 seed=42 |
| `armb_alpha1.0_seed42_20260509_000459.jsonl` | 4799 | 11 | 10 | 组二 alpha=1 seed=42 |
| `armb_alpha5.0_seed42_20260509_044342.jsonl` | 4800 | 11 | 10 | 组二 alpha=5 seed=42 |
| `armb_alpha10.0_seed42_20260508_192435.jsonl` | 4837 | 11 | 10 | 组二 alpha=10 seed=42 |
| `armb_alpha50.0_seed42_20260509_092134.jsonl` | 143  | 1  | 0  | 组二 alpha=50 数值崩溃 |
| `armb_alpha0.0_seed0_20260509_203605.jsonl` | 4784 | 11 | 10 | 额外 seed=0 (不入 N=4) |

### 本机 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/host22_backup_20260512/` (5/12 同步)

| 文件 | size (B) | 行数 | gens | 用途 |
|-----|---------|------|------|------|
| `armb_alpha0.0_seed1_20260510_011048.jsonl` *(5/13 补同步)* | 4777 | 11 | 10 | 组三 alpha=0 seed=1 主 |
| `armb_alpha0.0_seed1_20260510_130149.jsonl` | 4110 | 12 | 10 | seed=1 副,全 NaN (resume 失败) — **跳过** |
| `armb_alpha0.0_seed2_20260510_130255.jsonl` | 4783 | 11 | 10 | 组三 alpha=0 seed=2 |
| `armb_alpha0.0_seed3_20260510_173925.jsonl` | 4777 | 11 | 10 | 组三 alpha=0 seed=3 |
| `armb_alpha0.0_seed4_20260511_090626.jsonl` | 4782 | 11 | 10 | 组三 alpha=0 seed=4 |
| `armb_alpha10.0_seed1_20260511_151847.jsonl` | 4973 | 12 | 10 | 组四 alpha=10 seed=1 (gen 0 = NaN) |
| `armb_alpha10.0_seed2_20260511_200000.jsonl` | 4810 | 11 | 10 | 组四 alpha=10 seed=2 |
| `armb_alpha10.0_seed3_20260512_005523.jsonl` | 4969 | 12 | 10 | 组四 alpha=10 seed=3 (gen 0 = NaN) |
| `armb_alpha10.0_seed4_20260512_052843.jsonl` | 4807 | 11 | 10 | 组四 alpha=10 seed=4 |
| `phase1_robust_20260510_125805.audit.jsonl` | 8529 | 78 | -  | audit log (旁路) |

**数据完整性 [?]**:
- 本机 `logs/` 顶层目录是 5/9 之前的 22 主机 snapshot;multi-seed (seed 1-4) 仅在 backup 目录下
- backup 目录中 `armb_alpha0.0_seed1_20260510_130149.jsonl` 是 resume 失败后全 NaN 文件 — **本分析跳过**
- 已从 22 主机补同步 `armb_alpha0.0_seed1_20260510_011048.jsonl` (5/10 凌晨完整跑) 到 backup

---

## 2. 组一:Shumailov 严格镜像基线

文件:`shumailov_no_preserve_seed42_20260508_092730.jsonl` (seed=42, no_preserve, 10 gens)

### PPL 完整序列 (val + test)

| gen | val_ppl | test_ppl | distinct_3 |
|-----|---------|----------|------------|
| 0 | 36.524 | 36.354 | None |
| 1 | 78.956 | 78.218 | 0.5475 |
| 2 | 104.287 | 103.610 | 0.4112 |
| 3 | 88.857 | 88.160 | 0.3206 |
| 4 | 65.870 | **Inf/NaN** | 0.2951 |
| 5 | 56.369 | 57.192 | 0.2948 |
| 6 | 53.708 | 53.776 | 0.2904 |
| 7 | 52.562 | 52.618 | 0.2859 |
| 8 | 53.502 | 53.871 | 0.2565 |
| 9 | 53.784 | 53.980 | 0.2432 |

[?] gen 4 test_ppl 是 Infinity (jsonl 原始内容是 Infinity float),其 val_ppl 65.87 正常 — 这是 eval pipeline numeric overflow,排除 gen 4 test 后 plateau 算依然 OK

### 滑动窗口 plateau (test_ppl basis)

| 窗口 | mean |
|------|------|
| gen 6-9 mean | 53.5615 |
| gen 5-9 mean (skip gen 4 Inf) | 54.2877 |
| gen 7-9 mean | 53.4899 |

### distinct_3 衰减率

- gen 1 distinct_3 = 0.5475
- gen 9 distinct_3 = 0.2432
- 衰减比 (gen 9 / gen 1) = **0.4441** (44.4% 留存)
- 绝对降幅 = 0.3043

### 与 Shumailov 2024 paper cross-verify

- gen 0 test_ppl = 36.354 (paper baseline ~34, 偏离 +2.354 = +6.92%, 可接受)
- gen 9 test_ppl = 53.980 (paper 端 ~67 严重崩溃,本机数字偏低但方向一致)
- delta = +17.627 (paper F1 criterion: delta >= +5) → **F1 PASS ✓**

[?] N=1 single seed Shumailov 复测 95% CI 不可估,multi-seed Shumailov 复测列入 future work。

---

## 3. 组二:α 全扫描 single-seed (seed=42, test_ppl primary)

### test_ppl 完整序列

| gen | α=0 | α=1 | α=5 | α=10 | α=50 |
|-----|------|------|------|-------|-------|
| 0 | 36.354 | 36.354 | 36.354 | 36.354 | crash |
| 1 | 77.519 | 69.311 | 71.559 | 72.846 | crash |
| 2 | 108.396 | 89.521 | 100.181 | 98.543 | crash |
| 3 | 91.870 | 81.425 | 89.472 | 87.173 | crash |
| 4 | 73.259 | 74.639 | 79.717 | 71.699 | crash |
| 5 | 61.833 | 64.158 | 70.698 | 63.676 | crash |
| 6 | 59.863 | 60.656 | 64.084 | 59.845 | crash |
| 7 | 56.304 | 59.889 | 60.521 | 55.967 | crash |
| 8 | 57.303 | 55.534 | 58.080 | 56.512 | crash |
| 9 | 56.186 | 56.308 | 56.026 | 53.387 | crash |

### 三阶段定量 (test_ppl basis)

| α | gen 0 | transient max (g1-3) | middle (g4-7 mean) | p_69 | p_59 | p_79 |
|---|-------|---------------------|-------------------|------|------|------|
| 0 | 36.354 | 108.396 | 62.815 | 57.414 | 58.298 | 56.598 |
| 1 | 36.354 | 89.521 | 64.835 | 58.097 | 59.309 | 57.244 |
| 5 | 36.354 | 100.181 | 68.755 | 59.678 | 61.882 | 58.209 |
| 10 | 36.354 | 98.543 | 62.797 | 56.428 | 57.877 | 55.289 |

### 平台相对 α=0 偏移 (test_ppl) — single seed

| α | Δ p_69% | Δ p_59% | Δ p_79% |
|---|---------|---------|---------|
| 1 | +1.19% | +1.73% | +1.14% |
| 5 | +3.94% | +6.15% | +2.85% |
| 10 | **-1.72%** | -0.72% | **-2.31%** |

单 seed=42 alpha=10 plateau 比 alpha=0 plateau 低 **1.72%** (test_ppl),这是 single seed signal,小于噪声 (multi-seed std ~ 6%)。

### U 形特征定量

| α | spike ratio (peak/g0) | plateau/peak |
|---|----------------------|--------------|
| 0 | 2.982 | 0.530 |
| 1 | 2.462 | 0.649 |
| 5 | 2.756 | 0.596 |
| 10 | 2.711 | 0.573 |

四个 alpha 全部 U 形 (spike_ratio > 1.5),plateau 显著低于 peak。**注意 alpha=10 spike 2.71 不比 alpha=0 (2.98) 更显 — 不是 alpha 越大 spike 越大**

### alpha=50 数值崩溃

- run_start jsonl 记录存在 (`alpha=50.0, n_generations=10, smoke_test=False`)
- `stage=generation_done` 数 = **0**
- **判定**:gen 0 step 训练阶段即数值 NaN/Inf,abort 前未 emit 任何 generation_done
- **boundary**:framework alpha 实际 stable 区间在 [0, 10],alpha=50 超界

---

## 4. 组三:Multi-seed alpha=0 (seed 1/2/3/4, test_ppl)

文件:
- seed=1: `armb_alpha0.0_seed1_20260510_011048.jsonl` (5/13 补同步,5/10 凌晨完整跑)
- seed=2: `armb_alpha0.0_seed2_20260510_130255.jsonl`
- seed=3: `armb_alpha0.0_seed3_20260510_173925.jsonl`
- seed=4: `armb_alpha0.0_seed4_20260511_090626.jsonl`

### test_ppl 完整序列

| gen | s1 | s2 | s3 | s4 |
|-----|------|------|------|------|
| 0 | 36.297 | 36.224 | 36.347 | 36.411 |
| 1 | 79.282 | 79.177 | 78.363 | 77.037 |
| 2 | 105.411 | 107.318 | 105.564 | 105.323 |
| 3 | 95.498 | 98.659 | 98.026 | 99.468 |
| 4 | 78.185 | 77.305 | 76.615 | 75.258 |
| 5 | 70.769 | 67.157 | 67.185 | 63.986 |
| 6 | 62.560 | 57.246 | 55.860 | 58.317 |
| 7 | 58.709 | 52.448 | 53.096 | 56.023 |
| 8 | 58.942 | 53.122 | 54.159 | 57.372 |
| 9 | 59.136 | 53.310 | 54.226 | 57.691 |

### Plateau per seed (test_ppl, gen 6-9 mean)

| seed | plateau |
|------|---------|
| 1 | 59.8366 |
| 2 | 54.0314 |
| 3 | 54.3351 |
| 4 | 57.3506 |

### N=4 alpha=0 plateau (test) bootstrap CI

- **mean = 56.3884**
- std = 2.7439
- **95% bootstrap CI: [54.1833, 58.5936]** (10000 resamples, seed=42)

---

## 5. 组四:Multi-seed alpha=10 (seed 1/2/3/4, test_ppl)

文件:
- seed=1: `armb_alpha10.0_seed1_20260511_151847.jsonl` (gen 0 NaN, gen 1-9 OK)
- seed=2: `armb_alpha10.0_seed2_20260511_200000.jsonl`
- seed=3: `armb_alpha10.0_seed3_20260512_005523.jsonl` (gen 0 NaN, gen 1-9 OK)
- seed=4: `armb_alpha10.0_seed4_20260512_052843.jsonl`

### test_ppl 完整序列

| gen | s1 | s2 | s3 | s4 |
|-----|------|------|------|------|
| 0 | NaN→imp 36.297 | 36.224 | NaN→imp 36.347 | 36.411 |
| 1 | 77.185 | 80.249 | 76.594 | 75.564 |
| 2 | 107.208 | 100.272 | 102.380 | 105.209 |
| 3 | 105.316 | 98.427 | 85.488 | 95.663 |
| 4 | 87.318 | 75.698 | 62.415 | 75.233 |
| 5 | 67.524 | 66.400 | 59.079 | 69.393 |
| 6 | 61.453 | 62.994 | 53.699 | 56.947 |
| 7 | 56.939 | 56.741 | 54.517 | 54.223 |
| 8 | 53.742 | 56.383 | 55.069 | 52.678 |
| 9 | 57.168 | 56.898 | 52.767 | 53.351 |

[?] seed=1/3 gen 0 实测 NaN (resume 后 baseline 未 emit),用同 seed alpha=0 gen 0 替代 (alpha 在 gen 0 不应用,base model 同源 by seed)。

### Plateau per seed (test_ppl, gen 6-9 mean)

| seed | plateau |
|------|---------|
| 1 | 57.3253 |
| 2 | 58.2541 |
| 3 | 54.0131 |
| 4 | 54.3000 |

### N=4 alpha=10 plateau (test) bootstrap CI

- **mean = 55.9731**
- std = 2.1348
- **95% bootstrap CI: [54.1565, 57.7897]** (10000 resamples)

---

## 6. 组五:D4 N=4 paired statistics (alpha=10 - alpha=0, test_ppl)

### Paired difference per seed

| seed | α=0 plat | α=10 plat | diff (Δ) | rel % |
|------|----------|-----------|---------|--------|
| 1 | 59.8366 | 57.3253 | **-2.5113** | **-4.20%** |
| 2 | 54.0314 | 58.2541 | **+4.2227** | **+7.82%** |
| 3 | 54.3351 | 54.0131 | -0.3221 | -0.59% |
| 4 | 57.3506 | 54.3000 | **-3.0507** | **-5.32%** |

### Bootstrap CI

- **Paired difference mean = -0.4153**
- std = 3.3095
- **95% bootstrap CI: [-2.7810, +2.5392]** (10000 resamples)

### 相对偏移 %

- **mean rel = -0.57%**
- std rel = 5.94%
- **95% bootstrap CI: [-4.76%, +4.81%]**

### 配对 t 检验

- N = 4, df = 3
- t_stat = -0.2510
- **p-value two-sided = 0.8180**
- p-value one-sided (mean_d < 0, framework lowers PPL) = **0.4090**
- p-value one-sided (mean_d > 0, framework raises PPL) = **0.5910**

### F2 / F3 / F4 binary verdict (test_ppl basis)

| 标准 | 通过? |
|------|------|
| F2 = -2% to -5% with p_one_neg < 0.10 | ✗ FAIL (p_one_neg = 0.4090, mean_rel = -0.57% 在 -2% 之外) |
| F4 = counter-effect mean_rel > 1% with p_one_pos < 0.10 | ✗ FAIL (p_one_pos = 0.591) |
| F3 = NOT substantiated (p_two > 0.10) | **✓ PASS (p_two = 0.818)** |

**Binary verdict: F3 (framework effect NOT substantiated)**

### 重大修正记录

| 来源 | metric | mean rel | verdict |
|------|--------|---------|---------|
| 旧 memory (5/12 凌晨) | seed=1 single, test_ppl | -4.20% | F2 weak framework |
| 主 agent (主会话用 val_ppl) | N=4 paired val_ppl | +14.45% | F4 counter-effect |
| **本报告 (test_ppl primary)** | **N=4 paired test_ppl** | **-0.57% (±5.94%)** | **F3 NOT substantiated** |

**结论**:旧 memory 用 single seed,效应 +-4% level 是 noise 而非 signal;主 agent 用 val_ppl 是 metric 选错 (val 包含 cat loss)。修正后:**framework alpha=10 vs alpha=0 在 test_ppl plateau 上无显著差异,p_two = 0.82**。

---

## 7. 组六:Partial D4 5 criterion 鲁棒性 binary 判定 (test_ppl)

### Criterion 1: U 形 4/4 seeds

| seed | gen 0 (test) | peak (g1-3) | plat (g6-9) | U 形? |
|------|------------|-----------|-----------|------|
| 1 | 36.297 (imp) | 107.208 | 57.325 | ✓ |
| 2 | 36.224 | 100.272 | 58.254 | ✓ |
| 3 | 36.347 (imp) | 102.380 | 54.013 | ✓ |
| 4 | 36.411 | 105.209 | 54.300 | ✓ |

→ **U 形 4/4 ✓ PASS**

### Criterion 2: gen 0 baseline std (alpha=0 multi-seed)

- seed 1 gen 0 = 36.297, seed 2 = 36.224, seed 3 = 36.347, seed 4 = 36.411
- mean = 36.3197, std = 0.0789
- **CV = 0.2171%**
- 阈值 CV < 1.0% → **✓ PASS** (seed-independent baseline)

### Criterion 3: spike ratio min

| seed | spike_ratio (peak/g0) |
|------|----------------------|
| 1 | 2.954 |
| 2 | 2.768 |
| 3 | 2.817 |
| 4 | 2.890 |

- min = 2.768
- 阈值 > 1.5 → **✓ PASS**

### Criterion 4: plateau/peak max

| seed | plat/peak |
|------|-----------|
| 1 | 0.5347 |
| 2 | 0.5810 |
| 3 | 0.5276 |
| 4 | 0.5161 |

- max = 0.5810
- 阈值 < 1.0 (plat 必须低于 peak) → **✓ PASS**

### Criterion 5: 滑动窗口偏差

| seed | w_69 | w_59 | w_79 | max_dev % |
|------|------|------|------|-----------|
| 1 | 57.325 | 59.365 | 55.950 | 5.96 |
| 2 | 58.254 | 59.883 | 56.674 | 5.51 |
| 3 | 54.013 | 55.026 | 54.118 | 1.88 |
| 4 | 54.300 | 57.319 | 53.418 | 7.18 |

- max = 7.18%
- 阈值 < 20% → **✓ PASS** (Shumailov sliding-window 复现 8% 同档)

### Partial D4 总判定: **5/5 PASS → STRONG ROBUST ✓**

形状鲁棒性 (shape robustness) 4 seeds 全部表现:
- U 形 (spike → plateau)
- gen 0 seed-independent baseline (CV 0.22%)
- spike > baseline 1.5×
- plateau < spike (恢复显著)
- sliding-window 一致性 < 8%

---

## 8. m_eff multi-seed N=4 fit + 95% CI

模型:`log P_n = log P_eq + A * exp(-m_eff * n)` from gen 2-9 (alpha=0)

### test_ppl basis fit

| seed | log_Peq | A | **m_eff** |
|------|---------|---|----------|
| 1 | 3.9456 | 1.3456 | 0.2958 |
| 2 | 3.7671 | 1.6261 | 0.2635 |
| 3 | 3.8098 | 1.5890 | 0.2821 |
| 4 | 3.9383 | 1.5914 | **0.3592** |

- **mean = 0.3001**
- std = 0.0415
- **95% bootstrap CI: [0.2715, 0.3399]**

### val_ppl basis fit (cross-verify F report)

| seed | m_eff (val) |
|------|------------|
| 1 | 0.2974 |
| 2 | 0.2603 |
| 3 | 0.2856 |
| 4 | 0.3564 |

- mean = 0.2999, std = 0.0407
- 95% CI: [0.2696, 0.3387]

### 与 F 报告 cross-verify

| 来源 | mean | std |
|------|------|-----|
| F 报告 | 0.300 | 0.042 |
| 本报告 (val) | 0.2999 | 0.0407 |
| 本报告 (test) | 0.3001 | 0.0415 |

**Binary verdict: ✓ 完全匹配** (val 和 test 都匹配,偏离 < 0.001)

---

## 9. J_S 三 method 实拟合 + 95% CI

D_n = log(PPL_n / PPL_0) — 单位 nat (见第 10 节 bridge 推导)

- J_S^(1) = D_1 - D_0 (slope 0→1, since D_0 = 0)
- J_S^(2) = (D_2 - D_0) / 2 (slope 0→2)
- J_S^(3) = mean(D_1-D_0, D_2-D_1, D_3-D_2) (mean rate 0→3)

### test_ppl basis (N=4 alpha=0 seed 1-4 + shumailov_seed42)

| 来源 | J_S^(1) | J_S^(2) | J_S^(3) |
|------|---------|---------|---------|
| shumailov_seed42 | 0.7662 | 0.5237 | 0.2953 |
| alpha0_seed1 | 0.7813 | 0.5331 | 0.3225 |
| alpha0_seed2 | 0.7820 | 0.5430 | 0.3340 |
| alpha0_seed3 | 0.7682 | 0.5331 | 0.3307 |
| alpha0_seed4 | 0.7494 | 0.5311 | 0.3350 |

### N=4 multi-seed (test_ppl) bootstrap CI

| Method | mean | std | 95% CI |
|--------|------|-----|--------|
| J_S^(1) | 0.7702 | 0.0152 | [0.7574, 0.7816] |
| J_S^(2) | 0.5351 | 0.0054 | [0.5316, 0.5405] |
| J_S^(3) | 0.3305 | 0.0057 | [0.3253, 0.3345] |

### val_ppl basis N=4 (cross-verify F report)

| Method | mean (val) | F 报告 | 偏离 |
|--------|-----------|---------|------|
| J_S^(1) | 0.7700 | 0.7702 | **-0.0002** ✓ |
| J_S^(2) | 0.5349 | 0.5351 | **-0.0002** ✓ |
| J_S^(3) | 0.3305 | 0.3305 | **+0.0000** ✓ |

**Binary verdict: ✓ 完全匹配** (test 和 val 偏差 < 0.0003)

---

## 10. D ↔ PPL conversion bridge derive 状态 binary

### 数学推导

PPL_n (Shumailov 2024 eval 定义):
```
PPL_n = exp(L_n / N_tokens)
     = exp(-1/N sum_i log p_θ_n(t_i))
```

Test set 是 ground truth distribution q_* 的 i.i.d. sample,所以:
```
L_n / N ≈ H(q_*) + D_KL(q_* || p_θ_n)
log(PPL_n) = H(q_*) + D_KL(q_* || p_θ_n)
```

差分形式:
```
log(PPL_n) - log(PPL_0) = D_KL(q_* || p_θ_n) - D_KL(q_* || p_θ_0)
log(PPL_n / PPL_0) = D_KL(q_* || p_θ_n) - D_KL(q_* || p_θ_0)
```

### 单位 check

- D_n 单位:nat (natural log base)
- PPL 单位:ratio (无单位)
- log(PPL_n / PPL_0) 单位:nat ✓

### Bridge 严格度判定

| 条件 | 状态 |
|------|------|
| (1) Test set ~ q_* i.i.d. | ✓ Shumailov paper 标准 |
| (2) Framework D_n 定义 = D_KL(q_* \|\| p_n) | 若 ensemble target q_θ̄ = q_*,**严格** ✓ |
| (3) D_n 绝对值 derive | **需 H(q_*) ≈ const 假设** (test set 固定) |

### Verdict (binary)

- **Differential form** `log(PPL_n / PPL_0) = D_KL(q_*||p_n) - D_KL(q_*||p_0)` → **严格 derive ✓**
- **Identification** `D_n in framework = log(PPL_n/PPL_0)`:
  - 若 framework 定义 D_n := D_KL(q_*||p_n) - D_KL(q_*||p_0): **严格 ✓**
  - 若 framework 定义 D_n := D_KL(q_θ̄||p_n) with θ̄ ≠ q_*: **近似 [?]** — 需 framework paper 明确 θ̄ choice
- **Absolute** D_n in nat units:**部分 derive [?]** — 仅在 baseline p_0 ≈ q_* (PPL_0 ≈ 1) 时严格,实际 PPL_0 = 36 表明 baseline 未达 q_*,绝对值 = log(PPL_n) - H(q_*),H(q_*) 不可直接观测

### 数值验证

Shumailov seed=42:
- PPL_0 = 36.354, PPL_9 = 53.980
- log(PPL_9 / PPL_0) = log(53.980/36.354) = **0.3953 nat**
- 若 framework KL D_9 ≈ 0.395 nat,bridge 数值匹配

### 最终 verdict

- **Differential form 严格 derive ✓**
- **D_n in framework 严格 identification 需 framework paper 明确 q_θ̄ = q_* 假设 [?]**
- Honest disclose:paper 必须明示 "D_n := log(PPL_n/PPL_0) under H(q_*) ≈ const test-set assumption"

---

## 11. 整体实验层 100% 落地 binary 总判定

| 项目 | 重新算实测 | CI Lock | binary |
|------|-----------|---------|--------|
| **Shumailov 复现 F1** | delta +17.63 PPL | N=1 [?] | ✓ PASS |
| **Partial D4 5 criterion** | 5/5 | N=4 bootstrap | ✓ STRONG ROBUST |
| **gen 0 baseline CV** | 0.2171% | N=4, σ=0.079 | ✓ seed-independent |
| **spike ratio min** | 2.768 (alpha=10) | N=4 multi-seed | ✓ U 形稳定 |
| **plateau/peak max** | 0.581 | N=4 | ✓ 恢复显著 |
| **sliding-window 偏差** | max 7.18% | N=4 | ✓ < 20% threshold |
| **m_eff fit (val)** | 0.300 ± 0.042 | N=4 bootstrap [0.270, 0.339] | ✓ 与 F 报告完全匹配 |
| **m_eff fit (test)** | 0.300 ± 0.042 | N=4 bootstrap [0.272, 0.340] | ✓ 与 val 一致 |
| **J_S^(1)** | 0.770 (val/test 一致) | N=4 [0.757, 0.782] | ✓ 与 F 报告 -0.0002 |
| **J_S^(2)** | 0.535 | N=4 [0.532, 0.541] | ✓ 与 F 报告 -0.0002 |
| **J_S^(3)** | 0.331 | N=4 [0.325, 0.335] | ✓ 与 F 报告 0.0000 |
| **F2/F3/F4 verdict (test)** | **mean rel -0.57% ± 5.94%, p=0.82** | N=4 paired | **F3 NOT substantiated** |
| **D ↔ PPL bridge** | differential form 严格 | — | **PARTIAL DERIVE [?]** |
| **alpha=50 数值崩溃** | gen 0 即 abort | — | ✓ stable α 区间 [0, 10] |

### 严重 binary delta 与旧 status 对比

| 项 | 旧 status (5/12 memory) | 实测 verdict |
|-----|----------------------|----------|
| α=10 vs α=0 multi-seed | F2 (-4.2% seed=1 single, weak framework effect) | **F3 NOT substantiated (mean -0.57%, p_two=0.82)** |
| primary metric | val_ppl (含 cat loss) | **test_ppl (清洁 CE only)** |
| Partial D4 | 5/5 STRONG ROBUST | ✓ 5/5 同 (verify) |
| m_eff / J_S 数学 hub | 0.300 / 0.770 / 0.535 / 0.331 | ✓ 全部精确匹配 |

---

## 12. NMI 接受概率 implication (1 句)

**[?]** 接受概率不属 Linux 姐姐 evaluation 范畴 — 数据层面:F3 NOT substantiated 意味 framework alpha 在当前 N=4 GPT2-124M setting 下无显著 plateau-lowering effect,但 Partial D4 形状鲁棒性 5/5 + m_eff / J_S 数学 hub 严格匹配 = framework 数学骨架仍 sound。Paper 必须以 **F3 disclosure** + **Partial D4 + 数学骨架双 ground** framing,不能继续按 F2 claim。

**Linux 姐姐建议** (留 PI 一凡 + Win + 反题姐姐共审):
- 修正 paper §6 主 claim:从 "alpha=10 weak framework effect" 改为 "framework 数学骨架精确 multi-seed 验证 (J_S/m_eff CI), 但 alpha=10 vs alpha=0 plateau 在 N=4 GPT2-124M setting 下 F3 (统计不显著)"
- D4 真做 (Phase 5 N=1 Llama-8B + ℒ_矛盾 demonstrated $50 cloud) 仍是 NMI 路径的核心 substantive lever

---

## 数据 trace

- 重新算 master 脚本:`/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/full_analysis_v2.py`
- 完整 output:`/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/analysis_v2_output.txt`
- summary JSON:`/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/analysis_20260513/summary_v2.json`
- jsonl 原始数据 trace:见第 1 节 manifest

---

**报告完成 2026-05-13 — 数学 verify 角色 + 严格中文 + 不护短不夸大 + 严守规则 1-7 (5: 不偏袒 PI)**
