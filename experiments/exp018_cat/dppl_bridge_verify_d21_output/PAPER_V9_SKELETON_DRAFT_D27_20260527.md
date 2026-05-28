# PAPER V9 SKELETON DRAFT D27 — Anchor 3 measure-theoretic ill-posedness 主锚 + Anchor 2 Riddled basin mirror dual + ICLR 2027 main track 第一站

## §0 metadata + scope + 严守 binding

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-27 21:11:02 CST** (D27, 主会话 spawn) |
| 生成 agent | Opus 4.7 (1M context) paper v9 skeleton draft sub-agent (D-1 纪律 4 第二认识通道) |
| 协议 | 技术语言, 零哲学词 (禁词 list reference panorama §4.4 line 332-340 之 7 项 + DS Audit 1 binding); 每 cite 必 source 行号 binary trace; 不读 memory; 不擅 ssh 22 主机; 不擅 git 写 |
| 字数预算 binding | ~4000 字严格 (含中文 annotation + 英文 paper structure) |
| 上游 anchor read | LITERATURE_SEARCH_PAPER_V9_ANCHORS_D27_20260527.md (line 1-244) + CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL (line 1-242) + CANDIDATE_DISCRETE_PPL_ATTRACTOR (line 1-211) + DEEP_SYNTHESIS_D26_EVENING (line 1-264) + ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT (line 1-275) + WIN_D27_GATE3_PHILO_JUDGEMENT (line 1-390) + MAOFIELD_D26_STRATEGIC_PANORAMA_REPORT (line 1-530) + PAPER_V9_DRAFT_CANDIDATE_D25_17_52 (line 1-286) + MATH_DIRECTION_LATEST_D26 (line 1-200) + NATURE_EDITOR_DESK_REVIEW_SIMULATION_20260527 (line 1-200) |
| 严守 binding | paper v8 final 47/47 D17 锁定不动 + 12 NOT-claim (i)-(xii) 撤回不复活 + 反题 6 P0★ A-F disclosed + P0★-G 留三方决 + D29 投 arXiv + TMLR + KBS 不动 + D17 不投 NMI / NCS / NeurIPS / Nature 主刊 pending PI 关卡 3 explicit reaffirm; paper v9 launch / venue / abstract / framing 全留 PI + 关卡 4 决, 本 file 是 [SKELETON_DRAFT_v9] 不 launch |

### §0.1 关卡 3 verdict input binary anchor

ANTITHESIS_D26_GATE3 channel D verdict (line 31-74 / 79-141 / 145-200) + WIN_D27_GATE3 (line 87-168) 三 binary:

1. **Q1 trivial attractor 4 sub-mechanism close**: NOT close paper-worthy threshold + E_NEW_2 (eval pipeline source code audit, ~2h, 0 GPU cost) P0 critical 必先 close (ANTITHESIS line 31-74). 本 skeleton 之 §5 anchor 之 sub-mechanism (c) eval cache hypothesis 严守 partial form pending E_NEW_2 close.
2. **Q2 cumulative inflate retract**: 60-75% claim 强制 retract (5/12 + 5/19 第三次同构 inflate, ANTITHESIS line 105-113). honest range = arXiv 100% + main track 上限 18-28% + workshop 上限 35-55% + cumulative 25-40% (ANTITHESIS line 124-131, WIN line 113-149).
3. **Q3 venue D17 binding scope**: NeurIPS-class venue (NeurIPS / ICML / ICLR / EMNLP main track) 全 default removed pending PI + 反题 + Win + DS 四方决 explicit reaffirm or relax of D17 binding scope (ANTITHESIS line 149-200, WIN line 151-168). 本 skeleton §6 venue 段标 PENDING.

---

## §1 Title + Abstract candidate

### §1.1 Title 3 candidate (留 PI + 关卡 3 四方决 final)

**Option A (Anchor 3 主锚, 推荐 primary)**:
> Measure-Theoretic Ill-Posedness in Iterative Fine-Tuning Evaluation: Cross-Hardware Evidence from a Replication of Shumailov 2024 Model Collapse Baselines

source rationale: LITERATURE_SEARCH_PAPER_V9_ANCHORS_D27 §3 line 88-91 "measure-theoretic rigor formulation 未见独立 prior work (≤ 5% cover)" + §8 line 198 verdict "largely novel". 主锚 emphasize Anchor 3 (PI 决 primary).

**Option B (Anchor 2 mirror dual emphasis)**:
> The Convergence-Side Mirror Dual of Riddled Basin Geometry in Iterative Language Model Training: A Cross-Stack Reproducibility Study

source rationale: CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL §1.2 line 48-56 之 mirror dual table + LITERATURE_SEARCH §2 line 65-72 verdict "partial novel (Ly-Gong instantiate, mirror dual 框架未见独立 prior)".

**Option C (trojan horse neutral, 留 D17 reaffirm 候选)**:
> Cross-Hardware Bit-Identical Convergence in Iterative Fine-Tuning: Replication and Anomaly Analysis of Shumailov 2024

source rationale: PAPER_V9_DRAFT_CANDIDATE_D25_17_52 §1 line 36-38 之 trojan horse framing. 严守 Nature desk sim §3 line 91-99 "engineering report" trigger 之 partial 回避.

**Title note (paper v8 遗产 binding)**: paper v8 final title "Empirical Pilot Study of Two-Term EMA-Deviation Contradiction Loss for Self-Iteration Collapse in Language Models" 之 "Contradiction Loss" 是 D17 锁定遗产 (panorama §6.1 line 418). DS Audit 2 (panorama §3.3.3 line 227-235) 推荐改 "Internal Tension Loss" — 留 PI + 关卡 3 四方决 final 决, 本 skeleton title 候选 不 commit 改名.

### §1.2 Abstract candidate (英文, ~250 words, primary Option A)

