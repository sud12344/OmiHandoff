"""loose_survey.py (2026-10-20): read the per-size Brennan FS0306 / FS0318 / FS0319 STEPs with the validated pilot extractors
(tools/_out/orfs_wp2_20261020/measure/fsmeasure.py measure_nut / measure_sleeve) -> loose_survey.json + .txt. Read-only."""
import os, sys, json, glob, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure'), os.path.join(ROOT, 'tools', 'measure')]
import fsmeasure as M, prof
from section import load
from model_nutcap import vol, nsolids
out = {}; lines = []
for root in ('FS0306', 'FS0318', 'FS0319'):
    for p in sorted(glob.glob(os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{root}-??.stp'))):
        pn = os.path.basename(p)[8:-4]; prof._cache.clear()
        S = load(p); b = prof.bbox(p)
        o = dict(solids=nsolids(S), volume=round(vol(S), 5), bbox=[round(b[3 + i] - b[i], 4) for i in range(3)])
        try:
            o.update(M.measure_sleeve(p, 0) if root == 'FS0319' else M.measure_nut(p, 0))
        except Exception as ex:
            o['ERROR'] = repr(ex)
        out[pn] = o
        lines.append(f'{pn}: ' + json.dumps({k: v for k, v in o.items() if k not in ('INNER', 'EDGES')}))
        if root == 'FS0319' and 'EDGES' in o: lines += ['    ' + str(e) for e in o['EDGES']]
        if root != 'FS0319' and 'INNER' in o: lines += ['    inner ' + str(e[1:]) for e in o['INNER']]
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(out, open(os.path.join(here, 'loose_survey.json'), 'w'), indent=1, default=str)
open(os.path.join(here, 'loose_survey.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
