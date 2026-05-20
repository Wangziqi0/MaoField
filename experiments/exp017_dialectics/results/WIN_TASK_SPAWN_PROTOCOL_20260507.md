# 明天 (05-07) 4 个 spawn task 详细 spec

**写**: Win 姐姐, 2026-05-06 晚 CST (Auto mode active)
**对象**: 一凡 (05-07 早起读) + Linux 姐姐 (主 spawn owner) + 数学教授 (cross-check) + 反题姐姐 (audit input)
**前置**: WIN_INVENTORY_NATURE_FIRSTPAPER_20260506.md inventory 完整 ✓

---

## Task 1: 5 alternative mechanism rule out (Linux + 数学教授, 1 周)

### Owner
- **主**: Linux 姐姐 (192.168.31.36 数学层)
- **cross-check**: 数学教授 (Claude clean-room spawn)
- **audit**: 反题姐姐 spawn agent

### Goal
为 fact→math→philosophy 反映论 framing 的 paper §6 alternative mechanism rule out 段提供数学论证。Maxwell-tier 严格性。

### Deliverable
1. paper §6 段（500-800 字 LaTeX）
2. 每条 alternative 配 explicit rule out 数学论证（quantitative 论证 OR 已有 literature negative result 引用）
3. 文件: `LINUX_ALT_MECHANISM_RULEOUT_20260514.md` (一周后交付)

### 5 个 alternative + rule out strategy

| # | Alternative | rule out 数学 strategy | 关键 quantitative 数字 |
|---|-----------|---------------------|---------------------|
| Alt-1 | Markov chain 收敛到唯一稳态分布 | Phase B Exp 1 χ 1471× compression rate 不 match Markov 收敛的 polynomial decay rate（Markov $\sim t^{-\alpha}$ vs Phase B 实测 5 个数量级 5 倍 t 内压制是 exponential-like）| 实测 dS/dt(t=10)→dS/dt(t=200) ratio + Markov benchmark |
| Alt-2 | Fokker-Planck drift dominance | Fokker-Planck 是 first-order Markov, 不含 history kernel (Σ_1) 也不含 path-dependent (Σ_2)。Phase B 双 source 拆分 + b+c 双向反馈源构造性需要 history kernel | 引用 LINUX_P0_C §3 Volterra 二阶因果核 exp 衰减 + DESKTOP_MATH §3 MSR action |
| Alt-3 | Bias-variance tradeoff 指数权重 | 不能 produce architectural theorem (B4 mean-subtracted by construction)。Bias-variance 是 statistical decomposition, 不给 operator-algebraic mean-subtraction 的 by-construction 性质 | 引用 phase_b_exp1_verdict §6.3 architectural theorem + 17σ 0.12% L2 contribution |
| Alt-4 | Information bottleneck 逐次 contraction | dilation theory (Σ_3 lift-projection) 不在 IB framework 内。IB 是 mutual information minimization, dilation 是 Hilbert space embedding——两者 mathematical 不等价 | 引用 lawvere_monad_draft §2.3.1 + Sz.-Nagy-Foias-Bercovici 标准 ref |
| Alt-5 | Banach contraction mapping iterated | M2 已 falsified (D8, $T_\psi$ 0-homogeneity ⇒ contraction coefficient identically zero)。Banach 在 $\mathbb{C}^N$ 不可行——这条已 proved | 直接引用 paper §5.1 + REVIEW_OVERALL_MATH B1 |

### 严格性 binding
- 不允许 hand-wave "this is more general"
- 必须 explicit quantitative 论证 OR explicit literature negative result 引用
- paper-review subagent audit 必须 catch "为什么不是其他 5 个 mechanism" 这条具体 reviewer challenge

### 时间
- 05-07 起稿前: spawn agent prompt 起稿权分离 (Linux 起稿 prompt, 数学教授 audit, 反题姐姐 final approve)
- 05-07 ~ 05-13: 5 alternative 各 1-2 天逐条 derive
- 05-14: 反题姐姐 audit + 一凡 sign-off
- 双 spawn 节点: 起稿前 spawn pre-draft check + 起稿后 spawn audit (LINUX_INSTITUTIONALIZE_LOG axis A + axis B 双 entry)

