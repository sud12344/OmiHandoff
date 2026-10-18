import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json
from prof import leg_edges, bbox
from swiv import seg_list, near, legs_of
from ports import ends_of, ang

def measure_npsm(p, ends=None, model=False):
    # 2026-10-02 (new master 1502): ends = [(axis, sign)] of the swivel leg on an ELBOW (the default ends_of() assumes a straight);
    # model=True: the STEP is OUR model (OCP rebuild / SolidWorks export) for the closed loop - our nut has no 45deg rear hex chamfer
    # and no nut/body collar, so the hex foot is the vertical step from the nut corner radius to the skirt front and the nut rear
    # face runs down to the neck (never use it on a Brennan STEP)
    cands = []
    for axis, sign in (ends or ends_of(p)):
        # elbow (ends given): the other leg = the other of the two largest extents; in the plane that contains it, read the side away from it
        oth_ = [l for l, _ in legs_of(p) if l[0] != axis] if ends else []
        for pn in [k for k in (0, 1, 2) if k != axis]:
            o_ = [k for k in (0, 1, 2) if k not in (axis, pn)][0]
            rs_ = -oth_[0][1] if oth_ and oth_[0][0] == o_ else 1
            S = [s for s in seg_list(leg_edges(p, axis, sign, pn, a0=-99, rside=rs_)) if min(s['r1'], s['r2']) > -1e-6]
            af = max(max(s['a1'], s['a2']) for s in S)
            cs = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 40 < ang(s) < 50]
            if cs: cands.append((max(max(s['r1'], s['r2']) for s in S if s['a1'] > af - 0.6), axis, sign, pn, af, S, cs[0]))
    rmax, axis, sign, pn, af, S, cs = max(cands, key=lambda c: c[0])
    rflat = min(c[0] for c in cands if (c[1], c[2]) == (axis, sign))
    s_ = lambda a: round(af - a, 4)
    horiz = [s for s in S if near(s['r1'], s['r2'], 1e-3) and s['a2'] - s['a1'] > 0.004]
    verts = [s for s in S if s['k'] == 'L' and near(s['a1'], s['a2']) and abs(s['r2'] - s['r1']) > 0.004]
    if not model:
        ch = [s for s in S if near(max(s['r1'], s['r2']), rmax, 3e-3) and 40 < ang(s) < 50 and s['a1'] < af - 0.1]
        ch = min(ch, key=lambda s: s['a1']); a_foot, SKF = ch['a1'], ch['r1']
    else:
        st = [s for s in verts if s['a1'] < af - 0.05 and near(max(s['r1'], s['r2']), rmax, 3e-3) and min(s['r1'], s['r2']) < rmax - 0.005]
        st = max(st, key=lambda s: s['a1']); a_foot, SKF = st['a1'], min(st['r1'], st['r2'])
    sk = [s for s in S if near(s['a2'], a_foot) and near(s['r2'], SKF) and s['r1'] < SKF - 0.005 and 4 < ang(s) < 25]
    sk = sk[0]; SKS_a, SKR = sk['a1'], sk['r1']
    # inner nut: countersink -> minor -> 45deg relief -> relief radius -> step up to the counterbore -> counterbore end
    CSR, MINR = cs['r2'], cs['r1']
    mn = [h for h in horiz if near(h['a2'], cs['a1']) and near(h['r1'], MINR)][0]; TE_a = mn['a1']
    rel = [s for s in S if near(s['a2'], TE_a) and near(s['r2'], MINR) and s['r1'] > MINR + 0.005 and 40 < ang(s) < 50][0]
    RB0_a, RELR = rel['a1'], rel['r1']
    up = [v for v in verts if near(v['a1'], RB0_a) and near(min(v['r1'], v['r2']), RELR)]
    CBR = max(up[0]['r1'], up[0]['r2']) if up else RELR
    cb = [h for h in horiz if near(h['a2'], RB0_a) and near(h['r1'], CBR)][0]
    cb_end = cb['a1']
    # 2026-10-02: the fillet may come as a B-spline edge ('S'; Brennan 1502-08-08-FG, plane through the nut corners)
    fil = [s for s in S if s['k'] in ('C', 'S') and near(s['a2'], cb_end) and near(s['r2'], CBR) and s['a1'] < cb_end - 1e-4 and s['r1'] < CBR - 1e-4]
    if fil: cb_end = fil[0]['a1']
    # stem: tip face (vertical, from the bore to TIPR) at the largest a below the counterbore; 30deg cone; stem OD
    cone = [s for s in S if 25 < ang(s) < 35 and s['r1'] > s['r2'] and s['r1'] < MINR and s['a1'] > cb_end - 0.05 and s['a2'] < af]
    cone = max(cone, key=lambda s: s['a2'])
    tip_a, TIPR = cone['a2'], cone['r2']; cone_a, STEMR = cone['a1'], cone['r1']
    # outer rear: body face = vertical outer line rising from the neck to the body; neck = horizontal at its foot
    bf = None
    for v in sorted(verts, key=lambda v: v['a1']):
        lo, hi = min(v['r1'], v['r2']), max(v['r1'], v['r2'])
        n_ = [h for h in horiz if near(h['a1'], v['a1']) and near(h['r1'], lo) and h['a2'] < SKS_a]
        if n_ and hi > lo + 0.05 and v['a1'] < tip_a - 0.1: bf = (v, n_[0]); break
    body_face, neck = bf; NECKR = neck['r1']; BODY_a = body_face['a1']
    rear = [v for v in verts if BODY_a < v['a1'] < SKS_a and min(v['r1'], v['r2']) > (NECKR - 1e-3 if model else NECKR + 0.01) and max(v['r1'], v['r2']) > SKR - 0.03 and max(v['r1'], v['r2']) > CBR]
    rear = min(rear, key=lambda v: v['a1']); NUTL_a = rear['a1']
    AF = round(2 * rmax * math.cos(math.radians(30)), 4)
    return dict(end=(axis, sign, pn), face=round(af, 4), AF=AF, AF_flats_plane=round(2 * rflat, 4), HEXL=s_(a_foot), SKF=round(SKF, 4), SKS=s_(SKS_a), SKR=round(SKR, 4),
                NUTL=s_(NUTL_a), CSR=round(CSR, 4), MINR=round(MINR, 4), TE=s_(TE_a), RELR=round(RELR, 4), RB0=s_(RB0_a), CBR=round(CBR, 4), CBEND=s_(cb_end),
                NECKR=round(NECKR, 4), BODY_TO_TIP=round(tip_a - BODY_a, 4), CONEL=round(tip_a - cone_a, 4), STEMR=round(STEMR, 4), TIPR=round(TIPR, 4), TIP_B=s_(tip_a))

if __name__ == '__main__':
    import gen_straight2 as G
    args = sys.argv[1:]; ends = None; model = '--model' in args
    if model: args.remove('--model')
    if '--leg' in args:      # 2026-10-02: the swivel leg of an elbow, e.g. --leg 1,1 (axis Y, + side)
        k = args.index('--leg'); ends = [tuple(int(v) for v in args[k + 1].split(','))]; del args[k:k + 2]
    for p in args:
        m = measure_npsm(p, ends=ends, model=model); print(p.split('/')[-1], json.dumps(m))
        if '1404-08-08' in p:
            ref = G.NPSM_MEAS[8]
            d = {k: (m[k], ref[k]) for k in ref if k in m and isinstance(ref[k], float) and abs(m[k] - ref[k]) > 0.0015}
            print('   vs NPSM_MEAS[8]:', 'ALL MATCH' if not d else d)
