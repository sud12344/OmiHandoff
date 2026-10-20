"""closed_loop_fs_loose.py (2026-10-20, ORFS staging): OCP closed loop of the loose face-seal parts of the staging generator: the nuts FS0306
(bulkhead locknut) and FS0318 (tube nut), and the braze sleeve FS0319 (round, measure_sleeve). Each configuration is rebuilt from the generator's OWN geometry (the DRIVE chain of
checks/allcfg_check.straight_chain revolved about X, common with the HEXB hex prism, then the BORE_A / BORE_B / POCKET_A cuts the macro makes),
written as a STEP and read back with fsmeasure.measure_nut / measure_sleeve - the extractors that read the Brennan pilots. Its readings must return (1) the SW2
row and (2) the Brennan pilot's readings for everything the model carries (hex, length, thread minor, countersinks, lip face, lip bore).
Not modelled, so not compared: threads (THD_* suppressed), hex end chamfers, the FS0318 0.0046 thread relief and mouth countersink, the
FS0319 inner 45deg chamfers and the spigot fillet.
  OMI_ROOT=<repo> OMI_REV_EXTRA=<stage_orfs/04_DESIGN_TABLES> python closed_loop_fs_loose.py FS0306 FS0318 FS0319 FS0319C [--out DIR]"""
