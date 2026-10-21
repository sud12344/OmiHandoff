"""step_checklist.py (2026-10-21, cloud): the Brennan STEP download list the PC session sent on 2026-10-20 (blocked-needs summary,
section 1), expanded to full part numbers and checked against the repo. Read-only except for its two outputs.

For every requested file:
- brennan_pn: the number to search for on Brennan's PARTcommunity portal = the Brennan catalog's printed number when the catalog prints
  this size (exact or same core), else the OMi number (marked "not in the PDF catalogs - may not exist at Brennan");
- have: already in 09_STEP_FILES;
- frees: the not-ready OMi parts with the same core (size + shape) - the parts this one file is for (pilot / shape files free more,
  through their family; that is noted in the group, not counted here).
Writes STEP_CHECKLIST.csv and STEP_CHECKLIST.md next to this script.
Usage: python -I step_checklist.py            (re-run after new files land in 09_STEP_FILES: the "have" column updates)"""
import os, re, csv, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
SUFFIX = {'FG', 'NWO', 'O', 'TUBE', 'ASY'}


def core(pn):
    t = [x for x in norm(pn).split('-') if x]
    while len(t) > 1 and t[-1] in SUFFIX:
        t.pop()
    return '-'.join(x.zfill(2) if x.isdigit() and len(x) < 2 else x for x in t)


def sizes(root, dashes, n=1, suffix=''):
    """sizes('6805', '04-02 04-04', ...) -> ['6805-04-02<suffix>', ...]; n repeats a single dash n times (tees)."""
    return [f"{root}-{'-'.join([d] * n) if '-' not in d else d}{suffix}" for d in dashes.split()]


G = []   # (priority, group, note, [part numbers as the PC list names them])
G.append((1, 'Quick wins', 'together free 18 parts (5405 family)', ['5405-24-24', '5405-32-32']))
G.append((2, 'ORFS shared shape files', 'each serves several FS masters',
          sizes('FS2403', '04-04 06-06 10-10 12-12 16-16 20-20') + sizes('FS2701', '04-04 06-06 10-10 12-12 16-16', suffix='-FG')
          + sizes('FS6801', '04-04 06-06 10-10 12-12 16-16 20-20 24-24', suffix='-NWO-FG')
          + ['FS6500-24-24-FG', 'FS6502-06-06-FG', 'FS2406-08-04', 'FS0304-C-08', 'FS2503-08-06-FG', 'FS6809-06-06-NWO-FG']))
G.append((3, 'ORFS one file per part', '',
          sizes('FS1700', '12-12 16-16 20-20 24-24') + sizes('FS1800', '12-12 16-16 20-20 24-24')
          + sizes('FS1704', '12-12 16-16 20-20 24-24', suffix='-FG') + sizes('FS1804', '12-12 16-16 20-20 24-24', suffix='-FG')
          + ['FS2406-12-16', 'FS2406-16-20', 'FS6400-10-06-O', 'FS6400-12-20-O', 'FS6565-10-10', 'FS6565-16-16', 'FS7202-06-04-NWO-FG']))
G.append((4, 'Code 62 heads', 'not needed if the user says yes to Q2 of the PC list', sizes('1824', '12 16 20 24 32')))
G.append((5, 'Pilots (one shape file per family)', 'each unlocks its whole family',
          [p + '-NWO-FG' for p in ('6801-L-08-08', '6801-LL-08-08', '6805-08-08', '6806-08-08', '6807-08-08', '6809-10-10', '6815-08-08',
                                   '6901-06-08', '6902-08-08', '6832-08-08-08', '6835-08-08-08')] + ['6900-08-08-O']))
