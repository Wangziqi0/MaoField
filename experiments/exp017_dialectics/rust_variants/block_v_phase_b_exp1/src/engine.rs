//! Phase B Exp 1 engine: open dissipative complex scalar field ψ ∈ ℂ with
//! b+c bidirectional self-feedback source + exponential-weighted history.
//!
//! EOM (per Win taskbook §1.4):
//!   γ ∂_t ψ = D ∇²ψ − ∂V/∂ψ* + S(x, t)
//!   V(ψ) = (|ψ|² − v²)²     (Mexican hat, v = 1 default → U(1) Goldstone softmode)
//!   ∂V/∂ψ* = 2(|ψ|² − v²) · ψ
//!
//! Source (§1.2):
//!   S(x, t) = S₀(x) + α · (ψ(x, t) − ⟨ψ⟩_x) + β · δS_history(x, t)
//!   δS_history(x, t) = Σ_{k=0}^{N-1} w_k · (ψ(x, t − k Δt) − ⟨ψ⟩_{x, t − k Δt})
//!   w_k = exp(−λ · k · Δt)
//!
//! Real + imaginary parts are evolved separately (a = Re ψ, b = Im ψ).
//! All fields are periodic BC on a G³ cubic lattice, dx = 1.
//!
//! The engine does NOT internally drive the multi-scale loop — that is main.rs's
//! responsibility. This module provides:
//!   - inner step (one ψ update at dt_inner, with current source)
//!   - spatial mean of ψ
//!   - push current (ψ − ⟨ψ⟩) to the exponential-weighted history buffer
//!   - recompute effective source from (S₀, current ψ, history)
//!   - spatial block-average of source (middle loop coarse-graining)
//!   - entropy production rate observable (O2)
//!   - snapshot extract (for O1 FFT / O3 RG downstream)

pub const G: usize = 32;
pub const N: usize = G * G * G;

/// Build periodic nearest-neighbor index table (±x, ±y, ±z).
pub fn build_nb() -> Vec<[usize; 6]> {
    let mut t = vec![[0usize; 6]; N];
    for z in 0..G {
        for y in 0..G {
            for x in 0..G {
                let k = x + y * G + z * G * G;
                let xm = if x == 0 { G - 1 } else { x - 1 };
                let xp = if x == G - 1 { 0 } else { x + 1 };
                let ym = if y == 0 { G - 1 } else { y - 1 };
                let yp = if y == G - 1 { 0 } else { y + 1 };
                let zm = if z == 0 { G - 1 } else { z - 1 };
                let zp = if z == G - 1 { 0 } else { z + 1 };
                t[k] = [
                    xm + y * G + z * G * G,
                    xp + y * G + z * G * G,
                    x + ym * G + z * G * G,
                    x + yp * G + z * G * G,
                    x + y * G + zm * G * G,
                    x + y * G + zp * G * G,
                ];
            }
        }
    }
    t
}

/// Xorshift64* RNG (deterministic seed).
#[inline]
fn xorshift(state: &mut u64) -> u64 {
    *state ^= *state << 13;
    *state ^= *state >> 7;
    *state ^= *state << 17;
    *state
}

#[inline]
fn rand_unit(state: &mut u64) -> f32 {
    (xorshift(state) as f32 / u64::MAX as f32) * 2.0 - 1.0
}

/// Engine parameters — passed explicitly, not hidden as statics, so null/control
/// modes can disable feedback by setting α=0 / β=0 / single-scale.
pub struct EngineParams {
    pub d: f32,           // diffusion D
    pub v_min: f32,       // Mexican hat radius v  (V = (|ψ|² − v²)²)
    pub alpha: f32,       // instantaneous feedback strength
    pub beta: f32,        // history-cumulative feedback strength
    pub lambda_hist: f32, // history exp-decay rate in time units
    pub n_hist: usize,    // history window length in inner steps
    pub clamp_abs: f32,   // safety clamp on |a|, |b| to avoid runaway
}

