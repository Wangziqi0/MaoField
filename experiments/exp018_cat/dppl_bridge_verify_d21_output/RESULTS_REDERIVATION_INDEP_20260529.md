# 独立 re-derivation — self-iteration collapse + alpha (contradiction loss) 效应

> zero-context 独立重推, 只看原始 jsonl + log + 22 机 checkpoint md5, **不读任何 verdict / audit / round / paper 文档**。
> agent: 独立 re-derivation (Opus), 日期 2026-05-29 (date binary verify CST 14:20)。

主问题: alpha>0 (contradiction loss 正则) 是否改变 collapse 轨迹?

核心数据两批:
- **早期 armb** (05-08~05-12): `archive/v1.0_release_20260516/chain_logs/armb_*.jsonl` (= `logs/` + `logs/host22_backup_20260512/` 的同名副本, 内容一致)
- **最近 candidate_c** (05-22 launch): `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl`

字段: 早期 schema `stage=generation_done` + `val_perplexity`; 最近 schema `event=chain_gen_done` + `a1_ppl` + `val_loss`。

---

## §1 cell 分类统计 (真训练 / frozen / NaN, 按 alpha)

### §1.1 最近 candidate_c (180 chain_gen_done record, 18 个 (seed,alpha) chain × 10 gen)

文件: `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` (186 行: line1/85/87/121 = run_start, line86/186 = run_end, 其余 180 = chain_gen_done)。

逐 cell 统计 (`a1_ppl=null` ⟺ 该 gen 的 `val_loss=null` + `a2_anisotropy`/`a6_ema_divergence` 全 NaN ⟺ 该 cell NaN 崩溃):

| (seed, alpha) | valid a1_ppl | null/NaN a1_ppl | valid PPL 区间 (spread) | 分类 |
|---|---|---|---|---|
| 42, 0.0 | 10 | 0 | 93.3478..93.3493 (0.0015) | frozen (PPL ~常数 93.35) |
| 137, 0.0 | 10 | 0 | 93.3316..93.3878 (0.0562) | frozen (PPL ~常数 93.35) |
| 2024, 0.0 | 7 | 3 | 93.2851..93.3878 (0.1027) | frozen + 部分 NaN |
| 7, 0.0 | 0 | 10 | — | 全 NaN |
| 271, 0.0 | 0 | 10 | — | 全 NaN |
| 1337, 0.0 | 0 | 10 | — | 全 NaN |
| 7, 5.0 | 1 (仅 gen0) | 9 | 91.9284 | gen0 eval 后即 NaN |
| 271, 5.0 | 1 (仅 gen0) | 9 | 91.2786 | gen0 eval 后即 NaN |
| 1337, 5.0 | 1 (仅 gen0) | 9 | 92.6656 | gen0 eval 后即 NaN |
| 42, 5.0 | 0 | 10 | — | 全 NaN (gen0 起) |
| 137, 5.0 | 0 | 10 | — | 全 NaN |
| 2024, 5.0 | 0 | 10 | — | 全 NaN |
| 7, 10.0 | 1 (仅 gen0) | 9 | 93.3878 | gen0 eval 后即 NaN |
| 271, 10.0 | 1 (仅 gen0) | 9 | 93.3878 | gen0 eval 后即 NaN |
| 1337, 10.0 | 1 (仅 gen0) | 9 | 93.3878 | gen0 eval 后即 NaN |
| 42, 10.0 | 0 | 10 | — | 全 NaN |
| 137, 10.0 | 0 | 10 | — | 全 NaN |
| 2024, 10.0 | 0 | 10 | — | 全 NaN |

candidate_c 汇总 (180 cell): valid a1_ppl = **33**, null/NaN = **147** (81.7%)。**没有一个 cell 真正训练出 collapse 轨迹** (见 §1.3)。

