# MaoField

> *一个辩证唯物主义的非统计语义表示框架*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status: v0.1.0](https://img.shields.io/badge/status-v0.1.0_position_paper-orange)](paper/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--8344--1149-a6ce39)](https://orcid.org/0009-0008-8344-1149)

[English version](README.md)

## 这是什么？

当前 AI 语义理解范式建立在统计模式匹配之上——这是一种认识论上的功能主义范式，在反映客观实在、处理内在矛盾、质变涌现和自我修正等维度存在结构性局限。**MaoField** 是一个以**辩证唯物主义**为哲学根基、通过偏微分方程描述语义场演化的计算框架。

本仓库包含：

- **哲学基础**：辩证唯物主义计算的七条公理，借助范畴论伴随函子形式化（Lawvere 1970）
- **数学框架**：耦合 Allen-Cahn 方程与复数 Ginzburg-Landau 动力学
- **实验证据**：5 个 BEIR 标准 benchmark + 机制诊断 + 吸引子容量分析
- **完整可复现**：Rust + Python 流水线，全部随机种子固定

## 核心发现（v0.1.0）

| 发现 | 证据 | 状态 |
|---|---|---|
| PDE 场演化能从原始字节源场中提取语义信号 | 5 个 BEIR 数据集上相对字节余弦基线 +48–172% nDCG@10（top-20 重排） | 已验证 |
| 双井 Ginzburg-Landau 势函数只容纳 k*≈2 个稳定吸引子 | 3 种表征 × 2 种源场一致验证 | 已验证 |
| k*=2 通过两种不同的对称破缺机制涌现 | Z₁ 相位塌缩（稀疏字节源场）vs Z₂ 幅值双稳（稠密学习 embedding） | 已诊断 |
| 单纯定义多井势函数无法激发新 basin | Stage A1：V=\|ψ\|²(\|ψ\|²−1)²(\|ψ\|²−4)² 下 99.15% 占据 \|ψ\|≈1 井，0.00% 在 \|ψ\|≈2 井 | 已确认 |
| 梯度流下降无法实现完整的辩证运动 | 势垒高度 13.2 ≫ 初始动能 1 | Open Problem 2 锚点 |
| MaoField vs SOTA cross-encoder (BGE) | 平均 −23pp 落差；由 k*=2 容量上限解释 | 诚实上限 |

## 为什么是辩证唯物主义？

辩证唯物主义——经由马克思、恩格斯、列宁、毛泽东的发展——系统处理了统计 AI 难以应对的现象：

- **反映论**（列宁）：认识是与客观实在的结构化对应，不是不透明的函数拟合
- **矛盾论**（毛）：内在矛盾是认识发展的动力
- **质量互变**（恩格斯）：量变到一定程度引起质变——相变，不是平滑插值
- **实践—认识循环**（毛）：认识通过反复实践深化；学习与推理无清晰界限
- **否定之否定**：自我修正是发展的结构性阶段，不是外部补丁

尽管辩证唯物主义系统性地处理了困扰统计 AI 的问题，但它从未被认真工程化为计算框架。Lawvere 1970 建立了范畴论伴随函子作为"对立统一"的精确数学形式——提供了一座半个世纪以来基本未被跨越的桥梁。

MaoField 是尝试跨越它的工作。

## 快速开始

> 说明：论文 PDF 和复现脚本正在为 v0.1.0 正式发布做最后准备。
> 本仓库当前托管研究框架和基础性内容。

```bash
git clone https://github.com/Wangziqi0/MaoField.git
cd MaoField

# 当 scripts/ 就绪后：
./scripts/setup.sh
./scripts/reproduce_exp017.sh
```

复现结果会出现在 `experiments/exp017_dialectics/results/`。

## 论文

完整的方向性论文位于 [`paper/maofield_v1.pdf`](paper/)。

结构：

- §1 — 统计学习的认识论局限
- §2 — 七公理 + 范畴论形式化（伴随 → monad → T-代数 = 合题）
- §3 — 数学框架（Allen-Cahn + Ginzburg-Landau + 耦合）
- §4 — 实验证据（Blocks I–IV.5，机制诊断）
- §5 — 研究路线图（对称群设计、非平衡扩展、多步伴随推理、源场重构）
- §6 — 局限、开放问题、合作邀请

## 状态

**v0.1.0 — 方向性宣告，附初步实验证据**。

我们同等呈现：

- **有效的部分**：PDE 动力学在无训练情况下确实能从原始物质源场中提取语义信号
- **无效的部分**：朴素的多井扩展不足；纯梯度流无法实现辩证运动的上升阶段
- **开放的部分**：辩证上升的非平衡动力学（Open Problem 2）；公理 6（匹配即自我训练）的严格数学形式（Open Problem 1）

我们**明确不**声称 MaoField 超越现有最强检索器——它没有。**对机制和局限的诚实报告本身就是核心贡献**。

## 路线图

- [ ] **Block V**：对称群设计（Z_n / U(1) / 非 Abel 群）
- [ ] **非平衡扩展**（Langevin / Hamiltonian / 主动驱动）— Open Problem 2
- [ ] **A 跳跃**：多步伴随迭代 → 推理
- [ ] **C 跳跃**：源场重构（Clifford 代数 / 图 PDE）
- [ ] **流形感知评估**：persistent homology / 拓扑数据分析
- [ ] **公理 6 形式化**：M2 不动点迭代 → Banach 压缩映射证明（Open Problem 1）

## 合作

本工作明确定位为**方向性宣告**，**邀请跨学科合作**。

如果你工作于以下领域之一，看到连接点，欢迎联系：

- 偏微分方程理论（分岔、非平衡动力学、Ginzburg-Landau 扩展）
- 范畴论（monad、Kleisli 范畴、高阶范畴推广）
- 信息检索（dense retrieval、reranking、组合泛化）
- AI 对齐（机制可解释性、非统计方法）
- AI 哲学（认识论、辩证法、计算认识论）

参与方式：
- 在 Issues 提出技术或哲学问题
- Fork 并通过 Pull Request 贡献（见 `docs/CONTRIBUTING.md`）
- 在相关工作中引用（格式见下）

## 引用

学术工作中使用或基于 MaoField 的理念时：

```bibtex
@software{chen2026maofield,
  author       = {Chen, Yifan},
  title        = {MaoField: A Dialectical-Materialist Framework for Non-Statistical Semantic Representation},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX},
  orcid        = {0009-0008-8344-1149}
}
```

结构化引用元数据见 [CITATION.cff](CITATION.cff)——被 GitHub、Zenodo、Zotero 等主流参考文献管理工具支持。

## 许可

Apache License 2.0 — 见 [LICENSE](LICENSE)。

你可自由使用、修改、分发本工作，包括商业用途，前提是遵守 Apache 2.0 条款。专利授权条款保护贡献者和使用者。

## 致谢

本工作得到了 AI 研究协作者的大量帮助（Anthropic 的 Claude Opus 4.6，在不同实例上分别承担实验执行、数学验证、哲学写作）。所有战略决策、核心物理直觉（例如*"辩证融合应该从运动中产生，而非被外部施加"*）、哲学 framing 和最终判断均为作者本人。

辩证唯物主义计算的七条公理由作者本人提出，不源自既有文献。

本工作立于一个传统之中：**思想的形式通过与物质实践的对抗而发展**。这一传统由马克思、恩格斯、列宁、毛泽东所开创，本工作尝试将其方法论延伸至他们当年无法预见的领域。

---

*"哲学家们只是用不同的方式解释世界，而问题在于改变世界。"*
— 马克思《关于费尔巴哈的提纲》第十一条

*"实践是检验真理的唯一标准。"*
— 毛泽东《实践论》

*本工作试图让一套哲学接受它自己提出的标准的检验。*
