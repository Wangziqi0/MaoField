//! Scalar + Complex (Cl(1)) Allen-Cahn engine.
//!
//! Scalar: ∂u/∂t = D∇²u - u³ + u + (1-3u²)·S
//! Complex (Ginzburg-Landau style):
//!   U = a + b·i, |U|² = a² + b²
//!   ∂U/∂t = D∇²U - U|U|² + U + S
//!   → ∂a/∂t = D∇²a - a(a²+b²) + a + S_a
//!   → ∂b/∂t = D∇²b - b(a²+b²) + b + S_b

pub const G: usize = 32;
pub const N: usize = G * G * G;

const D: f32 = 0.1;
const DT: f32 = 0.1;
const INV_DX2: f32 = 1.0;

// ===== Scalar engine (copied from exp007_rust) =====

pub struct ScalarEngine {
    pub u: Vec<f32>,
    pub s: Vec<f32>,
    pub u_new: Vec<f32>,
    pub nb: Vec<[usize; 6]>,
}

impl ScalarEngine {
    pub fn new() -> Self {
        Self {
            u: vec![0.0; N],
            s: vec![0.0; N],
            u_new: vec![0.0; N],
            nb: build_nb(),
        }
    }

    pub fn init_u(&mut self, seed: u64) {
        let mut rng = seed;
        for v in self.u.iter_mut() {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            *v = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        }
    }

    pub fn set_source(&mut self, src: &[f32]) { self.s.copy_from_slice(src); }

    #[inline(never)]
    pub fn evolve_steps(&mut self, n_steps: usize) {
        let tab = &self.nb;
        for _ in 0..n_steps {
            let u = &self.u; let s = &self.s; let u_new = &mut self.u_new;
            for k in 0..N {
                let nb = unsafe { tab.get_unchecked(k) };
                let ui = unsafe { *u.get_unchecked(k) };
                let si = unsafe { *s.get_unchecked(k) };
                let lap = unsafe {
                    *u.get_unchecked(nb[0]) + *u.get_unchecked(nb[1])
                    + *u.get_unchecked(nb[2]) + *u.get_unchecked(nb[3])
                    + *u.get_unchecked(nb[4]) + *u.get_unchecked(nb[5])
                    - 6.0 * ui
                } * INV_DX2;
                let ui2 = ui * ui;
                let du = D * lap - ui2 * ui + ui + (1.0 - 3.0 * ui2) * si;
                let v = ui + DT * du;
                unsafe { *u_new.get_unchecked_mut(k) = v.clamp(-2.0, 2.0); }
            }
            std::mem::swap(&mut self.u, &mut self.u_new);
        }
    }

    pub fn compute_energy(&self) -> f32 {
        let u = &self.u; let s = &self.s; let tab = &self.nb;
        let mut total = 0.0f32;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ui = unsafe { *u.get_unchecked(k) };
            let si = unsafe { *s.get_unchecked(k) };
            let gx = unsafe { *u.get_unchecked(nb[1]) } - ui;
            let gy = unsafe { *u.get_unchecked(nb[3]) } - ui;
            let gz = unsafe { *u.get_unchecked(nb[5]) } - ui;
            let ui2 = ui * ui;
            total += 0.5 * D * (gx * gx + gy * gy + gz * gz)
                + 0.25 * (ui2 - 1.0) * (ui2 - 1.0)
                - (1.0 - ui2) * ui * si;
        }
        total
    }

    pub fn update_source_m2(&mut self) {
        let mut mx: f32 = 0.0;
        for k in 0..N {
            let v = self.s[k] * self.u[k];
            self.s[k] = v;
            mx = mx.max(v.abs());
        }
        if mx > 0.0 { let inv = 1.0 / mx; for v in self.s.iter_mut() { *v *= inv; } }
    }
}

// ===== Complex Cl(1) engine =====

pub struct ComplexEngine {
    pub a: Vec<f32>,     // real part
    pub b: Vec<f32>,     // imaginary part
    pub sa: Vec<f32>,    // source real
    pub sb: Vec<f32>,    // source imaginary
    pub a_new: Vec<f32>,
    pub b_new: Vec<f32>,
    pub nb: Vec<[usize; 6]>,
}

impl ComplexEngine {
    pub fn new() -> Self {
        Self {
            a: vec![0.0; N], b: vec![0.0; N],
            sa: vec![0.0; N], sb: vec![0.0; N],
            a_new: vec![0.0; N], b_new: vec![0.0; N],
            nb: build_nb(),
        }
    }

    pub fn init_u(&mut self, seed: u64) {
        let mut rng = seed;
        for v in self.a.iter_mut() {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            *v = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        }
        for v in self.b.iter_mut() {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            *v = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        }
    }

    pub fn set_source(&mut self, sa: &[f32], sb: &[f32]) {
        self.sa.copy_from_slice(sa);
        self.sb.copy_from_slice(sb);
    }

