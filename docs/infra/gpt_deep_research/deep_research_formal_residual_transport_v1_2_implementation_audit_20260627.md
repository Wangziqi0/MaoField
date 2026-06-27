# Formal Residual Transport v1.2 实现审计报告

## 审计范围与一页结论

本次审计严格按上传 bundle 的边界执行：只审有限维数学定义、定理文字、toy harness 结构、JSON/summary 合同与 claim gate，不把任何 synthetic pass 解释成 MaoField 经验支持；允许上限仍是 `definitions_and_harness_viable_only`，Mode B MaoField 经验状态仍必须保持 `insufficient_artifact`。prompt 还明确要求：若 GitHub connector 不可用或不明确，就继续采用 bundle-first，并把仓库二次核验标成 blocked；因此以下结论全部以上传 bundle 为证据边界。〔证据：00-README_FOR_142_AND_PRO.md:11-25；prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md:13-18,24-32,53-63；from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:75-107〕

我的一页 verdict 是：**本地 v1.2 已经把 report (28) 要求的数学补丁主体真正落地，属于有效的小补丁实现；但它仍需要一次小而明确的修订，因此不应给“完全接受”而应给“minor revision”。** 我不给 major revision，因为 registered ambient、squared-capture Beta 闭合、exact product-weight Hoeffding theorem、square-holonomy telescoping、以及 synthetic-only claim gate 这五件核心事，已经都被 note 与 harness 正面实现；我不给 outright accepted，是因为 threshold 单一真相源这一块还存在一个**实现层面的自相矛盾**：文档声称 pass/fail “only by `evaluate_test`”，但 meta-block `threshold_contract_single_source_control` 实际并未经 `evaluate_test`，而是自行计算并写入 `pass`；同时它名为 `json_threshold_contract_sha256` 的字段也不是从已写出的 JSON 重新取回，而是直接复制 runtime hash。数学核心是对的，合同设计方向也是对的，但这两个点足以阻止“严格字面意义上的完全通过”。〔证据：from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md:19-31,263-265,300-343；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:278-313,332-340；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:72-130,682-753,756-787,790-814；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-36〕

换句话说，**v1.2 不是“口号版补丁”，而是“基本数学已闭合、合同审计还差最后一刀”的补丁。** 它已经足够证明 local Codex 没有把 report (28) 整体做歪；但它还没有把 threshold meta-audit 做到我愿意称为“严格无例外单源”的程度。Mode B MaoField 经验状态则完全不变，仍然只能是 `insufficient_artifact`。〔证据：from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:19-42,75-107,109-121；from_repo/STATE.md:16,24-29,87；from_repo/GPT55_PRO_RESEARCH_INDEX_20260622.md:5-14,299-304〕

## 数学审计

### Registered ambient

v1.2 已经把“共同 ambient”从 v1.1 的警告语升级成了真正的注册定义。它先固定每个顶点的带权 Hilbert 空间 `(H_s, <.,.>_{w_s})`、source-fixed nuisance 子空间 `N_s` 与残差投影 `P_s`，然后定义 registered ambient datum 为一个有限 Hilbert 空间 `(E,<.,.>_E)` 与各残差空间到 `E` 的等距嵌入 `A_s:N_s^{\perp,w_s}\to E`，并据此定义 registered residual `Rtilde_s(K_s)=A_sP_sK_s`。更关键的是，它没有再笼统地说“这些量是不变量”，而是先给出 equivalent registration 的定义，再把 invariance 语言明确限制在“存在 ambient 间等距同构 `U` 且 `UA_s=A'_s`”这一类注册等价之下；在此之外，正确术语只能是“registration-dependent diagnostic”。这正是 prompt 要求的收口方式。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:40-108；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md:46-64；from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md:40-78〕

harness 也与这个收口方向一致。`common_ambient_registration_control` 不再假装“任何 stack/spectrum/norm 都天然可比”，而是构造一个等距注册 `registered_b = u @ residuals` 与一个非等距坏注册 `bad_registration = diag(2,1,1) @ residuals`，然后比较在等距注册下的 metric diff 与坏注册下的 metric diff。它实际检查的是一组有限 toy diagnostics——奇异值、Gram 矩阵、stack Frobenius norm——而不是完整 invariant theory，但这完全足够支持 v1.2 的有限目标：**先证明“等距注册下不变；非等距注册下不应乱说不变”。**〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:275-289,407-443；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:153-170〕

