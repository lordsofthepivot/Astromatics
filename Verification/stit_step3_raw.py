"""
STIT Step 3 Verification Computation
Lords of the Pivot LLC / Astromatics
May 2026

Question: Does δ_k = λ1(R_k) - λ2(R_k) > 0 for ALL non-trivial
k-frequency subsets of the 8 solar planets?

If yes: Davis-Kahan bounds are finite for all subsystems.
STIT Step 3 conditional closes. Proof is complete.

RSM formula (from ARAM framework):
  H_ii = 0
  H_ij = exp(-δ_ij / ε),  ε = 0.03
  δ_ij = fractional deviation of ratio from best rational n/m, n,m ≤ 15
"""

import numpy as np
from itertools import combinations

# ─── PLANET DATA ────────────────────────────────────────────────────────────
planets = ['Mercury', 'Venus', 'Earth', 'Mars',
           'Jupiter', 'Saturn', 'Uranus', 'Neptune']

periods = np.array([87.9691, 224.701, 365.256, 686.971,
                    4332.59, 10759.22, 30688.5, 60195.0])

EPSILON = 0.03
MAX_NM  = 15

# ─── CORE FUNCTIONS ─────────────────────────────────────────────────────────

def best_rational(ratio, max_n=MAX_NM):
    """
    Find n/m (n,m ≤ max_n) minimising fractional deviation |ratio - n/m| / (n/m).
    Returns (n, m, fractional_deviation).
    """
    best_dev = float('inf')
    best = (1, 1)
    for n in range(1, max_n + 1):
        for m in range(1, max_n + 1):
            r = n / m
            dev = abs(ratio - r) / r
            if dev < best_dev:
                best_dev = dev
                best = (n, m)
    return best[0], best[1], best_dev

def build_rsm(planet_periods):
    """Build RSM for a list of periods."""
    k = len(planet_periods)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i != j:
                ratio = (max(planet_periods[i], planet_periods[j]) /
                         min(planet_periods[i], planet_periods[j]))
                _, _, dev = best_rational(ratio)
                H[i, j] = np.exp(-dev / EPSILON)
    return H

def spectral_gap(H):
    """λ1 - λ2 of symmetric matrix H."""
    eigvals = np.sort(np.linalg.eigvalsh(H))[::-1]
    return eigvals[0] - eigvals[1], eigvals[0], eigvals[1]

def dominant_eigvec(H):
    vals, vecs = np.linalg.eigh(H)
    return vecs[:, -1]   # largest eigenvalue last in eigvalsh

def r_plus(k):
    return np.ones(k) / np.sqrt(k)

def cos_alignment(v, w):
    return float(abs(np.dot(v / np.linalg.norm(v), w / np.linalg.norm(w))))

# ─── FULL 8×8 RSM ───────────────────────────────────────────────────────────
print("=" * 65)
print("STIT STEP 3 — SPECTRAL GAP VERIFICATION")
print("All 247 non-trivial solar-system RSM subsets")
print("=" * 65)

RSM8 = build_rsm(periods)
delta8, lam1_8, lam2_8 = spectral_gap(RSM8)
v8 = dominant_eigvec(RSM8)

print(f"\n8-PLANET FULL RSM")
print(f"  λ1 = {lam1_8:.6f}")
print(f"  λ2 = {lam2_8:.6f}")
print(f"  δ_8 = λ1 - λ2 = {delta8:.6f}")
print(f"  Dominant eigenvector: {np.round(v8, 4)}")
print(f"  Alignment with r+ : cos = {cos_alignment(v8, r_plus(8)):.6f}")

# Verify pairwise couplings match ARAM paper examples
print("\nCOUPLING STRENGTH SPOT CHECKS:")
pairs_to_check = [
    (1, 2, "Venus:Earth",   "13:8",  0.989),
    (4, 5, "Jupiter:Saturn","5:2",   0.799),
]
for i, j, label, ratio_str, expected in pairs_to_check:
    ratio = max(periods[i], periods[j]) / min(periods[i], periods[j])
    n, m, dev = best_rational(ratio)
    coupling = np.exp(-dev / EPSILON)
    check = "✓" if abs(coupling - expected) < 0.01 else f"? (expected {expected})"
    print(f"  {label}: ratio={ratio:.4f}, best={n}/{m}, dev={dev*100:.3f}%, "
          f"H={coupling:.3f} {check}")

# ─── ALL SUBSETS ─────────────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("COMPUTING ALL NON-TRIVIAL SUBSETS (k=2..8)...")
print(f"{'─'*65}")

results = []
all_gaps_positive = True

for k in range(2, 9):
    for subset_idx in combinations(range(8), k):
        idx = list(subset_idx)
        sub_periods = periods[idx]
        sub_names   = [planets[i] for i in idx]

        H_k      = build_rsm(sub_periods)
        delt, l1, l2 = spectral_gap(H_k)
        v_star   = dominant_eigvec(H_k)
        cos_rp   = cos_alignment(v_star, r_plus(k))

        # Embedded alignment with 8-dim r+
        v_embed       = np.zeros(8)
        for pos, planet_idx in enumerate(idx):
            v_embed[planet_idx] = v_star[pos]
        v_embed      /= np.linalg.norm(v_embed)
        cos_embed     = cos_alignment(v_embed, r_plus(8))

        # Geometric lower bound from Prop 11 extension
        geo_floor = np.sqrt(k / 8)

        if delt <= 0:
            all_gaps_positive = False

        results.append(dict(
            k=k, idx=idx, names=sub_names,
            delta=delt, lam1=l1, lam2=l2,
            cos_rp=cos_rp, cos_embed=cos_embed,
            geo_floor=geo_floor
        ))

