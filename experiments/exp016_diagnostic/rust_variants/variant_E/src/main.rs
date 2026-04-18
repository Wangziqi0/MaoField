mod engine;

use engine::*;
use rayon::prelude::*;
use serde::{Serialize, Deserialize};
use std::time::Instant;

const EVOLVE_STEPS: usize = 5000;
const FUSION_STEPS: usize = 2000;

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
    bm25_order: Vec<String>,     // original BM25 order
    mao_order: Vec<String>,      // MaoField reranked
    mao_scores: Vec<ScoredDoc>,
    qrels: serde_json::Value,
}

/// Truncate text to first N chars (Unicode-safe-ish for ASCII).
fn truncate(text: &str, n: usize) -> String {
    text.chars().take(n).collect()
}

/// Process a text into complex engine (a, b, sa, sb).
fn process(text: &str, seed: u64) -> ComplexEngine {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_complex(text);
    eng.set_source(&sa, &sb);
    eng.evolve_steps(EVOLVE_STEPS);
    eng
}

/// Fuse query and doc, return energy (lower = more relevant).
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

fn rerank_one(q: &QueryInput, seed_off: u64) -> QueryOutput {
    let query_text = truncate(&q.query, 500);
    let seed = seed_off + q.query_id.len() as u64 * 7;

    // Process query once
    let eq = process(&query_text, seed);

    // Parallelize candidates: each candidate = process doc + fuse
    let mut scored: Vec<ScoredDoc> = q.candidates.par_iter().enumerate().map(|(rank, cand)| {
        let doc_text = truncate(&cand.text, 500);
        let ed = process(&doc_text, seed + rank as u64 + 1);
        let energy = fuse_energy(&eq, &ed);
        ScoredDoc { doc_id: cand.doc_id.clone(), energy, bm25_rank: rank }
    }).collect();

    // Sort by energy ascending (lower = more relevant)
    let mut mao_sorted = scored.clone();
    mao_sorted.sort_by(|a, b| a.energy.partial_cmp(&b.energy).unwrap());
    let mao_order: Vec<String> = mao_sorted.iter().map(|s| s.doc_id.clone()).collect();
    let bm25_order: Vec<String> = q.candidates.iter().map(|c| c.doc_id.clone()).collect();

    // Keep scored in BM25 order for analysis
    scored.sort_by_key(|s| s.bm25_rank);

    QueryOutput {
        query_id: q.query_id.clone(),
        query: q.query.clone(),
        bm25_order,
        mao_order,
        mao_scores: scored,
        qrels: q.qrels.clone(),
    }
}

fn p_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let mut hits = 0usize;
    for d in order.iter().take(k) {
        if let Some(score) = qrels.get(d).and_then(|v| v.as_i64()) {
            if score > 0 { hits += 1; }
        }
    }
    hits as f64 / k as f64
}

fn dcg_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let mut s = 0.0;
    for (i, d) in order.iter().take(k).enumerate() {
        if let Some(score) = qrels.get(d).and_then(|v| v.as_i64()) {
            let rel = score as f64;
            if rel > 0.0 {
                s += (2f64.powf(rel) - 1.0) / ((i as f64 + 2.0).log2());
            }
        }
    }
    s
}

