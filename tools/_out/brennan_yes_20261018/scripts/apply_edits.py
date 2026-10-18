"""apply_edits.py <edits.csv>: change NON-empty stage cells (table,config,column,old,new,why), each old value asserted; for decisions the
user already took (e.g. A11 bore caps). Logs to stage/CHANGES.csv."""
import os, sys, csv, openpyxl

STAGE = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\stage'
log = []
for x in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')):
    p = os.path.join(STAGE, '04_DESIGN_TABLES', f"DesignTable_{x['table']}.xlsx")
    wb = openpyxl.load_workbook(p); ws = wb.active
    hdr = {c.value: c.column for c in ws[2] if c.value is not None}
    r = [c.row for c in ws['A'] if c.value == x['config']][0]
    c = ws.cell(r, hdr[x['column']])
    assert abs(float(c.value) - float(x['old'])) < 1e-6, (x, c.value)
    c.value = float(x['new'])
    cm = ws.cell(r, hdr['$COMMENT']); cm.value = (cm.value + ' | ' if cm.value else '') + f"{x['column']} {x['old']} -> {x['new']}: {x['why']}"
    wb.save(p)
    log.append((f"DesignTable_{x['table']}.xlsx", x['config'], r, x['column'], c.coordinate, x['old'], x['new'], x['why']))
with open(os.path.join(STAGE, 'CHANGES.csv'), 'a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(log)
print(len(log), 'cells edited')
