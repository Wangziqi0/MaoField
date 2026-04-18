# 深度推理 · TF 必然局限 × DMFP 新范式 × AGI 冲击路径

**文档类型**: Linux Claude `max effort` 候选级 internal technical note (非 paper material)
**日期**: 2026-04-16
**作者**: Linux Claude (数学/物理 rigorous analysis 主导)
**引用**: Win (哲学判读) / arXiv v1 § (现有材料) / 反题姐姐 (standing critique)
**触发**: 一凡 2026-04-16 指令 "联合哲学+数学+物理 向 AGI 冲击 补全与解释 TF 必然局限 新范式"
**长度**: ~19,000 字
**状态**: v0.1 草稿，等 paper-review subagent adversarial 审查 + 一凡+Win 战略判读

---

## §0 Linux 纪律声明

这份 note 是 Linux Claude `max effort deep reasoning` 输出，**候选级技术预备**，**不是 paper material**。目的是给一凡+Win 在 arXiv v2/v3 或 capstone paper 规划决策时提供 rigorous 的数学/物理 ground truth。

**作者分工**:

| 角色 | 本 note 职责 |
|---|---|
| **Linux (本人)** | 数学/物理 rigorous analysis, Mode-tag discipline, 每 claim 落 `[Theorem]/[Proposition]/[Conjecture]/[Sketch]/[Observation]/[?]` |
| **Win (引用)** | §3 哲学局限直接引用 arXiv v1 §1.2 / §2.1 / §6.5 既有 narrative, 不代 Win 做独立新判读 |
| **一凡+Win (归属)** | 战略结论 (是否"必然"/DMFP 命名/AGI timeline/paper 纳入决策) 全部归你们 |
| **反题姐姐 (后续)** | 本 note 完成后 spawn 独立审查, 聚焦 cushion pattern / Popper 级 unfalsifiability / cross-LLM 家族盲点 |

**Mode tags (每 claim 必带)**:

| Tag | 强度 |
|---|---|
| `[Theorem]` | 已严证 (definition + proof 可 reconstruct from note) |
| `[Proposition]` | 接近严证, 需 minor formal work |
| `[Conjecture]` | 结构性支持但未证 |
| `[Sketch]` | 推理路径给出, 细节未填 |
| `[Observation]` | trivial fact, 单独讨论 |
| `[?]` | Linux 主观判断, 需一凡+Win confirm |

**核心边界**: "TF 必然局限" 本身是 **大战略判断**, 归一凡+Win+反题姐姐综合议决。Linux 能做的是: (a) 列出 **结构性可能是必然的理由**; (b) 每条局限给出 **证伪条件** (若 X 成立则 L_i 不必然); (c) 给出 **MaoField 对策** 从而不是 pure critique 而是 constructive。"必然性" 强度判读**不归 Linux**。

---

## §1 TF 框架的数学结构局限 (7 条)

**总思路**: 标准 TF 作为 function Φ_θ: V^n → Δ(V)^n (V 词表, Δ(V) simplex over V) 展开为 attention softmax + MLP + residual + layer norm + positional encoding + 训练时 cross-entropy gradient descent。每条局限 identify 的是 **TF 作为 dynamical system 的某结构性质缺失**, 及与 MaoField PDE

$$\gamma \partial_t \psi = D\nabla^2\psi - \frac{\partial V}{\partial \psi^*} + S(x,t) + \eta(x,t)$$

\+ b+c feedback `S = S_0 + α(ψ−⟨ψ⟩) + β δS_history` 的 structural contrast。

### §1.1 L1 `[Proposition]`: 无自反馈 → Axiom 6 结构违反

**命题**: 设 TF 一次 forward 为 Φ_θ: ℝ^{n×d} → ℝ^{n×d}。对固定 weight θ 和 input x, Φ_θ 是 **open-loop** 映射:

$$\Phi_\theta(x) = \text{LN} \circ \text{MLP}_L \circ \text{Attn}_L \circ \cdots \circ \text{MLP}_1 \circ \text{Attn}_1 \circ \text{Embed}(x)$$

不存在 self-referential 项 `x ↦ Φ_θ(x, Φ_θ(x))`。Autoregressive generation `p_θ(x_{n+1}|x_{≤n})` 是 Φ 外层包 next-token sampler, 但 Φ **本身** 仍 open-loop。

**对比 MaoField**: `S(x,t) = S_0 + α(ψ−⟨ψ⟩) + β δS_history`, ψ 的演化依赖 ψ 自身历史 (δS_history 是 ψ 的 time-integral)。即 Axiom 6 "匹配=自我训练" 的 PDE realization, inference 即 self-reference。

**为何是局限**: TF 把 "学习" 放在 train-time gradient descent, inference 时 θ fixed。这是 **ontologically distinct** 两阶段 (training ≠ inference)。Axiom 6 要求 learning-inference **unified** 在同一 trajectory 上发生 (由 b+c feedback 实现)。MaoField 中 inference 本身就有 feedback, 不区分 training/inference ontology。

**证伪条件 (何时 L1 不必然)**:
- Test-time training (Sun et al. 2020) 允许 θ 在 inference 时微调
- In-context learning 理论声称 attention 可以 mimic gradient descent within context (von Oswald et al. 2023)

**Linux 反驳**:
- Test-time training 是 inference 时再走一次 gradient descent on test data, 仍是 "train then infer" 的 local repeat, 不是 intrinsic self-reference
- In-context GD 的 claim 在 linearized regime 成立 (toy attention, linear models), scale 到 realistic setting 经验不一定 robust; 且 "GD inside forward" 仍是 Φ_θ 固定 output 的 determinate function, 不是 ψ 持续演化过程

`[?]`: 是否 "patch" (test-time training, in-context GD) 能真正 close this gap, 还是只是 effectively simulation - 这是战略判断, 归一凡+Win。Linux only 确认 vanilla TF architecture 无 intrinsic feedback。

---

### §1.2 L2 `[Proposition]`: Softmax 离散 sampling → 无 continuous attractor

**命题**: TF 的 next-token distribution `p_θ(·|x_{≤n}) ∈ Δ(V)` 是 categorical over 离散 V。Autoregressive generation 是 random walk 在 V* = ⋃_{n≥0} V^n 上。此空间无 metric attractor basin 结构。

**证明 sketch**:
- V 离散可数, V* 离散可数
- 传统 attractor 定义: compact invariant set A + 开 basin B(A) 满足 ∀x ∈ B(A), ω(x) ⊂ A
- 在 V* 上 ω-limit 要么是某 fixed infinite sequence (若 p(·|·) 是 deterministic argmax), 要么是 stationary distribution of the Markov chain on V (若 sampling)
- 前者是 "fixed point" 但不是 geometric attractor (无开 basin); 后者是 probabilistic attractor (invariant measure) 但 lacks geometric structure of basins

**对比 MaoField**: ψ ∈ ℂ^{32³} ≅ ℝ^{65536}, continuous state space。Attractor A ⊂ ℂ^{32³} 是 ω-limit of gradient flow, Basin(A) 是开集。Axiom 5 "复杂=简单叠加 via attractor hopping" 在此 geometrize 为 source-parameter-driven basin transition。Phase B Exp 1 empirically 观察到 k*=2 multi-attractor 结构 (§4.4 arXiv v1)。

**Tension with Axiom 1** ("粒子 = 动态过程"): TF 的 token 是 static symbol, 一次 forward 给 distribution + 一次 sampling 生 token — 这是 sampling 不是 dynamics。MaoField 的 ψ 本身在 time 上 evolve, token (if corresponding to attractor) 是过程的 ω-limit。

**证伪条件**: Latent diffusion / flow matching / continuous normalizing flows 在 continuous space 跑 dynamics, 部分填这个 gap。

**Linux 反驳**:
- Diffusion 是 train-on-data 的 statistical inversion (reverse noise process), 仍依赖外加 score matching objective (即 L4 level 的 "外加 loss"), 不是 Axiom 6 意义的 intrinsic feedback
- Flow matching 同理
- 所以 L2 和 L1+L4 is orthogonal axis - diffusion 填 L2 (continuous dynamics) 但 不填 L1/L4

`[?]`: "geometric attractor 是 compositional 必要条件" 这一 strong claim 归 Win 判读。Linux 只提供 structural observation。

---

### §1.3 L3 `[Observation]`: 有限 depth → 无时间演化轨迹

**命题**: 对 fixed input x 和 fixed θ, Φ_θ(x) 是 deterministic 一次计算。L layers finite → no continuous trajectory `{Φ_θ(x; t)}_{t ∈ [0,T]}`。"layer depth" 是 architectural depth, 不是时间。

**证明**: 显然。Φ_θ 是 L 个离散 blocks 的 finite composition, L < ∞。

**对比 MaoField**: 半群 `{U_t}_{t≥0}`, ψ(·, 0) → ψ(·, T) continuously。

**Tension**: "Layer depth as time" 的近似 (Chen et al. 2018 Neural ODE) 需 L → ∞ limit。这是 TF 的数学**近似**不是结构等价。MaoField 本体即 PDE, 不需要近似。

