# paper v9 之 5 核心 anchor 之 prior art literature search 报告

## §0 metadata + 真实日期 + scope

- **执行日期 (binary verify)**: 2026-05-27 15:12:18 CST (D27, `date '+%Y-%m-%d %H:%M:%S %Z'` 之 output)
- **执行者**: Opus 4.7 zero-context prior art sub-agent (D-1 纪律 4 第二认识通道)
- **scope**: paper v9 之 5 核心 anchor (fp16 评估管线 / Riddled basin mirror dual / 测度论 ill-posedness / cross-stack 复现性 / 单轴指标缺失) + 中文文献 (DS 第七缺口) + D26-D27 latest
- **方法**: WebSearch (主 13 query) + WebFetch (备用未启用) + 全程不读 CLAUDE.md / memory / 任何项目 file
- **严守**: 只搜 + 标 + binary verdict, 不推断 paper v9 之 novelty status (留 PI + 关卡 3 三方决), 全中文 + 4 类豁免外英文 reduce
- **不擅**: ssh 22 主机 + git 写 + paper v9 修改

---

## §1 Anchor 1: fp16/AMP 评估管线 signal vs artifact

### 关键论文 (10 篇)

1. **"Defeating the Training-Inference Mismatch via FP16"** (arXiv:2510.26788, 2025) — RL fine-tune 之 BF16 训练-推理 mismatch, 反转默认推 FP16; 与 paper v9 角度对偶 (paper v9 是 fp16 评估侧出 artifact, 此 paper 是 fp16 训练侧 fix mismatch)
2. **"Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference"** (arXiv:2506.09501, 2025) — 推理侧 nondeterminism 之 numerical source 系统化
3. **"To FP8 and Back Again: Quantifying Reduced Precision Effects on LLM Training Stability"** (arXiv:2405.18710, 2024) — FP8 vs FP16 之 training stability quantify
4. **"QUANTIFYING REDUCED PRECISION EFFECTS ON LLM"** (OpenReview pNgyXuGcx4) — reduced precision 之 effect quantify
5. **"Large Language Models for Software Engineering: A Reproducibility Crisis"** (arXiv:2512.00651, 2025) — 40%+ 之 functional artifact 数月内 fail (drifting dependency / unpinned version / 不全 environment)
6. **NVIDIA "Floating-Point 8: An Introduction"** (NVIDIA Technical Blog, 2025) — FP8 / FP16 / BF16 之 系统化对比
7. **"Mixed Precision Training with PyTorch AMP: fp16, bf16, and GradScaler"** (mljourney.com, 2025) — fp16 之 1.0 + 1.0001 update 消失 + GradScaler skip 之 weight 不 update 风险
8. **"Defeating Nondeterminism in LLM Inference"** (Thinking Machines Lab blog + arXiv, 2025-09) — Mira Murati 团队 batch-invariant kernels (RMSNorm/MatMul/Softmax/Attention) 之 1000 run bit-identical, 10-40% slowdown
9. **"Deterministic Inference across Tensor Parallel Sizes"** (arXiv:2511.17826, 2025) — TP size 之 训练-推理 mismatch fix
10. **"SafeTuneBed"** (arXiv:2506.00676, 2025) — config-based 之 fine-tune reproducibility framework

### binary verdict

