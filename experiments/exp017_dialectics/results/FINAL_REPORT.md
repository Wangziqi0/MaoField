---
name: exp017 辩证法四重检验 — 最终归档报告
date: 2026-04-13
authors: em × Win Claude × Linux Claude
purpose: exp017 dialectics 实验全部数据归档（Block I-IV + IV.5 Stage C），不含哲学判读（见分离文件 philosophical_interpretation.md）
status: data archive, no conclusions drawn herein
---

# exp017 FINAL REPORT

## Section 1：Setup

### 1.1 实验目的
四重检验 MaoField 的物理假说：
- H1（运动到融合）：Kuramoto 耦合替代显式 fusion 能否提升 ≥20%？
- H2（矛盾主次质变）：有效 attractor 数是否有限？是否解释了 top-20/top-100 的性能差？
- H3（物质起点）：相同 PDE 算子下，字节源场（唯物）vs embedding 源场（唯心）是否展示不同能力？

### 1.2 实验范围
- Block I：5 数据集 × 6 scorer 基线矩阵
- Block II：Kuramoto diffusive 耦合 g 扫描
- Block III：Attractor 数量诊断（单源场）
- Block IV：唯物/唯心四组对照 + 五维评估
- Block IV.5 Stage C：Phase 诊断（症结定位）

### 1.3 公共配置
- PDE engine：exp015 `ComplexEngine`，GL 势 `V=¼(|ψ|²−1)²`，Allen-Cahn 版
- 网格：3D 32³ = 32768 voxels
- Evolve steps：5000（reranker 配置）或 2000（Block II 耦合版）
- 候选池：BM25 top-K，K ∈ {6, 20, 100} 视任务
- 随机种子：20260412 / 20260413
- 数据集：BEIR 子集（NFCorpus, SciFact, FiQA, ArguAna, TREC-COVID）+ CodeSearchNet (D7)
- 评估：nDCG@10 / P@10 / MRR@10，BEIR 标准

### 1.4 硬件
- Linux server 192.168.31.36：256 核 EPYC 7B13 CPU，503G RAM
- Linux server 192.168.31.22：RX 9070 XT (gfx1201) ROCm + llama.cpp，跑 bge-m3 embedding (:8080) + bge-reranker-v2-m3 (:8081)

---

## Section 2：Block I–IV 完整数据

### 2.1 Block I：5 数据集 × 6 scorer 基线矩阵（nDCG@10）

| dataset | BM25 | S1 byte | S4 3gram | BGE-reranker | MaoField_base | MaoField_E |
|---|---:|---:|---:|---:|---:|---:|
| NFCorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | 0.2026 |
| SciFact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | 0.3002 |
| FiQA | 0.2167 | 0.0686 | 0.1163 | 0.2992 | 0.0294 | 0.1082 |
| ArguAna | 0.2838 | 0.0556 | 0.2085 | 0.4560 | 0.0289 | 0.1514 |
| TREC-COVID | 0.5589 | 0.4299 | 0.3962 | 0.7257 | 0.3553 | 0.4932 |

**观察**：
- MaoField_E vs S1：5 数据集全部正增益，相对提升 +14.7% ~ +172.3%
- MaoField_E vs BGE-reranker：5 数据集全线落后，差 −10.8 ~ −32.2 pp
- MaoField_E vs MaoField_base：5 数据集全部显著提升，+7.9 ~ +26.0 pp
- BGE-reranker 在 SciFact 低于 BM25（−3.7 pp）

文件：`block1_baselines.csv`, `block1_summary.md`, `block1/*.json` (30 per-query ranks)

### 2.2 Block II：Kuramoto diffusive 耦合 g 扫描

耦合形式：`∂ψ_q/∂t = GL(ψ_q) + g·(ψ_d − ψ_q)`，同步演化 2000 步。

nDCG@10 表（F2 锁相度打分，g_best 为扫描最优）：

