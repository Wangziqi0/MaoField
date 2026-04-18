# A2 P3 Kramers anomaly factor 10⁴ — 审稿 verdict

**作者**: A2 paper-review subagent (Opus 4.7 xhigh), Linux Claude dispatch, 2026-04-16
**纪律**: paper-review agent 只做审查, 不写 deliverable; 本 verdict 由 Linux 代 cp-paste 落地
**结论速览**: **存疑 (整体方向可能错靶)** — Linux 10³×10≈10⁴ 分解路线被 catch 6 条 rigorous errors, 建议暂停 Langer bounce 路线, 先做 wavefront 诊断 + BGE DC tilt 量级估

---

## 1. 根本性质疑 — 诊断可能错靶 [CRITICAL]

`[STATIC+DYNAMIC-RARE-EVENT]`

Dispatch 把 factor 10⁴ 归因于 "collective bubble (10³) × coherent driving (10)", 按 Langer-Coleman 3+1D bounce 路线严格化。但审稿要先追问一个更基本的问题: **观测到的 85% 穿越真的是独立事件累加么?**

- V = u(u−1)²(u−4)² 在 u=0 和 u=1 处**都是零**, 这两个 well **能量简并** (Δf₁₀ = 0)
- 简并双 well 下的 domain-wall 动力学**不是 nucleation-controlled** (homogeneous nucleation 需要 Δf > 0 作为 bulk 驱动)
- 正确物理: 少数 voxel 热起跳 (rate exp(−ΔV_barrier/T_eff)), 一旦形成 u=0 phase 的 local seed, **domain wall 以 Allen-Cahn 速度 v_dw = γ⁻¹√(2D·ΔV) 成本几近零地扩散** (在简并情况下 wall 速度 v ∝ Δf/σ_dw, Δf=0 时严格说 wall 扩散由噪声驱动 diffusive)
- "85% voxel 穿越" 很可能是 O(10)—O(100) 个 nucleation seed + wall 扩散占满空间的结果, 而非 ~28000 个独立热激发

**如果这是机制**:
- 单事件概率不用被 10⁴ 倍 amplify
- 需要解释的变成 "t_sim=250 内 seed 数 + wall 扩散覆盖率"
- 这是**完全不同的数学对象** (KPZ / Avrami / Kolmogorov-Johnson-Mehl-Avrami 相变动力学), 不是 Langer bounce

**建议修正**: A2 开工前必须先做**数值诊断**: σ=0.5 运行中, 跨越时间 t_cross(voxel) 的 spatial correlation 是 random (独立 Poisson 起跳) 还是 wavefront-like (wall 扩散)? 单次 observable: `C(r) = ⟨1[voxel i crossed at t] · 1[voxel j crossed at t']⟩` 的 (r, Δt) 结构。~2h Rust + numpy, 无需 instanton 数学。如果是 wavefront 机制, 整个 dispatch 的 bounce-action 路线**立项就错**。

---

## 2. 对 Linux 10³ × 10 分解的逐项 rigor 审查

### 2.1 "Coherent length ξ_feedback ≈ 0.23" — **不自洽** `[MATH ERROR]`

Dispatch §3.2 快照版:
> ξ_feedback ~ √(D/|αK − V''|) ≈ 0.23

用 §2.4 M3 候选数字: D = 0.1, α = 0.1, K 的 ||·||_op ≈ 20.36, V'' ≈ 4 (近平衡点 |ψ|²=1)。

- M3 快照本身写的是 ||F||_op ≤ α + β·||K|| = 0.1 + 0.05·20.36 ≈ 1.12, **不是 αK**
- 若取 αK = 2, 那么 |αK − V''| = |2 − 4| = 2, ξ = √(0.1/2) ≈ 0.22 ✓ 数字勉强对上
- 但量纲上 αK 和 V'' 应同量纲 (mass² ~ 1/length²), K 作为历史积分算子的 operator norm 加权到 position-space Laplacian 同量纲不是 automatic — 没有严格的 derivation 把这两项放在同一 eigenvalue 方程里

