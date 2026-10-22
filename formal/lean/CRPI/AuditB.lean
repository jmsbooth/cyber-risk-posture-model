import CRPI

/-!
Run: lake env lean CRPI/AuditB.lean
Phase B theorem-level axiom ledger. Passing the compiler and the audit is
required before any candidate is labeled verified.
-/

#print axioms CRPI.regularizedBase_bounds
#print axioms CRPI.regularizedProduct_bounds
#print axioms CRPI.regularizedGeometric_bounded
#print axioms CRPI.regularizedGeometric_zero
#print axioms CRPI.regularizedGeometric_one
#print axioms CRPI.regularizedProduct_zero_weight_irrelevance
#print axioms CRPI.regularizedGeometric_zero_weight_irrelevance
#print axioms CRPI.regularizedGeometric_mono
#print axioms CRPI.regularizedGeometric_strictMono
#print axioms CRPI.regularizedGeometric_pos_of_positive_component
#print axioms CRPI.domainResilience_bounded
#print axioms CRPI.effectiveConsequence_mono_domain
#print axioms CRPI.effectiveConsequence_antitone_resilience
#print axioms CRPI.hazard_mono_threat
#print axioms CRPI.hazard_mono_consequence
#print axioms CRPI.mitigation_mono_usom
#print axioms CRPI.mitigation_mono_cm
#print axioms CRPI.instantaneousResidual_mono_hazard
#print axioms CRPI.instantaneousResidual_antitone_mitigation
#print axioms CRPI.currentResidual_mono_threat
#print axioms CRPI.currentResidual_mono_domain
#print axioms CRPI.currentResidual_antitone_resilience
#print axioms CRPI.currentResidual_antitone_usom
#print axioms CRPI.currentResidual_antitone_cm
