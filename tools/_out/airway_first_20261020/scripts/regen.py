"""Regenerates the affected roots with the LIVE tools/generators:
  control = live tables (repo 04_DESIGN_TABLES)  -> must reproduce the shipped 03_SCRIPTS macro + 04_DESIGN_TABLES SW2
  stage   = stage/04_DESIGN_TABLES (Air-Way first)
Writes regen/{control,stage}/{straight,tee}/ + stdout, and regen/cmp.txt (per root: configurations, new / lost / changed, cells changed
by column, macro vs shipped).   af_control = tools_af (live tools + 6410 reference 6410-24-20-O) on the live tables -> must equal control except 6410
  stage uses tools_af. Roots: from revert_list.csv (2404_FINAL -> 2404)."""
import os, sys, re, csv, subprocess, collections, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
GEN = os.path.join(H, 'tools', 'generators')
GEN_AF = os.path.join(A, 'tools_af', 'generators')
OUT = os.path.join(A, 'regen')
def roots(g):
    code = open(os.path.join(GEN, g), encoding='utf-8').read()
    m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    keys = re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M) if m else []
    keys += re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)
    return set(keys)
want = sorted({r['root'].replace('_FINAL', '') for f in ('revert_list.csv', 'brennan_cells.csv') for r in csv.DictReader(open(os.path.join(A, f)))})
gs, gt = roots('gen_straight2.py'), roots('gen_tee.py')
def run(sub, root_dir, g, r, gen=GEN):
    o = os.path.join(OUT, sub); os.makedirs(o, exist_ok=True)
    env = dict(os.environ, OMI_ROOT=root_dir, GS_OUT=os.path.join(o, 'straight'), GT_OUT=os.path.join(o, 'tee'))
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(gen, g), r], env=env, capture_output=True, text=True)
    open(os.path.join(o, f'{r}_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode
def load(p):
    if not os.path.exists(p): return None
    rows = list(openpyxl.load_workbook(p, data_only=True).active.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
    if hi is None: return {}
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None} for r in rows[hi + 1:] if r and r[0]}
def txt(p):
    if not os.path.exists(p): return None
    s = open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    return re.sub(r"(?m)^.*(Generated|generated) .*\d{4}-\d{2}-\d{2}.*$", '', s)
lines = []
for r in want:
    g, sub = ('gen_tee.py', 'tee') if r in gt else ('gen_straight2.py', 'straight') if r in gs else (None, None)
    if g is None:
        lines.append(f'{r:8s} NO GENERATOR SPEC (hand-made table) - not regenerated'); print(lines[-1]); continue
    rc_c = run('control', H, g, r); rc_s = run('stage', os.path.join(A, 'stage'), g, r, GEN_AF); rc_a = run('af_control', H, g, r, GEN_AF)
    c = load(os.path.join(OUT, 'control', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
    s = load(os.path.join(OUT, 'stage', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
    shipped = load(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')) or {}
    m_c = txt(os.path.join(OUT, 'control', sub, f'Build_{r}_MASTER.bas')); m_ship = txt(os.path.join(H, '03_SCRIPTS', f'Build_{r}_MASTER.bas'))
    m_s = txt(os.path.join(OUT, 'stage', sub, f'Build_{r}_MASTER.bas'))
    af_same = (load(os.path.join(OUT, 'af_control', sub, f'DesignTable_{r}_SW2.xlsx')) == c) and txt(os.path.join(OUT, 'af_control', sub, f'Build_{r}_MASTER.bas')) == m_c
    new = sorted(set(s) - set(c)); lost = sorted(set(c) - set(s))
    chg = collections.Counter(); cfgs = set()
    for k in set(c) & set(s):
        for col in set(c[k]) | set(s[k]):
            if c[k].get(col) != s[k].get(col):
                chg[col] += 1; cfgs.add(k)
    lines.append(f'{r:8s} [{sub}] rc {rc_c}/{rc_s}/{rc_a} af_control=control: {af_same} | control {len(c):3d} (=shipped SW2: {c == shipped}, macro=shipped: {m_c == m_ship}) '
                 f'stage {len(s):3d} | macro changed: {m_c != m_s} | configs changed {len(cfgs)} | new {new} | LOST {lost} | cells {dict(chg)}')
    print(lines[-1], flush=True)
open(os.path.join(OUT, 'cmp.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
