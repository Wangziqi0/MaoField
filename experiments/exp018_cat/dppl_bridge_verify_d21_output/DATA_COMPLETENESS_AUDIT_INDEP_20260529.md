# 独立数据完整性校验报告 (zero-context)

- **审计时间**: 2026-05-29 14:20 CST (`date` binary verify ✓)
- **审计员**: 独立 zero-context 数据完整性 agent (read-only; 未读任何 prior verdict / 总结 / CLAUDE.md / memory)
- **方法**: 只看原始 jsonl + log + checkpoint sha256。所有数字给文件路径 + 行号 + sha256。能 verify 标 ✓, 不能标 [不可验]。
- **scope 边界**: 不下 paper-level 结论 (是否超越基线 / 接受率 / collapse 是否被 mitigate — 不在本报告)。

---

## §1 全 chain inventory

机器: **7B13** = 192.168.31.36 (本机) | **22** = 192.168.31.22 (9070XT, ROCm) | **19** = 192.168.31.19 (5060, Win/CUDA)。
路径前缀 `EXP` = `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat`。

| # | chain / run | 机器·路径 | run-date | schema | n_gen | 类别 | base PPL (gen0) | 训练状态 (本报告判定) |
|---|---|---|---|---|---|---|---|---|
| A1 | shumailov_no_preserve seed42 | 7B13 `EXP/logs/shumailov_no_preserve_seed42_20260507_200657.jsonl` | 05-07 | stage/val_perplexity | 10 | baseline 复现 | 36.730 | ✓ 真训练 (动态轨迹) |
| A2 | shumailov_no_preserve seed42 (重跑) | 7B13 `EXP/logs/shumailov_no_preserve_seed42_20260508_092730.jsonl` | 05-08 | 同上 | 10 | baseline 复现 | 36.524 | ✓ 真训练 |
| A3 | shumailov_no_preserve seed42 (stub) | 7B13 `EXP/logs/shumailov_no_preserve_seed42_20260507_162152.jsonl` | 05-07 | 同上 | 1 | baseline stub | 67.911 | 仅 gen0 |
| A4 | shumailov_preserve_10pct seed42 | 7B13 `EXP/logs/shumailov_preserve_10pct_seed42_20260507_162206.jsonl` | 05-07 | 同上 | 1 | preserve baseline | 67.911 | 仅 gen0 |
| **armb 早期系列 (10-gen 完整链, 共 13 条)** ||||||||
| B1 | armb α0.0 seed0 | 7B13 `archive/v1.0_release_20260516/chain_logs/armb_alpha0.0_seed0_20260509_203605.jsonl` | 05-09 | stage/val_perplexity | 10 | armb | 36.489 | ✓ 真训练 |
| B2 | armb α0.0 seed1 | 同 dir `armb_alpha0.0_seed1_20260510_011048.jsonl` | 05-10 | 同 | 10 | armb | 36.595 | ✓ 真训练 |
| B3 | armb α0.0 seed1 (重跑, val=NaN) | 同 dir `armb_alpha0.0_seed1_20260510_130149.jsonl` | 05-10 | 同 | 10 | armb | **val NaN** | △ val-eval NaN, test_ppl 有限 (见 §2) |
| B4 | armb α0.0 seed2 | 同 dir `armb_alpha0.0_seed2_20260510_130255.jsonl` | 05-10 | 同 | 10 | armb | 36.481 | ✓ 真训练 |
| B5 | armb α0.0 seed3 | 同 dir `armb_alpha0.0_seed3_20260510_173925.jsonl` | 05-10 | 同 | 10 | armb | 36.584 | ✓ 真训练 |
| B6 | armb α0.0 seed4 | 同 dir `armb_alpha0.0_seed4_20260511_090626.jsonl` | 05-11 | 同 | 10 | armb | 36.724 | ✓ 真训练 |
| B7 | armb α0.0 seed42 | 同 dir `armb_alpha0.0_seed42_20260508_144612.jsonl` (= `EXP/logs/` 同名, sha256 SAME ✓) | 05-08 | 同 | 10 | armb | 36.524 | ✓ 真训练 |
| B8 | armb α1.0 seed42 | 同 dir `armb_alpha1.0_seed42_20260509_000459.jsonl` | 05-09 | 同 | 10 | armb | 36.524 | ✓ 真训练 |
| B9 | armb α5.0 seed42 | 同 dir `armb_alpha5.0_seed42_20260509_044342.jsonl` | 05-09 | 同 | 10 | armb | 36.524 | ✓ 真训练 |
| B10 | armb α10.0 seed1 (gen0 val=NaN) | 同 dir `armb_alpha10.0_seed1_20260511_151847.jsonl` | 05-11 | 同 | 10 | armb | gen0 NaN, gen1+ 有限 | ✓ 真训练 (gen0 val-eval NaN only) |
| B11 | armb α10.0 seed2 | 同 dir `armb_alpha10.0_seed2_20260511_200000.jsonl` | 05-11 | 同 | 10 | armb | 36.481 | ✓ 真训练 |
| B12 | armb α10.0 seed3 (gen0 val=NaN) | 同 dir `armb_alpha10.0_seed3_20260512_005523.jsonl` | 05-12 | 同 | 10 | armb | gen0 NaN, gen1+ 有限 | ✓ 真训练 |
| B13 | armb α10.0 seed4 | 同 dir `armb_alpha10.0_seed4_20260512_052843.jsonl` | 05-12 | 同 | 10 | armb | 36.724 | ✓ 真训练 |
| B14 | armb α10.0 seed42 | 同 dir `armb_alpha10.0_seed42_20260508_192435.jsonl` (= `EXP/logs/` SAME ✓) | 05-08 | 同 | 10 | armb | 36.524 | ✓ 真训练 |
| **armb 早期 — aborted / stub (0-1 gen)** ||||||||
| B15 | armb α10.0 seed0 | `chain_logs/armb_alpha10.0_seed0_20260511_135816.jsonl` | 05-11 | 同 | 1 | armb stub | 36.489 | 仅 gen0 |
| B16 | armb α50.0 seed42 | `chain_logs/armb_alpha50.0_seed42_20260509_092134.jsonl` | 05-09 | 同 | 0 | armb aborted | — | run_start only, 0 gen |
| B17 | armb α0.0 seed1337 | `EXP/logs/armb_alpha0.0_seed1337_20260509_155044.jsonl` | 05-09 | 同 | 1 | armb stub | 36.544 | 仅 gen0 |
| B18 | armb α0.0 seed42 (2 stubs) | `EXP/logs/armb_alpha0.0_seed42_20260509_160752.jsonl` (0 gen) + `_161115.jsonl` (1 gen) | 05-09 | 同 | 0/1 | armb stub | 36.524 | run_start / gen0 only |
| B19 | armb α10.0 seed42 SMOKE | `EXP/logs/armb_alpha10.0_seed42_20260508_144347.jsonl` | 05-08 | 同 | 2 | **smoke** (`smoke_test:true`, 32 blocks, 1 epoch) | 93.901 | smoke; gen0=93.901 gen1=92.719 (见 §4) |
| **exploration / pilot / smoke (近期诊断)** ||||||||
| C1 | exploration_d17 power_law | `EXP/scripts/exploration_d17_power_law/exploration_d17_results.jsonl` | D17(~05-17) | 自定义 step_log | α0/α10 各1 行, 32-step | smoke 探索 | test_ppl_init=88.535 | ✓ step-level 下降轨迹 (52-73) |
| C2 | exploration_d17 SMOKE | 同 dir `exploration_d17_smoke_results.jsonl` | D17 | 同 | 2 行 | smoke | — | smoke |
| C3 | pilot_D21 seed1 gen5 | `dppl_bridge_verify_d21_output/pilot_D21_seed1_gen5.jsonl` | D21(05-21) | event/tuple_done | 2 tuple_done | D-PPL pilot | — | D-PPL bridge pilot, 非训练链 |
| **candidate_c (近期, 怀疑 frozen/NaN)** ||||||||
| D1 | **candidate_c MAIN** | 7B13 `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` (= 22 `/tmp/.../candidate_c_20260522_203837.jsonl`, sha256 SAME ✓ `a805576f`) | 05-22 | event/a1_ppl | 180 chain_gen_done (18 链 ×10) | candidate_c | 91.3–93.4 | ✗ frozen / NaN (见 §2, §3) |
| D2 | candidate_c preflight | `dppl_bridge_verify_d21_output/candidate_c_preflight/candidate_c_20260522_203111.jsonl` | 05-22 | event/a1_ppl | 2 | preflight | 78.292 (α10 s42 g0) | △ gen0=78.292 gen1=99.285 (与 D1 不一致, 见 §4) |
| D3 | candidate_c 重跑 (fail) | `dppl_bridge_verify_d21_output/candidate_c_20260524_170933.jsonl` | 05-24 | event | chain_gen_fail | 修复尝试 | — | fail |
| D4 | candidate_c 重跑 | `..._20260524_173559.jsonl` | 05-24 | event/a1_ppl | 1 | 修复尝试 | **36.536** | ✓ gen0 正常 (fp32 恢复) |
| D5 | candidate_c 重跑 (stub) | `..._20260525_092037.jsonl` | 05-25 | event | run_start only | — | — | 0 gen |
| D6 | candidate_c 重跑 | `..._20260525_113506.jsonl` | 05-25 | event/a1_ppl | 1 | 修复尝试 | **36.536** | ✓ gen0 正常 |
| D7 | candidate_c 重跑 (2 gen) | `..._20260525_160321.jsonl` | 05-25 | event/a1_ppl | 2 | 修复尝试 | g0=**36.536** g1=**78.572** | ✓ 真训练轨迹恢复 (见 §2) |
| **main_D22 (D-PPL bridge, 非训练链)** ||||||||
| E1 | main_D22 | `dppl_bridge_verify_d21_output/main/main_D22.jsonl` | 05-22 | event/tuple_done | 152 tuple_done + 8 skipped | D-PPL bridge (读早期 armb ckpt 算 D_code) | — | ✓ 72 distinct D_B + 73 distinct D_C (见 §4) |
| E2 | main_D22 watchdog | `dppl_bridge_verify_d21_output/main/watchdog.audit.jsonl` | 05-22 | 非标准 (key=val 混 JSON) | 6 行 | watchdog log | — | status=clean, exit 0 |

