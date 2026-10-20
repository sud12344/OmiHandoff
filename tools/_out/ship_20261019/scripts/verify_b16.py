"""Batch 16 post-ship check (2026-10-19): with the LIVE tools/ and the LIVE 04_DESIGN_TABLES review tables, regenerate every root
into verify/{straight,tee} and compare with the shipped 03_SCRIPTS macro (date line aside) and 04_DESIGN_TABLES SW2 (cell by cell).
Expected: the 24 shipped roots identical; every root's SW2 identical to the live one except the 5 cosmetic $COMMENT roots
(0318 5406 2650 2605 5600: a leading ' | '); macros of the pre-2026-09-25 03_SCRIPTS roots differ (known). Output: checks/verify_b16.txt"""
import json, os, subprocess, sys, openpyxl
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHIPPED = '6505 2404 0304 0306 2606 2609 2611 2501 5500 5502 5504 2503 2504 2505 2701 2702 6500 6501 6503 6502 1501 1502 6802 6801'.split()
roots = json.load(open(os.path.join(HERE, 'regen', 'roots.json')))
gens = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def cells(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return {(r[0], c): x for r in v[1:] for c, x in zip(h, r)}


out = [__doc__]
bad = 0
for k, (g, var) in gens.items():
    d = os.path.join(HERE, 'verify', k); os.makedirs(d, exist_ok=True)
    for r in roots[k]:
        env = dict(os.environ, **{var: d}); env.pop('OMI_ROOT', None)
        subprocess.run([sys.executable, os.path.join(R, 'tools', 'generators', g), r], env=env, capture_output=True)
        m = os.path.join(d, f'Build_{r}_MASTER.bas')
        if not os.path.exists(m):
            out.append(f'{r:7} no macro'); continue
        ml = os.path.join(R, '03_SCRIPTS', f'Build_{r}_MASTER.bas'); tl = os.path.join(R, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')
        mac_same = os.path.exists(ml) and mac(m) == mac(ml)
        a, b = cells(os.path.join(d, f'DesignTable_{r}_SW2.xlsx')), cells(tl) if os.path.exists(tl) else {}
        cols = sorted({x[1] for x in set(a) | set(b) if a.get(x) != b.get(x)}, key=str)
        if r in SHIPPED:
            st = 'OK' if mac_same and not cols else 'BAD'
        else:
            st = 'ok' if not cols or (r in ('0318', '5406', '2650', '2605', '5600') and cols == ['$COMMENT']) else 'BAD'
        bad += st == 'BAD'
        out.append(f'{r:7} {"SHIPPED" if r in SHIPPED else "-      "} {st:3} macro {"identical" if mac_same else "differs"}; SW2 columns differing {cols}')
out.append(f'\n{bad} BAD')
open(os.path.join(HERE, 'checks', 'verify_b16.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(l for l in out[1:] if 'SHIPPED' in l or 'BAD' in l))
