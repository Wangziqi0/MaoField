//! Topological feature extraction from 3D Allen-Cahn field.
//!
//! Features: domain wall fraction, surface area, connected components (Betti β₀),
//! volume distribution, curvature histogram.

use crate::engine::{G, N};
use std::collections::VecDeque;

const SLAB: usize = G * G;

/// Neighbor indices for 6-connected 3D grid with periodic BC.
#[inline]
fn neighbors_6(x: usize, y: usize, z: usize) -> [(usize, usize, usize); 6] {
    let xm = if x == 0 { G - 1 } else { x - 1 };
    let xp = if x == G - 1 { 0 } else { x + 1 };
    let ym = if y == 0 { G - 1 } else { y - 1 };
    let yp = if y == G - 1 { 0 } else { y + 1 };
    let zm = if z == 0 { G - 1 } else { z - 1 };
    let zp = if z == G - 1 { 0 } else { z + 1 };
    [(xm, y, z), (xp, y, z), (x, ym, z), (x, yp, z), (x, y, zm), (x, y, zp)]
}

#[inline]
fn idx(x: usize, y: usize, z: usize) -> usize {
    x + y * G + z * SLAB
}

/// Domain wall: |u| < threshold.
pub fn wall_fraction(u: &[f32], threshold: f32) -> f32 {
    let count = u.iter().filter(|&&v| v.abs() < threshold).count();
    count as f32 / N as f32
}

/// Wall surface area: count faces between wall and non-wall cells.
pub fn wall_surface_area(u: &[f32], threshold: f32) -> f32 {
    let mut faces = 0u32;
    for z in 0..G {
        for y in 0..G {
            for x in 0..G {
                let k = idx(x, y, z);
                let is_wall = u[k].abs() < threshold;
                for (nx, ny, nz) in &neighbors_6(x, y, z) {
                    let nk = idx(*nx, *ny, *nz);
                    let n_is_wall = u[nk].abs() < threshold;
                    if is_wall != n_is_wall {
                        faces += 1;
                    }
                }
            }
        }
    }
    // Each face counted twice (from both sides)
    faces as f32 / 2.0
}

/// 3D connected components via BFS. Returns (n_components, sorted volumes descending).
pub fn connected_components(u: &[f32], positive: bool, threshold: f32) -> (usize, Vec<usize>) {
    let mut visited = vec![false; N];
    let mut components = Vec::new();

    for z in 0..G {
        for y in 0..G {
            for x in 0..G {
                let k = idx(x, y, z);
                if visited[k] { continue; }
                let val = u[k];
                let in_domain = if positive { val > threshold } else { val < -threshold };
                if !in_domain { continue; }

                // BFS flood fill
                let mut queue = VecDeque::new();
                queue.push_back((x, y, z));
                visited[k] = true;
                let mut vol = 0usize;

                while let Some((cx, cy, cz)) = queue.pop_front() {
                    vol += 1;
                    for (nx, ny, nz) in &neighbors_6(cx, cy, cz) {
                        let nk = idx(*nx, *ny, *nz);
                        if !visited[nk] {
                            let nv = u[nk];
                            let n_in = if positive { nv > threshold } else { nv < -threshold };
                            if n_in {
                                visited[nk] = true;
                                queue.push_back((*nx, *ny, *nz));
                            }
                        }
                    }
                }
                components.push(vol);
            }
        }
    }
    components.sort_by(|a, b| b.cmp(a));
    let n = components.len();
    (n, components)
}

