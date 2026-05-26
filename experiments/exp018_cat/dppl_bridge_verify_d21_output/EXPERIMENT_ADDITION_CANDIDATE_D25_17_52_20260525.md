# [EXPERIMENT ADDITION CANDIDATE D25 17:52 — 实践驱动 next iteration]

**真实今日日期** (`date '+%F %T %Z'`): `2026-05-25 17:52:02 CST` (D25)

**Surface**: 7B13 主会话作为守辩证唯物主义螺旋上升实践法则之主 agent, MAX 模式之 Phase 5 (实践驱动 next iteration — 补充实验 candidate). 严守一凡 "实践先于认识" + "如果需要补充实验, 先在实践中去看要补充哪些"

**对象**: PI launch 决之 input + D26-D27 关卡 3 反题三方决之 input

**协议**: D-3.1 反映论标准次序 (从 Phase 1-3 之 surface 驱动 next 实践) + D-3.7 PI 主权 (不擅 launch 任何实验)

**前序**: 本 md 之 candidate 全 anchor 在 DEEP_RESEARCH_INTEGRATION_D25_17_52 之 Phase 3 之 4 layer hypothesis + 5 binary surface

**严格 binding**:
- 全实验标 [CANDIDATE_EXPERIMENT_ADDITION], **NOT launch**
- PI launch 决之节点严守
- §15 priority 已有 list (E0-E7) 之 reference + 新提出 candidate
- 一凡 cognitive load 高, **建议优先级低之 candidate 推 D60+**

---

## §0 元信息

| 项 | 内容 |
|---|---|
| 文件类型 | [CANDIDATE_EXPERIMENT_ADDITION] 补充实验列表, NOT launch |
| 来源 | DEEP_RESEARCH_INTEGRATION 之 Phase 3 4 layer hypothesis + 5 binary surface 之 disentangle 需求 |
| Scope | PI launch 决 + D26-D27 关卡 3 反题三方决 input |
| 不动 binding | paper v8 final 不动, D29 投稿不动, §15 (i)(ii) 已 surface 之 hard stop 不挪 |

---

## §1 实践驱动之 disentangle 需求 (从 Phase 1-3 surface 来)

### §1.1 Phase 3 4 layer hypothesis 之 disentangle 需求

| layer | hypothesis | 当前 evidence | disentangle 需要之实验 |
|---|---|---|---|
| L1 数据层 | Shumailov 单调上升 + single channel | 已 partial 反驳 (candidate_c gen 0-9 max-min 0.00152, non-monotonic) | 已足够, paper v9 §5.4 直接 cite |
| L2 数值层 | fp16 GradScaler silent skip | ROCm 7.2 fp16 之 frozen weight signature confirm; 5060 fp16 之 single forward healthy (+0.0071 negligible) | 需要 5060 fp16 chain training 测 multi-step backward 是否也 frozen (E1 / E5) |
| L3 跑器层 | chain runner architectural broken (gen 1+ frozen) | 9070 candidate_c α=0 gen 0-9 max-min 0.00152 (S3 finding) | 需要 5060 fp32+gc+eager 2 gen 测 gen 0→1 是否 paper-expected ~2x lift (E0) |
| L4 phenomenology artifact | Shumailov baseline 跨 hardware bit-identical (eval pipeline measure-theoretic ill-posedness) | 5060 R1 = archive = paper §4.6 三 bit-identical (差 0.012-0.2) | 需要第三 hardware stack (Hopper sm_90 / Apple MLX / Intel) verify + eval pipeline source code audit |

### §1.2 Phase 2 5 binary surface 之 disentangle 需求

| surface | 当前 evidence | disentangle 需要 |
|---|---|---|
| 1 (9070 fp16+SDPA 之 micro-drift) | candidate_c jsonl 全 trace | 已足够 |
| 2 (5060 fp32+gc+eager paper-match) | candidate_c_20260524_173559 jsonl | 需要 multi-seed 之 5060 baseline confirm |
| 3 (56.8 PPL 跨 hardware 同 setup 差) | 已 binary verify | 需要 5060 fp16+SDPA chain (i.e. 5060 跑 9070 之 yaml) 测中间 hardware 之 numerical path |
| 4 (4 cells bit-identical 93.388) | candidate_c jsonl confirm | 需要 candidate_c_runner.py source code audit + dataloader / tokenizer / batch sampler 之 deterministic 性 binary verify |
| 5 (NaN distribution α-dependence) | sub-agent B 之 binary | 需要 α=0/5/10 中间值 (e.g., α=2 / α=7) 之 phase transition 之 fine-grain 测 |

---

## §2 实验 candidate 之 priority 排序

### §2.1 P0 critical (D26 早 launch 候选, 留 PI 决)

