import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring










noncomputable section

namespace NavierStokes.StressAlgebra

open MeasureTheory Set


def axialExponent (h : ℝ) : ℝ := 1 / 2 - h


def velocityExponent (h : ℝ) : ℝ := 1 / 2 + h


def coordinateFactor (η : ℝ) : ℝ := 1 - η ^ 2


def angularSource (h η x W U H Hx Hη : ℝ) : ℝ :=
  -W * x * Hx - h * (1 - 2 * η * U) * H -
    (axialExponent h * η + coordinateFactor η * U) * Hη


def axialSource (h η x W U Ux Uη P Px Pη : ℝ) : ℝ :=
  -W * x * Ux - velocityExponent h * (1 - 2 * η * U) * U -
    (axialExponent h * η + coordinateFactor η * U) * Uη -
    coordinateFactor η * Pη + 4 * velocityExponent h * η * P + 2 * η * x * Px


def angularPrimitive (h η : ℝ) (W H I Iη J Jη : ℝ → ℝ) (x : ℝ) : ℝ :=
  -(x * W x * H x) + (1 - h) * I x - axialExponent h * η * Iη x -
    coordinateFactor η * Jη x + 2 * (h - axialExponent h) * η * J x


def axialPrimitive (h η : ℝ) (W U M Mη S Sη P Pη : ℝ → ℝ) (x : ℝ) : ℝ :=
  -(x * W x * U x) + axialExponent h * (M x - η * Mη x) +
    4 * h * η * S x - coordinateFactor η * Sη x +
    x * (4 * velocityExponent h * η * P x - coordinateFactor η * Pη x)


theorem angular_derivative_algebra
    (h η x W Wx U Uη H Hx Hη : ℝ)
    (hW : W + x * Wx = 1 - 2 * axialExponent h * η * U - coordinateFactor η * Uη) :
    -((W + x * Wx) * H + x * W * Hx) + (1 - h) * H -
      axialExponent h * η * Hη - coordinateFactor η * (Uη * H + U * Hη) +
      2 * (h - axialExponent h) * η * (U * H) =
      angularSource h η x W U H Hx Hη := by
  unfold angularSource
  linear_combination -H * hW


theorem axial_derivative_algebra
    (h η x W Wx U Ux Uη E Eη P Px Pη Pηx : ℝ)
    (hW : W + x * Wx = 1 - 2 * axialExponent h * η * U - coordinateFactor η * Uη)
    (hP : x * Px = E ^ 2 / 2)
    (hPη : x * Pηx = E * Eη) :
    -((W + x * Wx) * U + x * W * Ux) + axialExponent h * (U - η * Uη) +
      4 * h * η * (U ^ 2 - E ^ 2 / 2) -
      coordinateFactor η * (2 * U * Uη - E * Eη) +
      (4 * velocityExponent h * η * P - coordinateFactor η * Pη) +
      x * (4 * velocityExponent h * η * Px - coordinateFactor η * Pηx) =
      axialSource h η x W U Ux Uη P Px Pη := by
  unfold axialSource axialExponent velocityExponent coordinateFactor at *
  linear_combination -U * hW + (4 * h * η) * hP - (1 - η ^ 2) * hPη




theorem angularPrimitive_hasDerivAt
    (h η x : ℝ) (W H I Iη J Jη : ℝ → ℝ) (Wx Hx U Uη Hη : ℝ)
    (hWderiv : HasDerivAt W Wx x) (hH : HasDerivAt H Hx x)
    (hI : HasDerivAt I (H x) x) (hIη : HasDerivAt Iη Hη x)
    (hJ : HasDerivAt J (U * H x) x)
    (hJη : HasDerivAt Jη (Uη * H x + U * Hη) x)
    (hW : W x + x * Wx =
      1 - 2 * axialExponent h * η * U - coordinateFactor η * Uη) :
    HasDerivAt (angularPrimitive h η W H I Iη J Jη)
      (angularSource h η x (W x) U (H x) Hx Hη) x := by
  have hd := (((((hasDerivAt_id x).mul hWderiv).mul hH).neg.add
    (hI.const_mul (1 - h))).sub (hIη.const_mul (axialExponent h * η))).sub
      (hJη.const_mul (coordinateFactor η))
  have hd' := hd.add (hJ.const_mul (2 * (h - axialExponent h) * η))
  apply hd'.congr_deriv
  simpa only [Pi.mul_apply, Pi.sub_apply, id_eq, one_mul] using
    angular_derivative_algebra h η x (W x) Wx U Uη (H x) Hx Hη hW



