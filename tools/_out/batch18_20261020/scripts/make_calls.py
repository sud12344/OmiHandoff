"""make_calls.py <name> <srcdir> <root> [<root> ...]: SolidWorks dry-run call file dryrun/calls_<name>.json - each root's macro + SW2 from
<srcdir> (relative to this batch folder) built into dryrun/<root>/, swept, closed; a shipped master in 11_MASTERS is swept read-only too."""
import json, os, sys
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
B = os.path.join(H, 'tools', '_out', 'batch18_20261020')
name, src, roots = sys.argv[1], os.path.join(B, sys.argv[2]), sys.argv[3:]
calls = [['sw_status', {}]]
for r in roots:
    D = os.path.join(B, 'dryrun', r); os.makedirs(D, exist_ok=True)
    calls += [['run_macro', {'path': os.path.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                             'const_overrides': {'TABLE_PATH': os.path.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                 'SAVE_PATH': os.path.join(D, f'{r}_MASTER.SLDPRT'),
                                                 'REPORT_PATH': os.path.join(D, f'Build_{r}_report.txt')}}],
              ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
              ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    live = os.path.join(H, '11_MASTERS', f'{r}_MASTER.SLDPRT')
    if os.path.exists(live):
        calls += [['open_doc', {'path': live, 'read_only': True}], ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
json.dump(calls, open(os.path.join(B, 'dryrun', f'calls_{name}.json'), 'w'), indent=1)
print(name, len(calls), 'calls')
