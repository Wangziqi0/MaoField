use crate::config::TARGET_THREADS;

/// Configure rayon thread pool to use ~70% of cores.
/// On Zen3 NPS4 EPYC with 8 NUMA nodes, we spread threads across all nodes.
pub fn setup_threads() {
    rayon::ThreadPoolBuilder::new()
        .num_threads(TARGET_THREADS)
        .build_global()
        .expect("Failed to build rayon thread pool");
    eprintln!("Rayon pool: {} threads (70% of 256)", TARGET_THREADS);
}
