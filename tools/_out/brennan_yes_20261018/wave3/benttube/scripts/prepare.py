"""prepare.py (wave 3, bent tube, 2026-10-18): cells.csv / rows.csv / mapping_evidence.csv / rb_from_pairs.csv for the 68 bent-tube
rows (brennan_rows.csv group A-newscope). Read-only on every input; writes only into wave3/benttube/.

Letter mappings (catalog drawings Flange p4-p5, TFA p38 - see work/z1704.png, z1803b.png, img_p4_35_x6.png, z6701.png):
  1704 / 1804 (90 deg): L1 = JIC tip -> leg-2 axis (gen_bent M1); L2 = JIC axis -> flange face (gen_bent L1); A/F = end-piece hex (CHEX).
  1703 / 1803 (45 deg): L1 / L2 = horizontal / vertical distance from the JIC tip / JIC axis to the point where the leg-2 axis meets the
                        flange face  ->  gen_bent L1 = L2 * sqrt(2), M1 = L1 - L2 (crossing of the two leg axes).
  6701 / 6701-L       : M = JIC tip -> swivel leg axis (M1); L = JIC axis -> swivel nut face (L1); C1 = end-piece hex (CHEX); C2 = nut hex.
  TUBE O.D. = the JIC end's tube size (same column on the forged -FG rows, which have no tube) - NOT the bent tube's O.D.
"""
import csv, json, math, os, re
import openpyxl

H = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
W = os.path.join(H, r'tools\_out\brennan_yes_20261018\wave3\benttube')
BASE = os.path.join(H, r'tools\_out\brennan_yes_20261018\base_root\04_DESIGN_TABLES')
STAGE = os.path.join(H, r'tools\_out\brennan_yes_20261018\stage\04_DESIGN_TABLES')
CAT = json.load(open(os.path.join(H, r'tools\_out\brennan_catalog_20261001\catalog_verified.json')))
ROWS = [r for r in csv.DictReader(open(os.path.join(H, r'tools\_out\brennan_yes_20261018\brennan_rows.csv'))) if r['group'] == 'A-newscope']
assert len(ROWS) == 68, len(ROWS)

# --- Brennan catalog rows by part number --------------------------------------------------------------------------------------------
BR = {}
for t in CAT['tables']:
    for r in t['rows']:
        BR[re.sub(r'\s+', '', r['pn']).upper()] = (t, r)


def frac(s):
    """printed inch value -> float: '1 11/16', '1-3/8', '.9375', '2', '7/8'"""
    s = str(s).strip().replace('-', ' ')
    tot = 0.0
    for p in s.split():
        if '/' in p:
            a, b = p.split('/'); tot += int(a) / int(b)
        else:
            tot += float(p)
    return round(tot, 4)


# --- Air-Way s115 (1701-61-A-B = OMi 1704-A-B-Tube, scope doc 2026-10-14) ------------------------------------------------------------
AW115 = {}
for ln in open(os.path.join(H, r'tools\_out\airway_20261014\series_115_pass1.txt')).read().splitlines()[1:]:
    f = [x.strip() for x in ln.split('|')]
    a, b = f[0].split('-')[2:4]
    AW115[f'1704-{int(a):02d}-{int(b):02d}-Tube'] = dict(N4=float(f[3]), M3=float(f[4]), C=float(f[5]), D=float(f[6]), O=float(f[7]))
assert open(os.path.join(H, r'tools\_out\airway_20261014\series_115_pass1.txt')).read() == \
    open(os.path.join(H, r'tools\_out\airway_20261014\series_115_pass2.txt')).read()

# --- code 61 head O.D. by flange size: Air-Way s61 via the 1700 review table (base) --------------------------------------------------
ws = openpyxl.load_workbook(os.path.join(BASE, 'DesignTable_1700.xlsx'), data_only=True).worksheets[0]
rr = list(ws.iter_rows(values_only=True)); hh = rr[1]
O61 = {}
for x in rr[2:]:
    d = dict(zip(hh, x))
    m = re.match(r'1700-61-(\d+)-(\d+)$', str(x[0] or ''))
    if m and isinstance(d['O@DRIVE'], (int, float)):
        O61.setdefault(int(m.group(2)), []).append((x[0], d['O@DRIVE']))
