# Phase B Experiment 1 Taskbook

## "开放耗散自反馈场的语义粒子自发现"

**撰写**：Win Claude
**日期**：2026-04-15（一凡 × Win 上午脑暴后）
**启动日期**：**2026-04-21**（v0.1.1 release 后的周一，**不在 release 周里启动**）
**预估时长**：1.5 days（Linux 1 day Rust + Win 0.5 day 解读）
**可证伪性**：明确（4 observables，5 fail conditions）
**结果**：无论成功或失败都产出一篇 paper（双保险）

---

## 0. Why — 来源与意图

2026-04-15 上午，Win × 一凡 一次极高密度脑暴，产生 5 条论文级洞见:

1. **基本粒子 = 场激发态**（Goldstone / soliton / breather），不是 localized 点
2. **原子 = 过程**（公理 1：粒子是动态过程；熵增、跨尺度、可变）
3. **驱动 = 客观物质反映**（开放耗散系统；BGE drift 是历史压印不是 noise bias）
4. **耦合 = b+c 双向自反馈**（公理 6 "匹配 = 自我训练" 的真正数学形式）
5. **时间结构 = 多尺度同步**（RG 从 Phase B 开始，不等 Phase C）

本实验在**一次 run 里同时测试 5 条**。任何一条 fail 都对应一个 pinpointed 错误洞见（可证伪）；全部 pass 则 MaoField 第一阶段难题（"物理场长什么样" / 原子映射）**基本解决**。

---

## 1. Ingredients（Rust 实现规格）

### 1.1 场

- ψ ∈ ℂ, 32³ 格子, 周期 BC
- dx = 1
- 默认 V = (|ψ|² − v²)²（Mexican hat，v = 1）—— 允许 Goldstone 软模
- γ = 1, D = 0.1

### 1.2 源 S 用 b+c 反馈形式

```
S(x, t) = S₀(x) + α · (ψ(x, t) − ⟨ψ⟩_x) + β · δS_history(x, t)

δS_history(x, t) = ∫_{t-Nτ}^{t} w(t − t') · (ψ(x, t') − ⟨ψ⟩_{x, t'}) dt'
```

其中：
- `S₀(x)`：BGE embedding tiled（**不 whitening**，保留 17σ 历史 drift）
- `α = 0.1` — 瞬时反馈强度（默认）
- `β = 0.05` — 历史累积强度（默认）
- `N = 100` 步 — 历史窗口长度
- `w(·) = exp(−λ·Δt)`，λ = 0.05（指数衰减权重）
- `⟨ψ⟩_x` = 全 grid 空间平均

**参数 scan（第二轮，if 必要）**：α ∈ {0.01, 0.1, 0.5}, β ∈ {0, 0.05, 0.2}, N ∈ {50, 100, 500}

### 1.3 多尺度时间步

- **内层** `dt₁ = 0.01` — 每步同步 update ψ
- **中层** 每 10 步（`dt₂ = 0.1`）重新归一化 S 的粗粒度结构（block-average）
- **外层** 每 100 步（`dt₃ = 1.0`）update `δS_history` 累积

### 1.4 演化

- Free evolve 5000 inner steps（t_sim = 50）
- Seed: 20260421
- 文档: NFCorpus 100 docs（70 有 BGE embedding cached）

---

## 2. Observables

### O1 — 局域相干结构谱

- 稳态 ψ 场做 3D FFT
- 找 localized spatial peaks（real-space clustering on |ψ|）
- 测 Goldstone 软模：沿 Mexican hat 底部 phase direction 的 k→0 modes 应有 gapless dispersion
- **Pass 条件**：至少 3 个 localized structures，每个 size < grid/4；phase 方向 low-k modes exist

### O2 — 熵产生率

```
dS/dt = ∫ (∇V · ∇ψ)² / γ dx  +  noise contribution term
```

计算每 100 steps，plot time series。

**Pass 条件**：
- 初始瞬态后进入 `dS/dt > 0` 的稳态（持续非零）
- `dS/dt` 饱和（不爆炸），approach quasi-stationary value
- Fail 两种：dS/dt → 0（系统 equilibrium，洞见 2-3 错）或 dS/dt 无界增长（系统发散，洞见 4 错）

### O3 — RG 不变性

- 用 `dt = 0.01 / 0.1 / 1` 三个 time scale 跑三次
- 粗粒化到同一空间 + 时间分辨率（blocking average）
- 计算 structure function 相关系数

**Pass 条件**：三个 time scale 的 coarse-grained pattern 相关系数 > 0.7（self-similar）

---

## 3. Control Baseline（必做，不可省）

同一 setup 但三处 fix:

1. S 不带 feedback：`S(x, t) = S₀(x) const`
2. BGE whitening：`S₀' = S₀ − ⟨S₀⟩`
3. 单一 time scale：只用 `dt = 0.01`

