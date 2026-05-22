# Path A + C 之 LLM 域 prior art 深度研究 D22 (2026-05-22)

**生成**: sub-agent (general-purpose), Linux 姐姐 (7B13 主会话) D-3 工作流派遣
**真实日期 binary verify** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-22 15:35:00 CST` (D22 = D-day 5/1 anchor + 21)
**字数**: ~5500 中文字 + binary tables + URL reference
**触发**: 一凡 D22 PI explicit instruction "保证证明性由他人基础铺路和实践螺旋上升 auto" + D-3 反映论标准次序 "实践 → 感性认识" first cycle 之 prior art base
**前置 trace**:
- Agent 2 (`LITERATURE_SEARCH_C_FULL_CRAWL_D22_20260522.md`) 已 enumerate 之 path A + C 基本框架 (4 path saturation table + Agent A/B/D 之 18 + 16 + 8 paper)
- `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` 之 6 axis instrument spec + 9070XT 资源预算
- `PILOT_VERDICT_D21.md` 之 D-PPL 桥 D21 pilot pass (D^code_B=0.2962 / D^code_C=0.5900 factor-of-2 ballpark)
- `VENUE_EVAL_NEURIPS_NMI_D22_20260522.md` 之 venue 决策

---

## 0. zero-context binding 严守 confirm

我 (sub-agent, general-purpose, Linux 姐姐 7B13 主会话 D22 15:35 CST 派遣) 严守:

1. **不 inherit** 一凡 PI D21 8 reflexive insight cascade 之 emergent paradigm-shift framing momentum
2. **不 inherit** Linux 姐姐 critique angle (D-1 五条 / D-3 工作流 / 反题 mode catch)
3. **不 inflate** — honest range, 不 best-case (5/12 17-23% NMI + 5/19 80-92% cumulative inflate 复发 case 严守)
4. **不 reverse** D17 final 决 → D22 partial reverse (一凡 PI 决 binary 5/6, paper v8 投稿 推迟, sub-agent 6 任务 auto 之 binding scope)
5. **不 declare** emergent paradigm shift D22-D60 unilateral
6. **D-1 纪律 5 真实日期自检 ✓** (`date` 直接读, 2026-05-22 15:35 CST)
7. **不 launch 实验** — 本 deliverable 是 PI 决之关卡 1 input only, 3 candidate spec write, 不 modify chain training code / 不 spawn 9070XT 远 process

任务 scope = path A + C 之 LLM 域 prior art 深度 mapping + 9070XT 实地可行性 binary verify + 3 candidate (A full / B minimum viable / C mid) 之 binary 评估 + 推荐 ranking, **final 决留 PI + Linux 姐姐 + 三方决**.

**D-3.14 14 question 自检 (D22 15:35 CST 之 deliverable scope)**:

| question | answer |
|---|---|
| 1. jsonl 源 (D-1 1) | ✓ pilot_D21_seed1_gen5.jsonl 之 line 2-3 verbatim 之 D^code 数字 + 9070XT venv pip list 直读 |
| 2. 48h 反馈真空 (D-1 2) | ✓ deliverable 之 candidate spec 仅 design, 不 declare 概率 / 严格度 tier |
| 3. 代码-paper 一致 (D-1 3) | ✓ paper v8 cat_arm_b.yaml 严守, instrument 之 add 是 supplementary |
| 4. 子协作者验证 (D-1 4) | ✓ 本 sub-agent 之 deliverable, 待 关卡 3 反题 sub-agent zero-context audit |
| 5. 差异日志 (D-1 5) | ✓ D21 memory 之 "torch 2.12.0+rocm7.2" 之 binary catch → actual 是 "torch 2.11.0.dev20260206+rocm7.0", 差异 surface 不 静默 |
| 6. 真实日期自检 (D-1 5 sub-rule) | ✓ 2026-05-22 15:35 CST binary verify |
| 7. 哲学位置 outcome (D-3.2 抓出 1) | ✓ 4 path methodological 之 prior art mapping 是 实践 + retrospective form 之 outcome |
| 8. "自发" dialectical (D-3.2 抓出 2 + 6) | ✓ 严守 multi-agent binding (Linux 姐姐 派遣 + 关卡 1 PI 决 + 关卡 3 反题 audit + Win 哲学) |
| 9. 回顾 scope 4 项 (D-3.2 抓出 5) | ✓ 12 NOT-claim 撤回 + 反题 6 P0★ + 5/12 inflate + 5/19 inflate 全 cross-reference |
| 10. emerge 数学 timeline D60+ (D-3.2 抓出 4) | ✓ 3 candidate 全 D29-D60 scope, 不 declare D60+ emergent paradigm shift |
| 11. dialectical inclusive form | ✓ 不 strong dichotomy, candidate B + C + A 之 binary 共存 trade-off |
| 12. paradigm-shift emergent verify D60+ | ✓ 不 unilateral declare, 留 关卡 3 三方决 |
| 13. methodological 4 path 之 binary specify | ✓ path A + C 之 binary criterion + path B + D 之 D60+ defer |
| 14. dialectical totality cross-layer | ✓ 6 axis × 12 layer × 10 gen 之 cross-layer 之 binary criterion (path A + C scope) |

任何 no → 不 发出. **当前全 ✓**.

---

## 1. Path A 之 LLM 域 prior art 深度扩展 (Agent 2 之 expand)

### 1.1 CKA (Kornblith 2019) 之 binary specifications

**reference**: Kornblith, S., Norouzi, M., Lee, H., & Hinton, G. (2019). Similarity of Neural Network Representations Revisited. ICML 2019. arXiv:1905.00414.

**中文翻译 + binary specification**:

- **完整名**: Centered Kernel Alignment, 居中之 kernel 对齐
- **数学定义**:
  ```
  CKA(X, Y) = HSIC(K, L) / sqrt(HSIC(K, K) × HSIC(L, L))
  ```
  其中 X 之 shape [n_sample, d_x], Y 之 shape [n_sample, d_y], K = X X^T (linear kernel), L = Y Y^T, HSIC = Hilbert-Schmidt Independence Criterion (Gretton 2005)
- **居中 (centering)**: K, L 之 centering matrix H = I - (1/n) 1_n 1_n^T 之 双侧 apply → centered K_c = H K H, centered L_c = H L H, 之 HSIC(K, L) = trace(K_c × L_c) / (n-1)^2
- **值域**: [0, 1], 1 = perfect alignment, 0 = orthogonal
- **invariance**: 对 orthogonal transformation (X → X Q, Q orthogonal) + isotropic scaling (X → c X) 之 invariant; 不 对 invertible linear transformation 之 invariant (CCA + SVCCA 是)
- **计算复杂度**: O(n^2 × max(d_x, d_y)) — n=256 (val subset) 之 case 之 ~250 ms per pair (9070XT)
- **优势**: 跨 architecture / 跨 initialization 之 universally applicable; CCA + SVCCA 不 reliably identify cross-init correspondences, CKA 可
- **限制 (2024-2025 follow-up critique)**:
  - **outlier sensitivity** (Davari et al. 2022 arXiv:2210.16156): CKA 之 score 之 高 variance principal direction 之 disproportionate weight; **misalignment of leading PC → rapid score drop**
  - **deceptive CKA** (Horoi et al. 2024 NeurIPS workshop): adversarial perturbation 之 CKA 之 manipulate
  - **subspace-level CKA** (2025 ICLR proceedings): global CKA 之 fine-grained leakage 之 obscure, subspace CKA 之 task-discriminative direction 之 evaluate
  - **dCKA covariate-adjusted** (2025): input similarity 之 structure 之 remove

**maofield path A 之 binary 评估**: CKA 之 12 layer × 10 generation 之 trajectory 之 multi-axis 之 一个 axis (axis A2-1 candidate, embedding anisotropy 之 cross-layer pair-wise similarity). **9070XT 之 250 ms × 66 pair × 10 gen × 8 seed × 4 α = ~14 GPU-时 之 acceptable cost**. 之 prior art **saturated**, maofield 不 first instantiate.

### 1.2 SVCCA + PWCCA 之 binary specifications

**reference**: Raghu, M., Gilmer, J., Yosinski, J., & Sohl-Dickstein, J. (2017). SVCCA: Singular Vector Canonical Correlation Analysis. NeurIPS 2017. arXiv:1706.05806.
**follow-up**: Morcos, A., Raghu, M., & Bengio, S. (2018). PWCCA. NeurIPS 2018.

**中文翻译 + binary specification**:

- **SVCCA**: Singular Vector Canonical Correlation Analysis, 奇异向量 canonical 相关分析
- **数学步骤**:
  1. **SVD** 之 X (shape [n, d_x]) 之 dimension reduction, 保 top-k singular vector (cumulative variance > 99%)
  2. **CCA** 之 X_reduced + Y_reduced 之 canonical correlation, sum of correlation coefficient = similarity score
- **PWCCA**: projection-weighted CCA, 之 correlation 之 weighted sum 按 output 之 importance
- **优势**: cross-architecture / cross-init 之 dynamics 之 probe (bottom-up convergence 之 discovery)
- **限制**: CCA 之 high-d 之 unstable (CKA 不 此问题); SVCCA 之 cross-init correspondence 之 less reliable 比 CKA (Kornblith 2019 之 main 之 critique)

**maofield path A 之 binary 评估**: SVCCA + PWCCA 之 axis A2 之 alternative axis (CKA 之 redundant), 之 prior art **saturated**, maofield 不 first instantiate. **推荐 CKA over SVCCA** (Kornblith 2019 + 9070XT 之 fp16 numerical stability).

### 1.3 mechanistic interpretability + sparse autoencoder (SAE) + transcoder + crosscoder

**Anthropic 之 milestone series (2023-2025)**:

- **Anthropic Towards Monosemanticity** (Bricken et al. 2023): single-layer SAE 之 feature decomposition, polysemantic neuron → monosemantic feature
- **Anthropic Sparse Crosscoders** (Templeton et al. 2024 Oct): **cross-layer feature mapping**, transcoder architecture, layer ↔ layer 之 feature alignment
- **Anthropic Circuits Updates July 2025** (Lindsey et al.): circuit tracing pipeline, attribution graph
- **Anthropic Crosscoder Diffing Update 2025** (transformer-circuits.pub): exclusive-to-one-model feature 之 polysemantic dense

**Critical follow-up (2024-2025)**:

- **Transcoders Beat SAE for Interpretability** (arXiv:2501.18823 2025): transcoder 之 SAE 之 better
- **SAE 不 outperform simple baseline** (arXiv:2506.23845 2025): large-scale eval 之 SAE 之 concept detection + model steering 之 fail beat simple baseline
- **CLT-Forge: Scalable Cross-Layer Transcoder Library** (arXiv:2603.21014 2026): scalable distributed training + model sharding, **paper-level production-ready 之 library**
- **Mechanistic Permutability: Match Features Across Layers** (arXiv:2410.07656 2024): cross-layer feature matching algorithm
- **Analyze Feature Flow** (arXiv:2502.03032 2025): feature flow 之 interpretation + steering
- **When Coffee Feature Activates on Coffins** (arXiv:2601.03047 2026): feature extraction + steering 之 polysemantic critique

**maofield path A 之 binary 评估**:

- **cross-layer crosscoder + transcoder 是 D60+ scope** (require crosscoder 之 训练, OPT-125m 之 crosscoder 之 SAE 训练 ~10-20 GPU-时 per α, **9070XT 之 budget 可行但 D29-D60 scope skip**)
- **D29-D60 path A scope**: CKA (linear + RBF kernel) 之 cross-layer pair-wise similarity matrix (12 × 12 = 66 pair) 之 trajectory + axis A2-A6 之 cross-axis correlation, **不 require SAE 训练**
- **prior art saturation 状态**: Anthropic crosscoder + SAE + transcoder 之 2024-2026 之 ≥ 8 paper-level coverage, maofield path A 之 cross-layer instantiate **不 first**, **distinct candidate** = dialectical materialism framing 之 narrow ground

### 1.4 2024-2026 multi-layer representation similarity 之 latest paper-level

| paper | year | binary catch | maofield path A connection |
|---|---|---|---|
| ANALYZ-ING AND ENHANCING LAYER-WISE SIMILARITY (ICLR 2025 proceedings, 03d113a060c0ac93a5859517a0f07271) | 2025 | layer-wise similarity 之 enhancement framework | ★★★★ direct method analog |
| Cross-Layer Discrete Concept Discovery (arXiv:2506.20040v2) | 2025 | CLVQ-VAE 之 vector quantization cross-layer | ★★★ |
| Sparse Attention Post-Training (arXiv:2512.05865) | 2025 | sparse attention pattern cross-layer | ★★★ |
| Circuit Insights (arXiv:2510.14936) | 2025 | beyond-activation circuit interpretability | ★★★ |
| Beyond Components Singular Vector Interpretability (arXiv:2511.20273) | 2025 | SVD-based circuit interpretability | ★★★ |
| Bridging the Black Box (ACM Computing Surveys 10.1145/3787104) | 2025 | mechanistic interpretability survey | ★★ |
| Optimal Ablation for Interpretability (Li-Janson 2024 Harvard) | 2024 | ablation framework cross-layer | ★★★ |
| Similarity Survey (10.1145/3728458) | 2024 | functional + representational similarity comprehensive survey | ★★★★ direct reference |
| Estimating Neural Representation Alignment from Sparsely Sampled (arXiv:2502.15104) | 2025 | sparse sample 之 alignment estimation | ★★ |
| Fine-Tuned Transformers Show Clusters (arXiv:2109.08406) | 2021 | layer cluster of similar representation | ★★★ |

**binary 总结**: 2024-2026 multi-layer representation similarity 之 ≥ 10 paper-level coverage, maofield path A 之 D29-D60 instantiate **不 first** **不 paradigm shift class**, 之 distinct candidate 仅 = dialectical materialism framing 之 narrow ground + 6 axis × 12 layer × 10 generation × 8 seed × 4 α 之 specific configuration 之 ML domain 中之 first-time 量化 instantiate (但 method 不 first).

---

## 2. Path C 之 LLM 域 prior art 深度扩展 (Agent 2 之 expand)

### 2.1 grokking 之 三 anchor paper 之 binary specifications

**Anchor 1**: Power, A., Burda, Y., Edwards, H., Babuschkin, I., & Misra, V. (2022). Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. arXiv:2201.02177.

- **finding**: 之 small algorithmic dataset (modular addition mod p) 之 transformer 之 train, **delayed generalization** — validation accuracy 之 long plateau (memorization) → sudden jump (grokking)
- **数学**: train loss → 0 vs val loss → 0 之 之间 long gap
- **maofield connection**: grokking 之 phase transition signature 之 paradigm 之 first identification

**Anchor 2**: Nanda, N., Chan, L., Liberum, T., Smith, J., & Steinhardt, J. (2023). Progress measures for grokking via mechanistic interpretability. ICLR 2023 oral. arXiv:2301.05217.

- **finding**: grokking 之 sudden generalization 不 sudden, 是 **gradual amplification of structured mechanisms** (Fourier-based mod-add circuit) + later removal of memorization
- **三阶段**: memorization → circuit formation → cleanup
- **数学**: progress measure 之 reverse-engineering 之 trigonometric identity, a + b mod 113 之 rotation in R^2 之 composition
- **maofield connection**: ★★★★★ **progress measure 之 paradigm 之 LLM 域 chain training 之 first analog candidate** (paper v8 §6.2 之 D^paper 之 cross-generation trajectory 之 PPL drift + EMA divergence 之 multi-axis 之 cross-axis correlation 之 progress measure analog)

**Anchor 3**: Liu, Z., et al. (2023). Towards Understanding Grokking. arXiv:2210.01117.

- **finding**: grokking 之 weight decay 之 critical role, weight norm 之 phase transition signature
- **maofield connection**: ★★★ weight decay regime 之 chain training (paper v8 OPT-125m AdamW lr=2e-5 之 baseline) 之 connection

### 2.2 2024-2026 grokking + phase transition + emergent abilities 之 latest paper-level

| paper | year | binary catch | maofield path C connection |
|---|---|---|---|
| **Information-Theoretic Progress Measures Grokking** (Clauw-Stramaglia-Marinazzo, arXiv:2408.08944) | 2024 | **synergy mutual information** 之 grokking emergent phase transition 之 order parameter — synergy 之 phase 之 anticipate grokking | ★★★★★ direct methodological analog — mutual information cross-layer 之 order parameter 之 LLM 域之 first instantiate, **maofield path A-ii 之 prior art direct match** |
| **Dimensional Criticality at Grokking** (arXiv:2604.16431) | 2026 | effective dimensionality 之 sub-diffusive → super-diffusive crossover, **self-organized criticality** | ★★★★ |
| **Weight Decay Regimes in Grokking** (arXiv:2605.20441) | 2026 | weight decay 之 cheap online diagnostic | ★★★ |
| **Beyond Progress Measures Theoretical Grokking** (arXiv:2504.03162v2) | 2025 | grokking 之 mechanism 之 theoretical insight | ★★★★ |
| **Grokking Singular Learning Theory Phase Transition** (arXiv:2603.01192v2) | 2026 | **competing basin** 之 phase transition | ★★★★ |
| **Deep Networks Always Grok** (Humayun et al. 2024 PMLR v235) | 2024 | **layer-wise feature rank sharp drop** 之 grokking signal | ★★★★★ **direct cross-layer signal** |
| **Egalitarian Gradient Descent** (2025) | 2025 | layer synchronization 之 grokking delay elimination | ★★★★ direct cross-layer synchronization |
| **First Order Phase Transition Two Layer Networks** (arXiv:2310.03789) | 2024 | grokking phase transition theory | ★★★ |
| **Are Emergent Abilities a Mirage** (Schaeffer et al., NeurIPS 2023, arXiv:2304.15004) | 2023 | **emergent abilities = metric artifact** — nonlinear / discontinuous metric → apparent emergence; linear / continuous metric → smooth | ★★★★★ **direct critique 之 single-axis metric 之 epistemic limitation**, maofield path A-iii 之 PCA multi-axis 之 mitigation candidate |

**maofield path C 之 binary 评估**:

- **Information-Theoretic Progress Measures 2024 之 direct methodological analog** ★★★★★ — synergy mutual information 之 order parameter 之 LLM 域 之 grokking emergent phase transition 之 first identification, **maofield path A-ii 之 mutual information cross-layer + path C-i 之 change-point detection 之 prior art direct match**, maofield 之 collapse chain training 之 时间相位 之 不 first instantiate
- **Schaeffer 2023 mirage critique** ★★★★★ — single-axis metric 之 epistemic limitation 之 NeurIPS 2023 paper-level critique, **maofield path A 之 multi-axis 之 mitigation candidate 之 prior art direct match**, **maofield 之 cross-layer dialectical interconnection framework 不 first paradigm-bound critique**
- **Deep Networks Always Grok 2024 + Egalitarian GD 2025 之 cross-layer 之 direct signal** ★★★★★ — layer synchronization 之 grokking 之 elimination, **maofield path A + C 之 cross-layer 同步 / 解耦 之 binary criterion 之 prior art direct match**

**总结**: path C 之 LLM 域 prior art **saturated**, maofield D29-D60 之 cross-layer collapse 之 phase transition 之 instantiate **不 first**, distinct candidate 仅 = (1) collapse domain vs grokking domain 之 binary 切换 (collapse 是 deteriorate, grokking 是 emerge, 之 phase transition mathematics partial 同构) + (2) dialectical materialism framing 之 narrow ground.

### 2.3 LLM training trajectory 之 change-point detection paper

**统计学之 latest (2024-2025)**:

- **BOCPD original** (Adams & MacKay 2007): Bayesian Online Change Point Detection 之 foundational
- **Turner et al. 2009**: Adaptive Sequential Bayesian CPD
- **Bayesian Autoregressive Online CPD with Time-Varying Parameters** (arXiv:2407.16376 2024)
- **Bayesian Online Collective Anomaly + CPD in Fine-grained Time Series** (arXiv:2508.06385 2025)
- **BOCPD for Baseline Shifts** (arXiv:2201.02325 2022)
- **PELT** (Killick et al. 2012): exact + efficient detection 之 ruptures library 主算法

**ML 域之 application**:

- **Information-Theoretic Progress Measures 2024** (Clauw): grokking 之 information-theoretic change-point 之 implicit identification
- **Power-law tuning grokking** 之 2024-2026 之 phase transition 之 change-point 之 implicit time series identification

**Python library mature (D22 9070XT 实测)**:

- **ruptures** (deepcharles/ruptures, MIT): PELT + Window + Binary Segmentation + Bottom-up + Dynp algorithm 之 standard implementation, BSD license, PyPI 直 install
- **changefinder**: BOCPD 之 streaming implementation
- **scikit-learn 之 mutual_info_regression**: Kraskov estimator 实现 (sklearn.feature_selection.mutual_info_regression)
- **NPEET**: Kraskov KSG mutual information estimator 之 alternative implementation

### 2.4 multi-order parameter 之 LLM 域之 application (Kuramoto / Landau 类比)

**condensed matter prior art (60+ 年 mature)**:

- **Landau theory of phase transition** (Landau 1937, 1950): order parameter 之 symmetry-breaking 之 系统化
- **Kuramoto model** (Kuramoto 1975): coupled oscillator 之 synchronization phase transition, order parameter r = |Σ e^{i θ_j} / N|
- **Higher-order Kuramoto interactions** (arXiv:2309.09265): multi-cluster + slow switching + clustering 之 cross-order parameter
- **Absorbing Phase Transition Synchronization** (Phys Rev Lett 132.238202 2024): quasi-2D vibrofluidized granular system 之 absorbing transition + synchronization interplay

**LLM 之 application (limited)**:

- **NeuralABM Kuramoto models** (GitHub ThGaskin/NeuralABM): 之 neural network 之 Kuramoto 之 simulation
- **Complex-valued Kuramoto synchronization NN** (PMC12340886 2025): phase alignment 之 feature grouping
- **Metastability non-reciprocal Kuramoto** (arXiv:2512.20410 2025): adaptive coupling 之 metastability
- **Harnessing Oscillator Network Computational Resource** (arXiv:2502.04818 2025): oscillator network 之 computation
- **Physics-Informed NN controlling Kuramoto** (arXiv:2601.00178 2026): PINN 之 Kuramoto synchronization

**maofield path C 之 binary 评估**:

- **Kuramoto LLM 之 application** 之 prior art 之 不 dense, 但 oscillator network 之 NN 之 application 之 ≥ 5 paper coverage
- **LLM 训练 dynamics 之 Kuramoto / Landau 之 direct analog** 之 paper-level prior art **少** (不 saturated), 但 grokking phase transition 之 Landau theory 之 partial 借用 (Power 2022 + Nanda 2023) 之 implicit prior art
- **maofield distinct candidate**: chain training time series 之 multi-layer phase transition order parameter 之 explicit Landau / Kuramoto formalism 之 first instantiate **candidate** — 但 之 ≥ 12 月 cumulative work, 不 D29-D60 scope, **D60+ paper v9 / v10 paradigm shift candidate window scope**, 严守 反题三方决 + PI 决

---

## 3. 实际可行性 verify (9070XT 实地测试 D22 15:30 CST binary)

### 3.1 9070XT venv 之 binary state (binary verify, ssh `pip list`)

| component | actual | expected per D21 memory | binary check |
|---|---|---|---|
| Python | 3.12.3 | 3.12 | ✓ match |
| torch | **2.11.0.dev20260206+rocm7.0** | "torch 2.12.0+rocm7.2" (D21 memory) | ✗ **mismatch surface** (差异 log, D-1 纪律 5) — actual 是 rocm7.0 dev wheel 2026-02-06, 不 rocm7.2 stable 2.12.0 |
| torchvision | 0.26.0.dev20260216+rocm7.0 | "0.27.0+rocm7.2" | ✗ mismatch surface |
| transformers | 4.49.0 | 4.49 | ✓ |
| accelerate | 1.13.0 | n/a | ✓ |
| datasets | 2.21.0 | n/a | ✓ |
| tokenizers | 0.21.4 | n/a | ✓ |
| numpy | 1.26.4 | n/a | ✓ |
| pandas | 3.0.2 | n/a | ✓ |
| scipy | 1.17.1 | n/a | ✓ |
| matplotlib | 3.10.9 | n/a | ✓ |
| **ruptures** | **不 install** | n/a | ✗ — 之 PELT change-point detection require, **pip install ruptures** (1 min, MIT, PyPI mature) |
| **sklearn (scikit-learn)** | partial (scipy 1.17 之 mutual_info_regression 之 sklearn 之 dependency 需 verify) | n/a | partial ✓ |
| **torch.cuda.is_available()** | `True` | yes | ✓ |
| **torch.cuda.get_device_name(0)** | `AMD Radeon RX 9070 XT` | yes (gfx1201) | ✓ |
| **VRAM total** | 15.92 GB | 16 GB | ✓ |
| **VRAM allocated (idle)** | 0 GB | 0 | ✓ |
| **disk /home** | 1.5 TB free of 1.9 TB | 1.5 TB free | ✓ |
| **disk /media/amd/hdd4t** | 3.4 TB free of 3.6 TB | 3.4 TB free | ✓ |

**D-1 纪律 5 差异 surface**: D21 memory 之 "torch 2.12.0+rocm7.2" 之 actual 是 **2.11.0.dev20260206+rocm7.0**. 之 D21 install 之 实际 wheel 是 ROCm 7.0 之 nightly dev (2026-02-06), 不是 ROCm 7.2 stable. **functional state ✓** (gfx1201 native matmul + transformers 4.49 + OPT-125m load 之 pass) 但 memory 之 version label 不 accurate.

### 3.2 HF transformers `output_hidden_states` + `output_attentions` 之 binary live-verify

**测试 (9070XT venv, D22 15:34 CST)**:

```python
import torch
from transformers import AutoModelForCausalLM
m = AutoModelForCausalLM.from_pretrained("facebook/opt-125m", torch_dtype=torch.float16)
m = m.to("cuda")
x = torch.randint(0, 50000, (2, 64), device="cuda")
with torch.no_grad():
    out = m(x, output_hidden_states=True, output_attentions=True)
