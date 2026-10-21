import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import omi_paths as P    # portable paths (2026-09-25)
_WORK = P.COVERAGE_WORK; _os.makedirs(_WORK, exist_ok=True); _HERE = _os.path.dirname(_os.path.abspath(__file__))
import openpyxl, glob, os, re, collections, json
R = P.ROOT
skus = [s.strip() for s in open(f'{R}/07_RAW_EXTRACTS/omi_feed/omi_skus_all.txt') if s.strip()]
assert len(skus) == len(set(skus))
coll_of_root = {}
for line in open(f'{R}/07_RAW_EXTRACTS/cs_roots.txt'):
    parts = line.strip().split('|')
    for r in parts[1:]: coll_of_root[r] = parts[0]
roots = sorted(coll_of_root, key=len, reverse=True)
def root_of(s):
    for r in roots:
        if s == r or s.startswith(r + '-'): return r
    return None
def load(f):
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows[:6]) if any(isinstance(x, str) and ('DataStatus' in x or '@' in x) for x in r if x))
    hdr = [str(x) if x is not None else '' for x in rows[hi]]
    def col(k):
        for i, h in enumerate(hdr):
            if k in h: return i
        return None
    out = []
    for r in rows[hi+1:]:
        if not r or not r[0]: continue
        g = lambda k: (r[col(k)] if col(k) is not None and col(k) < len(r) else None)
        out.append(dict(cfg=str(r[0]).strip(), sku=g('OMiSKU'), part=g('PartNo'), ds=g('DataStatus'), sa=g('ScopeAction'), cm=g('COMMENT') or '', ax=g('AxialSource') or ''))
    return out
masters = {os.path.basename(p)[:-14] for p in glob.glob(f'{R}/11_MASTERS/*_MASTER.SLDPRT')}
macros = {os.path.basename(p)[6:-11] for p in glob.glob(f'{R}/03_SCRIPTS/Build_*_MASTER.bas')}
cover = {}   # sku -> (master, status)
sw2rows = {}
for f in sorted(glob.glob(f'{R}/04_DESIGN_TABLES/DesignTable_*_SW2.xlsx')):
    m = os.path.basename(f)[12:-9]
    rows = load(f); sw2rows[m] = rows
    st = 'BUILT' if m in masters else ('BUILT-WB' if m in ('2404', '6400') else ('MACRO' if m in macros else 'TABLE-ONLY'))
    for x in rows:
        for k in (x['sku'], x['part'], x['cfg']):
            if k and str(k).strip() in skus:
                cover.setdefault(str(k).strip(), (m, st)); break
rev = {}
for f in sorted(glob.glob(f'{R}/04_DESIGN_TABLES/DesignTable_*.xlsx')):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2': continue
    for x in load(f):
        k = str(x['sku']).strip() if x['sku'] else None
        if k: rev.setdefault(k, []).append((t, x))
res = []
for s in skus:
    r = root_of(s); c = coll_of_root.get(r)
    if s in cover:
        m, st = cover[s]; res.append((s, r, c, st, m, '')); continue
    if s in rev:
        t, x = rev[s][0]
        ds = (x['ds'] or '').upper(); sa = x['sa']
        st = 'DATA-NO-MACRO' if (ds.startswith('VERIFIED') or ds.startswith('ASSUMED')) else ('MISSING' if 'MISSING' in ds else 'OTHER:' + ds)
        if sa == 'DROP': st = 'DROPPED?'
        res.append((s, r, c, st, t, (x['cm'] or '')[:160])); continue
    if s.endswith('-KIT') or r in ('1901', '1902', '1927-61', '1927-62'):
        res.append((s, r, c, 'OUT-KIT', '', '')); continue
    res.append((s, r, c, 'UNTABLED', '', ''))
json.dump(res, open(os.path.join(_WORK, 'res.json'), 'w'))
cnt = collections.Counter(x[3] for x in res)
print('TOTAL', len(res), dict(cnt))
bycoll = collections.defaultdict(collections.Counter)
for x in res: bycoll[x[2]][x[3]] += 1
for k, v in bycoll.items(): print(k, sum(v.values()), dict(v))
print('SW2 masters:', len(sw2rows), 'configs total', sum(len(v) for v in sw2rows.values()))
unmatched_cfg = {m: [x['cfg'] for x in rows if not any(k and str(k).strip() in skus for k in (x['sku'], x['part'], x['cfg']))] for m, rows in sw2rows.items()}
for m, v in unmatched_cfg.items():
    if v: print('SW2 configs not in OMi feed:', m, len(v), v[:6])
