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

// ===== Type 1: Literal similar + Semantically related (control) =====
const TYPE1: &[(&str, &str, &str)] = &[
    ("故意伤害怎么判", "故意伤害他人身体的处三年以下有期徒刑", "用人单位应当支付劳动报酬"),
    ("盗窃怎么处罚", "盗窃公私财物数额较大的处三年以下有期徒刑", "婚姻关系存续期间的财产为共同财产"),
    ("醉驾怎么罚", "醉酒驾驶机动车的吊销驾驶证", "承揽人应当以自己的设备完成工作"),
    ("杀人判多少年", "故意杀人的处死刑无期徒刑或十年以上", "合同条款有争议按合同词句理解"),
    ("诈骗判几年", "诈骗公私财物数额较大处三年以下有期徒刑", "工资奖金为夫妻共同财产"),
    ("离婚财产怎么分", "离婚时共同财产由双方协议处理", "故意伤害他人身体处三年以下"),
    ("借钱不还怎么办", "借款人应当按期限返还借款", "盗窃公私财物处三年以下"),
    ("房东不退押金", "租赁期满出租人应退还押金", "醉酒驾驶吊销驾驶证"),
    ("假货怎么维权", "欺诈行为应按消费者要求增加赔偿", "故意杀人处死刑无期徒刑"),
    ("被辞退怎么赔", "违法解除劳动合同按二倍支付赔偿金", "共同财产由双方协议处理"),
];

