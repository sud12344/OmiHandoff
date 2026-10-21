"""Batch 18 ship (2026-10-20, user: "Ship batch 18 as staged, including the 40 cells as Air-Way."). python ship_b18.py [go]  (plan without 'go')

Batch 18 = (a) Air-Way first (airway_first_20261020: 320 cells back to Air-Way + 4 Brennan cells, 26 roots, incl. the 40 cells of the Triveni
draft as Air-Way), (b) the ORFS generator stage (50 FS masters) + the O-ring master 4000 (4000 / 4001 / FS4000), (c) A14 1603-08-08-08-FG,
(d) the held roots of QA #175 fixed: 1700RC 1800 1703 4503 4603 (5404N stays held). One toolset tools_b18, one input set root18 + the FS /
O-ring review tables; prep_b18.py (KEEP_TOOLS=1) proves every macro / SW2 equals the file its SolidWorks dry run built.
Per file the OLD live copy is MOVED to _to_delete/superseded_20261020/batch18_replaced/<path> AND copied to old_files/<path> (MANIFEST.txt).
New files are COPIED (staging keeps its copies):
  part + report   the dry-run folder of the root                    -> 11_MASTERS / 03_SCRIPTS
  macro + SW2     regen/<straight|tee|ring>/                         -> 03_SCRIPTS (CRLF -> LF) / 04_DESIGN_TABLES
  review tables   root18 where it differs from live (Air-Way 26 + 1603), brennan_yes_20261018/stage_orfs (FS, 51),
                  newtypes_20261014/review_tables (4000 / 4001: live = the 2026-09-23 empty skeletons)  -> 04_DESIGN_TABLES
  toolchain       tools_b18 -> tools/ (changed + new files; not __pycache__, _out, *.orig, coverage/work)"""
import filecmp, hashlib, json, os, shutil, sys

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
S = os.path.join(R, r'tools\_out\batch18_20261020')
AF = os.path.join(R, r'tools\_out\airway_first_20261020')
OR = os.path.join(R, r'tools\_out\orfs_dryrun_20261020')
TD = os.path.join(R, '_to_delete', 'superseded_20261020', 'batch18_replaced')
OF = os.path.join(S, 'old_files')
TN = os.path.join(S, 'tools_b18')
GO = len(sys.argv) > 1 and sys.argv[1] == 'go'

af_roots = sorted(json.load(open(os.path.join(AF, 'dryrun', 'roots.json'))))
orfs_roots = sorted(l.split()[1] for l in open(os.path.join(OR, 'VERDICT.txt'), encoding='utf-8') if l.startswith('PASS '))
# FS2403 / FS6400 were built by hand on 2026-10-20 (not in VERDICT.txt): rebuilt from the final macros into dryrun/ (out_fs2.txt, 0 FAIL)
own_roots = ['1603', '1700RC', '1800', '1703', '4503', '4603', 'FS2403', 'FS6400']
assert len(af_roots) == 26 and len(orfs_roots) == 49 and not set(orfs_roots) & set(own_roots), (len(af_roots), len(orfs_roots))
DRY = {**{r: os.path.join(AF, 'dryrun', r) for r in af_roots}, **{r: os.path.join(OR, r) for r in orfs_roots},
       **{r: os.path.join(S, 'dryrun', r) for r in own_roots}}
assert len(DRY) == 26 + 49 + 8
# verdicts: Air-Way first (checks/dryrun_verdict.txt), ORFS (VERDICT.txt), own dry runs (report: 0 FAIL)
afv = open(os.path.join(AF, 'checks', 'dryrun_verdict.txt'), encoding='utf-8').read().splitlines()
for r in af_roots:
    assert any(l.split()[:2] == [r, 'PASS'] for l in afv), 'Air-Way verdict ' + r
