# 2026-10-18 (genfeat PERLEGSW): closed loop for the roots with several swivel / adjustable-ORB legs. Every configuration is rebuilt in OCP
# from the generator's own data (perleg_model.build for tees, nwo_model.build for 90 deg elbows with adjustable ORB legs), written as a STEP,
# read back and measured with the extractors used on the Brennan STEPs, leg by leg:
#   female NPSM swivel: npsm.measure_npsm(..., ends=[leg], model=True, oth=<other legs>)   (section half away from the other legs)
#   female JIC swivel : swiv._measure_leg on the section of that leg (half away from the other legs)
#   adjustable ORB    : nwo.measure_nwo / nwo.parse per leg (flats-plane reading)
# plus the body hex (thin probe across the run bar / branch arm: |z| extent = flats), each leg's bore (smallest horizontal radius of its
# section) and the leg extents. The readings must return the ROW values (leg lengths, nut face / stem tip / nose tip, nut hex, body hex,
# bores) and the END-LIBRARY values (NPSM_MEAS / SWIV_MEAS / NWO_MEAS), within TOL. Threads are not modelled (suppressed in saved masters).
#   python tools/measure/perleg_closedloop.py <root> [<root> ...] [--out <dir>]     (OMI_ROOT / GT_OUT as for gen_tee)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, json, math
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
import gen_tee as T
import gen_straight2 as G
from pipetee_model import vol, nsolids, write, MM, PLACE
import perleg_model as PM
import nwo_model as NM
from prof import leg_edges, bbox, shape
from swiv import seg_list, near, _measure_leg
from npsm import measure_npsm
from nwo import measure_nwo, parse

TOL = 0.0015          # as the other closed loops (swiv.py / npsm.py model mode)
NPSM_KEYS = ('HEXL', 'SKF', 'SKS', 'SKR', 'NUTL', 'CSR', 'MINR', 'TE', 'RELR', 'RB0', 'CBR', 'CBEND', 'NECKR', 'BODY_TO_TIP', 'CONEL', 'STEMR', 'TIPR')
SWIV_KEYS = ('HEXL', 'SKF', 'SKS', 'SKR', 'NUTL', 'NECKR', 'BODYS', 'MINR', 'TE', 'RELR', 'FLOOR', 'NOSER', 'SEATR')


def half_side(ax, pn, oth):
    """rside of the section plane normal to pn for a leg on axis ax: the half away from the other legs; None = other legs on both halves"""
    o_ = [k for k in (0, 1, 2) if k not in (ax, pn)][0]
    s_o = {sg for a_, sg in oth if a_ == o_}
    return None if len(s_o) > 1 else (-s_o.pop() if s_o else 1)


def measure_swivel_leg(p, ax, sg, oth):
    cands = []
    for pn in [k for k in (0, 1, 2) if k != ax]:
        rs = half_side(ax, pn, oth)
        if rs is None: continue
        S = [s for s in seg_list(leg_edges(p, ax, sg, pn, a0=0.0, rside=rs)) if min(s['r1'], s['r2']) > -1e-6]
        if not S: continue
        af = max(max(s['a1'], s['a2']) for s in S)
        cs = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 40 < math.degrees(math.atan2(s['r2'] - s['r1'], s['a2'] - s['a1'])) < 60]
        if cs: cands.append((max(max(s['r1'], s['r2']) for s in S if s['a1'] > af - 0.5), ax, sg, pn, af, S))
    c = max(cands, key=lambda c: c[0]); rflat = min(c_[0] for c_ in cands)
    m = _measure_leg(*c, rflat, model=True)
    m['AF'] = m['AF_if_corners'] if c[3] == 2 else m['AF_flats_plane']     # plane z = 0 holds the nut corners (flats normal to Z)
    return m, c[5]