impl EngineParams {
    pub fn default_exp() -> Self {
        Self {
            d: 0.1,
            v_min: 1.0,
            alpha: 0.1,
            beta: 0.05,
            lambda_hist: 0.05,
            n_hist: 100,
            clamp_abs: 3.0,
        }
    }

    pub fn null_test() -> Self {
        // α=0, β=0 → feedback terms vanish → static source only.
        let mut p = Self::default_exp();
        p.alpha = 0.0;
        p.beta = 0.0;
        p
    }

    pub fn control_const_source() -> Self {
        // Same as null: S = S₀ const, no feedback.
        Self::null_test()
    }
}

/// Ring buffer of (Δa, Δb) = (a − ⟨a⟩, b − ⟨b⟩) snapshots.
/// Storage: cap snapshots × N voxels × 2 f32.
/// Memory per engine with cap=100, N=32³ = 26 MB.
pub struct HistoryBuffer {
    pub cap: usize,
    pub len: usize,    // current valid length (≤ cap)
    pub head: usize,   // next slot to write
    pub da: Vec<Vec<f32>>,
    pub db: Vec<Vec<f32>>,
}

impl HistoryBuffer {
    pub fn new(cap: usize) -> Self {
        Self {
            cap,
            len: 0,
            head: 0,
            da: (0..cap).map(|_| vec![0.0f32; N]).collect(),
            db: (0..cap).map(|_| vec![0.0f32; N]).collect(),
        }
    }

    /// Push a fresh snapshot. Returns nothing (caller fills slot via closure-free
    /// direct mutation is cleaner with this shape).
    pub fn push(&mut self, new_da: &[f32], new_db: &[f32]) {
        let s = self.head;
        self.da[s].copy_from_slice(new_da);
        self.db[s].copy_from_slice(new_db);
        self.head = (self.head + 1) % self.cap;
        if self.len < self.cap {
            self.len += 1;
        }
    }

    /// Compute exponential-weighted integral over history (literal Win taskbook
    /// §1.2 formulation — NO normalization):
    ///   δS(x) = Σ_{k=0}^{len-1} w_k · snapshot[k] · Δt_outer
    ///   w_k = exp(−λ·k·Δt_outer)
    /// k = 0 is the MOST RECENT snapshot; larger k is older.
    /// Caller passes `kernel_step = λ·Δt_outer` (the per-k kernel decrement) and
    /// `dt_outer` (the integration measure). With λ=0.05, Δt_outer=1.0:
    /// kernel_step = 0.05, dt_outer = 1.0; saturated Σ w_k ≈ 20.4 over 100 slots.
    pub fn weighted_sum_into(
        &self,
        kernel_step: f32,
        dt_outer: f32,
        out_a: &mut [f32],
        out_b: &mut [f32],
    ) {
        out_a.iter_mut().for_each(|v| *v = 0.0);
        out_b.iter_mut().for_each(|v| *v = 0.0);
        if self.len == 0 {
            return;
        }
        // walk from most recent backwards
        for k in 0..self.len {
            let idx = (self.head + self.cap - 1 - k) % self.cap;
            let w = (-kernel_step * k as f32).exp() * dt_outer;
            let da = &self.da[idx];
            let db = &self.db[idx];
            for i in 0..N {
                out_a[i] += w * da[i];
                out_b[i] += w * db[i];
            }
        }
    }
}

/// Phase B Exp 1 ψ-field engine.
pub struct Engine {
    pub a: Vec<f32>,
    pub b: Vec<f32>,
    pub a_new: Vec<f32>,
    pub b_new: Vec<f32>,
    pub s0a: Vec<f32>, // static base source (real)
    pub s0b: Vec<f32>, // static base source (imag)
    pub sa: Vec<f32>,  // effective source real (= S₀ + α·Δψ + β·δS_history)
    pub sb: Vec<f32>,  // effective source imag
    pub nb: Vec<[usize; 6]>,
    pub hist: HistoryBuffer,
    pub params: EngineParams,
    // scratch buffers for delta_s_history and (a-<a>, b-<b>)
    pub scratch_da: Vec<f32>,
    pub scratch_db: Vec<f32>,
    pub scratch_ds_a: Vec<f32>,
    pub scratch_ds_b: Vec<f32>,
    pub time: f32,
}

