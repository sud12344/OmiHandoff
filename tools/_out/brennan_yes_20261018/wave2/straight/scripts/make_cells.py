"""make_cells.py (wave 2, group "straight", 2026-10-18)

Brief: tools/_out/brennan_yes_20261018/wave2/BRIEF.md. Rows: wave2/rows_straight.csv (87 rows, enumerated here - never a stated count).
User decision 2026-10-18: "yes use brennan but still differentiate the two in tables in case i need to change it later".
OMi values (07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx, Items) and Air-Way values already in a table win; Brennan fills EMPTY
cells only. No review table is edited here: the main session applies ../cells.csv with apply_brennan.py (it sets DataStatus / DimSource /
AxialSource itself, so those three columns are never in the cell list).

Inputs (read only):
  - base tables  brennan_yes_20261018/base_root/04_DESIGN_TABLES (header row 2, part number column A)
  - Brennan catalog parse  brennan_catalog_20261001/catalog_verified.json (page-verified tables)
  - column-mapping evidence: ../pairing.json (scripts/pairing.py, today's base) + the catalog-drawing pairings recorded in
    brennan_catalog_20261001/impact/F2a / F2b / F45D / F3.json
  - OMi Items sheet
  - end libraries: batch-16 gen_straight2 (puckfix_20261009/tools_new/generators) imported read-only against the base tables
  - STEP measurement ../measure/bulkhead_I1.json (scripts/measure_bulkhead.py, validated on Brennan 2705-08-08 = Air-Way I1 1.44)
Outputs: ../cells.csv, ../rows.csv, ../rows_scenarioB.csv (informative: rows whose data is complete but are held by a decision)
"""
import os, sys, csv, json, re, math
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
W2 = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\wave2')
OUT = os.path.join(W2, 'straight')
BASE_ROOT = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root')
BASE = os.path.join(BASE_ROOT, '04_DESIGN_TABLES')
TOOLS = os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new')
STEPS = os.path.join(ROOT, '09_STEP_FILES')
B = '[Brennan = yes 2026-10-18]'

os.environ['OMI_ROOT'] = BASE_ROOT
os.environ['GS_OUT'] = os.path.join(OUT, r'test\_libimport'); os.environ['GT_OUT'] = os.environ['GS_OUT']
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(TOOLS, 'generators'))
import gen_straight2 as G          # noqa: E402  read-only use of JIC / NPTF / ENDL / FPT / ORB / npt_thr / ORBF_MEAS / JICF_MEAS

ROWS_IN = list(csv.DictReader(open(os.path.join(W2, 'rows_straight.csv'), encoding='utf-8')))
print(len(ROWS_IN), 'rows in rows_straight.csv')

# ---------------------------------------------------------------- Brennan catalog
CATJ = json.load(open(os.path.join(ROOT, r'tools\_out\brennan_catalog_20261001\catalog_verified.json'), encoding='utf-8'))
CAT = {}
for t in CATJ['tables']:
    for r in t['rows']:
        CAT.setdefault(r['pn'], []).append((t, r))


def cat(pn):
    h = CAT.get(pn, [])
    assert len(h) <= 1, (pn, len(h))
    return h[0] if h else (None, None)


def catv(pn, col):
    t, r = cat(pn)
    assert t is not None and t.get('verified') is True and not r.get('warnings'), (pn, col)
    s = r['values'][col]
    return float(s), s, (f"Brennan TFA catalog p{t['page']} table {t['table_id']} \"{t['series']} {t['title']}\" row {pn} col \"{col}\" = \"{s}\" "
                         f"(07_RAW_EXTRACTS/brennan_catalogs/TFA Catalog.pdf; brennan_catalog_20261001/catalog_verified.json, line_y {r['line_y']}, page verified)")


