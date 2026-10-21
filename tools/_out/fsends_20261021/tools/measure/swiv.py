import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json
from prof import leg_edges, bbox

def legs_of(p):
    b = bbox(p); ext = {(0, -1): -b[0], (0, 1): b[3], (1, -1): -b[1], (1, 1): b[4], (2, -1): -b[2], (2, 1): b[5]}
    return sorted(ext.items(), key=lambda kv: -kv[1])[:2]

def seg_list(E):
    S = []
    for kind, P in E:
        (a1, r1), (a2, r2) = P[0], P[-1]
        if a1 > a2: (a1, r1), (a2, r2) = (a2, r2), (a1, r1)
        S.append(dict(a1=a1, r1=r1, a2=a2, r2=r2, k=('L' if kind == 'L' else 'C' if isinstance(kind, tuple) else 'S'), P=P))
    return S

def near(x, y, t=2e-3): return abs(x - y) < t

NECK_RATIO = 0.9   # body neck radius behind the swivel nut < NECK_RATIO x nut skirt radius (see _measure_leg)

def measure_swivel(p, verbose=False, model=False):
    # model=True (CLI --model): the STEP is OUR OWN model (SolidWorks export of a built master, or an OCP rebuild) for the closed loop.
    # Our swivel nut has no hex chamfers and no nut/body collar, so two steps of the chain read the modelled shape instead (see
    # _measure_leg). Never use it on a Brennan STEP: there the chamfer / collar rules below must hold (2026-10-01).
    cands = []
    for (axis, sign), ext in legs_of(p):
        for pn in [k for k in (0, 1, 2) if k != axis]:
            E = leg_edges(p, axis, sign, pn, a0=0.0)
            S = [s for s in seg_list(E) if min(s['r1'], s['r2']) > -1e-6]
            if not S: continue
            af = max(max(s['a1'], s['a2']) for s in S)
            face = [s for s in S if near(s['a1'], af) and near(s['a2'], af) and s['k'] == 'L']
            if not face: continue
            # the swivel end has an inner 50deg countersink starting at the face
            cs = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 40 < math.degrees(math.atan2(s['r2'] - s['r1'], s['a2'] - s['a1'])) < 60]
            if cs:
                rmx = max(max(s['r1'], s['r2']) for s in S if s['a1'] > af - 0.5)
                cands.append((rmx, axis, sign, pn, af, S))
    # the plane through the nut hex CORNERS (largest radius) shows the 45deg rear hex chamfer.
    # 2026-10-01: the candidates are tried largest radius first and the first one on which the WHOLE swivel chain (hex chamfer, skirt,
    # neck, nut rear face, countersink, minor, relief, counterbore, nose, seat) is found wins - on a straight with a female pipe port
    # (6506) the port's ~45deg countersink also passes the face test above, and its hex can be as large as the nut (6506-12-14: both 1.375).
    # On every 6500 STEP the first candidate is the swivel (unchanged result).
    if not cands: raise ValueError('no leg end with a 40-60deg countersink at its face')
    errs = []
    for c in sorted(cands, key=lambda c: -c[0]):
        rflat = min(c_[0] for c_ in cands if (c_[1], c_[2]) == (c[1], c[2]))
        try:
            return _measure_leg(*c, rflat, model=model)
        except (ValueError, IndexError, TypeError) as ex:
            errs.append(f'leg {c[1:4]}: {type(ex).__name__} {ex}')
    raise ValueError('swivel chain not found on any candidate leg: ' + ' | '.join(errs))


