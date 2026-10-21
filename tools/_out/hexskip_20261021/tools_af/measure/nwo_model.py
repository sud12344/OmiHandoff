# closed-loop check of the 6801 macro geometry: rebuild the reference (or any) configuration from the generator's own vertex lists with
# OCP (leg revolves, hex arms, corner puck, locknut hex cut, bores; threads not modelled), write it as a STEP and measure it with the SAME
# extractor used on the Brennan STEPs (nwo.py / nwo_chamfer.py). Also recomputes the locknut-cut volume independently.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, os, math
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.gp import gp_Ax2
MM = 25.4

def face(pts3):
    poly = BRepBuilderAPI_MakePolygon()
    for p in pts3: poly.Add(gp_Pnt(*[c * MM for c in p]))
    poly.Close()
    return BRepBuilderAPI_MakeFace(poly.Wire()).Face()

def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass() / MM ** 3

def revolve_leg(V, ax):
    pts = [(a, r, 0) if ax == 0 else (r, a, 0) for a, r in V]
    d = gp_Dir(1, 0, 0) if ax == 0 else gp_Dir(0, 1, 0)
    return BRepPrimAPI_MakeRevol(face(pts), gp_Ax1(gp_Pnt(0, 0, 0), d), 2 * math.pi).Shape()

def hexagon(ax, af, at):
    Rc = af / math.sqrt(3); h = af / 2
    q = [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]     # (in-plane other axis, z): flats normal to Z
    return [(at, u, z) if ax == 0 else (u, at, z) for u, z in q]

def hex_prism(ax, af, a0, a1):
    v = (a1 - a0) * MM
    return BRepPrimAPI_MakePrism(face(hexagon(ax, af, a0)), gp_Vec(v, 0, 0) if ax == 0 else gp_Vec(0, v, 0)).Shape()

def fuse(a, b): return BRepAlgoAPI_Fuse(a, b).Shape()
def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()

# 2026-10-01 (6802-E45): 45 deg elbows (gen_tee SPEC e45: leg 2 on the 135 deg axis, its hex arm flats normal to Z) and the corner neck trim
# ORBTRIMi (revolve cut of the generator's own trim loop about the ORB axis, after the locknut cut - the macro order). The 90 deg path is unchanged.
U135 = (math.cos(math.radians(135)), math.sin(math.radians(135)))

def revolve_leg_u(V, u):
    ux, uy = u; nx, ny = -uy, ux
    pts = [(a * ux + r * nx, a * uy + r * ny, 0) for a, r in V]
    return BRepPrimAPI_MakeRevol(face(pts), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(ux, uy, 0)), 2 * math.pi).Shape()

def hex_prism_u(u, af, a0, a1):
    ux, uy = u; nx, ny = -uy, ux; Rc = af / math.sqrt(3); h = af / 2; v = (a1 - a0) * MM
    q = [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]     # (in-plane normal of the leg, z): flats normal to Z
    return BRepPrimAPI_MakePrism(face([(a0 * ux + p * nx, a0 * uy + p * ny, z) for p, z in q]), gp_Vec(v * ux, v * uy, 0)).Shape()

def body(b, e45=False):
    """legs + hex arms + corner puck, fused (before the locknut cut, the trim and the bores)"""
    legs = b['legs']; BR = b['BR']; AC = b['AC']
    S = None
    for i, lg in enumerate(legs):
        s = revolve_leg_u(lg['V'], U135) if (e45 and i == 1) else revolve_leg(lg['V'], i); S = s if S is None else fuse(S, s)
    for i, lg in enumerate(legs):
        S = fuse(S, hex_prism_u(U135, 2 * BR, 0.0, lg['hexl']) if (e45 and i == 1) else hex_prism(i, 2 * BR, 0.0, lg['hexl']))
    # 30deg double-cone corner puck about Z
    h = BR; r1 = AC - BR * math.tan(math.radians(30)); xc = AC
    pk = BRepPrimAPI_MakeRevol(face([(0, 0, -h), (r1, 0, -h), (xc, 0, 0), (r1, 0, h), (0, 0, h)]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 2 * math.pi).Shape()
    return fuse(S, pk)

def build(b, e45=False, trim=True):
    legs = b['legs']
    if e45: assert legs[1]['kind'] != 'NWO', '45 deg elbow: the adjustable ORB leg must be leg 1 (+X)'
    S = body(b, e45)
    v_before = vol(S); removed = {}
    for i, lg in enumerate(legs):
        if lg['kind'] != 'NWO': continue
        n = lg['nut']; BIG = 20.0
        slab = BRepPrimAPI_MakeBox(gp_Pnt(-BIG * MM, n['n0'] * MM, -BIG * MM), gp_Pnt(BIG * MM, n['w0'] * MM, BIG * MM)).Shape() if i == 1 else \
               BRepPrimAPI_MakeBox(gp_Pnt(n['n0'] * MM, -BIG * MM, -BIG * MM), gp_Pnt(n['w0'] * MM, BIG * MM, BIG * MM)).Shape()
        tool = cut(slab, hex_prism(i, n['af'], n['n0'], n['w0']))
        v0 = vol(S); S = cut(S, tool); removed[i + 1] = v0 - vol(S)
    for i, lg in enumerate(legs):
        if not (trim and lg.get('nwo_trim')): continue
        assert i == 0, 'corner neck trim: adjustable ORB leg on +X only'
        tool = BRepPrimAPI_MakeRevol(face([(x, r, 0) for x, r in lg['nwo_trim_pts']]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 2 * math.pi).Shape()
        v0 = vol(S); S = cut(S, tool); removed[f'ORBTRIM{i + 1}'] = v0 - vol(S)
    for i, lg in enumerate(legs):
        M = lg.get('Mtip', lg['V'][-1][0])
        d = gp_Dir(1, 0, 0) if i == 0 else (gp_Dir(U135[0], U135[1], 0) if e45 else gp_Dir(0, 1, 0))
        S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), d), lg['bore'] / 2 * MM, M * MM).Shape())
    return S, removed

def write(S, path):
    w = STEPControl_Writer(); w.Transfer(S, STEPControl_AsIs); w.Write(path)

if __name__ == '__main__':
    import gen_tee as T
    root = sys.argv[1]; pns = sys.argv[2:]
    built, _ = T.build_rows(root)
    for b in built:
        if b['pn'] not in pns: continue
        S, removed = build(b, e45=bool(T.SPEC[root].get('e45')))
        os.makedirs(OP.SCRATCH, exist_ok=True); path = os.path.join(OP.SCRATCH, f'MODEL_{b["pn"]}.stp'); write(S, path)
        exp = {i + 1: T.nwo_nut_removed(lg['nut']) for i, lg in enumerate(b['legs']) if lg['kind'] == 'NWO'}
        print(b['pn'], 'volume', round(vol(S), 5), 'in^3; locknut cut removed (OCP)', {k: round(v, 6) for k, v in removed.items()}, 'vs generator integral', {k: round(v, 6) for k, v in exp.items()}, '->', path)