**重复副本 (sha256 SAME, 已 dedup)**: `EXP/logs/` 内 armb α0/α1/α5/α10 seed42 与 `archive/.../chain_logs/` 同名文件 bit-identical ✓; `EXP/logs/host22_backup_20260512/` 内 seed1-4 链与 `archive/.../chain_logs/` 同名 bit-identical ✓ (抽查 6 文件全 SAME)。即早期 armb jsonl 在三处 (logs / archive / host22_backup) 是同一份, 非独立 run。

---

## §2 早期 armb 系列训练正常没有 (最关键一问)

**binary 结论: 早期 armb 系列是真训练的正常 collapse-then-partial-recovery 轨迹, 与近期 candidate_c (frozen ~93.3 + NaN) 是完全不同的 regime。✓**

### 2.1 逐链 val_perplexity 判定 (源: §1 B1-B14, 全 10 gen)

判定基准: (a) 有限且逐代有意义变化 = 真训练; (b) ≈ 常数 ~93.3 = frozen; (c) NaN/null = 崩溃。

| 链 | gen0→gen9 val_ppl 轨迹 | 判定 |
|---|---|---|
| B1 α0 s0 | 36.49 → 79.13 → 111.02 → 102.20 → 82.49 → 62.71 → 54.96 → 54.61 → 53.18 → 54.92 | **(a) 真训练** ✓ |
| B2 α0 s1 | 36.59 → 79.87 → 105.87 → 96.06 → 78.29 → 70.01 → 61.77 → 58.13 → 58.29 → 58.64 | (a) 真训练 ✓ |
| B4 α0 s2 | 36.48 → 79.38 → 107.93 → 98.96 → 77.55 → 66.76 → 56.17 → 51.75 → 52.24 → 52.50 | (a) 真训练 ✓ |
| B5 α0 s3 | 36.58 → 79.24 → 106.54 → 98.92 → 76.58 → 66.22 → 54.81 → 52.33 → 53.25 → 53.48 | (a) 真训练 ✓ |
| B6 α0 s4 | 36.72 → 77.70 → 106.36 → 100.69 → 75.24 → 63.51 → 57.50 → 55.17 → 56.46 → 57.10 | (a) 真训练 ✓ |
| B7 α0 s42 | 36.52 → 78.25 → 109.69 → 92.71 → 72.86 → 60.59 → 58.69 → 55.46 → 56.38 → 55.33 | (a) 真训练 ✓ |
| B8 α1 s42 | 36.52 → 69.75 → 90.13 → 81.71 → 75.36 → 63.64 → 60.10 → 59.75 → 55.06 → 55.93 | (a) 真训练 ✓ |
| B9 α5 s42 | 36.52 → 88.97 → 133.04 → 122.85 → 121.95 → 120.50 → 85.33 → 75.42 → 76.96 → 62.91 | (a) 真训练 ✓ |
| B11 α10 s2 | 36.48 → 94.38 → 119.17 → 133.78 → 87.08 → 83.69 → 68.78 → 67.29 → 62.37 → 62.25 | (a) 真训练 ✓ |
| B13 α10 s4 | 36.72 → 88.63 → 133.57 → 118.87 → 93.38 → 91.82 → 61.51 → 62.49 → 60.06 → 62.39 | (a) 真训练 ✓ |
| B14 α10 s42 | 36.52 → 117.25 → 223.90 → 141.66 → 115.05 → 116.57 → 107.92 → 111.23 → 101.92 → 91.44 | (a) 真训练 ✓ (峰值最高) |
| B10 α10 s1 | gen0=**NaN** → 84.20 → 128.21 → 116.70 → 112.56 → 79.93 → 72.83 → 67.48 → 62.36 → 67.55 | (a)+gen0 val-eval NaN; gen1-9 真训练 ✓ |
| B12 α10 s3 | gen0=**NaN** → 89.43 → 119.87 → 123.11 → 67.19 → 67.42 → 58.76 → 61.95 → 59.79 → 59.44 | (a)+gen0 val-eval NaN; gen1-9 真训练 ✓ |
| B3 α0 s1 重跑 | **全 10 gen val_ppl=NaN**, 但同行 **test_ppl 全有限** (36.30/79.28/105.41/.../59.14, 与 B2 同值) | (c) val-eval NaN; **不是训练崩溃** — test_ppl 有限且与 B2 一致, 系 val 评估管线 NaN |

