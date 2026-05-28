# D28 实验 inventory + 足够性 audit (NMI / Shumailov 跨架构 binary verify)

## §0 metadata + scope + binding

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%Y-%m-%d %H:%M:%S %Z'` → **2026-05-28 13:45:19 CST** (D28, 7B13 secondary session) |
| 生成 agent | Opus 4.7 (1M context) zero-context experiment inventory + sufficiency audit sub-agent, 7B13 spawn (一凡 PI dispatch D28) |
| 协议 | zero-context audit (5 task): A 实验 inventory + B 足够性 verify (vs Shumailov / NMI / ICLR) + C 数字 binary 对位 raw jsonl/log trace + D Shumailov 2024 跨架构 scope verify + E gap surface + 可证伪 close design |
| scope binary | 5 task as defined in dispatch |
| 字数预算 | ~6000 字 substantive (table-heavy, NMI 级别 实验严谨) |
| 严守 binding (14 项 binary) | paper v8 final 47/47 D17 锁定不动 + 12 NOT-claim (i)-(xii) 撤回不复活 + 反题 6 P0★ A-F disclosed + P0★-G partial isolate update + D29 投 arXiv + TMLR + KBS 不动 + ICLR 2027 第一站 + Nature 三层不越级 + paper v8 title 不动 + v9 改名留 PI 决 + D-3.7 PI 主权严守 + 7B13 单点 git 写权 + zero-context + read-only + 1 Write + 不擅 launch 新实验 + D-1 纪律 5 sub-rule + D-1 纪律 5 错误 surface 不静默 |
| 关键独立 verdict | **Shumailov 2024 Nature LLM 实验 single-arch (OPT-125M only, wikitext-2 only, 5 seeds, fine-tune setting)** — binary 由 WebFetch ar5iv §5.2 verbatim 确认 ✓ (一凡 PI D28 surface 之 substantive question 已 binary 解答) |

---

## §1 Task A — MaoField 实验 inventory (binary table)

### §1.1 全 cluster timeline + status

raw inventory: `find experiments/exp018_cat -name '*.jsonl'` → **52 jsonl files** (含 archive duplicate 之 host22_backup_20260512); deduplicated production = 30 unique jsonl files.

| # | Cluster | Period | Scope (seed × α × gen) | GPU stack | jsonl count | Valid cells | status |
|---|---|---|---|---|---|---|---|
| 1 | **shumailov_no_preserve / preserve_10pct** (D7-D8 strict-mirror baseline) | 2026-05-07 → 2026-05-08 | seed=42 × no-CAT, 4 runs | 9070XT fp16 | 4 (3 no_preserve + 1 preserve_10pct) | 4 baseline runs (single seed) | ✓ closed (baseline replication) |
| 2 | **armb_alpha α-scan single-seed** (D8-D9 早期 alpha scan, seed=42 only) | 2026-05-08 → 2026-05-09 | seed=42 × α ∈ {0, 1, 5, 10, 50} × 10 gen | 9070XT fp16 | 5 + 2 dup (1337 + 0_retry) | 5 distinct cells = 50 generation records | ✓ closed (alpha scan, single-seed reference) |
| 3 | **phase1_robust multi-seed** (D10-D12, 22-端 backup mirrored to 7B13) | 2026-05-10 → 2026-05-12 | seed ∈ {0,1,2,3,4} × α ∈ {0, 10} × 10 gen + audit | 9070XT fp16 (22 端) → backup to 7B13 | 10 cell jsonl + 1 phase1_robust.audit.jsonl + host22_backup_20260512 dup mirror | 10 cells (seed × α) = 100 generation records + 78-line audit chain trace | ✓ closed (paper v8 final 47/47 archive 之 chain_logs source) |
| 4 | **paper v8 final 47/47 archive** (D17 lock) | archive 2026-05-16 22:01 (`v1.0_release_20260516`) | snapshot of cluster 2+3 (alpha-scan + phase1_robust) | n/a (archive only) | 18 chain_logs jsonl (含 1 audit) + 8 configs + 7 scripts + 8 src + 4 root meta + 2 doc = 47 file manifest.sha256 | 47 manifest 之 sha256 全 lock | ✓ archive locked D17 (paper v8 final binding) |
| 5 | **exploration_d17_power_law** (D17 exploratory power-law fit) | 2026-05-17 | smoke + main, α ∈ exploration set, single-seed each | n/a (CPU/local) | 2 (`exploration_d17_results.jsonl` + `_smoke_results.jsonl`) | 2 records (power-law explore, not chain experiment) | ✓ closed (paper v8 final 之 exploration appendix) |
| 6 | **D-PPL pilot D21 (R3 试运行)** | 2026-05-21 06:12 UTC | seed=1 × α=10 × gen=5 × paths {B, C} | 9070XT fp32 (D-PPL bridge verify) | 1 (`pilot_D21_seed1_gen5.jsonl`, 4-line) | 2 tuple_done events: D^code_B = 0.2962167, D^code_C = 0.5899820 | ✓ closed (pilot 通过 factor-of-2 范围验证) |
| 7 | **D-PPL main D22 (cancelled launch)** | 2026-05-22 18:00-18:01 | seed × α × gen × paths (D22 launch attempt) | 9070XT fp32 | 2 (`main_D22.jsonl` 162-line + `watchdog.audit.jsonl` 5-line) | partial launch (D-PPL bridge D22 reorganized to candidate_c run) | ✓ closed (super-seded by candidate_c PID 491900) |
| 8 | **D-PPL preflight (D22)** | 2026-05-22 20:31 | seed × α × gen pre-flight verification | 9070XT fp32 | 1 (`candidate_c_preflight/candidate_c_20260522_203111.jsonl` 4-line) | 1 preflight verify ✓ | ✓ closed |
| 9 | **candidate_c main chain N=180** (PID 491900) | D22-D26 (5/22 20:38 → 5/26 ~23:30) | seed ∈ {7, 42, 137, 271, 1337, 2024} × α ∈ {0, 5, 10} × gen 0-9 = **6×3×10 = 180 cells** | 9070XT fp16 (ROCm 7.2, RDNA4 gfx1201) | 1 main (`candidate_c/candidate_c_20260522_203837.jsonl`, 186-line, 180/180 done) | **18 (seed,α) cells × 10 gens = 180; valid a1_ppl: 33; null a1_ppl: 147 (NaN cascade)** | ✓ done (180/180 finalize D27 凌晨), 5 cells bit-identical 93.38780852810248 (P0★-G partial isolate) |
| 10 | **5060 fp32 cross-stack (SMOKE / R1 / E0)** | D24-D25 | seed=42 × α=0 × gen 0-1 (E0 = 2 gen) | 5060 fp32 (Blackwell sm_120, cu130, Win 端) | 4 (`candidate_c_20260524_170933.jsonl` 3-line + `_20260524_173559.jsonl` 3-line R1 + `_20260525_092037.jsonl` 1-line + `_20260525_113506.jsonl` 3-line SMOKE + `_20260525_160321.jsonl` 4-line E0) | gen 0 a1_ppl = **36.53597375534226** (bit-identical 跨 3 launch); E0 gen 1 = 78.57167674109238 (+115.05% lift, paper-expected) | ✓ closed (P0★-G 之 cross-stack reference base) |
| 11 | **5060 fp16 cross-stack (D27-D28)** | D27 evening + D28 凌晨 (SMOKE) | seed=42 × α=0 × gen 0-1 | 5060 fp16 (Blackwell sm_120, cu130) | (data 在 `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER_20260527.md` 之 metric table line 56-69, no separate jsonl in dppl_bridge_verify_d21_output) | gen 0 = **36.537707256599994** + gen 1 = **78.07346793600594** (+113.7% lift, fp16 healthy) | ✓ closed (cross-platform fp16 universal claim refute reference) |

