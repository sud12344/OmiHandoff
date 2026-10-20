"""verdict.py out_g1.txt [out_g2.txt ...]: per root of the batch-17 dry runs -
  macro: ran ok, problems in the final MsgBox, FAIL lines of the report, saved to the scratch folder (never 11_MASTERS);
  dry-run sweep (the first sweep after the macro): every configuration ok, 1 body, configuration set = the b17 SW2 table;
  live sweep (the second sweep, the shipped 11_MASTERS part, read-only): per old configuration, volume / size vs the dry run;
    an old configuration whose SW2 dimension cells did not change (checks/b17_roots.json + regen tables) must match (|dV| <= 1e-6 or
    relative 1e-5, size 1e-4); one whose cells changed (A19 / A21 / ...) is listed with its dV.
Writes checks/verdict.txt (appends nothing: rewritten from all given logs) and checks/verdict.json. A later log of the same root wins."""
import json, os, re, sys, openpyxl

B17 = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\batch17_20261019'
info = json.load(open(os.path.join(B17, 'checks', 'b17_roots.json')))


def sw2(sub, kind, r):
    p = os.path.join(B17, 'regen', kind, sub, f'DesignTable_{r}_SW2.xlsx')
    if not os.path.exists(p):
        return {}
    rows = list(openpyxl.load_workbook(p, data_only=True).active.iter_rows(values_only=True))
    h = rows[0]
    return {x[0]: {str(h[j]): x[j] for j in range(1, len(h)) if h[j] is not None and not str(h[j]).startswith('$')} for x in rows[1:] if x and x[0]}


def same(a, b):
    if a in (None, '') and b in (None, ''):
        return True
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return str(a).strip() == str(b).strip()


# FAIL lines explained and accepted (root, start of the FAIL text) -> reason; printed as ACCEPTED, not counted as issues
ACCEPT = {('5406HHP', 'Body diameter'): 'GetPartBox is loose around the live helical thread (length box 0.6464 vs 0.61 too); exact sweep size 0.61 x 0.84 x 0.84 = table',
          ('5406SHP', 'Body diameter'): 'GetPartBox is loose around the live helical thread; exact sweep size 1.02 x 0.84 x 0.84 = table'}
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
            m = re.search(r'Build_(\w+?)_MASTER\.bas', head)
            cur = m.group(1)
            res[cur] = dict(log=os.path.basename(log), macro=j, dry=None, live=None)
        elif tool == 'sweep_configs' and cur:
            if res[cur]['dry'] is None and res[cur]['live'] is None and 'open_doc' not in res[cur].get('_last', ''):
                res[cur]['dry'] = j
            else:
                res[cur]['live'] = j
        if cur:
            res[cur]['_last'] = tool

out, verdict = [], {}
for r in sorted(res):
    d = res[r]; m = d['macro']; sub = info[r]['sub']
    rep = os.path.join(B17, 'sw_dryrun', r, f'Build_{r}_report.txt')
    fails = [l for l in open(rep, encoding='utf-8', errors='replace').read().splitlines() if l.startswith('FAIL')] if os.path.exists(rep) else ['NO REPORT']
    acc = [(f, why) for f in fails for (ar, pre), why in ACCEPT.items() if ar == r and f[6:].startswith(pre)]
    fails = [f for f in fails if f not in [a[0] for a in acc]]
    saved = os.path.exists(os.path.join(B17, 'sw_dryrun', r, f'{r}_MASTER.SLDPRT'))
    probs = [x for x in m.get('msgbox', []) if 'problem' in x]
    new = sw2(sub, 'b17v2', r) or sw2(sub, 'b17', r)
    old = sw2(sub, 'control', r)
    issues = []
    if not m.get('ok'):
        issues.append(f"macro: {m.get('error')}")
    if fails:
        issues.append(f'{len(fails)} FAIL line(s): ' + ' | '.join(f[6:90] for f in fails[:4]))
    if not saved:
        issues.append('no part saved')
    dry = d['dry'] or {}
    rows = {x['config']: x for x in dry.get('rows', []) if x['config'] != 'Default'}
    if dry:
        bad = [c for c, x in rows.items() if not x.get('ok') or x.get('bodies') != 1]
        if bad:
            issues.append(f'sweep: {len(bad)} configuration(s) not ok / not 1 body: {bad[:6]}')
        if set(rows) != set(new):
            issues.append(f'configuration set != SW2: missing {sorted(set(new) - set(rows))[:6]} extra {sorted(set(rows) - set(new))[:6]}')
    elif m.get('ok'):
        issues.append('no dry-run sweep')
    cmp_lines = []
    live = d['live'] or {}
    if live:
        lrows = {x['config']: x for x in live.get('rows', []) if x['config'] != 'Default'}
        for c, lx in sorted(lrows.items()):
            if c not in rows:
                issues.append(f'old configuration {c} missing in the dry run'); continue
            nx = rows[c]
            dv = (nx['volume'] or 0) - (lx['volume'] or 0)
            dsz = max(abs(a - b) for a, b in zip(nx['size'], lx['size']))
            changed = c in old and c in new and any(not same(old[c].get(k), new[c].get(k)) for k in set(old[c]) | set(new[c]))
            match = abs(dv) <= max(1e-6, 1e-5 * abs(lx['volume'] or 1)) and dsz <= 1e-4
            tag = 'same' if match else ('CHANGED (table cells changed)' if changed else 'DIFFERS')
            if not match:
                cmp_lines.append(f'      {c}: dV {dv:+.6f} in^3 ({100 * dv / (lx["volume"] or 1):+.3f} %), dSize {dsz:.5f} - {tag}')
            if not match and not changed:
                issues.append(f'{c}: dV {dv:+.6f} with unchanged table cells')
    verdict[r] = dict(issues=issues, n=len(rows), live=bool(live))
    out.append(f'{r:8s} {"PASS" if not issues else "CHECK"}  configs {len(rows)}  live compared {bool(live)}  ' + ('; '.join(issues) if issues else ''))
    out += cmp_lines
    out += [f'      ACCEPTED: {f[6:80]} - {why}' for f, why in acc]
open(os.path.join(B17, 'checks', 'verdict.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(verdict, open(os.path.join(B17, 'checks', 'verdict.json'), 'w'), indent=1)
print('\n'.join(out))
