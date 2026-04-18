# 审查报告 Block V Phase A 设计（post-A1.4 refinement）

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：`BLOCK_V_DESIGN.md` §4.5 Phase A-0/A-1/A-2/A-3/A-joint
**判定**：v1 **存疑（3 blocker + 4 major）** → v2 修订后 **release-ready**

---

## 必修 Blockers (3 项) → 已全部修

1. **A-2.a 乘法形式 `V·(1+α(u-3)²)` 的 tail 本质未变为 `u⁷`**，仍是多项式，未解决 A1.4 诊断的 Axis B shallow-tail 问题。
   - **v2 修**：改为**加法 quartic** `V + α·(u − u_c)⁴·[u > u_c]`，`u⁴` 尾独立于 base `u⁵`
2. **A-3.c "velocity sign reflection" 在 overdamped SDE 中概念错误**（overdamped 无 velocity）
   - **v2 修**：改为 **Skorokhod 径向投影** `if |ψ_{n+1}| > R_max then ψ_{n+1} ← R_max·ψ_{n+1}/|ψ_{n+1}|`，指定 `R_max=√3.5`，引用 Bossy-Talay 2005
3. **Phase A-0 Reachability pre-check 遗漏**：未验证 Kramers τ_cross vs t_sim=250 是否使 Laplace target 可达
   - **v2 修**：新增 §4.5.0 Phase A-0（1h）：算 σ=0.3/0.5 下 τ_cross（0.3: 29 < 250 ✓；0.5: 7.5 marginal）+ σ=0 deterministic Monte Carlo baseline

## 应修 Major (4 项) → 已全部修

4. **A-1 success criterion "approaching init-distribution" 不 testable**
   - **v2 修**：改为定量 `max_k |p_obs(k) − p_A-0(k)| < 0.05`，对照 Phase A-0 Monte Carlo 预测
5. **A-3.b IMEX 的 J 结构未指定**
   - **v2 修**：明确 **per-voxel 2×2 real Jacobian** `J_{2×2} = f(u)·I₂ + 2f'(u)·[[a², ab], [ab, b²]]`，closed-form 2×2 matrix inverse，O(N) 成本
6. **A-joint "best of" 组合爆炸**
   - **v2 修**：改为 *confirmatory* framing（1 config: A-1.a + A-2.b + A-3.b）；失败后 2-stage 2×2×2 grid (+3h)
7. **A-2.c 与 A-3.c 概念重复**（硬 cap ≡ reflecting BC）
   - **v2 修**：删除 A-2.c，整合到 A-3.c Skorokhod projection
8. **A-joint ±5pp tolerance 对小 p(0)=0.028 过宽**
   - **v2 修**：改为 KL `KL(p_obs ∥ p_Laplace) < 0.05`

## 其他改进（v2）

- axis-D 候选列 D-1/D-2/D-3/D-4（field theory / Laplacian coupling / init sensitivity / horizon）+ 诊断路径
- 时间预算从 10h 上调到 **12h MVP / 24h full**（含 A-0 1h + A-3 IMEX+Skorokhod 开发 1h + A-grid backup 3h）
- A-2 success criterion 同时报 "Axis A applied" 和 "not applied" 两栏，避免循环依赖

---

## Bottom Line

Phase A 设计作为**内部研发路线图**逻辑清晰；v2 修订后可作为 arXiv §5 "OP2 methodological refinement" 的正式引用对象。

**三大修订亮点**：
- Phase A-0 reachability pre-check 防止 Laplace target unreachable 的陷阱
- Axis B 从乘法改加法 quartic，Axis C 从错误的 velocity reflection 改正确的 Skorokhod projection
- A-joint 从 "best-of optimization" 改为 "confirmatory + grid fallback"，避免 selection bias 被 reviewer 打回

v2 release-ready for arXiv §5 引用。
