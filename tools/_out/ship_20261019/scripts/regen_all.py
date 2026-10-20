"""Batch 16 ship check 1 (2026-10-19): regenerate EVERY root from the staged review tables
(wave1_ship_20261009/scratch_root) with the staged toolchain (puckfix_20261009/tools_new) into regen/{straight,tee}, each root
in its own process. Roots = the SPEC keys of both generators + wave1_ship regen/after/roots.json."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.dirname(HERE)
SCR = os.path.join(O, 'wave1_ship_20261009', 'scratch_root')
TN = os.path.join(O, 'puckfix_20261009', 'tools_new', 'generators')
rj = json.load(open(os.path.join(O, 'wave1_ship_20261009', 'regen', 'after', 'roots.json')))


def spec_roots(gen):
    s = open(os.path.join(TN, gen), encoding='utf-8').read()
    i = s.index('SPEC = {'); j = s.index('\n}\n', i)
    return re.findall(r"^\s*'([0-9A-Z]+)': dict\(", s[i:j], re.M)


kinds = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}
log, roots = [], {}
for k, (gen, var) in kinds.items():
    roots[k] = list(dict.fromkeys(spec_roots(gen) + rj[k]))
    out = os.path.join(HERE, 'regen', k); os.makedirs(out, exist_ok=True)
    for r in roots[k]:
        env = dict(os.environ, OMI_ROOT=SCR, **{var: out})
        p = subprocess.run([sys.executable, os.path.join(TN, gen), r], env=env, capture_output=True, text=True)
        log.append(f'{k} {r} rc {p.returncode} {p.stderr.strip().splitlines()[-1] if p.returncode and p.stderr.strip() else ""}')
json.dump(roots, open(os.path.join(HERE, 'regen', 'roots.json'), 'w'), indent=1)
open(os.path.join(HERE, 'regen', 'regen_log.txt'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(l for l in log if ' rc 0 ' not in l + ' '))
print(sum(len(v) for v in roots.values()), 'roots')
