# 审查报告 A1.4 VERDICT

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：`block4_5/a1_4/VERDICT.md` v1 → v2
**判定**：v1 **存疑（3 blocker + 6 polish）**；v2 修订后 **release-ready for arXiv §4 底稿**

---

## 必过三条（一凡指定）

| # | 项 | v1 判定 | v2 修订 |
|---|---|---|---|
| 1 | three-fold framing accurate | ✅ 数学正确，三轴独立 | 保持，加 Helmholtz 严格化 |
| 2 | 数据表无量纲混淆 | ⚠️ "10⁴ orders" 字面错 | **v2 修为 "factor ~10⁴ (~4 orders)"** |
| 3 | 不 overclaim | ✅ 五条 not-claimed 完整 | 保持 |

---

## §1 Three-fold framing 验证

### Axis A — Source drift ✅
- σ=0 → 66% u=2 作为 Laplace 反驳：**逻辑严谨**（σ→0 极限是 basin-of-attraction + S drift，不是 Boltzmann）
- BGE Sb t=−17.1：独立核算 = −17.2 ✓（n=70 per-doc-mean 1-sample t-test）
- "detailed balance 破坏" 精度：v1 说 "⟨S⟩≠0 breaks DB"，**严格 statement**: non-gradient (solenoidal) S breaks DB; ⟨S⟩≠0 是一个 diagnostic。v2 已改为 Helmholtz-decomposition 措辞
- **v2 补**：累积 forcing `|S|·t_sim ~ 25 ≫ ΔV_outer=0.095` 能量尺度论证

### Axis B — Potential tail ✅
- V ~ u⁵ for u>2：`u⁵ − 6u⁴ + 13u³ − 12u² + 4u` 展开 ✓
- σ√dt=0.112：`0.5·√0.05 = 0.1118` ✓
- u 位移 ≈ 2|ψ|·0.112=0.22 at |ψ|~1 ✓
- k=4 wall C³-smooth at u=u_max：`V=V'=V''=V'''=0, V''''=24` ✓
- **v2 补**：`u⁵ = |ψ|¹⁰` in ψ-space vs A1 原势 `|ψ|¹⁸` 对比

### Axis C — Numerical scheme（v1 数字错，v2 修正）
独立 SymPy 验算 at u=10, a²=b²=5, λ=1:
- `f_wall = 1687.5`, `f'_wall = 675`
- `J11=J22 = 8437.5`, `J12 = 6750`
- `J_max = J11 + J12 = 15187.5`

| 量 | v1 (错) | v2 (正确) |
|---|---:|---:|
| `J (λ=1)` | 30000 | **15188** |
| `J (λ=10)` | 300000 | **151875** |
| `dt_max,c1` | 6.7×10⁻⁵ | **1.3×10⁻⁴** |
| `dt_max,c2` | 6.7×10⁻⁶ | **1.3×10⁻⁵** |
| CFL 违反 (c1) | 750× | **380×** |
| CFL 违反 (c2) | 7500× | **3800×** |

**结论不变**（都是 O(10²~10³) 量级 CFL 违反），**但数字精确**。

---

## §2 数据/量纲审查

| 检查项 | v1 | v2 |
|---|---|---|
| T_eff = σ²/2 全部 σ 行一致 | ✅ | ✅ |
| Kramers × horizon dimensionless | ✅ | ✅ |
| "~43 orders of magnitude" (outer, log-gap) | ✅ | ✅ |
| "3.07× static ratio" | ✅ | ✅ |
| **§5.1 title "10⁴ orders"** | **❌ 字面错 = 10^10000** | **v2 修 "factor ~10⁴ (~4 orders)"** |
| **§2.4 表格 inner ΔV/T 标注缺失** | **⚠️** | **v2 补表格含 outer+inner ΔV/T 列 + † 注** |
| Laplace p(0)/p(1)/p(2) 数值 | ✅ 0.028/0.569/0.402 | ✅ |

---

## §3 Overclaim 扫描

| 检查 | v1 | v2 |
|---|---|---|
| §0 "refinement, not resolution" | ✅ | ✅ |
| §7 五条 "not claimed" | ✅ | ✅ |
| §4.2 "inner barrier crossed via Kramers" | ⚠️ 未标量化差距 | **v2 加 "(quantitative rate differs by factor ~10⁴)"** |
| §5.1 "Ratio ~10⁴" | ✅ ratio OK | **v2 "factor ~10⁴ (~4 orders), not 10^10000"** |

---

## §4 Win narrative 一致性

| 项 | v2 |
|---|---|
| §一 #7 reframe (Langevin works inner, fails outer) | ✅ 贯彻 |
| §二 Giry / OP2 / Kramers three-fold | ✅ v2 补 cross-ref "Giry lift deferred to lawvere_monad_draft.md" |
| §三 Kramers/Laplace 双框架 | ✅ 贯彻 §1.3 + §2.4 |
| §五 量纲 static vs log-gap | ✅ v2 无混淆 |

---

## Bottom Line

v2 满足一凡指定必过三条：
1. three-fold framing accurate ✓
2. 数据表无量纲混淆 ✓（"10⁴ orders" 字面错已修）
3. 不 overclaim ✓

**Release-ready for arXiv §4 底稿**。
