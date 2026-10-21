"""edit_6900.py: A3 (2026-10-18 "correct the 6900 table: male ORB x female NPSM swivel straight").
- title / Threads text corrected; the old "BLOCKED: female-JIC union internals" note (wrong identity) replaced
- Air-Way rows with every SPEC column filled: MISSING -> ASSUMED (Air-Way s105 single source); Brennan's record printed in $COMMENT
  as a cross-check (Air-Way values stay)
- 6900-32-32-O (no Air-Way row): the empty W4 / L2 / D cells <- Brennan record L / L1 / A2D (codes decoded on BRENNAN_6900-08-08-O:
  L = ORB tip -> nut face 1.550, L1 = ORB tip -> stem tip 1.270, A2D = NPSM bore 0.460, B1D = ORB bore 0.391)"""
import tabedit as T

NEED = ['W4@DRIVE', 'L2@DRIVE', 'C2HEX@HEX', 'CHEX@HEX', 'D1@BORE', 'D@BORE', 'THDMAJ_B@DRIVE']
XCHK = [('W4@DRIVE', 'L'), ('L2@DRIVE', 'L1'), ('C2HEX@HEX', 'C4'), ('CHEX@HEX', 'C'), ('D1@BORE', 'B1D'), ('D@BORE', 'A2D')]
NPSM = {2: '1/8-27', 4: '1/4-18', 6: '3/8-18', 8: '1/2-14', 12: '3/4-14', 16: '1-11 1/2', 20: '1 1/4-11 1/2', 24: '1 1/2-11 1/2', 32: '2-11 1/2'}
ORB = {4: '7/16-20', 5: '1/2-20', 6: '9/16-18', 8: '3/4-16', 10: '7/8-14', 12: '1 1/16-12', 14: '1 3/16-12', 16: '1 5/16-12', 20: '1 5/8-12',
       24: '1 7/8-12', 32: '2 1/2-12'}


def main():
    t = T.Table('6900')
    t.ws.cell(1, 1).value = ('OMi 6900 Male ORB x Female NPSM Swivel Adapter - Design Table v1 | AW s105 double-pass 24 rows | GENERATED 2026-09-06 | '
                             'identity corrected 2026-10-21 (A3 2026-10-18; was "Female Adapter Union x Male NPSM")')
    for pn in t.rows:
        if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
        a, b = (int(x) for x in pn.split('-')[1:3])
        rec = T.record(pn)
        if pn == '6900-32-32-O' and rec:
            for c, k in (('W4@DRIVE', 'L'), ('L2@DRIVE', 'L1'), ('D@BORE', 'A2D')): t.fill_brennan(pn, c, rec[k], k)
        t.set(pn, '$PRP@Threads', f'{ORB[a]} (male ORB) x {NPSM[b]} NPSM (female swivel)', 'A3: corrected identity')
        com = t.get(pn, '$COMMENT') or ''
        if com.startswith('BLOCKED: female-JIC union'):
            rest = com.split(' | ', 1)[1] if ' | ' in com else ''
            t.set(pn, '$COMMENT', 'A3 (user 2026-10-18): male ORB x female NPSM swivel straight - the old "female-JIC union internals" block was the wrong '
                  'identity (removed 2026-10-21)' + (' | ' + rest if rest else ''), 'A3')
        if rec:
            x = [(c, k, t.get(pn, c), rec.get(k)) for c, k in XCHK]
            diff = [f'{c.split("@")[0]} {v} vs Brennan {k} {bv}' for c, k, v, bv in x if v is not None and isinstance(bv, float) and abs(v - bv) > 0.0101]
            if pn != '6900-32-32-O':
                t.note(pn, '$COMMENT', 'Brennan CAD record cross-check (2026-10-21; Air-Way values built): ' +
                       (('differ: ' + '; '.join(diff)) if diff else 'agree within the 2-decimal rounding on W4 / L2 / C2 / C / D1 / D'))
        if all(t.get(pn, c) is not None for c in NEED) and t.get(pn, '$PRP@DataStatus') == 'MISSING':
            t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'A3: every column filled (Air-Way s105, single source)')
            if pn == '6900-05-04-O':
                # Q-CONFLICT-6900-05-04-O, user 2026-10-21 "do the recommended" (2026-10-18 recommendation: keep W4): Air-Way W4 1.30 stays; L2 1.19
                # is the cell that cannot be built (nut face 0.11 from the stem tip) -> Brennan's L1 1.09 (user Q1 2026-10-20 "use brennans"), marked BRENNAN
                aw = t.get(pn, 'L2@DRIVE')
                t.set(pn, 'L2@DRIVE', rec['L1'], 'user 2026-10-21 (keep W4) + Q1: Air-Way L2 not buildable -> Brennan record L1')
                t.set(pn, '$PRP@DimSource', 'BRENNAN', 'Q1 2026-10-20', create=True)
                t.note(pn, '$PRP@AxialSource', '[BRENNAN-CELL 2026-10-21: L2@DRIVE]', front=True)
                t.note(pn, '$COMMENT', f'Q-CONFLICT-6900-05-04-O (user 2026-10-21 "do the recommended" = keep W4): Air-Way W4 {t.get(pn, "W4@DRIVE")} kept; '
                       f'Air-Way L2 {aw} put the nut face {t.get(pn, "W4@DRIVE") - aw:.2f} from the stem tip (the measured -04 NPSM swivel cannot be built) '
                       f'-> L2 = the Brennan CAD record L1 {rec["L1"]} (user Q1 2026-10-20 "use brennans"; Brennan prints L {rec["L"]})')
    t.save()
