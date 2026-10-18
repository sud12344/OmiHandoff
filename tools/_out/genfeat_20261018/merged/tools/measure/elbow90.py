# 90 deg forged ELBOW body extractor (FOLDS, 2026-10-02): per leg of a two-leg 90 deg elbow STEP (legs along two of +-X / +-Y,
# forged hex arms with their flats normal to Z, as every Brennan elbow and every gen_tee elbow model):
#   tip       crossing -> leg tip face (the leg's bounding-box extent)
#   flats     hex across flats of the arm (section in the plane through the leg axis and Z: the outer line nearest the crossing)
#   hexend    crossing -> end of the forged hex arm (last point of the outer line at the flats radius; the 0.002 deep parting-line
#             ripples Brennan draws near the crossing are bridged, any other step ends the arm)
#   arm_steps the steps found on that outer line between the crossing and hexend (a, depth) - an arm that "simply runs on" has
#             only the parting ripples near the crossing
#   endlen    tip - hexend (= the end module's length in gen_tee: JIC chain sum, 5404 NPTF end length ENDL, swivel BODYS)
#   bore      the smallest-radius long inner line of the leg (through bore / drill)
#   end_prof  the outline from hexend to the tip in the flats plane, as (distance from the tip, radius) - two parts with the same
#             end compare directly whatever their leg length
# Legs and axis signs are found from the bounding box (the two largest extents along +-X / +-Y), so it reads Brennan STEPs
# (JIC on -X) and OCP / SolidWorks rebuilds of the gen_tee macros (leg 1 on +X) alike.
#
#   python tools/measure/elbow90.py <step> [<step> ...]          -> one JSON line per STEP
#   python tools/measure/elbow90.py --validate                   -> reproduces the sizes already measured (see VALIDATE)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, math, json
from prof import leg_edges, bbox, shape
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

RIPPLE = 0.003      # largest depth of a parting-line ripple that is bridged (Brennan draws 0.002 at 0.025..0.12 from the crossing)


def legs_of(p):
    b = bbox(p)
    ext = {(0, -1): -b[0], (0, 1): b[3], (1, -1): -b[1], (1, 1): b[4]}
    two = sorted(ext.items(), key=lambda kv: -kv[1])[:2]
    assert {k[0] for k, _ in two} == {0, 1}, ('expected one leg along X and one along Y', two)
    return two


def volume(p):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(shape(p), g)
    return g.Mass() / 25.4 ** 3


def segs(p, axis, sign, pn):
    out = []
    for kind, P in leg_edges(p, axis, sign, pn, a0=-0.01):
        (a1, r1), (a2, r2) = P[0], P[-1]
        if min(r1, r2) < -1e-6: continue
        if a1 > a2: a1, r1, a2, r2 = a2, r2, a1, r1
        out.append(dict(a1=a1, r1=r1, a2=a2, r2=r2, k='L' if kind == 'L' else 'C' if isinstance(kind, tuple) else 'S'))
    return out