impl Engine {
    pub fn new(params: EngineParams) -> Self {
        let cap = params.n_hist.max(1);
        Self {
            a: vec![0.0; N],
            b: vec![0.0; N],
            a_new: vec![0.0; N],
            b_new: vec![0.0; N],
            s0a: vec![0.0; N],
            s0b: vec![0.0; N],
            sa: vec![0.0; N],
            sb: vec![0.0; N],
            nb: build_nb(),
            hist: HistoryBuffer::new(cap),
            params,
            scratch_da: vec![0.0; N],
            scratch_db: vec![0.0; N],
            scratch_ds_a: vec![0.0; N],
            scratch_ds_b: vec![0.0; N],
            time: 0.0,
        }
    }

    /// Init ψ randomly in a small shell around |ψ| ≈ v
    /// (so we sit near the Mexican hat minimum, not at the saddle at 0).
    pub fn init_psi_near_minimum(&mut self, seed: u64) {
        let mut rng = seed | 1;
        let v = self.params.v_min;
        for k in 0..N {
            let theta = rand_unit(&mut rng) * std::f32::consts::PI;
            let r = v + 0.1 * rand_unit(&mut rng);
            self.a[k] = r * theta.cos();
            self.b[k] = r * theta.sin();
        }
    }

    pub fn set_base_source(&mut self, s0a: &[f32], s0b: &[f32]) {
        self.s0a.copy_from_slice(s0a);
        self.s0b.copy_from_slice(s0b);
        self.sa.copy_from_slice(s0a);
        self.sb.copy_from_slice(s0b);
    }

    /// Recompute effective source: S = S₀ + α·(ψ − ⟨ψ⟩) + β·δS_history
    /// Also refreshes scratch_da = ψ − ⟨ψ⟩ (needed by caller for history push).
    /// `dt_outer` = time between successive history pushes (defaults 1.0 in Win
    /// taskbook: outer tick every 100 inner × dt_inner 0.01).
    pub fn recompute_effective_source(&mut self, dt_outer: f32) {
        // 1) spatial mean of ψ
        let mut ma: f32 = 0.0;
        let mut mb: f32 = 0.0;
        for k in 0..N {
            ma += self.a[k];
            mb += self.b[k];
        }
        ma /= N as f32;
        mb /= N as f32;
        // 2) Δψ = ψ − ⟨ψ⟩
        for k in 0..N {
            self.scratch_da[k] = self.a[k] - ma;
            self.scratch_db[k] = self.b[k] - mb;
        }
        // 3) δS_history (exp-weighted integral over history buffer, per taskbook §1.2)
        let kernel_step = self.params.lambda_hist * dt_outer;
        self.hist.weighted_sum_into(
            kernel_step,
            dt_outer,
            &mut self.scratch_ds_a,
            &mut self.scratch_ds_b,
        );
        // 4) effective S
        let a_coef = self.params.alpha;
        let b_coef = self.params.beta;
        for k in 0..N {
            self.sa[k] = self.s0a[k] + a_coef * self.scratch_da[k] + b_coef * self.scratch_ds_a[k];
            self.sb[k] = self.s0b[k] + a_coef * self.scratch_db[k] + b_coef * self.scratch_ds_b[k];
        }
    }

    /// Push current (ψ − ⟨ψ⟩) into history (scratch_da/db must be up-to-date).
    pub fn push_history(&mut self) {
        self.hist.push(&self.scratch_da, &self.scratch_db);
    }

