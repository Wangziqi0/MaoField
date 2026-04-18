mod engine;

use engine::*;
use rayon::prelude::*;
use serde::Serialize;
use std::time::Instant;

const INIT_STEPS: usize = 1000;
const FUSION_STEPS: usize = 2000;
const MAX_ROUNDS: usize = 5;
const TOP_K: usize = 10;
const CONVERGENCE_TOL: f32 = 0.01;
const CORPUS_SIZE: usize = 200;
const DB_PATH: &str = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db";
const N_RUNS: usize = 3;

// Same-domain mismatch: query and match are semantically related (different wording),
// mismatch is ALSO a legal text but semantically unrelated.
const PAIRS: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗",
     "殴打致人轻伤依据刑法第二百三十四条处以刑罚",
     "合同当事人应当按照约定全面履行各自的义务"),
    ("偷了别人的钱包",
     "秘密窃取他人随身携带的财物属于扒窃行为",
     "夫妻离婚时共同债务应当共同偿还"),
    ("喝了酒还开车上路",
     "饮酒后操控机动车辆属于危险驾驶行为",
     "遗产按照法定继承办理由第一顺序继承人继承"),
    ("把人弄死了",
     "非法剥夺他人生命的行为构成最严重的刑事犯罪",
     "经营者不得对消费者进行侮辱诽谤侵犯人格尊严"),
    ("骗了老人的养老钱",
     "以虚构事实隐瞒真相手段非法占有他人财物",
     "劳动者享有平等就业和选择职业的权利"),
    ("两口子过不下去了",
     "夫妻感情确已破裂经调解无效应准予解除婚姻",
     "盗窃公私财物数额特别巨大处十年以上有期徒刑"),
    ("朋友欠钱一直拖着",
     "债务人未按约定履行还款义务债权人可主张权利",
     "国家实行劳动者每日工作时间不超过八小时的制度"),
    ("房子到期了不让住了",
     "租赁合同届满后承租人拒不腾退出租人可诉请返还",
     "生产销售假药的处三年以下有期徒刑并处罚金"),
    ("买的东西是假的",
     "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿",
     "父母对未成年子女负有抚养教育和保护的义务"),
    ("老板突然不要我了",
     "未经法定程序单方终止劳动关系的用工方应承担赔偿责任",
     "侵占他人财物数额较大拒不退还的处二年以下有期徒刑"),
];

fn load_corpus() -> Vec<String> {
    let conn = rusqlite::Connection::open(DB_PATH).expect("DB open failed");
    let mut stmt = conn.prepare("SELECT content FROM law_chunks ORDER BY RANDOM() LIMIT ?1").unwrap();
    let rows: Vec<String> = stmt.query_map(rusqlite::params![CORPUS_SIZE], |row| row.get(0))
        .unwrap().map(|r| r.unwrap()).collect();
    let mut texts = rows;
    let mut rng: u64 = 42;
    for i in (1..texts.len()).rev() {
        rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1);
        let j = (rng >> 33) as usize % (i + 1);
        texts.swap(i, j);
    }
    texts
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
    mean_avg_delta: f32,
}

fn process_text(text: &str, seed: u64, corpus: &[Vec<f32>], use_m2: bool) -> (Vec<f32>, Vec<f32>) {
    let mut eng = MaoFieldEngine::new();
    eng.init_u(seed);
    eng.set_source(&build_source_f32(text));
    eng.evolve_adaptive(INIT_STEPS, 200, 1e-4);
    if use_m2 {
        eng.adjoint_iteration_m2(corpus, MAX_ROUNDS, TOP_K, CONVERGENCE_TOL);
    } else {
        eng.adjoint_iteration_fixed(corpus, MAX_ROUNDS, TOP_K, CONVERGENCE_TOL);
    }
    (eng.u, eng.s)
}

