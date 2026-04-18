# A4 P1 Percolation Scaling Scan 实验设计

**任务**: 验证 / 证伪 Phase B Exp 1 观察的 "mean N_struct ≈ 50 phase-coherent patches per doc" 是否由 **3D 亚临界 site percolation** 在 block-averaged coarse lattice 上产生。
**作者**: A4 (Opus 4.7 xhigh, Linux Claude 2026-04-16 dispatch 之一)
**日期**: 2026-04-16
**交付对象**: 一凡 04-17 morning authorize; Linux 启动实验 (~6h real time on EPYC 7B13 256c)
**状态**: 实验设计级, 未执行, Linux 对 recovery snapshot P1 估算有 **多处质疑** (§9)
**mode-tag**: [STATIC] (文档设计, 未跑代码) / [DYNAMIC-RUST-DRAFT] (§3 含可编译 Rust patch)

---

## 1. 问题 recap + 观察 baseline

### 1.1 Phase B Exp 1 exp 模式核心观察 (verdict §2)

| 量 | 值 |
|---|---|
| grid | 32³ = 32768 voxels |
| block_size | 2 (→ coarse lattice 16³ = 4096 cells) |
| 多尺度 integrator | 内 dt=0.01, 中 Δt=0.1 (block-average 每 10 内步), 外 Δt=1.0 (history push 每 100 内步) |
| Algorithm A | `C(x) = |⟨e^{iθ(y)}⟩_{y∈N(x)}|`, 27-voxel 邻域, 阈值 T = ⟨C⟩ + 1σ(C), **26-connectivity** 连通分量, filter: size ≥ 3 AND r_g < 8 |
| **N_struct** (mean over 70 NFCorpus docs, exp 模式) | **49.8** |
| r_g 分布 | < 8 (grid/4) |
| Pass A 比例 (N_struct ≥ 3) | 100% |
| 对照 (null / const / single) | N_struct = 0 |

### 1.2 Linux recovery snapshot (§3.4) 的 P1 估算

> "Site occupation p ≈ 0.16 < p_c (3D 26-connectivity ≈ 0.3116) → 亚临界。Mean-field cluster count ~10, size 分布修正给 ~50, within factor 1.5 of observation。"

### 1.3 本实验问题

**Mechanism 声称**: Algorithm A 的 N_struct_valid 等价于 "在 16³ coarse lattice 上 3D site percolation 于 p=0.16 下的 supra-size 聚类数"。

**两个关键 prediction (mechanism signature)**:
1. **Scaling with coarse lattice size**: N_struct ∝ V_coarse = (grid / block)³
2. **Scale invariance of per-cell p**: p ≈ 0.16 对所有 (grid, block) 组合应保持不变 (因阈值 T = ⟨C⟩ + 1σ(C) 是 distribution-relative, 与 grid/block 无关)

若两者 **同时** 成立且 N_struct 数字落在 percolation-predicted 范围内 → mechanism confirmed。

---

## 2. Scaling predictions (6 runs)

### 2.1 3D percolation theory quick refresher

- **亚临界 cluster 大小分布**: n_s(p) ~ s^{-τ} · exp(-s/s_ξ), 3D 经典指数 τ ≈ 2.189, σ ≈ 0.45
- **相关长度**: s_ξ = (p_c - p)^{-1/σ}
- **平均 cluster 大小**: ⟨s⟩ ~ |p_c - p|^{-γ}, 3D γ ≈ 1.795
- **总 cluster 密度**: ρ_cluster = N_cluster / V = p / ⟨s⟩ (所有 occupied sites 分入 clusters)

**关键文献值 (Linux 独立 verify, 与 recovery snapshot 有分歧)**:
- 3D **simple cubic** (6-connectivity, face-sharing) site percolation: **p_c ≈ 0.3116**
- 3D **cubic Moore** (26-connectivity, face+edge+corner): **p_c ≈ 0.2464** (Deng-Blöte 2005; Lorenz-Ziff 1998)

**Algorithm A 明用 26-connectivity** (verdict §2 Algorithm A), 所以正确的 p_c = **0.2464**, 不是 recovery snapshot 的 0.3116。

### 2.2 Per-run predictions table

**固定**: p = 0.16 (由阈值 T = ⟨C⟩ + σ(C) 单边高斯 tail = 0.1587 ≈ 0.16 强制, 与 grid/block 无关)