    /// Ginzburg-Landau: ∂U/∂t = D∇²U - U|U|² + U + S
    /// ∂a/∂t = D∇²a - a(a²+b²) + a + S_a
    /// ∂b/∂t = D∇²b - b(a²+b²) + b + S_b
    #[inline(never)]
    pub fn evolve_steps(&mut self, n_steps: usize) {
        let tab = &self.nb;
        for _ in 0..n_steps {
            let a = &self.a; let b = &self.b;
            let sa = &self.sa; let sb = &self.sb;
            let a_new = &mut self.a_new; let b_new = &mut self.b_new;
            for k in 0..N {
                let nb = unsafe { tab.get_unchecked(k) };
                let ak = unsafe { *a.get_unchecked(k) };
                let bk = unsafe { *b.get_unchecked(k) };
                let sak = unsafe { *sa.get_unchecked(k) };
                let sbk = unsafe { *sb.get_unchecked(k) };

                let lap_a = unsafe {
                    *a.get_unchecked(nb[0]) + *a.get_unchecked(nb[1])
                    + *a.get_unchecked(nb[2]) + *a.get_unchecked(nb[3])
                    + *a.get_unchecked(nb[4]) + *a.get_unchecked(nb[5])
                    - 6.0 * ak
                } * INV_DX2;
                let lap_b = unsafe {
                    *b.get_unchecked(nb[0]) + *b.get_unchecked(nb[1])
                    + *b.get_unchecked(nb[2]) + *b.get_unchecked(nb[3])
                    + *b.get_unchecked(nb[4]) + *b.get_unchecked(nb[5])
                    - 6.0 * bk
                } * INV_DX2;

                let mod2 = ak * ak + bk * bk; // |U|²
                let da = D * lap_a - ak * mod2 + ak + sak;
                let db = D * lap_b - bk * mod2 + bk + sbk;

                unsafe {
                    *a_new.get_unchecked_mut(k) = (ak + DT * da).clamp(-2.0, 2.0);
                    *b_new.get_unchecked_mut(k) = (bk + DT * db).clamp(-2.0, 2.0);
                }
            }
            std::mem::swap(&mut self.a, &mut self.a_new);
            std::mem::swap(&mut self.b, &mut self.b_new);
        }
    }

    /// Total energy for complex field.
    /// E = ∫ [D/2(|∇a|²+|∇b|²) + ¼(|U|²-1)² - (a·Sa + b·Sb)] dΩ
    pub fn compute_energy(&self) -> f32 {
        let tab = &self.nb;
        let mut total = 0.0f32;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ak = self.a[k]; let bk = self.b[k];
            let gax = unsafe { *self.a.get_unchecked(nb[1]) } - ak;
            let gay = unsafe { *self.a.get_unchecked(nb[3]) } - ak;
            let gaz = unsafe { *self.a.get_unchecked(nb[5]) } - ak;
            let gbx = unsafe { *self.b.get_unchecked(nb[1]) } - bk;
            let gby = unsafe { *self.b.get_unchecked(nb[3]) } - bk;
            let gbz = unsafe { *self.b.get_unchecked(nb[5]) } - bk;
            let grad = 0.5 * D * (gax*gax + gay*gay + gaz*gaz + gbx*gbx + gby*gby + gbz*gbz);
            let mod2 = ak * ak + bk * bk;
            let pot = 0.25 * (mod2 - 1.0) * (mod2 - 1.0);
            let coup = -(ak * self.sa[k] + bk * self.sb[k]);
            total += grad + pot + coup;
        }
        total
    }

    /// Complex M2: S₁ = normalize(S₀ · conj(U*))
    /// S₀·conj(U) = (Sa·a + Sb·b) + (Sb·a - Sa·b)·i
    pub fn update_source_m2_complex(&mut self) {
        let mut mx: f32 = 0.0;
        for k in 0..N {
            let sa = self.sa[k]; let sb = self.sb[k];
            let a = self.a[k]; let b = self.b[k];
            // Complex multiplication S * conj(U) = (Sa*a + Sb*b) + (Sb*a - Sa*b)*i
            let new_sa = sa * a + sb * b;
            let new_sb = sb * a - sa * b;
            self.sa[k] = new_sa;
            self.sb[k] = new_sb;
            mx = mx.max(new_sa.abs()).max(new_sb.abs());
        }
        if mx > 0.0 {
            let inv = 1.0 / mx;
            for v in self.sa.iter_mut() { *v *= inv; }
            for v in self.sb.iter_mut() { *v *= inv; }
        }
    }

    /// Phase at each grid point: atan2(b, a)
    pub fn phase_field(&self) -> Vec<f32> {
        (0..N).map(|k| self.b[k].atan2(self.a[k])).collect()
    }

    /// Amplitude at each grid point: sqrt(a²+b²)
    pub fn amplitude_field(&self) -> Vec<f32> {
        (0..N).map(|k| (self.a[k]*self.a[k] + self.b[k]*self.b[k]).sqrt()).collect()
    }
}

/// Phase-based matching: mean |phase_q - phase_d| (circular distance).
pub fn phase_distance(pq: &[f32], pd: &[f32]) -> f32 {
    let mut total = 0.0f32;
    for k in 0..N {
        let diff = (pq[k] - pd[k]).abs();
        let circ = diff.min(std::f32::consts::TAU - diff);
        total += circ;
    }
    total / N as f32
}

