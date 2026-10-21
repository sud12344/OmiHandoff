"""closed_loop_orbport.py (group B, 2026-10-21): OCP closed loop of the female ORB port legs (gen_tee leg_ORBPORT: 6815 / 6832 / 6835).
Every configuration is rebuilt from the generator's own leg profiles and SW2 values in the macro's feature order - elbow: legs + hex arms + the
30deg corner puck (measure/nwo_model.body), tee: legs + run bar + branch arm (measure/pipetee_model); the adjustable-ORB lock-nut hex cut; the
pockets / connecting bores / stud bores; the port MOUTH (the ORBMOUTHi loop revolved about the leg axis, cut) - written as a STEP, read back and
each port measured with the reader of tools/measure/ports.py (measure_orbf, applied to one leg): face position, face radius RF, O-ring chamfer
angle and foot radius RC, minor radius (port drill / 2) and minor-bore depth P must return the row. The same reader on the Brennan STEP of the
family (where 09_STEP_FILES has the part) must agree with the model within the Air-Way rounding of the port drill. Threads are not modelled.
  OMI_ROOT=<group B stage> python closed_loop_orbport.py 6815 6832 6835 [--out DIR]"""
import os, sys, json, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T_ = os.path.join(HERE, 'tools_af')
for p_ in (os.path.join(T_, 'generators'), os.path.join(T_, 'measure'), T_):
    sys.path.insert(0, p_)
os.environ.setdefault('GT_OUT', os.path.join(HERE, 'scratch', 'cl_orbport'))
import gen_tee as T
import nwo_model as NM
import pipetee_model as PT
import prof
from swiv import seg_list, near
from ports import ang
from OCP.gp import gp_Pnt, gp_Ax1, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakeBox
from section import load

TOL = 0.0015
MM = 25.4


def port_reading(p, axis, sign):
    """measure_orbf (tools/measure/ports.py) on one leg: section through the leg axis (plane normal Z), the leg face = the largest a"""
    E = prof.leg_edges(p, axis, sign, 2, a0=-99)
    S = [s for s in seg_list(E) if min(s['r1'], s['r2']) > -1e-6]
    af = max(max(s['a1'], s['a2']) for s in S)
    ch = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 9 < ang(s) < 18]
    if not ch: return None
    ch = ch[0]; RF, RC = ch['r2'], ch['r1']
    horiz = [s for s in S if near(s['r1'], s['r2'], 1e-3) and s['a2'] - s['a1'] > 0.05 and s['a2'] < ch['a1'] + 0.06 and s['r1'] < RC - 0.005]
    mn = max(horiz, key=lambda s: s['a2'])
    return dict(face=round(af, 4), RF=round(RF, 4), RC=round(RC, 4), CHANG=round(ang(ch), 2), MINR=round(mn['r1'], 4), P=round(af - mn['a1'], 4))


def place(sp, i):
    return T.place(sp)[i]


def build(root, b):
    sp = T.SPEC[root]; legs = b['legs']; c = b['cols']
    if sp.get('elbow'):
        S = NM.body(b)
        for i, lg in enumerate(legs):
            if lg['kind'] != 'NWO': continue
            n = lg['nut']; BIG = 20.0
            slab = BRepPrimAPI_MakeBox(gp_Pnt(-BIG * MM, n['n0'] * MM, -BIG * MM), gp_Pnt(BIG * MM, n['w0'] * MM, BIG * MM)).Shape() if i == 1 else \
                BRepPrimAPI_MakeBox(gp_Pnt(n['n0'] * MM, -BIG * MM, -BIG * MM), gp_Pnt(n['w0'] * MM, BIG * MM, BIG * MM)).Shape()
            S = NM.cut(S, NM.cut(slab, NM.hex_prism(i, n['af'], n['n0'], n['w0'])))
        for i, lg in enumerate(legs, 1):
            ax, sg = place(sp, i); M = lg['V'][-1][0]
            if lg['kind'] == 'NPTFF':
                S = PT.cut(S, PT.drill(ax, sg, M, c[f'TAPDRILL{i}@POCKET{i}'], c[f'DEPTH@POCKETCUT{i}']))
                if f'D{i}@BORE{i}' in c: S = PT.cut(S, PT.drill(ax, sg, M, c[f'D{i}@BORE{i}'], c[f'DEPTH@BORECUT{i}']))
            else: S = PT.cut(S, PT.drill(ax, sg, M, c[f'D{i}@BORE{i}'], M))
    else:
        S, _ = PT.build(b, False)
        for i, lg in enumerate(legs, 1):
            if lg['kind'] != 'NWO': continue
            ax, sg = place(sp, i); n = lg['nut']; BIG = 20.0
            lo = [-BIG * MM] * 3; hi = [BIG * MM] * 3; x0, x1 = sorted((sg * n['n0'], sg * n['w0'])); lo[ax] = x0 * MM; hi[ax] = x1 * MM
            S = PT.cut(S, PT.cut(BRepPrimAPI_MakeBox(gp_Pnt(*lo), gp_Pnt(*hi)).Shape(), PT.hex_prism(ax, n['af'], x0, x1)))
    rem = {}
    for i, lg in enumerate(legs, 1):
        if not lg.get('orbmouth'): continue
        ax, sg = place(sp, i); om = lg['orbmouth']
        d = gp_Dir(sg, 0, 0) if ax == 0 else gp_Dir(0, sg, 0)
        tool = BRepPrimAPI_MakeRevol(PT.face([PT.pt(ax, sg, a, r) for a, r in om['pts']]), gp_Ax1(gp_Pnt(0, 0, 0), d), 2 * math.pi).Shape()
        v0 = PT.vol(S); S = PT.cut(S, tool); rem[i] = (v0 - PT.vol(S), om['vol'])
    return S, rem


