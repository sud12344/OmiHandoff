"""Batch 17 ship (2026-10-19, user: "can you ship batch 17?"). python ship_b17.py [go]   (without 'go' = plan only)

Batch 17 = the 2026-10-18 stage (brennan_yes_20261018/stage: OMi answers, Brennan rows waves 1-3, A19-A23, the 37 wrongly-DROP adapters
+ wave-3 adapter rows, the generator-feature rows) checked against the live state after batch 16 (checks/cmp3_full.txt: 0 stale cells),
regenerated with tools_b17 (= genfeat_20261018/merged/tools = live tools + 5 features, + the Atan2V ByVal fix) -> regen/b17v2.
Per shipped root the OLD live files (11_MASTERS part, 03_SCRIPTS macro + report, 04 SW2) and every replaced review table / tools file are
MOVED to _to_delete/superseded_20261019b/batch17_replaced/<folder>/ AND copied to tools/_out/batch17_20261019/old_files/<folder>/
(MANIFEST.txt in both). New files are COPIED (staging keeps its copies):
  part + report   sw_dryrun/<root>/ (the SolidWorks dry run)       -> 11_MASTERS / 03_SCRIPTS
  macro + SW2     regen/b17v2/<sub>/ (what built that part)          -> 03_SCRIPTS (CRLF -> LF) / 04_DESIGN_TABLES
  review tables   root/04_DESIGN_TABLES (= the stage's tables) where they differ from live -> 04_DESIGN_TABLES
  toolchain       tools_b17 -> tools/ (changed + new files; not __pycache__, _out, *.orig, coverage/work)
Roots shipped = every changed root (checks/b17_roots.json) whose dry run is PASS in checks/verdict.json, minus HOLD."""
import filecmp, hashlib, json, os, shutil, sys

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
S = os.path.join(R, r'tools\_out\batch17_20261019')
TD = os.path.join(R, '_to_delete', 'superseded_20261019b', 'batch17_replaced')
OF = os.path.join(S, 'old_files')
TN = os.path.join(S, 'tools_b17')
DT = os.path.join(S, 'root', '04_DESIGN_TABLES')
GO = len(sys.argv) > 1 and sys.argv[1] == 'go'
HOLD = {'4503': 'hose face-off on the 135 deg hose leg fails (HOSEFACE2 / STUBFILL2, bore D2 picks the face-off circle)',
        '4603': 'hose face-off on the second (hose) leg fails (HOSEFACE2 / STUBFILL2)',
        '1703': 'leg-2 hex arm (HEX2) extrudes the wrong way in both directions at -24',
        '1700RC': 'FLATS sketch not fully defined in SolidWorks (cut made, sketch under-defined)',
        '1800': 'FLATS sketch not fully defined in SolidWorks (cut made, sketch under-defined)',
        '5404N': '-06 thread sweeps fail again (QA #163) + body diameter check 0.8861 / 0.8931 vs 0.880; the 4-configuration master stays'}

info = json.load(open(os.path.join(S, 'checks', 'b17_roots.json')))
verdict = json.load(open(os.path.join(S, 'checks', 'verdict.json')))
changed = sorted(r for r in info if info[r]['changed'] and info[r]['b17'] > 0)
missing = [r for r in changed if r not in HOLD and r not in verdict]
notpass = [r for r in changed if r not in HOLD and r in verdict and verdict[r]['issues']]
assert not missing and not notpass, ('no verdict', missing, 'not PASS', notpass)
SHIP = [r for r in changed if r not in HOLD]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


old, new = [], []
for r in SHIP:
    sub = info[r]['sub']
    d = os.path.join(S, 'sw_dryrun', r); g = os.path.join(S, 'regen', 'b17v2', sub)
    new += [(os.path.join(d, f'{r}_MASTER.SLDPRT'), f'11_MASTERS/{r}_MASTER.SLDPRT', 'copy'),
            (os.path.join(d, f'Build_{r}_report.txt'), f'03_SCRIPTS/Build_{r}_report.txt', 'copy'),
            (os.path.join(g, f'Build_{r}_MASTER.bas'), f'03_SCRIPTS/Build_{r}_MASTER.bas', 'lf'),
            (os.path.join(g, f'DesignTable_{r}_SW2.xlsx'), f'04_DESIGN_TABLES/DesignTable_{r}_SW2.xlsx', 'copy')]
for f in sorted(os.listdir(DT)):
    if f.startswith('DesignTable_') and f.endswith('.xlsx') and '_SW2' not in f:
        live = os.path.join(R, '04_DESIGN_TABLES', f)
        if not os.path.exists(live) or not filecmp.cmp(os.path.join(DT, f), live, shallow=False):
            new.append((os.path.join(DT, f), f'04_DESIGN_TABLES/{f}', 'copy'))
for dp, dn, fn in os.walk(TN):
    dn[:] = [x for x in dn if x not in ('__pycache__', '_out') and not (os.path.basename(dp) == 'coverage' and x == 'work')]
    for f in fn:
        if f.endswith('.orig') or f.endswith('.pyc'):
            continue
        src = os.path.join(dp, f); rel = 'tools/' + os.path.relpath(src, TN).replace('\\', '/')
        live = os.path.join(R, rel)
        if not os.path.exists(live) or not filecmp.cmp(src, live, shallow=False):
            new.append((src, rel, 'copy'))
for s, d, how in new:
    assert os.path.isfile(s), s
    if os.path.exists(os.path.join(R, d)):
        old.append(d)
print(f'ship {len(SHIP)} roots, hold {len(HOLD)}; {len(old)} old files to supersede, {len(new)} new files to place; GO={GO}')
if not GO:
    print('SHIP', ' '.join(SHIP)); print('HOLD', HOLD)
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
        'Batch 17 (2026-10-19): files replaced by the ship (sha256  path relative to OMi_Handoff). Second copy: '
        + ('_to_delete/superseded_20261019b/batch17_replaced/' if base == OF else 'tools/_out/batch17_20261019/old_files/') + '\n'
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
open(os.path.join(S, 'checks', 'shipped_files_sha256.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
print('done:', len(man), 'old files superseded,', len(log), 'new files placed')
