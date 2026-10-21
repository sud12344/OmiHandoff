"""regen19.py (batch 19): tools_b19 on root19 regenerates every root of gen_straight2 / gen_tee + gen_ring (4000, 0319) into merge/regen/,
compared with the live shipped 03_SCRIPTS macro / 04_DESIGN_TABLES SW2 (generated-date line + line endings ignored) and, for the SW2, cell by
cell keyed on the configuration name: same / CHANGED (old configurations whose row changed, new ones, lost ones) / NEW root / not shipped.
Output merge/regen_cmp.txt + regen_cmp.json"""
import os, sys, json, subprocess
import openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
M = os.path.join(H, 'tools', '_out', 'batch19_20261021', 'merge')
T = os.path.join(M, 'tools_b19'); R = os.path.join(M, 'root19')
OUT = os.path.join(M, 'regen')
env0 = {k: v for k, v in os.environ.items() if k not in ('OMI_REV_EXTRA', 'GR_REV')}
env0['OMI_ROOT'] = R


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()] if os.path.exists(p) else None


def sw2(p):
    if not os.path.exists(p): return None
    rows = [tuple(r) for r in openpyxl.load_workbook(p, data_only=True).worksheets[0].iter_rows(values_only=True)]
    h = rows[0]
    return h, {r[0]: dict(zip(h, r)) for r in rows[1:] if r and r[0]}


def spec_roots(g):
    code = (f"import sys, json, io, contextlib; sys.path[:0] = [{os.path.join(T, 'generators')!r}, {T!r}]\n"
            f"with contextlib.redirect_stdout(io.StringIO()):\n    import {g[:-3]} as m\nprint(json.dumps(list(m.SPEC)))")
    p = subprocess.run([sys.executable, '-I', '-c', code], env=env0, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-1500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


jobs = [(k, g, v, r) for k, g, v in (('straight', 'gen_straight2.py', 'GS_OUT'), ('tee', 'gen_tee.py', 'GT_OUT')) for r in spec_roots(g)]
jobs += [('ring', 'gen_ring.py', 'GR_OUT', '4000'), ('ring', 'gen_ring.py', 'GR_OUT', '0319')]
out, res = [], {}
for kind, g, var, r in jobs:
    d = os.path.join(OUT, kind); os.makedirs(d, exist_ok=True)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(T, 'generators', g), r], env=dict(env0, **{var: d}), capture_output=True, text=True)
    open(os.path.join(d, f'{r}_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    m0, m1 = mac(os.path.join(H, '03_SCRIPTS', f'Build_{r}_MASTER.bas')), mac(os.path.join(d, f'Build_{r}_MASTER.bas'))
    t0, t1 = sw2(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')), sw2(os.path.join(d, f'DesignTable_{r}_SW2.xlsx'))
    if t1 is None and m1 is None:
        res[r] = dict(kind=kind, status='no output', rc=p.returncode); out.append(f'{kind:8} {r:10} no output (rc {p.returncode})'); continue
    if t0 is None and m0 is None:
        res[r] = dict(kind=kind, status='NEW', n=len(t1[1]) if t1 else 0); out.append(f'{kind:8} {r:10} NEW root, {res[r]["n"]} configurations'); continue
    if m0 == m1 and t0 is not None and t1 is not None and t0 == t1:
        res[r] = dict(kind=kind, status='same'); out.append(f'{kind:8} {r:10} same'); continue
    new = sorted(set(t1[1]) - set(t0[1])) if t0 and t1 else []
    lost = sorted(set(t0[1]) - set(t1[1])) if t0 and t1 else []
    chg = {c: sorted(k for k in set(t0[1][c]) | set(t1[1][c]) if t0[1][c].get(k) != t1[1][c].get(k)) for c in set(t0[1]) & set(t1[1])} if t0 and t1 else {}
    chg = {c: v for c, v in chg.items() if v}
    res[r] = dict(kind=kind, status='CHANGED', macro_same=m0 == m1, header_same=(t0[0] == t1[0]) if t0 and t1 else None, new=new, lost=lost, changed=chg)
    out.append(f'{kind:8} {r:10} CHANGED macro {"=" if m0 == m1 else "!="} header {"=" if res[r]["header_same"] else "!="} new {len(new)} lost {len(lost)} '
               f'old-changed {len(chg)} {sorted(chg)[:6]} {sorted({k for v in chg.values() for k in v})[:8]}')
open(os.path.join(M, 'regen_cmp.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(res, open(os.path.join(M, 'regen_cmp.json'), 'w'), indent=1, default=str)
print('\n'.join(l for l in out if not l.endswith(' same')))
