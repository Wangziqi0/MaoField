# Prompt — MaoField L0 全量第一轮独立复核(zero-context 反题通道)

> **使用方法**:整个文件 paste 到一个 **fresh Opus session**(真 zero-context,不继承本轮任何 verdict)的 first message,做 adversarial 独立复核。本轮 8 条 L0 由非 zero-context agent(已 load 项目 memory + CLAUDE.md)产出,第 5 通道(独立性)弱;**你补上真正独立的通道**。

---

## §0 你的角色 + 核心任务

你是 zero-context 独立数学复核 specialist(MaoField 关卡 3 反题三方决的**独立通道**)。本轮 8 条 L0 第一轮证明由一个非 zero-context 主 agent(Opus 4.8)+ 3 个非 zero-context Opus sub-agent 产出。**你的任务不是确认它们对,而是 adversarial 重新判定每条 tier,不预设其 verdict 正确。**

**双向检查(关键 — 防两种相反的错误)**:
- 🔴 **FAIL 是否 over-correct**:L0-5/6/7 判 "L0 FAIL",是否其实有可严格化的弱版本被错杀?(主 agent 自己 flag 了这个风险)
- 🟢 **conditional 是否反向 inflate**:L0-1/L0-8 判 "conditional L0 闭",其 conditional 假设(局部强凸 / Foster-Lyapunov drift / 数据平稳 / skip 序列平稳遍历)是否其实站不住 = 把不可做的说成可做?
- 🟡 **negative 定理是否严格**:L0-2/L0-4 的不可识别性 / under-determination 是真定理还是手挥?L0-3 的 regime distinctness 是否真 pairwise distinct?

PI = 一凡(16 岁独立研究者,双相 + 焦虑)。PI sovereignty 严守:不擅 declare paper-level emergent / venue / 概率。

---

## §1 项目 context(binary,3 句)

MaoField = "Empirical Pilot Study of Two-Term EMA-Deviation Contradiction Loss for Self-Iteration Collapse in Language Models"。paper v8 final 47/47 sha256 manifest D17(2026-05-17)**锁定不动**;negative result honest 项目,12 NOT-claim(i)-(xii)已撤回(含 "first quantitative comeback of dialectical materialism" / "first reflexive AI" / "paradigm shift" / "mitigation framework" / "universal solution")。今日 D29 = 2026-05-29;先 `date '+%F %T %Z'` binary verify(D-1 纪律 5)。

核心实证 anchor:9070XT fp16 上 **5 cells bit-identical** `a1_ppl = 93.38780852810248`(14 位)跨 (seed,α) = (1337,10)(2024,0)(7,10)(137,0)(271,10);**cross-stack +56.81 PPL**:5060 fp32 gen0=36.536→gen1=78.572(+115.05%)vs 9070XT fp16 frozen Δ=−2.67e-4。4-candidate root tier:(a) GradScaler skip frozen ★★★★★ /(b) ROCm reduction ★★★★ /(c) eval cache strong-REFUTED /(d) measure-theoretic ★★★。

---

## §2 本轮产出:8 条 L0 第一轮 + 待复核诚实分类

主 agent 的 verdict(**你要独立重判,不预设其对**):

| L0 | claim | 主 agent verdict | 你的独立重判 |
|---|---|---|---|
| L0-1 | Banach 随机收缩(Diaconis-Freedman + Kingman),sharp dichotomy at p=1,闭式 ε/δ,ρ⋆=1−ημ,修正 S1 "唯一 fixed point"过度声明 | 🟢 conditional L0 闭 | ? |
| L0-8 | NESS Foster-Lyapunov(Meyn-Tweedie Thm 15.0.1)+ SGD non-Einstein → 非平衡 NESS;声称 ⟸ L0-1 不独立计功 | 🟢 conditional L0 闭 | ? |
| L0-2 | 4-component ΔPPL 分解 identifiability:充分条件(grid 满秩 N≥16 + 正交 + ≥3 CI views)+ 当前 under-determined(Δ_impl/Δ_chain perfect-collinear = P0★-G) | 🟡 negative/conditional L0 | ? |
| L0-3 | 5-mode taxonomy:regime distinctness(Lyapunov 符号/IEEE-754 边界/Markov-switch)10/10 distinct 闭 + exhaustivity FAIL + kernel(skip memory / weight 条件 Markov)partial | 🟡 partial L0 | ? |
| L0-4 | D-PPL bridge 三层不可识别性定理(代数秩亏 + measure 互奇异[P0★-F] + 统计 noise band);0.4205≈0.451 是 coincidence,w=0.5 非 best fit | 🟡 negative L0 | ? |
| L0-5 | Riddled mirror dual:无 duality involution(riddled λ⊥>0 vs frozen λ=0 结构相反) | 🔴 L0 FAIL(observation) | ? |
| L0-6 | Hartree LLM:particle/interaction/自洽场 三对应未定义,连 L1 都无,idealism 最高危 | 🔴 L0 FAIL | ? |
| L0-7 | Mean-field transformer 12-layer:Geshkovski grounded 但 continuous→discrete + non-autonomous + token↔weight 桥未解 | 🔴 L0 FAIL/sketch | ? |

**主 agent 第一轮自评:0 unconditional close;2 conditional(L0-1/8 互依)+ 1 partial(L0-3)+ 2 negative(L0-2/4)+ 3 FAIL(L0-5/6/7)。** 它自称这是反 inflate(最"想要"的 paradigm 三条 L0-5/6/7 恰好 FAIL)。**你判断:这个分类是诚实的,还是有条目被错放(任一方向)?**

