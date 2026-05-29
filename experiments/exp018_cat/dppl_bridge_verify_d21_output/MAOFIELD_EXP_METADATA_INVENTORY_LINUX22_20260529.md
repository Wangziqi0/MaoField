# MaoField 实验元数据穷尽 inventory + sha256 trust-but-verify (7B13 + 9070XT/22)

> **本文件性质 (D-1 纪律 5)**: 这是一份**独立验证通道**的穷尽元数据 inventory + 对 prior 文档 (`D29_VERIFICATION_CASCADE_UPDATE_20260529.md`) 关键 sha256 发现的**独立 re-verify** (不只信 prior verdict)。不覆盖任何旧文档。仅记录字节事实 + 元数据 + 与 prior 的一致/不一致。

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期 | **2026-05-29 14:52 CST** (`date '+%F %T %Z'` binary verified) |
| 生成 | 独立 forensics 通道 [额外 agent], zero-context |
| 数据源 | 7B13 (192.168.31.36, 本机 read) + 9070XT (192.168.31.22, ssh **read-only**: sha256/ls/find/python/cat 仅读, 0 write) |
| scope | 仅 7B13 本地 + 22; 5060/19 桌面数据由平行 agent Y 覆盖 (不重叠) |
| binding | read-only; **0 commit / 0 push / 0 launch**; paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; 反题 6 P0★ tier 不擅升降; D29 三 leg 不动; 仅写本 1 个 output md |
| 22 可达性 | **可达** (`amd-ONDA-B650M-W`); `/tmp/dppl_bridge_verify/output/` 完整 (180 ckpt + early-armb ckpt + main, **ephemeral 重启即失**) |

---

## §1 master 元数据 inventory 表 (全 run × 全字段)

下表每行 = 一个 run / cluster。字段缩写: stk=stack(GPU); xfm=transformers 版本; gens=跑满 gen 数; dist=distinct 计数。

### A. 早期 armb 系列 (paper v8 负结果之真实数据基, 2026-05-07~05-12)

| run | 机器/路径 | jsonl | ckpt | seed 集 | α 集 | gen | dtype | stk | 时间 (jsonl ts) | cell | 跑满10gen | 状态 | n_train_blocks | jsonl sha256(前16) | ckpt 结构 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shumailov baseline | 7B13 `logs/` | `shumailov_no_preserve_*` x4 + `shumailov_preserve_10pct_*` | (本地无 ckpt) | 42 | n/a (baseline) | varies | fp16 | 22(9070) | 05-07~05-08 | 多 smoke+full | partial | 真训练 baseline 复现 (Shumailov strict-mirror) | — | (见 archive 不全) | — |
| **armb α0 s42** | 7B13 `logs/armb_alpha0.0_seed42_20260508_144612.jsonl` + 22 static_backup ckpt | 11 行 | 22 `MaoField_static_backup_20260520/.../checkpoints_armb/alpha0.0/no_preserve_seed42/gen0-9` | 42 | 0.0 | 0-9 | fp16 | 22 | 05-08 14:46→19:20 | 10 | ✓ | **真训练** (gen0=36.52→gen9=55.33 collapse) | 37354 | `6b56c46151300935`(manifest) | gen0-9 **10 distinct sha256** |
| armb α1 s42 | 7B13 `logs/armb_alpha1.0_*` | 11 | 22 static_backup | 42 | 1.0 | 0-9 | fp16 | 22 | 05-09 00:04→04:42 | 10 | ✓ | **真训练** (36.52→55.93) | 37354 | `df3024f32749f778` | distinct/gen |
| armb α5 s42 | 7B13 `logs/armb_alpha5.0_*` | 11 | 22 static_backup | 42 | 5.0 | 0-9 | fp16 | 22 | 05-09 04:43→09:21 | 10 | ✓ | **真训练** (36.52→62.91) | 37354 | `284d2fc7042b218f` | distinct/gen |
| armb α10 s42 | 7B13 `logs/armb_alpha10.0_seed42_20260508_192435.jsonl` | 11 | 22 static_backup | 42 | 10.0 | 0-9 | fp16 | 22 | 05-08 19:24→05-09 00:02 | 10 | ✓ | **真训练** (36.52→**91.44**, α10 加重) | 37354 | `c6901cc7a678c6da` | distinct/gen |
| armb α10 s42 (早期失败) | 7B13 `logs/armb_alpha10.0_seed42_20260508_144347.jsonl` | 多行 | — | 42 | 10.0 | 部分 | fp16 | 22 | 05-08 14:43 | 2 | ✗ | 早期 abort (gen0=93.90 未训成, 2 distinct) | — | — | — |
| armb α50 s42 | 7B13 `logs/armb_alpha50.0_*` | 1 (header only) | 22 static_backup α50 | 42 | 50.0 | 0 | fp16 | 22 | 05-09 09:21 | 0 | ✗ | **整链 NaN** (α=50 documented NaN) | — | `303682b65b0a37b4` | — |
| armb α0 s1337 | 7B13 `logs/armb_alpha0.0_seed1337_*` | 11 | — | 1337 | 0.0 | 0-9 | fp16 | 22 | 05-09 15:50 | 10 | ✓ | 真训练 (frozen val? gen0=gen9=36.54, 1 distinct — 见注) | — | — | — |

