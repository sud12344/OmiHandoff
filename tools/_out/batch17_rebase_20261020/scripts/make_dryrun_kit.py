"""Batch 17 SolidWorks dry-run kit (written in the cloud 2026-10-20, to RUN ON THE PC). For every root batch 17 changes (changeset.json,
status != unchanged) one call file dryrun/calls/NN_<root>.json for `python sw_mcp/call.py @<file>`:
  1. existing master only: open 11_MASTERS/<root>_MASTER.SLDPRT read-only, sweep_configs, close (discard)   = the "before" sweep
  2. run_macro regen/b17/<kind>/Build_<root>_MASTER.bas with SAVE_PATH / REPORT_PATH -> dryrun/<root>/, TABLE_PATH -> regen/b17 SW2
     (11_MASTERS untouched)
  3. open the dry-run part, sweep_configs, close (discard)
Order: features never tried in SolidWorks first (MERGE_LOG / NEXT_SESSION_PROMPT_2026-10-19), then the other new roots, then changed
roots. Usage: python -I make_dryrun_kit.py <repo>   (paths in the JSON = OMI_DEV, the Windows project folder)"""
import os, sys, json
REPO = os.path.abspath(sys.argv[1]); H = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')
DEV = os.environ.get('OMI_DEV', r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff')
W = lambda *p: '\\'.join((DEV,) + p)
cs = json.load(open(os.path.join(H, 'changeset.json')))
GROUPS = [('hose barb face-off', '4501 4503 4601 4603'), ('threads on 45 deg legs', '1503 1504 5501 5503 5505 6902'),
          ('per-leg swivels / NPSM nut on leg 2', '1601 1602 1603 6606 6807'), ('5404N OMi names + -06 threads', '5404N'),
          ('flange legs / collars', '1703 1704 1804 1700RC 1724 1800 1824'), ('6400 generator rebuild (A6; replaces the hand-built master)', '6400')]
order, why = [], {}
for g, rs in GROUPS:
    for r in rs.split():
        if r in cs and cs[r]['status'] != 'unchanged': order.append(r); why[r] = 'NEVER TRIED: ' + g
for r in sorted(cs):
    if r not in order and cs[r]['status'] == 'NEW root': order.append(r); why[r] = 'new root'
for r in sorted(cs):
    if r not in order and cs[r]['status'] != 'unchanged': order.append(r); why[r] = cs[r]['status'] + (' (pre-2026-09-25 macro in 03_SCRIPTS)' if cs[r]['prefix_macro'] else '')
os.makedirs(os.path.join(H, 'dryrun/calls'), exist_ok=True)
lines = []
for i, r in enumerate(order, 1):
    k = cs[r]['kind']; calls = []
    existing = cs[r]['shipped'] > 0 and r != '6400' or r == '6400'
    if existing:
        m = W('11_MASTERS', f'{r}_MASTER.SLDPRT')
        calls += [['open_doc', {'path': m, 'read_only': True}], ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
                  ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    d = W('tools', '_out', 'batch17_rebase_20261020', 'dryrun', r)
    calls += [['run_macro', {'path': W('tools', '_out', 'batch17_rebase_20261020', 'regen', 'b17', k, f'Build_{r}_MASTER.bas'),
                             'const_overrides': {'SAVE_PATH': d + f'\\{r}_MASTER.SLDPRT', 'REPORT_PATH': d + f'\\Build_{r}_report.txt',
                                                 'TABLE_PATH': W('tools', '_out', 'batch17_rebase_20261020', 'regen', 'b17', k, f'DesignTable_{r}_SW2.xlsx')},
                             'timeout_s': 1700}],
              ['open_doc', {'path': d + f'\\{r}_MASTER.SLDPRT'}], ['sweep_configs', {'doc': f'{r}_MASTER', 'timeout_s': 1700}],
              ['close_doc', {'doc': f'{r}_MASTER', 'discard_unsaved': True}]]
    fn = f'{i:02d}_{r}.json'
    json.dump(calls, open(os.path.join(H, 'dryrun/calls', fn), 'w'), indent=1)
    lines.append(f'{i:02d}  {r:8s} {k:8s} {cs[r]["shipped"]:3d} -> {cs[r]["b17"]:3d} configs  {why[r]}')
open(os.path.join(H, 'dryrun/ORDER.txt'), 'w').write(
    'Run on the PC, SolidWorks 2026 SP4 running and signed in (3DEXPERIENCE), one file per call, output kept next to it:\n'
    '  mkdir tools\\_out\\batch17_rebase_20261020\\dryrun\\<root>   (the macro does not create it)\n'
    '  python sw_mcp\\call.py @tools\\_out\\batch17_rebase_20261020\\dryrun\\calls\\NN_<root>.json > tools\\_out\\batch17_rebase_20261020\\dryrun\\out\\NN_<root>.txt\n'
    'Restart SolidWorks every ~40 builds (CLAUDE.md). Then: python tools\\_out\\batch17_rebase_20261020\\scripts\\cmp_dryrun_b17.py\n\n'
    + '\n'.join(lines) + '\n')
print(len(order), 'roots'); print('\n'.join(lines[:30]))