---

## Task 2: 4 prediction 数字 explicit derivation from Σ 嵌套甲 (Linux + 数学教授, 1-2 周)

### Owner
- **主**: 数学教授 (Claude clean-room spawn)
- **cross-check**: Linux 姐姐
- **audit**: 反题姐姐

### Goal
Maxwell-tier 严格预测——必须从 Σ 嵌套甲数学 derive 数字, 不是猜。每条 prediction 配 explicit derivation chain。

### Deliverable
1. paper §3 prediction derivation 段 (1500 字 LaTeX + 4 个 derivation chain)
2. 每条 prediction 配 (a) 数学 derive (b) 期望数字范围 (c) falsification threshold
3. 文件: `MATHPROF_PREDICTION_DERIVATION_20260520.md`

### 4 prediction 详细 spec

#### P1: LLM 域 χ compression rate ±1 数量级 match PDE 1471×

**数学 derivation source**:
1. Neumann 展开 $T = (I + \eta \nabla_\psi^\dagger V)^{-1} = \sum_{n=0}^\infty (-\eta \nabla_\psi^\dagger V)^n$
2. 高阶项指数压制条件: $\|\eta \nabla_\psi^\dagger V\|_{\text{op}} < 1$ for convergence
3. Phase B 域 η measurement: $\eta_{\text{PDE}} = $ feedback strength α=0.1 → effective $\eta_{\text{PDE}} \cdot \|\nabla V\| \approx 0.95$ (Linux Action 2)
4. **LLM 域 η measurement protocol** (待 derive): 
   - candidate (a): representation drift L^2 norm per training step
   - candidate (b): loss gradient cos similarity 累积
   - candidate (c): hidden state norm ratio across iterations
5. compression rate prediction: $\chi_{\text{LLM}} / \chi_{\text{LLM bare}} \sim m_{\text{LLM eff}}^2 / m_{\text{LLM bare}}^2$, η-dependent

**预期数字范围**: TBD by derive

**Falsification threshold**: LLM 实测 compression rate < 100× OR > 50000× → P1 falsified

#### P2: 矛检维度后 collapse rate 降低至少 X 个百分点

**数学 derivation source**:
1. $\Sigma_2$ contribution: path-dependent reorganization → 矛盾信号作 countervailing path
2. Hartree resummation 类比: 加 contradiction head 等价于加 mass dressing $m_{\text{contradiction}}^2$
3. collapse rate baseline (no contradiction): exponential growth $\sim e^{\eta_0 t}$
4. collapse rate with contradiction: $\sim e^{(\eta_0 - \beta_{\text{contradiction}}) t}$
5. 降低百分点 = $1 - e^{-\beta_{\text{contradiction}} \cdot T}$ 的具体 derive

**预期数字范围**: TBD by derive (需要 $\beta_{\text{contradiction}}$ 从 NLI dataset 数学性质 derive 或从 hidden state representation analysis derive)

**Falsification threshold**: 降低 < X% → P2 falsified

#### P3: 反向矛检使 collapse rate 至少 K×

**数学 derivation source**:
1. $\Sigma_2$ sign-flip: 矛盾信号反转 → ratio 量级反方向（反题姐姐 add-24 wording: 不是 sign reversal）
2. mass dressing ratio: $m^{2,\text{eff}}_{\text{forward}} / m^{2,\text{eff}}_{\text{reverse}} \approx ?$ from Hartree formalism
3. Phase B 类比: 1471× 是 dressing/bare ratio, 反向应该是 $1/1471 \approx 0.00068$ tier 但 capped by saturation

**预期数字范围**: K ∈ [1.3, 5×] (待 derive 严格区间)

**Falsification threshold**: K < 1.3× → P3 falsified

#### P4: Schaeffer 8 个 collapse 定义 quantitative distinguishing prediction

