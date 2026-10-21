# ==== GROUP C (2026-10-21, compression / bite type, SAE J514/2 flareless): BITE end library, end modules, SPECs C2402 C2403 C2404 C2405 C0318 ====
# STAGED in tools/_out/groupC_20261021/tools_c (README.md there). Additive: no existing root reads anything below.
# BITE end library = Brennan's CAD parameter records of OMi's compression fittings (PARTcommunity reversemap, user 2026-10-21 "yes you can use
# them following my rule"; tools/_out/partcommunity_20261021/pc_final.csv) - the B1 codes of the C2402 / C2403 / C2405 / C2500 / C2501 / C2502 /
# C2601 / C6801 records and the B2 codes of the bite-x-bite records are IDENTICAL for every record of a tube dash (groupC scripts/records.py,
# bite_lib(): 71 records, 0 disagreements), so the chain is a per-dash end library like the JIC chain:
#   TM   thread major (B1THD; = the OMi file thread callout "Side 1 Thread")     A  tube socket dia (AB1)      K  tube socket depth (KB1)
#   NL   relief neck length behind the thread (CB1)                              ND relief neck dia (EB1)
#   EL   body tip to the hex face = BB1 (hex face to the nut face) + MB1 (nut face to the body tip, assembled)
# Letters decoded on the ten Brennan -08 STEPs (09_STEP_FILES/BRENNAN_C*-08*.stp; groupC measure/measure_c.txt): C2402 / C2403 / C2405 and the
# forged C2500 / C2501 / C2502 / C2601 / C6801 legs all show the same -08 end: socket 0.514 x 0.305 deep at the tip, thread major 0.750 from the
# tip to 0.423, 45deg ramp down to the 0.660 neck, neck 0.094 long, hex face 0.562 from the tip.
BITE_MEAS = {   # dash: TM, A, K, NL, ND, EL  (Brennan records, single source -> ASSUMED)
    4: dict(TM=0.4375, A=0.261, K=0.234, NL=0.075, ND=0.364, EL=0.453),
    6: dict(TM=0.5625, A=0.386, K=0.250, NL=0.083, ND=0.482, EL=0.469),
    8: dict(TM=0.7500, A=0.514, K=0.305, NL=0.094, ND=0.660, EL=0.562),
    10: dict(TM=0.8750, A=0.641, K=0.350, NL=0.107, ND=0.773, EL=0.625),
    12: dict(TM=1.0625, A=0.766, K=0.350, NL=0.125, ND=0.945, EL=0.688),
    16: dict(TM=1.3125, A=1.016, K=0.415, NL=0.125, ND=1.194, EL=0.688),
    20: dict(TM=1.6250, A=1.270, K=0.415, NL=0.125, ND=1.507, EL=0.688),
    24: dict(TM=1.8750, A=1.520, K=0.485, NL=0.125, ND=1.755, EL=0.688),
    32: dict(TM=2.5000, A=2.022, K=0.485, NL=0.125, ND=2.381, EL=0.688),
}
BITE_THR = {4: '7/16-20', 6: '9/16-18', 8: '3/4-16', 10: '7/8-14', 12: '1 1/16-12', 16: '1 5/16-12', 20: '1 5/8-12', 24: '1 7/8-12', 32: '2 1/2-12'}  # OMi file / Brennan B1
BITE_RAMPANG = 45      # thread major -> relief neck, measured on every -08 Brennan STEP (C2402 / C2403 / C2500 / C2501 / C2601); ASSUMED at the other dashes
BITE_COLS = (('A', 'BITE_SOCKD@DRIVE'), ('K', 'BITE_SOCKL@DRIVE'), ('ND', 'BITE_NECKD@DRIVE'), ('NL', 'BITE_NECKL@DRIVE'), ('EL', 'BITE_ENDL@DRIVE'))
BITE_ASSUME = ('BITE-TYPE (SAE J514/2 flareless) BODY END = Brennan CAD records (per-dash library BITE_MEAS, identical on every Brennan compression '
               'record of a dash; single manufacturer -> ASSUMED): male thread of the tube dash (TM) from the body tip, 45deg ramp (measured on the '
               'Brennan -08 STEPs, ASSUMED at the other dashes) down to the relief neck ND x NL, hex face EL = BB + MB from the tip; tube socket A x K '
               'deep at the tip (the tube stop), through bore behind it. NOT modelled: the 24deg sleeve cone (Brennan\'s CAD has none: its socket is a '
               'plain counterbore - SAE J514/2 not available as a citable source), the tip chamfer (hidden inside the fused nut on every Brennan STEP; '
               'starts at dia 0.676 on the -08 tip face), hex end chamfers. The nut (C0318) and the sleeve (C0319) are separate parts, not modelled '
               'in the body (as the 2700-LN locknut); "-M1" body-only part numbers = the same body (ASSUMED, OMi "(Body)")')