| dataset | pool | g=0 | g_best | best g | 相对增益 |
|---|---|---:|---:|---:|---:|
| NFCorpus | top-6 | 0.2201 | 0.2252 | 1.0 | +2.3% |
| NFCorpus | top-20 | 0.1712 | 0.1712 | 0.0 | 0.0% |
| SciFact | top-6 | 0.4082 | 0.4362 | 0.05 | +6.9% |
| SciFact | top-20 | 0.1836 | 0.2179 | 0.05 | **+18.7%** |

**观察**：
- H1 阈值 +20%：最大 +18.7%（SciFact top-20），未达阈值 → **弱证伪**
- g_c 跨数据集不一致（NFC=1.0, SciFact=0.05）
- F3 锁相步数度量粒度过粗（采样 100 步、阈值 0.8），g≥0.05 全部在首次采样锁相，鉴别力低

文件：`block2_scan.csv`, `block2_gc_findings.md`

### 2.3 Block III：Attractor 数量诊断（byte 源场，NFC 100 docs）

每 doc 独立 evolve 5000 步，final state (a,b) 做聚类。

| 表征 | 维度 | 最优 k\* | silhouette |
|---|---:|---:|---:|
| raw_ab | 65536 | **2** | 0.214 |
| amplitude | 32768 | **2** | 0.037 |
| phase (cos/sin) | 65536 | **2** | 0.223 |

**观察**：三表征均指向 k\*=2。

文件：`block3_cluster_k_search.csv`, `block3_summary.md`, `block3_states.bin`

### 2.4 Block IV：唯物/唯心四组对照 + 五维评估

| 维度 | 数据集 | IV-A 唯物动态 | IV-B 唯心动态 | IV-C 唯心静态 | IV-D 唯物静态 |
|---|---|---:|---:|---:|---:|
| 总体 nDCG@10 | NFCorpus | 0.2026 | 0.2495 | **0.3089** | 0.2159 |
| 总体 nDCG@10 | SciFact | 0.3002 | 0.3814 | **0.6143** | 0.3555 |
| 总体 nDCG@10 | FiQA | 0.1082 | 0.1901 | **0.2774** | 0.1309 |
| 长尾 nDCG@10 | NFC n=227 | 0.2117 | 0.2608 | **0.3149** | 0.2264 |
| 长尾 nDCG@10 | SciFact n=3 | **0.6667** | 0.4206 | 0.2854 | 0.2477 |
| 长尾 nDCG@10 | FiQA n=29 | 0.1404 | 0.1551 | **0.2199** | 0.1341 |
| 鲁棒性 drop | SciFact n=200 | −0.010 | +0.011 | −0.015 | +0.031 |
| attractor k\* | NFC 100 doc | **2** (sil 0.13) | **2** (sil 0.06) | N/A | N/A |
| 跨语言 | mMARCO | SKIPPED | SKIPPED | SKIPPED | SKIPPED |

**观察**：
- 三数据集总体 nDCG 排序一致：IV-C > IV-B > IV-D > IV-A
- IV-A（byte+PDE）< IV-D（byte cos）差 −1.3 ~ −5.5 pp
- IV-B（BGE+PDE）< IV-C（BGE cos）差 −5.9 ~ −23.3 pp
- k\*=2 在 IV-A 与 IV-B 均成立（两种源场），silhouette 分别 0.13 与 0.06
- SciFact 长尾 n=3 样本不可信；其余长尾子集排序与总体一致
- 鲁棒性 drop 全部 |drop| < 0.04，差异在噪声内
- 跨语言因 mMARCO 下载问题 SKIP

文件：`block4_matrix.csv`, `block4_summary.md`, `block4/IV-*_*.json`

---

## Section 3：Block IV.5 — 症结诊断与多井干预

### §3.1 Stage C：症结诊断（phase 诊断）

**问题**：k\*=2 在两种不同源场（byte / BGE）都成立。是否来自同一物理机制？若不同，Z_2 对称性各来自哪里？

**方法**：对 IV-A 与 IV-B 的 final states 做 phase 诊断：
- 全局 phase 分布 `|R|`（circular mean resultant，0=均匀，1=全锁定）
- per-doc phase 集中度 `|R|` 均值
- 100 docs 的 circular-mean phase 做 k=2 clustering，看两中心是否反极（180° 分开）

**结果**：

