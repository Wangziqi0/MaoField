"""
Action 3 路线 A: Wavefront 诊断
重现 block4_5/b1_langevin σ=0.5 (A1 原势 V = u(u-1)²(u-4)²) Langevin,
tracking per-voxel t_cross (first time u < 0.5, 即穿过 inner saddle).

输出:
  - t_cross 数组 (32768 voxels)
  - N_crossed(t) 时间序列 (5000 steps)
  - C_s(r) 空间相关
  - Avrami fit n
"""

import json
import numpy as np
import sys
import os
import time

G = 32
N = G * G * G
D = 0.1
DT = 0.05
STEPS = 5000
SIGMA = 0.5
CLAMP = 3.0
SEED = 1000  # same as doc 0 seed in b1_langevin

# Barrier crossing threshold: inner saddle at u ~ 0.2597, midpoint between u=1 well
# and u=0.2597 saddle. We take u_thresh = 0.5 as 定义 crossing 穿过 inner barrier from u=1 side.
U_THRESH = 0.5

def build_nb(G):
    """6-neighbor periodic indices."""
    idx = np.arange(G*G*G).reshape(G, G, G)
    xm = np.roll(idx, 1, axis=2).ravel()
    xp = np.roll(idx, -1, axis=2).ravel()
    ym = np.roll(idx, 1, axis=1).ravel()
    yp = np.roll(idx, -1, axis=1).ravel()
    zm = np.roll(idx, 1, axis=0).ravel()
    zp = np.roll(idx, -1, axis=0).ravel()
    return xm, xp, ym, yp, zm, zp

def xorshift_uniform(seed, n):
    """Deterministic xorshift PRNG, matches Rust rng."""
    # 模拟 Rust: rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17
    # 对于大量点, 直接用 numpy 的 RNG 替代 — 物理 statistic 等价
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n).astype(np.float32)