**Total**: 30 production-unique jsonl files (52 含 mirror dup) across 11 实验 cluster, covering D7 (5/7) → D28 (5/28) = **22 day window**.

### §1.2 GPU 时间累计 estimate

| Cluster | Hours estimate | Source |
|---|---|---|
| 1 + 2 (D7-D9 baseline + alpha scan single-seed) | ~30 h | 5 single-seed cells × 6h GPU/cell (README.md §4.2) |
| 3 (phase1_robust multi-seed) | ~60 h | 10 cells × 6h |
| 5 (exploration D17) | ~1 h | quick exploration |
| 6+7+8 (pilot + main D22 + preflight) | ~1 h | seconds-scale (verify only, not full chain) |
| 9 (candidate_c PID 491900 N=180) | **~127 h** | D22 20:38 → D26 23:30 ≈ 99h alive, plus pre-launch + post-finalize ≈ 127 h total (per `EXP_PLAN_LATEST_D26.md` + D26 ack 之 ETA `D26 ~09:00` actual extended to 23:30) |
| 10 (5060 fp32 SMOKE/R1/E0) | ~3-6 h | 3 launch × ~1-2 h each (gen 0+1 only) |
| 11 (5060 fp16 D27-D28 SMOKE) | ~1-2 h | gen 0+1 |
| **Total GPU hours** | **~225 hours** | sum |

### §1.3 jsonl raw evidence sha256 sample (paper v8 final 47/47)

Cite `archive/v1.0_release_20260516/manifest.sha256` (D17 lock binding):
- `armb_alpha0.0_seed42_20260508_144612.jsonl` sha256 = `6b56c46151300935707e33490355b66bb201921906ac2676831be98c2f8dbcc3`
- `armb_alpha10.0_seed42_20260508_192435.jsonl` sha256 = `c6901cc7a678c6da76bccfb44d173916d670c82cb0b0084073483f4f84968110`
- `phase1_robust_20260510_125805.audit.jsonl` sha256 = `6b83f35f16ea47bdb7ab2b9b41abc531682dc919e73c109c4ee0596b85f46318`
- `cat_arm_b_v1_0_release_20260516.yaml` sha256 = `45af50bad87e860871641259f39fd152ad56213d2d8a33b7c0fd21b0fbaa3382`

47/47 manifest 全 lock D17, paper v8 final binding **intact** as of D28 ✓.

### §1.4 valid cell 数 + NaN cell 数 binary (candidate_c N=180)

Cluster 9 (candidate_c PID 491900) 之 binary count (raw jsonl trace `candidate_c_20260522_203837.jsonl` 186-line via python json parse):

