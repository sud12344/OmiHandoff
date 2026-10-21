"""survey.py (2026-10-21): the per-size face-seal end libraries from the 18 Brennan STEPs received 2026-10-21 (FS2403-NN-NN, FS2701-NN-NN-FG,
FS6801-NN-NN-NWO-FG), read with the validated pilot extractors (tools/_out/orfs_wp2_20261020/measure/fsmeasure.py) in the same orientation
calls as the -08 pilots (validate_pilots.py). The -08 pilots are re-read first: they must reproduce the generator's FSM_MEAS[8] /
FSBH_MEAS[8] / NWO_FS[8]. -> ../survey.json, ../survey.txt. Read-only."""
import os, sys, json, traceback
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure'), os.path.join(ROOT, 'tools', 'measure')]
import fsmeasure as M, prof
STEP = lambda pn: os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp')
calls = []
for d in ('08', '04', '06', '10', '12', '16', '20'):
    calls += [(f'FSM FS2403-{d}-{d} +X', lambda d=d: M.measure_fsm(STEP(f'FS2403-{d}-{d}'), 0, 1)),
              (f'FSM FS2403-{d}-{d} -X', lambda d=d: M.measure_fsm(STEP(f'FS2403-{d}-{d}'), 0, -1))]
for d in ('08', '04', '06', '10', '12', '16'):
    pn = f'FS2701-{d}-{d}-FG'
    calls += [(f'FSBH {pn}', lambda pn=pn: M.measure_fsm(STEP(pn), 1, 1, ((0, -1),), bulkhead=True))]
for d in ('08', '04', '06', '10', '12', '16', '20', '24'):
    pn = f'FS6801-{d}-{d}-NWO-FG'
    calls += [(f'STUD {pn}', lambda pn=pn: M.measure_stud(STEP(pn), 1, 1, ((0, -1),))),
              (f'STUDPROF {pn}', lambda pn=pn: dict(PROFILE=[(round(s['a1'], 4), round(s['r1'], 4), round(s['a2'], 4), round(s['r2'], 4))
                                                         for s in M.half(STEP(pn), 1, 1, 2, ((0, -1),))[0]] if hasattr(M, 'half') else None))]
out = {}; lines = []
for name, f in calls:
    prof._cache.clear()
    try:
        out[name] = f()
    except Exception as ex:
        out[name] = dict(ERROR=repr(ex), TB=traceback.format_exc().splitlines()[-3:])
    lines.append(f'{name}: ' + json.dumps({k: v for k, v in out[name].items() if k not in ('EDGES', 'CHAIN', 'PROFILE', 'BH_STEPS')}, default=str)[:900])
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(out, open(os.path.join(here, 'survey.json'), 'w'), indent=1, default=str)
open(os.path.join(here, 'survey.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