# Brennan 3300-61 / 3300-62 braze flange head (Flange p8): A = head O.D., D = head thickness, H = groove O.D. (drawing)
B3300 = {}
for code in ('61', '62'):
    for pn, (t, r) in BR.items():
        if t['series'] == f'3300-{code}':
            fl = int(pn.split('-')[3])
            B3300.setdefault((code, fl), []).append((pn, frac(r['values']['A']), float(r['values']['D']), float(r['values']['H'])))
FLG61 = {8: dict(TH=0.265, GO=0.5), 12: dict(TH=0.265, GO=0.625), 16: dict(TH=0.315, GO=0.78), 20: dict(TH=0.315, GO=0.875),
         24: dict(TH=0.315, GO=1.0575), 32: dict(TH=0.375, GO=1.245)}     # gen_straight2.FLG61_MEAS (measured on Brennan 1700 STEPs)
FLG62_08 = 1.250                                                          # gen_bent.FLG62_MEAS[8]['O'] (Brennan 1800/1824/1804-FG -08 STEPs)
SWIV = {4: (0.5625, 0.35), 5: (0.625, 0.382), 6: (0.6875, 0.38), 8: (0.875, 0.43), 10: (1.0, 0.5), 12: (1.25, 0.57), 16: (1.5, 0.6),
        20: (2.0, 0.64), 24: (2.25, 0.72), 32: (2.875, 0.95)}           # gen_straight2.SWIV_MEAS (AF, NOSETIP_B)


def o61(fl):
    v = O61.get(fl, [])
    vals = sorted({x[1] for x in v})
    return vals, v


cells, rows, ev = [], [], []
CAT_SRC = {'1703': 'Brennan Flange catalog p4 table 1703 (MJ-FLANGE 45 DEG ELBOW CODE 61)', '1704': 'Brennan Flange catalog p5 table 1704 (MJ-FLANGE 90 DEG CODE 61)',
           '1803': 'Brennan Flange catalog p5 table 1803 (MJ-FLANGE 45 DEG CODE 62)', '1804': 'Brennan Flange catalog p6 table 1804 (MJ-FLANGE 90 DEG CODE 62)',
           '6701': 'Brennan TFA catalog p38 table 6701 (MJ-FJS SWEPT 90 DEG ELBOW)', '6701-L': 'Brennan TFA catalog p38 table 6701-L (MJ-FJS SWEPT 90 LONG)'}


def cell(t, c, col, v, src, kind):
    cells.append(dict(table=t, config=c, column=col, value=v, source=src, kind=kind))


