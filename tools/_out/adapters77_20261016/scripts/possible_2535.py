"""possible_2535.py (2026-10-18): how much of OMi's carbon-steel catalog (2,535 parts) is looked at, possible now, and possible in
theory with Brennan's catalogs ("spec sheets") as a dimension source. Read-only; prints a summary and writes ../possible_2535.json.

Inputs: tools/_out/unblock_20261008/rows.csv (the 763 unbuilt BUILD rows of the 1,804 with their user gates, 2026-10-08),
re-judged with the decisions taken since (s5): Q-TRANSFER-ENDLIB yes, the 6 capabilities yes, Q-SCOPE-TUBE / -ORING yes, O-ring
sizes from Air-Way (4000 / 4001 have data), Q-BRENNAN-ONLY NO (2026-10-08) and the own-file rule on hold. New-scope rows that need
OMi's sizes are set to OMi (bent tubes, 4005, 6701, 0618 / 0619). Then the parts outside the 1,804: the 77 dropped adapters
(adapters77_20261016/rows77.json), the 385 ORFS (orfs_airway_20261015/compare_orfs.json, website list), 230 compression and 12 test
gauge (07_RAW_EXTRACTS/omi_feed), checked against the Brennan catalog parse of 2026-10-01 (catalog_verified.json, 5,056 rows)."""
import csv, json, os, re, collections

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
O = lambda *p: os.path.join(ROOT, *p)
cat = json.load(open(O('tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json'), encoding='utf-8'))
BPN = {re.sub(r'\s+', '', r['pn']).upper() for t in cat['tables'] for r in t['rows']}


def in_brennan(pn):
    k = re.sub(r'\s+', '', str(pn)).upper()
    cands = {k, k.replace('-TUBE', ''), k.replace('-ASY', ''), k + '-FG', k.replace('-FG', ''), re.sub(r'-LN(-|$)', r'\1', k)}
    return any(c in BPN for c in cands)


def gate_kind(g):
    alts = [a.strip() for a in g.split('|') if a.strip()]
    order = {'decided': 0, 'step': 1, 'decide': 2, 'brennan': 3, 'omi': 4, 'blocked': 5}
    def one(a):
        if a.startswith('CAP:') or a.startswith('capability ') or a in ('Q-TRANSFER-ENDLIB', 'Q-SCOPE-TUBE', 'Q-SCOPE-ORING', 'Q-NEW-ORINGSRC'):
            return 'decided'
        if a == 'STEP' or a.startswith('STEP:') or a == 'STEP download':
            return 'step'
        if a in ('Q-BRENNAN-ONLY', 'OWN-STEP'):
            return 'brennan'
        if a == 'OMi answer' or a.startswith('Q-NEW-4005'):
            return 'omi'
        if a == 'BLOCKED':
            return 'blocked'
        return 'decide'
    return min((one(a) for a in alts), key=lambda x: order[x]) if alts else 'decided'


def main():
    out = collections.OrderedDict()
    # ---- A. the 1,804 BUILD rows of the existing review tables
    rows = list(csv.DictReader(open(O('tools', '_out', 'unblock_20261008', 'rows.csv'), encoding='utf-8-sig')))
    A = collections.Counter()
    for r in rows:
        tab, cfg = r['table'], r['config']
        ks = {gate_kind(g) for g in r['user_gates'].split(';') if g.strip()} - {'decided'}
        if tab in ('4000', '4001'):
            t = 'data now (Air-Way O-rings, master staged)'
        elif tab == '4005' or (tab in ('1703', '1704', '1803', '1804') and cfg.endswith('-Tube')) or tab in ('6701', '0618', '0619'):
            # new scope: no Air-Way sizes; Brennan prints its swept elbows without the -Tube suffix
            t = ('BRENNAN: possible only with Brennan data (catalog prints it)' if in_brennan(cfg) else 'needs OMi (new scope: no Air-Way sizes)')
        elif not ks:
            t = 'data / my work only' if r['status'] == 'DATA' else 'my work only (staged or to generate)'
        elif ks <= {'step'}:
            t = 'needs your STEP downloads (shape)'
        elif ks <= {'step', 'decide'}:
            t = 'needs your decisions (+ downloads)'
        elif 'brennan' in ks and ks <= {'step', 'decide', 'brennan'}:
            t = 'BRENNAN: possible only with Brennan data' + (' (catalog prints it)' if in_brennan(cfg) else ' (Brennan 3D file only)')
        elif 'omi' in ks:
            t = 'needs OMi'
        else:
            t = 'blocked: ' + ','.join(sorted(ks))
        A[t] += 1
    out['A_1804'] = dict(built=1041, unbuilt=dict(A))
    # ---- B. the 77 dropped adapters
    R77 = json.load(open(O('tools', '_out', 'adapters77_20261016', 'rows77.json'), encoding='utf-8'))
    B = collections.Counter('data (staged, wrongly DROP)' if r['row'] else ('BRENNAN: catalog prints it' if r['brennan'] else 'no source (OMi only)') for r in R77)
    out['B_77'] = dict(B)
    # ---- C. ORFS on the website
    C = json.load(open(O('tools', '_out', 'orfs_airway_20261015', 'compare_orfs.json'), encoding='utf-8'))
    Cw = [r for r in C if r.get('on_website')]
    Cc = collections.Counter()
    for r in Cw:
        if r['status'] in ('VERIFIED', 'ASSUMED'):
            Cc['data (staged; needs the ORFS model type + STEPs)'] += 1
        else:
            Cc['BRENNAN: catalog prints it' if (r.get('brennan_rows') or in_brennan(r['omi_pn'])) else 'no source (OMi only)'] += 1
    out['C_ORFS'] = dict(Cc)
    # ---- D. compression, test gauge
    for name, f in (('D_compression', 'omi_skus_compression.txt'), ('E_testgauge', 'omi_skus_testgauge.txt')):
        sk = [s.strip() for s in open(O('07_RAW_EXTRACTS', 'omi_feed', f), encoding='utf-8') if s.strip() and not s.startswith('#')]
        out[name] = dict(collections.Counter('BRENNAN: catalog prints it' if in_brennan(s) else 'no source (OMi only)' for s in sk))
    out['F_kits'] = {'out of scope (kits)': 30}
    json.dump(out, open(O('tools', '_out', 'adapters77_20261016', 'possible_2535.json'), 'w', encoding='utf-8'), indent=1)
    for k, v in out.items():
        print(k, json.dumps(v))
    tot = collections.Counter()
    tot['built'] = 1041
    for grp in ('B_77', 'C_ORFS', 'D_compression', 'E_testgauge', 'F_kits'):
        for k, n in out[grp].items():
            tot[k.split(' (')[0] if k.startswith(('data', 'BRENNAN', 'no source', 'out of')) else k] += n
    for k, n in out['A_1804']['unbuilt'].items():
        tot['BRENNAN' if k.startswith('BRENNAN') else k] += n
    print('ALL', sum(tot.values()), dict(tot))


if __name__ == '__main__':
    main()
