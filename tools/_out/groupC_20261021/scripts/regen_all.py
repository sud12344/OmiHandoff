"""regen_all.py (group C, 2026-10-21): regenerate EVERY root with the base toolset (tools/_out/airway_first_20261020/tools_af) and the group C
toolset (tools_c), same tables (OMI_ROOT = the Brennan-CAD stage, the latest stage; tools_c also sees the C tables via OMI_REV_EXTRA), and diff:
every existing root must give the identical macro text and SW2 table content; only the C roots may be new.
Writes regen/{old,new}/{straight,tee}/... and regen/cmp.txt."""
import os, sys, re, subprocess, hashlib, openpyxl, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
OLD = os.path.join(ROOT, 'tools', '_out', 'airway_first_20261020', 'tools_af', 'generators'); NEW = os.path.join(A, 'tools_c', 'generators')
BASE = os.path.join(ROOT, 'tools', '_out', 'brennancad_20261021', 'stage'); CT = os.path.join(A, 'stage', '04_DESIGN_TABLES')
OUT = os.path.join(A, 'regen')


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():m.end() + 200000], re.M)) if m else set()
    return sorted(k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)))


def run(which, gen, g, r):
    o = os.path.join(OUT, which); env = dict(os.environ, OMI_ROOT=BASE, GS_OUT=os.path.join(o, 'straight'), GT_OUT=os.path.join(o, 'tee'))
    env.pop('OMI_REV_EXTRA', None)
    if which == 'new': env['OMI_REV_EXTRA'] = CT
    os.makedirs(os.path.join(o, 'log'), exist_ok=True)
    p = subprocess.run([sys.executable, '-B', os.path.join(gen, g), r], env=env, capture_output=True, text=True, cwd=gen)
    open(os.path.join(o, 'log', f'{r}.txt'), 'w').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode


def sw2(p):
    if not os.path.exists(p): return None
    return [tuple(r) for r in openpyxl.load_workbook(p, read_only=True).worksheets[0].iter_rows(values_only=True)]


def bas(p):
    return open(p).read().replace('\r\n', '\n') if os.path.exists(p) else None


jobs = []
for g, sub in (('gen_straight2.py', 'straight'), ('gen_tee.py', 'tee')):
    o_, n_ = spec(os.path.join(OLD, g)), spec(os.path.join(NEW, g))
    for r in sorted(set(o_) | set(n_)):
        jobs.append((g, sub, r, r in o_, r in n_))
with cf.ThreadPoolExecutor(8) as ex:
    futs = {}
    for g, sub, r, io, inn in jobs:
        if io: futs[ex.submit(run, 'old', OLD, g, r)] = ('old', r)
        if inn: futs[ex.submit(run, 'new', NEW, g, r)] = ('new', r)
    rc = {futs[f]: f.result() for f in cf.as_completed(futs)}
lines = []; same = diff = new = 0
for g, sub, r, io, inn in jobs:
    po = lambda w, f: os.path.join(OUT, w, sub, f)
    bo, bn = bas(po('old', f'Build_{r}_MASTER.bas')), bas(po('new', f'Build_{r}_MASTER.bas'))
    to, tn = sw2(po('old', f'DesignTable_{r}_SW2.xlsx')), sw2(po('new', f'DesignTable_{r}_SW2.xlsx'))
    if not io:
        new += 1; lines.append(f'{r:8} [{sub}] NEW root (group C): rc {rc.get(("new", r))}, {len(tn) - 1 if tn else 0} configurations'); continue
    ok = bo == bn and to == tn and rc.get(('old', r)) == rc.get(('new', r))
    same += ok; diff += not ok
    lines.append(f'{r:8} [{sub}] rc {rc.get(("old", r))}/{rc.get(("new", r))} ' + ('IDENTICAL' if ok else f'DIFFERENT macro {bo == bn} table {to == tn}') +
                 (f' ({len(to) - 1} configurations)' if to else ' (no table: nothing to build)'))
head = f'regen_all: {same} roots identical, {diff} different, {new} new (group C)'
print(head); print('\n'.join(l for l in lines if 'DIFFERENT' in l or 'NEW' in l))
open(os.path.join(OUT, 'cmp.txt'), 'w').write(head + '\n' + '\n'.join(lines) + '\n')