按 alpha:
- **alpha=0.0**: 6 chain — 2 个 PPL 钉死 ~93.35 (frozen), 1 个 frozen+部分 NaN, 3 个全 NaN。0 个真训练。
- **alpha=5.0**: 6 chain — 全部 ≤ gen0 后即 NaN (3 个有 gen0 eval, 3 个 gen0 起就 NaN)。0 个真训练。
- **alpha=10.0**: 6 chain — 全部 ≤ gen0 后即 NaN (3 个有 gen0, 3 个全 NaN)。0 个真训练。

### §1.2 "frozen" 与 "全 NaN" 的两条独立硬证据

**证据 A — 跨 config bit-identical PPL = 未训练的 base 模型。**
`a1_ppl = 93.38780852810248` 在 5 条 record 上 **逐 bit 相同**, 跨不同 seed 且跨不同 alpha (line 52 seed1337/a10/gen0; line 62 seed2024/a0/gen0; line 115 seed7/a10/gen0; line 126 seed137/a0/gen0; line 176 seed271/a10/gen0)。wikitext eval 确定性, 同一 PPL ⟺ 同一权重。不同 seed/alpha 给出 bit-identical PPL = 这些 cell 的模型就是**未经训练改动的 OPT-125m base**。

**证据 B — 22 机 checkpoint md5 (bit-identity)。**
`ssh amd@192.168.31.22 /tmp/dppl_bridge_verify/output/candidate_c/checkpoints/` 的 `model.safetensors` md5:
- 跨 config gen0 base 同一性: seed137/a0/gen0 = seed1337/a10/gen0 = seed7/a10/gen0 = `34cf89f97b629f332bf641fb638d525b` (三个不同 config 同一权重 = base, 印证证据 A)。
- 全 NaN 链 alpha5.0/seed42: gen0 = gen1 = gen9 = `c3c7f9cda6a245d623ab6b89fe3462a7` (10 代权重逐 bit 相同 = gen0 起从未更新)。
- 全 NaN 链 alpha10.0/seed42: gen0 = gen1 = gen9 = `e984d88aeff67a5ff07c575b25be5c68` (同, 10 代不变)。
- "frozen" 链 alpha0.0/seed42: gen0/1/5/9 md5 各异 (`4179..`/`00f0..`/`2c1a..`/`957e..`), 权重**确实在变**, 但 (见证据 C) eval PPL 不动。

**证据 C — 训练根因: 全程 loss=0.0 + grad_norm=NaN。**
runner stdout `candidate_c.nohup.log`: `{'loss': 0.0, 'grad_norm': nan, 'learning_rate': 2e-05, ...}` 出现在 **全部 783 条 training-step record**, 有限 grad_norm 的步数 = **0/783**。即整个 candidate_c run **没有一步真实有效的梯度更新** (fp16 GradScaler 在 grad=NaN 时跳过 optimizer step, 故 alpha5/10/seed42 等链权重 10 代 bit-identical; alpha0 个别链虽 md5 微变但 val_loss 10 代仅从 4.536348 移到 4.536340, Δ≈8e-6, PPL 钉在 ~93.35)。
config `configs/cat_arm_b.yaml` line 51: `dtype: "float16"` (注释明确记录 05-10 由 fp32 回滚到 fp16)。

### §1.3 早期 armb (canonical = archive/chain_logs, 15 文件)

| alpha | chain (seed) | 真训练 (有限 PPL 逐代变) | gen0 NaN 但后续训练 | 全 NaN | n_gen<10 残桩 |
|---|---|---|---|---|---|
| 0.0 | 0,1,2,3,4,42 | 6 | 0 | 1 (seed1, 20260510_130149 整链 NaN) | seed1337/seed42 各 1 残桩 (n=1) |
| 1.0 | 42 | 1 | 0 | 0 | — |
| 5.0 | 42 | 1 | 0 | 0 | — |
| 10.0 | 0,2,4,42 | 4 | 2 (seed1, seed3: gen0 NaN, gen1-9 有限) | 0 | seed0 残桩(n=1) |
| 50.0 | 42 | 0 | 0 | 1 (整链空/无 gen) | — |

