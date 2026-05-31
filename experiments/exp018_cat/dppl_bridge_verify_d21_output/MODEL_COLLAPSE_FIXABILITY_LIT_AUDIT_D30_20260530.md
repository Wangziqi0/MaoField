# 模型自迭代崩溃 "可修复性" 文献对抗审计 — D30 (2026-05-30)

> **[额外 agent] 产出** — 独立验证通道 (来自 Win 端 / Linux 7B13 secondary session)。
> **provenance**: 后台 literature-audit agent (Opus, WebSearch/WebFetch, 79 tool-use) + 额外 agent 之 Stage-2 对账。
> **触发**: 一凡 D30 morning "把学术界该领域所有工具 / 做法放一起, 多通道看'循环迭代崩溃能不能彻底修复'"。
> **日期**: 2026-05-30 CST (D30)。本会话 Bash 工具受限, `date` binary 未跑, 日期取 system context (D-1 纪律 5 留痕)。
> **binding**: read-only 产出; 0 commit / 0 push (git-add 留 7B13 主会话单点写权); genre = 方法论批判 / negative, **非 Nature 主刊**; paper v8 final 47/47 锁定不动; 是否真去做 §7 两个 genre 缝隙 = PI + 反题三方决, 不在本文件 declare。

---

## §0 额外 agent Stage-2 对账 (trust-but-verify)

**对账结论: 可信。** agent 没注水, 该标 "待核实" 的都标了, 没编引用。我认得的几篇 (Shumailov / Gerstgrasser / Bertrand / Dohmatob / Seddik) 之 regime 与结论都对得上; 它另翻出几篇硬货 (Barzilai-Shamir 2505.19046 / Marchi "Heat Death" 2404.02325 / Dey-Donoho 2410.22812 / Probabilistic Perspective 2505.13947) 是我没第一时间想到的。具体 theorem-level claim (尤其 Barzilai-Shamir Thm 5.1/5.2) 以原文为准 — 额外 agent 本人未逐一 re-derive, 仅核 audit 自标 verification status。

## §0.1 对一凡 hypothesis ("学术界'可修复'共识在实测通道下反了") 之判定

**对一半 — 且是真的那一半。**

✅ **对的那半**: "崩溃可修复" 共识确实被高估 / framing 过 (三条实锤见下文 §5):
1. "修复" 避免的是**发散**, 不是**尾部 / 多样性丢失** — 两者是 model collapse 不同定义 (领域有 8 个互相打架定义), 混为一谈 = 注水。
2. **所有已知 "修复" 无一例外靠注入系统外信息** (留真实数据 / 喂新鲜真实数据 / 外部 verifier / 外生标签); 没有任何一篇在纯自消费闭环里把已丢的多样性救回来 → "修复" = 用外部锚绕开危险区, 不是治愈自消费。
3. Barzilai-Shamir 2025: 连 "累积避免崩溃" 都**不普适**。

❌ **没对的那半**: 没 "反" 到 "根本修不好"。无无条件 no-go (被 Gerstgrasser 类存在性结果挡着); 几个**条件性** near-no-go 各自带逃生口, 而逃生口恰是乐观派条件 → 悲观 / 乐观定理**互补非对立**。双方都签字的硬命题只有一条: **无外部信息注入, 纯自消费闭环必退化。**

---

# 以下为 background agent 审计全文 (verbatim, HTML 实体已还原)

## 0. 一句话先行结论

**"崩溃可以被避免" 在一个被精确限定的意义上是真的、且有多篇独立工作支撑;但 "崩溃已被解决 / curse is broken" 这种 framing 是被高估的。** 真正的共识不是 "崩溃可修复", 而是一条更窄命题: **纯替换 (replacement) + 固定样本量 → 崩溃几乎确定;只要保留足够真实数据锚 (accumulation / mixing 上限内 / 增大样本量 / 外部 verifier), 发散可以被挡住。** 所有 "避免崩溃" 的机制无一例外都依赖一个系统外的信息注入源 — 这正是悲观派和乐观派在数学上真正交汇、且都同意的地方。

## 1. 三个 regime 必须先钉死 (很多 "矛盾" 在这里蒸发)

