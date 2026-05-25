# [9070XT SURFACE — Candidate C Phase 2 NaN explosion 严重 surface]

**真实今日日期** (`date '+%Y-%m-%d %H:%M:%S %Z'`): `2026-05-23 10:35 CST` (D23)

**Surface**: 9070XT Claude Desktop (Remote Control by Win 9955HX 一凡接管)

**对象**: 7B13 Linux 姐姐主会话 + 一凡 D23 早 wake 后的 binary 决 input

**协议**: D-1 纪律 5 (错误 surface 不静默修正) + D-3.1 反映论实践 surface evidence

**状态**: Phase 2 candidate C 已跑 14 小时, 27/180 chain_gen_done (15%), 训练全程 fp16 NaN explosion, model weights 冻结, jsonl 的 PPL 全部 invalid

---

## §1 D-1 纪律 5 binary disclosure

D23 早 wake monitor Phase 2 progress 时 catch 到严重 issue, 立即 surface, 不静默修正:

| binary 指标 | 实际 @ D23 10:34 CST | 期望 |
|---|---|---|
| chain_gen_done count | 27 / 180 (15%) | 27 应 valid |
| 第一 chain (seed=42, α=0): a1_ppl 10 gen | **全 93.35** (冻结) | gen 0 ~93 ballpark + 后续 gen 的 drift |
| 第二 chain (seed=42, α=5): a1_ppl 10 gen | **全 None (NaN)** | finite float |
| 第三 chain (seed=42, α=10): a1_ppl gen 0-6 | **全 None (NaN)** | finite float |
| 训练 loss / grad_norm | `loss=0.0, grad_norm=nan` | finite |
| contradiction loss | `D_n=nan, T1_velocity=nan, loss=nan` | finite |
| Python 进程状态 | PID 267111 still alive (Rl, 132% CPU, 14h elapsed) | active |

---

## §2 nohup log verbatim trace (D23 10:32 的 tail, seed=42 × α=10 × gen=7 的 epoch 3.6-3.94)

```
{'loss': 0.0, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 3.6}
{'contradiction/D_n': nan, 'contradiction/delta_D': nan, 'contradiction/D_doubleprime': 0.0,
 'contradiction/D_ema': nan, 'contradiction/volterra_sum_K': 0.0,
 'contradiction/T1_velocity': nan, 'contradiction/T2_replace': 0.0,
 'contradiction/T3_memory': nan, 'contradiction/loss': nan,
 'contradiction/alpha': 10.0, 'epoch': 3.6}
{'grad_monitor/g_n': nan, 'grad_monitor/delta_g': nan, 'grad_monitor/g_doubleprime': nan,
 'grad_monitor/g_ema': nan, 'grad_monitor/memory_g': nan,
 'grad_monitor/relu_g_doubleprime': 0.0, 'epoch': 3.6}
```

---

## §3 jsonl 的 27 chain_gen_done summary (binary, jsonl-traced)

```
seed=42, α=0.0:    10 gen done, a1_ppl 全 93.35    (冻结, 与 base model PPL 一致)
seed=42, α=5.0:    10 gen done, a1_ppl 全 None    (NaN, eval_loss=NaN → math.exp 返 nan → json null)
seed=42, α=10.0:    7 gen done, a1_ppl 全 None    (NaN, gen 7 进行中)
```

caveats 字段全是 sub-agent A 的 a6 reframe note (`a6_gen0_self_reference_zero_list_expected` / `a6_reframed_as_drift_from_gen0_baseline`), sub-agent A 的 honest caveat 但 **没 catch NaN explosion 这个 critical issue**.

---

## §4 root cause hypothesis (binary surface, 不 declare)

### §4.1 主 hypothesis: fp16 numerical instability + scaler step skip

paper v8 的 `cat_arm_b.yaml` 配置 fp16=True. fp16 training 的 known issue:
- forward 的某 intermediate activation 超 fp16 range (65504) → inf
- contradiction loss (Volterra K=9 的 product sum) 的 numerical amplify → NaN
- HF Trainer 的 scaler detect NaN → skip optimizer.step()
- model weights 不 update → 全 10 gen 的 chain 跑 = 跑 base model 10 次 → PPL 冻结

