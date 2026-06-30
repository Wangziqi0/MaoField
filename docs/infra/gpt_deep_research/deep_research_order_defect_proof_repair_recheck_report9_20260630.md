# Order-Defect Proof-Repair Recheck V4 审计报告

## Bundle Identity And Verdict

我先做了非实质性核验。上传文件本身是 `MaoField_PRO_OrderDefect_ProofRepairRecheck_V4_FINAL_20260630_1358.zip`；审计侧本地计算到的该 zip SHA-256 为 `0285cf2678f149eddf2caaf8ffd94032e3e47b2c3b9d4ebdfe0e3aaaf46d512c`。解压后，`PACKAGE_README.md` 明确把它标识为 “Order-Defect Proof-Repair Recheck V4 Package”，并说明这是 gate/proof/bibliography recheck material only；包内没有字面名为 `SHA256SUMS` 的文件，但有 `PACKAGE_FILE_MANIFEST.sha256`，其内部文件清单经本地逐项校验通过。更关键的是，`STATE.md` 与 `MD_CATALOG.md` 都把当前目标包写成 `MaoField_PRO_OrderDefect_ProofRepairRecheck_V4_FINAL_20260630_1358.zip`；同时，RAG 记录把较旧的 `1303`/`e866...` 轨迹明确标成 superseded/provenance，而把 final/finalfix/finalclean 叙述留作当前链路。因此，这个 bundle **看起来是 final 1358 包，而不是旧的 superseded 包**，不触发 `BUNDLE_VERSION_MISMATCH`。不过，`STATE.md`/`MD_CATALOG.md`/RAG 反复引用的 package-record 文件 `from_repo/docs/infra/DEBRANDED_RESIDUAL_TRANSPORT_19_PACKAGE_ORDER_DEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md` 实际并未随 zip 一起上传，所以“zip 自身哈希”无法在 bundle 内部再闭合到那份 package record；这是一条身份链残余缺口，但不足以把当前包判成旧包。 （`PACKAGE_README.md:L1-L6`；`from_repo/STATE.md:L16-L17,L88-L89`；`from_repo/MD_CATALOG.md:L9,L72-L76`；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md:L152-L162,L211-L228,L248-L319,L340-L369`）

**Verdict**

```text
PROOF_REPAIR_ACCEPTED_FOR_LOCAL_DRAFT_ONLY
```

这个 verdict 的含义是：在用户限定的有限维对象上，Proposition 2 与 Proposition 3 的 proof-repair candidate 已经把 report(8) 指向的核心逻辑缝补到可接受的本地草稿级；但这仍然只是 local draft / advisory 结论，不是 proof authority，更不解除 emergency lock，也不授权 paper body、posting 或 Mode B 升级。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L4-L5,L9-L12,L13-L32`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md:L8-L18,L20-L41,L83-L86`；`from_repo/STATE.md:L16,L24-L28`）

## Claim Labels

| 项目 | 结论 |
|---|---|
| Proposition 1 | `COMPLETE_LOCAL_DRAFT` |
| Proposition 2 | `COMPLETE_LOCAL_DRAFT` |
| Proposition 3 | `COMPLETE_LOCAL_DRAFT` |
| exact witness | `COMPLETE_LOCAL_DRAFT` |
| deterministic harness | `COMPLETE_LOCAL_DRAFT` |
| bibliography | `COMPLETE_LOCAL_DRAFT` |

理由需要缩得很窄。Proposition 1 的 centered-cell-indicator 反向证明是完整的有限和展开；Proposition 2 的修补版已经把 `D_w=0 => P_A|_{B0}=0 => A ⟂ B0 => product` 这条链闭合；Proposition 3 的修补版已经把“非 product ⇒ 存在 `K in B0` 且 wrong-order 非零但 true additive residual 为零”的存在性证明闭合，并明确拒绝 universal reading。exact witness 在 Markdown、JSON、脚本三个层面上对同一 2×2 有理证书保持内容一致；deterministic harness 作为**回归支持工件**也是自洽的，但它的角色严格受限于 regression support only；bibliography 的元数据和定位语句也已经压到 bundle 自己要求的保守边界。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L106-L152,L177-L239,L243-L283,L285-L335`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L71-L108,L110-L158,L164-L239`；`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L30-L66`；`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:L7-L18,L34-L39,L44-L79`；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L33-L49,L53-L79`）

## Blocking Issues