theorem axialPrimitive_hasDerivAt
    (h η x : ℝ) (W U M Mη S Sη P Pη : ℝ → ℝ)
    (Wx Ux Uη E Eη Px Pηx : ℝ)
    (hWderiv : HasDerivAt W Wx x) (hU : HasDerivAt U Ux x)
    (hM : HasDerivAt M (U x) x) (hMη : HasDerivAt Mη Uη x)
    (hS : HasDerivAt S ((U x) ^ 2 - E ^ 2 / 2) x)
    (hSη : HasDerivAt Sη (2 * U x * Uη - E * Eη) x)
    (hPderiv : HasDerivAt P Px x) (hPηderiv : HasDerivAt Pη Pηx x)
    (hW : W x + x * Wx =
      1 - 2 * axialExponent h * η * U x - coordinateFactor η * Uη)
    (hP : x * Px = E ^ 2 / 2) (hPη : x * Pηx = E * Eη) :
    HasDerivAt (axialPrimitive h η W U M Mη S Sη P Pη)
      (axialSource h η x (W x) (U x) Ux Uη (P x) Px (Pη x)) x := by
  have hd := (((((hasDerivAt_id x).mul hWderiv).mul hU).neg.add
    ((hM.sub (hMη.const_mul η)).const_mul (axialExponent h))).add
      (hS.const_mul (4 * h * η))).sub (hSη.const_mul (coordinateFactor η))
  have hd' := hd.add ((hasDerivAt_id x).mul
    ((hPderiv.const_mul (4 * velocityExponent h * η)).sub
      (hPηderiv.const_mul (coordinateFactor η))))
  apply hd'.congr_deriv
  simpa only [Pi.mul_apply, Pi.sub_apply, id_eq, one_mul, add_assoc] using
    axial_derivative_algebra h η x (W x) Wx (U x) Ux Uη E Eη
      (P x) Px (Pη x) Pηx hW hP hPη



structure AngularMomentData (h η X : ℝ) where
  W : ℝ → ℝ
  Wx : ℝ → ℝ
  H : ℝ → ℝ
  Hx : ℝ → ℝ
  Hη : ℝ → ℝ
  U : ℝ → ℝ
  Uη : ℝ → ℝ
  I : ℝ → ℝ
  Iη : ℝ → ℝ
  J : ℝ → ℝ
  Jη : ℝ → ℝ
  W_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt W (Wx x) x
  H_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt H (Hx x) x
  I_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt I (H x) x
  Iη_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt Iη (Hη x) x
  J_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt J (U x * H x) x
  Jη_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt Jη (Uη x * H x + U x * Hη x) x
  W_balance : ∀ x ∈ uIcc 0 X,
    W x + x * Wx x = 1 - 2 * axialExponent h * η * U x - coordinateFactor η * Uη x
  I_zero : I 0 = 0
  Iη_zero : Iη 0 = 0
  J_zero : J 0 = 0
  Jη_zero : Jη 0 = 0



theorem angular_integrated_identity
    {h η X : ℝ} (p : AngularMomentData h η X)
    (hint : IntervalIntegrable
      (fun x => angularSource h η x (p.W x) (p.U x) (p.H x) (p.Hx x) (p.Hη x))
      volume 0 X) :
    intervalIntegral
      (fun x => angularSource h η x (p.W x) (p.U x) (p.H x) (p.Hx x) (p.Hη x))
      0 X volume =
      angularPrimitive h η p.W p.H p.I p.Iη p.J p.Jη X := by
  have hd : ∀ x ∈ uIcc 0 X,
      HasDerivAt (angularPrimitive h η p.W p.H p.I p.Iη p.J p.Jη)
        (angularSource h η x (p.W x) (p.U x) (p.H x) (p.Hx x) (p.Hη x)) x := by
    intro x hx
    exact angularPrimitive_hasDerivAt h η x p.W p.H p.I p.Iη p.J p.Jη
      (p.Wx x) (p.Hx x) (p.U x) (p.Uη x) (p.Hη x)
      (p.W_deriv x hx) (p.H_deriv x hx) (p.I_deriv x hx) (p.Iη_deriv x hx)
      (p.J_deriv x hx) (p.Jη_deriv x hx) (p.W_balance x hx)
  have hzero : angularPrimitive h η p.W p.H p.I p.Iη p.J p.Jη 0 = 0 := by
    simp [angularPrimitive, p.I_zero, p.Iη_zero, p.J_zero, p.Jη_zero]
  simpa only [hzero, sub_zero] using
    intervalIntegral.integral_eq_sub_of_hasDerivAt hd hint


