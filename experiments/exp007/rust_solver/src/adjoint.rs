//! Adjoint iteration with dynamic source field update.
//!
//! Update modes for exp007b:
//!   Fixed:      No update (baseline)
//!   M2:         S₁ = S₀·u*, renormalized, every round (cumulative)
//!   M2NoNorm:   S₁ = S₀·u*, NO renormalization
//!   M2Once:     S₁ = S₀·u* only after round 0, then fixed

use rayon::prelude::*;
use crate::field::*;

pub const INIT_STEPS: usize = 1000;
pub const INTERACT_STEPS: usize = 300;
pub const RELAX_STEPS: usize = 100;
pub const FUSION_STEPS: usize = 2000;
pub const MAX_ROUNDS: usize = 5;
pub const CONVERGENCE_TOL: f64 = 0.01;
pub const TOP_K: usize = 10;
pub const CORPUS_SIZE: usize = 200;
pub const DB_PATH: &str = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db";

/// Source field update mode.
#[derive(Clone, Copy, PartialEq)]
pub enum UpdateMode {
    Fixed,      // No update (baseline)
    M2,         // S·u*, renormalized, every round
    M2NoNorm,   // S·u*, no renormalization
    M2Once,     // S·u* only after round 0, then fixed
}

impl UpdateMode {
    pub fn name(&self) -> &'static str {
        match self {
            UpdateMode::Fixed => "Fixed",
            UpdateMode::M2 => "M2: S·u* (norm, cumul)",
            UpdateMode::M2NoNorm => "M2: S·u* (no norm)",
            UpdateMode::M2Once => "M2: S·u* (once only)",
        }
    }
}

/// Compute coupling c_i = |integral e(x) * S_i(x) dx| for each corpus source.
fn compute_couplings(e: &Field3D, corpus_sources: &[Field3D]) -> Vec<f64> {
    corpus_sources
        .par_iter()
        .map(|s_i| {
            let c: f64 = e.iter().zip(s_i.iter()).map(|(a, b)| a * b).sum();
            c.abs()
        })
        .collect()
}

/// Select top-k by coupling strength.
fn select_topk(couplings: &[f64], k: usize) -> Vec<usize> {
    let mut indexed: Vec<(usize, f64)> = couplings.iter().copied().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    indexed.iter().take(k.min(indexed.len())).map(|(i, _)| *i).collect()
}

/// Adjoint iteration with dynamic S update.
pub fn adjoint_iteration(
    u: &mut Field3D,
    s: &mut Field3D,
    corpus_sources: &[Field3D],
    mode: UpdateMode,
) -> Vec<RoundInfo> {
    let mut history = Vec::new();
    let mut prev_metric: Option<f64> = None;

    for round in 0..MAX_ROUNDS {
        // G: compute energy density
        let e = energy_density(u, s);
        let e_std = {
            let mean = e.iter().sum::<f64>() / NCELLS as f64;
            let var = e.iter().map(|v| (v - mean) * (v - mean)).sum::<f64>() / NCELLS as f64;
            var.sqrt()
        };

        // Coupling + selection
        let couplings = compute_couplings(&e, corpus_sources);
        let targets = select_topk(&couplings, TOP_K);
        let coupling_max = couplings.iter().copied().fold(0.0f64, f64::max);

        let info = RoundInfo {
            round,
            e_std,
            coupling_max,
            n_targets: targets.len(),
        };
        eprintln!(
            "    Round {}: e_std={:.4} c_max={:.4} targets={}",
            round, e_std, coupling_max, targets.len()
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

        // F: practice with selected corpus
        for &ci in &targets {
            let s_i = &corpus_sources[ci];
            let mut s_combined: Field3D = s.iter().zip(s_i.iter()).map(|(a, b)| a + b).collect();
            let mx = s_combined.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
            if mx > 0.0 {
                for v in s_combined.iter_mut() {
                    *v /= mx;
                }
            }
            evolve(u, &s_combined, INTERACT_STEPS);
            evolve(u, s, RELAX_STEPS);
        }

        // Dynamic S update
        match mode {
            UpdateMode::Fixed => {},
            UpdateMode::M2 => {
                for k in 0..NCELLS {
                    s[k] = s[k] * u[k];
                }
                normalize(s);
            }
            UpdateMode::M2NoNorm => {
                for k in 0..NCELLS {
                    s[k] = s[k] * u[k];
                }
                // No normalize — let scale drift
            }
            UpdateMode::M2Once => {
                if round == 0 {
                    for k in 0..NCELLS {
                        s[k] = s[k] * u[k];
                    }
                    normalize(s);
                }
                // After round 0: no more updates
            }
        }
    }

    history
}

#[derive(Clone, serde::Serialize)]
pub struct RoundInfo {
    pub round: usize,
    pub e_std: f64,
    pub coupling_max: f64,
    pub n_targets: usize,
}
