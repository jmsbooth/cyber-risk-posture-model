import CRPI.Envelope

/-!
# CRPI regularized geometric aggregation

This is an independent finite-index real-valued formalization of the exact
operator in the Governing Model. No constant epsilon or two-input restriction
is introduced. Phase B does not change the equations.
-/

namespace CRPI

/-- The positive regularized base ε + (1 - ε) xᵢ. -/
def regularizedBase (ε x : ℝ) : ℝ := ε + (1 - ε) * x

/-- The weighted product in the manuscript's geometric operator. -/
noncomputable def regularizedProduct {ι : Type*} (s : Finset ι)
    (ε : ℝ) (w x : ι → ℝ) : ℝ :=
  ∏ i ∈ s, (regularizedBase ε (x i)) ^ (w i)

/-- G_ε(x,w) = (∏ (ε + (1 - ε)xᵢ)^wᵢ - ε)/(1 - ε). -/
noncomputable def regularizedGeometric {ι : Type*} (s : Finset ι)
    (ε : ℝ) (w x : ι → ℝ) : ℝ :=
  (regularizedProduct s ε w x - ε) / (1 - ε)

theorem regularizedBase_bounds {ε x : ℝ}
    (hε0 : 0 < ε) (hε1 : ε < 1) (hx : Bounded x) :
    ε ≤ regularizedBase ε x ∧ regularizedBase ε x ≤ 1 := by
  rcases hx with ⟨hx0, hx1⟩
  have hc : 0 ≤ 1 - ε := by linarith
  have hlo : 0 ≤ (1 - ε) * x := mul_nonneg hc hx0
  have hhi : 0 ≤ (1 - ε) * (1 - x) :=
    mul_nonneg hc (by linarith)
  unfold regularizedBase
  constructor
  · linarith
  · nlinarith

/-- For normalized nonnegative weights, the product is in [ε,1]. -/
theorem regularizedProduct_bounds {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hsum : (∑ i ∈ s, w i) = 1)
    (hx : ∀ i ∈ s, Bounded (x i)) :
    ε ≤ regularizedProduct s ε w x ∧
      regularizedProduct s ε w x ≤ 1 := by
  have hlo :
      (∏ i ∈ s, ε ^ (w i)) ≤
        (∏ i ∈ s, (regularizedBase ε (x i)) ^ (w i)) := by
    apply Finset.prod_le_prod₀
    · intro i hi
      exact Real.rpow_nonneg (le_of_lt hε0) (w i)
    · intro i hi
      exact Real.rpow_le_rpow (le_of_lt hε0)
        (regularizedBase_bounds hε0 hε1 (hx i hi)).1 (hw i hi)
  have hlowProduct :
      ε ≤ regularizedProduct s ε w x := by
    have hnormal : (∏ i ∈ s, ε ^ (w i)) = ε := by
      rw [← Real.rpow_sum_of_pos hε0 w s, hsum, Real.rpow_one]
    rw [hnormal] at hlo
    exact hlo
  have hupper :
      (∏ i ∈ s, (regularizedBase ε (x i)) ^ (w i)) ≤
        (∏ i ∈ s, (1 : ℝ) ^ (w i)) := by
    apply Finset.prod_le_prod₀
    · intro i hi
      have hp : 0 < regularizedBase ε (x i) :=
        lt_of_lt_of_le hε0
          (regularizedBase_bounds hε0 hε1 (hx i hi)).1
      exact Real.rpow_nonneg (le_of_lt hp) (w i)
    · intro i hi
      have hp : 0 ≤ regularizedBase ε (x i) :=
        le_trans (le_of_lt hε0)
          (regularizedBase_bounds hε0 hε1 (hx i hi)).1
      exact Real.rpow_le_rpow hp
        (regularizedBase_bounds hε0 hε1 (hx i hi)).2
        (hw i hi)
  constructor
  · exact hlowProduct
  · have : (∏ i ∈ s, (regularizedBase ε (x i)) ^ (w i)) ≤ 1 := by
      simpa using hupper
    exact this

