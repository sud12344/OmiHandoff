"""verdict19.py dryrun/out_g1.txt [...]: per batch-19 root (adapted from airway_first_20261020/scripts/verdict.py) -
  macro ran ok, 0 FAIL lines, part saved into dryrun/<root>; dry-run sweep: every configuration ok + 1 body, configuration set = regen SW2;
  live sweep (the shipped master, read-only; 2500 / 2502 / 2603 = the hand-built 2500HX / 2502HX / 2603HX): every old configuration must
  match volume / size, except the HX migration (E_gen job 2 README: 2500 corner puck inset 0.0005, 2502 port collar 0.26 + origin at the
  crossing, 65 non-OMi / DROP configurations dropped) - listed as EXPECTED, not issues.
Writes merge/checks/dryrun_verdict.txt + .json. A later log of the same root wins."""
import json, os, re, sys, openpyxl
M = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H = os.path.abspath(os.path.join(M, '..', '..', '..', '..'))
ship = json.load(open(os.path.join(M, 'ship_roots.json')))
HX = {'2500': '2500HX', '2502': '2502HX', '2603': '2603HX'}


def cfgs(p):
    if not os.path.exists(p): return set()
    return {r[0] for r in openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0].iter_rows(min_row=2, values_only=True) if r and r[0]}


res = {}
for log in sys.argv[1:]:
    blocks = re.split(r'^=== ', open(log, encoding='utf-8', errors='replace').read(), flags=re.M)[1:]
    cur = None
    for b in blocks:
        head, _, body = b.partition('\n')
        tool = head.split(' ', 1)[0]
        txt = body.rsplit('\n--- ', 1)[0].strip()
        try:
            j = json.loads(txt)
        except ValueError:
            j = {'raw': txt[:300]}
        if tool == 'run_macro':
            cur = re.search(r'Build_(\w+?)_MASTER\.bas', head).group(1)
            res[cur] = dict(macro=j, dry=None, live=None, _last='run_macro')
        elif tool == 'sweep_configs' and cur:
            res[cur]['live' if res[cur]['_last'] == 'open_doc' else 'dry'] = j
        if cur:
            res[cur]['_last'] = tool

out, verdict = [], {}
for r in sorted(ship):
    if r not in res:
        out.append(f'{r:9s} NOT RUN'); verdict[r] = dict(issues=['not run']); continue
    d = res[r]; m = d['macro']
    rep = os.path.join(M, 'dryrun', r, f'Build_{r}_report.txt')
    fails = [l for l in open(rep, encoding='utf-8', errors='replace').read().splitlines() if l.startswith('FAIL')] if os.path.exists(rep) else ['NO REPORT']
    saved = os.path.exists(os.path.join(M, 'dryrun', r, f'{r}_MASTER.SLDPRT'))
    new = cfgs(os.path.join(M, 'regen', ship[r], f'DesignTable_{r}_SW2.xlsx'))
    issues, notes = [], []
    if not m.get('ok'): issues.append(f"macro: {m.get('error')}")
    if fails: issues.append(f'{len(fails)} FAIL line(s): ' + ' | '.join(f[6:90] for f in fails[:4]))
    if not saved: issues.append('no part saved')
    rows = {x['config']: x for x in (d['dry'] or {}).get('rows', []) if x['config'] != 'Default'}
    if d['dry']:
        bad = [c for c, x in rows.items() if not x.get('ok') or x.get('bodies') != 1]
        if bad: issues.append(f'sweep: {len(bad)} not ok / not 1 body: {bad[:6]}')
        if set(rows) != new: issues.append(f'configuration set != SW2: missing {sorted(new - set(rows))[:6]} extra {sorted(set(rows) - new)[:6]}')
    else:
        issues.append('no dry-run sweep')
    live = d['live'] or {}
    lrows = {x['config']: x for x in live.get('rows', []) if x['config'] != 'Default'}
    nsame = 0
    for c, lx in sorted(lrows.items()):
        if c not in rows:
            (notes if r in HX else issues).append(f'old configuration {c} not in the new master' + (' (HX: non-OMi / DROP, EXPECTED)' if r in HX else ''))
            continue
        nx = rows[c]
        dv = (nx['volume'] or 0) - (lx['volume'] or 0)
        dsz = max(abs(a - b) for a, b in zip(sorted(nx['size']), sorted(lx['size'])))
        if abs(dv) <= max(1e-6, 1e-5 * abs(lx['volume'] or 1)) and dsz <= 1e-4:
            nsame += 1; continue
        line = f'{c}: dV {dv:+.6f} in^3 ({100 * dv / (lx["volume"] or 1):+.3f} %), dSize {dsz:.5f}'
        (notes if r in HX else issues).append(line + (' (HX migration, EXPECTED)' if r in HX else ''))
    verdict[r] = dict(issues=issues, n=len(rows), live=bool(live), old_same=nsame, old=len(lrows))
    out.append(f'{r:9s} {"PASS" if not issues else "CHECK"}  configs {len(rows)}  old master compared {bool(live)} ({nsame} / {len(lrows)} identical)  '
               + ('; '.join(issues[:6]) if issues else ''))
    out += [f'      {n}' for n in notes]
os.makedirs(os.path.join(M, 'checks'), exist_ok=True)
open(os.path.join(M, 'checks', 'dryrun_verdict.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(verdict, open(os.path.join(M, 'checks', 'dryrun_verdict.json'), 'w'), indent=1)
print('\n'.join(out))
