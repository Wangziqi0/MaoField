# C · meta-pattern 证据库组装 (D618)

> 收口 dispatch §3: C = 默认交付物。**写成【结构解释】非失败清单** (否则被 "skill issue, 没试 X" 打掉)。
> **本文件 = Linux 角色: 组装 frame-neutral 已确立 claim + 证据 trace 库 (可证伪、邀反例)。** narrative/叙事 framing + DM/反映论 归因**归 Win+PI**, 本文件不写, 留占位。
> 红线: 不写"collapse 不可测"(过强); flow-space = labeled hypothesis 非 established; 不复活 DM-instance/first-reflexive/paradigm。

## 1 已确立 claim (frame-neutral, 可证伪, 邀反例)
**"跨 5 次预注册 + 盲 + 敌意-gate 的尝试, 每个候选【独立于 PPL】的崩溃测度——权重距离 / eff_supp / 通道-flux Φ / 恢复相几何 / distinct-2——要么塌回 PPL 的姊妹约简(影子), 要么被晚代 seed 噪声地板淹没(σ 6×@g7, 同通道 5-seed 在测度自己的阈值下假分层 5/10), 要么连轨迹符号都由 decode 配置决定(distinct-2 rep1↔3 翻号)。"**
- **可证伪 / 邀反例**: 谁能给出一个【非 PPL-影子 且 高于晚代噪声地板】的崩溃测度 → 推翻本 claim。
- **不外推**: 只证【这些】测度在【此空间】失败, **不写"崩溃不可测"** (留真独立测度存在的可能)。
- **⚠️ refine (高阶探针 E11, 防过度声称)**: claim 限于"【独立于 PPL】候选测度全塌"。**不可写"一切都是 mean-PPL"** —— PPL 对象**内部**的高阶泛函里, F3 差异化崩溃迟滞 (freq vs rare token 在同 mean_lp 走不同 gap) 是**弱真例外** (尚非 positive, 假复制+0-1/3 bar)。C 的诚实版 = "独立测度全塌 + 高阶大多重构, **一个弱真高阶例外待追**"。

