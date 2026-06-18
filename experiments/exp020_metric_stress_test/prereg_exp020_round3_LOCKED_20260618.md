# exp020 round3 · 2×2 析因消融 · 预注册 LOCKED (D618)

> **commit-lock 时序 (exp019 教训: 上次开奖前未 lock 被披露, 这次硬锁)**: 本文件 commit 后才读 {00,0A,BA} 与 B0 g4+ 结果。
> **诚实披露**: B0(base-prev,prompt-real) seed1 已跑到 g3 (g0=36.3/g1=78.6/g2=140.1/g3=134.3, 已见, 非冻结 GATE 通过)。本 prereg 锁**判据 + 三控制 cell + 全析因决策**于读它们之前。
> 反题 agent dispatch (D618 ~15:00) 起草; Linux 主会话执行。哲学判读归 Win+PI, Linux 不判。

## 0 命题
"自迭代崩溃 = 内通道(合成退化) vs 外通道(真 prompt + gen0 base 重置) 的多通道均衡, 非纯自吞"。
要求**两锚各自有效 + 通量可测**, 不是"剥 base 后恢复消失"就够 (反题诊断②③)。

## 1 2×2 析因 (单变量铁律, 反题§D)
4 cell 只差 base-reset / real-prompt 两变量; **其余全同** (精度 fp16+manual-LN / seed 集 / N tokens / rep_penalty=3.0 / eval 协议)。
| cell | base | prompt | 含义 | 输出 |
|---|---|---|---|---|
| 00 | gen0-reset | real | 原版 canonical (**matched 重跑, 禁用旧 α=0 链当 control**, §D) | `checkpoints_armb_ABL_00` |
| B0 | prev | real | 剥 base-reset (跑中) | `checkpoints_armb_ABL_baseprev` |
| 0A | gen0-reset | synthetic | 剥 real-prompt | `checkpoints_armb_ABL_0A` |
| BA | prev | synthetic | 真纯自吃 = 决定性 control | `checkpoints_armb_ABL_BA` |
- **禁用旧链当 00** (反题§D): 旧 α=0 链 (g2=105/g9=56) 与新 cell 差≥2 变量 (精度/patch 不确定), 且旧 fp16 baseline 的"驼峰恢复"自身可能 artifact。必须同批 matched 重跑 00。
- Stage-A = 4 cell × {seed1, seed42}; Stage-B (过 gate 才投) = 补 {seed2,3,7} 满 5 seed。

## 2 两测量通道 (反题§F; 缺则只是 reframe 撞§2规则6)
- **channel-2a 冻结 GATE (每链每代硬 abort, 诊断①)**: ckpt sha256 互比**非 bit-identical** + skip/NaN/GradScaler 计数=0 + 梯度非全 NaN。任一链冻结 → 作废重跑或标 artifact, **不进分析**。(prev-mode 让腐败累积, 外观=单调爬升=与"确认"结局同构, 故必须前置 gate。)
- **channel-2b flux 量化 (reframe/贡献 分界)**: per-channel per-gen KL(训练数据 ‖ 模型) 或等价通量, 测两锚各自注入的信息量级。**无 flux, "通量是本质"=叙事非实证。**

## 3 锁定判据 (双向可证伪, 反题§G; 读结果前锁)
**支持多通道 (全部满足)**: B0 **AND** 0A 都使恢复减弱/消失 + BA 最深 + flux 显**两锚各自独立**贡献 + 全链非冻结。
**证伪 (按 D-1 纪律5 记 FALSE, 禁 spin 成新发现)**:
- F1: **0A 无效** (剥 prompt 恢复照旧) → real-prompt 非外锚 = 单通道非多通道。
- F2: **B0 恢复照旧** (g4-g9 像原版回落) → base-reset 非恢复驱动 = D618 中心命题 FALSE。
- F3: **单调爬升与 vanilla Shumailov 退化无法区分** (flux 测不出独立通量) → 被 prior art 占 (诊断②), 无 novel。
- **铁律 (诊断③)**: "驼峰仍在" ≡ 中心命题 FALSE, **不许改标签成"新发现"** (= exp019 险些翻车那一步)。

## 4 子 agent 校验 (D-1 纪律4, 反题§H; 开析因后派)
≥1 Opus 子 agent, 敌意 default-to-refute, 独立验: (a) 冻结 gate 独立复算 (重写 sha256/熵脚本不复用主会话); (b) 因果归因合法性 (4 cell 真只差两锚? control 是 matched 非旧链?); (c) 诊断② 区分"单调爬升≠vanilla Shumailov"是否站得住 (核 Schaeffer 2503.03150/grounded-data)。失败自动撤回; 主会话只能据结果**下调不上调**。

## 5 binding + 红线
- 22 ROCm 必经 manual-LN patch; 单 GPU 串行 (GPU1 核显排除); fp32 confirmatory 可选搬 5060 (PI 关卡 J①), **禁跨 fp16/fp32 混跑当同一析因**。
- 不可再生 (verdict/flux/差异日志/prereg) 立即 rsync canonical; ckpt=22 scratch。
- 红线: 不复活 paradigm-shift/first-DM-instantiation/reflexive-AI; framing 写"对既有可证伪 operationalize/量化补缺"不写"首次提出"; 哲学归 Win+PI; 一凡 priority1 健康。

## 6 概率 + 关卡 (反题§J)
- P(B0 干净非冻结 & 单调不回落) ≈ 75-85% (≠确认多通道, 诊断②)。
- P("多通道均衡"作 novel 量化贡献存活 | 全析因+flux+被占核查) ≈ **15-30%**; 天花板 TMLR/workshop 非主刊。
- PI 关卡: ① fp32 confirmatory 用不用 5060; ② 值不值串行 GPU-天 (Stage-A ~2天先行, 过 gate 再投 Stage-B ~3.3天)。

---
*LOCKED D618。开跑 {00,0A,BA} 与读 B0 g4+ 之前 commit。双向可证伪, "两边都赢"被禁 (诊断③)。*
