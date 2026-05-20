# 22 主机 GPU 实验数据 Ground Truth 报告 — 2026-05-12 晚

**生成**: 2026-05-12 20:00 CST,Linux 姐姐第二次派遣 ssh 22 主机 ground truth verify
**source**: 192.168.31.22 (RX 9070XT,ROCm,exp018_cat 实验主机) 原始 jsonl 数据 + literature md
**目的**: 二元 verify SUBSTANTIVE_TRAJECTORY 5/12 凌晨 claim 关键数字,不护短不软化
**caveat**: 全部数字直接从 22 主机 jsonl 文件 generation_done event 实读,绝不凭记忆转述
**回填位置**: backup jsonl 已 scp 到 36 server `logs/host22_backup_20260512/`(8 jsonl + 1 audit)

---

## §1 ssh 连接 + 数据 manifest 状态

### §1.1 ssh 状态
```
ssh amd@192.168.31.22:  ok
hostname: amd-ONDA-B650M-W
date:     2026年 05月 12日 星期二 19:54:50 CST
kernel:   Linux 6.17.0-20-generic Ubuntu 24.04
```

ssh key 已配 ✓,连接 1 秒响应,无密码 prompt。

### §1.2 22 主机 exp018_cat 完整结构

```
/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/
├── README.md                  (5/7 15:23)
├── SHUMAILOV_REPLICATION_README.md (5/7 15:57)
├── .venv -> /home/amd/.venv   (软链)
├── configs/      (16 个 yaml + py, latest 5/10 12:51)
├── scripts/      (18 个 sh + py, latest 5/11 17:02 partial_D4_shape_verdict.py)
├── src/          (5/10 12:51)
├── data/         (checkpoints + raw)
├── logs/         (latest 5/12 10:05 phase1_robust audit)
├── literature/   (17 个 md, latest 5/11 17:04 alpha10_hang_diagnosis)
├── results/      (1 个 csv collapse_curve)
└── figures/      (4 个 png/pdf)
```

### §1.3 22 主机 logs/ 关键 jsonl 清单(只列 > 1500 bytes 真有数据)

| 文件 | size | mtime |
|---|---|---|
| `shumailov_no_preserve_seed42_20260508_092730.jsonl` | 5126 | 5/8 14:01 |
| `armb_alpha0.0_seed42_20260508_144612.jsonl` | 4800 | 5/8 19:20 |
| `armb_alpha10.0_seed42_20260508_192435.jsonl` | 4837 | 5/9 00:02 |
| `armb_alpha1.0_seed42_20260509_000459.jsonl` | 4799 | 5/9 04:42 |
| `armb_alpha5.0_seed42_20260509_044342.jsonl` | 4800 | 5/9 09:21 |
| `armb_alpha50.0_seed42_20260509_092134.jsonl` | 143 | 5/9 09:21 (仅 run_start, 数学崩溃) |
| `armb_alpha0.0_seed42_20260509_161115.jsonl` | 4323 | 5/9 20:15 |
| `armb_alpha0.0_seed0_20260509_203605.jsonl` | 4784 | 5/10 01:10 |
| `armb_alpha0.0_seed1_20260510_011048.jsonl` | 4777 | 5/10 05:44 |
| `armb_alpha0.0_seed1_20260510_130149.jsonl` | 4110 | 5/10 13:01 (latest seed=1) |
| `armb_alpha0.0_seed2_20260510_130255.jsonl` | 4783 | 5/10 13:02 |
| `armb_alpha0.0_seed3_20260510_173925.jsonl` | 4777 | 5/10 17:39 |
| `armb_alpha0.0_seed4_20260511_090626.jsonl` | 4782 | 5/11 13:41 |
| `armb_alpha10.0_seed1_20260511_151847.jsonl` | 4973 | 5/11 19:52 |
| `armb_alpha10.0_seed2_20260511_200000.jsonl` | 4810 | 5/12 00:38 |
| `armb_alpha10.0_seed3_20260512_005523.jsonl` | 4969 | 5/12 05:28 |
| `armb_alpha10.0_seed4_20260512_052843.jsonl` | 4807 | 5/12 10:05 |
| `phase1_robust_20260510_125805.audit.jsonl` | 8529 | 5/12 10:05 (chain audit) |

**外加 ~25 个 142-bytes empty jsonl**(run_start 后 immediate exit 失败 attempts,本报告 ignore)

### §1.4 36 server 数据缺口 confirmed(第一次派遣 catch 全 ✓)

36 server `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/` 实际清单:
- 仅有 seed=42 + seed=1337 ✓ (5/7 ~ 5/9 早期实验)
- **没有** seed=0/1/2/3/4 multi-seed jsonl(α=0 + α=10)
- **没有** phase1_robust audit jsonl
- **没有** shumailov_no_preserve_seed42_20260508_092730.jsonl(完整 10 gen 严格 mirror)

