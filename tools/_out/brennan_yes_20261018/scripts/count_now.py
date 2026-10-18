"""count_now.py: configurations now - in the live SW2 tables (= what the shipped macros build) vs BUILD rows with data in the
live review tables, the batch-16 staging (base_root minus OMi answers is not separable, so: wave1_ship scratch_root) and the stage."""
import os, glob, openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'


def sw2_count(folder):
    n = 0
    for p in glob.glob(os.path.join(folder, 'DesignTable_*_SW2.xlsx')):
        ws = openpyxl.load_workbook(p, read_only=True).active
        rows = list(ws.iter_rows(values_only=True))
        hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
        if hi is not None:
            n += sum(1 for r in rows[hi + 1:] if r and r[0])
    return n


def review_count(folder):
    c = {'BUILD rows': 0, 'with data (ASSUMED/VERIFIED)': 0, 'VERIFIED': 0, 'MISSING': 0, 'BRENNAN-marked with data': 0}
    for p in glob.glob(os.path.join(folder, 'DesignTable_*.xlsx')):
        if p.endswith('_SW2.xlsx') or '_FINAL' in p:
            continue
        ws = openpyxl.load_workbook(p, read_only=True).active
        rows = list(ws.iter_rows(values_only=True))
        if len(rows) < 3:
            continue
        hdr = {h: i for i, h in enumerate(rows[1]) if h}
        if '$PRP@ScopeAction' not in hdr or '$PRP@DataStatus' not in hdr:
            continue
        for r in rows[2:]:
            if not r or not r[0] or r[hdr['$PRP@ScopeAction']] != 'BUILD':
                continue
            st = str(r[hdr['$PRP@DataStatus']] or '')
            c['BUILD rows'] += 1
            if st.startswith(('ASSUMED', 'VERIFIED')):
                c['with data (ASSUMED/VERIFIED)'] += 1
                if '$PRP@DimSource' in hdr and r[hdr['$PRP@DimSource']] == 'BRENNAN':
                    c['BRENNAN-marked with data'] += 1
            if st.startswith('VERIFIED'):
                c['VERIFIED'] += 1
            if st == 'MISSING':
                c['MISSING'] += 1
    return c


print('live SW2 configurations (shipped macros):', sw2_count(os.path.join(ROOT, '04_DESIGN_TABLES')))
for name, f in (('live review tables', os.path.join(ROOT, '04_DESIGN_TABLES')),
                ('batch-16 staging', os.path.join(ROOT, r'tools\_out\wave1_ship_20261009\scratch_root\04_DESIGN_TABLES')),
                ('stage (batch 16 + today)', os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\stage\04_DESIGN_TABLES'))):
    print(name, review_count(f))
