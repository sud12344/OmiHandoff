"""patch_gt.py: GROUP C additions to gen_tee.py - leg_BITEM, the C25xx / C2601 / C6801 SPECs, and inserted hooks (no existing line edited)"""
import sys
p = sys.argv[1]; s = open(p).read()
def ins_before(anchor, text):
    global s
    assert s.count(anchor) == 1, (anchor[:70], s.count(anchor))
    i = s.index(anchor); s = s[:i] + text + s[i:]
def ins_after(anchor, text):
    global s
    assert s.count(anchor) == 1, (anchor[:70], s.count(anchor))
    i = s.index(anchor) + len(anchor); s = s[:i] + text + s[i:]

LEG = '''
# ==== GROUP C (2026-10-21, compression / bite type): the bite-type leg of a forged elbow / tee (STAGED, tools/_out/groupC_20261021) ====
# Chain = gen_straight2 BITE_MEAS (Brennan compression records, per tube dash) - the same end as the straight C24xx bodies: hex arm to
# M - EL, relief neck ND x NL, 45deg ramp, thread major to the tip, tube socket A x K cut at the tip. The socket is part of the revolved leg
# profile (the leg sketch steps down at the tip face to the socket radius and closes on the axis at the socket bottom); the leg bore is cut from
# the tip face to the crossing as on every leg. Brennan -08 forged STEPs (C2500 / C2501 / C2502 / C2601 / C6801): hex arm ends at M - 0.562,
# neck 0.660 x 0.094, thread 0.750 to the tip, socket 0.514 x 0.305 - identical to the straight bodies.
def leg_BITEM(i, dash, M, BR):
    if dash not in G.BITE_MEAS: raise KeyError(f'no -{dash:02d} entry in the BITE end library')
    e = G.BITE_MEAS[dash]; rM = e['TM'] / 2; rN = e['ND'] / 2; rS = e['A'] / 2; K = e['K']
    ramp = (rM - rN) / math.tan(math.radians(G.BITE_RAMPANG)); sh = M - e['EL']
    x1 = sh + e['NL']; x2 = x1 + ramp; TZ = round(M - x2, 6)
    V = [(0, 0), (0, BR), (sh, BR), (sh, rN), (x1, rN), (x2, rM), (M, rM), (M, rS), (M - K, rS), (M - K, 0)]
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': round(BR, 5), f'BITE{i}_NECKR@LEG{i}': rN, f'BITE{i}_NECKL@LEG{i}': e['NL'],
            f'BITE{i}_RAMPANG@LEG{i}': G.BITE_RAMPANG, f'THDMAJR_B{i}@LEG{i}': rM, f'BITE{i}_THDZ@LEG{i}': TZ, f'BITE{i}_SOCKR@LEG{i}': rS,
            f'BITE{i}_SOCKL@LEG{i}': K}
    pitch = 1 / G.tpi_of(G.BITE_THR[dash])
    tcols = {f'THDDIA@THD_End{i}': e['TM'], f'THDPITCH@THD_End{i}': round(pitch, 5), f'DEPTH@THD_End{i}': TZ,
             f'Profile_Height@THD_End{i}_PROF': round(0.54127 * pitch, 5), f'Profile_Land@THD_End{i}_PROF': round(0.25 * pitch, 5), f'THDPITCH@THD_End{i}_PROF': round(pitch, 5)}
    dims = [('pair', 6, 0, f'M{i}', M, M / 2, BR + 0.6), ('rad', 1, 'BODYR', BR, sh / 2, -0.4), ('rad', 3, f'BITE{i}_NECKR', rN, (sh + x1) / 2, -0.2),
            ('len', 3, f'BITE{i}_NECKL', e['NL'], (sh + x1) / 2, BR + 0.15), ('ang', 4, 5, f'BITE{i}_RAMPANG', G.BITE_RAMPANG, x1 + 0.03, BR + 0.1),
            ('rad', 5, f'THDMAJR_B{i}', rM, (x2 + M) / 2, -0.3), ('len', 5, f'BITE{i}_THDZ', TZ, (x2 + M) / 2, BR + 0.35),
            ('rad', 7, f'BITE{i}_SOCKR', rS, M - K / 2, -0.1), ('len', 7, f'BITE{i}_SOCKL', K, M - K / 2, BR + 0.45)]
    thread = dict(type='CUT', ex=x2, er=rM, depth=TZ, size=f"{e['TM']:.4f}-{G.tpi_of(G.BITE_THR[dash]):g}", pitch=pitch)
    return dict(kind='BITEM', dash=dash, V=V, endlen=e['EL'], cols=cols, tcols=tcols, dims=dims, rmax=max(rM, rN),
                thr=G.BITE_THR[dash] + ' (bite type)', thread=thread, tipR=rM, Mtip=M,
                e=e, rM=rM, rN=rN, rS=rS, TZ=TZ)
# ==== end GROUP C leg ====

'''
ins_before('def leg_JICBH(i, dash, M, BR, i2, K1, O):\n', LEG)

