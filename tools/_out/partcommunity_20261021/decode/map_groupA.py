"""map_groupA.py (2026-10-21): map Brennan record codes to review-table columns for families with NO calibration rows of their own (no built
part of that Brennan family in the table) - the non-FS "group A" families. Rule as before (user 2026-10-21): Brennan values fill EMPTY cells
of not-ready BUILD rows only, marked BRENNAN; Air-Way first.
A (column, code) pair is used when two independent signals agree and nothing contradicts:
  NAME     the code is the column's letters (M7 = M7@DRIVE, C4 = C4HEX@HEX, Y = Y@REF, L = L@DRIVE ...);
  SIBLING  the same column name is MAPPED to the same code in column_map.csv for another (table, family) - a letter convention shared
           across families;
  DONOR    the Air-Way row of the same size in this table (usually the plain part the forged one was near-matched to) agrees with the
           record on >= 60 % of the sizes that have both (2-decimal Air-Way values: rounding tolerance; forged bodies may differ a little,
           so 'agree' = within 0.06 in or 6 %).
  Required: (NAME or SIBLING) and DONOR, or NAME and SIBLING with no donor rows; a DONOR agreement below 30 % rejects the pair.
Writes column_map_A.csv and proposals_A.csv (same columns as proposals.csv)."""
import os, re, csv, json, glob, collections
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
cache = json.load(open(os.path.join(PC, 'cache.json')))
FAMS = ['1501_fg', '2404', '5406_c', '5602_fg', '5604_fg', '6405_o', '6503_fg', '6803_nwo_fg', '6807_nwo_fg', '6810_nwo_fg', '6902_nwo_fg']
NOT_READY = {norm(l) for l in open(J('tools', '_out', 'sources_20261021', 'not_ready_1022.txt')) if l.strip()}
cmap = list(csv.DictReader(open(os.path.join(H, 'column_map.csv'), encoding='utf-8')))
sib = collections.defaultdict(collections.Counter)
for r in cmap:
    if r['status'] == 'MAPPED':
        sib[r['column']][r['code']] += 1


def base(col):
    b = col.split('@')[0]
    return re.sub(r'(HEX|REF)$', '', b) or b


def rec(p):
    for v in (p, p[:-5] if p.endswith('-TUBE') else p):
        a = cache.get(v)
        if a and 'mident' in a:
            fam = re.match(r'\{\$CADENAS_DATA/23d-libs/brennan/([^}]*)\.prj\}', a['mident']).group(1)
            kv = {}
            for k, x in re.findall(r'\{([A-Z0-9_]+)=([^{}]*)\}', a['mident']):
                try:
                    f = float(x)
                except ValueError:
                    continue
                if f > 0 and k not in ('DN', 'FONTSIZE', 'WEIGHT', 'PITCH', 'LINEID', 'GX'):
                    kv[k] = f
            return fam, kv
    return None, None


def close(t, x):
    tol = 0.0055 if abs(round(t, 2) - t) < 1e-9 else 0.0015
    return abs(t - x) <= max(tol, min(0.06, 0.06 * max(abs(t), abs(x))))


dsh = lambda p: tuple(re.findall(r'-(\d\d)(?=-|$)', p))
# geometry kinds each code matched on its family's STEP (decode_families.py) - a DONOR-only pair must fit the column type
geo = {(r['family'], r['code']): r['kinds'] for r in csv.DictReader(open(os.path.join(H, 'family_codes.csv'), encoding='utf-8'))
       if r['status'] in ('DECODED', 'AMBIGUOUS')}


def fits(col, kinds):
    if not kinds:
        return False
    if '@BORE' in col or col.startswith(('THDMAJ', 'D')):
        return 'CYL_D' in kinds
    if 'HEX' in col or col.startswith(('W', 'Y')):
        return 'GAP' in kinds or 'AX_PL' in kinds
    return any(k in kinds for k in ('AX_PL', 'GAP', 'BOX', 'AX_AX'))
