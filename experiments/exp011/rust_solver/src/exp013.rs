mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;
use std::f32::consts::PI;

const EVOLVE_STEPS: usize = 5000;
const FUSION_STEPS: usize = 2000;
const N_RUNS: usize = 3;

// exp008b same-domain (hardest)
const PAIRS_T4: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "合同当事人应当按照约定全面履行各自的义务"),
    ("偷了别人的钱包", "秘密窃取他人随身携带的财物属于扒窃行为", "夫妻离婚时共同债务应当共同偿还"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于危险驾驶行为", "遗产按照法定继承办理由第一顺序继承人继承"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "经营者不得对消费者进行侮辱诽谤侵犯人格尊严"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "劳动者享有平等就业和选择职业的权利"),
    ("两口子过不下去了", "夫妻感情确已破裂经调解无效应准予解除婚姻", "盗窃公私财物数额特别巨大处十年以上有期徒刑"),
    ("朋友欠钱一直拖着", "债务人未按约定履行还款义务债权人可主张权利", "国家实行劳动者每日工作时间不超过八小时的制度"),
    ("房子到期了不让住了", "租赁合同届满后承租人拒不腾退出租人可诉请返还", "生产销售假药的处三年以下有期徒刑并处罚金"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "父母对未成年子女负有抚养教育和保护的义务"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "侵占他人财物数额较大拒不退还的处二年以下有期徒刑"),
];

#[derive(Clone, Copy)]
enum Cond {
    A_Full,        // Full complex field
    B_RealOnly,    // Only real part energy for matching
    C_ImagOnly,    // Only imaginary part energy for matching
    D_Decoupled,   // Decoupled: a³ instead of (a²+b²)a
    E_Amplitude,   // Amplitude |U| matching
    F_Phase,       // Phase arg(U) matching
    G_SwapSplit,   // Swap: odd→real, even→imag
    H_RandomSplit, // Random bit assignment
}

impl Cond {
    fn name(&self) -> &'static str {
        match self {
            Cond::A_Full => "A_full_complex",
            Cond::B_RealOnly => "B_real_only",
            Cond::C_ImagOnly => "C_imag_only",
            Cond::D_Decoupled => "D_decoupled",
            Cond::E_Amplitude => "E_amplitude",
            Cond::F_Phase => "F_phase",
            Cond::G_SwapSplit => "G_swap_split",
            Cond::H_RandomSplit => "H_random_split",
        }
    }
}

// ===== Decoupled engine: two independent Allen-Cahn =====
fn evolve_decoupled(eng: &mut ComplexEngine, n_steps: usize) {
    let tab = &eng.nb;
    const D: f32 = 0.1;
    const DT: f32 = 0.1;
    const INV_DX2: f32 = 1.0;

    for _ in 0..n_steps {
        let a = &eng.a; let b = &eng.b;
        let sa = &eng.sa; let sb = &eng.sb;
        let a_new = &mut eng.a_new; let b_new = &mut eng.b_new;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ak = unsafe { *a.get_unchecked(k) };
            let bk = unsafe { *b.get_unchecked(k) };
            let sak = unsafe { *sa.get_unchecked(k) };
            let sbk = unsafe { *sb.get_unchecked(k) };

            let lap_a = unsafe {
                *a.get_unchecked(nb[0]) + *a.get_unchecked(nb[1])
                + *a.get_unchecked(nb[2]) + *a.get_unchecked(nb[3])
                + *a.get_unchecked(nb[4]) + *a.get_unchecked(nb[5])
                - 6.0 * ak
            } * INV_DX2;
            let lap_b = unsafe {
                *b.get_unchecked(nb[0]) + *b.get_unchecked(nb[1])
                + *b.get_unchecked(nb[2]) + *b.get_unchecked(nb[3])
                + *b.get_unchecked(nb[4]) + *b.get_unchecked(nb[5])
                - 6.0 * bk
            } * INV_DX2;

            // DECOUPLED: a³ and b³ independently, no cross-term
            let da = D * lap_a - ak * ak * ak + ak + sak;
            let db = D * lap_b - bk * bk * bk + bk + sbk;

            unsafe {
                *a_new.get_unchecked_mut(k) = (ak + DT * da).clamp(-2.0, 2.0);
                *b_new.get_unchecked_mut(k) = (bk + DT * db).clamp(-2.0, 2.0);
            }
        }
        std::mem::swap(&mut eng.a, &mut eng.a_new);
        std::mem::swap(&mut eng.b, &mut eng.b_new);
    }
}

// ===== Source field variants =====