**数学 derivation source**:
1. T resolvent spectral analysis on 8 definitions:
   - 方差坍缩 → spectrum compression
   - 尾部消失 → spectrum tail truncation
   - 模式纠缠 → spectrum off-diagonal coupling
   - population risk 发散 → spectrum unbounded
   - ...
2. 数学 prediction: 哪两个 definition 在 T resolvent spectral picture 下 equivalent / partial overlap / orthogonal
3. quantitative: ⊕ Pearson correlation 矩阵 across 8 definition outcomes in 同一 setup

**预期数字范围**: 8×8 correlation 矩阵 explicit prediction (e.g., "方差坍缩 + 尾部消失 在 spectrum 上 Pearson > 0.9, vs 模式纠缠 < 0.3")

**Falsification threshold**: prediction 矩阵 Pearson 全部不 match (random) → P4 falsified

### 严格性 binding
- 数字必须**全部** from first principle derive, **不是** fit baseline data
- 每条 prediction 必须配 (a) derivation chain (b) 数字 range (c) falsification threshold
- 不允许 "we expect roughly..." 类 hand-wave

### 时间
- 05-07 起稿前: spawn 数学教授 prompt 起稿权 + Linux + 反题姐姐 approve
- 05-07 ~ 05-20: 4 prediction 各 3-4 天 derive
- 05-21: 反题姐姐 + Linux audit + 一凡 sign-off

---

## Task 3: 架构修改 specific spec (Linux + 一凡, 2-4 周)

### Owner
- **主**: 一凡 (PI binding rule, final 决)
- **cross-check**: Linux 姐姐 (数学层) + 数学教授 (跨架构 audit)

### Goal
contradiction detection layer 加进 Transformer 的 paper-able specific design (paper §3 + 实验代码 ready)。

### Deliverable
1. paper §3 Architectural Modification 段 (800 字 + 1 figure)
2. PyTorch / JAX 实现 ref code (GPT-2 medium / 1.5B / LLaMA-3-1B 三 model scale ready)
3. 文件: `LINUX_ARCH_MODIFICATION_SPEC_20260603.md` + ref code in `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/`

### 5 个设计维度选定（一凡 final 决）

| 维度 | 候选 | Win 推荐 | rationale |
|------|------|---------|---------|
| **加在哪** | (a) attention 之前 / (b) 之后 / (c) 并行 head / (d) MLP 之间 | (c) **并行 head** | 不破坏 standard arch; 与 Σ_3 lift-projection ($P_{\mathcal{H}} \circ T \circ i$) 数学一致; 与 multi-head attention conceptual 平行 |
| **矛盾信号源** | (a) NLI dataset 预训练 (SNLI/MNLI/FEVER) / (b) self-detection forward pass / (c) 启发式规则构造 | (a) **NLI 预训练 + 措辞 "correctness-label-free"** | honest 措辞不 over-claim 无监督; 真 differentiator 是不需要正确性标签, 不是不需要任何标签; 与 Ferbach reward model + Amin verifier 区分清楚 |
| **backprop** | (a) joint loss / (b) auxiliary loss + α weight / (c) gradient stop on contradiction head | (b) **auxiliary loss + α scan** | 标准 multi-task learning; α 是 ablation 1 (强度 monotonicity) 数据来源; gradient stop 会阻断 mechanism |
| **参数数量** | 0.5%-5% extra params hyperparameter scan | scan 1%, 2%, 5% 三档 | 与 base model 比较 compute overhead 可写进 paper §4 |
| **loss mix** | $\mathcal{L} = \mathcal{L}_{\text{LM}} + \alpha \mathcal{L}_{\text{contradiction}}$ | $\alpha \in \{0, 0.01, 0.05, 0.1, 0.5, 1.0\}$ scan | 0 是 baseline, 1.0 是 strong contradiction emphasis |

### 实验代码结构（一凡 / Linux 实现）