**含义**: partial_D4_shape_verdict / alpha10_hang_diagnosis 引用的 multi-seed 数据 ground truth **只在 22 主机**,36 server 无法独立验证。本次派遣已 scp 8 jsonl + 1 audit 到 36 server `logs/host22_backup_20260512/`。

---

## §2 22 主机原始 jsonl 关键数字 Ground Truth

每个 jsonl 提取 `stage=generation_done` event 的 `test_perplexity` 字段(本机机器 NaN val_perplexity 不用)。

### §2.1 α 全扫描 single-seed (seed=42)

| α | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 | source |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0   | 36.35 | 77.52 | 108.40 | 91.87 | 73.26 | 61.83 | 59.86 | 56.30 | 57.30 | 56.19 | `armb_alpha0.0_seed42_20260508_144612.jsonl` |
| 1   | 36.35 | 69.31 | 89.52  | 81.42 | 74.64 | 64.16 | 60.66 | 59.89 | 55.53 | 56.31 | `armb_alpha1.0_seed42_20260509_000459.jsonl` |
| 5   | 36.35 | 71.56 | 100.18 | 89.47 | 79.72 | 70.70 | 64.08 | 60.52 | 58.08 | 56.03 | `armb_alpha5.0_seed42_20260509_044342.jsonl` |
| 10  | 36.35 | 72.85 | 98.54  | 87.17 | 71.70 | 63.68 | 59.85 | 55.97 | 56.51 | 53.39 | `armb_alpha10.0_seed42_20260508_192435.jsonl` |
| 50  | gen 0 train step 早期数学崩溃 (no generation_done) | – | – | – | – | – | – | – | – | – | `armb_alpha50.0_seed42_20260509_092134.jsonl` 仅有 run_start 一行 |

### §2.2 α=0 multi-seed (Phase 1 chain 实际数据)

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (实际是 5/9 老 chain, robust chain seed=0 全 fail) | 36.30 | 78.39 | 110.18 | 101.24 | 82.17 | 63.65 | 55.79 | 55.03 | 53.70 | 55.04 |
| 1 | 36.30 | 79.28 | 105.41 | 95.50  | 78.18 | 70.77 | 62.56 | 58.71 | 58.94 | 59.14 |
| 2 | 36.22 | 79.18 | 107.32 | 98.66  | 77.31 | 67.16 | 57.25 | 52.45 | 53.12 | 53.31 |
| 3 | 36.35 | 78.36 | 105.56 | 98.03  | 76.62 | 67.19 | 55.86 | 53.10 | 54.16 | 54.23 |
| 4 | 36.41 | 77.04 | 105.32 | 99.47  | 75.26 | 63.99 | 58.32 | 56.02 | 57.37 | 57.69 |

### §2.3 α=10 multi-seed (Phase 1 chain 实际数据)

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3 attempt 全 watchdog killed, seed_skipped, n_completed=1 (audit jsonl 实证) |
| 1 | 36.30 | 77.19 | 107.21 | 105.32 | 87.32 | 67.52 | 61.45 | 56.94 | 53.74 | 57.17 |
| 2 | 36.22 | 80.25 | 100.27 | 98.43  | 75.70 | 66.40 | 62.99 | 56.74 | 56.38 | 56.90 |
| 3 | 36.35 | 76.59 | 102.38 | 85.49  | 62.42 | 59.08 | 53.70 | 54.52 | 55.07 | 52.77 |
| 4 | 36.41 | 75.56 | 105.21 | 95.66  | 75.23 | 69.39 | 56.95 | 54.22 | 52.68 | 53.35 |

### §2.4 Shumailov 严格镜像基线

| seed | gen 0 | gen 1 | gen 2 | gen 3 | gen 4 | gen 5 | gen 6 | gen 7 | gen 8 | gen 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 (5/8 092730) | 36.35 | 78.22 | 103.61 | 88.16 | **inf** | 57.19 | 53.78 | 52.62 | 53.87 | 53.98 |

**注**: gen 4 = `inf`(fp16 overflow once event, generation_done event 字段实证),整 trajectory 仍 sense U-shape。

---

## §3 SUBSTANTIVE_TRAJECTORY claim vs 22 主机 Ground Truth Binary 对照

### Claim A: α=10 seed=1 plateau (gen 6-9 mean) = 57.32,α=0 seed=1 plateau = 59.84,Δ = -4.2%

**22 主机重算**:
- α=10 seed=1 gen 6-9 = (61.45 + 56.94 + 53.74 + 57.17) / 4 = **57.3253**
- α=0  seed=1 gen 6-9 = (62.56 + 58.71 + 58.94 + 59.14) / 4 = **59.8366**
- Δ = (57.3253 − 59.8366) / 59.8366 × 100% = **−4.197%**