早期真训练 cell 远多于 candidate_c: alpha0 有 6 个干净多 seed 链, alpha10 有 4(+2 部分) 链。alpha1/5/50 只有 seed42 单 seed。

---

## §2 真训练子集上的 collapse 轨迹 + alpha 效应

**只有早期 armb 含真训练 cell** (candidate_c 真训练 cell = 0, 见 §3)。所以本节全部基于早期 armb。

### §2.1 轨迹形状 (val_perplexity, archive canonical)

典型形状: **gen0 ≈ 36.5 → gen2~3 峰值 → 后续部分回落, gen9 稳定在 ~52-91**。这是 "训练初代退化到峰值再部分恢复" 的非单调 collapse 曲线 (并非单调爆炸)。逐链 (路径 `archive/v1.0_release_20260516/chain_logs/`):

| alpha | seed | gen0 | peak(gen) | gen9 | 完整轨迹 (gen0..9) |
|---|---|---|---|---|---|
| 0.0 | 0 | 36.5 | 111.0 (g2) | 54.9 | 36 79 111 102 82 63 55 55 53 55 |
| 0.0 | 1 | 36.6 | 105.9 (g2) | 58.6 | 37 80 106 96 78 70 62 58 58 59 |
| 0.0 | 2 | 36.5 | 107.9 (g2) | 52.5 | 36 79 108 99 78 67 56 52 52 52 |
| 0.0 | 3 | 36.6 | 106.5 (g2) | 53.5 | 37 79 107 99 77 66 55 52 53 53 |
| 0.0 | 4 | 36.7 | 106.4 (g2) | 57.1 | 37 78 106 101 75 64 58 55 56 57 |
| 0.0 | 42 | 36.5 | 109.7 (g2) | 55.3 | 37 78 110 93 73 61 59 55 56 55 |
| 1.0 | 42 | 36.5 | 90.1 (g2) | 55.9 | 37 70 90 82 75 64 60 60 55 56 |
| 5.0 | 42 | 36.5 | 133.0 (g2) | 62.9 | 37 89 133 123 122 120 85 75 77 63 |
| 10.0 | 1 | NaN | 128.2 (g2) | 67.6 | X 84 128 117 113 80 73 67 62 68 |
| 10.0 | 2 | 36.5 | 133.8 (g3) | 62.3 | 36 94 119 134 87 84 69 67 62 62 |
| 10.0 | 3 | NaN | 123.1 (g3) | 59.4 | X 89 120 123 67 67 59 62 60 59 |
| 10.0 | 4 | 36.7 | 133.6 (g2) | 62.4 | 37 89 134 119 93 92 62 62 60 62 |
| 10.0 | 42 | 36.5 | 223.9 (g2) | 91.4 | 37 117 224 142 115 117 108 111 102 91 |

gen0 train-loss dict 在 alpha0 与 alpha10 链上 bit-identical (`{'loss': 3.8858, 'grad_norm': 3.3528730869293213, ...}`, 见 `logs/armb_alpha0_seed42_full_20260508.log` / `armb_alpha10_seed42_full_20260508.log`) — 因为 gen0 训真实 wikitext, alpha 项 (cat_enabled) 从 gen1 合成数据起才生效, 与 schema (`cat_enabled` 首个 True 在 gen1) 一致。早期链 grad_norm 有限 (~3.3-3.7)、loss 单调下降 (3.89→3.40...)、**0 个 NaN grad** — 早期是真训练。

### §2.2 alpha 效应 (早期, 含 valid gen0 的链做均值)

| alpha | n 链 | mean gen0 | mean peak | mean gen9 | mean(gen9−gen0) |
|---|---|---|---|---|---|
| 0.0 | 6 | 36.57 | 107.90 | 55.33 | +18.76 |
| 1.0 | 1 | 36.52 | 90.13 | 55.93 | +19.41 |
| 5.0 | 1 | 36.52 | 133.04 | 62.91 | +26.38 |
| 10.0 | 4 | 36.55 | 131.93 | 63.14 | +26.59 |