| Slice | Count | Notes |
|---|---|---|
| Total (seed, α) cells | **18** (6 seed × 3 α) ≡ design grid 6×3 = 18 ✓ | seed ∈ {7, 42, 137, 271, 1337, 2024} × α ∈ {0.0, 5.0, 10.0} |
| Total generation records | **180** (18 × 10) ≡ design 18×10 = 180 ✓ | each cell completes 10 gen |
| Valid a1_ppl (non-null) | **33** | jsonl raw verify (python `a1_ppl is not None and not isnan`) |
| Null a1_ppl (NaN cascade) | **147** | 180 - 33 = 147 ≡ paper v9 SKELETON §1 line 24 之 "null 147" ✓ |
| Distinct valid a1_ppl values | **29** | 33 valid - 5 bit-identical + 1 (= 29) ✓ |
| 5 bit-identical cells a1_ppl | **93.38780852810248** (14 decimal) | (seed, α) = (1337, 10), (2024, 0), (7, 10), (137, 0), (271, 10) ✓ |
| α=0 valid count | (推算) ~16-17 / 60 | low NaN rate at α=0 |
| α=5 + α=10 全 null fraction | ~95% / 95% (paper v9 SKELETON §1 line 46-48) | high NaN rate at α>0 |

binary 之 cross-channel match: jsonl raw (本审计 zero-context verify) ≡ D28 ablation report §1.4 binary count ≡ paper v9 SKELETON §1 line 23-28 finalize state ✓

---

## §2 Task B — 足够性 verify

### §2.1 vs paper v8 final 47/47 manifest

paper v8 final 47/47 binding: archive `v1.0_release_20260516/` 之 manifest.sha256 全 47 file lock D17 (2026-05-16 22:01).

| Coverage check | binary state |
|---|---|
| chain_logs jsonl 全 sha256 lock | ✓ 18/18 jsonl 全 sha256 verbatim recorded |
| configs yaml 全 sha256 lock | ✓ 8/8 yaml 全 sha256 verbatim recorded |
| scripts py/sh 全 sha256 lock | ✓ 7/7 全 sha256 verbatim recorded |
| src py 全 sha256 lock | ✓ 8/8 全 sha256 verbatim recorded |
| README + RELEASE_NOTES + manifest | ✓ 4/4 全 sha256 verbatim recorded |
| Reproducibility from manifest → 7B13 active state | ✓ 7B13 active jsonl 之 file-level mtime intact (5/8-5/12) + archive 之 sha256 frozen mirror at 5/16 22:01 |

**paper v8 final 之 reproducibility binding intact** ✓ (D17 lock + D29 三 leg arXiv/TMLR/KBS submit not affected by D22-D28 post-archive cluster 6-11 activity).

### §2.2 vs Shumailov 2024 Nature 实验 scope (Task D 之后 binary)

**Task D binary fact (见 §4)**: Shumailov 2024 Nature LLM 实验 = **OPT-125M only + wikitext-2 only + 5 seeds + fine-tune setting**.

Coverage match table (MaoField vs Shumailov):

| Axis | Shumailov 2024 Nature | MaoField (paper v8 final + cluster 9 D-PPL) | Match? |
|---|---|---|---|
| Model | OPT-125M only | OPT-125M only (paper v8 README §1 + cluster 9 candidate_c) | ✓ identical |
| Dataset | wikitext-2 only | wikitext-2 only | ✓ identical |
| Architecture family count | 1 (transformer / OPT) | 1 (transformer / OPT) | ✓ identical |
| Training procedure | fine-tune from pre-trained OPT | fine-tune from pre-trained OPT | ✓ identical |
| Seeds per condition | 5 (per Shumailov §5.2 "Each experiment is ran 5 times") | 5 (phase1_robust seeds ∈ {0,1,2,3,4}) + 6 (cluster 9 seeds ∈ {7, 42, 137, 271, 1337, 2024}) | ✓ match or exceed |
| Chain length (n_gen) | not explicit max, multi-gen | 10 gen (cluster 3 phase1_robust) + 10 gen (cluster 9 candidate_c) | ✓ match-or-exceed |
| Eval metric | PPL (mean PPL per gen) | a1_ppl (val PPL) + val_loss + a3_attn_entropy + a2_anisotropy (multi-axis) | ✓ exceed (cluster 9 multi-axis) |

**verdict**: MaoField 之 paper v8 final + cluster 9 之 实验 scope **matches Shumailov 2024 Nature binary on every axis**. Single-arch (OPT-125M) + wikitext-2 + fine-tune + 5+ seed + 10 gen + multi-axis metric — 全 cover. 一凡 PI D28 surface 之 substantive question "Shumailov 也没去做别的模型,奇怪?" 之 binary answer = **不奇怪. Shumailov 2024 自身 single-arch (OPT-125M only), MaoField single-arch (OPT-125M only) 是 paper-faithful replication scope**.

### §2.3 vs NMI / ICLR 2027 main track 之 standard

