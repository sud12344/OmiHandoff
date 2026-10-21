"""edit_4005.py: 4005 flange O-rings (SAE J518 code 61 / 62 flange face O-rings) - no Air-Way page, no OMi sizes -> the Brennan CAD record
(o_rings_and_seals/4005): ID = ring I.D., W = cross-section, MAT = Buna-N, OD = the flange tube size. Checked on BRENNAN_4005-08 (prof.py):
section circles r 0.367 / 0.507 -> I.D. 0.734, O.D. 1.014, Z extent +-0.070 -> W 0.140 = the record. The -08 / -12 / -16 code 61 and code 62
flange face grooves are the same (measured: 1700 / 1800 / FS1700 / FS1800 STEPs), so the ring fits both codes (Q-NEW-4005CODE needs no answer
for the geometry). Folded into the 4000 O-ring master (gen_ring SPEC 4000 tables), as FS4000."""
import tabedit as T

FRAC = {0.5: '1/2', 0.625: '5/8', 0.75: '3/4', 1.0: '1', 1.25: '1 1/4', 1.5: '1 1/2', 2.0: '2', 2.5: '2 1/2', 3.0: '3'}


def main():
    t = T.Table('4005'); n = 0
    t.ws.cell(1, 1).value = ('OMi 4005 Flange O-Ring (Buna-N) - review table | Brennan CAD records (PARTcommunity, o_rings_and_seals/4005) | group B 2026-10-21 '
                             '| folded into the 4000 O-ring master')
    for c in ('ID@DRIVE', 'W@DRIVE', '$PRP@TubeOD', '$PRP@Material', '$PRP@DimSource'): t.col(c, create=True)
    for pn in t.rows:
        if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
        rec = T.record(pn)
        if not rec or not isinstance(rec.get('ID'), float):
            t.note(pn, '$COMMENT', 'group B 2026-10-21: no Brennan CAD record for this size (PARTcommunity returned none) - stays MISSING')
            continue
        t.fill_brennan(pn, 'ID@DRIVE', rec['ID'], 'ID'); t.fill_brennan(pn, 'W@DRIVE', rec['W'], 'W')
        t.set(pn, '$PRP@TubeOD', FRAC.get(rec['OD'], str(rec['OD'])), 'Brennan CAD record OD (flange tube size)')
        t.set(pn, '$PRP@Material', f'{rec["MAT"]} (Brennan CAD record)', 'Brennan CAD record MAT')
        t.set(pn, '$PRP@AxialSource', 'Brennan CAD record ' + pn + ' (I.D. ' + str(rec['ID']) + ', W ' + str(rec['W']) + '; checked on BRENNAN_4005-08: I.D. 0.734 / '
              'O.D. 1.014 / W 0.140); no Air-Way page, no OMi sizes [user 2026-10-21: Brennan CAD records "following my rule"]', 'group B')
        t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: one source (Brennan)'); n += 1
    t.save(); print(f'4005: {n} rows ASSUMED')
