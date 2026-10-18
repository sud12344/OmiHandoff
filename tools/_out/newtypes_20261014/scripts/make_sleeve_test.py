"""make_sleeve_test.py (2026-10-14): TEST table for the SLEEVE model type of gen_ring.py - review-table layout, DataStatus TEST.
NOT part data: proves that the sleeve sketch solves and the design table drives it across sizes. Never ship, never copy into
04_DESIGN_TABLES.

Rows (0319 = JIC tube sleeve, the same kind of part as the flareless sleeve 0619):
- 0319-08: L 0.56 and collar O.D. X 0.68 = Air-Way s48 (07_RAW_EXTRACTS/airway_passes/0319_p1.txt), bore 0.505 = OMi parts
  file Side 1 ID (Items row 47); collar length 0.220, spigot radius 0.2810, front-face inner radius 0.2945 and the cone
  (slope 0.6491 from the front face, reaching the bore at 0.0647) = SHAPE of BRENNAN_0319-08.stp (probe_sleeve.py).
- 0319-02 / 0319-32: Air-Way L / X and OMi bore as above; the four shape values SCALED from -08 (collar length and cone
  length in proportion to L, spigot and front-face radii as the same fraction of the collar wall) - TEST values only.

python make_sleeve_test.py  ->  tools/_out/newtypes_20261014/test_tables/DesignTable_0319T.xlsx"""
import os
import openpyxl

OUT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\newtypes_20261014\test_tables'
AW = {'0319-02': (0.34, 0.27), '0319-08': (0.56, 0.68), '0319-32': (1.19, 2.41)}       # Air-Way s48 L, X
OMI_ID = {'0319-02': 0.130, '0319-08': 0.505, '0319-32': 2.014}                         # OMi Items Side 1 ID (rows 42 / 47 / 53)
TUBE = {'0319-02': '1/8', '0319-08': '1/2', '0319-32': '2'}
B = dict(L=0.56, COLLARR=0.34, BORER=0.2525, COLLARL=0.220, SPIGOTR=0.2810, FRONTIR=0.2945)
B['CONEL'] = round((B['FRONTIR'] - B['BORER']) / 0.6491, 4)                              # Brennan cone line extended to the bore
WALL = B['COLLARR'] - B['BORER']
F = dict(COLLARL=B['COLLARL'] / B['L'], CONEL=B['CONEL'] / B['L'],
         SPIGOTR=(B['SPIGOTR'] - B['BORER']) / WALL, FRONTIR=(B['FRONTIR'] - B['BORER']) / WALL)

HDR = [None, 'L@DRIVE', 'COLLARR@DRIVE', 'COLLARL@DRIVE', 'SPIGOTR@DRIVE', 'BORER@DRIVE', 'FRONTIR@DRIVE', 'CONEL@DRIVE',
       '$PRP@TubeOD', '$PRP@PartNo', '$PRP@DataStatus', '$PRP@AxialSource', '$COMMENT', '$PRP@ScopeAction', '$PRP@OMiSKU']
rows = []
for pn in ('0319-02', '0319-08', '0319-32'):
    L, X = AW[pn]
    Rc, Rb = X / 2, OMI_ID[pn] / 2
    if pn == '0319-08':
        v = dict(B)
        src = 'L / X: Air-Way s48; bore: OMi Items row 47 Side 1 ID; collar length, spigot, front face, cone: BRENNAN_0319-08.stp SHAPE'
    else:
        w = Rc - Rb
        v = dict(L=L, COLLARR=Rc, BORER=Rb, COLLARL=round(F['COLLARL'] * L, 4), CONEL=round(F['CONEL'] * L, 4),
                 SPIGOTR=round(Rb + F['SPIGOTR'] * w, 4), FRONTIR=round(Rb + F['FRONTIR'] * w, 4))
        src = 'L / X: Air-Way s48; bore: OMi Side 1 ID; collar length, spigot, front face, cone: SCALED from the -08 shape (TEST only)'
    rows.append([pn, v['L'], v['COLLARR'], v['COLLARL'], v['SPIGOTR'], v['BORER'], v['FRONTIR'], v['CONEL'], TUBE[pn], pn, 'TEST',
                 'TEST ROW - geometry test of the SLEEVE model type, not part data, never ship | ' + src,
                 'TEST: proves the sketch / design table across sizes', 'BUILD', None])
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Sheet1'
ws.append(['TEST TABLE 0319T - SLEEVE model type (gen_ring.py) | 3 TEST rows | NOT PART DATA | 2026-10-14'])
ws.append(HDR)
for r in rows:
    ws.append(r)
p = os.path.join(OUT, 'DesignTable_0319T.xlsx')
wb.save(p)
print(p)
for r in rows:
    print('  ', r[:8])
