# 审查报告 — 今晚两份数学预研

**审查员**：Opus 4.6 独立 agent（paper-review subagent）
**日期**：2026-04-13 late night
**范围**：`block4_5/a1_4_shifted_potential_analysis.md` + `zn_angular_potential_math.md`
**判定**：**需返工**（S1 两项必须修，S2 三项应修）

---

## §1 数学验证逐条

### 文档 1 — A1.4 shifted potential

| 项 | 判定 | 说明 |
|---|---|---|
| 1.1 因式分解 `dV/du = (u−1)(u−2)(5u²−9u+2)` | ✅ | 手算展开验证完全一致 |
| 1.2 鞍点 `u = (9±√41)/10` | ✅ | 0.25969 / 1.54031 验证 |
| 1.3 鞍点 V 值 0.431 / 0.095 | ✅ | 精度良好 |
| 1.4 u=0,1,2 是 local min | ⚠️ | **u=0 不是无约束 local min**，是 `u=|ψ|²≥0` 的 boundary min。V(−ε)≈−4ε<0。需加注"物理域边界"。u=1, u=2 的 d²V/du² = 2, 4 > 0 ✅ |
| 1.5 `⟨KE⟩ ~ σ²/(2γ)` 动能预算 | ❌ | Overdamped Langevin **没有动能概念**。`σ²/(2γ)` 是 **effective temperature T_eff**，与 barrier 比较用 Arrhenius rate，不是"能量能不能爬"。**概念错误，措辞必改** |
| 1.6 `p_k ∝ exp(−V_saddle_k/T)` 占据率 | ❌ | **结构性错误**。Boltzmann 平衡态是 `p_k ∝ ∫exp(−V/T)du` 对 basin 积分；三井都 V_min=0，严格 Boltzmann 给**近乎等占据**（按 `1/√V''(u_k)` 曲率微调）。用 saddle 高度作权重**不是 Boltzmann 也不是 TST**。TST 给的是 *rate*，从 rate 到 steady-state 要解 master equation。预测表 "p(u=1)=0.667, p(u=2)=0.312" **数字结构上错** |

### 文档 2 — Z_n angular potential

| 项 | 判定 | 说明 |
|---|---|---|
| 2.1 `Re(Cψⁿ) = |C|rⁿcos(nθ+φ_C)` | ✅ | 展开正确 |
| 2.2 极小点 `θ_k = ((2k+1)π−φ_C)/n` | ✅ | |
| 2.3 `r_min ≈ v·[1 − nε|C|v^{n−4}/8]` | ❌ | **符号错**。设 r=v(1+δ), leading-order 解 δ = +nε|C|v^{n−4}/8。r_min **比 v 大**（cos=−1 方向势被负贡献拉低→径向向外扩）。r_saddle 符号相反为 − |
| 2.4 `ΔV = 2ε|C|vⁿ` | ⚠️ | leading order 正确，需标 O(ε²) 修正 |
| 2.5 `∂²V/∂θ² = n²ε|C|vⁿ` 正定 | ✅ | |
| 2.6 `∂²V/∂r² ≈ 8v²` | ⚠️ | leading order，漏写 `+ n(n−1)ε|C|v^{n−2}` O(ε) 修正 |
| 2.7 `∂²V/∂r∂θ = 0 at minimum` | ✅ | |
| 2.8 `τ_θ/τ_r ~ 1/(n√ε)` | ❌ | 用的是**欠阻尼**公式（振荡频率 `√(λ/m)`）。**MaoField 是 overdamped，应为 `1/(n²ε)`**。模型不一致错误 |
| 2.9 n<4 径向稳定 | ✅ | |
| 2.10 `ε→∞` V→−∞ 归因于"n 偶" | ❌ | **归因错**。关键是 n 与 4 的关系（n>4 or n=4 且 ε|C|>1）。与奇偶无关（奇 n 也能找 cos=−1 方向） |
| 2.11 Rust `psi.powu(n-1)` 梯度 | ❌ | **Wirtinger 导数错**：∂/∂ψ*[Re(Cψⁿ)] = (n/2)·ε·C*·**(ψ\*)^{n-1}**。代码应为 `psi.conj().powu(n-1)` 不是 `psi.powu(n-1)`。**对 n=2 巧合重合，n=3,4 物理完全错**。且½系数与 Mexican hat 的 2(...)ψ 惯例需对齐 |

**统计**：✅ 11 项 / ⚠️ 6 项 / ❌ 5 项

---

## §2 发现的错误（按严重性）

### S1 严重（必改）

**E1. 文档 1, §1.6 占据率预测**
`p_k ∝ exp(−V_saddle_k/T)` 概念错误。真实平衡态 Boltzmann 给三井近乎等占据。Table "p(u=0)=0.021, p(u=1)=0.667, p(u=2)=0.312" **数值不可信**。

