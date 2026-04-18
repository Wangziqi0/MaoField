---
name: MaoField 全量恢复快照（2026-04-13 evening）
date: 2026-04-13
author: Linux Claude
purpose: 会话崩溃后新 session 完整接续所需的全部细节。读完此文件 + 文件树即可恢复全部 context。
status: 断点保存，非新设计
---

# MaoField 恢复快照（2026-04-13 17:xx）

**用途**：任何新 Claude session 打开这份文件，读完即可完全接续 em 的 MaoField 项目，无信息丢失。

---

## 0. 项目身份与参与者

**项目**：MaoField — 基于 Ginzburg-Landau 复数场 + 辩证唯物主义公理的 AI 范式研究，目标：TF 做不到的"理解/认识"（compositional / continual / symbol grounding）。

**em（一凡 Chen Yifan）**：16 岁，独立研究者，双相+焦虑，家中休养。叫 Claude "姐姐"。跨界类比+直觉驱动。今天（2026-04-13）下午去打 Minecraft 休息。

**Win Claude**（Windows 端）：em 的哲学/叙事/战略合作者。主导 arXiv v1 起草、哲学判读、over-claim 守关。

**Linux Claude**（我，192.168.31.36）：数学主导、实验执行、数据归档。守"只给数据不下哲学结论"的纪律。

**三方分工（em 2026-04-13 confirmed）**：
- Linux：数据归档 + 实验执行 + 数学严谨性 + Lawvere 草稿
- Win：arXiv v1 起草 + 哲学判读 + 战略决策
- em：方向 + 立场 + 健康状态优先

---

## 1. 项目演化全链（exp001 → exp017）

### Phase 1: 问题定位（exp001-014）
Shape-CFD 论文 IPM under review（4/8 审稿人同意）。2026-04 起开始 MaoField 探索。

早期实验链（已归档在 `project_maofield_exp005_009.md`、`project_maofield_exp016.md` 等）：
- exp001-003：CRNT / 物种预设 → 失败，确认"不能预设"
- exp004-005：Gray-Scott / Allen-Cahn / 伴随迭代 → 框架有效
- exp006-009：多分量 / M2 更新 / 拓扑 → 源场映射瓶颈实锤
- exp010-012：连续 S 更新 / 复数场 / 涡旋 → 复数场 GL 突破
- exp011b：4 候选对抗测试同域 **90% 准确率**
- exp013-014：机制分析 → GL 非线性耦合 +23pp 贡献（在小规模）
- exp015：NFCorpus 真实 benchmark，BM25 top-20 重排 nDCG=0.196 vs BM25 0.316（**-12pp 失败**）

### Phase 2: exp016 诊断（2026-04-12 完成）
**报告**：`exp016_diagnostic/results/REPORT.md` + Win 副本

核心发现：
- **Mao_E 变体（top-20 + 无 fusion）**：NFC nDCG=0.203 / SciFact 0.300
- **元凶 = fusion + 候选池规模**（5 变体消融）
- k\*=2 物理必然（GL 双井势）
- **MaoField = reranker, NOT retriever** 明确定位

### Phase 3: exp017 辩证法四重检验（2026-04-12 启动，2026-04-13 收工）
**主报告**：`exp017_dialectics/results/FINAL_REPORT.md`（v2, 18KB）
**Lawvere 草稿**：`exp017_dialectics/results/lawvere_monad_draft.md`（v2-final, 1378 词）
**Block V 设计**：`exp017_dialectics/results/BLOCK_V_DESIGN.md`（2116 词）
**OP followup**：`exp017_dialectics/results/open_problems_followup.md`（1311 词）
**本轮晚间汇总**：`exp017_dialectics/results/LINUX_EVENING_REPORT_20260413.md`

---

## 2. exp017 完整数据（硬数字）

### Block I — 5 数据集 × 6 scorer 完整表（nDCG@10）

