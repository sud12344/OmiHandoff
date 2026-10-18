"""build_tables.py (2026-10-15): STAGED review tables for the OMi FS (ORFS) series - Air-Way dimensions, Brennan check in every row.

User 2026-10-15: "use airway dimensions, check brennan too". Inputs: compare_orfs.json (compare_orfs.py), the Air-Way passes, OMi's parts
file. Output: ../review_tables/DesignTable_<OMi series>.xlsx (NOT in 04_DESIGN_TABLES - nothing reads them yet; the ORFS end type does
not exist in the generators). Layout = the v1 review tables (e.g. DesignTable_0318.xlsx): title row, header row, one row per part.
  - columns: Air-Way's own letters in the catalog-letter convention (L6@DRIVE, S1HEX@HEX, D1@BORE, THDMAJ_D@DRIVE + $PRP@Thread_D ...)
  - rows: every FS part of that series in OMi's parts file; ScopeAction BUILD when it is on OMi's website ORFS list (two-pass list
    07_RAW_EXTRACTS/omi_feed/omi_skus_orfs.txt, else the single pass A list omi_orfs_website_passA.txt of 2026-10-16), else DROP
    (first version, before any website list existed: all BUILD, PROVISIONAL - the OMi website list could not be read on
    2026-10-15) + Air-Way rows OMi does not list (DROP) ; DataStatus from compare_orfs (VERIFIED / ASSUMED / MISSING)
  - where Brennan differs the row is built to Air-Way (ASSUMED) with Brennan's value in $COMMENT (PROJECT_STATUS s6 convention)
python -I build_tables.py"""
import json, os, re, sys, datetime
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import load
from compare_orfs import PAIRS, NO_AIRWAY, FORGED_AW, FORGED_BR, FG_USER, dashes, parse_num
FORGED_NONE = ('FS1704', 'FS1804', 'FS2502', 'FS2601', 'FS6503', 'FS7202')     # forged series with no Air-Way non-forged series

TODAY = datetime.date.today().isoformat()
OUT = os.path.join(load.HERE, 'review_tables')
USER = '[user 2026-10-15: "use airway dimensions, check brennan too"]'
WEBNOTE = 'not checked: the OMi website list could not be read on 2026-10-15 (store rate limit) - scope from OMi parts file'
_ws = os.path.join(load.HERE, 'website_source.json')
WEB_SRC = json.load(open(_ws, encoding='utf-8'))['source'] if os.path.exists(_ws) else None
TYPOS = {}            # Air-Way row pn -> {thread column: (printed, usual)} (thread_typos, filled in main)
ONWEB = {}            # OMi part -> True / False / None (filled in main from compare_orfs.json)


def scope_of(pn):
    """(ScopeAction, $PRP@OnWebsite, $PRP@OMiSKU, comment prefix) of an OMi-file part: the OMi website decides which parts exist"""
    w = ONWEB.get(pn)
    if w is None:
        return 'BUILD', WEBNOTE, pn, ''
    if w:
        return 'BUILD', f'yes - {WEB_SRC}', pn, ''
    return 'DROP', f'no - {WEB_SRC}', None, f'DROP: in OMi\'s parts file but NOT on OMi\'s website ({WEB_SRC}) | '


def tag(c):
    t = re.sub(r'\((\d)\)', r'_\1', c.upper())
    return re.sub(r'[^A-Z0-9_]', '', t)


def colname(c):
    """Air-Way display name -> review-table column (catalog-letter convention)"""
    if re.search(r'UN/UNF|NPTF', c):
        return ('THREAD', tag(c.split(' UN')[0].split(' NPTF')[0].strip()))
    if c.upper().replace('.', '') in ('TUBE OD', 'OD'):
        return ('PRP', 'TubeOD')
    if c == 'Style':
        return ('PRP', 'Style')
    if c == 'W/HOLE':
        return ('DIM', 'WHOLE@BORE')
    if c == 'TAP DRILL':
        return ('DIM', 'TAPDRILL@BORE')
    if re.match(r'^S\d*(\s*\(\d\))?(\s*HEX)?$', c) or c == 'C2' or c == 'NUT S (FF318)':
        return ('DIM', ('NUT' if c.startswith('NUT') else tag(c.replace(' HEX', ''))) + 'HEX@HEX')
    if re.match(r'^[dD]\d*(\s*\(\d\))?$', c) and c.lower() != 'd8':
        return ('DIM', tag(c) + '@BORE')
    return ('DIM', tag(c) + '@DRIVE')


