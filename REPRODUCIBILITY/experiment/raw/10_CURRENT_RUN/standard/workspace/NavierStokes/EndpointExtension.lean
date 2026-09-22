import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.ContDiff.Comp














noncomputable section

open Set
open scoped ContDiff

namespace NavierStokes.EndpointExtension


def glue {V : Type*} (a : ℝ) (left right : ℝ → V) (x : ℝ) : V :=
  if x ≤ a then left x else right x

theorem glue_eq_left {V : Type*} {a x : ℝ} {left right : ℝ → V} (hx : x ≤ a) :
    glue a left right x = left x := by
  simp only [glue, ite_eq_left hx]

theorem glue_eq_right {V : Type*} {a x : ℝ} {left right : ℝ → V} (hx : a < x) :
    glue a left right x = right x := by
  simp only [glue, ite_eq_right (not_le_of_gt hx)]



theorem glue_eqOn_right {V : Type*} {a : ℝ} {left right : ℝ → V}
    (hvalue : left a = right a) : EqOn (glue a left right) right (Ici a) := by
  intro x hx
  by_cases hxa : x ≤ a
  · have hEq : x = a := le_antisymm hxa hx
    subst x
    simpa only [glue, ite_eq_left le_rfl] using hvalue
  · simp only [glue, ite_eq_right hxa]


theorem glue_vanishes_from {V : Type*} [Zero V] {a b : ℝ} {left right : ℝ → V}
    (hab : a ≤ b) (hvalue : left a = right a)
    (hzero : ∀ x, b ≤ x → right x = 0) :
    ∀ x, b ≤ x → glue a left right x = 0 := by
  intro x hx
  rw [glue_eqOn_right hvalue (hab.trans hx)]
  exact hzero x hx

section Normed

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]



theorem hasDerivAt_glue {a : ℝ} {left right leftDeriv rightDeriv : ℝ → V}
    (hleft : ∀ x ≤ a, HasDerivWithinAt left (leftDeriv x) (Iic a) x)
    (hright : ∀ x, a ≤ x → HasDerivWithinAt right (rightDeriv x) (Ici a) x)
    (hvalue : left a = right a) (hderiv : leftDeriv a = rightDeriv a) (x : ℝ) :
    HasDerivAt (glue a left right) (glue a leftDeriv rightDeriv x) x := by
  have hL (y : ℝ) (hy : y ≤ a) :
      HasDerivWithinAt (glue a left right) (leftDeriv y) (Iic a) y :=
    (hleft y hy).congr_of_mem (fun z hz => glue_eq_left hz) hy
  have hR (y : ℝ) (hy : a ≤ y) :
      HasDerivWithinAt (glue a left right) (rightDeriv y) (Ici a) y :=
    (hright y hy).congr_of_mem (glue_eqOn_right hvalue) hy
  rcases lt_trichotomy x a with hlt | heq | hgt
  · simpa only [glue, ite_eq_left hlt.le] using (hL x hlt.le).hasDerivAt (Iic_mem_nhds hlt)
  · subst x
    have hright' : HasDerivWithinAt (glue a left right) (leftDeriv a) (Ici a) a := by
      rw [hderiv]
      exact hR a le_rfl
    have h := (hL a le_rfl).union hright'
    simpa only [Iic_union_Ici, hasDerivWithinAt_univ, glue, ite_eq_left le_rfl] using h
  · simpa only [glue, ite_eq_right (not_le_of_gt hgt)] using
      (hR x hgt.le).hasDerivAt (Ici_mem_nhds hgt)


def gluedJet (a : ℝ) (left right : ℝ → V) (n : ℕ) : ℝ → V :=
  glue a (iteratedDerivWithin n left (Iic a)) (iteratedDerivWithin n right (Ici a))