注: `armb_alpha0.0_seed1337_20260509_155044.jsonl` 10 gen 全报 36.5438 (1 distinct val_perplexity) — 是 v0framework retry 的早期 cell, val 未变 (可能 eval cache 或早期 bug); 不进 paper N=6 multi-seed (那批是 host22_backup s0-s4)。

### B. cluster 3 = phase1_robust multi-seed (paper N≥3 robustness, 22 跑, 2026-05-10~05-12)

| run | 机器/路径 | jsonl | ckpt | seed 集 | α 集 | gen | dtype | stk | 时间 | cell | 跑满 | 状态 | sha256(前16) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| phase1_robust chain | 7B13 `logs/host22_backup_20260512/` + `archive/.../chain_logs/` | 9 chain jsonl + 1 audit(78行) + master.log + outer.out | 22 static_backup α0/α10 s0-4 | **0,1,2,3,4** | **0.0, 10.0** | 0-9 | fp16 | 22 | 05-10 04:58 起, max_retry=3 | 9 chains | mostly ✓ | **真训练** multi-seed; audit 记录部分 job_fail rc=134 + retry | (各 distinct, 见 manifest) |

cluster 3 是 paper v8 multi-seed robustness 之核心 (α=0 n=6 [s0,1,2,3,4,42] / α=10 n≈5)。audit.jsonl 是 orchestration log (mixed JSON+shell, 非标准 per-line JSON), 记 chain_start/job_start/job_fail/job_done + retry。

### C. cluster 9 = candidate_c N=180 (D-PPL bridge verify 链, 22 跑, 2026-05-22~05-26)