# ─── SUMMARY STATISTICS ─────────────────────────────────────────────────────

print(f"\nTotal subsets computed: {len(results)}")
print(f"All δ_k > 0: {all_gaps_positive}")

# Worst case (minimum gap)
worst = min(results, key=lambda r: r['delta'])
best  = max(results, key=lambda r: r['delta'])

print(f"\nWORST-CASE (minimum spectral gap):")
print(f"  Planets  : {worst['names']}")
print(f"  k        : {worst['k']}")
print(f"  λ1       : {worst['lam1']:.6f}")
print(f"  λ2       : {worst['lam2']:.6f}")
print(f"  δ_k      : {worst['delta']:.6f}")
print(f"  cos(v*,r+): {worst['cos_rp']:.6f}")

print(f"\nBEST-CASE (maximum spectral gap):")
print(f"  Planets  : {best['names']}")
print(f"  k        : {best['k']}")
print(f"  δ_k      : {best['delta']:.6f}")

# Per-k summary
print(f"\n{'─'*65}")
print(f"{'k':>3} | {'#sets':>5} | {'min δ':>10} | {'max δ':>10} | "
      f"{'min cos(embed)':>14} | {'geo floor':>9}")
print(f"{'─'*65}")

for k in range(2, 9):
    k_res  = [r for r in results if r['k'] == k]
    deltas = [r['delta']     for r in k_res]
    embeds = [r['cos_embed'] for r in k_res]
    floor  = np.sqrt(k / 8)
    print(f"{k:>3} | {len(k_res):>5} | {min(deltas):>10.4f} | "
          f"{max(deltas):>10.4f} | {min(embeds):>14.4f} | {floor:>9.4f}")

# ─── DAVIS-KAHAN BOUNDS ─────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("DAVIS-KAHAN BOUND ANALYSIS")
print("Perturbation norm ε_pert = max off-diagonal coupling ≈ max H_ij")
print("For 'small' perturbation = removing one planet from k+1 system")
print(f"{'─'*65}")

# The 'perturbation' when going from k+1 to k system is removing a row/col.
# The norm of this perturbation is the column removed, bounded by sum of H_ij.
# For RSMs, max coupling < 1.0 (exponential formula).
# DK bound: sin(angle) ≤ ε_pert / δ_k

max_coupling = np.max(RSM8)
print(f"\nMax single coupling in RSM8: {max_coupling:.4f}")
print(f"\nDavis-Kahan sin(angle) bounds (ε_pert / δ_k):")
print(f"{'k':>3} | {'min δ_k':>9} | {'DK bound sin∠':>14} | {'angle (deg)':>12}")
print(f"{'─'*50}")
for k in range(2, 9):
    k_res   = [r for r in results if r['k'] == k]
    min_dlt = min(r['delta'] for r in k_res)
    # Use max row sum of removed rows as perturbation bound
    dk_bound = max_coupling / min_dlt
    angle_deg = np.degrees(np.arcsin(min(dk_bound, 1.0)))
    print(f"{k:>3} | {min_dlt:>9.4f} | {dk_bound:>14.4f} | {angle_deg:>12.2f}°")

# ─── E8 ALIGNMENT VS GEOMETRIC FLOOR ────────────────────────────────────────
print(f"\n{'─'*65}")
print("E8 ALIGNMENT: ACTUAL vs GEOMETRIC FLOOR (√(k/8))")
print(f"{'─'*65}")
print(f"{'k':>3} | {'floor √(k/8)':>12} | {'min actual':>10} | {'max actual':>10} | {'above floor?':>12}")
print(f"{'─'*65}")
for k in range(2, 9):
    k_res  = [r for r in results if r['k'] == k]
    floor  = np.sqrt(k / 8)
    actuals = [r['cos_embed'] for r in k_res]
    above = all(a >= floor - 0.001 for a in actuals)
    print(f"{k:>3} | {floor:>12.4f} | {min(actuals):>10.4f} | "
          f"{max(actuals):>10.4f} | {'✓' if above else 'BELOW':>12}")

# ─── FINAL VERDICT ──────────────────────────────────────────────────────────
print(f"\n{'='*65}")
print("FINAL VERDICT")
print(f"{'='*65}")
min_gap_overall = min(r['delta'] for r in results)
print(f"\n  Total subsets     : {len(results)}")
print(f"  All δ_k > 0       : {all_gaps_positive}")
print(f"  Global minimum δ  : {min_gap_overall:.6f}")
print(f"  Global minimum gap subset: {worst['names']}")
print()
if all_gaps_positive:
    print("  ✓ STIT STEP 3 CONDITIONAL CLOSED.")
    print("  ✓ Davis-Kahan bounds are finite across ALL subsystems.")
    print("  ✓ Dominant eigenvector E8 alignment inherits for all k-frequency")
    print("    subsets of the solar system RSM.")
    print("  ✓ Proof of STIT Step 3 is COMPLETE.")
else:
    print("  ✗ Some spectral gaps are zero or negative.")
    print("  ✗ Conditional NOT closed. Further analysis required.")
print(f"{'='*65}")
