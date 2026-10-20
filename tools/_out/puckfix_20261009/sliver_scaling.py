"""2026-10-19: the cmp_dryrun 'sliver' window (0 > dV > -0.002 in^3) is a fixed number, but the PUCK_INSET sliver is a shell
0.0005 in thick over the puck's outer cones, so it grows with AF^2. Print dV / AF^2 for every configuration that kept its puck
(all sizes, all 17 roots): if the -24 / -32 'CHECK' rows sit on the same dV/AF^2 as the small sizes of the same elbow angle,
they are the sliver and nothing else. Output: sliver_scaling_out.txt."""
import json, os, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'cmp_dryrun_resume.py'), encoding='utf-8').read().split("out = open(")[0])   # old{} + calls_of
audits = {}
for tool, res in calls_of(os.path.join(HERE, 'out_dryrun.txt')):
    if tool == 'run_python' and isinstance(res, dict) and not res.get('error'):
        audits[res['result']['root']] = res['result']['rows']
for root in os.listdir(os.path.join(HERE, 'sw_dryrun')):
    ap = os.path.join(HERE, 'sw_dryrun', root, 'puck_audit.json')
    if root not in audits and os.path.exists(ap):
        audits[root] = json.load(open(ap))['rows']
lines, by = [], {}
for root, rows in sorted(audits.items()):
    e45 = max(x['ratio'] for x in rows) < 0.7
    for x in rows:
        o = old.get(x['config'])
        if not o or (o['ratio'] is not None and o['ratio'] < 0.2):
            continue                       # no earlier build, or the corner was missing before (restored rows)
        dv = x['volume'] - o['volume']
        if dv > 0.001:
            continue                       # restored corner (staged dry-run baselines carry no ratio)
        k = dv / x['af'] ** 2
        by.setdefault('45' if e45 else '90', []).append(k)
        lines.append(f"{x['config']:22} {'45' if e45 else '90'} AF {x['af']:.4f}  dV {dv:+.6f}  dV/AF^2 {k:+.6f}" + ('   <- CHECK in cmp' if dv <= -0.002 else ''))
out = [__doc__, ''] + lines + ['']
for a, ks in sorted(by.items()):
    out.append(f'{a} deg: n {len(ks)}  dV/AF^2 min {min(ks):+.6f} max {max(ks):+.6f} median {st.median(ks):+.6f}')
open(os.path.join(HERE, 'sliver_scaling_out.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(l for l in out if 'CHECK' in l or ' deg:' in l))
