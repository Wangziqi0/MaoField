# D707 内部 v0 有限图路径循环缺陷说明严格内部关卡审查报告

## 执行摘要

我已按 `START_HERE_MAIN_PROMPT_20260708_1001_internal_v0_gate.md` 的顺序，仅基于上传 zip 内文件与随附哈希清单完成审查；该提示明确要求只用包内文件，并且只能在四个指定 verdict 中四选一。fileciteturn0file0

就**数学正文本身**而言，`docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md` 的有限维对象定义、空路径约定、路径缺陷组合恒等式、循环迭代望远镜恒等式、全局范数界、以及 restricted-norm 警告，整体上是连贯且边界受控的，未发现足以触发 `REJECT_OR_STOP_PARK` 的正文级数学错误（主说明见 `FORMAL_NOTE_D707...:34-252`；Loop 3 定义见 `.../loop3/FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md:19-193`；Loop 3 组合引理见 `.../loop3/COMPOSITION_LEMMA_LOOP3_20260707.md:7-148`；Loop 4 循环、望远镜与范数界分别见 `.../loop4/FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md:18-157`、`.../loop4/TELESCOPING_PROOF_LOOP4_20260707.md:7-157`、`.../loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md:7-141`）。

但就你要求的**严格 internal promotion-gate package 审核**而言，当前上传包的证据链**没有闭合**：其一，包内多份 manifest / review index 把三个 Loop 状态文件标为 core 且给出精确 SHA256，却未实际打包；其二，`STATE.md` 记录的 zip 哈希、prompt 哈希、以及文件数，与实际上传物和包内清单不一致；其三，`STATE.md` 与 Loop manifest 声称消费或引用的若干 D708 级别记录文件并未打包。因此，我不能在“严格 promotion-gate”层面直接给出接受结论。

**Verdict：`REQUEST_NODE36_FILES`**

**Zip SHA256：`2cf1a9117a1c521fb60be7f99014b62715b033090e17d7973e8fc651cd55965a`**。这个哈希由你随附的外部 `SHA256SUMS_20260708_1001_internal_v0_gate.txt` 给出，且与当前上传 zip 的实测哈希一致。fileciteturn0file1

- 数学主说明本体基本可成立为“内部本地说明”，但当前 verdict 不是被数学正文卡住，而是被**包证据完整性**卡住。
- `loop3/ARTIFACT_MANIFEST`、`loop4/ARTIFACT_MANIFEST`、`session4/REVIEW_ARTIFACT_INDEX` 均把 `LOOP_STATUS_LOOP0_20260707.md`、`LOOP_STATUS_LOOP3_20260707.md`、`LOOP_STATUS_LOOP4_20260707.md` 作为 precondition/core 证据，并给出哈希；这三文件却都不在 zip 内（分别见 `loop3/ARTIFACT_MANIFEST...:37-58,84-118,129-135`，`loop4/ARTIFACT_MANIFEST...:37-78,105-128,158-164`，`session4/REVIEW_ARTIFACT_INDEX...:9-17,35-60,63-79`）。
- `STATE.md` 声称 node19 桌面 zip 哈希为 `4b9721...`、prompt 哈希为 `3adc88...`、manifest=`51 files`；但当前上传 zip 的实测哈希是 `2cf1a9...`，包内 `START_HERE...` 与镜像 prompt 的哈希都是 `6b4219...`，包内 manifest 有 53 个 payload，解包后总文件 55 个，存在明显 provenance mismatch（`STATE.md:16-18`；`SHA256SUMS_D708_INTERNAL_V0_PROMOTION_GATE_20260708.txt:1-54`；`MANIFEST_D708_INTERNAL_V0_PROMOTION_GATE_20260708.txt:1-53`）。fileciteturn0file1
- `STATE.md` 还引用了 D708 package record、node19 delivery record、D708 RAG record 等文件，但这些不在 zip 内（`STATE.md:16,25-28`）。
- `loop3/ARTIFACT_MANIFEST` 与 `loop4/ARTIFACT_MANIFEST` 还把 `AGENTS.md`、`/media/amd/raid1/canonical/AGENTS.md`、`CLAUDE.md` 视为已消费输入，但包内并未提供，因此无法对“规则环境”做完全重放核验（`loop3/ARTIFACT_MANIFEST...:59-82`；`loop4/ARTIFACT_MANIFEST...:79-104`）。
- 需要的补件不是新的理论或外部数据，而是**node36 侧已被本包自身引用/哈希化/标为 core 的缺失内部文件**，以及一份与当前上传物一致的更正 provenance 记录。

