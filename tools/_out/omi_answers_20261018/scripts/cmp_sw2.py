"""cmp_sw2.py <old_SW2.xlsx> <new_SW2.xlsx>: configurations added / removed, and old configurations whose cells changed."""
import sys, openpyxl


def load(p):
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3)
    hdr = rows[hi]
    out = {}
    for r in rows[hi + 1:]:
        if r[0]:
            out[r[0]] = {str(hdr[j]): r[j] for j in range(1, len(hdr)) if hdr[j] is not None}
    return out


a, b = load(sys.argv[1]), load(sys.argv[2])
print('old', len(a), 'new', len(b))
print('added:', sorted(set(b) - set(a)))
print('removed:', sorted(set(a) - set(b)))
for k in sorted(set(a) & set(b)):
    d = [(h, a[k].get(h), b[k].get(h)) for h in sorted(set(a[k]) | set(b[k])) if a[k].get(h) != b[k].get(h) and not h.startswith('$PRP@Gen')]
    if d:
        print('CHANGED', k, d[:6])
