"""regen_all.py (2026-10-21): CLAUDE.md "changing a generator touches every macro" - every SPEC root of gen_straight2 / gen_tee regenerated with
the OLD toolset (tools/_out/orfs_gen_20261020/tools = the ORFS staging tools) and the NEW one (../tools = + the per-size FS end tables), on the
same inputs (OMI_ROOT = the brennancad stage, OMI_REV_EXTRA = its ORFS tables). Per root: exit codes, configurations old / new, NEW / LOST,
changed configurations and which columns changed, macro identical (generation-date lines ignored). -> ../regen/cmp.txt"""
import os, sys, re, subprocess, collections, openpyxl
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
OLD = os.path.join(ROOT, 'tools', '_out', 'orfs_gen_20261020', 'tools', 'generators'); NEW = os.path.join(H, 'tools', 'generators')
ST = os.path.join(ROOT, 'tools', '_out', 'brennancad_20261021', 'stage')
OUT = os.path.join(H, 'regen')


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M)) if m else set()
    return k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M))


def run(side, gen, g, r):
    o = os.path.join(OUT, side, r); os.makedirs(o, exist_ok=True)
    env = dict(os.environ, OMI_ROOT=ST, OMI_REV_EXTRA=os.path.join(ST, 'orfs_tables'), GS_OUT=o, GT_OUT=o)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(gen, g), r], env=env, capture_output=True, text=True)
    open(os.path.join(o, 'stdout.txt'), 'w').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode


def load(p):
    if not os.path.exists(p):
        return {}
    rs = list(openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)); h = rs[0]
    return {r[0]: dict(zip(h, r)) for r in rs[1:] if r and r[0]}


def txt(p):
    if not os.path.exists(p):
        return None
    s = open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    return re.sub(r'(?m)^.*(Generated|generated) .*\d{4}-\d{2}-\d{2}.*$', '', s)


jobs = [(r, 'gen_straight2.py') for r in sorted(spec(os.path.join(NEW, 'gen_straight2.py')))] + \
       [(r, 'gen_tee.py') for r in sorted(spec(os.path.join(NEW, 'gen_tee.py')))]
# the FS leg-shape sibling masters are added to SPEC in a loop (gen_tee fs_code), so spec() does not list them
SIBLINGS = ['FS2500N', 'FS2501N', 'FS2503N', 'FS2601N', 'FS2603N', 'FS6500C', 'FS6500NC', 'FS6500N', 'FS6600C', 'FS6600NC', 'FS6600N',
            'FS6602C', 'FS6602NC', 'FS6602N', 'FS6801NR', 'FS6801R', 'FS6802NR', 'FS6802R', 'FS2701N', 'FS2702N', 'FS2703N', 'FS2704N',
            'FS6803R', 'FS6803NR', 'FS6804R', 'FS6804NR']
jobs += [(r, 'gen_tee.py') for r in SIBLINGS if (r, 'gen_tee.py') not in jobs]


def one(job):
    r, g = job
    rc_o = run('old', OLD, g, r); rc_n = run('new', NEW, g, r)
    o = load(os.path.join(OUT, 'old', r, f'DesignTable_{r}_SW2.xlsx')); n = load(os.path.join(OUT, 'new', r, f'DesignTable_{r}_SW2.xlsx'))
    mo = txt(os.path.join(OUT, 'old', r, f'Build_{r}_MASTER.bas')); mn = txt(os.path.join(OUT, 'new', r, f'Build_{r}_MASTER.bas'))
    chg = collections.Counter(); cfgs = []
    for k in set(o) & set(n):
        if o[k] != n[k]:
            cfgs.append(k)
            for c in set(o[k]) | set(n[k]):
                if o[k].get(c) != n[k].get(c):
                    chg[c] += 1
    return (f'{r:8} rc {rc_o}/{rc_n} | configs {len(o):3d} -> {len(n):3d} | NEW {sorted(set(n) - set(o))} | LOST {sorted(set(o) - set(n))} | '
            f'changed {len(cfgs)} {dict(chg)} | macro same: {mo == mn}')


with ThreadPoolExecutor(6) as ex:
    lines = list(ex.map(one, jobs))
open(os.path.join(OUT, 'cmp.txt'), 'w').write('\n'.join(lines) + '\n')
same = [l for l in lines if 'NEW [] | LOST [] | changed 0 {} | macro same: True' in l]
print(f'{len(lines)} roots; {len(same)} identical; differences:')
print('\n'.join(l for l in lines if l not in same))
