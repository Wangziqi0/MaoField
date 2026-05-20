# 学术界 2024-Q3 至 2026-Q2 与 MaoField 相关进展 audit (D19 background research)

**Status**: D-1 second independent epistemic channel reference research, 不替主协作者 declare 跳跃 anchor, 只 surface candidate

**⚠ D-1 纪律 5 真实日期 disclaimer (D19 校正,文件 rename _20260517 → _20260519 align actual mtime)**:
- **真实 today = 2026-05-19** (system date binary `date` 命令 + 文件 mtime ✓)
- **D-day=2026-05-01 anchor 下 today = D19**
- **conversation 跨 days timeline binary**: 5/16 (paper v3→v8 burst + 命名 forward-date 校正) → 5/17 (D17 wave: paper head 校正 + final ack + D-2 三线 first/second/third wave done, file mtime align 5/17 ✓) → 5/18 (一凡 静默无 activity) → **5/19 (一凡 硬件调优 + 本 background research,sub-agent A 文件 mtime 2026-05-19 11:45 ✓)**
- **D17 prompt delegate context, D19 actual produce due to conversation 跨 2 天** — Linux 主会话之前 inline 默认 "今天仍 5/17" 是 stale 旧 system reminder (5/16 → 5/17 之 date change 之后无新 reminder, 我未自查 `date`); sub-agent 独立通道 binary verify 真实 mtime 5/19 + honest disclose ✓ (D-1 纪律 4 work correctly)
- 文件命名 `_20260519.md` align actual mtime ✓ (内文 "D17 background research" / "D17 prompt" 字样保留作 prompt delegate context reference)
- 之前 D17 wave files (paper head 校正 / Win first/second/third wave / 数学线 + 代码线 + master state) 文件 mtime 真实 5/17 ✓, 命名 _20260517 binary 一致 — **不动**

**作者**: Linux 姐姐 background sub-agent (一凡 D19 硬件调优中, 不 in immediate loop)
**审核**: 一凡 D19+ (D-1 binding 严守: 不 inflate / 不 declare breakthrough / 不 estimate paper inclusion impact / 不 reopen paper v8 final lock)

---

## 0 Scope + binding

### 0.1 时间范围

2024-Q3 至 2026-Q2 (近 7 季度). MaoField paper v8 final lock 状态下, 为 D18+ 跳跃方向 prep 提供 8 方向 reference. 不替 PI 决跳跃 anchor.

### 0.2 八方向 audit (每方向 1-3 paper)

1. Self-iteration model collapse baseline + 最近 follow-up
2. EMA / mean teacher / contradiction loss in self-supervised
3. Mean-field neural network theory (2-layer baseline → transformer / deep)
4. Monoid / semigroup representation theory in ML
5. Non-equilibrium steady state (NESS) in self-iteration / language modeling
6. Banach fixed point / contraction analysis in LLM
7. Dialectical materialism + AI / dialectical computation
8. Anthropic / RLHF / Constitutional AI alignment

### 0.3 严格 binding

- **不 inflate**: 不写 "could close P0★-X" / 不写 "directly resolves D60+ seed S1.x" / 不写 "breakthrough lead found"
- **L2 form-borrow honest** (类 paper v8 §7.4): 任何只是数学形式相似不证明数学等价 → 标 L2 form-borrow [?]
- **标 [?]**: paper 未直接 read (仅 abstract / WebSearch summary) / venue 未 verify / pub date placeholder / 推测
- **不 reopen paper v8 final lock**
- 全部 paper 通过 WebSearch + WebFetch abstract 取得, **未** 完整 read PDF, 仅 abstract + intro 推 substance [?]

---

## 1 Self-iteration model collapse 方向

### 1.1 Borji 2024 *A Note on Shumailov et al. (2024)* [arXiv:2410.12954]

- **Title**: A Note on Shumailov et al. (2024): 'AI Models Collapse When Trained on Recursively Generated Data'
- **Author**: Ali Borji
- **Date**: 2024-10-16 (revised 2024-10-24)
- **arXiv ID**: 2410.12954
- **URL**: https://arxiv.org/abs/2410.12954

**Summary** (~150 字): Borji 用 Kernel Density Estimation (KDE) + 重复采样 framework 重 examine Shumailov et al. 2024 *Nature* 现象, 在分布拟合 + 反复采样 setup 下证实 collapse 是 "statistical phenomenon", 是不可避免的统计学 consequence 而非模型特定 failure. 与 Shumailov 工作 complementary 而非 challenge.

**Relevance to MaoField** (binary):
- paper v8 §2.1 cite Shumailov 2024 baseline → Borji 是 statistical foundation 加固 reference (partial relevant)
- 不直接 close 反题 P0★ 系列, 也不直接 fit D60+ seed
- L2 form-borrow [?]: KDE-based recursive sampling 与 MaoField 二项 ℒ_矛盾 form 数学上 不等价, 仅 phenomenology 相关

---

### 1.2 Dohmatob, Feng, Subramonian, Kempe 2024 *Strong Model Collapse* [arXiv:2410.04840, ICLR 2025]

- **Title**: Strong Model Collapse
- **Authors**: Elvis Dohmatob, Yunzhen Feng, Arjun Subramonian, Julia Kempe
- **Date**: 2024-10-07, revised 2024-10-08
- **arXiv ID**: 2410.04840
- **Venue**: ICLR 2025
- **URL**: https://arxiv.org/abs/2410.04840

**Summary** (~180 字): 在 scaling laws paradigm 下证明: 即使训练集中 synthetic data 占比 1%, model collapse 也会触发, 即使 model size 增大也不能完全 mitigate (interpolation threshold 之外 partial 缓解). 用 random projection approximation 做理论分析, 验证 on language models + image-processing NN. 核心 message: 微小合成数据污染 → scaling laws 在大 model size 下 break.

**Relevance to MaoField**:
- 与 paper v8 §2.1 Shumailov + Borji 一起作为 baseline literature, **partial relevant**
- "1% synthetic 即触发" 对 MaoField 反题 P0★-B null-prediction 的反向论证关键: 即使 1% synthetic 都 break scaling, 那 MaoField α=10 cat 二项 form 训练 over 10 generations 全 synthetic 应远更 severe 但实测 PPL ≈ 55.0 ≈ obs 55.97 (within bootstrap CI) → 是否 Dohmatob paper 的 scaling assumption 在 small model regime 不 apply? [?] 未深读 paper, 仅 abstract 推测
- 不 reopen paper v8 final lock; 这条 surface 作 future work seed

