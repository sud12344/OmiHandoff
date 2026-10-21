"""edit_fs6402.py: FS6402 (male face seal x female JIC swivel, straight; no Air-Way series) - EMPTY cells <- the part's Brennan CAD record.
Codes placed on BRENNAN_FS6402-08-08 (tools/measure/prof.py, face-seal face at x = -0.504, hex face at 0): L 1.770 = face-seal face -> JIC nut
face (bbox), AD 0.378 = the bore (one dia face -> seat), CC 0.422 = JIC nut face -> nose tip (nose tip at 0.844, nut face at 1.266), H = body
hex 0.875, C = nut hex 0.875. New column SNT@DRIVE (nut face -> nose tip) <- CC: the part's own value (instead of the end-library NOSETIP_B)."""
import tabedit as T
MP = [('L@DRIVE', 'L'), ('S1HEX@HEX', 'H'), ('SHEX@HEX', 'C'), ('D1@BORE', 'AD'), ('SNT@DRIVE', 'CC'), ('THDMAJ_D@DRIVE', 'ATHD'), ('THDMAJ_B@DRIVE', 'BTHD')]


def main():
    t = T.Table('FS6402', fs=True); t.col('SNT@DRIVE', create=True); nb = np_ = 0
    for pn in t.rows:
        if t.get(pn, '$PRP@ScopeAction') != 'BUILD': continue
        rec = T.record(pn)
        if not rec: continue
        for c, k in MP:
            if isinstance(rec.get(k), float) and t.fill_brennan(pn, c, rec[k], k): nb += 1
        if all(t.get(pn, c) is not None for c, _ in MP) and t.get(pn, '$PRP@DataStatus') == 'MISSING':
            t.set(pn, '$PRP@DataStatus', 'ASSUMED', 'group B: every SPEC column filled (one source)'); np_ += 1
    t.save(); print(f'FS6402: {nb} Brennan cells, {np_} rows MISSING -> ASSUMED')