fn ndcg_at_k(order: &[String], qrels: &serde_json::Value, k: usize) -> f64 {
    let dcg = dcg_at_k(order, qrels, k);
    // Ideal DCG: sort all qrels by score desc
    let mut rels: Vec<i64> = qrels.as_object().unwrap().values()
        .filter_map(|v| v.as_i64()).filter(|&s| s > 0).collect();
    rels.sort_by(|a, b| b.cmp(a));
    let mut ideal = 0.0;
    for (i, &r) in rels.iter().take(k).enumerate() {
        ideal += (2f64.powf(r as f64) - 1.0) / ((i as f64 + 2.0).log2());
    }
    if ideal > 0.0 { dcg / ideal } else { 0.0 }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    let input_path = std::env::args().nth(1).expect("Usage: exp015_solver <input.json> <output.json>");
    let output_path = std::env::args().nth(2).expect("Usage: exp015_solver <input.json> <output.json>");

    eprintln!("============================================================");
    eprintln!("MaoField Exp015: NFCorpus BM25 Rerank");
    eprintln!("============================================================");

    let t0 = Instant::now();
    let input_txt = std::fs::read_to_string(&input_path).expect("failed to read input");
    let queries: Vec<QueryInput> = serde_json::from_str(&input_txt).expect("bad JSON");
    eprintln!("Loaded {} queries", queries.len());

    // Process queries sequentially (each query's candidates parallelize internally)
    let mut outputs = Vec::with_capacity(queries.len());
    for (i, q) in queries.iter().enumerate() {
        let tq = Instant::now();
        let out = rerank_one(q, 1000);
        let elapsed = tq.elapsed().as_secs_f64();
        // Quick metrics
        let p10_bm25 = p_at_k(&out.bm25_order, &out.qrels, 10);
        let p10_mao = p_at_k(&out.mao_order, &out.qrels, 10);
        let ndcg_bm25 = ndcg_at_k(&out.bm25_order, &out.qrels, 10);
        let ndcg_mao = ndcg_at_k(&out.mao_order, &out.qrels, 10);
        eprintln!("  [{:3}/{}] {} bm25_P@10={:.2} mao_P@10={:.2} bm25_nDCG={:.3} mao_nDCG={:.3} ({:.1}s)",
            i+1, queries.len(), out.query_id, p10_bm25, p10_mao, ndcg_bm25, ndcg_mao, elapsed);
        outputs.push(out);
    }

    // Aggregate
    let n = outputs.len() as f64;
    let p10_bm25_avg = outputs.iter().map(|o| p_at_k(&o.bm25_order, &o.qrels, 10)).sum::<f64>() / n;
    let p10_mao_avg = outputs.iter().map(|o| p_at_k(&o.mao_order, &o.qrels, 10)).sum::<f64>() / n;
    let ndcg_bm25_avg = outputs.iter().map(|o| ndcg_at_k(&o.bm25_order, &o.qrels, 10)).sum::<f64>() / n;
    let ndcg_mao_avg = outputs.iter().map(|o| ndcg_at_k(&o.mao_order, &o.qrels, 10)).sum::<f64>() / n;

    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\n============================================================");
    eprintln!("  STAGE 1 SUMMARY ({} queries, {:.1}s)", outputs.len(), elapsed);
    eprintln!("------------------------------------------------------------");
    eprintln!("  BM25      P@10 = {:.4}  nDCG@10 = {:.4}", p10_bm25_avg, ndcg_bm25_avg);
    eprintln!("  MaoField  P@10 = {:.4}  nDCG@10 = {:.4}", p10_mao_avg, ndcg_mao_avg);
    eprintln!("  Delta     P@10 = {:+.4}  nDCG@10 = {:+.4}", p10_mao_avg - p10_bm25_avg, ndcg_mao_avg - ndcg_bm25_avg);
    eprintln!("============================================================");

    let summary = serde_json::json!({
        "n_queries": outputs.len(),
        "total_time_s": elapsed,
        "bm25_p10": p10_bm25_avg,
        "bm25_ndcg10": ndcg_bm25_avg,
        "mao_p10": p10_mao_avg,
        "mao_ndcg10": ndcg_mao_avg,
        "delta_p10": p10_mao_avg - p10_bm25_avg,
        "delta_ndcg10": ndcg_mao_avg - ndcg_bm25_avg,
        "per_query": outputs,
    });
    std::fs::write(&output_path, serde_json::to_string_pretty(&summary).unwrap()).unwrap();
    eprintln!("Wrote {}", output_path);
}
