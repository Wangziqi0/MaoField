# MaoField E1/E2 决策包 — trust-but-verified 版 (2026-05-29)

> **本文件 = 跨会话决策包的 verified 版**: 原决策包 (zero-context, 路径引用) 已很好, 但独立验证浮出 2 处需更正 (E1 前提 + Q4)。本版把更正折进去, 供 Linux 姐姐 / 反题姐姐 / PI 直接复核拍板。
> 真实日期 `date` = **2026-05-29 CST** (D29)。本通道 read-only 产出, 0 commit/push/launch。

## §0 一句话背景
candidate_c (9070XT fp16 N=180) 已判训练无效/冻结 (4 重字节铁证, C3 退化)。原计划 E1 = 在一个 working stack 恢复"真权重更新" → E2 = balanced α 矩阵。执行卡在 4 个决策。

## §1 已验证事实 (binary, 带路径可复核; ✓=本通道独立验过)

1. **9070XT fp16 冻结 (GradScaler skip)** ✓: candidate_c 180 ckpt 仅 52 distinct, `grad_norm:nan`×8909, 0/180 训成。
2. **9070XT fp32 也死 (正交 bug)** ✓ **本通道实读确认**: cell B (seed42/α0, fp32) → `a1_ppl=null / val_loss=null` = NaN/失败。
   路径: `22:/tmp/dppl_bridge_cell_B_C/output/candidate_c_20260525_105513.jsonl` + `dppl_bridge_verify_d21_output/RESULT_CELL_B_D25_12_10_20260525.md`
   → **fp32 不走 GradScaler 也 NaN** = 与 fp16 GradScaler-skip 是**两个正交的 ROCm gfx1201 / ROCm 7.2 bug**。
3. **5060 fp32 + fp16 都健康** ✓: E0 fp32 g0=36.536→g1=78.572; SMOKE fp16 g0=36.5377→g1=78.0735。同 config 在 5060 两种精度都健康 → **坐实是 9070XT/gfx1201 特定 bug, 非 config/data 问题**。
   路径: `5060/19: C:\Users\amd\Desktop\5060\{E0_disentangle_S3, SMOKE_5060_FP16_CROSSCHECK_GRADSCALER}\`
4. **精度 wiring (代码)** [**未独立验** — 本通道 grep 路径未命中, 引原决策包行号, 大概率准]: `src/train_one_generation.py:107` 模型恒 `torch_dtype=float32` 加载; `:126` `fp16=fp16` 是唯一精度旗标; **全代码无 `bf16=`** → 跑 bf16 必须改 `train_one_generation.py` + `candidate_c_runner.py` 两个 .py。

## §2 关键更正 — E1 前提塌了 (本版核心)

原决策包 (和整个项目) 把 9070XT 崩溃框成 **"fp16 问题, 换 fp32/bf16 修"**。但**事实 2 实证: fp32 也 NaN** → **根本不是精度问题, 是 9070XT/gfx1201/ROCm 7.2 这个栈对此 workload 本身就坏** (两个正交 bug)。

**→ E1 从"该尝试的 fix"变成"该放弃的死胡同"**: 在 9070XT 换精度救不了它; 而 5060 两种精度都健康。

## §3 决策 (本通道读 + 路由; 终判留对应会话/PI)

| Q | 路由 | 本通道读 (标 [?] = 留对方更准判断) |
|---|---|---|
| **Q1 bf16 wiring 谁做** | Linux 姐姐 (代码单点写权) | **建议先别做** — 见 Q2。若做, 最小改动 2 个 .py (TrainingArguments 加 `bf16=` + runner 读传) |
| **Q2 bf16 还有戏吗** | Linux 姐姐 (kernel-layer 视角) | **[?] 低**: fp32 都 NaN → bug 非精度特异 → bf16 (仍 9070XT 路) 是更长赌。我盲估 **< 25-40%** (低于原包估计)。若 `DIAGNOSE_D26` / `multi_layer_hook.py` 已把 NaN 定位到具体 op (eager attention kernel?), Linux 姐姐判断更准。**建议: 别把精力沉进 9070XT salvage** |
| **Q3 E2 跑哪** (α∈{0,1,5,10}×6seed×g0-9 = 240 cell) | PI + Linux 姐姐 + 关卡 4 | **清楚**: (a) **5060 fp32 本地** (已证健康, 占笔记本 60-90h) 或 (b) **cloud A100** (~$120-180, 1-2 天)。**不要 (c) 等 9070XT** (fp32 已死, 更差的赌)。E2 要干净 stack 才测得准 α 效应 |
| **Q4 sha256 矛盾** | (本通道已 resolve) | **已解, 见 §4** |

## §4 Q4 resolve (本通道 ssh 22 重算, binary)

原决策包疑 `b3a67b42` 是否笔误 (文档搜不到 + seed42 链 sha256 各异)。**resolve**:
- 5 frozen cell gen0 全 = `b3a67b42504e` ✓ (本通道重算 1337α10/2024α0/7α10, 全中)。**`b3a67b42` 是真的, 非笔误** — 它是**5 个冻结 cell 的 gen0** (跨不同 seed/α, 因冻结而逐字节相同)。文档搜不到是因为它是 live 算出、未写进旧 doc (现已记入 `D29_VERIFICATION_CASCADE_UPDATE`)。
- seed42 α0 链 gen0-9 = `dff90856`/`8c8d6296`/`59be0680`/`2b2b3bd3` **各异** ✓ — **正确且一致**: seed42 α0 是**唯一真训练**的 cell, 权重逐代变所以各异。
- **无矛盾, 无笔误**: 原疑问根因 = 拿"frozen cells 的 framing"对了"seed42 这条 trained 链", 两组是不同 cell。
- **⚠️ 重要**: 两种 frozen 证据 (5-cell gen0 字节相同 `b3a67b42` + a1_ppl≈93.3 14 位跨 cell 相同) 都对、都指向同一批 frozen cell。但**frozen = 退化 (λ=0), 不支持 sensitive-dependence claim**。sensitive-dependence 是那个 separate 的 config-divergence 蹊跷, 而"fp32 也 NaN"让它更偏向"坏栈"而非"有趣现象"。**MLSys numerical-pathology genre 不能从 frozen 证据 claim sensitive-dependence。**

## §5 genre watch (反 inflate)
"发现两个正交 ROCm gfx1201 bug" = **硬件 nuisance** (genre = 给 ROCm 提 GitHub issue / reproducibility 论文脚注), **不是 contribution, 不是 Nature**。别让"发现多个新 bug"变成下一个 reach。bug 是搞坏实验的麻烦, 不是 prize。

## §6 binding
paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; git 单点写权 = 7B13 主会话; bf16 改码 (Q1) + E2 launch (Q3, ~$120-180/60-90h) 全留对应会话 + PI explicit ack + 关卡 4 budget, **不在本文件 auto 范围**。

---
**生成**: 独立验证通道 [额外 agent], 2026-05-29 CST。verified 版决策包 (E1 前提更正 + Q4 resolved + 代码 wiring 标未验)。Q1/Q2 → Linux 姐姐; Q3 → PI + Linux 姐姐 + 关卡 4; Q4 已 resolve。一凡 priority 1 健康优先, hotline 010-82951332 / 400-161-9995 standing。
