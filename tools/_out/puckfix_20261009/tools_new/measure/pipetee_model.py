# 2026-10-02 (PIPE-TEES): closed-loop rebuild of a gen_tee TEE / CROSS configuration (not elbows) with OCP, from the generator's own data -
# the same features the macro draws, in the same order: leg revolves LEGi (profile V about the leg axis), the RUN hex bar along X
# (-HEXL2 .. +HEXL1), the branch hex arm HEX3 along +Y (0 .. HEXL3) or, on a cross, the RUN2 bar along Y (-HEXL4 .. +HEXL3), all with flats
# normal to Z; then the NPTFF pockets (TAPDRILLi dia from the leg face, depth DEPTH@POCKETCUTi), their connecting bores where the table
# carries one, and the male / JIC leg bores (Di dia from the tip to the crossing). Threads are not modelled (suppressed in the saved masters).
# The rebuild is written as a STEP and measured with the SAME extractor as the Brennan STEPs (pipetee.py).
#   python tools/measure/pipetee_model.py <root> <pn> [<pn> ...] [--out <dir>]      (OMI_ROOT / GT_OUT as for gen_tee)
# (named pipetee_model.py, not tee_model.py: the JIC-TEES group of the same wave adds its own tools/measure/tee_model.py)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
MM = 25.4
PLACE = {1: (0, +1), 2: (0, -1), 3: (1, +1), 4: (1, -1)}      # = gen_tee.PLACE (tees / crosses)


def face(pts3):
    poly = BRepBuilderAPI_MakePolygon()
    for p in pts3: poly.Add(gp_Pnt(*[c * MM for c in p]))
    poly.Close()
    return BRepBuilderAPI_MakeFace(poly.Wire()).Face()


def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass() / MM ** 3


def nsolids(s):
    n = 0; ex = TopExp_Explorer(s, TopAbs_SOLID)
    while ex.More(): n += 1; ex.Next()
    return n


def pt(ax, sg, a, r, z=0.0):
    """leg coordinates (a along the leg from the crossing, r in the Front Plane across it) -> model xyz"""
    return (sg * a, r, z) if ax == 0 else (r, sg * a, z)


def revolve_leg(V, ax, sg):
    d = gp_Dir(sg, 0, 0) if ax == 0 else gp_Dir(0, sg, 0)
    return BRepPrimAPI_MakeRevol(face([pt(ax, sg, a, r) for a, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), d), 2 * math.pi).Shape()


def hex_prism(ax, af, a0, a1):
    """hex bar along axis ax from coordinate a0 to a1 (signed), flats normal to Z"""
    Rc = af / math.sqrt(3); h = af / 2
    q = [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]
    pts = [(a0, u, z) if ax == 0 else (u, a0, z) for u, z in q]
    v = (a1 - a0) * MM
    return BRepPrimAPI_MakePrism(face(pts), gp_Vec(v, 0, 0) if ax == 0 else gp_Vec(0, v, 0)).Shape()


def drill(ax, sg, face_a, dia, depth):
    """cylinder of dia from the leg face (at a = face_a) inward over depth"""
    o = pt(ax, sg, face_a, 0.0); d = gp_Dir(-sg, 0, 0) if ax == 0 else gp_Dir(0, -sg, 0)
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*[c * MM for c in o]), d), dia / 2 * MM, depth * MM).Shape()


def fuse(a, b): return BRepAlgoAPI_Fuse(a, b).Shape()
def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()


def build(b, cross):
    cols = b['cols']; legs = b['legs']; AF = cols['HEXAF@RUN']
    S = None
    for i, lg in enumerate(legs, 1):
        ax, sg = PLACE[i]; s = revolve_leg(lg['V'], ax, sg); S = s if S is None else fuse(S, s)
    S = fuse(S, hex_prism(0, AF, -cols['HEXL2@RUN_BODY'], cols['HEXL1@RUN_BODY']))
    if cross: S = fuse(S, hex_prism(1, cols['HEXAF@RUN2'], -cols['HEXL2@RUN2_BODY'], cols['HEXL1@RUN2_BODY']))
    else: S = fuse(S, hex_prism(1, cols['HEXAF@HEX3'], 0.0, cols['HEXL@HEX3_BODY']))
    v_body = vol(S)
    for i, lg in enumerate(legs, 1):
        ax, sg = PLACE[i]; M = lg.get('Mtip', lg['V'][-1][0])
        if lg['kind'] == 'NPTFF':
            S = cut(S, drill(ax, sg, M, cols[f'TAPDRILL{i}@POCKET{i}'], cols[f'DEPTH@POCKETCUT{i}']))
            if f'D{i}@BORE{i}' in cols: S = cut(S, drill(ax, sg, M, cols[f'D{i}@BORE{i}'], cols[f'DEPTH@BORECUT{i}']))
        else:
            S = cut(S, drill(ax, sg, M, cols[f'D{i}@BORE{i}'], cols[f'DEPTH@BORECUT{i}']))
    return S, v_body


def write(S, path):
    w = STEPControl_Writer(); w.Transfer(S, STEPControl_AsIs); w.Write(path)


if __name__ == '__main__':
    import gen_tee as T
    args = sys.argv[1:]; out = OP.SCRATCH
    if '--out' in args: k = args.index('--out'); out = args[k + 1]; del args[k:k + 2]
    root, pns = args[0], args[1:]
    sp = T.SPEC[root]; assert not sp.get('elbow'), 'tees / crosses only (elbows: nwo_model.py / e45_model.py)'
    built, _ = T.build_rows(root)
    os.makedirs(out, exist_ok=True)
    for b in built:
        if pns and b['pn'] not in pns: continue
        S, vb = build(b, bool(sp.get('cross')))
        path = os.path.join(out, f'MODEL_{b["pn"]}.stp'); write(S, path)
        print(b['pn'], 'solids', nsolids(S), 'volume', round(vol(S), 5), 'in^3 (body before the bores', round(vb, 5), ') ->', path)
