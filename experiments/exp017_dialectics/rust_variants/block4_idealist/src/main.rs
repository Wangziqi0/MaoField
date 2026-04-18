//! IV-B Idealist dynamic: identical GL operator (FUSION=0) but the source
//! field is built from a BGE-M3 1024-d embedding instead of UTF-8 bytes.
//!
//! Mapping (32^3 = 32768 grid; 32768/1024 = 32):
//!   sa[k] = emb[0..512][k % 512]   (real, tile 64x then truncate at N)
//!   sb[k] = emb[512..1024][k % 512] (imag)
//! Then smooth + normalize via engine::normalize_f32 only (no smoothing here
//! since BGE embeddings already have no high-freq spatial content).

mod engine;

use engine::*;
use rayon::prelude::*;
use serde::{Serialize, Deserialize};
use std::time::Instant;
use std::collections::HashMap;

const EVOLVE_STEPS: usize = 5000;
const FUSION_STEPS: usize = 0;

#[derive(Deserialize)]
struct Candidate { doc_id: String, text: String }

#[derive(Deserialize)]
struct QueryInput {
    query_id: String,
    query: String,
    candidates: Vec<Candidate>,
    qrels: serde_json::Value,
}

#[derive(Serialize, Clone)]
struct ScoredDoc { doc_id: String, energy: f32, bm25_rank: usize }

#[derive(Serialize)]
struct QueryOutput {
    query_id: String,
    query: String,
    bm25_order: Vec<String>,
    mao_order: Vec<String>,
    mao_scores: Vec<ScoredDoc>,
    qrels: serde_json::Value,
}

