"""regen_b17v2.py: as regen_b17.py, with tools_b17 (= merged tools + Atan2V ByVal fix, 2026-10-19) into regen/b17v2 (control not re-run).

  root/04_DESIGN_TABLES = copy of the live 04_DESIGN_TABLES + the batch-17 review tables from brennan_yes_20261018/stage
                          (checked first: stage = live + logged batch-17 edits, 0 stale cells - checks/cmp3_full.txt)
  control = LIVE tools/generators on the LIVE repo (must reproduce 03_SCRIPTS / 04_DESIGN_TABLES for shipped roots)
  b17     = MERGED tools (genfeat_20261018/merged/tools = live tools + 5 features) on root/
Writes regen/{control,b17}/{straight,tee}/ and regen/cmp.txt."""
import os, sys, re, shutil, subprocess, openpyxl

H = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
B17 = os.path.join(H, r'tools\_out\batch17_20261019')
LIVE_GEN = os.path.join(H, r'tools\generators')
MERGED_GEN = os.path.join(H, r'tools\_out\batch17_20261019\tools_b17\generators')
STAGE_DT = os.path.join(H, r'tools\_out\brennan_yes_20261018\stage\04_DESIGN_TABLES')
ROOT = os.path.join(B17, 'root')
OUT = os.path.join(B17, 'regen')


def make_root():
    dt = os.path.join(ROOT, '04_DESIGN_TABLES')
    if os.path.exists(dt):
        return
    shutil.copytree(os.path.join(H, '04_DESIGN_TABLES'), dt)
    n = 0
    for f in os.listdir(STAGE_DT):
        if f.startswith('DesignTable_') and f.endswith('.xlsx') and '_SW2' not in f:
            shutil.copy2(os.path.join(STAGE_DT, f), os.path.join(dt, f)); n += 1
    print('root built: live tables +', n, 'staged review tables')


def roots(gen_dir, g):
    code = open(os.path.join(gen_dir, g), encoding='utf-8').read()
    m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    keys = re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M) if m else []
    keys += re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)
    return sorted(set(keys))


def run(gen_dir, root_dir, sub, g, r):
    env = dict(os.environ, OMI_ROOT=root_dir, GS_OUT=os.path.join(OUT, sub, 'straight'), GT_OUT=os.path.join(OUT, sub, 'tee'))
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(gen_dir, g), r], env=env, capture_output=True, text=True)
    open(os.path.join(OUT, sub, f'{r}_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
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
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None} for r in rows[hi + 1:] if r and r[0]}


make_root()
for s in ('b17v2',):
    os.makedirs(os.path.join(OUT, s), exist_ok=True)
lines = []
for g, sub in (('gen_straight2.py', 'straight'), ('gen_tee.py', 'tee')):
    live_roots = roots(LIVE_GEN, g)
    for r in roots(MERGED_GEN, g):
        rc_c = None
        rc_t = run(MERGED_GEN, ROOT, 'b17v2', g, r)
        a = load(os.path.join(OUT, 'b17', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        b = load(os.path.join(OUT, 'b17v2', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        lost = sorted(set(a) - set(b)); new = sorted(set(b) - set(a))
        chg = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        lines.append(f'{r:8s} [{sub}] rc {rc_c}/{rc_t}  control {len(a):3d} b17 {len(b):3d}  new {len(new):3d} {new}  lost {lost}  changed {chg}')
        print(lines[-1], flush=True)
open(os.path.join(OUT, 'cmp_v2.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
