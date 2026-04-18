"""
MaoField Exp004: Evolution Experiments A-E
===========================================

A: Pure Gray-Scott verification (no tokens)
B: Single text injection → observe patterns
C: Similar texts comparison (quantitative change)
D: Cross-domain comparison
E: Query-Doc matching via field fusion
"""

import numpy as np
import json
import time
import os
from simulator import ReactionDiffusion3D
from inject import inject_tokens, compute_token_positions
from config import *


def save_snapshot(name, sim, out_dir=SNAPSHOTS_DIR):
    np.save(os.path.join(out_dir, f"{name}_u.npy"), sim.u)
    np.save(os.path.join(out_dir, f"{name}_v.npy"), sim.v)


def field_distance(v1, v2):
    """L2 distance between two v-fields (normalized)"""
    diff = v1 - v2
    return float(np.sqrt(np.mean(diff * diff)))


def field_correlation(v1, v2):
    """Pearson correlation between two v-fields"""
    v1f = v1.flatten()
    v2f = v2.flatten()
    v1c = v1f - v1f.mean()
    v2c = v2f - v2f.mean()
    num = np.dot(v1c, v2c)
    den = np.sqrt(np.dot(v1c, v1c) * np.dot(v2c, v2c))
    return float(num / (den + 1e-15))


def fusion_test(v_query, v_doc, f_base=F_BASE, k_base=K_BASE,
                max_steps=5000, convergence_threshold=1e-6):
    """
    Put query and doc fields together and continue evolving.
    Matching = fast fusion (energy stabilizes quickly).
    Non-matching = slow/no fusion.

    Returns: (convergence_step, final_energy, energy_drop)
    """
    # Create a new simulator with merged fields
    sim = ReactionDiffusion3D(f_base=f_base, k_base=k_base)

    # Initialize u from query, v from combination
    # Strategy: average the two v-fields as starting point
    sim.v = (v_query + v_doc) / 2.0
    sim.u = 1.0 - sim.v  # complementary

    initial_energy = sim.compute_energy()
    prev_energy = initial_energy

    convergence_step = max_steps
    for step in range(max_steps):
        sim.step()
        if (step + 1) % 100 == 0:
            energy = sim.compute_energy()
            change = abs(energy - prev_energy) / (abs(prev_energy) + 1e-10)
            if change < convergence_threshold:
                convergence_step = step + 1
                break
            prev_energy = energy

    final_energy = sim.compute_energy()
    energy_drop = initial_energy - final_energy

    return convergence_step, final_energy, energy_drop


# ── Experiment A: Pure Gray-Scott ──

def experiment_a():
    print("\n" + "=" * 60)
    print("EXPERIMENT A: Pure Gray-Scott Verification")
    print("=" * 60)

    # Try different (F, k) combinations to find pattern-forming region
    param_grid = []
    for F in [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06]:
        for k in [0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07]:
            param_grid.append((F, k))

    results = []
    best_params = None
    best_pattern_strength = 0

    for F, k in param_grid:
        sim = ReactionDiffusion3D(f_base=F, k_base=k)
        sim.init_random_seed(seed_size=4)

        # Quick run
        sim.run(5000, snapshot_interval=5000, verbose=False)

        v_std = sim.v.std()
        v_max = sim.v.max()
        has_pattern = sim.has_pattern()
        pattern_strength = v_std * v_max

        results.append({
            "F": F, "k": k,
            "v_std": float(v_std), "v_max": float(v_max),
            "has_pattern": has_pattern,
            "pattern_strength": float(pattern_strength)
        })

        if pattern_strength > best_pattern_strength:
            best_pattern_strength = pattern_strength
            best_params = (F, k)

        marker = "✓" if has_pattern else " "
        if has_pattern:
            print(f"  {marker} F={F:.3f} k={k:.3f} v_std={v_std:.4f} v_max={v_max:.4f}")

    print(f"\n  Best params: F={best_params[0]:.3f} k={best_params[1]:.3f} (strength={best_pattern_strength:.6f})")

    # Full run with best params
    print(f"\n  Running full simulation with best params...")
    sim = ReactionDiffusion3D(f_base=best_params[0], k_base=best_params[1])
    sim.init_random_seed(seed_size=4)
    snapshots = sim.run(MAX_STEPS, verbose=True)
    save_snapshot("exp_a_pure_gs", sim)

    return best_params, results


# ── Experiment B: Single text injection ──

def experiment_b(f_base, k_base):
    print("\n" + "=" * 60)
    print("EXPERIMENT B: Single Text Injection")
    print("=" * 60)

    test_texts = [
        ("criminal", "故意伤害他人身体"),
        ("labor", "解除劳动合同赔偿"),
        ("civil", "离婚后财产分割"),
        ("criminal_heavy", "故意伤害他人身体致人重伤"),
        ("admin", "交通事故责任认定"),
    ]

    results = []
    fields = {}

    for name, text in test_texts:
        print(f"\n  --- {name}: '{text}' ---")

        sim = ReactionDiffusion3D(f_base=f_base, k_base=k_base)
        sim.init_uniform_with_noise(noise_level=0.001)

        # Inject tokens
        positions = inject_tokens(sim, text)
        print(f"  Injected {len(positions)} tokens")
        for tok, x, y, z in positions:
            print(f"    '{tok}' → ({x},{y},{z})")

        # Evolve
        sim.run(MAX_STEPS, verbose=True)
        save_snapshot(f"exp_b_{name}", sim)

        v_std = sim.v.std()
        v_max = sim.v.max()
        energy = sim.compute_energy()
        has_pattern = sim.has_pattern()

        print(f"  Pattern: {'YES' if has_pattern else 'NO'} v_std={v_std:.4f} v_max={v_max:.4f} energy={energy:.2f}")

        fields[name] = sim.v.copy()
        results.append({
            "name": name, "text": text,
            "n_tokens": len(positions),
            "has_pattern": has_pattern,
            "v_std": float(v_std), "v_max": float(v_max),
            "energy": float(energy)
        })

    return fields, results