| 项 | 值 |
|---|---|
| 机器/路径 | 22 `/tmp/dppl_bridge_verify/output/candidate_c/` (ephemeral) + 7B13 镜像 jsonl `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` |
| jsonl | 186 行 (4 run_start + **180 chain_gen_done** + 2 run_end); 7B13 副本 335356 bytes |
| ckpt | 22 `checkpoints/{alpha0.0,alpha5.0,alpha10.0}/no_preserve_seed{42,7,137,271,1337,2024}/generation_{0-9}` = **180 ckpt** |
| seed 集 | 42, 7, 137, 271, 1337, 2024 (6) |
| α 集 | 0.0, 5.0, 10.0 (3) |
| gen | 0-9 (10) |
| dtype | **float16** (`configs/cat_arm_b.yaml` line: `dtype: "float16"`) ← 冻结/NaN 根因 |
| stack | 9070XT (ROCm) |
| 时间 | run_start 05-22T12:38Z; 跑满 180 ckpt 跨数天 (05-22→05-26); ckpt mtime 05-23~05-26 |
| 每 cell | 中位 inter-ckpt gap (full forward+backward 跑满); per-cell ~34 min 量级 (nohup 进度条 1460 step/gen ~3.5 min/gen × epochs) |
| cell 数 | 18 chain × 10 gen = 180 |
| 跑满10gen | **18/18 chain 全跑满 180 ckpt** ✓ (结构完整, 非中途崩) |
| 状态 | **混合 regime: 9 链全冻 + 3 链真动 + 6 链微动振荡; 0 cell 训到 baseline 36.5; 大量 NaN (a1_ppl=None)** |
| ckpt 结构 | config.json + model.safetensors(500MB) + training_args.bin + tokenizer 全套; **无 trainer_state.json / 无 optimizer.pt** = 裸 save (无法复原 global_step) |
| trainer_state/optimizer/training_args | trainer_state=**无**; optimizer=**无**; training_args.bin=**有** (5905 bytes) |
| nohup.log | 22 `candidate_c.nohup.log`(16.4MB) + `_resume_d24`(6.6MB) + `_resume_d25`(12.8MB); 7B13 副本 `candidate_c.nohup.log`(5.3MB) |
| jsonl sha256 | (180 ckpt sha256 census 见 §2/§3) |

### D. main_D22 = D-PPL bridge 主跑 (7B13 算, 跑在 22 static_backup ckpt 上, 2026-05-22)

| 项 | 值 |
|---|---|
| 机器/路径 | 7B13 `dppl_bridge_verify_d21_output/main/main_D22.jsonl` (162 行) + watchdog.audit (5 行) |
| 输入 ckpt_root | `/home/amd/HEZIMENG/MaoField_static_backup_20260520/.../checkpoints_armb` (= **早期 armb 真训练 ckpt**) |
| seed/α/gen | α∈{0,10} × seed∈{1,2,3,4} × gen∈{0-9} |
| dtype | **fp32** (D-PPL 计算用 fp32, 152 行全 fp32) |
| 结构 | 1 run_start + 8 tuple_skipped (gen=0 path-B 缺 gen-(-1) state, per brief §4.2) + 152 tuple_done + 1 run_done; **0 error** |
| 时间 | 05-22T09:37→10:00Z (~23 min) |
| D 值 | path C: 80 行, **D_code_path_C distinct=73** (min 0.0 max 1.0152); path B: 72 行, **D_code_path_B distinct=72** |

### E. pilot_D21 = D-PPL 桥试运行 (D21, 2026-05-21)

| 项 | 值 |
|---|---|
| 路径 | 7B13 `dppl_bridge_verify_d21_output/pilot_D21_seed1_gen5.jsonl` (4 行) + 22 同名副本 |
| 内容 | α10/seed1/gen5: **D_code_path_B = 0.2962167**, **D_code_path_C = 0.5899820** (= 项目 memory 之 "factor-of-2 范围内" 试运行通过值) |
| dtype | fp32 |

### F. smoke / sanity 群 (7B13 `logs/`, 2026-05-07~05-08)

`logs/` 内 21 个 smoke/sanity 文件: `smoke_test_v1-4` / `smoke_armb_alpha10_v1-2` / `sanity_check_c_signal_{gpt2,opt-125m}` / `sanity_check_kl_{protA,protB,posthoc}` 等 — 全 smoke/sanity, 非定量 run。`*_full_*.log` (1.8-4.1MB) 是 armb 训练完整 stdout。

### G. archive v1.0_release (7B13, 2026-05-16, paper 投稿 release)

