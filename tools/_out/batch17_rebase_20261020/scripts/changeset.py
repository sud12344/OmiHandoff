"""Which roots batch 17 changes, against batch 16 AS SHIPPED. Per root: b17 macro vs live-regen macro (date line ignored) and b17 SW2 vs the
SHIPPED SW2 (cell values). Writes changeset.json + changeset.txt. Usage: python -I changeset.py <repo>"""
import os, sys, re, json, glob, openpyxl
REPO = os.path.abspath(sys.argv[1]); H = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')
DATE = re.compile(r'\d{4}-\d\d-\d\d[ T]\d\d:\d\d(:\d\d)?')
def bas(p): return [DATE.sub('<d>', l) for l in open(p, encoding='latin-1').read().replace('\r\n', '\n').split('\n')] if os.path.exists(p) else None
def sw2(p):
    if not os.path.exists(p): return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3)
    return {r[0]: r[1:] for r in rows[hi + 1:] if r and r[0]}, rows[hi]
summ = json.load(open(os.path.join(H, 'regen/b17_summaries.json')))
PRE_FIX = set('5000 5404 2408 0318 5406 5406C 5406P 2700 4404 4604 5404N 2406 1405 1700 2650 2602 2605 5600 5602 2704 6600 6602'.split())
HAND = {'6400', '2500HX', '2502HX', '2603HX'}
out, js = [], {}
for sub in ('straight', 'tee'):
    for p in sorted(glob.glob(os.path.join(H, 'regen/b17', sub, 'Build_*_MASTER.bas'))):
        r = os.path.basename(p)[6:-11]
        b, lv = bas(p), bas(os.path.join(H, 'regen/live', sub, f'Build_{r}_MASTER.bas'))
        sh_bas = os.path.exists(os.path.join(REPO, '03_SCRIPTS', f'Build_{r}_MASTER.bas'))
        s17 = sw2(os.path.join(H, 'regen/b17', sub, f'DesignTable_{r}_SW2.xlsx'))
        ssh = sw2(os.path.join(REPO, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
        n17 = len(s17[0]); nsh = len(ssh[0]) if ssh else 0
        macro_same = lv is not None and b == lv
        sw2_same = ssh is not None and s17 == ssh
        if not sh_bas and not ssh: st = 'NEW root'
        elif macro_same and sw2_same: st = 'unchanged'
        elif macro_same: st = 'table change'
        elif sw2_same: st = 'macro change only'
        else: st = 'macro + table change'
        sm = summ.get(r, {})
        js[r] = dict(kind=sub, status=st, shipped=nsh, b17=n17, new=sorted(set(s17[0]) - set(ssh[0] if ssh else {})),
                     lost=sorted(set(ssh[0] if ssh else {}) - set(s17[0])), blocked=sm.get('blocked', []), prefix_macro=r in PRE_FIX, hand_built=r in HAND)
        out.append(f'{r:8s} {sub:8s} {st:22s} shipped {nsh:3d} -> b17 {n17:3d}  new {len(js[r]["new"]):3d} lost {len(js[r]["lost"])}'
                   f'  blocked {len(js[r]["blocked"])}' + ('  [pre-2026-09-25 macro in 03_SCRIPTS]' if r in PRE_FIX else '') + ('  [hand-built master]' if r in HAND else ''))
json.dump(js, open(os.path.join(H, 'changeset.json'), 'w'), indent=1)
open(os.path.join(H, 'changeset.txt'), 'w').write('\n'.join(out) + '\n')
import collections
print(collections.Counter(v['status'] for v in js.values()))
print('configurations b17', sum(v['b17'] for v in js.values()), 'new', sum(len(v['new']) for v in js.values()))
