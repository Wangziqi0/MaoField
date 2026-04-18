# 审查报告 P4 — T_eff / Kramers / gradient-flow 术语清理

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：lawvere_monad_draft.md (line 46, 52, 73) + b1_verdict.md (line 37-39) + BLOCK_V_DESIGN.md (line 32, 434)
**判定**：部分通过 + **两处必修（#4, #5）** → Linux 修订完毕

---

## 逐条结果

| # | 项 | 第一次修订判定 | 第二次修订（post-review）|
|---|---|---|---|
| 1 | gradient flow "confined to basin" 论证 | ✅ 严格 | 已补 L²-gradient flow of F[ψ] PDE 层 |
| 2 | T_eff = σ²/(2γ) 措辞 | ⚠️ γ 未定义 | 已加 "overdamped regime + γ=1 normalization" |
| 3 | V(1.69)=4.29 数值 | ✅ | 改用 `u_init ∈ [0.49,1.69] ⊂ basin-of-attraction(u=1)` 陈述（比 V 值比较更直接） |
| 4 | b1_verdict u=0 归因为 direct relaxation | ❌❌ 物理错误 | **撤回**：85% u=0 占据必然由 Langevin 噪声的 Kramers 跨越（init 整个在 u=1 basin，gradient flow 不能跨 inner saddle u_s=0.296 到达 u=0） |
| 5 | "~44 orders/×" 混淆 | ❌ 线性比 vs log-gap 两个概念混 | **分开报**：静态比 V_saddle/V_init_max = 3.07×（gradient flow），动力学 log-gap ~43 orders（Langevin Kramers @σ=0.5） |
| 6 | arXiv v1 读者负担 | ⚠️ | 分层表达：正文用 monotone descent + Kramers 一句话，数值归 Appendix |

## 关键纠正

**#4（物理错误撤回）**：
- `u_init ∈ [0.49, 1.69]`, inner saddle 在 u=0.296 **左侧**，outer saddle 在 u=2.704 **右侧**
- 整个 init range 都在 u=1 basin of attraction 里 → gradient flow 全部收敛 u=1，**不可能直接到达 u=0**
- B1 实测 85% u=0 占据 **必然**由 Langevin 噪声 Kramers 跨越 inner barrier ΔV=2.0 实现
- 前次修订误写"direct relaxation, not barrier crossing"是错的，已撤回并用正确 Kramers 论证替换

**#5（量纲修正）**：
- "V_saddle/V_init ≈ 44" 是基于旧错数 V_init=0.3 的**线性比**
- "~44 orders of magnitude" 是 Langevin Kramers 的 **log-probability gap**
- 两者 coincidence，混在一起会严重误导
- 新版分开：静态比 13.187/4.29 = **3.07×**；log-gap 45.82−2.40 = **~43 orders**（严格不是 44）

## Bottom Line

v2 修订引入了新物理错误（#4），已 intercept 并撤回。最终版本：
- gradient-flow 层：L²-monotone descent of F[ψ] + basin-of-attraction 陈述
- Langevin 层：Kramers rate × horizon 框架，overdamped + γ=1 规约
- 数值双 track：静态比 3.07× / 动力学 log-gap ~43 orders

三份文档 (lawvere / b1_verdict / BLOCK_V_DESIGN) 一致化完毕。arXiv v1 Section 5 可直接基于此措辞起草。
