"""prep_b18.py (2026-10-20): batch-18 candidate = the ORFS staging toolset (tools/_out/orfs_gen_20261020/tools, SolidWorks dry runs: all
51 masters PASS) + the Air-Way-first 6410 reference line (tools_af) on ONE set of inputs:
  root18/04_DESIGN_TABLES = the Air-Way-first stage (a full copy of the live tables + 26 edited review tables)
                            + DesignTable_1603.xlsx from brennan_yes_20261018/stage (A14, 1603-08-08-08-FG) when it differs from live only there
  OMI_REV_EXTRA           = brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES (the 51 FS review tables)
Every root of both generators is regenerated with tools_b18 and compared with the file that was tested or shipped:
  Air-Way-first roots -> airway_first_20261020/regen/stage (the files of the running SolidWorks dry runs)
  FS roots            -> orfs_gen_20261020/out (+ out/tee) (the dry-run-tested ORFS files)
  1603                -> shipped files; only the A14 row may differ
  every other root    -> the shipped 03_SCRIPTS macro + 04_DESIGN_TABLES SW2
Writes tools_b18/, root18/, regen/, cmp.txt. Read-only for everything outside tools/_out/batch18_20261020."""
import os, re, sys, shutil, subprocess, json
import openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
B = os.path.join(H, 'tools', '_out', 'batch18_20261020')
ORFS = os.path.join(H, 'tools', '_out', 'orfs_gen_20261020')
AF = os.path.join(H, 'tools', '_out', 'airway_first_20261020')
EXTRA = os.path.join(H, 'tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')
A14 = os.path.join(H, 'tools', '_out', 'brennan_yes_20261018', 'stage', '04_DESIGN_TABLES', 'DesignTable_1603.xlsx')
T = os.path.join(B, 'tools_b18'); R = os.path.join(B, 'root18')
log = []
def say(s): print(s, flush=True); log.append(s)

# 1. toolset (KEEP_TOOLS=1: use tools_b18 as it is - it carries the 2026-10-20 held-root fixes; a fresh copy would drop them)
if os.environ.get('KEEP_TOOLS') == '1':
    say('tools_b18 kept as it is (held-root fixes: FlatsCut second diagonal + H/V, HexArmV direction fallback)')
else:
    if os.path.exists(T): shutil.rmtree(T)
    shutil.copytree(os.path.join(ORFS, 'tools'), T, ignore=shutil.ignore_patterns('_out', '__pycache__', '*.orig'))
    p = os.path.join(T, 'generators', 'gen_straight2.py')
    s = open(p, encoding='utf-8', newline='').read()
    old = "ref='6410-12-08-O', thrchk=(('A', 'THDMAJ_B1@DRIVE', 'a'),),"
    assert s.count(old) == 1, 'the 6410 line is not unique'
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, old.replace('6410-12-08-O', '6410-24-20-O')))
    say('tools_b18 = orfs staging tools + 6410 ref 6410-24-20-O')


# 2. inputs
def rows(path):
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    return [tuple(r) for r in ws.iter_rows(values_only=True)]
if os.path.exists(R): shutil.rmtree(R, ignore_errors=True)      # OneDrive may keep the empty folder locked: reused below
shutil.copytree(os.path.join(AF, 'stage', '04_DESIGN_TABLES'), os.path.join(R, '04_DESIGN_TABLES'), dirs_exist_ok=True)
live16 = rows(os.path.join(H, '04_DESIGN_TABLES', 'DesignTable_1603.xlsx')); a14 = rows(A14)
stage16 = rows(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_1603.xlsx'))
assert stage16 == live16, 'the Air-Way stage changed 1603'
diff = [(i, a, b) for i, (a, b) in enumerate(zip(live16, a14)) if a != b]
assert len(live16) == len(a14) and all(str(a[0]) == '1603-08-08-08-FG' for _, a, _ in diff), diff
shutil.copy2(A14, os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_1603.xlsx'))
say(f'root18 = Air-Way stage + A14 1603 ({len(diff)} row(s) differ from live: 1603-08-08-08-FG)')
# (the generators read only <OMI_ROOT>/04_DESIGN_TABLES - as in airway_first_20261020/scripts/regen.py, OMI_ROOT = its stage folder)


# 3. regenerate + compare
GENS = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}
def spec_roots(g):
    code = (f"import sys, json, io, contextlib; sys.path[:0] = [{os.path.join(T, 'generators')!r}, {T!r}]\n"
            f"with contextlib.redirect_stdout(io.StringIO()):\n    import {g[:-3]} as m\nprint(json.dumps(list(m.SPEC)))")
    p = subprocess.run([sys.executable, '-I', '-c', code], env=dict(os.environ, OMI_ROOT=R, OMI_REV_EXTRA=EXTRA), capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])
