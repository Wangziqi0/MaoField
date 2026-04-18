"""
MaoField Exp004: Iterative Fusion
==================================

Spiral ascent: query and doc fields iteratively fuse.
No hand-written scoring. Convergence speed and energy ARE the metrics.
"""

import numpy as np
from simulator_ac import AllenCahn3D, laplacian_3d_periodic


def evolve_text_to_steady(tokens_source, D=0.1, dt=0.1, dx=1.0,
                          grid_size=32, max_steps=5000, noise=0.01):
    """
    Evolve a text's source field to steady state.
    Returns: (final_u, sim)
    """
    sim = AllenCahn3D(grid_size=grid_size, D=D, dt=dt, dx=dx)
    sim.init_noise(noise_level=noise)
    sim.S = tokens_source.copy()
    sim.run(max_steps, snapshot_interval=max_steps, verbose=False)
    return sim.u.copy(), sim


def iterative_fusion(u_q, u_d, S_q, S_d, D=0.1, dt=0.1, dx=1.0,
                     max_rounds=10, inner_steps=2000, tol=1e-3,
                     grid_size=32, verbose=True):
    """
    Spiral ascent fusion of two fields.

    Each round:
    1. Merge u_q and u_d
    2. Evolve under combined source (with self-adaptive coupling)
    3. Update both fields toward fused state
    4. Check convergence

    Returns: (n_rounds, final_energy, energy_history)
    """
    energies = []

    for r in range(max_rounds):
        # Merge
        u = 0.5 * (u_q + u_d)

        # Combined source
        S = S_q + S_d
        if S.max() > 0:
            S = S / S.max()  # renormalize

        # Evolve to equilibrium with modified Allen-Cahn
        for step in range(inner_steps):
            lap = laplacian_3d_periodic(u, dx)
            coupling = (1.0 - 3.0 * u * u) * S
            dudt = D * lap - u**3 + u + coupling
            u_new = u + dt * dudt
            u_new = np.clip(u_new, -1.5, 1.5)

            if step > 0 and step % 100 == 0:
                change = np.max(np.abs(u_new - u))
                if change < 1e-5:
                    break
            u = u_new

        # Energy
        grad_x = np.roll(u, -1, axis=0) - u
        grad_y = np.roll(u, -1, axis=1) - u
        grad_z = np.roll(u, -1, axis=2) - u
        grad_energy = 0.5 * D * (grad_x**2 + grad_y**2 + grad_z**2)
        potential = 0.25 * (u**2 - 1)**2
        source_coupling = -(1.0 - u**2) * u * S
        energy = float(np.sum(grad_energy + potential + source_coupling))
        energies.append(energy)

        if verbose:
            pos = (u > 0.5).mean()
            neg = (u < -0.5).mean()
            print(f"    Round {r+1}: E={energy:.1f} +1={pos:.1%} -1={neg:.1%} inner_steps={step+1}")

        # Update both fields (spiral: each learns from fusion)
        alpha = 0.3
        u_q = (1 - alpha) * u_q + alpha * u
        u_d = (1 - alpha) * u_d + alpha * u

        # Convergence
        if r > 0 and abs(energies[-1] - energies[-2]) / (abs(energies[-2]) + 1e-10) < tol:
            if verbose:
                print(f"    Converged at round {r+1}")
            break

    return r + 1, energies[-1], energies
