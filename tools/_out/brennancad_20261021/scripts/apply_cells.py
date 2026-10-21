"""apply_cells.py (2026-10-21): stage the verified Brennan CAD cells (user: "stage").
Base = the Air-Way-first stage (tools/_out/airway_first_20261020/stage/04_DESIGN_TABLES: the newest review tables, batch 18 candidate) and,
for FS roots, the ORFS stage tables (tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES). Both are copied; the originals and the
live 04_DESIGN_TABLES are not touched.
Per cell of ../../partcommunity_20261021/decode/verify.csv (verdict OK; all 427 are): the target cell must be EMPTY in the base table
(else: not written, logged as 'not empty'). Per touched row:
  $PRP@DimSource = BRENNAN (column added at the end when the table has none);
  $PRP@AxialSource prefixed '[BRENNAN-CAD 2026-10-21: <columns>] ';
  $COMMENT appended 'Brennan CAD record <pn> (PARTcommunity / CADENAS, codes <col>=<code>, ...; user 2026-10-21 "yes you can use them
  following my rule")';
  $PRP@DataStatus MISSING -> ASSUMED (single source) only when no required dimension column is still empty (required = filled on >= 90 %
  of the table's shipped rows; thread / port / seat columns come from the end library by thread size and are not counted); else the row
  stays MISSING (its cells are staged as data, the generator keeps skipping it).
Writes stage/04_DESIGN_TABLES, stage/orfs_tables, CHANGES.csv, rows.csv."""
import os, re, csv, glob, shutil, collections
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
STD = re.compile(r'^(THDMAJ|TAPDRILL|ORB_|JIC_|SEAT|RELIEF|NPT|NPSM|NOSE|FSM_|FSW|NWO_)', re.I)
BASE = J('tools', '_out', 'airway_first_20261020', 'stage', '04_DESIGN_TABLES')
BASE_FS = J('tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')
ST = os.path.join(A, 'stage', '04_DESIGN_TABLES'); ST_FS = os.path.join(A, 'stage', 'orfs_tables')
for src, dst in ((BASE, ST), (BASE_FS, ST_FS)):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

# the 4 cells verify.csv flagged, each explained (2026-10-21): 1/4 NPT major 0.540 (= Air-Way); forged Y flats = Brennan's printed catalog
# (the plain Air-Way part differs); FS6402-12-12 L 2.25 vs Brennan's catalog misprint 0.609 (BLOCKED_NEEDS: 'L misprinted')
EXPLAINED = {('6807-08-06-NWO-FG', 'THDMAJ_B2@DRIVE'),   # group A: 9/16 ORB thread major = Air-Way; the catalog test hit another column
             ('6805-04-04-NWO-FG', 'THDMAJ_A@DRIVE'), ('6807-08-08-NWO-FG', 'Y@HEX'), ('6809-10-10-NWO-FG', 'Y@HEX'), ('FS6402-12-12', 'L@DRIVE')}
cells = [r for f in ('verify.csv', 'verify_A.csv')     # verify_A.csv = group A (map_groupA.py, 2026-10-21)
         if os.path.exists(J('tools', '_out', 'partcommunity_20261021', 'decode', f))
         for r in csv.DictReader(open(J('tools', '_out', 'partcommunity_20261021', 'decode', f), encoding='utf-8'))
         if r['verdict'] == 'OK' or (r['part'], r['column']) in EXPLAINED]
cache_pn = {r['part']: (r['tried_as'] or r['part']) for r in csv.DictReader(open(J('tools', '_out', 'partcommunity_20261021', 'pc_final.csv'), encoding='utf-8'))}
shipped = set()
for p in glob.glob(J('04_DESIGN_TABLES', '*_SW2.xlsx')):
    ws = openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    for r in rows[1:]:
        if r and r[0]:
            d = dict(zip(h, r)); shipped.add(norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or r[0]))

# gen_straight2 ORB_GW_MEASURED: the ORB -32 / -14 groove width (0.125) is the generator's measured library value when the cell is empty;
# writing it into a row makes that row the first -32 entry of the shared ORB library and drops the 'MEASURED on the Brennan STEP' note
# from other tables' -32 rows (6405, 2026-10-21). So: not written, and counted as present.
def lib_supplied(col, part):
    d = re.findall(r'-(\d\d)(?=-|$)', part)
    return col == 'ORB_GRVW@DRIVE' and bool(d) and int(d[0]) in (14, 32)


by_root = collections.defaultdict(list)
for c in cells:
    by_root[c['root']].append(c)