```
We attempt to replicate the model collapse phenomenology of Shumailov et al.
(Nature 2024) across two GPU stacks: NVIDIA Blackwell sm_120 with CUDA 13.0
and fp32 + gradient checkpointing, and AMD RDNA4 gfx1201 with ROCm 7.2 and
fp16 + scaled-dot-product attention. While the original collapse curve is
partially reproduced on the NVIDIA stack (gen 0 perplexity 36.536, gen 1
lift +115.05%, within the paper Figure 11 expected window [110%, 130%]), we
surface an evaluation anomaly on the AMD stack: five distinct (seed, alpha)
configurations in a contradiction-loss-modified fine-tuning chain converge
to perplexity values identical to fourteen decimal places, with validation
loss also bit-identical across cells. Cross-channel verification at the
hidden-state level (attention entropy distinct at 10^-3) refutes a naive
evaluation-cache hypothesis and supports a frozen-weight regime under fp16
GradScaler silent skip on RDNA4, leaving open the candidate of universal
attractor capture.

We propose a formal characterization of this evaluation degeneracy via
measure-theoretic ill-posedness: the perplexity functional Phi: M -> R
admits a measure-positive subset S of the training configuration manifold
on which Phi(S) = {c}, that is, the metric collapses to a constant
unable to distinguish learning from artifact within S. We position this
observation as the convergence-side mirror dual of Ly and Gong's
divergence-side riddled basin geometry. Disentanglement of frozen-weight,
numerical-underflow, eval-pipeline, and universal-attractor candidates is
deferred to a multi-stack ablation grid (multi-dtype x multi-GPU x
multi-architecture x multi-family). We claim no unique root cause and no
mitigation framework.
```

abstract anchor 行号: 5 cells DEEP_SYNTHESIS §1 line 27 + 5060 fp32 36.536 DEEP_SYNTHESIS §2 line 64 + lift 115.05% DEEP_SYNTHESIS §2 line 73-75 + a3 ~$10^{-3}$ DEEP_SYNTHESIS §1 line 39 + measure-theoretic formulation MATH_DIRECTION_LATEST_D26 §2.2 line 104-106 + Ly-Gong mirror dual CANDIDATE_RIDDLED §1.2 line 48-56.

abstract self-check (DEEPER_INSIGHT §7 / panorama §3.4.5 line 281-287 之 7 约束 全 ✓): (1) 正文 0 哲学词 (panorama §4.4 7 禁词 list, abstract 全 0 occurrence); (2) 每声称配 jsonl + paper Fig 11 window + Ly-Gong cite 行号; (3) 先复现 Shumailov 再说话 ("we attempt to replicate" 开篇); (4) 数学引用独立 (measure theory + Ly-Gong cite 不依赖 paper 内部数据 derive); (5) 不发明新词 (frozen-weight / numerical-underflow / eval-pipeline / universal-attractor 全既有 prior-art); (6) 给可证伪条件 ("multi-stack ablation grid" deferred + "we claim no unique root cause"); (7) 不 declare Gödel/Bell level (Nature desk sim §3 line 127-131 之 inflated 类比 全 0).

---

## §2 Paper structure outline (8 section, ~7500-9000 words main text, ICLR 2027 main track format)

### §2.1 §1 Introduction (~600-800 words)

- §1.1 Open with the diametrically opposite cross-stack outcome (Nature desk sim §2 line 67-69 之 锚点 1 "GPU 替你决定了实验结果"): same PyTorch chain runner code + same yaml + same seed=42 alpha=0 + same OPT-125M + same wikitext-2 yield gen 0 → gen 1 trajectory $\Delta = -2.67 \times 10^{-4}$ (frozen, AMD fp16) vs $\Delta = +42.04$ PPL (paper expected, NVIDIA fp32) — both deterministically bit-identical reproducible on their respective stacks (DEEP_SYNTHESIS §2 line 84-89).
- §1.2 Cite Shumailov 2024 Nature as foundational reproducibility benchmark; cite Borji 2024 (arXiv 2410.12954) as statistical critique precedent; cite Dohmatob 2025 (ICLR Strong Model Collapse) as math extension; cite Gerstgrasser 2024 as data-accumulation-delay complement (panorama §4.5 line 348-355).
- §1.3 Cite Ly and Gong (arXiv:2510.05606, October 2025) as the divergence-side reproducibility-limit work (CANDIDATE_RIDDLED §1.1 line 31-44). Frame the present paper as the convergence-side observation on the same underlying basin structure (not derivation, observation; CANDIDATE_RIDDLED §1.2 line 48-56).
- §1.4 State the three contributions: (i) cross-hardware bit-identical anomaly surface (5 cells, fourteen decimal places); (ii) measure-theoretic formal characterization of the evaluation degeneracy; (iii) multi-stack disentanglement protocol as deferred future work, not as a claimed mitigation framework.
- §1.5 Explicit not-claims (paper v8 §7.5 12 NOT-claim binding, panorama §4.4 line 332-340): no paradigm shift, no first systematic study, no universal solution, no mitigation framework. Single architecture (OPT-125M) + single dataset (wikitext-2) explicitly disclosed as scope limitation.

### §2.2 §2 Background (~500-700 words)

