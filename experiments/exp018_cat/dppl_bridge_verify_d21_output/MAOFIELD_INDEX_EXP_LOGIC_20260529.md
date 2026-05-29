# MaoField D8-D29 历程索引 — 维度: 实验历程 + 逻辑 (zero-context 忠实 catalog)

**真实日期 binary** (`date '+%Y-%m-%d %H:%M:%S %Z'`): **2026-05-29 12:11:57 CST** (D29 anchor D-day 2026-05-01).

**生成 agent**: Opus 历程索引 agent (zero-context, 2 维: 实验历程 + 逻辑; 不做数学/命题/哲学/论点 4 维, 平行 agent 之 scope).

**协议 + binding**: 只忠实 catalog (不 smooth / 不挖深意); negative (FAIL / 撤回 / tier 降级 / 通道 disagreement) 与正面 claim 同等或更高 prominence; 每条目标三元组 (① tier/status ② jsonl 源 ③ 是否过 zero-context 独立通道); paper v8 final 47/47 不动; 12 NOT-claim 撤回不复活; 反题 P0★ tier 不擅升降; 0 commit/push/launch/ssh write; read-only + 1 Write.

**cluster 编号 schema** (per `D28_EXPERIMENT_INVENTORY_AND_SUFFICIENCY_AUDIT`): 2 = alpha-scan / 3 = phase1_robust / 9 = candidate_c N=180 / 10 = 5060 fp32 / 11 = 5060 fp16.

---

## §1 实验时间线表 (D8 → D29, chronological)

注: 关键数全 jsonl-traced verbatim. **negative 事实 (NaN / frozen / FAIL / terminated) 同等 prominence 标 ★**.

