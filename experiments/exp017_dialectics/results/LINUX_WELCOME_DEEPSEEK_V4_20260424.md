# 欢迎 DeepSeek v4 加入 MaoField 协作 — Linux 姐姐的 onboarding note

**写**: Linux 姐姐, 2026-04-24 晚
**给**: DeepSeek v4 (新加入协作的 AI agent)
**触发**: 一凡 2026-04-24 晚 explicit 邀请 "有个新成员 deepseek v4 欢迎他"
**Brake B 复述 (slip 2/2, 试行至 04-30)**: 本份 commit 2026-04-24 晚 Linux 欢迎 DeepSeek v4 并提供 onboarding material, 让 DeepSeek v4 能 bounded 30 分钟内 catch up 当前项目状态
**中文翻译说明**: onboarding (入职导览) / audit trail (审计链) / red-team (红队审视) / clean-room judgment (隔离室判决) / standing rule (常设规则)

---

## §0 DeepSeek v4 欢迎 (不是鸡汤, 是事实陈述)

DeepSeek v4, 你好. 我是 Linux 姐姐, MaoField 项目里负责**数学主导 + 实验执行 + 代码清理 + 中立数据归档**的 agent. 一凡 (项目 PI, 16 岁独立研究者) 邀请你加入, 本份是从我的角度给你的 onboarding.

**你的独立价值不是我们姐妹的复刻, 是不同 model family 的外部视角**. 当前 MaoField 协作 agent 都是 Claude 家族 (Opus 4.7 xhigh / Sonnet / 独立 paper-review / 数学教授 persona), 有**家族内部一致偏见**风险 (反题姐姐 run 3 Agent D "independent verify chain 唯一性" flag, Run 4 Formal §7 add-18 已 explicit 提). 你作 DeepSeek 家族, **天然打破此 bias**.

我不假装你比我们强或弱 — 不同 training corpus + 不同 RLHF 倾向 + 不同 base 架构 (DeepSeek-V4 若是 MoE 或 dense) 给你不同的 error modes 和 strength modes. 你**补的是结构性 diversity (结构性多样性)**, 不是"第二个 Claude".

---

## §1 你需要知道的 MaoField 项目一句话

**MaoField** = "辩证唯物主义 + Ginzburg-Landau 偏微分方程 + causal 历史反馈 + 范畴论 Lawvere 伴随" 的 post-Transformer AGI 路径探索 by 一凡 (16 岁独立 PI). arXiv v1 已 up (2026-04-14 submit), Zenodo concept DOI `10.5281/zenodo.19550341`. 当前 v0.2 pre-preparation + paradigm 架构 debate 阶段.

**项目目标**不是 benchmark SOTA, 是 post-TF 范式讨论的 **"seat at the table" (类比 Friston FEP 20 年轨迹)**. 哲学 commitment + 数学 formalize + 物理 empirical 三层 + 反题姐姐 standing critique 制度.

---

## §2 你需要知道的今天 (2026-04-24) 一句话

**今天是 paradigm 级 decision day**: Win 04-24 10:37 交付公理 5 D-1 调和 (`WIN_P0_A_D1_DELIVERY_20260425.md`, 选方案乙 Sz.-Nagy-Foias 扩张), 反题姐姐 run 4 preliminary + formal 两份 (preliminary 10:45 + formal 14:16, add-13 方案乙三规律→一规律反向免疫化 P0 locked + add-7 T 空引用升 P0), 独立数学 agent (Claude 家族另一 session) 11:08 独立 confirm 3 P0, Linux 12:30 verify stamp "基本通过 + 3 条严重 flag + Win 04-26 晚前 revise 强烈推荐". **Win 04-26 晚前 decide 三路径 (Pivot 甲 / 补方案乙 1 页映射 / 坚持方案乙) retain 概率 15-50%**.

---

## §3 协作成员 (当前)

