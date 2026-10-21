# 2026-10-02 (new master 1502): OCP rebuild of a gen_tee 90 deg ELBOW whose legs are female NPTF ports (POCKET) and / or swivel ends (NPSM or
# JIC swivel: nut hex cut), from the generator's OWN data, in the macro's feature order: LEGi revolves (each leg profile V, the swivel
# cavity included), HEX1 / HEX2 arms (flats normal to Z), the 30deg double-cone corner PUCK about Z, the swivel nut hex cut (everything
# outside the nut hexagon over the nut hex length from the nut face - NutHexCutAx), then the pockets / bores (BoreCut: from the leg face
# inward, POCKETi = tap drill over DEPTH@POCKETCUTi, BOREi = the leg bore over the leg length). Threads are not modelled (the saved masters
# carry them suppressed), so the volume is the one sweep_configs reports on a saved master.
#
#   python tools/measure/elbow_model.py <root> <pn> [<pn> ...]   -> <scratch>/MODEL_<pn>.stp (scratch = $ELBOW_MODEL_OUT or tools/_out/scratch)
#   python tools/measure/elbow_model.py --all <root>             -> every configuration: solids, volume (JSON lines)
#   python tools/measure/elbow_model.py --mirror-x <in.stp> <out.stp>   -> mirror a STEP in X (a Brennan elbow drawn with its leg 1 on -X)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from nwo_model import face, vol, fuse, cut, write, revolve_leg, hex_prism, MM
from section import load

DIRS = {0: (1, 0, 0), 1: (0, 1, 0)}


def nsolids(S):
    n = 0; ex = TopExp_Explorer(S, TopAbs_SOLID)
    while ex.More(): n += 1; ex.Next()
    return n


def cyl(ax, r, a0, a1):
    """cylinder of radius r about the leg axis ax (0 = X, 1 = Y), from a0 to a1 along it"""
    o = [0.0, 0.0, 0.0]; o[ax] = a0 * MM
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*o), gp_Dir(*DIRS[ax])), r * MM, (a1 - a0) * MM).Shape()


def build(b, sp):
    assert sp.get('elbow') and not sp.get('e45'), '90 deg elbows only (legs on +X / +Y)'
    legs = b['legs']; BR = b['BR']; AC = b['AC']; steps = {}
    S = None
    for i, lg in enumerate(legs):                                            # LEG1 / LEG2 revolves
        s = revolve_leg(lg['V'], i); S = s if S is None else fuse(S, s)
    for i, lg in enumerate(legs):                                            # HEX1 / HEX2 arms
        S = fuse(S, hex_prism(i, 2 * BR, 0.0, lg['hexl']))
    h = BR; r1 = AC - BR * math.tan(math.radians(30))                        # PUCK: 30deg double cone about Z
    pk = BRepPrimAPI_MakeRevol(face([(0, 0, -h), (r1, 0, -h), (AC, 0, 0), (r1, 0, h), (0, 0, h)]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 2 * math.pi).Shape()
    S = fuse(S, pk); steps['body'] = vol(S)
    for i, lg in enumerate(legs):                                            # swivel nut hex: outside the hexagon over [Mtip - HEXL, Mtip]
        if lg['kind'] not in ('NPSMSW', 'JICSW'): continue
        a1 = lg['Mtip']; a0 = a1 - lg['m']['HEXL']; BIG = 20.0
        lo = [-BIG * MM] * 3; hi = [BIG * MM] * 3; lo[i] = a0 * MM; hi[i] = a1 * MM
        slab = BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape()
        S = cut(S, cut(slab, hex_prism(i, lg['nut_af'], a0, a1))); steps[f'NUTCUT{i + 1}'] = vol(S)
    for i, lg in enumerate(legs):                                            # pockets and bores, from the leg face inward
        if lg['kind'] == 'NPTFF':
            M = lg['V'][2][0]
            S = cut(S, cyl(i, lg['td'] / 2, M - lg['pocket'], M)); steps[f'POCKETCUT{i + 1}'] = vol(S)
            if not lg['to_centre']: S = cut(S, cyl(i, lg['conn'] / 2, 0.0, M)); steps[f'BORECUT{i + 1}'] = vol(S)
        else:
            M = lg.get('Mtip', lg['V'][-1][0])
            S = cut(S, cyl(i, lg['bore'] / 2, 0.0, M)); steps[f'BORECUT{i + 1}'] = vol(S)
    return S, steps


def mirror_x(inp, outp):
    S = load(inp); t = gp_Trsf(); t.SetMirror(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)))
    M = BRepBuilderAPI_Transform(S, t, True).Shape(); write(M, outp); return M


if __name__ == '__main__':
    import gen_tee as T
    args = sys.argv[1:]
    if args[0] == '--mirror-x':
        M = mirror_x(args[1], args[2]); print('mirrored', args[1], '->', args[2], 'volume', round(vol(M), 5)); sys.exit(0)
    out = os.environ.get('ELBOW_MODEL_OUT', OP.SCRATCH); os.makedirs(out, exist_ok=True)
    allc = args[0] == '--all'
    root = args[1] if allc else args[0]; pns = args[2:] if allc else args[1:]
    built, _ = T.build_rows(root); sp = T.SPEC[root]
    for b in built:
        if b['chk'] or (not allc and b['pn'] not in pns): continue
        S, steps = build(b, sp)
        rec = dict(pn=b['pn'], solids=nsolids(S), volume=round(vol(S), 6), steps={k: round(v, 6) for k, v in steps.items()})
        if not allc:
            p = os.path.join(out, f'MODEL_{b["pn"]}.stp'); write(S, p); rec['step'] = p
        print(json.dumps(rec), flush=True)
