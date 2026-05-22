# 实验启动方案 — 路径 A + C candidate C (mid) D22 (2026-05-22)

**生成**: Linux 姐姐 7B13 主会话, D22 16:00 CST
**真实日期 binary verify**: `date '+%Y-%m-%d'` → 2026-05-22 (D22, D-day=2026-05-01 anchor)
**触发**: 一凡 D22 PI auto 指令 + Agent 4 (`PATH_AC_PRIOR_ART_DEEP_DIVE_D22`) candidate C 第一推荐 + 一凡 "尽快确定方向"
**前置**: `RESEARCH_CHAIN_SPEC_D22_20260522.md` + `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md`

---

## 0. PI 决 binary trace (D22, 一凡 5/6 答 + auto)

| # | PI 决 | binary 状态 |
|---|---|---|
| 1 | paper v8 D29 投稿 | **推迟** ✓ (D17 final 决 partial reverse, 一凡 PI binary) |
| 2 | 路径 A + C D25-D40 启动 | **自动决 ✓** (candidate C honest 二元排名, final 决留关卡 2 PI 决 + 反题三方决) |
| 3 | N=6 多种子 (paper v8 N=4 → N=6 递增) | **自动决 ✓** (candidate C, 不 跳 N=8 避 5/19 膨胀模式) |
| 4 | 4 维度子集 (A1 + A2 + A3 + A6) | **自动决 ✓** (candidate C) |
| 5 | 路径 B + D defer 至 D60+ cloud A100 | **推迟** ✓ |
| 6 | paper v8.1 打磨脚注 D27-D45 (不撤回 12 不主张) | **确认** ✓ |

---

## 1. candidate C spec lock

### 1.1 model + chain training 配置

- **model**: OPT-125m (paper v8 binding, 12 layer, 768 hidden, 12 head, fp16, ~250 MB VRAM)
- **数据集**: WikiText-2 (paper v8 main, ~2M token)
- **chain training 配置**: paper v8 `cat_arm_b.yaml` 严守不动
  - block_size=64, batch_size=8, AdamW, lr=2e-5, fp16
  - 10 代 per seed, 每代 5 epoch
  - beam_search num_beams=5, repetition_penalty=3.0, match_original output_size
- **EMA**: paper v8 `CATTrainer` 之 EMA model, tau=0.999, kl_update_every=10
- **关键 binding (Agent 4 catch 之 SDPA 注意)**: `attn_implementation="eager"` 必 explicit 配置 (避 SDPA 之 `output_attentions=True` silent fallback + warning)

### 1.2 N=6 多种子方案

- **种子**: `[42, 1337, 2024, 7, 137, 271]` (paper v8 N=4 之 [42, 1337, 2024, 7] + N=6 递增之 [137, 271])
- **α 层级**: `[0, 1, 5, 10]` → candidate C 之 3 层 = `[0, 5, 10]` (avoid α=1 之 transient 噪声层)
  - α=0: baseline (no contradiction loss)
  - α=5: mid 之 contradiction strength
  - α=10: paper v8 main 之 plateau α (-5% PPL drift baseline)
- **10 代生成** per (seed, α): 同 paper v8 chain training scheme
- **总 chain training run**: 6 种子 × 3 α × 10 代 = 180 chain training run
- **statistical power**: N=6 之 path A 之 Pearson r d=0.50 之 power ≈ 0.86 (Agent 4 verify)

### 1.3 4 维度子集 (multi-layer instrument)

每 OPT-125m 之 12 layer 之 per-generation + val 256 句之 mean:

| 维度 | 测量 | per-layer? | 实现 | wall-clock cost |
|---|---|---|---|---|
| **A1. PPL 漂移** | test PPL on WikiText-2 test (paper v8 之 §6 baseline, expand to per-gen trajectory) | no (global) | paper v8 reuse | +0% |
| **A2. 嵌入各向异性** | per layer hidden_state output 之 cosine similarity matrix 之 isotropy score (Mu-Viswanath 2018 + Ethayarajh 2019) | **yes (12 layer)** | HF `output_hidden_states=True` | +5% |
| **A3. attention 头熵** | per head per layer 之 attention pattern Shannon 熵 (Voita 2019) | **yes (12 layer × 12 head = 144)** | HF `output_attentions=True` + `attn_implementation="eager"` | +8% |
| **A6. 每层 EMA 散度** | per layer 之 EMA state vs current weight 之 L2 distance (paper v8 §3.5 之 D^code, expand to per-layer) | **yes (12 layer)** | paper v8 EMA model 之 per-layer L2 hook | +3% |

