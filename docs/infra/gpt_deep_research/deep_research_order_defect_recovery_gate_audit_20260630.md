# MaoField / Order-Defect Recovery 严格恢复审计

## 审计范围与结论先行

本次审计只按 bundle 内现存工件做恢复性核查，不把仓库外事实、公开网页、GitHub 页面或模型记忆当成补充证据。就 2026-06-25 至 2026-06-29 的 MaoField / Order-Defect / Mode A 有限维数学线而言，这个 bundle **基本内部自洽**，而且足以支持一次**gate-only 审计**：其核心对象、最小安全命题、v1.6 wording lock、v1.5 bibliography floor、v1.4 exact witness、以及 Mode A / Mode B 边界在多个文件中是相互钩住的。与此同时，它**不是 clean authoritative freeze**：恢复时间线明示抓包时工作树处于 dirty state，`STATE.md` 尚有修改、`docs/infra/recovery/` 尚未纳入 git 跟踪，因此它更像“可审计救援包”，不是“无争议定稿快照”。［证据：docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L5-L5,L7-L20；docs/infra/recovery/EVIDENCE_INDEX_SINCE_20260625.md:L6-L12,L16-L33；STATE.md:L16-L16；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L5-L13］

我的最终裁决是：

```text
STOP_AND_FIX_GATES
```

原因不是 Gate 1 或 Gate 2 自身失败，而是更高优先级的 **external-model emergency lock** 仍然生效。`STATE.md` 明写：在人工解除前，当前 OpenAI/Pro/外部模型输出一律只可视为 `non_authoritative_scratch` / `gate_only_audit`，不得作为 paper draft、proof authority、bibliography authority 或 posting authority；handoff 文件也因此把推荐动作写成 `STOP_AND_FIX_GATES`。所以，这个 bundle **足够支撑“现在不该写正文”的结论**，却**不足以授权“现在开始权威起草短札”**。［证据：STATE.md:L16-L16,L24-L29；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L15-L18,L70-L72］

## 内部一致性判断