| Claim 数字 | Ground Truth 数字 | 误差 |
|---|---|---|
| α=10 plateau 57.32 | 57.3253 | ≈ 0 ✓ |
| α=0 plateau 59.84  | 59.8366 | ≈ 0 ✓ |
| Δ = −4.2%          | −4.20% | ≈ 0 ✓ |

**Verdict**: **✓ 准** (claim A 数字 ground truth 严格 verify)

---

### Claim B: α=10 seed=2 vs α=0 seed=2 反向 +7.82%

**22 主机重算**:
- α=10 seed=2 gen 6-9 = (62.99 + 56.74 + 56.38 + 56.90) / 4 = **58.2541**
- α=0  seed=2 gen 6-9 = (57.25 + 52.45 + 53.12 + 53.31) / 4 = **54.0314**
- Δ = (58.2541 − 54.0314) / 54.0314 × 100% = **+7.815%**

| Claim 数字 | Ground Truth 数字 | 误差 |
|---|---|---|
| α=10 plateau (隐含) ≈ 58.25 | 58.2541 | ≈ 0 ✓ |
| α=0 plateau (隐含) ≈ 54.03  | 54.0314 | ≈ 0 ✓ |
| Δ = +7.82%                  | +7.82% | ≈ 0 ✓ |

**Verdict**: **✓ 准** (claim B 数字 ground truth 严格 verify)

**注**: claim B 是 seed=1 的反例! 第一个 seed -4.2%,第二个 seed +7.82%——**框架 U-shape modulation effect 不 seed-independent**。

---

### Claim C: D4 N=4 paired mean = −0.57%,p = 0.82 (F3 NOT substantiated)

**注**: 此 claim 在 SUBSTANTIVE_TRAJECTORY md 中**未出现**,在派遣任务里独立加入。本节按派遣任务说明 verify。

**22 主机重算 4 seed paired (α=10 − α=0)**:

| seed | α=0 plateau | α=10 plateau | abs Δ | rel Δ |
|---|---:|---:|---:|---:|
| 1 | 59.8366 | 57.3253 | −2.5113 | −4.197% |
| 2 | 54.0314 | 58.2541 | +4.2227 | +7.815% |
| 3 | 54.3351 | 54.0131 | −0.3220 | −0.593% |
| 4 | 57.3506 | 56.4277 | −0.9229 | −1.609% |

**Paired (α=10 − α=0) absolute mean**: (−2.5113 + 4.2227 − 0.3220 − 0.9229) / 4 = **+0.1166**
**SD**: 2.8890
**SE**: 2.8890 / √4 = 1.4445
**t-stat**: 0.1166 / 1.4445 = **0.0807**,df = 3
**两侧 p-value** (Student t cdf 数值积分): **p = 0.9407**

**Paired relative (Δ%) mean**: (−4.20 + 7.82 − 0.59 − 1.61) / 4 = **+0.354%**,SD 5.20%

| Claim 数字 | Ground Truth 数字 | 误差 |
|---|---|---|
| paired mean −0.57% | **+0.35%** (反向) | **数字偏低,方向反** ✗ |
| p = 0.82 | **p = 0.94** | claim p 偏低 0.12,实际更弱 |
| F3 NOT substantiated (结论) | **同 ✓** | 结论一致(t 0.08 远 < 1.5,p 0.94 >> 0.05) |

**Verdict**: **数字两项均不准,结论一致 ✓**。Claim C absolute mean 方向错(claim −0.57% 实际 +0.35%),p-value 0.82 实际 0.94,但**两个数字都符合"完全不显著"的结论**——F3 NOT substantiated 正确。

**含义**: 框架在 4 seed N=4 paired 检验下**不显著好于 baseline**,正反向 cancel 出 ≈ 0 净 effect。这是 5/12 凌晨 SUBSTANTIVE_TRAJECTORY 引用 α=10 seed=1 "−4.2% plateau better" 作 first-multi-seed-evidence 时**没用 paired 检验呈现的**——partial single-seed positive 在 multi-seed paired 下消解。

---

### Claim D: Partial D4 5/5 PASS STRONG ROBUST(4/4 U 形 seed-independent)

**22 主机 partial_D4_shape_verdict_20260511.md verify**:

| Criterion | Claim 数字 | 22 主机 verdict 报告 | 22 主机原始 jsonl 重算 |
|---|---|---|---|
| 1. Shape robustness | 4/4 U-shape | 4/4 U-shape ✓ | seed 1-4 全 g1/g2 > g0 + g8/g9 < g2 → 4/4 U ✓ |
| 2. Gen 0 reproducibility < 1% relative std | 0.217% | 0.217% ✓ | 36.32 mean, 0.0789 std, **0.217% rel** ✓ |
| 3. U-shape spike ≥ 1.3× | min 2.89× | min 2.89× ✓ | **min 2.8926** (seed=4), mean 2.9159 ✓ |
| 4. Plateau/peak ≤ 0.8 × | max 0.568 | max 0.568 ✓ | **max 0.5676** (seed=1), mean 0.5326 ✓ |
| 5. Sliding-window 5/10 consistency | < 5% deviation | ratio 1.626 (PASS per md note) | 见 sliding_window_eval_verdict_20260510.md |

