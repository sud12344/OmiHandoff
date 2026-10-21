"""regen_fs.py (2026-10-20): regenerate the FS roots (+ 4000 is gen_ring, not touched) with the staging toolset into regen_after/, then diff
against backup_20261020/regen_before (= orfs_gen_20261020/regen/new before the -10 TE fix): macro lines (generated-date aside, CRLF ignored),
SW2 cell by cell. Prints every differing root with its changed lines / cells."""
import os, subprocess, sys, glob
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
TOOLS = os.path.join(ROOT, 'tools', '_out', 'orfs_gen_20261020', 'tools')
EXTRA = os.path.join(ROOT, 'tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')
BEFORE = os.path.join(HERE, "backup_20261020", os.environ.get("REGEN_BEFORE", "regen_before"))
AFTER = os.path.join(HERE, os.environ.get("REGEN_AFTER", "regen_after"))
GENS = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def sw2(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


n_diff = 0
for kind, (g, var) in GENS.items():
    roots = sorted({os.path.basename(p)[len('Build_'):-len('_MASTER.bas')] for p in glob.glob(os.path.join(BEFORE, kind, 'Build_FS*_MASTER.bas'))})
    d = os.path.join(AFTER, kind); os.makedirs(d, exist_ok=True)
    for r in roots:
        p = subprocess.run([sys.executable, '-I', os.path.join(TOOLS, 'generators', g), r],
                           env=dict(os.environ, OMI_ROOT=ROOT, OMI_REV_EXTRA=EXTRA, **{var: d}), capture_output=True, text=True)
        m0, m1 = (os.path.join(x, kind, f'Build_{r}_MASTER.bas') for x in (BEFORE, AFTER))
        t0, t1 = (os.path.join(x, kind, f'DesignTable_{r}_SW2.xlsx') for x in (BEFORE, AFTER))
        if not os.path.exists(m1):
            print(f'{kind} {r}: NO MACRO (rc {p.returncode}) {p.stderr[-300:]}'); n_diff += 1; continue
        a, b = mac(m0), mac(m1)
        ml = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y] + ([('len', len(a), len(b))] if len(a) != len(b) else [])
        ta, tb = sw2(t0), sw2(t1)
        cells = [(ta[0][j], ta[i][0], x, y) for i, (ra, rb) in enumerate(zip(ta, tb)) for j, (x, y) in enumerate(zip(ra, rb)) if x != y]
        if len(ta) != len(tb) or any(len(x) != len(y) for x, y in zip(ta, tb)):
            cells.append(('shape', len(ta), len(tb)))
        if ml or cells:
            n_diff += 1
            print(f'{kind} {r}: macro lines changed {len(ml)}, SW2 cells changed {len(cells)}')
            for x in ml[:6]: print('   macro', x)
            for x in cells[:12]: print('   cell ', x)
print(n_diff, 'FS root(s) differ')