def _measure_leg(rmx, axis, sign, pn, af, S, rflat, model=False):
    s_ = lambda a: round(af - a, 4)
    # outer: nut corner radius = max r in the nut region; plane may cut the corners or the flats -> also section in the other plane
    rmax = max(max(s['r1'], s['r2']) for s in S if s['a1'] > af - 0.5)
    if not model:
        # 45deg rear hex chamfer: a line at 45deg whose upper end is at rmax
        ch = [s for s in S if s['k'] in ('L', 'S') and near(max(s['r1'], s['r2']), rmax, 3e-3) and 40 < math.degrees(math.atan2(abs(s['r2'] - s['r1']), abs(s['a2'] - s['a1']) + 1e-12)) < 50]
        ch = min(ch, key=lambda s: s['a1'])
        a_foot = ch['a1']; r_foot = ch['r1']
    else:
        # our model: the hex zone ends in a vertical step from the hex radius down to the skirt front (end_JICSW VO points 1 -> 2);
        # the face itself (a = af) is not it; of the steps behind the face the one nearest the face is the hex foot
        st = [s for s in S if s['k'] == 'L' and near(s['a1'], s['a2']) and s['a1'] < af - 1e-3 and near(max(s['r1'], s['r2']), rmax, 3e-3)
              and min(s['r1'], s['r2']) < rmax - 0.005]
        st = max(st, key=lambda s: s['a1'])
        a_foot = st['a1']; r_foot = min(st['r1'], st['r2'])
    # the 8deg skirt taper: an edge ending (upper-a) within 0.03 below the foot, sloping ~8deg
    tap = [s for s in S if s['a2'] <= a_foot + 1e-6 and s['a2'] > a_foot - 0.06 and s['r2'] > s['r1'] and 2 < math.degrees(math.atan2(s['r2'] - s['r1'], s['a2'] - s['a1'] + 1e-12)) < 11]
    tap = max(tap, key=lambda s: s['a2'] - s['a1'])
    SKF, SKS_a, SKR = tap['r2'], tap['a1'], tap['r1']
    # body face: vertical outer line at the smallest a > 0.2 that rises to the body hex; neck = horizontal edge ending there
    verts = sorted([s for s in S if s['k'] == 'L' and near(s['a1'], s['a2']) and abs(s['r2'] - s['r1']) > 0.02], key=lambda s: s['a1'])
    # neck: horizontal edge with lower-a end on a vertical line (body face) and r below the nut skirt
    horiz = [s for s in S if near(s['r1'], s['r2'], 1e-3) and s['a2'] - s['a1'] > 0.02]
    # 2026-10-01: of the (body face, neck) pairs, those whose neck radius is below NECK_RATIO x the skirt radius are kept and the one
    # CLOSEST TO THE NUT (largest a) is taken; if none passes, the old rule (first pair from the leg crossing) applies. The old rule alone
    # takes, on a tee body (Brennan 6600-04-04-04-FG), a step of the run-leg hex (neck r 0.34, then 0.2529 vs skirt 0.2574) and could take
    # the far end's tip face on a straight. Measured on the 10 Brennan 6500 STEPs: neck / skirt radius = 0.57 (-04) ... 0.77 (-32) for the
    # true neck (6600-04-04-04-FG: 0.57 as 6500-04-04-FG); the only other pairs on a swivel leg are a nut lip (-32 corner plane, 0.96)
    # and the 6600 run hex (1.32 / 0.98) -> NECK_RATIO 0.9 separates them
    # (tools/_out/tier1_20261001/work/MEASURED-ENDS/evidence/swiv/neck_pairs.txt)
    pairs = []
    for v in verts:
        lo = min(v['r1'], v['r2']); hi = max(v['r1'], v['r2'])
        n_ = [h for h in horiz if near(h['a1'], v['a1']) and near(h['r1'], lo) and h['a2'] < SKS_a]
        if n_ and hi > lo + 0.05: pairs.append((v, n_[0]))
    ok = [q for q in pairs if q[1]['r1'] < NECK_RATIO * SKR]
    neck = ok[-1] if ok else pairs[0] if pairs else None
    if neck is None: raise ValueError('no body face / neck pair behind the nut')
    body_face, neck_e = neck
    NECKR = neck_e['r1']; BODYS_a = body_face['a1']
    # nut rear face: vertical outer line between the neck end and the skirt, above NECKR (Brennan: the nut/body collar keeps its lower
    # end above the neck; our model draws the rear face straight down to the neck radius -> model mode accepts it reaching NECKR)
    lo_min = NECKR - 1e-3 if model else NECKR + 0.01
    rear = [v for v in verts if BODYS_a < v['a1'] < SKS_a and min(v['r1'], v['r2']) > lo_min and max(v['r1'], v['r2']) > SKR - 0.03]
    rear = min(rear, key=lambda v: v['a1'])
    NUTL_a = rear['a1']
    # inner: countersink -> minor -> relief -> counterbore -> slot floor -> nose OD -> nose tip -> seat
    cs = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 40 < math.degrees(math.atan2(s['r2'] - s['r1'], s['a2'] - s['a1'])) < 60][0]
    MINR = cs['r1']
    minor = [h for h in horiz if near(h['a2'], cs['a1']) and near(h['r1'], MINR)][0]
    TE_a = minor['a1']
    rel = [s for s in S if near(s['a2'], TE_a) and near(s['r1'], MINR) is False and near(s['r2'], MINR) and s['r1'] > MINR]
    rel = [s for s in S if (near(s['a2'], TE_a) and near(s['r2'], MINR) and s['r1'] > MINR + 0.01)]
    RELR = rel[0]['r1']; a_rel = rel[0]['a1']
    cb = [h for h in horiz if near(h['a2'], a_rel) and near(h['r1'], RELR)][0]
    # nose OD: the largest-radius horizontal edge under the counterbore whose tip lies inside the counterbore and whose foot is at the slot floor
    nose = [h for h in horiz if h['r1'] < RELR - 0.01 and cb['a1'] < h['a2'] <= cb['a2'] + 1e-6 and h['a1'] < cb['a1'] + 0.05]
    nose = max(nose, key=lambda h: h['r1'])
    NOSER = nose['r1']; FLOOR_a = nose['a1']; TIP_a = nose['a2']
    tipv = [v for v in verts if near(v['a1'], TIP_a) and near(max(v['r1'], v['r2']), NOSER)]
    SEATR = min(tipv[0]['r1'], tipv[0]['r2'])
    AF = round(2 * rmax * math.cos(math.radians(30)), 4)
    AF_flats = round(2 * rflat, 4)
    # if the plane cut the flats, rmax is the flat radius: check against the chamfer ring / other plane later
    return dict(leg=(axis, sign, pn), face=af, rmax=round(rmax, 4), AF_if_corners=AF, AF_flats_plane=AF_flats, HEXL=s_(a_foot), SKF=round(SKF, 4), SKS=s_(SKS_a), SKR=round(SKR, 4),
                NUTL=s_(NUTL_a), NECKR=round(NECKR, 4), BODYS=s_(BODYS_a), MINR=round(MINR, 4), TE=s_(TE_a), RELR=round(RELR, 4),
                FLOOR=s_(FLOOR_a), NOSER=round(NOSER, 4), NOSETIP_B=s_(TIP_a), SEATR=round(SEATR, 4))

