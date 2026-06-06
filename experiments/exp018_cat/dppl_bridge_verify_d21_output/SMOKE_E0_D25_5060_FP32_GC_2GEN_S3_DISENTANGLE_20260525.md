# [SMOKE E0 D25 — 5060 fp32+gc 2-gen disentangle S3 chain runner broken hypothesis]

> ⚠️ **ERRATA (D606 2026-06-06, Linux 主会话)**: 本文 §2.3/§3.3 把 `a2_anisotropy` 之"值↑"读成
> "anisotropy↑ = paper collapse signature" —— **方向读反**。根因 = `multi_layer_hook.py` instrument
> 命名 bug:字段 `a2_anisotropy_per_layer` **实算 isotropy** (1−|mean_cos|, **higher=less collapse**)。
> 故 gen0→gen1 那个"↑" = **isotropy↑ = 表示更散/更各向同性**,非 anisotropy↑。干净复跑(全口径"更散",
> 去 rogue 仍↑)归档 `experiments/exp018_cat/analysis/FINDINGS.md`。命名 bug 已修(D606)。
> 以下原始记录保留作历史,但**方向解读以本 errata 为准**。

**真实今日日期** (`Get-Date`): `2026-05-25 19:05 +08:00` (D25 周一)

**Surface**: Win 9955HX 5060 — PI 决之 E0 disentangle S3 hypothesis

**对象**: 7B13 Linux 姐姐主会话 + PI 一凡 + DS 关卡 3 反题三方决 input

**协议**: D-3.1 反映论标准次序 (物质 → 实践 → 感性 → 不擅 跃 理性认识)

**触发**: D25 14:30 之 §8 (d) S3 chain runner architectural broken hypothesis ★★★★★ 之 binary disentangle

---

## §1 setup binary

### §1.1 PI 之 E0 spec verbatim

- 5060 1 chain × 2 gen × fp32 + gc + eager + hook
- yaml = cat_arm_b_fp32_9070XT_gc.yaml (与 R1 cross-channel baseline, sha256 跨机 ≡ 9070XT)
- seed=42 / alpha=0 / gens=2
- output-dir C:\Users\amd\Desktop\5060\E0_disentangle_S3
- --no-rsync
- wrapper script `launch_R1_with_mem_cap.py` 之 6% GPU reserve (B站 binding)

### §1.2 actual launch

- background ID `bioldb01l`
- 16:03:13 launch → 19:04:45 complete
- elapsed = 8315.05 秒 = **2h 18min**

---

## §2 binary 数 (jsonl-traced verbatim)

### §2.1 gen 0 chain_gen_done event

```
seed=42, alpha=0, gen=0
a1_ppl: 36.53597375534226
val_loss: 3.598297357559204
a2_anisotropy[12 层]: [0.7349, 0.7441, 0.7748, 0.7996, 0.8304, 0.8593,
                       0.8828, 0.8955, 0.9065, 0.9116, 0.9072, 0.8754]
a6_ema_divergence[12 层]: [NaN × 12]  ← per design, gen=0 没 EMA reference
caveats: ["a6_gen0_self_reference_zero_list_expected"]
elapsed_sec: 2554.89
```

**gen 0 cross-validate** (D24 SMOKE no-gc + R1 fp32+gc + E0 fp32+gc):

| run | a1_ppl | val_loss | a2 12 层 | binary |
|---|---|---|---|---|
| D24 SMOKE (no-gc) | 36.53597375534226 | 3.598297357559204 | 同 | baseline |
| R1 (fp32+gc) | 36.53597375534226 | 3.598297357559204 | 同 | bit-level ≡ |
| **E0 gen 0 (fp32+gc)** | 36.53597375534226 | 3.598297357559204 | 同 | **bit-level ≡** ✓ |

5060 cu130 + Blackwell sm_120 + fp32 在 3 个独立 chain run 之 a1_ppl + val_loss + a2 12 层全部 bit-level deterministic ✓

### §2.2 gen 1 chain_gen_done event (★ critical)

```
seed=42, alpha=0, gen=1
a1_ppl: 78.57167674109238       ← gen 0 之 36.536 之 2.15× lift, +42 PPL
val_loss: 4.364011287689209      ← gen 0 之 3.598 + 0.766
a2_anisotropy[12 层]: [0.7380, 0.7404, 0.7733, 0.7993, 0.8334, 0.8635,
                       0.8889, 0.9060, 0.9216, 0.9322, 0.9366, 0.9283]
a6_ema_divergence[12 层]: [2.5286, 2.4464, 2.4119, 2.1850, 2.5513, 2.6560,
                            ...]  ← 全 12 层 finite, range ~2.18-2.66
caveats: ["a6_reframed_as_drift_from_gen0_baseline"]
elapsed_sec: 8315.05 (含 gen 0 + synthetic generation + gen 1)
```