for r in own_roots:
    rep = open(os.path.join(DRY[r], f'Build_{r}_report.txt'), encoding='utf-8', errors='replace').read()
    assert 'FAIL' not in rep and 'Saved to' in rep, 'own dry run ' + r


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def macro_lines(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


new = []
for r in sorted(DRY):
    sub = next(s for s in ('straight', 'tee', 'ring') if os.path.exists(os.path.join(S, 'regen', s, f'Build_{r}_MASTER.bas')))
    g = os.path.join(S, 'regen', sub)
    new += [(os.path.join(DRY[r], f'{r}_MASTER.SLDPRT'), f'11_MASTERS/{r}_MASTER.SLDPRT', 'copy'),
            (os.path.join(DRY[r], f'Build_{r}_report.txt'), f'03_SCRIPTS/Build_{r}_report.txt', 'copy'),
            (os.path.join(g, f'Build_{r}_MASTER.bas'), f'03_SCRIPTS/Build_{r}_MASTER.bas', 'lf'),
            (os.path.join(g, f'DesignTable_{r}_SW2.xlsx'), f'04_DESIGN_TABLES/DesignTable_{r}_SW2.xlsx', 'copy')]
tables = {}
DT18 = os.path.join(S, 'root18', '04_DESIGN_TABLES')
for f in sorted(os.listdir(DT18)):
    if f.startswith('DesignTable_') and f.endswith('.xlsx') and '_SW2' not in f:
        live = os.path.join(R, '04_DESIGN_TABLES', f)
        if not os.path.exists(live) or not filecmp.cmp(os.path.join(DT18, f), live, shallow=False):
            tables[f] = os.path.join(DT18, f)
for d in (os.path.join(R, r'tools\_out\brennan_yes_20261018\stage_orfs\04_DESIGN_TABLES'), os.path.join(R, r'tools\_out\newtypes_20261014\review_tables')):
    for f in sorted(os.listdir(d)):
        if f.startswith('DesignTable_') and f.endswith('.xlsx'):
            assert f not in tables, 'table from two sources: ' + f
            live = os.path.join(R, '04_DESIGN_TABLES', f)
            if not os.path.exists(live) or not filecmp.cmp(os.path.join(d, f), live, shallow=False):
                tables[f] = os.path.join(d, f)
new += [(tables[f], f'04_DESIGN_TABLES/{f}', 'copy') for f in sorted(tables)]
for dp, dn, fn in os.walk(TN):
    dn[:] = [x for x in dn if x not in ('__pycache__', '_out') and not (os.path.basename(dp) == 'coverage' and x == 'work')]
    for f in fn:
        if f.endswith('.orig') or f.endswith('.pyc'):
            continue
        src = os.path.join(dp, f); rel = 'tools/' + os.path.relpath(src, TN).replace('\\', '/')
        live = os.path.join(R, rel)
        # line endings ignored: the ORFS staging copy came back from the cloud with LF - 57 files differ only in CR (keep the live copy)
        if not os.path.exists(live) or open(src, 'rb').read().replace(b'\r\n', b'\n') != open(live, 'rb').read().replace(b'\r\n', b'\n'):
            new.append((src, rel, 'copy'))
dst_seen = set()
for s, d, how in new:
    assert os.path.isfile(s), s
    assert d not in dst_seen, 'two sources for ' + d
    dst_seen.add(d)
old = [d for s, d, how in new if os.path.exists(os.path.join(R, d))]
print(f'ship {len(DRY)} roots (Air-Way {len(af_roots)}, ORFS/O-ring {len(orfs_roots)}, own {len(own_roots)}), {len(tables)} review tables; '
      f'{len(old)} old files to supersede, {len(new)} new files to place; GO={GO}')
if not GO:
    for p in old:
        print('  old', p)
    for s, d, how in new:
        print(f'  {how:4} {os.path.relpath(s, R)} -> {d}')
    sys.exit()

man = []
for p in old:
    src = os.path.join(R, p); h = sha(src)
    for base in (OF, TD):
        os.makedirs(os.path.dirname(os.path.join(base, p)), exist_ok=True)
    assert not os.path.exists(os.path.join(TD, p)), 'already in _to_delete: ' + p
    shutil.copy2(src, os.path.join(OF, p))
    shutil.move(src, os.path.join(TD, p))
    assert sha(os.path.join(OF, p)) == h and sha(os.path.join(TD, p)) == h, p
    man.append(f'{h}  {p}')
for base in (OF, TD):
    open(os.path.join(base, 'MANIFEST.txt'), 'w', encoding='utf-8').write(
        'Batch 18 (2026-10-20): files replaced by the ship (sha256  path relative to OMi_Handoff). Second copy: '
        + ('_to_delete/superseded_20261020/batch18_replaced/' if base == OF else 'tools/_out/batch18_20261020/old_files/') + '\n'
        + '\n'.join(man) + '\n')
log = []
for s, d, how in new:
    dst = os.path.join(R, d)
    assert not os.path.exists(dst), 'target exists: ' + d
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    h = sha(s)
    if how == 'copy':
        shutil.copy2(s, dst)
        assert sha(dst) == h
    else:
        b = open(s, 'rb').read()
        open(dst, 'wb').write(b.replace(b'\r\n', b'\n'))
    log.append(f'{sha(dst)}  {d}   <- {how} {os.path.relpath(s, R)} (source sha256 {h})')
os.makedirs(os.path.join(S, 'checks'), exist_ok=True)
open(os.path.join(S, 'checks', 'shipped_files_sha256.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
print('done:', len(man), 'old files superseded,', len(log), 'new files placed')
