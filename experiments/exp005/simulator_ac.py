"""
MaoField Exp005: Allen-Cahn 3D PDE Solver
==========================================
Reused from exp004 with minor cleanup.

From Lagrangian L = ∫[D/2|∇u|² + V(u) - (1-u²)·u·S] dΩ
Gradient flow: ∂u/∂t = D∇²u - u³ + u + (1-3u²)·S(x;t)
Double-well potential V(u) = ¼(u²-1)²
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


def evolve_steps(u, S, D, dt, dx, n_steps):
    """Run Allen-Cahn n_steps with source S."""
    for _ in range(n_steps):
        lap = laplacian_3d_periodic(u, dx)
        coupling = (1.0 - 3.0 * u * u) * S
        u = u + dt * (D * lap - u**3 + u + coupling)
        u = np.clip(u, -2, 2)
    return u


def compute_energy(u, S, D, dx):
    """Total free energy L[u, S]."""
    gx = np.roll(u, -1, 0) - u
    gy = np.roll(u, -1, 1) - u
    gz = np.roll(u, -1, 2) - u
    grad_energy = 0.5 * D * (gx**2 + gy**2 + gz**2)
    potential = 0.25 * (u**2 - 1)**2
    coupling = -(1.0 - u**2) * u * S
    return float(np.sum(grad_energy + potential + coupling)) * dx**3


def compute_energy_density(u, S, D, dx):
    """Local energy density e(x) — nonzero even at equilibrium."""
    gx = np.roll(u, -1, 0) - u
    gy = np.roll(u, -1, 1) - u
    gz = np.roll(u, -1, 2) - u
    grad_energy = 0.5 * D * (gx**2 + gy**2 + gz**2)
    potential = 0.25 * (u**2 - 1)**2
    coupling = -(1.0 - u**2) * u * S
    return grad_energy + potential + coupling


def compute_residual(u, S, D, dx):
    """Residual imbalance r(x) = D∇²u - u³ + u + (1-3u²)·S.
    At perfect equilibrium r(x) = 0. In practice, nonzero."""
    lap = laplacian_3d_periodic(u, dx)
    return D * lap - u**3 + u + (1.0 - 3.0 * u * u) * S
