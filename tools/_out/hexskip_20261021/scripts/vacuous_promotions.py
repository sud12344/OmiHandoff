"""vacuous_promotions.py (2026-10-21): rows apply_cells.py promoted MISSING -> ASSUMED in a table where its 'required columns' list was EMPTY
(no row of the table in a shipped SW2 table, so 'required = filled on >= 90 % of the shipped rows' required nothing) - the 6810 case.
Same logic as apply_cells.py (shipped = every SW2 table of <ref 04_DESIGN_TABLES> at stage time). Lists each such row's empty numeric cells.
  python vacuous_promotions.py <folder holding the 04_DESIGN_TABLES apply_cells.py read> > vacuous_promotions.txt"""
import os, re, sys, csv, glob, openpyxl
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..', '..'))
BC = os.path.join(ROOT, 'tools', '_out', 'brennancad_20261021'); REF = sys.argv[1]
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
shipped = set()
for p in glob.glob(os.path.join(REF, '04_DESIGN_TABLES', '*_SW2.xlsx')):
    rs = list(openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)); h = rs[0]
    for r in rs[1:]:
        if r and r[0]:
            d = dict(zip(h, r)); shipped.add(norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or r[0]))
pro = [r for r in csv.DictReader(open(os.path.join(BC, 'rows.csv'), encoding='utf-8')) if r['status_before'] == 'MISSING' and r['status_after'] == 'ASSUMED']
n = 0
for root in sorted({r['root'] for r in pro}):
    p = os.path.join(BC, 'stage', 'orfs_tables' if root.startswith('FS') else '04_DESIGN_TABLES', f'DesignTable_{root}.xlsx')
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    hr = next(i for i in range(1, 7) if any(c.value == '$PRP@PartNo' for c in ws[i]))
    head = {c.value: c.column for c in ws[hr] if c.value}
    keys = {}
    for i in range(hr + 1, ws.max_row + 1):
        pn = ws.cell(row=i, column=head['$PRP@PartNo']).value
        if pn:
            sku = ws.cell(row=i, column=head['$PRP@OMiSKU']).value if '$PRP@OMiSKU' in head else None
            keys.setdefault(norm(sku or pn), i)
    if any(k in shipped for k in keys):
        continue
    numcols = [k for k in head if k and not str(k).startswith('$')]
    for r in pro:
        if r['root'] != root: continue
        i = keys[norm(r['part'])]
        empty = [c for c in numcols if not isnum(ws.cell(row=i, column=head[c]).value)]
        st = ws.cell(row=i, column=head['$PRP@DataStatus']).value
        n += 1; print(f"{root:7} {r['part']:22} now {st:8} empty: {', '.join(empty) or '-'}")
print(f'{n} rows promoted with an empty required-column list')