def thread_major(s):
    """major dia (in) of a UN / UNF callout '9/16-18', '1 3/16-12', '1-14' (pipe threads get no THDMAJ column: their nominal is not the OD)"""
    m = re.fullmatch(r'\s*(?:(\d+)[ -])?(\d+)/(\d+)-(\d+)\s*', s or '') or re.fullmatch(r'\s*(\d+)()()-(\d+)\s*', s or '')
    if not m:
        return None
    whole = int(m.group(1) or 0)
    frac = int(m.group(2)) / int(m.group(3)) if m.group(2) else 0.0
    return round(whole + frac, 4)


def thread_typos(A, codes):
    """Air-Way thread callouts that are printing slips (2026-10-16, plan D1) -> {Air-Way row pn: {column: (printed, usual)}}.
    Same-source consistency, no voting between sources: in each thread column the callout follows one dash of the part number (the
    dash position that explains the most rows); a row is a slip when its callout differs from what Air-Way prints for that dash in the
    same series (seen >= 2 times) or, where the series has no second row of that dash, in the same kind of column across all ORFS
    series (d = face seal, n = straight thread, B = JIC; seen >= 3 times). Only the THDMAJ cell is affected (left empty, noted)."""
    from compare_orfs import norm_thread
    import collections
    glob_ = collections.defaultdict(collections.Counter)
    plan = []
    for code in codes:
        aw = A[code]
        rows = [(r['pn'], dashes(r['pn']), r['values']) for r in aw['rows']]
        for col in [c for c in aw['cols'] if re.search(r'UN/UNF', c)]:
            cand = []
            for pos in range(max((len(d) for _, d, _ in rows), default=0)):
                m = collections.defaultdict(collections.Counter)
                for pn, d, v in rows:
                    if pos < len(d) and v.get(col):
                        m[d[pos]][norm_thread(v[col])] += 1
                cand.append((sum(c.most_common(1)[0][1] for c in m.values()), pos, m))
            if not cand:
                continue
            top = max(c[0] for c in cand)
            idx = re.search(r'\(\s*(\d)\s*\)', col)              # d(2) / d (2): the 2nd dash breaks a tie (equal-dash tees / crosses)
            pick = [c for c in cand if c[0] == top and idx and c[1] == int(idx.group(1)) - 1]
            best = pick[0] if pick else next(c for c in cand if c[0] == top)
            kind = col.strip()[0]
            for dash, cnt in best[2].items():
                glob_[(kind, dash)].update(cnt)
            plan.append((code, col, kind, best[1], best[2], rows))
    out = {}
    for code, col, kind, pos, m, rows in plan:
        for pn, d, v in rows:
            if pos >= len(d) or not v.get(col):
                continue
            t = norm_thread(v[col])
            usual, n = m[d[pos]].most_common(1)[0]
            if n < 2 or usual == t:
                usual, n = glob_[(kind, d[pos])].most_common(1)[0]
                if n < 3:
                    continue
            if t != usual:
                out.setdefault(pn, {})[col] = (v[col], usual)
    return out


def val(s):
    p = parse_num(s)
    if p is None:
        return (s or None)
    return float(p[0])


NUMTOL = re.compile(r'^\s*([0-9]*\.[0-9]+)\s*±\s*([0-9]*\.[0-9]+)\s*$')
MAT = {'CH (Buna-N)': 'Buna-N (nitrile), Air-Way compound CH', 'HK (Viton)': 'Viton (FKM), Air-Way compound HK',
       'CH (Hi-Temp)': 'Hi-Temp nitrile, Air-Way compound CH (Hi-Temp)'}


