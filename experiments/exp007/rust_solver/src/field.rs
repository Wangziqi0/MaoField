//! Single-component Allen-Cahn 3D PDE solver (reused from exp005/06).
//!
//! PDE: du/dt = D*lap(u) - u^3 + u + (1-3u^2)*S

use rayon::prelude::*;

pub const GRID: usize = 32;
pub const NCELLS: usize = GRID * GRID * GRID;
pub const D_COEFF: f64 = 0.1;
pub const DT: f64 = 0.1;
pub const DX: f64 = 1.0;

pub type Field3D = Vec<f64>;

#[inline(always)]
pub fn idx(x: usize, y: usize, z: usize) -> usize {
    x + y * GRID + z * GRID * GRID
}

#[inline(always)]
fn wrap(v: isize) -> usize {
    ((v % GRID as isize) + GRID as isize) as usize % GRID
}

/// Evolve single-component Allen-Cahn for n_steps.
pub fn evolve(u: &mut Field3D, s: &Field3D, n_steps: usize) {
    let inv_dx2 = 1.0 / (DX * DX);
    let mut new_u = vec![0.0f64; NCELLS];

    for _ in 0..n_steps {
        new_u.par_chunks_mut(GRID * GRID)
            .enumerate()
            .for_each(|(z, slab)| {
                let zm = wrap(z as isize - 1);
                let zp = wrap(z as isize + 1);
                for y in 0..GRID {
                    let ym = wrap(y as isize - 1);
                    let yp = wrap(y as isize + 1);
                    for x in 0..GRID {
                        let xm = wrap(x as isize - 1);
                        let xp = wrap(x as isize + 1);
                        let k = idx(x, y, z);
                        let ui = u[k];
                        let lap = (u[idx(xp, y, z)] + u[idx(xm, y, z)]
                            + u[idx(x, yp, z)] + u[idx(x, ym, z)]
                            + u[idx(x, y, zp)] + u[idx(x, y, zm)]
                            - 6.0 * ui) * inv_dx2;
                        let du = D_COEFF * lap - ui * ui * ui + ui
                            + (1.0 - 3.0 * ui * ui) * s[k];
                        slab[x + y * GRID] = (ui + DT * du).clamp(-2.0, 2.0);
                    }
                }
            });
        std::mem::swap(u, &mut new_u);
    }
}

/// Total free energy.
pub fn energy(u: &Field3D, s: &Field3D) -> f64 {
    let dx3 = DX * DX * DX;
    let sum: f64 = (0..NCELLS)
        .into_par_iter()
        .map(|k| {
            let x = k % GRID;
            let y = (k / GRID) % GRID;
            let z = k / (GRID * GRID);
            let xp = wrap(x as isize + 1);
            let yp = wrap(y as isize + 1);
            let zp = wrap(z as isize + 1);
            let ui = u[k];
            let gx = u[idx(xp, y, z)] - ui;
            let gy = u[idx(x, yp, z)] - ui;
            let gz = u[idx(x, y, zp)] - ui;
            let grad = 0.5 * D_COEFF * (gx * gx + gy * gy + gz * gz);
            let pot = 0.25 * (ui * ui - 1.0) * (ui * ui - 1.0);
            let coup = -(1.0 - ui * ui) * ui * s[k];
            grad + pot + coup
        })
        .sum();
    sum * dx3
}

/// Energy density field e(x).
pub fn energy_density(u: &Field3D, s: &Field3D) -> Field3D {
    let mut e = vec![0.0f64; NCELLS];
    e.par_chunks_mut(GRID * GRID)
        .enumerate()
        .for_each(|(z, slab)| {
            for y in 0..GRID {
                for x in 0..GRID {
                    let k = idx(x, y, z);
                    let xp = wrap(x as isize + 1);
                    let yp = wrap(y as isize + 1);
                    let zp = wrap(z as isize + 1);
                    let ui = u[k];
                    let gx = u[idx(xp, y, z)] - ui;
                    let gy = u[idx(x, yp, z)] - ui;
                    let gz = u[idx(x, y, zp)] - ui;
                    slab[x + y * GRID] = 0.5 * D_COEFF * (gx * gx + gy * gy + gz * gz)
                        + 0.25 * (ui * ui - 1.0) * (ui * ui - 1.0)
                        - (1.0 - ui * ui) * ui * s[k];
                }
            }
        });
    e
}

/// Initialize field with small random noise.
pub fn init_field(seed: u64) -> Field3D {
    let mut f = vec![0.0f64; NCELLS];
    let mut rng = seed;
    for v in f.iter_mut() {
        rng ^= rng << 13;
        rng ^= rng >> 7;
        rng ^= rng << 17;
        *v = (rng as f64 / u64::MAX as f64) * 0.02 - 0.01;
    }
    f
}

/// Normalize field to [-1, 1].
pub fn normalize(s: &mut Field3D) {
    let mx = s.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
    if mx > 0.0 {
        for v in s.iter_mut() {
            *v /= mx;
        }
    }
}
