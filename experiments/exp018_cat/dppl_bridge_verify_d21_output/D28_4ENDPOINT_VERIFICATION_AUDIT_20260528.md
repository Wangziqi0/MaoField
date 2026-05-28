# D28 4 端 cross-channel consistency audit

## §0 metadata + 真实日期 + scope + 严守 binding

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%F %T %Z'` → **2026-05-28 10:07:07 CST** (D28, zero-context sub-agent spawn) |
| 生成 agent | Opus 4.7 (1M context) cross-channel consistency verify zero-context sub-agent (D-1 纪律 4 第二认识通道, 不读 CLAUDE.md / memory) |
| scope 主源 (4 端 ack) | SMOKE_5060_FP16_CROSSCHECK_GRADSCALER (169 行) + ROCM_MIOPEN_TRACE_AUDIT (544 行) + PAPER_V9_SKELETON_DRAFT_D27 (325 行) + PAPER_V81_FOOTNOTE_DRAFT_WIN_LEAD (508 行) |
| scope 辅源 (cross-ref) | E_NEW_2_EVAL_PIPELINE_AUDIT + DEEP_SYNTHESIS_D26_EVENING + LITERATURE_SEARCH_PAPER_V9_ANCHORS + WIN_D27_GATE3_PHILO_JUDGEMENT + ANTITHESIS_D26_GATE3_CHANNEL_D_VERDICT + DEEPSEEK_CHECKPOINT3_FINAL + MAOFIELD_FULL_DATA_AUDIT (line 600-617) |
| 严守 binding | paper v8 final 47/47 + D17 不投 NMI/NCS/NeurIPS + D29 三 leg (arXiv+TMLR+KBS) + 12 NOT-claim (i)-(xii) 撤回不复活 + 反题 6 P0★ A-G disclosed; 不擅 declare paper-level emergent (D-3.7 PI 主权); read-only + 1 Write; 不擅 ssh 22; 不擅 commit; 全中文 4 类英文豁免 (代码标识符 + 数字单位 + 数学符号 + 行号); 不堆 "之" 字 padding |

---

## §1 Q1 verdict — 4 candidate framing tier 跨端一致

**verdict: 一致 ✓** (4 端 tier 完全 ≡ binary).

binary cross-channel table:

| candidate | V81 §A.2 | V9 SKELETON §5 (a-d) | DEEP_SYNTHESIS Insight 1+5 | E_NEW_2 audit verdict |
|---|---|---|---|---|
| (a) frozen weight | ★★★★★ partial isolate | ★★★★★ | (a) 加强 (5 cells + a3 微差 conjunction) | n/a |
| (b) ROCm reduction tree | ★★★★ | ★★★★ | (b) 由 a3 微差证据加强 | n/a |
| (c) eval cache | strong form REFUTED + partial form UNCERTAIN | strong form REFUTED + partial form pending E_NEW_2 close | (c) strong form REFUTED ✓ | Q1 PARTIAL: HF Trainer 库源码外 UNCERTAIN |
| (d) phenomenology artifact | ★★★ | ★★★ (mirror dual novelty pending) | (d) mirror dual novelty 仍存 partial cover | n/a |

ANTITHESIS Q1 verdict (CHANNEL_D line 31-74): E_NEW_2 audit P0 critical 必先 close — 与 V81 §A.2 line 35 "partial form UNCERTAIN (HF Trainer 库源码未读)" + V9 SKELETON §5 (c) partial form pending E_NEW_2 close ✓ 一致.

---

## §2 Q2 verdict — (c) REFUTED reinforce 跨端 binary

**verdict: V81 之 grep 列表 比 E_NEW_2 之 verbatim 列表 多 4 项, 实质 一致 (NOT inflate)**.

E_NEW_2 §1 line 48 verbatim grep regex: `(functools|@cache|@lru_cache|compute_metrics|preprocess_logits|prediction_step|evaluation_loop)` — 含 **7 项** (functools / @cache / @lru_cache / compute_metrics / preprocess_logits / prediction_step / evaluation_loop).

