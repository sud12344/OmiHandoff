"""revert_brennan.py <04_DESIGN_TABLES folder> [--apply]

Undo of the 2026-10-18 Brennan decision, should the user change it: every row with $PRP@DimSource = BRENNAN goes back to
DataStatus MISSING (its values stay visible, the generators skip MISSING rows). Without --apply it only lists the rows."""
import os, sys, glob, openpyxl

folder = sys.argv[1]
apply = '--apply' in sys.argv
n = 0
for p in sorted(glob.glob(os.path.join(folder, 'DesignTable_*.xlsx'))):
    if p.endswith('_SW2.xlsx'):
        continue
    wb = openpyxl.load_workbook(p); ws = wb.active
    hdr = {c.value: c.column for c in ws[2] if c.value is not None}
    if '$PRP@DimSource' not in hdr:
        continue
    hit = False
    for r in range(3, ws.max_row + 1):
        if ws.cell(r, hdr['$PRP@DimSource']).value == 'BRENNAN':
            n += 1; hit = True
            print(os.path.basename(p), ws.cell(r, 1).value, ws.cell(r, hdr['$PRP@DataStatus']).value, '-> MISSING' if apply else '')
            if apply:
                ws.cell(r, hdr['$PRP@DataStatus']).value = 'MISSING'
                c = ws.cell(r, hdr['$COMMENT']); c.value = ((c.value + ' | ') if c.value else '') + 'Brennan decision reverted: row back to MISSING'
    if apply and hit:
        wb.save(p)
print(n, 'BRENNAN rows', '(set MISSING)' if apply else '(list only)')
