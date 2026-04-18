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

// ===== Original 10 test pairs =====
const TEST_PAIRS_10: &[(&str, &str, &str)] = &[
    ("他打我要怎么判",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
     "用人单位应当按照劳动合同约定和国家规定向劳动者及时足额支付劳动报酬"),
    ("偷东西会怎么样",
     "盗窃公私财物数额较大的或者多次盗窃的处三年以下有期徒刑",
     "离婚时夫妻共同财产由双方协议处理"),
    ("醉酒开车怎么处罚",
     "醉酒驾驶机动车的由公安机关交通管理部门约束至酒醒吊销机动车驾驶证",
     "承揽人应当以自己的设备技术和劳力完成主要工作"),
    ("杀人判几年",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑",
     "当事人对合同条款的理解有争议的应当按照合同所使用的词句"),
    ("诈骗怎么判",
     "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金",
     "婚姻关系存续期间所得的工资奖金劳务报酬为夫妻共同财产"),
    ("离婚后房子怎么分",
     "离婚时夫妻共同财产由双方协议处理协议不成的由人民法院判决",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制"),
    ("借钱不还怎么办",
     "借款人应当按照约定的期限返还借款",
     "盗窃公私财物数额较大的处三年以下有期徒刑"),
    ("租房合同到期房东不退押金",
     "租赁期限届满承租人应当返还租赁物出租人应当退还押金",
     "醉酒驾驶机动车的由公安机关吊销机动车驾驶证"),
    ("买到假货怎么维权",
     "经营者提供商品或者服务有欺诈行为的应当按照消费者的要求增加赔偿",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑"),
    ("被公司辞退怎么赔偿",
     "用人单位违法解除劳动合同的应当按照经济补偿标准的二倍向劳动者支付赔偿金",
     "离婚时夫妻共同财产由双方协议处理"),
];

// ===== Extended 20 pairs for generalization =====
const TEST_PAIRS_EXT: &[(&str, &str, &str)] = &[
    ("交通事故怎么赔偿",
     "机动车发生交通事故造成人身伤亡财产损失的由保险公司在交强险责任限额范围内予以赔偿",
     "借款人应当按照约定的期限返还借款"),
    ("合同违约怎么办",
     "当事人一方不履行合同义务或者履行合同义务不符合约定的应当承担继续履行采取补救措施或者赔偿损失等违约责任",
     "盗窃公私财物数额较大的处三年以下有期徒刑"),
    ("遗产怎么继承",
     "继承开始后由第一顺序继承人继承第二顺序继承人不继承",
     "醉酒驾驶机动车的由公安机关吊销机动车驾驶证"),
    ("房屋买卖合同纠纷",
     "不动产物权的设立变更转让和消灭经依法登记发生效力未经登记不发生效力",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑"),
    ("工伤怎么认定",
     "职工在工作时间和工作场所内因工作原因受到事故伤害的应当认定为工伤",
     "离婚时夫妻共同财产由双方协议处理"),
    ("网络诈骗怎么报案",
     "利用电信网络技术手段实施诈骗公私财物价值三千元以上的应予立案追诉",
     "承揽人应当以自己的设备技术和劳力完成主要工作"),
    ("拖欠工资怎么办",
     "用人单位应当按照劳动合同约定和国家规定及时足额支付劳动者劳动报酬逾期不支付的应当加付赔偿金",
     "当事人对合同条款的理解有争议的应当按照合同所使用的词句"),
    ("邻居噪音扰民怎么办",
     "不动产的相邻权利人应当按照有利生产方便生活团结互助公平合理的原则处理相邻关系",
     "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金"),
    ("孩子抚养权怎么判",
     "离婚后不满两周岁的子女以由母亲直接抚养为原则已满两周岁的父母双方协议不成的由人民法院判决",
     "故意伤害他人身体的处三年以下有期徒刑拘役或者管制"),
    ("担保人要承担什么责任",
     "保证人与债权人未约定保证期间的债权人有权自主债务履行期限届满之日起六个月内要求保证人承担保证责任",
     "婚姻关系存续期间所得的工资奖金劳务报酬为夫妻共同财产"),
    ("高空抛物砸伤人谁负责",
     "从建筑物中抛掷物品或者从建筑物上坠落的物品造成他人损害的由侵权人依法承担侵权责任",
     "租赁期限届满承租人应当返还租赁物出租人应当退还押金"),
    ("快递丢了怎么赔",
     "承运人对运输过程中货物的毁损灭失承担赔偿责任但是承运人证明货物的毁损灭失是因不可抗力的除外",
     "经营者提供商品或者服务有欺诈行为的应当按照消费者的要求增加赔偿"),
    ("老人赡养义务",
     "成年子女对父母负有赡养扶助和保护的义务成年子女不履行赡养义务的缺乏劳动能力或者生活困难的父母有要求成年子女给付赡养费的权利",
     "用人单位违法解除劳动合同的应当按照经济补偿标准的二倍向劳动者支付赔偿金"),
    ("公司股东权益",
     "股东按照实缴的出资比例分取红利公司新增资本时股东有权优先按照实缴的出资比例认缴出资",
     "故意杀人的处死刑无期徒刑或者十年以上有期徒刑"),
    ("个人信息泄露怎么维权",
     "处理个人信息应当遵循合法正当必要原则不得过度收集个人信息自然人的个人信息受法律保护",
     "盗窃公私财物数额较大的处三年以下有期徒刑"),
    ("民间借贷利率上限",
     "借贷双方约定的利率超过合同成立时一年期贷款市场报价利率四倍的超过部分人民法院不予支持",
     "醉酒驾驶机动车的由公安机关吊销机动车驾驶证"),
    ("物业费不交会怎样",
     "业主应当按照约定向物业服务人支付物业费物业服务人已经按照约定提供服务的业主不得以未接受或者无需接受为由拒绝支付物业费",
     "承揽人应当以自己的设备技术和劳力完成主要工作"),
    ("商标侵权怎么处理",
     "未经商标注册人的许可在同一种商品上使用与其注册商标相同的商标的构成侵犯注册商标专用权",
     "当事人对合同条款的理解有争议的应当按照合同所使用的词句"),
    ("酒后打人怎么判",
     "醉酒的人犯罪应当负刑事责任故意伤害他人身体的处三年以下有期徒刑拘役或者管制",
     "离婚时夫妻共同财产由双方协议处理协议不成的由人民法院判决"),
    ("二手车买到事故车",
     "出卖人交付的标的物不符合质量要求的买受人可以依照本法的规定要求承担违约责任",
     "诈骗公私财物数额较大的处三年以下有期徒刑拘役或者管制并处或者单处罚金"),
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
    query_ms: f64,
}

#[derive(Serialize)]
struct CondResult {
    name: String,
    accuracy: f64,
    avg_delta: f32,
    n_pairs: usize,
    pairs: Vec<PairResult>,
    wall_ms: f64,
    avg_query_ms: f64,
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

fn run_pair(idx: usize, q: &str, m: &str, mm: &str, corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> PairResult {
    let seed = seed_off + idx as u64;
    let t0 = Instant::now();
    let (u_q, s_q) = process_text(q, seed, corpus, use_m2);
    let query_ms = t0.elapsed().as_secs_f64() * 1000.0;
    let (u_m, s_m) = process_text(m, seed + 100, corpus, use_m2);
    let (u_mm, s_mm) = process_text(mm, seed + 200, corpus, use_m2);
    let e_m = fuse_and_score(&u_q, &u_m, &s_q, &s_m);
    let e_mm = fuse_and_score(&u_q, &u_mm, &s_q, &s_mm);
    let correct = e_m < e_mm;
    let delta = if e_mm != 0.0 { (e_mm - e_m) / e_mm.abs() * 100.0 } else { 0.0 };
    PairResult {
        query: q.chars().take(10).collect(),
        e_match: e_m, e_mismatch: e_mm, correct, delta, query_ms,
    }
}

fn run_condition(name: &str, pairs: &[(&str, &str, &str)], corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> CondResult {
    let t0 = Instant::now();
    let results: Vec<PairResult> = pairs.par_iter().enumerate()
        .map(|(i, &(q, m, mm))| run_pair(i, q, m, mm, corpus, use_m2, seed_off))
        .collect();
    let wall = t0.elapsed().as_secs_f64() * 1000.0;
    let correct = results.iter().filter(|p| p.correct).count();
    let acc = correct as f64 / results.len() as f64;
    let avg_d = results.iter().map(|p| p.delta).sum::<f32>() / results.len() as f32;
    let avg_q = results.iter().map(|p| p.query_ms).sum::<f64>() / results.len() as f64;
    eprintln!("  {}: acc={:.0}% avg_Δ={:.1}% wall={:.0}ms avg_q={:.1}ms ({} pairs)",
        name, acc * 100.0, avg_d, wall, avg_q, results.len());
    CondResult { name: name.to_string(), accuracy: acc, avg_delta: avg_d, n_pairs: results.len(), pairs: results, wall_ms: wall, avg_query_ms: avg_q }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Fast Engine v2 + Generalization");
    eprintln!("============================================================");
    let t0 = Instant::now();

    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  {} texts", corpus_texts.len());

    eprintln!("Precomputing source fields...");
    let tp = Instant::now();
    let corpus: Vec<Vec<f32>> = corpus_texts.par_iter().map(|t| build_source_f32(t)).collect();
    eprintln!("  Done in {:.1}ms", tp.elapsed().as_secs_f64() * 1000.0);

    // Benchmark
    {
        let mut eng = MaoFieldEngine::new();
        eng.init_u(999);
        eng.set_source(&build_source_f32("基准测试"));
        let tb = Instant::now();
        eng.evolve_steps(1000);
        let ms = tb.elapsed().as_secs_f64() * 1000.0;
        eprintln!("\nBenchmark: 1000 steps = {:.2}ms ({:.4}ms/step)", ms, ms / 1000.0);
        let tb2 = Instant::now();
        let steps = eng.evolve_adaptive(1000, 200, 1e-4);
        let ms2 = tb2.elapsed().as_secs_f64() * 1000.0;
        eprintln!("Adaptive 1000: {:.2}ms, {} steps actually run", ms2, steps);
    }

    let mut all = Vec::new();

    // === Phase 1: Original 10 pairs, 3 runs each ===
    eprintln!("\n--- Phase 1: Original 10 pairs (3 runs each) ---");
    for run in 1..=3u64 {
        all.push(run_condition(&format!("A_10p_r{}", run), TEST_PAIRS_10, &corpus, false, run * 1000));
        all.push(run_condition(&format!("B2_10p_r{}", run), TEST_PAIRS_10, &corpus, true, run * 1000));
    }

    // Summarize 10-pair results
    let a_accs: Vec<f64> = (0..3).map(|i| all[i * 2].accuracy).collect();
    let b2_accs: Vec<f64> = (0..3).map(|i| all[i * 2 + 1].accuracy).collect();
    let mean_a = a_accs.iter().sum::<f64>() / 3.0;
    let mean_b2 = b2_accs.iter().sum::<f64>() / 3.0;
    eprintln!("\n  10-pair summary:");
    eprintln!("    A  runs: [{}] mean={:.0}%", a_accs.iter().map(|a| format!("{:.0}%", a * 100.0)).collect::<Vec<_>>().join(", "), mean_a * 100.0);
    eprintln!("    B2 runs: [{}] mean={:.0}%", b2_accs.iter().map(|a| format!("{:.0}%", a * 100.0)).collect::<Vec<_>>().join(", "), mean_b2 * 100.0);

    // === Phase 2: 30 pairs (10 original + 20 extended) ===
    eprintln!("\n--- Phase 2: 30-pair generalization ---");
    let all_30: Vec<(&str, &str, &str)> = TEST_PAIRS_10.iter().chain(TEST_PAIRS_EXT.iter()).copied().collect();
    all.push(run_condition("A_30p", &all_30, &corpus, false, 5000));
    all.push(run_condition("B2_30p", &all_30, &corpus, true, 5000));

    let acc_a30 = all[all.len() - 2].accuracy;
    let acc_b2_30 = all[all.len() - 1].accuracy;

    let elapsed = t0.elapsed().as_secs_f64();

    // Final summary
    eprintln!("\n============================================================");
    eprintln!("  FINAL SUMMARY");
    eprintln!("------------------------------------------------------------");
    eprintln!("  10 pairs:  A mean={:.0}%  B2 mean={:.0}%  Δ={:+.0}pp", mean_a * 100.0, mean_b2 * 100.0, (mean_b2 - mean_a) * 100.0);
    eprintln!("  30 pairs:  A={:.0}%       B2={:.0}%       Δ={:+.0}pp", acc_a30 * 100.0, acc_b2_30 * 100.0, (acc_b2_30 - acc_a30) * 100.0);
    let all_query_ms: Vec<f64> = all.iter().flat_map(|c| c.pairs.iter()).map(|p| p.query_ms).collect();
    let avg_q = all_query_ms.iter().sum::<f64>() / all_query_ms.len() as f64;
    let max_q = all_query_ms.iter().copied().fold(0.0f64, f64::max);
    eprintln!("  Timing: avg_query={:.1}ms max={:.1}ms total={:.1}s", avg_q, max_q, elapsed);
    eprintln!("============================================================");

    // JSON
    let output = serde_json::json!({
        "meta": { "date": "2026-04-11", "experiment": "exp007_fast_v2_generalization", "engine": "f32_fused_adaptive" },
        "phase1_10pair": { "A_mean": mean_a, "B2_mean": mean_b2, "A_runs": a_accs, "B2_runs": b2_accs },
        "phase2_30pair": { "A": acc_a30, "B2": acc_b2_30 },
        "all_conditions": all,
        "timing": { "avg_query_ms": avg_q, "max_query_ms": max_q, "total_s": elapsed },
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp007_v2_results.json"), serde_json::to_string_pretty(&output).unwrap());

    let summary = format!(
        "MaoField Fast v2 + Generalization\n\n10-pair: A={:.0}% B2={:.0}% Δ={:+.0}pp\n30-pair: A={:.0}% B2={:.0}% Δ={:+.0}pp\nTiming: avg_q={:.1}ms total={:.1}s\n",
        mean_a * 100.0, mean_b2 * 100.0, (mean_b2 - mean_a) * 100.0,
        acc_a30 * 100.0, acc_b2_30 * 100.0, (acc_b2_30 - acc_a30) * 100.0,
        avg_q, elapsed
    );
    let _ = std::fs::write(results_dir.join("exp007_v2_summary.txt"), summary);
    eprintln!("\nSaved to {:?}", results_dir);
}
