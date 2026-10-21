# 2026-10-02 (new masters, group NUTS-CAPS): axial-section profile walker for one-piece AXISYMMETRIC HEX parts with a female thread
# (JIC cap nut 0304-C, JIC bulkhead locknut 0306). Used by capnut.py / locknut.py on the Brennan pilot STEPs and, for the closed loop,
# on the OCP rebuild of the generator geometry (model_nutcap.py).
#
# Method (same building blocks as swiv.py / ports.py): OpenCascade plane section through the part axis (section.py / prof.py), the
# half with r >= 0 kept; the section is taken in BOTH planes through the axis that are normal to a coordinate axis - one of them runs
# through the hex CORNERS (largest radius = corner radius, shows the corner chamfers), the other through the FLATS (largest radius =
# half the across-flats). The bore outline is the same in both (axisymmetric).
#   chain(): starting at a face point, follow connected straight segments (end points equal within 1e-4 in) - the internal outline
#            from a face's inner edge inward, or the outer outline from a face's outer edge over the hex to the other face.
# Edges crossing the axis (a closed crown face, a pocket bottom) are kept as one segment from -r to +r; they are recognised as
# 'axis faces' (the chain ends there).
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import math
from prof import leg_edges, bbox

TOL = 1e-4


def axis_of(p):
    """the part axis = the axis of its cylindrical faces (thread minor bore, pocket), as a coordinate index. (The bounding-box rule of
    ports.py - the odd span out - fails on an EXACT box of a short hex part: span along the axis, across flats and across corners all
    differ; the Brennan boxes only pass it because OCC enlarges them.)"""
    from prof import shape
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopoDS import TopoDS
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder
    b = bbox(p)
    ex = TopExp_Explorer(shape(p), TopAbs_FACE)
    while ex.More():
        s = BRepAdaptor_Surface(TopoDS.Face(ex.Current()))
        if s.GetType() == GeomAbs_Cylinder:
            d = s.Cylinder().Axis().Direction(); c = [abs(d.X()), abs(d.Y()), abs(d.Z())]
            k = max(range(3), key=lambda i: c[i])
            if c[k] > 0.9999: return k, b
        ex.Next()
    sp = [b[3] - b[0], b[4] - b[1], b[5] - b[2]]
    k = max(range(3), key=lambda i: abs(sp[i] - sum(sp[j] for j in range(3) if j != i) / 2))
    return k, b


def segs(p, axis, plane_normal):
    """straight segments of the axial section (a = along the axis from the bbox minimum, r = radius), r >= 0 half; axis-crossing
    edges are returned with r1 = 0 (flag 'ax')"""
    E = leg_edges(p, axis, 1, plane_normal, a0=-99)
    a0 = min(min(q[0] for q in P) for kind, P in E)        # the exact end-face plane (the OCC bounding box is enlarged by its tolerance)
    out = []
    for kind, P in E:
        (a1, r1), (a2, r2) = P[0], P[-1]
        if kind != 'L': raise ValueError(f'non-straight edge in the section ({kind}) - the walker handles straight edges only')
        ax = False
        if min(r1, r2) < -TOL:
            if max(r1, r2) <= TOL: continue
            # crosses the axis (a face through the axis): keep the r >= 0 part
            if abs(a1 - a2) > TOL: raise ValueError('slanted edge crossing the axis')
            r1, r2 = 0.0, max(r1, r2); ax = True
        out.append(dict(a1=a1 - a0, r1=max(r1, 0.0), a2=a2 - a0, r2=max(r2, 0.0), ax=ax))
    return out


def chain(S, start, avoid=None):
    """follow connected segments from point `start` (a, r); returns the list of points; stops at a dead end or at the axis"""
    pts = [start]; used = set(avoid or ())
    cur = start
    while True:
        nxt = None
        for i, s in enumerate(S):
            if i in used: continue
            for (pa, pr), (qa, qr) in (((s['a1'], s['r1']), (s['a2'], s['r2'])), ((s['a2'], s['r2']), (s['a1'], s['r1']))):
                if abs(pa - cur[0]) < TOL and abs(pr - cur[1]) < TOL:
                    nxt = (i, (qa, qr)); break
            if nxt: break
        if not nxt: break
        used.add(nxt[0]); cur = nxt[1]; pts.append(cur)
        if cur[1] < TOL: break
    return pts


