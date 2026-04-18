# REVIEW_PHASE_B_EXP1_math_O3.md — 2026-04-15

**Reviewer**: math audit subagent (independent)
**Scope**: Win taskbook §2 O3 — "RG self-similarity metric, structure function correlation > 0.7"
**Status**: 读 taskbook §2/§4 + day2/exp meta 后独立审查。未读代码。

---

## Summary verdict

**判定**: **存疑（tractable but under-specified）**。

Win 的 O3 judgement 在 physically 方向没错（self-similar coarse-grained patterns 是多尺度同步的可观测签名），但 taskbook 的四句话把至少 4 个自由度留给了实验者：(a) "三个 time scale 跑三次" 的 semantics；(b) blocking 的空间 vs 时间对齐；(c) structure function 的定义；(d) "相关系数 > 0.7" 的统计意义。不先 pin 死这四点，O3 pass/fail 都**不可证伪**——任何结果都能被重新解读。阈值 0.7 在当前自由度下偏宽（两条带 smooth 单调趋势的 S(r) 即便物理无关，Pearson 也容易 > 0.7）。此外 "RG" 的语言是 **overclaim**：Exp 1 没有 parameter flow，只是 Kadanoff-style kinematic blocking，应改用 "kinematic self-similarity under block averaging"。

---

## Judgment criteria audit

### 1. "三个 time scale 跑三次" 的 intended semantics

taskbook 没说清。三种合理解读：

- **解读 A (dynamical)**: 三 runs 均用 `dt_inner ∈ {0.01, 0.1, 1.0}`，其他参数不变。问题：middle/outer hardcode 为每 10/100 inner steps，所以 dt_middle 跟着从 0.1→1→10，dt_outer 从 1→10→100。total inner steps=5000 时 t_sim 分别 = 50/500/5000——**物理时长都不同**。这不是同一个系统看三个尺度，是三个不同系统。
- **解读 B (sampling)**: 固定 `dt_inner=0.01`，只是在 analysis 时从**同一** trajectory 的 t ∈ {t₀, 10 t₀, 100 t₀} 取 snapshot 做 coarse-graining。这是 temporal-scale 的观察尺度，和动力学无关。
- **解读 C (hybrid)**: 固定 t_sim=50，三 runs dt_inner ∈ {0.01, 0.1, 1.0}，对应 inner steps = 5000/500/50。middle/outer 的 physical 周期都锁在 {0.1, 1.0}。analysis 取相同 physical time 的 snapshot。

**我判 C 最贴近 Win 的直觉**：他想问"不同时间分辨率解算下，稳态 pattern 是否长得一样"——numerical-resolution robustness + physical self-similarity 的混合。**必须 Win 在 Day 2 morning 钉死**。

### 2. Blocking 算法（空间 + 时间）

taskbook: "粗粒化到同一空间 + 时间分辨率（blocking average）"。

- **空间 blocking**: 32³ lattice，block=N 的立方块平均 → (32/N)³ 粗格。N=2 → 16³（最保守，丢一半信息），N=4 → 8³（结构函数 r 范围只有 1~4，r-bin 偏少），N=8 → 4³（太粗）。**建议 N=2**，所有三 runs 都 block 到 16³。
- **时间 blocking**: 若采解读 C，三 runs 都有 t_sim=50，分别在 outer dt ∈ {1, 10, 100} 的粒度 push history。取 last-K 个 outer snapshots（K=5~10）做 ensemble 平均或 block average 到共同 "late-stationary" window。**对齐准则：相同 physical t**（不是相同 step index）。
- 若解读 A：三 runs physical t 都不同，必须 rescale，Win 的 judgement 会崩。再次佐证解读 C 是正解。

### 3. Structure function 选择

taskbook 没定义，这是 O3 最大隐患。三种候选：

- **S₂^|ψ|²(r) = ⟨(|ψ(x+r)|² − |ψ(x)|²)²⟩**：对 amplitude 波动敏感，适合诊断"粒子态"尺度。
- **C_ψ(r) = Re⟨ψ*(x+r)ψ(x)⟩ / ⟨|ψ|²⟩**：phase coherence，对 Goldstone mode 敏感。
- **G(r) = ⟨ψ(x+r) ψ*(x)⟩** 的 modulus — 混合。

在 open-dissipative + b+c feedback setting 下，若 |ψ| 近恒定（Goldstone manifold），**S₂^|ψ|² 会 saturate 小而 C_ψ(r) 有结构**；若系统进 amplitude-broken phase（O1 localized structures），反过来。**建议 O3 同时 report S₂^|ψ|²(r) 和 C_ψ(r) 两条曲线**，并声明 verdict 由哪条决定。单选一条会在 O1 结果未知前就预设 phase。

### 4. "相关系数 > 0.7" 的合理性 + alternatives

- **"相关系数 = Pearson(S^(dt_a)(r), S^(dt_b)(r)) over r bins"** 是最自然解读。三 runs 产 3 条 S(r)，两两 corr 3 对（0.01-0.1, 0.1-1, 0.01-1），取 min 或 mean。
- **0.7 阈值偏宽**：S(r) 通常 monotone decreasing（或 power-law），两条 generic monotone 曲线在有限 r-bin 下 Pearson 常 > 0.8 even with 不同 exponents。**这意味着 O3 在 naive 阈值下几乎不可能 fail**——不 falsifiable。
- **建议 principled alternatives** (Day 2 可选其一 primary + 其余辅助):
  1. **Scaling collapse χ²**: 假设 S(r; dt) = dt^(-α) · F(r / ξ(dt))，拟合 (α, ξ) 使三条 curve collapse，report residual χ²/dof；pass threshold: χ²/dof < 2。这是严格 self-similarity。
  2. **Log-log slope consistency**: 若 S(r) ~ r^η，三 runs 的 η 应一致（|Δη| / η̄ < 10%）。
  3. **KS test on rank-normalized S(r)**: 去掉 amplitude 比较 shape，p > 0.05。
  4. 若保留 Pearson，**阈值改 > 0.9** 并 corr on log S vs log r 的 **residual**（去掉主 trend 后）。

