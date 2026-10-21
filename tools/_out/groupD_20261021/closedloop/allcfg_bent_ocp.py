"""allcfg_bent_ocp.py (group D, 2026-10-21): the bent-tube masters' all-configuration check (the gen_bent counterpart of
checks/allcfg_check.py): EVERY generated configuration is built in OCP from gen_bent's own numbers (bent_ocp.model, threads off) and must
be one valid solid with a positive volume whose box equals the macro's per-configuration box check (expected_box, 0.01 in), and the
outlines (end-piece chain, head / swivel half-section) must not self-intersect.
    OMI_ROOT=<brennancad stage> GS_OUT=<scratch> GB_REV=stage python allcfg_bent_ocp.py   -> closedloop/allcfg.txt
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bent_ocp as B
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID

sys.path.insert(0, os.path.join(B.H, 'tools_gd', 'checks'))
os.environ.setdefault('GT_OUT', os.environ.get('GS_OUT', '/tmp'))
from allcfg_check import poly_issues          # the straights' outline test (zero segments, self-intersection)


def nsolids(s):
    e = TopExp_Explorer(s, TopAbs_SOLID); n = 0
    while e.More():
        n += 1; e.Next()
    return n


def main():
    gb = B.load_gb()
    out, bad, exp = [], 0, {}
    for root in ('1704T', '1703T', '6701'):
        built = [b for b in gb.build_rows(root)[0] if not b[1]]
        for cols, _, X in built:
            pn = cols['$PRP@PartNo']
            c, g, J, lib = X['c'], X['g'], X['J'], X['lib']
            issues = []
            V, _ = gb.end1_profile(c, J)
            issues += [f'end piece: {x}' for x in poly_issues(V)]
            if lib is not None:
                F, u, n = (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)            # the head section in its own (a, r) frame
                rO = c['O'] / 2
                sec = [(0, 0), (0, lib['GI']), (lib['GD'], lib['GI']), (lib['GD'], lib['GO']), (0, lib['GO']), (0, rO), (lib['TH'], rO)]
                sec += [(lib['TH'], c['HUBD'] / 2), (c['HUBL'], c['HUBD'] / 2), (c['HUBL'], 0)] if 'HUBD' in c else [(lib['TH'], 0)]
                issues += [f'head section: {x}' for x in poly_issues(sec)]
            s = B.model(gb, X, cols)
            ok_valid = BRepCheck_Analyzer(s).IsValid()
            ns = nsolids(s)
            v = B.vol(s)
            bx = B.box(s)
            e = X['box']
            got = dict(xmax=bx[3], ymax=bx[4], ymin=bx[1], zmax=bx[5])
            dev = {k: round(got[k] - e[k], 4) for k in e}
            if not ok_valid: issues.append('OCP solid not valid')
            if ns != 1: issues.append(f'{ns} solids')
            if v <= 0: issues.append(f'volume {v}')
            if any(abs(d) > 0.01 for d in dev.values()): issues.append(f'box off the macro check: {dev}')
            bad += bool(issues)
            exp[pn] = dict(root=root, volume=round(v, 6), size=[round(bx[3] - bx[0], 5), round(bx[4] - bx[1], 5), round(bx[5] - bx[2], 5)])
            out.append(f'{root:6} {pn:18} {"OK " if not issues else "BAD"} vol {v:.4f} in^3  box dev {dev}' + (f'  {issues}' if issues else ''))
            print(out[-1], flush=True)
    out.append(f'{len(out)} configurations, {bad} with problems')
    print(out[-1])
    open(os.path.join(B.H, 'closedloop', 'allcfg.txt'), 'w').write('\n'.join(out) + '\n')
    import json
    json.dump(exp, open(os.path.join(B.H, 'dryrun', 'expected_ocp.json'), 'w'), indent=1)     # for scripts/verdict.py
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