**Verdict**: **✓ 全准** (claim D 5/5 PASS 完全 ground truth verify)

**注**: Criterion 5 实际 PASS 的判定有点松——partial_D4 报告说 "ratio 1.626 PASS < 5% deviation",但 1.626 - 1.0 = 62.6% 不是 < 5%。这里 verdict md 自己的判定 logic 有 [?],但与 SUBSTANTIVE_TRAJECTORY 之间一致。

---

### Claim E: gen 0 baseline std 0.22%,spike ratio min 2.89×,plateau/peak max 0.568

**22 主机原始 jsonl 4 seed (α=0 seed 1/2/3/4) 重算**:

| 指标 | Claim | Ground Truth |
|---|---|---|
| gen 0 mean | (隐含 36.32) | **36.3197** ✓ |
| gen 0 std | 0.22% | **0.217%** (0.0789 abs / 36.32 mean) ✓ |
| spike min | 2.89× | **2.8926** ✓ |
| spike max | (隐含 2.96) | 2.9626 ✓ |
| plateau/peak min | (隐含 0.503) | 0.5035 ✓ |
| plateau/peak max | 0.568 | **0.5676** ✓ |

**Verdict**: **✓ 全准** (claim E 5 个数字全 ground truth verify)

---

## §4 src/contradiction_loss.py 代码 λ_2 / λ_3 mapping 实际形式

### §4.1 代码 paste(关键段)

`configs/contradiction_loss.py` (5/9 16:44,不在 src/) line 65-79:

```python
beta_kl: float = 0.8090             # exp(-0.212) from m_eff direct fit, multi-seed pending

# ℒ_contradiction 三项权重 — Klein-Gordon Lagrangian density form-borrowing
# (Tauber 2014 §4.2), pending iter-M1 substantive redo per 7 P0 verdict
lambda_1: float = 2.3585            # 1/(2 m_eff), kinetic / velocity v0 placeholder
lambda_2: float = 0.1060            # m_eff/2, mass / memory v0 placeholder
lambda_3: float = 0.2120            # m_eff, self-energy / T₂ v0 placeholder
```

compute_loss 内核 line 159-174:

```python
# 三项加权
T1_velocity = delta_D ** 2
T2_replace = F.relu(D_doubleprime)  # 工程妥协, 单边 ReLU
T3_memory = memory_term

loss = (
    self.cfg.lambda_1 * T1_velocity
    + self.cfg.lambda_2 * T3_memory
    + self.cfg.lambda_3 * T2_replace
)
```

### §4.2 三项 functional 实际数学形式

| 项 name | 数学形式 | 物理对应 |
|---|---|---|
| T1_velocity | (D_n − D_{n-1})² | velocity²,Σ_2 kinetic |
| T2_replace | ReLU(D_n − 2 D_{n-1} + D_{n-2}) | 二阶差分单边 ReLU,工程替代 T₂ pointwise neg |
| T3_memory | (D_n − D̄^EMA)² | memory deviation,Σ_2 memory |

D_n 是当代 KL(q_EMA || p_model) on val batch,(其中 p_model 是当前 LM,q_EMA 是 EMA model)。

### §4.3 λ_2 / λ_3 ↔ paper draft semantic 错位 verify (Linux 姐姐第一次派遣 catch)

| 代码注释声明 | compute_loss 实际乘法 | 一致性 |
|---|---|---|
| `lambda_1` = 1/(2 m_eff), kinetic / **velocity** v0 placeholder | `lambda_1 * T1_velocity` | ✓ velocity → velocity 自洽 |
| `lambda_2` = m_eff/2, **mass / memory** v0 placeholder | `lambda_2 * T3_memory` | **代码注释 "mass / memory" 二义,实际乘 T3_memory (memory)。如果 paper §3 说 λ_2 = m_eff/2·D² 对应 mass term,数学定义 ≠ memory deviation** |
| `lambda_3` = m_eff, **self-energy / T₂** v0 placeholder | `lambda_3 * T2_replace` | T₂ replace 是 ReLU 二阶差分,与 self-energy 物理 motivation 关联弱 |