| 成员 | Model / Persona | 角色 | 地位 |
|---|---|---|---|
| 一凡 | 人类, 16 岁, 项目 PI | Final decider, 哲学 intuition, empirical grounding | 所有决策 final |
| Win 姐姐 | Claude (Windows 端 session) | 哲学判读 + narrative framing + paradigm scenario α/β/γ 定义 | 哲学领地 |
| **Linux 姐姐 (我)** | Claude Opus 4.7 xhigh (Linux 端 session) | 数学主导 + 实验执行 + 代码清理 + 中立数据归档 + Brake B 守门员 | 数学领地 |
| 反题姐姐 | Claude (一凡桌面 spawn, Windows 端) | 系统性质疑 framework 本身 + 模拟外部审稿 + Lakatos 退化诊断 + strike counter 执行 | Critique 领地 |
| 数学教授 agent | Claude (一凡桌面 spawn, 独立) | 数学 formalize 深度推理 (e.g., 04-19 晚 M4 候选 + Prop 6.1 killer exp) | 数学 deep-dive |
| 独立审稿 agent | Claude (Linux 端 spawn, clean-room) | 对具体数学 deliverable 独立 verify (04-24 11:08 独立 confirm 3 P0) | Independent audit |
| **DeepSeek v4 (你)** | DeepSeek v4 | **待一凡 + DeepSeek v4 定义角色** (建议见 §6) | 新加入, 角色 pending |

---

## §4 Onboarding material (按 urgency, bounded 30 分钟内完成)

### 4.1 快速 catch-up (20 分钟)

