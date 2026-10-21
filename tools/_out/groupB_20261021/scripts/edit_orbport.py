"""edit_orbport.py: 6815 / 6832 / 6835 (adjustable male ORB x female ORB port elbow / tees) - skeleton tables -> dimension columns.
Source: the Brennan TFA catalog (p45 6815-NWO-FG, p61 6832-NWO-FG / 6835-NWO-FG; brennan_catalog_20261001/catalog_verified.json), cross-checked
against each part's Brennan CAD record (codes placed on the family STEPs with tools/measure/prof.py, crossing at the origin):
  6815-08-08-NWO-FG: ORB stud on -X 1.590 (M8), port face on +Y 0.880 (M6), body flats 1.062 (Y), locknut C, stud drill B1 0.391
  6832-08-08-08-NWO-FG: ports on +-X 0.880 (M1 / N2), stud on +Y 1.590 (M7)
  6835-08-08-08-NWO-FG: stud on -X 1.590 (M7), ports on +X / +Y 0.880 (M1 / M2)
A catalog value and its record value that differ by more than the print rounding -> the row is held (never picked). Port drill = Air-Way's
per-size female ORB port drill (A11 2026-10-18 Q-TRANSFER-D3: the 6404 / 6410 tables, majority per size; Brennan's 0.682 at -08 = Air-Way 0.68).
Thread majors = the ORB thread the part number names (end library)."""
import os, sys, re, json
import tabedit as T
sys.path.insert(0, os.path.join(T.A, 'tools_af', 'generators')); sys.path.insert(0, os.path.join(T.A, 'tools_af'))
os.environ.setdefault('OMI_ROOT', os.path.join(T.A, 'stage'))
import gen_straight2 as G

CAT = json.load(open(os.path.join(T.ROOT, 'tools', '_out', 'brennan_catalog_20261001', 'catalog_verified.json')))
PD = {4: 0.38, 6: 0.50, 8: 0.68, 10: 0.80, 12: 0.97, 16: 1.22, 20: 1.53, 24: 1.78}     # A11: Air-Way per-size port drill (6404 / 6410 majority)
# root: (catalog series, [(column, catalog key, record code)], port-drill columns by dash position, [(thread col, dash position)])
DEF = {'6815': ('6815-NWO-FG', [('M8@DRIVE', 'M8 LGTH', 'M8'), ('M6@DRIVE', 'M6 LGTH', 'M6'), ('D1@BORE', 'B1 DRILL', 'B1D'), ('CHEX@HEX', 'C HEX', 'C'),
                                ('Y@HEX', 'Y FLATS', 'Y')], [('PD@BORE', 1)], [('THDMAJ_B1@DRIVE', 0)]),
       '6832': ('6832-NWO-FG', [('M1@DRIVE', 'M1 LGTH', 'M1'), ('N2@DRIVE', 'N2 LGTH', 'N2'), ('M7@DRIVE', 'M7 LGTH', 'M7'), ('D3@BORE', 'B3 DRILL', 'B3D'),
                                ('CHEX@HEX', 'C HEX', 'C'), ('Y@HEX', 'Y FLATS', 'Y')], [('PD1@BORE', 0), ('PD2@BORE', 1)], [('THDMAJ_B3@DRIVE', 2)]),
       '6835': ('6835-NWO-FG', [('M7@DRIVE', 'M7 LGTH', 'M7'), ('M1@DRIVE', 'M1 LGH', 'M1'), ('M2@DRIVE', 'M2 LGTH', 'M2'), ('D1@BORE', 'B1 DRILL', 'B1D'),
                                ('CHEX@HEX', 'C HEX', 'C'), ('Y@HEX', 'Y FLATS', 'Y')], [('PD2@BORE', 1), ('PD3@BORE', 2)], [('THDMAJ_B1@DRIVE', 0)])}


def main():
    for root, (ser, mp, pdc, thc) in DEF.items():
        tab = [x for x in CAT['tables'] if x.get('series') == ser][0]; cat = {r['pn']: r['values'] for r in tab['rows']}
        t = T.Table(root); n_ok = n_held = 0
        t.ws.cell(1, 1).value = (f'OMi {root} - review table | Brennan TFA catalog {tab["table_id"]} + Brennan CAD records (group B 2026-10-21); '
                                 'port drill = Air-Way per-size (A11) | was a skeleton')
        for c, _, _ in mp: t.col(c, create=True)
        for c, _ in pdc + thc: t.col(c, create=True)
        t.col('$PRP@DimSource', create=True)
        for pn in t.rows:
            if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
            dd = [int(x) for x in re.findall(r'-(\d\d)', pn)]
            cv = cat.get(pn); rec = T.record(pn) or {}
            if not cv:
                t.note(pn, '$COMMENT', 'group B 2026-10-21: not in the Brennan TFA catalog table - stays MISSING'); continue
            diff = []
            for c, ck, rk in mp:
                v = float(cv[ck]); rv = rec.get(rk)
                if isinstance(rv, float) and abs(v - rv) > 0.0051: diff.append(f'{c.split("@")[0]} catalog {v} vs CAD record {rk} {rv}')
            if diff:
                t.note(pn, '$COMMENT', 'HELD (group B 2026-10-21): Brennan catalog and CAD record differ - ' + '; '.join(diff) + ' (ask the user; never picked)')
                n_held += 1; continue
            for c, ck, rk in mp:
                t.set(pn, c, float(cv[ck]), f'Brennan TFA catalog {tab["table_id"]} {ck}' + (f' (= CAD record {rk})' if rk in rec else ''))
            for c, k in pdc:
                if dd[k] not in PD: t.note(pn, '$COMMENT', f'no Air-Way per-size port drill for -{dd[k]:02d}'); continue
                t.set(pn, c, PD[dd[k]], f'A11 Q-TRANSFER-D3: Air-Way per-size -{dd[k]:02d} female ORB port drill')
            for c, k in thc: t.set(pn, c, G.JIC[dd[k]]['TM'], f'thread major of the -{dd[k]:02d} ORB thread named by the part number')
            t.set(pn, '$PRP@DimSource', 'BRENNAN', 'group B')
            t.set(pn, '$PRP@AxialSource', f'[BRENNAN-CAT {T.TODAY}: ' + ', '.join(c for c, _, _ in mp) + f'] Brennan TFA catalog {tab["table_id"]} (CAD record agrees '
                  'within the print rounding); port drill ' + ', '.join(c for c, _ in pdc) + ' = Air-Way per-size (A11) [user 2026-10-18 "Brennan = yes"; 2026-10-21 '
                  'CAD records "following my rule"]', 'group B')
            if all(t.get(pn, c) is not None for c, _, _ in mp) and all(t.get(pn, c) is not None for c, _ in pdc):
                t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: one source (Brennan)'); n_ok += 1
        t.save(); print(f'{root}: {n_ok} rows ASSUMED, {n_held} held')