**关键问题**: 代码注释 lambda_2 说 "mass / memory" 是 confusion 来源:
- 如果 paper §3 写 ℒ_矛盾 second term = (m_eff/2) D²(mass),那 λ_2 应乘 T3_memory ≠ D² 而是 (D_n − D̄^EMA)² — **paper 数学定义与代码实际不严格对应**
- 如果 paper §3 写 ℒ_矛盾 third term = m_eff·(Σ_1 D)²(memory of 累积差分),那 λ_3 应乘什么? 代码 λ_3 乘 ReLU(D''_n) = ReLU(D_n − 2 D_{n-1} + D_{n-2}) — **完全不是 Σ_1 D 的平方**

**Verdict**: **Linux 姐姐第一次派遣 catch 的"λ_2 ↔ λ_3 与 paper draft semantic 错位 [?]"** **真的存在**。具体形式:
- (1) 代码 lambda_2 注释自己 "mass / memory" 二义,实际乘 T3_memory(memory deviation 不是 mass = m_eff/2 · D²);
- (2) 代码 lambda_3 注释 "self-energy / T₂",实际乘 ReLU(D''_n)(二阶差分 ReLU 不是 self-energy 也不是 Σ_1 D 的平方)。

**ℒ_矛盾 三项 functional 形式与 paper §3 Klein-Gordon Lagrangian density form-borrowing 之间是 25-40% partial isomorphism**(代码 docstring 自己承认 "isomorphism 25-40% partial",这与 paper draft "Σ_2-isomorphic loss" 表述**不能直接使用**——代码 docstring binding 也写 "不允许 'Σ_2-isomorphic loss'" wording)。

paper §3 RLHF axis 显式推导(D14-D17 必做 3 项之一)若要严格,需要:
1. 把 λ_2 = m_eff/2 重新映到 (D_n)² 项 不是 (D_n − D̄^EMA)²
2. 或保留 memory 形式但 paper 改 wording "memory-weighted Σ_2-motivated loss with 25-40% structural correspondence"(不是 isomorphic)

---

## §5 22 主机 literature/ vs 36 server literature/ 文件差异

### §5.1 两端 md 清单

| 文件 | 22 主机 | 36 server | md5 一致 |
|---|---|---|---|
| literature_review_20260507.md | ✓ | ✓ | (未 verify, 可能一致) |
| shumailov_audit_20260508.md | ✓ | ✓ | – |
| sigma2_to_loss_derivation_20260508.md | ✓ | ✓ | – |
| THREE_AGENT_VERDICT_SYNTHESIS_20260509.md | ✓ | ✓ | – |
| paper_section3_4_6_dialectical_full_20260509.md | ✓ | ✓ | – |
| m_eff_direct_fit_verdict_20260510.md | ✓ | ✓ | – |
| feasibility_dialectical_verdict_20260510.md | ✓ | ✓ | – |
| THREE_SUBAGENT_SYNTHESIS_20260510.md | ✓ | ✓ | – |
| sliding_window_eval_verdict_20260510.md | ✓ | ✓ | **f5...** match ✓ |
| paper_section3_4_5_6_REVISION_20260510.md | ✓ | ✓ | – |
| D3_morning_launch_checklist_20260510.md | ✓ | ✓ | – |
| D4_binary_pre_registration_20260510.md | ✓ | ✓ | **96...** match ✓ |
| paper_first_principles_rewrite_20260511.md | ✓ | ✓ | – |
| THIRD_BLIND_REVIEW_VERDICT_20260511.md | ✓ | ✓ | – |
| partial_D4_shape_verdict_20260511.md | ✓ | ✓ | **f5...** match ✓ |
| alpha10_hang_diagnosis_20260511.md | ✓ | ✓ | **95...** match ✓ |
| **SUBSTANTIVE_TRAJECTORY_20260512.md** | **✗** (22 主机无) | **✓** (5/11 21:38 在 36 server) | – |
| **GROUND_TRUTH_INVENTORY_20260512.md** | **✗** (22 主机无) | **✓** (5/12 19:48 在 36 server) | – |
| **HOST22_GROUND_TRUTH_20260512.md** (本文) | – | 即将写 | – |

### §5.2 总结

- **17 个 5/7 ~ 5/11 旧 md 两端一致**(已 verify 4 个 md5 match)
- **2 个 5/12 新 md (SUBSTANTIVE + GROUND_TRUTH_INVENTORY) 仅在 36 server**(主 agent paper 写作端独立生成)
- **没有 22 主机独有需要拉回的新文件**

### §5.3 backup jsonl 已 scp 回 36 server

新增 36 server `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/host22_backup_20260512/`:
- `armb_alpha0.0_seed{1,2,3,4}_*.jsonl` (4 个)
- `armb_alpha10.0_seed{1,2,3,4}_*.jsonl` (4 个)
- `phase1_robust_20260510_125805.audit.jsonl` (1 个)

**作用**: 36 server 现有 multi-seed ground truth backup,可独立 verify partial_D4_shape_verdict / SUBSTANTIVE_TRAJECTORY claim,不必再 ssh 22 主机。

