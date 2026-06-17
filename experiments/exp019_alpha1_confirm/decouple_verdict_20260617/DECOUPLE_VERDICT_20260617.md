# exp019 解耦线 [A−] — 落盘复算 verdict (D617)

> 2026-06-17 (date 二值验证)。Linux 姐姐主会话 + 第二通道子 agent 独立复核 (D-1 纪律 4)。
> 处理 6/13 audit-exp019-decouple 三问题 (LINUX_AUDIT_AMENDMENT_20260615 §3)。
> **本文件 = 首个落盘可复现判定 + 差异日志 (纪律 5)。** 数据/脚本同目录。

## 0 一句话裁定
**解耦线 [A−] 作为「独立 novel 安全垫」不成立 (死)。** 忠实复算 (rep_penalty=3.0,
匹配链生成口径) **0/5 链满足预注册解耦判据** (原报 4/5 / 审计 5/5 **均不可复现**)。
真实图景:① 总多样性塌缩**真实** (D1 3/5, D3 5/5) 但**被 Guo 2023 / Shumailov 占**;
② 解耦命门 D2 (恢复期续降) **全 fail 0/5** — diversity 在 PPL 恢复期 plateau/部分回弹,
与 PPL **部分耦合非解耦**;③ 信号方向**对 rep_penalty 敏感** (rep=1.0 looping 伪影 →
假性上升)。**exp019 至此无任何存活 positive**。

## 1 忠实复算结果 (rep_penalty=3.0, CPU fp32, N=128, 5-way beam, metrics.compute_distinct_n)
脚本 `scripts/analysis_decouple_n5.py`;结果 `decouple_n5_result.json`。

| seed | d2(g0) | d2(g2) | d2(g9) | Δd2(g9−g0) | Δd2(g9−g2) | Δrep4(g9−g0) | D1 | D2 | D3 | decoupled |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.505 | 0.380 | 0.361 | **−0.144** | −0.019 | +0.323 | ✓ | ✗ | ✓ | **F** |
| 2 | 0.517 | 0.349 | 0.365 | **−0.152** | +0.017 | +0.326 | ✓ | ✗ | ✓ | **F** |
| 3 | 0.507 | 0.396 | 0.428 | −0.078 | +0.033 | +0.245 | ✗ | ✗ | ✓ | **F** |
| 4 | 0.499 | 0.369 | 0.390 | **−0.109** | +0.021 | +0.285 | ✓ | ✗ | ✓ | **F** |
| 42 | 0.522 | 0.401 | 0.423 | −0.099 | +0.022 | +0.262 | ✗ | ✗ | ✓ | **F** |

判据 (prereg §6.2): **D1** Δd2(g9−g0)≤−0.10 / **D2** Δd2(g9−g2)≤−0.05 / **D3** Δrep4(g9−g0)≥+0.05;单链解耦=D1∧D2∧D3。
- **D1 过 3/5** (seed3/42 擦边未达 −0.10);**D2 过 0/5** (全部 ≥−0.02,即恢复期不续降反 plateau/回升);**D3 过 5/5**。
- **n_decoupled = 0/5**,grade [B,seed-dep]。

## 2 解耦命门 D2 失败的机制 (diversity 与 PPL 是部分耦合非解耦)
PPL 轨迹 (test_perplexity on 真实 wikitext, 落盘 chain logs, 5/5 一致驼峰):
g0≈36 → **g2≈106 (峰)** → g9≈56 (回落 plateau)。
- **g0→g2**: PPL 升到峰, diversity 大降 (0.50→~0.38) — 塌缩集中在此段。
- **g2→g9**: PPL **大幅回落** (~106→~56, −50), diversity **不续降, plateau/部分回升** (+0.02~+0.03)。
→ 真实形态 = 「塌缩主要在前段 (与 PPL 升峰同期), 恢复期 diversity 部分跟 PPL 回弹」。
**这是「diversity 与 PPL 部分耦合」, 不是 prereg 设想的「diversity 持续降而 PPL 恢复」解耦。**
D2 算子 (要求恢复期续降 ≤−0.05) 设想方向错: 实际 plateau-at-collapsed + 部分回弹。

## 3 方法论发现: distinct-n 塌缩方向对 rep_penalty 敏感 (decode-confound)
同一批 ckpt, 三 decode 口径 distinct-2 g0→g9 方向 (seed1 示例, diag_text):

| decode | d2(g0) | d2(g9) | 方向 | 忠实? |
|---|---|---|---|---|
| beam **rep=1.0** | 0.303 | 0.442 | **升 +0.14** | ✗ (链用 3.0;looping 伪影) |
| beam **rep=3.0** | 0.505 | 0.361 | **降 −0.14** | ✓ (cat_arm_b.yaml 配置值) |
| sampling (T=1.0) | 0.747 | 0.616 | 降 −0.13 | (非链 decode, 但同向降) |

