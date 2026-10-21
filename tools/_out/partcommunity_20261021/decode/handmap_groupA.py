"""handmap_groupA.py (2026-10-21): the by-hand mapping aid for the group-A columns map_groupA.py could not settle (user: "why can't you
finish the non-fs parts?"). For each family and each column still empty on its not-ready rows, compare every Brennan record code with the
Air-Way value of the SAME SIZE over all sizes (Air-Way's own -FG row when it prints one, else the plain row the forged part was
near-matched to): median |difference|, spread, sizes compared. Prints a ranked table per column; the decisions taken from it are written
by hand into HANDMAP (below) with the reason, and only those become proposals (proposals_H.csv -> verify_proposals.py -> verify_H.csv).
Rule (user 2026-10-21): Brennan values fill EMPTY cells only, Air-Way first, marked BRENNAN."""
import os, re, csv, json, glob, statistics, collections, sys
import openpyxl

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
isnum = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
cache = json.load(open(os.path.join(PC, 'cache.json')))
NOT_READY = {norm(l) for l in open(J('tools', '_out', 'sources_20261021', 'not_ready_1022.txt')) if l.strip()}
dsh = lambda p: tuple(re.findall(r'-(\d\d)(?=-|$)', p))
BASE = J('tools', '_out', 'airway_first_20261020', 'stage', '04_DESIGN_TABLES')

