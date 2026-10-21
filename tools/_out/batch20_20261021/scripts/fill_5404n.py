"""fill_5404n.py (batch 20, 2026-10-21): the 4 long 5404-N nipples get the A4 transfer their siblings already carry (user 2026-10-18 A4 "YES"):
L from the part number, bar dia (COD) / bores / thread majors from the Air-Way nipple of the same dash (the values every sibling row of that dash
holds: -06 = 5404-N-06-06-X1, -08 = 5404-N-08-08-X3). Writes root20/04_DESIGN_TABLES/DesignTable_5404N.xlsx (copy of the live table) + CHANGES.csv."""
import csv, os, re, shutil, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
S = os.path.join(H, 'tools', '_out', 'batch20_20261021')
DT = os.path.join(S, 'root20', '04_DESIGN_TABLES'); os.makedirs(DT, exist_ok=True)
src = os.path.join(H, '04_DESIGN_TABLES', 'DesignTable_5404N.xlsx'); dst = os.path.join(DT, 'DesignTable_5404N.xlsx')
shutil.copy2(src, dst)
wb = openpyxl.load_workbook(dst); ws = wb.worksheets[0]
hi = next(r for r in range(1, 8) if any(ws.cell(r, c).value == '$PRP@PartNo' for c in range(1, ws.max_column + 1)))
col = {ws.cell(hi, c).value: c for c in range(1, ws.max_column + 1) if ws.cell(hi, c).value}
SIB = {'06': '5404-N-06X3.000', '08': '5404-N-08X3.500'}
AW = {'06': '5404-N-06-06-X1', '08': '5404-N-08-08-X3'}
TH = {'06': '3/8-18 x 3/8-18 NPTF', '08': '1/2-14 x 1/2-14 NPTF'}
rows = {ws.cell(r, 1).value: r for r in range(hi + 1, ws.max_row + 1) if ws.cell(r, 1).value}
log = []
for pn in ('5404-N-06X4.500', '5404-N-06X5.500', '5404-N-08X2.500', '5404-N-08X5.500'):
    r = rows[pn]; dash, L = re.match(r'5404-N-(\d\d)X([\d.]+)$', pn).groups(); L = float(L); s = rows[SIB[dash]]
    new = {'L@DRIVE': L}
    for k in ('COD@REF', 'D1@BORE', 'D2@BORE', 'THDMAJ_A1@DRIVE', 'THDMAJ_A2@DRIVE'):
        new[k] = ws.cell(s, col[k]).value
    new['$PRP@Threads'] = f'{TH[dash]}, cut length {L:g} in'
    new['$PRP@DataStatus'] = 'ASSUMED'
    old_c = ws.cell(r, col['$COMMENT']).value or ''
    new['$COMMENT'] = (old_c + ' | ' if old_c else '') + (
        f'2026-10-21 (batch 20): L from the part number, bar dia and bores from the Air-Way nipple {AW[dash]} (A4 yes 2026-10-18), as every '
        f'{dash} sibling row; MISSING -> ASSUMED')
    for k, v in new.items():
        c = ws.cell(r, col[k]); old = c.value
        if old != v:
            c.value = v; log.append([pn, k, old, v, f'A4 transfer from {SIB[dash]} / Air-Way {AW[dash]}' if '@' in k else 'batch 20'])
wb.save(dst)
with open(os.path.join(S, 'CHANGES.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['cfg', 'column', 'old', 'new', 'source']); w.writerows(log)
print(len(log), 'cells')
