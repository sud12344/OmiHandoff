"""source_lookup.py (2026-10-21, cloud): for every OMi carbon-steel part that is not ready (not in a shipped master and not generated
in the committed staging), list which of the three dimension sources print it. Read-only.

Sources checked (all from the repo; nothing fetched from the web):
- AIR-WAY: the raw extracts 07_RAW_EXTRACTS/<root>.csv (first column), the 2026-10-14 Air-Way parses (tools/_out/airway_20261014,
  O-rings / bent tubes), and the OMi -> Air-Way FF... row map of the ORFS parts (tools/_out/orfs_airway_20261015/compare_orfs.csv).
- BRENNAN catalog: every printed row of the four Brennan PDF catalogs (tools/_out/brennan_catalog_20261001/catalog_verified.json).
- BRENNAN STEP: 09_STEP_FILES/BRENNAN_<pn>.stp already in the repo.
- OMi file: 07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx, rows with at least one dimension cell filled
  (Overall Length, Body Diameter, M 1/2, L 1/2, Hex Flat, Side 1..4 ID, Nut Hex 1/2).
- the review tables (04_DESIGN_TABLES/DesignTable_<root>.xlsx + the ORFS ones): the row's ScopeAction / DataStatus, for context.

Matching: exact part number first; otherwise a "core" key (dash sizes zero-padded, the flange code token 61 dropped, trailing FG / NWO /
O / TUBE tokens dropped). A core-only match is reported as such ("~"), never as an exact one.

Writes sources.csv (one row per not-ready part) and sources_summary.json next to this script.
Usage: python -I source_lookup.py <not_ready.txt>"""
import os, sys, re, csv, glob, json, collections
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
SUFFIX = {'FG', 'NWO', 'O', 'TUBE'}


def aliases(pn):
    """OMi -> supplier numbering differences already used in the library (5406-HHP / 6408-HHP built from Brennan 5406-HP / 6408-H
    STEPs, batch 17) or proposed (0618 / 0619 = Brennan V0318 / V0319, Q-NEW-F3-FLARELESS-ALIAS, open)."""
    out = []
    m = re.match(r'^6408-HHP-(\d\d)-O$', pn)
    if m: out.append(f'6408-H{m.group(1)}-O')
    if pn.startswith('5406-HHP-'): out.append(pn.replace('5406-HHP-', '5406-HP-'))
    if re.match(r'^06(18|19)-', pn): out.append('V03' + pn[2:])
    return out


def core(pn):
    t = [x for x in norm(pn).replace('--', '-').split('-') if x]
    ln = [x for x in t[1:] if x in ('LN', 'L', 'LL', 'LLL')]   # Air-Way writes 2702-12-12-FG-LN, OMi 2702-LN-12-12-FG
    t = [t[0]] + ln[:1] + [x for x in t[1:] if x not in ('LN', 'L', 'LL', 'LLL')]
    if len(t) > 1 and re.match(r'^(FS)?1[78]\d\d$', t[0]) and t[1] in ('61', '62'):
        t.pop(1)
    while len(t) > 1 and t[-1] in SUFFIX:
        t.pop()
    t = [x.zfill(2) if x.isdigit() and len(x) < 2 else x for x in t]
    return '-'.join(t)


class Src:
    def __init__(self, name):
        self.name, self.exact, self.core = name, {}, collections.defaultdict(list)

    def add(self, pn, where):
        pn = norm(pn)
        self.exact.setdefault(pn, where)
        self.core[core(pn)].append(pn)

    def find(self, pn):
        if pn in self.exact:
            return '=' + pn, self.exact[pn]
        for a in aliases(pn):
            if a in self.exact:
                return 'alias ' + a, self.exact[a]
        c = self.core.get(core(pn))
        if c:
            return '~' + c[0], self.exact[c[0]]
        return '', ''


# --- Air-Way
aw = Src('AIR-WAY')
for f in sorted(glob.glob(J('07_RAW_EXTRACTS', '*.csv'))):
    for l in open(f, encoding='utf-8', errors='replace'):
        p = l.split('|')[0].strip()
        if p and p.lower() != 'part' and re.search(r'\d', p):
            aw.add(re.sub(r'\s*X\s*', 'X', p.upper()), os.path.basename(f))
for f in sorted(glob.glob(J('tools', '_out', 'airway_20261014', 'series_*_pass1.txt'))):
    for l in open(f, encoding='utf-8', errors='replace'):
        p = l.split('|')[0].strip()
        if p and not p.lower().startswith('part') and re.search(r'\d', p):
            aw.add(p, 'airway_20261014/' + os.path.basename(f))


def review_rows(paths):
    for f in paths:
        try:
            ws = openpyxl.load_workbook(f, read_only=True, data_only=True).worksheets[0]
        except Exception:
            continue
        rows = list(ws.iter_rows(values_only=True))
        hi = next((i for i, r in enumerate(rows[:6]) if r and '$PRP@PartNo' in r), None)
        if hi is None:
            continue
        h = rows[hi]
        for r in rows[hi + 1:]:
            if not r or not r[0]:
                continue
            yield f, dict(zip(h, r))


