import CRPI.Consequence

namespace CRPI

/-- M = SOE * (m0 + (1 - m0) * CM). -/
def mitigation (soe cm m0 : ℝ) : ℝ :=
  soe * (m0 + (1 - m0) * cm)

theorem mitigation_bounded {soe cm m0 : ℝ}
    (hsoe : Bounded soe)
    (hcm : Bounded cm)
    (hm0 : Bounded m0) :
    Bounded (mitigation soe cm m0) := by
  have hblend : Bounded (m0 + (1 - m0) * cm) := by
    rcases hm0 with ⟨hm0_nonneg, hm0_le⟩
    rcases hcm with ⟨hcm_nonneg, hcm_le⟩
    constructor
    · have h : 0 ≤ (1 - m0) * cm :=
        mul_nonneg (by linarith) hcm_nonneg
      linarith
    · have h : 0 ≤ (1 - m0) * (1 - cm) :=
        mul_nonneg (by linarith) (by linarith)
      nlinarith
  exact bounded_mul hsoe hblend

/-- R_inst = H * (1 - M). -/
def instantaneousResidual (h m : ℝ) : ℝ := h * (1 - m)

theorem instantaneousResidual_bounded {h m : ℝ}
    (hh : Bounded h) (hm : Bounded m) :
    Bounded (instantaneousResidual h m) := by
  exact bounded_mul hh (bounded_complement hm)

end CRPI