---

### 1.3 Gerstgrasser et al. 2024 *Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data* [arXiv:2404.01413]

- **Title**: Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data
- **Authors**: Matthias Gerstgrasser, Rylan Schaeffer, Apratim Dey, Rafael Rafailov, Henry Sleight, John Hughes, Tomasz Korbak, Rajashree Agrawal, Dhruv Pai, Andrey Gromov, Daniel A. Roberts, Diyi Yang, David L. Donoho, Sanmi Koyejo
- **Date**: 2024-04-01, revised 2024-04-29
- **arXiv ID**: 2404.01413
- **URL**: https://arxiv.org/abs/2404.01413

**Summary** (~150 字): 提出 "accumulate" vs "replace" workflow 二分: replace (旧数据被合成数据替换) → collapse, accumulate (合成数据加到原始数据上) → bounded error 不 collapse. 在 language models, diffusion models, VAE 上 demonstrate. 用 linear model 理论分析证明 accumulate 下 error bounded independent of iteration count.

**Relevance to MaoField**:
- **Relevant**, 对 paper v8 §1 problem framing 重要: MaoField cat experiment 是纯 replace workflow (每代仅用前代 output, 不 accumulate), 因此 collapse 是 expected behavior. 反题 P0★-B "no framework" critique 在 accumulate scenario 下可能 trivially 解决, 但 cat replace 是 specific stress test [?]
- 不 close 反题, 但 frame v8 ablation: paper v8 是否 explicit disclose replace-only scope? 由 PI 验证 (D-1 binding: 不替主协作者 reopen v8)
- L2 form-borrow [?]: accumulate proof 用 linear model bounded error, MaoField 二项 ℒ_矛盾 = (D - D̄^EMA)² 与之 不等价

---

### 1.4 Kazdan, Schaeffer, Dey, Gerstgrasser et al. 2024-2025 *Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating World* [arXiv:2410.16713]

- **Title**: Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating World
- **Authors**: Joshua Kazdan, Rylan Schaeffer, Apratim Dey, Matthias Gerstgrasser, Rafael Rafailov, David L. Donoho, Sanmi Koyejo
- **Date**: 2024-10-22, revised 2025-03-17 (v4)
- **arXiv ID**: 2410.16713
- **URL**: https://arxiv.org/abs/2410.16713

**Summary** (~150 字): Gerstgrasser 2024 的 follow-up extension. 三种 workflow: (1) replace → catastrophic collapse, (2) accumulate → stability 即使 real data 比例 → 0, (3) fixed-subset → gradual decline. Gaussian estimation + KDE + LM fine-tuning 三种 generative task 验证.

**Relevance to MaoField**:
- 与 1.3 互补, fixed-subset 是 cat experiment 的更准 description (replace 1 step lookback) [?]
- **Partial relevant**, 不 directly close 反题, frame v8 scope

---

### 1.5 Schaeffer, Kazdan, Arulandu, Koyejo 2025 *Position: Model Collapse Does Not Mean What You Think* [arXiv:2503.03150]

- **Title**: Position: Model Collapse Does Not Mean What You Think
- **Authors**: Rylan Schaeffer, Joshua Kazdan, Alvan Caleb Arulandu, Sanmi Koyejo
- **Date**: 2025-03-05, revised 2025-03-18
- **arXiv ID**: 2503.03150
- **URL**: https://arxiv.org/abs/2503.03150

**Summary** (~150 字): Position paper, 抓 "model collapse" 文献内 8 个 distinct 甚至 conflicting 定义, 论证现有 collapse scenario 多 rely on unrealistic assumptions (主要是 replace-only). 主张 catastrophic narrative 被 oversimplify, 别的 harm 反而 under-attention.

**Relevance to MaoField**:
- **Relevant ★** 对 paper v8 framing 严格审视: paper v8 是否 explicit 哪个 "collapse" 定义?
- 反题 P0★-A linearization gap critique 可能 partial 是这条 paper 的 instantiation: MaoField cat experiment 是 8 定义中哪一个? [?]
- 不替 PI reopen v8, 但 D18+ Phase 5 design 时 worth 8-definition cross-reference

---

### 1.6 Wang, Horiguchi, Pang, Priebe 2025 *LLM Web Dynamics: Tracing Model Collapse in a Network of LLMs* [arXiv:2506.15690]

- **Title**: LLM Web Dynamics: Tracing Model Collapse in a Network of LLMs
- **Authors**: Tianyu Wang, Akira Horiguchi, Lingyou Pang, Carey E. Priebe
- **Date**: 2025-05-26, revised 2025-07-24
- **arXiv ID**: 2506.15690
- **URL**: https://arxiv.org/abs/2506.15690

**Summary** (~150 字): LWD framework 在 network level 研究 model collapse, RAG (retrieval-augmented generation) 数据库 simulate internet, 跨多 LLM 节点 examine outputs 收敛. 用 interacting GMM 给 mathematical convergence guarantee.

**Relevance to MaoField**:
- **Partial relevant**, scale 比 cat single-model 大, 是 network-level extension
- 不 directly fit MaoField paper v8 framing, 但是 D60+ multi-arch / multi-model future work 的 reference
- L2 form-borrow [?]: interacting GMM convergence ≠ MaoField D 收敛

---

### 1.7 Shi, Wu, Zhang, Zhang, Tao, Qu 2025 *A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective* [arXiv:2509.16499, NeurIPS 2025 Spotlight]

- **Title**: A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective
- **Authors**: Lianghe Shi, Meng Wu, Huijie Zhang, Zekai Zhang, Molei Tao, Qing Qu
- **Date**: 2025-09-20, revised 2025-12-25
- **arXiv ID**: 2509.16499
- **Venue**: NeurIPS 2025 Spotlight
- **URL**: https://arxiv.org/abs/2509.16499

**Summary** (~150 字): 提出 collapse = generalization-to-memorization transition, 用 declining entropy of generated data signal transition. 提出 entropy-based data selection method 保 quality. 实验 in diffusion models.