    /// Spatial block-average of source fields with block_size (cubic blocks).
    /// Replaces sa, sb with block-piecewise-constant versions.
    /// This is the middle-layer "renormalize S coarse structure" step.
    pub fn block_average_source(&mut self, block: usize) {
        if block <= 1 {
            return;
        }
        // number of blocks per side
        let nb = G / block;
        let mut acc_a = vec![0.0f32; nb * nb * nb];
        let mut acc_b = vec![0.0f32; nb * nb * nb];
        let inv = 1.0 / (block * block * block) as f32;
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    let bi = (x / block) + (y / block) * nb + (z / block) * nb * nb;
                    acc_a[bi] += self.sa[k];
                    acc_b[bi] += self.sb[k];
                }
            }
        }
        for v in acc_a.iter_mut() {
            *v *= inv;
        }
        for v in acc_b.iter_mut() {
            *v *= inv;
        }
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    let bi = (x / block) + (y / block) * nb + (z / block) * nb * nb;
                    self.sa[k] = acc_a[bi];
                    self.sb[k] = acc_b[bi];
                }
            }
        }
    }

    /// One explicit-Euler inner step at dt using the CURRENT effective source.
    /// EOM:  ∂a/∂t = D∇²a − 2a(|ψ|² − v²) + S_a    (γ = 1)
    ///       ∂b/∂t = D∇²b − 2b(|ψ|² − v²) + S_b
    #[inline(never)]
    pub fn evolve_inner_step(&mut self, dt: f32) {
        let tab = &self.nb;
        let d = self.params.d;
        let v2 = self.params.v_min * self.params.v_min;
        let clamp = self.params.clamp_abs;
        let a = &self.a;
        let b = &self.b;
        let sa = &self.sa;
        let sb = &self.sb;
        let a_new = &mut self.a_new;
        let b_new = &mut self.b_new;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ak = unsafe { *a.get_unchecked(k) };
            let bk = unsafe { *b.get_unchecked(k) };
            let sak = unsafe { *sa.get_unchecked(k) };
            let sbk = unsafe { *sb.get_unchecked(k) };
            let lap_a = unsafe {
                *a.get_unchecked(nb[0])
                    + *a.get_unchecked(nb[1])
                    + *a.get_unchecked(nb[2])
                    + *a.get_unchecked(nb[3])
                    + *a.get_unchecked(nb[4])
                    + *a.get_unchecked(nb[5])
                    - 6.0 * ak
            };
            let lap_b = unsafe {
                *b.get_unchecked(nb[0])
                    + *b.get_unchecked(nb[1])
                    + *b.get_unchecked(nb[2])
                    + *b.get_unchecked(nb[3])
                    + *b.get_unchecked(nb[4])
                    + *b.get_unchecked(nb[5])
                    - 6.0 * bk
            };
            let mod2 = ak * ak + bk * bk;
            let drive_coef = 2.0 * (mod2 - v2); // ∂V/∂ψ* prefactor (= 2(|ψ|²−v²))
            let da = d * lap_a - drive_coef * ak + sak;
            let db = d * lap_b - drive_coef * bk + sbk;
            unsafe {
                *a_new.get_unchecked_mut(k) = (ak + dt * da).clamp(-clamp, clamp);
                *b_new.get_unchecked_mut(k) = (bk + dt * db).clamp(-clamp, clamp);
            }
        }
        std::mem::swap(&mut self.a, &mut self.a_new);
        std::mem::swap(&mut self.b, &mut self.b_new);
        self.time += dt;
    }

    // ========== Observables ==========

    /// Spatial mean |ψ|² (used as overall amplitude tracker).
    pub fn mean_mod2(&self) -> f32 {
        let mut s = 0.0f32;
        for k in 0..N {
            s += self.a[k] * self.a[k] + self.b[k] * self.b[k];
        }
        s / N as f32
    }

    /// Spatial std of |ψ|² (tracks inhomogeneity / localized structure formation).
    pub fn std_mod2(&self) -> f32 {
        let mean = self.mean_mod2();
        let mut v = 0.0f32;
        for k in 0..N {
            let m2 = self.a[k] * self.a[k] + self.b[k] * self.b[k];
            let d = m2 - mean;
            v += d * d;
        }
        (v / N as f32).sqrt()
    }

    /// Complex spatial mean ⟨ψ⟩.
    pub fn mean_psi(&self) -> (f32, f32) {
        let mut ma: f32 = 0.0;
        let mut mb: f32 = 0.0;
        for k in 0..N {
            ma += self.a[k];
            mb += self.b[k];
        }
        (ma / N as f32, mb / N as f32)
    }

    /// Source L2 norm (monitor whether S blows up under feedback).
    pub fn source_l2(&self) -> f32 {
        let mut s = 0.0f32;
        for k in 0..N {
            s += self.sa[k] * self.sa[k] + self.sb[k] * self.sb[k];
        }
        (s / N as f32).sqrt()
    }

    /// Entropy production rate (O2).
    /// For an overdamped system ∂_t ψ = −∂V/∂ψ* + S + diffusion + noise,
    /// the deterministic dissipation rate is:
    ///   dS_diss/dt = ∫ |∂_t ψ|² dx     [gradient-flow + source]
    /// (this collapses to the free-energy descent rate in the noise-free limit).
    /// Since noise=0 here, we compute:
    ///   dS/dt ≈ (1/N) · Σ_k (|ψ(k, t+dt) − ψ(k, t)|² / dt²)
    /// using the most recent inner step (a/b vs a_new/b_new are already swapped,
    /// so we reconstruct from the increment that was applied).
    /// For efficiency, we re-evaluate the RHS |deterministic_rhs|² at current state
    /// (which is what dψ/dt² would be for an infinitesimal next step).
    pub fn entropy_production_rate(&self) -> f32 {
        let tab = &self.nb;
        let d = self.params.d;
        let v2 = self.params.v_min * self.params.v_min;
        let mut acc = 0.0f32;
        for k in 0..N {
            let nb = tab[k];
            let ak = self.a[k];
            let bk = self.b[k];
            let lap_a = self.a[nb[0]] + self.a[nb[1]] + self.a[nb[2]]
                + self.a[nb[3]] + self.a[nb[4]] + self.a[nb[5]]
                - 6.0 * ak;
            let lap_b = self.b[nb[0]] + self.b[nb[1]] + self.b[nb[2]]
                + self.b[nb[3]] + self.b[nb[4]] + self.b[nb[5]]
                - 6.0 * bk;
            let mod2 = ak * ak + bk * bk;
            let drive = 2.0 * (mod2 - v2);
            let ra = d * lap_a - drive * ak + self.sa[k];
            let rb = d * lap_b - drive * bk + self.sb[k];
            acc += ra * ra + rb * rb;
        }
        acc / N as f32
    }

    /// Total free energy E = ∫ [D/2(|∇a|²+|∇b|²) + (|ψ|² − v²)² − (a·Sa + b·Sb)] dx
    /// (using the taskbook convention V = (|ψ|²−v²)², no 1/4 factor.)
    pub fn free_energy(&self) -> f32 {
        let tab = &self.nb;
        let d = self.params.d;
        let v2 = self.params.v_min * self.params.v_min;
        let mut total = 0.0f32;
        for k in 0..N {
            let nb = tab[k];
            let ak = self.a[k];
            let bk = self.b[k];
            let gax = self.a[nb[1]] - ak;
            let gay = self.a[nb[3]] - ak;
            let gaz = self.a[nb[5]] - ak;
            let gbx = self.b[nb[1]] - bk;
            let gby = self.b[nb[3]] - bk;
            let gbz = self.b[nb[5]] - bk;
            let grad = 0.5 * d * (gax * gax + gay * gay + gaz * gaz
                + gbx * gbx + gby * gby + gbz * gbz);
            let mod2 = ak * ak + bk * bk;
            let diff = mod2 - v2;
            let pot = diff * diff;
            let coup = -(ak * self.sa[k] + bk * self.sb[k]);
            total += grad + pot + coup;
        }
        total
    }

    /// Serialize current (a, b) to f32 little-endian bytes.
    pub fn snapshot_bytes(&self, buf: &mut Vec<u8>) {
        buf.clear();
        for v in &self.a {
            buf.extend_from_slice(&v.to_le_bytes());
        }
        for v in &self.b {
            buf.extend_from_slice(&v.to_le_bytes());
        }
    }
}