| | 全局 \|R\| | χ²/72 | per-doc \|R\| 均值 | k=2 中心距离 |
|---|---:|---:|---:|---:|
| **IV-A (byte)** | **0.807** | 94989.7 | **0.840** | **26.2°**（非反极）|
| **IV-B (BGE)** | 0.165 | 4879.9 | **0.197** | 81.4° |

**IV-A（byte 稀疏源场）**：
- per-doc |R|=0.84 → 每个 doc 内部 32768 voxel 的 phase 高度集中
- 100 docs 的 mean phase 全部落在 158°~-175° 范围（26° 窄扇区）
- k=2 两中心距离 26° ≠ 180°
- 数据层含义：phase 近似 collapse 到单一方向；k\*=2 在 phase 轴上的分离度很小

**IV-B（BGE 稠密源场）**：
- per-doc |R|=0.20 → phase 近似均匀
- k=2 两中心距离 81°
- 数据层含义：phase 不是主要分离轴；k\*=2 必然来自 amplitude 或 spatial 结构

**Stage C 诊断结论（数据层）**：
Z_2 的来源在两种源场下完全不同：
- byte 路径：arg(ψ) 分布强集中（per-doc |R|=0.84，kmeans-2 中心距 26.2°），U(1) 对称 in the empirical distribution 被破缺，但 phase 未 antipodally split（Z_2 ⊂ U(1) 的 signature 应为两中心分离 π rad = 180°），**Z_2 在 arg(ψ) 分布上未实现** [^zn-loose]
- BGE 路径：amplitude 出现 bimodal 分布 `|ψ|∈{0,1}`；注意 V=¼(|ψ|²−1)² 在 ψ∈ℂ 空间只有 |ψ|=1 是 true minima，ψ=0 是 critical point 但 Hessian 负定（unstable local max/fixed point）；|ψ|=0 与 |ψ|=1 **不同 U(1)-orbit**，不存在交换它们的 Z_2 group action —— "Z_2 amplitude bistability" 仅指 bimodal distribution pattern [^zn-loose]

文件：`block4_5/stageC_verdict.md`, `stageC_phase_diag.json`, `stageC_phase_diag.png`

### §3.2 Stage A1：Multi-well amplitude intervention

**动机**：Stage C 定位了 BGE 路径的 Z_2 源自 amplitude 双井。A1 对此做**干预验证**：若改用三井 amplitude 势函数，k\* 是否上涨？

**设置**：
- 势函数：`V(ψ) = |ψ|²·(|ψ|²−1)²·(|ψ|²−4)²`
- 三个 amplitude minima：|ψ| ∈ {0, 1, 2}
- 源场：BGE-M3 embedding（和 IV-B 一致）
- 数据集：NFCorpus 100 docs（实际评估 70 docs，30 个 doc 无 cached embedding，与 IV-B 同子集）
- Evolve：5000 步，DT=0.05，clamp=3.0
- 初始化：`|ψ|_init ≈ 1.0 ± 0.3`（给系统机会进 u=1 或 u=4 井）
- 其他参数与 IV-B 完全一致

**稳定性**：0 NaN，u_max=1.20，u_mean=1.01，5000 步全程稳定。

**Amplitude 分布结果**：

| 井 | \|ψ\| | u=\|ψ\|² | occupancy |
|---|---|---|---:|
| u=0 | 0 | 0 | **0.85%** |
| u=1 | 1 | 1 | **99.15%** |
| u=4 | 2 | 4 | **0.00%** |

系统实际只激发 1 个井（u=1），u=4 井未被触及（u_max=1.20 << 4）。

**Phase 诊断**（确认多井 amplitude 不诱导 phase 退化）：

| 指标 | A1 | 对照 IV-B |
|---|---:|---:|
| 全局 \|R\| | 0.159 | 0.165 |
| per-doc \|R\| 均值 | 0.185 | 0.197 |
| kmeans-2 antipodal | 57.9° | 81.4° |

phase 保持近均匀，|R| < 0.3，与 IV-B 相当。

**k-means k=2..5 silhouette**（所有三表征最优 k\*）：

