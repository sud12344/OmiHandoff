"""verdict.py dryrun/out_bent.txt (group D): per bent-tube master of the dry run -
  macro: ran ok, FAIL lines of the report (incl. its own per-configuration box check and the thread check), saved to dryrun/<root>;
  sweep: every configuration ok and 1 body, configuration set = regen/stage SW2;
  closed loop: each configuration's volume / box size vs the OCP rebuild of the same numbers (dryrun/expected_ocp.json, threads off):
    PASS within 0.3 % volume and 0.005 in size (the OCP model is the macro's geometry; only the threads' suppressed state may differ).
Writes checks/dryrun_verdict.txt."""
import json, os, re, sys, openpyxl
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exp = json.load(open(os.path.join(H, 'dryrun', 'expected_ocp.json')))
res = {}
for log in sys.argv[1:]:
    cur = None
    for b in re.split(r'^=== ', open(log, encoding='utf-8', errors='replace').read(), flags=re.M)[1:]:
        head, _, body = b.partition('\n')
        tool = head.split(' ', 1)[0]
        txt = body.rsplit('\n--- ', 1)[0].strip()
        try:
            j = json.loads(txt)
        except ValueError:
            j = {'raw': txt[:300]}
        if tool == 'run_macro':
            cur = re.search(r'Build_(\w+?)_MASTER\.bas', head).group(1); res[cur] = dict(macro=j, sweep=None)
        elif tool == 'sweep_configs' and cur:
            res[cur]['sweep'] = j
out = []
for r in ('1704T', '1703T', '6701'):
    if r not in res:
        out.append(f'{r:6} NOT RUN'); continue
    d = res[r]; m = d['macro']; issues = []
    rep = os.path.join(H, 'dryrun', r, f'Build_{r}_report.txt')
    fails = [l for l in open(rep, encoding='utf-8', errors='replace').read().splitlines() if l.startswith('FAIL')] if os.path.exists(rep) else ['NO REPORT']
    if not m.get('ok'): issues.append(f"macro: {m.get('error')}")
    if fails: issues.append(f'{len(fails)} FAIL line(s): ' + ' | '.join(f[6:100] for f in fails[:5]))
    if not os.path.exists(os.path.join(H, 'dryrun', r, f'{r}_MASTER.SLDPRT')): issues.append('no part saved')
    rows = {x['config']: x for x in (d['sweep'] or {}).get('rows', []) if x['config'] != 'Default'}
    want = {k for k, v in exp.items() if v['root'] == r}
    t = list(openpyxl.load_workbook(os.path.join(H, 'regen', 'stage', f'DesignTable_{r}_SW2.xlsx')).active.iter_rows(values_only=True))
    sw2 = {x[0] for x in t[1:] if x and x[0]}
    if set(rows) != sw2: issues.append(f'configuration set differs from the SW2: missing {sorted(sw2 - set(rows))}, extra {sorted(set(rows) - sw2)}')
    cl = []
    for c in sorted(rows):
        x = rows[c]
        if not x.get('ok') or x.get('bodies') != 1:
            issues.append(f'{c}: ok {x.get("ok")}, bodies {x.get("bodies")}')
        if c in exp and x.get('volume'):
            dv = (x['volume'] - exp[c]['volume']) / exp[c]['volume']
            ds = max(abs(a - b) for a, b in zip(sorted(x['size']), sorted(exp[c]['size'])))
            tag = 'ok' if abs(dv) <= 0.003 and ds <= 0.005 else 'CHECK'
            if tag != 'ok': issues.append(f'{c}: volume {100 * dv:+.2f} % / size {ds:.4f} vs the OCP closed loop')
            cl.append(f'      {c:18} SW {x["volume"]:.5f} OCP {exp[c]["volume"]:.5f} ({100 * dv:+.3f} %), size dev {ds:.4f} {tag}')
    out.append(f'{r:6} {"PASS" if not issues else "ISSUES"} - {len(rows)} configurations' + ''.join(f'\n   - {i}' for i in issues))
    out += cl
open(os.path.join(H, 'checks', 'dryrun_verdict.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
