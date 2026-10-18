"""regen_compare.py <tag>: control = base batch-16 tools on the stage; test = MERGED tools on genfeat_trial. Every root of both generators
(SPEC keys of the merged tools). Writes <BY>/regen_<tag>/{control,test}/... and cmp.txt; prints totals."""
import os, sys, re, glob, json, subprocess, openpyxl

BY = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018'
BASE = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\puckfix_20261009\tools_new\generators'
MERGED = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\genfeat_20261018\merged\tools\generators'
tag = sys.argv[1]
OUT = os.path.join(BY, f'regen_{tag}')


def roots(gen_dir, g):
    code = open(os.path.join(gen_dir, g), encoding='utf-8').read()
    m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    keys = re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M) if m else []
    keys += re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)       # SPECs added after the dict (6400, 1700RC, 1800, ...)
    return sorted(set(keys))


def run(gen_dir, root_dir, sub, g, r):
    env = dict(os.environ, OMI_ROOT=root_dir, GS_OUT=os.path.join(OUT, sub, 'straight'), GT_OUT=os.path.join(OUT, sub, 'tee'))
    p = subprocess.run([sys.executable, '-I', os.path.join(gen_dir, g), r], env=env, capture_output=True, text=True)
    return p.returncode


def load(p):
    if not os.path.exists(p):
        return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
    if hi is None:
        return {}
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None and not str(h[j]).startswith('$')} for r in rows[hi + 1:] if r and r[0]}


lines, tot_c, tot_t, changed_old = [], 0, 0, 0
for g, sub in (('gen_straight2.py', 'straight'), ('gen_tee.py', 'tee')):
    for r in roots(MERGED, g):
        rc_c = run(BASE, os.path.join(BY, 'stage'), 'control', g, r) if r in roots(BASE, g) else None
        rc_t = run(MERGED, os.path.join(BY, 'genfeat_trial'), 'test', g, r)
        a = load(os.path.join(OUT, 'control', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        b = load(os.path.join(OUT, 'test', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        lost = sorted(set(a) - set(b)); new = sorted(set(b) - set(a))
        chg = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        tot_c += len(a); tot_t += len(b); changed_old += len(chg) + len(lost)
        lines.append(f'{r:8s} [{sub}] rc {rc_c}/{rc_t}  control {len(a):3d} test {len(b):3d}  new {len(new):3d}  lost {lost}  changed {chg}')
open(os.path.join(OUT, 'cmp.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(l for l in lines if ' new   0  lost []  changed []' not in l))
print(f'TOTAL configurations: control {tot_c}  test {tot_t}  (+{tot_t - tot_c}); old configurations changed or lost: {changed_old}')
