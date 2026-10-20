"""Batch 17 post-ship check (2026-10-20): with the LIVE tools/ and the LIVE 04_DESIGN_TABLES, regenerate every root into verify/{straight,tee}
and compare with the shipped 03_SCRIPTS macro (date line aside) and 04_DESIGN_TABLES SW2 (cell by cell).
Expected: the 74 shipped roots identical (OK); every other root's SW2 identical (ok) except the held 5404N (its batch-17 table regenerates 22
configurations, the 4-configuration master stays) and the held new roots without shipped files (4503 4603 1703 1700RC 1800: 'no live file');
macros of the roots whose 03_SCRIPTS macros predate the 2026-09-25 generator fixes differ (known: 2408 4404 4604 5404N 1700 5602 2704).
Output: checks/verify_b17.txt"""
import json, os, re, subprocess, sys, openpyxl

B17 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.dirname(os.path.dirname(os.path.dirname(B17)))
sys.path.insert(0, os.path.join(B17, 'scripts'))
SHIPPED = set(open(os.path.join(B17, 'checks', 'ship_plan.txt'), encoding='utf-8').read().split('SHIP ', 1)[1].split('\n', 1)[0].split())
KNOWN_MACRO = set('2408 4404 4604 5404N 1700 5602 2704'.split())
HELD = set('4503 4603 1703 1700RC 1800 5404N'.split())
gens = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}


def roots(g):
    code = open(os.path.join(R, 'tools', 'generators', g), encoding='utf-8').read()
    m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    keys = re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M)
    keys += re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)
    return sorted(set(keys))


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def cells(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return {(r[0], c): x for r in v[1:] if r and r[0] for c, x in zip(h, r)}


out = [__doc__]
bad = 0
for k, (g, var) in gens.items():
    d = os.path.join(B17, 'verify', k); os.makedirs(d, exist_ok=True)
    for r in roots(g):
        env = dict(os.environ, **{var: d}); env.pop('OMI_ROOT', None)
        subprocess.run([sys.executable, '-B', os.path.join(R, 'tools', 'generators', g), r], env=env, capture_output=True)
        m = os.path.join(d, f'Build_{r}_MASTER.bas')
        ml = os.path.join(R, '03_SCRIPTS', f'Build_{r}_MASTER.bas'); tl = os.path.join(R, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')
        if not os.path.exists(m):
            st = 'BAD' if r in SHIPPED else 'ok'
            out.append(f'{r:8} {st}  no macro generated (no buildable row)'); bad += st == 'BAD'; continue
        if not os.path.exists(ml) or not os.path.exists(tl):
            st = 'held' if r in HELD else ('BAD' if r in SHIPPED else 'ok')
            out.append(f'{r:8} {st}  no live file (macro {os.path.exists(ml)}, SW2 {os.path.exists(tl)})'); bad += st == 'BAD'; continue
        mac_same = mac(m) == mac(ml)
        a, b = cells(os.path.join(d, f'DesignTable_{r}_SW2.xlsx')), cells(tl)
        cols = sorted({x[1] for x in set(a) | set(b) if a.get(x) != b.get(x)}, key=str)
        if r in SHIPPED:
            st = 'OK' if mac_same and not cols else 'BAD'
        elif r in HELD:
            st = 'held'
        else:
            st = 'ok' if not cols and (mac_same or r in KNOWN_MACRO) else 'BAD'
        bad += st == 'BAD'
        out.append(f'{r:8} {st:4} {"SHIPPED" if r in SHIPPED else "-":7} macro {"identical" if mac_same else "differs"}; SW2 columns differing {cols[:6]}')
out.append(f'BAD: {bad}')
open(os.path.join(B17, 'checks', 'verify_b17.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(l for l in out[1:] if ' OK ' not in l))
