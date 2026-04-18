# 审查报告 — exp017 整体数学严谨性

**审查员**：Opus 4.6 独立 agent（paper-review subagent）
**日期**：2026-04-13 late night
**范围**：FINAL_REPORT + lawvere_monad_draft + open_problems_followup + Stage C/A1/B1 verdict + BLOCK_V_DESIGN
**判定**：**不拒，需改**（4 项 P0 硬修正 + 5 项 P1 建议 + 2 项 P2 弱化）

---

## §1 Lawvere monad 部分

### A1. `T-Alg_T^{(η, p_0)}` 良定义性 — **存疑**

三个问题：
1. **类型不匹配**。`η : Id ⇒ T` 自然变换在 C 中，但 "generates path to (X, α)" 的 (X,α) 是 **EM-范畴** C^T 的对象。从 C 态射到 EM-algebra 的桥没定义。标准应为 Kleisli composition `g ∘_K f = μ ∘ Tg ∘ f`。
2. **"path via μ" 含糊**。μ 是 multiplication 不"生成路径"。
3. **哪个 C 有 supp(p_0)**。footnote 4 取 discrete category 绕开问题，但此时 monad 退化，"Kleisli 可达"≈等价类反身闭包，与 PDE basin reachability 语义相去甚远。

**建议**：改为 "Kleisli-reachable full subcategory"，显式给 Kleisli composition；区分 Kleisli 与 EM。

### A2. `Δ_OP2 := |T-Alg_T| ⊖ |T-Alg_T^{(η,p_0)}|` — **存疑/弱**

1. `⊖` 符号未定义。
2. 子范畴 cardinality：一般 T-Alg_T 是 proper class，无良定 cardinality 差。
3. **A1 例子里根本不需要**：u=4 井与 u=1 井局部几何同构（都是 |ψ|²=const 的 U(1)-orbit），作为 T-algebras **可能同构**。丢失的不是 algebras 而是 specific realizations (moduli space 上的点)。Cardinality 没抓住这个 moduli-stack 结构。

**建议**：footnote 3 已承认"symbolic first pass"——把 `|·|⊖|·|` 从主文移到 footnote，主文只写 "placeholder quantity"。更稳健 formulation: groupoid-cardinality `∑ 1/|Aut|` 或 moduli-stack measure。

### A3. 三候选量化"qualitative stable"— **over-claim**

Heyting complement 在 non-Boolean topos 严格不满足 double negation；Kan extension obstruction 依赖 enrichment；PH 度量 point-cloud 拓扑与 categorical algebra 无 a priori 联系。把这三者并列"stable"无证据。follow-up §OP2.5 措辞"qualitative content stable"更稳妥，但主草稿 footnote 3 的"expected to be stable"是 over-claim。

**建议**：改为"we leave as conjecture whether these agree in a common limit"。

### A4. monad T 对应 PDE evolution — **未给出**

1. `T_sparse = G ∘ F_sparse`，F: Text→Field，G: Field→Score-ready，**复合方向不对**，T 不是 C→C 自同函子，根本不是 monad。
2. 没给 η, μ 的具体定义；monad 三公理未验证。
3. **方向性问题**：PDE gradient flow 更像 **F-coalgebra `X→F(X)`**（连续动力系统=coalgebra），不是 monad。最接近的候选是 **Giry monad** (stochastic kernel)——Kleisli for Giry 有 Markov kernel 解读，是正确方向。

**建议**：补 η, μ 的 Markov-kernel / Giry 定义；或改用 coalgebra 语言；或把"两 monads" 措辞降级为"endofunctor with conjectured monad structure"。

---

## §2 OP1 证伪部分

### B1. M2 不是 Banach contraction — **证明正确但理由错**

真正理由是 **T_ψ 是 0-齐次**（`T_ψ(λS) = T_ψ(S) for λ>0`），所以 `‖T_ψ(S)−T_ψ(2S)‖=0` 而 `‖S−2S‖=‖S‖`，contraction coefficient 无意义。草稿给的"normalize 在 0 奇异"不是正确理由。

有意义的问题是 ℂP^{N-1} 上在 **Fubini-Study 距离**下是否 contraction。§A.4 的线性收敛率暗示 contraction-like，但严格 Lipschitz 估计未做。

**建议**：主文改为 "T_ψ 齐次 trivially 不是 ℂ^N 上 contraction，但在 ℂP^{N-1} Fubini-Study 下表现为 contraction-like"。

### B2. 收敛到 one-hot — **正确但初值条件不完整**

推导 A.2–A.4 是标准 power iteration，严谨。**不完整处**：
- 若 max `|ψ_k|` 在多 index 同时取到，收敛到 span，不是 one-hot。
- 若 `S^{(0)}_{k*}=0`，收敛到次大 index。
草稿只说 "with S^{(0)}_{k*}≠0"，未讨论零测集以外的 degenerate 情形。

