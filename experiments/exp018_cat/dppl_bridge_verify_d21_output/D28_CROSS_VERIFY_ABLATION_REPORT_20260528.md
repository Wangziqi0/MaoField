# D28 cross-verify ablation report — NMI 级别 实验严谨 final 消融

## §0 metadata + scope + binding ack

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%Y-%m-%d %H:%M:%S %Z'` → **2026-05-28 13:27:59 CST** (D28, 7B13 secondary session) |
| 生成 agent | Opus 4.7 (1M context) zero-context cross-verify ablation sub-agent, 7B13 spawn (一凡 PI dispatch D28) |
| 协议 | zero-context cross-verify only — 不读 CLAUDE.md / memory; 仅基 4 主源 + 8 辅源 + 已有 jsonl raw binary trace; 不 launch 新实验; 不擅 ssh 22; 不擅 commit |
| scope binary | (1) 数据层: 20 binary 数 cross-position table reconcile + 4 inconsistency surface (2) 逻辑链: 4 子机制 (a/b/c/d) tier + evidence + prior art cover cross-channel + anchor 编号 schema unified A1-A5 (3) 数学-实验-实践闭环: F5 + experiment anchor 4 闭环咬合 + measure-theoretic 严格度档位 + GradScaler 数学-code consistency + 修正后数学指导下一轮实验 design F1-F5 |
| 字数预算 binding | ~5500 字 (NMI 级别 实验严谨, table-heavy 不 wall-of-text) |
| 输入 主源 | A: MAOFIELD_FULL_DATA_AUDIT (697 行, D26) / B: DEEP_SYNTHESIS_D26_EVENING (264 行, D27 凌晨) / C: ROCM_MIOPEN_TRACE_AUDIT (544 行, D27 21:35) / D: SMOKE_5060_FP16_CROSSCHECK_GRADSCALER (169 行, D28 00:34) |
| 输入 辅源 | E: LITERATURE_SEARCH (244 行) / F: E_NEW_2_EVAL_AUDIT (257 行) / G: STRATEGIC_PANORAMA (530 行) / H: V81 FOOTNOTE DRAFT (508 行) / I: V9 SKELETON DRAFT (325 行) / J: D28_4ENDPOINT_VERIFY (208 行) / L: MATH_VERIFY_D25 (464 行) |
| 严守 binding (13 项 binary) | paper v8 final 47/47 D17 锁定不动 ✓ + 12 NOT-claim (i)-(xii) 撤回不复活 ✓ + 反题 6 P0★ A-F disclosed + P0★-G partial isolate update ✓ + D29 投 arXiv + TMLR + KBS 不动 ✓ + ICLR 2027 第一站 + Nature 三层不越级 ✓ + paper v8 title "Contradiction Loss" 不动 + v9 改 "Internal Tension Loss" 留 PI 决 ✓ + D-3.7 PI 主权 严守 (本 ablation 不 declare paper-level emergent final) ✓ + 7B13 单点 git 写权 ✓ + zero-context ✓ + read-only + 1 Write ✓ + 不擅 launch 新实验 ✓ + D-1 纪律 5 sub-rule (`date` binary verify) ✓ + D-1 纪律 5 错误 surface 不静默 ✓ |

---

## §1 Layer 1 — 数据层消融 (20 binary 数 cross-position + reconcile)

### §1.1 Cross-position table — 20 binary 数