def build_source_from_emb(emb):
    """Match Rust build_source_from_emb: tile 512-dim to 32³, smooth 3x, max-normalize."""
    assert emb.shape == (1024,)
    half = 512
    sa = emb[:half].repeat(N // half + 1)[:N].astype(np.float32)
    sb = emb[half:].repeat(N // half + 1)[:N].astype(np.float32)
    # 但 Rust 写的是 k % half，即 sa[k] = emb[k % 512]
    sa = emb[np.arange(N) % half].astype(np.float32).copy()
    sb = emb[half + (np.arange(N) % half)].astype(np.float32).copy()

    xm, xp, ym, yp, zm, zp = build_nb(G)
    def smooth(s):
        s = s.copy()
        buf = np.empty_like(s)
        for _ in range(3):
            buf = (s[xm] + s + s[xp]) / 3.0; s = buf.copy()
            buf = (s[ym] + s + s[yp]) / 3.0; s = buf.copy()
            buf = (s[zm] + s + s[zp]) / 3.0; s = buf.copy()
        mx = np.abs(s).max()
        if mx > 0: s = s / mx
        return s

    sa = smooth(sa); sb = smooth(sb)
    return sa, sb

def init_u_nonzero(seed):
    """|psi| ≈ 1.0 ± 0.3, imag spread 0.3."""
    rng = np.random.default_rng(seed + 1)
    u_a = rng.random(N).astype(np.float32)
    u_b = rng.random(N).astype(np.float32)
    a = 1.0 + 0.3 * (u_a * 2.0 - 1.0)
    b = 0.3 * (u_b * 2.0 - 1.0)
    return a.astype(np.float32), b.astype(np.float32)

def run_langevin(emb, seed=SEED, sigma=SIGMA, steps=STEPS, dt=DT, clamp=CLAMP,
                 track_crossing=True, return_snapshots=False, snapshot_every=50):
    """
    Run Langevin on A1 potential V = u(u-1)²(u-4)²
    f_u = (u-1)²(u-4)² + 2u(u-1)(u-4)(2u-5)
    dψ = D∇²ψ - f_u ψ + S + σ·√dt · η
    """
    a, b = init_u_nonzero(seed)
    sa, sb = build_source_from_emb(emb)
    xm, xp, ym, yp, zm, zp = build_nb(G)
    noise_scale = sigma * np.sqrt(dt)
    rng = np.random.default_rng(seed * 31415)

    # per-voxel t_cross: step index when u first dropped below U_THRESH
    t_cross = np.full(N, -1, dtype=np.int32)
    N_crossed = np.zeros(steps + 1, dtype=np.int64)

    snapshots = [] if return_snapshots else None

    u0 = a * a + b * b
    crossed = u0 < U_THRESH
    t_cross[crossed] = 0
    N_crossed[0] = int(crossed.sum())

    t0 = time.time()
    for step in range(1, steps + 1):
        # laplacian
        lap_a = a[xm] + a[xp] + a[ym] + a[yp] + a[zm] + a[zp] - 6.0 * a
        lap_b = b[xm] + b[xp] + b[ym] + b[yp] + b[zm] + b[zp] - 6.0 * b
        u = a * a + b * b
        um1 = u - 1.0
        um4 = u - 4.0
        f_u = um1 * um1 * um4 * um4 + 2.0 * u * um1 * um4 * (2.0 * u - 5.0)

        da = D * lap_a - f_u * a + sa
        db = D * lap_b - f_u * b + sb

        eta_a = rng.standard_normal(N).astype(np.float32)
        eta_b = rng.standard_normal(N).astype(np.float32)

        a = np.clip(a + dt * da + noise_scale * eta_a, -clamp, clamp)
        b = np.clip(b + dt * db + noise_scale * eta_b, -clamp, clamp)

        if track_crossing:
            u_new = a * a + b * b
            # voxel crossed if not yet crossed AND now u < U_THRESH
            just_crossed = (t_cross < 0) & (u_new < U_THRESH)
            t_cross[just_crossed] = step
            N_crossed[step] = int((t_cross >= 0).sum())

        if return_snapshots and (step % snapshot_every == 0):
            snapshots.append((step, (a*a + b*b).copy()))

        if step % 500 == 0:
            print(f"  step {step}/{steps}, N_crossed={N_crossed[step]}/{N} "
                  f"({100*N_crossed[step]/N:.1f}%), elapsed={time.time()-t0:.1f}s", flush=True)

    return {
        'a_final': a, 'b_final': b,
        't_cross': t_cross,
        'N_crossed': N_crossed,
        'snapshots': snapshots,
        'elapsed_s': time.time() - t0,
    }


def compute_Cs_r(t_cross, G=32, dt_thresh_steps=10, max_r=16, n_pairs_sample=200_000):
    """
    C_s(r) = <1[|t_cross(i) - t_cross(j)| < dt_thresh] | r(i,j) = r>
    仅用 crossed voxel; uncrossed 的 t_cross=-1 会被滤掉.
    采样 n_pairs_sample 对 voxel.
    """
    crossed_idx = np.flatnonzero(t_cross >= 0)
    n_crossed = len(crossed_idx)
    print(f"  n_crossed={n_crossed}, sampling {n_pairs_sample} pairs")

    rng = np.random.default_rng(42)
    i_sel = rng.choice(n_crossed, size=n_pairs_sample)
    j_sel = rng.choice(n_crossed, size=n_pairs_sample)
    mask = i_sel != j_sel
    i_sel = crossed_idx[i_sel[mask]]
    j_sel = crossed_idx[j_sel[mask]]

    # 转化为 3D 坐标
    zi, yi, xi = np.unravel_index(i_sel, (G, G, G))
    zj, yj, xj = np.unravel_index(j_sel, (G, G, G))

    dx = np.minimum(np.abs(xi - xj), G - np.abs(xi - xj))
    dy = np.minimum(np.abs(yi - yj), G - np.abs(yi - yj))
    dz = np.minimum(np.abs(zi - zj), G - np.abs(zi - zj))

    r = np.sqrt(dx**2 + dy**2 + dz**2)
    dt_abs = np.abs(t_cross[i_sel] - t_cross[j_sel])

    r_bins = np.arange(0, max_r + 1.5, 1.0)
    Cs = np.zeros(len(r_bins) - 1)
    counts = np.zeros(len(r_bins) - 1, dtype=np.int64)
    for b in range(len(r_bins) - 1):
        mask = (r >= r_bins[b]) & (r < r_bins[b+1])
        if mask.sum() > 0:
            Cs[b] = (dt_abs[mask] < dt_thresh_steps).mean()
            counts[b] = mask.sum()

    r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
    return r_centers, Cs, counts


def fit_avrami(N_crossed, N_total, dt_step=DT, t_skip_frac=0.02):
    """
    Avrami: N(t)/N_total = 1 - exp(-(t/tau)^n)
    取 log: log(-log(1 - N/N_total)) = n*log(t) - n*log(tau)
    skip 前 2% 和后 2% 避免 edge
    """
    f = N_crossed / N_total
    # 规避 f=0 或 f>0.98
    n_total_steps = len(N_crossed)
    t_steps = np.arange(n_total_steps) * dt_step
    mask = (f > 0.05) & (f < 0.95) & (t_steps > 0.1)
    if mask.sum() < 10:
        return None, None, None
    y = np.log(-np.log(1 - f[mask]))
    x = np.log(t_steps[mask])
    # linear regression
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    n_avrami, intercept = coef
    tau = np.exp(-intercept / n_avrami)
    # residual R²
    y_pred = n_avrami * x + intercept
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    return n_avrami, tau, r2


if __name__ == "__main__":
    t_start = time.time()

    print("=== Action 3 Wavefront Diagnostic ===")
    print(f"G={G}, N={N}, steps={STEPS}, dt={DT}, sigma={SIGMA}, U_THRESH={U_THRESH}")
    print(f"SEED={SEED} (matches b1_langevin doc 0)")

    # Load 1 doc's embedding
    emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
    with open(emb_path) as f:
        embs = json.load(f)

    # match b1_langevin doc_ids[0] = MED-961
    doc_id = 'MED-961'
    key = f'd:{doc_id}'
    emb = np.array(embs[key], dtype=np.float32)
    print(f"Doc: {doc_id}, emb stats: mean={emb.mean():.4e}, std={emb.std():.4e}")
    sb_mean = emb[512:].mean()
    print(f"  emb[512:] (Sb) per-doc mean = {sb_mean:.4e}")

    print("\n--- Running Langevin ---")
    result = run_langevin(emb, seed=1000, sigma=SIGMA, steps=STEPS, track_crossing=True,
                          return_snapshots=True, snapshot_every=250)

    t_cross = result['t_cross']
    N_crossed = result['N_crossed']
    n_crossed_final = int((t_cross >= 0).sum())
    frac = n_crossed_final / N
    print(f"\n--- Results ---")
    print(f"Final N_crossed = {n_crossed_final}/{N} ({100*frac:.2f}%)")
    print(f"Elapsed: {result['elapsed_s']:.1f}s")

    # Compare to b1_langevin observed 85% u=0 at σ=0.5 — if we're not near that, check thresh
    u_final = result['a_final']**2 + result['b_final']**2
    print(f"Final u stats: max={u_final.max():.3f}, mean={u_final.mean():.3f}")
    print(f"Final u<0.5 fraction: {(u_final < 0.5).mean():.3f}")
    print(f"Final u<0.1 fraction (near u=0 basin): {(u_final < 0.1).mean():.3f}")
    print(f"Final 0.5<u<1.5 (u=1 basin): {((u_final>=0.5) & (u_final<1.5)).mean():.3f}")
    print(f"Final u>2 (clamp region): {(u_final > 2).mean():.3f}")

    # t_cross distribution
    t_cross_steps = t_cross[t_cross >= 0]
    print(f"\n--- t_cross statistics ---")
    print(f"min={t_cross_steps.min()}, max={t_cross_steps.max()}, "
          f"mean={t_cross_steps.mean():.1f}, median={np.median(t_cross_steps):.1f}")
    print(f"t_cross percentiles: "
          f"10%={np.percentile(t_cross_steps, 10):.0f}, "
          f"25%={np.percentile(t_cross_steps, 25):.0f}, "
          f"50%={np.percentile(t_cross_steps, 50):.0f}, "
          f"75%={np.percentile(t_cross_steps, 75):.0f}, "
          f"90%={np.percentile(t_cross_steps, 90):.0f}")

    # N_crossed time series
    print(f"\n--- N_crossed(t) samples ---")
    for step in [0, 100, 250, 500, 1000, 2000, 3000, 4000, 5000]:
        if step <= STEPS:
            print(f"  step={step} (t={step*DT:.1f}): N={N_crossed[step]} ({100*N_crossed[step]/N:.2f}%)")

    # Avrami fit
    print(f"\n--- Avrami fit ---")
    # Use current final count as N_total (全部 voxel 最终 crossed 的占比)
    N_total_effective = max(n_crossed_final, 1)
    n_av, tau, r2 = fit_avrami(N_crossed, N_total_effective, dt_step=DT)
    if n_av is not None:
        print(f"  Avrami exponent n = {n_av:.3f}")
        print(f"  tau = {tau:.2f} (time units)")
        print(f"  R² = {r2:.4f}")
        print(f"  Interpretation: n~3-4 → 3D wavefront; n~1 → independent Poisson; n~2 → 1D or 2D wall")
    else:
        print("  Avrami fit failed (insufficient data in 5-95% range)")

    # C_s(r) spatial correlation
    print(f"\n--- C_s(r) spatial correlation ---")
    for dt_thr in [5, 10, 20, 50]:
        print(f"  dt_thresh = {dt_thr} steps ({dt_thr*DT:.2f} time units):")
        r_centers, Cs, counts = compute_Cs_r(t_cross, dt_thresh_steps=dt_thr,
                                              max_r=16, n_pairs_sample=500_000)
        for i, rc in enumerate(r_centers):
            if counts[i] > 100:
                print(f"    r={rc:.1f}: C_s={Cs[i]:.4f}  (n_pairs={counts[i]})")

    # Save results for offline plotting
    out_dir = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront'
    np.savez_compressed(
        os.path.join(out_dir, 'wavefront_doc0.npz'),
        t_cross=t_cross,
        N_crossed=N_crossed,
        u_final=u_final,
        config=dict(G=G, N=N, sigma=SIGMA, dt=DT, steps=STEPS, U_THRESH=U_THRESH,
                   doc_id=doc_id, seed=1000),
    )
    print(f"\nSaved to {out_dir}/wavefront_doc0.npz")
    print(f"\nTotal wall time: {time.time()-t_start:.1f}s")