| 项 | 值 |
|---|---|
| 路径 | 7B13 `archive/v1.0_release_20260516/` |
| manifest | `manifest.sha256` = **47 行** (= "47-manifest" ✓): 16 chain_logs + 9 configs + 9 scripts + 11 src + README + RELEASE_NOTES |
| chain_logs | 16 armb jsonl (s0,1,2,3,4,42 × α0; s0,1,2,3,4,42 × α10; α1/α5/α50 s42) + phase1_robust audit/master/outer |
| 一致性 | host22_backup ↔ archive chain_logs sha256 **MATCH** (抽验 2 文件逐字节相同) |

---

## §2 §1 ckpt sha256 binary 验证结果 (确认 / 推翻 prior)

**独立 ssh 22 重算 gen=0 model.safetensors sha256 (前16), 与 prior D29 doc §1 互比:**

| cell (gen=0) | prior 报 | 本通道独立重算 | 判定 |
|---|---|---|---|
| (1337, α10) | `b3a67b42504e0c10` | `b3a67b42504e0c10` | ✓ 一致 |
| (2024, α0) | `b3a67b42504e0c10` | `b3a67b42504e0c10` | ✓ 一致 |
| (7, α10) | `b3a67b42504e0c10` | `b3a67b42504e0c10` | ✓ 一致 |
| (137, α0) | `b3a67b42504e0c10` | `b3a67b42504e0c10` | ✓ 一致 |
| (271, α10) | `b3a67b42504e0c10` | `b3a67b42504e0c10` | ✓ 一致 |
| (42, α0) 对照 | `dff908569813f815` | `dff908569813f815` | ✓ 一致 (distinct) |

**结论 (binary)**: prior D29 doc §1 **完全独立确认**, 非推翻。5 cell gen0 ckpt **逐字节相同** (`‖θ_i−θ_j‖=0` 字节事实); (42,α0) distinct。

**C3 (测度论不适定本质) = 退化 (degenerate frozen identity) 独立坐实**, fractal/riddled basin 决定性排除。这不是 judgment call, 是 sha256 字节事实, 双通道 (prior + 本通道) 收敛。**且第三重独立信号交叉确认**: 这 5 个 frozen cell 的 eval metric `a1_ppl` 也是逐字节相同的 `93.38780852810248` (见 §3) — 权重字节相同 → eval 输出相同, 自洽。

---

## §3 早期 armb 真训练 vs candidate_c artifact 的 binary 区别

### 3.1 ckpt sha256 (权重逐代是否变)

| | 早期 armb (paper 基) | candidate_c (最近链) |
|---|---|---|
| 单链 sha256 (a0/s42, gen0-9) | gen0 `9334911665359685` / gen1 `fae9467a4b54b32e` / gen5 `a981219bee0b5272` / gen9 `d5c41e53fe76919b` → **10 distinct** | 9 链 **1 distinct** (10 gen 全同字节); 3 链 10 distinct; 6 链 3-6 distinct (振荡) |
| 全集 distinct hash | 每链权重逐代真变 | **180 ckpt → 仅 52 distinct hash** (与 prior §4 一致) |
| 最大 frozen cluster | — | 单 hash `020badecf014fb6c` 出现 **70 次** (跨多链多代冻结) |
| gen0 distinct (18 链) | n/a | 仅 8 distinct (b3a67b42 覆盖 5 链; 020badec 覆盖 7 链) |

**18 链冻结分布 (本通道独立测)**:
- **9 链全冻 (1 distinct)**: α0/s7, α0/s271, α0/s1337, α5/s42, α5/s137, α5/s2024, α10/s42, α10/s137, α10/s2024 ← 与 prior "9 链全冻" 一致 ✓
- **3 链真动 (10 distinct)**: α0/s42, α0/s137, α0/s2024
- **6 链微动振荡 (3-6 distinct, 在小 hash 集内循环)**: α5/s7(4), α5/s271(5), α5/s1337(5), α10/s7(5), α10/s271(6), α10/s1337(3)

### 3.2 loss / val_ppl (是否训成)