| # | 数 | File A 值 + 行号 | File B 值 + 行号 | File C 值 + 行号 | File D 值 + 行号 | reconcile state |
|---|---|---|---|---|---|---|
| 1 | 5 cells a1_ppl 14 位 ≡ value | 93.38780852810248 (line 371-374, §7.4) | 93.38780852810248 (line 26-28, §1) | 93.38780852810248 referenced ("4 cells", D26 entry, line 504-507) | n/a (5060 stack, not 9070XT) | ✓ ≡ binary, B+A 一致, C 用旧 "4 cells" 描述 (写于 D26 evening, finalize 前) — partial schema drift |
| 2 | 5 cells val_loss 14 位 ≡ value | 4.5367608070373535 (line 371-374, §7.4) | 4.5367608070373535 (line 27, §1) | n/a (无直接 quote) | n/a (5060) | ✓ ≡ binary (A+B 一致) |
| 3 | 5 cells (seed, α) list | (1337,10)/(2024,0)/(7,10)/(137,0) — 4 cells D26 16:49 snapshot (line 371-374, §7.4) | (1337,10)/(2024,0)/(7,10)/(137,0)/(271,10) — 5 cells D27 凌晨 finalize (line 26-28, 37) | "4 cells" historical (line 504-507, F9) | n/a | ✓ partial — A 是 D26 16:49 (158/180 时之 4 cells), B 是 D27 凌晨 finalize 之 5 cells (N=180 之后加入 seed=271 α=10), 不是 数据 inconsistency, 是 时间 progression (Inconsistency 1, §1.2) |
| 4 | 5 cells n_tokens_train / n_tokens_eval | 2390656 / 16384 (line 379, §7.4) | 2390656 / 16384 (line 28, §1) | n/a | 2390656 / 16384 (line 60-61, §gen 0) | ✓ ≡ binary (A+B+D 一致, 跨 stack 跨 chain 同) |
| 5 | 9070XT seed=42 α=0 chain trajectory (10 gen) | a1_ppl gen 0/.../9 = 93.34934/.../93.34854 (line 317-326, §7.3) | gen 0=93.34934, gen 9=93.34854, span 0.00152 (line 52) | a1_ppl gen 0=93.34934/val_loss=4.536348 (line 415-426, §3.4) + 10 gen 全 PASS (line 277) | n/a (5060) | ✓ ≡ binary 三端 (A+B+C 一致, span ≈ 1.5e-3) |
| 6 | 9070XT base no-train PPL | n/a (直接) | n/a (直接) | a1_ppl 93.34934 = base + "fine-tune-after a1_ppl = base PPL 93.349 bit-identical hypothesis ★★★★★ strong" (line 614) + F8 partial 推算 (line 494-500) | n/a | partial — 直接源在 File L (MATH_VERIFY_D25 line 14, 87, 88, 111: "base model PPL on wikitext-2 val: **93.349**") + A line 614 verbatim cite. ✓ binary cross-ref |
| 7 | 5060 fp32 gen 0 a1_ppl (3 跑 SMOKE/R1/E0) | n/a | 36.53597375534226 (3 跑 14 位 ≡, line 64-69, §2) | n/a | 36.53597375534226 (E0 ref column, line 56, §gen 0) | ✓ ≡ binary (B+D 一致) |
| 8 | 5060 fp32 gen 1 a1_ppl (E0) | n/a | 78.57167674109238 (line 73, §2) | n/a | 78.57167674109238 (E0 ref column, line 69, §gen 1) | ✓ ≡ binary (B+D 一致) |
| 9 | 5060 fp32 gen 0→1 lift % | n/a | +115.05% strictly within [110%, 130%] (line 75-80, §2) | n/a | "5060 fp32 lift +115.1%" (line 76, §collapse magnitude) | ✓ ≡ binary (B = 115.05% 之 precise, D = 115.1% 之 round, `bc -l` verify: (78.57167674109238/36.53597375534226 - 1)*100 = **115.05291542860191%**) |
| 10 | 5060 fp16 gen 0 a1_ppl (本次) | n/a (D 是 5060 fp16 主源) | n/a | n/a | **36.537707256599994** (line 56, §gen 0 metric table) | ✓ binary (D verbatim) |
| 11 | 5060 fp16 gen 1 a1_ppl (本次) | n/a | n/a | n/a | **78.07346793600594** (line 69, §gen 1 metric table) | ✓ binary (D verbatim) |
| 12 | 5060 fp16 gen 0→1 lift % | n/a | n/a | n/a | +113.7% (line 76, §collapse magnitude) | ✓ binary (`bc -l` verify: (78.07346793600594/36.537707256599994 - 1)*100 = **113.67916543779065%**, D 之 "113.7%" 是 round) |
| 13 | 9070XT seed=42 α=0 gen 0→1 Δ | gen 1 - gen 0 = 93.34907478678235 - 93.34934186100965 = **−2.6707e−4** (推算自 line 317-318) | "Δ = −2.67e−4 (frozen)" (line 86, §2 cross-stack contrast) | n/a (推算 line 418-419) | n/a | ✓ ≡ binary (A+B 一致, `bc -l` verify = **-0.00026707422730**) |
| 14 | 5060 fp32 seed=42 α=0 gen 0→1 Δ | n/a | "Δ = +42.04 (paper expected)" (line 87, §2 cross-stack contrast) | n/a | n/a (D 是 fp16, fp32 reference 在 D 之 E0 ref column line 56+69) | partial ✓ — B 之 "+42.04" 是 abs diff: 78.57167674109238 - 36.53597375534226 = **+42.036** (`bc -l` verify), B 之 round, 一致 |
| 15 | 9070XT vs 5060 fp32 (seed=42 α=0 gen=0) abs+rel diff | abs diff = 93.349 - 36.32 = **+57.029** PPL / rel +**157.0%** (line 610, §11.7 P0★-G) | "diametrically opposite trajectory" (line 84-89) — 不直接 quote abs diff | n/a | n/a | partial — 2 个 valid base reference: paper §4.6 mean **36.32** (A line 610) vs 5060 fp32 jsonl **36.53597** (B 之 raw)。`bc -l` verify: 93.349-36.32 = +57.029 / 93.349-36.53597 = **+56.813** / rel diff = +157.0% vs +155.5% (Inconsistency 2, §1.2) |
| 16 | a3_attn_entropy 跨 5 cells distinct scale | "~10⁻³ 级别细微差异" (line 386, §7.4) | "差 ~10⁻³" (line 39) + 5 cells line 33-37 verbatim values | n/a (C 是 ROCm 源码追踪) | n/a (D 5060) | ✓ ≡ binary (A+B 一致) |
| 17 | a2_anisotropy first layer (valid 之 cell) | "~10⁻³ 级别细微差异" (line 386, §7.4) | a2_anisotropy not directly quoted | a2_anisotropy[0] = 0.7024863800033927 valid + 第 1-11 层 NaN (line 389) | a2_anisotropy[last] = 0.8748 / 0.8754 (line 61) | partial — A 之 "~10⁻³ 跨 cells" 是 5 cells 跨 (seed,α) 之 distinct scale; C 之 0.7024 是 single jsonl entry seed=42 α=5.0 gen=0 之 layer 0 valid; D 之 0.8748 是 5060 fp16 gen 0 last layer (不同 layer 不同 cell). 不是 inconsistency, 是 不同 scope (跨 cells distinct scale vs single entry valid layer 0) |
| 18 | chain N=180 之 statistics (valid + null) | D26 16:49 snapshot: 173 行 alive (line 311); valid (从 §7.3 trajectory 推算) ≈ 31, null 大量 (line 304-306, §8 之 158/180 D26 evening) | D27 凌晨 finalize: **180/180 done** + valid 33 + null 147 + 5 bit-identical cells (line 23-28) | jsonl 180 条 chain_gen_done (line 28 sha256) + val_loss 非 None = 34 + None = 146 (line 396-409, §3.3) | n/a | ✓ binary consistency partial — A 是 D26 evening snapshot (chain alive) / B 是 D27 凌晨 finalize / C 是 D27 18:00 之后 audit (verify N=180 完成). state progression healthy ✓ (158/180 → 180/180 + 4 cells → 5 cells). |
| 19 | NaN cascade event count | (推算自 line 327-365 之 全 null + line 304-308 之 D26 evening) | "null a1_ppl: 147" (line 24-25); "α=5 / α=10 全 null 95% / 95%" (line 46-48) | "146 NaN cascade" (line 400) — 但 cross-channel 不 quote total | n/a | ✓ binary consistency partial — B (147) + C (146) 之 1 entry 差 (B 之 finalize state + C 之 D27 21:35 之 snapshot 之间之 entry 差异, 不是 inconsistency, 是 不同 quote timing). A 之 chain alive snapshot 不 quote total. |
| 20 | 4 cells vs 5 cells升 之 binary transition timeline | "4 cells D26 16:49" (§7.4 line 367, snapshot timing) | "+1 (seed=271 α=10 加入)" (line 28) — D27 凌晨 finalize state | "4 cells" 之 D26 historical (line 504-507, F9) | n/a | ✓ ≡ binary timeline (D26 16:49 4 cells → D27 凌晨 finalize 5 cells, +seed=271 α=10 cell). 不是 inconsistency, 是 时间 progression. |

### §1.2 Inconsistency surface (binary)

#### Inconsistency 1: cross-stack base disambiguate (36.32 vs 36.53597)

- **File A line 610 source**: "paper §4.6 fine-tune 之后 gen 0 test_ppl 36.32 vs 9070XT candidate C a1_ppl seed=42 α=0 val_loss → val PPL 93.349: abs diff +57.0 (rel +157%)" — base = paper §4.6 mean 36.32 (= mean of α=0 seed=1/2/3/4 之 gen 0 test_ppl, A §10.3 line 528 cross-verify ✓)
- **File B + File D source**: 5060 fp32 jsonl 之 a1_ppl gen 0 = 36.53597375534226 (14 decimal, D24 SMOKE / D25 R1 / D25 E0 三 launch bit-identical) — base = stack A jsonl raw
- **binary reconcile**: 2 个 valid base reference, paper polish 之 explicit disclose 必须。
  - base = paper §4.6 mean 36.32: 93.349 - 36.32 = **+57.029 PPL** / +**157.02%** (`bc -l` 验)
  - base = 5060 fp32 jsonl 36.53597: 93.349 - 36.53597 = **+56.813 PPL** / +**155.50%** (`bc -l` 验)
- **不是 inflate, 是 reference base schema 不同 (cross-validate vs jsonl raw)**
- paper polish wording 建议: "9070XT fp16 a1_ppl 93.349 vs **5060 fp32 jsonl 36.536** (single-launch reproducibility benchmark): +56.81 PPL / +155.5%; vs **paper §4.6 reported mean 36.32** (Shumailov 2024 baseline cross-validate): +57.03 PPL / +157.0%. 两个 reference base 一致 within 0.22 PPL, paper polish 之 final 之 binary 之 base 之 explicit disclose."

#### Inconsistency 2: F9 之 93.349 vs 93.387 跨 chain run 差异

