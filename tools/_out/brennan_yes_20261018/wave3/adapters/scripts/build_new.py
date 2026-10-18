"""build_new.py (wave 3 adapters, 2026-10-18): the 34 dropped-77 tube fittings with no Air-Way row that Brennan's TFA catalog prints
(brennan_rows.csv group B-dropped77), plus the 2 -LN parts of the "no source" six that A10 (Q-TRANSFER-LN yes) now covers, and the two
5406-P plugs whose Air-Way alias rows exist (A4 Q-NEW-AWALIAS yes).

Outputs (wave3/adapters/):
  newrows.csv      table,config,column,value,source,kind   - one line per column of every proposed NEW row (rows go at the end of the table)
  edits_5406P_alias.csv table,config,column,old,new,why     - the alias rows 5406-08P / 5406-12P: DROP -> BUILD (old asserted vs the stage)
  cells.csv        table,config,column,value,source,kind   - empty cells of EXISTING rows (none for this group: header only)
  rows.csv         table,config,ready,missing_columns,gates,conflicts,notes (new rows + alias rows + the 3 parts with no table)
  mapping_evidence.txt  catalog letter -> table column per table, with the same-table agreement counts (stage rows with a value)
Read-only on the project. Run: python -I -B build_new.py
"""
import os, sys, csv, json, re, collections
R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
BY = os.path.join(R, r'tools\_out\brennan_yes_20261018')
OUT = os.path.join(BY, r'wave3\adapters')
STAGE_ROOT = os.path.join(BY, 'stage')
STAGE = os.path.join(STAGE_ROOT, '04_DESIGN_TABLES')
TOOLS = os.path.join(R, r'tools\_out\puckfix_20261009\tools_new')
os.environ['OMI_ROOT'] = STAGE_ROOT
os.environ['GS_OUT'] = os.environ['GT_OUT'] = os.path.join(OUT, 'scratch', 'libs')
sys.path[:0] = [os.path.join(TOOLS, 'generators'), TOOLS]
import openpyxl
from openpyxl.utils import get_column_letter
import gen_straight2 as G

TODAY = '2026-10-18'
BY_TAG = '[Brennan = yes 2026-10-18]'
CATF = os.path.join(R, r'tools\_out\brennan_catalog_20261001\catalog_verified.json')
D = json.load(open(CATF, encoding='utf-8'))
CAT = {}
for t in D['tables']:
    for rr in t['rows']:
        CAT.setdefault(rr['pn'], []).append((t, rr))
TAB = {t['table_id']: t for t in D['tables']}