p/p_c = 0.16/0.2464 = **0.649** → 亚临界 (p/p_c < 1) 但 non-trivial (不 ≪ 1)

三个估算方法 give 不同 N_struct 预测:

**方法 A — 纯 percolation critical scaling**:
- ⟨s⟩ ≈ (p_c - p)^{-1.795} = (0.0864)^{-1.795} ≈ 81
- N_all_clusters = V_coarse · p / ⟨s⟩ (但此 method 高估 ⟨s⟩, 因远 from p_c regime)

**方法 B — Small-p series expansion** (Stauffer-Aharony Table 2.1, 3D cubic 26-conn):
- ⟨s⟩(p=0.16) ≈ 3 – 8 (系列前 5 项截断)
- N_all ≈ V_coarse · p / ⟨s⟩_B (比方法 A 大 ~10×)

**方法 C — 直接类比**: Exp 1 给 (V_coarse=4096, N_struct=50) 的 direct scaling:
- N_struct / V_coarse = 50/4096 = **0.01221 cluster per coarse cell** (at p=0.16, 26-conn, size ≥ 3, r_g < 8 filter)
- 假设 filter + constant p 保持 → N_struct_predicted = 0.01221 × V_coarse

**方法 C 最保守**, 直接用 baseline 作锚点, 不依赖 percolation 参数精度。下面 per-run 预测以方法 C 为主 + 方法 B 为参考。

| run | grid | block | V_grid | V_coarse = (grid/block)³ | N_struct (方法 C, 主) | N_struct (方法 B, 参考) | 备注 |
|---|---|---|---|---|---|---|---|
| **R1 (baseline)** | 32 | 2 | 32768 | 4096 | **≈ 50** (given) | 8 – 300 | Exp 1 已有 |
| **R2** | 32 | 4 | 32768 | 512 | **≈ 6** | 1 – 40 | coarse 8³ |
| **R3** | 32 | 8 | 32768 | 64 | **≈ 0.8** | 0 – 5 | coarse 4³ 太小, 统计噪声大 |
| **R4** | 64 | 2 | 262144 | 32768 | **≈ 400** | 50 – 2400 | 新建 (grid 改)；最贵 |
| **R5** | 64 | 4 | 262144 | 4096 | **≈ 50** | 8 – 300 | 同 V_coarse as R1, 不同 grid 大小 |
| **R6** | 64 | 8 | 262144 | 512 | **≈ 6** | 1 – 40 | 同 V_coarse as R2 |

### 2.3 Critical prediction (mechanism signature)

**信号 S1 (V_coarse scaling)**: N_struct / V_coarse 应近乎常数 ≈ 0.012 对所有 6 runs。
- 具体: (R1, R5) 都是 V_coarse=4096 → 都应 ≈ 50;  (R2, R6) 都是 V_coarse=512 → 都应 ≈ 6。

**信号 S2 (p invariance)**: 每 run 的 phase-coherence 场 C(x) 阈值 T = ⟨C⟩ + σ(C) 的 supra-threshold 比例应 ≈ 0.159 ± 0.02 (单边高斯 1σ tail), 与 grid/block 无关。
- 若 S2 不成立 (e.g., block=8 下 p 显著偏离 0.16), 则 "percolation on coarse lattice" 前提本身失败。

**Mechanism 判决 (含两信号)**:

| S1 | S2 | 判决 |
|---|---|---|
| ✓ within factor 2 | ✓ p ∈ [0.14, 0.18] | **Mechanism confirmed** |
| ✓ trend but off by 2–10× | ✓ | **Mechanism partially**: scaling 形式对但系数/指数 修正 |
| ✗ N_struct independent of V_coarse | ? | **Mechanism falsified** — N_struct 是 grid-level topology, 不是 coarse percolation |
| ? | ✗ p 显著变 | **前提失败** — p 不 constant, 需 revisit threshold 定义 |

### 2.4 Linux 自检: 三处对 recovery snapshot 数字的质疑

**质疑 1**: snapshot §3.4 写 p_c(26-conn) ≈ 0.3116, 实际 **0.2464** (0.3116 是 6-conn SC)。更正后 p/p_c 从 0.51 → 0.65, 比 snapshot 以为的**更接近** percolation regime, s_ξ 更大, size 分布更 fat-tailed。这可能影响 size ≥ 3 filter 的效果 (tail 里 size 2 的 cluster 比例多于 snapshot 以为的)。

