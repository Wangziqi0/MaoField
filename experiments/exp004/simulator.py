"""
MaoField Exp004: 3D Reaction-Diffusion PDE Solver
===================================================

Gray-Scott model on 32³ grid with periodic boundary.

∂u/∂t = D_u ∇²u - u*v² + F*(1-u)
∂v/∂t = D_v ∇²v + u*v² - (F+k)*v

F and k can be spatially varying (injected by tokens).
"""

import numpy as np
from config import *


def laplacian_3d_periodic(field, dx):
    """3D Laplacian with periodic boundary using np.roll"""
    return (
        np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
        np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) +
        np.roll(field, 1, axis=2) + np.roll(field, -1, axis=2) -
        6 * field
    ) / (dx * dx)


class ReactionDiffusion3D:
    def __init__(self, grid_size=GRID_SIZE, d_u=D_U, d_v=D_V,
                 f_base=F_BASE, k_base=K_BASE, dt=DT, dx=DX):
        self.N = grid_size
        self.d_u = d_u
        self.d_v = d_v
        self.dt = dt
        self.dx = dx

        # Fields: u (activator), v (inhibitor)
        self.u = np.ones((grid_size, grid_size, grid_size), dtype=np.float64)
        self.v = np.zeros((grid_size, grid_size, grid_size), dtype=np.float64)

        # Spatially varying F and k (can be modified by token injection)
        self.F = np.full((grid_size, grid_size, grid_size), f_base, dtype=np.float64)
        self.k = np.full((grid_size, grid_size, grid_size), k_base, dtype=np.float64)

        self.step_count = 0
        self.energy_history = []

    def init_random_seed(self, seed_size=5, rng=None):
        """Initialize with small random perturbation in center region"""
        if rng is None:
            rng = np.random.RandomState(42)
        c = self.N // 2
        r = seed_size
        # Add small perturbation to v in center
        self.v[c-r:c+r, c-r:c+r, c-r:c+r] = 0.25 + 0.05 * rng.randn(2*r, 2*r, 2*r)
        # Slightly reduce u in center
        self.u[c-r:c+r, c-r:c+r, c-r:c+r] = 0.75 + 0.05 * rng.randn(2*r, 2*r, 2*r)

    def init_uniform_with_noise(self, noise_level=0.01, rng=None):
        """Initialize u=1, v=0 with small global noise"""
        if rng is None:
            rng = np.random.RandomState(42)
        self.u = np.ones((self.N, self.N, self.N)) + noise_level * rng.randn(self.N, self.N, self.N)
        self.v = noise_level * np.abs(rng.randn(self.N, self.N, self.N))

    def step(self):
        """One Euler step of the Gray-Scott equations"""
        lap_u = laplacian_3d_periodic(self.u, self.dx)
        lap_v = laplacian_3d_periodic(self.v, self.dx)

        uv2 = self.u * self.v * self.v

        du = self.d_u * lap_u - uv2 + self.F * (1.0 - self.u)
        dv = self.d_v * lap_v + uv2 - (self.F + self.k) * self.v

        self.u += du * self.dt
        self.v += dv * self.dt

        # Clamp to [0, 1] for stability
        self.u = np.clip(self.u, 0.0, 1.0)
        self.v = np.clip(self.v, 0.0, 1.0)

        self.step_count += 1

    def compute_energy(self):
        """System energy: sum of v (pattern intensity)"""
        return float(np.sum(self.v))

    def run(self, n_steps, snapshot_interval=SNAPSHOT_INTERVAL, verbose=True):
        """Run simulation for n_steps, collecting snapshots and energy"""
        snapshots = []
        for i in range(n_steps):
            self.step()
            if (i + 1) % snapshot_interval == 0:
                energy = self.compute_energy()
                self.energy_history.append((self.step_count, energy))
                snapshots.append((self.step_count, self.u.copy(), self.v.copy()))
                if verbose and (i + 1) % (snapshot_interval * 10) == 0:
                    v_max = self.v.max()
                    v_mean = self.v.mean()
                    print(f"  Step {self.step_count}: energy={energy:.2f} v_max={v_max:.4f} v_mean={v_mean:.6f}")
        return snapshots

    def has_pattern(self, threshold=0.01):
        """Check if a non-trivial pattern has formed"""
        v_std = self.v.std()
        v_max = self.v.max()
        return v_std > threshold and v_max > 0.05

    def get_state(self):
        """Return current state as dict"""
        return {
            "u": self.u.copy(),
            "v": self.v.copy(),
            "F": self.F.copy(),
            "k": self.k.copy(),
            "step": self.step_count,
            "energy": self.compute_energy()
        }


if __name__ == "__main__":
    print("Testing 3D Gray-Scott simulator...")
    sim = ReactionDiffusion3D()
    sim.init_random_seed()
    print(f"Grid: {sim.N}³, D_u={sim.d_u}, D_v={sim.d_v}, F={F_BASE}, k={K_BASE}")
    print(f"dt={sim.dt}, stability limit: dt < {sim.dx**2 / (6*sim.d_u):.3f}")

    snapshots = sim.run(2000, snapshot_interval=200, verbose=True)
    print(f"\nPattern formed: {sim.has_pattern()}")
    print(f"v stats: max={sim.v.max():.4f} mean={sim.v.mean():.6f} std={sim.v.std():.6f}")
