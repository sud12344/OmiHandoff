"""pending_omi.py (wave 3 adapters, 2026-10-18): OMi values that DIFFER from the table on the 37 adapters77 rows after edits_77 is applied
(found by a patched copy of the A19 / A23 comparison, scripts/a23_check_copy_of_a19_diff.py -> a23_check/A23_verified_candidates.csv).
The 2026-10-16 staging took OMi values only on the audit's 'certain' mappings (Task A form); these use batch-15-settled / open readings or a
rounding call. Under A19 ("first tell me which configs differ then update all if i approve") they are LISTED, not applied.
Writes pending_omi_A19.csv: table,config,column,table_now,omi,omi_cell,brennan,proposed,why"""
import os, csv, json, openpyxl
from openpyxl.utils import get_column_letter
R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
OUT = os.path.join(R, r'tools\_out\brennan_yes_20261018\wave3\adapters')
wb = openpyxl.load_workbook(os.path.join(R, r'07_RAW_EXTRACTS\omi_dimensions\WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)
it = wb['Items'].iter_rows(values_only=True); OH = next(it)
OMI = {}
for i, r in enumerate(it, start=2):
    if r[0]:
        OMI.setdefault(str(r[0]).strip(), (i, dict(zip(OH, r))))
L = {h: get_column_letter(j + 1) for j, h in enumerate(OH) if h}
D = json.load(open(os.path.join(R, r'tools\_out\brennan_catalog_20261001\catalog_verified.json'), encoding='utf-8'))
CAT = {r['pn']: (t, r) for t in D['tables'] for r in t['rows']}
# (table, config as in the table, column, table value now, OMi part number, OMi header, Brennan pn, Brennan column, note)
ITEMS = [
    ('2705', '2705-06-06', 'C5HEX@HEX', 1.0, '2705-06-06', 'Hex Flat', '2705-06-06', 'C1 HEX', 'body hex; certain mapping on the built 2705 rows (impact M057)'),
    ('6405', '6405-16-06-O', 'L31@DRIVE', 1.0, '6405-16-06-O', 'Overall Length', '6405-16-06-O', 'L LGTH',
     'Air-Way printed "1" (no decimals); the 2026-10-16 staging called 1.125 vs 1 rounding-only (0 decimals) and marked the Brennan check "agrees"'),
    ('6500', '6500-08-06-FG', 'LEG_M5@DRIVE', 1.33, '6500-08-06-FG', 'M 2 Size', '6500-08-06-FG', 'M6 LGTH', 'swivel nut-face leg; batch-15-settled reading (Q36-8)'),
    ('6500', '6500-08-06-FG', 'LEG_M10@DRIVE', 0.95, '6500-08-06-FG', 'M 1 Size', '6500-08-06-FG', 'M4 LGTH', 'swivel seat leg; batch-15-settled reading (Q36-8)'),
    ('6505', '6505-24-24', 'L15@DRIVE', 2.94, '6505-24-24', 'Overall Length', '6505-24-24', None, 'pipe tip to nut face; batch-15-settled reading (Q36-10); OMi L15 - L16 = Air-Way (0.73): consistent pair'),
    ('6505', '6505-24-24', 'L16@DRIVE', 2.21, '6505-24-24', 'L 1 Size', '6505-24-24', None, 'pipe tip to seat; batch-15-settled reading (Q36-10)'),
    ('6505', '6505-32-32', 'L15@DRIVE', 3.59, '6505-32-32', 'Overall Length', '6505-32-32', None, 'pipe tip to nut face; OMi L15 - L16 = Air-Way (0.94): consistent pair'),
    ('6505', '6505-32-32', 'L16@DRIVE', 2.65, '6505-32-32', 'L 1 Size', '6505-32-32', None, 'pipe tip to seat'),
    ('5502', '5502-16-12-FG', 'N1@DRIVE', 1.39, '5502-16-12-FG', 'L 1 Size', '5502-16-12-FG', 'N1 LGTH', 'open reading M110 (Q36-5); the 2026-10-16 staging noted the Brennan difference 1.39 vs 1.360'),
]
out = []
for t, cfg, col, now, opn, oh, bpn, bc, note in ITEMS:
    i, row = OMI[opn]
    ov = str(row[oh]).strip()
    bv = CAT[bpn][1]['values'].get(bc) if bc and bpn in CAT else None
    if bc is None and bpn in CAT:
        bv = 'catalog lengths not mapped for 6505 here: ' + ', '.join(f'{k} {v}' for k, v in CAT[bpn][1]['values'].items() if 'LGTH' in k)
    out.append(dict(table=t, config=cfg, column=col, table_now=now, omi=ov, omi_cell=f'Items!{L[oh]}{i} "{oh}"', brennan=bv or '', proposed=ov,
                    why=f'OMi first (user 2026-09-25) - needs the A19-style approval (list first, apply if approved); {note}'))
out.append(dict(table='6500', config='6500-08-06-FG', column='$PRP@DataStatus', table_now='VERIFIED (edits_77)', omi='', omi_cell='', brennan='',
                proposed='ASSUMED', why='edits_77 (2026-10-16) sets VERIFIED from a Brennan check of LEG_M / hex / flats / bores only; the swivel legs LEG_M5 / LEG_M10 '
                'of Air-Way (1.33 / 0.95) differ from OMi = Brennan (1.28 / 0.91) - two sources do not agree on every driving cell -> ASSUMED (whichever leg value is used)'))
with open(os.path.join(OUT, 'pending_omi_A19.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for x in out:
    print(x['config'], x['column'], x['table_now'], '->', x['proposed'], '| Brennan', str(x['brennan'])[:80])