/// Swap split: odd bits → real, even bits → imag (reversed from normal)
fn build_source_swap(text: &str) -> (Vec<f32>, Vec<f32>) {
    let bytes = text.as_bytes();
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];
    let mut bit_idx = 0usize;
    for &byte in bytes {
        for i in (0..8).rev() {
            let bit = if (byte >> i) & 1 == 1 { 1.0f32 } else { -1.0 };
            let k = (bit_idx / 2) % N;
            // SWAPPED: odd→real, even→imag
            if bit_idx % 2 == 1 { sa[k] += bit; } else { sb[k] += bit; }
            bit_idx += 1;
        }
    }
    smooth_and_normalize(&mut sa);
    smooth_and_normalize(&mut sb);
    (sa, sb)
}

/// Random bit assignment with fixed seed per text
fn build_source_random(text: &str) -> (Vec<f32>, Vec<f32>) {
    let bytes = text.as_bytes();
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];

    // Deterministic shuffle based on text hash
    let mut rng: u64 = 12345;
    for &b in bytes { rng = rng.wrapping_mul(6364136223846793005).wrapping_add(b as u64); }

    let mut bit_idx = 0usize;
    for &byte in bytes {
        for i in (0..8).rev() {
            let bit = if (byte >> i) & 1 == 1 { 1.0f32 } else { -1.0 };
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            let k = (bit_idx / 2) % N;
            if rng % 2 == 0 { sa[k] += bit; } else { sb[k] += bit; }
            bit_idx += 1;
        }
    }
    smooth_and_normalize(&mut sa);
    smooth_and_normalize(&mut sb);
    (sa, sb)
}

fn smooth_and_normalize(s: &mut Vec<f32>) {
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
}

// ===== Energy functions for partial matching =====

fn energy_real_only(eng: &ComplexEngine) -> f32 {
    let tab = &eng.nb;
    let mut total = 0.0f32;
    for k in 0..N {
        let nb = unsafe { tab.get_unchecked(k) };
        let ak = eng.a[k];
        let gx = unsafe { *eng.a.get_unchecked(nb[1]) } - ak;
        let gy = unsafe { *eng.a.get_unchecked(nb[3]) } - ak;
        let gz = unsafe { *eng.a.get_unchecked(nb[5]) } - ak;
        total += 0.5 * 0.1 * (gx*gx + gy*gy + gz*gz)
            + 0.25 * (ak*ak - 1.0) * (ak*ak - 1.0)
            - ak * eng.sa[k];
    }
    total
}

fn energy_imag_only(eng: &ComplexEngine) -> f32 {
    let tab = &eng.nb;
    let mut total = 0.0f32;
    for k in 0..N {
        let nb = unsafe { tab.get_unchecked(k) };
        let bk = eng.b[k];
        let gx = unsafe { *eng.b.get_unchecked(nb[1]) } - bk;
        let gy = unsafe { *eng.b.get_unchecked(nb[3]) } - bk;
        let gz = unsafe { *eng.b.get_unchecked(nb[5]) } - bk;
        total += 0.5 * 0.1 * (gx*gx + gy*gy + gz*gz)
            + 0.25 * (bk*bk - 1.0) * (bk*bk - 1.0)
            - bk * eng.sb[k];
    }
    total
}

fn amplitude_similarity(eq: &ComplexEngine, ed: &ComplexEngine) -> f32 {
    // -L2 distance of amplitude fields (higher = more similar)
    let mut dist = 0.0f32;
    for k in 0..N {
        let aq = (eq.a[k]*eq.a[k] + eq.b[k]*eq.b[k]).sqrt();
        let ad = (ed.a[k]*ed.a[k] + ed.b[k]*ed.b[k]).sqrt();
        let d = aq - ad;
        dist += d * d;
    }
    -dist.sqrt()
}

fn phase_similarity(eq: &ComplexEngine, ed: &ComplexEngine) -> f32 {
    // Sum of cos(phase_q - phase_d) (higher = more similar)
    let mut total = 0.0f32;
    for k in 0..N {
        let pq = eq.b[k].atan2(eq.a[k]);
        let pd = ed.b[k].atan2(ed.a[k]);
        total += (pq - pd).cos();
    }
    total / N as f32
}

// ===== Process and match =====

struct ProcessedField {
    eng: ComplexEngine,
}

fn process_text(text: &str, seed: u64, cond: Cond) -> ProcessedField {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);

    let (sa, sb) = match cond {
        Cond::G_SwapSplit => build_source_swap(text),
        Cond::H_RandomSplit => build_source_random(text),
        _ => build_source_complex(text),
    };
    eng.set_source(&sa, &sb);

    match cond {
        Cond::D_Decoupled => evolve_decoupled(&mut eng, EVOLVE_STEPS),
        _ => eng.evolve_steps(EVOLVE_STEPS),
    };

    ProcessedField { eng }
}

