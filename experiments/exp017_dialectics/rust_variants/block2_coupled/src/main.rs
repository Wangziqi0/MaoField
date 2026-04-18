mod engine;

use engine::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::time::Instant;

/// Coupled evolution params
const COUPLED_STEPS: usize = 2000;
const SAMPLE_EVERY: usize = 100;
const LOCK_THRESH: f32 = 0.8;

// Physics constants (must match engine.rs)
const D_COEF: f32 = 0.1;
const DT: f32 = 0.1;
const INV_DX2: f32 = 1.0;

#[derive(Deserialize, Clone)]
struct Candidate {
    doc_id: String,
    text: String,
}

#[derive(Deserialize, Clone)]
struct QueryInput {
    query_id: String,
    query: String,
    candidates: Vec<Candidate>,
    qrels: serde_json::Value,
}

#[derive(Serialize, Clone)]
struct CandScore {
    doc_id: String,
    bm25_rank: usize,
    f1_energy_diff: f32,
    f2_phase_lock: f32,
    f3_lock_step: i32, // -1 means never locked; else step index where F2 first >= thresh
    nan_flag: bool,
}

#[derive(Serialize)]
struct QueryOutputG {
    query_id: String,
    query: String,
    bm25_order: Vec<String>,
    candidates: Vec<CandScore>,
    qrels: serde_json::Value,
}

fn truncate(text: &str, n: usize) -> String {
    text.chars().take(n).collect()
}

/// One coupled evolution of (eng_q, eng_d) for COUPLED_STEPS with diffusive coupling g.
/// Returns (F1, F2, F3, nan_flag).
fn coupled_evolve(
    qa: &mut [f32], qb: &mut [f32],
    qa_new: &mut [f32], qb_new: &mut [f32],
    da: &mut [f32], db: &mut [f32],
    da_new: &mut [f32], db_new: &mut [f32],
    sqa: &[f32], sqb: &[f32],
    sda: &[f32], sdb: &[f32],
    nb: &[[usize; 6]],
    g: f32,
) -> (f32, f32, i32, bool) {
    let mut first_lock: i32 = -1;
    let mut last_f2: f32 = 0.0;
    let mut nan_flag = false;

    for step in 0..COUPLED_STEPS {
        // Update both fields simultaneously using ψ at current step (synchronous explicit Euler)
        for k in 0..N {
            let nbi = unsafe { nb.get_unchecked(k) };
            let qak = unsafe { *qa.get_unchecked(k) };
            let qbk = unsafe { *qb.get_unchecked(k) };
            let dak = unsafe { *da.get_unchecked(k) };
            let dbk = unsafe { *db.get_unchecked(k) };

            let lap_qa = unsafe {
                *qa.get_unchecked(nbi[0]) + *qa.get_unchecked(nbi[1])
                + *qa.get_unchecked(nbi[2]) + *qa.get_unchecked(nbi[3])
                + *qa.get_unchecked(nbi[4]) + *qa.get_unchecked(nbi[5])
                - 6.0 * qak
            } * INV_DX2;
            let lap_qb = unsafe {
                *qb.get_unchecked(nbi[0]) + *qb.get_unchecked(nbi[1])
                + *qb.get_unchecked(nbi[2]) + *qb.get_unchecked(nbi[3])
                + *qb.get_unchecked(nbi[4]) + *qb.get_unchecked(nbi[5])
                - 6.0 * qbk
            } * INV_DX2;
            let lap_da = unsafe {
                *da.get_unchecked(nbi[0]) + *da.get_unchecked(nbi[1])
                + *da.get_unchecked(nbi[2]) + *da.get_unchecked(nbi[3])
                + *da.get_unchecked(nbi[4]) + *da.get_unchecked(nbi[5])
                - 6.0 * dak
            } * INV_DX2;
            let lap_db = unsafe {
                *db.get_unchecked(nbi[0]) + *db.get_unchecked(nbi[1])
                + *db.get_unchecked(nbi[2]) + *db.get_unchecked(nbi[3])
                + *db.get_unchecked(nbi[4]) + *db.get_unchecked(nbi[5])
                - 6.0 * dbk
            } * INV_DX2;

            let qmod2 = qak * qak + qbk * qbk;
            let dmod2 = dak * dak + dbk * dbk;

            let sqak = unsafe { *sqa.get_unchecked(k) };
            let sqbk = unsafe { *sqb.get_unchecked(k) };
            let sdak = unsafe { *sda.get_unchecked(k) };
            let sdbk = unsafe { *sdb.get_unchecked(k) };

            let dqa = D_COEF * lap_qa - qak * qmod2 + qak + sqak + g * (dak - qak);
            let dqb = D_COEF * lap_qb - qbk * qmod2 + qbk + sqbk + g * (dbk - qbk);
            let dda = D_COEF * lap_da - dak * dmod2 + dak + sdak + g * (qak - dak);
            let ddb = D_COEF * lap_db - dbk * dmod2 + dbk + sdbk + g * (qbk - dbk);

            unsafe {
                *qa_new.get_unchecked_mut(k) = (qak + DT * dqa).clamp(-2.0, 2.0);
                *qb_new.get_unchecked_mut(k) = (qbk + DT * dqb).clamp(-2.0, 2.0);
                *da_new.get_unchecked_mut(k) = (dak + DT * dda).clamp(-2.0, 2.0);
                *db_new.get_unchecked_mut(k) = (dbk + DT * ddb).clamp(-2.0, 2.0);
            }
        }
        qa.swap_with_slice(qa_new);
        qb.swap_with_slice(qb_new);
        da.swap_with_slice(da_new);
        db.swap_with_slice(db_new);

        // Sample F2 every SAMPLE_EVERY
        if (step + 1) % SAMPLE_EVERY == 0 {
            let mut sum = 0.0f32;
            let mut cnt = 0i32;
            for k in 0..N {
                let qak = qa[k]; let qbk = qb[k];
                let dak = da[k]; let dbk = db[k];
                let mq = (qak * qak + qbk * qbk).sqrt();
                let md = (dak * dak + dbk * dbk).sqrt();
                if mq > 1e-6 && md > 1e-6 {
                    let c = (qak * dak + qbk * dbk) / (mq * md);
                    if c.is_finite() {
                        sum += c;
                        cnt += 1;
                    } else {
                        nan_flag = true;
                    }
                }
            }
            let f2_now = if cnt > 0 { sum / cnt as f32 } else { 0.0 };
            last_f2 = f2_now;
            if first_lock < 0 && f2_now >= LOCK_THRESH {
                first_lock = (step + 1) as i32;
            }
        }
    }

    // Compute F1: |E_q - E_d|
    let e_q = compute_energy(qa, qb, sqa, sqb, nb);
    let e_d = compute_energy(da, db, sda, sdb, nb);
    let f1 = (e_q - e_d).abs();
    if !f1.is_finite() { nan_flag = true; }

    // Compute F2 final (use last sampled value, which equals step 2000)
    let f2 = last_f2;

    let f3 = if first_lock > 0 { first_lock } else { COUPLED_STEPS as i32 };

    (f1, f2, f3, nan_flag)
}

