"""wave2 tee_elbow - build cells.csv / rows.csv (2026-10-18).

Read-only on the project. Inputs: wave2/rows_tee_elbow.csv, today's base tables (base_root/04_DESIGN_TABLES), the Brennan catalog parse
(catalog_verified.json), OMi WebsitePartsInfo2026 Items, the batch-16 end libraries (puckfix tools_new gen_straight2 / ms51500 imported with
OMI_ROOT = base_root), the impact rows of 2026-10-01 (impact_rows.json, made by impact_dump.py) for the STEP verdicts.
Only cells EMPTY in the base are proposed. No DataStatus / DimSource / AxialSource cells (the apply script sets them).
    python -I -B build.py        (run from anywhere; env is set inside)
"""
import os, sys, csv, json, re, collections
R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
W2 = os.path.join(R, r'tools\_out\brennan_yes_20261018\wave2')
OUT = os.path.join(W2, 'tee_elbow')
HERE = os.path.join(OUT, 'scripts')
BASE_ROOT = os.path.join(R, r'tools\_out\brennan_yes_20261018\base_root')
BASE = os.path.join(BASE_ROOT, '04_DESIGN_TABLES')
TOOLS = os.path.join(R, r'tools\_out\puckfix_20261009\tools_new')
os.environ['OMI_ROOT'] = BASE_ROOT
os.environ['GS_OUT'] = os.environ['GT_OUT'] = os.path.join(OUT, 'scratch_libs')
sys.path[:0] = [os.path.join(TOOLS, 'generators'), TOOLS]
import openpyxl
from openpyxl.utils import get_column_letter
import gen_straight2 as G, ms51500 as MS

D = json.load(open(os.path.join(R, r'tools\_out\brennan_catalog_20261001\catalog_verified.json'), encoding='utf-8'))
TAB = {t['table_id']: t for t in D['tables']}
CAT = {}
for t in D['tables']:
    for rr in t['rows']:
        CAT.setdefault(rr['pn'], (t, rr))
IMP = json.load(open(os.path.join(HERE, 'impact_rows.json'), encoding='utf-8'))
ROWS = list(csv.DictReader(open(os.path.join(W2, 'rows_tee_elbow.csv'), encoding='utf-8')))

