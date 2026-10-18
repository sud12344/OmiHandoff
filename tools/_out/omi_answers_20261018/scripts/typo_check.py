"""For each 'Possible typos' thread row OMi confirmed, print the thread text our review table carries for that part."""
import os, glob, openpyxl
ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
ws = openpyxl.load_workbook(os.path.join(ROOT, r'07_RAW_EXTRACTS\omi_answers_20261018\zip_a\OMi_missing_sizes_and_typos_2026-10-09.xlsx'))['Possible typos']
want = {}
for r in range(3, ws.max_row + 1):
    pn = ws[f'A{r}'].value
    if pn and not pn.startswith('(') and ws[f'E{r}'].value == 'thread size does not match the part number':
        want[pn] = (ws[f'D{r}'].value, ws[f'F{r}'].value)
print(len(want), 'thread rows')
found = {}
for p in glob.glob(os.path.join(ROOT, '04_DESIGN_TABLES', 'DesignTable_*.xlsx')):
    if p.endswith('_SW2.xlsx'):
        continue
    sh = openpyxl.load_workbook(p, read_only=True).active
    rows = list(sh.iter_rows(values_only=True))
    if len(rows) < 3:
        continue
    hdr = rows[1]
    cols = [i for i, h in enumerate(hdr) if h and ('Thread' in str(h))]
    for row in rows[2:]:
        k = row[0]
        for pn in want:
            if k == pn or (row and any(row[i] == pn for i, h in enumerate(hdr) if h == '$PRP@OMiSKU')):
                found.setdefault(pn, []).append((os.path.basename(p), k, [row[i] for i in cols]))
for pn, (exp, ans) in want.items():
    print(pn, '| expected', exp, '| OMi', ans, '|', found.get(pn, 'NOT IN ANY TABLE'))