# ── Experiment C: Similar texts comparison ──

def experiment_c(fields):
    print("\n" + "=" * 60)
    print("EXPERIMENT C: Similar Texts (Quantitative Change)")
    print("=" * 60)

    v1 = fields.get("criminal")
    v2 = fields.get("criminal_heavy")

    if v1 is None or v2 is None:
        print("  SKIP: missing fields")
        return {}

    dist = field_distance(v1, v2)
    corr = field_correlation(v1, v2)

    print(f"  '故意伤害他人身体' vs '故意伤害他人身体致人重伤'")
    print(f"  L2 distance: {dist:.6f}")
    print(f"  Correlation: {corr:.6f}")
    print(f"  {'SIMILAR but DIFFERENT' if 0.3 < corr < 0.95 else 'TOO SIMILAR' if corr > 0.95 else 'TOO DIFFERENT'}")

    return {"distance": dist, "correlation": corr}


# ── Experiment D: Cross-domain comparison ──

def experiment_d(fields):
    print("\n" + "=" * 60)
    print("EXPERIMENT D: Cross-Domain Comparison")
    print("=" * 60)

    pairs = [
        ("criminal", "labor"),
        ("criminal", "civil"),
        ("criminal", "admin"),
        ("labor", "civil"),
        ("labor", "admin"),
        ("civil", "admin"),
    ]

    results = []
    for n1, n2 in pairs:
        v1 = fields.get(n1)
        v2 = fields.get(n2)
        if v1 is None or v2 is None:
            continue
        dist = field_distance(v1, v2)
        corr = field_correlation(v1, v2)
        print(f"  {n1:16s} vs {n2:16s}: dist={dist:.6f} corr={corr:.6f}")
        results.append({"pair": f"{n1}_vs_{n2}", "distance": dist, "correlation": corr})

    return results


# ── Experiment E: Query-Doc Matching ──

def experiment_e(f_base, k_base):
    print("\n" + "=" * 60)
    print("EXPERIMENT E: Query-Doc Matching via Field Fusion")
    print("=" * 60)

    query = "他打我要怎么判"
    doc_relevant = "故意伤害他人身体"
    doc_irrelevant = "解除劳动合同赔偿"

    # Evolve each text separately
    texts = {
        "query": query,
        "doc_relevant": doc_relevant,
        "doc_irrelevant": doc_irrelevant,
    }

    v_fields = {}
    for name, text in texts.items():
        print(f"\n  Evolving '{text}'...")
        sim = ReactionDiffusion3D(f_base=f_base, k_base=k_base)
        sim.init_uniform_with_noise(noise_level=0.001)
        inject_tokens(sim, text)
        sim.run(MAX_STEPS, verbose=False)
        v_fields[name] = sim.v.copy()
        print(f"  Done: v_std={sim.v.std():.4f}")

    # Fusion tests
    print(f"\n  Fusion: query + relevant doc...")
    conv1, energy1, drop1 = fusion_test(v_fields["query"], v_fields["doc_relevant"],
                                         f_base=f_base, k_base=k_base)
    print(f"  Convergence: step {conv1}, energy={energy1:.2f}, drop={drop1:.2f}")

    print(f"\n  Fusion: query + irrelevant doc...")
    conv2, energy2, drop2 = fusion_test(v_fields["query"], v_fields["doc_irrelevant"],
                                         f_base=f_base, k_base=k_base)
    print(f"  Convergence: step {conv2}, energy={energy2:.2f}, drop={drop2:.2f}")

    print(f"\n  === Fusion Result ===")
    print(f"  Relevant:   conv_step={conv1} energy_drop={drop1:.4f}")
    print(f"  Irrelevant: conv_step={conv2} energy_drop={drop2:.4f}")
    if conv1 < conv2:
        print(f"  ✓ Relevant doc fuses FASTER → correct discrimination")
    elif conv1 > conv2:
        print(f"  ✗ Irrelevant doc fuses faster → wrong")
    else:
        print(f"  = Same convergence speed → no discrimination")

    return {
        "query": query,
        "relevant": {"doc": doc_relevant, "conv_step": conv1, "energy_drop": float(drop1)},
        "irrelevant": {"doc": doc_irrelevant, "conv_step": conv2, "energy_drop": float(drop2)},
        "correct": conv1 < conv2
    }


def main():
    print("=" * 60)
    print("MaoField Exp004: 3D Reaction-Diffusion Semantic Field")
    print("=" * 60)
    t0 = time.time()

    # A: Find working parameters
    best_params, a_results = experiment_a()
    f_base, k_base = best_params

    # B: Single text injection
    fields, b_results = experiment_b(f_base, k_base)

    # C: Similar texts
    c_results = experiment_c(fields)

    # D: Cross-domain
    d_results = experiment_d(fields)

    # E: Query-Doc matching
    e_results = experiment_e(f_base, k_base)

    # Save all results
    all_results = {
        "meta": {"date": "2026-04-10", "grid_size": GRID_SIZE, "max_steps": MAX_STEPS},
        "best_params": {"F": best_params[0], "k": best_params[1]},
        "exp_a_param_scan": a_results,
        "exp_b_injection": b_results,
        "exp_c_similar": c_results,
        "exp_d_cross_domain": d_results,
        "exp_e_matching": e_results,
    }

    out_path = os.path.join(ANALYSIS_DIR, "exp004_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n\nSaved: {out_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
