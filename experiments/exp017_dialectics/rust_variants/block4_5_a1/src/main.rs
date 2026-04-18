//! Block IV.5 Stage A1: multi-well amplitude potential dumper.
//! Input: block3_input_100.json + embeddings_nfcorpus.json
//! Output: states.bin + meta.json
//!
//! Usage:
//!   block4_5_a1 <input.json> <emb.json> <states.bin> <meta.json> [dt] [steps] [clamp] [mode]
//!   mode: "full" (default) or "smoke" (first 5 docs + progress prints)
mod engine;
use engine::*;
use rayon::prelude::*;
use serde::Deserialize;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

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

fn evolve_emb(emb: &[f32], seed: u64, dt: f32, steps: usize, clamp_hi: f32)
    -> (Vec<f32>, Vec<f32>, f32, f32, bool)
{
    let mut eng = ComplexEngine::new();
    eng.init_u_nonzero(seed);
    let (sa, sb) = build_source_from_emb(emb);
    eng.set_source(&sa, &sb);
    eng.evolve_steps_multiwell(steps, dt, clamp_hi);
    let mut u_max: f32 = 0.0;
    let mut u_mean: f32 = 0.0;
    let mut has_nan = false;
    for k in 0..N {
        let ak = eng.a[k]; let bk = eng.b[k];
        if !ak.is_finite() || !bk.is_finite() { has_nan = true; }
        let u = ak*ak + bk*bk;
        u_mean += u;
        if u > u_max { u_max = u; }
    }
    u_mean /= N as f32;
    (eng.a.clone(), eng.b.clone(), u_max, u_mean, has_nan)
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();
    let args: Vec<String> = std::env::args().collect();
    let input_path = args.get(1).expect("input.json").clone();
    let emb_path = args.get(2).expect("emb.json").clone();
    let states_path = args.get(3).expect("states.bin").clone();
    let meta_path = args.get(4).expect("meta.json").clone();
    let dt: f32 = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(0.05);
    let steps: usize = args.get(6).and_then(|s| s.parse().ok()).unwrap_or(5000);
    let clamp_hi: f32 = args.get(7).and_then(|s| s.parse().ok()).unwrap_or(3.0);
    let mode = args.get(8).cloned().unwrap_or_else(|| "full".to_string());

    let t0 = Instant::now();
    let docs: Vec<DocIn> = serde_json::from_str(&std::fs::read_to_string(&input_path).unwrap()).unwrap();
    eprintln!("Loaded {} docs", docs.len());
    let embs: HashMap<String, Vec<f32>> = serde_json::from_str(&std::fs::read_to_string(&emb_path).unwrap()).unwrap();
    eprintln!("Loaded {} embeddings", embs.len());
    eprintln!("DT={} steps={} clamp={} mode={}", dt, steps, clamp_hi, mode);

    let docs_use: Vec<&DocIn> = if mode == "smoke" { docs.iter().take(5).collect() } else { docs.iter().collect() };

    let results: Vec<(String, Vec<f32>, Vec<f32>, f32, f32, bool)> =
        docs_use.par_iter().enumerate().filter_map(|(i, d)| {
            let key = format!("d:{}", d.doc_id);
            let emb = embs.get(&key)?;
            let seed = 1000 + i as u64 * 17;
            let (a, b, umax, umean, nan) = evolve_emb(emb, seed, dt, steps, clamp_hi);
            Some((d.doc_id.clone(), a, b, umax, umean, nan))
        }).collect();

    let mut n_nan = 0usize;
    let mut u_max_all: f32 = 0.0;
    let mut u_mean_all: f32 = 0.0;
    for (did, _, _, umax, umean, nan) in &results {
        if *nan { n_nan += 1; }
        if *umax > u_max_all { u_max_all = *umax; }
        u_mean_all += *umean;
        if mode == "smoke" {
            eprintln!("  doc {}: u_max={:.4} u_mean={:.4} nan={}", did, umax, umean, nan);
        }
    }
    u_mean_all /= results.len().max(1) as f32;
    eprintln!("evolved {}/{}  u_max_all={:.4}  u_mean_all={:.4}  n_nan={}",
             results.len(), docs_use.len(), u_max_all, u_mean_all, n_nan);

    let mut w = BufWriter::new(File::create(&states_path).unwrap());
    for (_, a, b, _, _, _) in &results {
        for v in a { w.write_all(&v.to_le_bytes()).unwrap(); }
        for v in b { w.write_all(&v.to_le_bytes()).unwrap(); }
    }
    w.flush().unwrap();

    let meta = serde_json::json!({
        "n_docs": results.len(),
        "grid_size": G, "n_voxels": N,
        "evolve_steps": steps, "dt": dt, "clamp_hi": clamp_hi, "mode": mode,
        "potential": "A1_multiwell: V=|psi|^2*(|psi|^2-1)^2*(|psi|^2-4)^2",
        "init": "init_u_nonzero: |psi|=1.0+-0.3",
        "u_max_all": u_max_all, "u_mean_all": u_mean_all, "n_nan": n_nan,
        "elapsed_s": t0.elapsed().as_secs_f64(),
        "doc_ids": results.iter().map(|r| r.0.clone()).collect::<Vec<_>>(),
        "layout": "for each doc: [a f32 x N][b f32 x N] little-endian",
    });
    std::fs::write(&meta_path, serde_json::to_string_pretty(&meta).unwrap()).unwrap();
    eprintln!("Wrote {} ({} docs, {:.1}s)", states_path, results.len(), t0.elapsed().as_secs_f64());
}