wb = openpyxl.load_workbook(os.path.join(R, r'07_RAW_EXTRACTS\omi_dimensions\WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)
_it = wb['Items'].iter_rows(values_only=True); OH = next(_it)
OMI = {}
for i, r in enumerate(_it, start=2):
    if r[0]:
        OMI.setdefault(str(r[0]).strip(), (i, dict(zip(OH, r))))
OCOL = {h: get_column_letter(j + 1) for j, h in enumerate(OH) if h}

_tabs = {}


def table(t):
    if t not in _tabs:
        ws = openpyxl.load_workbook(os.path.join(STAGE, f'DesignTable_{t}.xlsx'), read_only=True).worksheets[0]
        v = list(ws.iter_rows(min_row=2, values_only=True))
        hdr = list(v[0])
        rows = collections.OrderedDict()
        for r in v[1:]:
            if r[0]:
                rows[str(r[0]).strip()] = dict(zip(hdr, r))
        _tabs[t] = (hdr, rows)
    return _tabs[t]


def num(s):
    s = str(s).strip()
    return float(s) if re.fullmatch(r'\d*\.\d+|\d+', s) else None


def fmt(v):
    if isinstance(v, str):
        return v
    return ('%.4f' % v).rstrip('0').rstrip('.')


def empty(v):
    return v is None or (isinstance(v, str) and not v.strip())


def catrow(pn):
    hits = CAT.get(pn, [])
    assert len(hits) == 1, (pn, len(hits))
    return hits[0]


def catsrc(pn, ccol, mean, mapping):
    t, rr = catrow(pn)
    raw = rr['values'][ccol]
    return (f'Brennan TFA catalog p.{t["page"]} table {t["table_id"]} "{t["series"]} {t["title"]}" row {pn} col "{ccol}" = "{raw}" '
            f'(07_RAW_EXTRACTS/brennan_catalogs/TFA Catalog.pdf; tools/_out/brennan_catalog_20261001/catalog_verified.json, line_y {rr.get("line_y")}, '
            f'page verified {t.get("verified")}) {BY_TAG} - {mean}; mapping: {mapping}')


def omiv(pn, col):
    i, row = OMI[pn]
    v = row.get(col)
    if v in (None, ''):
        return None, None
    return float(str(v).strip()), f'OMi WebsitePartsInfo2026.xlsx Items!{OCOL[col]}{i} "{col}" = {str(v).strip()}'


def dashes(pn):
    return [int(x) for x in re.findall(r'-(\d\d)(?=-|$| )', pn)]


NPT = {d: G.npt_thr(d) for d in (2, 4, 6, 8, 12, 16, 20, 24, 32)}
JICSRC = 'end library gen_straight2 JIC[{d}] (= tools_new/generators/templates/DesignTable_2403_SW2.xlsx, MS33656J chain, VERIFIED vs Brennan) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
ORBSRC = 'end library gen_straight2 ORB[{d}] (from the 6401 / 6405 / 6410 review tables; SAE J1926) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
NPSRC = 'end library: ASME B1.20.1 {nps} NPT pipe OD = tools_new/generators/ms51500.NPTF[{d}] (as on every built pipe end) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
NPSMSRC = 'end library: pipe OD of the -{d:02d} NPSM swivel thread = ms51500.NPTF[{d}] {v} (the value every built 1501 / 1405 / 1502 / 1504 row carries for its NPSM end) [Q-TRANSFER-ENDLIB yes 2026-10-08]'
FPTSRC = ('end library gen_straight2 FPT[{d}] (= tools_new/generators/templates/DesignTable_2405_SW2.xlsx TAPDRILL@BORE_A) = Air-Way per-size tap drill '
          '(-02 0.33 ... -20 1.48) [user 2026-10-18 A1 Q-TRANSFER-TAPDRILL yes, 00_DOCS/ANSWERS_2026-10-18.md]')
ENDLSRC = 'end library gen_straight2 ENDL[{d}] = {v} (the 5404 Brennan-measured male NPTF end length of the pipe dash; the value every 2404 row of that pipe dash carries)'

NEW, ROWS, EDITS, MAPEV = [], [], [], []
# rows with complete data that the batch-16 generator BLOCKS (wave3 test, test/compare.txt + gen_applied/logs) -> ready = no, gate named
GEN_BLOCK = {
    '2505-04-04-FG': ('GENERATOR BLOCKS: "leg 1: port depth P1 0.67 >= leg length 0.62" (gen_tee 2505, wave3 test) = Q-ANGLED-P1 (A15: settle from Brennan if it answers; '
                      'the TFA catalog prints no port depth and 09_STEP_FILES/BRENNAN_2505-04-04-FG.stp is not there -> needs STEP download); same block as 2505-08-08-FG / -16-16-FG in the stage'),
    '5404-N-06X5.500': ('BLOCKED by the batch-16 generator: KeyError("part number has no dash pair") - SPEC 5404N reads "5404-N-d-d X L" part numbers only; the OMi form kept by A4 '
                        'needs generator work (same as the 18 wave2 5404-N rows)'),
}
NOT_PROPOSED = set()


class Row:
    def __init__(self, t, pn, kind_default='brennan-dim'):
        self.t, self.pn = t, pn
        self.hdr, self.rows = table(t)
        assert pn not in self.rows, (t, pn, 'row already exists')
        self.v = collections.OrderedDict()
        self.missing, self.gates, self.conf, self.notes = [], [], [], []
        self.extra_cols = []

    def put(self, col, val, src, kind):
        if col not in self.hdr and col not in self.extra_cols:
            self.extra_cols.append(col)
        self.v[col] = (val, src, kind)

    def cat(self, col, ccol, mean, mapping, omi=None):
        """catalog value; if OMi gives the same feature, OMi first (user 2026-09-25) - Brennan = cross-check"""
        t, rr = catrow(self.pn)
        raw = rr['values'].get(ccol, '')
        b = num(raw)
        src = catsrc(self.pn, ccol, mean, mapping) if raw else None
        if omi:
            o, osrc = omiv(self.pn, omi)
            if o is not None:
                if b is not None and abs(o - b) <= 0.0051:
                    tag = 'equal' if abs(o - b) < 1e-9 else 'rounding only'
                    self.put(col, o, f'{osrc} (OMi first, user 2026-09-25); Brennan cross-check: {src.split(" - ")[0]}: {tag} (OMi and Brennan count as ONE source, evidence 2026-09-26)', 'other')
                else:
                    self.put(col, o, f'{osrc} (OMi first, user 2026-09-25); Brennan prints {ccol} "{raw}" - DIFFERS, listed as a conflict', 'other')
                    self.conf.append(f'{col}: OMi {o} vs Brennan {ccol} {raw} (OMi kept)')
                return
        if b is None:
            self.missing.append(col)
            if raw:
                self.conf.append(f'{col}: Brennan {ccol} prints "{raw}" (a range / not one value) - never averaged, left empty')
            else:
                self.notes.append(f'{col}: Brennan {ccol} not printed')
            self.put(col, None, f'no source: Brennan {ccol} = "{raw}"', 'none')
            return
        self.put(col, b, src, 'brennan-dim')

    def lib(self, col, val, src):
        self.put(col, val, src, 'endlib')

    def other(self, col, val, src):
        self.put(col, val, src, 'other')

    def done(self, ready_gates=(), status=None, axial=None, comment=None, dimsource=None):
        if self.pn in GEN_BLOCK:
            self.gates.append(GEN_BLOCK[self.pn])
        drv = [c for c in self.hdr + self.extra_cols if c and ('@' in c) and not c.startswith('$')]
        for c in drv:
            if c not in self.v:
                self.missing.append(c)
                self.v[c] = (None, 'no source (not proposed)', 'none')
        miss = [c for c in dict.fromkeys(self.missing)]
        ready = not miss and not self.gates
        st = status or ('ASSUMED' if ready else 'MISSING')
        brennan = any(k == 'brennan-dim' for _, _, k in self.v.values())
        ds = dimsource if dimsource is not None else ('BRENNAN' if brennan else ('OMI' if any(k == 'other' and 'OMi WebsitePartsInfo' in s for _, s, k in self.v.values()) else None))
        self.put('$PRP@PartNo', self.pn, 'the part number (= the OMi SKU; config name = OMi part number)', 'other')
        self.put('$PRP@DataStatus', st, ('every driving cell has a source; ' + ('Brennan alone = one source' if brennan else 'one source') + ' -> ASSUMED') if st == 'ASSUMED'
                 else f'held (ready = no): {"; ".join(self.gates + ["missing " + ", ".join(miss)] if miss else self.gates)[:300]} -> MISSING until settled', 'other')
        self.put('$PRP@AxialSource', axial, 'row source summary (per-cell sources in this file)', 'other')
        self.put('$COMMENT', comment, 'note', 'other')
        self.put('$PRP@ScopeAction', 'BUILD', '2026-10-16: OMi sells this part (website, two-pass crawl 2026-10-16, tools/_out/omi_enum_20261015); the 2026-09-23 crawl had dropped the SKU', 'other')
        self.put('$PRP@OMiSKU', self.omisku if hasattr(self, 'omisku') else self.pn, 'the OMi part number (website list 07_RAW_EXTRACTS/omi_feed)', 'other')
        self.put('$PRP@DimSource', ds, 'marking rule 2026-10-18 ("yes use brennan but still differentiate the two in tables"): BRENNAN = at least one size from Brennan alone; OMI = sizes from OMi\'s parts file; empty = Air-Way / transfer' + ('' if '$PRP@DimSource' in self.hdr else ' [column not in today\'s stage table: add it at the end of header row 2]'), 'other')
        for c in self.hdr:
            if c is None:
                continue
            if c not in self.v:
                self.v[c] = (None, 'not filled: no source for this property (siblings of this table leave it empty or carry an Air-Way value)', 'none')
        for c in self.hdr + self.extra_cols:
            if c is None or c not in self.v:
                continue
            val, src, kind = self.v[c]
            if c in self.extra_cols and '[column not in' not in src:
                src += ' [column not in today\'s stage table: add it]'
            NEW.append(dict(table=self.t, config=self.pn, column=c, value='' if val is None else fmt(val), source=src, kind=kind))
        ROWS.append(dict(table=self.t, config=self.pn, ready='yes' if ready else 'no', missing_columns=' ; '.join(miss), gates=' ; '.join(self.gates),
                         conflicts=' ; '.join(self.conf), notes=' ; '.join(self.notes)))
        return ready


# ------------------------------------------------------------------------ mapping evidence
def norm(pn):
    return re.sub(r'\s+', '-', pn.strip())


def pairing(t, maps, tid_prefix=None, label=''):
    """compare table columns with catalog columns on every stage row that the catalog prints (same pn, blank -> '-')"""
    hdr, rows = table(t)
    out = [f'===== {t} {label}']
    for col, ccol, mean in maps:
        eq = rnd = n = 0; diff = []
        for pn, r in rows.items():
            hits = CAT.get(norm(pn)) or []
            if len(hits) != 1 or empty(r.get(col)):
                continue
            ct, crow = hits[0]
            if tid_prefix and not ct['table_id'].startswith(tid_prefix):
                continue
            b = num(crow['values'].get(ccol, ''))
            if b is None:
                continue
            n += 1
            a = float(r[col])
            if abs(a - b) < 1e-9: eq += 1
            elif abs(a - b) <= 0.0051: rnd += 1
            else: diff.append(f'{pn} {a} vs {b}')
        out.append(f'  {col:16} <- {ccol:10} {mean[:60]:60} | stage rows printed by the catalog: {eq + rnd}/{n} agree to rounding' + (f' (differ: {"; ".join(diff[:4])}{" ..." if len(diff) > 4 else ""})' if diff else ''))
    MAPEV.extend(out)


def twin_pairing(t, maps, pairs, label='plain / sibling twins (different parts - information)'):
    hdr, rows = table(t)
    out = [f'  -- {label}']
    for col, ccol, mean in maps:
        eq = n = 0; diff = []
        for tpn, cpn in pairs:
            if tpn not in rows or empty(rows[tpn].get(col)) or cpn not in CAT:
                continue
            b = num(CAT[cpn][0][1]['values'].get(ccol, ''))
            if b is None:
                continue
            n += 1
            a = float(rows[tpn][col])
            if abs(a - b) <= 0.0051: eq += 1
            else: diff.append(f'{tpn} {a} vs {cpn} {b}')
        out.append(f'  {col:16} <- {ccol:10} {eq}/{n}' + (f' (differ: {"; ".join(diff[:4])})' if diff else ''))
    MAPEV.extend(out)


COMMENT0 = (f'{TODAY} (wave 3 adapters, staged, not shipped): NEW row - OMi sells this part (SKU dropped by the 2026-09-23 crawl; two-pass crawl 2026-10-16, '
            'tools/_out/adapters77_20261016/REPORT_77.md); Air-Way does not print this size')
AX_B = '[BRENNAN-ONLY 2026-10-18] OMi catalog SKU dropped by the 2026-09-23 crawl (adapters77, 2026-10-16); NO Air-Way row for this size; 2026-10-18 Brennan allowed (user: "yes use brennan but still differentiate"): '
AX_O = 'OMi catalog SKU dropped by the 2026-09-23 crawl (adapters77, 2026-10-16); NO Air-Way row for this size; '
TOOLGATE = 'GATE TOOLCHAIN: no {t} SPEC in the batch-16 generators (puckfix tools_new gen_straight2 / gen_tee) - master not built yet'


def jicchain(row, d, prefix='JIC'):
    e = G.JIC[d]
    for col, k in ((f'{prefix}_RELIEFL@DRIVE', 'RL'), (f'{prefix}_THDZ@DRIVE', 'TZ'), (f'{prefix}_CONEDIA@DRIVE', 'CD'), (f'{prefix}_LANDL@DRIVE', 'LL'), (f'{prefix}_SEATL@DRIVE', 'SL')):
        row.lib(col, e[k], JICSRC.format(d=d) + f' {k} (end detail per dash)')
    row.lib('RELIEFANG@DRIVE', 60, 'gen_straight2 end_JICM constant 60 deg relief ramp (the value on every row of this table) [Q-TRANSFER-ENDLIB yes]')
    row.lib('SEATB@DRIVE', 37, 'gen_straight2 end_JICM constant 37 deg flare seat (the value on every row of this table) [Q-TRANSFER-ENDLIB yes]')


def thr_eq(cat_s, lib_s):
    a = re.sub(r'\s*(UN-2B|UNF-2B|NPTF|UNF|UN)\s*$', '', str(cat_s).strip())
    a = re.sub(r'^(\d+)[- ](\d+/\d+)', r'\1 \2', a).replace('-11-1/2', '-11 1/2')
    return a == str(lib_s).strip()


# ============================================================ 1504 (FP x FPS 45 deg elbow, forged) - no SPEC
M1504 = [('N2@DRIVE', 'L LGTH', 'axis crossing to the female NPTF port face'), ('M@DRIVE', 'M1 LGTH', 'axis crossing to the NPSM swivel stem tip (45 deg leg)'),
         ('W2@HEX', 'M LGTH', 'axis crossing to the swivel-nut face (45 deg leg)'), ('CHEX@HEX', 'C HEX', 'swivel nut hex'), ('C1HEX@HEX', 'Y FLATS', 'forged body flats'),
         ('D@BORE', 'A2 DRILL', 'NPSM swivel stem bore')]
pairing('1504', M1504, 'TFA-p022', '(TFA p.22 "1504-FG FP-FPS 45 DEG ELBOW"; mapping = wave2 tee_elbow mapping_evidence.txt; OMi drawing row 1504-20-20-FG is the strongest pair)')
MAP1504 = 'TFA p.22 1504-FG drawing: L = crossing to the female port face, M1 = to the NPSM stem tip, M = to the nut face, C = nut hex, Y = forged flats, A2 DRILL = stem bore (wave2 tee_elbow mapping_evidence.txt; check on the OMi-drawn 1504-20-20-FG row in mapping_evidence.txt here)'
for pn in ('1504-08-08-FG', '1504-12-12-FG', '1504-16-16-FG'):
    a, b = dashes(pn)
    r = Row('1504', pn)
    t_, rr = catrow(pn)
    assert thr_eq(rr['values']['A1 NPTF'], NPT[a]) and thr_eq(rr['values']['A2 NPSM'], NPT[b]), rr['values']
    for col, cc, mean in M1504:
        r.cat(col, cc, mean, MAP1504)
    r.lib('TAPDRILL@BORE', G.FPT[a]['TD'], FPTSRC.format(d=a))
    r.lib('THDMAJ_A@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a))
    r.lib('THDMAJ_A1@DRIVE', G.NPTF[b][2], NPSMSRC.format(d=b, v=G.NPTF[b][2]))
    r.other('$PRP@Threads', f'{NPT[a]} (A NPTF) x {NPT[b]} (A1 NPSM)', 'thread callouts from the part-number dashes, format of the table\'s rows; = Brennan A1 NPTF / A2 NPSM columns')
    r.conf.append('D@BORE: Brennan A2 DRILL proposed (only source); the OMi 2026-10-18 drawings of sibling sizes print the stem bore 0.01-0.02 below the Brennan drill on 7 of 7 bores (wave2 tee_elbow) - flag')
    r.gates.append(TOOLGATE.format(t='1504') + ' (wave2 tee_elbow: 1504 held by the approved-but-unmerged angled-leg / NPSM-neck capabilities)')
    r.done(axial=AX_B + 'N2 / M / W2 / nut hex / flats / stem bore from the Brennan TFA catalog p.22; tap drill, thread majors from the end library',
           comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.22 alone, end details from the end library; marked DimSource BRENNAN')

# ============================================================ 2404 (male JIC x male NPTF connector) - OMi first
M2404 = [('D1@DRIVE', 'L LGTH', 'overall length', 'Overall Length'), ('HEXB@HEX', 'C HEX', 'body hex', 'Hex Flat'),
         ('_BJIC', 'B1 DRILL', 'JIC-end bore', 'Side 1 ID'), ('_APIPE', 'A2 DRILL', 'pipe-end bore', 'Side 2 ID')]
pairing('2404_FINAL', [('D1@DRIVE', 'L LGTH', 'overall'), ('HEXB@HEX', 'C HEX', 'body hex')], 'TFA-p006', '(TFA p.6 "2404 MJ-MP STRAIGHT")')
for pn in ('2404-14-12', '2404-16-08'):
    a, b = dashes(pn)          # a = JIC, b = pipe
    r = Row('2404_FINAL', pn)
    t_, rr = catrow(pn)
    assert thr_eq(rr['values']['B1 SAE 37Deg'].replace('-', ' ', 1), G.JIC[a]['thr']) and thr_eq(rr['values']['A2 NPTF'], NPT[b]), rr['values']
    MAP = 'TFA p.6 2404 drawing: L = overall, C HEX = body hex, B1 DRILL = JIC-end bore, A2 DRILL = pipe-end bore (wave2 straight DRAW["2404L"]; OMi Overall Length / Hex Flat / Side 1 ID (JIC) / Side 2 ID (pipe) = the same features, mapping certain on the built 2404 rows, A19)'
    for col, cc, mean, oc in M2404:
        r.cat(col, cc, mean, MAP, omi=oc)
    bj, bp = r.v.pop('_BJIC'), r.v.pop('_APIPE')
    jb, pb = bj[0], bp[0]
    r.lib('PIPEOD@DRIVE', G.NPTF[b][2], NPSRC.format(nps=G.NPTF[b][0], d=b))
    r.lib('NPTF_ENDL@DRIVE', G.ENDL[b], ENDLSRC.format(d=b, v=G.ENDL[b]))
    hx = r.v['HEXB@HEX'][0]
    r.other('BODYDIA@DRIVE', round(hx * 2 / 3 ** 0.5, 4), f'derived: hex across corners = HEXB {fmt(hx)} x 2/sqrt(3) (the rule every row of this table follows, e.g. 2404-16-12 1.375 -> 1.5877)')
    r.lib('THDMAJ_B@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major')
    jicchain(r, a)
    # bores: the table's two-bore encoding (D3 = the smaller through bore, the larger as a counterbore at its end, no published depth -> hex mid-plane)
    if pb <= jb:
        r.other('D3@BORE_THRU', pb, f'= the pipe-end bore {fmt(pb)} ({bp[1].split(";")[0]}) - the smaller bore runs through (table convention, e.g. 2404-20-16)')
        r.other('CBDIA@BORE_A', pb, 'pipe end (End A) carries the through bore: CBDIA = D3, $STATE S (table convention)')
        r.other('DEPTH@CBCUT_A', 0.1, 'constant 0.1 on every suppressed counterbore of this table (table convention)')
        r.other('$STATE@CBCUT_A', 'S', 'suppressed: End A has no counterbore')
        r.other('CBDIA@BORE_B', jb, f'= the JIC-end bore {fmt(jb)} ({bj[1].split(";")[0]})' + (' - equal to the pipe bore: the step has zero height (two published bores of the same size)' if abs(jb - pb) < 1e-9 else ''))
        r.put('DEPTH@CBCUT_B', None, 'empty = no published counterbore depth -> step at the hex mid-plane (generator rule MID2404_ASSUME, as on 2404-20-16 / -24-16)', 'other')
        r.other('$STATE@CBCUT_B', 'U', 'unsuppressed: the JIC-end bore is the counterbore (table convention)')
    else:
        raise SystemExit('pipe bore larger than JIC bore: not expected for these two')
    r.other('$PRP@Description', f'Male Connector, Male 37 deg Flare (JIC) x Male Pipe NPTF, {G.JIC[a]["thr"]} x {NPT[b]}', 'format of the table\'s rows (the generator writes its own description)')
    r.other('$PRP@GeometryRoot', '2404', 'constant of the table')
    r.other('$PRP@EndA_Thread', NPT[b], NPSRC.format(nps=G.NPTF[b][0], d=b) + ' thread text')
    r.other('$PRP@EndB_Thread', G.JIC[a]['thr'], JICSRC.format(d=a) + ' thread text')
    r.other('$PRP@Material', 'Carbon Steel', 'constant of the table (carbon steel only)')
    r.other('$PRP@Finish', 'Trivalent Cr3 Zinc', 'constant of the table')
    r.notes.append('PressureRating left empty: no source (the Brennan-only rows of this table leave it empty too)')
    r.done(axial='OMi-only SKU (absent from Air-Way); dropped by the 2026-09-23 crawl (adapters77 2026-10-16); L / hex / bores: OMi WebsitePartsInfo2026 Items (= Brennan TFA p.6 on every cell; OMi and Brennan count as one source); JIC end MS33656J chain, NPTF end ASME + ENDL; bores: two published bores, step at the hex mid-plane',
           comment=COMMENT0 + '; L / hex / bores from OMi Items (= the Brennan TFA catalog p.6 on every cell, one source); end details from the end library',
           dimsource='OMI')

# ============================================================ 2502 (JIC x female pipe 90 elbow, forged) - Q-HX
M2502 = [('M1@DRIVE', 'M LGTH', 'axis crossing to the JIC tip', 'M 1 Size'), ('N1@DRIVE', 'L LGTH', 'axis crossing to the female NPTF port face', 'L 1 Size'),
         ('Y1@DRIVE', 'Y FLATS', 'forged body flats', 'Hex Flat'), ('D@BORE', 'B1 DRILL', 'JIC end drill', 'Side 1 ID')]
pairing('2502', [x[:3] for x in M2502], 'TFA-p025', '(TFA p.25 "2502-FG MJ-FP 90 DEG ELBOW")')
for pn in ('2502-04-06-FG', '2502-05-04-FG'):
    a, b = dashes(pn)
    r = Row('2502', pn)
    t_, rr = catrow(pn)
    MAP = 'TFA p.25 2502-FG drawing: M = crossing to the JIC tip, L = crossing to the female port face, Y = forged flats, B1 DRILL = JIC drill (wave2 tee_elbow mapping_evidence.txt: same -FG rows 10/10 on every column; OMi M 1 / L 1 / Hex Flat / Side 1 ID = the same features)'
    for col, cc, mean, oc in M2502:
        r.cat(col, cc, mean, MAP, omi=oc)
    r.lib('TAPDRILL@BORE', G.FPT[b]['TD'], FPTSRC.format(d=b))
    r.lib('THDMAJ_B@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major')
    r.lib('THDMAJ_A@DRIVE', G.NPTF[b][2], NPSRC.format(nps=G.NPTF[b][0], d=b))
    r.other('$PRP@Threads', f'{G.JIC[a]["thr"]} (JIC 37) x {NPT[b]} (NPTF female)', 'thread callouts from the part-number dashes, format of the table\'s rows (= OMi Side 1 / Side 2 Thread)')
    r.gates.append('GATE Q-HX (A7 answered 2026-10-18: move 2502HX to the generator LATER): no 2502 generator SPEC yet')
    r.notes.append('MS51506 not checked for these sizes (Q-CONFLICT-2502-MS51506 concerns -08-04 / -12-08 only)')
    r.done(axial=AX_O + 'M1 / N1 / flats / bore: OMi WebsitePartsInfo2026 Items (= Brennan TFA p.25, one source); tap drill = Air-Way per size (A1); JIC end MS33656J',
           comment=COMMENT0 + '; legs / flats / bore from OMi Items (= Brennan TFA p.25, one source); end details from the end library', dimsource='OMI')

# ============================================================ 2504 (45 JIC union elbow, forged) - SPEC 2504
M2504 = [('M2_1@DRIVE', 'M1 LGTH', 'leg 1 JIC tip to the crossing', 'M 1 Size'), ('M2_2@DRIVE', 'M2 LGTH', 'leg 2 JIC tip to the crossing', 'M 2 Size'),
         ('Y@HEX', 'Y FLATS', 'forged body flats', 'Hex Flat'), ('D1@BORE', 'B1 DRILL', 'leg 1 bore', 'Side 1 ID'), ('D2@BORE', 'B2 DRILL', 'leg 2 bore', 'Side 2 ID')]
pairing('2504', [x[:3] for x in M2504], 'TFA-p026', '(TFA p.26 "2504-FG MJ-MJ 45 DEG ELBOW")')
pn = '2504-16-16-FG'; a, b = dashes(pn)
r = Row('2504', pn)
MAP = 'TFA p.26 2504-FG drawing: M1 / M2 = legs, Y = flats, B1 / B2 DRILL = bores (the table\'s own AxialSource names this mapping for the OMi columns; pairing in mapping_evidence.txt)'
for col, cc, mean, oc in M2504:
    r.cat(col, cc, mean, MAP, omi=oc)
r.lib('THDMAJ_B1@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major')
r.lib('THDMAJ_B2@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major')
r.notes.append('$PRP@TubeOD / $PRP@Threads left empty like the built -FG rows of this table')
r.done(axial=AX_O + 'legs / flats / bores: OMi WebsitePartsInfo2026 Items M 1 / M 2 / Hex Flat / Side 1 ID / Side 2 ID (= Brennan TFA p.26, one source); JIC ends MS33656J',
       comment=COMMENT0 + '; legs / flats / bores from OMi Items (= Brennan TFA p.26, one source)', dimsource='OMI')

# ============================================================ 2505 (45 JIC x female pipe elbow, forged) - SPEC 2505
M2505 = [('M2@DRIVE', 'M LGTH', 'JIC leg', 'M 1 Size'), ('N6@DRIVE', 'N LGTH', 'female pipe leg along the 45 deg axis', 'M 2 Size'),
         ('Y1@HEX', 'Y FLATS', 'forged body flats', 'Hex Flat'), ('D@BORE', 'B1 DRILL', 'JIC end drill', 'Side 1 ID')]
pairing('2505', [x[:3] for x in M2505], 'TFA-p027', '(TFA p.27 "2505-FG MJ-FP 45 DEG ELBOW")')
for pn in ('2505-04-04-FG', '2505-06-06-FG'):
    a, b = dashes(pn)
    r = Row('2505', pn)
    MAP = 'TFA p.27 2505-FG drawing: M = JIC leg, N = female leg, Y = flats, B1 DRILL = JIC drill (wave2 tee_elbow: same -FG rows 3/3 on every column; OMi M 1 / M 2 / Hex Flat / Side 1 ID)'
    for col, cc, mean, oc in M2505:
        r.cat(col, cc, mean, MAP, omi=oc)
    r.lib('TAPDRILL@BORE', G.FPT[b]['TD'], FPTSRC.format(d=b))
    r.lib('THDMAJ_B@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major')
    r.lib('THDMAJ_A@DRIVE', G.NPTF[b][2], NPSRC.format(nps=G.NPTF[b][0], d=b))
    r.put('PORTDEPTH@BORE', None, 'empty like every built row of this table (the generator uses the library port depth P1; Q-ANGLED-P1 applies if the leg is shorter)', 'none')
    r.notes.append('$PRP@TubeOD / $PRP@Threads left empty like the built -FG rows; PORTDEPTH@BORE empty like every built row (library P1)')
    r.done(axial=AX_O + 'legs / flats / bore: OMi WebsitePartsInfo2026 Items (= Brennan TFA p.27, one source); tap drill = Air-Way per size (A1); JIC end MS33656J',
           comment=COMMENT0 + '; legs / flats / bore from OMi Items (= Brennan TFA p.27, one source); end details from the end library', dimsource='OMI')
    r.missing = [m for m in r.missing if m != 'PORTDEPTH@BORE']
    ROWS[-1]['missing_columns'] = ' ; '.join(m for m in ROWS[-1]['missing_columns'].split(' ; ') if m and m != 'PORTDEPTH@BORE')
    if not ROWS[-1]['missing_columns'] and not ROWS[-1]['gates']:
        ROWS[-1]['ready'] = 'yes'
        for x in NEW:
            if x['config'] == pn and x['column'] == '$PRP@DataStatus':
                x['value'] = 'ASSUMED'; x['source'] = 'every driving cell has a source (PORTDEPTH empty = library P1, as on every built row); one source -> ASSUMED'

# ============================================================ 2613 (MP x FP x MJ tee, forged) - no SPEC
M2613 = [('N5@DRIVE', 'L LGTH', 'run axis to the A1 male NPTF tip'), ('N1@DRIVE', 'L1 LGTH', 'run axis to the A2 female NPTF port face'),
         ('M1@DRIVE', 'M LGTH', 'run axis to the B3 JIC tip'), ('Y1@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'A1 DRILL', 'male NPTF drill'),
         ('D@BORE', 'B3 DRILL', 'JIC drill')]
pairing('2613', M2613, 'TFA-p053', '(TFA p.53 "2613-FG MP-FP-MJ TEE")')
twin_pairing('2613', M2613, [('2613-04-04-04', '2613-04-04-04-FG'), ('2613-04-04-06', '2613-04-04-06-FG'), ('2613-08-08-10', '2613-08-08-10-FG'), ('2613-12-12-12', '2613-12-12-12-FG')],
             'Air-Way plain rows vs the Brennan -FG row of the same size (different parts; letter check only)')
pn = '2613-04-04-04-FG'; a1, a2, b3 = dashes(pn)
r = Row('2613', pn)
MAP = ('TFA p.53 2613-FG drawing (A1 male pipe, A2 female pipe, B3 JIC): L = to the male tip, L1 = to the female face, M = to the JIC tip, Y = flats, A1 / B3 DRILL = bores; '
       'the same letters as the 2611-FG table wave2 confirmed (M1 <- M, N5 <- L, N1 <- L1); Air-Way plain twins agree on L / L1 / bores (mapping_evidence.txt), M differs (forged vs plain body, as on 2611)')
for col, cc, mean in M2613:
    r.cat(col, cc, mean, MAP)
r.lib('TAPDRILL@BORE', G.FPT[a2]['TD'], FPTSRC.format(d=a2))
r.lib('THDMAJ_A1@DRIVE', G.NPTF[a1][2], NPSRC.format(nps=G.NPTF[a1][0], d=a1))
r.lib('THDMAJ_A2@DRIVE', G.NPTF[a2][2], NPSRC.format(nps=G.NPTF[a2][0], d=a2))
r.lib('THDMAJ_B@DRIVE', G.JIC[b3]['TM'], JICSRC.format(d=b3) + ' thread major')
r.other('$PRP@TubeOD', '1/4', 'Brennan TFA p.53 col "TUBE O.D." = "1/4" (= the -04 JIC tube; format of the table\'s rows)')
r.other('$PRP@Threads', f'{NPT[a1]} (A (1) NPTF) x {NPT[a2]} (A (2) NPTF) x {G.JIC[b3]["thr"]} (B UN/UNF-2A)', 'thread callouts from the part-number dashes, format of the table\'s rows')
r.gates.append(TOOLGATE.format(t='2613'))
r.done(axial=AX_B + 'legs / flats / bores from the Brennan TFA catalog p.53; tap drill = Air-Way per size (A1); thread majors from the end library',
       comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.53 alone; marked DimSource BRENNAN')

# ============================================================ 2705-06-04 (female pipe x JIC bulkhead) - SPEC 2705
pairing('2705', [('L24@DRIVE', 'L LGTH', 'overall'), ('C5HEX@HEX', 'C1 HEX', 'body hex'), ('D@BORE', 'B2 DRILL', 'bore')], 'TFA-p008', '(TFA p.8 "2705 FP-MJ BULKHEAD STRAIGHT")')
pn = '2705-06-04'; a, b = dashes(pn)
r = Row('2705', pn)
MAP = 'TFA p.8 2705 drawing: L = overall, C1 HEX = body hex, B2 DRILL = bulkhead-end bore (OMi Overall Length / Hex Flat / Side 2 ID = the same features: impact/F2a.json M056-M058, certain)'
for col, cc, mean, oc in (('L24@DRIVE', 'L LGTH', 'overall length', 'Overall Length'), ('C5HEX@HEX', 'C1 HEX', 'body hex', 'Hex Flat'), ('D@BORE', 'B2 DRILL', 'bore from the bulkhead tip', 'Side 2 ID')):
    r.cat(col, cc, mean, MAP, omi=oc)
hdr, rows = table('2705')
i1 = sorted({(k, v['I1@DRIVE']) for k, v in rows.items() if not empty(v.get('I1@DRIVE')) and dashes(k)[1:2] == [b] and 'LN' not in k})
assert len({x[1] for x in i1}) == 1, i1
r.other('I1@DRIVE', i1[0][1], f'Air-Way bulkhead length of the -{b:02d} JIC bulkhead = {i1[0][1]} (stage rows {", ".join(k for k, _ in i1)}) [user 2026-10-18 A8 Q-TRANSFER-I1 yes: Air-Way I1 per size, -04 1.20]')
r.lib('TAPDRILL@BORE', G.FPT[a]['TD'], FPTSRC.format(d=a))
r.lib('THDMAJ_A@DRIVE', G.NPTF[a][2], NPSRC.format(nps=G.NPTF[a][0], d=a))
r.lib('THDMAJ_B@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major')
tub = sorted({(k, v['$PRP@TubeOD']) for k, v in rows.items() if not empty(v.get('$PRP@TubeOD')) and len(set(dashes(k)[:2])) == 2})
r.notes.append(f'$PRP@TubeOD left empty: OMi Side 2 Size (JIC) 1/4 vs Brennan TUBE O.D. 3/8 (pipe dash); unequal-dash rows of this table with a TubeOD: {tub[:3]} - convention not settled, property only')
r.other('$PRP@Threads', f'{NPT[a]} (A NPTF) x {G.JIC[b]["thr"]} (B UN/UNF-2A)', 'thread callouts from the part-number dashes, format of the table\'s rows (= OMi Side 1 / Side 2 Thread)')
r.done(axial=AX_O + 'L24 / hex / bore: OMi WebsitePartsInfo2026 Items (= Brennan TFA p.8, one source); I1 = Air-Way -04 bulkhead length (A8); tap drill = Air-Way per size (A1); JIC end MS33656J',
       comment=COMMENT0 + '; L24 / hex / bore from OMi Items (= Brennan TFA p.8), I1 = Air-Way per size (A8)', dimsource='OMI')

# ============================================================ 3474 (adjustable ORB x ORB straight) - skeleton table, no SPEC
pn_list = ('3474-08-08-NWO', '3474-10-10-NWO')
h6801, r6801 = table('6801')
for pn in pn_list:
    a, b = dashes(pn)
    r = Row('3474', pn)
    t_, rr = catrow(pn)
    MAP = 'TFA p.9 3474-NWO drawing: L1 = tip to tip, C1 HEX = locknut hex, C2 HEX = body hex, B1 / B2 DRILL = adjustable / fixed-end bores (wave1 w1brennan, same mapping on the 7 sibling rows)'
    r.cat('L1@DRIVE', 'L1 LGTH', 'tip to tip', MAP); r.cat('C1HEX@HEX', 'C1 HEX', 'locknut hex', MAP); r.cat('C2HEX@HEX', 'C2 HEX', 'body hex', MAP)
    r.cat('D1@BORE', 'B1 DRILL', 'adjustable-end bore', MAP); r.cat('D2@BORE', 'B2 DRILL', 'fixed-end bore', MAP)
    r.lib('THDMAJ_A@DRIVE', G.ORB[a]['TM'], ORBSRC.format(d=a) + f' thread major = Brennan "B1 AORB" "{rr["values"]["B1 AORB"]}"')
    r.lib('THDMAJ_B@DRIVE', G.ORB[b]['TM'], ORBSRC.format(d=b) + f' thread major = Brennan "B2 ORB" "{rr["values"]["B2 ORB"]}"')
    src6801 = f'6801-{a:02d}-{a:02d}-NWO-FG'
    for col in ('ORB_I3@DRIVE', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'):
        r.lib(col, r6801[src6801][col], f'end library (adjustable ORB stud of the same ORB size): DesignTable_6801.xlsx row {src6801} col {col} = {r6801[src6801][col]} (today\'s stage table) - no 3474 STEP of this size; same rule as wave1 w1brennan for the 7 sibling rows [Q-TRANSFER-ENDLIB yes 2026-10-08]')
    r.gates.append('GATE TOOLCHAIN: the 3474 family (SPEC 3474 + NWO_3474_TRANSFER, tools/_out/newmasters_20261002/work/3474) is not merged into the batch-16 tools; the stage table is the 7-column skeleton (wave1 w1brennan_cells.csv adds the same family columns to the 7 sibling rows)')
    r.done(axial=AX_B + 'L1 / hexes / bores from the Brennan TFA catalog p.9; ORB majors from the end library; adjustable-end I3 / thread length / groove from the 6801 row of the same ORB size',
           comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.9 alone; adjustable end data from the 6801 end library; marked DimSource BRENNAN')

# ============================================================ 5404-N-06X5.500 (round long nipple) - SPEC 5404N (A4)
pn = '5404-N-06X5.500'; d = 6; X = 5.5
r = Row('5404N', pn)
t_, rr = catrow(pn)
assert abs(float(rr['values']['L LGTH']) - X) < 1e-9
r.other('L@DRIVE', X, f'length = the X of the OMi part number {pn} [user 2026-10-18 A4: Q-TRANSFER-5404N yes, length from the part number; keep the OMi form]; cross-check Brennan TFA p.11 {t_["table_id"]} L LGTH "{rr["values"]["L LGTH"]}": equal')
hdr, rows = table('5404N'); AW = '5404-N-06-06-X1'; awr = rows[AW]
for col in ('COD@REF', 'D1@BORE', 'D2@BORE'):
    r.other(col, awr[col], f'Air-Way 5404-N nipple of the same size: stage row {AW} ({awr["$PRP@ScopeAction"]}, {awr["$PRP@DataStatus"]}) {col} = {awr[col]} [user 2026-10-18 A4: Q-TRANSFER-5404N yes - bar diameter and bore from the Air-Way nipple of the same size, every length]')
r.conf.append(f'D1/D2: Air-Way transfer {awr["D1@BORE"]} (A4, used) vs Brennan TFA p.11 A1 / A2 DRILL {rr["values"]["A1 DRILL"]} - information only (as wave2 straight on the other 5404-N rows)')
for col in ('THDMAJ_A1@DRIVE', 'THDMAJ_A2@DRIVE'):
    r.lib(col, G.NPTF[d][2], NPSRC.format(nps=G.NPTF[d][0], d=d))
r.other('$PRP@Threads', f'{NPT[d]} x {NPT[d]} NPTF, cut length 5.5 in', 'thread texts from the part-number dash, format of the built 5404N rows')
r.notes.append('expected to BLOCK in gen_straight2 SPEC 5404N: it reads only the Air-Way "5404-N-6-6 X 1" form ("no dash pair" on the OMi form) - generator work scheduled (wave2 straight, 18 sibling rows)')
r.done(axial=AX_O + 'L from the part number (= Brennan TFA p.11); bar dia / bores from the Air-Way nipple 5404-N-06-06-X1 (A4 transfer); NPTF ends ASME',
       comment=COMMENT0 + '; L from the part number, bar dia and bores from the Air-Way nipple 5404-N-06-06-X1 (A4 yes 2026-10-18); no Brennan size used', dimsource='')

# ============================================================ 5601 (MP x MP x FP branch tee, forged) - SPEC 5601
M5601 = [('N_1@DRIVE', 'N1 LGTH', 'A1 male run leg'), ('N2@DRIVE', 'N2 LGTH', 'A2 male run leg'), ('N1@DRIVE', 'N3 LGTH', 'A3 female branch port face'),
         ('W@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'A1 DRILL', 'A1 drill'), ('D2@BORE', 'A2 DRILL', 'A2 drill')]
pairing('5601', M5601, 'TFA-p055', '(TFA p.55 "5601-FG MP-MP-FP TEE")')
twin_pairing('5601', M5601, [('5601-08-08-08', '5601-08-08-08-FG'), ('5601-12-12-12', '5601-12-12-12-FG'), ('5601-16-16-16', '5601-16-16-16-FG'), ('5601-04-04-04', '5601-04-04-04-FG'), ('5601-06-06-06', '5601-06-06-06-FG')],
             'Air-Way plain rows vs the Brennan -FG row of the same size (different parts; letter check only)')
for pn in ('5601-08-08-08-FG', '5601-12-12-12-FG', '5601-16-16-16-FG'):
    a1, a2, a3 = dashes(pn)
    r = Row('5601', pn)
    MAP = 'TFA p.55 5601-FG drawing: N1 / N2 = male run legs, N3 = female branch face, Y = flats, A1 / A2 DRILL = male drills (wave1 w1brennan 5601 rows -02 / -04 / -06 / -20, built in the stage)'
    for col, cc, mean in M5601:
        r.cat(col, cc, mean, MAP)
    r.lib('TAPDRILL@BORE', G.FPT[a3]['TD'], FPTSRC.format(d=a3))
    for col, dd in (('THDMAJ_A1@DRIVE', a1), ('THDMAJ_A2@DRIVE', a2), ('THDMAJ_A3@DRIVE', a3)):
        r.lib(col, G.NPTF[dd][2], NPSRC.format(nps=G.NPTF[dd][0], d=dd))
    r.other('$PRP@Threads', f'{NPT[a1]} (A (1) NPTF) x {NPT[a2]} (A (2) NPTF) x {NPT[a3]} (A (3) NPTF)', 'thread callouts from the part-number dashes, format of the table\'s rows')
    r.done(axial=AX_B + 'legs / flats / drills from the Brennan TFA catalog p.55; tap drill = Air-Way per size (A1); NPTF majors ASME',
           comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.55 alone; marked DimSource BRENNAN')

# ============================================================ 6402-12-10-O (male ORB x female JIC swivel) - SPEC 6402, OMi first
M6402 = [('L26@DRIVE', 'L1 LGTH', 'ORB tip to the nut face (overall)', 'Overall Length'), ('L27@DRIVE', 'L LGTH', 'ORB tip to the seat', 'L 1 Size'),
         ('C4HEX@HEX', 'C HEX', 'body hex', 'Hex Flat'), ('C3HEX@HEX', 'C1 HEX', 'swivel nut hex', 'Nut Hex 1'),
         ('D1@BORE', 'B DRILL', 'ORB-end bore', 'Side 1 ID'), ('D2@BORE', 'A DRILL', 'swivel-end bore', 'Side 2 ID')]
pairing('6402', [x[:3] for x in M6402], 'TFA-p015', '(TFA p.15 "6402-O MORB-FJS STRAIGHT")')
pn = '6402-12-10-O'; a, b = dashes(pn)
r = Row('6402', pn)
MAP = 'TFA p.15 6402-O drawing: L1 = overall to the nut face, L = to the seat, C = body hex, C1 = nut hex, B / A DRILL = bores; OMi Overall Length / L 1 / Hex Flat / Nut Hex 1 / Side 1 ID / Side 2 ID = the same features (A19 group 3: M020 / M021 on the built rows)'
for col, cc, mean, oc in M6402:
    r.cat(col, cc, mean, MAP, omi=oc)
r.lib('THDMAJ_B1@DRIVE', G.ORB[a]['TM'], ORBSRC.format(d=a) + ' thread major (male ORB end)')
r.lib('THDMAJ_B2@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major (female JIC swivel)')
hdr, rows = table('6402')
tub = sorted({(k, v['$PRP@TubeOD']) for k, v in rows.items() if not empty(v.get('$PRP@TubeOD')) and len(set(dashes(k)[:2])) == 2})
r.notes.append(f'$PRP@TubeOD left empty: OMi Side 1 Size 3/4 (= Brennan TUBE O.D.) vs the JIC swivel tube 5/8 (OMi Side 2 Size); the table\'s unequal-dash rows carry Air-Way\'s own reading ({tub[:4]}; AxialSource flags 6402-6-8-O / -8-12-O) - not settled, property only')
r.other('$PRP@Threads', f'{G.JIC[a]["thr"]} (B (1) UN/UNF-2A) x {G.JIC[b]["thr"]} (B (2) UN/UNF-2B)', 'thread callouts from the part-number dashes, format of the table\'s rows (= OMi Side 1 / Side 2 Thread)')
r.done(axial=AX_O + 'L26 / L27 / body hex / nut hex / bores: OMi WebsitePartsInfo2026 Items (= Brennan TFA p.15 on every cell, one source); ORB end from the ORB library; JIC swivel from SWIV_MEAS',
       comment=COMMENT0 + '; sizes from OMi Items (= the Brennan TFA catalog p.15, one source)', dimsource='OMI')

# ============================================================ 6801-16-10-NWO-FG (JIC x adjustable ORB 90 elbow, forged) - SPEC 6801
M6801 = [('LEG_JIC@DRIVE', 'M LGTH', 'JIC tip to the ORB axis'), ('LEG_ORB@DRIVE', 'M7 LGTH', 'adjustable ORB tip to the JIC axis'),
         ('HEXB@HEX', 'C HEX', 'locknut hex'), ('D1@BORE', 'B1 DRILL', 'JIC-end bore'), ('D2@BORE', 'B2 DRILL', 'ORB-end bore'), ('Y@REF', 'Y FLATS', 'forged body flats')]
pairing('6801', M6801, 'TFA-p04', '(TFA p.40 / p.41 "6801-NWO-FG MJ-MAORB 90 DEG ELBOW")')
pn = '6801-16-10-NWO-FG'; a, b = dashes(pn)
r = Row('6801', pn)
MAP = 'TFA p.41 6801-NWO-FG drawing: M = JIC leg, M7 = adjustable ORB leg, C = locknut hex, B1 / B2 DRILL = bores, Y = flats (pairing on the built 6801 rows: mapping_evidence.txt; b15held / batch 15 used the same letters)'
for col, cc, mean in M6801:
    r.cat(col, cc, mean, MAP)
r.lib('THDMAJ_A@DRIVE', G.JIC[a]['TM'], JICSRC.format(d=a) + ' thread major (JIC end)')
jicchain(r, a)
r.lib('THDMAJ_B@DRIVE', G.ORB[b]['TM'], ORBSRC.format(d=b) + ' thread major (adjustable ORB end)')
hdr, rows = table('6801')
same = {k: v for k, v in rows.items() if len(dashes(k)) >= 2 and dashes(k)[1] == b and all(not empty(v.get(c)) for c in ('ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE', 'ORB_GRVW@DRIVE', 'ORB_I3@DRIVE'))}
for col in ('ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE', 'ORB_GRVW@DRIVE', 'ORB_I3@DRIVE'):
    vals = collections.Counter(round(float(v[col]), 4) for v in same.values())
    blt = collections.Counter(round(float(v[col]), 4) for v in same.values() if v.get('$PRP@ScopeAction') == 'BUILD')
    use = blt if blt else vals
    if len(use) == 1:
        val = next(iter(use))
        r.lib(col, val, f'adjustable-ORB end value of the -{b:02d} ORB size from the table\'s own rows: {col} = {fmt(val)} on every row with ORB -{b:02d} ({", ".join(sorted(k for k, v in same.items() if (not blt or v.get("$PRP@ScopeAction") == "BUILD")))}) [user 2026-10-18 A5 Q-NEW-F1B-ORBEND yes]'
              + ('' if len(vals) == 1 else f' (DROP rows differ: {dict(vals)})'))
    else:
        r.missing.append(col); r.put(col, None, f'rows of ORB -{b:02d} disagree: {dict(use)} - not picked', 'none'); r.conf.append(f'{col}: same-ORB-size rows differ {dict(use)}')
r.other('$PRP@EndA_Thread', G.JIC[a]['thr'], JICSRC.format(d=a) + ' thread text')
r.other('$PRP@EndB_Thread', G.JIC[b]['thr'], ORBSRC.format(d=b) + ' thread text (ORB UN thread = the same callout)')
r.done(axial=AX_B + 'legs / locknut hex / bores / flats from the Brennan TFA catalog p.41; JIC end MS33656J; adjustable ORB end data from the table\'s own -10 ORB rows (A5)',
       comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.41 alone; JIC end chain + ORB end data from the libraries / same-ORB-size rows; marked DimSource BRENNAN')

# ============================================================ 6803-04-04-06-NWO-FG (JIC run x adjustable ORB branch tee) - SPEC 6803
M6803 = [('LEG1@DRIVE', 'M1 LGTH', 'B1 JIC leg'), ('LEG2@DRIVE', 'M2 LGTH', 'B2 JIC leg'), ('LEG3@DRIVE', 'M7 LGTH', 'B3 adjustable ORB leg'),
         ('HEXB@HEX', 'C HEX', 'locknut hex'), ('Y@REF', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'B1 DRILL', 'B1 bore'), ('D2@BORE', 'B2 DRILL', 'B2 bore'), ('D3@BORE', 'B3 DRILL', 'B3 bore')]
pairing('6803', M6803, 'TFA-p059', '(TFA p.59 "6803-NWO-FG MJ-MJ-MAORB BRANCH TEE")')
twin_pairing('6803', M6803, [(k, k + '-FG') for k in table('6803')[1] if k.endswith('-NWO')], 'Air-Way plain rows vs the Brennan -FG row of the same size (different parts; letter check only)')
pn = '6803-04-04-06-NWO-FG'; a1, a2, b3 = dashes(pn)
r = Row('6803', pn)
MAP = 'TFA p.59 6803-NWO-FG drawing: M1 / M2 = JIC run legs, M7 = adjustable ORB branch, C = locknut hex, Y = flats, B1-B3 DRILL = bores (pairing on the built 6803 rows: mapping_evidence.txt)'
for col, cc, mean in M6803:
    r.cat(col, cc, mean, MAP)
r.lib('THDMAJ_1@DRIVE', G.JIC[a1]['TM'], JICSRC.format(d=a1) + ' thread major')
r.lib('THDMAJ_2@DRIVE', G.JIC[a2]['TM'], JICSRC.format(d=a2) + ' thread major')
r.lib('THDMAJ_3@DRIVE', G.ORB[b3]['TM'], ORBSRC.format(d=b3) + ' thread major (adjustable ORB branch)')
hdr, rows = table('6803')
same = {k: v for k, v in rows.items() if len(dashes(k)) >= 3 and dashes(k)[2] == b3 and all(not empty(v.get(c)) for c in ('ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE', 'ORB_GRVW@DRIVE'))}
for col, lk in (('ORB_THDL@DRIVE', 'THDL'), ('ORB_GRVDIA@DRIVE', 'GD'), ('ORB_GRVW@DRIVE', 'GW')):
    vals = collections.Counter(round(float(v[col]), 4) for v in same.values())
    blt = collections.Counter(round(float(v[col]), 4) for v in same.values() if v.get('$PRP@ScopeAction') == 'BUILD')
    use = blt if blt else vals
    assert len(use) == 1, (col, use)
    val = next(iter(use))
    r.lib(col, val, f'adjustable-ORB end value of the -{b3:02d} ORB size from the table\'s own rows: {col} = {fmt(val)} on {", ".join(sorted(k for k, v in same.items() if (not blt or v.get("$PRP@ScopeAction") == "BUILD")))}'
          + (' (Air-Way DROP rows: no BUILD row of this ORB size has the value)' if not blt else '') + f'; = gen_straight2 ORB[{b3}] {lk} {G.ORB[b3][lk]} [user 2026-10-18 A5 Q-NEW-F1B-ORBEND yes]')
r.other('$PRP@Threads', f'{G.JIC[a1]["thr"]} x {G.JIC[a2]["thr"]} x {G.JIC[b3]["thr"]}', 'thread callouts from the part-number dashes, format of the table\'s rows')
r.notes.append('ORB_I3: none in this table - gen_tee SPEC 6803 takes the 6801 adjustable-end I3 of the same ORB size (nwo "=6801")')
r.done(axial=AX_B + 'legs / locknut hex / flats / bores from the Brennan TFA catalog p.59; JIC ends MS33656J; ORB branch end data from the table\'s own -06 ORB rows (A5) = the ORB library',
       comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.59 alone; marked DimSource BRENNAN')

# ============================================================ 6807 (adjustable ORB x adjustable ORB 90 elbow, forged) - no SPEC
M6807 = [('M7_1@DRIVE', 'M1 LGTH', 'B1 adjustable ORB leg'), ('M7_2@DRIVE', 'M2 LGTH', 'B2 adjustable ORB leg'), ('C4_1HEX@HEX', 'C HEX', 'B1 locknut hex'),
         ('C4_2HEX@HEX', 'C2 HEX', 'B2 locknut hex'), ('Y@HEX', 'Y FLATS', 'forged body flats'), ('D1@BORE', 'B1 DRILL', 'B1 bore'), ('D2@BORE', 'B2 DRILL', 'B2 bore')]
pairing('6807', M6807, 'TFA-p044', '(TFA p.44 "6807-NWO-FG MAORB-MAORB 90 DEG ELBOW")')
twin_pairing('6807', M6807, [(f'6807-{x}-{x} NWO', f'6807-{x}-{x}-NWO-FG') for x in ('16', '20', '24', '32')], 'Air-Way plain rows vs the Brennan -FG row of the same size (different parts; letter check only)')
for pn in ('6807-16-16-NWO-FG', '6807-20-20-NWO-FG'):
    a, b = dashes(pn)
    r = Row('6807', pn)
    MAP = 'TFA p.44 6807-NWO-FG drawing: M1 / M2 = legs, C / C2 HEX = locknut hexes, Y = flats, B1 / B2 DRILL = bores (Air-Way plain twins agree on legs / locknut hexes / bores: mapping_evidence.txt; flats differ = forged vs plain)'
    for col, cc, mean in M6807:
        r.cat(col, cc, mean, MAP)
    r.lib('THDMAJ_B1@DRIVE', G.ORB[a]['TM'], ORBSRC.format(d=a) + ' thread major')
    r.lib('THDMAJ_B2@DRIVE', G.ORB[b]['TM'], ORBSRC.format(d=b) + ' thread major')
    r.other('$PRP@Threads', f'{G.JIC[a]["thr"]} (B (1) UN/UNF-2A) x {G.JIC[b]["thr"]} (B (2) UN/UNF-2A)', 'thread callouts from the part-number dashes, format of the table\'s rows')
    r.gates.append(TOOLGATE.format(t='6807'))
    r.done(axial=AX_B + 'legs / locknut hexes / flats / bores from the Brennan TFA catalog p.44; ORB majors from the end library',
           comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.44 alone; marked DimSource BRENNAN')

# ============================================================ 6809 (adjustable ORB x female JIC swivel 90 elbow, forged) - no SPEC
M6809 = [('M7@DRIVE', 'M7 LGTH', 'adjustable ORB tip to the swivel axis'), ('M5@DRIVE', 'M6 LGTH', 'ORB axis to the swivel-nut face'), ('M10@DRIVE', 'M LGTH', 'ORB axis to the swivel nose / seat'),
         ('C3HEX@HEX', 'C2 HEX', 'swivel nut hex (end B2)'), ('C4HEX@HEX', 'C1 HEX', 'locknut hex (end B1)'), ('Y@HEX', 'Y FLATS', 'forged body flats'),
         ('D1@BORE', 'B1 DRILL', 'ORB-end bore'), ('D2@BORE', 'B2 DRILL', 'swivel-end bore')]
pairing('6809', M6809, 'TFA-p044', '(TFA p.44 "6809-NWO-FG MAORB-FJS 90 DEG ELBOW")')
twin_pairing('6809', M6809, [(k, k.replace(' NWO', '-NWO-FG')) for k in table('6809')[1] if k.endswith(' NWO')], 'Air-Way plain rows vs the Brennan -FG row of the same size (different parts; letter check only)')
for pn in ('6809-04-04-NWO-FG', '6809-06-06-NWO-FG', '6809-08-08-NWO-FG'):
    a, b = dashes(pn)
    r = Row('6809', pn)
    MAP = ('TFA p.44 6809-NWO-FG drawing: M7 = ORB leg, M6 = to the nut face, M = to the seat, C1 HEX = locknut (end B1), C2 HEX = swivel nut (end B2), Y = flats, B1 / B2 DRILL = bores; '
           'Air-Way plain twins agree on M7 / hexes / bores (mapping_evidence.txt); M6 = nut face and M = seat leg as on the built forged swivel elbows '
           '(6500 LEG_M5 <- M6, 6502 M14 <- M on the swivel leg, 4/4 rows each); C1 = C2 on these three rows, so the nut / locknut assignment does not change a value')
    for col, cc, mean in M6809:
        r.cat(col, cc, mean, MAP)
    r.lib('THDMAJ_B1@DRIVE', G.ORB[a]['TM'], ORBSRC.format(d=a) + ' thread major (adjustable ORB)')
    r.lib('THDMAJ_B2@DRIVE', G.JIC[b]['TM'], JICSRC.format(d=b) + ' thread major (female JIC swivel)')
    t_, rr = catrow(pn)
    r.other('$PRP@TubeOD', rr['values']['TUBE O.D.'], f'Brennan TFA p.44 col "TUBE O.D." = "{rr["values"]["TUBE O.D."]}" (equal dashes; format of the table\'s rows)')
    r.other('$PRP@Threads', f'{G.JIC[a]["thr"]} (B (1) UN/UNF-2A) x {G.JIC[b]["thr"]} (B (2) UN/UNF-2B)', 'thread callouts from the part-number dashes, format of the table\'s rows')
    r.gates.append(TOOLGATE.format(t='6809'))
    r.done(axial=AX_B + 'legs / hexes / flats / bores from the Brennan TFA catalog p.44; ORB / JIC majors from the end libraries',
           comment=COMMENT0 + '; sizes from the Brennan TFA catalog p.44 alone; marked DimSource BRENNAN')

# ============================================================ 6901 (adjustable ORB x female NPSM swivel 90 elbow, forged) - no SPEC
M6901c = [('CHEX@HEX', 'C1 HEX', 'NPSM swivel nut hex'), ('C4HEX@HEX', 'C HEX', 'ORB locknut hex'), ('D1@BORE', 'B DRILL', 'ORB end drill'), ('D@BORE', 'A DRILL', 'NPSM end drill')]
M6901u = [('N5@DRIVE', 'M7 LGTH', 'candidate: ORB tip to the swivel axis'), ('M1@DRIVE', 'M LGTH', 'candidate: ORB axis to the stem tip'), ('W3@HEX', 'M6 LGTH', 'candidate: ORB axis to the nut face'),
          ('C1HEX@HEX', 'Y FLATS', 'candidate: forged body flats')]
pairing('6901', M6901c + M6901u, 'TFA-p04', '(TFA p.45 / p.46 "6901-NWO-FG MAORB-FPS 90 DEG ELBOW"; the stage -FG rows are Air-Way s142 rows, so this IS a same-part pairing)')
for pn in ('6901-08-06-NWO-FG', '6901-08-12-NWO-FG', '6901-10-06-NWO-FG'):
    a, b = dashes(pn)
    r = Row('6901', pn)
    MAP = 'TFA p.45 6901-NWO-FG drawing: C1 HEX = NPSM nut, C HEX = locknut, B DRILL = ORB drill, A DRILL = NPSM drill (wave2 tee_elbow mapping, confirmed on the Air-Way -FG rows: mapping_evidence.txt)'
    for col, cc, mean in M6901c:
        r.cat(col, cc, mean, MAP)
    t_, rr = catrow(pn)
    for col, cc, mean in M6901u:
        r.missing.append(col)
        r.put(col, None, f'not proposed: candidate Brennan {cc} = {rr["values"].get(cc)} does not pair with the Air-Way -FG rows of this table (mapping_evidence.txt; wave2 tee_elbow left it out too)', 'none')
        r.conf.append(f'{col}: candidate {cc} {rr["values"].get(cc)} not proposed (mapping not confirmed)')
    r.lib('THDMAJ_B@DRIVE', G.ORB[a]['TM'], ORBSRC.format(d=a) + ' thread major (adjustable ORB)')
    r.lib('THDMAJ_A1@DRIVE', G.NPTF[b][2], NPSMSRC.format(d=b, v=G.NPTF[b][2]))
    r.other('$PRP@Threads', f'{G.JIC[a]["thr"]} (B UN/UNF-2A) x {NPT[b]} (A1 NPSM)', 'thread callouts from the part-number dashes, format of the table\'s rows')
    r.gates.append(TOOLGATE.format(t='6901') + ' (wave2 tee_elbow: the approved capability for this family is not merged)')
    if 'D@BORE' in r.missing:
        r.gates.append('A14 (answered 2026-10-18: measure the STEP): Brennan prints the NPSM drill as a range -> needs 09_STEP_FILES/BRENNAN_' + pn + '.stp (not on disk)')
    r.done(axial=AX_B + 'nut / locknut hexes / bores from the Brennan TFA catalog p.45; legs and body flats NOT proposed (catalog letters do not pair with the Air-Way rows)',
           comment=COMMENT0 + '; hexes / bores from the Brennan TFA catalog p.45 alone; legs / flats open; marked DimSource BRENNAN')

# ============================================================ 2701-LN-02-02-FG / -05-05-FG: the plain part's row (A10 Q-TRANSFER-LN yes)
hdr, rows = table('2701')
for plain in ('2701-02-02-FG', '2701-05-05-FG'):
    pn = plain + '-LN'                       # table naming of the -LN rows (2701-06-06-FG-LN, OMiSKU 2701-LN-06-06-FG)
    r = Row('2701', pn)
    r.omisku = '2701-LN-' + plain[5:]
    pr = rows[plain]
    for col in hdr:
        if col and '@' in col and not col.startswith('$'):
            r.other(col, pr[col], f'= stage row {plain} ({pr["$PRP@ScopeAction"]}, {pr["$PRP@DataStatus"]}; built in batch 15 from its own Brennan STEP 09_STEP_FILES/BRENNAN_{plain}.stp, catalog p.27 agrees) [user 2026-10-18 A10 Q-TRANSFER-LN yes: -LN parts modelled as the plain part, locknut not modelled]')
    r.other('$PRP@Threads', pr['$PRP@Threads'], f'= stage row {plain}')
    r.notes.append(f'OMi SKU {r.omisku} (one of the six with "no source" on 2026-10-16): A10 now gives it the plain part\'s row; config named like the table\'s other -LN rows (2701-06-06-FG-LN)')
    r.done(axial=f'OMi catalog SKU {r.omisku} dropped by the 2026-09-23 crawl (adapters77 2026-10-16); -LN = the plain {plain} + a locknut (A10 Q-TRANSFER-LN yes 2026-10-18): every size = row {plain} (its own Brennan STEP, batch 15)',
           comment=f'{TODAY} (wave 3 adapters, staged, not shipped): NEW row - OMi sells {r.omisku}; copied from {plain} (A10: -LN modelled as the plain part, no locknut)', dimsource='')

# ============================================================ the two 5406-P plugs: Air-Way alias rows exist (A4 Q-NEW-AWALIAS yes) -> edits, not new rows
hdr, rows = table('5406P')
pairing('5406P', [('L2@DRIVE', 'L LGTH', 'plug length'), ('C2HEX@HEX', 'C HEX', 'hex')], 'TFA-p067', '(TFA p.67 "5406-P EXTERNAL HEX PIPE PLUG"; the alias rows 5406-16P ... -32P are BUILD with OMiSKU 5406-P-16 ...)')
for pn, alias in (('5406-P-08', '5406-08P'), ('5406-P-12', '5406-12P')):
    ar = rows[alias]
    t_, rr = catrow(pn)
    chk, agree = [], True
    for col, cc in (('L2@DRIVE', 'L LGTH'), ('C2HEX@HEX', 'C HEX')):
        bv = float(rr['values'][cc]); av = float(ar[col])
        ok = abs(av - bv) <= 0.0051
        agree &= ok
        chk.append(f'{col} Air-Way {av} vs Brennan {cc} {rr["values"][cc]}: ' + ('equal' if abs(av - bv) < 1e-9 else 'rounding only' if ok else 'DIFFERS (Air-Way kept, s6)'))
    why = f'{TODAY}: OMi sells {pn} (website, two-pass crawl 2026-10-16; the 2026-09-23 crawl had dropped it) and Air-Way row {alias} is the same part (A4 Q-NEW-AWALIAS yes 2026-10-18; as 5406-16P = OMi 5406-P-16)'
    bt = f'Brennan TFA p.67 {t_["table_id"]} row {pn}: ' + '; '.join(chk)
    EDITS.append(dict(table='5406P', config=alias, column='$PRP@ScopeAction', old=ar['$PRP@ScopeAction'], new='BUILD', why=why))
    EDITS.append(dict(table='5406P', config=alias, column='$PRP@OMiSKU', old=ar['$PRP@OMiSKU'] or '', new=pn, why=why))
    if ar['$PRP@PartNo'] != alias:
        EDITS.append(dict(table='5406P', config=alias, column='$PRP@PartNo', old=ar['$PRP@PartNo'], new=alias,
                          why=f'zero-padded part number (CLAUDE.md rule) = the row\'s config name; gen_straight2 SPEC 5406P skips "{ar["$PRP@PartNo"]}" ("part number has no dash", wave3 test first run)'))
    if agree:
        EDITS.append(dict(table='5406P', config=alias, column='$PRP@DataStatus', old=ar['$PRP@DataStatus'], new='VERIFIED', why=bt + ' -> Air-Way and Brennan agree on every cell: VERIFIED (2 independent sources)'))
    EDITS.append(dict(table='5406P', config=alias, column='$COMMENT (append)', old=ar['$COMMENT'] or '', new=f'{TODAY}: BUILD - the DROP above is void: OMi sells {pn} (alias of this Air-Way row, A4) | {bt}', why='note'))
    ROWS.append(dict(table='5406P', config=alias, ready='yes', missing_columns='', gates='', conflicts='' if agree else '; '.join(c for c in chk if 'DIFFERS' in c),
                     notes=f'existing Air-Way alias row of OMi {pn} turned BUILD (edits_5406P_alias.csv), like 5406-16P ... -32P; NOT a new row. DataStatus ' + ('VERIFIED' if agree else 'stays ASSUMED')
                     + '. Note: 5406-P-02 / -04 / -06 were added as separate Brennan rows on 2026-10-18 (b15held) while their alias rows 5406-02P / -04P / -06P stay DROP - with A4 = yes the main session may want one convention'))

# ============================================================ the 3 parts with no review table
hdr6316 = None
for pn in ('6316-08', '6316-12', '6316-16'):
    t_, rr = catrow(pn)
    ROWS.append(dict(table='(no review table)', config=pn, ready='no', missing_columns='whole table', gates='GATE TOOLCHAIN: no 6316 review table, no topology, no generator SPEC', conflicts='',
                     notes=f'Brennan TFA p.13 {t_["table_id"]} "6316 FJS-WELD STRAIGHT" prints it: ' + ', '.join(f'{k} {v}' for k, v in rr['values'].items())
                     + '. Needs: a review table DesignTable_6316.xlsx (columns L / L1 / C HEX nut / C4 HEX body / B DRILL / weld-stub OD) and a gen_straight2 SPEC = female JIC swivel end '
                       '(end_JICSW, as 6402 / 6504) x a NEW butt-weld tube-stub end (no weld end module exists; shape from a Brennan STEP - none on disk: BRENNAN_6316-08 / -12 / -16)'))

# ------------------------------------------------------------------------ write
with open(os.path.join(OUT, 'newrows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'column', 'value', 'source', 'kind']); w.writeheader(); w.writerows(NEW)
with open(os.path.join(OUT, 'edits_5406P_alias.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'column', 'old', 'new', 'why']); w.writeheader(); w.writerows(EDITS)
with open(os.path.join(OUT, 'cells.csv'), 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerow(['table', 'config', 'column', 'value', 'source', 'kind'])
with open(os.path.join(OUT, 'rows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes']); w.writeheader(); w.writerows(ROWS)
open(os.path.join(OUT, 'mapping_evidence.txt'), 'w', encoding='utf-8').write('\n'.join(MAPEV) + '\n')
print(len(NEW), 'newrow cells,', len({(x['table'], x['config']) for x in NEW}), 'new rows;', collections.Counter(x['kind'] for x in NEW))
print(len(EDITS), 'alias edits;', len(ROWS), 'rows;', collections.Counter(r['ready'] for r in ROWS))
for r in ROWS:
    print(f"{r['table']:12} {r['config']:22} ready={r['ready']:3} miss=[{r['missing_columns'][:70]}] gates=[{r['gates'][:90]}] conf=[{r['conflicts'][:120]}]")
