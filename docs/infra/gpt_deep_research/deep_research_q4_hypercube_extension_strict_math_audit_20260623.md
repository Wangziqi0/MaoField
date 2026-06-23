# MaoField 超立方体扩展严格数学审计

## 结论

我的判定是：**Allow zero-GPU audit only**。理由不是保守措辞，而是对象尚未被实现、尚未被识别、也尚未被证伪到足以支持更强动作。就这份 bundle 的可核验证据而言，MaoField 当前**没有**一个已观察到的、可作为“超越 scalar collapse / smoothing”的非标量数学现象；现有实现停留在 q4 频率分箱上的均值模态 \(D\)、均值去除后的 \(u\)，以及单一有序频率斜率投影 \(P\)。full 50-checkpoint panel 仍未实现；独立的 fold-local q4/full-panel 分析脚本缺失；你点名要求先读的四个 2026-06-23 关键文件在 bundle 内也不可得，因此你在问题里给出的“weighted slope-orthogonal residual field”公式目前只能作为**上下文目标**，不能作为**仓库已证事实**。`STATE.md`、研究索引、runbook、q4 adoption note 和 generator 代码都一致把当前状态限定为 `insufficient_artifact` / `blocked-until-gated` / `full panel not approved`。`highorder_raw_logprob_panel.py` 还明确写着 full 50-checkpoint panel generation **未实现**。因此，现在能允许的最强动作不是 full panel，不是新训练，不是新 loss，而只是**零 GPU 的形式化预注册/可识别性审计**。 (`repo_files/STATE.md` L22-L27, L29-L33; `repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md` L5-L14, L26-L33; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L14-L25, L305-L335; `repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L33-L40, L62-L67; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L1-L12, L487-L492)

更尖锐地说：**如果把 scalar smoother、人为 dashboard 坐标和事后故事都拿掉，当前 bundle 里留下的不是“已成立的残差场”，而只是“一个未来可审计的残差算子目标”**。这个目标若要在超立方体扩展中保持数学意义，必须被改写成：在一个**预注册的有限乘积划分**上，先去掉均值模态与预先固定的 nuisance 子空间，再只检验其正交补中的**交互残差**是否存在、是否稳定、是否优于随机同性维子空间、是否在留一 seed / 留一 generation block 下不崩。达不到这一步，所谓 hypercube 只是在增加坐标，自由度更大，进步更少。 (`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L21-L23, L83-L112, L124-L153; `repo_files/docs/infra/gpt_deep_research/MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md` L20-L24, L53-L53)

## 证据边界

我本次审计**只使用上传的仓库 bundle** 作为主证据，不用 public GitHub、不用 raw.githubusercontent、不用搜索引擎摘要，也不根据记忆补文件内容。这与 bundle 内现有 strict-audit 文件的边界一致。 (`repo_files/docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md` L5-L7)

按你指定顺序，我实际读到的文件如下。可读：`repo_files/STATE.md`，`repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md`，`repo_files/MD_CATALOG.md`，`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md`，`repo_files/scripts/math_turn_loso_audit.py`，`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md`，`repo_files/docs/infra/gpt_deep_research/MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md`。**不可得**：`repo_files/docs/infra/gpt_deep_research/Q4_RESIDUAL_FIELD_STRICT_MATH_AUDIT_ADOPTION_NOTE_20260623.md`，`repo_files/docs/infra/gpt_deep_research/deep_research_q4_residual_field_strict_math_audit_20260623.md`，`repo_files/docs/infra/math_turn_20260622/Q4_IMPLEMENTATION_GATE_UPDATE_20260623.md`，`repo_files/scripts/q4_full_panel_foldlocal_analysis.py`。因此，这四个文件中的任何主张，我都**不能**当作 repository fact。 (`repo_files/MD_CATALOG.md` L6-L12; `repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md` L16-L33)

