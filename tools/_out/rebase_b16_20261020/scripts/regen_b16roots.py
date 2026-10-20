"""regen_b16roots.py (2026-10-20, after batch 16 shipped at d63e1a6): regenerate the 24 roots batch 16 shipped (every elbow root of the
corner-puck fix + the 12 changed review tables 0304 0306 1502 2504 2505 2606 2609 2611 6500 6500L 6501 6505; 6500L folds into 6500)
ONLY from the new state, each root in its own process:
  A = live tools/ + live 04_DESIGN_TABLES (shipped state)   -> must equal the shipped 03_SCRIPTS macro (generated-date line aside) and
                                                              04_DESIGN_TABLES SW2, cell by cell (as ship_20261019/scripts/verify_b16.py)
  B = merged batch-17 tools (genfeat_20261018/merged/tools) + the batch-17 stage (brennan_yes_20261018/stage)
      -> compared with A: configurations added / dropped, changed cells of the A configurations, macro lines.
Output: regen/{A,B}/<kind>/, regen_b16roots.txt + .json"""
import json, os, re, subprocess, sys
import openpyxl
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
SHIPPED = '6505 2404 0304 0306 2606 2609 2611 2501 5500 5502 5504 2503 2504 2505 2701 2702 6500 6501 6503 6502 1501 1502 6802 6801'.split()
STATES = {'A': (os.path.join(ROOT, 'tools', 'generators'), ROOT),
          'B': (os.path.join(ROOT, 'tools', '_out', 'genfeat_20261018', 'merged', 'tools', 'generators'),
                os.path.join(ROOT, 'tools', '_out', 'brennan_yes_20261018', 'stage'))}
GENS = {'tee': ('gen_tee.py', 'GT_OUT'), 'straight': ('gen_straight2.py', 'GS_OUT')}


def spec_roots(path):
    s = open(path, encoding='utf-8').read()
    i = s.index('SPEC = {'); j = s.index('\n}\n', i)
    return set(re.findall(r"^\s*'([0-9A-Z]+)': dict\(", s[i:j], re.M)) | set(re.findall(r"^SPEC\['([0-9A-Z]+)'\] = dict\(", s, re.M))


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def sw2(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return h, {r[0]: dict(zip(h, r)) for r in v[1:] if r[0] is not None}


def same(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) < 1e-9
    return a == b


kind = {}
for k, (g, _) in GENS.items():
    for r in spec_roots(os.path.join(STATES['A'][0], g)):
        kind.setdefault(r, k)
res, out, bad = {}, [__doc__], 0
for r in SHIPPED:
    k = kind[r]; g, var = GENS[k]; res[r] = {'kind': k}
    for s, (gd, root) in STATES.items():
        d = os.path.join(HERE, 'regen', s, k); os.makedirs(d, exist_ok=True)
        env = dict(os.environ, OMI_ROOT=root, **{var: d})
        p = subprocess.run([sys.executable, '-I', os.path.join(gd, g), r], env=env, capture_output=True, text=True)
        res[r][s + '_rc'] = p.returncode
        res[r][s + '_line'] = (p.stdout.strip().splitlines() or [''])[0]
        if p.returncode:
            res[r][s + '_err'] = p.stderr.strip().splitlines()[-1:]
    dA, dB = (os.path.join(HERE, 'regen', s, k) for s in 'AB')
    mA, mB = (os.path.join(x, f'Build_{r}_MASTER.bas') for x in (dA, dB))
    tA, tB = (os.path.join(x, f'DesignTable_{r}_SW2.xlsx') for x in (dA, dB))
    # A vs shipped
    ml, tl = os.path.join(ROOT, '03_SCRIPTS', f'Build_{r}_MASTER.bas'), os.path.join(ROOT, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')
    hA, cA = sw2(tA); hL, cL = sw2(tl)
    a_mac = mac(mA) == mac(ml)
    a_cols = sorted({c for pn in set(cA) | set(cL) for c in set(hA) | set(hL) if not same(cA.get(pn, {}).get(c), cL.get(pn, {}).get(c))}, key=str)
    okA = a_mac and not a_cols
    bad += not okA
    # B vs A
    hB, cB = sw2(tB)
    added = [pn for pn in cB if pn not in cA]; dropped = [pn for pn in cA if pn not in cB]
    newcols = [c for c in hB if c not in hA]; lostcols = [c for c in hA if c not in hB]
    changed = {}
    for pn in cA:
        if pn in cB:
            d = [c for c in hA if c and c in hB and not same(cA[pn].get(c), cB[pn].get(c))]
            if d: changed[pn] = {c: (cA[pn].get(c), cB[pn].get(c)) for c in d}
    la, lb = mac(mA), mac(mB)
    import difflib
    ndiff = sum(1 for l in difflib.unified_diff(la, lb, lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---')))
    res[r].update(A_vs_shipped='identical' if okA else f'DIFFERS macro_same={a_mac} cols={a_cols}', A_configs=len(cA), B_configs=len(cB),
                  added=added, dropped=dropped, newcols=newcols, lostcols=lostcols, changed=changed, macro_lines_changed=ndiff)
    out.append(f"{r:5} {k:8} A vs shipped: {res[r]['A_vs_shipped']:9} | B: {len(cA)} -> {len(cB)} configs, +{len(added)} -{len(dropped)}, "
               f"old configs with changed cells {len(changed)} ({sorted({c for v in changed.values() for c in v})}), new cols {newcols}, "
               f"lost cols {lostcols}, macro lines changed {ndiff}")
    for pn in added: out.append(f'        + {pn}')
    for pn, v in changed.items(): out.append(f'        ~ {pn}: ' + '; '.join(f'{c} {a} -> {b}' for c, a, b in [(c, *ab) for c, ab in v.items()]))
out.append(f'\nA vs shipped: {len(SHIPPED) - bad} of {len(SHIPPED)} identical')
open(os.path.join(HERE, 'regen_b16roots.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(res, open(os.path.join(HERE, 'regen_b16roots.json'), 'w'), indent=1, default=str)
print('\n'.join(out[1:]))