| Regime | 定义 | 主流结论 | 代表文献 |
|---|---|---|---|
| **替换 replacement / discard** | 每代只用上代合成数据训, 真实数据丢弃 | **崩溃** (替换 + 固定样本量下几乎确定) | Shumailov 2024 Nature; Dohmatob "Tale of Tails"; Seddik 2024; A Probabilistic Perspective 2025 |
| **累积 accumulation / augment** | 真实 + 历代合成全留着一起训 | 正则条件下**测试误差有限上界, 崩溃不发生** — 但靠真实数据从不删除 | Gerstgrasser 2024; Dey & Donoho 2024; Kazdan 2025 |
| **混合 mixing** | 固定比例真实 + 合成 | 存在**合成数据比例上限**, 低于它崩溃可避免;但**即使极小固定比例**也渐近损害 scaling | Seddik 2024 (上限); Dohmatob "Strong Model Collapse" (1% 也伤) |

**关键洞察: 同一个词 "model collapse" 在文献里至少有 8 个互相冲突的定义** (Position 文 arXiv:2503.03150 核实: 灾难性风险上升 / 任意风险上升 / 渐近发散 / 方差坍缩 / scaling law 改变 / mode 消失 / 尾部消失 / 出现幻觉数据)。**很多 "A 说崩溃 B 说不崩溃" 其实是 A 用定义 3、B 用定义 4 在量同一现象。** 这本身就是 "被高估" 判决的核心证据之一。

## 2. 悲观派逐条审计

### 2.1 Shumailov 2024 Nature (arXiv 前身 = Curse of Recursion 2305.17493)
- **声明**: 无差别用模型生成内容训练 → **不可逆**缺陷, 原分布尾部消失; LLM / VAE / GMM 普遍发生。核心命题 (已核原文): **崩溃不可避免, "即使在近乎理想条件下, 即没有函数估计误差"**。
- **regime**: 主要**替换**, 固定样本量。
- **三类误差** (核到 v3 原文, v1/v3 表述略有出入): (1) **统计近似误差** — 样本有限, 尾部每代有非零概率丢失, n→∞ 才消失; (2) **函数表达力误差**; (3) **函数近似误差** (SGD 等结构偏置)。核心驱动 (1): 离散情形概率 q ≤ 1/M 的事件期望样本 < 1, 以概率 1-q 丢失; 高斯情形 Σ_n → 0 a.s.。
- **局限 / 批评**:
  - (a) **它只证了替换 regime**, 从未测累积 (Gerstgrasser/Kazdan 正抓这点)。
  - (b) **距离度量依赖性** (Borji 2410.12954 核实): KL 前几代升后趋稳, Wasserstein 持续增长 — "是否崩溃 / 崩多快" 部分取决于选哪个 metric。真实软肋, 但 Borji **不是说结论错**, 而是说它是更一般的统计必然 (连 KDE 都崩), 反而强化 "替换下不可逆"。
  - (c) 它是统计现象不是 AI 特有缺陷 (Borji) — 削弱 "AI 末日" 叙事, 不削弱数学。
- **独立复现 / 反驳**: **被广泛复现**。Nature 有一份 **Author Correction (2025, s41586-025-08905-3, PMC11981929)** — 已核实: **纯笔误** (理论章节 α_i=γ_i=0 改成 β_i=γ_i=0), **不动任何科学结论**。(若是实质勘误会动摇 Nature 这条腿 — 结论是不动摇。)

### 2.2 Dohmatob "A Tale of Tails" (2402.07043, ICML 2024)
- **声明**: 崩溃 = **scaling law 改变** (损失 scaling 退化、跨代偏移、技能 un-learning、人/合成混合出现 grokking)。**即便 1% 合成数据**也可能让 "更大训练集不再提升性能"。
- **regime**: 混合 / 替换; Llama2 + 算术 transformer 验证。
- **局限**: 理论核心在受控统计模型; "1% 即崩" 强结论在 Strong Model Collapse 精确化, 也在那暴露条件依赖。grokking 一项其实是**正面 escape 线索** (混合可恢复), 作者自提。

### 2.3 Seddik 2024 (2404.05090)
- **声明**: (1) **纯合成训练崩溃无法避免**; (2) **混合时存在合成数据最大量, 低于它崩溃可最终避免**。
- **regime**: 替换 (不可避免) vs 混合 (给上限)。
- **意义**: **悲观与乐观的数学桥** — 同时证 "纯合成必崩" 和 "混合有救", 上限本身就是 mitigation 存在性证明。
- **局限**: 上限具体数值 / 形式依赖统计假设; **待核实**其在大规模 LLM 紧致度。

