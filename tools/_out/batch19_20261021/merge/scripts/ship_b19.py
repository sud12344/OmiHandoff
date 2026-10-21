"""Batch 19 ship (2026-10-21, user: "finish the 94 parts that need no input from me"). python ship_b19.py [go]  (plan without 'go')

Batch 19 = the 94-part "(d) generator / table work only" list of tools/_out/blocked_needs_20261020/BLOCKED_NEEDS.md, staged by five agents
(A_answered, B_newspec, C_ownstep, D_geom, E_gen) and merged here: tools_b19 (live tools + their generator patches; 2502 parked in SPEC_WAITING
after its dry run), root19 (live tables + their 34 edited / new review tables). regen19.py: no old configuration changes in any SW2;
SolidWorks dry runs 31 / 31 PASS (checks/dryrun_verdict.txt).
Per file the OLD live copy is MOVED to _to_delete/superseded_20261021/batch19_replaced/<path> AND copied to old_files/<path> (MANIFEST.txt).
New files are COPIED:
  part + report   dryrun/<root>/                                  -> 11_MASTERS / 03_SCRIPTS
  macro + SW2     regen/<straight|tee|ring>/                     -> 03_SCRIPTS (CRLF -> LF) / 04_DESIGN_TABLES
  review tables   root19 where it differs from live (34)          -> 04_DESIGN_TABLES
  toolchain       tools_b19 -> tools/ (content changes + new files; line endings ignored)
RETIRED (A7: moved to the generator): the hand-built 2500HX / 2603HX master, macro, report and SW2 (replaced by 2500 / 2603) - moved like old
files, no new file at their path. 2502HX stays (2502 parked)."""
import hashlib, json, os, shutil, sys

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
M = os.path.join(R, r'tools\_out\batch19_20261021\merge')
TD = os.path.join(R, '_to_delete', 'superseded_20261021', 'batch19_replaced')
OF = os.path.join(M, 'old_files')
TN = os.path.join(M, 'tools_b19')
GO = len(sys.argv) > 1 and sys.argv[1] == 'go'
ship = json.load(open(os.path.join(M, 'ship_roots.json')))
verdict = json.load(open(os.path.join(M, 'checks', 'dryrun_verdict.json')))
assert len(ship) == 31 and '2502' not in ship and '5404N' not in ship
for r in ship:
    assert not verdict[r]['issues'], (r, verdict[r]['issues'])
RETIRE = [f'{p}' for hx in ('2500HX', '2603HX') for p in (f'11_MASTERS/{hx}_MASTER.SLDPRT', f'03_SCRIPTS/Build_{hx}_MASTER.bas',
                                                           f'03_SCRIPTS/Build_{hx}_report.txt', f'04_DESIGN_TABLES/DesignTable_{hx}_SW2.xlsx')]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def body(p):
    return open(p, 'rb').read().replace(b'\r\n', b'\n')


new = []
for r in sorted(ship):
    g = os.path.join(M, 'regen', ship[r]); d = os.path.join(M, 'dryrun', r)
    new += [(os.path.join(d, f'{r}_MASTER.SLDPRT'), f'11_MASTERS/{r}_MASTER.SLDPRT', 'copy'),
            (os.path.join(d, f'Build_{r}_report.txt'), f'03_SCRIPTS/Build_{r}_report.txt', 'copy'),
            (os.path.join(g, f'Build_{r}_MASTER.bas'), f'03_SCRIPTS/Build_{r}_MASTER.bas', 'lf'),
            (os.path.join(g, f'DesignTable_{r}_SW2.xlsx'), f'04_DESIGN_TABLES/DesignTable_{r}_SW2.xlsx', 'copy')]
DT = os.path.join(M, 'root19', '04_DESIGN_TABLES')
for f in sorted(os.listdir(DT)):
    if f.startswith('DesignTable_') and f.endswith('.xlsx') and '_SW2' not in f:
        live = os.path.join(R, '04_DESIGN_TABLES', f)
        if not os.path.exists(live) or body(os.path.join(DT, f)) != body(live):
            new.append((os.path.join(DT, f), f'04_DESIGN_TABLES/{f}', 'copy'))
for dp, dn, fn in os.walk(TN):
    dn[:] = [x for x in dn if x not in ('__pycache__', '_out') and not (os.path.basename(dp) == 'coverage' and x == 'work')]
    for f in fn:
        if f.endswith(('.orig', '.pyc', '.rej')):
            continue
        src = os.path.join(dp, f); rel = 'tools/' + os.path.relpath(src, TN).replace('\\', '/')
        live = os.path.join(R, rel)
        if not os.path.exists(live) or body(src) != body(live):
            new.append((src, rel, 'copy'))
dsts = [d for s, d, h in new]
assert len(dsts) == len(set(dsts))
for s, d, how in new:
    assert os.path.isfile(s), s
old = [d for d in dsts if os.path.exists(os.path.join(R, d))] + RETIRE
for p in RETIRE:
    assert os.path.exists(os.path.join(R, p)), p
print(f'ship {len(ship)} roots; {len(old)} old files to supersede (incl. {len(RETIRE)} retired HX files), {len(new)} new files; GO={GO}')
if not GO:
    for p in old: print('  old', p)
    for s, d, how in new: print(f'  {how:4} {os.path.relpath(s, R)} -> {d}')
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
    man.append(f'{h}  {p}' + ('   (RETIRED: hand-built HX, A7)' if p in RETIRE else ''))
for base in (OF, TD):
    open(os.path.join(base, 'MANIFEST.txt'), 'w', encoding='utf-8').write(
        'Batch 19 (2026-10-21): files replaced or retired by the ship (sha256  path relative to OMi_Handoff). Second copy: '
        + ('_to_delete/superseded_20261021/batch19_replaced/' if base == OF else 'tools/_out/batch19_20261021/merge/old_files/') + '\n'
        + '\n'.join(man) + '\n')
log = []
for s, d, how in new:
    dst = os.path.join(R, d)
    assert not os.path.exists(dst), 'target exists: ' + d
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    h = sha(s)
    if how == 'copy':
        shutil.copy2(s, dst); assert sha(dst) == h
    else:
        open(dst, 'wb').write(open(s, 'rb').read().replace(b'\r\n', b'\n'))
    log.append(f'{sha(dst)}  {d}   <- {how} {os.path.relpath(s, R)} (source sha256 {h})')
open(os.path.join(M, 'checks', 'shipped_files_sha256.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
print('done:', len(man), 'old files superseded / retired,', len(log), 'new files placed')