// ===== Type 2: Literal different + Semantically related (CORE TEST) =====
const TYPE2: &[(&str, &str, &str)] = &[
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

// ===== Type 3: Literal similar + Semantically unrelated (distractor test) =====
const TYPE3: &[(&str, &str, &str)] = &[
    ("故意伤害怎么判", "蓄意对他人身体实施暴力行为的刑事责任", "伤害的近义词是损害打击创伤"),
    ("盗窃罪判多久", "秘密窃取公私财物价值较大的刑罚标准", "盗窃之王是一部法国喜剧电影"),
    ("合同违约怎么赔", "一方不履行协议义务给对方造成损失应予补偿", "合同工与正式工的区别是什么"),
    ("酒驾的处罚标准", "血液中乙醇含量超标驾车的行政与刑事制裁规定", "各类酒驾现象的社会学分析报告"),
    ("遗产怎么继承", "被继承人死亡后其合法财产按法定顺序由亲属取得", "继承者们是一部韩国电视剧"),
    ("劳动合同到期", "用工协议届满后双方权利义务的终止与续签规定", "到期国债收益率曲线分析方法"),
    ("抚养权归谁", "父母离异后未成年子女由哪方直接照顾生活", "抚养比是指非劳动年龄人口占比"),
    ("交通事故责任", "机动车碰撞造成人身财产损害的过错认定与赔偿", "交通事故频发路段的地理特征研究"),
    ("网络诈骗怎么报案", "利用信息网络实施欺诈犯罪的被害人向公安机关控告的程序", "网络诈骗案例分析与防范意识培养讲座"),
    ("商标侵权赔偿", "未经许可使用他人注册标识造成混淆的应承担损害赔偿", "商标设计的基本原则与经典案例赏析"),
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
    pair_type: String,
    query: String,
    e_match: f32,
    e_mismatch: f32,
    correct: bool,
    delta: f32,
}

#[derive(Serialize)]
struct TypeResult {
    type_name: String,
    accuracy: f64,
    avg_delta: f32,
    n_pairs: usize,
}

#[derive(Serialize)]
struct RunResult {
    run: usize,
    seed_offset: u64,
    types: Vec<TypeResult>,
    overall_accuracy: f64,
    pairs: Vec<PairResult>,
}

#[derive(Serialize)]
struct CondResult {
    name: String,
    use_m2: bool,
    runs: Vec<RunResult>,
    mean_type1: f64,
    mean_type2: f64,
    mean_type3: f64,
    mean_overall: f64,
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

fn run_pair(idx: usize, ptype: &str, q: &str, m: &str, mm: &str,
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
        pair_type: ptype.to_string(),
        query: q.chars().take(12).collect(),
        e_match: e_m, e_mismatch: e_mm, correct, delta,
    }
}

fn run_one_pass(corpus: &[Vec<f32>], use_m2: bool, seed_off: u64) -> Vec<PairResult> {
    // Build all 30 pairs with type labels
    let all_pairs: Vec<(usize, &str, &str, &str, &str)> = TYPE1.iter().enumerate()
        .map(|(i, &(q, m, mm))| (i, "T1_literal+semantic", q, m, mm))
        .chain(TYPE2.iter().enumerate()
            .map(|(i, &(q, m, mm))| (i + 10, "T2_diff_literal+semantic", q, m, mm)))
        .chain(TYPE3.iter().enumerate()
            .map(|(i, &(q, m, mm))| (i + 20, "T3_similar_literal+unrelated", q, m, mm)))
        .collect();

    all_pairs.par_iter()
        .map(|&(idx, ptype, q, m, mm)| run_pair(idx, ptype, q, m, mm, corpus, use_m2, seed_off))
        .collect()
}

fn compute_type_stats(pairs: &[PairResult], type_prefix: &str) -> TypeResult {
    let typed: Vec<&PairResult> = pairs.iter().filter(|p| p.pair_type.starts_with(type_prefix)).collect();
    let correct = typed.iter().filter(|p| p.correct).count();
    let acc = if typed.is_empty() { 0.0 } else { correct as f64 / typed.len() as f64 };
    let avg_d = if typed.is_empty() { 0.0 } else {
        typed.iter().map(|p| p.delta).sum::<f32>() / typed.len() as f32
    };
    TypeResult {
        type_name: type_prefix.to_string(),
        accuracy: acc,
        avg_delta: avg_d,
        n_pairs: typed.len(),
    }
}

fn run_condition(name: &str, corpus: &[Vec<f32>], use_m2: bool) -> CondResult {
    let mut runs = Vec::new();
    let mut type1_accs = Vec::new();
    let mut type2_accs = Vec::new();
    let mut type3_accs = Vec::new();

    for run in 0..N_RUNS {
        let seed_off = (run as u64 + 1) * 1000;
        let t0 = Instant::now();
        let pairs = run_one_pass(corpus, use_m2, seed_off);
        let wall = t0.elapsed().as_secs_f64();

        let t1 = compute_type_stats(&pairs, "T1");
        let t2 = compute_type_stats(&pairs, "T2");
        let t3 = compute_type_stats(&pairs, "T3");

        let overall = pairs.iter().filter(|p| p.correct).count() as f64 / pairs.len() as f64;

        eprintln!("  {} run {}: T1={:.0}% T2={:.0}% T3={:.0}% overall={:.0}% ({:.1}s)",
            name, run + 1, t1.accuracy * 100.0, t2.accuracy * 100.0, t3.accuracy * 100.0, overall * 100.0, wall);

        type1_accs.push(t1.accuracy);
        type2_accs.push(t2.accuracy);
        type3_accs.push(t3.accuracy);

        runs.push(RunResult {
            run: run + 1,
            seed_offset: seed_off,
            types: vec![t1, t2, t3],
            overall_accuracy: overall,
            pairs,
        });
    }

    let mean = |v: &[f64]| v.iter().sum::<f64>() / v.len() as f64;

    CondResult {
        name: name.to_string(),
        use_m2,
        runs,
        mean_type1: mean(&type1_accs),
        mean_type2: mean(&type2_accs),
        mean_type3: mean(&type3_accs),
        mean_overall: mean(&[mean(&type1_accs), mean(&type2_accs), mean(&type3_accs)]),
    }
}

fn main() {
    rayon::ThreadPoolBuilder::new().num_threads(179).build_global().unwrap();

    eprintln!("============================================================");
    eprintln!("MaoField Exp008: Semantic vs Bit-Pattern — Decisive Test");
    eprintln!("============================================================");
    let t0 = Instant::now();

    eprintln!("\nLoading corpus...");
    let corpus_texts = load_corpus();
    eprintln!("  {} texts", corpus_texts.len());

    eprintln!("Precomputing source fields...");
    let tp = Instant::now();
    let corpus: Vec<Vec<f32>> = corpus_texts.par_iter().map(|t| build_source_f32(t)).collect();
    eprintln!("  Done in {:.0}ms", tp.elapsed().as_secs_f64() * 1000.0);

    let mut results = Vec::new();

    eprintln!("\n--- Condition A: Fixed S (baseline) ---");
    results.push(run_condition("A_fixed", &corpus, false));

    eprintln!("\n--- Condition B2: M2 S·u* ---");
    results.push(run_condition("B2_m2", &corpus, true));

    let elapsed = t0.elapsed().as_secs_f64();

    // Final summary
    eprintln!("\n============================================================");
    eprintln!("  DECISIVE RESULTS");
    eprintln!("------------------------------------------------------------");
    eprintln!("  {:12} {:>8} {:>8} {:>8}", "", "T1:lit+sem", "T2:CORE", "T3:trap");
    for r in &results {
        eprintln!("  {:12} {:>7.0}% {:>7.0}% {:>7.0}%",
            r.name, r.mean_type1 * 100.0, r.mean_type2 * 100.0, r.mean_type3 * 100.0);
    }

    let a = &results[0];
    let b = &results[1];
    eprintln!("\n  Key verdicts:");
    if a.mean_type2 > 0.6 || b.mean_type2 > 0.6 {
        eprintln!("    ★ Type 2 > 60%: FRAMEWORK CAPTURES SEMANTICS");
    } else if a.mean_type2 > 0.5 || b.mean_type2 > 0.5 {
        eprintln!("    ~ Type 2 ≈ 50-60%: Weak signal, inconclusive");
    } else {
        eprintln!("    ✗ Type 2 ≤ 50%: BIT PATTERN MATCHING ONLY");
    }

    if b.mean_type3 > a.mean_type3 {
        eprintln!("    M2 anti-distraction: B2 T3 ({:.0}%) > A T3 ({:.0}%)", b.mean_type3 * 100.0, a.mean_type3 * 100.0);
    } else {
        eprintln!("    M2 no anti-distraction: B2 T3 ({:.0}%) ≤ A T3 ({:.0}%)", b.mean_type3 * 100.0, a.mean_type3 * 100.0);
    }

    eprintln!("  Total time: {:.1}s", elapsed);
    eprintln!("============================================================");

    // JSON
    let output = serde_json::json!({
        "meta": {
            "date": "2026-04-11",
            "experiment": "exp008_semantic_vs_bitpattern",
            "engine": "f32_fused_adaptive",
            "n_runs": N_RUNS,
        },
        "conditions": results,
        "summary": {
            "A_type1": a.mean_type1, "A_type2": a.mean_type2, "A_type3": a.mean_type3,
            "B2_type1": b.mean_type1, "B2_type2": b.mean_type2, "B2_type3": b.mean_type3,
        },
        "total_time_s": elapsed,
    });
    println!("{}", serde_json::to_string_pretty(&output).unwrap());

    let results_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).parent().unwrap().join("results");
    let _ = std::fs::create_dir_all(&results_dir);
    let _ = std::fs::write(results_dir.join("exp008_results.json"), serde_json::to_string_pretty(&output).unwrap());

    let summary = format!(
        "Exp008: Semantic vs Bit-Pattern\n\n{:12} {:>8} {:>8} {:>8}\n{:12} {:>7.0}% {:>7.0}% {:>7.0}%\n{:12} {:>7.0}% {:>7.0}% {:>7.0}%\n\nTotal: {:.1}s\n",
        "", "T1", "T2:CORE", "T3:trap",
        a.name, a.mean_type1 * 100.0, a.mean_type2 * 100.0, a.mean_type3 * 100.0,
        b.name, b.mean_type1 * 100.0, b.mean_type2 * 100.0, b.mean_type3 * 100.0,
        elapsed
    );
    let _ = std::fs::write(results_dir.join("exp008_summary.txt"), summary);
    eprintln!("Saved to {:?}", results_dir);
}
