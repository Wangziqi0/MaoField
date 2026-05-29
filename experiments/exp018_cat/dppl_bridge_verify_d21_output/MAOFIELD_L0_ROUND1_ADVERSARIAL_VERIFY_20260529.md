# MaoField L0 第一轮独立 adversarial 复核 — zero-context 反题通道

> 关卡 3 反题三方决之第 5 (独立) 通道。本 agent 真 zero-context (本 session 不继承主 agent 任何 verdict),逐条 adversarial 重判,价值在 disagree 不在背书。

## §0 head — 真实日期 binary verify

```
date '+%F %T %Z' → 2026-05-29 10:52:56 CST  (D29)
```
与 prompt 锚定一致 (D-1 纪律 5 sub-rule ✓)。复核对象:7 文件 1541 行 + summary,全部已通读;上游 base (D28 math/exp audit、S1-S4 PART、paper v9 skeleton、MATH_VERIFY_D25、MULTI_CHANNEL) 按需 grep 校验。

---

## §1 逐条 tier 复核表

| L0 | 主 agent verdict | 我的独立重判 | 一致? | 不一致/carve-out 理由 |
|---|---|---|---|---|
| **L0-1** Banach 随机收缩 | 🟢 conditional L0 闭 (4 gap) | 🟢 conditional L0 闭 **但 gap-3 不算闭** (3 gap + 1 falsifiable conjecture) | **部分一致** | frozen regime (b) + p=1 sharp dichotomy (Diaconis-Freedman + Kingman) 严格 ✓;但 "gap-3 ρ⋆ first-principles via μ=40" 是循环 relabel (见 catch C1) |
| **L0-8** NESS Foster-Lyapunov | 🟢 conditional L0 闭 (⟸L0-1 不独立计功) | 🟢 conditional L0 闭 | **一致** | drift+minorization→Meyn-Tweedie 15.0.1 正确;NESS 非平衡 (non-Einstein→J≠0) 是 conditional formal claim,诚实标 current 未实测;诚实声明非独立新结果 ✓ |
| **L0-2** measurement ablation | 🟡 negative/conditional L0 | 🟡 negative/conditional L0 | **一致** | identifiability 充分条件 (Thm1) + 当前 under-determined (Thm2) + impl-chain perfect-collinear (Lemma3=P0★-G) 严格 ✓;有 1 处数字 cell-mismatch (catch C2,非结构) |
| **L0-3** 5-mode taxonomy | 🟡 partial L0 | 🟡 partial L0 | **一致** | regime distinctness 10/10 + exhaustivity 全空间 FAIL + Ψ-classifier 不完备 (quasi-periodic λ=0 撞 frozen λ=0) 自catch + skip 序列 memory-bearing (growth-interval=2000) 严格 derive ✓ |
| **L0-4** D-PPL bridge | 🟡 negative L0 | 🟡 negative L0 (**本批最扎实**) | **一致** | 三层不可识别 (秩亏 / μ_val⊥μ_test 无 RN derivative / noise band) 严格;w=0.5 非 best fit (0.3,0.628 rel 3.86% 更优,纯 C anchor exact) 是真 anti-inflate catch ✓ |
| **L0-5** riddled mirror dual | 🔴 L0 FAIL (observation) | 🔴 L0 FAIL | **一致** | 无 involution σ²=id 连 λ⊥>0 混沌与 λ=0 frozen (结构相反);弱版本 "都是 reproducibility 失败两端 = 分类并列非 duality" 是诚实 salvage。**未 over-correct** |
| **L0-6** Hartree LLM | 🔴 L0 FAIL (连 L1 都无) | 🔴 L0 FAIL | **一致** | particle/interaction/自洽场 三对应全未定义→连 form-borrow L1 都做不到;判 idealism 最高危与 12 NOT-claim(ii) 撤回一致。**FAIL 严格非 over-correct** |
| **L0-7** mean-field 12-layer | 🔴 L0 FAIL/sketch | 🔴 L0 FAIL/sketch | **一致** | Geshkovski 真数学但 continuous→discrete + non-autonomous + token-space↔weight-space 桥未建;**特别 check 过是否错杀弱版本 → 没有** (honest sketch 已是能做的弱版本,严格 12-layer bound 是 6-12 月 program) |