def leg_bore(p, ax, sg, oth, amax):
    """bore radius of a leg: the smallest-radius horizontal edge of its section (half away from the other legs) inside the leg"""
    for pn in [k for k in (0, 1, 2) if k != ax]:
        rs = half_side(ax, pn, oth)
        if rs is None: continue
        S = seg_list(leg_edges(p, ax, sg, pn, a0=0.0, rside=rs))
        h = [s for s in S if near(s['r1'], s['r2'], 1e-4) and s['r1'] > 0.01 and s['a2'] - s['a1'] > 0.05 and s['a2'] <= amax + 1e-6 and s['a2'] > 0.3 * amax]
        if h: return round(2 * min(s['r1'] for s in h), 4)
    return None


def probe_flats(S, ax, at):
    """|z| half-extent of the solid in a thin probe across axis ax at coordinate `at` (the other in-plane coordinate |u| <= 0.0005)"""
    d = 0.0005; lo = [-d, -d, -5.0]; hi = [d, d, 5.0]; lo[ax] = at - d; hi[ax] = at + d
    C = BRepAlgoAPI_Common(S, BRepPrimAPI_MakeBox(gp_Pnt(*[v * MM for v in lo]), gp_Pnt(*[v * MM for v in hi])).Shape()).Shape()
    b = Bnd_Box(); BRepBndLib.Add_s(C, b)
    return round(max(-b.CornerMin().Z(), b.CornerMax().Z()) / MM, 4)


def clip_leg(S, ax, sg, a_clip, R):
    """the part of the solid beyond a_clip along the signed leg axis and within R of it (the other legs and the run bar / branch arm corners
    cut away), so the section extractors see one leg only, in both section planes (on a tee the corner plane of the branch also holds both
    run legs; a perpendicular swivel nut can reach past this leg's body face, far out along its own axis - hence the radial limit R)"""
    BIG = 20.0; lo = [-R] * 3; hi = [R] * 3; lo[ax] = -BIG; hi[ax] = BIG
    if sg > 0: lo[ax] = a_clip
    else: hi[ax] = -a_clip
    return BRepAlgoAPI_Common(S, BRepPrimAPI_MakeBox(gp_Pnt(*[v * MM for v in lo]), gp_Pnt(*[v * MM for v in hi])).Shape()).Shape()


def cmp(out, tag, got, want, tol=TOL):
    ok = got is not None and want is not None and abs(got - want) <= tol
    out.append((tag, got, round(want, 4) if want is not None else None, ok))


def rowdict(root):
    h, rows = T.load_review(root)
    return {r['$PRP@PartNo']: r for r in rows}