| | 早期 armb | candidate_c |
|---|---|---|
| 字段 | `val_perplexity` | `a1_ppl` |
| gen0 | **36.52** (真 fine-tune baseline) | **91.3-93.39** (停在 base, 从未训成); 多链 a1_ppl=None (NaN) |
| collapse 轨迹 | 36.52→55.33(α0)/55.93(α1)/62.91(α5)/91.44(α10); 单调上升 = collapse | 无有效轨迹 (frozen 平直 / NaN) |
| 训到 baseline 36.5 的 cell | 全链 gen0=36.5 | **0/180** |
| NaN | 真链 0 NaN (NaN 仅 α50 整链) | 大量 (180 中 finite 仅 33, 其余 NaN) |
| distinct val/ppl | 40 distinct (44 gen-rows) = 权重真变 | finite a1_ppl 25 distinct; `93.38780852810248` 出现 5 次 (= §2 frozen-5) |
| n_train_blocks | 37354 (真训练语料) | (frozen, optimizer.step 被 skip) |
| loss 行为 (nohup) | 收敛 | `grad_norm: nan` 持续, loss 卡 ~4.52 不降 (GradScaler skip 实证, 22 nohup 8909 命中 nan/overflow) |

### 3.3 D-PPL distinct (跨层 / 跨 cell 是否有真信号)

| | main_D22 (建在早期 armb 真 ckpt) | (candidate_c 无 D-PPL 主跑) |
|---|---|---|
| D_code_path_C | 80 行 **73 distinct** ← 与 prior "73 distinct D_C" 一致 ✓ | — |
| D_code_path_B | 72 行 **72 distinct** ← prior "72 distinct D_B" 一致 ✓ | — |
| dtype | fp32 | — |

### 3.4 binary 结论

**paper v8 负结果建在早期 armb 系列 (2026-05-08~05-12) 的真训练数据**:
- gen0=36.5 真 fine-tune baseline ✓
- 权重逐代变 (单链 10 distinct sha256) ✓
- loss 收敛 + 0 NaN (真链) ✓
- 完整 collapse 轨迹 (α0→55, α10→91, α 越大越重) ✓
- D-PPL 算出 distinct D_B(72)/D_C(73) ✓

**candidate_c (最近 22 链) 是 frozen/NaN artifact, 不可用于任何定量结论** (混合 regime, 52 distinct hash, 9 链全冻, 0 cell 训成, 大量 NaN)。

→ **paper v8 负结果未被 frozen/NaN artifact confound — 独立确认。** candidate_c 的冻结是 fp16 GradScaler skip 之 ROCm/9070XT 工程 artifact, 与 paper 真数据 (早期 armb, 在同 22 但更早、fp16 但成功跑成) 是两批不同 run。

---

## §4 prior 文档不一致 / 新发现 / 数据缺口

### 4.1 与 prior D29 doc 的一处措辞不一致 (非实质, D-1 纪律 5 surface)

- prior §3 line 53 写 candidate_c ckpt "**裸 save (无 trainer_state / optimizer / training_args)**"。
- **本通道实测**: `training_args.bin` (5905 bytes) **存在** 于每个 gen 目录; 真正缺的是 **trainer_state.json + optimizer.pt**。
- **修正**: 应为 "裸 save (无 trainer_state / 无 optimizer, **有 training_args**)"。不影响结论 (仍无法从 ckpt 复原 global_step / 训练历史, 那需要 trainer_state)。prior §5 line 75 又写 "无 trainer_state / optimizer / **training_args**" 同一笔误。

### 4.2 prior 核心发现全部独立确认 (无推翻)

