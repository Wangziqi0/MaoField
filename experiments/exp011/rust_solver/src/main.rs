mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

const INIT_STEPS: usize = 1000;
const FUSION_STEPS: usize = 2000;
const M2_ROUNDS: usize = 5;
const STEPS_PER_ROUND: usize = 1000;
const N_RUNS: usize = 3;

const PAIRS: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "合同当事人应当按照约定全面履行各自的义务"),
    ("偷了别人的钱包", "秘密窃取他人随身携带的财物属于扒窃行为", "夫妻离婚时共同���务应当共同偿还"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于��险驾驶行为", "遗产按照法定继承办理���第一顺序继承人继承"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "经营者不得对消费者进行侮辱诽谤侵犯人格尊严"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "劳动者享有���等就业和选择��业的权利"),
    ("两口子过不下去了", "夫妻感情确已破裂经调��无���应准��解除婚姻", "盗窃公私财物数额特别巨大处十年以上有期徒刑"),
    ("朋友欠钱一直拖着", "债务人未按约定��行还款义务债权人可主张权利", "国家���行劳动者每日工作时间不超过八小时的制度"),
    ("房子到期了不让住了", "租赁合��届满后承租人拒不腾退出租人可诉请返还", "生产销售���药的处三年以下有期徒刑并处罚金"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "父���对未成年子女负有抚养教育和保护的义务"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "侵占他人财物数额较大拒不退还的处二年以下有期徒刑"),
];

#[derive(Clone, Copy)]
enum Cond { ScalarFixed, ScalarM2, ComplexFixed, ComplexM2, ComplexPhase }

impl Cond {
    fn name(&self) -> &'static str {
        match self {
            Cond::ScalarFixed => "A_scalar",
            Cond::ScalarM2 => "B_scalar_M2",
            Cond::ComplexFixed => "C_complex",
            Cond::ComplexM2 => "D_complex_M2",
            Cond::ComplexPhase => "E_complex_phase",
        }
    }
}

#[derive(Serialize, Clone)]
struct PairResult { query: String, correct: bool, delta: f32, method: String }

#[derive(Serialize)]
struct RunResult { run: usize, accuracy: f64, pairs: Vec<PairResult> }

#[derive(Serialize)]
struct CondResult { name: String, runs: Vec<RunResult>, mean_accuracy: f64 }

/// Scalar: process text, return (u, s).
fn scalar_process(text: &str, seed: u64, use_m2: bool) -> (Vec<f32>, Vec<f32>) {
    let mut eng = ScalarEngine::new();
    eng.init_u(seed);
    eng.set_source(&build_source_f32(text));
    if use_m2 {
        for _ in 0..M2_ROUNDS {
            eng.evolve_steps(STEPS_PER_ROUND);
            eng.update_source_m2();
        }
    } else {
        eng.evolve_steps(INIT_STEPS + (M2_ROUNDS - 1) * STEPS_PER_ROUND);
    }
    (eng.u, eng.s)
}

