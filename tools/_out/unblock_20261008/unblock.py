"""2026-10-08: what blocks each BUILD row that is not yet in a master, and which user action would unblock it.

Read-only. Inputs: live review / SW2 tables + 11_MASTERS (after batch 15), the catalog impact analysis of the then-727 MISSING rows
(tools/_out/brennan_catalog_20261001/impact/*.json: bucket, open questions, cells, STEP verdicts), the Task C question list
(omi_apply_20260925/taskC/taskC_merged.json: kind gate / opt), 09_STEP_FILES, the batch-15 held rows (QA #169) and the wave-1
family results (tools/_out/newmasters_20261002/work/*/NOTES.md, read by hand on 2026-10-08 - listed below).
Output: rows.csv (one line per unbuilt row) + summary.txt.
"""
import collections, csv, glob, json, os, re
import openpyxl

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
O = os.path.join(R, 'tools', '_out')
HERE = os.path.dirname(os.path.abspath(__file__))


def load(f):
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    wb.close()
    hi = next(i for i, r in enumerate(rows[:6]) if any(isinstance(x, str) and ('DataStatus' in x or '@' in x) for x in r if x))
    hdr = [str(x) if x is not None else '' for x in rows[hi]]
    ci = lambda k: next((i for i, h in enumerate(hdr) if k in h), None)
    out = []
    for r in rows[hi + 1:]:
        if not r or not r[0]:
            continue
        g = lambda k: (r[ci(k)] if ci(k) is not None and ci(k) < len(r) else None)
        out.append(dict(cfg=str(r[0]).strip(), sku=g('OMiSKU'), part=g('PartNo'), ds=str(g('DataStatus') or ''), sa=str(g('ScopeAction') or '')))
    return out


# ---- live state
masters = {os.path.basename(p)[:-14] for p in glob.glob(os.path.join(R, '11_MASTERS', '*_MASTER.SLDPRT'))} | {'2404', '6400'}
in_master = set()
for f in glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*_SW2.xlsx')):
    m = os.path.basename(f)[12:-9]
    if m in masters:
        in_master |= {x['cfg'] for x in load(f)}
in_master -= {'5405-12-08', '5405-16-08', '5405-16-12'}     # in the table, not in the built file (re-run Build_5405)
unbuilt = []
for f in sorted(glob.glob(os.path.join(R, '04_DESIGN_TABLES', 'DesignTable_*.xlsx'))):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2':
        continue
    for x in load(f):
        if x['sa'].strip().upper() != 'BUILD':
            continue
        if any(k and str(k).strip() in in_master for k in (x['cfg'], x['part'], x['sku'])):
            continue
        ds = x['ds'].upper()
        x['status'] = 'MISSING' if 'MISSING' in ds else 'DATA' if ds.startswith(('ASSUMED', 'VERIFIED')) else 'OTHER:' + x['ds']
        x['table'] = t
        unbuilt.append(x)
for c in ('5405-12-08', '5405-16-08', '5405-16-12'):
    pass   # counted as "in a master" by the project counts (macro ready); listed separately in the summary

# ---- impact rows
imp = {}
for g in ['F1a', 'F1b', 'F2a', 'F2b', 'F3', 'F45D']:
    for r in json.load(open(os.path.join(O, 'brennan_catalog_20261001', 'impact', f'{g}.json'), encoding='utf-8'))['rows']:
        r['_g'] = g
        imp.setdefault(r['config'], r)
NEWQ = collections.defaultdict(set)     # questions raised by the catalog review: impact/<g>.json new_questions[].gating_rows
for g in ['F1a', 'F1b', 'F2a', 'F2b', 'F3', 'F45D']:
    for q in json.load(open(os.path.join(O, 'brennan_catalog_20261001', 'impact', f'{g}.json'), encoding='utf-8')).get('new_questions') or []:
        for c in (q.get('gating_rows') or q.get('rows') or []):
            NEWQ[c].add(q['id'].replace('(new) ', ''))
qkind = {q['id']: q['kind'] for q in json.load(open(os.path.join(O, 'omi_apply_20260925', 'taskC', 'taskC_merged.json'), encoding='utf-8'))['questions']}
steps_have = {os.path.basename(p)[8:-4] for p in glob.glob(os.path.join(R, '09_STEP_FILES', 'BRENNAN_*.stp'))}


def qid(q):
    q = q if isinstance(q, str) else q.get('id', '')
    q = q.replace('(new) ', '')
    return re.split(r' - | \(', q)[0].strip()


