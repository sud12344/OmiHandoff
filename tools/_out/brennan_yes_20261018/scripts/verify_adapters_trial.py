"""Regenerate (batch-16 tools) every root whose SW2 the adapters agent produced in test/gen_applied, from adapters_trial, and compare SW2
configuration sets + cells with the agent's. Expected differences: only the pending-OMi cells (2705-06-06, 6405-16-06-O, 6500-08-06-FG,
6505-24-24, 6505-32-32, 5502-16-12-FG) and $PRP texts."""
import os, sys, glob, subprocess, openpyxl

BY = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018'
T = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\puckfix_20261009\tools_new\generators'
AG = os.path.join(BY, r'wave3\adapters\test\gen_applied')
OUT = os.path.join(BY, 'adapters_trial_gen')
EXPECT = {'2705-06-06', '6405-16-06-O', '6500-08-06-FG', '6505-24-24', '6505-32-32', '5502-16-12-FG'}


def load(p):
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3)
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None and not str(h[j]).startswith('$')} for r in rows[hi + 1:] if r and r[0]}


bad = 0
for p in sorted(glob.glob(os.path.join(AG, '**', 'DesignTable_*_SW2.xlsx'), recursive=True)):
    root = os.path.basename(p)[12:-9]
    sub = 'tee' if os.sep + 'tee' + os.sep in p else 'straight'
    env = dict(os.environ, OMI_ROOT=os.path.join(BY, 'adapters_trial'), GS_OUT=os.path.join(OUT, 'straight'), GT_OUT=os.path.join(OUT, 'tee'))
    g = 'gen_tee.py' if sub == 'tee' else 'gen_straight2.py'
    subprocess.run([sys.executable, '-I', os.path.join(T, g), root], env=env, capture_output=True)
    mine = os.path.join(OUT, sub, os.path.basename(p))
    if not os.path.exists(mine):
        print(root, 'NO OUTPUT'); bad += 1; continue
    a, b = load(p), load(mine)
    add, rem = set(b) - set(a), set(a) - set(b)
    chg = [k for k in set(a) & set(b) if a[k] != b[k]]
    unexpected = [k for k in chg if k not in EXPECT]
    print(f'{root:8s} agent {len(a):3d} mine {len(b):3d}  added {sorted(add)} removed {sorted(rem)} changed {sorted(chg)}' + ('  <-- UNEXPECTED' if add or rem or unexpected else ''))
    bad += bool(add or rem or unexpected)
print('UNEXPECTED DIFFERENCES:', bad)