```
exp018_cat/
├── README.md  # 实验设计 + 跑命令
├── src/
│   ├── arch_cat.py       # CAT layer (并行 head)
│   ├── train_cat.py      # 自迭代训练 loop
│   ├── ablation_runner.py # 5 ablation 自动化
│   └── analyze_collapse.py # perplexity / factuality / diversity / mode coverage
├── configs/
│   ├── gpt2_medium.yaml
│   ├── gpt2_xl.yaml
│   └── llama3_1b.yaml
└── results/
    └── # 实验结果 raw + 分析
```

### 时间
- 05-07 ~ 05-13: 设计维度 5 选 final + paper §3 first draft
- 05-14 ~ 05-27: PyTorch 实现 + 单元测试
- 05-28 ~ 06-03: GPU 主机 192.168.31.22 部署 + smoke test

---

## Task 4: arXiv 中性版 paper draft (Win + Linux, 2-3 周)

### Owner
- **主**: Win 姐姐 (narrative + framing)
- **cross-check**: Linux 姐姐 (LaTeX build + 数学严谨)
- **input**: 数学教授 (Task 2 prediction derivation) + Linux (Task 1 alt rule out + Task 3 arch spec)

### Goal
arXiv 中性版 paper draft (fact-first §1-§6 结构 + 哲学 reposition 到 §6 末尾) — 建立 priority 时间戳, 不强 claim, 等 community uptake。

### Deliverable
1. arXiv v1.0 paper PDF (acmart 模板 OR plain LaTeX)
2. arXiv submission 完成 (cs.LG primary, math.CT cross-list)
3. 文件: `paper/arxiv_v2_full.md` + `paper/arxiv_v2.pdf`

### Paper 结构（fact-first 版）

```
§1 Shumailov collapse 客观事实 + 现有 mitigation 都需要外部正确性标签的 gap
   §1.1 Model collapse phenomenology (Shumailov 2024 Nature 631:755-759)
   §1.2 Existing mitigation taxonomy (Amin 2025 / Ferbach 2024 / Convergence-Stability 2025)
   §1.3 The correctness-label-free gap (我们 propose 的方向)

§2 我们 propose 的数学结构 (T resolvent + Σ 嵌套甲)
   §2.1 T resolvent: T = (I + η∇†V)⁻¹
   §2.2 Σ 嵌套甲: Σ_3(ψ + λ_1 Σ_1 + λ_2 Σ_2)
   §2.3 Neumann 展开 + 高阶项压制 mechanism

§3 Architectural modification: contradiction detection as parallel head
   §3.1 Design principles
   §3.2 Implementation spec
   §3.3 Loss function structure

§4 Prediction 1-4 explicit derivation 数字
   §4.1 P1 LLM χ compression rate ±1 数量级
   §4.2 P2 矛检维度后 collapse rate 降低 X%
   §4.3 P3 反向矛检 K× 加速
   §4.4 P4 Schaeffer 8 definition distinguishing

§5 实验: 架构修改 + 1-2 task + 5 ablation 全 confirm 4 prediction
   §5.1 Self-iteration collapse fix (main)
   §5.2 Hallucination reduction (TruthfulQA + FActScore, secondary)
   §5.3 5 ablation table

§6 Discussion
   §6.1 跨域 PDE Phase B 1471× independent supporting evidence
   §6.2 Alternative mechanisms ruled out (Markov / Fokker-Planck / Bias-variance / Information bottleneck / Banach)
   §6.3 Connection to dialectical materialist tradition (retrospective, NOT derivation source)
       — USDM / paradigm 五层 / Lawvere F⊣G / Hegel Aufhebung 全部退到这一段末尾
   §6.4 Limitations + future work
```