我另外读取了与当前 q4 审计直接相关、但不在你“必读清单”中的本地证据文件：`repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md`、`repo_files/docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md`、`repo_files/scripts/build_panel_schema_20260622.py`、`repo_files/docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json`、`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md`、`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_NEGATIVE_SMOKE_20260622.md`、`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md`、`repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/*.json`，以及 `raw_wip/*.jsonl` smoke rows。这样做的原因很简单：索引和 adoption note 只能定位，真正可裁判的还是代码、schema、manifest、aggregate 与 raw rows。 (`repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md` L26-L33; `repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L9-L23)

在“Markdown prose 与 code/data 冲突时，代码/数据优先”的规则下，这里有一个必须点明的小冲突：runbook 要求 manifest 必须带 `builder_script_sha256` 等 provenance 字段，但 bundle 里的 `one_checkpoint_smoke_seed1_gen0_manifest.json` 是较早的 v1 产物，确实缺少这组字段；相反，当前 `highorder_raw_logprob_panel.py` 的 `base_manifest()` 已在代码里加入 `builder_script_sha256` 与 `generator_script_sha256`，而 seed2/gen5、seed42/gen9 的 v3 manifests 也已补上。这说明**provenance 清理在进行，但尚未形成统一历史一致性**，所以不能把“manifest 问题已彻底解决”当作已完成事实。代码与 later manifests 可以证明“修补已写入”，但不能抹掉 earlier artifact 的缺口。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L158-L177; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L171-L223; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md` L17-L20)

## 当前 q4 对象的重建

就 **bundle 内已实现对象** 而言，q4 的 sample unit 不是 token，也不是 fold，而是一个 checkpoint 行 \(i=(s,g)\)，即固定 checkpoint root 下某个 `seed` 与某个 `generation` 的组合。raw row 仍然是 token 级记录，但聚合审计的行单位是 checkpoint。runbook 把 panel scope 锁定为 seeds `[1,2,3,4,42]` 与 generations `0..9`，generator 代码也把这些范围写死。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L125-L140; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L54-L55, L84-L85, L489-L492)

在每个 checkpoint 单位 \(i\) 上，当前 q4 向量是
\[
k_i=(k_i(0),k_i(1),k_i(2),k_i(3))\in\mathbb{R}^4,
\]
其中
\[
k_i(j)=\text{该 checkpoint 在 q4 slice }j\text{ 上的 token logprob 均值。}
\]
这不是我的猜测，而是 `aggregate_smoke()` 逐 slice 取 `mean_logprob` 后写成 `k_value = mean`；runbook 也把 primary schema 固定为四个按 `target_count_audit_blocks` 生成的 q4 频率箱，edges 为 `[2,10,73]`，bin sizes 为 `[1374,2581,2020,2089]`。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L75-L106; `repo_files/scripts/build_panel_schema_20260622.py` L81-L90, L111-L167; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L139-L149, L276-L311)

权重是
\[
w_j=\frac{n_j}{\sum_{\ell=0}^{3} n_\ell},
\]
在当前固定 source blocks 下，\(n_j\) 由 schema 锁定。加权内积写作
\[
\langle x,y\rangle_w=\sum_{j=0}^{3} w_j x_j y_j.
\]
当前均值模态是
\[
D_i=\langle \mathbf 1,k_i\rangle_w=\sum_{j=0}^{3} w_j k_i(j),
\]
均值去除后的向量是
\[
u_i = k_i - D_i \mathbf 1.
\]
这在 runbook 和 `weighted_projection()` 中完全一致：runbook 明写 `D = sum_j w_j k_j`、`u_j = k_j - D`；代码也先算 `d_value = sum(weights * k)`，再做 `u = k - d_value`。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L95-L106; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L258-L273)