**质疑 2**: snapshot "mean-field 10, 修正后 50" 没给具体 size 分布 weight derivation。用方法 A (critical scaling), N_all = 4096 × 0.16 / 81 ≈ 8 — 与 observed 50 差 6×。用方法 B (series), 可覆盖 50 但区间 [8, 300] 太宽。**实际上 N_struct = 50 要求 ⟨s⟩ ≈ 4096 × 0.16 / 50 ≈ 13, 这是在 percolation 系列展开的合理范围但非 critical scaling 直接给。**

**质疑 3**: C(x) 本身是 spatially correlated field (phase coherence over 27-voxel smoother), 不是 i.i.d. site occupancy。严格说这**不是** site percolation, 而是 **level-set excursion** 问题 (Adler-Taylor, Gaussian random fields)。Percolation 是粗糙 proxy, 若 mechanism 确实是 level-set, scaling 也是 N_struct ∝ V_coarse (Euler characteristic density 的 ergodic 性质), 所以信号 S1 判决仍有效, 但 p 的 interpretation 变。

**结论**: Linux 保留 P1 作为 **scaling prediction 可测** 的实验, 但不 endorse recovery snapshot "percolation 解释精确到 factor 1.5" 的修辞。**本实验测 S1, 不测 percolation 参数是否完美匹配。**

---

## 3. Rust 代码修改 draft

### 3.1 engine.rs 定位

当前 engine.rs 用 **编译时 const**:
```rust
pub const G: usize = 32;
pub const N: usize = G * G * G;
```
并在所有 buffer (a, b, s0a, hist.da, hist.db) 分配时用 `N`。

main.rs 中 `run_one_doc` 的 `block_size=2` 硬编码为字面量 (第 327 行的 `2`)。`middle_every=10`, `outer_every=100` 也是字面量 (第 325-326 行)。

**两方案**:

**方案 P1 (runtime generic, 较大改动)**: 把 G 改为 runtime 参数, 所有 buffer 改 `Vec<f32>` 动态长度。Engine struct 加 `pub g: usize, pub n: usize` 字段, build_nb() / block_average_source() 等用 self.g。估时 **~2 小时代码改 + 1 小时回归测试** (确保 R1 new = R1 old 数字复现)。

**方案 P2 (compile-time feature flags, 快)**: 新建 engine_g64.rs (G=64 const), 两 binary 并存:
- `block_v_phase_b_exp1` (G=32) — 当前, 跑 R1/R2/R3
- `block_v_phase_b_exp1_g64` (G=64) — 新建, 跑 R4/R5/R6

block_size 改为 runtime 参数 (CLI flag)。估时 **~30 分钟** (80% 是 cp + sed + 改 Cargo.toml)。

**推荐 P2** (快, 回归零风险)。以下 diff 基于 P2。

### 3.2 Patch diff (concrete code, P2 方案)

**Step 1**: 复制 engine 目录为 G=64 版本

```bash
cd /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/rust_variants
cp -r block_v_phase_b_exp1 block_v_phase_b_exp1_g64
cd block_v_phase_b_exp1_g64
```

**Step 2**: 改 Cargo.toml (包名)

```toml
# Cargo.toml (block_v_phase_b_exp1_g64)
[package]
name = "block_v_phase_b_exp1_g64"
version = "0.1.0"
edition = "2024"

[dependencies]
rayon = "1.10"
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
```

**Step 3**: 改 engine.rs 第 27–28 行

```rust
// OLD
pub const G: usize = 32;
pub const N: usize = G * G * G;

// NEW (G=64 版本)
pub const G: usize = 64;
pub const N: usize = G * G * G;  // 262144
```

**注意内存检查**: G=64 下 HistoryBuffer 默认 cap=100 × 262144 × 2 × 4 bytes = **209 MB per engine**. rayon 32 线程并发 = 6.7 GB. EPYC 256c 有足够内存 (假设 > 64 GB), 但仍需 confirm (见 §6)。

**Step 4**: 改 main.rs — 把 `block_size` 改为 CLI 参数 (两 binary 都改)

```rust
// 在 main() 内 args 解析部分加 (现有 args.get(9) 已是 obs_every, 加 args.get(10)):

let block_size: usize = args
    .get(10)
    .and_then(|s| s.parse().ok())
    .unwrap_or(2);

// 改 usage 字符串:
if args.len() < 4 {
    eprintln!(
        "usage: {} <input.json> <emb.json> <out_dir> [mode=exp] [dt=0.01] [steps=5000] [seed=20260421] [n_docs=100] [obs_every=100] [block_size=2]",
        args[0]
    );
    std::process::exit(1);
}
```