OPT = {'Q-NEW-STDBUY', 'Q-NEW-PARKER4300', 'Q-CALIPER', 'Q-NEW-MS51531NUT', 'Q-MS-FG'}
ANSWERED = {'Q-NEW-ASME40': 'user 2026-10-02: Brennan-measured -40 threads accepted', 'Q-NEW-2702HOLD': 'batch 14b shipped 2702 / 2703',
            'Q-NEW-6802E45CHECK': 'tier-1 6802-E45 shipped (batch 14)', 'Q-NEW-BRENNANPN': 'catalog confirmed 0304-C'}
CAPAB = {'Q-NEW-ANGLEDHELIX': '45-deg leg thread (1503 1504 5501 5503 5505 6810 6902)', 'Q-NEW-PERLEGSW': 'several swivel / adj-ORB legs on one part',
         'Q-NEW-HOSEB': 'hose-barb elbow leg (4501 4503 4601 4603)', 'Q-NEW-FLG61LEG': 'code 61 flange leg on elbows (1703 1704)',
         'Q-NEW-ANGLEDFEMALE': 'female pipe port on the 45-deg leg (5505 1504)', 'Q-NEW-ANGLEDNUT': 'swivel nut on the 45-deg leg (6810 6902)',
         'Q-NEW-FLG62LEG': 'code 62 flange leg (1804)'}
SCOPE = {'Q-SCOPE-TUBE', 'Q-SCOPE-ORING', 'Q-NEW-ORINGSRC', 'Q-NEW-4005CODE'}


def classify(q):
    if q in OPT:
        return None
    if q in ANSWERED:
        return None
    if q.startswith('Q-NEWMASTER-') or q.startswith('Q-NEW-FOLD-') or q.startswith('Q-B-OTHER-') or q in ('Q-B-ELBOW', 'Q-B-TEE'):
        return 'MINE'
    if q in CAPAB:
        return 'CAPABILITY'
    if q in SCOPE:
        return 'SCOPE'
    return 'DECIDE'


# ---- batch-15 held rows (QA #169) and wave-1 results (NOTES.md of each family, 2026-10-02)
B15_HELD = {}
for c in ['2406-04-02', '2406-04-04', '2406-04-08', '2406-06-10', '2406-08-08', '2406-10-16', '2406-12-04', '2406-12-12',
          '5404-16-04', '5404-20-12', '5404-24-12', '5404-32-12', '5404-32-16', '5600-20-20-20-FG', '5600-24-24-24-FG']:
    B15_HELD[c] = {'Q-BRENNAN-ONLY'}
for c in ['6504-04-06', '6504-06-04', '6504-08-10', '6504-12-16']:
    B15_HELD[c] = {'Q-BRENNAN-ONLY|Q-NEW-CATRANK'}
for c in ['5406-P-02', '5406-P-04', '5406-P-06']:
    B15_HELD[c] = {'Q-BRENNAN-ONLY|Q-NEW-AWALIAS'}
B15_HELD['6600-24-24-24-FG'] = {'Q-BRENNAN-ONLY|Q-GARBLE'}
B15_HELD['2408-14-SOLID'] = {'Q-NEW-CATRANK'}
B15_HELD['6801-05-05-NWO-FG'] = {'Q-NEW-CATRANK|QUESTION-25'}
W1_READY = (['1502-08-08-FG', '1502-02-02-FG', '2501-LL-08-08-FG'] + [f'6500-L-{d}-{d}-FG' for d in ('04', '06', '08', '12', '16')]
            + ['2606-08-08-08-FG', '2611-06-06-06-FG', '2505-08-08-FG'] + [f'0304-C-{d}' for d in '03 04 05 06 08 10 12 14 16 20 24 32'.split()]
            + [f'0306-{d}' for d in '03 04 05 06 08 10 12 16 20 24 32'.split()]
            + ['5652-08-08-08-08-FG', '5603-08-08-08-FG', '5601-06-06-06-FG'] + [f'6408-HHP-{d}-O' for d in '05 10 12 16 20 24 32'.split()])
W1_2504 = '2504-'   # all 4 2504 rows build (-04 -06 -08 -12)
W1_BO = {}   # wave-1 rows prepared from Brennan only: gate set beyond Q-BRENNAN-ONLY
for d in ('06-06', '12-08', '12-12', '16-16', '20-20', '24-24', '32-32'):
    W1_BO[f'1502-{d}-FG'] = set()
for d in ('04-04', '06-04', '06-06', '12-12', '16-16', '20-20'):
    W1_BO[f'2501-LL-{d}-FG'] = set()
W1_BO_PREFIX = {'3474-': set(), '1724-': {'STEP'}, '1800-': {'STEP'}, '1824-': {'STEP'}, '5406-HHP-': set(), '5406-SHP-': set(),
                '5652-': {'Q-TRANSFER-TAPDRILL|STEP'}, '5603-': {'Q-TRANSFER-TAPDRILL|STEP'}, '5601-': {'Q-TRANSFER-TAPDRILL|STEP'},
                '6408-HHP-': {'STEP'}}
