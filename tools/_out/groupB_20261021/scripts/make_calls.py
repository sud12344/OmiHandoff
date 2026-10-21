"""make_calls.py (group B): SolidWorks dry runs of the group B masters, as call files for sw_mcp/call.py (paths are the PC's: OMI_DEV, default
the user's OMi_Handoff). Per master: run_macro with TABLE_PATH = the staged SW2 in out/<set>/, SAVE_PATH / REPORT_PATH -> dryrun/<master>/
(11_MASTERS and 03_SCRIPTS untouched), sweep_configs, close (discard). 6801 also opens the shipped 11_MASTERS part read-only and sweeps it (the
39 old configurations must keep their volume / size). Three groups (CLAUDE.md: restart SolidWorks every ~40 builds)."""
import json, ntpath, os
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'groupB_20261021')
DEV = os.environ.get('OMI_DEV', r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff')
AD = ntpath.join(DEV, r'tools\_out\groupB_20261021')
GROUPS = {'g1': [('af', r) for r in ('6900', '6901', '6805', '6806', '6809', '6801')],
          'g2': [('af', r) for r in ('6815', '6832', '6835')] + [('fs', r) for r in ('FS2408', 'FS6402', 'FS6809', 'FS6809C', 'FS6809R', 'FS6809RC')],
          'g3': [('fs', r) for r in ('FS6801', 'FS6801R', 'FS6801NR', 'FS6802R', 'FS6802NR', 'FS6803NR', 'FS6804R', 'FS6804NR', '4000')],
          'g4': [('fs', r) for r in ('FS2403', 'FS2404', 'FS6400', 'FS6403')]}      # phase 2 (2026-10-21 STEPs): the FS straights with the new FSM_MEAS sizes
SHIPPED = {'6801'}
for g, rr in GROUPS.items():
    calls = [['sw_status', {}]]
    for s, r in rr:
        src = ntpath.join(AD, 'out', s); out = ntpath.join(AD, 'dryrun', r)
        os.makedirs(os.path.join(A, 'dryrun', r), exist_ok=True); open(os.path.join(A, 'dryrun', r, '.gitkeep'), 'w').close()
        assert os.path.exists(os.path.join(A, 'out', s, f'Build_{r}_MASTER.bas')), r
        calls += [['run_macro', {'path': ntpath.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                                 'const_overrides': {'TABLE_PATH': ntpath.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                     'SAVE_PATH': ntpath.join(out, f'{r}_MASTER.SLDPRT'),
                                                     'REPORT_PATH': ntpath.join(out, f'Build_{r}_report.txt')}}],
                  ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
        if r in SHIPPED:
            calls += [['open_doc', {'path': ntpath.join(DEV, '11_MASTERS', f'{r}_MASTER.SLDPRT'), 'read_only': True}],
                      ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                      ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    calls.append(['sw_status', {}])
    json.dump(calls, open(os.path.join(A, 'dryrun', f'calls_{g}.json'), 'w', encoding='utf-8'), indent=1)
    print(g, ' '.join(r for _, r in rr))
