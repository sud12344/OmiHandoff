"""stage_77.py (2026-10-16): the 77 OMi adapter SKUs the 2026-09 crawl dropped (listing session REPORT.md section 3,
tools/_out/omi_enum_20261015/data/missing_adapters_vs_review_tables.csv). User 2026-10-15: "use airway dimensions, check brennan too";
standing rule 2026-09-25: OMi's dimension file first, Air-Way fills (Task A form, certain column mappings only).

Read-only on every source. Writes ../CHANGES.csv (row-level edits, nothing applied), ../rows77.json and ../REPORT_77.md.
  - 37 SKUs already have an Air-Way row in their review table, marked DROP only because the crawl had dropped the OMi SKU:
      ScopeAction DROP -> BUILD, $PRP@OMiSKU = the SKU;
      OMi value (certain mapping, tools/_out/omi_audit/mapping_final.json) that differs beyond rounding -> replaces the Air-Way value
      (row becomes ASSUMED, Task A form in $PRP@AxialSource);
      Brennan TFA catalog check on clearly paired columns (same letter / same meaning): Air-Way = Brennan on every compared cell, with
      length and hex among them, and no OMi value taken -> VERIFIED; a difference -> noted in $COMMENT (dimension source wins, s6).
  - 40 SKUs have no row (Air-Way does not print them): listed with OMi's values and Brennan's row; not added (a new row needs the
    end-library columns of its table - the tabling step), DataStatus would be MISSING unless OMi's values cover the row.
python -I stage_77.py"""
import csv, json, os, re, sys, collections
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools', '_out', 'orfs_airway_20261015', 'scripts'))
from compare_orfs import cmp_num                                  # the project's rounding rule (match_ORFS.py cmp_num)

G = json.load(open(os.path.join(HERE, 'gathered.json'), encoding='utf-8'))
MAP = [m for m in json.load(open(os.path.join(ROOT, 'tools', '_out', 'omi_audit', 'mapping_final.json'), encoding='utf-8')) if m['certainty'] == 'certain']
OMICOL = {'OverallLength': 'Overall Length', 'BodyDiameter': 'Body Diameter', 'M1': 'M 1 Size', 'M2': 'M 2 Size', 'L1': 'L 1 Size',
          'L2': 'L 2 Size', 'HexFlat': 'Hex Flat', 'S1ID': 'Side 1 ID', 'NutHex1': 'Nut Hex 1', 'S2ID': 'Side 2 ID', 'NutHex2': 'Nut Hex 2',
          'S3ID': 'Side 3 ID', 'S4ID': 'Side 4 ID'}
