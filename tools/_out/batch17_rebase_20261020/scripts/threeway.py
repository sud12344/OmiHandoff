"""3-way check of the batch-17 stage review tables against batch 16.
B = review table before batch 16 (git 974c8bd), L = live (batch 16 shipped, d63e1a6), S = batch-17 stage.
Per cell keyed (sheet, row key = column A / row number, header of row 2):
  B16-CARRIED  L != B and S == L     (stage already has the batch-16 value)
  B16-STALE    L != B and S == B     (stage holds the pre-batch-16 value -> must be rebased)
  B16-CONFLICT L != B and S not in {B, L}
  B17          L == B and S != L     (a batch-17 edit on top)
Usage: python -I threeway.py <repo root> <dir with pre-16 copies> <out.txt>"""
import sys, os, collections, openpyxl
ROOT, PRE, OUT = sys.argv[1:4]
LIVE = os.path.join(ROOT, '04_DESIGN_TABLES')
STAGE = os.path.join(ROOT, 'tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES')

def norm(v):
    if v is None or v == '': return None
    if isinstance(v, float) and v == int(v): return int(v)
    return v

def cells(path):
    if not os.path.exists(path): return {}
    wb = openpyxl.load_workbook(path)
    d = {}
    for ws in wb:
        rows = list(ws.iter_rows(values_only=True))
        hdr = rows[1] if len(rows) > 1 else ()
        seen = collections.Counter()
        for i, row in enumerate(rows):
            key = row[0] if (i >= 2 and row and row[0] not in (None, '')) else f'#row{i+1}'
            seen[key] += 1
            if seen[key] > 1: key = f'{key}#{seen[key]}'
            for j, v in enumerate(row):
                h = hdr[j] if (i >= 2 and j < len(hdr) and hdr[j]) else f'#col{j+1}'
                d[(ws.title, key, h)] = norm(v)
    return d

lines, summ = [], []
for fn in sorted(os.listdir(PRE)):
    B, L, S = cells(os.path.join(PRE, fn)), cells(os.path.join(LIVE, fn)), cells(os.path.join(STAGE, fn))
    if not S:
        summ.append(f'{fn}: not in the stage'); continue
    c = collections.Counter()
    for k in sorted(set(B) | set(L) | set(S), key=str):
        b, l, s = B.get(k), L.get(k), S.get(k)
        if l != b:
            tag = 'B16-CARRIED' if s == l else 'B16-STALE' if s == b else 'B16-CONFLICT'
        elif s != l: tag = 'B17'
        else: continue
        c[tag] += 1
        if tag != 'B16-CARRIED':
            lines.append(f'{tag}\t{fn}\t{k[0]}\t{k[1]}\t{k[2]}\tpre16={b!r}\tlive={l!r}\tstage={s!r}'[:400])
    summ.append(f'{fn}: ' + ', '.join(f'{t} {n}' for t, n in sorted(c.items())))
open(OUT, 'w', encoding='utf-8').write('\n'.join(summ) + '\n\n' + '\n'.join(lines) + '\n')
print('\n'.join(summ))
