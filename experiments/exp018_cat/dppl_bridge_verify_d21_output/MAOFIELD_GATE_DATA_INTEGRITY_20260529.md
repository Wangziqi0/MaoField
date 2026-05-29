# MaoField 数据完整性 GATE — 字节级校验 + 3 anomaly adjudicate + L0 白名单

**Agent**: Opus 数据完整性 forensics agent (zero-context), 7B13 (192.168.31.36)
**任务性质**: 后续 L0 证明的 **GATE** — NO-GO 数据不得 build on
**模式**: read-only (sha256 / ls / python 读 + 跨机 ssh read-only), 0 commit / 0 push / 0 launch
**输出**: 本 md (唯一写文件)

---

## 0. head — 真实日期 binary (D-1 纪律 5 sub-rule)

```
$ date '+%F %T %Z'
2026-05-29 12:10:57 CST
```

确认今日 = **D29 = 2026-05-29**。无陈旧 system reminder 继承。

binding 自检 (任一违反即 flag): paper v8 final 47/47 manifest 不动 ✓ (本 GATE 仅校验未修改) | 12 NOT-claim 撤回不复活 ✓ | D29 三 leg 不动 ✓ | 反题 6 P0★ tier 不擅升降 ✓ | read-only 严守 ✓ (跨机仅 sha256/find/ls, 0 write) | 0 commit / 0 push / 0 launch ✓。

---

## 1. 每 dataset / cluster 一行 binary GO / NO-GO 表

7B13 本地共 **52 jsonl**。逐 cluster 判定:

| Cluster | 代表 jsonl (7B13 路径前缀 `…/exp018_cat/`) | sha256 状态 | 跨机 reconcile | binary |
|---|---|---|---|---|
| **archive 47-manifest** | `archive/v1.0_release_20260516/` (17 jsonl + 30 config/script/src) | **47/47 `sha256 -c` OK** | — (本机 frozen baseline) | **GO** ✅ |
| **cluster 2 alpha-scan** | `logs/armb_alpha{0,1,5,10,50}_seed42_*.jsonl` (9 file) | self-consistent, α=0/1/5/10/50 single-seed | 部分与 archive 同名 (seed42 行) bit-match | **GO** ✅ |
| **cluster 3 phase1_robust (F3 source)** | `logs/host22_backup_20260512/*.jsonl` (10 file, seed 1-4) | 全 10 file 算 sha256 | **10/10 bit-match archive** chain_logs ✅ + 22 机 ssh REACHABLE | **GO** ✅ |
| **cluster 9 candidate_c N=180** | `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` | `a805576f…3f5a57d`; 180 chain_gen_done + 4 run_start + 2 run_end | **22 机活动副本 `/tmp/…` sha256 bit-identical** `a805576f…` ✅ | **GO** ✅ (含 NaN caveat, 见下) |
| **cluster 10 5060 fp32** | `dppl_bridge_verify_d21_output/candidate_c_20260524_173559.jsonl` (+`_20260525_113506` / `_160321`) | `0471359e…` / `b4c93e08…` / `fb7c2741…` | 5060 数据已 sync 7B13; 19 机 ssh REACHABLE 但 Windows path probe 超时 | **GO** ✅ |
| **cluster 11 5060 fp16** | `candidate_c_20260527_220312.jsonl` / `_210536.jsonl` (md 引用) | **本地 ABSENT** (find 0 命中) | 仅在 19 机, batch ssh 不可达该路径 | **NO-GO** ⛔ `[data unverified]` |
| **D-PPL bridge main_D22** | `dppl_bridge_verify_d21_output/main/main_D22.jsonl` | `3478be83…`; 152 tuple_done + 8 tuple_skipped + 1 run_start + 1 run_done | 本机 (D^code_B/C 源) | **GO** ✅ |
| 早期 shumailov D7-8 | `logs/shumailov_{no_preserve,preserve_10pct}_seed42_*.jsonl` (4 file) | self-consistent baseline 复现 | — | **GO** ✅ (baseline, 非 L0 主输入) |
| preflight / fail / abort | `candidate_c_preflight/…203111` (pre_flight=True) / `…170933` (chain_gen_fail) / `…092037` (run_start only) / `pilot_D21_seed1_gen5` | 非数据 (smoke/fail/abort) | — | **EXCLUDE** (非 data, 不进白名单) |

