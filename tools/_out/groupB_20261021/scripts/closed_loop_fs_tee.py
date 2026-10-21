"""(copied to groupB_20261021/scripts 2026-10-21: tools = groupB tools_fs) closed_loop_fs_tee.py (2026-10-20, ORFS staging): OCP closed loop of the forged FS roots of the staging gen_tee
(tools/_out/orfs_gen_20261020/tools). Every configuration is rebuilt from the generator's own leg profiles and SW2 values in the macro's
feature order: elbows (90 / 45 deg) with measure/nwo_model.build (LEGi revolves, one hex arm per leg, the 30deg corner puck - without the
0.0005 PUCK_INSET, irrelevant to the leg ends -, the adjustable-ORB lock-nut hex cut, bores); tees with the RUN bar + HEX3 arm of
measure/pipetee_model + the same lock-nut cut for an adjustable leg + bores. Written as a STEP, read back and measured with the extractors that
read the Brennan pilots (tools/_out/orfs_wp2_20261020/measure/fsmeasure.py), leg by leg, in the section plane through the hex FLATS (the
plane through the corners shows the hex arm corners, not the forged step). A 45 deg leg is measured on a copy of the model turned -135 deg
about Z (fsmeasure cannot section an angled leg). The readings must return the SW2 row. Threads are not modelled.
  OMI_ROOT=<repo> OMI_REV_EXTRA=<stage_orfs/04_DESIGN_TABLES> python closed_loop_fs_tee.py FS2500 FS2701 ... [--out DIR]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
T_ = os.path.join(HERE, 'tools_fs')
for p_ in (os.path.join(T_, 'generators'), os.path.join(T_, 'measure'), T_, os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure')):
    sys.path.insert(0, p_)
os.environ.setdefault('GT_OUT', os.path.join(HERE, 'scratch'))
import gen_tee as T
import nwo_model as NM
import pipetee_model as PT
from OCP.gp import gp_Pnt, gp_Ax1, gp_Dir, gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
import fsmeasure as M
import prof

TOL = 0.0015
MM = 25.4


def nut_cut(S, ax, sg, af, n0, w0):
    """lock-nut hex cut of an adjustable leg on signed axis (ax, sg) of a TEE: slab n0..w0 along the leg minus the nut hexagon"""
    BIG = 20.0; lo = [-BIG * MM] * 3; hi = [BIG * MM] * 3
    x0, x1 = sorted((sg * n0, sg * w0)); lo[ax] = x0 * MM; hi[ax] = x1 * MM
    return PT.cut(S, PT.cut(BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape(), PT.hex_prism(ax, af, x0, x1)))


def build_tee(b):
    c = b['cols']; legs = b['legs']; S = None
    for i, lg in enumerate(legs, 1):
        ax, sg = PT.PLACE[i]; s = PT.revolve_leg(lg['V'], ax, sg); S = s if S is None else PT.fuse(S, s)
    S = PT.fuse(S, PT.hex_prism(0, c['HEXAF@RUN'], -c['HEXL2@RUN_BODY'], c['HEXL1@RUN_BODY']))
    S = PT.fuse(S, PT.hex_prism(1, c['HEXAF@HEX3'], 0.0, c['HEXL@HEX3_BODY']))
    for i, lg in enumerate(legs, 1):
        if lg['kind'] == 'NWO':
            ax, sg = PT.PLACE[i]; n = lg['nut']; S = nut_cut(S, ax, sg, n['af'], n['n0'], n['w0'])
    for i, lg in enumerate(legs, 1):
        ax, sg = PT.PLACE[i]; Mt = lg.get('Mtip', lg['V'][-1][0])
        S = PT.cut(S, PT.drill(ax, sg, Mt, c[f'D{i}@BORE{i}'], c[f'DEPTH@BORECUT{i}']))
    return S


def turned(S, deg):
    t = gp_Trsf(); t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(deg))
    return BRepBuilderAPI_Transform(S, t, True).Shape()


def leg_frames(sp, n):
    """(axis, sign, rotate_deg) of each leg in the written model, and the other legs' (axis, sign)"""
    if sp.get('e45'): pl = {1: (0, 1, 0), 2: (0, 1, -135)}
    elif sp.get('elbow'): pl = {1: (0, 1, 0), 2: (1, 1, 0)}
    else: pl = {k: (*PT.PLACE[k], 0) for k in range(1, n + 1)}
    return pl


