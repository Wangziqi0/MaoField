/// Grid size (32^3)
pub const GRID: usize = 32;
pub const NCELLS: usize = GRID * GRID * GRID;

/// Allen-Cahn parameters
pub const D_COEFF: f64 = 0.1;
pub const DT: f64 = 0.1;
pub const DX: f64 = 1.0;

/// Evolution steps
pub const INIT_STEPS: usize = 1000;
pub const INTERACT_STEPS: usize = 300;
pub const RELAX_STEPS: usize = 100;
pub const FUSION_STEPS: usize = 2000;

/// Adjoint iteration
pub const MAX_ROUNDS: usize = 5;
pub const CONVERGENCE_TOL: f64 = 0.01;
pub const TOP_K: usize = 10;

/// Corpus
pub const CORPUS_SIZE: usize = 200;

/// Database path
pub const DB_PATH: &str =
    "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db";

/// 70% of 256 hw threads
pub const TARGET_THREADS: usize = 179;

/// Gaussian smoothing sigma
pub const SIGMA: f64 = 1.0;
