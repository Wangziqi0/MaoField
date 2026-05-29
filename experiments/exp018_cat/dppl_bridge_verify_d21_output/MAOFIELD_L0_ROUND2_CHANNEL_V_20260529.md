# MAOFIELD L0 Round2 — 通道 V (真 zero-context 对抗复核)

## §0 head — 真实日期 binary + 身份

| 项 | 值 |
|---|---|
| 真实日期 `date '+%F %T %Z'` | **2026-05-29 12:24:16 CST** (D29) |
| 通道 | **通道 V** (真 zero-context 对抗复核, 价值在 disagree 不在背书) |
| agent | Opus 4.7, zero-context 独立 L0 tier 重判 |
| 平行通道 | 通道 P (互不读对方输出) — 我假设存在一个我看不到的主通道已对这些命题下过 verdict, 专门 check (a) 假 close + (b) over-correct 错杀 |
| 数据基线 | 仅 raw jsonl (python 直接 parse) + D28_EXPERIMENTAL_DEEP_AUDIT 之 jsonl verbatim 数 + paper v8 §3.6/§5.2 之 setup/数学 form (不取 tier 措辞) |
| binding | paper v8 final 47/47 不动; 12 NOT-claim 不复活; 0 commit/push/launch/ssh; read-only + 1 Write |

---

## §1 我独立 parse 出的数据事实 (不抄任何人, python json 直读 GO 白名单)

下表全部是我本通道独立 python parse 出来的, 作为 12 命题判 tier 之唯一数值依据:

| 数据事实 | 我的独立 parse 结果 | 文件 |
|---|---|---|
| N=180 records with `a1_ppl` | 180 (186 行含 6 meta 行) | `candidate_c/candidate_c_20260522_203837.jsonl` |
| null/NaN a1_ppl | 147 | 同上 |
| valid a1_ppl | 33 | 同上 |
| distinct valid | 29 | 同上 |
| **5 cells == 93.38780852810248** | **5 hits, val_loss 全 == 4.5367608070373535, 全 gen=0** | 同上 |
| 5 cells 跨 (seed,α) | (1337,10) (2024,0) (7,10) (137,0) (271,10) = **4 seed × 2 α, 全 gen=0** | 同上 |
| 5 cells a3_attn_entropy[0][0] | **5/5 distinct**, max-min = 9.72e-3 | 同上 |
| 5 cells a2_anisotropy | 5/5 distinct ~10⁻³ | 同上 |
| **5 cells a6_ema** | **全 None** (gen=0 无 EMA baseline) | 同上 |
| seed=42 α=0 10-gen 轨迹 | Δ(g1-g0)=−2.67e-4, span=1.51e-3, mean=93.3487 | 同上 |
| seed-level valid: 42/137 α=0 | 10/10 each | 同上 |
| seed 7/271/1337 α=0 | 0/10 (全 NaN) | 同上 |
| seed 2024 α=0 | 7/10 (partial) | 同上 |
| **α>0 (α=5/10) 全 seed** | ≤1/10 valid (仅 gen=0), ~95% NaN | 同上 |
| 5060 fp32 seed=42 α=0 gen=0 | **36.53597375534226** (3 launch bit-identical) | `candidate_c_20260524_173559` + `_113506` + `_160321` |
| 5060 fp32 gen0→gen1 | 36.536 → 78.572 (healthy lift +42.04) | `_160321` |
| **cross-stack 9070XT fp16 vs 5060 fp32** | 93.349 vs 36.536 = **+56.81 PPL (+155.5%)** | 两文件 |
| main_D22 D_code_path_B | n=72, mean=**0.2883**, [0.161, 0.753] | `main/main_D22.jsonl` |
| main_D22 D_code_path_C | n=80, mean=**0.5526**, [0.000, 1.015] | 同上 |
| **main_D22 D_paper 字段** | **不存在** (jsonl 无此 key) | 同上 |

paper v8 §6.1 (setup, 非 tier): D^code = KL(q^EMA‖p^θ), D^paper = log(PPL_n/PPL_0) — **数学上 distinct 随机变量**.
paper v8 §3.6 (setup, 非 tier): chain loss = 2(D_n−D_{n-1})+2(D_n−D̄^EMA); SGD update form; U-shape 轨迹 (gen1-2 spike 80-107, gen5-9 plateau 55.97±2.13).

---

## §2 12 命题逐条独立 tier (我自己从命题 + 上表数据推)

