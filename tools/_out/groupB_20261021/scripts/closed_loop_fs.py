"""(copied to groupB_20261021/scripts 2026-10-21: tools = groupB tools_fs) closed_loop_fs.py (2026-10-20, ORFS staging): OCP closed loop of the FS straight roots of the staging generator
(tools/_out/orfs_gen_20261020/tools). Every configuration is rebuilt from the generator's OWN geometry - the DRIVE vertex chain
(checks/allcfg_check.straight_chain = what the macro draws) revolved about X, hex-cut (common with a hex prism of HEXB across flats, corners on
Y, as HEXCUT), the two bore cuts BORECUT_A / BORECUT_B (mode 'mid') - written as a STEP, read back and measured with the SAME extractors that
read the Brennan pilots (tools/_out/orfs_wp2_20261020/measure/fsmeasure.py). The readings must return the SW2 row: face-seal end (groove,
land, chamfer, thread, flank, relief, end length), ORB stud (thread, length, groove), overall length, bores. Threads are not modelled (the
saved masters keep THD_* suppressed). Also: the -08 rebuilds against the Brennan pilot volume (the pilot has the O-rings, hex chamfers and
tip chamfers the model leaves out).
  OMI_ROOT=<repo> OMI_REV_EXTRA=<stage_orfs/04_DESIGN_TABLES> python closed_loop_fs.py FS2403 FS6400 [--out DIR]"""
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
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
import fsmeasure as M
import prof
from section import load

TOL = 0.0015


def build(cols, EA, EB, L, hexb, rB):
    V = straight_chain(EA, EB, L, rB)
    S = revolve(V)
    S = BRepAlgoAPI_Common(S, hex_prism(hexb, -0.1, L + 0.1)).Shape()
    # group B 2026-10-21: a bore the row does not have (FS2408 plug: End B blind hole only) is skipped
    if cols.get('DA@BORE_A') is not None:
        ra, da = cols['DA@BORE_A'] / 2, cols['DEPTH@BORECUT_A']
        S = BRepAlgoAPI_Cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-0.01 * MM, 0, 0), gp_Dir(1, 0, 0)), ra * MM, (da + 0.01) * MM).Shape()).Shape()
    if cols.get('DB@BORE_B') is not None:
        rb, db = cols['DB@BORE_B'] / 2, cols['DEPTH@BORECUT_B']
        S = BRepAlgoAPI_Cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt((L + 0.01) * MM, 0, 0), gp_Dir(-1, 0, 0)), rb * MM, (db + 0.01) * MM).Shape()).Shape()
    return S


def expect_fsm(cols, sfx):
    g = lambda k: cols[f'FSM{sfx}_{k}@DRIVE']
    rM = cols[f'THDMAJR_{sfx}@DRIVE']; ch = rM - g('FACER')
    return dict(GI=g('GRVIR'), GO=g('GRVOR'), GD=g('GRVD'), FR=g('FACER'), CH=ch, CH_ANG=cols['FSMCHANG@DRIVE'], RMAJ=rM,
                THD_END=ch + g('THDL'), FLANK_ANG=cols['RELIEFANG@DRIVE'], RELR=g('RELR'), RELL=g('RELL'),
                ENDL=ch + g('THDL') + (rM - g('RELR')) / math.tan(math.radians(cols['RELIEFANG@DRIVE'])) + g('RELL'))