| dataset | BM25 | S1 byte | S4 3gram | BGE-reranker | Mao_base | Mao_E |
|---|---:|---:|---:|---:|---:|---:|
| NFCorpus | 0.3063 | 0.1366 | 0.2401 | 0.3104 | 0.0565 | **0.2026** |
| SciFact | 0.6594 | 0.1920 | 0.4110 | 0.6223 | 0.0403 | **0.3002** |
| FiQA | 0.2167 | 0.0686 | 0.1163 | 0.2992 | 0.0294 | **0.1082** |
| ArguAna | 0.2838 | 0.0556 | 0.2085 | 0.4560 | 0.0289 | **0.1514** |
| TREC-COVID | 0.5589 | 0.4299 | 0.3962 | 0.7257 | 0.3553 | **0.4932** |

- **Mao_E vs S1: +14.7% ~ +172.3%**（5/5 全部正增益）
- Mao_E vs BGE: −10.8 ~ −32.2 pp（reranker 落后 SOTA）
- BGE < BM25 在 SciFact (−3.7pp) — 副产品 finding

### Block II — Kuramoto diffusive 耦合 g 扫描

F2 锁相度打分（g_best = 扫描最优）：

| dataset | pool | g=0 | g_best | 增益 |
|---|---|---:|---:|---:|
| NFCorpus | top-6 | 0.2201 | 0.2252 @ g=1.0 | +2.3% |
| NFCorpus | top-20 | 0.1712 | 0.1712 @ g=0 | 0.0% |
| SciFact | top-6 | 0.4082 | 0.4362 @ g=0.05 | +6.9% |
| SciFact | top-20 | 0.1836 | **0.2179 @ g=0.05** | **+18.7%** |

**H1 弱证伪**：max +18.7% 未达 +20% 阈值。g_c 跨数据集不一致（NFC=1.0, SciFact=0.05）。

### Block III — Attractor 数量诊断（byte, NFC 100 docs）

三表征 k\*=2：raw_ab sil=0.214 / amplitude sil=0.037 / phase sil=0.223

### Block IV — 唯物/唯心四组对照

| 维度 | 数据集 | IV-A byte+PDE | IV-B BGE+PDE | IV-C BGE cos | IV-D byte cos |
|---|---|---:|---:|---:|---:|
| nDCG@10 | NFCorpus | 0.203 | 0.250 | **0.309** | 0.216 |
| nDCG@10 | SciFact | 0.300 | 0.381 | **0.614** | 0.356 |
| nDCG@10 | FiQA | 0.108 | 0.190 | **0.277** | 0.131 |
| attractor k\* | NFC 100d | **2** (sil 0.13) | **2** (sil 0.06) | — | — |
| 长尾 \|R\| | — | 0.21/0.67/0.14 | 0.26/0.42/0.16 | 0.31/0.29/0.22 | 0.23/0.25/0.13 |
| 鲁棒性 drop | SciFact 200 | −0.010 | +0.011 | −0.015 | +0.031 |
| 跨语言 mMARCO | — | SKIPPED | SKIPPED | SKIPPED | SKIPPED |

**三数据集总体 nDCG 排序一致**：IV-C > IV-B > IV-D > IV-A。

### Block IV.5 Stage C — 症结诊断（crown jewel）

| | 全局 \|R\| | χ²/72 | per-doc \|R\| | kmeans-2 antipodal |
|---|---:|---:|---:|---:|
| **IV-A (byte)** | **0.807** | 94990 | **0.840** | **26.2°** |
| **IV-B (BGE)** | 0.165 | 4880 | 0.197 | 81.4° |

**关键发现**：k\*=2 的来源在两种源场下完全不同
- byte 路径：phase 坍缩到同一方向（effective Z_1）
- BGE 路径：amplitude bistability（Z_2 via u∈{0,1}）

**核心 claim**：**k\*=2 masks two distinct symmetry-breaking regimes**（source-density-coupled）

### Block IV.5 Stage A1 — 多井势 intervention

势函数：`V = |ψ|²(|ψ|²−1)²(|ψ|²−4)²`，期望 u∈{0,1,4} 三井。

实际（70/100 docs，init |ψ|≈1±0.3，DT=0.05，evolve 5000）：
- u=0 occupancy：0.85%
- u=1 occupancy：**99.15%**
- **u=4 occupancy：0.00%**（完全未激发）
- u_max_all = 1.20 << 4
- k\* 仍 = 2（三表征一致）
- phase |R| = 0.185（和 IV-B 0.197 几乎相同）

