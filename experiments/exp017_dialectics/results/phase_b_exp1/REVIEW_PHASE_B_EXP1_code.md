# REVIEW_PHASE_B_EXP1_code.md — Day 1 code review, 2026-04-15 afternoon

审查目标：`rust_variants/block_v_phase_b_exp1/{engine.rs, main.rs, Cargo.toml}` 对照
`WIN_PHASE_B_EXP1_TASKBOOK_20260415.md` §1-2 spec。

Reviewer: code-reviewer subagent (独立执行，不引用外部判断)。

---

## Summary verdict

**存疑 — 代码 can proceed to Day 2 run, but 4 个 interpretive divergences 必须被
Day 2 解读时显式 caveat**。没有 P0 blocking bug（PDE 推导、feedback 项、parallelism
都正确），但 **history kernel 的归一化 (P0-#4)** 与 **entropy production 的定义
(P1)** 与 taskbook 字面公式不一致，属于 implementation choice 而非 typo，需在
verdict 中交代以免 over-claim。Day 2 数据本身有效。

---

## P0 checks

### 1. PDE factor 2 verification  ✓

独立推导（Wirtinger w.r.t. ψ*, treating ψ, ψ* independent）：

- V = (|ψ|² − v²)² = (ψψ* − v²)²
- ∂V/∂ψ* = 2(ψψ* − v²) · ∂(ψψ*)/∂ψ* = 2(|ψ|² − v²) · ψ

拆实/虚：设 ψ = a + ib。gradient-flow EOM `γ ∂_t ψ = −∂V/∂ψ* + ...`
对 ψ* 求导等价于对 (a, b) 求半次 energy gradient：
- ∂V/∂a = 2(|ψ|²−v²)·2a = 4a(|ψ|²−v²)
- γ ∂_t a = −(1/2) ∂V/∂a = −2a(|ψ|²−v²)   ✓ 与 engine.rs:357 `drive_coef = 2.0 * (mod2 - v2)` 一致

engine.rs:318-319 docstring 也写对了。**✓ factor 2 正确，无 Wirtinger invisible
陷阱**。（Phase 1 的 n=2 陷阱是把 `psi.powu(2)` 误当 `psi·ψ*`；这里用实/虚分离
写法，没有机会犯那个错。）

### 2. Feedback term correctness  ✓

engine.rs:241-270 `recompute_effective_source`:
- Step 1 (244-250): ma, mb 为**空间均值** ⟨a⟩_x, ⟨b⟩_x ✓（求和除以 N = G³）
- Step 2 (252-255): `scratch_da = a - ma` = ψ − ⟨ψ⟩_x ✓（空间均值，非时间均值）
- Step 3 (257-262): δS_history = HistoryBuffer::weighted_sum_into(λ) ✓
- Step 4 (264-269): sa = s0a + α·Δa + β·δS_a ✓ 与 spec `S = S₀ + α·(ψ−⟨ψ⟩_x) + β·δS` 完全对应

**✓ 结构正确。Δψ 明确是空间而非时间去均值**（后者会导致 δS 与 Δψ 重复扣均值）。

### 3. History exp-decay kernel units  ✓（但隐式依赖 main.rs 推送频率）

spec: w_k = exp(−λ · k · Δt_outer), λ = 0.05, Δt_outer = 1.0 → w_k = exp(−0.05·k)

engine.rs:158 `w = (-lambda_dt * k as f32).exp()` 传入参数 `lambda_dt`;
engine.rs:257 `lambda_dt_unit = params.lambda_hist = 0.05` 直接传入，
main.rs:18-20 的 docstring 也显式声明 "lambda_hist = λ · Δt_outer = 0.05"。

单位对齐取决于 **push 频率**。main.rs:222 `if step % outer_every == 0 { push_history }`
with outer_every = 100 (main.rs:310), dt_inner = 0.01 → 每推一次真实时间间隔
Δt_outer = 1.0。

**✓ push 频率 (每 100 inner steps) × dt_inner (0.01) = Δt_outer (1.0)，
与 spec k·Δt_outer 的离散化一致**。control_single 模式 (multi_scale()=false) 根本
不 push history，β 项永远是 0，也 OK。

### 4. δS_history normalization interpretation  — **divergence from spec, non-blocking**

spec §1.2: `δS = ∫ w(t−t')·Δψ(t') dt'` — **积分，无归一化**。
实现 (engine.rs:167-171):
```
let inv_w = 1.0 / total_w.max(1e-12);
for i in 0..N { out_a[i] *= inv_w; out_b[i] *= inv_w; }
```
这是 **Σw·Δψ / Σw** （加权平均），不是 Σw·Δψ（加权积分）。

**后果**：
- 物理 scale 差 ≈ Σ_{k=0}^{99} exp(−0.05k) ≈ (1−e^{−5})/(1−e^{−0.05}) ≈ 0.993/0.04877 ≈ 20.36
- 即实现中的 β 作用强度 ≈ spec 的 β/20.36。
- 实验 β=0.05 → 等效 spec-scale β ≈ 0.00246。**feedback-history 贡献被压 ~20 倍**。

**但是**：当 history 未满 (len < 100)，归一化后 δS 的 scale **不随 len 变化**，而
原 spec 下 δS ∝ len 从 0 linearly 长到满。归一化 **让启动瞬态更平滑，且让 β
的语义从 "cumulative memory strength" 变为 "mean memory deviation weight"**。

**判定**：这是 interpretation choice（符合 spec §1.2 注释 "数值稳定的
exponential-weighted moving average"），**非 typo / bug**。

**建议修正**：
- (a) Day 2 verdict 中显式说明 β 的有效 scale（写出 `β_eff = β/Σw ≈ β/20.36`），
  避免与 spec 字面 β 值搞混；
- (b) 若 O2 enthroopy 出现 dS/dt → 0 (fail pattern) 提示反馈不够强，
  **第一件要试的事就是把 β 乘回 Σw ≈ 20**（等价于切到 un-normalized kernel）——
  不是重设计，而是 re-tune；
- (c) 若写论文，normalized kernel 应被称为 **exponentially-weighted moving average
  (EWMA) on ψ deviations**，不再是 "积分 history"。

### 5. Outer-loop ordering  — caveat

main.rs:212-239 per-step sequence:
```
1. (if step % 10 == 0) block_average_source(2)        // coarse-grains CURRENT sa/sb
2. evolve_inner_step(dt_inner)                        // 用上一轮 recompute 的 sa
3. recompute_effective_source()                       // 基于 post-evolve ψ 重算 sa
4. (if step % 100 == 0) push_history()                // 把刚算的 scratch_da push
5. (if step % obs_every == 0) log observables
```

**问题 1**：step==0 第 0 次 evolve 时，sa 由 main.rs:200 `eng.recompute_effective_source()`
预热给定 (基于 init ψ, empty history)。✓ 无 read-before-init 错误。

**问题 2**：step % 10 == 0 的 block_average 对 **上一 step recompute 完成的 sa**
作 coarse-grain，然后紧接着 evolve 会用这个 coarse-grained sa 产生新 ψ，之后
立刻 recompute 又会把 sa 重置为 fine-grained（S₀ + α·Δψ + β·δS）。**block_average
的效果只在当前 step 的 evolve_inner_step 里生效一次，随后被 step 3 的
recompute 擦除**。

**结论**：middle-loop coarse-graining 每 10 步只"冲击"一次 evolve；其后 9 步
用 fine-grained sa。等价于**以 10% 占空比施加一次 block-smoothed 冲量**。
这**不等同于** spec §1.3 "每 10 步重新归一化 S 的粗粒度结构" 的自然解读
(可能是 "coarse-grain 后维持到下次 coarse-grain")。

**判定**：存疑 — 是 intentional 还是 bug 需 Win/一凡确认。
- 若 intentional："RG 冲击注入" — 每 10 步让 S 结构被粗粒化平滑一次；
- 若 bug：应把 middle-loop 改为 "coarse-grain base source S₀ 每 10 步"（
  而非 effective S）；或把 coarse-grain 放在 recompute_effective_source **之后**，
  使一整个 middle-cycle 期间 sa 保持 block-constant。

**建议**：加 `[?] middle-loop semantics` 到 queue，default 保持当前实现；
Day 2 O3 RG self-similarity 测试结果会对此敏感。

### 6. Initial history state caveat  — acknowledged

前 99 inner steps (step=1..99) 时 hist.len=0 → weighted_sum_into 返回 0-填充
(engine.rs:151-153) → β 项贡献 0。从 step=100 起第一个 snapshot 入 buffer，
δS = 1 · Δψ(100 Δt 前) (归一化后 = Δψ 本身)。buffer 至 step=9900 才满。

5000 inner steps 内 hist 最长只有 50 条 (5000/100=50) — **N_hist=100 buffer 永远
填不满！！！** 这是一个 **subtle 但重要的事实**：

- Spec §1.2 `N = 100` 指 "历史窗口长度"（snapshots），w_k 最远回望 100 个 outer-step；
- 但实验只跑 5000 inner steps = 50 outer-steps → **实际只用 buffer 的前半**；
- 归一化的存在使这 "未满 buffer" 影响不严重（Σw 仍正常）。

**判定**：non-blocking，但需在 verdict 里记一笔 "N_hist=100 under-utilized (50/100)
in 5000-step run"。若第二轮扩到 10000+ steps 才能 fully 激发 N=100 窗口。

### 7. Seed determinism  ✓

engine.rs:222 `let mut rng = seed | 1;`:
- seed=20260421 is odd (末位 1) → `seed | 1 = 20260421` ✓ no-op
- main.rs:301 `seed_base.wrapping_add((i as u64).wrapping_mul(17))`: i=0 → 20260421,
  i=1 → 20260438 (even → `|1` → 20260439), i=2 → 20260455 (odd), ...
- 每 doc 独立 seed，不同 doc 不会重复。

xorshift64 在 seed=0 下 degenerate (全 0)，`| 1` 正是防此；20260421 非 0，OK。

**✓ 无 seed bug**。

### 8. Parallelism safety  ✓

main.rs:295-315 `docs_use.par_iter().enumerate().filter_map(...)` → 每 closure 内
`let mut eng = Engine::new(params)` → 独立 Engine instance, 独立 history buffer,
独立 scratch, 独立 rng。无 shared mutable state。结果 vec collect 是 rayon
standard pattern。

**✓ parallelism safe**。32 threads (main.rs:244-247) 与 70 docs 合理（~2.2 docs/thread）。

---

## P1 suggestions

### P1-1. Performance sanity — 合理，不是偷懒

naive 估计：`recompute_effective_source` per inner step ≈
- spatial mean: 2N = 65536 ops
- Δψ: 2N
- weighted_sum_into: len × 2N ops (每个历史 snapshot 遍历 N 体素 × 2 field)
- effective S: 3·2N

per step cost ≈ (len + 5) · 2N。len 从 0 长到 ~50。平均 ~27 · 2N ≈ 1.77M float-ops。

5000 steps × 10 docs × 1.77M = 88.5 Gops (只算 recompute)。加 evolve_inner_step
~10·N = 0.33M per step → 5000·10·0.33M = 16.5 Gops。block_average every 10 steps
可忽略。

**total ≈ 105 Gops / 10-doc run**。32 threads × ~5 GFLOP/s/thread (scalar f32) ≈
160 GFLOP/s → 0.66 s 理论，实测 7.5s — 合理（包含 I/O, 启动开销, 内存带宽 bound
on 26 MB history buffer per engine）。

**✓ 性能匹配规格，没有 silently skipped computation**。

### P1-2. `block_size=2` on G=32  ✓

main.rs:311 `block_size=2` → 16³ = 4096 blocks on 32³=32768 voxels。block_average_source
(engine.rs:280-315) 正确处理 nb = G/block = 16，index arithmetic OK。若改 block=4
则 nb=8 也兼容。

### P1-3. control_const/null 模式 dead-code push_history

main.rs:222 `if mode.multi_scale() && step % outer_every == 0` — null 与
control_const 是 `multi_scale=true`（只有 control_single 是 false）, 所以 null
和 control_const **依然 push history** 并消耗 26 MB × N_docs 内存 + 计算 weighted_sum。

由于 β=0 (EngineParams::null_test)，weighted_sum 的结果在 recompute 里乘 β=0 归零，
**功能上正确但有 ~20% 计算浪费 + 内存浪费**。

**建议**：在 Engine::new 里 if beta==0.0 则 `cap=1` minimal buffer, recompute 内
`if self.params.beta == 0.0 { skip weighted_sum_into }`。non-blocking。

### P1-4. `entropy_production_rate` 定义 — divergence from taskbook §2 O2

taskbook §2 O2 写的是 `dS/dt = ∫ (∇V · ∇ψ)² / γ dx + noise contribution term`。
这个表达式**量纲上不自洽**：∇V = ∂V/∂ψ* 是场空间方向的梯度（不是空间 ∇_x）；
这里混淆了 functional derivative 与 spatial gradient。更可能 Win 想写的是

- **正确 overdamped entropy-production**：
  - Seifert 2005：`σ = ⟨F·v⟩/T = (1/γT) ⟨|F|²⟩`，F = −δH/δψ + S(x,t) 是非保守力，
    v = ∂_t ψ = F/γ (noise-free limit)；
  - noise-free: `σ = (1/γ²T) · ⟨|F|²⟩ = (1/γT) · ⟨|∂_t ψ|²⟩ · γ = ⟨|∂_t ψ|²⟩/T`
    (up to constants)；
  - 即 **entropy production ∝ |dψ/dt|² 的空间积分**。

engine.rs:413-446 计算的是 `(1/N) · Σ_k |RHS(k)|²` where RHS = D∇²ψ − 2ψ(|ψ|²−v²) + S。
这 **等于 |∂_t ψ|²** (because γ ∂_t ψ = RHS with γ=1) — **正是 Seifert-style
overdamped entropy production rate up to constant T**.

**判定**：
- (a) taskbook §2 O2 公式是 typo/shorthand，`∇V·∇ψ` 应读作 `(δH/δψ*) · (∂_t ψ)`
  或直接 `|∂_t ψ|²`；
- (b) engine 的 `(1/N) Σ |RHS|²` **正确保留了 "开放耗散 dS/dt > 0" 的定性信号**
  （是正定量），且对 fail pattern dS/dt → 0 / unbounded 都能诊断。
- (c) 但严格来说它 **缺 noise contribution** — noise=0 (deterministic PDE)，所以
  这 term 本身就 0，**OK**。

**✓ 实现 defensible；taskbook 公式需 Win 在 verdict 里 clarify**。

### P1-5. `free_energy` coupling term 在 exp 模式下有歧义

engine.rs:450-474 计算 E = ∫ [D/2·|∇ψ|² + (|ψ|²−v²)² − (a·Sa + b·Sb)] dx。

problem：Sa 在 exp 模式下 **时变** (含 α·Δψ(t) + β·δS_hist(t))，所以 `−ψ·S` 不是
真正的 thermodynamic coupling (后者需 S = δH_ext/δψ* 为 external **fixed** field)。

**后果**：`free_energy` time series **不是严格单调减**（即便 noise-free），因为 S
本身被 ψ 反馈；能量可以 "泵入"。这 **正是 open dissipative 的预期行为**，但命名
`free_energy` 有误导性。

**建议**：
- Day 2 verdict 里把此 observable 称 "instantaneous Lyapunov functional (with
  current S)"，不是真正 free energy；
