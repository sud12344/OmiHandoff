# 2026-10-09 (wave 2, HOSEB + PERLEGSW; 2026-10-18 genfeat HOSEB: the table's corner puck, see body()): OCP closed loop of the new elbow configurations (4601 / 4603 hose elbows with the face-off, 6807
# double adjustable-ORB elbow). Rebuilds a configuration from the generator's own build_rows() data IN THE MACRO'S FEATURE ORDER (leg revolves,
# hex arms, corner puck - nwo_model.body; then the face-off HOSEFACEi cut + STUBFILLi refill from the SW2 face-off values; the locknut hex cuts;
# the bores; threads not modelled), writes a STEP, reads it back and measures it:
#   * one solid; locknut cut volume = nwo_nut_removed() (the macro's NutHexCutNWO expectation); face-off cut >= the stub ring, refill = the stub
#     ring exactly, net change (< 0 where the corner stood past the hose hex face, 0 where it clears);
#   * nothing of the forged corner past the hose hex face outside the stub (90 deg: up to the other leg's hex arm end; 45 deg: any direction),
#     up to the bead: volume of the solid in that region = 0;
#   * hose leg from the STEP faces: coaxial cylinders stub rS / bead rA / bore, planes normal to the hose axis at the hex face, the bead edges
#     and the tip; NO face left by the face-off (no cylinder at rin, no plane at the face-off end);
#   * every adjustable-ORB leg from the STEP with the SAME extractor used on the Brennan 6801 STEPs (nwo.measure_nwo / parse, per leg): tip,
#     I3, thread length, undercut, washer, nut, neck = the generator's values.
# usage: hoseb_model.py <root> [<pn> ...]   (env as gen_tee: OMI_ROOT, GT_OUT; HB_OUT = folder for the STEPs and results.json)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeRevol
from OCP.gp import gp_Ax1
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
import nwo_model as NM
from nwo_model import MM, vol, fuse, cut, hex_prism, write
from nwo import measure_nwo, parse, walk, key as nkey
from prof import leg_edges
from swiv import seg_list
from prof import shape


def cyl(u, a0, a1, r):
    """solid cylinder of radius r about the leg axis u (through the origin) from a0 to a1"""
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(a0 * u[0] * MM, a0 * u[1] * MM, 0), gp_Dir(u[0], u[1], 0)), r * MM, (a1 - a0) * MM).Shape()


def ring(u, a0, a1, r0, r1): return cut(cyl(u, a0, a1, r1), cyl(u, a0, a1, r0))


def box(x0, y0, z0, x1, y1, z1): return BRepPrimAPI_MakeBox(gp_Pnt(x0 * MM, y0 * MM, z0 * MM), gp_Pnt(x1 * MM, y1 * MM, z1 * MM)).Shape()


def nsolids(S):
    e = TopExp_Explorer(S, TopAbs_SOLID); n = 0
    while e.More(): n += 1; e.Next()
    return n


def axes(e45): return [(1.0, 0.0), NM.U135 if e45 else (0.0, 1.0)]


