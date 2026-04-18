mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

const TOTAL_STEPS: usize = 5000;
const FUSION_STEPS: usize = 2000;
const CORPUS_SIZE: usize = 200;
const DB_PATH: &str = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db";
const N_RUNS: usize = 3;

// exp008b same-domain pairs
const PAIRS: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "合同当事人应当按照约定全面履行各自的义务"),
    ("偷了别人的钱包", "秘密窃取他人随身携带���财物属于扒窃行为", "夫妻离婚时共同债务应当共同偿还"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于危险驾驶行为", "遗产按照法定继承办理由第一顺序继承人继承"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "经营者不得对消费���进行侮辱诽谤侵犯人格尊严"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "劳动者享有平等就业和选择职业的权利"),
    ("两口子过不下去了", "夫妻感情确已破裂经调解无效应准予解除婚姻", "盗窃公私财物数额特别巨大处十年以上有期徒刑"),
    ("朋友欠钱一直拖着", "债务人未按约定履行还款义务债权人可主张权利", "国家实行劳动者每日工作时间不超过八小时���制度"),
    ("房子到期了不让住了", "租赁合同届满后承租人拒不腾退出租人可诉请返还", "生产销售假药的处三年以下有期徒刑并处罚金"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "父母对未成年子女负有��养教育和保护的义务"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "侵占他人财物数额较大拒不退还的处二年以下有期徒刑"),
];

#[derive(Clone, Copy, PartialEq)]
enum Mode {
    Fixed,       // A: S never changes
    M2Discrete,  // B: M2 every 1000 steps (5 rounds)
    ContC1,      // C1: S_current = S0 * u each step
    ContC2,      // C2: S_current = S0 * tanh(u) each step
}

impl Mode {
    fn name(&self) -> &'static str {
        match self {
            Mode::Fixed => "A_fixed",
            Mode::M2Discrete => "B_m2_discrete",
            Mode::ContC1 => "C1_cont_u",
            Mode::ContC2 => "C2_cont_tanh",
        }
    }
}

/// Evolve with continuous S update: each step, S_current = S0 * f(u).
/// Fused into the PDE step for performance.
fn evolve_continuous(eng: &mut MaoFieldEngine, s0: &[f32], n_steps: usize, use_tanh: bool) {
    let tab = &eng.nb;
    const D: f32 = 0.1;
    const DT: f32 = 0.1;
    const INV_DX2: f32 = 1.0;

    for _ in 0..n_steps {
        let u = &eng.u;
        let u_new = &mut eng.u_new;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ui = unsafe { *u.get_unchecked(k) };
            let s0k = unsafe { *s0.get_unchecked(k) };

            // Continuous S update: S_current = S0 * f(u)
            let si = if use_tanh {
                s0k * ui.tanh()  // C2: soft limit
            } else {
                s0k * ui          // C1: direct multiply
            };

            let lap = unsafe {
                *u.get_unchecked(nb[0]) + *u.get_unchecked(nb[1])
                + *u.get_unchecked(nb[2]) + *u.get_unchecked(nb[3])
                + *u.get_unchecked(nb[4]) + *u.get_unchecked(nb[5])
                - 6.0 * ui
            } * INV_DX2;
            let ui2 = ui * ui;
            let du = D * lap - ui2 * ui + ui + (1.0 - 3.0 * ui2) * si;
            let v = ui + DT * du;
            unsafe {
                *u_new.get_unchecked_mut(k) = if v > 2.0 { 2.0 } else if v < -2.0 { -2.0 } else { v };
            }
        }
        std::mem::swap(&mut eng.u, &mut eng.u_new);
    }
}

/// Process one text under given mode. Returns (u_final, s_final).
fn process_text(text: &str, seed: u64, mode: Mode) -> (Vec<f32>, Vec<f32>) {
    let mut eng = MaoFieldEngine::new();
    eng.init_u(seed);
    let s0 = build_source_f32(text);
    eng.set_source(&s0);

    match mode {
        Mode::Fixed => {
            eng.evolve_steps(TOTAL_STEPS);
        }
        Mode::M2Discrete => {
            // 5 rounds of 1000 steps, M2 update between rounds
            for _ in 0..5 {
                eng.evolve_steps(1000);
                eng.update_source_m2();
            }
        }
        Mode::ContC1 => {
            evolve_continuous(&mut eng, &s0, TOTAL_STEPS, false);
        }
        Mode::ContC2 => {
            evolve_continuous(&mut eng, &s0, TOTAL_STEPS, true);
        }
    }

    // For fusion, use the current S (which may have been updated)
    let s_final = eng.s.clone();
    (eng.u, s_final)
}