我在这一项上没有发现需要改公式的数学错误。真正要保持克制的是表述边界：该 note 已经把授权语言收紧到了 equivalent isometric registration，不再宣称完成 common-ambient invariant theory；这一点是对的，必须保留，不能再往上吹。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:98-108,317-323,338-340〕

### Random-subspace squared capture null

v1.2 已经把 v1.1 最明显的统计闭合缺口修掉了。formal note 直接把解析统计量写成
\[
Z=\|\Pi_S u\|_2^2/\|u\|_2^2,
\]
并把 Beta law 显式限制在 **先 whiten，再看 Euclidean `k`-plane**，且仅适用于 `0<k<d` 的情形；它还明确禁止把 unsquared norm ratio 当作“直接 Beta 校准”的 gate。这个 theorem 文字本身是对的，限制条件也写对了。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:110-147；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_WORKPLAN_20260626.md:65-83〕

脚本现在与 formal statistic 一致。`squared_capture()` 先做 weighted projection，再取投影范数与原向量范数之比，最后显式平方返回；`block_random_subspace_beta_squared_capture_control()` 记录的 statistic 名称也已经改成 `"squared_capture"`，并同时输出 `beta_alpha`、`beta_beta`、Monte Carlo 的 mean/variance/p95/p99，以及 heldout 在随机 `k`-平面 null 下的 quantile。对应 JSON 的 test_id 也已经换成 `random_subspace_beta_squared_capture_control`。这与 v1.1 的 `weighted_projection_energy()` 明显不同；v1.1 返回的是 unsquared norm ratio，而 JSON 却把 analytic law 写成 “Beta for squared capture after whitening”，那一版才是真闭口不严。v1.2 在这一点上已经完成补丁。〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:241-263,540-593；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:244-272；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:68-75；from_repo/scripts/debranded_residual_transport_harness_v1_1.py:237-243,540-588；from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_1_strict_audit_20260626.md:39-46,56-58〕

更细一点看，脚本的“whitening”不是口头说说，而是通过 weighted-orthonormal basis 隐式完成的：`residual_space_basis()` 先在 weighted geometry 中取 `N^\perp_w` 的基，`weighted_orthonormal_rows()` 则在乘上 `sqrt(weights)` 后做 SVD，使返回的 rows 成为 weighted-orthonormal 的 Euclidean coordinates。也就是说，formal note 所说的“先 whiten 再应用 Euclidean Beta law”，在 harness 里不是另写一个名叫 `whiten()` 的函数，而是以加权正交规范化的形式实现了。这个实现方式是合法的。〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:241-251,254-263,241-245,540-559；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:141-147〕

### Product-weight Hoeffding theorem

v1.2 note 已经把 v1.1 里只算“边界写对了、正向 theorem 还不够”的那一段补成了正面的 theorem text。它先假设 exact product weights `w(q,b)=w_Q(q)w_B(b)`，再定义带权内积、加性 nuisance `N_add={c+a(q)+b(b)}`、以及
\[
H(K)(q,b)=K(q,b)-K_Q(q)-K_B(b)+\mu.
\]
随后 Proposition 3 直接陈述 `P_{N_add}^{\perp,w}K=H(K)`，并给出 proof sketch：常数、零均值 q-only、零均值 b-only 三部分在 product weights 下正交，因此把三块投影减掉就得到 Hoeffding interaction component。这个证明草图虽然不长，但在当前 finite-dimensional 小补丁的标准下已经足够。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:149-205；from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md:105-162〕

更关键的是，边界没有被偷换。note 明写：若权重不是 exact product form，则上述正交性一般失效，此时对象只能叫 **non-product weighted projection residual**，不得继续叫 product-measure Hoeffding interaction；harness 也保留了两块与此对应的 regression：`exact_product_weight_equality_control` 证明 exact product 情况下 observed 与 product-reference 的 additive residual 一致，而 `product_reweighting_separation` 则用一个 non-product 反例把两者分开。这个“正向 theorem + 反向边界反例”的搭配是正确的。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:181-205；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:343-382；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:38-51,77-84；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:92-135〕