**total instrument 开销 ≈ +16% wall-clock** (vs paper v8 baseline)

### 1.4 路径 A 多通道交叉验证 (multi-channel cross-verify)

**framing reformulate (一凡 D22 表述严守, dialectical inclusive form, 物质第一)**: 路径 A 的二元目的 = **积累 cross-layer dialectical interconnection 在 LLM 训练机制层缺失/存在的 multi-channel binary evidence**, 不 declare external target ("证明 dialectical totality framing correct" 的 implicit reified target 的 reformulate). evidence accumulation 留关卡 3 反题三方决 + Win 哲学协作 + PI 决的节点.

**核心 binary 判据**:
- A 之 12 layer × 4 维度 trajectory cross-verify
- per (seed, α) 之 12 layer trajectory 之 Pearson r matrix + 互信息 matrix
- **同步 OR 解耦 binary 判据**:
  - 若 ≥ 6/12 layer 之 trajectory r > 0.7 → 跨层 unified motion 证据 partial
  - 若 ≤ 3/12 layer 之 trajectory r > 0.7 → 跨层 isolated motion 证据 partial

**prior art base** (Agent 4 catch):
- CKA (Kornblith 2019) HSIC normalized
- SVCCA / PWCCA (Raghu 2017)
- Anthropic crosscoder + transcoder + SAE
- maofield 不 first methodology, 之 **collapse 域 × dialectical totality framing 之 narrow extension**

### 1.5 路径 C 时间相位模式 (temporal phase pattern)

**framing reformulate (物质第一严守)**: 路径 C 的二元目的 = **multi-layer chain training 时序的 phase transition synchronized OR decoupled 的 binary evidence accumulation**, 不 declare external target. 留关卡 3 反题三方决的节点.

**核心 binary 判据**:
- C 之 chain training 时序之 multi-layer phase transition synchronized OR decoupled
- per (seed, α) 之 10 代 trajectory 之 change-point detection (用 `ruptures` Python library, Agent 4 verify pip install 1 min)
- **同步 OR 解耦 binary 判据**:
  - 若 ≥ 6/12 layer 之 phase transition timing 之 σ < 2 代 → 同步 partial
  - 若 ≥ 6/12 layer 之 phase transition timing 之 σ > 4 代 → 解耦 partial

**prior art base** (Agent 4 catch ★★★★★):
- Clauw 2024 information-theoretic progress measure (mutual info synergy order parameter)
- Schaeffer 2023 mirage critique (emergent ability 之 metric 之 artifact)
- Power 2022 + Nanda 2023 + Liu 2023 grokking anchor
- maofield **不 first methodology**, 之 collapse 域 × grokking 相变数学之部分同构

---

## 2. 9070XT 启动 timeline + 资源

| 时段 | task | resource | conflict check |
|---|---|---|---|
| D22-D24 | **9070XT D-PPL 桥主跑** (paper v8.1 polish footnote P0★-F partial close candidate) | 9070XT GPU 100% | candidate C 之 conflict 严守 = 不 launch |
| D24-D25 | **9070XT code dev** (chain training trainer 之 `attn_implementation="eager"` + multi-layer hook + per-layer EMA L2 save + ruptures install + sklearn Kraskov MI) | 9070XT CPU only | 不 conflict D-PPL 桥 |
| **D25 关卡 2 PI 决** | 一凡 read 本启动方案 + 反题 sub-agent zero-context audit (本方案之 binary verify) → PI 决 launch | n/a | **candidate C 实际 launch 严守 PI 决之关卡 2** |
| **D25-D40** (15 GPU-天 wall-clock, candidate C 仅需 2.7 GPU-天, slack 12 GPU-天) | **candidate C 实际 chain training 跑** (6 种子 × 3 α × 10 代, ~64 GPU-时 actual + ~10 GPU-时 instrument 开销) | 9070XT GPU | 主任务, 无 conflict |
| D40-D45 | **分析** (cross-layer Pearson r + 互信息 + change-point detection) + **paper v8.1 polish footnote 草稿** (D-PPL 桥 + 路径 A + C partial circumstantial 承认, 不撤回 12 不主张) | 7B13 CPU | 不 conflict |
| **D45 关卡 3 反题三方决** | 反题 sub-agent zero-context audit 路径 A + C 结果 + DS 协商 + PI 决 paper v8.1 polish accept | n/a | 关卡 3 PI 决之节点 |
| D45-D55 | Win 哲学协作 spawn (路径 A + C 辩证 reframe + paper v8.1 叙事 framing) | Win 姐姐 | parallel |
| D55-D60 | 关卡 4 PI 决投稿 timing (paper v8.1 投 arXiv + TMLR + KBS 之 reconsider) | n/a | 一凡 PI |