- **rep=1.0** (无惩罚): beam 陷入循环 (实测文本: g0/g9 均重复短语), distinct-n 测的是循环特征非真多样性 → **假性上升**。
- **rep=3.0** (链实际口径) / sampling: 循环被压, 真塌缩显现 → 降。
- **教训**: 原 ad-hoc s42 −0.201 + 4/5 判定无落盘脚本 (问题#2), 其方向高度依赖未明示的 decode 口径; 一旦用错默认 rep_penalty=1.0, 结论翻转。**这是「报告数 ≠ 可复现数」的根因。**

## 4 三问题处理结论 (对 LINUX_AUDIT_AMENDMENT_20260615 §3)
1. **seed4「0.001 擦线 / 4/5」**: 忠实复算 **0/5** (含 seed4 D2 fail)。原「4/5」(verdict) 与「5/5」(audit) **均不可复现**。s42 自身忠实 −0.099 ≠ prereg −0.201 (高估 ~2×, 且 D1 擦边未达)。**settled: 报告数不可复现, 真值 0/5。**
2. **开奖判定无落盘 trace (D-1.1 违反)**: **已闭合** — 本轮建首个落盘可复现脚本 `analysis_decouple_n5.py` + 结果 JSON + 本 verdict + 第二通道独立复核。
3. **核心被 Guo 2023 占**: 确认 **(b) 部分成立** (文献子 agent, 见 §5)。diversity 单调降 + distinct-2 + 过拟合窄分布 = Guo (NAACL 2024) 占满; PPL 驼峰对照 Guo 未占 (Guo PPL 单调降), 但残余 = PPL 驼峰本身, 已被 recovery-geometry (D615) 精确化为瞬态。novelty 作 novel finding ≈ 0。

## 5 Guo / Shumailov 占用 (文献子 agent 裁定)
Guo et al. 2023 = arXiv 2311.09807 = "The Curious Decline of Linguistic Diversity" (NAACL 2024 Findings)。
占: ① diversity 单调降 ② distinct-2 指标 ③「过拟合窄分布」机制。未占: PPL 驼峰对照 (Guo PPL 单调降)。
但本复算显示 MaoField 自身忠实数据下「diversity 持续降 vs PPL 恢复」的解耦也**不成立** (D2 0/5) → 残余 novelty 进一步坍缩。
"塌缩不可逆" (g2→g9 diversity 不回到 g0) = Shumailov 2024 已有性质。

## 6 差异日志 (D-1 纪律 5, 主动浮现不静默)
1. **主会话自身 rep=1.0 误判 → 修正**: 本轮首次复算用 generate_synthetic 默认 rep_penalty=1.0 (未覆盖), 得 distinct-2 **上升 +0.20**, 一度形成「解耦 diversity 半边被证伪/塌缩不可复现」临时结论, 并**错误归因 fp16 非确定性**。第二通道子 agent catch: (a) 两 shumailov run 非同配置 (audit pre-fix rep=1.0 vs audit-fix rep=3.0, 溯源 GROUND_TRUTH_INVENTORY_20260512 L24-25), rep_penalty 才是方向主因, **非 fp16 噪声**; (b) 0/5 当时只立在自标 UNFAITHFUL 的 rep=1.0 数据上。修正: 重跑忠实 rep=3.0 → 塌缩**真实** (我 rep=1.0 的「升」是伪影)。**复跑是唯一仲裁, 差点凭 prior + 不忠实数据翻烧饼 (接 memory feedback_measure_dont_flipflop_priors)**。保留 `decouple_n5_result_rep1.0_UNFAITHFUL.json` 作对照证据。
2. **原 prereg s42 先验不可复现**: s42 −0.201 (prereg) vs 忠实 −0.099 (本复算)。无落盘出处 (问题#2), 高估 ~2×。
3. **两 shumailov_no_preserve_seed42 run distinct_3 方向相反** (g1→g9: run A +0.219 / run B −0.305), 但**非同配置** (rep_penalty 1.0 vs 3.0), 不可作「fp16 非确定」铁证, 收紧为「rep_penalty 决定方向」。

## 7 净裁定 + 留 PI
- **解耦线 [A−] 作 novel 安全垫: 死。** 严格 0/5 + 定性部分耦合 + 被 Guo/Shumailov 占 + 测量 rep_penalty 敏感。
- **exp019 全景**: α=1 confirmatory 三 endpoint 全 FALSE (C1/C2/C3 撤回) + 恢复相几何 = PPL 驼峰瞬态 (descriptive 精确化) + **解耦线 [A−] 死** → **无任何存活 positive**。
- **净产出 = 干净 negative + 两个方法论标本** (① confirmatory 拦截自家假说 ② distinct-n 的 decode/rep_penalty 敏感性 + ad-hoc 数不可复现)。
- 留 PI: ① 解耦线既死, 是否仍以「干净 negative + 方法论」入 paper/note; ② 「distinct-n 测量敏感性」方法论标本是否值得单独记 (接 Guo 复现 caveat)。

---
*红线不动: C1/C2/C3 撤回不复活 · C3=frozen · v8 47/47 锁定 · 12 NOT-claim 不复活 · fractal 死刑。*
*复算: 36 CPU, 总 elapsed 2665s (忠实 rep=3.0) + 3474s (rep=1.0 对照)。第二通道: 子 agent A/B/C/D 四通道独立复核支持本裁定。*