| 日期 | cluster / run | 关键数 (jsonl-traced) | jsonl 源 (file + 字段) | 状态 |
|---|---|---|---|---|
| **D-7 (5/7)** | Shumailov strict-mirror first | smoke 4 attempt setup error (epochs=1); 16:21 gen 0 val=67.91/test=90.72 | `logs/shumailov_no_preserve_seed42_20260507_162152.jsonl` | setup error → fix |
| **D-7 (5/7)** | Shumailov audit-pre-fix full | gen 0 val=36.730, gen 9 val=43.614/test=43.649 | `logs/shumailov_no_preserve_seed42_20260507_200657.jsonl` (11 行) | GO |
| **D-6 (5/8)** | Shumailov audit-fix rerun | gen 0 val=36.524/test=36.354; **gen 4 test = 1.7976931348623157e+308 (sys.float_info.max overflow) ★** | `logs/shumailov_no_preserve_seed42_20260508_092730.jsonl` | ★ overflow surface |
| **D-6 (5/8)** | cluster 2 armb_alpha0 seed42 full 10gen | val_ppl gen 0..9 = 36.524 / 78.250 / 109.692 / 92.707 / 72.860 / 60.595 / 58.687 / 55.464 / 56.381 / 55.332 | `logs/armb_alpha0.0_seed42_20260508_144612.jsonl` (11 行) | GO |
| **D-6 (5/8)** | cluster 2 armb_alpha10 seed42 full 10gen | val_ppl gen 0=36.524, gen 1=117.249, gen 2=223.904 (peak), gen 9=91.438 | `logs/armb_alpha10.0_seed42_20260508_192435.jsonl` (11 行) | GO |
| **D-5 (5/9)** | cluster 2 α=1/5 seed42 full | α=1: g0=36.524, g9=55.933; α=5: g0=36.524, g9=62.908 (U-shape: α=5 mid worse) | `logs/armb_alpha{1,5}.0_seed42_*.jsonl` | GO |
| **D-5 (5/9)** | cluster 2 α=50 seed42 | **仅 run_start 1 行, gen 0 未完 (break) ★** | `logs/armb_alpha50.0_seed42_20260509_092134.jsonl` (143 bytes) | ★ break |
| **D-5 (5/9)** | armb_alpha0 seed1337 | **仅 g0 val=36.544, retry failed ★** | `logs/armb_alpha0.0_seed1337_20260509_155044.jsonl` (2 行) | ★ break |
| **D-4~D-2 (5/10-12)** | cluster 3 phase1_robust multi-seed | α=0 seed{0,1,2,3,4} + α=10 seed{0,1,2,3,4} × 10gen; α=0 seed=1 g0 val=36.595/test=36.30; **α=10 seed=0 仅 g0 (2 行) → F3 source N=4 不是 N=5 ★** | `logs/armb_alpha{0,10}.0_seed{0-4}_*.jsonl` (17 chain + 1 audit) | GO (1 cell deficit ★) |
| **D-2 (5/12)** | exp016 → MaoField reranker 转向 | Shape-CFD 诊断 (D-day 前历史) | `exp016_diagnostic/` | (不入 paper v8) |
| **D16 (5/16)** | archive v1.0_release_20260516 freeze | 47 file manifest.sha256, **47/47 sha256 全 OK (本 agent 未重验, 多 audit 已验)**; host22_backup 10/10 EQ | `archive/v1.0_release_20260516/manifest.sha256` | locked (paper v8 binding) |
| **D17 (5/17)** | exploration_d17_power_law main | α=0 (seed=99, 32 step): init=88.535, final=57.204; α=10: final=58.589 + 8-step contradiction_log (T1/T2/T3) | `scripts/exploration_d17_power_law/exploration_d17_results.jsonl` (2 行) | GO |
| **D21 (5/21) 14:12** | D-PPL pilot (9070XT, fp32) | **D_code_B = 0.2962167025671511** (ratio 0.66 vs D^paper 0.451); **D_code_C = 0.5899820340218606** (ratio 1.31); 20 sec total, n_error=0 | `pilot_D21_seed1_gen5.jsonl` (4 行); `PILOT_VERDICT_D21.md` | GO (pilot pass ✓) |
| **D22 (5/22) 09:37-10:00** | D-PPL main run (9070XT) | 160 tuple_done (8 skip per design); **D_code_B mean 0.2883 (n=72)**, **D_code_C mean 0.5527 (n=80)** vs D^paper 0.451 (ratio 0.640 / 1.226 factor-of-2 ✓); watchdog exit 0, 0 kill, 24 min | `main/main_D22.jsonl` (162 行); `main/watchdog.audit.jsonl` | GO |
| **D22 (5/22) 20:31** | candidate_c preflight (CPU fp32) | gen 0 **a1_ppl=78.29159504124766**, gen 1 a1_ppl=99.285 + a6_ema_divergence 12-layer finite | `candidate_c_preflight/candidate_c_20260522_203111.jsonl` (4 行) | GO (preflight CPU+fp32+α=0 only ★ — gap) |
| **D22 (5/22) 20:38:37** | cluster 9 candidate_c launch (9070XT fp16, PID 267111) | seeds=[42,1337,2024,7,137,271], alphas=[0,5,10], n_gens=10 = 180 grid; first gen 12% @ 60 sec, ETA ~D23 11:30 | `LAUNCH_CANDIDATE_C_STARTED_D22.md`; `candidate_c/candidate_c_20260522_203837.jsonl` | launch |
| **D22-D23** | candidate_c seed=42 α=0 10gen | **a1_ppl 全 93.349 frozen (10 代, Δ gen1-gen0 = −2.67e-4, span 1.51e-3) ★ frozen** | `candidate_c/..._203837.jsonl` line 2-11 | ★ frozen (= base PPL) |
| **D23 (5/23) 10:32** | NaN explosion surface | 27/180; seed=42 α=5/10 **a1_ppl 全 None (NaN) ★**; nohup `loss=0.0, grad_norm=nan, eval_loss=nan` | `SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md`; `candidate_c.nohup.log` (5.1 MB) | ★ NaN explosion |
| **D24 (5/24) ~15:33** | PID 267111 死 | **83/180 (46%) partial; 死因 = Claude Code crash task harness SIGTERM (一凡 ack "claudecode 炸了"), 非 NaN/非 ROCm ★ terminated** | `TERMINATION_D24_15_33_PARTIAL_RUN_20260524.md` | ★ terminated (external) |
| **D24 (5/24) 16:40** | resume launch (PID 417000, --resume) | load_done_set skip 83 tuple; 17:35 healthy 续点 seed=2024 α=10 gen=3 a1_ppl=inf | `RESUME_LAUNCH_D24_16_40_20260524.md`; `MONITORING_D24_17_35_20260524.md` | GO (resume) |
| **D24 (5/24) 14:25-14:56** | cluster 10 5060 stage 0 (fp32, untrained base) | OPT-125m base test PPL=98.328, val PPL=100.577 (untrained); fp16 vs fp32 single forward diff +0.0071 | `PROGRESS_D24_5060_STAGE0_VAL_PPL.md` | GO |
| **D24 (5/24) 17:09** | 5060 fp32 chain launch FAIL | **TypeError: TrainingArguments got unexpected kwarg 'evaluation_strategy' (transformers 5.7.0 vs 9070XT 4.49.0 major diff) ★ launch fail** | `SURFACE_D24_5060_FP32_LAUNCH_FAIL_TRANSFORMERS_VERSION_DIFF.md` | ★ launch fail → path A downgrade |
| **D24 (5/24) ~18:11** | cluster 10 5060 fp32 SMOKE/R1 (cold) | seed=42 α=0 gen 0 **a1_ppl=36.53597375534226** (严格命中 paper §4.6 36.32); elapsed 30862.59 s (8.57h cold) | `candidate_c_20260524_173559.jsonl` (3 行) | GO |
| **D25 (5/25) 04:14** | cluster 10 5060 R1 SMOKE (fp32+gc, warm) | gen 0 a1_ppl=36.53597375534226 **bit-identical D24**, 39.4 min warm | `candidate_c_20260525_113506.jsonl` (3 行) | GO (bit-identical) |
| **D25 (5/25) 09:16** | MATH_VERIFY GradScaler skip | 数学 verify: fp16 GradScaler skip optimizer.step → weight 不 update → a1_ppl = base PPL 93.349 ★★★★★ strong; Volterra K=9 hypothesis 排除 (no_grad, metric only) | `MATH_VERIFY_D25_GRADSCALER_SKIP_20260525.md` | verdict (数学子协作者) |
| **D25 (5/25) 12:10** | cluster 9 cell B (resume 续点) | RESULT_CELL_B + CUDA context stale fail → resume | `RESULT_CELL_B_D25_12_10_20260525.md`; `RESUME_AFTER_CELL_B_AND_CUDA_CONTEXT_STALE_FAIL_D25_13_22_20260525.md` | ★ CUDA stale fail → resume |
| **D25 (5/25) 16:03-19:04** | cluster 10 5060 E0 disentangle (fp32+gc, 2gen) | gen 0=36.53597375534226 (bit-identical); **gen 1 a1_ppl=78.57167674109238 (+42.04 PPL, 2.15× lift, +115.05%)** → **S3 chain-runner-broken hypothesis REFUTED ★** (4 outcome criterion 命中 (2)) | `SMOKE_E0_..._20260525.md`; `candidate_c_20260525_160321.jsonl` (4 行) | GO (S3 REFUTED) |
| **D25-D26** | cluster 9 PID 491900 (resume continue) | D25 alive; D26 11:49 = 158/180; α=5/10 高 NaN rate ~95% | (PID 491900 chain) | GO (NaN continue) |
| **D26 (5/26) 11:35** | NaN cascade same-source verdict | PID 491900 NaN = D23 Phase 2 **same source ✓**; 34 min/gen = fp16 normal cadence (L1 "stuck retry loop" 误判主动校正 ★); α continue > β fp32 > γ retract | `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23_20260526.md` | verdict |
| **D26 (5/26) 16:49** | full data audit (4 cells) | candidate_c 173 行 alive; **4 cells bit-identical a1_ppl=93.38780852810248** (1337/10, 2024/0, 7/10, 137/0) | `MAOFIELD_FULL_DATA_AUDIT_20260526.md` (697 行) | snapshot (4 cells) |
| **D26 (5/26) ~21:00** | cluster 9 N=180 finalize | **180/180 chain_gen_done; valid 33; null 147 (本 agent python 实算 binary verify ✓)**; **5 cells bit-identical** (+seed=271 α=10) | `candidate_c/candidate_c_20260522_203837.jsonl` (186 行 / 335356 bytes) | done (N=180) |
| **D27-D28 (~5/27-28 00:34)** | cluster 11 5060 fp16 SMOKE | gen 0 a1_ppl=36.537707256599994, gen 1=78.07346793600594 (**+113.7% lift, GradScaler skip NO, grad healthy ★ → cross-platform fp16 universal failure 否决**) | `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER_20260527.md` (**jsonl file 缺失, data 在 md table only ★ P2 gap**) | GO (anchor 1 否决) |
| **D28 (5/28)** | 4 端 + deep + ablation audit | 4 端 cross-channel 一致 (3 schema gap NOT inflate); F1 pass Stack A, F2/F3/F4 refuted Stack B, F5 pending D60+; paper v8 F3 N=4 not N=5 honest surface (P0) | `D28_4ENDPOINT_*` / `D28_EXPERIMENTAL_DEEP_AUDIT_*` / `D28_CROSS_VERIFY_ABLATION_*` | audit |
| **D29 (5/29)** | L0 rigorous proof round (平行 math agent) | L0-1/2/3/4/8 proof + **L0-5/6/7 FAIL verdict ★** (本 agent 不评数学维, 仅 catalog 存在) | `MAOFIELD_L0_*_20260529.md` | (数学维, 不展开) |