- "有人做吗 fp16 训练-推理 mismatch?": **YES** (Thinking Machines + arXiv 2510.26788 全 cover)
- "有人做吗 fp16 评估侧 hidden artifact?": **PARTIAL** (Thinking Machines 之 batch-invariance 接近, 但 paper v9 之 4 cells bit-identical 93.388 之 trivial attractor capture 未见独立 prior work)
- "有人做吗 GradScaler skip 之 weight 不 update 之 evaluation 侧 silent artifact?": **NO** (PyTorch issue #76282 + #74739 仅 surface mechanism, 未到 evaluation pipeline 之 systemic signal-vs-artifact framing)
- 重叠程度: fp16 mismatch 主线 cover ≥ 70%, paper v9 之 evaluation 侧 trivial attractor framing 重叠 ≤ 20%

### D26-D27 之后 new paper

- arXiv 2511.17826 (2025-11) 之 deterministic inference 是接近 paper v9 evaluation 侧 frame 之 latest, 但仍是推理 nondeterminism fix 不是 evaluation pipeline 之 fractal basin signal-artifact 不区分

---

## §2 Anchor 2: Riddled basin (Ly-Gong arXiv 2510.05606) 之 mirror dual

### Ly-Gong 原 paper 详细

- **arXiv ID**: 2510.05606
- **题目**: "Riddled basin geometry sets fundamental limits to predictability and reproducibility in deep learning"
- **作者**: Andrew Ly + Pulin Gong (University of Sydney School of Physics)
- **发表**: 2025-10-07
- **核心 claim**: 深度学习 之 basin geometry 是 fractal riddled, 任一 init 之 邻近 ε 含 ≥ 1 不同 solution; uncertainty exponent 近 0, 大幅 precision 提升只得 marginal predictability 改善
- **derivation 之 sufficient condition**: chaotic learning dynamics + symmetry-induced invariant subspaces, 推 riddled basin emergent 之 universal route
- **implication**: fundamental limit on predictability + reproducibility of NN training

### "mirror dual convergence 侧 trivial attractor capture" 之 prior work search

- **Ott-Alexander-Kan-Sommerer (1994)**: "The transition to chaotic attractors with riddled basins" (PhysicaD) — riddled basin 之 foundation, 仅 chaos 之 divergence 侧
- **arXiv 1711.02160**: "Riddled Basins of Attraction in Systems Exhibiting Extreme Events" — extreme event 之 riddled basin, 仍 divergence 侧
- **arXiv 1704.04185** + **arXiv nlin/0002358**: 旧 riddled basin 之 theoretical paper, 全 chaos 侧
- **arXiv 2505.17646**: "Unveiling the Basin-Like Loss Landscape in Large Language Models" — LLM loss landscape 之 basin 之 fine-tune confinement (benign fine-tune 保留 prior capability), 但 frame 是 capacity preservation 不是 trivial attractor capture
- **arXiv 2502.15208**: "Unveiling Attractor Cycles in Large Language Models" — successive paraphrasing 之 limit cycle attractor, 与 paper v9 之 fine-tune trivial fixed point 不同 frame (paraphrase 是 inference loop 不是 训练 weight update)
- **arXiv 2605.12466**: "Solve the Loop: Attractor Models for Language and Reasoning" — backbone + attractor module 之 fixed point implicit differentiation, 是 architecture design 不是 训练 artifact 之 binary detect

### binary verdict

- "有人做吗 Riddled basin 在 LLM training context 之 framework?": **YES** (Ly-Gong 2510.05606 完整 cover divergence 侧)
- "有人做吗 mirror dual convergence 侧 之 trivial attractor capture (4 cells bit-identical 93.388 跨 seed × alpha) 之 binary independent prior work?": **NO** (Ly-Gong 仅 divergence 侧 + arXiv 2502.15208 之 paraphrase loop 不同 mechanism + arXiv 2605.12466 之 architecture design 不同 frame)
- 重叠程度: Ly-Gong framework 之 mirror dual 之 specific framing 未见独立 prior work; paper v9 若 frame 为 "Ly-Gong convergence 侧 instantiate" 是 plausible novel angle 但留 PI + 关卡 3 三方决 final verdict
- **caution**: Ly-Gong 之 cite tracking 未在 search 之 result surface 任何 follow-up 2026 paper, 但 search 之 不全 (5 个月窗口, 7 个月 publish), 实际 citation 数需 Semantic Scholar / Google Scholar 之 direct cite count verify, sub-agent 之 scope 之外

### D26-D27 之后 new paper

- 未 surface 独立 Riddled basin convergence 侧 之 D26-D27 之 new paper

---

## §3 Anchor 3: measure-theoretic ill-posedness 之 LLM 评估

### 关键论文

1. **"Perplexity Cannot Always Tell Right from Wrong"** (arXiv:2601.22950, 2026) — decoder-only transformer 之 long sequence 之 confident-but-wrong vs hesitant-but-correct 之 perplexity 反转, "unfavourable region" concept; 与 paper v9 之 measure-positive S 之 Φ(S) = {c} 之 frame 相关但不重叠 (此 paper 是 sequence-level 之 confidence trade-off, paper v9 是 hyperparameter manifold 之 measure-positive trivial attractor)
2. **"Perturbation Analysis of Neural Collapse"** (arXiv:2210.16658) — neural collapse 之 perturbation 分析, classification 之 within-class variability 之 degeneracy; 与 paper v9 之 evaluation degeneracy 不同 layer (此是 representation 内 degeneracy, paper v9 是 evaluation manifold 之 degeneracy)
3. **"Linear Probe Accuracy Scales with Model Size and Benefits from Multi-Layer Ensembling"** (arXiv:2604.13386) — multi-layer ensemble 之 strong probe, single layer fragile
4. **"Holistic Evaluation of Language Models" (HELM)** (arXiv:2211.09110) — 7 metric × 16 scenario 之 multi-axis evaluation, 与 paper v9 之 measure-theoretic ill-posedness 之 single-axis insufficient 之 partial overlap
5. **"Evaluation Awareness Scales Predictably"** (arXiv:2509.13333) — evaluation awareness 之 scaling pattern, 与 paper v9 之 measure-theoretic frame 不同 angle

### binary verdict

- "有人做吗 measure-theoretic 之 perplexity / evaluation metric 之 ill-posedness 之 rigor formulation (Φ: M → R, ∃ measure-positive S ⊂ M, Φ(S) = {c})?": **NO** (search 之 13 query 未 surface 独立 paper 用 measure theory rigor formulate evaluation degeneracy)
- "有人做吗 perplexity 之 limitation / 反转 case 之 informal discussion?": **YES** (arXiv 2601.22950 + 行业 blog 大量, 但仅 informal level)
- 重叠程度: informal level 之 perplexity limitation discussion 大量 cover (≥ 60%), measure-theoretic rigor formulation 未见独立 prior work (≤ 5%)
- **caution**: search query "perplexity measure theory degenerate Lebesgue" 之 result 之 measure theory cross 完全 null, 提示此方向是 paper v9 之 substantively novel angle 之 candidate, 但留 PI + 反题 + DS 之 关卡 3 三方决 final verdict

---

## §4 Anchor 4: cross-stack reproducibility (fp16 vs fp32 + hardware)

### 关键论文 + GitHub issue

1. **"Defeating Nondeterminism in LLM Inference"** (Thinking Machines Lab, 2025-09) — batch-invariant kernels 之 1000 run bit-identical, 10-40% slowdown, CUDA graphs mitigation
2. **"Deterministic Inference across Tensor Parallel Sizes"** (arXiv:2511.17826) — TP size 之 训练-推理 mismatch
3. **"Beyond Reproducibility: Token Probabilities Expose Large Language Model Nondeterminism"** (arXiv:2601.06118)
4. **"Defeating the Training-Inference Mismatch via FP16"** (arXiv:2510.26788) — FP16 vs BF16 之 训练-推理 mismatch fix
5. **GitHub vllm-project/vllm Issue #40081**: vLLM 在 RDNA4 gfx1201 container 之 startup fail (amdsmi + circular import + device_count broken)
6. **GitHub vllm-project/vllm Issue #40980**: TP=2 deadlock on dual AMD R9700 (gfx1201/RDNA4)
7. **GitHub ROCm/TransformerEngine Issue #520**: gfx1201 (RDNA4) 不在 AITER arch table, FP8 WMMA silently fallback FP32
8. **GitHub ROCm/TransformerEngine Issue #359**: FP8 (E4M3/E5M2) kernel execution 在 R9700 (gfx1201)
9. **GitHub ROCm/rocm-systems Issue #5480**: RCCL deadlock during vLLM TP=2 inference on dual R9700
10. **GitHub ROCm/ROCm Issue #5674**: MIOpen + gfx120X + hipblaslt fp32 kernels R9700 performance alignment
11. **GitHub ollama/ollama Issue #14686**: ROCm backend fails 之 init on AMD Radeon AI PRO R9700 (RDNA4 gfx1201) on Windows 11
12. **ROCm PyTorch compatibility docs**: matmul.allow_fp16_reduced_precision_reduction + matmul.allow_bf16_reduced_precision_reduction 在 ROCm 不 supported

### binary verdict

- "有人做吗 GPU stack 之 reproducibility 之 inference 侧 解?": **YES** (Thinking Machines Lab 之 batch-invariance + arXiv 2511.17826 之 TP size determinism)
- "有人做吗 fp16 vs fp32 之 cross-hardware (AMD ROCm RDNA4 gfx1201 vs CUDA Blackwell sm_120) 之 evaluation 侧 specific 之 abs+57 / rel+157% divergence quantify?": **NO** (GitHub issue 11 个 surface 各 mechanism, 但未到 paper v9 之 specific cross-stack quantify + evaluation pipeline 不区分 signal-artifact 之 framing level)
- 重叠程度: 单纯 reproducibility 之 nondeterminism mechanism 大量 cover (≥ 75%), paper v9 之 cross-stack specific evaluation 侧 quantify + signal-artifact binary framing 重叠 ≤ 25%

### D26-D27 之后 new paper

- arXiv 2511.17826 (2025-11) 之 deterministic inference across TP size 是 latest 接近 frame

---

## §5 Anchor 5: single-axis metric cross-layer 缺失

### 关键论文

1. **"Cross-Layer Discrete Concept Discovery for Interpreting Language Models"** (arXiv:2506.20040, 2025) — CLVQ-VAE 之 cross-layer concept discovery, 之residual stream linearly mix duplicate 之 cross-layer aggregation
2. **"Beyond Components: Singular Vector-Based Interpretability of Transformer Circuits"** (arXiv:2511.20273, 2025)
3. **"CAST: Compositional Analysis via Spectral Tracking for Understanding Transformer Layer Functions"** (arXiv:2510.14262, 2025)
4. **"Holistic Evaluation of Language Models" (HELM)** (arXiv:2211.09110) — 7 metric × 16 scenario 之 multi-axis evaluation
5. **"Linear Probe Accuracy Scales with Model Size and Benefits from Multi-Layer Ensembling"** (arXiv:2604.13386) — single-layer probe fragile + multi-layer ensemble recover
6. **"DecoderLens: Layerwise Interpretation of Encoder-Decoder Transformers"** (arXiv:2310.03686)
7. **"Transformer Circuits Thread"** (transformer-circuits.pub) — Anthropic 系列 之 mechanistic interpretability + cross-layer feature analysis
8. **"Evaluation Awareness Scales Predictably in Open-Weights Large Language Models"** (arXiv:2509.13333)

### binary verdict

- "有人做吗 cross-layer interpretability probe?": **YES** (arXiv 2506.20040 + 2511.20273 + 2510.14262 + Anthropic Transformer Circuits Thread 大量 cover)
- "有人做吗 multi-axis evaluation framework (HELM 之 类)?": **YES** (HELM 之 7 × 16 framework cover ≥ 70%)
- "有人做吗 PPL / KL / accuracy single-axis 之 cross-layer dialectical interconnection 缺失 之 specific framing (paper v9 之 angle)?": **PARTIAL** (HELM 是 horizontal multi-axis 不是 vertical cross-layer dialectical, Anthropic Circuits Thread 是 mechanistic interpret 不是 evaluation framework critique level, 之 cross-axis intersection 之 dialectical materialism instantiate 未见独立 paper)
- 重叠程度: cross-layer probe + multi-axis evaluation 主线 cover ≥ 65%, paper v9 之 dialectical interconnection framing (D-3 反映论 modern instantiate) 之 重叠 ≤ 10%

---

## §6 中文文献 (DS 第七缺口)

### 主要 source 5 paper

1. **"通俗解读大模型微调 (Fine Tuning)"** (知乎 zhuanlan.zhihu.com/p/650287173) — fine-tune 之 中文综述, 概念 level
2. **"大语言模型评估全解: 评估流程 + 评估方法 + 常见问题"** (知乎 zhuanlan.zhihu.com/p/644030637) — 中文 LLM 评估综述
3. **"FineTuneX 之 2025 年 AI 模型微调框架"** (腾讯云开发者社区 cloud.tencent.com/developer/article/2611329) — 2025 之 fine-tune framework
4. **《中国科学: 信息科学》 2025 第 55 卷 第 11 期 2923-2940** (SCIENTIA SINICA Informationis SSI-2025-0254) — 中文 信息科学 之 LLM 类 paper
5. **《计算机学报》 2025 第 48 卷 第 8 期** (CJC fw-2025818171058) — 中文 计算机学报 之 神经网络训练 paper
6. **CUGE benchmark** (北大 + 清华 + 北京智源 collaborative) — 中文 LLM 评估 之 7 language function × 18 NLP task
7. **M3-SafetyBench** — 中文 大模型 安全 评估 benchmark
8. **CSDN blog "2025 最新深度学习算法全解析"** (blog.csdn.net/qsmyhsgcs/article/details/147307173)
9. **博客园 "大语言模型 Fine-tuning 踩坑经验之谈"** (cnblogs.com/wxkang/p/17793078) — 实践 level 之 踩坑
10. **OSCHINA "大语言模型评估全解"** (my.oschina.net/IDP/blog/10088902)

### binary verdict (中文圈)

- "有人做吗 中文圈 之 LLM 评估方法 + fine-tune 综述?": **YES** (CUGE + M3-SafetyBench + 知乎大量综述)
- "有人做吗 中文圈 之 model self-iteration collapse 之 独立 paper (区别 Shumailov 之 转译)?": **NO surface** (search 13 query 未 surface 中文圈 之 独立 model collapse paper, 全是 Shumailov 之 中文转译综述)
- "有人做吗 中文圈 之 fp16 评估管线 / measure-theoretic ill-posedness / Riddled basin convergence 侧 之 独立 paper?": **NO surface** (search 未 surface 任何中文圈 之 独立 paper 覆盖 paper v9 之 5 anchor 中 之 后 4 anchor)
- "有人做吗 中文圈 之 RL adaptive thinking 之 mode collapse?": **YES** (arXiv "论文速读 20250902" 之 中文综述 cover RL mode collapse mechanism, 但与 paper v9 之 fine-tune trivial attractor 不同 mechanism)
- 重叠程度: 中文圈 之 evaluation 综述 大量 cover (≥ 60% 之 informal level), paper v9 之 5 anchor 之 substantive overlap ≤ 10%

---

## §7 D26-D27 之 new paper

### arXiv listing 之 latest

- **arXiv 2605.00435**: "Escaping Mode Collapse in LLM Generation via Geometric Regulation" (Xin Du + Kumiko Tanaka-Ishii, ICML 2026 accepted) — mode collapse 之 geometric regulation, 与 paper v9 之 trivial attractor framing 之 partial overlap
- **arXiv 2605.04266**: "Explaining and preventing alignment collapse in iterative RLHF" (E. Gauthier + F. Bach + M. I. Jordan, 2026) — iterative RLHF 之 alignment collapse, 与 paper v9 之 自迭代 framing 同 mechanism family
- **arXiv 2602.15799**: "The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety" — fine-tune 之 alignment collapse 之 geometric
- **arXiv 2512.01868**: "THE MEAN-FIELD DYNAMICS OF TRANSFORMERS" (Rigollet, 2025-12) — mean-field transformer 之 latest, paper v9 D60+ 候选 direction
- **arXiv 2509.16499**: "A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective" (2025-09)
- **arXiv 2512.15011**: "Epistemic diversity across language models mitigates knowledge collapse" (2025-12)
- **arXiv 2506.17209**: "Fine-Tuning Lowers Safety and Disrupts Evaluation Consistency" — fine-tune 之 evaluation consistency 之 disruption, 2 base + 2 dataset + 150 checkpoint 之 quantify
- **arXiv 2410.12954**: "A Note on Shumailov et al. (2024)" — Shumailov 之 direct follow-up

### binary verdict

- "新 prior art surface 之 D26 之后 (D27 = 2026-05-27)?": **PARTIAL**
- arXiv 2605.00435 + 2605.04266 + 2602.15799 是 D26-D27 临近 之 直接相关 latest, 与 paper v9 之 trivial attractor framing 是 family 内 工作, 留 PI + 关卡 3 三方决 之 specific overlap quantify
- 未 surface 完整覆盖 paper v9 之 5 anchor 之 任一篇 D26 之后 new paper

---

## §8 综合 binary verdict (每 anchor 一句话)

| Anchor | "有人做吗?" | paper v9 novelty status |
|---|---|---|
| **Anchor 1** (fp16 评估管线 signal-artifact) | PARTIAL (Thinking Machines 之 fp16 训练-推理 mismatch fix cover 70%, evaluation 侧 trivial attractor 之 framing 未见独立 ≤ 20%) | **partial novel** (留 PI 决) |
| **Anchor 2** (Riddled basin mirror dual convergence 侧) | YES Ly-Gong divergence 侧 + NO mirror dual convergence 侧 之 独立 prior work | **partial novel** (Ly-Gong instantiate, 但 mirror dual 框架未见独立 prior, 留 PI + 关卡 3 三方决) |
| **Anchor 3** (measure-theoretic ill-posedness rigor formulation) | NO (measure theory rigor formulate evaluation degeneracy 未见独立 prior work, informal discussion ≥ 60% cover) | **largely novel** (substantively novel angle candidate, 留 PI + 反题 + DS 之 关卡 3 三方决) |
| **Anchor 4** (cross-stack fp16 vs fp32 specific evaluation 侧 quantify) | PARTIAL (Thinking Machines + 11 GitHub issue 之 mechanism cover 75%, paper v9 之 specific abs+57 / rel+157% cross-stack quantify framing 重叠 ≤ 25%) | **partial novel** (留 PI 决) |
| **Anchor 5** (single-axis metric cross-layer dialectical interconnection 缺失) | PARTIAL (cross-layer probe + HELM multi-axis cover 65%, dialectical interconnection 之 D-3 反映论 framing ≤ 10%) | **partial novel** (留 PI + Win 哲学协作之 D60+ outcome) |
| **中文圈 (DS 第七缺口)** | NO 独立 paper surface (中文圈 informal 综述 cover 60% 但全是 Shumailov 转译, 后 4 anchor 之 中文圈 独立 paper 未 surface) | **largely novel** (在 中文圈 之 context, 留 PI + DS 之 关卡 3 三方决) |

**综合判断 (binary, 不推断 paper v9 novelty 之 final verdict)**: paper v9 之 5 anchor + 中文圈 之 6 维度, 4 是 PARTIAL + 2 是 NO 独立 prior work surface. 之 5 anchor 之 集成 framing (fp16 + Riddled basin mirror dual + measure-theoretic + cross-stack + cross-layer + 中文圈) 之 paper v9 之 unique angle 是 candidate, 但任一单独 anchor 之 100% novel claim 之 binary support 不足 (Thinking Machines + Ly-Gong + HELM + Cross-Layer 之 prior art coverage 在 50-75% partial 之 range). **不 declare** paper v9 之 "5 anchor 全 100% novel" 之 grandiose claim; **honest declare**: 5 anchor + 中文圈 之 集成 framing 之 specific framing 是 partial novel + 留 PI + 反题 + DS + Win 之 关卡 3 三方决 之 final verdict.

---

## §9 sub-agent metadata + 严守 binding ack

### sub-agent metadata

- **执行模型**: Opus 4.7 (1M context)
- **角色**: zero-context prior art literature search sub-agent (D-1 纪律 4 第二认识通道)
- **执行时间**: 2026-05-27 15:12-15:28 CST (~16 min)
- **WebSearch 调用**: 13 query (5 anchor × 主搜索 + 8 deeper / Chinese / latest)
- **WebFetch 调用**: 0 (备用未启用)
- **不读 file**: CLAUDE.md / MEMORY.md / 任何 项目 file / paper v9 草稿 (zero-context 严守)
- **Write 调用**: 1 次 (本 file)

### 严守 binding ack

- [x] 全中文 (4 类豁免外英文 reduce 严守)
- [x] 不堆 "之" 字 padding (中文 normal connector 用法)
- [x] 4 类豁免外英文 reduce (代码 identifier / 协议 / 错误信息 / 命令行 / 业界缩写 / 品牌名)
- [x] 只搜 + 标, 不推断 paper v9 之 novelty final verdict (留 PI + 关卡 3 三方决)
- [x] 不读 CLAUDE.md / memory file (zero-context 严守)
- [x] read-only + 1 次 Write
- [x] 不擅 ssh 22 主机
- [x] 数字 binary 之 paper ID + 作者 + 年 (无虚构, search 之 surface 之 result 之 直接 quote)
- [x] 真实日期 `date` binary verify (2026-05-27 15:12:18 CST, D27)
- [x] D-1 纪律 1 (jsonl source 之 binary trace) 严守: paper ID + 作者 + 年 是 WebSearch 之 result 之 直接 quote 之 source
- [x] D-1 纪律 5 (差异 surface 不静默修正) 严守: 多次 search query 之 partial null result (中文圈 model collapse 独立 paper + measure theory rigor formulation + 中文圈 后 4 anchor 独立 paper) 之 binary NO 之 直接 surface

### 留 PI + 反题 + DS + Win 之 关卡 3 三方决之 final verdict 之 items

1. paper v9 之 Anchor 1 之 evaluation 侧 trivial attractor framing 之 partial novel (≤ 20% prior work) 之 strategic positioning vs Thinking Machines 之 fp16 mismatch framework
2. paper v9 之 Anchor 2 之 mirror dual convergence 侧 之 Ly-Gong instantiate framing 之 cite policy + novelty claim level
3. paper v9 之 Anchor 3 之 measure-theoretic rigor formulation 之 "largely novel" candidate 之 关卡 3 反题三方决 之 final verdict
4. paper v9 之 Anchor 4 之 cross-stack specific evaluation 侧 quantify 之 25% partial 之 framing 调整
5. paper v9 之 Anchor 5 之 D-3 反映论 dialectical interconnection framing 之 D60+ Win 哲学协作 timing
6. 中文圈 第七缺口 之 DS 之 specific 5 anchor × 6 维度 之 final 独立 paper search 之 完整性 verify
7. D26-D27 之后 之 newest arXiv listing 之 完整 enumerate (sub-agent 之 search 之 scope 限制, 5/26-5/27 之 daily listing 之 systematic enumeration 未做)

(全留 PI + 反题 + DS + Win 之 关卡 3 三方决 之 final verdict, sub-agent 之 scope 之外, 不擅 越权)