## 审查范围与方法

本次审查只用上传包，不调用外部网页、仓库、公共资料，也不把 RAG、prompt、handoff、manifest 当作证明；这与 `START_HERE` 的约束一致。fileciteturn0file0 我实际按以下顺序核查：`STATE.md`、D708 taskbook、D707 主说明、Report38 及 adoption note、本地 verification、Loop0/3/4、Session4，随后回看包内 manifest 与 SHA256 列表，并对 zip 自身做解包、文件枚举与哈希复核。

包内涉及的节点标识主要是三类。`node36` 是打包、状态更新、以及本地 verification 的执行节点，见 `STATE.md:16-18,26-28` 与 `D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md:77-89`。`node19` 是 D708 promotion-gate 包的投递目标，见 `STATE.md:16,25,28`。`node22` 是一次性向量/RAG worker，见 `STATE.md:16` 与 `D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md:77-89`。这些节点信息在包内是“流程 provenance”，不是数学证明。

从格式和可读性看，当前 zip 内主证据全部为 `.md` / `.txt`，没有损坏或无法解压的成员；包内 `SHA256SUMS_D708_INTERNAL_V0_PROMOTION_GATE_20260708.txt` 对它**列出的**文件逐项校验均可通过。问题不在“已列入哈希表的文件被篡改”，而在“若干被其他文档标为核心证据或已消费输入的文件根本未入包”。

## 数学审计

主说明把对象严格限制为有限有向图 `G=(C,E)`、各 chart 上的有限维实赋范空间 `H_c, O_c`、线性 chart 映射 `Phi_c`、以及声明型边传输 `U_e, T_e`，并明确不把这些“transports”解释成经验观测场或 canonical identification，这一点与 taskbook 和 boundary guards 一致（`FORMAL_NOTE_D707...:34-54`，`D708_INTERNAL_V0_PROMOTION_GATE_TASKBOOK_20260708.md:46-121`，`BOUNDARY_GUARDS_LOOP4_20260707.md:7-47`）。类型层面没有发现错配：路径复合 `U_alpha, T_alpha` 的端点、缺陷映射 `Delta_alpha: H_{c_0} -> O_{c_k}` 的值域、循环缺陷 `Delta_gamma` 与迭代缺陷 `Delta_{gamma,n}` 的 base-chart endomorphism 结构，均保持一致（`FORMAL_NOTE_D707...:56-93,125-145`；对应前身草稿见 Loop 3/4 文件）。

空路径约定是自洽的。主说明把 `U_id_c = I_{H_c}`、`T_id_c = I_{O_c}`，并由此得 `Delta_id_c = 0`（`FORMAL_NOTE_D707...:69-82`）。Loop 3 组合引理文件还显式检查了当 `alpha=id` 或 `beta=id` 时右端退化到相应单一路径缺陷，未发现符号方向反转或 endpoint 错位（`COMPOSITION_LEMMA_LOOP3_20260707.md:120-145`）。

组合顺序约定也前后一致。Loop 3 先固定 `beta circ alpha` 表示“先走 `alpha`，后走 `beta`”，并对应 `U_{beta circ alpha}=U_beta U_alpha`、`T_{beta circ alpha}=T_beta T_alpha`（`FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md:113-118`）。主说明与 Loop 3 引理均据此证明
\[
\Delta_{\beta \circ \alpha}=T_\beta \Delta_\alpha + \Delta_\beta U_\alpha,
\]
其中加减中间项 `T_beta Phi_{c_1} U_alpha` 的方式在类型上正确，且左右两项都确实是 `H_{c_0} -> O_{c_2}`（主说明 `FORMAL_NOTE_D707...:95-123`；前身证明 `COMPOSITION_LEMMA_LOOP3_20260707.md:75-118`）。