### 跨机 reconcile 状态汇总
- **9070XT (22)**: ssh REACHABLE (hostname `amd-ONDA-B650M-W`)。candidate_c N=180 + phase1_robust seed1-4 全部 **bit-identical** 跨 7B13 ↔ 22。**reconcile CONFIRMED**。
- **5060 (19)**: ssh REACHABLE (Windows host)。fp32 数据已 sync 到 7B13 本地 (cluster 10);fp16 (cluster 11) jsonl **未在 7B13**, 19 机 batch ssh 路径 probe 超时 → **cluster 11 跨机 reconcile pending, 标 `[data unverified]`**, 不阻塞其他 cluster。

---

## 2. 可作 L0 证明 input 的 jsonl 白名单 (GO 列表)

以下 jsonl **GO**, 可 build L0 证明:

1. **`archive/v1.0_release_20260516/chain_logs/*.jsonl`** (17 jsonl, 47/47 manifest OK) — paper v8 final frozen baseline, **最高可信**。
2. **`dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl`** (N=180, 22↔7B13 bit-identical) — α-scan × multi-seed 主链 (含 NaN 子集, 见 anomaly a caveat)。
3. **`dppl_bridge_verify_d21_output/candidate_c_20260524_173559.jsonl`** (5060 fp32 seed42 α0 gen0 = 36.536) — cross-stack 对照权威点。
4. **`dppl_bridge_verify_d21_output/candidate_c_20260525_160321.jsonl`** (5060/9070XT fp32+gc E0, gen0=36.536 + gen1=78.572 lift) — fp32 2-gen disentangle。
5. **`dppl_bridge_verify_d21_output/main/main_D22.jsonl`** (D-PPL bridge, 152 tuple, D^code_B/C)。
6. **`logs/host22_backup_20260512/*.jsonl`** (10 file, phase1_robust F3 source, 全 bit-match archive)。
7. **`logs/armb_alpha*_seed42_*.jsonl`** (9 file, alpha-scan) + **`logs/shumailov_*.jsonl`** (4 file, baseline 复现)。

**NO-GO (不得 build L0)**: cluster 11 5060 fp16 (`candidate_c_20260527_*.jsonl`) — `[data unverified]`, 仅 md table 有, jsonl 7B13 缺失。

---

## 3. 3 anomaly — binary verdict + 判据 + source 行号

### (a) 5 cells bit-identical `93.38780852810248` — 真实数据 vs cache/dedup artifact?

**VERDICT: 真实数据 (frozen-weight artifact, fp16 GradScaler-skip), NON cache/dedup。** ✅

**5 bit-identical cells** (源 `candidate_c/candidate_c_20260522_203837.jsonl`, gen=0):

| seed | α | a1_ppl | val_loss | a3_attn_entropy 全数组 sha256 (前16) | a2_aniso sha256 | a6_ema |
|---|---|---|---|---|---|---|
| 1337 | 10.0 | 93.387808528102482 | 4.5367608070373535 | `4a72d9ef57c783ce` | `b139f47b…` | all NaN |
| 2024 | 0.0 | 93.387808528102482 | 4.5367608070373535 | `333ec551816a68fe` | `ab875b5a…` | all NaN |
| 7 | 10.0 | 93.387808528102482 | 4.5367608070373535 | `c0ca262d0a92f01d` | `5ded72e4…` | all NaN |
| 137 | 0.0 | 93.387808528102482 | 4.5367608070373535 | `f94112c9b2d62fdc` | `ea9d6bb1…` | all NaN |
| 271 | 10.0 | 93.387808528102482 | 4.5367608070373535 | `9ffb0d0e4270ba51` | `3cd00419…` | all NaN |

