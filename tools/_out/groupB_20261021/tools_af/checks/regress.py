import openpyxl, os, sys
def load(f):
    rows = list(openpyxl.load_workbook(f, read_only=True).active.iter_rows(values_only=True))
    h = rows[0]; return h, {r[0]: dict(zip(h, r)) for r in rows[1:] if r[0]}
def cmp(old, new, roots, skip_cols=('$COMMENT', '$PRP@AxialSource', '$PRP@Description')):
    for r in roots:
        fo, fn = f'{old}/DesignTable_{r}_SW2.xlsx', f'{new}/DesignTable_{r}_SW2.xlsx'
        if not (os.path.exists(fo) and os.path.exists(fn)): print(r, 'missing', os.path.exists(fo), os.path.exists(fn)); continue
        ho, o = load(fo); hn, n = load(fn)
        newcols = [c for c in hn if c not in ho]; lostcols = [c for c in ho if c not in hn]
        diffs = []
        for pn in o:
            if pn not in n: diffs.append((pn, 'LOST')); continue
            for c in ho:
                if c in skip_cols or c is None or c not in hn: continue
                a, b = o[pn].get(c), n[pn].get(c)
                if a != b and not (isinstance(a, float) and isinstance(b, float) and abs(a - b) < 1e-9): diffs.append((pn, c, a, b))
        print(f'{r:6} configs {len(o)} -> {len(n)}  new cols {newcols}  lost cols {lostcols}  changed cells in old configs: {len(diffs)}', diffs[:4])
if __name__ == '__main__':
    cmp(sys.argv[1], sys.argv[2], sys.argv[3:])