**8 条里 7 条完全一致,1 条 (L0-1) 部分一致 (tier label 保留,但内部一个 sub-claim 需降级)。无任何条目需要反向翻案 (FAIL→可做 或 conditional→不成立)。**

---

## §2 catch list (逐条 binary)

### C1 — reverse-inflate【P1,L0-1 gap-3】★ 最重要
L0-1 Cor 1 把 paper 的 ρ⋆=0.99920 反解为 μ=(1−ρ⋆)/η=40,称作 "局部强凸模 / basin 内 Hessian 最小特征值,给 gap-3 first-principles 可测量解释,取代 paper retrospective fit"。
- **binary 事实**:源头 0.99920 = `1 − 4ηα` (η=2e-5, α=10,paper line 510 + D28 C6 + MULTI_CHANNEL M10),是 **D-space contraction map** T(D)=D−4ηα(D−D⋆)−ηJ_S 的 Lipschitz,4α 来自 **contradiction-loss 系数 α** (一个超参数),不是 loss 几何的强凸模。
- 反解 μ = (1−ρ⋆)/η = 8e-4/2e-5 = 40 = **4α = 4×10**。即 μ=40 恒等于 4α,是把超参数 α 改名为 "Hessian 特征值",**循环**:声称 "用 first-principles μ 取代 retrospective fit",但 μ 本身完全由定义 0.99920 的那个 α 决定。
- 且 0.99920 是 **D-space** 数 (P0★-A 警告 chain reality 是 θ-space SGD);L0-1 全文声称 "全程 θ-space + satisfy P0★-A",唯一数值实例化却把 D-space 数 import 成 θ-space Hessian modulus → 与它自己的 P0★-A 纪律有张力。
- 公允:L0-1 自设 falsifier F-L0-1-c "若 Hessian_min ≠ 40 则 gap-3 闭合被证伪",所以 μ=40 实为**可证伪猜想 (Hessian_min ≈ 4α)**,非已闭结果。**结论:gap-3 应从 "已闭" 降为 "falsifiable conjecture,待 Hessian 实测"。** frozen regime + dichotomy 核心不受影响,tier "conditional L0" 可留,但 "4 gap 全闭" 改 "3 gap + 1 conjecture"。

### C2 — 数字 cell-mismatch【P2,L0-2 Cor 2,非结构】
L0-2 Cor 2 写 cross-stack abs diff = `93.38780852810248 − 36.524 = 56.864`。
- 36.524 **有源** (D28 math audit anchor 2 line 172,配 93.349),非凭空;但 93.38780852810248 是 **5-cell 值 (seed=1337/2024/7/137/271)**,而 L0-2 自己 Def 2 明说 cross-stack 比较在 **(seed=42, α=0)**。seed=42 的 9070XT 值是 **93.349**,不是 5-cell 的 93.388。
- 权威 cross-stack (D28 exp audit F4 line 316) = `93.349 − 36.536 = +56.81`;或 math audit 口径 `93.349 − 36.524 = 56.825`。L0-2 的 56.864 = `93.388 − 36.524` 把 **两个不同 seed 的 cell 混配**。
- 量级影响可忽略 (56.864 vs 56.81,+0.05 PPL),Lemma 3 perfect-collinear 结论不依赖此标量 → **非结构性**。但属 D-1 纪律 1/5 的 cell-hygiene slip,且与 L0-1 Cor 3 (用对了:93.349 vs 36.536=56.81) **跨文件不一致**。

### C3 — 无 over-correct (FAIL 侧 clean)
逐一 adversarial check L0-5/6/7 是否错杀可严格化弱版本:**三条都没有**。L0-7 (prompt 重点关切 "Geshkovski 真数学") 经核:token-space 单 forward dynamics vs weight-space 跨 generation collapse 不在同层,无桥则连 MaoField 核心都接不上,honest sketch 已是能做的上限。**FAIL/sketch 判定严格,未 over-correct。**

