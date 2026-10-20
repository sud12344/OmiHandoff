# A14 (user 2026-10-18 "measure the STEP"): list every cylindrical / conical face of a Brennan STEP, in inches, with its axis, the axial
# extent along that axis, and whether it is a hole (material outside) or a boss (material inside). Read-only; no table is touched.
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'measure'))
from section import load
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Cone
from OCP.BRepTools import BRepTools
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
IN = 25.4

def survey(p):
    sh = load(p)
    ns = 0; ex = TopExp_Explorer(sh, TopAbs_SOLID)
    while ex.More(): ns += 1; ex.Next()
    out = []
    ex = TopExp_Explorer(sh, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); ex.Next()
        s = BRepAdaptor_Surface(f); t = s.GetType()
        if t not in (GeomAbs_Cylinder, GeomAbs_Cone): continue
        u0, u1, v0, v1 = BRepTools.UVBounds_s(f)
        if t == GeomAbs_Cylinder:
            g = s.Cylinder(); r = g.Radius(); ang = 0.0
        else:
            g = s.Cone(); r = g.RefRadius(); ang = math.degrees(g.SemiAngle())
        ax = g.Axis(); d = ax.Direction(); o = ax.Location()
        # sample points on the face to get its axial extent and radius range
        pts = [s.Value(u0 + (u1 - u0) * i / 6, v0 + (v1 - v0) * j / 4) for i in range(7) for j in range(5)]
        dd = (d.X(), d.Y(), d.Z())
        axial = [((q.X() - o.X()) * dd[0] + (q.Y() - o.Y()) * dd[1] + (q.Z() - o.Z()) * dd[2]) / IN for q in pts]
        # hole vs boss: the face normal at the middle points toward the axis = hole
        um, vm = (u0 + u1) / 2, (v0 + v1) / 2
        from OCP.gp import gp_Pnt, gp_Vec
        P = gp_Pnt(); D1u = gp_Vec(); D1v = gp_Vec(); s.D1(um, vm, P, D1u, D1v)
        n = D1u.Crossed(D1v)
        if f.Orientation() == TopAbs_REVERSED: n.Reverse()
        # radial vector from the axis to P
        w = gp_Vec(o, P); wa = gp_Vec(*dd).Multiplied(w.Dot(gp_Vec(*dd))); rad = w.Subtracted(wa)
        hole = n.Dot(rad) < 0
        gp = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, gp); area = gp.Mass() / IN ** 2
        out.append(dict(kind='cyl' if t == GeomAbs_Cylinder else 'cone', dia=round(2 * r / IN, 4), semi_angle=round(ang, 2),
                        axis=tuple(round(x, 4) for x in dd), origin=tuple(round(x / IN, 4) for x in (o.X(), o.Y(), o.Z())),
                        a_min=round(min(axial), 4), a_max=round(max(axial), 4), sweep_deg=round(math.degrees(u1 - u0), 1),
                        hole=hole, area=round(area, 4)))
    return ns, out

if __name__ == '__main__':
    p = sys.argv[1]
    ns, out = survey(p)
    print('file', os.path.basename(p), 'solids', ns, 'cyl/cone faces', len(out))
    for c in sorted(out, key=lambda c: (c['axis'], c['dia'], c['a_min'])):
        print(json.dumps(c))