fn fuse_and_score(u_q: &[f32], u_d: &[f32], s_q: &[f32], s_d: &[f32]) -> f32 {
    let mut eng = MaoFieldEngine::new();
    for k in 0..N { eng.u[k] = 0.5 * (u_q[k] + u_d[k]); }
    for k in 0..N { eng.s[k] = s_q[k] + s_d[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

#[derive(Serialize, Clone)]
struct PairResult {
    query: String,
    e_match: f32,
    e_mismatch: f32,
    correct: bool,
    delta: f32,
}

#[derive(Serialize)]
struct RunResult {
    run: usize,
    accuracy: f64,
    avg_delta: f32,
    pairs: Vec<PairResult>,
}

#[derive(Serialize)]
struct CondResult {
    name: String,
    runs: Vec<RunResult>,
    mean_accuracy: f64,
    mean_delta: f32,
}

fn run_pair(idx: usize, q: &str, m: &str, mm: &str, mode: Mode, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let (u_q, s_q) = process_text(q, seed, mode);
    let (u_m, s_m) = process_text(m, seed + 100, mode);
    let (u_mm, s_mm) = process_text(mm, seed + 200, mode);
    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm);
    let correct = e_m < e_mm;
    let delta = if e_mm != 0.0 { (e_mm - e_m) / e_mm.abs() * 100.0 } else { 0.0 };
    PairResult { query: q.chars().take(12).collect(), e_match: e_m, e_mismatch: e_mm, correct, delta }
}

fn run_condition(mode: Mode) -> CondResult {
    let mut runs = Vec::new();
    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();
        let results: Vec<PairResult> = PAIRS.par_iter().enumerate()
            .map(|(i, &(q, m, mm))| run_pair(i, q, m, mm, mode, seed_off))
            .collect();
        let wall = t0.elapsed().as_secs_f64();
        let n = results.len() as f64;
        let acc = results.iter().filter(|p| p.correct).count() as f64 / n;
        let avg_d = results.iter().map(|p| p.delta).sum::<f32>() / results.len() as f32;
        eprintln!("  {} run {}: acc={:.0}% avg_Δ={:.1}% ({:.1}s)", mode.name(), run + 1, acc * 100.0, avg_d, wall);
        runs.push(RunResult { run: run + 1, accuracy: acc, avg_delta: avg_d, pairs: results });
    }
    let mean_acc = runs.iter().map(|r| r.accuracy).sum::<f64>() / runs.len() as f64;
    let mean_d = runs.iter().map(|r| r.avg_delta).sum::<f32>() / runs.len() as f32;
    CondResult { name: mode.name().to_string(), runs, mean_accuracy: mean_acc, mean_delta: mean_d }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp010: Continuous S Update");
    eprintln!("============================================================");
    let t0 = Instant::now();

    // Diagnostic: check C1 stability
    eprintln!("\nDiagnostic: C1 stability check (100 steps)...");
    {
        let mut eng = MaoFieldEngine::new();
        eng.init_u(999);
        let s0 = build_source_f32("测试稳定性");
        eng.set_source(&s0);
        evolve_continuous(&mut eng, &s0, 100, false);
        let u_max = eng.u.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
        let u_mean = eng.u.iter().map(|v| v.abs()).sum::<f32>() / N as f32;
        eprintln!("  C1 after 100 steps: u_max={:.4} u_mean={:.4}", u_max, u_mean);
        if u_max >= 2.0 {
            eprintln!("  WARNING: C1 hitting clamp limit, may be unstable");
        } else {
            eprintln!("  C1 looks stable");
        }
    }
    {
        let mut eng = MaoFieldEngine::new();
        eng.init_u(999);
        let s0 = build_source_f32("测试稳定性");
        eng.set_source(&s0);
        evolve_continuous(&mut eng, &s0, 100, true);
        let u_max = eng.u.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
        let u_mean = eng.u.iter().map(|v| v.abs()).sum::<f32>() / N as f32;
        eprintln!("  C2 after 100 steps: u_max={:.4} u_mean={:.4}", u_max, u_mean);
    }

    let mut all = Vec::new();

    eprintln!("\n--- Running conditions ---");
    all.push(run_condition(Mode::Fixed));
    all.push(run_condition(Mode::M2Discrete));
    all.push(run_condition(Mode::ContC1));
    all.push(run_condition(Mode::ContC2));

    let elapsed = t0.elapsed().as_secs_f64();

    eprintln!("\n============================================================");
    eprintln!("  RESULTS");
    eprintln!("------------------------------------------------------------");
    for r in &all {
        let accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy * 100.0)).collect();
        eprintln!("  {:18}: mean={:.0}%  avg_Δ={:.1}%  runs=[{}]",
            r.name, r.mean_accuracy * 100.0, r.mean_delta, accs.join(", "));
    }

    let acc = |i: usize| all[i].mean_accuracy;
    eprintln!("\n  Key comparisons:");
    eprintln!("    C1 ({:.0}%) vs A ({:.0}%): Continuous direct {}",
        acc(2) * 100.0, acc(0) * 100.0, if acc(2) > acc(0) + 0.05 { "HELPS" } else { "no effect" });
    eprintln!("    C2 ({:.0}%) vs A ({:.0}%): Continuous tanh {}",
        acc(3) * 100.0, acc(0) * 100.0, if acc(3) > acc(0) + 0.05 { "HELPS" } else { "no effect" });
    eprintln!("    C2 ({:.0}%) vs B ({:.0}%): Continuous vs discrete {}",
        acc(3) * 100.0, acc(1) * 100.0, if acc(3) > acc(1) + 0.05 { "continuous BETTER" } else { "same or worse" });

    let best = (0..4).max_by(|&a, &b| acc(a).partial_cmp(&acc(b)).unwrap()).unwrap();
    eprintln!("    Best: {} ({:.0}%)", all[best].name, acc(best) * 100.0);

    if acc(2).max(acc(3)) > 0.5 {
        eprintln!("\n    ★ Continuous update > 50% on same-domain!");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp010_continuous_s_update" },
        "conditions": all,
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp010_results.json"), serde_json::to_string_pretty(&output).unwrap());

    let mut summary = String::from("Exp010: Continuous S Update\n\n");
    for r in &all {
        let accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy * 100.0)).collect();
        summary.push_str(&format!("{}: mean={:.0}% runs=[{}]\n", r.name, r.mean_accuracy * 100.0, accs.join(", ")));
    }
    summary.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp010_summary.txt"), summary);
}
