"""edit_elbows.py: the adjustable-ORB elbows 6901 / 6805 / 6806 / 6809 - EMPTY cells of the OMi -FG BUILD rows <- the part's Brennan CAD
record (Air-Way first: filled cells are never touched). The record codes were placed on each family's STEP (prof.py / bbox, crossing at
the origin, ORB leg on -X, the other leg on +Y):
  6901-06-08-NWO-FG: M7 1.320 = crossing -> ORB tip (-X extent), M6 1.320 = crossing -> NPSM nut face (+Y extent), M 1.040 = crossing -> stem tip,
                     body hex Y 0.750 (corner r 0.433), NPSM bore AD 0.450, ORB bore BD 0.297, C = locknut, C1 = swivel nut
  6805-08-08-NWO-FG: M7 1.620 = ORB leg, N 1.230 = crossing -> female port face, Y 1.062 = body hex (Z extent +-0.531), BD 0.391 = ORB bore,
                     C = locknut; the port tap drill 0.718 (CT) runs on to the crossing (no separate connecting drill)
  6806-08-06-NWO-FG: M7 1.450 = ORB leg, N 1.220 = crossing -> male pipe tip, BD 0.391 = ORB bore, AD 0.406 = pipe-end drill, C = locknut, Y = body hex
  6809-10-10-NWO-FG: M7 1.700 = ORB leg, M6 1.620 = crossing -> swivel nut face, M 1.120 = crossing -> nose tip (seat mouth plane);
                     C1 = locknut, C2 = swivel nut (TFA p44: 6809-06-04 C1 0.688 = the -06 locknut, C2 0.563 = the -04 JIC nut)
Thread-major cells left empty take the standard major of the thread the part number names (ORB / JIC: UN major; pipe: ASME B1.20.3 E0
major as on every Air-Way row) - the record names the same thread (BTHD / ATXT). A row becomes ASSUMED (one source) once every column
its SPEC reads is filled."""
import os, sys, re
import tabedit as T
sys.path.insert(0, os.path.join(T.A, 'tools_af', 'generators')); sys.path.insert(0, os.path.join(T.A, 'tools_af'))
os.environ.setdefault('OMI_ROOT', os.path.join(T.A, 'stage'))
import gen_straight2 as G

MAP = {
    '6901': [('N5@DRIVE', 'M7'), ('M1@DRIVE', 'M'), ('W3@HEX', 'M6'), ('CHEX@HEX', 'C1'), ('C4HEX@HEX', 'C'), ('C1HEX@HEX', 'Y'),
             ('D1@BORE', 'BD'), ('D@BORE', 'AD')],
    '6805': [('M17@DRIVE', 'M7'), ('N1@DRIVE', 'N'), ('C4HEX@HEX', 'C'), ('Y1@REF', 'Y'), ('D@BORE', 'BD')],
    '6806': [('M7@DRIVE', 'M7'), ('N@DRIVE', 'N'), ('C4HEX@HEX', 'C'), ('Y@REF', 'Y'), ('D@BORE', 'BD'), ('D1@BORE', 'AD')],
    '6809': [('M7@DRIVE', 'M7'), ('M5@DRIVE', 'M6'), ('M10@DRIVE', 'M'), ('C4HEX@HEX', 'C1'), ('C3HEX@HEX', 'C2'), ('Y@HEX', 'Y'),
             ('D1@BORE', 'B1D'), ('D2@BORE', 'B2D')],
}
# thread-major columns: (column, which dash 0/1, kind)
THR = {'6901': [('THDMAJ_B@DRIVE', 0, 'UN'), ('THDMAJ_A1@DRIVE', 1, 'NPT')], '6805': [('THDMAJ_B@DRIVE', 0, 'UN'), ('THDMAJ_A@DRIVE', 1, 'NPT')],
       '6806': [('THDMAJ_B@DRIVE', 0, 'UN'), ('THDMAJ_A@DRIVE', 1, 'NPT')], '6809': [('THDMAJ_B1@DRIVE', 0, 'UN'), ('THDMAJ_B2@DRIVE', 1, 'UN')]}
