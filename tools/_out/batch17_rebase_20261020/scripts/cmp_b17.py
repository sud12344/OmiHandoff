"""Batch 17 rebase compare (2026-10-20). For every root:
 (1) live-regen vs SHIPPED (03_SCRIPTS macro, 04_DESIGN_TABLES SW2): proves the cloud run of the live tools = batch 16 as shipped
 (2) b17-regen vs SHIPPED SW2, per configuration: new / lost / changed configurations (values incl. $ columns)
 (3) b17 macro vs live-regen macro: number of changed lines (date line and line endings ignored)
Usage: python -I cmp_b17.py <repo root> <out.txt>"""
import os, sys, re, glob, openpyxl, difflib
REPO, OUTF = os.path.abspath(sys.argv[1]), sys.argv[2]
HERE = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')


def sw2(p):
    if not os.path.exists(p): return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
    if hi is None: return {}
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None} for r in rows[hi + 1:] if r and r[0]}


DATE = re.compile(r"(generated|GENERATED|Generated)[^\n]*\d{4}-\d{2}-\d{2}[^\n]*")
def bas(p):
    if not os.path.exists(p): return None
    t = open(p, encoding='latin-1').read().replace('\r\n', '\n')
    return [DATE.sub('<date>', l) for l in t.split('\n')]


def dims(c):  # numeric/driving columns only
    return {k: v for k, v in c.items() if not k.startswith('$')}


lines, tot = [], dict(ship=0, b17=0, new=0, lost=0, chg_dim=0, chg_prp=0)
roots = sorted({(os.path.basename(os.path.dirname(p)), re.match(r'DesignTable_(.+)_SW2', os.path.basename(p)).group(1))
                for p in glob.glob(os.path.join(HERE, 'regen/*/*/DesignTable_*_SW2.xlsx'))}, key=lambda x: x[1])
for sub, r in roots:
    ship_s = sw2(os.path.join(REPO, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
    ship_b = bas(os.path.join(REPO, '03_SCRIPTS', f'Build_{r}_MASTER.bas'))
    live_s = sw2(os.path.join(HERE, 'regen/live', sub, f'DesignTable_{r}_SW2.xlsx'))
    live_b = bas(os.path.join(HERE, 'regen/live', sub, f'Build_{r}_MASTER.bas'))
    b_s = sw2(os.path.join(HERE, 'regen/b17', sub, f'DesignTable_{r}_SW2.xlsx'))
    b_b = bas(os.path.join(HERE, 'regen/b17', sub, f'Build_{r}_MASTER.bas'))
    f1 = ('SW2=' + ('same' if live_s == ship_s else 'DIFF' if ship_s is not None and live_s is not None else f'ship:{ship_s is not None} live:{live_s is not None}'))
    if ship_b is not None and live_b is not None:
        n = sum(1 for d in difflib.unified_diff(ship_b, live_b, n=0, lineterm='') if d[:1] in '+-' and d[:3] not in ('+++', '---'))
        f1 += f' bas={"same" if n == 0 else f"{n} lines"}'
    else: f1 += f' bas ship:{ship_b is not None}'
    ref = ship_s if ship_s is not None else {}
    b = b_s or {}
    new = sorted(set(b) - set(ref)); lost = sorted(set(ref) - set(b))
    cd = sorted(k for k in set(b) & set(ref) if dims(b[k]) != dims(ref[k]))
    cp = sorted(k for k in set(b) & set(ref) if dims(b[k]) == dims(ref[k]) and b[k] != ref[k])
    nb = (sum(1 for d in difflib.unified_diff(live_b, b_b, n=0, lineterm='') if d[:1] in '+-' and d[:3] not in ('+++', '---'))
          if live_b is not None and b_b is not None else None)
    tot['ship'] += len(ref); tot['b17'] += len(b); tot['new'] += len(new); tot['lost'] += len(lost); tot['chg_dim'] += len(cd); tot['chg_prp'] += len(cp)
    lines.append(f'{r:8s} [{sub:8s}] (1) {f1:28s} | (2) shipped {len(ref):3d} b17 {len(b):3d} new {len(new):3d} lost {len(lost)} '
                 f'dimchg {len(cd)} prpchg {len(cp)} | (3) macro lines vs live-regen {nb}'
                 + (f'\n           lost {lost}' if lost else '') + (f'\n           dimchg {cd}' if cd else '')
                 + (f'\n           new {new}' if new else ''))
s = '\n'.join(lines) + f'\nTOTAL {tot}\n'
open(OUTF, 'w').write(s); print(s[-3000:])