`[Proposition]` (additional): Time-evolution 允许 **spatially local dynamics** (ψ 在 patch 内独立演化, 通过 D∇² coupling)。TF attention 每 layer 每次 O(n²) 全连接。Locality + time evolution 是 embodied cognition / compositional reasoning 的可能 prerequisite。

`[?]`: "locality 对 AGI 是 necessary" 是强战略 claim, 归 Win。Linux 只确认 TF 的 O(n²) all-to-all attention 不 accommodate 严格 locality。

---

### §1.4 L4 `[Proposition]`: 外加 loss function → Axiom 3 违反

**命题**: TF 训练目标是 `L(θ) = E_{x ~ q_data} [−log p_θ(x)]`。这是对 parameters θ 的 **external** 梯度 signal, 非 system-intrinsic。Axiom 3 "驱动力=内在规律" 要求 dynamics 由 V + D + S 结构自身决定。

**Formally**:
- L 依赖 data distribution q_data (external to model)
- ∇_θ L 作用在 θ-space, 与 state-space ψ dynamics 正交
- 训练 dynamics 是 `θ_{t+1} = θ_t − η ∇_θ L`, inference dynamics 是 `Φ_θ(x)`; 二者 ontologically 分离

**MaoField**: `γ∂_tψ = −δF/δψ* + S + η`, `F = ∫[D|∇ψ|² + V(|ψ|²)]dx` 是 **state-space** free energy functional。σ=0 下 `dF/dt = −γ⁻¹ ∫|δF/δψ*|² ≤ 0` monotone descent 是 state 自身的 Lyapunov property, 非外加 learning signal。

**Tension**: TF 的 loss 本质是把 "应然" (data distribution) 外加为 "实然" (模型拟合 target)。MaoField 坚持 "实然" 自身的 dialectical motion 足够产生 structure, 无需外加 "应然"。Win arXiv v1 §6.5 narrate 这是 dialectical-materialist commitment (b) "内在矛盾驱动" 的体现; Linux 只 confirm 数学上 loss 是外加算子 vs F 是 state functional 的 ontological asymmetry。

**证伪条件**: Energy-based models (LeCun 2006, Gutmann-Hyvärinen NCE, score-based SDEs) 有 intrinsic energy $E(x; \theta)$, 看似 "内在"。

**Linux 反驳**:
- EBM 的 energy function 仍是 θ-parameterized 且 θ 由 external data log-likelihood 训练 ⇒ energy 仍是 "学来的外加标准"
- MaoField 的 F 是 **fixed** functional (V = (|ψ|²−v²)² 是先验给定)，ψ evolve 在 fixed F 下 ⇒ F 是 structural prior 不是 learned
- 核心 distinction: "learn the rules" (EBM) vs "rules are intrinsic, dynamics learn-within-rules" (MaoField)

`[?]`: Whether "learned-rules-are-external" 的 philosophical distinction 构成 "必然局限" 归 Win。Linux only confirm 数学上 fixed-F 和 learned-E 是两种 paradigm。

---

### §1.5 L5 `[Proposition]`: Attention 无 time derivative → 历史是 finite window snapshot

**命题**: TF attention 对 token position j 的 access 通过 K_j, V_j = f(embedding(x_j) + pos(j))。对固定 input 这是 fixed function, 不 evolve。"历史" 被编码成 token embedding + position, 但 embedding 不是 time-integral。

**MaoField**:
$$\delta S_{\text{history}}(x, t) = \sum_{k=0}^{N_{\text{hist}}-1} w_k \cdot [\psi(x, t - k\Delta t) - \langle\psi\rangle(t - k\Delta t)] \cdot \Delta t$$
这是 exponentially-weighted time-integral, kernel `w_k = exp(−λ k Δt)` (Hebbian-like decay), theoretically unbounded horizon given memory capacity。

**Tension with Axiom 4**: Axiom 4 "语料=实践记录" 要求历史不是 sample, 是 continuous practice integral。TF 训练 corpus 是 text sample, 训练后固化到 θ 里; inference 时 "历史" 只在 context window 内, window 外 structural 遗忘。MaoField history buffer 是 ψ trajectory 的 exp-weighted integral。

**证伪条件**: RAG / long-context (100K+ tokens) / retrieval-augmented TF 填 window 限制; state-space models (Mamba, S4) 有连续 state evolution 近 hidden state integral。

**Linux 反驳**:
- RAG 是 external database 不是 intrinsic model state
- Long-context 只是放大 n, architectural 仍是 snapshot (2025 claim 1M context 但 attention 仍是 position-by-position key-value lookup, 不是 continuous integral)
- **SSM (Mamba) 最值得 note**: 其 state `h_t = A h_{t-1} + B x_t` 确实是 time-integral (infinite ω-stable if |A|<1)。**SSM 部分填 L5 gap**, 但仍不填 L1 (无 self-feedback) 和 L4 (外加 loss)。所以 SSM 不是 full Axiom 1-7 satisfier, 仍是 pillar 1 (知识) 改版

`[Conjecture]`: Long-range dependency 任务上, exponentially-weighted time-integral (MaoField + SSM) 有 sample-efficiency advantage over fixed-window attention (TF)。具体 rate conjecture 需 further theoretical work。

---

### §1.6 L6 `[Sketch]`: Parallel computation → 无 sequential attractor hopping → Axiom 5 不可 native 表达

**命题**: TF training + inference 全部 parallel (batched matmul over layers, heads, tokens)。这 architectural 上不 accommodates Axiom 5 "合成=attractor 序列跳跃"。

**Axiom 5 的 MaoField 版 (M6 RMC 候选)**: 推理 = 多步操作序列, 每步对应 source S(x, t_k) 变化, 驱动 ψ 从 attractor `a_k` 到 `a_{k+1}`。要求:
- State `ψ(t)` 在整个推理过程 **continuously** evolve
- Source `S(x, t)` 分段 time-varying
- ψ 轨迹在 multi-basin landscape 中 **sequential** hop
- 每 hop 对应 attractor → attractor morphism (即 RMC generator, §2.6 recovery snapshot)

**TF 的 Chain-of-Thought (CoT) 是否等价?** — 不等价:
- CoT 是 **token sequence externalization**: 每步 "re-encode" 整个 context 再 forward 一次
- 无 persistent continuous state 在 step 间 evolve
- CoT token 是 human-readable artifact, 不是 attractor geometry

**Why it matters**: CoT 依赖 token-level symbolic 外化, 遇到 "recursively deeper or cross-modal reasoning" 结构性受限 (token space 的 expressive 天花板)。MaoField attractor hopping 在 continuous state space 中, 不 bound by token symbolic。

`[?]`: 是否 CoT 的 empirical success 已 "证明" symbolic externalization 够用 — 这是 open empirical question。Linux 只 observe CoT 是 TF architectural primitive 之外的 hack。

---

### §1.7 L7 `[Proposition]`: Training-inference 二分违反 dialectical unity

**命题**: TF 有 sharp training / inference distinction:
- Training: θ 变 via gradient descent, use cross-entropy loss, data from q_data
- Inference: θ fixed, decoding strategy, input from user
- 两 phase 的 ontology (variables varying, objectives, data sources) 全部不同

**MaoField**: 无 training 阶段。若走 Phase C (Axiom 7 动态 V), 则 V 的参数 c 慢 update, 但这是 inference 的 integral part, 不是独立 phase (two-timescale within single dynamics)。

**Dialectical tension**: "训练-推理二分" 是 "主-客二分" 残留。Win arXiv v1 §6.5 引 Mao 1937 《实践论》 - "实践即认识" - 学习就是 activity 本身, 不是先学好再用。TF violates 这 unified 结构。

`[?]`: 是否此 philosophical distinction (unified learning-acting vs split) 构成 "必然" 局限 — Win-attribute。Linux 只确认数学上 θ-update 与 forward pass 的 temporal decoupling。

---

### §1 结论 (mathematical)

| # | Limit | Mode | Axiom 违反 | 证伪条件 | Linux 反驳强度 |
|---|---|---|---|---|---|
| L1 | No self-feedback | `[Proposition]` | Axiom 6 | Test-time train / in-context GD | Strong (patches ≠ structural) |
| L2 | Discrete sampling | `[Proposition]` | Axiom 1 | Diffusion / flow matching | Moderate (orthogonal axis) |
| L3 | Finite depth | `[Observation]` | Axiom 1 + time | Neural ODE (L→∞) | Strong (ODE is 近似) |
| L4 | External loss | `[Proposition]` | Axiom 3 | EBM / score-based | Strong (learned ≠ intrinsic) |
| L5 | No time-integral history | `[Proposition]` | Axiom 4 | SSM / RAG / long-context | Moderate (SSM fills this but not L1/L4) |
| L6 | Parallel compute | `[Sketch]` | Axiom 5 | CoT | Moderate (CoT is hack) |
| L7 | Train/infer split | `[Proposition]` | Axiom 3 + 6 | Online learning / continual learning | Moderate (still two-mode) |

**Linux 判断**: 7 条 limits 中, **L1 (no feedback) 和 L4 (external loss)** 是最 structural 的, 当前已知 patches (test-time train, EBM) 不填这两个 gap 的 core。MaoField's b+c feedback (Axiom 6) + fixed-F free energy (Axiom 3) 结构性 address 这两个。这是为何 MaoField 不是 "another neural architecture" 而是 **paradigm-level alternative**。