循环定义与望远镜恒等式也成立。Loop 4 先把 `gamma` 作为基于 `c_0` 的闭路径，定义 `U_gamma, T_gamma` 为 base-chart endomorphisms，再定义 `Delta_gamma` 与 `Delta_{gamma,n}`（`FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md:43-153`）。随后把组合引理应用于 `alpha=\gamma^n, beta=\gamma`，得到递推
\[
\Delta_{\gamma,n+1}=T_\gamma\Delta_{\gamma,n}+\Delta_\gamma U_\gamma^n,
\]
再经归纳证明
\[
\Delta_{\gamma,n}=\sum_{j=0}^{n-1}T_\gamma^{n-1-j}\Delta_\gamma U_\gamma^j.
\]
这个证明没有额外偷用可逆性、正交性或不变性（`TELESCOPING_PROOF_LOOP4_20260707.md:33-157`；主说明 `FORMAL_NOTE_D707...:150-188`）。

范数界部分的“安全版”写法也是对的。主说明与 Loop 4 bounds 文件都把对任意子集 `S` 的上界写成
\[
\|\Delta_{\gamma,n}|_S\|
\le \sum_{j=0}^{n-1} a^{n-1-j} b^j \|\Delta_\gamma\|,
\]
即右端使用**全局**算子范数 `||Delta_gamma||`，而不是对子集 `S` 的受限范数（`FORMAL_NOTE_D707...:190-252`；`CYCLE_NORM_BOUNDS_LOOP4_20260707.md:26-141`）。这一点非常关键，因为望远镜求和中的 `Delta_gamma` 实际作用在 `U_gamma^j x` 上；若没有 `U_gamma^j(S) \subset S` 一类 image-control / invariance，直接替换为 `||Delta_gamma|_S||` 并不合法。主说明在第 7 节把这一封口写清楚了，Loop 3/4 也一致强调 `S` 若只是子集而非线性子空间，则这里只是 restricted sup-ratio，不应套用一般线性算子范数定理（`FORMAL_NOTE_D707...:236-252`；`FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md:150-169`；`CYCLE_NORM_BOUNDS_LOOP4_20260707.md:98-137`）。

边界与 overclaim 控制总体合格。主说明明确拒绝 public-ready、paper-ready、NMI-ready、empirical-positive、broad theory、dynamic-collapse、black-box solved、proof-by-artifact，并把 `CID_gamma(S)`、`CIC_N(gamma,S)` 限定为 finite-object bookkeeping quantities（`FORMAL_NOTE_D707...:10-32,140-148,254-286`）。此外，它还在 positioning 段承认该对象“可能接近标准的 commutator / intertwining / path-defect algebra”，因此 duplicate risk 至少 `MEDIUM` 的内部态度是自洽的（`FORMAL_NOTE_D707...:254-262`；`STATE.md:16,27`）。

综合而言，**数学正文单独看，最接近的结论其实是“可作为内部本地说明继续保留”**；真正阻断当前 strict promotion-gate 的，不是 theorem body，而是包证据层的缺件与 provenance 不一致。

## 证据链与完整性核验

先说一致的部分。包内 `SHA256SUMS_D708_INTERNAL_V0_PROMOTION_GATE_20260708.txt` 能通过对其所列文件的逐项校验；已入哈希表的文件没有出现“包内 hash 不匹配”的情况。zip 也可正常解压，所有成员均为文本型证据文件，格式上没有异常。zip 内所有成员的打包时间戳统一为 2026-07-08 02:18，作为一次性打包时间是可以接受的；文档正文中的自述日期则主要分布在 2026-07-07 与 2026-07-08，时间顺序也基本合理。

但严格证据链存在三组更重要的问题。

