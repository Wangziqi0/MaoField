mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;
use std::f32::consts::PI;

const EVOLVE_STEPS: usize = 5000;
const N_RUNS: usize = 3;

// ===== A: Polysemous vs Monosemous =====
const POLYSEMOUS: &[&str] = &["打", "开", "下", "过", "上"];
const MONOSEMOUS: &[&str] = &["有期徒刑", "拘役", "罚金", "管制", "缓刑"];

// ===== B: Context disambiguation =====
const CONTEXT_DA: &[&str] = &["打", "打人", "他打人", "他打我要怎么判"];
const CONTEXT_DA2: &[&str] = &["打", "打电话", "他打电话", "他打电话给我"];

// ===== C: Sense switching =====
const SENSE_KAI: &[&str] = &[
    "他在银行开了户",
    "他把门开了",
    "他开心极了",
];

/// Detect vortices in a 2D z-slice of the phase field.
/// Returns (positive_count, negative_count) for that slice.
fn detect_vortices_slice(phase: &[f32], z: usize) -> (usize, usize) {
    let mut pos = 0usize;
    let mut neg = 0usize;

    for y in 0..G {
        for x in 0..G {
            // Compute winding number around the plaquette (x,y)→(x+1,y)→(x+1,y+1)→(x,y+1)
            let xp = if x == G - 1 { 0 } else { x + 1 };
            let yp = if y == G - 1 { 0 } else { y + 1 };

            let p00 = phase[x + y * G + z * G * G];
            let p10 = phase[xp + y * G + z * G * G];
            let p11 = phase[xp + yp * G + z * G * G];
            let p01 = phase[x + yp * G + z * G * G];

            // Phase differences wrapped to (-π, π]
            let d1 = wrap_angle(p10 - p00);
            let d2 = wrap_angle(p11 - p10);
            let d3 = wrap_angle(p01 - p11);
            let d4 = wrap_angle(p00 - p01);

            let winding = d1 + d2 + d3 + d4;

            // winding ≈ ±2π → vortex/antivortex
            if winding > PI {
                pos += 1;
            } else if winding < -PI {
                neg += 1;
            }
        }
    }
    (pos, neg)
}

#[inline]
fn wrap_angle(mut d: f32) -> f32 {
    while d > PI { d -= 2.0 * PI; }
    while d <= -PI { d += 2.0 * PI; }
    d
}

#[derive(Serialize, Clone)]
struct VortexInfo {
    text: String,
    total_vortices: usize,
    positive_vortices: usize,
    negative_vortices: usize,
    net_winding: i32,
    vortex_density: f32,
    phase_variance: f32,
}

fn analyze_text(text: &str, seed: u64) -> (VortexInfo, Vec<f32>, Vec<f32>) {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_complex(text);
    eng.set_source(&sa, &sb);
    eng.evolve_steps(EVOLVE_STEPS);

    let phase = eng.phase_field();

    // Detect vortices across all z-slices
    let mut total_pos = 0usize;
    let mut total_neg = 0usize;
    for z in 0..G {
        let (p, n) = detect_vortices_slice(&phase, z);
        total_pos += p;
        total_neg += n;
    }

    // Phase variance
    let phase_mean = phase.iter().sum::<f32>() / N as f32;
    let phase_var = phase.iter().map(|&p| {
        let d = wrap_angle(p - phase_mean);
        d * d
    }).sum::<f32>() / N as f32;

    let info = VortexInfo {
        text: text.to_string(),
        total_vortices: total_pos + total_neg,
        positive_vortices: total_pos,
        negative_vortices: total_neg,
        net_winding: total_pos as i32 - total_neg as i32,
        vortex_density: (total_pos + total_neg) as f32 / N as f32,
        phase_variance: phase_var,
    };

    (info, eng.a, eng.b)
}

fn run_text_multi(text: &str) -> Vec<VortexInfo> {
    (0..N_RUNS as u64)
        .into_par_iter()
        .map(|run| {
            let seed = (run + 1) * 1000 + text.len() as u64;
            let (info, _, _) = analyze_text(text, seed);
            info
        })
        .collect()
}