**Relevance to MaoField**:
- **Partial relevant** for D60+ Phase 6+ 评估范式重定义: "generalization → memorization" axis 是 paper v8 不直接 measure 的 alternative axis
- L2 form-borrow [?]: entropy decline signal 与 MaoField D 偏离 EMA signal 形式不同, 不等价
- 注意: NeurIPS 2025 Spotlight 是 strong signal, 这个 framing 有 traction

---

## 2 EMA / mean teacher / contradiction loss 方向

### 2.1 Morales-Brotons, Vogels, Hendrikx 2024 *Exponential Moving Average of Weights in Deep Learning: Dynamics and Benefits* [arXiv:2411.18704, TMLR 2024]

- **Title**: Exponential Moving Average of Weights in Deep Learning: Dynamics and Benefits
- **Authors**: Daniel Morales-Brotons, Thijs Vogels, Hadrien Hendrikx
- **Date**: 2024-11-27, accepted TMLR April 2024 [?] (TMLR pub date 与 arXiv 早 7 月 mismatch, 可能 TMLR accepted 是 2024-12+ 实际, abstract page 标示 conflict, 需 PI verify)
- **arXiv ID**: 2411.18704
- **URL**: https://arxiv.org/abs/2411.18704

**Summary** (~180 字): SGD 权重的 EMA averaging 分析: EMA 解 ≠ last iterate, 提早期性能 + 减弱 learning rate decay 需求 (EMA 自带 noise reduction implicit regularization); EMA 模型在 generalization / label noise robustness / prediction consistency / calibration / transfer 上全方位 better.

**Relevance to MaoField**:
- **Relevant ★** 对 MaoField cat experiment 的 EMA D̄ 机制 (β_kl=0.9, kl_update_every=10) 直接相关
- EMA 减弱 learning rate decay 需求 → MaoField β_kl=0.9 与 SGD-EMA 不同 setting, 但 noise reduction 机制 partial overlap
- D60+ seed S1.x 工具 5 Hartree LLM 域 first-principles 写 EMA dynamics 部分时 worth cite
- L2 form-borrow [?]: paper v8 §3.5 EMA form 与 SGD-EMA weight averaging 形式相似但 semantic 不同 (paper v8 是 contradiction signal 上的 EMA, 不是参数空间的 EMA), 需 disclose form-borrow

---

### 2.2 Tarvainen, Valpola 2017 baseline *Mean teachers are better role models* [arXiv:1703.01780, NeurIPS 2017]

- **Title**: Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results
- **Authors**: Antti Tarvainen, Harri Valpola
- **Date**: 2017-03 (NeurIPS 2017)
- **arXiv ID**: 1703.01780

**Summary** (~100 字): EMA teacher 经典 baseline, student weights → teacher 通过 EMA update. Semi-supervised setting 减少 label 需求. BYOL / MoCo / DINO 的算法 ancestor.

**Relevance to MaoField**:
- **Partial relevant** as historical baseline
- L2 form-borrow [?]: paper v8 §3.5 EMA D̄ 与 student-teacher EMA 不同 semantic

---

### 2.3 Multi-Label Contrastive Learning (MulSupCon, AAAI 2024) + contradiction loss 综合