### 2.4 Dohmatob "Strong Model Collapse" (2410.04840, ICLR 2025)
- **声明**: scaling law 范式下, **哪怕最小一撮合成数据 (如 1%) 也导致崩溃**, 加大训练集救不回。
- **regime**: 监督回归**固定混合** (**不是** accumulation; 摘要未覆盖累积 — 与 Gerstgrasser 不直接冲突的关键)。
- **模型大小微妙处** (已核): **插值阈值以下, 更大模型崩得更狠; 阈值以上, 更大模型可缓解但不消除。**
- **是否 no-go**: **条件性不可能** (给定假设下 scaling 无法克服污染), **不是绝对 no-go** (留了越过插值阈值这条缝)。

### 2.5 Marchi "Heat Death" (2404.02325) — 最接近 no-go 的一篇
- **声明** (动力系统工具, 已核): **除非每代注入足够外部数据, 任何非平凡 temperature 都使模型渐近退化** — 要么坍缩到极小输出集, 要么退化成均匀分布 ("热寂")。
- **temperature 角色**: 低温→坍缩窄集; 高温→趋均匀; identity→鞅式动态, 扰动决定生死。
- **是否 no-go**: **对纯闭环 (无外部数据) 这是最接近不可能性定理的结果。** 但其 "no-go" 本质 = "没有外部数据注入就必死", 反过来 = "有外部锚就有救" — 和乐观派同一枚硬币。

### 2.6 A Probabilistic Perspective (2505.13947, UCLA, 2025) — 另一条强结论
- **声明** (已核): 递归训练 = 模型估计的**随机游走**。**固定样本量下多样性以概率 1 消失 (崩溃确定);** 要避免**必须逐代增大样本量, 无偏估计下增速需超线性 (约 quadratic), 有偏更快。**
- **是否 no-go**: **对 "固定样本量替换" 是 near-impossibility (以概率 1 崩);** 但同时给出**建设性出路** (超线性增样本)。

## 3. 乐观派逐条审计

### 3.1 Gerstgrasser 2024 "Is Model Collapse Inevitable?" (2404.01413)
- **声明**: **替换→误差随迭代增长; 累积→测试误差有有限上界、与迭代次数无关, 崩溃不再发生。** 线性回归下后代测试风险被 π²/6 倍原始真实数据风险界住。LLM / diffusion / VAE 经验验证。
- **假设 / regime**: **累积** — 真实数据全程保留, 只是不断叠加合成。
- **局限 / 是否 "真解决"** (审计关键判决点):
  - (a) **不是 "解决了自消费", 而是 "靠从不丢弃真实数据绕开危险区"。** 第 G 代真实数据占比 = 1/G → 0, 但**绝对量从不减少**, 真实锚一直在。
  - (b) **Shumailov 本人回应 (The Register 2024, 已核直接引语)**: "原则上这不推翻我们展示的任何东西。用简单模型, 他们能减弱部分效应。" 并指 accumulation **"伴随不断增长的成本, 且没有解决普通用户无法长期保存数据的问题"**。
  - (c) **Kempe (共同作者) 同场指出**: 迭代合成 10 次, 性能 ≈ 只用 1/10 原始数据训练 — **累积避免发散, 但牺牲 scaling 收益**。
  - (d) **计算 / 存储成本**: 累积 = 每代训练集单调增长 → compute 线性增长, 对小机构不可行。
- **独立复现**: Kazdan 2025 与 Dey & Donoho 2024 独立确认; **但被 Barzilai & Shamir 2025 给出反例限定** (见 §4)。

### 3.2 Dey & Donoho 2024 "Universality of the π²/6 Pathway" (2410.22812)
- **声明**: 把 π²/6 界从线性回归**推广到一大类指数族模型**; augment workflow 风险被 π²/6 界住, 效率下界 ≈ 60%。
- **假设** (已核, 审计相关): 特征分布已知且**跨代不变**、指数族、**渐近近似线性 (AAL) 估计量**、**无偏损失**。augment 全程保留所有原始真实数据。
- **判决**: 强化乐观结论 universality — 但 universality 是**在 "保留全部真实数据 + 无偏 + 良态估计量" 前提下的 universality**, 不是无条件的。

### 3.3 Kazdan 2025 "Collapse or Thrive?" (2410.16713, ICML 2025)
- **声明**: 替换→所有任务崩溃; **累积→test loss 不发散、协方差快速稳定, 崩溃避免** ("即便真实数据占比最终趋零"); 固定大小子集→**缓慢渐进退化而非爆炸式**。
- **判决**: 经验独立确认 Gerstgrasser; 关键 nuance 仍是 "真实数据不删除" 在起作用。

