mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Deserialize;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

const EVOLVE_STEPS: usize = 5000;

#[derive(Deserialize)]
struct DocIn { doc_id: String, text: String }

fn truncate(text: &str, n: usize) -> String {
    text.chars().take(n).collect()
}

fn evolve_one(text: &str, seed: u64) -> (Vec<f32>, Vec<f32>) {
    let text = truncate(text, 500);
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_complex(&text);
    eng.set_source(&sa, &sb);
    eng.evolve_steps(EVOLVE_STEPS);
    (eng.a.clone(), eng.b.clone())
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    let input_path = std::env::args().nth(1).expect("usage: block3_dumper <input.json> <states.bin> <meta.json>");
    let states_path = std::env::args().nth(2).expect("states.bin");
    let meta_path = std::env::args().nth(3).expect("meta.json");

    let t0 = Instant::now();
    let txt = std::fs::read_to_string(&input_path).expect("read input");
    let docs: Vec<DocIn> = serde_json::from_str(&txt).expect("parse input");
    eprintln!("Loaded {} docs", docs.len());

    let results: Vec<(String, Vec<f32>, Vec<f32>)> = docs.par_iter().enumerate().map(|(i, d)| {
        let seed = 1000 + i as u64 * 17;
        let (a, b) = evolve_one(&d.text, seed);
        (d.doc_id.clone(), a, b)
    }).collect();

    let mut w = BufWriter::new(File::create(&states_path).unwrap());
    for (_, a, b) in &results {
        for v in a { w.write_all(&v.to_le_bytes()).unwrap(); }
        for v in b { w.write_all(&v.to_le_bytes()).unwrap(); }
    }
    w.flush().unwrap();

    let meta = serde_json::json!({
        "n_docs": results.len(),
        "grid_size": G,
        "n_voxels": N,
        "evolve_steps": EVOLVE_STEPS,
        "elapsed_s": t0.elapsed().as_secs_f64(),
        "doc_ids": results.iter().map(|r| r.0.clone()).collect::<Vec<_>>(),
        "layout": "for each doc: [a f32 x N][b f32 x N] little-endian",
    });
    std::fs::write(&meta_path, serde_json::to_string_pretty(&meta).unwrap()).unwrap();

    eprintln!("Wrote {} ({} docs, {:.1}s)", states_path, results.len(), t0.elapsed().as_secs_f64());
}
