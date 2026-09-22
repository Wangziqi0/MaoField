import Mathlib.Analysis.Normed.Group.Continuity
import Mathlib.Analysis.Normed.Field.Basic
import Mathlib.Tactic.Ring












open Filter Topology

namespace NavierStokes.Flatness

variable {α : Type*} {l : Filter α} {q f g : α → ℝ}



def PowerFlat (l : Filter α) (q f : α → ℝ) : Prop :=
  ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧ ∀ᶠ x in l, |f x| ≤ C * |q x| ^ n




theorem fixed_power_loss_bound {x scale C : ℝ} {n loss : ℕ}
    (hscale : scale ≠ 0) (hx : |x| ≤ C * |scale| ^ (n + loss)) :
    |x / scale ^ loss| ≤ C * |scale| ^ n := by
  rw [abs_div, abs_pow]
  apply (div_le_iff₀ (pow_pos (abs_pos.mpr hscale) loss)).2
  simpa only [pow_add, mul_assoc] using hx


theorem PowerFlat.div_pow (hf : PowerFlat l q f)
    (hq : ∀ᶠ x in l, q x ≠ 0) (loss : ℕ) :
    PowerFlat l q (fun x => f x / q x ^ loss) := by
  intro n
  obtain ⟨C, hC, hbound⟩ := hf (n + loss)
  refine ⟨C, hC, ?_⟩
  filter_upwards [hq, hbound] with x hx hfx
  exact fixed_power_loss_bound hx hfx


theorem PowerFlat.add (hf : PowerFlat l q f) (hg : PowerFlat l q g) :
    PowerFlat l q (fun x => f x + g x) := by
  intro n
  obtain ⟨C, hC, hfb⟩ := hf n
  obtain ⟨D, hD, hgb⟩ := hg n
  refine ⟨C + D, add_nonneg hC hD, ?_⟩
  filter_upwards [hfb, hgb] with x hfx hgx
  calc
    |f x + g x| ≤ |f x| + |g x| := abs_add_le _ _
    _ ≤ C * |q x| ^ n + D * |q x| ^ n := add_le_add hfx hgx
    _ = (C + D) * |q x| ^ n := (add_mul _ _ _).symm



theorem PowerFlat.mul (hf : PowerFlat l q f) (hg : PowerFlat l q g) :
    PowerFlat l q (fun x => f x * g x) := by
  intro n
  obtain ⟨C, hC, hfb⟩ := hf n
  obtain ⟨D, hD, hgb⟩ := hg 0
  refine ⟨C * D, mul_nonneg hC hD, ?_⟩
  filter_upwards [hfb, hgb] with x hfx hgx
  have hgx' : |g x| ≤ D := by simpa only [pow_zero, mul_one] using hgx
  calc
    |f x * g x| = |f x| * |g x| := abs_mul _ _
    _ ≤ (C * |q x| ^ n) * D :=
      mul_le_mul hfx hgx' (abs_nonneg _) (mul_nonneg hC (pow_nonneg (abs_nonneg _) _))
    _ = (C * D) * |q x| ^ n := by ring




theorem PowerFlat.mul_of_power_bound (hf : PowerFlat l q f)
    (hq : ∀ᶠ x in l, q x ≠ 0) (loss : ℕ) {D : ℝ} (hD : 0 ≤ D)
    (hg : ∀ᶠ x in l, |g x| ≤ D / |q x| ^ loss) :
    PowerFlat l q (fun x => f x * g x) := by
  intro n
  obtain ⟨C, hC, hfb⟩ := hf (n + loss)
  refine ⟨C * D, mul_nonneg hC hD, ?_⟩
  filter_upwards [hq, hfb, hg] with x hqx hfx hgx
  have hden : |q x| ^ loss ≠ 0 := pow_ne_zero _ (abs_ne_zero.mpr hqx)
  calc
    |f x * g x| = |f x| * |g x| := abs_mul _ _
    _ ≤ (C * |q x| ^ (n + loss)) * (D / |q x| ^ loss) :=
      mul_le_mul hfx hgx (abs_nonneg _)
        (mul_nonneg hC (pow_nonneg (abs_nonneg _) _))
    _ = ((C * D) * |q x| ^ n) * (|q x| ^ loss / |q x| ^ loss) := by
      rw [pow_add]
      ring
    _ = (C * D) * |q x| ^ n := by rw [div_self hden, mul_one]




theorem powerFlat_of_stage_bounds {exponent : ℕ → ℕ} (loss : ℕ)
    (hexponent : ∀ n : ℕ, ∃ j : ℕ, n ≤ exponent j)
    (hq : ∀ᶠ x in l, |q x| ≤ 1)
    (hstage : ∀ j : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ᶠ x in l, |f x| ≤ C * |q x| ^ (exponent j - loss)) :
    PowerFlat l q f := by
  intro n
  obtain ⟨j, hj⟩ := hexponent (n + loss)
  obtain ⟨C, hC, hb⟩ := hstage j
  have hn : n ≤ exponent j - loss := Nat.le_sub_of_add_le hj
  refine ⟨C, hC, ?_⟩
  filter_upwards [hq, hb] with x hqx hfx
  exact hfx.trans (mul_le_mul_of_nonneg_left
    (pow_le_pow_of_le_one (abs_nonneg _) hqx hn) hC)



theorem PowerFlat.tendsto_zero (hf : PowerFlat l q f)
    (hq : Tendsto q l (𝓝 0)) : Tendsto f l (𝓝 0) := by
  obtain ⟨C, _, hb⟩ := hf 1
  apply squeeze_zero_norm' (f := f) (a := fun x => C * |q x|)
  · simpa only [Real.norm_eq_abs, pow_one] using hb
  · simpa only [abs_zero, mul_zero] using hq.abs.const_mul C


theorem PowerFlat.div_pow_tendsto_zero (hf : PowerFlat l q f)
    (hq : Tendsto q l (𝓝 0)) (hq_ne : ∀ᶠ x in l, q x ≠ 0) (loss : ℕ) :
    Tendsto (fun x => f x / q x ^ loss) l (𝓝 0) :=
  (hf.div_pow hq_ne loss).tendsto_zero hq

end NavierStokes.Flatness
