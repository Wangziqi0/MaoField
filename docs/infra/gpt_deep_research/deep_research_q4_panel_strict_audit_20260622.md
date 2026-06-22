# MaoField q4 Panel 严格审计报告

## Bundle Access Report

我**直接检查并解压了上传的 zip bundle**，并且只以 bundle 内部文件与原始 `raw_wip` 内容作为审计证据。`README_FOR_PRO.md` 明确要求本次审查**不得依赖 GitHub、公开网页或其他外部路径**，而应直接审 bundle 内文件；它同时把主问题限定为：是否应从“q4 locked schema + manifest-only / one-checkpoint-smoke”推进到“full 50-checkpoint q4 panel generation”。〔README_FOR_PRO.md:3-5, 23-35, 37-61〕

我读取了你指定的全部必读文件：`README_FOR_PRO.md`、`COMMIT.txt`、`SHA256SUMS.txt`、`repo_files/STATE.md`、`repo_files/MD_CATALOG.md`、`repo_files/docs/infra/math_turn_20260622/` 下的五份审计/协调/预注册/运行说明文件与 schema JSON、`repo_files/scripts/build_panel_schema_20260622.py`、`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_ppl_run.py`、`highorder_raw_logprob_panel.py`、`panel_primary_20260622/` 下三份 manifest/aggregate JSON、`repo_files/scripts/math_turn_loso_audit.py`，以及可选原始文件 `raw_wip/smoke_seed1_generation0_token_panel.jsonl`。这些文件正是 README 指定的审计范围。〔README_FOR_PRO.md:37-61〕

**校验结果分成两层：**
一层是**bundle 完整性**：`SHA256SUMS.txt` 列出了 18 个 bundle 内文件的 sha256；我对这些文件逐一重算，未发现任何文件级 checksum 不一致。另一层是**提交来源一致性**：`README_FOR_PRO.md` 与 `COMMIT.txt` 都把 bundle 指向期望提交 `a98b59fe5e35c64e3555a30d309b6bd3a5e298aa`，但 bundle 内两份生成结果 manifest 自己记录的 `repo_head` 却分别是 `16a09d4...` 与 `6a189f1...`，并且都显示当时仓库是 `ahead` 状态；协调文件的 dispatch HEAD 又是 `47a9119...`。这说明**文件内容的 checksum 是自洽的，但生成物 provenance 不是单一 clean HEAD**，存在“bundle 所属提交”和“生成时 repo_head”不一致的问题。对数学结论这不是直接正证伪，但对 full panel 的可追溯性是实质性瑕疵。〔SHA256SUMS.txt:1-18; README_FOR_PRO.md:7-12; COMMIT.txt:1; PANEL_PRIMARY_ARTIFACT_COORDINATION_20260622.md:12-18; manifest_only_20260622.json:4-8; one_checkpoint_smoke_seed1_gen0_manifest.json:4-8〕

当前**正式项目边界**没有变化：`STATE.md` 把数学转向继续标为 `blocked-until-gated`，并明确说当前 aggregate audit verdict 仍是 `insufficient_artifact`；`MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md` 也把最终 verdict 写成 `insufficient_artifact`，并阻断 “LOSO passed / mean-null vector field survives / glass box broken / F3 positive”。`MD_CATALOG.md` 还把 q4 schema/runbook lock、manifest-only 与 one-checkpoint smoke 归类为“当前实验收敛 + 数学转向 gate”，没有把它们升级成已通过的 primary artifact。〔STATE.md:16-17, 24-27; MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:5, 40-49; MD_CATALOG.md:29-32〕

## Must Fix Before Full Panel

**第一，最硬的 blocker 不是数学，而是实现事实：当前 generator 根本没有 full 50-checkpoint mode。** `highorder_raw_logprob_panel.py` 开头就写明它“故意保持狭窄”，只支持 `manifest-only` 与 `one-checkpoint-smoke`，并明确说 **“full 50-checkpoint panel generation is not implemented here”**；参数解析也只允许这两个模式二选一，`main()` 只走 manifest 或 one-checkpoint smoke 两条路径。你不能把“full panel 还没实现”的 bundle，当成“可批准 full panel 运行”的 bundle。〔highorder_raw_logprob_panel.py:2-10, 425-460〕

