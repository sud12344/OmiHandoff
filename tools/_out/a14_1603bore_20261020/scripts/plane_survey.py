# A14 cross-check: planar faces of a Brennan STEP grouped by normal direction and offset from the origin (inches) -> hex flats across.
import os, sys, math, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'measure'))
from section import load
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
IN = 25.4
sh = load(sys.argv[1]); seen = collections.defaultdict(list)
ex = TopExp_Explorer(sh, TopAbs_FACE)
while ex.More():
    f = TopoDS.Face(ex.Current()); ex.Next(); s = BRepAdaptor_Surface(f)
    if s.GetType() != GeomAbs_Plane: continue
    pl = s.Plane(); n = pl.Axis().Direction(); o = pl.Location()
    nn = [n.X(), n.Y(), n.Z()]
    k = max(range(3), key=lambda i: abs(nn[i]))
    if nn[k] < 0: nn = [-x for x in nn]
    d = (o.X() * nn[0] + o.Y() * nn[1] + o.Z() * nn[2]) / IN
    g = GProp_GProps(); BRepGProp.SurfaceProperties_s(f, g); c = g.CentreOfMass()
    seen[tuple(round(x, 3) for x in nn)].append((round(d, 4), tuple(round(v / IN, 3) for v in (c.X(), c.Y(), c.Z()))))
for n, L in sorted(seen.items()):
    print('normal', n, 'offsets', sorted(set(d for d, _ in L)))
    for d, c in sorted(L): print('    ', d, 'centroid', c)