forged = (sizes('6801', '08-04 08-16 12-20 16-24 24-16') + ['6801-L-16-16', '6801-L-20-20', '6801-LL-12-12', '6801-LL-16-16', '6801-LL-20-20']
          + ['6802-06-10', '6802-08-12', '6803-08-08-06', '6803-08-08-10', '6803-24-24-24', '6804-24-24-24', '6810-12-12']
          + sizes('6805', '04-02 04-04 06-06 10-08 12-08 16-12 16-16 20-20') + sizes('6806', '06-04 06-06 08-06 10-08 12-08 12-12 16-16 20-20 24-24')
          + sizes('6807', '04-04 08-06 12-12') + sizes('6809', '12-12 16-16 20-20') + sizes('6815', '04-04 06-06 10-10 12-12 16-16')
          + sizes('6832', '04 06 16', 3) + sizes('6835', '04 06 12', 3)
          + sizes('6901', '04-04 04-06 10-12 12-06 12-08 12-12 12-16 16-12 16-16 20-16 20-20 24-24 32-32')
          + sizes('6902', '04-04 06-04 06-06 08-06 10-08 10-12 16-16 24-24')
          + sizes('5602', '02 06 12 16 20 24 32', 3) + sizes('5604', '02 12 16 20 32', 3) + sizes('5605', '02 12 16 20 32', 3)
          + sizes('5505', '02 06 12 16', 2) + sizes('5503', '04-02 06-04 08-06 12-08 16-12')
          + ['5504-32-32', '5652-32-32-32-32', '6503-06-06', '6503-16-16', '6603-16-16-16', '6606-12-12-12', '6566-16-16', '1504-24-24',
             '1504-32-32', '2505-16-16'])
G.append((6, 'Forged parts, one file per size', '', forged))
G.append((7, 'Flanges', '', sizes('1703', '08-08 12-12 16-16 20-20 32-32', suffix='-FG') + sizes('1704', '08-08 12-12 16-16 20-20 32-32', suffix='-FG')
          + sizes('1803', '12-12 16-16 20-20 24-24 32-32', suffix='-FG') + sizes('1804', '12-12 16-16 20-20 24-24 32-32', suffix='-FG')
          + sizes('1800', '12-12 12-16 16-12 16-16 16-20 16-24 20-16 20-20 20-24 24-20 24-24 32-32') + sizes('1724', '12 16 20 24 32 40')))
G.append((8, 'Plugs', 'OMi 6408-HHP-NN-O = Brennan 6408-HNN-O (as for the shipped -08)',
          [f'6408-H{d}-O' for d in '02 03 04 05 06 10 12 16 20 24 32'.split()]))
G.append((9, 'Other', '', ['0304-C-02', '0306-02', '5404-L-04X3.000', '5404-L-04X4.000', '5405-08-16', '6405-32-24-O', '6420-12-12']
          + sizes('6425', '04-04 06-06 10-10 12-12 16-16') + ['6900-32-32-O', '2404-32-48', 'V0318-08', 'V0319-08']))

# --- data
cat = json.load(open(J('tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')))
bcat, bcore = {}, collections.defaultdict(list)
for t in cat['tables']:
    for r in t['rows']:
        p = norm(r['pn']); bcat.setdefault(p, f"{t['catalog']} p{t.get('printed_page') or t['page']}"); bcore[core(p)].append(p)
have = {norm(os.path.basename(f)[8:-4]) for f in glob.glob(J('09_STEP_FILES', 'BRENNAN_*.stp'))}
nr = [norm(l) for l in open(os.path.join(HERE, 'not_ready_1022.txt')) if l.strip()]
nr_core = collections.defaultdict(list)
for p in nr:
    nr_core[core(p.replace('6408-HHP-', '6408-H').replace('5406-HHP-', '5406-HP-').replace('0618-', 'V0318-').replace('0619-', 'V0319-'))].append(p)

rows, seen = [], set()
for prio, grp, note, pns in G:
    for p in pns:
        p = norm(p); c = core(p)
        if p in bcat:
            bpn, where = p, bcat[p]
        elif bcore.get(c):
            b = bcore[c][0]
            # take the catalog's number when it only adds suffixes (6805-04-02 -> 6805-04-02-NWO-FG); keep a requested -FG that the
            # flange catalog leaves off (1703-08-08-FG: the portal files carry it, e.g. the BRENNAN_1703-24-24-FG.stp in the repo)
            bpn = b if len(b) >= len(p) else p
            where = bcat[b] + ('' if b == bpn else f' (printed as {b})')
        else:
            bpn, where = p, 'not in the PDF catalogs - may not exist at Brennan; search the portal'
        frees = nr_core.get(c, [])
        rows.append(dict(priority=prio, group=grp, requested=p, brennan_pn=bpn, file_name=f'BRENNAN_{bpn}.stp',
                         have='yes' if bpn in have or p in have else '', duplicate='yes' if bpn in seen else '',
                         in_brennan_catalog=where, frees_parts=len(frees), frees=' '.join(frees), group_note=note))
        seen.add(bpn)