**第二，manifest 没有完全满足 locked runbook 自己要求的 provenance 字段。** Runbook 明确要求每个生成的 manifest 必须包含 `builder_script_sha256`、`schema_sha256`、`source_split=train`、三类 source hashes、checkpoint root、seed/generation 范围、device/dtype，以及 `no_training=true` 和 `no_new_loss=true`。现有两个 manifest 虽然包含 `schema_sha256`、`source_split`、source hashes、checkpoint root、device/dtype 与 no-training/no-new-loss 边界，但**缺了 `builder_script_sha256`**。这会让未来 full panel 无法严格证明“你生成 panel 的代码，就是 runbook 锁定的那份代码”。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:154-173; manifest_only_20260622.json:1-75; one_checkpoint_smoke_seed1_gen0_manifest.json:1-122〕

**第三，提交 provenance 必须清洗。** 当前 bundle 的 `COMMIT.txt` 指向 `a98b59f...`，但两份 manifest 的 `repo_head` 都不是它，而且都记录了 dirty/ahead 状态。这不是“文件坏了”，但它会在 full panel 时制造一个严重问题：审稿人无法清晰回答“full panel 是在哪个 exact HEAD、哪份 exact generator、哪份 exact schema 下跑的”。full panel 之前，必须在**单一 clean commit** 上重跑 manifest-only 与 smoke，或者至少把“bundle commit、artifact generation commit、builder script hash”全部并列写入 manifest。〔COMMIT.txt:1; manifest_only_20260622.json:4-8; one_checkpoint_smoke_seed1_gen0_manifest.json:4-8〕

**第四，必须先补“失败即中止”的负控 smoke，而不是只做一个成功 smoke。** 现在 bundle 只证明了：在 `seed=1, generation=0`、CPU fp32、q4 locked schema 下，generator 能重载 train audit blocks、校验 source/schema hashes、写出 raw JSONL 与 q4 aggregate，并把旧 aggregate 行逐字段复现为零差。它没有证明：篡改 schema hash 会中止、篡改 target hash 会中止、错误 split 标注会中止、错误 q4 边界会中止，也没有证明多 checkpoint 循环不会出现路径枚举或 checkpoint 缺失问题。one-checkpoint smoke 的作用被文档自己限定为“generator alignment”，不是“scientific signal”。〔PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:8-15, 16-25, 71-103, 123-142; highorder_raw_logprob_panel.py:89-131, 281-324, 372-418〕

**第五，full panel 解释脚本尚未实现，所以 fold-local 约束仍停留在纸面。** 预注册草案和 locked runbook 都要求：LOSO、matched-mean pairing、projection fitting、residualization 必须在 held-out seed 的 fold 内局部拟合，并且 mean-only synthetic controls 与 rank-1 synthetic controls 不得通过完整 gate stack。但 bundle 里现成的 `math_turn_loso_audit.py` 只处理旧 aggregate 的三项指标；它确实做了 LOSO 的 CV-R2，但 matched-mean 是在全体行上两两配对，不是 fold-local；rank/residual 也只是对两切片 aggregate 做 diagnostic placeholder，而不是 q4 full panel analysis。full panel 前，必须把**分析脚本**和**生成脚本**分开，并先把 full-panel 分析实现好。〔PANEL_PRIMARY_ARTIFACT_PREREG_DRAFT_20260622.md:128-175; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:206-277; math_turn_loso_audit.py:91-158, 161-227, 323-345〕

**第六，旧脚本的措辞污染还没清干净。** `highorder_ppl_run.py` 的说明和变量注释仍写着 “fixed true wikitext eval” 和 “eval target token frequency”，但它实际加载的是 `raw["train"]` 的前 128 个 blocks；runbook 已经把这种误称明确定义为 `invalid_artifact`。同样，`math_turn_loso_audit.py` 的 verdict 代码里仍保留了 `survive` 这一输出词，而 runbook 后来把允许词表收紧成 `invalid_artifact / killed / insufficient_artifact / eligible_for_next_design_review_only`。这些不是文字吹毛求疵；它们会直接导致后续 claim 泄漏。〔highorder_ppl_run.py:5-10, 57-76; PANEL_PRIMARY_ARTIFACT_COORDINATION_20260622.md:89-95; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:68-69, 281-307; math_turn_loso_audit.py:190-227〕

## Full Panel Decision

我选择：**3. Do not approve full panel; require additional smoke/negative controls.**

理由非常直接，而且是 bundle 内证据足够支撑的。现有证据最多只说明：q4 schema 已被锁定；q8 的 empty-bin 处理是诚实的；manifest-only 与 one-checkpoint smoke 证明了**单 checkpoint 生成器与既有 aggregate 计算在一个点上对齐**。但这距离“批准 full 50-checkpoint q4 panel generation”仍差三步：**没有 full mode 实现、没有 fail-fast 负控 smoke、没有 full-panel gate analysis 实现**。因此现在不能批准 full panel 运行。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:314-330; highorder_raw_logprob_panel.py:4-10, 425-460; PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:123-142〕

