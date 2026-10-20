"""Static checks of the staged regeneration (tools_af on stage/): dofcheck, allcfg, vbacheck, regress (stage vs control), and a trace:
every SW2 change belongs to a configuration of revert_list.csv, and the macro of a root changes only in the reference-geometry block
when its reference row was reverted (or the 6410 reference change). Output -> checks/*.txt"""
import os, sys, csv, subprocess, glob, collections, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
T = os.path.join(A, 'tools_af', 'checks'); R = os.path.join(A, 'regen'); C = os.path.join(A, 'checks')
env = dict(os.environ, OMI_ROOT=os.path.join(A, 'stage'), GS_OUT=os.path.join(A, 'scratch'), GT_OUT=os.path.join(A, 'scratch'))
def sh(args, out):
    p = subprocess.run([sys.executable, '-I', '-B'] + args, env=env, capture_output=True, text=True, cwd=H)
    open(os.path.join(C, out), 'w', encoding='utf-8').write(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''))
    return p.stdout
S = sorted(os.path.basename(f)[6:-11] for f in glob.glob(os.path.join(R, 'stage', 'straight', 'Build_*_MASTER.bas')))
Tt = sorted(os.path.basename(f)[6:-11] for f in glob.glob(os.path.join(R, 'stage', 'tee', 'Build_*_MASTER.bas')))
print(sh([os.path.join(T, 'dofcheck_straight.py')] + [os.path.join(R, 'stage', 'straight', f'Build_{r}_MASTER.bas') for r in S], 'dofcheck_straight.txt')[-600:])
print(sh([os.path.join(T, 'dofcheck_tee.py')] + [os.path.join(R, 'stage', 'tee', f'Build_{r}_MASTER.bas') for r in Tt], 'dofcheck_tee.txt')[-600:])
print(sh([os.path.join(T, 'allcfg_check.py'), 's'] + S, 'allcfg_straight.txt'))
print(sh([os.path.join(T, 'allcfg_check.py'), 't'] + Tt, 'allcfg_tee.txt'))
print(sh([os.path.join(T, 'vbacheck.py')] + glob.glob(os.path.join(R, 'stage', '*', 'Build_*_MASTER.bas')), 'vbacheck.txt'))
out = []
for sub, rr in (('straight', S), ('tee', Tt)):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(T, 'regress.py'), os.path.join(R, 'control', sub), os.path.join(R, 'stage', sub)] + rr,
                       env=env, capture_output=True, text=True, cwd=H)
    out.append(p.stdout + p.stderr)
open(os.path.join(C, 'regress.txt'), 'w', encoding='utf-8').write(''.join(out))
# trace
rev = collections.defaultdict(set)
for x in csv.DictReader(open(os.path.join(A, 'revert_list.csv'), encoding='utf-8')):
    rev[x['root'].replace('_FINAL', '').replace('2501L', '2501')].add(x['cfg'])
def load(p):
    rows = list(openpyxl.load_workbook(p, read_only=True).active.iter_rows(values_only=True))
    h = rows[0]; return {r[0]: dict(zip(h, r)) for r in rows[1:] if r[0]}
lines, bad = [], 0
for sub, rr in (('straight', S), ('tee', Tt)):
    for r in rr:
        c = load(os.path.join(R, 'control', sub, f'DesignTable_{r}_SW2.xlsx')); s = load(os.path.join(R, 'stage', sub, f'DesignTable_{r}_SW2.xlsx'))
        chg = {k for k in set(c) | set(s) if c.get(k) != s.get(k)}
        untraced = sorted(chg - rev[r]); quiet = sorted(rev[r] - chg)
        bad += len(untraced)
        lines.append(f'{r:6s} changed configs {len(chg):3d}  in revert list {len(rev[r]):3d}  UNTRACED {untraced}  reverted but SW2 unchanged {quiet}')
open(os.path.join(C, 'trace.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + f'\nUNTRACED total: {bad}\n')
print('\n'.join(lines)); print('UNTRACED total', bad)