# ---------------------------------------------------------------- OMi Items
OWS = openpyxl.load_workbook(os.path.join(ROOT, r'07_RAW_EXTRACTS\omi_dimensions\WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)['Items']
OMI = {}
for i, r in enumerate(OWS.iter_rows(values_only=True), 1):
    if r[0]:
        OMI.setdefault(str(r[0]).strip(), []).append((i, r))
OHDR = {11: 'Overall Length', 12: 'Body Diameter', 17: 'Hex Flat', 18: 'Side 1 ID', 19: 'Side 1 Size', 20: 'Side 1 Thread', 21: 'Nut Hex 1',
        23: 'Side 2 ID', 25: 'Side 2 Size', 26: 'Side 2 Thread'}
LET = lambda j: chr(ord('A') + j)
DIMCOLS = (11, 12, 13, 14, 15, 16, 17, 18, 21, 23, 24, 28)


def omi_row(pn):
    h = OMI.get(pn, [])
    assert len(h) == 1, (pn, 'OMi rows', len(h))
    return h[0]


def omi_dims(pn):
    i, r = omi_row(pn)
    return i, {j: r[j] for j in DIMCOLS if r[j] not in (None, '') and str(r[j]).strip().upper() != 'NA'}


def omiv(pn, j):
    i, r = omi_row(pn)
    return float(r[j]), f'OMi WebsitePartsInfo2026.xlsx Items!{LET(j)}{i} "{OHDR[j]}" = {r[j]}'


# ---------------------------------------------------------------- base tables
TBL = {}


def base(t):
    if t not in TBL:
        ws = openpyxl.load_workbook(os.path.join(BASE, f'DesignTable_{t}.xlsx')).active
        hdr = [c.value for c in ws[2]]
        rows = {}
        for k in range(3, ws.max_row + 1):
            pn = ws.cell(k, 1).value
            if pn:
                rows[str(pn).strip()] = {h: ws.cell(k, j + 1).value for j, h in enumerate(hdr) if h}
        TBL[t] = (hdr, rows)
    return TBL[t]


def empty(v):
    return v is None or (isinstance(v, str) and v.strip() == '')


# ---------------------------------------------------------------- mapping evidence (printed into each brennan-dim source)
PAIR = json.load(open(os.path.join(OUT, 'pairing.json'), encoding='utf-8'))
DRAW = {   # catalog drawing reading (impact F2a / F2b / F45D / F3 pairings, page-verified)
    '2403': 'TFA p5 2403 drawing: L = overall, C HEX = body hex, B1/B2 DRILL = bore at end B1/B2 (impact/F2a.json, pairing certain)',
    '2403LH': 'TFA p5 2403-LH drawing: L = overall, C HEX = the large body hex, B1/B2 DRILL = bores (impact/F2a.json, certain)',
    '2404L': 'TFA p6 2404-L drawing: L = overall, C HEX = body hex, B1 DRILL = JIC-end bore (certain), A2 DRILL = pipe-end bore (likely) (impact/F2a.json)',
    '2405': 'TFA p7 2405 drawing: L = overall, C HEX = body hex, B1 DRILL = through bore from the JIC end (impact/F2a.json, certain)',
    '2406': 'TFA p7 2406 drawing: L0 spans the whole part (female face to male JIC tip), C HEX = body hex, B2 DRILL = male-end bore (impact/F2a.json certain; drawing re-read 2026-10-18, verify/png/TFA_p07_RT.png)',
    '2700': 'TFA p8 2700 drawing: L = overall, C HEX = body hex, B1/B2 DRILL = bores (impact/F2a.json, certain)',
    '2706': 'TFA p9 2706 drawing: L = overall, C1 HEX = body hex, A1 DRILL = pipe-end bore, B2 DRILL = bulkhead-end bore (impact/F2a.json certain; = OMi M059-M062)',
    '5000': 'TFA p10 5000 drawing: L = overall, C HEX = body hex (impact/F2a.json, certain)',
    '5404': 'TFA p11 5404 drawing: L = overall, C HEX = body hex, A1/A2 DRILL = bores (impact/F2a.json, certain)',
    '5404N': 'TFA p11 5404-N drawing: L = overall (= the cut length in the part number), A1/A2 DRILL = through drill at each end (impact/F2b.json, certain)',
    '5405': 'TFA p12 5405 drawing: L = overall, C HEX = body hex, A1 DRILL = male-end bore = SPEC 5405 bore D (impact/F2b.json, certain)',
    '5406': 'TFA p13 5406 drawing: L = overall, C HEX = bushing hex (impact/F2b.json, certain); A1 DRILL is NOT a printed tap drill (likely only)',
    '5406C': 'TFA p66 5406-C drawing: L = whole closed cap, C HEX = cap hex (impact/F2b.json, certain role; Air-Way caps of the other sizes differ, 0/6)',
    '6400': 'TFA p14 6400-O drawing: L5 = JIC tip to ORB end face (overall), C4 HEX = body hex, B1 DRILL = JIC end, B2 DRILL = ORB end (impact/F45D.json, certain)',
    '6405': 'TFA p15 6405-O drawing: L = overall, C4 HEX = body hex, B DRILL = drill from the ORB end = D3 (impact/F2b.json, certain)',
    '6410': 'TFA p16 6410-O drawing: L = overall, C4 HEX = body hex, B DRILL = drill from the male ORB end = D (impact/F2b.json, certain)',
}


def pairtxt(t, col):
    p = PAIR.get(t, {}).get(col)
    if not p:
        return 'no same-table pair to compare'
    return (f"same-table check on today's base: {p['eq'] + p['rnd']}/{p['n']} rows with an Air-Way/OMi value agree with this catalog column to rounding"
            + (f" ({len(p['diff'])} differ, e.g. {p['diff'][0][0]} {p['diff'][0][2]} vs {p['diff'][0][3]})" if p['diff'] else ''))


CELLS, ROWS, CONFLICTS, SCEN_B, EDITS = [], [], [], [], []


def add(t, pn, col, val, src, kind):
    hdr, rows = base(t)
    cur = rows[pn].get(col) if col in hdr else None
    assert col not in ('$PRP@DataStatus', '$PRP@DimSource', '$PRP@AxialSource'), col
    if col != '$COMMENT' and not empty(cur):
        raise SystemExit(f'not empty in base: {t} {pn} {col} = {cur!r} (proposed {val!r})')
    if col not in hdr and col != '$COMMENT':
        src += ' [column not in today\'s base table: add it]'
    CELLS.append(dict(table=t, config=pn, column=col, value=val, source=src, kind=kind))


def cat_cell(t, pn, col, ccol, what):
    v, s, src = catv(pn, ccol)
    add(t, pn, col, v, f'{src} {B} - {what}; mapping: {DRAW[t]}; {pairtxt(t, col)}', 'brennan-dim')
    return v


def thr_eq(cat_s, lib_s):
    a = re.sub(r'\s*(UN-2B|UNF-2B|NPTF)\s*$', '', str(cat_s).strip())
    a = re.sub(r'^(\d+)[- ](\d+/\d+)', r'\1 \2', a).replace('-11-1/2', '-11 1/2').replace('-11 1/2', '-11 1/2')
    return a == str(lib_s).strip()


JICSRC = 'end library gen_straight2 JIC[{d}] (= tools_new/generators/templates/DesignTable_2403_SW2.xlsx, MS33656J chain, VERIFIED vs Brennan) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
NPSRC = 'end library: ASME B1.20.1 / B1.20.3 {nps} NPT basic dimensions = tools_new/generators/ms51500.NPTF[{d}] [Q-TRANSFER-ENDLIB yes 2026-10-08]'
FPTSRC = ('end library gen_straight2 FPT[{d}] (= tools_new/generators/templates/DesignTable_2405_SW2.xlsx row of that pipe dash: TAPDRILL@BORE_A {td}, '
          'FPT_P1 {p1} = MS51503 P1 max)')
TAPGATE = ' = Air-Way per-size tap drill (-02 0.33 ... -20 1.48) [user 2026-10-18 A1 Q-TRANSFER-TAPDRILL yes, 00_DOCS/ANSWERS_2026-10-18.md]'
A9 = 'Q-CONFLICT-TAPDRILL-{d} (A9, still open: -24 1.72 / 1.70, -32 2.20 / 2.19)'


def tapsrc(d):
    return TAPGATE if d <= 20 else ' - end-library value; ' + A9.format(d=d) + ' keeps this cell provisional'


def a9(g, *ds):
    for d in ds:
        if d > 20 and f'Q-CONFLICT-TAPDRILL-{d}' not in ' '.join(g):
            g.append(A9.format(d=d))
    return g


def jic_chain(t, pn, prefix, d):
    e = G.JIC[d]
    for col, k in ((f'{prefix}_RELIEFL@DRIVE', 'RL'), (f'{prefix}_THDZ@DRIVE', 'TZ'), (f'{prefix}_CONEDIA@DRIVE', 'CD'), (f'{prefix}_LANDL@DRIVE', 'LL'), (f'{prefix}_SEATL@DRIVE', 'SL')):
        add(t, pn, col, round(e[k], 5), JICSRC.format(d=d) + f' {k} (end detail per dash)', 'endlib')


def jic_consts(t, pn):
    add(t, pn, 'RELIEFANG@DRIVE', 60, 'gen_straight2 end_JICM constant 60 deg relief ramp (the value on every built row of this table) [Q-TRANSFER-ENDLIB yes]', 'endlib')
    add(t, pn, 'SEATB@DRIVE', 37, 'gen_straight2 end_JICM constant 37 deg flare seat (the value on every built row of this table) [Q-TRANSFER-ENDLIB yes]', 'endlib')


def comment(t, pn, text):
    add(t, pn, '$COMMENT', f'2026-10-18 Brennan = yes (wave 2 straight, staged, not shipped): {text}', 'appended to the base note (apply_brennan appends, never replaces)', 'other')


def row(t, pn, ready, missing, gates, conflicts, notes, scenB=False):
    ROWS.append(dict(table=t, config=pn, ready='yes' if ready else 'no', missing_columns=' ; '.join(missing), gates=' ; '.join(gates),
                     conflicts=' ; '.join(conflicts), notes=notes))
    if scenB:
        SCEN_B.append((t, pn))


# user answers 2026-10-18 (00_DOCS/ANSWERS_2026-10-18.md, group A): decided YES -> no longer gates (A9 -24/-32 tap drill stays open)
DECIDED = {'Q-TRANSFER-TAPDRILL': 'A1', 'Q-6900-IDENT': 'A3', 'Q-TRANSFER-5404N': 'A4', 'Q-NEW-5404N-NAME': 'A4 (keep OMi form)', 'Q-NEW-AWALIAS': 'A4',
           'Q-CAT-5404N-BORE': 'A4 (bore = Air-Way nipple of the same size)', 'Q-TRANSFER-I1': 'A8', 'Q-TRANSFER-LN': 'A10', 'Q-TRANSFER-D3': 'A11',
           'Q-BOREWIDE': 'A11 (cap at the port drill)', 'Q-PLACEHOLDER': 'OMi answer 2026-10-18 (6410-32-20-O real length 1.43)', 'Q-TRANSFER-ORBGW': 'A18',
           'Q-TRANSFER-ENDLIB': '2026-10-08', 'Q-B-OTHER': 'catalog', 'Q-B-OTHER-6420': 'catalog'}
# STEP gates that were only the alternative to a tap drill / placeholder now decided (impact/F2a.md, F2b.md: "nothing if Q-TRANSFER-TAPDRILL = yes")
STEP_ALT_TABLES = {'2405', '5000', '5405', '5406', '5406C', '6405', '6410'}
DECIDED_SEEN = {}


def gates_of(r):
    g = [x.strip() for x in r['other_gates'].replace('|', ';').split(';') if x.strip()]
    out = []
    for x in g:
        if x in DECIDED:
            DECIDED_SEEN.setdefault(r['config'], []).append(f'{x} = yes ({DECIDED[x]})')
            continue
        if x.startswith('STEP:') and r['table'] in STEP_ALT_TABLES:
            DECIDED_SEEN.setdefault(r['config'], []).append(f'{x} not needed (it was the alternative to a decision now answered)')
            continue
        if x.startswith('STEP:'):
            p = x[5:]
            have = os.path.exists(os.path.join(STEPS, f'BRENNAN_{p}.stp'))
            out.append(f'{x} ({"file present" if have else "needs STEP download: 09_STEP_FILES/BRENNAN_" + p + ".stp"})')
        else:
            out.append(x)
    return list(dict.fromkeys(out))


MEAS = json.load(open(os.path.join(OUT, r'measure\bulkhead_I1.json'), encoding='utf-8'))
NOFILE = set('1405-20-24 2403-06-02 2406-06-12 2700-04-02 2700-08-06 2700-10-08 2700-12-10 2705-04-02 5404-L-04X2.000 5404-R-04-04-047'.split())  # 3D_FILES_NEEDED.md "Brennan has no file"

done = set()
BY = {r['config']: r for r in ROWS_IN}


def G_(pn):
    return gates_of(BY[pn])


# ============================================================ 0304-C-02 / 0306-02 (already OMi-filled; only the shape is missing)
for t, pn, cols in (('0304', '0304-C-02', (('L@DRIVE', 'L LGTH'), ('CHEX@HEX', 'C HEX'))), ('0306', '0306-02', (('h2@DRIVE', 'W WIDTH'), ('S4@DRIVE', 'C HEX')))):
    hdr, rows = base(t); cur = rows[pn]
    chk = []
    for col, cc in cols:
        v, s, _ = catv(pn, cc)
        chk.append(f'{col} base {cur[col]} (OMi) vs Brennan {cc} {s}: ' + ('equal' if abs(float(cur[col]) - v) <= 0.0051 else 'DIFFERS'))
    row(t, pn, False, [], G_(pn) + ['GENERATOR: no female -02 JIC geometry (gen_straight2: "needs a Brennan STEP with a female -02 JIC thread + seat (BRENNAN_' + pn + ' or a 2406-02-xx)")'],
        [], 'no empty cell to fill: the row is already ASSUMED with OMi values; Brennan catalog cross-check ' + '; '.join(chk) + '. Only the STEP (shape) is missing.')
    done.add(pn)

# ============================================================ rows with no data source at all (3D-file rows without a STEP)
for r in ROWS_IN:
    pn, t = r['config'], r['table']
    if r['how'] != '3D file' or pn in ('2705-04-02', '2705-LN-04-02'):
        continue
    have = os.path.exists(os.path.join(STEPS, f'BRENNAN_{pn}.stp'))
    assert not have, pn
    i, od = omi_dims(pn)
    assert not od, (pn, od)
    why = ('Brennan has no 3D file for this part (3D_FILES_NEEDED.md "Not to ask for")' if pn in NOFILE else
           f'needs STEP download: 09_STEP_FILES/BRENNAN_{pn}.stp (3D_FILES_NEEDED.md section 2)' if pn in ('5404-L-04X3.000', '5404-L-04X4.000') else
           f'needs STEP download / no Brennan file listed (the plain part {pn.replace("-LN", "")} has none either)')
    row(t, pn, False, ['every dimension column'], G_(pn) + [why], [], f'no source: not in the Brennan catalog, no Brennan STEP in 09_STEP_FILES, OMi Items row {i} gives no dimension, no Air-Way row. Nothing prepared.')
    done.add(pn)

# ============================================================ 2403 (male JIC x male JIC union)
for pn in ('2403-04-02', '2403-10-04', '2403-16-10', '2403-24-16'):
    t = '2403'; a, b = G.dashes(pn)
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[a]['thr']) and thr_eq(rr['values']['B2 SAE 37Deg'], G.JIC[b]['thr']), (pn, rr['values'])
    cat_cell(t, pn, 'L1@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'HEXB@HEX', 'C HEX', 'body hex across flats')
    cat_cell(t, pn, 'D1@BORE', 'B1 DRILL', 'bore at end A (first dash)'); cat_cell(t, pn, 'D2@BORE', 'B2 DRILL', 'bore at end B (second dash)')
    add(t, pn, 'THDMAJ_A@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + f" thread major; catalog B1 {rr['values']['B1 SAE 37Deg']}", 'endlib')
    add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + f" thread major; catalog B2 {rr['values']['B2 SAE 37Deg']}", 'endlib')
    jic_chain(t, pn, 'JICA', a); jic_chain(t, pn, 'JICB', b); jic_consts(t, pn)
    add(t, pn, '$PRP@EndA_Thread', G.JIC[a]['thr'], JICSRC.format(d=a) + ' thread text (format of the built 2403 rows)', 'endlib')
    add(t, pn, '$PRP@EndB_Thread', G.JIC[b]['thr'], JICSRC.format(d=b) + ' thread text', 'endlib')
    comment(t, pn, f'L1 / hex / D1 / D2 from the Brennan TFA catalog p5 alone (no OMi dimension, no Air-Way row); JIC ends from the end library')
    row(t, pn, True, [], [], [], f'Brennan TFA p5 {tt["table_id"]}; JIC chains from the end library; OMi Items row {i}: no dimension')
    done.add(pn)

# ============================================================ 2403-LH-24-24 (large-hex union, folded into 2403)
pn, t = '2403-LH-24-24', '2403LH'
i, od = omi_dims(pn); assert not od
tt, rr = cat(pn)
assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[24]['thr']) and thr_eq(rr['values']['B2 SAE 37Deg'], G.JIC[24]['thr']), rr['values']
cat_cell(t, pn, 'L1@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'C2HEX@HEX', 'C HEX', 'large body hex')
cat_cell(t, pn, 'D1@BORE', 'B1 DRILL', 'bore end B1'); cat_cell(t, pn, 'D2@BORE', 'B2 DRILL', 'bore end B2')
for col in ('THDMAJ_B1@DRIVE', 'THDMAJ_B2@DRIVE'):
    add(t, pn, col, G.JIC[24]['TM'], JICSRC.format(d=24) + ' thread major (1 7/8-12)', 'endlib')
add(t, pn, '$PRP@Threads', '1 7/8-12 x 1 7/8-12 (male JIC, large hex)', JICSRC.format(d=24) + ' thread texts, format of the built 2403LH rows', 'endlib')
comment(t, pn, 'L1 / large hex / bores from the Brennan TFA catalog p5 alone; JIC ends from the 2403 end library (load_2403 fold)')
row(t, pn, True, [], [], [], f'Brennan TFA p5 {tt["table_id"]}; folds into the 2403 master (load_2403); OMi Items row {i}: no dimension')
done.add(pn)

# ============================================================ 2404-L-32-32 (long male connector; hand-made 2404 master - Q-HANDMADE)
pn, t = '2404-L-32-32', '2404L'
i, od = omi_dims(pn); assert not od
tt, rr = cat(pn)
assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[32]['thr']) and thr_eq(rr['values']['A2 NPTF'], G.npt_thr(32)), rr['values']
cat_cell(t, pn, 'L20@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'CHEX@HEX', 'C HEX', 'body hex')
cat_cell(t, pn, 'D@BORE', 'B1 DRILL', 'JIC-end bore'); cat_cell(t, pn, 'D1@BORE', 'A2 DRILL', 'pipe-end bore (pairing "likely": Air-Way D1 agrees on 3/8 only - Brennan drills the pipe end smaller on -06/-08/-12, Q-2404-BORE)')
add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[32]['TM'], JICSRC.format(d=32) + ' JIC thread major (2 1/2-12)', 'endlib')
add(t, pn, 'THDMAJ_A@DRIVE', G.NPTF[32][2], NPSRC.format(nps=G.NPTF[32][0], d=32) + ' pipe OD', 'endlib')
add(t, pn, '$PRP@Threads', '2 1/2-12 (JIC) x 2-11 1/2 (NPTF) long pattern', 'thread texts from the part-number dashes (JIC[32] / NPTF[32]), format of the built 2404L rows', 'endlib')
comment(t, pn, 'L20 / hex / bores from the Brennan TFA catalog p6 alone; T20REF (Air-Way hex-length reference) not printed by Brennan - left empty (the generator only uses it as a check)')
row(t, pn, False, ['T20REF@REF (reference only, not needed)'], G_(pn), [],
    'values prepared; held by Q-HANDMADE (the 2404 / 2404-L master is the user\'s hand-built one). Own STEP 09_STEP_FILES/BRENNAN_2404-L-32-32.stp present (overall checked below in REPORT)', scenB=True)
done.add(pn)

# ============================================================ 2405 (female pipe x male JIC) - tap drill gate
for pn in ('2405-10-06', '2405-14-12'):
    t = '2405'; a, b = G.dashes(pn)        # a = JIC, b = pipe
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[a]['thr']) and thr_eq(rr['values']['A2 NPTF'], G.npt_thr(b)), rr['values']
    cat_cell(t, pn, 'L2@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'HEXB@HEX', 'C HEX', 'body hex'); cat_cell(t, pn, 'D3@BORE_THRU', 'B1 DRILL', 'through bore from the JIC end')
    add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major', 'endlib')
    jic_chain(t, pn, 'JIC', a); jic_consts(t, pn)
    f = G.FPT[b]
    add(t, pn, 'FPT_P1@DRIVE', f['P1'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + ' - port depth = MS51503 P1 max per pipe dash (end detail) [Q-TRANSFER-ENDLIB yes]', 'endlib')
    add(t, pn, 'TAPDRILL@BORE_A', f['TD'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + TAPGATE, 'endlib')
    add(t, pn, '$PRP@EndA_Thread', f['thr'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + ' thread text', 'endlib')
    add(t, pn, '$PRP@EndB_Thread', G.JIC[a]['thr'], JICSRC.format(d=a) + ' thread text', 'endlib')
    comment(t, pn, 'L2 / hex / D3 from the Brennan TFA catalog p7 alone; JIC end + port depth from the end library; tap drill = Air-Way per size (A1 yes)')
    g = G_(pn)
    row(t, pn, not g, [], g, [], 'every cell prepared; tap drill = Air-Way per-size value (A1 yes 2026-10-18); STEP gate was only the alternative to A1')
    done.add(pn)

# ============================================================ 2406-03-04 (female JIC -03 x male JIC -04)
pn, t = '2406-03-04', '2406'
a, b = G.dashes(pn)
i, od = omi_dims(pn); assert not od
tt, rr = cat(pn)
assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[a]['thr']) and thr_eq(rr['values']['B2 SAE 37Deg'], G.JIC[b]['thr']), rr['values']
assert a in G.JICF_MEAS, 'female -03 port'
cat_cell(t, pn, 'L23@DRIVE', 'L0 LGTH', 'overall length'); cat_cell(t, pn, 'HEXB@HEX', 'C HEX', 'body hex'); cat_cell(t, pn, 'D3@BORE', 'B2 DRILL', 'male-end bore')
add(t, pn, 'THDMAJ_A@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major of the female end (first dash)', 'endlib')
add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major of the male end (second dash)', 'endlib')
jic_chain(t, pn, 'JICB', b); jic_consts(t, pn)
add(t, pn, '$PRP@EndA_Thread', f"{G.JIC[a]['thr']} (female JIC)", JICSRC.format(d=a) + ' thread text (format of the built 2406 rows)', 'endlib')
add(t, pn, '$PRP@EndB_Thread', G.JIC[b]['thr'], JICSRC.format(d=b) + ' thread text', 'endlib')
comment(t, pn, 'L23 / hex / D3 from the Brennan TFA catalog p7 alone (built 2406 rows are Air-Way; Brennan L0 equals their L23 on 16/47 only - different bodies, see wave2 REPORT); '
        'female -03 port = JICF_MEAS[3] (Brennan 2406-03-04 STEP, already in the end library)')
row(t, pn, True, [], [], [], f'Brennan TFA p7 {tt["table_id"]}; female -03 port in JICF_MEAS (measured on this part\'s own STEP); OMi Items row {i}: no dimension')
done.add(pn)

# ============================================================ 2700-02-02 / 2700-LN-02-02 (JIC x JIC bulkhead -02)
for pn in ('2700-02-02', '2700-LN-02-02'):
    t = '2700'; src_pn = '2700-02-02'
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(src_pn)
    assert thr_eq(rr['values']['B1 SAE 37Deg'], G.JIC[2]['thr']) and thr_eq(rr['values']['B2 SAE 37Deg'], G.JIC[2]['thr'])
    ln = pn != src_pn
    lnnote = ' [the -LN part = the plain 2700-02-02 + a locknut: Q-TRANSFER-LN open]' if ln else ''
    for col, cc, what in (('L4@DRIVE', 'L LGTH', 'overall length'), ('C2HEX@HEX', 'C HEX', 'body hex'), ('D1@BORE', 'B1 DRILL', 'bore end B1'), ('D2@BORE', 'B2 DRILL', 'bore end B2 (bulkhead)')):
        v, s, src = catv(src_pn, cc)
        add(t, pn, col, v, f'{src} {B} - {what}{lnnote}; mapping: {DRAW[t]}; {pairtxt(t, col)}', 'brennan-dim')
    m = MEAS['2700-02-02']
    add(t, pn, 'I1@DRIVE', m['I1'], (f"own Brennan STEP 09_STEP_FILES/BRENNAN_2700-02-02.stp (sha256 {m['sha256'][:16]}...) measured with wave2/straight/scripts/measure_bulkhead.py "
                                      f"(prof.py section; validated: Brennan 2705-08-08 gives I1 1.44 = Air-Way): bulkhead tip {m['tip']} - relief start {m['relief_start']} "
                                      f"(after the 0.04 collar) = {m['I1']}; the -02 nose on the STEP = MS33656J JIC[2] (seat {m['SL']}, land {m['LL']}, relief {m['RL']}); "
                                      f"STEP overall {m['overall']} = catalog L 1.870, hex {m['hex_af_from_corners']} = catalog 0.562 {B}{lnnote}"), 'brennan-dim')
    for col in ('THDMAJ_B1@DRIVE', 'THDMAJ_B2@DRIVE'):
        add(t, pn, col, G.JIC[2]['TM'], JICSRC.format(d=2) + ' thread major (5/16-24)', 'endlib')
    add(t, pn, '$PRP@Threads', '5/16-24 x 5/16-24 (JIC) + bulkhead', JICSRC.format(d=2) + ' thread texts, format of the built 2700 rows', 'endlib')
    comment(t, pn, 'L4 / hex / bores from the Brennan TFA catalog p8, I1 measured on the Brennan 2700-02-02 STEP (no Air-Way -02 bulkhead)' + (' - copied from the plain part (Q-TRANSFER-LN)' if ln else ''))
    if ln:
        g = G_(pn)
        row(t, pn, not g, [], g, [], 'values = the plain 2700-02-02 (catalog + its STEP) [A10 Q-TRANSFER-LN yes: -LN = the plain part, locknut not modelled]')
    else:
        row(t, pn, True, [], [], [], f'Brennan TFA p8 {tt["table_id"]} + I1 from the part\'s own STEP; OMi Items row {i}: no dimension')
    done.add(pn)

# ============================================================ 2705-04-02 / 2705-LN-04-02 (female pipe x JIC bulkhead -02): OMi dims, no I1
for pn in ('2705-04-02', '2705-LN-04-02'):
    t = '2705'; a, b = G.dashes(pn)      # a = pipe -04, b = bulkhead JIC -02
    i, orow = omi_row(pn)
    for col, j in (('L24@DRIVE', 11), ('C5HEX@HEX', 17), ('D@BORE', 23)):
        v, src = omiv(pn, j)
        add(t, pn, col, v, f'{src} (OMi first, user 2026-09-25; mapping impact/F2a.json M056-M058 certain); no Brennan catalog row or STEP for this part', 'other')
    f = G.FPT[a]
    add(t, pn, 'TAPDRILL@BORE', f['TD'], FPTSRC.format(d=a, td=f['TD'], p1=f['P1']) + TAPGATE, 'endlib')
    add(t, pn, 'THDMAJ_A@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a) + ' pipe OD', 'endlib')
    add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major', 'endlib')
    comment(t, pn, 'L24 / hex / D from OMi Items; I1 (the -02 bulkhead length) has no source: no Brennan file exists for this part, and the two -02 bulkhead STEPs disagree (2700-02-02 1.07, 2706-04-02 1.11), so no per-size transfer')
    g = G_(pn) + ['MISSING I1@DRIVE: no Brennan 2705-04-02 file exists (3D_FILES_NEEDED "not to ask for"); A8 (Q-TRANSFER-I1 yes) takes Air-Way\'s per-size I1, but Air-Way has no -02 bulkhead; '
                  'the two measured Brennan -02 bulkheads differ (2700-02-02 1.07, 2706-04-02 1.11) - choosing one would be a pick between sources (user)']
    row(t, pn, False, ['I1@DRIVE'], g, [], 'OMi gives L / hex / bore; tap drill and threads prepared from the end library')
    done.add(pn)

# ============================================================ 2706-04-02 / 2706-LN-04-02 (male pipe -04 x JIC bulkhead -02)
for pn in ('2706-04-02', '2706-LN-04-02'):
    t = '2706'; a, b = G.dashes(pn)
    i, orow = omi_row(pn)
    tt, rr = cat('2706-04-02')
    assert thr_eq(rr['values']['A1 NPTF'], G.npt_thr(a)) and thr_eq(rr['values']['B2 SAE 37Deg'], G.JIC[b]['thr'])
    ln = pn != '2706-04-02'
    conf = []
    for col, j, cc in (('L25@DRIVE', 11, 'L LGTH'), ('C2HEX@HEX', 17, 'C1 HEX'), ('D1@BORE', 18, 'A1 DRILL'), ('D@BORE', 23, 'B2 DRILL')):
        v, src = omiv(pn, j); cv, cs, csrc = catv('2706-04-02', cc)
        tag = 'equal' if abs(v - cv) < 1e-9 else 'rounding only' if abs(v - cv) <= 0.0051 else 'DIFFERS'
        if tag == 'DIFFERS':
            conf.append(f'{col} OMi {v} vs Brennan {cs}'); CONFLICTS.append(dict(table=t, config=pn, column=col, kept=f'OMi {v}', other=f'Brennan {cs}'))
        add(t, pn, col, v, f'{src} (OMi first, user 2026-09-25; mapping impact/F2a.json M059-M062 certain); cross-check {csrc}: {tag}', 'other')
    m = MEAS['2706-04-02']
    add(t, pn, 'I1@DRIVE', m['I1'], (f"own Brennan STEP 09_STEP_FILES/BRENNAN_2706-04-02.stp (sha256 {m['sha256'][:16]}...) measured with wave2/straight/scripts/measure_bulkhead.py "
                                      f"(validated on Brennan 2705-08-08 = Air-Way I1 1.44): bulkhead tip {m['tip']} - relief start {m['relief_start']} = {m['I1']}; "
                                      f"STEP overall {m['overall']} = OMi / catalog 1.980, hex {m['hex_af_from_corners']} = 0.625 {B}"
                                      + (' [the -LN part = the plain 2706-04-02 + a locknut: Q-TRANSFER-LN open]' if ln else '')), 'brennan-dim')
    add(t, pn, 'THDMAJ_A@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a) + f' pipe OD; OMi Items!U{i} "{orow[20]}"', 'endlib')
    add(t, pn, 'THDMAJ_B@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + f' thread major; OMi Items!AA{i} "{orow[26]}"', 'endlib')
    add(t, pn, '$PRP@TubeOD', '1/8', f"Brennan TFA p9 {tt['table_id']} row 2706-04-02 col \"TUBE O.D.\" = \"{rr['values']['TUBE O.D.']}\" (= the -02 JIC tube; format of the built 2706 rows)", 'other')
    add(t, pn, '$PRP@Threads', f"{G.npt_thr(a)} (A NPTF) x {G.JIC[b]['thr']} (B UN/UNF-2A)", 'thread texts from the part-number dashes (NPTF[4] / JIC[2]), format of the built 2706 rows', 'endlib')
    comment(t, pn, 'L25 / hex / bores from OMi Items (= Brennan TFA p9); I1 measured on the Brennan 2706-04-02 STEP (no Air-Way -02 bulkhead)' + (' - copied from the plain part (Q-TRANSFER-LN)' if ln else ''))
    if ln:
        g = G_(pn)
        row(t, pn, not g, [], g, conf, f'OMi gives this -LN part\'s own L / hex / bores (Items row {i}, = the plain part); I1 from the plain part\'s STEP [A10 Q-TRANSFER-LN yes]')
    else:
        row(t, pn, True, [], [], conf, f'OMi Items row {i} (= Brennan TFA p9); I1 from the part\'s own STEP')
    done.add(pn)

# ============================================================ 5000 (female pipe coupling)
for pn in ('5000-06-02', '5000-16-08', '5000-24-20', '5000-40-40'):
    t = '5000'; a, b = G.dashes(pn)
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    cat_cell(t, pn, 'L@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'CHEX@HEX', 'C HEX', 'body hex')
    miss, g = [], G_(pn)
    for col_td, col_maj, d in (('TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE', a), ('TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE', b)):
        if d in G.FPT:
            assert thr_eq(rr['values']['A1 NPTF' if col_td == 'TAPDRILL1@BORE' else 'A2 NPTF'], G.npt_thr(d)), (pn, rr['values'])
            f = G.FPT[d]
            add(t, pn, col_td, f['TD'], FPTSRC.format(d=d, td=f['TD'], p1=f['P1']) + (TAPGATE if d <= 20 else ' - ' + A9.format(d=d) + ' keeps this cell provisional'), 'endlib')
            add(t, pn, col_maj, G.NPTF[d][2], NPSRC.format(nps=G.NPTF[d][0], d=d) + ' pipe OD', 'endlib')
            if d > 20 and f'Q-CONFLICT-TAPDRILL-{d}' not in ' '.join(g):
                g.append(A9.format(d=d))
        else:
            miss += [col_td, col_maj]
    if a in G.FPT and b in G.FPT:
        add(t, pn, '$PRP@Threads', f'{G.npt_thr(a)} x {G.npt_thr(b)} NPTF (female both ends)', 'thread texts from the part-number dashes (NPTF lib), format of the built 5000 rows', 'endlib')
    else:
        miss.append('$PRP@Threads')
        g = g + ['GENERATOR: no -40 NPTF end in the batch-16 end library (NPTF / ENDL / FPT stop at -32); own STEP 09_STEP_FILES/BRENNAN_5000-40-40.stp is present (measure + library work)']
    comment(t, pn, 'L / hex from the Brennan TFA catalog p10 alone' + ('; -40 pipe ends not in the end library' if miss else '; tap drills = Air-Way per size (A1 yes)'))
    row(t, pn, not g and not miss, miss, g, [], 'L / hex from the catalog; ' + ('the -40 ends need generator work' if miss else 'tap drills = Air-Way per-size values'),
        scenB=not miss)
    done.add(pn)

# ============================================================ 5404-40-40 (hex nipple -40)
pn, t = '5404-40-40', '5404'
i, od = omi_dims(pn); assert not od
for col, cc, what in (('L@DRIVE', 'L LGTH', 'overall length'), ('HEXB@HEX', 'C HEX', 'body hex'), ('D1@BORE', 'A1 DRILL', 'bore end A1'), ('D2@BORE', 'A2 DRILL', 'bore end A2')):
    cat_cell(t, pn, col, cc, what)
comment(t, pn, 'L / hex / bores from the Brennan TFA catalog p11 alone; the -40 NPTF ends are not in the end library')
row(t, pn, False, [f'NPTF{s}_{k}@DRIVE' for s in 'AB' for k in ('ENDL', 'E0', 'E1', 'L2')] + ['PIPEODA@DRIVE', 'PIPEODB@DRIVE', '$PRP@EndA_Thread', '$PRP@EndB_Thread'],
    ['GENERATOR: no -40 NPTF end in the batch-16 end library (NPTF / ENDL stop at -32); own STEP 09_STEP_FILES/BRENNAN_5404-40-40.stp is present (measure + library work)'], [],
    'body sizes prepared; the NPTF -40 end columns stay empty (no library source, ASME B1.20.1 -40 is not transcribed in the project)')
done.add(pn)

# ============================================================ 5404-N (round long nipples)
for r in ROWS_IN:
    pn, t = r['config'], r['table']
    if t != '5404N':
        continue
    i, od = omi_dims(pn); assert not od
    m = re.match(r'5404-N-(\d\d)X(\d+\.\d+)$', pn); d = int(m.group(1)); X = float(m.group(2))
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['A1 NPTF'], G.npt_thr(d)) and thr_eq(rr['values']['A2 NPTF'], G.npt_thr(d)), rr['values']
    v, s_, csrc = catv(pn, 'L LGTH')
    assert abs(v - X) < 1e-9, (pn, v, X)
    add(t, pn, 'L@DRIVE', X, f'length = the X of the OMi part number {pn} [user 2026-10-18 A4: Q-TRANSFER-5404N yes, length from the part number; keep the OMi part-number form]; '
        f'cross-check {csrc}: equal', 'other')
    AW = {4: '5404-N-04-04-X2', 6: '5404-N-06-06-X1', 8: '5404-N-08-08-X3'}[d]
    awr = base(t)[1][AW]
    conf = []
    for col in ('COD@REF', 'D1@BORE', 'D2@BORE'):
        add(t, pn, col, awr[col], (f'Air-Way 5404-N nipple of the same size: review row {AW} ({awr["$PRP@ScopeAction"]}, {awr["$PRP@DataStatus"]}) {col} = {awr[col]} '
                                    f'[user 2026-10-18 A4: Q-TRANSFER-5404N yes - bar diameter and bore from the Air-Way nipple of the same size, every length]'), 'other')
    garbled = rr['values']['A1 DRILL'] == rr['values']['L LGTH']
    if garbled:
        cnote = 'Brennan catalog row misprinted: A1 / A2 DRILL = 3.500 / 88.90 (the length in inch and mm; verify/png/TFA_p12_L3.png)'
    else:
        bv = float(rr['values']['A1 DRILL'])
        cnote = f'Brennan prints a different through drill {bv} (A1 / A2 DRILL) vs the Air-Way transfer {awr["D1@BORE"]}'
        if abs(bv - float(awr['D1@BORE'])) > 0.0051:
            conf.append(f'D1/D2 Air-Way transfer {awr["D1@BORE"]} (used, A4) vs Brennan TFA {tt["table_id"]} A1/A2 DRILL {bv} - information only')
            CONFLICTS.append(dict(table=t, config=pn, column='D1@BORE / D2@BORE', kept=f'Air-Way transfer {awr["D1@BORE"]} (A4 decision)', other=f'Brennan catalog {bv}'))
    for col in ('THDMAJ_A1@DRIVE', 'THDMAJ_A2@DRIVE'):
        add(t, pn, col, G.NPTF[d][2], NPSRC.format(nps=G.NPTF[d][0], d=d) + f' pipe OD (= {AW} {awr[col]})', 'endlib')
    add(t, pn, '$PRP@Threads', f'{G.npt_thr(d)} x {G.npt_thr(d)} NPTF, cut length {X:g} in', 'thread texts from the part-number dash, format of the built 5404N rows', 'endlib')
    comment(t, pn, f'L from the part number (= Brennan catalog), bar dia and bores from the Air-Way nipple {AW} (A4 yes 2026-10-18); {cnote}')
    g = G_(pn)
    row(t, pn, not g, [], g, conf, f'A4 transfer from {AW}; no Brennan size used (no DimSource BRENNAN); {cnote}')
    done.add(pn)

# ============================================================ 5405 (male pipe x female pipe adapter)
for r in ROWS_IN:
    pn, t = r['config'], r['table']
    if t != '5405':
        continue
    a, b = G.dashes(pn)
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['A1 NPTF'], G.npt_thr(a)) and thr_eq(rr['values']['A2 NPTF'], G.npt_thr(b)), rr['values']
    cat_cell(t, pn, 'L@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'CHEX@HEX', 'C HEX', 'body hex'); cat_cell(t, pn, 'D@BORE', 'A1 DRILL', 'male-end bore (to the pocket)')
    f = G.FPT[b]
    add(t, pn, 'TAPDRILL@BORE', f['TD'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + tapsrc(b), 'endlib')
    add(t, pn, 'THDMAJ_A1@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a) + ' pipe OD (male end)', 'endlib')
    add(t, pn, 'THDMAJ_A2@DRIVE', G.NPTF[b][2], NPSRC.format(nps=G.NPTF[b][0], d=b) + ' pipe OD (female end)', 'endlib')
    add(t, pn, '$PRP@Threads', f'{G.npt_thr(a)} x {G.npt_thr(b)} NPTF', 'thread texts from the part-number dashes, format of the built 5405 rows', 'endlib')
    comment(t, pn, 'L / hex / D from the Brennan TFA catalog p12 alone; tap drill = Air-Way per size (A1 yes)' + (' - -24 / -32 provisional (A9 open)' if b > 20 else ''))
    g = a9(G_(pn), b)
    row(t, pn, not g, [], g, [], 'every cell prepared' + ('; held only by A9 (the -%d tap drill)' % b if g else ''), scenB=bool(g))
    done.add(pn)

# ============================================================ 5406 (reducer bushing)
for pn in ('5406-32-04', '5406-40-32'):
    t = '5406'; a, b = G.dashes(pn)
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    cat_cell(t, pn, 'L2@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'C2HEX@HEX', 'C HEX', 'bushing hex')
    miss, g = [], G_(pn)
    f = G.FPT[b]
    add(t, pn, 'TAPDRILL@BORE', f['TD'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + tapsrc(b)
        + f"; the catalog A1 DRILL {rr['values']['A1 DRILL']} is the male-end drill, not a printed tap drill (impact/F2b.json: likely only) - not used", 'endlib')
    add(t, pn, 'THDMAJ_A2@DRIVE', G.NPTF[b][2], NPSRC.format(nps=G.NPTF[b][0], d=b) + ' pipe OD (female end)', 'endlib')
    if a in G.NPTF:
        add(t, pn, 'THDMAJ_A1@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a) + ' pipe OD (male end)', 'endlib')
        add(t, pn, '$PRP@Threads', f'{G.npt_thr(a)} (male) x {G.npt_thr(b)} (female) NPTF', 'thread texts from the part-number dashes, format of the built 5406 rows', 'endlib')
    else:
        miss += ['THDMAJ_A1@DRIVE', '$PRP@Threads']
        g = g + ['GENERATOR: no -40 NPTF male end in the batch-16 end library; own STEP 09_STEP_FILES/BRENNAN_5406-40-32.stp is present (measure + library work)']
    comment(t, pn, 'L2 / hex from the Brennan TFA catalog p13 alone; tap drill = Air-Way per size (A1 yes)' + ('; -40 male end not in the end library' if miss else ''))
    g = a9(g, b)
    row(t, pn, not g and not miss, miss, g, [], 'L2 / hex from the catalog; tap drill = Air-Way per-size value', scenB=bool(g) and not miss)
    done.add(pn)

# ============================================================ 5406-C (pipe caps)
for pn in ('5406-C-20', '5406-C-24', '5406-C-32'):
    t = '5406C'; d = int(pn.rsplit('-', 1)[1])
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['A1 NPTF'], G.npt_thr(d)), rr['values']
    L = cat_cell(t, pn, 'L@DRIVE', 'L LGTH', 'overall cap length'); cat_cell(t, pn, 'C1HEX@HEX', 'C HEX', 'cap hex')
    f = G.FPT[d]
    add(t, pn, 'TAPDRILL@BORE', f['TD'], FPTSRC.format(d=d, td=f['TD'], p1=f['P1']) + tapsrc(d), 'endlib')
    add(t, pn, 'THDMAJ_A@DRIVE', G.NPTF[d][2], NPSRC.format(nps=G.NPTF[d][0], d=d) + ' pipe OD', 'endlib')
    add(t, pn, '$PRP@Threads', f'{G.npt_thr(d)} NPTF female cap', 'thread text from the part-number dash, format of the built 5406C rows', 'endlib')
    wall = round(L - f['P1'], 3)
    comment(t, pn, f'L / hex from the Brennan TFA catalog p67 alone (Brennan caps are 0.11-0.36 shorter than the Air-Way caps built in this table); end wall L - P1 = {wall}')
    g = a9(G_(pn), d)
    row(t, pn, not g, [], g, [], f'end wall under the MS51503 P1-max port = {wall} in; Brennan caps are a shorter body than the Air-Way caps of the built sizes (0/6 lengths agree) - mixed sources in one master', scenB=bool(g))
    done.add(pn)

# ============================================================ 6400 (hand-made master; only the ORB groove width is empty)
for r in ROWS_IN:
    pn, t = r['config'], r['table']
    if t != '6400':
        continue
    a, b = G.dashes(pn)         # a = JIC, b = ORB
    hdr, rows = base(t); cur = rows[pn]
    i, od = omi_dims(pn)
    conf = []
    for col, cc in (('D1@DRIVE', 'L5 LGTH'), ('HEXB@HEX', 'C4 HEX'), ('D3@BORE_B', 'B1 DRILL'), ('D4@BORE_A', 'B2 DRILL')):
        cv, cs, _ = catv(pn, cc)
        if abs(float(cur[col]) - cv) > 0.0051:
            conf.append(f'{col} base {cur[col]} vs Brennan {cs}')
    own = os.path.exists(os.path.join(STEPS, f'BRENNAN_{pn}.stp'))
    gw = G.ORB_GW_MEASURED[b]
    if own:
        add(t, pn, 'ORB_GRVW@DRIVE', gw, (f'own Brennan STEP 09_STEP_FILES/BRENNAN_{pn}.stp: ORB -{b:02d} groove width {gw} measured 2026-09-2{"4" if b == 32 else "5"} '
                                         f'(gen_straight2 ORB_GW_MEASURED[{b}], source "{G.ORB_GW_SRC[b]}") {B}'), 'brennan-dim')
    else:
        add(t, pn, 'ORB_GRVW@DRIVE', gw, (f'end library gen_straight2 ORB_GW_MEASURED[{b}] = {gw}, measured on the {G.ORB_GW_SRC[b]} (another part, same ORB -{b:02d} end) - '
                                         f'per-size end detail [user 2026-10-18 A18 Q-TRANSFER-ORBGW: accept the 0.125 measured on Brennan 6400-14-14-O / -32-32-O]'), 'endlib')
    comment(t, pn, f'ORB -{b:02d} groove width {gw} ' + ('from this part\'s own Brennan STEP' if own else 'from the end library (Brennan 6400-%02d STEP of the same ORB size; Q-TRANSFER-ORBGW)' % b)
            + '; every other cell already filled (Air-Way = OMi = Brennan catalog)')
    row(t, pn, False, [], [x for x in G_(pn) if x != 'Q-HANDMADE'] + ['TOOLCHAIN: A6 (2026-10-18) = rebuild 6400 with the generator (fold 6400-L in) - SPEC 6400 does not exist in the batch-16 generator yet; the row is a complete generator row once it does'], conf,
        f'only ORB_GRVW was empty; Brennan catalog = base on D1 / hex / bores' + (f' except {conf}' if conf else ''), scenB=False)
    done.add(pn)

# ============================================================ 6405-02-02-O / -02-04-O (male ORB -02 x female pipe)
for pn in ('6405-02-02-O', '6405-02-04-O'):
    t = '6405'; a, b = G.dashes(pn)
    i, od = omi_dims(pn); assert not od
    tt, rr = cat(pn)
    assert thr_eq(rr['values']['B SAE ORB'], G.ORB_THR[a]) and thr_eq(rr['values']['A NPTF'], G.npt_thr(b)), rr['values']
    cat_cell(t, pn, 'L31@DRIVE', 'L LGTH', 'overall length'); cat_cell(t, pn, 'HEXB@HEX', 'C4 HEX', 'body hex'); cat_cell(t, pn, 'D3@BORE', 'B DRILL', 'bore from the ORB end')
    o = G.ORB[a]
    osrc = f"end library gen_straight2 ORB[{a}] (src: {o.get('src')}; MS51527G / MS51528D J2, Parker ORD-5700 Table 4-4) [Q-TRANSFER-ENDLIB yes]"
    add(t, pn, 'THDMAJ_A@DRIVE', o['TM'], osrc + ' thread major', 'endlib')
    # ORB_THDL / ORB_GRVDIA / ORB_GRVW deliberately NOT filled: gen_straight2 builds its ORB end library from every 6401 / 6405 / 6410 row
    # that carries ORB_GRVW (any DataStatus), so filling them here would make this row the ORB[2] source instead of the 6408-02-O-SOLID row
    # and drop that row's provenance note; the generator takes the -02 end from ORB[2] either way (identical values)
    f = G.FPT[b]
    add(t, pn, 'FPT_P1@DRIVE', f['P1'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + ' port depth (end detail) [Q-TRANSFER-ENDLIB yes]', 'endlib')
    add(t, pn, 'TAPDRILL@BORE_A', f['TD'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + TAPGATE, 'endlib')
    add(t, pn, '$PRP@EndA_Thread', f'{G.ORB_THR[a]} (ORB)', 'thread text from the part-number dash, format of the built 6405 rows', 'endlib')
    add(t, pn, '$PRP@EndB_Thread', f['thr'], FPTSRC.format(d=b, td=f['TD'], p1=f['P1']) + ' thread text', 'endlib')
    comment(t, pn, 'L31 / hex / D3 from the Brennan TFA catalog p15 alone; ORB -02 end from the 6408-02-O-SOLID row library; tap drill = Air-Way per size (A1 yes)')
    g = G_(pn)
    row(t, pn, not g, [], g, [], 'every cell prepared')
    done.add(pn)

# ============================================================ 6410
pn, t = '6410-04-02-O', '6410'
a, b = G.dashes(pn)
i, orow = omi_row(pn)
for col, j, cc in (('L33@DRIVE', 11, 'L LGTH'), ('C1HEX@HEX', 17, 'C4 HEX'), ('D@BORE', 18, 'B DRILL')):
    v, src = omiv(pn, j); cv, cs, csrc = catv(pn, cc)
    tag = 'equal' if abs(v - cv) < 1e-9 else 'rounding only' if abs(v - cv) <= 0.0051 else 'DIFFERS'
    assert tag != 'DIFFERS'
    add(t, pn, col, v, f'{src} (OMi first, user 2026-09-25; mapping impact/F2b.json M006-M008 certain); cross-check {csrc}: {tag}', 'other')
o = G.ORB[a]; osrc = f"end library gen_straight2 ORB[{a}] (src: {o.get('src')}) [Q-TRANSFER-ENDLIB yes]"
add(t, pn, 'THDMAJ_B1@DRIVE', o['TM'], osrc + ' male ORB thread major', 'endlib')
add(t, pn, 'THDMAJ_B2@DRIVE', G.ORB[b]['TM'], f"end library gen_straight2 ORB[{b}] thread major (female -02 port thread 5/16-24)", 'endlib')
add(t, pn, 'ORB_THDL@DRIVE', o['THDL'], osrc + ' thread length', 'endlib')
add(t, pn, 'ORB_GRVDIA@DRIVE', o['GD'], osrc + ' groove root dia', 'endlib')
add(t, pn, 'ORB_GRVW@DRIVE', o['GW'], osrc + ' groove width', 'endlib')
add(t, pn, '$PRP@Threads', f'{G.ORB_THR[a]} (male ORB) x {G.ORB_THR[b]} (female ORB)', 'thread texts from the part-number dashes, format of the built 6410 rows', 'endlib')
comment(t, pn, 'L33 / hex / D from OMi Items (= Brennan TFA p16); male ORB -04 end from the library; female -02 ORB port: no port drill D3 and no measured -02 port geometry yet (own STEP present)')
row(t, pn, False, ['D3@BORE'], ['MISSING D3@BORE (female -02 ORB port drill: no OMi / Air-Way / catalog value; A11 Q-TRANSFER-D3 yes, but the Air-Way per-size list starts at -04)',
                                 'GENERATOR: female -02 ORB port not in ORBF_MEAS (batch-16); own STEP 09_STEP_FILES/BRENNAN_6410-04-02-O.stp present (measure with tools/measure/ports.py + library work)'],
    [], 'OMi gives L / hex / D; male end from the library')
done.add(pn)

for pn in ('6410-32-20-O', '6410-32-24-O'):
    t = '6410'
    hdr, rows = base(t); cur = rows[pn]
    i, od = omi_dims(pn)
    conf = []
    for col, cc in (('L33@DRIVE', 'L LGTH'), ('C1HEX@HEX', 'C4 HEX'), ('D@BORE', 'B DRILL')):
        cv, cs, _ = catv(pn, cc)
        if abs(float(cur[col]) - cv) > 0.0051:
            conf.append(f'{col} base {cur[col]} (Air-Way; = OMi\'s 2026-10-18 real length) vs Brennan {cs} - base kept')
            CONFLICTS.append(dict(table=t, config=pn, column=col, kept=f'base {cur[col]} (Air-Way = OMi answer 2026-10-18)', other=f'Brennan catalog {cs}'))
    # ORB_GRVW@DRIVE (the only empty cell) deliberately NOT filled: gen_straight2 builds ORB[32] from any 6401/6405/6410 row carrying
    # ORB_GRVW; a value here replaces the library source (6408 row + Brennan 6400-32-32-O STEP) and changed the $COMMENT of 3 built
    # configurations in the first test run (6401-32-32-O, 6405-32-20-O, 6405-32-32-O). The generator uses 0.125 for this end anyway (A18).
    fd = {20: 1.53, 24: None}[G.dashes(pn)[1]]
    edits = []
    if fd is not None and abs(float(cur['D3@BORE']) - fd) > 1e-9:
        edits.append(('D3@BORE', cur['D3@BORE'], fd, 'A11 Q-TRANSFER-D3: Air-Way per-size -20 port drill 1.53 instead of the impossible 1.72 (questions_20261008/merged.json orb-port-drill-per-size)'))
    d3 = fd if fd is not None else float(cur['D3@BORE'])
    if float(cur['D@BORE']) > d3 + 1e-9:
        edits.append(('D@BORE', cur['D@BORE'], d3, f'A11 Q-BOREWIDE: cap the through bore at the port drill {d3} (report to OMi)'))
    for c_, old, new, why in edits:
        EDITS.append(dict(table=t, config=pn, column=c_, old=old, new=new, why=why))
    g = [x for x in G_(pn)] + ([f'MAIN-SESSION EDIT (non-empty Air-Way cells, outside this cell list): ' + '; '.join(f'{c_} {old} -> {new} ({why})' for c_, old, new, why in edits)] if edits else [])
    row(t, pn, not g, [], g, conf, 'no cell: ORB_GRVW stays empty on purpose (the generator takes the -32 groove 0.125 from its library, A18; filling it changes 3 built $COMMENTs). '
        'A11 decided (cap / per-size port drill); the edits change non-empty base cells, so they are listed in test/edits_A11.csv for the main session, not in cells.csv', scenB=bool(edits))
    done.add(pn)

# ============================================================ 6420 / 6425 / 6900: no generator SPEC -> values listed in notes only (no new columns)
for r in ROWS_IN:
    pn, t = r['config'], r['table']
    if t not in ('6420', '6425', '6900'):
        continue
    tt, rr = cat(pn)
    i, od = omi_dims(pn)
    vals = '; '.join(f'{k} {v}' for k, v in rr['values'].items())
    om = '; '.join(f'{OHDR.get(j, j)} {v}' for j, v in od.items()) or 'none'
    conf = []
    if t in ('6420', '6425'):
        for j, cc in ((11, 'L LGTH'), (17, 'C4 HEX')):
            if j in od and abs(float(od[j]) - float(rr['values'][cc])) > 0.0051:
                conf.append(f'OMi {OHDR[j]} {od[j]} vs Brennan {cc} {rr["values"][cc]}')
    if pn == '6420-08-08':
        conf.append('OMi website 1.320 (copy-down; OMi 2026-10-18 real length 1.5) vs Brennan catalog 1.500 vs own STEP 1.620 (hex STEP 1.125 vs 1.000) - Q-NEW-F3-6420-0808-OAL')
    if conf:
        CONFLICTS.append(dict(table=t, config=pn, column='overall / hex', kept='nothing (no column, no generator)', other=' | '.join(conf)))
    note = (f'no batch-16 SPEC {t} (Q-NEWMASTER-{t}) and today\'s table has no dimension column' + (' (7-column skeleton)' if t != '6900' else '') +
            f' -> no cells written. Brennan TFA p{tt["page"]} {tt["table_id"]}: {vals}. OMi Items row {i}: {om}.')
    if t == '6900':
        note += (' 6900 columns exist (W4 / L2 / C2HEX / CHEX / D1 / D) but the length and NPSM-bore pairings are only "likely" and the Air-Way rows agree with Brennan on 3/24 (W4), 8/24 (L2), 1/24 (D): '
                 'the mapping is not confirmed on data, so nothing is proposed (the identity is settled by A3 2026-10-18 - male ORB x female NPSM swivel - but the length / NPSM-bore columns still need the 6900 SPEC (Q-NEWMASTER-6900) and its own STEP).')
    g = G_(pn) + [f'TOOLCHAIN: no SPEC {t} in the batch-16 generator (Q-NEWMASTER-{t})']
    row(t, pn, False, ['all dimension columns (none exist / mapping unconfirmed)'], g, conf, note)
    done.add(pn)

# feedback of the generator test (test.py writes test/blocked.json): a complete row the batch-16 generator BLOCKS is not ready
BLK = os.path.join(OUT, 'test', 'blocked.json')
if os.path.exists(BLK):
    for k, why in json.load(open(BLK, encoding='utf-8')).items():
        for r in ROWS:
            if r['config'] == k and r['ready'] == 'yes':
                r['ready'] = 'no'; r['gates'] = (r['gates'] + ' ; ' if r['gates'] else '') + 'BLOCKED by the batch-16 generator: ' + why
                SCEN_B.append((r['table'], r['config']))

missing_rows = [r['config'] for r in ROWS_IN if r['config'] not in done]
assert not missing_rows, missing_rows
assert len(ROWS) == len(ROWS_IN) == len({(r['table'], r['config']) for r in ROWS})

with open(os.path.join(OUT, 'cells.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'column', 'value', 'source', 'kind']); w.writeheader(); w.writerows(CELLS)
with open(os.path.join(OUT, 'rows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes']); w.writeheader(); w.writerows(ROWS)
# informative scenario B: rows with complete data held only by decisions -> ready=yes in a separate file (NOT a proposal)
with open(os.path.join(OUT, r'test\rows_scenarioB.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes']); w.writeheader()
    for r in ROWS:
        w.writerow(dict(r, ready='yes' if r['ready'] == 'yes' or (r['table'], r['config']) in SCEN_B else 'no'))
json.dump(CONFLICTS, open(os.path.join(OUT, r'test\conflicts.json'), 'w'), indent=1)
with open(os.path.join(OUT, r'test\edits_A11.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'column', 'old', 'new', 'why']); w.writeheader(); w.writerows(EDITS)
json.dump(DECIDED_SEEN, open(os.path.join(OUT, r'test\decided_gates.json'), 'w'), indent=1)
from collections import Counter
print(len(CELLS), 'cells', dict(Counter(c['kind'] for c in CELLS)))
print('rows', len(ROWS), 'ready', sum(r['ready'] == 'yes' for r in ROWS), 'scenario-B extra', len(SCEN_B))
print('by table', dict(Counter(c['table'] for c in CELLS)))
for c in CONFLICTS:
    print('CONFLICT', c)