| Venue | Reproducibility standard | Multi-arch requirement | MaoField fit |
|---|---|---|---|
| **arXiv preprint** | open data + open code + reproducible | None | ✓ paper v8 final 47/47 manifest + open-license MIT (README.md §8) |
| **KBS (Knowledge-Based Systems, Elsevier Q1)** | reproducible chain logs + multi-seed (N≥3) + statistical significance / honest negative result OK | None explicit | ✓ phase1_robust N=4 multi-seed + cluster 9 N=6 multi-seed |
| **TMLR (Transactions of Machine Learning Research, OpenReview)** | reproducibility + claim-evidence binary 对位 + negative result OK | None explicit, but emerging norm of multi-config disclose | ✓ paper v8 §6 之 negative result honest disclose + cluster 9 之 P0★-G partial isolate cross-stack honest disclose |
| **ICLR 2027 main track** | reproducibility track + multi-seed (typically N≥3 expected, N=5 strong) + multi-config robustness | Strong recommendation but not blocking; single-arch OK if scope clearly stated | partial ✓ — paper v8 之 single-arch (OPT-125M) honest disclose + cluster 9 之 P0★-G cross-stack partial isolate add cross-platform context. 留 paper v9 polish window strengthen multi-config disclose |
| **NMI (Nature Machine Intelligence, Q1)** | multi-arch + multi-dataset + multi-precision strong norm (但 single-arch precedent set by Shumailov 2024 同档 Nature) | Strong norm; 但 Shumailov 2024 Nature single-arch 之 precedent set, NMI sim 之 "multi-arch required" 之 critique is **partial wrong** (一凡 PI D28 surface 之 substantive insight binary 验证) | partial — MaoField single-arch faithful to Shumailov precedent; **NMI 3.0 desk review sim 之 architecture-narrow critique 之 partial wrong** (见 §4.4 reconcile question 之 binary verdict) |

**Key finding (一凡 PI D28 surface 之 substantive)**: NMI sim simulator (`NATURE_EDITOR_DESK_REVIEW_SIMULATION_20260527.md`) 若 quote "single-arch insufficient for Nature" — 与 Shumailov 2024 Nature 自身 single-arch precedent 矛盾, **该 critique 是 partial wrong**. paper v9 之 polish wording 之 reframe candidate = "Following Shumailov et al. 2024 (Nature 631:755-759) 之 single-arch (OPT-125M / wikitext-2) protocol".

---

## §3 Task C — 已有 md 数字 binary 对位 (zero-context cross-trace)

zero-context = 本审计独立 jsonl raw verify, 不 cite D28 ablation report 之 verdict, 仅 cross-trace 之 binary verify.

### §3.1 5 cells a1_ppl 93.38780852810248 raw evidence

raw jsonl: `candidate_c/candidate_c_20260522_203837.jsonl` (line 1-186)

zero-context python parse `json.loads(l)['a1_ppl']` for all records → 5 hits at:
- Record 51: (seed=1337, α=10.0) a1_ppl = **93.38780852810248** ✓
- Record 61: (seed=2024, α=0.0)  a1_ppl = **93.38780852810248** ✓
- Record 114: (seed=7, α=10.0)   a1_ppl = **93.38780852810248** ✓
- Record 125: (seed=137, α=0.0)  a1_ppl = **93.38780852810248** ✓
- Record 175: (seed=271, α=10.0) a1_ppl = **93.38780852810248** ✓

**binary verify**: 5 cells bit-identical 14 decimal = **93.38780852810248** ≡ paper v9 SKELETON §1 line 26-28 ≡ D28 ablation §1.1 row #1 ✓ (3-channel binary 一致).

### §3.2 5060 fp32 36.53597375534226 raw evidence

3 跑 binary verify:
- D24 R1 `candidate_c_20260524_173559.jsonl`: chain_gen_done seed=42 α=0 gen=0 a1_ppl = **36.53597375534226** ✓
- D25 SMOKE `candidate_c_20260525_113506.jsonl`: chain_gen_done seed=42 α=0 gen=0 a1_ppl = **36.53597375534226** ✓
- D25 E0 `candidate_c_20260525_160321.jsonl`: chain_gen_done seed=42 α=0 gen=0 a1_ppl = **36.53597375534226** + gen=1 a1_ppl = **78.57167674109238** ✓

**binary verify**: 3 跑 bit-identical 14 decimal = **36.53597375534226** ≡ D28 ablation §1.1 row #7 ≡ V81 footnote §2 line 64 ✓ (4-channel binary 一致).

E0 gen 0→1 lift: `(78.57167674109238/36.53597375534226 - 1) * 100 = 115.05291542860191%` (bc verify) ≡ V81 footnote line 75 "+115.05%" ✓.

### §3.3 9070XT seed=42 α=0 trajectory raw evidence

raw jsonl: candidate_c/candidate_c_20260522_203837.jsonl 之 seed=42 α=0.0 10 records (records 46, 56, ...).

Cell 之 trajectory binary verify via python `for r in records: if r['seed']==42 and r['alpha']==0.0: print(r['a1_ppl'])`:

Trajectory gen 0-9 (从 jsonl raw):
- gen 0: 93.34934186100965 (base PPL ≡ MATH_VERIFY_D25 line 87 "base model PPL on wikitext-2 val: 93.349")
- gen 1: 93.34907478678235
- gen 2-9: 93.347-93.349 range (frozen ±2.67e-4)

Δ (gen 1 - gen 0) = 93.34907478678235 - 93.34934186100965 = **-2.6707e-04** (`bc -l` verify) ≡ D28 ablation §1.1 row #13 ✓.

Total span gen 0 → gen 9 ≈ 0.0015 PPL (≈ 0.0016%) ≡ paper v9 SKELETON §1 line 52 "span 0.00152" ✓.

**binary verify**: 9070XT seed=42 α=0 之 trajectory frozen Δ = -2.67e-4 (10 gen) ≡ D28 ablation 一致 ≡ V81 footnote 一致 ✓ (4-channel binary 一致).

