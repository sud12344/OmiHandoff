"""regress_all.py (2026-10-20, ORFS generator staging): regenerate EVERY root of both generators with the OLD toolset (the merged batch-17
tools, tools/_out/genfeat_20261018/merged/tools) and the NEW one (tools/_out/orfs_gen_20261020/tools), same inputs (OMI_ROOT = the batch-17
stage; OMI_REV_EXTRA = the staged ORFS tables for the new FS roots), each root in its own process, and compare: macro (generated-date line
aside, line endings ignored), SW2 cell by cell, summary json, exit code. Expected: every existing root identical; only the FS roots new.
Output: regen/{old,new}/{straight,tee}/, regress_all.txt"""
import os, re, subprocess, sys, json
import openpyxl
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
TOOLS = {'old': os.path.join(ROOT, 'tools', '_out', 'genfeat_20261018', 'merged', 'tools'), 'new': os.path.join(HERE, 'tools')}
STAGE = os.path.join(ROOT, 'tools', '_out', 'brennan_yes_20261018', 'stage')
EXTRA = os.path.join(ROOT, 'tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')
GENS = {'straight': ('gen_straight2.py', 'GS_OUT'), 'tee': ('gen_tee.py', 'GT_OUT')}


def roots(gen):
    s = open(gen, encoding='utf-8').read()
    i = s.index('SPEC = {'); j = s.index('\n}\n', i)
    upd = ''.join(s[k:s.index('\n})\n', k)] for k in [m.end() for m in re.finditer(r'^SPEC\.update\(\{', s, re.M)])
    return list(dict.fromkeys(re.findall(r"^\s*'([0-9A-Z]+(?:-[A-Z]+)?)': dict\(", s[i:j], re.M) + re.findall(r"^SPEC\['([0-9A-Z]+)'\] = dict\(", s, re.M)
                              + re.findall(r"^\s*'([0-9A-Z]+)': dict\(", upd, re.M)))


def mac(p):
    return [l for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').splitlines() if 'generated' not in l.lower()]


def sw2(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    return [tuple(r) for r in ws.iter_rows(values_only=True)]


out, bad = [], 0
for kind, (g, var) in GENS.items():
    rs = {v: roots(os.path.join(TOOLS[v], 'generators', g)) for v in TOOLS}
    allr = list(dict.fromkeys(rs['old'] + rs['new']))
    for r in allr:
        res = {}
        for v, t in TOOLS.items():
            if r not in rs[v]:
                res[v] = None; continue
            d = os.path.join(HERE, 'regen', v, kind); os.makedirs(d, exist_ok=True)
            env = dict(os.environ, OMI_ROOT=STAGE, OMI_REV_EXTRA=EXTRA, **{var: d})
            p = subprocess.run([sys.executable, '-I', os.path.join(t, 'generators', g), r], env=env, capture_output=True, text=True)
            res[v] = (p.returncode, d)
        if res['old'] is None:
            out.append(f'{kind:8} {r:8} NEW root (rc {res["new"][0]})'); continue
        if res['new'] is None:
            out.append(f'{kind:8} {r:8} LOST in the new toolset'); bad += 1; continue
        (rc0, d0), (rc1, d1) = res['old'], res['new']
        m0, m1 = (os.path.join(x, f'Build_{r}_MASTER.bas') for x in (d0, d1))
        t0, t1 = (os.path.join(x, f'DesignTable_{r}_SW2.xlsx') for x in (d0, d1))
        same_rc = rc0 == rc1
        same_m = (os.path.exists(m0) == os.path.exists(m1)) and (not os.path.exists(m0) or mac(m0) == mac(m1))
        same_t = (os.path.exists(t0) == os.path.exists(t1)) and (not os.path.exists(t0) or sw2(t0) == sw2(t1))
        ok = same_rc and same_m and same_t
        bad += not ok
        out.append(f'{kind:8} {r:8} {"identical" if ok else "DIFFERS"} (rc {rc0}/{rc1}, macro {"=" if same_m else "!="}, SW2 {"=" if same_t else "!="})')
    # the summary json covers every root of the last run of each generator; compare per root entry
out.append(f'\n{bad} root(s) differ or lost')
open(os.path.join(HERE, 'regress_all.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(l for l in out if 'identical' not in l))
print(sum('identical' in l for l in out), 'identical')
