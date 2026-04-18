//! Phase B Experiment 1 driver (Win taskbook 2026-04-15).
//!
//! Modes:
//!   exp              — α=0.1, β=0.05, N=100, multi-scale, BGE source (NO whiten)
//!   null             — α=0, β=0, multi-scale, BGE source    (sanity check: must
//!                      produce identical trajectory to control_const)
//!   control_const    — α=0, β=0, multi-scale, BGE source    (structurally same as null;
//!                      kept as an explicit control for clarity in falsification table)
//!   control_whiten   — α=0.1, β=0.05, multi-scale, BGE-whitened source
//!   control_single   — α=0.1, β=0.05, SINGLE-SCALE (no block-average, no history push)
//!
//! Multi-scale structure (Day 1 review P0-5 fix — refresh S at middle tick, not
//! every inner step; block-average persists between middle ticks):
//!   inner  dt = 0.01             (every step: evolve ψ with CURRENT S)
//!   middle every 10 inner steps  (dt = 0.10): recompute effective S
//!                                             + block-average (block=2) coarse-grain;
//!                                             S frozen for next 10 inner steps
//!   outer  every 100 inner steps (dt = 1.00): push (ψ − ⟨ψ⟩) to history buffer
//!
//! History kernel w_k · dt_outer = exp(−λ · k · dt_outer) · dt_outer with
//! λ = 0.05, dt_outer = 1.0. Literal taskbook integral (no normalization, Day 1
//! review P0-4 fix).
//!
//! Default seed 20260421.
//!
//! Observables logged every 100 inner steps (outer tick):
//!   t, mean_mod2, std_mod2, mean_psi_re, mean_psi_im, source_l2, dS_dt, free_energy

mod engine;
use engine::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

#[derive(Deserialize)]
struct DocIn {
    doc_id: String,
    #[allow(dead_code)]
    text: String,
}

#[derive(Serialize, Clone)]
struct ObsRow {
    t: f32,
    mean_mod2: f32,
    std_mod2: f32,
    mean_psi_re: f32,
    mean_psi_im: f32,
    source_l2: f32,
    ds_dt: f32,
    free_energy: f32,
}

#[derive(Serialize)]
struct DocObservables {
    doc_id: String,
    seed: u64,
    rows: Vec<ObsRow>,
}

