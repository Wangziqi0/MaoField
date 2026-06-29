# Order-Defect 预印本终门审计

## 最终分类

```text
short_note_requires_minor_wording_or_bibliography_fixes
```

这不是数学核失败，也不是 related-work 主体失败。相反，**文献地板已经达到外发最低要求，Lamboni 2026 已被纳入，projection-theory 边界也已写出**；当前卡住短札草稿门的，主要是**harness 边界语句还没有在指定工件中用同一条规范句统一落地**，尤其是 `README.md` 里还没有把该句真正写进去，只是在说明“下一轮要检查它”。因此，我不能把它判成 `short_note_draft_gate_passed_after_copyediting`；更准确的结论是：**还差一轮很小但必须做的 wording cleanup**。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/README.md:221-225`；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:73-79,122-126,154-169`；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:12-14,100-109`；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:13-15,209-211`；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py:4-8,448-455`；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:17-31,33-49,53-65`。）

## 审核总判断

数学边界并未被削弱。`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 仍然明写：对象仅限**finite positive weighted two-way table**；`w(q,b)=w_Q(q)w_B(b)` 当且仅当 `A` 与 `B0` 正交；顺序无关当且仅当 product weights；非 product 时只推出**存在性 witness**，而不是“每个输入都顺序相关”；错误顺序下出现的非零输出是 **sequential stripping artifact**，不是真 interaction residual；并保留了 exact `2 x 2` 有理证书示例。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:41-84,108-113,177-190,229-255,285-335,360-369`；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:30-66`；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:24-65,78-248`。）

我还做了一个严格的本地再验证：重跑了 bundle 内的两份脚本。`debranded_residual_transport_exact_witness_v1_4.py` 重新生成后的 exact witness 与当前 bundle 中的主 witness、对称 witness、以及 `D_w` 精确矩阵一致；`debranded_residual_transport_harness_v1_3.py` 重新生成后的 harness 保持相同的 `threshold_contract_sha256` 与四个 block 的 pass 状态，仅存在时间戳与机器精度级别的浮点舍入差异。这说明 **exact math 没有被 v1.5 wording 修补悄悄改坏**。  
（本地执行核对；并与 `from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:32-60,61-211`、`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:1-249` 比对。）

## 文献地板与重复风险

`BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 第 40–49 行已经把你要求的 durable floor 十条全部列齐：Hooker 2007；Chastaing–Gamboa–Prieur 2012；Chastaing–Gamboa–Prieur 2014/2015；Owen–Prieur 2017；Iooss–Prieur 2019；Il Idrissi et al. 2025；Lamboni 2026；Böttcher–Spitkovsky 2010；Corach–Maestripieri arXiv:1011.5237；Halmos 1969。就“文献是否存在、是否是正确近邻、是否足以形成 durable floor”而言，这一项我判 **PASS**。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:33-49`。）这些条目与外部稳定记录相符：Hooker 2007 确属 dependent-variable functional ANOVA 诊断文献；Chastaing–Gamboa–Prieur 2012 与 2015 分别对应 generalized Hoeffding–Sobol decomposition 与 dependent-variable numerical methods；Owen–Prieur 2017 与 Iooss–Prieur 2019 对应 dependent inputs / correlated inputs 下的 Shapley 重要性与 sensitivity；Il Idrissi et al. 2025 与 Lamboni 2026 则明确占据了 dependent random variables / non-independent variables 的近邻地带。citeturn3search2turn6search0turn2search3turn2search4turn4search8turn5search4turn1search2

其中 **Lamboni 2026** 的纳入是实质性收口，而不是装饰性加条目。该文确实是 2026 年的 SIAM/ASA JUQ 文章，题名就直接指向“ANOVA-Type Decompositions of Functions with Non-independent Variables”，这正是你这篇短札最容易被误读为“我也在做 dependent-input ANOVA program”的邻域。因此，把它写进本地 positioning floor，是正确且必要的。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:46`；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:108-110`。）citeturn1search2turn1search5