def describe(pts):
    """polyline -> list of elements: ('cyl', r, a_from, a_to) | ('cone', angle_to_axis_deg, (a,r) from, (a,r) to) | ('step', a, r_from, r_to)"""
    out = []
    for (a1, r1), (a2, r2) in zip(pts, pts[1:]):
        if abs(r1 - r2) < TOL: out.append(('cyl', round(r1, 4), round(a1, 4), round(a2, 4)))
        elif abs(a1 - a2) < TOL: out.append(('step', round(a1, 4), round(r1, 4), round(r2, 4)))
        else: out.append(('cone', round(math.degrees(math.atan2(abs(r2 - r1), abs(a2 - a1))), 2), (round(a1, 4), round(r1, 4)), (round(a2, 4), round(r2, 4))))
    return out


def planes(p):
    """(axis, length, corner-plane segments, flats-plane segments, corner radius, flats radius)"""
    axis, b = axis_of(p)
    cand = []
    for pn in [k for k in (0, 1, 2) if k != axis]:
        S = segs(p, axis, pn)
        rmax = max(max(s['r1'], s['r2']) for s in S)
        cand.append((rmax, pn, S))
    cand.sort(key=lambda c: -c[0])
    (Rc, pnc, Sc), (Rf, pnf, Sf) = cand
    L = max(max(s['a1'], s['a2']) for s in Sc)               # exact length from the section (faces at a = 0 and a = L)
    return dict(axis=axis, L=round(L, 4), Sc=Sc, Sf=Sf, Rc=round(Rc, 4), Rf=round(Rf, 4), pn_corner=pnc, pn_flats=pnf)


def face_segments(S, a, tol=2e-3):
    """vertical segments lying in the plane a (an end face)"""
    return [s for s in S if abs(s['a1'] - a) < tol and abs(s['a2'] - a) < tol]


def outer_chain(S, L, Rmax):
    """outer outline in a section: from the End A face outer point over the hex (corner or flat) to the End B face (end faces excluded,
    the walk stops on reaching the End B face plane)"""
    fa = face_segments(S, 0.0)
    if not fa: raise ValueError('no End A face in the section')
    top = max(fa, key=lambda s: max(s['r1'], s['r2']))
    start = (top['a1'] if top['r1'] >= top['r2'] else top['a2'], max(top['r1'], top['r2']))
    rest = [s for s in S if not ((abs(s['a1']) < 2e-3 and abs(s['a2']) < 2e-3) or (abs(s['a1'] - L) < 2e-3 and abs(s['a2'] - L) < 2e-3))]
    pts = [start]; cur = start; used = set()
    while abs(cur[0] - L) > 2e-3:
        nx = None
        for i, s in enumerate(rest):
            if i in used: continue
            for (pa, pr), (qa, qr) in (((s['a1'], s['r1']), (s['a2'], s['r2'])), ((s['a2'], s['r2']), (s['a1'], s['r1']))):
                if abs(pa - cur[0]) < TOL and abs(pr - cur[1]) < TOL: nx = (i, (qa, qr)); break
            if nx: break
        if not nx: break
        used.add(nx[0]); cur = nx[1]; pts.append(cur)
    return pts


def chamfers(pts, L, Rtop):
    """corner / face chamfers on an outer chain: the slanted segments touching an end face"""
    out = {}
    for (a1, r1), (a2, r2) in zip(pts, pts[1:]):
        if abs(a1 - a2) < TOL or abs(r1 - r2) < TOL: continue
        ang_face = math.degrees(math.atan2(abs(a2 - a1), abs(r2 - r1)))      # angle between the chamfer and the end FACE plane
        end = 'A' if min(a1, a2) < 2e-3 else 'B' if max(a1, a2) > L - 2e-3 else None
        if end: out[end] = dict(face_r=round(min(r1, r2), 4), top_r=round(max(r1, r2), 4), axial=round(abs(a2 - a1), 4), angle_to_face_deg=round(ang_face, 2))
    return out
