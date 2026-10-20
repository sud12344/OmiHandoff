"""explain_tables.py: are the batch-17 stage copies of the 12 review tables batch 16 shipped (d63e1a6) = the SHIPPED table + logged batch-17
changes? For every cell where 04_DESIGN_TABLES (shipped) and brennan_yes_20261018/stage differ: the change logs (omi_answers_20261018/CHANGES.csv,
then stage/CHANGES.csv, in order) must start at the shipped value and end at the stage value. Text notes ($COMMENT / $PRP@AxialSource) may
also be the shipped text with more appended. Rows only in the stage need a '(new row)' log line. Read-only."""
import os, csv, collections
import openpyxl
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
R = ['0304', '0306', '1502', '2504', '2505', '2606', '2609', '2611', '6500', '6500L', '6501', '6505']
LOGS = [os.path.join(ROOT, 'tools/_out/omi_answers_20261018/CHANGES.csv'), os.path.join(ROOT, 'tools/_out/brennan_yes_20261018/stage/CHANGES.csv')]
ch = collections.defaultdict(list)
for f in LOGS:
    for r in csv.DictReader(open(f, encoding='utf-8')):
        ch[(r['table'], r['part_number'], r['column'])].append(r)


def load(p):
    ws = openpyxl.load_workbook(p).worksheets[0]
    hdr = [c.value for c in ws[2]]
    return hdr, {r[0]: dict(zip(hdr, r)) for r in ws.iter_rows(min_row=3, values_only=True) if r[0] is not None}


def eq(a, b):
    if a in (None, '') and b in (None, ''):
        return True
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return str(a) == str(b)


tot = bad = 0
for t in R:
    T = f'DesignTable_{t}.xlsx'
    ha, ra = load(os.path.join(ROOT, '04_DESIGN_TABLES', T)); hb, rb = load(os.path.join(ROOT, 'tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES', T))
    n = 0; nb = 0
    for k in [k for k in ra if k not in rb]:
        bad += 1; nb += 1; print('  ROW ONLY IN SHIPPED', t, k)
    for k in rb:
        if k not in ra:
            ok = bool(ch.get((T, k, '(new row)')))
            n += 1; tot += 1
            if not ok:
                bad += 1; nb += 1
            print(f'  {t} {k}: row only in the stage - {"logged new row" if ok else "UNLOGGED"}')
            continue
        for h in hb:
            if not h or eq(ra[k].get(h), rb[k].get(h)):
                continue
            n += 1; tot += 1
            live, st = ra[k].get(h), rb[k].get(h)
            L = ch.get((T, k, h), [])
            ok = bool(L) and eq(L[0]['old'], live) and eq(L[-1]['new'], st)
            if not ok and h in ('$COMMENT', '$PRP@AxialSource') and live and st and str(st).startswith(str(live)):
                ok = True                                     # shipped note + appended text
            if not ok and h in ('$COMMENT', '$PRP@AxialSource') and live and st and L and str(live) in str(L[0]['old']) + str(st):
                ok = str(st).startswith(str(L[0]['old'])[:len(str(live))]) or str(live) in str(st)
            if not ok and h == '$COMMENT' and live in (None, '') and str(st).startswith('A19 (') and any(
                    x['source'].startswith('A19') for (tt, kk, hh), xs in ch.items() if tt == T and kk == k for x in xs):
                ok = True; print(f'  {t} {k} $COMMENT: A19 note on an empty cell (apply_a19.py did not log notes; its dimension cells are logged)')
            if not ok:
                bad += 1; nb += 1
                print(f'  UNEXPLAINED {t} {k} {h}: shipped {str(live)[:80]!r} stage {str(st)[:80]!r} log {[(x["old"][:30], x["new"][:30]) for x in L]}')
    print(f'{t}: {n} differing cells/rows, {nb} unexplained')
print('TOTAL', tot, 'differing,', bad, 'unexplained')