当前**唯一被实现并允许触发 primary diagnostic carrier 的方向**是有序频率斜率方向。其原始坐标是
\[
v_{\mathrm{raw}}=(-1.5,-0.5,0.5,1.5),
\]
然后做 weighted-center 与 unit-normalize，得到 \(v\)。最后定义单一标量投影
\[
P_i=\langle v,u_i\rangle_w.
\]
runbook 明确说 “No other projection can trigger the strongest verdict”；generator 也只输出 `projection_weights_v` 与 `primary_projection_P`。因此，**当前代码实现的 q4 主对象仍然是一个 scalar carrier \(P\)，不是残差场**。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L95-L106, L271-L307; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L258-L273, L316-L325)

如果把你在问题中给出的 2026-06-23 上下文公式
\[
r_i=u_i-\langle v,u_i\rangle_w v
\]
当作一个**目标对象**，那么它在 q4 加权空间里的数学维度是清楚的：四维空间里去掉均值模态后得到三维 mean-null 子空间；再去掉一个单位斜率方向，余下的是二维残差子空间。这个“二维”是线性代数推导，不是仓库里已经过脚本验证的事实。bundle 内四个 2026-06-23 关键文件缺失，所以我**不能**把“当前 adopted q4 object 已正式切换为 residual field”写成仓库真相。我只能说：**从数学上，这个 residual object 合法；从仓库证据上，它尚未在当前 bundle 中被验证为已实现对象。**（线性代数推导；缺失文件见上节）

