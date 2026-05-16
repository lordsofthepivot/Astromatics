import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

open BigOperators Real Finset

-- ================================================================
-- PROP 11 — Universal Alignment Lower Bound
-- ================================================================

lemma sq_sum_ge_sum_sq {n : ℕ} (v : Fin n → ℝ) (hnn : ∀ i, 0 ≤ v i) :
    (∑ i, v i) ^ 2 ≥ ∑ i, (v i) ^ 2 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Fin.sum_univ_castSucc, Fin.sum_univ_castSucc]
    set a := ∑ i : Fin n, v (Fin.castSucc i)
    set b := v (Fin.last n)
    have ha : 0 ≤ a := sum_nonneg (fun i _ => hnn _)
    have hb : 0 ≤ b := hnn _
    have ih' : a ^ 2 ≥ ∑ i : Fin n, (v (Fin.castSucc i)) ^ 2 :=
      ih (fun i => v (Fin.castSucc i)) (fun i => hnn _)
    nlinarith [sq_nonneg (a - b), mul_nonneg ha hb]

theorem prop11 (v : Fin 8 → ℝ)
    (hunit : ∑ i, (v i) ^ 2 = 1)
    (hnn : ∀ i, 0 ≤ v i) :
    ∑ i, v i ≥ 1 := by
  have key := sq_sum_ge_sum_sq v hnn
  rw [hunit] at key
  have hpos : 0 ≤ ∑ i : Fin 8, v i :=
    Finset.sum_nonneg (fun i _ => hnn i)
  nlinarith [sq_nonneg (∑ i : Fin 8, v i)]

-- ================================================================
-- COROLLARY 10 RETRACTION — 120° achievable within D8
-- ================================================================

theorem corollary10_retraction :
    ∃ (v₁ v₂ : Fin 8 → ℝ),
      (∑ i, (v₁ i) ^ 2 = 2) ∧
      (∑ i, (v₂ i) ^ 2 = 2) ∧
      (∑ i, v₁ i * v₂ i = -1) := by
  refine ⟨![1, 1, 0, 0, 0, 0, 0, 0], ![0, -1, 1, 0, 0, 0, 0, 0], ?_, ?_, ?_⟩
  · simp [Fin.sum_univ_eight]; norm_num
  · simp [Fin.sum_univ_eight]; norm_num
  · simp [Fin.sum_univ_eight]

-- ================================================================
-- ACTOR ROOTS — Valid E8 roots + Opposition Theorem
-- ================================================================

def rFORCE            : Fin 8 → ℝ := ![1, 1, 0, 0, 0, 0, 0, 0]
def rSTRUCTURE        : Fin 8 → ℝ := ![1, -1, 0, 0, 0, 0, 0, 0]
noncomputable def rSIGNAL    : Fin 8 → ℝ := ![1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2]
noncomputable def rIDENTITY  : Fin 8 → ℝ := ![1/2, 1/2, 1/2, 1/2, -1/2, -1/2, -1/2, -1/2]
noncomputable def rVALUE     : Fin 8 → ℝ := ![1/2, 1/2, -1/2, -1/2, 1/2, 1/2, -1/2, -1/2]

theorem actor_roots_valid :
    ∑ i, (rFORCE i) ^ 2     = 2 ∧
    ∑ i, (rSTRUCTURE i) ^ 2 = 2 ∧
    ∑ i, (rSIGNAL i) ^ 2    = 2 ∧
    ∑ i, (rIDENTITY i) ^ 2  = 2 ∧
    ∑ i, (rVALUE i) ^ 2     = 2 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;>
  simp [rFORCE, rSTRUCTURE, rSIGNAL, rIDENTITY, rVALUE, Fin.sum_univ_eight] <;>
  norm_num

theorem opposition_theorem :
    ∑ i, rFORCE i     * rSTRUCTURE i = 0 ∧
    ∑ i, rFORCE i     * rSIGNAL i    = 1 ∧
    ∑ i, rFORCE i     * rIDENTITY i  = 1 ∧
    ∑ i, rFORCE i     * rVALUE i     = 1 ∧
    ∑ i, rSTRUCTURE i * rSIGNAL i    = 0 ∧
    ∑ i, rSTRUCTURE i * rIDENTITY i  = 0 ∧
    ∑ i, rSTRUCTURE i * rVALUE i     = 0 ∧
    ∑ i, rSIGNAL i    * rIDENTITY i  = 0 ∧
    ∑ i, rSIGNAL i    * rVALUE i     = 0 ∧
    ∑ i, rIDENTITY i  * rVALUE i     = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
  simp [rFORCE, rSTRUCTURE, rSIGNAL, rIDENTITY, rVALUE, Fin.sum_univ_eight] <;>
  norm_num