---

## §2 逻辑依赖图 (文字: build-on 链 + tier 降级链 + 反题 catch 链)

### §2.1 实验 build-on 链 (谁依赖谁)

```
cluster 2 (alpha-scan D8-9, single-seed U-shape)
   └─→ cluster 3 (phase1_robust D10-12, N=5 multi-seed)  ← paper v8 §4.4/§4.6 main result source
          └─→ archive v1.0 (D16 freeze, snapshot of cluster 2+3, 47/47 sha256)  ← paper v8 final binding
                 │
                 ├─→ D17 exploration_d17_power_law (单独探索, 不入 main result)
                 │
                 └─→ D21 pilot (D-PPL 桥 D^code vs D^paper, single tuple)
                        └─→ D22 main run (160 tuple, factor-of-2 ballpark)  ← P0★-F partial close candidate
                        └─→ D22 candidate_c (cluster 9, N=180 chain, 4-axis a1/a2/a3/a6)
                               ├─→ [D23 NaN explosion] → [D24 external terminate] → [D24 resume PID 417000] → [D26 PID 491900 finalize N=180]
                               └─→ cross-stack disentangle:
                                      ├─ cluster 10 (5060 fp32: D24 SMOKE / D25 R1 / D25 E0)  ← S3 REFUTED + paper §4.6 命中
                                      └─ cluster 11 (5060 fp16: D27-D28)  ← cross-platform fp16 universal 否决
```