orfs_rev = sorted(glob.glob(J('tools', '_out', 'orfs_airway_20261015', 'review_tables', '*.xlsx')))
rev = {}
for f, d in review_rows(sorted(glob.glob(J('04_DESIGN_TABLES', 'DesignTable_*.xlsx'))) + orfs_rev):
    if f.endswith('_SW2.xlsx'):
        continue
    keys = {norm(d.get('$PRP@PartNo') or ''), norm(d.get('$PRP@OMiSKU') or '')} - {''}
    info = dict(table=os.path.basename(f), scope=str(d.get('$PRP@ScopeAction') or ''), status=str(d.get('$PRP@DataStatus') or ''),
                dimsource=str(d.get('$PRP@DimSource') or ''), axial=str(d.get('$PRP@AxialSource') or '')[:300],
                comment=str(d.get('$COMMENT') or '')[:300])
    for k in keys:
        # prefer a BUILD row over a DROP donor row for the same OMi part
        if k not in rev or (rev[k]['scope'] != 'BUILD' and info['scope'] == 'BUILD'):
            rev[k] = info

# ORFS: the 2026-10-15 OMi -> Air-Way comparison names the Air-Way row (FF...) of every OMi FS part that has one
for r in csv.DictReader(open(J('tools', '_out', 'orfs_airway_20261015', 'compare_orfs.csv'), encoding='utf-8-sig')):
    if r['Air-Way row'].strip():
        aw.add(r['OMi part'], 'Air-Way ' + r['Air-Way row'].strip() + ' (orfs_airway_20261015/compare_orfs.csv)')

# --- Brennan catalog + STEPs
br = Src('BRENNAN catalog')
cat = json.load(open(J('tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')))
for t in cat['tables']:
    for r in t['rows']:
        br.add(r['pn'], f"{t['catalog']} p{t.get('printed_page') or t['page']} {t['series']} {t['title']}")
st = Src('BRENNAN STEP')
for f in glob.glob(J('09_STEP_FILES', 'BRENNAN_*.stp')):
    st.add(os.path.basename(f)[8:-4], '09_STEP_FILES')

# --- OMi website file
om = Src('OMi file')
DIMCOLS = ('Overall Length', 'Body Diameter', 'M 1 Size', 'M 2 Size', 'L 1 Size', 'L 2 Size', 'Hex Flat', 'Side 1 ID', 'Side 2 ID',
           'Side 3 ID', 'Side 4 ID', 'Nut Hex 1', 'Nut Hex 2')
ws = openpyxl.load_workbook(J('07_RAW_EXTRACTS', 'omi_dimensions', 'WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)['Items']
rows = list(ws.iter_rows(values_only=True)); h = rows[0]
omi_all = set()
for r in rows[3:]:
    d = dict(zip(h, r))
    if not d.get('Part Number'):
        continue
    pn = norm(d['Part Number']); omi_all.add(pn)
    filled = [c for c in DIMCOLS if d.get(c) not in (None, '') and str(d.get(c)).strip() not in ('', '0', '-')]
    if filled:
        om.add(pn, ', '.join(filled))

# --- per part
nr = [norm(l) for l in open(sys.argv[1]) if l.strip()]
out = []
for p in nr:
    a, aw_w = aw.find(p); b, br_w = br.find(p); s, _ = st.find(p); o, om_w = om.find(p)
    rv = rev.get(p, {})
    hits = (a, b, o, s)
    if p.endswith('-TUBE'):
        cls = 'BENT TUBE'          # the flange head is printed (Brennan 17xx / 18xx); the bend (radius, tube length) is printed nowhere
    elif any(x.startswith('=') for x in hits):
        cls = 'HAS SOURCE'
    elif any(x.startswith('alias') for x in hits):
        cls = 'HAS SOURCE (alias)'
    elif any(hits):
        cls = 'NEAR MATCH ONLY'
    else:
        cls = 'NO SOURCE'
    out.append(dict(part=p, cls=cls, airway=a, airway_where=aw_w, brennan_cat=b, brennan_where=br_w, brennan_step=s, omi_file=o,
                    omi_dims=om_w, omi_listed_in_file='yes' if p in omi_all else 'no', review_table=rv.get('table', ''),
                    scope=rv.get('scope', ''), status=rv.get('status', ''), dimsource=rv.get('dimsource', ''),
                    axial=rv.get('axial', ''), comment=rv.get('comment', '')))
with open(os.path.join(HERE, 'sources.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
summ = collections.OrderedDict(not_ready=len(out), by_class=dict(collections.Counter(r['cls'] for r in out)),
                               airway_exact=sum(r['airway'].startswith('=') for r in out),
                               brennan_catalog_exact=sum(r['brennan_cat'].startswith('=') for r in out),
                               brennan_step_in_repo=sum(bool(r['brennan_step']) for r in out),
                               omi_file_dims_exact=sum(r['omi_file'].startswith('=') for r in out))
json.dump(summ, open(os.path.join(HERE, 'sources_summary.json'), 'w'), indent=1)
print(json.dumps(summ, indent=1))
