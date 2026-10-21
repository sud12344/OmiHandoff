"""dump_step.py: every analytic face of a Brennan STEP (inches; the STEPs are in mm) - planes (normal, offset, area), cylinders
(axis, location, dia, axial extent), cones, tori (centre, axis, major R, tube dia 2r) and the bounding box. Used to decode the
bent-tube records (group D, 2026-10-21).   python dump_step.py <stp> [...]"""
import sys, math, collections
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
MM = 25.4
F = getattr(TopoDS, 'Face', None) or TopoDS.Face_s


def load(p):
    r = STEPControl_Reader()
    assert r.ReadFile(p) == IFSelect_RetDone, p
    r.TransferRoots()
    return r.OneShape()


def faces(s):
    ex = TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        yield F(ex.Current())
        ex.Next()


def bget(b):
    lo, hi = b.CornerMin(), b.CornerMax()
    return [lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z()]


def fbox(f):
    b = Bnd_Box(); BRepBndLib.Add_s(f, b)
    return [v / MM for v in bget(b)]


def area(f):
    g = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g)
    return g.Mass() / MM / MM


def dump(p):
    s = load(p)
    b = Bnd_Box(); BRepBndLib.Add_s(s, b)
    print('#', p); print('BOX', ' '.join(f'{v / MM:.4f}' for v in bget(b)))
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); print(f'VOL {g.Mass() / MM**3:.5f} in^3')
    rows = []
    for f in faces(s):
        a = BRepAdaptor_Surface(f)
        t = a.GetType()
        bx = fbox(f)
        bxs = '[' + ' '.join(f'{v:.3f}' for v in bx) + ']'
        if t == GeomAbs_Plane:
            pl = a.Plane(); n = pl.Axis().Direction(); q = pl.Location()
            d = (n.X() * q.X() + n.Y() * q.Y() + n.Z() * q.Z()) / MM
            rows.append(f'PLANE n=({n.X():+.4f},{n.Y():+.4f},{n.Z():+.4f}) d={d:+.4f} A={area(f):.4f} {bxs}')
        elif t == GeomAbs_Cylinder:
            c = a.Cylinder(); ax = c.Axis(); dd = ax.Direction(); q = ax.Location()
            rows.append(f'CYL  dia={2 * c.Radius() / MM:.4f} ax=({dd.X():+.4f},{dd.Y():+.4f},{dd.Z():+.4f}) at=({q.X() / MM:.4f},{q.Y() / MM:.4f},{q.Z() / MM:.4f}) {bxs}')
        elif t == GeomAbs_Cone:
            c = a.Cone(); ax = c.Axis(); dd = ax.Direction(); q = ax.Location()
            rows.append(f'CONE ang={math.degrees(c.SemiAngle()):.2f} refdia={2 * c.RefRadius() / MM:.4f} ax=({dd.X():+.4f},{dd.Y():+.4f},{dd.Z():+.4f}) at=({q.X() / MM:.4f},{q.Y() / MM:.4f},{q.Z() / MM:.4f}) {bxs}')
        elif t == GeomAbs_Torus:
            c = a.Torus(); ax = c.Axis(); dd = ax.Direction(); q = ax.Location()
            rows.append(f'TOR  R={c.MajorRadius() / MM:.4f} tube_dia={2 * c.MinorRadius() / MM:.4f} ax=({dd.X():+.4f},{dd.Y():+.4f},{dd.Z():+.4f}) at=({q.X() / MM:.4f},{q.Y() / MM:.4f},{q.Z() / MM:.4f}) {bxs}')
        else:
            rows.append(f'OTHER type {t} {bxs}')
    for r in rows:
        print(r)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        dump(p)