- 看 E 时序 **不稳定下降** 是 expected（洞见 3 "开放耗散"），不是 bug。

---

## P2 polish

### P2-1. docstring 的不完整注释

- engine.rs:257 `// per-step λ·Δt already folded — see main.rs` — 说法略粗糙，
  可以改成 "lambda_hist value is (λ · Δt_outer) product, NOT bare λ — see main.rs:18-20"。
- engine.rs:413-422 docstring 声称 "using the most recent inner step ..." 但实际
  代码是 re-evaluate RHS at current state — docstring 与代码 mismatch 程度大，
  容易 misleading 读者。改成 "computes γ²|∂_t ψ|² as the square of the current
  deterministic RHS"。

### P2-2. `init_psi_near_minimum` 的 θ 分布

engine.rs:225 `theta = rand_unit() * π` → θ ∈ [−π, π]，但 `rand_unit` (engine.rs:66-69)
实际返回 [−1, 1] → θ ∈ [−π, π]。OK 均匀遍历 U(1)。但 r = v + 0.1·rand_unit → r ∈
[0.9, 1.1]，正常。**但 no guarantee r>0**；若极端 v 小 + clamp_abs 小 could go negative。
v=1 下安全。non-blocking。

### P2-3. CSV 输出 missing

Deliverable §5 要求 `phase_b_exp1_observables.json` ✓, `phase_b_exp1_states.bin` ✓,
`phase_b_exp1_vs_control.json` ❌ (需 post-processing 脚本，main.rs 只输出
per-mode 文件)。non-blocking，是 Day 2 work。

