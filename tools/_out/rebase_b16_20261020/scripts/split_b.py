"""split_b.py (after regen_b16roots.py): split the A -> B differences of the 24 batch-16 roots into
  tools: C = merged batch-17 tools + the SHIPPED tables, compared with A (live tools + shipped tables);
  data : B (merged tools + batch-17 stage) compared with C.
For every A configuration whose SW2 cells change in B, the review-table row must carry a logged batch-17 dimension change (stage/CHANGES.csv
or omi_answers CHANGES.csv; not a text / status column) - otherwise it is reported UNTRACED. Output: split_b.txt"""
import os, csv, json, subprocess, sys, difflib, collections
import openpyxl
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
res = json.load(open(os.path.join(HERE, 'regen_b16roots.json')))
MG = os.path.join(ROOT, 'tools', '_out', 'genfeat_20261018', 'merged', 'tools', 'generators')
GENS = {'tee': ('gen_tee.py', 'GT_OUT'), 'straight': ('gen_straight2.py', 'GS_OUT')}
TEXT = ('$COMMENT', '$PRP@AxialSource', '$PRP@DataStatus', '$PRP@DimSource', '$PRP@OMiSKU', '$PRP@ScopeAction', '$PRP@Threads', '(new row)')
logs = collections.defaultdict(list)
for f in ('tools/_out/omi_answers_20261018/CHANGES.csv', 'tools/_out/brennan_yes_20261018/stage/CHANGES.csv'):
    for r in csv.DictReader(open(os.path.join(ROOT, f), encoding='utf-8')):
        if r['column'] not in TEXT and not r['column'].startswith('$'):
            logs[(r['table'].replace('DesignTable_', '').replace('.xlsx', ''), r['part_number'])].append(f"{r['column']} {r['old']} -> {r['new']}")


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


def cmp(pa, pb):
    ha, a = sw2(pa); hb, b = sw2(pb)
    ch = {pn: [c for c in ha if c and c in hb and not same(a[pn].get(c), b[pn].get(c))] for pn in a if pn in b}
    return {pn: c for pn, c in ch.items() if c}, [p for p in b if p not in a], [p for p in a if p not in b], ha != hb


out = [__doc__]; untraced = 0; tooldiff = 0
for r, x in res.items():
    k = x['kind']; g, var = GENS[k]
    dC = os.path.join(HERE, 'regen', 'C', k); os.makedirs(dC, exist_ok=True)
    subprocess.run([sys.executable, '-I', os.path.join(MG, g), r], env=dict(os.environ, OMI_ROOT=ROOT, **{var: dC}), capture_output=True)
    pA, pB, pC = (os.path.join(HERE, 'regen', s, k) for s in 'ABC')
    chAC, addAC, dropAC, hdrAC = cmp(os.path.join(pA, f'DesignTable_{r}_SW2.xlsx'), os.path.join(pC, f'DesignTable_{r}_SW2.xlsx'))
    mAC = sum(1 for l in difflib.unified_diff(mac(os.path.join(pA, f'Build_{r}_MASTER.bas')), mac(os.path.join(pC, f'Build_{r}_MASTER.bas')), lineterm='', n=0)
              if l[:1] in '+-' and not l.startswith(('+++', '---')))
    tool_same = not chAC and not addAC and not dropAC and not hdrAC and mAC == 0
    tooldiff += not tool_same
    chCB, addCB, dropCB, _ = cmp(os.path.join(pC, f'DesignTable_{r}_SW2.xlsx'), os.path.join(pB, f'DesignTable_{r}_SW2.xlsx'))
    mCB = sum(1 for l in difflib.unified_diff(mac(os.path.join(pC, f'Build_{r}_MASTER.bas')), mac(os.path.join(pB, f'Build_{r}_MASTER.bas')), lineterm='', n=0)
              if l[:1] in '+-' and not l.startswith(('+++', '---')))
    out.append(f"{r:5} tools (A vs C): {'identical' if tool_same else f'DIFFER cfg cells {len(chAC)} +{len(addAC)} -{len(dropAC)} hdr {hdrAC} macro lines {mAC}'}"
               f" | data (C vs B): +{len(addCB)} configs, {len(chCB)} old configs changed, macro lines {mCB}")
    for pn, cols in chCB.items():
        geo = [c for c in cols if not c.startswith('$')]
        if not geo:
            out.append(f'      {pn}: text/status only {cols}'); continue
        L = [l for suf in ('', 'L', 'LL', 'LLL') for l in logs.get((r + suf, pn), [])]      # long variants fold in from <root>L / LL / LLL tables
        if not L:
            untraced += 1
        out.append(f"      {pn}: {len(geo)} geometry cells ({', '.join(geo[:6])}{' ...' if len(geo) > 6 else ''}) <- {'; '.join(L) if L else 'UNTRACED'}")
out.append(f'\ntools differ on {tooldiff} of {len(res)} roots; untraced geometry changes: {untraced}')
open(os.path.join(HERE, 'split_b.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[1:]))