# Brennan TFA column per review-table column - only pairs with the same letter or an unambiguous meaning (length / hex / flats / drill)
BR = {
    '2403': {'L1@DRIVE': 'L LGTH', 'HEXB@HEX': 'C HEX', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'},
    '2406': {'L23@DRIVE': 'L0 LGTH', 'HEXB@HEX': 'C HEX', 'D3@BORE': 'B2 DRILL'},
    '2501': {'M@DRIVE': 'M LGTH', 'N@DRIVE': 'L LGTH', 'Y@REF': 'Y FLATS', 'D@BORE': 'B1 DRILL', 'D1@DRILL': 'A2 DRILL'},
    '2502': {'M1@DRIVE': 'M LGTH', 'N1@DRIVE': 'L LGTH', 'Y1@DRIVE': 'Y FLATS', 'D@BORE': 'B1 DRILL'},
    '2650': {'M1@DRIVE': 'M1 LGTH', 'M2@DRIVE': 'M2 LGTH', 'M3@DRIVE': 'M3 LGTH', 'M4@DRIVE': 'M4 LGTH', 'Y@HEX': 'Y FLATS',
             'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL', 'D3@BORE': 'B3 DRILL', 'D4@BORE': 'B4 DRILL'},
    '2705': {'L24@DRIVE': 'L LGTH', 'D@BORE': 'B2 DRILL'},
    '5406': {'L2@DRIVE': 'L LGTH', 'C2HEX@HEX': 'C HEX', 'TAPDRILL@BORE': 'A1 DRILL'},
    '5502': {'N@DRIVE': 'N LGTH', 'N1@DRIVE': 'N1 LGTH', 'W@REF': 'Y FLATS', 'D@BORE': 'A1 DRILL'},
    # 6400: BORE_B = the JIC side (audit mapping S1ID -> D3@BORE_B; OMi side 1 = male JIC), Brennan B1 = the 37 deg side
    '6400': {'D1@DRIVE': 'L5 LGTH', 'HEXB@HEX': 'C4 HEX', 'D3@BORE_B': 'B1 DRILL', 'D4@BORE_A': 'B2 DRILL'},
    '6405': {'L31@DRIVE': 'L LGTH', 'HEXB@HEX': 'C4 HEX'},
    '6410': {'L33@DRIVE': 'L LGTH', 'C1HEX@HEX': 'C4 HEX', 'D@BORE': 'B DRILL'},
    '6500': {'LEG_M@DRIVE': 'M LGTH', 'HEXB@HEX': 'C HEX', 'Y@REF': 'Y FLATS', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'},
    '6502': {'M2@DRIVE': 'M2 LGTH', 'M6@DRIVE': 'M6 LGTH', 'C3HEX@HEX': 'C HEX', 'Y@HEX': 'Y FLATS', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'},
    '6505': {'CHEX@HEX': 'C HEX', 'C3HEX@HEX': 'C1 HEX', 'D@BORE': 'B DRILL'},
    '6602': {'M1@DRIVE': 'M LGTH', 'C3HEX@HEX': 'C HEX', 'Y@HEX': 'Y HEX', 'D1@BORE': 'A1 DRILL', 'D2@BORE': 'A2 DRILL', 'D3@BORE': 'A3 DRILL'},
    '6801': {'LEG_ORB@DRIVE': 'M7 LGTH', 'HEXB@HEX': 'C HEX', 'Y@REF': 'Y FLATS', 'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL'},
    '6803': {'LEG1@DRIVE': 'M1 LGTH', 'LEG2@DRIVE': 'M2 LGTH', 'LEG3@DRIVE': 'M7 LGTH', 'HEXB@HEX': 'C HEX', 'Y@REF': 'Y FLATS',
             'D1@BORE': 'B1 DRILL', 'D2@BORE': 'B2 DRILL', 'D3@BORE': 'B3 DRILL'},
    '6901': {'CHEX@HEX': 'C1 HEX', 'C4HEX@HEX': 'C HEX', 'D1@BORE': 'B DRILL', 'D@BORE': 'A DRILL'},
}
LEN_HEX = lambda c: bool(re.search(r'(^L\d*@|^M\d*@|^N\d*@|LEG|^D1@DRIVE)', c)) or 'HEX' in c or c.startswith(('Y@', 'Y1@', 'W@'))


def omi_items():
    wb = openpyxl.load_workbook(os.path.join(ROOT, '07_RAW_EXTRACTS', 'omi_dimensions', 'WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)
    rows = list(wb['Items'].iter_rows(values_only=True))
    hdr = [str(h) if h is not None else '' for h in rows[0]]
    want = {x['sku'] for x in G}
    out = {}
    for i, r in enumerate(rows[1:], start=2):
        pn = str(r[0] or '').strip()
        if pn in want:
            out[pn] = dict(zip(hdr, r), _row=i)
    return out, hdr


def main():
    O, hdr = omi_items()
    col_letter = {h: openpyxl.utils.get_column_letter(i + 1) for i, h in enumerate(hdr)}
    changes, recs = [], []
    for x in G:
        sku, tab = x['sku'], x['table']
        root = tab.replace('DesignTable_', '').replace('.xlsx', '') if x['row'] else None
        o = O.get(sku, {})
        rec = dict(sku=sku, table=tab, row=x['row'], old_scope=x['scope'], old_status=x['status'], brennan=x['brennan'],
                   omi_row=o.get('_row'), omi_values={k: o.get(v) for k, v in OMICOL.items() if o.get(v) not in (None, '', 'NA', 'N/A', '-')})
        if not x['row']:
            rec['proposal'] = ('no Air-Way row (Air-Way does not print this size); Brennan prints it (check only)' if x['brennan'] else
                               'no Air-Way row and no Brennan catalog row') + ('; OMi parts file gives ' + ', '.join(f'{k} {v}' for k, v in rec['omi_values'].items()) if rec['omi_values'] else '; OMi gives no dimension')
            recs.append(rec)
            continue
        dims = dict(x['dims'])
        took = []
        for m in MAP:                                              # OMi first (certain mappings only, Task A form)
            if m['review_table'] != root or m['review_column'] not in dims:
                continue
            ov = o.get(OMICOL.get(m['omi_column'], m['omi_column']))
            if ov in (None, '', 'NA', 'N/A', '-'):
                continue
            res = cmp_num(str(ov), str(dims[m['review_column']]))
            if res == 'different':
                cell = f'Items!{col_letter.get(OMICOL[m["omi_column"]], "?")}{o["_row"]}'
                took.append((m['review_column'], dims[m['review_column']], ov, cell))
                dims[m['review_column']] = float(ov) if re.fullmatch(r'\s*\d*\.?\d+\s*', str(ov)) else ov
        cells = []
        for tc, bc in BR.get(root, {}).items():                    # Brennan check on clearly paired columns
            if tc in dims and x.get('brennan_values') and x['brennan_values'].get(bc) not in (None, ''):
                cells.append((tc, dims[tc], bc, x['brennan_values'][bc], cmp_num(str(dims[tc]), str(x['brennan_values'][bc]))))
        agree = [c for c in cells if c[4] in ('equal', 'rounding_only')]
        differ = [c for c in cells if c[4] == 'different']
        lh = any(LEN_HEX(c[0]) and 'HEX' in c[0] or c[0].startswith(('Y', 'W@')) for c in agree) and any(LEN_HEX(c[0]) and 'HEX' not in c[0] and not c[0].startswith(('Y', 'W@')) for c in agree)
        if took:
            new_status = 'ASSUMED'
        elif cells and not differ and lh:
            new_status = 'VERIFIED' if x['status'] in ('ASSUMED', 'VERIFIED', 'VERIFIED-CORE', 'VERIFIED-LEGS') else x['status']
        else:
            new_status = x['status']
        why = []
        if took:
            why.append('OMi dims first (user 2026-09-25): ' + '; '.join(f'{c}: OMi WebsitePartsInfo2026.xlsx {cell} = {nv} (table had {ov_})' for c, ov_, nv, cell in took))
        if cells:
            why.append(f'Brennan TFA {x["brennan"]}: agrees on ' + (', '.join(c[0] for c in agree) or 'nothing') +
                       ('; DIFFERS on ' + '; '.join(f'{c[0]} {c[1]} vs Brennan {c[2]} {c[3]}' for c in differ) + ' (built to the dimension source, s6)' if differ else ''))
        elif x['brennan']:
            why.append(f'Brennan TFA {x["brennan"]} printed, no clearly paired column')
        else:
            why.append('no Brennan catalog row')
        rec.update(new_scope='BUILD', new_status=new_status, omi_taken=[dict(col=c, table=a, omi=b, cell=d) for c, a, b, d in took],
                   brennan_cells=[dict(col=c[0], value=c[1], brennan_col=c[2], brennan=c[3], result=c[4]) for c in cells], why=' | '.join(why))
        tag = '2026-10-16: OMi sells this part (website, two-pass crawl 2026-10-16); the 2026-09-23 crawl had dropped the SKU, so it was DROP'
        changes.append([tab, x['row'], '$PRP@ScopeAction', x['scope'], 'BUILD', tag])
        changes.append([tab, x['row'], '$PRP@OMiSKU', '', sku, tag])
        for c, a, b, d in took:
            changes.append([tab, x['row'], c, a, b, f'OMi dims first (user 2026-09-25): OMi WebsitePartsInfo2026.xlsx {d} = {b} (table had {a}) [Task A form]'])
        if new_status != x['status']:
            changes.append([tab, x['row'], '$PRP@DataStatus', x['status'], new_status, rec['why']])
        changes.append([tab, x['row'], '$COMMENT (append)', '',
                        '2026-10-16: BUILD - the DROP above is void: OMi sells this part, the 2026-09-23 crawl had dropped its SKU | ' + rec['why'],
                        'Brennan check / OMi values, 2026-10-16'])
        recs.append(rec)
    with open(os.path.join(HERE, 'CHANGES.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['review table', 'row (config name)', 'column', 'old', 'new', 'reason'])
        w.writerows(changes)
    json.dump(recs, open(os.path.join(HERE, 'rows77.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    with37 = [r for r in recs if r['row']]
    print('37:', collections.Counter(r['new_status'] for r in with37), '| took OMi values:', sum(1 for r in with37 if r['omi_taken']),
          '| Brennan differs on some cell:', sum(1 for r in with37 if any(c['result'] == 'different' for c in r['brennan_cells'])))
    print('40:', collections.Counter(('OMi values' if r['omi_values'] else 'no OMi values') + (' + Brennan' if r['brennan'] else '') for r in recs if not r['row']))
    print(len(changes), 'change lines ->', os.path.join(HERE, 'CHANGES.csv'))
    for r in with37:
        print(f'  {r["sku"]:<22} {r["old_status"]:<14} -> {r["new_status"]:<9} OMi {len(r["omi_taken"])}  BR ' +
              ' '.join(f'{c["col"]}={c["result"][0]}' for c in r['brennan_cells']))


if __name__ == '__main__':
    main()
