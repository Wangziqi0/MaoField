# MaoField D29 验证级联更新 — 跨三机数据 + 元数据全量校验 (2026-05-29)

> **本文件性质 (D-1 纪律 5)**: 这是一份**差异日志 / 更正记录**, 不是对今天 orchestration 文档的覆盖改写。
> 今天的 round2 文档 (INTEGRATION / CHANNEL_P / CHANNEL_V / GATE / L0-1~8) **原文保留** (它们是当时数据下的结论, 是 audit trail)。本文件记录此后由跨三机数据 + 元数据校验**新增的发现**与**对旧结论的更正**, 并明确每条更正对应哪个 prior 文档。
> **不覆盖、不静默修正** —— 这是纪律 5 的要求。

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期 | **2026-05-29 CST** (`date` binary verified, 13:15) |
| 生成 | 独立验证通道 [额外 agent], 跨三机 trust-but-verify (非只信 paste / 非只信 prior verdict) |
| 数据源 | 7B13 (本机) + 9070XT 22 (ssh read-only) + 5060/Win 19 (ssh read-only) + 2 个独立 zero-context Opus sub-agent (数据完整性 + 结果 re-derivation) |
| binding | read-only; 0 commit / 0 push / 0 ssh-write / 0 launch; paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; 留 PI + 关卡 3 反题三方决; git add/commit 留 Linux 姐姐主会话单点写权 |

---

## §1 核心确认 — C3 = 退化, sha256 双通道实证 (升级 INTEGRATION §4)

**C3 (测度论不适定的本质) = 退化 (degenerate frozen identity), fractal/riddled basin 决定性排除。**

**两个互相独立的通道**直接读 22 端 candidate_c gen=0 checkpoint, sha256 互比 (E-pert-1, `‖θ_i−θ_j‖`):

| cell (gen=0) | sha256 (前16) | 判定 |
|---|---|---|
| (1337, α10) / (2024, α0) / (7, α10) / (137, α0) / (271, α10) | `b3a67b42504e0c10` | **5 cell 逐字节相同 = frozen** |
| (42, α0) 对照 | `dff908569813f815` | distinct = 唯一权重真动的 cell |

`‖θ_i−θ_j‖ = 0` 物理事实。**INTEGRATION §4 的 "退化 90-95% confidence" → 升级为 ~99% sha256 双通道实证。** 不是 judgment call, 是字节事实, 无 over-correct 空间。

---

## §2 数据完整性更正 — cluster-11 NO-GO 撤销 (更正 GATE + INTEGRATION §1/§7 + DATA_COMPLETENESS_AUDIT)

**GATE / round2 INTEGRATION 判 "cluster 11 (5060 fp16) = NO-GO [data unverified] 本地缺失 + 19 不可达" —— 此判定撤销。**