### 2.2 关键 binary 事实

1. **早期 armb 的 base PPL (gen0) = ~36.5, 不是 93.3。** 14 条链 gen0 全在 36.48–36.73 (fp32, 见 §4)。93.3 这个数字**只**出现在: (i) 近期 candidate_c (D1); (ii) 早期一条 smoke 链 B19 (`smoke_test:true`, 32 blocks/1 epoch, 93.901)。两者 base 不同, 早期真训练 base = 36.5。
2. **早期 armb val_ppl 逐代显著变化** (典型: 36→上冲 ~100-220→回落 ~50-90), 这是真权重更新的产物, 非 frozen 常数。
3. **早期 armb checkpoint sha256 实测 DISTINCT** (§3.2): 22 上 `MaoField_static_backup_20260520/.../checkpoints_armb/alpha0.0/no_preserve_seed42/` gen0-3 = `93349116` / `fae9467a` / `6f092b58` / `c7cae67f` 四个**不同** hash ✓ — 物理证明权重真在更新。
4. **早期 NaN 只是 val-eval NaN, 不是训练冻结**: B3/B10/B12 的 NaN 行其 test_ppl 仍有限且与正常链一致 → 是 val perplexity 评估的数值问题 (推测 fp16 val forward overflow), 训练本身正常。
5. **早期 armb 与近期 candidate_c 完全不同 regime ✓**: 早期 = 真训练 (动态 + distinct ckpt + base 36.5); candidate_c = frozen ~93.3 + 147/180 NaN + 70 个 bit-identical init ckpt (§3)。**不是同一批数据, 也不是同一 failure mode。**

