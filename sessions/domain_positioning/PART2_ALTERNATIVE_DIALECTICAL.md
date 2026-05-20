# §2 辩证唯物论 Alternative：正确性从内部 emergent

## 2.1 辩证唯物论与机械唯物论的根本区分

| | 机械唯物论 | 辩证唯物论 |
|---|----------|----------|
| 正确性来源 | 外部给定 | 内部矛盾中 emergent |
| 系统状态 | 被动反映 | 主动持有矛盾并自我运动 |
| 稳态 | 到达外部 reference | 非零 tension 上动态平衡 |
| 矛盾的地位 | 需要消除的误差 | 系统运动的驱动 |
| 训练范式 | single-channel fit | dual-channel tension |
| 标注工 | 需要（正确性的人形载体） | 不需要（正确性内部 emergent） |

## 2.2 矛检的数学结构：第二通道

当前所有模型的训练：
$$
\mathcal{L}_{\text{single}} = -\mathbb{E}[\log p_\theta(x)]
$$
单通道——只做分布拟合。当训练数据是模型自己的输出——分布被反复 fit——坍缩到 trivial attractor——崩溃。

矛检的扩展：
$$
\mathcal{L}_{\text{dual}} = \mathcal{L}_{\text{LM}} + \alpha \cdot \mathcal{L}_{\text{spear}}
$$
双通道——第二通道检测模型**内部的矛盾 tension**——不需要外部信号。

**第二通道不来自外部——来自模型自己对自己内部矛盾的度量。** 正确性信号是 (D_n - D̄^EMA)^2 ——当前偏离历史趋势的 tension——不是外部 label 告诉它"这个答案好不好"——是它内部的两个力（拟合分布 vs 检测矛盾）之间的 tension 在持续校准参数。

## 2.3 双通道 → 稳态 → 温暖

- 单通道：D → 0 → 冷崩溃（无张力，frozen state）
- 双通道：D → D*(α) > 0 → 稳态（finite tension，持续自迭代）
- 过度矛检：α → ∞ → D 被压制 too hard → 过冷（输出单调）

**D*(α) > 0 不是 bug。是对"矛盾不能消除只能转化"的数学 instantiation。** α 是温度调节器——不是"压制信号"——是"让系统在有限张力下持续运动"。

## 2.4 实证 evidence（GPT-2 124M, Wikitext-2, 10 代, N=4 seeds）

- **U-shape 非单调相变**：α=0→spike→崩溃，α=10→spike→recover→接近基线 PPL
- **D4 5/5 PASS STRONG ROBUST**：U-shape across all seeds + all alpha levels
- **m_eff = 0.300 ± 0.042**：multi-seed relaxation envelope fit, 95% CI [0.234, 0.366]
- **J_S in [0.331, 0.770] nat/generation**：三 method empirical fit
- **ρ = 0.9174, n_{1/2} = 8.0 gen**：Banach contraction to D* > 0
- **F3 p=0.82**：frame effect on PPL not significant — possible indicator that PPL as metric needs redefinition