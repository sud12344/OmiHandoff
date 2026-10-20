"""Batch 16 ship (2026-10-19, user: "Yes, ship batch 16 as planned."). python ship_b16.py [go]   (without 'go' = plan only)

Plan and evidence: ../SHIP_PLAN.md. Per shipped root the OLD live files (11_MASTERS part, 03_SCRIPTS macro + report, 04 SW2, the
review tables listed in REVIEW) are MOVED to _to_delete/superseded_20261019/batch16_replaced/<folder>/ AND copied to
tools/_out/ship_20261019/old_files/<folder>/ (MANIFEST.txt in both); the same for every live tools/ file the deploy replaces.
New files are COPIED from the staging folders (which stay as they are - protected evidence):
  part + report   the SolidWorks dry run of the root (DRY below) -> 11_MASTERS / 03_SCRIPTS
  macro + SW2     the macro + SW2 that built that part -> 03_SCRIPTS (CRLF -> LF) / 04_DESIGN_TABLES
                  (5405: its live macro + SW2 built the part - they stay, only part + report change)
  review tables   wave1_ship_20261009/scratch_root/04_DESIGN_TABLES -> 04_DESIGN_TABLES
  toolchain       puckfix_20261009/tools_new -> tools/ (changed + new files; not __pycache__, _out, *.orig)
"""
import filecmp, hashlib, os, shutil, sys

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
O = os.path.join(R, 'tools', '_out')
S = os.path.join(O, 'ship_20261019')
TD = os.path.join(R, '_to_delete', 'superseded_20261019', 'batch16_replaced')
OF = os.path.join(S, 'old_files')
GO = len(sys.argv) > 1 and sys.argv[1] == 'go'

PUCK = os.path.join(O, 'puckfix_20261009')
W1 = os.path.join(O, 'wave1_ship_20261009')
SCR = os.path.join(W1, 'scratch_root', '04_DESIGN_TABLES')
TN = os.path.join(PUCK, 'tools_new')
# root -> (folder with part + report, folder with macro + SW2 that built it)
DRY = {r: (os.path.join(PUCK, 'sw_dryrun', r), os.path.join(PUCK, 'regen', 'new'))
       for r in '2504 2505 1502 6500 6501 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802'.split()}
DRY.update({'0304': (os.path.join(W1, 'swtest', '0304'), os.path.join(W1, 'regen', 'after', 'straight')),
            '0306': (os.path.join(W1, 'swtest', '0306'), os.path.join(W1, 'regen', 'after', 'straight')),
            '2606': (os.path.join(W1, 'swtest', '2606'), os.path.join(W1, 'regen', 'jictees')),
            '2609': (os.path.join(W1, 'swtest', '2609'), os.path.join(W1, 'regen', 'jictees')),
            '2611': (os.path.join(W1, 'swtest', '2611'), os.path.join(W1, 'regen', 'jictees')),
            '6505': (os.path.join(W1, 'swtest', '6505'), os.path.join(W1, 'regen', 'leftovers', 'straight')),
            '2404': (os.path.join(O, 'r2404_20261009', 'swtest'), os.path.join(O, 'r2404_20261009', 'regen', 'after')),
            '5405': (os.path.join(W1, 'swtest', '5405'), None)})
REVIEW = {'0304': ['0304'], '0306': ['0306'], '1502': ['1502'], '2504': ['2504'], '2505': ['2505'], '2606': ['2606'],
          '2609': ['2609'], '2611': ['2611'], '6500': ['6500', '6500L'], '6501': ['6501'], '6505': ['6505']}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


old, new = [], []   # old: repo-relative paths; new: (abs source, repo-relative target, how)
for r, (pdir, mdir) in DRY.items():
    new += [(os.path.join(pdir, f'{r}_MASTER.SLDPRT'), f'11_MASTERS/{r}_MASTER.SLDPRT', 'copy'),
            (os.path.join(pdir, f'Build_{r}_report.txt'), f'03_SCRIPTS/Build_{r}_report.txt', 'copy')]
    if mdir:
        new += [(os.path.join(mdir, f'Build_{r}_MASTER.bas'), f'03_SCRIPTS/Build_{r}_MASTER.bas', 'lf'),
                (os.path.join(mdir, f'DesignTable_{r}_SW2.xlsx'), f'04_DESIGN_TABLES/DesignTable_{r}_SW2.xlsx', 'copy')]
    new += [(os.path.join(SCR, f'DesignTable_{t}.xlsx'), f'04_DESIGN_TABLES/DesignTable_{t}.xlsx', 'copy') for t in REVIEW.get(r, [])]
for dp, dn, fn in os.walk(TN):
    dn[:] = [d for d in dn if d not in ('__pycache__', '_out')]
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
print(f'{len(old)} old files to supersede, {len(new)} new files to place; GO={GO}')
if not GO:
    for p in old:
        print('  old', p)
    for s, d, how in new:
        print(f'  {how:4} {os.path.relpath(s, R)} -> {d}')
    sys.exit()

# 1. old files: copy to old_files, move to _to_delete (sha256 checked)
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
        'Batch 16 (2026-10-19): files replaced by the ship (sha256  path relative to OMi_Handoff). Second copy: '
        + ('_to_delete/superseded_20261019/batch16_replaced/' if base == OF else 'tools/_out/ship_20261019/old_files/') + '\n'
        + '\n'.join(man) + '\n')

# 2. new files (copies; the staging folders keep theirs)
log = []
for s, d, how in new:
    dst = os.path.join(R, d)
    assert not os.path.exists(dst), 'target exists: ' + d
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    h = sha(s)
    if how == 'copy':
        shutil.copy2(s, dst)
        assert sha(dst) == h
    else:   # 'lf': CRLF -> LF, nothing else (the shipped macros are LF)
        b = open(s, 'rb').read()
        open(dst, 'wb').write(b.replace(b'\r\n', b'\n'))
        assert open(dst, 'rb').read() == b.replace(b'\r\n', b'\n')
    log.append(f'{sha(dst)}  {d}   <- {how} {os.path.relpath(s, R)} (source sha256 {h})')
os.makedirs(os.path.join(S, 'checks'), exist_ok=True)
open(os.path.join(S, 'checks', 'shipped_files_sha256.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
print('done:', len(man), 'old files superseded,', len(log), 'new files placed')
