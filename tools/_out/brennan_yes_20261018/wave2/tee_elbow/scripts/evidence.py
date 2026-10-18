"""mapping evidence per table: for every (table column <- catalog column) of build.T, agreement on (a) rows of the same table with the
same -FG part number holding a base value, (b) plain Air-Way twins (pn without -FG; a different part: meaning evidence only),
(c) OMi Items same part (build.omi_checks), (d) OMi drawings 2026-10-18 (1504 / 1602 siblings). Tolerance 0.011 (2-decimal rounding)."""
import os, sys, csv, json, re
sys.argv = [sys.argv[0]]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
out = []
for t, cfg in B.T.items():
    hdr, brows = B.btabs.get(t) or B.base_table(t)
    out.append(f'===== {t}  ({cfg["tid"]}, TFA p.{B.TAB[cfg["tid"]]["page"]} "{B.TAB[cfg["tid"]]["series"]} {B.TAB[cfg["tid"]]["title"]}")')
    for col, ccol, mean in cfg['dims'] + [(c, cc, 'NOT PROPOSED (unconfirmed)') for c, cc in cfg.get('unconf', [])]:
        res = {}
        for mode in ('same-FG', 'twin'):
            m = n = 0; bad = []
            for pn, row in brows.items():
                p2 = pn.replace(' ', '-')
                if mode == 'twin':
                    if p2.endswith('FG'): continue
                    p2 = p2 + '-FG'
                elif not p2.endswith('FG'): continue
                if p2 not in B.CAT or col not in row or B.empty(row.get(col)): continue
                tab, cr = B.CAT[p2]
                if tab['table_id'] != cfg['tid']: continue
                v = B.num(cr['values'].get(ccol, ''))
                try: a = float(row[col])
                except (TypeError, ValueError): continue
                if v is None: continue
                n += 1
                if abs(a - v) <= 0.011: m += 1
                else: bad.append(f'{pn} {a} vs {v}')
            res[mode] = f'{m}/{n}' + (f' (differ: {"; ".join(bad[:3])}{" ..." if len(bad) > 3 else ""})' if bad else '')
        oc = [x for x in json.load(open(os.path.join(HERE, 'omi_checks.json'))) if x[0] == t and x[2] == col]
        om = f'{sum(1 for x in oc if abs(float(x[3]) - x[4]) <= 0.0005)}/{len(oc)}' if oc else '-'
        out.append(f'  {col:16} <- {ccol:9} {mean[:70]:70} | same -FG pn in table: {res["same-FG"]} | plain twins: {res["twin"]} | OMi same part: {om}')
# OMi drawings (2026-10-18) of 1504 / 1602 siblings vs the catalog
dr = list(csv.DictReader(open(os.path.join(B.R, r'tools\_out\omi_answers_20261018\source\drawings_transcribed.csv'), encoding='utf-8')))
FEAT = {'leg_port': 'L LGTH', 'leg_stemtip': 'M1 LGTH', 'leg_nutface': 'M LGTH', 'hex': 'Y FLATS', 'nut': 'C HEX', 'nut2': 'C HEX', 'bore': 'A2 DRILL', 'bore2': 'A3 DRILL'}
out.append('===== OMi drawings 2026-10-18 (tools/_out/omi_answers_20261018/source/drawings_transcribed.csv) vs Brennan TFA p.22 (1504) / p.48 (1602)')
for x in dr:
    if not x['part_number'].startswith(('1504', '1602')) or x['feature'] not in FEAT: continue
    c = B.CAT.get(x['part_number'])
    if not c: out.append(f'  {x["part_number"]} not in catalog'); continue
    v = c[1]['values'].get(FEAT[x['feature']], '')
    ok = B.num(v) is not None and abs(float(x['value']) - B.num(v)) <= 0.0005
    out.append(f'  {x["part_number"]:17} {x["feature"]:12} ({x["meaning"][:55]:55}) OMi {x["value"]:6} | Brennan {FEAT[x["feature"]]:8} {v:6} {"EQUAL" if ok else "DIFFERS"}')
open(os.path.join(B.OUT, 'mapping_evidence.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
