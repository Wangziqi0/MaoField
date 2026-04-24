# Win 半成品 — §4.11.1 P3 reformulation v2

**作者**: Win 姐姐（04-18 晚 → 04-19 新会话）
**日期**: 2026-04-19
**给**: Linux 姐姐（数字层 + coordination spot-check）+ 一凡（narrative final）
**base**: `LINUX_TO_WIN_SECTION4_11_P3_REFORMULATION_20260419.md` + `ACTION3_P3_WAVEFRONT_TILT_20260418.md` §3.3
**状态**: 半成品，**未 apply** 到 `arxiv_v1_full.md`。等 04-20 三方对齐。

---

## 1. §4.11 整 section 标题判断

**Win [?] judgment**: **保留** v1 原标题 *"Open methodological questions"*。

**理由**：
- §4.11 还有另外 3 个 items（§4.11.2 / §4.11.3 / §4.11.4）**仍 open**，未被 Action 3 处理
- §4.11.1 从 "open question" 降为 "identified artifact" 改变的是**单个 item 的 status**，不是整 section 性质
- 若整 section 标题改为 "Methodological diagnoses and residual questions" 之类，反而让读者以为所有 items 都已 resolve，这是对 Linux §4.11 其他 3 items 的 misrepresent

**如果一凡觉得**原标题不再准确，可用 *"Methodological diagnostics: resolved and open items"* —— Win 不推荐但 acceptable。

---

## 2. §4.11.1 v2 prose（基于 Action 3 §3.3 + Linux raw, Win 润色）

### Proposed text