# ---- decisions taken by hand from the printed comparison (filled below after reading it) ----
HANDMAP = {   # (table, column) -> (code, reason); from the printed comparison (median |Brennan - Air-Way| over n sizes) + Brennan's catalog letters
    ('6807', 'M7_1@DRIVE'): ('M1', 'Brennan M1 LGTH; = Air-Way on all 3 sizes'), ('6807', 'M7_2@DRIVE'): ('M2', 'Brennan M2 LGTH; = Air-Way, 3 sizes'),
    ('6807', 'C4_1HEX@HEX'): ('C', 'Brennan C HEX (end 1); 3 sizes'), ('6807', 'C4_2HEX@HEX'): ('C2', 'Brennan C2 HEX (end 2); 3 sizes'),
    ('6807', 'Y@HEX'): ('Y', 'Brennan Y FLATS'), ('6807', 'D1@BORE'): ('B1D', 'Brennan B1 DRILL'), ('6807', 'D2@BORE'): ('B2D', 'Brennan B2 DRILL'),
    ('6807', 'THDMAJ_B1@DRIVE'): ('B1THD', 'thread B1, exact'), ('6807', 'THDMAJ_B2@DRIVE'): ('B2THD', 'thread B2, exact'),
    ('6803', 'LEG1@DRIVE'): ('M1', 'Brennan M1 LGTH; = Air-Way on 8 sizes'), ('6803', 'LEG2@DRIVE'): ('M2', 'Brennan M2 LGTH; 8 sizes'),
    ('6803', 'LEG3@DRIVE'): ('M7', 'Brennan M7 LGTH (ORB leg); exact on 8 sizes'), ('6803', 'HEXB@HEX'): ('C', 'Brennan C HEX; 8 sizes'),
    ('6803', 'Y@REF'): ('Y', 'Brennan Y FLATS; 8 sizes'), ('6803', 'THDMAJ_1@DRIVE'): ('B1THD', 'exact'), ('6803', 'THDMAJ_2@DRIVE'): ('B2THD', 'exact'),
    ('6803', 'THDMAJ_3@DRIVE'): ('B3THD', 'exact'), ('6803', 'D1@BORE'): ('B1D', 'Brennan B1 DRILL'), ('6803', 'D2@BORE'): ('B2D', 'Brennan B2 DRILL'),
    ('6803', 'D3@BORE'): ('B3D', 'Brennan B3 DRILL'),
    ('5602', 'N@DRIVE'): ('N', 'Brennan N LGTH; exact'), ('5602', 'N1_2@DRIVE'): ('N1', 'Brennan N1 LGTH (leg 2); exact'),
    ('5602', 'N1_3@DRIVE'): ('N2', 'Brennan N2 LGTH (leg 3); exact'), ('5602', 'WY@REF'): ('Y', 'Brennan Y FLATS'), ('5602', 'D@BORE'): ('A1D', 'Brennan A1 DRILL'),
    ('5602', 'THDMAJ_A1@DRIVE'): ('ATHD', 'equal-dash parts: all three pipe majors equal'), ('5602', 'THDMAJ_A2@DRIVE'): ('A2THD', 'exact'),
    ('5602', 'THDMAJ_A3@DRIVE'): ('A3THD', 'exact'),
    ('5604', 'N1_1@DRIVE'): ('N1', 'Brennan N1 LGTH; exact on 4 sizes'), ('5604', 'N1_2@DRIVE'): ('N2', 'Brennan N2 LGTH; exact'),
    ('5604', 'N@DRIVE'): ('N', 'Brennan N LGTH; exact'), ('5604', 'W@HEX'): ('Y', 'Brennan Y FLATS'), ('5604', 'D@BORE'): ('A3D', 'Brennan A3 DRILL (male end)'),
    ('5604', 'THDMAJ_A1@DRIVE'): ('THD1', 'equal-dash parts'), ('5604', 'THDMAJ_A2@DRIVE'): ('THD1', 'equal-dash parts'),
    ('5604', 'THDMAJ_A3@DRIVE'): ('THD3', 'equal-dash parts'),
    ('6503', 'N1@DRIVE'): ('M2', 'Brennan M2 LGTH; exact on 4 sizes'), ('6503', 'M5@DRIVE'): ('M6', 'Brennan M6 LGTH; 0.025 from the plain Air-Way part'),
    ('6503', 'M10@DRIVE'): ('M4', 'Brennan M4 LGTH; 0.015'), ('6503', 'C3HEX@HEX'): ('C', 'Brennan C HEX'), ('6503', 'Y1@HEX'): ('Y', 'Brennan Y FLATS'),
    ('6503', 'D@BORE'): ('BD', 'Brennan B DRILL'), ('6503', 'THDMAJ_A@DRIVE'): ('ATHD', 'exact'), ('6503', 'THDMAJ_B@DRIVE'): ('BTHD', 'exact'),
    ('6902', 'CHEX@HEX'): ('C1', 'Brennan C1 HEX (swivel nut); exact on 9 sizes'), ('6902', 'C4HEX@HEX'): ('C', 'Brennan C HEX (lock nut)'),
    ('6902', 'D1@BORE'): ('BD', 'Brennan B DRILL'), ('6902', 'D@BORE'): ('AD', 'Brennan A DRILL'), ('6902', 'THDMAJ_B@DRIVE'): ('BTHD', 'ORB thread, exact'),
}
# not mapped, on purpose: 6902 N4 / M / W2 (forged lengths differ from the plain Air-Way part by 0.08-0.15 and the letters differ - needs
# the two catalog drawings), 6902 C1HEX (Air-Way's third hex; Brennan prints two), pipe majors where Air-Way and Brennan use different
# definitions (6902 A1: pipe OD 0.54 vs NPSM major 0.526) - the end library / generator supplies those.
A5 = {'6803': ('ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE', 'ORB_GRVW@DRIVE')}   # A5: adjustable-ORB end values from the table's own rows of the same ORB size


def rec(p):
    a = cache.get(p)
    if not a or 'mident' not in a:
        return None
    out = {}
    for k, x in re.findall(r'\{([A-Z0-9_]+)=([^{}]*)\}', a['mident']):
        try:
            f = float(x)
        except ValueError:
            continue
        if f > 0 and k not in ('DN', 'FONTSIZE', 'WEIGHT', 'PITCH', 'PITCH2', 'LINEID', 'GX', 'OD'):
            out[k] = f
    return out


def table(root):
    ws = openpyxl.load_workbook(os.path.join(BASE, f'DesignTable_{root}.xlsx'), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True)); hi = next(i for i, r in enumerate(rows[:6]) if r and '$PRP@PartNo' in r)
    return rows[hi], [dict(zip(rows[hi], r)) for r in rows[hi + 1:] if r and r[0]]


