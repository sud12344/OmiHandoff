"""load.py (2026-10-15): shared loaders for the ORFS Air-Way / Brennan comparison (read-only on all sources).

airway()   -> {code: dict(sid, name, cols, rows=[{pn, values}])}       from 07_RAW_EXTRACTS/airway_passes/<code>_p1.txt (pass 1 == pass 2)
brennan()  -> list of ORFS catalog tables (catalog_verified.json, the 2026-10-01 verified parse)
omi_file() -> {pn: row dict} carbon-steel FS / C / TGT rows of OMi's parts file (WebsitePartsInfo2026.xlsx, sheet Items)
core(pn)   -> part-number key for Air-Way <-> Brennan / OMi matching: FF -> FS, upper case, no spaces, dashes zero-padded"""
import json, os, re
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSES = os.path.join(ROOT, '07_RAW_EXTRACTS', 'airway_passes')
CATALOG = os.path.join(ROOT, 'tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')
OMI = os.path.join(ROOT, '07_RAW_EXTRACTS', 'omi_dimensions', 'WebsitePartsInfo2026.xlsx')


def airway():
    summ = json.load(open(os.path.join(HERE, 'airway_orfs_summary.json'), encoding='utf-8'))
    out = {}
    for s in summ:
        p1 = os.path.join(PASSES, f'{s["code"]}_p1.txt')
        p2 = os.path.join(PASSES, f'{s["code"]}_p2.txt')
        t1, t2 = open(p1, encoding='utf-8').read(), open(p2, encoding='utf-8').read()
        assert t1 == t2, s['code']
        lines = t1.rstrip('\n').split('\n')
        cols = lines[0].split('|')
        rows = []
        for ln in lines[1:]:
            v = ln.split('|')
            rows.append(dict(pn=v[0].strip(), values=dict(zip(cols[1:], v[1:]))))
        out[s['code']] = dict(sid=s['sid'], name=s['name'], url=s['url'], cols=cols[1:], rows=rows)
    return out


def brennan():
    d = json.load(open(CATALOG, encoding='utf-8'))
    return [t for t in d['tables'] if t.get('catalog') == 'ORFS']


def core(pn):
    s = re.sub(r'\s+', '', str(pn or '')).upper()
    if s.startswith('FF'):
        s = 'FS' + s[2:]
    # zero-pad bare dash numbers: FS2404-8-4 -> FS2404-08-04 (series codes such as 0304-C or 6400-L are left alone)
    parts = s.split('-')
    return '-'.join(p.zfill(2) if p.isdigit() and len(p) == 1 else p for p in parts)


def omi_file():
    wb = openpyxl.load_workbook(OMI, read_only=True, data_only=True)
    rows = list(wb['Items'].iter_rows(values_only=True))
    hdr = [str(h) if h is not None else '' for h in rows[0]]
    out = {}
    for i, r in enumerate(rows[1:], start=2):
        pn = str(r[0] or '').strip()
        if re.match(r'^(FS\d|C\d{4}|TGT)', pn):
            out[pn] = dict(zip(hdr, r), _row=i)
    return out