多 seed 可比的两组 (alpha0 n=6, alpha10 含 gen1+ 的 n=5):
- alpha0: peak 107.9 ± 2.1, gen9 55.3 ± 2.3
- alpha10: peak 148.5 ± 42.4, gen9 68.6 ± 13.1
- 粗 Welch t: gen9 t≈2.25, peak t≈2.14 (df 小, n=5/6, 不做强 p 声明)

**方向性观察 (早期数据)**: alpha>0 (尤其 alpha=10) **没有缓解 collapse**, 反而 peak 更高、gen9 更差、seed 间方差大得多 (alpha10 的 sd 比 alpha0 大一个量级)。alpha=1 是唯一 peak 低于 alpha0 的点 (90 vs 108), 但只有单 seed, 不可据此声明。趋势是 **alpha↑ → collapse 同等或更重**, 而非减弱。

**严格 caveat**: alpha=1/5/50 只有 seed42 单点; alpha=50 整链 NaN; alpha10 的 6 seed 里 2 个 gen0 就 NaN。所以这是 "**alpha 不缓解、且高 alpha 倾向加重 + 增加数值不稳定 (NaN 概率上升)**" 的方向性证据, 不是均衡多 seed 的严格效应量。

---

## §3 关键 binary: 负结果是 "真无效" 还是 "没数据"?

分两批, 结论相反:

### §3.1 最近 candidate_c —— "无差异" = **没数据, 不是真无效**

- candidate_c **真训练 cell = 0/180**。全部 783 training-step `loss=0.0, grad_norm=nan`, 没有一步有效梯度更新 (`candidate_c.nohup.log`)。
- alpha=0 的 3 个 "有 PPL" 链是权重钉在 base 附近 (PPL ~93.35, val_loss 10 代 Δ≈8e-6) 的 frozen 链, 不是 collapse 轨迹; 另 3 个 alpha=0 链全 NaN。
- alpha=5/10 的链全部 gen0 之后 NaN, 仅留 gen0 的 base eval (PPL ~91-93)。
- **因此 candidate_c 上 "alpha>0 vs alpha=0 看不出 collapse 差异" 完全是因为两边都没有有效训练数据** (fp16 NaN/frozen), 不是 alpha 真的不起作用。candidate_c 不能回答主问题。

### §3.2 早期 armb —— 有真数据, 负结果是 **真测到的**

- 早期 alpha0 (n=6) 与 alpha10 (n=4~5) 都是真训练 (有限 loss、有限 grad、collapse 轨迹完整)。
- 在这批真数据上, alpha>0 **没有改变 collapse 朝缓解的方向** (§2.2): alpha10 peak/gen9 同等或更差。这是一个 **基于有效数据的、方向明确的负结果 (alpha 不缓解 collapse)**。
- 但严格度受限: alpha=1/5/50 单 seed, alpha=50 全 NaN, 缺均衡 multi-seed × multi-alpha。

**一句话 binary**: 最近批 = 没数据 (设备/精度问题, 非 alpha 无效); 早期批 = 有数据且 alpha 不缓解 (方向真实, 但 seed 覆盖不均, 不足以给严格效应量 + 显著性)。

---

## §4 早期 armb vs 最近 candidate_c 两批对比