fn scalar_fuse(u_q: &[f32], u_d: &[f32], s_q: &[f32], s_d: &[f32]) -> f32 {
    let mut eng = ScalarEngine::new();
    for k in 0..N { eng.u[k] = 0.5 * (u_q[k] + u_d[k]); }
    for k in 0..N { eng.s[k] = s_q[k] + s_d[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

/// Complex: process text, return engine (owns a, b, sa, sb).
fn complex_process(text: &str, seed: u64, use_m2: bool) -> ComplexEngine {
    let mut eng = ComplexEngine::new();
    eng.init_u(seed);
    let (sa, sb) = build_source_complex(text);
    eng.set_source(&sa, &sb);
    if use_m2 {
        for _ in 0..M2_ROUNDS {
            eng.evolve_steps(STEPS_PER_ROUND);
            eng.update_source_m2_complex();
        }
    } else {
        eng.evolve_steps(INIT_STEPS + (M2_ROUNDS - 1) * STEPS_PER_ROUND);
    }
    eng
}

fn complex_fuse_energy(eq: &ComplexEngine, ed: &ComplexEngine) -> f32 {
    let mut eng = ComplexEngine::new();
    for k in 0..N {
        eng.a[k] = 0.5 * (eq.a[k] + ed.a[k]);
        eng.b[k] = 0.5 * (eq.b[k] + ed.b[k]);
        eng.sa[k] = eq.sa[k] + ed.sa[k];
        eng.sb[k] = eq.sb[k] + ed.sb[k];
    }
    // Normalize source jointly
    let mx = (0..N).map(|k| eng.sa[k].abs().max(eng.sb[k].abs())).fold(0.0f32, f32::max);
    if mx > 0.0 {
        let inv = 1.0 / mx;
        for k in 0..N { eng.sa[k] *= inv; eng.sb[k] *= inv; }
    }
    eng.evolve_steps(FUSION_STEPS);
    eng.compute_energy()
}

fn run_pair(idx: usize, q: &str, m: &str, mm: &str, cond: Cond, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let (correct, delta, method) = match cond {
        Cond::ScalarFixed | Cond::ScalarM2 => {
            let use_m2 = matches!(cond, Cond::ScalarM2);
            let (uq, sq) = scalar_process(q, seed, use_m2);
            let (um, sm) = scalar_process(m, seed+100, use_m2);
            let (umm, smm) = scalar_process(mm, seed+200, use_m2);
            let em = scalar_fuse(&uq, &um, &sq, &sm);
            let emm = scalar_fuse(&uq, &umm, &sq, &smm);
            let d = if emm != 0.0 { (emm - em) / emm.abs() * 100.0 } else { 0.0 };
            (em < emm, d, "energy".to_string())
        }
        Cond::ComplexFixed | Cond::ComplexM2 => {
            let use_m2 = matches!(cond, Cond::ComplexM2);
            let eq = complex_process(q, seed, use_m2);
            let em_eng = complex_process(m, seed+100, use_m2);
            let emm_eng = complex_process(mm, seed+200, use_m2);
            let em = complex_fuse_energy(&eq, &em_eng);
            let emm = complex_fuse_energy(&eq, &emm_eng);
            let d = if emm != 0.0 { (emm - em) / emm.abs() * 100.0 } else { 0.0 };
            (em < emm, d, "energy".to_string())
        }
        Cond::ComplexPhase => {
            let eq = complex_process(q, seed, true);
            let em_eng = complex_process(m, seed+100, true);
            let emm_eng = complex_process(mm, seed+200, true);
            let pq = eq.phase_field();
            let pm = em_eng.phase_field();
            let pmm = emm_eng.phase_field();
            let dm = phase_distance(&pq, &pm);
            let dmm = phase_distance(&pq, &pmm);
            let d = if dmm != 0.0 { (dmm - dm) / dmm.abs() * 100.0 } else { 0.0 };
            (dm < dmm, d, "phase".to_string())
        }
    };
    PairResult { query: q.chars().take(12).collect(), correct, delta, method }
}

fn run_condition(cond: Cond) -> CondResult {
    let mut runs = Vec::new();
    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();
        let results: Vec<PairResult> = PAIRS.par_iter().enumerate()
            .map(|(i, &(q, m, mm))| run_pair(i, q, m, mm, cond, seed_off))
            .collect();
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
    eprintln!("MaoField Exp011: Clifford Cl(1) Complex Field");
    eprintln!("============================================================");
    let t0 = Instant::now();

    let mut all = Vec::new();
    for &cond in &[Cond::ScalarFixed, Cond::ScalarM2, Cond::ComplexFixed, Cond::ComplexM2, Cond::ComplexPhase] {
        eprintln!("\n--- {} ---", cond.name());
        all.push(run_condition(cond));
    }

    let elapsed = t0.elapsed().as_secs_f64();

    eprintln!("\n============================================================");
    eprintln!("  RESULTS");
    eprintln!("------------------------------------------------------------");
    for r in &all {
        let accs: Vec<String> = r.runs.iter().map(|rr| format!("{:.0}%", rr.accuracy*100.0)).collect();
        eprintln!("  {:20}: mean={:.0}%  runs=[{}]", r.name, r.mean_accuracy*100.0, accs.join(", "));
    }
    let acc = |i: usize| all[i].mean_accuracy;
    eprintln!("\n  Key comparisons:");
    eprintln!("    D_complex_M2 ({:.0}%) vs B_scalar_M2 ({:.0}%): Clifford {}",
        acc(3)*100.0, acc(1)*100.0, if acc(3) > acc(1) + 0.05 { "HELPS" } else { "no effect" });
    eprintln!("    E_phase ({:.0}%) vs D_energy ({:.0}%): Phase {}",
        acc(4)*100.0, acc(3)*100.0, if acc(4) > acc(3) + 0.05 { "HELPS" } else { "no effect" });
    if acc(3).max(acc(4)) > 0.6 {
        eprintln!("    ★ Clifford > 60% on same-domain!");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp011_clifford_cl1" },
        "conditions": all,
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp011_results.json"), serde_json::to_string_pretty(&output).unwrap());
    let mut s = String::from("Exp011: Clifford Cl(1)\n\n");
    for r in &all { s.push_str(&format!("{}: mean={:.0}%\n", r.name, r.mean_accuracy*100.0)); }
    s.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp011_summary.txt"), s);
}