def end_BITEM(dash, sfx):
    """male bite-type (flareless) body end: thread major from the tip (x = 0) over TZ, 45deg ramp to the relief neck, neck to the hex face at EL.
    The tube socket (A x K) is cut from the tip face by a pocket (BoreCut POCKET_<sfx>, as the 0403 braze socket)."""
    if dash not in BITE_MEAS: raise KeyError(f'no -{dash:02d} entry in the BITE end library; needs a Brennan compression record / STEP with a -{dash:02d} bite end')
    e = BITE_MEAS[dash]; rM = e['TM'] / 2; rN = e['ND'] / 2; ramp = (rM - rN) / math.tan(math.radians(BITE_RAMPANG))
    TZ = round(e['EL'] - e['NL'] - ramp, 6)
    assert TZ > e['K'] - 1e-9, (dash, TZ, e['K'])
    V = [(0.0, rM), (TZ, rM), (TZ + ramp, rN), (e['EL'], rN)]
    seg = dict(face=0, thd=1, ramp=2, neck=3)
    P_ = 1 / tpi_of(BITE_THR[dash]); rS = e['A'] / 2
    cols = {f'THDMAJR_{sfx}@DRIVE': rM, f'BITE{sfx}_THDZ@DRIVE': TZ, f'BITE{sfx}_RAMPANG@DRIVE': BITE_RAMPANG, f'BITE{sfx}_NECKR@DRIVE': rN,
            f'BITE{sfx}_NECKL@DRIVE': e['NL'], f'SOCKDIA@POCKET_{sfx}': e['A'], f'DEPTH@POCKETCUT_{sfx}': e['K'],
            f'THDDIA@THD_End{sfx}': e['TM'], f'THDPITCH@THD_End{sfx}': round(P_, 5), f'DEPTH@THD_End{sfx}': TZ,
            f'Profile_Height@THD_End{sfx}_PROF': round(0.54127 * P_, 5), f'Profile_Land@THD_End{sfx}_PROF': round(0.25 * P_, 5), f'THDPITCH@THD_End{sfx}_PROF': round(P_, 5)}
    return dict(kind='BITEM', V=V, endlen=e['EL'], seg=seg, cols=cols, thr=BITE_THR[dash] + ' (bite type)', e=e, rM=rM, rN=rN, TZ=TZ, ramp=ramp,
                faceR=round((rS + rM) / 2, 5), td=e['A'], P1=e['K'], rS=rS, dash=dash,
                thread=dict(type='CUT', ex=TZ, er=rM, depth=TZ, size=f"{e['TM']:.4f}-{tpi_of(BITE_THR[dash]):g}", pitch=P_))


def bite_checks(E, bore, rB, hexb):
    """chk / warn for a BITEM end and the through bore behind its tube socket"""
    chk, warn = [], []
    e = E['e']; P_ = E['thread']['pitch']; root_ = E['rM'] - 0.6134 * P_
    if bore is None: chk.append('no through bore behind the tube socket')
    elif bore >= e['A'] - 0.02: chk.append(f'bore {bore} not below the tube socket {e["A"]} (no tube stop)')
    if root_ - E['rS'] < 0.03: chk.append(f'wall between the tube socket ({e["A"]}) and the thread root ({2 * root_:.4f}) only {root_ - E["rS"]:.4f}')
    if bore is not None and E['rN'] - bore / 2 < 0.03: chk.append(f'neck wall {E["rN"] - bore / 2:.4f} (neck dia {e["ND"]}, bore {bore})')
    if E['rM'] >= rB - 0.005: chk.append(f'bite thread major {e["TM"]} not below the hex corners {2 * rB:.4f}')
    elif hexb is not None and E['rM'] > hexb / 2 - 0.002: warn.append(f'bite thread major {e["TM"]} at / above the hex flats {hexb} (the thread lies outside the hex zone: harmless)')
    return chk, warn


def bite_rowcheck(r, E, sfx_cols):
    """the row's own Brennan bite cells (if filled) must equal the library chain of its dash"""
    out = []
    for k, c in BITE_COLS:
        v = r.get(c)
        if v is not None and abs(v - E['e'][k]) > 5e-4: out.append(f'{c} {v} differs from the BITE library -{E["dash"]:02d} {E["e"][k]}')
    return out


