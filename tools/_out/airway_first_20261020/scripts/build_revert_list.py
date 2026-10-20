"""OMi (Triveni) 2026-10-20: "We will prefer to use Airway over Brennan dimension when Airway has them available" - and, asked whether that
also covers the numbers in OMi's own website parts file (= Brennan's data, evidence 2026-09-26): YES.
-> every review-table cell that holds an OMi-file value where Air-Way prints a different value goes back to Air-Way.

Builds revert_list.csv from
  (1) checks/aw_audit.csv  (audit_vs_airway.py: every BUILD cell vs 07_RAW_EXTRACTS/<root>.csv by column name; kind OMi = the cell's
      source note names OMi / A19 / A20) - target = the Air-Way raw value (verified = raw);
  (2) roots with no Air-Way raw extract in the repo (6401 6405 6408 6500): the logged old value of each OMi change
      ("(table had X)" / "A19...: COL X -> Y") - target = X (verified = log; re-check on the PC against the Air-Way pages);
  (3) 2404 (table 2404_FINAL, raw 2404.csv has no header): D1@DRIVE = col 5 (L).
Excluded: Air-Way garbled / impossible values (kept with the reason), rounding-only differences (<= 0.005), and HOLD: cells whose Air-Way
value the generator cannot build (found by the first regeneration, regen/first_try_cmp.txt) - kept at the current value, user decision."""
import csv, os, re, sys, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
DT = os.path.join(H, '04_DESIGN_TABLES')
out, excl = [], []
HOLD = {}   # 2026-10-20 Q1 answered (user: "use brennans"): the unbuildable Air-Way cells take Brennan's value -> BRENNAN_CELLS
# Air-Way's value cannot be built; Brennan TFA catalog value instead (user 2026-10-20, Q1 "use brennans"); written to brennan_cells.csv
BRENNAN_CELLS = {
    ('6405', '6405-24-16-O', 'L31@DRIVE'): (1.75, 'Brennan TFA catalog p16 table TFA-p016-t01 "MORB-FP STRAIGHT" row 6405-24-16-O col "L LGTH" = 1.75',
                                            'Air-Way L 1.00 < the 1-NPTF pocket depth 1.14: no room for a bore (generator BLOCKED)'),
    ('6504', '6504-24-24', 'D1@BORE'): (1.312, 'Brennan TFA catalog p17 table TFA-p017-t05 "MJ-FJS STRAIGHT" row 6504-24-24 col "B1 DRILL" = 1.312',
                                        'Air-Way bore 1.38 >= the -24 JIC tip dia 1.381 (generator BLOCKED)'),
    ('6565', '6565-10-10', 'C3_1HEX@HEX'): (1.0, 'Brennan TFA catalog p18 table TFA-p018-t04 "FJS-FJS STRAIGHT" row 6565-10-10 col "C1 HEX" = 1.000',
                                            'Air-Way nut hex 0.94 vs the Brennan -10 swivel nut (1.000) the nut shape is measured from (generator: no end data)'),
    ('6565', '6565-10-10', 'C3_2HEX@HEX'): (1.0, 'Brennan TFA catalog p18 table TFA-p018-t04 "FJS-FJS STRAIGHT" row 6565-10-10 col "C2 HEX" = 1.000',
                                            'Air-Way nut hex 0.94 vs the Brennan -10 swivel nut (1.000) the nut shape is measured from (generator: no end data)')}
for r in csv.DictReader(open(os.path.join(A, 'checks', 'aw_audit.csv'))):
    if r['kind'] != 'OMi':
        continue
    if re.search(r'garbled|impossible', r['why']):
        excl.append(dict(r, reason='Air-Way value garbled / impossible (kept)')); continue
    out.append(dict(root=r['root'], cfg=r['cfg'], col=r['col'], current=r['current'], target=r['airway'], verified='raw 07_RAW_EXTRACTS',
                    why=r['why'][:300]))
