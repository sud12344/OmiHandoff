"""catalog_match.py (2026-10-21): name each Brennan CAD record code by the Brennan PDF catalog column that prints the same value for the
same part number (tools/_out/brennan_catalog_20261001/catalog_verified.json). Every record in ../cache.json whose part number the
catalog prints is used, so a family is checked on all of its printed sizes, not only the STEPs on disk.
A code is NAMED when one catalog column equals it (|diff| <= 0.0015 in, fractions like 1-1/16 parsed) on >= 80 % of the family's
printed parts and on at least 2 parts. Writes catalog_codes.csv (family, code, column, agree, of)."""
import os, re, csv, json, collections
from fractions import Fraction

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
cache = json.load(open(os.path.join(PC, 'cache.json')))
cat = json.load(open(os.path.join(ROOT, 'tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')))
printed = {}
for t in cat['tables']:
    for r in t['rows']:
        printed.setdefault(r['pn'].upper(), r['values'])


def val(s):
    s = str(s).strip().replace('"', '')
    try:
        return float(s)
    except ValueError:
        pass
    m = re.match(r'^(\d+)[ -](\d+)/(\d+)$', s) or re.match(r'^()(\d+)/(\d+)$', s)
    if m:
        return float(int(m.group(1) or 0) + Fraction(int(m.group(2)), int(m.group(3))))
    return None


agree = collections.defaultdict(collections.Counter); total = collections.Counter(); fam_parts = collections.Counter()
for pn, a in cache.items():
    if 'mident' not in a or pn.upper() not in printed:
        continue
    fam = re.match(r'\{\$CADENAS_DATA/23d-libs/brennan/([^}]*)\.prj\}', a['mident']).group(1)
    kv = dict(re.findall(r'\{([A-Z0-9_]+)=([^{}]*)\}', a['mident']))
    cols = {k: val(v) for k, v in printed[pn.upper()].items()}
    fam_parts[fam] += 1
    for k, v in kv.items():
        x = val(v)
        if x is None or x <= 0 or k in ('DN', 'FONTSIZE', 'WEIGHT', 'PITCH', 'LINEID'):
            continue
        total[(fam, k)] += 1
        for c, y in cols.items():
            if y is not None and abs(x - y) <= 0.0015:
                agree[(fam, k)][c] += 1
rows = []
for (fam, k), n in sorted(total.items()):
    best = agree[(fam, k)].most_common(3)
    named = best and best[0][1] >= max(2, 0.8 * n)
    rows.append(dict(family=fam, code=k, column=best[0][0] if named else '', agree=best[0][1] if best else 0, of=n,
                     others='; '.join(f'{c} {m}' for c, m in best[1:]) if best else ''))
with open(os.path.join(H, 'catalog_codes.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(fam_parts), 'families with printed parts;', sum(1 for r in rows if r['column']), 'of', len(rows), 'codes named by a catalog column')
