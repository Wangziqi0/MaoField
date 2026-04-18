# 审查报告 arXiv §2.1/§2.2

**审查员**：independent paper-review subagent
**范围**：`arxiv_v1_section2_1_2_2_DRAFT.md` (Win 起草)
**判定**：**Conditional Pass — 1 P1 必修 + 1 P2 必修 后 release**

---

## P0 (无)

## P1 必修 (1 项)

**P1.1 §2.1.4 Engels 质量互变 realization 段数字与因果误归因**

当前 (line 35):
> "a *quantitative* reduction of the outer barrier from 13.187 to 0.095 (a 140× reduction) produced a *qualitative* loss of well structure (52.5% voxel residency at the clamp boundary, vs 0% for the unmodified potential)"

**三问题**:
1. §2 应 qualitative，不应搬 §4 的 13.187/0.095/140×/52.5% 硬数字
2. "barrier reduction → well structure loss" 单因果归因 **与 §4.9.3 三轴诊断 (source / potential / scheme) 不一致**；§2 承诺 §4 兑现不了的命题
3. "vs 0% for unmodified potential" 对照基准不清（B1 的哪个 σ?）
4. 140× 数字不准: 13.187/0.095 = 138.8×

**建议重写** (qualitative)：
> "Stage A1.4 (§4.9) is a direct experimental instance: a quantitative reduction of the potential's outer barrier — undertaken to probe continuity of parameter change — triggered a qualitative regime shift in which the field explored amplitudes orders of magnitude larger than the original potential admitted. §4.9.3 decomposes this regime shift into three coupled axes (source statistics, potential geometry, numerical scheme); the quantitative-qualitative discontinuity is the phenomenon, the three-axis decomposition is its mechanism."

## P2 必修 (1 项)

**P2.1 L17 "No information loss" 对 byte-frequency scattering 不准确**

byte-frequency scattering 保留 byte value identity 但**丢失位置信息**。"every voxel directly traceable to a UTF-8 byte position" 是错的。
→ 改："every voxel corresponds to a UTF-8 byte value (position information collapsed to histogram); the construction is injective at the histogram level but lossy at the sequence level"

## P3 nice-to-have
- §2.1 开头加 forward reference "seven axioms stated in §3.2"
- §2.1.5 bullet 2 加 OP1/OP2 明确绑定
- §2.2.1 末尾 bridge §2.3.2 三层 realization
- L35 若保留数字用 "~140×" 或 "approximately two orders of magnitude"

---

## 通过项

- 四方法论承诺完整（Reflection / Contradiction / Practice / Q-to-Q）+ rationale 充分
- Lawvere adjunction / η / ε / triangle identities / T-algebra 严格正确
- 与 §2.3 / §3 / §4 上下游一致
- disclaimer 密度总体克制
- 无 Z_n / SSB 滥用（§2 没用该语言）

## Bottom Line

§2.1/§2.2 骨架质量高于一般 methodology draft。核心问题是 §2.1.4 Engels 例子承诺了 §4.9 兑现不了的单因果叙事 — 修掉即为 A-grade。
