"""Compare the batch-17 stage review tables against the live 04_DESIGN_TABLES (batch-16 state).
Every differing cell, keyed by (sheet, row key = column A or row number, header in row 2), is checked against stage/CHANGES.csv:
  LOGGED   = CHANGES.csv has (table, part, column) with new == stage value  (a batch-17 edit)
  UNLOGGED = differs, no log line -> stage copy may be stale (pre-batch-16) or an untracked edit
Usage: python -I cmp_stage_live.py <repo root> <out.txt>"""
import sys, os, csv, collections, openpyxl
ROOT, OUT = sys.argv[1], sys.argv[2]
LIVE = os.path.join(ROOT, '04_DESIGN_TABLES')
STAGE = os.path.join(ROOT, 'tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES')
log = collections.defaultdict(list)
for lp in (os.path.join(STAGE, '..', 'CHANGES.csv'), os.path.join(ROOT, 'tools/_out/omi_answers_20261018/CHANGES.csv')):
    with open(lp, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            log[(r['table'], r['part_number'], r['column'])].append(r)
PROSE = ('$COMMENT', '$PRP@AxialSource')   # free-text notes: appended by every staging script, not logged cell by cell

def norm(v):
    if v is None or v == '': return None
    if isinstance(v, float) and v == int(v): return int(v)
    return v

def cells(path):
    wb = openpyxl.load_workbook(path, data_only=False)
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
                if i < 2: h = f'#col{j+1}'
                d[(ws.title, key, h)] = norm(v)
    return d

out = []
summary = []
for fn in sorted(os.listdir(STAGE)):
    if not fn.endswith('.xlsx') or fn.endswith('_SW2.xlsx'): continue
    sp, lp = os.path.join(STAGE, fn), os.path.join(LIVE, fn)
    if not os.path.exists(lp):
        summary.append(f'{fn}: NEW in stage (no live table)'); continue
    S, L = cells(sp), cells(lp)
    nlog = nun = 0
    for k in sorted(set(S) | set(L), key=str):
        s, l = S.get(k), L.get(k)
        if s == l: continue
        sheet, part, col = k
        pk = str(part).split('#')[0]
        hits = log.get((fn, pk, col), [])
        if part == '#row2':
            hits = [h for (t, pn, c), hs in log.items() if t == fn and pn == '(header)' for h in hs]
        newrow = log.get((fn, pk, '(new row)')) and not any(kk[1] == part for kk in L if kk[0] == sheet)
        ok = any(norm(_num(h['new'])) == s for h in hits) if False else None
        def match(h):
            nv = h['new']
            try: nvv = float(nv)
            except ValueError: nvv = nv
            return norm(nvv if nv != '' else None) == (float(s) if isinstance(s, (int, float)) else s) or str(nv) == str(s)
        if newrow: nlog += 1; tag = 'LOGGED-NEWROW'
        elif col in PROSE: nlog += 1; tag = 'PROSE'
        elif any(match(h) for h in hits): nlog += 1; tag = 'LOGGED'
        else: nun += 1; tag = 'UNLOGGED'
        if tag == 'UNLOGGED' or '-v' in sys.argv:
            out.append(f'{tag}\t{fn}\t{sheet}\t{part}\t{col}\tlive={l!r}\tstage={s!r}\tlog={[h["new"] for h in hits]}')
    if nlog or nun: summary.append(f'{fn}: {nlog} logged, {nun} UNLOGGED')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary) + '\n\n' + '\n'.join(out) + '\n')
print('\n'.join(summary)); print(len(out), 'detail lines ->', OUT)