rows.append(dict(priority=9, group='Other', requested='3051-??-??', brennan_pn='3051 (size not given)', file_name='BRENNAN_3051-<size>.stp',
                 have='', duplicate='', in_brennan_catalog='TFA: 3051-02-02 ... -16-16 printed',
                 frees_parts=sum(len(v) for k, v in nr_core.items() if k.startswith('3051')),
                 frees=' '.join(p for p in nr if p.startswith('3051')), group_note='the PC list does not say which size - ask the PC session'))
with open(os.path.join(HERE, 'STEP_CHECKLIST.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

todo = [r for r in rows if not r['have'] and not r['duplicate']]
md = ['# Brennan STEP download checklist (2026-10-21)', '',
      'Source: the PC session\'s blocked-needs list of 2026-10-20 (section 1), expanded to full part numbers by `step_checklist.py`.',
      'Download each from Brennan\'s PARTcommunity / CADENAS portal and save it as `09_STEP_FILES/BRENNAN_<part number>.stp`',
      '(the file name column). Re-run `python -I tools/_out/sources_20261021/step_checklist.py` afterwards: the box column fills in.', '',
      f'**{len(todo)} files to download** ({sum(1 for r in rows if r["have"])} already in the repo, '
      f'{sum(1 for r in rows if r["duplicate"])} listed twice). Files marked * are not printed in Brennan\'s PDF catalogs: '
      'search for them, and tell me which ones Brennan does not have.', '']
for prio, grp, note, _ in G:
    rs = [r for r in rows if r['group'] == grp]
    md += [f'## {prio}. {grp} ({len(rs)})' + (f' - {note}' if note else ''), '', '| | File | For (not-ready OMi parts of this size) |', '|---|---|---|']
    for r in rs:
        box = 'x' if r['have'] else ('dup' if r['duplicate'] else ' ')
        star = ' *' if r['in_brennan_catalog'].startswith('not in') else ''
        md.append(f"| [{box}] | `{r['file_name']}`{star} | {r['frees'] or '(shape file for the family)'} |")
    md.append('')
md += ['## Also', '', '- One 3051 file: the PC list does not say which size (not-ready: ' + rows[-1]['frees'] + ').', '']
# --- arrival check: every BRENNAN_*.stp must name its own part number in a STEP PRODUCT entry (as the 2026-10-20 pilots do)
bad = []
for f in sorted(glob.glob(J('09_STEP_FILES', '*'))):
    b = os.path.basename(f)
    if b.lower().endswith('.zip'):
        continue
    if not re.match(r'^BRENNAN_[A-Z0-9][A-Z0-9.\-]*\.stp$', b):
        bad.append(f'{b}: name is not BRENNAN_<part number>.stp'); continue
    head = open(f, encoding='latin-1', errors='replace').read(400000).upper()
    prods = re.findall(r"PRODUCT\s*\(\s*'([^']*)'", head)
    if prods and not any(norm(x) == norm(b[8:-4]) or norm(b[8:-4]) in norm(x) for x in prods):
        bad.append(f'{b}: STEP PRODUCT names {prods[:2]}')
md += ['## Arrival check (09_STEP_FILES)', ''] + ([f'- {x}' for x in bad] or ['- every file is named BRENNAN_<pn>.stp and names that part inside.']) + ['']
open(os.path.join(HERE, 'STEP_CHECKLIST.md'), 'w', encoding='utf-8').write('\n'.join(md))
print('arrival check:', bad or 'clean')
print(f'{len(rows)} requested, {len(todo)} to download, {sum(1 for r in rows if r["have"])} in repo, '
      f'{sum(1 for r in rows if r["in_brennan_catalog"].startswith("not in"))} not in the PDF catalogs, '
      f'{sum(1 for r in rows if not r["frees_parts"])} free no not-ready part directly')
for r in rows:
    if not r['frees_parts'] or r['have']:
        print('  ', r['requested'], 'have' if r['have'] else 'frees 0', r['in_brennan_catalog'][:50])