for R in ROWS:
    t, pn = R['table'], R['config']
    key = pn.upper().replace('-TUBE', '')
    bt, br = BR[key]
    v = br['values']
    gates = ['Q-SCOPE-TUBE (yes 10-14)', 'Q-BRENNAN-ONLY (yes 10-18)']
    if 'Q-SOP5' in R['other_gates']:
        gates.append('Q-SOP5 (A2 hexless allowed)')
    conflicts, notes, missing = [], [], []
    have = set()
    if t == '6701':
        src = CAT_SRC['6701-L' if '-L-' in pn else '6701']
        M, L, C1, C2 = float(v['M LGTH']), float(v['L LGTH']), float(v['C1 HEX']), float(v['C2 HEX'])
        b = int(pn.replace('-L-', '-').split('-')[2])
        cell(t, pn, 'M1@DRIVE', M, f'{src}: M {v["M LGTH"]} = JIC tip -> swivel-leg axis (drawing)', 'brennan-dim'); have.add('M1')
        cell(t, pn, 'L1@DRIVE', L, f'{src}: L {v["L LGTH"]} = JIC axis -> swivel nut face (drawing)', 'brennan-dim'); have.add('L1')
        cell(t, pn, 'CHEX@HEX', C1, f'{src}: C1 HEX {v["C1 HEX"]} = male JIC end-piece hex', 'brennan-dim'); have.add('CHEX')
        cell(t, pn, 'NUTHEX@NUTHEXSK', C2, f'{src}: C2 HEX {v["C2 HEX"]} = swivel nut hex (= swivel library SWIV_MEAS AF {SWIV[b][0]})', 'brennan-dim'); have.add('NUTHEX')
        assert abs(C2 - SWIV[b][0]) < 0.007, (pn, C2)
        cell(t, pn, 'NOSETIP@SWSK', SWIV[b][1], f'end library (Q-TRANSFER-ENDLIB): gen_straight2 SWIV_MEAS[{b}] NOSETIP_B (female JIC swivel -{b:02d}, Brennan 6500 STEP)', 'endlib'); have.add('NOSETIP')
        ev.append(dict(table=t, config=pn, check='C2 nut hex vs swivel library SWIV_MEAS AF', brennan=C2, other=SWIV[b][0], agree='yes'))
        if pn == '6701-20-20':
            notes.append('as printed M 2.750 < 6701-16-16 M 3.10 while L 3.750 > 3.15 (6701-L-20-20 M 3.500): possible printed M/L swap - check before building')
        need = ['M1', 'L1', 'CHEX', 'HEXL', 'NUTHEX', 'NOSETIP', 'D', 'TUBEOD', 'RB']
    else:
        code = '61' if t.startswith('17') else '62'
        th = 45 if t.endswith('03') else 90
        src = CAT_SRC[t]
        a, b = (int(x) for x in pn.split('-')[1:3])
        L1c, L2c, AF = float(v['L1 (in.)']), float(v['L2 (in.)']), frac(v['A/F (in.)'])
        if th == 90:
            M1, LL = L1c, L2c
            fm = f'{src}: L1 {v["L1 (in.)"]} = JIC tip -> leg-2 axis'
            fl = f'{src}: L2 {v["L2 (in.)"]} = JIC axis -> flange face'
        else:
            M1, LL = round(L1c - L2c, 4), round(L2c * math.sqrt(2), 4)
            fm = f'{src}: L1 {v["L1 (in.)"]} - L2 {v["L2 (in.)"]} (L1 / L2 = horizontal / vertical to the leg-2 axis at the flange face; crossing of the leg axes = L1 - L2 at 45 deg)'
            fl = f'{src}: L2 {v["L2 (in.)"]} x sqrt(2) (crossing -> flange face along leg 2 at 45 deg)'
        aw = AW115.get(pn)
        cell(t, pn, '$PRP@FlangeCode', code, f'OMi part description "Code {code} Flange" + {src.split(" (")[0]} title', 'other')
        if aw:
            # Air-Way first ("use airway sizes"); M3 read as JIC tip -> leg-2 axis (its numbers equal Brennan L1 at 12-12)
            dm, dl = aw['M3'] - M1, aw['N4'] - LL
            ev.append(dict(table=t, config=pn, check='Air-Way s115 M3 vs Brennan L1 (both JIC tip -> leg-2 axis?)', brennan=M1, other=aw['M3'], agree='yes' if abs(dm) <= 0.015 else f'NO ({dm:+.2f})'))
            ev.append(dict(table=t, config=pn, check='Air-Way s115 M3 - O/2 (M3 to the head far edge, as drawn) vs Brennan L1', brennan=M1, other=round(aw['M3'] - aw['O'] / 2, 3), agree='NO'))
            ev.append(dict(table=t, config=pn, check='Air-Way s115 N4 vs Brennan L2 (JIC axis -> flange face)', brennan=LL, other=aw['N4'], agree='yes' if abs(dl) <= 0.015 else f'NO ({dl:+.2f})'))
            ev.append(dict(table=t, config=pn, check='Air-Way s115 C vs Brennan A/F (end-piece hex)', brennan=AF, other=aw['C'], agree='yes' if abs(aw['C'] - AF) <= 0.006 else 'NO'))
            cell(t, pn, 'CHEX@HEX', aw['C'], f'Air-Way s115 1701-61-{a}-{b} C {aw["C"]} (Brennan A/F {v["A/F (in.)"]} agrees)', 'other'); have.add('CHEX')
            cell(t, pn, 'D@BORE', aw['D'], f'Air-Way s115 1701-61-{a}-{b} D {aw["D"]} (bore; Brennan prints none)', 'other'); have.add('D')
            cell(t, pn, 'O@DRIVE', aw['O'], f'Air-Way s115 1701-61-{a}-{b} O {aw["O"]} (head O.D.; = Air-Way s61 / Brennan 3300-61 A for flange -{b:02d})', 'other'); have.add('O')
            if abs(dm) <= 0.015 and abs(dl) <= 0.015:
                cell(t, pn, 'M1@DRIVE', aw['M3'], f'Air-Way s115 1701-61-{a}-{b} M3 {aw["M3"]} read as JIC tip -> leg-2 axis (= {fm}; the Air-Way drawing puts M3 at the head far edge - schematic, the numbers agree with Brennan)', 'other'); have.add('M1')
                cell(t, pn, 'L1@DRIVE', aw['N4'], f'Air-Way s115 1701-61-{a}-{b} N4 {aw["N4"]} = flange face -> JIC axis (= {fl})', 'other'); have.add('L1')
                notes.append('Air-Way + Brennan agree on M1 / L1 / CHEX (2 sources: VERIFIED candidate for those cells)')
            else:
                conflicts.append(f'M1: Air-Way s115 M3 {aw["M3"]} (or {aw["M3"] - aw["O"] / 2:.3f} if M3 ends at the head far edge as drawn) vs Brennan L1 {M1}; '
                                 f'L1: Air-Way N4 {aw["N4"]} vs Brennan L2 {LL} - Air-Way first, but its M3 meaning is unclear and it differs from Brennan by '
                                 f'{dm:+.2f} / {dl:+.2f}: ask (no length cell written)')
        else:
            cell(t, pn, 'M1@DRIVE', M1, fm, 'brennan-dim'); have.add('M1')
            cell(t, pn, 'L1@DRIVE', LL, fl, 'brennan-dim'); have.add('L1')
            cell(t, pn, 'CHEX@HEX', AF, f'{src}: A/F {v["A/F (in.)"]} = male JIC end-piece hex', 'brennan-dim'); have.add('CHEX')
            if code == '61':
                vals, srcs = o61(b)
                if len(vals) == 1:
                    cell(t, pn, 'O@DRIVE', vals[0], f'end library (Q-TRANSFER-ENDLIB): code 61 head O.D. flange -{b:02d} = Air-Way s61 O via DesignTable_1700 ({", ".join(x[0] for x in srcs)}); Brennan 3300-61 A agrees', 'endlib'); have.add('O')
                elif vals:
                    cell(t, pn, 'O@DRIVE', max(vals, key=lambda x: sum(1 for s in srcs if s[1] == x)),
                         f'end library: code 61 head O.D. flange -{b:02d}: Air-Way s61 via DesignTable_1700 {srcs} (rounding-only difference); Brennan 3300-61 A {B3300[("61", b)][0][1]}', 'endlib'); have.add('O')
                    notes.append(f'head O.D. -{b:02d}: Air-Way s61 prints {vals} (rounding only)')
            else:
                if b == 8:
                    cell(t, pn, 'O@DRIVE', FLG62_08, 'end library: gen_bent FLG62_MEAS[8] O 1.250 (code 62 -08 head measured on the Brennan 1800-08-08 / 1824-08 / 1804-08-08-FG STEPs)', 'endlib'); have.add('O')
                elif ('62', b) in B3300:
                    A_ = sorted({x[1] for x in B3300[('62', b)]})
                    assert len(A_) == 1
                    cell(t, pn, 'O@DRIVE', A_[0], f'Brennan Flange catalog p8 3300-62 (braze flange head, code 62) A {A_[0]} = head O.D. flange -{b:02d} ({", ".join(x[0] for x in B3300[("62", b)])})', 'brennan-dim'); have.add('O')
                if b != 8:
                    gates.append(f'STEP: code 62 -{b:02d} flange head (gen_bent FLG62_MEAS has -08 only)')
            if pn in ('1803-20-12-Tube', '1804-20-12-Tube'):
                notes.append(f'A/F printed {v["A/F (in.)"]} (other -20 JIC rows 1 11/16) - kept as printed (A13)')
        need = ['M1', 'L1', 'CHEX', 'HEXL', 'O', 'D', 'TUBEOD', 'RB']
    missing = [k for k in need if k not in have]
    rows.append(dict(table=t, config=pn, ready='no', missing_columns=' / '.join(missing), gates='; '.join(gates),
                     conflicts=' | '.join(conflicts), notes=' | '.join(notes)))

