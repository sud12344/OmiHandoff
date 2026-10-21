"""fix_6810_row.py (2026-10-21): 6810-12-12-NWO-FG in the Brennan CAD stage table.
apply_cells.py promoted it MISSING -> ASSUMED although Y@HEX (forged body flats) and the swivel cells M19@DRIVE / M20@DRIVE / C3HEX@HEX
were empty: its 'required columns' come from the root's shipped rows and 6810 has none, so the test was vacuous.
- Y@HEX = 1.062: Brennan printed catalog TFA p44 6810-NWO-FG 'Y FLATS' 1.062 (brennan_catalog_20261001/catalog_verified.json, verified)
  = Brennan CAD record Y 1.062 (partcommunity_20261021/decode/decode_6810_nwo_fg.txt, AMBIGUOUS there) = BRENNAN_6810-12-12-NWO-FG.stp:
  3 flat pairs 1.062 apart, 60 deg apart around both leg axes (scripts/step_flats.py). One source (Brennan), DimSource BRENNAN.
  Air-Way prints only the plain 6810-12-12 NWO (Y 1.13; not copied to the -FG row, as for 6807 / 6809); OMi's file prints no 6810 dimension.
- DataStatus back to MISSING: M19 / M20 (swivel nose / nut face) have no settled source (catalog M / M6 pairing uncertain, F1b.md),
  C3HEX empty; with Y filled the generator stops in leg_JICSW on M19 / M20 (TypeError), so the row cannot build.
Original: ../old_files/DesignTable_6810.xlsx."""
import os, openpyxl
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..', '..'))
p = os.path.join(ROOT, 'tools', '_out', 'brennancad_20261021', 'stage', '04_DESIGN_TABLES', 'DesignTable_6810.xlsx')
wb = openpyxl.load_workbook(p); ws = wb.worksheets[0]
hr = next(i for i in range(1, 7) if any(c.value == '$PRP@PartNo' for c in ws[i]))
head = {c.value: c.column for c in ws[hr] if c.value}
i = next(i for i in range(hr + 1, ws.max_row + 1) if ws.cell(row=i, column=head['$PRP@PartNo']).value == '6810-12-12-NWO-FG')
cell = lambda c: ws.cell(row=i, column=head[c])
assert cell('Y@HEX').value is None and cell('$PRP@DataStatus').value == 'ASSUMED' and cell('$PRP@DimSource').value == 'BRENNAN'
cell('Y@HEX').value = 1.062
cell('$PRP@DataStatus').value = 'MISSING'
cell('$PRP@AxialSource').value = cell('$PRP@AxialSource').value.replace(
    'THDMAJ_B1@DRIVE] ', 'THDMAJ_B1@DRIVE; 2026-10-21 Y@HEX = Brennan catalog TFA p44 Y FLATS 1.062 = CAD record Y = STEP flats] ', 1)
cell('$COMMENT').value += (' | 2026-10-21 (hexskip_20261021): Y@HEX 1.062 = Brennan catalog TFA p44 Y FLATS (= CAD record Y, = BRENNAN_6810-12-12-NWO-FG '
                           'STEP flats); back to MISSING: M19@DRIVE / M20@DRIVE / C3HEX@HEX still empty (catalog M / M6 pairing uncertain, F1b.md)')
wb.save(p)
print('6810-12-12-NWO-FG: Y@HEX 1.062, DataStatus MISSING')