就数学证明本身而言，我没有发现继续阻断 Proposition 2 或 Proposition 3 的硬性 proof blocker。真正留下的是三类**非证明主干**的清理项。第一，bundle 身份链并不完全自闭：`STATE.md`、`MD_CATALOG.md` 与 RAG 记录都把当前 zip 的 authoritative zip hash 指向外部 package record / SHA256SUMS，但那份 package-record Markdown 并未随本 zip 一起提供。第二，标签文字存在轻微漂移：report(8) 与其 adoption note 仍用 `PLAUSIBLE_LOCAL_DRAFT`，而 taskbook、`STATE.md`、`MD_CATALOG.md` 已换成 `PROOF_REPAIR_CANDIDATE`。第三，exact witness 与 harness 的**整文件** SHA-256 在跨运行环境复跑时并不稳定，但这是脚本设计使然，不构成数学内容矛盾。 （`from_repo/STATE.md:L16,L88-L89`；`from_repo/MD_CATALOG.md:L9,L72-L73`；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md:L158-L162,L250-L263,L315-L319`；`from_repo/docs/infra/gpt_deep_research/deep_research_order_defect_proof_biblio_repair_audit_report8_20260630.md:L32,L41-L42`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md:L19-L25`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md:L56-L66`）

如果 node36 希望把状态文本彻底统一，最值得补的一刀不是再改数学证明，而是把上述 label drift 和 package-record 缺件补齐；否则以后做身份链或状态链审计时还会反复看到 “1303 provenance / 1358 final / external hash only” 这类残余噪音。 （`from_repo/STATE.md:L16`；`from_repo/MD_CATALOG.md:L9,L73-L76`；`from_repo/docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_ORDERDEFECT_PROOF_REPAIR_RECHECK_V4_20260630.md:L211-L228,L248-L369`）

## Proof Details

### Proposition 2

`A cap B0 = {0}` 这一步成立。candidate 在 Lemma 0 中说得够用：若一个函数既只依赖 `q` 又只依赖 `b`，则它在 `Q x B` 上必为常数；而落在 `A` 或 `B0` 中又要求相应加权均值为零，所以该常数只能是零。这里没有隐藏的额外假设，除了 bundle 已经固定的“有限、正权、总和为 1”，这也自动排除了空行/空列集合。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L71-L80`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L212-L218`）

`D_w = P_B0 P_A - P_A P_B0` 这一步也可接受，但必须把 candidate 与 source note 一起读。candidate 直接给了结论；source note 则补了缺省展开：先写成 `(P_B0P_A-P_AP_B0)(I-P_C)`，再用 `P_A 1 = P_B0 1 = 0` 说明 commutator 右乘 `P_C` 为零，于是可简化为全空间上的 `P_B0P_A-P_AP_B0`。因此，这一步不是空降。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L65-L69`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L156-L175`）

对任意 `b in B0`，由 `P_B0 b=b` 得到 `0=D_w b=P_B0P_Ab-P_Ab`，于是 `P_A b = P_B0 P_A b`，所以 `P_A b` 落在 `B0`；另一方面，`P_A b` 当然落在 `A`。这就把 `P_A b` 放进 `A cap B0`，再由上一步推出 `P_A b=0`。这一串推理完全闭合，没有多余跳步。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L138-L148`）

接着的 self-adjointness 步也成立。对任意 `a in A`、`b in B0`，因为 `P_A` 是到 `A` 的正交投影且自伴，`a=P_A a`，所以 `<a,b>_w = <P_A a,b>_w = <a,P_A b>_w = 0`。candidate 写成 `<a,b>_w = <a,P_A b>_w`，在这里是充足而正确的。然后由 Proposition 1 回推 product weights，等价链闭合。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L150-L158`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L106-L152`）

degenerate one-row / one-column 情形也没有额外风险。candidate 明确指出此时 `A` 或 `B0` 之一为零，且任意正的单行或单列表都等于其边际乘积；这和 Proposition 1 的退化讨论一致。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L160-L162`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L150-L152`）

### Proposition 3

第一步“非 product ⇒ `A` 不与 `B0` 正交”完全来自 Proposition 1 的逆否命题；candidate 随后利用 `<a,b>_w = <a,P_A b>_w` 选出一个 `b in B0` 使 `P_A b != 0`，这就是所需 witness 的来源。这里的量词是**存在性**，不是全称性。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L180-L187`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L229-L239`）

把这个 `b` 记作 `K` 后，`K in B0` 自动给出两件事：其全局均值为零，所以 `P_CK=0`；同时 `P_B0K=K`。因此 `R_B_then_Q K=(I-P_A)(I-P_B0)(I-P_C)K=0`。这一步没有缺口。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L187-L194`）

另一侧，candidate 算出 `R_Q_then_B K = -(I-P_B0)P_AK`。若假设它也为零，那么 `P_AK=P_B0P_AK`，于是 `P_AK` 同时落在 `A` 与 `B0`；借助 Lemma 0 只能为零，这与 `P_AK != 0` 矛盾。所以 wrong-order 输出必须非零。这个 contradiction step 正是 report(8) 先前要求显式补上的那一刀，现在已经补上。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L196-L206`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md:L37-L44`）

最后，“这不是 true interaction residual，而只是 sequential stripping artifact” 的论断由 `K in N_add` 且 `(I-P_N)K=0` 直接支撑。candidate 也明确写了“该 statement 是 existential only；不声称 every input differs”。因此，命题的量词范围和语义边界现在都是对的。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L166-L178,L208-L215`；`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L229-L239,L254-L255`）

## Exact Witness Consistency

