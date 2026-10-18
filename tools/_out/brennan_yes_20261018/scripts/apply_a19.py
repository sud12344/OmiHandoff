"""A19, user 2026-10-18: "apply groups 1, 2 and 3 (accept the open Q36 readings too), skipping 6504 L13 and holding the 3 swapped rows".
Applies a19_omi_diffs_20261018/A19_changes.csv (certain) + A19_uncertain_readings.csv (settled + open) to the stage tables. Each cell is
checked against the value the CSV says it holds now. A row that takes an OMi value differing from Air-Way cannot be VERIFIED (OMi + Air-Way
disagree there) -> any such row marked VERIFIED goes back to ASSUMED. Logs to stage/CHANGES.csv."""
import os, csv, collections, openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
STAGE = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\stage')
A = os.path.join(ROOT, r'tools\_out\a19_omi_diffs_20261018')
HOLD = {'2503-04-08-FG', '2503-10-12-FG', '5500-16-12-FG'}           # look leg-swapped: held
rows = [dict(x, grp='1 certain') for x in csv.DictReader(open(os.path.join(A, 'A19_changes.csv'), encoding='utf-8-sig'))]
for x in csv.DictReader(open(os.path.join(A, 'A19_uncertain_readings.csv'), encoding='utf-8-sig')):
    rows.append(dict(x, grp='3 open' if x['reading_status'].startswith('open') else '2 settled'))
books, log, skipped, n = {}, [], [], collections.Counter()


def sheet(t):
    if t not in books:
        p = os.path.join(STAGE, '04_DESIGN_TABLES', f'DesignTable_{t}.xlsx')
        wb = openpyxl.load_workbook(p); ws = wb.active
        books[t] = (p, wb, ws, {c.value: c.column for c in ws[2] if c.value is not None})
    return books[t]


touched = set()
for x in rows:
    t, pn, h = x['table'], x['config'], x['column']
    if pn in HOLD:
        skipped.append((pn, h, 'held: looks leg-swapped')); continue
    if t == '6504' and h.startswith('L13'):
        skipped.append((pn, h, 'skipped: 6504 L13 (OMi gives no L14)')); continue
    _, _, ws, hdr = sheet(t)
    r = [c.row for c in ws['A'] if c.value == pn]
    assert len(r) == 1, (t, pn, r)
    c = ws.cell(r[0], hdr[h])
    assert abs(float(c.value) - float(x['current_value'])) < 1e-6, (t, pn, h, c.value, x['current_value'])
    old = c.value; c.value = float(x['omi_value'])
    cm = ws.cell(r[0], hdr['$COMMENT'])
    cm.value = (cm.value + ' | ' if cm.value else '') + f"A19 (user 2026-10-18, group {x['grp']}): {h} {old} -> OMi {x['omi_value']} ({x['omi_cell']}, {x['mapping_id']})"
    ax = ws.cell(r[0], hdr['$PRP@AxialSource'])
    ax.value = (ax.value or '') + f"; {h}: OMi WebsitePartsInfo2026.xlsx {x['omi_cell']} = {x['omi_value']} (table had {old}) [user 2026-10-18 A19]"
    log.append((f'DesignTable_{t}.xlsx', pn, r[0], h, c.coordinate, old, c.value, f"A19 group {x['grp']}: OMi {x['omi_cell']} ({x['mapping_id']})"))
    n[(t, x['grp'])] += 1; touched.add((t, pn, r[0]))
down = 0
for t, pn, r in touched:
    _, _, ws, hdr = sheet(t)
    s = ws.cell(r, hdr['$PRP@DataStatus'])
    if s.value == 'VERIFIED':
        s.value = 'ASSUMED'; down += 1
        log.append((f'DesignTable_{t}.xlsx', pn, r, '$PRP@DataStatus', s.coordinate, 'VERIFIED', 'ASSUMED', 'A19: now carries an OMi value that differs from Air-Way'))
for p, wb, ws, hdr in books.values():
    wb.save(p)
with open(os.path.join(STAGE, 'CHANGES.csv'), 'a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(log)
print('cells applied:', sum(n.values()), 'rows:', len(touched), '| VERIFIED->ASSUMED:', down, '| skipped:', len(skipped))
for k in sorted(n): print('  ', k, n[k])
for s in skipped: print('  skip', s)
