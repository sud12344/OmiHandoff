"""make_calls.py (group C): the SolidWorks dry-run call files for the laptop (sw_mcp/call.py @calls_<g>.json).
Per root: run_macro with SAVE_PATH / REPORT_PATH -> dryrun/<root>/ and TABLE_PATH = the staged SW2 (regen/new/...), sweep_configs, geometry on the
reference configuration, screenshots (isometric + top; front with a section through the axis - the PNG paths are in out_<g>.txt), close without saving. 11_MASTERS untouched."""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
DEV = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'; S = DEV + r'\tools\_out\groupC_20261021'
G = {'g1': [('C2402', 'straight'), ('C2403', 'straight'), ('C2405', 'straight'), ('C0318', 'straight')],
     'g2': [('C2500', 'tee'), ('C2501', 'tee'), ('C2502', 'tee'), ('C2601', 'tee'), ('C6801', 'tee')],
     'g3': [('C0319', 'ring')]}      # gen_ring CSLEEVE (compression sleeve)
for g, roots in G.items():
    calls = [['sw_status', {}]]
    for r, sub in roots:
        d = f'{S}\\dryrun\\{r}'; doc = f'{r}_MASTER'
        calls += [['run_macro', {'path': f'{S}\\regen\\new\\{sub}\\Build_{r}_MASTER.bas', 'timeout_s': 1750,
                                 'const_overrides': {'TABLE_PATH': f'{S}\\regen\\new\\{sub}\\DesignTable_{r}_SW2.xlsx',
                                                     'SAVE_PATH': f'{d}\\{doc}.SLDPRT', 'REPORT_PATH': f'{d}\\Build_{r}_report.txt'}}],
                  ['sweep_configs', {'doc': doc, 'timeout_s': 1700}],
                  ['geometry', {'doc': doc}],
                  ['screenshot', {'doc': doc, 'views': ['isometric', 'top']}],
                  ['screenshot', {'doc': doc, 'views': ['front'], 'section_plane': 'Front Plane'}],
                  ['close_doc', {'doc': doc, 'discard_unsaved': True}]]
    json.dump(calls, open(os.path.join(A, 'dryrun', f'calls_{g}.json'), 'w'), indent=1)
    print(g, len(calls), 'calls')
