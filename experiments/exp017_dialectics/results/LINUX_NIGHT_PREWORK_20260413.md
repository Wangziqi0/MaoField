# Linux Night Pre-work 2026-04-13 (evening)

**背景**：一凡今天情感密度大，晚上去睡。Win 已完成 arXiv v1 Section 1。Linux 无实验在跑，BGE 服务健康（:8080 + :8081 RUNNING）。按一凡 + Win 一致建议做"不消耗一凡决策"的方向 2 + 3 预研。

## 交付（两份数学文档 + 两张图）

| 文件 | 大小 | 内容 |
|---|---:|---|
| `block4_5/a1_4_shifted_potential_analysis.md` | 4.4 KB | A1.4 数值预估 |
| `block4_5/a1_4_shifted_barrier.png` | 88 KB | 原势 vs shifted 势对比图 |
| `zn_angular_potential_math.md` | 7.9 KB | Z_n angular 完整数学 |
| `block4_5/zn_angular_slices.png` | 111 KB | Z_2/Z_3/Z_4 角向势剖面 |

Win 端同步到 `docs/word/RAG范式革新/` 前缀 `exp017_` 4 份。

## 关键数字（2 行 TL;DR）

**A1.4 shifted**（u∈{0,1,2} 代替 {0,1,4}）：outer barrier **13.19 → 0.095**（降 139×，σ=0.5 Langevin 动能预算 0.125 以内），预测 σ=0.5 下 u=2 占据率 ~30%（对比 B1 原势 0%）。inner/outer 非对称 **反转** 到 4.54×（现 inner > outer）。

**Z_n angular**（Mexican hat + ε·Re(C·ψⁿ)）：n 个等间距极小 `θ_k = ((2k+1)π−φ_C)/n`，相邻势垒 `ΔV = 2ε|C|vⁿ`，Hessian 对角 `(λ_r, λ_θ) = (8v², n²ε|C|vⁿ)`，切向软比率 ~1/(n√ε)，**k*=n 直接预测**。ε→0 恢复 U(1) flat ring（PH Betti₁=1 检测）；ε→∞ 非物理。

## 对 11 个 [?] 的 *数学-only* 输入（不下结论）

- **[?] 9 (A1.4 是否先跑)**：A1.4 预计 σ=0.5 下 u=2 ~30%、u=1 ~65%、u=0 ~5%。若实测偏离，说明 Boltzmann 平衡假设失效（有 kinetic trap）。Rust 改动仅一行势函数常数，<1h 验证成本极低。
- **[?] 10 (OP2 措辞 "add noise" → "restructure barrier topology")**：若 A1.4 实测激发 u=2，保守措辞"barrier geometry must be designed compatible with available driving"更稳（是工程问题）；若实测仍失败才必须 OP2 激进 reframe（是范式问题）。建议 A1.4 结果出来再定稿 OP2 措辞。
- **[?] 8 (Langevin 优先级)**：A1.4 预研本身不决定这个。若 A1.4 成功，V.3-L sub-block 保留为"Langevin on barrier-compatible potential"，不降级；若 A1.4 失败才确认降级。
- **[?] 1 (Z_n / U(1) / non-Abelian 哲学优先级)**：纯哲学，不碰。数学上 n=3 是首个"非平凡离散破缺"，n=2 和 baseline GL 拓扑等价。
- **[?] 7 (Δ_OP2 量化)**：Z_n 势在 ε→0 极限的 PH Betti₁=1 → 离散 n 时 Betti₁=0, Betti₀=n，是 PH 对 `|T-Alg_T^{(η,p₀)}|` 结构变化的 direct indicator，支持 PH 作为 Δ_OP2 canonical 候选。

## Linux 纪律守住

- 未启动 Rust 实验
- 未改 BLOCK_V_DESIGN.md 或 OP followup 或 arXiv 相关文件
- 未对 Axiom 6 或 OP1/OP2 做新措辞提案（只做数学）
- 所有推断加 [?] 标注

## 明天见

一凡睡醒时此文件 + 两份数学 + 两张图在 `exp017_dialectics/results/` 下，Win 端也已同步。无 pending 实验在跑，无服务需要重启。