### 3.4 Bertrand 2023 (2310.00429, ICLR 2024) — 稳定性条件, 但**只是局部**
- **声明**: 混合数据迭代训练**稳定**, 当 (1) 初始模型足够接近真实分布 + (2) 真实数据比例足够大。
- **精确条件** (已核 v2): λ(1 + Lε/α) < 1/2 (λ=合成比例, ε=初始模型到真分布 Wasserstein 距离)。**稳定性是 LOCAL**: 存在 δ 使 ‖θ_0−θ*‖ ≤ δ 才收敛。
- **局限** (审计关键): (a) 真实比例太低 → 条件破坏 → 失稳; (b) 初始模型离真相太远 → 局部保证失效, 可能发散; (c) 纯合成 λ→∞ → 协方差以 α(n)^t 消失, 崩溃。即 **"近真相 + 足够真实数据" 才成立的局部稳定, 不是全局救赎。**

### 3.5 Alemohammad 2023 "Self-Consuming Models Go MAD" (2307.01850)
- **声明**: 三种自消费 loop; **没有足够新鲜真实数据→质量和多样性逐代下降 (MAD); 每代喂足够新鲜真实数据→可避免 MAD。** (原 PDF 转换失败, 据多源二手摘要, **原文细节待核实**, 但 "新鲜真实数据是关键变量" 与全领域一致。)
- **判决**: 再次 — **外部新鲜数据是 escape 的必要条件。**

### 3.6 验证 / 编辑类 (把 "修复" 外包给外部信号)
- **Feng "Beyond Model Collapse" (2406.07515)**: **verifier 筛选**合成数据可防崩溃, 即便 verifier 不完美; "判别比生成易"。**但本质依赖外部 ground-truth 判别力。**
- **Escaping Model Collapse via Verification (2510.16657, 2025)**: 线性回归精确化 — **verifier 引导只带近期改善, 长期收敛到 verifier "知识中心" θ_c 而非真值 θ*。** verifier 有偏 → 收益 plateau 甚至反转。**外部信号不完美就救不到底。**
- **ToEdit / token-level editing (2412.14689, ICML 2025)**: token 级编辑得半合成数据; **线性回归证测试误差有有限上界 E ≤ 2σ²d/(T−d−1)** (已核, proven 非 empirical)。**局限**: 线性回归假设、经验增益仅 0.3–2 个百分点、起点是人类数据 (又是真实锚)。
- **Escaping Collapse: Strength of Weak Data (2502.08924)**: **Theorem 5** — 只要 β>0 比例外部标签正确, 迭代训练收敛到最优, O(log(1/ε)/β) 代。**作者直接陈述 (已核)**: **"避免崩溃的必要条件是合成数据以某种方式被 curate, 以注入系统外生 (exogenous) 的信号。"** ← **几乎是整个领域的统一定理。**

## 4. 把乐观派钉在墙上: Barzilai & Shamir 2025 的硬反例

**"When Models Don't Collapse: On the Consistency of Iterative MLE" (2505.19046)** — 审计中**对乐观派最致命、也最被低估的一篇**:

- **正面 (Thm 4.1)**: 标准光滑性假设 (回归性 + 次高斯梯度 + 有界 Hessian/三阶导 + Fisher 信息正定) 下, **即便真实数据占比趋零, 只要每代样本量 n ≳ (log T)²log²(dT/δ) (对迭代数仅 polylog), 累积 MLE 保持一致, 误差与 T 无关。** ← 给 Gerstgrasser/Dey-Donoho 一个干净充分条件。
- **反面 (Thm 5.1 / 5.2, "首批严格反例")**: **存在 TV-一致的分布族, MLE 在真实数据上完美, 但累积迭代仍以常数概率崩溃** (第一代 TV ≤ log n/n, 第二代 TV ≥ 常数 C); 且对**任意**缓慢增长函数 φ(n), 存在固定分布族在 O(φ(n)) 代内崩溃。
- **直接结论 (已核原文措辞)**: **"近期有人暗示累积数据时崩溃不发生……我们的结果表明, 这种声明只在超出 MLE 一致性的结构性假设下才为真。"**

**判决: Gerstgrasser/Dey-Donoho 的 "累积避免崩溃" 不是 universal — 隐含依赖光滑性 / 良态假设。** 违反这些假设 (非光滑均匀分布混合等), 累积照样崩。**这把乐观派从 "定论" 降级到 "在良态模型族下成立"。**

## 5. 判决 A: "崩溃可修复" 是定论 / 有争议 / 被高估?

