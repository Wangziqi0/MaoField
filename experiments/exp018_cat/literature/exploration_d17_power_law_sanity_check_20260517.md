# D-2 代码线 third wave — Power-law alternative form sanity check (D17 = 2026-05-17)

- **D-day anchor**: D-day = 2026-05-01, D17 = 2026-05-17
- **真实 mtime**: 2026-05-17 (CST)
- **角色**: Linux 姐姐 D-2 代码线 third wave sub-agent (code-impl 专门 agent type)
- **波次**: D-2 代码线 third wave (一个 alternative form sketch sanity check, 不发散)
- **scope**: throwaway exploration prototype 不是 production code, N=1 gen 1 seed sanity check 不是 verification
- **D-1 binding**: 第二独立认识通道, 只能下调主协作者声明严格度, 不能上调
- **不动**: paper v8 final lock + v1.0 release archive 47/47 manifest 任何文件

---

## §1 任务 binary 完成度

| 任务 | 状态 | 备注 |
|------|------|------|
| 读 v1.0 release EMA loss 实现 reference | ✓ | `archive/v1.0_release_20260516/src/{contradiction_loss,train_one_generation,cat_trainer}.py` + `configs/cat_arm_b.yaml` read-only |
| 写 power-law alternative form sketch | ✓ | `scripts/exploration_d17_power_law/exploration_d17_power_law_loss.py` (PowerLawContradictionConfig + PowerLawContradictionTracker, 复用 v1.0 release form, 只改 T3_memory) |
| 写 1 gen 1 seed run script (OPT-125M, seed=99) | ✓ | `scripts/exploration_d17_power_law/exploration_d17_run_1gen_1seed.py` |
| 跑 script + record output | ✓ | 本机 EPYC 7B13 CPU only (torch 2.11.0+cpu), 总用时 ~4 min (smoke) + ~5 min (full), 远低于 30 min budget |
| 写 sanity check report | ✓ | 本文件 |
| 不 modify v1.0 release archive | ✓ | binary verify: 仅 read; manifest hash unchanged |
| 不动 paper v8 final lock | ✓ | binary verify: 未访问 paper v8 任何 file |

## §2 数字 binary list (sanity check finite / NaN / OOM / cache miss)

### 执行环境
- **平台**: Linux 192.168.31.36, EPYC 7B13 64-core CPU, 503 GB RAM, 无 GPU
- **torch**: 2.11.0+cpu, cuda=False, rocm=None
- **transformers**: 5.7.0
- **datasets**: 4.8.5 (newly installed for this task)
- **OPT-125M HF cache**: newly downloaded 480MB, 125.2M params load in ~4-8s
- **wikitext-2-raw-v1**: HF datasets cache, train=36718 / val=3760 / test=4358 samples

### Run 1 (α=0 baseline, contradiction loss disabled)
- **config**: seed=99, n_steps=32, batch_size=8, lr=2.0e-5, kl_update_every=4 (ignored since α=0), max_train_samples=2000, max_val_samples=256, max_test_samples=512
- **test_ppl_init** (untrained, step 0): **88.535** ✓ finite
- **test_ppl_final** (step 32): **57.204** ✓ finite
- **trajectory** (test_ppl per log_every=4 step): 88.535 → 73.76 (step 4) → 65.74 → 61.45 → 58.78 → 56.83 → 55.24 → 53.86 → 52.36 (step 32) → 57.20 (final eval 16 batches) ✓ monotone decrease (sanity ✓)
- **lm_loss** at step 32: 4.205 ✓ finite, in expected ~4 nat range
- **NaN / OOM / cache miss**: NONE ✓