如果必须给出**当前最强允许表述**，它也只能是：**当前 generator 与 q4 locked schema 最多只具备进入 full-panel generation review 的资格，不具备直接开跑 full panel 的资格**。这与 README 允许的最强结论是一致的，也与 runbook 自己的边界一致。〔README_FOR_PRO.md:130-136; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:301-307〕

## Claim Boundary

以下 claim **全部仍然 blocked**，而且 bundle 内证据并不足以解除它们：

- **`LOSO passed` 仍然 blocked。** 旧 aggregate audit 的最终 verdict 仍是 `insufficient_artifact`；新 q4 面板还没生成，更没有完成 q4 的 fold-local LOSO 审计。〔MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:5, 42-49; STATE.md:27〕
- **`F3 positive` 仍然 blocked。** 现有正式边界只允许 “F3 weak exception / worth pursuing / not positive”；旧 audit 也只允许 “at most a weak F3 lead”。〔STATE.md:16, 24, 27; MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:42-49〕
- **`mean-null vector field survives` 仍然 blocked。** 旧 audit 明说当前 artifact 只有 rare/freq 两切片 aggregate，不能认证固定的 `J>=4` mean-null vector field；新 q4 panel 还没完成。〔MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:32-39, 45-49; math_turn_loso_audit.py:161-187〕
- **`glass box broken` 仍然 blocked。** `STATE.md` 明说当前方法尚未打破 glass box；runbook 也把这列为 forbidden wording。〔STATE.md:16, 24, 27; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:290-310〕
- **`training authorized` 与 `new loss authorized` 仍然 blocked。** README、runbook、smoke record 和 generator 脚本都明确禁止训练、backward、optimizer step、新 loss 与 text generation。〔README_FOR_PRO.md:29-30, 80-85, 117-136; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:19-20, 309-310; PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:24-25, 123-136; highorder_raw_logprob_panel.py:4-10〕
- **把 `source_split=train` 说成 validation/test/eval 的任何表述，都应视为 blocked 或 invalid。** 新 runbook 已经把这点写成刚性规则，但旧 aggregate generator 仍留有误称。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:48-69, 179-189; highorder_ppl_run.py:5-10, 57-76〕

## Mathematical Objections

**关于 q4 是否仍有 post-hoc slicing 或隐藏 multiplicity：**
相对于 checkpoint outcomes，q4 的 binning 现在基本是**outcome-blind** 的：它只依赖 fixed audit blocks 上的 target token counts，schema JSON 把 block indices、tokenizer、三类 source hashes、quantile method、tie policy、edge inclusivity 与 empty-bin policy 都写死了；generator 也会复算并核对这些 hash 与 bin sizes。就这一点说，q4 比旧 F3 rare/freq top-bottom 20% 干净得多。〔panel_schema_freq_q4_audit_targets_20260622.json:11-15, 147-152, 9056-9090, 9136-9153; build_panel_schema_20260622.py:65-109, 111-167; highorder_raw_logprob_panel.py:89-131〕
但它**仍不是 clean confirmatory prereg**。预注册草案自己承认这是 “exploration-aware prospective lock”；q4 之所以是 primary、q8 之所以降为 sensitivity，是在看到数据离散度和 q8 空 bin 之后做出的制度化收缩。因此 multiplicity 不是完全消失，而是被压缩到一个“唯一 primary q4 slope projection + 其他全 sensitivity-only”的框架里。对“是否可以生成面板”来说，这足够谨慎；对“是否可以宣称强结论”来说，仍远远不够。〔PANEL_PRIMARY_ARTIFACT_PREREG_DRAFT_20260622.md:42-79; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:267-307〕

**关于 q4 ordered frequency-slope projection 是否太任意：**
是的，**它在数学上具有明确任意性**。runbook 把唯一 primary scalar 定义为对四个 q4 bin 的有序斜率投影：`v_raw = [-1.5,-0.5,0.5,1.5]`，再做 weighted centering 与 unit normalization，最后以 `P = sum_j w_j v_j u_j` 聚合。这个选择并不是从模型、数据生成机制或独立理论中推出的；它本质上是“沿频率分位顺序的单调对比”这一研究者设定。它会天然偏好**单调低频到高频的线性/准线性偏移**，却对 U-shape、端点效应、局部凸性或非单峰结构不敏感。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:91-102; highorder_raw_logprob_panel.py:210-225〕
不过，我不会把这种任意性夸大成“因此不能生成 full panel”。它的正确结论是：**这个投影足以作为一个被锁定的 primary diagnostic carrier，但不足以支撑强科学 claim。** 也正因为它任意，所以 runbook 正确地把“任何其他投影都不能触发 strongest verdict”写死了。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:91-102, 267-307〕

