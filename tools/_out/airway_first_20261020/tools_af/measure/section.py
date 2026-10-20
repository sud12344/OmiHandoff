import sys, math
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.gp import gp_Pln, gp_Pnt, gp_Dir
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_SOLID
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.GeomAbs import GeomAbs_Line, GeomAbs_Circle
from OCP.TopoDS import TopoDS
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

def load(p):
    r = STEPControl_Reader(); st = r.ReadFile(p); assert st == IFSelect_RetDone
    r.TransferRoots(); return r.OneShape()

def section(shape, n=(0, 0, 1), o=(0, 0, 0)):
    s = BRepAlgoAPI_Section(shape, gp_Pln(gp_Pnt(*o), gp_Dir(*n)))
    s.Build(); return s.Shape()

def edges(sh, IN=25.4, npts=24):
    out = []
    ex = TopExp_Explorer(sh, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge(ex.Current()); c = BRepAdaptor_Curve(e)
        t0, t1 = c.FirstParameter(), c.LastParameter()
        typ = c.GetType()
        if typ == GeomAbs_Line: pts = [c.Value(t0), c.Value(t1)]; kind = 'L'
        elif typ == GeomAbs_Circle:
            pts = [c.Value(t0 + (t1 - t0) * k / npts) for k in range(npts + 1)]; kind = 'C'
            ci = c.Circle(); ctr = ci.Location(); kind = ('C', (ctr.X() / IN, ctr.Y() / IN, ctr.Z() / IN), ci.Radius() / IN)
        else: pts = [c.Value(t0 + (t1 - t0) * k / npts) for k in range(npts + 1)]; kind = 'S%d' % typ
        out.append((kind, [(p.X() / IN, p.Y() / IN, p.Z() / IN) for p in pts]))
        ex.Next()
    return out

if __name__ == '__main__':
    p = sys.argv[1]; sh = load(p)
    nsol = 0; ex = TopExp_Explorer(sh, TopAbs_SOLID)
    while ex.More(): nsol += 1; ex.Next()
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(sh, g)
    b = Bnd_Box(); BRepBndLib.Add_s(sh, b); xmin, ymin, zmin = b.CornerMin().X(), b.CornerMin().Y(), b.CornerMin().Z(); xmax, ymax, zmax = b.CornerMax().X(), b.CornerMax().Y(), b.CornerMax().Z()
    print('solids', nsol, 'volume in3 %.5f' % (g.Mass() / 25.4 ** 3), 'bbox', [round(v / 25.4, 4) for v in (xmin, ymin, zmin, xmax, ymax, zmax)])