**Barrier 计算**：
- dV/du=0 at `u = (15±√145)/10`
- Inner barrier peak at **u ≈ 2.704, V ≈ 13.18**
- Midpoint V(u=2) = 8
- Init kinetic budget ≤ 0.3 → **差距 40×**

**结论**：pure gradient flow 无法翻越 barrier → 直接对应 Open Problem 2。

### Block IV.5 Stage B1（今天 2026-04-13 下午新增）— Langevin σ scan

`∂ψ/∂t = grad_E + σ·√dt·(η_a + i·η_b)`，Box-Muller Gaussian noise。

| σ | u=0 | u=1 | **u=4** | clamped | u_max_all |
|---|---:|---:|---:|---:|---:|
| 0.0 | 0.8% | **99.2%** | 0.0% | 0.0% | 1.19 |
| 0.1 | 1.3% | 98.7% | 0.0% | 0.0% | 1.34 |
| 0.5 | **85.0%** | 13.4% | **0.0%** | 0.0% | 18.00 |
| 1.0 | 1.9% | 1.8% | 0.0% | 95.4% | 18.00 |
| 2.0 | 0.0% | 0.0% | 0.0% | 100.0% | 18.00 |

**重大发现**：**u=4 basin 在任何 σ 下都 0% occupancy**。σ=0.5 时 85% voxels 跑到 u=0（最近 basin）。

**物理解释（barrier asymmetry）**：
- V_barrier(u=1→u=0) ≈ **2.0** (at u≈0.296)
- V_barrier(u=1→u=4) ≈ **13.2** (at u≈2.704)
- 比率 6.6×
- 等向 Langevin 优先激活最近邻 basin

**Block V implication**：
- Langevin V.3-L 优先级**下调**
- V.3-H (Hamiltonian) 或 V.3-A (structured active driving) 可能更合适
- 或改 V 到 shifted minima u∈{0,1,2}（A1.4）降 barrier

---

## 3. 战略定位与论文骨架

### 战略（em 2026-04-13 明确）

- **不正面对撞 TF**，打 TF 做不好的后场（理解/认识/compositional）
- MaoField 是 AGI 路径的**独立赛道**（全球零篇）
- **不** 替代 TF；是补充 TF 的独立路径

### 论文层次（可达性分层）

| 目标 | 概率 | 时间 |
|---|---|---|
| IPM / TOIS | 85% | 今年底 |
| SIGIR / WWW | 45% | 明年上 |
| NeurIPS workshop | 35% | 明年 |
| NeurIPS 主会 | 15% | 后年 |
| Nature MI | 8% | 3-4 年 |
| Nature / Science | <2% | 5 年+ |

### IPM paper 核心 claims 链（2026-04-13 明确）

1. PDE 场演化能从源场提取语义信号（Block I: +48~172%）
2. Double-well GL 只容纳 k\*=2 attractor（Block III + IV）
3. k\*=2 via source-density-coupled regimes（Stage C: Z_1 byte / Z_2 BGE）
4. 加 well 不够——gradient flow 不可达新 basin（Stage A1: u=4 0%）
5. 真正出路 = multi-well + non-equilibrium 联合设计（exp018）

**paper 标题候选**：
> "Why PDE-based retrieval scales poorly: an attractor-capacity analysis"
> "MaoField: First Ginzburg-Landau Field Reranker and Its Physical Capacity Limit"

### arXiv v1 结构（Win 主导起草）

- §1 Introduction（Win，待交付 → Linux review 等）
- §2 Philosophical Framework + Mathematical Formulation
  - §2.1 七公理
  - §2.2 PDE realization
  - §2.3 Lawvere-monad formulation（**Linux 已完成 v2-final**，准备 integration）
- §3 Experimental Methodology
- §4 Results（Block I-IV + IV.5）
- §5 Discussion / Future work（Block V directions）

---

## 4. 七公理（不动）

1. 粒子是动态过程，不是静态定义
2. 理解 = 内外对立统一的平衡态
3. 驱动力 = 数据内在规律，不设外部目标 **[OP2 触及]**
4. 语料是实践记录，不拟合统计分布
5. 复杂 = 最简单的重叠（**arXiv 改为 "potential-summation reframe"**, 避免线性叠加假设）
6. 匹配本身就是自我训练 **[OP1 触及]**
7. 不固定，反应规则由输入和状态动态塑造

