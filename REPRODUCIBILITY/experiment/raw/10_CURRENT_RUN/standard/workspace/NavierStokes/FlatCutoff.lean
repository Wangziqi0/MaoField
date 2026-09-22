import Mathlib.Analysis.SpecialFunctions.SmoothTransition
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring













noncomputable section

open Filter Topology Polynomial

namespace NavierStokes.FlatCutoff


def edge (c x : ℝ) : ℝ :=
  if x ≤ 0 then 0 else Real.exp (-c / x ^ 2)

theorem edge_of_nonpos (c : ℝ) {x : ℝ} (hx : x ≤ 0) : edge c x = 0 := by
  simp [edge, hx]

@[simp] theorem edge_zero (c : ℝ) : edge c 0 = 0 := edge_of_nonpos c le_rfl

theorem edge_of_pos (c : ℝ) {x : ℝ} (hx : 0 < x) :
    edge c x = Real.exp (-c / x ^ 2) := by
  simp [edge, not_le_of_gt hx]

theorem edge_nonneg (c x : ℝ) : 0 ≤ edge c x := by
  by_cases hx : x ≤ 0
  · simp [edge, hx]
  · rw [edge, ite_eq_right hx]
    exact (Real.exp_pos _).le

theorem edge_pos (c : ℝ) {x : ℝ} (hx : 0 < x) : 0 < edge c x := by
  rw [edge_of_pos c hx]
  exact Real.exp_pos _