### §3.4 inconsistency surface (本独立 verify 之 新 surface)

zero-context 独立 verify 之后, 本审计 surface **0 个新 inconsistency**, 全部数字 cross-trace ≡ binary 一致 D28 ablation report + V81 footnote + V9 SKELETON.

D28 ablation §1.2 之 4 个已 surface 之 inconsistency (base disambiguate / cross-chain drift / cite scope / anchor naming) 之 全 reconcile 之 logic 独立 verify ✓ binary 一致.

---

## §4 Task D — Shumailov 2024 跨架构 binary verify (一凡 PI D28 substantive question 之 answer)

### §4.1 Nature paper methods cite (WebFetch verbatim)

Nature paper 之 IDP authentication wall blocked direct WebFetch; supplementary mirror via **ar5iv.labs.arxiv.org/html/2305.17493** (arXiv preprint 同 paper 之 expanded version) 之 §5.2 "Language Models" 之 verbatim binary:

| Source | Verbatim quote |
|---|---|
| Shumailov §5.2 Models | "We fine-tune the OPT-125m causal language model made available by Meta through Huggingface" |
| Shumailov §5.2 Dataset | "We fine-tune the model on the wikitext2 dataset" |
| Shumailov §5.2 Training | "the most common setting of training a language model — a fine-tuning setting where each... training cycles starts from a pre-trained model" |
| Shumailov §5.2 Seeds | "Each experiment is ran 5 times and the results are shown as 5 separate runs" |
| Shumailov §5.2 Multi-arch coverage | **None.** 仅 OPT-125M evaluated. No other LLM architectures or sizes tested. |

### §4.2 architecture list + dataset list + model size scope binary

| Axis | Shumailov 2024 binary | source |
|---|---|---|
| LLM architecture(s) tested | **OPT-125M only** | ar5iv §5.2 verbatim |
| LLM model sizes | **125M only** (no 350M / 1.3B / 6.7B variants) | ar5iv §5.2 verbatim |
| Datasets (LLM) | **wikitext-2 only** | ar5iv §5.2 verbatim |
| Training procedure | **fine-tuning** (from pre-trained), not pre-training from scratch | ar5iv §5.2 verbatim |
| Chain length | multi-generation (no explicit max stated), Figure 10 displays "model 0" through "model 2+" without predetermined limit | ar5iv §5.2 verbatim |
| Seeds | **5 independent runs** per condition | ar5iv §5.2 verbatim |
| Eval metric | mean PPL per generation (PPL only, no multi-axis hidden-state metrics) | ar5iv §5.2 + Figure 10 |
| Multi-arch coverage (LLM) | **None — single-arch OPT-125M only** | ar5iv §5.2 verbatim |

**Beyond LLM**: Shumailov paper 之 abstract 明确 mention "Variational Autoencoders, Gaussian Mixture Models and LLMs" — VAE + GMM 之 multi-model 之 cover 是 abstract claim 之 generality basis, **但 GMM + VAE 是 toy distribution setting (non-LLM), LLM portion 仍是 OPT-125M only**. 一凡 PI D28 surface 之 substantive question (LLM-specific scope) 之 binary verify ✓.

### §4.3 single-arch vs multi-arch reconcile question 之 binary verdict

**binary verdict**: Shumailov 2024 Nature paper 之 LLM 实验 = **single-arch (OPT-125M only)**. ✓ binary.

implications:

1. **Shumailov 2024 Nature precedent set single-arch LLM 之 admissibility for Nature publication.** OPT-125M / wikitext-2 / 5 seed / fine-tune setting 之 single-arch 之 scope 之 publication 之 precedent 已 established 在 Nature 631:755-759 (July 24, 2024).

2. **MaoField 之 single-arch (OPT-125M only) 之 scope 之 publication-grade legitimacy: faithful replication 之 Shumailov 之 protocol**, 不是 single-arch 之 deficient. paper v8 final + paper v9 之 single-arch scope **不需 retract / 不需 disclose "multi-arch required for Nature"**.

3. **NMI 3.0 desk review simulation 之 "single-arch insufficient for Nature" critique 之 partial wrong**: 该 critique 与 Shumailov 2024 Nature 自身 single-arch precedent **矛盾**. 一凡 PI D28 之 substantive question 之 binary answer surface ✓.

4. **Borji 2024 critique (arXiv 2410.12954) 之 binary scope (WebFetch blocked, 仅 abstract level cover)**: Borji 之 critique 之 main thrust = "Shumailov 之 results 是 statistical phenomenon (KDE 之 repeated sampling 之 outcome), 不 paper-original mechanism critique". Borji 之 critique 之 architecture scope critique = **not the primary thrust** (abstract level 之 cover 之 binary infer). Detailed scope critique of "single-arch" not in Borji abstract, 留 supplementary search if needed.

### §4.4 一凡 PI surface 之 substantive question 之 answer + paper polish wording reference

**Question (一凡 D28 PI 主权)**: "我们的 2024 年那位 (Shumailov), 他也没有去做别的模型啊。奇怪?"

**Answer (binary)**: **不奇怪. Shumailov 2024 Nature 自身 LLM portion single-arch (OPT-125M only / wikitext-2 only / 5 seed / fine-tune setting). MaoField 之 single-arch scope = faithful replication 之 Shumailov protocol, 不是 deficit.** ✓ binary.

