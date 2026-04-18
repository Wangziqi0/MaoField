"""
MaoField Exp004 (Revised): Allen-Cahn 3D PDE Solver
=====================================================

From Lagrangian L = ∫[D/2|∇u|² + V(u) - u·S] dΩ
Gradient flow: ∂u/∂t = D∇²u - u³ + u + S(x;t)

Double-well potential V(u) = ¼(u²-1)²
Minima at u=+1 and u=-1 → domains spontaneously form
"""

import numpy as np
from config import GRID_SIZE, SNAPSHOTS_DIR
import os


def laplacian_3d_periodic(field, dx):
    """3D Laplacian with periodic boundary"""
    return (
        np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
        np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) +
        np.roll(field, 1, axis=2) + np.roll(field, -1, axis=2) -
        6 * field
    ) / (dx * dx)


class AllenCahn3D:
    def __init__(self, grid_size=GRID_SIZE, D=0.5, dt=0.1, dx=1.0):
        self.N = grid_size
        self.D = D
        self.dt = dt
        self.dx = dx

        # Field u: starts near 0 (unstable equilibrium)
        self.u = np.zeros((grid_size, grid_size, grid_size), dtype=np.float64)

        # Source field S: initially zero (set by token injection)
        self.S = np.zeros((grid_size, grid_size, grid_size), dtype=np.float64)

        self.step_count = 0
        self.energy_history = []

    def init_noise(self, noise_level=0.05, rng=None):
        """Initialize u ≈ 0 + small noise (unstable, should split into ±1 domains)"""
        if rng is None:
            rng = np.random.RandomState(42)
        self.u = noise_level * rng.randn(self.N, self.N, self.N)

    def step(self):
        """One Euler step: ∂u/∂t = D∇²u - u³ + u + (1-3u²)·S
        The (1-3u²) factor is from variational derivation of nonlinear coupling.
        Self-adaptive: source vanishes at |u|≈1 (already decided regions)."""
        lap = laplacian_3d_periodic(self.u, self.dx)
        coupling = (1.0 - 3.0 * self.u * self.u) * self.S
        dudt = self.D * lap - self.u**3 + self.u + coupling
        self.u += dudt * self.dt
        self.u = np.clip(self.u, -1.5, 1.5)
        self.step_count += 1

    def compute_energy(self):
        """
        Free energy: L = ∫[D/2|∇u|² + V(u) - u·S] dΩ
        V(u) = ¼(u²-1)²
        """
        # Gradient energy (approximate)
        grad_x = np.roll(self.u, -1, axis=0) - self.u
        grad_y = np.roll(self.u, -1, axis=1) - self.u
        grad_z = np.roll(self.u, -1, axis=2) - self.u
        grad_energy = 0.5 * self.D * (grad_x**2 + grad_y**2 + grad_z**2)

        # Double-well potential
        potential = 0.25 * (self.u**2 - 1)**2

        # Nonlinear source coupling: -(1-u²)·u·S
        source_coupling = -(1.0 - self.u**2) * self.u * self.S

        total = float(np.sum(grad_energy + potential + source_coupling)) * self.dx**3
        return total

    def run(self, n_steps, snapshot_interval=100, verbose=True):
        """Run simulation, collecting snapshots and energy"""
        snapshots = []
        for i in range(n_steps):
            self.step()
            if (i + 1) % snapshot_interval == 0:
                energy = self.compute_energy()
                self.energy_history.append((self.step_count, energy))
                snapshots.append((self.step_count, self.u.copy()))
                if verbose and (i + 1) % (snapshot_interval * 10) == 0:
                    u_mean = self.u.mean()
                    u_std = self.u.std()
                    pos_frac = (self.u > 0.5).mean()
                    neg_frac = (self.u < -0.5).mean()
                    print(f"  Step {self.step_count}: E={energy:.1f} mean={u_mean:.4f} std={u_std:.4f} +1域={pos_frac:.2%} -1域={neg_frac:.2%}")
        return snapshots

    def has_domains(self):
        """Check if u has split into ±1 domains"""
        pos_frac = (self.u > 0.5).mean()
        neg_frac = (self.u < -0.5).mean()
        # Both domains should be present and non-trivial
        return pos_frac > 0.1 and neg_frac > 0.1

    def domain_wall_fraction(self):
        """Fraction of grid points on domain walls (|u| < 0.5)"""
        return float((np.abs(self.u) < 0.5).mean())