**Step 5**: run_one_doc 的 block_size 改传入

原 main.rs 第 311-331 行 `par_iter().enumerate().filter_map(...)` 块内, `run_one_doc(..., 2)` 的 `2` 改为传入 block_size:

```rust
let results: Vec<(String, u64, Vec<f32>, Vec<f32>, Vec<ObsRow>)> = docs_use
    .par_iter()
    .enumerate()
    .filter_map(|(i, d)| {
        let key = format!("d:{}", d.doc_id);
        let emb = embs.get(&key)?;
        let seed = seed_base.wrapping_add((i as u64).wrapping_mul(17));
        let (a, b, rows) = run_one_doc(
            emb,
            mode,
            dt,
            steps,
            seed,
            obs_every,
            10,
            100,
            block_size,  // 从 CLI 传入
        );
        Some((d.doc_id.clone(), seed, a, b, rows))
    })
    .collect();
```

**Step 6**: meta.json 记录 block_size (原已写 `"block_size": 2` 字面量, 改为变量):

```rust
let meta = serde_json::json!({
    "mode": mode.label(),
    "n_docs": results.len(),
    "grid_size": G,
    "n_voxels": N,
    "dt_inner": dt,
    "n_inner_steps": steps,
    "middle_every": 10,
    "outer_every": 100,
    "block_size": block_size,  // 变量
    ...
});
```

**Step 7**: 重编译

```bash
cd /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/rust_variants/block_v_phase_b_exp1
cargo build --release  # 32 版本, block_size CLI 化
cd ../block_v_phase_b_exp1_g64
cargo build --release  # 64 版本, block_size CLI 化
```

### 3.3 回归检查 (P2 方案必须做, 0 风险)

跑 baseline R1 (G=32, block=2) 复现 Exp 1 exp 模式, 核对 `N_struct_valid mean` 与 Phase B Exp 1 `o1_analysis.json` 结果。若差 > 1% 即改动出 bug, stop。

```bash
# 在 rebuild 后、跑 R2–R6 前, 先验 R1 regression
./block_v_phase_b_exp1/target/release/block_v_phase_b_exp1 \
    <input.json> <emb.json> /tmp/R1_regression_test exp 0.01 5000 20260421 70 100 2

python3 analyze_O1.py /tmp/R1_regression_test/states_exp.bin  # 复用现有脚本
# 期望: N_struct_valid ≈ 49.8
```

### 3.4 CLI 调用表 (6 runs)

```bash
# R1 (baseline, regression; 如已通过可跳)
block_v_phase_b_exp1/target/release/block_v_phase_b_exp1 \
    <input.json> <emb.json> results/phase_b_p1_scan/R1_g32b2 exp 0.01 5000 20260421 70 100 2

# R2 (grid=32, block=4, coarse 8³=512)
block_v_phase_b_exp1/target/release/block_v_phase_b_exp1 \
    <input.json> <emb.json> results/phase_b_p1_scan/R2_g32b4 exp 0.01 5000 20260421 70 100 4

# R3 (grid=32, block=8, coarse 4³=64; 最小 coarse, 可能边缘效应 dominant)
block_v_phase_b_exp1/target/release/block_v_phase_b_exp1 \
    <input.json> <emb.json> results/phase_b_p1_scan/R3_g32b8 exp 0.01 5000 20260421 70 100 8

# R4 (grid=64, block=2, coarse 32³=32768; 最贵, N_struct prediction ~400)
block_v_phase_b_exp1_g64/target/release/block_v_phase_b_exp1_g64 \
    <input.json> <emb.json> results/phase_b_p1_scan/R4_g64b2 exp 0.01 5000 20260421 70 100 2

# R5 (grid=64, block=4, coarse 16³=4096; V_coarse 同 R1 但 G 不同)
block_v_phase_b_exp1_g64/target/release/block_v_phase_b_exp1_g64 \
    <input.json> <emb.json> results/phase_b_p1_scan/R5_g64b4 exp 0.01 5000 20260421 70 100 4

# R6 (grid=64, block=8, coarse 8³=512; V_coarse 同 R2)
block_v_phase_b_exp1_g64/target/release/block_v_phase_b_exp1_g64 \
    <input.json> <emb.json> results/phase_b_p1_scan/R6_g64b8 exp 0.01 5000 20260421 70 100 8
```