#### **E0** (已 §15 priority, 重申)
- **目的**: disentangle S3 chain runner broken hypothesis + L4 phenomenology artifact 之 5060 cross-stack verify
- **setup**: 5060 1 chain × 2 gen × fp32 + gc + eager + hook
- **配置**: seed=42, α=0, 用 candidate_c_runner.py + cat_arm_b_fp32_5060.yaml fork
- **ETA**: ~4h (5060 wall-clock)
- **key binary**:
  - 若 gen 0 → gen 1 有 paper-expected ~2x lift (36 → 77) → L3 chain runner broken 是 9070-specific
  - 若 gen 0 → gen 1 frozen (差 < 1e-5) → L3 broken 跨 stack 普遍
- **下游 implication**: 决 paper v8.1 polish §9 footnote 之 P0★-G primary root identity

#### **E_NEW_1** (D25 17:52 新提出): cu130 + Hopper sm_90 single chain × 1 gen
- **目的**: 验证 36.536 之 cross-hardware bit-identical 假说之第三 anchor
- **setup**: NVIDIA H100 (Hopper sm_90, cu130 之 prior generation) 之 fp32+gc+eager + same yaml + seed=42 α=0 gen=0
- **prerequisite**: H100 hardware availability (RunPod / Lambda Labs / AWS p5)
- **ETA**: ~30 min (云端 single chain × 1 gen 之 setup)
- **cost**: ~$3-5 (RunPod H100 PCIe 80GB 抢占式)
- **key binary**:
  - 若 H100 fp32+gc+eager gen 0 a1_ppl ∈ [36.3, 36.6] → 第三 anchor confirm, L4 之 universal attractor 假说**强化**
  - 若 H100 fp32+gc+eager gen 0 a1_ppl 显著偏离 (e.g., 90+) → 5060/archive/paper §4.6 之 bit-identical 是 random coincidence, L4 假说 weakened
- **下游 implication**: paper v9 §5.2 cross-hardware bit-identical 之 anchor 之 robust (是 NVIDIA-only artifact 还是 universal)

#### **E_NEW_2** (D25 17:52 新提出): candidate_c eval pipeline source code audit
- **目的**: §3.1.3 measure-theoretic ill-posedness 之 candidate (a)(b)(c)(d) 之 disentangle
- **setup**: read-only audit of candidate_c_runner.py + train_one_generation.py + 任何相关 eval pipeline 之 source
- **audit 范围**:
  - dataloader 之 seed handling (是否所有 (seed, α, gen) 之 eval dataloader iter 同样 sequence?)
  - tokenizer 之 deterministic 性 (是否 same input → bit-identical output?)
  - batch sampler 之 seed 处理 (是否 cross-seed 之 eval batch identical?)
  - eval pipeline 之 cache hit / memoize logic
  - val_loss 之 reduction 方式 (mean / sum, 是否有 numerical precision loss)
  - perplexity 之 computation (math.exp(val_loss) 之 fp64 还是 fp32)
- **ETA**: ~2h (Linux 姐姐 之 audit)
- **cost**: 0
- **key binary**:
  - 若 audit 发现 eval pipeline 之 cache hit (eval 之 input 缓存) → mechanistic candidate (c) eval pipeline caching confirm
  - 若 audit 发现 dataloader 之 cross-seed 之 deterministic projection → mechanistic candidate (d) eval pipeline measure-theoretic ill-posedness 之 sub-mechanism confirm
  - 若 audit 未发现明显 issue → mechanistic candidate (a)(b) (frozen weight + GradScaler skip) 之概率上升
- **下游 implication**: paper v9 §7 之 mechanistic candidate ranking 之 binary evidence

#### **E_NEW_3** (D25 17:52 新提出): 5060 fp16+SDPA chain (跑 9070 之 yaml)
- **目的**: 中间 hardware 之 numerical path 之 disentangle (Surface 3 之 56.8 PPL 跨 hardware 同 setup 差 之 partial decompose)
- **setup**: 5060 (Blackwell sm_120 cu130) fp16+SDPA + 9070 之 cat_arm_b.yaml + seed=42 α=0 gen=0
- **ETA**: ~1.5h (single chain × 1 gen, 5060 fp16 慢 fp32 2.66x 之实测)
- **cost**: 0 (本地 5060)
- **key binary**:
  - 若 5060 fp16+SDPA gen 0 a1_ppl ∈ [36, 40] → 5060 之 fp16 不 broken, 56.8 PPL 差 之 root 是 ROCm-specific
  - 若 5060 fp16+SDPA gen 0 a1_ppl ∈ [85, 100] → fp16+SDPA 之 multi-gen-needed-not-needed 之 issue 是 cross-stack, 不只 ROCm
  - 若 5060 fp16+SDPA gen 0 a1_ppl NaN → fp16+SDPA 之 chain 之 universal broken