def measure_leg(p, axis, sign, tip):
    # flats plane: through the leg axis and Z (normal = the other in-plane axis); r = |z|
    S = segs(p, axis, sign, 1 - axis)
    hz = [s for s in S if s['k'] == 'L' and abs(s['r1'] - s['r2']) < 1e-5 and s['a2'] - s['a1'] > 1e-4]
    # the outer line at the flats radius starts within 0.2 of the crossing (the corner puck and the other arm stop there)
    near0 = [s for s in hz if s['a1'] < 0.2 and s['a2'] > 0.0]
    rflat = max(s['r1'] for s in near0)
    # the end of the hex arm is read on the CORNERS plane (the plane through the leg axis normal to Z; r = the corner radius):
    # on the flats plane a JIC thread major equal to the flats (6500 -04/-08/-12/-16: TM = Y) continues the flats line with no step
    rc = rflat * 2 / math.sqrt(3)
    S2 = segs(p, axis, sign, 2)
    on = sorted([s for s in S2 if s['k'] == 'L' and abs(s['r1'] - s['r2']) < 1e-5 and abs(s['r1'] - rc) < RIPPLE * 2 / math.sqrt(3)
                 and s['a2'] > 0.0 and s['a2'] - s['a1'] > 1e-4], key=lambda s: s['a1'])
    on = [s for s in on if s['a1'] >= on[0]['a1'] - 1e-9]
    assert on and on[0]['a1'] < rc + 0.05, ('hex corner line does not start at the crossing', rc, on[:2])
    rc_ = max(s['r1'] for s in on if s['a1'] < rc + 0.05)
    # walk the corner line from the crossing: contiguous segments at the corner radius (or a parting ripple just below it)
    steps = []; cur = None
    for s in on:
        if cur is None:
            cur = s['a2']; continue
        if s['a1'] <= cur + 1e-4:
            if abs(s['r1'] - rc_) > 1e-5: steps.append((round(s['a1'], 4), round(rc_ - s['r1'], 4)))
            cur = max(cur, s['a2'])
        else:
            break
    a_end = cur
    ripples_only = all(d <= RIPPLE and a < 0.2 for a, d in steps)
    # bore: smallest-radius long horizontal inner line
    inner = [s for s in hz if s['r1'] > 0.01 and s['a2'] - s['a1'] > 0.25 and s['r1'] < rflat - 0.02]
    bore_r = min(s['r1'] for s in inner) if inner else None
    # outline beyond the hex arm, measured from the tip (outer + inner lines with a >= a_end - 1e-4)
    endp = sorted([(round(tip - s['a2'], 4), round(s['r2'], 4), round(tip - s['a1'], 4), round(s['r1'], 4), s['k'])
                   for s in S if s['a1'] >= a_end - 1e-4 and s['r1'] + s['r2'] > 0.02], key=lambda t: (t[0], t[2], t[1]))
    return dict(axis='XY'[axis], sign=sign, tip=round(tip, 4), flats=round(2 * rflat, 4), corner_r=round(rc_, 4), hexend=round(a_end, 4), endlen=round(tip - a_end, 4),
                arm_steps=[list(x) for x in steps], arm_runs_on=ripples_only, bore=round(2 * bore_r, 4) if bore_r else None, end_prof=endp)


def measure(p):
    out = dict(step=os.path.basename(p), volume=round(volume(p), 5), bbox=bbox(p), legs=[])
    for (axis, sign), ext in legs_of(p):
        out['legs'].append(measure_leg(p, axis, sign, ext))
    return out


import os
# sizes already measured (values established before this script: SWIV_MEAS BODYS = nut face - body face, the gen_tee / gen_straight2
# end modules, the built review rows and the 2501-L fold note in gen_tee SPEC '2501'): (STEP, {leg axis: {key: expected}})
VALIDATE = [
    ('2501-L-06-04-FG', {'X': dict(tip=1.06, flats=0.5625, bore=0.297), 'Y': dict(tip=1.58, flats=0.5625, endlen=0.56, bore=0.281, arm_runs_on=True)}),
    ('6500-04-04-FG', {'X': dict(tip=0.89, endlen='JIC4'), 'Y': dict(tip=1.00, endlen=0.685, arm_runs_on=True)}),
    ('6500-08-08-FG', {'X': dict(tip=1.25, flats=0.75, endlen='JIC8', bore=0.391), 'Y': dict(tip=1.38, flats=0.75, endlen=0.885, bore=0.391, arm_runs_on=True)}),
    ('6500-12-12-FG', {'X': dict(tip=1.66, endlen='JIC12'), 'Y': dict(tip=1.75, endlen=1.089, arm_runs_on=True)}),
    ('6500-16-16-FG', {'X': dict(tip=1.81, endlen='JIC16'), 'Y': dict(tip=2.00, endlen=1.175, arm_runs_on=True)}),
]


def jic_endlen(d):
    import gen_straight2 as G
    e = G.JIC[d]
    return round(e['RL'] + (e['TM'] - e['CD']) / 2 / G.TAN60 + e['TZ'] + e['LL'] + e['SL'], 4)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--validate':
        bad = 0
        for pn, exp in VALIDATE:
            m = measure(OP.step(pn))
            for L in m['legs']:
                for k, v in exp[L['axis']].items():
                    if isinstance(v, str) and v.startswith('JIC'): v = jic_endlen(int(v[3:]))
                    got = L[k]
                    ok = (got == v) if isinstance(v, bool) else abs(got - v) <= 0.0015
                    bad += not ok
                    print(f'{pn:18} leg {L["axis"]}{"+" if L["sign"] > 0 else "-"} {k:12} measured {got!s:8} expected {v!s:8} {"ok" if ok else "MISMATCH"}')
        print('VALIDATION', 'PASSED' if not bad else f'FAILED ({bad})')
        sys.exit(1 if bad else 0)
    for p in a:
        print(json.dumps(measure(p)))
