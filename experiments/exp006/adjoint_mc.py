"""
MaoField Exp006: Multi-Component Adjoint Iteration
====================================================

G: per-component energy density -> coupling with corpus source fields
c_total = sum_i |c_i| where c_i = integral e_i(x) * S_i_corpus(x) dx
"""

import numpy as np
from simulator_mc import (
    evolve_steps_mc, compute_energy_mc,
    compute_energy_density_mc, compute_residual_mc
)
from config import D, DT, DX, INTERACT_STEPS, RELAX_STEPS, TOP_K


def compute_coupling_mc(e_list, S_corpus_mc_list):
    """Multi-component coupling: c_total = sum_i |integral e_i * S_i_corpus|.

    Args:
        e_list: list of per-component energy density arrays [e_0, e_1, ...]
        S_corpus_mc_list: list of corpus entries, each entry is [S_0, S_1, ...]

    Returns:
        couplings: array of total coupling strengths, one per corpus entry
    """
    n_corpus = len(S_corpus_mc_list)
    couplings = np.zeros(n_corpus)
    for j in range(n_corpus):
        c_total = 0.0
        for i, e_i in enumerate(e_list):
            c_i = float(np.sum(e_i * S_corpus_mc_list[j][i]))
            c_total += abs(c_i)
        couplings[j] = c_total
    return couplings


def select_practice_targets(couplings, k=TOP_K):
    """Select top-k by coupling strength (already absolute)."""
    if k >= len(couplings):
        return np.argsort(couplings)[::-1]
    return np.argsort(couplings)[-k:][::-1]


def practice_with_targets_mc(u_list, S_query_list, target_indices,
                              S_corpus_mc_list, lambdas,
                              interact_steps=INTERACT_STEPS,
                              relax_steps=RELAX_STEPS):
    """Interact with selected corpus, then relax (multi-component)."""
    for idx in target_indices:
        S_corpus_entry = S_corpus_mc_list[idx]
        # Combined source = query + corpus, per component
        S_combined = []
        for i in range(len(u_list)):
            sc = S_query_list[i] + S_corpus_entry[i]
            mx = max(abs(sc.max()), abs(sc.min()))
            if mx > 0:
                sc = sc / mx
            S_combined.append(sc)
        # Interact
        u_list = evolve_steps_mc(u_list, S_combined, D, DT, DX,
                                  interact_steps, lambdas)
        # Relax with query only
        u_list = evolve_steps_mc(u_list, S_query_list, D, DT, DX,
                                  relax_steps, lambdas)
    return u_list


def adjoint_iteration_mc(u_list, S_query_list, S_corpus_mc_list, lambdas,
                          corpus_texts=None, max_rounds=5,
                          convergence_tol=0.01, k=TOP_K):
    """Full F<->G adjoint iteration for multi-component fields."""
    history = []
    prev_metric = None

    for round_idx in range(max_rounds):
        # G: compute energy density per component
        e_list = compute_energy_density_mc(u_list, S_query_list, D, DX, lambdas)
        r_list = compute_residual_mc(u_list, S_query_list, D, DX, lambdas)

        r_norm = float(np.sqrt(sum(np.sum(r**2) for r in r_list)))
        e_std = float(np.mean([np.std(e) for e in e_list]))

        # Coupling
        couplings = compute_coupling_mc(e_list, S_corpus_mc_list)
        targets = select_practice_targets(couplings, k=k)

        metric = e_std

        round_info = {
            'round': round_idx,
            'r_norm': r_norm,
            'e_std': e_std,
            'coupling_max': float(np.max(couplings)),
            'targets': len(targets),
            'metric': float(metric),
        }
        history.append(round_info)
        print(f"    Round {round_idx}: ‖r‖={r_norm:.4f} e_std={e_std:.4f} "
              f"coupling_max={round_info['coupling_max']:.4f} targets={len(targets)}")

        # Convergence check
        if prev_metric is not None:
            change = abs(metric - prev_metric) / (abs(prev_metric) + 1e-10)
            print(f"      metric change: {change:.4f}")
            if change < convergence_tol:
                print(f"      Converged at round {round_idx}.")
                break
        prev_metric = metric

        # F: practice with selected corpus
        u_list = practice_with_targets_mc(
            u_list, S_query_list, targets, S_corpus_mc_list, lambdas)

    return u_list, history


def blind_practice_mc(u_list, S_query_list, S_corpus_mc_list, indices,
                       lambdas, interact_steps=INTERACT_STEPS,
                       relax_steps=RELAX_STEPS):
    """Blind practice for multi-component fields (condition A baseline)."""
    for i_step, idx in enumerate(indices):
        S_corpus_entry = S_corpus_mc_list[idx]
        S_combined = []
        for c in range(len(u_list)):
            sc = S_query_list[c] + S_corpus_entry[c]
            mx = max(abs(sc.max()), abs(sc.min()))
            if mx > 0:
                sc = sc / mx
            S_combined.append(sc)
        u_list = evolve_steps_mc(u_list, S_combined, D, DT, DX,
                                  interact_steps, lambdas)
        u_list = evolve_steps_mc(u_list, S_query_list, D, DT, DX,
                                  relax_steps, lambdas)
        if (i_step + 1) % 10 == 0:
            e = compute_energy_mc(u_list, S_query_list, D, DX, lambdas)
            print(f"      Blind practice {i_step+1}/{len(indices)}: E={e:.0f}")
    return u_list