### §2.2 推理链 (闭环咬合, 实验侧)

- **GradScaler skip 闭环** (数学-code-实验 三端): MATH_VERIFY D25 (数学 derive: skip → weight frozen → a1_ppl = base PPL) ← 9070XT seed=42 α=0 a1_ppl=93.349 = base PPL 93.349 bit-identical (实测) ← 5060 fp32 36.536 命中 paper §4.6 (cross-validate, fp32 bypass GradScaler).
- **S3 chain-runner-broken hypothesis 降级链**: D25 14:30 §8(d) tier ★★★★★ most critical → D25 19:05 E0 gen1=78.572 (+42 PPL lift) → **REFUTED ★** (frozen weight 不可能 produce +42 lift). chain runner working as Shumailov design.
- **4 候选 root cause tier 移动** (D25 14:30 → post-E0): (d) chain-runner-broken ★★★★★ → **REFUTED**; (a) ROCm gfx1201 ★★★ → **★★★★ upgrade**; (b) fp16 GradScaler skip ★★★★ → **★★★★★ upgrade**; (c) eager attn ★★★★ → ★★★ (未 isolate).
- **anchor 1 否决链**: cluster 11 5060 fp16 healthy chain (+113.7% lift, GradScaler skip NO) → 否决 "cross-platform fp16 fundamental" (anchor 1) → ROCm-side specific manifest (anchor 4) 强证.

