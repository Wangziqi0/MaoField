//! MaoField fast engine v3: back to Vec-based neighbor table (LLVM vectorizes better).
//!
//! v1 approach: Vec<[usize;6]> + unsafe get_unchecked = 0.10ms/step
//! v2 static u32 approach was slower (0.26ms) due to lost auto-vectorization.
//! v3 = v1 core + adaptive early exit + inplace buffers.

pub const G: usize = 32;
pub const N: usize = G * G * G;

const D: f32 = 0.1;
const DT: f32 = 0.1;
const INV_DX2: f32 = 1.0;

pub struct MaoFieldEngine {
    pub u: Vec<f32>,
    pub s: Vec<f32>,
    u_new: Vec<f32>,
    nb: Vec<[usize; 6]>,
    pub e_buf: Vec<f32>,
    pub s_buf: Vec<f32>,
}

impl MaoFieldEngine {
    pub fn new() -> Self {
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
                        xm + y * G + z * G * G,
                        xp + y * G + z * G * G,
                        x + ym * G + z * G * G,
                        x + yp * G + z * G * G,
                        x + y * G + zm * G * G,
                        x + y * G + zp * G * G,
                    ]);
                }
            }
        }
        Self {
            u: vec![0.0; N],
            s: vec![0.0; N],
            u_new: vec![0.0; N],
            nb,
            e_buf: vec![0.0; N],
            s_buf: vec![0.0; N],
        }
    }

    pub fn init_u(&mut self, seed: u64) {
        let mut rng = seed;
        for v in self.u.iter_mut() {
            rng ^= rng << 13;
            rng ^= rng >> 7;
            rng ^= rng << 17;
            *v = (rng as f32 / u64::MAX as f32) * 0.02 - 0.01;
        }
    }

    pub fn set_source(&mut self, src: &[f32]) {
        self.s.copy_from_slice(src);
    }

    #[inline(never)]
    pub fn evolve_steps(&mut self, n_steps: usize) {
        let tab = &self.nb;
        for _ in 0..n_steps {
            let u = &self.u;
            let s = &self.s;
            let u_new = &mut self.u_new;
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
                unsafe {
                    *u_new.get_unchecked_mut(k) = if v > 2.0 { 2.0 } else if v < -2.0 { -2.0 } else { v };
                }
            }
            std::mem::swap(&mut self.u, &mut self.u_new);
        }
    }

    /// Adaptive: check energy every check_every steps, stop if converged.
    pub fn evolve_adaptive(&mut self, max_steps: usize, check_every: usize, tol: f32) -> usize {
        let mut prev_e = self.compute_energy();
        let mut done = 0;
        while done < max_steps {
            let batch = check_every.min(max_steps - done);
            self.evolve_steps(batch);
            done += batch;
            let e = self.compute_energy();
            if ((e - prev_e) / (prev_e.abs() + 1e-10)).abs() < tol {
                break;
            }
            prev_e = e;
        }
        done
    }

    pub fn compute_energy(&self) -> f32 {
        let u = &self.u;
        let s = &self.s;
        let tab = &self.nb;
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

    pub fn compute_energy_density_inplace(&mut self) {
        let u = &self.u;
        let s = &self.s;
        let tab = &self.nb;
        for k in 0..N {
            let nb = unsafe { tab.get_unchecked(k) };
            let ui = unsafe { *u.get_unchecked(k) };
            let si = unsafe { *s.get_unchecked(k) };
            let gx = unsafe { *u.get_unchecked(nb[1]) } - ui;
            let gy = unsafe { *u.get_unchecked(nb[3]) } - ui;
            let gz = unsafe { *u.get_unchecked(nb[5]) } - ui;
            let ui2 = ui * ui;
            unsafe {
                *self.e_buf.get_unchecked_mut(k) = 0.5 * D * (gx * gx + gy * gy + gz * gz)
                    + 0.25 * (ui2 - 1.0) * (ui2 - 1.0)
                    - (1.0 - ui2) * ui * si;
            }
        }
    }

    pub fn update_source_m2(&mut self) {
        let mut mx: f32 = 0.0;
        for k in 0..N {
            let v = self.s[k] * self.u[k];
            self.s[k] = v;
            let a = v.abs();
            if a > mx { mx = a; }
        }
        if mx > 0.0 {
            let inv = 1.0 / mx;
            for v in self.s.iter_mut() { *v *= inv; }
        }
    }

    pub fn compute_couplings_into(&self, corpus: &[Vec<f32>], out: &mut Vec<f32>) {
        out.clear();
        let e = &self.e_buf;
        for sc in corpus {
            let mut c: f32 = 0.0;
            for k in 0..N {
                c += unsafe { *e.get_unchecked(k) * *sc.get_unchecked(k) };
            }
            out.push(c.abs());
        }
    }

    pub fn topk_indices(couplings: &[f32], k: usize) -> Vec<usize> {
        let mut best: Vec<(usize, f32)> = Vec::with_capacity(k);
        for (i, &c) in couplings.iter().enumerate() {
            if best.len() < k {
                best.push((i, c));
                if best.len() == k {
                    best.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
                }
            } else if c > best[k - 1].1 {
                best[k - 1] = (i, c);
                best.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
            }
        }
        best.iter().map(|(i, _)| *i).collect()
    }

    pub fn adjoint_iteration_m2(&mut self, corpus: &[Vec<f32>], max_rounds: usize, k: usize, tol: f32) {
        let mut prev_metric: Option<f32> = None;
        let mut couplings = Vec::with_capacity(corpus.len());

        for _round in 0..max_rounds {
            self.compute_energy_density_inplace();
            let e_std = {
                let mean = self.e_buf.iter().sum::<f32>() / N as f32;
                let var = self.e_buf.iter().map(|v| (v - mean) * (v - mean)).sum::<f32>() / N as f32;
                var.sqrt()
            };
            self.compute_couplings_into(corpus, &mut couplings);
            let targets = Self::topk_indices(&couplings, k);

            if let Some(prev) = prev_metric {
                if (e_std - prev).abs() / (prev.abs() + 1e-10) < tol { break; }
            }
            prev_metric = Some(e_std);

            self.s_buf.copy_from_slice(&self.s);
            for &ci in &targets {
                let sc = &corpus[ci];
                let mut mx: f32 = 0.0;
                for j in 0..N {
                    let v = self.s_buf[j] + sc[j];
                    self.s[j] = v;
                    let a = v.abs();
                    if a > mx { mx = a; }
                }
                if mx > 0.0 {
                    let inv = 1.0 / mx;
                    for v in self.s.iter_mut() { *v *= inv; }
                }
                self.evolve_steps(300);
                self.s.copy_from_slice(&self.s_buf);
                self.evolve_steps(100);
            }
            self.update_source_m2();
            self.s_buf.copy_from_slice(&self.s);
        }
    }

    pub fn adjoint_iteration_fixed(&mut self, corpus: &[Vec<f32>], max_rounds: usize, k: usize, tol: f32) {
        let mut prev_metric: Option<f32> = None;
        let mut couplings = Vec::with_capacity(corpus.len());

        for _round in 0..max_rounds {
            self.compute_energy_density_inplace();
            let e_std = {
                let mean = self.e_buf.iter().sum::<f32>() / N as f32;
                let var = self.e_buf.iter().map(|v| (v - mean) * (v - mean)).sum::<f32>() / N as f32;
                var.sqrt()
            };
            self.compute_couplings_into(corpus, &mut couplings);
            let targets = Self::topk_indices(&couplings, k);

            if let Some(prev) = prev_metric {
                if (e_std - prev).abs() / (prev.abs() + 1e-10) < tol { break; }
            }
            prev_metric = Some(e_std);

            self.s_buf.copy_from_slice(&self.s);
            for &ci in &targets {
                let sc = &corpus[ci];
                let mut mx: f32 = 0.0;
                for j in 0..N {
                    let v = self.s_buf[j] + sc[j];
                    self.s[j] = v;
                    let a = v.abs();
                    if a > mx { mx = a; }
                }
                if mx > 0.0 {
                    let inv = 1.0 / mx;
                    for v in self.s.iter_mut() { *v *= inv; }
                }
                self.evolve_steps(300);
                self.s.copy_from_slice(&self.s_buf);
                self.evolve_steps(100);
            }
        }
    }
}

