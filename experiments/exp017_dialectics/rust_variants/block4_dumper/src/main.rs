//! Dump 100 doc final-state (a, b) for IV-B (BGE source).
//! Input: same block3_input_100.json (doc_id + text) + embeddings_nfcorpus.json
//! Output: states.bin + meta.json (same layout as exp017 block3_states.bin)
mod engine;
use engine::*;
use rayon::prelude::*;
use serde::Deserialize;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

const EVOLVE_STEPS: usize = 5000;

#[derive(Deserialize)]
struct DocIn { doc_id: String, #[allow(dead_code)] text: String }

fn build_source_from_emb(emb: &[f32]) -> (Vec<f32>, Vec<f32>) {
    assert_eq!(emb.len(), 1024);
    let half = 512usize;
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];
    for k in 0..N {
        sa[k] = emb[k % half];
        sb[k] = emb[half + (k % half)];
    }
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
    let mut sa = sa; let mut sb = sb;
    smooth(&mut sa); smooth(&mut sb);
    (sa, sb)
}

fn evolve_emb(emb: &[f32], seed: u64) -> (Vec<f32>, Vec<f32>) {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_from_emb(emb);
    eng.set_source(&sa, &sb);
    eng.evolve_steps(EVOLVE_STEPS);
    (eng.a.clone(), eng.b.clone())
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();
    let input_path = std::env::args().nth(1).expect("input.json");
    let emb_path = std::env::args().nth(2).expect("emb.json");
    let states_path = std::env::args().nth(3).expect("states.bin");
    let meta_path = std::env::args().nth(4).expect("meta.json");

    let t0 = Instant::now();
    let docs: Vec<DocIn> = serde_json::from_str(&std::fs::read_to_string(&input_path).unwrap()).unwrap();
    eprintln!("Loaded {} docs", docs.len());
    let embs: HashMap<String, Vec<f32>> = serde_json::from_str(&std::fs::read_to_string(&emb_path).unwrap()).unwrap();
    eprintln!("Loaded {} embeddings", embs.len());

    let results: Vec<(String, Vec<f32>, Vec<f32>)> = docs.par_iter().enumerate().filter_map(|(i, d)| {
        let key = format!("d:{}", d.doc_id);
        let emb = embs.get(&key)?;
        let seed = 1000 + i as u64 * 17;
        let (a, b) = evolve_emb(emb, seed);
        Some((d.doc_id.clone(), a, b))
    }).collect();
    eprintln!("evolved {}/{}", results.len(), docs.len());

    let mut w = BufWriter::new(File::create(&states_path).unwrap());
    for (_, a, b) in &results {
        for v in a { w.write_all(&v.to_le_bytes()).unwrap(); }
        for v in b { w.write_all(&v.to_le_bytes()).unwrap(); }
    }
    w.flush().unwrap();

    let meta = serde_json::json!({
        "n_docs": results.len(),
        "grid_size": G, "n_voxels": N, "evolve_steps": EVOLVE_STEPS,
        "elapsed_s": t0.elapsed().as_secs_f64(),
        "doc_ids": results.iter().map(|r| r.0.clone()).collect::<Vec<_>>(),
        "layout": "for each doc: [a f32 x N][b f32 x N] little-endian",
    });
    std::fs::write(&meta_path, serde_json::to_string_pretty(&meta).unwrap()).unwrap();
    eprintln!("Wrote {} ({} docs, {:.1}s)", states_path, results.len(), t0.elapsed().as_secs_f64());
}