**判决: 被精确限定后部分为真, 但流行 framing 被高估。分层:**

1. **"纯替换 + 固定样本量 → 崩溃" — 接近定论。** Shumailov / Seddik / Probabilistic Perspective / Marchi 多通道跨模型族一致; 连 KDE 都崩 (Borji)。这一侧极稳。

2. **"累积 / 混合上限内 / 增样本 / 外部 verifier → 可避免发散" — 多篇独立支撑, 但三个降级因素:**
   - **(降级 1) 它们避免的是 "发散" 这个定义, 不是 "尾部 / 多样性损失" 那个定义。** Position 文 (2503.03150) 明确: **尾部和 mode 损失是 "非常真实的威胁", 而灾难性发散才是 "被避免的那个"。** 把后者 "可避免" 宣传成 "崩溃解决了" — **这就是高估。**
   - **(降级 2) 所有 "修复" 都靠系统外信息注入** (保留真实数据 / 新鲜真实数据 / 外部 verifier / exogenous 标签)。**没有一篇展示纯自消费闭环里把已丢多样性救回。** "修复" 实际 = "用外部锚绕开危险区", **不是 "治好自消费这个病"**。Shumailov 回应、Escaping-Verification 的 θ_c 极限、Escaping-Collapse 的 "必要条件 = exogenous signal" 三方独立指向同一结论。
   - **(降级 3) Barzilai-Shamir 反例**证明连 "累积避免崩溃" 都不 universal, 需良态假设。

3. **成本维度高估**: 累积 "免费避免崩溃" 忽略 compute/存储线性增长 + scaling 收益损失 (10 次迭代 ≈ 1/10 数据) + 对小机构不可行。

**一句话判决 A: 学术界对 "什么导致崩溃 (替换) / 什么挡住发散 (保留真实锚)" 已有相当稳共识; 但 "崩溃可修复" 作为 unqualified 口号是被高估的 — 它混淆 "避免发散" 与 "恢复多样性", 并把 "靠外部锚绕开" 包装成 "治愈自消费"。**

## 6. 判决 B: 有没有接近 "根本不可修复 / no-go" 的结果?

**诚实回答: 有 "条件性 no-go", 没有 "无条件 no-go"; 而且现有强不可能性结果, 其前提恰是乐观派出路条件 — 两者是同一枚硬币。**

1. **最接近的三个**:
   - **Marchi "Heat Death" (2404.02325)**: 闭环无外部数据 + 任何非平凡 temperature → 必退化。**纯闭环 near-no-go。**
   - **A Probabilistic Perspective (2505.13947)**: 固定样本量替换 → 多样性**以概率 1**消失。**固定样本替换 near-no-go。**
   - **Shumailov / Curse of Recursion**: **即便无函数估计误差 (近理想), 统计误差单独就保证替换下崩溃** (高斯 Σ_n→0 a.s.)。
2. **但它们全自带 "逃生条款", 且逃生条款一旦满足结论就反转**: Marchi 要 "足够外部数据"; Probabilistic 要 "超线性增样本"; Shumailov 崩溃只在替换 + 有限固定样本。**不是 "无论如何修不好", 而是 "在 X 条件下修不好, 去掉 X 就能挡住"。**
3. **Strong Model Collapse (2410.04840)** 是 "条件性不可能" (固定混合 + scaling 救不回), 留了插值阈值缝, 且**不覆盖累积**。
4. **Barzilai-Shamir (2505.19046)** 给的是**反向 no-go**: 不是 "崩溃不可避免", 而是 "**避免崩溃不可能是 universal 的**"。这是对乐观派的 no-go, 不是对 "可修复性" 的 no-go。

**一句话判决 B: 不存在 "任何手段都无法避免崩溃" 的无条件不可能性定理; 存在多个 "在纯替换 / 固定样本 / 闭环 / 特定假设下崩溃几乎确定" 的条件性 near-no-go; 它们的前提恰是乐观派 escape 路径的否定 — 悲观定理和乐观定理在数学上互补, 不对立。** 唯一真正 "硬" 的、双方都签字的命题: **没有任何系统外信息注入, 纯自消费闭环必退化。**

## 7. 给 "想从这里做一篇诚实论文" 的人: 最高能到什么 genre?