theorem edge_le_glue {c x : ℝ} (hxc : x ≤ c) :
    edge c x ≤ expNegInvGlue x := by
  by_cases hx : x ≤ 0
  · rw [edge_of_nonpos c hx, expNegInvGlue.zero_of_nonpos hx]
  · have hx' : 0 < x := lt_of_not_ge hx
    rw [edge_of_pos c hx']
    simp only [expNegInvGlue, ite_eq_right hx]
    apply Real.exp_le_exp.mpr
    have hi : x⁻¹ ≤ c / x ^ 2 := by
      apply (le_div_iff₀ (sq_pos_of_pos hx')).2
      calc
        x⁻¹ * x ^ 2 = x := by field_simp
        _ ≤ c := hxc
    simpa only [neg_div] using neg_le_neg hi


def polynomialEdge (c : ℝ) (p : ℝ[X]) (x : ℝ) : ℝ :=
  p.eval x⁻¹ * edge c x

@[simp] theorem polynomialEdge_zero (c : ℝ) (p : ℝ[X]) :
    polynomialEdge c p 0 = 0 := by simp [polynomialEdge]



theorem polynomialEdge_tendsto_zero {c : ℝ} (hc : 0 < c) (p : ℝ[X]) :
    Tendsto (polynomialEdge c p) (𝓝 0) (𝓝 0) := by
  apply squeeze_zero_norm'
    (a := fun x : ℝ => ‖p.eval x⁻¹ * expNegInvGlue x‖)
  · filter_upwards [gt_mem_nhds hc] with x hxc
    simp only [polynomialEdge, norm_mul, Real.norm_eq_abs,
      abs_of_nonneg (edge_nonneg c x), abs_of_nonneg (expNegInvGlue.nonneg x)]
    exact mul_le_mul_of_nonneg_left (edge_le_glue hxc.le) (abs_nonneg _)
  · simpa only [norm_zero] using (expNegInvGlue.tendsto_polynomial_inv_mul_zero p).norm



def derivativePolynomial (c : ℝ) (p : ℝ[X]) : ℝ[X] :=
  C (2 * c) * X ^ 3 * p - X ^ 2 * p.derivative

theorem polynomialEdge_hasDerivAt {c : ℝ} (hc : 0 < c) (p : ℝ[X]) (x : ℝ) :
    HasDerivAt (polynomialEdge c p)
      (polynomialEdge c (derivativePolynomial c p) x) x := by
  rcases lt_trichotomy x 0 with hx | rfl | hx
  · rw [polynomialEdge, edge_of_nonpos c hx.le, mul_zero]
    refine (hasDerivAt_const x 0).congr_of_eventuallyEq ?_
    filter_upwards [gt_mem_nhds hx] with y hy
    simp [polynomialEdge, edge_of_nonpos c hy.le]
  · rw [polynomialEdge_zero, hasDerivAt_iff_tendsto_slope]
    refine ((polynomialEdge_tendsto_zero hc (p * X)).mono_left inf_le_left).congr ?_
    intro x
    simp [slope_def_field, polynomialEdge, div_eq_mul_inv, mul_right_comm]
  · have hinv : HasDerivAt (fun y : ℝ => y⁻¹) (-(x ^ 2)⁻¹) x :=
      hasDerivAt_inv hx.ne'
    have hpoly := (p.hasDerivAt x⁻¹).comp x hinv
    have hexp := (((hinv.pow 2).const_mul (-c)).exp)
    have hprod := hpoly.mul hexp
    convert! hprod.congr_of_eventuallyEq ?_ using 1
    · simp [polynomialEdge, derivativePolynomial, edge_of_pos c hx, inv_pow,
        div_eq_mul_inv]
      ring
    · filter_upwards [lt_mem_nhds hx] with y hy
      simp [polynomialEdge, edge_of_pos c hy, div_eq_mul_inv, inv_pow]

theorem polynomialEdge_differentiable {c : ℝ} (hc : 0 < c) (p : ℝ[X]) :
    Differentiable ℝ (polynomialEdge c p) :=
  fun x => (polynomialEdge_hasDerivAt hc p x).differentiableAt


theorem polynomialEdge_contDiff {c : ℝ} (hc : 0 < c) (p : ℝ[X]) {n : ℕ∞} :
    ContDiff ℝ n (polynomialEdge c p) := by
  apply contDiff_all_iff_nat.2 (fun m => ?_) n
  induction m generalizing p with
  | zero => exact contDiff_zero.2 (polynomialEdge_differentiable hc p).continuous
  | succ m ih =>
    rw [show ((m + 1 : ℕ) : WithTop ℕ∞) = m + 1 from rfl]
    refine contDiff_succ_iff_deriv.2 ⟨polynomialEdge_differentiable hc p, by simp, ?_⟩
    convert! ih (derivativePolynomial c p) using 2
    funext x
    exact (polynomialEdge_hasDerivAt hc p x).deriv


theorem edge_contDiff {c : ℝ} (hc : 0 < c) {n : ℕ∞} : ContDiff ℝ n (edge c) := by
  convert! polynomialEdge_contDiff hc (1 : ℝ[X]) (n := n) using 1
  funext x
  simp [polynomialEdge]


def jetPolynomial (c : ℝ) (p : ℝ[X]) : ℕ → ℝ[X]
  | 0 => p
  | m + 1 => derivativePolynomial c (jetPolynomial c p m)

theorem iteratedDeriv_polynomialEdge {c : ℝ} (hc : 0 < c) (p : ℝ[X]) (m : ℕ) :
    iteratedDeriv m (polynomialEdge c p) = polynomialEdge c (jetPolynomial c p m) := by
  induction m with
  | zero => simp [jetPolynomial]
  | succ m ih =>
    rw [iteratedDeriv_succ, ih]
    funext x
    exact (polynomialEdge_hasDerivAt hc (jetPolynomial c p m) x).deriv

@[simp] theorem polynomialEdge_one (c : ℝ) : polynomialEdge c 1 = edge c := by
  funext x
  simp [polynomialEdge]


theorem iteratedDeriv_edge_zero {c : ℝ} (hc : 0 < c) (m : ℕ) :
    iteratedDeriv m (edge c) 0 = 0 := by
  rw [← polynomialEdge_one c, iteratedDeriv_polynomialEdge hc 1 m]
  exact polynomialEdge_zero c _


theorem polynomialEdge_div_pow (c : ℝ) (p : ℝ[X]) (loss : ℕ) :
    (fun x => polynomialEdge c p x / x ^ loss) = polynomialEdge c (p * X ^ loss) := by
  funext x
  simp [polynomialEdge, div_eq_mul_inv, inv_pow, mul_assoc, mul_comm]


theorem edge_div_pow_contDiff {c : ℝ} (hc : 0 < c) (loss : ℕ) {n : ℕ∞} :
    ContDiff ℝ n (fun x => edge c x / x ^ loss) := by
  rw [← polynomialEdge_one c, polynomialEdge_div_pow]
  exact polynomialEdge_contDiff hc _


theorem weighted_iteratedDeriv_contDiff {c : ℝ} (hc : 0 < c)
    (m loss : ℕ) {n : ℕ∞} :
    ContDiff ℝ n (fun x => iteratedDeriv m (edge c) x / x ^ loss) := by
  rw [← polynomialEdge_one c, iteratedDeriv_polynomialEdge hc 1 m,
    polynomialEdge_div_pow]
  exact polynomialEdge_contDiff hc _



theorem weighted_iteratedDeriv_tendsto_zero {c : ℝ} (hc : 0 < c) (m loss : ℕ) :
    Tendsto (fun x => iteratedDeriv m (edge c) x / x ^ loss) (𝓝 0) (𝓝 0) := by
  rw [← polynomialEdge_one c, iteratedDeriv_polynomialEdge hc 1 m,
    polynomialEdge_div_pow]
  exact polynomialEdge_tendsto_zero hc _



theorem edge_div_edge (c d : ℝ) :
    (fun x => edge c x / edge d x) = edge (c - d) := by
  funext x
  by_cases hx : x ≤ 0
  · simp [edge, hx]
  · simp only [edge, ite_eq_right hx, ← Real.exp_sub]
    congr 1
    ring

theorem edge_quotient_contDiff {c d : ℝ} (hdc : d < c) {n : ℕ∞} :
    ContDiff ℝ n (fun x => edge c x / edge d x) := by
  rw [edge_div_edge]
  exact edge_contDiff (sub_pos.mpr hdc)

end NavierStokes.FlatCutoff