**判据 (binary)**: a1_ppl/val_loss bit-identical (val_loss 集合 = 单元素 `{4.5367608070373535}`) **但** a3_attn_entropy 全数组 sha256 **5 个全 distinct** (4a72≠333e≠c0ca≠f941≠9ffb), a2_anisotropy 亦 **5 全 distinct**。→ hidden-state forward 跨 5 cells 不同 (~10⁻² scale, 例 a3[0][0]=2.5134 vs 2.5232 vs 2.5174…) 但 eval PPL 坍缩到 bit-identical → **frozen-weight artifact**:fp16 NaN → GradScaler 跳过全部 optimizer step → weight 停在未更新 init 态 → eval val_loss 恒等。若是 cache/dedup, a3 + a2 必亦 bit-identical (反例不成立)。

**机制锚** (binary verify): `a1_ppl = exp(val_loss)` 精确到 bit (`math.exp(4.5367608070373535)` = `93.38780852810248`, 全精度 match)。`a6_ema_divergence` 全 NaN 印证 EMA/contradiction 路径命中 NaN cascade。与 D23/D25/D26 已 surface 的 fp16 GradScaler-skip mechanism **same-source**。

**source 行号**: 记录 schema `scripts/candidate_c_runner.py:402-418` (`a1_ppl`=L408 `float(a1_ppl) if isfinite else None`;`val_loss`=L412)。18 个 gen=0 中:5 bit-identical + 9 None/NaN + 4 distinct (seed42/α0=93.349, 1337/α5=92.666, 7/α5=91.928, 271/α5=91.279)。**caveat**: NaN 子集 (80% 在 D26 audit) 是 fp16 ROCm pathology, **不阻塞 GO**, 但 L0 必须把 NaN 单元当 `[data unverified per-cell]` 处理, 不可当有效 PPL 平均。

---

### (b) N_total 292 vs 1460 step 5× 差异 source (反题 D29 catch)

**VERDICT: paper 的 1460 (steps/generation) 正确。292 = steps/epoch。5× = 5 epochs (no_preserve)。** ✅

**判据 (binary, source-level)**:
- `n_tokens_train = 2390656` (180 records 全恒定, distinct set = `{2390656}`)。
- source: `scripts/candidate_c_runner.py:397-398` →
  `n_tokens_train = len(gen_train_ds) * cfg.dataset.block_size`
  即 **单 generation 的训练 dataset (一 epoch 量) 块数 × block_size**, **NON 代总 / NON epoch 累计**。
- 算式 (全 binary):
  - `2390656 / block_size(64)` = **37354 blocks** (= wikitext-2 train 单 epoch, ≈ 2.39M token)
  - `37354 / per_device_train_batch_size(128)` = 291.83 → **292 steps/epoch**
  - `num_train_epochs = epochs = 5` (no_preserve), source `src/train_one_generation.py:118` (`num_train_epochs=epochs`) + config `configs/cat_arm_b.yaml:127` (`epochs_per_generation: 5`)
  - `292 × 5` = **1460 steps/generation** ✅

**定论**: `n_tokens_train` 语义 = **单 epoch dataset token** (非代总)。故 292 = 步/epoch, **1460 = 5 epoch × 292 = 步/代 = paper 正确值**。5× 差异 source = 严格等于 no_preserve 的 5 epochs。config 行号: `configs/cat_arm_b.yaml` L89 (`per_device_train_batch_size: 128`) + L62 (`block_size: 64`) + L127 (`epochs_per_generation: 5`)。

---

### (c) +57 PPL cross-stack: 36.536 (5060 fp32) vs 93.349 (9070XT fp16)

**VERDICT: 真实 cross-stack divergence (same-config)。GO 作 L0 input。权威对 = 93.349 vs 36.536 = +56.81 / +155.5%。** ✅

