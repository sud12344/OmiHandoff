"""Copied 2026-10-20 for the batch 17 paperwork from (batch 18: copied from tools/_out/batch17_20261019/paperwork, unchanged) tools/_out/ship_20261019/paperwork/count_configs.py (unchanged logic; 6400 is now a
generated master in 11_MASTERS, so the hand-built branch counts nothing). Run without the old argument.
no longer listed as missing configurations (batch 16 rebuilt it with all 26). Run without the old argument.
Copied 2026-10-08 for the batch 15 paperwork from tools/_out/ship_20261002/paperwork/count_configs.py (unchanged logic; writes its json here).
Batch 14 paperwork (2026-10-02): count BUILD rows and configurations in a master.

Read-only. Usage: python count_configs.py [old]
  (no arg) = the current 04_DESIGN_TABLES SW2 tables and 11_MASTERS
  old      = the state BEFORE batch 14: the 22 replaced SW2 tables are read from
             tools/_out/ship_20261002/old_files/04_DESIGN_TABLES (to reproduce the 2026-09-25 counts 853 / 4 / 98 / 21)
Definitions (as PROJECT_STATUS section 1, 2026-09-25):
  BUILD row   = a review-table row (04_DESIGN_TABLES/DesignTable_<t>.xlsx, not _SW2, not 6400_v2) with $PRP@ScopeAction BUILD
  in a master = a BUILD row that is a configuration of an SW2 table whose root has a master:
                11_MASTERS (current set; minus configurations known to be missing from the built file),
                hand-built 2404 / 6400 (files not in the repo), held-back 2702 / 2703 (tools/_out/overnight)
"""
import glob, os, sys, json, collections
import openpyxl

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
OLD = len(sys.argv) > 1 and sys.argv[1] == 'old'
OLD_SW2 = os.path.join(R, r'tools\_out\ship_20261002\old_files\04_DESIGN_TABLES')


def load(f):
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    hi = next(i for i, r in enumerate(rows[:6]) if any(isinstance(x, str) and ('DataStatus' in x or '@' in x) for x in r if x))
    hdr = [str(x) if x is not None else '' for x in rows[hi]]

    def col(k):
        for i, h in enumerate(hdr):
            if k in h:
                return i
        return None
    out = []
    for r in rows[hi + 1:]:
        if not r or not r[0]:
            continue
        g = lambda k: (r[col(k)] if col(k) is not None and col(k) < len(r) else None)
        out.append(dict(cfg=str(r[0]).strip(), sku=g('OMiSKU'), part=g('PartNo'), ds=str(g('DataStatus') or ''),
                        sa=str(g('ScopeAction') or '')))
    return out


# review tables
build = {}          # cfg / part / sku -> (table, ds)
n_build = 0
n_missing = 0
by_status = collections.Counter()
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2':
        continue
    for x in load(f):
        if x['sa'].strip().upper() != 'BUILD':
            continue
        n_build += 1
        ds = x['ds'].upper()
        st = 'VERIFIED' if ds.startswith('VERIFIED') else 'ASSUMED' if ds.startswith('ASSUMED') else 'MISSING' if 'MISSING' in ds else 'OTHER'
        by_status[st] += 1
        for k in (x['cfg'], x['part'], x['sku']):
            if k:
                build.setdefault(str(k).strip(), (t, st))

masters = {os.path.basename(p)[:-14] for p in glob.glob(os.path.join(R, '11_MASTERS', '*_MASTER.SLDPRT'))}
ROOTS22 = '6502 6802 6404 6410 6565 2403 2405 0403 1404 2705 2706 6401 6402 6405 6408 6504 6505 2501 2503 5500 5502 6500'.split()
NOT_IN_FILE = {}
if OLD:
    NOT_IN_FILE['6401'] = {'6401-32-32-O'}
res = collections.OrderedDict()
tot = collections.Counter()
per_root = {}
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*_SW2.xlsx'))):
    m = os.path.basename(f)[12:-9]
    if OLD and m in ROOTS22:
        f = os.path.join(OLD_SW2, os.path.basename(f))
    rows = load(f)
    cfgs = [x['cfg'] for x in rows]
    inb = [c for c in cfgs if c in build]
    notb = [c for c in cfgs if c not in build]
    if m in masters:
        miss = NOT_IN_FILE.get(m, set())
        k_built = [c for c in inb if c not in miss]
        k_wait = [c for c in inb if c in miss]
        tot['11_MASTERS'] += len(k_built)
        tot['waiting'] += len(k_wait)
        tot['sw2_rows_11_MASTERS'] += len([c for c in cfgs if c not in miss])
        kind = '11_MASTERS'
    elif m in ('2404', '6400'):
        tot['hand-built 2404/6400'] += len(inb)
        kind = 'hand-built'
    elif m in ('2702', '2703'):
        tot['held 2702/2703'] += len(inb)
        kind = 'held'
    else:
        tot['table, no master'] += len(inb)
        kind = 'no master'
    per_root[m] = dict(kind=kind, sw2_rows=len(cfgs), build_rows=len(inb), non_build=notb)
