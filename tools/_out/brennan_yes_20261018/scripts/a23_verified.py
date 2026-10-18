"""A23 (1), user 2026-10-18: the 15 rows filled from OMi's 2026-10-18 answers are VERIFIED. Edits the Brennan stage tables; logs to
stage/CHANGES.csv."""
import os, csv, openpyxl

STAGE = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\stage\04_DESIGN_TABLES'
OMI_CH = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\omi_answers_20261018\CHANGES.csv'
rows = {(c['table'], c['part_number']) for c in csv.DictReader(open(OMI_CH, encoding='utf-8'))
        if c['column'] == '$PRP@DataStatus' and c['new'] == 'ASSUMED'}
assert len(rows) == 15, rows
log = []
for t in sorted({t for t, _ in rows}):
    p = os.path.join(STAGE, t)
    wb = openpyxl.load_workbook(p); ws = wb.active
    hdr = {c.value: c.column for c in ws[2] if c.value is not None}
    for tt, pn in sorted(rows):
        if tt != t:
            continue
        r = [c.row for c in ws['A'] if c.value == pn][0]
        cell = ws.cell(r, hdr['$PRP@DataStatus']); old = cell.value
        assert old == 'ASSUMED', (t, pn, old)
        cell.value = 'VERIFIED'
        cm = ws.cell(r, hdr['$COMMENT'])
        cm.value = (cm.value + ' | ' if cm.value else '') + 'VERIFIED by user decision 2026-10-18 (A23-1: OMi\'s own answer counts as verified)'
        log.append((t, pn, r, '$PRP@DataStatus', cell.coordinate, old, 'VERIFIED', 'user 2026-10-18 A23 (1)'))
    wb.save(p)
with open(os.path.join(os.path.dirname(STAGE), 'CHANGES.csv'), 'a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(log)
print(len(log), 'rows -> VERIFIED')
