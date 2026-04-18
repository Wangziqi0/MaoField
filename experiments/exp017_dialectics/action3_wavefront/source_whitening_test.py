"""
对照: 如果 mean-subtract source (whiten), σ=0.5 crossing 会怎样变?
如果 tilt 主导 → crossing 消失
如果 diffusion 主导 → crossing 率几乎不变
"""
import sys, os, time, json
sys.path.insert(0, '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/action3_wavefront')
from wavefront_diag import (run_langevin, build_source_from_emb,
                             init_u_nonzero, build_nb,
                             G, N, D, DT, STEPS, CLAMP, U_THRESH)
import numpy as np

emb_path = '/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4/embeddings_nfcorpus.json'
embs = json.load(open(emb_path))
emb = np.array(embs['d:MED-961'], dtype=np.float32)

def run_with_source(sa, sb, seed=1000, sigma=0.5, steps=500, dt=DT, clamp=CLAMP,
                    track=True):
    a, b = init_u_nonzero(seed)
    xm, xp, ym, yp, zm, zp = build_nb(G)
    noise_scale = sigma * np.sqrt(dt)
    rng = np.random.default_rng(seed * 31415)
    t_cross = np.full(N, -1, dtype=np.int32)
    N_crossed = np.zeros(steps+1, dtype=np.int64)
    u0 = a*a + b*b
    t_cross[u0 < U_THRESH] = 0
    N_crossed[0] = (u0 < U_THRESH).sum()
    for step in range(1, steps+1):
        lap_a = a[xm]+a[xp]+a[ym]+a[yp]+a[zm]+a[zp] - 6*a
        lap_b = b[xm]+b[xp]+b[ym]+b[yp]+b[zm]+b[zp] - 6*b
        u = a*a + b*b
        um1, um4 = u-1.0, u-4.0
        f_u = um1**2 * um4**2 + 2*u*um1*um4*(2*u-5)
        da = D*lap_a - f_u*a + sa
        db = D*lap_b - f_u*b + sb
        eta_a = rng.standard_normal(N).astype(np.float32)
        eta_b = rng.standard_normal(N).astype(np.float32)
        a = np.clip(a + dt*da + noise_scale*eta_a, -clamp, clamp)
        b = np.clip(b + dt*db + noise_scale*eta_b, -clamp, clamp)
        if track:
            u = a*a + b*b
            jc = (t_cross < 0) & (u < U_THRESH)
            t_cross[jc] = step
            N_crossed[step] = (t_cross >= 0).sum()
    return t_cross, N_crossed, a, b

# Build normal source
sa_orig, sb_orig = build_source_from_emb(emb)
sb_mean_orig = sb_orig.mean()
sa_mean_orig = sa_orig.mean()
print(f"Original source: ⟨Sa⟩={sa_mean_orig:.4e}, ⟨Sb⟩={sb_mean_orig:.4e}")
print(f"  Sa: std={sa_orig.std():.4f}, max={sa_orig.max():.3f}, min={sa_orig.min():.3f}")
print(f"  Sb: std={sb_orig.std():.4f}, max={sb_orig.max():.3f}, min={sb_orig.min():.3f}")

# Whitened (mean-subtracted)
sa_whit = sa_orig - sa_mean_orig
sb_whit = sb_orig - sb_mean_orig
print(f"\nWhitened: ⟨Sa⟩={sa_whit.mean():.4e}, ⟨Sb⟩={sb_whit.mean():.4e}")

# Zero source
sa_zero = np.zeros(N, dtype=np.float32)
sb_zero = np.zeros(N, dtype=np.float32)

scenarios = [
    ('original (BGE raw)', sa_orig, sb_orig),
    ('whitened (mean=0)', sa_whit, sb_whit),
    ('zero source', sa_zero, sb_zero),
]

print("\n=== Crossing under different source ===")
for name, sa, sb in scenarios:
    tc, Nc, a, b = run_with_source(sa, sb, seed=1000, sigma=0.5, steps=500)
    final_frac = (tc >= 0).sum() / N
    u_final = a*a + b*b
    frac_u0 = (u_final < 0.5).mean()
    tc_arr = tc[tc >= 0]
    median = np.median(tc_arr) if len(tc_arr) > 10 else -1
    # when does 50% cross?
    frac = Nc / N
    t_50 = np.argmax(frac >= 0.50) if (frac >= 0.50).any() else -1
    print(f"\n{name}:")
    print(f"  crossed_frac (u<0.5 during run) = {final_frac:.3f}")
    print(f"  final u<0.5 fraction = {frac_u0:.3f}")
    print(f"  t_50 = {t_50} steps, median t_cross = {median} steps")

# Also σ=0 对照: 纯 gradient + source (no noise)
print("\n=== σ=0 (no Langevin), 只比较 gradient flow + source ===")
for name, sa, sb in scenarios:
    tc, Nc, a, b = run_with_source(sa, sb, seed=1000, sigma=0.0, steps=5000)
    final_frac = (tc >= 0).sum() / N
    u_final = a*a + b*b
    frac_u0 = (u_final < 0.5).mean()
    frac_u1 = ((u_final >= 0.5) & (u_final < 1.5)).mean()
    print(f"{name} (σ=0): u<0.5={frac_u0:.3f}, 0.5<u<1.5={frac_u1:.3f}, u_max={u_final.max():.3f}")

# 最终总结
print("\n=== verdict ===")
print("如果 σ=0.5 crossing 主要来自 BGE DC tilt:")
print("  → whitened source 应该大幅减少 crossing")
print("如果 σ=0.5 crossing 主要来自 diffusion:")
print("  → whitened source 几乎不影响 crossing rate")
print("如果 σ=0 deterministic 就已经 cross to u<0.5:")
print("  → tilt 主导 (source drift 能独立 cross)")
