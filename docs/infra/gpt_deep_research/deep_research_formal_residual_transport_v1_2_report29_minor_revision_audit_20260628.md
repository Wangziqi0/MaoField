# Formal v1.2 Report 29 Minor Revision Audit

## 审计范围与证据边界

本次审计严格按上传 bundle 的读序进行，审查对象是 **report (29) 所要求的阈值合同小修是否已经在本地实现闭合**，而不是重新设计 Formal v1.2，也不是为 MaoField 做经验性“翻案”。bundle 自带提示词明确限定：这是一次狭义 implementation audit；证据边界仍然是 Mode A 有限维 synthetic harness；不允许把它上升为 full panel、训练、新 loss、观测到 MaoField field、或 completed formal system 的结论。`00-README` 与主提示词对这一点写得很死。

仓库二次校验方面，bundle 允许在 **GitHub connector 可用** 时仅把私仓 `Wangziqi0/MaoField` 作为次级核验来源；本会话中并无可用的 GitHub 仓库连接器，因此我没有把任何公开 GitHub 页面、raw 链接、搜索摘要、或 404 页面当成私仓证据。本报告的实质证据全部来自用户上传的审计 bundle，与提示词要求一致。

## 一页结论

结论先行：**report (29) 要求的那两个 implementation-level minor revision 已经在本地闭合。** 旧的 implementation audit adoption note 明确记录：先前被采纳的结论是“需要 minor revision”，而且缺口只限于两点——`threshold_contract_single_source_control` 不能在 `evaluate_test()` 之外自行给出最终 `pass/fail`，以及 `json_threshold_contract_sha256` 不能只是 runtime mirror、必须来自真实写盘 JSON 的 readback。adoption note 同时声称 node36 已按这两个点做了最小修补。`STATE.md` 也同步记录了同一件事。

我审完脚本、summary、JSON 后的判断是：**这次小修已经达到关闭 report (29) minor revision 的要求**。原因很具体，不靠口号。第一，meta-block 现在确实只产出 metrics，不再自己写 `pass`。第二，最终 JSON 中的 `json_threshold_contract_source` 也确实是 `readback_from_written_json_threshold_contract`，而且 `json_threshold_contract_sha256` 与写盘 JSON 中 `threshold_contract` 的哈希一致。第三，所有 evaluated blocks 的合同来源、阈值快照和中央 evaluator 路径在实现逻辑上已经收束到同一条通道。

因此，我的审计 verdict 是：**本地 report (29) minor revision 已关闭；没有剩余的阻断性 minor issue；实现分类可以从“上次 implementation audit 的待修状态”上调为“minor revision 修补后接受”。** 但这里的“接受”只是在 **本地 synthetic harness contract consistency** 这一窄范围内成立；最强本地结论仍然只能是 `definitions_and_harness_viable_only`，Mode B MaoField empirical status 仍然必须是 `insufficient_artifact`。

## Harness 实现审计

这次修补最关键的地方，在 `scripts/debranded_residual_transport_harness_v1_2.py` 里已经改对了。`build_threshold_contract()` 仍然是单一阈值源；其中 `threshold_contract_single_source_control` 也有自己的合同项，要求合同哈希匹配、per-test threshold 匹配、以及 central evaluator 真正参与。换言之，合同规则的源头没有分叉。

中央 evaluator 路径也已经闭合。`evaluate_test()` 现在有专门的 `elif test_id == "threshold_contract_single_source_control"` 分支；这个分支读取 meta-block metrics，再统一按合同计算 `passed`。更关键的是，`evaluate_test()` 在返回时统一把 `thresholds`、`threshold_contract_hash`、`evaluated_by="evaluate_test"` 和最终 `pass` 写回输出对象。也就是说，最终的 pass/fail 归属已经落回中央 evaluator，而不是落在 meta-block 自己手里。

与此配套，`block_threshold_contract_single_source_control(...)` 现在确实只负责**收集证据**，不负责**宣布结果**。它做的事情是：遍历已评估 blocks，检查每个 block 的 `thresholds` 是否与合同一致、`threshold_contract_hash` 是否一致，然后组装一个只含 metrics 的 meta-block，其中包括 `runtime_threshold_contract_sha256`、`json_threshold_contract_sha256`、`json_threshold_contract_source`、`per_test_threshold_mismatches`、`central_evaluator_used` 等字段。它不写 `pass`，也不自己写最终 `thresholds/evaluated_by`。这正是 report (29) 要求的那一刀。

`build_result()` 进一步把这个闭环落地：前 11 个普通 blocks 先经 `evaluate_test()`；然后构造 meta metrics；接着把 meta metrics **再次送入 `evaluate_test()`**；只有这个统一后的 `evaluated` 列表才被写入最终 JSON。这个路径不再留“旁路”。

JSON readback 修补也已经做实。脚本先构造一个 bootstrap draft，把 runtime 合同哈希暂写进去；写盘后调用 `readback_threshold_contract_sha256(path)`，从**真实写出的 JSON 文件**重新读取 `threshold_contract` 并计算哈希；再用这个 readback hash 第二次构造正式 `result`，把 `json_threshold_contract_source` 标成 `readback_from_written_json_threshold_contract`；最后再次写盘，并且在退出前比较 `final_readback_hash` 与 `result["threshold_contract_sha256"]`，不一致就返回失败。这个实现已经不再是“runtime hash 换个名字”。