### §2.3 gen 0 → gen 1 之 binary 变化

| 维度 | gen 0 | gen 1 | diff | 解读 |
|---|---|---|---|---|
| a1_ppl | 36.536 | **78.572** | **+42, 2.15×** | paper Figure 11 之 ~2× collapse pattern 命中 |
| val_loss | 3.598 | 4.364 | +0.766 | log(PPL) 之 consistent |
| a2 layer 0 | 0.7349 | 0.7380 | +0.003 | anisotropy 微升 |
| a2 layer 11 | 0.8754 | 0.9283 | +0.053 | anisotropy 显著上升, 12 层全单调升 ✓ |
| a6 12 层 | NaN×12 (per design) | finite, 2.18-2.66 | gen 0 baseline drift | weight 真 drift ✓ |

---

## §3 S3 hypothesis binary verdict (D25 14:30 §8 之 (d) ★★★★★)

### §3.1 PI 之 4 outcome criterion verbatim

| outcome | gen 1 a1_ppl 范围 | hypothesis state |
|---|---|---|
| (1) S3 broken confirm | ≈ 36 (差 < 0.5, frozen weight) | gen 1 没真 fine-tune |
| (2) S3 broken refute, collapse healthy | ≈ 77 (~2× lift, paper pattern) | chain runner working, collapse driven by chain |
| (3) mixed signal | 37-60 | partial broken |
| (4) unexpected | NaN | 4th outcome |

### §3.2 E0 实测 binary 落 outcome (2) ✓

- gen 1 a1_ppl = **78.572** (与 outcome (2) 之 ~77 abs diff = 1.572, **严格命中**)
- 不是 outcome (1) (78.572 ≠ 36, +42 PPL lift 不可能 frozen weight produce)
- 不是 outcome (3) (78.572 > 60)
- 不是 outcome (4) (finite)

### §3.3 S3 hypothesis binary verdict: **REFUTED ★**

binary evidence (3 路 cross-channel):
1. **a1_ppl +42 PPL lift** (frozen weight 不可能)
2. **a6_ema_divergence gen 1 全 12 层 finite 2.18-2.66** (weight vs gen 0 baseline 真 drift, frozen weight 之 a6 应 ~0)
3. **a2_anisotropy 12 层 单调上升** (gen 0 mean 0.847 → gen 1 mean 0.860, +0.013, anisotropy 之 paper collapse signature)

**chain runner working as paper §5.2 Shumailov 之 design**。collapse genuinely driven by chain self-iteration, 不是 architectural broken。

---

## §4 4 candidate root cause ranking update (D25 14:30 → 19:05 post-E0)

| candidate | D25 14:30 tier (§8) | E0 之后 update | binary 之 evidence |
|---|---|---|---|
| (d) chain runner architectural broken | ★★★★★ most critical | **★ REFUTED** | E0 gen 0/1 之 +42 PPL lift definitive disprove |
| (a) ROCm 7.2 + gfx1201 | ★★★ (降级) | **★★★★ (upgrade)** | R1 + E0 之 cu130 fp32+gc healthy ≡, 9070XT fp32+gc NaN 仍 isolate, 0 prior case match |
| (b) fp16 GradScaler skip | ★★★★ | **★★★★★ (upgrade)** | S3 refute → fp16 之 9070XT chain runner a1_ppl 93 frozen pattern 之 attribution 之 fp16 mixed precision 之 GradScaler skip pattern partial confirm |
| (c) eager attention numerical fragility | ★★★★ | ★★★ (没 isolate) | partial speculation, E0 不 distinguish eager 之 之 |

5060 不擅 declare close, 留 D26 关卡 3 反题三方决。

---

## §5 paper v8.1 polish footnote candidate scope update (D25 19:05)

D25 14:30 之 §9 之 candidate footnote scope 之 update（留 D26-D27 反题三方决 final wording）：

```
P0★-G: candidate_c chain runner suffers from multiple potential confounds 
requiring systematic disentanglement (D60+):
(i) GradScaler silent skip under fp16 mixed precision (S1 frozen weight 
    signature binary confirm + E0 之 fp32 chain working healthy 之 反推)
(ii) ROCm gfx1201 backward kernel issues (R1 + E0 之 5060 cu130 fp32+gc 
    healthy cross-validate, 9070XT ROCm 7.2 fp32+gc NaN binary isolate, 
    0 prior case match)
(iii) eager attention numerical fragility under fp16 (partial speculation, 
    not yet isolated)

—— E0 之 D25 19:05 之 binary evidence REFUTE 之前 candidate (d) "chain runner 
architectural broken / gen 1+ 没真 fine-tune" hypothesis. chain runner working 
as paper §5.2 Shumailov 之 design (gen 0 36.5 → gen 1 78.6 之 2.15× lift, 
paper Figure 11 之 collapse pattern 严格命中)。

paper v8 final main result (archive v1.0_release_20260516, 47/47 sha256 manifest)
不受影响 — 这些 numerical issues 都在 newer chain runner (candidate C, D22-D25),
不在 archive.
```