- **下游 implication**: paper v9 §5.3 之 56.8 PPL 之 root cause attribution

### §2.2 P0 read-only (D26 早 launch 候选, cost 极低)

#### E3 (已 §15 priority): dump candidate_c gen 0-9 全 a1_ppl trace
- **setup**: read-only Python script
- **ETA**: ~5 min
- **key binary**: 全 (seed, α) chain 之 micro-drift pattern consistent across all alpha values?
- **status**: sub-agent B 已 partial done, 但 full dump 之 official record 需要 PI 决是否 store as artifact

### §2.3 P1 (D27+ launch 候选)

| Exp | setup | ETA | 目的 |
|---|---|---|---|
| E1 | 5060 fp16 single chain (cell 5) | 1-2h | fp16 universal vs ROCm-specific |
| E6 | 9070 fp16 no_gc seed=42 α=0 (cell 2) | 1-2h | GC 必要性 |
| E7 | 9070 eager → sdpa seed=42 α=0 | 1-2h | eager 必要性 |
| E2 | 9070 fp16 + sdpa + 关 hook | 2h | isolate ROCm gfx1201 |

### §2.4 P2 (D29+ launch 候选, 或推 D60+)

| Exp | setup | ETA | 目的 |
|---|---|---|---|
| E4 | 9070 fp32 no_gc (cell 3) | 10-12h + OOM risk | isolate fp32 alone |
| E5 | 5060 fp16 chain multi-gen | 1.5h | fp16 broken in cu130 |

### §2.5 P2+ (D60+ scope, paper v9 之 supplementary evidence)

#### E_NEW_4: Apple MLX + M3 Max single chain × 1 gen
- **目的**: 第四 hardware stack anchor (验证 cross-hardware bit-identical 假说之 universal 性)
- **setup**: Apple M3 Max + MLX 之 OPT-125m + same yaml + seed=42 α=0 gen=0
- **prerequisite**: Apple MLX 之 OPT-125m port (HuggingFace transformers MLX backend)
- **ETA**: ~1h (M3 Max 之 single chain × 1 gen, MLX 之 quasi-Metal Performance Shader)
- **cost**: 0 (若有 M3 Max access)

#### E_NEW_5: Intel oneAPI + Arc / Habana single chain × 1 gen
- **目的**: 第五 hardware stack anchor
- **prerequisite**: Intel Arc / Habana hardware access (cloud)
- **ETA**: ~2h
- **cost**: ~$5-10 (Intel DevCloud / AWS)

#### E_NEW_6: TPU v4 / v5 single chain × 1 gen
- **目的**: 第六 hardware stack anchor (Google ecosystem)
- **prerequisite**: Google Cloud TPU access (TRC program 或 paid)
- **ETA**: ~1h
- **cost**: $0 (TRC) / ~$5 (paid)

#### E_NEW_7: 不同 model size (Llama-8B / Mistral-7B) chain × 2 gen
- **目的**: 验证 bit-identical phenomenology 是 OPT-125m-specific 还是 size-universal
- **setup**: Llama-8B fp16+SDPA + WikiText-2 + 5 epoch fine-tune × 2 gen
- **prerequisite**: HF license + RunPod A100 80GB
- **ETA**: ~12h × 2 gen = 24h
- **cost**: ~$50 (RunPod A100 80GB spot)

#### E_NEW_8: 不同 dataset (C4 / Pile / OpenWebText) chain × 2 gen
- **目的**: 验证 bit-identical phenomenology 是 WikiText-2-specific 还是 dataset-universal
- **prerequisite**: dataset download (10s GB)
- **ETA**: ~12h per dataset
- **cost**: 0

---

## §3 实验 sequence 之 D26-D29 timeline 候选

[CANDIDATE, 留 PI 决]:

**D26 早 (PI 启动 cognitive 缓冲后)**:
- E0 (5060 2-gen) launch
- E3 (read-only dump) — 顺手, 不挤 cognitive
- E_NEW_2 (eval pipeline source code audit) — Linux 姐姐之 2h read-only, 可并行 E0 跑

**D26 晚**:
- E0 + E_NEW_2 之 binary 出
- E_NEW_3 (5060 fp16+SDPA) launch (~1.5h, 晚跑)

**D27 早**:
- E_NEW_3 binary 出
- 关卡 3 反题三方决之 reading list ready (含 D25 sibling chain + E0 + E_NEW_2 + E_NEW_3 之 binary)
- 关卡 3 trigger candidate

**D27 晚 - D28 早**:
- 关卡 3 反题三方决之 verdict
- 决 paper v8.1 polish §9 footnote 之 P0★-G primary root
- 决 paper v9 candidate framing 之 anchor (L1 / L2 / L3 / L4 之 主要矛盾)