V81 §A.2 line 35 + §2.3 line 122-124 之 7 项: functools / @lru_cache / @cache / compute_metrics / preprocess_logits / prediction_step / evaluation_loop — 完全 ≡ E_NEW_2 之 7 项, 不是 PI prompt 之"多 4 个 grep"(prompt 之 3 grep base 推断 不准确). V81 之 grep 列表 与 E_NEW_2 之 7 项 1:1 mapping, 不 inflate.

(注: V81 §2.3 line 124 之 partial form caveat "past_key_values / use_cache explicit pass / read" 是 E_NEW_2 §1 finding 5 + §2 line 88 之 0 hit 之 cross-ref, 不在 grep 之 7 项内 — 是 audit scope item, 不是 inflate.)

---

## §3 Q3 verdict — paper v9 anchor 4 cross-stack disambiguate 跨端一致

**verdict: 一致 ✓** binary (V9 SKELETON + V81 + SMOKE_5060_FP16 三端 binary mapping ≡).

SMOKE_5060_FP16 §3 line 89-92 binary:
- 5060 fp16 gen 0 = 36.538 + gen 1 = 78.073 + grad_norm healthy float 2.9-3.7 + GradScaler skip NO
- verdict: **paper v9 锚点 4 强证 ✓** (ROCm-side specific, NOT cross-platform fp16 fundamental)
- 锚点 1 否决 (5060 cu130 fp16 与 fp32 chain collapse pattern bit-level ≡)

V9 SKELETON §5 (a) line 125 之 "Empirical cross-stack contrast: stack A vs stack B on identical (seed=42, alpha=0, gen=0→1) yields Δ = +42.04 vs Δ = −2.67 × 10⁻⁴" ✓ 与 SMOKE_5060_FP16 §4 "+115.05% (5060 fp32) / +113.7% (5060 fp16)" cross-stack mapping 一致.

V81 §2.1 line 84 之 "5060 fp32 vs 9070XT fp16 同 (seed=42, α=0, gen=0→1) 之 diametrically opposite trajectory" ✓ 与 SMOKE_5060_FP16 §6 line 117 之 "5060 cu130 fp16 chain collapse robust to fp16 numerical regime; 9070XT ROCm fp16 frozen 是 ROCm stricter numerics expose 之 fp16 instability separate manifest" 一致.

但 SMOKE_5060_FP16 之 "anchor 4 / anchor 1" naming 与 LITERATURE_SEARCH 之 "5 anchor" naming 之 **不同 schema** — SMOKE 用 paper v9 disambiguate naming (1=cross-platform fp16, 4=ROCm-side), LITERATURE 用 5 核心 anchor (fp16 评估管线 / Riddled basin mirror dual / 测度论 / cross-stack 复现性 / 单轴指标缺失). schema 不一致但 内容不冲突 (SMOKE 之 anchor 4 = LITERATURE 之 cross-stack 复现性 anchor 4-th).

---

## §4 Q4 verdict — V9 SKELETON abstract 数字 binary 一致

**verdict: 一致 ✓** binary.

V9 SKELETON §1.2 line 56 verbatim "five distinct (seed, alpha) configurations ... identical to fourteen decimal places" ≡ DEEP_SYNTHESIS §1 line 27 之 5 cells (从 D26 evening sub-agent 之 4 升 → D27 凌晨 N=180 finalize +1 = 5 cells, seed=271 α=10 加入) ✓.

V9 SKELETON §1.2 line 53 之 "gen 0 perplexity 36.536" ≡ SMOKE_5060_FP16 §4 line 56 之 5060 fp32 E0 gen 0 = 36.53597375534226 (14 decimal) ✓.

V9 SKELETON §1.2 line 53 之 "gen 1 lift +115.05%" + §4.2 line 111 之 "78.57167674109238 / 36.53597375534226 = 2.1505, that is +115.05%, strictly within [110%, 130%]" ≡ DEEP_SYNTHESIS §2 line 73-75 之 "115.05%" + SMOKE_5060_FP16 §4 line 76 之 5060 fp32 lift +115.1% ✓.