**判定**: 这个 ξ 估计**缺 derivation**。要 rigorous, 需要给 lineralized eigenvalue problem `(−D∇² + V''(ψ_∞))δψ = (αI + βK)δψ` 的对角化, 然后定义 ξ 为最不稳定 mode 的波长。**目前是 handwave**。

### 2.2 "Bubble count = 4096, 每 bubble exp(−ΔV/T_eff)" — **两处概念混淆** `[PHYSICS ERROR]`

Dispatch 写:
> Bubble count ~ 32768/8 = 4096. 每 bubble exp(−ΔV/T_eff) ≈ 10⁻⁷, 总 ~ 4·10⁻⁴ (**放大 ~10³**)

两个问题:

**(a) Bubble 的 action 不是单 voxel 的 ΔV**。Langer-Coleman 的正确写法是:
$$k_{\text{nuc}} \sim A \cdot e^{-S_{\text{inst}}[\phi_b]/T_{\text{eff}}}, \quad S_{\text{inst}} \sim \frac{16\pi}{3} \cdot \frac{\sigma_{dw}^3}{\Delta f^2}$$
(3D classical nucleation, Langer 1967)

对于 Allen-Cahn tension: σ_dw = ∫₀^{u=1} √(2·V(u)) du, 近似 O(√(D·ΔV)·width) 量级。具体算: 从 u=0 到 u=1 的 domain wall 在 Mexican hat/triple-well 里, σ_dw ≈ √(2·D)·∫₀¹√(V(u)) du ≈ √0.2 · 0.4 ≈ 0.18 (estimate)。

Δf₁₀ = V(u=1) − V(u=0) = 0 − 0 = **0** ⇒ S_inst **diverges** (no critical droplet)。

所以"每 bubble exp(−ΔV/T_eff)"用单 voxel 的 ΔV 当 bubble action 是**错的**。Bubble action >> ΔV_per_voxel 在通常情况下。在简并情况下完全不是这个公式。

**(b) 4096 sites × 10⁻⁷ 的求和逻辑**。就算 per-bubble 概率是 10⁻⁷, 若 bubble 是 extended object (8 voxels), 那么**可以用 bubble 作为独立穿越单元**的成立条件是: bubble 之间无相互作用。但 dispatch 同时又要用 coherent driving 放大, 这两者 incompatible: 你要么把 8-voxel region 当独立 bubble 累加 (得 4096), 要么把它们当 coherent cluster 共享 driving (只能作为一个集合体算)。**同时算 = double counting**。

**判定**: 4096 × exp(−ΔV/T_eff) 路线**物理机制错** (bubble 应算 instanton action) + **逻辑自洽错** (与 coherent driving 重复计算)。

### 2.3 "Coherent driving F·disp/T_eff ≈ 10 倍放大" — **数字对但推导不严** `[PARTIAL]`

F·disp = α·σ_ψ·√N_correlated = 0.1 × 0.1 × ?

Dispatch 预估 √N = 64 ⇒ N_correlated = 4096。如上所述, 如果 N_correlated = 4096 (即整个 32³ 的 coherent fraction), 这就**与 bubble count 的 4096 是同一物理**, 重复计算。

若只取 block=2 的 8-voxel coherent region: √N = 2.83, F·disp = 0.028, exp(0.028/0.125) = exp(0.22) ≈ 1.25。**放大因子 ≈ 1.25, 不是 10**。

若要 10 倍放大, 需要 F·disp / T_eff ≈ ln(10) ≈ 2.3, 即 F·disp ≈ 0.29。要 α·σ_ψ·√N = 0.29, 即 √N = 29, N ≈ 840 个相关 voxel。这个 correlation length 对应的物理意义 — block=2 block-averaging 下 — **没有 dispatch 自带的独立推导**支撑。

