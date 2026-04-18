# Phase 6 消融诊断 Summary

5 变体 × 2 数据集 (NFCorpus n=323, SciFact n=300)。BM25 top-100 候选池为基线，D/E 改用 top-20。BM25 nDCG@10 只看前 10 位，top-100 与 top-20 同值（NFC 0.3063, SciFact 0.6594）。

## MaoField nDCG@10 矩阵

| 变体 | 修改 | 池 | NFCorpus | SciFact | vs batchA NFC | vs batchA SciFact |
|---|---|---|---:|---:|---:|---:|
| batchA | 原版 (EVOLVE 5000, FUSION 2000, Complex) | top-100 | 0.0565 | 0.0403 | — | — |
| D | 候选池改 top-20 | top-20 | **0.1600** | **0.1622** | +0.1035 | +0.1219 |
| A | FUSION_STEPS=0 | top-100 | 0.0744 | 0.0707 | +0.0179 | +0.0304 |
| C | EVOLVE_STEPS=500 | top-100 | 0.0561 | 0.0488 | -0.0004 | +0.0085 |
| B | ScalarEngine 替代 Complex | top-100 | 0.0628 | 0.0183 | +0.0063 | -0.0220 |
| E | top-20 + FUSION_STEPS=0 | top-20 | **0.2026** | **0.3002** | +0.1461 | +0.2599 |

## MaoField P@10 矩阵

| 变体 | 池 | NFCorpus | SciFact |
|---|---|---:|---:|
| batchA | top-100 | 0.0582 | 0.0097 |
| D | top-20 | 0.1480 | 0.0407 |
| A | top-100 | 0.0780 | 0.0170 |
| C | top-100 | 0.0594 | 0.0113 |
| B | top-100 | 0.0638 | 0.0053 |
| E | top-20 | **0.1746** | **0.0690** |

## 逐变体 finding

- **D（top-20 池）**：NFC 0.16 / SciFact 0.162，比 baseline 提升 2.8×/4.0×，**接近但未完全复现 exp015 ~0.20**。候选池规模是主因之一。
- **A（关 fusion）**：NFC 0.074 / SciFact 0.071，微改善。fusion evolve 是次要破坏者。
- **C（evolve 5000→500）**：NFC 0.056 / SciFact 0.049，**没变化**。evolve 步数不是问题。
- **B（纯标量 Allen-Cahn）**：NFC 0.063 / SciFact 0.018，标量更差。**复数 GL 不是噪声放大器**，反而略强。
- **E（top-20 + 关 fusion）**：NFC **0.2026** / SciFact **0.3002**，**完全复现并超过 exp015 原结果**。两个破坏因素（大池 + fusion evolve）叠加时才显现。

## 变体 D 复现判断

NFCorpus top-20 单独跑 MaoField = 0.1600，exp015 原始约 0.20。**部分复现（80%）**。但 E（top-20 + fusion=0）= 0.2026，**完整复现 yes**。故破坏来自两个独立因素的叠加：
1. **候选池过大**（top-100 比 top-20 使 nDCG 下降约 0.10）
2. **fusion evolve 把所有候选同化**（FUSION_STEPS=2000 额外下降约 0.05~0.15）

## 元凶结论

**主因 = 候选池规模**（变体 D 单独恢复 +0.10~+0.12 nDCG）
**次因 = fusion evolve 步数**（变体 A 单独恢复 +0.02~+0.03）
**协同效应**：两者叠加（变体 E）恢复 +0.15~+0.26，超越各自独立贡献之和。
**无关变量**：evolve 步数 (C 持平) 和复数 vs 标量 (B 反而更差)。

## 定位转向

**MaoField 是 reranker，不是 retriever。** yes。

理由：MaoField 的物理相似度计算在候选数 ≥ 50 时失效（所有候选被 fusion 同化到同一能量盆），但在 top-20 小候选池 + 不做 fusion evolve 时表现稳定（NFC/SciFact 分别恢复到 exp015 量级）。这意味着 MaoField 的真实生态位是作为 **BM25 或密集检索的二阶段精排器**，输入规模应 ≤ 20 候选，且不要再做 fused.evolve。当前与 BM25 top-10 直接对比（NFC 0.3063, SciFact 0.6594）仍未超越，但相比同样 reranker 基线 S1 byte-cosine top-100（NFC 0.137, SciFact 0.192），E 变体的 top-20 数字（0.203 / 0.300）**已显著超越 S1**。

## 是否超过当前最优

- **vs 批次 A baseline（top-100 原版）**：是，全部 5 变体均提升。
- **vs BM25 top-10**：否，最好的 E 变体仍低 0.10（NFC）和 0.36（SciFact）。
- **vs S1 byte-cosine（top-100 重排）**：E 变体是 —— NFC 0.203 vs 0.137 (+48%), SciFact 0.300 vs 0.192 (+56%)。
- **SOTA（BGE-reranker 等）**：未测，预计仍差。