| 表征 | k\* | silhouette |
|---|---:|---:|
| raw_ab | 2 | 0.054 |
| amplitude | 2 | 0.150 |
| phase_cos_sin | 2 | 0.055 |

**按 Stage C 预定义规则的判读（数据层）**：
- 不满足 "k\*≥3 + phase 均匀" → 多井势函数**未**把 k\* 提升至 3-5
- 命中 "k\*=2 + phase 均匀（|R|=0.19）" → 多井结构在势函数中存在（V 定义上 u=4 是 minima），但系统**未激发 u=4 井**（occupancy=0%）
- phase 未退化（|R|=0.19 < 0.3），无反例信号

**数据层诊断**（不做哲学判读）：
- 势函数里的三井结构数学上存在（V(u=0,1,4)=0 为 minima）
- 但在当前 init spread（`|ψ|≈1±0.3`，u∈[0.49, 1.69]）与源场 drive（|S|≤1）条件下，系统的能量预算不足跨越 u=1 ↔ u=4 之间的势垒（`V(u=2.5) >> k_B T_eff`）
- 所有 voxel 回落到最近的 u=1 井
- k\*=2 的数值保持，机制与 IV-B 无实质差异

**A1 作为 Stage C 的 intervention 结果（data-driven 陈述）**：

A1 kmeans 结果（k\*=2 across all three representations, silhouette 0.054 / 0.150 / 0.055）表明：The presence of additional wells in `V(ψ)` does not automatically translate to observed attractor multiplication. Under A1's initialization regime (`|ψ|_init ≈ 1.0 ± 0.3`), population of the `|ψ|=2` basin was dynamically suppressed: the amplitude distribution shows **99.15% at |ψ|≈1, 0.85% at |ψ|≈0, and 0.00% at |ψ|≈2** (u_max across all voxels and docs = 1.199, far below the u=4 required to enter the outer well).

Phase distribution remains nearly identical to IV-B (global |R|=0.159 vs IV-B 0.165; per-doc |R|=0.185 vs IV-B 0.197), confirming that multi-well amplitude structure did not induce new phase-domain degeneracy.

This suggests future Block V designs may need to jointly tune the triple (potential shape `V`, initialization distribution `p₀`, source-field amplitude scale), rather than modifying `V` alone. This empirically aligns with **Open Problem 2** (non-equilibrium extensions for the ascending phase of dialectical motion): gradient flow populates locally-reachable minima but cannot explore globally disjoint basins without additional driving mechanisms.

**A1 未测的变体（留 exp018）**：
- A1.2：init spread 放大到 `|ψ|≈1.5±1.0` 跨越鞍点
- A1.3：源场幅值 3-5×
- A1.4：shifted minima `u∈{0,1,2}` 降低外井能垒

文件：`block4_5/a1_verdict.{md,json}`, `a1_states.bin`, `a1_amp_hist.png`, `a1_phase_diag.png`, `a1_cluster_k_search.csv`

---

## Section 4：Core Findings

### 4.1 Fusion-step degrades signal (Block II + exp016)
显式 `fused.evolve_steps(2000)` 在 query-doc 混合场上的额外演化会把判别性同化（Block II g=0 独立演化打分显著优于 exp015 原版；exp016 E 变体无 fusion 比 baseline 提升 +7.9~+26.0 pp 在 5 数据集）。

### 4.2 Double-well GL: k\*=2 masks two distinct symmetry-breaking regimes

Sparse byte sources exhibit distributionally concentrated arg(ψ)（U(1) broken in empirical distribution but not antipodally split — Z_2 ⊂ U(1) not realized）; dense learned embeddings exhibit bimodal amplitude distribution at |ψ|∈{0,1}（no rigorous Z_2 group action, since V(0)=¼ ≠ V(1)=0）. Both yield k\*=2 numerically, but via source-density-coupled mechanisms [^zn-loose]. **Z_n labels below are used in the loose sense of remaining-symmetry-pattern in the empirical distribution, not as rigorous group actions on the field.**

- 稀疏源场（byte）：arg(ψ) 分布强集中到近似单一方向（per-doc |R|=0.84，100 docs mean phase 聚在 26° 内），U(1) 在 empirical distribution 中 appears broken 但 kmeans-2 中心距 26.2° ≠ 180°，**Z_2 phase inversion 的 signature 未出现** [^zn-loose]

