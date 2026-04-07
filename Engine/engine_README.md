# Engine

## ARAM V3 Academic Engine

**Status:** Open source · Academic replication instrument  
**Performance:** 33.3% weighted accuracy on in-scope events (11.1% random baseline → 3× lift)  
**Purpose:** Independent verification of the ARAM framework's baseline architecture

---

## What V3 Is

The V3 engine is the intentionally reduced open-source version of the ARAM classification system. It implements the core geometric logic of the framework — E8 root-pair angle detection, actor class assignment, stage classification — without the proprietary enhancement layers that comprise ACE.

V3 is designed for one purpose: **independent replication**. Any researcher can download this file, run it against an independently constructed event corpus, and verify whether the baseline framework produces above-chance topology matching. No black box. No hidden parameters. No trained weights. The classifier is purely geometric.

---

## What V3 Is Not

V3 is not ACE. The gap between them is significant and intentional.

| | V3 Academic | ACE v5.3-FINAL |
|---|---|---|
| Topology recall | 33.3% weighted | 99.2% consistency |
| Enhancement layers | None | 13 proprietary layers |
| Parameters | Zero | Zero (still parameter-free) |
| Availability | Open source | Hash-locked, proprietary |
| Purpose | Replication baseline | Commercial / research instrument |

The gap between 33.3% and 99.2% is the intellectual property. It represents two years of architectural development documented in Working Papers I–VII. The enhancement layers are the subject of the pending patent application.

Publishing V3 establishes the **reproducible floor**. ACE performance above that floor is verified by:
1. SHA-256 hash: `caa4c8aebc57b3229bc7571170ad1f84669b46a90e39bcc09e9bb673e7d95f74`
2. OSF timestamp registry preceding all validation results
3. Pre-registered prospective predictions (5/5 confirmed, p = 0.0001)

---

## How to Run V3

```bash
pip install pyswisseph numpy
python3 ARAM_V3_Engine_Academic.py
```

The file includes a self-test that runs on several known historical events and prints topology classifications with match scores.

**Basic usage:**

```python
from datetime import datetime, timezone
import ARAM_V3_Engine_Academic as v3

# Get sky geometry for a date
dt = datetime(2022, 2, 24, 5, 0, tzinfo=timezone.utc)  # Russia-Ukraine invasion
sky = v3.get_sky(dt)

# Classify topology
result = v3.classify_sky(sky)
print(result['primary']['key'])        # FORCE_PLANE
print(result['primary']['topology'])   # Physical conflict or crackdown
print(result['significance'])          # CRITICAL
```

---

## How to Run an Independent Replication Study

The Topology Match Methodology document (OSF: 10.17605/OSF.IO/YM4TF) specifies the complete replication protocol. Summary:

1. **Construct a corpus independently** — select major world events from Tier 1 news sources (Reuters, AP, AFP) without consulting ACE output. Minimum 50 events across at least 4 categories.

2. **Assign categories before running V3** — classify each event into the 9-category taxonomy (Military, Financial, Governance, Diplomatic, Social, Disaster, Health, Technology, Legal) before retrieving any engine output.

3. **Run V3 and score** — retrieve the topology signature for each event date, score against the pre-specified ACTOR×STAGE → category mapping table (Appendix A of the Pre-Registration Protocol).

4. **Report all results** — including non-matches. The protocol explicitly prohibits selective reporting.

5. **Compute against baseline** — V3's 11.1% random baseline is the uniform prior over 25 output combinations across 9 categories. Compare your observed match rate against this baseline.

A V3 replication study producing consistent results with the baseline (33.3% weighted accuracy, 3× lift) constitutes independent academic validation of the framework's core architecture. A study producing significantly higher results would suggest additional signal in V3 not yet measured. A study producing chance-level results would be a genuine falsification finding.

**The methodology document provides all rules needed. The invitation for replication is open.**

---

## The Pre-Registration Protocol

All prospective predictions from the 2026–2050 grid are governed by Pre-Registration Protocol v1.0 (OSF: 10.17605/OSF.IO/YM4TF), filed before any prediction windows opened.

The protocol specifies in advance:
- What counts as a qualifying event (P1–P10)
- Which news sources are approved (Tier 1: Reuters, AP, AFP)
- What magnitude thresholds apply (Tier A automatic, Tier B conditional)
- How matches are scored (1.0 full, 0.5 partial, 0.0 none)
- What statistical threshold constitutes corpus-level success

No scoring decision after an event can override any protocol definition. The protocol is immutable upon OSF deposit. Any amendments are versioned separately and cannot retroactively apply to open windows.

---

## Contact

**Lords of the Pivot / Astromatics**  
lordsofthepivot.com  
OSF: https://osf.io/ym4tf/

Commercial licensing inquiries: lordsofthepivot.com/contact  
Academic collaboration: Open. Cite the OSF repository and reach out.