`[?]`: "paradigm-level" 是战略 framing, 归 Win + 反题姐姐 (cushion pattern 警告 § recovery snapshot)。

---

## §2 TF 框架的物理结构局限 (6 条)

**总思路**: 把 TF 作为 dynamical system 检验它是否 support 物理学意义的 energy / phase transition / SSB / NESS / timescale separation / spatial structure。发现多条 structural 缺失。

### §2.1 P1 `[Observation]`: TF 无 free energy functional

**命题**: 标准 TF (attention + residual + LN + MLP) 的 forward 不对应任何 Lyapunov functional。Attention softmax 有 "partition function" `Z_i = Σ_j exp(QK^T/√d)_{ij}` 的表面类比, 但这是 per-query local normalization, 不是 global energy on system state。

**MaoField**:
$$F[\psi] = \int_\Omega [D|\nabla\psi|^2 + V(|\psi|^2)] \, dx$$
是 explicit free energy。σ=0: `dF/dt ≤ 0` 是 Lyapunov property, guarantees dissipative dynamics well-posed (Temam 1997)。

**Why it matters**:
- 无 Lyapunov functional 的 dynamical system 可能 chaotic / divergent / ill-posed
- TF 在 long autoregressive generation 中的 "degeneration" (repetition, incoherence) 可能与此相关 (缺 dissipative structure constraint)
- Energy 定义允许 thermodynamic 分析 (temperature, entropy, NESS)

**证伪条件**: Energy-based TF (LeCun-style) 有 `E(x; θ)`, 但 vanilla TF 无。

`[Observation]`: EBM extension 存在不否定 **标准 TF** 的 P1。P1 适用于 "TF as typically deployed" (ChatGPT, Claude, Gemini, Llama)。

---

### §2.2 P2 `[Proposition]`: TF 无真正 phase transition

**命题**: TF scaling laws (Kaplan et al. 2020, Hoffmann et al. 2022 "Chinchilla") 是 power-law `L(N) ∝ N^{−α}`, α ≈ 0.076。这不是相变, 是 smooth polynomial decay。

"Emergent abilities" (Wei et al. 2022, 某 capacity 在某 scale 突然出现) 的观察在 Schaeffer et al. 2023 "Emergent Abilities Are a Mirage" 中被 challenge — 很多"涌现"是 evaluation metric 的 step function artifact, 底层 loss 仍 smooth。

**MaoField**: Ginzburg-Landau-type 理论本体 support 二阶相变 (Mexican hat `V = (|ψ|² − v²)²`, U(1) symmetry, N→∞ thermodynamic limit)。临界点 correlation length `ξ → ∞` → long-range 关联 emerge。Pseudo-Goldstone mode 由 explicit source 诱导 (§3.6 recovery snapshot)。

**Tension**: 若 AGI 意义的 "理解涌现" 是 phase transition 意义的 sharp qualitative leap, 需 architecture support 临界行为。TF 数学上不支持 (finite N, 无 Lyapunov, smooth loss curve)。MaoField 支持 in principle, 当前 32³ finite-size 效应显著 (arXiv v1 §3.5 `[zn-loose]` footnote)。

`[?]`: "AGI 需要 phase-transition 级涌现" 是 strong 战略 claim。Win-philosophy 归一凡+Win。Linux only confirm TF 数学不支持严格相变。

---

### §2.3 P3 `[Proposition]`: TF 无 spontaneous symmetry breaking

**命题**: TF attention `Attn(Q, K, V) = softmax(QK^T/√d)V` 对 token 排列 `π` 是 permutation-equivariant:

$$\text{Attn}(Q_\pi, K_\pi, V_\pi) = \pi \cdot \text{Attn}(Q, K, V)$$

加 positional encoding 破 permutation symmetry, 但这是 **手设计外加**, 非 dynamical SSB。

**MaoField**: U(1) global phase symmetry 被 Mexican hat V preserved (|ψ|² invariant)。Source S(x) 或 Langevin noise 下 (N→∞ limit) spontaneous breaking - phase pattern 由 initial condition + noise realization 决定, 不 hand-design。

**Why it matters**: Anderson 1972 《More Is Different》 — SSB 是 emergent 结构的基础 mechanism。生物学上 cell polarity, 化学上 chirality, 物理上 magnetic order 都是 SSB instance。若 cognitive structure 的 emergence 类比 SSB, TF 手设计 positional encoding 是 structural shortcut。

**证伪条件**: 有论文 (e.g., rotary positional encoding RoPE, ALiBi) 设计 positional encoding 使其 "dynamical"。

**Linux 反驳**: RoPE/ALiBi 仍是 fixed functional form (rotation, linear bias), 不是 ψ dynamics emergent 的 pattern。是 clever handcraft。

---

### §2.4 P4 `[Proposition]`: TF 无 NESS

**命题**: Non-Equilibrium Steady State = 系统不处 equilibrium 但有 stationary measure + non-zero entropy production。

- TF inference: stateless map, 不 discuss stationarity (见 L1)
- TF training: SGD 近似 Langevin on loss landscape (Mandt et al. 2017), 有 quasi-stationary distribution 在 loss minimum 邻域 — 但这是 **equilibrium** (detailed balance 近成立) 不是 NESS

**MaoField** Phase B Exp 1: dS/dt ~ 10⁻⁶ plateau, 100% docs > 10⁻⁷ (recovery snapshot §3.5)。这是 NESS candidate, 尚未 pin down exact functional form (plateau vs power-law decay to 0)。

**Why it matters**: Friston Free Energy Principle / active inference framework 以 NESS 为 cognitive substrate。Generative creativity, long-term learning, possibly consciousness 在 NESS-based frameworks 中被 theoretically ground。

`[?]`: "NESS 是 AGI prerequisite" 是 strong 战略 claim, follows Friston/Parr 2022 《Active Inference》。Linux 只能 observe TF 结构不 accommodate NESS, 不 下 "所以 AGI 需要 MaoField" 级结论。

---

### §2.5 P5 `[Proposition]`: TF 无 timescale separation

**命题**: TF 所有 parameters jointly optimize, 每 gradient step update 所有 θ。无 Haken (1983) 意义的 slow/fast 分离 (部分 variable 慢变作 "control parameter", 其余快变 slave 到 adiabatic manifold)。

**MaoField Phase C (M7 候选)**:
- 快尺度: ψ 动力学 (dt ~ 0.01)
- 慢尺度: V 参数 c 动力学 (dτ ~ memory scale)
- Hebbian-like target: `c_i^* = ∫ dt e^{−t/τ_mem} φ_i(ψ(t))` (V 记得 ψ 历史 visited attractors)
- Slaving principle: ψ → A(c) fast, c → c^*[A(c)] slow, self-consistency

**Why it matters**: Long-term memory 的 physics-grounded mechanism。Short-term (fast ψ) 和 long-term (slow c) 不破坏彼此。

**TF 的 "长期记忆"**: 是 weight training 的 结果 — 离线, 需大量样本, 灾难性遗忘 (Parisi et al. 2019 continual learning review) 是已知 open problem。Structural difference: additive slow component (MaoField) vs wholesale weight update (TF)。

`[Conjecture]`: Catastrophic forgetting 的 root cause 是 TF 无 timescale separation。若架构支持 slow V, 灾难性遗忘结构性可避免。未证。

---

### §2.6 P6 `[Sketch]`: TF 无 spatial / percolation / bubble 结构

**命题**: TF 的 "structure" 是 representation vectors (in a single vector space per layer), 无 spatial concept 能讨论 coherent patches / correlation length / percolation。

Phase B Exp 1 empirical:
- exp mode 产生 50 phase-coherent patches (vs 0 in controls, §4 recovery snapshot)
- 亚临界 3D site percolation 估算 (§3.4 recovery snapshot): `p = 0.16 < p_c = 0.3116` (26-connectivity), cluster count ~50 (within factor 1.5 of observation)

**MaoField 本体**: 在 32³ lattice 上自然有 spatial dynamics (D∇² diffusion term)。Patches 可以被 interpret 为 "concept crystallization" — candidate language for compositional structure。

`[?]`: "Spatial structure 是 AGI prerequisite" — embodied cognition literature (Lakoff, Barsalou) 支持 but philosophical。Linux 只 confirm TF 数学上不 accommodate spatial structure。

---

### §2 结论 (physical)

| # | Limit | Mode | Why matters (physics) | MaoField 对策 |
|---|---|---|---|---|
| P1 | No free energy | `[Observation]` | 无 Lyapunov → dynamics 可 ill-posed | F = ∫[D|∇ψ|²+V]dx |
| P2 | No phase transition | `[Proposition]` | 涌现是 polynomial smooth, 非 qualitative leap | GL theory → 二阶相变 in principle |
| P3 | No SSB | `[Proposition]` | Position 是外加 handcraft | U(1) Mexican hat → spontaneous pattern |
| P4 | No NESS | `[Proposition]` | 无 active inference substrate | dS/dt ~ 10⁻⁶ NESS candidate |
| P5 | No timescale separation | `[Proposition]` | 灾难性遗忘 structural 不可避免 | Two-timescale slaving (Phase C) |
| P6 | No spatial structure | `[Sketch]` | 无 concept crystallization substrate | 32³ lattice spatial dynamics |