theorem hasDerivAt_gluedJet {a : ℝ} {left right : ℝ → V}
    (hleft : ContDiffOn ℝ ∞ left (Iic a))
    (hright : ContDiffOn ℝ ∞ right (Ici a))
    (hmatch : ∀ n : ℕ,
      iteratedDerivWithin n left (Iic a) a = iteratedDerivWithin n right (Ici a) a)
    (n : ℕ) (x : ℝ) :
    HasDerivAt (gluedJet a left right n) (gluedJet a left right (n + 1) x) x := by
  apply hasDerivAt_glue
  · intro y hy
    have hd := (hleft.differentiableOn_iteratedDerivWithin (m := n)
      (ENat.natCast_lt_of_coe_top_le_withTop le_rfl n)
      (uniqueDiffOn_Iic a) y hy).hasDerivWithinAt
    simpa only [iteratedDerivWithin_succ] using hd
  · intro y hy
    have hd := (hright.differentiableOn_iteratedDerivWithin (m := n)
      (ENat.natCast_lt_of_coe_top_le_withTop le_rfl n)
      (uniqueDiffOn_Ici a) y hy).hasDerivWithinAt
    simpa only [iteratedDerivWithin_succ] using hd
  · exact hmatch n
  · exact hmatch (n + 1)



theorem iteratedDeriv_glue {a : ℝ} {left right : ℝ → V}
    (hleft : ContDiffOn ℝ ∞ left (Iic a))
    (hright : ContDiffOn ℝ ∞ right (Ici a))
    (hmatch : ∀ n : ℕ,
      iteratedDerivWithin n left (Iic a) a = iteratedDerivWithin n right (Ici a) a)
    (n : ℕ) :
    iteratedDeriv n (glue a left right) = gluedJet a left right n := by
  induction n with
  | zero => simp only [iteratedDeriv_zero, gluedJet, iteratedDerivWithin_zero]
  | succ n ih =>
    rw [iteratedDeriv_succ, ih]
    funext x
    exact (hasDerivAt_gluedJet hleft hright hmatch n x).deriv



theorem contDiff_glue {a : ℝ} {left right : ℝ → V}
    (hleft : ContDiffOn ℝ ∞ left (Iic a))
    (hright : ContDiffOn ℝ ∞ right (Ici a))
    (hmatch : ∀ n : ℕ,
      iteratedDerivWithin n left (Iic a) a = iteratedDerivWithin n right (Ici a) a) :
    ContDiff ℝ ∞ (glue a left right) := by
  apply contDiff_of_differentiable_iteratedDeriv
  intro n _
  rw [iteratedDeriv_glue hleft hright hmatch n]
  intro x
  exact (hasDerivAt_gluedJet hleft hright hmatch n x).differentiableAt


theorem iteratedDeriv_glue_at_join {a : ℝ} {left right : ℝ → V}
    (hleft : ContDiffOn ℝ ∞ left (Iic a))
    (hright : ContDiffOn ℝ ∞ right (Ici a))
    (hmatch : ∀ n : ℕ,
      iteratedDerivWithin n left (Iic a) a = iteratedDerivWithin n right (Ici a) a)
    (n : ℕ) :
    iteratedDeriv n (glue a left right) a = iteratedDerivWithin n left (Iic a) a := by
  rw [iteratedDeriv_glue hleft hright hmatch n]
  exact glue_eq_left le_rfl


theorem iteratedDerivWithin_zero_curve (s : Set ℝ) (n : ℕ) :
    iteratedDerivWithin n (fun _ : ℝ => (0 : V)) s = fun _ => 0 := by
  induction n with
  | zero => simp only [iteratedDerivWithin_zero]
  | succ n ih =>
    funext x
    simp only [iteratedDerivWithin_succ, ih, derivWithin_fun_const, Pi.zero_apply]



theorem contDiff_zero_extension {a : ℝ} {left : ℝ → V}
    (hleft : ContDiffOn ℝ ∞ left (Iic a))
    (hflat : ∀ n : ℕ, iteratedDerivWithin n left (Iic a) a = 0) :
    ContDiff ℝ ∞ (glue a left (fun _ => 0)) := by
  apply contDiff_glue hleft contDiffOn_const
  intro n
  rw [hflat n, iteratedDerivWithin_zero_curve]

end Normed

end NavierStokes.EndpointExtension