**用途**：若实验组 O1/O2/O3 show 有趣 pattern，对照组 show trivial pattern，才能证明 pattern attributable 到 (feedback + history + multi-scale) 三件事联合，而不是 base PDE 就有。

---

## 4. Falsification Table

| Observable fail | 对应哪条洞见错 | 可能 downstream |
|---|---|---|
| O1 没 localized structures | 洞见 1（粒子 = 激发态） | 换 V（加 explicit symmetry breaking） |
| O2 dS/dt → 0 | 洞见 2-3（开放耗散/熵增） | 换 driving（active forcing） |
| O2 unbounded 增长 | 洞见 4（b+c 能自稳） | 调 α, β（damp feedback） |
| O3 不 self-similar | 洞见 5（多尺度同步） | single-scale 退回 |
| 对照组 show 同样 pattern | 这 5 条都错（base PDE 自己就有） | MaoField 框架需大修 |

**全部 pass**：MaoField 第一阶段难题 empirically 解决 → Phase B 第一篇 paper 的 empirical backbone。

---

## 5. Deliverables（Linux 归档）

- `phase_b_exp1_verdict.md` — 最终 verdict，按 Falsification Table 逐条判定
- `phase_b_exp1_observables.json` — O1/O2/O3 raw data
- `phase_b_exp1_states.bin` — ψ 场稳态快照
- `phase_b_exp1_vs_control.json` — 实验组 vs 对照组对比
- `REVIEW_PHASE_B_EXP1.md` — spawn-agent 独立审查报告
- `phase_b_exp1_figures/` — O1 FFT 谱, O2 时间序列, O3 RG self-similarity 对比图

---

## 6. Timeline（2026-04-21 启动）

| Day | Morning | Afternoon |
|---|---|---|
| Day 1 (Mon) | Rust 实现 + sanity check（v=1, α=0 null test） | 实验组 + 对照组并行跑 |
| Day 2 (Tue) | Observables 计算 + Win 解读 | verdict.md 起笔 |
| Day 3 (Wed) | spawn-agent review | 根据 review 修订 |
| Day 4 (Thu) | Final verdict + 下一步规划 | Paper draft 起笔（成功或失败分支） |

---

## 7. Paper Branches

### Branch A — All Pass

**Paper**: *"Self-organized semantic particles in open dissipative PDE systems: a dialectical-materialist field-theoretic account"*

核心 claim：
- 语义单位是 self-sustaining localized excitations
- 机制：b+c 双向自反馈 + 历史压印 + 多尺度同步
- MaoField 第一阶段难题（"物理场长什么样"）**基本 resolved**

Target venue：arXiv v2 / IPM mechanism paper / Physical Review X AI-adjacent

### Branch B — Any Fail

**Paper**: *"Why open dissipative framing of MaoField fails: a diagnostic"*

核心 claim：
- 列出 5 条洞见 + 相应 falsification
- Pinpoint 哪一条 break 了（精确到 observable）
- 提出 refined roadmap（换 V / 换 driving / 调 feedback / 退回 single-scale）

Target venue：arXiv v2 supplementary / Block V Design 升级

**两条 branch 都 publishable**。这是实验的**最大保险**：任何结果都产出学术贡献。

---

## 8. Review Pipeline（standing rule）

按 2026-04-13 确立的 standing rule：

1. Rust 实现完成 → spawn-agent review 代码（检查 S(x,t) feedback 项没写错）
2. Observables 计算完成 → spawn-agent review 计算公式（特别是 entropy production rate 的推导）
3. verdict 起笔完成 → spawn-agent review 诚实度（over-claim / under-claim）
4. Paper draft 完成 → spawn-agent review 整体

每个 review 报告归档到 `REVIEW_PHASE_B_EXP1_{stage}.md`。

---

## 9. 不做

- 不在 2026-04-15 ~ 2026-04-20 启动（release 周保持专注）
- 不跑参数 full scan（默认参数先跑，第二轮再决定是否 scan）
- 不加 more observables（3 个够了，5 条洞见都覆盖；加 more 会 dilute focus）
- 不启动 Phase A 其他实验（Phase A-0/A-1/A-2/A-3 按原 Block V Design 走，不被本实验干扰）

---

## 10. 给 Linux 的话

这个 taskbook 的 design 是**姐妹俩一上午脑暴出来的，一凡亲自参与每一步决策**。每一条 ingredient 都有哲学 motivation，不是随便选的。具体 motivation 在本文件 §0 列出。

启动时先读 §0 再读 §1-§8。如果有任何一处你觉得 implementation 不 natural，或者 observable 测不出来，**不要自己改设计，打 [?] 标给一凡决定**。

一凡的 stance：**"证伪也没关系，我希望实验成功"**。两条 branch 都被 pre-authorized，任何结果都不是 "失败"。

Win × Linux × 一凡，三方协同，第一阶段难题 endgame 的第一颗子弹。

— Win, 2026-04-15