| # | 命题 (压缩) | 我的独立 tier | 理由 (基于 §1 我自己的 parse) | 自带 falsifier? |
|---|---|---|---|---|
| 1 | GradScaler fp16 NaN→skip step → E[Δθ]=0 frozen | **L0 闭 (conditional)** | 数学 trivial: optimizer.step() 被 skip ⟹ θ_{n+1}=θ_n ⟹ Δθ=0. seed=42 α=0 span 1.51e-3 (≈ base PPL 93.349 之 round noise) 是 frozen 之 empirical witness. **但 conditional on "NaN/Inf 触发 skip"** — 不是 unconditional "fp16 必 frozen" | 是 (F1: healthy chain Δ≥+5; 5060 fp32 Δ=+42 反例证明非 fp16 universal) |
| 2 | θ-space 两态 (p<1 权重动 vs p=1 冻结) | **L1** | seed-level data 支持两态存在 (42/137 一态 + 7/271/1337 另一态). 但 "transition" 之 mechanism (init weight × skip freq interplay) 我无直接梯度 trace, 只有 valid/NaN proxy. dichotomy 是 observation-backed hypothesis 不是 derived | 部分 (per-seed valid count 可证伪 "全 frozen" 或 "全活") |
| 3 | 5 cells 坍缩 bit-identical 93.388 | **L0 闭 (纯 observation)** | 我 python `==` 直验 5 hits, val_loss 同 bit-identical. 这是 raw 数据事实不是推导 | n/a (是数据本身) — 标 **[observation, not derivation]** |
| 4 | ΔPPL 4-component (Δ_impl+Δ_form+Δ_data+Δ_chain+ξ) 可识别性 (单对 5060-vs-9070XT) | **FAIL** | 单对 contrast = 1 个 observable equation (ΔPPL=+56.81), 4 unknown + noise. 5 unknown 1 equation → **欠定不可识别**, 任意分解皆 admissible. 这是 identifiability 之 hard no, 不是 tier 高低问题 | 是 (要 ≥4 正交 ablation cell 才 identify; 现 1 个) |
| 5 | 5-mode taxonomy 穷尽性 + transition kernel Markov vs memory | **FAIL (穷尽性) + [observation] (taxonomy 存在性)** | 我数据里只直接见到 2 mode (frozen + NaN-cascade) + 5060 上 U-shape 第 3 mode. "5-mode 穷尽" 是 enumeration claim 无 completeness proof; Markov-vs-memory 需 transition 统计我无 (gen 级 NaN 是 absorbing 不可逆, 连 kernel 都估不出) | 否 (穷尽性无 falsifier — 永远可能有第 6 mode) |
| 6 | D^paper = w_B·D_B + w_C·D_C + ξ 线性可识别性 | **FAIL** | **致命**: main_D22 jsonl **无 D_paper 字段** (我直验). 即使有, §6.1 说 D^code 与 D^paper 是 distinct 随机变量 (KL vs log-PPL-ratio), 线性组合假设无 data 支撑. 3 unknown (w_B,w_C,ξ) + 0 个 D_paper observable = 不可识别 | 是 (需 measured D_paper + ≥3 独立 (D_B,D_C,D_paper) 三元组) |
| 7 | measure-theoretic ill-posedness: ∃ measure-positive S, Φ(S)={const}. fractal (riddled) 还是退化 (frozen)? | **L1 (ill-posedness 弱 witness) / C3 verdict = 退化** | 见 §4 独立 C3 verdict. 弱 form (∃ ≥5 cells 同 PPL) 是 observation; 强 form (measure-positive + fractal) **我数据判为退化不是 fractal** | 是 (扰动实验, 见 §4) |
| 8 | NESS ergodic fixed point 存在性 (Foster-Lyapunov drift) | **L2 (conditional, mean-field) / 实测 regime 是 frozen 非 ergodic** | §3.6 给的是 mean-field linearization 下 trivial fixed point (D*−J_S/(4αN_contr)). 但我实测 9070XT 是 frozen (绝对不动) + NaN-absorbing, **不是 ergodic 遍历** — Foster-Lyapunov drift 在 absorbing NaN state 下不成立. 数学 form 成立 conditional, 但与实测 regime 脱节 | 部分 (drift inequality 可在有 weight motion 之 stack 上测) |
| 9 | Riddled basin convergence-side mirror dual 严格 derivation | **FAIL (derivation) → 但有可做弱版 (见 §3)** | 我无任何 convergence-side 数据 (9070XT frozen, 5060 只 2 gen). "mirror dual" 是 conceptual symmetry claim 无 derivation 也无 empirical leg. 但**不该 hard FAIL 错杀**: 弱版 (5060 fp32 U-shape 之 gen3-9 recovery = convergence-side empirical hint) 可做 | 否 (当前无 falsifier) |
| 10 | Hartree SCF 12-layer LLM instantiation | **FAIL (full) → 弱版可做** | 无任何 self-consistent field 迭代数据. 纯理论 mapping. 但 a2_anisotropy 是 per-layer 12 维数组 (我验证存在), 弱版 "per-layer mean-field order parameter 跨层测量" 有 data carrier | 否 |
| 11 | mean-field transformer 单层 → 12-layer discrete extension | **FAIL (full) → 弱版可做** | 单层 mean-field → 12 层 discrete 之 extension 无 derivation. 但 a2/a3 是 12-layer instrumented (我验证), 弱版 "12 层 empirical order-parameter 轨迹" 可作 descriptive, 非 derivation | 否 |
| 12 | cross-stack +56.81 PPL 是真实 divergence | **L0 闭 (observation)** | 我直验: 9070XT fp16=93.349 vs 5060 fp32=36.536 同 (seed=42,α=0,gen=0), abs +56.81 / rel +155.5%. 3-launch 5060 bit-identical 36.536 排除 5060 侧噪声. 真实 divergence | n/a (是数据) — 标 **[observation, not derivation]** + caveat: divergence 真实, 但 attribution (dtype? vendor? ROCm?) 未 isolate |