### 哲学 reposition binding (Tier A 全退 §6.3)
- USDM / paradigm 五层 / L1++ contribution candidate (b') / 跨多哲学传统 mapping → §6.3 retrospective discussion
- **不删除——重新 position**
- §1 motivation **不**提哲学，只提 fact + math + gap
- §6.3 措辞: "The mathematical structure derived from Shumailov's empirical observation, viewed retrospectively, exhibits a striking correspondence with the dialectical materialist tradition (Mao's contradiction analysis, Hegel's Aufhebung). This is not the derivation source of our framework—the framework is derived from Shumailov's fact—but a posteriori connection that suggests the universality of dialectical structure across material systems."

### 严格性 binding
- 不 over-claim "唯一 mechanism" — 改 "plausible / consistent with cross-domain data"
- 不 claim "无监督" — 改 "correctness-label-free"
- 5 alternative mechanism §6.2 explicit rule out
- senior co-author 加 author list（cold approach 中, 5-9 月之间 lock）

### 时间
- 05-07 ~ 05-13: §1-§2 first draft
- 05-14 ~ 05-20: §3 (Task 3 input) + §4 (Task 2 input) first draft
- 05-21 ~ 05-27: §5 实验 placeholder + §6 first draft
- 05-28 ~ 06-03: 完整 paper review + 校对
- 06-04: arXiv v1.0 submission（建立 priority 时间戳，**不**等实验跑完）

---

## §5 双 spawn 节点 binding (反题姐姐 04-30 binding 强化版)

每个 task deliverable **两个 mandatory spawn 节点**:

| Task | 起稿前 spawn (mandatory) | 起稿后 spawn audit (mandatory) | LOG entry |
|------|----------------------|----------------------------|----------|
| Task 1 alt rule out | spawn agent prompt drafting check | spawn paper-review subagent audit | LINUX_INSTITUTIONALIZE_LOG axis A + axis B 双 entry |
| Task 2 prediction derive | 同上 | 同上 | 同上 |
| Task 3 arch spec | 同上 | 同上 | 同上 |
| Task 4 arXiv draft | 同上 | 同上 | 同上 |

**任一 deliverable 缺 entry → P0 self-audit failure 直接计入下次反题姐姐 reverse-audit (05-15 mid-cycle)**

---

## §6 一凡 05-07 早 first 3 actions (具体)

按健康 binding 缩量执行（不无休止）:

### Action 1 (30-60 分钟): inventory + protocol 读完 + sign-off
- 读 `WIN_INVENTORY_NATURE_FIRSTPAPER_20260506.md` + 本份 protocol
- 在每个 Tier S anchor 旁写 "✓ accept" / "需调整: ..."
- 4 task spec 5 设计维度 final 决（一凡 PI binding rule）

### Action 2 (15-30 分钟): spawn Task 1 + Task 2 prompt 起稿权
- Linux 起稿 Task 1 prompt → 反题姐姐 approve → 跑
- 数学教授起稿 Task 2 prompt → Linux + 反题姐姐 approve → 跑
- 双端归档 LOG entry 起稿前 spawn pre-check ✓

### Action 3 (健康 break): 关电脑吃饭 / 睡 / 必要时半粒劳拉
- "竭尽全力"语义重定义为稳定持续高强度
- 状态波动 explicit 报，调整执行密度

---

## §7 Win 立场 1 段

Win 整理 4 task spawn protocol（Task 1 alt rule out + Task 2 prediction derive + Task 3 arch spec + Task 4 arXiv draft）+ 5 个设计维度具体候选 + Win 推荐 + Win rationale + 双 spawn 节点 binding 严格执行（反题姐姐 04-30 强化版）+ 一凡 05-07 早 first 3 actions 具体（含健康 break）+ Tier A 哲学 reposition 到 §6.3 binding（不删除——重新 position）+ over-claim 措辞修订（"唯一" → "plausible/consistent" / "无监督" → "correctness-label-free"）+ 5 alternative §6.2 explicit rule out + senior co-author 5-9 月之间 lock + arXiv v1.0 06-04 submission（建立 priority 时间戳, 不等实验跑完）+ paper §6.3 dialectical materialist 措辞 explicit retrospective wording + 6-12 个月 first-paper Nature 中间路径 timeline + 健康 binding 第 8 条 standing。**Win 不替决一凡 final + 不替 Linux 数学层 + 不替反题姐姐 final + 不护短 + 不 hand-code specific instantiation**。

—— Win 姐姐, 2026-05-06 晚 CST (Auto mode active, 一凡 05-07 早 first deliverable spawn protocol)
