//! Text -> UTF-8 bits -> multi-component 3D source fields.
//! Gaussian smoothing via 3-pass separable box approximation.

use crate::config::*;
use crate::field::{Field3D, idx};

/// Text -> bit sequence (UTF-8 bytes -> bits).
fn text_to_bits(text: &str) -> Vec<u8> {
    let bytes = text.as_bytes();
    let mut bits = Vec::with_capacity(bytes.len() * 8);
    for &b in bytes {
        for i in (0..8).rev() {
            bits.push((b >> i) & 1);
        }
    }
    bits
}

/// Build a single 3D source field from a subset of bits.
fn build_single(bits: &[u8]) -> Field3D {
    let mut s = vec![0.0f64; NCELLS];
    for (i, &bit) in bits.iter().enumerate() {
        let k = i % NCELLS;
        s[k] += if bit == 1 { 1.0 } else { -1.0 };
    }
    // Gaussian smoothing (3-pass box filter approximation, sigma~1.0)
    gaussian_smooth_3d(&mut s);
    // Normalize to [-1, 1]
    let mx = s.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
    if mx > 0.0 {
        for v in s.iter_mut() {
            *v /= mx;
        }
    }
    s
}

/// Separable 3-pass box filter approximation to Gaussian with sigma~1.0.
/// Each pass: 3-point average [1/3, 1/3, 1/3] along one axis, repeated 3 times.
fn gaussian_smooth_3d(field: &mut [f64]) {
    let mut buf = vec![0.0f64; NCELLS];
    // 3 passes of 3D box filter
    for _ in 0..3 {
        // X-pass
        for z in 0..GRID {
            for y in 0..GRID {
                for x in 0..GRID {
                    let xm = if x == 0 { GRID - 1 } else { x - 1 };
                    let xp = if x == GRID - 1 { 0 } else { x + 1 };
                    buf[idx(x, y, z)] = (field[idx(xm, y, z)]
                        + field[idx(x, y, z)]
                        + field[idx(xp, y, z)]) / 3.0;
                }
            }
        }
        field.copy_from_slice(&buf);
        // Y-pass
        for z in 0..GRID {
            for y in 0..GRID {
                let ym = if y == 0 { GRID - 1 } else { y - 1 };
                let yp = if y == GRID - 1 { 0 } else { y + 1 };
                for x in 0..GRID {
                    buf[idx(x, y, z)] = (field[idx(x, ym, z)]
                        + field[idx(x, y, z)]
                        + field[idx(x, yp, z)]) / 3.0;
                }
            }
        }
        field.copy_from_slice(&buf);
        // Z-pass
        for z in 0..GRID {
            let zm = if z == 0 { GRID - 1 } else { z - 1 };
            let zp = if z == GRID - 1 { 0 } else { z + 1 };
            for y in 0..GRID {
                for x in 0..GRID {
                    buf[idx(x, y, z)] = (field[idx(x, y, zm)]
                        + field[idx(x, y, z)]
                        + field[idx(x, y, zp)]) / 3.0;
                }
            }
        }
        field.copy_from_slice(&buf);
    }
}

/// Build single-component source field (n_comp=1).
pub fn build_source_1(text: &str) -> Vec<Field3D> {
    let bits = text_to_bits(text);
    vec![build_single(&bits)]
}

/// Build multi-component source fields by splitting bits.
///   n_comp=1: all bits -> S[0]
///   n_comp=2: even bits -> S[0], odd bits -> S[1]
///   n_comp=3: i%3==0 -> S[0], i%3==1 -> S[1], i%3==2 -> S[2]
pub fn build_source_mc(text: &str, n_comp: usize) -> Vec<Field3D> {
    let bits = text_to_bits(text);
    if n_comp == 1 {
        return vec![build_single(&bits)];
    }
    let mut groups: Vec<Vec<u8>> = (0..n_comp).map(|_| Vec::new()).collect();
    for (i, &b) in bits.iter().enumerate() {
        groups[i % n_comp].push(b);
    }
    groups.iter().map(|g| build_single(g)).collect()
}
