"""straight_model.py - OCP rebuild of gen_straight2 configurations of a root with an ADJUSTABLE ORB end (SPEC flag nwo, e.g. 3474), from the
generator's own vertex chain (the DRIVE profile of the macro, checks/allcfg_check.straight_chain), in the macro's feature order:

  revolve the DRIVE chain about X -> body hex cut over its zone [START@HEXCUT, + DEPTH@HEXCUT] -> locknut hex cut over [START@NUTCUTA,
  + DEPTH@NUTCUTA] (everything outside the hexagon in that slab) -> bores DA from End A to DEPTH@BORECUT_A, DB from End B back DEPTH@BORECUT_B.
  Threads are not modelled (the macro's THD_* features are suppressed in the saved master and in its STEP export).

The hexagons are oriented like the Brennan STEPs (flats normal to Z), so the solid can be compared with the Brennan part directly.
  python tools/measure/straight_model.py 3474 "3474-12-12-NWO TEST" [--transfer] [--out <dir>] [--shift <x>]
writes <out>/MODEL_<pn>.stp (default out: tools/_out/scratch) and prints the volume, the locknut cut volume (vs the generator integral
nwo_nut_removed) and the hex cut volume. --shift moves the solid along X (e.g. -1.14 puts the body face at x = 0 like the Brennan 3474 STEP).
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE, _os.path.join(_TOOLS, 'checks')):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math
os.environ.setdefault('GS_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
MM = 25.4


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


def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()


def hex_slab_tool(af, x0, x1, big=20.0):
    """everything in x0..x1 OUTSIDE the hexagon of across-flats af about X (flats normal to Z)"""
    Rc = af / math.sqrt(3); h = af / 2
    q = [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]          # (y, z)
    hp = BRepPrimAPI_MakePrism(face([(x0, y, z) for y, z in q]), gp_Vec((x1 - x0) * MM, 0, 0)).Shape()
    slab = BRepPrimAPI_MakeBox(gp_Pnt(x0 * MM, -big * MM, -big * MM), gp_Pnt(x1 * MM, big * MM, big * MM)).Shape()
    return cut(slab, hp)


def build(b):
    """b = one built row of gen_straight2.build_rows: (cols, EA, EB, L, hexb, rB, body, chk)"""
    import allcfg_check as A
    cols, EA, EB, L, hexb, rB, body, chk = b
    V = A.straight_chain(EA, EB, L, rB)
    S = BRepPrimAPI_MakeRevol(face([(x, r, 0) for x, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 2 * math.pi).Shape()
    v_rev = vol(S); rem = {}
    s0, d0 = cols['START@HEXCUT'], cols['DEPTH@HEXCUT']
    v0 = vol(S); S = cut(S, hex_slab_tool(hexb, s0, s0 + d0)); rem['HEXCUT'] = v0 - vol(S)
    s1, d1 = cols['START@NUTCUTA'], cols['DEPTH@NUTCUTA']
    v0 = vol(S); S = cut(S, hex_slab_tool(cols['NUTHEXA@NUTHEXA'], s1, s1 + d1)); rem['NUTCUTA'] = v0 - vol(S)
    S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), cols['DA@BORE_A'] / 2 * MM, cols['DEPTH@BORECUT_A'] * MM).Shape())
    S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(L * MM, 0, 0), gp_Dir(-1, 0, 0)), cols['DB@BORE_B'] / 2 * MM, cols['DEPTH@BORECUT_B'] * MM).Shape())
    return S, v_rev, rem


def shift(S, dx):
    t = gp_Trsf(); t.SetTranslation(gp_Vec(dx * MM, 0, 0))
    return BRepBuilderAPI_Transform(S, t, True).Shape()


def write(S, path):
    w = STEPControl_Writer(); w.Transfer(S, STEPControl_AsIs); w.Write(path)


if __name__ == '__main__':
    import gen_straight2 as G
    a = sys.argv[1:]
    out = OP.SCRATCH; dx = 0.0
    if '--transfer' in a: a.remove('--transfer'); G.NWO_3474_TRANSFER = True       # (2026-10-21: the switch is on in the generator since Q-TRANSFER-ENDLIB = yes; kept for old calls)
    if '--out' in a: i = a.index('--out'); out = a[i + 1]; del a[i:i + 2]
    if '--shift' in a: i = a.index('--shift'); dx = float(a[i + 1]); del a[i:i + 2]
    root, pns = a[0], a[1:]
    built, _ = G.build_rows(root)
    os.makedirs(out, exist_ok=True)
    for b in built:
        pn = b[0]['$PRP@PartNo']
        if pns and pn not in pns: continue
        if b[7]: print(pn, 'BLOCKED', b[7]); continue
        S, v_rev, rem = build(b)
        exp = G.nwo_nut_removed(b[1]['nut'])
        if dx: S = shift(S, dx)
        path = os.path.join(out, f'MODEL_{pn.replace(" ", "_")}.stp'); write(S, path)
        print(f'{pn}: solids {nsolids(S)}, volume {vol(S):.5f} in^3 (revolve {v_rev:.5f}); HEXCUT removed {rem["HEXCUT"]:.5f}; NUTCUTA removed {rem["NUTCUTA"]:.5f} '
              f'(generator integral {exp:.5f}, diff {rem["NUTCUTA"] - exp:+.6f}) -> {path}')
