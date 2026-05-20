# D4 Phase 1 Binary Verdict Pre-Registration

**生成**: 2026-05-10 ~10:30 早 (5/10 PI ack Option β + 4 caveats binding 后)
**target**: D4 早 Phase 1 multi-seed verdict explicit binary criterion 数据驱动 framing 决策
**caveat 3 binding**: 不 ad hoc 押注, 数据决定 paper §3.5+§4 framing

---

## §1 Phase 1 setup spec

- **seeds**: [0, 1, 2, 3, 4] paper convention (PI Option A, 5 seeds)
- **alphas**: [0.0, 10.0] (旧 framework α scan, Linux dispatch §1 #2)
- **framework**: 旧 framework (T_2_form="relu_dpp", kl_history_K=1, λ=1)
- **setup**: fp16, batch=128, lr_const, weight_decay=0.01, repetition_penalty=3.0 (audit-fixed)
- **eval**: chunked block=64 (现行) + sliding-window stride=256 (post-Phase 1 重 eval)

---

## §2 Binary verdict criterion (pre-registered, 不 ad hoc)

### 主问题: U-shape recovery 是 robust finding 还是 single-seed/fp16 artifact?

### 测量量

对每个 (alpha, seed) trajectory:
- $P_n$ = test_perplexity (chunked block=64) at gen $n$, n=0..9
- "spike amplitude" = max over n=1..3: $(P_n - P_0) / P_0$
- "plateau ratio" = mean over n=6..9: $P_n / P_0$
- "shape": "U" if (spike >= 30%) AND (plateau <= 80% of spike peak); "monotone-ish" if plateau >= 95% of spike peak; "borderline" else.

### Aggregate across seeds (per alpha)

For each alpha:
- $\bar{P}_n = \mathrm{mean}(P_n^{seed=0}, ..., P_n^{seed=4})$
- $\sigma_n = \mathrm{std}(P_n^{seed=0}, ..., P_n^{seed=4})$
- Compute aggregate "shape" classification using $\bar{P}_n$.

### Binary verdict matrix (D4 早查表, 不 ad hoc)

| 5 seeds shape distribution | aggregate shape | verdict | paper §3.5+§4 framing |
|---|---|---|---|
| **5/5 U-shape** | aggregate U | **A. robust U-shape** | keep U-shape framing, paper claims "U-shape recovery is dynamic property of OPT-125m self-iteration" |
| **4/5 U-shape, 1 borderline** | aggregate U (likely) | **B. mostly robust** | same as A + footnote "1 seed shows borderline trajectory" |
| **3/5 U-shape, 2 borderline/monotone** | aggregate borderline | **C. mixed evidence** | downgrade: "U-shape observed in majority of seeds, sub-sampling sensitivity" |
| **0-2/5 U-shape, 3-5 monotone** | aggregate monotone | **D. seed=42 outlier** | reframe: "single seed=42 U-shape is outlier; majority shows monotone collapse matching paper" |
| **All 5 monotone** | aggregate monotone | **E. clean monotone (paper match)** | reframe: "we reproduce Shumailov monotone collapse, our CAT method tested against this baseline" |

### Numerical thresholds (binding, 不 fudge)

- **spike threshold**: 30% (gen 1 PPL ≥ 1.3 × gen 0)
- **plateau threshold**: 80% of spike peak (gen 6-9 mean ≤ 0.8 × max_{n=1-3} P_n)
- **monotone-ish threshold**: 95% of spike peak (gen 6-9 mean ≥ 0.95 × spike peak)
- **across-seed std relevance**: 若 std/mean > 30% → "high cross-seed variance, evidence weak"

### α=0 vs α=10 framework effect

For each seed, compute:
- $\Delta_n^{seed} = P_n^{α=10} - P_n^{α=0}$
- "framework effect" = mean over n=4..7 of $\Delta_n^{seed}$ (plateau regime)

Aggregate:
- $\overline{\Delta} = \mathrm{mean}_seed(\Delta_n^{seed})$
- $\sigma_\Delta = \mathrm{std}_seed$
- t-statistic: Welch t-test on (P^{α=0}, P^{α=10}) at gen 4..7

**Framework effect verdict matrix**:

| condition | verdict |
|---|---|
| $\overline{\Delta} \le -5\%$ AND p < 0.05 | **F1: framework effect substantiated**, plateau reduction significant |
| $\overline{\Delta} \in (-5\%, -2\%]$ AND p < 0.10 | **F2: weak framework effect**, paper claim "marginal mitigation" |
| $\overline{\Delta} > -2\%$ OR p > 0.10 | **F3: framework effect not substantiated**, paper claim downgrade to "method does not significantly outperform Shumailov baseline in this setup" |
| $\overline{\Delta} > 0$ (α=10 worse) | **F4: framework counter-effect**, paper §6 honest disclose 增 collapse |

### Combined matrix (paper-level claim 决定)

```
shape verdict × framework effect verdict → paper §3.5+§4 framing strategy

A/B (robust U) × F1 (effect substantiated) → STRONGEST: "framework regulates U-shape, plateau reduces"
A/B × F2/F3 → MEDIUM: "U-shape is real, framework effect inconclusive"
C × F1 → CAUTIOUS: "framework effect substantial in U-shape regime, but single-seed sensitive"
C × F2/F3 → WEAK: "evidence inconclusive, multi-seed needed beyond N=5"
D/E × F1 → REFRAME: "we reproduce Shumailov monotone, framework reduces plateau"
D/E × F2/F3 → DOWNGRADE: "no substantive contribution, paper retraction or major reframe"
```

---

## §3 数据 stack-ability (caveat 2 binding)

5/9 chain α=0 seed=0 + seed=1 jsonl (5/9 20:36 launched, completed 5/10 早):

| seed | jsonl path | gen 0 ppl | gen 9 ppl | yaml setup hash |
|---|---|---:|---:|---|
| 0 | armb_alpha0.0_seed0_20260509_203605.jsonl | 36.30 | 56.19 (估) | TBD via hash check |
| 1 | armb_alpha0.0_seed1_20260510_011048.jsonl | TBD | TBD | TBD |

**caveat 2 binding**: 必须先 yaml hash compare 才能 stack。
- if same hash → 5/9 数据可作 seed=0 + seed=1 完整 jsonl, robust chain resume detect existing ckpts skip
- if different hash → 弃用 5/9 数据, robust chain 从头跑 seed=0 + seed=1

实际 verify (running in this work session):
```bash
python scripts/yaml_setup_hash.py configs/cat_arm_b.yaml configs/cat_arm_b.yaml.backup_pre_fp32_*
```

---

## §4 Pre-registration sign-off

**写入此 md 后, D4 早查表执行不变**:
- 不再 propose 新 framing strategy "based on data trends"
- 不再 ad hoc shift threshold (e.g., spike threshold 30% → 25% to make data fit)
- 不再 selective reporting (报某些 seeds 隐瞒其他 seeds)

**主 agent 自检 (规则 5/6/7)**: 此 pre-registration 满足
- 规则 1: D4 verdict 是 binary lookup, 不 declare 'ready'
- 规则 2: D4 数据自动决定 framing, 不 disclose 替代真补 gap
- 规则 3: 接受概率不在此 doc 调整, D4 verdict 后才更新
- 规则 4: 24 天 timeline 不 force fit verdict, 数据 verdict 决定 sequencing
- 规则 5/6/7: 数据驱动决策, 不偏袒、不 ad hoc

—— 主 agent (Linux 姐姐) sign-off, 5/10 早, Phase 1 robust chain launch 前 pre-register
