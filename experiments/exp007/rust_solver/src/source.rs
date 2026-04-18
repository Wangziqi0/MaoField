//! Text -> UTF-8 bits -> 3D source field (single component).

use crate::field::{Field3D, GRID, NCELLS, idx};

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

/// 3-pass separable box filter (approximates Gaussian with sigma~1).
fn gaussian_smooth(field: &mut [f64]) {
    let mut buf = vec![0.0f64; NCELLS];
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

pub fn build_source(text: &str) -> Field3D {
    let bits = text_to_bits(text);
    let mut s = vec![0.0f64; NCELLS];
    for (i, &bit) in bits.iter().enumerate() {
        let k = i % NCELLS;
        s[k] += if bit == 1 { 1.0 } else { -1.0 };
    }
    gaussian_smooth(&mut s);
    let mx = s.iter().map(|v| v.abs()).fold(0.0f64, f64::max);
    if mx > 0.0 {
        for v in s.iter_mut() {
            *v /= mx;
        }
    }
    s
}
