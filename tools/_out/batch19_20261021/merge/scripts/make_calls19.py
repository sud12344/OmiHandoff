"""make_calls19.py: SolidWorks dry-run call files for the batch-19 ship roots (ship_roots.json), 3 groups -> dryrun/calls_g1..g3.json.
Per root: run_macro (regen/<kind> macro + SW2 via TABLE_PATH, SAVE / REPORT -> dryrun/<root>/) -> sweep_configs -> close; then the shipped
master (11_MASTERS; for 2500 / 2502 / 2603 the hand-built 2500HX / 2502HX / 2603HX) opened read-only -> sweep_configs -> close."""
import json, os
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
M = os.path.join(H, 'tools', '_out', 'batch19_20261021', 'merge')
ship = json.load(open(os.path.join(M, 'ship_roots.json')))
OLDNAME = {'2500': '2500HX', '2502': '2502HX', '2603': '2603HX'}
roots = sorted(ship)
groups = [roots[i::3] for i in range(3)]
for gi, g in enumerate(groups, 1):
    calls = [['sw_status', {}]]
    for r in g:
        src = os.path.join(M, 'regen', ship[r])
        D = os.path.join(M, 'dryrun', r); os.makedirs(D, exist_ok=True)
        calls += [['run_macro', {'path': os.path.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                                 'const_overrides': {'TABLE_PATH': os.path.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                     'SAVE_PATH': os.path.join(D, f'{r}_MASTER.SLDPRT'),
                                                     'REPORT_PATH': os.path.join(D, f'Build_{r}_report.txt')}}],
                  ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
        o = OLDNAME.get(r, r)
        live = os.path.join(H, '11_MASTERS', f'{o}_MASTER.SLDPRT')
        if os.path.exists(live):
            calls += [['open_doc', {'path': live, 'read_only': True}], ['sweep_configs', {'doc': f'{o}_MASTER', 'timeout_s': 1700}],
                      ['close_doc', {'doc': f'{o}_MASTER', 'discard_unsaved': True}]]
    json.dump(calls, open(os.path.join(M, 'dryrun', f'calls_g{gi}.json'), 'w'), indent=1)
    print(f'g{gi}: {" ".join(g)}')