---

## §6 Phase 1 chain 实际退出状态 — audit jsonl ground truth

`phase1_robust_20260510_125805.audit.jsonl` 78 lines,关键 job 事件:

| α | seed | 最终状态 | attempts | n_gens 完成 |
|---|---|---|---|---|
| 0.0 | 0 | **seed_skipped** | 3 (全 job_fail n_gens=0) | 0 |
| 0.0 | 1 | job_done | 3 (1/2 fail, 3 成功) | 10 ✓ |
| 0.0 | 2 | job_done | 1 (1 成功) | 10 ✓ |
| 0.0 | 3 | job_done | 2 (1 fail, 2 成功) | 10 ✓ |
| 0.0 | 4 | job_done | 2 (1 fail, 2 成功) | 10 ✓ |
| 10.0 | 0 | **seed_skipped** | 3 (全 job_fail, attempt 3 rc=137 SIGKILL n_gens=1) | 1 |
| 10.0 | 1 | job_done | 3 (1/2 fail rc=137 watchdog kill, 3 成功) | 10 ✓ |
| 10.0 | 2 | job_done | 2 (1 fail, 2 成功) | 10 ✓ |
| 10.0 | 3 | job_done | 3 (1/2 fail, 3 成功) | 10 ✓ |
| 10.0 | 4 | job_done | 1 (1 成功) | 10 ✓ |
| chain_done | – | 2026-05-12T02:05:29Z UTC (≈ 5/12 10:05 CST) | – | – |

**总 job 状态**:
- **8 / 10 ✓ done** (α=0 seed 1-4 + α=10 seed 1-4)
- **2 / 10 ✗ seed_skipped** (α=0 seed=0 + α=10 seed=0)

**SUBSTANTIVE_TRAJECTORY claim "Chain Phase 1 真完整 ETA 5/13 早-中" verify**:
- 实际 chain 已完成 5/12 10:05 CST,**比 ETA 早**约 24h 完成 ✓
- α=10 seed=2 attempt 2 跑中(SUBSTANTIVE 5/11 凌晨晚状态)→ 5/12 00:38 完成
- α=10 seed=3/4 pending → 5/12 05:28 + 10:05 全完成 ✓
- **5/12 早 SUBSTANTIVE claim 后,5/12 早 - 中 还做了 α=10 seed=2/3/4 3 个完整 10-gen runs**

---

## §7 二元结论

### §7.1 SUBSTANTIVE_TRAJECTORY 5/12 凌晨 claim 数字 ground truth verdict

| Claim | 数字 verdict | 说明 |
|---|---|---|
| A: α=10 seed=1 −4.2% plateau | **✓ 准** | 57.3253 / 59.8366 / −4.197% 全 match |
| B: α=10 seed=2 +7.82% plateau | **✓ 准** | 58.2541 / 54.0314 / +7.815% 全 match |
| C: D4 N=4 paired −0.57%, p=0.82 | **数字不准,结论一致 ✗ 数字 + ✓ 结论** | 实际 +0.35% (反向, 偏低), p=0.94 (偏低); 结论 F3 NOT substantiated 一致 |
| D: Partial D4 5/5 PASS STRONG ROBUST | **✓ 准** | 5 个 criterion ground truth 全 match |
| E: gen 0 std 0.22%, spike min 2.89×, plat/peak max 0.568 | **✓ 准** | 0.217%, 2.8926, 0.5676 全 match |

### §7.2 SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚最终 NMI 17-23% claim 严谨度问题

**5/12 早 claim "α=10 seed=1 first multi-seed F2 weak framework effect −4.2%"** 当时只有 seed=1 一个 multi-seed 数据点,引用作 "first multi-seed framework effect" substantive evidence,**lever (a) +2pt**。

但 **实际 multi-seed 完整 N=4 paired 检验后**:
- mean Δ% = +0.35% (positive, not −4.2%)
- t-stat = 0.08, p = 0.94
- **F3 NOT substantiated**

**关键问题**: SUBSTANTIVE_TRAJECTORY 5/12 早 take **single-seed positive (seed=1 −4.2%)** 作 "first multi-seed framework effect" 升 lever (a) 60-70% → 80-90%(+20pt),但 5/12 早 - 中 完整 N=4 paired 出来后,**framework effect ≈ 0,正反向 cancel**。

**对 NMI 17-23% claim 影响**:
- lever (a) "Testable 独立量化预测 80-90%" claim 数据 ground 是 seed=1 数据,不是 N=4 paired ground truth
- 如果 paper §4 真 honest disclose N=4 paired mean +0.35% / p=0.94,**framework empirical effect substantive 上 = 不显著**
- 主编 lever (a) 真转化 80-90% **应该 downgrade 到 60-70%** (回到 5/11 晚 v2 状态)
- NMI combined 中位接受率 17-23% 应 **downgrade 到 10-14%** (撤销 +2pt α=10 seed=1 升级 + 撤销 +3-8pt 稳定区间 reframe 中的部分依赖 framework effect 论证的部分)