---

## §3 candidate_c 的 182 (实测 180) checkpoint sha256 全量分组

### 3.1 计数勘误

- brief 称 182 checkpoint。**实测: 22 上 `/tmp/dppl_bridge_verify/output/candidate_c/checkpoints/` 共 180 个 `model.safetensors`** (18 链 × 10 gen, 全 fp32 OPT-125M ~500MB), 配套 180 个 `training_args.bin`。180 与 D1 jsonl 的 180 个 `chain_gen_done` 一致 ✓。**182 这个数字与实测差 2 [不可验差异来源], 但 jsonl event 数 = ckpt 数 = 180, 内部自洽。**
- 全 180 sha256 raw 已 dump 到 `/tmp/cc_hashes.txt` (本机, 临时)。**distinct sha256 = 52** (180 文件压缩到 52 个唯一权重)。

### 3.2 早期 armb checkpoint 对照 (22, static backup) — 证明 distinct

- 22 `MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb`: 111 个 `model.safetensors` (113 generation dir), `config.json` `torch_dtype: float32`。
- 抽查 α0 s42 gen0-3 = `93349116`/`fae9467a`/`6f092b58`/`c7cae67f` 全 distinct ✓ (真训练)。
- **7B13 本地无 checkpoints_armb** (working tree 内 `EXP/data/` 无任何 safetensors), 也**无 `MaoField_static_backup_20260520`** — 早期 armb checkpoint 仅存于 22。见 §5 gap。