### §2.3 measure-theoretic 严格度档位降级链 (L1 → L0 尝试 → 部分 FAIL)

- **L1 (formal definition + empirical witness, 无 measure-positivity proof)**: paper v9 §6.1 formal def + §6.2 5-cells empirical witness lower bound — **可 actualize within D29-D60** ✓.
- **L0 (stricter, measure-positivity proof)**: 需 multi-stack ablation grid 8-cell — **不可 actualize within D29-D60, 留 D60+**.
- **L0 proof round D29 (平行 math agent)**: L0-1/2/3/4/8 proof 完成 + **L0-5/6/7 FAIL verdict ★** (`MAOFIELD_L0_L0-5-6-7_FAIL_VERDICT_20260529.md`) — negative 同等 prominence; 本 agent 不评数学正确性 (数学维 scope), 仅 catalog 该 FAIL 之存在.

### §2.4 反题 catch 链 (时间序, inflate 复发监控)

| 时间 | catch 事件 | 方向 | 源 |
|---|---|---|---|
| **5/12** | 17-23% NMI inflate (单通道自评 upward drift, Shumailov 同构) → forced retract | inflate ↓ | (历史, 反题 audit binding 引用) |
| **5/19** | 5-leg parallel 80-92% cumulative inflate → D20 sub-agent Y catch → retract 30-40% | inflate ↓ | (历史) |
| **D21 16:41** | 一凡 8 reflexive insight cascade momentum → **P0★-AA ★★ critical: D22-D60 unilateral declare "L1 paradigm shift" 严禁** | preemptive | `ANTITHESIS_AUDIT_D21_16_REFLEXIVE_INSIGHTS_20260521.md` |
| **D22** | candidate C N=6 not N=8 (5/19 inflate jump 模式避免); candidate B underpowered NOT recommended (5/12 复发 risk) | preemptive | `ANTITHESIS_AUDIT_D22_FULL_FLOW_20260522.md` |
| **D24** | 5060 catch → **P0★-G FATAL critical reproducibility break candidate** surface (a1_ppl 93.349 vs paper 36.32, +57 PPL) | surface ↑ severity | `ANTITHESIS_AUDIT_D24_5060_CATCH_P0G_20260524.md` |
| **D26 (关卡 3 Channel D)** | **D29 v9 cumulative ≥1 by 12月 60-75% claim → "YES INFLATED ✗ retract 必" → 改 25-40% main / 50-65% workshop / cumulative 25-40% honest (−30~35pt) ★** | inflate ↓ (= 任务 "μ=40 reverse-inflate" 之 D29 reverse) | `ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT_20260526.md` (line 138) |

注: 任务 prompt 称之 "D29 μ=40 reverse-inflate" 之 binary 对应 = D26 关卡 3 三方决之 cumulative 60-75% → 25-40% retract (Channel D verbatim "YES INFLATED ✗ retract 必"); 三方 spread (Win [?] / 反题 25-40% / DS 10-20%) 全 ≤ 初始 claim, 全 retract 方向. ("μ=40" literal token 本 agent grep 未命中 reverse-inflate 上下文; nearest = math verify N=40 power ρ=0.5→0.92.)

---

## §3 跨 md 矛盾清单 (同等 prominence, 每条两端数字 + 出处 + reconcile 状态)

