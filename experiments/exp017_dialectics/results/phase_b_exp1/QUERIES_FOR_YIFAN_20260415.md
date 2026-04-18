# Phase B Exp 1 — Queries for 一凡 (batch-process 2026-04-16 morning)

**Linux Claude, Day 1 evening, 2026-04-15**
**不打断 release 周；这些 [?] 留一凡明早 batch 回答**

---

## [?] Q1 — `N = 100` history window vs `t_sim = 50` 不一致

**Observation**: Taskbook §1.2 说 `N = 100 步`，§1.4 说 `5000 inner steps (t_sim = 50)`。外层 push 每 100 inner steps 一次 → 50 个 pushes 在 5000 inner steps 内。History buffer cap=100 但只能填到 50（永远不满）。

**Consequence**: Effective history window 是 **50 outer-ticks (t=50)**，不是 spec 声明的 100-window。若 N=100 is steps-meaning "outer-ticks"，需 t_sim ≥ 100（即 steps ≥ 10000）才能让 buffer 真填满。

**Options**:
- (A) N_hist = 50 + steps = 5000 (不变 t_sim, 缩 window)
- (B) N_hist = 100 + steps = 10000 (延长 t_sim, 保 window, +2x cost)
- (C) 保持现状，在 verdict 注明 "effective window truncated"
- (D) N_hist = 100 (inner-step unit), push every inner step (最密集, β 需重新 calibrate)

**Linux tentative**: (C) for Day 2 MVP, 视 O2 结果决定是否 (B) Day 3 复跑。

---

## [?] Q2 — dS/dt → ~10⁻⁶ (near-zero) for exp mode

**Observation**: Exp-smoke (10 docs, 5000 steps) 末态 dS/dt ≈ 7.6·10⁻⁶, source_l2 saturated ≈ 1.17, mean|ψ|² = 1.41. 系统在 t=50 已接近 equilibrium fixed point（deterministic，无 noise）。

**Implication**: O2 Pass condition 是 "进入 dS/dt > 0 的**稳态**（**持续非零**）"。当前数据显示 dS/dt 指数衰减向零，不是稳定在正值。若照字面理解，**O2 fail**。

**Interpretation**:
- 可能 (i) MaoField b+c 反馈**不产生持续耗散**（→ 洞见 2-3 需修正：系统是"收敛到 shifted 吸引子"而非"持续生成熵"）
- 可能 (ii) t_sim 太短，长时间后 dS/dt 真正稳态（plateau 还没到）
- 可能 (iii) 缺 noise/stochastic 驱动 — 确定性 gradient flow 天然走向 attractor；开放耗散需要 temporal drive

**Options**:
- (A) 按字面 O2 判定 fail 并 pinpoint 洞见 2-3 错
- (B) 加 Langevin noise σ 项到 EOM 让 exp 真正 driven (但改变 spec)
- (C) 延 t_sim 到 100 or 200 看 plateau 是否真是 0
- (D) reframe "持续非零" 为 "quasi-stationary small but positive"（current mean=7.6·10⁻⁶ 非零）

**Linux tentative**: Day 2 并行跑 (C) t_sim = 200 的副本检查 plateau；Day 3 verdict 按 (A) or (D) 判定。

---

## [?] Q3 — `block_average` middle-tick 语义

**Question (code review P0-5)**: Win taskbook §1.3 "中层 每 10 步 重新归一化 S 的粗粒度结构（block-average）". Linux 实现为：每 10 inner steps 在 middle tick 上 `recompute_effective_source → block_average(block=2)` → S 被 coarse 版本替换，驱动下一个 10 inner steps。

**潜在歧义**:
- 解 A (当前实现): 每 10 步 S = coarse(S₀ + αΔψ + βδS)，between ticks 不变
- 解 B: S₀ 本身被 block-averaged 永久 coarser，每 10 步进一步平均
- 解 C: 每 10 步 "重新归一化" = 能量/范数归一（不是 coarse-graining）？但 Win 明说 "block-average"

**Linux tentative**: 解 A 最 natural，Day 2 按此执行。若 O3 RG self-similarity fail，Day 3 可重跑 解 B 对比。

---

## [?] Q4 — O2 公式 `dS/dt = ∫(∇V·∇ψ)²/γ` 量纲

**Observation**: Taskbook §2 O2 给出 `dS/dt = ∫ (∇V·∇ψ)² / γ dx + noise contribution term`. Linux 代码实现的是 **`|deterministic RHS|²`** 的空间平均（Seifert-style EP for overdamped Langevin）。

**Issue**: 
- Taskbook 公式 `(∇V·∇ψ)²` 量纲是 [energy²/length²·field²]，不是 entropy production rate 的常见形式
- Linux 的 `|RHS|² = |γ⁻¹∂_t ψ|² · γ²` 是 dissipation rate (功率)，在 overdamped 系统里与 EP rate 成正比（系数 1/T for isothermal）

**Linux tentative**: 当前 Linux 实现是 physically defensible 的替代，**请 Win 审**是否 taskbook 公式有打字/符号错或我理解错。

---

## [?] Q5 — β·δS_history 无 normalization 导致有效 β 随 buffer 填充而变

**Observation**: 代码 review P0-4 fix 后，δS 是 literal integral `Σ w_k · Δψ · dt_outer`（不归一化）。Buffer 填 1 snapshot 时 δS 小；填 50 snapshots 时 Σw ≈ 17.55 → δS ≈ 17.55 × Δψ。

**Implication**: 有效 β 不是常数，而是 β × (current buffer saturation factor)。从 t=0 到 t=50 effective β grows from 0 to 0.05·17.55 = 0.878。在 transient 期间 (t < 10~20) β effectively ~0.1·0.05·k 小，quasi-steady 后接近 0.88。

**Implication for verdict**: 反馈 ramp-up 是 physical feature（"历史需要时间累积"），不是 bug。但需要在 verdict narrative 里明说 "effective β is a time-varying ramp"。

**Linux tentative**: 保持现实现。verdict 里写入 caveat + figure of β_eff(t)。

---

## Day 1 Summary for 一凡

✅ Rust crate `block_v_phase_b_exp1` 完成（engine + multi-scale loop + 5 modes）
✅ Null test (α=β=0) 70/70 docs 无 NaN, source_l2 invariant, dS/dt 单调衰减
✅ Exp smoke (α=0.1, β=0.05, multi-scale) 10/10 docs 无 NaN, 反馈 active
✅ Spawn-agent code review (opus) 完成 → `REVIEW_PHASE_B_EXP1_code.md`
✅ Review P0-4 (δS normalization) + P0-5 (middle-tick ordering) 已修
⚠️ 5 个 [?] queue 明早回答（不阻塞 Day 2 启动）
✅ Day 2 可直接跑 `exp` + 4 种 control modes

**Day 2 Plan (tentative)**: 早上跑 5 modes × 70 docs × 5000 steps (~30 min 全部)，上午计算 O1/O2/O3 observables，spawn-agent review 公式推导。

— Linux Claude, 2026-04-15 evening