### B3. "M2 不符合 Axiom 6 directly" 强度 — **措辞得当**

只证伪 **M2 作为候选**，未证伪 Axiom 6。OP1.3 措辞"M2 不是 Axiom 6 的满意形式"合格。OP1.5 arXiv 建议措辞合适。

---

## §3 Stage C 对称性分类

### C1. byte 路径 "Z_1 phase collapse" — **术语错用 + 静默升级**

**事实**：per-doc |R|=0.84，global 0.807，kmeans-2 angle 26.2°。

**术语问题**：
- **Z_1 = trivial group**。"Z_1 phase collapse" 字面 = "剩下 trivial symmetry" = U(1) 完全破缺到一点——但这与"phase collapse"物理直觉反而冲突（Z_1 "没有" 对称破缺 vs "collapse"是强破缺）。
- `stageC_verdict.md` **原文**："ambiguous (|R|=0.840, antipodal=26°). Need deeper test."
- `FINAL_REPORT §3.1 / §4.2`：升级为 **"effective Z_1 phase collapse"**。

**这是 FINAL_REPORT 相对子文档的一次静默 claim-strengthening**，没有新证据支撑。

**建议**：FINAL_REPORT 回退为 "phase strongly concentrated (|R|=0.84), not antipodally split; U(1) broken but Z_2 not realized in phase sector"。

### C2. BGE 路径 "Z_2 via u∈{0,1}" — **成立但 Z_2 术语不严格**

- amplitude bistability 对应 GL 双井**数值上成立**。
- 但 `V = ¼(|ψ|²−1)²` 的**真正 minima 只有 |ψ|=1 的 U(1) 圆轨**；|ψ|=0 是 unstable fixed point (∂²V|_0 = −1 < 0)。
- 不存在把 |ψ|=0 和 |ψ|=1 对换的 Z_2 group action（V(0)=¼ ≠ V(1)=0，不对称）。
- "Z_2 amplitude bistability" 作为严格 symmetry 陈述**不成立**，应为 "bimodal amplitude distribution" 或 "metastable 0-basin + stable 1-basin"。

kmeans-2 angle 81.4° ≈ 但不等于 90°；既非 antipodal 也非 orthogonal；文内没解释这个值为什么是这个。

### C3. "k*=2 masks two regimes" — **over-claim 中等风险**

数字支撑充分（per-doc |R| 0.84 vs 0.20, χ² 94989 vs 4879 差异巨大），"机制不同" defensible。**弱点**：
- 只有 byte 和 BGE 两条 pathway，没测其他源场 robustness。
- byte=Z_1 / BGE=Z_2 标签都不严格 group-theoretic。
- §4.3 "源场与算子对称性互相耦合" → 只有两个数据点，只是 suggestive。措辞"This means" 略强。

**建议**：Z_n 标签加脚注 "in the loose sense of remaining-symmetry observed in empirical distribution, not a rigorous group action"；§4.3 改"consistent with...coupling; more datapoints needed"。

---

## §4 B1 barrier 计算

### D1. 势垒解析值 — **正确**

| u | V | 角色 |
|---|---:|---|
| 0.2958 | 2.0127 | 外 barrier (u=0↔u=1) |
| 1.0000 | 0 | min |
| 2.7042 | 13.1873 | 内 barrier (u=1↔u=4) |
| 4.0000 | 0 | min |

与 b1_verdict 和 Appendix 2.3.A 一致。V(u=2)=8 正确。**通过**。

### D2. "Kinetic budget" 论证 — **概念混淆**

两处问题：

**(i) Appendix 2.3.A "kinetic budget ≤ 0.3" 数值错**
`u_init ∈ [0.49, 1.69]` 对应 V(u_init) 最大值：
- V(0.49) = 1.570
- V(1.69) = **4.293**
- V(1.00) = 0

所以 `V(u_init) ≤ 4.29`，**不是 ≤ 0.3**。"0.3" 可能来自 `|ψ|_init−1≤0.3` 的线性近似到 ¼(u−1)²·... 小量，但 A1 势不是双井 GL，偏差 0.3 对应的 V 不是 0.3 量级。

**(ii) "Kinetic budget" 在 gradient flow 无意义**
Gradient flow `du/dt = −∂V/∂u` 是 1st-order 耗散 ODE，**无动能项**，系统单调沿 V 下降。不存在 "kinetic budget" 去"翻越" barrier。

**正确表述**：
> "Under pure gradient flow, V is monotone-non-increasing along trajectories, so any trajectory with V(u_init)<V(saddle u=2.704)=13.18 is confined to the u=1 basin. Observed u_max=1.199 confirms no escape."

