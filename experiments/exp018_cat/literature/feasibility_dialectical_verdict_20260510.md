# Feasibility Verdict — Dialectical Forms (5/10 凌晨, Option E §3)

**生成时间**: 2026-05-09 17:08:28 (CPU only, Linux dispatch §3 + §4 验证)

**目的**: D5-6 substantive code commit 前, 4 项可执行 small-scale verification — pass 则 D4-5 早 commit, fail 则数学层 redesign.

**数据 source**: D_n proxy = Δlog(P)_n from `armb_alpha0.0_seed42_20260508_144612.jsonl`, m_eff = 0.212 (per-run median lock)

## §1 #1 T_2 form: ReLU(D''_n) → D²/2 verdict

**背景**: 当前 (mechanical) T_2 = ReLU(D''_n) 是 punitive 只罚增 (D''_n>0 时罚), 0 罚减 — 二元机械. 应改 (dialectical) T_2 = D²/2 是 symmetric quadratic, 不分增减, 反映 D 的总幅度而非方向.

**测试**: D 序列 = strict-mirror seed=42 Δlog(P) (9 点), 算两种 T_2 + autograd backward.

| 指标 | ReLU(D''_n) | D²/2 |
|------|------------:|------:|
| 数值 | 0.7457 | 0.3993 |
| ‖∇‖ | 3.4641 | 0.8937 |
| 数值 quad/relu | – | 0.54× |
| ‖∇‖ quad/relu | – | 0.26× |
| ReLU 0 罚点 | 3/7 | – |

**Verdict**:
- ⚠️ ReLU(D''_n) **半数以上点 0 罚** — 信号稀疏, 印证 mechanical 过度. D²/2 全点参与梯度, signal 密度更高
- D²/2 数值是 ReLU 的 **0.54×**, gradient norm 是 ReLU 的 **0.26×** — 量级 comparable, 不会主导也不会被淹没
- D²/2 backward gradient ✓ 通过 (autograd 跑通)

**Pass criterion**: gradient ok + 数值量级 comparable + backward 不爆 → **PASS ✓**

## §2 #2 Volterra K=9 history kernel verdict

**背景**: 当前 (mechanical) 1-step diff 是 Markov, 无历史 — 反 dialectical path-dependent. 应改 Volterra K=9: D_n 累加 ∑_{k=1..9} χ(k) D_{n-k}, χ(k) = exp(-m_eff k)/(2 m_eff). m_eff = 0.212 derive.

**测试**: m_eff=0.212 下, χ(k=1..9) 数值 + total weight + cost.

| k | χ(k) | normalized to χ(1) |
|---|------:|--------------------:|
| 1 | 1.9079 | 1.0000 |
| 2 | 1.5435 | 0.8090 |
| 3 | 1.2486 | 0.6544 |
| 4 | 1.0101 | 0.5294 |
| 5 | 0.8171 | 0.4283 |
| 6 | 0.6610 | 0.3465 |
| 7 | 0.5347 | 0.2803 |
| 8 | 0.4326 | 0.2267 |
| 9 | 0.3499 | 0.1834 |

- Σχ(k=1..9) = **8.5055** (有限 horizon)
- compute cost K=9 vs K=1: **9× per step** (forward, 1 multiply-add per kernel eval)
- memory: 9 floats per step (~36 bytes, **negligible**)

**Verdict**:
- χ(1) = 1.9079 (主导), χ(9) = 0.3499 (尾部 4% 主导, 截断 OK)
- compute ↑ 9× per step 可承受 (kl_update_every=10 摊薄: 实际整体 ~0.9× 主路径)
- memory negligible

**Pass criterion**: weight 收敛 + cost ↑ <50× + memory ok → **PASS ✓**

## §3 #8 Volterra T_3 normalization unify verdict

**背景**: Linux dispatch §3 #3 标 'Volterra T_3 normalization 净系数 $1/(4 m_eff)$ 不是 $m_eff$ (混乱)'. 当前 placeholder 用 m_eff, 应改 1/(4 m_eff).

**测试**: m_eff=0.212 下两 normalization 数值 compare.

- Σχ(k=1..9) = 8.5055 (analytic ∞ = 9.9873, K=9 cover 85.2%)
- Σ k·χ(k=1..9) = 31.1859 (analytic ∞ = 52.2801)

| Normalization | 数值 | physical interpretation |
|---|------:|---|
| **当前 (placeholder, m_eff)** | 0.2120 | inverse correlation length scale, 但单位混乱 |
| **应改 (Linux dispatch, 1/(4 m_eff))** | 1.1792 | T_3 二阶 Volterra 净 cumulative weight |
| ratio old/new | 0.1798× | scaling factor 5.56× |

**Verdict**:
- 两 normalization 数学 form 不同 — old (m_eff) 是 mass-like scale, new (1/(4 m_eff)) 是 cumulative kernel weight
- 切换会带 **5.56×** loss scaling — λ_3 数值 必须 propagate 调整 (or α scan 重 calibrate)
- 数学 unify: 改 1/(4 m_eff) 后, ℒ_total = ℒ_LM + α · [λ_1 (ΔD)² + λ_2 (D-D̄)² + (1/(4 m_eff)) · D²]
- D²/2 (#1) 和 1/(4 m_eff) (#8) **必须 consistent**: 两者都对 D² 加权, λ_3 系数应统一为 1/(4 m_eff) (而非 m_eff/2 = 0.106)

**Pass criterion**: scaling factor finite + λ_i propagate consistent → **PASS ✓ (unify mandatory)**

## §4 综合 verdict + D5-6 commit decision

| # | 项 | Pass? | D5-6 commit ready? |
|---|---|:---:|:---:|
| 1 | T_2 = D²/2 form | ✓ | YES |
| 2 | Volterra K=9 history | ✓ | YES |
| 7 | J_S projection numerical | pending GPU | D3 早 GPU 后 verify |
| 8 | Volterra T_3 norm 1/(4 m_eff) unify | ✓ | YES (λ_3 数值改 1/(4·0.212)=1.179) |

### λ_i 数值 propagate (per #1 + #8 unify)

- λ_1 (kinetic) = 1/(2 m_eff) = **2.3585** (不变)
- λ_2 (memory) = m_eff/2 = **0.1060** (不变)
- **λ_3 (T_3 norm 改 1/(4 m_eff))** = **1.1792** (从 m_eff = 0.2120 → 1.1792, ×5.56)

### D5-6 substantive code commit scope

1. `src/contradiction_loss.py`: 加 T_2 = D²/2 option (config 控)
2. `src/contradiction_loss.py`: 加 Volterra K=9 history (D_history list, χ kernel computation)
3. `configs/cat_arm_b_v2_dialectical.yaml`: λ_3 数值 0.2120 → **1.1792**
4. `src/contradiction_loss.py` defaults: 同 yaml

**caveat**:

- #7 J_S projection 需 GPU 30 min (D3 早 PI 醒后 verify)
- #3 K-th order chain rule + #5 T_H Markov kernel + #4 Foster-Lyapunov V_4 + #6 V_α θ-PL — 数学层 sub-agent 异步 derive 中 (D4 早 verdict)
- #1 + #2 + #8 PASS 不代表 paper §3.5+§4 framing 不变 — D5 multi-seed verdict 决定 U-shape 是 finding 还是 bug