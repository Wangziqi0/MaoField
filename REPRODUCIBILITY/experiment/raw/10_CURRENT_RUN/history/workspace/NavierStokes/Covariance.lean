import Mathlib.Analysis.Real.Sqrt
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring














noncomputable section

namespace NavierStokes.Covariance

open Matrix


def signedMatrix (a b scaleMinus scalePlus : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-a * scaleMinus, -a * scalePlus;
     -b * scaleMinus,  b * scalePlus]


def target (m t : ℝ) : Fin 2 → ℝ := ![-m, t]


def coefficients (a b scaleMinus scalePlus m t : ℝ) : Fin 2 → ℝ :=
  ![(b * m - a * t) / (2 * a * b * scaleMinus),
    (b * m + a * t) / (2 * a * b * scalePlus)]

theorem determinant_formula (a b scaleMinus scalePlus : ℝ) :
    (signedMatrix a b scaleMinus scalePlus).det =
      -(2 * a * b * scaleMinus * scalePlus) := by
  simp [signedMatrix, Matrix.det_fin_two]
  ring

theorem determinant_neg {a b scaleMinus scalePlus : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus) :
    (signedMatrix a b scaleMinus scalePlus).det < 0 := by
  rw [determinant_formula]
  have : 0 < 2 * a * b * scaleMinus * scalePlus := by positivity
  linarith

theorem determinant_ne_zero {a b scaleMinus scalePlus : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus) :
    (signedMatrix a b scaleMinus scalePlus).det ≠ 0 :=
  ne_of_lt (determinant_neg ha hb hMinus hPlus)


theorem reconstruct {a b scaleMinus scalePlus : ℝ} (m t : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0)
    (hMinus : scaleMinus ≠ 0) (hPlus : scalePlus ≠ 0) :
    (signedMatrix a b scaleMinus scalePlus).mulVec
      (coefficients a b scaleMinus scalePlus m t) = target m t := by
  ext i
  fin_cases i <;>
    simp [signedMatrix, coefficients, target, Matrix.mulVec, dotProduct,
      Fin.sum_univ_two] <;>
    field_simp <;> ring


theorem inverse_formula {a b scaleMinus scalePlus : ℝ} (m t : ℝ)
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus) :
    (signedMatrix a b scaleMinus scalePlus)⁻¹.mulVec (target m t) =
      coefficients a b scaleMinus scalePlus m t := by
  have hdet : IsUnit (signedMatrix a b scaleMinus scalePlus).det :=
    isUnit_iff_ne_zero.mpr (determinant_ne_zero ha hb hMinus hPlus)
  rw [← reconstruct m t (ne_of_gt ha) (ne_of_gt hb)
    (ne_of_gt hMinus) (ne_of_gt hPlus)]
  rw [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hdet, Matrix.one_mulVec]

theorem solution_unique {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (y : Fin 2 → ℝ)
    (hy : (signedMatrix a b scaleMinus scalePlus).mulVec y = target m t) :
    y = coefficients a b scaleMinus scalePlus m t := by
  have hdet : IsUnit (signedMatrix a b scaleMinus scalePlus).det :=
    isUnit_iff_ne_zero.mpr (determinant_ne_zero ha hb hMinus hPlus)
  calc
    y = (signedMatrix a b scaleMinus scalePlus)⁻¹.mulVec
        ((signedMatrix a b scaleMinus scalePlus).mulVec y) := by
      rw [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hdet, Matrix.one_mulVec]
    _ = (signedMatrix a b scaleMinus scalePlus)⁻¹.mulVec (target m t) := by rw [hy]
    _ = coefficients a b scaleMinus scalePlus m t :=
      inverse_formula m t ha hb hMinus hPlus


theorem coefficients_pos {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hcone : |a * t| < b * m) :
    ∀ i, 0 < coefficients a b scaleMinus scalePlus m t i := by
  have hc := abs_lt.mp hcone
  intro i
  fin_cases i
  · change 0 < (b * m - a * t) / (2 * a * b * scaleMinus)
    exact div_pos (by linarith) (by positivity)
  · change 0 < (b * m + a * t) / (2 * a * b * scalePlus)
    exact div_pos (by linarith) (by positivity)


theorem coefficients_pos_iff {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus) :
    (∀ i, 0 < coefficients a b scaleMinus scalePlus m t i) ↔ |a * t| < b * m := by
  constructor
  · intro hy
    have hm : 0 < 2 * a * b * scaleMinus := by positivity
    have hp : 0 < 2 * a * b * scalePlus := by positivity
    have hnMinus : 0 < b * m - a * t :=
      (div_pos_iff_of_pos_right hm).mp (by simpa [coefficients] using hy 0)
    have hnPlus : 0 < b * m + a * t :=
      (div_pos_iff_of_pos_right hp).mp (by simpa [coefficients] using hy 1)
    exact abs_lt.mpr ⟨by linarith, by linarith⟩
  · exact coefficients_pos ha hb hMinus hPlus


def amplitudes (a b scaleMinus scalePlus m t : ℝ) : Fin 2 → ℝ :=
  fun i => Real.sqrt (coefficients a b scaleMinus scalePlus m t i)

theorem amplitudes_pos {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hcone : |a * t| < b * m) :
    ∀ i, 0 < amplitudes a b scaleMinus scalePlus m t i := by
  intro i
  exact Real.sqrt_pos.mpr (coefficients_pos ha hb hMinus hPlus hcone i)

theorem amplitudes_sq {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hcone : |a * t| < b * m) :
    (fun i => (amplitudes a b scaleMinus scalePlus m t i) ^ 2) =
      coefficients a b scaleMinus scalePlus m t := by
  funext i
  exact Real.sq_sqrt (le_of_lt (coefficients_pos ha hb hMinus hPlus hcone i))


theorem reconstruct_from_amplitudes {a b scaleMinus scalePlus m t : ℝ}
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hcone : |a * t| < b * m) :
    (signedMatrix a b scaleMinus scalePlus).mulVec
        (fun i => (amplitudes a b scaleMinus scalePlus m t i) ^ 2) = target m t := by
  rw [amplitudes_sq ha hb hMinus hPlus hcone]
  exact reconstruct m t (ne_of_gt ha) (ne_of_gt hb) (ne_of_gt hMinus) (ne_of_gt hPlus)