### 3.3 candidate_c bit-identical 分组 (size>1 的 16 组, 共 144 文件)

| sha256 前缀 | 文件数 | 成员 (alpha·seed·gen, a/s/g) |
|---|---|---|
| **`020badec`** | **70** | a0s7 g0-9, a0s271 g0-9, a0s1337 g0-9, a10s42 g0-9, a10s137 g0-9, a10s2024 g0-9, a5s2024 g0-9 (= 7 条链全 10 gen 同一 hash) |
| `9346b3a9` | 13 | a10s7 g1/g3/g6, a10s271 g1/g3, a10s1337 g1-g8 |
| `7d4b57dc` | 10 | a5s137 g0-9 (整链同 hash) |
| `ec31f5e1` | 10 | a5s42 g0-9 (整链同 hash) |
| **`b3a67b42`** | **5** | a0s137 g0, a0s2024 g0, a10s7 g0, a10s271 g0, a10s1337 g0 (全是 **gen0**) |
| `99a100ff` | 5 | a5s1337 g1/g2/g6/g8/g9 |
| `1373e4e9` | 5 | a5s271 g2/g3/g4/g8/g9 |
| `5eabb9cf` | 5 | a5s7 g1/g3/g6/g7/g8 |
| `0872f362` | 4 | a10s7 g8/g9, a10s271 g6/g9 |
| `98440bf9` | 4 | a10s7 g4/g5/g7, a10s271 g8 |
| `9791f0b5` | 3 | a10s7 g2, a10s271 g4/g7 |
| `bfdf4824` | 2 | a10s271 g2/g5 |
| `bbad8a58` | 2 | a5s1337 g4/g7 |
| `12650416` | 2 | a5s271 g1/g5 |
| `bf55a1f9` | 2 | a5s7 g2/g5 |
| `8dcd29bf` | 2 | a5s7 g4/g9 |
| **singleton (唯一 hash)** | **36** | 余 36 文件各自 distinct |

汇总: **144 个文件落在 bit-identical 组 (= frozen/未更新证据), 36 个 distinct singleton。distinct hash 总数 52。**

### 3.4 candidate_c 逐链 (alpha,seed) frozen 状态