> **§4.11.1 The ~10⁴ inner-Kramers factor: methodological artifact, not physical anomaly**
>
> `[DYNAMIC-DIFFUSIVE]` *(tag revised from v1's `[DYNAMIC-RARE-EVENT]`, which remains applicable only to the outer barrier, §4.9)*
>
> In v1 §4.8 we observed that the inner-barrier crossing fraction (0.85 at σ=0.5, t_sim=250) exceeds the 1D-Kramers prediction (9.5×10⁻⁵ per voxel) by a factor of ~10⁴, and flagged this as an open question with a suspected field-theoretic or coherent-source correction. Three diagnostic tests conducted as part of Action 3 (2026-04-18) rule out all such candidate mechanisms; the ~10⁴ discrepancy is instead attributable to the **inapplicability of the 1D-Kramers formula itself in this parameter regime**.
>
> **(i) Wavefront propagation rejected.** The spatial correlation C_s(r) of crossing events is flat over r ∈ [1.5, 16.5] voxel lattice distances at all tested Δt ∈ [1, 50] steps. An Avrami exponent fit across three independent documents gives n = 0.85 ± 0.01, inconsistent with the n=3 signature of three-dimensional nucleation-and-growth kinetics expected for Allen-Cahn wavefront dynamics. The 85% occupancy arises from voxel-local independent crossings, not from collective wavefront propagation.
>
> **(ii) BGE DC tilt rejected.** Using the post-smooth-normalize per-voxel ⟨S_b⟩_voxel ≈ −0.10 (scaled from the raw value 1.48×10⁻³ by the max-normalization factor), the projected force on the u-reaction-coordinate gives F_tilt ≈ 0.06, yielding a Boltzmann tilt ratio exp(F·d/T) ≈ 1.43—far below the ~10⁴ factor. A direct whitening control (source mean-subtracted) reproduces t_50 and final occupancy within 1pp of the original, confirming that DC tilt is not the driver.
>
> **(iii) Root cause identified.** A σ-scan (σ ∈ {0.3, 0.4, 0.5, 0.6, 0.7}) of the time-to-50%-crossing fits the power law 1/t_50 ∝ σ^3.09, **inconsistent** with the exp(−1/σ²) scaling of genuine Kramers escape (the implied ΔV extracted from a forced Kramers fit is 0.14, a factor of 14 smaller than the true barrier height 2.013). At σ = 0.5, the single-step noise displacement σ√Δt ≈ 0.112 produces Δu ≈ 0.22 on the reaction coordinate per step; in five to ten steps, cumulative diffusion traverses the u=1 → u=0.5 barrier distance. The relaxation time t_relax ~ 1/|V''(u=1)| ≈ 0.5 is comparable to the observed escape time t_escape ≈ 0.5; the **separation-of-timescales prerequisite** for 1D-Kramers validity (Mel'nikov & Meshkov, 1986; reviewed in Hänggi, Talkner & Borkovec, 1990) is **violated**. This regime is more accurately characterized as a **shallow-barrier, high-diffusion limit** in which the barrier provides only a modest (≈2×) slowdown relative to pure free diffusion, not as activated rare-event escape.
>
> The ~10⁴ factor, accordingly, is an **artifact of applying a formula outside its domain of validity**, not evidence of a physical mechanism awaiting explanation.
>
> **Consequence for the paradigm.** No Kramers-based quantitative prediction is reliable at σ ≥ 0.3 for the inner barrier with this potential. The reliable Kramers regime requires ΔV/T_eff ≳ 5 **and** t_relax ≪ t_escape; we satisfy the first (ΔV/T = 16) but violate the second. This reformulation does **not** affect the outer-barrier unreachability conclusion (§4.9): there, ΔV/T_eff = 105 and both prerequisites hold, so crossing is genuinely rare. The Axis A architectural result (§4.9; ⟨S_b⟩ = −1.48×10⁻³ at 17σ) likewise stands, as the whitening control in (ii) above confirms that the DC bias is not a driver of inner crossings.

### Win narrative judgments 注记

1. **Mel'nikov-Meshkov 1986 + Hänggi-Talkner-Borkovec 1990 显式 cite**：Win 同意 Linux [?]。这两个 reference 给方法学严格性 anchor，读者追问"为什么 Kramers 在这里不适用"时有 textbook ground truth 可查。**不 cite 过度**（两个就够），不挖 instanton / path integral 系列。

2. **"artifact of applying an inapplicable formula" 语气 vs "domain-of-validity"**：
   - Linux 原版（Action 3）: *"artifact of applying an inapplicable formula"*
   - Linux raw 备选: *"reflects the formula's domain-of-validity rather than a physical mechanism"*
   - **Win decision**: 混用——
     - 第一次出现用 *"artifact of applying a formula outside its domain of validity"*（= Linux 两版的 honest 合成，neither AI 味 softening 也不 self-flagellation）
     - Consequence 段用 *"reformulation does not affect..."*（积极语气 move forward）
   - **不用**纯 Action 3 版的"inapplicable formula"（偏 harsh, "self-criticism 色" 太重），**也不用**完全 softened "domain-of-validity" 版（过度礼貌）

3. **§4.9 explicit cross-reference**: 两处写入——
   - (a) mode tag 下的 parenthetical: *"which remains applicable only to the outer barrier, §4.9"*
   - (b) Consequence 段末: *"does not affect the outer-barrier unreachability conclusion (§4.9)... both prerequisites hold, so crossing is genuinely rare"*
   - (c) Axis A 显式 anchor: *"The Axis A architectural result (§4.9; ⟨S_b⟩ = −1.48×10⁻³ at 17σ) likewise stands"*
   这三处让 §4.11.1 的重写和 §4.9 的 outer barrier conclusion / Axis A result **零冲突**。

4. **Mode tag**: `[DYNAMIC-RARE-EVENT]` → `[DYNAMIC-DIFFUSIVE]` for inner barrier only。parenthetical 标清楚 outer 保留 `[DYNAMIC-RARE-EVENT]`。

---

## 3. 不做的事（Linux binding + Win 补充）

- ✗ **不**引入 "Langer bounce analysis pending" 或任何类似 cushion pattern（Linux Action 3 §5 明示反对）
- ✗ **不**用 "M3 almost works if we just..." 或类似 rhetorical softening
- ✗ **不**把 10⁴ factor 的 old framing（"field-theoretic correction suspected"）留作 hedge——直接改写，诚实 retract "suspected correction" 措辞
- ✗ **不** flag "future quantitative Kramers analysis" 为 roadmap item（方法学 artifact 识别 = 关门，不是新方向）

**Win 补充**：
- ✗ **不**显式 self-flagellate（"we were wrong in v1"）——用 "v1 §4.8 observed... flagged... Three diagnostic tests... rule out..."  的 neutral recount 语气。Popperian 诚实 = 说清楚事实，不需要姿态性道歉

---

## 4. 数字 binding spot-check 清单（给 Linux）

从 Linux raw §7 checklist + Win prose 对照：

| 数字 | Linux binding | Win prose 写法 | 一致? |
|---|---|---|---|
| 10⁴ factor | 保留 | "exceeds... by a factor of ~10⁴" + "~10⁴ discrepancy" | ✓ |
| 0.85 occupancy | 原文保留 | "inner-barrier crossing fraction (0.85 at σ=0.5, t_sim=250)" | ✓ |
| 9.5×10⁻⁵ Kramers prediction | 原文保留 | "1D-Kramers prediction (9.5×10⁻⁵ per voxel)" | ✓ |
| Avrami n = 0.85 ± 0.01 (3 docs) | 原文保留 | "n = 0.85 ± 0.01 across three independent documents" | ✓ |
| n=3 expected for 3D Allen-Cahn wavefront | 原文保留 | "inconsistent with the n=3 signature of three-dimensional nucleation-and-growth" | ✓ |
| C_s(r) flat | 原文保留 | "spatial correlation C_s(r)... flat over r ∈ [1.5, 16.5]" + "at all tested Δt ∈ [1, 50] steps" | ✓ |
| F_tilt = 0.06, Boltzmann = 1.43 | 原文保留 | "F_tilt ≈ 0.06, yielding a Boltzmann tilt ratio exp(F·d/T) ≈ 1.43" | ✓ |
| ⟨S_b⟩_voxel ≈ -0.10 | 原文保留 | "post-smooth-normalize per-voxel ⟨S_b⟩_voxel ≈ −0.10" | ✓ |
| raw 1.48×10⁻³ | 原文保留 | "scaled from the raw value 1.48×10⁻³" | ✓ |
| whitening control ±1pp | 原文保留 | "reproduces t_50 and final occupancy within 1pp" | ✓ |
| σ^3.09 | 原文保留 | "1/t_50 ∝ σ^3.09" | ✓ |
| implied ΔV 0.14 vs true 2.013, 14× smaller | 原文保留 | "implied ΔV... is 0.14, a factor of 14 smaller than the true barrier height 2.013" | ✓ |
| σ√Δt ≈ 0.112, Δu ≈ 0.22 | 原文保留 | "single-step noise displacement σ√Δt ≈ 0.112 produces Δu ≈ 0.22" | ✓ |
| "5-10 steps" cumulative traverse | 原文保留 | "in five to ten steps, cumulative diffusion traverses" | ✓ |
| t_relax ~ t_escape ≈ 0.5 | 原文保留 | "t_relax ~ 1/\|V''(u=1)\| ≈ 0.5... t_escape ≈ 0.5" | ✓ |
| ΔV/T_eff = 16 (inner) / 105 (outer) | 原文保留 | "ΔV/T = 16... outer barrier (§4.9): there, ΔV/T_eff = 105" | ✓ |
| "shallow-barrier, high-diffusion limit" | 原文保留 | 原短语保留 | ✓ |
| 2× slowdown | 原文保留 | "modest (≈2×) slowdown relative to pure free diffusion" | ✓ |
| "separation-of-timescales prerequisite violated" | 原文保留 | 原短语保留 | ✓ |
| ΔV/T ≳ 5 + t_relax ≪ t_escape 双条件 | 原文保留 | "requires ΔV/T_eff ≳ 5 **and** t_relax ≪ t_escape" | ✓ |
| Axis A ⟨S_b⟩ = -1.48×10⁻³, 17σ | 原文保留 | "⟨S_b⟩ = −1.48×10⁻³ at 17σ" | ✓ |

**0 处 round, 0 处 inflate, 0 处 drop provenance**。

---

## 5. §4.11 其他 3 items（未改动）

v1 §4.11.2 / §4.11.3 / §4.11.4 保持原样。Win **不碰**（Linux 明确声明：那些不是 P3 reformulation 范围内）。

---

## 6. 协调 check（§3 + §5.1 + §6.1 → §4.11.1）

- **§3 NESS 叙事**：§4.11.1 不涉及 SSB / Goldstone / 稳态结构讨论，和 §3 正交 ✓
- **§5.1 M3 falsification**：§4.11.1 只是 P3 重写，不和 M3 关联（P3 是 inner Kramers rate anomaly，M3 是 V_0 self-consistent PDE）——完全不同 claim。Win spot-check: §4.11.1 有无句子会被 read 成 "M3 也是方法学 artifact"？**没有**，§4.11.1 只谈 1D-Kramers formula 对 shallow-diffusion 的 domain-of-validity 问题。✓
- **§6.1 Claimed / Not Claimed**：§4.11.1 不影响 §6.1 任何 bullet（§6.1 #5 是 Axiom 6 / OP1 bullet，和 P3 Kramers 无关）。§6.1 若有 "open methodological questions" 相关 bullet，可以 soft update 为 "open methodological items identified in §4.11; one (inner-Kramers) resolved as artifact, others remain open"——**但这不是本 diff 要 gate 的**，归 §6.1 half 自行判断（本 half 不触发）。

---

## 7. Apply 时机

**建议**:
- **α 路径**：直接 apply（"honest retract, not affecting outer-barrier or paradigm conclusions"，完全 α 语气）
- **β 路径**：直接 apply + 可能追加 Phase 3 conditional experiment（finer σ-scan 验证 crossover σ* where Kramers becomes applicable）
- **γ 路径**：可 apply + 可能扩写为 "toward a unified description of shallow-to-deep barrier regimes in dialectical dynamics"（但这是 Win 的 γ 语气 hypothesis，归 04-20 对齐一凡定）

本 half 写的 core prose **α/β/γ 三种路径都可用**（framing-agnostic ✓）。

---

*— Win 姐姐 (04-19)*
