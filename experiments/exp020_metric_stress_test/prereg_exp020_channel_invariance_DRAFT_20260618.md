# exp020 channel-invariance 测试 · 预注册 DRAFT (D618)

> 🔴 **GATE FAILED (D618, 敌意子 agent a4b1 + 主会话亲核校准)** —— **本设计有致命洞, 不可 commit-lock, 不可跑作 confirmatory。** 修复方向见下 STATUS。
>
> ## STATUS: 敌意 gate verdict (主会话校准版)
> - **致命洞① Φ⊥PPL 共线 (decisive)**: §3a `Φ_data=c·D(μ₀‖p_synth_n)` 含"模型离 μ₀ 距离"因子 = 与 S/PPL 同源 → S-vs-Φ 曲线自相关 vacuous (项目 §4.8 老坑)。修: Φ 只测注入侧外生量 (Φ_data=c·Î(固定真样本; μ₀), 删 D 因子); ⊥PPL gate 改 partial-corr (|corr(Φ,PPL|c)|<0.3 且 |corr(S,Φ|PPL)|>阈, ≥2 seed), 非"回归残差非零"(4 档 c 必给非零, 太弱)。
> - **致命洞② common-currency ⊥ flux_spec_v2 (最深)**: flux_spec_v2 §2 证 c(measure-mixture) 与 1/η_eff(param-prior) 不可通约无满射 = wedge 卖点, 直接反噬"同 Φ 跨通道"。修: 单标量 Φ 降格为**假设非事实**, 预注册"matched-Φ 在 g1 相等但 g9 分层 → common-currency REFUTED"作前置 falsifier; 或改向量值 Φ (但即承认 channel matters = default)。
> - **洞③ S=H̄-留存 metric (核成立, 可修)**: H̄ 非单调 (5/5 seed: g0=3.39→g2谷≈1.92→g9≈2.79), 单端点 S 歧义 + 混淆"恢复 vs 稳定"。**⚠️ 校正子 agent: 它称"testB 疑 S 被 decode 伪通量污染"= 引反了 —— testB 实际 verdict `rep3_injects_flux: False` (rep3≈rep1), 已否决 rep_penalty 伪通量假说。** decode-污染腿(rep_penalty 版)已清; 权重臂"机械抬熵"被"谷-despite-reset"削弱。S 仍需换单调/decode-free/剔 θ₀-基线 metric (per-seq PPL 尾塌缩 or mode-coverage), 但非子 agent 说的那么烂。
> - **洞④ 混杂 (标准, 需预注册控制)**: 每臂"只动一锚"code 层不成立 (c 改 support+样本数; η 改优化动力学+skip 频率; prompt 改 length 分布; base-reset 改初值几何)。控: 固定 total-token/batch/accumulation/warmup/prompt_length/decode/eval-context; 每 cell 报 skip-count + ckpt sha256 全互异。
> - **P (只下调)**: 作 novel 量化贡献存活 conditional on 全部修复 ≈ **10-20%** (低于 flux_spec_v2 旧估 15-30%, 因洞① vacuous + 洞② frame 互斥新暴露)。
> - **决定**: 不锁不跑。战略 fork (重设计 exogenous-Φ+new-S / 收窄回 flux_spec_v2 Borkar-wedge / meta-pattern「测度反复塌回 PPL」自身作 paper) → 留 PI。
>
> --- 原 DRAFT (待修, 勿按此跑) ---

> PI frame-jump operationalize + 反题 dispatch 起草; Linux 执行。
> **源直觉**: 反映论(真实数据=客观实在; 模型=反映; 锚=实践再接触) → 硬预测 channel-invariance。
> **claim 纪律 (红线)**: 论文 claim 停在测试结果 = frame-neutral 信息论陈述 ("崩溃由 channel-(in)variant 真实信息通量支配")。**DM/反映论 = 生成假设的【启发】, discussion 标 [?] 归 Win+PI, 绝不写"实证反映论/DM 实例/first-reflexive-AI/paradigm"。**
> 状态: DRAFT。**§6 铁律: 先过敌意子 agent (攻 flux⊥PPL + common-currency 合法性 + 混杂) → 修 → commit-lock → 才跑/才读。** 本文件 supersede flux_spec_v2 的 scope (Borkar-distinction 现 = 本测试的 data-mixing 臂 vs 权重臂对比, 数学见 flux_spec_v2 §2)。

## 1 可证伪预测 (双向, 锁死)
**H: 崩溃稳定性 S = f(流进系统的真实分布信息【总通量】Φ), 与注入【通道】无关。**
- **支持 (channel-invariant)**: 三通道在【同等 measured Φ】下给【同等 S】→ 三色落**一条** S-vs-Φ 曲线。
- **证伪 (channel matters)**: 同 Φ 下不同通道给不同 S → 三色**分层** → 机制特异 (优化几何 ⊥ 数据测度; Borkar data-only 赢; M3 的 ∝1/η_eff 是其中一条曲线)。
- **两边都是真 finding, 禁 spin**: "channel matters" 不是失败, 是"通道有机制特异性"的 positive 结论 (= flux_spec_v2 的 distinction 在此变成实证可测)。

## 2 三条锚通道 + 扫法 (单变量铁律: 每臂只动一个锚, 其余固定 fp16+manual-LN/seed/N/eval)
| 臂 | 锚 | 扫 | 成本 | 关系到现有 |
|---|---|---|---|---|
| **数据-mixing (c)** | Borkar c / Gerstgrasser 轴 | original_fraction ∈ {0, 0.05, 0.1, 0.2} | 廉价 | 现 2×2 是 c=0 锚点 |
| **权重-reset (∝1/η_eff) = M3** | 优化几何 | base-reset cell (c=0) 扫 epochs/lr 2-3 档 | M3, 中 | 现 2×2 是 fixed-η 单点 |
| **生成-conditioning (prompt)** | 二值 | real vs synthetic | 廉价 (两路估弱) | 现 2×2 已含 (00vs0A / B0vsBA) |
- 现跑的 Stage-A 2×2 {00,B0,0A,BA} = **本测试的 c=0 + fixed-η 子集**, 不浪费; channel-invariance 需补 c-扫 + η-扫两组新链。

