import CRPI.Mitigation

namespace CRPI

/-- CRPI is the conservative envelope of current residual and persistent state. -/
def envelope (residual stock : ℝ) : ℝ := max residual stock

theorem envelope_bounded {residual stock : ℝ}
    (hr : Bounded residual) (hs : Bounded stock) :
    Bounded (envelope residual stock) := by
  constructor
  · change 0 ≤ max residual stock
    exact le_trans hr.1 (le_max_left residual stock)
  · change max residual stock ≤ 1
    exact max_le hr.2 hs.2

theorem envelope_mono_residual {x y stock : ℝ}
    (hxy : x ≤ y) : envelope x stock ≤ envelope y stock := by
  unfold envelope
  apply max_le
  · exact le_trans hxy (le_max_left y stock)
  · exact le_max_right y stock

theorem envelope_mono_stock {residual x y : ℝ}
    (hxy : x ≤ y) : envelope residual x ≤ envelope residual y := by
  unfold envelope
  apply max_le
  · exact le_max_left residual y
  · exact le_trans hxy (le_max_right residual y)

end CRPI
