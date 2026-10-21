"""Brennan CAD parameter records (PARTcommunity, tools/_out/partcommunity_20261021/pc_final.csv) of the 68 group-D OMi parts
(1703 / 1704 / 1803 / 1804 -Tube, 6701 / 6701-L) -> data/records.csv (one row per OMi part, one column per record code)."""
import csv, os, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..'))
PC = os.path.join(ROOT, 'tools', '_out', 'partcommunity_20261021', 'pc_final.csv')
import openpyxl
STAGE = os.path.join(ROOT, 'tools', '_out', 'brennancad_20261021', 'stage', '04_DESIGN_TABLES')


def parse(params):
    out, buf = {}, params
    # values may hold quoted lists with commas: split on ';' (no ';' inside values in these records)
    for kv in buf.split(';'):
        if '=' in kv:
            k, v = kv.split('=', 1)
            out[k] = v
    return out


def omi_parts():
    parts = []
    for r in ('1703', '1704', '1803', '1804', '6701'):
        ws = openpyxl.load_workbook(os.path.join(STAGE, f'DesignTable_{r}.xlsx'), data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
        for x in rows[2:]:
            if x[0] and ('TUBE' in str(x[0]).upper() or r == '6701'):
                parts.append((r, x[0]))
    return parts


if __name__ == '__main__':
    pc = {}
    for row in csv.DictReader(open(PC, encoding='utf-8')):
        pc[row['part'].upper()] = row
    parts = omi_parts()
    recs, keys = [], []
    for tbl, pn in parts:
        row = pc.get(pn.upper())
        d = dict(table=tbl, part=pn, match=row['match'] if row else 'not looked up', family=row['family'] if row else '',
                 brennan_pn=row['pn'] if row else '')
        if row and row['match'] in ('exact', 'alias'):
            p = parse(row['params'])
            for k, v in p.items():
                if k not in keys:
                    keys.append(k)
            d.update(p)
        recs.append(d)
    hdr = ['table', 'part', 'match', 'family', 'brennan_pn'] + keys
    with open(os.path.join(H, 'data', 'records.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, hdr); w.writeheader(); w.writerows(recs)
    print(len(recs), 'parts;', sum(1 for r in recs if r['match'] in ('exact', 'alias')), 'with a record')
    for r in recs:
        if r['match'] not in ('exact', 'alias'):
            print('  no record:', r['part'], r['match'])
