"""make_calls.py (group D): the SolidWorks dry runs of the three bent-tube masters as a call file for sw_mcp/call.py -> dryrun/calls_bent.json.
Per root: run_macro (macro + SW2 from regen/stage, SAVE_PATH / REPORT_PATH / TABLE_PATH -> dryrun/<root>/: 11_MASTERS / 03_SCRIPTS /
04_DESIGN_TABLES untouched), sweep_configs (every configuration, key dims), geometry on the reference + the two extreme sizes, close
(discard). Paths are the PC's (OMI_DEV). 61 configurations in 3 masters - one group (CLAUDE.md: restart SolidWorks every ~40 builds:
3 builds here)."""
import json, ntpath, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV = os.environ.get('OMI_DEV', r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff')
GD = ntpath.join(DEV, r'tools\_out\groupD_20261021')
exp = json.load(open(os.path.join(H, 'dryrun', 'expected_ocp.json')))
DIMS = {'1704T': ['RB@PATH', 'TUBEOD@TUBE', 'TUBEID@BORE', 'FX@PATH', 'FY@PATH', 'FACEEXT@PATH', 'FLGB_HEADR@HEADSK', 'FLGB_HUBR@HEADSK'],
        '1703T': ['RB@PATH', 'TUBEOD@TUBE', 'TUBEID@BORE', 'FX@PATH', 'FY@PATH', 'FACEEXT@PATH', 'FLGB_HEADR@HEADSK', 'FLGB_HUBR@HEADSK'],
        '6701': ['RB@PATH', 'TUBEOD@TUBE', 'TUBEID@BORE', 'FX@PATH', 'FY@PATH', 'OFFSET@NUTPLN', 'SWB_NOSETIP@SWSK']}
calls = [['sw_status', {}]]
for r in ('1704T', '1703T', '6701'):
    src = ntpath.join(GD, 'regen', 'stage'); out = ntpath.join(GD, 'dryrun', r)
    os.makedirs(os.path.join(H, 'dryrun', r), exist_ok=True)
    open(os.path.join(H, 'dryrun', r, '.gitkeep'), 'w').close()      # the folder must exist on the PC (the macro checks it first)
    cfgs = sorted((v['volume'], k) for k, v in exp.items() if v['root'] == r)
    calls += [['run_macro', {'path': ntpath.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                             'const_overrides': {'TABLE_PATH': ntpath.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                 'SAVE_PATH': ntpath.join(out, f'{r}_MASTER.SLDPRT'),
                                                 'REPORT_PATH': ntpath.join(out, f'Build_{r}_report.txt')}}],
              ['sweep_configs', {'doc': f'{r}_MASTER', 'dims': DIMS[r], 'timeout_s': 1700}]]
    for v, c in (cfgs[0], cfgs[-1]):
        calls.append(['geometry', {'doc': f'{r}_MASTER', 'config': c}])
    calls.append(['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}])
calls.append(['sw_status', {}])
json.dump(calls, open(os.path.join(H, 'dryrun', 'calls_bent.json'), 'w', encoding='utf-8'), indent=1)
print(len(calls), 'calls ->', os.path.join(H, 'dryrun', 'calls_bent.json'))