对 B1 Langevin 部分：Fokker-Planck 稳态 `P ∝ exp(−V/σ²)` 里 σ² 是**有效温度**不是"kinetic budget"。`exp(13.2/0.25)=exp(52.8)` 远 > 5000·dt=250 仿真时间——**定性结论对**（σ=0.5 永远到不了 u=4），理由要改。

**建议**：Appendix 2.3.A 和 b1/BLOCK_V 中所有 "kinetic budget" 替换为 "thermal budget σ²" 或 "effective temperature"。

**结论（不可达 u=4）依然正确**，但论证依据错了。

---

## §5 跨文档一致性

| 项 | 评价 |
|---|---|
| A1 barrier 13.2/2.0 | ✓ 一致 |
| A1 occupancy [0.85, 99.15, 0]% | ✓ 一致 |
| per-doc \|R\| 0.84/0.197 | ✓ 一致 |
| kmeans angle 26.2°/81.4° | ✓ 一致 |
| **byte 路径分类** | **✗ FINAL_REPORT 从 stageC "ambiguous" 升级到 "effective Z_1"** |
| u_max A1 = 1.199 | ✓ 一致 |
| **"kinetic budget ≤ 0.3"** | **✗ 孤点错误在 lawvere Appx** |

**实质不一致 2 处**，均向 over-claim 方向。

---

## §6 整体诚实度

### 做得好的
- OP1 主动证伪自己的 M2 候选。
- Stage A1 occupancy 0% 诚实报告。
- b1_verdict "No Goldilocks zone" / "Langevin alone is NOT OP2 answer"。
- FINAL_REPORT §5.5 Open Problems 明确标 open。
- lawvere footnote 1-4 承认严格度不够的点。

### Over-claim 需回退
1. "Z_1 phase collapse" (FINAL_REPORT §3.1/§4.2) — stageC 只说 ambiguous。
2. "qualitative invariant stable across quantifications" (lawvere footnote 3)。
3. "T_sparse / T_dense are distinct monads" (lawvere §2.3.2)。
4. "kinetic budget ≤ 0.3" (lawvere Appx)。

### 公理 vs 定理边界
**没有混淆**。七公理按公理对待，OP1/OP2 是 meta-problems。
**小问题**：lawvere §2.3.1 "synthesis = T-algebra" / "η=立, ε=破" 是 **postulates**，应标 "we propose the following identification"。

### 统计显著性
- Block I nDCG 无 bootstrap CI 或 paired test。
- Block III/IV silhouette 0.054 / 0.150 **非常低** (< 0.25 通常认为 "no substantial structure")。用 silhouette 0.054 argue k*=2 的结构性在**统计上薄弱**。
- Block IV.5 BGE per-doc |R|=0.20 远大于 uniform baseline 0.0055（χ²=4879@72df 强烈拒绝均匀）——BGE "nearly uniform" 的任何说法都是错的。应为 "much less concentrated than byte, but significantly non-uniform"。

---

## Bottom Line

**arXiv v1 可基于这些材料，条件是做以下修正**。

### P0 必改（审稿人会抓）

1. **Lawvere Appendix 2.3.A "kinetic budget ≤ 0.3"** → `V(u_init) ≤ 4.29, V(saddle)=13.18`, 用"gradient flow monotone in V"论证。
2. **FINAL_REPORT §3.1/§4.2 "effective Z_1 phase collapse"** → 回退到 "phase strongly concentrated, Z_2 not realized in phase sector"。
3. **Lawvere §2.3.2 两 monads** → 要么补 Giry / Markov-kernel 定义，要么措辞降级为 "endofunctor with conjectured monad structure"。
4. **"kinetic budget" Langevin 语境** → 替换为 "thermal budget σ²" 或 "effective temperature"。

### P1 建议

5. Lawvere footnote 3 "stable" → "conjecture"。
6. Block I 数字补 bootstrap CI 或 paired test。
7. Silhouette <0.25 在 §3.1 诚实标注 "clustering separation is weak"。
8. OP1 "Banach contraction" 证伪理由 → 0-homogeneity。
9. "Z_2 amplitude bistability" 加脚注 "in loose sense of bimodal distribution; no rigorous Z_2 group action since V(0)≠V(1)"。

### P2 弱化

10. "Core Finding 4.3 源场与算子对称性耦合" → "consistent with...; more datapoints needed"。
11. "T-Alg_T^{(η,p_0)} Kleisli-reachable" 给形式定义或降为 "sketch"。

### P3 保留（已诚实）

OP1 M2 证伪 (B2) / A1 u=4 0% 报告 / B1 Langevin NOT answer / footnote 1-4 / stageC_verdict 的 "ambiguous" 原文。

---

**一句话结论**

**实验层（Block I–IV, IV.5）扎实可发；OP1 诚实尝试合格；Lawvere monad 章可上 arXiv 但需四处硬修正 (P0)。数字可信，范畴论口号需要 footnote 化落地。**

*审查完成。不拒，需改。*