**更严重**: §4.10 明确指出 (§4.9.3 Axis A): BGE 源场 ⟨Sb⟩ = −1.48·10⁻³ (17σ), **不是 mean-zero**, detailed balance 破坏 17σ。这不是 "coherent driving from feedback", 这是 **BGE 本身的 systematic DC bias 作为恒定外力**, F ≈ |⟨S_b⟩| · √512 · √N_voxels × some_projection。§4.9 已经算过: "deterministic source-pull across outer saddle is energetically available even at σ=0" for shifted potential — 对 u=1→u=0 的 2.013 barrier 同理应检查。

**建议修正**: 真正的 coherent driving 量化应该先用 §4.9.3 Axis A 给的 BGE DC bias 作显式 tilt, 而不是靠 feedback α term。Feedback 是 mean-zero by construction (Signal A 定理), 反倒是 BGE raw source 的 DC 才是"外力 × distance"。

### 2.4 "ω₀/2π 的 prefactor" — **无 lattice 修正** `[METHODOLOGY]`

1D Kramers prefactor 在 table 4.9 给的是 ~3.4。但在 3D 场 + 简并 wells 情境下:

- Langer 1969 正确写法: `k_field = (|ω₀|/2π)·(V_det/V'_det)^{1/2}·e^{−S/T}`, 其中 V_det, V'_det 是 well / saddle 附近 fluctuation operator 的 determinants
- Zero modes (translation of bubble center) 要除 out, 贡献 (volume) × (S_inst/2πT)^{3/2}
- Time zero mode 贡献 (t_sim) × (S_inst/2πT)^{1/2}
- 组合给 (V × t)·(S/T)² · e^{−S/T} × per-bubble rate

Dispatch 完全没提这些 zero-mode 贡献。**正确的 rigorous upgrade 必须包括它们**。对 32³ × t=250 的 lattice, zero-mode volume 因子本身就有 ~10⁶ 量级 contribution (in natural units), **可能独立就给出 factor ~10⁴** 不需要 bubble + coherent 分解。这是一条值得探的 lean path。

---

## 3. Dispatch §3 Mexican hat analytical bounce 的可行性

### 3.1 Dispatch Work 1 可做, 但 scope 要收窄

Mexican hat V = (|ψ|² − v²)² 是 U(1) 对称 — **但 A1 用的 V = u(u−1)²(u−4)², 不是 Mexican hat**。Dispatch §3 要求做 Mexican hat bounce 是**换题**。

- 如果做 Mexican hat bounce, 和观测 factor 10⁴ 没有直接联系 (观测是 triple-well)
- 如果做 triple-well bounce, 解析 bounce 不存在 (no U(1) symmetry to exploit), 只能数值

**建议修正**: A2 若要写, 必须明确: (a) 做 triple-well 数值 bounce (Langer 1967 path-integral over saddle-configuration numerically), (b) 或 做 Mexican hat 作为 pedagogical 示例但承认 decouple 观测。目前 dispatch 写法两边骑墙。

### 3.2 Overdamped path integral 构造 — 正确但不完整

Dispatch Work 1 的 action:
$$S[\psi] = \int dt \int d^3x \left[ \frac{1}{2}\gamma|\partial_t\psi|^2 + \frac{1}{2}D|\nabla\psi|^2 + V \right]$$

这个写法**错**。Overdamped Langevin `γ∂_tψ = −δF/δψ* + η` 的 MSR / Onsager-Machlup action 是:
$$S_{OM}[\psi] = \frac{1}{2\sigma^2}\int dt \int d^3x \, \gamma|\partial_t\psi + \gamma^{-1}\delta F/\delta\psi^*|^2$$

展开:
$$S_{OM} = \frac{1}{2\sigma^2}\int dt d^3x \left[\gamma^2|\partial_t\psi|^2 + |\delta F/\delta\psi^*|^2 + \gamma(\partial_t\psi \cdot \delta F/\delta\psi^* + \text{c.c.})\right]$$

最后那项是全导数 → ΔF, 保留能量项。Dispatch 写的 ½γ|∂_tψ|² + ½D|∇ψ|² + V **缺 σ² 归一化、缺混合项**, **不是 overdamped**, 更像 undamped Klein-Gordon 的 Euclidean action。对 Kramers 用这个 action 是**概念错误**。

