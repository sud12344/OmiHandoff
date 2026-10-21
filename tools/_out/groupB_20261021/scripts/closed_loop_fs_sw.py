"""(copied to groupB_20261021/scripts 2026-10-21: tools = groupB tools_fs) closed_loop_fs_sw.py (2026-10-20, ORFS staging): OCP closed loop of the straight face-seal SWIVELS of the staging generator (FS6565 / FS6540 /
FS6504 / FS6505 and their counterbored-mouth masters ...C). Every configuration is rebuilt from the generator's OWN geometry as the macro builds it:
the DRIVE chain (checks/allcfg_check.straight_chain) revolved about X, the body hex cut only over its zone (End A end .. the swivel body face,
ZoneHexCut), each swivel nut hex cut over its own zone from the nut face (NUTCUT / NUTCUTA), the stepped bores BORE_A / BORE_B (mode sw2). The STEP
is read back with the extractor that read the Brennan pilots (tools/_out/orfs_wp2_20261020/measure/fsmeasure.measure_fssw, model=True; an End A
swivel on a copy turned 180deg about Y) and must return the row: seal face, nut face, stem head, cavity (mouth, minor, relief), nut hex, skirt,
nut rear face, neck, body face, bore. Also: the overall length and hex extents, the ORB stud of FS6540 (measure_stud), and against
BRENNAN_FS6565-08-08 the seal face -> seal face distance and the volume. The male JIC (FS6504) and pipe (FS6505) ends are the accepted library ends
(MS33656J / ASME B1.20.3, closed-looped with their own masters) - not read here.
  OMI_ROOT=<repo> OMI_REV_EXTRA=<stage_orfs/04_DESIGN_TABLES> python closed_loop_fs_sw.py FS6565 FS6565C ... [--out DIR]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
T = os.path.join(HERE, 'tools_fs')
for p_ in (os.path.join(T, 'generators'), os.path.join(T, 'checks'), os.path.join(T, 'measure'), T,
           os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure')):
    sys.path.insert(0, p_)
os.environ.setdefault('GS_OUT', os.path.join(HERE, 'scratch'))
import gen_straight2 as G
from allcfg_check import straight_chain
from model_nutcap import revolve, hex_prism, vol, nsolids, write, MM
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Trsf, gp_Vec
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
import fsmeasure as M
import prof
from section import load

TOL = 0.0015


def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()


def zone_hex(S, af, x0, x1):
    """remove everything outside the hexagon af (corners on Y, flats normal to Z) over x0 .. x1 - as ZoneHexCut"""
    B = 20.0
    box = BRepPrimAPI_MakeBox(gp_Pnt(x0 * MM, -B * MM, -B * MM), gp_Pnt(x1 * MM, B * MM, B * MM)).Shape()
    return cut(S, cut(box, hex_prism(af, x0, x1)))


def bore(S, d, x0, x1):
    return cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0 * MM, 0, 0), gp_Dir(1, 0, 0)), d / 2 * MM, (x1 - x0) * MM).Shape())


def build(cols, EA, EB, L, hexb, rB):
    S = revolve(straight_chain(EA, EB, L, rB))
    swA = EA['kind'] == 'FSSW'
    xs0 = EA['endlen'] if swA else 0.0; xbody = L - EB['endlen']
    S = zone_hex(S, hexb, xs0 - (0 if swA else 0.1), xbody)
    S = zone_hex(S, EB['nut_af'], L - EB['m']['HEXL'], L + 0.1)
    if swA: S = zone_hex(S, EA['nut_af'], -0.1, EA['m']['HEXL'])
    S = bore(S, cols['DA@BORE_A'], -0.01, cols['DEPTH@BORECUT_A'] + 1e-4)
    S = bore(S, cols['DB@BORE_B'], cols['START@BORECUT_B'] - 1e-4, cols['START@BORECUT_B'] + cols['DEPTH@BORECUT_B'])
    return S


def turn(S, L):
    """the part turned 180deg about Y and moved back onto x = 0 .. L (End A becomes the +X end)"""
    t = gp_Trsf(); t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)), math.pi)
    t2 = gp_Trsf(); t2.SetTranslation(gp_Vec(L * MM, 0, 0))
    S = BRepBuilderAPI_Transform(S, t, True).Shape()
    return BRepBuilderAPI_Transform(S, t2, True).Shape()


def cmp(exp, got, tag, bad):
    n = 0
    for k, e_ in exp.items():
        g_ = got.get(k); n += 1
        if g_ is None or abs(e_ - g_) > (0.15 if k.endswith('ANG') else TOL): bad.append(f'{tag} {k}: row {round(e_, 5)} / model {g_}')
    return n


def sw_expect(E, cols, sfx, L, bore_d):
    m = E['m']; g = lambda k: cols[f'FSW{sfx}_{k}@DRIVE']
    exp = dict(SEAL_a=L - g('SEAL'), NUTFACE_a=L, SEAL_TO_NUTFACE=g('SEAL'), STEMR=g('STEMR'), HEAD_REAR_a=L - g('SEAL') - g('HEADL'), MINR=g('MINR'),
               TE=E['cs'] + g('THDL'), NUTL=g('NUTL'), NECKR=g('NECKR'), BODYFACE_a=L - g('BODYS'), BORER=bore_d / 2, NUT_CORNER_R=round(E['nut_af'] / math.sqrt(3), 5))
    if E['cb']: exp.update(CBR=g('CBR'), CBD=g('CBD'), CB_ANG=g('CSANG'), CB_CS_DEPTH=E['cs'] - g('CBD'))
    else: exp.update(MOUTH_R=g('CSR'), MOUTH_DEPTH=E['cs'])
    return exp


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
            bad, n = [], 0
            # End B swivel (+X)
            m = M.measure_fssw(f, 0, 1, model=True)
            n += cmp(sw_expect(EB, cols, 'B', L, cols['DB@BORE_B']), m, 'End B FSSW', bad)
            n += 1
            if m.get('MOUTH') != ('cb' if EB['cb'] else 'cs'): bad.append(f'End B mouth {m.get("MOUTH")}')
            hx = m['NUT_HEX_s']; n += 1
            if not hx or abs(hx[1] - cols['FSWB_NUTHEXL@DRIVE']) > TOL: bad.append(f'End B nut hex ends at {hx} (row {cols["FSWB_NUTHEXL@DRIVE"]})')
            # End A
            if EA['kind'] == 'FSSW':
                fT = os.path.join(out, f'MODEL_{pn}_turned.stp'); write(turn(S, L), fT); prof._cache.clear()
                mA = M.measure_fssw(fT, 0, 1, model=True)
                n += cmp(sw_expect(EA, cols, 'A', L, cols['DA@BORE_A']), mA, 'End A FSSW', bad)
                n += 1
                if mA.get('MOUTH') != ('cb' if EA['cb'] else 'cs'): bad.append(f'End A mouth {mA.get("MOUTH")}')
            elif EA['kind'] == 'ORBM':
                ms = M.measure_stud(f, 0, -1, model=True); o = EA['o']
                ex = dict(RMAJ=o['TM'] / 2, THD_END=o['THDL'], UCR=o['GD'] / 2, UCL=o['GW'], SHOULDER=o['THDL'] + o['GW'], BORER=cols['DA@BORE_A'] / 2)
                n += cmp(ex, ms, 'End A ORB stud', bad)
                tip = -ms['tip_a']; n += 1
                if abs(tip) > TOL: bad.append(f'End A tip at x {tip}')
            # the body hex A/F (flats normal to Z), the largest nut, the overall length
            bb = prof.bbox(f); big = max(hexb, EB['nut_af'], EA.get('nut_af', 0)); n += 2
            if abs((bb[5] - bb[2]) - big) > TOL: bad.append(f'z extent {round(bb[5] - bb[2], 4)} (largest hex A/F {big})')
            if abs((bb[3] - bb[0]) - L) > TOL: bad.append(f'overall {round(bb[3] - bb[0], 4)} (row {L})')
            r = dict(pn=pn, checks=n, solids=nsolids(S), volume=round(vol(S), 5))
            if r['solids'] != 1: bad.append(f'{r["solids"]} solids')
            pil = G.P.step(pn)
            if os.path.exists(pil):
                vb = vol(load(pil)); r['brennan_volume'] = round(vb, 5); r['diff_pct'] = round(100 * (r['volume'] - vb) / vb, 2)
                if EA['kind'] == 'FSSW':
                    prof._cache.clear()
                    pB = M.measure_fssw(pil, 0, 1)
                    # the pilot's two seal faces: the radial faces at the bore radius (its -X swivel does not read in measure_fssw, ends_survey)
                    S_ = M.half(pil, 0, 1, 2, ())
                    vs = [s for s in S_ if s['k'] == 'L' and abs(s['a1'] - s['a2']) < 1e-4 and abs(min(s['r1'], s['r2']) - pB['BORER']) < 1e-3]
                    seals = sorted(s['a1'] for s in vs)
                    r['pilot_seal_to_seal'] = round(seals[-1] - seals[0], 4); r['model_seal_to_seal'] = round(L - cols['FSWA_SEAL@DRIVE'] - cols['FSWB_SEAL@DRIVE'], 4)
                    n += 1
                    if abs(r['pilot_seal_to_seal'] - r['model_seal_to_seal']) > 0.006: bad.append(f'seal face -> seal face: pilot {r["pilot_seal_to_seal"]} / model {r["model_seal_to_seal"]}')
                    for k in ('SEAL_TO_NUTFACE', 'STEMR', 'MINR', 'NUTL', 'NECKR', 'TE'):
                        n += 1
                        if abs(pB[k] - m[k]) > TOL: bad.append(f'pilot End B {k}: {pB[k]} / model {m[k]}')
            r.update(checks=n, off=len(bad), bad=bad); res.append(r); nbad += len(bad); nchk += n
            lines.append(f"{pn}: {n} checks, {len(bad)} off; solids {r['solids']}, volume {r['volume']} in^3"
                         + (f"; Brennan pilot {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '')
                         + (f"; seal -> seal pilot {r['pilot_seal_to_seal']} / model {r['model_seal_to_seal']}" if 'pilot_seal_to_seal' in r else '')
                         + ''.join('\n   OFF ' + b for b in bad))
    lines.append(f'\nFS straight swivel closed loop {"PASS" if nbad == 0 else "FAIL"}: {len(res)} configurations, {nchk} checks, {nbad} off (tolerance {TOL})')
    json.dump(res, open(os.path.join(out, 'closed_loop_sw.json'), 'w'), indent=1)
    open(os.path.join(out, 'closed_loop_sw.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]; out = os.path.join(HERE, 'ocp')
    if '--out' in a: k = a.index('--out'); out = a[k + 1]; del a[k:k + 2]
    main(a, out)
