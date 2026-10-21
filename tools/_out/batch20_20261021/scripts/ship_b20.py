"""Batch 20 ship (2026-10-21, user: "SolidWorks is free now - run the 5404N dry run and ship batch 20 if it passes."). python ship_b20.py [go]
5404N: the -06 thread fix (QA #178: helix 0.005 short of the round-bar shoulder) + the 4 long nipples (A4). Dry run dryrun/5404N: 26
configurations rebuilt with the threads live, 0 failures, 1 body each; the 4 shipped configurations identical (dV 0); the one FAIL line is the
reference-configuration body-diameter extent check reading the loose part box around the live helix (exact size 0.88 = table; accepted as for
5406HHP / 5406SHP in batch 17). Same move-and-copy scheme as batch 19 (old -> _to_delete/superseded_20261021b/batch20_replaced + old_files)."""
import hashlib, os, shutil, sys
R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
S = os.path.join(R, r'tools\_out\batch20_20261021')
TD = os.path.join(R, '_to_delete', 'superseded_20261021b', 'batch20_replaced')
OF = os.path.join(S, 'old_files')
GO = len(sys.argv) > 1 and sys.argv[1] == 'go'
D = os.path.join(S, 'dryrun', '5404N'); G = os.path.join(S, 'regen_all', 'straight')
rep = open(os.path.join(D, 'Build_5404N_report.txt'), encoding='utf-8', errors='replace').read()
fails = [l for l in rep.splitlines() if l.startswith('FAIL')]
assert fails == ['FAIL  Body diameter 0.8861 / 0.8931 (expect 0.8800)'], fails
assert 'All-config sweep: 26 configurations rebuilt, 0 feature/body failures' in rep
new = [(os.path.join(D, '5404N_MASTER.SLDPRT'), '11_MASTERS/5404N_MASTER.SLDPRT', 'copy'),
       (os.path.join(D, 'Build_5404N_report.txt'), '03_SCRIPTS/Build_5404N_report.txt', 'copy'),
       (os.path.join(G, 'Build_5404N_MASTER.bas'), '03_SCRIPTS/Build_5404N_MASTER.bas', 'lf'),
       (os.path.join(G, 'DesignTable_5404N_SW2.xlsx'), '04_DESIGN_TABLES/DesignTable_5404N_SW2.xlsx', 'copy'),
       (os.path.join(S, 'root20', '04_DESIGN_TABLES', 'DesignTable_5404N.xlsx'), '04_DESIGN_TABLES/DesignTable_5404N.xlsx', 'copy'),
       (os.path.join(S, 'tools_b20', 'generators', 'gen_straight2.py'), 'tools/generators/gen_straight2.py', 'copy')]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


old = [d for s, d, h in new if os.path.exists(os.path.join(R, d))]
print(f'{len(old)} old files, {len(new)} new files; GO={GO}')
if not GO:
    for s, d, h in new: print(f'  {h:4} {os.path.relpath(s, R)} -> {d}')
    sys.exit()
man = []
for p in old:
    src = os.path.join(R, p); h = sha(src)
    for base in (OF, TD): os.makedirs(os.path.dirname(os.path.join(base, p)), exist_ok=True)
    assert not os.path.exists(os.path.join(TD, p)), p
    shutil.copy2(src, os.path.join(OF, p)); shutil.move(src, os.path.join(TD, p))
    assert sha(os.path.join(OF, p)) == h and sha(os.path.join(TD, p)) == h
    man.append(f'{h}  {p}')
for base in (OF, TD):
    open(os.path.join(base, 'MANIFEST.txt'), 'w', encoding='utf-8').write('Batch 20 (2026-10-21): files replaced by the ship (sha256  path)\n' + '\n'.join(man) + '\n')
log = []
for s, d, how in new:
    dst = os.path.join(R, d); assert not os.path.exists(dst), d
    if how == 'copy':
        shutil.copy2(s, dst); assert sha(dst) == sha(s)
    else:
        open(dst, 'wb').write(open(s, 'rb').read().replace(b'\r\n', b'\n'))
    log.append(f'{sha(dst)}  {d}   <- {how} {os.path.relpath(s, R)}')
os.makedirs(os.path.join(S, 'checks'), exist_ok=True)
open(os.path.join(S, 'checks', 'shipped_files_sha256.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
print('done:', len(man), 'old,', len(log), 'new')
