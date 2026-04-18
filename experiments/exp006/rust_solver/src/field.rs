//! Multi-component Allen-Cahn 3D PDE solver.
//!
//! Field equations (variational from Lagrangian):
//!   du_i/dt = D*lap(u_i) - u_i^3 + u_i - sum_{j!=i} lambda_ij*u_j + (1-3*u_i^2)*S_i

use rayon::prelude::*;
use crate::config::*;

/// A single 3D scalar field stored as flat Vec<f64> of length NCELLS.
pub type Field3D = Vec<f64>;

/// Multi-component field: one Field3D per component.
pub type McField = Vec<Field3D>;

/// Lambda coupling matrix stored as flat upper-triangle.
/// For components i < j, index = i * n_comp + j.
#[derive(Clone)]
pub struct Lambdas {
    pub n_comp: usize,
    vals: Vec<f64>,
}

impl Lambdas {
    pub fn new(n_comp: usize, default: f64) -> Self {
        let mut vals = vec![0.0; n_comp * n_comp];
        for i in 0..n_comp {
            for j in (i + 1)..n_comp {
                vals[i * n_comp + j] = default;
                vals[j * n_comp + i] = default;
            }
        }
        Self { n_comp, vals }
    }

    pub fn zero(n_comp: usize) -> Self {
        Self {
            n_comp,
            vals: vec![0.0; n_comp * n_comp],
        }
    }

    #[inline(always)]
    pub fn get(&self, i: usize, j: usize) -> f64 {
        self.vals[i * self.n_comp + j]
    }
}

/// 3D index helpers
#[inline(always)]
pub fn idx(x: usize, y: usize, z: usize) -> usize {
    x + y * GRID + z * GRID * GRID
}

#[inline(always)]
fn wrap(v: isize) -> usize {
    ((v % GRID as isize) + GRID as isize) as usize % GRID
}

/// Compute Laplacian with periodic BC for a flat field.
fn laplacian(u: &[f64], out: &mut [f64]) {
    let inv_dx2 = 1.0 / (DX * DX);
    // Process z-slabs in parallel for NUMA locality
    out.par_chunks_mut(GRID * GRID)
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
                    let c = u[idx(x, y, z)];
                    let lap = u[idx(xp, y, z)] + u[idx(xm, y, z)]
                        + u[idx(x, yp, z)] + u[idx(x, ym, z)]
                        + u[idx(x, y, zp)] + u[idx(x, y, zm)]
                        - 6.0 * c;
                    slab[x + y * GRID] = lap * inv_dx2;
                }
            }
        });
}

/// Evolve multi-component Allen-Cahn for n_steps.
pub fn evolve_mc(u_list: &mut McField, s_list: &[Field3D], lambdas: &Lambdas, n_steps: usize) {
    let n_comp = u_list.len();
    let mut lap_buf = vec![0.0f64; NCELLS];
    let mut new_fields: Vec<Field3D> = (0..n_comp).map(|_| vec![0.0; NCELLS]).collect();

    for _ in 0..n_steps {
        for i in 0..n_comp {
            laplacian(&u_list[i], &mut lap_buf);

            // Precompute cross-coupling sum for component i
            // cross[k] = sum_{j!=i} lambda_ij * u_j[k]
            let new = &mut new_fields[i];

            // Parallel over cells - each z-slab independently
            new.par_chunks_mut(GRID * GRID)
                .enumerate()
                .for_each(|(z, slab)| {
                    let base = z * GRID * GRID;
                    for local in 0..GRID * GRID {
                        let k = base + local;
                        let ui = u_list[i][k];
                        let si = s_list[i][k];

                        // Cross-coupling
                        let mut cross = 0.0f64;
                        for j in 0..n_comp {
                            if j != i {
                                let lam = lambdas.get(i, j);
                                if lam != 0.0 {
                                    cross += lam * u_list[j][k];
                                }
                            }
                        }

                        let du = D_COEFF * lap_buf[k]
                            - ui * ui * ui + ui
                            - cross
                            + (1.0 - 3.0 * ui * ui) * si;

                        let v = ui + DT * du;
                        slab[local] = v.clamp(-2.0, 2.0);
                    }
                });
        }
        // Swap
        for i in 0..n_comp {
            std::mem::swap(&mut u_list[i], &mut new_fields[i]);
        }
    }
}