我在这一项上也没有发现 theorem 本身的数学错误。它做的不是一般 measure-theoretic Hoeffding decomposition，而是严格的 finite weighted product-space 命题；只要保持这个边界，它就是正确的。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:151-205〕

### Square holonomy telescoping

这是本次审计里我检查得最仔细的一项。note 把路径
\[
p:s_0\to s_1\to \cdots \to s_m
\]
上的 operator 写成
\[
M_p(J)=P_m C_m Q_{m-1} C_{m-1}\cdots Q_1 C_1 P_0,
\quad Q_i=P_i \text{ if } i\in J,\ \text{else } I,
\]
并定义 `Delta_p = Chat_p - M_p(empty)`，然后陈述
\[
\Delta_p=\sum_{i=1}^{m-1}\bigl(M_p(\{1,\dots,i\})-M_p(\{1,\dots,i-1\})\bigr).
\]
这个 telescoping 公式的 operator order 是正确的；它不是把 `(P_i-I)` 插在“前一个 map 左边”或“后一个 map 右边”随便换位，而是严格地按 path order 插入。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:207-276〕

手算长度二时，
\[
\Delta_p
= P_2C_2P_1C_1P_0 - P_2C_2C_1P_0
= P_2C_2(P_1-I)C_1P_0.
\]
这与 note 的 length-2 展开完全一致。手算长度三时，
\[
\Delta_p
= P_3C_3P_2C_2P_1C_1P_0 - P_3C_3C_2C_1P_0
\]
可按
\[
[M(\{1\})-M(\emptyset)] + [M(\{1,2\})-M(\{1\})]
\]
拆成
\[
P_3C_3C_2(P_1-I)C_1P_0
\;+\;
P_3C_3(P_2-I)C_2P_1C_1P_0.
\]
这里第一项对应“先插入 `P_1`”，第二项对应“在已经插入 `P_1` 的前提下再插入 `P_2`”。如果把第二项误写成 `P_3C_3(P_2-I)C_2C_1P_0`，那才是 index/order 错误；但当前 note 没犯这个错。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:238-276〕

脚本的 `path_product()` 与上述公式逐字匹配：初始化为 `P_0`，每过一条边先右乘对应 transport map `C_i`，只在 `i` 属于 internal mask 时插入内部投影 `P_i`，并在终点总是插入 `P_m`。`block_square_holonomy_telescoping_control()` 再用 `path_product(projectors, maps, set(range(1, i+1)))` 逐步构造 telescoping summands，并检查 `defect = sum(terms)` 以及 `Omega = raw_diff + defect_p - defect_q` 的 square identity。operator order 与 note 完全一致，我没有发现需要修正的 index/order bug。〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:329-340,596-643；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:275-290〕

## Harness 审计

先说通过的部分。v1.2 note、script、summary、JSON 的 test names 是一致的，且 block 数量一致为 12 个：`FORMAL_NOTE_V1_2_20260627.md` 给出的 v1.2 blocks 列表，与 `make_metric_blocks()` 的调用顺序、summary 的 block 列表、以及 JSON 的 `blocks[].test_id` 顺序相互对齐。这说明本地实现没有出现“文档叫 A、脚本跑 B、JSON 写 C”的命名漂移。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:295-309；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:666-679；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:38-51；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:89-320；from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:67-73〕

再说 JSON 充分性。top-level JSON 已经包含 schema、seed、draws、environment、evidence boundary、`threshold_contract`、`threshold_contract_sha256`、每个 block 的 metrics、per-block threshold snapshot、per-block `threshold_contract_hash`、per-block `pass`，以及 allowed/forbidden interpretation。**就“复核本地 stated verdict”而言，这已经足够，不需要读取隐藏 scratch state。** 也就是说，你不必访问 node36 临时目录里的隐藏中间变量，单看 JSON 就能知道：跑了哪 12 块、阈值合同是什么、每块是否过线、最强允许 verdict 是什么、哪些解释仍被禁止。〔证据：from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:1-324；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:24-36,38-75,77-101〕