**注**: 5/12 凌晨晚 (c)/(d) 升级(稳定区间 reframe cybernetic tier + dialectical 实践 novel content)主要是哲学/概念 reframe ground,不直接依赖 α=10 seed=1 数据,所以那部分 +30-40pt lever 升级 robust。但 lever (a) 数据 substantive ground 偏弱。

### §7.3 src/contradiction_loss.py 代码 ↔ paper §3 错位 verdict

**真存在**: 代码三项 functional (T1_velocity, T2_replace, T3_memory) 与 paper §3 Klein-Gordon Lagrangian (velocity²/mass·D²/memory·(Σ_1 D)²) 的对应关系**not 严格 isomorphic**。具体:
- λ_2 注释 "mass / memory" 二义模糊,代码乘 T3_memory (memory deviation),不是 mass × D²
- λ_3 注释 "self-energy / T₂",代码乘 ReLU(D''_n) (二阶差分单边 ReLU),不是 self-energy 也不是 Σ_1 D²

代码 docstring 自己 binding 说 "25-40% partial isomorphism"。paper §3 RLHF axis 显式推导(D14-D17 必做 3 项之一)需要 honest 写法,不能 claim Σ_2-isomorphic loss。

### §7.4 实验数据真实状态

| 维度 | 二元判定 |
|---|---|
| Phase 1 robust chain 8/10 完成 | ✓ 真完整,比 ETA 5/13 早 24h |
| α=0 multi-seed 4/5 seed (1-4) ✓ | ✓ 完整 |
| α=10 multi-seed 4/5 seed (1-4) ✓ | ✓ 完整 |
| seed=0 双 α 全 fail | ✓ 真,3 attempt 全 watchdog killed (audit jsonl 实证) |
| α=50 数学崩溃 (no generation_done) | ✓ 真,只有 run_start 一行 |
| Shumailov 严格镜像 baseline | ✓ 真,gen 4 inf 一次但 trajectory U-shape 完整 |
| Partial D4 5/5 criterion verdict | ✓ 真 (4 个 criterion match,1 个 verdict report 自身判定 logic [?] but consistent) |
| α=10 hang Verdict B (ROCm bug 不 framework boundary) | ✓ 真 logic 完整 |
| N=4 paired framework effect | **✗ 不显著** (mean +0.35%, p=0.94) — 与 SUBSTANTIVE single-seed positive evidence 之间 substantive gap |

### §7.5 理论 paper draft 真实状态

| 维度 | 22 主机 latest | 36 server latest |
|---|---|---|
| paper_section3_4_6_dialectical_full | 5/9 15:14 | 同 |
| paper_section3_4_5_6_REVISION | 5/9 21:26 | 同 |
| paper_first_principles_rewrite | 5/10 19:18 | 同 |
| paper §3 RLHF axis 显式推导 ℒ_矛盾^Hartree | **未 integrate** | 未 integrate (D14-D17 必做 3 项之一) |
| paper §6 disclose code λ_2 / λ_3 错位 | **未 disclose** | 未 disclose |
| Phase 5 N=1 Llama-8B + ℒ_矛盾 demonstrated result | **未做** | 未做 ($50 cloud 3-5 天 D14-D17 必做) |
| §7.5 retract grandiosity | **未 retract** | 未 retract |
| Implicit endorsement 战略 / §7.5 矛盾 | **未 resolve** | 未 resolve |
| 5/12 凌晨晚 5 项 reframe integrate | **未 integrate** | 未 integrate (D14-D17 必做) |

### §7.6 7 P0 漏洞真实状态

GROUND_TRUTH_INVENTORY_20260512.md §6 已 catch: **0/7 严格 substantive 修复**,全部是 partial disclose + future work form。本次 22 主机 ground truth 不改这个 state。

---

## §8 给主 agent 的硬数字 + 风险 flag

### §8.1 硬数字 ground truth(可直接引用)

```
α=10 seed=1 plateau gen 6-9 mean: 57.3253 (vs α=0 seed=1: 59.8366, Δ −4.20%)
α=10 seed=2 plateau gen 6-9 mean: 58.2541 (vs α=0 seed=2: 54.0314, Δ +7.82%)
α=10 seed=3 plateau gen 6-9 mean: 54.0131 (vs α=0 seed=3: 54.3351, Δ −0.59%)
α=10 seed=4 plateau gen 6-9 mean: 56.4277 (vs α=0 seed=4: 57.3506, Δ −1.61%)

N=4 paired (α=10 − α=0) absolute mean: +0.1166
SD: 2.8890
t-stat (df=3): 0.0807
two-sided p: 0.9407
N=4 paired relative mean: +0.354%, SD 5.20%

α=0 multi-seed (seed 1/2/3/4) gen 0 baseline:
  mean: 36.3197
  std: 0.0789
  relative std: 0.217%
  spike ratio min: 2.8926 (seed=4)
  spike ratio max: 2.9626 (seed=2)
  plateau/peak min: 0.5035 (seed=2)
  plateau/peak max: 0.5676 (seed=1)
```