-- ================================================================
-- ASPECT-E8 IDENTITY — Achievability + Cosine Correspondence
-- ================================================================

theorem aspect_e8_achievability :
    (∑ i : Fin 8, (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i *
                  (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i = 2) ∧
    (∑ i : Fin 8, (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i *
                  (![1,0,1,0,0,0,0,0] : Fin 8 → ℤ) i = 1) ∧
    (∑ i : Fin 8, (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i *
                  (![0,0,1,1,0,0,0,0] : Fin 8 → ℤ) i = 0) ∧
    (∑ i : Fin 8, (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i *
                  (![-1,0,1,0,0,0,0,0] : Fin 8 → ℤ) i = -1) ∧
    (∑ i : Fin 8, (![1,1,0,0,0,0,0,0] : Fin 8 → ℤ) i *
                  (![-1,-1,0,0,0,0,0,0] : Fin 8 → ℤ) i = -2) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp [Fin.sum_univ_eight]

theorem aspect_e8_cosines :
    cos 0       = (2:ℝ)/2 ∧
    cos (π/3)   = (1:ℝ)/2 ∧
    cos (π/2)   = (0:ℝ)/2 ∧
    cos (2*π/3) = (-1:ℝ)/2 ∧
    cos π       = (-2:ℝ)/2 := by
  constructor
  · rw [cos_zero]; norm_num
  constructor
  · rw [cos_pi_div_three]
  constructor
  · rw [cos_pi_div_two]; norm_num
  constructor
  · rw [show (2:ℝ)*π/3 = π - π/3 by ring, cos_pi_sub, cos_pi_div_three]; norm_num
  · rw [cos_pi]; norm_num

-- ================================================================
-- BOUNDS DIRECTION — Type-1 × Type-1 (ℤ)
-- ================================================================

def IsType1Root (v : Fin 8 → ℤ) : Prop :=
  ∃ i j : Fin 8, i ≠ j ∧
    (v i = 1 ∨ v i = -1) ∧ (v j = 1 ∨ v j = -1) ∧
    ∀ k : Fin 8, k ≠ i → k ≠ j → v k = 0

lemma type1_entry_range (v : Fin 8 → ℤ) (hv : IsType1Root v) (k : Fin 8) :
    v k = -1 ∨ v k = 0 ∨ v k = 1 := by
  obtain ⟨i, j, _, hvi, hvj, hrest⟩ := hv
  by_cases hki : k = i
  · subst hki
    rcases hvi with h | h
    · exact Or.inr (Or.inr h)
    · exact Or.inl h
  · by_cases hkj : k = j
    · subst hkj
      rcases hvj with h | h
      · exact Or.inr (Or.inr h)
      · exact Or.inl h
    · exact Or.inr (Or.inl (hrest k hki hkj))

lemma pm1_mul_small (a b : ℤ) (ha : a = 1 ∨ a = -1)
    (hb : b = -1 ∨ b = 0 ∨ b = 1) : -1 ≤ a * b ∧ a * b ≤ 1 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl | rfl <;> norm_num

theorem type1_ip_bound (v₁ v₂ : Fin 8 → ℤ)
    (h₁ : IsType1Root v₁) (h₂ : IsType1Root v₂) :
    -2 ≤ ∑ k : Fin 8, v₁ k * v₂ k ∧ ∑ k : Fin 8, v₁ k * v₂ k ≤ 2 := by
  obtain ⟨i, j, hij, hvi, hvj, hrest⟩ := h₁
  have hsum : ∑ k : Fin 8, v₁ k * v₂ k = v₁ i * v₂ i + v₁ j * v₂ j := by
    have h0 : ∀ k ∈ (univ : Finset (Fin 8)), k ∉ ({i, j} : Finset (Fin 8)) →
              v₁ k * v₂ k = 0 := by
      intro k _ hk
      simp only [mem_insert, mem_singleton] at hk
      push Not at hk
      rw [hrest k hk.1 hk.2, zero_mul]
    have heq := (sum_subset (subset_univ ({i, j} : Finset (Fin 8))) h0).symm
    rw [heq, sum_insert (mem_singleton.not.mpr hij), sum_singleton]
  have hbi := pm1_mul_small _ _ hvi (type1_entry_range v₂ h₂ i)
  have hbj := pm1_mul_small _ _ hvj (type1_entry_range v₂ h₂ j)
  rw [hsum]
  exact ⟨by linarith [hbi.1, hbj.1], by linarith [hbi.2, hbj.2]⟩

-- ================================================================
-- BOUNDS DIRECTION — Type-2 × Type-2 (ℚ)
-- ================================================================

def IsType2Root (v : Fin 8 → ℚ) : Prop :=
  ∀ k : Fin 8, v k = 1/2 ∨ v k = -1/2

lemma half_mul_half (a b : ℚ) (ha : a = 1/2 ∨ a = -1/2) (hb : b = 1/2 ∨ b = -1/2) :
    -(1/4) ≤ a * b ∧ a * b ≤ 1/4 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> norm_num

theorem type2_ip_bound (v₁ v₂ : Fin 8 → ℚ)
    (h₁ : IsType2Root v₁) (h₂ : IsType2Root v₂) :
    (-2 : ℚ) ≤ ∑ k : Fin 8, v₁ k * v₂ k ∧ ∑ k : Fin 8, v₁ k * v₂ k ≤ 2 := by
  have hge : ∀ k : Fin 8, -(1/4 : ℚ) ≤ v₁ k * v₂ k := fun k =>
    (half_mul_half _ _ (h₁ k) (h₂ k)).1
  have hle : ∀ k : Fin 8, v₁ k * v₂ k ≤ (1/4 : ℚ) := fun k =>
    (half_mul_half _ _ (h₁ k) (h₂ k)).2
  constructor
  · calc (-2 : ℚ) = ∑ _k : Fin 8, (-(1/4) : ℚ) := by
          rw [sum_const, card_univ, Fintype.card_fin]; norm_num
      _ ≤ ∑ k : Fin 8, v₁ k * v₂ k := sum_le_sum (fun k _ => hge k)
  · calc ∑ k : Fin 8, v₁ k * v₂ k
        ≤ ∑ _k : Fin 8, (1/4 : ℚ) := sum_le_sum (fun k _ => hle k)
      _ = 2 := by rw [sum_const, card_univ, Fintype.card_fin]; norm_num

-- ================================================================
-- BOUNDS DIRECTION — Type-1 × Type-2 (ℚ)
-- ================================================================

def IsType1RootQ (v : Fin 8 → ℚ) : Prop :=
  ∃ i j : Fin 8, i ≠ j ∧
    (v i = 1 ∨ v i = -1) ∧ (v j = 1 ∨ v j = -1) ∧
    ∀ k : Fin 8, k ≠ i → k ≠ j → v k = 0

lemma one_mul_half (a b : ℚ) (ha : a = 1 ∨ a = -1) (hb : b = 1/2 ∨ b = -1/2) :
    -(1/2) ≤ a * b ∧ a * b ≤ 1/2 := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> norm_num

theorem type12_ip_bound (v₁ v₂ : Fin 8 → ℚ)
    (h₁ : IsType1RootQ v₁) (h₂ : IsType2Root v₂) :
    (-1 : ℚ) ≤ ∑ k : Fin 8, v₁ k * v₂ k ∧ ∑ k : Fin 8, v₁ k * v₂ k ≤ 1 := by
  obtain ⟨i, j, hij, hvi, hvj, hrest⟩ := h₁
  have hsum : ∑ k : Fin 8, v₁ k * v₂ k = v₁ i * v₂ i + v₁ j * v₂ j := by
    have h0 : ∀ k ∈ (univ : Finset (Fin 8)), k ∉ ({i, j} : Finset (Fin 8)) →
              v₁ k * v₂ k = 0 := by
      intro k _ hk
      simp only [mem_insert, mem_singleton] at hk
      push Not at hk
      rw [hrest k hk.1 hk.2, zero_mul]
    have heq := (sum_subset (subset_univ ({i, j} : Finset (Fin 8))) h0).symm
    rw [heq, sum_insert (mem_singleton.not.mpr hij), sum_singleton]
  have hbi := one_mul_half _ _ hvi (h₂ i)
  have hbj := one_mul_half _ _ hvj (h₂ j)
  rw [hsum]
  exact ⟨by linarith [hbi.1, hbj.1], by linarith [hbi.2, hbj.2]⟩

#check @prop11
#check @corollary10_retraction
#check @actor_roots_valid
#check @opposition_theorem
#check @aspect_e8_achievability
#check @aspect_e8_cosines
#check @type1_ip_bound
#check @type2_ip_bound
#check @type12_ip_bound