**total 9070XT GPU 占用 D24-D40 = ~3 GPU-天 actual + slack 12 GPU-天 buffer**. 之 实际可行性 ✓.

---

## 3. D-1 纪律 5 之错误 surface 不静默 (Agent 4 catch)

### 3.1 9070XT torch 版本记忆校正

- memory 写: "torch 2.12.0+rocm7.2 / torchvision 0.27.0+rocm7.2 / triton-rocm 3.7.0"
- 9070XT actual (Agent 4 D22 14:55 binary live-verify): **torch 2.11.0.dev20260206+rocm7.0 / torchvision 0.26.0.dev20260216+rocm7.0**
- 功能 ✓ (OPT-125m load 0.24 GB VRAM, gfx1201 RDNA 4 native matmul ✓)
- **memory correction**: 我整合后 update 主会话 memory + 项目级 CLAUDE.md 校正 (D-1 纪律 5 错误 surface 不 静默 instantiate)

### 3.2 HF transformers SDPA 注意

- OPT model 之 default SDPA attention 之 `output_attentions=True` 不 support, silent fallback 到 eager + warning
- **binding**: chain training trainer 之 explicit `attn_implementation="eager"` 配置 (避 silent fallback 之 wall-clock latency + 模糊行为)
- 之 D24-D25 code dev 之 必 implement check

### 3.3 路径 A + C 先前研究饱和 honest surface

- Anthropic crosscoder + Clauw 2024 information-theoretic progress measure + Schaeffer 2023 mirage critique + Deep Networks Always Grok 等 ≥ 8 paper-level coverage
- maofield candidate C 之 instantiate **不 first / 不 paradigm shift class**
- maofield 区别候选仅 = 辩证唯物主义框架的窄基础 + collapse 域 × grokking 相变数学的部分同构
- 之 paper v8.1 polish footnote 之 framing 严守 honest narrow (不 inflate paper-level breakthrough)

---

## 4. 严守 binding 重申

- paper v8 final lock 47/47 + 12 不主张撤回 不动 ✓
- D29 投稿推迟 (D17 final 决 partial reverse, 一凡 PI 决 binary)
- D22-D60 unilateral declare emergent paradigm shift 严禁 (反题 P0★-AA ★★ critical)
- D60+ window emergent outcome 严守反题三方决 + Win 哲学协作 + PI 决之节点
- 路径 B + D defer 至 D60+ cloud A100 ✓
- 5/12 + 5/19 inflate 复发 risk 严守 (candidate C 之 N=6 递增不 跳 N=8)
- 健康约束 priority 1 (一凡 alive + sustainable, 之 实验启动不必今天)

---

## 5. 实际 launch 之 PI 决节点

- **关卡 2 (D25)**: 本方案 + 反题 sub-agent zero-context audit → PI 决 launch (binary 答)
- **关卡 3 (D45)**: 路径 A + C 结果 + 反题三方决 + DS 协商 → PI 决 paper v8.1 polish accept
- **关卡 4 (D55)**: paper v8.1 polish + Win 哲学协作 → PI 决投稿 timing

**Linux 姐姐 不 unilateral launch**, 严守 PI 决之节点.

---

## 6. reference

- `PATH_AC_PRIOR_ART_DEEP_DIVE_D22_20260522.md` (Agent 4, 45 KB / 621 行 / candidate C 第一推荐 + 实际可行性 verify)
- `RESEARCH_CHAIN_SPEC_D22_20260522.md` (Phase 2 整合, 8 节 + 14 自检 14/14 pass)
- `EXP_DESIGN_4PATH_METHODOLOGICAL_D22_20260522.md` (Agent 3, 40.7 KB)
- `LITERATURE_SEARCH_C_FULL_CRAWL_D22_20260522.md` (Agent 2, 51 KB / ~90 URL)
- `INDEX_MD_D22_20260522.md` (Agent 1, 47.9 KB / 299 md inventory)
- `VENUE_EVAL_NEURIPS_NMI_D22_20260522.md` (D22 venue eval, 47.6 KB)
- `paper_v8_final_20260516.md` (D17 final lock 47/47)
- `/home/amd/HEZIMENG/MaoField/CLAUDE.md` (项目级 D-1 + D-2 + D-3 standing rule)

---

**方案完成. 等关卡 2 (D25) PI 决 launch**. cope timeline 不 rush. 一凡 alive + sustainable priority 1. 握着.