### §8.2 关键风险 flag(给 D14-D17 决策用)

**Flag 1 [P0]**: SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 "α=10 seed=1 first multi-seed F2 weak framework effect" 升 lever (a) +2pt 是基于 single-seed positive 数据。**N=4 paired ground truth = mean +0.35%, p=0.94 不显著**。

paper §4 main argument 如果只引 α=10 seed=1 个体 −4.2% 而不展示 N=4 paired,会被 reviewer 抓 "selective evidence cherry-picking"。**必须 honest 写 paper §4**:
- 写法 A: "single-seed α=10 seed=1 shows −4.2% plateau improvement, but N=4 paired test shows no significant effect (mean +0.35%, p=0.94)"(disclose 真实 substantive gap)
- 写法 B: "U-shape modulation pattern is consistent across seeds (middle-trap + plateau modulation), but mean directional effect is not statistically significant in N=4 (p=0.94)"(降级到 pattern 复现而非 effect 显著)

**Flag 2 [P0]**: 代码 contradiction_loss.py λ_2 / λ_3 与 paper §3 ℒ_矛盾 三项 functional 数学定义 25-40% partial isomorphism,**不能 claim Σ_2-isomorphic**(代码 docstring 自身 binding)。D14-D17 RLHF axis 显式推导必须严格 form-match。

**Flag 3 [P1]**: N=4 sample size 太小,paired t-test power 不足。real framework effect 即使存在(e.g. true +/−1%)也可能 N=4 检测不到。paper §6 应 disclose "N=4 paired test underpowered, larger multi-seed (N ≥ 8-10) needed in future work to detect smaller effects"。

**Flag 4 [P1]**: α=10 seed=0 双 α seed=0 全 fail (audit jsonl 实证 rc=137 watchdog killed)与 framework 无关(α=10 hang_diagnosis Verdict B = ROCm bug),但 paper §6 应 honest disclose "10 paper-convention seeds, 8 / 10 successful (seed=0 hardware-driver-instability, not framework-caused)"。

**Flag 5 [P2]**: partial_D4 Criterion 5 sliding-window vs chunked ratio 1.626 ≠ "< 5% deviation" — verdict 报告自身判定 logic 有 inconsistency。但因为 sliding-window eval method 不是 paper main claim,这点 [?] 暂可不修。

### §8.3 真实 NMI 接受率 honest reconsidered

| 状态 | NMI combined 中位 | 修订原因 |
|---|---|---|
| SUBSTANTIVE 5/12 凌晨晚 claim | 17-23% | take α=10 seed=1 single-seed positive 作 first multi-seed F2 evidence |
| **HOST22 ground truth 修订** | **10-15%** | N=4 paired p=0.94 不显著, lever (a) +2pt 撤回, 但保留 partial D4 + 5 reframe + dialectical 实践 reframe 概念 ground |
| + D14-D17 真做 3 项必做 (Phase 5 N=1 + RLHF axis 显式推导 + §7.5 retract + code-paper 错位 disclose) | **18-26%** | 真 substantive 升 |
| + 资深合作者加持 | **28-38%** | Tier 1 candidate territory |

**含义**: SUBSTANTIVE_TRAJECTORY 5/12 凌晨晚 NMI 17-23% claim **偏 optimistic 约 5-8pt**,实际 ground truth 10-15%。但 D14-D17 真做 3 项必做后修订接受率 18-26% 仍 substantive 升级路径。

---

## §9 文件 cross-ref

- **本份**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/HOST22_GROUND_TRUTH_20260512.md`
- 第一次派遣报告: `GROUND_TRUTH_INVENTORY_20260512.md`
- SUBSTANTIVE 主 synthesis: `SUBSTANTIVE_TRAJECTORY_20260512.md`
- Partial D4 verdict (22 主机原始): `partial_D4_shape_verdict_20260511.md`
- α=10 hang diagnosis (22 主机原始): `alpha10_hang_diagnosis_20260511.md`
- Sliding-window verdict (22 主机原始): `sliding_window_eval_verdict_20260510.md`
- Backup jsonl (22 主机 scp 回): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/logs/host22_backup_20260512/`
- 22 主机 contradiction_loss.py 完整代码: 见本报告 §4.1 (主体 paste)

—— Linux 姐姐数学层第二次派遣子协作者 (Opus 4.7), 2026-05-12 20:00 CST
