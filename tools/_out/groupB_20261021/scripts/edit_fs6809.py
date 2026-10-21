"""edit_fs6809.py: FS6809 - EMPTY cells <- the part's Brennan CAD record (codes placed on BRENNAN_FS6809-06-06-NWO-FG, see gen_tee NWO_FS[6]):
N = crossing -> stud tip (L10), AAA = crossing -> swivel seal face (L21), C1 = swivel nut (SHEX), C2 = lock nut (S3HEX), JJ = body hex (S2HEX),
AD / BD = swivel / stud bores (D19 / D20); the washer face L11 = N - DT (DT = stud tip -> washer face: 0.457 on the -06 STEP, 0.540 on the
FS6801-08 pilot; the Air-Way rows agree: -06 1.45 - 0.98 = 0.47, -16 2.35 - 1.62 = 0.73 = DT 0.727, -20 0.73)."""
import tabedit as T
MP = [('L10@DRIVE', 'N'), ('L21@DRIVE', 'AAA'), ('SHEX@HEX', 'C1'), ('S3HEX@HEX', 'C2'), ('S2HEX@HEX', 'JJ'), ('D19@BORE', 'AD'), ('D20@BORE', 'BD'),
      ('THDMAJ_D@DRIVE', 'ATHD'), ('THDMAJ_N@DRIVE', 'BTHD')]
NEED = [c for c, _ in MP] + ['L11@DRIVE']


def main():
    t = T.Table('FS6809', fs=True); nb = np_ = 0
    for pn in t.rows:
        if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
        rec = T.record(pn)
        if not rec: continue
        for c, k in MP:
            if isinstance(rec.get(k), float) and t.fill_brennan(pn, c, rec[k], k): nb += 1
        if t.get(pn, 'L11@DRIVE') is None and isinstance(rec.get('DT'), float):
            t.fill_brennan(pn, 'L11@DRIVE', round(rec['N'] - rec['DT'], 4), 'N-DT'); nb += 1
        if all(t.get(pn, c) is not None for c in NEED) and t.get(pn, '$PRP@DataStatus') == 'MISSING':
            t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: every SPEC column filled (one source)'); np_ += 1
    t.save(); print(f'FS6809: {nb} Brennan cells, {np_} rows MISSING -> ASSUMED')