当前脚本真正测试的东西，也必须说清。`math_turn_loso_audit.py` 不是 q4 residual-field 脚本，它读取的是旧的 `highorder_result.json` aggregate rows，只对 `F1_var`、`F1_tail`、`F3_slice_gap` 三个标量指标做 LOSO delta、matched-mean 与一个“两切片 diagnostic placeholder”的 rank audit；它自己就在注释和返回值里承认当前 artifact 只有 rare/freq 两切片，**不能**认证固定的 `J>=4` mean-null vector field。换言之，旧 zero-GPU 脚本测试的是“旧 aggregate 标量是否值得继续追踪”，不是“q4 residual field 是否存在”。 (`repo_files/scripts/math_turn_loso_audit.py` L1-L8, L21-L27, L91-L114, L117-L187, L190-L227, L323-L345; `repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L124-L153)

同时，`highorder_raw_logprob_panel.py` 也不是 full-panel q4 分析脚本。它只支持 `--manifest-only` 与 `--one-checkpoint-smoke`，并且在文件开头直接声明 full 50-checkpoint panel generation **未实现**。smoke 记录和 multi-checkpoint smoke 也都把自己限定为 generator alignment / schema closure / one-point or three-point reproduction，而不是科学证据。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L1-L12, L420-L459, L487-L513; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md` L8-L25; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md` L8-L20)

## 超立方体候选与识别问题

一个干净的 hypercube 扩展，不应当是“把更多轴塞进 dashboard”，而应当是把 q4 的 slice 向量推广为一个**有限乘积划分上的加权 cell 向量**。设 panel 单位仍是 checkpoint 行 \(i=(s,g)\)。设
\[
C=A_1\times A_2\times \cdots \times A_m
\]
是预注册 cell 集。对每个 cell \(c\in C\)，定义
\[
k_i(c)=\frac{1}{n_c}\sum_{t\in T_c}\ell_{i,t},
\]
其中 \(\ell_{i,t}\) 是第 \(i\) 个 checkpoint 在固定 train audit blocks 上第 \(t\) 个 token 的 logprob，\(T_c\) 是落入 cell \(c\) 的 token 集，\(n_c=|T_c|\)。权重定义为
\[
w_c=\frac{n_c}{\sum_{c'\in C} n_{c'}}.
\]
这样 \((\mathbb R^C,\langle\cdot,\cdot\rangle_w)\) 成为一个有限维加权 Hilbert 空间。这个定义与当前 q4 代码完全兼容：只不过把四个 slice cells 推广为多轴 cells。原始可观测 token-level 字段，bundle 当前确实只给出了 `audit_block_id`、`token_pos`、`target_token_id`、`target_count_audit_blocks`、`slice_id`、`token_logprob` 等，见 `write_raw_jsonl()`。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L380-L405)

但 axis 不能随便编。根据 bundle 可证字段，我认为现在唯一能被严肃讨论的 axis 只有三类。第一，**频率轴**：当前锁定的 q4 frequency quantile，这是现成 primary schema。第二，**位置轴**：`token_pos` 可直接从 raw rows 读出，因此可以预注册成粗位置桶。第三，**source localization 轴**：例如 `audit_block_id` 的粗桶，这在数据上可得，但科学意义偏弱，最多适合 sensitivity / nuisance，不适合作 primary 结构轴。反过来，`token-type bucket` 在 bundle 内没有 canonical 映射；`baseline surprise bucket` 在 raw rows 中没有 baseline/ref logprob 字段，当前 bundle 也没有你点名缺失的 `q4_full_panel_foldlocal_analysis.py` 来定义这种 baseline；`seed`、`fold`、`generation` 则更不应被当成 cell 轴，而应当保留为 panel 单位索引或 CV block，否则会把“结构坐标”和“样本索引”混在一起。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L380-L405; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L125-L140)

因此，一个**最小而干净**的 hypercube 候选是
\[
C=Q\times B,
\]
其中 \(Q=\{0,1,2,3\}\) 是锁定 q4 频率箱，\(B=\{0,1,2,3\}\) 是从 `token_pos` 预注册出来的四个粗位置桶。这个选择至少满足两点：它完全来自 bundle 现有字段；并且在现有 smoke raw rows 上，16 个 cells 全都非空。我本地对 `raw_wip/smoke_seed1_generation0_token_panel.jsonl` 直接计数得到：`q4 × 4个 token_pos 桶` 的 16 个格子全部非空，而 `q4 × 128个 audit_block_id` 虽然也非空，但最小格子只有 1 个 token，明显过稀；这正好说明“位置粗桶”比“block 精细轴”更接近可审对象。这个计数不是正向证据，只是 feasibility check。原始字段模式由 `write_raw_jsonl()` 固定。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L380-L405；本地派生计数基于 `raw_wip/smoke_seed1_generation0_token_panel.jsonl`)

接下来必须定义 nuisance 子空间 \(N\)。如果做得不狠，hypercube 就只是更大的 dashboard。我给出一个严格版本。先定义总均值模态 \(\mathbf 1_C\)。再设 \(v_Q\) 是当前 q4 的 locked frequency-slope 方向，提升到 hypercube 空间就是
\[
\tilde v_Q = v_Q\otimes \mathbf 1_B.
\]
若再加入位置轴 \(B\)，那么所有**纯位置主效应**也必须当 nuisance，因为“不同 token 位置天然难度不同”本来就是最典型的 scalar smoother 容器。于是
\[
N_{\mathrm{mand}}
=
\operatorname{span}\{\mathbf 1_C,\tilde v_Q\}
\;\oplus\;
\{\,\mathbf 1_Q\otimes g:\ \langle g,\mathbf 1_B\rangle_{w_B}=0\,\}.
\]
在这个定义下，真正的超立方体残差对象是
\[
r_i = P_{N_{\mathrm{mand}}^\perp}k_i.
\]
若进一步要求比当前 q4 更强的 additive stripping，则还可以把频率轴的全部 centered main effects 一并塞进 nuisance；那样得到的是更接近 weighted ANOVA interaction residual 的对象。但我不建议先走这一步，因为自由度会更大、解释更脆。**最低限度**必须做的是：去掉总均值、去掉 q4 slope、去掉所有纯新增轴主效应。否则你根本没有证明“不是 scalar smoothing”。（数学推导，基于当前 q4 slope 定义见 `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L95-L106）

这里立刻暴露出识别问题。若 \(C=Q\times B\) 且 \(|Q|=|B|=4\)，那么 \(\dim \mathbb R^C=16\)。即便只去掉 \(\mathbf 1_C\)、q4 slope 和位置轴 centered main effects，nuisance 维数也至少是 \(1+1+3=5\)，剩余的 \(N^\perp\) 维度仍有 11。若再去掉完整 additive main effects，则 nuisance 维数是 \(1+3+3=7\)，残差仍有 9 维。**这比原 q4 的二维残差空间大得多，也比 50 行 panel 更容易产生 rank inflation、multiple comparisons 与解释任意性。** 所以 hypercube extension **本身并不自动解决 non-identification**；恰恰相反，它先把坐标自由度扩大了。除非你把 axis、权重、nuisance basis、coarsening/refinement 稳定性和 random-subspace guard 全部预注册，否则“tensor structure”不会自动变成数学对象，它只是更大的坐标图。这个批评与当前收敛 note 的精神完全一致：下一步必须拒绝 scalar completion，但也不能把“更多指标”错当成新 carrier。 (`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L83-L112, L138-L150)

因此，我对“hypercube 是否真的解决识别问题”的回答是：**默认不解决**。它只有在下列条件同时满足时，才从“任意坐标膨胀”变成“可识别的残差对象”：轴来自 outcome-independent observables；cell weights 来自 source-only schema；nuisance projection 事先固定；CV 是 fold-local 的；residual 的稳定性优于 matched-mean/-slope 与随机同性维子空间；结果对合理 coarsening/refinement 不脆弱；empty/sparse cell 被严厉处理。少一个都不行。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L183-L307; `repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L36-L40, L55-L67)

## 代码审计与反证

从代码层面说，**已实现的**部分很有限，但边界清晰。`build_panel_schema_20260622.py` 确实会重建固定的 Wikitext-2 train audit blocks，并锁定 q4 primary schema；它还诚实地把 q8 标成 `not_locked_empty_bin`，并把“changing quantile method / tie policy / bins from outcomes”等 fallback 列为 forbidden。`highorder_raw_logprob_panel.py` 也确实会验证 schema/source hashes、重建 tokens 的 q4 slice assignment、在一个 checkpoint 上写 raw JSONL 与 aggregate JSON，并输出 `D`、`u` 与 `P`。当然，negative smoke 与 multi-checkpoint smoke 也都已存在，并且严格把自己限定在 invalid-artifact 检查和 generator alignment。 (`repo_files/scripts/build_panel_schema_20260622.py` L46-L62, L81-L90, L111-L167; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L120-L168, L171-L223, L258-L325, L380-L405; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_NEGATIVE_SMOKE_20260622.md` L8-L10, L14-L25, L33-L36; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md` L8-L20)

**缺失的**部分才是本次审计的中心。第一，full 50-checkpoint generator mode 缺失，这不是 interpretation，而是代码开头直写、参数解析直拦。第二，你点名要读的 `scripts/q4_full_panel_foldlocal_analysis.py` 在 bundle 中不存在。第三，bundle 内没有任何已执行脚本计算并审计 \(r_i=u_i-\langle v,u_i\rangle_wv\) 这一 q4 slope-orth residual field；代码只算 \(D,u,P\)。第四，没有任何已实现的 fold-local hypercube analysis path：没有 matched-slope control，没有 random same-dimension subspace multiplicity guard，没有 coarsening/refinement sensitivity check，没有基于 full panel 的 residual rank/noise-floor 审计。第五，旧 `math_turn_loso_audit.py` 明确只是旧 aggregate 的 zero-GPU gate，而且其 rank audit 自己承认只是两切片 placeholder。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L1-L12, L487-L513; 缺失：`repo_files/scripts/q4_full_panel_foldlocal_analysis.py`; `repo_files/scripts/math_turn_loso_audit.py` L161-L187)

