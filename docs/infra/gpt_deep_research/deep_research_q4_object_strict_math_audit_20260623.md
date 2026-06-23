# MaoField q4 对象严格数学审计报告

## 结论

**裁定：拒绝把“当前已实现的 q4 对象”视为数学推进候选。**
原因并不复杂。现有包内证据只支持三件事：其一，q4 固定切片 schema 已经锁定；其二，生成器已经能做 manifest-only、单 checkpoint smoke、若干 fail-fast negative smoke，以及三个点的 multi-checkpoint smoke；其三，旧 aggregate 行可以在这三个 smoke 点上被逐字段零差复现。它**不**支持以下更强命题：已经存在 full 50-checkpoint panel；已经存在独立的 fold-local q4 分析路径；已经通过 mean-null 残差、matched-mean、rank/noise-floor 与 multiplicity 的整套门槛；因此更不支持“真实数学推进”“vector field survives”“LOSO passed”“F3 positive”“glass box broken”或任何训练授权。包内 canonical state、研究索引、收敛说明、runbook、adoption note、smoke 记录和代码都同向给出这个边界。〔repo_files/STATE.md:16-27；repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md:5-10,302-336；repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:21-23,39-50,52-68；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:15-21,33-67；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_SMOKE_20260622.md:16-25,123-148；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md:46-53〕

更严格地说，**当前真正剩下的不是一个“已观察到的数学对象”，而只是一个“未来必须被证成的对象定义”**：固定 q4 切片上的**fold-local、去均值、去 nuisance、且非 rank-1 的残差结构**。如果这个对象不存在，MaoField 依旧只是一个标量平滑器周围的后验测量故事。收敛说明已经把旧训练对象定为两项标量 KL/EMA smoother，并明确说“下一步必须拒绝 scalar completion”，转而去问 mean-null 子空间里是否还有稳定残差。〔repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:41-50,72-85,87-112〕

**观察证据类。** 我把脚本、JSON、raw_wip smoke 行和状态说明分开看。观察上，`build_panel_schema_20260622.py` 确实构造了固定 train blocks 上的 q4 schema，并把 q8 因空 bin 降为 sensitivity only；`highorder_raw_logprob_panel.py` 确实只实现了 `--manifest-only` 与 `--one-checkpoint-smoke`，并在文件头写死“full 50-checkpoint panel generation is not implemented here”；`math_turn_loso_audit.py` 只消费旧 `highorder_result.json`，并在 rank/residual 处把自己标成“diagnostic placeholder”，因为它只有 rare/freq 两切片 aggregate。三个 smoke manifest/aggregate 与 raw_wip JSONL 也都表明当前只是单点或三点代码对齐，而不是 full panel。〔repo_files/scripts/build_panel_schema_20260622.py:46-68,81-167；repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:2-12,473-519；repo_files/scripts/math_turn_loso_audit.py:1-7,161-187；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed1_gen0_manifest.json:74-122；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed2_gen5_manifest.json:80-128；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed42_gen9_manifest.json:80-128；raw_wip/smoke_seed1_generation0_token_panel.jsonl:1-3〕

**导出计算类。** 从 locked 定义本身可以推出：q4 primary 统计量 \(P\) 只是 mean-null q4 空间上的一个一维线性泛函，因此单独观察到 \(P\) 的信号，永远不足以说明存在非标量结构；还必须看 full \(u\)-matrix 的 rank/noise-floor 与 nuisance-residual。再从旧 aggregate 审计结果可推出：当前旧 artifact 只有 rare/freq 两切片，所以在去均值后残差空间至多一维，根本不可能认证一个固定 \(J\ge 4\) 的 mean-null vector field。`math_turn_loso_audit_result_20260622.json` 和对应 verdict markdown 已把这件事写死：status=`diagnostic_only_two_slice_aggregate`，`sigma2/sigma1 ≈ 3.27e-17`，最终 verdict=`insufficient_artifact`。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:95-106,253-269；repo_files/docs/infra/math_turn_20260622/math_turn_loso_audit_result_20260622.json:1-63,86-121；repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:5,17-19,25-38,42-49〕