W1_PILOT_ONLY = {'1724-08', '1800-08-08', '1824-08'}     # these sizes have their pilot STEP; the others need their own STEP

rows = []
for x in unbuilt:
    c, t = x['cfg'], x['table']
    r = imp.get(c)
    gates, mine, notes = set(), set(), []
    src = ''
    if c in W1_READY or c.startswith(W1_2504):
        src = 'WAVE1-READY'
        mine.add('wave 1: SolidWorks dry run + merge + ship')
    elif c in B15_HELD:
        src = 'B15-HELD'
        gates |= B15_HELD[c]
    elif c in W1_BO or any(c.startswith(p) for p in W1_BO_PREFIX):
        src = 'WAVE1-BRENNAN-ONLY'
        gates.add('Q-BRENNAN-ONLY')
        extra = W1_BO.get(c)
        if extra is None:
            extra = next(v for p, v in W1_BO_PREFIX.items() if c.startswith(p))
        extra = set(extra)
        if 'STEP' in extra and c in W1_PILOT_ONLY:
            extra.discard('STEP')
        gates |= extra
        mine.add('wave 1: merge + SolidWorks dry run')
    elif x['status'] != 'MISSING':
        src = 'DATA-NO-MASTER'
    elif r is not None:
        src = 'IMPACT-' + r['new_bucket']
        for q in r.get('questions_still_open') or []:
            q = qid(q)
            k = classify(q)
            if k == 'MINE':
                mine.add(q)
            elif k:
                gates.add(q if k != 'CAPABILITY' else 'CAP:' + q)
        for q in NEWQ.get(c, ()):
            if q not in ('Q-NEW-CATRANK',) and not q.startswith('Q-B-OTHER'):
                gates.add(q)
        if c.startswith(('6801-L-', '6801-LL-')):
            gates.add('STEP:6801-L / -LL pilots (coming)')
        # catalog-only cells (impact treated the catalog as usable; Q-BRENNAN-ONLY is open since 2026-10-02)
        cells = [cl for cl in (r.get('cells') or []) if cl.get('needed', True)]
        bo = [cl for cl in cells if str(cl.get('omi_compare', '')).startswith('OMi gives no') and cl.get('agrees_with_airway') is None
              and str(cl.get('airway_compare', '')).lower().startswith('no air-way')]
        if bo:
            gates.add('Q-BRENNAN-ONLY' if not c.endswith('-FG') else 'Q-BRENNAN-ONLY|OWN-STEP')
        for s in r.get('steps') or []:
            if s.get('role', 'required' if s.get('pn') == c else 'reference') == 'required' and s.get('verdict') in ('partly', 'not_replaced') and not str(s.get('still_needed_for', '')).startswith('nothing'):
                if s['pn'] in steps_have:
                    mine.add('measure received STEP ' + s['pn'])
                else:
                    snf = str(s.get('still_needed_for', ''))
                    alt = sorted(set(re.findall(r'Q-[A-Z0-9-]*[A-Z0-9]', snf))) if ('only if' in snf or 'not needed at all' in snf) else []
                    gates.add('|'.join(['STEP:' + s['pn']] + alt))
        if r['new_bucket'] == 'WORK' and not mine:
            mine.add('generator work')
    else:
        src = 'NOT-IN-IMPACT'
    rows.append(dict(cfg=c, table=t, status=x['status'], source=src, bucket=(r or {}).get('new_bucket', ''),
                     gates=sorted(gates), mine=sorted(mine)))

# ---- the 88 rows with data and no master: reasons (PROJECT_STATUS section 3 + wave-1 notes)
DNM = {'0319': {'STEP:0319 (tube sleeve)', 'Q-SOP5'}, '1503': {'CAP:Q-NEW-ANGLEDHELIX'}, '2404L': {'OMI:2404 bores'}, '2404_FINAL': {'OMI:2404 bores'},
       '3051': {'STEP:3051'}, '4501': {'CAP:Q-NEW-HOSEB'}, '4601': {'CAP:Q-NEW-HOSEB'}, '4603': {'CAP:Q-NEW-HOSEB'},
       '5503': {'CAP:Q-NEW-ANGLEDHELIX'}, '5505': {'CAP:Q-NEW-ANGLEDFEMALE', 'CAP:Q-NEW-ANGLEDHELIX'}, '6400L': {'Q-HANDMADE'},
       '6801L': {'STEP:6801-L pilot (coming)'}, '6801LL': {'STEP:6801-LL pilot (coming)'}, '6805': {'STEP:6805 pilot (coming)'},
       '6806': {'STEP:6806 pilot (coming)'}, '6807': {'STEP:6807 pilot (coming)', 'CAP:Q-NEW-PERLEGSW'},
       '6901': {'STEP:6901 pilot (coming)'}, '6902': {'STEP:6902 pilot (coming)', 'CAP:Q-NEW-ANGLEDNUT'}}
