# 45 deg elbows with a helical thread / female port / swivel nut on the 135 deg leg (ANGLED, 2026-10-18: 1503 1504 5501 5503 5505 6902): OCP rebuild
# of every configuration from the generator's OWN data (gen_tee.build_rows), in the macro's feature order - LEG1 (+X) / LEG2 (135 deg) revolves,
# hex arms HEX1 / HEX2 (flats normal to Z), the 30deg double-cone corner PUCK about Z (equator PUCK_INSET inside the hex corners, as the macro),
# NECKTRIM / NECKFILL on a +X swivel that carries the turn, the swivel nut hex cuts (outside the nut hexagon over the nut hex length, on either
# leg), the adjustable-ORB locknut cut (+X), then each leg's pocket / connecting bore / bore from its face. Threads are not modelled (every THD_
# feature is suppressed in the saved masters), so the volumes are the ones sweep_configs reports on a saved master.
#
#   python tools/measure/angled_model.py --all <root>               -> every configuration: one solid?, volume (expected values for the dry run)
#   python tools/measure/angled_model.py --loop <root> [<pn> ...]   -> CLOSED LOOP: model STEP -> the validated extractors (forged.py for the pipe
#                                                                     legs, neck45.py for the swivel legs, forged.corner_arcs for the puck) ->
#                                                                     must give back the generator's own values (tips, hex faces, collar, drill,
#                                                                     bores, A/F, body face, neck, nut face, nothing outside the neck)
#   python tools/measure/angled_model.py --cmp <root> <pn>          -> vs the Brennan STEP of <pn> (placed like it): both readings + the
#                                                                     symmetric difference in connected pieces
# Output folder: $TEE_MODEL_OUT or tools/_out/scratch.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol
from nwo_model import face, vol, fuse, cut, write, MM
from tee_model import revolve_leg, hex_prism, cyl, nsolids, place, pieces

OUTD = os.environ.get('TEE_MODEL_OUT', OP.SCRATCH)
U135 = (math.cos(math.radians(135)), math.sin(math.radians(135)))
AXES = [(1.0, 0.0), U135]
THETA = [0.0, 135.0]
SIDE = [-1, 1]                          # LP half-plane of each model leg: away from the other leg (as tee_model MODEL_LEGS)
BRENNAN = {'5501-08-08-FG': (('mirror_x',), [('NPTFM', 180, -1), ('NPTFM', 45, 1)], [0, 1]),
           '5503-16-16-FG': (('rot_z', 45.0), [('NPTFM', 180, -1), ('NPTFF', 45, 1)], [1, 0])}


def ring(u, a0, a1, r0, r1):
    ux, uy = u; nx, ny = -uy, ux
    pts = [(a * ux + r * nx, a * uy + r * ny, 0) for a, r in ((a0, r0), (a1, r0), (a1, r1), (a0, r1))]
    return BRepPrimAPI_MakeRevol(face(pts), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(ux, uy, 0)), 2 * math.pi).Shape()


def outside_hex(u, af, a0, a1):
    """everything outside the hexagon (A/F af, flats normal to Z) between a0 and a1 along u: the 'outside' nut-hex cut"""
    return cut(hex_prism(u, 60.0, a0, a1), hex_prism(u, af, a0, a1))