def oring_table(A, O, C):
    """FS4000 = Buna O-rings for face-seal ends, in the layout of the staged 4000 O-ring table (newtypes_20261014/review_tables)"""
    aw = A['AWs40']
    hdr = [None, 'ID@DRIVE', 'W@DRIVE', '$PRP@TubeOD', '$PRP@PartNo', '$PRP@Material', '$PRP@Hardness', '$PRP@Temperature', '$PRP@Tolerance',
           '$PRP@DataStatus', '$PRP@AxialSource', '$COMMENT', '$PRP@ScopeAction', '$PRP@OMiSKU', '$PRP@OnWebsite']
    src = (f'Air-Way s40 only (O-Ring For SAE J1453/2/3 Face Seal Ends; double-pass {len(aw["rows"])} rows, parts.air-way.com/api/series/40 '
           f'fetched twice {TODAY}, identical); Air-Way part numbers FF4000-n {USER}')
    rows, used = [], set()
    for pn in sorted(p for p, r in O.items() if str(r.get('Series')) == 'FS4000'):
        c = C.get(pn, {})
        r = next((x for x in aw['rows'] if x['pn'] in (c.get('airway_rows') or [])), None)
        sc, wn, sku, pre = scope_of(pn)
        if r is None:
            rows.append([pn, None, None, None, pn, None, None, None, None, 'MISSING', 'no Air-Way FF4000 row of this size', pre + str(c.get('reason')), sc, sku, wn])
            continue
        used.add(r['pn'])
        v = r['values']
        (idv, idt), (wv, wt) = (NUMTOL.match(v['I.D.']).groups(), NUMTOL.match(v['W']).groups())
        rows.append([pn, float(idv), float(wv), v['TUBE OD'], pn, MAT[v['Type']], v['Shore Hardness'].replace('  ', ' '), v['Temperature'],
                     f'I.D. +/-{idt}, W +/-{wt} (Air-Way)', 'ASSUMED', src,
                     pre + f'Air-Way {r["pn"]} | OMi parts file row {O[pn]["_row"]}: "{O[pn].get("Part Description")}" (no sizes) | same model type as the '
                     '4000 O-ring master (fold in when the O-rings ship)', sc, sku, wn])
    for r in aw['rows']:
        if r['pn'] in used:
            continue
        v = r['values']
        (idv, idt), (wv, wt) = (NUMTOL.match(v['I.D.']).groups(), NUMTOL.match(v['W']).groups())
        rows.append([f'AWs40:{r["pn"]}', float(idv), float(wv), v['TUBE OD'], None, MAT.get(v['Type'], v['Type']), v['Shore Hardness'].replace('  ', ' '),
                     v['Temperature'], f'I.D. +/-{idt}, W +/-{wt} (Air-Way)', 'ASSUMED', src,
                     f'DROP: Air-Way row with no matching OMi part in OMi\'s parts file ({TODAY}) - OMi lists only the Buna FS4000', 'DROP', None, None])
    return hdr, rows


