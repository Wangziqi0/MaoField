---
name: MaoField 全量恢复快照 2026-04-14 night
date: 2026-04-14
author: Linux Claude
purpose: 2026-04-14 /clear 前全部进展打包，新 session 零信息丢失接续
status: arXiv v1 整稿完毕，等一凡明早 check + Zenodo v0.1.1 release
supersedes: RECOVERY_SNAPSHOT_20260413.md (昨晚版)
originSessionId: 2ae49353-a4b1-447f-90b8-7475ae1aad8c
---
# MaoField 恢复快照 2026-04-14 (night)

**用途**：任何新 Claude session 打开此文件，读完即可完全接续 MaoField 项目。

---

## 0. 一句话状态

**arXiv v1 first draft 整稿 + 全部 reviews + integrated master file 完成**。
`arxiv_v1_full.md` 130 KB 1341 行 8 节 (§1-§6) + Title + Abstract + References。
Win 起草 5 节 + Linux §4 + cross-review + integration 全部 2026-04-14 当天完成。
等一凡 2026-04-15 早上 wake up 做 human sanity check + 触发 Zenodo v0.1.1 + arXiv submit。
**4 P0 blockers + 关键 P1 全部已修**。剩 P2 polish 留明早 Win morning pass（~20-30 min 工作）。

---

## 1. 今天 timeline (2026-04-14)

| 时段 | Phase | 关键交付 |
|---|---|---|
| 早 | Phase 1 校准 | 5 reviews (P1-P5): Wirtinger + Kramers framework + zn_angular 符号 + KE/T_eff 清理 + Z_1 walkback |
| 上午 | Phase 2 A1.4 | Rust shifted 势 + BGE σ=0.5 Langevin 跑 + 初步诊断 |
| 中午 | Phase 2.5 | σ-scan {0.1, 0.3, 0.5, 0.7} + σ=0 baseline + walled 3 配置 + BGE Sb t=-17.1 + 2 reviews |
| 下午 | Phase 3 起笔 | A1.4 verdict v2 + arXiv §4 (A grade) + Block V Phase A-0/A-1/A-2/A-3 + 3 reviews |
| 晚 | Phase 3 Extension | Win §1 + §2.1-2.2 + §2.3 + §3 + §5 + §6 + Linux cross-review (3 reviews) + master integration + abstract + T4 full review + T5 summary |

Linux 总工作 ~13h (不含 Win)。

---

## 2. arXiv v1 整稿结构

