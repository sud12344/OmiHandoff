"""make_bent_test.py (2026-10-15): TEST tables for the bent-tube model type (gen_bent.py) - review-table layout, DataStatus TEST.
NOT part data: they prove the sketches / features / design table across sizes and both bend angles. Never ship.

Where a value has a source it is used and cited; the rest is a TEST value, chosen only so that the geometry fits:
- 1704T (90 deg): 1704-12-12 / -24-24 / -24-20 / -16-20-Tube take Air-Way s115 (1701-61-A-B = OMi 1704-A-B-Tube):
  M1 = M3 - O/2 (M3 = JIC tip to the far edge of the flange head, O = head dia - Air-Way drawing), L1 = N4 (flange face to the
  JIC axis), CHEX = C, D = bore, O. TEST: tube OD = the JIC dash size, end-piece hex length HEXL 0.30, bend radius RB.
  1704-08-08-Tube: everything TEST except O / C / D, taken from Air-Way s61 1700-61-8-8 (the straight code 61 adapter).
- 1703T (45 deg): no Air-Way 45 deg bent-tube page - lengths TEST; O / C / D from Air-Way s61 1700-61 of the same sizes.

python make_bent_test.py  ->  tools/_out/newtypes_20261014/test_tables/DesignTable_1704T.xlsx, DesignTable_1703T.xlsx"""
import os
import openpyxl

OUT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\newtypes_20261014\test_tables'
AW115 = {'12-12': dict(N4=2.12, M3=2.84, C=1.13, D=0.61, O=1.50), '16-20': dict(N4=2.37, M3=2.79, C=1.38, D=0.84, O=2.00),
         '24-20': dict(N4=2.50, M3=3.52, C=2.00, D=1.08, O=2.00), '24-24': dict(N4=2.75, M3=3.67, C=2.00, D=1.31, O=2.38)}
AW61 = {'8-8': dict(C=0.81, D=0.39, O=1.19), '12-12': dict(C=1.13, D=0.61, O=1.50), '24-24': dict(C=2.00, D=1.31, O=2.38)}
TUBE = {8: 0.5, 12: 0.75, 16: 1.0, 20: 1.25, 24: 1.5, 32: 2.0}
HDR = [None, 'M1@DRIVE', 'L1@DRIVE', 'CHEX@HEX', 'HEXL@HEX', 'O@DRIVE', 'D@BORE', 'TUBEOD@TUBE', 'RB@PATH', '$PRP@FlangeCode',
       '$PRP@TubeOD', '$PRP@PartNo', '$PRP@DataStatus', '$PRP@AxialSource', '$COMMENT', '$PRP@ScopeAction', '$PRP@OMiSKU']


def row(pn, M1, L1, C, HEXL, O, D, OD, RB, src, code='61'):
    return [pn, M1, L1, C, HEXL, O, D, OD, RB, code, f'{OD:g}', pn, 'TEST',
            'TEST ROW - geometry test of the bent-tube model type, not part data, never ship | ' + src,
            'TEST: proves the sketches / sweeps / head / design table', 'BUILD', None]


t1704 = []
for k, rb in (('12-12', 0.875), ('24-24', 1.0), ('24-20', 1.0), ('16-20', 0.6)):
    a = AW115[k]
    jd = int(k.split('-')[0])
    t1704.append(row(f'1704-{k.split("-")[0]:0>2}-{k.split("-")[1]:0>2}-Tube', round(a['M3'] - a['O'] / 2, 4), a['N4'], a['C'], 0.30, a['O'], a['D'],
                     TUBE[jd], rb, f'M1 = M3 {a["M3"]} - O/2, L1 = N4 {a["N4"]}, C, D, O: Air-Way s115 1701-61-{k}; tube OD = dash, HEXL, RB: TEST'))
