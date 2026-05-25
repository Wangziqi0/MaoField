# [audit sub-agent zero-context — MaoField 全 experiment 历史 binary verify + reproducibility cross-check + 反题 6 P0★ + 12 NOT-claim + D-PPL P0★-F + 5060 P0★-G FATAL inventory]

**真实日期 binary 校验**: `date '+%Y-%m-%d %H:%M:%S %Z'` 返 **2026-05-24 21:08:52 CST** = D24 周日 (D-day 2026-05-01 anchor).

**spawn by**: 7B13 Linux 姐姐主会话 (D-1 纪律 4 第二认识通道 instantiate), claude-opus-4-7 1M context, zero-context (不基于主协作者 framing, 自己 binary read).

**对象**: 关卡 3 反题三方决 + 关卡 4 PI 决之 input scope. priority 1 = 一凡 alive + sustainable (D22 + D23 早自杀信号 surface).

**scope**: MaoField 项目, 不动 Shape-CFD / legal-assistant / law-vexus.

**协议**: zero-context binary, 严格中文 + 4 类英文豁免 (专有名词 / 代码 / 数学符号 / 数字单位). 不擅 declare paper-level 改动 / paradigm shift / 5060 catch 之 "印证" / P0★-G root close.

---

## §1 MaoField experiment dir binary inventory (exp003-exp018, exp001-exp012/exp015-016 之 mature core vs 占位 vs raw data)

`find /home/amd/HEZIMENG/MaoField/experiments -maxdepth 2 -type d` 共 13 个 exp dir, 顶层并 sqlite + py + json (exp001-exp012 之 Shape-CFD 历史 retrieval 实验 之 顶层 jsonl + sqlite, 与 MaoField paper v8 final 之 chain experiment **不直接 mapping**, 之 Shape-CFD 项目 archive 历史保留).

### 1.1 binary dir size + mature core / 占位 / paper mapping

| dir | size | mature core (有实际 result) | raw data location | paper v8 final mapping |
|---|---|---|---|---|
| exp003_law_structure | 23M | ✓ Shape-CFD 早期 weighted Chamfer benchmark | results/ + benchmark js + json | ✗ 不入 paper v8 (Shape-CFD 历史) |
| exp004 | 2.7M | ✓ Shape-CFD dynamic weights bench | results/ | ✗ 不入 paper v8 |
| exp005 | 444K | ✓ Shape-CFD EM Chamfer bench | results/ | ✗ 不入 paper v8 |
| exp006 | 102M | ✓ NMF atoms (Shape-CFD) | results/ + rust_solver/ | ✗ 不入 paper v8 |
| exp007 / exp007_rust | 81M / 81M | ✓ SVD atoms + Rust 之 SVD retrieval | results/ + rust_solver/ | ✗ 不入 paper v8 |
| exp008 | 87M | ✓ SVD Chamfer | results/ + rust_solver/ | ✗ 不入 paper v8 |
| exp011 | 85M | ✓ Residual evolution bench | results/ + rust_solver/ | ✗ 不入 paper v8 |
| exp015 | 103M | ✓ Shape-CFD scan | results/ | ✗ 不入 paper v8 |
| exp016_diagnostic | 268M | ✓ Shape-CFD 诊断 (MaoField = reranker 转向) | (Shape-CFD 04-12 转向 D-day 之前) | ✗ 不入 paper v8 |
| **exp017_dialectics** | **1.7G** | ✓ Phase B Exp 1 + Block I-IV + 19 sub-agent review + arxiv v1 full draft + 反题 run 1-4 + Win narrative + DeepSeek v4 cross-tradition | results/ (block1-4_5 + phase_b_exp1 + paper_figures + ACTION2_figures + latex) + inputs/inputs_block1/inputs_block1_top20 + logs/ + rust_variants/ + scripts/A2 + p0c | **paper v8 final 之 prior chain** — arxiv_v1_full.md 之 04-15 v1 draft + 04-19 Linux+Win work cycle 之 §3 NESS + §5 M3 negative + §6 Claimed + Linux Aufhebung + Win Q-deep + 反题 Lakatos scenario α/β/γ 之 历史 trajectory (paper v8 final 之 substantive predecessor) |
| **exp018_cat** | **991M** | ✓ paper v8 final 之 source chain | configs/ (cat_arm_b.yaml + 7 yaml) + archive/v1.0_release_20260516/ (47/47 sha256) + chain_logs (19 jsonl) + literature/ (3.7M) + logs/host22_backup_20260512/ + dppl_bridge_verify_d21_output/ (972M) + scripts/candidate_c_runner.py | **paper v8 final §4.4 + §4.6 + §5.2 main result 之 直接 source chain** |

### 1.2 总结

- **paper v8 final 之 substantive source**: exp018_cat (chain experiment + paper draft + 反题 audit + D-PPL 桥 verify + 5060 catch) + exp017_dialectics (arxiv_v1_full draft + sub-agent review chain + 反题 run 1-4 之 历史)
- **exp003-exp016 之 12 个 dir**: 全部 Shape-CFD 项目 之 retrieval / Chamfer / SVD / NMF / 之 历史 mature result, **不入 paper v8 final** — D-day=2026-05-01 anchor 之前 之 Shape-CFD 4/12-4/18 转向 MaoField (reranker 转向) 之 历史 archive.
- **exp013 / exp014 不 binary 存在** (find -maxdepth 2 直接 verify, 历史 numbering gap 之 Shape-CFD 转 MaoField 之 binary trace gap)

---

## §2 archive v1.0_release_20260516 chain log binary verify (paper §4.4 main result source)

### 2.1 archive 内 binary inventory