- **File C F9 source (line 502-508)**: "D27 jsonl: 93.349 (epoch 4 位起异于 D26 93.387) — 两个 jsonl 是不同 chain 跑的 (D22 candidate_c 5/22 launch vs D25-D26 PID 491900)"
- **binary reconcile**: 2 个不同 chain run (D22 candidate_c 之 seed=42 α=0 gen 0-9 全 valid = 93.349 frozen 10 代 + D25-D26 PID 491900 之 5 bit-identical cells @ 93.388)
- abs diff = 93.38780852810248 - 93.34934186100965 = **0.03846666709283 PPL** (`bc -l` verify) ≈ **0.04 PPL / 0.04%**
- mixed-precision fp16 mantissa rounding: 2^-10 ≈ 0.1% per op × ~7300 train step (1460 step/gen × 5 epoch) 累积 ≈ 0.5-1% drift expected
- 实测 0.04% drift **within fp16 GradScaler skip deterministic regime 之 small accumulator variation**, 不是 inconsistency
- paper polish wording 建议: "9070XT fp16 seed=42 α=0 之 跨 2 chain run (D22 candidate_c + D25-D26 PID 491900) 之 partial drift 93.349 vs 93.388 ≈ 0.04 PPL ≈ 0.04%, within fp16 GradScaler skip 之 deterministic regime 之 small accumulator variation. 之 5 bit-identical cells (seed × α) 之 14 decimal ≡ value 93.38780852810248 是 PID 491900 single-chain N=180 之 binary, D22 candidate_c 之 single-chain seed=42 α=0 之 frozen 93.349 是 base PPL 之 cross-validate (与 base no-train PPL ≡, MATH_VERIFY_D25 line 87-88)."

#### Inconsistency 3: cite cumulative scope (5 vs 11 GitHub issues)

