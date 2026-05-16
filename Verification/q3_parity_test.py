"""
Q3 Parity Test — ARAM XIV
Do physical RSM eigenvectors align preferentially with EVEN-parity
type-2 E8 roots vs ODD-parity uniform vectors?

If yes: supports E8 specifically (not just the hypercube shell).
If no: empirical claim reduces to "uniform-component alignment."

Usage: python q3_parity_test.py
Requires: numpy
"""

import numpy as np
from itertools import combinations


# ── E8 ROOT GENERATION ────────────────────────────────────────────────────────

def generate_e8_roots():
    roots = []
    # Type-1: 112 pair-concentrated roots
    for i, j in combinations(range(8), 2):
        for si in [1, -1]:
            for sj in [1, -1]:
                r = np.zeros(8); r[i] = si; r[j] = sj
                roots.append(r / np.sqrt(2))
    # Type-2: 128 even-parity uniform roots
    for mask in range(256):
        if bin(mask).count('1') % 2 == 0:  # even number of minus signs
            r = np.array([(-0.5 if (mask >> k) & 1 else 0.5) for k in range(8)])
            roots.append(r / np.linalg.norm(r))
    return np.array(roots)

E8 = generate_e8_roots()
E8_t1 = E8[:112]   # type-1 (D8)
E8_t2 = E8[112:]   # type-2 (E8-exclusive, even parity)

# All 256 uniform ±1/√8 vectors (even AND odd parity)
all_uniform = np.array([
    np.array([(-1 if (mask >> k) & 1 else 1) for k in range(8)], dtype=float) / np.sqrt(8)
    for mask in range(256)
])
even_parity = all_uniform[[bin(mask).count('1') % 2 == 0 for mask in range(256)]]  # 128
odd_parity  = all_uniform[[bin(mask).count('1') % 2 == 1 for mask in range(256)]]  # 128

assert len(even_parity) == 128 and len(odd_parity) == 128
assert np.allclose(even_parity, E8_t2), "even_parity should match E8 type-2 roots"


# ── RSM CONSTRUCTION ─────────────────────────────────────────────────────────

def build_rsm(periods, eps=0.03, max_n=15):
    p = np.array(periods, dtype=float)
    H = np.zeros((8, 8))
    for i in range(8):
        for j in range(i + 1, 8):
            ratio = max(p[i], p[j]) / min(p[i], p[j])
            best_dev = np.inf
            for n in range(1, max_n + 1):
                for m in range(1, max_n + 1):
                    dev = abs(ratio - n / m)
                    if dev < best_dev:
                        best_dev = dev
            frac_dev = best_dev / ratio
            H[i, j] = H[j, i] = np.exp(-frac_dev / eps)
    return H

def get_eigenvectors(periods):
    H = build_rsm(periods)
    _, vecs = np.linalg.eigh(H)
    # Return as rows, normalized
    return np.array([vecs[:, k] / np.linalg.norm(vecs[:, k]) for k in range(8)])


# ── PERIOD DATA ───────────────────────────────────────────────────────────────

solar = [87.969, 224.701, 365.256, 686.971, 4332.59, 10759.22, 30688.5, 60195.0]
saturn = [0.9424, 1.3702, 1.8878, 2.7369, 4.5175, 15.9454, 21.2766, 79.3215]
tidal = [0.5175, 1.0758, 27.5545, 27.2122, 29.5306, 182.621, 365.242, 6798.38]

solar_labels  = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
saturn_labels = ["Mimas", "Enceladus", "Tethys", "Dione", "Rhea", "Titan", "Hyperion", "Iapetus"]
tidal_labels  = ["M2", "O1", "Anom", "Drac", "Syn", "SemiAnn", "Ann", "Nodal"]

systems = [
    ("Solar system",   solar,  solar_labels),
    ("Saturn moons",   saturn, saturn_labels),
    ("Earth tidal",    tidal,  tidal_labels),
]


# ── PARITY TEST ───────────────────────────────────────────────────────────────

THRESH = 0.95

print("=" * 65)
print("Q3 PARITY TEST — Do RSM eigenvectors prefer even-parity type-2 roots?")
print("=" * 65)
print(f"\nThreshold: |cos| > {THRESH}")
print(f"Even-parity (E8 type-2): {len(even_parity)} vectors")
print(f"Odd-parity  (complement): {len(odd_parity)} vectors")
print(f"All uniform (both):       {len(all_uniform)} vectors")