def main(roots, out):
    os.makedirs(out, exist_ok=True); lines, res, nbad, nchk = [], [], 0, 0
    for root in roots:
        sp = T.SPEC[root]; built, _ = T.build_rows(root)
        for b in built:
            pn = b['pn']
            if b['chk']: lines.append(f'{pn}: generator-blocked {b["chk"]}'); continue
            S, rem = build(root, b); f = os.path.join(out, f'MODEL_{pn}.stp'); NM.write(S, f); prof._cache.clear()
            bad, n = [], 0
            pil = os.path.join(HERE, '..', '..', '..', '09_STEP_FILES', f'BRENNAN_{pn}.stp'); have_pil = os.path.exists(pil)     # the repo's STEPs (OMI_ROOT = the stage)
            for i, lg in enumerate(b['legs'], 1):
                if not lg.get('orbmouth'): continue
                ax, sg = place(sp, i); om = lg['orbmouth']; m = om['m']; M = lg['V'][-1][0]
                got = port_reading(f, ax, sg)
                # in the section plane the pocket bottom (at M - P) disappears where another leg's bore crosses it (|a| < that bore radius): the
                # reader then sees the minor line end at the other bore - expected reading min(P, M - the largest other bore radius)
                r_o = max([(o_.get('bore') or (o_['td'] if o_['kind'] == 'NPTFF' else 0)) / 2 for o_ in b['legs'] if o_ is not lg] + [0.0])
                exp = dict(face=M, RF=m['RF'], RC=m['RC'], CHANG=m['CHANG'], MINR=lg['td'] / 2, P=min(lg['P1'], M - r_o) if not lg['to_centre'] else None)
                if got is None: bad.append(f'leg {i}: no ORB port read'); n += 1; continue
                for k, v in exp.items():
                    if v is None: continue
                    n += 1
                    if abs(got[k] - v) > (0.15 if k == 'CHANG' else TOL): bad.append(f'leg {i} {k}: row {round(v, 4)} / model {got[k]}')
                n += 1; rv, ev = rem[i]
                if abs(rv - ev) > 0.02 * ev: bad.append(f'leg {i} mouth cut removed {rv:.6f} in^3 vs generator {ev:.6f}')
                if have_pil:
                    # Brennan draws the legs mirrored on some families: read the port on the leg of the same length (the reader takes any axis)
                    cand = [x for x in (port_reading(pil, a_, s_) for a_ in (0, 1) for s_ in (1, -1)) if x and abs(x['face'] - M) < 0.006]
                    if not cand: bad.append(f'leg {i}: no Brennan port at {M} on the pilot STEP'); n += 1
                    else:
                        bp = cand[0]
                        for k in ('face', 'RF', 'RC', 'CHANG', 'MINR'):
                            n += 1
                            if abs(bp[k] - got[k]) > (0.15 if k == 'CHANG' else 0.006 if k == 'MINR' else 0.004): bad.append(f'leg {i} {k}: Brennan {bp[k]} / model {got[k]}')
                        lines.append(f'   {pn} leg {i} port: model {got} | Brennan {bp}')
            r = dict(pn=pn, checks=n, off=len(bad), solids=PT.nsolids(S), volume=round(PT.vol(S), 5), bad=bad)
            if have_pil:
                vb = PT.vol(load(pil)); r['brennan_volume'] = round(vb, 5); r['diff_pct'] = round(100 * (r['volume'] - vb) / vb, 2)
            if r['solids'] != 1: bad.append(f"{r['solids']} solids")
            nchk += n; nbad += len(bad); res.append(r)
            lines.append(f"{pn}: {n} checks, {len(bad)} off; solids {r['solids']}, volume {r['volume']} in^3"
                         + (f"; Brennan {r['brennan_volume']} in^3 ({r['diff_pct']:+} %)" if 'brennan_volume' in r else '') + ''.join('\n   OFF ' + x for x in bad))
    lines.append(f'\nORB port closed loop {"PASS" if nbad == 0 else "FAIL"}: {len(res)} configurations, {nchk} checks, {nbad} off (tolerance {TOL})')
    json.dump(res, open(os.path.join(out, 'closed_loop_orbport.json'), 'w'), indent=1)
    open(os.path.join(out, 'closed_loop_orbport.txt'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    a = sys.argv[1:]; out = os.path.join(HERE, 'ocp', 'orbport')
    if '--out' in a: k = a.index('--out'); out = a[k + 1]; del a[k:k + 2]
    main(a, out)
