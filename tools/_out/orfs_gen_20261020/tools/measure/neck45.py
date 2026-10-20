# swivel-leg body face / neck clearance extractor for forged elbows (2026-10-01, work item NECK-6502).
#
#   python tools/measure/neck45.py <step> <ang_deg> [<step> <ang_deg> ...]
#
# The swivel leg lies in the XY plane through the origin (the axis crossing) at <ang_deg> from +X (Brennan 6502 / 1503: 45,
# Brennan 6500: 90, the gen_tee 45 deg elbow model: 0). From the solid's own B-rep:
#   face     the swivel BODY FACE: the planar face normal to the leg axis, nearest the crossing, whose inner edge is a circle on the
#            axis (the neck) and whose outer edge reaches past the neck by > 0.05 (the forged hex arm end)
#   neckr    the radius of that inner circle (= the neck)
#   face_rmax  the largest distance of the body face from the leg axis (= the hex corner radius where the face reaches the corners)
#   nut_face   the farthest point of the solid along the leg axis (= the swivel nut face; gen_tee: Air-Way M5 / M6)
# Then the solid is SECTIONED by planes normal to the leg axis from face + 0.002 outward (step 0.002) and, per plane, the largest
# distance of the section from the leg axis (rmax) is recorded until rmax jumps above the neck by > 0.03 (= the swivel nut rear face):
#   nut_rear the first plane where the nut appears
#   excess   max(rmax - neckr) over the planes between the body face and the nut: 0 = nothing stands outside the neck past the
#            body face (the corner is TRIMMED at the face); > 0 = the corner puck / the other hex arm stand out of the neck there
#   past     rmax in the first plane past the face (face + 0.002)
# Validated (2026-10-01) on the sizes modelled before: Brennan 6500-08-08-FG / 6500-12-12-FG (body face = nut face - SWIV_MEAS BODYS,
# neck = SWIV_MEAS NECKR, both measured with swiv.py) and Brennan 6502-08-08-FG (body face 0.395, corner radius 0.433: BRENNAN_NOTES).
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Circle, GeomAbs_Line
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir
from section import load

IN = 25.4


def _pts(edge, n=96):
    c = BRepAdaptor_Curve(edge); t0, t1 = c.FirstParameter(), c.LastParameter()
    k = 1 if c.GetType() == GeomAbs_Line else n
    return [c.Value(t0 + (t1 - t0) * j / k) for j in range(k + 1)], c


def _leg(p, d):
    x, y, z = p.X() / IN, p.Y() / IN, p.Z() / IN
    a = x * d[0] + y * d[1]
    return a, math.sqrt(max(0.0, x * x + y * y + z * z - a * a))


def planar_faces(shape, d):
    """planar faces normal to the leg axis: (a, rho_min, rho_max, inner circle radii on the axis)"""
    out = []
    ex = TopExp_Explorer(shape, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); s = BRepAdaptor_Surface(f)
        if s.GetType() == GeomAbs_Plane:
            ax = s.Plane().Axis(); n = ax.Direction()
            if abs(abs(n.X() * d[0] + n.Y() * d[1]) - 1) < 1e-6:
                lo = gp_Pnt(ax.Location().X(), ax.Location().Y(), ax.Location().Z())
                a0 = (lo.X() * d[0] + lo.Y() * d[1]) / IN
                rmin, rmax, circ = 1e9, 0.0, []
                ee = TopExp_Explorer(f, TopAbs_EDGE)
                while ee.More():
                    e = TopoDS.Edge(ee.Current()); P, c = _pts(e)
                    for q in P:
                        _, r = _leg(q, d); rmin = min(rmin, r); rmax = max(rmax, r)
                    if c.GetType() == GeomAbs_Circle:
                        ci = c.Circle(); cc = ci.Location(); ca, cr = _leg(cc, d)
                        if cr < 1e-5: circ.append(round(ci.Radius() / IN, 4))
                    ee.Next()
                out.append((round(a0, 4), rmin, rmax, sorted(set(circ))))
        ex.Next()
    return sorted(out)


def rmax_at(shape, d, a):
    o = gp_Pnt(a * IN * d[0], a * IN * d[1], 0.0)
    sec = BRepAlgoAPI_Section(shape, gp_Pln(o, gp_Dir(d[0], d[1], 0.0))); sec.Build(); sh = sec.Shape()
    r = 0.0; ex = TopExp_Explorer(sh, TopAbs_EDGE)
    while ex.More():
        P, _ = _pts(TopoDS.Edge(ex.Current()))
        for q in P: r = max(r, _leg(q, d)[1])
        ex.Next()
    return r


def tip_along(shape, d):
    """the farthest point of the solid along the leg direction (vertices + sampled edges) = the swivel NUT FACE for a swivel leg"""
    a = -1e9; ex = TopExp_Explorer(shape, TopAbs_EDGE)
    while ex.More():
        P, _ = _pts(TopoDS.Edge(ex.Current()), 24)
        for q in P: a = max(a, _leg(q, d)[0])
        ex.Next()
    return a


def merged_planes(F):
    """coplanar planar faces merged into one entry (a, rho_min, rho_max, axis circles): a modelled body face can come split at the leg
    revolve's hex-flats circle (annulus neck .. flats + hexagon outside it); Brennan's body faces are one face"""
    G = {}
    for a0, rmin, rmax, circ in F:
        g = G.setdefault(round(a0, 4), [1e9, 0.0, set()])
        g[0] = min(g[0], rmin); g[1] = max(g[1], rmax); g[2] |= set(circ)
    return sorted((k, g[0], g[1], sorted(g[2])) for k, g in G.items())


def measure(path, ang):
    sh = load(path); d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    F = planar_faces(sh, d)
    # body face: nearest the crossing (a > 0.05), its inner edge a circle on the axis (the neck), the face reaching > 0.05 past it
    body = [f for f in merged_planes(F) if f[0] > 0.05 and f[3] and abs(f[1] - min(f[3])) < 1e-3 and f[2] - f[1] > 0.05]
    face, neckr, face_rmax, circ = body[0]; neckr = round(neckr, 4)
    prof = []; a = face + 0.002; nut = None
    while a < face + 1.5:
        r = rmax_at(sh, d, a); prof.append((round(a, 4), round(r, 4)))
        if len(prof) > 1 and r > prof[-2][1] + 0.03: nut = a; break      # the swivel nut rear face (a step up, not the shrinking puck)
        a += 0.002
    slab = [r for (aa, r) in prof if nut is None or aa < nut - 1e-9]
    return dict(file=_os.path.basename(path), ang=ang, nut_face=round(tip_along(sh, d), 4), face=face, neckr=neckr, face_rmax=round(face_rmax, 4), past=prof[0][1],
                excess=round(max(slab) - neckr, 4), nut_rear=round(nut, 3) if nut else None,
                profile=prof[:6] + ([('...',)] if len(prof) > 8 else []) + prof[-2:],
                planar_faces=[(f[0], round(f[1], 4), round(f[2], 4), f[3]) for f in F if f[0] > 0][:8])


if __name__ == '__main__':
    args = sys.argv[1:]
    for k in range(0, len(args), 2):
        m = measure(args[k], float(args[k + 1]))
        print(json.dumps(m))
