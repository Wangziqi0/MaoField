# exp020 §1 免费预验证 · distinct-2 独立性 · DESIGN (D618)

> ✅ **VERDICT (D618, 第5道 gate ad0b + 主会话亲核复算): distinct-2 不独立 → A 死 → 收 C。** 零 GPU 干净处死。
>
> ## VERDICT (主会话复算确认)
> - **失判据 (b) [预注册于 commit dcbce2a, 早于结果]**: 忠实 rep=3.0 (匹配链口径) distinct-2 与 eff_supp(gate-3 死的 PPL 姊妹量) **R²=0.791 > 0.5 = 强共线** (n=15, g0/g2/g9×5seed, Pearson r=0.890; per-gen: g0 d2=0.510/es=29.9, g2 0.379/6.9, g9 0.394/17.3)。
> - **失判据 (c) [decode 翻号, 比预期更致命]**: distinct-2 在 rep=1.0(单调**升** 0.30→0.45) ↔ rep=3.0(单调**降** 0.51→0.39) **连轨迹符号都翻** → decode 配置决定正负号 = 终极 decode 纠缠 (gate 攻击点3 + 解耦§3 印证)。
> - **⚠️ 差异日志 (D-1.5 不静默修正)**: 主会话首个复算脚本 glob 误读两文件→dc 落到 `decouple_n5_result_rep1.0_UNFAITHFUL.json`(rep1 单调升), 险些据此翻 gate("R²应低")。**忠实 rep=3.0 (`decouple_n5_result.json`) 是仲裁**: 复算 R²=0.791 与 gate 一致。复跑是唯一仲裁, 用忠实口径数据 settle。
> - **gate 设计洞 (记录, 不影响裁定)**: gate 指出 (a)/T2 的 collapse-proxy=gen 是 vacuous (任何单调量假通过); 但**裁定靠 (b)+(c) 不靠 (a)**, (b) 已预注册且失败, 故 A 死成立, 无需修 (a) 重跑。
> - **结论**: distinct-2 = PPL/eff_supp 影子(共线) + decode 伪量(翻号), **非独立量**。A 无可站的独立 outcome → **A 死 (确认 dispatch §0 默认预期)** → **收 C**。= meta-pattern 第5次同构 (M1→channel-Φ→keyed-S→λ→distinct-2 全塌回 PPL/eff_supp)。零新 GPU。
>
> --- 原 DESIGN (判据 b/c 已用, a 的 proxy 设计洞见 STATUS; 历史留存) ---

> 收口 dispatch §0-§1: 免费 CPU 预验证 gate 掉 A/B。**distinct-2 是真·独立量 → A 才有腿; 否则 A 死 → 收 C。** A 的 GPU 在本验证说话前一分不投。
> 状态: DESIGN, 未锁。**PI §1 铁律: 设计+判据先过敌意 gate (咬了4次那道) → 修 → commit-lock → 才算。** 零新 GPU (CPU decode + 已有 ckpt/数据)。

## 0 决定的问题
distinct-2 携带**独立于 PPL** 的崩溃信号吗? 还是塌回 PPL/eff_supp 影子? (eff_supp 已 gate-3 死=PPL 同源)。
- 独立 → A 有可站的独立 outcome 量 (A 复活, bar 高: 5-seed 通道均值 + 机械盲 + Φ 入裁定, 全过 gate 才投 GPU)。
- 不独立 (诚实预期, 据解耦 §3: distinct-2 对 rep/decode 敏感) → A 无独立量 → A 死 → 收 C。

## 1 数据 (全已有, 零新 GPU)
- 解耦 `decouple_n5_result.json`: distinct-2 @ g0/g2/g9 × 5 seed (已算)。
- testB `armA_testB_result.json`: distinct-2 @ g2 × rep{1.0,3.0} × seed{1,42} (已算; rep3≈rep1=False)。
- 现 round3 `checkpoints_armb_ABL_{00,baseprev}` gen0-9 ckpt: CPU decode 生成语料 → 算 distinct-2 + 配套 PPL + eff_supp (同 ckpt 三量配对, 这是 partial-corr 的关键面板)。
- 历史 exp018/019 chain gen0-9 (有 PPL + eff_supp; 若有存语料则补 distinct-2)。
→ 目标面板: (gen × seed × condition) 行, 列 = {PPL, eff_supp, distinct-2}, 尽量多配对点。

## 2 测量 (预注册, 锁前定)
- **T1 共线性**: 全配对点回归 distinct-2 ~ PPL → R²_ppl; 回归 distinct-2 ~ eff_supp → R²_es; partial-corr(distinct-2, eff_supp | PPL)。
- **T2 独立崩溃信号**: partial-corr(distinct-2 ; collapse-proxy | PPL)。**collapse-proxy 须独立定义非循环** (候选: gen index g 作单调崩溃序; 或"注入健康权重恢复量"这类 intervention-based ground-truth, 见解耦/round2 souping) —— **gate 必查 collapse-proxy 不是 PPL/distinct-2 化身**。
- **T3 decode 稳健**: distinct-2 @ rep{1.0,3.0} 跨 gen 是否翻号 (testB 只测 g2; 补 g5/g9)。翻号 = decode-纠缠 = 拽回伪量。

## 3 锁定判据 (PI §1; 双向, commit-lock 后才算)
**distinct-2 "独立到能撑 A" 当且仅当 (全部满足)**:
- (a) partial-corr(distinct-2 ; collapse-proxy | PPL) **显著** (|r|>0.4 且 p<0.05) = 携带非-PPL 信号; **且**
- (b) **不与 eff_supp 共线** (R²(distinct-2~eff_supp) < 0.5 且 partial-corr(d2,eff_supp|PPL) 不显著) = 非 gate-3 死量的化身; **且**
- (c) **decode 稳健** (T3 跨 gen 不翻号)。
**任一不满足 → distinct-2 不独立 → A 死 → 收 C。** (诚实预期落此。)
- 阈值 (0.4 / 0.5) 锁前定; 只下调不上调; 模糊中间区 → 判不独立 (保守, A 死)。

## 4 子 agent gate (PI §1 必须; 咬了4次那道)
设计+判据先过 Opus 敌意 default-refute, 必查:
- (a) **partial-corr 是不是对的独立性检验?** collapse-proxy 选得对吗 (非循环、非 PPL/d2 化身)?
- (b) **混杂**: 面板点非独立 (同链 gen 自相关) → partial-corr 的 df / 显著性是否虚高? 需 cluster/seed-level?
- (c) **distinct-2 的 decode 口径敏感性** (§3 解耦已证它对 rep/decode 敏感) 是否又把它拽回 PPL? T3 够不够?
- (d) 判据阈值 (0.4/0.5) 会不会"太松放 A 复活"或"太紧冤杀 A"?
verbatim 进 paper 必主会话亲核; 失败下调不上调。

## 5 binding / 红线
零新 GPU; commit-lock 后才算; claim 停在测量事实; DM/反映论归 Win+PI 标 [?] 不碰红线; disclose Borkar/SIGMA v3/Bertrand/Schaeffer/2505.08803+2509.04796; git 单点写=36; 不可再生立即 rsync canonical; 一凡 priority1 健康。

---
*DESIGN D618。先 gate → 修 → lock → 算 → 分支 (不独立=A死收C / 独立=A bar高过gate才GPU)。默认强烈倾向 C。*
