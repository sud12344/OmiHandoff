# 2026-10-02 (new masters, group NUTS-CAPS): measure a JIC CAP NUT (0304-C) STEP - closed hex crown + female 37deg JIC cavity.
#   python tools/measure/capnut.py <STEP> [...]            -> one JSON line per file
#   python tools/measure/capnut.py --port <2406 STEP>      -> VALIDATION mode: the same cavity walker on the female JIC port of a 2406
#                                                             reducer (must reproduce JICF_MEAS of gen_straight2: minor-bore depth P,
#                                                             37deg seat starting there)
# Output (inches; depths measured FROM THE OPEN FACE):
#   L, AF (2 x flats radius), corner R; cavity chain from the open face: thread minor (radius, depth), optional relief / tap-drill
#   bore (radius, end depth = seat start), seat (angle to the axis, end radius, end depth), pocket (radius, bottom depth), crown
#   thickness (L - pocket bottom); hex corner chamfers at both ends; flats recesses (marking) reported, not used.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path: _sys.path.insert(0, _HERE)
import sys, json, math
from nutprof import planes, chain, describe, face_segments, outer_chain, chamfers, segs, axis_of, TOL


def cavity(S, L, open_at):
    """inner chain from the open face (a = open_at) inward; returns depth-based elements"""
    fs = [s for s in face_segments(S, open_at) if not s['ax']]
    if not fs: raise ValueError(f'no open face ring at a={open_at}')
    inner = min(fs, key=lambda s: min(s['r1'], s['r2']))
    r_in = min(inner['r1'], inner['r2']); a_in = inner['a1'] if inner['r1'] <= inner['r2'] else inner['a2']
    others = [s for s in S if s is not inner]
    pts = chain(others, (a_in, r_in))
    dep = [(round(abs(a - open_at), 4), r) for a, r in pts]
    return dep, describe(dep)


def measure_cap(p):
    P = planes(p); L = P['L']; S = P['Sc']
    # open face = the end whose face does NOT cross the axis
    ends = {}
    for a in (0.0, L):
        fs = face_segments(S, a)
        ends[a] = any(s['ax'] for s in fs)
    closed = [a for a, ax in ends.items() if ax]; opened = [a for a, ax in ends.items() if not ax]
    if len(closed) != 1 or len(opened) != 1: raise ValueError(f'not a cap: faces crossing the axis at {closed}, open at {opened}')
    dep, el = cavity(S, L, opened[0])
    out = dict(file=_os.path.basename(p), L=L, AF=round(2 * P['Rf'], 4), corner_R=P['Rc'], open_end='B' if opened[0] > 0 else 'A', cavity=el)
    # interpret: minor cyl, [relief step + cyl], seat cone, pocket cyl, bottom step to the axis
    cyl = [e for e in el if e[0] == 'cyl']; cone = [e for e in el if e[0] == 'cone']
    out['minor_r'] = cyl[0][1]; out['minor_depth'] = cyl[0][3]
    seat = [e for e in cone if 30 < e[1] < 40]
    if seat:
        s = seat[0]; out['seat_angle'] = s[1]; out['seat_start'] = dict(depth=s[2][0], r=s[2][1]); out['seat_end'] = dict(depth=s[3][0], r=s[3][1])
        rel = [e for e in cyl[1:] if e[3] <= s[2][0] + TOL]
        if rel: out['relief'] = dict(r=rel[-1][1], from_depth=rel[-1][2], to_depth=rel[-1][3])
        pk = [e for e in cyl if e[2] >= s[3][0] - TOL]
        if pk: out['pocket'] = dict(r=pk[0][1], from_depth=pk[0][2], bottom_depth=pk[0][3]); out['crown'] = round(L - pk[0][3], 4)
    oc = outer_chain(S, L, P['Rc'])
    out['corner_chamfers'] = chamfers(oc, L, P['Rc'])
    ofl = outer_chain(P['Sf'], L, P['Rf'])
    rec = [(round(a1, 4), round(a2, 4), round(r1, 4)) for (a1, r1), (a2, r2) in zip(ofl, ofl[1:]) if abs(r1 - r2) < TOL and r1 < P['Rf'] - 1e-3 and r1 > P['Rf'] - 0.01]
    out['flats_recesses'] = rec
    return out


def validate_port(p):
    """the same cavity walker on the female JIC port (2406): find the port end (45deg countersink at a face), walk inward"""
    axis, b = axis_of(p)
    L = round(b[axis + 3] - b[axis], 4)
    for pn in [k for k in (0, 1, 2) if k != axis]:
        S = segs(p, axis, pn)
        for a in (0.0, L):
            fs = [s for s in face_segments(S, a) if not s['ax']]
            if not fs: continue
            try:
                dep, el = cavity(S, L, a)
            except ValueError:
                continue
            cones = [e for e in el if e[0] == 'cone']
            if cones and 40 < cones[0][1] < 50 and cones[0][2][0] < 1e-3:
                cyl = [e for e in el if e[0] == 'cyl']
                seat = [e for e in cones if 30 < e[1] < 40]
                return dict(file=_os.path.basename(p), port_face_a=a, RCS=cones[0][2][1], CSANG=cones[0][1], MINR=cyl[0][1], P=cyl[0][3],
                            seat_angle=seat[0][1] if seat else None, seat_start_depth=seat[0][2][0] if seat else None,
                            seat_end=dict(depth=seat[0][3][0], r=seat[0][3][1]) if seat else None)
    return None


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--port':
        for f in args[1:]: print(json.dumps(validate_port(f)))
    else:
        for f in args: print(json.dumps(measure_cap(f)))
