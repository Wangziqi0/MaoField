import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring










namespace NavierStokes.CurlGeometry

abbrev Vec3 (R : Type*) := Fin 3 → R

def dot {R : Type*} [CommRing R] (u v : Vec3 R) : R :=
  u 0 * v 0 + u 1 * v 1 + u 2 * v 2

def cross {R : Type*} [CommRing R] (u v : Vec3 R) : Vec3 R :=
  ![u 1 * v 2 - u 2 * v 1,
    u 2 * v 0 - u 0 * v 2,
    u 0 * v 1 - u 1 * v 0]

theorem cross_perpendicular_left {R : Type*} [CommRing R] (u v : Vec3 R) :
    dot u (cross u v) = 0 := by
  simp only [dot, cross, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val]
  ring

theorem cross_perpendicular_right {R : Type*} [CommRing R] (u v : Vec3 R) :
    dot v (cross u v) = 0 := by
  simp only [dot, cross, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val]
  ring


theorem triple_product {R : Type*} [CommRing R] (n a : Vec3 R) :
    cross n (cross n a) = dot n a • n - dot n n • a := by
  funext j
  fin_cases j <;> simp [cross, dot] <;> ring


theorem tangent_double_cross {R : Type*} [CommRing R] (n a : Vec3 R)
    (ha : dot n a = 0) :
    cross n (cross n a) = -(dot n n • a) := by
  rw [triple_product, ha, zero_smul, zero_sub]

theorem cross_smul {R : Type*} [CommRing R] (s t : R) (u v : Vec3 R) :
    cross (s • u) (t • v) = (s * t) • cross u v := by
  funext j
  fin_cases j <;> simp [cross] <;> ring


theorem real_dot_self_ne_zero {n : Vec3 ℝ} (hn : n ≠ 0) : dot n n ≠ 0 := by
  intro h
  have h0 : n 0 = 0 := by
    dsimp [dot] at h
    nlinarith [sq_nonneg (n 0), sq_nonneg (n 1), sq_nonneg (n 2)]
  have h1 : n 1 = 0 := by
    dsimp [dot] at h
    nlinarith [sq_nonneg (n 0), sq_nonneg (n 1), sq_nonneg (n 2)]
  have h2 : n 2 = 0 := by
    dsimp [dot] at h
    nlinarith [sq_nonneg (n 0), sq_nonneg (n 1), sq_nonneg (n 2)]
  apply hn
  funext j
  fin_cases j <;> simp_all


theorem normalized_double_cross {R : Type*} [Field R] (n a : Vec3 R)
    (hn : dot n n ≠ 0) (ha : dot n a = 0) :
    (-1 / dot n n) • cross n (cross n a) = a := by
  rw [tangent_double_cross n a ha]
  funext j
  simp only [Pi.smul_apply, Pi.neg_apply, smul_eq_mul]
  field_simp

noncomputable def curlSymbol (ξ A : Vec3 ℂ) : Vec3 ℂ :=
  cross (Complex.I • ξ) A



noncomputable def potentialCoefficient (k : ℂ) (n a : Vec3 ℂ) : Vec3 ℂ :=
  (Complex.I / (k * dot n n)) • cross n a



theorem principal_symbol_realizes (k : ℂ) (n a : Vec3 ℂ)
    (hk : k ≠ 0) (hn : dot n n ≠ 0) (ha : dot n a = 0) :
    curlSymbol (k • n) (potentialCoefficient k n a) = a := by
  unfold curlSymbol potentialCoefficient
  rw [smul_smul, cross_smul]
  have hs : (Complex.I * k) * (Complex.I / (k * dot n n)) =
      -1 / dot n n := by
    calc
      _ = (Complex.I * Complex.I) * (k / (k * dot n n)) := by ring
      _ = _ := by rw [Complex.I_mul_I]; field_simp
  rw [hs]
  exact normalized_double_cross n a hn ha

def complexify (n : Vec3 ℝ) : Vec3 ℂ := fun j => (n j : ℂ)

theorem complexify_dot_self (n : Vec3 ℝ) :
    dot (complexify n) (complexify n) = ((dot n n : ℝ) : ℂ) := by
  simp [complexify, dot]



theorem real_normal_principal_symbol (k : ℝ) (n : Vec3 ℝ) (a : Vec3 ℂ)
    (hk : k ≠ 0) (hn : n ≠ 0) (ha : dot (complexify n) a = 0) :
    curlSymbol ((k : ℂ) • complexify n)
      (potentialCoefficient k (complexify n) a) = a := by
  apply principal_symbol_realizes (k : ℂ) (complexify n) a
    (Complex.ofReal_ne_zero.mpr hk) ?_ ha
  rw [complexify_dot_self]
  exact Complex.ofReal_ne_zero.mpr (real_dot_self_ne_zero hn)

theorem curl_symbol_transverse (ξ A : Vec3 ℂ) : dot ξ (curlSymbol ξ A) = 0 := by
  unfold curlSymbol
  have h := cross_smul Complex.I (1 : ℂ) ξ A
  simp only [one_smul, mul_one] at h
  rw [h]
  simp only [dot, Pi.smul_apply, smul_eq_mul]
  have hp := cross_perpendicular_left ξ A
  dsimp [dot] at hp
  calc
    _ = Complex.I * (ξ 0 * cross ξ A 0 + ξ 1 * cross ξ A 1 + ξ 2 * cross ξ A 2) := by
      ring
    _ = 0 := by rw [hp, mul_zero]










def cylindricalCurl {F : Type*} [CommRing F]
    (Dr Dθ Dz : F →+ F) (q : F) (A : Vec3 F) : Vec3 F :=
  ![q * Dθ (A 2) - Dz (A 1),
    Dz (A 0) - Dr (A 2),
    Dr (A 1) + q * A 1 - q * Dθ (A 0)]

def cylindricalDiv {F : Type*} [CommRing F]
    (Dr Dθ Dz : F →+ F) (q : F) (v : Vec3 F) : F :=
  Dr (v 0) + q * v 0 + q * Dθ (v 1) + Dz (v 2)



theorem cylindrical_div_curl {F : Type*} [CommRing F]
    (Dr Dθ Dz : F →+ F) (q : F)
    (hrr : ∀ f, Dr (q * f) = q * Dr f - q ^ 2 * f)
    (hzq : ∀ f, Dz (q * f) = q * Dz f)
    (hrθ : ∀ f, Dr (Dθ f) = Dθ (Dr f))
    (hrz : ∀ f, Dr (Dz f) = Dz (Dr f))
    (hθz : ∀ f, Dθ (Dz f) = Dz (Dθ f))
    (A : Vec3 F) : cylindricalDiv Dr Dθ Dz q (cylindricalCurl Dr Dθ Dz q A) = 0 := by
  simp only [cylindricalDiv, cylindricalCurl, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val, map_sub, map_add]
  rw [hrr, hzq, hzq, hrθ, hrz, hθz]
  ring

end NavierStokes.CurlGeometry