---

## 4. 实验 protocol

### 4.1 Parameters

| 参数 | 值 | 说明 |
|---|---|---|
| mode | exp | α=0.1, β=0.05, multi-scale ✓, whiten=no |
| dt_inner | 0.01 | 同 Exp 1 |
| n_inner_steps | 5000 | 同 Exp 1 (t_sim=50) |
| seed_base | 20260421 | 同 Exp 1 |
| n_docs | 70 | NFCorpus 有 BGE 缓存的 70 docs, 与 Exp 1 完全一致 |
| obs_every | 100 | observable 每外步 log 一次 |
| middle_every | 10 | block-average 每 10 内步 (dt_mid=0.1) |
| outer_every | 100 | history push 每 100 内步 (dt_outer=1.0) |
| block_size | {2, 4, 8} | 扫描 |
| grid (G) | {32, 64} | 扫描 |

**不变量** (六 runs 共享): α, β, λ, N_hist, D, v, t_sim, seed — 保证 唯一 factor 是 (grid, block_size)。

### 4.2 Compute budget estimate

Phase B Exp 1 参考: 8 runs × 50–100 docs × 5000 steps, G=32, 全部完成在**几小时**级 (verdict 未给具体 wall-clock, meta.json elapsed 可查)。

**估算** (单 run, 70 docs):
- G=32: 32³ voxels × 5000 steps × 70 docs = 5.7 × 10¹⁰ voxel-updates. 现代 CPU 单核 ~10⁸ voxel-update/s → 570 秒 / 32 线程 ≈ **~20 秒** (rayon 已高效). Phase B Exp 1 实测可能 ~1-2 分钟 (rayon overhead + observable logging)。
- G=64: voxel 数 × 8 → 每 run **~2-16 分钟**

**6-run 总预算** (保守):
| run | 估时 |
|---|---|
| R1 | 2 分钟 (regression) |
| R2, R3 | 2 分钟 each |
| R4 | 15 分钟 (最贵, G=64 block=2) |
| R5, R6 | 10 分钟 each |
| **总** | **~45 分钟 compute** |

分析 (Python algorithm A+B, aggregate) 约 +30 分钟。**总 wall-clock: ~1.5 小时**。

**内存 peak**: R4 (G=64, block=2) — 32 rayon 线程 × (8 主 buffer + 100 hist slots) × 262144 × 4 bytes ≈ 32 × (8 + 200) × 1 MB = **6.6 GB**. 需要 check 机器可用 RAM (EPYC 256c 通常 > 128 GB, 应充裕)。

### 4.3 Order of runs (建议 small-first)

1. **R1 regression** (baseline 验证 code 改动无 bug)
2. **R2, R3** (cheap, G=32 其他 block_size; 若 R2 scaling 不对, 早期 abort R4/R5/R6)
3. **R5, R6** (G=64 中等成本, 验 "same V_coarse 不同 grid" 的 signal)
4. **R4** (最贵, 最后跑; 若前 5 个已 confirm/falsify mechanism, R4 提供 decisive 数据)

**Early abort**: R2 N_struct 若 > 20 (预测 ~6), 即 N_struct **不 scale with V_coarse**, mechanism 早期 falsified, 不必跑 R4–R6。通知一凡 re-authorize 决策。

---

## 5. Pass/fail 判决

### 5.1 Pass/fail 梯度

| 级别 | 判据 (信号 S1 + S2) | 后续行动 |
|---|---|---|
| **Mechanism confirmed** | 所有 6 runs N_struct / V_coarse ∈ [0.006, 0.024] (within factor 2 of 0.012) AND p ∈ [0.13, 0.19] | arXiv v2 §A.3.1 加 quantitative percolation subsection; recovery snapshot §3.4 P1 候选升级 "verified" |
| **Mechanism partially** | 5/6 runs 符合 OR within factor 2–5; trend 方向对但 off-by-systematic-factor | arXiv v2 appendix 写 "qualitative scaling confirmed; quantitative relation requires further work"; P1 候选留在 "narrative" |
| **Mechanism falsified (weak)** | ≥ 2 runs off by > factor 5 OR N_struct 不随 V_coarse 单调 | Recovery snapshot §3.4 主动下调: "50 patches 的 mechanism 非 coarse-lattice percolation" |
| **Mechanism falsified (strong)** | R4 (V_coarse=32768) N_struct ≪ 400 (e.g., < 100) OR R3/R6 (V_coarse=64/512) N_struct ≫ prediction | 同上 + paper 须 remove percolation narrative, 改 "patches 形成 mechanism 未知, 进一步研究" |