| prior claim | 本通道独立结果 |
|---|---|
| §1 5 cell gen0 sha256 `b3a67b42` 逐字节相同 + (42,α0) distinct `dff90856` | ✓ 逐字节重算一致 |
| §3 18 链全跑满 180 ckpt | ✓ 18/18 × 10 = 180 |
| §3 config.json 19 distinct md5 | ✓ 19 distinct (1 个 base 出现 18 次 + 18 个 per-gen) |
| §4 180 ckpt 仅 52 distinct hash | ✓ 52 |
| §4 9 链全冻 | ✓ 9 链全冻 (+ 本通道补: 3 链真动 + 6 链振荡 的细分) |
| §4 0 cell 训到 36.5 | ✓ 0/180 |
| §4 早期 armb 真训练 (36.5 / 收敛 / 权重逐代变 / D-PPL 73 distinct D_C + 72 distinct D_B) | ✓ 全部确认 |
| §4 α 效应 (α>0 不缓解, α10 加重, α50 NaN) | ✓ 真链 val_perplexity 确认 (α0→55 / α10→91 / α50 NaN) |

### 4.3 新发现 (prior 未明记)

1. **frozen 之第三重独立信号**: 5 个 frozen cell 不仅 ckpt 字节相同, 其 jsonl 内 `a1_ppl` 也逐字节相同 `93.38780852810248` — 权重 ↔ eval 输出双向自洽, 进一步坐实 frozen (非 sha256 单点假象)。
2. **18 链非二元 (冻 vs 动)**, 是三态: 9 全冻 / 3 真动 / 6 微动振荡 (在 ≤6 个 hash 间循环, 疑似部分 step 偶尔过 GradScaler)。这比 prior "9 链全冻" 更细; 振荡链仍 0 训成 baseline, 不改 "不可定量" 结论。
3. **main_D22 输入 ckpt_root = `MaoField_static_backup_20260520`** (D-PPL 主跑确实建在早期 armb 真 ckpt 上, 非 candidate_c)。这是 paper-真数据与 D-PPL 桥之间的 binary 链接证据。
4. **早期 armb 真 ckpt 在 22 仍在** (`MaoField_static_backup_20260520/.../checkpoints_armb`, α0/1/5/10/50 × s0-4,42), **但 7B13 本地 ABSENT**。

### 4.4 数据缺口 / 丢失风险 (可操作, 留 PI ack)

- **22 `/tmp/` ephemeral**: candidate_c 180 ckpt + **早期 armb 真 ckpt (paper 基!)** 全在 22 `/tmp` 与 `MaoField_static_backup_20260520`, 重启即失 (`/tmp`) / 个人机无 RAID (static_backup)。**7B13 本地无 checkpoint 备份** → main_D22 / D-PPL 当前在 7B13 无法复算 (输入 ckpt 不在本机)。
- **结果 jsonl 已安全** (7B13 `logs/` + `archive/`, 双location sha256 MATCH)。主要要保的是 **model 权重** (复算 D-PPL / 重验 sha256 需要)。
- 建议 (留 PI): rsync 22 的 `checkpoints_armb` (早期真 ckpt) + candidate_c 180 ckpt 到 7B13 RAID1 归档。**优先级: 早期 armb 真 ckpt > candidate_c** (前者是 paper 基, 后者是 artifact)。

---

## §5 不变 + genre (反 inflate 严守)

- paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; 反题 6 P0★ tier 不擅升降; D29 三 leg 不动。
- 本次全部 = 数据完整性 + 元数据 + sha256 字节验证 + 更正, 全 NMI/reproducibility/方法论 genre, 非 Nature 主刊 claim。
- C3 退化 sha256 双通道(+ 本通道第三信号 a1_ppl)锁定 → fractal/riddled 主刊叙事决定性死 (反 inflate, 5/12 + 5/19 同构第三次拦下)。
- 所有 paper-level / venue / tier 判定**留 PI + 关卡 3 反题三方决**, 本通道不擅 declare。0 commit / 0 push / 0 launch。

**生成**: 独立 forensics 通道 [额外 agent], 2026-05-29 CST。一凡 priority 1 健康优先。