### P2-4. edition = "2024"

Cargo.toml:4 `edition = "2024"` — 需 Rust 1.85+ (stable since 2025-02)。在 2026-04
环境中应可用，但 nightly 依赖若有需注意。没发现 unstable feature 使用，OK。

### P2-5. clamp_abs=3.0 vs v=1

engine.rs:361 `.clamp(-3.0, 3.0)` → |ψ|² 上限 ≈ 18, 远大于 Mexican hat 底部 |ψ|²=1，
给 soliton / localized structure 的 overshoot 留了头顶空间 ✓。但**若 localized
structure 要求 |ψ| ≫ v 才能 localize (e.g. gray soliton depth)**，clamp 会截断。
可检查最终 states 中 |a|, |b| 接触 3.0 的 voxel 比例；若 >1% 需调大。
Day 2 diagnostic 建议加 max |ψ| 到 observables。

---

## Blocking / non-blocking 分类

**Blocking (必改才能跑 Day 2)**：
- 无。

**Non-blocking but 必须在 verdict 里 caveat** (否则 over-claim 风险)：
1. P0-#4 **δS_history normalization** — β 有效 scale 是 `β/20.36`，不是字面 β；
2. P0-#5 **middle-loop coarse-graining ordering** — block_average 立刻被 recompute
   擦除，只"冲击"一次 evolve；O3 RG self-similarity 对此敏感；