def body(b, e45):
    """2026-10-18 (genfeat HOSEB, batch-16 base): nwo_model.body with the corner puck of the TABLE (PUCK_XC / PUCK_R1B / PUCK_HB of the SW2 row:
    equator AC - PUCK_INSET since the 2026-10-09 puck fix) instead of nwo_model's puck at AC - the macro's puck, so the rebuild is the macro's"""
    legs = b['legs']; BR = b['BR']; c = b['cols']; S = None
    for i, lg in enumerate(legs):
        s = NM.revolve_leg_u(lg['V'], NM.U135) if (e45 and i == 1) else NM.revolve_leg(lg['V'], i); S = s if S is None else fuse(S, s)
    for i, lg in enumerate(legs):
        S = fuse(S, NM.hex_prism_u(NM.U135, 2 * BR, 0.0, lg['hexl']) if (e45 and i == 1) else hex_prism(i, 2 * BR, 0.0, lg['hexl']))
    h = c['PUCK_HB@PUCK']; r1 = c['PUCK_R1B@PUCK']; xc = c['PUCK_XC@PUCK']
    assert abs(c['PUCK_HT@PUCK'] - h) < 1e-12 and abs(c['PUCK_R1T@PUCK'] - r1) < 1e-12
    pk = BRepPrimAPI_MakeRevol(NM.face([(0, 0, -h), (r1, 0, -h), (xc, 0, 0), (r1, 0, h), (0, 0, h)]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 2 * math.pi).Shape()
    return fuse(S, pk)


def build(b, e45):
    """the macro's order: legs + hex arms + puck -> face-off cut + refill -> locknut cuts -> bores"""
    legs = b['legs']; c = b['cols']; U = axes(e45); info = {}
    S = body(b, e45)
    for i, lg in enumerate(legs, 1):
        fo = lg.get('faceoff')
        if not fo: continue
        u = U[i - 1]; sh = c[f'D1@HFPLN{i}']; dep = c[f'DEPTH@HOSEFACE{i}']; rin = c[f'HF{i}_DIN@HOSEFACE{i}_SK'] / 2; rS = c[f'SF{i}_DOUT@STUBFILL{i}_SK'] / 2
        if e45: tool = ring(u, sh, sh + dep, rin, c[f'HF{i}_DOUT@HOSEFACE{i}_SK'] / 2)
        else:
            assert u == (1.0, 0.0)
            zh = c[f'HF{i}_ZH@HOSEFACE{i}_SK']
            tool = cut(box(sh, -c[f'HF{i}_YLO@HOSEFACE{i}_SK'], -zh, sh + dep, c[f'HF{i}_YTOP@HOSEFACE{i}_SK'], zh), cyl(u, sh, sh + dep, rin))
        v0 = vol(S); S = cut(S, tool); v1 = vol(S); S = fuse(S, ring(u, sh, sh + dep, rin, rS)); v2 = vol(S)
        info[f'HOSEFACE{i}'] = dict(cut=v0 - v1, fill=v2 - v1, ring=math.pi * (rS ** 2 - rin ** 2) * dep, net=v2 - v0, past=fo['past'])
    for i, lg in enumerate(legs):
        if lg['kind'] != 'NWO': continue
        assert not (e45 and i == 1)
        n = lg['nut']; BIG = 20.0
        slab = box(-BIG, n['n0'], -BIG, BIG, n['w0'], BIG) if i == 1 else box(n['n0'], -BIG, -BIG, n['w0'], BIG, BIG)
        v0 = vol(S); S = cut(S, cut(slab, hex_prism(i, n['af'], n['n0'], n['w0']))); info[f'NUTCUT{i + 1}'] = dict(removed=v0 - vol(S), expect=NM_T.nwo_nut_removed(n))
    for i, lg in enumerate(legs):
        S = cut(S, cyl(U[i], 0.0, lg.get('Mtip', lg['V'][-1][0]), lg['bore'] / 2))
    return S, info


def residual(S, b, e45):
    """volume of the finished solid past each hose hex face, outside the stub, before the bead (must be 0)"""
    out = {}
    for i, lg in enumerate(b['legs'], 1):
        if lg['kind'] != 'HOSEB': continue
        u = axes(e45)[i - 1]; sh = lg['hexl']; b0 = lg['bead'][0]; rS = lg['rS']
        if e45: R = cut(cyl(u, sh + 1e-4, b0 - 1e-4, 10.0), cyl(u, sh, b0, rS + 1e-5))
        else: R = cut(box(sh + 1e-4, -10, -10, b0 - 1e-4, b['cols'][f'HF{i}_YTOP@HOSEFACE{i}_SK'] - 1e-4, 10), cyl(u, sh, b0, rS + 1e-5))
        out[f'leg{i}'] = vol(BRepAlgoAPI_Common(S, R).Shape())
    return out


def faces(p, u):
    """cylinders coaxial with the leg axis u (radius, axial span) and planes normal to it (position) of a STEP"""
    S = shape(p); e = TopExp_Explorer(S, TopAbs_FACE); cy, pl = set(), set()
    while e.More():
        f = TopoDS.Face(e.Current()) if hasattr(TopoDS, "Face") else TopoDS.Face_s(e.Current()); s = BRepAdaptor_Surface(f); e.Next()
        if s.GetType() == GeomAbs_Cylinder:
            c = s.Cylinder(); d = c.Axis().Direction(); L = c.Location()
            if abs(abs(d.X() * u[0] + d.Y() * u[1]) - 1) > 1e-6: continue
            lx, ly, lz = L.X() / MM, L.Y() / MM, L.Z() / MM; t = lx * u[0] + ly * u[1]
            if math.hypot(lx - t * u[0], ly - t * u[1], lz) > 1e-5: continue
            cy.add(round(c.Radius() / MM, 5))
        elif s.GetType() == GeomAbs_Plane:
            q = s.Plane(); d = q.Axis().Direction(); L = q.Location()
            if abs(abs(d.X() * u[0] + d.Y() * u[1]) - 1) > 1e-6: continue
            pl.add(round((L.X() * u[0] + L.Y() * u[1]) / MM, 5))
    return cy, pl


def measure_legs(p, legs):
    """nwo.measure_nwo on GIVEN legs [(axis, sign)] (its own legs_of() takes the two largest box extents - on a 45 deg hose elbow those can
    both belong to the angled hose leg); same section walk and parse"""
    res = []
    for axis, sign in legs:
        for pn in [k for k in (0, 1, 2) if k != axis]:
            S = [s for s in seg_list(leg_edges(p, axis, sign, pn, a0=0.05)) if min(s['r1'], s['r2']) > -1e-6]
            at = max(max(s['a1'], s['a2']) for s in S)
            face = [s for s in S if abs(s['a1'] - at) < 1e-3 and abs(s['a2'] - at) < 1e-3]
            if not face: continue
            rstart = max(max(s['r1'], s['r2']) for s in face)
            res.append(((axis, sign, pn), at, walk(S, nkey((at, rstart)), 0.06)))
    return res


def nwo_legs(p, legs=None):
    """the adjustable ORB legs of a STEP, per leg (axis, sign), with nwo.py's own pattern (the Brennan 6801 extractor)"""
    best = {}
    for leg, at, pts in (measure_legs(p, legs) if legs else measure_nwo(p)):
        M = parse(at, pts)
        if len(M) < 6: continue
        t, u_, w, n, k, b = M[:6]
        if not (u_[2] < t[2] and w[2] > u_[2] and n[2] < w[2] + 0.2 and k[2] < n[2] and b[2] > k[2] - 0.05): continue
        c = dict(tip=round(at, 4), TM=round(2 * t[2], 4), UR=round(u_[2], 4), THDL=round(at - u_[0], 4), WR=round(w[2], 4), WT=round(w[0] - w[1], 4),
                 NUTR=round(n[2], 4), NUTT=round(n[0] - n[1], 4), NECKR=round(k[2], 4), NECKL=round(k[0] - k[1], 4), I3=round(at - k[1], 4))
        key = leg[:2]
        if key not in best or c['NUTR'] < best[key]['NUTR']: best[key] = c
    return best


def run(T, root, pns=(), outd=None, verbose=True):
    """closed loop of every buildable configuration of a gen_tee root (or the listed ones); T = the imported gen_tee (SPEC may carry injected
    TEST roots). Returns (results, problems)."""
    global NM_T
    NM_T = T; e45 = bool(T.SPEC[root].get('e45')); outd = outd or os.environ.get('HB_OUT', OP.SCRATCH); os.makedirs(outd, exist_ok=True)
    built, _ = T.build_rows(root); res = {}; bad = []
    for b in built:
        if b['chk'] or (pns and b['pn'] not in pns): continue
        S, info = build(b, e45); path = os.path.join(outd, f'MODEL_{b["pn"]}.stp'); write(S, path)
        r = dict(volume=vol(S), solids=nsolids(S), info=info, residual=residual(S, b, e45)); errs = []
        if r['solids'] != 1: errs.append(f'{r["solids"]} solids')
        for k, v in info.items():
            if k.startswith('NUTCUT') and abs(v['removed'] - v['expect']) > 0.005 * v['expect']: errs.append(f'{k} removed {v["removed"]:.6f} vs {v["expect"]:.6f}')
            if k.startswith('HOSEFACE'):
                if v['cut'] < 0.98 * v['ring']: errs.append(f'{k} cut {v["cut"]:.6f} < ring')
                if abs(v['fill'] - v['ring']) > 1e-4 * v['ring']: errs.append(f'{k} refill {v["fill"]:.7f} vs ring {v["ring"]:.7f}')
                if (v['net'] < -1e-3 * v['ring']) != v['past']: errs.append(f'{k} net {v["net"]:.6f} vs past {v["past"]}')
        for k, v in r['residual'].items():
            if v > 1e-7: errs.append(f'{k}: {v:.7f} in^3 of the solid past the hose hex face outside the stub')
        # hose leg faces from the STEP
        for i, lg in enumerate(b['legs'], 1):
            if lg['kind'] != 'HOSEB': continue
            u = axes(e45)[i - 1]; cy, pl = faces(path, u); fo = lg['faceoff']; L_ = lg['V'][-1][0]; b0, b1 = lg['bead']
            want_c = {round(lg['rS'], 5), round(lg['rA'], 5), round(lg['bore'] / 2, 5)}; want_p = {round(x, 5) for x in (lg['hexl'], b0, b1, L_)}
            r[f'hose{i}'] = dict(cylinders=sorted(cy), planes=sorted(pl))
            if not want_c <= cy: errs.append(f'hose leg {i}: cylinders {sorted(cy)} miss {sorted(want_c - cy)}')
            if not want_p <= pl: errs.append(f'hose leg {i}: planes {sorted(pl)} miss {sorted(want_p - pl)}')
            if round(fo['rin'], 5) in cy: errs.append(f'hose leg {i}: a face-off cylinder (rin {fo["rin"]}) is left')
            if round(lg['hexl'] + fo['depth'], 5) in pl: errs.append(f'hose leg {i}: a face-off end plane ({lg["hexl"] + fo["depth"]:.4f}) is left')
        # adjustable ORB legs from the STEP (nwo.py extractor) vs the generator's leg values
        got = nwo_legs(path, [(0, 1)] + ([] if e45 else [(1, 1)])); r['nwo'] = {str(k): v for k, v in got.items()}
        for i, lg in enumerate(b['legs']):
            if lg['kind'] != 'NWO': continue
            key = (0, 1) if i == 0 else ((1, 1) if not e45 else None)
            m = got.get(key)
            want = dict(tip=lg['V'][-1][0], I3=lg['endlen'], THDL=round(lg['V'][-1][0] - lg['te'], 4), UR=lg['UR'], WR=lg['m']['WR'], WT=lg['m']['WT'],
                        NUTR=lg['nut']['af'] / 2, NUTT=lg['m']['NUTT'], NECKR=lg['m']['NECKR'], NECKL=lg['m']['NECKL'], TM=2 * lg['rM'])
            if not m: errs.append(f'leg {i + 1}: the nwo.py extractor found no adjustable ORB leg on {key}'); continue
            dif = {k: (m[k], round(v, 4)) for k, v in want.items() if abs(m[k] - v) > 0.0015}
            r[f'nwo_leg{i + 1}'] = dict(measured=m, want={k: round(v, 4) for k, v in want.items()}, diff=dif)
            if dif: errs.append(f'leg {i + 1} NWO measured != generator: {dif}')
        r['errors'] = errs; res[b['pn']] = r; bad += [f'{b["pn"]}: {x}' for x in errs]
        if verbose: print(b['pn'], 'volume %.5f in^3, %d solid(s)' % (r['volume'], r['solids']),
              {k: {kk: round(vv, 6) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in info.items()},
              'residual', {k: round(v, 8) for k, v in r['residual'].items()}, 'OK' if not errs else errs)
    json.dump(res, open(os.path.join(outd, f'results_{root}.json'), 'w'), indent=1, default=str)
    return res, bad


if __name__ == '__main__':
    import gen_tee
    root = sys.argv[1]
    res, bad = run(gen_tee, root, sys.argv[2:])
    print(root, 'closed loop', 'PASS' if not bad else f'FAIL ({len(bad)})')