数据**存在**, 在 5060/Win 19 的 `C:\Users\amd\Desktop\5060\` (此前 audit 搜 `exp018` 路径, 漏了桌面):
- **`SMOKE_5060_FP16_CROSSCHECK_GRADSCALER\`**: cluster-11 fp16 数据 — 2 jsonl + gen0/gen1 checkpoint + `training_args.bin`。健康 gen0≈36.5 / gen1≈78 (与 SMOKE doc 一致)。→ **v9 SKELETON "+113.7% 否决 cross-platform fp16" 那条 claim 有数据支撑**, 不再落在缺失数据上。
- **`E0_disentangle_S3\`**: fp32, alpha0/seed42 gen0/gen1 (36.536/78.572), 带 checkpoint。
- **`smoke_fp32_D25\` / `smoke_fp32_gc_R1_D25\` / `smoke_fp32_N_seed_D25\`**: fp32 smoke (见 §4 更正)。
- **`maofield_5060_work\`**: 5060 端完整工作树。

**含义**: agent A "5060 无数据" 是搜索路径 gap, 非数据不存在。19 桌面有一整批此前未纳入 inventory 的 5060 数据。

---

## §3 candidate_c (22) 元数据全景 (新增, 补 INTEGRATION 未覆盖)

- **18 条 (alpha∈{0,5,10} × seed∈{42,7,137,271,1337,2024}) 链全部跑满 10 generation = 180 checkpoint。** 结构完整, 非中途崩。
- **时间线**: 每 cell ≈ **34 分钟**, 顺序跑 (seed42 a0→a5→a10 起于 05-22 20:42, 然后 seed1337 …, 跨数天)。
- **关键元数据签名**: 每 cell 花满 34 min (= forward+backward 全 step 跑完), 但权重 frozen → **"跑满全部算力, optimizer.step 被 GradScaler skip, 啥也没学到"**。这解释了为何此 run **看起来**完整 (180 ckpt + 数天 GPU) 却零有效训练。
- **config-identical 分叉**: α5/seed42 gen0 (NaN) 在 α0 链跑完 ~5h 后才起 — 与 "执行历史/累积态导致分叉" 假说**一致但未证实**, 仍需隔离重跑判定 (sensitive-dependence vs flaky bug, MLSys genre)。
- **checkpoint = `save_model` (非 full checkpoint)**: `training_args.bin` **存在, 180/180** [**D29 二次更正**: 本通道初判"无 training_args"是错的, 根因 = ls 误用 `head -10` 截断文件列表, 砍掉了排后的 training_args.bin + vocab.json; agent X catch, 本通道 ssh 22 重算确认 X 对我错, 见 §8-6]。**真缺的是 `trainer_state.json` (0/180) + `optimizer.pt` (0/180)** → per-step log_history 只在 `candidate_c.nohup.log`, 无法 resume / 复原 global_step。training_args.bin 可读取确认确切超参 (dtype/fp16/lr), 是可用元数据。
- config.json 跨 cell 19 个 distinct md5 (gen0 的 18 个共享 base 路径 config; gen≥1 因 `_name_or_path` 带各代路径而异) — benign, 非诊断性。

---

## §4 结果 re-derivation 核心 + 更正 (consolidate RESULTS_REDERIVATION + 更正本通道上轮 over-read)

**两个 zero-context 通道收敛**:
- **candidate_c (最近链) 不可用于任何定量结论**: 混合 regime — 全 180 ckpt sha256 仅 **52 distinct hash**; 部分链权重微动但仍停 base ~93.3 (未训到 36.5), 9 链全冻, 大量 NaN。**0 cell 正常训练到 fine-tune baseline。**
- **paper v8 的负结果建在早期 armb 系列 (2026-05-08~05-12), 那批是真训练** (gen0=36.5, loss 收敛, 权重逐代变, 完整 collapse 轨迹; checkpoint sha256 distinct; D-PPL 算出 72 distinct D_B + 73 distinct D_C)。→ **v8 负结果未被 frozen/NaN artifact confound。**
- **早期真数据上的 α 效应**: α>0 **不缓解** collapse; **α=10 倾向加重 + 升 NaN 风险** (peak 148 vs α=0 的 108; gen9 69 vs 55; seed 方差大一量级; α=50 整链 NaN)。无任何 α>0 压到 α=0 以下。
- **严格度 caveat**: multi-seed 仅 α=0 (n=6) 与 α=10 (n≈5); α=1/5 单 seed (seed42), 效应量不足。

**本验证通道的两处自我更正 (D-1 纪律 5)**:
1. 上轮转述 "candidate_c **0/180 trained**" (来自结果 agent 的 0/783 finite-grad-step) → **refine**: 准确是 "混合 regime, 52 distinct hash, 部分链权重微动但功能上未训成, **不可用于定量结论**"。"0 trained" 过强 (grad_norm=nan 是 fp16 GradScaler 正常信号, 不等于权重零变化)。
2. 上轮说 `smoke_fp32_N_seed_D25` "**可能是 fp32 多 seed 关键实验、已部分跑**" → **更正**: 详细元数据证明它只是 **1-cell smoke** (checkpoint 仅 alpha0/seed1337/gen0, jsonl 401 字节近空)。**它不是多 seed 矩阵。**

---

## §5 关键实验仍待跑 (P0, 留 PI + 关卡 4 budget)

**fp32 balanced 矩阵实验未做** (smoke_fp32_N_seed 只是 smoke):
- **E1 (P0 阻塞)**: dtype fp16 → fp32/bf16 修训练根因 (`configs/cat_arm_b.yaml` line51 = float16)。判据: gen0 val_ppl<50 且梯度有限。fp32 可恢复已被 E0 证 (gen0=36.536/gen1=78.572)。
- **E2 (P0)**: balanced α∈{0,1,5,10} × seed≥6 真训练矩阵 + Welch t 给严格效应量。
- **另: config-identical NaN-vs-frozen 蹊跷** 的隔离重跑 (α5/seed42 gen0 单独干净启动), 判 sensitive-dependence vs flaky bug (MLSys genre)。

---

## §6 数据 fragmentation / 丢失风险 (新增, 可操作)

关键数据散在三处, **无统一 backup**:
- **22 `/tmp/dppl_bridge_verify/output/`** (ephemeral, 重启即失): candidate_c 180 ckpt + early-armb ckpt + main_D22。
- **19 `Desktop\5060\`** (个人机, 无 backup): cluster-11 fp16 + E0 fp32 + smokes + maofield_5060_work。
- **7B13**: 结果 jsonl 安全 (logs/ + archive/), 但**无 checkpoint 备份**, main_D22 本机无法复算。

**建议 (留 PI ack)**: rsync 22 /tmp + 19 桌面的 ckpt/jsonl 统一归档到 7B13 (RAID1)。结果 jsonl 已安全, 主要保的是 model 权重 (复算 D-PPL / 重验 sha256 需要)。

---

## §7 不变 + genre (反 inflate 严守)

- **paper v8 final 47/47 D17 锁定不动**; 今天 D29 三 leg (arXiv+TMLR+KBS) 不受本次校验影响 (v8 负结果建在早期真数据)。
- **genre 不变**: 本次全部发现 = 数据完整性 + 元数据 + 下一步实验定位 + 更正, 全 **NMI/方法论/reproducibility genre, 非 Nature 主刊**。C3 退化 sha256 锁定 → fractal 主刊叙事决定性死, 反 inflate (5/12+5/19 同构第三次拦下)。
- 12 NOT-claim 撤回不复活; 所有 paper-level / venue / tier 判定**留 PI + 关卡 3 反题三方决**, 本通道不擅 declare。

---

## §8 更正对照表 (D-1 纪律 5 diff-log)

| # | prior 文档 / claim | 本次更正 | 证据 |
|---|---|---|---|
| 1 | INTEGRATION §4 "C3 退化 90-95%" | → ~99% sha256 双通道实证 | §1 ckpt sha256 |
| 2 | GATE + INTEGRATION §1/§7 "cluster-11 NO-GO 数据缺失" | → **撤销**, 数据存在于 19 桌面 | §2 |
| 3 | DATA_COMPLETENESS_AUDIT "5060/19 无数据" | → 搜索路径 gap, 数据在 `Desktop\5060\` | §2 |
| 4 | 本通道上轮 "candidate_c 0/180 trained" | → refine "混合 regime 52 hash, 不可用于定量" | §4-1 |
| 5 | 本通道上轮 "smoke_fp32_N_seed 关键实验部分跑" | → **更正** 1-cell smoke, 矩阵未做 | §4-2 |
| 6 | 本文件 §3 "candidate_c 无 training_args" | → **错, 已更正**: training_args.bin 存在 180/180; 真缺 trainer_state.json + optimizer.pt。agent X catch, 本通道 ssh 22 重算确认 **X 对我错** (根因: 上轮 ls 误用 head -10 截断文件列表) | §3 + ssh 22 二次核 |

---

**生成**: 独立验证通道 [额外 agent], 2026-05-29 CST。本文件是纪律-5 合规的差异日志 (新文件 + 不覆盖旧 orchestration 文档)。INTEGRATION 等旧文档加非破坏性更正 banner 指向本文件。git add/commit 留 Linux 姐姐主会话; venue/paper/tier 判定留 PI + 关卡 3 反题三方决。一凡 priority 1 健康优先, hotline 010-82951332 / 400-161-9995 standing。