# --- 45 / 90 pair consistency (same dash pair in 1703 + 1704, 1803 + 1804): same JIC leg a, bend radius RB, leg-2 straight b? ------
pairs = []
for s45, s90 in (('1703', '1704'), ('1803', '1804')):
    for pn, (t, r) in BR.items():
        if t['series'] != s45:
            continue
        k90 = s90 + pn[4:]
        if k90 not in BR or BR[k90][0]['series'] != s90:
            continue
        v4, v9 = r['values'], BR[k90][1]['values']
        L1_45, L2_45, L1_90, L2_90 = (float(x) for x in (v4['L1 (in.)'], v4['L2 (in.)'], v9['L1 (in.)'], v9['L2 (in.)']))
        X0 = L1_45 - L2_45; Lg = L2_45 * math.sqrt(2); t22 = math.tan(math.radians(22.5))
        RB = (L1_90 - X0) / (1 - t22)
        b45, b90 = Lg - RB * t22, L2_90 - RB
        pairs.append(dict(pair=f'{pn} / {k90}', L1_45=L1_45, L2_45=L2_45, L1_90=L1_90, L2_90=L2_90, implied_RB=round(RB, 3),
                          leg2_straight_45=round(b45, 3), leg2_straight_90=round(b90, 3), diff=round(b45 - b90, 3)))