/// Total free energy for multi-component field.
pub fn energy_mc(u_list: &McField, s_list: &[Field3D], lambdas: &Lambdas) -> f64 {
    let n_comp = u_list.len();
    let dx3 = DX * DX * DX;

    let per_comp: f64 = (0..n_comp)
        .map(|i| {
            let u = &u_list[i];
            let s = &s_list[i];
            (0..NCELLS)
                .into_par_iter()
                .map(|k| {
                    let x = k % GRID;
                    let y = (k / GRID) % GRID;
                    let z = k / (GRID * GRID);
                    let xp = wrap(x as isize + 1);
                    let yp = wrap(y as isize + 1);
                    let zp = wrap(z as isize + 1);
                    let gx = u[idx(xp, y, z)] - u[idx(x, y, z)];
                    let gy = u[idx(x, yp, z)] - u[idx(x, y, z)];
                    let gz = u[idx(x, y, zp)] - u[idx(x, y, z)];
                    let grad = 0.5 * D_COEFF * (gx * gx + gy * gy + gz * gz);
                    let ui = u[k];
                    let pot = 0.25 * (ui * ui - 1.0) * (ui * ui - 1.0);
                    let coup = -(1.0 - ui * ui) * ui * s[k];
                    grad + pot + coup
                })
                .sum::<f64>()
        })
        .sum();

    // Cross-coupling energy
    let mut cross = 0.0f64;
    for i in 0..n_comp {
        for j in (i + 1)..n_comp {
            let lam = lambdas.get(i, j);
            if lam != 0.0 {
                let dot: f64 = (0..NCELLS)
                    .into_par_iter()
                    .map(|k| u_list[i][k] * u_list[j][k])
                    .sum();
                cross += lam * dot;
            }
        }
    }

    (per_comp + cross) * dx3
}

/// Per-component energy density (returned as Vec of Field3D).
pub fn energy_density_mc(u_list: &McField, s_list: &[Field3D]) -> Vec<Field3D> {
    let n_comp = u_list.len();
    let mut densities = Vec::with_capacity(n_comp);

    for i in 0..n_comp {
        let u = &u_list[i];
        let s = &s_list[i];
        let mut e = vec![0.0f64; NCELLS];
        e.par_chunks_mut(GRID * GRID)
            .enumerate()
            .for_each(|(z, slab)| {
                let base = z * GRID * GRID;
                for local in 0..GRID * GRID {
                    let k = base + local;
                    let x = k % GRID;
                    let y = (k / GRID) % GRID;
                    let xp = wrap(x as isize + 1);
                    let yp = wrap(y as isize + 1);
                    let zp = wrap(z as isize + 1);
                    let gx = u[idx(xp, y, z)] - u[idx(x, y, z)];
                    let gy = u[idx(x, yp, z)] - u[idx(x, y, z)];
                    let gz = u[idx(x, y, zp)] - u[idx(x, y, z)];
                    let grad = 0.5 * D_COEFF * (gx * gx + gy * gy + gz * gz);
                    let ui = u[k];
                    let pot = 0.25 * (ui * ui - 1.0) * (ui * ui - 1.0);
                    let coup = -(1.0 - ui * ui) * ui * s[k];
                    slab[local] = grad + pot + coup;
                }
            });
        densities.push(e);
    }
    densities
}

/// Initialize multi-component field with small random noise.
pub fn init_field_mc(n_comp: usize, seed: u64) -> McField {
    let mut fields = Vec::with_capacity(n_comp);
    for c in 0..n_comp {
        let mut f = vec![0.0f64; NCELLS];
        // Simple xorshift seeded per component
        let mut rng = seed.wrapping_add(c as u64 * 1337);
        for v in f.iter_mut() {
            rng ^= rng << 13;
            rng ^= rng >> 7;
            rng ^= rng << 17;
            // Map to [-0.01, 0.01]
            *v = (rng as f64 / u64::MAX as f64) * 0.02 - 0.01;
        }
        fields.push(f);
    }
    fields
}