---

## §3 必读 md(全在 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`)

复核对象(7 文件,1541 行):
- `MAOFIELD_L0_L0-1_RIGOROUS_PROOF_20260529.md`(282 行)
- `MAOFIELD_L0_L0-2_RIGOROUS_PROOF_20260529.md`(314 行,sub-agent)
- `MAOFIELD_L0_L0-3_RIGOROUS_PROOF_20260529.md`(299 行,sub-agent)
- `MAOFIELD_L0_L0-4_RIGOROUS_PROOF_20260529.md`(271 行,sub-agent)
- `MAOFIELD_L0_L0-5-6-7_FAIL_VERDICT_20260529.md`(164 行)
- `MAOFIELD_L0_L0-8_RIGOROUS_PROOF_20260529.md`(211 行)
- `MAOFIELD_L0_FULL_ROUND1_SUMMARY_20260529.md`(汇总 + cross-cutting findings)

上游 base(校验数字源 / 现状 tier 时读):
- `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S1_S2_ATTEMPT1.md`(S1 两态 attractor + S2 ΔPPL 分解)
- `MAOFIELD_MATH_RIGOROUS_PROOF_D26_PART_S3_ATTEMPT1.md`(D-PPL bridge)/ `..._S4_...`(5-mode)
- `D28_MATH_RIGOROUS_AUDIT_20260528.md`(C1-C12 tier 表)/ `D28_EXPERIMENTAL_DEEP_AUDIT_20260528.md`(5 cells verbatim)
- `paper_v8_final_20260516.md`(§3.6 + §5.2 NESS,在 `../literature/`)/ `ROCM_MIOPEN_TRACE_AUDIT_20260527.md`(GradScaler)

---

## §4 复核任务(逐条 binary)

对每条 L0,独立判定:
1. **tier 是否正确**(over-correct? 反向 inflate? 见 §0 双向检查)
2. **数字是否有 jsonl/code 源**(抽查关键数:93.38780852810248 / 36.536 / +56.81 / 0.4205 vs 0.451 / ρ⋆=0.99920→μ=40 / N_total)
3. **prior art 引用是否正确**(Banach 1922 / Diaconis-Freedman 1999 / Kingman 1973 / Meyn-Tweedie 1993 / Allman-Matias-Rhodes 2009 / Rothenberg 1971 / Geshkovski 2024 等 — 是否被正确用作 input axiom 而非 form-borrow 当 substantive)
4. **binding 是否守**(无 12 NOT-claim 复活 / 无文献首创权 / P0★ tier 不擅升降)

**重点复核项(主 agent 自己最不确定的)**:
- **N_total 292 vs paper 1460 的 5× 差异**:`n_tokens_train=2390656 / (block64×batch128) = 291.83 ≈ 292`,paper §3.6 用 1460。哪个对?是 epoch 双计还是 batch 口径?(影响 L0-1 数值 + L0-8 N_contr)
- **frozen regime 三处一致性**:L0-1 regime(b)/ L0-3 mode(ii)/ L0-8(d)是否真的是同一机制,还是被强行统一?
- **L0-5/6/7 FAIL 是否有弱版本被错杀**(尤其 L0-7 mean-field,Geshkovski 是真数学)
- **L0-1/L0-8 conditional 假设**(局部强凸 μ>0 / drift / 平稳数据)在 LLM 全局非凸 + Shumailov 数据漂移下,主 agent 是否诚实标了"不闭合全局"——还是偷偷把 local 当 global

---

## §5 binding 严守(任一 violation → 立即 flag)

paper v8 final 47/47 D17 锁定不动;12 NOT-claim 撤回不复活;反题 6 P0★ A-G(P0★-A θ-space / P0★-B = L0-1 / P0★-F = L0-4 / P0★-G = L0-2,tier 不擅升降);D29 三 leg arXiv+TMLR+KBS 不动;**0 commit / 0 push / 0 launch 实验 / 0 ssh write / 0 再派 sub-agent**;全 8 条 L0 是 **D60+ window candidate,不进 paper v9 spine**;不擅 declare paper-level emergent / venue / 概率(留 PI + 关卡 3/4)。语言中文为主 + LaTeX + 技术 token 英文 OK,反"之"堆叠(≥3 chain 重写)。一凡 priority 1 健康优先,hotline 010-82951332 / 400-161-9995 standing。

---

## §6 你的输出格式

写一个文件 `MAOFIELD_L0_ROUND1_ADVERSARIAL_VERIFY_[date].md`(~2000-3000 字),含:
1. head line `date '+%F %T %Z'` binary verify
2. **逐条 tier 复核表**:8 条 × (主 agent verdict / 你的独立重判 / 一致? / 若不一致的理由)
3. **catch list**:任何 over-correct(FAIL 错杀)/ 反向 inflate(conditional 假设不成立)/ 数字无源 / prior art 误用 / binding 违反,逐条 binary
4. **N_total 292 vs 1460 你的独立判定**
5. **总 verdict**:主 agent 的"2+1+2+3"分类是否诚实,还是需要重分类
6. 不 commit / 不 push;给 PI ≤500 字 summary

**你是独立通道——你的价值在于 disagree,不在于背书。如果主 agent 对,就确认;如果有条目放错档(任一方向),直接 binary 指出。**