def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()] if os.path.exists(p) else None
def sw2(p):
    return rows(p) if os.path.exists(p) else None
af_roots = set(json.load(open(os.path.join(AF, 'dryrun', 'roots.json'))))
bad = 0; res = []
for kind, (g, var) in GENS.items():
    for r in spec_roots(g):
        d = os.path.join(B, 'regen', kind); os.makedirs(d, exist_ok=True)
        p = subprocess.run([sys.executable, '-I', '-B', os.path.join(T, 'generators', g), r], capture_output=True, text=True,
                           env=dict(os.environ, OMI_ROOT=R, OMI_REV_EXTRA=EXTRA, **{var: d}))
        m1, t1 = mac(os.path.join(d, f'Build_{r}_MASTER.bas')), sw2(os.path.join(d, f'DesignTable_{r}_SW2.xlsx'))
        if r in af_roots:
            ref, src = os.path.join(AF, 'regen', 'stage', kind), 'airway-stage'
        elif r.startswith('FS'):
            ref = os.path.join(ORFS, 'out', 'tee') if kind == 'tee' else os.path.join(ORFS, 'out'); src = 'orfs-tested'
        else:
            ref, src = None, 'shipped'
        if ref:
            m0, t0 = mac(os.path.join(ref, f'Build_{r}_MASTER.bas')), sw2(os.path.join(ref, f'DesignTable_{r}_SW2.xlsx'))
        else:
            m0, t0 = mac(os.path.join(H, '03_SCRIPTS', f'Build_{r}_MASTER.bas')), sw2(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
        sm, st = m0 == m1, t0 == t1
        note = ''
        if r == '1603' and t0 and t1:
            dr = [a[0] for a, b in zip(t0, t1) if a != b] + [x[0] for x in t1[len(t0):]]
            note = f' changed rows {dr}'
        status = 'same' if sm and st else 'DIFFERS'
        if not (sm and st) and r != '1603': bad += 1
        res.append(f'{kind:8} {r:9} vs {src:12} rc {p.returncode} macro {"=" if sm else "!=" if m0 and m1 else "missing" } SW2 {"=" if st else "!=" if t0 and t1 else "missing"} {status}{note}')
# the O-ring master 4000 (gen_ring: 4000 / 4001 / FS4000) vs the dry-run-tested orfs_gen_20261020/out/ring
d = os.path.join(B, 'regen', 'ring'); os.makedirs(d, exist_ok=True)
p = subprocess.run([sys.executable, '-I', '-B', os.path.join(T, 'generators', 'gen_ring.py'), '4000'], capture_output=True, text=True,
                   env=dict(os.environ, OMI_ROOT=R, OMI_REV_EXTRA=EXTRA, GR_OUT=d,
                            GR_REV=os.path.join(H, 'tools', '_out', 'newtypes_20261014', 'review_tables')))
ref = os.path.join(ORFS, 'out', 'ring')
sm = mac(os.path.join(ref, 'Build_4000_MASTER.bas')) == mac(os.path.join(d, 'Build_4000_MASTER.bas'))
st = sw2(os.path.join(ref, 'DesignTable_4000_SW2.xlsx')) == sw2(os.path.join(d, 'DesignTable_4000_SW2.xlsx'))
bad += not (sm and st)
res.append(f'ring     4000      vs orfs-tested  rc {p.returncode} macro {"=" if sm else "!="} SW2 {"=" if st else "!="} {"same" if sm and st else "DIFFERS"}')
say('\n'.join(res))
say(f'\n{bad} root(s) differ (1603 listed separately)')
open(os.path.join(B, 'cmp.txt'), 'w', encoding='utf-8').write('\n'.join(log) + '\n')