第一组是**缺失的 core/status 证据**。`loop3/ARTIFACT_MANIFEST` 说它预先 byte-check 了 `loop0/LOOP_STATUS_LOOP0_20260707.md`，并在 artifact hashes 里给出了 `LOOP_STATUS_LOOP3_20260707.md` 的 SHA256；`loop4/ARTIFACT_MANIFEST` 又给出了 `LOOP_STATUS_LOOP4_20260707.md` 的 SHA256；`session4/REVIEW_ARTIFACT_INDEX` 更把这三份状态文件全部列为 core，并写明 exact status 与 hash（`loop3/ARTIFACT_MANIFEST...:37-58,95-105,129-135`；`loop4/ARTIFACT_MANIFEST...:37-78,117-128,158-164`；`session4/REVIEW_ARTIFACT_INDEX...:9-17,35-60`）。然而这些文件都不在 zip 内。这意味着“Loop0 → Loop3 → Loop4 → Session4”的 dispatch/precondition 链不能在当前包里被完整复算。

第二组是**provenance 元数据冲突**。`STATE.md` 报告当前 D708 promotion-gate zip 的 SHA256 为 `4b9721a855e4...`，prompt SHA256 为 `3adc882ea025...`，manifest 为 `51 files`（`STATE.md:16-18`）。但你随附外部 `SHA256SUMS_20260708_1001_internal_v0_gate.txt` 给出的 zip 哈希是 `2cf1a9117a1c...`，并且这与当前上传 zip 的实测哈希一致；同一外部清单对 `START_HERE...` 的哈希是 `6b42193d...`，这也与包内 `START_HERE...` 以及其镜像文件 `docs/infra/gpt_deep_research/GPT55_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PROMPT_20260708.md` 一致。fileciteturn0file1turn0file0 包内 manifest 共有 53 条 payload，而解包后总文件数为 55。也就是说，**当前上传物与 `STATE.md` 描述的 package/provenance 不是同一字节态**，至少不能直接当成同一 package 处理。

第三组是**被声称消费但未入包的支持记录**。`STATE.md` 引用了 `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md`、`docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md`、`docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_D708_INTERNAL_V0_GATE_PACKAGE_20260708.md`，但这几份文件都不在 zip 内（`STATE.md:16,25`）。而 loop manifests 还把 `AGENTS.md`、外部路径下的 `AGENTS.md`、以及 `CLAUDE.md` 视作已消费规则输入（`loop3/ARTIFACT_MANIFEST...:59-82`；`loop4/ARTIFACT_MANIFEST...:79-104`），同样未打包。它们未必都是数学证明的必要文件，但的确是当前包自己声称依赖过的“exact local records”。

下图能更直观看出证据链与缺口的关系：

```mermaid
timeline
    title D707 到 D708 包内证据链
    2026-07-07 14:05 : Loop 3 manifest 生成
                     : 声称依赖 LOOP_STATUS_LOOP0
                     : 产出 LOOP_STATUS_LOOP3
    2026-07-07 14:11 : Loop 4 manifest 生成
                     : 声称依赖 LOOP_STATUS_LOOP0 与 LOOP_STATUS_LOOP3
                     : 产出 LOOP_STATUS_LOOP4
    2026-07-07 晚间 : Session 4 review index / handoff / blockers
                   : 把三个 LOOP_STATUS 标成 core
    2026-07-07 21:01 : Report38 adoption 与 local verification
    2026-07-08 10:01-10:10 : D708 taskbook 与 STATE 打包记录
                           : 但当前上传包未含三个 LOOP_STATUS
                           : 且 STATE 中 zip/prompt 哈希与实物不一致
```

下表汇总了本次严格核验中最关键的“被引用证据文件”状态。前半部分优先列出 `START_HERE` 与 D707 主说明要求阅读或直接依赖的文件；后半部分列出当前包自己声称存在、但实际缺失的重要证据文件。

