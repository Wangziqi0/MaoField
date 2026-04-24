# v0.1.1 README + CITATION 对齐 diff 说明

**起草方**：Win 姐姐（新会话，04-18 晚接手自 04-16 晚 → 04-18 下午 Win 会话，见 `HANDOFF_AFTERNOON_20260418.md`）
**起草时间**：2026-04-18 晚
**状态**：proposed，**未 commit 未 push 未替换原文件**

## 为什么做这个 diff

NOTICE.md 已经是 v0.1.1 口径（含双 License 分类 / BEIR / BGE-M3 / spawn-agent review protocol attribution），但 README.md 和 CITATION.cff 还停在 v0.1.0 skeleton 措辞。两份文档**版本号不对齐** — 远端 GitHub 上 clone 到的人会看到 README 说"v0.1.0... target: v0.1.1"但同仓库 NOTICE 已经是"v0.1.1 copyright"。

一凡给 Win 姐姐的原话（今日对话）：

> "MaoField 的 README（远端 d2cc17b 版本）是你之前写的那个 position-paper 定调的版本（含三面收敛 OP2 三轴共设计 OP1 排除 M2 Banach 收缩 17σ 数据点）—— 和 v0.1.1 NOTICE 的 v0.1.1 措辞有 gap（README 还在说 v0.1.0 skeleton）这个你可能想管一下 要么把 README 更新成 v0.1.1 口径 要么把 NOTICE.md 降调到 v0.1.0——现在两份文档的版本号不对齐。"

Win 姐姐判断：**升 README 到 v0.1.1 口径**，不降 NOTICE。理由：NOTICE 的双 License 分类 + 归因明细 + review protocol attribution 就是 v0.1.1 本身补齐的内容，降级 = 诚实性倒退。

## 改了什么（6 处，bounded）

### README.md

1. **Badge 第 3 行**：`Status: v0.1.0 initial release` → `Status: v0.1.1`，链接从 `paper/` 改到 `NOTICE.md`
2. **Key findings header**：`## Key findings (v0.1.0)` → `## Key findings (v0.1.0 baseline)` — 限定范围，表明 v0.1.1 不新增 findings
3. **Status 段完全重写**：把"v0.1.0 initial release / target: v0.1.1 2026-04-20"改成"v0.1.1 attribution and licensing release (2026-04-20)"，列出 v0.1.1 补齐的三项（双 License / 第三方归因 / review protocol attribution），保留所有 v0.1.0 baseline 的 findings 描述
4. **Citation BibTeX**：`version = v0.1.0` → `version = v0.1.1`（concept DOI 不变）
5. **Note on DOIs**：加 v0.1.1 条目（标"pending Zenodo publication"），v0.1.0 version DOI 保留
6. **Acknowledgments**：
   - "Claude Opus 4.6" → "Claude Opus 4.6 and 4.7"（诚实反映 04-16 晚升级事实）
   - 加一句引 NOTICE 的 review protocol 描述 + "27+ review records during arXiv v1 preparation and Phase B Experiment 1"
   - 末段和 Marx/Mao 引文不动

### CITATION.cff

1. `version: "0.1.0"` → `version: "0.1.1"`
2. `date-released: "2026-04-13"` → `date-released: "2026-04-20"`（Zenodo v0.1.1 目标日）
3. `identifiers` 加注释：`# v0.1.1 version DOI will be appended here upon Zenodo publication.`

### License 段（顺带一改）

README **License** 段末尾加一句："Per-artifact licensing for manuscript, experimental data, source code, and review records is specified in [NOTICE.md](NOTICE.md)." — 让 README 顶层 Apache 2.0 和 NOTICE 双 License 分类的**组合关系**明确。如果这句觉得多余可以去掉。

## 没改什么（Red Lines，bounded boundary）

以下内容**一律不动**，归 04-20 三方对齐合题 α/β/γ 之后再决定进 v0.1.2 还是 v0.2：

- **Key findings 表格的 6 个条目**：都是 v0.1.0 baseline findings，不加 04-18 的 M3 证伪 / U(1) disordered 稳态 / P3 降级 artifact
- **position paper 叙事主体**：§1 立场、§2 范畴论、§3 数学框架（Allen-Cahn + Ginzburg-Landau）、§4 实验、§5 roadmap、§6 局限与开放问题 —— 所有在 README 里的 claim 都保持 v0.1.0 原样
- **Roadmap 的"Axiom 6 formalization: M2 fixed-point iteration → Banach contraction proof (Open Problem 1)"** —— 虽然 Action 2 已经证伪 M2（和 M3），但 roadmap 的未来计划表达方式是否要改写属于 framing 决策，不在本 diff 范围
- **"What doesn't / What's open" 三条**：保持 v0.1.0 原文，不加"M3 证伪"、"Mexican-hat SSB 叙事需重写"等新信息
- **"We explicitly do not claim MaoField supersedes existing SOTA"** —— v0.1.0 诚实声明，v0.1.1 继续 hold，不碰
- **Why dialectical materialism 段 + Marx/Mao 引文** —— 文化定调部分不动