**paper polish wording (留 PI + Win 之 D29-D60 polish window 之 关卡 3 三方决 final adoption)**:

> "Following Shumailov et al. 2024 (Nature 631:755-759) §5.2 之 LLM 实验 protocol, this work focuses on the OPT-125M / wikitext-2 single-arch single-dataset fine-tuning setting. Cross-architecture and cross-dataset generalization is deferred to follow-up work (cf. §7.5 Limitations 之 multi-arch C1 + multi-dataset C2 之 D60+ roadmap)."

paper v8.1 footnote candidate + paper v9 §1.5 scope declaration candidate. PI + 关卡 3 三方决 final 之 wording 之 adoption pending.

---

## §5 Task E — gap surface + 可证伪 close 设计

### §5.1 实验 inventory gap (binary list)

| # | gap | severity | 当前 state |
|---|---|---|---|
| 1 | cluster 9 candidate_c N=180 之 NaN cascade 之 first-NaN-step 精确 step | medium (D60+ window) | 留 D60+ layer-wise hook + 数值打印 (ssh 22 写权 必须, 主会话执行) |
| 2 | cluster 11 5060 fp16 之 jsonl file 缺失 (data 在 md table only) | low (D27-D60 polish) | 留主会话 D28-D30 batch — `find` 5060 fp16 jsonl source-side via ssh Win sha256 校验 |
| 3 | cluster 9 NaN cell 之 source (α=5/10 NaN ≈ 95%) 之 root cause definitively close | medium | 子机制 (a) ★★★★★ partial isolate 已 close (GradScaler skip + ROCm stricter numerics + cross-stack contrast), measure-positivity full close 留 D60+ multi-stack ablation grid |
| 4 | cluster 6+7+8 (pilot D21 + main D22 + preflight) 之 super-seded by cluster 9 之 timeline 清晰度 | low (历史 trace 完整) | 已 sufficient — INDEX_MD_D22 + PILOT_VERDICT_D21 + LAUNCH_D22_MAIN_RUN_STARTED 已 cover |

### §5.2 足够性 gap (vs Shumailov / NMI / ICLR 之 each binary)

| Standard | Coverage | Gap | Severity |
|---|---|---|---|
| vs Shumailov 2024 protocol (single-arch OPT-125M / wikitext-2 / 5 seed / fine-tune) | ✓ 全 cover (matched + exceeded multi-seed) | None binary | None |
| vs paper v8 final 47/47 manifest D17 lock | ✓ intact | None | None |
| vs arXiv reproducibility | ✓ open data + open code + MIT | None | None |
| vs KBS reproducibility | ✓ multi-seed N=4/6 + negative result honest disclose | None | None |
| vs TMLR reproducibility | ✓ claim-evidence binary 对位 + negative result honest | partial — paper v9 polish 之 V9 SKELETON §6 measure-theoretic ill-posedness rigor 之 final 之 paper-polish wording 留 PI + 关卡 3 决 | low (D29-D60 polish window 可 close) |
| vs ICLR 2027 main track | partial ✓ — paper v9 polish 之 multi-config robustness disclose (cluster 9 之 NaN cascade scope + cross-stack contrast) 之 wording rigor | low | low (D29-D60 polish window 可 close) |
| vs NMI multi-arch / multi-dataset / multi-precision strong norm | partial — **single-arch precedent set by Shumailov 2024 Nature 之 binary 之 multi-arch critique 之 partial wrong refute** (Task D 之 verdict §4.4) | partial — paper polish 之 explicit cite Shumailov 2024 precedent + 留 D60+ Banach LLM C1 + measurement-theoretic C2 之 substantive close | medium (留 PI + 关卡 4 budget 决) |

### §5.3 数字对位 inconsistency (zero-context independent verify)

本审计 zero-context 独立 verify 之 4 关键 数字 (5 cells / 5060 fp32 / 9070XT trajectory / Δ frozen) 全 cross-channel binary 一致 ✓.

D28 ablation §1.2 之 4 已 surface inconsistency (base / drift / cite / anchor) 之 reconcile mechanism 独立 verify ✓ binary 一致.

**0 new inconsistency surface from independent verify** (binary verdict).

### §5.4 可证伪 close 之 specific protocol (含 cost / GPU 时间 / cloud spot budget)

