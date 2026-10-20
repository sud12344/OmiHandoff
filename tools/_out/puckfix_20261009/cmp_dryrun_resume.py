"""2026-10-19 resume of cmp_dryrun.py (unchanged logic). The 2026-10-09 run (out_dryrun.txt) stopped after 2701 when SolidWorks
closed; 2702 5500 5502 5504 6502 6503 1501 6801 6802 were dry-run on 2026-10-18/19 through the MCP tools directly (the CLI could not
reach SolidWorks): their reports are sw_dryrun/<root>/Build_<root>_report.txt and their puck audits sw_dryrun/<root>/puck_audit.json
(same audit code as make_calls.py). Output: cmp_dryrun_resume_out.txt.

2026-10-09 puck fix: check the SolidWorks dry runs of the 17 elbow roots built with PUCK_INSET (out_dryrun.txt).

Per root: report FAIL lines; every configuration 1 body and its corner puck present (cone area about Z / AF^2 > 0.2; a merged
puck gives ~0.79 on 90 deg elbows, ~0.39 on 45 deg, a dropped one 0).
Per configuration against the build before the fix:
  shipped configurations  puck_audit_20261009/audit_rows.json (read-only audit of the 11_MASTERS parts, same measure)
  new configurations      wave1_ship_20261009/swtest/calls/out_all.txt (today's dry runs of the staged batch, before the fix)
Expected: a configuration whose puck was there loses only the PUCK_INSET sliver (-0.0005 in radially on the outer corner:
0 > dV > -0.002 in^3); one whose puck was dropped gains the outer corner = 0.1527 AF^3 (quarter puck, 90 deg) or 0.0764 AF^3
(eighth, 45 deg) minus the sliver (within 3 %).
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
O = os.path.abspath(os.path.join(HERE, '..'))


def calls_of(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'=== (\w+) (.*?)\n(.*?)\n--- [\d.]+s', t, re.S):
        try:
            yield m.group(1), json.loads(m.group(3))
        except Exception:
            yield m.group(1), m.group(3)


old = {}
for x in json.load(open(os.path.join(O, 'puck_audit_20261009', 'audit_rows.json'))):
    old[x['config']] = dict(volume=x['volume'], ratio=x['ratio'], src='11_MASTERS audit')
for tool, res in calls_of(os.path.join(O, 'wave1_ship_20261009', 'swtest', 'calls', 'out_all.txt')):
    if tool == 'sweep_configs' and isinstance(res, dict):
        for r in res['rows']:
            if r['config'] != 'Default' and r['config'] not in old:
                old[r['config']] = dict(volume=r['volume'], ratio=None, src='staged dry run 10-09')
QUARTER = 0.02718 / 0.5625 ** 3          # quarter puck at A/F 0.5625 (FOLDS EXPECTED) -> per AF^3

out = open(os.path.join(HERE, 'cmp_dryrun_resume_out.txt'), 'w', encoding='utf-8')


def say(s=''):
    print(s)
    out.write(s + '\n')


say(__doc__)
reports, audits = {}, {}
for tool, res in calls_of(os.path.join(HERE, 'out_dryrun.txt')):
    if tool == 'run_macro' and isinstance(res, dict) and 'ran' in res:   # skip the 'SolidWorks is not running' errors of 10-09
        reports[res['ran'].replace('Build', '')] = res
    if tool == 'run_python' and isinstance(res, dict):
        if res.get('error'):
            continue   # the 10-09 run's errors after SolidWorks closed (those roots come from sw_dryrun/ below)
        audits[res['result']['root']] = res['result']['rows']
for root in os.listdir(os.path.join(HERE, 'sw_dryrun')):
    ap = os.path.join(HERE, 'sw_dryrun', root, 'puck_audit.json')
    rp = os.path.join(HERE, 'sw_dryrun', root, f'Build_{root}_report.txt')
    if root in audits or not os.path.exists(ap) or not os.path.exists(rp):
        continue
    audits[root] = json.load(open(ap))['rows']
    lines = open(rp, encoding='utf-8', errors='replace').read().splitlines()
    fl = [l for l in lines if l.startswith('FAIL')]
    reports[root] = dict(ok=any(l.startswith('OK    Saved to') for l in lines), secs='mcp',
                         report=dict(fail=len(fl), fail_lines=fl, tail=[l for l in lines if 'All-config sweep' in l]))
allok = True
nfixed = 0
for root in '2504 2505 1502 6500 6501 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802'.split():
    rep = reports.get(root); rows = audits.get(root)
    if not rep or rows is None:
        say(f'{root:6} MISSING run_macro or audit'); allok = False; continue
    rs = rep.get('report') or {}
    tail = [l for l in rs.get('tail', []) if 'All-config sweep' in l]
    e45 = max(x['ratio'] for x in rows) < 0.7      # 90 deg elbows ~0.79, 45 deg ~0.39 (2503 up to 0.62)
    bad, fixed, sliver, other = [], [], [], []
    for x in rows:
        if x['bodies'] != 1 or x['ratio'] < 0.2:
            bad.append(f"{x['config']} bodies {x['bodies']} ratio {x['ratio']}"); continue
        o = old.get(x['config'])
        if not o:
            other.append(f"{x['config']}: no earlier build"); continue
        dv = x['volume'] - o['volume']
        corner = QUARTER * x['af'] ** 3 * (0.5 if e45 else 1.0)
        if -0.002 < dv <= 1e-6:
            sliver.append(dv)
        elif abs(dv - corner) <= 0.03 * corner:
            fixed.append(f"{x['config']} +{dv:.6f} (corner {corner:.6f}; was {o['src']}{', ratio %s' % o['ratio'] if o['ratio'] is not None else ''})")
        else:
            other.append(f"{x['config']}: dV {dv:+.6f} (corner would be {corner:.6f}) [{o['src']}]")
    nfixed += len(fixed)
    ok = rep['ok'] and not rs.get('fail') and not bad and not other
    allok &= ok
    say(f"{root:6} {'OK ' if ok else 'BAD'} report FAIL {rs.get('fail')} ({rep['secs']} s; {tail[-1].strip() if tail else ''}); "
        f"{len(rows)} configurations, puck present in all: {not bad}; sliver only {len(sliver)}"
        f"{' (dV %.6f .. %.6f)' % (min(sliver), max(sliver)) if sliver else ''}; corner restored {len(fixed)}")
    for l in rs.get('fail_lines', []):
        say('    FAIL ' + l)
    for l in bad:
        say('    NO PUCK ' + l)
    for l in fixed:
        say('    restored ' + l)
    for l in other:
        say('    CHECK ' + l)
say()
say(f'{nfixed} configurations got their outer corner back')
say('ALL CHECKS PASS' if allok else 'SOMETHING TO CHECK - see above')