/// Curvature histogram on domain wall cells.
/// H ≈ ∇²u / |∇u| (mean curvature approximation).
pub fn curvature_histogram(u: &[f32], wall_threshold: f32, n_bins: usize) -> Vec<f32> {
    let mut curvatures = Vec::new();

    for z in 0..G {
        for y in 0..G {
            for x in 0..G {
                let k = idx(x, y, z);
                if u[k].abs() >= wall_threshold { continue; }

                let nb = neighbors_6(x, y, z);
                let ux = u[idx(nb[1].0, nb[1].1, nb[1].2)] - u[idx(nb[0].0, nb[0].1, nb[0].2)];
                let uy = u[idx(nb[3].0, nb[3].1, nb[3].2)] - u[idx(nb[2].0, nb[2].1, nb[2].2)];
                let uz = u[idx(nb[5].0, nb[5].1, nb[5].2)] - u[idx(nb[4].0, nb[4].1, nb[4].2)];
                let grad_mag = (ux * ux + uy * uy + uz * uz).sqrt();

                if grad_mag < 1e-6 { continue; }

                // Laplacian
                let lap = u[idx(nb[0].0, nb[0].1, nb[0].2)]
                    + u[idx(nb[1].0, nb[1].1, nb[1].2)]
                    + u[idx(nb[2].0, nb[2].1, nb[2].2)]
                    + u[idx(nb[3].0, nb[3].1, nb[3].2)]
                    + u[idx(nb[4].0, nb[4].1, nb[4].2)]
                    + u[idx(nb[5].0, nb[5].1, nb[5].2)]
                    - 6.0 * u[k];

                let h = lap / grad_mag;
                curvatures.push(h);
            }
        }
    }

    // Build histogram
    let mut hist = vec![0.0f32; n_bins];
    if curvatures.is_empty() { return hist; }

    let min_c = curvatures.iter().copied().fold(f32::MAX, f32::min);
    let max_c = curvatures.iter().copied().fold(f32::MIN, f32::max);
    let range = max_c - min_c;
    if range < 1e-10 { hist[0] = 1.0; return hist; }

    for &c in &curvatures {
        let bin = ((c - min_c) / range * (n_bins as f32 - 0.001)) as usize;
        let bin = bin.min(n_bins - 1);
        hist[bin] += 1.0;
    }
    // Normalize to probability
    let total = curvatures.len() as f32;
    for v in hist.iter_mut() { *v /= total; }
    hist
}

/// Full topological feature vector (~24 dimensions).
#[derive(Clone, serde::Serialize)]
pub struct TopoFeatures {
    pub wall_fraction: f32,
    pub wall_surface_area: f32,
    pub n_pos_domains: usize,
    pub n_neg_domains: usize,
    pub pos_volumes: [f32; 5],  // top-5 positive domain volumes (normalized)
    pub neg_volumes: [f32; 5],  // top-5 negative domain volumes (normalized)
    pub curvature_hist: [f32; 10],
}

impl TopoFeatures {
    pub fn extract(u: &[f32]) -> Self {
        let wt = 0.5f32;

        let wf = wall_fraction(u, wt);
        let wsa = wall_surface_area(u, wt);

        let (n_pos, pos_vols) = connected_components(u, true, wt);
        let (n_neg, neg_vols) = connected_components(u, false, wt);

        let mut pv = [0.0f32; 5];
        for (i, &v) in pos_vols.iter().take(5).enumerate() {
            pv[i] = v as f32 / N as f32;
        }
        let mut nv = [0.0f32; 5];
        for (i, &v) in neg_vols.iter().take(5).enumerate() {
            nv[i] = v as f32 / N as f32;
        }

        let ch_vec = curvature_histogram(u, wt, 10);
        let mut ch = [0.0f32; 10];
        for (i, &v) in ch_vec.iter().enumerate() { ch[i] = v; }

        Self {
            wall_fraction: wf,
            wall_surface_area: wsa,
            n_pos_domains: n_pos,
            n_neg_domains: n_neg,
            pos_volumes: pv,
            neg_volumes: nv,
            curvature_hist: ch,
        }
    }

    /// Convert to flat f32 vector for distance computation.
    pub fn to_vec(&self) -> Vec<f32> {
        let mut v = Vec::with_capacity(24);
        v.push(self.wall_fraction);
        v.push(self.wall_surface_area / 10000.0); // normalize to ~O(1)
        v.push(self.n_pos_domains as f32 / 10.0);
        v.push(self.n_neg_domains as f32 / 10.0);
        v.extend_from_slice(&self.pos_volumes);
        v.extend_from_slice(&self.neg_volumes);
        v.extend_from_slice(&self.curvature_hist);
        v
    }
}

/// Euclidean distance between two feature vectors.
pub fn euclidean_dist(a: &[f32], b: &[f32]) -> f32 {
    a.iter().zip(b.iter()).map(|(x, y)| (x - y) * (x - y)).sum::<f32>().sqrt()
}

/// Cosine similarity between two feature vectors.
pub fn cosine_sim(a: &[f32], b: &[f32]) -> f32 {
    let dot: f32 = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum();
    let na: f32 = a.iter().map(|x| x * x).sum::<f32>().sqrt();
    let nb: f32 = b.iter().map(|x| x * x).sum::<f32>().sqrt();
    if na < 1e-10 || nb < 1e-10 { return 0.0; }
    dot / (na * nb)
}

/// Betti number distance: |β₀⁺(a) - β₀⁺(b)| + |β₀⁻(a) - β₀⁻(b)|.
pub fn betti_dist(a: &TopoFeatures, b: &TopoFeatures) -> f32 {
    (a.n_pos_domains as f32 - b.n_pos_domains as f32).abs()
    + (a.n_neg_domains as f32 - b.n_neg_domains as f32).abs()
}