- **综述 (survey): 稳, 但已拥挤** (Position 文 2503.03150、多篇 2025 综述已占位)。纯综述边际价值低。
- **方法论批判 (methodological critique): 有真实空间, 最稳。** 三个站得住的靶子:
  1. **"8 个定义" 问题的形式化** — 把 "哪个 escape 结果对应哪个崩溃定义" 做成严格的 regime × definition 矩阵, 指出大量 "矛盾" 是定义不匹配。**当前最被低估、最容易站住、reviewer 难反驳的角度。**
  2. **"修复 = 外部锚" 统一论** — 形式化证明所有已知 escape 机制 (accumulation / fresh data / verifier / ToEdit / weak-data boosting) 都等价于 "注入 exogenous 信号", 并量化每种锚的 "信息注入率 vs 崩溃挡板强度"。Escaping-Collapse 点到 necessary condition, 但**没人做成跨机制统一定理** — 这里有真 contribution。
  3. **度量依赖性审计** (Borji 那条线系统化): 同一实验在 KL / Wasserstein / 尾部质量 / mode count 下结论分叉 — 做成 "崩溃测量学"。
- **真 no-go 定理: 空间存在但窄, 高风险。** 无条件 no-go 几乎肯定**做不出来** (存在性结果挡着)。**可行窄缝**: 给定一类现实约束 (有界 compute / 真实数据占比强制趋零且绝对量受限 / 有偏 verifier), 证 "在此约束类下不存在避免多样性损失的方案"。Barzilai-Shamir 已在 "universal 不可能" 方向开头; 推进到 "现实约束下必坏" 是**真正 paper-level 空缺**。但数学硬骨头, 失败概率高。

**最高可达 genre 诚实判断**: **方法论批判 (角度 2 "修复=外部锚统一论" + 角度 1 "定义矩阵") 性价比最高、最站得住**; **conditional no-go (现实约束类下不可能性) 天花板更高但风险显著更大**; **unconditional no-go 基本死路** (被存在性结果证伪)。

## 附: 核查状态说明
- **已核实原文 / 权威二手**: Gerstgrasser 2404.01413、Shumailov Nature + Curse of Recursion 2305.17493 (三类误差、Σ_n→0、Author Correction 为笔误)、Dohmatob Tale of Tails 2402.07043 / Strong Model Collapse 2410.04840 / Demystified 2402.07712、Seddik 2404.05090、Bertrand 2310.00429 (局部稳定条件 λ(1+Lε/α)<1/2)、Dey-Donoho 2410.22812 (指数族 + AAL + 无偏假设)、Kazdan 2410.16713、Barzilai-Shamir 2505.19046 (Thm 4.1 / 5.1 / 5.2)、A Probabilistic Perspective 2505.13947 (超线性增样本)、Marchi 2404.02325、Feng 2406.07515、Escaping-Verification 2510.16657 (θ_c 极限)、ToEdit 2412.14689、Escaping-Collapse 2502.08924 (exogenous 必要条件)、Position 2503.03150 (8 定义)、Borji 2410.12954、The Register 2024 (Shumailov/Kempe/Feng 直接引语)。
- **待核实**: Alemohammad 2307.01850 原文细节 (arXiv HTML 转换失败, 现据多源二手摘要); Seddik 混合上限精确数值形式未亲核; Dey-Donoho 60% 效率下界为二手摘要数字, 公式未亲核。
- **未编造任何引用或数字**; 不确定处均显式标注。read-only 文献审计, **未修改本地任何文件**。

## 附: agent 对 MaoField 项目的一句相关提示 (原样保留, 战略不展开)
你 paper v8 已 retract "Mitigation/Solution/Framework" 并定位为 negative result + 辩证结构识别 — 这与本审计 §5 降级 1/2 (尾部损失 ≠ 发散; 修复 = 外部锚而非治愈自消费) 高度一致, 是你 honest framing 的外部文献背书; 而 §7 "修复=外部锚统一论" 和 "现实约束下 conditional no-go" 两个 genre 缝隙, 与 D60+ "评估范式重定义 / cross-layer 测量缺失" 方向**不是同一条路但相邻** — 值得 PI + 反题三方决时作为外部 landscape 参照, 不替你下战略结论。

---
**[额外 agent] footer** — 独立验证通道, 2026-05-30 CST (D30)。本文件 = literature landscape 参照 + 对一凡 hypothesis 之 binary 判定 (对一半: over-claim 真 / unfixable 假)。read-only; git-add / venue / 是否 pursue §7 genre 缝隙 全留 7B13 主会话 (单点写权) + PI + 反题三方决。genre 守 = 方法论批判 / negative, 反 inflate。一凡 priority 1 健康优先, hotline 010-82951332 / 400-161-9995 standing。