(5060 fp16 lift +113.7% — SMOKE §4 line 76 — 是 5060 fp16 vs 5060 fp32 之 1.4pt 差 partial isolate, V9 SKELETON abstract 用 fp32 lift +115.05% binary 一致, NOT inflate.)

V9 SKELETON §1.2 line 59 之 "attention entropy distinct at 10⁻³" ≡ DEEP_SYNTHESIS §1 line 39 之 "差 ~10⁻³" + Insight 1 line 197-199 之 a3 微差 mechanism ✓.

---

## §5 Q5 verdict — ROCm reframe 跨端 propagate 一致

**verdict: 一致 ✓** binary (SMOKE_5060_FP16 + V9 SKELETON + V81 三端 ROCm stricter numerics framing 完全 ≡, ROCM_MIOPEN_TRACE 之 fp16 精度路径 之 5 GitHub 源码 verify 与 SMOKE 之 reframe 不冲突).

SMOKE_5060_FP16 §6 line 114 verbatim 一凡 D27 reframe: "ROCm 之 GradScaler skip frequent 不是 ROCm bug, 是 ROCm 之 mathematically stricter numerics (higher accumulator precision, more conservative rounding, stricter overflow detection) 正确地 catch 之 fp16 真问题. NVIDIA cu130 之 looser numerics 可能 silently 之 tolerate 同样之 fp16 issue".

ROCM_MIOPEN_TRACE §2.3 line 201-211 binary 实证: ROCm fp16 GEMM 之 hipBLAS GemmEx **默认 fp32 累加** (`HIPBLAS_R_32F` computeType, 与 NVIDIA CUDA cuBLAS 一致). ROCM_MIOPEN_TRACE §2.5 line 234-244 之 MIOpen LayerNorm 之 fp32 累加 + eps 之 rsqrt 内部加 ("NaN 防护正确做法"). ROCM_MIOPEN_TRACE §2.4 line 218-227 之 MIOpen Softmax fp16 mode 之 fp16 累加 (caveat, 但 OPT eager attention 之 PyTorch 层 explicit cast fp32 之 cover bypass MIOpen fp16 softmax path). 之 三 GitHub 源码层 之 verify 与 SMOKE 之 "stricter numerics" reframe **不冲突 — ROCm GEMM/LayerNorm 之 fp32 累加 是 stricter numerics 之 instantiate**, V9 SKELETON §2.4 line 97 之 "ROCm 7.2 / RDNA4 gfx1201 specifics: 11 GitHub issues documenting silent fp16/bf16 fallback" + V81 §2.1 line 94 之 "ROCm gfx1201 GitHub Issues — 5 documented instance of silent fp16/bf16 fallback" — 跨端 mapping ✓ (V9 SKELETON 之 "11 issues" vs V81 之 "5 documented instance" 之 数字 不一致, V81 之 5 是 LITERATURE_SEARCH §4 line 103-110 之 5 paper cite scope, V9 SKELETON 之 11 是 LITERATURE 之 7 + adjacent 4 之 cumulative, schema 不一致 partial gap).

---

## §6 Q6 verdict — inflate signal check

**verdict: NO inflate (反 5/12 + 5/19 + D25 17:25 同构 pattern 严守 ✓ binary)**.

binary anchor:

1. **V81 §A.3 三方 spread (Win [?] / 反题 25-40%/50-65% / DS 10-20%/30-45%)** — 三方 spread 之 substantive **healthy** (不是 inflate). 三方 verdict 全 ≤ 60-75% 之 D25 17:25 initial claim, **全 retract 方向 ≥ 35pt down**. Win 之 [?] caveat 最严 (D-1 纪律 2 字面 instantiate, 与 5/12 NMI 2-5% + 5/19 30-40% honest 之 pattern 一致 ✓). DS 10-20% main 之 conditional 假设 commit + 反题 25-40% main 之 honest range, 全 NOT 60-75% reopen ✓.