**解释类。** adoption note 与 q4 strict audit 都把 q4 frequency-slope projection 定位成“locked diagnostic carrier”，不是 theory-derived proof object。这一定义是诚实的，也恰好说明它还不是数学推进。它最多是一个被锁定的诊断通道。〔repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:43-50；repo_files/docs/infra/gpt_deep_research/deep_research_q4_panel_strict_audit_20260622.md:49-55〕

**阻断主张类。** 包内多处明确阻断：`LOSO passed`、`F3 positive`、`mean-null vector field survives`、`glass box broken`、训练授权、新 loss 授权都不得说。这里没有解释空间。〔repo_files/STATE.md:27-33；repo_files/GPT55_PRO_RESEARCH_INDEX_20260622.md:329-336；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:283-315；repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:42-49〕

## 形式化定义

用户问的“真正需要存在的 fold-local q4 对象”不是当前 runbook 里的单个标量 \(P\)，而是**固定 q4 切片上的残差向量结构**。把 full panel 的每一行记作 \(r=(s,g)\)，其中 \(s\) 是 seed，\(g\) 是 generation。对锁定的四个 q4 bin \(B_1,\dots,B_4\)，定义每行的切片均值向量
\[
k_r(j)=\frac1{|B_j|}\sum_{t\in B_j}\ell_{r,t},
\]
其中 \(\ell_{r,t}=\log p_{\theta_{s,g}}(x_t\mid x_{<t})\)。weights 由锁定的 bin sizes 给出，
\[
w_j=\frac{n_j}{\sum_{m=1}^4 n_m},
\]
在当前 schema 中 \(n=(1374,2581,2020,2089)\)。runbook 与 aggregate JSON 一致地把均值模写成
\[
D_r=w^\top k_r,
\]
并把 mean-null 分量写成
\[
u_r=P_\perp k_r,\qquad P_\perp=I-\mathbf 1 w^\top .
\]
这里 \(\mathbf 1=(1,1,1,1)^\top\)，因此 \(w^\top u_r=0\)。这正是收敛说明所说的“拒绝 scalar completion，转向 mean-null subspace”的最小形式化对象。〔repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:87-112；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:95-106；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed42_gen9_aggregate.json:9-80〕

runbook 另外锁定了一个**主标量载体**
\[
v_{\text{raw}}=(-1.5,-0.5,0.5,1.5),\qquad
v=\text{weighted-center-and-unit-normalize}(v_{\text{raw}},w),
\]
\[
P_r=\sum_{j=1}^4 w_j v_j u_r(j).
\]
但这只是 `primary scalar projection`，不是你要的“超越 scalar collapse/smoothing 的对象”。原因很简单：\(\mathcal U_w=\{u\in\mathbb R^4:w^\top u=0\}\) 是三维空间，而 \(P_r\) 只是 \(\mathcal U_w\) 上的一个一维线性泛函。即使 \(P_r\) 看起来有信号，也仍然可能只是沿某一预设方向的单轴漂移，而不是稳定的多维残差几何。要超越标量塌缩，真正需要存在的是：**在 held-out seed 上，\(u_r\) 在 nuisance 去除后仍保留非平凡、非 rank-1、且方向稳定的残差能量。**〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:95-106,210-269；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:45-50〕

因此，严格定义如下。
设 fold \(F\) 的 held-out seed 为 \(s^\star\)，训练部分为 \(T_F=\{r=(s,g): s\neq s^\star\}\)，测试部分为 \(H_F=\{r=(s^\star,g)\}\)。对每个 fold，用 \(T_F\) 仅基于训练 seed 拟合 nuisance 预测器
\[
\widehat{\mathcal N}_F:\ (D_r,g_r,g_r^2)\mapsto \widehat u_r
\]
或其对 \(P_r\) 的对应预测 \(\widehat P_r\)。于是 row-space 残差算子为
\[
R_F(z_r)=z_r-\widehat{\mathcal N}_F(D_r,g_r,g_r^2),
\]
其中 \(z_r\) 可以是 \(u_r\) 或 \(P_r\)。用户问的 nuisance scalar subspace 至少包括 slice-space 的 mean mode \(\mathrm{span}\{\mathbf 1\}\)，以及 row-space 的低阶 nuisance 坐标 \(\mathrm{span}\{D_r,g_r,g_r^2\}\)。如果 residualization、matched-mean pairing 或 projection fitting 不是 fold-local，而是先看全局 panel 再定，则结果立即污染。runbook 已把这一点写成刚性要求。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:212-241；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:36-41〕