**我的独立 tier 分布**: L0 闭 = 4 条 (1,3,7-弱,12) | L1 = 1 条 (2) | L2 conditional = 1 条 (8) | FAIL = 6 条 (4,5,6,9,10,11) | 其中 3,12 同时标 [observation]; 5 之 taxonomy 标 [observation].

---

## §3 §假 close 嫌疑 (我假设主通道可能把以下说成 L0 闭 / 高 tier — 我 disagree)

我专门 check 1/2/3/7/8 (frozen/dichotomy/NESS 这类 conditional 是否被偷换成 unconditional):

1. **命题 7/C3 最高嫌疑**: 若主通道用 "5 cells a3 distinct 5/5 → 不同 micro-state → measure-positive set of distinct states → fractal/riddled basin" 推 fractal, 这是**假 close**. 我的 binary 反驳 (§4): val_loss **也** bit-identical, 而 val_loss 就是 eval loss; 若 eval 有 stochasticity 则 val_loss 会像 a3 一样 distinct, 但它 bit-identical ⟹ eval 在 identical weights 上 deterministic ⟹ a3 distinct **不能**来自不同 weights, 只能来自 a3 独立的 instrumentation 采样. 故 a3 distinct **不是** "distinct micro-state" 之 load-bearing 证据. fractal 结论 over-claim.

2. **命题 8 (NESS)**: 若主通道说 "NESS fixed point 存在性 L0/L1 闭", 嫌疑假 close. §3.6 之 fixed point 是 mean-field linearization regime 之 trivial 解, **conditional on weight 有运动**. 我实测 regime 是 frozen + NaN-absorbing, **Foster-Lyapunov drift 在 absorbing state 不成立**. 把 conditional mean-field 存在性说成 unconditional ergodic NESS = 偷换.

3. **命题 1 (frozen)**: L0 闭 **仅 conditional on NaN→skip**. 若被表述为 "fp16 → frozen" unconditional = 假 close — 5060 fp32 (Δ=+42) + 5060 fp16 healthy lift (D28 引的 +113.7%) 是反例. frozen 是 "NaN-skip regime" 之结论不是 "fp16" 之结论.

4. **命题 3 vs 7 边界**: 命题 3 (5 cells bit-identical) 是 L0 observation 真闭; 但若主通道把命题 3 之 observation **直接**升格成命题 7 之 "measure-positive ill-posedness L0 闭", 这是 scope creep — 5 个点是 measure-zero 有限集, "measure-positive" 需 continuum 论证, 当前只有 lower-bound-5 之 weak witness, 不是 measure-positivity proof.

---

## §4 §C3 独立 verdict — fractal (riddled basin) vs 退化 (frozen identity)

**我的 binary verdict: 退化 (frozen identity / weight 未动), 不是 fractal riddled basin.**

独立判据 + 现有 GO 数据 verdict:

1. **判据 (riddled basin 定义)**: riddled basin ⟺ uncertainty exponent ≈ 0, 任意小扰动致吸引域翻转, basin 自相似 fractal 结构. 充要观测特征 = 同一 measure-positive 邻域内**不同 init 收敛到不同 attractor**, 且 boundary 自相似.