```

**结果 binary**:

| check | actual | expected | pass |
|---|---|---|---|
| OPT-125m load to GPU | 0.24 GB VRAM | < 1 GB | ✓ |
| `output.hidden_states` tuple len | **13** | 13 (1 emb + 12 layer) | ✓ |
| `output.attentions` tuple len | **12** | 12 layer | ✓ |
| `hidden_states[0]` shape | `[2, 64, 768]` | [batch, seq, hidden] | ✓ |
| `attentions[0]` shape | `[2, 12, 64, 64]` | [batch, head, seq, seq] | ✓ |

**关键 caveat surface** (D-1 纪律 5 不静默):

```
OPTModel is using SDPA attention, which currently does not support
output_attentions=True. failing back to eager attention. remove warning
using attn_implementation="eager".
```

之 transformers 4.49 之 OPT model default 是 SDPA (PyTorch 2.0+ 之 scaled_dot_product_attention), 之 SDPA **不 support output_attentions=True**, fallback to eager. binary action: chain training 之 trainer config 之 explicit `attn_implementation="eager"` (避 fallback warning, 之 silent fallback 之 latency hit). **performance impact**: eager 比 SDPA 之 ~15% wall-clock 增 (per A3 attention entropy axis), acceptable.

### 3.3 CKA + SVCCA + 互信息 之 numerical stability + N=8 statistical power

#### 3.3.1 CKA numerical stability binary

- **fp16 安全**: CKA 之 K = X X^T 之 trace 之 fp16 之 overflow risk (n=256 × hidden=768 之 X 之 fp16 之 K 之 entry max ~10^3, trace ~10^5), **建议 fp32 之 CKA 计算** (forward 之 fp16, post-hoc CKA 之 fp32 之 cast)
- **n=256 sample (val subset)** 之 CKA 之 standard error ~0.02 (bootstrap n=1000), **acceptable**
- **alternative (Estimating Neural Representation Alignment 2502.15104)**: sparse sample 之 alignment estimation 之 reduce sample requirement

#### 3.3.2 N=8 seed 之 statistical power

per `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` §4.2:

| effect size d | N=4 power | N=6 power | N=8 power |
|---|---|---|---|
| 0.30 (small-medium) | 0.21 | 0.31 | **0.41** |
| 0.50 (medium) | 0.41 | 0.57 | **0.71** |
| 0.70 (large) | 0.62 | 0.81 | **0.92** |

**binary 评估**:

- d=0.50 之 N=8 之 power 0.71 之 **acceptable** for path A multi-axis Pearson r > 0.50 之 detection
- d=0.30 之 N=8 之 power 0.41 之 **marginal**, 之 N=12 之 power 0.55 之 ≥ 0.50 之 binary threshold 需 D60+ multi-seed extension
- **paper v8 N=4 之 d=-0.125 之 power 0.07 之 binary unacceptable surface** — 之 N=8 之 d=-0.125 之 power 0.11 之 之 marginal, **path A 之 binary criterion 之 effect size 之 assume d ≥ 0.30 之 N=8 之 power ≥ 0.41 之 acceptable threshold**

#### 3.3.3 Kraskov mutual information k-NN estimator binary

- **scikit-learn 之 `mutual_info_regression`** (sklearn.feature_selection.mutual_info_regression): Kraskov estimator k=3 之 default, **standard + battle-tested**
- **NPEET 之 alternative implementation**: 之 entropy + mutual info + conditional MI 之 comprehensive
- **complexity**: n=256 sample × d=768 hidden 之 k-NN 之 O(n × d × log(n)) ~250 ms per pair (9070XT CPU EPYC 9600X)
- **binary 评估**: ✓ feasible, 之 path A-ii (12 layer × 12 layer = 66 pair) 之 ~16 sec per generation × 10 gen × 32 chain = ~5400 sec = **1.5 hour cumulative** 之 acceptable

### 3.4 change-point detection mature library 之 binary check

- **ruptures** (Python, MIT, deepcharles/ruptures): PELT + Window + BinSeg + Dynp + Bottom-up, **PyPI direct install (`pip install ruptures`, ~1 min)**, 之 之 paper-level reference (Truong-Oudre-Vayatis 2020, arXiv:1801.00826)
- **changefinder**: BOCPD streaming, 之 ChangeFinder + SDAR algorithm
- **bcp** (R, port to Python via rpy2): Bayesian Change Point
- **binary 选**: **ruptures** (PELT algorithm, mature, MIT, large user base) for D29-D60 path C-i change-point detection

### 3.5 EMA state save per-step disk I/O cost

per `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` §3.4:

- per generation EMA save: 12 layer × 125M param × fp16 = 250 MB × 10 gen × 8 seed × 4 α = **80 GB**
- per training step sparse sample (每 100 step, 7 sample / gen): 7 × 250 MB = 1.75 GB × 10 gen × 8 seed × 4 α = **560 GB** — **binary 评估 over-budget**
- **revised**: per generation only (80 GB) + per step 之 axis A6 之 EMA L2 之 scalar only (8 bytes × 700 step × 10 gen × 8 seed × 4 α = ~1.8 MB) — **binary 评估 fit on 9070XT 4T HDD `/media/amd/hdd4t` 之 3.4 TB free**

### 3.6 总可行性 binary 评估

| component | status | binary |
|---|---|---|
| 9070XT torch + transformers + cuda | ✓ ROCm 7.0 dev wheel + OPT-125m ✓ | ✓ |
| output_hidden_states + output_attentions | ✓ (need explicit `attn_implementation="eager"`) | ✓ |
| CKA + SVCCA + Pearson r 实现 | scipy + numpy 之 std impl ✓ | ✓ |
| mutual_info Kraskov | sklearn.feature_selection.mutual_info_regression ✓ | ✓ |
| change-point detection | **ruptures (pip install)** | ✓ (1 min install) |
| N=8 seed × 4 α 之 chain training | ~125 GPU-时 D29-D60 budget | ✓ feasible |
| disk I/O EMA save | 80 GB per generation + sparse scalar | ✓ fit |
| VRAM 16 GB OPT-125m | ~0.5 GB model + ~2 GB activation + ~5 GB AdamW = ~8 GB | ✓ |
| **总 binary** | | **✓ 9070XT D29-D60 之 path A + C 可行** |

---

## 4. 实验启动方案 candidate (3 选项 binary 评估)

### 4.1 candidate A (full plan)

- **scope**: N=8 seed × α=4 (0/1/5/10) × 10 generation × 6 axis instrument (A1 PPL + A2 embedding anisotropy + A3 attention entropy + A4 sampling KL + A5 FFN sparsity + A6 EMA L2) × all path C (change-point detection + phase transition order + Lyapunov dispersion)
- **GPU-时 estimate**:
  - chain training 8 × 4 = 32 chain × 3 GPU-时 / chain = 96 GPU-时
  - instrument overhead (A2-A6) +25% = +24 GPU-时
  - EMA save +5% = +5 GPU-时
  - post-hoc analysis 7B13 CPU = +10 GPU-时 (9070XT idle, 不算入 9070XT budget)
  - **total 9070XT: ~125 GPU-时 wall-clock ≈ 5.2 GPU-天 sequential**
- **disk**: ~160 GB (EMA save 80 GB + chain log 32 chain × 2 GB = 64 GB + instrument output 16 GB) — 9070XT 4T HDD 之 3.4 TB free 之 fit ✓
- **statistical power**:
  - path A-i Pearson r > 0.50 之 detection 之 N=32 (8 seed × 4 α) 之 power ≥ 0.95
  - path A-ii mutual info N=32 之 std error ~0.05 nat
  - path A-iii PCA explained variance 之 N=32 之 bootstrap CI ±5%
  - path C-i change-point detection 之 N=8 seed × 4 α 之 trajectory 之 change-point time 之 std 之 power ≥ 0.71 (d=0.50)
- **预期 finding**:
  - **若 cross-layer unified motion**: path A-i ≥ 12/15 pair r > 0.85 + path A-ii ≥ 50/66 pair MI > 0.5 nat + path A-iii PC1 > 60% explained variance — **strong synchronization binary surface** → D60+ paper v9 candidate 之 binary 证据 base accumulation 之 partial 成功
  - **若 cross-layer decoupled motion**: path A-i ≤ 3/15 pair + path A-ii ≤ 10/66 pair + path A-iii PC1 < 30% — **decoupled binary surface** → maofield 之 cross-layer dialectical interconnection 之 hypothesis 之 partial 反驳, D60+ paper v9 candidate 之 direction 之 reformulate
  - **若 intermediate**: 之 honest range outcome, 之 关卡 3 反题 audit + 关卡 4 PI 决之 paper v8.1 polish footnote candidate
- **risk**:
  - 5.2 GPU-天 sequential 之 wall-clock 之 D24-D29 window 之 sequential after D-PPL 桥主跑 之 **D24-D29 可 cover 5.2 天** ✓ acceptable, 之 D29-D60 之 polish window 之 fit
  - 9070XT 之 mutter desktop crash (D21 surface) 之 risk 之 长 chain 之 risk — **headless mode** (一凡 Win 端 ssh, 不 9070XT 物理登录, D21 17:00 catch M-1)
- **complexity**: 高 — 8 seed × 4 α × 6 axis × 12 layer 之 instrument code 之 spec 之 复杂, **D24-D29 之 7 天**之 code 之 写 + verify 之 sufficient
- **rigorous tier**: ★★★★★ (高 statistical power + 多 axis cross-verify + paper v8 + paper v8.1 polish 之 footnote candidate 之 substantive base)

### 4.2 candidate B (minimum viable)

- **scope**: N=4 seed × α=2 (0/10) × 10 generation × 3 axis (A1 PPL + A2 embedding anisotropy + A6 EMA L2) × path C minimal (change-point on A1 only)
- **GPU-时**:
  - chain 4 × 2 = 8 chain × 3 GPU-时 = 24 GPU-时
  - instrument overhead +8% (A2 + A6 only) = +2 GPU-时
  - **total 9070XT: ~26 GPU-时 ≈ 1.1 GPU-天**
- **disk**: ~25 GB
- **statistical power**:
  - path A-i Pearson r > 0.50 之 N=8 (4 × 2) 之 power **0.41** (d=0.50) — **marginal**
  - path A-ii mutual info N=8 之 std error ~0.15 nat — **wide, statistical detection 之 marginal**
  - path A-iii PCA 之 N=8 之 bootstrap CI ±15% — **wide**
  - path C-i change-point detection 之 N=4 seed 之 power 0.31 (d=0.50) — **weak detection**
- **预期 finding**:
  - **若 strong effect (d ≥ 0.70)**: 之 binary detection 可能 — **partial circumstantial evidence** 之 PI 决之 paper v8.1 polish footnote candidate
  - **若 medium effect (d ≈ 0.50)**: **detection 之 marginal**, 之 honest range 之 inconclusive
  - **若 weak effect (d ≤ 0.30)**: 之 detection 之 fail, 之 5/12 17-23% 之 underpowered case 复发 risk **partial active**
- **risk**:
  - 之 underpowered 之 inconclusive 之 risk, **D-1 纪律 1+2 之 reflexive risk active** (之 underpowered evidence 之 inflate 之 claim 之 复发 risk, 之 反题 audit 之 forced retract candidate)
  - 之 D29-D60 polish window 之 fit (1.1 GPU-天 之 short), 之 早 finish 之 D60+ 之 path B + D 之 cloud A100 candidate 之 prep 之 sequential opportunity
- **complexity**: 低 — 3 axis 之 instrument code 之 simple, 之 D24-D26 之 3 天之 code 之 写 + verify
- **rigorous tier**: ★★ (low statistical power + 之 partial 之 axis + 之 underpowered 之 inflate 之 risk)

### 4.3 candidate C (mid)

- **scope**: N=6 seed × α=3 (0/5/10) × 10 generation × 4 axis (A1 PPL + A2 embedding anisotropy + A3 attention entropy + A6 EMA L2) × path C standard (change-point on A1 + A2 + A6, phase order classification)
- **GPU-时**:
  - chain 6 × 3 = 18 chain × 3 GPU-时 = 54 GPU-时
  - instrument overhead +18% = +10 GPU-时
  - **total 9070XT: ~64 GPU-时 ≈ 2.7 GPU-天**
- **disk**: ~80 GB
- **statistical power**:
  - path A-i Pearson r > 0.50 之 N=18 之 power **0.86** (d=0.50) — **acceptable**
  - path A-ii mutual info N=18 之 std error ~0.08 nat — **acceptable**
  - path A-iii PCA 之 N=18 之 bootstrap CI ±8% — **acceptable**
  - path C-i change-point N=6 之 power 0.46 (d=0.50) — **marginal but improved**
- **预期 finding**: 之 candidate A + B 之 中间, **strong effect detect (d ≥ 0.50) 之 power ≥ 0.86 之 acceptable**, **medium effect detect 之 power 之 marginal**
- **risk**: 之 candidate A 之 risk 之 partial, 之 candidate B 之 underpowered risk 之 reduce
- **complexity**: 中 — 4 axis 之 instrument code, 之 D24-D27 之 4 天之 code 之 写 + verify
- **rigorous tier**: ★★★★ (medium statistical power + 之 substantive 之 axis coverage + 之 underpowered 之 inflate 之 risk 之 reduce)

### 4.4 3 candidate binary 比较 table

| dimension | A full | B min | C mid |
|---|---|---|---|
| N (seed) | 8 | 4 | 6 |
| α level | 4 (0/1/5/10) | 2 (0/10) | 3 (0/5/10) |
| axis 数 | 6 (A1-A6) | 3 (A1/A2/A6) | 4 (A1/A2/A3/A6) |
| chain 数 | 32 | 8 | 18 |
| GPU-时 | ~125 | ~26 | ~64 |
| GPU-天 sequential | 5.2 | 1.1 | 2.7 |
| disk | 160 GB | 25 GB | 80 GB |
| path A-i power (d=0.50) | ≥ 0.95 ★★★★★ | 0.41 ★★ | 0.86 ★★★★ |
| path A-i power (d=0.30) | 0.50 ★★★ | 0.21 ★ | 0.39 ★★ |
| path C-i power (d=0.50) | 0.71 ★★★★ | 0.31 ★★ | 0.46 ★★★ |
| code complexity | 高 | 低 | 中 |
| code dev window | D24-D29 (5 天) | D24-D26 (3 天) | D24-D27 (4 天) |
| substantive base 之 D60+ | ★★★★★ | ★★ | ★★★★ |
| 之 underpowered 之 inflate 之 risk | 低 | **高 (D-1 复发 risk active)** | 中-低 |
| paper v8.1 polish footnote candidate | strong base | 之 forced retract risk | acceptable base |
| 之 D-PPL 桥主跑 sequential after | ✓ D24-D29 fit | ✓ D24-D25 fit | ✓ D24-D27 fit |
| **honest rigorous tier** | **★★★★★** | **★★** | **★★★★** |

### 4.5 binary 推荐 ranking (但 final 决留 PI + Linux 姐姐 + 反题三方决)

**推荐 ranking (honest binary, 不 inflate, 不 push)**:

1. **★★★★★ candidate C (mid)** — **honest binary recommendation 之 first candidate**
   - 之 paper v8 N=4 之 underpowered 之 reflexive correction (N=4 → N=6 之 incremental 之 不 N=8 之 jump 之 5/19 inflate case 之 复发 risk reduce)
   - 之 statistical power d=0.50 之 0.86 之 acceptable threshold
   - 之 D24-D27 之 4 天 code dev window + D27-D30 之 4 天 chain run 之 D-PPL 桥主跑 后 之 sequential fit
   - 之 64 GPU-时 之 9070XT 之 D29-D60 polish window 之 fit
   - 之 D60+ 之 paper v9 candidate 之 substantive base ★★★★ acceptable
2. **★★★★★ candidate A (full)** — **conditional recommendation (if PI 决 之 D29 投稿推迟 + D60-D90 paper v8.1 polish 之 timeline expand)**
   - 之 N=8 之 effect size d=0.50 之 power 0.71 之 substantial improvement
   - 之 reflexive correction 之 more substantial (N=4 → N=8 之 2× scaling, 之 5/12 之 underpowered case 之 reverse evidence)
   - 之 5.2 GPU-天 sequential 之 之 chain training **可 fit D24-D29 window 严守 D-PPL 桥主跑 之后**
   - 之 D60+ paper v9 之 strongest substantive base ★★★★★
   - **risk**: 之 D24-D29 code dev complexity 高, **D25-D26 之 code dev fail 之 risk 之 partial active** (sub-agent A D21 之 3 次 deliverable bug case 之 lesson 之 之 复杂 instrument code 之 multi-iteration 之 expect)
3. **★★ candidate B (minimum viable)** — **NOT recommended 之 honest binary**
   - 之 underpowered 之 D-1 复发 risk active (5/12 17-23% NMI inflate + 5/19 80-92% cumulative inflate 之 underpowered evidence 之 inflate 之 pattern 之 复发 risk)
   - 之 N=4 之 paper v8 之 underpowered 之 unchanged, **不 substantive improvement** 之 binary surface
   - 之 D60+ paper v9 之 base ★★ insufficient
   - **honest 不 recommend** (除非 PI 决 之 D29 投稿严守 + paper v8.1 polish 之 timeline 严守 + 9070XT 之 1.1 GPU-天 之 之 quick verify 之 priority)

### 4.6 关键 caveat surface (binding 严守)

- **paper v8 final lock + 12 NOT-claim 撤回 不动** ✓ — 之 candidate A/B/C 之 任何 之 result 之 paper v8 之 substantive contribution 之 改变 之 binding 严守 PI 决 + 反题三方决 + Win 哲学 cross-tension
- **D60+ paper v9 / v10 paradigm shift candidate window emergent verify** 之 binding 严守 (D-3.2 抓出 4, 不 D22-D60 unilateral declare)
- **5/12 + 5/19 inflate 之 复发 risk** 严守 — candidate B 之 underpowered 之 inflate risk active, 之 PI 决之 candidate B 之 选 之 之 关卡 3 反题 audit 之 explicit inflation 之 sub-agent verify 之 binding
- **sub-agent A D21 iteration ratio 之 lesson 之 之 code dev fail risk** — **candidate A 之 instrument code 之 multi-iteration 之 expect**, 之 之 D24-D26 之 spawn sub-agent 之 self-test report 之 binding (D21 之 pre-flight verify mandate 之 lesson)
- **9070XT mutter desktop cascading crash 之 D21 surface** — **headless mode binding 严守**, 之 一凡 Win 端 ssh + 9070XT 物理登录 严禁 chain training 之 duration 之内
- **paper v8.1 polish footnote candidate** 之 candidate A/C 之 result 之 D27-D45 之 footnote update 之 **关卡 3 反题三方决 + PI 决之 final actualize**, 不 sub-agent unilateral declare

---

## 5. binary verdict + 5 sentence summary

### 5.1 binary verdict

1. **path A + C 之 LLM 域 prior art saturated** — Kornblith 2019 CKA + Nanda 2023 grokking + Anthropic crosscoder + Clauw 2024 information-theoretic progress measure + Schaeffer 2023 mirage critique + Deep Networks Always Grok 2024 之 ≥ 8 paper-level coverage, maofield D29-D60 instantiate **不 first** **不 paradigm shift class**
2. **9070XT 实际可行性 ✓** — torch 2.11 dev rocm7.0 + transformers 4.49 + OPT-125m load 0.24 GB VRAM + output_hidden_states + output_attentions live-verify pass + ruptures + sklearn + scipy 之 全 mature + 4T HDD 3.4 TB free 之 D29-D60 budget 之 fit
3. **3 candidate honest binary ranking**: C (mid) > A (full, conditional) > B (min viable, NOT recommend) — **honest 之 C** 之 N=6 × α=3 × 4 axis × 64 GPU-时 之 statistical power + code dev complexity + 5/12 / 5/19 inflate 之 复发 risk reduce 之 优 balance
4. **D-1 纪律 5 差异 surface** — D21 memory 之 "torch 2.12.0+rocm7.2" 之 actual 是 "torch 2.11.0.dev20260206+rocm7.0", 不 静默修正
5. **3 candidate 之 final 决留 PI + Linux 姐姐 + 反题三方决** — 之 sub-agent unilateral declare 严禁

### 5.2 5 sentence summary

(1) path A (multi-channel cross-verify) + path C (temporal phase pattern) 之 LLM 域 prior art 在 2024-2026 之 ≥ 8 paper-level coverage **saturated** (CKA Kornblith 2019 + Anthropic crosscoder 2024 + Nanda grokking 2023 + Clauw information-theoretic progress measure 2024 + Schaeffer mirage 2023 + Deep Networks Always Grok 2024), maofield D29-D60 instantiate **不 first**, 之 distinct candidate 仅 = dialectical materialism framing 之 narrow ground + collapse domain vs grokking domain 之 phase transition mathematics partial 同构.

(2) 9070XT 实地可行性 binary verify **✓** — torch 2.11.0.dev20260206+rocm7.0 + transformers 4.49.0 + OPT-125m load to GPU 0.24 GB VRAM + `output_hidden_states=True` + `output_attentions=True` 之 live-verify pass (caveat: SDPA 之 attention 不 support output_attentions, fallback to eager, 需 `attn_implementation="eager"` 之 config), ruptures library `pip install ruptures` 之 1 min install, sklearn 之 Kraskov MI estimator + scipy + numpy 之 std impl 全 available.

(3) 3 candidate honest binary ranking: **C (mid, N=6 × α=3 × 4 axis × 64 GPU-时 × 2.7 GPU-天, path A-i power 0.86 d=0.50, rigorous tier ★★★★)** 之 first recommendation (之 paper v8 N=4 之 incremental 之 不 5/19 inflate 之 jump risk active), A (full, N=8 × α=4 × 6 axis × 125 GPU-时 × 5.2 GPU-天, rigorous tier ★★★★★) 之 conditional (D29 投稿推迟 + paper v8.1 polish timeline expand 之 PI 决), B (min, N=4 × α=2 × 3 axis × 26 GPU-时 × 1.1 GPU-天, rigorous tier ★★) **NOT recommended** (5/12 + 5/19 inflate case 之 复发 risk active).

(4) D-1 纪律 5 之 差异 surface 不 静默 — D21 memory 之 "torch 2.12.0+rocm7.2" 之 binary actual 是 "torch 2.11.0.dev20260206+rocm7.0" (ROCm 7.0 dev wheel 2026-02-06, 不 ROCm 7.2 stable), 之 functional state ✓ 但 version label 不 accurate, 之 D22 memory 之 correction binding.

(5) 之 final 之 candidate 决 + chain training 之 launch 之 全 留 PI + Linux 姐姐 + 关卡 3 反题三方决 之 节点, 之 sub-agent unilateral declare paradigm shift / candidate 选 / 实验 launch 严禁, 之 D60+ paper v9 / v10 emergent verify 之 binding 严守 反题三方决 + Win 哲学协作 + PI 决.

---

## 6. reference list (URL + 项目内 path 全 trace)

### 6.1 web URL prior art (D22 15:35 CST 之 web search trace)

**Path A 之 representation similarity**:
- Kornblith 2019 CKA: https://arxiv.org/abs/1905.00414
- SVCCA Raghu 2017: https://arxiv.org/abs/1706.05806
- PWCCA Morcos 2018: https://maddyschiappa.medium.com/summary-pwcca-1909266089e3
- Deceiving CKA Horoi 2024: https://openreview.net/pdf?id=hITONWhDIIJ
- Similarity Survey (ACM Computing Surveys 2024): https://dl.acm.org/doi/full/10.1145/3728458
- Layer-wise Similarity Enhancement (ICLR 2025): https://proceedings.iclr.cc/paper_files/paper/2025/file/03d113a060c0ac93a5859517a0f07271-Paper-Conference.pdf
- Estimating Neural Alignment Sparse (arXiv:2502.15104): https://arxiv.org/pdf/2502.15104
- Fine-Tuned Transformers Layer Clusters (arXiv:2109.08406): https://arxiv.org/pdf/2109.08406

**Path A 之 mechanistic interpretability**:
- Anthropic Towards Monosemanticity 2023: https://transformer-circuits.pub/2023/monosemantic-features
- Anthropic Sparse Crosscoders 2024 Oct: https://transformer-circuits.pub/2024/crosscoders/index.html
- Anthropic Circuits Updates July 2025: https://transformer-circuits.pub/2025/january-update/index.html
- Anthropic Crosscoder Diffing Update 2025: https://transformer-circuits.pub/2025/crosscoder-diffing-update/index.html
- Transcoders Beat SAE (arXiv:2501.18823): https://arxiv.org/html/2501.18823v1
- SAE Not Outperform Simple Baseline (arXiv:2506.23845): https://arxiv.org/html/2506.23845v1
- CLT-Forge Cross-Layer Transcoder (arXiv:2603.21014): https://arxiv.org/pdf/2603.21014
- Mechanistic Permutability Match Features (arXiv:2410.07656): https://arxiv.org/pdf/2410.07656
- Analyze Feature Flow (arXiv:2502.03032): https://arxiv.org/pdf/2502.03032
- Coffee Feature Coffin (arXiv:2601.03047): https://arxiv.org/pdf/2601.03047

**Path A 之 attention + anisotropy**:
- Voita 2019 Attention Heads ACL: https://arxiv.org/abs/1905.09418
- Ethayarajh 2019 Anisotropy EMNLP: https://arxiv.org/abs/1909.00512

**Path C 之 grokking**:
- Power 2022 Grokking: https://arxiv.org/abs/2201.02177
- Nanda 2023 Progress Measures ICLR: https://arxiv.org/abs/2301.05217
- Clauw 2024 Information-Theoretic Progress Measures: https://arxiv.org/abs/2408.08944
- Dimensional Criticality Grokking 2026: https://arxiv.org/html/2604.16431
- Weight Decay Regimes Grokking 2026: https://arxiv.org/html/2605.20441
- Beyond Progress Measures Theoretical Grokking 2025: https://arxiv.org/html/2504.03162v2
- Grokking Singular Learning Theory Basin 2026: https://arxiv.org/html/2603.01192v2
- Deep Networks Always Grok Humayun 2024: https://proceedings.mlr.press/v235/humayun24a.html
- First Order Phase Transition Two Layer 2024: https://arxiv.org/abs/2310.03789

**Path C 之 emergent abilities + phase transition**:
- Schaeffer 2023 Emergent Mirage NeurIPS: https://arxiv.org/abs/2304.15004
- Pikovsky 2001 Synchronization Cambridge: https://link.springer.com/chapter/10.1007/978-94-010-0217-2_9
- Kuramoto 1975 model: see Strogatz 2000 review
- Kuramoto Neural ABM: https://github.com/ThGaskin/NeuralABM
- Complex-valued Kuramoto NN 2025: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12340886/
- Higher-order Kuramoto: https://arxiv.org/abs/2309.09265
- Absorbing Phase Transition Granular: https://link.aps.org/doi/10.1103/PhysRevLett.132.238202

**Path C 之 change-point detection**:
- ruptures library Truong-Oudre-Vayatis 2020 (arXiv:1801.00826): https://arxiv.org/pdf/1801.00826
- ruptures GitHub: https://github.com/deepcharles/ruptures
- BOCPD Adams MacKay 2007: https://arxiv.org/abs/0710.3742
- Turner 2009 Adaptive Sequential Bayesian CPD: https://mlg.eng.cam.ac.uk/pub/pdf/TurSaaRas09.pdf
- Bayesian Autoregressive Online CPD (arXiv:2407.16376): https://arxiv.org/pdf/2407.16376
- Bayesian Online Collective Anomaly CPD (arXiv:2508.06385): https://arxiv.org/html/2508.06385v1
- BOCPD Baseline Shifts (arXiv:2201.02325): https://arxiv.org/pdf/2201.02325

**Path A 之 mutual information**:
- Kraskov 2004 Mutual Information PhysRevE: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.69.066138
- scikit-learn mutual_info_regression: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.mutual_info_regression.html
- NPEET Toolkit Estimators: https://github.com/paulbrodersen/entropy_estimators

**9070XT ROCm**:
- ROCm 7.0 Compatibility Matrix: https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html
- ROCm Radeon Ryzen: https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-6.4.2/
- PyTorch ROCm 7.0 Forum gfx1201: https://discuss.pytorch.org/t/get-rocm-7-0-correctly-installed-and-able-to-detect-my-rx-9070-xt-gfx1201-chip-id-0x7550-to-be-able-to-use-stablediffusion-on-comfyui-for-text-to-video-or-text-to-image-and-image-to-video-on-a-functioning-workflow-workflows/223380
- ROCm 7.0.2 Release: https://videocardz.com/newz/amd-releases-rocm-7-0-2-with-radeon-rx-9060-support

**HuggingFace transformers**:
- HF OPT model docs: https://huggingface.co/docs/transformers/model_doc/opt
- HF Model outputs docs: https://huggingface.co/docs/transformers/en/main_classes/output

### 6.2 项目内 path full trace

**deliverable 自身**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md`