fn fuse_and_energy(eq: &ComplexEngine, ed: &ComplexEngine, cond: Cond) -> f32 {
    let mut fused = ComplexEngine::new();
    for k in 0..N {
        fused.a[k] = 0.5 * (eq.a[k] + ed.a[k]);
        fused.b[k] = 0.5 * (eq.b[k] + ed.b[k]);
        fused.sa[k] = eq.sa[k] + ed.sa[k];
        fused.sb[k] = eq.sb[k] + ed.sb[k];
    }
    let mx = (0..N).map(|k| fused.sa[k].abs().max(fused.sb[k].abs())).fold(0.0f32, f32::max);
    if mx > 0.0 { let inv = 1.0/mx; for k in 0..N { fused.sa[k]*=inv; fused.sb[k]*=inv; } }

    match cond {
        Cond::D_Decoupled => evolve_decoupled(&mut fused, FUSION_STEPS),
        _ => fused.evolve_steps(FUSION_STEPS),
    };

    fused.compute_energy()
}

/// Returns true if match is preferred over mismatch.
fn judge_pair(pq: &ProcessedField, pm: &ProcessedField, pmm: &ProcessedField, cond: Cond) -> (bool, f32) {
    match cond {
        Cond::B_RealOnly => {
            let mut fq_m = ComplexEngine::new();
            let mut fq_mm = ComplexEngine::new();
            for k in 0..N {
                fq_m.a[k] = 0.5*(pq.eng.a[k]+pm.eng.a[k]); fq_m.b[k] = 0.5*(pq.eng.b[k]+pm.eng.b[k]);
                fq_m.sa[k] = pq.eng.sa[k]+pm.eng.sa[k]; fq_m.sb[k] = pq.eng.sb[k]+pm.eng.sb[k];
                fq_mm.a[k] = 0.5*(pq.eng.a[k]+pmm.eng.a[k]); fq_mm.b[k] = 0.5*(pq.eng.b[k]+pmm.eng.b[k]);
                fq_mm.sa[k] = pq.eng.sa[k]+pmm.eng.sa[k]; fq_mm.sb[k] = pq.eng.sb[k]+pmm.eng.sb[k];
            }
            for eng in [&mut fq_m, &mut fq_mm] {
                let mx = (0..N).map(|k| eng.sa[k].abs().max(eng.sb[k].abs())).fold(0.0f32, f32::max);
                if mx > 0.0 { let inv=1.0/mx; for k in 0..N { eng.sa[k]*=inv; eng.sb[k]*=inv; } }
                eng.evolve_steps(FUSION_STEPS);
            }
            let em = energy_real_only(&fq_m);
            let emm = energy_real_only(&fq_mm);
            let d = if emm != 0.0 { (emm-em)/emm.abs()*100.0 } else { 0.0 };
            (em < emm, d)
        }
        Cond::C_ImagOnly => {
            let mut fq_m = ComplexEngine::new();
            let mut fq_mm = ComplexEngine::new();
            for k in 0..N {
                fq_m.a[k] = 0.5*(pq.eng.a[k]+pm.eng.a[k]); fq_m.b[k] = 0.5*(pq.eng.b[k]+pm.eng.b[k]);
                fq_m.sa[k] = pq.eng.sa[k]+pm.eng.sa[k]; fq_m.sb[k] = pq.eng.sb[k]+pm.eng.sb[k];
                fq_mm.a[k] = 0.5*(pq.eng.a[k]+pmm.eng.a[k]); fq_mm.b[k] = 0.5*(pq.eng.b[k]+pmm.eng.b[k]);
                fq_mm.sa[k] = pq.eng.sa[k]+pmm.eng.sa[k]; fq_mm.sb[k] = pq.eng.sb[k]+pmm.eng.sb[k];
            }
            for eng in [&mut fq_m, &mut fq_mm] {
                let mx = (0..N).map(|k| eng.sa[k].abs().max(eng.sb[k].abs())).fold(0.0f32, f32::max);
                if mx > 0.0 { let inv=1.0/mx; for k in 0..N { eng.sa[k]*=inv; eng.sb[k]*=inv; } }
                eng.evolve_steps(FUSION_STEPS);
            }
            let em = energy_imag_only(&fq_m);
            let emm = energy_imag_only(&fq_mm);
            let d = if emm != 0.0 { (emm-em)/emm.abs()*100.0 } else { 0.0 };
            (em < emm, d)
        }
        Cond::E_Amplitude => {
            let sm = amplitude_similarity(&pq.eng, &pm.eng);
            let smm = amplitude_similarity(&pq.eng, &pmm.eng);
            let d = if smm.abs() > 0.0 { (sm - smm) / smm.abs() * 100.0 } else { 0.0 };
            (sm > smm, d)
        }
        Cond::F_Phase => {
            let sm = phase_similarity(&pq.eng, &pm.eng);
            let smm = phase_similarity(&pq.eng, &pmm.eng);
            let d = if smm.abs() > 0.0 { (sm - smm) / smm.abs() * 100.0 } else { 0.0 };
            (sm > smm, d)
        }
        _ => {
            // A, D, G, H: full complex energy matching via fusion
            let em = fuse_and_energy(&pq.eng, &pm.eng, cond);
            let emm = fuse_and_energy(&pq.eng, &pmm.eng, cond);
            let d = if emm != 0.0 { (emm-em)/emm.abs()*100.0 } else { 0.0 };
            (em < emm, d)
        }
    }
}