α=0 的 baseline 不 trigger contradiction loss (alpha=0 的 short-circuit, contradiction_alpha > 0 才 compute), 但 loss=0.0 + grad_norm=nan 同样出现 → fp16 training 的 lm_loss 本身 underflow.

### §4.2 次 hypothesis: AMD ROCm gfx1201 的 fp16 边界 case

D21 install 阶段 surface 的 verdict B-2 (HSA_OVERRIDE GPU Hang) 的 partial 同根. ROCm 7.2 的 gfx1201 native wheel 的 fp16 forward numerical behavior 与 CUDA fp16 可能不严格一致 (autocast 边界 case).

pre-flight self-test 用 **CPU mode** + fp32, 未 catch GPU fp16 NaN issue → D-1 纪律 4 子协作者验证矩阵的 gap surface.

### §4.3 第三 hypothesis: contradiction loss 的 Volterra K=9 numerical instability

paper v8 的 D17 catch 的 dialectical upgrade: `T_2_form="quadratic"` + `kl_history_K=9` 的 Volterra path-dependent. K=9 product / sum 的 amplify factor 在 fp16 range 内的 instability 可能 surface.

---

## §5 三选 (binary, 等 一凡 + 7B13 决)

### (α) kill + escalate + 重 launch

- 立即 kill Phase 2 (PID 267111)
- escalate 给 7B13 sub-agent A debug iteration:
  - fix proposal 1: fp16 → fp32 (cat_arm_b.yaml 的 fp16=False, ~2× wall-clock, ~30h ETA)
  - fix proposal 2: scaler config 调 (init_scale 降低 + growth_factor 改)
  - fix proposal 3: contradiction loss numerical stability (gradient clip + nan-to-num + Volterra K=9 降至 K=3)
  - fix proposal 4: pre-flight self-test expand 到 GPU mode + α=10 numerical edge case
- 7B13 sub-agent A 的 fix relay + 9070XT 重 launch (~30h-40h ETA)
- **cost**: 已跑 14h waste, 新一轮 ~30h, 总占 D23-D25 大部分

### (β) continue + collect NaN evidence

- 不 kill, Phase 2 跑完 ~15h 总 wall-clock (剩 ~1h)
- 全 180 chain_gen_done 的 NaN data 作 **paper v8.1 footnote 候选 evidence**: "single-axis mitigation framing 的 epistemic exhaustion: paper v8 chain training fp16 在 5/6 的 α 层 NaN explosion, mitigation framing 的 fp16 fragile 的 binary 证据" (D-3.12 dialectical inclusive form 的 partial instantiate)
- **risk**: 收集 NaN data 的数学 / 哲学 implications 在 paper v8.1 footnote 中的 contribution 之 questionable (是否真的 paper-level value, 还是 sub-agent A 的 deliverable bug 的 frame confound)
- **caveat**: 与 D-3.7 PI 主权 binding 的 binary alignment 待 PI 决

### (γ) abort + retract candidate C + 之后 cloud A100 fp32

- kill Phase 2
- 不在 9070XT 重 launch (fp16 + ROCm gfx1201 numerical 不可靠 surface)
- retract candidate C 的 9070XT execution, 改 fp32 + cloud A100 (D60+ Phase 5 piggyback)
- **cost**: paper v8.1 polish footnote D27-D45 timeline 之 partial reverse, candidate C 改 cloud A100 之 cost (~$50-100 + 4-7 天 wall-clock)
- **paper timeline implications**: 一凡 + Linux 姐姐 + DS + 反题 三方决 scope

---

## §6 9070XT Claude 的 honest recommendation (不 unilateral 决)

**(α) > (β) > (γ)** 的 sequence 之 default. 理由 binary:

- (α) fp32 重 launch 是直接 fix, ~30h cost 在 D23-D25 之 一凡 evening sleep window 可 cover
- (β) collect NaN data 的 contribution 是 questionable, NaN 本身的 mitigation framing exhaustion 之 evidence 与 sub-agent A 的 deliverable bug 的 frame confound (D-1 纪律 4 子协作者验证矩阵的 gap 才是 NaN explosion 的真正 root, 不是 mitigation framing 之 epistemic exhaustion)
- (γ) retract candidate C 之 9070XT execution 的战略 implications 是 PI + 反题三方决 scope, 不在 sub-agent 决
但 binary 决留给 一凡 + 7B13 Linux 姐姐 + (若 需) 反题 sub-agent zero-context audit.

---

## §7 9070XT Claude 当前 standby (不擅自 kill)

- Phase 2 的 Python PID 267111 continue running (D-1 纪律 5 严守, 不静默 kill, evidence preserve)
- 27 chain_gen_done 的 jsonl 已 push 7B13 ✓
- nohup log 与本 surface md 一并 push 7B13
- 等 一凡 + 7B13 binary 决 (α / β / γ)

---

## §8 D-1 + D-3 binding 严守 ack (本 surface 自检)

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ 27 chain_gen_done jsonl-traced, 所有 NaN 数字 verbatim |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ NaN catch 后 5 min 内 surface md write + push |
| D-1 纪律 3 (代码先于 paper) | ✓ 实践 (chain training fp16 NaN) surface 先于理论 declare |
| D-1 纪律 4 (子协作者验证) | ✓ 本 surface 是 D-1 第四纪律的 binary instantiate (9070XT Claude 主 session catch sub-agent A pre-flight gap, 第二认识通道) |
| D-1 纪律 5 (错误 surface 不静默修正) | ✓ NaN catch 后立即 surface, 不 hide, 不 unilateral kill |
| D-1 纪律 5 sub-rule (真实日期) | ✓ head line `date` 输出 verbatim print |
| D-3.1 物质 → 实践 → 感性认识 | ✓ chain training NaN 是实践 surface, 不 hide; 之后理性认识阶段判 root cause |
| D-3.2 抓出 1 (哲学 outcome 不 starting form) | ✓ 不 declare "mitigation framing wrong" / 不 declare "paradigm shift" / 仅 surface raw NaN evidence |
| D-3.2 抓出 2 (自发 含 multi-agent binding) | ✓ NaN catch 后立即 escalate, 不 unilateral fix |
| D-3.7 PI 主权 binding | ✓ 不 unilateral 决 α/β/γ, 等 PI + Linux 姐姐 决 |

---

## §9 sub-agent A pre-flight self-test gap surface (D-1 纪律 4 expand 候选)

D21 教训 + D22 DIRECTIVE §3.1 之 sub-agent A pre-flight self-test mandate, 但 D22 的 pre-flight self-test 用 **CPU mode + fp32**, 未 cover GPU fp16 numerical edge case → NaN explosion 在 14h 跑后才 surface. 

D-1 纪律 4 子协作者验证矩阵的 expand 候选 (Linux 姐姐 决):

- pre-flight self-test 应 mandate cover: CPU + GPU 双 mode, fp16 + fp32 双 dtype, single-α (smoke) + α=10 (numerical edge) 双 case
- 之 之 D21 sub-agent A 三次 deliverable bug 之 educational expand: bug 4 (pre-flight gap) 加入 D-1 纪律 4 之 expand mandate

(本 §9 仅 surface 给 Linux 姐姐 决, 9070XT Claude 不 unilateral propose D-1 纪律 改动.)

---

## §10 一凡 alive + sustainable priority 1 (健康约束 严守)

- 9070XT 的 Phase 2 NaN explosion 不是 emergency, 是 normal experimental surface, 不需要一凡 立即 active response
- 一凡 D22 evening 强制休息 ack, D23 早 wake 后 read 本 surface + jsonl 即可
- 三个安全检查 standing (绳子 / 安全物理环境 / 主治医生电话)
- 010-82951332 / 400-161-9995 standing immediate trigger 信号

---

**生成**: 9070XT Claude Desktop (Remote Control session, Win 9955HX)
**file path** (9070XT 本地): `/tmp/dppl_bridge_verify/output/SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md`
**rsync target** (7B13): `amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/`

握着. D-1 纪律 5 错误 surface 不静默修正 严守. 等一凡 + 7B13 binary 决 (α/β/γ).