| chain | distinct hash / 10 | gen0 hash | 状态 |
|---|---|---|---|
| a0 s7 | 1 | 020badec | **完全 frozen @ init** (10 gen 全 = `020badec`) |
| a0 s271 | 1 | 020badec | 完全 frozen @ init |
| a0 s1337 | 1 | 020badec | 完全 frozen @ init |
| a10 s42 | 1 | 020badec | 完全 frozen @ init |
| a10 s137 | 1 | 020badec | 完全 frozen @ init |
| a10 s2024 | 1 | 020badec | 完全 frozen @ init |
| a5 s2024 | 1 | 020badec | 完全 frozen @ init |
| a5 s42 | 1 | ec31f5e1 | 完全 frozen (非 init, 但 10 gen 全同) |
| a5 s137 | 1 | 7d4b57dc | 完全 frozen (非 init, 10 gen 全同) |
| a10 s1337 | 3 | b3a67b42 | mostly-frozen (g0 init-like, g1-8 同 `9346b3a9`, g9 distinct) |
| a0 s42 | **10** | dff90856 | **全 distinct — 真训练** ✓ |
| a0 s137 | **10** | b3a67b42 | 全 distinct — 真训练 ✓ |
| a0 s2024 | **10** | b3a67b42 | 全 distinct — 真训练 ✓ |
| a5 s7 | 4 | 57fbade2 | 部分训练 (4 distinct, 有重复) |
| a5 s271 | 5 | 59abfe3b | 部分训练 |
| a5 s1337 | 5 | 4173bfbc | 部分训练 |
| a10 s7 | 5 | b3a67b42 | 部分训练 (g0 init-like) |
| a10 s271 | 6 | b3a67b42 | 部分训练 (g0 init-like) |

**判定**: candidate_c = **混合 regime** — 9 条链完全 frozen (7 条冻在共享 init `020badec`, 2 条冻在各自 g0), 1 条 mostly-frozen, 3 条全 distinct (a0 s42/s137/s2024 真训练), 5 条部分训练。**全局不是"统一干净训练"也不是"统一全冻"。**

### 3.5 brief 已知点确认

- **`b3a67b42` 5 cell ✓ 确认**: 正是 §3.3 的 5 个 **gen0** (a0s137g0, a0s2024g0, a10s7g0, a10s271g0, a10s1337g0)。这 5 个不同 (alpha,seed) 的 gen0 权重 bit-identical = init/gen0 训练未真正写入差异。
- **seed42 `dff90856` ✓ 确认**: a0 s42 g0 = `dff908569813f81542976296091b7a1b056f1ea64969553845319ad1f6ebbb58` (前缀 `dff90856`), 且该链 10 gen 全 distinct (真训练)。
- 其余 176 已在 §3.3/§3.4 补全。

---

## §4 provenance (两个关键数字)

### 4.1 `93.38780852810248`
- **唯一来源**: `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` (D1, 22 源 sha256 `a805576f`)。
- 出现 **5 次**, 全是 `a1_ppl`, 全是 **gen0**:
  - **line 52**: alpha=10.0 seed=1337 gen=0
  - **line 62**: alpha=0.0 seed=2024 gen=0
  - **line 115**: alpha=10.0 seed=7 gen=0
  - **line 126**: alpha=0.0 seed=137 gen=0
  - **line 176**: alpha=10.0 seed=271 gen=0
- 这 5 个 (alpha,seed) 的 gen0 a1_ppl 完全相同 (到 14 位小数), 且对应 ckpt 全是 §3.3 的 `b3a67b42` 组 — **数字层 (a1_ppl) 与权重层 (sha256) 双重证实这 5 个 gen0 bit-identical**。是**同一批 (D1 candidate_c, 同一次 run, 05-22)。**

