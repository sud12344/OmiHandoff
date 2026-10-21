"""summary.py (group B): per series of the group B list - OMi BUILD rows, configurations generated (by master), rows not generated with the reason.
Writes checks/series_summary.txt."""
import os, sys, re, subprocess, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
CODE = r'''
import sys, os, json
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, os.path.dirname(sys.argv[1]))
gen = sys.argv[2]; roots = sys.argv[3:]
import importlib; m = importlib.import_module(gen)
out = {}
for r in roots:
    b, s = m.build_rows(r)
    if gen == 'gen_tee': ok = [x['pn'] for x in b if not x['chk']]; bl = [(x['pn'], '; '.join(x['chk'])) for x in b if x['chk']]
    elif gen == 'gen_ring': ok = [x[0]['$PRP@PartNo'] for x in b if not x[1]]; bl = [(x[0]['$PRP@PartNo'], '; '.join(x[1])) for x in b if x[1]]
    else: ok = [x[0]['$PRP@PartNo'] for x in b if not x[7]]; bl = [(x[0]['$PRP@PartNo'], '; '.join(x[7])) for x in b if x[7]]
    out[r] = dict(ok=ok, blocked=bl, skipped=[list(map(str, x)) if not isinstance(x, str) else [x] for x in s])
print(json.dumps(out))
'''
J = lambda *a: os.path.join(ROOT, *a)
AF = dict(OMI_ROOT=os.path.join(A, 'stage'))
FS = dict(OMI_ROOT=ROOT, OMI_REV_EXTRA=os.pathsep.join([os.path.join(A, 'stage', 'orfs_tables'), os.path.join(A, 'stage', '04_DESIGN_TABLES')]),
          GR_REV=J('tools', '_out', 'newtypes_20261014', 'review_tables'))
JOBS = [('tools_af', 'gen_straight2', ['6900'], AF), ('tools_af', 'gen_tee', ['6901', '6805', '6806', '6809', '6815', '6832', '6835', '6801'], AF),
        ('tools_fs', 'gen_straight2', ['FS2408', 'FS6402', 'FS2403', 'FS2404', 'FS6400', 'FS6403'], FS),
        ('tools_fs', 'gen_tee', ['FS6809', 'FS6809C', 'FS6809R', 'FS6809RC', 'FS6801', 'FS6801R', 'FS6801N', 'FS6801NR', 'FS6802R', 'FS6802NR', 'FS6803NR', 'FS6804R', 'FS6804NR'], FS),
        ('tools_fs', 'gen_ring', ['4000'], FS)]
res = {}
for t, g, roots, env in JOBS:
    p = subprocess.run([sys.executable, '-I', '-B', '-c', CODE, os.path.join(A, t, 'generators'), g] + roots, capture_output=True, text=True,
                       env=dict(os.environ, GS_OUT=os.path.join(A, 'scratch', 'sum'), GT_OUT=os.path.join(A, 'scratch', 'sum'), GR_OUT=os.path.join(A, 'scratch', 'sum'), **env))
    if p.returncode: print(p.stderr[-2000:]); raise SystemExit(1)
    res.update(json.loads(p.stdout.strip().splitlines()[-1]))
SERIES = ['6900', '6901', '6805', '6806', '6809', '6815', '6832', '6835', '6801-L', '6801-LL', '4005', 'FS2408', 'FS6402', 'FS6809', 'FS6801-L']
lines = []
for s in SERIES:
    ok = sorted({p for r in res.values() for p in r['ok'] if re.match(re.escape(s) + r'-\d', p)})
    bl = sorted({tuple(x) for r in res.values() for x in r['blocked'] if re.match(re.escape(s) + r'-\d', x[0])})
    sk = [x for r in res.values() for x in r['skipped'] if re.match(re.escape(s) + r'-\d', x[0]) and 'DROP' not in x[1:2]]
    sk = {x[0]: x for x in sk if x[0] not in ok}
    lines.append(f'{s}: {len(ok)} configurations - {" ".join(ok)}')
    for p, why in bl: lines.append(f'   BLOCKED {p}: {why[:300]}')
    for p, x in sorted(sk.items()): lines.append(f'   not generated {p}: {" / ".join(x[1:])[:300]}')
other = sorted({p for r in res.values() for p in r['ok'] if not any(re.match(re.escape(s) + r'-\d', p) for s in SERIES)} - {p for p in res.get('6801', {}).get('ok', []) if not p.startswith('6801-L')} - {p for p in res.get('4000', {}).get('ok', []) if not p.startswith('4005')})
lines.append(f'\nother configurations in the regenerated masters (existing FS / 6801 roots, incl. the configurations the old toolset already had; new ones: regen/cmp.txt): {len(other)}')
lines.append('   ' + ' '.join(other))
open(os.path.join(A, 'checks', 'series_summary.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