a = AW61['8-8']
t1704.append(row('1704-08-08-Tube', 1.9, 1.8, a['C'], 0.30, a['O'], a['D'], 0.5, 0.6, 'C, D, O: Air-Way s61 1700-61-8-8; M1, L1, HEXL, RB, tube OD: TEST'))
# code 62 (1804 -Tube): head OD 1.250 = the measured code 62 -08 head (FLG62_MEAS, wave-1 FLANGE62) - the only code 62 head measured
t1704.append(row('1804-08-08-Tube', 1.9, 1.85, a['C'], 0.30, 1.25, a['D'], 0.5, 0.6, 'code 62 head OD 1.250: FLG62_MEAS -08 (wave-1 FLANGE62); C, D: Air-Way s61 1700-61-8-8; M1, L1, HEXL, RB, tube OD: TEST', '62'))
t1703 = []
for pn, M1, L1, k, OD, RB in (('1703-12-12-Tube', 2.0, 1.6, '12-12', 0.75, 0.875), ('1703-24-24-Tube', 2.6, 2.2, '24-24', 1.5, 1.0),
                              ('1703-08-08-Tube', 1.9, 1.6, '8-8', 0.5, 0.6), ('1803-12-12-Tube', 2.0, 1.6, '12-12', 0.75, 0.875)):
    a = AW61[k]
    t1703.append(row(pn, M1, L1, a['C'], 0.30, a['O'], a['D'], OD, RB, f'C, D, O: Air-Way s61 1700-61-{k}; M1, L1, HEXL, RB, tube OD: TEST',
                     '62' if pn.startswith('18') else '61'))      # 1803-12-12 (code 62 -12 head not measured) must BLOCK
# 6701 (90 deg, male JIC x female JIC swivel): no Air-Way page - lengths TEST; end-piece hex C / bore D from Air-Way s61 1700-61 of
# the same JIC size; swivel nut hex and nose-tip depth from the straights' swivel library (SWIV_MEAS AF / NOSETIP_B, gen_straight2)
SW = {8: (0.875, 0.43), 12: (1.25, 0.57), 16: (1.5, 0.60)}
HDR_SW = [None, 'M1@DRIVE', 'L1@DRIVE', 'CHEX@HEX', 'HEXL@HEX', 'NUTHEX@NUTHEXSK', 'NOSETIP@SWSK', 'D@BORE', 'TUBEOD@TUBE', 'RB@PATH',
          '$PRP@TubeOD', '$PRP@PartNo', '$PRP@DataStatus', '$PRP@AxialSource', '$COMMENT', '$PRP@ScopeAction', '$PRP@OMiSKU']
t6701 = []
for pn, M1, L1, C, D, OD, RB in (('6701-08-08', 1.6, 1.8, 0.81, 0.39, 0.5, 0.6), ('6701-12-12', 2.2, 2.3, 1.13, 0.61, 0.75, 0.875),
                                 ('6701-16-16', 2.6, 2.7, 1.38, 0.84, 1.0, 1.0)):
    af, nt = SW[int(pn.split('-')[1])]
    t6701.append([pn, M1, L1, C, 0.30, af, nt, D, OD, RB, f'{OD:g}', pn, 'TEST',
                  'TEST ROW - geometry test of the bent-tube swivel model type, not part data, never ship | C, D: Air-Way s61 1700-61 of the '
                  'same JIC size; nut hex / nose tip: swivel library SWIV_MEAS (gen_straight2); M1, L1, HEXL, RB, tube OD: TEST',
                  'TEST: proves the swivel end on the bent leg', 'BUILD', None])
os.makedirs(OUT, exist_ok=True)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Sheet1'
ws.append([f'TEST TABLE 6701T - bent-tube swivel model type (gen_bent.py) | {len(t6701)} TEST rows | NOT PART DATA | 2026-10-15'])
ws.append(HDR_SW)
for r in t6701:
    ws.append(r)
wb.save(os.path.join(OUT, 'DesignTable_6701T.xlsx'))
print(os.path.join(OUT, 'DesignTable_6701T.xlsx'))
for root, rows in (('1704T', t1704), ('1703T', t1703)):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sheet1'
    ws.append([f'TEST TABLE {root} - bent-tube model type (gen_bent.py) | {len(rows)} TEST rows | NOT PART DATA | 2026-10-15'])
    ws.append(HDR)
    for r in rows:
        ws.append(r)
    p = os.path.join(OUT, f'DesignTable_{root}.xlsx')
    wb.save(p)
    print(p)
    for r in rows:
        print('  ', r[:10])