相应的零假设与备择假设也应当写清楚。
**零假设 \(H_0\)**：q4 对象在去均值后并无稳定残差；任何表面信号都可由 \(D\)、generation、generation\(^2\)、matched-mean 选择偏差、或 rank-1 shadow 解释。形式上，可接受等价表述为：fold-local nuisance 模型几乎解释了全部 \(u_r\) 或 \(P_r\)；matched-mean 的方向统计不稳定；或 centered q4 slice matrix 的 \(\sigma_2/\sigma_1\) 低于锁定阈值，或残差幅度低于 noise floor。
**备择假设 \(H_1\)**：至少一个预注册的 q4 定义对象在 held-out seed 上留下了超出 nuisance-only 预测、且超过 noise floor 的残差；并且 matched-mean 方向稳定，矩阵不是有效 rank-1。〔repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:131-150；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:224-269〕

严格的否证准则已经被 runbook 预写好，我直接采用，不加柔化：
只要出现以下任一情形，就不得宣称该对象成立：其一，LOSO 弱门槛在主标量 \(P\) 上都过不去；其二，matched-mean 两个 tolerance 中任一不稳；其三，residualization、pairing、projection fitting 不是 fold-local；其四，`\sigma_2/\sigma_1 < 0.25` 或残差幅度不超过 \(2\max(\text{seed bootstrap p90},\text{rank-1 control p90})\)；其五，结果依赖未注册切片、q8 修补、旧 rare/freq mask 或其他 post-hoc projection。满足这些 kill 条件中的任一条，就只能得到 `killed` 或 `insufficient_artifact`，绝无更高结论。〔repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:138-150；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:210-315〕

## 代码与制品审计

先说已经实现的部分。`build_panel_schema_20260622.py` 的实现是实的，不是空壳：它离线重建 Wikitext-2 train split 的前 128 个 blocked sequences，用 `numpy.quantile(..., method="nearest")` 和 `searchsorted(..., side='right')` 固定 q4/q8 分箱，锁住 source hashes，并把 q8 的空 bin 写成 `not_locked_empty_bin`，同时把 forbidden claims 写入 schema 的 `claim_policy`。就“固定数据源与切片定义”这一层，它是完成的。〔repo_files/scripts/build_panel_schema_20260622.py:65-168；repo_files/docs/infra/math_turn_20260622/panel_schema_freq_q4_audit_targets_20260622.json:1-15,9047-9153〕

`highorder_raw_logprob_panel.py` 也不是空文件。它能做四件事：重建 blocks 和 source hashes；验证 q4 bin sizes；写 manifest；在一个指定 checkpoint 上前向推理、写 raw JSONL、生成 q4 aggregate，并把旧 `highorder_result.json` 的六个字段做到 \(10^{-5}\) 以内零差复现。negative smoke JSON 还表明它已经能对 schema hash、builder hash、wrong source split、source hash 和 q4 bin size 篡改做 fail-fast 中止。multi-smoke JSON 也表明 seed1/gen0、seed2/gen5、seed42/gen9 三个点都能复现旧 aggregate 行。〔repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:99-149,171-237,258-372,420-519；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/negative_smoke_20260622.json:1-66；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/multi_checkpoint_smoke_20260622.json:1-44〕

但关键缺口恰恰也写在代码里：**full-panel generator mode 根本没有实现。** 这不是我猜测；脚本头部直接写了 `full 50-checkpoint panel generation is not implemented here`，参数解析也只允许 `--manifest-only` 与 `--one-checkpoint-smoke` 二选一。换言之，当前代码实现的是 smoke generator，不是 full-panel generator。〔repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:2-12,473-519〕

