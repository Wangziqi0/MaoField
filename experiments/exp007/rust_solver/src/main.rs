mod field;
mod source;
mod adjoint;
mod experiment;

use std::time::Instant;

/// 70% of 256 hw threads
const TARGET_THREADS: usize = 179;

fn main() {
    rayon::ThreadPoolBuilder::new()
        .num_threads(TARGET_THREADS)
        .build_global()
        .expect("Failed to build rayon thread pool");
    eprintln!("Rayon pool: {} threads", TARGET_THREADS);

    let t0 = Instant::now();
    experiment::run_all();
    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\nTotal time: {:.0}s ({:.1}min)", elapsed, elapsed / 60.0);
}