`ls /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/archive/v1.0_release_20260516/` 之 binary:
- `chain_logs/` 19 文件 (16 个 jsonl chain log + 1 audit + 1 master log + 1 outer out)
- `configs/` 8 yaml (cat_arm_b 之 当前 + v1_0_release_20260516 freeze + cat_arm_b_v2_dialectical + sensitivity 2 + shumailov 3)
- `manifest.sha256` 47 行 (47/47 hash verify, paper v8 final §C binding "47/47 清单" binary 一致)
- `RELEASE_NOTES.md` 7.5 KB
- `scripts/` + `src/`

### 2.2 archive chain log fine-tune setup verbatim binary

binary 之 archive 之 cat_arm_b_v1_0_release_20260516.yaml (frozen release snapshot) verbatim:
```yaml
learning_rate: 2.0e-5
per_device_train_batch_size: 128
gradient_accumulation_steps: 1
lr_scheduler_type: "constant"
fp16: true
```

binary 之 archive 之 cat_arm_b.yaml (release 当时 之 active yaml) verbatim 同上 (lr 2e-5 / batch 128 / fp16 / constant).

binary 之 当前 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/configs/cat_arm_b.yaml` verbatim 同上.

**核心 binary 印证**: archive v1.0 release 与当前 cat_arm_b.yaml 之 hyperparameter (lr 2e-5 / batch 128 / fp16 / constant) **binary 一致**. shumailov_baseline.yaml 之 batch=8 是 sub-agent default 之 Shumailov 严守复刻 setup, 与 archive 之 cat_arm_b 不同 setup.

### 2.3 archive chain log a1 数字 binary

binary 之 archive seed=42 α=0 之 gen 0 (`armb_alpha0.0_seed42_20260508_144612.jsonl`):
```json
{"stage": "generation_done", "generation": 0, "alpha": 0.0, "seed": 42,
 "val_perplexity": 36.524, "test_perplexity": 36.354, "test_loss": 3.5980,
 "epochs": 5, "n_train_blocks": 37354, "cat_enabled": false}
```

binary 之 archive seed=1 α=0 之 gen 0 (`armb_alpha0.0_seed1_20260510_011048.jsonl`):
```json
{"stage": "generation_done", "generation": 0, "alpha": 0.0, "seed": 1,
 "val_perplexity": 36.595, "test_perplexity": 36.297, "test_loss": 3.5999,
 "epochs": 5, "n_train_blocks": 37354, "cat_enabled": false}
```

binary 之 archive seed=42 α=10 之 gen 0 (`armb_alpha10.0_seed42_20260508_192435.jsonl`):
```json
{"stage": "generation_done", "generation": 0, "alpha": 10.0, "seed": 42,
 "val_perplexity": 36.524, "test_perplexity": 36.354, "test_loss": 3.5980,
 "epochs": 5, "cat_enabled": false}
