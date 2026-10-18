"""compare test/04_DESIGN_TABLES (cells applied) with the untouched copies in tables/ and with base_root: every changed cell must be a
cells.csv cell, a $COMMENT append, or the apply script's marking ($PRP@DimSource / $PRP@AxialSource) - writes evidence/verify_apply.txt"""
import os, csv, glob, collections
import openpyxl

W3 = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\wave3\orfs'
BASE = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\base_root\04_DESIGN_TABLES'
cells = {(c['table'], c['config'], c['column']): c['value'] for c in csv.DictReader(open(os.path.join(W3, 'cells.csv'), encoding='utf-8'))}
out, bad, cnt = [], [], collections.Counter()


def load(p):
    ws = openpyxl.load_workbook(p, data_only=True).active
    hdr = [c.value for c in ws[2]]
    return hdr, {r[0]: dict(zip(hdr, r)) for r in ws.iter_rows(min_row=3, values_only=True)}


for p in sorted(glob.glob(os.path.join(W3, 'test', '04_DESIGN_TABLES', '*.xlsx'))):
    name = os.path.basename(p)
    t = name[12:-5]
    ref = os.path.join(W3, 'tables', name) if t.startswith('FS') else os.path.join(BASE, name)
    h0, a = load(ref)
    h1, b = load(p)
    if set(a) != set(b):
        bad.append(f'{name}: row set changed')
    for pn in b:
        for col in h1:
            va, vb = a.get(pn, {}).get(col), b[pn].get(col)
            if va == vb or (va in (None, '') and vb in (None, '')):
                continue
            if col in ('$PRP@DimSource', '$PRP@AxialSource', '$COMMENT'):
                cnt[(t.startswith('FS'), col)] += 1
                if col == '$COMMENT' and va and not str(vb).startswith(str(va)):
                    bad.append(f'{name} {pn} $COMMENT not an append')
                continue
            if va not in (None, ''):
                bad.append(f'{name} {pn} {col}: non-empty cell changed {va} -> {vb}')
            elif (t, pn, col) not in cells:
                bad.append(f'{name} {pn} {col}: changed but not in cells.csv ({vb})')
            else:
                cnt[(t.startswith('FS'), 'filled')] += 1
applied = cnt[(True, 'filled')]
out.append(f'FS cells filled: {applied} (cells.csv without $COMMENT: {sum(1 for k in cells if k[2] != "$COMMENT")})')
out.append('marking / notes: ' + ', '.join(f'{"FS" if k[0] else "non-FS"} {k[1]} {n}' for k, n in sorted(cnt.items()) if k[1] != 'filled'))
out.append('non-FS tables: only $PRP@DimSource (apply_brennan.py OMi-answers block, not this wave) changed' if not cnt[(False, 'filled')] else f'non-FS filled cells: {cnt[(False, "filled")]}')
out.append('problems: ' + ('none' if not bad else '\n  ' + '\n  '.join(bad)))
open(os.path.join(W3, 'evidence', 'verify_apply.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