## 2 证据 trace 库 (全已在手, 零新跑; 每条带 source 二值可核)
| # | 证据 | 它确立什么 | source |
|---|---|---|---|
| E1 | exp019 α=1 confirmatory E1/E2/E3 **全反 s42 先验** | 预注册双向可证伪首次正面拦 inflate; C1/C2/C3 撤回 | `exp019_alpha1_confirm/verdict_20260614/` |
| E2 | **gate-1**: M1 权重距离 ‖θ_n−θ₀‖ = base-mode 代码同义反复 (REFUTED) | "测度=代码定义"非 emergent; 子 agent a157 | `flux_spec_borkar_distinction_DRAFT` §5 / commit f572ec1 |
| E3 | **gate-2**: channel-inv Φ_data=c·D(μ₀‖p_synth) 含模型距离项 = PPL 共线 (REFUTED, vacuous) | 测度=PPL 影子; 子 agent a4b1 | `prereg_channel_invariance_DRAFT` STATUS / commit 22e3745 |
| E4 | **gate-3**: keyed S=eff_supp=exp(H̄) 与 PPL=exp(CE) = 同一 softmax logits 姊妹约简 | "decode-free≠非-PPL"; 测度仍 PPL 同源; 子 agent ae8f | `keyed..DESIGN` STATUS / commit 1a7a384 |
| E5 | **gate-4 + 主会话复算**: 晚代 seed σ 爆 6.0× (g7 σ=1.09 vs 早 0.18); 同通道 5-seed k=2 下 **5/10 假分层** | outcome 噪声地板 > 期望通道效应(1v1); 测度阈值低于自身噪声 | `verify_gate4_falsestrat.py` / commit 1a7a384 |
| E6 | 解耦 §3: distinct-2 对 rep_penalty 敏感 (rep=1.0 looping 伪影→假上升; 忠实 rep=3.0 0/5) | 候选独立量被 decode 配置纠缠 | `decouple_verdict_20260617/` |
| E7 | 恢复相几何 ≈ PPL 投影 (E0"崩溃→升维"=PPL 驼峰瞬态, 几何与 PPL 同步) | 又一候选独立测度(几何)被证 = PPL 投影非独立 | `exp018_cat/analysis/RECOVERY_GEOMETRY_FINDINGS_20260615` |
| E8 | fp16 冻结伪影 (D612): 93.388=GradScaler-skip 冻结, 被 3 次读成自愈/恢复(全假) | 精度伪影冒充"恢复信号"的标本 | memory `project_fp16_frozen_attractor` / `wip/maofield_armb_deepdive` |
| E9 | **Stage-A cell 00 matched 基线完成 + 冻结 gate PASS**: g0=37→g2=109 峰→g9=53 复现 hump; **10/10 gen ckpt sha256 全互异 (非冻结, ≠D612 bit-identical)**; val_ppl=nan 仅 1 行(B0 resume re-eval quirk, test 正常)=benign | **hump 非旧链 artifact 坐实** (干净同批 matched 重跑, 真训练); 喂 E5 噪声 | round3 `checkpoints_armb_ABL_00/alpha0.0/no_preserve_seed1/` (sha256 互异 10/10) |
| E10 | **distinct-2 = PPL/eff_supp 影子 + decode 伪量 (gate-5 + 复算确认)**: 忠实 rep=3.0 与 eff_supp R²=0.791 共线; rep=1.0↔3.0 轨迹**翻号** | 测度-inventory **完成**: 第5个候选独立量也塌 (共线+decode 纠缠), A 死 | `preverify_distinct2_independence_DESIGN` VERDICT + `verify_gate5b.py` |
| E11 | **高阶 PPL 泛函大部分重构 mean-PPL, 但有【弱真例外】**: F1-var/tail ~98% mean-PPL 重参数化; **F3_slice_gap 迟滞真** (gen1↔gen4 同 mean_lp ΔF3_gap=0.122 t=-4.6, 纯 mean_lp 函数禁止; 差异化崩溃 freq vs rare 2.2×) | C **不能**写"全塌 mean-PPL"; 高阶大多塌但 **F3 差异化崩溃迟滞 = 弱真结构** (假复制 CV0.4-0.8%, 0-1/3 bar, **值得追非 positive**) | `highorder_ppl_structure_DESIGN` FINAL VERDICT + `highorder_2ndchannel_check.py` + `highorder_verify_hysteresis.py` |

## 3 结构 why (支持的 hypothesis; **labeled hypothesis 非 established**)
- 候选测度都活在**输出分布空间** (next-token logits), 那里 **PPL 主导 + 晚代 seed 噪声地板**。
- (假设) 真正支配崩溃的量在**真实信息流空间** (flow-space) —— **= labeled hypothesis, 不是已确立**。
- **[?] 归 Win+PI**: flow-space 这个 framing 与反映论/DM 的关系 = 生成假设的启发, discussion 标 [?], **Linux 不判, 绝不写"实证反映论/DM 实例"**。

## 4 意义 (frame-neutral)
解释 3 派 (Shumailov / Gerstgrasser / Schaeffer) 为何**实证上吵不出结果**: 都在量同一个被噪声淹没的 PPL 影子 + 各用 decode/精度敏感的伪独立量。= reclassification / 玻璃箱 一路指向的真东西的**可证伪、可发版本**。天花板 TMLR / workshop。

## 5 待 Win+PI (本文件不写, 归属明确)
- 叙事 framing (结构解释怎么讲); 反映论/DM 归因 [?] 段落; paper venue + 措辞; "已确立 negative + 结构 why"的 narrative 编排。
- Linux 只递: §1 claim (frame-neutral) + §2 证据库 (trace 二值) + §3 hypothesis 的测量事实部分。

---
*组装 D618。E10(distinct-2) 待 §1 gate→lock→算 补格。证据库零新跑已成立; 默认交付。*