def compare(root):
    head, data = table(root)
    targets = [d for d in data if norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo')) in NOT_READY and str(d.get('$PRP@ScopeAction')).upper() == 'BUILD'
               and rec(norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo')))]
    cols = [c for c in head[1:] if c and not str(c).startswith('$') and any(not isnum(d.get(c)) for d in targets)]
    # Air-Way reference per size: an Air-Way -FG row first, else the plain row
    ref = {}
    for d in data:
        p = norm(d.get('$PRP@PartNo') or '')
        if 'AIR-WAY' not in str(d.get('$PRP@AxialSource') or '').upper():
            continue
        k = dsh(p)
        if k not in ref or '-FG' in p:
            ref[k] = d
    # Brennan records of every size of this family that Air-Way prints (not only the targets): more sizes = better evidence
    fam_parts = {}
    for d in data:
        p = norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo'))
        r = rec(p) or rec(p + '-FG') or rec(p + '-NWO-FG') or (rec(p.replace(' ', '')) if ' ' in p else None)
        if r:
            fam_parts[dsh(p)] = r
    out = {}
    for c in cols:
        # per column: only Air-Way rows that print a value in it (the OMi -FG rows mention Air-Way in their note but are empty)
        refc = {}
        for d in data:
            p = norm(d.get('$PRP@PartNo') or '')
            if isnum(d.get(c)) and 'AIR-WAY' in str(d.get('$PRP@AxialSource') or '').upper() and (dsh(p) not in refc or '-FG' in p):
                refc[dsh(p)] = d
        stats = []
        codes = sorted({k for r in fam_parts.values() for k in r})
        for k in codes:
            diffs = [fam_parts[s][k] - float(refc[s][c]) for s in fam_parts if s in refc and k in fam_parts[s]]
            if len(diffs) >= 2:
                stats.append((statistics.median(abs(x) for x in diffs), statistics.pstdev(diffs), len(diffs), k))
        stats.sort()
        out[c] = stats[:4]
    return targets, out


if __name__ == '__main__' and len(sys.argv) > 1:
    for root in sys.argv[1:]:
        t, out = compare(root)
        print(f'== {root}: {len(t)} target rows')
        for c, st in out.items():
            print(f'  {c:18}', '  '.join(f'{k}: med {m:.3f} sd {s:.3f} n{n}' for m, s, n, k in st))


def proposals():
    props = []
    for root in sorted({t for t, c in HANDMAP} | set(A5)):
        head, data = table(root)
        for d in data:
            p = norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo'))
            r = rec(p)
            if p not in NOT_READY or str(d.get('$PRP@ScopeAction')).upper() != 'BUILD' or not r:
                continue
            for (t, c), (k, why) in HANDMAP.items():
                if t == root and c in head and not isnum(d.get(c)) and k in r:
                    props.append(dict(root=root, part=p, column=c, value=r[k], code=k, evidence=f'hand map: {why}', row_status=d.get('$PRP@DataStatus') or ''))
            for c in A5.get(root, ()):
                if c in head and not isnum(d.get(c)):
                    me = dsh(p)
                    src = next((q for q in data if isnum(q.get(c)) and dsh(norm(q.get('$PRP@PartNo') or '')) and
                                dsh(norm(q.get('$PRP@PartNo') or ''))[-1] == me[-1]), None)
                    if src is not None:
                        props.append(dict(root=root, part=p, column=c, value=src[c], code='A5',
                                          evidence=f"A5: same ORB size row {norm(src.get('$PRP@PartNo'))}", row_status=d.get('$PRP@DataStatus') or ''))
    with open(os.path.join(H, 'proposals_H.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(props[0])); w.writeheader(); w.writerows(props)
    print(len(props), 'cells in', len({x['part'] for x in props}), 'parts', collections.Counter(x['root'] for x in props))


if __name__ == '__main__' and len(sys.argv) == 1:
    proposals()