changes, rowlog = [], []
for root, cs in sorted(by_root.items()):
    path = os.path.join(ST_FS if root.startswith('FS') else ST, f'DesignTable_{root}.xlsx')
    wb = openpyxl.load_workbook(path); ws = wb.worksheets[0]
    hr = next(i for i in range(1, 7) if any(c.value == '$PRP@PartNo' for c in ws[i]))
    head = {c.value: c.column for c in ws[hr] if c.value}
    if '$PRP@DimSource' not in head:
        col = ws.max_column + 1; ws.cell(row=hr, column=col, value='$PRP@DimSource'); head['$PRP@DimSource'] = col
    numcols = [k for k in head if k and not str(k).startswith('$')]
    rows = {}
    for i in range(hr + 1, ws.max_row + 1):
        pn = ws.cell(row=i, column=head['$PRP@PartNo']).value
        if not pn:
            continue
        sku = ws.cell(row=i, column=head['$PRP@OMiSKU']).value if '$PRP@OMiSKU' in head else None
        rows.setdefault(norm(sku or pn), i)
    ship_rows = [i for k, i in rows.items() if k in shipped]
    req = [c for c in numcols if ship_rows and sum(isnum(ws.cell(row=i, column=head[c]).value) for i in ship_rows) >= 0.9 * len(ship_rows)]
    touched = collections.defaultdict(list)
    dsh = lambda p: set(re.findall(r'-(\d\d)(?=-|$)', p))
    for c in cs:
        i = rows.get(c['part'])
        if i is None or c['column'] not in head:
            changes.append(dict(root=root, part=c['part'], column=c['column'], value=c['value'], code=c['code'], result='row / column not found')); continue
        # a column the built rows of the same size leave EMPTY is supplied by the generator's measured library (e.g. the ORB -32 / -14
        # groove width): do not fill it (2026-10-21, 6405 note)
        if lib_supplied(c['column'], c['part']):
            changes.append(dict(root=root, part=c['part'], column=c['column'], value=c['value'], code=c['code'],
                                result='skipped (library-driven: the generator measured value for this ORB size)')); continue
        same_size = [j for k, j in rows.items() if k in shipped and dsh(k) & dsh(c['part'])]
        if same_size and any(not isnum(ws.cell(row=j, column=head[c['column']]).value) for j in same_size):
            changes.append(dict(root=root, part=c['part'], column=c['column'], value=c['value'], code=c['code'],
                                result='skipped (library-driven: empty on built rows of this size)')); continue
        cell = ws.cell(row=i, column=head[c['column']])
        if cell.value not in (None, ''):
            changes.append(dict(root=root, part=c['part'], column=c['column'], value=c['value'], code=c['code'], result=f'not empty ({cell.value})')); continue
        cell.value = float(c['value'])
        touched[i].append(c)
        changes.append(dict(root=root, part=c['part'], column=c['column'], value=c['value'], code=c['code'], result='written'))
    for i, cs_ in touched.items():
        part = cs_[0]['part']
        ws.cell(row=i, column=head['$PRP@DimSource'], value='BRENNAN')
        ax = ws.cell(row=i, column=head['$PRP@AxialSource'])
        ax.value = f"[BRENNAN-CAD 2026-10-21: {', '.join(c['column'] for c in cs_)}] " + (ax.value or '')
        if '$COMMENT' in head:
            cm = ws.cell(row=i, column=head['$COMMENT'])
            note = (f"Brennan CAD record {cache_pn.get(part, part)} (PARTcommunity / CADENAS, "
                    + ', '.join(f"{c['column']}={c['code']}" for c in cs_) + '; user 2026-10-21 "yes you can use them following my rule")')
            cm.value = (cm.value + ' | ' if cm.value else '') + note
        st = ws.cell(row=i, column=head['$PRP@DataStatus'])
        # every required column, the thread / port / seat ones included: the generator reads them from the row (2026-10-21: 5000 / 5406
        # rows without a tap drill crashed end_NPTFF)
        still = [c for c in req if not isnum(ws.cell(row=i, column=head[c]).value) and not lib_supplied(c, part)]
        old = st.value
        if str(old or '').upper() == 'MISSING' and not still:
            st.value = 'ASSUMED'
        rowlog.append(dict(root=root, part=part, cells=len(cs_), status_before=old, status_after=st.value, still_missing=', '.join(still)))
    wb.save(path)

for name, data in (('CHANGES.csv', changes), ('rows.csv', rowlog)):
    with open(os.path.join(A, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
print(collections.Counter(c['result'].split(' (')[0] for c in changes))
print('rows touched', len(rowlog), '| MISSING -> ASSUMED', sum(1 for r in rowlog if r['status_before'] == 'MISSING' and r['status_after'] == 'ASSUMED'),
      '| still MISSING', sum(1 for r in rowlog if r['status_after'] == 'MISSING'))
