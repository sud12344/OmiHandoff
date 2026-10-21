# 2026-10-02 (new masters, group NUTS-CAPS): measure a JIC BULKHEAD LOCKNUT (0306) STEP - thin hex nut, thread through.
#   python tools/measure/locknut.py <STEP> [...]           -> one JSON line per file
#   python tools/measure/locknut.py --port <2406 STEP>     -> VALIDATION mode: the countersink reader on the female JIC port face of a 2406
#                                                             reducer (must reproduce JICF_MEAS RCS of gen_straight2 and 45deg)
# Output (inches): W (thickness), AF, corner R; through-bore chain from face A to face B: countersink A (face radius, angle to the
# axis, axial length), minor (radius, length), countersink B; hex corner chamfers at both faces.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path: _sys.path.insert(0, _HERE)
import sys, json
from nutprof import planes, chain, describe, face_segments, outer_chain, chamfers, segs, axis_of, TOL


def countersink_at(S, a):
    fs = [s for s in face_segments(S, a) if not s['ax']]
    if not fs: return None
    inner = min(fs, key=lambda s: min(s['r1'], s['r2']))
    r_in = min(inner['r1'], inner['r2']); a_in = inner['a1'] if inner['r1'] <= inner['r2'] else inner['a2']
    pts = chain([s for s in S if s is not inner], (a_in, r_in))
    return [(round(abs(x - a), 4), r) for x, r in pts]


def measure_nut(p):
    P = planes(p); W = P['L']; S = P['Sc']
    for a in (0.0, W):
        if any(s['ax'] for s in face_segments(S, a)): raise ValueError('a face crosses the axis: not a through nut')
    dep = countersink_at(S, 0.0)
    cut = next((i for i, (d, r) in enumerate(dep) if i > 0 and abs(d - W) < 2e-3), None)     # stop at the End B face plane
    if cut is not None: dep = dep[:cut + 1]
    el = describe(dep)
    out = dict(file=_os.path.basename(p), W=W, AF=round(2 * P['Rf'], 4), corner_R=P['Rc'], bore=el)
    cones = [e for e in el if e[0] == 'cone']; cyl = [e for e in el if e[0] == 'cyl']
    if len(cones) >= 2 and cyl:
        ca, cb = cones[0], cones[-1]
        out['csk_A'] = dict(face_r=ca[2][1], angle=ca[1], axial=round(abs(ca[3][0] - ca[2][0]), 4), to_r=ca[3][1])
        out['csk_B'] = dict(face_r=cb[3][1], angle=cb[1], axial=round(abs(cb[3][0] - cb[2][0]), 4), to_r=cb[2][1])
        out['minor_r'] = cyl[0][1]; out['minor_len'] = round(cyl[0][3] - cyl[0][2], 4)
    oc = outer_chain(S, W, P['Rc'])
    out['corner_chamfers'] = chamfers(oc, W, P['Rc'])
    ofl = outer_chain(P['Sf'], W, P['Rf'])
    out['flats_recesses'] = [(round(a1, 4), round(a2, 4), round(r1, 4)) for (a1, r1), (a2, r2) in zip(ofl, ofl[1:])
                             if abs(r1 - r2) < TOL and P['Rf'] - 0.01 < r1 < P['Rf'] - 1e-3]
    return out


def validate_port(p):
    axis, b = axis_of(p); L = round(b[axis + 3] - b[axis], 4)
    for pn in [k for k in (0, 1, 2) if k != axis]:
        S = segs(p, axis, pn)
        for a in (0.0, L):
            dep = countersink_at(S, a)
            if not dep: continue
            el = describe(dep)
            if el and el[0][0] == 'cone' and 40 < el[0][1] < 50:
                return dict(file=_os.path.basename(p), face_a=a, RCS=el[0][2][1], CSANG=el[0][1], to_r=el[0][3][1], axial=round(el[0][3][0], 4))
    return None


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--port':
        for f in args[1:]: print(json.dumps(validate_port(f)))
    else:
        for f in args: print(json.dumps(measure_nut(f)))