def update_source(S_q, S_d, u):
    """
    Source field modified by current state.
    Already-understood regions (|u|≈1) suppress source.
    Undecided regions (|u|≈0, domain walls) keep full source.
    """
    suppression = 1.0 - np.abs(u)
    suppression = np.clip(suppression, 0.1, 1.0)
    return (S_q + S_d) * suppression


def evolve_to_equilibrium(u_init, S, D, dt, dx, max_steps=5000, tol=1e-4):
    """Evolve Allen-Cahn until energy stabilizes"""
    sim = AllenCahn3D(grid_size=u_init.shape[0], D=D, dt=dt, dx=dx)
    sim.u = u_init.copy()
    sim.S = S.copy()

    prev_energy = sim.compute_energy()
    for step in range(max_steps):
        sim.step()
        if (step + 1) % 50 == 0:
            energy = sim.compute_energy()
            if abs(energy - prev_energy) / (abs(prev_energy) + 1e-10) < tol:
                return sim.u, energy, step + 1
            prev_energy = energy

    return sim.u, sim.compute_energy(), max_steps


def iterative_fusion(u_q, u_d, S_q, S_d, D=0.5, dt=0.1, dx=1.0,
                     max_rounds=10, tol=1e-3):
    """
    Spiral ascent: query and doc fields iteratively fuse.
    Each round: merge → evolve → update both fields.
    """
    energies = []

    for rnd in range(max_rounds):
        # Merge
        u = 0.5 * (u_q + u_d)

        # Combined source (modified by current state)
        S_combined = update_source(S_q, S_d, u)

        # Evolve to equilibrium
        u_new, energy, conv_steps = evolve_to_equilibrium(u, S_combined, D, dt, dx)
        energies.append(energy)

        # Update both fields from fused result
        # Query learns from doc's contribution
        alpha = 0.3  # learning rate
        u_q = (1 - alpha) * u_q + alpha * u_new
        u_d = (1 - alpha) * u_d + alpha * u_new

        # Convergence check
        if rnd > 0 and abs(energies[-1] - energies[-2]) / (abs(energies[-2]) + 1e-10) < tol:
            break

    return rnd + 1, energies[-1], energies


if __name__ == "__main__":
    print("Testing Allen-Cahn 3D simulator...")
    print("Verifying double-well potential domain formation\n")

    # Parameter scan for D
    for D in [0.1, 0.2, 0.5, 1.0, 2.0]:
        sim = AllenCahn3D(D=D)
        sim.init_noise(noise_level=0.05)
        sim.run(5000, snapshot_interval=5000, verbose=False)
        has = sim.has_domains()
        wall = sim.domain_wall_fraction()
        pos = (sim.u > 0.5).mean()
        neg = (sim.u < -0.5).mean()
        print(f"  D={D:.1f}: domains={'YES' if has else 'NO'} +1={pos:.2%} -1={neg:.2%} wall={wall:.2%}")

    # Full run with best D
    print("\nFull run with D=0.5...")
    sim = AllenCahn3D(D=0.5)
    sim.init_noise(noise_level=0.05)
    snapshots = sim.run(10000, verbose=True)
    print(f"\nDomains formed: {sim.has_domains()}")
    print(f"Domain wall fraction: {sim.domain_wall_fraction():.2%}")
    np.save(os.path.join(SNAPSHOTS_DIR, "exp_a_allen_cahn_u.npy"), sim.u)
    print("Saved.")