**关于 q8 empty-bin handling 是否诚实：**
这一点我认为是**诚实且合格的**。schema builder 对 q8 采用同样的 preregistered quantile method `nearest` 与 assignment policy `np.searchsorted(..., side='right')`；在固定 audit frequencies 上，确实得到 `edges = [1,2,5,10,39,73,238]`，并出现 `bin_sizes[0] = 0`。bundle 没有把它偷偷修补成非空，也没有把 q8 继续包装成 primary；相反，runbook 和 schema JSON 都明确写成 `not_locked_empty_bin`，并要求“不得在看到这个事实后再修”。这是审计上正确的处理。〔build_panel_schema_20260622.py:46-62, 81-84, 126-135; panel_schema_freq_q4_audit_targets_20260622.json:9092-9133; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:104-119〕

**关于 pseudo-replication：**
这个漏洞**并没有因为未来有 50 行 panel 就消失**。runbook 自己已经诚实承认：5 个 seed × 10 个 generation 的 50 个 seed-generation rows 不是 50 个独立样本，而是同一 checkpoint root、同一 base-reset regime 下的 within-regime seed trajectories。也因此，LOSO 在这里只能算“within-regime seed-held-out diagnostic”，不能被表述成 independent replication。任何未来摘要如果把 50 行说成 N=50 的独立证据，都是统计学错误。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:121-136, 206-218, 273-277; PANEL_PRIMARY_ARTIFACT_COORDINATION_20260622.md:181-190〕

**关于 nuisance leakage 与 fold-local 要求：**
这里我坚持强硬：**residualization、matched-mean pairing、projection fitting 都必须 fold-local。** 这个要求在 prereg 草案和 runbook 中都已写明，而且是正确的；如果未来 full-panel analysis 在 held-out seed 外先看了全局 panel 再定 pairing/projection/threshold，那就会把 leakage 直接写进 primary result。当前 bundle 只有条文，没有 full-panel analysis 实现，所以这仍是未完成工作，而不是已解决问题。〔PANEL_PRIMARY_ARTIFACT_PREREG_DRAFT_20260622.md:128-148; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:220-247〕

**关于 rank-1 shadow 与 noise floor：**
runbook 已经比旧版严谨得多：它锁了 `sigma2_over_sigma1_min = 0.25`，把 residual amplitude floor 定义为 `2 * max(noise_floor_seed_bootstrap_p90, noise_floor_rank1_control_p90)`，并写了 bootstrap replicates 与 RNG seed。单从 preregistration 角度看，这比“以后再看”要好得多。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:249-264〕
但我仍然不把它当成“已足够”。原因有二：第一，**负控实现不在 bundle 中**，mean-only synthetic controls 与 rank-1 synthetic controls 还只停留在 runbook 文字；第二，阈值虽然注册了，但还没有在真实 q4 panel 分析代码里跑通。因此我的结论是：**门槛定义已经开始合格，但门槛执行尚未合格。**〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:234-247, 249-264〕

**关于 one-checkpoint smoke 与 zero-diff reproduction 的含义：**
这一步的含义必须严格缩窄：它只证明**单 checkpoint 下 generator 与旧 aggregate 计算的一致性**，而不是任何“科学信号成立”。smoke record 自己已经写得很清楚：它只验证 fixed train blocks、schema/source hash、一个 CPU fp32 checkpoint、raw token rows 写出，以及旧 aggregate 行的逐字段复现；它明确否认 full panel 已生成，也否认任何训练或新 loss 授权。seed1/gen0 的 six-field absolute diffs 全为 0，这很好，但只是**代码对齐 smoke**，不是“F3 survives”的证据。〔PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:8-25, 71-103, 123-142; one_checkpoint_smoke_seed1_gen0_manifest.json:83-120〕

## Instructions Back To Codex

先改代码，再跑更多 smoke；**不要**先跑 full 50-checkpoint panel。当前 bundle 支持的 strongest honest step 不是“开跑 full panel”，而是“把 full-panel path 补到可审状态”。〔highorder_raw_logprob_panel.py:4-10, 425-460; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:320-330〕

具体要做的事如下。