pat_had = re.compile(r'([A-Za-z0-9_]+@[A-Za-z0-9_]+)[^|;\[]*?OMi[^|;\[]*?=\s*([0-9.]+)[^|;\[]*?\(table had ([0-9.]+)')
pat_arrow = re.compile(r"(A19[^:]*|A19-style[^:]*):\s*([A-Za-z0-9_]+@[A-Za-z0-9_]+)\s+([0-9.]+)\s*->\s*(?:OMi\s*)?([0-9.]+)")
for root in ('6401', '6405', '6408', '6500'):
    ws = openpyxl.load_workbook(os.path.join(DT, f'DesignTable_{root}.xlsx'), read_only=True).worksheets[0]; th = None
    for row in ws.iter_rows(values_only=True):
        if th is None:
            if row and '$PRP@PartNo' in row: th = list(row)
            continue
        if not row or not row[0]: continue
        d = dict(zip(th, row))
        if d.get('$PRP@ScopeAction') != 'BUILD': continue
        t = str(d.get('$PRP@AxialSource') or '') + ' | ' + str(d.get('$COMMENT') or '')
        got = {}
        for m in pat_had.finditer(t): got.setdefault(m.group(1), (float(m.group(2)), float(m.group(3)), m.group(0)))
        for m in pat_arrow.finditer(t): got.setdefault(m.group(2), (float(m.group(4)), float(m.group(3)), m.group(0)))
        for col, (omi, old, txt) in got.items():
            cur = d.get(col)
            if cur is None or abs(float(cur) - omi) > 1e-6 or abs(omi - old) <= 0.005: continue
            out.append(dict(root=root, cfg=str(row[0]), col=col, current=cur, target=old, verified='log (no Air-Way raw extract in the repo)', why=txt[:300]))
def norm(pn): return '-'.join(str(int(x)) if x.isdigit() else x for x in pn.split('-'))
raw = {norm(l.split('|')[0]): l.split('|') for l in open(os.path.join(H, '07_RAW_EXTRACTS', '2404.csv')).read().splitlines() if l.strip()}
ws = openpyxl.load_workbook(os.path.join(DT, 'DesignTable_2404_FINAL.xlsx'), read_only=True).worksheets[0]; th = None
for row in ws.iter_rows(values_only=True):
    if th is None:
        if row and '$PRP@PartNo' in row: th = list(row)
        continue
    if not row or not row[0]: continue
    d = dict(zip(th, row)); a = raw.get(norm(str(row[0])))
    if not a or d.get('$PRP@ScopeAction', 'BUILD') not in ('BUILD', None): continue
    v = d.get('D1@DRIVE')
    if v is not None and abs(float(v) - float(a[4])) > 0.005:
        out.append(dict(root='2404_FINAL', cfg=str(row[0]), col='D1@DRIVE', current=v, target=float(a[4]), verified='raw 07_RAW_EXTRACTS (2404.csv col 5 L)',
                        why=str(d.get('$COMMENT'))[:300]))
keep, bren = [], []
for o in out:
    k = (o['root'], o['cfg'], o['col'])
    if k in HOLD: excl.append(dict(o, reason='HOLD: ' + HOLD[k]))
    elif k in BRENNAN_CELLS:
        v, cite, why = BRENNAN_CELLS[k]
        bren.append(dict(root=o['root'], cfg=o['cfg'], col=o['col'], current=o['current'], airway=o['target'], brennan=v, cite=cite, why_not_airway=why))
    else: keep.append(o)
assert len(bren) == len(BRENNAN_CELLS), bren
out = keep
with open(os.path.join(A, 'brennan_cells.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(bren[0].keys())); w.writeheader(); w.writerows(bren)
f = ['root', 'cfg', 'col', 'current', 'target', 'verified', 'why']
with open(os.path.join(A, 'revert_list.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=f); w.writeheader(); w.writerows(out)
with open(os.path.join(A, 'revert_excluded.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=sorted({k for e in excl for k in e}), restval=''); w.writeheader(); w.writerows(excl)
import collections
print('brennan cells', len(bren), '| revert cells', len(out), 'configs', len({(o['root'], o['cfg']) for o in out}), 'roots', len({o['root'] for o in out}), '| excluded', len(excl))
print(collections.Counter(o['root'] for o in out))