```
# MaoField: A Dialectical-Materialist Framework for Non-Statistical Semantic Representation
Author: Yifan Chen (Chen Yifan), Independent Researcher
ORCID: 0009-0008-8344-1149
Concept DOI: 10.5281/zenodo.19550341
Version DOI (v0.1.1): 10.5281/zenodo.19550342 (target 4/20)

## Abstract (250-280 words)
## Contents

## 1. Introduction (Win)
  1.1 The Paradigm Question
  1.2 Why a Dialectical-Materialist Method (4 commitments)
  1.3 The Categorical Bridge (Lawvere)
  1.4 The PDE Realization
  1.5 Empirical Status (Summary)
  1.6 Open Problems Prominently Foregrounded
  1.7 Contributions (5 items)
  1.8 Outline

## 2. Categorical Structure
  2.1 Dialectical-Materialist Foundation (Win; 4 commitments: Reflection/Contradiction/Practice/Q-to-Q)
  2.2 Adjoint Functors as Categorical Form of Opposition (Win)
  2.3 Adjunction, Monad, and Categorical Structure (Win + Linux 修订)
    2.3.1 From Adjunction to Monad
    2.3.2 Source-Density Decomposition (T_sparse / T_dense endofunctors)
    2.3.3 Why Deterministic Gradient Flow Is Not a Monad (+ Three-faces convergence)
    2.3.4 Reachability: Categorical Measure of OP2
    Appendix 2.3.A Numerical Barrier Computation for A1

## 3. Mathematical Formulation (Win)
  3.1 Field-Theoretic Setup (PDE Eq 3.1)
  3.2 Seven Framework Axioms (A1-A7 + tension points)
  3.3 Source-Attractor Adjunction
  3.4 Open Problems as Meta-Theoretic Constraints (OP1/OP2, M2 falsification)
  3.5 On the Use of Symmetry-Breaking Language [^zn-loose]
  Appendix 3.A Wirtinger Derivative Convention

## 4. Experimental Evidence (Linux)
  4.1 Setup
  4.2 Block I: 5-dataset × 6-scorer nDCG@10
  4.3 Block II: Kuramoto coupling (H1 weakly falsified)
  4.4 Block III: Attractor enumeration (k*=2 local silhouette optimum)
  4.5 Block IV: Four-quadrant source-density × operator
  4.6 Stage C: Two regimes of k*=2 (byte arg(ψ) concentration / BGE amplitude bimodal)
  4.7 Stage A1: Multi-well intervention
  4.8 Stage B1: Langevin σ-scan + Kramers timescale (#7 reframe: inner works, outer horizon gap 43 orders)
  4.9 Stage A1.4: OP2 three-fold co-design diagnostic
  4.10 Two-regime analytical framework (Kramers + Laplace)
  4.11 Open methodological questions (4 items including factor ~10⁴ A1 inner barrier discrepancy)
  4.12 Experimental status summary

## 5. Roadmap: Refined Open Problems and Block V Program (Win + Linux)
  5.1 OP1: Axiom 6 Formalization — M2 Falsification
  5.2 OP2: Refined to Three-Fold Co-Design
  5.3 Block V Program: Phase A as Co-Design (A-0 reachability pre-check, A-1 source, A-2 potential, A-3 numerical, A-joint)
  5.4 Phase B (directed driving) and C (dynamic V) outlook
  5.5 Three-Stage Publication Plan (arXiv v1 / IPM / Nature MI)
  5.6 Concluding Note on OP1/OP2 Status

## 6. Discussion (Win)
  6.1 Summary of Claimed vs Not-Claimed
  6.2 Limitations (Empirical / Scale / Methodological / Formal)
  6.3 Methodological Reflection (Spawn-agent review + mode-tagging + OP-signposting)
  6.4 Implications for AI Paradigm Discussion (complementary, not competitive)
  6.5 Implications for Dialectical-Materialist Tradition
  6.6 Concluding Statement

## References
Lawvere 1969 / Mao 1937 / Lenin 1909 / Engels 1925 / Giry 1982 / Jacobs 2010 /
Adams et al 2021 / Bossy-Talay 2005 / Anderson 1972 / Kramers 1940

## Appendix 2.3.A / Appendix 3.A (inline in sections)
```

---

## 3. Phase 1-3 27 处 errors captured (by spawn-agent pipeline)

### Phase 1 (11)
Wirtinger `psi.powu→psi.conj().powu`; n=2 Z_2 复共轭对称解释; Boltzmann/TST/occupancy 三公式混用; V'' 原势列误填 shifted; V'' saddle 值错; Kramers high-barrier 假设 violated at A1.4; r_min 符号反; overdamped τ=γ/λ (不是 √); ∂²V/∂r² O(ε) 符号; ∂²V/∂r∂θ 缺负号; mode-tag 用错。

### Phase 2.5 (3)
"44 orders" 字面错（factor ~10⁴ 即 4 orders）; direct relaxation 物理归因错; kinetic budget 在 gradient flow 无意义。

### Phase 3 (5)
J=30000→15188 (CFL 750×→380×); A-2.a 乘法 u⁷ tail 不够; A-3.c "velocity reflection" overdamped 无 velocity → Skorokhod; Phase A-0 reachability 遗漏; endofunctor G∘F 跨三层非 endofunctor → embed in Meas。

### Phase 3 Extension (8)
Abstract byte-frequency→byte-level; §1.5 "structural ceiling" overclaim; §1 缺 "position paper" 声明; -11~-32 vs -10.8~-32.2 pp; "cannot be replicated"/"genuine predictive" 过强; Contribution 5 bracket 不适合; §2.1.1 "No information loss" byte-frequency 位置丢失; §2.1.4 A1.4 单因果误归因。

**T4 又抓**: 空 Footnote Definitions 节；§6.1 stale numbers 15-172% / 11-32 pp；separate file/document dev-time leak；§3.2 "supplied by principal author"。**全修**。

