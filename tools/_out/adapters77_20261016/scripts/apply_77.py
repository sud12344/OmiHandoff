"""apply_77.py (2026-10-16): apply ../CHANGES.csv (stage_77.py) to the LIVE review tables in 04_DESIGN_TABLES - only when the user
says so (ship step). Default = DRY RUN: prints every change and every guard failure, writes nothing.

    python -I apply_77.py            dry run
    python -I apply_77.py --apply    write: each touched table is first copied to tools/_out/adapters77_20261016/old_files/ AND
                                     _to_delete/superseded_<today>/adapters77/ (the user empties _to_delete), then edited in place

Guards: the row must exist (by its config name in column A) and the cell must still hold the CHANGES.csv 'old' value (rounding-safe for
numbers); otherwise that row is skipped and reported (the table changed since staging - re-run stage_77.py first). Columns are found
by their header. '$COMMENT (append)' appends ' | <text>'. After --apply: regenerate the touched roots (new GS_OUT / GT_OUT folder),
run the checks, dry-run in SolidWorks, as for any batch."""
import csv, datetime, os, shutil, sys, collections
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = '--apply' in sys.argv
TODAY = datetime.date.today().strftime('%Y%m%d')


def same(a, b):
    if a in (None, '') and b in (None, ''):
        return True
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return str(a).strip() == str(b).strip()


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, 'CHANGES.csv'), encoding='utf-8-sig')))
    by = collections.defaultdict(list)
    for r in rows:
        by[r['review table']].append(r)
    bad, done = [], 0
    for tab, chg in sorted(by.items()):
        p = os.path.join(ROOT, '04_DESIGN_TABLES', tab)
        wb = openpyxl.load_workbook(p)
        ws = wb.worksheets[0]
        hi = next(i for i in range(1, 7) if any(isinstance(c.value, str) and ('DataStatus' in c.value or '@' in c.value) for c in ws[i]))
        hdr = {str(c.value): c.column for c in ws[hi] if c.value is not None}
        rowof = {str(ws.cell(r, 1).value).strip(): r for r in range(hi + 1, ws.max_row + 1) if ws.cell(r, 1).value}
        plan = []
        for c in chg:
            r = rowof.get(c['row (config name)'])
            col = c['column'].replace(' (append)', '')
            if r is None or col not in hdr:
                bad.append(f'{tab} {c["row (config name)"]} {col}: row or column not found'); continue
            cell = ws.cell(r, hdr[col])
            if c['column'].endswith('(append)'):
                new = (str(cell.value) + ' | ' if cell.value else '') + c['new']
            else:
                if not same(cell.value, c['old']):
                    bad.append(f'{tab} {c["row (config name)"]} {col}: cell is {cell.value!r}, CHANGES.csv expects {c["old"]!r}'); continue
                new = float(c['new']) if c['new'].replace('.', '', 1).isdigit() else c['new']
            plan.append((cell, new, c))
        for cell, new, c in plan:
            print(f'{"APPLY" if APPLY else "dry  "} {tab:<26} {c["row (config name)"]:<22} {c["column"]:<20} {str(cell.value)[:30]!r} -> {str(new)[:60]!r}')
        if APPLY and plan:
            for d in (os.path.join(HERE, 'old_files'), os.path.join(ROOT, '_to_delete', f'superseded_{TODAY}', 'adapters77')):
                os.makedirs(d, exist_ok=True)
                shutil.copy2(p, os.path.join(d, tab))
            for cell, new, c in plan:
                cell.value = new
            wb.save(p)
            done += len(plan)
    print(f'{"applied" if APPLY else "would apply"} {done if APPLY else sum(1 for _ in rows) - len(bad)} changes; {len(bad)} guard failures')
    for b in bad:
        print('  GUARD', b)


if __name__ == '__main__':
    main()
