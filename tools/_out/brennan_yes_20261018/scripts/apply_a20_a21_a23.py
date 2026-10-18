"""Apply the user's answers of 2026-10-18 to the stage tables (no SolidWorks; built masters change only when batch 17 is rebuilt):
  A20 - 1404 nut face W@HEX = OMi overall length (23 configurations)
  A21 - 1404 bores back to Air-Way (18 cells)
  A23 (2) - OMi and Air-Way agree -> VERIFIED: the clean candidates of a19_omi_diffs_20261018/A23_verified_candidates.csv
            (all_agree yes, ASSUMED, no cell on an unsettled reading (note empty), not 2404)
Every changed cell is checked against the value the CSV says it holds now; logs to stage/CHANGES.csv."""
import os, csv, collections, openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
STAGE = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\stage')
A = os.path.join(ROOT, r'tools\_out\a19_omi_diffs_20261018')
rd = lambda f: list(csv.DictReader(open(os.path.join(A, f), encoding='utf-8-sig')))
books, log = {}, []


def sheet(t):
    if t not in books:
        p = os.path.join(STAGE, '04_DESIGN_TABLES', f'DesignTable_{t}.xlsx')
        wb = openpyxl.load_workbook(p); ws = wb.active
        books[t] = (p, wb, ws, {c.value: c.column for c in ws[2] if c.value is not None})
    return books[t]


def cell_of(t, pn, h):
    _, _, ws, hdr = sheet(t)
    r = [c.row for c in ws['A'] if c.value == pn]
    assert len(r) == 1, (t, pn, r)
    return ws.cell(r[0], hdr[h]), r[0]


def note(t, pn, text):
    c, _ = cell_of(t, pn, '$COMMENT')
    c.value = (c.value + ' | ' if c.value else '') + text


for x in rd('A20_1404_nutface.csv'):
    c, r = cell_of(x['table'], x['config'], x['column'])
    assert abs(float(c.value) - float(x['current_value'])) < 1e-6, (x, c.value)
    old = c.value; c.value = float(x['omi_value'])
    note(x['table'], x['config'], f"A20 (user 2026-10-18): {x['column']} {old} -> OMi {x['omi_value']} ({x['omi_cell']}; nut face at OMi's overall length)")
    log.append((f"DesignTable_{x['table']}.xlsx", x['config'], r, x['column'], c.coordinate, old, c.value, f"A20 user 2026-10-18: OMi WebsitePartsInfo2026.xlsx {x['omi_cell']}"))
for x in rd('A21_1404_bores.csv'):
    c, r = cell_of(x['table'], x['config'], x['column'])
    assert abs(float(c.value) - float(x['current_value'])) < 1e-6, (x, c.value)
    old = c.value; c.value = float(x['airway_value'])
    note(x['table'], x['config'], f"A21 (user 2026-10-18): {x['column']} {old} (OMi, batch 14) -> Air-Way {x['airway_value']} ({x['airway_printed_check']})")
    log.append((f"DesignTable_{x['table']}.xlsx", x['config'], r, x['column'], c.coordinate, old, c.value, f"A21 user 2026-10-18: Air-Way {x['airway_printed_check']}"))
n23 = collections.Counter()
for x in rd('A23_verified_candidates.csv'):
    if x['all_agree'] != 'yes' or x['current_DataStatus'] != 'ASSUMED' or x['note'].strip() or x['table'].startswith('2404'):
        continue
    c, r = cell_of(x['table'], x['config'], '$PRP@DataStatus')
    if c.value != 'ASSUMED':
        continue
    c.value = 'VERIFIED'; n23[x['table']] += 1
    note(x['table'], x['config'], f"A23 (user 2026-10-18): VERIFIED - OMi = Air-Way on {x['cells_agree']}")
    log.append((f"DesignTable_{x['table']}.xlsx", x['config'], r, '$PRP@DataStatus', c.coordinate, 'ASSUMED', 'VERIFIED', f"A23 user 2026-10-18: OMi = Air-Way on {x['cells_agree']}"))

for p, wb, ws, hdr in books.values():
    wb.save(p)
with open(os.path.join(STAGE, 'CHANGES.csv'), 'a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(log)
print('A20/A21 cells:', sum(1 for l in log if l[3] != '$PRP@DataStatus'), '| A23 VERIFIED rows:', sum(n23.values()), dict(n23))
