mod engine;
mod topo;

use engine::*;
use topo::*;
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

// exp008b same-domain pairs (hardest test)
const PAIRS_SAME_DOMAIN: &[(&str, &str, &str)] = &[
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

// exp008 Type 2 cross-domain pairs (easier, for calibration)
const PAIRS_CROSS_DOMAIN: &[(&str, &str, &str)] = &[
    ("打人会坐牢吗", "殴打致人轻伤依据刑法第二百三十四条处以刑罚", "打印机维修服务保修条款"),
    ("偷了别人的钱包", "秘密窃取他人随身携带的财物属于扒窃行为", "钱包品牌皮具保养方法"),
    ("喝了酒还开车上路", "饮酒后操控机动车辆属于危险驾驶行为", "开车自驾游路线推荐"),
    ("把人弄死了", "非法剥夺他人生命的行为构成最严重的刑事犯罪", "弄堂里的老上海风情"),
    ("骗了老人的养老钱", "以虚构事实隐瞒真相手段非法占有他人财物", "养老保险缴费年限计算方式"),
    ("两口子过不下去了", "夫妻感情确已破裂经调解无效应准予解除婚姻", "下载安装软件步骤说明"),
    ("朋友欠钱一直拖着", "债务人未按约定履行还款义务债权人可主张权利", "拖地机器人使用说明书"),
    ("房子到期了不让住了", "租赁合同届满后承租人拒不腾退出租人可诉请返还", "住了三年的二手房装修翻新"),
    ("买的东西是假的", "销售者提供的商品掺杂掺假以次充好应承担惩罚性赔偿", "买的新款手机开箱评测"),
    ("老板突然不要我了", "未经法定程序单方终止劳动关系的用工方应承担赔偿责任", "要我说这道菜的做法其实很简单"),
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

/// Process text -> (u_final, s_final, topo_features)
fn process_text(text: &str, seed: u64, corpus: &[Vec<f32>], use_m2: bool) -> (Vec<f32>, Vec<f32>, TopoFeatures) {
    let mut eng = MaoFieldEngine::new();
    eng.init_u(seed);
    eng.set_source(&build_source_f32(text));
    eng.evolve_adaptive(INIT_STEPS, 200, 1e-4);
    if use_m2 {
        eng.adjoint_iteration_m2(corpus, MAX_ROUNDS, TOP_K, CONVERGENCE_TOL);
    } else {
        eng.adjoint_iteration_fixed(corpus, MAX_ROUNDS, TOP_K, CONVERGENCE_TOL);
    }
    let topo = TopoFeatures::extract(&eng.u);
    (eng.u, eng.s, topo)
}

fn fuse_and_score(u_q: &[f32], u_d: &[f32], s_q: &[f32], s_d: &[f32]) -> f32 {
    let mut eng = MaoFieldEngine::new();
    for k in 0..N { eng.u[k] = 0.5 * (u_q[k] + u_d[k]); }
    for k in 0..N { eng.s[k] = s_q[k] + s_d[k]; }
    normalize_f32(&mut eng.s);
    eng.evolve_adaptive(FUSION_STEPS, 500, 1e-4);
    eng.compute_energy()
}

#[derive(Serialize, Clone)]
struct PairResult {
    query: String,
    // Energy matching
    e_match: f32,
    e_mismatch: f32,
    energy_correct: bool,
    // Topo euclidean
    topo_dist_match: f32,
    topo_dist_mismatch: f32,
    topo_eucl_correct: bool,
    // Topo cosine
    topo_cos_match: f32,
    topo_cos_mismatch: f32,
    topo_cos_correct: bool,
    // Betti
    betti_dist_match: f32,
    betti_dist_mismatch: f32,
    betti_correct: bool,
}

fn run_pair(idx: usize, q: &str, m: &str, mm: &str,
            corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;

    let (u_q, s_q, topo_q) = process_text(q, seed, corpus, use_m2);
    let (u_m, s_m, topo_m) = process_text(m, seed + 100, corpus, use_m2);
    let (u_mm, s_mm, topo_mm) = process_text(mm, seed + 200, corpus, use_m2);

    // Energy matching (fusion)
    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm);

    // Topo feature vectors
    let v_q = topo_q.to_vec();
    let v_m = topo_m.to_vec();
    let v_mm = topo_mm.to_vec();

    // Euclidean distance (lower = more similar)
    let td_m = euclidean_dist(&v_q, &v_m);
    let td_mm = euclidean_dist(&v_q, &v_mm);

    // Cosine similarity (higher = more similar)
    let tc_m = cosine_sim(&v_q, &v_m);
    let tc_mm = cosine_sim(&v_q, &v_mm);

    // Betti distance (lower = more similar)
    let bd_m = betti_dist(&topo_q, &topo_m);
    let bd_mm = betti_dist(&topo_q, &topo_mm);

    PairResult {
        query: q.chars().take(12).collect(),
        e_match: e_m, e_mismatch: e_mm,
        energy_correct: e_m < e_mm,
        topo_dist_match: td_m, topo_dist_mismatch: td_mm,
        topo_eucl_correct: td_m < td_mm,
        topo_cos_match: tc_m, topo_cos_mismatch: tc_mm,
        topo_cos_correct: tc_m > tc_mm,
        betti_dist_match: bd_m, betti_dist_mismatch: bd_mm,
        betti_correct: bd_m < bd_mm,
    }
}

#[derive(Serialize)]
struct RunResult {
    run: usize,
    energy_acc: f64,
    topo_eucl_acc: f64,
    topo_cos_acc: f64,
    betti_acc: f64,
    pairs: Vec<PairResult>,
}

#[derive(Serialize)]
struct CondResult {
    name: String,
    pair_set: String,
    use_m2: bool,
    runs: Vec<RunResult>,
    mean_energy: f64,
    mean_topo_eucl: f64,
    mean_topo_cos: f64,
    mean_betti: f64,
}

fn run_condition(name: &str, pairs: &[(&str, &str, &str)], pair_set: &str,
                 corpus: &[Vec<f32>], use_m2: bool) -> CondResult {
    let mut runs = Vec::new();
    let mut ea = Vec::new();
    let mut ta = Vec::new();
    let mut ca = Vec::new();
    let mut ba = Vec::new();

    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();
        let results: Vec<PairResult> = pairs.par_iter().enumerate()
            .map(|(i, &(q, m, mm))| run_pair(i, q, m, mm, corpus, use_m2, seed_off))
            .collect();
        let wall = t0.elapsed().as_secs_f64();
        let n = results.len() as f64;
        let e_acc = results.iter().filter(|p| p.energy_correct).count() as f64 / n;
        let t_acc = results.iter().filter(|p| p.topo_eucl_correct).count() as f64 / n;
        let c_acc = results.iter().filter(|p| p.topo_cos_correct).count() as f64 / n;
        let b_acc = results.iter().filter(|p| p.betti_correct).count() as f64 / n;

        eprintln!("  {} run {}: E={:.0}% T_eucl={:.0}% T_cos={:.0}% Betti={:.0}% ({:.1}s)",
            name, run + 1, e_acc * 100.0, t_acc * 100.0, c_acc * 100.0, b_acc * 100.0, wall);

        ea.push(e_acc); ta.push(t_acc); ca.push(c_acc); ba.push(b_acc);
        runs.push(RunResult { run: run + 1, energy_acc: e_acc, topo_eucl_acc: t_acc, topo_cos_acc: c_acc, betti_acc: b_acc, pairs: results });
    }

    let mean = |v: &[f64]| v.iter().sum::<f64>() / v.len() as f64;
    CondResult {
        name: name.to_string(), pair_set: pair_set.to_string(), use_m2,
        runs, mean_energy: mean(&ea), mean_topo_eucl: mean(&ta), mean_topo_cos: mean(&ca), mean_betti: mean(&ba),
    }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp009: Topological Feature Matching");
    eprintln!("============================================================");
    let t0 = Instant::now();

    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  {} texts", corpus_texts.len());
    let tp = Instant::now();
    let corpus: Vec<Vec<f32>> = corpus_texts.par_iter().map(|t| build_source_f32(t)).collect();
    eprintln!("  Sources in {:.0}ms", tp.elapsed().as_secs_f64() * 1000.0);

    let mut all = Vec::new();

    // Same-domain (hardest)
    eprintln!("\n=== Same-domain mismatch (exp008b pairs) ===");
    all.push(run_condition("E-A", PAIRS_SAME_DOMAIN, "same_domain", &corpus, false));
    all.push(run_condition("T-A", PAIRS_SAME_DOMAIN, "same_domain", &corpus, false));
    // ^ T-A reuses E-A's field but we re-run for independent seeds; topo metrics extracted in same run
    all.push(run_condition("T-B2", PAIRS_SAME_DOMAIN, "same_domain", &corpus, true));

    // Cross-domain (calibration)
    eprintln!("\n=== Cross-domain mismatch (exp008 T2 pairs) ===");
    all.push(run_condition("E-A-cross", PAIRS_CROSS_DOMAIN, "cross_domain", &corpus, false));
    all.push(run_condition("T-A-cross", PAIRS_CROSS_DOMAIN, "cross_domain", &corpus, false));
    all.push(run_condition("T-B2-cross", PAIRS_CROSS_DOMAIN, "cross_domain", &corpus, true));

    let elapsed = t0.elapsed().as_secs_f64();

    eprintln!("\n============================================================");
    eprintln!("  RESULTS");
    eprintln!("------------------------------------------------------------");
    eprintln!("  {:14} {:>7} {:>7} {:>7} {:>7}", "", "Energy", "T_eucl", "T_cos", "Betti");
    for r in &all {
        eprintln!("  {:14} {:>6.0}% {:>6.0}% {:>6.0}% {:>6.0}%  [{}]",
            r.name, r.mean_energy * 100.0, r.mean_topo_eucl * 100.0,
            r.mean_topo_cos * 100.0, r.mean_betti * 100.0, r.pair_set);
    }

    // Find best topo method on same-domain
    let same_domain: Vec<&CondResult> = all.iter().filter(|r| r.pair_set == "same_domain").collect();
    let best_topo = same_domain.iter()
        .flat_map(|r| vec![
            (format!("{} eucl", r.name), r.mean_topo_eucl),
            (format!("{} cos", r.name), r.mean_topo_cos),
            (format!("{} betti", r.name), r.mean_betti),
        ])
        .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
        .unwrap();
    let best_energy = same_domain.iter().map(|r| r.mean_energy).fold(0.0f64, f64::max);

    eprintln!("\n  Same-domain verdict:");
    eprintln!("    Best energy: {:.0}%", best_energy * 100.0);
    eprintln!("    Best topo:   {:.0}% ({})", best_topo.1 * 100.0, best_topo.0);
    if best_topo.1 > 0.6 {
        eprintln!("    ★ TOPO > 60%: Topological features capture semantic structure!");
    } else if best_topo.1 > best_energy + 0.1 {
        eprintln!("    △ Topo better than energy by >10pp, but below 60%");
    } else {
        eprintln!("    ✗ Topo ≈ energy: topological features don't help with bit source fields");
    }

    eprintln!("  Time: {:.1}s", elapsed);
    eprintln!("============================================================");

    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp009_topo_matching" },
        "conditions": all,
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp009_results.json"), serde_json::to_string_pretty(&output).unwrap());

    let mut summary = String::from("Exp009: Topological Feature Matching\n\n");
    summary.push_str(&format!("{:14} {:>7} {:>7} {:>7} {:>7}\n", "", "Energy", "T_eucl", "T_cos", "Betti"));
    for r in &all {
        summary.push_str(&format!("{:14} {:>6.0}% {:>6.0}% {:>6.0}% {:>6.0}%  [{}]\n",
            r.name, r.mean_energy * 100.0, r.mean_topo_eucl * 100.0,
            r.mean_topo_cos * 100.0, r.mean_betti * 100.0, r.pair_set));
    }
    summary.push_str(&format!("\nTime: {:.1}s\n", elapsed));
    let _ = std::fs::write(results_dir.join("exp009_summary.txt"), summary);
}
