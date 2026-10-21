"""edit_6801L.py: 6801-L / 6801-LL review tables, folded into the 6801 master (user 2026-10-21 "keep it the same as that" = as 2501-L / -LL).
Where the extra length goes (Q-NEW-FOLD-6801L), measured with tools/measure/prof.py (section through the ORB leg, crossing at the origin):
  BRENNAN_6801-08-08-NWO-FG     ORB tip 1.450, ORB body face 0.590, JIC leg 1.250
  BRENNAN_6801-L-08-08-NWO-FG   ORB tip 1.970, ORB body face 1.110, JIC leg 1.250
  BRENNAN_6801-LL-08-08-NWO-FG  ORB tip 2.480, ORB body face 1.620, JIC leg 1.250
  -> tip to body face 0.860 on all three (= the 6801 ORB_I3 at -08): the forged hex arm of the ORB leg runs longer, the adjustable ORB
     end (neck, locknut, washer, thread) is the 6801 one. Same topology -> rows of the 6801 master.
Cells:
- ORB_I3 / ORB_THDL (columns the 6801 SPEC reads, not printed in the -L / -LL tables) and an EMPTY ORB_GRVDIA = the 6801 table's own Air-Way
  rows of the same ORB size (A5 2026-10-18 "copy adjustable-ORB end values from the table's own rows of the same ORB size"; ORB_I3 checked
  against the two STEPs above at -08)
- other EMPTY cells of BUILD rows <- the part's Brennan CAD record (codes on BRENNAN_6801-L-08-08-NWO-FG: M = JIC leg, M7 = ORB leg, C =
  locknut, Y = body hex, B1D / B2D = JIC / ORB bores); thread majors = the thread the part number names (end library)
- 6801-LL-08-08-NWO-FG: Air-Way prints exactly its -08-10 row (M12 3.25, locknut 1.00, ORB bore 0.48 - the -10 values) -> user 2026-10-21
  "use brennan": every dimension cell = the Brennan CAD record, marked BRENNAN"""
import os, re, sys, openpyxl
import tabedit as T
sys.path.insert(0, os.path.join(T.A, 'tools_af', 'generators')); sys.path.insert(0, os.path.join(T.A, 'tools_af'))
os.environ.setdefault('OMI_ROOT', os.path.join(T.A, 'stage'))
import gen_straight2 as G

LEGC = {'6801L': 'M11@DRIVE', '6801LL': 'M12@DRIVE'}


def per_orb(col):
    ws = openpyxl.load_workbook(os.path.join(T.STAGE, 'DesignTable_6801.xlsx'), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]; m = {}
    for r in rows[2:]:
        if not r[0]: continue
        d = dict(zip(h, r)); dd = [int(x) for x in re.findall(r'-(\d\d)', d['$PRP@PartNo'])]
        if len(dd) == 2 and d.get(col) is not None and d.get('$PRP@DimSource') != 'BRENNAN': m.setdefault(dd[1], set()).add(d[col])
    return {k: v.pop() for k, v in m.items() if len(v) == 1}


def main():
    lib = {c: per_orb(c) for c in ('ORB_I3@DRIVE', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE')}
    for root, legc in LEGC.items():
        t = T.Table(root); nb = np_ = 0
        mp = [('M@DRIVE', 'M'), (legc, 'M7'), ('C4HEX@HEX', 'C'), ('Y@REF', 'Y'), ('D1@BORE', 'B1D'), ('D2@BORE', 'B2D')]
        for pn in t.rows:
            if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
            a, b = [int(x) for x in re.findall(r'-(\d\d)', pn)][:2]
            rec = T.record(pn)
            if pn == '6801-LL-08-08-NWO-FG':
                # Air-Way prints this row with exactly the 6801-LL-08-10 values (M12 3.25, locknut 1.00, ORB bore 0.48); user 2026-10-21 "use brennan
                # for 5": every dimension cell = the Brennan CAD record (= BRENNAN_6801-LL-08-08-NWO-FG: ORB tip 2.480, JIC leg 1.250), marked BRENNAN
                old = {c: t.get(pn, c) for c, _ in mp}
                for c, k in mp: t.set(pn, c, rec[k], f'user 2026-10-21 "use brennan": Air-Way row = its -08-10 row -> Brennan CAD record {k}')
                t.set(pn, '$PRP@DimSource', 'BRENNAN', 'user 2026-10-21', create=True)
                t.note(pn, '$PRP@AxialSource', '[BRENNAN-CELL 2026-10-21: ' + ', '.join(c for c, _ in mp) + ']', front=True)
                t.note(pn, '$COMMENT', 'Air-Way prints this row with the 6801-LL-08-10 values (' + ', '.join(f'{c.split("@")[0]} {v}' for c, v in old.items()) +
                       ') -> every dimension cell = the Brennan CAD record (user 2026-10-21 "use brennan"; = BRENNAN_6801-LL-08-08-NWO-FG: ORB tip 2.480, '
                       'JIC leg 1.250)')
            if rec:
                for c, k in mp:
                    if isinstance(rec.get(k), float) and t.fill_brennan(pn, c, rec[k], k): nb += 1
            for c, d, kind in (('THDMAJ_B1@DRIVE', a, 'UN'), ('THDMAJ_B2@DRIVE', b, 'UN')):
                if t.get(pn, c) is None: t.set(pn, c, G.JIC[d]['TM'], f'thread major of the -{d:02d} thread named by the part number (end library)')
            for c in ('ORB_I3@DRIVE', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'):
                if t.get(pn, c) if c in t.hdr else None: continue
                if b in lib[c]:
                    t.set(pn, c, lib[c][b], f'A5 2026-10-18: the 6801 table\'s own Air-Way rows of the -{b:02d} ORB size', create=True)
                    t.note(pn, '$PRP@AxialSource', f'{c.split("@")[0]} {lib[c][b]} = Air-Way 6801 rows of the -{b:02d} ORB size (A5; I3 = Brennan 6801 / 6801-L / '
                           '6801-LL STEPs at -08)')
            need = ['M@DRIVE', legc, 'C4HEX@HEX', 'Y@REF', 'D1@BORE', 'D2@BORE', 'ORB_I3@DRIVE', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE']
            if all(t.get(pn, c) is not None for c in need) and t.get(pn, '$PRP@DataStatus') == 'MISSING':
                t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: every SPEC column filled (one source)'); np_ += 1
            if rec and isinstance(rec.get('M7'), float) and t.get(pn, legc) is not None and abs(t.get(pn, legc) - rec['M7']) > 0.0101:
                t.note(pn, '$COMMENT', f'Brennan CAD record ORB leg M7 {rec["M7"]} vs Air-Way {legc.split("@")[0]} {t.get(pn, legc)} - built to Air-Way '
                       '(Air-Way first; tell the user / OMi)')
        t.save(); print(f'{root}: {nb} Brennan cells, {np_} rows MISSING -> ASSUMED')