### 5.2 Secondary observables (mechanism triangulation)

除 N_struct, 同时记录每 run:
- **per-doc N_struct 分布**: mean, std, min, max (70 docs sample), 判决 S1 用 mean 但 dispersion 也告知 mechanism 健壮性
- **p_empirical**: supra-threshold voxel 比例 = (C > ⟨C⟩+σ).mean(). 判决 S2 用
- **mean cluster size ⟨s⟩**: total supra-threshold voxels / N_clusters
- **cluster size 分布 histogram**: 与 percolation n_s ~ s^{-τ} 比对; 3D τ ≈ 2.189 预测
- **r_g 分布**: 与 block_size × (coarse lattice sparsity) 的 scaling 比对

这些告诉我们 mechanism 哪里对 / 哪里偏离, 不只是 pass/fail binary。

### 5.3 具体 threshold 数字 (Linux propose, 一凡可调)

**Confirmed** (严格):
- 6/6 runs 满足 N_struct / V_coarse ∈ [baseline × 0.5, baseline × 2] = [0.006, 0.024]
- 6/6 runs p_empirical ∈ [0.14, 0.18]

**Partially** (宽松):
- 4/6 满足上面任一信号

**Falsified**:
- 不 partially 且任一 run 偏 > factor 5

---

## 6. 风险 + mitigation

| # | 风险 | 概率 | 影响 | Mitigation |
|---|---|---|---|---|
| 1 | R4 (G=64) 内存溢出 | 低 | run fail | 先 `free -h` check, 若 < 16 GB 可用改 rayon 线程 32 → 16 |
| 2 | R4 runtime 远超 15 min | 中 | 时间压力 | R4 放最后, 可 overnight |
| 3 | R3 / R6 (small coarse lattice) 统计噪声 dominant, p_empirical 与 0.16 显著偏差 | **中** | S2 判决失败 | R3 预测 mean 0.8 patches; 70 docs mean 的 std error ~ √(0.8·70)/70 ≈ 0.1, variance 大; 需 emphasise R3 为 "lower-bound sanity check" 而非 precision 测量 |
| 4 | R4 N_struct 确实 ≈ 400, 但 r_g<8 filter 在 V_coarse 巨大的情况下排除大 cluster, 统计偏倚 | 中 | 可能 artifact-confirmed | Secondary obs 看 r_g 分布; 若 g64 r_g 分布 shift → flag filter 依 coarse lattice dependence |
| 5 | Code 改动引入 regression (R1 与 Exp 1 不 match) | 低 | 全实验 invalid | Step 3.3 必做; 若 regression fail stop |
| 6 | percolation mechanism 假 (实为 Gaussian level-set 或 其他), 但 N_struct ∝ V_coarse 偶然成立 | 中 | confirmed-but-wrong-reason | 分析时同时比 level-set Euler 特征预测 (Adler-Taylor, N_euler ≈ V · exp(-T²/2) · T · (2π)^{-3/2}); 若 level-set Euler 也 match, 需两 mechanism 对 scaling 信号 degenerate 的谨慎结论 |
| 7 | Recovery snapshot p_c=0.3116 is error (26-conn 实为 0.2464), 影响 prediction | **已确认**, Linux 已 correct | 小 | §2.1 / §2.4 已注明, 用 0.2464 |

---

## 7. arXiv v2 implication

### 7.1 若 mechanism confirmed

**§A.3.1 新增 quantitative percolation subsection (~300 字)**:
- 声明 N_struct 随 V_coarse 线性 scale, 系数 ≈ 0.012 cluster/cell
- 声明 supra-threshold 比例 p ≈ 0.16 (单边 1σ tail), p/p_c(26-conn) ≈ 0.65, 亚临界 but non-trivial
- 对照 6 runs 表, scaling exponent fit
- **降级措辞 (Linux 纪律)**: "the 50-patches-per-doc observation is scaling-consistent with 3D subcritical site percolation on the block-averaged coarse lattice; this does not establish that the mechanism **is** percolation (the C field is spatially correlated, violating independence), only that the scaling exponent and amplitude are reproduced within factor 2"
- 更新 Phase B Exp 1 verdict §2: N_struct 的 "mechanism" 从 "narrative" 升级 "scaling-quantitatively verified"

