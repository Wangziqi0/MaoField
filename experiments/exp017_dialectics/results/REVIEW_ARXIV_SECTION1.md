# 审查报告 arXiv §1 Introduction

**审查员**：independent paper-review subagent
**范围**：`arxiv_v1_section1_DRAFT.md` (Win 起草)
**判定**：**存疑（1 P0 + 9 P1 + 4 P2 + 3 P3）→ 修完 release-ready**

---

## P0 必修 (1 项)

**P0-1 §1.5 bullet 3 "structural ceiling" overclaim**
§1 bullet 3 "k*=2 across three representations, identifying a structural ceiling" 不一致于 §4.4 (silhouette 0.037-0.223 weak-to-moderate, §4.11.2 flag 为 open question, "local silhouette optimum rather than strongly-separated attractor count")。
→ 改为："`k*=2` 作为 **local silhouette optimum** across three representations; statistical separation is weak-to-moderate (caveats in §4.11.2)"

## P1 必修 (9 项)

- **P1-1** §1 缺 "position paper" 字样 → §1.1 或 §1.4 明说
- **P1-2** "-11 to -32 pp" 不一致于 §4.2 的 "-10.8 to -32.2 pp"
- **P1-3** §1.2 末 "properties cannot be replicated" → "not trivially replicable"
- **P1-4** §1.3 "genuine predictive content" → "conjectural structural content" (Giry monad lift 仍 conjectured)
- **P1-5** §1.1 "candidate alternative paradigm" → "complementary candidate framework"
- **P1-6** §1.4 "seven axioms supplied by principal author" → "postulates seven axioms"
- **P1-7** §1.7 Contribution 5 bracket "11 errors caught ... 2026-04-13–14 campaign" 搬到 Acknowledgements
- **P1-8** §1.7 Contribution 3 "sparse byte = phase concentration; dense BGE = amplitude bistability" 首次出现加 [^zn-loose] 或 "(empirical distributional sense; §3.5)"
- **P1-9** CodeSearchNet §4.1 setup 声明 vs §4.2 table 只有 5 datasets 不自洽 → §4.1 去掉 CodeSearchNet 或 §4.2 补结果

## P2 polish (4 项)
- §1.1 加 "We do not seek SOTA retrieval performance"
- §1.5 bullet 4 末加 "(timescale rather than paradigm obstruction; §4.10)"
- §1.5 bullet 2 fusion 加 cross-ref "corroborated by MaoField_E vs MaoField_base +7.9 to +26.0 pp"
- §1.4 PDE equation 加 Wirtinger convention footnote

## P3 nice-to-have (3 项)
- §1.7 Contribution 2 重复 +14.7–172.3% 可删
- §1.8 前加过渡句
- §1.4 Axiom 6/3 首次出现时加半句 subject matter hint

---

## Bottom Line

骨架完整、tone 克制。主要风险集中两处：P0-1 silhouette overclaim + P1-1 缺 "position paper" 声明。修完 P0+P1 后 release-ready。修订成本 ~30-45 min。