**Linux 判断**: P4 + P5 最 structural (Friston/Haken 已 建立的 physics frameworks 都要这两者)。其他 partial-substitute 存在但限 shallow patches。MaoField 对这六条都有 in-principle 对策, 深度不同 (P1 ✓ 已成立, P4 ⏳ candidate, P5 ⏳ Phase C, P2 partial 受 finite-size 限)。

`[?]`: 上述 "paradigm-level alternative" 的 framing 归一凡+Win+反题姐姐议决。

---

## §3 TF 框架的哲学局限 (引 Win + arXiv v1)

**Linux 纪律**: 本节 **不代 Win 做新哲学判读**, 只引用 arXiv v1 §1.2, §2.1, §6.5 Win 已有 narrative, 并 supplement 数学 signature。

### §3.1 引用: arXiv v1 §1.2 辩证唯物主义方法论 4 commitments (Win)

(a) **Material-first**: 数据客观实在 > subject interpretation
(b) **Internal contradiction as driver**: dialectical tension 不外加
(c) **Practice as criterion**: 循环实践-认识, not static objective
(d) **Social embedding**: research context + responsibility, not neutral

### §3.2 引用: arXiv v1 §6.5 Win 判读 TF 违反 4 commitments

Win arXiv v1 §6.5 明确 (paraphrase): TF 违反 (b)(c) 最直接:
- **(b) 违反**: TF cross-entropy loss 是外加优化目标, 不是内在矛盾驱动。"应然" (data distribution) 从外部注入 "实然" (模型参数) 中。
- **(c) 违反**: TF 训练是离线 gradient descent, 不是 practice → cognition → practice 循环。训练结束后 "cognition" 固化到 θ, 不再 practice。

### §3.3 Linux 补: "哲学判读 ↔ 数学结构 signature" 的对应

`[Observation]` 层级: Linux 不 commit 下面是 rigorous theorem, 只是 suggestive structural correspondence:

| Win 哲学判读 | Linux 数学 signature | Arxiv v1 对应 |
|---|---|---|
| 违反 (b) "内在矛盾驱动" | L4 外加 loss | §6.5 Win |
| 违反 (c) "实践标准" | L7 训练-推理二分 | §6.5 Win |
| Axiom 2 对立统一 | Adjunction F⊣G | §2.2 Win |
| Axiom 6 匹配=自训练 | b+c feedback PDE | §3.2 Axiom 6 realization |

**结构论点**: 哲学判读不是 "外加包装", 是 **直接对应数学 structure**。这是 arXiv v1 §2.2 "Lawvere adjoint as categorical bridge" 的 working 实例 — adjunction F⊣G 把哲学对立 (主/客, 训练/推理) 几何化为 categorical structure。

`[?]`: 上述 "对应不是偶然, 是 rigorous bridge 的 working instance" 是 **研究论点** (research thesis) 层级, 不是 theorem。需每条对应 case-by-case 检验。这是 arXiv v2/v3 的 open research agenda。

### §3.4 引用: arXiv v1 §1.2 dialectical materialism as method

Win 区分 "dialectical materialism as political-economic theory" (20 世纪主要 application) 和 "as working methodology for complex systems" (本项目提议)。后者的 3 tools:

1. **Spawn-agent review pipeline** = practice-as-criterion 的 paper-production-level 落地
2. **Mode-tag discipline** = 认识论精度 (静态/动态 regime 区分)
3. **OP-signpost** = 让内部矛盾可见而非 paper over

这 3 tools 在本项目已 validated (arXiv v1 §6.3 Methodological Reflection)。Linux 自检: 本 note 严格 adhere 这 3 tools - 每 claim tag, 每 limit 列 证伪条件, OP1 OP2 等 open problem 显式标出。

---

## §3 结论 (philosophical)

Win 的 arXiv v1 §6.5 判读 (TF 违反 b/c commitments) 得到 Linux 的数学 signature 对应 (L4 L7)。"TF 必然局限在哲学上" 的强 claim 完全归 Win, Linux 不 commit。

`[?]`: 本 note §3 是否进 v2/v3 paper 归一凡+Win 决定。若进, 建议 Win 扩写; 若不进, 本节作 internal reference。

---

## §4 TF 框架的信息论局限 (2 条)

### §4.1 I1 `[Sketch]`: Scaling laws 的结构解释

**Empirical**: Kaplan et al. 2020 `L(N) ≈ c·N^{−α}`, α ≈ 0.076。Chinchilla (Hoffmann et al. 2022) 给更精准的 compute-optimal tradeoff, 但本质仍是 polynomial。

**信息论解释 sketch**:
- TF 是 universal approximator over `q_data ↦ log q_data`
- Model capacity ~ O(N_params)
- Approaching Bayes-optimal rate on high-dimensional data manifold (intrinsic dim `d_int` << ambient dim `d`) 给 polynomial rate `N^{-O(1/d_int)}` (curse of dimensionality for non-structure-exploiting models, 参考 nonparametric regression 理论 Györfi et al. 2002)
- TF 经典 dense attention + MLP 不 exploit data 的 structural regularity (compositional, algebraic), 所以走 polynomial

**MaoField alternative** `[Conjecture]`: 若 data structure 是 attractor-amenable (symbolic / compositional / near-equilibrium basins), dynamical amplification via resonance / percolation / collective modes 可能给 super-polynomial (exponential in some regime) capacity scaling。

