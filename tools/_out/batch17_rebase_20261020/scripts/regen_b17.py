"""Batch 17 rebase (2026-10-20, cloud): regenerate EVERY root twice.
  live : live tools/ on the live repo tables (= batch 16 as shipped)        -> regen/live/{straight,tee}
  b17  : genfeat_20261018/merged/tools on batch17_rebase_20261020/root       -> regen/b17/{straight,tee}
         (root = live 04_DESIGN_TABLES overlaid with the batch-17 stage review tables; the stage's own SW2 copies are NOT used)
Roots = SPEC keys of the merged generators (dict entries + SPEC['x'] = ... lines). One process per root, run in parallel.
Usage: python -I regen_b17.py <repo root>"""
import os, sys, re, json, subprocess
from concurrent.futures import ThreadPoolExecutor
REPO = os.path.abspath(sys.argv[1])
HERE = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')
SETS = {'live': (os.path.join(REPO, 'tools/generators'), REPO),
        'b17': (os.path.join(REPO, 'tools/_out/genfeat_20261018/merged/tools/generators'), os.path.join(HERE, 'root'))}


def roots(gen_dir, g):
    code = open(os.path.join(gen_dir, g), encoding='utf-8').read()
    m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    keys = re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M) if m else []
    keys += re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)
    return sorted(set(keys))


jobs = []
for tag, (gd, rd) in SETS.items():
    for g, sub, var in (('gen_straight2.py', 'straight', 'GS_OUT'), ('gen_tee.py', 'tee', 'GT_OUT')):
        for r in sorted(set(roots(SETS['b17'][0], g)) | set(roots(SETS['live'][0], g))):
            jobs.append((tag, gd, rd, g, sub, var, r))


def run(j):
    tag, gd, rd, g, sub, var, r = j
    out = os.path.join(HERE, 'regen', tag, sub); os.makedirs(out, exist_ok=True)
    env = dict(os.environ, OMI_ROOT=rd, **{var: out})
    p = subprocess.run([sys.executable, '-I', os.path.join(gd, g), r], env=env, capture_output=True, text=True)
    err = p.stderr.strip().splitlines()[-1] if p.returncode and p.stderr.strip() else ''
    return f'{tag} {sub} {r} rc {p.returncode} {err}'


with ThreadPoolExecutor(os.cpu_count() or 4) as ex:
    log = list(ex.map(run, jobs))
open(os.path.join(HERE, 'regen', 'regen_log.txt'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(l for l in log if ' rc 0 ' not in l + ' '))
print(len(jobs), 'jobs')
