import Mathlib

namespace CRPI

/-- The paper's common closed, real-valued score interval. -/
def Bounded (x : ℝ) : Prop := 0 ≤ x ∧ x ≤ 1

theorem bounded_complement {x : ℝ} (hx : Bounded x) :
    Bounded (1 - x) := by
  rcases hx with ⟨hx0, hx1⟩
  constructor
  · linarith
  · linarith

theorem bounded_mul {x y : ℝ} (hx : Bounded x) (hy : Bounded y) :
    Bounded (x * y) := by
  rcases hx with ⟨hx0, hx1⟩
  rcases hy with ⟨hy0, hy1⟩
  constructor
  · exact mul_nonneg hx0 hy0
  · have h : 0 ≤ (1 - x) * y := mul_nonneg (by linarith) hy0
    nlinarith

/-- A finite weighted sum; paper profiles require nonnegative normalized weights. -/
def weightedSum {ι : Type*} (s : Finset ι) (w x : ι → ℝ) : ℝ :=
  ∑ i ∈ s, w i * x i

theorem weightedSum_bounded {ι : Type*} (s : Finset ι)
    (w x : ι → ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i)
    (hsum : (∑ i ∈ s, w i) = 1)
    (hx : ∀ i ∈ s, Bounded (x i)) :
    Bounded (weightedSum s w x) := by
  change 0 ≤ (∑ i ∈ s, w i * x i) ∧
    (∑ i ∈ s, w i * x i) ≤ 1
  constructor
  · apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw i hi) (hx i hi).1
  · have hle : (∑ i ∈ s, w i * x i) ≤ (∑ i ∈ s, w i) := by
      apply Finset.sum_le_sum
      intro i hi
      have h : 0 ≤ w i * (1 - x i) :=
        mul_nonneg (hw i hi) (by linarith [(hx i hi).2])
      nlinarith
    linarith

end CRPI