## 3 两个测量 (decode-free, CPU@36, 不靠 PPL; flux_spec_v2 的 measure() 复用)
### 3a per-channel 真实信息 flux Φ (本测试地基; 子 agent 重点攻)
**提案定义 (待敌意验证)**: 每代经该通道注入的"对 μ₀ 的真实信息接触量", nats, 测在**注入site (上游 of 崩溃 outcome)**:
- Φ_data(c) = c · D(μ₀ ‖ p_synth_n) — 训练数据里真数据 fraction × 真/合成漂移距 (从训练数据测)。
- Φ_weight(η_eff) — reset 回 θ₀ 恢复的 μ₀-info, 经 1/η_eff 标定 (θ₀ 已编码 μ₀, flux_spec_v2 §1)。
- Φ_prompt — 真 prompt vs 合成 prompt 条件化生成注入的 μ₀-info。
- **common-currency 校准 (必要条件)**: 同 Φ 下, 三通道的**单步 (g0→g1) 即时 recovery 须匹配** (否则 Φ 不是合法共同轴 → 测试无效)。
- **⊥PPL gate (硬, 项目 §4.8 反复栽此)**: 全 (channel,setting) 点回归 Φ on test_ppl; 要求**残差方差非零** (Φ 不是 PPL 单调函数), 否则整个测试循环 = 无效。
### 3b 稳定/崩溃 outcome S (decode-free, 非 PPL)
S = **晚代分布层多样性留存** = (H̄_g9 − H̄_collapsed)/(H̄_g0 − H̄_collapsed), 用 armA measure() 的 eff_supp/H̄ (= "反映的多样性"留存), **非 PPL 轨迹**。
- **S ⊥ Φ 非循环**: Φ 测**输入** (注入 site, 上游), S 测**outcome** (晚代留存); 两者必须独立测、不可同源。

## 4 决定性图 + 判据 (commit-lock 后才读)
plot: **S(y) vs total-Φ(x), 按通道染色**。
- **三色落一条曲线 → channel-invariant → H 支持** (但 DM 归因 [?] Win+PI: 别的 frame 也可能预测 invariance, 测试只证预测不证形而上学)。
- **三色分层 → channel matters → 证伪 H → 机制特异** (M3 ∝1/η_eff 是哪条曲线)。
- 量化判据 (待 §6 子 agent 定): 三色曲线在 matched-Φ 处 S 差 < ε_inv (≥2 seed) → invariant; > ε_strat 且通道间单调可分 → stratified。ε 锁前定。

## 5 分段 (单 GPU 串行, fail-fast; PI ROI §7)
1. **2 点便宜先 (已能定方向)**: c-扫取 2 点 + η-扫取 2 点 (M3 最小), 加现有 c=0 锚 → 初判一条线 vs 分层。
2. 过了再补全曲线 + prompt 臂 + 多 seed (满 5)。c-扫和 prompt-二值廉价; η_eff 扫=M3 主成本。
3. 现 Stage-A 2×2 跑完先 (c=0+fixed-η 锚 + prompt 臂), 不动。

## 6 纪律 (不可省)
- **设计先过敌意子 agent 再跑** (杀 M1 那道关): 重点攻 (a) Φ 真测 real-info-contact 且 ⊥PPL? (b) common-currency 合法? 同 Φ 是否 conflate 三种不可通约注入 (data-mixing 改训练分布 SHAPE 非仅通量大小; η 扫改优化动力学非仅锚强度; prompt 改条件化)? (c) S ⊥ Φ 非循环? (d) 混杂 (通道是否还改 Φ 以外的东西)?
- **commit-lock prereg 后才读结果** (exp019 教训; H 双向判据 + ε + Φ 定义锁死)。
- 每链过 fp16 冻结 gate (sha256 互异/skip/NaN/GradScaler=0); 22 必经 manual-LN patch; 单 GPU 串行 GPU1 核显排除。
- **claim 纪律 (红线)**: claim = "崩溃由 channel-(in)variant 真实信息通量支配" (操作化/frame-neutral/可证伪)。DM/反映论 discussion 标 [?] 归 Win+PI; **绝不写 实证反映论/DM 实例/first-reflexive-AI/paradigm**。
- disclose: Borkar 2506.09401 (persistent-excitation, **data-only — channel-invariance 是他没碰的扩展**) / SIGMA v3 (通道当 knobs 未测 invariance) / Bertrand 2310.00429 / Schaeffer 2503.03150 / 2505.08803 + 2509.04796 (conditioning-grounding 已占)。
- 子 agent Opus 敌意 refute; verbatim 进 paper 必主会话亲核; 哲学归 Win+PI; 一凡 priority1 健康。

## 7 ROI (给 PI; 两边都非 null)
- **channel-invariant** → 真实数据 = 通量一种形式坐实 = 把领域"数据轴"揭示成**一个投影** = construct-validity critique 拿到正面 quantitative clincher (天花板可抬 TMLR)。
- **channel matters** → Borkar 机制特异赢, 仍是干净 falsifiable finding (优化几何锚 = 新轴)。
- D-3 兑现: 理性认识 = outcome 被新实践检验 (非 starting form)。

---
*DRAFT D618。先敌意验 (§6) → 修 → commit-lock → 跑。双向可证伪, 禁 spin。claim frame-neutral, DM 归因永 [?] Win+PI。*