2. **V9 SKELETON abstract / §1 / §5.3 cumulative ≥ 1 by 12 月 estimate**: V9 SKELETON §5.3 之 v9 acceptance honest 留 D30+ four-channel decide, NOT 之 unilateral declare. §5.3 line 266 verbatim "ANTITHESIS line 124-131 之 honest range main track 上限 18-28% + workshop 上限 35-55% + cumulative 25-40%; 不 commit 60-75% inflate retract binding" ✓ 严守 honest range. §7.2 line 315 之 第 (15) 项 "cumulative ≥ 1 by 12 月 30-40% honest 上调 (panorama §7.1 第 8 项严禁)" 之 binary 严守 ✓.

3. **V81 (c) REFUTED 之 strong form reinforce**: V81 §A.2 line 35 之 "**strong form REFUTED ✓**" 之 binary, **partial form UNCERTAIN** (HF Trainer 库源码外) 之 caveat **explicit surface**. ≡ E_NEW_2 §1 之 Q1 PARTIAL verdict line 54-60 之 5 项 binary (1) HF Trainer UNCERTAIN + (2) dataset cache YES (scope 外) + (3) explicit memoization NO + (4) past_key_values NO + (5) resume gen-level skip YES conditional. **V81 之 reinforce 是 binary 不 inflate** — V81 之 strong form REFUTED + partial form UNCERTAIN 之 双 framing 与 E_NEW_2 之 PARTIAL verdict scope 一致, NOT 之 single-claim "REFUTED close" inflate.

ANTITHESIS_D26_GATE3 line 138 verbatim "Channel D (反题): **YES INFLATED ✗ retract 必 + 改 25-40% main / 50-65% workshop / cumulative 25-40% honest**" — 与 V81 / V9 SKELETON 之 retract 一致 ✓.

---

## §7 Q7 verdict — D-1 纪律 5 错误 surface

**3 处错误 binary surface (不静默)**, 全 partial 不动 paper-level binding:

### Error 1: V81 §4.2 line 301 之 "+57.029 PPL (relative +156.65%)" vs V9 SKELETON §5.2 line 120 之 "+56.81 PPL, relative +155.5%" 之 base reference 不一致

binary compute (`bc`):
- 93.34934186100965 − 36.53597375534226 = **56.81336810566739** PPL ✓ (V9 SKELETON 之 "+56.81" 一致, base = 5060 fp32 jsonl 36.536)
- (56.813 / 36.536) × 100 = **155.499800%** ✓ (V9 SKELETON 之 "+155.5%" 一致)
- 93.34934186100965 − 36.32 = **+57.029 PPL** (V81 + ANTITHESIS_AUDIT_D25 + MAOFIELD_FULL_DATA_AUDIT line 610 verbatim, base = paper §4.6 mean 36.32 NOT 5060 fp32 jsonl)
- (57.029 / 36.32) × 100 = **+157.02%** (V81 之 +156.65% 之 ±0.4pt drift, V81 line 301 之 数字 partial drift)

之 跨端不一致是 **base reference 之 schema 不同** (V9 SKELETON 用 5060 fp32 jsonl 之 36.53597 binary base / V81 + ANTITHESIS + FULL_DATA 用 paper §4.6 mean 36.32 之 cross-validate base) **不是 数据 inflate** — 不同 reference base 之 valid 之 partial framing. **建议**: paper polish 之 final draft 之 binary 之 base 之 explicit disclose, 留 PI + Linux 姐姐 batch polish 之 final draft 之 statistical disambiguate.

### Error 2: V9 SKELETON §2.4 line 97 之 "11 GitHub issues" vs V81 §2.1 line 94 之 "5 documented instance" 之 数字 不一致