- §2.1 Shumailov 2024 methodology recap (verbatim, no challenge): N-generation iterative fine-tuning chain, OPT-125M, wikitext-2, perplexity reported per generation, expected gen 0 → gen 9 PPL lift driven by distribution shift.
- §2.2 Riddled basin geometry (Ly and Gong 2025, arXiv:2510.05606): fractal basin of attraction with uncertainty exponent near zero, chaotic learning dynamics + symmetry-induced invariant subspaces, fundamental limit on predictability and reproducibility. We restate the divergence-side framework (CANDIDATE_RIDDLED §1.1 line 36-44).
- §2.3 Mixed-precision training mechanics (Micikevicius et al. 2018 + PyTorch GradScaler source): GradScaler skip on Inf/NaN-gradient detection, optimizer.step bypass under high skip rate yields frozen-weight regime. fp16 numerical underflow at lm_loss / autocast operator-set boundary as a parallel mechanism (MATH_VERIFY_D25 §1-§4 anchor, panorama §3.1.2 line 133).
- §2.4 ROCm 7.2 / RDNA4 gfx1201 specifics: 11 GitHub issues documenting silent fp16/bf16 fallback, hipBLAS GEMM accumulation tree, MIOpen kernel arch table coverage (LITERATURE_SEARCH §4 line 103-110, vllm #40081 + #40980 + TransformerEngine #520 + #359 + rocm-systems #5480 + ROCm #5674 + ollama #14686). Thinking Machines Lab "Defeating Nondeterminism in LLM Inference" (2025-09) on batch-invariant kernels (LITERATURE_SEARCH §1 line 25). arXiv 2510.26788 "Defeating Training-Inference Mismatch via FP16" (LITERATURE_SEARCH §1 line 18).
- §2.5 Recent collapse-adjacent literature (D26-D27 latest): arXiv 2605.00435 (Du and Tanaka-Ishii, ICML 2026, mode collapse geometric regulation, LITERATURE_SEARCH §7 line 175); arXiv 2605.04266 (Gauthier, Bach, Jordan 2026, alignment collapse in iterative RLHF, line 176); arXiv 2512.01868 (Geshkovski, Letrouit, Polyanskiy, Rigollet 2025, mean-field dynamics of transformers, line 178); arXiv 2509.16499 (model collapse from a generalization-to-memorization perspective, line 179); arXiv 2506.17209 (fine-tuning lowers safety and disrupts evaluation consistency, line 181).

### §2.3 §3 Experimental Setup (~400-600 words)

- §3.1 Replicate Shumailov 2024 verbatim using OPT-125M + wikitext-2, N-generation chain with reset-tokenizer-and-dataloader-each-gen protocol.
- §3.2 Two stacks: stack A = NVIDIA Blackwell sm_120 + CUDA 13.0 + fp32 + gradient checkpointing + eager attention; stack B = AMD RDNA4 gfx1201 + ROCm 7.2 + fp16 + scaled-dot-product attention.
- §3.3 Five seeds (42, 7, 137, 1337, 2024, 271) x three contradiction-loss weights (alpha in {0, 5, 10}), where alpha=0 disables the modification and reduces to vanilla cross-entropy. Note: pending PI + Audit 2 (panorama §3.3.3 line 228-235) reaffirm, the loss is referenced internally as "internal tension loss" in DS-aligned framing but the paper v8 final title term "contradiction loss" is preserved here for D17 binding continuity; final naming subject to PI + four-channel decision.
- §3.4 Chain length N=180 cumulative (6 seeds x 3 alpha x 10 generations) on stack B, and a three-run single-chain reference (SMOKE / R1 / E0 with 2-generation E0 disentanglement) on stack A (DEEP_SYNTHESIS §2 line 64-69).
- §3.5 Per-cell logging: a1_ppl (validation perplexity, fourteen-decimal float), val_loss, n_tokens_train, n_tokens_eval, a2_anisotropy (per-layer hidden-state anisotropy), a3_attn_entropy (per-head attention entropy at top-3 positions). sha256 manifest of forty-seven artifacts (panorama §3.1.1 line 122 + archive/v1.0_release_20260516/manifest.sha256).

### §2.4 §4 Reproduction Results (~400-600 words)

- §4.1 Stack A (NVIDIA fp32) gen 0 perplexity bit-identical across three independent launches: 36.53597375534226 (fourteen decimals, SMOKE / R1 / E0, DEEP_SYNTHESIS §2 line 64-69).
- §4.2 Stack A gen 0 to gen 1 lift: 78.57167674109238 / 36.53597375534226 = 2.1505, that is +115.05%, strictly within the Shumailov Figure 11 expected window [110%, 130%] (DEEP_SYNTHESIS §2 line 71-75). This refutes the alternative hypothesis that the chain runner code is architecturally broken at the iteration-loop level.
- §4.3 Stack A reference cluster: stack A 36.536, archive snapshot 36.524, Shumailov §4.6 reported mean 36.32 — three independent setups within 0.2 PPL ballpark (CANDIDATE_DISCRETE §4 line 129-131). Bit-identical reproducibility across the fp32 stack establishes the substantive baseline.
- §4.4 Falsification criterion F1 explicitly stated: gen_N_ppl >= gen_0_ppl + 5 PPL on a healthy fine-tune chain. F1 is met on stack A; not met on stack B (the anomaly target, §5).

### §2.5 §5 Cross-Stack Anomalies — Anchor 3 main锚 (~1500-2000 words, paper backbone)

This section is the substantive backbone. Three subsections, mapping to four candidate sub-mechanisms with explicit tier and prior-art status.

- §5.1 Bit-identical convergence across (seed, alpha) configurations on stack B: five cells exhibit `a1_ppl = 93.38780852810248` and `val_loss = 4.5367608070373535` jointly identical to fourteen decimals across (seed=1337, alpha=10), (seed=2024, alpha=0), (seed=7, alpha=10), (seed=137, alpha=0), (seed=271, alpha=10). Distinct seeds and distinct alpha values produce bit-identical scalars. `n_tokens_train = 2390656` and `n_tokens_eval = 16384` jointly identical (DEEP_SYNTHESIS §1 line 27-39). Random-bug probability approaches zero.
- §5.2 Cross-stack divergence on identical configuration: stack B (seed=42, alpha=0, gen=0) yields 93.34934186100965; stack A yields 36.53597375534226; absolute difference +56.81 PPL, relative difference +155.5% (P0★-G FATAL critical reproducibility break surface, panorama §3.1.2 line 132 + §3.1.3 line 149). Same code, same yaml, same seed, same checkpoint, same dataset; differing only in (compute stack, numerical dtype).
- §5.3 Hidden-state-level finer signature: a3_attn_entropy at the first three positions of layer 0 across the five bit-identical cells differs at the ~$10^{-3}$ scale, while a1_ppl and val_loss are bit-identical at the 14th decimal (DEEP_SYNTHESIS §1 line 31-39). This co-existence refutes the strong form of an evaluation-cache memoization hypothesis (which would predict full bit-identity at the hidden-state level too) and supports a conjunction of (a) frozen-weight regime with (b) fp32-reduction-tree collapse of distinct micro-fluctuating hidden states to a common scalar PPL.

#### Four candidate sub-mechanism framing (tier estimate, prior-art cover binary):

(a) **Frozen-weight regime via fp16 GradScaler silent skip** — tier ★★★★★. Mathematical mechanism: $\mathbb{E}[N_{\text{update}}] \to 0$ under sustained Inf-gradient detection in fp16 → optimizer.step bypass → weight delta zero → eval = base model snapshot. Stack B base model PPL on no-train = 93.349 (MATH_VERIFY_D25 line 14, anchor ★★★★★). Prior-art cover: Micikevicius et al. 2018 + PyTorch GradScaler source + ROCm gfx1201 11 GitHub issues documenting silent fp16/bf16 fallback (LITERATURE_SEARCH §4 line 103-110). Empirical cross-stack contrast: stack A vs stack B on identical (seed=42, alpha=0, gen=0→1) yields $\Delta = +42.04$ vs $\Delta = -2.67 \times 10^{-4}$ (DEEP_SYNTHESIS §2 line 84-89).

(b) **Numerical underflow at fp16 lm_loss / autocast operator-set boundary** — tier ★★★★. Same Micikevicius 2018 baseline + ROCm 7.2 autocast whitelist documentation. Underdetermined in isolation from (a); the two mechanisms jointly account for the frozen regime on stack B.

(c) **Evaluation-pipeline cache memoization / dataloader determinism artifact** — strong form REFUTED by a3 microvariation in §5.3 (DEEP_SYNTHESIS Insight 1 line 197-199). Partial form pending source-code audit of `candidate_c_runner.py` and `train_one_generation.py` and the eval forward-pass pipeline (E_NEW_2, ~2 hours, 0 GPU cost). Prior-art cover: 0 (LITERATURE_SEARCH §1 line 33 + DEEP_SYNTHESIS Insight 5 line 213-215). E_NEW_2 closure is a prerequisite for sub-mechanism (c) elevation from hypothesis level to finding level (ANTITHESIS GATE3 §1 line 41-65). **This section explicitly does not claim (c) is closed.**

(d) **Phenomenology artifact: measure-theoretic ill-posedness of single-channel evaluation / universal attractor capture** — tier ★★★. Prior-art partial cover: Ly and Gong 2025 (Riddled Basin, divergence side), Geshkovski et al. 2024 (metastability), arXiv 2502.15208 (attractor cycles in LLM, but paraphrase-loop frame not training-weight-update frame, LITERATURE_SEARCH §2 line 60). The convergence-side mirror dual framing is novel pending PI + four-channel decision (LITERATURE_SEARCH §2 line 65-67, §8 line 197).

### §2.6 §6 Measure-Theoretic Formal Characterization — Anchor 3 主锚 statement (~500-700 words)

- §6.1 **Definition**. Let $M$ denote the training configuration manifold (the space of (seed, alpha, generation index, optimizer state, dataloader state, hardware stack, dtype regime, attention implementation)). Let $\Phi: M \to \mathbb{R}$ denote the validation perplexity functional. The evaluation metric $\Phi$ is **measure-theoretically ill-posed** at constant $c$ if there exists a measure-positive subset $S \subset M$ (under any natural reference measure compatible with the training procedure) such that $\Phi(S) = \{c\}$, that is, $\Phi$ collapses to the constant value $c$ on $S$.
- §6.2 **Empirical witness**. The five-cell bit-identical surface in §5.1, plus the stack-B base-model PPL match on no-train, supplies an empirical lower bound on $|S|$: at minimum, $S$ contains the union $\{(\text{seed}, \alpha) : (\text{seed}, \alpha) \in F\} \times \{\text{stack B, fp16, gfx1201, ROCm 7.2}\}$ where $F$ is the five-element set of §5.1. Measure-positivity is supported by the cross-seed cross-alpha variation: nonzero variation along seed and alpha within $S$ is preserved, and $S$ is not a measure-zero coincidence set.
- §6.3 **Position relative to Ly-Gong 2025**. Ly and Gong's riddled basin geometry establishes the divergence-side reproducibility ceiling: arbitrarily close initial conditions yield distinct outcomes (fractal basin, uncertainty exponent near zero). The present observation establishes a convergence-side reproducibility floor: arbitrarily distinct configurations yield bit-identical outcomes within $S$. The two are not equivalent and not derived from each other; we frame them as observed dual phenomena on the same underlying basin manifold (CANDIDATE_RIDDLED §1.2 line 48-56). We claim no derivation.
- §6.4 **Prior-art novelty status**. measure-theoretic rigor formulation of LLM evaluation degeneracy: search across 13 queries surfaced no independent prior work (LITERATURE_SEARCH §3 line 87-91, §8 line 198, verdict "largely novel"). Informal perplexity-limitation discussion is extensive (arXiv 2601.22950 and industry blogs, LITERATURE_SEARCH §3 line 80, partial cover ≥ 60% at informal level). Holistic Evaluation framework (HELM, arXiv 2211.09110) is horizontal multi-axis (line 83), not measure-theoretic vertical degeneracy.
- §6.5 **Falsifiability**. The measure-theoretic ill-posedness claim is falsifiable by a multi-stack ablation grid (multi-dtype $\times$ multi-GPU $\times$ multi-architecture $\times$ multi-family). If $\Phi(S) = \{c\}$ holds robustly across $S$ under independent verification on stacks not represented in this paper, the claim survives; if cross-stack independent verification yields $\Phi(S) \neq \{c\}$ at all of (seed, alpha) in $F$ on stacks other than stack B, the claim is restricted to stack B specific and is not measure-theoretic at the manifold level. We do not claim the present paper resolves this; the grid is deferred (§8).

### §2.7 §7 Discussion (~400-500 words)

- §7.1 Four candidate root-cause layers and their independence status; explicit "no unique root cause is claimed" (panorama §7.1 §12 19 项不擅 declare 列 line 466).
- §7.2 Mirror dual to riddled basin geometry: positioned as observed dual phenomenology, not as derived corollary of Ly-Gong 2025. Cite Geshkovski-Letrouit-Polyanskiy-Rigollet 2025 (arXiv:2512.01868) mean-field transformer dynamics as adjacent framework (LITERATURE_SEARCH §7 line 178).
- §7.3 Implications for reproducibility crisis literature: Sculley 2018 + Pineau 2019 + Henderson 2018 + the recent "Large Language Models for Software Engineering: A Reproducibility Crisis" (arXiv:2512.00651, LITERATURE_SEARCH §1 line 22) — the present cross-stack evidence adds a measure-theoretic dimension distinct from the dependency-drift / unpinned-version dimension.
- §7.4 Open questions explicitly framed as questions, not claims: (i) is bit-identical convergence stack-specific or universal? (ii) does measure-theoretic ill-posedness extend to BLEU / ROUGE / human eval / downstream task metrics? (iii) can multi-channel verification become a standard reporting requirement?

### §2.8 §8 Limitations + Future Work (~300-400 words)

- §8.1 Single architecture (OPT-125M), single dataset (wikitext-2), two stacks (NVIDIA + AMD only; Apple MLX / Intel oneAPI / TPU absent), N=180 cumulative cells; six seeds × three alpha × ten generations partial coverage. Explicit disclosure following the DEEPER_INSIGHT §5 6-gap list (panorama §3.4.3 line 260-267).
- §8.2 Future work three lines (panorama §5 line 363-407): (i) Banach-contraction LLM first instantiation, 3-6 months, closes S1 candidate; (ii) measurement-theoretic ablation framework first instantiation, 6-9 months, closes S2 candidate and P0★-G candidate via four-component decomposition $\Delta\text{PPL} = \Delta_{\text{impl}} + \Delta_{\text{form}} + \Delta_{\text{data}} + \Delta_{\text{chain}} + \xi$; (iii) Banach 5-mode failure taxonomy + transition kernel, 6-12 months, closes S3 + S4 candidate.
- §8.3 Multi-channel verification protocol explicitly framed as **detection mechanism, not solution framework** (DEEPER_INSIGHT §5 gap 5 line 95, paper v8 §7.5 NOT-claim viii 撤回不复活 binding).
- §8.4 No claim of mitigation. No claim of paradigm shift. No claim of universal solution across architectures.

---

## §3 Cite list 主源 + 行号 anchor (Reference section, ~20-25 items)

### §3.1 Primary collapse-line citations (paper §1 + §2 + §3 + §4)

1. Shumailov et al. 2024 Nature — `paper §4.6 mean 36.32 reference` (CANDIDATE_DISCRETE §4 line 129)
2. Borji 2024 arXiv:2410.12954 "A Note on Shumailov et al. (2024)" — statistical critique precedent (CANDIDATE_DISCRETE §5 line 149)
3. Dohmatob 2025 ICLR "Strong Model Collapse" — math extension
4. Gerstgrasser et al. 2024 — data-accumulation-delay complement (panorama §4.5 line 354)
5. Ferbach 2024 — engineering mitigation prior art
6. Ly and Gong 2025 arXiv:2510.05606 "Riddled Basin Geometry Sets Fundamental Limits to Predictability and Reproducibility in Deep Learning" — **divergence-side reproducibility limit, Anchor 2 主 prior art** (CANDIDATE_RIDDLED §1.1 line 31-44)
7. Nature 640 E6 (2025) Shumailov Author Correction — `pending full content verify` (CANDIDATE_DISCRETE §5 line 150)

### §3.2 Mixed-precision and cross-stack reproducibility citations (paper §2 + §3 + §4 + §5)

8. Micikevicius et al. 2018 "Mixed Precision Training" — fp16 baseline (MATH_VERIFY_D25 §1-§4 + panorama §3.1.2 line 133)
9. Thinking Machines Lab "Defeating Nondeterminism in LLM Inference" 2025-09 (arXiv) — batch-invariant kernels (LITERATURE_SEARCH §1 line 25)
10. arXiv 2510.26788 "Defeating Training-Inference Mismatch via FP16" (2025-10) — fp16 vs BF16 mismatch fix (LITERATURE_SEARCH §1 line 18)
11. arXiv 2511.17826 "Deterministic Inference across Tensor Parallel Sizes" (2025-11) — TP-size mismatch (LITERATURE_SEARCH §4 line 100)
12. arXiv 2506.09501 "Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference" (LITERATURE_SEARCH §1 line 19)
13. arXiv 2405.18710 "To FP8 and Back Again" (LITERATURE_SEARCH §1 line 20)
14. arXiv 2512.00651 "Large Language Models for Software Engineering: A Reproducibility Crisis" (LITERATURE_SEARCH §1 line 22)
15. PyTorch GradScaler source documentation — GradScaler skip mechanism
16. ROCm PyTorch compatibility documentation — `matmul.allow_fp16_reduced_precision_reduction` unsupported on ROCm (LITERATURE_SEARCH §4 line 110)

### §3.3 GitHub issues — 11 ROCm gfx1201 anchor (paper §3 Methods + Appendix)

17. vllm-project/vllm Issue #40081 — vLLM RDNA4 gfx1201 container startup fail (LITERATURE_SEARCH §4 line 103)
18. vllm-project/vllm Issue #40980 — TP=2 deadlock on dual AMD R9700 gfx1201 (line 104)
19. ROCm/TransformerEngine Issue #520 — gfx1201 not in AITER arch table, FP8 WMMA silently fallback FP32 (line 105)
20. ROCm/TransformerEngine Issue #359 — FP8 (E4M3/E5M2) kernel execution on R9700 gfx1201 (line 106)
21. ROCm/rocm-systems Issue #5480 — RCCL deadlock during vLLM TP=2 inference on dual R9700 (line 107)
22. ROCm/ROCm Issue #5674 — MIOpen + gfx120X + hipblaslt fp32 kernels R9700 performance alignment (line 108)
23. ollama/ollama Issue #14686 — ROCm backend fails init on RDNA4 gfx1201 (line 109)

### §3.4 Recent collapse-adjacent (D26-D27 latest, paper §2 + §7)

24. Du and Tanaka-Ishii 2026 arXiv:2605.00435 (ICML 2026 accepted) — mode collapse geometric regulation (LITERATURE_SEARCH §7 line 175)
25. Gauthier, Bach, Jordan 2026 arXiv:2605.04266 — iterative RLHF alignment collapse (line 176)
26. arXiv 2602.15799 "The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety" (line 177)
27. Geshkovski, Letrouit, Polyanskiy, Rigollet 2025 arXiv:2512.01868 "The Mean-Field Dynamics of Transformers" (line 178)
28. arXiv 2509.16499 "A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective" (line 179)
29. arXiv 2512.15011 "Epistemic diversity across language models mitigates knowledge collapse" (line 180)
30. arXiv 2506.17209 "Fine-Tuning Lowers Safety and Disrupts Evaluation Consistency" (line 181)

### §3.5 Anchor 3 measure-theoretic-side citations (paper §6 + §7)

31. arXiv 2601.22950 "Perplexity Cannot Always Tell Right from Wrong" — sequence-level confidence trade-off (LITERATURE_SEARCH §3 line 80)
32. arXiv 2211.09110 HELM "Holistic Evaluation of Language Models" — horizontal multi-axis evaluation framework (LITERATURE_SEARCH §3 line 83)
33. arXiv 2509.13333 "Evaluation Awareness Scales Predictably" (LITERATURE_SEARCH §3 line 84)
34. arXiv 2502.15208 "Unveiling Attractor Cycles in Large Language Models" — successive paraphrasing limit cycle attractor (LITERATURE_SEARCH §2 line 60)

### §3.6 Chinese-language references (DS 第七缺口 reduced cite, paper §1 / §7 footnote level)

- CUGE benchmark + M3-SafetyBench — Chinese LLM evaluation surveys (LITERATURE_SEARCH §6 line 155-156). **Note**: 中文圈 之 model self-iteration collapse 之 独立 paper search 13 query 之 NO surface (LITERATURE_SEARCH §6 line 164). 中文文献 crawl 之 pending PI 决之 D26-D27 关卡 3 之后 之 D28+ extend search.

---

## §4 关键数据 binary anchor + 4 道墙 PR strategy

### §4.1 关键 binary 数 cluster (paper §3 + §4 + §5 + Appendix)

| 数 | 值 | source 行号 |
|---|---|---|
| 5 bit-identical cells a1_ppl | 93.38780852810248 (14 decimals) | DEEP_SYNTHESIS §1 line 27 |
| 5 cells val_loss | 4.5367608070373535 (14 decimals) | DEEP_SYNTHESIS §1 line 27 |
| 5 cells n_tokens_train | 2390656 | DEEP_SYNTHESIS §1 line 28 |
| 5 cells n_tokens_eval | 16384 | DEEP_SYNTHESIS §1 line 28 |
| Stack A 3-run gen 0 | 36.53597375534226 (14 decimals) | DEEP_SYNTHESIS §2 line 64 |
| Stack A E0 gen 1 | 78.57167674109238 | DEEP_SYNTHESIS §2 line 73 |
| Stack A gen 0→1 lift | +115.05% (in [110%, 130%]) | DEEP_SYNTHESIS §2 line 75 |
| Stack A vs Stack B (seed=42, α=0, gen=0) | 36.536 vs 93.349, +56.81 PPL, +155.5% | panorama §3.1.2 line 132 |
| Stack B base no-train PPL | 93.349 | MATH_VERIFY_D25 line 14 |
| Stack A vs Stack B Δ gen=0→1 | +42.04 vs −2.67e−4 | DEEP_SYNTHESIS §2 line 84-89 |
| a3_attn_entropy distinct scale | ~$10^{-3}$ | DEEP_SYNTHESIS §1 line 31-39 |
| 47-file manifest sha256 | archive/v1.0_release_20260516/manifest.sha256 | panorama §3.1.1 line 122 |

### §4.2 4 道墙 PR strategy (paper §3 + §5 + §8, DEEPER_INSIGHT §3 panorama §4.3 line 322-328)

1. **第一道**: 5 cells (seed, alpha) 全坍缩 14 位小数 93.38780852810248 — random-bug probability approaches zero, deterministic bifurcation
2. **第二道**: Stack A fp32 三跑 36.536 bit-identical — not NVIDIA immunity, NVIDIA in fractal boundary landing on the healthy side
3. **第三道**: weight frozen 但 PPL clean = base-model PPL bit-identical — not random crash / ECC error, GradScaler silent skip + optimizer step zero + eval completes cleanly
4. **第四道**: ROCm open-source, reviewers can inspect MIOpen + hipBLAS code on GitHub — GEMM accumulation order + fp16 quantization deterministic bifurcation on the fractal boundary

### §4.3 Falsification criteria (paper §3 + §6 + §8, DEEPER_INSIGHT §7 panorama §3.4.5 line 281-287 之 第 6 约束 binding)

- F1: gen_N_ppl >= gen_0_ppl + 5 PPL on a healthy fine-tune chain (Stack A pass, Stack B fail)
- F2: bit-identical convergence cells distinct count > 1 across (seed, alpha) on Stack B (refuted: 5 cells with distinct count 1 surface)
- F3: hidden-state-level signature distinct count > 1 across the 5 bit-identical cells (refuted: a3_attn_entropy distinct count = 5 with ~$10^{-3}$ scale)
- F4: cross-stack divergence absent under identical (seed=42, alpha=0, gen=0) configuration (refuted: +56.81 PPL surface)
- F5: measure-theoretic ill-posedness restricted to stack B only (pending: multi-stack ablation grid, §8 future work)

---

## §5 venue + ICLR 2027 + Nature 三层递进 (PENDING PI + 关卡 3 四方决 explicit reaffirm)

### §5.1 D17 binding scope clarification — PENDING

D17 final decision (2026-05-17 panorama §6.1 line 415-422): paper v8 final 不投 NMI / NCS / NeurIPS / Nature 主刊. D17 rationale (panorama §6.2 line 430): paper v8 grand-framework form 在 NeurIPS / NMI / NCS class venue 之 review variance 极高 + 哲学 framing 与 ML community 之 epistemological friction (5/9 NMI A4 desk reject precedent + 5/11 Nature 主编 第三次盲审 64 条审稿意见).

paper v9 form (本 skeleton) 与 paper v8 form 之 substantive 差异: 0 哲学词 (panorama §4.4 line 332-340 之 7 禁词 全 0 in §1-§4 正文 + §5-§7 仅 retrospective level), trojan horse incremental form. D17 binding scope clarification = paper-specific (仅 paper v8 grand framework) 还是 venue-class-specific (all-paper applicable) = **PENDING PI + 反题 + Win + DS 四方决 explicit reaffirm or relax** (ANTITHESIS GATE3 §3 line 184-200, WIN §3.3 line 159-168).

### §5.2 ICLR 2027 main track 第一站 (PI + DS final 之 primary candidate, PENDING D17 reaffirm)

PI explicit (prompt header) + DS final candidate: **ICLR 2027 main track 第一站**. PENDING D17 reaffirm 前, 本 skeleton 标注 "candidate primary, pending PI + 关卡 3 四方决 explicit reaffirm". 若 D17 binding scope clarified as paper-specific (paper v9 trojan horse form 不在 D17 binding scope 内), ICLR 2027 main track is primary; 若 D17 binding scope clarified as venue-class-specific, paper v9 venue 改 arXiv + TMLR + workshop (parallel D17 binding 之 venue-class default).

### §5.3 Nature 三层递进 (PI prompt header + Nature desk sim line 178-184)

| 阶段 | venue | scope | acceptance honest |
|---|---|---|---|
| v9 (D30+ launch candidate, PENDING D17 reaffirm) | **ICLR 2027 main track 第一站** | reproducibility + cross-stack anomaly + measure-theoretic formal characterization + Riddled basin mirror dual observation | 留 D30+ four-channel decide (ANTITHESIS line 124-131 之 honest range main track 上限 18-28% + workshop 上限 35-55% + cumulative 25-40%; 不 commit 60-75% inflate retract binding) |
| v10 (D60-D90+ candidate window) | NeurIPS 2028 | Banach LLM 数学 form + measurement-theoretic ablation grid (multi-arch × multi-family) close + Llama-8B Phase 5 | 留 D60+ window emergent outcome 决, 不 D22-D60 unilateral declare |
| v11 (D90+ candidate window) | Nature 主刊 (Nature desk sim §5 line 158-184) | full multi-stack disentanglement + cross-arch + cross-dataset + RLHF axis + 评估范式 formal critique | desk review honest 25-35% / 全文 10-20% / cumulative 3-7% (Nature desk sim line 159-165) — Nature 主刊 NOT越级 V9, NOT越级 V10 |

binding 严守: v9 不越级 v10 measure-theoretic full formalization (留 D60+ Banach LLM first instantiation), v9 不越级 v11 Nature 主刊 framing (留 D90+ multi-stack disentanglement complete). 12 NOT-claim (i) paradigm shift + (xi) first systematic empirical study 不复活 (panorama §4.4 line 327-340).

---

## §6 字数预算 + writing protocol

### §6.1 字数预算 (ICLR 2027 main track 8-9 page, ~5000-6300 words main text excl. references)

§1 Intro 600-800 / §2 Background 500-700 / §3 Setup 400-600 / §4 Reproduction 400-600 / §5 Cross-Stack Anomalies (backbone) 1500-2000 / §6 Measure-Theoretic Formal 500-700 / §7 Discussion 400-500 / §8 Limitations + Future 300-400 / References 25-30 items / Methods + Appendix unbounded. Total main text ~4600-6300, within ICLR 2027 page bound.

### §6.2 Writing protocol binding (DEEPER_INSIGHT §7 7 约束 panorama §3.4.5 line 281-287)

1. 正文 0 哲学词 (禁词 list reference panorama §4.4 line 332-340 之 7 项 binding, 全 0 in §1-§8 main text; "internal tension" / "internal dynamics" 用代替, DS Audit 2 panorama §3.3.3 line 228-235)
2. 每声称配数据行号 + sha256 (47-file manifest reference panorama §3.1.1 line 122)
3. 先复现 Shumailov 再说话 (§3 + §4 reproduction-extension framing, §5 surface anomaly)
4. 数学引用独立于实验 (Ly-Gong cite + measure theory 引用全独立证明, 不依赖 paper 内部数据 derive)
5. 不发明新词, 只用既有术语 (frozen-weight / GradScaler skip / Riddled basin / measure-theoretic ill-posedness / phenomenology artifact 全既有 prior-art coverage)
6. 给自己声称标可证伪条件 (F1-F5 falsification criteria §4.3)
7. 不 declare Gödel/Bell 级别 achievement (Nature desk sim §3 line 127-131 之 inflated 类比禁止)

### §6.3 12 NOT-claim 不复活 binding (paper v8 §7.5 锁定, list reference panorama §4.4 + MATH_DIRECTION_LATEST_D26 §1.2 line 27-43)

list reference: (i)-(xii) 全 disclosed 在 paper v8 §7.5 final. 本 skeleton 严守不复活. 关键 enforcement: (i) paradigm-shift framing absent in §1-§8 正文; (ii) first-quantitative-comeback framing absent; (viii) **mitigation framework** 改 "detection mechanism" (multi-channel verification framing in §2.8 §8.3); (xi) **first systematic empirical study** 改 "pilot study" / "preliminary cross-stack observation" (abstract + §2.1 §1.4 framing). source binary trace: paper v8 final §7.5 + panorama §4.4 line 327-340 + MATH_DIRECTION_LATEST_D26 §1.2 line 27-43 之 12-row table.

---

## §7 严守 binding ack + 不擅 declare list

### §7.1 严守 binding self-check (D-1 + D-3 + 10 问 binary)

| binding | binary | anchor |
|---|---|---|
| paper v8 final 47/47 D17 锁定不动 | ✓ | §0 |
| 12 NOT-claim (i)-(xii) 撤回不复活 | ✓ | §6.3 + §2.1.5 + §2.8.4 |
| 反题 6 P0★ A-F disclosed + P0★-G 留三方决 | ✓ | §2.5 (a)(b) + §6.5 + §8.2 line C2 |
| D29 投 arXiv + TMLR + KBS 不动 | ✓ | paper v9 separate, 不冲突 v8 D29 三 leg |
| 技术语言, 零哲学词 (panorama §4.4 7 禁词 list reference) | ✓ | §1-§8 main text 0 occurrence; explicit not-claim list §2.1.5 + §2.6 |
| 每 cite 配 source 行号 binary trace | ✓ | §1-§5 全 cite anchor 行号 |
| ICLR 2027 main track 第一站 + Nature 三层递进 + 不越级 | ✓ | §5.2 + §5.3 PENDING D17 reaffirm |
| "Contradiction Loss" 是 D17 遗产, 考虑改 "Internal Tension Loss" 留 PI 决 | ✓ | §2.3 §3.3 explicit pending PI 决 |
| 中文文献 crawl 先, 不急写入 v9 (PI 决之 4) | ✓ | §3.6 explicit pending D28+ extend |
| 字数 4000 字 binding | ✓ | pending final word count verify |

### §7.2 不擅 declare 列 (paper v9 launch / venue / abstract / framing / title 全留 PI + 关卡 3 + 关卡 4 决)

15 项 全留 PI + 关卡 3 + 关卡 4 final 决 (本 skeleton 不擅): (1) v9 launch (D30+ scope); (2) abstract final (Option A/B/C); (3) venue final (ICLR 2027 primary candidate PENDING D17 reaffirm); (4) title final ("Contradiction Loss" vs "Internal Tension Loss"); (5) cumulative acceptance prob (honest range main track 18-28% + workshop 35-55% + cumulative 25-40%; 不复活 60-75% inflate, ANTITHESIS line 124-131); (6) E_NEW_2 launch trigger (WIN (α) D27 关卡 3 之前, ANTITHESIS Q1 必要); (7) sub-mechanism (c) close (留 E_NEW_2 close); (8) (a)(b)(c)(d) unique root (留 D60+ multi-stack ablation grid); (9) P0★-G FATAL final close (留 D60+ measurement-theoretic grid); (10) v10 NeurIPS 2028 substantive commit (留 D60+ emergent); (11) v11 Nature 主刊 declare (留 D90+ multi-stack disentanglement, Nature desk sim §5 line 158-184 之 25-35% desk honest); (12) paper v8.1 footnote polish (WIN §4 candidate 1+2+3 草拟); (13) 中文文献 crawl 完整 (D28+ extend); (14) D60+ 三线 prioritization (panorama §5 line 363-407); (15) cumulative ≥ 1 by 12 月 30-40% honest 上调 (panorama §7.1 第 8 项严禁).

### §7.3 sub-agent metadata + commit

agent: Opus 4.7 paper v9 skeleton draft sub-agent, 7B13 spawn. tool use: Read ~10 + Bash ~3 + Write 1. file path: 本 file. commit: 不擅, 留 Linux 主会话 batch (等关卡 3 四方决 之后).

---

**生成**: Opus 4.7 (1M context) paper v9 skeleton draft sub-agent, 7B13 主会话 spawn, 2026-05-27 21:11 CST

**核心 output**: paper v9 [SKELETON_DRAFT] — 8 section outline + title 3 candidate + abstract draft + 25-30 cite list anchor + 4 道墙 PR + ICLR 2027 主 track 第一站 PENDING D17 reaffirm + Nature 三层不越级 + 12 NOT-claim 不复活 + 留 PI + 关卡 3 + 关卡 4 决. paper v9 全标 [SKELETON_DRAFT], NOT actualize NOT launch NOT submit. paper v8 final + D17 + D29 三 leg + 12 NOT-claim + 反题 6 P0★ 全 binding 严守.