再看分析路径。`math_turn_loso_audit.py` 也确实做了一些事：它对旧 50 行 aggregate 跑了 leave-one-seed-out 的 CV-R² 对比、两档 matched-mean sign stability、以及一个 rank/residual 诊断。结果是 F3 的弱 LOSO delta 过了，但 matched-mean 全部失败，rank/residual 也失败，最终 verdict=`insufficient_artifact`。然而这仍然**不是 q4 full-panel analysis**，因为它吃的是旧 `highorder_result.json`，不是 q4 panel；它的 matched-mean 不是 fold-local；它的 rank/residual 只有 rare/freq 两切片 aggregate，因此代码自己已经备注说这只是 placeholder，无法认证固定 \(J\ge 4\) 的 mean-null vector field。〔repo_files/scripts/math_turn_loso_audit.py:91-158,161-227,323-345；repo_files/docs/infra/math_turn_20260622/math_turn_loso_audit_result_20260622.json:1-121；repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:5,17-19,25-49〕

这里必须按你的硬约束处理一次**“Markdown 与 code/data 冲突时，谁赢”**。
runbook 明确要求“每个生成 manifest 都必须包含 `builder_script_sha256`”。但包内实际文件显示：`manifest_only_20260622.json` 与 `one_checkpoint_smoke_seed1_gen0_manifest.json` 都是 `generator.v1`，它们没有 `schema_builder_path`、`builder_script_sha256`、`generator_script_sha256` 或 `artifact_generation_repo_head` 字段；相反，后来的 `seed2/gen5` 与 `seed42/gen9` 的 `generator.v3` manifest 才含有这些字段。因此，**provenance 硬化只在后续 v3 manifest 中部分实现，未在整个 artifact 集中统一实现。**这里必须以实际 JSON 为准，不能因为后续 markdown 说“new v3 manifests include ...”就把更早 v1 manifest 的缺口抹掉。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:158-177；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/manifest_only_20260622.json:1-13,33-40；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed1_gen0_manifest.json:1-13,33-40；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed2_gen5_manifest.json:1-18；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed42_gen9_manifest.json:5-18；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md:17-20〕

所以，对你的第三问，我的答案是：**当前代码没有实现“需要被证成的数学对象”；它实现的是 schema builder、provenance/hash 守门、单 checkpoint q4 aggregate 生成、旧 aggregate 对齐 smoke，以及一个针对旧 rare/freq aggregate 的零 GPU 审计。严格说，它实现的是 smoke tests 与 schema alignment，不是 full q4 object。**〔repo_files/STATE.md:27；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:33-41,62-67；repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:2-12,473-519；repo_files/scripts/math_turn_loso_audit.py:161-227〕

## 现阶段能成立的命题

**命题一：仅凭锁定主标量 \(P\)，无法识别非标量 q4 结构。**
证明很短。按 locked q4 定义，\(u\in\mathcal U_w=\{u\in\mathbb R^4:w^\top u=0\}\)，这是一个三维空间。主统计量 \(P(u)=\sum_j w_j v_j u_j\) 是 \(\mathcal U_w\) 上的单个线性泛函，因此 \(\ker P\cap \mathcal U_w\) 至少二维。于是存在无穷多个不同的 mean-null 向量 \(u\neq u'\) 使得 \(P(u)=P(u')\)。所以，**只看 \(P\) 的任何成功，都不能证明存在稳定的多维残差结构**；它至多证明沿着预设 slope direction 的一维对比有信号。正因为如此，runbook 把 LOSO on \(P\) 与 rank/noise-floor on full \(u\) 分开设门，而不是让 \(P\) 一票否决或一票通过。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:95-106,210-269〕

**命题二：从当前旧 rare/freq aggregate，不可能认证固定 \(J\ge 4\) 的 mean-null vector field。**
这不是观点，是维度事实。当前 `math_turn_loso_audit.py` 的 rank/residual 输入只有 `F3_slice_rare` 与 `F3_slice_freq` 两个切片均值；脚本自己因此把状态写成 `diagnostic_only_two_slice_aggregate`，并说明“这不能认证 proposed fixed J>=4 mean-null vector field”。在两切片情形下，去均值后的残差空间本来就至多一维；于是任何要求“非 rank-1 的 q4 残差几何”的命题，都在输入层面不可判定。输出中的 `sigma2/sigma1 ≈ 3.27e-17` 只是这一维度事实的数值回声。〔repo_files/scripts/math_turn_loso_audit.py:161-187；repo_files/docs/infra/math_turn_20260622/math_turn_loso_audit_result_20260622.json:66-94；repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:32-38〕