structure AxialMomentData (h η X : ℝ) where
  W : ℝ → ℝ
  Wx : ℝ → ℝ
  U : ℝ → ℝ
  Ux : ℝ → ℝ
  Uη : ℝ → ℝ
  E : ℝ → ℝ
  Eη : ℝ → ℝ
  P : ℝ → ℝ
  Px : ℝ → ℝ
  Pη : ℝ → ℝ
  Pηx : ℝ → ℝ
  M : ℝ → ℝ
  Mη : ℝ → ℝ
  S : ℝ → ℝ
  Sη : ℝ → ℝ
  W_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt W (Wx x) x
  U_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt U (Ux x) x
  M_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt M (U x) x
  Mη_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt Mη (Uη x) x
  S_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt S (U x ^ 2 - E x ^ 2 / 2) x
  Sη_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt Sη (2 * U x * Uη x - E x * Eη x) x
  P_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt P (Px x) x
  Pη_deriv : ∀ x ∈ uIcc 0 X, HasDerivAt Pη (Pηx x) x
  W_balance : ∀ x ∈ uIcc 0 X,
    W x + x * Wx x = 1 - 2 * axialExponent h * η * U x - coordinateFactor η * Uη x
  pressure_balance : ∀ x ∈ uIcc 0 X, x * Px x = E x ^ 2 / 2
  pressure_η_balance : ∀ x ∈ uIcc 0 X, x * Pηx x = E x * Eη x
  M_zero : M 0 = 0
  Mη_zero : Mη 0 = 0
  S_zero : S 0 = 0
  Sη_zero : Sη 0 = 0


theorem axial_integrated_identity
    {h η X : ℝ} (p : AxialMomentData h η X)
    (hint : IntervalIntegrable
      (fun x => axialSource h η x (p.W x) (p.U x) (p.Ux x) (p.Uη x)
        (p.P x) (p.Px x) (p.Pη x)) volume 0 X) :
    intervalIntegral
      (fun x => axialSource h η x (p.W x) (p.U x) (p.Ux x) (p.Uη x)
        (p.P x) (p.Px x) (p.Pη x)) 0 X volume =
      axialPrimitive h η p.W p.U p.M p.Mη p.S p.Sη p.P p.Pη X := by
  have hd : ∀ x ∈ uIcc 0 X,
      HasDerivAt (axialPrimitive h η p.W p.U p.M p.Mη p.S p.Sη p.P p.Pη)
        (axialSource h η x (p.W x) (p.U x) (p.Ux x) (p.Uη x)
          (p.P x) (p.Px x) (p.Pη x)) x := by
    intro x hx
    exact axialPrimitive_hasDerivAt h η x p.W p.U p.M p.Mη p.S p.Sη p.P p.Pη
      (p.Wx x) (p.Ux x) (p.Uη x) (p.E x) (p.Eη x) (p.Px x) (p.Pηx x)
      (p.W_deriv x hx) (p.U_deriv x hx) (p.M_deriv x hx) (p.Mη_deriv x hx)
      (p.S_deriv x hx) (p.Sη_deriv x hx) (p.P_deriv x hx) (p.Pη_deriv x hx)
      (p.W_balance x hx) (p.pressure_balance x hx) (p.pressure_η_balance x hx)
  have hzero : axialPrimitive h η p.W p.U p.M p.Mη p.S p.Sη p.P p.Pη 0 = 0 := by
    simp [axialPrimitive, p.M_zero, p.Mη_zero, p.S_zero, p.Sη_zero]
  simpa only [hzero, sub_zero] using
    intervalIntegral.integral_eq_sub_of_hasDerivAt hd hint



theorem angular_integrated_lag
    {h η X : ℝ} (p : AngularMomentData h η X) (hX : X ≠ 0) (hH : p.H X ≠ 0)
    (hint : IntervalIntegrable
      (fun x => angularSource h η x (p.W x) (p.U x) (p.H x) (p.Hx x) (p.Hη x))
      volume 0 X) :
    intervalIntegral
      (fun x => angularSource h η x (p.W x) (p.U x) (p.H x) (p.Hx x) (p.Hη x))
      0 X volume / (X * p.H X) =
      -p.W X + ((1 - h) * p.I X - axialExponent h * η * p.Iη X -
        coordinateFactor η * p.Jη X + 2 * (h - axialExponent h) * η * p.J X) /
          (X * p.H X) := by
  rw [angular_integrated_identity p hint]
  unfold angularPrimitive
  field_simp; ring



