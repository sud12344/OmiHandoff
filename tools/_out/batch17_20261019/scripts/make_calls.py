"""make_calls.py <name> <root> [<root> ...]: SolidWorks dry runs of batch-17 roots (macro + SW2 from regen/b17v2/<sub>) into
sw_dryrun/<root>/ (SAVE_PATH / REPORT_PATH / TABLE_PATH overridden: 11_MASTERS and 03_SCRIPTS untouched), then sweep_configs (every
configuration: rebuild errors, solid bodies, volume, bbox; output in the call.py log), close with discard.
Writes calls_<name>.json for sw_mcp/call.py."""
import json, os, sys

B17 = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\batch17_20261019'
name, roots = sys.argv[1], sys.argv[2:]
info = json.load(open(os.path.join(B17, 'checks', 'b17_roots.json')))
calls = [['sw_status', {}]]
for r in roots:
    sub = info[r]['sub']
    src = os.path.join(B17, 'regen', 'b17v2', sub)   # b17v2 = tools_b17 (Atan2V ByVal fix): = b17 except the 6 angled macros
    out = os.path.join(B17, 'sw_dryrun', r)
    os.makedirs(out, exist_ok=True)
    calls += [['run_macro', {'path': os.path.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                             'const_overrides': {'TABLE_PATH': os.path.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                 'SAVE_PATH': os.path.join(out, f'{r}_MASTER.SLDPRT'),
                                                 'REPORT_PATH': os.path.join(out, f'Build_{r}_report.txt')}}],
              ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
              ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    live = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(B17))), '11_MASTERS', f'{r}_MASTER.SLDPRT')
    if os.path.exists(live):   # the shipped master, read-only, for the old-configuration comparison (never saved)
        calls += [['open_doc', {'path': live, 'read_only': True}],
                  ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
calls.append(['sw_status', {}])
p = os.path.join(B17, f'calls_{name}.json')
json.dump(calls, open(p, 'w', encoding='utf-8'), indent=1)
print(p, len(calls))