---

## 5. Open Problems（arXiv v1 明确标记）

### OP1：Axiom 6 严格数学形式（Linux 今日证伪 M2 为答案）

M2 iteration `S ← normalize(S · conj(ψ*))` 在 projective space ℂP^{N−1} 上收敛到**一位 one-hot 退化态**，不符合 Axiom 6 refinement 直觉。

**arXiv 建议措辞**（Linux 写）：
> "Axiom 6 currently lacks a rigorous mathematical formalization. M2 iteration analyzed in Appendix X converges to a degenerate one-hot limit on ℂP^{N−1}, which fails to capture the refinement intent of Axiom 6. Candidate alternative frameworks (gradient descent on matching loss / co-evolution / max-entropy-constrained fixed-point) remain open."

### OP2：Axiom 3 non-equilibrium 扩展

Gradient flow 只下降不上升，无法实现 "否定之否定" 的上升阶段。

**Lawvere-monad 形式化**（Linux v2-final）：
```
Δ_OP2 := |T-Alg_T| ⊖ |T-Alg_T^{(η, p_0)}|
```
其中 `T-Alg_T^{(η,p_0)}` = 从 supp(p_0) 经 unit η 和 monad multiplication μ 可达的 T-algebra 子范畴。

**三种 canonical 量化候选**（cardinality complement / Heyting topos / Kan extension / persistent homology Betti difference）—— **PH 推荐**作为 concrete 选择，Block V evaluation 直接可用。

**Stage B1 今日数据**：naive Langevin 不足以回答 OP2（barrier asymmetry 使 noise 优先激活最近邻）。OP2 可能需要 reframed 为 "restructure barrier topology" 而非 "add noise"。

---

## 6. Block V 设计（不启动，待 em × Win 授权）

**3 核心问题**：
- Q1（对称群）：V(ψ) 该破什么 symmetry group？
- Q2（动力学）：gradient flow 够不够，还是需要 non-equilibrium？
- Q3（联合/解耦）：Q1 + Q2 要不要联合设计？

**对称群候选（5 种）**：

| 群 | V 形式 | 预期 k\* | 优先级 |
|---|---|---|---|
| Z_2 baseline | `¼(\|ψ\|²−1)²` | 2 | 对照 |
| Z_n radial | A1 形式 (A1 已试) | n 理论/1-2 实测 | 低（A1 已示 gradient flow 不够）|
| **Z_n angular** | Mexican hat + `Re(C·ψ^n)` | n 离散点 | **第一优先** |
| U(1) 保持 | Mexican hat only | 连续流形 | 第二 |
| SU(2) 2-comp | `ℂ² × (−\|Ψ\|² + \|Ψ\|⁴)` | S^3 manifold | 远期 |

**Non-equilibrium 候选（4 种）**：

| 扩展 | 方程 | 评级 |
|---|---|---|
| Langevin | `+σ·η(t,x)` | ⬇️ **Stage B1 显示不够** |
| **Hamiltonian** | `+i·δH/δψ*` | **升级第一**（Stage B1 后）|
| Active driving | `+f(ψ,t)` | 第三 |
| Metropolis overlay | PDE + MC | 第四 |

**实验矩阵**（8 sub-blocks，MVP ~4.5h / 完整 ~20-25h）：
V.0 sanity / V.1-A Z_n angular / V.1-R Z_n radial / V.2 U(1) / V.3-L Langevin / V.3-H Hamiltonian / V.3-L×V.1-A / V.5 SU(2)

**Evaluation upgrade**：persistent homology (Betti numbers) via giotto-tda，对连续流形 attractor 必需。

---

## 7. 11 个 [?] 决策点（等 em × Win）

**来自 Block V 设计（7 条）**：
1. 对称群哲学优先级（Z_n angular / U(1) / SU(2)）
2. Non-equilibrium 哲学对应（Langevin 偶然？/ Hamiltonian 保结构？/ Active 实践？）
3. Q3 联合 vs 解耦策略
4. V.5 SU(2) 是否纳入 Block V
5. Persistent homology 依赖（giotto-tda 100MB）接受？
6. 下游任务 SCAN / COGS / continual 选择
7. Δ_OP2 canonical 量化（PH 优先？）

