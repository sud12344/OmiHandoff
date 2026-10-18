"""nptfm40.py (2026-10-18, genfeat straights) - the male NPTF end of a Brennan straight STEP, read at BOTH ends, and its relation to the
project's end library (gen_straight2 NPTF = ASME B1.20.3 / B1.20.1 basic dimensions, ENDL = the Brennan-measured end length of the 5404 table).

    python tools/measure/nptfm40.py <step> [<step> ...]          one JSON line per male NPTF end found
    python tools/measure/nptfm40.py --validate <step> [...]      + the comparison with NPTF / ENDL for the dashes the library carries
    python tools/measure/nptfm40.py --leg AXIS,SIGN <step> [...]  the male NPTF end of one elbow leg (forged elbows, e.g. 2501-40-40-FG)

Method: plugs.py (validated on the PLUGS pilots and on 5406-08-04 = ENDL[8]): plane section through the X axis; at each end the 45deg tip
chamfer, the 1.788deg blank cone (Brennan models the male thread as a plain cone, no helix), its extrapolation to the tip face, the collar
after it and the end length to the first face that steps out past the collar (hex face). The end's dash is identified from the collar
(= the pipe OD D of the dash, within 0.01) when the library carries it.
Brennan cone vs ASME: k = (cone dia at the tip face - E0) * tpi - the cone sits k pitches above the ASME pitch diameter at the small end.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, json, math
import plugs
from plugs import axial, upper, ang, frame
from ms51500 import NPTF


def ends(p):
    """the two end planes of the axial section (x min / x max) as (tip, sgn)"""
    ax, tip, head, sgn = frame(p)
    return [(tip, sgn), (head, -sgn)]


def male_end(p, tip, sgn):
    S = upper(axial(p, 0.0, tip, sgn))
    ln = [s for s in S if s[4] == 'L']
    tipch = [s for s in ln if s[0] < 1e-4 and 30 < ang(s) < 60 and s[3] > s[1]]
    if not tipch: return None
    a0 = tipch[0][2]
    cone = [s for s in ln if 1.0 < ang(s) < 3.0 and abs(s[0] - a0) < 1e-4 and s[3] > s[1]]
    if not cone: return None
    cone = cone[0]
    t = math.tan(math.radians(ang(cone)))
    r_tip = cone[1] - cone[0] * t
    collar = [s for s in ln if abs(s[1] - s[3]) < 1e-6 and abs(s[0] - cone[2]) < 2e-3 and s[1] > cone[3] - 1e-6]
    c_end = collar[0][2] if collar else cone[2]
    c_r = collar[0][1] if collar else None
    face = [s for s in ln if abs(s[0] - s[2]) < 1e-6 and abs(s[0] - c_end) < 1e-3 and max(s[1], s[3]) > (c_r or cone[3]) + 0.01]
    return dict(chamfer_len=round(a0, 4), chamfer_r_tip=round(tipch[0][1], 4), cone_angle=round(ang(cone), 3), cone_tip_dia=round(2 * r_tip, 4),
                cone_end=round(cone[2], 4), cone_end_dia=round(2 * cone[3], 4), collar_dia=round(2 * c_r, 4) if c_r else None,
                end_length=round(c_end, 4) if face else None, bore_open_at_tip=None)


def leg_male_end(p, axis, sign, pn=2):
    """the male NPTF end of an ELBOW leg (2501-40-40-FG): prof.leg_edges along the leg axis, re-expressed as distance from the leg tip"""
    from prof import leg_edges
    E = [(k, P) for k, P in leg_edges(p, axis, sign, pn) if k == 'L']
    tipa = max(max(q[0] for q in P) for k, P in E)
    S = []
    for k, P in E:
        (a1, r1), (a2, r2) = (tipa - P[0][0], P[0][1]), (tipa - P[-1][0], P[-1][1])
        if a1 > a2: a1, r1, a2, r2 = a2, r2, a1, r1
        if min(r1, r2) > -1e-6: S.append((a1, r1, a2, r2, 'L'))
    S.sort(key=lambda s: (s[0], s[2]))
    global axial
    keep = axial
    try:
        axial = lambda *_a, **_k: S          # male_end() reads the section through axial(); feed it the leg section
        return male_end(p, 0.0, 1)
    finally:
        axial = keep


def dash_of(m):
    if not m.get('collar_dia'): return None
    best = min(NPTF, key=lambda d: abs(NPTF[d][2] - m['collar_dia']))
    return best if abs(NPTF[best][2] - m['collar_dia']) < 0.011 else None


def run(p, validate=False):
    out = []
    import gen_straight2 as G       # ENDL (5404 review table) - only for --validate
    for tip, sgn in ends(p):
        m = male_end(p, tip, sgn)
        if not m: continue
        m = dict(step=_os.path.basename(p), end_x=round(tip, 4), **m)
        d = dash_of(m); m['dash'] = d
        if validate and d:
            nps, tpi, D, E0, E1, L1, L2 = NPTF[d]
            m['lib'] = dict(D=D, E0=E0, crest_tip=round(E0 + 0.8 / tpi, 4), L2=L2, ENDL=G.ENDL.get(d), tpi=tpi)
            m['k_cone_minus_E0_pitches'] = round((m['cone_tip_dia'] - E0) * tpi, 4)
            m['d_endl'] = None if m['end_length'] is None or G.ENDL.get(d) is None else round(m['end_length'] - G.ENDL[d], 4)
            m['cone_end_minus_L2'] = round(m['cone_end'] - L2, 4)
        out.append(m)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]; v = False
    if a and a[0] == '--leg':
        ax_, sg_ = (int(x) for x in a[1].split(','))
        for p in a[2:]: print(json.dumps(dict(step=_os.path.basename(p), leg=(ax_, sg_), **(leg_male_end(p, ax_, sg_) or {}))))
        sys.exit(0)
    if a and a[0] == '--validate': v = True; a = a[1:]
    for p in a:
        try:
            for m in run(p, v): print(json.dumps(m))
        except Exception as ex:
            print(json.dumps(dict(step=_os.path.basename(p), error=f'{type(ex).__name__} {ex}')))
