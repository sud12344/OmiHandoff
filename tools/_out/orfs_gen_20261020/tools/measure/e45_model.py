# 45 deg swivel elbow rebuild (2026-10-01, NECK-6502): every configuration of a gen_tee 45 deg elbow with a female JIC swivel on leg 1
# (6502) rebuilt as an OCP solid from the generator's OWN data, in the macro's feature order: LEG1 / LEG2 revolves (leg 1 along +X,
# leg 2 along 135 deg), hex arms HEX1 / HEX2 (flats normal to Z), the 30deg double-cone corner PUCK about Z, the swivel neck turn
# NECKTRIM (revolve cut of the ring rin .. rout) + NECKFILL (the ring rin .. neck back), the swivel nut hex cut (outside the nut hexagon over the nut hex length), bores.
# Threads are not modelled (the saved masters carry them suppressed), so the volumes are the ones sweep_configs reports on a saved master.
#
#   python tools/measure/e45_model.py <root> <pn> [<pn> ...]   -> scratch STEPs MODEL_<pn>.stp (with the turn) and MODEL_<pn>_NOTURN.stp
#   python tools/measure/e45_model.py --all <root>              -> every configuration: one solid?, volume with / without the turn,
#                                                                  symmetric difference, and whether that matches the generator's
#                                                                  decision (corner reach > neck radius <=> the turn removes material)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from nwo_model import face, vol, fuse, cut, write, MM

UX, UY = math.cos(math.radians(135)), math.sin(math.radians(135))


def revolve(pts3, d):
    return BRepPrimAPI_MakeRevol(face(pts3), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(*d)), 2 * math.pi).Shape()


def leg_solid(V, ax):
    if ax == 'X': return revolve([(a, r, 0) for a, r in V], (1, 0, 0))
    return revolve([(a * UX - r * UY, a * UY + r * UX, 0) for a, r in V], (UX, UY, 0))


def hex_pts(af):
    Rc = af / math.sqrt(3); h = af / 2
    return [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]      # (in-plane radial, z): flats normal to Z


def hex_prism(ax, af, a0, a1):
    if ax == 'X':
        return BRepPrimAPI_MakePrism(face([(a0, u, z) for u, z in hex_pts(af)]), gp_Vec((a1 - a0) * MM, 0, 0)).Shape()
    # angled leg: radial direction n = (-UY, UX, 0) in the Front Plane (the macro's DrawProfileU mapping), axis u = (UX, UY, 0)
    pts = [(a0 * UX - q * UY, a0 * UY + q * UX, z) for q, z in hex_pts(af)]
    return BRepPrimAPI_MakePrism(face(pts), gp_Vec((a1 - a0) * UX * MM, (a1 - a0) * UY * MM, 0)).Shape()


def nsolids(S):
    n = 0; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    return n


def build(b, turn=True):
    L1, L2 = b['legs']; BR = b['BR']; AC = b['AC']; AF = b['AF']
    assert L1['kind'] == 'JICSW' and L2['kind'] == 'JICM', 'e45_model: 6502 layout only (swivel on +X, male JIC on 135 deg)'
    S = fuse(leg_solid(L1['V'], 'X'), leg_solid(L2['V'], 'U'))
    S = fuse(S, hex_prism('X', AF, 0.0, L1['hexl']))
    S = fuse(S, hex_prism('U', AF, 0.0, L2['hexl']))
    h = BR; r1 = AC - BR * math.tan(math.radians(30))
    S = fuse(S, revolve([(0, 0, -h), (r1, 0, -h), (AC, 0, 0), (r1, 0, h), (0, 0, h)], (0, 0, 1)))
    removed = None
    t = L1.get('trim')
    if turn and t:
        a1 = t['a0'] + t['len']
        v0 = vol(S)
        S = cut(S, revolve([(t['a0'], t['rin'], 0), (a1, t['rin'], 0), (a1, t['rout'], 0), (t['a0'], t['rout'], 0)], (1, 0, 0)))
        v1 = vol(S)
        S = fuse(S, revolve([(t['a0'], t['rin'], 0), (a1, t['rin'], 0), (a1, t['r'], 0), (t['a0'], t['r'], 0)], (1, 0, 0)))
        removed = dict(cut=v0 - v1, net=v0 - vol(S), ring=math.pi * (t['r'] ** 2 - t['rin'] ** 2) * t['len'])
    # swivel nut hex: outside the nut hexagon over [Mtip - HEXL, Mtip] along leg 1
    Mt = L1['Mtip']; hx = L1['m']['HEXL']; BIG = 20.0
    slab = BRepPrimAPI_MakeBox(gp_Pnt((Mt - hx) * MM, -BIG * MM, -BIG * MM), gp_Pnt(Mt * MM, BIG * MM, BIG * MM)).Shape()
    S = cut(S, cut(slab, hex_prism('X', L1['nut_af'], Mt - hx, Mt)))
    # bores from each leg face to the crossing
    S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), L1['bore'] / 2 * MM, Mt * MM).Shape())
    M2 = L2['V'][-1][0]
    S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(UX, UY, 0)), L2['bore'] / 2 * MM, M2 * MM).Shape())
    return S, removed


if __name__ == '__main__':
    import gen_tee as T
    a = sys.argv[1:]
    if a[0] == '--all':
        root = a[1]; built, _ = T.build_rows(root); bad = 0; rows = []
        for b in built:
            if b['chk']: continue
            S0, _ = build(b, turn=False); S1, rem = build(b, turn=True)
            v0, v1 = vol(S0), vol(S1); only0 = vol(cut(S0, S1)); only1 = vol(cut(S1, S0))
            t = b['legs'][0].get('trim')
            out_ = t['reach'] > t['r'] if t else False
            ok = nsolids(S1) == 1 and only1 < 1e-7 and ((only0 > 1e-6) if out_ else (only0 < 1e-7)) and (rem is None or rem['cut'] > 0.98 * rem['ring'])
            bad += not ok
            row = dict(pn=b['pn'], solids=nsolids(S1), vol_noturn=round(v0, 6), vol_turn=round(v1, 6), only_noturn=round(only0, 7), only_turn=round(only1, 7),
                       reach=t['reach'] if t else None, neckr=t['r'] if t else None, rin=t['rin'] if t else None, slab_cavity=t['cav'] if t else None, corner_out_of_neck=out_, cut_took=round(rem['cut'], 6) if rem else None,
                       neck_ring=round(rem['ring'], 6) if rem else None, ok=ok)
            rows.append(row); print(json.dumps(row))
        print(f'{root}: {len(rows)} configurations, problems {bad}')
    else:
        root = a[0]; pns = a[1:]; built, _ = T.build_rows(root)
        os.makedirs(OP.SCRATCH, exist_ok=True)
        for b in built:
            if b['pn'] not in pns: continue
            for turn, tag in ((True, ''), (False, '_NOTURN')):
                S, rem = build(b, turn)
                p = os.path.join(OP.SCRATCH, f'MODEL_{b["pn"]}{tag}.stp'); write(S, p)
                print(b['pn'], tag or '(with the turn)', 'solids', nsolids(S), 'volume %.6f in^3' % vol(S), rem or '', '->', p)