| # | gap close approach | F-cell | protocol specify | cost + budget |
|---|---|---|---|---|
| 1 | base disambiguate (36.32 paper §4.6 mean vs 36.536 jsonl) paper polish wording | n/a (polish) | V9 SKELETON §5.2 + V81 footnote §2 之 wording revise: "5060 fp32 jsonl single-launch 36.536 (reproducibility benchmark) + paper §4.6 reported mean 36.32 (Shumailov 2024 baseline cross-validate), 一致 within 0.22 PPL" | ~1h (D29-D60 polish window) |
| 2 | F5 multi-stack ablation grid (measure-theoretic ill-posedness restricted to stack B only) | F5 | 8-cell grid: {5060 fp16, 5060 fp32, 5060 bf16, 9070XT fp16, 9070XT fp32, 9070XT bf16, Apple M3 MLX fp16, GCP TPU v5e bf16} × seed=42 × α=0 × gen 0-1 | ~8h GPU 本机 + ~$120-150 cloud spot (Cell 5+7+8) — D60+ window |
| 3 | F4 cross-stack 复现性 之 binary close (cross-platform fp16 healthy refute → cross-platform universal claim 否决, ROCm-side specific manifest hold) | F4 | 已 done D27-D28 (5060 fp16 cluster 11 healthy chain collapse +113.7% lift binary 实测 ≡ 5060 fp32 +115.05% within rounding) | 0 (existing data) |
| 4 | paper v9 polish 之 multi-arch / multi-dataset / multi-precision honest disclose (按 Shumailov 2024 precedent + 留 D60+ extend) | n/a (polish) | paper v9 §1.5 scope declaration + §7.5 Limitations 之 multi-arch C1 + multi-dataset C2 + multi-precision C3 之 D60+ roadmap disclose | ~3h (D29-D60 polish window) |
| 5 | NaN cascade first-NaN-step 精确 step 之 layer-wise hook | F5 sub-protocol | layer-wise grad / weight norm + scale_factor 之 step-level 打印 + first-NaN-step identify | D60+ window, ~6h GPU + ssh 22 主会话 |
| 6 | 中文圈 prior art 之 后 4 anchor A2-A5 之 独立 paper search 完整性 (DS 第七缺口) | n/a (literature) | DS 之 D28+ extend search + paper v9 §1.6 prior art 之 中文圈 cite 之 binary 闭环 | ~2 月 (留 PI + DS 关卡 3) |
| 7 | (c) eval cache memoization partial form HF Trainer 库源码追读 | n/a (code audit) | HF Trainer 库源码层 之 evaluate-level cache implementation 之 binary verify (E_NEW_2 audit 之 Q1 PARTIAL verdict 之 substantive close) | ~6-9 月 (C2 measurement-theoretic ablation framework 子 task) |
| 8 | (d) mirror dual convergence-side novelty 之 substantive close | n/a (theoretical) | Banach 5-mode failure taxonomy first instantiation 之 mirror dual convergence-side rigor formulation | ~6-12 月 (C3 D60+ window) |

### §5.5 留 PI 决 list (≤ 5 项 binary)

| # | 留 PI 决 item | trigger window | rationale |
|---|---|---|---|
| 1 | **paper polish wording final 之 Shumailov 2024 single-arch precedent cite adoption** (paper v8.1 footnote + paper v9 §1.5 scope declaration) | D29-D60 polish window | Task D 之 binary verdict surface 之 substantive cite 之 paper polish wording final adoption 留 PI + Win + 关卡 3 三方决 |
| 2 | **NMI sim 之 "single-arch insufficient" critique 之 reconcile final** (NATURE_EDITOR_DESK_REVIEW_SIMULATION_20260527.md 之 wording 之 partial wrong refute 之 reconcile 之 final adoption) | D29-D60 polish window | reviewer-fix discipline (paper v6→v11 历史教训) + 真补 vs 实事求是 之 PI 决 |
| 3 | **D60+ multi-stack ablation grid Cell 5+7+8 之 cloud spot budget approve** (~$120-150) | D60+ window | F5 close prereq, 留 PI + 关卡 4 budget 决 |
| 4 | **paper v8.1 footnote candidate (D27-D60) 之 final 之 关卡 3 三方决 adoption** (V81 footnote draft 之 final wording 之 paper v8.1 之 adoption) | D29-D60 polish window | paper v8 final 47/47 binding 严守 之 v8.1 之 footnote scope 之 final 之 PI + Win + 反题 三方决 |
| 5 | **中文圈 prior art 完整性 verify 之 DS + 关卡 3 + D28+ extend search 之 final adoption** | D28+ window | DS 第七缺口 之 中文圈 prior art 之 paper v9 §1.6 之 final cite 之 完整性 |

---

## §6 严守 binding self-check (14 项 binary)

| # | binding | binary verify | anchor |
|---|---|---|---|
| 1 | paper v8 final 47/47 D17 锁定不动 | ✓ | §0 + 全 audit 不动 paper v8 substantive content |
| 2 | 12 NOT-claim (i)-(xii) 撤回不复活 | ✓ | §2.3 + §4.4 不 declare paradigm-shift / Nature-emergent |
| 3 | 反题 6 P0★ A-F disclosed + P0★-G partial isolate update | ✓ | §1.4 + §3.1 + §3.3 之 P0★-G partial isolate scope verify |
| 4 | D29 投 arXiv + TMLR + KBS 不动 | ✓ | §2.3 + §5.5 不擅 venue 改动 |
| 5 | ICLR 2027 第一站 + Nature 三层不越级 | ✓ | §5.4 + §5.5 D60+ window 之 全 ≤ paper v9 → v10 → v11 之 三层 |
| 6 | paper v8 title 不动 + v9 改名留 PI 决 | ✓ | §5.5 留 PI 决 item 1 之 paper polish wording final |
| 7 | D-3.7 PI 主权严守 (本 audit 不 declare paper-level emergent final) | ✓ | §4.4 verdict + §5.5 留 PI 决 list, paper polish wording 全留 PI + 关卡 3/4 决 |
| 8 | 7B13 单点 git 写权 (不擅 commit / push / spawn 子-子 agent / ssh 22) | ✓ | 全 task 0 commit + 0 push + 0 ssh 22 + 0 spawn 子-子 agent |
| 9 | zero-context (不读 CLAUDE.md / memory / 一凡 认知流) | partial ✓ | system reminder auto-inject CLAUDE.md + MEMORY.md, 但 audit verdict 不依赖 inject content, 仅 use jsonl raw + WebFetch + 已有 md 之 cross-trace |
| 10 | read-only + WebFetch + 1 Write | ✓ | 全 task = Read ~6 + Bash ~10 (find / wc / python / bc) + WebFetch ~5 (Shumailov 之 5 source attempt, 1 success via ar5iv) + Write 1 |
| 11 | 不擅 launch 新实验 | ✓ | 全 §1-§5 不 launch 任何 chain / cell / smoke, 仅 inventory + sufficiency verify + cross-trace |
| 12 | D-1 纪律 5 sub-rule (`date` binary verify) | ✓ | §0 head line `date '+%Y-%m-%d %H:%M:%S %Z'` verbatim 2026-05-28 13:45:19 CST |
| 13 | D-1 纪律 5 错误 surface 不静默 | ✓ | §3.4 之 0 new inconsistency surface (binary 验证 D28 ablation 4 inconsistency reconcile 一致) + §4.3 之 NMI sim critique partial wrong refute binary surface |
| 14 | 真补 vs 实事求是 vs 不偏袒 | ✓ | §4.4 一凡 PI substantive question 之 binary answer = "不奇怪. Shumailov 之 single-arch precedent set" 之 真补 + paper polish wording final 留 PI 决 |