| 引用文件 | 存在 | 文件类型 | 大小 | SHA256 |
|---|---|---:|---:|---|
| `START_HERE_MAIN_PROMPT_20260708_1001_internal_v0_gate.md` | 是 | md | 6148 | `6b42193d6259465f4aa57402f5acc73980ab49b54bf0bfaac6c2894808c8cd8b` |
| `STATE.md` | 是 | md | 43025 | `ea400df33b60e802b2cee09f8ab912141407d6a7cbc2a82345f0c4cef945c714` |
| `docs/infra/recovery/D708_INTERNAL_V0_PROMOTION_GATE_TASKBOOK_20260708.md` | 是 | md | 4017 | `ae60a7bba8ae5d0871c020fca376a0f1c3d344bcdf64ac8ac5c3149d974d3026` |
| `docs/infra/debranded_residual_transport/FORMAL_NOTE_D707_CHART_PATH_CYCLE_DEFECT_V0_20260707.md` | 是 | md | 7612 | `e6e144e19f9827d40545458ee98c18ffc14732b001fdd3e458aea0154c945235` |
| `docs/infra/gpt_deep_research/deep_research_d707_bounded_formal_note_v0_draft_report38_20260707.md` | 是 | md | 18115 | `f596ba3895a49158803640029c89278335c7cabaad7fc2a8bc46907f1d40dffa` |
| `docs/infra/gpt_deep_research/D707_BOUNDED_FORMAL_NOTE_V0_DRAFT_REPORT38_ADOPTION_NOTE_20260707.md` | 是 | md | 2707 | `a7f805a1f1fb2cee2dfaf9dbc0f846d379f97a010dec1ef15f4a9fff9195cfbf` |
| `docs/infra/recovery/D707_BOUNDED_FORMAL_NOTE_V0_LOCAL_VERIFICATION_20260707.md` | 是 | md | 3493 | `39b91429d55e218b364c684b1bdd0655fa54f0e15de75e18dd1714e9a57ae8e5` |
| `docs/infra/recovery/d707_split_loop_outputs/loop0/CLAIM_LEDGER_LOOP0_20260707.md` | 是 | md | 5954 | `370c776a5cd79965a7095ef18a115e6e373e2569d0b1ffc1a8149744a31903cc` |
| `docs/infra/recovery/d707_split_loop_outputs/loop0/FORBIDDEN_CLAIMS_CHECKLIST_LOOP0_20260707.md` | 是 | md | 3057 | `835319c1e3910bd1a4a4ced00c39ebd571ee3a486024c90d92e46b5827eb5508` |
| `docs/infra/recovery/d707_split_loop_outputs/loop3/FORMAL_NOTE_TYPED_CHART_PATH_DEFINITIONS_LOOP3_20260707.md` | 是 | md | 7017 | `2ceae0ddbed64ff67508815b3e842d7d1a302e64ba430bdbf4d7b7de50e373dc` |
| `docs/infra/recovery/d707_split_loop_outputs/loop3/COMPOSITION_LEMMA_LOOP3_20260707.md` | 是 | md | 3411 | `80da7b7db6dc8784af72d6ccd7a51795077f54f8c663112a7617a8b9c829e6dd` |
| `docs/infra/recovery/d707_split_loop_outputs/loop3/ARTIFACT_MANIFEST_LOOP3_20260707.md` | 是 | md | 5254 | `37bd41d8ff0a80a1a6a56cec6a088f9117c7c0d55b4977936dc505a0bbb0402f` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/FORMAL_NOTE_FINITE_CYCLE_DEFECT_LOOP4_20260707.md` | 是 | md | 4998 | `22d79e723e874a0814e2d6220d5c539cd55148d91c6cd9c4560ba6d43122998d` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/TELESCOPING_PROOF_LOOP4_20260707.md` | 是 | md | 3326 | `ae9544f6b0c4bac4e36033298718a534847eb3fdacca335ba900fc4e48f1a8f2` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/CYCLE_NORM_BOUNDS_LOOP4_20260707.md` | 是 | md | 3388 | `449809a912e66dfd4439570a40b7c7682b10b40e0a437dc2cc4e39379acb2c1c` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/BOUNDARY_GUARDS_LOOP4_20260707.md` | 是 | md | 3325 | `38e7fd9e5b57025aa5a81987b8ccddd1755a9cbef183ecd2998a2b51ee326ccb` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/ARTIFACT_MANIFEST_LOOP4_20260707.md` | 是 | md | 6222 | `bd7f04611a79d158cd12e4edb6e286fabc1db33d3a048e60b40970f37011700e` |
| `docs/infra/recovery/d707_split_loop_outputs/session4/MAIN_PRO_HANDOFF_PACKET_20260707.md` | 是 | md | 7165 | `52b6112ec82cb690bb394ebe82d8e7ca84b88ff70c2be51e9a1ddebe71457d7c` |
| `docs/infra/recovery/d707_split_loop_outputs/session4/OPEN_BLOCKERS_FOR_PRO_20260707.md` | 是 | md | 2732 | `7dcb8d97a79c33a2d3f2cbcba4ed10cd6a1a55e4b89d9c6b8011582e83c38a20` |
| `docs/infra/recovery/d707_split_loop_outputs/session4/CLAIM_DIFF_AFTER_LOOPS_20260707.md` | 是 | md | 3296 | `60dfbae789623d7c0f3fa8bde0a153b54d58a25d70a14179eb84a6074fca81de` |
| `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_A_FINITE_MATH_PROMPT_20260707.md` | 是 | md | 3131 | `995b18d9784a1d993561452ea19926ae7e7d77708ec3ea88627e8878d1e688b4` |
| `docs/infra/recovery/d707_split_loop_outputs/session4/SUBPRO_E_REDTEAM_PROMPT_20260707.md` | 是 | md | 3029 | `61df340972d7fcfed2a076a1dffe158d12d7710a605fd4b2a747d760cfb7f8b4` |
| `docs/infra/recovery/d707_split_loop_outputs/loop0/LOOP_STATUS_LOOP0_20260707.md` | 否 | md | — | 包内缺失；`REVIEW_ARTIFACT_INDEX` 声称 `d3993191822d430b25832d7c9c82ee9b0bff182efa004bbca18ba873d5abc038` |
| `docs/infra/recovery/d707_split_loop_outputs/loop3/LOOP_STATUS_LOOP3_20260707.md` | 否 | md | — | 包内缺失；`ARTIFACT_MANIFEST_LOOP3` / `REVIEW_ARTIFACT_INDEX` 声称 `d73d2a317ae96572fcd622dcd9e7e58d519238997dbb2877b3e4063ea50bda43` |
| `docs/infra/recovery/d707_split_loop_outputs/loop4/LOOP_STATUS_LOOP4_20260707.md` | 否 | md | — | 包内缺失；`ARTIFACT_MANIFEST_LOOP4` / `REVIEW_ARTIFACT_INDEX` 声称 `07a623ffb333e639b8a0ce6a8aa45632ac759daea0234633cd2afab329dd15bb` |
| `docs/infra/rag_rebuild_20260622/NODE22_VECTOR_REFRESH_D708_INTERNAL_V0_GATE_PACKAGE_20260708.md` | 否 | md | — | 包内缺失；`STATE.md` 引用 |
| `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_PACKAGE_20260708.md` | 否 | md | — | 包内缺失；`STATE.md` 引用 |
| `docs/infra/MAOFIELD_PRO_D708_INTERNAL_V0_PROMOTION_GATE_NODE19_DELIVERY_20260708.md` | 否 | md | — | 包内缺失；`STATE.md` 引用 |
| `AGENTS.md` | 否 | md | — | 包内缺失；Loop 3/4 manifest 声称已消费 |
| `CLAUDE.md` | 否 | md | — | 包内缺失；Loop 3/4 manifest 声称已消费 |

## 结论与所需补件

严格按你给出的 gate 任务执行后，我的结论不是“正文应停摆”，而是“**当前 package 不能作为闭合 promotion-gate 证据包直接过关**”。因此本次只能返回：

**`REQUEST_NODE36_FILES`**

需要补入或重新打包的最小集合很明确，而且都来自当前包**自己已经引用过**的内部文件，而非外部文献或新实验数据：三份 `LOOP_STATUS_LOOP{0,3,4}_20260707.md`；与当前上传物一致的 D708 package record、node19 delivery record、D708 RAG record，或删除 `STATE.md` 中相应引用并重写 provenance；若要维持 Loop 3/4 manifest 对环境规则的“已消费输入”说法，则还需把 `AGENTS.md`、`CLAUDE.md` 打入包，或在 manifest 中改成“包外运行环境输入，非本包证据”。同时还必须把 `STATE.md` 中的 zip 哈希、prompt 哈希、以及文件数改成与当前上传物一致的值；否则即便数学本体无误，strict internal gate 仍然会被 provenance mismatch 卡住。