"""run_checks.py (group B): the static checks on every master the group B work adds or changes (regen/cmp.txt lines with NEW > 0 or a
macro that DIFFERS): vbacheck, dofcheck_straight / dofcheck_tee (fully defined, 0 redundant), allcfg_check (outline of every configuration),
regress (old configurations unchanged, roots that existed before). Writes checks/*.txt and copies the new macros + SW2 tables to out/<set>/."""
import os, sys, re, subprocess, shutil
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
sys.path.insert(0, H)
import regen_all as R
OUT = os.path.join(A, 'checks'); os.makedirs(OUT, exist_ok=True)
rows = []
for l in open(os.path.join(A, 'regen', 'cmp.txt'), encoding='utf-8'):
    m = re.match(r'(\w+):(\w+)\s+(\S+)\s+rc (\S+)/(\S+) \| configs old\s+(\d+) new\s+(\d+) \| NEW (\d+) \| LOST (\d+).*\| macro (\S+)', l)
    if not m: continue
    s, gen, mr, rco, rcn, co, cn, new, lost, mac = m.groups()
    if int(new) > 0 or mac == 'DIFFERS': rows.append((s, gen, mr, int(co), int(cn), int(new), int(lost), mac))
res = {k: [] for k in ('vbacheck', 'dofcheck_straight', 'dofcheck_tee', 'allcfg', 'regress')}
for s, gen, mr, co, cn, new, lost, mac in rows:
    cfg = R.SETS[s]; tools = cfg['new']; env = dict(os.environ, **cfg['env_new'])
    job = mr if os.path.isdir(os.path.join(A, 'regen', 'new', s, mr)) else [d for d in os.listdir(os.path.join(A, 'regen', 'new', s)) if os.path.exists(os.path.join(A, 'regen', 'new', s, d, f'Build_{mr}_MASTER.bas'))][0]
    nd = os.path.join(A, 'regen', 'new', s, job); od = os.path.join(A, 'regen', 'old', s, job)
    bas = os.path.join(nd, f'Build_{mr}_MASTER.bas')
    run = lambda args, e=None: subprocess.run([sys.executable] + args, capture_output=True, text=True, env=e or os.environ)
    p = run([os.path.join(tools, 'checks', 'vbacheck.py'), bas]); res['vbacheck'].append(p.stdout.strip().replace(A + os.sep, '') or p.stderr[-300:])
    if gen == 'gen_straight2':
        p = run([os.path.join(tools, 'checks', 'dofcheck_straight.py'), bas]); res['dofcheck_straight'].append(p.stdout.strip() or p.stderr[-300:])
        p = run([os.path.join(tools, 'checks', 'allcfg_check.py'), 's', mr], dict(env, GS_OUT=nd, GT_OUT=nd)); res['allcfg'].append(p.stdout.strip() or p.stderr[-300:])
    elif gen == 'gen_tee':
        p = run([os.path.join(tools, 'checks', 'dofcheck_tee.py'), bas]); res['dofcheck_tee'].append(p.stdout.strip() or p.stderr[-300:])
        p = run([os.path.join(tools, 'checks', 'allcfg_check.py'), 't', mr], dict(env, GS_OUT=nd, GT_OUT=nd)); res['allcfg'].append(p.stdout.strip() or p.stderr[-300:])
    if co:
        p = run([os.path.join(tools, 'checks', 'regress.py'), od, nd, mr]); res['regress'].append(p.stdout.strip() or p.stderr[-300:])
    dst = os.path.join(A, 'out', s); os.makedirs(dst, exist_ok=True)
    for f in (f'Build_{mr}_MASTER.bas', f'DesignTable_{mr}_SW2.xlsx'):
        if os.path.exists(os.path.join(nd, f)): shutil.copy2(os.path.join(nd, f), os.path.join(dst, f))
for k, v in res.items():
    open(os.path.join(OUT, f'{k}.txt'), 'w', encoding='utf-8').write('\n'.join(v) + '\n')
    print(f'== {k}'); print('\n'.join(v))