### Run 2 (α=10 power-law alternative form K=5 α_powerlaw=1.0)
- **config**: 同 Run 1 + memory_form="power_law", power_law_alpha=1.0, power_law_K=5, kl_update_every=4
- **power-law weights** (computed once at init): [0.4380, 0.2190, 0.1460, 0.1095, 0.0876], $Z = 2.283$ ✓ sums to 1
- **test_ppl_init** (untrained, step 0): **88.535** ✓ finite (identical to Run 1, seed lock ✓)
- **test_ppl_final** (step 32): **58.589** ✓ finite
- **trajectory** (test_ppl): 88.535 → 72.66 → 65.10 → 61.85 → 59.46 → 58.07 → 56.26 → 55.09 → 53.96 (step 32) → 58.59 (final eval) ✓ monotone decrease
- **lm_loss** at step 32: 4.117 ✓ finite
- **contradiction_loss trajectory** (per kl_update_every=4 step, 8 logged):
  - step 4: contra_loss=0.0 (cold start, history_len=1, bar_D = D_n = 0.199)
  - step 8: contra_loss=0.0038, T3_memory=0.0019, bar_D=0.199 D_n=0.242 (history_len=2)
  - step 12: contra_loss=0.0544, T3_memory=0.0093, bar_D=0.228 D_n=0.324 (history_len=3)
  - step 16: contra_loss=0.0018, T3_memory=9.1e-6, bar_D=0.279 D_n=0.282 (history_len=4)
  - step 20: contra_loss=0.0797, T3_memory=0.0017, bar_D=0.276 D_n=0.317 (history_len=5, K reached)
  - step 24: contra_loss=0.0820, T3_memory=0.0141, bar_D=0.292 D_n=0.411 (history_len=5)
  - step 28: contra_loss=0.0028, T3_memory=1.4e-4, bar_D=0.347 D_n=0.359 (history_len=5)
  - step 32: contra_loss=0.1417, T3_memory=0.0069, bar_D=0.353 D_n=0.436 (history_len=5)
- **NaN / OOM / cache miss**: NONE ✓
- **history buffer 满 K=5 在 step 20 之后** ✓ binary: power-law alternative form 之 substantive memory window 仅 step 20-32 (13 train steps) 真 active, step 4-16 history 部分填充 fallback renormalization

## §3 qualitative comparison (binary: 数值同 ballpark / 显著偏离 / NaN)

### Test perplexity (test_ppl_final, 16 eval batches)
- Run 1 (α=0): 57.204
- Run 2 (α=10 power-law): 58.589
- **delta** = +1.384 (power-law 比 baseline 略差 1.4 ppl, ~2.4% relative)
- **binary [BOTH FINITE]** ✓
- **binary [in baseline ±50%]** ✓ (1.384/57.204 = 2.4% « 50%)
- **binary [trajectory monotone]** ✓ (两 run 都 88.5 → ~53-54 平滑 decrease)

### 与 paper v8 §4.3 expected ballpark cross-check
- paper §4.3 报 α=10 plateau N=4 mean test_ppl=55.97 SD 2.13 bootstrap CI [54.16, 57.79] (5 epoch × 5-seed × ~1406 step strict-mirror)
- 本 sanity check: 32-step subset CPU run, test_ppl_final 57.2 (baseline) / 58.6 (power-law) 都 in paper baseline ballpark **±5%** ✓
- **caveat [?]**: 本 exploration 用 2000 train samples × 32 step × batch 8 (effective ~256 sample × 32 step) 远小于 paper strict-mirror (36k blocks × 1406 step × batch 128 5 epoch), 数字 ballpark 偶然 align 不构成 statistical evidence

### Power-law memory kernel qualitative behavior
- bar_D 单调 build (0.199 → 0.353) 在 history 充满 K=5 之前, plausibly because:
  (a) early steps weights renormalized so最 recent D_n dominates (~0.44 weight on k=1)
  (b) D_n itself 在 fine-tune 中 drift (KL between current model and EMA model grows as model updates)
- T3_memory $= (D_n - \bar{D})^2$ 在 step 24 spike 到 0.0141 (D_n=0.411 远超 bar_D=0.292)
- step 32 spike contra_loss=0.142, total_loss 5.53 vs lm_loss 4.12 (contra contributes ~25% of total at α=10)
- **qualitative trend**: bar_D 之 power-law form 仍能 track D_n 之 trend, 但有 lag (history 加权过去 K=5 步, recent dominant)

## §4 binary disclaimers (D-1 binding)