fn compute_energy(a: &[f32], b: &[f32], sa: &[f32], sb: &[f32], nb: &[[usize; 6]]) -> f32 {
    let mut total = 0.0f32;
    for k in 0..N {
        let nbi = unsafe { nb.get_unchecked(k) };
        let ak = a[k]; let bk = b[k];
        let gax = unsafe { *a.get_unchecked(nbi[1]) } - ak;
        let gay = unsafe { *a.get_unchecked(nbi[3]) } - ak;
        let gaz = unsafe { *a.get_unchecked(nbi[5]) } - ak;
        let gbx = unsafe { *b.get_unchecked(nbi[1]) } - bk;
        let gby = unsafe { *b.get_unchecked(nbi[3]) } - bk;
        let gbz = unsafe { *b.get_unchecked(nbi[5]) } - bk;
        let grad = 0.5 * D_COEF * (gax*gax + gay*gay + gaz*gaz + gbx*gbx + gby*gby + gbz*gbz);
        let mod2 = ak * ak + bk * bk;
        let pot = 0.25 * (mod2 - 1.0) * (mod2 - 1.0);
        let coup = -(ak * sa[k] + bk * sb[k]);
        total += grad + pot + coup;
    }
    total
}

/// Process one (query, doc) pair at one g-value.
/// Each pair: fresh init of both engines, set sources, run coupled evolution.
fn run_pair(
    query_text: &str,
    doc_text: &str,
    g: f32,
    seed_q: u64,
    seed_d: u64,
    nb: &[[usize; 6]],
) -> (f32, f32, i32, bool) {
    // Sources from text
    let (sqa, sqb) = build_source_complex(query_text);
    let (sda, sdb) = build_source_complex(doc_text);

    // Init fields
    let mut eng_q = ComplexEngine::new();
    eng_q.init_u(seed_q);
    let mut eng_d = ComplexEngine::new();
    eng_d.init_u(seed_d);

    let mut qa = std::mem::take(&mut eng_q.a);
    let mut qb = std::mem::take(&mut eng_q.b);
    let mut qa_new = vec![0.0f32; N];
    let mut qb_new = vec![0.0f32; N];
    let mut da = std::mem::take(&mut eng_d.a);
    let mut db = std::mem::take(&mut eng_d.b);
    let mut da_new = vec![0.0f32; N];
    let mut db_new = vec![0.0f32; N];

    coupled_evolve(
        &mut qa, &mut qb, &mut qa_new, &mut qb_new,
        &mut da, &mut db, &mut da_new, &mut db_new,
        &sqa, &sqb, &sda, &sdb,
        nb, g,
    )
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    let args: Vec<String> = std::env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: block2_coupled <input.json> <output_dir> <dataset_name> [g_list comma-sep]");
        std::process::exit(1);
    }
    let input_path = &args[1];
    let output_dir = &args[2];
    let dataset = &args[3];
    let g_list: Vec<f32> = if args.len() >= 5 {
        args[4].split(',').map(|s| s.trim().parse::<f32>().unwrap()).collect()
    } else {
        vec![0.0, 0.01, 0.05, 0.1, 0.3, 1.0]
    };

    eprintln!("============================================================");
    eprintln!("Block II Coupled Scan  dataset={} g_list={:?}", dataset, g_list);
    eprintln!("============================================================");

    let t0 = Instant::now();
    let txt = std::fs::read_to_string(input_path).expect("read input");
    let queries: Vec<QueryInput> = serde_json::from_str(&txt).expect("parse input");
    eprintln!("Loaded {} queries", queries.len());
    let total_pairs: usize = queries.iter().map(|q| q.candidates.len()).sum();
    eprintln!("Total (query,doc) pairs: {}  × {} g-values = {}", total_pairs, g_list.len(), total_pairs * g_list.len());

    std::fs::create_dir_all(output_dir).ok();

    let nb_tab = {
        // Build neighbor table once by constructing a temp engine
        let eng = ComplexEngine::new();
        eng.nb.clone()
    };

    // For each g value, run all (query, doc) pairs in parallel (flatten across queries & candidates)
    for &g in &g_list {
        let tg = Instant::now();
        eprintln!("\n--- g = {} ---", g);

        // Build flattened task list: (q_idx, c_idx)
        let tasks: Vec<(usize, usize)> = queries.iter().enumerate()
            .flat_map(|(qi, q)| (0..q.candidates.len()).map(move |ci| (qi, ci)))
            .collect();

        // Run in parallel
        let results: Vec<((usize, usize), (f32, f32, i32, bool))> = tasks.par_iter().map(|&(qi, ci)| {
            let q = &queries[qi];
            let c = &q.candidates[ci];
            let qtext = truncate(&q.query, 500);
            let dtext = truncate(&c.text, 500);
            let seed_q = 1000 + (q.query_id.len() as u64) * 7 + (qi as u64) * 13;
            let seed_d = 2000 + (ci as u64) * 17 + (qi as u64) * 29;
            let r = run_pair(&qtext, &dtext, g, seed_q, seed_d, &nb_tab);
            ((qi, ci), r)
        }).collect();

        // Collate per-query
        let mut per_q: Vec<Vec<Option<CandScore>>> = queries.iter()
            .map(|q| vec![None; q.candidates.len()]).collect();
        for ((qi, ci), (f1, f2, f3, nan)) in results {
            per_q[qi][ci] = Some(CandScore {
                doc_id: queries[qi].candidates[ci].doc_id.clone(),
                bm25_rank: ci,
                f1_energy_diff: f1,
                f2_phase_lock: f2,
                f3_lock_step: f3,
                nan_flag: nan,
            });
        }

        let outputs: Vec<QueryOutputG> = queries.iter().zip(per_q.into_iter()).map(|(q, cs)| {
            let cands: Vec<CandScore> = cs.into_iter().map(|o| o.unwrap()).collect();
            let bm25_order: Vec<String> = q.candidates.iter().map(|c| c.doc_id.clone()).collect();
            QueryOutputG {
                query_id: q.query_id.clone(),
                query: q.query.clone(),
                bm25_order,
                candidates: cands,
                qrels: q.qrels.clone(),
            }
        }).collect();

        let g_tag = format!("{:.2}", g).replace('.', "p");
        let out_path = format!("{}/{}_g{}.json", output_dir, dataset, g_tag);
        let runtime = tg.elapsed().as_secs_f64();
        let summary = serde_json::json!({
            "dataset": dataset,
            "g": g,
            "n_queries": outputs.len(),
            "runtime_s": runtime,
            "coupled_steps": COUPLED_STEPS,
            "per_query": outputs,
        });
        std::fs::write(&out_path, serde_json::to_string(&summary).unwrap()).unwrap();
        eprintln!("  g={} done in {:.1}s -> {}", g, runtime, out_path);
    }

    eprintln!("\nTotal elapsed: {:.1}s", t0.elapsed().as_secs_f64());
}