theorem axial_integrated_lag
    {h η X : ℝ} (p : AxialMomentData h η X) (hX : X ≠ 0)
    (hint : IntervalIntegrable
      (fun x => axialSource h η x (p.W x) (p.U x) (p.Ux x) (p.Uη x)
        (p.P x) (p.Px x) (p.Pη x)) volume 0 X) :
    intervalIntegral
      (fun x => axialSource h η x (p.W x) (p.U x) (p.Ux x) (p.Uη x)
        (p.P x) (p.Px x) (p.Pη x)) 0 X volume / X =
      -p.W X * p.U X + axialExponent h * (p.M X - η * p.Mη X) / X +
        (4 * h * η * p.S X - coordinateFactor η * p.Sη X) / X +
        4 * velocityExponent h * η * p.P X - coordinateFactor η * p.Pη X := by
  rw [axial_integrated_identity p hint]
  unfold axialPrimitive
  field_simp; ring



theorem angular_source_logarithmic_form
    (h η x W U H Hx Hη : ℝ) (hH : H ≠ 0) :
    H * (-W * (x * Hx / H) - h * (1 - 2 * η * U) -
      (axialExponent h * η + coordinateFactor η * U) * (Hη / H)) =
      angularSource h η x W U H Hx Hη := by
  unfold angularSource
  field_simp



theorem angular_lag_primitive_iff
    (H Q : ℝ → ℝ) (x Hx Qx Sq : ℝ)
    (hH : HasDerivAt H Hx x) (hQ : HasDerivAt Q Qx x) (hHne : H x ≠ 0) :
    HasDerivAt (fun y => y * H y * Q y) (H x * Sq) x ↔
      x * Qx + (1 + x * Hx / H x) * Q x = Sq := by
  have hd := ((hasDerivAt_id x).mul hH).mul hQ
  have hcalc : (1 * H x + x * Hx) * Q x + x * H x * Qx =
      H x * (x * Qx + (1 + x * Hx / H x) * Q x) := by
    field_simp; ring
  constructor
  · intro hp
    have heq := hd.unique hp
    simp only [Pi.mul_apply, id_eq] at heq
    rw [hcalc] at heq
    exact (mul_left_cancel₀ hHne) heq
  · intro hlag
    apply hd.congr_deriv
    simp only [Pi.mul_apply, id_eq]
    rw [hcalc, hlag]


theorem axial_lag_primitive_iff
    (N : ℝ → ℝ) (x Nx Sn : ℝ) (hN : HasDerivAt N Nx x) :
    HasDerivAt (fun y => y * N y) Sn x ↔ x * Nx + N x = Sn := by
  have hd := (hasDerivAt_id x).mul hN
  constructor
  · intro hp
    simpa only [Pi.mul_apply, Pi.sub_apply, id_eq, one_mul, add_comm] using hd.unique hp
  · intro hlag
    apply hd.congr_deriv
    simpa only [Pi.mul_apply, Pi.sub_apply, id_eq, one_mul, add_comm] using hlag



theorem stressFree_angular_lag_algebra
    (x L φ φx φxx : ℝ) (hφ : φ ≠ 0) :
    x * (-2 * L * (φxx * φ - φx ^ 2) / φ ^ 2) +
      (2 + x * φx / φ) * (-2 * L * φx / φ) =
      -2 * L * (x * φxx + 2 * φx) / φ := by
  field_simp; ring


theorem stressFree_axial_lag_algebra (x L Ux Uxx : ℝ) :
    x * (-2 * L * Uxx) + (-2 * L * Ux) = -2 * L * (x * Uxx + Ux) := by
  ring



theorem axial_stress_coefficient
    (x R E L Ns Ux : ℝ) (hR : R ≠ 0) (hE : E ≠ 0) (hL : L ≠ 0) :
    (E / R) * (x * Ns / (L * E) + 2 * x * Ux / E) =
      (x / R) * (Ns / L + 2 * Ux) := by
  field_simp



theorem angular_stress_coefficient
    (x R E L Qs Ex : ℝ) (hR : R ≠ 0) (hE : E ≠ 0) (hL : L ≠ 0) :
    (E / R) * (x * Qs / L - (1 - 2 * x * Ex / E)) =
      (E / R) * (x * Qs / L) + (2 * x * Ex - E) / R := by
  field_simp; ring

end NavierStokes.StressAlgebra