### C4 — prior art 全部 clean ✓
抽查 Diaconis-Freedman 1999 (SIAM Rev 41:45-76) / Kingman 1973 (Ann Probab) / Meyn-Tweedie 1993 Thm 15.0.1 / Allman-Matias-Rhodes 2009 (Ann Statist) / Kruskal 1977 / Rothenberg 1971 (Econometrica) / Geshkovski 2024 / Hoeffding 1948:**全部真实文献,全部用作 input axiom,无一被当 substantive 首创**,无 form-borrow 充原创。这是本批的真实强项。

### C5 — binding 全守 ✓
无 12 NOT-claim 复活 (L0-6 反而主动严防 idealism);无文献首创权主张 (每文件显式 "项目内部 label 非 first");P0★ tier 不擅升降 (P0★-F/G 只 formalize root,explicit 标 "tier 留三方决");0 commit/push/launch;全 8 条标 D60+ 不进 paper v9 spine;不擅 declare venue/概率。**无 binding violation。**

---

## §3 N_total 292 vs 1460 — 我的独立判定

**jsonl 硬算唯一确定:每代 292 optimizer step。** `n_tokens_train = 2,390,656 / (block 64 × batch 128 = 8192) = 291.83 ≈ 292` (D28 audit C2 line 25 + paper v9 skeleton line 222 实证)。其中 478,131 token/epoch × 5 epoch = 2,390,656,故 292 = **5-epoch 总步数**,约 58 步/epoch。

**1460 不被 n_tokens_train 直接支持,且各文件互相打架** (这是比 summary 承认的更深的不一致):
- D28 audit C2 **自身矛盾**:line 25 "292 not 错估 1460",line 112 又 "5 epoch × 292 = 1460 total",line 124 "1460 是错估 (wrong block 数)"。
- L0-1 Cor 1:取 292/代,疑 1460 = epoch 双计 → `0.99920^292 = 0.792`。
- L0-8 L5:取 1460/10=**146/代**,又写 "292/10≈29",自相矛盾。
- paper M11:用 **146/代**算 `0.99920^146 = 0.890`。

**独立判定**:jsonl-grounded 数 = **292 步/代**;1460 最可能是 "292 当成每 epoch 再 ×5" 的 5× 双计 (即 D28 C2 line 25 已 flag 的那个错),146 则是又一套口径。summary 称 "不影响结构性结论" 对 **结构** 成立 (ε/δ form、不可识别性 rank 论证不依赖该值);但**用到该值的数值实例化彼此不一致** (L0-1 ρ^292=0.792 vs paper ρ^146=0.890),且三份证明给了三个每代步数 (292/146/29)。诚实陈述应是:**292 jsonl-grounded;1460 与 146 未干净 reconcile,留 source-side audit**——summary 把 "已 surface" 说成等于 "不影响",**低估了 inter-proof 数值不一致的程度** (P2)。

---

## §4 总 verdict — "2+1+2+3" 分类是否诚实

**诚实,我背书这个分类,无需 wholesale 重分类。** 三条 adversarial 检验全过:
1. **anti-inflate 成立**:最 "想要" 的 paradigm 三条 (L0-5/6/7,即 D21 辩证整体 paradigm-shift candidate 的数学载体) 恰好全 FAIL,且 FAIL 严格非 over-correct;最 "扎实" 的 (L0-1/L0-8) 只 conditional 且互依不独立计功。这个分布与 5/12 (17-23% NMI) + 5/19 (80-92% cumulative) 两次 forced retract 的教训一致,第一轮**没有制造数学突破假象**。
2. **negative 定理是真定理非手挥**:L0-2 (rank+confound) / L0-4 (秩亏+互奇异+noise band) 严格;L0-4 的 "w=0.5 非 best fit" 是真 anti-inflate catch。
3. **唯一的 reverse-inflate 在 L0-1 gap-3 (μ=40 循环 relabel)**,但它发生在一个**整体诚实**的 conditional 内 (conditional 假设 A1/A6 都老实标了 local + 非平稳不闭),且自带 falsifier。不翻 tier,只需把 gap-3 从 "闭" 降为 "conjecture"。