# ---- OMi Items
wb = openpyxl.load_workbook(os.path.join(R, r'07_RAW_EXTRACTS\omi_dimensions\WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)
_ws = wb['Items']; _it = _ws.iter_rows(values_only=True); OH = next(_it)
OMI = {}
for i, r in enumerate(_it, start=2):
    if r[0]:
        OMI.setdefault(str(r[0]).strip(), (i, dict(zip(OH, r))))
OCOL = {h: get_column_letter(j + 1) for j, h in enumerate(OH) if h}

# ---- thread names (generator libraries)
NPT_NAME = {2: '1/8-27', 4: '1/4-18', 6: '3/8-18', 8: '1/2-14', 12: '3/4-14', 16: '1-11 1/2', 20: '1 1/4-11 1/2', 24: '1 1/2-11 1/2',
            32: '2-11 1/2', 40: '2 1/2-8'}      # = gen_straight2 FPT[d]['thr'] (2405 template) without " NPTF (female)"; -40 = PIPE_THD_NAME
for d, v in G.FPT.items():
    assert v['thr'].startswith(NPT_NAME[d]), (d, v)
UN = {d: v['thr'] for d, v in G.JIC.items()}     # JIC / ORB UN callouts (2403 template; -40 measured)

SRC_NPTF = 'end library: pipe OD of the -{d:02d} NPTF thread = {v} (ASME B1.20.1 Table 2, tools generators/ms51500.py NPTF[{d}], as on every built pipe end; thread from the part number) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
SRC_NPSM = 'end library: pipe OD of the -{d:02d} NPSM swivel thread = {v} (ASME B1.20.1 pipe OD, ms51500.py NPTF[{d}]; the value every built 1501 / 1405 / 1502 row carries for its NPSM end; thread from the part number) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
SRC_JIC = 'end library: male JIC -{d:02d} thread major = {v} (gen_straight2 JIC[{d}] = MS33656J chain of templates/DesignTable_2403_SW2.xlsx{x}) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
SRC_ORB = 'end library: SAE ORB -{d:02d} thread major = {v} (gen_straight2 ORB[{d}] from the 6401 / 6405 / 6410 review tables) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
SRC_TAP = ('end library: tap drill of the -{d:02d} female NPTF port = {v} (gen_straight2 FPT[{d}] = templates/DesignTable_2405_SW2.xlsx TAPDRILL@BORE_A; '
           '= Air-Way\'s per-size tap drill of OPEN_QUESTIONS A1){gate}')


def num(s):
    s = str(s).strip()
    if re.fullmatch(r'\d*\.\d+|\d+', s):
        return float(s)
    return None


def dashes(pn):
    return [int(x) for x in re.findall(r'-(\d\d)(?=-|$)', pn.replace(' ', '-'))]


def fmt(v):
    return ('%.4f' % v).rstrip('0').rstrip('.')


# ---- per-table configuration ----------------------------------------------------------------------------------------------
# dims: (table column, catalog column, meaning); ends: (table column, kind, dash index); thr: $PRP@Threads (or EndA/EndB) builder
# omi: table column -> OMi Items column (same part, same feature) ; unconf: catalog columns whose mapping is NOT confirmed (not filled)
T = {}
T['1501'] = dict(tid='TFA-p020-t01', dims=[('N1@DRIVE', 'L LGTH', 'axis crossing to the male NPTF tip'),
                                           ('M1@DRIVE', 'M LGTH', 'axis crossing to the NPSM swivel stem tip'),
                                           ('W3@HEX', 'M1 LGTH', 'axis crossing to the swivel-nut face'),
                                           ('CHEX@HEX', 'C HEX', 'swivel nut hex'), ('C1HEX@HEX', 'Y FLATS', 'forged body flats'),
                                           ('D2@BORE', 'A1 DRILL', 'male NPTF end drill'), ('D@BORE', 'A2 DRILL', 'NPSM swivel stem bore')],
                 ends=[('THDMAJ_A@DRIVE', 'NPTF', 0), ('THDMAJ_A1@DRIVE', 'NPSM', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A NPTF) x {NPT_NAME[d[1]]} (A1 NPSM)'})
T['1503'] = dict(tid='TFA-p021-t02', dims=[('N@DRIVE', 'L LGTH', 'axis crossing to the male NPTF tip'),
                                           ('M@DRIVE', 'M1 LGTH', 'axis crossing to the NPSM swivel stem tip (45 deg leg)'),
                                           ('W2@HEX', 'M LGTH', 'axis crossing to the swivel-nut face (45 deg leg)'),
                                           ('CHEX@HEX', 'C HEX', 'swivel nut hex'), ('C1HEX@HEX', 'Y FLATS', 'forged body flats'),
                                           ('D2@BORE', 'A1 DRILL', 'male NPTF end drill'), ('D@BORE', 'A2 DRILL', 'NPSM swivel stem bore')],
                 ends=[('THDMAJ_A@DRIVE', 'NPTF', 0), ('THDMAJ_A1@DRIVE', 'NPSM', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A NPTF) x {NPT_NAME[d[1]]} (A1 NPSM)'})
T['1504'] = dict(tid='TFA-p022-t01', dims=[('N2@DRIVE', 'L LGTH', 'axis crossing to the female NPTF port face'),
                                           ('M@DRIVE', 'M1 LGTH', 'axis crossing to the NPSM swivel stem tip (45 deg leg)'),
                                           ('W2@HEX', 'M LGTH', 'axis crossing to the swivel-nut face (45 deg leg)'),
                                           ('CHEX@HEX', 'C HEX', 'swivel nut hex'), ('C1HEX@HEX', 'Y FLATS', 'forged body flats'),
                                           ('D@BORE', 'A2 DRILL', 'NPSM swivel stem bore')],
                 ends=[('TAPDRILL@BORE', 'TAP', 0), ('THDMAJ_A@DRIVE', 'NPTF', 0), ('THDMAJ_A1@DRIVE', 'NPSM', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A NPTF) x {NPT_NAME[d[1]]} (A1 NPSM)'})
T['1601'] = dict(tid='TFA-p047-t02', dims=[('N1@DRIVE', 'L LGTH', 'run axis to the male NPTF (A1) branch tip'),
                                           ('M1_2@DRIVE', 'M1 LGTH', 'branch axis to the A2 swivel stem tip (printed once, A2 = A3)'),
                                           ('M1_3@DRIVE', 'M1 LGTH', 'branch axis to the A3 swivel stem tip'),
                                           ('W3_2@HEX', 'M LGTH', 'branch axis to the A2 swivel-nut face'),
                                           ('W3_3@HEX', 'M LGTH', 'branch axis to the A3 swivel-nut face (printed once, A2 = A3)'),
                                           ('C2HEX@HEX', 'C HEX', 'A2 swivel nut hex (printed once, A2 = A3)'), ('C3HEX@HEX', 'C HEX', 'A3 swivel nut hex'),
                                           ('C1HEX@HEX', 'Y FLATS', 'forged body flats'), ('D2@BORE', 'A1 DRILL', 'male NPTF end drill'),
                                           ('D_2@BORE', 'A2 DRILL', 'A2 NPSM stem bore'), ('D3@BORE', 'A3 DRILL', 'A3 NPSM stem bore')],
                 ends=[('THDMAJ_A@DRIVE', 'NPTF', 0), ('THDMAJ_A1_2@DRIVE', 'NPSM', 1), ('THDMAJ_A1_3@DRIVE', 'NPSM', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A NPTF) x {NPT_NAME[d[1]]} (A1 (2) NPSM) x {NPT_NAME[d[2]]} (A1 (3) NPSM)'})
T['1602'] = dict(tid='TFA-p048-t01', dims=[('N3@DRIVE', 'L LGTH', 'run axis to the female NPTF (A1) branch port face'),
                                           ('M1_2@DRIVE', 'M1 LGTH', 'branch axis to the A2 swivel stem tip (printed once, A2 = A3)'),
                                           ('M1_3@DRIVE', 'M1 LGTH', 'branch axis to the A3 swivel stem tip'),
                                           ('W3_2@HEX', 'M LGTH', 'branch axis to the A2 swivel-nut face'),
                                           ('W3_3@HEX', 'M LGTH', 'branch axis to the A3 swivel-nut face (printed once, A2 = A3)'),
                                           ('C2HEX@HEX', 'C HEX', 'A2 swivel nut hex (printed once, A2 = A3)'), ('C3HEX@HEX', 'C HEX', 'A3 swivel nut hex'),
                                           ('C1HEX@HEX', 'Y FLATS', 'forged body flats'),
                                           ('D2@BORE', 'A2 DRILL', 'A2 NPSM stem bore'), ('D3@BORE', 'A3 DRILL', 'A3 NPSM stem bore')],
                 ends=[('TAPDRILL@BORE', 'TAP', 0), ('THDMAJ_A@DRIVE', 'NPTF', 0), ('THDMAJ_A1_2@DRIVE', 'NPSM', 1), ('THDMAJ_A1_3@DRIVE', 'NPSM', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A NPTF) x {NPT_NAME[d[1]]} (A1 (2) NPSM) x {NPT_NAME[d[2]]} (A1 (3) NPSM)'})
T['1603'] = dict(tid='TFA-p048-t02', dims=[('M1@DRIVE', 'M2 LGTH', 'run/branch axis to the A1 stem tip - not printed for A1; A1 = A2 = A3 on every same-dash row, taken from the A3 stem tip M2 (symmetry; same value under any leg reading)'),
                                           ('M2_2@DRIVE', 'M1 LGTH', 'run axis to the A2 swivel stem tip'),
                                           ('M2_3@DRIVE', 'M2 LGTH', 'run axis to the A3 swivel stem tip'),
                                           ('W3@HEX', 'L LGTH', 'axis to the A1 (branch) swivel-nut face'),
                                           ('W5_2@HEX', 'M LGTH', 'axis to the A2 swivel-nut face - printed for A3 only; A2 = A3 (symmetry)'),
                                           ('W5_3@HEX', 'M LGTH', 'axis to the A3 swivel-nut face'),
                                           ('C_1HEX@HEX', 'C HEX', 'A1 swivel nut hex'), ('C2HEX@HEX', 'C1 HEX', 'A2 swivel nut hex (C1 HEX printed for A3; A2 = A3)'),
                                           ('C3HEX@HEX', 'C1 HEX', 'A3 swivel nut hex'), ('C1HEX@HEX', 'Y Flats', 'forged body flats'),
                                           ('D1@BORE', 'A1 DRILL', 'NPSM stem bore (A1)'), ('D2@BORE', 'A2 DRILL', 'NPSM stem bore (A2 / A3)')],
                 ends=[('THDMAJ_A1_1@DRIVE', 'NPSM', 0), ('THDMAJ_A1_2@DRIVE', 'NPSM', 1), ('THDMAJ_A1_3@DRIVE', 'NPSM', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A1 (1) NPSM) x {NPT_NAME[d[1]]} (A1 (2) NPSM) x {NPT_NAME[d[2]]} (A1 (3) NPSM)'})
T['2500'] = dict(tid='TFA-p022-t02', dims=[('M1@DRIVE', 'M1 LGTH', 'B1 JIC tip to the B2 axis'), ('M2@DRIVE', 'M2 LGTH', 'B2 JIC tip to the B1 axis'),
                                           ('Y@REF', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'B1 DRILL', 'B1 JIC end drill'),
                                           ('D2@BORE', 'B2 DRILL', 'B2 JIC end drill')],
                 ends=[('THDMAJ_B1@DRIVE', 'JIC', 0), ('THDMAJ_B2@DRIVE', 'JIC', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} x {UN[d[1]]} (male JIC both ends)'})
T['2501'] = dict(tid='TFA-p023-t01', dims=[('M@DRIVE', 'M LGTH', 'axis crossing to the JIC tip'), ('N@DRIVE', 'L LGTH', 'axis crossing to the male NPTF tip'),
                                           ('Y@REF', 'Y FLATS', 'forged body flats'), ('D@BORE', 'B1 DRILL', 'JIC end drill'),
                                           ('D1@DRILL', 'A2 DRILL', 'male NPTF end drill')],
                 ends=[('THDMAJ_A@DRIVE', 'JIC', 0), ('JICCHAIN', 'JICCHAIN', 0), ('NPTFCHAIN', 'NPTFCHAIN', 1)],
                 thr=lambda d: {'$PRP@EndA_Thread': NPT_NAME[d[1]].replace(' 1/2', '-1/2') if d[1] == 40 else NPT_NAME[d[1]], '$PRP@EndB_Thread': UN[d[0]]},
                 omi={'M@DRIVE': 'M 1 Size', 'N@DRIVE': 'L 1 Size', 'Y@REF': 'Hex Flat', 'D@BORE': 'Side 1 ID', 'D1@DRILL': 'Side 2 ID'})
T['2501LL'] = dict(tid='TFA-p024-t02', dims=[('M@DRIVE', 'M LGTH', 'JIC leg: crossing to the JIC tip'), ('N4@DRIVE', 'L LGTH', 'pipe leg: crossing to the male NPTF tip'),
                                             ('Y@REF', 'Y FLATS', 'forged body flats'), ('D@BORE', 'B1 DRILL', 'JIC-leg bore'), ('D1@BORE', 'A2 DRILL', 'pipe drill')],
                   ends=[('THDMAJ_B@DRIVE', 'JIC', 0), ('THDMAJ_A@DRIVE', 'NPTF', 1)],
                   thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} (JIC) x {NPT_NAME[d[1]]} (NPTF) N4 long pattern'})
T['2502'] = dict(tid='TFA-p025-t02', dims=[('M1@DRIVE', 'M LGTH', 'axis crossing to the JIC tip'), ('N1@DRIVE', 'L LGTH', 'axis crossing to the female NPTF port face'),
                                           ('Y1@DRIVE', 'Y FLATS', 'forged body flats'), ('D@BORE', 'B1 DRILL', 'JIC end drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 1), ('THDMAJ_B@DRIVE', 'JIC', 0), ('THDMAJ_A@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} (JIC 37) x {NPT_NAME[d[1]]} (NPTF female)'},
                 omi={'M1@DRIVE': 'M 1 Size', 'N1@DRIVE': 'L 1 Size', 'Y1@DRIVE': 'Hex Flat', 'D@BORE': 'Side 1 ID'})
T['2505'] = dict(tid='TFA-p027-t01', dims=[('M2@DRIVE', 'M LGTH', 'JIC leg'), ('N6@DRIVE', 'N LGTH', 'female pipe leg along the 45 deg axis'),
                                           ('Y1@HEX', 'Y FLATS', 'forged body flats'), ('D@BORE', 'B1 DRILL', 'JIC end drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 1), ('THDMAJ_B@DRIVE', 'JIC', 0), ('THDMAJ_A@DRIVE', 'NPTF', 1)], thr=None,
                 omi={'M2@DRIVE': 'M 1 Size', 'N6@DRIVE': 'M 2 Size', 'Y1@HEX': 'Hex Flat', 'D@BORE': 'Side 1 ID'})
T['2602'] = dict(tid='TFA-p049-t02', dims=[('M1_1@DRIVE', 'M1 LGTH', 'B1 JIC run leg'), ('M1_2@DRIVE', 'M2 LGTH', 'B2 JIC run leg'),
                                           ('N1@DRIVE', 'N LGTH', 'run axis to the female NPTF branch port face'), ('Y1@DRIVE', 'Y FLATS', 'forged body flats'),
                                           ('D1@BORE', 'B1 DRILL', 'B1 JIC drill'), ('D2@BORE', 'B2 DRILL', 'B2 JIC drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 2), ('THDMAJ_B1@DRIVE', 'JIC', 0), ('THDMAJ_B2@DRIVE', 'JIC', 1), ('THDMAJ_A@DRIVE', 'NPTF', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} x {UN[d[1]]} (JIC) x {NPT_NAME[d[2]]} (NPTF female branch)'},
                 omi={'M1_1@DRIVE': 'M 1 Size', 'M1_2@DRIVE': 'M 2 Size', 'N1@DRIVE': 'L 1 Size', 'Y1@DRIVE': 'Hex Flat', 'D1@BORE': 'Side 1 ID', 'D2@BORE': 'Side 2 ID'})
T['2606'] = dict(tid='TFA-p051-t01', dims=[('M1_1@DRIVE', 'M LGTH', 'B1 JIC run leg'), ('N1@DRIVE', 'L LGTH', 'female NPTF branch'), ('M1_3@DRIVE', 'N LGTH', 'B3 JIC run leg'),
                                           ('Y1@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'B1 DRILL', 'B1 drill'), ('D3@BORE', 'B3 DRILL', 'B3 drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 1), ('THDMAJ_B1@DRIVE', 'JIC', 0), ('THDMAJ_A@DRIVE', 'NPTF', 1), ('THDMAJ_B3@DRIVE', 'JIC', 2)], thr=None,
                 omi={'M1_1@DRIVE': 'M 1 Size', 'N1@DRIVE': 'M 2 Size', 'M1_3@DRIVE': 'L 1 Size', 'Y1@HEX': 'Hex Flat', 'D1@BORE': 'Side 1 ID', 'D3@BORE': 'Side 3 ID'})
T['2609'] = dict(tid='TFA-p052-t01', dims=[('M1@DRIVE', 'M LGTH', 'JIC leg'), ('N1_2@DRIVE', 'L1 LGTH', 'A2 female port'), ('N1_3@DRIVE', 'L LGTH', 'A3 female port'),
                                           ('Y1@HEX', 'Y FLATS', 'forged body flats'), ('D@BORE', 'B1 DRILL', 'JIC drill')],
                 ends=[('TAPDRILL2@BORE', 'TAP', 1), ('TAPDRILL3@BORE', 'TAP', 2), ('THDMAJ_B@DRIVE', 'JIC', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1), ('THDMAJ_A3@DRIVE', 'NPTF', 2)], thr=None,
                 omi={'M1@DRIVE': 'M 1 Size', 'N1_2@DRIVE': 'M 2 Size', 'N1_3@DRIVE': 'L 1 Size', 'Y1@HEX': 'Hex Flat', 'D@BORE': 'Side 1 ID'})
T['2611'] = dict(tid='TFA-p052-t03', dims=[('M1@DRIVE', 'M LGTH', 'axis to the B1 JIC tip'), ('N5@DRIVE', 'L LGTH', 'axis to the A2 male NPTF tip'),
                                           ('N1@DRIVE', 'L1 LGTH', 'axis to the A3 female NPTF port face'), ('Y1@HEX', 'Y FLATS', 'forged body flats'),
                                           ('D@BORE', 'B1 DRILL', 'JIC drill'), ('D1@BORE', 'A2 DRILL', 'male NPTF drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 2), ('THDMAJ_B@DRIVE', 'JIC', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1), ('THDMAJ_A3@DRIVE', 'NPTF', 2)], thr=None,
                 omi={'M1@DRIVE': 'M 1 Size', 'N5@DRIVE': 'M 2 Size', 'N1@DRIVE': 'L 1 Size', 'Y1@HEX': 'Hex Flat', 'D@BORE': 'Side 1 ID', 'D1@BORE': 'Side 2 ID'})
T['5501'] = dict(tid='TFA-p031-t02', dims=[('N4@DRIVE', 'N LGTH', 'A1 male NPTF leg (crossing to tip)'), ('N6@DRIVE', 'N1 LGTH', 'A2 male NPTF leg (crossing to tip, 45 deg)'),
                                           ('Y@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'A1 DRILL', 'A1 drill'), ('D2@BORE', 'A2 DRILL', 'A2 drill')],
                 ends=[('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A (1) NPTF) x {NPT_NAME[d[1]]} (A (2) NPTF)'},
                 omi={'N4@DRIVE': 'M 1 Size', 'N6@DRIVE': 'L 1 Size', 'Y@HEX': 'Hex Flat', 'D1@BORE': 'Side 1 ID', 'D2@BORE': 'Side 2 ID'})
T['5502'] = dict(tid='TFA-p031-t03', dims=[('N@DRIVE', 'N LGTH', 'axis crossing to the male NPTF tip'), ('N1@DRIVE', 'N1 LGTH', 'axis crossing to the female NPTF port face'),
                                           ('W@REF', 'Y FLATS', 'forged body flats'), ('D@BORE', 'A1 DRILL', 'male end drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 1), ('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (male) x {NPT_NAME[d[1]]} (female) NPTF'},
                 omi={'N@DRIVE': 'M 1 Size', 'N1@DRIVE': 'L 1 Size', 'W@REF': 'Hex Flat', 'D@BORE': 'Side 1 ID'})
T['5503'] = dict(tid='TFA-p032-t01', dims=[('N4@DRIVE', 'N LGTH', 'A1 male pipe tip to the 45 deg crossing'), ('N3@DRIVE', 'N1 LGTH', 'A2 female port face along the 45 deg axis'),
                                           ('W@HEX', 'Y FLATS', 'forged body flats'), ('D@BORE', 'A1 DRILL', 'male end drill')],
                 ends=[('TAPDRILL@BORE', 'TAP', 1), ('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A (1) NPTF) x {NPT_NAME[d[1]]} (A (2) NPTF)'})
T['5504'] = dict(tid='TFA-p032-t02', dims=[('N1_1@DRIVE', 'N LGTH', 'A1 female port face'), ('N1_2@DRIVE', 'N1 LGTH', 'A2 female port face'), ('W@REF', 'Y FLATS', 'forged body flats')],
                 ends=[('TAPDRILL1@BORE', 'TAP', 0), ('TAPDRILL2@BORE', 'TAP', 1), ('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} x {NPT_NAME[d[1]]} NPTF (female x female)'})
T['5505'] = dict(tid='TFA-p033-t01', dims=[('N2_1@DRIVE', 'N LGTH', 'A1 female port face'), ('N2_2@DRIVE', 'N1 LGTH', 'A2 female port face (45 deg)'), ('W@HEX', 'Y FLATS', 'forged body flats')],
                 ends=[('TAPDRILL1@BORE', 'TAP', 0), ('TAPDRILL2@BORE', 'TAP', 1), ('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A (1) NPTF) x {NPT_NAME[d[1]]} (A (2) NPTF)'})
T['5604'] = dict(tid='TFA-p056-t02', dims=[('N1_1@DRIVE', 'N1 LGTH', 'A1 female run port face'), ('N1_2@DRIVE', 'N2 LGTH', 'A2 female run port face'),
                                           ('N@DRIVE', 'N LGTH', 'A3 male branch tip'), ('W@HEX', 'Y FLATS', 'forged body flats'), ('D@BORE', 'A3 DRILL', 'male branch drill')],
                 ends=[('TAPDRILL1@BORE', 'TAP', 0), ('TAPDRILL2@BORE', 'TAP', 1), ('THDMAJ_A1@DRIVE', 'NPTF', 0), ('THDMAJ_A2@DRIVE', 'NPTF', 1), ('THDMAJ_A3@DRIVE', 'NPTF', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{NPT_NAME[d[0]]} (A (1) NPTF) x {NPT_NAME[d[1]]} (A (2) NPTF) x {NPT_NAME[d[2]]} (A (3) NPTF)'})
T['6606'] = dict(tid='TFA-p058-t04', dims=[(f'M5_{i}@DRIVE', 'M6 LGTH', f'leg {i}: axis to the swivel-nut face (printed once; all legs alike)') for i in (1, 2, 3)]
                 + [(f'M10_{i}@DRIVE', 'M LGTH', f'leg {i}: axis to the swivel nose (printed once; all legs alike)') for i in (1, 2, 3)]
                 + [(f'C3_{i}HEX@HEX', 'C HEX', f'leg {i} swivel nut hex') for i in (1, 2, 3)]
                 + [('Y@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'A1 DRILL', 'bore (A1 = A2 = A3 on every row)')],
                 ends=[('THDMAJ_B1@DRIVE', 'JIC', 0), ('THDMAJ_B2@DRIVE', 'JIC', 1), ('THDMAJ_B3@DRIVE', 'JIC', 2)],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} x {UN[d[1]]} x {UN[d[2]]} (female JIC swivel all three ends)'})
T['6815'] = dict(tid='TFA-p045-t01', newcols=True,
                 dims=[('LEG_ORB@DRIVE', 'M8 LGTH', 'B1 adjustable male ORB tip to the B2 axis (6801 analog LEG_ORB@DRIVE = catalog M7)'),
                       ('LEG_FORB@DRIVE', 'M6 LGTH', 'B1 axis to the B2 female ORB port face'),
                       ('HEXB@HEX', 'C HEX', 'lock-nut hex (6801 analog HEXB@HEX)'), ('Y@REF', 'Y FLATS', 'forged body flats (6801 analog Y@REF)'),
                       ('D2@BORE', 'B1 DRILL', 'bore of the adjustable male ORB end (6801 analog D2@BORE)')], ends=[], thr=None)
T['6832'] = dict(tid='TFA-p061-t01', newcols=True,
                 dims=[('LEG1@DRIVE', 'M1 LGTH', 'B1 female ORB port face to the branch axis (6803 analog LEG1@DRIVE)'),
                       ('LEG2@DRIVE', 'N2 LGTH', 'B2 female ORB port face to the branch axis (6803 analog LEG2@DRIVE)'),
                       ('LEG3@DRIVE', 'M7 LGTH', 'run axis to the B3 adjustable male ORB tip (6803 analog LEG3@DRIVE)'),
                       ('HEXB@HEX', 'C HEX', 'lock-nut hex'), ('Y@REF', 'Y FLATS', 'forged body flats'), ('D3@BORE', 'B3 DRILL', 'bore of the B3 male ORB end')], ends=[], thr=None)
T['6835'] = dict(tid='TFA-p061-t02', newcols=True,
                 dims=[('LEG1@DRIVE', 'M7 LGTH', 'B1 adjustable male ORB tip to the branch axis (6804 analog LEG2@DRIVE = catalog M7)'),
                       ('LEG2@DRIVE', 'M2 LGTH', 'branch axis to the B2 female ORB port face'),
                       ('LEG3@DRIVE', 'M1 LGH', 'run axis to the B3 female ORB port face'),
                       ('HEXB@HEX', 'C HEX', 'lock-nut hex'), ('Y@REF', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'B1 DRILL', 'bore of the B1 male ORB end')], ends=[], thr=None)
T['6901'] = dict(tid='TFA-p046-t01', dims=[('CHEX@HEX', 'C1 HEX', 'NPSM swivel nut hex'),
                                           ('C4HEX@HEX', 'C HEX', 'ORB lock-nut hex'), ('D1@BORE', 'B DRILL', 'ORB end drill'), ('D@BORE', 'A DRILL', 'NPSM end drill')],
                 ends=[('THDMAJ_B@DRIVE', 'ORB', 0), ('THDMAJ_A1@DRIVE', 'NPSM', 1)],
                 unconf=[('N5@DRIVE', 'M7 LGTH'), ('M1@DRIVE', 'M LGTH'), ('W3@HEX', 'M6 LGTH'), ('C1HEX@HEX', 'Y FLATS')],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} (B UN/UNF-2A) x {NPT_NAME[d[1]]} (A1 NPSM)'})
T['6902'] = dict(tid='TFA-p046-t02', dims=[('CHEX@HEX', 'C1 HEX', 'NPSM swivel nut hex'),
                                           ('C4HEX@HEX', 'C HEX', 'ORB lock-nut hex'), ('D1@BORE', 'B DRILL', 'ORB end drill'), ('D@BORE', 'A DRILL', 'NPSM end drill')],
                 ends=[('THDMAJ_B@DRIVE', 'ORB', 0), ('THDMAJ_A1@DRIVE', 'NPSM', 1)],
                 unconf=[('N4@DRIVE', 'M8 LGTH'), ('M@DRIVE', 'M LGTH'), ('W2@HEX', 'M6 LGTH'), ('C1HEX@HEX', 'Y FLATS')],
                 thr=lambda d: {'$PRP@Threads': f'{UN[d[0]]} (B UN/UNF-2A) x {NPT_NAME[d[1]]} (A1 NPSM)'})
# tables whose rows are all '3D file' (no catalog row): 6500 6501 6502 6566 6802 6806 (+ single rows of 1504 2502 5503) - no config needed

# ---- generator coverage (batch-16 tools)
GEN_TEE = {'1501', '1503', '2501', '2501LL', '2505', '2602', '2606', '2609', '2611', '5502', '5504', '5604', '6500', '6501', '6502', '6802'}   # 2501LL = fold of 2501
GEN_ROOT = {'2501LL': '2501'}
HX = {'2500': '2500HX', '2502': '2502HX'}
# generator results of the TEST (test/compare.txt) that hold a row whose data is complete
GEN_BLOCK = {'2505-16-16-FG': ('GENERATOR BLOCKS (base and test alike): "leg 1: port depth P1 1.14 >= leg length 1.12" = Q-ANGLED-P1 (A15: settle from Brennan if '
                               'it answers): the TFA catalog prints no port depth and 09_STEP_FILES/BRENNAN_2505-16-16-FG.stp is not there -> needs STEP download; '
                               'otherwise open for later')}

DECIDED = ('Q-TRANSFER-ENDLIB', 'Q-TRANSFER-TAPDRILL', 'Q-NEW-F1A-5504TAP')   # A1 answered YES 2026-10-18 (00_DOCS/ANSWERS_2026-10-18.md)
MOOT = {'Q-NEW-F2A-NOTINCAT': 'moot with Brennan = yes (OPEN_QUESTIONS "Closed": Brennan routes allowed)',
        'Q-NEW-F3-6566': 'moot with Brennan = yes (OPEN_QUESTIONS "Closed")', 'Q-B-OTHER-TEE2': 'Q-B-* moot with Brennan = yes'}
GATE_TXT = {
    'Q-HX': 'GATE Q-HX (A7 answered 2026-10-18: move 2500HX / 2502HX to the generator LATER, no hand typing): no 2500 / 2502 generator SPEC yet',
    'Q-TRANSFER-TAPDRILL': 'GATE Q-TRANSFER-TAPDRILL (A1, open): tap drill of a female pipe port on an existing family = Air-Way per-size value (prepared here = the end-library value)',
    'Q-NEW-F1A-5504TAP': 'GATE Q-NEW-F1A-5504TAP (part of A1, open): 5504 tap drills (prepared = end-library value)',
    'Q-CONFLICT-2502-MS51506': 'GATE Q-CONFLICT-2502-MS51506 (D, open): legs OMi/Brennan vs MS51506 - M1@DRIVE / N1@DRIVE left EMPTY (never picked)',
    'Q-CONFLICT-TAPDRILL-24': 'GATE Q-CONFLICT-TAPDRILL-24 (A9, open): -24 tap drill 1.72 vs 1.70 - left EMPTY',
    'Q-CONFLICT-TAPDRILL-32': 'GATE Q-CONFLICT-TAPDRILL-32 (A9, open): -32 tap drill 2.19 vs 2.20 - left EMPTY',
    'Q-CONFLICT-ORBTHDL-12': 'GATE Q-CONFLICT-ORBTHDL-12 (open): -12 ORB thread length (not a catalog column; no cell here)',
    'Q-TRANSFER-NUTHEX': 'GATE Q-TRANSFER-NUTHEX (open)',
}
CAP_TXT = 'capability approved 2026-10-08 but NOT implemented in the batch-16 generators (puckfix tools_new gen_tee / gen_straight2; staged separately in tools/_out/wave2_impl_20261009 / wave2_shapes_20261008, not merged)'


def steps_ok(cfg):
    """the impact STEP verdict: what the row's own STEP was still needed for"""
    out = []
    for s in IMP.get(cfg, {}).get('steps') or []:
        if s.get('role', 'required' if s.get('pn') == cfg else 'reference') == 'required':
            out.append((s.get('verdict'), str(s.get('still_needed_for') or '')))
    return out


def base_table(t):
    ws = openpyxl.load_workbook(os.path.join(BASE, f'DesignTable_{t}.xlsx')).active
    hdr = [c.value for c in ws[2]]
    rows = {}
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0]:
            rows[str(r[0]).strip()] = dict(zip(hdr, r))
    return hdr, rows


def empty(v):
    return v is None or (isinstance(v, str) and v.strip() == '')


cells, rowsout, conflicts_all, omi_checks, map_checks = [], [], [], [], []
btabs = {}
for row in ROWS:
    t, c, how = row['table'], row['config'], row['how']
    gates_in = [g for g in row['other_gates'].split(';') if g.strip()]
    if t not in btabs:
        btabs[t] = base_table(t)
    hdr, brows = btabs[t]
    assert c in brows, (t, c)
    b = brows[c]
    d = dashes(c)
    notes, gates, missing, conf = [], [], [], []
    mine = []                       # cells for this row
    # ---------- gates
    for g in gates_in:
        g = g.strip()
        if g in DECIDED:
            continue
        if g.startswith('CAP:'):
            gates.append(f'GATE {g}: {CAP_TXT}')
        elif g.startswith('STEP:'):
            alts = g.split('|')
            st = steps_ok(c)
            have = os.path.exists(os.path.join(R, '09_STEP_FILES', f'BRENNAN_{alts[0][5:]}.stp'))
            why = '; '.join(f'{v}: {w}' for v, w in st) or 'no impact verdict'
            if how == '3D file':
                continue            # handled below
            if have:
                notes.append(f'{alts[0]}: file present in 09_STEP_FILES (pilot / shape reference; not measured here)')
            elif any('end-library alternative' in w and 'TAPDRILL' in w for v, w in st) and not any(x for x in st if 'pilot' in x[1] or 'forged' in x[1] or 'geometry' in x[1]):
                notes.append(f'{alts[0]} satisfied without the file: the impact verdict says it was needed only for "{why[:160]}" -> end library (Q-TRANSFER-ENDLIB yes)' + (
                    ' / Q-TRANSFER-TAPDRILL' if 'Q-TRANSFER-TAPDRILL' in g else ''))
            elif len(alts) > 1 and 'only if Q-TRANSFER-TAPDRILL = no' in why:
                notes.append(f'{alts[0]} only needed if Q-TRANSFER-TAPDRILL = no ({"; ".join(MOOT.get(a, a) for a in alts[1:])})')
            else:
                gates.append(f'GATE {alts[0]} (shape / pilot file not in 09_STEP_FILES - needs STEP download): {why[:220]}')
        elif g in MOOT:
            notes.append(f'{g}: {MOOT[g]}')
        else:
            gates.append(GATE_TXT.get(g, f'GATE {g} (open)'))
    root = GEN_ROOT.get(t, t)
    if t in HX:
        pass                        # Q-HX gate already carries it
    elif root not in GEN_TEE:
        gates.append(f'GATE TOOLCHAIN: no {t} SPEC in the batch-16 generators (puckfix tools_new gen_tee.py / gen_straight2.py) - new master not built yet')
    # ---------- 3D file rows
    if how == '3D file':
        stp = os.path.join(R, '09_STEP_FILES', f'BRENNAN_{c}.stp')
        if not os.path.exists(stp):
            gates.insert(0, f'HOLD needs STEP download: 09_STEP_FILES/BRENNAN_{c}.stp is not there (no Brennan catalog row; the file is the only size source)')
        else:
            gates.insert(0, 'STEP present - not measured in this pass')
        rowsout.append(dict(table=t, config=c, ready='no', missing_columns='every dimension column', gates=' ; '.join(gates), conflicts='',
                            notes='3D-file row: ' + '; '.join(f'{v}: {w}' for v, w in steps_ok(c))[:300]))
        continue
    cfgT = T[t]
    tab, crow = CAT[c]
    assert tab['table_id'] == cfgT['tid'], (c, tab['table_id'], cfgT['tid'])
    vals = crow['values']
    cite0 = (f'Brennan TFA catalog p.{tab["page"]} table {tab["table_id"]} "{tab["series"]} {tab["title"]}" row {c} col "{{col}}" = "{{raw}}" '
             f'(07_RAW_EXTRACTS/brennan_catalogs/TFA Catalog.pdf; tools/_out/brennan_catalog_20261001/catalog_verified.json, line_y {crow.get("line_y")}, '
             f'page verified {tab.get("verified")}) [Brennan = yes 2026-10-18] - {{mean}} (column mapping: REPORT.md, table {t})')
    oi = OMI.get(c)
    filled_any = False
    for col, ccol, mean in cfgT['dims']:
        if col not in hdr and not cfgT.get('newcols'):
            raise SystemExit(f'{t}: column {col} not in base header')
        if col in hdr and not empty(b.get(col)):
            # already in the base: check it against Brennan (informative)
            v = num(vals.get(ccol, ''))
            if v is not None and abs(float(b[col]) - v) > 0.011:
                conf.append(f'base {col} {b[col]} vs Brennan {ccol} {vals.get(ccol)} (base kept)')
            continue
        raw = vals.get(ccol, '')
        v = num(raw)
        if t == '2502' and 'Q-CONFLICT-2502-MS51506' in row['other_gates'] and col in ('M1@DRIVE', 'N1@DRIVE'):
            missing.append(col)
            conf.append(f'{col}: Brennan {ccol} {raw} = OMi; MS51506 differs (Q-CONFLICT-2502-MS51506) - left empty')
            continue
        if v is None:
            missing.append(col)
            if raw:
                conf.append(f'{col}: Brennan {ccol} prints "{raw}" (a range / not one value) - never averaged, left empty; A14 answered 2026-10-18 = measure the STEP' + (
                    f' (09_STEP_FILES/BRENNAN_{c}.stp IS present - not measured in this pass, row held by its other gates)' if os.path.exists(os.path.join(R, '09_STEP_FILES', f'BRENNAN_{c}.stp')) else f' (needs STEP 09_STEP_FILES/BRENNAN_{c}.stp)'))
            else:
                notes.append(f'{col}: Brennan {ccol} blank on this row')
            continue
        src = cite0.format(col=ccol, raw=raw, mean=mean)
        okind = 'brennan-dim'
        om = cfgT.get('omi', {}).get(col)
        if oi and om:
            ov = oi[1].get(om)
            if ov not in (None, ''):
                ovn = float(ov)
                omi_checks.append((t, c, col, ov, v))
                if abs(ovn - v) <= 0.0005:
                    src += f'; = OMi WebsitePartsInfo2026 Items!{OCOL[om]}{oi[0]} "{om}" = {ov} (same value; OMi and Brennan count as one source)'
                else:
                    conf.append(f'{col}: OMi Items!{OCOL[om]}{oi[0]} {ov} vs Brennan {ccol} {raw} - OMi wins (user 2026-09-25)')
                    src = (f'OMi WebsitePartsInfo2026 Items!{OCOL[om]}{oi[0]} "{om}" = {ov} (OMi outranks; Brennan {ccol} prints {raw} - conflict listed)')
                    v = ovn; okind = 'other'
        if cfgT.get('newcols') and col not in hdr:
            src += ' [column not in today\'s base table: add it (name proposed after the built analog; no SPEC reads it yet)]'
        if t in ('1504', '1602') and ccol in ('A2 DRILL', 'A3 DRILL'):
            conf.append(f'{col}: Brennan {ccol} {raw} proposed (only source for this part), BUT the OMi 2026-10-18 drawings of the sibling sizes print the stem bore '
                        f'0.01-0.02 smaller than the Brennan drill on 7 of 7 bores (1504-20-20, 1602-02/-04/-16/-20; mapping_evidence.txt) - flag for the user')
        mine.append(dict(table=t, config=c, column=col, value=fmt(v), source=src, kind=okind))
        filled_any = True
    for col, ccol in cfgT.get('unconf', []):
        if col in hdr and empty(b.get(col)):
            missing.append(col)
            conf.append(f'{col}: candidate Brennan {ccol} = {vals.get(ccol)} NOT proposed - mapping not confirmed (Air-Way rows of this table do not pair with {ccol}; see REPORT)')
    # ---------- end-library cells
    for col, kind, k in cfgT['ends']:
        dd = d[k]
        if kind == 'JICCHAIN':
            j = G.JIC.get(dd)
            chain = [('JIC_RELIEFL@DRIVE', j['RL']), ('JIC_THDZ@DRIVE', j['TZ']), ('JIC_CONEDIA@DRIVE', j['CD']), ('JIC_LANDL@DRIVE', j['LL']), ('JIC_SEATL@DRIVE', j['SL'])]
            x = (' - the -40 entry is NOT from MS33656J: JIC_MEAS_40 measured on the Brennan 2404-40-32 STEP (gen_straight2 JIC40_ASSUME); '
                 'open question Q-SIZE40-JIC (D: Brennan geometry recommended)') if dd == 40 else ''
            for cc, vv in chain:
                if empty(b.get(cc)):
                    mine.append(dict(table=t, config=c, column=cc, value=fmt(vv), source=f'end library: male JIC -{dd:02d} chain value {cc} = {fmt(vv)} (gen_straight2 JIC[{dd}]{x}) [Q-TRANSFER-ENDLIB yes 2026-10-08]', kind='endlib'))
            for cc, vv in (('RELIEFANG@DRIVE', 60), ('SEATB@DRIVE', 37)):
                if empty(b.get(cc)):
                    mine.append(dict(table=t, config=c, column=cc, value=str(vv), source=f'constant of the JIC end chain: every 2501 row of today\'s table carries {cc} = {vv} (60 deg relief ramp, 37 deg seat)', kind='endlib'))
            if dd == 40:
                gates.append('GATE Q-SIZE40-JIC (D, open; Brengan geometry recommended): -40 JIC end from the Brennan 2404-40-32 STEP (prepared) vs MS33656J'.replace('Brengan', 'Brennan'))
            continue
        if kind == 'NPTFCHAIN':
            if dd not in MS.NPTF:
                for cc in ('NPTF_E0@DRIVE', 'NPTF_E1@DRIVE', 'NPTF_L2@DRIVE', 'PIPEOD@DRIVE'):
                    if empty(b.get(cc)):
                        missing.append(cc)
                gates.append(f'GATE Q-NEW-ASME40 (open): no -{dd:02d} (2-1/2 NPT) row in ms51500.NPTF / no ENDL[{dd}] - {G.lib_gap("NPTF", dd)[:160]}; the own STEP 09_STEP_FILES/BRENNAN_{c}.stp is present (could be measured: not done here)')
            else:
                nps, tpi, Dp, E0, E1, L1, L2 = MS.NPTF[dd]
                for cc, vv in (('NPTF_E0@DRIVE', E0), ('NPTF_E1@DRIVE', E1), ('NPTF_L2@DRIVE', L2), ('PIPEOD@DRIVE', Dp)):
                    if empty(b.get(cc)):
                        mine.append(dict(table=t, config=c, column=cc, value=fmt(vv), source=f'end library: ms51500.NPTF[{dd}] {cc} = {vv} (ASME B1.20.1)', kind='endlib'))
            continue
        if col not in hdr or not empty(b.get(col)):
            continue
        if kind == 'NPTF':
            if dd not in MS.NPTF:
                missing.append(col); continue
            mine.append(dict(table=t, config=c, column=col, value=fmt(MS.NPTF[dd][2]), source=SRC_NPTF.format(d=dd, v=fmt(MS.NPTF[dd][2])), kind='endlib'))
        elif kind == 'NPSM':
            mine.append(dict(table=t, config=c, column=col, value=fmt(MS.NPTF[dd][2]), source=SRC_NPSM.format(d=dd, v=fmt(MS.NPTF[dd][2])), kind='endlib'))
        elif kind == 'JIC':
            mine.append(dict(table=t, config=c, column=col, value=fmt(G.JIC[dd]['TM']), source=SRC_JIC.format(d=dd, v=fmt(G.JIC[dd]['TM']), x=''), kind='endlib'))
        elif kind == 'ORB':
            mine.append(dict(table=t, config=c, column=col, value=fmt(G.ORB[dd]['TM']), source=SRC_ORB.format(d=dd, v=fmt(G.ORB[dd]['TM'])), kind='endlib'))
        elif kind == 'TAP':
            if dd in (24, 32):
                missing.append(col)
                g = f'Q-CONFLICT-TAPDRILL-{dd}'
                txt = GATE_TXT[g]
                if txt not in gates:
                    gates.append(txt)
                conf.append(f'{col}: -{dd} tap drill printed two ways by Air-Way (A9) - left empty (end library 2405 template has {G.FPT[dd]["TD"]})')
                continue
            tg = [g for g in ('Q-TRANSFER-TAPDRILL', 'Q-NEW-F1A-5504TAP') if g in row['other_gates']]
            gate = (f' [{tg[0]} = A1 answered YES 2026-10-18 (00_DOCS/ANSWERS_2026-10-18.md): Air-Way per-size tap drill on existing families]' if tg
                    else ' [Q-TRANSFER-ENDLIB yes 2026-10-08: tap drills from the end library; = A1 YES 2026-10-18]')
            mine.append(dict(table=t, config=c, column=col, value=fmt(G.FPT[dd]['TD']), source=SRC_TAP.format(d=dd, v=fmt(G.FPT[dd]['TD']), gate=gate), kind='endlib'))
    # ---------- thread callouts
    if cfgT.get('thr') and mine:
        for col, txt in cfgT['thr'](d).items():
            if col in hdr and empty(b.get(col)):
                mine.append(dict(table=t, config=c, column=col, value=txt, source=f'thread callouts from the part number dashes in the format of the table\'s other rows; = Brennan {tab["table_id"]} thread columns ({", ".join(k + " " + v for k, v in vals.items() if any(x in k for x in ("NPTF", "NPSM", "SAE")))}) and OMi Items Side 1 / 2 / 3 Thread', kind='other'))
    if mine:
        mine.append(dict(table=t, config=c, column='$COMMENT', value='2026-10-18 Brennan = yes (wave2 tee_elbow, staged, not shipped): sizes from the Brennan TFA catalog'
                         + (' (= OMi Items, one source)' if any('= OMi' in x['source'] for x in mine) else '') + ', end details from the end library; marked $PRP@DimSource BRENNAN (to undo: clear the BRENNAN cells, set the row MISSING, regenerate)',
                         source='note appended to the base $COMMENT', kind='other'))
    # remaining empty driving columns
    dimcols = [x[0] for x in cfgT['dims']] + [x[0] for x in cfgT['ends'] if x[1] not in ('JICCHAIN', 'NPTFCHAIN')]
    proposed = {x['column'] for x in mine}
    for col in dimcols:
        if col in hdr and empty(b.get(col)) and col not in proposed and col not in missing:
            missing.append(col)
    already = not mine and not missing
    if already and gates:
        notes.append('2026-10-08 gate(s) of this row, informative only (the base row is already complete and ' + str(b.get('$PRP@DataStatus')) + ', carrying its tap drill): ' + ' / '.join(gates))
        gates = []
    if c in GEN_BLOCK:
        gates.append(GEN_BLOCK[c])
    ready = 'yes' if (not gates and not missing) else 'no'
    if already:
        notes.insert(0, f'ALREADY COMPLETE IN BASE - nothing to add: every driving cell already filled in today\'s base (DataStatus {b.get("$PRP@DataStatus")}); Brennan catalog '
                     + ('agrees on every value' if not conf else 'differs: ' + '; '.join(conf)))
    cells += mine
    rowsout.append(dict(table=t, config=c, ready=ready, missing_columns=' ; '.join(missing), gates=' ; '.join(gates), conflicts=' ; '.join(conf), notes=' ; '.join(notes)))

with open(os.path.join(OUT, 'cells.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'column', 'value', 'source', 'kind']); w.writeheader(); w.writerows(cells)
with open(os.path.join(OUT, 'rows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes']); w.writeheader(); w.writerows(rowsout)
json.dump(omi_checks, open(os.path.join(HERE, 'omi_checks.json'), 'w'), indent=0)
k = collections.Counter(x['kind'] for x in cells)
print(len(cells), 'cells', dict(k), '|', len(rowsout), 'rows', collections.Counter(r['ready'] for r in rowsout))
print('OMi compared', len(omi_checks), 'equal', sum(1 for x in omi_checks if abs(float(x[3]) - x[4]) <= 0.0005))
for r in rowsout:
    if r['ready'] == 'yes' or r['conflicts']:
        print(r['table'], r['config'], r['ready'], '| miss', r['missing_columns'][:80], '| conf', r['conflicts'][:200], '| notes', r['notes'][:150])