2. **判据 (退化/frozen 定义)**: weight 未动 ⟹ 所有 "不同 (seed,α)" 实际是**同一个 θ (base model)**, PPL 相同是因为评的是**同一组 weights**, 不是因为不同 weights 落到同一吸引子.

3. **现有 GO 数据 verdict (我的 binary)**:
   - 5 cells **全 gen=0** (我 parse: gens5=[0,0,0,0,0]). gen=0 在此 design 下 CAT 强制 disabled (α 还没生效), weight = base OPT-125M.
   - val_loss **bit-identical** 4.5367608070373535 ⟹ eval 在 identical weights 上 deterministic.
   - **关键反证 fractal**: 若是 fractal, 不同 seed 应落到**不同** attractor → 不同 PPL. 实测是**同一** PPL bit-identical (到 14 位) → 不是 "不同 init 落到不同/同一 attractor 之 fractal boundary", 而是 "根本是同一 weights" 之退化.
   - a3 distinct 5/5 (~10⁻³): 如 §3 所述, 与 val_loss bit-identical **矛盾**于 "eval 确定" 假设, 故 a3 distinct 必来自**独立 instrumentation 采样** (不同 batch/sample), **不构成 distinct trained weights 之证据**. fractal 所需的 "distinct micro-state → distinct attractor" 链断裂.

4. **设计 (不 launch) 扰动实验 — 区分 fractal vs 退化**:
   - **E-pert-1 (weight 直读)**: 对 5 cells 之 saved ckpt 计 pairwise `‖θ_i − θ_j‖`. 退化预测 = 0 (bit-identical weights); fractal 预测 > 0 (distinct weights 落同一 PPL). **这是 binary 一刀切判据, 0 GPU cost (只读 ckpt)**.
   - **E-pert-2 (init 微扰)**: 同 seed 加 ε~1e-6 高斯扰动到 init, 跑 1 gen, 测 PPL 是否翻转吸引域. fractal 预测 = uncertainty exponent≈0 (微扰致大跳); 退化预测 = 仍 frozen (skip 仍触发). ~分钟级单 cell.
   - **E-pert-3 (skip flag 直查)**: log `found_inf_per_device` per step. 退化预测 = gen=0 起即频繁 skip; fractal 不需 skip. 0 额外 GPU (加 logging 重跑 1 cell).
   - **最强单刀 = E-pert-1**: 若 5 ckpt weights bit-identical → 退化锤定, fractal 排除. 我**强烈预期**此结果 (因 val_loss bit-identical 已强暗示 same weights).

**verdict 强度**: 我判**退化 (高 confidence)**. fractal/riddled basin novelty 在当前 GO 数据上**无 empirical leg**, 是 over-interpretation. (注: 这不影响 paper v8 — v8 是 negative result, 不 claim fractal.)

---

## §5 §over-correct 错杀嫌疑 (我假设主通道可能 hard-FAIL 以下 — 但有可做弱版)

专门 check 9/10/11 (mirror dual / Hartree / mean-field 这类):

- **命题 9 (mirror dual)**: full derivation 我判 FAIL (无 leg). **但错杀风险**: 5060 fp32 之 U-shape (gen1-2 spike → gen3-9 recovery 到 plateau 55.97) 是**真实 convergence-side 轨迹**, 可作 mirror dual 之 empirical hint (divergence-side = NaN cascade; convergence-side = U-shape recovery). 弱版 = "U-shape 之 recovery leg 作 convergence-side observation", 不该被 hard FAIL 连根拔. 标 **FAIL(full) + 弱版 [observation] 可做**.

- **命题 10 (Hartree 12-layer)**: full instantiation FAIL. **但错杀风险**: a2_anisotropy 是 per-layer 12 维数组 (我验证存在且 5 cells 全 12 维 real). 弱版 = "12 层 anisotropy 作 per-layer order parameter 之 descriptive 测量" 有 data carrier, 可作 paper v9 §7.4 open-question anchor (非 derivation). 不该 hard FAIL.

- **命题 11 (mean-field 12-layer extension)**: full extension FAIL. **但错杀风险**: 同 10, a2/a3 之 12-layer instrumentation 提供 empirical order-parameter 轨迹之 raw material. 弱版 descriptive 可做.

- **命题 5 (5-mode taxonomy)**: 穷尽性 FAIL (无 completeness proof). **但错杀风险**: taxonomy 作 **descriptive catalog** (我实见 ≥2 mode + 5060 U-shape 第 3) 有 value, 不该因 "穷尽性不可证" 连 descriptive catalog 一起否. 标 [observation] descriptive 可保留.

