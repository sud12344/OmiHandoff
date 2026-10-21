"""verify_proposals.py (2026-10-21): check every proposed Brennan cell (proposals.csv) three independent ways and flag the doubtful ones.
1. CATALOG  - Brennan's PDF catalogs (catalog_verified.json): if the part is printed, some printed value must equal the proposed value
              when the column's code is printed for that family (catalog_codes.csv names the column); else n/a.
2. DONOR    - the review table's Air-Way row of the same size (usually the plain part the -FG / -NWO-FG part was "near-matched" to): the
              same column; flagged when the proposal differs by more than 15 % AND 0.06 in (forged bodies differ a little, hexes and
              bores should not jump).
3. TREND    - the column over the table's other rows sorted by dash size: flagged when the proposal lies outside the range of the two
              neighbouring sizes widened by 20 %.
A cell is OK when no check flags it, DOUBT when one does (with the reason). Writes verify.csv and adds a sheet to the review workbook."""
import os, re, csv, json, glob, collections
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
import sys
IN, OUT = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('proposals.csv', 'verify.csv')   # 2026-10-21: group A = proposals_A.csv -> verify_A.csv
props = list(csv.DictReader(open(os.path.join(H, IN), encoding='utf-8')))
cat = json.load(open(J('tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')))
printed = {}
for t in cat['tables']:
    for r in t['rows']:
        printed.setdefault(r['pn'].upper(), r['values'])
cache = json.load(open(os.path.join(PC, 'cache.json')))
catcodes = {(r['family'], r['code']): r['column'] for r in csv.DictReader(open(os.path.join(H, 'catalog_codes.csv'), encoding='utf-8')) if r['column']}


def fval(s):
    s = str(s).strip()
    try:
        return float(s)
    except ValueError:
        m = re.match(r'^(?:(\d+)[ -])?(\d+)/(\d+)$', s)
        return (int(m.group(1) or 0) + int(m.group(2)) / int(m.group(3))) if m else None


def family(p):
    for v in (p, p[:-5] if p.endswith('-TUBE') else p):
        a = cache.get(v)
        if a and 'mident' in a:
            return re.match(r'\{\$CADENAS_DATA/23d-libs/brennan/([^}]*)\.prj\}', a['mident']).group(1), v
    return '', p


def dashes(p):
    return tuple(int(x) for x in re.findall(r'-(\d\d)(?=-|$)', p))


tables = {}
for path in glob.glob(J('04_DESIGN_TABLES', 'DesignTable_*.xlsx')) + glob.glob(J('tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES', 'DesignTable_FS*.xlsx')):
    if path.endswith(('_SW2.xlsx', '_FINAL.xlsx', '_v2.xlsx')):
        continue
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows[:6]) if r and '$PRP@PartNo' in r), None)
    if hi is not None:
        tables[os.path.basename(path)[12:-5]] = [dict(zip(rows[hi], r)) for r in rows[hi + 1:] if r and r[0]]

out = []
for pr in props:
    v = float(pr['value']); flags = []
    fam, bpn = family(pr['part'])
    # 1 catalog
    col = catcodes.get((fam, pr['code']))
    cat_txt = 'n/a'
    if col and bpn.upper() in printed:
        pv = fval(printed[bpn.upper()].get(col, ''))
        if pv is not None:
            cat_txt = f'{col}={printed[bpn.upper()][col]}'
            if abs(pv - v) > 0.0055:
                flags.append(f'catalog {col} prints {printed[bpn.upper()][col]}')
    # 2 donor (Air-Way row of the same size)
    rows = tables.get(pr['root'], [])
    me = dashes(pr['part']); donor_txt = 'n/a'
    for d in rows:
        p = norm(d.get('$PRP@PartNo') or '')
        if p != pr['part'] and dashes(p) == me and isnum(d.get(pr['column'])) and 'AIR-WAY' in str(d.get('$PRP@AxialSource') or '').upper():
            dv = float(d[pr['column']]); donor_txt = f'{p}={dv}'
            if abs(dv - v) > 0.06 and abs(dv - v) > 0.15 * max(abs(dv), abs(v)):
                flags.append(f'Air-Way {p} has {dv}')
            break
    # 3 trend over the table's sizes
    pts = sorted((dashes(norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or '')), float(d[pr['column']])) for d in rows
                 if isnum(d.get(pr['column'])) and dashes(norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or '')))
    lo = [y for x, y in pts if x < me]; hi = [y for x, y in pts if x > me]
    trend_txt = 'n/a'
    if lo and hi and len(set(me)) == 1:          # equal-dash parts only: a reducer's other end moves the hex / bores off the trend
        a, b = sorted((lo[-1], hi[0])); span = max(b - a, 0.05)
        trend_txt = f'{lo[-1]} .. {hi[0]}'
        if v < a - 0.2 * span - 0.02 or v > b + 0.2 * span + 0.02:
            flags.append(f'outside neighbours {lo[-1]} .. {hi[0]}')
    out.append(dict(pr, catalog=cat_txt, airway_same_size=donor_txt, neighbours=trend_txt,
                    verdict='DOUBT' if flags else 'OK', why='; '.join(flags)))

with open(os.path.join(H, OUT), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
c = collections.Counter(r['verdict'] for r in out)
checked = sum(1 for r in out if r['catalog'] != 'n/a' or r['airway_same_size'] != 'n/a' or r['neighbours'] != 'n/a')
print(c, f'| checked by at least one test: {checked} of {len(out)}',
      '| catalog-confirmed:', sum(1 for r in out if r['catalog'] != 'n/a' and r['verdict'] == 'OK'))
print('DOUBT by root:', collections.Counter(r['root'] for r in out if r['verdict'] == 'DOUBT').most_common())
