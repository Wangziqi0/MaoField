"""
MaoField Exp006: Multi-Component Allen-Cahn PDE Solver
=======================================================

Multi-component Lagrangian:
  L = integral[ sum_i D_i/2|grad u_i|^2 + V(u) - sum_i (1-u_i^2)*u_i*S_i ] dOmega

Double-well + cross-coupling potential:
  V(u1, u2) = 1/4(u1^2-1)^2 + 1/4(u2^2-1)^2 + lambda*u1*u2

Field equations (variational):
  du_i/dt = D*lap(u_i) - u_i^3 + u_i - sum_{j!=i} lambda_ij*u_j + (1-3u_i^2)*S_i
"""

import numpy as np


def laplacian_3d_periodic(field, dx):
    """3D Laplacian with periodic boundary conditions."""
    return (
        np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
        np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) +
        np.roll(field, 1, axis=2) + np.roll(field, -1, axis=2) -
        6 * field
    ) / (dx * dx)


def evolve_steps_mc(u_list, S_list, D, dt, dx, n_steps, lambdas):
    """Multi-component Allen-Cahn evolution.

    Args:
        u_list: list of 3D arrays, one per component
        S_list: list of 3D source fields, one per component
        D: diffusion coefficient (same for all)
        dt, dx: time and space steps
        n_steps: number of evolution steps
        lambdas: dict of (i,j)->lambda_ij coupling constants
                 e.g. {(0,1): 0.1} for 2-component

    Returns:
        u_list: evolved fields (new list, same arrays mutated)
    """
    n_comp = len(u_list)
    u_list = [u.copy() for u in u_list]

    for _ in range(n_steps):
        new_u = []
        for i in range(n_comp):
            lap = laplacian_3d_periodic(u_list[i], dx)
            coupling_src = (1.0 - 3.0 * u_list[i]**2) * S_list[i]
            # Cross-coupling: -lambda_ij * u_j for each j != i
            cross = np.zeros_like(u_list[i])
            for j in range(n_comp):
                if j != i:
                    key = (min(i, j), max(i, j))
                    lam = lambdas.get(key, 0.0)
                    if lam != 0.0:
                        cross += lam * u_list[j]
            du = D * lap - u_list[i]**3 + u_list[i] - cross + coupling_src
            new_u.append(np.clip(u_list[i] + dt * du, -2, 2))
        u_list = new_u

    return u_list


def compute_energy_mc(u_list, S_list, D, dx, lambdas):
    """Total free energy for multi-component field."""
    energy = 0.0
    n_comp = len(u_list)

    for i in range(n_comp):
        u = u_list[i]
        S = S_list[i]
        gx = np.roll(u, -1, 0) - u
        gy = np.roll(u, -1, 1) - u
        gz = np.roll(u, -1, 2) - u
        grad_energy = 0.5 * D * (gx**2 + gy**2 + gz**2)
        potential = 0.25 * (u**2 - 1)**2
        coupling = -(1.0 - u**2) * u * S
        energy += float(np.sum(grad_energy + potential + coupling))

    # Cross-coupling energy: lambda_ij * u_i * u_j
    for (i, j), lam in lambdas.items():
        if lam != 0.0:
            energy += lam * float(np.sum(u_list[i] * u_list[j]))

    return energy * dx**3


def compute_energy_density_mc(u_list, S_list, D, dx, lambdas):
    """Per-component energy density arrays."""
    densities = []
    n_comp = len(u_list)

    for i in range(n_comp):
        u = u_list[i]
        S = S_list[i]
        gx = np.roll(u, -1, 0) - u
        gy = np.roll(u, -1, 1) - u
        gz = np.roll(u, -1, 2) - u
        grad_energy = 0.5 * D * (gx**2 + gy**2 + gz**2)
        potential = 0.25 * (u**2 - 1)**2
        coupling = -(1.0 - u**2) * u * S
        densities.append(grad_energy + potential + coupling)

    return densities


def compute_residual_mc(u_list, S_list, D, dx, lambdas):
    """Per-component residual imbalance."""
    residuals = []
    n_comp = len(u_list)

    for i in range(n_comp):
        lap = laplacian_3d_periodic(u_list[i], dx)
        cross = np.zeros_like(u_list[i])
        for j in range(n_comp):
            if j != i:
                key = (min(i, j), max(i, j))
                lam = lambdas.get(key, 0.0)
                if lam != 0.0:
                    cross += lam * u_list[j]
        r = D * lap - u_list[i]**3 + u_list[i] - cross + (1.0 - 3.0 * u_list[i]**2) * S_list[i]
        residuals.append(r)

    return residuals