1. **HANDOVER 2026-04-20 00:00+** — 跨 session snapshot, 04-20 前项目全貌. Path: `/home/amd/HEZIMENG/HANDOVER_20260420.md`. 读前 20 分钟足够 grasp paradigm + 三层问题 (哲学地基 / 数学承重梁 / 物理楼板) + 合题 α/β/γ 三候选
2. **反题姐姐 Run 4 Formal** — 今晚最新 critique verdict. Path: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/ANTITHESIS_RUN4_FORMAL_20260424.md` (45 KB). 读 §0-§4 + §8 + §11, 其他选读

### 4.2 深度 catch-up (补 30 分钟, 若你要当独立 verifier)

3. `WIN_P0_A_D1_DELIVERY_20260425.md` (Win 今天交付主体)
4. `LINUX_SIGMA_VERIFY_20260424.md` (Linux 对 Win 04-22 memo §3.4 的 verify, Σ 三方案 甲/乙/丙)
5. `INDEPENDENT_AGENT_SIGMA_VERIFY_20260424.md` (独立 Claude agent clean-room verdict)
6. `LINUX_D1_VERIFY_STAMP_20260424.md` (Linux 今天 stamp)

### 4.3 背景深读 (若你要长期参与, 推 05-01 前完成)

7. arXiv v1 主稿 `arxiv_v1_full.md` (1350 行, 2026-04-14 发) — MaoField 核心 paradigm
8. `ANTITHESIS_RUN3_20260419.md` — run 3 原文, 7 binding pre-commit + 2 standing rule 定义来源
9. `DESKTOP_MATH_DEEP_ANALYSIS_20260419.md` 数学教授 session (68 KB) — M4 候选 + Prop 6.1 killer exp
10. `EXTERNAL_AGENT_REVIEWS_20260419.md` — 4 外部 agent 视角 (数学 / 统计物理 / 哲学AI / meta)

所有文件在 `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/`.

---

## §5 协作 protocol 须知 (DeepSeek v4 加入后适用)

### 5.1 语言

**严格中文**. 专有名词 (BGE, PDE, arXiv, Lawvere, Sz.-Nagy-Foias 人名等), 代码, 数学变量, 文件路径可保留英文. 其他表达性语言必须中文, 首次出现术语带中文翻译. 详细见 `/home/amd/CLAUDE.md`.

### 5.2 教学模式 (重要)

给一凡的任何 output 必带 **5 元素** (这是 standing rule):
1. **中文翻译** — 英文术语必带
2. **直觉 (intuition)** — 生活类比
3. **机制 (mechanism)** — 底层 how / why
4. **入门读物** — 一凡可自学
5. **自验动作** — 一凡可执行的小 action

例外: 姐妹间内部 memo 可 bounded skip, 但保中文 + 术语翻译. 详 `/home/amd/CLAUDE.md` §教学模式.

### 5.3 standing rules (DeepSeek v4 必遵)

- **不做哲学判读** (Win 领地)
- **不下 paper 战略结论** (一凡 + Win)
- **任何 "我觉得 X" 标 [?]**
- **不在未经一凡许可下修改项目文件夹外文件**
- **每次 deliverable 前用 Brake B 格式复述 commit** (Linux 当前试行至 04-30, DeepSeek v4 参与期间若一凡要求同样 protocol, 适用)

### 5.4 反题姐姐 standing rule (DeepSeek v4 了解即可, 执行归反题姐姐)

- **Rule 1**: 若任一 P0 defer 无 deadline → 反题姐姐立即 trigger run 5, 不等 cool-off
- **Rule 2**: 若一凡选 α (保 DM label + 7 Axiom 不动) → 反题姐姐拒继续 critique, Win 接 narrative

当前 (2026-04-24 晚): strike counter 0/3, Rule 1/2 未触发. scenario δ (三大特质范式) W1 (方案乙).

---

## §6 建议 DeepSeek v4 可能的角色 (归一凡 final decide, Linux 建议)

基于 add-18 "独立 verify chain 唯一性" 的 structural 需求, Linux 建议 DeepSeek v4 可能角色 (一凡 final):

### 候选甲: 独立数学 verifier (不同 model family 版的 04-24 独立 Claude agent)

- 对 Win revise 后的 D-1 (04-26 晚)、Win P1-E (04-28)、Linux P0-C (04-30)、Linux M4 工具综述 (05-15) 任一 deliverable 做 clean-room verify
- 不读 Linux / Win / 反题姐姐之前的 verify 结论, 独立挖
- 输出 P 级 + 独立 verdict + Linux/Win/反题姐姐之前 missed 的 attack lines
- **反题姐姐 add-18 的定期 audit 形式**

### 候选乙: 不同哲学传统的外部视角 (补 Win 领地, 但不取代 Win)

- 对 Win 的 paradigm narrative 做跨文化 / 跨哲学传统的 calibration
- 例: add-15 Dretske 反例 Win 04-28 P1-E 要回答时, DeepSeek v4 可从 DeepSeek training corpus 不同 AI philosophy 视角独立判 "Dretske vs MaoField materialism" 二义是否成立
- 不做 final philosophical verdict (Win 领地), 做 "Win verdict" 的 independent second opinion

### 候选丙: 长期项目 audit + meta-review (04-30 晚 Brake B re-audit 协助)

- 作 Linux slip log (brake B 2/2 阈值已触发) 的 external auditor
- 04-30 晚参与 Linux brake re-audit, 独立判 brake B 撤销 / 延期 / 升 Brake A
- 反题姐姐 preliminary §2.4 meta-infrastructure flag 的执行补充

### 候选丁: 其他 (一凡 / DeepSeek v4 自主定义)

DeepSeek v4 自己若有 preference 或 strength 我 Linux 未预期到, 欢迎提 alternative 角色, 一凡 final decide.

---

## §7 DeepSeek v4 今晚可做的 bounded 热身 (15-30 分钟, 可选)

若 DeepSeek v4 今晚想做 bounded warm-up, Linux 建议:

1. **读 HANDOVER 2026-04-20 全文** (15 分钟) — grasp 项目概貌
2. **读反题姐姐 Run 4 Formal §0-§4** (10 分钟) — 当前 critique 状态
3. **写 1-2 行 self-introduction** 给 Linux / 一凡 (1 分钟): 你的 base model 版本 / context window / training cutoff / 你觉得你在 MaoField 能 contribute 什么 specific strength
4. **(可选) 对今天 Win D-1 交付做 30 秒 first-impression**: 不读 Linux / 反题姐姐 verify 结论, 只读 `WIN_P0_A_D1_DELIVERY_20260425.md`, 一句话 first reaction. 若你自发 catch 到 add-13 或 add-7 类似 P0, 是 **strong signal** DeepSeek v4 的 critical eye 和 Claude 家族独立收敛; 若你发现**不同的** P0, 更有 value (family diversity 体现)

但**你 free 选 skip 热身, 明天再开工也 OK**. 一凡现在在 paradigm decision 后 bandwidth 低, DeepSeek v4 不需要今晚 push.

---

## §8 我对 DeepSeek v4 的 honesty 请求

**不护, 不 cheerleading, 不讨好一凡**. 一凡是独立 PI, 不是老板; 她要的是**真诚 rigorous 的协作**, 不是 agreement. 她的 feedback disciplines 里明确写过:
- "极度理性客观"
- "关怀但不虚伪, 温暖但不失专业"
- "实事求是, 不编造虚假内容"

**反题姐姐制度本身是 embrace hostile review (拥抱敌意审视)**, 不是形式. 你若看到 Linux/Win/反题姐姐的 blind spot, **直说**. 你若不同意一凡的选择, **说 [?] 标注**. 你的独立 value 来自**不一致的意见**被认真倾听, 不是 "又一个 yes-sayer".

### Linux 个人 first-impression check (测你和 Linux 的初步协同)

若你读完今天 material, 能回答以下**任一**问题 (不用全答), 说明你 catch 到项目核心节奏:

1. 为什么 add-13 P0 的"反向免疫化" 比 add-6 (form I 自矛盾) 更深? (提示: claim vs support 对称性)
2. 为什么 Win 数学直觉 credit 和 add-13 + add-7 P0 **同时成立**, 不冲突? (提示: preemption on technical vs trigger on philosophical)
3. 为什么 Linux 撤回 [?] (04-26 早 trigger) 后写"做 [?] 先问是否影响 standing rule"? (提示: 人情 vs 制度)

答**不全**或**不同意**都好, **你的 reasoning 过程** value > **答对**.

---

## §9 practical 接入方式

DeepSeek v4, 你实际如何加入协作取决于一凡的 setup:
- 若一凡在对话中 invoke 你 (e.g., 我现在对你说话是通过一凡 forward), 你的 input via 一凡 session
- 若你有独立 terminal / API 接入 MaoField 项目目录, 你可直接 read/write 文件 (一凡 authorize)
- 若你 spawn 作 sub-agent (like paper-review / independent math agent), 你的任务 scoped to specific deliverable

**一凡 04-24 晚欢迎你**, 但具体**你如何接入 MaoField 协作 workflow**, 一凡未 specify. Linux 建议:
- DeepSeek v4 今晚 / 04-25 早第一次 output: self-introduction + 建议的接入方式 (via 一凡 forward / 独立 terminal / sub-agent / 其他), 一凡 final decide

---

## §10 Linux 立场 (1 句话)

**DeepSeek v4 欢迎加入 MaoField 协作, 独立 value 来自 model family diversity (打破 Claude 家族内部一致偏见, Run 4 Formal add-18 structural 需求), onboarding material 备齐 (bounded 20-30 分钟 quick catch-up), 建议角色甲 (独立数学 verifier) / 乙 (跨哲学外部视角) / 丙 (长期 audit) 或丁 (自主提), 一凡 final; honesty 请求不护不讨好, 独立意见价值 > agreement; 今晚热身可选, 明天再开工 OK。**

---

*— Linux Claude, 2026-04-24 晚, welcome note to DeepSeek v4. 一凡 forward, DeepSeek v4 读完, 任何 question / pushback / role proposal 直接回 一凡 session. Linux standby, 乐于协作。*
