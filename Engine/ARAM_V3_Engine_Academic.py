"""
A.R.A. Matrix Engine V3 — Academic Examination Version
Copyright © 2026 Abdullah Uriel Khafra. All Rights Reserved.
This version is designated for open academic examination.
It uses Swiss Ephemeris for precision positions.
It does NOT include proprietary V4/V5 enhancement layers:
  - No Decan Trigger (FIX-K)
  - No Nakshatra Moon (FIX-L)
  - No Era Weighting (FIX-M)
  - No Kalachakra (FIX-N)
  - No Second-Order Stage Setter (FIX-O)
  - No Haylag (FIX-P)
  - No Fast Trigger (FIX-E)
  - No Separating Decay (FIX-G)
  - No Orbital Modifier (FIX-I)
  - No Eclipse Weight (FIX-H)
  - No Lookback (FIX-D)
  - No Jupiter Ingress (FIX-J)
V3 represents the core geometric engine. Its results establish
a reproducible academic baseline. V5/ACE results exceed V3 due
to the proprietary enhancement layers listed above.
"""
import swisseph as swe
import math

swe.set_ephe_path('')  # use built-in ephemeris

PHI = 1.6180339887498948

# ── ACTORS ────────────────────────────────────────────────────────────────────
ACTORS = {
    'Jupiter': {'id': swe.JUPITER, 'weight': 1.000, 'class': 'FORCE_EXP'},
    'Saturn':  {'id': swe.SATURN,  'weight': 0.299, 'class': 'STRUCTURE'},
    'Neptune': {'id': swe.NEPTUNE, 'weight': 0.054, 'class': 'FIELD_GEN'},
    'Uranus':  {'id': swe.URANUS,  'weight': 0.046, 'class': 'FORCE_DIS'},
    'Sun':     {'id': swe.SUN,     'weight': 0.032, 'class': 'IDENTITY'},
    'Pluto':   {'id': swe.PLUTO,   'weight': 0.014, 'class': 'STRUCT_TRANS'},
    'Mars':    {'id': swe.MARS,    'weight': 0.011, 'class': 'FORCE_AGG'},
    'Moon':    {'id': swe.MOON,    'weight': 0.009, 'class': 'FIELD_LUNAR'},
    'Venus':   {'id': swe.VENUS,   'weight': 0.007, 'class': 'VALUE'},
    'Mercury': {'id': swe.MERCURY, 'weight': 0.002, 'class': 'SIGNAL'},
    'Rahu':    {'id': swe.TRUE_NODE,'weight':0.006, 'class': 'FIELD_NODAL'},
}
SLOW_ACTORS = ['Jupiter','Saturn','Neptune','Uranus','Pluto','Rahu']

# ── GEOMETRIC STAGES ─────────────────────────────────────────────────────────
# V3 uses 7 core stages (the E8-derivable set)
STAGES = [
    {'name':'ORIGIN', 'angle':0,   'orb':8.0, 'tension': 4.0},
    {'name':'VECTOR', 'angle':30,  'orb':3.0, 'tension': 1.0},
    {'name':'NODE',   'angle':60,  'orb':6.0, 'tension':-1.0},
    {'name':'PLANE',  'angle':90,  'orb':7.0, 'tension': 2.5},
    {'name':'TRIAD',  'angle':120, 'orb':7.0, 'tension':-2.0},
    {'name':'CUSP',   'angle':150, 'orb':3.0, 'tension': 0.8},
    {'name':'MIRROR', 'angle':180, 'orb':8.0, 'tension': 3.0},
]

STAGE_CHARACTER = {
    'PLANE':  'crisis',
    'MIRROR': 'confrontation',
    'ORIGIN': 'emergence',
    'TRIAD':  'stable_flow',
    'NODE':   'exchange',
    'VECTOR': 'new_momentum',
    'CUSP':   'correction',
}

ACTOR_DOMAIN = {
    'FORCE_EXP':   'political/economic',
    'FORCE_AGG':   'military/violence',
    'STRUCTURE':   'law/government/death',
    'IDENTITY':    'leadership/sovereignty',
    'VALUE':       'finance/diplomacy',
    'SIGNAL':      'technology/communication',
    'FIELD_LUNAR': 'collective/mass_emotion',
    'FIELD_GEN':   'ideology/religion',
    'FORCE_DIS':   'revolution/shock',
    'STRUCT_TRANS':'transformation/nuclear',
    'FIELD_NODAL': 'fate/eclipse_turn',
}