def check_tee(root, b, row, outd):
    sp = T.SPEC[root]; c = b['cols']; res = []
    S, st = PM.build(b, sp); p = os.path.join(outd, f'MODEL_{b["pn"]}.stp'); write(S, p)
    info = dict(solids=nsolids(S), volume=round(vol(S), 6), nutcut={k: round(v, 6) for k, v in st.items() if k.startswith('NUTCUT')})
    res.append(('one solid', info['solids'], 1, info['solids'] == 1))
    bb = bbox(p)
    legs4 = T.legs4(sp)
    for i, (L, (kind, lc, bc, tc)) in enumerate(zip(b['legs'], legs4), 1):
        ax, sg = T.PLACE[i]; oth = [T.PLACE[j] for j in range(1, len(b['legs']) + 1) if j != i]
        ext = bb[3] if (ax, sg) == (0, 1) else -bb[0] if (ax, sg) == (0, -1) else bb[4]
        # clip beyond the final reach of the perpendicular legs and the body hex corner (the nut-slab rule keeps it below this leg's nut),
        # and before this leg's body face where possible
        perp = [o for j, o in enumerate(b['legs'], 1) if T.PLACE[j][0] != ax]
        a_clip = max([T.final_reach(o) for o in perp] + [b['AC']]) + 0.003
        if kind in ('NPSMSW', 'JICSW', 'NPTFM'): a_clip = min(a_clip, L['hexl'] - 0.01)
        pl = os.path.join(outd, f'MODEL_{b["pn"]}_leg{i}.stp'); write(clip_leg(S, ax, sg, a_clip, max(T.final_reach(L), b['AC']) + 0.01), pl); oth = []
        if kind in ('NPSMSW', 'JICSW'):
            e_ = T.leg_end(sp, i - 1); W = row[e_[0]] if kind == 'NPSMSW' else row[lc]       # nut face
            cmp(res, f'leg {i} extent = nut face', ext, W)
            if kind == 'NPSMSW':
                lib = G.NPSM_MEAS[L['dash']]; m = measure_npsm(pl, ends=[(ax, sg)], model=True, oth=oth, win=lib['NUTL'] + 0.02)
                cmp(res, f'leg {i} NPSM nut face ({e_[0].split("@")[0]})', m['face'], W)
                cmp(res, f'leg {i} NPSM stem tip ({lc.split("@")[0]})', round(m['face'] - m['TIP_B'], 4), row[lc])
                af = m['AF'] if m['end'][2] == 2 else m['AF_flats_plane']
                cmp(res, f'leg {i} nut hex ({e_[1].split("@")[0]})', af, row[e_[1]], 0.002)
                for k in NPSM_KEYS: cmp(res, f'leg {i} NPSM {k} (NPSM_MEAS[{L["dash"]}])', m[k], lib[k])
            else:
                m, _ = measure_swivel_leg(pl, ax, sg, oth); lib = G.SWIV_MEAS[L['dash']]
                cmp(res, f'leg {i} JIC swivel nut face ({lc.split("@")[0]})', round(m['face'], 4), W)
                cmp(res, f'leg {i} JIC swivel nose tip ({e_[0].split("@")[0]})', round(m['face'] - m['NOSETIP_B'], 4), row[e_[0]])
                cmp(res, f'leg {i} nut hex ({e_[1].split("@")[0]})', m['AF'], row[e_[1]], 0.002)
                for k in SWIV_KEYS: cmp(res, f'leg {i} JIC swivel {k} (SWIV_MEAS[{L["dash"]}])', m[k], lib[k])
            cmp(res, f'leg {i} bore ({bc.split("@")[0]})', leg_bore(pl, ax, sg, oth, L['Mtip']), row[bc])
        else:
            cmp(res, f'leg {i} extent ({lc.split("@")[0]})', ext, row[lc])
            if kind != 'NPTFF': cmp(res, f'leg {i} bore ({bc.split("@")[0]})', leg_bore(pl, ax, sg, oth, row[lc]), row[bc])
            else: cmp(res, f'leg {i} tap drill ({bc.split("@")[0]})', leg_bore(pl, ax, sg, oth, row[lc]), row[bc] if row[bc] is not None else G.FPT[L['dash']]['TD'])
    # body hex: the run bar outside the branch arm (|x| between the hex corner and the body face), the branch arm above the run bar corners
    AC = b['AC']; hx = sp['hex']
    for nm, ax, a0, a1 in (('run bar +X', 0, AC, c['HEXL1@RUN_BODY']), ('run bar -X', 0, -c['HEXL2@RUN_BODY'], -AC), ('branch arm', 1, AC, c['HEXL@HEX3_BODY'])):
        if abs(a1 - a0) > 0.03: cmp(res, f'body hex {nm} ({hx.split("@")[0]})', round(2 * probe_flats(S, ax, (a0 + a1) / 2), 4), row[hx], 0.002)
    return res, info