import os, sys, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
T = os.path.join(HERE, 'tools')
for p_ in (os.path.join(T, 'generators'), os.path.join(T, 'checks'), os.path.join(T, 'measure'), T,
           os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure')):
    sys.path.insert(0, p_)
os.environ.setdefault('GS_OUT', os.path.join(HERE, 'scratch'))
import gen_straight2 as G
from allcfg_check import straight_chain
from model_nutcap import revolve, hex_prism, vol, nsolids, write, MM
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
import fsmeasure as M
import prof
from section import load

TOL = 0.0015


def cyl_cut(S, r, x0, d, fwd):
    ax = gp_Ax2(gp_Pnt((x0 - 0.01 if fwd else x0 + 0.01) * MM, 0, 0), gp_Dir(1 if fwd else -1, 0, 0))
    return BRepAlgoAPI_Cut(S, BRepPrimAPI_MakeCylinder(ax, r * MM, (d + 0.01) * MM).Shape()).Shape()


def build(cols, EA, EB, L, hexb, rB):
    S = revolve(straight_chain(EA, EB, L, rB))
    if 'BODYR@DRIVE' in cols and abs(cols['BODYR@DRIVE'] - hexb / 2) > 1e-6:      # hex part (a round part's body radius is hexb / 2: no hex cut)
        S = BRepAlgoAPI_Common(S, hex_prism(hexb, -0.1, L + 0.1)).Shape()
    if 'DA@BORE_A' in cols: S = cyl_cut(S, cols['DA@BORE_A'] / 2, 0.0, cols['DEPTH@BORECUT_A'], True)
    if 'DB@BORE_B' in cols: S = cyl_cut(S, cols['DB@BORE_B'] / 2, L, cols['DEPTH@BORECUT_B'], False)
    if 'TAPDRILLA@POCKET_A' in cols: S = cyl_cut(S, cols['TAPDRILLA@POCKET_A'] / 2, 0.0, cols['DEPTH@POCKETCUT_A'], True)
    if 'SOCKDIA@POCKET_A' in cols: S = cyl_cut(S, cols['SOCKDIA@POCKET_A'] / 2, 0.0, cols['DEPTH@POCKETCUT_A'], True)
    return S


def norm(m, L, flip):
    """axial readings measured from the End A face (flip: the pilot's End A lies at +X)"""
    f = (lambda a: round(L - a, 4)) if flip else (lambda a: a)
    mouth = sorted(tuple(sorted(((f(a1), r1), (f(a2), r2)))) for a1, r1, a2, r2 in m['MOUTH'])
    bores = sorted((r, *sorted((f(a1), f(a2)))) for r, a1, a2 in m['BORES'])
    return dict(AF=m['AF'], L=m['L'], MINR=m['MINR'], MOUTH=mouth, BORES=bores)


def num_cmp(a, b, tag, bad):
    if isinstance(a, (list, tuple)):
        if len(a) != len(b): bad.append(f'{tag}: {a} / {b}'); return 1
        return sum(num_cmp(x, y, f'{tag}[{i}]', bad) for i, (x, y) in enumerate(zip(a, b)))
    if abs(a - b) > TOL: bad.append(f'{tag}: {a} / {b}')
    return 1


def sleeve_read(p):
    """measure_sleeve plus the taper (the 15deg edge from the tube-side face) and the tube-stop face (the vertical inner edge between the stop
    bore and the braze bore), axial positions from the tube-side face (x min)"""
    o = M.measure_sleeve(p, 0); x0 = prof.bbox(p)[0]
    E = [(k, a_, round(a1 - x0, 4), r1, round(a2 - x0, 4), r2) for k, a_, a1, r1, a2, r2 in o['EDGES']]
    tp = [e for e in E if e[0] == 'L' and e[1] is not None and 10 < e[1] < 20]
    st = [e for e in E if e[0] == 'L' and e[1] == 90.0 and o['STOP_R'] - 1e-4 <= min(e[3], e[5]) and max(e[3], e[5]) <= o['BORE_R'] + 1e-4 and e[2] > 0.05]
    sf = [max(e[3], e[5]) for e in E if e[0] == 'L' and e[1] == 90.0 and abs(e[2] - o['L']) < 1e-3 and abs(e[4] - o['L']) < 1e-3]
    return dict(L=o['L'], OD_R=o['OD_R'], COLLARL=o['COLLARL'], BORE_R=o['BORE_R'], STOP_R=o['STOP_R'], SEALR=max(sf) if sf else None,
                SPIGOT_R=o['SPIGOT'][0][0] if o['SPIGOT'] else None,
                TAPER=(tp[0][1], min(tp[0][3], tp[0][5]), max(tp[0][3], tp[0][5])) if tp else None,
                LIPL=round(o['L'] - st[0][2], 4) if st else None)


def sleeve(f, cols, EA, L, hexb, pn):
    m = EA['m']; bad = []; n = 0
    mm = sleeve_read(f)
    coned = 'FSSEALB_CONEL@DRIVE' in cols     # FS0319C: the collar cylinder ends where the seal cone starts
    row = dict(L=L, OD_R=hexb / 2, COLLARL=round(L - cols['FSSLVA_SPIGOTL@DRIVE'] - (cols['FSSEALB_CONEL@DRIVE'] if coned else 0.0), 5),
               SEALR=cols['FSSEALB_SEALR@DRIVE'] if coned else hexb / 2, BORE_R=cols['SOCKDIA@POCKET_A'] / 2, STOP_R=cols['DB@BORE_B'] / 2,
               SPIGOT_R=cols['FSSLVA_SPIGOTR@DRIVE'], TAPER=(cols['FSSLVA_TAPANG@DRIVE'], cols['FSSLVA_FACER@DRIVE'], cols['FSSLVA_SPIGOTR@DRIVE']),
               LIPL=round(L - cols['DEPTH@POCKETCUT_A'], 5))
    for k in row:
        if mm[k] is None: bad.append(f'row {k}: no reading'); n += 1; continue
        if k == 'TAPER':
            n += 3
            if abs(mm[k][0] - row[k][0]) > 0.15: bad.append(f'row taper angle {row[k][0]} / model {mm[k][0]}')
            n -= 1; n += num_cmp(list(row[k][1:]), list(mm[k][1:]), 'row taper radii', bad)
        else: n += num_cmp(row[k], mm[k], f'row {k}', bad)
    r = dict(pn=pn, model=mm, row=row)
    pil = G.P.step(pn)
    if os.path.exists(pil):
        pp = sleeve_read(pil); r['pilot'] = pp
        for k in ('L', 'OD_R'):           # Air-Way row inputs: rounding allowance 0.01 (radius 0.005)
            n += 1
            if abs(pp[k] - mm[k]) > (0.01 if k == 'L' else 0.005): bad.append(f'pilot {k}: {pp[k]} / model {mm[k]}')
        for k in ('COLLARL', 'BORE_R', 'STOP_R', 'SPIGOT_R', 'LIPL') + (('SEALR',) if coned else ()):
            n += num_cmp(pp[k], mm[k], f'pilot {k}', bad)
        n += 1
        if abs(pp['TAPER'][0] - mm['TAPER'][0]) > 0.15: bad.append(f'pilot taper angle {pp["TAPER"][0]} / model {mm["TAPER"][0]}')
        n += num_cmp(list(pp['TAPER'][1:]), list(mm['TAPER'][1:]), 'pilot taper radii', bad)
        r['brennan_volume'] = round(vol(load(pil)), 5)
    r.update(checks=n, bad=bad)
    return r


def main(roots, out):
    os.makedirs(out, exist_ok=True)
    res, lines, nbad, nchk = [], [], 0, 0
    for root in roots:
        built, skipped = G.build_rows(root)
        for cols, EA, EB, L, hexb, rB, body, chk in built:
            pn = cols['$PRP@PartNo']
            if chk: lines.append(f'{pn}: generator-blocked {chk}'); continue
            S = build(cols, EA, EB, L, hexb, rB)
            f = os.path.join(out, f'MODEL_{pn}.stp'); write(S, f); prof._cache.clear()
            if EA.get('fsslv'):
                r = sleeve(f, cols, EA, L, hexb, pn); r.update(solids=nsolids(S), volume=round(vol(S), 5))
                if nsolids(S) != 1: r['bad'].append(f'{nsolids(S)} solids')
                if 'brennan_volume' in r: r['diff_pct'] = round(100 * (r['volume'] - r['brennan_volume']) / r['brennan_volume'], 2)
                r['off'] = len(r['bad']); res.append(r); nbad += len(r['bad']); nchk += r['checks']
                lines.append(f"{pn}: {r['checks']} checks, {r['off']} off; solids {r['solids']}, volume {r['volume']} in^3"
                             + (f"; Brennan pilot {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '')
                             + f"\n   model {r['model']}" + (f"\n   pilot {r['pilot']}" if 'pilot' in r else '') + ''.join('\n   OFF ' + b for b in r['bad']))
                continue
            mm = norm(M.measure_nut(f, 0), L, False)
            bad, n = [], 0
            # (1) against the row
            if EA['kind'] == 'NUTCSA':
                rmin, rcs, cs = EA['rmin'], EA['rcs'], EA['cs']
                row = dict(AF=hexb, L=L, MINR=rmin, MOUTH=[((0.0, rcs), (cs, rmin)), ((round(L - cs, 4), rmin), (L, rcs))], BORES=[(rmin, cs, round(L - cs, 4))])
            else:
                td, lip = cols['TAPDRILLA@POCKET_A'] / 2, cols['DEPTH@POCKETCUT_A']
                row = dict(AF=hexb, L=L, MINR=td, MOUTH=[], BORES=sorted([(cols['DB@BORE_B'] / 2, lip, L), (td, 0.0, lip)]))
            for k in row: n += num_cmp(row[k], mm[k], f'row {k}', bad)
            # (2) against the Brennan pilot (shape readings; hex and length are Air-Way row inputs, compared with the rounding allowance 0.01)
            pil = G.P.step(pn); r = dict(pn=pn, model=mm, row=row)
            if os.path.exists(pil):
                b_ = prof.bbox(pil); Lp = b_[3] - b_[0]
                mp = M.measure_nut(pil, 0)
                # both -08 pilots lie with End A (the open thread face) at their x min: axial readings re-based on it
                pp = norm(mp, round(b_[3], 4), False)
                pp = dict(pp, BORES=[(r_, round(a1 - b_[0], 4), round(a2 - b_[0], 4)) for r_, a1, a2 in pp['BORES']],
                          MOUTH=[tuple((round(a - b_[0], 4), rr) for a, rr in q) for q in pp['MOUTH']])
                r['pilot'] = pp
                for k in ('AF', 'L'):
                    n += 1
                    if abs(pp[k] - mm[k]) > 0.01: bad.append(f'pilot {k}: {pp[k]} / model {mm[k]}')
                known = EA.get('fsnote')      # Brennan's thread bore differs from the basic minor the model uses (noted in the row's $COMMENT)
                if known: r['expected_difference'] = f"thread bore r: Brennan {pp['MINR']} / model {mm['MINR']} (basic minor; {known.split(' - ')[0]})"
                else: n += num_cmp(pp['MINR'], mm['MINR'], 'pilot MINR', bad)
                if EA['kind'] == 'NUTCSA' and known:
                    # countersink outer radius only (its depth follows from the minor)
                    n += num_cmp([max(q[0][1], q[1][1]) for q in pp['MOUTH']], [max(q[0][1], q[1][1]) for q in mm['MOUTH']], 'pilot countersink outer radius', bad)
                elif EA['kind'] == 'NUTCSA':
                    # countersinks: radial extent and depth on both faces
                    dep = lambda q: round(abs(q[1][0] - q[0][0]), 4); rad = lambda q: (min(q[0][1], q[1][1]), max(q[0][1], q[1][1]))
                    n += num_cmp([dep(q) for q in pp['MOUTH']], [dep(q) for q in mm['MOUTH']], 'pilot countersink depth', bad)
                    n += num_cmp([rad(q) for q in pp['MOUTH']], [rad(q) for q in mm['MOUTH']], 'pilot countersink radii', bad)
                else:
                    # lip bore radius + lip face distance from the open (threaded) face; the pilot's relief / mouth readings are not modelled
                    lipP = [b for b in pp['BORES'] if abs(b[0] - cols['DB@BORE_B'] / 2) < 0.002]
                    lipM = [b for b in mm['BORES'] if abs(b[0] - cols['DB@BORE_B'] / 2) < 0.002]
                    n += 1
                    if not lipP or not lipM: bad.append(f'lip bore missing: pilot {lipP} / model {lipM}')
                    else:
                        oP = (lipP[0][1] if lipP[0][1] > 0.01 else round(Lp - lipP[0][2], 4)); oM = lipM[0][1]
                        n += num_cmp([lipP[0][0], oP], [lipM[0][0], oM], 'pilot lip (r, face from the open end)', bad)
                vb = vol(load(pil)); r['brennan_volume'] = round(vb, 5)
            r.update(checks=n, off=len(bad), solids=nsolids(S), volume=round(vol(S), 5), bad=bad)
            if nsolids(S) != 1: bad.append(f'{nsolids(S)} solids')
            if 'brennan_volume' in r: r['diff_pct'] = round(100 * (r['volume'] - r['brennan_volume']) / r['brennan_volume'], 2)
            res.append(r); nbad += len(bad); nchk += n
            lines.append(f"{pn}: {n} checks, {len(bad)} off; solids {r['solids']}, volume {r['volume']} in^3"
                         + (f"; Brennan pilot {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '')
                         + f"\n   model {mm}" + (f"\n   pilot {r['pilot']}" if 'pilot' in r else '')
                         + (f"\n   EXPECTED {r['expected_difference']}" if 'expected_difference' in r else '') + ''.join('\n   OFF ' + b for b in bad))
    lines.append(f'\nFS loose-part closed loop {"PASS" if nbad == 0 else "FAIL"}: {len(res)} configurations, {nchk} checks, {nbad} off (tolerance {TOL})')
    json.dump(res, open(os.path.join(out, 'closed_loop_loose.json'), 'w'), indent=1)
    open(os.path.join(out, 'closed_loop_loose.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]; out = os.path.join(HERE, 'ocp')
    if '--out' in a: k = a.index('--out'); out = a[k + 1]; del a[k:k + 2]
    main(a, out)