### 7.2 若 mechanism partially

- appendix 加弱版 subsection: "N_struct scales with V_coarse but the coefficient shifts systematically with grid size (or block size); percolation gives the right order of magnitude but the precise mechanism requires refinement"
- P1 候选留在 recovery snapshot "narrative 级", 不升级

### 7.3 若 mechanism falsified

- **Recovery snapshot §3.4 主动下调**: "2026-04-16 提出的 3D site percolation 解释在 04-17 scaling scan 中被实验 refute (R# off by factor X); 50 patches 的 mechanism 未知, 留为 open question"
- arXiv v1 §A.3.1 当前 narrative 不动 (原文本就不 claim percolation, 只 report observation), 只是**不添加** percolation mechanism claim
- P1 候选从 Linux max-effort 6 候选中 **删除** (其他 5 个候选不影响)

### 7.4 Zenodo / v0.1.1 release 影响

本实验 **不影响** 04-23/04-25 v0.1.1 release (Phase B Exp 1 appendix 已独立完成)。本实验结果入 arXiv **v2** (或 Phase B Exp 2 companion), 不 gate release。

---

## 8. 一凡 authorize 清单 (需要什么 input)

**P0 必需**:
1. **Authorize Linux 启动实验**: 批/否 本设计全量 (6 runs) 或 subset (e.g., 仅 R1/R2/R3 G=32 三 runs, 跳过 G=64; 成本减半)
2. **内存上限 confirm**: 若 EPYC 机可用 RAM < 32 GB, R4 需 abort 或 rayon 减线程
3. **Early-abort 权限**: 批 R2 N_struct 超预测 factor 3 时 Linux 可 decide 不跑 R4–R6, 直接写 falsified verdict

**P1 可选**:
4. **判决 threshold 调整**: §5.3 Linux 提的 "confirmed 需 6/6 in [0.5×, 2×]" 是否太严? 可放宽到 5/6 in [0.33×, 3×]
5. **Secondary mechanism triangulation**: 要不要额外算 level-set Euler 特征预测 (Adler-Taylor)? 加 ~2h 分析
6. **数据归档**: 6 runs × 70 docs × G=32/64 states.bin 共 ~500 MB - 3 GB. 归 Zenodo v0.2 (跟 arXiv v2)? 还是仅 project internal archive?

**P2 非阻塞**:
7. **实验 naming convention**: 建议用 `phase_b_exp2_p1_scan_20260417` 归档名? Or 别的
8. **是否 spawn review agent**: 结果出来后是否 spawn 独立 review 审 code + 统计 + 判决? Linux 倾向 **是** (standing rule)

---

## 9. Linux 自检: 实验设计 assumptions

**(A) Assumption: 阈值 T = ⟨C⟩ + 1σ(C) 在所有 (grid, block) 下均给 p ≈ 0.16 高斯 1σ tail**
- 自检: C(x) 是 |⟨e^{iθ}⟩_{27-nb}| 在 [0, 1] 支持, **不完全高斯**. 但经验上 1σ tail 约 13-20% (双侧高斯是 16%)。若分布偏态严重, p 可能偏 0.16 ±0.05. **S2 判决容忍 [0.14, 0.18]** 已部分吸收这个不确定, 但若 block=8 (small coarse lattice) 下 C 分布显著非高斯, 需单独 flag。
- **缓解**: 记录 p_empirical 分布 histogram per run, 不只 report mean。

**(B) Assumption: scaling signal S1 (N_struct ∝ V_coarse) 足够 distinguish 正确 / 错误 mechanism**
- 自检: **不完全足够**. 任何 homogeneous scaling (level-set Euler, "N independent topological features per unit coarse volume") 都给 S1. 若 mechanism 本质是 "level-set topology", 也通过 S1。**只有 S2 (p invariance) + cluster 大小分布 (τ ≈ 2.189 的 power-law tail) + r_g 分布 同时匹配**, 才能具体说 percolation。
- **缓解**: §5.2 secondary observables 必须全记录, 结果不能只看 S1 (binary 判决)。