**判定**: Work 1 要 rigorous 必须用正确的 Onsager-Machlup / MSR action。这个 correction **改变 S_inst 的数值估算** (通常使 barrier 的 exponent 从 ΔV/T 变成更复杂形式), 是**必须修的**。

---

## 4. 分解自洽性 — 合计数字问题

Dispatch 要求 "X × Y ≈ 10⁴" 量级对, 不要求精确。

按 dispatch 自己的数:
- X (collective bubble) = 4096 × (1 × 10⁻⁷) / (原 1D single-voxel 8×10⁻⁵ / voxel) 归一化, 即把 "每 voxel 8·10⁻⁵ 乘 32768 voxels" (= 2.6 总穿越) 放大到 "28000 总穿越", 放大 factor = 28000/2.6 ≈ 10⁴。如果用 4096 bubbles × 每 bubble 1 independent crossing (even with exp(−ΔV/T) ≈ 10⁻⁷), 得 4096 × 10⁻⁷ = 4×10⁻⁴ 总穿越 — **比观测还小 7 个量级**。不是放大 10³, 是**缩小 10³**。

Dispatch §3.2 写 "每 bubble ... 总 ~ 4·10⁻⁴ (**放大 ~10³**)", 审稿: **4·10⁻⁴ 对 8·10⁻⁵ 是放大 5 倍, 不是 10³**。Linux 下午这里**数字错**。

- Y (coherent driving) = exp(F·disp/T) ≈ 10 ⇒ 额外放大 10

合计: 5 × 10 = **50**, 不是 10⁴。差 factor 200。

**诚实 report**: Dispatch 声称的 "10³ × 10 = 10⁴" 分解在 Linux 自己给的数字上**跑不通**。

---

## 5. 可落地的修正路线 (建议给 A2)

若 A2 仍要执行, 审稿人推荐**完全重写路线**:

**路线 A (诊断优先)** — ~2h: 先做 wavefront-vs-independent-crossing 空间相关诊断。如果是 wavefront, 整个 Langer bounce 路线弃; 换 Allen-Cahn Avrami kinetics + seed counting analysis。

**路线 B (若 diagnostic 否定 wavefront)** — Langer bounce 严格化:
1. 用正确 Onsager-Machlup action
2. 对 triple-well V = u(u−1)²(u−4)² 的 u=1↔u=0 instanton 数值求解 (shooting method on reduced variable, ~300 行 Python)
3. 算 fluctuation determinant with zero-mode volumes (space 3 zero modes + time 1 zero mode)
4. 组合给 `k_field·t_sim = V_Ω·t_sim·(zero-mode prefactors)·exp(−S_inst/T_eff)`
5. 与观测 28000 穿越对比

**路线 C (BGE DC bias 显式 tilt)** — ~1h: 用 §4.9.3 Axis A 给的 ⟨S_b⟩ = −1.48·10⁻³ 作 constant tilt, 算 tilted barrier ΔV_eff = ΔV − |⟨S⟩| × effective_displacement, 看是否单独解释 10⁴。这**最 likely 是正确 mechanism**, 因 §4.9 已经 establish BGE DC 能独立在 σ=0 下跨 outer saddle。

**时间预算**: dispatch 给 A2 "~25-35 分钟"。审稿判定: **不够**。仅路线 A (诊断) 都要 2h。原预算**不现实**。建议一凡把 A2 时间预算升到 3-5h, 或 scope 收到 "只做路线 A 诊断"。

---

## 6. 对 arXiv §4.11.1 status 可达到何程度

Dispatch 目标: §4.11.1 从 "open methodological question" 升级到 "field-theoretic Kramers correction 量级 known (within factor 3)"。

审稿判定:
- **不可达** in 25-35 分钟
- **不可达** 通过 dispatch 提出的 bubble + coherent driving 分解 (机制可能完全错)
- **可达到** "diagnostic 路径 clarified, 排除了独立热起跳假设" (路线 A 可达)
- **可达到** "BGE DC tilt contribution 量级估算" (路线 C 可达, 可能 1h 内)
- **可达到** "triple-well bounce rigorous 数值 + zero-mode 分析" (路线 B, 但要 ~8-12h, 超 dispatch scope)