fn smooth_3x(s: &mut [f32]) {
    let mut buf = vec![0.0f32; N];
    for _ in 0..3 {
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    let xm = if x == 0 { G - 1 } else { x - 1 };
                    let xp = if x == G - 1 { 0 } else { x + 1 };
                    buf[k] = (s[xm + y * G + z * G * G] + s[k] + s[xp + y * G + z * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    let ym = if y == 0 { G - 1 } else { y - 1 };
                    let yp = if y == G - 1 { 0 } else { y + 1 };
                    buf[k] = (s[x + ym * G + z * G * G] + s[k] + s[x + yp * G + z * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    let zm = if z == 0 { G - 1 } else { z - 1 };
                    let zp = if z == G - 1 { 0 } else { z + 1 };
                    buf[k] = (s[x + y * G + zm * G * G] + s[k] + s[x + y * G + zp * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
    }
}

/// Build base source (s0a, s0b) from a BGE-M3 1024-dim embedding.
/// Lower half → real; upper half → imag. Tile on 32³ grid (k % 512).
/// If `whiten`, subtract spatial mean from each so ⟨s0a⟩ = ⟨s0b⟩ = 0 (breaks
/// the 17σ detailed-balance violation that the exp mode preserves).
fn build_source_from_emb(emb: &[f32], whiten: bool) -> (Vec<f32>, Vec<f32>) {
    assert_eq!(emb.len(), 1024);
    let half = 512usize;
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];
    for k in 0..N {
        sa[k] = emb[k % half];
        sb[k] = emb[half + (k % half)];
    }
    smooth_3x(&mut sa);
    smooth_3x(&mut sb);
    if whiten {
        let mean_a: f32 = sa.iter().sum::<f32>() / N as f32;
        let mean_b: f32 = sb.iter().sum::<f32>() / N as f32;
        for v in sa.iter_mut() {
            *v -= mean_a;
        }
        for v in sb.iter_mut() {
            *v -= mean_b;
        }
    }
    (sa, sb)
}

#[derive(Clone, Copy, Debug)]
enum Mode {
    Exp,
    Null,
    ControlConst,
    ControlWhiten,
    ControlSingle,
}

impl Mode {
    fn from_str(s: &str) -> Self {
        match s {
            "exp" => Mode::Exp,
            "null" => Mode::Null,
            "control_const" => Mode::ControlConst,
            "control_whiten" => Mode::ControlWhiten,
            "control_single" => Mode::ControlSingle,
            other => panic!("unknown mode: {}", other),
        }
    }

    fn params(self) -> EngineParams {
        match self {
            Mode::Exp | Mode::ControlWhiten | Mode::ControlSingle => EngineParams::default_exp(),
            Mode::Null | Mode::ControlConst => EngineParams::null_test(),
        }
    }

    fn whiten_source(self) -> bool {
        matches!(self, Mode::ControlWhiten)
    }

    fn multi_scale(self) -> bool {
        !matches!(self, Mode::ControlSingle)
    }

    fn label(self) -> &'static str {
        match self {
            Mode::Exp => "exp",
            Mode::Null => "null",
            Mode::ControlConst => "control_const",
            Mode::ControlWhiten => "control_whiten",
            Mode::ControlSingle => "control_single",
        }
    }
}

/// Run one doc for `n_inner_steps` inner steps with the chosen mode.
/// Returns (final a, final b, observables rows).
fn run_one_doc(
    emb: &[f32],
    mode: Mode,
    dt_inner: f32,
    n_inner_steps: usize,
    seed: u64,
    obs_every: usize, // inner steps per observable row
    middle_every: usize, // inner steps per block_average (middle loop)
    outer_every: usize, // inner steps per history push (outer loop)
    block_size: usize,
) -> (Vec<f32>, Vec<f32>, Vec<ObsRow>) {
    let params = mode.params();
    let dt_outer = dt_inner * outer_every as f32; // = 1.0 for default (100 × 0.01)
    let mut eng = Engine::new(params);
    eng.init_psi_near_minimum(seed);
    let (s0a, s0b) = build_source_from_emb(emb, mode.whiten_source());
    eng.set_base_source(&s0a, &s0b);
    let mut rows: Vec<ObsRow> = Vec::with_capacity(n_inner_steps / obs_every + 2);
    // Initial observable row (t = 0 pre-evolution); also seeds scratch_da/db.
    eng.recompute_effective_source(dt_outer);
    if mode.multi_scale() {
        eng.block_average_source(block_size);
    }
    let (mpre, mpim) = eng.mean_psi();
    rows.push(ObsRow {
        t: 0.0,
        mean_mod2: eng.mean_mod2(),
        std_mod2: eng.std_mod2(),
        mean_psi_re: mpre,
        mean_psi_im: mpim,
        source_l2: eng.source_l2(),
        ds_dt: eng.entropy_production_rate(),
        free_energy: eng.free_energy(),
    });
    for step in 1..=n_inner_steps {
        // Inner loop: evolve ψ one step using CURRENT (frozen between middle ticks) S.
        eng.evolve_inner_step(dt_inner);
        // Middle loop: at every `middle_every` inner steps, refresh S (which uses
        // the updated ψ via α·Δψ term AND current history buffer via β·δS),
        // then block-average. The freshly coarse-grained S drives the next
        // `middle_every` inner steps.
        if mode.multi_scale() && step % middle_every == 0 {
            eng.recompute_effective_source(dt_outer);
            eng.block_average_source(block_size);
        } else if !mode.multi_scale() {
            // Single-scale control: refresh S every inner step; no coarse-graining.
            eng.recompute_effective_source(dt_outer);
        }
        // Outer loop: push current (ψ − ⟨ψ⟩) to history (multi-scale only).
        // scratch_da/db are valid from the most recent recompute call; if the
        // outer tick falls on a middle tick (step % 100 == 0 implies step % 10 == 0),
        // the recompute above has just run. If not multi-scale, skip entirely.
        if mode.multi_scale() && step % outer_every == 0 {
            eng.push_history();
        }
        // Observable logging.
        if step % obs_every == 0 {
            // For obs consistency across modes, ensure scratch_da/db & effective S
            // reflect the current ψ at logging time.
            if mode.multi_scale() && step % middle_every != 0 {
                eng.recompute_effective_source(dt_outer);
                eng.block_average_source(block_size);
            }
            let (mpre, mpim) = eng.mean_psi();
            rows.push(ObsRow {
                t: eng.time,
                mean_mod2: eng.mean_mod2(),
                std_mod2: eng.std_mod2(),
                mean_psi_re: mpre,
                mean_psi_im: mpim,
                source_l2: eng.source_l2(),
                ds_dt: eng.entropy_production_rate(),
                free_energy: eng.free_energy(),
            });
        }
    }
    (eng.a, eng.b, rows)
}

fn main() {
    rayon::ThreadPoolBuilder::new()
        .num_threads(32)
        .build_global()
        .unwrap();
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 4 {
        eprintln!(
            "usage: {} <input.json> <emb.json> <out_dir> [mode=exp] [dt=0.01] [steps=5000] [seed=20260421] [n_docs=100] [obs_every=100]",
            args[0]
        );
        std::process::exit(1);
    }
    let input_path = args[1].clone();
    let emb_path = args[2].clone();
    let out_dir = args[3].clone();
    let mode_str = args.get(4).cloned().unwrap_or_else(|| "exp".to_string());
    let mode = Mode::from_str(&mode_str);
    let dt: f32 = args
        .get(5)
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.01);
    let steps: usize = args
        .get(6)
        .and_then(|s| s.parse().ok())
        .unwrap_or(5000);
    let seed_base: u64 = args
        .get(7)
        .and_then(|s| s.parse().ok())
        .unwrap_or(20260421);
    let n_docs: usize = args.get(8).and_then(|s| s.parse().ok()).unwrap_or(100);
    let obs_every: usize = args.get(9).and_then(|s| s.parse().ok()).unwrap_or(100);

    std::fs::create_dir_all(&out_dir).unwrap();
    let t0 = Instant::now();

    let docs: Vec<DocIn> =
        serde_json::from_str(&std::fs::read_to_string(&input_path).unwrap()).unwrap();
    let embs: HashMap<String, Vec<f32>> =
        serde_json::from_str(&std::fs::read_to_string(&emb_path).unwrap()).unwrap();
    eprintln!(
        "mode={} dt={} steps={} seed={} docs={}  loaded {} embeddings",
        mode.label(),
        dt,
        steps,
        seed_base,
        n_docs,
        embs.len()
    );

    let docs_use: Vec<&DocIn> = docs.iter().take(n_docs).collect();

    let results: Vec<(String, u64, Vec<f32>, Vec<f32>, Vec<ObsRow>)> = docs_use
        .par_iter()
        .enumerate()
        .filter_map(|(i, d)| {
            let key = format!("d:{}", d.doc_id);
            let emb = embs.get(&key)?;
            let seed = seed_base.wrapping_add((i as u64).wrapping_mul(17));
            let (a, b, rows) = run_one_doc(
                emb,
                mode,
                dt,
                steps,
                seed,
                obs_every,
                10, // middle_every (block_average every 10 inner steps → dt_mid=0.1)
                100, // outer_every (history push every 100 inner steps → dt_outer=1.0)
                2,   // block_size (2³ voxels averaged per block → 16³ coarse blocks on 32³)
            );
            Some((d.doc_id.clone(), seed, a, b, rows))
        })
        .collect();

    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!(
        "evolved {}/{} docs in {:.1}s",
        results.len(),
        docs_use.len(),
        elapsed
    );

    // states.bin
    let states_path = format!("{}/states_{}.bin", out_dir, mode.label());
    let mut w = BufWriter::new(File::create(&states_path).unwrap());
    for (_, _, a, b, _) in &results {
        for v in a {
            w.write_all(&v.to_le_bytes()).unwrap();
        }
        for v in b {
            w.write_all(&v.to_le_bytes()).unwrap();
        }
    }
    w.flush().unwrap();

    // observables.json
    let obs_path = format!("{}/observables_{}.json", out_dir, mode.label());
    let doc_obs: Vec<DocObservables> = results
        .iter()
        .map(|(id, seed, _, _, rows)| DocObservables {
            doc_id: id.clone(),
            seed: *seed,
            rows: rows.clone(),
        })
        .collect();
    std::fs::write(&obs_path, serde_json::to_string_pretty(&doc_obs).unwrap()).unwrap();

    // meta.json
    let p = mode.params();
    let meta = serde_json::json!({
        "mode": mode.label(),
        "n_docs": results.len(),
        "grid_size": G, "n_voxels": N,
        "dt_inner": dt,
        "n_inner_steps": steps,
        "middle_every": 10,
        "outer_every": 100,
        "block_size": 2,
        "seed_base": seed_base,
        "params": {
            "d": p.d,
            "v_min": p.v_min,
            "alpha": p.alpha,
            "beta": p.beta,
            "lambda_hist_per_outer": p.lambda_hist,
            "n_hist": p.n_hist,
            "clamp_abs": p.clamp_abs,
        },
        "potential": "V = (|psi|^2 - v_min^2)^2   (Mexican hat, U(1))",
        "eom": "gamma=1 : d_t psi = D*lap(psi) - 2*(|psi|^2 - v^2)*psi + S(x,t)",
        "source": "S(x,t) = S0(x) + alpha*(psi - <psi>_x) + beta*delta_S_history",
        "source_whiten": mode.whiten_source(),
        "multi_scale": mode.multi_scale(),
        "obs_every_inner": obs_every,
        "elapsed_s": elapsed,
        "doc_ids": results.iter().map(|r| r.0.clone()).collect::<Vec<_>>(),
        "states_layout": "per doc: [a f32 x N][b f32 x N] little-endian",
    });
    let meta_path = format!("{}/meta_{}.json", out_dir, mode.label());
    std::fs::write(&meta_path, serde_json::to_string_pretty(&meta).unwrap()).unwrap();

    eprintln!(
        "wrote:\n  {}\n  {}\n  {}",
        states_path, obs_path, meta_path
    );
}