def flats_plane(ax):
    return 1 if ax == 0 else 0           # X leg: XZ plane (normal Y); Y leg: YZ plane (normal X) - r = |z| = the flats


def cmp(exp, got, tag, bad):
    n = 0
    for k, e_ in exp.items():
        g_ = got.get(k) if isinstance(got, dict) else got[k]
        n += 1
        if g_ is None or abs(e_ - g_) > (0.15 if k.endswith('ANG') else TOL): bad.append(f'{tag} {k}: row {round(e_, 5)} / model {g_}')
    return n


def inside(f, P):
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from section import load
    c = BRepClass3d_SolidClassifier(load(f), gp_Pnt(*[x * MM for x in P]), 1e-6)
    return c.State() == TopAbs_IN


def main(roots, out):
    os.makedirs(out, exist_ok=True)
    lines, res, nbad, nchk = [], [], 0, 0
    for root in roots:
        sp = T.SPEC[root]; built, skipped = T.build_rows(root)
        rows = {r['$PRP@PartNo']: r for r in T.load_review(root)[1]}      # the review rows (incl. folded -LN rows): Air-Way's washer face
        for b in built:
            pn = b['pn']; c = b['cols']; legs = b['legs']
            if b['chk']: lines.append(f'{pn}: generator-blocked {b["chk"]}'); continue
            if sp.get('elbow'): S, _ = NM.build(b, e45=bool(sp.get('e45')))
            else: S = build_tee(b)
            # the swivel nut hex cut of a face-seal swivel leg (macro NutHexCutAx: from the nut face over NUTHEXL, flats normal to Z);
            # nwo_model / build_tee cut only the adjustable-ORB lock nuts
            plc = T.place(sp)
            for i_, lg_ in enumerate(legs, 1):
                if lg_['kind'] != 'FSSW': continue
                ax_, sg_ = plc[i_]
                assert ax_ != 'U', 'face-seal swivel on the 45 deg leg: no closed-loop nut cut here'
                S = nut_cut(S, ax_, sg_, c[f'NUTHEX{i_}@NUTHEX{i_}'], lg_['Mtip'] - c[f'DEPTH@NUTCUT{i_}'], lg_['Mtip'])
            f0 = os.path.join(out, f'MODEL_{pn}.stp'); NM.write(S, f0)
            files = {0: f0}
            bad, n = [], 0
            fr = leg_frames(sp, len(legs))
            for i, lg in enumerate(legs, 1):
                ax, sg, rot = fr[i]
                if rot not in files:
                    files[rot] = os.path.join(out, f'MODEL_{pn}_turned{rot}.stp'); NM.write(turned(S, rot), files[rot])
                f = files[rot]; prof._cache.clear()
                oth = []          # the flats plane holds no other leg (all legs lie in the XY plane)
                pnl = flats_plane(ax)
                g = lambda k: c[f'{k}@LEG{i}']
                Mi = g(f'M{i}')
                if lg['kind'] in ('FSM', 'FSBH'):
                    m = M.measure_fsm(f, ax, sg, oth, pn=pnl, bulkhead=lg['kind'] == 'FSBH', partial=bool(lg.get('nostep')))
                    rM = g(f'THDMAJR_B{i}'); ch = rM - g(f'FSM{i}_FACER')
                    exp = dict(face_a=Mi, GI=g(f'FSM{i}_GRVIR'), GO=g(f'FSM{i}_GRVOR'), GD=g(f'FSM{i}_GRVD'), FR=g(f'FSM{i}_FACER'), CH=ch,
                               CH_ANG=g(f'FSMCHANG{i}'), RMAJ=rM, BORER=c[f'D{i}@BORE{i}'] / 2)
                    if lg['kind'] == 'FSM' and lg.get('nostep'):
                        # 2026-10-20: no step - the thread major line runs on past the end length into the forged body
                        n += 1
                        if m.get('THD_END') is None or m['THD_END'] < lg['endlen'] - TOL: bad.append(f'leg {i} no-step leg: thread line ends at {m.get("THD_END")} (end length {lg["endlen"]})')
                    elif lg['kind'] == 'FSM':
                        exp.update(THD_END=ch + g(f'FSM{i}_THDL'), ENDL=ch + g(f'FSM{i}_THDL'), STEPR=g('BODYR'))
                        want_ = 'step' if rM > g('BODYR') else 'step_up'
                        if m.get('RUNOUT') != want_: bad.append(f'leg {i} FSM run-out {m.get("RUNOUT")} (expected the forged {want_})')
                    else:
                        i2, i4 = g(f'FSBH{i}_I2'), g(f'FSBH{i}_STEPL')
                        exp.update(RELR=g(f'FSBH{i}_RELR'), RELL=g(f'FSBH{i}_RELL'), REL_END=i2 - i4, FLANK_ANG=g(f'RELIEFANG{i}'))
                        st = [x for x in m['BH_STEPS'] if x[0] == 'cyl']
                        got_b = dict(STEPR=st[0][1], STEP_s0=st[0][2], STEP_s1=st[0][3], COLLARR=st[1][1], COLLAR_s0=st[1][2], COLLAR_s1=st[1][3])
                        n += cmp(dict(STEPR=g(f'FSBH{i}_STEPR'), STEP_s0=i2 - i4, STEP_s1=i2, COLLARR=g(f'COLLARR{i}'), COLLAR_s0=i2,
                                      COLLAR_s1=i2 + g(f'COLLARL{i}')), got_b, f'leg {i} FSBH', bad)
                    n += cmp(exp, m, f'leg {i} {lg["kind"]}', bad)
                    if m['RINGS']: bad.append(f'leg {i}: an O-ring arc in the model')
                    if lg['kind'] == 'FSM':
                        # 2026-10-20: the thread zone is free of the hex arm - a point just above the thread major, in the hex CORNER direction
                        # (in the legs' plane, normal to the leg), halfway between the hex arm end and the nose chamfer, must lie outside the solid
                        a_ = (Mi - lg['endlen'] + Mi - (rM - g(f'FSM{i}_FACER'))) / 2; q_ = rM + 0.004     # (the measured thread zone, not the arm being checked)
                        P_ = [0.0, 0.0, 0.0]; P_[ax] = sg * a_; P_[1 - ax] = q_
                        n += 1
                        if inside(f, P_): bad.append(f'leg {i}: hex material over the thread at {round(a_, 4)} from the crossing (r {q_:.4f}, hex corner direction)')
                        P0 = [0.0, 0.0, 0.0]; P0[ax] = sg * (lg['hexl'] - 0.01); P0[1 - ax] = (c[f'D{i}@BORE{i}'] / 2 + min(rM, g('BODYR') if lg.get('nostep') is None else rM)) / 2
                        n += 1
                        if not inside(f, P0): bad.append(f'leg {i}: classifier sanity - a point in the leg wall at {P0} reads outside')
                elif lg['kind'] == 'FSSW':
                    m = M.measure_fssw(f, ax, sg, oth, pn=pnl, model=True)
                    Mt = lg['Mtip']; rmin = g(f'FSW{i}_MINR')
                    exp = dict(SEAL_a=Mi, NUTFACE_a=Mt, SEAL_TO_NUTFACE=g(f'FSW{i}_SEAL'), STEMR=g(f'FSW{i}_STEMR'), HEAD_REAR_a=Mi - g(f'FSW{i}_HEADL'),
                               MINR=rmin, TE=lg['cs'] + g(f'FSW{i}_THDL'), NUTL=g(f'FSW{i}_NUTL'),
                               NECKR=g(f'FSW{i}_NECKR'), BODYFACE_a=Mi - g(f'FSW{i}_BODYS'), BORER=c[f'D{i}@BORE{i}'] / 2,
                               NUT_CORNER_R=c[f'NUTHEX{i}@NUTHEX{i}'] / 2)        # flats plane: the nut hex reads its A/F / 2
                    if lg.get('cb'):      # (group B: the angle is the sketch constant FSSW_CBANG - no table column) 2026-10-20: counterbore mouth (-10 up) + 60deg countersink to the minor
                        exp.update(CBR=g(f'FSW{i}_CBR'), CBD=g(f'FSW{i}_CBD'), CB_ANG=T.FSSW_CBANG, CB_CS_DEPTH=lg['cs'] - g(f'FSW{i}_CBD'))
                        n += 1
                        if m.get('MOUTH') != 'cb': bad.append(f'leg {i} FSSW mouth {m.get("MOUTH")} (expected the counterbore)')
                    else:
                        exp.update(MOUTH_R=g(f'FSW{i}_CSR'), MOUTH_DEPTH=lg['cs'])
                    n += cmp(exp, m, f'leg {i} FSSW', bad)
                    # the nut hex runs from the nut face over NUTHEXL, then the skirt cone / skirt
                    hx = m['NUT_HEX_s']; n += 1
                    if not hx or abs(hx[1] - g(f'FSW{i}_NUTHEXL')) > TOL: bad.append(f'leg {i} nut hex ends at {hx} (row NUTHEXL {g(f"FSW{i}_NUTHEXL")})')
                elif lg['kind'] == 'NWO':
                    m = M.measure_stud(f, ax, sg, oth, pn=pnl, model=True)
                    n_ = lg['nut']
                    exp = dict(tip_a=Mi, RMAJ=g(f'THDMAJR_B{i}'), THD_END=g(f'NW{i}_THDL'), UCR=g(f'NW{i}_UCR'), BORER=c[f'D{i}@BORE{i}'] / 2,
                               SHOULDER=Mi - n_['w0'] - g(f'NW{i}_WASHT'), UCL=Mi - n_['w0'] - g(f'NW{i}_WASHT') - g(f'NW{i}_THDL'))
                    n += cmp(exp, m, f'leg {i} NWO stud', bad)
                    # the washer face is where Air-Way puts it (L11 / L14 from the crossing)
                    n += 1; wf = round(Mi - m['SHOULDER'], 4); wrow = rows[pn][sp['fs_wf']]
                    if abs(wf - wrow) > TOL: bad.append(f'leg {i} washer face at {wf} from the crossing vs the row {sp["fs_wf"].split("@")[0]} {wrow}')
                elif lg['kind'] == 'NPTFM':
                    m = None          # male pipe legs: the closed loops of the accepted NPTFM legs cover them
                else:
                    bad.append(f'leg {i}: kind {lg["kind"]} has no closed-loop reader here')
            nchk += n; nbad += len(bad)
            r = dict(pn=pn, checks=n, off=len(bad), solids=NM.nsolids(S) if hasattr(NM, 'nsolids') else PT.nsolids(S), volume=round(PT.vol(S), 5), bad=bad)
            pil = T.G.P.step(pn)
            if os.path.exists(pil):
                from section import load
                vb = PT.vol(load(pil)); r['brennan_volume'] = round(vb, 5); r['diff_pct'] = round(100 * (r['volume'] - vb) / vb, 2)
            if r['solids'] != 1: bad.append(f"{r['solids']} solids"); nbad += 1
            res.append(r)
            lines.append(f"{pn}: {n} checks, {len(bad)} off; solids {r['solids']}, volume {r['volume']} in^3"
                         + (f"; Brennan pilot {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '') + ''.join('\n   OFF ' + x for x in bad))
    lines.append(f'\nFS tee / elbow closed loop {"PASS" if nbad == 0 else "FAIL"}: {len(res)} configurations, {nchk} checks, {nbad} off (tolerance {TOL})')
    json.dump(res, open(os.path.join(out, 'closed_loop_tee.json'), 'w'), indent=1)
    open(os.path.join(out, 'closed_loop_tee.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]; out = os.path.join(HERE, 'ocp')
    if '--out' in a: k = a.index('--out'); out = a[k + 1]; del a[k:k + 2]
    main(a, out)
