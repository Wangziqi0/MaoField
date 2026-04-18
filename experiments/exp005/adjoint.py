"""
MaoField Exp005: Adjoint Functor Implementation
=================================================

G = field's residual imbalance / energy density map.
Demand-driven practice selection via physical coupling.
Full F⇄G adjoint iteration.
"""

import numpy as np
from simulator_ac import (
    laplacian_3d_periodic, evolve_steps,
    compute_energy, compute_energy_density, compute_residual
)
from config import D, DT, DX, INTERACT_STEPS, RELAX_STEPS, TOP_K


def compute_coupling_residual(r, S_corpus_list):
    """Coupling between residual imbalance r(x) and each corpus source field.
    c_i = ∫ r(x) · S_i(x) dx  (volume integral = physical coupling energy)
    """
    couplings = np.array([float(np.sum(r * S_i)) for S_i in S_corpus_list])
    return couplings


def compute_coupling_energy(e, S_corpus_list):
    """Coupling between energy density e(x) and each corpus source field.
    c_i = ∫ e(x) · S_i(x) dx
    High energy regions coupling with source = where the field "needs" this text.
    """
    couplings = np.array([float(np.sum(e * S_i)) for S_i in S_corpus_list])
    return couplings


def select_practice_targets(couplings, k=TOP_K):
    """Select top-k corpus items by absolute coupling strength."""
    abs_c = np.abs(couplings)
    if k >= len(couplings):
        return np.argsort(abs_c)[::-1]
    indices = np.argsort(abs_c)[-k:][::-1]
    return indices


def practice_with_targets(u, S_query, target_indices, S_corpus_list,
                          interact_steps=INTERACT_STEPS,
                          relax_steps=RELAX_STEPS):
    """Interact with selected corpus texts sequentially, then relax.
    Relaxation uses S_query (query context stays; corpus removed).
    """
    for idx in target_indices:
        S_i = S_corpus_list[idx]
        S_combined = S_query + S_i
        mx = max(abs(S_combined.max()), abs(S_combined.min()))
        if mx > 0:
            S_combined = S_combined / mx
        # Interact
        u = evolve_steps(u, S_combined, D, DT, DX, interact_steps)
        # Relax: remove corpus, keep query context
        u = evolve_steps(u, S_query, D, DT, DX, relax_steps)
    return u


def adjoint_iteration(u, S_query, S_corpus_list, corpus_texts=None,
                      max_rounds=5, convergence_tol=0.01, k=TOP_K,
                      coupling_mode='energy'):
    """Full F⇄G adjoint iteration.

    Args:
        u: initial field (after init_steps evolution)
        S_query: query source field
        S_corpus_list: list of precomputed corpus source fields
        corpus_texts: optional, for logging
        max_rounds: max iteration rounds
        convergence_tol: stop if relative change in metric < this
        k: number of practice targets per round
        coupling_mode: 'energy' (default, safer) or 'residual'

    Returns:
        u: field after adjoint iteration
        history: list of dicts with diagnostics per round
    """
    history = []
    prev_metric = None

    for round_idx in range(max_rounds):
        # === G: compute imbalance ===
        r = compute_residual(u, S_query, D, DX)
        r_norm = float(np.sqrt(np.sum(r**2)))

        e = compute_energy_density(u, S_query, D, DX)
        e_total = float(np.sum(e))
        e_std = float(np.std(e))

        # Coupling computation
        if coupling_mode == 'residual':
            couplings = compute_coupling_residual(r, S_corpus_list)
            metric = r_norm
        else:  # 'energy'
            couplings = compute_coupling_energy(e, S_corpus_list)
            metric = e_std  # energy density spread

        # Select practice targets
        targets = select_practice_targets(couplings, k=k)

        # Diagnostics
        round_info = {
            'round': round_idx,
            'r_norm': r_norm,
            'e_total': e_total,
            'e_std': e_std,
            'coupling_mode': coupling_mode,
            'coupling_max': float(np.max(np.abs(couplings))),
            'coupling_min_selected': float(np.abs(couplings[targets[-1]])) if len(targets) > 0 else 0,
            'coupling_mean_all': float(np.mean(np.abs(couplings))),
            'selected_indices': targets.tolist(),
            'selected_couplings': [float(couplings[i]) for i in targets],
            'metric': float(metric),
        }
        if corpus_texts is not None:
            round_info['selected_texts'] = [corpus_texts[i][:30] for i in targets]

        history.append(round_info)
        print(f"    Round {round_idx}: ‖r‖={r_norm:.4f} e_std={e_std:.4f} "
              f"coupling_max={round_info['coupling_max']:.4f} "
              f"targets={len(targets)}")

        # Convergence check
        if prev_metric is not None:
            change = abs(metric - prev_metric) / (abs(prev_metric) + 1e-10)
            print(f"      metric change: {change:.4f}")
            if change < convergence_tol:
                print(f"      Converged at round {round_idx}.")
                break
        prev_metric = metric

        # === F: practice with selected corpus ===
        u = practice_with_targets(u, S_query, targets, S_corpus_list)

    return u, history


def blind_practice(u, S_query, S_corpus_list, indices,
                   interact_steps=INTERACT_STEPS,
                   relax_steps=RELAX_STEPS):
    """Blind practice: interact with given indices in order (no G selection).
    For condition B comparison.
    """
    for i, idx in enumerate(indices):
        S_i = S_corpus_list[idx]
        S_combined = S_query + S_i
        mx = max(abs(S_combined.max()), abs(S_combined.min()))
        if mx > 0:
            S_combined = S_combined / mx
        u = evolve_steps(u, S_combined, D, DT, DX, interact_steps)
        u = evolve_steps(u, S_query, D, DT, DX, relax_steps)
        if (i + 1) % 10 == 0:
            e = compute_energy(u, S_query, D, DX)
            print(f"      Blind practice {i+1}/{len(indices)}: E={e:.0f}")
    return u