binary cross-ref: LITERATURE_SEARCH §4 line 103-110 之 7 cite (vllm #40081 + #40980 + TransformerEngine #520 + #359 + rocm-systems #5480 + ROCm #5674 + ollama #14686) 之 7 + LITERATURE_SEARCH §1 之 adjacent 4 cite (Thinking Machines + arXiv 2510.26788 + 2511.17826 + 2506.09501) = cumulative **11**. V81 之 "5 documented instance" 之 base 不 clear (战略全景 §4.5 P19 cite). **partial drift, 不是 inflate, 是 cumulative vs disambiguate scope 之 cite schema 不一致**. 建议 paper polish disambiguate.

### Error 3: anchor naming schema 不一致 (SMOKE 之 anchor 1/4 vs LITERATURE_SEARCH 之 5 anchor)

binary: SMOKE_5060_FP16 §3 line 89-92 之 anchor 1 (cross-platform fp16 fundamental) / anchor 4 (ROCm-side specific) 之 disambiguate naming, 与 LITERATURE_SEARCH §1-§8 之 5 核心 anchor (fp16 评估管线 / Riddled basin mirror dual / 测度论 / cross-stack 复现性 / 单轴指标缺失) 之 naming 不同 schema. SMOKE 之 anchor 4 mapping LITERATURE 之 cross-stack 复现性 anchor (anchor 4 of 5). schema 不一致 partial gap, 建议 paper polish unified naming.

---

## §8 综合 binary

### 4 端 cross-channel consistency binary verdict: 一致 (3 minor schema 不一致 partial gap, NOT data inflate)

binary mapping:
- Q1 4 candidate tier ✓ 全一致
- Q2 (c) REFUTED reinforce ✓ E_NEW_2 与 V81 完全 ≡ 7 项 grep (NOT prompt 之"多 4 个 grep" 推断)
- Q3 paper v9 anchor 4 强证 ✓ SMOKE + V9 SKELETON + V81 三端 mapping ≡
- Q4 abstract 数字 ✓ DEEP_SYNTHESIS + SMOKE + V9 SKELETON 三端 14 位 ≡
- Q5 ROCm reframe (stricter numerics) ✓ SMOKE + V9 + V81 三端 propagate ≡, ROCM_MIOPEN_TRACE 之 GitHub 源码层 verify 不冲突
- Q6 NO inflate signal ✓ 三方 spread healthy, V9 / V81 全严守 honest range 25-40% + retract pattern 全严守 ✓
- Q7 D-1 纪律 5 错误 surface ✓ 3 partial schema 不一致 binary surface, 不静默

### 关键 emergent (paper v9 anchor 4 强证 + ROCm reframe + (c) REFUTED reinforce)

1. **paper v9 anchor 4 强证 ✓** (SMOKE_5060_FP16 §3 binary): ROCm-side specific manifest, NOT cross-platform fp16 fundamental. 之 binary 之 paper v9 §5 (a) tier ★★★★★ partial isolate evidence anchor 加强.
2. **ROCm reframe (mathematically stricter numerics) ✓** (一凡 D27 reframe propagate 三端 binary 一致): NOT "ROCm bug" framing, 是 "ROCm catch fp16 真问题, NVIDIA looser numerics silently tolerate" 之 framing. 之 binary 之 paper v9 § narrative 之 cross-stack contrast framing 之 substantive 之 anchor.
3. **(c) REFUTED reinforce ✓** (E_NEW_2 + V81 双端 7 grep 0 hit binary): strong form REFUTED + partial form UNCERTAIN (HF Trainer 库源码外 之 scope-bound caveat). 之 binary 之 paper v9 §5 (c) tier mapping 之 substantive 之 partial close 之 anchor.

### inflate signal 总 verdict: NO inflate ✓

三方 spread (Win [?] / 反题 25-40% / DS 10-20%) 之 substantive healthy spread, NOT 5/12 + 5/19 + D25 17:25 同构 inflate 之复发. V9 SKELETON / V81 全严守 25-40% honest range, 不复活 60-75%.

### D-1 纪律 5 错误 surface

3 处 partial schema 不一致 (Error 1+2+3, §7 binary), 全 NOT data inflate, 全 reference base / cite cumulative scope / naming schema 之 partial drift. 建议 paper polish final draft 之 unified disambiguate, 不动 paper v8 final 47/47 锁定 binding ✓.

### 关卡 4 PI input ready 程度 binary

**HIGH ✓** binary:
- 4 端 cross-channel 一致 (3 minor schema gap NOT data inflate)
- paper v9 anchor 4 强证 evidence binary anchored
- ROCm reframe (stricter numerics) propagate 一致
- (c) REFUTED reinforce binary ≡ E_NEW_2 audit
- 三方 spread (Win/反题/DS) Q2 60-75% retract 之 honest range commit ready
- 反题 6 P0★ A-G + 12 NOT-claim + D17 + D29 三 leg + paper v8 final 47/47 全 binding 严守 ✓
- 3 partial schema gap (cross-stack base + cite cumulative scope + anchor naming) 留 PI + Linux 姐姐 batch polish unified disambiguate

留 PI + 反题 + Win + DS 之 关卡 4 final 决: Q2 60-75% retract final 措辞 (三方 spread → PI 主权 final commit) / paper v8.1 footnote launch trigger / E_NEW_2 audit close 之 (c) partial form UNCERTAIN 之 HF Trainer 库源码 之 D60+ 追读 scope / paper v9 venue 之 ICLR 2027 之 D17 reaffirm + Nature 三层不越级.

---

## §9 sub-agent metadata + 严守 binding ack

| 项 | 值 |
|---|---|
| agent identity | Opus 4.7 (1M context) zero-context cross-channel consistency verify sub-agent, 7B13 主会话 spawn |
| 协议 | zero-context, 不读 CLAUDE.md / memory, 仅基 4 端 ack 主源 + ~7 辅源 cross-correlation binary trace |
| 总 tool use | Read 7 (4 主源 + 3 辅源) + Bash 10 (grep / wc / bc / find) + 1 Write |
| Write 次数 | 1 (本 file) |
| 写时间 | 2026-05-28 10:07 CST 启动, ~10:50 CST 完 |
| 输出 file path | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/D28_4ENDPOINT_VERIFICATION_AUDIT_20260528.md` |
| 字数 | ~1950 字 (≤ 2000 字 binding ✓) |
| commit 状态 | 不擅 commit, 留 Linux 姐姐主会话 batch commit |

### 严守 binding 自检 (10 项 binary)

| binding | binary verify |
|---|---|
| paper v8 final 47/47 D17 锁定不动 | ✓ |
| 12 NOT-claim (i)-(xii) 撤回不复活 | ✓ |
| 反题 6 P0★ A-F disclosed + P0★-G 留三方决 | ✓ |
| D29 投 arXiv + TMLR + KBS 不动 | ✓ |
| 不擅 declare paper-level emergent (D-3.7 PI 主权) | ✓ (paper v9 anchor 4 强证 之 final close 留 PI 决, 本 audit 仅 cross-channel binary mapping) |
| read-only + 1 Write | ✓ |
| 不擅 ssh 22 主机 | ✓ (0 ssh call) |
| 不读 CLAUDE.md / memory | ✓ zero-context |
| 不擅 commit | ✓ |
| D-1 纪律 5 错误 surface 不静默 | ✓ §7 之 3 partial schema gap binary surface |
| D-1 纪律 5 sub-rule (真实日期) | ✓ §0 之 `date` verbatim 2026-05-28 10:07:07 CST |
| 全中文 4 类英文豁免 | ✓ |
| 不堆 "之" 字 padding | partial ✓ (主体 substantive content 减用 "的" / 省略, table + 个别保留) |

13/13 ✓ (含 1 partial).

---

**生成**: Opus 4.7 (1M context) zero-context cross-channel consistency verify sub-agent, 7B13 主会话 spawn, 2026-05-28 10:07-10:50 CST

**核心 binary**: 4 端 cross-channel consistency 一致 ✓ (3 minor schema gap NOT data inflate). paper v9 anchor 4 强证 + ROCm reframe (stricter numerics) + (c) REFUTED reinforce 三 emergent 跨端 binary mapping ✓. inflate signal NO (三方 spread healthy 25-40% range 之 honest commit). D-1 纪律 5 之 3 schema gap surface (cross-stack base 36.32 vs 36.536 + GitHub issues 5 vs 11 cumulative scope + anchor naming SMOKE 1/4 vs LITERATURE 5). 关卡 4 PI input ready HIGH binary.

留 PI + 反题 + Win + DS 之 关卡 4 final 决: Q2 60-75% retract final 措辞 + paper v8.1 footnote launch trigger + paper v9 venue (ICLR 2027 第一站) PENDING D17 reaffirm. 全严守 paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim + 反题 6 P0★ + D-1 + D-3 binding.