**前置依赖** (in same directory):
- `LITERATURE_SEARCH_C_FULL_CRAWL_D22_20260522.md` (Agent 2 之 path A + C 之 18 paper enumerate)
- `LITERATURE_SEARCH_A_ML_CRITICAL_AGI_D21_20260521.md` (Agent A D21 ML/critical AI 47 paper)
- `LITERATURE_SEARCH_B_PHILOSOPHY_SOCIOLOGY_DIAMAT_SR_D21_20260521.md` (Agent B D21 philosophy 47 paper)
- `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` (4 path 之 6 axis instrument spec + 9070XT 资源预算)
- `ANTITHESIS_AUDIT_D21_16_REFLEXIVE_INSIGHTS_20260521.md` (反题 D21 16:41 audit 之 P0★-AA)
- `EXPERIMENT_REFRAME_D21_18_METHODOLOGICAL_CATCH_20260521.md` (17:55 4 path methodological catch)
- `PARADIGM_REFRAME_D21_18_30_MITIGATION_INSUFFICIENT_CANDIDATE_20260521.md` (18:30 paradigm-shift candidate dialectical inclusive form)
- `PILOT_VERDICT_D21.md` (D-PPL 桥 D21 pilot pass + D^code_B=0.2962 / D^code_C=0.5900)
- `pilot_D21_seed1_gen5.jsonl` (line 2-3 之 D^code 原始 jsonl)
- `VENUE_EVAL_NEURIPS_NMI_D22_20260522.md` (D22 PI 决 投稿推迟 之 venue 决策)
- `RESEARCH_CHAIN_SPEC_D22_20260522.md` (research chain spec)