这直接回答你的第三问：**当前代码没有实现 hypercube object；甚至连你给出的 q4 residual object 也没有作为 bundle-observed 主对象实现。当前实现的是 smoke path、schema alignment、source/provenance closure，以及旧 aggregate 的 LOSO/matched-mean 占位审计。** 所以若有人现在说“hypercube 只是 q4 residual 的自然推广，我们已经有了基础实现”，那是错的。现有基础实现只够说明“q4 schema + one-checkpoint raw/aggregate path 是可跑的”，不够说明“residual operator 已进入证据层”。 (`repo_files/docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md` L14-L18, L24-L30, L71-L75, L90-L96)

我现在给出一个比乐观框架更有价值的**负定理**。

**命题一：后验 nuisance 选择不可证。**
设 \(H=(\mathbb R^C,\langle\cdot,\cdot\rangle_w)\) 是任意有限维加权 Hilbert 空间，\(\mathbf 1\) 是常数模态，\(u\in H\) 满足 \(\langle u,\mathbf 1\rangle_w=0\) 且 \(u\neq 0\)。若分析者可以在看完 \(u\) 之后再选择一个一维 nuisance 方向 \(v\subset \mathbf 1^\perp\)，那么残差范数
\[
\|P_{v^\perp}u\|_w
\]
不是不变量：取 \(v=\operatorname{span}\{u\}\) 时残差为 \(0\)；取任意与 \(u\) 正交的 \(v\) 时残差为 \(\|u\|_w\)。因此，只要 nuisance basis 允许后验选择，所谓 residual signal 就可以被“做出来”或“擦掉”。这不是统计直觉，而是线性代数。**推论**：hypercube 只有在 axis 与 nuisance space 预注册时才可能成为证据对象；否则它只是坐标操纵。 （数学命题；与 runbook 对 fold-local / schema-freeze / multiplicity 的要求一致，见 `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L189-L193, L238-L275）

**命题二：在当前 bundle 证据下，任何 hypercube residual field 都不具有 evidential meaning，除非同时满足 X、Y、Z。**
X：存在完整 full-panel raw rows，而不是 3 个 smoke 点。
Y：cell axes、weights 与 nuisance 投影都在 outcomes 之外固定。
Z：存在独立的 fold-local analysis 脚本，对 residual 实施 matched-mean/-slope、随机子空间、多重性、rank/noise-floor、coarsening/refinement 检查。
证明思路很直接：当前 bundle 已知 full panel 未实现，分析脚本缺失，而 smoke artifacts 只能证明生成器与旧 aggregate 对齐，并不能把任一超立方体残差从“候选坐标”提升为“已识别现象”。所以在现有证据下，hypercube extension 最多只能进入 **formal prereg / zero-GPU feasibility audit**。 (`repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L33-L40, L62-L67; `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L1-L12; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md` L8-L25)