os.makedirs(W, exist_ok=True)


def wcsv(name, recs, cols):
    with open(os.path.join(W, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(recs)


wcsv('cells.csv', cells, ['table', 'config', 'column', 'value', 'source', 'kind'])
wcsv('rows.csv', rows, ['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes'])
wcsv('mapping_evidence.csv', ev, ['table', 'config', 'check', 'brennan', 'other', 'agree'])
wcsv('pairs_45_90.csv', pairs, list(pairs[0].keys()))
# code 61 head library vs Brennan 3300-61 (validates reading A / D / H of the 3300 tables)
h61 = []
for fl, m in sorted(FLG61.items()):
    for pn, A, D, Hh in B3300.get(('61', fl), []):
        h61.append(dict(flange=fl, brennan_3300=pn, A=A, D=D, H=Hh, airway_s61_O=o61(fl)[0], FLG61_TH=m['TH'], FLG61_GOx2=round(2 * m['GO'], 4),
                        agree_O='yes' if any(abs(A - x) <= 0.011 for x in o61(fl)[0]) else 'NO', agree_TH='yes' if abs(D - m['TH']) < 0.002 else 'NO',
                        agree_groove='yes' if abs(Hh - 2 * m['GO']) < 0.002 else 'NO'))
wcsv('head_3300_vs_library.csv', h61, list(h61[0].keys()))
print(len(cells), 'cells;', len(rows), 'rows;', len(pairs), 'pairs')
for p in pairs:
    print(p)
for h in h61:
    print(h)


# --- (run after make_test.py + the gen_bent runs) what-if outcome per row into rows.csv notes -------------------------------------
def add_whatif():
    p = os.path.join(W, r'test\out_D\gen_bent_summary_1704T_1703T_6701.json')
    pc = os.path.join(W, r'test\out_C\gen_bent_summary_1704T_1703T_6701.json')
    if not os.path.exists(p):
        return
    res = {}
    for tag, path in (('C', pc), ('D', p)):
        s = json.load(open(path))
        for v in s.values():
            for n in v.get('names', []):
                res.setdefault(n, {})[tag] = 'generates'
            for x in v['blocked']:
                n, why = x.split(': ', 1); res.setdefault(n, {})[tag] = 'BLOCKED: ' + why
            for x in v['skipped']:
                n, why = x.split(': ', 1); res.setdefault(n, {})[tag] = 'skipped: ' + why
    rr = list(csv.DictReader(open(os.path.join(W, 'rows.csv'), encoding='utf-8')))
    for r in rr:
        o = res.get(r['config'], {})
        r['notes'] = ' | '.join(x for x in (r['notes'], f'what-if C (TEST placeholders, gen_bent as is): {o.get("C")}',
                                            f'what-if D (+ code 62 heads from catalog 3300-62): {o.get("D")}') if x)
        r['status'] = 'held' if (r['conflicts'] or 'STEP:' in r['gates']) else 'blocked'
    wcsv('rows.csv', rr, ['table', 'config', 'ready', 'status', 'missing_columns', 'gates', 'conflicts', 'notes'])
    import collections
    print(collections.Counter((r['table'], r['status']) for r in rr))
    print(collections.Counter(r['status'] for r in rr))


add_whatif()
