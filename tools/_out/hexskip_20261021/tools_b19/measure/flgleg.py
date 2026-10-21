# FLANGE LEG of a forged elbow (2026-10-18, genfeat flange: Q-NEW-FLG61LEG / Q-NEW-FLG62LEG, DESIGN 4.11 "flgleg.py"): plane sections through
# the leg axis of a STEP, read with the tools/measure/flange62.py outline helpers (flange62.head is the head reader validated on the 9 Brennan
# 1700 STEPs = FLG61_MEAS and on the 1800-08-08 / 1824-08 / 1804-08-08-FG code 62 heads = FLG62_MEAS[8]).
#
#   python tools/measure/flgleg.py <step> <axis 0|1|2> <sign +1|-1> [...]   one JSON line per STEP: the leg whose axis is <sign> x <axis>
#
# Returns, in leg coordinates (a = distance from the axis crossing, origin of the STEP): M = the flange face, the head (O, TH, GI, GO, GD and the
# head back face), the bore D of the leg (smallest long horizontal line from the face), and the outline radius 0.01 behind the head back face in
# the plane where the hex shows its FLATS (radial coordinate = Z: flats normal to Z, as gen_tee and the Brennan forgings) and in the plane where it
# shows its CORNERS: = the hex flats / corner radius when the forged hex arm runs up to the head (the model), = a neck radius on the Brennan parts.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, json
from flange62 import segs, head, bore, r_at


def measure_leg(p, axis, sign):
    inplane = [k for k in (0, 1) if k != axis]
    assert axis in (0, 1) and inplane, 'the flange leg must lie in the XY plane (flats normal to Z)'
    pn_flats = inplane[0]        # section plane normal to the other in-plane axis: radial coordinate = Z -> the hex flats
    pn_corners = 2               # section plane z = 0: radial coordinate = the other in-plane axis -> the hex corners
    out = dict(step=_os.path.basename(p), axis='XYZ'[axis], sign=sign)
    for tag, pn in (('flats', pn_flats), ('corners', pn_corners)):
        S = [s for s in segs(p, axis, sign, pn) if s['a2'] > 1e-6]
        af = max(s['a2'] for s in S)
        H = head(S, af)
        if H is None: out[tag] = dict(error='no flange head found at the leg end'); continue
        out[tag] = dict(M=round(af, 4), head=H, r_behind_head=round(r_at(S, H['back'] - 0.01), 4), bore=bore(S, 0.0, af))
    f, c = out.get('flats', {}), out.get('corners', {})
    if 'head' in f and 'head' in c:
        out['M'] = f['M']; out['head'] = f['head']; out['bore'] = f['bore']
        out['flats_r_behind_head'] = f['r_behind_head']; out['corners_r_behind_head'] = c['r_behind_head']
        out['head_same_in_both_planes'] = all(abs(f['head'][k] - c['head'][k]) < 2e-4 for k in ('O', 'TH', 'GI', 'GO', 'GD'))
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    for k in range(0, len(a), 3):
        print(json.dumps(measure_leg(a[k], int(a[k + 1]), int(a[k + 2]))))