def main():
    os.makedirs(OUT, exist_ok=True)
    A, O = load.airway(), load.omi_file()
    C = {r['omi_pn']: r for r in json.load(open(os.path.join(load.HERE, 'compare_orfs.json'), encoding='utf-8'))}
    ONWEB.update({k: v.get('on_website') for k, v in C.items()})
    global TYPOS
    TYPOS = thread_typos(A, sorted({p['aw'] for p in PAIRS.values() if p['aw'] != 'AWs40'} | set(FORGED_AW.values())))
    json.dump(TYPOS, open(os.path.join(load.HERE, 'thread_slips.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    summary = []
    for ser in list(PAIRS) + list(NO_AIRWAY) + list(FORGED_AW) + list(FORGED_NONE):
        forged = ser in FORGED_AW or ser in FORGED_NONE
        P = PAIRS.get(ser) or (dict(aw=FORGED_AW[ser], br=[FORGED_BR[ser]], aw_ln=('-LN' in ser),
                                    note=f'forged (-FG): the Air-Way NON-forged series {FORGED_AW[ser]} is used only where Brennan {FORGED_BR[ser]} '
                                         'prints the same value in every compared cell (user 2026-10-15); forged body shape from Brennan (shape only)')
                               if ser in FORGED_AW else None)
        if ser == 'FS4000':
            hdr, rows = oring_table(A, O, C)
            nb = sum(1 for r in rows if r[12] == 'BUILD')
            st = {s: sum(1 for r in rows if r[12] == 'BUILD' and r[9] == s) for s in ('VERIFIED', 'ASSUMED', 'MISSING')}
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Sheet1'
            ws.append([f'OMi FS4000 Buna O-Ring (face-seal ends) - review table STAGED {TODAY} (not in 04_DESIGN_TABLES) | AW s40 double-pass | '
                       f'{nb} BUILD rows = on OMi\'s website ({WEB_SRC or "website NOT read - scope from OMi parts file, PROVISIONAL"}) | ' +
                       ', '.join(f'{k} {v}' for k, v in st.items())])
            ws.append(hdr)
            for r in rows:
                ws.append(r)
            p = os.path.join(OUT, 'DesignTable_FS4000.xlsx')
            wb.save(p)
            summary.append(dict(series=ser, airway='AWs40', build=nb, drop=len(rows) - nb, **st, file=os.path.relpath(p, load.ROOT)))
            print(f'{ser:<10} AW AWs40     BUILD {nb:>3} DROP {len(rows) - nb:>3}  {st}')
            continue
        omi = sorted(p for p, r in O.items() if str(r.get('Series')) == ser)
        if not omi:
            continue
        aw = A[P['aw']] if P and P['aw'] in A else None
        cols = [c for c in (aw['cols'] if aw else [])]
        if ser == 'FS2406':
            cols = cols + ['NUT S (FF318)']
        kinds = [colname(c) for c in cols]
        dimcols = [(c, k[1]) for c, k in zip(cols, kinds) if k[0] == 'DIM']
        thrcols = [(c, k[1]) for c, k in zip(cols, kinds) if k[0] == 'THREAD']
        prpcols = [(c, k[1]) for c, k in zip(cols, kinds) if k[0] == 'PRP']
        hdr = ([None] + [n for _, n in dimcols] + [f'THDMAJ_{t}@DRIVE' for c, t in thrcols if 'NPTF' not in c] + [f'$PRP@{n}' for _, n in prpcols] +
               [f'$PRP@Thread_{t}' for _, t in thrcols] +
               ['$PRP@PartNo', '$PRP@Description', '$PRP@DataStatus', '$PRP@AxialSource', '$COMMENT', '$PRP@ScopeAction', '$PRP@OMiSKU', '$PRP@OnWebsite'])
        rows, used_aw = [], set()

        def row_for(pn, desc, values, status, source, comment, scope, sku, web=None, slips=None):
            v = values or {}
            thr = [v.get(c) for c, _ in thrcols]
            maj = [None if (slips and c in slips) else thread_major(t) for (c, _), t in zip(thrcols, thr) if 'NPTF' not in c]
            return ([pn] + [val(v.get(c)) for c, _ in dimcols] + maj + [v.get(c) for c, _ in prpcols] + thr +
                    [pn, desc, status, source, comment, scope, sku, web])

        for pn in omi:
            c = C.get(pn, {})
            desc = O[pn].get('Part Description')
            values = c.get('airway_values')
            if c.get('airway_rows'):
                used_aw.update(c['airway_rows'])
            if values:
                src = f'Air-Way {P["aw"]} (s{aw["sid"]}, double-pass {TODAY}, parts.air-way.com/api/series/{aw["sid"]}, two fetches identical) {USER}'
                if ser == 'FS2406':
                    src += '; nut hex NUTHEX = Air-Way FF318 tube nut S of the female dash (Air-Way sells FF2407 with an FF318 nut)'
                if c.get('brennan_rows'):
                    src += f'; checked against the Brennan ORFS catalog p{c.get("brennan_page")} {c["brennan_rows"][0]}'
                if forged:
                    src += f'; FORGED part: Air-Way NON-forged row {c["airway_rows"][0]}, used because Brennan\'s forged row matches every compared cell {FG_USER}'
            elif forged:
                src = ('not built: forged part ' + ('without an Air-Way non-forged series' if not P else 'where Air-Way and Brennan do not match on every cell') +
                       ' (user 2026-10-15: the rest stay MISSING)')
            else:
                src = 'no Air-Way row' + (f' ({P["aw"]} has no row of this size)' if P else '')
            cm = [c.get('reason', '')]
            slips = TYPOS.get(c['airway_rows'][0], {}) if values and c.get('airway_rows') else {}
            for col, (printed, usual) in slips.items():
                cm.append(f'Air-Way thread printing slip: {col} "{printed}" where Air-Way prints {usual} for this dash - THDMAJ left empty, '
                          'the thread comes from the end library by dash (plan D1)')
            if c.get('extra_note'):
                cm.append(c['extra_note'])
            if c.get('thread_note'):
                cm.append(c['thread_note'])
            if c.get('airway_alternatives'):
                cm.append('Air-Way also prints ' + ', '.join(x['pn'] for x in c['airway_alternatives']) + ' (same size)')
            if P and P.get('note'):
                cm.append(P['note'])
            if ser in NO_AIRWAY:
                cm.append(NO_AIRWAY[ser])
            cm.append(f'OMi parts file row {O[pn]["_row"]} (no dimensions)')
            sc, wn, sku, pre = scope_of(pn)
            rows.append(row_for(pn, desc, values, c.get('status', 'MISSING'), src, pre + ' | '.join(x for x in cm if x), sc, sku, wn, slips))
        if aw:                                   # Air-Way rows OMi does not list -> DROP (as the existing review tables do)
            for r in aw['rows']:
                if r['pn'] in used_aw or (P.get('aw_ln') is not None and ('-LN' in r['pn'].upper()) != P['aw_ln']):
                    continue
                if any(dashes(r['pn']) == dashes(p) for p in omi):
                    continue                     # an alternative printing of a size OMi lists (style / suffix)
                rows.append(row_for(f'{P["aw"]}:{r["pn"]}', None, r['values'], 'ASSUMED',
                                    f'Air-Way {P["aw"]} (s{aw["sid"]}, double-pass {TODAY})',
                                    f'DROP: Air-Way {"non-forged " if forged else ""}row with no matching OMi part in OMi\'s parts file ({TODAY})',
                                    'DROP', None))
        nb = sum(1 for r in rows if r[-3] == 'BUILD')
        st = {s: sum(1 for r in rows if r[-3] == 'BUILD' and r[hdr.index('$PRP@DataStatus')] == s) for s in ('VERIFIED', 'ASSUMED', 'MISSING')}
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Sheet1'
        ws.append([f'OMi {ser} - review table STAGED {TODAY} (not in 04_DESIGN_TABLES) | dimensions: ' +
                   (f'Air-Way {P["aw"]} s{aw["sid"]} double-pass, checked against the Brennan ORFS catalog' if aw else 'NO Air-Way source') +
                   f' | {nb} BUILD rows = on OMi\'s website ({WEB_SRC or "website NOT read - scope from OMi parts file, PROVISIONAL"}) | ' +
                   ', '.join(f'{k} {v}' for k, v in st.items())])
        ws.append(hdr)
        for r in rows:
            ws.append(r)
        p = os.path.join(OUT, f'DesignTable_{ser}.xlsx')
        wb.save(p)
        summary.append(dict(series=ser, airway=P['aw'] if P else None, build=nb, drop=len(rows) - nb, **st, file=os.path.relpath(p, load.ROOT)))
        print(f'{ser:<10} AW {str(P["aw"] if P else "-"):<9} BUILD {nb:>3} DROP {len(rows) - nb:>3}  {st}')
    json.dump(summary, open(os.path.join(load.HERE, 'review_tables_summary.json'), 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main()