theorem regularizedGeometric_bounded {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hsum : (∑ i ∈ s, w i) = 1)
    (hx : ∀ i ∈ s, Bounded (x i)) :
    Bounded (regularizedGeometric s ε w x) := by
  have hp := regularizedProduct_bounds s ε w x hε0 hε1 hw hsum hx
  have hd : 0 < 1 - ε := by linarith
  unfold regularizedGeometric
  constructor
  · exact div_nonneg (by linarith [hp.1]) (le_of_lt hd)
  · apply (div_le_iff₀ hd).2
    linarith [hp.2]

/-- All-zero input returns zero, even when some weights vanish. -/
theorem regularizedGeometric_zero {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hsum : (∑ i ∈ s, w i) = 1) :
    regularizedGeometric s ε w (fun _ => 0) = 0 := by
  have hp : regularizedProduct s ε w (fun _ => 0) = ε := by
    unfold regularizedProduct
    have hbase :
        (∏ i ∈ s, (regularizedBase ε (0 : ℝ)) ^ (w i)) =
          (∏ i ∈ s, ε ^ (w i)) := by
      apply Finset.prod_congr rfl
      intro i hi
      simp [regularizedBase]
    rw [hbase, ← Real.rpow_sum_of_pos hε0 w s, hsum, Real.rpow_one]
  simp [regularizedGeometric, hp]

/-- All-one input returns one for any normalized weights. -/
theorem regularizedGeometric_one {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w : ι → ℝ)
    (hε1 : ε < 1) :
    regularizedGeometric s ε w (fun _ => 1) = 1 := by
  have hbase : regularizedBase ε (1 : ℝ) = 1 := by
    unfold regularizedBase
    ring
  have hp : regularizedProduct s ε w (fun _ => 1) = 1 := by
    simp [regularizedProduct, hbase]
  have hd : 1 - ε ≠ 0 := ne_of_gt (by linarith : 0 < 1 - ε)
  simp [regularizedGeometric, hp, hd]

/-- Changes confined to zero-weight coordinates cannot affect the product. -/
theorem regularizedProduct_zero_weight_irrelevance {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x y : ι → ℝ)
    (hxy : ∀ i ∈ s, w i ≠ 0 → x i = y i) :
    regularizedProduct s ε w x = regularizedProduct s ε w y := by
  unfold regularizedProduct
  apply Finset.prod_congr rfl
  intro i hi
  by_cases hwi : w i = 0
  · simp [hwi]
  · rw [hxy i hi hwi]

theorem regularizedGeometric_zero_weight_irrelevance {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x y : ι → ℝ)
    (hxy : ∀ i ∈ s, w i ≠ 0 → x i = y i) :
    regularizedGeometric s ε w x =
      regularizedGeometric s ε w y := by
  unfold regularizedGeometric
  rw [regularizedProduct_zero_weight_irrelevance s ε w x y hxy]

/-- Monotonicity holds in every normalized component with nonnegative weight. -/
theorem regularizedGeometric_mono {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x y : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hx : ∀ i ∈ s, Bounded (x i))
    (hxy : ∀ i ∈ s, x i ≤ y i) :
    regularizedGeometric s ε w x ≤
      regularizedGeometric s ε w y := by
  have hprod : regularizedProduct s ε w x ≤
      regularizedProduct s ε w y := by
    unfold regularizedProduct
    apply Finset.prod_le_prod₀
    · intro i hi
      have hb := regularizedBase_bounds hε0 hε1 (hx i hi)
      exact Real.rpow_nonneg (le_trans (le_of_lt hε0) hb.1) (w i)
    · intro i hi
      have hb := regularizedBase_bounds hε0 hε1 (hx i hi)
      apply Real.rpow_le_rpow (le_trans (le_of_lt hε0) hb.1) ?_
        (hw i hi)
      unfold regularizedBase
      have hc : 0 ≤ 1 - ε := by linarith
      exact add_le_add_left
        (mul_le_mul_of_nonneg_left (hxy i hi) hc) ε
  have hd : 0 < 1 - ε := by linarith
  unfold regularizedGeometric
  apply (div_le_div_iff₀ hd hd).2
  have hm : 0 ≤
      (regularizedProduct s ε w y - regularizedProduct s ε w x) *
        (1 - ε) :=
    mul_nonneg (by linarith) (le_of_lt hd)
  nlinarith

