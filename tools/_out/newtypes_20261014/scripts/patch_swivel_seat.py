"""patch_swivel_seat.py (2026-10-15): gen_bent.py swivel end - (1) the 37 deg seat cone ends at the bore radius (SEAT_TO_BORE, as on
6565: on the short bent-tube swivel body the cone apex fell behind the body face at -12 / -16 and the sketch crossed itself);
(2) the swivel is anchored on the tube centre line with the body face SWB_TUBEOVL past the tube end (it was coincident with the
tube end, which put the whole swivel 0.05 too high). Keeps a copy of the file before the patch in ../history/."""
import os, shutil

P = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\newtypes_20261014\generators\gen_bent.py'
H = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\newtypes_20261014\history\gen_bent_before_seatfix.py'
shutil.copy2(P, H)
s = open(P, encoding='utf-8').read()
i0 = s.index('def vba_swivel(g, S):')
i1 = s.index("SW_SUBS = '''")
NEW = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vba_swivel_v2.py.txt'), encoding='utf-8').read()
s = s[:i0] + NEW + '\n\n' + s[i1:]
REP = [
    ("    head = vba_swivel(g, X['S']) if swv else vba_head(g, lib, c['O'] / 2)",
     "    head = vba_swivel(g, X['S'], c['D'] / 2, X['ov'])[0] if swv else vba_head(g, lib, c['O'] / 2)"),
    ("                ov = min(0.05, S['m']['BODYS'] - S['P1'] - 0.01)\n",
     "                ov = 0.05\n"),
    ("                cols.update({'OFFSET@NUTPLN': c['L1'], 'NUTCX@NUTHEXSK': round(g['X0'], 6), 'NUTHEX@NUTHEXSK': c['NUTHEX'],",
     "                cols.update({'SWB_SEATENDR@SWSK': round(c['D'] / 2, 6), 'SWB_TUBEOVL@SWSK': ov,\n"
     "                             'OFFSET@NUTPLN': c['L1'], 'NUTCX@NUTHEXSK': round(g['X0'], 6), 'NUTHEX@NUTHEXSK': c['NUTHEX'],"),
    ("            built.append((cols, why, dict(c=c, g=g, J=J, lib=lib, S=S, box=expected_box(c, g, lib, S))))",
     "            built.append((cols, why, dict(c=c, g=g, J=J, lib=lib, S=S, ov=(ov if swv else None), box=expected_box(c, g, lib, S))))"),
    ("                if c['D'] / 2 > m['SEATR'] - 0.01:\n",
     "                seat_end = S['s_nt'] + (m['SEATR'] - c['D'] / 2) / gs.TAN37\n"
     "                if seat_end > m['BODYS'] - ov - 0.02:\n"
     "                    why.append(f'the 37 deg seat (ends {seat_end:.4f} from the nut face) reaches the tube end ({m[\"BODYS\"] - ov:.4f})')\n"
     "                if c['D'] / 2 > m['SEATR'] - 0.01:\n"),
]
for a, b in REP:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s)
print('patched', P, '- copy before in', H)