fn fuse_and_score(u_q: &[f32], u_d: &[f32], s_q: &[f32], s_d: &[f32]) -> f32 {
    let mut eng = MaoFieldEngine::new();
    for k in 0..N { eng.u[k] = 0.5 * (u_q[k] + u_d[k]); }
    for k in 0..N { eng.s[k] = s_q[k] + s_d[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_adaptive(FUSION_STEPS, 500, 1e-4);
    eng.compute_energy()
}

fn run_pair(idx: usize, q: &str, m: &str, mm: &str,
            corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let (u_q, s_q) = process_text(q, seed, corpus, use_m2);
    let (u_m, s_m) = process_text(m, seed + 100, corpus, use_m2);
    let (u_mm, s_mm) = process_text(mm, seed + 200, corpus, use_m2);
    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm);
    let correct = e_m < e_mm;
    let delta = if e_mm != 0.0 { (e_mm - e_m) / e_mm.abs() * 100.0 } else { 0.0 };
    PairResult {
        query: q.chars().take(12).collect(),
        e_match: e_m, e_mismatch: e_mm, correct, delta,
    }
}

fn run_one_pass(corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> Vec<PairResult> {
    PAIRS.par_iter().enumerate()
        .map(|(i, &(q, m, mm))| run_pair(i, q, m, mm, corpus, use_m2, seed_off))
        .collect()
}

fn run_condition(name: &str, corpus: &[Vec<f32>], use_m2: bool) -> CondResult {
    let mut runs = Vec::new();
    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();
        let pairs = run_one_pass(corpus, use_m2, seed_off);
        let wall = t0.elapsed().as_secs_f64();
        let correct = pairs.iter().filter(|p| p.correct).count();
        let acc = correct as f64 / pairs.len() as f64;
        let avg_d = pairs.iter().map(|p| p.delta).sum::<f32>() / pairs.len() as f32;
        eprintln!("  {} run {}: acc={:.0}% avg_Δ={:.1}% ({:.1}s)", name, run + 1, acc * 100.0, avg_d, wall);
        // Print per-pair
        for p in &pairs {
            let mark = if p.correct { "✓" } else { "✗" };
            eprintln!("    {} {} E_m={:.0} E_mm={:.0} Δ={:.1}%", p.query, mark, p.e_match, p.e_mismatch, p.delta);
        }
        runs.push(RunResult { run: run + 1, accuracy: acc, avg_delta: avg_d, pairs });
    }
    let mean_acc = runs.iter().map(|r| r.accuracy).sum::<f64>() / runs.len() as f64;
    let mean_d = runs.iter().map(|r| r.avg_delta).sum::<f32>() / runs.len() as f32;
    CondResult { name: name.to_string(), runs, mean_accuracy: mean_acc, mean_avg_delta: mean_d }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp008b: Same-Domain Mismatch — Final Gate");
    eprintln!("============================================================");
    let t0 = Instant::now();

    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  {} texts", corpus_texts.len());

    let tp = Instant::now();
    let corpus: Vec<Vec<f32>> = corpus_texts.par_iter().map(|t| build_source_f32(t)).collect();
    eprintln!("  Sources in {:.0}ms", tp.elapsed().as_secs_f64() * 1000.0);

    let mut results = Vec::new();

    eprintln!("\n--- A: Fixed S ---");
    results.push(run_condition("A_fixed", &corpus, false));
    eprintln!("\n--- B2: M2 S·u* ---");
    results.push(run_condition("B2_m2", &corpus, true));

    let elapsed = t0.elapsed().as_secs_f64();
    let a = &results[0];
    let b = &results[1];

    eprintln!("\n============================================================");
    eprintln!("  FINAL GATE RESULTS");
    eprintln!("------------------------------------------------------------");
    eprintln!("  A  mean: {:.0}% (runs: {})", a.mean_accuracy * 100.0,
        a.runs.iter().map(|r| format!("{:.0}%", r.accuracy * 100.0)).collect::<Vec<_>>().join(", "));
    eprintln!("  B2 mean: {:.0}% (runs: {})", b.mean_accuracy * 100.0,
        b.runs.iter().map(|r| format!("{:.0}%", r.accuracy * 100.0)).collect::<Vec<_>>().join(", "));
    eprintln!();
    if a.mean_accuracy > 0.6 || b.mean_accuracy > 0.6 {
        eprintln!("  ★★★ >60%: TRUE SEMANTIC UNDERSTANDING CONFIRMED ★★★");
        eprintln!("  System distinguishes semantic relevance WITHIN legal domain.");
    } else if a.mean_accuracy > 0.5 || b.mean_accuracy > 0.5 {
        eprintln!("  ~ 50-60%: Weak signal. Possibly domain detection leaking through.");
    } else {
        eprintln!("  ✗ ≤50%: Domain detection only. Previous results were law-vs-non-law.");
    }
    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp008b_same_domain_mismatch" },
        "conditions": results,
        "summary": { "A_mean": a.mean_accuracy, "B2_mean": b.mean_accuracy },
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp008b_results.json"), serde_json::to_string_pretty(&output).unwrap());
    let summary = format!(
        "Exp008b: Same-Domain Mismatch\n\nA: {:.0}% ({})\nB2: {:.0}% ({})\nTime: {:.1}s\n",
        a.mean_accuracy * 100.0, a.runs.iter().map(|r| format!("{:.0}%", r.accuracy * 100.0)).collect::<Vec<_>>().join(", "),
        b.mean_accuracy * 100.0, b.runs.iter().map(|r| format!("{:.0}%", r.accuracy * 100.0)).collect::<Vec<_>>().join(", "),
        elapsed
    );
    let _ = std::fs::write(results_dir.join("exp008b_summary.txt"), summary);
}