theorem scaled_primary_covariance {a b scaleMinus scalePlus m t ε : ℝ}
    (mask : ℝ) (hε : 0 ≤ ε)
    (ha : 0 < a) (hb : 0 < b)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hcone : |a * t| < b * m) :
    (signedMatrix a b scaleMinus scalePlus).mulVec
        (fun i => (Real.sqrt ε * amplitudes a b scaleMinus scalePlus m t i * mask) ^ 2) =
      (ε * mask ^ 2) • target m t := by
  have hsq :
      (fun i => (Real.sqrt ε * amplitudes a b scaleMinus scalePlus m t i * mask) ^ 2) =
        (ε * mask ^ 2) • (fun i => (amplitudes a b scaleMinus scalePlus m t i) ^ 2) := by
    funext i
    simp only [Pi.smul_apply, smul_eq_mul, mul_pow, Real.sq_sqrt hε]
    ring
  rw [hsq, Matrix.mulVec_smul, reconstruct_from_amplitudes ha hb hMinus hPlus hcone]


def normalMagnitude (c u : ℝ) : ℝ := -c * Real.sqrt (1 + u ^ 2)

theorem normalMagnitude_pos {c u : ℝ} (hc : c < 0) : 0 < normalMagnitude c u := by
  unfold normalMagnitude
  exact mul_pos (neg_pos.mpr hc) (Real.sqrt_pos.mpr (by nlinarith [sq_nonneg u]))


theorem cone_of_ratio {c u m t : ℝ} (hm : 0 < m)
    (hratio : |c * t / m| < u / Real.sqrt (1 + u ^ 2)) :
    |normalMagnitude c u * t| < u * m := by
  have hs : 0 < Real.sqrt (1 + u ^ 2) :=
    Real.sqrt_pos.mpr (by nlinarith [sq_nonneg u])
  have hr : |c * t| / m < u / Real.sqrt (1 + u ^ 2) := by
    simpa only [abs_div, abs_of_pos hm] using hratio
  have hcross : |c * t| * Real.sqrt (1 + u ^ 2) < u * m :=
    (div_lt_div_iff₀ hm hs).mp hr
  calc
    |normalMagnitude c u * t| = |c * t| * Real.sqrt (1 + u ^ 2) := by
      rw [show normalMagnitude c u * t = -(c * t) * Real.sqrt (1 + u ^ 2) by
        unfold normalMagnitude
        ring]
      rw [abs_mul, abs_neg, abs_of_pos hs]
    _ < u * m := hcross



theorem positive_primary {c u scaleMinus scalePlus m t : ℝ}
    (hc : c < 0) (hu : 0 < u) (hm : 0 < m)
    (hMinus : 0 < scaleMinus) (hPlus : 0 < scalePlus)
    (hratio : |c * t / m| < u / Real.sqrt (1 + u ^ 2)) :
    ∃ velocity : Fin 2 → ℝ,
      (∀ i, 0 < velocity i) ∧
      (signedMatrix (normalMagnitude c u) u scaleMinus scalePlus).mulVec
        (fun i => (velocity i) ^ 2) = target m t := by
  refine ⟨amplitudes (normalMagnitude c u) u scaleMinus scalePlus m t, ?_, ?_⟩
  · exact amplitudes_pos (normalMagnitude_pos hc) hu hMinus hPlus
      (cone_of_ratio hm hratio)
  · exact reconstruct_from_amplitudes (normalMagnitude_pos hc) hu hMinus hPlus
      (cone_of_ratio hm hratio)

end NavierStokes.Covariance
