import sys, itertools, collections
from OCP.STEPControl import STEPControl_Reader
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TopoDS import TopoDS
r=STEPControl_Reader(); r.ReadFile(sys.argv[1]); r.TransferRoots(); s=r.OneShape()
pl=[]; cyl=collections.Counter()
e=TopExp_Explorer(s,TopAbs_FACE)
while e.More():
    f=TopoDS.Face(e.Current()); a=BRepAdaptor_Surface(f)
    if a.GetType()==GeomAbs_Plane:
        p=a.Plane(); n=p.Axis().Direction(); o=p.Location()
        g=GProp_GProps(); BRepGProp.SurfaceProperties_s(f,g)
        pl.append(((n.X(),n.Y(),n.Z()),(o.X(),o.Y(),o.Z()),g.Mass()))
    elif a.GetType()==GeomAbs_Cylinder: cyl[round(a.Cylinder().Radius()*2/25.4,3)]+=1
    e.Next()
out=collections.Counter()
for (n1,o1,a1),(n2,o2,a2) in itertools.combinations(pl,2):
    d=sum(x*y for x,y in zip(n1,n2))
    if abs(abs(d)-1)<1e-6:
        dist=abs(sum((b-a)*c for a,b,c in zip(o1,o2,n1)))/25.4
        if dist>0.3: out[(round(dist,3), tuple(round(abs(x),3) for x in n1))]+=1
for k,v in sorted(out.items()): 
    if 0.9<k[0]<1.3: print('gap',k,v)
print('cyl dias', sorted(cyl.items()))