/-- A positive-weight strict component improvement strictly raises G. -/
theorem regularizedGeometric_strictMono {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x y : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hx : ∀ i ∈ s, Bounded (x i))
    (hxy : ∀ i ∈ s, x i ≤ y i)
    (hstrict : ∃ i ∈ s, 0 < w i ∧ x i < y i) :
    regularizedGeometric s ε w x <
      regularizedGeometric s ε w y := by
  have hprod : regularizedProduct s ε w x <
      regularizedProduct s ε w y := by
    unfold regularizedProduct
    apply Finset.prod_lt_prod₀
    · intro i hi
      have hb := regularizedBase_bounds hε0 hε1 (hx i hi)
      exact Real.rpow_pos_of_pos (lt_of_lt_of_le hε0 hb.1) (w i)
    · intro i hi
      have hb := regularizedBase_bounds hε0 hε1 (hx i hi)
      apply Real.rpow_le_rpow (le_trans (le_of_lt hε0) hb.1) ?_
        (hw i hi)
      unfold regularizedBase
      have hc : 0 ≤ 1 - ε := by linarith
      exact add_le_add_left
        (mul_le_mul_of_nonneg_left (hxy i hi) hc) ε
    · obtain ⟨i, hi, hwi, hxi⟩ := hstrict
      refine ⟨i, hi, ?_⟩
      apply Real.rpow_lt_rpow
      · exact le_trans (le_of_lt hε0)
          (regularizedBase_bounds hε0 hε1 (hx i hi)).1
      · unfold regularizedBase
        have hc : 0 < 1 - ε := by linarith
        exact add_lt_add_left
          (mul_lt_mul_of_pos_left hxi hc) ε
      · exact hwi
  have hd : 0 < 1 - ε := by linarith
  unfold regularizedGeometric
  apply (div_lt_div_iff₀ hd hd).2
  have hm : 0 <
      (regularizedProduct s ε w y - regularizedProduct s ε w x) *
        (1 - ε) :=
    mul_pos (by linarith) hd
  nlinarith

/-- One zero component is not an absorbing zero when another positively
weighted component is positive. -/
theorem regularizedGeometric_pos_of_positive_component {ι : Type*}
    (s : Finset ι) (ε : ℝ) (w x : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hsum : (∑ i ∈ s, w i) = 1)
    (hx : ∀ i ∈ s, Bounded (x i))
    (hpos : ∃ i ∈ s, 0 < w i ∧ 0 < x i) :
    0 < regularizedGeometric s ε w x := by
  have hstrict : regularizedGeometric s ε w (fun _ => 0) <
      regularizedGeometric s ε w x :=
    regularizedGeometric_strictMono s ε w (fun _ => 0) x
      hε0 hε1 hw
      (by intro i hi; exact ⟨le_refl (0 : ℝ), zero_le_one⟩)
      (by intro i hi; exact (hx i hi).1) hpos
  simpa [regularizedGeometric_zero s ε w hε0 hε1 hsum]
    using hstrict

/-- A domain-specific resilience projection uses exactly the same G operator. -/
noncomputable def domainResilience {ι : Type*} (s : Finset ι)
    (ε : ℝ) (a y : ι → ℝ) : ℝ :=
  regularizedGeometric s ε a y

theorem domainResilience_bounded {ι : Type*}
    (s : Finset ι) (ε : ℝ) (a y : ι → ℝ)
    (hε0 : 0 < ε) (hε1 : ε < 1)
    (ha : ∀ i ∈ s, 0 ≤ a i)
    (hasum : (∑ i ∈ s, a i) = 1)
    (hy : ∀ i ∈ s, Bounded (y i)) :
    Bounded (domainResilience s ε a y) := by
  exact regularizedGeometric_bounded s ε a y hε0 hε1 ha hasum hy

end CRPI
