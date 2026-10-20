"""Applies revert_list.csv to a stage copy of the live 04_DESIGN_TABLES (stage/04_DESIGN_TABLES; the live tables are not touched).
Per cell: checks the cell still holds the 'current' value, writes the Air-Way value, appends the reason to $COMMENT and $PRP@AxialSource
(the OMi / Brennan value is kept there, s6 convention). DataStatus: unchanged (the row goes back to its Air-Way state; VERIFIED-LEGS /
VERIFIED-CORE rows were verified on their Air-Way values), except rows whose VERIFIED -> ASSUMED was logged as caused by the OMi values
(brennan_yes_20261018/stage/CHANGES.csv): those go back to VERIFIED. Task A (2026-09-25) set ASSUMED without a cloud copy of the old
status - those rows stay ASSUMED (old status: tools/_out/omi_apply_20260925/originals_before_apply on the PC).
Logs every cell to stage/CHANGES.csv."""
import csv, os, shutil, collections, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
ST = os.path.join(A, 'stage', '04_DESIGN_TABLES')
TAG = 'OMi 2026-10-20 (Triveni): Air-Way over Brennan where Air-Way gives a value, incl. the numbers of OMi\'s website parts file (= Brennan data)'
if not os.path.exists(ST):
    shutil.copytree(os.path.join(H, '04_DESIGN_TABLES'), ST)
rows = list(csv.DictReader(open(os.path.join(A, 'revert_list.csv'), encoding='utf-8')))
books, log, n = {}, [], collections.Counter()
def sheet(t):
    if t not in books:
        p = os.path.join(ST, f'DesignTable_{t}.xlsx'); wb = openpyxl.load_workbook(p); ws = wb.worksheets[0]
        hr = next(r for r in range(1, 6) if '$PRP@PartNo' in [c.value for c in ws[r]])
        books[t] = (p, wb, ws, {c.value: c.column for c in ws[hr] if c.value is not None}, hr)
    return books[t]
touched = collections.defaultdict(list)
for x in rows:
    t, pn, col = x['root'], x['cfg'], x['col']
    p, wb, ws, hdr, hr = sheet(t)
    rr = [c.row for c in ws['A'] if c.row > hr and str(c.value) == pn]
    assert len(rr) == 1, (t, pn, rr)
    c = ws.cell(rr[0], hdr[col]); old = c.value
    assert abs(float(old) - float(x['current'])) < 1e-6, (t, pn, col, old, x['current'])
    new = float(x['target']); c.value = new
    cm = ws.cell(rr[0], hdr['$COMMENT'])
    cm.value = (str(cm.value) + ' | ' if cm.value else '') + f'2026-10-20 Air-Way first: {col} OMi/Brennan {old} -> Air-Way {new:g}'
    ax = ws.cell(rr[0], hdr['$PRP@AxialSource'])
    ax.value = (str(ax.value) if ax.value else '') + f'; {col}: Air-Way {new:g} ({x["verified"]}; OMi file / Brennan {old}) [{TAG}]'
    log.append((f'DesignTable_{t}.xlsx', pn, rr[0], col, c.coordinate, old, new, f'Air-Way first 2026-10-20 ({x["verified"]})'))
    n[t] += 1; touched[(t, pn, rr[0])].append(col)
prev = {}
for x in csv.reader(open(os.path.join(H, 'tools', '_out', 'brennan_yes_20261018', 'stage', 'CHANGES.csv'), encoding='utf-8')):
    if len(x) > 7 and x[3] == '$PRP@DataStatus' and x[5] == 'VERIFIED' and x[6] == 'ASSUMED' and ('A19' in x[7] or 'pending OMi' in x[7]):
        prev[(x[0][12:-5], x[1])] = x[7]
down = dim = 0
for (t, pn, r), cols in touched.items():
    p, wb, ws, hdr, hr = sheet(t)
    s = ws.cell(r, hdr['$PRP@DataStatus'])
    if (t, pn) in prev and s.value == 'ASSUMED':
        log.append((f'DesignTable_{t}.xlsx', pn, r, '$PRP@DataStatus', s.coordinate, s.value, 'VERIFIED', 'Air-Way first: back to VERIFIED (downgrade was: ' + prev[(t, pn)][:120] + ')'))
        s.value = 'VERIFIED'; down += 1
    if '$PRP@DimSource' in hdr:
        d = ws.cell(r, hdr['$PRP@DimSource'])
        if d.value == 'OMI':
            print('  DimSource OMI row touched (left as is, check):', t, pn, cols); dim += 1
for p, wb, ws, hdr, hr in books.values():
    wb.save(p)
with open(os.path.join(A, 'stage', 'CHANGES.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['table', 'part_number', 'excel_row', 'column', 'cell', 'old', 'new', 'source']); w.writerows(log)
print('cells', sum(n.values()), 'rows', len(touched), 'tables', len(n), '| ASSUMED->VERIFIED (logged OMi downgrades undone)', down, '| DimSource OMI rows', dim)