DNM_ROW = {'1501-04-02-FG': {'BLOCKED: bore vs -02 stem tip'}, '1501-24-24-FG': {'DECIDE: Air-Way nut 1.88 vs Brennan 2.125'},
           '1502-04-04-FG': {'BLOCKED: generator (body face inside the hex corner)'}, '2406-16-04': {'BLOCKED: port wall'},
           '2702-12-12-FG-LN': {'BLOCKED: bore vs JIC tip'}, '6405-32-24-O': {'STEP:6405-32-24-O (Air-Way D3 misprint)'},
           '6802-04-06-NWO-FG': {'DECIDE: Air-Way nut hex 0.56 for a -06 ORB'}}
for row in rows:
    if row['source'] != 'DATA-NO-MASTER':
        continue
    g = DNM_ROW.get(row['cfg']) or DNM.get(row['table']) or {'?'}
    row['gates'] = sorted(g)
    row['mine'] = ['generator / new master work'] if any(s.startswith('CAP:') for s in g) or row['table'] in ('0319', '3051', '6801L', '6801LL', '6805', '6806', '6807', '6901', '6902') else []

with open(os.path.join(HERE, 'rows.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['config', 'table', 'status', 'source', 'impact_bucket', 'user_gates', 'my_work'])
    for r in rows:
        w.writerow([r['cfg'], r['table'], r['status'], r['source'], r['bucket'], ' ; '.join(r['gates']), ' ; '.join(r['mine'])])

# ---- summary
out = []
p = out.append
p(f'unbuilt BUILD rows: {len(rows)}  by status {dict(collections.Counter(r["status"] for r in rows))}')
p(f'by source {dict(collections.Counter(r["source"] for r in rows))}')


def family(g):
    if g.startswith('STEP:') or g in ('STEP', 'OWN-STEP'):
        return 'STEP download'
    if g.startswith('CAP:'):
        return 'capability ' + g[4:]
    if g.startswith('OMI:'):
        return 'OMi answer'
    if g.startswith('BLOCKED') or g.startswith('DECIDE:'):
        return g.split(':')[0]
    return g


def alts(g):
    return frozenset(family(a) for a in g.split('|'))


AG = [[alts(g) for g in r['gates']] for r in rows]


def freed(done):
    return [i for i, gs in enumerate(AG) if all(a & done for a in gs)]


none_user = freed(set())
p(f'\nNO user action needed (only my work): {len(none_user)}  {dict(collections.Counter(rows[i]["source"] for i in none_user))}')
bo = freed({'Q-BRENNAN-ONLY'})
p(f'Q-BRENNAN-ONLY = yes ALONE makes {len(bo) - len(none_user)} more rows buildable (with my work): '
  f'{dict(collections.Counter(rows[i]["source"] for i in bo if i not in none_user))}')
p('  by table: ' + str(dict(collections.Counter(rows[i]['table'] for i in bo if i not in none_user).most_common())))
p(f'  Q-BRENNAN-ONLY is one of the gates (or an alternative) of {sum(1 for gs in AG if any("Q-BRENNAN-ONLY" in a for a in gs))} rows')
fams = collections.Counter()
for gs in AG:
    for f in (set().union(*gs) if gs else set()):
        fams[f] += 1
p('\nrows touched per user action (a row can need several):')
for f, n in fams.most_common(45):
    p(f'  {n:4}  {f:42}  alone frees {len(freed({f})) - len(none_user)}')
p('\ngreedy order (each step = the action that frees the most rows given the earlier ones; all STEP downloads pooled):')
done = set()
cur = len(none_user)
p(f'  start: {cur} rows need no user action')
for _ in range(25):
    best, bn = None, cur
    for f in fams:
        if f in done:
            continue
        n = len(freed(done | {f}))
        if n > bn:
            best, bn = f, n
    if not best:
        break
    done.add(best)
    p(f'  + {best:42} frees {bn - cur:4}  (cumulative {bn})')
    cur = bn
left = [rows[i] for i, gs in enumerate(AG) if not all(a & done for a in gs)]
p(f'  still blocked after those: {len(left)}; their gates: ' + str(collections.Counter(f for r in left for g in r['gates'] for f in alts(g)).most_common(25)))
s = '\n'.join(out)
print(s)
open(os.path.join(HERE, 'summary.txt'), 'w', encoding='utf-8').write(s + '\n')
