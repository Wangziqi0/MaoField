mod field;
mod source;
mod adjoint;
mod experiment;
mod config;
mod numa;

use std::time::Instant;
use experiment::run_all_conditions;

fn main() {
    let t0 = Instant::now();
    numa::setup_threads();
    run_all_conditions();
    let elapsed = t0.elapsed().as_secs_f64();
    eprintln!("\nTotal time: {:.0}s ({:.1}min)", elapsed, elapsed / 60.0);
}