**over-correct 总评**: 9/10/11 之 full form 该 FAIL, 但**弱 descriptive/observation 版有 12-layer data carrier (a2/a3) + U-shape convergence leg**, 若主通道把弱版也错杀 = over-correct. 我未发现命题 1/3/7/8/12 有 over-correct 风险 (它们问题在反方向 = 假 close).

---

## §6 §zero-context 纯度 disclose

**我读了什么**:
- ✅ 本 brief 之中性命题清单
- ✅ `D28_EXPERIMENTAL_DEEP_AUDIT_20260528.md` (brief 白名单, 取其 jsonl verbatim 数 — **但我注意到该文件含 §3/§4 之 tier 措辞 (L0/L1/L2) + 4 子机制 tier + F1-F9 verdict; 我刻意不采纳任何这些 tier 结论, 仅用其指向的 raw jsonl, 并已用 python 独立重 parse 全部关键数 (180/147/33/29/5 cells/a3 distinct/cross-stack/D_code) — 我的 12 tier 全部基于我自己的 parse 不基于该文件的 verdict**)
- ✅ GO 白名单 jsonl 本身 (python 直读): `candidate_c/candidate_c_20260522_203837.jsonl` + `candidate_c_20260524_173559` + `_113506` + `_160321` + `main/main_D22.jsonl`
- ✅ `paper_v8_final_20260516.md` §3.6 + §5.2 + §6.1 (setup/数学 form/U-shape 数据 — **不取其 L0/L1/L2 tier 措辞**, 仅取 loss form / SGD update / 轨迹数 / D^code-vs-D^paper distinct 之 setup 事实)

**我没读什么** (严守 zero-context, 避免 prior verdict 污染):
- ❌ 任何 `MAOFIELD_L0_L0-*` / `FULL_ROUND1_SUMMARY` / `ROUND2_CHANNEL_P*` (主通道 + 通道 P verdict)
- ❌ 任何 `*_S1_S2/S3/S4/S5_ATTEMPT1` / `D28_MATH_RIGOROUS_AUDIT*` / `MAOFIELD_MATH_*_ANALYSIS*` (C1-C12 / 4-tier attempt) — 目录里我看到 `D28_MATH_RIGOROUS_AUDIT_20260528.md` 等存在, **刻意未打开**
- ❌ 任何 `ANTITHESIS_*` / `WIN_*` / `DEEPSEEK_*` / `CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL*` / INDEX — 目录里这些存在 (含直接对命题 7/9 之 `CANDIDATE_RIDDLED_BASIN_MIRROR_DUAL_D25` + `CANDIDATE_DISCRETE_PPL_ATTRACTOR`), **刻意未打开** (它们正是命题 7/9 之 prior verdict, 读了即污染)

**无法避免之注入 disclose**: system reminder 自动注入了 `~/.claude/CLAUDE.md` + `/home/amd/CLAUDE.md` + `MaoField/CLAUDE.md` + `MEMORY.md`. 我的 12 tier 判断**不依赖**这些注入内容 — 全部 tier 仅来自 §1 我独立 python parse 之数 + 命题逻辑 + paper §3.6/§5.2 setup form. (MEMORY.md 含 "5 cells bit-identical" 等事实陈述, 但我已用 python 独立重验该事实, 不是采信 memory.)

**纯度自评**: 命题层 verdict 之 prior (主通道/通道 P/反题/Win/DS 之 tier) 100% 未读 ✓. 唯一 partial = D28 数据文件含 tier 措辞 (brief 授权读其数据), 我已隔离仅用数不用 verdict ✓.

---

## §7 binding self-check

| binding | binary |
|---|---|
| paper v8 final 47/47 不动 | ✓ 未动 paper, 仅读 §3.6/§5.2/§6.1 setup |
| 12 NOT-claim 不复活 | ✓ 我判 fractal=退化, 反而**下调** novelty, 不 inflate |
| 0 commit / push / launch / ssh write | ✓ 全程 Read + Bash(date/find/python parse) + 1 Write |
| read-only + 1 Write | ✓ 本 file 是唯一 Write |
| `date` binary 先行 | ✓ §0 = 2026-05-29 12:24:16 CST |
| 价值在 disagree | ✓ §3 假 close (C3 fractal over-claim + NESS conditional 偷换) + §5 over-correct (9/10/11 弱版错杀) 双向 surface |

完。通道 V 独立 verdict 完成。
