"""Batch 16 ship check 2 (2026-10-19). For every regenerated root (regen/, scripts/regen_all.py):
  A. vs LIVE: 03_SCRIPTS macro (line endings + the 'Generated' date line ignored) and 04_DESIGN_TABLES SW2 (cell by cell)
     -> which roots batch 16 changes;
  B. vs the macro + SW2 that was DRY-RUN in SolidWorks (DRY below) -> what ships is exactly what was built.
Output: checks/cmp_ship_out.txt + checks/changed_roots.json."""
import json, os, openpyxl
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = os.path.dirname(HERE); R = os.path.dirname(os.path.dirname(O))
W1 = os.path.join(O, 'wave1_ship_20261009', 'regen')
PN = os.path.join(O, 'puckfix_20261009', 'regen', 'new')
DRY = {r: PN for r in '2504 2505 1502 6500 6501 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802'.split()}
DRY.update({'0304': os.path.join(W1, 'after', 'straight'), '0306': os.path.join(W1, 'after', 'straight'),
            '2606': os.path.join(W1, 'jictees'), '2609': os.path.join(W1, 'jictees'), '2611': os.path.join(W1, 'jictees'),
            '6505': os.path.join(W1, 'leftovers', 'straight'), '5405': None,     # 5405: the live 03_SCRIPTS macro + live SW2
            '2404': os.path.join(O, 'r2404_20261009', 'regen', 'after')})


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def cells(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return {(r[0], c): x for r in v[1:] for c, x in zip(h, r)}, [r[0] for r in v[1:]]


def cmp(dir_a, dir_b, r):
    ma, mb = os.path.join(dir_a, f'Build_{r}_MASTER.bas'), os.path.join(dir_b, f'Build_{r}_MASTER.bas')
    ta, tb = os.path.join(dir_a, f'DesignTable_{r}_SW2.xlsx'), os.path.join(dir_b, f'DesignTable_{r}_SW2.xlsx')
    if not (os.path.exists(ma) and os.path.exists(ta)):
        return None
    if not (os.path.exists(mb) and os.path.exists(tb)):
        return dict(new=True)
    la, lb = mac(ma), mac(mb)
    nl = sum(1 for x, y in zip(la, lb) if x != y) + abs(len(la) - len(lb))
    (ca, ra), (cb, rb) = cells(ta), cells(tb)
    cols = sorted({k[1] for k in set(ca) | set(cb) if ca.get(k) != cb.get(k)}, key=str)
    return dict(lines=nl, cols=cols, added=[x for x in ra if x not in rb], gone=[x for x in rb if x not in ra], n=len(ra))


roots = json.load(open(os.path.join(HERE, 'regen', 'roots.json')))
out, changed = [], {}
for k in ('straight', 'tee'):
    for r in roots[k]:
        d = os.path.join(HERE, 'regen', k)
        live = cmp(d, os.path.join(R, '03_SCRIPTS'), r) if os.path.exists(os.path.join(R, '03_SCRIPTS', f'Build_{r}_MASTER.bas')) else None
        if live is None and os.path.exists(os.path.join(d, f'Build_{r}_MASTER.bas')):
            # live macro in 03_SCRIPTS, live SW2 in 04_DESIGN_TABLES: compare the two places separately
            pass
        # A. vs live: macro in 03_SCRIPTS, SW2 in 04_DESIGN_TABLES
        ma = os.path.join(d, f'Build_{r}_MASTER.bas')
        if not os.path.exists(ma):
            out.append(f'{k:8} {r:7} no macro (0 rows)'); continue
        ml = os.path.join(R, '03_SCRIPTS', f'Build_{r}_MASTER.bas'); tl = os.path.join(R, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')
        if not os.path.exists(ml) or not os.path.exists(tl):
            a = f'NEW (live macro {os.path.exists(ml)}, live SW2 {os.path.exists(tl)})'; ch = True
            ca, ra = cells(os.path.join(d, f'DesignTable_{r}_SW2.xlsx')); a += f', {len(ra)} configurations'
        else:
            la, lb = mac(ma), mac(ml)
            nl = sum(1 for x, y in zip(la, lb) if x != y) + abs(len(la) - len(lb))
            (ca, ra), (cb, rb) = cells(os.path.join(d, f'DesignTable_{r}_SW2.xlsx')), cells(tl)
            cols = sorted({kk[1] for kk in set(ca) | set(cb) if ca.get(kk) != cb.get(kk)}, key=str)
            added = [x for x in ra if x not in rb]; gone = [x for x in rb if x not in ra]
            ch = bool(nl or cols)
            a = f'{len(rb)} -> {len(ra)} configurations; macro lines differ {nl}; SW2 columns differ {len(cols)}' + \
                (f' {cols[:8]}{"..." if len(cols) > 8 else ""}' if cols else '') + (f'; added {added}' if added else '') + (f'; gone {gone}' if gone else '')
        # B. vs dry run
        b = ''
        if ch:
            if r not in DRY:
                b = 'NOT DRY-RUN'
            elif DRY[r] is None:
                b = 'dry run = live 03_SCRIPTS macro + live SW2' + ('' if not (nl or cols) else ' BUT REGEN DIFFERS FROM LIVE')
            else:
                x = cmp(d, DRY[r], r)
                b = 'IDENTICAL to dry-run' if x and not x.get('new') and not x['lines'] and not x['cols'] else f'DIFFERS from dry-run {x}'
            changed[r] = dict(kind=k, live=a, dry=b, dry_dir=DRY.get(r))
        elif r in DRY and DRY[r] is not None:
            b = '(unchanged vs live; was dry-run anyway)'
        out.append(f'{k:8} {r:7} {"CHANGED " if ch else "same    "}{a}  || {b}')
# 5405: the live macro was dry-run (3 configurations in the SW2 never built)
os.makedirs(os.path.join(HERE, 'checks'), exist_ok=True)
open(os.path.join(HERE, 'checks', 'cmp_ship_out.txt'), 'w', encoding='utf-8').write(__doc__ + '\n' + '\n'.join(out) + '\n')
json.dump(changed, open(os.path.join(HERE, 'checks', 'changed_roots.json'), 'w'), indent=1)
print('\n'.join(l for l in out if 'CHANGED' in l or 'DIFFERS' in l or 'NOT DRY' in l))
print(len(changed), 'changed roots')
