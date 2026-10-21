"""apply_tapdrill.py (2026-10-21): fill EMPTY female-pipe tap-drill cells of not-ready BUILD rows in the stage with Air-Way's per-size tap
drill - A1 (user 2026-10-18: "Air-Way's per-size tap drill where OMi gives none": -02 0.33, -04 0.43, -06 0.57, -08 0.70, -12 0.91,
-16 1.14, -20 1.48) and A9 (-24 / -32, settled 2026-10-21 by BRENNAN_5405-24-24 / -32-32: Brennan 1.734 / 2.218 -> the nearest Air-Way
values 1.72 / 2.20). Run after apply_cells.py, before promote_test.py.
Which end a TAPDRILL column belongs to differs per table (TAPDRILL@BORE = end B on 5406, TAPDRILL1 / TAPDRILL2 = ends A / B on 5000 ...):
per (table, column) the dash position is the one whose A1 value matches the column on >= 80 % (and >= 3) of the filled rows; a column with
no clear position is left alone. Rows keep their DataStatus here (promote_test.py decides); the source note goes into $PRP@AxialSource
('[A1/A9 TAPDRILL 2026-10-21: <col>]') and $COMMENT. Writes tapdrill.csv."""
import os, re, csv, glob, collections
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
A1 = {2: 0.33, 4: 0.43, 6: 0.57, 8: 0.70, 12: 0.91, 16: 1.14, 20: 1.48, 24: 1.72, 32: 2.20}
NOT_READY = {norm(l) for l in open(J('tools', '_out', 'sources_20261021', 'not_ready_1022.txt')) if l.strip()}
log = []
for path in sorted(glob.glob(os.path.join(A, 'stage', '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))):
    if path.endswith('_SW2.xlsx'):
        continue
    wb = openpyxl.load_workbook(path); ws = wb.worksheets[0]
    hr = next((i for i in range(1, 7) if any(c.value == '$PRP@PartNo' for c in ws[i])), None)
    if hr is None:
        continue
    head = {c.value: c.column for c in ws[hr] if c.value}
    tcols = [c for c in head if re.match(r'^TAPDRILL', str(c))]
    if not tcols:
        continue
    rows = []
    for i in range(hr + 1, ws.max_row + 1):
        pn = ws.cell(row=i, column=head['$PRP@PartNo']).value
        if pn:
            sku = ws.cell(row=i, column=head['$PRP@OMiSKU']).value if '$PRP@OMiSKU' in head else None
            rows.append((i, norm(sku or pn), [int(x) for x in re.findall(r'-(\d\d)(?=-|X|$)', str(pn))]))
    changed = False
    for col in tcols:
        best = None
        for k in range(4):
            vals = [(ws.cell(row=i, column=head[col]).value, d[k]) for i, p, d in rows if len(d) > k and d[k] in A1 and isnum(ws.cell(row=i, column=head[col]).value)]
            ok = sum(1 for v, d in vals if abs(v - A1[d]) <= 0.025)
            if vals and ok >= 3 and ok >= 0.8 * len(vals) and (best is None or ok > best[1]):
                best = (k, ok, len(vals))
        if best is None:
            # equal-dash parts (5602-12-12-12-FG ...): every port has the same size, the end position does not matter (2026-10-21)
            for i, p, d in rows:
                if p in NOT_READY and d and len(set(d)) == 1 and d[0] in A1 and not isnum(ws.cell(row=i, column=head[col]).value) and \
                        str(ws.cell(row=i, column=head['$PRP@ScopeAction']).value or '').upper() == 'BUILD':
                    ws.cell(row=i, column=head[col]).value = A1[d[0]]; changed = True
                    ax = ws.cell(row=i, column=head['$PRP@AxialSource']); ax.value = f'[A1/A9 TAPDRILL 2026-10-21: {col}] ' + (ax.value or '')
                    log.append(dict(table=os.path.basename(path), column=col, part=p, value=A1[d[0]], result='written (equal-dash part)'))
            log.append(dict(table=os.path.basename(path), column=col, part='', value='', result='no clear end position - equal-dash rows only')); continue
        k = best[0]
        for i, p, d in rows:
            if p not in NOT_READY or len(d) <= k or d[k] not in A1:
                continue
            if str(ws.cell(row=i, column=head.get('$PRP@ScopeAction', 0) or 1).value or '').upper() != 'BUILD':
                continue
            c = ws.cell(row=i, column=head[col])
            if isnum(c.value):
                continue
            c.value = A1[d[k]]; changed = True
            ax = ws.cell(row=i, column=head['$PRP@AxialSource'])
            ax.value = f'[A1/A9 TAPDRILL 2026-10-21: {col}] ' + (ax.value or '')
            if '$COMMENT' in head:
                cm = ws.cell(row=i, column=head['$COMMENT'])
                note = (f'{col} = Air-Way per-size tap drill -{d[k]:02d} {A1[d[k]]} (A1' +
                        (', A9: Brennan 5405-24-24 / -32-32 STEPs 1.734 / 2.218 -> nearest Air-Way 1.72 / 2.20' if d[k] in (24, 32) else '') + ')')
                cm.value = (cm.value + ' | ' if cm.value else '') + note
            log.append(dict(table=os.path.basename(path), column=col, part=p, value=A1[d[k]], result=f'written (dash position {k + 1}, {best[1]}/{best[2]} rows agree)'))
    if changed:
        wb.save(path)
with open(os.path.join(A, 'tapdrill.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'column', 'part', 'value', 'result']); w.writeheader(); w.writerows(log)
print(collections.Counter(x['result'].split(' (')[0] for x in log), '| rows', len({x['part'] for x in log if x['part']}))

# the rows that got a tap drill but no Brennan cell join rows.csv, so promote_test.py tries them too
rows_csv = os.path.join(A, 'rows.csv')
rws = list(csv.DictReader(open(rows_csv, encoding='utf-8'))); have = {r['part'] for r in rws}
for t, p in sorted({(x['table'], x['part']) for x in log if x['part']}):
    if p in have:
        continue
    ws = openpyxl.load_workbook(os.path.join(A, 'stage', '04_DESIGN_TABLES', t), read_only=True, data_only=True).worksheets[0]
    rs = list(ws.iter_rows(values_only=True)); hi = next(i for i, r in enumerate(rs[:6]) if r and '$PRP@PartNo' in r); h = rs[hi]
    for r in rs[hi + 1:]:
        d = dict(zip(h, r))
        if r[0] and norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo')) == p:
            rws.append(dict(root=t[12:-5], part=p, cells=0, status_before=d.get('$PRP@DataStatus'), status_after=d.get('$PRP@DataStatus'),
                            still_missing='(tap drill only)')); have.add(p); break
with open(rows_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rws[0])); w.writeheader(); w.writerows(rws)