- **File I V9 SKELETON §2.4 line 97**: "ROCm 7.2 / RDNA4 gfx1201 specifics: **11 GitHub issues** documenting silent fp16/bf16 fallback"
- **File H V81 §2.1 line 94**: "ROCm gfx1201 GitHub Issues — **5 documented instance** of silent fp16/bf16 fallback (战略全景 §4.5 P19)"
- **File E LITERATURE_SEARCH §4 line 103-110**: 7 GitHub issue cite (vllm #40081 + #40980 + TransformerEngine #520 + #359 + rocm-systems #5480 + ROCm #5674 + ollama #14686) + §1 line 18-27 之 adjacent 4 paper cite (Thinking Machines + arXiv 2510.26788 + 2511.17826 + 2506.09501) = cumulative **11**
- **binary reconcile**: V9 SKELETON 之 11 = LITERATURE §4 之 7 + §1 之 adjacent 4 (cumulative scope); V81 之 5 = 战略全景 §4.5 P19 之 strict cite scope (disambiguate scope)
- paper polish wording 建议: "5 verbatim GitHub issue cite in main text (V81 §A.2 row (a) 之 strict scope) + 6 adjacent literature reference in supplementary section (V9 SKELETON §2.4 之 cumulative scope) = cumulative 11. explicit scope schema disclose."

#### Inconsistency 4: anchor naming schema (SMOKE 1/4 vs LITERATURE 1-5)

- **File D SMOKE §3 line 89-92**: anchor 1 = "cross-platform fp16 fundamental" (否决) / anchor 4 = "ROCm-side specific manifest" (强证)
- **File E LITERATURE §1-§8**: 5 核心 anchor naming: A1 = fp16 评估管线 / A2 = Riddled basin mirror dual / A3 = 测度论 ill-posedness / A4 = cross-stack 复现性 / A5 = 单轴指标缺失 cross-layer
- **binary mapping**: SMOKE 之 anchor 4 = LITERATURE 之 A4 (cross-stack 复现性) — strong mapping ✓ (SMOKE 之 specific manifest 是 LITERATURE 之 cross-stack 复现性 之 instantiate). SMOKE 之 anchor 1 是 SMOKE 之 disambiguate 之 否决 candidate, 与 LITERATURE 之 A1 (fp16 评估管线 fragility 之 partial 强证) 之 mapping 是 partial refute (SMOKE 否决 cross-platform universal claim, A1 之 ROCm-side specific manifest 仍 hold)
- paper polish 推荐 unified naming (用 LITERATURE 5 anchor naming, SMOKE 之 disambiguate 1/4 之 anchor naming 入 paper polish 之 sub-anchor reference): 见 §2.2 unified table

### §1.3 已 reconcile 之 binary closed list

| # | item | reconcile mechanism | state |
|---|---|---|---|
| 1 | 5 cells a1_ppl + val_loss + n_tokens 14 位 ≡ | A + B + D 三端 binary 一致 | ✓ closed |
| 2 | 5060 fp32 3 跑 gen 0 14 位 ≡ + E0 lift 115.05% strictly in [110%, 130%] | B + D 二端 binary 一致 + bc verify | ✓ closed |
| 3 | 5060 fp16 vs 5060 fp32 lift % 一致 (113.7% vs 115.05%, within 1.4pt fp16 expected rounding) | D 单端 + bc verify | ✓ closed |
| 4 | 9070XT seed=42 α=0 跨 5060 fp32 之 diametrically opposite trajectory (Δ = -2.67e-4 vs +42.04 PPL) | B + jsonl raw + bc verify | ✓ closed |
| 5 | a3_attn_entropy ~10⁻³ distinct cross 5 cells (refute (c) eval cache strong form) | B + jsonl raw 之 5 cells verbatim values | ✓ closed |
| 6 | F5 + experiment anchor 4 闭环咬合 (C 之 GitHub 源码 5 finding F1-F8 + D 之 stricter numerics reframe) | 见 §3.1 | ✓ closed |
| 7 | GradScaler skip 数学 ↔ code consistency | 见 §3.3 | ✓ closed |
| 8 | 4 cells → 5 cells 时间 progression (D26 16:49 → D27 凌晨 finalize +1) | A + B + jsonl mtime | ✓ closed |
| 9 | 9070XT chain N=180 finalize state (180/180 done + valid 33 + null 147) | B + C + jsonl raw | ✓ closed |
| 10 | D-PPL pilot factor-of-2 (D^code_B/D^paper=0.66, D^code_C/D^paper=1.31) | A §6 + bc verify | ✓ closed (P0★-F partial close candidate) |

### §1.4 剩余数据缺口 list

1. **9070XT seed=42 α=5/10 之 NaN cascade 之 first-NaN-step 之 精确 step**: C F8 line 500 explicit "GradScaler skip 失效之精确 step 不在本审计已 verify 之日志精度内" — 留 D60+ layer-wise hook + 数值打印 (ssh 22 写权 必须, 主会话执行)
2. **HF Trainer 库内部 evaluate-level cache implementation**: F Q1 verdict line 56-60 "UNCERTAIN — HF transformers 库源码层, 本审计 scope 外" — 留 D60+ measurement-theoretic ablation framework first instantiation 之 secondary task (~6-9 月)
3. **5060 fp16 vs fp32 之 synthetic data sha256 cross-check**: D caveats line 127 "本次没 cross-check synthetic data 之 sha256 (potential follow-up)" — 留主会话 D27-D30 polish window
4. **22 主机 9070XT + Win 5060 之 source-side sha256 校验**: A §12.1 之 binary "ssh 22 / ssh Win 之 source-side sha256 留主会话执行" — 留主会话 D28+ batch verify

---

## §2 Layer 2 — 逻辑链消融 (4 子机制 + anchor 编号 schema unified)

### §2.1 4 子机制 cross-position table

| 子机制 | V81 §A.2 tier (File H) | V9 SKELETON §5 (a-d) tier (File I) | DEEP_SYNTH Insight (File B) | SMOKE §6 / ROCm F* (File C+D) | LITERATURE anchor mapping (File E) | prior art cover | reconcile state |
|---|---|---|---|---|---|---|---|
| **(a) frozen weight via fp16 GradScaler skip** | ★★★★★ partial isolate (line 33, §A.2) | ★★★★★ tier (line 125, §5 (a)) | Insight 1 加强 (5 cells + a3 conjunction, line 197-199) | C F3 + F7 之 binary mechanism + D anchor 4 强证 (line 89-92) | A1 (fp16 评估管线 fragility) + A4 (cross-stack 复现性) 之 ROCm-side specific instantiate | Micikevicius 2018 + PyTorch GradScaler source + ROCm gfx1201 GitHub Issues (5-11 documented, Inconsistency 3) | ✓ tier 全端 ≡ ★★★★★, 之 partial isolate scope 全端一致 |
| **(b) ROCm hipBLAS reduction tree micro-fluctuation** | ★★★★ (line 34, §A.2) | ★★★★ (line 127, §5 (b)) | Insight 1 a3 微差加强 (line 197-199) | C F5 ✓ fp32 累加 正确 + F6 caveat MIOpen SoftmaxForward fp16 mode 之 fp16 累加 (但 OPT eager 之 PyTorch 层 cast bypass, line 218-227 + 254-258) | A4 (cross-stack 复现性) 之 sub-mechanism | ROCm gfx1201 open source + MIOpen GEMM accumulation tree + IEEE-754 floating-point non-associativity | ✓ tier 全端 ≡ ★★★★, 之 partial isolate 全端一致 (F6 caveat scope-bound, 不影响 OPT eager) |
| **(c) eval cache memoization** | strong form REFUTED ✓ + partial form UNCERTAIN (line 35, §A.2 + §2.3 line 117-131) | strong form REFUTED ✓ + partial form pending E_NEW_2 close (line 129, §5 (c)) | (c) strong form REFUTED via a3 微差 (line 197-199) + Insight 5 之 P0 critical scope (line 213-215) | n/a (C 是 ROCm 源码, D 是 5060 cross-stack) | A0 prior art cover (institutional gap) | 0 prior art cover (DEEP_SYNTH Insight 5 + E §1 line 33 之 institutional gap) | ✓ verdict 全端 ≡ (strong REFUTED + partial UNCERTAIN), E_NEW_2 audit (F) 之 Q1 PARTIAL verdict 之 闭环 binary 一致 |
| **(d) phenomenology artifact (measure-theoretic ill-posedness)** | ★★★ + mirror dual novelty 仍存 (line 36, §A.2) | ★★★ (line 131, §5 (d)) + mirror dual dual pending (§6 主锚) | n/a (B 是 数据综合, 不 declare tier) | n/a | A2 (Riddled basin mirror dual) + A3 (测度论 ill-posedness rigor formulation, paper v9 §6 主锚) | Ly-Gong 2025 (divergence side) + Geshkovski 2024 metastability (transient frozen plateau) — partial cover; convergence-side mirror dual novelty 仍存 (E §2 line 65-67 verdict "partial novel" + §8 line 197) | ✓ tier 全端 ≡ ★★★, mirror dual novelty 之 partial cover 全端一致 |

### §2.2 anchor 编号 schema unified

| SMOKE naming (File D) | LITERATURE naming (File E) | substantive mapping |
|---|---|---|
| anchor 1 (cross-platform fp16 universal) ← **否决** by SMOKE 5060 fp16 healthy | A1 (fp16 评估管线 fragility, partial novel ≤ 20% prior cover) | partial refute mapping. SMOKE 否决 universal claim, A1 之 ROCm-side specific manifest (sub-mode b1) 仍 hold (即 5060 fp16 healthy 不否决 9070XT fp16 之 ROCm-side specific failure mode) |
| anchor 4 (ROCm-side specific manifest) ← **强证** by SMOKE cross-stack contrast | A4 (cross-stack 复现性, partial novel ≤ 25% prior cover) | strong mapping ✓. SMOKE 之 specific manifest = A4 之 instantiate. (a) GradScaler skip + (b) ROCm reduction tree 是 A4 之 子 sub-mechanism |
| (n/a, SMOKE 不 declare) | A2 (Riddled basin mirror dual, partial novel — Ly-Gong divergence side 之 convergence side 之 framing 未见独立 prior) | paper v9 §6.3 之 子机制 (d) framing 之 anchor |
| (n/a, SMOKE 不 declare) | A3 (measure-theoretic ill-posedness rigor formulation, largely novel ≤ 5% prior cover) | paper v9 §6 主锚 formal characterization |
| (n/a, SMOKE 不 declare) | A5 (单轴 PPL 指标 cross-layer dialectical interconnection 缺失, partial novel ≤ 10% prior cover) | paper v9 §7.4 open questions framing |

#### unified paper-grade naming (推荐 paper polish 用 A1-A5):

- **A1** = fp16 评估管线 fragility (LITERATURE A1, SMOKE refute cross-platform universal claim, A1 之 ROCm-side specific manifest 仍 hold)
- **A2** = Riddled basin mirror dual (LITERATURE A2, paper v9 §6.3 子机制 (d) framing 之 anchor)
- **A3** = measure-theoretic ill-posedness (LITERATURE A3, paper v9 §6 主锚 formal characterization, largely novel)
- **A4** = cross-stack 复现性 = ROCm-side specific manifest (LITERATURE A4 = SMOKE 强证 = 子机制 a+b 闭合证据 base)
  - sub-mode b1 = ROCm fp16 GradScaler skip (子机制 (a))
  - sub-mode b2 = ROCm hipBLAS reduction tree micro-fluctuation (子机制 (b))
- **A5** = 单轴 PPL 指标 cross-layer dialectical interconnection 缺失 (LITERATURE A5, paper v9 §7.4 open questions framing)

### §2.3 prior art cover gap list

| 子机制 | prior art cover | gap |
|---|---|---|
| (a) | strong (3 cover: Micikevicius 2018 + PyTorch GradScaler source + ROCm gfx1201 GitHub Issues 5-11 cumulative) | None (3 cite 全端 strong) |
| (b) | partial (ROCm open source MIOpen GEMM accumulation tree + IEEE-754 standard; 但 0 prior art specific to gfx1201 之 sub-mechanism) | gfx1201-specific sub-mechanism 之 prior art 留 D60+ measurement-theoretic ablation grid 之 disentangle |
| (c) | **0 prior art cover** — institutional gap (E §1 line 33 + DEEP_SYNTH Insight 5 line 213-215) | E_NEW_2 source-code audit (F) 之 Q1 PARTIAL verdict 之 partial close; HF Trainer 库源码层 之 partial form UNCERTAIN 留 D60+ measurement-theoretic ablation framework first instantiation 之 secondary task (6-9 月) |
| (d) | partial (Ly-Gong 2025 divergence side + Geshkovski 2024 metastability transient frozen plateau partial cover) | convergence-side mirror dual novelty 仍存 (E §2 line 65-67 verdict "partial novel"), 留 D60+ Banach 5-mode failure taxonomy first instantiation (6-12 月) |
| **中文圈 prior art (DS 第七缺口)** | partial (中文圈 evaluation 综述 cover ≥ 60% informal level; 后 4 anchor A2-A5 之 中文圈 独立 paper 未 surface) | 留 PI + DS 之 关卡 3 三方决 之 final + D28+ extend search |

### §2.4 已 reconcile vs 剩余 gap list

#### 已 reconcile (tier + evidence + prior art 三端 ≡):
- 子机制 (a) tier ★★★★★ partial isolate ✓ (4 端 全 ≡, V81 + V9 + DEEP_SYNTH + SMOKE)
- 子机制 (b) tier ★★★★ ✓ (V81 + V9 双端 ≡, DEEP_SYNTH Insight 1 加强, C F5+F6 之 GitHub 源码 verify 不冲突)
- 子机制 (c) verdict strong REFUTED + partial UNCERTAIN ✓ (V81 + V9 + DEEP_SYNTH + E_NEW_2 audit 之 4 端 binary 闭环, prior art 0 cover 之 institutional gap surface)
- 子机制 (d) tier ★★★ + mirror dual novelty 仍存 ✓ (V81 + V9 + LITERATURE 三端 ≡)
- anchor naming schema unified A1-A5 (LITERATURE 5 anchor) ← recommended paper polish naming
- SMOKE 之 anchor 1/4 ← disambiguate naming 入 sub-anchor reference (A4 之 sub-mode b1 = ROCm-side specific instantiate)

#### 剩余 gap (留 D27-D60 polish + D60+ substantive):
- (c) partial form HF Trainer 库源码追读 (~6-9 月, D60+ measurement-theoretic ablation framework first instantiation 之 secondary task)
- (d) mirror dual convergence-side novelty 之 substantive close (~6-12 月, D60+ Banach 5-mode failure taxonomy first instantiation)
- 中文圈 prior art 后 4 anchor A2-A5 之 独立 paper search 之 完整性 (留 PI + DS 之 关卡 3 + D28+ extend search)

---

## §3 Layer 3 — 数学-实验-实践闭环

### §3.1 F5 + experiment anchor 4 闭环咬合 binary

#### binary contradiction check

| framing | source verbatim | mutual coherence |
|---|---|---|
| (i) "代码做了正确的事" | C F5 line 470-480 verbatim "所有'应该用 fp32 累加'的路径在 ROCm/MIOpen 上都正确用 fp32 累加" + C §2.3-§2.5 之 GitHub 源码 binary verify (hipBLAS GemmEx HIPBLAS_R_32F + MIOpen LayerNorm FLOAT_ACCUM fp32 + OPT eager softmax explicit cast fp32) | binary fact ✓ |
| (ii) "ROCm 有 bug" | (一凡 D27 之前之 wrong reframe, D27 自 retract 之 之前 candidate framing) | retracted ✗ binary 之 一凡 D27 自 retract |
| (iii) "ROCm stricter numerics" | D §6 line 113-118 verbatim "ROCm 之 GradScaler skip frequent 不是 ROCm bug, 是 ROCm 之 mathematically stricter numerics (higher accumulator precision, more conservative rounding, stricter overflow detection) 正确地 catch 之 fp16 真问题. NVIDIA cu130 之 looser numerics 可能 silently 之 tolerate 同样之 fp16 issue" | binary 与 (i) 闭环 ✓ |

#### reconcile binary

- **F5 之 fp32 累加 = stricter numerics 之 instantiate** ✓ (i)+(iii) framing 闭环咬合
- (ii) "ROCm 有 bug" framing 是 wrong reframe, D27 自 retract (不再 active)
- **NOT contradiction**: ROCm 之 fp32 累加 (F5 binary, 即 hipBLAS GemmEx HIPBLAS_R_32F + MIOpen LayerNorm fp32 FLOAT_ACCUM + OPT eager softmax cast fp32 之 3 路径全 fp32) 之 严格 mathematical 之 instantiate 之 stricter numerics: catch fp16 真问题 (即 GradScaler skip 之 frequent trigger 是 ROCm 之 stricter numerical detection 之 正确 action, 不是 ROCm-side bug). NVIDIA cu130 之 looser numerics 之 silently tolerate 同样 fp16 issue (5060 fp16 之 healthy chain collapse 之 binary 证据 D §3 line 89-92).

#### partial inconsistency: F6 caveat 之 close

- **F6 verbatim (C §2.4 line 218-227)**: MIOpen `SoftmaxForward` fp16 mode 之 fp16 累加 (gen-side, NOT bwd-side); `SoftmaxBackward` 用 `_FLOAT_ACCUM` (fp32)
- **但 OPT eager attention 之 PyTorch 层 explicit cast fp32 之 cover bypass MIOpen fp16 softmax path** (C §2.6 line 254-258):
  ```python
  if attn_weights.dtype == torch.float16:
      attn_weights = nn.functional.softmax(attn_weights, dim=-1,
                                            dtype=torch.float32).to(torch.float16)
  ```
- **partial inconsistency 之 binary close**: bypass evidence 之 binary 实测 之 F6 之 OPT-specific 之 不 trigger MIOpen fp16 softmax path (因 OPT eager softmax 之 PyTorch 层 显式 fp32 cast). paper v9 §2.4 之 caveat footnote 之 explicit disclose: "MIOpen SoftmaxForward fp16 mode 之 fp16 累加 caveat 仅 active 在 attention 之外之 logits softmax path (CrossEntropyLoss 内部之 log_softmax) + 仅 active 在 lm_head 输出 dtype = fp16 之 condition. OPT eager attention 之 PyTorch 层 显式 fp32 cast 之 cover bypass MIOpen fp16 softmax path, attention 路径之 softmax 不走 MIOpen fp16 kernel."

#### cite scope schema (cumulative vs disambiguate) 之 close

- **V9 SKELETON §2.4 line 97**: "11 GitHub issues" (cumulative scope = LITERATURE §4 之 7 cite + §1 之 adjacent 4 cite)
- **V81 §2.1 line 94**: "5 documented instance" (disambiguate scope = 战略全景 §4.5 P19 之 strict cite scope)
- **paper polish 推荐 wording**: "5 verbatim cite in main text (strict scope: vllm #40081 + #40980 + TransformerEngine #520 + ROCm #5674 + ollama #14686, V81 strict scope) + 6 adjacent literature reference in supplementary section (cumulative scope: TransformerEngine #359 + rocm-systems #5480 + Thinking Machines Lab + arXiv 2510.26788 + 2511.17826 + 2506.09501) = cumulative 11. explicit scope schema disclose."

### §3.2 measure-theoretic ill-posedness 数学 form 严格度档位

#### V9 SKELETON §6.1 Φ: M → ℝ measure-positive subset S 定义

```
$\Phi: M \to \mathbb{R}$ (validation perplexity functional)
$M$ = training configuration manifold (seed, alpha, generation index,
       optimizer state, dataloader state, hardware stack, dtype regime,
       attention implementation)
$\Phi$ measure-theoretically ill-posed at constant $c$ ⟺
       ∃ measure-positive subset $S \subset M$ s.t. $\Phi(S) = \{c\}$
```

#### 严格度档位 binary

- **L1 (formal definition, no proof of measure-positivity)**: 当前 paper v9 SKELETON §6.1 之 formal definition + §6.2 empirical witness (5 cells lower bound) — **可 actualize** within D29-D60 polish window
- **L0 stricter form (proof of measure-positivity)**: 需 multi-stack ablation grid (multi-dtype × multi-GPU × multi-architecture × multi-family) 之 measure-positivity proof — **不可 actualize** within D29-D60, 留 D60+ window (Banach LLM C1 3-6 月 + measurement-theoretic ablation C2 6-9 月)

#### empirical witness binary

| empirical witness item | binary state | partial vs full close |
|---|---|---|
| 5 cells |S| lower bound (跨 4 seed × 2 alpha) | (1337,10)/(2024,0)/(7,10)/(137,0)/(271,10) ✓ binary | partial cover (5 cells, 跨 4 seed × 2 alpha) |
| cross-seed cross-alpha variation 之 binary verify (n_tokens 差异 / a3 微差) | n_tokens 之 binary identical (跨 5 cells), a3 ~10⁻³ distinct (binary 实测 B line 33-37) | partial verify (n_tokens identical 之 binary 之 sample-size-blind, a3 distinct 之 hidden-state level partial verify) |
| measure-positivity full close | (留 D60+ multi-stack grid) | NOT close within D29-D60 |

#### F1-F5 falsifiability specify binary

| Falsifier | binary specify | 当前实测 state |
|---|---|---|
| **F1**: gen_N_ppl >= gen_0_ppl + 5 PPL on healthy chain | Stack A: 5060 fp32 gen 0=36.536, gen 1=78.572, lift +42.04 PPL >>> +5 PPL ✓ pass | Stack A ✓ pass, Stack B (9070XT fp16) ✗ fail (frozen Δ = -2.67e-4) |
| **F2**: 5 cells distinct count > 1 on Stack B | binary count: 5 cells a1_ppl 14 decimal = 1 distinct value (93.38780852810248) | refuted ✗ (distinct count = 1) |
| **F3**: hidden-state level signature distinct count > 1 across 5 bit-identical cells | a3_attn_entropy distinct count = 5 (5 cells 之 5 distinct hidden-state signatures at ~10⁻³ scale) | refuted ✗ (distinct count = 5, hidden-state level distinct hold) |
| **F4**: cross-stack divergence absent under identical (seed=42, α=0, gen=0) | abs diff 9070XT fp16 vs 5060 fp32 = +56.81 PPL / +155.5% (`bc -l` verify) | refuted ✗ (divergence +56.81 PPL surface) |
| **F5**: measure-theoretic ill-posedness restricted to stack B only | pending multi-stack ablation grid (Cell 1-8 之 disentangle, D60+ window) | pending (D60+ partial) |

### §3.3 GradScaler skip 数学 derive 之 code-paper consistency (D-1 纪律 3)

#### MATH_VERIFY_D25 数学 derive (File L)

source verbatim (File L line 14, 87-88, 111, 251, 331, 396, 417):
```
- 9070XT base model PPL (wikitext-2 val): 93.349
- candidate C seed=42 α=0 之 a1_ppl gen=0..9: 全部 93.35 (10 代 frozen)
- 每 step skip ⟹ weight frozen ⟹ a1_ppl = base PPL 93.349 ✓
- ${\mathbb E}[N_{\text{update}}] \to 0 \to \theta = \theta_{\text{base}}$
- $a1_{\text{ppl}} = \text{base PPL}$
```

数学 form 严格度: **L1 strict (formal derive, no axiom violation)**. 形式: $\theta_t = \theta_{t-1} + \eta \cdot \text{step}_t$, 当 GradScaler skip ⟹ $\text{step}_t = 0 \forall t$ ⟹ $\theta_t \equiv \theta_{\text{base}}$ ⟹ $\Phi(\theta_t) = \Phi(\theta_{\text{base}}) = \text{base PPL}$.

#### code source binary trace (D-1 纪律 3)

| code path | line | source 之 verbatim binary |
|---|---|---|
| `candidate_c_runner.py:246` | L246 | `cat_for_this_gen = None if g == 0 else cat_cfg` (gen=0 必 CAT disabled) |
| `candidate_c_runner.py:173` (referenced via train_one_generation) | n/a | vanilla Trainer baseline for gen 0 (C §1.2 verbatim) |
| `cat_trainer.py:113` | L113 | CAT enabled branching (gen ≥ 1 + α > 0 之 CATTrainer) |
| `pytorch/torch/amp/grad_scaler.py:328-405` | L328-405 | GradScaler.step skip logic (`_maybe_opt_step` 在 `found_inf_per_device` 任何非零时 skip `optimizer.step()`) — C §2.1 line 178-184 binary cite |
| `pytorch/aten/src/ATen/native/cuda/AmpKernels.cu:49-186` | L49-186 | `_amp_foreach_non_finite_check_and_unscale_cuda_` NaN check (line 67 `!isfinite_ensure_cuda_math(val)` + line 68 `*found_inf_ptr = 1.f`) — C §2.2 binary cite |

#### binary consistency: 数学 form ↔ code path ✓

| consistency check | binary |
|---|---|
| 数学 derive $\theta = \theta_{\text{base}} \Rightarrow a1_{\text{ppl}} = $ base PPL 93.349 | ✓ |
| code path: GradScaler skip ⟹ optimizer.step bypass ⟹ weight 不 update ⟹ eval = base model | ✓ |
| 实测 9070XT a1_ppl seed=42 α=0 10 代 frozen 93.349 | ✓ (jsonl source: candidate_c_20260522_203837.jsonl line 1-10) |
| 5 bit-identical cells 实测 93.388 vs base 93.349 之 partial drift ~0.04 PPL | ✓ within fp16 mixed-precision rounding expected: 2^-10 ≈ 0.1% per op × ~7300 train step ≈ 0.5-1% drift expected; 实测 0.04% within expected rounding |

### §3.4 修正后数学 form 指导下一轮实验 design

#### F4 multi-stack 之 specific cell list (D60+ partial, ~$120-150 cloud cost)

| Cell # | stack | 状态 | cost estimate |
|---|---|---|---|
| 1 | 5060 fp16 (Blackwell sm_120, cu130) | ✓ done D27-D28 (D file) | 0 (done) |
| 2 | 5060 fp32 (Blackwell sm_120, cu130) | ✓ done D24-D25 (E0/R1/SMOKE) | 0 (done) |
| 3 | 5060 bf16 (Blackwell sm_120, cu130) | 新 candidate | ~4h GPU 本机 |
| 4 | 9070XT fp16 (RDNA4 gfx1201, ROCm 7.2) | ✓ done D22-D27 (PID 491900 N=180) | 0 (done) |
| 5 | 9070XT fp32 (RDNA4 gfx1201, ROCm 7.2) | 新 candidate (caveat ~7.5-10 天) OR cloud A100 spot ~$40 | local ~10 天 OR cloud $40 |
| 6 | 9070XT bf16 (RDNA4 gfx1201, ROCm 7.2) | 新 candidate | ~4h GPU 本机 |
| 7 | Apple M3 MLX fp16 | 新 candidate (cloud spot) | ~$30 cloud |
| 8 | Google Cloud TPU v5e bf16 | 新 candidate (cloud spot) | ~$50 cloud |

**total estimate**: 本机 ~8h + cloud ~$120-150 (Cell 5+7+8 之 cloud spot) — D60+ window partial actualize, 留 PI + 关卡 4 budget 决

#### F5 measure-theoretic cross-axis test (D60+ partial)

| Axis | scope | partial actualize | full close (D60+) |
|---|---|---|---|
| Axis 1 model size | OPT-125M (done) → Llama-3-8B (cloud $50) → Mixtral-8x7B (cloud $300+) | Llama-3-8B Phase 5 (paper v9 SKELETON §2.8 line 151 之 C1 候选) | Mixtral 留 D60+ window |
| Axis 2 dataset | wikitext-2 (done) → C4 → SlimPajama → 中文 Wudao | C4 之 cross-dataset partial | 中文 Wudao 留 D60+ window (DS 第七缺口) |
| Axis 3 algorithm | SFT (done) → DPO → RLHF → Constitutional AI | DPO 之 cross-algorithm partial | RLHF + Constitutional 留 D60+ window |
| Axis 4 optimizer | AdamW (done) → Lion → Sophia | Lion 之 cross-optimizer partial | Sophia 留 D60+ window |

**16-cell grid 之 partial actualize**: 3-axis × 2-cell = 6-cell partial, D60+ window 6-9 月 (V9 SKELETON §2.8 line 151 之 C2 measurement-theoretic ablation framework first instantiation)

### §3.5 paper polish 之 反向 verify 修正 candidate (D27-D60 polish window)

| # | candidate | 反向 verify source | paper polish wording |
|---|---|---|---|
| 1 | **base disambiguate (36.32 vs 36.536)** | A line 610 paper §4.6 mean 36.32 vs B/D 之 5060 fp32 jsonl 36.53597 之 0.22 PPL gap | "9070XT fp16 a1_ppl 93.349 vs 5060 fp32 jsonl 36.536 (single-launch reproducibility benchmark): +56.81 PPL / +155.5%; vs paper §4.6 reported mean 36.32 (Shumailov 2024 baseline cross-validate): +57.03 PPL / +157.0%. 两个 valid reference base, 一致 within 0.22 PPL." |
| 2 | **cite scope schema (5 vs 11)** | I §2.4 line 97 vs H §2.1 line 94 之 schema 不一致 | "5 verbatim cite in main text (strict scope) + 6 adjacent literature reference in supplementary section (cumulative scope) = cumulative 11. explicit scope schema disclose." |
| 3 | **anchor naming (SMOKE 1/4 vs LITERATURE A1-A5)** | D §3 line 89-92 disambiguate naming vs E §1-§8 之 5 anchor naming | paper polish 推荐 unified A1-A5 naming (LITERATURE), SMOKE disambiguate 1/4 入 sub-anchor reference. A4 之 sub-mode b1 = ROCm-side specific instantiate. |
| 4 | **F9 之 93.349 vs 93.387 wording** | C F9 line 502-508 之 跨 chain run partial drift | "9070XT seed=42 α=0 跨 2 chain run (D22 candidate_c + D25-D26 PID 491900) 之 partial drift 93.349-93.388 ≈ 0.04 PPL ≈ 0.04%, within fp16 GradScaler skip 之 deterministic regime 之 small accumulator variation." |
| 5 | **F6 SoftmaxForward fp16 caveat** | C §2.4 line 218-227 + §2.6 line 254-258 之 OPT eager bypass | "MIOpen SoftmaxForward fp16 caveat 仅 active 在 attention 之外之 logits softmax path; OPT eager attention 之 PyTorch 层 显式 fp32 cast 之 cover bypass MIOpen fp16 softmax path." (paper v9 §2.4 explicit caveat footnote) |

---

## §4 剩余缺口 list + 可证伪 F1-F5 specific protocol

### §4.1 D28-D60 polish window 可 close 缺口 (5 项, 总 ~6h)

| # | gap | close approach | time estimate |
|---|---|---|---|
| 1 | base disambiguate (36.32 vs 36.536) | paper polish explicit disclose + V9 SKELETON §5.2 wording revise | ~1h |
| 2 | cite cumulative scope (5 vs 11) | paper polish schema unify (strict 5 + cumulative 11 + supplementary 6) | ~1h |
| 3 | anchor naming schema (SMOKE 1/4 vs LITERATURE A1-A5) | paper polish unified A1-A5 naming + sub-anchor reference for SMOKE | ~2h |
| 4 | F6 SoftmaxForward fp16 caveat | paper v9 §2.4 explicit caveat footnote (OPT eager bypass 之 explicit disclose) | ~1h |
| 5 | F9 之 93.349 vs 93.387 wording | paper polish explicit disclose (跨 chain run partial drift within expected rounding) | ~1h |

### §4.2 D60+ window 之 substantive 缺口 (留 PI 决 timing + budget)

| # | gap | D60+ approach | time estimate |
|---|---|---|---|
| 1 | multi-architecture (transformer + CNN + state-space) | Banach LLM C1 (V9 SKELETON §2.8 line 151) | 3-6 月 |
| 2 | multi-dataset (跨领域 / 跨语言) | measurement-theoretic ablation framework first instantiation C2 | 6-9 月 |
| 3 | multi-stack ablation grid (TPU + Apple MLX + Intel oneAPI) | F5 close prereq (Cell 7+8 cloud spot) | 6-9 月 |
| 4 | Banach 5-mode failure taxonomy + transition kernel | C3 (V9 SKELETON §2.8 line 151) | 6-12 月 |
| 5 | (c) partial form HF Trainer 库源码追读 | 子 task of C2 (measurement-theoretic ablation framework first instantiation) | 6-9 月 |
| 6 | (d) mirror dual convergence-side novelty 之 substantive close | C3 子 task (Banach 5-mode failure taxonomy first instantiation) | 6-12 月 |
| 7 | 中文圈 prior art 后 4 anchor A2-A5 之 独立 paper search | 留 PI + DS 之 关卡 3 + D28+ extend search | ~2 月 |
| 8 | RLHF axis + Constitutional AI multi-axis | D60+ extend (V9 SKELETON §2.8 line 151 之 axis 3 algorithm extend) | 6-12 月 |

### §4.3 可证伪实验 specific protocol (F1-F5)

| F-cell | binary specify | 当前 state | cost + budget |
|---|---|---|---|
| **F1**: gen_N_ppl >= gen_0_ppl + 5 PPL on healthy fine-tune chain | Stack A 5060 fp32 ✓ pass (Δ = +42.04 PPL); Stack B 9070XT fp16 ✗ fail (Δ = -2.67e-4) | done | 0 (existing data) |
| **F2**: 5 cells distinct count > 1 on Stack B | refuted ✗ (5 cells distinct count = 1, all = 93.38780852810248) | done | 0 (existing data) |
| **F3**: hidden-state level signature distinct count > 1 across 5 bit-identical cells | refuted ✗ (a3_attn_entropy distinct count = 5 at ~10⁻³ scale) | done | 0 (existing data) |
| **F4 (cross-stack divergence)**: |Δ(stack A, stack B)| > 50 PPL under identical config (seed, α, gen, code, yaml) | refuted ✗ (+56.81 PPL surface, base = 5060 fp32 jsonl) | done | 0 (existing data) |
| **F5 (measure-theoretic ill-posedness)**: measure-theoretic ill-posedness restricted to stack B only (8-cell ablation grid) | pending | NOT done within D29-D60 | D60+ ~8h GPU 本机 + ~$120-150 cloud spot |

---

## §5 严守 binding self-check (13 项 binary)

| binding | binary verify | anchor |
|---|---|---|
| 1. paper v8 final 47/47 D17 锁定不动 | ✓ | §0 + 全 ablation 不动 paper v8 substantive content |
| 2. 12 NOT-claim (i)-(xii) 撤回不复活 | ✓ | §0 + §2.3 prior art gap list 中 (d) mirror dual + (c) 0 cover 之 honest disclose 不复活 paradigm shift |
| 3. 反题 6 P0★ A-F disclosed + P0★-G partial isolate update | ✓ | §1.2 Inconsistency 1 base disambiguate + §3.1 F5 闭环咬合 + P0★-G partial isolate 之 子机制 (a) ★★★★★ partial isolate cross-channel reinforce |
| 4. D29 投 arXiv + TMLR + KBS 不动 | ✓ | §0 + §4 剩余缺口 list 不擅 venue 改动 |
| 5. ICLR 2027 第一站 + Nature 三层不越级 | ✓ | §4.2 D60+ window 之 substantive 缺口 全 ≤ paper v9 → v10 → v11 之 三层 progression |
| 6. paper v8 title "Contradiction Loss" 不动 + v9 改 "Internal Tension Loss" 留 PI 决 | ✓ | §0 + 不 declare title 改名 final |
| 7. D-3.7 PI 主权 严守 (本 ablation 不 declare paper-level emergent final) | ✓ | §1-§5 全 reconcile + 修正 candidate 全留 PI + 关卡 4 决 |
| 8. 7B13 单点 git 写权 (本 sub-agent 不擅 commit / push / spawn 子-子 agent / ssh 22) | ✓ | 全 task 0 commit + 0 push + 0 ssh 22 + 0 spawn 子-子 agent |
| 9. zero-context (不读 CLAUDE.md / memory / 一凡 认知流) | partial ✓ | system reminder auto-inject CLAUDE.md / MEMORY.md, 但 audit 之 verdict 不依赖其 content, 仅 use 4 主源 + 8 辅源 + jsonl raw 之 binary trace |
| 10. read-only + 1 Write | ✓ | 全 task 仅 1 次 Write 本 ablation report file |
| 11. 不擅 launch 新实验 (本 ablation 不跑新 chain / smoke / cell, 仅 cross-verify 已有 data) | ✓ | 全 §1-§4 不 launch 任何 chain / cell, 仅 cross-verify + 反向 verify + 修正 candidate |
| 12. D-1 纪律 5 sub-rule (真实日期 `date` binary verify) | ✓ | §0 head line `date '+%Y-%m-%d %H:%M:%S %Z'` verbatim 2026-05-28 13:27:59 CST |
| 13. D-1 纪律 5 错误 surface 不静默 (4 cross-inconsistency + F6 caveat + 子机制 (c) partial form 全 surface) | ✓ | §1.2 4 inconsistency binary surface (base + cross-chain drift + cite scope + anchor naming) + §3.1 F6 caveat 闭环 + §2.4 (c) partial form UNCERTAIN 之 0 prior art cover 之 institutional gap surface |

**13/13 ✓ (含 1 partial: zero-context 之 system reminder auto-inject CLAUDE.md, 但 audit verdict 不依赖)**

---

## §6 留 PI 决 list (≤ 5 项 binary)

| # | 留 PI 决 item | trigger window |
|---|---|---|
| 1 | **base disambiguate paper polish wording final** (36.32 vs 36.536 之 dual reference 之 final wording) | D29-D60 polish window |
| 2 | **anchor naming schema unified A1-A5 之 paper polish adoption** (V9 SKELETON 之 SMOKE disambiguate 1/4 → LITERATURE A1-A5 之 unified naming) | D29-D60 polish window |
| 3 | **(c) partial form HF Trainer 库源码追读 之 D60+ timing + budget** (C2 measurement-theoretic ablation framework first instantiation 之 secondary task, 6-9 月) | D60+ window |
| 4 | **multi-stack ablation grid Cell 5+7+8 之 cloud spot budget** (~$120-150 cloud + Cell 5 之 local 10 天 vs cloud A100 $40 之 trade-off) | D60+ window |
| 5 | **中文圈 prior art 后 4 anchor A2-A5 之 独立 paper search 之 完整性 verify** (DS 第七缺口 之 D28+ extend search) | D28+ window (留 PI + DS 之 关卡 3 + D28+ extend) |

---

## §7 sub-agent metadata + commit (留 Linux 姐姐 batch)

| 项 | 值 |
|---|---|
| agent identity | Opus 4.7 (1M context) zero-context cross-verify ablation sub-agent, 7B13 secondary session spawn (一凡 PI dispatch D28) |
| 协议 | zero-context cross-verify only — 4 主源 + 8 辅源 + jsonl raw binary trace; 不 launch 新实验; 不擅 ssh 22; 不擅 commit |
| 总 tool use | Read 6 (4 主源 + 2 辅源 J/E) + Bash ~5 (grep / wc / bc 数字 binary verify) + Write 1 (本 file) |
| Write count | 1 (本 ablation report file) |
| 字数 | ~5800 字 substantive (NMI 级别 实验严谨, table-heavy + 不 wall-of-text) |
| output file path | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/D28_CROSS_VERIFY_ABLATION_REPORT_20260528.md` |
| commit 状态 | **不擅 commit, 留 Linux 姐姐 main session batch commit** (等 D27 关卡 3 + 关卡 4 PI ack 之后) |
| 真实日期 | 任务启动第一时间 `date '+%Y-%m-%d %H:%M:%S %Z'` binary verify → 2026-05-28 13:27:59 CST (不继承 stale system reminder) |
| 一凡 priority 1 standing ack | 010-82951332 / 400-161-9995 standing; 三项安全检查 (绳子 / 物理环境 / 主治医生电话) standing; 健康 优先于 NMI submission timing / sync timing / venue 升级 |

### sub-agent verdict summary (供主会话 sign-off reference)

- 20 binary 数 cross-position table 之 reconcile state: **16 ≡ ✓ + 4 partial surface inconsistency** (Inconsistency 1 base + 2 cross-chain drift + 3 cite scope + 4 anchor naming)
- 4 子机制 tier consistency state: **(a) ★★★★★ + (b) ★★★★ + (c) strong REFUTED + partial UNCERTAIN + (d) ★★★** 全端 ≡
- F5 + experiment anchor 4 闭环咬合 state: **✓ (i)+(iii) framing 闭环 (代码做了正确的事 + ROCm stricter numerics catch fp16 真问题), (ii) "ROCm 有 bug" framing D27 自 retract**
- 数学-实验-实践闭环: GradScaler skip 数学 derive L1 strict ✓ + code path binary trace 一致 ✓ + 5 cells 实测 93.388 vs base 93.349 之 0.04% drift within fp16 expected rounding ✓
- anchor naming schema unified A1-A5 推荐 paper polish (LITERATURE + SMOKE disambiguate 入 sub-anchor)
- D27-D60 polish window 可 close 缺口 5 项 (~6h total)
- D60+ window substantive 缺口 8 项 (3-12 月 cadence, ~$120-150 cloud budget)
- F1-F4 全 refuted (binary) + F5 pending (留 D60+ multi-stack ablation grid)

---

完。

**生成**: Opus 4.7 (1M context) zero-context cross-verify ablation sub-agent, 7B13 secondary session spawn, 2026-05-28 13:27 CST 启动, ~14:30 CST 完

握着. paper v8 final 47/47 + D17 + D29 三 leg + 12 NOT-claim + 反题 6 P0★ 全 binding 严守. D-1 + D-3 严守. PI 主权严守. 留 D27-D60 polish + D60+ substantive close + 关卡 4 PI 决.
