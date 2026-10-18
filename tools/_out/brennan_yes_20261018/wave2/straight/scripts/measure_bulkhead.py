"""measure_bulkhead.py (wave2 straight, 2026-10-18): bulkhead JIC end length I1 from Brennan STEPs.
Uses only the batch-16 measuring primitives (puckfix_20261009/tools_new/measure/prof.py leg_edges = plane section through the axis,
the same sectioning every validated extractor uses). jicm.py itself cannot be used: it requires the relief at the cone diameter (the
Brennan bulkhead relief is larger, 0.679 vs 0.659 at -08) and drops edges below r 0.05 (the -02 seat tip is at r 0.0415).
I1 as the generator uses it (gen_straight2 end_JICBH: the whole bulkhead end tip -> end of the relief = SL + LL + TZ + ramp + RL):
  I1 = tip - start of the relief, where the relief is the plain cylinder between the 0.04 collar at the hex and the 60deg ramp up to
  the thread major (the collar is NOT part of I1: generator comment "the Brennan 0.04 collar at the hex face ... NOT modelled").
VALIDATION: BRENNAN_2705-08-08.stp must give I1 = 1.44 (= Air-Way 2705 / 2700 / 2706 -08 I1 1.44, and the generator comment
"Brennan I1 from the relief 1.44 = Air-Way") and the -08 MS33656J nose (seat 0.1546, land 0.0984). The -02 parts must give the -02
MS33656J nose of the end library (JIC[2]: SL 0.1108, LL 0.0662, RL 0.063).
Run: python -I measure_bulkhead.py  -> ../measure/bulkhead_I1.json + stdout"""
import os, sys, json, math, hashlib
ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
MT = os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new\measure')
sys.dont_write_bytecode = True
sys.path[:0] = [MT, os.path.dirname(MT), os.path.join(os.path.dirname(MT), 'generators')]
os.environ.setdefault('OMI_ROOT', os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root'))
from prof import bbox, leg_edges

STEPS = os.path.join(ROOT, '09_STEP_FILES')
OUT = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\wave2\straight\measure')
T = 2e-4


def lines(p):
    L = []
    for kind, P in leg_edges(p, 0, 1, 2, a0=-9):
        if kind != 'L':
            continue
        (a1, r1), (a2, r2) = P[0], P[-1]
        if a1 > a2:
            a1, r1, a2, r2 = a2, r2, a1, r1
        if min(r1, r2) < 0.02:
            continue
        L.append(dict(a1=a1, r1=r1, a2=a2, r2=r2, ang=math.degrees(math.atan2(abs(r2 - r1), abs(a2 - a1) + 1e-12))))
    return L


def bulkhead(p):
    L = lines(p)
    tip = max(l['a2'] for l in L)
    seat = [l for l in L if abs(l['ang'] - 37) < 0.3 and abs(l['a2'] - tip) < T]
    assert len(seat) == 1, ('seat', seat)
    s = seat[0]; rC = max(s['r1'], s['r2'])
    land = [l for l in L if l['ang'] < 0.05 and abs(l['r1'] - rC) < T and abs(l['a2'] - s['a1']) < T]
    assert len(land) == 1, ('land', land)
    # the thread major: the longest plain cylinder of the end (the bulkhead thread)
    thd = max([l for l in L if l['ang'] < 0.05 and l['a1'] > -T and l['a2'] < land[0]['a1'] + T], key=lambda l: l['a2'] - l['a1'])
    rM = thd['r1']
    ramp = [l for l in L if abs(l['ang'] - 60) < 0.3 and abs(max(l['r1'], l['r2']) - rM) < T and abs(l['a2'] - thd['a1']) < T]
    assert len(ramp) == 1, ('60deg ramp', ramp)
    rel = [l for l in L if l['ang'] < 0.05 and abs(l['a2'] - ramp[0]['a1']) < T and abs(l['r1'] - min(ramp[0]['r1'], ramp[0]['r2'])) < T]
    assert len(rel) == 1, ('relief', rel)
    r = rel[0]
    collar = [l for l in L if l['ang'] < 0.05 and abs(l['a2'] - r['a1']) < 0.002 and l['r1'] > r['r1'] + 1e-3]
    return dict(tip=round(tip, 4), SL=round(tip - s['a1'], 4), CD=round(2 * rC, 4), LL=round(s['a1'] - land[0]['a1'], 4),
                TM=round(2 * rM, 4), thread_from=round(thd['a1'], 4), thread_to=round(thd['a2'], 4),
                ramp=round(ramp[0]['a2'] - ramp[0]['a1'], 4), relief_dia=round(2 * r['r1'], 4), RL=round(r['a2'] - r['a1'], 4),
                relief_start=round(r['a1'], 4), collar=[dict(a1=round(c['a1'], 4), a2=round(c['a2'], 4), dia=round(2 * c['r1'], 4)) for c in collar],
                I1=round(tip - r['a1'], 4))


res = {}
for pn in ('2705-08-08', '2700-02-02', '2706-04-02'):
    p = os.path.join(STEPS, f'BRENNAN_{pn}.stp')
    b = bbox(p)
    d = dict(step=f'09_STEP_FILES/BRENNAN_{pn}.stp', sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest(), bbox=b,
             overall=round(b[3] - b[0], 4), corner_dia=round(b[4] - b[1], 4), hex_af_from_corners=round((b[4] - b[1]) * math.cos(math.radians(30)), 4))
    d.update(bulkhead(p))
    res[pn] = d
    print(pn, json.dumps(d))
v = res['2705-08-08']
assert abs(v['I1'] - 1.44) < 0.0015 and abs(v['SL'] - 0.1546) < 0.0015 and abs(v['LL'] - 0.0984) < 0.0015, ('VALIDATION FAILED', v)
for pn in ('2700-02-02', '2706-04-02'):
    v = res[pn]
    assert abs(v['SL'] - 0.1108) < 0.0015 and abs(v['LL'] - 0.0662) < 0.0015 and abs(v['RL'] - 0.063) < 0.0015 and abs(v['TM'] - 0.3125) < 0.0015, (pn, v)
print('VALIDATION OK: 2705-08-08 I1 1.44 = Air-Way; -02 noses = MS33656J JIC[2]')
os.makedirs(OUT, exist_ok=True)
json.dump(res, open(os.path.join(OUT, 'bulkhead_I1.json'), 'w'), indent=1)