### 5. RG 语言 vs kinematic self-similarity

- **严格 Wilson RG**: 块自旋平均后重新缩放场振幅 + 投射耦合常数空间，追踪 β-function 和 fixed point。
- **Exp 1 实际做的**: 单次轨迹的 spatial/temporal block average，**无** 参数重整化，**无** field rescaling Z(ℓ)。
- **结论**: 这是 **Kadanoff block-averaging 的 kinematic self-similarity 检验**，不是 RG flow。taskbook 第 91 行标题 "O3 — RG 不变性" 与 verdict 语言（若写入 paper）应改为 **"kinematic self-similarity under block averaging (a prerequisite for RG fixed-point candidacy)"**。
- MaoField claim "RG 从 Phase B 开始" 宜降级为 "self-similarity diagnostics open the door to RG analysis in Phase C+"。现在写 RG 会被物理审稿人挑（非 blocking 但 embarrassing）。

---

## Concrete proposals for Day 2 implementation

### Step-by-step algorithm (Linux 可跑)

**前置（Day 2 morning, Win 拍板）**: 选解读 C（固定 t_sim=50, 三 dt_inner）。

1. **三 runs**: exp config 除 dt_inner ∈ {0.01, 0.1, 1.0} 外全同，seed 相同。inner_steps = t_sim / dt_inner。middle/outer 周期按 physical time 锁 {0.1, 1.0}（代码若 hardcode step count，Day 2 需小改以锁 physical time；若不能改，改用解读 A 并 accept 物理时长差异，但 analysis 要相同"late-stationary"语义，至少 rescale t / t_sim 到 [0.8, 1.0] window）。
2. **Snapshot 抽取**: 每 run 在 physical t ∈ {40, 42, …, 50} 取 6 snapshot，ensemble 平均消涨落。
3. **空间 block**: 对每个 snapshot 做 block=2 立方平均 → 16³ 格。
4. **Structure functions**: 在 16³ 上用 FFT 算 correlation C_ψ(r) = F⁻¹[|F[ψ]|²] / N，radial-average 到 r ∈ [1, 8]（7 bins）。同时算 S₂^|ψ|²(r)。
5. **Judgement metric** (primary): scaling collapse — 拟合 S(r; dt) = A(dt) · r^η 的 η，要求 |η_max − η_min| / η̄ < 0.15 且 Pearson on log S(r) > 0.9 pairwise。 (secondary): Pearson on raw S(r) > 0.7（保留 Win 原判据作 sanity）。
6. **Control**: 对照组（single-scale, dt=0.01 only）只有一条 curve，O3 不适用，但可 report C_ψ(r) 形状作为 "非多尺度 baseline"。
7. **Figure**: 3 curves × 2 observables (S₂^|ψ|² 和 C_ψ) on log-log，with collapsed version 叠图。

**Pass 定义（revised）**:
- Primary: scaling collapse η consistent（tolerance 15%）且 log-S Pearson > 0.9。
- Secondary: raw Pearson > 0.7（Win 原判据）。
- 两者都过 → O3 pass（strong）；仅 secondary 过 → O3 marginal（标 "kinematic self-similarity tentative"）；都 fail → O3 fail。

---

## Blocking / non-blocking 分类

- **Blocking（必须 Day 2 morning 解决，否则 O3 结果不可解读）**:
  1. 三 time scale 的 semantics（解读 A/B/C 二选一，建议 C）。
  2. Structure function 的具体公式（建议两条都算）。
  3. Pass 判据升级（scaling collapse 或 >0.9 log-log Pearson）。
- **Non-blocking（Paper 前修订可）**:
  4. "RG" → "kinematic self-similarity" 的 verdict 语言降级。
  5. Block size N=2 vs N=4 的 sensitivity check（可 Day 3 补）。

---

## Recommendations

- **Verdict 语言**: Phase B Exp 1 O3 verdict 里**不要**写 "RG invariance"。用 "**kinematic self-similarity under Kadanoff block-averaging**"。Paper Branch A 标题里的 "多尺度同步" 保留，但正文对 RG 的宣称需限定到 "self-similarity 是 RG fixed-point 的 necessary 非 sufficient 条件"。
- **阈值**: 保留 Win 的 Pearson > 0.7 作 secondary sanity，primary 改 scaling-collapse 或 log-log Pearson > 0.9。
- **同时 report S₂^|ψ|² 和 C_ψ(r)**，不要预设 phase。
- **Day 2 morning 先和 Win 对齐解读 C**，否则 Day 2 afternoon 跑出来的数字没法写 verdict。

---

## References

- Kadanoff L.P. (1966), "Scaling laws for Ising models near T_c", Physics 2, 263 — block-spin origin.
- Wilson K.G. (1971), "Renormalization group and critical phenomena I/II", PRB 4 — parameter flow vs kinematic blocking 的区分。
- Frisch U. (1995), *Turbulence: the Legacy of Kolmogorov*, §5 — structure function S_p(r) 的 scaling collapse 方法论。
- Aranson & Kramer (2002), Rev. Mod. Phys. 74, 99 — complex Ginzburg-Landau ψ=a+ib setting 下 C_ψ(r) vs |ψ|² structure functions 的 phase 依赖。
- Hohenberg & Halperin (1977), Rev. Mod. Phys. 49, 435 — open-dissipative dynamics Model A/B/H 分类，决定哪个 observable 主导。

---

(审查完，字数 ≈ 1900, 不改代码)