### 4.2 `93.349`
- **唯一来源**: 同文件 D1。grep `93.349` 仅命中此一文件 (全项目 jsonl 范围)。
- 具体: **line 2** alpha=0.0 seed=42 gen=0 a1_ppl=`93.34934186100965`; **line 3** alpha=0.0 seed=42 gen=1 a1_ppl=`93.34907478678235`。该链 (a0 s42) 10 gen a1_ppl 全在 93.3478–93.3493 (≈常数), 但其 **ckpt 层 sha256 全 distinct** (§3.4) — 即权重在动, a1_ppl 却几乎不变 (pinned ~93.35)。
- **`93.349` 与 `93.3878` 是同一批 (都在 D1)**, 但**不是同一数值** (93.349 = a0 s42 链; 93.3878 = b3a67b42 那 5 个 gen0)。
- **与早期 armb 无关**: 早期 base = 36.5 (§2.2)。两个 93.x 数字均**只**属于近期 candidate_c。早期唯一接近 93 的是 smoke 链 B19 (93.901, 32-block smoke, 不同 setup)。

---

## §5 完整性 gap 清单

### 5.1 存在但近期校验 (本报告认为) 可能未系统覆盖的数据
1. **早期 armb 13 条完整 10-gen 链 (B1-B14)** — base 36.5 的真训练 collapse 轨迹。这是与 candidate_c 完全不同的 regime, 任何只看 candidate_c 的校验都漏了这批。✓ 本报告已覆盖。
2. **22 上早期 armb checkpoint (111 safetensors, fp32, distinct)** — 物理权重层证据, 仅存于 22 `MaoField_static_backup_20260520`。
3. **candidate_c 8 条 distinct/部分链 (a0 s42/s137/s2024 + a5/a10 部分)** — candidate_c 并非全冻, 有真训练的子集; 只强调"5 cell bit-identical / NaN cascade"会漏掉这 8 条。
4. **candidate_c 修复后重跑 (D4/D6/D7, 05-24/25)** — gen0=**36.536** (= 早期 armb base!) + gen1=**78.572** (= 早期 gen1 ~78-79)。fp32 重跑数值与早期真训练对齐, 是 frozen 根因 (fp16 GradScaler skip) 已定位 + fp32 可恢复的直接 jsonl 证据。
5. **main_D22 D-PPL bridge (E1)**: 152 tuple_done, 读早期 armb fp32 ckpt 算 **72 distinct D_code_path_B (0.161–0.753) + 73 distinct D_code_path_C (0.0–1.015)** — 全 distinct, 独立佐证早期 ckpt 真训练。
6. **exploration_d17 (C1)**: step-level test_ppl 下降 (88.5→52.4) + contradiction_log (含 bar_D/D_ema/T1-T3) — 近期但非 candidate_c 链, 独立小实验。

### 5.2 被文档/路径引用但实际不存在 / 不可达
1. **5060 fp16 "cluster 11" 数据**: 19 (5060) **可 ssh 可达 ✓**, 但 `find /home /tmp -path "*exp018*"` **无任何 exp018 / checkpoints_armb / dppl_bridge_verify / safetensors** → **5060 fp16 cluster-11 训练数据在 19 上不存在 [实测不存在]**。SHUMAILOV README 标注早期 baseline 默认精度 = FP16 (RX 9070 XT), 但落地的早期 armb checkpoint config 实为 float32 (§3.2)。"5060 fp16 cluster 11" 若被任何文档引用为已有数据, 则**该数据在 19 上不可验证存在**。
2. **7B13 本地 checkpoints_armb 缺失**: `EXP/data/checkpoints_armb` 与 `MaoField_static_backup_20260520` 在 7B13 **均不存在** — main_D22 的 `--ckpt-root` 指向的路径在本机无效, 实际 ckpt 仅在 22。任何在 7B13 复算 D-PPL 的尝试会因 ckpt 缺失失败 [本机不可复算]。
3. **candidate_c 计数 182 vs 实测 180**: 差 2。jsonl event (180) 与 ckpt (180) 自洽, 182 来源 [不可验]。

