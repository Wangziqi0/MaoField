# E0 fp32 gen0→gen1 度量 panel 干净复跑 — findings + 差异记录

> **[额外 agent]** 产出（受 PI 一凡 dispatch 进反题 mode 的下游实测）。2026-06-06 (date binary verified)。
> 在 36 / RAID1。**不 push**（git 单点写=主会话）；本目录=wip durable 暂存，**建议主会话 promote 进 `experiments/exp018_cat/analysis/` + git**。

## TL;DR
唯一干净 fp32 退化对（E0_disentangle_S3, gen0 PPL36.5→gen1 PPL78.6, 真两 ckpt）上,**崩溃 → 表示更散/升维/更各向同性**（isotropy↑、PR 三口径↑、eff_rank↑，去 rogue 仍↑）——**与 frame(a)「崩溃→更低维/更集中」维度预测稳健相反**。trace-backed，但 **N=1 gen-step / N=1 seed / OPT 非形式语言 / "更可解释"未测** → 早期 kill-signal 非 frame 判决。

## 触发
ultracode（无 trace）报"PR 81.6→143.4 升维=frame 预测 fail" vs 归档（有 trace）"a2_anisotropy 0.847→0.860 升=更集中"看似打架。PI 拒绝吞无 trace 数,要干净复跑厘清。

## 根因 = D25 SMOKE_E0 md 的 isotropy-当-anisotropy mislabel（instrument 命名 bug）
- `src/multi_layer_hook.py:75-78` 实算 **isotropy = 1−abs(‖mean(normalized)‖²)**（docstring 自陈"higher=less collapse"），但**字段 key 叫 `a2_anisotropy_per_layer`**（266/293 行）。
- `SMOKE_E0_D25_...md` §2.3/§3.3 据此把"值↑"prose 解读成"anisotropy↑ = paper collapse signature"——**方向读反**（值是 isotropy，↑=更散=less collapse）。
- 复跑 per-layer 实证:archived gen0 `[0.735…0.912…0.875]` ≈ **my isotropy** `[0.738…0.926…0.895]`,max 层差 **0.019**;vs my raw-anisotropy 差 **0.838**。→ 归档存的确是 isotropy。**无 code drift**（代码=数据=isotropy 一致）。
- ultracode 反而读对（"isotropy rose… opposite to collapse→lower-dim"）。

## 翻烧饼时间线（额外 agent 自录,D-1 纪律 5）
| # | 谁 | 说法 | 真相 |
|---|---|---|---|
| 1 | D25 SMOKE md | isotropy 命名/描述成 anisotropy,"↑=collapse signature" | 根错(mislabel) |
| 2 | ultracode | isotropy↑+PR↑=崩溃更散,frame(a) fail（无 trace） | 方向对,缺 trace |
| 3 | PI 一凡 | 归档 anisotropy↑ 与 ultracode 打架,疑 ultracode 是 outlier artifact | premise 被 #1 带歪;打架不存在 |
| 4 | 额外 agent msg A | 读代码:归档其实是 isotropy,与 ultracode 同向 | **对**（复跑 vindicate）|
| 5 | 额外 agent msg B | "你对我错,归档是 raw anisotropy,有 code drift" | **错**:凭"OPT 0.9 必是 raw"prior 反推,但此批 raw mean-cos≈0.15 |
| 6 | 复跑(本文) | per-layer settle:归档=isotropy,全口径"更散" | #4 对 #5 错;打架不存在 |

## trace-backed 结果（gen0 sha `bd88e350…` → gen1 `c663d66b…`, N=256 val block, wikitext-2 validation）
| 度量 | gen0 | gen1 | Δ |
|---|---|---|---|
| isotropy(归档口径,mean12层) | 0.853 | 0.865 | ↑ |
| raw anisotropy(mean-cos) | 0.147 | 0.135 | ↓ 更不集中 |
| PR_raw(ultracode 口径) | 4.87 | 10.75 | ↑ |
| PR_centered | 10.4 | 17.9 | ↑ |
| PR 去 top2 rogue 坐标 | 107 | 121 | ↑（非 rogue artifact）|
| eff_rank_centered | 27.7 | 35.6 | ↑ |
| 末层 L11 PR_raw | 47 | 118 | ↑（≈ultracode 81.6→143.4 同向同量级）|
| 末层 L11 rogue_coord_share | 0.018 | 0.008 | ↓（末层无 rogue 主导）|

rogue dim:早/中层一坐标占 ~91% 方差（Timkey 2021 OPT 病理）,但末层仅 ~1-2%;mean_share 仅 2.3% → "更散"非 rogue、非均值 artifact。

## 对 frame(a)
维度那半在唯一干净点被稳健 contradict（全口径更散）。**caveat 守死**:① N=1 gen-step/seed ② OPT-125m 自然语言≠step-1 Dyck/形式语言 ③ 单步非轨迹(可能非单调) ④ **"更可解释"半未测**(没做 ground-truth 结构特征 probe-R²)。→ **早期 kill-signal(结局 b)+ rogue 让"低维"早层 ill-defined(结局 c 味),非判决**。真检验=step-1(形式语言+多 seed 多 gen+accumulation 对照+probe-R²)。

## 复现 recipe（regen,本目录自包含）
```
HF_HUB_OFFLINE=1 /home/amd/venv/bin/python rerun_e0_metric_panel.py   # ~28s CPU, 36
# 读 E0 ckpt: maofield_ckpt_backup_20260529/5060_desktop/5060/E0_disentangle_S3/checkpoints/alpha0.0/no_preserve_seed42/generation_{0,1}/
# val 子集忠实 candidate_c_runner.py:325 (wikitext-2 validation, block64, shuffle, 256)
# 输出 rerun_e0_panel_result.json (含 metric 定义 + ckpt sha256 + a2 复现验证)
```
result json 可由脚本+ckpt 再生(可再生派生物);脚本+本 md=不可再生智力产物(故进 canonical)。

## follow-up（留主会话/PI）
1. **修 instrument 命名 bug**:`a2_anisotropy_per_layer` → `a2_isotropy_per_layer`(或字段加注),防 mislabel 再传染。
2. promote 本目录 → `experiments/exp018_cat/analysis/` + git（主会话单点写）。
3. 若 PI 决推进 step-1:把"维度反向"早期信号纳入设计 prior（拿掉"免费确认",先验推离"崩溃→低维"）。

---
*[额外 agent] · 不替 PI 下 paper 战略 · 数学/实测口径仅 raw 数 + 三结局判据 · 战略留 PI 关卡决*