paths = [p for p in glob.glob(os.path.join(ROOT, 'tools', '_out', 'airway_first_20261020', 'stage', '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))   # the BASE tables (earlier cells are already filled in the brennancad stage)
         if not p.endswith(('_SW2.xlsx', '_v2.xlsx'))]
out_map, props = [], []
for path in sorted(paths):
    root = os.path.basename(path)[12:-5]
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows[:6]) if r and '$PRP@PartNo' in r), None)
    if hi is None:
        continue
    head = rows[hi]; numcols = [c for c in head[1:] if c and not str(c).startswith('$')]
    data = [dict(zip(head, r)) for r in rows[hi + 1:] if r and r[0]]
    targets = []
    for d in data:
        p = norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo'))
        fam, kv = rec(p)
        if fam and fam.split('/')[-1] in FAMS and p in NOT_READY and str(d.get('$PRP@ScopeAction') or '').upper() == 'BUILD':
            targets.append((p, d, fam, kv))
    if not targets:
        continue
    for fam in sorted({t[2] for t in targets}):
        recs = [(p, kv) for p, d, f, kv in targets if f == fam]
        # donor rows: same size, values present (Air-Way rows incl. the near-match DROP donors)
        donors = collections.defaultdict(list)
        for d in data:
            q = norm(d.get('$PRP@PartNo') or '')
            if 'AIR-WAY' in str(d.get('$PRP@AxialSource') or '').upper():
                donors[dsh(q)].append(d)
        codes = sorted({k for p, kv in recs for k in kv})
        for c in numcols:
            best = None
            cand_donor = []
            for k in codes:
                name = k == base(c); sibling = sib[c][k] > 0 and sib[c][k] == max(sib[c].values())
                agree = both = 0
                for p, kv in recs:
                    if k not in kv:
                        continue
                    for d in donors.get(dsh(p), []):
                        if isnum(d.get(c)):
                            both += 1; agree += close(float(d[c]), kv[k]); break
                frac = agree / both if both else None
                ok = ((name or sibling) and frac is not None and frac >= 0.6) or (name and sibling and both == 0)
                # DONOR alone (2026-10-21): >= 4 sizes, >= 80 %, and the code's measured geometry fits the column type (uniqueness below)
                donor_only = (not ok and both >= 4 and frac >= 0.8 and fits(c, geo.get((fam, k), '')))
                if frac is not None and frac < 0.3:
                    ok = donor_only = False
                if donor_only:
                    cand_donor.append((agree, k, frac, both))
                    continue
                if ok and (best is None or (name, sibling, frac or 0) > (best[1], best[2], best[3] or 0)):
                    best = (k, name, sibling, frac, both)
            if not best and cand_donor:
                cand_donor.sort(reverse=True)
                if len(cand_donor) == 1 or cand_donor[0][0] >= cand_donor[1][0] + 2:      # a clear winner only
                    a_, k_, f_, b_ = cand_donor[0]; best = (k_, False, False, f_, b_)
            if best:
                k, name, sibling, frac, both = best
                ev = ('+'.join(x for x, y in (('name', name), ('sibling', sibling)) if y) or 'geometry') + (f'+donor {frac:.0%} of {both}' if both else '')
                out_map.append(dict(root=root, family=fam, column=c, code=k, evidence=ev))
                for p, d, f, kv in targets:
                    if f == fam and k in kv and not isnum(d.get(c)):
                        props.append(dict(root=root, part=p, column=c, value=kv[k], code=k, evidence=f'group A: {ev}',
                                          row_status=d.get('$PRP@DataStatus') or ''))
for name, rows_ in (('column_map_A.csv', out_map), ('proposals_A.csv', props)):
    with open(os.path.join(H, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0])); w.writeheader(); w.writerows(rows_)
print(len(out_map), 'column mappings;', len(props), 'cells in', len({(r['root'], r['part']) for r in props}), 'parts')
print(collections.Counter(r['root'] for r in props).most_common())
