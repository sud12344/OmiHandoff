"""make_calls.py: SolidWorks dry runs of the Air-Way-first roots, written as call files for sw_mcp/call.py.
Per root: run_macro (macro + SW2 from regen/stage/<sub>; SAVE_PATH / REPORT_PATH / TABLE_PATH overridden -> dryrun/<root>/, so 11_MASTERS
and 03_SCRIPTS stay untouched), sweep_configs of the new part, close (discard); then the shipped 11_MASTERS part read-only, sweep, close
(discard) - for verdict.py's old-configuration comparison. Paths are the PC's (OMI_DEV, default the user's OMi_Handoff), so the files can be
written in the cloud. Groups of 8-9 roots (CLAUDE.md: restart SolidWorks every ~40 builds; run_dryrun.py checks memory between groups)."""
import json, ntpath, os, re
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
DEV = os.environ.get('OMI_DEV', r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff')
AD = ntpath.join(DEV, r'tools\_out\airway_first_20261020')
roots = []
for l in open(os.path.join(A, 'regen', 'cmp.txt'), encoding='utf-8'):
    m = re.match(r'(\S+)\s+\[(straight|tee)\]', l)
    if m: roots.append((m.group(1), m.group(2)))
# largest first in each group spreads the memory; 25 roots -> 3 groups
order = sorted(roots, key=lambda x: x[0])
groups = {'g1': order[0:9], 'g2': order[9:17], 'g3': order[17:]}
info = {}
for g, rr in groups.items():
    calls = [['sw_status', {}]]
    for r, sub in rr:
        info[r] = dict(sub=sub, group=g)
        src = ntpath.join(AD, 'regen', 'stage', sub); out = ntpath.join(AD, 'dryrun', r)
        os.makedirs(os.path.join(A, 'dryrun', r), exist_ok=True)
        open(os.path.join(A, 'dryrun', r, '.gitkeep'), 'w').close()   # the folder must exist on the PC for SaveAs / the report
        calls += [['run_macro', {'path': ntpath.join(src, f'Build_{r}_MASTER.bas'), 'timeout_s': 1750,
                                 'const_overrides': {'TABLE_PATH': ntpath.join(src, f'DesignTable_{r}_SW2.xlsx'),
                                                     'SAVE_PATH': ntpath.join(out, f'{r}_MASTER.SLDPRT'),
                                                     'REPORT_PATH': ntpath.join(out, f'Build_{r}_report.txt')}}],
                  ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}],
                  ['open_doc', {'path': ntpath.join(DEV, '11_MASTERS', f'{r}_MASTER.SLDPRT'), 'read_only': True}],
                  ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    calls.append(['sw_status', {}])
    json.dump(calls, open(os.path.join(A, 'dryrun', f'calls_{g}.json'), 'w', encoding='utf-8'), indent=1)
    print(g, len(rr), 'roots:', ' '.join(r for r, _ in rr))
json.dump(info, open(os.path.join(A, 'dryrun', 'roots.json'), 'w'), indent=1)
