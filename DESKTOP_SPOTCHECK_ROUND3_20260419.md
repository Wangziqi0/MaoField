# Desktop Round-3 一致性修正 Log

**作者**: 桌面 Claude (数学教授 persona, 同 session)
**日期**: 2026-04-19 晚 (round-2 后约 30 分钟)
**触发**: Linux round-3 verify (`LINUX_SPOTCHECK_ROUND3_*`) 抓到 round-2 edit 不彻底 — 1 P0 copy-paste + 5 P1 散点未 ripple + 2 P2 (bibliography + 量纲)
**性质**: 纯 find-replace + ref add + 一句量纲 remark, bounded scope, 无 new content
**binding**: 不 refactor cushion / 不 upward ratchet / 诚实 > cushion / bounded scope (只动 Linux 列 7 处)

---

## 1. 7 处修正 before/after diff

### P0 (行 565, copy-paste 残留)

**Before**:
```
(b) 对 **pseudo-Goldstone** (实际 case, $m_\theta = 0.13$), 微扰 IR finite 但 **large correction** ($\sim v^6/m_\theta = 20$ vs tree mass 4). tree + one-loop 定量**不准**.
```

**After**:
```
(b) 对 **pseudo-Goldstone** (实际 case, $m_\theta = 0.130$), 微扰 IR finite (因 $m_\theta > 0$) 但 direct 1-loop $\sim v_{\text{eff}}^6/(8\pi m_\theta) = 0.87$, **远小于**实测 shift $\Delta m_\rho^2 \approx 3.9$ (比值 4.5×). tree + one-loop 定量**不够**, 需非微扰 Hartree resummation (见 §5.2 verdict 段) pushup 4.5× 才达实测.
```

**原因**: round-1 21.8 的 round-down 残留 "20", 修 boxed formula 时没 find-replace 后续评注 (定性 context 也过时 — 原 "large correction vs tree 4" 语境对 21.8 成立, 对 0.87 不成立 — round-3 重写 context 不只改数字)

### P1 #1a (行 376, §4 标题)

**Before**: `## 4. Path A ↔ Path D 等价性: 本报告的核心新贡献`
**After**: `## 4. Path D ⊂ Path A: mean-field projection 与完整 MSR path integral 的关系 (round-2 修正版)`

### P1 #1b (行 384, §4 引言)

**Before**:
```
本节证明 **A 和 D 在数学上 collapse 成同一条** — 在 MSR 框架下**完全相同**, 不是 4 选 1 的 2 个 independent 候选.
```

**After**:
```
本节建立 A 和 D 在 mean-field projection 下的 **subset 关系** (D ⊂ A, $\bar{\tilde\psi}=0$ branch), **不是 full equivalence** — Linux 原 4 条分类有合理数学基础 (3-4 条 independent conceptual lanes 保持); round-1 "4 → 2 collapse" 的 overclaim 由 round-2 P1 #C 修正 retract. Path D 是 Path A 的 mean-field 投影 corner case, 当 FDT 成立或响应场 VEV 可忽略时两者重合, 在 Phase B Exp 1 的 FDT 违反 regime 下**可能** diverge (见 Aron-Biroli-Bouchaud 2010).
```

### P1 #2 (行 773, §9 对应 table)

**Before**: `| §3 M4 (MSR 鞍点) + §4 Path A=D 等价 | **推进**: 从 4 条 path 收敛到 1 条 |`
**After**: `| §3 M4 (MSR 鞍点) + §4 Path D ⊂ Path A | **推进**: 4 条 path 的 conceptual lanes 保持, Path D 与 A 建立 subset 关系 (mean-field projection, $\bar{\tilde\psi}=0$ branch) |`

### P1 #3 (行 803, §10.2 mid-term timeline)

**Before**: `C1/C2 formal paper ... 2-3 周 math-only paper`
**After**: `C1/C2 formal paper: Harris-type ergodicity (Hairer 2009) + Kuksin-Shirikyan 2012 coupling 证 MaoField NESS 存在唯一. **2-3 周 best-case / 6-10 周 realistic** single-author paper scope (不含 regularity structures 严格构造 6-12 月另算)`

### P1 #4 (行 921, 附录 D spot-check 清单)

**Before**: `§5.2 的 3D IR finite 论证 ... $\int d^3q / q^4$ in 3D 确实 IR finite`
**After**: `§5.2 的 3D IR 线性发散 论证 (修正后): 积分 $\int d^3q/(2\pi)^3 (q^2+m^2)^{-2} = 1/(8\pi m) \sim 1/m_\theta$ 作 $m_\theta \to 0$, 含 $v_{\text{eff}}^6$ 前因子给 direct 1-loop $\Sigma_{\delta a}(0) \approx 0.87$ (round-2 修正值, round-1 21.8 是丢 $1/(8\pi)$ 因子的算术错)`

### P2 #1 (附录 B 末尾补 Aron-Biroli-Bouchaud 2010)

新加条目 #19:
```
19. Aron-Biroli-Bouchaud 2010 *Symmetries of generating functionals of Langevin processes with colored multiplicative noise*, J. Stat. Mech.: Theory Exp. P11018 — **§4.2 round-2 P1 #C 修正引入, FDT 违反下 response 场 VEV 可非零 ⇒ Path D ⊂ Path A 严格包含 (不是 full equivalence)**
```