**(C) Assumption: Exp 1 R1 的 N_struct = 49.8 是 robust baseline, 可作 scaling 系数锚点**
- 自检: Exp 1 用 50 docs (verdict §1 说 "70 docs have BGE embeddings cached, all 5 main runs use these 70 docs identically")。实际 70 docs mean 49.8 with some per-doc variance. **per-doc variance** (std?) recovery 未记录; 若 std/mean > 0.5, 50 作锚点不稳。
- **缓解**: 在启动 R2–R6 前, 重算 Exp 1 o1_analysis.json 里 per-doc std, 决定 scaling coefficient 的 precision。

**(D) Assumption: 改 block_size 和 grid 不 alter 其他 dynamics 的 qualitative 行为 (e.g., pattern 形成本身 still occur)**
- 自检: block_size=8 on grid=32 给 coarse lattice 仅 4³=64 cells, multi-scale seeding 机制的 "seed" 数目 64 vs Exp 1 4096, **可能 qualitative 改变动力学**. control_single (无 multi-scale) 给 0 patches, R3 可能 regress 到 similar regime (介于 full multi-scale 和 no multi-scale).
- **缓解**: R3 是 expected-corner-case; pass/fail 主要靠 R4/R5/R6 (G=64). R3 数字用于诊断, 不作 mechanism 判决主信号.

**(E) Assumption: Phase B Exp 1 code 中 block_size 硬编码改 CLI 不影响 exp 模式其他部分**
- 自检: main.rs 第 327 行 `2` 是 `run_one_doc` 的 block_size 参数, 只传入 `engine.block_average_source(block)`; engine.rs `block_average_source` 函数用 `block <= 1` early-return (不 block) 和 `nb = G / block` 粗格数。**当 G % block ≠ 0 时** (e.g., G=32, block=8: 32/8=4 ✓; 但 G=64, block=3 不整除不支持), 需 flag. 本实验 6 runs 全整除。
- **缓解**: CLI parse 加 assert `G % block == 0` early。

**(F) Assumption: 70 docs 统计足够**
- 自检: R3 predicted mean N_struct ≈ 0.8, Poisson std ≈ 0.9, per-doc 层面几乎所有 doc 都 0 或 1. 70 docs sample 的 mean 估计 std error ≈ 0.9/√70 ≈ 0.11; prediction 0.8, 观测 mean 可能落 [0.7, 0.9] — 可诊断但不 precise。**R3 不适合做 precision scaling 判决**; 仅作 "边界测试"。
- **缓解**: 在表内标注 R3/R6 的 estimation error, 判决时去权。

**(G) Assumption: recovery snapshot §3.4 P1 的 "within factor 1.5" 说法是 Linux 可信**
- 自检: **不可信**. §2.4 已 flag 三处质疑 (p_c value wrong; mean-field → 50 的修正 不透明; C 场非独立). 本实验的目的之一就是 **replace** 那个 estimate with 实验数据, 不把 snapshot 数字当 ground truth。
- **缓解**: 本设计 §2 已 neutral framing, 不 bind pass/fail 到 snapshot 数字。

**Linux 对本设计的总 confidence**:
- [STATIC] 层 (数字 预测, mechanism 推导): 中-高。percolation 估算范围给出 [1 – 400] 的 wide envelope, 方法 C (直接锚定 baseline) 给 point estimate. Linux 诚实 flag 推导不 tight。
- [DYNAMIC-RUST-DRAFT] 层 (code 修改): 高。P2 方案是 minimal change, engine 核心逻辑不碰, 回归 R1 即可 catch bug。
- **最大 residual uncertainty**: mechanism 真解释是否 percolation (vs. level-set Euler vs. 别的), 本实验 S1+S2 能 partial distinguish 但不 definitive。

---

## 附 A. 相关文件 index

- **本文件**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/A4_P1_PERCOLATION_SCAN_DESIGN_20260416.md`
- **Phase B Exp 1 verdict**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/phase_b_exp1_verdict.md`
- **Phase B Exp 1 appendix**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/phase_b_exp1_appendix.md`
- **Engine source (待改)**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/rust_variants/block_v_phase_b_exp1/src/{engine,main}.rs`
- **Recovery snapshot §3.4 P1**: `/home/amd/.claude/projects/-home-amd-HEZIMENG/memory/RECOVERY_SNAPSHOT_20260416.md`
- **O1 分析脚本**: `/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/phase_b_exp1/analyze_O1.py` (已验过 R1 baseline 数据)

*— A4 (Opus 4.7 xhigh), 2026-04-16, under Linux Claude dispatch, 等一凡 04-17 morning authorize*