in_master = tot['11_MASTERS'] + tot['waiting'] + tot['hand-built 2404/6400'] + tot['held 2702/2703']
print('STATE', 'BEFORE batch 14 (old SW2 for the 22 roots)' if OLD else 'NOW')
print('review BUILD rows', n_build, dict(by_status))
print('masters in 11_MASTERS', len(masters))
for k, v in tot.items():
    print(f'  {k}: {v}')
print('  BUILD rows in a master:', in_master)
print('  BUILD rows with data (VERIFIED/ASSUMED) and no master configuration:',
      by_status['VERIFIED'] + by_status['ASSUMED'] - in_master)
for m, d in per_root.items():
    if d['non_build']:
        print('  SW2 configs that are not BUILD rows:', m, len(d['non_build']), d['non_build'][:20])
if not OLD:
    print('22 roots:', ' '.join(f"{m}={per_root[m]['sw2_rows']}" for m in ROOTS22))
json.dump(dict(state='old' if OLD else 'now', n_build=n_build, by_status=by_status, tot=tot, in_master=in_master,
               per_root=per_root), open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     'counts_old.json' if OLD else 'counts_now.json'), 'w'), indent=1)

# --- detail: the BUILD rows with data but no master configuration, and the OTHER-status rows
in_master_cfgs = set()
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*_SW2.xlsx'))):
    m = os.path.basename(f)[12:-9]
    if OLD and m in ROOTS22:
        f = os.path.join(OLD_SW2, os.path.basename(f))
    if m in masters or m in ('2404', '6400', '2702', '2703'):
        for x in load(f):
            in_master_cfgs.add(x['cfg'])
nomaster = collections.defaultdict(list)
other = []
sw2_roots = {os.path.basename(f)[12:-9] for f in glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*_SW2.xlsx'))}
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2':
        continue
    for x in load(f):
        if x['sa'].strip().upper() != 'BUILD':
            continue
        ds = x['ds'].upper()
        if not (ds.startswith('VERIFIED') or ds.startswith('ASSUMED') or 'MISSING' in ds):
            other.append((t, x['cfg'], x['ds']))
            continue
        if 'MISSING' in ds:
            continue
        if not any(k and str(k).strip() in in_master_cfgs for k in (x['cfg'], x['part'], x['sku'])):
            nomaster[t].append(x['cfg'])
print('OTHER-status BUILD rows:', other)
n = sum(len(v) for v in nomaster.values())
print('data rows without a master configuration:', n)
for t, v in sorted(nomaster.items()):
    print(f'  {t}: {len(v)} {v}')

# --- per topology (Topologies sheet roots): BUILD rows, rows in a master, fully modelled
import re as _re
wbm = openpyxl.load_workbook(os.path.join(R, '01_MASTER_DATA', 'OMi_Fitting_Library_MasterData_v1.xlsx'), read_only=True)
tops = [str(r[0]) for r in wbm['Topologies'].iter_rows(min_row=2, values_only=True) if r[0]]
wbm.close()
def top_of(t):
    if t in tops:
        return t
    m = _re.match(r'^(\d{4})', t)
    return m.group(1) if m and m.group(1) in tops else None
per_top = collections.defaultdict(lambda: [0, 0])
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2':
        continue
    tp = top_of(t)
    for x in load(f):
        if x['sa'].strip().upper() != 'BUILD':
            continue
        per_top[tp][0] += 1
        if any(k and str(k).strip() in in_master_cfgs for k in (x['cfg'], x['part'], x['sku'])):
            per_top[tp][1] += 1
with_build = [t for t in tops if per_top[t][0]]
with_master = [t for t in tops if per_top[t][1]]
full = [t for t in tops if per_top[t][0] and per_top[t][0] == per_top[t][1]]
print('topologies', len(tops), 'with BUILD rows', len(with_build), 'with a master configuration', len(with_master),
      'fully modelled', len(full), full)
print('unmapped tables:', per_top.get(None))