真正的问题出在 threshold single-source 这块的**字面严格性**。note 把 contract rule 写成：“`build_threshold_contract()` 是单一阈值源；block functions 只算 metrics；`evaluate_test()` 负责 pass/fail；JSON 序列化同一合同；`threshold_contract_single_source_control` 验证 per-test threshold equality 与 contract hash equality。” summary 甚至更强地写成 “pass/fail is assigned only by `evaluate_test`”。但 script 的真实结构是：前 11 个 metric blocks 先经过 `evaluate_test()`，之后再**额外 append** 一个 `block_threshold_contract_single_source_control(evaluated, contract)`；这个 meta-block 自己在函数内部计算 `passed`、自己写入 `thresholds`、`threshold_contract_hash` 和 `pass`，并没有经过 `evaluate_test()`。因此，“所有 pass/fail 都只由 `evaluate_test()` 指派”这句话在严格字面上是假的。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:286-293；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-36；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:682-753,756-787,790-794〕

第二个更细的缺口是：`threshold_contract_single_source_control` 里的 `json_threshold_contract_sha256` 并不是从已经写出的 JSON 文件重新读回来的 hash，而是直接把 runtime `contract_hash` 复制一份。因此它当然能与 `runtime_threshold_contract_sha256` 相等，但这并不是一个独立的“序列化后文件一致性”检查；它只是一个 in-memory 一致性断言。由于 `build_result()` top-level 也同样把 `threshold_contract` 与 `threshold_contract_sha256 = sha256_json(contract)` 放进返回对象，所以当前实现**按构造**会把同一合同写进 JSON，但 meta-control 的命名和说明比它实际做到的事情更强。严格说，它是 meaningful 的，但还不是完全独立的 file-level verifier。〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:760-787,790-814；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:31-88,306-320；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-36〕

因此，我对 harness 的结论是：**整体设计方向正确，threshold contract 基本已经成为单源；但“central evaluator absolutely唯一”“JSON hash 已被独立验证”这两句仍不够严格，属于 minor revision 级缺口，而不是 major defect。**〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:278-313；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:72-130,682-814；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-36〕

## 仍须禁止或降级的说法

v1.2 之后，以下表述仍然必须继续判死，不能因为 12 个 synthetic blocks 全 pass 就偷偷升级：

- **不得说 completed formal system。** v1.2 自己只允许 `v1_2_small_patch_feasible`，并反复说明这不是 completed formal system。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:332-340；from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:19-21,89-107〕
- **不得说 full panel 已跑，或 16-cell full-panel aggregate 已存在。**〔证据：00-README_FOR_142_AND_PRO.md:11-19；prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md:53-60；from_repo/STATE.md:16,24-29〕
- **不得说 MaoField residual / interaction / quotient-residual / transport / holonomy field 已观测到。**〔证据：00-README_FOR_142_AND_PRO.md:14-18；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:317-330；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:12-28,323-324〕
- **不得说 glass-box broken、F3 positive、LOSO passed。**〔证据：prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md:55-60,103-104；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:86-101〕
- **不得说 checkpoint loading、model inference、training、new loss 已授权。**〔证据：00-README_FOR_142_AND_PRO.md:14-18；from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:89-107；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:323-324〕
- **不得把 common-ambient 语言升级成“完整 invariant theory 已完成”。** 当前只授权“equivalent registration 下的不变性”。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:87-108,317-323〕
- **不得把 random-subspace null 升级成 absolute structure detector。** 该 null 只是 whitened residual space 里的 squared-capture analytic/MCMC 对照。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:141-147,319-320〕
- **不得把 product-weight theorem 扩张到 non-product weights。** 非 product 权重仍只允许叫 non-product weighted projection residual。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:202-205,321-322〕
- **不得把 square holonomy telescoping 说成 sheaf obstruction theory 或 curvature theorem。** note 明确禁止。〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:274-276,322-323〕

## 最小修补建议