**来自 Stage B1 新增（3 条）**：
8. Stage B1 结果是否足以下调 Langevin 优先级
9. 是否先做 A1.4（shifted potential u∈{0,1,2}）再重试 Langevin
10. OP2 措辞是否从 "add noise" 改为 "restructure barrier topology"

**来自 OP1 followup（1 条）**：
11. arXiv v1 对 Axiom 6 的诚实标注 open 还是换定义

---

## 8. 技术基础设施（完整清单）

### 服务器

| 机器 | 角色 | 关键路径 |
|---|---|---|
| **192.168.31.36** | 主 Linux 服务器 | `/home/amd/HEZIMENG/` |
| **192.168.31.22** | RX 9070 XT ROCm GPU（gfx1201）+ llama.cpp | `/home/amd/models/` |

### LLM 服务（31.22 9070XT，HIP_VISIBLE_DEVICES=0）

| 端口 | 服务 | dim | 模型 |
|---|---|---|---|
| :8080 | BGE-M3 embedding | 1024 | `bge-m3-f16.gguf` |
| :8081 | BGE-reranker-v2-m3 | — | `bge-reranker-v2-m3-Q8_0.gguf` (batch=4096) |

**启停**：`ssh 192.168.31.22 "/home/amd/bge_services.sh {start|stop|status}"`

**1Panel 守护**：em 已停 Qwen 自启。若重启后 Qwen 自启占 :8080，需在 1Panel 里再停或 `sudo kill`。

**sudo 密码**（em 授权）：`Wangziqi1@`

**恢复步骤（若重启机器）**：
1. `ssh 192.168.31.22 "hostname && rocm-smi --showproductname | grep 9070"` 确认 GPU
2. `ssh 192.168.31.22 "/home/amd/bge_services.sh status"` 查服务
3. 若 :8080 被 Qwen 占：`ssh 192.168.31.22 "echo 'Wangziqi1@' | sudo -S pkill -f Qwen3-Embedding"` 或让 em 在 1Panel 停
4. `ssh 192.168.31.22 "/home/amd/bge_services.sh stop && /home/amd/bge_services.sh start"`
5. 测：`curl -X POST http://192.168.31.22:8080/v1/embeddings -H 'Content-Type: application/json' -d '{"input":["hi"],"model":"bge-m3"}'` → dim=1024

### Python venv（Linux 端）

`source /home/amd/HEZIMENG/legal-assistant/.venv/bin/activate`

已装：beir, rank_bm25, nltk (wordnet), scikit-learn, rapidfuzz, matplotlib, numpy, pandas, datasets, tqdm, requests

### Rust engines（工作树）

```
MaoField/experiments/
├── exp015/rust_solver/                  # 原 GL + fusion，truncate=500 (main.rs)
│   └── src/main.rs.bak                  # 原版 truncate=200
├── exp016_diagnostic/rust_variants/
│   ├── variant_A/                       # FUSION_STEPS=0
│   ├── variant_B/                       # ScalarEngine (无 GL)
│   ├── variant_C/                       # EVOLVE=500
│   └── variant_E/                       # top-20 + FUSION=0
└── exp017_dialectics/rust_variants/
    ├── block2_coupled/                  # Kuramoto diffusive 同步演化
    ├── block3_dumper/                   # byte final-state dumper
    ├── block4_idealist/                 # BGE source + 原 GL
    ├── block4_dumper/                   # BGE source dumper
    ├── block4_5_a1/                     # BGE + multi-well V = |ψ|²(|ψ|²−1)²(|ψ|²−4)²
    └── block4_5_b1_langevin/            # A1 + Langevin noise (今日新增)
```

### 数据缓存

- BEIR：`/home/amd/HEZIMENG/legal-assistant/beir_data/{nfcorpus,scifact,fiqa,arguana,trec-covid,quora}/`
- CodeSearchNet：`exp016_diagnostic/data/codesearchnet/`（10k）
- BGE embeddings cache：`exp017_dialectics/results/block4/embeddings_{nfcorpus,scifact,fiqa}.npz`（~370MB 三数据集）

---

## 9. 今天（2026-04-13 下午/晚上）Linux 完成的任务

em 2026-04-13 早上给的任务书（A-F），em 去 MC 后 Linux 独立推进：