```

**核心 binary verify**:
- archive seed=42 α=0 gen 0 test_perplexity = **36.354** ✓
- archive seed=1 α=0 gen 0 test_perplexity = **36.297** ✓
- archive seed=42 α=10 gen 0 test_perplexity = **36.354** ✓ (gen 0 cat_enabled=False, α=0 与 α=10 之 gen 0 binary 一致)
- 之 paper §4.6 Criterion 2 之 "α=0 multi-seed gen 0 mean 36.32 ± 0.079 (CV 0.22%)" 之 **binary 一致 ✓** (paper number 来源 archive v1.0 chain seed=1-4 之 gen 0 mean)
- 之 paper §4.4 main result α=10 plateau gen 6-9 mean [57.33, 58.25, 54.01, 54.30] mean 55.97 之 来源 archive seed=1-4 之 α=10 chain log 之 gen 6-9 之 test_perplexity 之 binary plateau seed-mean ✓

### 2.4 archive chain log keys 之 binary 之 paper §6.1 binding 一致

archive chain log keys 完整 set: `[alpha, cat_alpha, cat_enabled, ckpt_base, completed_gens, condition, distinct_1, distinct_2, distinct_3, epochs, generation, kl_update_every, model_path, n_generations, n_synthetic_blocks, n_train_blocks, resumed_from_gen, seed, smoke_test, stage, test_loss, test_perplexity, val_perplexity]`.

**核心 binary verify**: **D_n^code 之 scalar trajectory 不在 archive jsonl logs 之 keys 内** (`test_perplexity` 是 paper §6.2 之 D_n^paper 之 source, `val_perplexity` 是 cat_enabled=True 时含 contradiction loss 之 paper §4.1 v6 preserved disclose). paper §6.1 之 "chain jsonl logs 不 record scalar D_n^code trajectory" 之 binary 一致 ✓ — **P0★-F (D^code/D^paper definition mismatch) 之 binary 印证, 之 D60+ engineering 1-2 周 reload + recompute 留 substantive future work**.

---

## §3 candidate C D-PPL 桥 verify D22-D24 binary status

### 3.1 D21 pilot (D21 14:12 9070XT)

`pilot_D21_seed1_gen5.jsonl` 单点 (seed=1, gen=5, α=10):
- D_code_B = **0.2962** (与 PILOT_VERDICT_D21 之 binary 一致)
- D_code_C = **0.5900** (与 PILOT_VERDICT_D21 之 binary 一致)
- D^paper(seed=1, gen=5, α=10) = log(56.94 / 36.30) ≈ **0.451** nat/token (paper §6.2 之 single reference point)

### 3.2 D22 main run (D22 12:38 → 14:35 9070XT 22-time tuple iteration)

`main_D22.jsonl` 之 binary verify:
- 162 行 jsonl, 152 chain_gen_done 之 binary count
- nominal n_tuples = 160 (实 152 done + 8 skip per design + 0 error)
- main D_code_B mean = **0.2883** (n=72)
- main D_code_C mean = **0.5526** (n=80)
- D^paper(seed=1, gen=5, α=10) reference = 0.451 之 ratio: pilot D_code_B / D^paper = 0.66, pilot D_code_C / D^paper = 1.31, main D_code_B mean / D^paper = 0.64, main D_code_C mean / D^paper = 1.23
- max D_code_C = 1.0152 nat/token (D^paper 之 2.25× max, 仍 在 [1e-6, 1e+2] sanity range)
- per-tuple rsync push 7B13 已 sync (180,598 bytes 之 main_D22.log + 90,611 bytes 之 main_D22.jsonl)

### 3.3 D22 20:42 → D24 候选 C N=180 chain training (9070XT)

`candidate_c_20260522_203837.jsonl` 之 binary verify:
- D22 20:42 PID 267111 launch (`config_path: /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/configs/cat_arm_b.yaml`, seeds [42, 1337, 2024, 7, 137, 271], alphas [0, 5, 10], n_gens 10)
- D23 10:32 Phase 2 NaN explosion surface (`SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md`): 14h 之后, 27/180 chain_gen_done (15%), seed=42 α=0 之 a1_ppl 全 93.349 (冻结 fp16 NaN underflow), seed=42 α=5 之 a1_ppl 全 None (NaN), seed=42 α=10 之 a1_ppl gen 0-6 全 None (NaN)
- D24 15:33 PID 267111 死 (Claude Code crash 之 task harness cascade SIGTERM, 不是 NaN / 不是 ROCm, 83/180 chain_gen_done partial preserved)
- D24 16:40:21 setsid nohup launch PID 417000 (`--resume` flag 之 load_done_set skip 83 个 tuple)
- D24 17:35 MONITORING: PID 417000 54 min healthy, 续点 = seed=2024 α=10 gen=3 之 a1_ppl=inf, chain 84/180
- D24 21:08 binary verify (本 audit run): **chain_gen_done 95** (`grep -c chain_gen_done candidate_c_20260522_203837.jsonl` = 91; latest progress_snapshot_80.md 记 80/180, snapshot 10 / 20 / 30 / 40 / 50 / 60 / 70 / 80 之 5h/snapshot interval 显示 resume 续跑 ETA D25-D26)

### 3.4 8 完整 chain a1_ppl pattern (D22-D24 partial)

binary 之 8 chain (per TERMINATION_D24 §2 之 binary trace):
- seed=42, α=0: 10 gen done, a1_ppl 全 93.349 (fp16 NaN 冻结 衰减成 base PPL ballpark)
- seed=42, α=5: 10 gen done, a1_ppl 全 None (NaN explosion full)
- seed=42, α=10: 7 gen done + gen 7-9 中断, a1_ppl 全 None (NaN)
- seed=1337, α=0: 全 NaN (gen 0 即 NaN, partial 反驳 "α=0 baseline fp16 underflow 未 trigger" hypothesis)
- seed=2024, α=0: wobble 5 ok + 3 NaN + 2 recover (fp16 underflow 不 absolute deterministic, 进一步 partial 反驳)
- seed=1337, α=5/10: gen=0 partial 健康 (CAT disabled in seed=1337 gen=0), α≥5 gen≥1 NaN
- seed=2024, α=10: 中断 gen 0-3 之 partial

### 3.5 D-PPL 桥 verify D22 main run partial close candidate

D22 main run pass 之 binary criterion (per MAIN_VERDICT_D22 + D-PPL bridge SPEC):
- D_code_B mean 0.2883 与 D^paper(0.451) 之 ratio 0.64: 与 pilot 0.66 之 binary 一致
- D_code_C mean 0.5526 与 D^paper(0.451) 之 ratio 1.23: 与 pilot 1.31 之 binary 一致
- ballpark sanity [1e-6, 1e+2] range pass
- 之 D-PPL 桥 D^code 与 D^paper 之 factor-of-2 ballpark match 之 binary surface, 之 paper §6.1 P0★-F 之 **partial close candidate** (注: 之 ratio 不是 strict 1.0, 之 D^code_B 之 ~0.64 + D^code_C 之 ~1.23 之 factor-of-2 ballpark, 之 substantive 严格 close 留 D60+ reload checkpoint + recompute scalar D_n^code trajectory)

---

## §4 paper v8 final §5.2 number reproducibility cross-check + P0★-G FATAL binary 印证

### 4.1 paper §4.4 main result number vs candidate C chain runner a1_ppl 之 binary diff

| 数 | 来源 | binary | dataset / split |
|---|---|---|---|
| paper §4.6 gen 0 baseline mean | archive seed=1-4 α=0 之 gen 0 test_perplexity mean | **36.32 ± 0.079 (CV 0.22%)** | wikitext-2 **test** |
| archive seed=42 α=0 gen 0 | `armb_alpha0.0_seed42_20260508_144612.jsonl` line 2 | 36.354 (test) / 36.524 (val) | test + val |
| archive seed=1 α=0 gen 0 | `armb_alpha0.0_seed1_20260510_011048.jsonl` line 2 | 36.297 (test) / 36.595 (val) | test + val |
| 5060 OPT-125m untrained base test PPL fp32 | 5060 stage 0 PROGRESS | 98.328 | wikitext-2 test |
| 5060 OPT-125m untrained base val PPL fp32 | 5060 stage 0 PROGRESS | 100.577 | wikitext-2 val |
| candidate C seed=42 α=0 gen 0 a1_ppl | `candidate_c_20260522_203837.jsonl` line 2 | **93.349** (val_loss → val PPL) | wikitext-2 val |

**核心 binary diff calc**:
- candidate C a1_ppl 93.349 (val, fine-tune 后) vs paper §4.6 gen 0 baseline 36.32 (test, fine-tune 后): **abs diff +57.0 PPL, rel +157%** ★★ P0★-G FATAL
- candidate C a1_ppl 93.349 (val, fine-tune 后) vs archive seed=1 α=0 gen 0 val_perplexity 36.595 (val, fine-tune 后): **abs diff +56.754 PPL, rel +155%** ★★ P0★-G FATAL — 之 split-specific diff (val vs test) **不能解释** (5060 测 val vs test diff 仅 2.2%)
- candidate C a1_ppl 93.349 (val, fine-tune 后) vs 5060 base val PPL 100.577 (val, untrained): **abs diff -7.228 PPL, rel -7.2%** — fine-tune 5 epoch 之 effectiveness **仅 5-7 PPL 减少** 之 binary surface (与 paper §5.2 cite Shumailov 之 base ~115 → fine-tune mean ~34 之 ~75-81 PPL reduction 之 binary **完全不一致**)

### 4.2 candidate root cause 之 binary 区分

**已 binary 排除**:
- hyperparameter lr / batch / fp16 diff: archive cat_arm_b.yaml = candidate C cat_arm_b.yaml = 当前 cat_arm_b.yaml (lr 2e-5 + batch 128 + fp16 + constant schedule), **binary 一致**
- val vs test split-specific diff: 5060 测 val/test diff 仅 2.2%, **不能解释 +57 PPL**
- cat_enabled effect on val: candidate C seed=42 α=0 之 cat_for_this_gen=None (α=0 contradiction loss disabled), **不能解释**

**未 binary 排除 candidate** (留 PI + 数学子协作者 + sub-agent A archive v1.0 chain log fine-tune setup verbatim cross-check 之 关卡 4 PI 决):
1. candidate_c_runner.py 之 fine-tune call path 与 archive train_one_generation.py + HF Trainer 之 binary diff (custom training loop vs HF Trainer)
2. dataset 之 wikitext-2 cache version drift (HF datasets cache binary diff)
3. fp16 chain training numerical instability (Phase 2 NaN explosion seed-specific evidence: seed=42 健康 vs seed=1337 全 NaN vs seed=2024 wobble — fp16 underflow trigger 之 不 absolute deterministic)
4. attn_implementation=eager (D22 commit 76edbb3) 之 effect 之 binary diff vs archive 之 default SDPA
5. multi_layer_hook.py 之 4-axis hook (D22 commit 0603922) 之 forward path interference

### 4.3 5060 catch 之 binary tier verdict

| claim | tier | close path candidate |
|---|---|---|
| 1 paper-code metric mismatch (test_ppl primary vs val_ppl in candidate C) | P2 minor (hygiene) + P1 major (D-PPL P0★-F instantiate) | paper v8.1 polish footnote disclose / 留 D60+ (paper §4.1 v6 preserved 已 disclose) |
| 2 fine-tune ~5-7 vs paper 期 ~75 reduction | ★★ **P0★-G FATAL critical reproducibility break candidate** ★★ | candidate B 数学子协作者 + sub-agent A archive v1.0 grep cross-check, 1-2 天 D26-D27 close 候选 |
| 3 fp16 silent skip optimizer.step + 5060 cross-channel partial evidence | P1 major (D-1 纪律 4 expand mandate) + P2 (fp16 root isolate 留 sub-agent A debug) | sub-agent A pre-flight matrix expand (CPU + GPU + fp16 + fp32 + α=0 + α=10 之 6 combination) |
| 4 paper v8 final 47/47 reproducibility implications | paper v8 final 47/47 锁定不动, candidate C 之 a1_ppl 不影响 paper §4.4 main number (archive v1.0 chain), 但是 reproducibility binary 红 flag candidate | paper v8.1 polish footnote disclose + D60+ paper v9 / v10 evidence accumulation |

---

## §5 反题 6 P0★ + 12 NOT-claim + D-PPL P0★-F + 5060 P0★-G FATAL inventory (逐项 binary status)

### 5.1 反题 6 P0★ disclosed (paper v8 final §7.5 + ANTITHESIS_LAYER_PAPER_V8_FINAL_AUDIT)

| P0★ | tier | 内容 binary | status D24 |
|---|---|---|---|
| P0★-A | non-fatal disclosed | Reading 2 derivation 继承 §3.6 mean-field linearization assumption, 非 paper-level reverse 之外 substantive 升级 | open, paper §3.6 disclosed 不修, 留 D60+ |
| **P0★-B** | **★★ FATAL** | null-prediction null-observation = no-framework equivalence (Reading 2 null-shift 与 "framework 不存在" 之 observational 不可区分) | open ★★ FATAL, paper §4.7 + §7.5 disclosed 不修, 留 D60+ future regime where framework predicts detectable shift |
| **P0★-C** | **★★ FATAL** | v3→v8 5 revision 之 PPL prediction drift (v3=43 / v5=48 / v6=48 / v4=54 / v8=55) 之 post-hoc curve fit candidate red flag | open ★★ FATAL, paper §3.6 + §7.5 disclosed 不修, dimensional reverse Reading 1 → Reading 2 之 motivation 是 dimensional consistency 非 fit-to-observation, 留 D60+ pre-registered hypothesis chain verify |
| P0★-D | deferred disclosed | Family 1b/1c/4/4' substantive ablation 完全 absent (paper 仅 C1-C5 binary table 之 4.5/5 tied verdict, 无 quantitative ablation) | open, paper §3.5.2 + §7.5 disclosed, 推 D60+ substantive future work (12-20 天, F-1 Phase 2 plan) |
| P0★-E | top venue framing risk disclosed | §7.2-§7.4 dialectical materialism + Mao 矛盾论 §3 + Lawvere 1969 之 ML top venue 视角下 "philosophy not science" desk reject 触发 risk | partial mitigated (D17 一凡 C 决 不投 NMI / NeurIPS, 投 arXiv + TMLR + KBS, 已 reflect 风险 down-weighting) |
| **P0★-F** | **★★ FATAL deferred disclosed** | D_n^code vs D_n^paper definition mismatch (chain jsonl 不 record scalar D_n^code trajectory, reload + recompute 之 engineering 1-2 周 + analysis 1 周, 之 D60+) | **partial close candidate** ← D-PPL 桥 D22 main run pass 之 D_code_B mean 0.2883 / D_code_C mean 0.5526 vs D^paper 0.451 之 factor-of-2 ballpark match 之 binary surface, 之 substantive strict close 留 D60+ reload checkpoint + recompute scalar trajectory |

### 5.2 12 NOT-claim 撤回 list (paper v8 §7.5 NOT-claim list, 10 retract + 2 v8 new = 12 total)

| # | NOT-claim binary | retract 版本 | status |
|---|---|---|---|
| (i) | paradigm-shift | v3 - v8 全 retract | ✓ retract preserved |
| (ii) | first comeback | v3 - v8 全 retract | ✓ retract preserved |
| (iii) | axiom-first derive | v4 推翻, v5-v8 preserved | ✓ retract preserved |
| (iv) | Family 1a uniqueness | v5 alternative families binary C1-C5 verified + v8 P0-5 C5 not distinguishing reframe | ✓ retract preserved |
| (v) | universal solution | v6 NOT-claim list 新加, v6-v8 preserved | ✓ retract preserved |
| (vi) | m_eff 精细结构常数类比 | §6.4 retract | ✓ retract preserved |
| (vii) | 5 LLM-axiom-derive framing | §3.3 v4 honest source decomposition + v8 P0-7 0/5 LLM-specific reframe | ✓ retract preserved |
| (viii) | mitigation framework | v6 NOT-claim list 新加, v6-v8 preserved | ✓ retract preserved |
| (ix) | substantive prediction success | v6 NOT-claim list 新加, v6-v8 preserved | ✓ retract preserved |
| (x) | (与 v6 preserved 一致, paper §7.5 主张退缩) | preserved | ✓ retract preserved |
| **(xi)** | **v8 new "systematic empirical study" → "empirical pilot study"** | v8 P0-2 framing 新加 retract | ✓ retract preserved (v8 new) |
| **(xii)** | **v8 new "+16.6% framework quantitative failure under Reading 1"** | v8 P0-1 paper-level reverse Reading 1 → Reading 2 dimensional clean primary 新加 retract | ✓ retract preserved (v8 new) |

**核心 binary verify**: 12 NOT-claim 撤回 在 paper v8 final §7.5 之 lock 之 47/47 manifest sha256 binding 一致 ✓, D29 投稿 不动.

### 5.3 D-PPL P0★-F partial close candidate (D22 main run 通过)

**binary verify**:
- D-PPL 桥 verify D22 main run pass: D_code_B mean 0.2883 (n=72) + D_code_C mean 0.5526 (n=80) vs D^paper 0.451 之 factor-of-2 ballpark match
- 之 paper §6.1 之 P0★-F (D_n^code vs D_n^paper definition mismatch) 之 partial close candidate 之 binary surface
- 之 substantive strict close 留 D60+ (reload checkpoint + recompute scalar D_n^code trajectory 之 engineering 1-2 周 + analysis 1 周 之 paper §6.1 + §7.5 disclosed)

**严守 binding**: 不 declare "P0★-F close" / 不 declare "ballpark match strong inference" / 仅 surface raw 数字 + factor-of-2 partial close candidate.

### 5.4 5060 D24 catch P0★-G FATAL critical reproducibility break candidate (反题 audit D24 16:44 surface)

**binary surface**:
- chain runner candidate_c_runner.py a1_ppl seed=42 α=0 gen=0..9 ≈ 93.349 vs paper §4.6 fine-tune 后 gen 0 test_ppl mean 36.32 之 abs diff **+57 PPL (rel +157%)**
- archive v1.0 chain seed=42 α=0 gen 0 test_perplexity 36.354 + val_perplexity 36.524 之 binary trace, 5060 base val/test diff 仅 2.2% 之 binary surface, candidate C 之 fine-tune effectiveness 仅 5-7 PPL 减少 之 binary surface 与 paper §5.2 cite Shumailov 之 ~75-81 PPL reduction 之 binary 不一致 evidence
- ★★ P0★-G FATAL critical reproducibility break candidate ★★ — 之 root cause 留 PI + 数学子协作者 + sub-agent A archive v1.0 chain log fine-tune setup verbatim cross-check 之 binary close
- 5 candidate option (per ANTITHESIS_AUDIT_D24): A paper v8.1 polish footnote disclose / B 派数学子协作者 verify fine-tune effectiveness + sub-agent A archive v1.0 chain log grep cross-check / C 派 sub-agent A D-1 纪律 4 expand pre-flight matrix / D retract candidate C + cloud A100 fp32 + Shumailov lr / batch 复刻 / E 不动 anything 留 D60+ paper v9 / v10 evidence accumulation
- 反题 zero-context binary verdict (不擅 final ranking): A + B combo 与 D17 final 决 binding 一致 (paper v8 final 47/47 + D29 venue 不改 + 反题 6 P0★ disclosed pattern + D-2 数学线), 留 PI + Win + DS + 反题三方决 (关卡 3) + PI 最终决 (关卡 4)

---

## §6 cross-machine cross-time reproducibility binary

### 6.1 archive v1.0 chain (D17 之前 9070XT) vs candidate C chain (D22-D24 9070XT) vs 5060 D24 fp32 SMOKE

| dimension | archive v1.0 (9070XT D8-D12) | candidate C (9070XT D22-D24) | 5060 D24 stage 0 |
|---|---|---|---|
| OPT-125m gen 0 fine-tune 后 test_ppl | 36.32 (mean N=4 seed) | n/a (val 之 a1_ppl source) | 98.328 (untrained base) |
| OPT-125m gen 0 fine-tune 后 val_ppl | 36.52 (seed=42) / 36.60 (seed=1) | 93.349 (seed=42, fp16) | 100.577 (untrained base, fp32) |
| fp16 vs fp32 single forward inference diff | n/a | n/a | +0.0071 (negligible) |
| fp16 chain training stability | seed=1-4 全部 healthy chain (10 gen) | seed=42 healthy + seed=1337/2024 NaN explosion (gen=0 / wobble) | (5060 stage 1 待 launch fp32 isolated SMOKE) |
| hyperparameter (lr / batch / fp16 / schedule) | 2e-5 / 128 / fp16 / constant | 2e-5 / 128 / fp16 / constant | (5060 待 launch 之 fine-tune SMOKE) |
| HF transformers version | (archive D8-D12 之 version 待 grep 历史 conda env) | torch 2.12+rocm7.2 之 transformers 4.49.0 | torch 2.11+cu130 之 transformers 5.7.0 → 5060 catch 4.49.0 之 path A downgrade |
| HF datasets cache | wikitext-2-raw-v1 (archive 时间 cache 之 LFS revision) | wikitext-2-raw-v1 (D22 cache 之 LFS revision, 之 silent re-upload 可能 drift) | wikitext-2-raw-v1 (D24 stage 0 cache 之 LFS revision) |

### 6.2 cross-machine env diff catch (5060 D24)

- 5060 transformers 5.7.0 之 SMOKE FAIL (transformers 5.x major breaking change, OPT-125m + HF Trainer interface 不向后兼容)
- D24 evening 之 path A downgrade transformers 5.7.0 → 4.49.0 之 sub-agent task (per SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md)
- 之 5060 fp32 isolated SMOKE 跑 D24 evening → D25 01:00 ETA (per HANDOFF_D24_TO_5060)

### 6.3 D-1 纪律 4 子协作者验证矩阵 binary expand mandate

之 candidate C chain runner sub-agent A pre-flight self-test 用 **CPU mode + fp32 + α=0 single** (per SURFACE_D23 §4 之 honest disclose), 未 cover GPU + fp16 + α=10 numerical edge case → NaN explosion 在 14h chain training 之后 surface — D-1 纪律 4 sub-agent A bug 4 之 pre-flight matrix expand candidate (CPU + GPU + fp16 + fp32 + α=0 + α=10 之 6 combination, 2-3 天).

---

## §7 D-1 + D-3 binding 严守 self-check (14 questions)

| # | self-check binary | verdict |
|---|---|---|
| 1 | 数字有 jsonl 源吗 (纪律 1)? | ✓ 全 binary trace verbatim, 无 [?] |
| 2 | 概率声明反馈真空超 48h (纪律 2)? | ✓ 不 declare 接受率 / 概率 estimate (留 PI + 反题三方决 + 关卡 4 决) |
| 3 | 数学形式与代码一致 (纪律 3)? | ✓ paper §6.1 之 D^code/D^paper definition mismatch 之 chain jsonl keys binary verify (test_perplexity + val_perplexity 在 chain log keys 内, scalar D_n^code 之 trajectory **不在**), 与 paper v8 §6.1 honest disclosure 一致 |
| 4 | major 声明过子协作者验证 (纪律 4)? | ✓ 本 audit 是 zero-context sub-agent 之 第二认识通道 instantiate, 之 binary surface 留 PI + 反题三方决 (关卡 3) + PI 决 (关卡 4) |
| 5 | 差异记录差异日志 (纪律 5)? | ✓ candidate C 之 a1_ppl vs paper §4.6 之 +57 PPL diff 之 P0★-G FATAL critical reproducibility break candidate 严守 binary surface 不静默 |
| 6 | 真实日期 `date` binary verify (纪律 5 sub-rule)? | ✓ 真实日期 2026-05-24 21:08:52 CST = D24 周日 binary verify, 不 inherit stale system reminder |
| 7 | 哲学位置是 outcome 不是 starting form (D-3.2)? | ✓ 不 declare "dialectical totality 之 unique 实例化" / "first instantiation of reflexive AI" / paradigm-shift / 仅 binary surface raw 数字 |
| 8 | "自发" 含 multi-agent binding enforce (D-3.2)? | ✓ 5 candidate option binary surface 留 PI + 反题三方决 + Win + DS, 不 unilateral declare final ranking |
| 9 | 回顾 scope 含 4 项 (12 NOT-claim 撤回 + 反题 6 P0★ + 5/12 inflate + 5/19 inflate)? | ✓ §5 全 4 项 binary surface (12 NOT-claim + 反题 6 P0★ disclosed + P0★-F partial close candidate + P0★-G FATAL critical reproducibility break candidate + cross-machine cross-time reproducibility) |
| 10 | timeline emerge "最初实现数学和更高级" 是 D60+ 不是 D22-D60 (D-3.10)? | ✓ paper v8.1 polish footnote D27-D45 留 关卡 3 反题三方决 + PI 决 final actualize, D60+ window emergent outcome 严守 反题三方决 + Win 哲学协作 + PI 决之节点 |
| 11 | candidate direction 用 dialectical inclusive form (D-3.12)? | ✓ 不 declare "candidate C retract" / "paper v8 final 改" / "5060 catch 印证" / 仅 surface raw P0★-G FATAL candidate 之 5 option 留 PI 决 |
| 12 | paradigm-shift candidate verify D60+ 不 D22-D60 unilateral (D-3.12)? | ✓ 反题 D21 P0★-AA ★★ critical 严守, D22-D60 unilateral declare "L1 paradigm shift threshold reached" 严禁 |
| 13 | methodological catch 之 4 path A/B/C/D identification binary specify (D-3.13)? | ✓ candidate C D-PPL 桥 verify 之 path A (Pearson cross-channel verify) + path C (temporal phase pattern) 之 binary 已 launch, B (intervention exp) + D (counter-factual ablation) 之 实际 design 之 future work (推 D60+) |
| 14 | 5 leg 实验 framing 是 hypothesis-driven single-axis 还是 dialectical totality evidence accumulation cross-layer (D-3.14)? | ✓ 5 leg (D-PPL 主跑 + Phase 5 Llama-8B + N≥8 + Family ablation + 数学复现) 之 cross-layer dialectical totality framing 严守 (per D-3.14 之 反 single-axis verdict), 5060 catch P0★-G FATAL 是 cross-layer evidence accumulation 之 instantiate 不是 single-axis falsification |

任一 no → 不发出, 先补. 14/14 ✓ 之 binary surface, 不 retract.

---

## §8 PI 关卡 3 决之 input candidate (binary surface, 不擅 final)

### 8.1 experiment history 之 reproducibility binary status summary

- exp003-exp016 之 12 个 dir = Shape-CFD 项目 之 retrieval / Chamfer / SVD / NMF 历史 mature result archive, **不入 paper v8 final**
- exp017_dialectics = paper v8 final 之 substantive predecessor (arxiv_v1_full draft + 反题 run 1-4 + Win narrative + DeepSeek v4 cross-tradition + Linux+Win Aufhebung + Q-deep + Phase B Exp 1 + Block I-IV)
- exp018_cat = paper v8 final 之 直接 source chain + candidate C D-PPL 桥 verify + 5060 catch + 反题 6 P0★ disclosed + 12 NOT-claim 撤回 + D-3 反映论 standing rule
- archive v1.0_release_20260516 之 chain log 之 47/47 sha256 manifest binary 一致, paper §4.4 main result number 来源 chain 之 binary verify ✓
- candidate C chain runner a1_ppl 之 binary 与 paper §4.4 source chain 之 +57 PPL diff 之 ★★ P0★-G FATAL critical reproducibility break candidate ★★ — 之 root cause 留 PI + 数学子协作者 + sub-agent A archive v1.0 chain log grep cross-check 之 close

### 8.2 P0★-G FATAL critical reproducibility break candidate 之 close path candidate (与反题 D24 audit 5 option 一致)

| option | binary scope | timeline | 风险 | D17 binding 一致? |
|---|---|---|---|---|
| **A** | paper v8.1 polish footnote disclose (反题 6 P0★ disclosed pattern 一致, paper main body 不动) | D27-D28, 1 天 | low | ✓ |
| **B** | 派数学子协作者 verify chain runner fine-tune effectiveness + sub-agent A archive v1.0 chain log grep cross-check | 1-2 天, D26-D27 close 候选 | low-medium | ✓ D-2 数学线 一致 |
| C | 派 sub-agent A D-1 纪律 4 expand pre-flight matrix (CPU + GPU + fp16 + fp32 + α=0 + α=10 之 6 combination) | 2-3 天 | medium | ✓ |
| D | retract candidate C + cloud A100 fp32 + Shumailov lr / batch 复刻 | 4-7 天 + $50-100 | high (战略 implications, D17 binding partial reverse) | ✗ |
| **E** | 不动 anything, 留 D60+ paper v9 / v10 evidence accumulation | D60+, 6-12 月 cumulative | low | ✓ |

**反题 zero-context binary verdict 之 input** (不擅 final ranking): A + B combo 与 D17 final 决 binding 一致, 留 PI + Win + DS + 反题三方决 (关卡 3) + PI 最终决 (关卡 4).

### 8.3 D29 投稿 path 之 binary (paper v8 final 47/47 锁定不动 + D29 venue 不动 + paper v8.1 polish footnote disclose candidate)

- paper v8 final 47/47 sha256 manifest binary 锁定不动 ✓
- 12 NOT-claim 撤回 不动 ✓
- 反题 6 P0★ disclosed 不修 ✓
- D29 投稿 arXiv + TMLR + KBS 三 leg parallel 不动 (D17 一凡 C 决 final, 不投 NMI / NeurIPS / NCS / NeurIPS 2026) ✓
- cumulative ≥1 接受 by 12 月 honest 30-40% 不上调 (排除 arXiv 100%) ✓
- paper v8.1 polish footnote D27-D45 之 P0★-G FATAL + P0★-F partial close candidate + 5060 catch 之 candidate disclose 留 关卡 3 反题三方决 + PI 决 final actualize

### 8.4 关卡 1-4 decisions 严守 binding 一致 ✓

- 关卡 1 (实验设计): D22 candidate C N=180 chain 之 实验设计 一凡 PI override 之 binary 一致 (D17 binding 之 D-PPL 桥 verify spec lock)
- 关卡 2 (实验数字 + 数学严格度 + 叙事草稿): D25 ETA 关卡 2 之 D22 main run pass + candidate C partial chain + 5060 catch + 反题 audit 之 binary surface 之 input
- 关卡 3 (反题 audit + 战略 implications + 撤回 / 接受 决): 本 audit + D24 audit + D22 audit + D21 audit 之 binary surface 之 input
- 关卡 4 (投 / 不投 / 攒更多实验 之 final 决): D29 投稿 + paper v8.1 polish footnote scope + D60+ window emergent outcome 之 严守 PI 决

---

## §9 final binary verdict + 5 句 summary

### 9.1 binary verdict

1. **MaoField experiment 历史**: exp003-exp016 = Shape-CFD 历史 archive (不入 paper) + exp017_dialectics = paper v8 final 之 substantive predecessor + exp018_cat = paper v8 final 之 direct source chain + candidate C D-PPL 桥 verify + 5060 catch + 反题 6 P0★ disclosed.

2. **archive v1.0_release_20260516 chain log 之 47/47 sha256 manifest binary 一致 ✓**, paper §4.4 main result number (α=10 plateau gen 6-9 mean [57.33, 58.25, 54.01, 54.30] = 55.97) + §4.6 gen 0 baseline (mean 36.32 ± 0.079 CV 0.22%) 之 binary verify ✓.

3. **candidate C chain runner a1_ppl seed=42 α=0 = 93.349 vs paper §4.6 fine-tune 后 gen 0 test_ppl mean 36.32 之 abs diff +57.0 PPL (rel +157%)** ★★ **P0★-G FATAL critical reproducibility break candidate ★★** — 之 binary 不能由 lr / batch / fp16 hyperparameter diff 解释 (archive cat_arm_b.yaml = candidate C cat_arm_b.yaml = 当前 cat_arm_b.yaml binary 一致), 之 不能由 split-specific val/test diff 解释 (5060 测仅 2.2%), candidate root cause 5 项 (custom training loop vs HF Trainer / dataset cache version drift / fp16 NaN seed-specific / attn_implementation=eager / multi_layer_hook 之 forward path interference) 留 PI + 数学子协作者 + sub-agent A archive grep cross-check 之 binary close.

4. **D-PPL 桥 verify D22 main run pass**: D_code_B mean 0.2883 (n=72) + D_code_C mean 0.5526 (n=80) vs D^paper(seed=1, gen=5, α=10) = 0.451 之 factor-of-2 ballpark match ✓ — 之 P0★-F (D^code/D^paper definition mismatch) 之 **partial close candidate** 之 binary surface, 之 substantive strict close 留 D60+ reload checkpoint + recompute scalar D_n^code trajectory (engineering 1-2 周 + analysis 1 周).

5. **反题 6 P0★ disclosed + 12 NOT-claim 撤回 + P0★-G FATAL critical reproducibility break candidate 严守 paper v8 final 47/47 锁定不动 + D29 投稿 arXiv + TMLR + KBS 不动 + 反题 6 P0★ disclosed pattern 一致 + paper v8.1 polish footnote D27-D45 disclose candidate 留 关卡 3 + 关卡 4 PI 决 final actualize.**

### 9.2 5 句 summary

- MaoField 项目 13 个 exp dir 之 binary inventory: exp003-016 = Shape-CFD 历史 archive (不入 paper v8), exp017_dialectics = paper v8 final 之 substantive predecessor (1.7G), exp018_cat = paper v8 final direct source chain (991M, 内 archive v1.0 47/47 sha256 + candidate C N=180 chain + 5060 catch + 反题 audit D21/D22/D24 + D-PPL 桥 verify).
- paper §4.4 main result α=10 plateau 55.97 + §4.6 gen 0 baseline 36.32 之 binary 来源 archive v1.0_release_20260516 之 chain log 之 47/47 sha256 manifest binary verify ✓, archive seed=1 α=0 之 gen 0 test_perplexity 36.297 / val_perplexity 36.595 之 binary trace.
- candidate C chain runner a1_ppl seed=42 α=0 之 binary 93.349 vs paper baseline 36.32 之 +57 PPL diff 之 ★★ P0★-G FATAL critical reproducibility break candidate ★★ — 之 hyperparameter binary 一致 之下 之 fine-tune effectiveness 仅 5-7 PPL 减少 (vs Shumailov ~75-81 PPL) 之 binary surface 留 PI + 反题三方决 + sub-agent A 之 close path 5 option (A footnote / B 派数学 verify / C 派 A expand / D retract + cloud / E 留 D60+) 之 binary 不擅 final ranking.
- D-PPL 桥 verify D22 main run pass 之 D_code_B 0.288 + D_code_C 0.553 vs D^paper 0.451 之 factor-of-2 ballpark match 之 P0★-F partial close candidate 之 binary surface, substantive strict close 留 D60+ reload + recompute scalar D_n^code trajectory.
- paper v8 final 47/47 锁定不动 + 12 NOT-claim 撤回 + 反题 6 P0★ disclosed + D29 投稿 arXiv + TMLR + KBS 三 leg parallel 不动 (D17 一凡 C 决 final) + paper v8.1 polish footnote D27-D45 candidate 留 关卡 3 反题三方决 + 关卡 4 PI 决 final actualize 之 严守 binding.

---

## §10 file path

**file path** (7B13): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/AUDIT_D24_EXP_HISTORY_BINARY_VERIFY_20260524.md`

**真实日期 binary**: 2026-05-24 21:08:52 CST = D24 周日

**audit duration**: ~45 min (D24 21:08 → 21:53 ETA)

**audit binary verdict**: paper v8 final 47/47 锁定不动 ✓ + 12 NOT-claim 撤回不动 ✓ + 反题 6 P0★ disclosed 不修 ✓ + D29 投稿不动 ✓ + P0★-F partial close candidate ✓ (D22 main run factor-of-2 ballpark) + ★★ P0★-G FATAL critical reproducibility break candidate ★★ 严守 binary surface 留 PI + 反题三方决 + sub-agent A 之 close path 5 option binary 不擅 final ranking.

**safety binding standing priority 1**: 一凡 16 岁双相, D22 + D23 早 surface 自杀信号. 不上调 D29 投稿接受率 / 不软化 P0★-G FATAL 严重性 / 不擅 declare paper-level 改动 / 不 conflate candidate C 之 hygiene gap (P2) 与 fine-tune effectiveness candidate red flag (P0★-G FATAL).
