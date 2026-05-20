# §6 关键文件 + 数字 anchor + 时间线

## 6.1 关键源文件

| 文件 | 内容 | 路径 (Linux 36) |
|------|------|-----------------|
| M 综合 | 13 份报告 cross-check + 全部数字锁 | `literature/INTERNAL_CONSISTENCY_100_PERCENT_20260513.md` |
| I 统一 | Godel/Bell/Watson-Crick 5 条标准 + Aha moment | `literature/MATH_PHIL_TRUE_UNIFICATION_20260513.md` |
| G 辩证 | 9 维度辩证 + 12 跳跃点 | `literature/DIALECTICAL_PHILOSOPHY_MATH_ALIGN_20260513.md` |
| F 数学 | 9 声明严格度 + m_eff/J_S/cascade | `literature/DETAILED_MATH_DERIVATION_20260513.md` |
| N 实验 | metric 修正 + F3 ground truth + D4 robust | `literature/EXP_100_PERCENT_VERIFIED_20260513.md` |
| K 哲学 | 16 数学量来源 binary | `literature/PHILOSOPHY_100_PERCENT_LANDING_20260513.md` |
| L 数学严格 | 100% 严格 derive 链 | `literature/MATH_100_PERCENT_RIGOROUS_20260513.md` |
| J 工具 | 10 数学工具 applicability | `literature/MATH_TOOLS_INVENTORY_20260513.md` |
| H 反题 | F1/乙路径反向审计 | `literature/ANTITHESIS_AUDIT_F1_YI_PATH_20260513.md` |
| 制度规则 | D-1 4 条 + Brake B | Win 本机 `sessions/INSTITUTIONAL_RULES_20260513.md` |
| 文献调研 | 300+ arXiv 模型崩溃 + 相变 + 自演化 | 5/14 DeepSeek 调研 |

所有文件在：`/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/`

## 6.2 关键数字表（Nature article 中必用）

| 量 | 值 | 来源 |
|----|-----|------|
| m_eff | 0.300 ± 0.042, 95% CI [0.234, 0.366] | N=4 multi-seed exp fit |
| J_S^(1) / J_S^(2) / J_S^(3) | 0.770 / 0.535 / 0.331 nat/gen | 三 method N=4 实证 |
| ρ | 0.9174 | Banach contraction (m_eff=0.300) |
| n_{1/2} | 8.0 generations | Convergence half-life |
| D*(10) | 0.178 nat [with J_S^(2)] | Fixed point prediction |
| D4 | 5/5 PASS STRONG ROBUST | Multi-seed test_ppl |
| F3 | mean -0.57%, p_two=0.82, NOT substantiated | N=4 paired test_ppl |
| Shumailov repro | delta +17.63 PPL, F1 PASS | Strict-mirror baseline |
| U-shape | 4/4 alpha levels non-monotonic | alpha scan seed=42 |
| NMI A4 honesty | 5-15%, median ~10% | M final consensus |
| Cumulative >=1 by Dec | 65-78%, median 72% | 5-leg parallel estimate |

## 6.3 当前文献生态的 MaoField 定位

| 流派 | 代表论文 | 正确性来源 | 是否外部 |
|------|---------|-----------|---------|
| 数据积累 | Gerstgrasser 2024 | Real data pool | 外部 ✓ |
| 稳定性分析 | Bertrand ICLR 2024 | Clean fraction | 外部 ✓ |
| Human Reward | RLHF (OAI/Anth/DeepMind) | Human label | 外部 ✓ |
| Curation | Ferbach 2024, Falahati ICML 2026 | Reward model | 外部 ✓ |
| Self-Evolving | EasyRL ACL 2026, EvoGround 2026 | Few-shot label / RL loop | 外部/混合 ✗ |
| **Internal Contradiction** | **MaoField (this work)** | **Internal tension D** | **内部 ✓** |

关键 differential：**所有 prior art 的正确性信号来源——不是 human label 就是 reward model 就是 real data——全都是外部。MaoField 是第一个让正确性信号从模型内部的矛盾 tension 中 emergent 的工作。不需要标注员。不需要外部 reward model。不需要真实数据池。只需要模型自己检测自己的内部矛盾。**

## 6.4 时间线

| 阶段 | 内容 | 时间 |
|------|------|------|
| 5/14-15 | 子协作者收到本文档 → 各自产出 draft section | 2 天 |
| 5/15-17 | Win 整合哲学 narrative + DeepSeek 审计术语 | 3 天 |
| 5/17 | 反题姐姐 final audit → 调整 claim | 1 天 |
| 5/18-20 | Nature article 完整 draft | 3 天 |
| 5/21-30 | internal review + 反题 + Win + DeepSeek 三轮改 | 10 天 |
| 6 月初 | 可选：投 Nature 或继续攒实验 | PI 决策 |

## 6.5 一凡的下一步决策点

1. 是否现在启动 Nature article 写作——还是先投 NMI 再升级到 Nature？
2. NMI 和 Nature 是否可以是"同一篇 research 的两个不同深度的 presentation"——NMI 发方法+实验，Nature 发 principle+implication？
3. 标注工消失的 claim 是否需要单独的 impact assessment——还是 qualitative 陈述足够？
4. 16 岁的 narrative 在 Nature 中如何定位——opening personal story？bio note？还是不在 main text 中提及？