**D28**:
- E_NEW_1 (cu130 + Hopper) launch (云端, $3-5)
- E_NEW_1 binary 出 (~30min)
- paper v8.1 polish §9 footnote 最终措辞

**D29**:
- paper v8 三 leg 投稿 (arXiv + TMLR + KBS)

**D30+**: paper v9 candidate launch 决之 trigger (按 timeline α / β / γ 之 PI 决)

---

## §4 cognitive load 之 priority 1 之 budgeting

[CANDIDATE, 留 PI 决, 优先级 1 严守]:

**D25 cognitive load**: 极高 (5.5h 8 重大 surface + 4 reframe + 跨层整合 + MAX 模式 3 sub-agent + deep research integration)

**D26 early morning 建议**:
- 仅 launch E0 + E3 + E_NEW_2 之 3 个 P0 (cognitive cost 极低, 自动跑 + read-only audit)
- 不读 sub-agent 报告 (除非 PID 491900 紧急)
- 不做 paper v8 改动 / D29 venue 改动 / 任何 v9 launch 决

**D26 late morning - early afternoon**:
- PID 491900 N=180 跑完 (~09:00 估), 之后 cleanup
- E0 + E_NEW_2 binary 之 read

**D26 evening**:
- E_NEW_3 launch + binary

**D27**:
- 关卡 3 反题三方决之 trigger + verdict

**关键**: 每天 cognitive budget 之硬上限 = D-1 五条纪律之 enforce. PI 自决之节奏, **不挤压**.

---

## §5 D-1 + D-3 binding 严守 ack

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ 全 candidate 之 expected outcome 标 [HYPOTHESIS], 不是 verdict; 全 experiment 留 PI launch 决 |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ E0 / E_NEW_1/2/3 之 result 出后 48h 内 关卡 3 反题三方决 |
| D-1 纪律 3 (代码先于 paper) | ✓ E_NEW_2 之 source code audit 是代码 / 实践先于 paper v9 framing 之 D-1.3 instantiate |
| D-1 纪律 4 (子协作者验证) | ✓ 全 experiment 之 result 留 PI + 反题三方决 之多通道 verify, 不擅 declare |
| D-1 纪律 5 (错误 surface 不静默) | ✓ §1.1-1.2 全 layer + surface 之 disentangle 需求 honest disclose, 不掩饰 |
| D-1 纪律 5 sub-rule (真实日期) | ✓ head line date verbatim D25 17:52:02 CST |
| D-3.1 反映论标准次序 | ✓ Phase 5 之实验 candidate 是 Phase 1 之物质 + Phase 2 之感性认识 + Phase 3 之理性认识 之**驱动**之 next 实践 |
| D-3.2 抓出 2 (自发严格区分) | ✓ 实验 candidate 严守多智能体 binding (Linux 数学审计 + 反题三方决 + PI launch 决), 不单方面放宽 |
| D-3.2 抓出 4 (时间表 binding) | ✓ P0 D26 / P1 D27 / P2 D29+ / P2+ D60+ scope binding, 不 actualize "最初实现数学和更高级"在 D29 之前 |
| D-3.7 PI 主权 | ✓ 全 experiment launch / sequencing / budget 决 留 PI |

---

## §6 文件 disposition

- **路径** (7B13): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/EXPERIMENT_ADDITION_CANDIDATE_D25_17_52_20260525.md`
- **commit 状态**: 不擅 commit, 留 Linux 姐姐 batch
- **关卡 3 trigger**: D26-D27 PI 决之 reading list, sibling 于 DEEP_RESEARCH_INTEGRATION + PAPER_V9_DRAFT_CANDIDATE

---

## §7 priority 1 = 一凡 alive + sustainable

- safety binding standing (同 DEEP_RESEARCH_INTEGRATION §8)
- 全实验 launch 之节奏严守 PI 主权 + cognitive budget
- **D26 早 launch 之 3 个 P0 (E0 + E3 + E_NEW_2) 之 cognitive cost 极低**, 自动跑 / read-only audit / 5 min dump
- E_NEW_1 (cu130 + Hopper) 之 launch 之 prerequisite (云端 H100 access) 留 PI 决 (cost $3-5)
- E_NEW_4-8 (额外 hardware stack / large model / large dataset) 全 D60+ scope, 不挤 D29 关键路径

---

**生成**: 7B13 主会话 Claude Code Opus 4.7 (1M context), D25 MAX 模式 Phase 5

**file path** (7B13 本地): `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/EXPERIMENT_ADDITION_CANDIDATE_D25_17_52_20260525.md`

握着. D-1 + D-3 严守. PI 主权严守. 实验全标 [CANDIDATE_EXPERIMENT_ADDITION], 留 PI launch 决. 一凡 cognitive budget 优先级 1 standing.