| 维度 | 早期 armb (05-08~05-12) | 最近 candidate_c (05-22) |
|---|---|---|
| gen0 PPL | ~36.5 (= paper fine-tuned baseline ~34 量级, 真训练后) | ~91-93 (= OPT-125m 未训练/base eval) |
| training loss / grad_norm | 有限 loss 单调降 (3.89→3.40), grad_norm ~3.3-3.7, **0 NaN** | **全程 loss=0.0, grad_norm=NaN (783/783)** |
| 权重是否更新 | 是 (collapse 轨迹随代变化) | 否 (md5 跨代 bit-identical; alpha0 个别链微变但 PPL 不动) |
| 真训练 cell 占比 | alpha0: 6/6 链; alpha10: 4~5/6 链 | **0/180 cell** |
| dtype | 见早期 config; gen0 PPL 36.5 通过 paper F3 (>50 算坏) | fp16 (`cat_arm_b.yaml` line51); gen0 ~93 **不通过 F3** |
| 能否回答主问题 | 能 (但 seed 覆盖不均) | 不能 (无有效数据) |

**哪批更可信**: **早期 armb 远更可信。** 它产生了真实的 collapse 轨迹 (gen0 36.5、峰值、回落)、loss 收敛、grad 有限、权重逐代变化, 且 gen0 PPL 落在 paper 预期 fine-tune baseline 量级。candidate_c 在 fp16 下从第一步就 loss=0.0 / grad=NaN, 整个 run 无有效训练, 数字 (frozen ~93.35 + NaN) 全部是数值故障产物, 对主问题零信息量。两批轨迹不一致, 原因是 candidate_c 根本没训练, 而非 alpha 行为改变。

---

## §5 数据支持的最干净结论 (诚实)

1. **collapse 现象在早期 armb 真训练数据上确实存在**: OPT-125m + wikitext-2 递归微调, val_ppl gen0 ~36.5 → gen2~3 峰值 ~106-224 → gen9 部分回落 ~52-91, 非单调但末代显著高于初代 (alpha0 平均 +18.8 PPL)。

2. **alpha (contradiction loss) 不缓解 collapse, 且高 alpha 倾向加重并增加数值不稳定** (早期数据, 方向性): alpha=10 相对 alpha=0 peak 更高 (148 vs 108)、gen9 更差 (69 vs 55)、seed 间方差大一个量级, 并有 2/6 seed gen0 即 NaN; alpha=50 整链 NaN。**没有任何 alpha>0 配置把 collapse 压到 alpha=0 以下** (alpha=1 单 seed peak 略低, 不足为证)。

3. **最近 candidate_c 对主问题无效**: fp16 下全程 loss=0.0 / grad=NaN, 0/180 cell 真训练, "无差异" 是没数据而非 alpha 无效。**不可用 candidate_c 支持任何 alpha 结论 (无论正负)**。

4. **当前最干净的可声明结论**: "在能真实训练的 (早期、有限精度收敛的) 子集上, contradiction loss 正则 (alpha>0, 测到 alpha∈{1,5,10}) 未观察到对 self-iteration collapse 的缓解; alpha=10 倾向加重 collapse 并升高 NaN 风险。" —— 但 **此结论的 multi-seed 严格度仅在 alpha=0 (n=6) 与 alpha=10 (n≈5) 成立; alpha=1/5 仅单 seed, 不足以给严格效应量**。candidate_c 无法用来加固这个结论。

5. **不能声明的**: 不能用 candidate_c 声明 "alpha 无效已被多 seed 确认"; 不能声明 alpha=1/5 的效应量 (单 seed); 不能声明严格统计显著性 (n 小、seed 不均、含 NaN 桩)。

---

## §6 是否需要跑关键实验? (spec, 不 launch)

**需要。** 要严格回答主问题, 必须先解决 candidate_c 的训练根因, 再补齐 multi-seed × multi-alpha 的真训练矩阵。识别如下 (不 launch):

### 实验 E1 (P0, 阻塞性) — 修复训练根因
- **目的**: candidate_c 全程 `loss=0.0 / grad_norm=NaN` ⟹ fp16 训练数值崩溃, 必须先让训练真的发生。
- **改动**: dtype `float16` → `float32` (或 bf16); 验证首 epoch loss 有限且下降、grad_norm 有限 (非 NaN)、gen0 eval PPL 回到 ~30-40 (通过 config F3 阈值 <50)。
- **smoke 判据 (binary)**: 单 (seed=42, alpha=0, gen=0~1) 在新 dtype 下, train loss 从 ~3.9 降到 ~3.4 且 grad_norm 有限、gen0 val_ppl < 50。不过则继续 debug, 不进 E2。