for sys_name, periods, labels in systems:
    eigvecs = get_eigenvectors(periods)
    H = build_rsm(periods)
    evals = np.linalg.eigh(H)[0]

    print(f"\n{'─'*65}")
    print(f"{sys_name}")
    print(f"{'─'*65}")
    print(f"{'Eigvec':>8} {'Eigenval':>10} {'MaxCos_even':>12} {'MaxCos_odd':>12} "
          f"{'Hits_even':>10} {'Hits_odd':>10} {'Parity_winner':>14}")

    total_even_hits = 0
    total_odd_hits  = 0
    parity_supported = []

    for k in range(8):
        v = eigvecs[k]
        lam = evals[k]

        cos_even = np.abs(even_parity @ v)
        cos_odd  = np.abs(odd_parity  @ v)

        max_even = cos_even.max()
        max_odd  = cos_odd.max()
        hits_even = int(np.sum(cos_even > THRESH))
        hits_odd  = int(np.sum(cos_odd  > THRESH))

        total_even_hits += hits_even
        total_odd_hits  += hits_odd

        # Which parity achieves higher max alignment?
        winner = "even ✓" if max_even >= max_odd else "odd  ✗"
        if hits_even > 0 or hits_odd > 0:  # only record for eigvecs that hit anything
            parity_supported.append(max_even >= max_odd)

        print(f"  λ{k:1d} ({lam:+.4f}) {max_even:>12.4f} {max_odd:>12.4f} "
              f"{hits_even:>10d} {hits_odd:>10d} {winner:>14}")

    print(f"\n  TOTALS: even hits={total_even_hits}  odd hits={total_odd_hits}")
    if total_even_hits + total_odd_hits > 0:
        pct_even = 100 * total_even_hits / (total_even_hits + total_odd_hits)
        print(f"  Even-parity share of all hits above threshold: {pct_even:.1f}%")

    # For eigvecs that align with ANY uniform vector: which parity dominates?
    if parity_supported:
        pct_even_max = 100 * sum(parity_supported) / len(parity_supported)
        print(f"  Eigvecs where even-parity achieves higher max cos: "
              f"{sum(parity_supported)}/{len(parity_supported)} ({pct_even_max:.0f}%)")


# ── RANDOM BASELINE: what fraction of random vectors prefer even parity? ─────

print(f"\n{'='*65}")
print("RANDOM BASELINE")
print(f"{'='*65}")
print("For random unit vectors in R^8, how often does even-parity")
print("achieve higher max cosine than odd-parity (expected ~50%)?")

rng = np.random.default_rng(42)
n_mc = 100_000
even_wins = 0
for _ in range(n_mc):
    v = rng.standard_normal(8); v /= np.linalg.norm(v)
    if np.abs(even_parity @ v).max() >= np.abs(odd_parity @ v).max():
        even_wins += 1

print(f"  Random: even-parity wins {even_wins}/{n_mc} = {100*even_wins/n_mc:.2f}%")
print(f"  (Expected ~50% for no parity preference)")


# ── SIGN-PATTERN ANALYSIS: which specific even-parity vectors align? ──────────

print(f"\n{'='*65}")
print("SIGN-PATTERN DETAIL: top-aligning type-2 roots per system")
print(f"{'='*65}")
print("For each system's eigenvectors that hit type-2 threshold,")
print("show which specific sign patterns align (verify even parity).")

for sys_name, periods, labels in systems:
    eigvecs = get_eigenvectors(periods)
    H = build_rsm(periods)
    evals = np.linalg.eigh(H)[0]

    print(f"\n{sys_name}:")
    for k in range(8):
        v = eigvecs[k]
        cos_even = np.abs(even_parity @ v)
        cos_odd  = np.abs(odd_parity  @ v)

        # Only show eigvecs that hit even-parity threshold
        if cos_even.max() > THRESH:
            best_idx = np.argmax(cos_even)
            best_root = even_parity[best_idx]
            signs = ['+'if x>0 else '-' for x in best_root]
            minus_count = signs.count('-')
            parity_ok = (minus_count % 2 == 0)
            print(f"  λ{k} ({evals[k]:+.4f}): best cos={cos_even.max():.4f}  "
                  f"sign pattern={''.join(signs)}  "
                  f"minus_count={minus_count}  even_parity={parity_ok}")

print(f"\n{'='*65}")
print("VERDICT")
print(f"{'='*65}")
print("""
Interpretation guide:
  IF physical eigvecs prefer even-parity at >> 50% rate while random ~50%:
    → E8 specifically supported, not just hypercube shell
    → Q3 becomes a positive result: PARITY CONFIRMED

  IF physical eigvecs split ~50/50 between even and odd:
    → Claim reduces to "uniform-component alignment"
    → E8 type-2 roots are being used as convenient uniform generators
    → Q3 remains: PARITY NOT VERIFIED

  Note: type-1 eigvecs (tidal system) are unaffected by this test —
  parity applies only to type-2 (uniform-component) eigvecs.
  This test is most informative for Solar and Saturn substrates.
""")
EOF