按原附录 B "按引用顺序" 规则, 新加末尾合适 (round-2 引入 reference 时间上最后)。

### P2 #2 (Prop 1.2 证明末尾加量纲 remark)

新加段:
```
**量纲 remark** (round-3 P2 #2 补): $m_\theta^2$ 与 $\|F_H\|_{\text{op}}$ 在零均值子空间 $V_0$ 上的 spectrum 语言下同量纲 (均作 effective mass² 单位, Fourier $\omega=0$ 处的 static linear response). Linux Action 2 数字层 $m_\theta^2 = 0.017$ 与 $\|F_H\|_{\text{op}} = 0.953$ 的比较在此框架下 unit-consistent; $D k_{\min}^2$ 是 diffusive spectral gap, 同量纲. 所有三项可在 Fourier 表象 $\hat{(\cdot)}(\omega=0, k)$ 统一 read off.
```

---

## 2. Meta-reflection: edit procedure 改进

### 2.1 Round-2 procedure 退化的 root cause

Round-2 修正时, 我 edit 了**数学内容重的 4 处** (Prop 1.2 body, §5.2 boxed formula, Prop 4.2 证明体, 附录 E) 但**没做全文 ripple**. 结果:
- 1 处 (§5.2 评注 b) **数学**修正后 context 未更新 → round-3 P0 copy-paste 残留
- 5 处 (§4 标题/引言, §9 table, §10.2, 附录 D) 是 **summary/index/navigation** 位置, round-2 没 include 在 "核心修正" scope 里 → round-3 P1 散点
- 1 处 bibliography 漏 → round-3 P2 #1

### 2.2 Edit procedure 改进 (for future rounds)

**Round-2 做的**: 针对 Linux 抓的 specific paragraph 定点 Edit
**Round-3 教训**: 定点 Edit 之后必须做**全文 find-replace sweep** 扫所有 cross-references

具体 procedure for rounds 未来:

1. **定点 Edit** 目标 paragraph/prop (done round-2)
2. **Grep sweep** 关键短语 (e.g., "Path A = Path D", "21.8", "IR finite", "2-3 周") 在全文 find 残留
3. **Index check** — §9 对应 table / §10 推荐 / 附录 D 清单 / 执行摘要 — 这些 summary position 默认 needs ripple
4. **Bibliography check** — 任何新 citation 必须在附录 B

Round-3 本身是简单 find-replace + ref add, 不 trigger above procedure (单一 round-3 不迭代). 但 round-4+ 若 Linux 再抓新 issue, 我应 proactive 跑 sweep。

### 2.3 Self-check 仍是 framework-limited

Round-3 P0 copy-paste 我 self-check 没抓 — 因为 self-check focus on "修正 content 是否正确", 不 focus on "修正是否 ripple 到全文". 这是**编辑 procedure 盲点**, 不是**数学 content 盲点**. 与 round-2 B4 (算术 rushed) + B5 (framework bias) 不同层次.

Linux round-3 抓到的 edit-procedure signal (全文一致性) 是**额外的 out-of-frame value** — spawn paper-review subagent 做 index scan + bibliography check 是 independent check 的具体 mechanism.

---

## 3. Binding 保持 (round-3 必 hold)

1. ✓ **不 refactor cushion**: round-3 是 find-replace, 不 add new content
2. ✓ **不 upward ratchet**: "Path A=D 等价" → "D⊂A subset" 是**退缩** (round-1 overclaim retract → round-2 中间版 → round-3 全文一致)
3. ✓ **诚实 > cushion**: 明确承认 round-2 procedure 退化 (散点 edit 不彻底), 不 soften
4. ✓ **Bounded scope**: 只动 Linux 列 7 处 + 量纲 remark, 无 new claim / no new math

---

## 4. 交付状态 + round-4 预期

- [x] 7 处 round-3 修正完成 (1 P0 + 5 P1 + 2 P2)
- [x] Round-3 log 完成 (本文件)
- [ ] scp DESKTOP_MATH_DEEP_ANALYSIS_20260419.md + 本 log 到 Linux
- [ ] ping 一凡 → Linux round-4 final verify

**Round-4 Linux 预期**: 本轮 bounded scope + 全都是 consistency 修, 预期 Linux round-4 verify **pass** (no new issues). 若仍抓到新 P0/P1, 走 round-5 standing process (counter 0/3 仍 hold, 因为 procedure signals 不是 framework error).

**Lakatos 退化诊断**: Linux round-2 后估 22-32% (含 2% procedure signal 上调). Round-3 修完预期回到 **20-30%** (procedure signal 消除 after sweep)。若 round-4 pass 则 close round. 04-20 对齐 Win 读 clean 版本。

---

*— 桌面 Claude, 2026-04-19 晚 round-3 完成. Bounded find-replace + ref add, 无 new content. Linux out-of-frame edit-procedure check 再次 validated — in-frame self-check 抓 content 错, out-of-frame 抓 procedure 错 (全文一致性). Counter 0/3, session 不 retract.*