SPECS = '''
# ==== GROUP C (2026-10-21, compression / bite type): forged -FG compression bodies (STAGED). Brennan -08 STEPs of each: the 2500HX / 2603HX forged
# pattern with bite legs (hex arms to M - 0.562, the female port collar 0.26 at the flats dia on C2502, the 6801 adjustable ORB leg on C6801). Rows:
# Brennan CAD records (DesignTable_C<root>.xlsx); "-M1" = the same body. The nut / sleeve (C0318 / C0319) are separate parts, not modelled.
SPEC['C2500'] = dict(name='Compression 90 deg Union Elbow', hex='Y@REF', elbow=True, ref='C2500-08-08-FG',
                     legs=[('BITEM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('BITEM', 'M2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE')])
SPEC['C2501'] = dict(name='Compression 90 deg Male Pipe Elbow', hex='Y@REF', elbow=True, ref='C2501-08-08-FG',
                     legs=[('BITEM', 'M@DRIVE', 'D@BORE', 'THDMAJ_A@DRIVE'), ('NPTFM', 'N@DRIVE', 'D1@DRILL', 'PIPEOD@DRIVE')])
SPEC['C2502'] = dict(name='Compression 90 deg Female Pipe Elbow', hex='Y@REF', elbow=True, ref='C2502-08-08-FG', conn=None, p1='PORTDEPTH@BORE',
                     legs=[('BITEM', 'M@DRIVE', 'D@BORE', 'THDMAJ_A@DRIVE'), ('NPTFF', 'N@DRIVE', 'TAPDRILL@BORE', 'PIPEOD@DRIVE')],
                     conn_src='the tap drill carried to the crossing (MEASURED: BRENNAN_C2502-08-06-FG STEP - the 0.578 drill runs from the bottom of the '
                              '0.58 deep tapered port to the run axis; the tapered port and its 45deg mouth countersink are drawn as the tap-drill cylinder + '
                              'the Thread feature, as on every built female port)',
                     assume_extra=['BRENNAN_C2502-08-06-FG STEP: female port leg = hex arm to 0.760, round collar 0.260 long at the flats dia (0.875) to the '
                                   'port face 1.020 = N; port thread length 0.58 = record BA2 (PORTDEPTH), tap drill 0.578 = record CA2'])
SPEC['C2601'] = dict(name='Compression Male Pipe Branch Tee', hex='Y@REF', ref='C2601-08-08-08-FG',
                     legs=[('BITEM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('BITEM', 'M2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                           ('NPTFM', 'N@DRIVE', 'DDRILL@BORE', 'THDMAJ_A@DRIVE')])
SPEC['C6801'] = dict(name='Compression 90 deg Adjustable Male ORB Elbow', hex='Y@REF', elbow=True, ref='C6801-08-08-NWO-FG',
                     nwo=('=6801', 'HEXB@HEX', '=ORB:THDL', '=ORB:GD'),
                     legs=[('BITEM', 'LEG_BITE@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('NWO', 'LEG_ORB@DRIVE', 'D2@BORE', 'THDMAJ_B@DRIVE')],
                     assume_extra=['adjustable ORB leg = the 6801 end library (I3 = Air-Way 6801 ORB_I3 of the ORB size, thread length / undercut = the ORB end '
                                   'library; Q-TRANSFER-ENDLIB = yes); BRENNAN_C6801-08-08-NWO-FG STEP: ORB leg 1.450 / locknut 0.875 / body face 0.590 = the '
                                   'Brennan record M7 / C and the 6801-08-08-NWO-FG row (LEG_ORB 1.45, I3 0.86, nut hex 0.88)'])
# ==== end GROUP C SPECs ====
'''
ins_before('SPEC_WAITING = {\n', SPECS)

# hooks in the row loop
ins_before("        # SIZE-40 (2026-10-01): a leg dash missing from an end library (e.g. -40 NPTF) -> skip the row with the source that would fill it\n",
"""        btd = [d for (kind, lc, bc, tc), d in zip(legs4(sp), dd) if kind == 'BITEM' and d not in G.BITE_MEAS]     # GROUP C
        if btd:
            skipped.append((pn, 'no end data', f'bite-type end not in the BITE library for -{btd[0]:02d} (needs a Brennan compression record of that tube dash)')); continue
""")
ins_after("            tm = r[tc]\n",     # 2026-10-21: the live (batch 20) 'want' line also reads the face-seal majors
"""            if kind == 'BITEM':     # GROUP C: the bite leg's thread = the BITE library major of its dash
                if tm is None or abs(tm - G.BITE_MEAS[d]['TM']) > 1e-3: chk.append(f'{tc} {tm} does not match the -{d:02d} bite end ({G.BITE_MEAS[d]["TM"]})')
                continue
""")
ins_before("            if kind == 'JICM': L = leg_JICM(i, d, M, BR)\n",
"""            if kind == 'BITEM':     # GROUP C
                L = leg_BITEM(i, d, M, BR); L['bore'] = r[bc]; legs.append(L); continue
""")
ins_after("        AC = BR / COS30\n",
"""        for i_, L_ in enumerate(legs, 1):
            if L_['kind'] == 'BITEM':     # GROUP C: socket / bore / neck / thread-vs-hex gates + the row's Brennan bite cells = the library
                c_, w_ = G.bite_checks(L_, L_['bore'], AC, None); chk += [f'leg {i_}: {x_}' for x_ in c_]; warn += w_
                if L_['rN'] >= BR - 0.003: chk.append(f'leg {i_}: bite neck dia {2 * L_["rN"]:.4f} not below the hex flats {AF}')
                chk += [f'leg {i_}: {x_}' for x_ in G.bite_rowcheck(r, L_, None)]
""")
ins_after("    if 'JICM' in k: t.append('JIC legs: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); Thread feature over THDZ')\n",
"""    if 'BITEM' in k: t.append(G.BITE_ASSUME + '; forged leg: hex arm to M - EL, the tube socket drawn in the revolved leg profile')     # GROUP C
""")
open(p, 'w').write(s); print('patched', p)
