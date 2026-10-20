"""detail_cmp.py: per root, control (live tools + live tables) vs b17 (merged tools + batch-17 tables) SW2 tables, split into
dimension cells and $-property cells, and every dimension change traced to the stage's CHANGES.csv / omi_answers CHANGES.csv (same row,
review column = SW2 column). Also: control vs the SHIPPED 04_DESIGN_TABLES SW2 + 03_SCRIPTS macro (must be identical apart from date lines).
Writes checks/detail_cmp.txt and checks/b17_roots.json."""
import os, re, csv, json, glob, collections, openpyxl

H = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
B17 = os.path.join(H, r'tools\_out\batch17_20261019')
REG = os.path.join(B17, 'regen')
os.makedirs(os.path.join(B17, 'checks'), exist_ok=True)
out = open(os.path.join(B17, 'checks', 'detail_cmp.txt'), 'w', encoding='utf-8')


def P(*a):
    print(*a, file=out)


def load(p):
    if not os.path.exists(p):
        return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next((i for i, r in enumerate(rows) if sum(v is not None for v in r) > 3), None)
    if hi is None:
        return {}
    h = rows[hi]
    return {r[0]: {str(h[j]): r[j] for j in range(1, len(h)) if h[j] is not None} for r in rows[hi + 1:] if r and r[0]}


def same(a, b):
    if a in (None, '') and b in (None, ''):
        return True
    try:
        return abs(float(a) - float(b)) < 1e-9
    except (TypeError, ValueError):
        return str(a).strip() == str(b).strip()


def macro_body(p):
    if not os.path.exists(p):
        return None
    t = open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    return [l for l in t.split('\n') if not re.search(r"(Generated|generated) .*20\d\d-\d\d-\d\d|^' *20\d\d-\d\d-\d\d", l)]


logged = collections.defaultdict(set)   # (part_number, column)
for f in (os.path.join(H, r'tools\_out\brennan_yes_20261018\stage\CHANGES.csv'), os.path.join(H, r'tools\_out\omi_answers_20261018\CHANGES.csv')):
    for r in csv.DictReader(open(f, encoding='utf-8-sig')):
        logged[r['part_number'].strip()].add(r['column'].strip())

res = {}
for sub in ('straight', 'tee'):
    for p in sorted(glob.glob(os.path.join(REG, 'b17', sub, 'DesignTable_*_SW2.xlsx')) + glob.glob(os.path.join(REG, 'control', sub, 'DesignTable_*_SW2.xlsx'))):
        r = re.search(r'DesignTable_(.+)_SW2', p).group(1)
        if r in res:
            continue
        a = load(os.path.join(REG, 'control', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        b = load(os.path.join(REG, 'b17', sub, f'DesignTable_{r}_SW2.xlsx')) or {}
        shipped = load(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
        # control vs shipped
        ctl_ok = None
        if shipped is not None and a:
            ctl_ok = set(a) == set(shipped) and all(same(a[k].get(c), shipped[k].get(c)) for k in a for c in set(a[k]) | set(shipped[k]))
        mc = macro_body(os.path.join(REG, 'control', sub, f'Build_{r}_MASTER.bas'))
        ms = macro_body(os.path.join(H, '03_SCRIPTS', f'Build_{r}_MASTER.bas'))
        mb = macro_body(os.path.join(REG, 'b17', sub, f'Build_{r}_MASTER.bas'))
        mac_ctl_ship = None if (mc is None or ms is None) else (mc == ms)
        mac_b17_ctl = None if (mc is None or mb is None) else (mc == mb)
        new = sorted(set(b) - set(a)); lost = sorted(set(a) - set(b))
        dimchg, prpchg, untraced = [], [], []
        for k in sorted(set(a) & set(b)):
            for c in sorted(set(a[k]) | set(b[k])):
                if same(a[k].get(c), b[k].get(c)):
                    continue
                if c.startswith('$'):
                    prpchg.append((k, c))
                else:
                    dimchg.append((k, c, a[k].get(c), b[k].get(c)))
                    if c not in logged.get(k, set()):
                        untraced.append((k, c, a[k].get(c), b[k].get(c)))
        changed = bool(new or lost or dimchg or prpchg or mac_b17_ctl is False)
        res[r] = dict(sub=sub, control=len(a), b17=len(b), new=new, lost=lost, dimchg=len(dimchg), prpchg=len(prpchg),
                      untraced=len(untraced), ctl_vs_shipped_sw2=ctl_ok, ctl_vs_shipped_macro=mac_ctl_ship, macro_changed=(mac_b17_ctl is False),
                      changed=changed, shipped=shipped is not None)
        P(f'== {r} [{sub}] control {len(a)} b17 {len(b)} | ctl=shipped SW2 {ctl_ok} macro {mac_ctl_ship} | b17 macro changed {mac_b17_ctl is False}')
        if new:
            P('   NEW', new)
        if lost:
            P('   LOST', lost)
        for d in dimchg:
            P('   DIM', d, '' if d not in untraced else '  <-- NOT IN ANY CHANGES.csv')
        if prpchg:
            P('   PRP', len(prpchg), 'cells; columns', sorted({c for _, c in prpchg}))
json.dump(res, open(os.path.join(B17, 'checks', 'b17_roots.json'), 'w'), indent=1)
P()
P('roots changed:', sorted(r for r in res if res[r]['changed']))
P('control != shipped SW2:', sorted(r for r in res if res[r]['ctl_vs_shipped_sw2'] is False))
P('control != shipped macro:', sorted(r for r in res if res[r]['ctl_vs_shipped_macro'] is False))
P('untraced dimension changes:', sum(v['untraced'] for v in res.values()))