[^zn-loose]: 本报告多处使用 "Z_1 / Z_2 / Z_n" 标签，**仅指 empirical distribution 中 observed 的 remaining-symmetry-pattern**，不表示对场 ψ 的严格 group action。严格 Spontaneous Symmetry Breaking (SSB) 需要：(1) group G acting on field space, (2) V 在该 action 下不变, (3) ground-state manifold 是 G-orbit（非 G-invariant 点）, (4) 一个 non-trivially-transforming 的 order parameter ⟨ψ⟩ ≠ 0, (5) 严格 SSB 只在热力学极限 N→∞ 下成立，**有限体系 N=32³ 只表现为 quasi-SSB with tunneling**。本文档中 (3)-(5) 均未严格验证，尤其 (5) 在我们 lattice 下必然违反。Z_n notation 保留作为 empirical distributional pattern 的 compact 描述符号。
- 稠密源场（BGE）：phase 保持近均匀（|R|=0.20），Z_2 来自 amplitude 双井（`|ψ|∈{0,1}`）
- Stage A1 干预（§3.2）进一步显示：多井势函数的数学定义（三井 at `|ψ|∈{0,1,2}`）不足以自动突破 k\*=2；需联合 init 能量 / 源场 drive 设计

### 4.3 Source-density / operator symmetry coupling
两条路径的 attractor capacity 都 = 2，但**物理机制不同**。这意味着源场的信息密度与 PDE 算子的有效对称性不是独立变量，而是**互相耦合**决定 attractor 结构。任何关于 "PDE 算子的内禀 k\*" 的陈述必须限定源场条件。

### 4.4 BGE reranker 非全域优势
在 5 数据集中 BGE 在 SciFact 低于 BM25（−3.7 pp）。SOTA cross-encoder 存在弱域，这对 PDE-based reranker 的定位空间有 suggestive 含义（不在本报告范围内展开）。

### 4.5 MaoField-E vs byte baseline 的正增益模式
5 数据集全部正增益（+14.7 ~ +172.3%）。该模式在 reranker 维度上确立，但总体仍落后 BGE-reranker（−10.8 ~ −32.2 pp）。

---

## Section 5：Future Directions

### 5.1 Multi-well amplitude potentials（A1 initial result in §3.2; full Block V design → exp018）
针对 BGE 路径的 Z_2 来源（amplitude 双井），A1 已给出第一个 data point：三井势 `V(ψ)=|ψ|²(|ψ|²−1)²(|ψ|²−4)²` 在当前 init/source 条件下未激发 u=4 井，k\* 未上涨（§3.2）。exp018 将联合设计势函数 + init 分布 + 源场 drive，验证多井结构在匹配能量条件下的激发。候选变体：A1.2（init spread 放大）、A1.3（source 幅值放大）、A1.4（shifted minima `u∈{0,1,2}`）。

### 5.2 Spatial anisotropy breaking（A2 → exp018）
针对 byte 路径的 phase collapse，引入空间异性项（如位置依赖的 Allen-Cahn 系数）打破全局 phase 对齐，使不同 doc 落到不同 phase basin。

### 5.3 Symmetry group design

> **Design principle for Block V**: The central question is not "how many wells" but "what symmetry group."

候选对称群：
- Z_n (n≥3)：加 `cos(n·arg(ψ))` 项破 U(1) 到 Z_n
- 完整 U(1)：设计势使 minima 成为连续圆轨（Goldstone 模保留）
- non-Abelian（SU(2) 等）：多分量场 + 规范耦合，attractor 成为带纤维结构的流形

### 5.4 Manifold-aware evaluation metrics
对 Section 5.3 的路径 β/γ，k-means + silhouette 的 point-cloud 假设失效。需引入：
- Persistent homology（TDA）刻画 basin 拓扑
- Manifold learning（UMAP, diffusion maps）捕捉连续结构
- Geodesic-aware clustering