# ---- C0318 compression tube nut (Brennan C0318 records + BRENNAN_C0318-08 STEP): hex prism; End A (x = 0) = the thread mouth: 45deg countersink
# from dia B to the basic minor, female UN/UNF thread over F; minor bore on to E; 45deg cone from the minor down to the tube hole D; tube hole to
# the End B face (x = L). STEP -08: countersink 0.755 -> 0.6824 (0.036 deep), minor to 0.516 (= F), a 0.6724 counterbore to 0.599 (= E; 0.005 radial
# step NOT in the record - drawn at the minor), 45deg cone to 0.505 at 0.6826, hole to 0.840 = L. Hex corner chamfers (30deg from dia A) NOT modelled.
CNUT_ASSUME = ('COMPRESSION TUBE NUT (bite type): L / hex / thread length F / cone start E / tube hole D / countersink dia B = the Brennan C0318 CAD '
               'record of the size (single source -> ASSUMED); construction measured on the BRENNAN_C0318-08 STEP: End A = thread mouth, 45deg '
               'countersink from dia B to the ASME B1.1 basic minor (D - 1.082532P; = the STEP 0.6824), straight helical UN/UNF-2B thread over F, '
               'minor bore to E, 45deg internal cone from the minor down to the tube hole D, tube hole through End B; the 0.005 radial counterbore '
               'step between F and E on the -08 STEP (not in the record) and the 30deg hex corner chamfers (from dia A) are NOT modelled')


def end_CNUTA(dash, sfx, major, thr, csd, F, hexaf):
    """C0318 End A: construction core (axis -> countersink bottom) + 45deg countersink, kind NUTCSA (same DRIVE segments as the 0306 locknut);
    carries the female thread (HELIX from the face over F); faceR = on the End A face between the countersink rim and the hex flats"""
    P_ = 1 / tpi_of(thr); rmin = round((major - 1.082532 * P_) / 2, 5); rcs = round(csd / 2, 5); cs = round(rcs - rmin, 5)
    if cs <= 0.002: raise AssertionError(f'countersink dia {csd} not above the thread minor {2 * rmin:.4f}')
    cols = {f'NUTCS{sfx}_MINR@DRIVE': rmin, f'NUTCS{sfx}_CSR@DRIVE': rcs,
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': F, f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    e = dict(TM=major, thr=thr)
    return dict(kind='NUTCSA', V=[(cs, rmin), (0.0, rcs)], endlen=0.0, seg=dict(core=0, csk=1, face=2), faceseg=2, cols=cols,
                thr=thr + (' UN-2B' if tpi_of(thr) <= 12 else ' UNF-2B') + ' (compression nut)', faceR=round((rcs + hexaf / 2) / 2, 5), td=2 * rmin, P1=cs, e=e, rmin=rmin,
                rcs=rcs, cs=cs, dash=dash, F=F,
                thread=dict(type='HELIX', r=rmin, height=F, pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


def end_CNUTB(dash, sfx, L, E_, D, rmin):
    """C0318 End B (x = L) cavity: tube hole D from the face, 45deg cone up to the minor at E_ from End A, flat construction core end there
    (the minor bore BORE_A from End A to E_ removes the core)"""
    rD = round(D / 2, 5); dc = rmin - rD
    if dc < 0.01: raise AssertionError(f'tube hole {D} not below the thread minor {2 * rmin:.4f}')
    xs = round(L - E_ - dc, 5)
    if xs < 0.03: raise AssertionError(f'cone end {E_ + dc:.4f} leaves no tube hole before L {L}')
    VG = [(0.0, rD), (xs, rD), (L - E_, rmin), (L - E_, 0.0)]
    cols = {f'CNUT{sfx}_HOLER@DRIVE': rD, f'CNUT{sfx}_HOLEL@DRIVE': xs, f'CNUT{sfx}_CONEANG@DRIVE': 45, f'CNUT{sfx}_MINR@DRIVE': rmin}
    return dict(kind='CNUTB', V=[], VG=VG, cav=True, endlen=0.0, seg=dict(face=0), cols=cols, thr=f'tube hole {D}', faceR=None, td=D, P1=L - E_,
                rD=rD, xs=xs, rmin=rmin, E=E_, dash=dash, thread=None)


SPEC['C2402'] = dict(name='Compression Male Connector', L='L@DRIVE', hex='HEXB@HEX', bite=True,
                     A=lambda r, a, b: end_BITEM(a, 'A'), B=lambda r, a, b: end_JICM(b, 'B'),
                     bore=('mid', 'D2@BORE', 'D2@BORE'), ref='C2402-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_B@DRIVE', 'b')),
                     desc=lambda r, tA, tB: f'Compression Male Connector, {tA} x {tB} male 37 deg JIC',
                     assume=BITE_ASSUME + '; male JIC end B: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L (bite body tip to JIC tip) / '
                            'hex: Brennan record (C2402-08-08: 1.500 / 0.812 = the STEP); hex between the two end lengths (Brennan C2402-08-08 hex 0.281 '
                            '= L - 0.562 - 0.657); ONE through bore = the JIC bore D2 (BRENNAN_C2402-08-08 STEP: the 0.391 bore runs from the JIC tip to '
                            'the tube socket - the record\'s B1D 0.422 is not on the STEP; a 0.505 x 0.013 ring between the bore and the socket is NOT modelled)')
SPEC['C2403'] = dict(name='Compression Union', L='L@DRIVE', hex='HEXB@HEX', bite=True,
                     A=lambda r, a, b: end_BITEM(a, 'A'), B=lambda r, a, b: end_BITEM(b, 'B'),
                     bore=('mid', 'D1@BORE', 'D2@BORE'), ref='C2403-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_B@DRIVE', 'b')),
                     desc=lambda r, tA, tB: f'Compression Union, {tA} x {tB}',
                     assume=BITE_ASSUME + ' (both ends); L (body tip to body tip) / hex: Brennan record (C2403-08-08: 1.422 / 0.812 = the STEP); hex '
                            'between the two end lengths; bores D1 / D2 (record B1D / B2D, equal on every record) stepped at the hex mid-plane (no effect)')