修复路径：
- 删除占据率表，改为 "Kramers rate 对比"：`k_{1→0} ~ exp(−0.43/T) ≈ 0.032`, `k_{1→2} ~ exp(−0.095/T) ≈ 0.468` at T=0.125。
- 明确"rate ≠ occupancy"；在 short-time rare-event regime（仿真时间 250 time units）u=2 占据由 `k_{1→2}·t` 控制。
- 或改为 Laplace-近似平衡占据 `p_k ∝ 1/√V''(u_k)`（此时三井竞争由 basin 曲率决定，不涉及 saddle）。

**E2. 文档 2, §2.11 Rust 代码**
`eps_c.conj() * psi.powu(n-1)` → `0.5 * (n as f64) * eps_c.conj() * psi.conj().powu(n-1)`（且与 mexican 的 2(...)ψ 惯例对齐，系数需调整）。**对 n=2 无差别（巧合）；对 n=3,4 物理完全错**——Block V V.1-A 实验如果基于此代码跑，结果不可信。

### S2 中等（应改）

**E3. 文档 1, §1.5** `⟨KE⟩ ~ σ²/(2γ)` → 改为 "effective temperature T_eff"。Overdamped dynamics 无动能项，σ² 是噪声方差，T_eff=σ²/(2γ) 是 Fokker-Planck 稳态有效温度。

**E4. 文档 2, §2.3 r_min 符号** 正号，不是负号。直觉：cos=−1 方向 V 被负贡献拉低 → 径向向外扩。r_saddle 对应 −。

**E5. 文档 2, §2.8 时间尺度** overdamped 对应 `τ_θ/τ_r ~ 1/(n²ε)`，不是 `1/(n√ε)`。

### S3 小错（条件漏标）

**E6.** 文档 1, §1.4: u=0 应显式标"物理边界 basin (u=|ψ|²≥0)"。
**E7.** 文档 2, §2.4: 加 "leading order in ε, O(ε²) corrections neglected"。
**E8.** 文档 2, §2.6: 加 `+ n(n−1)ε|C|v^{n−2}` O(ε) 修正。
**E9.** 文档 2, §2.9-2.10: 改"n 与 4 的大小关系 + ε|C| 系数大小"，不是"n 偶奇"。
**E10. Jacobian 未讨论**: V(u) 对 1D u 和对 2D ψ=re^{iθ} 的 Boltzmann 形式不同（前者 `p(u) ∝ exp(−V/T)`, 后者含 radial Jacobian `r·dr·dθ`）。文档未说明用哪个 coordinate，影响占据率预测再错一层。

---

## §3 诚实度 / 措辞

**Over-claim**
- 文档 1 "核心预测：u=2 ~30% 占据" 由错误公式生成，需撤回或大改。
- 文档 2 "良好的绝热分离" 定性结论在 overdamped 下仍成立（`1/(n²ε)→∞` 甚至更强），但量词要改。

**Under-claim / 缺省**
- 文档 2 工作区 `ε|C|vⁿ≤0.1v⁴` 没说是为保证径向 well 结构。
- 文档 1 没说 Langevin 坐标是 u 还是 ψ（Jacobian 问题）。

**[?] 覆盖**
- 两份文档的 [?] 都只覆盖"要不要跑"决策，**数学断言本身无 [?]**。鉴于 §2 发现，应该有 [?] 标注在 1.6（Boltzmann）、2.3（符号）、2.8（阻尼）、2.11（代码）处。

---

## Bottom Line

**需返工**（S1 两项必改，S2 三项应改，S3 四项补注）。

**可放行的部分**：因式分解、临界点位置、鞍点数值、Hessian 对角化、k*=n 结论、ε→0 极限 U(1) 拓扑论证——**数学骨架都对**。

**问题集中**：静态临界点 → 动力学/热力学预测的那一步（Boltzmann 结构、overdamped vs underdamped、Wirtinger 导数）。

**建议修复优先级**（总 ~80 分钟）：
1. 修 Rust 代码 ψ→ψ* + ½ 系数（5 分钟，关键 bug）
2. 撤回占据率表 / 改 Kramers rate 表（30 分钟）
3. 文档 2 r_min 符号 + overdamped τ_θ/τ_r（15 分钟）
4. KE → T_eff 概念清理、Jacobian 说明、边界 basin 注记（30 分钟）

**对 Block V 影响**：V.1-A 启动前必须修 Rust bug（E2）；A1.4 sanity check 的 Langevin 预测数字需重算（E1）。

---

*审查完成。文档骨架质量合格，动力学层有实质错误。一凡醒来请先过 S1 两项。*