### 5.5 已标记的 Open Problems（供 arXiv v1 引用）
- **OP1**：Axiom 6（匹配即自我训练）的严格数学形式（M2 iteration 的 contraction property）
- **OP2**：Axiom 3 的 non-equilibrium 扩展（Hamiltonian / stochastic / non-variational 项）对应"否定之否定"的上升运动

---

## Section 6：Artifacts & Reproducibility

### 6.1 代码
- Rust engines：
  - `exp015/rust_solver/` — 原 GL + fusion
  - `exp016/rust_variants/variant_{A,B,C,E}/` — 5 消融变体
  - `exp017_dialectics/rust_variants/block2_coupled/` — 耦合同步演化
  - `exp017_dialectics/rust_variants/block3_dumper/` — final-state dumper
  - `exp017_dialectics/rust_variants/block4_idealist/` — BGE source PDE
  - `exp017_dialectics/rust_variants/block4_dumper/` — BGE dumper
- Python 诊断：
  - `exp016_diagnostic/src/phase1_auc.py` — 6 度量 AUC
  - `exp017_dialectics/src/block3_cluster.py` — attractor 聚类
  - `exp017_dialectics/src/block4_5_phase_diag.py` — phase 诊断

### 6.2 数据
- BEIR：`/home/amd/HEZIMENG/legal-assistant/beir_data/`（含 NFCorpus/SciFact/FiQA/ArguAna/TREC-COVID/Quora）
- CodeSearchNet：`exp016_diagnostic/data/codesearchnet/`（10k 样本）
- BGE embeddings cache：`exp017_dialectics/results/block4/embeddings_{dataset}.npz`（~370MB 三数据集）

### 6.3 服务
- BGE-M3 embedding server：`http://192.168.31.22:8080/v1/embeddings`（9070XT, HIP_VISIBLE_DEVICES=0）
- BGE-reranker-v2-m3 server：`http://192.168.31.22:8081/v1/rerank`（batch=4096 after fix）

### 6.4 核心 CSV / MD 清单
```
exp017_dialectics/results/
├── block1_baselines.csv           # 5×6 nDCG matrix
├── block1_summary.md
├── block2_scan.csv                # 耦合 g 扫描
├── block2_gc_findings.md
├── block3_cluster_k_search.csv    # attractor silhouette
├── block3_summary.md
├── block4/
│   ├── block4_matrix.csv          # 4 组 × 3 数据集 × 5 维
│   ├── block4_summary.md
│   ├── IV-{A,B,C,D}_{ds}_out.json
│   ├── dim3_robustness.csv
│   ├── dim4_attractor_k.csv
│   └── dim5_crosslingual.csv      # SKIP 说明
├── block4_5/
│   ├── stageC_verdict.md
│   ├── stageC_phase_diag.json
│   └── stageC_phase_diag.png
└── FINAL_REPORT.md                # 本文件
```

### 6.5 哲学判读（分离归档）
Philosophical interpretation of Block IV findings is maintained in a separate document (`./philosophical_interpretation.md`, currently in preparation). This document covers:
- Why BGE-cosine static wins do not constitute an "idealist" victory (reflection theory analysis)
- The degenerate forms of dialectical motion realized by current PDE implementations
- Implications for the Axiom 5 potential-summation reframe
- Interpretation of Stage A1's non-excitation as "material conditions constrain dialectical realization"

arXiv v1 Sections 2-3 contain the formalized mathematical and categorical framework; Lawvere-monad章节（Section 2.3）以 Stage C 两路径分裂与 Stage A1 为 physical illustrations。

### 6.6 未纳入的后续工作
- **A1.2/A1.3/A1.4（A1 的参数变体）**：基于 §3.2 初步结果设计的补充实验，进 exp018。
- **A2 实验（spatial anisotropy，byte 路径）**：exp018 待启动。
- **Lawvere-monad 数学章节**：Linux Claude 起草中，供 arXiv v1 Section 2.3 使用。

---

*本报告生成于 2026-04-13。归档版本 v1。任何后续修改以 v2, v3 标注，不覆写本文件。*

*exp017 由 em（一凡）提出、Win Claude 设计判读、Linux Claude 执行验证。三方协作于 2026-04-12 — 2026-04-13。*