## 证伪与零 GPU 审计

如果这个对象其实只是 scalar smoother、matched-mean artifact、leakage 或 multiplicity 伪影，那么最快的 kill tests 应该非常残忍，而且都可以在 zero-GPU 路线先定义清楚。

第一类是**加性剥离 kill test**。对候选 hypercube \(C=Q\times B\)，先拟合加性 nuisance：
\[
k_i(q,b)\approx \mu_i+\alpha_i v_Q(q)+\gamma_i(b),
\]
其中 \(\gamma_i\) 是位置主效应；若你采用更保守版本，则再加完整 frequency centered main effects。然后看残差
\[
r_i=P_{N^\perp}k_i
\]
的加权范数、奇异值谱、留一 seed 稳定性。若 \(\|r_i\|_w\) 在 noise floor 内，或主方向在留一 block 下翻转，直接 kill。这个测试是对“不是 scalar smoother”的最短路径，因为它先把所有简单加性解释剥干净。支持它的仓库动机已经写在 convergence note 与 runbook 里：候选结构必须在 nuisance-only prediction 与 rank/noise-floor 下仍存活。 (`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L138-L150; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L238-L269)

第二类是**matched-mean / matched-slope 双重匹配 kill test**。当前 runbook 只写了 matched-mean gate，且主对象是 \(P\) 与 \(D\)。对 hypercube，我要求更狠：先匹配 \(D\)，再匹配 q4 slope \(P\)；只有在 \((D,P)\) 都匹配后，比较 residual \(r_i\) 是否仍有稳定方向。若在 matched-\((D,P)\) 后 residual 信号消失，那么 hypercube 只是 \(D\) 与 \(P\) 的重标记。这个要求比当前 runbook 更严，但正是 hypercube 想声称“超过 q4 scalar carrier”时所必须付出的代价。当前 bundle 没有脚本实现这一点，所以它只能作为待实现 kill-test，而不是已有 through gate。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L224-L251)

第三类是**随机同性维子空间 kill test**。假设 hypercube residual 补空间维数是 \(d\)。那就必须以固定 RNG、固定权重、固定 fold-local protocol，从 \(\mathbf 1^\perp\) 中抽 many random \(d\)-dimensional subspaces，比较所选 residual 子空间在稳定性、LOSO retained energy、奇异值谱和 matched-control surviving rate 上是否真正优于随机同维子空间。若不优于随机基线，kill。原因很朴素：在 9 维、11 维这种补空间里，随便抽一个方向都可能“看上去有结构”。不做 random-subspace guard，hypercube 几乎必然退化成 multiplicity 游戏。当前 bundle 的 runbook 已经把 multiplicity 原则锁死在 q4 primary 上；hypercube 若不做得比它更严，就根本没有资格自称 extension。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L271-L275; `repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L47-L56)

