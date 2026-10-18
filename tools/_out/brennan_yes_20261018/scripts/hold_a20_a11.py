"""Follow-up of A19 / A20 (2026-10-18), found by regenerating from the stage:
- A20 (OMi overall length as the 1404 nut face) breaks the measured NPSM swivel on 5 sizes ("nut/stem axial order broken for W-L ...",
  gen_straight2): OMi gives no stem-tip length (no L 1 for 1404), so OMi W cannot be paired with a matching L. These 5 go back to
  Air-Way W and are HELD for the user: 1404-02-02, -04-04, -16-12, -20-24, -24-20 (the last two look swapped in OMi's file: its
  SAE cross-reference column names 24-20 on the 1404-20-24 row and 20-24 on the 1404-24-20 row).
- A19 put OMi's 6404-06-08 D1 0.531 in, which is wider than the -06 port drill 0.50 (generator BLOCKED) -> A11 (cap at the port drill):
  back to 0.50."""
import os, csv, openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
STAGE = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\stage')
A20 = {x['config']: x for x in csv.DictReader(open(os.path.join(ROOT, r'tools\_out\a19_omi_diffs_20261018\A20_1404_nutface.csv'), encoding='utf-8-sig'))}
log = []


def fix(t, pn, h, expect, new, why):
    p = os.path.join(STAGE, '04_DESIGN_TABLES', f'DesignTable_{t}.xlsx')
    wb = openpyxl.load_workbook(p); ws = wb.active
    hdr = {c.value: c.column for c in ws[2] if c.value is not None}
    r = [c.row for c in ws['A'] if c.value == pn][0]
    c = ws.cell(r, hdr[h]); assert abs(c.value - expect) < 1e-6, (pn, h, c.value, expect)
    c.value = new
    cm = ws.cell(r, hdr['$COMMENT']); cm.value = (cm.value + ' | ' if cm.value else '') + why
    wb.save(p)
    log.append((f'DesignTable_{t}.xlsx', pn, r, h, c.coordinate, expect, new, why))


for pn in ('1404-02-02', '1404-04-04', '1404-16-12', '1404-20-24', '1404-24-20'):
    x = A20[pn]
    fix('1404', pn, 'W@HEX', float(x['omi_value']), float(x['current_value']),
        f"A20 HELD (2026-10-18): OMi overall length {x['omi_value']} as nut face breaks the measured NPSM swivel (W-L out of range; OMi gives no "
        f"stem-tip length to pair) -> kept at Air-Way W {x['current_value']}; user to decide")
fix('6404', '6404-06-08', 'D1@BORE', 0.531, 0.5, 'A11 (user 2026-10-18): OMi bore 0.531 wider than the -06 port drill 0.50 -> capped at 0.50 (report to OMi)')
with open(os.path.join(STAGE, 'CHANGES.csv'), 'a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(log)
print(len(log), 'cells reverted / capped')
