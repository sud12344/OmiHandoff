"""fetch_orfs.py (2026-10-15): Air-Way ORFS series, two passes each, for the OMi FS (ORFS) parts.

User 2026-10-15: "use airway dimensions, check brennan too". Air-Way's public API parts.air-way.com/api/series/<id> returns a
series' full table as JSON (the web page renders it with JavaScript). Series list = MasterData sheet Series, Category 'ORFS'.

python -I fetch_orfs.py pass1|pass2|compare
  pass1 / pass2: fetch every series -> ../raw/series_<id>_pass<n>.json
  compare: parse both passes -> 07_RAW_EXTRACTS/airway_passes/<code>_p1.txt / _p2.txt (new files only, never overwrites)
           + ../airway_orfs_summary.json (rows, columns, pass agreement per series)"""
import json, os, sys, time, urllib.request
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, 'raw')
PASSES = os.path.join(ROOT, '07_RAW_EXTRACTS', 'airway_passes')


def series_list():
    wb = openpyxl.load_workbook(os.path.join(ROOT, '01_MASTER_DATA', 'OMi_Fitting_Library_MasterData_v1.xlsx'), read_only=True, data_only=True)
    out = []
    for r in list(wb['Series'].iter_rows(values_only=True))[1:]:
        if str(r[3]) == 'ORFS' and r[1]:
            name = str(r[2] or '').strip()
            tok = name.split()[0] if name else ''
            code = tok if tok.startswith('FF') else f'AWs{r[1]}'
            out.append(dict(sid=int(r[1]), code=code, name=name, root=str(r[0]), shape=str(r[4]), url=str(r[5]), sheet_count=r[9]))
    return out


def fetch(sid):
    req = urllib.request.Request(f'https://parts.air-way.com/api/series/{sid}', headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def table(d):
    """columns in Air-Way's own order (SeriesProperties), rows in Air-Way's display order (Sequence); values verbatim"""
    props = d['Series']['SeriesProperties']
    cols = [(str(p['Id']), (p['DisplayName'] or '').strip()) for p in props]
    rows = []
    for part in sorted(d['Series']['Products'], key=lambda p: p.get('Sequence') or 0):
        vals = {k: (v or {}).get('Value') for k, v in (part.get('AssocTableValues') or {}).items()}
        rows.append([part.get('ItemNumber')] + [vals.get(i) for i, _ in cols])
    return ['Part #'] + [c for _, c in cols], rows


def text(head, rows):
    clean = lambda v: '' if v is None else str(v).replace('|', '/').replace('\r', ' ').replace('\n', ' ').strip()
    return '\n'.join(['|'.join(head)] + ['|'.join(clean(v) for v in r) for r in rows]) + '\n'


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(RAW, exist_ok=True)
    S = series_list()
    mode = sys.argv[1]
    if mode in ('pass1', 'pass2'):
        n = mode[-1]
        for s in S:
            p = os.path.join(RAW, f'series_{s["sid"]}_pass{n}.json')
            if os.path.exists(p):
                continue
            try:
                b = fetch(s['sid'])
                open(p, 'wb').write(b)
                print(s['sid'], s['code'], len(b), 'bytes')
            except Exception as ex:
                print(s['sid'], s['code'], 'FAILED', ex)
            time.sleep(1.0)
    elif mode == 'compare':
        summ = []
        for s in S:
            t = []
            for n in ('1', '2'):
                p = os.path.join(RAW, f'series_{s["sid"]}_pass{n}.json')
                t.append(text(*table(json.load(open(p, encoding='utf-8')))) if os.path.exists(p) else None)
            same = t[0] is not None and t[0] == t[1]
            head = t[0].split('\n', 1)[0] if t[0] else ''
            nrows = t[0].count('\n') - 1 if t[0] else 0
            written = []
            if same:
                for n, tx in (('1', t[0]), ('2', t[1])):
                    q = os.path.join(PASSES, f'{s["code"]}_p{n}.txt')
                    if os.path.exists(q):
                        if open(q, encoding='utf-8').read() != tx:
                            written.append(f'{os.path.basename(q)} EXISTS AND DIFFERS - not written')
                        continue
                    open(q, 'w', encoding='utf-8', newline='\n').write(tx)
                    written.append(os.path.basename(q))
            summ.append(dict(s, rows=nrows, columns=head.split('|'), passes_identical=same, written=written))
            print(f'{s["sid"]:>4} {s["code"]:<12} rows {nrows:>3} (sheet {s["sheet_count"]})  passes identical {same}  {head}')
        json.dump(summ, open(os.path.join(HERE, 'airway_orfs_summary.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print(len(summ), 'series;', sum(x['rows'] for x in summ), 'rows;', sum(not x['passes_identical'] for x in summ), 'series with differing passes')