我不建议重写项目；当前工件明显不是“逻辑不可救”。需要的只是最小 edit set。

第一，把 `threshold_contract_single_source_control` 也纳入 `evaluate_test()` 的统一 pass/fail 路径。最小做法有两种，二选一即可。要么给 `evaluate_test()` 加一个 `elif test_id == "threshold_contract_single_source_control"` 分支，让 meta-block 只产出 metrics，不自算 `pass`；要么修改文档措辞，把 “pass/fail is assigned only by `evaluate_test`” 收紧成 “all non-meta test blocks are assigned by `evaluate_test`”。如果想保留“strict single evaluator”的口径，前一种更干净。〔证据：from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:30-36；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:682-753,756-787,790-794〕

第二，把 `json_threshold_contract_sha256` 变成一个**真实的 JSON-side 值**，而不是 runtime hash 的镜像副本。最小做法是：在构造完整 `result` 后，对 `result["threshold_contract"]` 与 `result["threshold_contract_sha256"]` 做一次独立一致性检查；如果想更严格，就在写盘后重新读回 JSON 文件，再核验 serialized contract 的 hash。当前名字叫 `json_threshold_contract_sha256`，但实现上只是 `contract_hash` 的第二个别名；这个命名应当被补齐为真实检查，或者至少改名避免误导。〔证据：from_repo/scripts/debranded_residual_transport_harness_v1_2.py:760-787,808-809；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:306-320〕

第三，其余数学部分不要再大动。registered ambient、squared-capture Beta law、product-weight theorem、square-holonomy telescoping 这四块没有发现需要推翻的错误；如果为了修上面两个 harness 合同问题去改动数学正文，那反而是过度施工。当前最优策略就是：**只修合同元件，不重写数学主体。**〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:40-276；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:241-263,329-340,343-382,407-443,540-643〕

## 通俗解释与最终分类

如果用初中生能听懂的话说：这次补丁主要做了两件老老实实的事。第一，它先把“大家到底在同一个坐标系里比什么”写清楚了，不再没注册 ambient 就乱谈不变量；第二，它把“随机对照到底比什么统计量”“什么时候才能说是 product-weight 的 Hoeffding 交互”“绕路径一圈的差异到底怎么拆出来”这些最容易糊弄人的地方写成了明确规则。也就是说，**这个数学对象现在比 v1.1 诚实得多，也更像一个真正能审计的有限维线性代数对象。**〔证据：from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:40-147,149-276；from_repo/docs/infra/gpt_deep_research/deep_research_formal_residual_transport_v1_2_minimal_patch_20260627.md:339-343〕

但它仍然**什么也没有证明到 MaoField 经验层面**。原因很简单：这里跑的是 synthetic harness，不是 MaoField 数据；没有 full panel，没有 checkpoint loading，没有 inference，没有 training，没有 new loss，也没有任何 observed field。换句话说，这次补丁修的是“数学讲义与 toy audit contract”，不是“真实世界证据”。这一条必须继续钉死。〔证据：00-README_FOR_142_AND_PRO.md:11-25；from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_2_20260627.md:5-22,77-101；from_repo/docs/infra/debranded_residual_transport/synthetic_harness_v1_2_20260627.json:12-28,323-324；from_repo/STATE.md:24-29〕

最终分类我给：

**formal_v1_2_patch_requires_minor_revision**〔证据：prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md:129-138；from_repo/scripts/debranded_residual_transport_harness_v1_2.py:682-814；from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_2_20260627.md:278-340〕

并且无论这个分类如何，Mode B MaoField empirical status 都必须保持：

**insufficient_artifact**〔证据：00-README_FOR_142_AND_PRO.md:15-19；prompt/GPT55_PRO_FOUNDATIONAL_RESIDUAL_TRANSPORT_V1_2_IMPLEMENTATION_AUDIT_PROMPT_20260627.md:24-32；from_repo/docs/infra/gpt_deep_research/FORMAL_RESIDUAL_TRANSPORT_V1_2_MINIMAL_PATCH_ADOPTION_NOTE_20260627.md:75-87；from_repo/STATE.md:24-29〕