projection-theory 边界也已经写出来了。BIB 文件把 Böttcher–Spitkovsky 2010、Corach–Maestripieri 2010、Halmos 1969 收进 floor，并在 positioning paragraph 里明说“**not** a new projection theory”；placeholder 也把安全 novelty framing 锁在“compact finite weighted projection-order artifact note with an exact `2 x 2` witness”上，而不是推广成 noncommuting projections 的一般理论。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:47-49,53-60`；`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:122-126`。）外部稳定记录也支持这种收缩：two-projections / products of orthogonal projections / two subspaces 这些背景本来就已有成熟文献占位，你的安全做法只能是“借背景，不抢理论地盘”。citeturn5search5turn3search3turn9search4

关于 duplicate risk，我的判断是：**当前更像 overclaim risk，而不是 exact duplicate risk**。我检查到的稳定近邻记录都在 broad dependent-input decomposition、Shapley/sensitivity、two-projections / two-subspaces 背景里，但没有看到一个稳定记录与这份 bundle 当前锁定的狭义命题完全同构：即“finite positive weighted two-way table + order-independence iff product weights + existential pure-main-effect witness + exact `2 x 2` rational certificate”的这个组合。这个结论应理解为**基于所检查邻域文献的审慎推断**，而不是对全世界文献的非存在证明。citeturn3search2turn6search0turn2search4turn4search8turn5search4turn1search2turn5search5turn3search3turn9search4

## 审核矩阵

| 检查项 | 结论 | 审核意见 |
|---|---|---|
| `v1_4_WARN_items_closed` | **WARN** | 关闭了大部分，但**没有完全关闭**。bibliography、Lamboni、projection boundary 都已补上；未关闭的是 harness 边界语句的**统一性**，尤其 `README.md` 仍未实际写入规范句，只在说明下一轮要检查它。（本地证据：`README.md:221-225`；`BIBLIOGRAPHY_AND_POSITIONING...:33-65`。） |
| `formal_bibliography_floor` | **PASS** | 十条 durable floor 全在，且与稳定记录吻合。（本地证据：`BIBLIOGRAPHY_AND_POSITIONING...:40-49`。）citeturn3search2turn6search0turn2search3turn2search4turn4search8turn5search4turn1search2turn5search5turn3search3turn9search4 |
| `Lamboni_2026_inclusion` | **PASS** | 已写进 bibliography floor，也进入 placeholder 的最低 related-work 清单。（本地证据：`BIBLIOGRAPHY_AND_POSITIONING...:46`；`PREPRINT_PLACEHOLDER...:108-110`。）citeturn1search2turn1search5 |
| `projection_theory_boundary` | **PASS** | “not a new noncommuting projection theory” 的边界已经落地，且有 Böttcher / Corach / Halmos 三层背景支撑。（本地证据：`BIBLIOGRAPHY_AND_POSITIONING...:47-49,53-60`；`PREPRINT_PLACEHOLDER...:122-126`。）citeturn5search5turn3search3turn9search4 |
| `harness_regression_only_boundary_markdown` | **WARN** | 含义正确，但**不是锁定的一句规范句**。现在写成了“两句近义句”：deterministic regression support only + JSON floating-point outputs are not proof artifacts。语义安全，形式仍不统一。（本地证据：`SYNTHETIC_HARNESS_V1_3_20260628.md:12-14,106-109`。） |
| `harness_regression_only_boundary_json` | **WARN** | JSON 里同样是分拆表达：`harness_boundary`、`proof_responsibility`、`forbidden_interpretation` 三处都在说对的事情，但**没有把规范句原文作为一个统一字段落地**。（本地证据：`synthetic_harness_v1_3_20260628.json:13-15,209-211`。） |
| `harness_regression_only_boundary_script` | **WARN** | script docstring 与自动生成 markdown 的文案都明确否认“float regression harness = proof”，但仍是近义改写，并非锁定原句。（本地证据：`debranded_residual_transport_harness_v1_3.py:4-8,448-455`。） |
| `project_internal_wording_removed` | **PASS** | 我没有在目标本地文件中再看到 `diagnostic field` / `stable non-additive field` 等项目内部术语；当前对象名基本已回到 two-way table / array 与 finite weighted setup。（本地证据：`PREPRINT_PLACEHOLDER...:13-17,40-47,122-126`；`BIBLIOGRAPHY_AND_POSITIONING...:17-31,53-60`；对目标文件关键词检索无命中。） |
| `novelty_wording_narrow_enough` | **PASS** | bibliography file 已把安全 novelty sentence 锁为 **“a compact finite weighted projection-order artifact note with an exact 2 x 2 witness”**，placeholder 也未超过这个边界。（本地证据：`BIBLIOGRAPHY_AND_POSITIONING...:17-21`；`PREPRINT_PLACEHOLDER...:122-126`。） |
| `exact_math_still_unchanged` | **PASS** | 五个关键边界都还在：有限正权两向表；product-weight iff orthogonality；order-independence iff product weights；非 product 只给 existential witness；wrong-order residual 是 sequential stripping artifact；exact `2 x 2` witness 保持为证书级例子。（本地证据：`FORMAL_NOTE_V1_3_ORDER_DEFECT...:108-113,177-190,229-255,285-335`；`EXACT_WITNESS_V1_4...:32-66`；`exact_witness_v1_4...json:24-65,78-248`。） |
| `preprint_placeholder_ready_for_short_note_drafting` | **WARN** | 内容上已经接近短札门，但 placeholder 自己仍写着“Revise first”，而且 harness boundary 还没统一到指定句；因此我不建议现在就判通过。（本地证据：`PREPRINT_PLACEHOLDER...:73-79,122-126,154-169`。） |
| `evidence_boundary` | **PASS** | `definitions_and_harness_viable_only` 与 `insufficient_artifact` 保持一致，并持续拒绝 MaoField empirical upgrades、full panel、training、new loss、observed field、completed formal system 等 forbidden upgrades。（本地证据：`STATE.md:16,24-29`；`FORMAL_NOTE_V1_3_ORDER_DEFECT...:16-39,362-369`；`EXACT_WITNESS_V1_4...:16-28,62-66`；`synthetic_harness_v1_3_20260628.json:9-30`。） |
| `non_specialist_explanation` | **WARN** | bundle 里有一段不错的非专业解释，但它在归档 audit report 里，不在当前 placeholder / note 主体里；作为门审，这不是数学阻断项，但它还没有进入实际短札草稿对象。（本地证据：`from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_v1_4_exact_bibliography_audit_20260629.md:157-161`；而 `PREPRINT_PLACEHOLDER...` 未含对应段落。） |

## 仍需修正的最小剩余项

剩余问题是**小修，不是重写**。你不需要再加新数学，不需要再补新 bibliography 条目，也不需要再扩 related work。你只需要把下面这句话，**按原文一字不改地统一写进指定工件**：

> **The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.**

当前最关键的缺口是 `README.md`。它现在只说下一轮 final-gate 要检查 “regression-support-only across markdown/JSON/script”，但它自己没有把规范句写出来，所以还不能算 WARN fully closed。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/README.md:221-225`。）

