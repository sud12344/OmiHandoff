"""Reverted cells to look at: Air-Way values the tables already flagged (as-printed / suspect / unusual) or that move by more than 0.15 in.
-> checks/look_at.csv"""
import csv, os, re, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
A = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
cm = {}
for x in csv.DictReader(open(os.path.join(A, 'revert_list.csv'), encoding='utf-8')):
    t = x['root']
    if t not in cm:
        ws = openpyxl.load_workbook(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{t}.xlsx'), read_only=True).worksheets[0]; th = None; cm[t] = {}
        for r in ws.iter_rows(values_only=True):
            if th is None:
                if r and '$PRP@PartNo' in r: th = list(r)
                continue
            if r and r[0]: d = dict(zip(th, r)); cm[t][str(r[0])] = str(d.get('$COMMENT') or '') + ' | ' + str(d.get('$PRP@AxialSource') or '')
rows = []
for x in csv.DictReader(open(os.path.join(A, 'revert_list.csv'), encoding='utf-8')):
    c = cm[x['root']].get(x['cfg'], '')
    flag = re.findall(r'[^|;]*(?:as-printed|AS-PRINTED|suspect|unusual|misprint|cannot be right)[^|;]*', c)
    d = float(x['target']) - float(x['current'])
    if flag or abs(d) > 0.15:
        rows.append(dict(root=x['root'], cfg=x['cfg'], col=x['col'], now_omi=x['current'], airway=x['target'], delta=round(d, 3),
                         flagged=' / '.join(f.strip()[:160] for f in flag)))
with open(os.path.join(A, 'checks', 'look_at.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), 'cells,', sum(1 for r in rows if r['flagged']), 'already flagged')
for r in rows: print(r['cfg'], r['col'], r['now_omi'], '->', r['airway'], '|', r['flagged'][:110])