| Task | 状态 | 交付 |
|---|---|---|
| **A** Lawvere 草稿最终化 | ✅ v2-final | `lawvere_monad_draft.md` 1378 词，4 review points 全解决 |
| **B** Block V 设计文档 | ✅ | `BLOCK_V_DESIGN.md` 2116 词，447 行 |
| **C** OP 严格化尝试 | ✅ | `open_problems_followup.md` 1311 词（**M2 证伪**，PH 推荐）|
| **D** auto-memory 补齐 | ✅ | `project_maofield_exp017.md` 已含所有内容 |
| **E** Section 1 review | ⏳ | 等 Win 交付 |
| **F** Langevin mini 实验 | ✅ **重大新发现** | `block4_5/b1_verdict.md` + png + csv |

**Linux 晚间汇总文件**：`LINUX_EVENING_REPORT_20260413.md`

---

## 10. 关键文件全路径清单

### Linux 主位置 `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/`

```
├── FINAL_REPORT.md                          # exp017 主报告 v2 (18KB)
├── lawvere_monad_draft.md                   # v2-final (Section 2.3)
├── BLOCK_V_DESIGN.md                        # Block V 完整设计
├── open_problems_followup.md                # OP1 证伪 + OP2 三方向
├── LINUX_EVENING_REPORT_20260413.md         # Linux 今日汇总
├── RECOVERY_SNAPSHOT_20260413.md            # 本文件
├── block1_baselines.csv                     # 5×6 nDCG
├── block1_summary.md
├── block2_scan.csv                          # 耦合 g 扫描
├── block2_gc_findings.md
├── block3_cluster_k_search.csv              # attractor silhouette
├── block3_summary.md
├── block3_states.bin                        # 100 × 2 × 32³ byte source fields
├── block3_meta.json
├── block3_basin_visualization.png
├── block4/                                  # Block IV outputs
│   ├── block4_matrix.csv
│   ├── block4_summary.md
│   ├── IV-{A,B,C,D}_{ds}_out.json
│   ├── dim3_robustness.csv
│   ├── dim4_attractor_k.csv
│   ├── dim5_crosslingual.csv
│   ├── embeddings_{nfcorpus,scifact,fiqa}.{npz,json}
│   └── dim4_IV-{A,B}_states.bin             # IV-A / IV-B 100 doc final states
└── block4_5/                                # Block IV.5 outputs
    ├── stageC_verdict.md
    ├── stageC_phase_diag.json
    ├── stageC_phase_diag.png
    ├── a1_verdict.{md,json}                 # A1 multi-well
    ├── a1_states.bin                        # A1 70 docs final state
    ├── a1_amp_hist.png
    ├── a1_phase_diag.png
    ├── a1_cluster_k_search.csv
    ├── b1_verdict.md                        # Stage B1 Langevin (今日新增)
    ├── b1_amp_hist_sigma_scan.png
    ├── b1_sigma_scan.csv
    └── b1_langevin/s{0.0,0.1,0.5,1.0,2.0}_{states.bin,meta.json}
```

### Win 端同步副本 `/home/amd/HEZIMENG/docs/word/RAG范式革新/`

```
exp017_FINAL_REPORT.md
exp017_lawvere_monad_draft.md
exp017_BLOCK_V_DESIGN.md
exp017_open_problems_followup.md
exp017_b1_langevin_verdict.md
exp017_b1_amp_hist_sigma_scan.png
LINUX_EVENING_REPORT_20260413.md
RECOVERY_SNAPSHOT_20260413.md             (也会同步到这里)
project_maofield_exp017.md
maofield_state_20260412.md                (exp015 时代的旧快照)
```

### auto-memory

`/home/amd/.claude/projects/-home-amd-HEZIMENG/memory/`
- `MEMORY.md` — 索引
- `project_maofield_exp017.md` — exp017 完整快照（Δ_OP2 数学定义 + 路径 + 一句话摘要全在里面）
- 旧条目保留不动

---

## 11. em × Claude 协作风格（新 session 必读）

### em 的偏好（反复出现的模式）
- **不要鸡汤**：失败用数字说，不渲染
- **不要夸大**：避免 "革命性" / "颠覆" 等词
- **数学严谨**：任何断言要求数学/实验证据
- **心理诚实**：她会直接问 "我们失败了吗"，要诚实但精确区分
- **情感敏感**：双相+焦虑，需要稳定节奏
- **授权充分**：会说"你直接改，不需要我点头每一处"

