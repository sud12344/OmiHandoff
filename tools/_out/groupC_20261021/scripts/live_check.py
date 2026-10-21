"""live_check.py (group C, 2026-10-21, after the parent merged main = batches 18-20 into this branch): are the group C generator patches
ready for the LIVE toolset? tools_live = the live tools/ (batch 20) + scripts/patches applied (patch_ring.py, gs2_block.py + patch_gs2.py,
patch_gt.py). Regenerates EVERY root of gen_straight2 / gen_tee / gen_ring with the live tools and with tools_live on the LIVE tables
(04_DESIGN_TABLES; tools_live also reads the C tables via OMI_REV_EXTRA): every existing root must be identical, the C roots must give the
same SW2 tables as regen/new (built on the Air-Way-first toolset). Writes regen_live/cmp.txt and live_patched/ (the three patched generators);
tools_live/ is scratch (rebuilt each run, not kept)."""
import os, sys, re, subprocess, openpyxl, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
OLD = os.path.join(ROOT, 'tools', 'generators'); NEW = os.path.join(A, 'tools_live', 'generators')
CT = os.path.join(A, 'stage', '04_DESIGN_TABLES'); OUT = os.path.join(A, 'regen_live')


def make_tools_live():
    """tools_live (scratch, not kept) = the live tools/ (no _out) + the group C patches; also refreshes live_patched/ (the three patched files)"""
    import shutil
    T = os.path.join(A, 'tools_live'); P = os.path.join(H, 'patches'); G = os.path.join(T, 'generators')
    shutil.rmtree(T, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, 'tools'), T, ignore=shutil.ignore_patterns('_out', '__pycache__'))
    s = open(os.path.join(G, 'gen_straight2.py')).read(); a = 'def dashes(pn):\n'; assert s.count(a) == 1
    open(os.path.join(G, 'gen_straight2.py'), 'w').write(s.replace(a, open(os.path.join(P, 'gs2_block.py')).read() + a))
    for pat, f in (('patch_gs2.py', 'gen_straight2.py'), ('patch_gt.py', 'gen_tee.py'), ('patch_ring.py', 'gen_ring.py')):
        subprocess.run([sys.executable, os.path.join(P, pat), os.path.join(G, f)], check=True)
    os.makedirs(os.path.join(A, 'live_patched'), exist_ok=True)
    for f in ('gen_straight2.py', 'gen_tee.py', 'gen_ring.py'): shutil.copy(os.path.join(G, f), os.path.join(A, 'live_patched', f))


make_tools_live()


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():m.end() + 200000], re.M)) if m else set()
    return sorted(k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)))


def run(which, gen, g, r):
    o = os.path.join(OUT, which)
    env = dict(os.environ, OMI_ROOT=ROOT, GS_OUT=os.path.join(o, 'straight'), GT_OUT=os.path.join(o, 'tee'), GR_OUT=os.path.join(o, 'ring'))
    env.pop('OMI_REV_EXTRA', None); env.pop('GR_REV', None)
    if which == 'new': env['OMI_REV_EXTRA'] = CT
    os.makedirs(os.path.join(o, 'log'), exist_ok=True)
    p = subprocess.run([sys.executable, '-B', os.path.join(gen, g), r], env=env, capture_output=True, text=True, cwd=gen)
    open(os.path.join(o, 'log', f'{r}.txt'), 'w').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode


def sw2(p):
    return [tuple(r) for r in openpyxl.load_workbook(p, read_only=True).worksheets[0].iter_rows(values_only=True)] if os.path.exists(p) else None


def bas(p):
    return open(p).read().replace('\r\n', '\n') if os.path.exists(p) else None


jobs = []
for g, sub in (('gen_straight2.py', 'straight'), ('gen_tee.py', 'tee'), ('gen_ring.py', 'ring')):
    o_, n_ = spec(os.path.join(OLD, g)), spec(os.path.join(NEW, g))
    for r in sorted(set(o_) | set(n_)): jobs.append((g, sub, r, r in o_, r in n_))
with cf.ThreadPoolExecutor(8) as ex:
    futs = {}
    for g, sub, r, io, inn in jobs:
        if io: futs[ex.submit(run, 'old', OLD, g, r)] = ('old', r)
        if inn: futs[ex.submit(run, 'new', NEW, g, r)] = ('new', r)
    rc = {futs[f]: f.result() for f in cf.as_completed(futs)}
lines = []; same = diff = new = 0; cmatch = 0
for g, sub, r, io, inn in jobs:
    po = lambda w, f: os.path.join(OUT, w, sub, f)
    bo, bn = bas(po('old', f'Build_{r}_MASTER.bas')), bas(po('new', f'Build_{r}_MASTER.bas'))
    to, tn = sw2(po('old', f'DesignTable_{r}_SW2.xlsx')), sw2(po('new', f'DesignTable_{r}_SW2.xlsx'))
    if not io:
        new += 1
        tc = sw2(os.path.join(A, 'regen', 'new', sub, f'DesignTable_{r}_SW2.xlsx'))
        m_ = (tn == tc) if tn is not None else (tc is None)
        cmatch += m_
        lines.append(f'{r:8} [{sub}] NEW (group C): rc {rc.get(("new", r))}, {len(tn) - 1 if tn else 0} configurations; SW2 '
                     + ('== the staged regen/new table' if m_ else 'DIFFERS from the staged regen/new table'))
        continue
    ok = bo == bn and to == tn and rc.get(('old', r)) == rc.get(('new', r))
    same += ok; diff += not ok
    lines.append(f'{r:8} [{sub}] rc {rc.get(("old", r))}/{rc.get(("new", r))} ' + ('IDENTICAL' if ok else f'DIFFERENT macro {bo == bn} table {to == tn}')
                 + (f' ({len(to) - 1} configurations)' if to else ' (no table)'))
head = f'live_check: {same} live roots identical with the group C patches, {diff} different; {new} group C roots, {cmatch} with the same SW2 as regen/new'
print(head); print('\n'.join(l for l in lines if 'DIFFER' in l or 'NEW' in l))
open(os.path.join(OUT, 'cmp.txt'), 'w').write(head + '\n' + '\n'.join(lines) + '\n')
import shutil; shutil.rmtree(os.path.join(A, 'tools_live'), ignore_errors=True)     # scratch
