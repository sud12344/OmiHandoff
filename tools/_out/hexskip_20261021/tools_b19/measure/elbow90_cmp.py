# Closed-loop comparison of a 90 deg elbow MODEL (OCP rebuild of a gen_tee configuration, elbow90_model.py, or a SolidWorks STEP
# export of the built master) with the Brennan STEP of the same part (FOLDS, 2026-10-02).
#   1. both are measured with the SAME extractor (elbow90.py: tips, hex flats, hex-arm end, end length, bores; legs matched by their
#      tip length, so the model's leg 1 on +X meets Brennan's JIC leg on -X)
#   2. region volumes per leg, in leg coordinates: ARM = the forged hex arm away from the corner [corner radius + 0.01, hex end - 0.005],
#      END = the end module [hex end - 0.005, tip], CORNER = the rest (crossing, puck, the parting ripples); each by a boolean common with
#      a slab normal to the leg axis
#   3. cross-section area at three stations along each hex arm (slab of 0.002 / its thickness)
#   python tools/measure/elbow90_cmp.py <brennan.stp> <model.stp>  -> JSON
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, json, math
from OCP.gp import gp_Pnt
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from prof import shape
from nwo_model import vol, MM
import elbow90 as E9

BIG = 20.0


def slab(axis, sign, a0, a1, w):
    # slab normal to the leg axis, limited to +-w across it in the plane of the legs (so the other leg's swivel nut, whose corners
    # stand out past that leg's hex, never falls into this leg's slab); free along Z
    lo, hi = sorted((sign * a0, sign * a1))
    p0 = [-BIG, -BIG, -BIG]; p1 = [BIG, BIG, BIG]; p0[axis] = lo; p1[axis] = hi; p0[1 - axis] = -w; p1[1 - axis] = w
    return BRepPrimAPI_MakeBox(gp_Pnt(*[c * MM for c in p0]), gp_Pnt(*[c * MM for c in p1])).Shape()


def vin(S, axis, sign, a0, a1, w):
    return vol(BRepAlgoAPI_Common(S, slab(axis, sign, a0, a1, w)).Shape())


def regions(p, m):
    S = shape(p); tot = vol(S); out = {}
    for L in m['legs']:
        ax = 'XY'.index(L['axis']); sg = L['sign']; a_c = L['corner_r'] + 0.01; a_h = L['hexend'] - 0.005; w = L['corner_r'] + 0.1
        arm = vin(S, ax, sg, a_c, a_h, w) if a_h > a_c else 0.0
        end = vin(S, ax, sg, a_h, L['tip'] + 0.01, w)
        st = [round(a_c + (a_h - a_c) * f, 4) for f in (0.1, 0.5, 0.9)] if a_h > a_c + 0.01 else []
        area = {f'{s:.4f}': round(vin(S, ax, sg, s - 0.001, s + 0.001, w) / 0.002, 5) for s in st}
        out[f'tip{L["tip"]:.3f}'] = dict(arm=[round(a_c, 4), round(a_h, 4), round(arm, 6)], end=round(end, 6), area=area,
                                          arm_analytic=round((a_h - a_c) * (math.sqrt(3) / 2 * L['flats'] ** 2 - math.pi * (L['bore'] / 2) ** 2), 6))
    out['corner'] = round(tot - sum(v['arm'][2] + v['end'] for v in out.values()), 6)
    out['total'] = round(tot, 6)
    return out


def compare(pb, pm):
    mb, mm = E9.measure(pb), E9.measure(pm)
    rep = dict(brennan=os.path.basename(pb), model=os.path.basename(pm), legs=[])
    for Lb in mb['legs']:
        Lm = min(mm['legs'], key=lambda L: abs(L['tip'] - Lb['tip']))
        rep['legs'].append({k: (Lb[k], Lm[k]) for k in ('axis', 'tip', 'flats', 'corner_r', 'hexend', 'endlen', 'bore', 'arm_runs_on')})
        rep['legs'][-1]['end_prof_equal'] = Lb['end_prof'] == Lm['end_prof']
    rb, rm = regions(pb, mb), regions(pm, mm)
    rep['regions'] = {}
    for kb, km in zip(sorted(k for k in rb if k.startswith('tip')), sorted(k for k in rm if k.startswith('tip'))):
        rep['regions'][kb] = dict(brennan=rb[kb], model=rm[km], arm_diff=round(rm[km]['arm'][2] - rb[kb]['arm'][2], 6) if rm[km]['arm'][:2] == rb[kb]['arm'][:2] else 'arm slabs differ',
                                  end_diff=round(rm[km]['end'] - rb[kb]['end'], 6))
    rep['corner'] = dict(brennan=rb['corner'], model=rm['corner'], diff=round(rm['corner'] - rb['corner'], 6))
    rep['total'] = dict(brennan=rb['total'], model=rm['total'], diff=round(rm['total'] - rb['total'], 6))
    return rep


import os
if __name__ == '__main__':
    print(json.dumps(compare(sys.argv[1], sys.argv[2]), indent=1))