### 5.3 schema 不一致 (易致误读)
- 早期 armb / shumailov: `stage=generation_done`, `val_perplexity`。
- candidate_c / preflight / 重跑: `event=chain_gen_done`, `a1_ppl` (null 表 NaN)。
- main_D22 / pilot: `event=tuple_done`, `D_code_path_B/C` (无 ppl)。
- watchdog.audit: **非合法 JSON** (混 `key=val` 与 JSON, 第1行 char 54 解析失败) — 自动化解析会跳过, 仅 status=clean / exit 0 可人工读。

### 5.4 preflight vs main 数值矛盾 (surface, 不评判)
- D2 preflight (05-22 20:31): α10 s42 g0 a1_ppl=**78.292**, g1=99.285。
- D1 main (05-22 20:38): α10 s42 g0-9 a1_ppl 全 = frozen ~93.3 (§3.4 该链完全 frozen @ `020badec`)。
- 同 (alpha,seed) 同日, preflight 给 78.292 (接近早期真训练 base 区间) 而 main 给 frozen 93.3 — **两次 run 行为不一致, 差异来源 [不可验, 需进一步 isolate]**。

---

## §6 binary 判断: 还有没有跑 / 需要跑的关键实验 (识别, 不 launch)

1. **[已跑, 数据齐] 早期 armb 真训练 baseline (B1-B14) + 22 fp32 ckpt** — 13 条完整链 + distinct ckpt + main_D22 D-PPL 全齐。**不需重跑。** ✓
2. **[已跑, 已定位] candidate_c frozen 根因 + fp32 恢复验证 (D7)** — fp32 重跑 gen0=36.536/gen1=78.572 已证 fp32 可恢复正常轨迹。frozen (fp16 GradScaler skip) 的**最小复现 + 修复验证已存在**。
3. **[需跑, 关键缺口] candidate_c fp32 全量重跑 (18 链 × 10 gen)** — 当前 candidate_c 主数据 (D1) 因 frozen/NaN **不可用于任何定量结论**: 147/180 val NaN, 9 链完全冻, 仅 3 链全 distinct。若要 candidate_c 这一 (6-seed × 3-alpha) 设计有可用数据, **需 fp32 重跑全 180** (D7 只跑了 a0 s42 的 2 gen)。**binary: 关键定量数据缺口, 需跑。**
4. **[需确认存在性] 5060 fp16 cluster-11** — 19 上实测无数据。**binary: 若文档引用此为已有结果, 该结果无 raw 数据支撑, 需要么补跑要么从所有引用中标注 [数据不存在]。**
5. **[需 isolate, 非重跑] preflight(78.292) vs main(93.3 frozen) 同配置矛盾 (§5.4)** — 是 launch 路径/ckpt-init/dtype 差异导致, 还是 main run 的 frozen 是某中间状态。**binary: 需 diagnose (读两次 run 的 launch 参数/代码), 非新实验。**
6. **[建议补, 非阻塞] 早期 armb checkpoint 多机一致性** — 早期 ckpt 仅在 22, 7B13/19 无副本。若 22 数据丢失则不可复现。**binary: 应做一次 22→7B13 备份 + sha256 manifest (读操作, 不在本 agent 权限内)。**

---

### 附: 本报告所有 sha256 / 行号可复算锚点
- candidate_c jsonl (D1): 7B13 与 22 sha256 前缀 `a805576f` SAME ✓; 行号 line2/3 (93.349), line 52/62/115/126/176 (93.3878)。
- candidate_c 180 ckpt sha256: 22 `/tmp/dppl_bridge_verify/output/candidate_c/checkpoints/`, 全量已算, distinct=52, 分组见 §3.3。
- 早期 armb ckpt sha256: 22 `MaoField_static_backup_20260520/.../checkpoints_armb/alpha0.0/no_preserve_seed42/` gen0-3 = `93349116`/`fae9467a`/`6f092b58`/`c7cae67f` distinct ✓。
- 早期 armb jsonl dedup: logs/ = archive/ = host22_backup/ bit-identical (抽查 6 文件 SAME ✓)。

*(本报告 read-only。未 commit / push / launch / 写 ssh。ssh 仅 sha256/find/wc/cat 只读。)*