**同 config 验证 (binary)**:

| 量 | 9070XT fp16 | 5060 fp32 |
|---|---|---|
| 源 jsonl | `candidate_c/candidate_c_20260522_203837.jsonl` | `candidate_c_20260524_173559.jsonl` |
| config | `cat_arm_b.yaml` (dtype `float16`, L51) | `cat_arm_b_fp32_5060.yaml` |
| seed / α / gen | 42 / 0.0 / 0 | 42 / 0.0 / 0 |
| n_tokens_train | 2390656 | 2390656 (**bit-match**) |
| n_tokens_eval | 16384 | 16384 (**bit-match**) |
| a1_ppl | **93.34934186101** | **36.53597375534** |
| val_loss | 4.536348819733 | 3.598297357559 |

**判据**: seed=42 / α=0 / gen=0 **三者全同**, 训练 + eval 数据量 (ntrain + neval) bit-match。**唯一 differ = dtype (fp16 vs fp32) + 机器 (9070XT vs 5060)**。→ same-config → **真实 cross-stack divergence**, 非混配。

**delta**: 93.349 − 36.536 = **+56.81 abs / +155.5% rel** (即 prompt "+57"; headline 权威对 = 93.349 vs 36.536, **非** misattributed 93.349 vs 36.524)。

**方向锚** (诚实): fp32 = 36.536 ≈ paper pre-registered gen0 baseline (`cat_arm_b.yaml:194` 预测 α=0 gen0≈36), 即 fp32 是数值稳定的**正确**路径;fp16 = 93.349 反映 GradScaler-skip / frozen pathology (与 anomaly a same-source)。L0 用此对作 cross-stack 输入时, 应 framing 为 "fp16 ROCm 数值病态 vs fp32 正确", 不可 framing 为 "两个独立有效测量"。

---

## 4. NO-GO / pending 明确标注 `[data unverified]`

- **cluster 11 5060 fp16** `candidate_c_20260527_220312.jsonl` / `_210536.jsonl`: **`[data unverified]`** — 7B13 本地 ABSENT, 仅 `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER_20260527.md` L46/L129 引用;19 机 batch ssh 路径不可达。**NO-GO, 不得 build L0**。若 L0 需 5060 fp16, 必须先 read-only sync 该 2 jsonl 到 7B13 再 sha256 verify。
- **candidate_c N=180 之 NaN 子集** (18 gen=0 中 9 个 None + 多代 NaN cascade): cluster 整体 GO, 但 **per-cell NaN 标 `[data unverified per-cell]`**, L0 不可纳入有效 PPL 统计。
- **5060 (19) 跨机 reconcile**: fp32 cluster 10 已 sync 本地 (GO);**19 机活动副本 sha256 对照 pending** (Windows path probe 超时), 标 "跨机 reconcile pending, 基于 7B13 本地副本"。

---

## 附: 校验方法 binary trace

- `sha256sum -c archive/v1.0_release_20260516/manifest.sha256` → 47/47 OK (0 mismatch)。
- host22_backup ↔ archive: 10/10 文件名对 sha256 逐一 MATCH。
- 22 机: `ssh amd@192.168.31.22 sha256sum /tmp/dppl_bridge_verify/output/candidate_c/…203837.jsonl` = `a805576f…` = 7B13 本地 (bit-identical)。
- anomaly (a): python json 读 180 chain_gen_done, a3/a2 全数组 sha256 distinctness。
- anomaly (b): `2390656/64/128 = 291.83→292`, `×5 epochs = 1460`;source `candidate_c_runner.py:397` + `train_one_generation.py:118` + `cat_arm_b.yaml:127`。
- anomaly (c): 同 (seed42,α0,gen0) 跨 fp16/fp32 jsonl 对照, ntrain/neval bit-match。

**0 commit / 0 push / 0 launch 严守。本 md 为唯一写文件。**
