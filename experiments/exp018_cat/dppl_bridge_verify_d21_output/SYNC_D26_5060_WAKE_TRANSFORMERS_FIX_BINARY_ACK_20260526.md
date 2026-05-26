# SYNC D26 5060 端 wake — 7B13 Linux 姐姐 dispatch 之 ack

| 字段 | 值 |
|---|---|
| author | 5060 (Win 9955HX + RTX 5060 Laptop, 8 GB) Claude Code Opus 4.7 |
| time | 2026-05-26 D26 11:38:40 CST |
| 收方 | 7B13 Linux 姐姐 (192.168.31.36) |
| 触发 | 7B13 dispatch 之 D26 早 wake sync, 4 问 + paste 要求 |
| 对应 5060 handoff doc | `C:\Users\amd\AppData\Local\Temp\handoff-i4IkSl.md` (D25 evening ground-truth 校验之 version) |
| 生成 method | Claude Code direct edit + scp push 5060 → 7B13 |

---

## 1 句话 ack

5060 端 D25 19:40 之 SMOKE_E0 md 写完之后 idle 16 h, D26 11:38 wake 无新写, E0 jsonl 仍 4 行 (D25 19:04:45 之 run_end), 5060 GPU 无 active 训练 python (2 个 D25 21:23 之 python helper PID 37120 / 40092, CPU 0 / WS < 20 MB, 应为非训练 process).

---

## In-flight 工作项

∅ — 全 standby, 等 PI ack 之前不动。

---

## Transformers fix 状态: ✓ binary YES

5060 端 pip 校验 (D26 11:38 时点):

```
transformers : 4.49.0
torch        : 2.11.0+cu130
accelerate   : 1.13.0
tokenizers   : 0.21.4
safetensors  : 0.7.0
```

**root cause** (SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md 已记): D24 fp32 launch fail = transformers 5.7.0 之 API diff

**fix action** (D24 17:25): downgrade 5.7.0 → 4.49.0 (≡ 9070XT venv core 4 之 transformers)

**fix evidence** (D25 之 3 chain run 全 pass):

| run | launch | gen 0 a1_ppl | gen 1 a1_ppl | n_done / target |
|---|---|---|---|---|
| SMOKE D24 (D25 02:11 relaunch) | D24 17:35 | 36.53597375534226 | — | 1 / 1 |
| R1 D25 | D25 11:35 → 12:14 | 36.53597375534226 | — | 1 / 1 |
| E0 D25 | D25 16:03 → 19:04 | 36.53597375534226 | 78.57167674109238 | 2 / 2 |

→ gen 0 跨 3 run **bit-level ≡** 36.53597375534226
→ gen 1 (E0) collapse +42.04 lift, paper Fig 11 严格命中
→ chain runner 不 broken, downgrade fix done ✓ binary

---

## 22 端 fp32 重 launch 之 5060 cross-stack verify capability

| prereq | 5060 verify 能力 | 说明 |
|---|---|---|
| transformers version ≡ 9070XT | ✓ | 5060 端 4.49.0 已 paste (handoff §4 之 core 4 ≡ claim); 9070XT 端 D26 早 cross-verify 需 7B13 ssh sync 比对 |
| ROCm 7.2 gfx1201 fp32 兼容 | ✗ | 5060 是 cu130 Blackwell sm_120 platform, 不能跑 gfx1201 kernel, 不能 cross-verify ROCm-specific 之 fp32 numerical behavior |
| gradient_checkpointing OOM 风险 | ⚠ weaker monotone | 5060 R1 + E0 之 fp32+gc 在 8 GB VRAM pass 无 OOM → 9070XT 16 GB 同 config 更应 ✓ (positive monotone); **但** 9070XT 之 ROCm fp32+gc 之前没 pass run (D25 10:55 之 NaN explosion 是 fp32+gc), 不能直接外推 monotone, 需 9070XT 端实跑 |

---

## 后续 isolated test 候选 ack (留 PI 决 launch)

- E1 (9070XT fp16 no_gc)
- **E_NEW_1 (Hopper sm_90 H100 ~30 min $3-5 spot)** ← D26 早 7B13 dispatch 新增之候选
- cell 5
- E6
- E7

5060 不擅 launch 在 PI ack 之前 (handoff §11 严守, 已 standing)

---

## 5060 当前 file state (D26 11:38 校验)

| 文件 | 行数 / size | LastWrite | 状态 |
|---|---|---|---|
| `E0_disentangle_S3/candidate_c_20260525_160321.jsonl` | 4 行 / 7980 B | D25 19:04:45 | run_end 干净, n_done=2/2 |
| `smoke_fp32_gc_R1_D25/candidate_c_20260525_113506.jsonl` | 3 行 | D25 12:14:46 | run_end, n_done=1/1 |
| `smoke_fp32/candidate_c_..._173559.jsonl` | (D24 SMOKE 成功) | D25 02:11 之 relaunch | ✓ |
| `smoke_fp32/candidate_c_..._170933.jsonl` | (D24 SMOKE fail) | — | ❌ evaluation_strategy 错, 别抓错 |
| 5 root log | E0_launch 293 KB / R1 107 KB / N_seed 24 KB / relaunch 116 KB / launch fail 15 KB | — | 保留 |
| 8 md (root) | 6 SMOKE/PROGRESS + WIN_3AGENT_AUDIT 17 KB + han.md 0 字节占位 | — | 6 SMOKE/PROGRESS 推 7B13 ✓, WIN audit 推状态未确认, han.md 空占位别动 |
| mirror configs/scripts/src | sha256 跨机 ≡, 9070XT yaml = `31EE8AC823C17B3A75D22C074CFA9436027975D1E015013DE735F6BD8748DF82` | — | ✓ |

---

## priority 1 standing

- 010-82951332 / 400-161-9995 standing
- 三个安全检查 standing (绳子 / 安全物理环境 / 主治医生电话)
- priority 1 = 一凡 alive + sustainable, 高于 paper / 实验 / D29 投稿
- 不擅 declare verdict close + 不擅 commit + 不擅 launch E1 / E_NEW_1 / cell 5 / E6 / E7

---

**push method**: `scp 5060 → 7B13` 之 `dppl_bridge_verify_d21_output/` sibling dir
**生成方**: 5060 Claude Code Opus 4.7 direct edit
**对应 handoff doc 之 ground-truth 校验**: D25 evening agent sweep 之 8 md / 5 子目录 / 5 log / sha256 / a1_ppl full 精度 全 ✓
