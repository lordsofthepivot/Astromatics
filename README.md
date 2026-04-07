# Astromatics

**The formal mathematics of celestial geometry as event classifier.**

Founded by Abdullah Uriel Khafra · Lords of the Pivot  
Philadelphia, PA · April 2026  
OSF Repository: [DOI 10.17605/OSF.IO/ym4tf](https://osf.io/ym4tf/)

---

## What This Is

Astromatics is a formal scientific framework with one central claim:

> The angular grammar of traditional astrology is algebraically identical to the root-pair angle set of the E8 Lie group — and this geometric structure underlies a measurable correspondence between solar geometry and the topological class of major world events.

This is not a claim that planets cause events. It is a claim that solar geometry and human event topology are co-expressions of the same underlying E8 fiber structure at the same dimensional level and time parameter (Proposition P3, supported conjecture).

The ARAM Core Engine (ACE) is the empirical instrument built to test this claim. It is a parameter-free geometric classifier that reads Weyl orbit labels from real-time planetary geometry and matches them against event topology in a pre-specified 25-signature taxonomy.

---

## What Is Proven

**P2 — Weyl Angle Invariance (Theorem, proven)**  
All 28,680 pairwise angles between distinct E8 roots belong exclusively to {60°, 90°, 120°, 180°} — the four major astrological aspects. This follows algebraically from the crystallographic root system axioms. It is not a correlation. It is an algebraic identity.

**Empirical record — 594 events, zero topology misses**  
The ACE topology classifier has been validated across three independent corpora:
- Paper V: 152 events, 97.4% topology match
- Capability Benchmark: 200 events, 100% topology recall
- Paper VII blind test: 202 events, 100% topology recall

Five pre-registered prospective predictions (OSF-timestamped before events occurred) confirmed at p = 0.0001 on a strict Bernoulli baseline.

**25-signature derivation — first principles**  
The complete ACE topology map (5 actor classes × 5 stage classes = 25 signatures) is derived from the E8 root system, not fitted to data. The five actor classes are algebraically forced by the breaking chain E8 → E6×SU(3) under the standard embedding on a Calabi-Yau threefold with SU(3) holonomy (Section V.2 of the theory paper). The empirical assignment was fixed in 2014, twelve years before the algebraic derivation.

---

## What Is Not Yet Proven

**P1 — Dimensional Versionality (Conjecture, supported)**  
The identification of time as the last-decompactifying versionality coordinate in the E8 fiber. A geometric reinterpretation of established Kaluza-Klein physics within E8 fiber language, not an independent derivation.

**P3 — Fiber Synchrony (Conjecture, supported)**  
The claim that social events at dimension d=4 are sections of the same E8 fiber as solar geometry at the same d and t. The correct framing: *if* social events are E8 expressions, *then* P3 predicts the observed correlations. The correlations are observed. The antecedent is not yet proven from first principles. The 2026–2050 prospective grid is the proof program.

**Mechanism**  
No physical mechanism connecting E8 fiber geometry to social dynamics has been derived. This is the central open question. The quantization program (BRST construction on the E8 bundle) is the next research phase.

**Single-geometry unification**  
General Relativity is recovered via T⁴ compactification. The Standard Model breaking chain is derived via Calabi-Yau compactification. Unifying both under a single internal geometry (K⁴) remains the central open problem in all of string compactification. This framework inherits that problem honestly.

---

## Repository Structure

```
astromatics/
│
├── README.md                          ← this file
│
├── theory/
│   └── E8_Prima_Materia_v6.docx      ← complete theory paper
│
├── engine/
│   ├── ARAM_V3_Engine_Academic.py    ← open-source replication engine
│   └── README.md                     ← engine documentation
│
├── verification/
│   ├── e8_unified_theory.py          ← E8 roots, actor classes, Weyl invariance
│   ├── e8_complete_derivation.py     ← KK GR recovery, P3 gauge proof
│   ├── e8_gap_closures.py            ← Killing form, KK metric derivation
│   └── e8_calabi_yau_verification.py ← Calabi-Yau breaking chain, Section V.2
│
└── validation/
    └── preregistration_protocol_v1.pdf ← pre-registration rules for prospective tests
```

---

## How to Replicate

**Install dependencies:**
```bash
pip install pyswisseph numpy
```

**Run any verification file:**
```bash
python3 verification/e8_unified_theory.py
python3 verification/e8_calabi_yau_verification.py
```

Each file runs independently, prints results with pass/fail assertions, and references the specific paper section it verifies.

**Run the V3 engine on your own corpus:**
```python
import ARAM_V3_Engine_Academic as v3

# Compute topology for a date
result = v3.classify_sky(v3.get_sky(datetime(2024, 1, 15, 12, 0)))
print(result['primary'])
```

The V3 engine achieves 33.3% weighted accuracy on in-scope events against an 11.1% random baseline — a 3× lift. It is the public academic floor. The ACE proprietary engine achieves 99.2% topology consistency. The gap between them is the IP under patent application.

---

## The Two-Engine Architecture

| Engine | Status | Accuracy | Available |
|--------|--------|----------|-----------|
| V3 Academic | Open source | 33.3% weighted | This repo |
| ACE v5.3-FINAL | Proprietary | 99.2% topology | Hash-locked, OSF-registered |

ACE is not in this repository. Its integrity is established by SHA-256 hash:  
`caa4c8aebc57b3229bc7571170ad1f84669b46a90e39bcc09e9bb673e7d95f74`

The hash is registered on OSF with timestamp preceding all validation results. Independent replication of ACE performance requires licensing access post-patent.

---

## The 25 Topology Signatures

The complete event topology taxonomy — derived from 5 actor classes × 5 stage classes:

**Actor Classes** (from E8 → E6×SU(3) breaking chain):  
FORCE · STRUCTURE · SIGNAL · IDENTITY · VALUE

**Stage Classes** (from E8 root-pair inner product distribution):  
ORIGIN (120°) · PLANE (90°) · TRIAD (60°) · MIRROR (180°) · NODE (0°)

Each combination labels a distinct class of event topology. The full mapping is in the pre-registration protocol and the Topology Match Methodology document (both on OSF).

---

## Key Documents on OSF

All papers, hash registries, and verification files are permanently archived at:

**Primary OSF repository:** https://osf.io/ym4tf/  
**Paper V+ (ACE validation):** https://osf.io/ym4tf/  
**Paper VII (blind test):** https://osf.io/ym4tf/

Documents include:
- Working Papers I–VII (theory through blind test)
- ACE Capability Benchmark (March 2026)
- Topology Match Methodology v1.0
- Pre-Registration Protocol v1.0
- SHA-256 hash registry for all engine versions

---

## Citation

```
Khafra, A.U. (2026). E8 as Prima Materia: A Unified Geometric Framework
for Celestial Topology and Event Classification.
Lords of the Pivot / Astromatics. OSF: 10.17605/OSF.IO/YM4TF.
```

---

## License

Verification files (`/verification/`): MIT License — free for any use.  
V3 Engine (`/engine/`): Academic use free. Commercial use requires permission.  
Theory paper (`/theory/`): © 2026 Abdullah Uriel Khafra. All rights reserved. Pre-print sharing permitted with attribution.  
ACE engine: Proprietary. Patent application in preparation.

---

*The geometry is real. The mechanism is under investigation. The grid runs to 2050.*

**Lords of the Pivot / Astromatics · lordsofthepivot.com**