**诚实的 arXiv v2 语言 upgrade candidate**:

> §4.11.1 v2 草稿 [审稿提议]:
> "The factor ~10⁴ discrepancy has two candidate mechanisms that we diagnose separately: (i) **BGE source DC bias** (§4.9.3 Axis A, ⟨S_b⟩ at 17σ from zero) provides a coherent tilt across the inner barrier whose magnitude (0.1 × 0.0015 × √voxel-projection) is comparable to T_eff·ln(10⁴), making tilted-Kramers a leading hypothesis; (ii) **Non-independent crossings via domain-wall propagation** in the degenerate (V(u=0)=V(u=1)=0) double-well geometry, where few nucleation events saturate occupancy via Allen-Cahn wall sweep. A future σ-scan with whitened source + spatial-temporal correlation C(r, Δt) of crossing events will discriminate (i) vs (ii). The field-theoretic Langer-Coleman bounce treatment (originally flagged as the gap in v1) is neither necessary nor sufficient to explain the anomaly in this degenerate-well geometry."

这个 v2 reformulation 比强推 Langer bounce 诚实得多, 且 falsifiable。

---

## 7. 审稿 verdict 汇总

| 维度 | 判定 | 关键理由 |
|---|---|---|
| 10³ × 10 分解整体 | **存疑** | Linux 自己的数字跑不通 (5×10=50 ≠ 10⁴); 机制可能错靶 |
| Langer-Coleman bounce 作 upgrade 路线 | **存疑** | Action 错 (非 overdamped); Mexican hat ≠ 观测的 triple-well; degenerate wells Δf=0 下 nucleation 理论不适用 |
| Coherent length ξ 推导 | **否定** | 数字对但 derivation 缺; αK 与 V'' 同量纲无 justification |
| Bubble count × 单 voxel ΔV | **否定** | Bubble action 应 >> 单 voxel ΔV; 物理错误 |
| 4 × 10⁻⁴ 作 "放大 10³" | **否定** | 对 8·10⁻⁵ 放大 5 倍而非 10³; Linux 算术/对比对象错 |
| Coherent driving 10 倍 | **存疑** | 单独计算 ≈ 1.25 倍; 若取 10 需 N_corr ≈ 840 无独立支撑; 且与 bubble count double-count |
| BGE DC bias 作真正 tilt 源 | **遗漏** | §4.9.3 Axis A 已 establish, dispatch 未引用这条明显线索 |
| 25-35 分钟时间预算 | **否定** | 即使最小诊断路径也要 ~2h |
| §4.11 "open question" → "known within factor 3" | **不可达** via dispatch 当前路线 |
| §4.11 诚实 reformulation 到 "two diagnostic mechanisms identified" | **可达** via 路线 A + C ~3h |

**给一凡 + Linux 的建议**:
1. 暂停 A2 "场论 bounce" 路线
2. 先让 A2 做路线 A 诊断 (wavefront vs independent crossings), ~2h
3. 同步做路线 C (BGE DC tilt 量级估算), ~1h
4. 若诊断显示 wavefront/tilt 任一主导, §4.11.1 reformulation 按审稿 §6 的 v2 草稿走
5. Langer bounce 只在诊断排除 (i)(ii) 后才 warrant 8-12h 数值投入; 目前投入不 economical

`[?]` 审稿 flag: 以上 10⁴ ≈ ratio 用 §4.8.3 原文的 "observed/predicted ≈ 1.1·10⁴" 为基准。如果 Linux 对观测/预测的定义本身就有问题 (e.g. "85% 穿越"的 per-voxel rate 定义要不要乘 attempt frequency), 整个 anomaly 可能部分是 accounting 问题, 不需要物理解释。A2 开工前也建议重新对账这个 ratio 的 operational 定义。

---

*— A2 paper-review subagent (Opus 4.7 xhigh), 2026-04-16, Linux Claude dispatch, foregrounded 落地*