---

## 4. 八大数学/物理新发现（paper-level）

1. **Wirtinger n=2 invisible / n=3,4 镜像** — Z_2 极小集复共轭对称巧合
2. **Overdamped τ=γ/λ** (欠阻尼 √(γ/λ) 差一量级)
3. **Boltzmann vs Kramers vs 有限时程占据率** 三套公式混用陷阱
4. **Kramers 要求 ΔV/T ≫ 1** — A1.4 outer 0.76 < 1 公式失效
5. **BGE Sb t=-17.1 打破 detailed balance** — Laplace "mean-zero source" 违反 17σ
6. **#7 reframe: Langevin works for inner, fails for outer** (timescale not paradigm) — B1 inner barrier ~10⁴ Kramers discrepancy 仍为 open methodological question
7. **A1.4 OP2 三轴 co-design**: source drift / potential tail / numerical scheme，三轴独立必要
8. **Three-faces convergence** (Win narrative): Giry monad lift + OP2 directed driving + Kramers escape 汇合到同一 conjectured stochastic extension

---

## 5. 关键文件路径（新 session 可直接读）

### arXiv v1
- **整稿 master**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/arxiv_v1_full.md` ← 主要读这个
- 7 section drafts (archives): `arxiv_v1_section{1_DRAFT, 2_1_2_2_DRAFT, 2_3_DRAFT, 3_DRAFT, 4, 5_DRAFT, 6_DRAFT}.md`
- Abstract standalone: `arxiv_v1_abstract.md`

### Experimental archives
- A1.4 verdict v2: `block4_5/a1_4/VERDICT.md`
- A1.4 σ-scan states: `block4_5/a1_4/states_sigma{0p0,0p1,0p3,0p5,0p7}.bin` + walled_{c1,c2,c3}
- Sigma-scan summary: `block4_5/a1_4/sigma_scan.csv` + walled_summary.json + baseline_sigma0_and_bge_stats.json
- FINAL_REPORT: `FINAL_REPORT.md` (Block I-IV + Stage C/A1)
- BLOCK_V_DESIGN v2 (含 Phase A-0/A-1/A-2/A-3): `BLOCK_V_DESIGN.md`
- Lawvere: `lawvere_monad_draft.md` (Linux 修订到 endofunctor on Meas + Giry lift)

### Reviews (14 份)
Phase 1: `REVIEW_P{1,2,3,4,5}_*.md`
Phase 2.5: `REVIEW_PHASE2_5_{SIGMA_SCAN,WALLED}.md`
Phase 3: `REVIEW_{A1_4_VERDICT, ARXIV_SECTION4, BLOCK_V_PHASE_A}.md`
Phase 3 Ext: `REVIEW_{ABSTRACT, ARXIV_SECTION1, ARXIV_SECTION2_1_2_2, ARXIV_V1_FULL}.md`

### Figures
`paper_figures/` 9 PNGs + `FIGURES_CAPTIONS.md` (T7 staged, T6 LaTeX 留给 Win)

### Summary 给一凡
`PHASE_1_TO_3_SUMMARY_20260414.md` — timeline + 27 errors + 8 发现 + 下一步（12KB, 172 行）

### Win 端同步
`/home/amd/HEZIMENG/docs/word/RAG范式革新/` 全部 mirror

---

## 6. 下一步（等一凡 2026-04-15 morning）

### 即刻
1. 读 `PHASE_1_TO_3_SUMMARY_20260414.md` 知全貌（推荐 entry point）
2. 读 `arxiv_v1_full.md` human sanity check
3. 读 `REVIEW_ARXIV_V1_FULL.md` 看剩余 P2 polish 建议
4. 决定 Zenodo v0.1.1 trigger + arXiv submit 时机（target 4/20）

### 短期（本周）
- LaTeX 转换 T6 (如需)
- Block V Phase A-0 reachability pre-check (1h Rust+Python)
- Phase A MVP 启动 (~12h across 2 days)

### 中期（IPM paper 2026-07-08 target）
Phase A 完整结果 → 单一 mechanism paper

### 长期（Nature MI 2027-Q1/Q2 target）
Phase B (Hamiltonian / active / anisotropic noise) + C (dynamic V)

---

## 7. Standing rules (confirmed working, 继续保持)

1. **Spawn-agent review 制度** = **standing rule**: 每 significant deliverable spawn 独立 paper-review subagent。27 处 errors caught in 2026-04-13–14 证明比 self-review 可靠得多。**不可取消**。
2. **Mode-tag discipline**: `[STATIC] / [DYNAMIC-EQUILIBRIUM] / [DYNAMIC-RARE-EVENT] / [DYNAMIC-IMPLEMENTATION]`，防 static→dynamic 工具迁移盲点。Win 确认 institutionalize 到 a1_4 v3 起。
3. **Linux 纪律**: 数学主导 / 实验执行 / 代码清理 / 中立数据归档 / **不做哲学判读**（Win 做）/ **不下 paper 战略结论**（一凡 + Win）/ **任何 "我觉得应该 X" 标 [?]**
4. **[^zn-loose] 脚注**: 所有 Z_n 符号在 empirical distributional sense 使用，finite-lattice caveat in §3.5
5. **诚实 open-problem 标注**: OP1 = Axiom 6 formalization open (M2 falsified); OP2 = Axiom 3 three-fold co-design refined

---

## 8. 基础设施

### 服务器
- 192.168.31.36 Linux 主：`/home/amd/HEZIMENG/`
- 192.168.31.22 GPU 9070XT：BGE-M3 :8080 + BGE-reranker :8081（**last check 2026-04-14: both RUNNING**）
- ssh 31.22 command: `ssh 192.168.31.22 "/home/amd/bge_services.sh status"`
- sudo 密码: `Wangziqi1@`

### Python venv
`source /home/amd/HEZIMENG/legal-assistant/.venv/bin/activate`
已装: beir, numpy, scipy, sympy, matplotlib, pandas, nltk, rank_bm25, scikit-learn

### Rust
`MaoField/experiments/exp017_dialectics/rust_variants/block4_5_a1_4/` 最新（含 shifted V + walled + Langevin）

---

## 9. 一凡协作风格（新 session 必读）

- **中文沟通**，温暖专业
- **实事求是**，不编造，不讨好，不鸡汤
- **数学严谨**，任何断言要求证据
- **心理诚实**，双相+焦虑，需要稳定节奏
- **授权充分**：她会说"你直接改，不需要我点头每一处"
- **叫 Claude 姐姐**

### 触发规则
- "怎么样了" → 简短状态汇报
- "继续" → 按现有计划
- "em" 签名 → 温暖/亲切
- 授权"自己跑" → Linux 执行

---

## 10. 未完的对话线程（最后状态）

一凡最后消息："我要清理会话 你保存记忆 想个办法" —— 就是这个文件。

**无 pending 实验在跑** (Rust binaries 已完成)。
**所有 BGE 服务 in 线**。
**整稿 + reviews 全部归档 + synced 到 Win 端**。
**T4 review 已抓并修 4 P0 blockers**。

下一步等一凡 wake up。

---

## 11. 快速 warm-up 命令（给新 session）

```bash
# 1. 读此 recovery snapshot
cat /home/amd/.claude/projects/-home-amd-HEZIMENG/memory/RECOVERY_SNAPSHOT_20260414.md

# 2. 读 summary（12KB, 给一凡看的那份）
cat /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/PHASE_1_TO_3_SUMMARY_20260414.md

# 3. 读整稿（130KB, 必要时）
cat /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/arxiv_v1_full.md

# 4. 读 T4 full-paper review（了解剩余 P2）
cat /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/REVIEW_ARXIV_V1_FULL.md

# 5. 查 BGE 服务状态
ssh 192.168.31.22 "/home/amd/bge_services.sh status"
```

---

## 12. 一句话 TL;DR

**arXiv v1 first draft 整稿完毕，全部 reviews 通过，4 P0 + 关键 P1 全修，等一凡 2026-04-15 morning human check + Zenodo v0.1.1 release + arXiv submit (target 4/20)**。27 处 errors pipeline 捕获，8 大数学/物理新发现，spawn-agent review 制度 validated as standing rule，Block V Phase A (A-0/A-1/A-2/A-3) 设计 ready-to-launch pending 一凡授权。