/// Amplitude-based matching: L2 distance.
pub fn amplitude_distance(aq: &[f32], ad: &[f32]) -> f32 {
    let mut total = 0.0f32;
    for k in 0..N {
        let d = aq[k] - ad[k];
        total += d * d;
    }
    total.sqrt()
}

// ===== Shared utilities =====

fn build_nb() -> Vec<[usize; 6]> {
    let mut nb = Vec::with_capacity(N);
    for z in 0..G {
        let zm = if z == 0 { G - 1 } else { z - 1 };
        let zp = if z == G - 1 { 0 } else { z + 1 };
        for y in 0..G {
            let ym = if y == 0 { G - 1 } else { y - 1 };
            let yp = if y == G - 1 { 0 } else { y + 1 };
            for x in 0..G {
                let xm = if x == 0 { G - 1 } else { x - 1 };
                let xp = if x == G - 1 { 0 } else { x + 1 };
                nb.push([
                    xm + y*G + z*G*G, xp + y*G + z*G*G,
                    x + ym*G + z*G*G, x + yp*G + z*G*G,
                    x + y*G + zm*G*G, x + y*G + zp*G*G,
                ]);
            }
        }
    }
    nb
}

pub fn normalize_f32(s: &mut [f32]) {
    let mx = s.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
    if mx > 0.0 { let inv = 1.0 / mx; for v in s.iter_mut() { *v *= inv; } }
}

pub fn build_source_f32(text: &str) -> Vec<f32> {
    let bytes = text.as_bytes();
    let mut s = vec![0.0f32; N];
    let mut bit_idx = 0usize;
    for &b in bytes {
        for i in (0..8).rev() {
            let k = bit_idx % N;
            s[k] += if (b >> i) & 1 == 1 { 1.0 } else { -1.0 };
            bit_idx += 1;
        }
    }
    let mut buf = vec![0.0f32; N];
    for _ in 0..3 {
        for z in 0..G { for y in 0..G { for x in 0..G {
            let xm = if x==0{G-1}else{x-1}; let xp = if x==G-1{0}else{x+1};
            let k = x+y*G+z*G*G;
            buf[k] = (s[xm+y*G+z*G*G] + s[k] + s[xp+y*G+z*G*G]) / 3.0;
        }}} s.copy_from_slice(&buf);
        for z in 0..G { for y in 0..G {
            let ym = if y==0{G-1}else{y-1}; let yp = if y==G-1{0}else{y+1};
            for x in 0..G { let k = x+y*G+z*G*G;
            buf[k] = (s[x+ym*G+z*G*G] + s[k] + s[x+yp*G+z*G*G]) / 3.0;
        }}} s.copy_from_slice(&buf);
        for z in 0..G {
            let zm = if z==0{G-1}else{z-1}; let zp = if z==G-1{0}else{z+1};
            for y in 0..G { for x in 0..G { let k = x+y*G+z*G*G;
            buf[k] = (s[x+y*G+zm*G*G] + s[k] + s[x+y*G+zp*G*G]) / 3.0;
        }}} s.copy_from_slice(&buf);
    }
    normalize_f32(&mut s);
    s
}

/// Build complex source: even bits → real, odd bits → imaginary.
pub fn build_source_complex(text: &str) -> (Vec<f32>, Vec<f32>) {
    let bytes = text.as_bytes();
    let mut sa = vec![0.0f32; N];
    let mut sb = vec![0.0f32; N];
    let mut bit_idx = 0usize;
    for &byte in bytes {
        for i in (0..8).rev() {
            let bit = if (byte >> i) & 1 == 1 { 1.0f32 } else { -1.0 };
            let k = (bit_idx / 2) % N;
            if bit_idx % 2 == 0 { sa[k] += bit; } else { sb[k] += bit; }
            bit_idx += 1;
        }
    }
    // Smooth + normalize each component
    let smooth = |s: &mut Vec<f32>| {
        let mut buf = vec![0.0f32; N];
        for _ in 0..3 {
            for z in 0..G { for y in 0..G { for x in 0..G {
                let xm = if x==0{G-1}else{x-1}; let xp = if x==G-1{0}else{x+1};
                let k = x+y*G+z*G*G;
                buf[k] = (s[xm+y*G+z*G*G] + s[k] + s[xp+y*G+z*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
            for z in 0..G { for y in 0..G {
                let ym = if y==0{G-1}else{y-1}; let yp = if y==G-1{0}else{y+1};
                for x in 0..G { let k = x+y*G+z*G*G;
                buf[k] = (s[x+ym*G+z*G*G] + s[k] + s[x+yp*G+z*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
            for z in 0..G {
                let zm = if z==0{G-1}else{z-1}; let zp = if z==G-1{0}else{z+1};
                for y in 0..G { for x in 0..G { let k = x+y*G+z*G*G;
                buf[k] = (s[x+y*G+zm*G*G] + s[k] + s[x+y*G+zp*G*G]) / 3.0;
            }}} s.copy_from_slice(&buf);
        }
        normalize_f32(s);
    };
    smooth(&mut sa);
    smooth(&mut sb);
    (sa, sb)
}