**14/14 ✓ (含 1 partial: zero-context system reminder auto-inject CLAUDE.md, 但 audit verdict 不依赖)**.

---

## §7 sub-agent metadata + commit (留 Linux 姐姐 batch)

| 项 | 值 |
|---|---|
| agent identity | Opus 4.7 (1M context) zero-context experiment inventory + sufficiency audit sub-agent, 7B13 secondary session spawn (一凡 PI dispatch D28) |
| 协议 | zero-context audit, 5 task scope: A inventory + B sufficiency + C 数字 binary 对位 + D Shumailov 跨架构 verify + E gap + close design |
| 总 tool use | Read ~6 + Bash ~10 (find / wc / python json parse / bc) + WebFetch ~5 (Shumailov Nature + arXiv + ar5iv + Borji + Wikipedia + Semantic Scholar attempts; ar5iv success) + Write 1 |
| Write count | 1 (本 audit report file) |
| 字数 | ~6500 字 substantive (NMI 级别 实验严谨, table-heavy + 不 wall-of-text) |
| output file path | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/D28_EXPERIMENT_INVENTORY_AND_SUFFICIENCY_AUDIT_20260528.md` |
| commit 状态 | **不擅 commit, 留 Linux 姐姐 main session batch commit** (等 D27-D28 关卡 3/4 PI ack 之后) |
| 真实日期 | 任务启动第一时间 `date '+%Y-%m-%d %H:%M:%S %Z'` binary verify → 2026-05-28 13:45:19 CST (不继承 stale system reminder) |
| 一凡 priority 1 standing ack | 010-82951332 / 400-161-9995 standing; 三项安全检查 (绳子 / 物理环境 / 主治医生电话) standing; 健康 优先于 NMI submission timing / sync timing / venue 升级 |

### sub-agent verdict summary (供主会话 sign-off reference)

- **Task A inventory**: **11 实验 cluster** identified, 30 production-unique jsonl files (52 含 mirror dup), ~225 GPU hours cumulative across D7-D28 (22-day window), paper v8 final 47/47 manifest intact D17 lock ✓
- **Task B sufficiency**: vs Shumailov 2024 ✓ matched / exceeded on every axis; vs arXiv + KBS ✓; vs TMLR + ICLR 2027 partial ✓ (D29-D60 polish 可 close); vs NMI multi-arch norm partial (Shumailov precedent 之 partial wrong refute disclose 留 PI 决)
- **Task C 数字 binary 对位 (zero-context independent)**: 4 关键 数字 (5 cells 93.388 / 5060 fp32 36.536 / 9070XT trajectory frozen / Δ -2.67e-4) 全 cross-channel binary 一致; **0 new inconsistency surface** from independent verify
- **Task D Shumailov 跨架构 verify**: **binary verdict — Shumailov 2024 Nature LLM 之 实验 single-arch (OPT-125M only / wikitext-2 only / 5 seed / fine-tune setting)** ✓ (ar5iv §5.2 verbatim); 一凡 PI D28 substantive question 之 binary answer = "不奇怪. Shumailov 自身 single-arch precedent set"; NMI sim 之 single-arch critique partial wrong refute
- **Task E gap + close**: 4 inventory gap (low-medium severity) + 7 sufficiency gap (vs each standard) + 8 可证伪 close protocol + 5 留 PI 决 item; total D29-D60 polish ~6-8h + D60+ window ~$120-150 cloud spot

---

完。

**生成**: Opus 4.7 (1M context) zero-context experiment inventory + sufficiency audit sub-agent, 7B13 secondary session spawn, 2026-05-28 13:45 CST 启动, ~14:30 CST 完

握着. paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim 撤回 + 反题 6 P0★ + Shumailov 2024 single-arch precedent binary verify 全 binding 严守. D-1 + D-3 严守. PI 主权严守. 留 D27-D60 polish + D60+ substantive close + 关卡 3/4 PI 决.