def check_nwo_elbow(root, b, row, outd):
    sp = T.SPEC[root]; res = []
    S, removed = NM.build(b); p = os.path.join(outd, f'MODEL_{b["pn"]}.stp'); write(S, p)
    info = dict(solids=nsolids(S), volume=round(vol(S), 6), nutcut={k: round(v, 6) for k, v in removed.items()},
                nutcut_expect={i + 1: round(T.nwo_nut_removed(L['nut']), 6) for i, L in enumerate(b['legs'])})
    res.append(('one solid', info['solids'], 1, info['solids'] == 1))
    for i in info['nutcut']: cmp(res, f'NUTCUT{i} removed (generator integral)', info['nutcut'][i], info['nutcut_expect'][i], 0.005 * info['nutcut_expect'][i])
    rd = {}
    for leg, at, pts in measure_nwo(p):
        M = parse(at, pts)
        if len(M) < 6: continue
        t, u, w, n, k, bo = M[:6]
        if not (u[2] < t[2] and w[2] > u[2] and k[2] < n[2]): continue
        cand = dict(tip=round(at, 4), TM=round(2 * t[2], 4), UR=round(u[2], 4), THDL=round(at - u[0], 4), WR=round(w[2], 4), WT=round(w[0] - w[1], 4),
                    NUTR=round(n[2], 4), NUTT=round(n[0] - n[1], 4), NECKR=round(k[2], 4), I3=round(at - k[1], 4), BODYR=round(bo[2], 4))
        key = (leg[0], leg[1])
        if key not in rd or cand['NUTR'] < rd[key]['NUTR']: rd[key] = cand
    for i, (L, (kind, lc, bc, tc)) in enumerate(zip(b['legs'], T.legs4(sp)), 1):
        ax, sg = T.place(sp)[i]; m = rd.get((ax, sg)); e_ = T.leg_end(sp, i - 1); lib = T.NWO_MEAS[L['dash']]
        if m is None: res.append((f'leg {i} adjustable ORB reading', None, None, False)); continue
        cmp(res, f'leg {i} tip ({lc.split("@")[0]})', m['tip'], row[lc])
        cmp(res, f'leg {i} tip to body face (I3 {e_[0]})', m['I3'], L['endlen'])
        cmp(res, f'leg {i} locknut hex ({e_[1].split("@")[0]})', round(2 * m['NUTR'], 4), row[e_[1]], 0.002)
        cmp(res, f'leg {i} thread major ({tc.split("@")[0]})', m['TM'], row[tc])
        cmp(res, f'leg {i} ORB thread length ({e_[2]})', m['THDL'], L['cols'][f'NW{i}_THDL@LEG{i}'])
        cmp(res, f'leg {i} undercut dia ({e_[3]})', round(2 * m['UR'], 4), round(2 * L['UR'], 4))
        for k in ('NECKR', 'NUTT', 'WR', 'WT'): cmp(res, f'leg {i} {k} (NWO_MEAS[{L["dash"]}])', m[k], lib[k])
        cmp(res, f'leg {i} body flats ({sp["hex"].split("@")[0]})', round(2 * m['BODYR'], 4), row[sp['hex']], 0.002)
    return res, info


if __name__ == '__main__':
    args = sys.argv[1:]; out = OP.SCRATCH
    if '--out' in args: k = args.index('--out'); out = args[k + 1]; del args[k:k + 2]
    allbad = 0
    for root in args:
        sp = T.SPEC[root]; built, _ = T.build_rows(root); rows = rowdict(root); outd = os.path.join(out, root); os.makedirs(outd, exist_ok=True)
        recs = []
        for b in built:
            if b['chk']: continue
            res, info = (check_nwo_elbow if sp.get('elbow') else check_tee)(root, b, rows[b['pn']], outd)
            bad = [r for r in res if not r[3]]; allbad += len(bad)
            print(f'{b["pn"]}: {len(res)} checks, {len(bad)} off; solids {info["solids"]}, volume {info["volume"]} in^3, nut cuts {info["nutcut"]}'
                  + (f' (expect {info["nutcut_expect"]})' if 'nutcut_expect' in info else ''), flush=True)
            for r in bad: print('    OFF', r)
            recs.append(dict(pn=b['pn'], info=info, checks=[list(r) for r in res]))
        json.dump(recs, open(os.path.join(out, f'results_{root}.json'), 'w'), indent=1, default=str)
    print('PERLEGSW closed loop', 'PASS' if not allbad else f'FAIL ({allbad} checks off)')