第四类是**axis permutation / coarsening / refinement kill test**。如果新增轴是位置桶 \(B\)，那么在每个 checkpoint 行内、在保持 q4 slice 总量不变的前提下，随机打乱位置标签，或把 `4桶→2桶`、`4桶→8桶` 做预注册 sensitivity。若结果只在某一套桶化上“漂亮”，一 coarsen/refine 就翻转，kill。这个测试的意义是强迫你面对“partition arbitrariness”：如果 hypercube 真的对应对象，合理粗化或细化不应立即把它变成零。当前 bundle 里 q8 因 empty bin 诚实地被降成 sensitivity-only，这已经告诉你：**划分一旦动，结论就可能立刻失效**。hypercube 只会把这个问题放大。 (`repo_files/scripts/build_panel_schema_20260622.py` L81-L90, L126-L167; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L108-L123, L271-L275)

第五类是**稀疏格子 kill test**。空 cell 直接 invalid；极稀 cell 不能做 primary。当前我本地数过：`q4 × 4个 token_pos 桶` 的 16 格在 smoke rows 上全非空，倒是还像个可行的零 GPU 候选；而 `q4 × 128个 audit_block_id` 虽然无空格，但最小格只有 1 个 token，这种对象连 primary 候选都不配。结论很简单：如果 hypercube 一上来就把每格样本数打进几十以下，它不是“更高维对象”，而是“更高噪声对象”。（本地派生计数基于 `raw_wip/smoke_seed1_generation0_token_panel.jsonl`；raw 行字段来源于 `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L380-L405）

基于这些 kill tests，我建议在 node36 先做一个**严格的零 GPU 审计脚本**，而不是任何 full-panel 生成。脚本建议新建为 `repo_files/scripts/q4_hypercube_zero_gpu_audit.py`，不要改写现有 `math_turn_loso_audit.py`，因为后者是旧 aggregate 审计，不该继续承载新对象。它的输入应当只允许：锁定 q4 schema JSON、现有 smoke manifests/aggregates、`raw_wip/*.jsonl` smoke rows、runbook，以及一个**单独的 hypercube schema JSON**。输出应是两个工件：一个 machine-readable JSON，一个 MD 摘要。Pass/fail 只允许给出 feasibility / no-go 结论，比如：`invalid_artifact`、`axis_not_justified`、`sparse_cells`、`formal_prereg_only`。这个 zero-GPU 审计**不应该产生任何正向科学 verdict**；它的作用只是判定“哪些轴可以被正式预注册，哪些根本不该进入 primary”。 (`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L114-L123, L124-L153; `repo_files/scripts/math_turn_loso_audit.py` L1-L8, L230-L345)

若日后才考虑 full panel，那么所需工件边界必须更硬。raw rows 至少要保持当前字段：`schema_id`、`seed`、`generation`、`source_split`、`audit_block_id`、`token_pos`、`flat_token_index`、`target_token_id`、`target_count_audit_blocks`、`slice_id`、`token_logprob`、`neg_logprob`；新增 hypercube 轴标签最好不要直接写进 raw rows，而应由一个新的 schema builder 从这些 outcome-independent 字段**确定性派生**，以避免 outcome leakage。manifest 必须统一记录 `artifact_generation_repo_head`、`repo_head`、schema/builder/generator SHA、source hashes、checkpoint root、seed/generation 范围、device、dtype、`no_training=true`、`no_new_loss=true`。分析脚本必须与 generator 分离，严格实现 fold-local projection、fold-local matching、随机子空间 guard、coarsening/refinement guard 和 wording guard。即便未来这些都做好，最强允许表述也仍只能停在“eligible for next design review only”这一类级别，不能偷渡成“residual field observed”或“glass box broken”。 (`repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py` L171-L223, L380-L459; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L142-L177, L283-L314)

## node36 下一步

对 Codex on node36，我给出的下一动作是收紧，而不是扩张。

第一，**不要**动现有 `build_panel_schema_20260622.py` 和现有 q4 primary schema。若要做 hypercube，只能新建一个单独的 schema builder，例如 `repo_files/scripts/build_hypercube_schema_YYYYMMDD.py`，并且它只允许使用当前 raw rows 中已存在、与 outcome 无关的字段生成 axes。第一版建议只允许 `freq_q4 × token_pos_quartile` 这一最小候选，明确禁止 token-type、baseline surprise、post-hoc block patterns 进入 primary。q8 的历史教训已经足够：别在看见空 bin 或结果之后再修 schema。 (`repo_files/scripts/build_panel_schema_20260622.py` L81-L90, L126-L167; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L108-L123)

第二，新建 `repo_files/scripts/q4_hypercube_zero_gpu_audit.py`。这个脚本只做五件事：校验 schema 与 source closure；输出 cell occupancy；构建并固定 nuisance basis；执行 axis justification/no-go 检查；写 JSON/MD。不要在这个脚本里做任何“显著性营销”。它的职责是：证明对象**可被定义**，而不是证明对象**已经成立**。 (`repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md` L114-L123; `repo_files/docs/infra/gpt_deep_research/MATH_TURN_FRAMEWORK_ADOPTION_NOTE_20260622.md` L20-L24)

第三，若将来真的要补 full-panel path，必须新建而不是继续挪用旧东西。也就是说，未来缺失的 `repo_files/scripts/q4_full_panel_foldlocal_analysis.py` 应当作为**新脚本**补上，输入 full panel raw/aggregate、输出 machine-readable gate verdict；同时 `highorder_raw_logprob_panel.py` 最多只负责 deterministic generation，不负责解释。runbook 已经把“generator 与 analysis 分开”的边界写出来了。 (`repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L316-L335; `repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L36-L40, L62-L67)

第四，词汇守卫必须提前写死。把任何可能输出 `LOSO passed`、`F3 positive`、`mean-null vector field survives`、`glass box broken`、`training authorized`、`new loss authorized` 的摘要模板全部清掉。现有 runbook、claim policy、adoption notes 已经把这些句子列成 forbidden wording；hypercube 扩展只会增加误报风险，不会降低。 (`repo_files/scripts/build_panel_schema_20260622.py` L157-L167; `repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md` L283-L314; `repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md` L55-L67)

最终判定重申一次：**Allow zero-GPU audit only**。这不是鼓励性措辞，而是严格边界。当前 bundle 支持你做的，只有“把 hypercube 变成一个可拒绝、可稽核、可预注册的数学对象”；它**不支持**你把 hypercube 当成已经存在的现象，更不支持由此批准 full panel、新训练或新 loss。若这一步做不好，正确结论不是“研究方向太前沿暂时难证”，而是更简单的那句：**对象尚未被识别。**