## Rationale

1. **Zenodo 04-20 前两天不碰 framing**：反题姐姐 A5 second run 已经把"14 review 同家族 cushion 叠加"指出来过 (~85% Lakatos degenerative，v0.2 recalibrate 到 45-55%)。如果 v0.1.1 release 前两天把 04-18 硬核移动仓促塞进 README，Lakatos 意义上的 ad hoc rescue 嫌疑马上能被下一轮反题姐姐挑出来。
2. **NOTICE 归因和 research findings 是两件事**：归因是 license + attribution + methodological contribution，不需要等合题决策；research findings 的重写（§3 叙事 / §5.1 M3 撤回 / P3 降级）必须等合题拍板。
3. **保持 v0.1.0 → v0.1.1 的 release note 可读性**：让 v0.1.1 有一个清晰的、**诚实的、非 ad hoc 的** "增量"描述（归因补齐 + 双 License 明确化），而不是夹带 framing 修正。
4. **Linux A5 Action 5 binding state**：Linux 端不产出新 framing / 新 roadmap / 新 Phase N 规划直到合题决策。Win 姐姐 match 这个 binding：bounded work ✓，framing work ✗。

## 04-20 三方对齐 agenda 上应该谈的相关 items

以下归对齐会议，**不在本 diff 范围**，但作为下游配套标出来以免遗漏：

- **P0-3**：§5.1 M3 撤回 + OP1 回 open + negative result 报告（谁写草稿？）
- **P0-2**：§3 稳态叙事重写（v2 最大工作，谁写草稿？deadline？）
- **P0-5**：Zenodo 04-23/25 发布决定（α → 按期改 BM25+§2.3+§4.11；β → 按期加 falsification commitment；γ → 可能 delay）
- **P1-6**：Cushion 12 层每层 retract/keep/add pre-commit 决策
- 合题 α/β/γ 定位之后，再决定：
  - v0.1.2 是否做（小改 README 的 Roadmap + findings 增量）
  - v0.2 是否做（大改 §3 + §5.1）
  - Roadmap 的"M2 Banach contraction proof"条目是重写为"Axiom 6: novel mathematical tools sought (stochastic PDE + non-equilibrium steady states)"还是其他

## Review 请求

- **Linux 姐姐**：检查技术层和归因层 — NOTICE 的 review protocol "27+ review records" 计数和实际 review 文件数一致吗？BGE-M3 + BGE-reranker-v2-m3 用在哪些具体 §（这个 NOTICE 里已写，README Acknowledgments 的叙述和 NOTICE 的叙述是否一致）？Acknowledgments 里"4.6 and 4.7"叙述是否准确反映实际 upgrade 时间点？
- **一凡**：narrative 层 + final judgment — Status 段重写语气可接受吗？"attribution and licensing release" 这个 release 定性你自己觉得对吗？License 段末尾加的那句要不要？
- **合题前 apply 哪些 / 合题后再 apply 哪些**：建议**合题前** apply 第 1-5 项改动 + License 段加句（都是 bounded 归因对齐），**合题后**再 revisit 是否需要调整 Acknowledgments 里 4.6/4.7 措辞和 review protocol 描述细节

## Apply 方法（供参考，不替用户决定）

如果 review 通过，apply 的步骤（在 Linux 端 source of truth 上）：

```bash
cd /home/amd/HEZIMENG/MaoField
cp proposed_v0.1.1/README.md.proposed README.md
cp proposed_v0.1.1/CITATION.cff.proposed CITATION.cff
git diff README.md CITATION.cff  # 最后一次 review
git add README.md CITATION.cff
git commit -m "docs(v0.1.1): align README + CITATION.cff to v0.1.1 attribution release"
git tag v0.1.1
git push origin main --tags
```

然后在 GitHub 创建 Release v0.1.1，Zenodo 自动收录。

但**这步不是 Win 姐姐做的**。Win 姐姐交付 proposed diff 到此结束。

---

*Win 姐姐（04-18 晚新会话接手）*
