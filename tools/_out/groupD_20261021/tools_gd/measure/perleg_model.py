# 2026-10-18 (genfeat PERLEGSW, Q-NEW-PERLEGSW): OCP rebuild of a gen_tee TEE with several swivel legs (female JIC swivel / female NPSM
# swivel on +X, -X and / or +Y, plus male / female pipe or male JIC legs) from the configuration's SW2 values and leg profiles (build_rows),
# in the macro's feature order: LEGi revolves (each leg profile V about its signed axis, the swivel cavity included), the RUN hex bar along X
# (-HEXL2 .. +HEXL1) and the HEX3 branch arm along +Y (0 .. HEXL3), flats normal to Z; then every swivel nut hex cut in leg order
# (NutHexCutAx: everything outside the nut hexagon over DEPTH@NUTCUTi from the nut face inward), then the pockets / bores (BoreCut: from the leg
# face inward; POCKETi = tap drill over DEPTH@POCKETCUTi, BOREi = Di over DEPTH@BORECUTi). Threads are not modelled (the saved masters carry
# every THD_ feature suppressed). 90 deg elbows with adjustable ORB legs (6807): nwo_model.build. Written as a STEP and measured with the
# Brennan extractors in perleg_closedloop.py.
#   python tools/measure/perleg_model.py <root> [<pn> ...] [--out <dir>]      (OMI_ROOT / GT_OUT as for gen_tee)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from pipetee_model import PLACE, revolve_leg, hex_prism, drill, fuse, cut, vol, nsolids, write, MM


def nut_cut_tool(ax, sg, af, a0, a1):
    """the NutHexCutAx tool of a leg on signed axis (ax, sg): the slab a0 .. a1 along the leg (leg coordinates) minus the nut hexagon prism"""
    BIG = 20.0; lo = [-BIG * MM] * 3; hi = [BIG * MM] * 3
    x0, x1 = sorted((sg * a0, sg * a1)); lo[ax] = x0 * MM; hi[ax] = x1 * MM
    return cut(BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape(), hex_prism(ax, af, x0, x1))


def build(b, sp):
    assert not sp.get('elbow') and not sp.get('cross'), 'tees only (90 deg elbows with adjustable ORB legs: nwo_model.build)'
    c = b['cols']; legs = b['legs']; steps = {}
    S = None
    for i, lg in enumerate(legs, 1):                                           # LEG1..3
        ax, sg = PLACE[i]; s = revolve_leg(lg['V'], ax, sg); S = s if S is None else fuse(S, s)
    S = fuse(S, hex_prism(0, c['HEXAF@RUN'], -c['HEXL2@RUN_BODY'], c['HEXL1@RUN_BODY']))      # RUN
    S = fuse(S, hex_prism(1, c['HEXAF@HEX3'], 0.0, c['HEXL@HEX3_BODY']))                      # HEX3
    steps['body'] = vol(S)
    for i, lg in enumerate(legs, 1):                                           # NUTHEXi / NUTCUTi
        if lg['kind'] not in ('JICSW', 'NPSMSW'): continue
        ax, sg = PLACE[i]; a1 = c[f'M{i}@LEG{i}']; a0 = a1 - c[f'DEPTH@NUTCUT{i}']
        v0 = vol(S); S = cut(S, nut_cut_tool(ax, sg, c[f'NUTHEX{i}@NUTHEX{i}'], a0, a1)); steps[f'NUTCUT{i}'] = v0 - vol(S)
    steps['solids_after_hex'] = nsolids(S)
    for i, lg in enumerate(legs, 1):                                           # pockets / bores
        ax, sg = PLACE[i]; M = lg.get('Mtip', lg['V'][-1][0])
        if lg['kind'] == 'NPTFF':
            S = cut(S, drill(ax, sg, M, c[f'TAPDRILL{i}@POCKET{i}'], c[f'DEPTH@POCKETCUT{i}']))
            if f'D{i}@BORE{i}' in c: S = cut(S, drill(ax, sg, M, c[f'D{i}@BORE{i}'], c[f'DEPTH@BORECUT{i}']))
        else:
            S = cut(S, drill(ax, sg, M, c[f'D{i}@BORE{i}'], c[f'DEPTH@BORECUT{i}']))
    return S, steps


if __name__ == '__main__':
    import gen_tee as T
    args = sys.argv[1:]; out = OP.SCRATCH
    if '--out' in args: k = args.index('--out'); out = args[k + 1]; del args[k:k + 2]
    root, pns = args[0], args[1:]
    sp = T.SPEC[root]; built, _ = T.build_rows(root); os.makedirs(out, exist_ok=True)
    for b in built:
        if b['chk'] or (pns and b['pn'] not in pns): continue
        S, st = build(b, sp); path = os.path.join(out, f'MODEL_{b["pn"]}.stp'); write(S, path)
        print(b['pn'], 'solids', nsolids(S), 'volume', round(vol(S), 5), {k: round(v, 6) for k, v in st.items()}, '->', path)