**命题三：现在唯一成立的“弱允许句”仍然只是弱 F3 lead，而非数学推进。**
这点已经被 canonical 文档与程序输出共同锁死。旧 aggregate 审计允许的最强表述是 “supports at most a weak F3 lead”，并且明确“不授权训练新 vector-field loss”。收敛说明则把项目定位为“clean negative-centered measurement-audit result”，并说唯一存活技术线索只是“weak, post-hoc F3/slice residual”。这两份文件在语义上是完全一致的。〔repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:42-49；repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:52-68,124-169〕

## 快速证伪

如果你要尽快杀掉“这其实只是 scalar smoother / matched-mean artifact / leakage / multiplicity”的说法，我建议的最小脚本化 kill tests 不是再写长文，而是尽快写出以下四个硬测试。

第一，**fold-local nuisance-only 杀伤测试**。
对 full q4 panel 的每个 held-out seed，只能用其余四个 seed 拟合 \(\widehat P_F(D,g,g^2)\) 与 \(\widehat u_F(D,g,g^2)\)。如果 held-out 上的 \(P\) 或任何 \(u_j\) 的残差解释度几乎消失，或者 LOSO delta 主要来自全局拟合而非 fold-local 拟合，那么对象立刻判死。这正是 runbook 的 nuisance-leakage gate，只是把它从条文变成可执行脚本。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:210-241,250-269〕

第二，**matched-mean 快速杀伤测试**。
固定两档 tolerance \(0.02,0.04\)，但 pairing 必须 fold-local，只能用训练 seed 决定配对规则，再拿去测 held-out seed。一旦两档中任何一档的稳定方向比例达不到 \(0.70\)，或 \(z<2.58\)， claim 就该中止。旧 aggregate 审计已经表明，在当前历史 artifact 上，F3 的 matched-mean 两档全失败；这说明该测试对“看起来有 LOSO delta 的弱指标”具有真实杀伤力。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:224-241；repo_files/docs/infra/math_turn_20260622/MATH_TURN_LOSO_AUDIT_VERDICT_20260622.md:21-30〕

第三，**rank-1 shadow 合成负控**。
用真实 full panel 的 \(D_r\) 和锁定 slope direction \(v\) 构造合成对象
\[
k_r^{(1)} = D_r\mathbf 1 + a_r v,
\qquad
u_r^{(1)} = a_r v,
\]
其中 \(a_r\) 可以按真实 \(P_r\) 反推，或从训练 fold 分布抽样。这个负控天然是 mean-null 但严格 rank-1。如果它也能通过你的 LOSO、matched-mean、甚至主结论门槛，那么你的“对象”其实仍是单轴标量伪装，而不是多维残差。runbook 已经把 “rank-1 synthetic controls must not pass” 写进门槛；现在缺的只是实现。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:238-269〕

第四，**mean-only 合成负控**。
构造
\[
k_r^{(0)} = D_r\mathbf 1,\qquad u_r^{(0)}=0.
\]
如果你的 full-panel 分析路径在这种输入上还能产出“方向稳定”或“eligible_for_next_design_review_only”，那整个分析路径就是漏水的。这个测试非常便宜，而且应当先于任何 full run 的科学解释。runbook 也已经预写了 “mean-only synthetic controls must not pass”。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:238-269〕

第五，**multiplicity 速杀测试**。
把 analysis 脚本硬编码为：只有 `freq_q4_audit_targets_20260622` 加锁定 slope projection 可以触发 strongest allowed verdict；q8、旧 rare/freq top-bottom mask、其他 projection 只输出 sensitivity。只要有任何路径绕过这条约束，立刻记为 `invalid_artifact`。否则你会在 panel 生成以后重新打开 post-hoc 搜索空间。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:271-315；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:52-58〕

