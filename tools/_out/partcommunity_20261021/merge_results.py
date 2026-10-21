"""merge_results.py (2026-10-21): pass 1 (OMi number + known Brennan aliases) + pass 2 (re-try with -FG / -NWO swapped) -> pc_final.csv.
match: 'exact' = Brennan has a CAD model under the OMi number; 'alias' = under a known numbering difference (-TUBE dropped, 6408-HHP ->
6408-H, 5406-HHP -> 5406-HP, -ASY dropped); 'other part' = only a different part answered (forged <-> plain swap, e.g. OMi 1703-08-08-FG
vs Brennan's swept 1703-08-08) - NOT counted as found; '' = no CAD model at Brennan."""
import csv, os
H = os.path.dirname(os.path.abspath(__file__))
p1 = {r['part']: r for r in csv.DictReader(open(os.path.join(H, 'pc_results_pass1.csv'), encoding='utf-8'))}
p2 = {r['part']: r for r in csv.DictReader(open(os.path.join(H, 'pc_results_pass2.csv'), encoding='utf-8'))}
SWAP = lambda a, b: a.replace('-NWO-FG', '').replace('-FG', '') == b.replace('-NWO-FG', '').replace('-FG', '') and a != b
rows = []
for p, r in p1.items():
    r = dict(r)
    if r['found'] == 'yes':
        r['match'] = 'alias' if r['tried_as'] else 'exact'
    elif p in p2 and p2[p]['found'] == 'yes':
        r = dict(p2[p]); r['match'] = 'other part' if SWAP(p, r['tried_as'] or p) else 'alias'
    else:
        r['match'] = ''
    rows.append(r)
with open(os.path.join(H, 'pc_final.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['part', 'match', 'found', 'tried_as', 'family', 'pn', 'params']); w.writeheader()
    w.writerows({k: r.get(k, '') for k in w.fieldnames} for r in rows)
import collections; print(collections.Counter(r['match'] or 'none' for r in rows))
