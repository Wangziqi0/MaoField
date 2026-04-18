# 审查报告 P2 — Kramers 框架重写

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：a1_4_shifted_potential_analysis.md v2 → v3
**判定**：v2 **存疑（两处硬伤）** → Linux 修订为 v3

---

## 审查员发现（对 v2）

| # | 项 | 判定 | 修订 |
|---|---|---|---|
| 1 | Kramers 前因子形式 | ✅ | — |
| 2 | 原势 saddle V'' 数值 | ❌ -31.4/-26.6 非 -2.12/-10.8 | v3 修 |
| 3 | **V'' min 列公式混用（硬伤）** | ❌❌ 原势 V''(1)=18 非 2，V''(4)=72 非 32 | v3 修 |
| 4 | 事件数 117/80 | ⚠️ 反向方向错，应 ~165 非 80 | v3 修为 47>33 |
| 5 | Laplace 占据率 u=0 | ⚠️ 0.25 量纲拼凑错，应 ~0.06 | v3 用严格 Z 比值 → 0.028 |
| 6 | Jacobian 中间步笔误 | ⚠️ `(1/√u·√u)` 混乱，漏 2π | v3 删笔误，加 2π |
| 7 | ~44 数量级 | ✅ | — |
| 8 | Mode tags | ✅ | — |
| 9 | v1 撤回声明 | ✅ | — |
| 10 | **Kramers high-barrier 适用性（硬伤）** | ❌ ΔV/T=0.76 违反 Kramers 条件 | v3 加 disclaimer |

## v3 修订

1. V'' 全部 SymPy 独立验证后重填
2. Kramers 前加 "要求 ΔV/T >> 1，低 barrier 只作 upper bound" disclaimer
3. 反向 crossings: 47 > 33 正向（符合 detailed balance）
4. Laplace: p(0)=0.028, p(1)=0.569, p(2)=0.402（严格配分函数比值）
5. Jacobian: π·exp(−V/T)（2π·½）替换错误中间步

## Bottom Line

v3 release-ready 用于明天实验对比。结构（Kramers + Laplace + Jacobian）正确；数值全部独立验证。