#[derive(Serialize)]
struct PairResult { query: String, correct: bool, delta: f32 }

#[derive(Serialize)]
struct RunResult { run: usize, accuracy: f64, pairs: Vec<PairResult> }

#[derive(Serialize)]
struct CondResult { name: String, runs: Vec<RunResult>, mean_accuracy: f64 }

fn run_condition(cond: Cond) -> CondResult {
    let mut runs = Vec::new();
    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();

        let results: Vec<PairResult> = PAIRS_T4.par_iter().enumerate().map(|(i, &(q, m, mm))| {
            let seed = seed_off + i as u64;
            let pq = process_text(q, seed, cond);
            let pm = process_text(m, seed + 100, cond);
            let pmm = process_text(mm, seed + 200, cond);
            let (correct, delta) = judge_pair(&pq, &pm, &pmm, cond);
            PairResult { query: q.chars().take(12).collect(), correct, delta }
        }).collect();

        let wall = t0.elapsed().as_secs_f64();
        let acc = results.iter().filter(|p| p.correct).count() as f64 / results.len() as f64;
        eprintln!("  {} run {}: acc={:.0}% ({:.1}s)", cond.name(), run+1, acc*100.0, wall);
        runs.push(RunResult { run: run+1, accuracy: acc, pairs: results });
    }
    let mean = runs.iter().map(|r| r.accuracy).sum::<f64>() / runs.len() as f64;
    CondResult { name: cond.name().to_string(), runs, mean_accuracy: mean }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp013: Complex Field Mechanism Analysis");
    eprintln!("============================================================");
    let t0 = Instant::now();

    let conds = [
        Cond::A_Full, Cond::B_RealOnly, Cond::C_ImagOnly, Cond::D_Decoupled,
        Cond::E_Amplitude, Cond::F_Phase, Cond::G_SwapSplit, Cond::H_RandomSplit,
    ];

    let mut all = Vec::new();
    for &cond in &conds {
        eprintln!("\n--- {} ---", cond.name());
        all.push(run_condition(cond));
    }

    let elapsed = t0.elapsed().as_secs_f64();
    let acc = |i: usize| all[i].mean_accuracy;

    eprintln!("\n============================================================");
    eprintln!("  MECHANISM ANALYSIS RESULTS");
    eprintln!("------------------------------------------------------------");
    for r in &all {
        let accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy*100.0)).collect();
        eprintln!("  {:20}: mean={:.0}%  [{}]", r.name, r.mean_accuracy*100.0, accs.join(", "));
    }

    eprintln!("\n  Key findings:");
    eprintln!("    D_decoupled ({:.0}%) vs A_full ({:.0}%): U|U|² coupling {}",
        acc(3)*100.0, acc(0)*100.0,
        if acc(0) > acc(3) + 0.1 { "IS the key" } else if acc(3) > acc(0) + 0.1 { "NOT needed" } else { "marginal" });
    eprintln!("    B_real ({:.0}%) vs C_imag ({:.0}%): info in {}",
        acc(1)*100.0, acc(2)*100.0,
        if (acc(1) - acc(2)).abs() < 0.1 { "both equally" } else if acc(1) > acc(2) { "real part" } else { "imag part" });
    eprintln!("    E_amplitude ({:.0}%) vs F_phase ({:.0}%): signal in {}",
        acc(4)*100.0, acc(5)*100.0,
        if acc(4) > acc(5) + 0.1 { "amplitude" } else if acc(5) > acc(4) + 0.1 { "phase" } else { "both" });
    eprintln!("    G_swap ({:.0}%) vs A ({:.0}%): split order {}",
        acc(6)*100.0, acc(0)*100.0,
        if (acc(6) - acc(0)).abs() < 0.1 { "doesn't matter" } else { "matters" });
    eprintln!("    H_random ({:.0}%) vs A ({:.0}%): bit order {}",
        acc(7)*100.0, acc(0)*100.0,
        if (acc(7) - acc(0)).abs() < 0.1 { "doesn't matter" } else { "matters" });
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp013_mechanism_analysis" },
        "conditions": all, "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp013_results.json"), serde_json::to_string_pretty(&output).unwrap());
    let mut s = String::from("Exp013: Mechanism Analysis\n\n");
    for r in &all { s.push_str(&format!("{}: {:.0}%\n", r.name, r.mean_accuracy*100.0)); }
    s.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp013_summary.txt"), s);
}