exact witness 的三件主工件在**数学内容**上是相互一致的。Markdown 给出 canonical JSON 名称与其 canonical SHA-256；JSON 给出 `K`、`R_B_then_Q K`、`R_Q_then_B K`、范数平方以及投影矩阵；脚本 `build_certificate()` 生成同一组有理数据，并把 JSON 的哈希再写回 Markdown。审计侧复跑脚本后，除 `runtime` 字段以及因 JSON 哈希变化而联动的 Markdown 中 `sha256=` 一行之外，其余数学字段与 bundle 内 canonical JSON 完全一致。换言之，**内容一致，整文件哈希跨环境不稳定**；真正稳定的是有理证书内容，而不是跨主机整文件重现哈希。 （`from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L9-L14,L44-L66`；`from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json:L51-L77,L78-L249`；`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:L126-L220,L223-L305`）

具体地说，exact witness 脚本本来就把 `platform.python_version()` 与 `platform.platform()` 写进 JSON 的 `runtime` 字段，然后再重新计算该 JSON 的 SHA-256 并写入 Markdown。因此，只要运行环境不同，整文件哈希就会变，但证书主体不会变。这个设计解释了为何 canonical JSON/MD 的 bundle 内哈希是自洽的，同时审计侧复跑时又会出现不同哈希。 （`from_repo/scripts/debranded_residual_transport_exact_witness_v1_4.py:L214-L218,L301-L304`）

deterministic harness 的情况也类似，但角色更低。它的 summary Markdown 在审计侧复跑时可以做到与 bundle 内版本字节级一致；JSON 则显式包含 `created_utc` 与 `environment`，所以跨环境整文件哈希会变化。bundle 自己也已经把这件事写明：harness 只是 deterministic regression support，不能当作 proof artifact，不能当作 MaoField empirical evidence。就它被允许承担的角色而言，它是自洽的；但它不承担 theorem-proof 职能。 （`from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:L7-L18,L34-L39,L44-L79`；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:L3-L14,L59-L60,L190-L212`；`from_repo/scripts/debranded_residual_transport_harness_v1_3.py:L403-L423,L437-L589,L602-L621`）

## Bibliography Risks

bibliography/positioning 的边界目前是保守而窄的：bundle 只允许把当前对象表述为“compact finite weighted projection-order artifact note with an exact 2×2 witness”，明确禁止把它提升成新 ANOVA、new dependent-input decomposition、new Sobol/Shapley theory 或 new noncommuting projection theory。这个 framing 与 rescue audit 的“finite illustrative artifact / warning note”完全一致。 （`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L51-L60,L65-L79`；`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L24-L32`）

元数据处理也够克制。Hooker 2007、Chastaing–Gamboa–Prieur 2012 与 2014/2015、Owen–Prieur 2017、Iooss–Prieur 2019、Il Idrissi et al. 2025、Böttcher–Spitkovsky 2010、Halmos 1969 都被当作近邻/背景而非 novelty vacuum；Corach–Maestripieri 只保留 arXiv `1011.5237` 级别的背景定位；Lamboni 2026 被明确要求保持在 “DOI / publisher-online-record only” 的表述，不得臆造最终印刷期卷页。 （`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L7-L22`；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L38-L49`）

**Duplicate-risk class**

```text
MEDIUM
```

这里的 `MEDIUM` 不是说发现了 exact duplicate；bundle 反而明确说 “No exact duplicate is identified”。我给 `MEDIUM` 的原因是：在 narrow artifact framing 下，精确重复风险低，但 2025–2026 的近邻文献，尤其 Il Idrissi et al. 2025 与 Lamboni 2026，已经把“dependent variables / non-independent variables 下的 Hoeffding / ANOVA-type decomposition”空间占得很近，所以真正的风险不在 exact duplication，而在措辞一旦外扩就迅速撞进已有广域理论。 （`from_repo/docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L14-L16,L22-L30`；`from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L45-L49,L67-L79`）

## Forbidden-Claim Scan And Next Node36 Action

在当前**受控 proof-repair 文件集**中，我没有发现被正面背书的 forbidden claim。candidate、taskbook、adoption note、wording lock、harness JSON 都是在否定式或 blocked-claims 语境下提到这些敏感词：不授权 paper body，不授权 completed formal system，不授权 training / new loss / observed field，也不把 JSON floats 或 harness 当证明。这个边界是清楚的。 （`from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md:L19-L32`；`from_repo/docs/infra/recovery/ORDER_DEFECT_D630_PROOF_REPAIR_TASKBOOK_20260630.md:L31-L41,L83-L86`；`from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_PROOF_BIBLIO_REPAIR_REPORT8_ADOPTION_NOTE_20260630.md:L49-L74`；`from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:L27-L52`；`from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:L9-L30,L209-L212`）

需要注意的只是 bundle 内仍保留了旧的 `PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`。它本身并未越界，反而专门列出 forbidden claims；但由于文件名与旧 drafting 轨迹容易造成误读，后续若继续做封闭审计，最好继续把它排除在“当前受控证明集”之外，而不是让它重新回到主读集。 （`from_repo/docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:L126-L145`；`from_repo/STATE.md:L24-L28`）

**Next Node36 Action**

```text
LOCAL_DRAFT_OK_BUT_KEEP_EMERGENCY_LOCK
```