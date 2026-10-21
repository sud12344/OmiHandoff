"""static19.py: the batch-19 ship roots (regen_cmp.json: NEW, or CHANGED with new configurations; minus the held / pre-2026-09-25 'old' roots)
-> ship_roots.json; dofcheck_straight / dofcheck_tee / allcfg_check (OMI_ROOT = root19) / vbacheck with tools_b19 -> merge/checks/."""
import os, sys, json, subprocess
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
M = os.path.join(H, 'tools', '_out', 'batch19_20261021', 'merge')
T = os.path.join(M, 'tools_b19'); C = os.path.join(M, 'checks'); os.makedirs(C, exist_ok=True)
res = json.load(open(os.path.join(M, 'regen_cmp.json')))
HOLD = {'5404N'}
ship = {r: v['kind'] for r, v in res.items() if r not in HOLD and (v['status'] == 'NEW' or (v['status'] == 'CHANGED' and (v['new'] or v['lost'] or v['changed'])))}
json.dump(ship, open(os.path.join(M, 'ship_roots.json'), 'w'), indent=1)
print(len(ship), 'ship roots:', ' '.join(sorted(ship)))
env = dict(os.environ, OMI_ROOT=os.path.join(M, 'root19'), GS_OUT=os.path.join(M, 'scratch'), GT_OUT=os.path.join(M, 'scratch'))
mac = lambda r, k: os.path.join(M, 'regen', k, f'Build_{r}_MASTER.bas')
S = sorted(r for r, k in ship.items() if k == 'straight'); Tt = sorted(r for r, k in ship.items() if k == 'tee')
runs = [('dofcheck_straight', [os.path.join(T, 'checks', 'dofcheck_straight.py')] + [mac(r, 'straight') for r in S]),
        ('dofcheck_tee', [os.path.join(T, 'checks', 'dofcheck_tee.py')] + [mac(r, 'tee') for r in Tt]),
        ('allcfg_straight', [os.path.join(T, 'checks', 'allcfg_check.py'), 's'] + S),
        ('allcfg_tee', [os.path.join(T, 'checks', 'allcfg_check.py'), 't'] + Tt),
        ('vbacheck', [os.path.join(T, 'checks', 'vbacheck.py')] + [mac(r, k) for r, k in sorted(ship.items())])]
for name, cmd in runs:
    p = subprocess.run([sys.executable, '-I'] + cmd, env=env, capture_output=True, text=True)
    open(os.path.join(C, name + '.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    print(f'== {name} rc {p.returncode}, {len(p.stdout.splitlines())} lines')
