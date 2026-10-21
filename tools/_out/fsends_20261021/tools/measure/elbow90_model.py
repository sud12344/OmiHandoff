# 90 deg ELBOW rebuild (FOLDS, 2026-10-02): a gen_tee 90 deg elbow configuration (SPEC elbow=True, not e45) rebuilt as an OCP solid
# from the generator's OWN data, in the macro's feature order: LEG1 / LEG2 revolves (leg 1 along +X, leg 2 along +Y), hex arms HEX1 /
# HEX2 (flats normal to Z, from the crossing to each leg's hexl), the 30deg double-cone corner PUCK about Z (nwo_model.body), the swivel
# nut hex cut NUTCUT<i> of a female JIC / NPSM swivel leg (outside the nut hexagon over [Mtip - HEXL, Mtip]), the leg bores from the
# crossing to each leg's tip (Mtip for a swivel leg = DEPTH@BORECUT). Threads are not modelled (the saved masters carry them suppressed),
# so the volumes are the ones sweep_configs reports on a saved master. Adjustable ORB (NWO) legs and 45 deg elbows: nwo_model.py /
# e45_model.py.
#
#   python tools/measure/elbow90_model.py <root> <pn> [<pn> ...]   -> scratch STEPs MODEL_<pn>.stp + volume
#   python tools/measure/elbow90_model.py --all <root>             -> every configuration: one solid?, volume (JSON lines)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from nwo_model import vol, cut, write, MM, body, hex_prism


def nsolids(S):
    n = 0; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    return n


def build(b):
    legs = b['legs']
    assert len(legs) == 2 and all(lg['kind'] in ('JICM', 'NPTFM', 'NPTFF', 'JICSW', 'NPSMSW') for lg in legs), [lg['kind'] for lg in legs]
    assert not any(lg['kind'] == 'NPTFF' for lg in legs), 'female pipe legs (collar, pocket) are not rebuilt here'
    S = body(b, e45=False)
    BIG = 20.0
    for i, lg in enumerate(legs):
        if lg['kind'] not in ('JICSW', 'NPSMSW'): continue
        Mt = lg['Mtip']; hx = lg['m']['HEXL']
        slab = (BRepPrimAPI_MakeBox(gp_Pnt((Mt - hx) * MM, -BIG * MM, -BIG * MM), gp_Pnt(Mt * MM, BIG * MM, BIG * MM)) if i == 0 else
                BRepPrimAPI_MakeBox(gp_Pnt(-BIG * MM, (Mt - hx) * MM, -BIG * MM), gp_Pnt(BIG * MM, Mt * MM, BIG * MM))).Shape()
        S = cut(S, cut(slab, hex_prism(i, lg['nut_af'], Mt - hx, Mt)))
    for i, lg in enumerate(legs):
        M = lg.get('Mtip', lg['V'][-1][0])
        d = gp_Dir(1, 0, 0) if i == 0 else gp_Dir(0, 1, 0)
        S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), d), lg['bore'] / 2 * MM, M * MM).Shape())
    return S


if __name__ == '__main__':
    import gen_tee as T
    a = sys.argv[1:]
    if a[0] == '--all':
        root = a[1]; built, _ = T.build_rows(root)
        assert T.SPEC[root].get('elbow') and not T.SPEC[root].get('e45')
        bad = 0
        for b in built:
            if b['chk']: continue
            S = build(b); n = nsolids(S); bad += n != 1
            print(json.dumps(dict(pn=b['pn'], solids=n, volume=round(vol(S), 6))))
        print(f'{root}: {sum(1 for b in built if not b["chk"])} configurations, not one solid: {bad}')
    else:
        root = a[0]; pns = a[1:]; built, _ = T.build_rows(root)
        os.makedirs(OP.SCRATCH, exist_ok=True)
        for b in built:
            if b['pn'] not in pns: continue
            S = build(b); p = os.path.join(os.environ.get('MODEL_OUT', OP.SCRATCH), f'MODEL_{b["pn"]}.stp'); write(S, p)
            print(b['pn'], 'solids', nsolids(S), 'volume %.6f in^3' % vol(S), '->', p)