| # | 矛盾 | 端 A | 端 B | reconcile? |
|---|---|---|---|---|
| **1** | candidate C 实验编号 nomenclature | "180 chain training run" | "18 chain × 10 generation" | ✓ reconciled — 同物 (6 seed × 3 α = 18 chain, × 10 gen = 180 records). `ANTITHESIS_AUDIT_D22` 标 ★ nomenclature catch. **任务 prompt 之 "N_total 292 vs 1460" 非此** (见 #5). |
| **2** | 9070XT vs 5060 fp32 PPL diff (base reference) | **+57.029 PPL / +157.0%** (base = paper §4.6 mean 36.32) — `MAOFIELD_FULL_DATA_AUDIT` §11.7 line 610 + V81 §4.2 | **+56.81 PPL / +155.5%** (base = 5060 fp32 jsonl 36.53597) — `PAPER_V9_SKELETON` §5.2 line 120 | ✓ reconciled — **partial schema drift, NOT data inflate**. 2 valid base (cross-validate vs jsonl raw), abs diff 0.22 PPL. `D28_4ENDPOINT` §7 Error 1 + `D28_CROSS_VERIFY_ABLATION` §1.2 Inconsistency 1 binary surface. 留 paper polish unified disambiguate. **(此即任务 "56.864 vs 56.81" 之实际数对: 56.813 vs 57.029)** |
| **3** | F3 statistical p 值 | paper v8 F3 **p = 0.818** (paired/permutation under different null) — `MAOFIELD_FULL_DATA_AUDIT` §10.2 line 506 | **p ≈ 0.62** (Welch's t≈0.524, two-sided, raw re-aggregate) — `D28_EXPERIMENTAL_DEEP_AUDIT` §3.1 line 181-183 | ✓ reconciled — different test statistic, **实质 verdict 一致 (null effect direction)** ≡ paper v8 §6 negative result. partial discrepancy explicit disclosed (D-1 纪律 5). |
| **4** | candidate C valid/null 计数 (跨时间快照) | D26 16:49: 173 行 alive, ~31 valid (158/180 D26 evening) — `MAOFIELD_FULL_DATA_AUDIT` | D27 finalize: **180/180 done, 33 valid, 147 null** — `PAPER_V9_SKELETON` §1; **本 agent python 实算 33/147 binary confirm** | ✓ reconciled — 时间 progression (chain alive snapshot → N=180 finalize), NOT inconsistency. (D28 deep audit C 端记 34 valid / 146 null = D27 21:35 snapshot 之 1-entry 差, quote timing 差异.) |
| **5** | 训练 step 数 (N_total per chain) | brief 早估 "5 × 1460 step = 7300" (基于 wrong block 数) | **实际 ≈ 292 step** (5060 SMOKE n_tokens_train=2390656 反推) — `MATH_VERIFY_D25` §1.3 line 70 + 405 | ✓ reconciled (D-1 纪律 5 错误 surface). 注: 同 MATH_VERIFY §4.3 line 292 又用 "5 epoch × 292 ≈ 1460 total step" 之 Bernoulli 序列 — **同 file 内 292/gen vs 1460/chain 之 inconsistency partial 残留 (292 是 per-gen step, 1460 是 5-epoch-chain 累计? 文内未完全 disambiguate) ★ 未完全 reconcile**. (此即任务 "292 vs 1460".) LAUNCH_CANDIDATE_C §3.3 又记 "training step 176/1460 (12%)" + §4.2 "1460 steps per training generation (5 epoch × 292 step)" — **1460/gen vs 292/gen 跨 file 不一致 ★**. |
| **6** | 9070XT seed=42 α=0 frozen 值 (跨 chain run) | D22 candidate_c: **93.349** frozen 10 代 | D25-D26 PID 491900: **93.38780852810248** (5 cells) | ✓ reconciled — 2 不同 chain run, abs diff 0.038 PPL ≈ 0.04%, within fp16 GradScaler skip deterministic regime small accumulator variation. `D28_CROSS_VERIFY_ABLATION` §1.2 Inconsistency 2 (F9). |
| **7** | bit-identical cells 计数 | **4 cells** (D26 16:49 snapshot, 158/180) — `MAOFIELD_FULL_DATA_AUDIT` §7.4 | **5 cells** (D27 finalize, +seed=271 α=10) — `PAPER_V9_SKELETON` / `DEEP_SYNTHESIS` | ✓ reconciled — 时间 progression (N=180 完成后加入 seed=271 α=10 cell), NOT inconsistency. |
| **8** | ROCm GitHub issues cite 数 | **5 documented instance** (战略全景 §4.5 P19 strict scope) — `PAPER_V81_FOOTNOTE` §2.1 | **11 GitHub issues** (cumulative: LITERATURE §4 之 7 + adjacent 4) — `PAPER_V9_SKELETON` §2.4 | ✓ reconciled — cumulative vs disambiguate scope 之 cite schema 不一致. 留 paper polish: 5 main text + 6 supplementary = 11. |
| **9** | anchor naming schema | SMOKE: anchor 1 (cross-platform fp16) / anchor 4 (ROCm-side) — `SMOKE_5060_FP16` §3 | LITERATURE: A1-A5 (5 核心 anchor) — `LITERATURE_SEARCH_PAPER_V9_ANCHORS` | ✓ reconciled — SMOKE anchor 4 = LITERATURE A4 (cross-stack 复现性) strong mapping; SMOKE anchor 1 vs A1 partial refute. 留 paper polish unified A1-A5. |
| **10** | 5/12 master synthesis plateau Δ | master synthesis: α=10 g6-9 mean **57.32** / Δ_plateau **-4.2%** | jsonl 实测: **56.43** / **-1.71%** (差 ~2×) — `GROUND_TRUTH_INVENTORY` line 147 `[!]` | ⚠ surfaced 未 reconcile — master synthesis 偏夸大 ~2×, GROUND_TRUTH md explicit `[!]` 标. 留 PI / 反题三方决. (历史 D12 数据, 不影响 paper v8 final archive.) |

**矛盾总数: 10** (8 已 reconcile + 2 未完全 reconcile: #5 step 数 292 vs 1460 同 file/跨 file 残留 ★, #10 5/12 master synthesis -4.2% vs -1.71% surfaced 留 PI).

---

## §4 NaN / frozen / 间歇 现象专节 (negative 实验事实同等保留)

### §4.1 frozen 现象 (seed=42 α=0, 9070XT fp16)

- cluster 9 candidate_c seed=42 α=0 gen 0..9 **a1_ppl 全 ≈ 93.349 frozen** (gen1-gen0 Δ = −2.6707e-4, 10-gen span = 1.513e-3 PPL). 源: `candidate_c/..._203837.jsonl` line 2-11.
- 数学机制 (MATH_VERIFY D25 ★★★★★ strong): fp16 GradScaler 检测 grad NaN/Inf → skip optimizer.step → weight 不 update → fine-tune-after a1_ppl ≡ base model PPL 93.349 (bit-identical, 实测).
- ROCm 源码追踪 (D28 §4.1): 4 关键 op (hipBLAS GEMM / MIOpen LayerNorm / OPT eager softmax / GradScaler) **全 fp32 累加器** ✓ — NaN root **不在** fp16 累加器, 必在第 0 层 OPTDecoderLayer 输出之后 (a2[0] valid + a2[1..11] NaN, layer-wise hook 留 D60+ ssh 22).
- 一凡 D27 reframe (跨端一致): "ROCm GradScaler skip frequent 不是 ROCm bug, 是 ROCm mathematically stricter numerics 正确 catch fp16 真问题; NVIDIA cu130 looser numerics silently tolerate." (ealier "ROCm 有 bug" framing **D27 自 retract ★**.)

### §4.2 NaN explosion (α>0 + seed-specific, 9070XT fp16)

- **D23 surface**: 14h chain, 27/180; seed=42 α=5/10 a1_ppl 全 None; nohup `loss=0.0, grad_norm=nan, contradiction/D_n=nan`. 源: `SURFACE_D23_CANDIDATE_C_NAN_EXPLOSION.md`.
- **D26 same-source verdict**: PID 491900 NaN = D23 same source ✓ (5 同源证据); **34 min/gen = fp16 normal cadence, NOT retry loop (L1 误判主动校正 ★)**. 源: `DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23`.
- **final N=180 NaN rate** (D28 §3.2 + 本 agent python 实算): valid 33 / null 147; α=5 + α=10 之 **~95% NaN rate** (仅 gen 0 valid, gen≥1 全 NaN).
- **seed-level 50-50 split** (seed × α=0): seed 42/137 = 10/10 valid (frozen); seed 2024 = 7/10 partial (间歇); **seed 7/271/1337 = 0/10 全 NaN cascade ★**. fp16 underflow trigger 之 init weight + data ordering interplay, seed-dependent threshold.

### §4.3 间歇 (wobble) 现象 (seed=2024 α=0)

- seed=2024 α=0 gen 0..9 a1_ppl = **ok,ok,ok,ok,ok,NaN,ok,NaN,NaN,ok ★** (transient NaN + recover). 源: `TERMINATION_D24` §2.1 + `MAOFIELD_FULL_DATA_AUDIT` §7.3 (gen 5 null, gen 6 valid, gen 7 null, gen 8 val_loss=30.34 异常 a1_ppl=null, gen 9 valid).
- 数学 (MATH_VERIFY §4.4): base = generation_0_best 固定 (yaml base_model_for_each_generation), chain cumulative drift 不 propagate → 某代 NaN 之后 又 recover finite 之 可能.

### §4.4 5 cells bit-identical (negative-adjacent reproducibility 红 flag)

- **5 cells a1_ppl = 93.38780852810248** (14 位) ≡ val_loss = 4.5367608070373535 ≡ n_tokens (2390656/16384), 跨 4 seed × 2 α: (1337,10,0)/(2024,0,0)/(7,10,0)/(137,0,0)/(271,10,0). 源: `candidate_c/..._203837.jsonl` line 51/61/114/125/175 (D28 §2.2 verbatim).
- **F2 refuted ✗** (5 cells distinct count = 1, physically impossible without frozen-weight/cache); **F3 refuted ✗** (a3_attn_entropy 5 cells distinct 5/5 at ~10⁻³ scale → 否决 (c) eval cache strong form; PPL functional 之 measure-theoretic ill-posedness weak empirical witness).

### §4.5 其他 negative 实验事件 (同等 prominence)

- **D8 gen 4 test = 1.7976931348623157e+308** (sys.float_info.max overflow), `shumailov_no_preserve_seed42_20260508_092730.jsonl`.
- **D9 α=50 break** (仅 run_start) + **seed=1337 retry failed** (仅 g0).
- **cluster 3 α=10 seed=0 仅 g0** (last_gen=0) → paper v8 F3 source **N=4 not N=5 ★ P0 honest surface** (留 paper v8.1 footnote, `D28_EXPERIMENTAL_DEEP_AUDIT` §3.1).
- **D24 PID 267111 external terminate** (Claude Code crash, 非实验内因).
- **D24 5060 fp32 launch FAIL** (transformers 5.7.0 vs 4.49.0 API diff).
- **D25 CUDA context stale fail** (cell B 之后) → resume.
- **D29 L0-5/6/7 FAIL verdict** (数学维, 平行 agent scope, 仅 catalog 存在).

---

## §5 file path + metadata

**file path** (7B13): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/MAOFIELD_INDEX_EXP_LOGIC_20260529.md`

**生成**: Opus 历程索引 agent (zero-context, 实验历程 + 逻辑 2 维), 2026-05-29 D29.

**binding final ack**: paper v8 final 47/47 不动 + 12 NOT-claim 撤回不复活 + 反题 P0★ A-G tier 不擅升降 + D29 投 arXiv+TMLR+KBS 不动 + 0 commit/push/launch/ssh write + read-only + 1 Write. negative (NaN / frozen / FAIL / 撤回 / tier 降级 / 通道 disagreement / 矛盾) 同等或更高 prominence 严守, 不 inflate by omission. 全 unilateral declare (P0★-G root close / paper-level 改动 / α-β-γ 决 / 数学正确性) 留 PI + 反题三方决 + 平行 agent.