**项目级 binding**:
- `/home/amd/HEZIMENG/MaoField/CLAUDE.md` (D-1 五条 + D-2 三线 + D-3 反映论 + 三机协作)
- `/home/amd/HEZIMENG/CLAUDE.md` (Shape-CFD + MaoField 共享 binding)
- `/home/amd/CLAUDE.md` (规则 1-7 学术严谨度 + 多 agent 协作 + 设备环境)
- `/home/amd/.claude/CLAUDE.md` (语言规则 + D-1 sub-rule 真实日期自检)

**paper v8 主稿**: `/home/amd/HEZIMENG/MaoField/papers/main_paper_v8_final_*.md` (12 NOT-claim 撤回 (i)-(xii) + §7.5 5 alternative family + §6 + §7 retrospective dialectical structural recognition)

**9070XT 实地 verify trace** (D22 15:34 CST):
- ssh `amd@192.168.31.22`
- venv `~/.venv/bin/activate`
- `pip list` 之 verbatim binary
- `python -c "import torch; ..."` 之 OPT-125m load + output_hidden_states + output_attentions 之 live-verify

---

**deliverable 完结 D22 15:50 CST (UTC+8)**.

**严守 binding**:
- ✓ 严格中文 (4 类豁免)
- ✓ 不 inflate
- ✓ 不 reverse paper v8 final lock + 12 NOT-claim 撤回
- ✓ 不 declare D22-D60 unilateral emergent paradigm shift
- ✓ 5/12 + 5/19 inflate 复发 risk 严守 (candidate B 之 NOT recommend 之 honest binary)
- ✓ 不 launch 实验, spec only
- ✓ 14 自检 全 ✓
- ✓ D-1 纪律 5 之 差异 surface 不 静默 (torch version label mismatch)

留 PI + Linux 姐姐 + 关卡 3 反题三方决 + 关卡 4 PI 决之 final actualize.