fn mean_vortices(infos: &[VortexInfo]) -> f32 {
    infos.iter().map(|i| i.total_vortices as f32).sum::<f32>() / infos.len() as f32
}

fn mean_density(infos: &[VortexInfo]) -> f32 {
    infos.iter().map(|i| i.vortex_density).sum::<f32>() / infos.len() as f32
}

fn mean_phase_var(infos: &[VortexInfo]) -> f32 {
    infos.iter().map(|i| i.phase_variance).sum::<f32>() / infos.len() as f32
}

#[derive(Serialize)]
struct GroupResult {
    group: String,
    texts: Vec<TextResult>,
}

#[derive(Serialize)]
struct TextResult {
    text: String,
    mean_vortices: f32,
    mean_density: f32,
    mean_phase_var: f32,
    runs: Vec<VortexInfo>,
}

fn run_group(name: &str, texts: &[&str]) -> GroupResult {
    eprintln!("\n  --- {} ---", name);
    let mut text_results = Vec::new();
    for &text in texts {
        let infos = run_text_multi(text);
        let mv = mean_vortices(&infos);
        let md = mean_density(&infos);
        let mpv = mean_phase_var(&infos);
        eprintln!("    {:20} vortices={:.0} density={:.5} phase_var={:.4}",
            text, mv, md, mpv);
        text_results.push(TextResult {
            text: text.to_string(),
            mean_vortices: mv, mean_density: md, mean_phase_var: mpv,
            runs: infos,
        });
    }
    GroupResult { group: name.to_string(), texts: text_results }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp012: Vortex Encoding of Ambiguity");
    eprintln!("============================================================");
    let t0 = Instant::now();

    let mut all = Vec::new();

    // A: Polysemous vs Monosemous
    eprintln!("\n=== A: Polysemous vs Monosemous ===");
    all.push(run_group("A_polysemous", POLYSEMOUS));
    all.push(run_group("A_monosemous", MONOSEMOUS));

    let poly_mean = all[0].texts.iter().map(|t| t.mean_vortices).sum::<f32>() / all[0].texts.len() as f32;
    let mono_mean = all[1].texts.iter().map(|t| t.mean_vortices).sum::<f32>() / all[1].texts.len() as f32;
    eprintln!("\n  Polysemous mean vortices: {:.1}", poly_mean);
    eprintln!("  Monosemous mean vortices: {:.1}", mono_mean);
    if poly_mean > mono_mean * 1.2 {
        eprintln!("  ★ Polysemous > Monosemous by {:.0}%!", (poly_mean / mono_mean - 1.0) * 100.0);
    } else {
        eprintln!("  ~ No clear difference ({:.1} vs {:.1})", poly_mean, mono_mean);
    }

    // B: Context disambiguation
    eprintln!("\n=== B: Context Disambiguation ===");
    all.push(run_group("B_context_da_hit", CONTEXT_DA));
    all.push(run_group("B_context_da_call", CONTEXT_DA2));

    // Check if vortices decrease with more context
    for g in &all[2..4] {
        let vorts: Vec<f32> = g.texts.iter().map(|t| t.mean_vortices).collect();
        let decreasing = vorts.windows(2).all(|w| w[0] >= w[1]);
        eprintln!("\n  {} vortex sequence: {:?}", g.group,
            vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>());
        if decreasing && vorts[0] > vorts.last().unwrap() * 1.1 {
            eprintln!("  ★ Monotonically decreasing! Context → fewer vortices");
        } else {
            eprintln!("  ~ Not monotonically decreasing");
        }
    }

    // C: Sense switching
    eprintln!("\n=== C: Sense Switching ===");
    all.push(run_group("C_sense_kai", SENSE_KAI));

    // Check if different senses have different vortex counts
    let kai_vorts: Vec<f32> = all.last().unwrap().texts.iter().map(|t| t.mean_vortices).collect();
    let kai_range = kai_vorts.iter().copied().fold(f32::MIN, f32::max)
        - kai_vorts.iter().copied().fold(f32::MAX, f32::min);
    eprintln!("\n  'kai' senses vortex counts: {:?}",
        kai_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>());
    if kai_range > 5.0 {
        eprintln!("  ★ Different senses → different vortex counts (range={:.0})", kai_range);
    } else {
        eprintln!("  ~ Senses not clearly distinguished by vortex count");
    }

    let elapsed = t0.elapsed().as_secs_f64();

    // Summary
    eprintln!("\n============================================================");
    eprintln!("  VORTEX EXPERIMENT SUMMARY");
    eprintln!("------------------------------------------------------------");
    eprintln!("  A: poly={:.1} vs mono={:.1} vortices ({:+.0}%)",
        poly_mean, mono_mean, (poly_mean / mono_mean - 1.0) * 100.0);

    let da_vorts: Vec<f32> = all[2].texts.iter().map(|t| t.mean_vortices).collect();
    eprintln!("  B1: '打'→'打人'→'他打人'→'他打我要怎么判' = {:?}",
        da_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>());
    let da2_vorts: Vec<f32> = all[3].texts.iter().map(|t| t.mean_vortices).collect();
    eprintln!("  B2: '打'→'打电话'→'他打电话'→... = {:?}",
        da2_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>());
    eprintln!("  C: kai senses = {:?}",
        kai_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>());

    let all_pass = poly_mean > mono_mean * 1.2
        && da_vorts[0] > da_vorts.last().unwrap() * 1.1;
    if all_pass {
        eprintln!("\n  ★★★ VORTEX ENCODES AMBIGUITY — TOPOLOGICAL SEMANTIC DISCOVERY ★★★");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    // Save JSON
    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp012_vortex_ambiguity" },
        "groups": all,
        "summary": {
            "poly_mean_vortices": poly_mean,
            "mono_mean_vortices": mono_mean,
            "context_da_sequence": da_vorts,
            "context_da2_sequence": da2_vorts,
            "sense_kai_vortices": kai_vorts,
        },
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp012_results.json"), serde_json::to_string_pretty(&output).unwrap());

    // Save field data for visualization (just the first run of each B-group text)
    let fields_dir = results_dir.join("exp012_fields");
    let _ = std::fs::create_dir_all(&fields_dir);
    for text in CONTEXT_DA.iter().chain(CONTEXT_DA2.iter()).chain(SENSE_KAI.iter()) {
        let seed = 1000 + text.len() as u64;
        let (_, a_field, b_field) = analyze_text(text, seed);
        let fname = text.chars().take(10).collect::<String>().replace("/", "_");
        // Save as raw f32 binary (can be loaded in numpy with np.fromfile(..., dtype=np.float32).reshape(32,32,32))
        let _ = std::fs::write(fields_dir.join(format!("{}_a.bin", fname)),
            unsafe { std::slice::from_raw_parts(a_field.as_ptr() as *const u8, a_field.len() * 4) });
        let _ = std::fs::write(fields_dir.join(format!("{}_b.bin", fname)),
            unsafe { std::slice::from_raw_parts(b_field.as_ptr() as *const u8, b_field.len() * 4) });
    }
    eprintln!("Field data saved to {:?}", fields_dir);

    let mut summary = String::from("Exp012: Vortex Encoding of Ambiguity\n\n");
    summary.push_str(&format!("A: poly={:.1} vs mono={:.1} vortices\n", poly_mean, mono_mean));
    summary.push_str(&format!("B1: {:?}\n", da_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>()));
    summary.push_str(&format!("B2: {:?}\n", da2_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>()));
    summary.push_str(&format!("C: {:?}\n", kai_vorts.iter().map(|v| format!("{:.0}", v)).collect::<Vec<_>>()));
    summary.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp012_summary.txt"), summary);
}