def build(sp, b, turn=True):
    import gen_tee as T
    legs = b['legs']; BR = b['BR']; AC = b['AC']; AF = b['AF']
    S = fuse(revolve_leg(legs[0]['V'], AXES[0]), revolve_leg(legs[1]['V'], AXES[1]))
    for lg, u in zip(legs, AXES): S = fuse(S, hex_prism(u, AF, 0.0, lg['hexl']))
    h = BR; xc = AC - T.PUCK_INSET; r1 = xc - BR * math.tan(math.radians(30))
    S = fuse(S, BRepPrimAPI_MakeRevol(face([(0, 0, -h), (r1, 0, -h), (xc, 0, 0), (r1, 0, h), (0, 0, h)]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 2 * math.pi).Shape())
    for lg, u in zip(legs, AXES):
        t = lg.get('trim')
        if turn and t:
            assert u == AXES[0], 'neck turn on the +X leg only (as the macro)'
            S = cut(S, ring(u, t['a0'], t['a0'] + t['len'], t['rin'], t['rout']))
            S = fuse(S, ring(u, t['a0'], t['a0'] + t['len'], t['rin'], t['r']))
    for lg, u in zip(legs, AXES):
        if lg['kind'] in ('JICSW', 'NPSMSW'): S = cut(S, outside_hex(u, lg['nut_af'], lg['Mtip'] - lg['m']['HEXL'], lg['Mtip']))
    for lg, u in zip(legs, AXES):
        if lg['kind'] == 'NWO':
            assert u == AXES[0] and not lg.get('nwo_trim'), 'adjustable ORB leg on +X without ORBTRIM only'
            S = cut(S, outside_hex(u, lg['nut']['af'], lg['nut']['n0'], lg['nut']['w0']))
    for lg, u in zip(legs, AXES):
        M = lg.get('Mtip', lg['V'][-1][0])
        if lg['kind'] == 'NPTFF':
            S = cut(S, cyl(u, lg['td'] / 2, M - lg['pocket'], M))
            if not lg['to_centre']: S = cut(S, cyl(u, lg['conn'] / 2, 0.0, M))
        else:
            S = cut(S, cyl(u, lg['bore'] / 2, 0.0, M))
    return S


def expect(b, i, lg):
    """the generator's own values for leg i (what the extractor must give back)"""
    M = lg.get('Mtip', lg['V'][-1][0])
    if lg['kind'] == 'NPTFM':
        return dict(tip=M, hex_face=lg['hexl'], relief_dia=2 * lg['V'][3][1], bore_dia=lg['bore'], taper_len=lg['V'][4][0] and (M - lg['V'][4][0]))
    if lg['kind'] == 'NPTFF':
        return dict(face=M, collar_r=b['BR'], collar_len=lg['collar'], drill_dia=lg['td'],
                    drill_to_from_face=lg['pocket'] if lg['to_centre'] else lg['pocket'])
    return dict(nut_face=M, face=lg['hexl'], neckr=lg['m']['NECKR'], excess=0.0)


def read(p, i, lg):
    import forged as F, neck45 as N
    if lg['kind'] == 'NPTFM':
        r = F.nptfm(p, THETA[i], SIDE[i])
        return r, dict(tip=r['tip'], hex_face=r['hex_face'], relief_dia=r['relief_dia'], bore_dia=r['bore_dia'], taper_len=r['taper_len'])
    if lg['kind'] == 'NPTFF':
        r = F.nptff(p, THETA[i], SIDE[i])
        return r, dict(face=r['face'], collar_r=r['collar_r'], collar_len=r['collar_len'], drill_dia=(r['drill'] or {}).get('dia'),
                       drill_to_from_face=(r['drill'] or {}).get('to_from_face'))
    r = N.measure(p, THETA[i])
    return r, dict(nut_face=r['nut_face'], face=r['face'], neckr=r['neckr'], excess=r['excess'])


def loop(root, pns):
    import gen_tee as T, forged as F
    sp = T.SPEC[root]; built, _ = T.build_rows(root); out = []; bad = 0
    for b in built:
        if b['chk'] or (pns and b['pn'] not in pns): continue
        S = build(sp, b); p = os.path.join(OUTD, f'MODEL_{b["pn"]}.stp'); write(S, p)
        row = dict(pn=b['pn'], solids=nsolids(S), volume_in3=round(vol(S), 5), legs=[])
        for i, lg in enumerate(b['legs']):
            e = expect(b, i, lg)
            try: raw, g = read(p, i, lg)
            except Exception as ex: g = {k: f'ERROR {ex}' for k in e}
            d = {k: (round(e[k], 4), g.get(k), isinstance(g.get(k), (int, float)) and abs(g[k] - e[k]) < 6e-4) for k in e}
            row['legs'].append(dict(leg=i + 1, kind=lg['kind'], axis=('+X' if i == 0 else '135 deg'), values=d))
        arcs = F.corner_arcs(p); xc = round(b['AC'] - T.PUCK_INSET, 4)
        row['puck_arc'] = (xc, arcs, any(abs(a - xc) < 6e-4 for a in arcs))
        row['ok'] = row['solids'] == 1 and all(v[2] for L in row['legs'] for v in L['values'].values()) and row['puck_arc'][2]
        bad += not row['ok']; out.append(row); print(json.dumps(row))
    print(f'{root}: closed loop on {len(out)} configurations, problems {bad}')
    return out


if __name__ == '__main__':
    import gen_tee as T
    a = sys.argv[1:]
    os.makedirs(OUTD, exist_ok=True)
    if a[0] == '--all':
        root = a[1]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        for b in built:
            if b['chk']: continue
            S = build(sp, b)
            print(json.dumps(dict(pn=b['pn'], solids=nsolids(S), volume_in3=round(vol(S), 5))))
    elif a[0] == '--loop':
        loop(a[1], a[2:])
    elif a[0] == '--cmp':
        import forged as F
        root, pn = a[1], a[2]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        b = [x for x in built if x['pn'] == pn and not x['chk']][0]
        how, blegs, m2b = BRENNAN[pn]
        S = build(sp, b); pm = os.path.join(OUTD, f'MODEL_{pn}.stp'); write(S, pm)
        bp = os.path.join(os.environ.get('BRENNAN_STEP_DIR', OP.STEP_DIR), f'BRENNAN_{pn}.stp')
        B = F.shape(bp); Sb = place(S, how)
        res = dict(pn=pn, placed=how, model_volume=round(vol(S), 5), model_solids=nsolids(S),
                   model_legs=[read(pm, i, lg)[1] for i, lg in enumerate(b['legs'])],
                   brennan_legs=[F.KIND[k](bp, th, sd) for k, th, sd in (blegs[j] for j in m2b)], brennan_volume=round(vol(B), 5),
                   brennan_corner_arcs=F.corner_arcs(bp), model_corner_arcs=F.corner_arcs(pm))
        res['brennan_minus_model'] = round(vol(cut(B, Sb)), 5); res['model_minus_brennan'] = round(vol(cut(Sb, B)), 5)
        res['pieces_brennan_only'] = pieces(cut(B, Sb))[:12]; res['pieces_model_only'] = pieces(cut(Sb, B))[:12]
        json.dump(res, open(os.path.join(OUTD, f'cmp_{pn}.json'), 'w'), indent=1)
        print('written', os.path.join(OUTD, f'cmp_{pn}.json'))