## node36 下一步

对 Codex on node36，我的建议不是“再解释”，而是按文件和函数直接开工，且**在任何 full panel run 之前完成**。

首先，改 `repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py`。
这里必须新增一个显式的 `--full-panel` 模式，并与现有 `--manifest-only`、`--one-checkpoint-smoke` 严格互斥。新增的最少函数应包括：`enumerate_expected_checkpoints()`，负责枚举 5×10 的全部 `(seed,generation)` checkpoint，并对任何缺失直接 abort；`run_full_panel()`，负责逐 checkpoint 写 raw JSONL 与 q4 aggregate，并生成单独的 full manifest；`write_full_panel_summary()`，负责输出 full-panel machine-readable summary，而不是复用 smoke 文件名。当前代码没有这些函数，也没有这个模式。〔repo_files/experiments/exp020_metric_stress_test/scripts/highorder_raw_logprob_panel.py:2-12,473-519；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md:48-53〕

其次，给同一脚本补齐 provenance 强制项，而不是只在 v3 manifest 上局部出现。
必须统一写入 `artifact_generation_repo_head`、`schema_builder_path`、`builder_script_sha256`、`generator_script_sha256`，并新增 `expected_commit` 或等价 `bundle_commit` 验证参数；不匹配就 abort。更重要的是，**不要手工编辑已有 v1 manifest**，应在 clean commit 上重跑 `manifest_only_20260622.json` 与 `one_checkpoint_smoke_seed1_gen0_manifest.json`，使整组 panel artifacts 达到同一 provenance 标准。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:158-177；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/manifest_only_20260622.json:1-13；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed1_gen0_manifest.json:1-13；repo_files/experiments/exp020_metric_stress_test/panel_primary_20260622/one_checkpoint_smoke_seed2_gen5_manifest.json:5-14〕

再次，新建**独立**分析脚本，不要继续借用 `math_turn_loso_audit.py`。
建议新增文件名就叫 `repo_files/scripts/q4_full_panel_foldlocal_analysis.py`。这个脚本必须把输入限定为 full q4 panel aggregate，不许再读旧 rare/freq `highorder_result.json` 当主证据；必须实现 fold-local nuisance fitting、fold-local matched-mean pairing、mean-only/rank-1 synthetic controls、rank/noise-floor gate、per-seed LOSO verdict、per-generation paired summaries，并输出 runbook 允许的唯一 verdict 词表：`invalid_artifact`、`killed`、`insufficient_artifact`、`eligible_for_next_design_review_only`。不许出现 `survives` 或任何训练授权词。〔repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:210-315；repo_files/scripts/math_turn_loso_audit.py:190-227；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:36-41,52-58〕

最后，明确哪些事**不要做**。
不要修 q8 empty bin；不要把 q8 提升为 primary；不要把旧 rare/freq masks 复活成 primary；不要把 50 行 panel 当成 50 个独立样本；不要实现 backward、optimizer、EMA、新 loss 或 text generation；不要在 full-panel generator mode 与 full-panel analysis path 尚未落地前运行 50-checkpoint panel。当前 canonical state、runbook、adoption note 与 multi-smoke 记录对这些禁令是一致的。〔repo_files/STATE.md:27-33；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_RUNBOOK_20260622.md:108-123,138-140,271-315,334-335；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:52-67；repo_files/docs/infra/math_turn_20260622/PANEL_PRIMARY_ARTIFACT_MULTI_SMOKE_20260622.md:48-53〕

我的最终句子只有这一句：**现在可保留的，不是“已成立的数学推进”，而只是一个尚未被实现与尚未被证成的 fold-local q4 mean-null residual 审计对象；当前实现仍停在 smoke 与 schema 对齐层。**〔repo_files/STATE.md:16-27；repo_files/docs/infra/EXPERIMENT_CONVERGENCE_AND_MATH_TURN_20260622.md:83-112,124-169；repo_files/docs/infra/gpt_deep_research/Q4_PANEL_STRICT_AUDIT_ADOPTION_NOTE_20260622.md:62-67〕