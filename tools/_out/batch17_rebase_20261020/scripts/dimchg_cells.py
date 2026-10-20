"""List every SW2 cell that differs between the SHIPPED SW2 (04_DESIGN_TABLES) and the b17 regeneration, for configurations present in
both, and look each up in the stage logs (brennan_yes_20261018/stage/CHANGES.csv + omi_answers_20261018/CHANGES.csv): LOGGED when the
same part + column has a logged new value equal to the b17 value; otherwise UNLOGGED (the review-table cell may be unchanged and the
difference comes from the generator - e.g. a derived column). Usage: python -I dimchg_cells.py <repo> <out.csv>"""
import os, sys, csv, glob, re, collections, openpyxl
REPO, OUTF = sys.argv[1:3]
HERE = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')


def sw2(p):
    if not os.path.exists(p): return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None} for r in rows[hi + 1:] if r and r[0]}


log = collections.defaultdict(list)
for p in ('tools/_out/brennan_yes_20261018/stage/CHANGES.csv', 'tools/_out/omi_answers_20261018/CHANGES.csv'):
    for r in csv.DictReader(open(os.path.join(REPO, p), newline='', encoding='utf-8')):
        log[(r['part_number'], r['column'])].append((r['new'], os.path.basename(os.path.dirname(p)), r['source'][:160]))


def eq(a, b):
    try: return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError): return str(a) == str(b)


rows = []
for p in sorted(glob.glob(os.path.join(HERE, 'regen/b17/*/DesignTable_*_SW2.xlsx'))):
    r = re.match(r'DesignTable_(.+)_SW2', os.path.basename(p)).group(1)
    a = sw2(os.path.join(REPO, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
    if not a: continue
    b = sw2(p)
    for cfg in sorted(set(a) & set(b)):
        for col in sorted(set(a[cfg]) | set(b[cfg])):
            if col.startswith('$'): continue
            va, vb = a[cfg].get(col), b[cfg].get(col)
            if eq(va, vb): continue
            hits = log.get((cfg, col), [])
            ok = [h for h in hits if eq(h[0], vb)]
            rows.append([r, cfg, col, va, vb, 'LOGGED' if ok else 'UNLOGGED', (ok or hits or [('', '', '')])[0][1], (ok or hits or [('', '', '')])[0][2]])
w = csv.writer(open(OUTF, 'w', newline='', encoding='utf-8'))
w.writerow(['root', 'config', 'column', 'shipped', 'b17', 'log', 'logfile', 'source'])
w.writerows(rows)
c = collections.Counter((x[0], x[5]) for x in rows)
for k in sorted(c): print(k, c[k])