def cmp(exp, got, keys, tag):
    bad = []
    for k in keys:
        e_, g_ = exp[k], got.get(k)
        if g_ is None or abs(e_ - g_) > (0.15 if k.endswith('ANG') else TOL): bad.append(f'{tag} {k}: row {round(e_, 5)} / model {g_}')
    return bad


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
            for E, sfx, sign in ((EA, 'A', -1), (EB, 'B', 1)):
                # the part lies on x = 0 .. L: End A faces -X (leg sign -1, a measured from x = 0 outward = -x), End B faces +X
                if E['kind'] == 'FSM':
                    m = M.measure_fsm(f, 0, sign)
                    ex = expect_fsm(cols, sfx)
                    keys = ('GI', 'GO', 'GD', 'FR', 'CH', 'CH_ANG', 'RMAJ', 'THD_END', 'FLANK_ANG', 'RELR', 'RELL', 'ENDL'); n += len(keys)
                    bad += cmp(ex, m, keys, f'End {sfx} FSM')
                    face = m['face_a'] if sign > 0 else -m['face_a']
                    want = L if sign > 0 else 0.0; n += 1
                    if abs(face - want) > TOL: bad.append(f'End {sfx} face at x {face} (row {want})')
                    bo = cols['DA@BORE_A' if sfx == 'A' else 'DB@BORE_B'] / 2; n += 1
                    if abs(m['BORER'] - bo) > TOL: bad.append(f'End {sfx} bore r {m["BORER"]} (row {bo})')
                    if m['RINGS']: bad.append(f'End {sfx}: an O-ring arc in the model ({m["RINGS"]})')
                elif E['kind'] == 'ORBM':
                    m = M.measure_stud(f, 0, sign, model=True)
                    o = E['o']
                    ex = dict(RMAJ=o['TM'] / 2, THD_END=o['THDL'], UCR=o['GD'] / 2, UCL=o['GW'], SHOULDER=o['THDL'] + o['GW'])
                    keys = tuple(ex); n += len(keys)
                    bad += cmp(ex, m, keys, f'End {sfx} ORB stud')
                    tip = m['tip_a'] if sign > 0 else -m['tip_a']; want = L if sign > 0 else 0.0; n += 1
                    if abs(tip - want) > TOL: bad.append(f'End {sfx} tip at x {tip} (row {want})')
                    bo = cols['DA@BORE_A' if sfx == 'A' else 'DB@BORE_B'] / 2; n += 1
                    if abs(m['BORER'] - bo) > TOL: bad.append(f'End {sfx} bore r {m["BORER"]} (row {bo})')
                elif E['kind'] == 'PLAIN':
                    pass       # group B: the plug's plain back face (overall length checked below)
                elif E['kind'] in ('JICM', 'NPTFM'):
                    pass       # 2026-10-20: the accepted library ends (MS33656J / ASME B1.20.3), closed-looped with their own masters - not read here
                else:
                    bad.append(f'End {sfx}: kind {E["kind"]} has no closed-loop reader here')
            # hex across flats (thin probe: section normal to X at the hex mid-plane, plane through the flats = Z extent)
            bb = prof.bbox(f); n += 2
            if abs((bb[5] - bb[2]) - hexb) > TOL: bad.append(f'hex A/F (z extent) {round(bb[5] - bb[2], 4)} (row {hexb})')
            if abs((bb[3] - bb[0]) - L) > TOL: bad.append(f'overall {round(bb[3] - bb[0], 4)} (row {L})')
            r = dict(pn=pn, checks=n, off=len(bad), solids=nsolids(S), volume=round(vol(S), 5), bad=bad)
            if nsolids(S) != 1: bad.append(f'{nsolids(S)} solids')
            pil = G.P.step(pn)
            if os.path.exists(pil):
                vb = vol(load(pil)); r['brennan_volume'] = round(vb, 5); r['diff_pct'] = round(100 * (r['volume'] - vb) / vb, 2)
            res.append(r); nbad += len(bad); nchk += n
            lines.append(f"{pn}: {n} checks, {len(bad)} off; solids {r['solids']}, volume {r['volume']} in^3"
                         + (f"; Brennan pilot {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '') + ''.join('\n   OFF ' + b for b in bad))
    lines.append(f'\nFS closed loop {"PASS" if nbad == 0 else "FAIL"}: {len(res)} configurations, {nchk} checks, {nbad} off (tolerance {TOL})')
    json.dump(res, open(os.path.join(out, 'closed_loop.json'), 'w'), indent=1)
    open(os.path.join(out, 'closed_loop.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]; out = os.path.join(HERE, 'ocp')
    if '--out' in a: k = a.index('--out'); out = a[k + 1]; del a[k:k + 2]
    main(a, out)
