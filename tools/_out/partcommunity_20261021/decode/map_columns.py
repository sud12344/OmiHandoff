"""map_columns.py (2026-10-21): map Brennan CAD record codes to review-table columns, and propose the empty cells they would fill.
User 2026-10-21: Brennan's CAD records may be used as Brennan values, following the rule (Air-Way first, then OMi's file / answers, then
Brennan, marked $PRP@DimSource BRENNAN). So a proposal only ever fills an EMPTY numeric cell of a BUILD row; a filled cell that differs
from the record is reported as a difference, never changed. Nothing is written to 04_DESIGN_TABLES.

Mapping, per review table (04_DESIGN_TABLES/DesignTable_<root>.xlsx; the ORFS stage tables for FS roots):
  every row whose part (OMiSKU, else PartNo) has a Brennan record in ../cache.json is a calibration row; for each numeric column and
  record code, count the rows where both are present and agree within 0.0015 in (or 0.0015 relative x2 for big values).
  A column is MAPPED to a code when it agrees on >= 3 rows and on >= 90 % of the rows that have both. Ties / weaker evidence -> not mapped.
Writes column_map.csv (root, column, code, agree, both, status) and proposals.csv (root, part, column, value, code, row status).
Usage: python -I map_columns.py"""
import os, re, csv, json, glob, collections
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
try:
    cache = json.load(open(os.path.join(PC, 'cache.json')))
except json.JSONDecodeError:            # being rewritten by a running lookup - retry later
    raise SystemExit('cache.json is being written - run again in a moment')


def aliases(p):
    v = [p]
    if p.endswith('-TUBE'): v.append(p[:-5])
    m = re.match(r'^6408-HHP-(\d\d)-O$', p)
    if m: v.append(f'6408-H{m.group(1)}-O')
    if p.startswith('5406-HHP-'): v.append(p.replace('5406-HHP-', '5406-HP-'))
    if p.endswith('-ASY'): v.append(p[:-4])
    return v


def rec(p):
    for v in aliases(p):
        a = cache.get(v)
        if a and 'mident' in a:
            kv = dict(re.findall(r'\{([A-Z0-9_]+)=([^{}]*)\}', a['mident']))
            out = {}
            for k, x in kv.items():
                try:
                    f = float(x)
                except ValueError:
                    continue
                if f > 0 and k not in ('DN', 'FONTSIZE', 'WEIGHT', 'PITCH', 'LINEID', 'GX'):
                    out[k] = f
            return out
    return None


def num(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    return None


def same(table_v, x):
    """table value vs record value: a table value printed to 2 decimals (Air-Way) agrees with Brennan's 3-decimal value when it is the
    rounding of it (rounding-only differences are not changes, user 2026-09-25); otherwise 0.0015 in."""
    tol = 0.0055 if abs(round(table_v, 2) - table_v) < 1e-9 else 0.0015
    return abs(table_v - x) <= tol


def base(col):
    """column name -> its letters: 'C1HEX@HEX' -> 'C1', 'M7@DRIVE' -> 'M7', 'D@BORE' -> 'D'."""
    b = col.split('@')[0]
    return re.sub(r'(HEX|REF)$', '', b) or b

tables = sorted(glob.glob(J('04_DESIGN_TABLES', 'DesignTable_*.xlsx')))
tables = [t for t in tables if not t.endswith(('_SW2.xlsx', '_FINAL.xlsx', '_v2.xlsx'))]
stage_orfs = sorted(glob.glob(J('tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES', 'DesignTable_FS*.xlsx')))
NOT_READY = {norm(l) for l in open(J('tools', '_out', 'sources_20261021', 'not_ready_1022.txt')) if l.strip()}
cmap, props, diffs = [], [], []
for path in tables + stage_orfs:
    root = os.path.basename(path)[12:-5]
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows[:6]) if r and '$PRP@PartNo' in r), None)
    if hi is None:
        continue
    head = rows[hi]
    numcols = [c for c in head[1:] if c and not str(c).startswith('$')]
    data = []
    for r in rows[hi + 1:]:
        if not r or not r[0]:
            continue
        d = dict(zip(head, r)); p = norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or r[0])
        data.append((p, d, rec(p)))
    cal = [(p, d, R) for p, d, R in data if R]
    if not cal:
        continue
    agree = collections.defaultdict(collections.Counter); both = collections.defaultdict(collections.Counter)
    for p, d, R in cal:
        for c in numcols:
            v = num(d.get(c))
            if v is None:
                continue
            for k, x in R.items():
                both[c][k] += 1
                if same(v, x):
                    agree[c][k] += 1
    mapping = {}
    for c in numcols:
        best = sorted(((agree[c][k], k) for k in agree[c]), reverse=True)
        if not best:
            cmap.append(dict(root=root, column=c, code='', agree=0, both=0, status='no code agrees')); continue
        n, k = best[0]
        tied = [x for m, x in best if m == n]
        if len(tied) > 1:                                    # same value on every row: prefer the code named like the column
            named = [x for x in tied if x == base(c)]
            if len(named) == 1:
                k, tied = named[0], named
        b = both[c][k]
        tie = len(tied) > 1
        ok = n >= 3 and n >= 0.9 * b and not tie
        cmap.append(dict(root=root, column=c, code=k, agree=n, both=b,
                         status='MAPPED' if ok else ('tie: ' + ' / '.join(tied) if tie else 'weak')))
        if ok:
            mapping[c] = k
    for p, d, R in data:
        if not R or str(d.get('$PRP@ScopeAction') or '').upper() != 'BUILD':
            continue
        # only the not-ready parts get proposals: built rows leave some columns empty on purpose (the generator's measured libraries)
        fill_ok = p in NOT_READY
        for c, k in mapping.items():
            if k not in R:
                continue
            v = num(d.get(c))
            if v is None:
                if fill_ok:
                    props.append(dict(root=root, part=p, column=c, value=R[k], code=k, evidence=f'{agree[c][k]}/{both[c][k]} rows',
                                      row_status=d.get('$PRP@DataStatus') or ''))
            elif not same(v, R[k]):
                diffs.append(dict(root=root, part=p, column=c, table=v, brennan=R[k], code=k, row_status=d.get('$PRP@DataStatus') or ''))

for name, rows_ in (('column_map.csv', cmap), ('proposals.csv', props), ('differences.csv', diffs)):
    with open(os.path.join(H, name), 'w', newline='', encoding='utf-8') as f:
        if rows_:
            w = csv.DictWriter(f, fieldnames=list(rows_[0])); w.writeheader(); w.writerows(rows_)
mapped = [r for r in cmap if r['status'] == 'MAPPED']
print(f"{len(set(r['root'] for r in cmap))} tables with calibration rows; {len(mapped)} of {len(cmap)} columns mapped; "
      f"{len(props)} empty cells proposed in {len(set((r['root'], r['part']) for r in props))} rows; {len(diffs)} differences with filled cells")
