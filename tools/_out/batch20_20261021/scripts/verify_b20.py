"""verify_b20.py (after the batch-20 ship): the LIVE tools on the LIVE tables (no OMI_REV_EXTRA, no GR_REV) regenerate every root of
gen_straight2 / gen_tee + gen_ring 4000 and compare with the shipped 03_SCRIPTS macro (generated-date line and line endings ignored) and
04_DESIGN_TABLES SW2. Expected BAD: none among the 83 batch-20 roots; the pre-2026-09-25 macro roots (2408 4404 4604 1700 5602 2704 and the
other QA #172 ones) and held 5404N differ as before the ship. Output checks/verify_b20.txt"""
import os, sys, json, subprocess, tempfile
import openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
B = os.path.join(H, 'tools', '_out', 'batch20_20261021')
T = os.path.join(H, 'tools')
O = os.path.join(B, 'verify'); os.makedirs(O, exist_ok=True)
env0 = {k: v for k, v in os.environ.items() if k not in ('OMI_REV_EXTRA', 'GR_REV', 'OMI_ROOT')}
shipped = {l.split()[1].split('/')[1][6:-11] for l in open(os.path.join(B, 'checks', 'shipped_files_sha256.txt'), encoding='utf-8')
           if '  03_SCRIPTS/Build_' in l and l.split()[1].endswith('_MASTER.bas')}


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()] if os.path.exists(p) else None


def sw2(p):
    return [tuple(r) for r in openpyxl.load_workbook(p, data_only=True).worksheets[0].iter_rows(values_only=True)] if os.path.exists(p) else None


def spec_roots(g):
    code = (f"import sys, json, io, contextlib; sys.path[:0] = [{os.path.join(T, 'generators')!r}, {T!r}]\n"
            f"with contextlib.redirect_stdout(io.StringIO()):\n    import {g[:-3]} as m\nprint(json.dumps(list(m.SPEC)))")
    p = subprocess.run([sys.executable, '-I', '-c', code], env=env0, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-1500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


out, bad = [], []
jobs = [(k, g, v, r) for k, g, v in (('straight', 'gen_straight2.py', 'GS_OUT'), ('tee', 'gen_tee.py', 'GT_OUT')) for r in spec_roots(g)]
jobs += [('ring', 'gen_ring.py', 'GR_OUT', '4000'), ('ring', 'gen_ring.py', 'GR_OUT', '0319')]
for kind, g, var, r in jobs:
    d = os.path.join(O, kind); os.makedirs(d, exist_ok=True)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(T, 'generators', g), r], env=dict(env0, **{var: d}), capture_output=True, text=True)
    m0, m1 = mac(os.path.join(H, '03_SCRIPTS', f'Build_{r}_MASTER.bas')), mac(os.path.join(d, f'Build_{r}_MASTER.bas'))
    t0, t1 = sw2(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx')), sw2(os.path.join(d, f'DesignTable_{r}_SW2.xlsx'))
    if m0 is None and t0 is None:
        out.append(f'{kind:8} {r:9} not shipped (rc {p.returncode}, generated {m1 is not None})'); continue
    ok = m0 == m1 and t0 == t1
    tag = 'OK ' if ok else ('BAD' if r in shipped else 'old')
    if not ok and r in shipped: bad.append(r)
    out.append(f'{kind:8} {r:9} {tag} macro {"=" if m0 == m1 else "!="} SW2 {"=" if t0 == t1 else "!="}{"  (batch 20)" if r in shipped else ""}')
out.append(f'\nbatch-20 roots: {len(shipped)}, BAD {len(bad)} {bad}; "old" = not shipped in batch 18 and already different before (pre-2026-09-25 macros / held)')
open(os.path.join(B, 'checks', 'verify_b20.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(l for l in out if not l.split()[2:3] == ['OK'] and 'not shipped' not in l))