- **不 declare "signal found"** — N=1 single seed sanity check, no statistical comparison possible
- **不 declare "framework α-effect 成立 in power-law form"** — paired comparison N≥8 multi-seed pre-registered hypothesis 才能 verify, 当前是 ballpark sanity 不是 verification
- **不 declare "alternative form 优于 EMA"** — 1 seed delta=+1.384 ppl 在 paper bootstrap SD ~2 ppl 内 noise level, 不构成 effect
- **不 declare "alternative form 劣于 EMA"** — 同上, 1 seed delta sign 不 distinguishable from noise
- **不 declare any framework-level claim** — paper v8 final lock 不动, 反题 P0★-A linearization gap 不动
- **本 sketch 仅 surface "power-law alternative form numerically tractable on OPT-125M scope, no NaN / OOM, in paper baseline ballpark"** — 这是 prototype feasibility check, 不是 substantive comparison

## §5 cite reference (binary text refs)

- v1.0 release `archive/v1.0_release_20260516/src/contradiction_loss.py` line 184-265 (KLContradictionTracker.compute_loss EMA-deviation form, 本 sketch 之 reference baseline)
- v1.0 release `archive/v1.0_release_20260516/configs/cat_arm_b.yaml` line 169-195 (chain 实际跑 form, 旧 framework λ=1.0 β_kl=0.9 T_2=relu_dpp K=1)
- paper v8 §3 ℒ_contradiction definition (EMA-deviation 实际 form, code-first per D-1 纪律 3)
- paper v8 §3.6 mean-field NESS analysis (long-tail memory kernel discussion, power-law $k^{-\alpha}$ form 对应 long-tail 类别)
- paper v8 §3.2 P0-1 honest disclose (EMA-deviation 与 paper §3.5 Volterra form-borrowing 不一致 disclosure)
- paper v8 §4.3 α=10 plateau N=4 mean 55.97 SD 2.13 bootstrap CI [54.16, 57.79] (本 sketch 之 baseline ballpark reference)
- 反题 v8 P0★-A linearization gap (EMA-deviation Taylor leading order 与 Klein-Gordon mass term form-borrowing partial gap, power-law alternative 之 linearization 留 D60+)
- 反题 v8 P0★-B null-prediction = no framework (本 sketch 不 解决 P0★-B, 仅 form-level alternative numerical feasibility 加固)
- 数学线 D17 third wave outline (file `MATH_LINE_D17_THIRD_WAVE_THREE_QUESTIONS_OUTLINE_20260517.md` — **本 sketch 落地时尚未 surface 到 literature/**, 本 sketch 基于 prompt 中 outline 提及的 alternative form candidate list 之 power-law decay 选项)
- Win 哲学线 D17 second wave `WIN_PHIL_LINE_D17_PRACTICE_FIRST_DEEPEN_20260517.md` (cross-tension: code 之 alternative form sanity check 与哲学线之 D-1 工作流自指 instantiate 是 D-2 三线 parallel 之 simultaneous instantiate, 不互相替代)
- HEZIMENG `CLAUDE.md` D-1 五条纪律 + D-2 三线 parallel (binding 严守)

## §6 caveat [?] list

- [?] 本 sketch 是 throwaway prototype, K=5 history 在 32 train step 内仅 step 20-32 真 fill 满, 前 steps fallback renormalization 与 EMA cold-start 行为接近 — 单 seed 之 power-law effect substantive isolation 需 chain 多 gen 才能 surface, 当前 1 gen 不可判
- [?] CPU 跑 32 step batch 8 与 paper strict-mirror GPU 1406 step batch 128 之 effective sample size 差 ~150 倍, ballpark 数字 align 是 coincidental, 不构成 reproduce paper baseline 之 evidence
- [?] power-law $\alpha = 1.0$ + K=5 是 prototype 默认参数, 未 sweep, 不构成 form 之 optimal choice claim
- [?] memory_form="power_law" 之 single-axis 改变 isolated (T1 / T2 / λ_i / β_model 全 inherit v1.0 release), 但 baseline (memory_form="ema") 在本 sketch 未单独跑 (Run 1 α=0 完全 disable contradiction loss), 所以 power-law vs EMA-deviation 之 paired contradiction-on comparison 在本 sketch scope 外
- [?] 数学线 D17 third wave outline 落地后 cross-check power-law form 是否 form-consistent — 不强制 backport, 留主会话决定是否 promote sketch 到 substantive comparison
- [?] 反题 P0★-A linearization gap (Taylor leading order form-borrowing partial) 在 power-law form 下之 leading-order analysis 在 prototype scope 外 — power-law $\sum k^{-\alpha} D_{n-k}/Z$ 之 Taylor 展开与 EMA $\beta \bar{D} + (1-\beta) D_n$ 之 leading-order behavior 是否 form-equivalent (in some scaling limit) 留 D60+ 数学层
- [?] 本 sketch 之 sanity 是 numerical tractability binary check, 不是 form 之 mathematical justification — power-law 作为 alternative form 之 motivation (long-tail memory) 在 paper v8 §3.6 仅 mention 未 derive, 本 sketch 之 numerical run 不上调 §3.6 严格度
- [?] EMA reservoir D_ema 在 memory_form="power_law" 时仍维护 (cfg.beta_kl=0.9 update), 仅作 logging cross-check (本 run log 显示 EMA D_ema 与 power-law bar_D 在 step 12+ 之后 ~30% diverge), 不进 loss

## §7 D60+ substantive future work hand-off note

如果数学线 outline 之 power-law form D60+ seed promoted (in light of e.g., framework universality test failing for EMA form, or alternative form 之 long-tail decay 在某 regime 之 mean-field NESS substantive predict capability surface), substantive paired comparison 是 D60+ work:
- N≥8 multi-seed paired (EMA-deviation vs power-law, same α / same data / same seed set)
- pre-registered hypothesis (e.g., null = no difference, alternative = power-law 之 long-tail memory 在某 generation 后 effect size > $\sigma$)
- multi-generation chain (gen 0-9 paper §4 scope, vs 当前 1 gen)
- Wilcoxon paired signed-rank 或 paired t-test on per-seed test_ppl trajectory
- power-law $\alpha$ + K 之 sweep grid (e.g., α ∈ {0.5, 1.0, 2.0}, K ∈ {3, 5, 10, 30})
- 1-2 month timeline, RunPod A100 budget ~$50-100 per arm
- 数学线 supplementary: power-law form 之 mean-field NESS Hartree closure 之 first-principles derivation (Mei-Montanari 2018 类比, paper §3.6 reference)
- 此 future work 留 一凡 + DS + 反题三方决战略 (是否 promote 到 paper v8.1+ / 留 D60+ work, 不在本 sketch 之 sub-agent scope)

---

## §8 binary 完成 ack

- 3 输出文件:
  - `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/exploration_d17_power_law/exploration_d17_power_law_loss.py` ✓
  - `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/exploration_d17_power_law/exploration_d17_run_1gen_1seed.py` ✓
  - `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/exploration_d17_power_law_sanity_check_20260517.md` ✓ (本文件)
- run log: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/exploration_d17_power_law/exploration_d17_run_log_20260517.txt`
- results jsonl: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/exploration_d17_power_law/exploration_d17_results.jsonl`
- smoke run log: `exploration_d17_run_log_20260517_smoke.txt` (8 steps preliminary)
- smoke results: `exploration_d17_smoke_results.jsonl`
- v1.0 release manifest **不动** ✓ (read-only access only)
- paper v8 final lock **不动** ✓
- N=1 sanity scope **严守** ✓ (不 declare framework α-effect, 不 declare alternative form 优劣)

—— Linux 姐姐 D-2 代码线 third wave sub-agent (code-impl, Opus 4.7, 1M context), D17 = 2026-05-17 CST, alternative form = power-law decay $\bar{D}_n = \sum_{k=1}^{K} k^{-\alpha} D_{n-k}/Z$ (K=5 α=1.0), throwaway exploration prototype binary 完成 ✓