/// Build complex source from a 1024-d BGE embedding via tile-mapping.
/// Note: we DO smooth (3 iterations) + normalize like the byte version, so the
/// PDE operator sees the same smoothness regime.
fn build_source_from_emb(emb: &[f32]) -> (Vec<f32>, Vec<f32>) {
    assert_eq!(emb.len(), 1024, "BGE embedding must be 1024-d");
    let half = 512usize;
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];
    for k in 0..N {
        sa[k] = emb[k % half];
        sb[k] = emb[half + (k % half)];
    }
    // Smooth + normalize (mirrors build_source_complex)
    let smooth = |s: &mut Vec<f32>| {
        let mut buf = vec![0.0f32; N];
        for _ in 0..3 {
            for z in 0..G { for y in 0..G { for x in 0..G {
                let xm = if x==0{G-1}else{x-1}; let xp = if x==G-1{0}else{x+1};
                let k = x+y*G+z*G*G;
                buf[k] = (s[xm+y*G+z*G*G] + s[k] + s[xp+y*G+z*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
            for z in 0..G { for y in 0..G {
                let ym = if y==0{G-1}else{y-1}; let yp = if y==G-1{0}else{y+1};
                for x in 0..G { let k = x+y*G+z*G*G;
                buf[k] = (s[x+ym*G+z*G*G] + s[k] + s[x+yp*G+z*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
            for z in 0..G {
                let zm = if z==0{G-1}else{z-1}; let zp = if z==G-1{0}else{z+1};
                for y in 0..G { for x in 0..G { let k = x+y*G+z*G*G;
                buf[k] = (s[x+y*G+zm*G*G] + s[k] + s[x+y*G+zp*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
        }
        normalize_f32(s);
    };
    smooth(&mut sa);
    smooth(&mut sb);
    (sa, sb)
}

fn process_emb(emb: &[f32], seed: u64) -> ComplexEngine {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_from_emb(emb);
    eng.set_source(&sa, &sb);
    eng.evolve_steps(EVOLVE_STEPS);
    eng
}

fn fuse_energy(eq: &ComplexEngine, ed: &ComplexEngine) -> f32 {
    let mut fused = ComplexEngine::new();
    for k in 0..N {
        fused.a[k] = 0.5 * (eq.a[k] + ed.a[k]);
        fused.b[k] = 0.5 * (eq.b[k] + ed.b[k]);
        fused.sa[k] = eq.sa[k] + ed.sa[k];
        fused.sb[k] = eq.sb[k] + ed.sb[k];
    }
    let mx = (0..N).map(|k| fused.sa[k].abs().max(fused.sb[k].abs())).fold(0.0f32, f32::max);
    if mx > 0.0 { let inv = 1.0/mx; for k in 0..N { fused.sa[k] *= inv; fused.sb[k] *= inv; } }
    fused.evolve_steps(FUSION_STEPS);
    fused.compute_energy()
}

fn rerank_one(q: &QueryInput, embs: &HashMap<String, Vec<f32>>, seed_off: u64) -> Option<QueryOutput> {
    let qkey = format!("q:{}", q.query_id);
    let qemb = embs.get(&qkey)?;
    let seed = seed_off + q.query_id.len() as u64 * 7;
    let eq = process_emb(qemb, seed);

    let mut scored: Vec<ScoredDoc> = q.candidates.par_iter().enumerate().filter_map(|(rank, cand)| {
        let dkey = format!("d:{}", cand.doc_id);
        let demb = embs.get(&dkey)?;
        let ed = process_emb(demb, seed + rank as u64 + 1);
        let energy = fuse_energy(&eq, &ed);
        Some(ScoredDoc { doc_id: cand.doc_id.clone(), energy, bm25_rank: rank })
    }).collect();

    let mut mao_sorted = scored.clone();
    mao_sorted.sort_by(|a, b| a.energy.partial_cmp(&b.energy).unwrap());
    let mao_order: Vec<String> = mao_sorted.iter().map(|s| s.doc_id.clone()).collect();
    let bm25_order: Vec<String> = q.candidates.iter().map(|c| c.doc_id.clone()).collect();
    scored.sort_by_key(|s| s.bm25_rank);

    Some(QueryOutput {
        query_id: q.query_id.clone(),
        query: q.query.clone(),
        bm25_order, mao_order, mao_scores: scored,
        qrels: q.qrels.clone(),
    })
}

fn p_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let mut hits = 0usize;
    for d in order.iter().take(k) {
        if let Some(score) = qrels.get(d).and_then(|v| v.as_i64()) { if score > 0 { hits += 1; } }
    }
    hits as f64 / k as f64
}

fn dcg_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let mut s = 0.0;
    for (i, d) in order.iter().take(k).enumerate() {
        if let Some(score) = qrels.get(d).and_then(|v| v.as_i64()) {
            let rel = score as f64;
            if rel > 0.0 { s += (2f64.powf(rel) - 1.0) / ((i as f64 + 2.0).log2()); }
        }
    }
    s
}

fn ndcg_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let dcg = dcg_at_k(order, qrels, k);
    let mut rels: Vec<i64> = qrels.as_object().unwrap().values().filter_map(|v| v.as_i64()).filter(|&s| s > 0).collect();
    rels.sort_by(|a, b| b.cmp(a));
    let mut ideal = 0.0;
    for (i, &r) in rels.iter().take(k).enumerate() {
        ideal += (2f64.powf(r as f64) - 1.0) / ((i as f64 + 2.0).log2());
    }
    if ideal > 0.0 { dcg / ideal } else { 0.0 }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();
    let input_path = std::env::args().nth(1).expect("Usage: solver <input.json> <emb.json> <output.json>");
    let emb_path = std::env::args().nth(2).expect("emb.json required");
    let output_path = std::env::args().nth(3).expect("output.json required");

    eprintln!("============================================================");
    eprintln!("Block IV-B: Idealist dynamic (BGE-source GL, FUSION=0)");
    eprintln!("============================================================");

    let t0 = Instant::now();
    let queries: Vec<QueryInput> = serde_json::from_str(&std::fs::read_to_string(&input_path).unwrap()).unwrap();
    eprintln!("Loaded {} queries", queries.len());

    // emb_path: JSON object id -> [1024 floats]
    let raw: HashMap<String, Vec<f32>> = serde_json::from_str(&std::fs::read_to_string(&emb_path).unwrap()).unwrap();
    eprintln!("Loaded {} embeddings", raw.len());

    let mut outputs = Vec::with_capacity(queries.len());
    let mut skipped = 0;
    for (i, q) in queries.iter().enumerate() {
        let tq = Instant::now();
        match rerank_one(q, &raw, 1000) {
            Some(out) => {
                let elapsed = tq.elapsed().as_secs_f64();
                let p10_bm25 = p_at_k(&out.bm25_order, &out.qrels, 10);
                let p10_mao  = p_at_k(&out.mao_order,  &out.qrels, 10);
                let n_bm25 = ndcg_at_k(&out.bm25_order, &out.qrels, 10);
                let n_mao  = ndcg_at_k(&out.mao_order,  &out.qrels, 10);
                eprintln!("  [{:3}/{}] {} bm25_nDCG={:.3} mao_nDCG={:.3} ({:.1}s) p10_b={:.2} p10_m={:.2}",
                    i+1, queries.len(), out.query_id, n_bm25, n_mao, elapsed, p10_bm25, p10_mao);
                outputs.push(out);
            }
            None => { skipped += 1; eprintln!("  [skip] {} (missing emb)", q.query_id); }
        }
    }

    let n = outputs.len() as f64;
    let p10_bm25_avg = outputs.iter().map(|o| p_at_k(&o.bm25_order, &o.qrels, 10)).sum::<f64>() / n;
    let p10_mao_avg  = outputs.iter().map(|o| p_at_k(&o.mao_order, &o.qrels, 10)).sum::<f64>() / n;
    let nd_bm25_avg  = outputs.iter().map(|o| ndcg_at_k(&o.bm25_order, &o.qrels, 10)).sum::<f64>() / n;
    let nd_mao_avg   = outputs.iter().map(|o| ndcg_at_k(&o.mao_order, &o.qrels, 10)).sum::<f64>() / n;

    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("================================================");
    eprintln!("  IV-B Summary ({} queries, skipped={}, {:.1}s)", outputs.len(), skipped, elapsed);
    eprintln!("  BM25 nDCG@10={:.4}  MaoField-IV-B nDCG@10={:.4}", nd_bm25_avg, nd_mao_avg);

    let summary = serde_json::json!({
        "n_queries": outputs.len(),
        "skipped": skipped,
        "total_time_s": elapsed,
        "bm25_p10": p10_bm25_avg, "bm25_ndcg10": nd_bm25_avg,
        "mao_p10": p10_mao_avg,  "mao_ndcg10": nd_mao_avg,
        "delta_p10": p10_mao_avg - p10_bm25_avg,
        "delta_ndcg10": nd_mao_avg - nd_bm25_avg,
        "per_query": outputs,
    });
    std::fs::write(&output_path, serde_json::to_string_pretty(&summary).unwrap()).unwrap();
    eprintln!("Wrote {}", output_path);
}