归档 summary 和归档 JSON 与这条实现路径是一致的。summary 直接写明：`pass/fail` 只由 `evaluate_test` 指派；所有 thresholds 来自 `build_threshold_contract`；JSON-side threshold hash 是从 written JSON artifact read back 得到的；且 `threshold_contract_single_source_control` 最终为 pass。归档 JSON 则记录了同一个顶层 `threshold_contract_sha256`，meta-block 中 `runtime_threshold_contract_sha256` 与 `json_threshold_contract_sha256` 相等，`json_threshold_contract_source` 为 `readback_from_written_json_threshold_contract`，`per_test_threshold_mismatches` 为空数组，`central_evaluator_used` 为 `true`，meta-block 的 `evaluated_by` 也是 `evaluate_test`。

关于“JSON reproducibility”这一点，我的严格表述是：**它现在足以复现本地 verdict 所需的合同、通过状态与边界信息，但没有承诺跨环境字节级完全同一。** 理由也不复杂：脚本把 `created_utc` 和 `environment` 写入 JSON，因此 artifact 本身是带时间和环境元数据的；它证明的是“合同与 verdict 可由 JSON 直接读出”，不是“任意重跑必得逐字节同一文件”。这不是 report (29) 所指向的阻断缺陷，但如果以后想把“reproducibility”说得更强，需要额外收紧措辞。

## 数学核心与回归审计

这次小修没有碰坏数学核心。implementation audit adoption note 明文写着：此前 report (29) 已接受的核心，是 **registered ambient**、**squared-capture random-subspace Beta statistic**、**exact product-weight Hoeffding theorem**、以及 **square-holonomy telescoping**；当前 minor revision 只针对 threshold-contract meta-audit。`STATE.md` 也把这点重复写了一遍。

Formal note v1.2 内部，这四块核心仍然在原位而且定义完整。注册 ambient 的部分保留了 “先注册、后谈 invariants” 的结构；随机子空间部分明确把 Beta 校准对象限定为 **squared capture**；product-weight 部分保留了 exact product weights 下的 Hoeffding residual 命题，并把 non-product weights 明确降格为 boundary；square holonomy 部分保留了 per-edge telescoping 公式与 operator order。它们都没有因为这次 threshold-contract 修补而改坏。

更直接地说，Formal note 的 harness contract 条款已经和修后的脚本完全对齐：单一阈值源是 `build_threshold_contract()`；block functions 只算 metrics；`evaluate_test()` 统一赋 pass/fail，包括 `threshold_contract_single_source_control`；JSON 序列化同一合同和其 hash；meta-block 检查 per-test threshold equality、central-evaluator usage 与 JSON readback hash。这个条款现在不再是文档口号，而是脚本行为。

claim gate 也没有回归。Formal note、summary、JSON、README 都仍然把解释上限锁在 synthetic-only / finite-dimensional design review：没有 full panel、没有 observed MaoField field、没有 glass-box broken、没有 F3/LOSO 正向结论、没有 training、没有 new loss、没有 completed formal system。归档 JSON 甚至把 blocked claims 直接内嵌为 evidence boundary 字段。也就是说，这次修补没有偷偷把“合同修好”偷换成“经验结论升级”。

## 禁止语句与最小建议

这次修补完成后，以下说法仍然必须杀掉或降级，不能借 repaired harness 偷越边界：

- 说 **completed formal system**。
- 说 **full panel has run** 或 **16-cell full-panel aggregate exists**。
- 说已经观察到 **MaoField residual / interaction / quotient-residual / transport / holonomy field**。
- 说 **glass-box broken**、**LOSO passed**、或 **F3 positive**。
- 说 **checkpoint loading / inference / training / new loss** 已被授权。

就 report (29) 所点名的缺口而言，我**不要求再做任何阻断性 patch**。需要继续修改的，不是逻辑闭环本身，而最多只是文案卫生：如果维护者未来想把“JSON reproducibility”说得更强，最小编辑集只需在 summary 或 note 里补一句——当前 JSON 足以复述本地 verdict 与 threshold contract，但由于文件内含 `created_utc` 与 `environment`，它并不承诺跨环境字节级恒等。这是可选优化，不构成继续挂起这次 minor revision 的理由。

## 初中生解释

这次修的不是“数学本身”，而是“裁判规则到底是不是同一个人来判”。以前的问题是：前面 11 个测试都让 `evaluate_test()` 当裁判，但最后那个检查“阈值合同有没有前后一致”的 meta-test，却偷偷自己给自己判了 `pass`。这会让文档里“所有 pass/fail 都由中央裁判统一给出”这句话变成假的。现在脚本把这个 meta-test 也交回给 `evaluate_test()` 统一处理，所以规则和实现终于对上了。

第二个修点是：以前 JSON 里的那个“JSON 阈值合同哈希”，其实只是运行时哈希再抄一遍，名字比内容更强。现在脚本会先把 JSON 写出来，再把文件读回去，重新从写盘后的 `threshold_contract` 计算哈希，然后把这个 readback hash 写进最终结果里。这样“JSON 侧哈希”才真的是 **从 JSON 文件里读回来的**，不是内存里的自说自话。

但这仍然**完全不能**说明 MaoField 在经验上成立。原因是 bundle 从头到尾都在说：这只是 zero-GPU synthetic harness；没有 full panel，没有训练，没有 checkpoint inference，没有 observed field；最强也只是“定义和 harness 在本地能自洽”。所以，这次修好的是“本地规则执行更诚实了”，不是“现实世界里已经测到 MaoField 了”。

## 最终分类

```text
formal_v1_2_patch_accepted_after_minor_revision
```

Mode B MaoField empirical status 仍然必须保持为 `insufficient_artifact`。