# columns each SPEC reads (DataStatus gate)
NEED = {'6901': ['N5@DRIVE', 'M1@DRIVE', 'W3@HEX', 'CHEX@HEX', 'C4HEX@HEX', 'C1HEX@HEX', 'D1@BORE', 'D@BORE', 'THDMAJ_B@DRIVE', 'THDMAJ_A1@DRIVE'],
        '6805': ['M17@DRIVE', 'N1@DRIVE', 'C4HEX@HEX', 'Y1@REF', 'D@BORE', 'TAPDRILL@BORE', 'THDMAJ_B@DRIVE', 'THDMAJ_A@DRIVE'],
        '6806': ['M7@DRIVE', 'N@DRIVE', 'C4HEX@HEX', 'Y@REF', 'D@BORE', 'D1@BORE', 'THDMAJ_B@DRIVE', 'THDMAJ_A@DRIVE'],
        '6809': ['M7@DRIVE', 'M5@DRIVE', 'M10@DRIVE', 'C3HEX@HEX', 'C4HEX@HEX', 'Y@HEX', 'D1@BORE', 'D2@BORE', 'THDMAJ_B1@DRIVE', 'THDMAJ_B2@DRIVE']}


def main():
    for root, mp in MAP.items():
        t = T.Table(root); n_fill = n_prom = 0
        for pn in t.rows:
            if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
            sku = t.get(pn, '$PRP@OMiSKU') or pn
            rec = T.record(sku)
            if rec:
                for c, k in mp:
                    if isinstance(rec.get(k), float) and t.fill_brennan(pn, c, rec[k], k): n_fill += 1
            dd = [int(x) for x in re.findall(r'-(\d\d)', sku)][:2]
            for c, i, kind in THR[root]:
                if t.get(pn, c) is None:
                    d = dd[i]; v = G.JIC[d]['TM'] if kind == 'UN' else G.NPTF[d][2]
                    t.set(pn, c, v, f'thread major of the -{d:02d} {"ORB/JIC UN" if kind == "UN" else "NPTF"} thread named by the part number (end library, '
                          'as every built row)')
            if all(t.get(pn, c) is not None for c in NEED[root]) and t.get(pn, '$PRP@DataStatus') == 'MISSING':
                t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: every SPEC column filled (one source)'); n_prom += 1
        if root == '6805':
            # user Q1 2026-10-20 ("use brennans"): Air-Way's 6805-08-06-NWO-FG N1 0.63 (Air-Way's own comment: "likely typo", the non-FG row prints
            # 1.02) cannot be built (the -06 port P1 0.68 is longer than the leg) -> the Brennan record N 1.02, marked BRENNAN
            pn = '6805-08-06-NWO-FG'; old = t.get(pn, 'N1@DRIVE'); rec = T.record(pn)
            t.set(pn, 'N1@DRIVE', rec['N'], 'Q1 2026-10-20: Air-Way N1 not buildable -> Brennan record N')
            t.set(pn, '$PRP@DimSource', 'BRENNAN', 'Q1 2026-10-20', create=True)
            t.note(pn, '$PRP@AxialSource', '[BRENNAN-CELL 2026-10-21: N1@DRIVE]', front=True)
            t.note(pn, '$COMMENT', f'Air-Way N1 {old} cannot be built (female -06 port MS51503 P1 0.68 is longer than the leg) -> Brennan CAD record N '
                   f'{rec["N"]} (= Air-Way\'s own non-FG 6805-08-06-NWO row; user Q1 2026-10-20 "use brennans", confirmed 2026-10-21)')
        if root == '6901':
            pn = '6901-08-12-NWO-FG'
            t.note(pn, '$COMMENT', 'BRENNAN_6901-08-12-NWO-FG (received 2026-10-21, tools/measure/npsm.py): the swivel end = NPSM_MEAS[12] (the 1404-12 end) on '
                   'every value, nut face 1.580, stem tip 1.270 (= the record M6 / M), body hex 1.062 - the record is right. Still generator-BLOCKED: '
                   'the swivel neck is only 0.015 long (body face 0.76 behind the nut face, nut rear face 0.745; the generator wants >= 0.02) and the '
                   'forged corner (puck radius 0.613) reaches 0.004 into the ORB locknut slab (starts 0.609; Brennan ends the corner at the ORB body face '
                   '0.59) - needs a generator change (group B README)')
        t.save(); print(f'{root}: {n_fill} Brennan cells, {n_prom} rows MISSING -> ASSUMED')