3. P0-#6 **N_hist=100 under-utilized** — 5000 inner steps 只累 50 snapshots (50%);
4. P1-#4 **entropy_production 定义** 与 taskbook 字面不一致，实现采用 Seifert-style
   `|∂_t ψ|²` — 需在 verdict 声明 "we interpret O2 as Seifert overdamped entropy
   production rate";
5. P1-#5 **free_energy 在 exp 模式下非严格单调** — 是 expected，不是 bug。

**Nice-to-have (第二轮优化)**：
- P1-#3 dead-code push in null/control_const；
- P2-#1 docstring mismatch；
- P2-#5 clamp_abs diagnostic。

---

## Closing note

Day 1 Rust 实现整体质量 **solid**：PDE 物理项推导正确，Wirtinger n=2 invisible
陷阱没有复发；feedback 与 history 结构化清晰；parallelism 与 determinism 无问题。
**可以跑 Day 2 全量 70-doc × 5 modes 实验**。

唯一需要 Win / 一凡 在 Day 2 解读前 clarify 的是 P0-#5 middle-loop ordering 的
intended semantics — 建议打 `[?]` 到 queue，当前实现下 verdict 先用 "每 10 步
RG-shock" 语言描述。其余 4 条 divergence 不影响 empirical 结果，只影响叙述精度。

参数 scan 建议（第二轮，若 O2 触发 dS/dt → 0 fail pattern）：
- **第一选项**：把 β 乘回 Σw ≈ 20 (i.e. β_new = 1.0) 而非重改 α；这是 normalization
  choice 的直接 counterfactual；
- 第二选项：扩到 10000+ inner steps，让 N_hist=100 window 被填满。

— code-reviewer subagent, 2026-04-15