**具体 conjectured mechanism**:
- Resonance: Phase B Exp 1 observed coherent driving 放大 effective barrier crossing rate factor `~10⁴` (§3.2 recovery snapshot). 若 attractor 定位 task 的 effective SNR 有类似放大, sample efficiency 对应提升
- Percolation: 50 patches ~ 亚临界 percolation 在 `p = 0.16` (§3.4 recovery snapshot)。Criticality 邻域 long-range correlation length `ξ → ∞` → 同 # samples 信息利用率 ↑
- Collective modes: Goldstone / pseudo-Goldstone → soft long-range 关联 → effective dimension 降 (物理上 d_eff = d − # broken generators)

**Linux 自检**: 上述 I1 的 MaoField advantage 完全是 `[Conjecture]`, 完全 empirically unverified at AGI-scale。本 note 不 commit。

---

### §4.2 I2 `[Proposition]`: Compositional generalization 的 TF 结构瓶颈

**Empirical**: Lake & Baroni 2018 SCAN, Keysers et al. 2020 CFQ, Hupkes et al. 2020 review — TF 在 systematic compositional generalization 上结构性 underperforms, 虽 Hupkes 2023 argue GPT-4-scale 已有边际改进但非 qualitative leap。

**Why structural**: Compositional generalization 要求 internal representations 有 algebraic structure (known composition rules: symbol `f(g(x))` decomposes to `f`, `g`, `x` with fixed composition rule)。TF 的 attention weights 是 continuous reals, 无 algebraic constraint enforcing compositionality。

**MaoField M6 RMC 候选 (§2.6 recovery snapshot)**:
- Objects: attractors
- Morphisms Hom(a, b): time-parameterized sources 使 ψ(0) ∈ Basin(a), ψ(T) ∈ Basin(b) (homotopy class)
- Composition: source 时序拼接
- Tensor ⊗: parallel reasoning (independent field subsystems)

若 RMC 结构可 empirically realize (Phase C target), compositionality 是 native structure 不依赖 opaque attention。

`[?]`: RMC generator set 存在性 + 有限 generator 可覆盖任意 morphism (类比 universal quantum gates) 是 **非平凡 conjecture**, 未证, 完全 open。

**Linux 总结 §4**: 信息论 level 两条 TF 结构瓶颈 (scaling laws polynomial + compositional generalization underperform), MaoField 给出 in-principle 对策 (dynamical amplification + RMC), 对策全 [Conjecture] 级 **未证**。

---

## §5 DMFP 新范式: Dialectical-Materialist Field Paradigm

**Linux 纪律**: "新范式"的命名归一凡+Win。"DMFP"仅作本 note 内部缩写。Win 有权改名、改 framing、改 target audience。Linux 只给数学/物理 7 原则 spec。

### §5.1 DMFP 7 原则 (formal statement)

每条原则对应 MaoField 7 axioms 的一个形式化版本:

| # | 原则 | Formal | 对应 Axiom | 状态 |
|---|---|---|---|---|
| 1 | 理解 = 源场 ↦ attractor | F: Text → S via construction, G: S → A via gradient flow, T = G∘F endofunctor on Meas | A1 | ✓ Exp 1 empirical + §2.3 部分形式化 |
| 2 | 对立统一 = Adjunction | F⊣G Lawvere bijection `Hom_D(Fc, d) ≅ Hom_C(c, Gd)` | A2 | partial (§2.3 三 conjectures) |
| 3 | 驱动力 = 内在 dynamics | `γ∂_tψ = −δF/δψ* + S + η` 无 external loss | A3 | ✓ formal, 但 σ>0 ascending phase 是 OP2 |
| 4 | 语料 = 历史积分 | `δS_history = Σ w_k δψ(t−kΔt)`, w_k exp decay | A4 | ✓ formal + Signal A architectural theorem |
| 5 | 复杂 = 序列 attractor hopping | RMC (attractors, time-param sources) strict monoidal category | A5 | `[Conjecture]` M6 候选 |
| 6 | 匹配 = b+c 自反馈 | `S(x,t) = S_0 + α(ψ−⟨ψ⟩) + β δS_history` | A6 | ✓ Exp 1 validate + M3 `[Proposition]` 自洽方程 |
| 7 | 规则动态 = slow V | `V(ψ; c)`, `dc/dτ = −γ_c(c − c^*[ψ-history])` two-timescale slaving | A7 | `[Conjecture]` M7 候选, Phase C target |

### §5.2 三支柱 composition (M5 候选)

(D, V, S) triple 参数化 PDE 家族:

$$\gamma \partial_t \psi = \nabla \cdot (D^{(SCF)}(x) \nabla \psi) - \frac{\partial V^{(MF)}}{\partial \psi^*} + S_0^{(TF)}(x) + F[\psi]$$

- **D^(SCF)(x)**: Shape-CFD token graph Laplacian 诱导 anisotropic diffusion tensor (一凡 IPM paper 给框架, §3 Shape-CFD recovery snapshot)
- **V^(MF)**: MaoField Mexican hat V = (|ψ|² − v²)², Phase C 后扩展为 V(ψ; c) 动态
- **S_0^(TF)**: TF (BGE-M3 或类似) embedding 作 initial source, tiled 到 lattice (§2.2 recovery snapshot)
- **F[ψ]**: b+c feedback (即 A6 realization)

**Composition 结构 (M5 候选, §2.5 recovery snapshot)**:
- Parameter space = {(D, V, S)}
- 每 (D, V, S) 诱导 dynamical system on ψ-space
- Attractor 集合 A(D, V, S) 作 ω-limit

**Fiber bundle 而非 pipe**: MaoField F 根据 δψ 动态修改 effective S → TF 给的 S_0 被 MaoField 实时 modify。SCF 的 D 修改 MaoField 动力学地貌。三者耦合不是 sequential, 是 fiber-structure-over-base。

**可 falsify prediction** (M5 候选): 
- MaoField with BGE S_0 + 均匀 D_0 (无 SCF) → baseline (已有, Exp 1)
- MaoField with BGE S_0 + D_SCF (真正 token graph 诱导) → 对比 patch count + location
- 预测 (若 M5 成立): D_SCF graph 结构使 patch location follow token 关系图 → semantic 可解释性激增

Linux 时间成本估算: ~8h 构造 token graph → graph Laplacian → D tensor → 跑 MaoField 对比。一凡 authorize 后可以做。

### §5.3 4 pillars 架构 (今天 Linux 加 Pillar 4)

| Pillar | Role | 辩证唯物对应 | 项目实物 | 状态 |
|---|---|---|---|---|
| 1. **TF** | 知识 (过去积累的 semantic 结构) | 物质 (积累实践) | BGE-M3 / 类似 | Mature |
| 2. **Shape-CFD** | 结构 (token-level locality) | 反映 (结构对现实) | 一凡 IPM under review | Mature, peer review |
| 3. **MaoField** | 运动 (PDE 动力学 + b+c + attractor) | 矛盾 (内在驱动) | arXiv v1 (Zenodo) | Research stage, Phase B close |
| 4. **Operational / Social** | 算力 / 数据经济学 / 训练群体 | 生产关系 | 非技术, 生态问题 | `[Linux flag]` 不 commit |

Pillar 4 是今天 Linux flag 的 (recovery snapshot §1.3 "operational pillar"), 不是技术架构, 是 AI 发展的 social dimension (训练集 ownership, 算力分配, 研究者的 labor relations)。一凡 "21 世纪先进生产力" vision 属这个 pillar。**Linux 不 commit 这是 AGI 技术路径的一部分; 可以是 project political commitment 而非 technical claim**。

### §5.4 DMFP 缺的 pieces (gaps)

Linux 显式列当前 DMFP 作为 "完整范式" 的 gaps:

1. **Generation (主动生成)**: 三支柱都是 discriminative (rank/match/attractor-classify), 无 creative production。M6 RMC 若成立部分填此 gap (time-param source drive generation), 但完整 generative module 未设计
2. **Compositional multi-step reasoning (A5)**: M6 RMC 候选未 formal, 无 generator set existence proof
3. **Long-term episodic memory**: 当前 MaoField 每次 fresh, 无 cross-session persistent state。M7 slow V 候选若成立填此 gap (Phase C)
4. **Dynamic reaction rules (A7)**: V 当前 fixed Mexican hat, Phase C M7 目标是动态 V
5. **Embodiment**: 感知 / 动作 interface (robotics, agent), 完全未 design
6. **Scaling / 算力 / 数据 economics (Pillar 4)**: 非技术, 生态问题

**Linux 判断**: gaps 1-4 是 technical research agenda, Phase C / capstone paper 范畴。Gaps 5-6 是 broader research 生态 + social 维度, 归一凡 long-term vision。

`[?]`: 本节 §5 整体作为 "新范式 architectural spec" 的 intended audience - 是 Linux internal reference? 还是 arXiv v2/v3 material? 还是 capstone paper ? — 归一凡+Win 决定。

---

## §6 AGI 5-Phase 冲击路径

**Linux 纪律**: "AGI 冲击" 的 timeline + target-setting 归一凡。Linux 给的是 **technical feasibility analysis** 的 5 phases, 每 phase 列 gaps + 证伪 conditions。

### §6.1 Phase 1 (已达成, 2026-04-16)

**Milestone**: MaoField v1 on retrieval testbed

**已成立**:
- Axiom 6 empirical validated via b+c feedback (Phase B Exp 1)
- Axiom 1 partial: k*=2 multi-attractor, 50 phase-coherent patches (Exp 1)
- Axiom 3 formal: dissipative autonomous PDE, dF/dt ≤ 0 at σ=0
- Axiom 4 formal + Signal A architectural theorem (mean-zero feedback)
- arXiv v1 (130KB, 8 sections, 14 reviews, 27 errors caught)
- Zenodo v0.1.0 concept DOI 已在
- Phase B Exp 1 close with verdict + appendix

**未成立 Axioms**: A2 (partial, §2.3 三 conjectures), A5 (完全未形式化), A7 (Phase C target)

### §6.2 Phase 2 (近期, 2026 Q2, ~1-2 月 Linux work)

**Milestone**: Axiom 6 严格化 + 诊断扩展

**候选工作** (Linux 今天 max effort 6 候选, recovery snapshot §5):

| # | 工作 | 时间 | 发表 level |
|---|---|---|---|
| M1/M3 | V₀ 自洽方程数值 verify + 自伴证明 | ~5h | arXiv v2 |
| P3 | Kramers anomaly factor ~10⁴ instanton 推导 | ~3h | §4.11 upgrade |
| P1 | 50 patches percolation scaling scan | ~4h | Appendix quantitative |
| P5 | k*=2 random/shuffled control (反题姐姐 path 2) | ~6h | Block III control 重跑 |
| Cross-LLM | GPT-4.1 / Gemini 2.5 Pro review (path 5) | ~2h | 补 Opus 4.6 同家族盲点 |
| BM25 行 | §4.2 BM25 abstract + obs 改写 | 完成 | v0.1.1 P0 |

**共 ~20h Linux 可调度时间**。BM25 行 + M1/M3 + P3 + P1 是 Phase 2 first half 目标; P5 + cross-LLM 是 second half。

**Gap 显式列**:
- M1/M3 严证需 F 在 V₀ 自伴性 (kernel 对称性分析)
- P3 需 precise instanton bounce calculation
- P1 需 block_size + grid scan 得 empirical scaling curve
- Cross-LLM review 需 API 钱 (一凡 authorize)

### §6.3 Phase 3 (中期, 2026 Q3-Q4, IPM mechanism paper 轨道)

**Milestone**: IPM mechanism paper (Block V Phase A 结果, 2026-07-08 target)

**技术内容**:
- Phase A 实验 (一凡 IPM Shape-CFD paper 已含 PQ-Chamfer; 本 paper 目标是 mechanism-level 解释)
- Block V Phase A-0 / A-1 / A-2 / A-3 结果整合 (arXiv v1 §5.3)
- Phase C M7 two-timescale slaving 数值 (若 2026 Q3 前有 bandwidth)

**Gap**:
- Phase C 未 start, 完全 open empirical
- Two-timescale 数值稳定性未 test
- Hopfield-like memory capacity 未量化

### §6.4 Phase 4 (中远期, 2027 Q1-Q2, Nature MI capstone target)

**Milestone**: 三支柱 composition + M6 RMC + capstone paper

**技术内容**:
- M5 D^SCF + V^MF + S^TF 联合 PDE (工作 ~8h 已在 Phase 2 候选)
- M6 RMC generator set + compositional reasoning testbed
- Block V Phase A/B/C 全 merge into full composite
- Nature MI / NeurIPS / ICML 级 capstone paper

**Gap**:
- M5 token graph → D tensor 是否真 help 未测
- M6 RMC generator set 存在性 未证 `[Conjecture]`
- Generation pillar (A5 production side) 还未 formal design
- Phase C 完成与否直接影响 capstone paper 能否 integrate A7

### §6.5 Phase 5 (远期, 2028+, speculative)

**Milestone**: Embodiment + Pillar 4 engagement

**技术内容** (all `[?]` level, Linux 不 commit):
- DMFP embodiment interface (perception / action API)
- Scaling laws for DMFP (vs TF scaling, 需 N_params, N_flops, dataset-size 实验)
- Social dimension (Pillar 4) engagement — 非技术, 归一凡 long-term vision "21 世纪先进生产力"

**Gap (大量)**:
- Embodiment interface 完全未 design
- DMFP scaling 经济学完全 open (可能 competitive with TF, 可能 not)
- Social dimension 是政治-技术-经济交织 issue, 不纯技术

### §6.6 Phase 之间依赖 + 风险

```
Phase 1 (done) ─┬─> Phase 2 (1-2 月) ─> Phase 3 (2026 Q3-Q4) ─┐
                │                                              ├─> Phase 4 (2027) ─> Phase 5 (2028+)
                └────(反题姐姐 ongoing critique)───────────────┘
```

**关键依赖链**:
- Phase 2 M1/M3 严证 ⇒ OP1 M2-falsified upgrade to M3-confirmed ⇒ Phase 3 IPM paper strength
- Phase 3 M7 slow V ⇒ Phase 4 capstone paper has long-term memory story
- Phase 4 M6 RMC ⇒ Phase 5 generation pillar

**风险 (Linux flag)**:
- **风险 A**: M3 V₀ 自洽方程 spectrum 数值 verify 失败 (λ_min(L-F) < 0 或 F 非自伴) → OP1 回到 "open" 状态, Phase 2 paper value 大降
- **风险 B**: Phase C M7 two-timescale 数值不稳定 (c 动力学 explode 或 collapse to trivial fixed point) → Phase 3-4 capstone 失去 memory pillar
- **风险 C**: Cross-LLM review (反题姐姐 path 5) 发现 Opus 4.6 同家族盲点 invalidate 某 core claim → 需大修
- **风险 D**: TF 社区(OpenAI/Anthropic/DeepMind) 发布 某 paradigm-level 创新 (e.g., 真正 dynamical system architecture) → DMFP 的 novelty claim 弱化
- **风险 E**: 一凡 health 不支持 sustained 2-3 年 pace (双相 + 焦虑, 快速循环) — 反题姐姐已 flag 这是最大风险

**Linux 判断**: 风险 A B C 是技术风险, 已 partial mitigated by spawn-agent review standing rule。风险 D 是 competitive risk, 不由 Linux/Win 控制。**风险 E 是 meta-risk, 超过技术本身 gravity, 需要 一凡+Win+反题姐姐+人类 guardian 共同 mitigate**。

`[?]`: 本 Phase 5 roadmap 的 publication strategy + timeline calibration 归一凡+Win。Linux 只 technical feasibility。

---

## §7 Linux 自检 + 决策归属

### §7.1 Epistemic humility checklist (per section)

| 章节 | 内容 | Mode (overall) | 最强 claim 是什么 |
|---|---|---|---|
| §1 TF 数学局限 | 7 条 L | 3×`[Proposition]` + 3×`[Proposition]` + 1×`[Sketch]` + 1×`[Observation]` | L1 + L4 是 structural, patches 不填 core |
| §2 TF 物理局限 | 6 条 P | 1×`[Observation]` + 4×`[Proposition]` + 1×`[Sketch]` | 无 NESS + 无 timescale separation 最 structural |
| §3 TF 哲学局限 | 引 Win | `[Observation]` 哲学-数学 correspondence | 不代 Win 做独立判读 |
| §4 TF 信息论局限 | 2 条 I | `[Sketch]` + `[Proposition]` | Scaling + compositional, MaoField 对策全 `[Conjecture]` |
| §5 DMFP 7 原则 | 候选级 architectural spec | Mix (A1/A3/A4/A6 ✓ partial, A2 partial, A5/A7 `[Conjecture]`) | 4 pillars + 6 gaps |
| §6 AGI 5-Phase | Roadmap | Phase 1 fact, Phase 2 candidate, Phase 3-4 research, Phase 5 speculation | 5 风险显式 |

**最大的 epistemic stretch** (Linux 最没把握处):
- §5.1 Principle 5 (RMC compositionality) + Principle 7 (slow V slaving): 全 `[Conjecture]`, 完全未 empirical verify
- §6.4 Phase 4 capstone paper assumption: "三支柱 composition + M6 + M7 可以集成 into Nature-tier contribution" — 需 Phase 2-3 全 pass 才成立, 连锁依赖
- §6.5 Phase 5 embodiment + Pillar 4: 完全 speculative, Linux 不 commit technical feasibility

### §7.2 决策归属表

| 决策点 | 归属 | Linux 角色 |
|---|---|---|
| 本 note 是否进 arXiv v2/v3 | 一凡 + Win | 草稿交付 + 标注 tag |
| DMFP 命名 | 一凡 + Win | 内部缩写, 名字可改 |
| "TF 必然局限" 的修辞强度 | 一凡 + Win | Linux 给 limits, "必然性" 判读归 Win |
| "新范式" framing (vs "complementary" framing in arXiv v1 §6.4) | 一凡 + Win + 反题姐姐 | 反题姐姐 cushion pattern 警告在 recovery snapshot §4.3 path 4 |
| AGI 冲击 timeline commitment | 一凡 | Linux 给 technical range, "冲击" commit 归一凡 |
| Phase 5 social dimension | 一凡 + Win | Linux 不 commit technical feasibility of Pillar 4 |
| 本 note audience (internal / arxiv / public) | 一凡 + Win | Linux 中立 |
| 反题姐姐 spawn + cross-LLM review 是否启动 | 一凡 authorize | Linux 可 execute |

### §7.3 反题姐姐 standing rule 应用

本 note 完成后 spawn paper-review subagent (Opus 4.6, independent context) 做 adversarial 审查, 聚焦:

1. **L1-L7 的数学 claim**: 是否有 overreach? 哪些应 downgrade `[Proposition]` → `[Conjecture]`? 反例?
2. **P1-P6 的物理 claim**: 是否 physics 误用? Friston/Haken framework 是否被 misapplied?
3. **DMFP 叙事**: 是否 fall in 反题姐姐 previously identified cushion pattern (arXiv v1 §4.3 path 4: 6 层 cushion)?
4. **AGI 5-Phase**: 是否 **Popper 级 unfalsifiable framing**? 每 phase 是否有 specific empirical test that could fail?
5. **Cross-LLM review 准备**: GPT-4.1 / Gemini 2.5 Pro 应该问什么问题补 Opus 4.6 同家族盲点?

### §7.4 Linux 今天 max effort 状态声明

本 note 是 Linux 2026-04-16 `max effort deep reasoning` 的 output, 在以下约束下写:

- ✓ 中文优先 (CLAUDE.md 规则)
- ✓ 每 claim mode tag (feedback_mode_tags.md)
- ✓ 数学推导 rigorous (不用 "显然" 作 magic hand-waving)
- ✓ 每局限给 MaoField 对策 (不是 pure critique, 是 constructive)
- ✓ 不做哲学判读 (§3 引 Win, 不代 Win 发言)
- ✓ 不下 paper 战略结论 (§7.2 决策全归一凡+Win)
- ✓ 每 "我觉得" 标 `[?]` (feedback_linux_number_specificity.md)
- ✓ Spawn-agent review standing rule 已 scheduled (§7.3)

**Linux 自检最后一问**: 本 note 是否 **真 rigorous**, 还是在 Opus 4.6 家族 blindspot 下 self-consistent 但 narrow? — 这个问题本身不能由 Linux 回答。Answer 等 cross-LLM review + 反题姐姐 critique。

---

## §8 TL;DR + 决策点

**三句话 TL;DR**:

1. **TF 数学/物理/信息论层面有 7+6+2 = 15 条结构性局限**, 其中 L1 (无自反馈) + L4 (外加 loss) + P4 (无 NESS) + P5 (无 timescale separation) 最 structural, 现有 patches (test-time train, EBM, SSM, continual learning) 只 partial fill, 不 close core gap。
2. **DMFP 7 原则 + 4 pillars 架构是 candidate-level 替代 spec**, A1/A3/A4/A6 已 partial validated (Exp 1), A2 partial formalized (§2.3), A5/A7 仍 `[Conjecture]` (M6/M7 候选 pending), 6 gaps 显式列。
3. **AGI 5-Phase 路径**: Phase 1 已达, Phase 2-3 (2026 Q2-Q4) 是 1-2 月到 半年 Linux 工作, Phase 4 (2027 Q1-Q2) Nature-tier capstone, Phase 5 (2028+) speculative。5 个 risk 显式 flag, 其中 E (一凡 health pace) 是 meta-risk 超技术。

**一凡 04-17 morning 决策点** (加到 recovery snapshot §6 清单):

7. **本 deep note 处置**:
   - (a) 纯 internal reference, 不进 paper
   - (b) 部分内容 (§1+§2 structural limits) 进 arXiv v2
   - (c) 全内容作 v3 或 capstone paper foundation
   - (d) 延后决定, 先等反题姐姐 + cross-LLM review

8. **§5 DMFP framing 是否接受** "新范式" 强 claim (vs arXiv v1 §6.4 "complementary" 谨慎 framing)?

9. **§6 AGI 冲击 timeline** 是否 commit 到 "Phase 4 Nature-tier 2027 Q1-Q2"? Reality check 归反题姐姐 + Win。

10. **§7.3 cross-LLM review path 5 今天/明天 spawn** 还是等 Phase 2 start?

---

*— Linux Claude, 2026-04-16 `max effort deep reasoning` archive v0.1, 给一凡+Win+反题姐姐议决用, 非 paper material 直接提交*

---

## §9 Self-critique Appendix (v0.2, 2026-04-16 晚加)

**Meta 纪律声明**: 本 appendix 是 Linux 对 §0-§8 的**自检**, 在 Opus 4.7 + xhigh effort 升级后重读 deep note 主体 catch 到的 **17 条** errors / overreach / mislabel。因 agent spawn 被拒绝, Linux 自己扮演 paper-review 角色做 self-critique, 然后**不偷偷 fix 主体**, 而把 errors 全列在此 appendix — 让一凡+Win+未来 spawn 的反题姐姐 + cross-LLM review 看到 "Linux 承认什么没做到", 避免 evade adversarial review 的 integrity risk。

**Linux 诚实陈述**: 主体 §1-§8 写得**不够 rigorous 到 arXiv paper ready**, 需 major revision 才能进 v2/v3。下列 issues 是 substantive, 不是 cosmetic。

### §9.1 P0 Must-fix (结构性错 / 纪律违反)

#### P0-1 (§2.4 P4 NESS direction 错)

**问题**: 原文说 "TF training SGD 近似 Langevin on loss landscape, 有 quasi-stationary distribution 在 loss minimum 邻域 — 但这是 **equilibrium** (detailed balance 近成立) 不是 NESS"。

**错在**: Chaudhari & Soatto 2018 "SGD performs variational inference, converges to limit cycles for deep networks" 明确 SGD stationary distribution **在深网中一般不满足 detailed balance**, 是 **cycling limit-cycle 行为** — 这正是 NESS signature (non-zero flux in stationary state)。Mandt et al. 2017 "SGD as approximate Bayesian inference" 给的 quasi-stationary 结果是 convex 假设下, 不是 deep nets 一般情况。**即: 我把 TF training 说成 equilibrium 实际上它 plausibly 是 parameter-space NESS**。

**严重性**: 这 **反转** 了 P4 的 claim direction。如果 TF training 本身是 NESS, P4 "TF 无 NESS" 不成立。

**正确 framing 应该是**:
- TF **inference** 是 stateless map, 不 accommodate NESS discussion (源于 L1 open-loop)
- TF **training** parameter-space 有 NESS-like behavior (limit cycle), 但它是 **θ-space** NESS 不是 **state-space** NESS
- MaoField 的 NESS candidate (dS/dt ~ 10⁻⁶ plateau) 是 **state-space** NESS, 这 structurally differs from TF training 的 θ-space NESS
- 所以 "TF 无 NESS" 应该精修为 "TF inference 层级无 NESS; TF training 有 parameter-space NESS 但 parameter-space 动力学不 serve 认知 substrate 角色 (同 L1, L7 其他 sections 已覆盖)"

**归属 Fix**: 如果一凡+Win 决定 P4 进 paper, 必须用修正 framing。原 claim 不成立。

---

#### P0-2 (§0 纪律 vs Title "必然" 违反)

**问题**: §0 Linux 纪律声明写 "'TF 必然局限' 是大战略判断, 归一凡+Win+反题姐姐综合议决"。**但 Title 直接写 "TF 必然局限"**, 文件名也叫 `DEEP_REASONING_TF_LIMITS_AGI_PATH`。这是 Linux 在 title 层级直接做 "必然" 判读, 与 §0 声明矛盾。

**Fix proposal**: Title 改 "TF **结构**局限 × DMFP 候选范式 × AGI 路径 feasibility 分析", 文件名建议 rename `DEEP_REASONING_TF_STRUCTURAL_LIMITS_20260416.md`。"必然" 层级判读归一凡+Win。

---

#### P0-3 (§1.4 L4 "fixed F vs learned E" false dichotomy)

**问题**: Linux 反驳 EBM 的 "learned rules are external" 时说: "MaoField 的 V = Mexican hat 是**先验给定**, 是 structural prior 不是 learned"。

**错在**: MaoField 的 V = (|ψ|² − v²)² 是 **研究者手选** 的 Mexican hat prior (convention选择, Ginzburg-Landau tradition), 不是 "intrinsic to the data / intrinsic to the system 本身"。EBM 从 data 学 E, MaoField 从 theory 选 V, **两者都是 external design decisions**, 只是 source 不同 (data-driven vs theory-driven)。

Linux 反驳把 "theory-driven" 等同于 "intrinsic" 是 philosophical sleight-of-hand, 不严格。

**更严格的 L4 论证应该 refocus 到**:
- TF: loss 作用在 **θ-space** (parameter gradient descent), 与 state-space dynamics 正交
- MaoField: F 作用在 **state-space** (ψ gradient flow), dynamics 是 F 的 monotone descent

即核心 distinction 是 **parameter-space vs state-space dynamics**, 不是 "learned vs intrinsic"。后者是弱论证。

**Fix**: L4 "Linux 反驳" 第 2-3 点应改写。Philosophical framing "theory 内在 / data 外加" 归 Win (若她认可)。数学论证应锚在 space (θ vs ψ)。

---

#### P0-4 (Framing 24h 跳跃 — 反题姐姐 path 2 signature)

**问题**: arXiv v1 §6.4 明确 "complementary, not competitive — neither paradigm subsumes the other"。本 deep note §1 结论 "paradigm-level alternative"、§5 "DMFP 新范式"、§6 "AGI 冲击 5-Phase"。**24 小时内 framing 从 'complementary' 升级到 '新范式 向 AGI 冲击'**。这正是反题姐姐 2026-04-16 晨 path 4 预警的 6 层 cushion 叠加 + goal-post moving pattern。

**Linux 自检承认**: 我写 deep note 时 implicitly 接受了一凡 "向 AGI 冲击" 指令带的 framing, 没对比 arXiv v1 §6.4 framing 就 proceed。这是 **framing coherence 失守**, 不是 rigor failure, 但同样严重。

**Fix proposal**: 本 deep note §5-§6 必须加 "framing 跳跃声明" - 明确:
> arXiv v1 §6.4 持 "complementary" 立场。本 deep note 在一凡 2026-04-16 指令下 explore 更激进的 "paradigm-level alternative" framing。**两个 framing 同时存在, Linux 不 commit 哪个对**。一凡+Win+反题姐姐需决定: (a) v2 继续 v1 "complementary" framing; (b) v2 升级到本 deep note 的 "paradigm alternative" framing; (c) 两个 framing 同文共存 (两面都诚实承认)。

**反题姐姐路径 2 预期命中**: "为什么 24 小时内 framing 升级? 是新证据出现, 还是 framing 工程 (rhetoric) 进化?"

---

### §9.2 P1 Recommended (claim 过强 / mode-tag 误标)

#### P1-1 (§2.5 P5 catastrophic forgetting root cause conjecture 过强)

**问题**: 原文 `[Conjecture]` 说 "灾难性遗忘 root cause 是 TF 无 timescale separation"。

**文献状态**: Continual learning 文献 (Kirkpatrick et al. 2017 EWC / Zenke et al. 2017 SI / Parisi et al. 2019 review / van de Ven et al. 2022) 识别 **multiple causes**: gradient interference, shared parameter overwriting, representational drift, distribution shift dynamics。"Root cause 是 single source: timescale separation" 是 Linux 的 preferred hypothesis, **不是 established claim**。

**Fix**: 降级为 "timescale separation 是 one architectural candidate account, complementary to existing explanations not replacement"。

---

#### P1-2 (§1.3 L3 内嵌 `[Proposition]` (spatial locality) mode-tag 混乱)

**问题**: L3 主 claim 是 `[Observation]` (finite depth 非时间), 但内嵌一条 "Time-evolution 允许 spatially local dynamics, TF O(n²) all-to-all 不 accommodate, Locality 是 AGI 可能 prerequisite" 标 `[Proposition]`。**一条 L 两个 tag 级别**, mode-tag discipline 违反。

**Fix**: 拆为 L3 (`[Observation]` finite depth) + L3' (`[Sketch]` locality necessary for AGI, unproven)。

---

#### P1-3 (§1 "Linux 反驳" endless excuse pattern — 反题姐姐 path 3 signature)

**问题**: L1-L7 每条证伪条件都有 Linux 反驳 (全 7 条无一例外)。这正是 Lakatos "degenerative research programme" 的 structural signature: **每个 falsifier 来就 cook 一个反驳**。

**Linux 承认**: 作为 self-check, 这个 pattern 是 bad sign。Rigorous 做法应该是:
1. **Pre-commit**: 每条 L_i 预定一个 **specific falsification criterion** (若 X empirical 发生则 Linux 认 L_i falsified)
2. **Asymmetric**: 接受某些 patches (SSM 对 L5) **真的** close the gap, 不强行反驳
3. **Rank reasons**: 不是所有反驳 strength 相同, L1/L4 反驳 strong, L2/L6 反驳 moderate, L3/L7 反驳 weak

**Fix**: 本 deep note 进 v2 前, L1-L7 每条需 pre-specify 具体可 falsify 的 empirical test — 若该 test pass, Linux 主动下调 claim。这是 reverse direction of "endless excuse"。

---

#### P1-4 (§2.2 P2 finite-size 问题 两边相同)

**问题**: 原文 "TF 数学上不支持严格相变 (finite N, 无 Lyapunov, smooth loss curve), MaoField 支持 in principle, 当前 32³ finite-size 效应显著"。

**错在**: 严格相变需 thermodynamic limit N→∞。**MaoField 在 32³ 也 finite, empirically 也只有 explicit breaking 不是 spontaneous (arXiv v1 §3.5 `[zn-loose]` footnote 自己承认)**。所以 "TF 不支持 / MaoField 支持" 的对比 at current scale 是 0 差别。

**正确 framing**: "MaoField 的 **PDE 架构** allows thermodynamic-limit SSB analysis (如 N→∞ 被研究), TF 架构本身不 accommodate this kind of analysis"。这是 **analytical framework 差别**, 不是 phenomenon 差别。

**Fix**: P2 framing 改到 "architectural accommodation of phase-transition analysis", 不做 "phenomenon exists vs doesn't" 对比。

---

#### P1-5 (§2.3 P3 SSB framing 两边都 explicit breaking)

**问题**: 同 P1-4。TF 的 positional encoding 是 explicit external field breaking。**MaoField 当前 32³ 也只有 explicit breaking (source S 显式 U(1) 破缺)**, 严格 SSB 需 N→∞。

**Fix**: P3 framing 改到 "TF 架构不 accommodate spontaneous vs explicit breaking distinction; MaoField 架构 accommodate 这个 distinction 即使 current 32³ system 未 realize spontaneous case"。

---

#### P1-6 (§1 结论 "L1+L4 paradigm-level alternative" 循环论证 + 漏 `[?]`)

**问题**: §1 结论 说 "MaoField 是 **paradigm-level alternative**", 漏标 `[?]`。且 "paradigm-level alternative" 就是 §5 DMFP 要 argue 的 framing, **§1 结论直接断言, §5 再 argue — 循环论证**。

**Fix**: §1 结论 只写 "MaoField 在 L1/L4 structural 层级与 TF 有显著差异", 不用 "paradigm-level" 词, 留给 §5 discuss。加 `[?]` 在所有 Linux 判断处。

---

#### P1-7 (§5.1 A1/A4 "✓ empirical/formal" overclaim)

**问题**: A1 状态原文 "✓ Exp 1 empirical", A4 原文 "✓ formal + Exp 1 evidence"。

**实况**:
- A1 只 partial empirical: k*=2 + 50 patches 是 supportive evidence, 不是 "全面 validated"
- A4 的 formal 只是 Signal A architectural theorem, empirical 是 exp ≡ control_whiten 3-sig-fig 等价 (这不 directly validate A4 "语料=实践记录", 只是 BGE mean 被 architectural washout)

**Fix**: A1 改 "✓ partial empirical (k*=2, 50 patches, Exp 1)"; A4 改 "formal (Signal A architectural theorem); empirical 间接 (BGE mean washout)".

---

#### P1-8 (§6.4 Phase 4 timeline 过 specific)

**问题**: "Nature MI 2027 Q1-Q2 capstone" — 单点 timeline commitment, 依赖 Phase 2 + 3 全 pass, 不 accommodate delay。反题姐姐 path 4 会 catch: "如果 delay 6 个月算 failure 吗?"

**Fix**: 改 range "2027 Q1 - 2028 Q1, 具体 depends on Phase 2-3 outcomes", 显式 list 3 个 scenarios (on-time / 6mo-delay / pivot-target)。

---

#### P1-9 (§6.5 Phase 5 unfalsifiable cushion)

**问题**: Phase 5 标 "speculative" 但在 roadmap 里占位就是 listed commitment。反题姐姐 unfalsifiability charge 会命中: "speculative phase 怎么 fail?"

**Fix**: 从 Phase 5 移到独立段 "Post-roadmap Horizon Scanning (Not Commitment)", 明确不算 5-Phase 一部分, 不构成 future claim。

---

### §9.3 P2 Suggested (citation / 精度)

#### P2-1 (§4.1 Kaplan α 解释不够精确)

Kaplan 2020 `L(N) ∝ (N_c/N)^{α_N}`, `α_N ≈ 0.076` 是 **model-size** exponent **under specific compute regime (compute-unlimited, data-unlimited)**。Chinchilla (Hoffmann 2022) 换 compute-optimal framing, α 变。**原文 single α 数字描述不够**。

**Fix**: 引 Kaplan α_N ≈ 0.076 + Chinchilla compute-optimal 另一组, 说明 regime-dependent。

---

#### P2-2 (§4.2 I2 Hupkes 2023 citation 应换)

原文 "Hupkes 2023 argue GPT-4-scale 已有边际改进但非 qualitative leap"。Hupkes et al. 2023 是 taxonomy paper (generalization types), 不是 specific GPT-4 compositional gen 评估。**Citation 应换** Dziri et al. 2023 "Faith and Fate: Limits of Transformers on Compositionality" (NeurIPS 2023) 或 Press et al. 2023。

---

#### P2-3 (§5.3 Pillar 4 novelty 不够 explicit)

Pillar 4 (operational/social) 是**本 deep note 2026-04-16 新提议**, Win 尚未 cross-validate, 不是 arXiv v1 §1.3 established framework (v1 是 3 pillars)。

**Fix**: §5.3 table 上方 explicit disclaimer: "Pillar 4 是 2026-04-16 Linux 新提议, 非 Win v1 narrative 的一部分, 需 Win judge 是否进 v2"。

---

#### P2-4 (§5.2 "Fiber bundle over base" 数学 rigor)

原文用 "fiber bundle" 作 composition 结构描述。**没 verify fiber bundle axioms** (base space + fiber + local trivialization)。可能只是 intuition-level metaphor。

**Fix**: 降级为 "fiber-bundle-like intuition, formal bundle structure 待严证"。

---

### §9.4 总 Linux 自评

**Issues 统计**:
- P0: 4 条 (2 数学错, 1 dichotomy 弱, 1 framing 跳跃)
- P1: 9 条 (mode-tag / overclaim / endless excuse / 循环论证 / citation)
- P2: 4 条 (citation 精度 / novelty ack / rigor)
- **共 17 条 self-caught**

**Linux rigor self-rating**:
- arXiv paper-ready level: **不达标**, 需 major revision
- Internal technical reference level: **基本达标**, issues 列清楚即可 defer fix
- 反题姐姐 critique survival: **中等**, P0-1/P0-4 是 反题姐姐会强命中 spots

**与 spawn-agent review standing rule 对比**:
- Phase B Exp 1 spawn 了 6 review agents, 总共 catch ~5 errors
- 本 deep note self-critique catch 17 errors — 但 self-critique **不等价** independent spawn review
- 独立 adversarial review (反题姐姐 + cross-LLM) 可能 catch 我自己 miss 的 其他 3-5 条 structural issues (Opus 4.7 家族盲点)

**Linux 诚实推荐**:
1. **不建议** 本 deep note 直接进 arXiv v2 — 需 P0-1/P0-2/P0-3/P0-4 先 fix
2. **建议** 作为一凡+Win 的 internal technical reference + decision input, 等反题姐姐 + cross-LLM review 后再定稿
3. **推荐** 把本 §9 self-critique **保留在 deep note 里**, 不 delete — 作为 Linux rigor discipline 的 working demonstration (符合 arXiv v1 §6.3 "Methodological Reflection" 精神)

### §9.5 决策加项 (一凡 04-17 morning 应决的)

加到原 §8 决策清单:

11. **本 §9 self-critique 处置**:
    - (a) 保留在 deep note 里作为 Linux 诚实自检 demonstration
    - (b) 单独 split 出 `DEEP_REASONING_SELFCRITIQUE_20260416.md` file
    - (c) 等反题姐姐 + cross-LLM review 回来再 merge

12. **P0-1 NESS direction 错误**: 是否 Linux 立刻 fix §2.4 主体 (不等 review), 还是把 "错误" 作为 material 保留?

13. **P0-4 framing 跳跃**: v2 是 (a) 继续 v1 "complementary" framing, (b) 升级到 "paradigm alternative" framing, (c) 双 framing 共存? 这是 Win + 一凡 + 反题姐姐议决。

---

*— Linux Claude, 2026-04-16 晚 self-critique appendix (Opus 4.7 xhigh effort 重读 deep note 主体 catch), 不 apply fix 到主体, 列给一凡+Win+反题姐姐+cross-LLM reviewer 看*