pub fn normalize_f32(s: &mut [f32]) {
    let mx = s.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
    if mx > 0.0 {
        let inv = 1.0 / mx;
        for v in s.iter_mut() { *v *= inv; }
    }
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
        for z in 0..G {
            for y in 0..G {
                for x in 0..G {
                    let xm = if x == 0 { G - 1 } else { x - 1 };
                    let xp = if x == G - 1 { 0 } else { x + 1 };
                    let k = x + y * G + z * G * G;
                    buf[k] = (s[xm + y * G + z * G * G] + s[k] + s[xp + y * G + z * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
        for z in 0..G {
            for y in 0..G {
                let ym = if y == 0 { G - 1 } else { y - 1 };
                let yp = if y == G - 1 { 0 } else { y + 1 };
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    buf[k] = (s[x + ym * G + z * G * G] + s[k] + s[x + yp * G + z * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
        for z in 0..G {
            let zm = if z == 0 { G - 1 } else { z - 1 };
            let zp = if z == G - 1 { 0 } else { z + 1 };
            for y in 0..G {
                for x in 0..G {
                    let k = x + y * G + z * G * G;
                    buf[k] = (s[x + y * G + zm * G * G] + s[k] + s[x + y * G + zp * G * G]) / 3.0;
                }
            }
        }
        s.copy_from_slice(&buf);
    }
    normalize_f32(&mut s);
    s
}