- **补上真正的 full-panel mode，但与 smoke mode 严格分离。** 在 `experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` 中新增显式 `--full-panel` 模式，要求 checkpoint inventory 先枚举完整 50 个 `(seed, generation)` 路径，任何缺失即中止；输出单独的 full-panel manifest 与 aggregate 目录，不要复用 smoke 文件名。当前脚本只支持 `--manifest-only` 和 `--one-checkpoint-smoke`，这是必须先补的实现缺口。〔highorder_raw_logprob_panel.py:4-10, 425-460〕

- **把 provenance 锁紧。** full-panel manifest 必须新增并强制写入 `builder_script_sha256`、`expected_commit` 或等价 `bundle_commit`、`schema_sha256`、`source hashes`，并提供 `--expected-schema-sha256` 与 `--expected-builder-sha256` 之类的参数；如果实际文件 hash 不匹配，直接 abort。runbook 已要求 `builder_script_sha256`，但当前 manifest 没有。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:154-173; manifest_only_20260622.json:1-75; one_checkpoint_smoke_seed1_gen0_manifest.json:1-122〕

- **先做失败型 smoke，而非只做成功型 smoke。** 至少补三类负控：
  一是**篡改 schema** 的 smoke：改一个 q4 edge 或 bin size，脚本应在 schema-freeze gate 处失败；
  二是**篡改 source hash** 的 smoke：改 `input_ids_sha256` 或 `target_counts_sha256`，脚本应在 data-source gate 处失败；
  三是**错误 split/措辞** 的 smoke：任何把 `train` 写成 `eval_split` 或 validation/test 的输出，应被标成 `invalid_artifact`。这些负控现在都没有跑。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:179-190; highorder_raw_logprob_panel.py:89-131, 153-189〕

- **补至少一个多 checkpoint smoke。** 现在只有 `seed=1, generation=0` 的 smoke；这不足以排除硬编码路径、特例 checkpoint 或循环枚举 bug。建议至少再跑两个不同 checkpoint 的 smoke，覆盖**不同 seed**与**不同 generation 段**，例如一个早期、一个中期/后期。只有这样，full-panel generator 才不至于是“只会跑 s1g0 的脚本”。当前零差复现只能证明这个点，不证明全 50 格网。〔PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:41-51, 71-103; one_checkpoint_smoke_seed1_gen0_manifest.json:74-121〕

- **把 full-panel analysis 单独实现成新脚本，不要继续借用 `math_turn_loso_audit.py`。** 新脚本必须以 q4 full panel 为输入，显式实现 fold-local 的 LOSO、fold-local pairing、fold-local projection fitting，以及 runbook 规定的 mean-only / rank-1 synthetic controls；输出 machine-readable JSON，并使用 runbook 的词表 `invalid_artifact / killed / insufficient_artifact / eligible_for_next_design_review_only`。不要在任何新脚本里保留 `survive` 作为 verdict 词。〔PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:206-307; math_turn_loso_audit.py:190-227〕

- **清理措辞泄漏。** 把 `highorder_ppl_run.py` 中把 train blocks 叫作 `eval` 的注释和打印文案改掉；把所有 summary/template 中可能导向 `LOSO passed`、`F3 positive`、`mean-null vector field survives`、`glass box broken`、`training authorized`、`new loss authorized` 的字符串提前清除。runbook 已经把这些列为 forbidden wording，代码里就不该再残留。〔highorder_ppl_run.py:5-10, 57-76; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:290-310〕

- **不要做的事也要写死。** 不要修补 q8 empty bin；不要把 q8、old rare/freq masks 或额外 projection 提升为 primary；不要把 50 行当独立样本；不要把 full panel 的任何通过解释成训练授权；不要实现 backward、optimizer、EMA、新 loss 或 text generation。bundle 内所有正式文件都已经给出这些边界，后续 coding agent 只能在这个边界内工作。〔README_FOR_PRO.md:117-136; PANEL_PRIMARY_ARTIFACT_PREREG_DRAFT_20260622.md:69-79, 163-178; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:19-20, 104-119, 267-310; PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:24-25, 123-142〕

我的严格结论是：**现在不能批准 full 50-checkpoint q4 panel generation。** 现有 bundle 证明了 q4 schema 锁定与单点 smoke 对齐，证明了 q8 empty-bin 处理是诚实的，也证明了 one-checkpoint reproduction 是零差的；但它**没有**证明 full-panel generator 已实现、完整 provenance 已锁死、负控 smoke 已通过、或者 full-panel gate analysis 已具备 fold-local 与 rank/noise-floor 的可执行实现。因此，当前阶段至多只能说：**“当前 generator 与 q4 locked schema 仅具备进入 full-panel generation review 的资格。”**〔README_FOR_PRO.md:130-136; PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:301-307, 320-330; PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:138-142〕