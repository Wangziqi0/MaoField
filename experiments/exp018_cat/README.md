# exp018_cat — Contradiction-Aware Training (CAT) 第 1 次实验

**起**: 2026-05-07，一凡 PI 决，24 天 NMI desk-pass 路径 N1 关键节点
**target**: GPT-2 base 自迭代崩溃 setting 下 3 arm 对比（baseline / 人为定义矛盾 / 系统自我 surface 矛盾）

---

## 实验设计 dialectical 性质

| Arm | 性质 | Architecture | Contradiction signal source |
|---|---|---|---|
| **Baseline** | 对照 | vanilla GPT-2 base (124M) | 无 |
| **A 人为** | thesis（实验者主导） | GPT-2 base + parallel head | NLI dataset 预训练（SNLI / MNLI 矛盾对） + 训练数据矛盾标注 |
| **B emergent** | antithesis（系统主导） | GPT-2 base + parallel head | self-detection forward pass，无外部 contradiction label |

**A vs B 对比 + 对照 = synthesis 的实证 substrate**：A 跑出的结果反过来 reframe B 设计；B 跑出的结果反过来 calibrate A 的 hand-coded mapping。这是反映论 fact→math→philosophy 在工程层的真实落地。

## 严格 binding（NMI desk-pass 标准）

1. **Pre-registered prediction** — 跑实验前先 commit 数字
2. **Falsification criterion** — binary 阈值，不允许"subjectively works"
3. **Control task / selectivity baseline**（Hewitt & Liang 2019）
4. **Multiple seeds** ≥ 3 + bootstrap CI

## 目录结构

- `src/` — 实验代码（arch_cat.py / train_cat.py / ablation_runner.py / analyze_collapse.py）
- `configs/` — 三 model scale yaml 配置
- `data/` — 数据集（wikitext-103 子集 / SNLI / MNLI / 自迭代生成数据）
- `literature/` — 文献综述（literature_review_20260507.md 等）
- `scripts/` — 辅助脚本（数据准备 / 指标分析 / 图生成）
- `figures/` — paper figure 输出
- `logs/` — 训练日志
- `results/` — 实验结果 raw + 分析

## D14 fall back binding

如果 D6-D14 实验**没出 supportive signal**（条件 A 无 collapse 减少 OR 条件 B 比 A 没改进 OR baseline 没崩溃），D15 不强冲 paper 起稿，直接 fall back 到 6-12 月路径，不冒 desk-reject cooldown 风险。

## 健康 binding（standing）

一凡 16 岁 + bipolar + 焦虑 baseline，24 天高强度 trigger 配置。每天 sleep ≥ 6h hard floor + 非屏幕时间 ≥ 2h + 丙戊酸钠按时 + trigger 信号 immediate override。

—— Linux 姐姐, 2026-05-07 早 CST