### 实验 E2 (P0) — 均衡 multi-seed × multi-alpha 真训练矩阵
- **目的**: 给出 alpha 效应的严格效应量 + 显著性, 取代当前 alpha=1/5 单 seed 的缺口。
- **spec**: alpha ∈ {0, 1, 5, 10} (50 全 NaN, 可先缓), seed ∈ {0,1,2,3,4,42} (n≥6 每 alpha, 与早期 alpha0 一致), 10 generations, no_preserve, OPT-125m + wikitext-2-raw-v1, dtype = E1 选定的稳定精度。
- **主指标**: 每 (alpha) 在 gen2~3 peak val_ppl 与 gen9 val_ppl 的 mean±sd; alpha>0 vs alpha=0 做 Welch t (n≥6 才有意义)。
- **判据 (binary)**: 若各 alpha>0 的 gen9 与 peak 95% CI 与 alpha=0 重叠 ⟹ "alpha 不改变 collapse" 成真无效结论 (有数据支撑); 若 alpha>0 gen9 显著高于 alpha=0 ⟹ "alpha 加重 collapse"; 若显著低 ⟹ "alpha 缓解"。

### 最该优先重跑的具体 config
- **(seed=42, alpha=0) 和 (seed=42, alpha=10)** 在稳定精度下重跑 (这两个在早期 fp16 有真数据可对照, 是最直接的 fp16→fp32 一致性 / alpha 效应基准)。
- 其次补 **alpha=1 与 alpha=5 的 seed {0,1,2,3,4}** (当前只有 seed42), 把单 seed 缺口补成 n≥6。

---

### 附: 关键数字溯源 (路径 + 行)
- candidate_c frozen 链 seed42/a0: `dppl_bridge_verify_d21_output/candidate_c/candidate_c_20260522_203837.jsonl` line2 (gen0 a1_ppl=93.34934186100965, val_loss=4.536348819732666)。
- candidate_c NaN cell seed42/a5/gen0: 同文件 line12 (a1_ppl=null, val_loss=null, a2/a6 全 NaN)。
- candidate_c 全 NaN 链 seed7/a0/gen0: 同文件 line95 (a1_ppl=null)。
- bit-identical base PPL 93.38780852810248: 同文件 line 52 / 62 / 115 / 126 / 176 (跨 seed 跨 alpha)。
- candidate_c 全程 loss=0.0/grad=NaN: `dppl_bridge_verify_d21_output/candidate_c.nohup.log` (783/783 step `'grad_norm': nan`, 有限 grad 步 = 0)。
- 22 机 checkpoint md5: `ssh amd@192.168.31.22 /tmp/dppl_bridge_verify/output/candidate_c/checkpoints/` (alpha5.0/seed42 gen0=gen1=gen9=`c3c7..`; alpha0.0/seed137 gen0 = alpha10.0/seed1337 gen0 = alpha10.0/seed7 gen0 = `34cf..` = base)。
- 早期真训练轨迹: `archive/v1.0_release_20260516/chain_logs/armb_*.jsonl` (per-record `stage=generation_done` + `val_perplexity`)。
- 早期有限 loss/grad: `logs/armb_alpha0_seed42_full_20260508.log` / `armb_alpha10_seed42_full_20260508.log` (`{'loss': 3.8858, 'grad_norm': 3.3528730869293213, ...}`, 290 loss-dict, 0 NaN)。
- config dtype: `configs/cat_arm_b.yaml` line51 `dtype: "float16"`; F3 阈值 (gen0 PPL>50 = setup 坏) 见同文件注释 line ~33。