如果只看这条线自身的主链文件，内部叙事是连贯的：`FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md` 把对象限定在有限正权二向表，并把允许上限锁在 `definitions_and_harness_viable_only`、把 MaoField 经验态锁在 `insufficient_artifact`；`EXACT_WITNESS_V1_4_20260629.md` 把一个 `2 x 2` 见证升级为精确有理证书；`BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 把 novelty 收窄为 “a compact finite weighted projection-order artifact note with an exact 2 x 2 witness”；`WORDING_LOCK_V1_6_20260629.md` 则把 harness 边界句精确锁定，并要求它逐字出现在 README、placeholder、harness markdown、harness JSON、harness script 五处。几份 recovery 文件又把这条链按 D625→D629 的提交时序重新编排，叙述上没有出现“先有结论、后补对象”的逆序塌陷。［证据：docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L16-L39,L41-L75；docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L30-L66；docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L51-L80；docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:L7-L25,L27-L33；docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L22-L43］

这种自洽并不等于“已成权威定稿”。bundle 自己反复把若干目标文件标成 `RISKY` 或 `ONLY_WITH_BOUNDARY`，尤其是 `README.md`、`PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md`、`WORDING_LOCK_V1_6_20260629.md` 与各类 harness 工件；它们可以用来做范围锁定与门审，但不能脱离边界单独提升结论。换句话说，这个包的内部结构更接近“受控救援工件集”，不是“随便抽一篇就能代表最终立场”。［证据：docs/infra/recovery/EVIDENCE_INDEX_SINCE_20260625.md:L19-L33,L45-L52,L55-L60,L129-L138］

还需要单独指出一个**非致命但真实存在的包级风险**：恢复时间线把抓包时的 git 状态完整保留下来，明确显示 `STATE.md` 为修改态，`docs/infra/recovery/` 尚未提交。也就是说，审计链条本身能工作，但它是从一个尚未完全封存的工作树抓出来的。这不会推翻当前最小数学对象，也不会否定 Gate 1/2 的文本支持，但会影响“现在就把它当最终可外发快照”的可信度。［证据：docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L7-L20；STATE.md:L16-L17］

## Gate 1 与 Gate 2 复核

**Gate 1 我判断为“真实支持”，不是空泛自报。** `GATE_RESCUE_AUDIT_20260629.md` 不仅写了 PASS，而且给出了五个指定工件中的具体命中位点；我对实际文件本身也能复核到同一句规范句：`README.md` 第 234 行、`PREPRINT_PLACEHOLDER...` 第 77 行、`SYNTHETIC_HARNESS_V1_3...md` 第 12 行、`synthetic_harness_v1_3...json` 第 13–14 与 210–211 行、`debranded_residual_transport_harness_v1_3.py` 第 6 与 25 行都逐字出现 canonical sentence。再加上 `WORDING_LOCK_V1_6_20260629.md` 明文规定这五处必须 verbatim 出现，可以认定 v1.6 wording WARN 已在 bundle 内被实际关闭。［证据：docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md:L7-L17；docs/infra/debranded_residual_transport/README.md:L232-L239；docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:L73-L78；docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md:L5-L18；docs/infra/debranded_residual_transport/synthetic_harness_v1_3_20260628.json:L9-L15,L30-L33；scripts/debranded_residual_transport_harness_v1_3.py:L2-L7,L24-L25；docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md:L7-L25］

**Gate 2 也是真支持，但支持的是“证据与范围边界”，不是“所有数学细节都已经终审完成”。** v1.3 formal note 已经锁定：对象仅是有限正权二向表；product-weight 当且仅当主效应子空间正交；顺序无关当且仅当 product weights；非 product 情况下只给存在性见证，明确否认“每个输入都顺序相关”；错误顺序产生的非零量是 sequential stripping artifact，而不是真 interaction residual；当前展示见证是精确 `2 x 2` 有理例子。recovery 的 Gate 2 审计恰好把这些边界逐项点名为 PASS，并把 ceiling 继续锁在 `definitions_and_harness_viable_only` / `insufficient_artifact`。［证据：docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_20260628.md:L43-L75,L108-L113,L179-L190,L231-L237,L245-L255,L287-L321,L360-L369；docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L30-L66；docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md:L19-L43；STATE.md:L16-L16,L24-L29］

但 Gate 2 的 PASS 不应被误读成“证明责任完全闭合”。数学救援审计把四个核心对象分成不同等级：Proposition 1 是 `COMPLETE_LOCAL_DRAFT`，而“order-independence iff product weights”与“pure-main-effect non-product artifact”仍分别是 `PLAUSIBLE_LOCAL_DRAFT`；只有 exact `2 x 2` witness 被标成 `CERTIFICATE`。因此，Gate 2 的真实含义是：**bundle 确实把能说什么、不能说什么钉住了**；可它并没有把一般性定理自动升级成“形式系统级完成”。［证据：docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md:L19-L27,L28-L35,L59-L61；docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L62-L66］

## 证明、引文与边界风险

当前最主要的**证明缺口**不在 `2 x 2` 例子本身，而在“从局部草案到可授权论文证明”的那一步。`MATH_PROOF_RESCUE_AUDIT_20260629.md` 已经把 general theorem 的状态写得很谨慎：Proposition 2 与 Proposition 3 仍是 `PLAUSIBLE_LOCAL_DRAFT`。同时，exact witness 证书虽然很强——九项 exact checks 全 pass，而且救援审计还记录了 scratch rerun 与 canonical exact JSON 的 sha256 完全一致——但该证书文件自己也明写：它**不替代 analytic proof**。因此，当前最佳表述应当是“局部证明方向与精确见证相容”，而不是“定理已经完成形式化终审”。［证据：docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md:L21-L27,L36-L61；docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md:L30-L42,L62-L66］

当前最主要的**引文风险**集中在 Lamboni 2026 的元数据表述。救援 bibliography audit 把它列为 `MEDIUM` duplicate/citation risk，并明确要求“把 Lamboni 2026 视为 DOI / online-or-publisher-record status only，不要超出抓到的 Crossref 记录去暗示最终 print issue metadata”。但 v1.5 bibliography/positioning 文件在条目中写成了“2026, 14(2), 691-710”，这在门审语境里属于应保守处理的部位。换言之，bibliography floor 本身是够用的，但 Lamboni 这一条最好在任何后续草稿中降格为 DOI/online 记录式写法，以避免不必要的元数据争议。［证据：docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L7-L18,L20-L23；docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L33-L49］

当前最主要的**claim-boundary 风险**来自历史遗留语汇，而不是当前核心文件本身。forbidden-claims 扫描给出 `BLOCKER: 0`，但 `WARNING: 247112`；恢复时间线和 handoff 都提醒这些 WARNING 大多是历史 prompt、旧审计、禁语清单、旧 transport/holonomy/gluing/curvature 线索，它们是“风险定位器”，不是自动判错器。也正因此，任何后续 drafting 一旦放宽检索范围，就很容易把已被废弃的 residual/transport/holonomy 词汇重新泄回短札文本。结论是：**当前主链没有明显越界，但全仓上下文非常脏，起草时必须只围绕受控文件集工作。**［证据：docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md:L5-L15；docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L70-L92；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L19-L24,L59-L68］

还有一个需要明确写出的**权限边界风险**：即使 Gate 1、Gate 2 现在都 PASS，`STATE.md` 仍把当下外部模型输出降为 `non_authoritative_scratch` / `gate_only_audit`，并明确要求“暂停把该包交给 Pro 撰写短札”。所以现在真正阻断 drafting 的，不是 wording mismatch，也不是 bibliography floor，而是**更高层级的 emergency lock**。如果忽略这点，等于用“局部门通过”擅自覆盖“全局权限关闭”，那会直接违反当前 bundle 自身的 canonical state。［证据：STATE.md:L16-L16,L24-L29；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L15-L18,L70-L72］

## 动作裁决

我的裁决仍然是：

```text
STOP_AND_FIX_GATES
```

这不是因为证据不足到要落入 `DO_NOT_DRAFT_EVIDENCE_INSUFFICIENT`；恰恰相反，bundle 对 gate-only 审计已经足够：核心对象、exact witness、related-work floor、forbidden claims、以及最小安全命题都已在包内落地。之所以不能选 `DRAFT_SHORT_NOTE_WITH_BOUNDARIES`，是因为 `STATE.md` 的外部模型紧急锁定尚未被人工解除，而当前任务又明确要求在该锁下不得把输出升级成 proof authority、bibliography authority 或 posting authority。换句话说，**不是“没东西可审”，而是“有足够东西得出：现在不能权威起草”**。［证据：docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L5-L13,L15-L18,L55-L72；docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md:L19-L27,L36-L61；docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L24-L32；STATE.md:L16-L16,L24-L29］

因此，对用户提出的五项要求，我的直接回答是：**一，bundle 基本内部自洽，但仍带 dirty-state 封存风险；二，Gate 1 与 Gate 2 都被 included files 实质支持；三，主要剩余风险是 general-proof authority gap、Lamboni 2026 元数据保守性、历史 WARNING 污染、以及 emergency lock；四，下一动作应为 `STOP_AND_FIX_GATES`；五，如以后允许 drafting，也只能在解除 lock 并完成最小修补后进入 guarded outline，不得直接外推为论文正文。**［证据：docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L7-L20,L70-L92；docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md:L7-L43；docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md:L19-L27；docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L20-L32；STATE.md:L16-L16,L24-L29］

## 仅在后续允许 drafting 时可用的受限提纲与必要修复

如果以后进入 drafting 阶段，这里**只能给 guarded outline，不给正文**。安全提纲应严格缩到六段：题目与一段 boundary；有限正权二向表设定；Proposition 1 与主效应正交的 product-weight iff；Proposition 2 与 sequential stripping order-independence 的 iff；Proposition 3 的存在性 pure-main-effect witness；`2 x 2` 精确有理证书与一句 narrow related-work/boundary paragraph。这个结构其实已经被 placeholder 的 “Preprint-Safe Next Step” 和 bibliography/positioning 文件预先规定好了。［证据：docs/infra/debranded_residual_transport/PREPRINT_PLACEHOLDER_ORDER_DEFECT_20260629.md:L150-L167；docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md:L17-L31,L51-L80］

进入那一步之前，我认为至少要完成四个**精确修复**。第一，必须由人工明确解除外部模型紧急锁，或者改走一个高可信、可复核的人工/离线通道；否则任何 draft 仍只能算 `non_authoritative_scratch`。第二，把当前 dirty working tree 整理成 clean committed / sealed snapshot，尤其要消除“`STATE.md` 修改中、`docs/infra/recovery/` 未跟踪”的快照歧义。第三，Lamboni 2026 在后续参考文献中一律按 DOI/online 记录保守书写，不再主动宣称超出 rescue audit 保守范围的 print 元数据。第四，任何 drafting 前都必须只围绕 v1.3 formal note、v1.4 exact witness、v1.5 bibliography/positioning、v1.6 wording lock、placeholder 与 recovery 审计这些受控文件工作，并对 WARNING rich 的历史文件保持隔离，避免 residual/transport/holonomy 等旧术语回流。［证据：STATE.md:L16-L16,L24-L29；docs/infra/recovery/RECOVERY_TIMELINE_SINCE_20260625.md:L7-L20,L70-L92；docs/infra/recovery/BIBLIOGRAPHY_RESCUE_AUDIT_20260629.md:L15-L23；docs/infra/recovery/FORBIDDEN_CLAIMS_SCAN_20260629.md:L5-L15；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L19-L24,L59-L68］

综合起来，当前 bundle 最稳妥、也最符合其自身 canonical state 的结论是：**可审，不可权威起草；两门已过，总锁未解；数学对象已被清晰收窄，但 general-proof authority 与 drafting authority 仍未被授予。**［证据：docs/infra/recovery/GATE_RESCUE_AUDIT_20260629.md:L7-L43；docs/infra/recovery/MATH_PROOF_RESCUE_AUDIT_20260629.md:L19-L27,L59-L61；STATE.md:L16-L16；docs/infra/recovery/HANDOFF_TO_GPT55PRO_20260629.md:L70-L72］