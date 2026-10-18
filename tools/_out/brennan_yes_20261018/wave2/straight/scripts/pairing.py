"""pairing.py (wave2 straight, 2026-10-18): confirm each Brennan catalog column -> review-table column mapping on the rows of the same
table that carry an Air-Way / OMi value AND have a Brennan catalog row (exact part number, or the table's OMiSKU).
Writes ../pairing.json and prints a summary. Read-only on every input."""
import os, json, re, collections
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
BASE = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root\04_DESIGN_TABLES')
OUT = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\wave2\straight')
CATJ = json.load(open(os.path.join(ROOT, r'tools\_out\brennan_catalog_20261001\catalog_verified.json'), encoding='utf-8'))

# table -> (catalog table ids, {review column: catalog column})
MAP = {
    '2403':   (['TFA-p005-t01'], {'L1@DRIVE': 'L LGTH', 'HEXB@HEX': 'C HEX', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'}),
    '2403LH': (['TFA-p005-t02'], {'L1@DRIVE': 'L LGTH', 'C2HEX@HEX': 'C HEX', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'}),
    '2404L':  (['TFA-p006-t03'], {'L20@DRIVE': 'L LGTH', 'CHEX@HEX': 'C HEX', 'D@BORE': 'B1 DRILL', 'D1@BORE': 'A2 DRILL'}),
    '2405':   (['TFA-p007-t02'], {'L2@DRIVE': 'L LGTH', 'HEXB@HEX': 'C HEX', 'D3@BORE_THRU': 'B1 DRILL'}),
    '2406':   (['TFA-p007-t03', 'TFA-p008-t01'], {'L23@DRIVE': 'L0 LGTH', 'HEXB@HEX': 'C HEX', 'D3@BORE': 'B2 DRILL'}),
    '2700':   (['TFA-p008-t03'], {'L4@DRIVE': 'L LGTH', 'C2HEX@HEX': 'C HEX', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'}),
    '2705':   (['TFA-p008-t04'], {'L24@DRIVE': 'L LGTH', 'C5HEX@HEX': 'C1 HEX', 'D@BORE': 'B2 DRILL'}),
    '2706':   (['TFA-p009-t01'], {'L25@DRIVE': 'L LGTH', 'C2HEX@HEX': 'C1 HEX', 'D1@BORE': 'A1 DRILL', 'D@BORE': 'B2 DRILL'}),
    '5000':   (['TFA-p010-t04'], {'L@DRIVE': 'L LGTH', 'CHEX@HEX': 'C HEX'}),
    '5404':   (['TFA-p011-t04'], {'L@DRIVE': 'L LGTH', 'HEXB@HEX': 'C HEX', 'D1@BORE': 'A1 DRILL', 'D2@BORE': 'A2 DRILL'}),
    '5404N':  (['TFA-p011-t05', 'TFA-p012-t01'], {'L@DRIVE': 'L LGTH', 'D1@BORE': 'A1 DRILL', 'D2@BORE': 'A2 DRILL'}),
    '5405':   (['TFA-p012-t02'], {'L@DRIVE': 'L LGTH', 'CHEX@HEX': 'C HEX', 'D@BORE': 'A1 DRILL'}),
    '5406':   (['TFA-p013-t01'], {'L2@DRIVE': 'L LGTH', 'C2HEX@HEX': 'C HEX', 'TAPDRILL@BORE': 'A1 DRILL'}),
    '5406C':  (['TFA-p066-t06', 'TFA-p067-t01'], {'L@DRIVE': 'L LGTH', 'C1HEX@HEX': 'C HEX'}),
    '6400':   (['TFA-p014-t03'], {'D1@DRIVE': 'L5 LGTH', 'HEXB@HEX': 'C4 HEX', 'D3@BORE_B': 'B1 DRILL', 'D4@BORE_A': 'B2 DRILL'}),
    '6405':   (['TFA-p015-t04'], {'L31@DRIVE': 'L LGTH', 'HEXB@HEX': 'C4 HEX', 'D3@BORE': 'B DRILL'}),
    '6410':   (['TFA-p016-t02', 'TFA-p016-t03'], {'L33@DRIVE': 'L LGTH', 'C1HEX@HEX': 'C4 HEX', 'D@BORE': 'B DRILL'}),
    '6900':   (['TFA-p018-t05', 'TFA-p019-t01'], {'W4@DRIVE': 'L LGTH', 'L2@DRIVE': 'L1 LGTH', 'C2HEX@HEX': 'C4 HEX', 'CHEX@HEX': 'C HEX', 'D1@BORE': 'B1 DRILL', 'D@BORE': 'A2 DRILL'}),
}
TBL = {t['table_id']: t for t in CATJ['tables']}


def num(s):
    try:
        return float(str(s).strip())
    except (TypeError, ValueError):
        return None


def norm(pn):
    return re.sub(r'[^0-9A-Z]', '', str(pn).upper())


res = {}
for t, (tids, mp) in MAP.items():
    ws = openpyxl.load_workbook(os.path.join(BASE, f'DesignTable_{t}.xlsx'), read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]
    cat = {}
    for tid in tids:
        if tid not in TBL:
            print('no catalog table', tid); continue
        for r in TBL[tid]['rows']:
            cat[norm(r['pn'])] = (tid, r)
    stats = collections.defaultdict(lambda: dict(n=0, eq=0, rnd=0, diff=[]))
    for r in rows[2:]:
        if not r[0]:
            continue
        d = dict(zip(h, r))
        keys = [norm(d[None] if None in d else r[0]), norm(d.get('$PRP@OMiSKU') or '')]
        hit = next((cat[k] for k in keys if k and k in cat), None)
        if not hit:
            continue
        tid, cr = hit
        for col, cc in mp.items():
            v, c = num(d.get(col)), num(cr['values'].get(cc))
            if v is None or c is None:
                continue
            s = stats[col]; s['n'] += 1
            dd = abs(v - c)
            if dd < 1e-9: s['eq'] += 1
            elif dd <= 0.0051: s['rnd'] += 1
            else: s['diff'].append((r[0], d.get('$PRP@ScopeAction'), v, c))
    res[t] = {col: dict(catalog_col=mp[col], **s) for col, s in stats.items()}
    print(f'== {t} ({",".join(tids)})')
    for col, s in res[t].items():
        print(f'   {col:14} <- {s["catalog_col"]:10} pairs {s["n"]:3} equal {s["eq"]:3} rounding {s["rnd"]:3} differ {len(s["diff"]):3} {s["diff"][:6]}')
json.dump(res, open(os.path.join(OUT, 'pairing.json'), 'w', encoding='utf-8'), indent=1)