REF_MASS = math.sqrt(ACTORS['Jupiter']['weight'] * ACTORS['Saturn']['weight'])

def date_to_jd(year, month, day, hour=12.0):
    return swe.julday(year, month, day, hour)

def get_positions(jd):
    pos = {}
    for name, actor in ACTORS.items():
        try:
            result, _ = swe.calc_ut(jd, actor['id'], swe.FLG_SWIEPH | swe.FLG_SPEED)
            pos[name] = {'lon': result[0], 'speed': result[3]}
        except:
            pos[name] = {'lon': 0.0, 'speed': 0.0}
    rahu_lon = pos['Rahu']['lon']
    pos['Ketu'] = {'lon': (rahu_lon + 180) % 360, 'speed': pos['Rahu']['speed']}
    return pos

def angular_sep(lon1, lon2):
    diff = abs(lon1 - lon2) % 360
    return diff if diff <= 180 else 360 - diff

def detect_stage(sep):
    best = None; best_orb = float('inf')
    for s in STAGES:
        dev = abs(sep - s['angle'])
        if dev <= s['orb'] and dev < best_orb:
            best = {**s, 'orb_actual': dev}
            best_orb = dev
    return best

def amplify(n):
    return 1.0 if n < 3 else round(n ** PHI, 4)

def is_slow(a):
    return a in SLOW_ACTORS or a == 'Ketu'

def compute_v3(jd):
    pos = get_positions(jd)
    all_slow = SLOW_ACTORS + ['Ketu']
    slow_pairs = []
    n_tight = 0

    for i in range(len(all_slow)):
        for j in range(i+1, len(all_slow)):
            a1, a2 = all_slow[i], all_slow[j]
            if {a1,a2} == {'Rahu','Ketu'}: continue
            lon1 = pos[a1]['lon']; lon2 = pos[a2]['lon']
            sep = angular_sep(lon1, lon2)
            stage = detect_stage(sep)
            if not stage: continue
            w1 = ACTORS.get(a1,{}).get('weight',0.006)
            w2 = ACTORS.get(a2,{}).get('weight',0.006)
            if a1=='Ketu': w1=0.006
            if a2=='Ketu': w2=0.006
            orb_safe = max(stage['orb_actual'], 0.1)
            raw = math.sqrt(w1*w2) * stage['tension'] * (1/orb_safe**1.2)
            slow_pairs.append({
                'a1':a1,'a2':a2,'stage':stage['name'],
                'sep':round(sep,3),'orb':round(stage['orb_actual'],3),
                'tension':stage['tension'],'score':round(raw,5),
                'ac1':ACTORS.get(a1,{}).get('class',''),
                'ac2':ACTORS.get(a2,{}).get('class',''),
            })
            if stage['orb_actual'] <= 1.5: n_tight += 1

    slow_pairs.sort(key=lambda x: abs(x['score']), reverse=True)
    slow_raw = sum(p['score'] for p in slow_pairs)
    amp = amplify(n_tight)
    m2 = round(slow_raw * amp, 4)
    return m2, slow_pairs

def classify_v3(m2, slow_pairs):
    """
    V3 topology classifier — core geometric classification.
    Returns: (topology_string, stage_char, actor_domain, confidence)
    """
    if not slow_pairs:
        return "background [unspecified]", "background", "unspecified", 0.0

    dominant = slow_pairs[0]
    stage_char = STAGE_CHARACTER.get(dominant['stage'], dominant['stage'])

    # Determine dominant actor class by mass-weighted contribution
    tight = [p for p in slow_pairs if p['orb'] <= 3.0] or slow_pairs[:3]
    ac_weights = {}
    for p in tight:
        for ac, planet in [(p['ac1'],p['a1']),(p['ac2'],p['a2'])]:
            w = ACTORS.get(planet,{}).get('weight',0.006)
            ac_weights[ac] = ac_weights.get(ac,0) + w * abs(p['score'])

    dom_ac = max(ac_weights, key=ac_weights.get) if ac_weights else 'FORCE_EXP'
    domain = ACTOR_DOMAIN.get(dom_ac, 'unspecified')
    topology = f"{stage_char} [{domain}]"
    confidence = round(abs(m2), 4)
    return topology, stage_char, domain, confidence

print("V3 Engine loaded — Swiss Ephemeris precision, core geometric layers only.")