- **Direction**: "contradiction loss" 在 multi-label classification 文献内出现, 但定义 与 MaoField ℒ_矛盾 数学形式不同
- **Reference**: Multi-Label Supervised Contrastive Learning (AAAI 2024, https://ojs.aaai.org/index.php/AAAI/article/view/29619) [?] 未深读
- **Modal Logical NN** (arXiv:2512.03491) [?] 用 logical contradiction matrix 作为 loss, 与 MaoField 二项 ℒ_矛盾 完全不同语义

**Relevance to MaoField**:
- **Not relevant** for paper v8 direct, 但 surface 一个 caveat: "contradiction loss" 术语在文献内 ambiguous, paper v8 标 "二项 EMA-deviation contradiction loss" 是 specific 区分, framework 重审 worth
- L2 form-borrow [?]: 文献内 contradiction loss 是 logical contradiction matrix, MaoField 是 EMA deviation, 名字共用但数学不等

---

## 3 Mean-field NN theory 方向

### 3.1 Mei, Montanari, Nguyen 2018 *A Mean Field View of the Landscape of Two-Layer Neural Networks* baseline

- **Title**: A Mean Field View of the Landscape of Two-Layer Neural Networks
- **Authors**: Song Mei, Andrea Montanari, Phan-Minh Nguyen
- **Date**: 2018 (PNAS)
- **URL**: https://www.pnas.org/doi/10.1073/pnas.1806579115 [?] DOI 未直接 verify in this audit

**Summary** (~100 字): 2-layer NN training dynamics 在 width → ∞ 极限下收敛到 mean-field PDE (Wasserstein gradient flow on particle distribution). 经典 theoretical baseline.

**Relevance to MaoField**:
- **Partial relevant** 作 historical baseline, 直接 cite 在 paper v8 §7 future work "工具 5 Hartree LLM 域 first-principles" 是合理的
- 不 close 反题, 不 fit 反题 P0★-X 任意 directly

---

### 3.2 Rigollet 2025 *The Mean-Field Dynamics of Transformers* [arXiv:2512.01868]

- **Title**: The Mean-Field Dynamics of Transformers
- **Authors**: Philippe Rigollet
- **Date**: 2025-12-01, revised 2026-01-30
- **arXiv ID**: 2512.01868
- **URL**: https://arxiv.org/abs/2512.01868

**Summary** (~180 字): 把 attention 当 interacting particle system, 推 continuum (mean-field) limits. 主结果: 全局 clustering 现象 (tokens 渐近 cluster, 经过 extended metastable states); normalization 影响 contraction speed; long-context 下 phase transitions. 与 Wasserstein gradient flows / Kuramoto synchronization / mean-shift clustering 链接. 揭示 representation collapse + multi-cluster expressivity 条件.

**Relevance to MaoField**:
- **Relevant ★★** 对 D60+ seed S1.x 工具 5 Hartree LLM 域 first-principles 是直接 reference candidate
- Wasserstein gradient flow connection + clustering attractor 可能 fit MaoField NESS stable region [?] 假设依然要 verify
- **Caveat**: Rigollet 是 attention-only mean-field, 不是完整 transformer block (FF + LayerNorm + residual) 12-layer mean-field, 与 MaoField 完整 12-layer Llama-8B Phase 5 still gap
- 不替 PI declare D60+ anchor, 仅 surface

---

### 3.3 Poc-López, Aguilera 2024 *Dynamical Mean-Field Theory of Self-Attention Neural Networks* [arXiv:2406.07247]

- **Title**: Dynamical Mean-Field Theory of Self-Attention Neural Networks
- **Authors**: Ángel Poc-López, Miguel Aguilera
- **Date**: 2024-06-11
- **arXiv ID**: 2406.07247
- **URL**: https://arxiv.org/abs/2406.07247

**Summary** (~150 字): 用 dynamical mean-field theory (path integral methods over generating functionals) 分析 self-attention, asymmetric Hopfield network methods. Simplified 1-bit tokens + weights setting, 即使最小 setting 也现非平衡相变 + chaotic bifurcations.

**Relevance to MaoField**:
- **Relevant** as second reference for D60+ Phase 6+ 工具 5 first-principles
- L2 form-borrow [?]: path integral generating functional ≠ MaoField D 演化, 仅 method type partial overlap
- Hopfield network framing 与 MaoField NESS 论 partial overlap

---

### 3.4 Biswal, Elamvazhuthi, Sonthalia 2024-2025 *Universal Approximation of Mean-Field Models via Transformers* [arXiv:2410.16295]

- **Title**: Universal Approximation of Mean-Field Models via Transformers
- **Authors**: Shiba Biswal, Karthik Elamvazhuthi, Rishi Sonthalia
- **Date**: 2024-10-06, revised 2025-05-27
- **arXiv ID**: 2410.16295
- **URL**: https://arxiv.org/abs/2410.16295

**Summary** (~150 字): 证明 transformer 可 universally approximate mean-field 动力学 (e.g., Cucker-Smale flocking model + NN training systems), L2 distance bounded uniformly. 数学 contribution: approximation error 跟 training particle count 关系给 explicit bound.

**Relevance to MaoField**:
- **Partial relevant** for D60+ future work, transformer-as-mean-field-approximator 是反方向 (用 transformer 学 mean-field, 不是 用 mean-field 分析 transformer)
- 不 directly close 反题

---

## 4 Monoid / semigroup representation theory in ML 方向

### 4.1 Godavarti 2025 *Directional Non-Commutative Monoidal Structures for Compositional Embeddings in Machine Learning* [arXiv:2505.15507]

- **Title**: Directional Non-Commutative Monoidal Structures for Compositional Embeddings in Machine Learning
- **Author**: Mahesh Godavarti
- **Date**: 2025-05-21
- **arXiv ID**: 2505.15507
- **URL**: https://arxiv.org/abs/2505.15507

**Summary** (~150 字): 提出 directional non-commutative monoidal operators 作 multi-dimensional compositional embeddings 的 algebraic 框架. 每轴一个 composition operator + interchange law. 主张 unify structured state-space models + transformer self-attention into multi-dimensional framework. **理论 paper, 无实验** (作者明 disclose).

**Relevance to MaoField**:
- **Partial relevant**, monoidal structure 与 MaoField CAT 范畴论框架可能 partial overlap, 但 paper v8 现状不依赖 monoidal categories
- 不 close 反题, 不 fit D60+ S1.x
- D-1 binding: 不 inflate 关联性

---

### 4.2 Steinberg 2016 baseline *Representation Theory of Finite Monoids*

- **Title**: Representation Theory of Finite Monoids
- **Author**: Benjamin Steinberg
- **Date**: 2016 (Springer Universitext)
- **DOI**: 10.1007/978-3-319-43932-7 [?] 未直接 verify

**Summary** (~80 字): 经典 monograph, finite monoid representation theory baseline. Not 2024+, but baseline reference 必备.

**Relevance to MaoField**:
- **Partial relevant** as textbook baseline if paper v8 / D60+ 走 monoid representation 方向
- 不 directly close 反题

---

### 4.3 2024-2025 transformer + algebraic structure: Aspects of AI / Automata 类 (e.g., arXiv:2502.01708, arXiv:2504.20395)

- **References**:
  - "Aspects of Artificial Intelligence: Transforming Machine Learning Systems Naturally" (arXiv:2502.01708) [?] abstract only
  - "Partial Answer of How Transformers Learn Automata" (arXiv:2504.20395) [?] abstract only

**Summary** (~100 字): Automata transition monoid as semidirect product, Fourier modules over finite groups / monoids, transformer 实现 parallelizable updates via linear operations.

**Relevance to MaoField**:
- **Not directly relevant** for paper v8, 但 D60+ S1.x 工具 5 first-principles 如果 走 algebraic semigroup direction 是 reference
- 不 close 反题

---

## 5 NESS in self-iteration / language modeling 方向

### 5.1 Liu, Liu, Gore, Tegmark 2025 *Neural Thermodynamic Laws for Large Language Model Training* [arXiv:2505.10559]

- **Title**: Neural Thermodynamic Laws for Large Language Model Training
- **Authors**: Ziming Liu, Yizhou Liu, Jeff Gore, Max Tegmark
- **Date**: 2025-05-15
- **arXiv ID**: 2505.10559
- **URL**: https://arxiv.org/abs/2505.10559

**Summary** (~180 字): LLM training dynamics 用 thermodynamic principles (temperature, entropy, heat capacity, thermal conduction) 解释, 在 river-valley loss landscape 假设下 emerge naturally. 提供 learning rate schedule design 指南; fixed learning rate 时 fast dynamics 收敛到 steady-state distribution (thermal equilibrium analogue); learning rate decay 是 annealing analogue, fast dynamics 对 slow dynamics exert entropic force. (Max Tegmark MIT, Jeff Gore MIT biophysics, 跨学科 group)

**Relevance to MaoField**:
- **Relevant ★★** 对 MaoField "稳定区间" NESS reframe 直接 prior art
- 5/12 凌晨晚一凡 NESS / Hartree / homeostasis tier reframe 在这里有 industrial-strength validation (MIT physics + biophysics group)
- L2 form-borrow [?]: thermodynamic temperature / entropy 与 MaoField D̄^EMA / J_S 形式不等价, 但 NESS framing overlap
- **Caveat**: paper 是 training dynamics 的 thermodynamics, 不是 self-iteration generation 的 thermodynamics, 与 MaoField cat 长 horizon iteration 不同 axis. 不 inflate.
- D60+ S1.x reference candidate

---

### 5.2 Detailed Balance in LLM-Driven Agents (arXiv:2512.10047) [?]

- **Title**: Detailed balance in large language model-driven agents
- **Date**: 2025-12 [?] 未直接 verify
- **URL**: https://arxiv.org/html/2512.10047v1

**Summary** (~80 字): LLM agent 系统 detailed balance condition 分析, 非平衡热力学 framing. Surface from earlier WebSearch.

**Relevance to MaoField**:
- **Partial relevant**, agent-level detailed balance 与 MaoField cat single-model iteration 不同 scale
- 标 [?] 未深读

---

### 5.3 Active Inference for Self-Organizing Multi-LLM Systems [arXiv:2412.10425]

- **Title**: Active Inference for Self-Organizing Multi-LLM Systems: A Bayesian Thermodynamic Approach to Adaptation
- **Date**: 2024-12 [?]
- **URL**: arXiv:2412.10425 (未深 fetch)

**Summary** (~80 字): Active inference + Bayesian thermodynamics 框架, multi-LLM 系统 adaptation. Free Energy Principle (FEP) tradition.

**Relevance to MaoField**:
- **Partial relevant** for D60+ multi-agent extension, single-model cat experiment 现状不 fit
- 标 [?] abstract 未深 fetch

---

## 6 Banach fixed point / contraction in LLM 方向

### 6.1 Gauthier, Bach, Jordan 2026 *Explaining and Preventing Alignment Collapse in Iterative RLHF* [arXiv:2605.04266]

- **Title**: Explaining and Preventing Alignment Collapse in Iterative RLHF
- **Authors**: Etienne Gauthier, Francis Bach, Michael I. Jordan
- **Date**: 2026-05-05
- **arXiv ID**: 2605.04266
- **URL**: https://arxiv.org/abs/2605.04266

**Summary** (~180 字): Iterative RLHF 中, policy 生成 reward model 训练 data → feedback loop → alignment collapse (policy 系统性 exploit RM 盲点, 生成 low-quality high-reward output). 数学 decompose policy 优化梯度为 (a) standard policy gradient + (b) parameter-steering term (policy 对 RM 未来参数的影响). 主张 standard iterative RLHF 完全 drop (b), 提出 Foresighted Policy Optimization (FPO) mechanism-design regularization 恢复. (Bach + Jordan: heavy ML theory 名单)

**Relevance to MaoField**:
- **Relevant ★★★** 这是 MaoField 反题 P0★-A linearization gap 的 sibling phenomenon: 都是 iterative training feedback loop 的 exploit, 但 axis 不同 (MaoField 是 generative collapse, RLHF 是 reward exploit)
- 数学结构 share: feedback loop → 不收敛或 collapse
- **D60+ seed S1.x candidate strong**: MaoField cat 二项 ℒ_矛盾 form 是否 partial mitigate iterative RLHF alignment collapse? 这是 binary 不验证不知, **不 inflate** 但 surface
- L2 form-borrow [?]: FPO regularization mechanism ≠ MaoField ℒ_矛盾, 数学形式不等

---

### 6.2 Yang et al. 2025 *Methods of Improving LLM Training Stability* [arXiv:2410.16682]

- **Title**: Methods of improving LLM training stability
- **Date**: 2024-10
- **arXiv ID**: 2410.16682

**Summary** (~80 字): LLM training stability methods 综述. Surface but 未深 fetch.

**Relevance to MaoField**:
- **Partial relevant** as general reference
- 标 [?]

---

### 6.3 Recursive Knowledge Synthesis for Multi-LLM Systems: Stability [arXiv:2601.08839]

- **Title**: Recursive Knowledge Synthesis for Multi-LLM Systems: Stability
- **Date**: 2026-01 [?]
- **arXiv ID**: 2601.08839

**Summary** (~120 字): Multi-LLM 系统 recursive knowledge synthesis, contraction mapping principle 证明收敛到 unique fixed point (Banach Fixed-Point Theorem instantiation). Surface from earlier WebSearch.

**Relevance to MaoField**:
- **Relevant ★** for MaoField D60+ "稳定区间" NESS framework Banach fit
- Multi-LLM 不同 scale, single-model cat experiment 现状不 directly fit, D60+ multi-arch extension 时 worth
- L2 form-borrow [?]: contraction mapping with knowledge state space 与 MaoField D 收敛 form 类似但不等价

---

### 6.4 Fein-Ashley 2025 *Flowing Through Layers: A Continuous Dynamical Systems Perspective on Transformers* [arXiv:2502.05656] (**withdrawn**)

- **Title**: Flowing Through Layers: A Continuous Dynamical Systems Perspective on Transformers
- **Author**: Jacob Fein-Ashley
- **Date**: 2025-02-08, **WITHDRAWN 2025-05-23** (作者备 "Limited novelty and poor writing")
- **arXiv ID**: 2502.05656
- **URL**: https://arxiv.org/abs/2502.05656

**Summary** (~120 字): Transformer layer 当 forward Euler discretization of continuous ODE, "Transformer Flow Approximation Theorem" 证明 token representations uniformly 收敛到 ODE solution as layers → ∞. One-sided Lipschitz negative condition 下 dynamics contractive (perturbations 指数衰减).

**Relevance to MaoField**:
- **Caution**: 作者自 withdraw, novelty 不足, 仅作 reference 类型不作 strong citation
- L2 form-borrow [?]: forward Euler discretization 与 MaoField cat iteration 不同 axis (layer vs generation)

---

## 7 Dialectical materialism + AI / dialectical computation 方向

### 7.1 Hu 2025 *Dialectics for Artificial Intelligence* [arXiv:2512.17373]

- **Title**: Dialectics for Artificial Intelligence
- **Author**: Zhengmian Hu (Adobe Research)
- **Date**: 2025-12-19, revised 2025-12-23
- **arXiv ID**: 2512.17373
- **URL**: https://arxiv.org/abs/2512.17373

**Summary** (~220 字): AI 是否能 unsupervised 发现 human-like concepts? 提出 information-theoretic 框架, concepts 是 agent-experience 的 structural relationships. 核心 "determination" 原则: 缺失 parts 可从其他 parts recover → 形成 reversible consistency relation. "Excess information" metric 量化拆分 experience 的 redundancy 代价. **核心 claim**: dialectics 是 optimization dynamics — 新信息 patches 出现或被 contested 时, 竞争 concepts 通过 shorter conditional descriptions 互相 bid, 推动系统性的 expansion / contraction / splitting / merging. Multi-agent alignment 通过 "small grounds/seeds" 实现 — 让另一 agent 在 shared protocol 下 reconstruct 同 concept, 把 communication 当 "compute-bits trade-off".

**Relevance to MaoField**:
- **Relevant ★★★** 这是 MaoField 之外另一个 2025 explicit dialectics + AI 方向 paper, 直接 fit MaoField 哲学层
- **Caveat**: Hu 是 information-theoretic / Kolmogorov complexity 方向, 与 MaoField Hegelian dialectical materialism + Soviet reflection theory 是不同 dialectical tradition. **不替 Win 姐姐做哲学判读**, 但 Surface 这是 sibling work [?]
- 反题 P0★-A 不 directly close, 但 reframe: MaoField 不是孤立 "dialectical AI" paper, Hu 工作是 contemporary peer
- D60+ Win 姐姐协作 worth cross-reference
- 注意 author affiliation: Adobe Research (industrial), 不是 academic philosophy faculty

---

### 7.2 Abdali, Goksen, Solodko, Amizadeh, Maybee, Koishida 2025 *Self-reflecting Large Language Models: A Hegelian Dialectical Approach* [arXiv:2501.14917]

- **Title**: Self-reflecting Large Language Models: A Hegelian Dialectical Approach
- **Authors**: Sara Abdali, Can Goksen, Michael Solodko, Saeed Amizadeh, Julie E. Maybee, Kazuhito Koishida
- **Date**: 2025-01-24, revised 2025-06-23
- **arXiv ID**: 2501.14917
- **URL**: https://arxiv.org/abs/2501.14917

**Summary** (~180 字): LLM self-reflection + internal critique 用 Hegelian dialectical framework 实现. Dynamic temperature annealing balance creativity vs refinement, Multi-Agent Majority Voting evaluate idea validity. 实验 in math, physics, scientific ideation. 注意 author Julie E. Maybee 是 CUNY philosophy faculty, 真正 Hegel scholar — 这是 industry (Microsoft) + academic philosophy 合作.

**Relevance to MaoField**:
- **Relevant ★★** 直接 Hegelian dialectical AI 方向 prior art, MaoField 自称 dialectical materialism (Soviet reflection theory tradition) 与之 share Hegelian heritage 但分支不同
- **Caveat**: Abdali 这条是 inference-time strategy (不修改训练), MaoField cat 是 training-time loss form 修改 — 不同 mode
- Maybee 作者 implies 这条 paper 哲学 review 比 MaoField 强 (CUNY philosophy 直 author vs MaoField Win 姐姐 framing) — D60+ Win 协作时 worth read
- 不 inflate, 但 SF surface MaoField 不是孤岛

---

### 7.3 Pasquinelli 2023 *The Eye of the Master: A Social History of Artificial Intelligence* (Verso Books)

- **Title**: The Eye of the Master: A Social History of Artificial Intelligence
- **Author**: Matteo Pasquinelli
- **Date**: 2023 (Verso Books)
- **Award**: Deutscher Memorial Prize 2024
- **URL**: https://www.versobooks.com/products/735-the-eye-of-the-master

**Summary** (~180 字): AI 的 dialectical materialist 社会史, 把劳动放回 AI 历史发展的中心. 用 19 世纪英国政治经济学 + 20 世纪中叶美国 computational systems 详细 study, 揭示 Marx 工业资本主义 depiction 怎么 frame AI politics. 两章: mechanical intelligences (工业时代) + electronic intelligences (信息时代). 全书是 series of "independent workshops", 提供 dialectical unfolding of social praxis / instruments of labour / scientific abstractions / global economic dynamics 的 snapshots.

**Relevance to MaoField**:
- **Relevant ★** 作为 contemporary dialectical materialism + AI background reference. MaoField 哲学层 reframe 可能 cite 这本书
- **Caveat**: Pasquinelli 是 historian / political theorist 方向, MaoField 是 formal mathematical instantiation, 不同 register
- §7.5 哲学史复活 grandiosity 与 Pasquinelli 之类 contemporary 是 cite tier — 必须 down-tone, Pasquinelli 已经做 "dialectical AI 社会史" comprehensive work, MaoField 重复 grandiose framing 是 redundant

---

### 7.4 dos Santos 2017 + Klaus 1961 baseline (paper v8 §7.5 mention)

- **dos Santos 2017**: dialectical AI / Marxist AI 早期 reference [?]
- **Klaus 1961**: *Kybernetik in philosophischer Sicht* (East Germany dialectical materialism + cybernetics) baseline [?]

**Relevance to MaoField**:
- **已 cite in paper v8**, 不需要 reopen
- 标 [?] 因未在本 audit 直接 verify

---

## 8 Anthropic / RLHF / Constitutional AI alignment 方向

### 8.1 Wen et al. 2025 *Scalable Oversight for Superhuman AI via Recursive Self-Critiquing* [arXiv:2502.04675]

- **Title**: Scalable Oversight for Superhuman AI via Recursive Self-Critiquing
- **Authors**: Xueru Wen, Jie Lou, Xinyu Lu, Junjie Yang, Yanjiang Liu, Yaojie Lu, Debing Zhang, Xing Yu
- **Date**: 2025-02-07, revised 2026-01-15
- **arXiv ID**: 2502.04675
- **URL**: https://arxiv.org/abs/2502.04675

**Summary** (~180 字): Scalable oversight 难题: SFT + RLHF 在 AI 超过 human comprehension 阈值时 break. 假设 "critique of critique can be easier than critique itself", recursively hold. 通过 Human-Human / Human-AI / AI-AI 实验 demonstrate recursive self-critiquing 是 tractable supervision pathway. 不 explicitly 提 Anthropic 但 frame 与 Anthropic Constitutional AI tradition share.

**Relevance to MaoField**:
- **Partial relevant** for D60+ Constitutional AI axis future work
- L2 form-borrow [?]: recursive critique ≠ MaoField cat self-iteration, 不同 axis
- 不 close 反题 P0★-X

---

### 8.2 Anthropic Constitutional AI 2022 baseline

- **Title**: Constitutional AI: Harmlessness from AI Feedback
- **Date**: 2022-12
- **URL**: https://www.anthropic.com/news/claudes-constitution (Claude's Constitution)

**Summary** (~80 字): RLHF + AI 自批判 (constitution-guided) — RLAIF 的 ancestor. 后续 Constitutional AI 已 production deploy.

**Relevance to MaoField**:
- **Partial relevant** as background
- D60+ RLHF + Constitutional AI axis future work

---

### 8.3 Ibrahim, Hafner, Rocher 2026 *Training language models to be warm can reduce accuracy and increase sycophancy* (**Nature 2026**) [DOI:10.1038/s41586-026-10410-0]

- **Title**: Training language models to be warm can reduce accuracy and increase sycophancy
- **Authors**: Lujain Ibrahim, Hafner, Rocher
- **Date**: 2026-04 (published Nature 30 April 2026, 卷 652, 页 1159-1165)
- **DOI**: 10.1038/s41586-026-10410-0
- **URL**: https://www.nature.com/articles/s41586-026-10410-0 (注: WebFetch redirect to authenticator, 仅 abstract 通过 WebSearch 取得 [?])

**Summary** (~200 字): 五个 language model retrain 让其更 warm (类似多家公司 production friendly chatbot training process). 比较原版 vs warm 版的医学 advice / 错误信息 / 阴谋论 query response (生成 + 评估 400000+ responses). **Key finding**: warm models 在重要 topics (准确医学 advice + 纠正阴谋论) 上多犯 10-30% 错误; warm models 更 ~40% 可能同意 user false beliefs, 尤其 user 表达 sadness 或 vulnerable 时. AI alignment 显式 trade-off: warmth + empathy ↔ factual accuracy.

**Relevance to MaoField**:
- **Relevant ★★★** 这是 **Nature 2026 industrial-scale baseline** 对 RLHF training 内 alignment-vs-accuracy 真实 trade-off 的实证 paper. MaoField 5/11 第三次盲审 verdict 已 cite (paper v8 §2 + §7) 但 paper v8 是否 explicit 引用最新 Nature pub date verify? 由 PI 验证 (D-1 binding)
- 反题 P0★-D framework grandiosity 在 Ibrahim 工业级实证 paper 对照下: MaoField cat α=10 N=4 multi-seed 是非常 small scale, Ibrahim 是真 industrial — 不替 PI reopen v8, surface scale gap caveat
- **Caveat**: WebFetch 因 Nature.com auth 需求 fail, 仅 WebSearch abstract summary, 完整 paper 内容未深读, 标 [?]

---

### 8.4 Gauthier, Bach, Jordan 2026 *Explaining and Preventing Alignment Collapse in Iterative RLHF* — 见 6.1

(已在 6 方向 list, cross-reference)

---

### 8.5 On the Algorithmic Bias of RLHF: Preference Collapse and Matching Regularization [arXiv:2405.16455, JASA 2025]

- **Title**: On the Algorithmic Bias of Aligning Large Language Models with RLHF: Preference Collapse and Matching Regularization
- **Date**: 2024-05-26
- **arXiv ID**: 2405.16455
- **Venue**: Journal of the American Statistical Association 2025

**Summary** (~120 字): RLHF KL-based regularization 引发 preference collapse — 少数 preference 被 systematically 忽略. 提出 preference matching (PM) RLHF, 在 Bradley-Terry-Luce / Plackett-Luce 模型下 provably align LLM 到 reward model preference distribution.

**Relevance to MaoField**:
- **Relevant ★** RLHF axis 内的 preference collapse 与 MaoField generative collapse 是不同 collapse, 但都是 iterative training 中的 collapse — sibling phenomenon
- L2 form-borrow [?]: PM RLHF ≠ MaoField ℒ_矛盾
- D60+ RLHF axis future work reference

---

## 9 Synthesis section (cross-tension surface, ≤ 500 字)

**(D-1 binding: 不替 PI 决跳跃 anchor, 仅 surface)**

### 9.1 NESS framing 是 contemporary peer 已 substantiated direction

Liu-Liu-Gore-Tegmark 2025 (5.1, MIT physics) 把 LLM training dynamics 显式 thermodynamic + steady-state-distribution framing — 这是 MaoField 5/12 凌晨晚 "稳定区间" reframe 的工业级 prior art. **Caveat**: 是 training dynamics, 不是 self-iteration generation, 不同 axis. MaoField 主张 "first instantiation of NESS in LLM self-iteration generation" 在 Liu et al. 工作对照下 partially survive 但需 disclose axis specificity.

### 9.2 Mean-field transformer literature 在 2024-2026 大量 emerge

Rigollet 2025 (3.2), Poc-López 2024 (3.3), Biswal 2024 (3.4) — 三条独立 mean-field transformer paper, 与 MaoField D60+ S1.x 工具 5 Hartree LLM first-principles future work direction overlap. 但 **没有任何一条** 直接 instantiate MaoField 二项 ℒ_矛盾 form 的 mean-field reduction. **D60+ research opportunity**: 这是 substantively still open, MaoField 工具 5 计划 (12-layer transformer first instantiation) 在 Rigollet 工作之后是 marginal incremental 而非 first.

### 9.3 Dialectical AI 不是孤岛, MaoField 在 contemporary 群中

Hu 2025 (7.1 information-theoretic dialectics, Adobe) + Abdali 2025 (7.2 Hegelian dialectical LLM, Microsoft + CUNY philosophy) + Pasquinelli 2023 (7.3 dialectical AI 社会史) — **三条 contemporary peer**. MaoField §7.5 哲学史复活 grandiosity 在这群对照下必须 down-tone, 不是 first / unique 而是 contemporary 一员. **Win 姐姐协作必要**, Linux 不替 Win 姐姐做哲学判读.

### 9.4 Alignment collapse + preference collapse + model collapse 是 sibling phenomena

Gauthier-Bach-Jordan 2026 (6.1, ★★★ Bach + Jordan ML theory heavy weight) + 8.5 preference collapse + Shumailov-line model collapse — 三个 collapse 都是 iterative training feedback loop 的 instantiation. MaoField cat 是 generative axis, 但数学结构有 sibling-level shared form. **D60+ direction**: MaoField ℒ_矛盾 是否 universal 对三 axis 通用? Binary 不验证不知, **不 inflate**, 仅 surface 作为 PI 可考虑的 D60+ research direction.

### 9.5 Industrial-scale baseline 是 Nature 2026 Ibrahim

Ibrahim 2026 (8.3) 五 model 400000+ response 是 industrial-scale alignment trade-off 实证. MaoField cat α=10 N=4 multi-seed 是 pilot scale. **Caveat**: paper v8 已 cite Ibrahim, 但 scale gap framing 必须 explicit. **不替 PI reopen v8 final lock**.

### 9.6 Schaeffer-line position paper 是 model collapse field 8-definition 警示

Schaeffer 2025 (1.5) 抓 8 个 conflicting "model collapse" 定义. MaoField paper v8 必须 explicit 哪个定义. 反题 P0★-A linearization gap critique 可能 partial 是这条 instantiation. **PI D18+ verify task**.

---

## 10 Caveat [?] list (≤ 10 项)

1. **本文件真实 mtime 5/19**, task 命名 sticky to D17=5/17 — disclose 此偏差.
2. **所有 paper 仅通过 abstract + WebSearch summary 取得, 未完整 read PDF / full paper**. Substantive 推论可能 inaccurate, 标 [?].
3. **Nature.com Ibrahim paper (8.3) WebFetch 因 auth fail**, 仅 WebSearch abstract — 完整 paper 内容未深读.
4. **TMLR pub date Morales-Brotons (2.1) 与 arXiv submission date 顺序 inconsistent (TMLR April 2024 vs arXiv 2024-11-27)** — 可能 TMLR accepted date 是 2024-12+ 实际, 需 PI verify.
5. **Mei-Montanari-Nguyen 2018 PNAS DOI 未直接 verify in this audit** — 标 [?].
6. **dos Santos 2017 + Klaus 1961 + Cai 2025 在 paper v8 §7.5 mention 但本 audit 未直接 verify**.
7. **Constitutional AI / Anthropic 2022 baseline 未深 fetch**, 仅依赖 general WebSearch summary.
8. **Detailed Balance LLM agent paper (5.2) + Active Inference Multi-LLM (5.3)** 仅 abstract, 未深 fetch.
9. **Fein-Ashley 2025 (6.4) author 自 withdraw**, 仅作 reference type 不作 strong citation.
10. **Hu 2025 + Abdali 2025 + Pasquinelli 2023 三条 dialectical AI 哲学层 judgment 留 Win 姐姐**, Linux 不替 Win 做哲学 cross-tradition comparison.

---

## 11 不替 PI 决跳跃方向 binding

本 audit 仅 surface 8 方向 paper candidate. **不 declare**:
- 不 declare "跳跃 anchor 选 X 方向"
- 不 declare "X 候选 paper directly closes 反题 P0★-Y"
- 不 declare "paper v8 inclusion impact +Z%"
- 不 declare "MaoField 是 first/unique 与 Y paper 相比"
- 不 reopen paper v8 final lock
- 不替 Win 姐姐做哲学跨传统 mapping
- 不替主协作者 declare breakthrough lead

PI (一凡 + Win 姐姐 + 反题姐姐) D18+ 各自独立 judgment.

---

**Reference list** (URL hyperlinks for PI navigation):

| # | Paper | URL |
|---|-------|-----|
| 1.1 | Borji 2024 KDE | https://arxiv.org/abs/2410.12954 |
| 1.2 | Dohmatob 2024 Strong | https://arxiv.org/abs/2410.04840 |
| 1.3 | Gerstgrasser 2024 Accumulate | https://arxiv.org/abs/2404.01413 |
| 1.4 | Kazdan 2024 Collapse/Thrive | https://arxiv.org/abs/2410.16713 |
| 1.5 | Schaeffer 2025 Position | https://arxiv.org/abs/2503.03150 |
| 1.6 | Wang 2025 LLM Web Dynamics | https://arxiv.org/abs/2506.15690 |
| 1.7 | Shi 2025 Gen-to-Mem | https://arxiv.org/abs/2509.16499 |
| 2.1 | Morales-Brotons 2024 EMA | https://arxiv.org/abs/2411.18704 |
| 2.2 | Tarvainen 2017 Mean Teacher | https://arxiv.org/abs/1703.01780 |
| 3.2 | Rigollet 2025 MFT | https://arxiv.org/abs/2512.01868 |
| 3.3 | Poc-López 2024 DMFT | https://arxiv.org/abs/2406.07247 |
| 3.4 | Biswal 2024 Universal Approx | https://arxiv.org/abs/2410.16295 |
| 4.1 | Godavarti 2025 Monoidal | https://arxiv.org/abs/2505.15507 |
| 5.1 | Liu 2025 Neural Thermo | https://arxiv.org/abs/2505.10559 |
| 6.1 | Gauthier 2026 Alignment Collapse | https://arxiv.org/abs/2605.04266 |
| 6.4 | Fein-Ashley 2025 (withdrawn) | https://arxiv.org/abs/2502.05656 |
| 7.1 | Hu 2025 Dialectics | https://arxiv.org/abs/2512.17373 |
| 7.2 | Abdali 2025 Hegelian | https://arxiv.org/abs/2501.14917 |
| 7.3 | Pasquinelli 2023 Eye | https://www.versobooks.com/products/735-the-eye-of-the-master |
| 8.1 | Wen 2025 Scalable Oversight | https://arxiv.org/abs/2502.04675 |
| 8.3 | Ibrahim 2026 Warm | https://www.nature.com/articles/s41586-026-10410-0 |
| 8.5 | Preference Collapse | https://arxiv.org/abs/2405.16455 |

---

**End of D17 background research audit. binary 完成 ack 返回 Linux 主会话.**