我建议的最小修补如下，不需要改动任何数学内容：

- 在 `from_repo/docs/infra/debranded_residual_transport/README.md` 的 `## Current Next Step` 前后，直接插入上面的规范句原文。  
- 把 `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md` 第 77–79 行当前的近义表述，替换成该规范句原文。  
- 把 `SYNTHETIC_HARNESS_V1_3_20260628.md` 第 12–14 行当前的两句改写，替换成该规范句原文。  
- 在 `synthetic_harness_v1_3_20260628.json` 中保留现有安全字段也可以，但**必须新增或改写一个字段**，使该规范句原文完整出现一次。  
- 在 `scripts/debranded_residual_transport_harness_v1_3.py` 中，至少把模块 docstring 与生成 markdown 的 boundary 文案，统一成这句原文。  
（本地证据：`PREPRINT_PLACEHOLDER...:77-79`；`SYNTHETIC_HARNESS_V1_3_20260628.md:12-14`；`synthetic_harness_v1_3_20260628.json:13-15,209-211`；`debranded_residual_transport_harness_v1_3.py:4-8,448-455`。）

除此以外，我只给一个可选的、非阻断的 copyedit 提醒：你当前 placeholder 的标题 **“Order Defects in Finite Weighted Residual Decompositions”** 比锁定的 novelty sentence 稍宽，读感上仍可能比正文更像一个一般性 decomposition note。它不是 gate blocker，但如果你想把误读风险压到最低，标题最好也向“finite weighted projection-order artifact / two-way table / exact 2×2 witness”收窄。  
（本地证据：`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:1,7-17,122-126`。）

## 结论

我的严厉结论是：**v1.5 已经把真正困难的部分做完了，剩下的不是数学，不是 bibliography floor，不是 Lamboni，不是 duplicate-risk 主体，而是“把安全边界句子在指定工件里做成真正统一文本”**。在目前这个状态下，我不能判短札草稿门已通过；但我也明确地说，**它离通过只差一轮很小的 wording cleanup**。  
（本地证据：`README.md:194-200,221-228`；`BIBLIOGRAPHY_AND_POSITIONING...:17-31,33-81`；`PREPRINT_PLACEHOLDER...:73-79,122-126,154-169`。）从外部文献视角看，这样的收窄是正确方向：邻域文献已相当成熟，安全做法就是把叙述稳定地锁在“有限加权两向表中的 projection-order artifact 与 exact `2 x 2` witness”这一层，不再给任何 broad-theory 误读留下缝隙。citeturn3search2turn6search0turn2search4turn4search8turn5search4turn1search2turn5search5turn3search3turn9search4