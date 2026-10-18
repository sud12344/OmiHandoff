"""enumerate.py (2026-10-18, after the user's "yes use brennan but still differentiate the two in tables"):
list every part the Brennan decision opens, and every 3D file (STEP) still needed, by re-using possible_2535.py's judgement.
Read-only. Writes ../brennan_rows.csv and ../steps_needed.csv; prints a summary."""
import csv, json, os, re, sys, collections

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
O = lambda *p: os.path.join(ROOT, *p)
OUT = O('tools', '_out', 'brennan_yes_20261018')
sys.path.insert(0, O('tools', '_out', 'adapters77_20261016', 'scripts'))
import possible_2535 as P   # in_brennan, gate_kind, BPN (reads only)

rows = list(csv.DictReader(open(O('tools', '_out', 'unblock_20261008', 'rows.csv'), encoding='utf-8-sig')))
B, S = [], []
for r in rows:
    tab, cfg = r['table'], r['config']
    gates = [g.strip() for g in r['user_gates'].split(';') if g.strip()]
    ks = {P.gate_kind(g) for g in gates} - {'decided'}
    steps = sorted({a.split(':', 1)[1].strip() for g in gates for a in g.split('|') if a.strip().startswith('STEP:')})
    if tab in ('4000', '4001'):
        continue          # O-rings: Air-Way s218 data (possible_2535 counts them as "data now")
    newscope = tab == '4005' or (tab in ('1703', '1704', '1803', '1804') and cfg.endswith('-Tube')) or tab in ('6701', '0618', '0619')
    if newscope:
        if P.in_brennan(cfg):
            B.append(dict(group='A-newscope', table=tab, config=cfg, how='catalog', other_gates=';'.join(gates), steps=' '.join(steps)))
        continue
    if 'brennan' in ks and ks <= {'step', 'decide', 'brennan'}:
        how = 'catalog' if P.in_brennan(cfg) else '3D file'
        B.append(dict(group='A-existing', table=tab, config=cfg, how=how, other_gates=';'.join(g for g in gates if P.gate_kind(g) != 'brennan'),
                      steps=' '.join(steps)))
    if 'step' in ks:
        for s in steps or ['(STEP, part not named)']:
            S.append(dict(why=('Brennan-only row' if 'brennan' in ks else 'shape') , table=tab, config=cfg, step=s))

R77 = json.load(open(O('tools', '_out', 'adapters77_20261016', 'rows77.json'), encoding='utf-8'))
for r in R77:
    if not r['row'] and r['brennan']:
        B.append(dict(group='B-dropped77', table=str(r.get('root') or r.get('table') or ''), config=r.get('pn') or r.get('omi_pn') or r.get('sku'), how='catalog', other_gates='', steps=''))
C = json.load(open(O('tools', '_out', 'orfs_airway_20261015', 'compare_orfs.json'), encoding='utf-8'))
for r in C:
    if r.get('on_website') and r['status'] not in ('VERIFIED', 'ASSUMED') and (r.get('brennan_rows') or P.in_brennan(r['omi_pn'])):
        B.append(dict(group='C-ORFS', table=r['omi_pn'].split('-')[0], config=r['omi_pn'], how='catalog', other_gates='ORFS model type', steps=''))

with open(os.path.join(OUT, 'brennan_rows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['group', 'table', 'config', 'how', 'other_gates', 'steps']); w.writeheader(); w.writerows(B)
with open(os.path.join(OUT, 'steps_needed.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['why', 'table', 'config', 'step']); w.writeheader(); w.writerows(S)

print('Brennan-opened parts:', len(B), dict(collections.Counter((b['group'], b['how']) for b in B)))
print('by table (top 40):', collections.Counter(b['table'] for b in B).most_common(40))
have = {os.path.basename(p)[8:-4].upper() for p in os.listdir(O('09_STEP_FILES')) if p.upper().startswith('BRENNAN_')}
need = sorted({s['step'] for s in S})
missing = [s for s in need if s.upper() not in have]
print('STEP names referenced:', len(need), 'already in 09_STEP_FILES:', len(need) - len(missing), 'still missing:', len(missing))
print('missing:', missing)