SPEC['C2404'] = dict(name='Compression Male Pipe Adapter', L='L@DRIVE', hex='HEXB@HEX', bite=True,
                     A=lambda r, a, b: end_BITEM(a, 'A'), B=lambda r, a, b: end_NPTFM(b, 'B'),
                     bore=('mid', 'D1@BORE', 'D2@BORE'), ref='C2404-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'PIPEOD@DRIVE', 'b')),
                     desc=lambda r, tA, tB: f'Compression Male Pipe Adapter, {tA} x {tB}',
                     assume=BITE_ASSUME + '; male NPTF end B per ASME B1.20.3 with the 5404 Brennan-measured end length (end library); L / hex / bores: '
                            'review table; bore step at the hex mid-plane (ASSUMPTION, as 2403)')
SPEC['C2405'] = dict(name='Compression Female Pipe Adapter', L='L@DRIVE', hex='HEXB@HEX', bite=True,
                     A=lambda r, a, b: end_BITEM(a, 'A'), B=lambda r, a, b: end_NPTFF(b, 'B', r['TAPDRILL@BORE']),
                     bore=('A_to_pocket', 'D1@BORE', None), ref='C2405-08-08', p1col='FPT_P1@DRIVE', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'),),
                     desc=lambda r, tA, tB: f'Compression Female Pipe Adapter, {tA} x {tB}',
                     assume=BITE_ASSUME + '; female NPTF port (End B): tap drill TAPDRILL (record CA2) to the drill depth FPT_P1 (record EA2; C2405-08-06 '
                            'STEP: 0.578 drill to 0.680 = the record), helical thread over the drill depth (end-library rule; Brennan\'s thread length '
                            'PORTTHDL = record BA2, 0.580 on the -08-06 STEP); the 45deg port countersink (PORTCSKD) and the 120deg drill point NOT modelled; '
                            'L (bite body tip to the port face) / hex: Brennan record (C2405-08-06: 1.470 / 0.875 = the STEP); hex from the bite end to the port face; '
                            'through bore D1 (record B1D) from the tube socket to the port bottom')
SPEC['C0318'] = dict(name='Compression Tube Nut', L='L1@DRIVE', hex='CHEX@HEX', single=True,
                     A=lambda r, a, b: end_CNUTA(a, 'A', r['THDMAJ_B@DRIVE'], BITE_THR[a], r['CSKDIA@DRIVE'], r['THDL@DRIVE'], r['CHEX@HEX']),
                     B=lambda r, a, b: end_CNUTB(a, 'B', r['L1@DRIVE'], r['CONEX@DRIVE'], r['TUBEHOLE@BORE'],
                                                 round((r['THDMAJ_B@DRIVE'] - 1.082532 / tpi_of(BITE_THR[a])) / 2, 5)),
                     bore=('cnut_thru', None, None), ref='C0318-08', cnut=True,
                     desc=lambda r, tA, tB: f'Compression Tube Nut, {tA.split(" (")[0]}, {tB}',
                     assume=CNUT_ASSUME)
# ==== end GROUP C block ====


