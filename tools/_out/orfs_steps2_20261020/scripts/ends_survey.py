"""ends_survey.py (2026-10-20): the male face-seal end (measure_fsm) and the female face-seal swivel (measure_fssw) of the new per-size Brennan
STEPs, read with the validated pilot extractors (tools/_out/orfs_wp2_20261020/measure/fsmeasure.py), same orientation calls as the -08 pilots
(validate_pilots.py). -> ends_survey.json / .txt. Read-only; a reading that fails is recorded with its error."""
import os, sys, json, traceback
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(ROOT, 'tools', '_out', 'orfs_wp2_20261020', 'measure'), os.path.join(ROOT, 'tools', 'measure')]
import fsmeasure as M, prof
STEP = lambda pn: os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp')
calls = []
for d in ('08', '04', '06', '10', '12', '16', '20'):
    pn = f'FS6500-{d}-{d}-FG'
    calls += [(f'FSM {pn}', lambda pn=pn: M.measure_fsm(STEP(pn), 0, -1, ((1, 1),))),
              (f'FSSW {pn}', lambda pn=pn: M.measure_fssw(STEP(pn), 1, 1, ((0, -1),)))]
calls += [('FSM FS2403-24-24 +X', lambda: M.measure_fsm(STEP('FS2403-24-24'), 0, 1)), ('FSM FS2403-24-24 -X', lambda: M.measure_fsm(STEP('FS2403-24-24'), 0, -1)),
          ('FSM FS6400-32-32-O', lambda: M.measure_fsm(STEP('FS6400-32-32-O'), 0, -1)), ('STUD FS6400-32-32-O', lambda: M.measure_stud(STEP('FS6400-32-32-O'), 0, 1)),
          ('FSM FS2501-08-08-FG', lambda: M.measure_fsm(STEP('FS2501-08-08-FG'), 0, -1, ((1, 1),))),
          ('FSSW FS6565-08-08 -X', lambda: M.measure_fssw(STEP('FS6565-08-08'), 0, -1)), ('FSSW FS6565-08-08 +X', lambda: M.measure_fssw(STEP('FS6565-08-08'), 0, 1))]
out = {}; lines = []
for name, f in calls:
    prof._cache.clear()
    try: out[name] = f()
    except Exception as ex: out[name] = dict(ERROR=repr(ex), TB=traceback.format_exc().splitlines()[-3:])
    lines.append(f'{name}: ' + json.dumps({k: v for k, v in out[name].items() if k not in ('EDGES', 'CHAIN', 'PROFILE')}, default=str))
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(out, open(os.path.join(here, 'ends_survey.json'), 'w'), indent=1, default=str)
open(os.path.join(here, 'ends_survey.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
