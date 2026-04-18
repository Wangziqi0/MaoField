//! Multi-component adjoint iteration: G (energy density coupling) + F (practice).

use rayon::prelude::*;
use crate::config::*;
use crate::field::{McField, Field3D, Lambdas, init_field_mc, evolve_mc, energy_density_mc, idx};

/// Compute coupling c_total = sum_i |integral e_i * S_i_corpus| for each corpus entry.
pub fn compute_couplings(e_list: &[Field3D], corpus_mc: &[Vec<Field3D>]) -> Vec<f64> {
    corpus_mc
        .par_iter()
        .map(|s_entry| {
            let mut c_total = 0.0f64;
            for (i, e_i) in e_list.iter().enumerate() {
                let c_i: f64 = e_i.iter().zip(s_entry[i].iter()).map(|(a, b)| a * b).sum();
                c_total += c_i.abs();
            }
            c_total
        })
        .collect()
}

/// Select top-k indices by coupling strength.
fn select_topk(couplings: &[f64], k: usize) -> Vec<usize> {
    let mut indexed: Vec<(usize, f64)> = couplings.iter().copied().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    indexed.iter().take(k.min(indexed.len())).map(|(i, _)| *i).collect()
}

/// Practice with selected corpus entries (interact + relax per entry).
fn practice_with_targets(
    u_list: &mut McField,
    s_query: &[Field3D],
    targets: &[usize],
    corpus_mc: &[Vec<Field3D>],
    lambdas: &Lambdas,
) {
    for &idx in targets {
        // Combined source = query + corpus, per component, normalized
        let s_combined: Vec<Field3D> = (0..u_list.len())
            .map(|c| {
                let mut sc: Field3D = s_query[c]
                    .iter()
                    .zip(corpus_mc[idx][c].iter())
                    .map(|(a, b)| a + b)
                    .collect();
                let mx = sc.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
                if mx > 0.0 {
                    for v in sc.iter_mut() {
                        *v /= mx;
                    }
                }
                sc
            })
            .collect();

        // Interact
        evolve_mc(u_list, &s_combined, lambdas, INTERACT_STEPS);
        // Relax with query only
        evolve_mc(u_list, s_query, lambdas, RELAX_STEPS);
    }
}

/// Round diagnostics.
#[derive(Clone, serde::Serialize)]
pub struct RoundInfo {
    pub round: usize,
    pub r_norm: f64,
    pub e_std: f64,
    pub coupling_max: f64,
    pub n_targets: usize,
}

/// Full adjoint iteration for a single text's field.
pub fn adjoint_iteration(
    u_list: &mut McField,
    s_query: &[Field3D],
    corpus_mc: &[Vec<Field3D>],
    lambdas: &Lambdas,
    label: &str,
) -> Vec<RoundInfo> {
    let mut history = Vec::new();
    let mut prev_metric: Option<f64> = None;

    for round in 0..MAX_ROUNDS {
        // G: energy density per component
        let e_list = energy_density_mc(u_list, s_query);

        // Residual norm (for diagnostics)
        let r_norm = residual_norm_mc(u_list, s_query, lambdas);

        // e_std = mean of per-component std
        let e_std = e_list
            .iter()
            .map(|e| {
                let mean = e.iter().sum::<f64>() / NCELLS as f64;
                let var = e.iter().map(|v| (v - mean) * (v - mean)).sum::<f64>() / NCELLS as f64;
                var.sqrt()
            })
            .sum::<f64>()
            / e_list.len() as f64;

        let couplings = compute_couplings(&e_list, corpus_mc);
        let targets = select_topk(&couplings, TOP_K);
        let coupling_max = couplings.iter().copied().fold(0.0f64, f64::max);

        let info = RoundInfo {
            round,
            r_norm,
            e_std,
            coupling_max,
            n_targets: targets.len(),
        };
        eprintln!(
            "    Round {}: ‖r‖={:.4} e_std={:.4} c_max={:.4} targets={}",
            round, r_norm, e_std, coupling_max, targets.len()
        );
        history.push(info);

        // Convergence check
        let metric = e_std;
        if let Some(prev) = prev_metric {
            let change = (metric - prev).abs() / (prev.abs() + 1e-10);
            eprintln!("      metric change: {:.4}", change);
            if change < CONVERGENCE_TOL {
                eprintln!("      Converged at round {}.", round);
                break;
            }
        }
        prev_metric = Some(metric);

        // F: practice
        practice_with_targets(u_list, s_query, &targets, corpus_mc, lambdas);
    }
    let _ = label; // used only for future logging
    history
}

/// Residual norm: sqrt(sum over components of sum r_i^2).
fn residual_norm_mc(u_list: &McField, s_list: &[Field3D], lambdas: &Lambdas) -> f64 {
    let n_comp = u_list.len();
    let inv_dx2 = 1.0 / (DX * DX);
    let mut total = 0.0f64;

    for i in 0..n_comp {
        let u = &u_list[i];
        let s = &s_list[i];
        let sum: f64 = (0..NCELLS)
            .into_par_iter()
            .map(|k| {
                let x = k % GRID;
                let y = (k / GRID) % GRID;
                let z = k / (GRID * GRID);
                let xm = if x == 0 { GRID - 1 } else { x - 1 };
                let xp = if x == GRID - 1 { 0 } else { x + 1 };
                let ym = if y == 0 { GRID - 1 } else { y - 1 };
                let yp = if y == GRID - 1 { 0 } else { y + 1 };
                let zm = if z == 0 { GRID - 1 } else { z - 1 };
                let zp = if z == GRID - 1 { 0 } else { z + 1 };
                let lap = (u[idx(xp, y, z)] + u[idx(xm, y, z)]
                    + u[idx(x, yp, z)] + u[idx(x, ym, z)]
                    + u[idx(x, y, zp)] + u[idx(x, y, zm)]
                    - 6.0 * u[k])
                    * inv_dx2;
                let ui = u[k];
                let mut cross = 0.0f64;
                for j in 0..n_comp {
                    if j != i {
                        let lam = lambdas.get(i, j);
                        if lam != 0.0 {
                            cross += lam * u_list[j][k];
                        }
                    }
                }
                let r = D_COEFF * lap - ui * ui * ui + ui - cross
                    + (1.0 - 3.0 * ui * ui) * s[k];
                r * r
            })
            .sum();
        total += sum;
    }
    total.sqrt()
}