# 2026-10-01: position of the female JIC SWIVEL (FJS) dash among the dash groups of a Brennan part number, from the end order in the
# series names of the Brennan TFA catalog index (pp. 69-71): 6500-FG MJ-FJS, 6501-FG MP-FJS, 6502-FG MJ-FJS, 6503-FG FP-FJS,
# 6504 MJ-FJS, 6505 MP-FJS, 6506 FP-FJS, 6402-O MORB-FJS -> 2nd dash; 6600-FG MJ-MJ-FJS -> 3rd; 6602-FG MJ-FJS-MJ -> 2nd;
# 6565 FJS-FJS -> 1st (both); 6809/6810-NWO-FG MAORB-FJS -> 2nd. (The old code took the FIRST dash: 6506-12-14 was compared with SWIV_MEAS[12].)
FJS_POS = {'6500': 1, '6501': 1, '6502': 1, '6503': 1, '6504': 1, '6505': 1, '6506': 1, '6402': 1, '6600': 2, '6602': 1, '6565': 0,
           '6809': 1, '6810': 1}


def swivel_dash(path):
    import os, re
    b = os.path.basename(path)
    b = re.sub(r'^(BRENNAN_|MODEL_|SW_)', '', b, flags=re.I)
    m = re.match(r'^(\d{4})(?:-[A-Z]+)*((?:-\d\d)+)', b)
    if not m or m.group(1) not in FJS_POS: return None
    dd = [int(x) for x in m.group(2).split('-')[1:]]
    k = FJS_POS[m.group(1)]
    return dd[k] if k < len(dd) else None


if __name__ == '__main__':
    import gen_straight2 as G
    import os
    args = sys.argv[1:]; force = None
    model = '--model' in args          # closed loop on OUR model (SolidWorks STEP export / OCP rebuild): see measure_swivel
    if model: args.remove('--model')
    if '--dash' in args:
        k = args.index('--dash'); force = int(args[k + 1]); del args[k:k + 2]
    for p in args:
        m = measure_swivel(p, model=model)
        d = force if force is not None else swivel_dash(p)
        ref = G.SWIV_MEAS.get(d) if d is not None else None
        print(os.path.basename(p), 'swivel dash', d, json.dumps(m))
        if d is None: print('   swivel dash unknown for this series - pass --dash N to compare with SWIV_MEAS[N]')
        elif not ref: print('   SWIV_MEAS has no -%02d entry: these are NEW values (paste with the STEP name as source)' % d)
        if ref:
            # model mode: the nose tip (Air-Way L minus to-seat) and the nut hex (Air-Way C3) come from the configuration's row, not from
            # SWIV_MEAS -> compare them with the SW2 columns SW_NOSETIP / SW_NUTR instead
            skip = ('NOSETIP_B', 'AF') if model else ()
            diffs = {k: (m[k], ref[k]) for k in ref if k in m and k not in skip and abs(m[k] - ref[k]) > 0.0015}
            print('   vs SWIV_MEAS[%d]:' % d, 'ALL MATCH' if not diffs else diffs, '| AF', m['AF_if_corners'], ref['AF'],
                  '(model: AF and nose tip are the row values)' if model else '')