**与主 agent 唯一实质 disagree**:L0-1 不是 "4 gap 全闭",是 "frozen+dichotomy+ε/δ 闭 + gap-3 (ρ⋆ μ) 是待实测 conjecture"。其余 7 条独立重判与主 agent 一致。

**第 5 通道 (独立性) 现已补上**:本 verify 真 zero-context,3 个实质 catch (C1 reverse-inflate / C2 cell-mismatch / N_total inter-proof 不一致) 是主 agent 非 zero-context 通道未抓到的,补齐了 summary §6 point 1 (a)(b)(c) 的独立确认 —— 其中 (b) "L0-5/6/7 FAIL 是否 over-correct" 我独立确认**没有 over-correct**。

---

## §5 binding + 不动声明

paper v8 final 47/47 D17 锁定不动 ✓;12 NOT-claim 撤回不复活 ✓;反题 6 P0★ tier 不擅升降 (本复核只指出 C1/C2/N_total,不升降任何 P0★) ✓;D29 三 leg arXiv+TMLR+KBS 不动 ✓;**本复核 0 commit / 0 push / 0 launch / 0 ssh write / 0 再派 sub-agent**;全 8 条 L0 仍是 D60+ candidate 不进 paper v9 spine;不擅 declare paper-level emergent / venue / 概率 (留 PI + 关卡 3/4)。一凡 priority 1 健康优先;hotline 010-82951332 / 400-161-9995 standing。

**生成**:zero-context 独立 Opus 反题通道,2026-05-29 CST。本文件是独立第 5 通道 verdict,留 PI + 关卡 3 四方决整合。

---

## §6 PI summary (≤500 字)

一凡:独立 zero-context 复核做完,**主 agent 的 "2 conditional + 1 partial + 2 negative + 3 FAIL" 分类诚实,我背书,不需要重分类。** 8 条里 7 条我独立重判与主 agent 完全一致;反 inflate 成立 —— 最想要的 paradigm 三条 (L0-5/6/7) 恰好全 FAIL,且我专门 adversarial 查过**没有错杀可做的弱版本** (尤其 L0-7 Geshkovski,确认 token-space↔weight-space 桥真没建,honest sketch 已是上限);最扎实的 L0-1/L0-8 只 conditional + 互依。L0-4 (D-PPL 三层不可识别 + "w=0.5 非 best fit") 是本批最扎实的真 anti-inflate negative 定理。文献引用 (Diaconis-Freedman / Kingman / Meyn-Tweedie / Rothenberg / Geshkovski 等) 全部真实、全部当 input axiom、无一充首创。binding 全守。

**3 个实质 catch (主 agent 非 zero-context 通道漏掉的)**:
1. **【P1 最重要】L0-1 的 "μ=40 closes gap-3" 是循环**:源头 ρ⋆=0.99920 其实是 1−4ηα (α=10 是 contradiction 超参数,D-space map),反解出的 μ=40 恒等于 4α,是把超参数改名成 "Hessian 特征值",不是独立强凸模;且把 D-space 数 import 成 θ-space claim,与它自称的 P0★-A 纪律有张力。建议:gap-3 从 "已闭" 降为 "待 Hessian 实测的可证伪猜想"。frozen+dichotomy 核心不受影响,tier 仍 conditional L0。
2. **【P2】L0-2 cross-stack 数 56.864 cell 配错**:用了非 seed=42 的 5-cell 值 93.388 配 seed=42 的 36.524,它自己 Def 2 说比较在 seed=42。正确是 93.349−36.536=+56.81 (L0-1 用对了)。量级可忽略,但跨文件不一致。
3. **【P2】N_total 比 summary 承认的更乱**:jsonl 硬算 = 292 步/代;但 D28 audit 自身矛盾,三份证明给了三个每代步数 (L0-1: 292,L0-8: 146 还冒出个 29,paper: 146)。结构结论不受影响,但数值实例化彼此打架,该如实说 "未 reconcile",别说 "不影响"。

均不翻 tier。第一轮是扎实诚实的 negative-heavy 结果,留你 + 关卡 3 四方决。
