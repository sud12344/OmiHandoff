"""Re-run every batch-17 root into its own folder regen/b17_per_root/<root>/ (the generators overwrite one summary json per output folder),
collect the summaries into regen/b17_summaries.json and check the macro + SW2 equal regen/b17 (determinism). Usage: python -I summaries_b17.py <repo>"""
import os, sys, json, subprocess, filecmp, glob
from concurrent.futures import ThreadPoolExecutor
REPO = os.path.abspath(sys.argv[1]); HERE = os.path.join(REPO, 'tools/_out/batch17_rebase_20261020')
G = os.path.join(REPO, 'tools/_out/genfeat_20261018/merged/tools/generators')
jobs = [(sub, os.path.basename(p)[6:-11]) for sub in ('straight', 'tee') for p in glob.glob(os.path.join(HERE, 'regen/b17', sub, 'Build_*_MASTER.bas'))]
jobs += [('tee', '1803'), ('tee', '6810')]
def run(j):
    sub, r = j; out = os.path.join(HERE, 'regen/b17_per_root', r); os.makedirs(out, exist_ok=True)
    g, var = ('gen_straight2.py', 'GS_OUT') if sub == 'straight' else ('gen_tee.py', 'GT_OUT')
    subprocess.run([sys.executable, '-I', os.path.join(G, g), r], env=dict(os.environ, OMI_ROOT=os.path.join(HERE, 'root'), **{var: out}), capture_output=True)
    s = json.load(open(os.path.join(out, g.replace('.py', '_summary.json'))))
    same = all(filecmp.cmp(os.path.join(out, f), os.path.join(HERE, 'regen/b17', sub, f), shallow=False)
               for f in (f'Build_{r}_MASTER.bas', f'DesignTable_{r}_SW2.xlsx') if os.path.exists(os.path.join(HERE, 'regen/b17', sub, f)))
    return r, sub, s.get(r, s), same
with ThreadPoolExecutor(4) as ex: res = list(ex.map(run, jobs))
json.dump({r: dict(kind=sub, **s) for r, sub, s, _ in res}, open(os.path.join(HERE, 'regen/b17_summaries.json'), 'w'), indent=1)
print('not byte-identical to regen/b17:', [r for r, _, _, same in res if not same])