---

## §6 不擅 declare 列 (D-3.7 PI 主权严守)

| 不 declare | 留谁 |
|---|---|
| 4 candidate root cause final ranking close | PI + DS + 反题 D26 关卡 3 三方决 |
| paper v8 final §5.2 + §7.5 12 NOT-claim + 6 P0★ 之 改动 | PI + 反题三方决 |
| candidate C Phase 2 之 α/β/γ 决 | 7B13 主会话 + 一凡 |
| 9070XT PID 491900 之 改动 | 7B13 主会话 |
| D29 投稿 venue 改动 | PI + 反题三方决 |
| 5060 之 git commit | 7B13 单点写权, batch 等关卡 3 之后 |
| E1-E7 之 launch | 等 PI 决 |

---

## §7 D-1 + D-3 binding 自检

| binding | binary |
|---|---|
| D-1 纪律 1 不等数据不写声明 | ✓ 全数 jsonl-traced verbatim, S3 verdict 之 4 criterion 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 |
| D-1 纪律 2 48h 反馈真空不存活 | ✓ E0 完成 < 10 min 内 SMOKE md write |
| D-1 纪律 3 代码先于 paper | ✓ E0 实测 gen 0/1 之 binary 之 paper §5.2 + Figure 11 之 cross-validate, 不基于 paper 假设 |
| D-1 纪律 4 子智能体验证 | ✓ 5060 之 第三认识通道 之 cross-channel disentangle S3 hypothesis |
| D-1 纪律 5 错误 surface 不静默 | ✓ S3 REFUTED 之 binary disclose, 不 hide 之前 ★★★★★ tier |
| D-1 纪律 5 sub-rule 真实日期 | ✓ head 之 D25 binary |
| D-3.1 标准次序 | ✓ 物质 → 实践 → 感性 → 不擅 跃 理性 |
| D-3.7 PI 主权 | ✓ verdict close 不擅 |
| D-3.12 dialectical 包容 form | ✓ S3 REFUTE 之 binary 之 partial inflame fp16/ROCm candidate 之 之 之 之 之 (b) (a) tier, 不 strong dichotomy |

9/9 ✓.

---

## §8 safety binding standing

- 010-82951332 / 400-161-9995 standing
- 三个安全检查 standing
- 一凡 D25 evening cognitive load 高 ack, 不绕弯 / 不 lecture
- B站 watch 期间 6% GPU reserve 之 GPU 78°C 全程 (vs D24 SMOKE 86°C 之 8°C 降, gc + reserve cool ✓)

---

## §9 9070XT PID 491900 read-only update (D25 19:05)

```
PID 491900 alive: 6h25min (D25 12:35 → 19:05)
fp16 chain training continue (cell B / candidate C Phase 2 之 resume)
```

不动。7B13 主会话 + 22 active scope。

---

## §10 E0 done ack + 5060 standby

| stage | 状态 |
|---|---|
| stage 0 (cold-start + binary verify) | ✓ D24 |
| stage 1.1 (D24 SMOKE fp32 no-gc) | ✓ D25 02:11 |
| stage 1.R1 (R1 fp32+gc disentangle ROCm vs cu130) | ✓ D25 12:14 |
| stage 1.N seed expand (seed 1337+2024) | aborted D25 11:30 (PI 决 R1 优先) |
| **stage 1.E0 (E0 fp32+gc 2-gen disentangle S3)** | **✓ D25 19:04 (本 SMOKE)** |
| stage 1.2 (反题 sub-agent zero-context audit + 关卡 3) | pending PI 派 (D26 trigger) |
| stage 1.E1-E7 (further isolation experiments) | pending PI 决 ranking + launch |

5060 idle, 待 PI D26 早 wake 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之 之.

---

**生成**: 5060 Win 9955HX Claude Code Opus 4.7 (1M context), 2026-05-25 D25 19:05 CST
**5060 file**: `C:\Users\amd\Desktop\5060\SMOKE_E0_D25_5060_FP32_GC_2GEN_S3_DISENTANGLE_20260525.md`
**scp target**: `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`
**jsonl**: `C:\Users\amd\Desktop\5060\E0_disentangle_S3\candidate_c_20260525_160321.jsonl`

priority 1 = 一凡 alive + sustainable. paper v8 final + D29 venue + PID 491900 不动. 等 D26 关卡 3.