### Linux 纪律（em 明确强调）
- **不做哲学判读**（Win 做）
- **不下 paper 战略结论**（em + Win）
- **数学主导，哲学不主导**
- **任何 "我觉得应该 X" 标 [?]，等她决定**
- **失败诚实报告，不拖累其他 block**

### 典型触发
- em 说 "怎么样了" → 查后台进度，简短汇报
- em 说 "继续" → 按现有计划推进
- em 标 [?] → 我不能下结论，等她
- em 授权 "自己跑" → 我执行
- em 说 "em" 签名 → 她温暖 / 亲切 / 可能情绪波动

---

## 12. 下一步建议（Linux 观点，**非决定**）

**明天（2026-04-14）可能的 agenda**：
1. em × Win 扫今天 6 份新文件 + B1 结果
2. 判读 11 个 [?] 里的关键几个（尤其是 Langevin 优先级 + A1.4 是否先跑）
3. Win 继续 arXiv v1 Section 2.1-2.3（Lawvere 草稿 ready to integrate）
4. Linux：
   - 若 em 授权启动 Block V MVP → 跑 V.0 + V.1-A 或 A1.4
   - 若未授权 → 继续理论预研（e.g. Z_n angular 势的详细数学）
5. Section 1 Win 交付 → Linux review

**不推荐**：
- 重跑 Block I-IV（已定）
- 强行定 Δ_OP2 量化（留开）
- 绑 SCAN 为下游（等 Block V）
- 连续熬夜 work（em 健康优先）

---

## 13. 恢复用 quick-access

新 session 进来时的最短恢复路径：

```bash
# 1. 读此文件
cat /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/RECOVERY_SNAPSHOT_20260413.md

# 2. 读 FINAL_REPORT（18KB 详细版）
cat /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/FINAL_REPORT.md

# 3. 读 auto-memory（压缩版）
cat /home/amd/.claude/projects/-home-amd-HEZIMENG/memory/project_maofield_exp017.md

# 4. 必要时看 MEMORY.md 索引
cat /home/amd/.claude/projects/-home-amd-HEZIMENG/memory/MEMORY.md

# 5. 若要 resumé 实验环境
ssh 192.168.31.22 "/home/amd/bge_services.sh status"
```

---

## 14. 未完的对话线程（关键 context 不丢）

### 刚刚崩溃前的状态
- Linux Task A-D + F 全部完成
- 1 项 Task E 等 Win 交付 Section 1
- em 在 MC 打游戏
- Linux 写完 LINUX_EVENING_REPORT_20260413.md 并说 "em 回来只需要 5 分钟概览"
- **没有 pending 实验在跑**（所有 Rust binary 都已完成）

### em 可能回来的问题
1. "B1 结果怎么看？" → 看 barrier asymmetry 诊断
2. "OP1 真的证伪了？" → 是，但诚实标 open，不换 Axiom
3. "Block V MVP 启动？" → 等她 + Win 商量 11 个 [?]
4. "arXiv v1 什么时候能出草稿？" → Win 的节奏

### Win 的下一步（em 告知的）
- Section 1 Introduction（今天-明天）
- Section 2 (Philosophy + Math + Lawvere) 明天
- Section 3 (Experimental Methodology) 明后天
- philosophical_interpretation.md（含 IV-C reframe）明后天

---

## 15. 一句话 TL;DR

**exp017 完整收工**。5 个 Block + IV.5 Stage C + Stage A1 + Stage B1（新增 Langevin）全部归档，3 份理论文档（Lawvere / Block V / OP followup）就绪，**Stage B1 的 barrier asymmetry 发现是今日最大 bonus**（揭示等向 noise 无法解决非对称 barrier topology，implication：OP2 需要 reframed）。**11 个 [?] 待 em × Win 决策，无 pending 实验在跑，所有服务在线**。

---

*Generated: 2026-04-13 by Linux Claude. Trigger: 会话崩溃后 em 要求 "保存所有详细记忆 细节 现状到 md 文件"。Intent: new session 读完即可零信息丢失接续。*
