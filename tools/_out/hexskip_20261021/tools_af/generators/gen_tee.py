#!/usr/bin/env python3
"""gen_tee.py - generic forged TEE / CROSS master generator (legs about X and Y, hex bars).

  python3 gen_tee.py 2650 2601 2602 2605 5600 5602 5604 5605

Geometry = the proven 2603HX pattern (Build_2603HX_MASTER, built 2026-09-18, clean all-config sweep):
  * every leg is a revolve on the Front Plane from the axis crossing to its tip face (LEGi / LEGi_BODY);
    legs 1,2 run along +X / -X, leg 3 along +Y, leg 4 (crosses) along -Y
  * forged body = hex bars, flats normal to Z, A/F = 2*BODYR:
      RUN  : one hex bar through the crossing along X (HEXL1 to +X, HEXL2 to -X)
      HEX3 : branch hex arm along +Y (tees)   |   RUN2 : second continuous bar along Y (crosses)
    Brennan 2650-08-08-08-08-FG STEP (09_STEP_FILES): both bars continuous, A/F 0.750 = Air-Way Y,
    hex shoulders at 0.593 = M - JIC end length, bore 0.392 = Air-Way D  -> this generator reproduces it.
  * A/F = max(catalog hex, JIC thread majors, male-NPTF max diameter) - the 2603HX rule (QA #115)
Leg end modules (same data as gen_straight2):
  JICM   MS33656J chain per dash (2403 table, VERIFIED vs Brennan); Thread feature over THDZ (2603HX rule)
  NPTFM  ASME B1.20.3 cone + relief to the Brennan-measured 5404 end length (ASSUMPTION for a forged tee)
  NPTFF  tap drill (Air-Way) to MS51503 P1 max (VERIFIED -08 by Brennan 5405 STEP); connecting drill from
         the pocket bottom to the crossing = the part's own bore column, or the tap drill carried to the
         crossing when the part publishes no bore (ASSUMPTION, logged per root)
Every table value is traceable; every assumption goes into $PRP@AxialSource.
"""
import sys, math, re, os, json, datetime, openpyxl
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import omi_paths as P          # tools/omi_paths.py (2026-09-25: made portable for Claude Code)
from progress_patch import add_progress, ref_config_at_save
import gen_straight2 as G
import sp3fix as sp3
IN = 0.0254; COS30 = math.cos(math.radians(30)); TAN60 = G.TAN60; TAN37 = G.TAN37; TAPER = G.TAPER
TODAY = datetime.date.today().isoformat()
REV = P.DESIGN_TABLES          # review tables DesignTable_<root>.xlsx (04_DESIGN_TABLES = single source of truth)
OUT = P.OUT_TEE; os.makedirs(OUT, exist_ok=True)
DEV = G.DEV
HX2603 = open(os.path.join(P.TEMPLATES, 'Build_2603HX_MASTER.bas')).read()   # frozen VBA helper library (2603HX macro, built clean)

BR5405 = 'Brennan 5405-08-08 STEP: 1/2 NPTF port drill depth 0.900 = MS51503 P1 max (VERIFIED -08 only)'
SPEC = {
    '2650': dict(name='Union Cross', hex='Y@HEX', cross=True, ref='2650-08-08-08-08-FG',
                 legs=[('JICM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('JICM', 'M3@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE'), ('JICM', 'M4@DRIVE', 'D4@BORE', 'THDMAJ_B4@DRIVE')]),
    '2601': dict(name='Male Branch Tee', hex='Y@REF', ref='2601-08-08-08-FG',
                 legs=[('JICM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('NPTFM', 'N@DRIVE', 'DDRILL@BORE', 'THDMAJ_A@DRIVE')]),
    '2602': dict(name='Female Branch Tee', hex='Y1@DRIVE', ref='2602-06-06-06-FG', conn='D1@BORE',
                 legs=[('JICM', 'M1_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M1_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE')]),
    '2605': dict(name='Male Run Tee', hex='Y@HEX', ref='2605-08-08-08-FG',
                 legs=[('JICM', 'M1@DRIVE', 'D_1@BORE', 'THDMAJ_B1@DRIVE'), ('NPTFM', 'N@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'),
                       ('JICM', 'M3@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    # ---- 2026-10-02 (new masters from the Brennan pilot STEPs, user: "yes, go ahead"): forged -FG tees with a female pipe port, measured with
    #      tools/measure/forged.py (validated by forged_validate.py on 2650-08 / 5605-08 / 5600-16 / 6502-08) = the existing 2603HX tee pattern
    #      (run bar through the crossing, branch hex arm, 0.26 round collar at the female port, every bore from its face to the crossing).
    #      PN order = leg order (end 1 = +X, end 2 = -X, end 3 = +Y branch); Brennan draws end 1 on -X (mirror image, same part).
    #      p1 = the female port thread length column (measured on the part's own STEP; the MS51503 P1 library value where the row has none).
    '2606': dict(name='Female Run Tee', hex='Y1@HEX', ref='2606-08-08-08-FG', conn=None, p1='PORTDEPTH@BORE',
                 legs=[('JICM', 'M1_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE'),
                       ('JICM', 'M1_3@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')],
                 conn_src='the tap drill carried to the crossing (MEASURED: Brennan 2606-08-08-08-FG STEP - the 0.718 drill runs from the bottom of the '
                          '0.75 deep tapered port to the axis crossing; the tapered port itself and its 45deg mouth chamfer are drawn as the tap-drill '
                          'cylinder + the Thread feature, as on every built female port)',
                 assume_extra=['Brennan 2606-08-08-08-FG STEP (2026-10-02, tools/measure/forged.py): run hex bar from the JIC hex face (0.863 = M - the '
                               '2403 -08 JIC end length 0.657) through the crossing to the female collar (0.970), branch hex arm to 0.863, female port '
                               'round collar 0.260 long at the flats dia, A/F 1.062, flats normal to Z, bores 0.391 = this pattern; JIC seat / land / '
                               'cone / thread major = the 2403 -08 chain, but the STEP shows NO thread relief (thread major runs to the hex face): the '
                               'model keeps the MS33656J relief of the 2403 chain, as every built tee / elbow (ASSUMPTION; Brennan 2505-08-08-FG and the '
                               '2403 straights show the relief)']),
    # 2026-10-09: male JIC run x female pipe run x female pipe branch (Air-Way s-page 2609: M1 / N1_2 / N1_3 / Y1 / D / TAPDRILL2 / 3); the
    # forged body of 2606 (JIC run end) with the 5605 female legs (collar); rows filled from OMi, ports = end library (Q-TRANSFER-ENDLIB = yes)
    '2609': dict(name='Female Run x Female Branch Tee', hex='Y1@HEX', ref='2609-08-08-08-FG', conn=None,
                 legs=[('JICM', 'M1@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1_3@DRIVE', 'TAPDRILL3@BORE', 'THDMAJ_A3@DRIVE')]),
    '2611': dict(name='Male Run x Female Branch Tee', hex='Y1@HEX', ref='2611-06-06-06-FG', conn=None, p1='PORTDEPTH@BORE',
                 legs=[('JICM', 'M1@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE'), ('NPTFM', 'N5@DRIVE', 'D1@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A3@DRIVE')],
                 conn_src='the tap drill carried to the crossing (MEASURED: Brennan 2611-06-06-06-FG STEP - the 0.578 drill runs from the bottom of the '
                          '0.58 deep tapered port to the run axis; the tapered port itself and its 45deg mouth chamfer are drawn as the tap-drill '
                          'cylinder + the Thread feature, as on every built female port)',
                 assume_extra=['Brennan 2611-06-06-06-FG STEP (2026-10-02, tools/measure/forged.py): run hex bar from the JIC hex face (0.754 = M - the '
                               '2403 -06 JIC end length 0.556) through the crossing to the male pipe hex face (0.660 = N - the 5404 -06 end length 0.56), '
                               'branch hex arm to the female collar (0.760), collar 0.260 long at the flats dia, A/F 0.875, flats normal to Z, bores '
                               '0.297 / 0.406 from each face to the crossing = this pattern; JIC end = the 2403 -06 chain but with NO thread relief on '
                               'the STEP (model keeps the MS33656J relief, ASSUMPTION as on every built tee); male pipe end: STEP taper 0.4817 from a '
                               '45deg tip chamfer + a 0.028 relief at the pipe OD 0.675, model = ASME B1.20.3 cone + relief (library, as every built '
                               'male pipe leg) with the same end length 0.56']),
    '5600': dict(name='Male Pipe Tee', hex='Y@HEX', ref='5600-08-08-08-FG',
                 legs=[('NPTFM', 'N1@DRIVE', 'D1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N2@DRIVE', 'D2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFM', 'N3@DRIVE', 'D3@BORE', 'THDMAJ_A3@DRIVE')]),
    '5602': dict(name='Male Run Pipe Tee', hex='WY@REF', ref='5602-08-08-08-FG', conn='D@BORE',
                 legs=[('NPTFM', 'N@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1_3@DRIVE', 'TAPDRILL3@BORE', 'THDMAJ_A3@DRIVE')]),
    '5604': dict(name='Male Branch Pipe Tee', hex='W@HEX', ref='5604-08-08-08-FG', conn='D@BORE',
                 legs=[('NPTFF', 'N1_1@DRIVE', 'TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFM', 'N@DRIVE', 'D@BORE', 'THDMAJ_A3@DRIVE')]),
    '5605': dict(name='Female Pipe Tee', hex='W@HEX', ref='5605-06-06-06-FG', conn=None,
                 legs=[('NPTFF', 'N1_1@DRIVE', 'TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1_3@DRIVE', 'TAPDRILL3@BORE', 'THDMAJ_A3@DRIVE')]),
    # ---- 2026-10-02 (new masters wave 1, PIPE-TEES): forged pipe tees / cross from their Brennan pilot STEPs, measured with
    #      tools/measure/pipetee.py (validated on Brennan 5605-08-08-08-FG = COLLAR_L 0.26, 5600-16-16-16-FG = hex stop N - 0.94, relief 1.315).
    #      The pilots show the existing BODY modules: run hex bar continuous through the crossing (+ branch hex arm, or a second continuous bar
    #      on the cross), flats normal to Z; male legs: hex stops at the 5404 end length; female legs: round collar 0.26 at the flats and the
    #      drill of the TAPDRILL column from the port face to the axis crossing (conn=None: on all three STEPs the drill reaches the crossing).
    #      The END SHAPES stay the library NPTFM / NPTFF ends, as on the accepted 5600 / 5602 / 5604 / 5605 masters - NOT the pilots' own
    #      (Brennan relief ring, simplified cone, tip chamfer, countersink; tapered port + mouth chamfer): user gate Q-TRANSFER-ENDLIB is open.
    #      'pilot' = the Brennan STEP the root is measured on; __main__ then rewrites the MODEL part of each row's $PRP@AxialSource with
    #      pilot_rows() / pilot_text() (per row). 'pilot_port' (depth of the pilot's 1.79deg tapered port, measured) and 'pilot_notes'
    #      (root-specific modelling notes) are text only.
    '5652': dict(name='Female Pipe Cross', hex='W@HEX', cross=True, ref='5652-08-08-08-08-FG', conn=None,
                 pilot='5652-08-08-08-08-FG', pilot_port=0.750,
                 legs=[('NPTFF', 'N1_1@DRIVE', 'TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1_3@DRIVE', 'TAPDRILL3@BORE', 'THDMAJ_A3@DRIVE'), ('NPTFF', 'N1_4@DRIVE', 'TAPDRILL4@BORE', 'THDMAJ_A4@DRIVE')]),
    '5603': dict(name='Female Run Pipe Tee', hex='W@REF', ref='5603-08-08-08-FG', conn=None,
                 pilot='5603-08-08-08-FG', pilot_port=0.750,
                 pilot_notes=('orientation: A1 (male run, first dash) on +X, A2 (female run) on -X, A3 (male branch) on +Y - the leg order of every '
                              'gen_tee tee; the Brennan 5603-08-08-08-FG STEP draws A1 on -X and A2 on +X: the same part turned 180deg about Y (flats '
                              'stay normal to Z), no dimension changes',),
                 legs=[('NPTFM', 'N1@DRIVE', 'D1_1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFM', 'N3@DRIVE', 'D1_3@BORE', 'THDMAJ_A3@DRIVE')]),
    '5601': dict(name='Female Branch Pipe Tee', hex='W@HEX', ref='5601-06-06-06-FG', conn=None,
                 pilot='5601-06-06-06-FG', pilot_port=0.580,
                 legs=[('NPTFM', 'N_1@DRIVE', 'D1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N2@DRIVE', 'D2@BORE', 'THDMAJ_A2@DRIVE'),
                       ('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A3@DRIVE')]),
    # ---- 90 deg elbows: 2500HX pattern (two hex arms + 30deg double-cone corner puck), legs along +X and +Y
    '2501': dict(name='90 deg Male Elbow', hex='Y@REF', elbow=True, ref='2501-08-08-FG',
                 legs=[('JICM', 'M@DRIVE', 'D@BORE', 'THDMAJ_A@DRIVE'), ('NPTFM', 'N@DRIVE', 'D1@DRILL', 'PIPEOD@DRIVE')],
                 # 2026-09-25 (user decision: fold the long variant into the base master): 2501-L rows join as extra configurations -
                 # the long NPTF leg is Air-Way N3; Brennan 2501-L-06-04-FG STEP: the forged hex arm simply runs longer (to N3 - the NPTF
                 # end length 0.56 = the 5404 value), same shape otherwise -> same topology
                 fold=[('2501L', {'N3@DRIVE': 'N@DRIVE', 'THDMAJ_B@DRIVE': 'THDMAJ_A@DRIVE', 'THDMAJ_A@DRIVE': 'PIPEOD@DRIVE', 'D1@BORE': 'D1@DRILL'}),
                       # 2026-10-02 (FOLDS): 2501-LL (extra long) rows join the same way - the long NPTF leg is Air-Way / Brennan N4 / L.
                       # Brennan 2501-LL-08-08-FG STEP (pilot), tools/measure/elbow90.py (validated on 2501-L-06-04-FG and 6500-04/-08/-12/-16-FG):
                       # forged hex arm A/F 0.875 continuous from the crossing to 2.120 = N4 2.870 - 0.750 (= ENDL[8], the 5404 -08 NPTF end
                       # length, also the 5502-08-08-FG forged male end), no step on the arm; JIC end 0.657 = the MS33656J chain -> same topology
                       ('2501LL', {'N4@DRIVE': 'N@DRIVE', 'THDMAJ_B@DRIVE': 'THDMAJ_A@DRIVE', 'THDMAJ_A@DRIVE': 'PIPEOD@DRIVE', 'D1@BORE': 'D1@DRILL'},
                        dict(why='2501-LL row folded into the 2501 master: Brennan 2501-LL-08-08-FG STEP (pilot) shows the forged hex arm simply running '
                                 'on along the pipe leg (Q-NEW-FOLD-2501LL, 2026-10-02)',
                             assume='2501-LL fold: forged hex arm runs on along the pipe leg to N4 minus the 5404 NPTF end length (Brennan '
                                    '2501-LL-08-08-FG STEP, tools/measure/elbow90.py: arm 0..2.120 continuous, end 0.750 = ENDL[8]; measured at -08-08 only)',
                             # the 2501-LL -FG rows have no OMi or Air-Way dimension (Brennan only): the generic text names the row's own source
                             src=[('A/F = max(Air-Way hex, JIC thread majors)', "A/F = max(the row's hex Y (its source: the start of this AxialSource), JIC thread majors)"),
                                  ('hex A/F raised from Air-Way ', "hex A/F raised from the row's hex Y ")]))]),
    '5500': dict(name='90 deg Male Pipe Elbow', hex='Y@REF', elbow=True, ref='5500-08-08-FG',
                 legs=[('NPTFM', 'N1@DRIVE', 'D1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N2@DRIVE', 'D2@BORE', 'THDMAJ_A2@DRIVE')]),
    '5502': dict(name='90 deg Street Pipe Elbow', hex='W@REF', elbow=True, ref='5502-08-08-FG', conn='D@BORE',
                 legs=[('NPTFM', 'N@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A2@DRIVE')]),
    '5504': dict(name='90 deg Female Pipe Elbow', hex='W@REF', elbow=True, ref='5504-08-08-FG', conn=None,
                 legs=[('NPTFF', 'N1_1@DRIVE', 'TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N1_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE')]),
    # ---- 45 deg elbows: Brennan 2504-08-08-FG body (hex arm per leg + the same 30deg puck), legs 135 deg apart.
    #      Leg 1 (male NPTF) along +X, leg 2 (JIC) along (cos135, sin135) - part numbers are JIC-NPTF, so dmap swaps them.
    '2503': dict(name='45 deg Male Elbow', hex='Y@REF', elbow=True, e45=True, dmap=(1, 0), ref='2503-08-06-FG',
                 legs=[('NPTFM', 'N2@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('JICM', 'M2@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    # 2026-10-02 (new masters from the Brennan pilot STEPs): 45 deg JIC union elbow - the STEP this e45 pattern was taken from; both legs JIC
    '2504': dict(name='45 deg Male JIC Union Elbow', hex='Y@HEX', elbow=True, e45=True, ref='2504-08-08-FG',
                 legs=[('JICM', 'M2_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M2_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE')],
                 # 2026-10-09 (wave-1 polish): the 2504 rows are filled from OMi Items (M 1 / M 2 / Hex Flat / Side IDs), not from Air-Way
                 src=[('A/F = max(Air-Way hex, JIC thread majors)', 'A/F = max(OMi Hex Flat (Y), JIC thread majors)'),
                      ('hex A/F raised from Air-Way ', 'hex A/F raised from OMi Hex Flat ')],
                 assume_extra=['Brennan 2504-08-08-FG STEP (re-measured 2026-10-02, tools/measure/forged.py): both JIC tips 0.980, hex arms end 0.323 '
                               '(= M - the 2403 -08 JIC end length 0.657), A/F 0.750, corner puck radius 0.433 = the hex corner radius, bores 0.391 = this '
                               'pattern; JIC seat / land / cone / thread major = the 2403 -08 chain, but the STEP shows NO thread relief (thread major runs '
                               'to the hex face): the model keeps the MS33656J relief of the 2403 chain, as every built tee / elbow (ASSUMPTION)']),
    # 45 deg JIC x female pipe elbow: the female port on leg 1 (+X; the angled leg carries only Thread-feature ends), JIC on the 135 deg leg;
    # PN = 2505-JIC-NPTF, so dmap swaps them (as 2503)
    '2505': dict(name='45 deg Male JIC x Female Pipe Elbow', hex='Y1@HEX', elbow=True, e45=True, dmap=(1, 0), ref='2505-08-08-FG', conn=None, p1='PORTDEPTH@BORE',
                 legs=[('NPTFF', 'N6@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE'), ('JICM', 'M2@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')],
                 conn_src='the tap drill carried to the crossing (MEASURED: Brennan 2505-08-08-FG STEP - the 0.718 drill runs from the bottom of the '
                          '0.75 deep tapered port to the axis crossing; the tapered port itself and its 45deg mouth chamfer are drawn as the tap-drill '
                          'cylinder + the Thread feature, as on every built female port)',
                 assume_extra=['Brennan 2505-08-08-FG STEP (2026-10-02, tools/measure/forged.py): JIC leg tip 1.040, its hex arm ends 0.383 (= M - the '
                               '2403 -08 JIC end length 0.657), JIC end = the 2403 -08 chain INCLUDING the thread relief (0.094 at the cone dia + 60deg '
                               'ramp); female leg face 0.940, hex arm to 0.680 then the round collar 0.260 at the flats dia; A/F 1.062, corner puck radius '
                               '0.6131 = the hex corner radius, flats normal to Z, legs 135 deg apart = the gen_tee e45 pattern (Brennan draws the JIC '
                               'leg on -X and the port at 45 deg - the same part turned)']),
    # ---- bulkhead elbows / tees (Brennan 2701-08-08-FG STEP): the bulkhead leg carries a collar (Air-Way O x K1) and the
    #      JIC bulkhead end (relief-to-tip = Air-Way i2)
    '2701': dict(name='90 deg Bulkhead Elbow', hex='Y@HEX', elbow=True, ref='2701-08-08-FG', bh=('i2@DRIVE', 'K1@DRIVE', 'O@DRIVE'),
                 legs=[('JICM', 'M3@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICBH', 'M4@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE')]),
    # bh_short (2026-10-02, BH_ARM_SHORT below): bulkhead-leg dashes whose hex arm ends BH_ARM_SHORT before the collar face (each needs
    # its BH_ARM_SHORT_SEEN entry: the date of the SolidWorks run where that arm did not rebuild)
    '2702': dict(name='45 deg Bulkhead Elbow', hex='Y@HEX', elbow=True, e45=True, ref='2702-08-08-FG', bh=('i2@DRIVE', 'K1@DRIVE', 'O@DRIVE'), bh_short=(16,),
                 legs=[('JICM', 'M2@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICBH', 'M9@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE')]),
    '2703': dict(name='Bulkhead Branch Tee', hex='Y@HEX', ref='2703-08-08-08-FG', bh=('i2@DRIVE', 'K1@DRIVE', 'O@DRIVE'), bh_short=(16,),
                 legs=[('JICM', 'M3_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M3_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('JICBH', 'M4@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    '2704': dict(name='Bulkhead Run Tee', hex='Y@HEX', ref='2704-08-08-08-FG', bh=('i2@DRIVE', 'K1@DRIVE', 'O@DRIVE'),
                 legs=[('JICM', 'M3_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICBH', 'M4@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('JICM', 'M3_3@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    # ---- female JIC SWIVEL families (Brennan 6500-04/-08/-12/-16-FG STEPs: nut + nose measured, one solid)
    '6500': dict(name='90 deg Female Swivel Elbow', hex='Y@REF', elbow=True, ref='6500-12-12-FG', sw=('LEG_M10@DRIVE', 'HEXB@HEX'),
                 legs=[('JICM', 'LEG_M@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('JICSW', 'LEG_M5@DRIVE', 'D2@BORE', 'THDMAJ_B@DRIVE')],
                 # 2026-10-02 (FOLDS): 6500-L (long) rows join as extra configurations. Brennan 6500-L-08-08-FG STEP (pilot) vs 6500-08-08-FG:
                 # tools/measure/swiv.py -> swivel end = SWIV_MEAS[8] exactly (nut, skirt, neck, body face 0.885 behind the nut face, thread,
                 # nose, seat); tools/measure/elbow90.py -> JIC leg identical, swivel hex arm continuous from the crossing to 1.925 (6500:
                 # 0.495) - the whole extra length (2.81 - 1.38 = 1.430) is the forged swivel hex arm; STEP volume difference 0.52492 in^3
                 # = 1.430 x (hex A/F 0.75 - bore 0.391 section) 0.52491 -> same topology. 6500L column M9 = crossing to the swivel-nut face
                 # (OMi 'M 2 Size' = Brennan catalog M6), M12 = crossing to the nose tip (OMi 'M 1 Size' = Brennan M4), M = male JIC leg
                 fold=[('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX',
                                  'THDMAJ_B1@DRIVE': 'THDMAJ_A@DRIVE', 'THDMAJ_B2@DRIVE': 'THDMAJ_B@DRIVE'},
                        dict(why='6500-L row folded into the 6500 master: Brennan 6500-L-08-08-FG STEP (pilot) = 6500-08-08-FG with the forged '
                                 'swivel hex arm 1.430 longer (Q-NEW-FOLD-6500L, 2026-10-02)',
                             assume='6500-L fold: the extra length is the forged swivel hex arm, the swivel end is the 6500 one of the same size '
                                    '(Brennan 6500-L-08-08-FG STEP, tools/measure/swiv.py + elbow90.py: swivel end = SWIV_MEAS[8], arm 0..1.925 '
                                    'continuous; measured at -08 only, ASSUMED for the other sizes)',
                             # the 6500-L -FG rows are filled from OMi Items (M 1 / M 2 / Hex Flat / Nut Hex 1), not from Air-Way: the generic
                             # 6500 text names OMi instead (a 6500-L row filled from another source would need its own wording here)
                             src=[('A/F = max(Air-Way hex, JIC thread majors)', 'A/F = max(OMi Hex Flat (Y), JIC thread majors)'),
                                  ('hex A/F raised from Air-Way ', 'hex A/F raised from OMi Hex Flat '),
                                  ('swivel nut hex = Air-Way C3', 'swivel nut hex = OMi Nut Hex 1 (CHEX)'),
                                  ('nose tip at Air-Way L minus the to-seat length (Brennan within 0.01)', 'nose tip at OMi M 1 Size (M12)'),
                                  ('swivel leg length = Air-Way M5 (crossing to the nut face), nose tip at Air-Way M10',
                                   'swivel leg length = OMi M 2 Size (M9, crossing to the nut face), nose tip at OMi M 1 Size (M12, crossing to the nose tip)'),
                                  ('Air-Way nut-face-to-seat', 'OMi nut-face-to-nose-tip (M 2 - M 1)'),
                                  ('Air-Way nut hex C3', 'OMi Nut Hex 1')]))]),
    '6501': dict(name='90 deg Male Pipe x Female Swivel Elbow', hex='Y@HEX', elbow=True, ref='6501-04-04-FG', sw=('M10@DRIVE', 'C3HEX@HEX'),
                 legs=[('NPTFM', 'N@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('JICSW', 'M5@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '6503': dict(name='90 deg Female Pipe x Female Swivel Elbow', hex='Y1@HEX', elbow=True, ref='6503-08-08-FG', conn='D@BORE', sw=('M10@DRIVE', 'C3HEX@HEX'),
                 legs=[('NPTFF', 'N1@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE'), ('JICSW', 'M5@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '6502': dict(name='45 deg Male JIC x Female Swivel Elbow', hex='Y@HEX', elbow=True, e45=True, dmap=(1, 0), ref='6502-08-08-FG', sw=('M14@DRIVE', 'C3HEX@HEX'),
                 legs=[('JICSW', 'M6@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'), ('JICM', 'M2@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE')]),
    '6600': dict(name='Female Swivel Branch Tee', hex='Y@HEX', ref='6600-08-08-08-FG', sw=('M10@DRIVE', 'C3HEX@HEX'),
                 legs=[('JICM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICM', 'M2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('JICSW', 'M5@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    # ---- female NPSM (pipe) SWIVEL elbows (Brennan 1404-08-08 STEP: nut + stem, one solid; swivel size -08 only)
    '1501': dict(name='90 deg Male Pipe x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, ref='1501-08-08-FG', npsm=('W3@HEX', 'CHEX@HEX'),
                 legs=[('NPTFM', 'N1@DRIVE', 'D2@BORE', 'THDMAJ_A@DRIVE'), ('NPSMSW', 'M1@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE')]),
    # 2026-10-18 (ANGLED, genfeat): 1503 gains the angled helix (male pipe end on the 135 deg leg) and the NPSM neck turn (neck_turn, N1 / N2:
    # the 6502 NECKTRIM / NECKFILL on the +X NPSM swivel + the slot test on what the corner really reaches - Q-ANGLED-NECKNPSM settled from the
    # Brennan 1503-08-08-FG / 1503-12-08-FG / 1504-06-06-FG STEPs, ANGLED_NECK_ASSUME)
    '1503': dict(name='45 deg Male Pipe x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='1503-08-08-FG', npsm=('W2@HEX', 'CHEX@HEX'),
                 neck_turn=True,
                 legs=[('NPSMSW', 'M@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N@DRIVE', 'D2@BORE', 'THDMAJ_A@DRIVE')]),
    # ---- 2026-10-18 (ANGLED, genfeat; capabilities Q-NEW-ANGLEDHELIX / -ANGLEDFEMALE / -ANGLEDNUT approved 2026-10-08, design
    #      tools/_out/wave2_shapes_20261008/ANGLED/DESIGN.md): 45 deg elbows whose 135 deg leg carries a helical thread (male / female NPTF, swivel-nut
    #      thread: HelixThreadV), a female pipe port (BoreCutV pocket + collar) or a swivel nut (NutHexCutV). The adjustable ORB leg and an NPSM swivel
    #      that needs the neck turn stay on +X (their locknut cut / ORBTRIM / NeckRing are +X-only and proven there).
    #      p1 = 'PORTDEPTH@BORE': a row's own Brennan port depth where the MS51503 P1 library value does not fit the short 45 deg leg (Q-ANGLED-P1,
    #      settled from the Brennan STEPs 2026-10-18 - the per-size port depth Brennan draws, ANGLED_P1_NOTE); the library value everywhere else.
    '1504': dict(name='45 deg Female Pipe x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='1504-06-06-FG',
                 conn=None, npsm=('W2@HEX', 'CHEX@HEX'), neck_turn=True, p1='PORTDEPTH@BORE',
                 nptff_text='ANGLED_NPTFF',
                 legs=[('NPSMSW', 'M@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N2@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE')]),
    '5501': dict(name='45 deg Male Pipe Elbow', hex='Y@HEX', elbow=True, e45=True, ref='5501-08-08-FG',
                 legs=[('NPTFM', 'N4@DRIVE', 'D1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N6@DRIVE', 'D2@BORE', 'THDMAJ_A2@DRIVE')]),
    # 5503: the female port's tap drill runs from the port face to the axis crossing and ends flat there (conn=None) - Brennan 5503-16-16-FG STEP
    # (OCP, angled/ocp/cmp_5503-16-16-FG.json: drill 1.156 from the port bottom 0.94 deep to the crossing); the male bore D runs from the male tip
    '5503': dict(name='45 deg Street Pipe Elbow', hex='W@HEX', elbow=True, e45=True, dmap=(1, 0), ref='5503-16-16-FG', conn=None, p1='PORTDEPTH@BORE',
                 nptff_text='ANGLED_NPTFF',
                 legs=[('NPTFF', 'N3@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A2@DRIVE'), ('NPTFM', 'N4@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE')]),
    '5505': dict(name='45 deg Female Pipe Elbow', hex='W@HEX', elbow=True, e45=True, ref='5505-20-20-FG', conn=None, p1='PORTDEPTH@BORE',
                 nptff_text='ANGLED_NPTFF',
                 legs=[('NPTFF', 'N2_1@DRIVE', 'TAPDRILL1@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFF', 'N2_2@DRIVE', 'TAPDRILL2@BORE', 'THDMAJ_A2@DRIVE')]),
    # adjustable ORB leg on +X (first dash), swivel on the 135 deg leg; the adjustable-ORB end cells Air-Way does not print for 6810 / 6902 come
    # from the Air-Way 6801 rows of the same ORB size ('=6801' in nwo positions 1, 3, 4: I3 checked = Brennan 6801, as 6803 / 6804; thread length
    # and groove dia, Q-TRANSFER-ENDLIB = yes 2026-10-08). No neck turn on the 135 deg leg (NeckRing is +X-only; the 6902 corner stays inside the neck).
    '6810': dict(name='45 deg Adjustable Male ORB x Female JIC Swivel Elbow', hex='Y@HEX', elbow=True, e45=True, ref='6810-12-12-NWO-FG',
                 sw=('M20@DRIVE', 'C3HEX@HEX'), nwo=('=6801', 'C4HEX@HEX', '=6801', '=6801'),
                 legs=[('NWO', 'M8@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICSW', 'M19@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE')]),
    '6902': dict(name='45 deg Adjustable Male ORB x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, e45=True, ref='6902-12-12-NWO-FG',
                 npsm=('W2@HEX', 'CHEX@HEX'), nwo=('=6801', 'C4HEX@HEX', '=6801', '=6801'),
                 legs=[('NWO', 'N4@DRIVE', 'D1@BORE', 'THDMAJ_B@DRIVE'), ('NPSMSW', 'M@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE')]),
    # 2026-10-02 (new master 1502; user 2026-10-02 "yes, go ahead": new masters from the pilot STEPs): 90 deg female pipe x female NPSM swivel
    # FORGED elbow. Pilot Brennan 1502-08-08-FG STEP, measured with tools/measure/fgelbow.py + npsm.py --leg 1,1 (validated first on 2500-06-06-FG,
    # 5504-08-08-FG, 5502-04/-08/-16-FG, 2502-06-04-FG, 5405-08-08 and the 9 1404 STEPs): the 2500HX elbow body (hex arms, flats normal to Z,
    # 30deg corner puck about Z, radius = hex corner, within 0.0001), the 5504 forged female pipe leg (hex arm to 0.26 short of the port face,
    # round collar dia = the hex flats; tap drill running on below the thread to the crossing) and the 1501 / 1404 NPSM swivel leg (= NPSM_MEAS[8]
    # on every value; body face 0.48 behind the stem tip) - only existing modules. Leg 1 (+X) = the female pipe end (first dash), leg 2 (+Y) = the
    # NPSM swivel (second dash); Brennan draws the pipe leg along -X (mirror image, same part). N3 = port face to the swivel axis, M1 = pipe axis
    # to the stem tip, W3 = pipe axis to the nut face (Air-Way letters = Brennan TFA p21 L / M / M1 on the pilot).
    # npsm_bodyface: per size (leg dashes) - the body face is measured on an elbow forging only at 1502-08-08-FG; every other size keeps the
    # 1404 straight value as an ASSUMPTION (review 2026-10-02). arm_ridge_check: see build_rows (the other arm's corner beyond the body face).
    '1502': dict(name='90 deg Female Pipe x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, ref='1502-08-08-FG', conn=None, npsm=('W3@HEX', 'CHEX@HEX'),
                 npsm_bodyface={(8, 8): 'CONFIRMED on the Brennan 1502-08-08-FG elbow forging: its hex arm ends 0.48 behind the stem tip, at 0.76 from the crossing',
                                'other': 'ASSUMED for the elbow forging of this size: measured on an elbow forging only at 1502-08-08-FG (hex arm ends 0.48 behind '
                                         'the stem tip = the 1404-08 straight); no 1502 forging of this size measured'},
                 arm_ridge_check=True,
                 # 2026-10-09 (wave-1 polish): texts name Air-Way only - the built 1502 rows are Air-Way rows; the own-file pilot
                 # 1502-08-08-FG is held (ruling 2026-10-08). Re-word these if a row from another source is ever built.
                 assume_reps=(('forged elbow body per the 2500HX pattern (Brennan 2500-06-06-FG STEP)',
                               'forged elbow body per the 2500HX pattern (Brennan 2500-06-06-FG STEP; CONFIRMED on the pilot Brennan 1502-08-08-FG STEP, '
                               'tools/measure/fgelbow.py: hex arms with flats normal to Z, corner = 30deg double cone about Z of the hex corner radius, within 0.0001)'),
                              ('A/F = max(Air-Way hex, JIC thread majors)', 'A/F = the row body hex C1HEX (Air-Way; no JIC leg)'),
                              ('nut hex = Air-Way C(2) (must equal the Brennan nut, checked per row)', 'nut hex = the row CHEX (must equal the Brennan nut, checked per row)'),
                              ('NUT FACE AT AIR-WAY W3 AND STEM TIP AT AIR-WAY M1/M (crossing to the stem tip) (user decision 2026-09-24: follow Air-Way - at -08 '
                               'Air-Way W-L 0.33 vs Brennan 0.28, so the nut sits 0.05 further out than on the Brennan part)',
                               'NUT FACE AT THE ROW W3 AND STEM TIP AT THE ROW M1 (pipe-leg axis to the nut face / to the stem tip; Air-Way; shape check: the '
                               'Brennan 1502-08-08-FG part has W3 - M1 = 0.28); where W3 - M1 differs from the Brennan 1404 nut-face-to-stem-tip '
                               'the row is followed (user decision 2026-09-24) and the row carries a warning')),
                 nptff_text=('female NPTF leg: tap drill = the row TAPDRILL (Air-Way) from the '
                             'port face to the axis crossing, tapered helical thread over MS51503 P1 max (' + BR5405 + ') - the Brennan 1502-08-08-FG and '
                             '5504-08-08-FG STEPs show this tap drill running on below the thread to the crossing (Brennan 1502: it ends in a ball 0.23 past '
                             'the crossing, at the far wall of the NPSM bore; modelled with a flat end at the crossing: ASSUMPTION, the NPSM bore opens into it); '
                             'the thread-zone minor cone (1.79deg, -08: dia 0.791 -> 0.747 over 0.75 deep) and the 45deg port-mouth chamfer are NOT modelled '
                             '(the helical thread represents the thread zone; its length is MS51503 P1 max, 0.90 at -08, vs the Brennan thread zone 0.75)'),
                 legs=[('NPTFF', 'N3@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE'), ('NPSMSW', 'M1@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE')]),
    '6602': dict(name='Female Swivel Run Tee', hex='Y@HEX', ref='6602-08-08-08-FG', sw=('M10@DRIVE', 'C3HEX@HEX'),
                 legs=[('JICM', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE'), ('JICSW', 'M5@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE'),
                       ('JICM', 'M3@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    # ---- ADJUSTABLE male ORB families (Brennan 6801-XX-XX-NWO-FG STEPs, 12 sizes): forged elbow body + NWO leg (nut, washer, undercut, thread)
    #      nwo = (tip-to-body-face, locknut hex, ORB thread length, O-ring groove/undercut dia)
    # 45 deg: the adjustable ORB leg along +X (its locknut cut needs an axis-aligned leg), the JIC leg on the 135 deg axis; PN = 6802-JIC-ORB
    '6802': dict(name='45 deg Male JIC x Adjustable Male ORB Elbow', hex='Y@REF', elbow=True, e45=True, dmap=(1, 0), ref='6802-08-08-NWO-FG',
                 nwo=('ORB_I3@DRIVE', 'HEXB@HEX', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'),
                 legs=[('NWO', 'LEG_ORB@DRIVE', 'D2@BORE', 'THDMAJ_B@DRIVE'), ('JICM', 'LEG_JIC@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE')]),
    # tees: Air-Way prints no I3 for 6803/6804 -> the 6801 adjustable-end I3 of the same ORB size ('=6801', checked = Brennan 6801 STEP)
    '6803': dict(name='Male JIC Run x Adjustable Male ORB Branch Tee', hex='Y@REF', ref='6803-08-08-08-NWO-FG',
                 nwo=('=6801', 'HEXB@HEX', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'),
                 legs=[('JICM', 'LEG1@DRIVE', 'D1@BORE', 'THDMAJ_1@DRIVE'), ('JICM', 'LEG2@DRIVE', 'D2@BORE', 'THDMAJ_2@DRIVE'),
                       ('NWO', 'LEG3@DRIVE', 'D3@BORE', 'THDMAJ_3@DRIVE')]),
    '6804': dict(name='Male JIC x Adjustable Male ORB Run Tee', hex='Y@REF', ref='6804-08-08-08-NWO-FG',
                 nwo=('=6801', 'HEXB@HEX', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'),
                 legs=[('JICM', 'LEG1@DRIVE', 'D1@BORE', 'THDMAJ_1@DRIVE'), ('NWO', 'LEG2@DRIVE', 'D2@BORE', 'THDMAJ_2@DRIVE'),
                       ('JICM', 'LEG3@DRIVE', 'D3@BORE', 'THDMAJ_3@DRIVE')]),
    '6801': dict(name='90 deg Male JIC x Adjustable Male ORB Elbow', hex='Y@REF', elbow=True, ref='6801-08-08-NWO-FG',
                 nwo=('ORB_I3@DRIVE', 'HEXB@HEX', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE'),
                 legs=[('JICM', 'LEG_JIC@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('NWO', 'LEG_ORB@DRIVE', 'D2@BORE', 'THDMAJ_B@DRIVE')]),
    # ---- 2026-10-09 wave 2, PERLEGSW (Q-NEW-PERLEGSW, user 2026-10-08 "yes go ahead"): several swivel / NPSM swivel / adjustable-ORB legs on
    #      one forged body. A leg tuple may carry a 5th element = the column tuple of ITS end (layout of the SPEC-wide sw / npsm / nwo); a
    #      4-tuple leg reads the SPEC-wide tuple, so every older root is unchanged. A value is a table column or an END-LIBRARY token (end_val;
    #      Q-TRANSFER-ENDLIB = yes, user 2026-10-08): '=6801' (adjustable-ORB I3 = Air-Way 6801 ORB_I3), '=ORB:THDL' / '=ORB:GD' (ORB end
    #      library thread length / undercut dia), '=FPT:TD' (female pipe tap drill, only where the row's cell is empty). perleg=True switches on
    #      the per-leg checks and wording (nut-cut slabs of every nut, envelope overlap, arm ridge on tees, NWO legs in the ridge checks).
    # 6807: only 6807-06-06-NWO-FG has an allowed size source - its own Air-Way -FG row (s140 "6807-6-6 NWO-FG"); OMi Items row 2299 lists the
    # part with no dimension. Body form ASSUMED from the 6801 forging until a 6807 STEP is seen (DESIGN_REVIEW P6: dry run now, ship gated).
    '6807': dict(name='90 deg Adjustable Male ORB x Adjustable Male ORB Elbow', hex='Y@HEX', elbow=True, perleg=True, arm_ridge_check=True,
                 ref='6807-06-06-NWO-FG',
                 assume_extra=['two adjustable ORB legs on one 90 deg elbow forging (OMi "MAORB - MAORB 90 deg Elbow Forged"; no Brennan 6807 STEP seen: '
                               'the body form - 2500HX hex arms + 30deg corner puck, each ORB leg = the ORB leg of the accepted 6801 forging - is ASSUMED '
                               'from the Brennan 6801-XX-XX-NWO-FG STEPs, shape only)'],
                 legs=[('NWO', 'M7_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE', ('=6801', 'C4_1HEX@HEX', '=ORB:THDL', '=ORB:GD')),
                       ('NWO', 'M7_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE', ('=6801', 'C4_2HEX@HEX', '=ORB:THDL', '=ORB:GD'))]),
    # ---- 2026-10-18 (genfeat PERLEGSW, Q-NEW-PERLEGSW approved 2026-10-08): the tees with several female swivel / NPSM swivel legs, out of
    #      SPEC_WAITING now that rows have sizes: the Brennan TFA catalog (user 2026-10-18 "Brennan = yes"; tables 1601 / 1602 / 1603 / 6606,
    #      cells tools/_out/brennan_yes_20261018/wave2/tee_elbow/cells.csv) and, for 1602-02/-04/-08/-16/-20-FG, OMi's own 2026-10-18 drawings.
    #      Body = the 2603HX tee (run hex bar continuous through the crossing + branch hex arm, flats normal to Z), every special leg = the
    #      library end (SWIV_MEAS / NPSM_MEAS, Q-TRANSFER-ENDLIB), its hex arm ending at the library body face - the shape seen on the Brennan
    #      6603-06-06-06-FG / 6606-06-06-06-FG / 1601-08-08-08-FG / 1603-08-08-08-FG tee forgings (shape only, PERLEGSW DESIGN section 3).
    #      Column meanings: JIC swivel legs: leg col = crossing to the nut face (Brennan M6 / Air-Way M5), extra = (crossing to the nose tip
    #      M10, nut hex C3); NPSM legs: leg col = crossing to the stem tip (Brennan M1 / M2), extra = (crossing to the nut face W3 / W5 =
    #      Brennan M / L, nut hex).
    '6606': dict(name='Female Swivel Tee (three swivels)', hex='Y@HEX', perleg=True, arm_ridge_check=True, ref='6606-08-08-08-FG',
                 legs=[('JICSW', f'M5_{k}@DRIVE', 'D1@BORE', f'THDMAJ_B{k}@DRIVE', (f'M10_{k}@DRIVE', f'C3_{k}HEX@HEX')) for k in (1, 2, 3)]),
    # 1601 / 1602: the first dash is the pipe branch (Air-Way 1601-06-04-04: A = 3/8 NPTF; Brennan A1 = the NPTF branch) -> dmap; every -FG
    # BUILD row has equal dashes today
    '1601': dict(name='Female NPSM Swivel Run x Male Pipe Branch Tee', hex='C1HEX@HEX', perleg=True, arm_ridge_check=True, dmap=(1, 2, 0),
                 ref='1601-08-08-08-FG',
                 legs=[('NPSMSW', 'M1_2@DRIVE', 'D_2@BORE', 'THDMAJ_A1_2@DRIVE', ('W3_2@HEX', 'C2HEX@HEX')),
                       ('NPSMSW', 'M1_3@DRIVE', 'D3@BORE', 'THDMAJ_A1_3@DRIVE', ('W3_3@HEX', 'C3HEX@HEX')),
                       ('NPTFM', 'N1@DRIVE', 'D2@BORE', 'THDMAJ_A@DRIVE')]),
    '1602': dict(name='Female NPSM Swivel Run x Female Pipe Branch Tee', hex='C1HEX@HEX', perleg=True, arm_ridge_check=True, dmap=(1, 2, 0),
                 conn=None, ref='1602-08-08-08-FG',
                 legs=[('NPSMSW', 'M1_2@DRIVE', 'D2@BORE', 'THDMAJ_A1_2@DRIVE', ('W3_2@HEX', 'C2HEX@HEX')),
                       ('NPSMSW', 'M1_3@DRIVE', 'D3@BORE', 'THDMAJ_A1_3@DRIVE', ('W3_3@HEX', 'C3HEX@HEX')),
                       ('NPTFF', 'N3@DRIVE', 'TAPDRILL@BORE', 'THDMAJ_A@DRIVE')]),          # an empty TAPDRILL takes '=FPT:TD' (end library)
    # 1603: side 1 = the branch: the leg Air-Way prints differently (W3 / M1 vs W5 / M2 at -04); the Brennan TFA 1603 table labels A1's nut face
    # L (axis to the A1 branch nut face) and A2 / A3 the run (M, M1 / M2) - still logged as an ASSUMPTION (every -FG row has equal dashes)
    '1603': dict(name='Female NPSM Swivel Tee (three swivels)', hex='C1HEX@HEX', perleg=True, arm_ridge_check=True, dmap=(1, 2, 0),
                 ref='1603-06-06-06-FG',
                 assume_extra=['1603 side order: part-number side 1 (W3 / M1) = the branch leg, sides 2 / 3 (W5 / M2) = the run (ASSUMPTION: Air-Way prints '
                               'side 1 differently, the Brennan TFA 1603 table labels A1 as the branch; every -FG row has equal dashes)'],
                 legs=[('NPSMSW', 'M2_2@DRIVE', 'D2@BORE', 'THDMAJ_A1_2@DRIVE', ('W5_2@HEX', 'C2HEX@HEX')),
                       ('NPSMSW', 'M2_3@DRIVE', 'D2@BORE', 'THDMAJ_A1_3@DRIVE', ('W5_3@HEX', 'C3HEX@HEX')),
                       ('NPSMSW', 'M1@DRIVE', 'D1@BORE', 'THDMAJ_A1_1@DRIVE', ('W3@HEX', 'C_1HEX@HEX'))]),
    # ---- 2026-10-18 genfeat HOSEB (Q-NEW-HOSEB, user 2026-10-08 "yes go ahead"; port of wave2_impl_20261009): beaded hose-barb leg on forged
    #      elbows = the straight 4404 / 4604 end (gen_straight2.end_HOSEB) ported to a leg (leg_HOSEB). hoseb = (stub OD column, bead dia column);
    #      hose_bore = where the hose-leg bore comes from (Q-HOSEB-BORE, user 2026-10-18 A15):
    #        'own'   the HOSEB leg's bore column is the part's single bore, carried through both legs (option (a): 4601 / 4603);
    #        'col'   the HOSEB leg's bore column is the part's own hose drill (DH@BORE = Brennan TFA B1 DRILL, "look at Brennan": 4501 / 4503);
    #                a row with that cell empty is skipped;
    #        '=4404' the Air-Way 4404 equal-size through bore (option (b), not chosen); None = no source (rows skipped).
    #      hose_dh = per-row fallback of an 'own' root: where the row has this hose-drill column filled (DH@BORE, Brennan B1 DRILL, A15 "look at
    #                Brennan"), the hose leg takes it; rows without it stay on 'own' (4601-16-20-NWO-FG: bore 1.078 > the 1.000 stub under (a)).
    #      pn = the column that names the configuration (OMi SKU form: the Air-Way review rows spell '4601-06-06 NWO-FG', which dashes() cannot
    #      parse). nwo: '=ORB:THDL' / '=ORB:GD' = the ORB end library (hoseb_endlib; Q-TRANSFER-ENDLIB). The threaded leg stays axis-aligned
    #      (+X / +Y): on the 45 deg elbows the 135 deg leg is the hose leg (no thread -> no angled helix). The forged corner past the hose hex
    #      face is faced off (HOSEFACEi / STUBFILLi) in every configuration.
    '4601': dict(name='90 deg Adjustable Male ORB x Beaded Hose Elbow', hex='Y@HEX', elbow=True, ref='4601-08-08-NWO-FG', hoseb=('$PRP@TubeOD', 'AA@DRIVE'),
                 hose_bore='own', hose_dh='DH@BORE', pn='$PRP@OMiSKU', nwo=('=6801', 'C4HEX@HEX', '=ORB:THDL', '=ORB:GD'),
                 legs=[('HOSEB', 'L4@DRIVE', 'D@BORE', None), ('NWO', 'M7@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '4603': dict(name='45 deg Adjustable Male ORB x Beaded Hose Elbow', hex='CHEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='4603-08-08-NWO-FG',
                 hoseb=('$PRP@TubeOD', 'AA@DRIVE'), hose_bore='own', hose_dh='DH@BORE', pn='$PRP@OMiSKU', nwo=('=6801', 'C4HEX@HEX', '=ORB:THDL', '=ORB:GD'),
                 legs=[('NWO', 'M8@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE'), ('HOSEB', 'L5@DRIVE', 'D@BORE', None)]),
    # 4501 / 4503: the single bore D1 is the PIPE-end drill (Brennan A2 DRILL; 0.030 wall through the 2.000 stub on 4501-32-32-FG) - the hose
    # leg reads its own drill DH (Brennan B1 DRILL). 4501-32-32-FG (Air-Way row) has no DH cell: skipped until it gets one.
    '4501': dict(name='90 deg Male Pipe x Beaded Hose Elbow', hex='Y@HEX', elbow=True, ref='4501-08-08-FG', hoseb=('$PRP@TubeOD', 'AA@DRIVE'), hose_bore='col',
                 legs=[('HOSEB', 'L4@DRIVE', 'DH@BORE', None), ('NPTFM', 'N@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE')]),
    '4503': dict(name='45 deg Male Pipe x Beaded Hose Elbow', hex='CHEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='4503-08-08-FG',
                 hoseb=('$PRP@TubeOD', 'AA@DRIVE'), hose_bore='col',
                 legs=[('NPTFM', 'N2@DRIVE', 'D1@BORE', 'THDMAJ_A@DRIVE'), ('HOSEB', 'L5@DRIVE', 'DH@BORE', None)]),
    # ---- 2026-10-18 (genfeat flange): SAE code 61 / code 62 FLANGE LEG on the forged elbows (Q-NEW-FLG61LEG approved 2026-10-08; Q-NEW-FLG62LEG
    #      user 2026-10-18 A17). Design tools/_out/wave2_shapes_20261008/FLG61LEG/DESIGN.md: the flange is leg 1 on +X (axis-aligned, unthreaded),
    #      the JIC leg 2 (+Y on 90 deg, the 135 deg axis on 45 deg); PN = <root>-JIC-FLANGE, so dmap swaps them (as 2503 / 2505 / 6802). Brennan
    #      1703-24-24-FG / 1704-24-24-FG / 1804-08-08-FG STEPs: the 2500HX / 2504 forged body with the 1700 (code 61) / 1800 (code 62) head on the
    #      flange leg. Per-leg bores: the flange leg reads DFLG@BORE, the JIC leg D@BORE (own STEPs: 1.260 / 1.312 at -24). flg_o = the row's head
    #      OD column, cross-checked against the end library (FLG_O). assume_reps: the rows are not Air-Way rows - the shared elbow sentence names
    #      the row's own hex source instead.
    '1703': dict(name='45 deg Male JIC x SAE Code 61 Flange Elbow (forged)', hex='CHEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='1703-24-24-FG', flg_o='O@DRIVE',
                 assume_reps=(('A/F = max(Air-Way hex, JIC thread majors)', "A/F = max(the row hex A/F (its source: the start of this AxialSource), JIC thread majors)"),),
                 legs=[('FLG61', 'N3@DRIVE', 'DFLG@BORE', None), ('JICM', 'M2@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '1704': dict(name='90 deg Male JIC x SAE Code 61 Flange Elbow (forged)', hex='Y@HEX', elbow=True, dmap=(1, 0), ref='1704-24-24-FG', flg_o='O@DRIVE',
                 assume_reps=(('A/F = max(Air-Way hex, JIC thread majors)', "A/F = max(the row hex A/F (its source: the start of this AxialSource), JIC thread majors)"),),
                 legs=[('FLG61', 'N2@DRIVE', 'DFLG@BORE', None), ('JICM', 'M@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '1803': dict(name='45 deg Male JIC x SAE Code 62 Flange Elbow (forged)', hex='CHEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='1803-08-08-FG', flg_o='O@DRIVE',
                 assume_reps=(('A/F = max(Air-Way hex, JIC thread majors)', "A/F = max(the row hex A/F (its source: the start of this AxialSource), JIC thread majors)"),),
                 legs=[('FLG62', 'N3@DRIVE', 'DFLG@BORE', None), ('JICM', 'M2@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
    '1804': dict(name='90 deg Male JIC x SAE Code 62 Flange Elbow (forged)', hex='Y@HEX', elbow=True, dmap=(1, 0), ref='1804-08-08-FG', flg_o='O@DRIVE',
                 assume_reps=(('A/F = max(Air-Way hex, JIC thread majors)', "A/F = max(the row hex A/F (its source: the start of this AxialSource), JIC thread majors)"),),
                 legs=[('FLG62', 'N2@DRIVE', 'DFLG@BORE', None), ('JICM', 'M@DRIVE', 'D@BORE', 'THDMAJ_B@DRIVE')]),
}
# 2026-10-09 wave 2: families whose capability is implemented but which have NO buildable row (no allowed body-size source: OMi Items carry
# no dimension, Air-Way only the non-forged twin, Brennan-only sizes not allowed - user decisions 2026-10-08). Outside the generator loop;
# the TEST harnesses read them (rows copied from built siblings, never shipped). The ship that brings a root's first row moves it into SPEC.
# 2026-10-18 (genfeat PERLEGSW): 1601 / 1602 / 1603 / 6606 moved into SPEC (rows from the Brennan TFA catalog, user 2026-10-18 "Brennan =
# yes", and the 1602-FG rows from OMi's 2026-10-18 drawings); 6603 / 6566 still have no data-complete row.
SPEC_WAITING = {
    # PERLEGSW. Column meanings (Air-Way headers): JIC swivel legs: leg col = crossing to the nut face (M5), extra = (crossing to the nose tip
    # M10, nut hex C3); NPSM legs: leg col = crossing to the stem tip, extra = (crossing to the nut face, nut hex).
    '6603': dict(name='Female Swivel Run x Male JIC Branch Tee', hex='Y@HEX', perleg=True, arm_ridge_check=True, ref='6603-06-06-06-FG',
                 legs=[('JICSW', 'M5_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE', ('M10_1@DRIVE', 'C3_1HEX@HEX')),
                       ('JICSW', 'M5_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE', ('M10_2@DRIVE', 'C3_2HEX@HEX')),
                       ('JICM', 'M@DRIVE', 'D3@BORE', 'THDMAJ_B3@DRIVE')]),
    # 6566: the review table is a skeleton (no Air-Way series). These column names are a PLACEHOLDER for the TEST harness only - not staged in
    # any table (DESIGN_REVIEW P10). Open: OMi gives one M 1 / M 2 pair for two swivel legs (6500-L fold: M 2 = crossing to the nut face,
    # M 1 = crossing to the nose tip) - the leg mapping is a question for when data arrives.
    '6566': dict(name='90 deg Female Swivel x Female Swivel Elbow', hex='Y@HEX', elbow=True, perleg=True, arm_ridge_check=True, ref='6566-06-06-FG',
                 legs=[('JICSW', 'M5_1@DRIVE', 'D1@BORE', 'THDMAJ_B1@DRIVE', ('M10_1@DRIVE', 'C3_1HEX@HEX')),
                       ('JICSW', 'M5_2@DRIVE', 'D2@BORE', 'THDMAJ_B2@DRIVE', ('M10_2@DRIVE', 'C3_2HEX@HEX'))]),
}
# leg placement: (axis 0=X 1=Y, sign)
PLACE = {1: (0, +1), 2: (0, -1), 3: (1, +1), 4: (1, -1)}
PLACE_ELBOW = {1: (0, +1), 2: (1, +1)}
PLACE_E45 = {1: (0, +1), 2: ('U', +1)}
UXV, UYV = math.cos(math.radians(135)), math.sin(math.radians(135))
TAN30 = math.tan(math.radians(30))
# 2026-10-09 (puck audit): the corner PUCK sits PUCK_INSET radially inside the hex corners (equator AC - PUCK_INSET, 30 deg cones kept).
# With the equator exactly on the hex corner radius its section through Z equals the hex-arm end face, the faces coincide and SolidWorks
# silently dropped the puck from the union in some configurations (no error; the outer corner stayed square: 2504-04-04 / -06-06-FG,
# 6500-L-04-04 / -L-06-06-FG, 6500-06-06-FG, 2501-06-02 / -L-06-04-FG). A construction margin, not a part dimension.
PUCK_INSET = 0.0005
COLLAR_L = 0.26      # female pipe port collar length, Brennan-measured (constant at -04/-08/-16)
# 2026-10-02 (user decision "OK to stop the bulkhead hex arm 0.001 in short of the collar", PROJECT_STATUS section 3 item 1;
# 00_DOCS/OVERNIGHT_BUILD_2026-09-25.md "The 2 held-back parts"): a JICBH leg's hex arm ends exactly on the bulkhead collar face
# (hexl = M - i2 - K1). At -16 on 2702 / 2703 that arm does not rebuild in SolidWorks: HEX2_BODY (2702) / HEX3_BODY (2703) fail
# (2026-09-25 overnight build: HEXL 0.870 fails, 0.869 and 0.871 rebuild; 2703: 1.110 fails, 1.109 / 1.111 rebuild). The cause is not
# fully known: there the collar circle (radius O/2) lies between the hex flats and corners, so hex end face and collar face share the
# plane with crossing outlines - but the same crossing BUILDS at 2702 -10 / -12, 2703 -12 / -12-LN and on the accepted 2704 -10 / -12 /
# -16 (2704-16-16-16 has the 2703-16 numbers; its arm is one end of the HexRun bar). So the crossing is necessary, not sufficient, and
# is only a guard here. Where it applies the hex arm ends BH_ARM_SHORT before the collar face; the revolved leg core (0.02 inside the
# flats) runs on to the collar, so the solid stays one body with a BH_ARM_SHORT wide round neck between hex and collar (the core is
# NOT hidden by the hex over that band). Applied ONLY to the bulkhead-leg dashes a SPEC lists in 'bh_short' (the SolidWorks-proven
# failures) and only where the arm would otherwise end on the collar face with crossing outlines: every other configuration
# (2701 / 2704, 2702 / 2703 -04 ... -12, which build) keeps its hex arm unchanged.
BH_ARM_SHORT = 0.001
# {root: {dash: date of the SolidWorks run in which that bulkhead hex arm, ending on the collar face, did not rebuild}} - goes into the
# $PRP@AxialSource / $COMMENT of every row the offset touches. A dash added to a SPEC's bh_short needs its entry here (asserted).
BH_ARM_SHORT_SEEN = {'2702': {16: '2026-09-25'}, '2703': {16: '2026-09-25'}}


def bh_arm_short(root, sp, L, BR, AC):
    """2026-10-02 (BH_ARM_SHORT): True when this leg is a JICBH leg of a listed dash (SPEC 'bh_short') whose hex arm would end exactly on
    the collar face (V[2] -> V[3] is the core-to-collar step at sh = M - i2 - K1) and whose collar circle crosses the hex outline there
    (hex flats radius BR < collar radius < hex corner radius AC)"""
    if L['kind'] != 'JICBH' or L['dash'] not in sp.get('bh_short', ()): return False
    assert L['dash'] in BH_ARM_SHORT_SEEN.get(root, {}), \
        f'{root} bh_short lists -{L["dash"]:02d}: add BH_ARM_SHORT_SEEN[{root!r}][{L["dash"]}] = <date of the SolidWorks run where its hex arm failed>'
    sh, rO = L['V'][3]
    return abs(L['hexl'] - sh) <= 5e-5 + 1e-12 and BR + 1e-9 < rO < AC - 1e-9      # hexl = V[2] rounded to 4 decimals


def bh_len(x):
    """a hex arm position as printed in the BH_ARM_SHORT texts: 3 decimals when exact (0.869, 0.870), else 4"""
    return f'{x:.3f}' if abs(round(x, 3) - x) < 1e-9 else f'{x:.4f}'


BRENNAN_NOTES = {   # per-part comparisons with a Brennan STEP of the same part number (Air-Way values are the ones built)
    # 2026-10-02 (new masters, tools/measure/forged.py validated by forged_validate.py): the pilot STEP of each new root vs its row (OMi values)
    '2504-08-08-FG': 'Brennan 2504-08-08-FG STEP (2026-10-02, tools/measure/forged.py): JIC tips 0.980 / 0.980 = OMi M 1 / M 2; hex arms end 0.323; A/F 0.750 = OMi; '
                     'corner puck radius 0.433; bores 0.391 / 0.391 = OMi; JIC chain = 2403 -08 (no thread relief on the STEP, modelled with it); volume 0.57131 in^3',
    '2505-08-08-FG': 'Brennan 2505-08-08-FG STEP (2026-10-02, tools/measure/forged.py): JIC tip 1.040 = OMi M 1; female face 0.940 = OMi M 2; A/F 1.062 = OMi; JIC bore '
                     '0.391 = OMi; JIC hex arm to 0.383 and chain = 2403 -08 incl. the relief; port: collar 0.260, tapered port 0.75 deep (minor 0.747 -> 0.792 dia, '
                     '45deg mouth to 0.855), drill 0.718 from the port bottom to the crossing (= TAPDRILL / PORTDEPTH of this row); volume 0.94759 in^3',
    '2606-08-08-08-FG': 'Brennan 2606-08-08-08-FG STEP (2026-10-02, tools/measure/forged.py): JIC tips 1.520 / 1.520 = OMi M 1 / L 1; female face 1.230 = OMi M 2; '
                        'A/F 1.062 = OMi; JIC bores 0.391 / 0.391 = OMi; JIC hex faces 0.863, chain = 2403 -08 (no thread relief on the STEP, modelled with it); '
                        'port: collar 0.260, tapered port 0.75 deep, drill 0.718 from the port bottom to the crossing (= TAPDRILL / PORTDEPTH of this row); volume 2.01024 in^3',
    '2611-06-06-06-FG': 'Brennan 2611-06-06-06-FG STEP (2026-10-02, tools/measure/forged.py): JIC tip 1.310 = OMi M 1; male pipe tip 1.220 = OMi M 2; female face 1.020 = '
                        'OMi L 1; A/F 0.875 = OMi; bores 0.297 (JIC) / 0.406 (male pipe) = OMi; JIC hex face 0.754, chain = 2403 -06 (no thread relief on the STEP, '
                        'modelled with it); male pipe end 0.560 = 5404 -06; port: collar 0.260, tapered port 0.58 deep, drill 0.578 from the port bottom to the run '
                        'axis (= TAPDRILL / PORTDEPTH of this row); volume 1.12766 in^3',
    # 6801: every Brennan 6801-XX-XX-NWO-FG STEP of an OMi part, compared with its Air-Way row (tools/measure/nwo_cmp.py)
    '6801-04-02-NWO-FG': 'Brennan 6801-04-02-NWO-FG STEP (2026-09-25): JIC leg 0.890, ORB leg 0.920, tip to body face 0.590, ORB thread 0.234, nut hex 0.438, body hex 0.438, undercut dia 0.250 - DIFFERS: LEG_ORB Air-Way 1.03 vs Brennan 0.92 - built to Air-Way (flag for OMi); the rest agrees with Air-Way',
    '6801-04-04-NWO-FG': 'Brennan 6801-04-04-NWO-FG STEP (2026-09-25): JIC leg 0.890, ORB leg 1.030, tip to body face 0.730, ORB thread 0.265, nut hex 0.563, body hex 0.438, undercut dia 0.364 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-05-05-NWO-FG': 'Brennan 6801-05-05-NWO-FG STEP (2026-09-25): JIC leg 0.950, ORB leg 1.130, tip to body face 0.730, ORB thread 0.265, nut hex 0.625, body hex 0.562, undercut dia 0.427 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-06-06-NWO-FG': 'Brennan 6801-06-06-NWO-FG STEP (2026-09-25): JIC leg 1.060, ORB leg 1.250, tip to body face 0.750, ORB thread 0.312, nut hex 0.688, body hex 0.562, undercut dia 0.482 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-08-08-NWO-FG': 'Brennan 6801-08-08-NWO-FG STEP (2026-09-25): JIC leg 1.250, ORB leg 1.450, tip to body face 0.860, ORB thread 0.344, nut hex 0.875, body hex 0.750, undercut dia 0.660 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-10-10-NWO-FG': 'Brennan 6801-10-10-NWO-FG STEP (2026-09-25): JIC leg 1.450, ORB leg 1.700, tip to body face 1.000, ORB thread 0.391, nut hex 1.000, body hex 0.875, undercut dia 0.773 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-12-12-NWO-FG': 'Brennan 6801-12-12-NWO-FG STEP (2026-09-25): JIC leg 1.660, ORB leg 1.940, tip to body face 1.140, ORB thread 0.410, nut hex 1.250, body hex 1.062, undercut dia 0.945 - DIFFERS: ORB_THDL Air-Way 0.469 vs Brennan 0.410 - built to Air-Way (flag for OMi); the rest agrees with Air-Way',
    '6801-20-20-NWO-FG': 'Brennan 6801-20-20-NWO-FG STEP (2026-09-25): JIC leg 2.060, ORB leg 2.250, tip to body face 1.140, ORB thread 0.469, nut hex 1.875, body hex 1.625, undercut dia 1.507 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-24-24-NWO-FG': 'Brennan 6801-24-24-NWO-FG STEP (2026-09-25): JIC leg 2.330, ORB leg 2.390, tip to body face 1.140, ORB thread 0.469, nut hex 2.125, body hex 1.875, undercut dia 1.756 - all agree with Air-Way (within its 2-decimal rounding)',
    '6801-32-32-NWO-FG': 'Brennan 6801-32-32-NWO-FG STEP (2026-09-25): JIC leg 3.060, ORB leg 2.890, tip to body face 1.140, ORB thread 0.469, nut hex 2.750, body hex 2.500, undercut dia 2.381 - all agree with Air-Way (within its 2-decimal rounding)',
    '6502-08-08-FG': 'Brennan 6502-08-08-FG STEP (2026-09-24): JIC hex arm to 0.323 and JIC tip 0.98 = model; body hex 0.75 = model; corner radius 0.433 = model; '
                     'nut face 1.28 from the crossing vs Air-Way -FG M6 1.25 (Air-Way non-FG row 1.28) - built to Air-Way; Brennan body face 0.395 = nut face - 0.885 as modelled',
    # 2026-10-02 (new master 1502): the pilot - its row values ARE this STEP (forged -FG part built from its own Brennan STEP)
    '1502-08-08-FG': 'Brennan 1502-08-08-FG STEP (2026-10-02, tools/measure/fgelbow.py + npsm.py --leg 1,1): the row values are this STEP (forged part built '
                     'from its own Brennan STEP): port face 1.230 (N3), nut face 1.520 (W3), stem tip 1.240 (M1), body hex 1.062 (corner radius 0.6131 = the '
                     '30deg puck radius), nut hex 1.000, NPSM bore 0.460, tap drill 0.718, round collar 0.26 x dia 1.062 at the port, swivel body face 0.76; '
                     'the NPSM swivel end equals NPSM_MEAS[8] (Brennan 1404-08-08) on every value; Brennan TFA catalog p21 prints the same L/M/M1/C/Y/A2 DRILL. '
                     'NOT modelled: the thread-zone minor cone and the port-mouth 45deg chamfer, the ball end of the tap drill past the crossing, the nut 30deg '
                     'face chamfer and 45deg rear hex chamfer, the nut rear undercut and the nut/body joint, 0.01 fillets, the 0.002 deep marking on the hex flats',
    # 2026-10-18 (genfeat HOSEB): Brennan TFA catalog p29 / p30 vs the Air-Way-sized 4601 / 4603 rows (they keep their Air-Way values; Brennan
    # fills only empty cells, 2026-10-18); the other cells (M, C HEX, B2 DRILL) agree within 0.011 (HOSEB DESIGN 2.5)
    '4601-06-06-NWO-FG': 'Brennan TFA catalog p29 (cross-check): L, M, C HEX and B2 DRILL agree with Air-Way within 0.011 (L4 1.81 = Brennan L within 0.002)',
    '4601-08-08-NWO-FG': 'Brennan TFA catalog p29 (cross-check): L 1.980 / Y 0.750 vs Air-Way L4 1.91 / Y 0.81 (built to Air-Way); the rest agrees within 0.011',
    '4601-10-10-NWO-FG': 'Brennan TFA catalog p29 (cross-check): L 2.055 / Y 0.875 vs Air-Way L4 1.97 / Y 0.94 (built to Air-Way); the rest agrees within 0.011',
    '4601-12-12-NWO-FG': 'Brennan TFA catalog p29 (cross-check): L 2.197 vs Air-Way L4 2.06 (built to Air-Way); the rest agrees within 0.011',
    '4601-16-12-NWO-FG': 'Brennan TFA catalog p29 (cross-check): L 2.358 / Y 1.312 vs Air-Way -FG L4 1.90 / Y 1.06 - LARGE DIFFERENCE; Air-Way\'s own '
                         'non-forged 4601-16-12 NWO row prints L4 2.06 / Y 1.13: possible Air-Way misprint - built to the -FG row per the rules, FLAG FOR THE USER / OMi; '
                         'the hose-leg bore 0.61 (Air-Way D) leaves a 0.195 wall in the -16 stub, Brennan\'s hose drill is 0.844 (Q-HOSEB-BORE)',
    '4601-32-32-NWO-FG': 'Brennan TFA catalog p30 (cross-check): Y 2.625 vs Air-Way 2.50 (built to Air-Way); hose drill 1.843 vs the Air-Way bore 1.78 '
                         'carried through the hose leg (Q-HOSEB-BORE (a)); L4 2.81 = Brennan L within 0.002',
    '4603-04-04-NWO-FG': 'Brennan TFA catalog p30 (cross-check): L 1.681 vs Air-Way L5 1.70 (built to Air-Way); the rest agrees within 0.011',
    '4603-06-06-NWO-FG': 'Brennan TFA catalog p30 (cross-check): Y 0.562 vs Air-Way CHEX 0.63 (built to Air-Way); the rest agrees within 0.011',
    '4603-08-08-NWO-FG': 'Brennan TFA catalog p30 (cross-check): L 1.625 / Y 0.812 vs Air-Way L5 1.69 / CHEX 0.75 (built to Air-Way); the rest agrees within 0.011',
    '4603-12-12-NWO-FG': 'Brennan TFA catalog p30 (cross-check): L 1.894 vs Air-Way L5 1.75 (built to Air-Way); the rest agrees within 0.011',
    # 2026-10-01 (NECK-6502): tools/measure/neck45.py (body face, neck, what stands outside the neck) + prof45.py (JIC leg)
    '6502-12-12-FG': 'Brennan 6502-12-12-FG STEP (2026-10-01, tools/measure/neck45.py + prof45.py): JIC tip 1.280 = model (Air-Way M2); JIC hex arm to 0.416 = model; '
                     'JIC bore 0.609 (Air-Way D1 0.61); body hex corner radius 0.6131 (A/F 1.062; model 1.0625 = the JIC thread major, 2603HX rule); swivel nut face '
                     '1.500 = model (Air-Way M6); swivel body face 0.412 (model 0.411 = M6 - BODYS 1.089), neck radius 0.417 = model, nut rear face 0.453 = model; '
                     'nothing outside the neck between the body face and the nut rear face = model with NECKTRIM1 / NECKFILL1 (an untrimmed corner would stand '
                     '0.038 out of the neck at the body face)',
}


def place(sp):
    return PLACE_E45 if sp.get('e45') else PLACE_ELBOW if sp.get('elbow') else PLACE


def load_review(root):
    ws = openpyxl.load_workbook(f'{REV}/DesignTable_{root}.xlsx', read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]
    out = [dict(zip(h, r)) for r in rows[2:] if r[0]]
    for sub, ren, *note in SPEC.get(root, {}).get('fold', []):
        # length variant folded into this master (one master per topology): its rows, with its column names mapped to ours
        # 2026-10-02 (FOLDS): an optional third item dict(why=..., assume=..., src=...) gives the fold's own $COMMENT text, the modelling
        # assumption it adds to each folded row's $PRP@AxialSource, and src = (generic wording, this fold's wording) pairs that build_rows
        # applies to the folded rows' generated MODEL text, warnings and check messages, which name Air-Way as the dimension source
        # (the 2501L fold keeps its text: its output is unchanged)
        note = note[0] if note else {}
        ws2 = openpyxl.load_workbook(f'{REV}/DesignTable_{sub}.xlsx', read_only=True).active
        rows2 = list(ws2.iter_rows(values_only=True)); h2 = rows2[1]
        for r2 in rows2[2:]:
            if not r2[0]: continue
            d2 = dict(zip(h2, r2)); d = {}
            for k, v in d2.items():
                d[ren.get(k, k)] = v
            d['$COMMENT'] = ' | '.join(x for x in (d2.get('$COMMENT'), note.get('why') or f'{sub} row folded into the {root} master (user decision 2026-09-25)') if x)
            if note.get('assume') and d.get('$PRP@AxialSource'): d['$PRP@AxialSource'] = d['$PRP@AxialSource'] + ' | FOLD: ' + note['assume']
            if note.get('src'): d['_FOLD_SRC'] = note['src']        # read by build_rows only (never a table column)
            out.append(d)
    return h, out


# ---------------------------------------------------------------- leg modules (vertices from the crossing outward)
def leg_JICM(i, dash, M, BR):
    e = G.JIC[dash]; rT = (e['CD'] - 2 * e['SL'] * TAN37) / 2; rC = e['CD'] / 2; rM = e['TM'] / 2
    ramp = (e['TM'] - e['CD']) / 2 / TAN60
    endlen = e['RL'] + ramp + e['TZ'] + e['LL'] + e['SL']; sh = M - endlen
    x1 = sh + e['RL']; x2 = x1 + ramp; x3 = x2 + e['TZ']; x4 = x3 + e['LL']
    V = [(0, 0), (0, BR), (sh, BR), (sh, rC), (x1, rC), (x2, rM), (x3, rM), (x3, rC), (x4, rC), (M, rT), (M, 0)]
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': round(BR, 5), f'THDMAJR_B{i}@LEG{i}': rM, f'JIC{i}_RELIEFL@LEG{i}': e['RL'],
            f'JIC{i}_THDZ@LEG{i}': e['TZ'], f'JIC{i}_CONER@LEG{i}': rC, f'JIC{i}_LANDL@LEG{i}': e['LL'], f'JIC{i}_SEATL@LEG{i}': e['SL'],
            f'RELIEFANG{i}@LEG{i}': 60, f'SEATB{i}@LEG{i}': 37}
    pitch = 1 / G.tpi_of(e['thr'])
    tcols = {f'THDDIA@THD_End{i}': e['TM'], f'THDPITCH@THD_End{i}': round(pitch, 5), f'DEPTH@THD_End{i}': e['TZ'],
             f'Profile_Height@THD_End{i}_PROF': round(0.54127 * pitch, 5), f'Profile_Land@THD_End{i}_PROF': round(0.25 * pitch, 5), f'THDPITCH@THD_End{i}_PROF': round(pitch, 5)}
    dims = [('len', -1, f'M{i}', M, M / 2, BR + 0.6), ('rad', 1, 'BODYR', BR, sh / 2, -0.4), ('rad', 5, f'THDMAJR_B{i}', rM, (x2 + x3) / 2, -0.3),
            ('len', 3, f'JIC{i}_RELIEFL', e['RL'], (sh + x1) / 2, BR + 0.25), ('ang', 4, 5, f'RELIEFANG{i}', 60, x1 - 0.06, BR + 0.1),
            ('len', 5, f'JIC{i}_THDZ', e['TZ'], (x2 + x3) / 2, BR + 0.35), ('rad', 7, f'JIC{i}_CONER', rC, (x3 + x4) / 2, -0.2),
            ('len', 7, f'JIC{i}_LANDL', e['LL'], (x3 + x4) / 2, BR + 0.15), ('ptl', 8, 'False', 9, f'JIC{i}_SEATL', e['SL'], (x4 + M) / 2, BR + 0.45),
            ('ang', 8, 10, f'SEATB{i}', 37, x4 - 0.05, -0.15), ('col', 3, 7)]
    return dict(kind='JICM', dash=dash, V=V, endlen=endlen, cols=cols, tcols=tcols, dims=dims, rmax=max(rM, rC),
                thr=e['thr'], thread=dict(type='CUT', ex=x2, er=rM, depth=e['TZ'], size=f"{e['TM']:.4f}-{G.tpi_of(e['thr']):g}", pitch=pitch),
                tipR=rT)


def leg_JICBH(i, dash, M, BR, i2, K1, O):
    # JIC BULKHEAD leg of a forged elbow/tee (Brennan 2701-08-08-FG STEP): hex arm -> round collar dia O (Air-Way) ->
    # JIC bulkhead end whose relief-to-tip length is Air-Way i2 (2.11 - 0.86 = 1.25 on the STEP = i2) with the JIC thread
    # run from the relief to the land. K1 is read as the collar thickness (ASSUMPTION - the STEP collar is 0.125 thick and
    # is followed by a 0.125 round shank that is not modelled).
    e = G.JIC[dash]; rT = (e["CD"] - 2 * e["SL"] * TAN37) / 2; rC = e["CD"] / 2; rM = e["TM"] / 2; rO = O / 2
    ramp = (e['TM'] - e['CD']) / 2 / TAN60
    tz = round(i2 - (e['SL'] + e['LL'] + ramp + e['RL']), 4)
    assert tz > e['TZ'], (dash, i2, tz)
    sh = M - i2 - K1; c1 = sh + K1
    x1 = c1 + e['RL']; x2 = x1 + ramp; x3 = x2 + tz; x4 = x3 + e['LL']
    # 2026-09-25: the revolved leg core under the hex arm is drawn 0.02 inside the hex flats radius. It is hidden inside the hex
    # prism (inscribed radius BR), so the solid is unchanged, but the collar step (core -> collar dia O) never has zero height:
    # Air-Way prints O equal to the hex flats at -06/-10/-12 (2701), which a core AT the flats radius could not model.
    BRc = round(BR - 0.02, 5)
    assert abs(rO - BRc) > 0.003, ('collar radius equals the leg core radius', rO, BRc)
    V = [(0, 0), (0, BRc), (sh, BRc), (sh, rO), (c1, rO), (c1, rC), (x1, rC), (x2, rM), (x3, rM), (x3, rC), (x4, rC), (M, rT), (M, 0)]
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': BRc, f'COLLARR{i}@LEG{i}': round(rO, 5), f'COLLARL{i}@LEG{i}': K1,
            f'THDMAJR_B{i}@LEG{i}': rM, f'JIC{i}_RELIEFL@LEG{i}': e['RL'], f'JIC{i}_THDZ@LEG{i}': tz, f'JIC{i}_CONER@LEG{i}': rC,
            f'JIC{i}_LANDL@LEG{i}': e['LL'], f'JIC{i}_SEATL@LEG{i}': e['SL'], f'RELIEFANG{i}@LEG{i}': 60, f'SEATB{i}@LEG{i}': 37}
    pitch = 1 / G.tpi_of(e['thr'])
    tcols = {f'THDDIA@THD_End{i}': e['TM'], f'THDPITCH@THD_End{i}': round(pitch, 5), f'DEPTH@THD_End{i}': tz,
             f'Profile_Height@THD_End{i}_PROF': round(0.54127 * pitch, 5), f'Profile_Land@THD_End{i}_PROF': round(0.25 * pitch, 5), f'THDPITCH@THD_End{i}_PROF': round(pitch, 5)}
    top = max(BR, rO)
    dims = [('len', -1, f'M{i}', M, M / 2, top + 0.6), ('rad', 1, 'BODYR', BRc, sh / 2, -0.4), ('rad', 3, f'COLLARR{i}', rO, sh + K1 / 2, -0.5),
            ('len', 3, f'COLLARL{i}', K1, sh + K1 / 2, top + 0.2), ('len', 5, f'JIC{i}_RELIEFL', e['RL'], (c1 + x1) / 2, top + 0.25),
            ('ang', 6, 7, f'RELIEFANG{i}', 60, x1 - 0.06, top + 0.1), ('rad', 7, f'THDMAJR_B{i}', rM, (x2 + x3) / 2, -0.3),
            ('len', 7, f'JIC{i}_THDZ', tz, (x2 + x3) / 2, top + 0.35), ('rad', 9, f'JIC{i}_CONER', rC, (x3 + x4) / 2, -0.2),
            ('len', 9, f'JIC{i}_LANDL', e['LL'], (x3 + x4) / 2, top + 0.15), ('ptl', 10, 'False', 11, f'JIC{i}_SEATL', e['SL'], (x4 + M) / 2, top + 0.45),
            ('ang', 10, 12, f'SEATB{i}', 37, x4 - 0.05, -0.15), ('col', 5, 9)]
    return dict(kind='JICBH', dash=dash, V=V, endlen=i2 + K1, cols=cols, tcols=tcols, dims=dims, rmax=max(rM, rC, rO),
                thr=e['thr'], thread=dict(type='CUT', ex=x2, er=rM, depth=tz, size=f"{e['TM']:.4f}-{G.tpi_of(e['thr']):g}", pitch=pitch),
                tipR=rT)


# 2026-10-18 (genfeat flange, Q-NEW-FLG61LEG / Q-NEW-FLG62LEG): FLANGE LEG of a forged elbow. The head is the end library's: code 61 =
# gen_straight2 end_FLG61 / FLG61_MEAS (Brennan 1700 STEPs, the accepted 1700 master), code 62 = end_FLG62 / FLG62_MEAS (Brennan 1800-08-08 /
# 1824-08 / 1804-08-08-FG STEPs). Head OD by flange size (FLG61_O): the code 61 head OD as built in the 1700 master (DesignTable_1700 column O,
# Air-Way s61; one value per flange size - -24 is printed 2.38 on 1700-61-24-24 and 2.37 on 1700-61-20-24, both 2.375 rounded: 2.38, rounding-
# only, Q-FLG61-O24; the Brennan 1700 STEPs read 1.188 / 1.5 / 1.75 / 2.0 / 2.375 / 2.812); code 62: FLG62_MEAS O. The forged hex arm runs from
# the crossing to the head back face (as the 1700 decision 2026-09-24); the Brennan round neck between hex arm and head is NOT modelled (Q-FLG61-NECK).
FLG_KINDS = ('FLG61', 'FLG62')
FLG61_O = {8: 1.19, 12: 1.50, 16: 1.75, 20: 2.00, 24: 2.38, 32: 2.81}
FLG_O_ROUND = 0.0101        # |row O - library| up to two 2-decimal roundings of the same value (2.375 -> 2.37 / 2.38) = rounding, noted; above: conflict
FLGLEG_ASSUME = {
    'FLG61': ('code 61 flange leg (Q-NEW-FLG61LEG, user 2026-10-08): the SAE code 61 head of the 1700 end library on the axis-aligned leg 1 - head '
              'thickness and face O-ring groove by flange size = FLG61_MEAS (Brennan 1700-08/-12/-16/-20/-24/-32 STEPs, tools/measure/flange.py), head '
              'OD by flange size = the 1700 master value (FLG61_O: DesignTable_1700 column O, Air-Way s61; -24 = 2.38, the 2.375 printed 2.37 / 2.38 - '
              'rounding only; Brennan 1700 STEPs agree; Q-TRANSFER-ENDLIB 2026-10-08); the Brennan 1703-24-24-FG / 1704-24-24-FG STEPs carry the same '
              '-24 head'),
    'FLG62': ('code 62 flange leg (Q-NEW-FLG62LEG, user 2026-10-18 A17): the SAE code 62 head of the 1800 end library on the axis-aligned leg 1 - head '
              'OD, thickness and face O-ring groove = FLG62_MEAS (Brennan 1800-08-08 / 1824-08 / 1804-08-08-FG STEPs, tools/measure/flange62.py, agree to '
              '0.0002); measured for flange size -08 only (another size needs a code 62 head STEP)')}
FLGLEG_SHAPE = ('forged hex arm from the crossing to the head back face (as the 1700 decision 2026-09-24): the Brennan elbow STEPs instead end the hex '
                'arm near the crossing and carry a round neck (between the hex flats and corners) up to the head - NOT modelled (Q-FLG61-NECK); the '
                'groove inner-wall draft, the bore chamfer at the face, head edge chamfers and the hex-end chamfers NOT modelled; the flange-leg bore '
                'is the row DFLG (own STEP), the JIC-leg bore the row D; single manufacturer (Brennan) head geometry -> ASSUMED at most')


def flg_o(kind, dash):
    # head OD of a flange leg from the end library (KeyError names what is missing)
    if kind == 'FLG62': return G.flg62_head(dash)['O']
    if dash not in G.FLG61_MEAS or dash not in FLG61_O:
        raise KeyError(f'code 61 flange head not measured for -{dash:02d}: needs a FLG61_MEAS[{dash}] entry (head thickness, face groove) measured with '
                       f'tools/measure/flange.py on a Brennan STEP with a -{dash:02d} code 61 head, and its head OD (FLG61_O)')
    return FLG61_O[dash]


def leg_FLG(i, kind, dash, M, BR, O):
    """flange leg i (from the crossing): leg core 0.02 inside the hex flats (the JICBH convention: hidden in the hex prism, and the core-to-head
    step never has zero height) to the head back face sh = M - TH, the head (radius O/2) to the face at M, the face O-ring groove, the inner face
    disc down to the axis. = the end module's own profile (G.end_FLG61 / G.end_FLG62, face coordinates) turned into leg coordinates."""
    E = G.end_FLG61(dash, str(i), O) if kind == 'FLG61' else G.end_FLG62(dash, str(i))
    m = E['m']; TH, GI, GO, GD = m['TH'], m['GI'], m['GO'], m['GD']; rO = E['rO']
    BRc = round(BR - 0.02, 5)
    VH = [(M - x, r) for (x, r) in reversed(E['V'])]             # head back (sh, rO) -> face ring -> groove -> inner face disc (M, GI)
    sh = VH[0][0]                                                 # = M - TH, exactly the head back face of the profile (not rounded)
    V = [(0, 0), (0, BRc), (sh, BRc)] + VH + [(M, 0)]
    assert len(V) == 10 and abs(VH[0][1] - rO) < 1e-12 and abs(sh - (M - TH)) < 1e-12, V
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': BRc}
    for k_, v_ in E['cols'].items(): cols[k_.replace('@DRIVE', f'@LEG{i}')] = v_
    top = max(BR, rO)
    dims = [('len', -1, f'M{i}', M, M / 2, top + 0.6), ('rad', 1, 'BODYR', BRc, sh / 2, -0.4),
            ('rad', 3, f'FLG{i}_HEADR', rO, (sh + M) / 2, -0.35), ('len', 3, f'FLG{i}_HEADT', TH, (sh + M) / 2, top + 0.3),
            ('rad', 5, f'FLG{i}_GRVOR', GO, M - GD / 2, -0.25), ('rad', 7, f'FLG{i}_GRVIR', GI, M - GD / 2, -0.15),
            ('len', 7, f'FLG{i}_GRVD', GD, M - GD / 2, top + 0.45), ('col', 4, 8)]
    return dict(kind=kind, dash=dash, V=V, endlen=TH, cols=cols, tcols={}, dims=dims, rmax=rO, thr=E['thr'], thread=None, tipR=GI, m=m, rO=rO, BRc=BRc)


def flg_leg_checks(i, L, BR, AC):
    """2026-10-18: geometry gates of a flange leg (DESIGN 4.5 + review fixes 2 / 4): (checks, warnings)"""
    c, w = [], []; sh = L['hexl']; rO = L['rO']; GI = L['m']['GI']; b = L['bore']
    if sh < 0.03: c.append(f'leg {i}: flange leg {L["V"][-1][0]} leaves no hex arm ({sh:.3f}) behind the head (thickness {L["endlen"]})')
    if b is None: c.append(f'leg {i}: no bore')
    else:
        if GI - b / 2 < 0.03: c.append(f'leg {i}: bore {b} leaves {GI - b / 2:.3f} (< 0.03) face land inside the flange O-ring groove (groove inner dia {2 * GI:.3f})')
        if BR - b / 2 < 0.03: c.append(f'leg {i}: bore {b} leaves < 0.03 wall under the hex flats ({2 * BR:.4f})')
    if abs(rO - L['BRc']) < 0.003: c.append(f'leg {i}: flange head radius {rO:.4f} equals the leg core radius {L["BRc"]:.4f} (zero-height head back face)')
    if abs(rO - AC) < 0.003: c.append(f'leg {i}: flange head radius {rO:.4f} equals the hex corner radius {AC:.4f} (tangent head / hex outline)')
    if AC + 0.03 > sh: c.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches within 0.03 of the flange head back face ({sh:.3f})')
    if BR + 1e-9 < rO < AC - 1e-9:
        w.append(f'leg {i}: hex arm ends on the flange head back face with the head circle (radius {rO:.4f}) between the hex flats {BR:.4f} and corners '
                 f'{AC:.4f} - the 2702 -16 situation (crossing outlines on a coplanar union; builds at 2702 -10 / -12, 2703 -12, 2704 -10 / -12 / -16); '
                 f'SolidWorks decides (Q-FLG61-SHORT)')
    elif rO <= BR: w.append(f'leg {i}: the hex arm stands proud of the flange head (head radius {rO:.4f} <= hex flats {BR:.4f})')
    return c, w


# 2026-09-25 (batch 13b): ADJUSTABLE ORB stud end ("NWO": nut, washer, O-ring), measured with tools/measure/nwo.py on the Brennan
# 6801-XX-XX-NWO-FG STEPs (one per ORB size, user download 2026-09-25; -14 from the earlier bundle). From the body face outward: neck
# (radius NECKR, length NECKL), locknut (hex, thickness NUTT), backup washer (radius WR, thickness WT), O-ring undercut, ORB thread.
# Air-Way agrees on every size: tip-to-body-face ORB_I3 (0.59 ... 1.14) = Brennan, nut hex HEXB = Brennan, thread and undercut root.
# Brennan's thread length THDL differs from Air-Way only at -12 (0.410 vs 0.469) - the model follows Air-Way (THDL, undercut root).
NWO_MEAS = {
    2:  dict(NECKR=0.1752, NECKL=0.011, NUTT=0.22, WR=0.252, WT=0.03, UL_B=0.095, THDL_B=0.234, I3_B=0.59, AF_B=0.4375),
    4:  dict(NECKR=0.2252, NECKL=0.029, NUTT=0.28, WR=0.325, WT=0.035, UL_B=0.121, THDL_B=0.265, I3_B=0.73, AF_B=0.5625),
    5:  dict(NECKR=0.25, NECKL=0.029, NUTT=0.28, WR=0.361, WT=0.035, UL_B=0.121, THDL_B=0.265, I3_B=0.73, AF_B=0.625),
    6:  dict(NECKR=0.2752, NECKL=0.012, NUTT=0.27, WR=0.397, WT=0.035, UL_B=0.121, THDL_B=0.312, I3_B=0.75, AF_B=0.6875),
    8:  dict(NECKR=0.35, NECKL=0.019, NUTT=0.31, WR=0.505, WT=0.041, UL_B=0.146, THDL_B=0.344, I3_B=0.86, AF_B=0.875),
    10: dict(NECKR=0.40, NECKL=0.030, NUTT=0.36, WR=0.5775, WT=0.05, UL_B=0.169, THDL_B=0.391, I3_B=1.00, AF_B=1.0),
    12: dict(NECKR=0.50, NECKL=0.027, NUTT=0.41, WR=0.722, WT=0.05, UL_B=0.243, THDL_B=0.410, I3_B=1.14, AF_B=1.25),
    14: dict(NECKR=0.55, NECKL=0.027, NUTT=0.41, WR=0.7945, WT=0.05, UL_B=0.184, THDL_B=0.469, I3_B=1.14, AF_B=1.375),
    16: dict(NECKR=0.60, NECKL=0.027, NUTT=0.41, WR=0.866, WT=0.05, UL_B=0.184, THDL_B=0.469, I3_B=1.14, AF_B=1.5),
    20: dict(NECKR=0.75, NECKL=0.027, NUTT=0.41, WR=1.0825, WT=0.05, UL_B=0.184, THDL_B=0.469, I3_B=1.14, AF_B=1.875),
    24: dict(NECKR=0.85, NECKL=0.027, NUTT=0.41, WR=1.227, WT=0.05, UL_B=0.184, THDL_B=0.469, I3_B=1.14, AF_B=2.125),
    32: dict(NECKR=1.10, NECKL=0.027, NUTT=0.41, WR=1.58, WT=0.05, UL_B=0.184, THDL_B=0.469, I3_B=1.14, AF_B=2.75),
}
# 2026-09-25: the locknut CHAMFERS, measured on all 12 STEPs (tools/measure/nwo_chamfer.py, section through the hex corners): both nut
# faces carry a cone 15.0 deg (+-0.06) to the face plane, starting at the across-flats circle (radius AF/2 +-0.0003) and running out at the
# hex corners. Modelled as Brennan draws it: the nut is a revolved envelope (face -> 15deg cone -> corner cylinder -> 15deg cone -> face)
# cut to the hexagon. Two modelling offsets keep SolidWorks away from tangent geometry (the finished solid is unchanged by NWO_RN_MARGIN;
# NWO_CH_DR shifts the chamfer start 0.005 outward, a cosmetic difference):
NWO_CHANG = 15.0          # chamfer cone to the nut face plane, deg (MEASURED, every size)
NWO_CH_DR = 0.005         # chamfer start radius = AF/2 + 0.005 (Brennan: exactly AF/2 - tangent to the flats; ASSUMPTION, cosmetic)
NWO_RN_MARGIN = 0.010     # revolved nut envelope radius = hex corner radius + 0.010, removed by the hex cut (no effect on the solid)
NWO_ASSUME = ('adjustable ORB stud end (nut, washer, O-ring) - Brennan 6801-XX-XX-NWO-FG STEPs, one per ORB size -02..-32: from the body face '
              '(Air-Way LEG minus ORB_I3, = Brennan on every STEP) a round neck, the locknut (hex = Air-Way HEXB = Brennan, measured thickness, both faces '
              'chamfered 15deg to the face from the across-flats circle as MEASURED on all 12 STEPs - drawn as a revolved envelope cut to the hexagon, flats normal to Z; '
              'chamfer start drawn 0.005 outside the flats circle to avoid a tangent edge: ASSUMPTION, cosmetic), the backup washer (measured OD and thickness), the O-ring '
              'undercut (root = Air-Way groove dia = Brennan) and the male ORB thread (Air-Way thread length, Thread feature); locknut, washer and O-ring are one solid '
              'with the body, as on the Brennan STEPs (O-ring not drawn); the nut sits where Brennan shows it (backed off against the washer); no tip chamfer (as on the '
              'fixed ORB ends)')


def nwo_radial(lg):
    """largest distance from its own axis of an adjustable ORB leg outside the body hex (washer or nut corners)"""
    return max(lg['m']['WR'], lg['nut']['af'] / math.sqrt(3))


_I3_CACHE = {}
def nwo_i3_from(src, dash):
    """tip-to-body-face of the adjustable ORB end, from another Air-Way series of the same maker (6801): every row of that table with this
    ORB size must print the same value (all Air-Way rows, OMi scope does not matter for a dimension) - and it must equal the Brennan STEP"""
    if src not in _I3_CACHE:
        ws = openpyxl.load_workbook(f'{REV}/DesignTable_{src}.xlsx', read_only=True).active
        rows = list(ws.iter_rows(values_only=True)); h = rows[1]; m = {}
        for r in rows[2:]:
            if not r[0]: continue
            d = dict(zip(h, r)); dd = dashes(d['$PRP@PartNo'])
            if len(dd) == 2 and d.get('ORB_I3@DRIVE') is not None: m.setdefault(dd[1], set()).add(d['ORB_I3@DRIVE'])
        _I3_CACHE[src] = m
    v = _I3_CACHE[src].get(dash)
    if not v or len(v) != 1: raise KeyError(f'no single Air-Way {src} ORB_I3 for -{dash:02d}: {v}')
    i3 = v.pop(); _I3_CACHE[src][dash] = {i3}
    if abs(i3 - NWO_MEAS[dash]['I3_B']) > 0.006: raise KeyError(f'Air-Way {src} ORB_I3 {i3} for -{dash:02d} differs from the Brennan 6801 STEP {NWO_MEAS[dash]["I3_B"]}')
    return i3


# ---------------------------------------------------------------- 2026-10-09 wave 2, HOSEB: beaded hose-barb leg + face-off of the forged corner
HOSE_WALL_MIN = 0.015     # hose stub wall (stub OD - bore) / 2 below this -> BLOCKED; 0.015 .. 0.03 -> warning (the built 4404-04-04 master has 0.020)
FACEOFF_DELTA = 0.05      # the face-off runs this far past the forged corner radius (the stub ring it takes is put back); also its region margin
FACEOFF_GAP = 0.02        # clearances of the face-off: cut end vs bead start, region bounds vs the corner material / the other leg's end
FACEOFF_ROUT_K = 1.5      # 45 deg elbow: outer radius of the face-off ring = this x the hex corner radius (as NECKTRIM, TRIM_ROUT_K)
HOSEB_ASSUME = ('beaded hose-barb leg (Q-NEW-HOSEB, port of the straight 4404 / 4604 end): stub OD = the row\'s TubeOD (hose size), bead dia = the row\'s AA '
                '(sources: the row\'s own AxialSource); stub 1.500 from the hose-leg hex face to the tip, bead centre 0.251 from the tip and bead chord width from the bead section radius '
                '0.060 - the hose end library (Brennan 4404-08-06 STEP; Q-TRANSFER-ENDLIB), the same on the Brennan 4404-16-16, 4501-08-08-FG, 4503-08-08-FG and '
                '4603-16-16-NWO-FG STEPs (4601-08-06-NWO-FG: stub 1.530) - shape only; the forged hex arm of the hose leg = the row\'s hose leg length minus the stub; the round '
                'bead section is modelled as a flat-topped ring of the same chord width; plain hose tip, no thread on the hose leg; bores flat to the crossing '
                '(Brennan: ball-ended drills)')
FACEOFF_ASSUME = ('FORGED CORNER FACED OFF AT THE HOSE HEX FACE (Q-NEW-HOSEB, features HOSEFACE / STUBFILL): nothing of the forged corner (30deg puck, the other '
                  "leg's hex arm) stands past the hose-leg hex face outside the hose stub - as on the Brennan 4503-08-08-FG and 4603-16-16-NWO-FG forgings (hose "
                  'hex face a complete hexagon inside the corner radius, nothing beyond it) and the Brennan 6500-05-05-FG elbow (corner faced off at the body '
                  'face), shape only; modelled as a cut of the region past the hose hex face (90 deg: a rectangle along the other leg up to its hex arm end; '
                  '45 deg: a ring to 1.5 x the hex corner radius) to 0.05 beyond the corner radius, then the stub ring put back (STUBFILL) - in every '
                  'configuration, no change where the corner clears the face; the 0.05 overrun and the region bounds are construction margins, not part '
                  'dimensions (ASSUMPTION for these forgings: no 90 deg hose elbow whose hose hex arm ends inside the corner radius has been seen)')


# END-LIBRARY tokens of the adjustable-ORB end of a HOSEB root (Q-TRANSFER-ENDLIB = yes, user 2026-10-08 "reuse end details - yes"); the same values
# and texts as the PERLEGSW end_val (wave2_impl_20261009), so a later merge of PERLEGSW reads the same SPEC tuple unchanged
HOSEB_ENDLIB = {
    '=ORB:THDL': ('THDL', 'adjustable ORB thread length', 'the ORB end library (6401 / 6405 / 6410 tables; = Air-Way 6801 ORB_THDL at every dash -02..-32)'),
    '=ORB:GD': ('GD', 'adjustable ORB undercut dia', 'the ORB end library (6401 / 6405 / 6410 tables; = Air-Way 6801 ORB_GRVDIA at every dash -02..-32)'),
}


def hoseb_endlib(sp, r, dd, warn, chk):
    """a HOSEB root's row with the end-library tokens of its SPEC nwo tuple filled in as virtual keys of a COPY of the row (the leg modules read
    r[sp['nwo'][k]]); a dash missing from the library is a check failure; the source of every value goes into the warnings ($COMMENT)"""
    r = dict(r)
    for i, ((kind, lc, bc, tc), d) in enumerate(zip(legs4(sp), dd), 1):
        if kind != 'NWO': continue
        for c in sp['nwo']:
            if c not in HOSEB_ENDLIB: continue
            key, what, src = HOSEB_ENDLIB[c]
            if d not in G.ORB or G.ORB[d].get(key) is None: chk.append(f'leg {i}: no -{d:02d} entry in the ORB end library for {what}'); continue
            r[c] = G.ORB[d][key]
            warn.append(f'leg {i}: {what} {r[c]} = {src} for -{d:02d} (end library, Q-TRANSFER-ENDLIB 2026-10-08)')
    return r


def hose_bore_lib(dash):
    """'=4404' (Q-HOSEB-BORE option b, ONLY after the user picks it): the Air-Way 4404 through bore D3 of the equal-size row 4404-dd-dd"""
    ws = openpyxl.load_workbook(f'{REV}/DesignTable_4404.xlsx', read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]
    for r in rows[2:]:
        if not r[0]: continue
        d = dict(zip(h, r)); dd = dashes(str(d['$PRP@PartNo']))
        if dd == [dash, dash] and d.get('D3@BORE') is not None: return d['D3@BORE']
    raise KeyError(f'no Air-Way 4404-{dash:02d}-{dash:02d} through bore')


def leg_HOSEB(i, dash, L, BR, stubOD, bead):
    """beaded hose leg from the crossing: hex core to the hose hex face, stub (tail), bead (flat-topped ring), stub nose, plain tip face"""
    E = G.end_HOSEB(str(i), stubOD, bead)
    rS, rA, p1, p2, w = E['rS'], E['rA'], E['p1'], E['p2'], E['w']
    sh = round(L - E['endlen'], 4); b0 = round(L - p2, 4); b1 = round(L - p1, 4)
    V = [(0, 0), (0, BR), (sh, BR), (sh, rS), (b0, rS), (b0, rA), (b1, rA), (b1, rS), (L, rS), (L, 0)]
    cols = {f'M{i}@LEG{i}': L, f'BODYR@LEG{i}': round(BR, 5), f'HOSE{i}_TAILL@LEG{i}': round(b0 - sh, 4), f'HOSE{i}_BEADR@LEG{i}': round(rA, 5),
            f'HOSE{i}_BEADW@LEG{i}': w, f'HOSE{i}_STUBR@LEG{i}': round(rS, 5), f'HOSE{i}_BEADPOS@LEG{i}': p1}
    top = max(BR, rA)
    dims = [('len', -1, f'M{i}', L, L / 2, top + 0.6), ('rad', 1, 'BODYR', BR, sh / 2, -0.4),
            ('len', 3, f'HOSE{i}_TAILL', round(b0 - sh, 4), (sh + b0) / 2, top + 0.15), ('rad', 5, f'HOSE{i}_BEADR', rA, (b0 + b1) / 2, -0.35),
            ('len', 5, f'HOSE{i}_BEADW', w, (b0 + b1) / 2, top + 0.35), ('rad', 7, f'HOSE{i}_STUBR', rS, (b1 + L) / 2, -0.25),
            ('len', 7, f'HOSE{i}_BEADPOS', p1, (b1 + L) / 2, top + 0.25), ('col', 3, 7)]
    return dict(kind='HOSEB', dash=dash, V=V, endlen=E['endlen'], cols=cols, tcols={}, dims=dims, rmax=max(rA, rS), rS=rS, rA=rA,
                bead=(b0, b1), thr=E['thr'], thread=None, tipR=rS)


def leg_axes(sp, n):
    """unit vector (XY plane) of every leg axis, in leg order"""
    out = []
    for i in range(1, n + 1):
        ax, sg = place(sp)[i]
        out.append((UXV, UYV) if ax == 'U' else (float(sg), 0.0) if ax == 0 else (0.0, float(sg)))
    return out


def faceoff_geo(sp, legs, ih, BR, AC, N=60):
    """the forged corner past the hose hex face of leg ih (0-based), sampled exactly as the design check (HOSEB/scripts/faceoff_geo.py):
    the 30deg corner puck (cone surface + interior), the other leg's hex arm outline from the crossing to its hexl, and the other leg's END
    (its revolved profile beyond its hex arm, plus the adjustable-ORB locknut envelope) inside the slab [hexl, max(AC, hexl) + DELTA]. Points
    past the hex face (along the hose axis) and outside the stub radius are the material the face-off must take."""
    U = leg_axes(sp, len(legs)); H = legs[ih]; u = U[ih]; n = (-u[1], u[0]); s = H['hexl']; rS = H['rS']
    io = 1 - ih; O = legs[io]; uo = U[io]; no = (-uo[1], uo[0]); pts = []; T30_ = math.tan(math.radians(30))
    def keep(x, y, z, tag):
        a = x * u[0] + y * u[1]
        if a <= s + 1e-9: return
        t_ = x * n[0] + y * n[1]; r = math.hypot(t_, z)
        if r <= rS + 1e-9: return
        pts.append((tag, a, r, x * uo[0] + y * uo[1]))
    for k in range(N + 1):
        z = -BR + 2 * BR * k / N; R = AC - abs(z) * T30_
        for j in range(360):
            th = 2 * math.pi * j / 360; c_, s_ = math.cos(th), math.sin(th)
            for f_ in (1.0, 0.8, 0.6): keep(f_ * R * c_, f_ * R * s_, z, 'puck')
    hexv = [(AC, 0.0), (AC / 2, BR), (-AC / 2, BR), (-AC, 0.0), (-AC / 2, -BR), (AC / 2, -BR)]
    for k in range(N + 1):
        ao = O['hexl'] * k / N
        for j in range(6):
            (p1, z1), (p2, z2) = hexv[j], hexv[(j + 1) % 6]
            for q in range(25):
                p_ = p1 + (p2 - p1) * q / 24; z = z1 + (z2 - z1) * q / 24
                keep(ao * uo[0] + p_ * no[0], ao * uo[1] + p_ * no[1], z, 'other hex arm')
    endpts = []; amax = max(AC, s) + FACEOFF_DELTA
    def endpt(ao, ro, ph):
        p_ = ro * math.cos(ph); z = ro * math.sin(ph); x = ao * uo[0] + p_ * no[0]; y = ao * uo[1] + p_ * no[1]; a = x * u[0] + y * u[1]
        if s - 1e-9 <= a <= amax: endpts.append((math.hypot(x * n[0] + y * n[1], z), ao))
    for (a1, r1), (a2, r2) in zip(O['V'], O['V'][1:]):
        for k in range(41):
            ao = a1 + (a2 - a1) * k / 40; ro = r1 + (r2 - r1) * k / 40
            if ao <= O['hexl'] + 1e-9: continue
            for j in range(72): endpt(ao, ro, 2 * math.pi * j / 72)
    if O['kind'] == 'NWO':
        for ao in (O['nut']['n0'], O['nut']['w0']):
            for j in range(72): endpt(ao, O['nut']['Rn'], 2 * math.pi * j / 72)
    r = dict(past=bool(pts))
    if pts:
        r.update(past_max_r=max(p_[2] for p_ in pts), past_max_a=max(p_[1] for p_ in pts), past_max_along_other=max(p_[3] for p_ in pts),
                 past_by=sorted({p_[0] for p_ in pts}))
    if endpts: r.update(end_min_r=min(e[0] for e in endpts), end_min_along_other=min(e[1] for e in endpts))
    return r


_NWOCOL_CACHE = {}
def nwo_col_from(src, col, dash):
    """2026-10-18 (ANGLED): an adjustable-ORB end cell (thread length / groove dia) from another Air-Way series of the same maker (6801), as
    nwo_i3_from: every row of that table with this ORB size must print one single value (all Air-Way rows; OMi scope does not matter)"""
    if (src, col) not in _NWOCOL_CACHE:
        ws = openpyxl.load_workbook(f'{REV}/DesignTable_{src}.xlsx', read_only=True).active
        rows = list(ws.iter_rows(values_only=True)); h = rows[1]; m = {}
        for r in rows[2:]:
            if not r[0]: continue
            d = dict(zip(h, r)); dd = dashes(d['$PRP@PartNo'])
            if len(dd) == 2 and d.get(col) is not None: m.setdefault(dd[1], set()).add(d[col])
        _NWOCOL_CACHE[(src, col)] = m
    v = _NWOCOL_CACHE[(src, col)].get(dash)
    if not v or len(v) != 1: raise KeyError(f'no single Air-Way {src} {col} for -{dash:02d}: {v}')
    return next(iter(v))


def leg_NWO(i, dash, LEG, BR, I3, nutAF, THDL, GRVD):
    """adjustable ORB leg (a from the crossing): body hex arm to the body face, neck, locknut envelope with its two 15deg chamfer
    cones (cut to the hexagon later: NUTCUTi), washer, O-ring undercut, male ORB thread to the tip"""
    m = NWO_MEAS[dash]; e = G.JIC[dash]; rM = e['TM'] / 2; UR = GRVD / 2
    sh = round(LEG - I3, 4); n0 = round(sh + m['NECKL'], 4); w0 = round(n0 + m['NUTT'], 4); w1 = round(w0 + m['WT'], 4); te = round(LEG - THDL, 4)
    rc = round(nutAF / 2 + NWO_CH_DR, 5); Rn = round(nutAF / math.sqrt(3) + NWO_RN_MARGIN, 5)
    chA = 90.0 - NWO_CHANG                                  # sketch angle between each chamfer cone and the envelope line
    ch = (Rn - rc) * math.tan(math.radians(NWO_CHANG))      # axial run of each cone
    if abs(nutAF - m['AF_B']) > 0.007: raise AssertionError(f'Air-Way locknut hex {nutAF} differs from the Brennan nut {m["AF_B"]} for -{dash:02d}')
    if te - w1 < 0.03: raise AssertionError(f'no room for the O-ring undercut ({te - w1:.3f}) between the washer and the thread')
    if not (m['NECKR'] < nutAF / 2 - 0.01 and m['WR'] > rc + 0.005 and m['WR'] > UR + 0.02 and m['WR'] > rM + 0.02 and UR < rM - 0.005):
        raise AssertionError('radial order neck < nut flats < washer, undercut < thread < washer')
    if abs(m['NECKR'] - BR) < 0.003: raise AssertionError(f'neck radius {m["NECKR"]} equals the body hex flats radius {BR:.4f} (zero-height body face)')
    if m['NUTT'] < 2 * ch + 0.05: raise AssertionError(f'nut {m["NUTT"]} too thin for its two chamfers ({2 * ch:.3f})')
    V = [(0, 0), (0, BR), (sh, BR), (sh, m['NECKR']), (n0, m['NECKR']), (n0, rc), (n0 + ch, Rn), (w0 - ch, Rn), (w0, rc), (w0, m['WR']), (w1, m['WR']),
         (w1, UR), (te, UR), (te, rM), (LEG, rM), (LEG, 0)]
    AX = len(V) - 1
    cols = {f'M{i}@LEG{i}': LEG, f'BODYR@LEG{i}': round(BR, 5), f'NW{i}_BODYL@LEG{i}': sh, f'NW{i}_NECKR@LEG{i}': m['NECKR'], f'NW{i}_NECKL@LEG{i}': m['NECKL'],
            f'NW{i}_CHR@LEG{i}': rc, f'NW{i}_CHANG1@LEG{i}': chA, f'NW{i}_NUTR@LEG{i}': Rn, f'NW{i}_CHANG2@LEG{i}': chA, f'NW{i}_NUTT@LEG{i}': m['NUTT'],
            f'NW{i}_CHR2@LEG{i}': rc, f'NW{i}_WASHR@LEG{i}': m['WR'], f'NW{i}_WASHT@LEG{i}': m['WT'], f'NW{i}_UCR@LEG{i}': round(UR, 5),
            f'THDMAJR_B{i}@LEG{i}': rM, f'NW{i}_THDL@LEG{i}': THDL,
            f'NUTHEX{i}@NUTHEX{i}': nutAF, f'DEPTH@NUTCUT{i}': m['NUTT']}
    pitch = 1 / G.tpi_of(e['thr'])
    tcols = {f'THDDIA@THD_End{i}': e['TM'], f'THDPITCH@THD_End{i}': round(pitch, 5), f'DEPTH@THD_End{i}': THDL,
             f'Profile_Height@THD_End{i}_PROF': round(0.54127 * pitch, 5), f'Profile_Land@THD_End{i}_PROF': round(0.25 * pitch, 5), f'THDPITCH@THD_End{i}_PROF': round(pitch, 5)}
    top = max(BR, m['WR'], Rn)
    dims = [('len', -1, f'M{i}', LEG, LEG / 2, top + 0.6), ('rad', 1, 'BODYR', BR, sh / 2, -0.4), ('len', 1, f'NW{i}_BODYL', sh, sh / 2, top + 0.45),
            ('rad', 3, f'NW{i}_NECKR', m['NECKR'], (sh + n0) / 2, -0.25), ('len', 3, f'NW{i}_NECKL', m['NECKL'], (sh + n0) / 2, top + 0.35),
            ('ptl', 5, 'False', AX, f'NW{i}_CHR', rc, n0 - 0.05, rc / 2),
            ('ang', 5, 6, f'NW{i}_CHANG1', chA, n0 + ch - 0.03, Rn - 0.01),
            ('rad', 6, f'NW{i}_NUTR', Rn, (n0 + w0) / 2, -0.45),
            ('ang', 6, 7, f'NW{i}_CHANG2', chA, w0 - ch + 0.03, Rn - 0.01),
            ('pair', 4, 8, f'NW{i}_NUTT', m['NUTT'], (n0 + w0) / 2, top + 0.25),
            ('ptl', 8, 'False', AX, f'NW{i}_CHR2', rc, w0 + 0.05, rc / 2),
            ('rad', 9, f'NW{i}_WASHR', m['WR'], (w0 + w1) / 2, -0.35), ('len', 9, f'NW{i}_WASHT', m['WT'], (w0 + w1) / 2, top + 0.2),
            ('rad', 11, f'NW{i}_UCR', UR, (w1 + te) / 2, -0.15), ('rad', 13, f'THDMAJR_B{i}', rM, (te + LEG) / 2, -0.3),
            ('len', 13, f'NW{i}_THDL', THDL, (te + LEG) / 2, top + 0.15)]
    return dict(kind='NWO', dash=dash, V=V, endlen=I3, cols=cols, tcols=tcols, dims=dims, rmax=max(m['WR'], nutAF / 2), m=m,
                nut=dict(n0=n0, w0=w0, dep=m['NUTT'], af=nutAF, rc=rc, Rn=Rn), sh=sh, te=te, UR=UR, rM=rM, thr=e['thr'] + ' (adjustable male ORB)',
                thread=dict(type='CUT', ex=te, er=rM, depth=THDL, size=f"{e['TM']:.4f}-{G.tpi_of(e['thr']):g}", pitch=pitch), tipR=rM)


def nwo_nut_removed(nut, n=4000):
    """volume (in^3) of the revolved, chamfered locknut envelope lying outside the hexagon (what NUTCUTi removes): numerical integral
    over the nut thickness of (disc of the envelope radius minus the hexagon, flats d = AF/2, corners Rc)"""
    n0, w0, rc, Rn, af = nut['n0'], nut['w0'], nut['rc'], nut['Rn'], nut['af']
    d = af / 2; Rc = af / math.sqrt(3); k = 1 / math.tan(math.radians(NWO_CHANG)); tot = 0.0; h = (w0 - n0) / n
    for j in range(n):
        a = n0 + (j + 0.5) * h
        r = min(Rn, rc + (a - n0) * k, rc + (w0 - a) * k)
        if r <= d: continue
        if r >= Rc: tot += math.pi * r * r - 2 * math.sqrt(3) * d * d
        else: tot += 6 * (r * r * math.acos(d / r) - d * math.sqrt(r * r - d * d))
    return tot * h


# 2026-10-01 (Q-NEW-6802E45CHECK, user-approved): 45 deg elbows with an adjustable ORB leg (6802). The ORB leg lies on +X, the other leg
# on the 135 deg axis, i.e. it points AWAY from the ORB leg. The locknut check used the 90-deg rule (the other leg's thread radius counts
# as its reach across this leg) - wrong at 135 deg: a point of the angled leg at axial a, radius r reaches only a*cos135 + r*sin135
# along +X, so its farthest reach is the hex-arm corner at the crossing (AC*cos45; the forged arm starts there, flats normal to Z, corners
# in the leg plane). That blocked 6802-20-16 / -20-20 / -24-24 for no geometric reason.
# Second change: the CORNER NECK TRIM (feature ORBTRIMi). Where the forged corner (30deg puck, the angled hex arm or its leg core) stands
# out of the ORB neck beyond the ORB body face, the turned ORB stud cuts it back: a revolve cut about the ORB axis from the body face through
# the neck and the locknut's inner 15deg chamfer to the full nut corner, down to the ORB profile (Brennan 6502-12-12-FG STEP, 45 deg swivel
# elbow: the forged corner stops at the body face, only the turned neck beyond it). Every other part of the corner beyond the body face must
# lie inside the ORB end's revolved profile (sampled check below). The trim exists only in macros where some configuration needs it (none of
# the current 6802 rows; the MISSING 6802-32-32-NWO-FG would) and is suppressed ($STATE S) in every configuration that does not need it.
NWO_TRIM_MIN = 0.02       # corner material standing >= this far outside the ORB neck / nut chamfer -> trimmed; within +-this -> near-tangent, BLOCKED
NWO_BEYOND_MIN = 0.01     # past the full nut corner, corner material must stay this far inside the ORB end's revolved profile
NWO_TRIM_RO = 0.10        # outer radius of the trim loop = max(nut envelope radius, sqrt(2)*AC) + this (sqrt(2)*AC bounds every corner point there)
NWO_TRIM_ASSUME = ('CORNER NECK TRIM (45 deg elbow, 2026-10-01, feature ORBTRIM): the forged corner (30deg puck / angled hex arm) stands out of the adjustable '
                   'ORB neck beyond the body face; it is cut back about the ORB axis to the ORB profile (neck, locknut inner face and inner 15deg chamfer, from '
                   'the body face to the full nut corner) - as the turned ORB stud would leave it (Brennan 6502-12-12-FG STEP, 45 deg swivel elbow: the forged '
                   'corner stops at the body face, only the neck beyond it). ASSUMPTION for the 6802 forging: no Brennan 6802 STEP measured')


def e45_reach(o, AC):
    """farthest reach ALONG +X of a leg lying on the 135 deg axis: its hex arm starts at the crossing (corner at AC in the leg plane) and
    its revolved profile V (a along its own axis, r radius) reaches a*cos135 + r*sin135"""
    return max([AC * UYV] + [a * UXV + r * UYV for (a, r) in o['V']])


def env_radius(V, x):
    """radius of a leg's revolved profile V at axial x (the larger side at a radial step)"""
    best = None
    for (a1, r1), (a2, r2) in zip(V, V[1:]):
        if min(a1, a2) - 1e-9 <= x <= max(a1, a2) + 1e-9:
            r = max(r1, r2) if abs(a2 - a1) < 1e-12 else r1 + (r2 - r1) * (x - a1) / (a2 - a1)
            best = r if best is None else max(best, r)
    return best


def e45_foreign(L, legs, BR, AC, n=120):
    """45 deg elbow, adjustable ORB leg L on +X: sample the surfaces of the OTHER material near the crossing - the angled leg's hex arm (from
    the crossing to its hexl, flats normal to Z) and revolved leg, and the 30deg corner puck - and report, per zone along +X beyond the body
    face, the largest radial excess over L's own revolved profile: zone 'trim' = body face .. full nut corner (n0 + chamfer run),
    'beyond' = past it. Returns {(piece, zone): (excess, x, r)}; excess < 0 = inside the ORB end."""
    sh = L['sh']; nut = L['nut']; V = L['V']
    xT = nut['n0'] + (nut['Rn'] - nut['rc']) * math.tan(math.radians(NWO_CHANG))
    NXV, NYV = -UYV, UXV; T30 = math.tan(math.radians(30)); res = {}
    def put(piece, X, Y, Z):
        if X <= sh + 1e-6: return
        R = env_radius(V, X)
        if R is None: R = 0.0                                     # past the ORB tip: nothing of the ORB end there
        r = math.hypot(Y, Z); e = r - R; k = (piece, 'trim' if X <= xT + 1e-9 else 'beyond')
        if k not in res or e > res[k][0]: res[k] = (e, X, r)
    hexv = [(AC, 0.0), (AC / 2, BR), (-AC / 2, BR), (-AC, 0.0), (-AC / 2, -BR), (AC / 2, -BR)]
    for o in legs:
        if o is L: continue
        amax = min(o['hexl'], AC - math.sqrt(2) * sh)            # a point of the hex arm at axial a reaches at most (AC - a)*cos45 along +X
        if amax > 0:
            for k in range(n + 1):
                a = amax * k / n
                for j in range(6):
                    (p1, z1), (p2, z2) = hexv[j], hexv[(j + 1) % 6]
                    for t in range(24):
                        p = p1 + (p2 - p1) * t / 24; z = z1 + (z2 - z1) * t / 24
                        put('angled hex arm', a * UXV + p * NXV, a * UYV + p * NYV, z)
            for ip in range(41):                                  # its end face at the crossing
                for iz in range(41):
                    p = -AC + 2 * AC * ip / 40; z = -BR + 2 * BR * iz / 40
                    if abs(p) <= AC - abs(z) * T30 + 1e-12: put('angled hex arm', p * NXV, p * NYV, z)
        for (a1, r1), (a2, r2) in zip(o['V'], o['V'][1:]):
            if max(r1, r2) - min(a1, a2) <= math.sqrt(2) * sh: continue      # a*cos135 + r*sin135 <= sh everywhere on this segment
            for k in range(n + 1):
                a = a1 + (a2 - a1) * k / n; r = r1 + (r2 - r1) * k / n
                for j in range(144):
                    ph = 2 * math.pi * j / 144; p = r * math.cos(ph)
                    put('angled leg', a * UXV + p * NXV, a * UYV + p * NYV, r * math.sin(ph))
    for k in range(n + 1):                                        # puck: two 30deg cones about Z ...
        z = -BR + 2 * BR * k / n; R = AC - abs(z) * T30
        if R <= sh: continue
        tm = math.acos(sh / R)
        for j in range(241):
            th = -tm + 2 * tm * j / 240; put('corner puck', R * math.cos(th), R * math.sin(th), z)
    if AC / 2 > sh:                                               # ... and its flat top / bottom (radius AC/2)
        for z in (-BR, BR):
            for k in range(1, 41):
                R = AC / 2 * k / 40
                for j in range(181):
                    th = math.pi * (j / 90 - 1); put('corner puck', R * math.cos(th), R * math.sin(th), z)
    return res


def nwo_trim_geo(L, AC):
    """loop of the corner neck trim (revolve cut about the ORB axis), from the body face: (x, r) points and its table values"""
    m = L['m']; nut = L['nut']; sh = L['sh']; n0 = nut['n0']; rc = nut['rc']; Rn = nut['Rn']
    # the trim follows the ORB leg's own surfaces EXACTLY (neck radius, nut face, chamfer cone): coincident, never nearly coincident. So the
    # chamfer run is NOT rounded - it must equal the run SolidWorks solves from the leg's own 75deg chamfer angle, (Rn - rc) * tan 15
    ch = (Rn - rc) * math.tan(math.radians(NWO_CHANG)); x1 = n0 + ch
    RO = round(max(Rn, math.sqrt(2) * AC) + NWO_TRIM_RO, 4)
    pts = [(sh, m['NECKR']), (n0, m['NECKR']), (n0, rc), (x1, Rn), (x1, RO), (sh, RO)]
    vals = dict(X0=sh, NECKL=round(n0 - sh, 4), NECKR=m['NECKR'], FACEH=round(rc - m['NECKR'], 5), CHL=ch, TOPH=round(RO - Rn, 5), RO=RO)
    return pts, vals


def leg_NPTFM(i, dash, M, BR):
    nps, tpi, D, E0, E1, L1, L2 = G.NPTF[dash]; P = 1 / tpi
    rS = (E0 + 0.8 * P) / 2; rL = rS + L2 * math.tan(TAPER); endl = G.ENDL[dash]; sh = M - endl
    assert endl > L2 + 1e-6
    V = [(0, 0), (0, BR), (sh, BR), (sh, rL), (M - L2, rL), (M, rS), (M, 0)]
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': round(BR, 5), f'NPTF{i}_MAJR@LEG{i}': round(rS, 5), f'NPTF{i}_THDL@LEG{i}': L2,
            f'NPTF{i}_TAPER@LEG{i}': 1.7899, f'NPTF{i}_RELL@LEG{i}': round(endl - L2, 4)}
    tcols = {f'HELIXDIA@HELIXSK_{i}': round(2 * rS, 5), f'HEIGHT@HELIX_{i}': L2, f'PITCH@HELIX_{i}': round(P, 5),
             f'PROF_R@THDPROF_{i}': round(rS, 5), f'APEXR@THDPROF_{i}': round(rS - 0.8 * P, 5), f'PROF_AX@THDPROF_{i}': M}
    dims = [('len', -1, f'M{i}', M, M / 2, BR + 0.6), ('rad', 1, 'BODYR', BR, sh / 2, -0.4),
            ('len', 5, f'NPTF{i}_MAJR', rS, M + 0.15, rS / 2), ('ptl', 4, 'False', 5, f'NPTF{i}_THDL', L2, M - L2 / 2, BR + 0.25),
            ('ang', 4, 6, f'NPTF{i}_TAPER', 1.7899, M - L2 / 2, rS * 0.5), ('len', 3, f'NPTF{i}_RELL', endl - L2, (sh + M - L2) / 2, BR + 0.15)]
    return dict(kind='NPTFM', dash=dash, V=V, endlen=endl, cols=cols, tcols=tcols, dims=dims, rmax=rL,
                thr=G.npt_thr(dash) + ' NPTF', thread=dict(type='HELIX', r=rS, height=L2, pitch=P, thdh=0.8 * P, taperOut=True, apexOut=False),
                tipR=rS)


def leg_NPTFF(i, dash, M, BR, td, conn, split=False, p1=None):
    f = G.FPT[dash]; P = 1 / G.tpi_of(f['thr'])
    P1 = f['P1'] if p1 is None else p1      # 2026-10-02: a row's own measured port thread length (SPEC 'p1' column) replaces the MS51503 P1
    V = [(0, 0), (0, BR), (M, BR), (M, 0)]
    cols = {f'M{i}@LEG{i}': M, f'BODYR@LEG{i}': round(BR, 5)}
    if split and conn is not None and conn > td:
        # elbows: keep one feature layout for every config - a connecting drill larger than the tap drill is capped at the
        # tap drill (= the tap drill carried to the crossing, as on the tees), cut as a separate BORE feature
        conn = td
    to_centre = conn is None or (conn >= td - 1e-9 and not split)
    pk = M if to_centre else P1
    tcols = {f'HELIXDIA@HELIXSK_{i}': td, f'HEIGHT@HELIX_{i}': P1, f'PITCH@HELIX_{i}': round(P, 5),
             f'PROF_R@THDPROF_{i}': round(td / 2, 5), f'APEXR@THDPROF_{i}': round(td / 2 + 0.8 * P, 5), f'PROF_AX@THDPROF_{i}': M}
    dims = [('len', -1, f'M{i}', M, M / 2, BR + 0.6), ('rad', 1, 'BODYR', BR, M / 2, -0.4)]
    return dict(kind='NPTFF', dash=dash, V=V, endlen=0.0, cols=cols, tcols=tcols, dims=dims, rmax=td / 2, td=td, P1=P1,
                pocket=pk, to_centre=to_centre, conn=conn, thr=f['thr'],
                thread=dict(type='HELIX', r=td / 2, height=P1, pitch=P, thdh=0.8 * P, taperOut=False, apexOut=True), tipR=None)


def leg_JICSW(i, dash, M5, BR, M10, nutAF):
    # female 37deg JIC SWIVEL leg: hex arm to the measured body face, neck, nut (skirt + hex), nut thread, slot, nose, 37deg seat.
    # M5 = crossing to the nut face, M10 = crossing to the nose tip (Air-Way); the rest is the measured Brennan swivel end.
    s_nt = round(M5 - M10, 4)
    E = G.end_JICSW(dash, str(i), s_nt, nutAF)
    m = E['m']; sh = round(M5 - m['BODYS'], 4)
    V = [(0, 0), (0, BR), (sh, BR)] + [(M5 - s_, r_) for (s_, r_) in E['VO'][::-1]] + [(M5 - s_, r_) for (s_, r_) in E['VG']]
    assert len(V) == 19
    cols = {f'M{i}@LEG{i}': M5, f'BODYR@LEG{i}': round(BR, 5)}
    tcols = {}
    for k_, v_ in E['cols'].items():
        if k_.endswith('@DRIVE'): cols[k_.replace('@DRIVE', f'@LEG{i}')] = v_
        else: tcols[k_] = v_
    tcols[f'PROF_AX@THDPROF_{i}'] = M5
    cols[f'NUTHEX{i}@NUTHEX{i}'] = nutAF; cols[f'DEPTH@NUTCUT{i}'] = m['HEXL']
    top = max(BR, E['Rn'])
    a_ = lambda s_: M5 - s_
    dims = [('pair', 0, 9, f'M{i}', M5, M5 / 2, top + 0.7), ('rad', 1, 'BODYR', BR, sh / 2, -0.4),
            ('pair', 2, 9, f'SW{i}_BODYS', m['BODYS'], a_(m['BODYS'] / 2), top + 0.55), ('rad', 3, f'SW{i}_NECKR', m['NECKR'], (sh + a_(m['NUTL'])) / 2, -0.15),
            ('pair', 4, 9, f'SW{i}_NUTL', m['NUTL'], a_(m['NUTL'] / 2), top + 0.45), ('rad', 5, f'SW{i}_SKIRTR', m['SKR'], a_((m['NUTL'] + m['SKS']) / 2), -0.3),
            ('len', 5, f'SW{i}_SKIRTL', m['NUTL'] - m['SKS'], a_((m['NUTL'] + m['SKS']) / 2), top + 0.2),
            ('ptl', 7, 'False', 18, f'SW{i}_SKIRTFR', m['SKF'], a_(m['HEXL']) - 0.05, m['SKF'] / 2),
            ('len', 8, f'SW{i}_NUTHEXL', m['HEXL'], a_(m['HEXL'] / 2), top + 0.3), ('rad', 8, f'SW{i}_NUTR', E['Rn'], a_(m['HEXL'] / 2), -0.45),
            ('ptl', 10, 'False', 18, f'SW{i}_CSR', E['rcs'], M5 + 0.1, E['rcs'] / 2), ('ang', 10, 18, f'SW{i}_CSANG', G.SW_CSANG, a_(E['cs'] / 2), E['rcs'] + 0.08),
            ('rad', 11, f'SW{i}_MINR', E['rmin'], a_((E['cs'] + m['TE']) / 2), -0.6), ('len', 11, f'SW{i}_THDL', m['TE'] - E['cs'], a_((E['cs'] + m['TE']) / 2), top + 0.1),
            ('ang', 12, 18, f'SW{i}_RELANG', G.SW_RELANG, a_((m['TE'] + E['scb0']) / 2), E['rmin'] + 0.05),
            ('rad', 13, f'SW{i}_RELR', m['RELR'], a_((E['scb0'] + m['FLOOR']) / 2), -0.75),
            ('pair', 14, 9, f'SW{i}_FLOOR', m['FLOOR'], a_(m['FLOOR'] / 2), top + 0.65), ('rad', 15, f'SW{i}_NOSER', m['NOSER'], a_((m['FLOOR'] + s_nt) / 2), -0.9),
            ('pair', 16, 9, f'SW{i}_NOSETIP', s_nt, a_(s_nt / 2), top + 0.75),
            ('ptl', 17, 'False', 18, f'SW{i}_SEATR', m['SEATR'], a_(s_nt) - 0.05, m['SEATR'] / 2),
            ('ang', 17, 18, f'SW{i}_SEATANG', G.SW_SEATANG, a_(s_nt) - 0.1, m['SEATR'] * 0.3)]
    t = E['thread']
    return dict(kind='JICSW', dash=dash, V=V, endlen=m['BODYS'], cols=cols, tcols=tcols, dims=dims, rmax=nutAF / 2, nut_af=nutAF,
                thr=E['thr'], thread=dict(type='HELIX', r=t['r'], height=t['height'], pitch=t['pitch'], thdh=t['thdh'], taper=0.0, taperOut=False, apexOut=True),
                tipR=m['SEATR'], Mtip=M5, s_nt=s_nt, m=m, E=E)


def leg_NPSMSW(i, dash, M1, BR, W3, nutAF):
    # female NPSM (pipe) SWIVEL leg, from the Brennan 1404-08-08 STEP (G.end_NPSMSW): hex arm to the body face, neck, nut (lip,
    # 14deg skirt, hex), straight NPSM nut thread, 45deg relief, counterbore/slot, stem with the 30deg male cone and its tip face.
    # W3 = crossing to the NUT FACE, M1 = crossing to the STEM TIP (Air-Way; W3 - M1 = W - L of the 1404 union = 0.33 at -08).
    s_tip = round(W3 - M1, 4)
    E = G.end_NPSMSW(dash, str(i), s_tip, nutAF)
    m = E['m']; s_body = E['endlen']; sh = round(W3 - s_body, 4)
    V = [(0, 0), (0, BR), (sh, BR)] + [(W3 - s_, r_) for (s_, r_) in E['VO'][::-1]] + [(W3 - s_, r_) for (s_, r_) in E['VG']]
    assert len(V) == 20
    cols = {f'M{i}@LEG{i}': W3, f'BODYR@LEG{i}': round(BR, 5)}
    tcols = {}
    for k_, v_ in E['cols'].items():
        if k_.endswith('@DRIVE'): cols[k_.replace('@DRIVE', f'@LEG{i}')] = v_
        else: tcols[k_] = v_
    tcols[f'PROF_AX@THDPROF_{i}'] = W3
    cols[f'NUTHEX{i}@NUTHEX{i}'] = nutAF; cols[f'DEPTH@NUTCUT{i}'] = m['HEXL']
    top = max(BR, E['Rn']); a_ = lambda s_: W3 - s_; AX = 19
    dims = [('pair', 0, 9, f'M{i}', W3, W3 / 2, top + 0.7), ('rad', 1, 'BODYR', BR, sh / 2, -0.4),
            ('pair', 2, 9, f'NP{i}_BODYS', s_body, a_(s_body / 2), top + 0.55), ('rad', 3, f'NP{i}_NECKR', m['NECKR'], (sh + a_(m['NUTL'])) / 2, -0.15),
            ('pair', 4, 9, f'NP{i}_NUTL', m['NUTL'], a_(m['NUTL'] / 2), top + 0.45), ('rad', 5, f'NP{i}_LIPR', m['SKR'], a_((m['NUTL'] + m['SKS']) / 2), -0.3),
            ('len', 5, f'NP{i}_LIPL', round(m['NUTL'] - m['SKS'], 4), a_((m['NUTL'] + m['SKS']) / 2), top + 0.2),
            ('ptl', 7, 'False', AX, f'NP{i}_SKIRTFR', m['SKF'], a_(m['HEXL']) - 0.05, m['SKF'] / 2),
            ('len', 8, f'NP{i}_NUTHEXL', m['HEXL'], a_(m['HEXL'] / 2), top + 0.3), ('rad', 8, f'NP{i}_NUTR', E['Rn'], a_(m['HEXL'] / 2), -0.45),
            ('ptl', 10, 'False', AX, f'NP{i}_CSR', m['CSR'], W3 + 0.1, m['CSR'] / 2), ('ang', 10, AX, f'NP{i}_CSANG', G.NPSM_CSANG, a_(E['cs'] / 2), m['CSR'] + 0.08),
            ('rad', 11, f'NP{i}_MINR', m['MINR'], a_((E['cs'] + m['TE']) / 2), -0.6), ('len', 11, f'NP{i}_THDL', round(m['TE'] - E['cs'], 4), a_((E['cs'] + m['TE']) / 2), top + 0.1),
            ('ang', 12, AX, f'NP{i}_RELANG', G.NPSM_RELANG, a_((m['TE'] + m['RB0']) / 2), m['MINR'] + 0.05),
            ('ptl', 13, 'False', AX, f'NP{i}_RELR', m['RELR'], a_(m['RB0']) + 0.03, m['RELR'] / 2),
            ('rad', 14, f'NP{i}_CBR', m['CBR'], a_((m['RB0'] + m['CBEND']) / 2), -0.75),
            ('pair', 15, 9, f'NP{i}_CBEND', m['CBEND'], a_(m['CBEND'] / 2), top + 0.65),
            ('rad', 16, f'NP{i}_STEMR', m['STEMR'], a_((m['CBEND'] + E['s_cone']) / 2), -0.9),
            ('ang', 17, AX, f'NP{i}_CONEANG', G.NPSM_CONEANG, a_(s_tip) - 0.08, m['TIPR'] * 0.3),
            ('ptl', 18, 'False', AX, f'NP{i}_TIPR', m['TIPR'], a_(s_tip) - 0.05, m['TIPR'] / 2),
            ('pair', 18, 9, f'NP{i}_STEMTIP', s_tip, a_(s_tip / 2), top + 0.75)]
    t = E['thread']
    return dict(kind='NPSMSW', dash=dash, V=V, endlen=s_body, cols=cols, tcols=tcols, dims=dims, rmax=nutAF / 2, nut_af=nutAF,
                thr=E['thr'], thread=dict(type='HELIX', r=t['r'], height=t['height'], pitch=t['pitch'], thdh=t['thdh'], taper=0.0, taperOut=False, apexOut=True),
                tipR=m['TIPR'], Mtip=W3, s_nt=s_tip, s_tip=s_tip, m=m, E=E)


def puck_margin(a, r, AC, BR):
    # smallest (distance - puck radius) over the circle at axial a, radius r of a leg lying in the XY plane:
    # > 0 means the circle is outside the 30deg double-cone puck about Z (radius AC - |z| tan30)
    worst = 1e9
    for k in range(0, 91):
        ph = math.radians(k); z = r * math.sin(ph)
        if z > BR: continue
        lim = AC - z * math.tan(math.radians(30))
        if lim <= 0: continue
        worst = min(worst, math.sqrt(a * a + (r * math.cos(ph)) ** 2) - lim)
    return worst


# 2026-10-01 (NECK-6502): SWIVEL NECK TURN on a 45 deg elbow (6502: female JIC swivel on leg 1 along +X, male JIC on the 135 deg leg).
# The 30deg corner puck (radius AC about Z) and the start corner of the angled hex arm (sqrt(2)/2 * AC along +X) reach past the
# swivel body face; at 6502-05-05 / -12-12 (and 6502-16-12 with the OMi legs) they stood OUT of the neck there (batch 13a "STILL OUT").
# Brennan 6502-12-12-FG STEP, tools/measure/neck45.py (validated on Brennan 6500-05-05 / -08-08 / -12-12-FG = SWIV_MEAS and 6502-08-08-FG =
# BRENNAN_NOTES): nut face 1.500, body face 0.412, neck 0.417, NOTHING outside the neck from the body face to the nut rear face (0.453) -
# an untrimmed corner (hex corner radius 0.6131) would stand 0.038 out of the neck at the body face. Brennan 1503-08-08-FG (NPSM swivel,
# 45 deg) is consistent: nothing outside its neck (0.304) where an untrimmed corner would stand 0.005 out.
# Model: NECKTRIM<i> = revolve cut about the leg axis over [body face, nut rear face] of the ring from TRIM rin out to TRIM_ROUT_K x the
# hex corner radius (beyond every forged point in that slab: puck <= AC, angled arm < sqrt(2) AC), then NECKFILL<i> = revolve boss of the
# ring from the same rin out to the neck radius. rin lies halfway between the neck and the larger of the leg bore radius and the swivel
# profile's own cavity in that slab (the 37deg seat cone drawn to its apex reaches into it at -32), so the ring the cut takes is always
# solid and the boss only puts back what the cut took. Both act in EVERY configuration: the cut always takes that ring (never a cut that
# removes nothing), the boss always puts it back, so a configuration whose corner stays inside the neck keeps exactly its geometry and one
# whose corner stood out of the neck loses only that part.
TRIM_ROUT_K = 1.5
SQ2 = math.sqrt(2.0)
NECK_ASSUME = ('swivel neck turned clear of the forged corner (Brennan 6502-12-12-FG STEP, tools/measure/neck45.py, 2026-10-01: body face 0.412, '
               'neck 0.417, nothing outside the neck from the body face to the nut rear face 0.453, where an untrimmed corner would stand 0.038 out; '
               'Brennan 1503-08-08-FG consistent): from the swivel body face to the swivel nut rear face the 30deg corner puck and the start corner '
               'of the angled hex arm are cut down to the neck radius (NECKTRIM1 revolve cut + NECKFILL1 ring back to the neck, in every '
               'configuration; no change where the corner stays inside the neck) - measured on ONE size whose corner stands out of the neck (-12), '
               'ASSUMED for the other sizes (-05)')


# 2026-10-18 (ANGLED, N1 / N2 - Q-ANGLED-NECKNPSM settled from Brennan, user A15 2026-10-18 "look at Brennan parts"): tools/measure/neck45.py on the
# Brennan 45 deg NPSM swivel forgings (tools/_out/genfeat_20261018/angled/scripts/neck45_1503_1504_out.txt): the body face lies inside the hex corner
# radius and NOTHING stands outside the neck between the body face and the nut rear face - the corner is turned down to the neck, as on 6502.
ANGLED_NECK_ASSUME = ('NPSM swivel neck turned clear of the forged corner as on 6502 (NECKTRIM1 revolve cut + NECKFILL1 ring back to the neck, in every '
                      'configuration; no change where the corner stays inside the neck): Brennan 1503-08-08-FG / 1503-12-08-FG / 1504-06-06-FG STEPs '
                      '(tools/measure/neck45.py 2026-10-18): body face 0.400 / 0.570 / 0.360 inside the hex corner radius 0.5052 / 0.6131 / 0.5052, '
                      'neck 0.304 / 0.304 / 0.2465, nothing outside the neck from the body face to the nut rear face (excess 0.000) - ASSUMED for every '
                      'NPSM size (Q-ANGLED-NECKNPSM, settled from the Brennan STEPs 2026-10-18); past the swivel slot start the corner must lie inside the '
                      'stem by 0.02 (slot test on what the corner reaches, N2)')
# Q-ANGLED-P1 (settled from Brennan 2026-10-18): the female NPTF port depth Brennan draws (face to the bottom of the 1.79deg tapered port, 45deg mouth
# included), tools/_out/genfeat_20261018/angled/scripts/brennan_port_depths_out.txt - the same value on every Brennan STEP of a size. Used ONLY through a
# row's PORTDEPTH cell (SPEC p1) where the MS51503 P1 library value does not fit the short 45 deg leg; text only here.
ANGLED_P1_NOTE = {4: '0.560 (Brennan 2502-06-04-FG, 5405-04-04, 5406-08-04, 5502-04-04-FG STEPs)',
                  6: '0.580 (Brennan 1504-06-06-FG, 2611-06-06-06-FG, 5601-06-06-06-FG STEPs)',
                  8: '0.750 (Brennan 1502 / 2505 / 2606 / 5502 / 5504 / 5505 / 5603 / 5605 / 5652 -08 STEPs and 5 more)',
                  12: '0.770 (Brennan 5405-12-12, 6506-12-14 STEPs)',
                  16: '0.940 (Brennan 5405-16-16, 5502-16-16-FG, 5503-16-16-FG STEPs)',
                  32: '0.970 (Brennan 5406-40-32 STEP)'}


def angled_nptff_text(sp):
    """2026-10-18 (ANGLED): the female-port sentence of 1504 / 5503 / 5505 (tap drill, port depth, connecting drill - sources named)"""
    cn = (f"the part's own {sp['conn'].split('@')[0]} column (the male bore; capped at the tap drill where larger)" if sp.get('conn')
          else 'the tap drill carried to the crossing (Brennan 1504-06-06-FG / 5503-16-16-FG / 5505-08-08-FG STEPs, OCP 2026-10-18: the drill runs '
               'from the bottom of the tapered port to the axis crossing and ends flat there; the other leg bore opens into it)')
    return ("female NPTF legs: tap drill = the row's TAPDRILL (end library: the per-size tap drill every built female pipe port carries, Q-TRANSFER-ENDLIB "
            "= yes 2026-10-08), tapered helix over MS51503 P1 max (" + BR5405 + ") - where that does not fit the short 45 deg leg (P1 >= leg - 0.05) over "
            "the row's " + sp['p1'].split('@')[0] + " = the port depth Brennan draws for that size (Q-ANGLED-P1, settled from the Brennan STEPs 2026-10-18; "
            "said per leg below); connecting drill to the axis crossing = " + cn + '; the 1.79deg port cone and the 45deg mouth chamfer are NOT modelled')


def angled_texts(sp, legs):
    """2026-10-18 (ANGLED, design review B2): the $PRP@AxialSource sentences of the three capabilities - only for a leg on the 135 deg axis that
    carries a helical thread, a female port or a swivel nut (no released root has one, so no released text changes)"""
    if not sp.get('e45'): return []
    t = []; P_ = place(sp)
    U = [L for i, L in enumerate(legs, 1) if P_[i][0] == 'U' and (L['thread'] or {}).get('type') == 'HELIX']
    if not U: return t
    L = U[0]; k = L['kind']
    if k == 'NPTFM':
        t.append('male NPTF end on the 45 deg leg (Q-NEW-ANGLEDHELIX): the library male end of the axis legs (ASME B1.20.3 cone + relief to the 5404 end '
                 'length) turned to the 135 deg axis; its bore ends at the axis crossing as on every built root (Brennan 5501-08-08-FG / 5503-16-16-FG '
                 'STEPs, OCP 2026-10-18: the male drill runs on a little past the crossing, and Brennan draws its own simplified thread cone and a bore-mouth '
                 'countersink - NOT modelled)')
    elif k == 'NPTFF':
        t.append('female NPTF port on the 45 deg leg (Q-NEW-ANGLEDFEMALE): the 5504 / 1502 forged female leg turned to the 135 deg axis - hex arm to 0.26 '
                 'short of the port face, round collar of dia = the hex flats, tap drill from the port face (pocket), tapered helical thread over the port '
                 'depth (Brennan 1504-06-06-FG / 5505-08-08-FG / 5503-16-16-FG STEPs: collar 0.26 at the flats dia on the 45 deg leg, the same end as on '
                 'the axis legs)')
    else:
        t.append('swivel on the 45 deg leg (Q-NEW-ANGLEDNUT): the swivel end of the axis legs (same end library) turned to the 135 deg axis, its forged '
                 'hex arm ending at the body face; the nut hex is cut on the nut face (NutHexCutV: hexagon with flats normal to Z, outside cut over the '
                 'nut hex length, accepted only when the cut is centred on the nut). Composed shape: no Brennan STEP of this series measured (pilot '
                 'STEP on the download list) - ASSUMPTION')
    t.append('helical thread on the 45 deg leg (HelixThreadV, 2026-10-18): helix on the leg end face (circle centred on the leg axis), started in the '
             'Front Plane, right hand, into the part, tapered as on the axis legs; 60deg tooth profile on the Front Plane with its sides parallel / '
             'normal to the leg axis, swept along the helix - the thread of the axis legs (HelixThread) about the 135 deg axis; SolidWorks\' Thread '
             'feature is not used there (an off-axis Thread feature crashed SolidWorks 2026-10-15); drawing-only thread, suppressed in the saved model and STEP')
    for i, Lf in enumerate(legs, 1):
        if Lf['kind'] == 'NPTFF' and abs(Lf['P1'] - G.FPT[Lf['dash']]['P1']) > 1e-9:
            t.append(f'leg {i} port depth {Lf["P1"]:.3f} = the row {sp["p1"].split("@")[0]} instead of MS51503 P1 {G.FPT[Lf["dash"]]["P1"]} (which does not fit '
                     f'the {Lf["V"][-1][0]:.2f} leg): the port depth Brennan draws for -{Lf["dash"]:02d}: {ANGLED_P1_NOTE.get(Lf["dash"], "no Brennan STEP of this size")}')
    return t


def neck_trim_leg(sp, i, L):
    """legs that carry the NECKTRIM / NECKFILL turn: a female JIC swivel on the +X leg of a 45 deg elbow (6502); 2026-10-18 (ANGLED, N1):
    with SPEC neck_turn also a female NPSM swivel on the +X leg (1503 / 1504)"""
    if sp.get('neck_turn'):
        return bool(sp.get('e45')) and L['kind'] in ('JICSW', 'NPSMSW') and place(sp)[i] == (0, +1)
    return bool(sp.get('e45')) and L['kind'] == 'JICSW' and place(sp)[i] == (0, +1)


def inner_env(V, a, rlim):
    """2026-10-18 (ANGLED, N2): radius of a swivel leg's solid core at axial a beyond the slot start - the NPSM stem (or the JIC nose) as the
    inner profile V[9:] draws it: the largest radius of the segments spanning a that lie at or below rlim (stem / nose radius); 0 past its tip"""
    best = 0.0
    for (pa, pr), (qa, qr) in zip(V[9:-1], V[10:]):
        if max(pr, qr) > rlim + 1e-9: continue
        lo, hi = min(pa, qa), max(pa, qa)
        if a < lo - 1e-9 or a > hi + 1e-9: continue
        best = max(best, max(pr, qr) if abs(qa - pa) < 1e-12 else pr + (qr - pr) * (a - pa) / (qa - pa))
    return best


def slot_reach_check(L, AC, BR, hexl2, slot_a, n=60):
    """2026-10-18 (ANGLED, N2): the slot test on what the forged corner really reaches - from the swivel slot start to the corner's end (AC)
    every corner point must lie inside the stem / nose (solid there) by 0.02: returns (worst margin, a, reach, core radius)"""
    rlim = L['m']['STEMR'] if L['kind'] == 'NPSMSW' else L['m']['NOSER']
    worst = None
    if AC <= slot_a: return None
    for k in range(n + 1):
        a = slot_a + (AC - slot_a) * k / n
        rc = corner_reach(a, AC, BR, hexl2); core = inner_env(L['V'], a, rlim); mg = core - rc
        if worst is None or mg < worst[0]: worst = (mg, a, rc, core)
    return worst


def corner_reach(a0, AC, BR, hexl2):
    """largest distance from the +X leg axis of the 45 deg elbow's forged corner at X >= a0: the 30deg double-cone puck about Z
    (radius R(z) = AC - |z| tan30, |z| <= BR) and the angled hex arm (flats normal to Z, half-width R(z) across its axis, from the
    crossing to hexl2 along 135 deg; its point s*u - t*n with u = (-1, 1)/sqrt2, n = (-1, -1)/sqrt2 lies at x = (t - s)/sqrt2,
    y = (t + s)/sqrt2). 0 when nothing of the corner reaches X = a0."""
    best = 0.0
    for k in range(401):
        z = BR * k / 400; R = AC - z * TAN30
        if R > a0: best = max(best, math.sqrt(R * R - a0 * a0 + z * z))            # puck: largest y at x = a0
        s = min(R - SQ2 * a0, hexl2)                                               # arm: t = R, the largest s with x >= a0
        if s >= 0: best = max(best, math.sqrt(0.5 * (R + s) ** 2 + z * z))
    return best


def slab_cavity(V, a0, a1):
    """largest radius of a swivel leg profile's own inner cavity (V[9] .. V[18]: nut face, thread, slot, nose, 37deg seat cone to its
    apex on the axis) over a0 <= a <= a1 - the material between it and the neck is solid before the bore is cut"""
    best = 0.0
    for (pa, pr), (qa, qr) in zip(V[9:-1], V[10:]):
        lo, hi = min(pa, qa), max(pa, qa)
        if hi < a0 or lo > a1: continue
        if abs(qa - pa) < 1e-12: best = max(best, pr, qr); continue
        for a in (max(lo, a0), min(hi, a1)): best = max(best, pr + (qr - pr) * (a - pa) / (qa - pa))
    return best


def dashes(pn):
    return [int(x) for x in re.findall(r'-(\d\d)(?=-|$)', pn)]


# ---------------------------------------------------------------- 2026-10-09 wave 2, PERLEGSW: per-leg end columns and end-library tokens
def legs4(sp):
    """the (kind, leg col, bore col, thread col) part of every SPEC leg (a leg may carry a 5th element: its own end columns)"""
    return [l[:4] for l in sp['legs']]


def leg_end(sp, k):
    """the end-column tuple of leg k (0-based): the leg's own 5th element, else the SPEC-wide sw / npsm / nwo tuple (every older root)"""
    l = sp['legs'][k]
    return l[4] if len(l) > 4 else sp[{'JICSW': 'sw', 'NPSMSW': 'npsm', 'NWO': 'nwo'}[l[0]]]


# END-LIBRARY tokens (Q-TRANSFER-ENDLIB = yes, user 2026-10-08 "reuse end details - yes"): token -> (library, key, what, source text)
ENDLIB_TOKENS = {
    '=ORB:THDL': ('ORB', 'THDL', 'adjustable ORB thread length', 'the ORB end library (6401 / 6405 / 6410 tables; = Air-Way 6801 ORB_THDL at every dash -02..-32)'),
    '=ORB:GD': ('ORB', 'GD', 'adjustable ORB undercut dia', 'the ORB end library (6401 / 6405 / 6410 tables; = Air-Way 6801 ORB_GRVDIA at every dash -02..-32)'),
    '=FPT:TD': ('FPT', 'TD', 'female NPTF tap drill', 'the female pipe port end library (per-size tap drill of the 2405 table, carried by every built female pipe port)'),
}
ENDLIB_TEXT = {
    '=6801': 'adjustable ORB tip-to-body-face = Air-Way 6801 ORB_I3 of the same ORB size (= the Brennan 6801 STEPs)',
    '=ORB:THDL': 'adjustable ORB thread length = the ORB end library (6401 / 6405 / 6410 tables, = Air-Way 6801 at every dash)',
    '=ORB:GD': 'adjustable ORB O-ring undercut dia = the ORB end library (6401 / 6405 / 6410 tables, = Air-Way 6801 at every dash)',
    '=FPT:TD': 'female NPTF tap drill = the female pipe port end library (2405 table tap drill), only where the row has none',
}


def end_val(r, c, d, i, warn):
    """an end value of leg i (dash d): the row's column c, or an END-LIBRARY token (ENDLIB_TOKENS / '=<root>' = the adjustable-ORB I3 of that
    Air-Way series); the source of every token value goes into the row's warnings ($COMMENT). A missing library entry raises KeyError."""
    if not (isinstance(c, str) and c.startswith('=')): return r[c]
    if c in r: return r[c]       # merge 2026-10-18: a HOSEB row copy carries the token values already (hoseb_endlib said their source)
    if c in ENDLIB_TOKENS:
        lib, key, what, src = ENDLIB_TOKENS[c]
        lv = getattr(G, lib)
        if d not in lv: raise KeyError(f'no -{d:02d} entry in the {lib} end library for {what}')
        v = lv[d][key]
        warn.append(f'leg {i}: {what} {v} = {src} for -{d:02d} (end library, Q-TRANSFER-ENDLIB 2026-10-08)')
        return v
    v = nwo_i3_from(c[1:], d)
    warn.append(f'leg {i}: adjustable ORB tip-to-body-face {v} = Air-Way {c[1:]} ORB_I3 for -{d:02d} (= Brennan 6801 STEP; not printed for this series - ASSUMPTION)')
    return v


def nptff_td(r, bc, d, i, sp, warn):
    """female NPTF tap drill of a leg: the row's column; on a perleg root an EMPTY cell takes the end-library tap drill ('=FPT:TD')"""
    return end_val(r, '=FPT:TD', d, i, warn) if r[bc] is None and sp.get('perleg') else r[bc]


ARM_RIDGE_EPS = 1e-4      # a hex corner standing more than this past a special leg's body face is a ridge (wave-1 1502 value, named once)
NUTSLAB_MIN = 0.003       # a nut cut's slab must start this far beyond every perpendicular leg's final reach and the body hex corner


def nut_slab(L):
    """(start, end) along its own axis of the slab a leg's nut hex cut clears to the hexagon (None for legs without a nut cut)"""
    if L['kind'] in ('JICSW', 'NPSMSW'): return (round(L['Mtip'] - L['m']['HEXL'], 4), L['Mtip'])
    if L['kind'] == 'NWO': return (L['nut']['n0'], L['nut']['w0'])
    return None


def final_reach(o):
    """largest distance from its own axis of a leg in the FINISHED part: swivel nut corners / skirt, adjustable-ORB washer / nut corners, else rmax"""
    if o['kind'] in ('JICSW', 'NPSMSW'): return max(o['nut_af'] / math.sqrt(3), o['m']['SKR'])
    if o['kind'] == 'NWO': return nwo_radial(o)
    return o['rmax']


def nwo_overlap(L, O, n=2000):
    """volume (in^3) of the perpendicular adjustable-ORB leg O's revolved locknut ENVELOPE lying beyond L's locknut slab start n0 (along L's
    axis): NUTCUTi of L (built first) removes it, so L's cut removes that much more and O's that much less than nwo_nut_removed(). The slab
    rule keeps O's final hex corners and L's below the other slab, so only the envelope margin can reach (circular segments, integrated)."""
    a0 = L['nut']['n0']; nu = O['nut']; k = 1 / math.tan(math.radians(NWO_CHANG)); h = (nu['w0'] - nu['n0']) / n; tot = 0.0
    for j in range(n):
        a = nu['n0'] + (j + 0.5) * h
        r = min(nu['Rn'], nu['rc'] + (a - nu['n0']) * k, nu['rc'] + (nu['w0'] - a) * k)
        if r > a0: tot += r * r * math.acos(a0 / r) - a0 * math.sqrt(r * r - a0 * a0)
    return tot * h


def pilot_text(root, legs, pn):
    """2026-10-02 (new masters wave 1, PIPE-TEES): the $PRP@AxialSource MODEL text of a row of a root whose shape is measured on its own
    Brennan pilot STEP (SPEC 'pilot'). = assume_text() with its shared body / collar / port / male sentences reworded for these roots - every
    rewording must match exactly once, so a changed shared sentence stops the generator here instead of leaving a wrong source in the
    table - plus the SPEC 'pilot_notes' and, per row, every female leg whose helical thread runs out into a perpendicular bore. Per row: only
    the pilot row is said to carry a value measured on its own STEP. Kept out of assume_text() (below) so no other root's text changes."""
    sp = SPEC[root]; pl = sp['pilot']; own = pn == pl; k = {L['kind'] for L in legs}; s = assume_text(root, legs)
    bars = 'two continuous bars (X and Y)' if sp.get('cross') else 'run bar continuous through the branch, branch hex arm'
    lib = 'end shape NOT taken from the pilot STEP, as on the accepted 5600 / 5602 / 5604 / 5605 masters - user decision Q-TRANSFER-ENDLIB open'
    hc = sp['hex'].split('@')[0]; port = f"1.79deg, {sp['pilot_port']:.3f} deep"
    af = f'max(the row {hc}, male thread majors)' if k - {'NPTFF'} else f'the row {hc} (no male leg)'
    ends = ' / '.join(x for c, x in (('NPTFF', 'to 0.26 short of a female face (round collar)'), ('NPTFM', 'to the 5404 end length of a male leg')) if c in k)
    reps = [('hex bars A/F = max(Air-Way hex, male thread majors), flats normal to Z, ' + bars + '; hex-end 75deg chamfers and edge fillets NOT modelled',
             f'hex bars A/F = {af}, flats normal to Z, {bars}; CONFIRMED on the Brennan {pl} pilot STEP (tools/measure/pipetee.py 2026-10-02, validated '
             f'on Brennan 5605-08-08-08-FG and 5600-16-16-16-FG): hex {ends}, flat hex ends with no chamfer and no edge fillet (the STEP has plane, '
             'cylinder and cone faces only); the 0.002-deep marks on its hex flats near the crossing are NOT modelled')]
    if 'NPTFM' in k:
        a = '0.001 proud of the 1.3125 flats)'
        reps.append((a, a + f"; male legs = the library NPTFM end ({lib}): on the Brennan {pl} pilot STEP the hex stops at the 5404 end length and "
                        "the bore of the row's drill column runs from the tip to the crossing (= the model); Brennan's relief ring at the pipe OD (0.03-0.04 "
                        'long), its simplified thread cone, the 45deg tip chamfer and the 30deg bore-mouth countersink are NOT modelled (ASSUMPTION)'))
    if 'NPTFF' in k:
        reps.append(('single manufacturer); port-mouth 45deg chamfer and hex chamfers not modelled',
                     f'single manufacturer; the Brennan {pl} pilot STEP too: collar 0.260 on every female leg); port-mouth 45deg chamfer not modelled'))
        reps.append(('female NPTF legs: Air-Way tap drill to MS51503 P1 max (' + BR5405 + '), tapered helix over P1; connecting drill to the axis crossing = '
                     'the tap drill carried to the crossing (ASSUMPTION: Air-Way publishes no bore for this part)',
                     f'female NPTF legs = the library NPTFF end ({lib}): a drill of the row TAPDRILL ('
                     + ('this row: the drill MEASURED on its own Brennan STEP' if own else "its source: this row's cell sources before ' | MODEL:'")
                     + f') from the port face to the axis crossing - on the Brennan {pl} pilot STEP the drill runs from the bottom of the tapered port '
                     f"to the crossing, so no separate connecting drill; helical NPTF thread over MS51503 P1 max ({BR5405}); the pilot's port taper "
                     f"({port}, shorter than P1) and its 45deg mouth chamfer are NOT modelled (ASSUMPTION: the thread representation of "
                     'the library NPTFF end)'))
    for a, b in reps:
        assert s.count(a) == 1, (root, a[:90]); s = s.replace(a, b)
    t = [s] + list(sp.get('pilot_notes', ()))
    # a female leg's helical thread (P1 from the face) that ends inside a perpendicular bore: legs 1, 2 lie on X, legs 3 (, 4) on Y (PLACE)
    ax = {j: place(sp)[j + 1][0] for j in range(len(legs))}
    rad = [(L['td'] / 2 if L.get('to_centre') else (L.get('conn') or 0) / 2) if L['kind'] == 'NPTFF' else (L.get('bore') or 0) / 2 for L in legs]
    run = {}
    for j, L in enumerate(legs):
        if L['kind'] != 'NPTFF': continue
        end = L['V'][-1][0] - L['P1']; rp = max([rad[q] for q in ax if ax[q] != ax[j]] or [0])
        if rp > end + 1e-9: run.setdefault((L['P1'], round(end, 4), round(rp, 4), round(L['V'][-1][0] - sp['pilot_port'], 4)), []).append(j + 1)
    for (P1, end, rp, pend), js in run.items():
        t.append(f"leg{'s' if len(js) > 1 else ''} {', '.join(map(str, js))}: the helical NPTF thread (MS51503 P1 {P1:.3f} from the face) ends {end:.3f} "
                 f'from the axis crossing, {rp - end:.3f} inside the perpendicular bore (radius {rp:.4f}): it runs out into the cross hole (ASSUMPTION; '
                 'drawing-only thread, suppressed in the saved model and STEP'
                 + ((f"; the pilot's own {sp['pilot_port']:.3f}-deep tapered port ends {pend:.3f} from the crossing, " + (f'{pend - rp:.3f} short of that bore)' if pend > rp else 'inside that bore too)')) if own else ')'))
    return '; '.join(t)


def pilot_rows(root, built):
    """2026-10-02 (new masters wave 1, PIPE-TEES): for a root with a SPEC 'pilot', replace the MODEL part of each built row's
    $PRP@AxialSource by pilot_text(). Called by __main__ right after build_rows(), so build_rows() itself stays as it is (its
    $PRP@AxialSource line is rewritten by another wave-1 patch, FOLDS). The MODEL part must be exactly assume_text() of the row - anything
    else (e.g. a merged patch that changed how build_rows() writes it) stops the generator here instead of leaving a wrong source in the table."""
    for b in built:
        c = b['cols']; s = c['$PRP@AxialSource']; a = ' | MODEL: ' + assume_text(root, b['legs'])
        assert s.endswith(a), (root, b['pn'], 'the MODEL part of $PRP@AxialSource is not assume_text() - pilot_rows() cannot reword it')
        c['$PRP@AxialSource'] = s[:-len(a)] + ' | MODEL: ' + pilot_text(root, b['legs'], b['pn'])


# ---------------------------------------------------------------- table rows
def build_rows(root):
    sp = SPEC[root]; h, rows = load_review(root)
    out, skipped = [], []
    nleg = len(sp['legs'])
    for r in rows:
        pn = r[sp.get('pn', '$PRP@PartNo')] or r['$PRP@PartNo']       # 2026-10-18 (HOSEB): SPEC pn = the column that names the configuration
        if r.get('$PRP@ScopeAction') != 'BUILD' or r['$PRP@DataStatus'] == 'MISSING':
            skipped.append((pn, r.get('$PRP@ScopeAction'), r['$PRP@DataStatus'])); continue
        dd = dashes(pn)
        if sp.get('dmap') and len(dd) == len(sp['dmap']): dd = [dd[k] for k in sp['dmap']]
        chk, warn = [], []
        if len(dd) != nleg: skipped.append((pn, 'dash count', dd)); continue
        # 2026-10-18 (genfeat PERLEGSW): a perleg row with an EMPTY body cell (leg length, bore, body hex, a swivel's nut-face / nose / nut hex
        # column) is skipped with the columns named - never filled here (an empty female NPTF tap drill takes the end library, nptff_td)
        if sp.get('perleg'):
            _need = [sp['hex']] + [c_ for k_, (kind, lc, bc, tc) in enumerate(legs4(sp)) for c_ in
                                   ([lc] + ([bc] if kind != 'NPTFF' else []) + [x_ for x_ in (leg_end(sp, k_) if kind in ('JICSW', 'NPSMSW', 'NWO') else ())
                                                                               if not str(x_).startswith('=')])]
            _miss = [c_ for c_ in dict.fromkeys(_need) if r.get(c_) is None]
            if _miss: skipped.append((pn, 'missing data', 'empty cell(s) ' + ', '.join(_miss) + ' - no value from any allowed source (DataStatus gate)')); continue
        if sp.get('hoseb'):
            # 2026-10-18 (HOSEB): the hose-leg bore source (SPEC hose_bore, Q-HOSEB-BORE) must exist; the adjustable-ORB end-library tokens of the
            # SPEC nwo tuple are filled into a copy of the row (hoseb_endlib)
            _hb = [bc_ for kind_, lc_, bc_, tc_ in legs4(sp) if kind_ == 'HOSEB'][0]
            if sp.get('hose_bore', 'own') is None:
                skipped.append((pn, 'no end data', 'hose bore: no source (Q-HOSEB-BORE)')); continue
            if sp['hose_bore'] == 'col' and r.get(_hb) is None:
                skipped.append((pn, 'no end data', f'hose bore: the row has no hose drill {_hb} (Q-HOSEB-BORE: the 4501 / 4503 hose leg = the part\'s own '
                                                   'hose drill, Brennan B1 DRILL, user 2026-10-18 A15)')); continue
            r = hoseb_endlib(sp, r, dd, warn, chk)
        # 2026-10-09 (wave 2, PERLEGSW): the end-data gates check EVERY swivel leg and name the first missing dash (the same text as before
        # for a root with one swivel; a perleg root also names the leg)
        swd = [(k_, d) for k_, ((kind, lc, bc, tc), d) in enumerate(zip(legs4(sp), dd), 1) if kind == 'JICSW' and d not in G.SWIV_MEAS]
        # 2026-10-01: the measured sizes are read from the tables (the fixed texts "-04/-08/-12/-16 only" / "-08 only" were stale since batch 13)
        _have = lambda tab: '/'.join(f'-{k:02d}' for k in sorted(tab))
        _onleg = lambda k_: f' on leg {k_}' if sp.get('perleg') else ''
        if swd:
            skipped.append((pn, 'no end data', f'female JIC swivel end not measured for -{swd[0][1]:02d}{_onleg(swd[0][0])} (SWIV_MEAS has {_have(G.SWIV_MEAS)}; needs a Brennan STEP carrying a -{swd[0][1]:02d} JIC swivel)')); continue
        npd = [(k_, d) for k_, ((kind, lc, bc, tc), d) in enumerate(zip(legs4(sp), dd), 1) if kind == 'NPSMSW' and d not in G.NPSM_MEAS]
        if npd:
            skipped.append((pn, 'no end data', f'female NPSM swivel end not measured for -{npd[0][1]:02d}{_onleg(npd[0][0])} (NPSM_MEAS has {_have(G.NPSM_MEAS)})')); continue
        nwd = [d for (kind, lc, bc, tc), d in zip(legs4(sp), dd) if kind == 'NWO' and d not in NWO_MEAS]
        if nwd:
            skipped.append((pn, 'no end data', f'adjustable ORB end not measured for -{nwd[0]:02d}')); continue
        # SIZE-40 (2026-10-01): a leg dash missing from an end library (e.g. -40 NPTF) -> skip the row with the source that would fill it
        # (until now an uncaught KeyError here stopped the whole root)
        gaps = G.lib_gaps([(kind, d) for (kind, lc, bc, tc), d in zip(legs4(sp), dd)])
        if gaps:
            skipped.append((pn, 'no end data', '; '.join(gaps))); continue
        if any(kind in FLG_KINDS for (kind, lc, bc, tc) in legs4(sp)):
            # 2026-10-18 (flange leg): a flange size without end data, or a row with an empty leg / hex / bore cell -> skipped with the reason
            try:
                for (kind, lc, bc, tc), d in zip(legs4(sp), dd):
                    if kind in FLG_KINDS: flg_o(kind, d)
            except KeyError as ex:
                skipped.append((pn, 'no end data', str(ex).strip('"\''))); continue
            miss_ = [c_ for (kind, lc, bc, tc) in legs4(sp) for c_ in (lc, bc, tc) if c_ and r.get(c_) is None] + ([sp['hex']] if r.get(sp['hex']) is None else [])
            if miss_:
                skipped.append((pn, 'row without ' + ' / '.join(miss_), 'needs the cell(s) before the row can build')); continue
        # the leg threads must be the ones the part number says
        for (kind, lc, bc, tc), d in zip(legs4(sp), dd):
            if tc is None: continue
            tm = r[tc]
            want = G.JIC[d]['TM'] if kind in ('JICM', 'JICBH', 'JICSW', 'NWO') else G.NPTF[d][2]
            if tm is None and sp.get('perleg'):      # 2026-10-09 (PERLEGSW): an empty cell takes the library major (a filled one must match)
                warn.append(f'{tc} empty: thread major {want} = the -{d:02d} end library (Q-TRANSFER-ENDLIB)'); continue
            if tm is None or abs(tm - want) > 1e-3: chk.append(f'{tc} {tm} does not match the -{d:02d} end ({want})')
        # 2026-10-21 (6810 hex): a row with an empty hex cell (SPEC hex) is skipped with the column named - it stopped the whole root
        # (6810-12-12-NWO-FG, promoted to ASSUMED without its forged hex Y)
        if r.get(sp['hex']) is None:
            skipped.append((pn, 'row without ' + sp['hex'], 'needs the cell before the row can build')); continue
        Y = r[sp['hex']]
        # 2603HX rule: A/F = max(Air-Way hex, JIC thread majors) - the JIC nipple keeps its relief below the flats
        maxes = [G.JIC[d]['TM'] for (kind, lc, bc, tc), d in zip(legs4(sp), dd) if kind in ('JICM', 'JICBH')]
        AF = max([Y] + maxes); BR = AF / 2
        if AF > Y + 1e-9: warn.append(f'hex A/F raised from Air-Way {Y} to {AF:.4f} (JIC thread major; 2603HX rule)')
        # male NPTF: the thread cylinder at its vanish point (radius rL) must sit inside the hex flats with a real shoulder
        for i, ((kind, lc, bc, tc), d) in enumerate(zip(legs4(sp), dd), 1):
            if kind == 'NPTFM':
                nps, tpi, D, E0, E1, L1, L2 = G.NPTF[d]; P = 1 / tpi
                rL = (E0 + 0.8 * P) / 2 + L2 * math.tan(TAPER)
                # Brennan 5600-16-16-16-FG STEP: the round male end (relief dia 1.315) stands 0.001 proud of the hex flats
                # (A/F 1.3125) and the hex stops at N - 0.94 (= the 5404 end length). So a male end at or above the flats is
                # real forged geometry; only a zero-height shoulder (degenerate sketch line) is refused.
                if abs(BR - rL) < 0.0003:
                    chk.append(f'leg {i}: male NPTF thread dia at L2 ({2*rL:.4f}) equals the hex flats ({2*BR:.4f}) - zero-height shoulder')
                elif BR - rL < 0.005:
                    warn.append(f'leg {i}: male NPTF thread dia at L2 {2*rL:.4f} vs hex flats {2*BR:.4f} (round end {"proud of" if rL > BR else "flush with"} the flats by {abs(rL-BR):.4f}; Brennan 5600-16-16-16-FG also has its round end proud of the flats, by 0.0012)')
        conn = r[sp['conn']] if sp.get('conn') else None
        legs = []
        for i, ((kind, lc, bc, tc), d) in enumerate(zip(legs4(sp), dd), 1):
            M = r[lc]
            if kind == 'JICM': L = leg_JICM(i, d, M, BR)
            elif kind == 'JICBH':
                try: L = leg_JICBH(i, d, M, BR, r[sp['bh'][0]], r[sp['bh'][1]], r[sp['bh'][2]])
                except AssertionError as ex: chk.append(f'leg {i} bulkhead: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind == 'NPTFM': L = leg_NPTFM(i, d, M, BR)
            elif kind == 'JICSW':
                # 2026-10-09 (PERLEGSW): each swivel leg reads its own end columns (leg_end) - table columns or end-library tokens (end_val)
                try: e_ = leg_end(sp, i - 1); L = leg_JICSW(i, d, M, BR, end_val(r, e_[0], d, i, warn), end_val(r, e_[1], d, i, warn))
                except AssertionError as ex: chk.append(f'leg {i} swivel: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind == 'NPSMSW':
                try: e_ = leg_end(sp, i - 1); L = leg_NPSMSW(i, d, M, BR, end_val(r, e_[0], d, i, warn), end_val(r, e_[1], d, i, warn))
                except (AssertionError, KeyError) as ex: chk.append(f'leg {i} NPSM swivel: {ex}'); L = leg_NPTFM(i, d, M, BR)
            elif kind == 'NWO':
                try:
                    # merge 2026-10-18: PERLEGSW per-leg end tuple (leg_end / end_val: I3 '=6801' same value and warning text as before, nut hex,
                    # thread length, undercut dia - table columns or end-library tokens) + ANGLED (6810 / 6902): a thread length / groove dia token
                    # '=<series>' (not an end-library token) = the Air-Way rows of the same ORB size in that series (nwo_col_from)
                    e_ = leg_end(sp, i - 1)
                    I3 = end_val(r, e_[0], d, i, warn)
                    nut_ = end_val(r, e_[1], d, i, warn)
                    i3c, thc_, gvc_ = e_[0], e_[2], e_[3]
                    _ser = lambda c_: isinstance(c_, str) and c_.startswith('=') and c_ not in ENDLIB_TOKENS
                    if _ser(thc_) or _ser(gvc_):
                        # 2026-10-18 (ANGLED, 6810 / 6902): thread length / groove dia not printed for this series -> the Air-Way rows of the same
                        # ORB size in the source series (Q-TRANSFER-ENDLIB = yes 2026-10-08); I3 keeps its Brennan check above
                        THDL_ = nwo_col_from(thc_[1:], 'ORB_THDL@DRIVE', d) if _ser(thc_) else end_val(r, thc_, d, i, warn)
                        GRVD_ = nwo_col_from(gvc_[1:], 'ORB_GRVDIA@DRIVE', d) if _ser(gvc_) else end_val(r, gvc_, d, i, warn)
                        if _ser(thc_):
                            warn.append(f'leg {i}: adjustable ORB thread length {THDL_} = Air-Way {thc_[1:]} ORB_THDL for -{d:02d} (not printed for this series; '
                                        f'Q-TRANSFER-ENDLIB 2026-10-08)' + (f' - Brennan 6801 STEP {NWO_MEAS[d]["THDL_B"]}' if abs(THDL_ - NWO_MEAS[d]['THDL_B']) > 0.006 else ''))
                        if _ser(gvc_):
                            warn.append(f'leg {i}: adjustable ORB groove dia {GRVD_} = Air-Way {gvc_[1:]} ORB_GRVDIA for -{d:02d} (not printed for this series; Q-TRANSFER-ENDLIB 2026-10-08)')
                        L = leg_NWO(i, d, M, BR, I3, nut_, THDL_, GRVD_)
                        L['nwo_src'] = (i3c, thc_ if _ser(thc_) else '', gvc_ if _ser(gvc_) else '', I3, THDL_, GRVD_)
                    else:
                        L = leg_NWO(i, d, M, BR, I3, nut_, end_val(r, thc_, d, i, warn), end_val(r, gvc_, d, i, warn))
                except (AssertionError, KeyError, TypeError) as ex: chk.append(f'leg {i} adjustable ORB: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind == 'HOSEB':
                try: L = leg_HOSEB(i, d, M, BR, G.frac(r[sp['hoseb'][0]]), r[sp['hoseb'][1]])
                except (AssertionError, KeyError, TypeError, ValueError) as ex: chk.append(f'leg {i} hose barb: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind in FLG_KINDS:
                # 2026-10-18 (flange leg): only on an axis-aligned leg (the flange dims / vertical collinear are not drawn through DimLenU / DimRadU)
                assert place(sp)[i][0] != 'U', f'{root}: flange leg {i} on the angled axis is not supported'
                O_ = flg_o(kind, d)
                try: L = leg_FLG(i, kind, d, M, BR, O_)
                except AssertionError as ex: chk.append(f'leg {i} flange: {ex}'); L = leg_JICM(i, d, M, BR)
                ro_ = r.get(sp['flg_o']) if sp.get('flg_o') else None
                if ro_ is not None and abs(ro_ - O_) > FLG_O_ROUND: chk.append(f'leg {i}: row head OD {sp["flg_o"].split("@")[0]} {ro_} differs from the end library {O_} - conflict, ask the user')
                elif ro_ is not None and abs(ro_ - O_) > 1e-9: warn.append(f'leg {i}: row head OD {ro_} vs end library {O_} - rounding only (built at {O_})')
            elif sp.get('p1'):
                # 2026-10-02: the row's own measured port thread length where it has one, else the MS51503 P1 library value (said in $COMMENT)
                p1_ = r.get(sp['p1'])
                if p1_ is None: warn.append(f'leg {i}: female port thread length = MS51503 P1 {G.FPT[d]["P1"]} (library) - the row has no measured {sp["p1"]}')
                L = leg_NPTFF(i, d, M, BR, nptff_td(r, bc, d, i, sp, warn), conn, split=bool(sp.get('elbow')), p1=p1_)
            else: L = leg_NPTFF(i, d, M, BR, nptff_td(r, bc, d, i, sp, warn), conn, split=bool(sp.get('elbow')))
            L['bore'] = r[bc] if kind != 'NPTFF' else None
            if kind == 'NPTFF' and sp.get('perleg') and r[bc] is None: L['td_lib'] = True      # 2026-10-09 (PERLEGSW): tap drill from the end library
            if kind == 'HOSEB' and L['kind'] == 'HOSEB':
                # 2026-10-18 (HOSEB): the hose-leg bore (Q-HOSEB-BORE, user 2026-10-18 A15); hose_dh = per-row fallback of an 'own' root
                hb_, bcn_ = sp.get('hose_bore', 'own'), bc
                if hb_ == 'own' and sp.get('hose_dh') and r.get(sp['hose_dh']) is not None:
                    hb_, bcn_ = 'col', sp['hose_dh']; L['bore'] = r[bcn_]
                L['hbsrc'] = (hb_, bcn_)
                if hb_ == 'own':
                    warn.append(f"leg {i}: hose-leg bore {L['bore']} = the row's single bore {bc.split('@')[0]} (the adjustable-ORB end drill) carried through "
                                'the hose leg (Q-HOSEB-BORE option (a), user 2026-10-18 A15)')
                elif hb_ == 'col':
                    warn.append(f"leg {i}: hose-leg bore {L['bore']} = the row's own hose drill {bcn_.split('@')[0]} (Brennan B1 DRILL; Q-HOSEB-BORE, user 2026-10-18 "
                                "A15 'look at Brennan')" + (f"; the adjustable-ORB leg keeps the row's {bc.split('@')[0]} {r[bc]}" if bcn_ != bc else ''))
                else:
                    try: L['bore'] = hose_bore_lib(d); warn.append(f'leg {i}: hose-leg bore {L["bore"]} = Air-Way 4404-{d:02d}-{d:02d} through bore (hose end library, Q-HOSEB-BORE option (b))')
                    except KeyError as ex: chk.append(f'leg {i} hose bore: {ex}')
            legs.append(L)
        AC = BR / COS30
        # geometry checks
        for i, L in enumerate(legs, 1):
            L['hexl'] = round(L['V'][2][0], 4)
            if bh_arm_short(root, sp, L, BR, AC):
                # 2026-10-02 (BH_ARM_SHORT): end the bulkhead hex arm 0.001 before the collar face (the leg profile V is unchanged)
                f_ = f'HEX{i}' if sp.get('elbow') else 'RUN' if i <= 2 else 'RUN2' if sp.get('cross') else 'HEX3'
                a0_ = L['hexl']; L['hexl'] = round(a0_ - BH_ARM_SHORT, 4)
                L['arm_short'] = dict(feat=f_, a0=a0_, a1=L['hexl'], rO=L['V'][3][1], seen=BH_ARM_SHORT_SEEN[root][L['dash']])
                warn.append(f'leg {i}: BULKHEAD HEX ARM ENDED {BH_ARM_SHORT} SHORT of the collar face ({f_}_BODY {bh_len(a0_)} -> {bh_len(L["hexl"])}): '
                            f'ending on the collar face, {f_}_BODY did not rebuild in SolidWorks at this size ({L["arm_short"]["seen"]}); the collar '
                            f'radius {L["V"][3][1]:.4f} lies between the hex flats {BR:.4f} and corners {AC:.4f}, but that crossing builds on other '
                            f'sizes, so it is not the whole cause (BH_ARM_SHORT, user decision 2026-10-02)')
            if L['kind'] == 'NPTFF':
                # 2026-09-24: round collar at the female port, dia = the hex flats, length 0.260 MEASURED on every Brennan forged female pipe
                # port we have - 2502-06-04-FG, 5502-04-04-FG, 5502-08-08-FG, 5502-16-16-FG, 5504-08-08-FG (both legs), 5605-08-08-08-FG
                # (all 3 legs): the same 0.26 at -04, -08 and -16 (NOT proportional to the leg); kept clear of the corner puck by 0.03
                Mf = L['V'][2][0]; CL = round(min(COLLAR_L, Mf - AC - 0.03), 3)
                L['collar'] = CL; L['hexl'] = round(Mf - CL, 4)
            if L['kind'] in FLG_KINDS:
                c_, w_ = flg_leg_checks(i, L, BR, AC); chk += c_; warn += w_; continue       # 2026-10-18: the flange leg's own gates and wording
            if L['kind'] != 'NPTFF':
                if L['hexl'] < 0.03: chk.append(f'leg {i}: end length {L["endlen"]:.3f} leaves no hex ({L["hexl"]:.3f})')
                if L['bore'] is None: chk.append(f'leg {i}: no bore')
                elif L['bore'] / 2 >= L['tipR'] - 0.002: chk.append(f'leg {i}: bore {L["bore"]} >= tip dia {2*L["tipR"]:.3f}')
            else:
                if L['td'] / 2 >= BR - 0.03: chk.append(f'leg {i}: tap drill {L["td"]} leaves < 0.03 wall in hex {AF}')
                if L['P1'] >= L['V'][2][0] - 0.05: chk.append(f'leg {i}: port depth P1 {L["P1"]} >= leg length {L["V"][2][0]}')
            if L['kind'] in ('JICSW', 'NPSMSW') and (sp.get('e45') or sp.get('elbow')) and L['hexl'] < AC + 0.002:
                # 2026-09-24: Brennan's own 45 deg swivel forgings do this too (6502-08-08-FG: body face 0.395, corner radius 0.433;
                # 1503-08-08-FG: 0.40 / 0.505). The puck part beyond the body face is harmless when it stays inside the neck (it adds no
                # material outside the swivel) and ends before the swivel slot: at the body face the puck circle reaches
                # q = sqrt(AC^2 - hexl^2) off the axis (less off the Z=0 plane), and it ends at AC along the axis.
                m_ = L['m']; slot_a = L['Mtip'] - (m_['FLOOR'] if L['kind'] == 'JICSW' else m_['CBEND'])
                q_ = math.sqrt(max(0.0, AC * AC - L['hexl'] ** 2))
                if neck_trim_leg(sp, i, L):
                    # 2026-10-01 (NECK-6502): this leg carries the NECKTRIM / NECKFILL turn - whatever of the corner (puck and the start
                    # corner of the angled hex arm) stands out of the neck between the body face and the nut rear face is cut away, as on
                    # the Brennan 6502-12-12-FG STEP. Still required: past the nut rear face the corner stays inside the nut (it is hidden
                    # there) and short of the swivel slot.
                    oth_ = [o for o in legs if o is not L][0]
                    hexl2_ = round(oth_['V'][2][0], 4); a_nr_ = round(L['V'][4][0], 4)
                    reach_ = corner_reach(L['hexl'], AC, BR, hexl2_); reach_n_ = corner_reach(a_nr_, AC, BR, hexl2_)
                    arm_ = SQ2 / 2 * AC > L['hexl']
                    # 2026-10-18 (ANGLED, N2; SPEC neck_turn only): the puck reaches the slot start on its axis only (point (AC, 0, 0)); what
                    # matters is how far off the axis the corner stands from the slot start on - inside the stem / nose it is hidden in solid
                    sr_ = slot_reach_check(L, AC, BR, hexl2_, slot_a) if sp.get('neck_turn') else None
                    if sp.get('neck_turn') and sr_ is not None and sr_[0] < 0.02:
                        chk.append(f'leg {i}: past the swivel slot start ({slot_a:.3f}) the corner stands {sr_[2]:.4f} off the axis at {sr_[1]:.4f}, '
                                   f'outside the {"stem" if L["kind"] == "NPSMSW" else "nose"} ({sr_[3]:.4f}) - margin {sr_[0]:.4f} < 0.02')
                    elif sp.get('neck_turn') and sr_ is not None:
                        warn.append(f'leg {i}: the corner (radius {AC:.3f}) reaches past the swivel slot start ({slot_a:.3f}) but stays inside the '
                                    f'{"stem" if L["kind"] == "NPSMSW" else "nose"} there (worst margin {sr_[0]:.4f} at {sr_[1]:.4f}: corner {sr_[2]:.4f} off the '
                                    f'axis vs {sr_[3]:.4f}) - hidden in solid (slot test N2, 2026-10-18)')
                    if sp.get('neck_turn') and sr_ is not None and sr_[0] < 0.02:
                        pass
                    elif AC > slot_a - 0.02 and not sp.get('neck_turn'):
                        chk.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches into the swivel slot (starts {slot_a:.3f})')
                    elif reach_n_ > m_['SKR'] - 0.02:
                        chk.append(f'leg {i}: past the swivel nut rear face ({a_nr_:.3f}) the corner stands {reach_n_:.3f} off the axis, not inside the nut (skirt radius {m_["SKR"]:.3f})')
                    elif reach_ <= m_['NECKR']:
                        warn.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches {AC - L["hexl"]:.3f} past the swivel body face ({L["hexl"]:.3f}) but stays '
                                    f'inside the neck (max {reach_:.3f} off the axis vs neck radius {m_["NECKR"]:.3f}) - as on the Brennan 6502-08-08-FG / 1503-08-08-FG forgings')
                    else:
                        warn.append(f'leg {i}: the corner (puck radius {AC:.3f}{"; the angled hex arm starts at " + format(SQ2 / 2 * AC, ".3f") + " along this leg" if arm_ else ""}) '
                                    f'stands {reach_ - m_["NECKR"]:.3f} out of the neck past the swivel body face ({L["hexl"]:.3f}; {reach_:.3f} off the axis vs neck radius '
                                    f'{m_["NECKR"]:.3f}) - turned down to the neck from the body face to the nut rear face ({a_nr_:.3f}) by NECKTRIM{i} / NECKFILL{i}, '
                                    f'as on the Brennan 6502-12-12-FG STEP (NECK-6502, 2026-10-01)')
                elif q_ <= m_['NECKR'] - 0.02 and AC <= slot_a - 0.02:
                    warn.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches {AC - L["hexl"]:.3f} past the swivel body face ({L["hexl"]:.3f}) but stays '
                                f'inside the neck (max {q_:.3f} off the axis vs neck radius {m_["NECKR"]:.3f}) - as on the Brennan 6502-08-08-FG / 1503-08-08-FG forgings')
                else:
                    chk.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches past the swivel body face ({L["hexl"]:.3f}) outside the neck '
                               f'({q_:.3f} off the axis vs neck radius {m_["NECKR"]:.3f}) or into the swivel slot (starts {slot_a:.3f})')
            if sp.get('e45'):
                # Brennan 2504-08-08-FG: hex shoulders at 0.323 from the centre, inside the puck (radius 0.433) - normal for
                # a 45 deg forging. Only the thread must stay clear of the puck.
                if L['kind'] in ('JICM', 'NPTFM', 'JICBH'):
                    ta, tr = L['V'][5] if L['kind'] == 'JICM' else L['V'][7] if L['kind'] == 'JICBH' else L['V'][4]      # inner end of the thread zone
                    m = puck_margin(ta, tr, AC, BR)
                    if m < 0: chk.append(f'leg {i}: the corner puck buries the inner thread edge (margin {m:.4f})')
                    elif m < 0.01: warn.append(f'leg {i}: inner thread edge clears the corner puck by only {m:.4f}')
            elif sp.get('elbow'):
                if sp.get('arm_ridge_check') and L['hexl'] < AC:        # 2026-10-02 (1502): an arm ending inside the corner radius does not clear it
                    warn.append(f'leg {i} hex arm {L["hexl"]:.3f} ends {AC - L["hexl"]:.3f} INSIDE the hex corner radius ({AC:.3f})')
                elif L['hexl'] < AC + 0.03 and L['kind'] != 'HOSEB':       # (HOSEB: the face-off below says what happens at the hose hex face)
                    warn.append(f'leg {i} hex arm {L["hexl"]:.3f} barely clears the corner puck (radius {AC:.3f})')
            elif i >= 3 and L['hexl'] < AC + 0.03 and not sp.get('cross'):
                warn.append(f'leg {i} hex arm {L["hexl"]:.3f} barely clears the run bar corner ({AC:.3f})')
        # 2026-10-02 (1502, review of the new master): on a 90 deg elbow the OTHER leg's hex arm (flats normal to Z) has its corner at z = 0,
        # at AC from its own axis over its whole length - i.e. at AC along the swivel axis. When the swivel body face lies inside AC
        # (hexl < AC), that arm stands AC - hexl beyond the body face, as a ridge |z| <= (AC - hexl) / tan30, OUTSIDE the neck wherever the
        # arm runs farther from the swivel axis than the neck radius. The puck check above sees only the 30deg corner, not this ridge.
        # Brennan 6500-05-05-FG STEP (90 deg forged swivel elbow; swivel body face 0.314 inside the hex corner radius 0.3245): the male arm's
        # corner is faced off at the body face - nothing outside the neck from the body face on (section y = 0.319: only the neck and the
        # bore). The 90 deg elbow has no such facing cut (NECKTRIM / NECKFILL serve the +X swivel leg of a 45 deg elbow only), so such a
        # row is BLOCKED. Opt-in per root (SPEC arm_ridge_check): 6500 carries the same ridge on its built 6500-05-05-FG (0.009) - not
        # switched on there (it would block a shipped configuration); left to the main session.
        if sp.get('arm_ridge_check') and sp.get('elbow') and not sp.get('e45'):
            for i, L in enumerate(legs, 1):
                # 2026-10-09 (PERLEGSW, DESIGN_REVIEW P4): a perleg root checks its adjustable ORB legs too (neck = NWO_MEAS NECKR)
                if L['kind'] not in (('JICSW', 'NPSMSW', 'NWO') if sp.get('perleg') else ('JICSW', 'NPSMSW')): continue
                oth_ = [o for o in legs if o is not L][0]; nr_ = L['m']['NECKR']; h_ = AC - L['hexl']
                if h_ > ARM_RIDGE_EPS and oth_['hexl'] > nr_:
                    chk.append(f'leg {i}: the other leg\'s hex arm corner (hex corner radius {AC:.4f}) stands {h_:.4f} beyond the {"adjustable ORB" if L["kind"] == "NWO" else "swivel"} body face '
                               f'({L["hexl"]:.4f}) OUTSIDE the neck (radius {nr_:.4f}), from the neck out to the arm end {oth_["hexl"]:.3f} along the other '
                               f'leg (ridge {2 * h_ / TAN30:.4f} wide) - Brennan faces it off at the body face (6500-05-05-FG STEP: body face 0.314 inside '
                               f'the corner radius 0.3245, nothing outside the neck beyond it); the 90 deg elbow has no facing cut')
        # 2026-10-18 (genfeat PERLEGSW): the row's nut face -> stem tip (NPSM) / nut face -> nose tip (JIC swivel) is followed; on a perleg
        # root it is compared with the Brennan value of the library end (NPSM_MEAS TIP_B, SWIV_MEAS NOSETIP_B) and a difference is said
        if sp.get('perleg'):
            for i, L in enumerate(legs, 1):
                if L['kind'] not in ('JICSW', 'NPSMSW'): continue
                k_, w_ = ('TIP_B', 'stem tip') if L['kind'] == 'NPSMSW' else ('NOSETIP_B', 'nose tip')
                if abs(L['s_nt'] - L['m'][k_]) > 0.005:
                    warn.append(f'leg {i}: nut face to {w_} {L["s_nt"]:.3f} (row) vs {L["m"][k_]:.3f} on the Brennan -{L["dash"]:02d} swivel ({k_}) - the row is followed')
        # 2026-10-09 (wave 2, PERLEGSW, DESIGN 4.4 c): the same ridge on a TEE. A run special leg (+/-X) whose body face lies inside the hex
        # corner radius sees the branch hex arm HEX3 (corners at x = +/-AC) stand AC - hexl beyond it, outside the neck wherever the arm runs
        # farther from the run axis than the neck (hexl3 > NECKR). A branch special leg (+Y) sees the run bar's corners (y = +/-AC) the same
        # way. The run-side rule follows the Brennan 6500-05-05-FG evidence (90 deg elbow); the BRANCH-side rule is CONSERVATIVE, UNCONFIRMED
        # (no tee -05 forging seen; DESIGN_REVIEW P3). Opt-in: perleg roots only (the shipped 6602-05 / 6600-05 carry such a ridge - main session).
        if sp.get('perleg') and sp.get('arm_ridge_check') and not sp.get('elbow') and not sp.get('cross'):
            for i, L in enumerate(legs, 1):
                if L['kind'] not in ('JICSW', 'NPSMSW', 'NWO'): continue
                nr_ = L['m']['NECKR']; h_ = AC - L['hexl']
                if h_ <= ARM_RIDGE_EPS: continue
                if i <= 2 and legs[2]['hexl'] > nr_:
                    chk.append(f'leg {i}: the branch hex arm corner (hex corner radius {AC:.4f}) stands {h_:.4f} beyond the run body face ({L["hexl"]:.4f}) '
                               f'OUTSIDE the neck (radius {nr_:.4f}), from the neck out to the branch arm end {legs[2]["hexl"]:.3f} (ridge {2 * h_ / TAN30:.4f} wide) '
                               '- Brennan faces such a corner off at the body face (6500-05-05-FG STEP); the tee has no facing cut')
                elif i == 3 and max(legs[0]['hexl'], legs[1]['hexl']) > nr_:
                    chk.append(f'leg {i}: the run bar corner (hex corner radius {AC:.4f}) stands {h_:.4f} beyond the branch body face ({L["hexl"]:.4f}) '
                               f'OUTSIDE the neck (radius {nr_:.4f}), along the run bar to {max(legs[0]["hexl"], legs[1]["hexl"]):.3f} (ridge {2 * h_ / TAN30:.4f} wide) '
                               '- CONSERVATIVE rule, unconfirmed (no tee -05 forging seen); the tee has no facing cut')
        # 2026-10-09 (wave 2, PERLEGSW, DESIGN 4.4 a / b): every nut cut removes everything outside its hexagon over its slab, so every
        # perpendicular leg's FINAL reach (swivel nut corners / skirt, adjustable-ORB washer / nut corners, else rmax) and the body hex corner
        # must stay NUTSLAB_MIN short of the slab start (a same-axis opposite leg cannot reach it). Two adjustable ORB legs: the revolved locknut
        # ENVELOPE (NWO_RN_MARGIN beyond the final corners) of the later leg may reach into the earlier leg's slab - the final solid is the same,
        # but the earlier NUTCUT removes that sliver (nwo_overlap) and the later one that much less: warned here, bounded in emit().
        if sp.get('perleg'):
            for i, L in enumerate(legs, 1):
                sl_ = nut_slab(L)
                if not sl_: continue
                ax_ = place(sp)[i][0]
                for j, o in enumerate(legs, 1):
                    if o is L or place(sp)[j][0] == ax_: continue
                    rch_ = max(final_reach(o), AC)
                    if sl_[0] < rch_ + NUTSLAB_MIN:
                        chk.append(f'leg {i}: nut cut slab starts {sl_[0]:.4f} from the crossing, inside the final reach {rch_:.4f} of leg {j} / the body hex corner '
                                   f'(+{NUTSLAB_MIN} needed): the nut cut would shave that leg')
                    elif L['kind'] == 'NWO' and o['kind'] == 'NWO' and j > i:
                        ov_ = nwo_overlap(L, o)
                        if ov_ > 0:
                            L.setdefault('nut_overlap', {})[j] = ov_
                            warn.append(f'leg {j}: its revolved locknut envelope (radius {o["nut"]["Rn"]:.4f}, {NWO_RN_MARGIN} beyond the nut corners) reaches past '
                                        f'leg {i}\'s locknut slab start {sl_[0]:.4f}: NUTCUT{i} removes {ov_:.6f} in^3 of it ({100 * ov_ / nwo_nut_removed(o["nut"]):.2f} % '
                                        f'of NUTCUT{j}); the finished solid is unchanged')
            for i, L in enumerate(legs, 1):
                if L['kind'] == 'NWO' and BR - L['m']['NECKR'] < 0.01:
                    warn.append(f'leg {i}: the adjustable ORB body face is a {BR - L["m"]["NECKR"]:.4f} step (hex flats radius {BR:.4f} vs neck radius {L["m"]["NECKR"]:.4f})')
        # 2026-10-09 (wave 2, HOSEB, DESIGN 4.5 / 4.6): the hose stub (wall, hex-face step, bead clear of the face-off) and the FACE-OFF of the forged
        # corner at the hose hex face - in EVERY configuration (HOSEFACEi cut + STUBFILLi refill; net 0 where the corner clears the face)
        for i, L in enumerate(legs, 1):
            if L['kind'] != 'HOSEB': continue
            assert sp.get('elbow') and (place(sp)[i] == ('U', 1) if sp.get('e45') else place(sp)[i] == (0, 1)), 'hose leg: +X on a 90 deg elbow, 135 deg on a 45 deg elbow'
            b0_ = L['bead'][0]; sh_ = L['hexl']; rS_ = L['rS']; e45_ = bool(sp.get('e45'))
            if L['bore'] is not None:
                wl_ = rS_ - L['bore'] / 2
                if wl_ < HOSE_WALL_MIN - 1e-9: chk.append(f'leg {i}: hose stub wall {wl_:.4f} (stub OD {2 * rS_:.3f}, bore {L["bore"]}) < {HOSE_WALL_MIN}')
                elif wl_ < 0.03: warn.append(f'leg {i}: thin hose stub wall {wl_:.4f} (stub OD {2 * rS_:.3f}, bore {L["bore"]}; the 4404-04-04 master has 0.020)')
            if rS_ > BR - 0.01: chk.append(f'leg {i}: hose stub radius {rS_:.4f} not below the hex flats radius {BR:.4f} - 0.01 (no hex face step)')
            if chk or L['bore'] is None: continue
            fo_ = faceoff_geo(sp, legs, i - 1, BR, AC); O_ = legs[2 - i]
            fo_.update(rect=not e45_, sh=sh_, depth=round(max(AC - sh_, 0.0) + FACEOFF_DELTA, 4), rin=round((L['bore'] / 2 + rS_) / 2, 5), rS=rS_)
            cend_ = round(sh_ + fo_['depth'], 4)
            if b0_ < cend_ + FACEOFF_GAP: chk.append(f'leg {i}: hose bead starts {b0_:.4f} from the crossing, within {FACEOFF_GAP} of the face-off end {cend_:.4f}')
            if not (L['bore'] / 2 + 0.005 <= fo_['rin'] <= rS_ - 0.005): chk.append(f'leg {i}: face-off inner radius {fo_["rin"]} not between the bore and the stub radius')
            if e45_:
                fo_['rout'] = round(FACEOFF_ROUT_K * AC, 4)
                if fo_['past'] and fo_['past_max_r'] > fo_['rout'] - FACEOFF_GAP:
                    chk.append(f'leg {i}: the forged corner past the hose hex face reaches {fo_["past_max_r"]:.4f} off the hose axis, beyond the face-off ring {fo_["rout"]}')
                if fo_.get('end_min_r', 1e9) < fo_['rout'] + FACEOFF_GAP:
                    chk.append(f'leg {i}: the other leg\'s end lies {fo_["end_min_r"]:.4f} off the hose axis inside the face-off slab - the ring {fo_["rout"]} would cut it')
            else:
                fo_['ylo'] = round(AC + FACEOFF_DELTA, 4); fo_['zh'] = round(BR + FACEOFF_DELTA, 5)
                fo_['ytop'] = round(min(O_['hexl'], fo_.get('end_min_along_other', 1e9)), 4)
                if fo_['ytop'] < rS_ + 0.01: chk.append(f'leg {i}: face-off rectangle ends {fo_["ytop"]:.4f} along the other leg, inside the stub radius {rS_:.4f} + 0.01')
                if fo_['past'] and fo_['past_max_along_other'] > fo_['ytop'] + 1e-6:
                    chk.append(f'leg {i}: the forged corner past the hose hex face reaches {fo_["past_max_along_other"]:.4f} along the other leg, beyond the face-off rectangle ({fo_["ytop"]:.4f})')
            L['faceoff'] = fo_
            if fo_['past']:
                warn.append(f'leg {i}: hose hex arm {sh_:.3f} ends {AC - sh_:.3f} inside the forged corner radius ({AC:.3f}): the corner past the hose hex face '
                            f'({", ".join(fo_["past_by"])}, up to {fo_["past_max_r"]:.3f} off the hose axis, {fo_["past_max_a"] - sh_:.3f} deep) is faced off to the '
                            f'stub (HOSEFACE{i} / STUBFILL{i}, depth {fo_["depth"]:.4f}' + (', as the Brennan 4503-08-08-FG / 4603-16-16-NWO-FG forgings show)' if e45_ else ')'))
        # 2026-10-01 (NECK-6502): the neck turn of a swivel leg on a 45 deg elbow - in EVERY configuration of the root (the master carries
        # the two features in all of them), whether or not the corner reaches out of the neck in this one
        for i, L in enumerate(legs, 1):
            if not neck_trim_leg(sp, i, L): continue
            nr_ = L['m']['NECKR']; a0_ = round(L['V'][3][0], 4); a1_ = round(L['V'][4][0], 4)
            assert abs(a0_ - L['hexl']) < 1e-9 and abs(L['V'][3][1] - nr_) < 1e-9 and abs(L['V'][4][1] - nr_) < 1e-9, ('V3..V4 is not the neck line', pn)
            oth_ = [o for o in legs if o is not L][0]
            cav_ = slab_cavity(L['V'], a0_, a1_); lo_ = max(cav_, L['bore'] / 2)          # solid from lo_ out to the neck in that slab
            L['trim'] = dict(a0=a0_, len=round(a1_ - a0_, 4), rin=round((lo_ + nr_) / 2, 5), rout=round(TRIM_ROUT_K * AC, 5), r=nr_,
                             reach=round(corner_reach(a0_, AC, BR, round(oth_['V'][2][0], 4)), 5), cav=round(cav_, 5))
            if L['trim']['len'] < 0.01: chk.append(f'leg {i}: neck length {L["trim"]["len"]:.4f} between the body face and the nut rear face is too short for the neck turn')
            if nr_ - lo_ < 0.02: chk.append(f'leg {i}: neck wall {nr_ - lo_:.3f} in the neck turn (bore / swivel cavity radius {lo_:.3f} vs neck radius {nr_:.3f})')
            # the turn may only take forged-corner material: the other leg beyond its hex arm (radius <= rmax) must stay short of the body face
            if SQ2 / 2 * (oth_['rmax'] - oth_['V'][2][0]) > a0_ - 0.01:
                chk.append(f'leg {i}: the other leg\'s end reaches {SQ2 / 2 * (oth_["rmax"] - oth_["V"][2][0]):.3f} along this leg, into the neck turn (body face {a0_:.3f})')
        # 2026-10-18 (ANGLED): checks that only a leg on the 135 deg axis with a swivel or a female port reaches (no released root has one)
        if sp.get('e45'):
            for i, L in enumerate(legs, 1):
                if place(sp)[i][0] != 'U': continue
                oth_ = [o for o in legs if o is not L][0]
                if L['kind'] in ('JICSW', 'NPSMSW'):
                    # the nut hex is an OUTSIDE cut over [Mtip - HEXL, Mtip] along this leg: nothing else may stand in that slab (the +X leg's farthest
                    # reach along the 135 deg axis = e45_reach by the mirror symmetry of the 45 deg elbow about its bisector)
                    s0_ = L['Mtip'] - L['m']['HEXL']; rch_ = e45_reach(oth_, AC)
                    if rch_ >= s0_ - 0.01: chk.append(f'leg {i}: the other leg / corner reaches {rch_:.3f} along the 135-deg leg, into the swivel nut hex slab (from {s0_:.3f})')
                if L['kind'] == 'NPTFF' and oth_['kind'] in ('JICSW', 'NPSMSW'):
                    # the female port on the 135 deg leg (its tap drill to the crossing, its thread over P1 from the face) must stay short of the +X swivel
                    # slot / nut cavity: a point at a along this leg, radius q reaches (q - a) / sqrt2 along +X
                    fp_ = L['thread']; a_in_ = L['V'][-1][0] - L['P1']; q_t_ = L['td'] / 2 + fp_['thdh']
                    reach_x_ = SQ2 / 2 * max(L['td'] / 2 - (0.0 if L['to_centre'] else L['V'][-1][0] - L['pocket']), q_t_ - a_in_)
                    m_o = oth_['m']; slot_o = oth_['Mtip'] - (m_o['FLOOR'] if oth_['kind'] == 'JICSW' else m_o['CBEND'])
                    if reach_x_ > slot_o - 0.02: chk.append(f'leg {i}: the female port reaches {reach_x_:.3f} along the swivel leg, into its slot (starts {slot_o:.3f})')
        cols = {}
        for L in legs: cols.update(L['cols'])
        # bores / pockets
        for i, L in enumerate(legs, 1):
            if L['kind'] == 'NPTFF':
                cols[f'TAPDRILL{i}@POCKET{i}'] = L['td']; cols[f'DEPTH@POCKETCUT{i}'] = round(L['pocket'], 4)
                if not L['to_centre']: cols[f'D{i}@BORE{i}'] = L['conn']; cols[f'DEPTH@BORECUT{i}'] = L['V'][2][0]
            else:
                cols[f'D{i}@BORE{i}'] = L['bore']; cols[f'DEPTH@BORECUT{i}'] = L.get('Mtip', L['V'][-1][0])
                if L['kind'] == 'NPSMSW':
                    m_ = L['m']; b2 = L['bore'] / 2
                    if m_['NECKR'] - b2 < 0.03: chk.append(f'leg {i}: neck wall {m_["NECKR"] - b2:.3f} (neck dia {2*m_["NECKR"]:.3f}, bore {L["bore"]})')
                    if m_['NECKR'] >= BR - 0.02: chk.append(f'leg {i}: NPSM swivel neck dia {2*m_["NECKR"]:.3f} not below the body hex flats {AF:.4f}')
                    if m_['STEMR'] - b2 < 0.05: chk.append(f'leg {i}: stem wall {m_["STEMR"] - b2:.3f}')
                    if b2 > m_['TIPR'] - 0.03: chk.append(f'leg {i}: bore {L["bore"]} leaves < 0.03 at the stem tip (tip dia {2*m_["TIPR"]:.3f})')
                    if abs(L['s_tip'] - m_['TIP_B']) > 0.02: warn.append(f'leg {i}: Air-Way nut face to stem tip (W - M) {L["s_tip"]:.3f} vs Brennan {m_["TIP_B"]:.3f}: nut placed at Air-Way W (user decision 2026-09-24, as 1404/1405)')
                if L['kind'] == 'NWO':
                    m_ = L['m']; b2 = L['bore'] / 2
                    if min(m_['NECKR'], L['UR']) - b2 < 0.03: chk.append(f'leg {i}: adjustable ORB wall {min(m_["NECKR"], L["UR"]) - b2:.3f} (neck dia {2*m_["NECKR"]:.3f}, undercut dia {2*L["UR"]:.3f}, bore {L["bore"]})')
                    # the locknut is cut to its hexagon over [n0, w0] along its own axis (everything outside the hexagon in that slab goes):
                    # the other legs and the corner must stay short of the slab
                    n0_ = L['nut']['n0']; hexl_ = L['V'][2][0]
                    if sp.get('e45'):
                        # 45 deg elbow (2026-10-01, Q-NEW-6802E45CHECK): the other leg lies on the 135 deg axis and points away from this one - its
                        # thread radius never reaches this leg (was counted, 90-deg rule: blocked 6802-20-16/-20-20/-24-24). Its true reach along this
                        # leg is its hex-arm corner at the crossing, AC*cos45 (e45_reach). The corner puck (radius AC about Z) may reach past the body face.
                        oth = max(e45_reach(o, AC) for o in legs if o is not L)
                        q_ = math.sqrt(AC * AC - hexl_ * hexl_) if hexl_ < AC else None
                        if q_ is not None and q_ <= m_['NECKR'] - 0.02:
                            warn.append(f'leg {i}: the corner puck (radius {AC:.3f}) reaches {AC - hexl_:.3f} past the body face ({hexl_:.3f}) inside the neck (max {q_:.3f} off the axis vs neck radius {m_["NECKR"]:.3f}) - as on the 45 deg Brennan forgings')
                        lens = math.sqrt(max(0.0, AC * AC - n0_ * n0_))
                        if lens > L['nut']['af'] / 2 - 0.01: chk.append(f'leg {i}: the corner puck reaches the locknut face outside the nut flats ({lens:.3f})')
                        # everything of the corner beyond the body face, sampled (e45_foreign): inside the ORB end -> as before; standing out between the
                        # body face and the full nut corner -> corner neck trim (ORBTRIM); near-tangent or standing out farther out -> BLOCKED
                        fz = e45_foreign(L, legs, BR, AC)
                        L['nwo_trim_pts'], L['nwo_trim_vals'] = nwo_trim_geo(L, AC); L['nwo_trim'] = False
                        xT_ = L['nwo_trim_pts'][3][0]
                        bad_ = [f'{pc} stands {e_:+.3f} outside the adjustable ORB end at x={x_:.3f} (r {r_:.3f}), past the full locknut corner ({xT_:.3f}) where no trim reaches'
                                for (pc, zn), (e_, x_, r_) in sorted(fz.items()) if zn == 'beyond' and e_ > -NWO_BEYOND_MIN]
                        tan_ = [f'{pc} {e_:+.3f} at x={x_:.3f}' for (pc, zn), (e_, x_, r_) in sorted(fz.items()) if zn == 'trim' and -NWO_TRIM_MIN < e_ < NWO_TRIM_MIN]
                        out_ = [(pc, e_, x_, r_) for (pc, zn), (e_, x_, r_) in sorted(fz.items()) if zn == 'trim' and e_ >= NWO_TRIM_MIN]
                        for t_ in bad_: chk.append(f'leg {i}: {t_}')
                        if tan_: chk.append(f'leg {i}: corner material within {NWO_TRIM_MIN} of the ORB neck / locknut inner chamfer beyond the body face ({"; ".join(tan_)}) - near-tangent, neither clear nor trimmable')
                        if out_ and not bad_ and not tan_:
                            L['nwo_trim'] = True
                            if max(r_ for _, _, _, r_ in out_) > L['nwo_trim_vals']['RO'] - 0.05: chk.append(f'leg {i}: corner material beyond the trim loop radius {L["nwo_trim_vals"]["RO"]}')
                            warn.append(f'leg {i}: CORNER NECK TRIM (ORBTRIM{i}): beyond the body face ({hexl_:.3f}) the corner stands outside the ORB neck / locknut inner chamfer - '
                                        + ', '.join(f'{pc} by {e_:.3f} (x={x_:.3f}, r {r_:.3f})' for pc, e_, x_, r_ in out_)
                                        + f' - cut back to the ORB profile up to the full nut corner ({xT_:.3f}); the rest of the corner lies inside the ORB end')
                        if n0_ < oth + 0.003 and not bad_ and not tan_:
                            warn.append(f'leg {i}: the angled hex arm corner reaches {oth:.3f} along this leg, past the locknut face ({n0_:.3f}) - '
                                        + ('cut back by the corner neck trim and ' if L['nwo_trim'] else '') + 'inside the locknut envelope beyond (sampled check)')
                    else:
                        oth = max([0.0] + [nwo_radial(o) if o['kind'] == 'NWO' else o['rmax'] for o in legs if o is not L])
                        oth = max(oth, AC)
                        if n0_ < oth + 0.003 and not sp.get('perleg'): chk.append(f'leg {i}: locknut starts {n0_:.3f} from the crossing, inside the reach of the other legs / corner ({oth:.3f})')
                if L['kind'] == 'JICSW':
                    m_ = L['m']
                    if m_['NECKR'] - L['bore'] / 2 < 0.03: chk.append(f'leg {i}: neck wall {m_["NECKR"] - L["bore"] / 2:.3f} (neck dia {2*m_["NECKR"]:.3f}, bore {L["bore"]})')
                    if m_['NECKR'] >= BR - 0.02: chk.append(f'leg {i}: swivel neck dia {2*m_["NECKR"]:.3f} not below the body hex flats {AF:.4f}')
                    if abs(L['s_nt'] - m_['NOSETIP_B']) > 0.02: warn.append(f'leg {i}: Air-Way nut-face-to-seat {L["s_nt"]:.3f} vs Brennan {m_["NOSETIP_B"]:.3f}')
        for L in legs: cols.update(L['tcols'])
        # hex bars
        if sp.get('elbow'):
            R1 = AC - PUCK_INSET - BR * TAN30
            cols['HEXAF@HEX1'] = round(AF, 5); cols['HEXL@HEX1_BODY'] = legs[0]['hexl']
            cols['HEXAF@HEX2'] = round(AF, 5); cols['HEXL@HEX2_BODY'] = legs[1]['hexl']
            cols['PUCK_HB@PUCK'] = round(BR, 5); cols['PUCK_HT@PUCK'] = round(BR, 5)
            cols['PUCK_R1B@PUCK'] = round(R1, 5); cols['PUCK_R1T@PUCK'] = round(R1, 5); cols['PUCK_XC@PUCK'] = round(AC - PUCK_INSET, 5)
            for i, L in enumerate(legs, 1):
                fo_ = L.get('faceoff')
                if not fo_: continue
                # 2026-10-09 (HOSEB): the face-off columns (plane offset, cut region, depth, refill ring) - diameters, as BoreCut dimensions its circles
                cols[f'D1@HFPLN{i}'] = fo_['sh']; cols[f'HF{i}_DIN@HOSEFACE{i}_SK'] = round(2 * fo_['rin'], 5)
                if fo_['rect']:
                    cols[f'HF{i}_ZH@HOSEFACE{i}_SK'] = fo_['zh']; cols[f'HF{i}_YTOP@HOSEFACE{i}_SK'] = fo_['ytop']
                    cols[f'HF{i}_ZH2@HOSEFACE{i}_SK'] = fo_['zh']; cols[f'HF{i}_YLO@HOSEFACE{i}_SK'] = fo_['ylo']
                else: cols[f'HF{i}_DOUT@HOSEFACE{i}_SK'] = round(2 * fo_['rout'], 5)
                cols[f'DEPTH@HOSEFACE{i}'] = fo_['depth']
                cols[f'SF{i}_DIN@STUBFILL{i}_SK'] = round(2 * fo_['rin'], 5); cols[f'SF{i}_DOUT@STUBFILL{i}_SK'] = round(2 * fo_['rS'], 5)
                cols[f'DEPTH@STUBFILL{i}'] = fo_['depth']
            for i, L in enumerate(legs, 1):
                if L.get('trim'):
                    t_ = L['trim']
                    cols[f'TRIM_A0@NECKTRIM{i}'] = t_['a0']; cols[f'TRIM_LEN@NECKTRIM{i}'] = t_['len']
                    cols[f'TRIM_RIN@NECKTRIM{i}'] = t_['rin']; cols[f'TRIM_ROUT@NECKTRIM{i}'] = t_['rout']
                    cols[f'FILL_A0@NECKFILL{i}'] = t_['a0']; cols[f'FILL_LEN@NECKFILL{i}'] = t_['len']
                    cols[f'FILL_RIN@NECKFILL{i}'] = t_['rin']; cols[f'FILL_ROUT@NECKFILL{i}'] = t_['r']
        else:
            cols['HEXAF@RUN'] = round(AF, 5); cols['HEXL1@RUN_BODY'] = legs[0]['hexl']; cols['HEXL2@RUN_BODY'] = legs[1]['hexl']
        if sp.get('elbow'):
            pass
        elif sp.get('cross'):
            cols['HEXAF@RUN2'] = round(AF, 5); cols['HEXL1@RUN2_BODY'] = legs[2]['hexl']; cols['HEXL2@RUN2_BODY'] = legs[3]['hexl']
        else:
            cols['HEXAF@HEX3'] = round(AF, 5); cols['HEXL@HEX3_BODY'] = legs[2]['hexl']
        thr = [L['thr'] + ' JIC bulkhead' if L['kind'] == 'JICBH' else L['thr'] + ' JIC' if L['kind'] == 'JICM' else L['thr'] for L in legs]
        cols['$PRP@PartNo'] = pn; cols['$PRP@Description'] = f"{sp['name']}, " + ' x '.join(thr); cols['$PRP@GeometryRoot'] = root
        for i, t in enumerate(thr, 1): cols[f'$PRP@End{i}_Thread'] = t
        ds_ = r['$PRP@DataStatus']; c0_ = r.get('$COMMENT') or ''
        if any(L['kind'] == 'NPSMSW' for L in legs) and ds_ not in ('ASSUMED', 'MISSING'):
            c0_ = (c0_ + ' | ' if c0_ else '') + f'DataStatus {ds_} -> ASSUMED: the NPSM swivel nut/stem geometry is single-source (Brennan 1404-08-08 STEP)'
            ds_ = 'ASSUMED'
        if any(L['kind'] == 'HOSEB' for L in legs) and ds_ not in ('ASSUMED', 'MISSING', 'TEST'):
            c0_ = (c0_ + ' | ' if c0_ else '') + f'DataStatus {ds_} -> ASSUMED: the hose-barb stub / bead geometry is single-source (Brennan 4404-08-06 STEP)'
            ds_ = 'ASSUMED'
        if any(L['kind'] == 'NWO' for L in legs) and ds_ not in ('ASSUMED', 'MISSING'):
            c0_ = (c0_ + ' | ' if c0_ else '') + f'DataStatus {ds_} -> ASSUMED: the adjustable ORB nut/washer/neck geometry is single-source (Brennan 6801-XX-XX-NWO-FG STEPs)'
            ds_ = 'ASSUMED'
        if any(L['kind'] == 'JICSW' for L in legs):
            BLK_ = 'BLOCKED: female-JIC swivel nut internal geometry UNPUBLISHED (nut thread depth, nose, sleeve seat) - measure a Brennan 6500 STEP'
            if BLK_ in c0_:
                c0_ = c0_.replace(BLK_, 'RESOLVED 2026-09-24 for swivel dashes -04/-08/-12/-16: swivel nut, nose and 37deg seat measured on the Brennan 6500-04/-08/-12/-16-FG STEPs (was BLOCKED: female-JIC swivel nut internal geometry unpublished)')
                c0_ = c0_.replace('internal seat still MISSING', 'internal seat measured 2026-09-24 (Brennan STEPs)')
            if ds_ not in ('ASSUMED', 'MISSING'):
                c0_ = (c0_ + ' | ' if c0_ else '') + f'DataStatus {ds_} -> ASSUMED: the swivel nut/nose geometry is single-source (Brennan STEPs)'
                ds_ = 'ASSUMED'
        if any(L['kind'] in FLG_KINDS for L in legs):
            if ds_ not in ('ASSUMED', 'MISSING', 'TEST'):
                c0_ = (c0_ + ' | ' if c0_ else '') + f'DataStatus {ds_} -> ASSUMED: the flange head geometry is single-source (Brennan STEPs)'
                ds_ = 'ASSUMED'
            warn[:] = [w_.replace('hex A/F raised from Air-Way ', "hex A/F raised from the row's hex ") for w_ in warn]
        model_ = assume_text(root, legs)
        src_ = r.get('_FOLD_SRC') or SPEC[root].get('src')
        if src_:
            # 2026-10-02 (FOLDS): a folded row filled from another source than the base table names that source, not Air-Way, in the
            # generated text (fold note 'src'); generic Air-Way wording left over is a check failure, so a wrong attribution never ships.
            # 2026-10-09 (wave-1 polish): a SPEC may carry the same 'src' pairs for all its rows (2504: every value is OMi's)
            for a_, b_ in src_:
                model_ = model_.replace(a_, b_); warn[:] = [w_.replace(a_, b_) for w_ in warn]; chk[:] = [c_.replace(a_, b_) for c_ in chk]
            left_ = [t_ for t_ in [model_] + warn + chk if 'Air-Way' in t_]
            if left_: chk.append(('folded row' if r.get('_FOLD_SRC') else 'root with its own src pairs')
                                 + ': generic Air-Way source wording not renamed by the src pairs: '
                                 + ' / '.join(t_[max(0, t_.index('Air-Way') - 40):t_.index('Air-Way') + 60] for t_ in left_))
        cols['$PRP@DataStatus'] = 'BLOCKED' if chk else ds_
        cols['$PRP@AxialSource'] = (r.get('$PRP@AxialSource') or '') + ' | MODEL: ' + model_
        for L in legs:      # 2026-10-02 (BH_ARM_SHORT): a modelling assumption of this row only
            s_ = L.get('arm_short')
            if s_: cols['$PRP@AxialSource'] += (f'; bulkhead hex arm (MODELLING ASSUMPTION, user decision 2026-10-02): {s_["feat"]}_BODY did not '
                                                f'rebuild at this size in SolidWorks ({s_["seen"]}); the arm ends {BH_ARM_SHORT} short of the collar '
                                                f'face ({bh_len(s_["a1"])} instead of {bh_len(s_["a0"])}) and rebuilds; the {BH_ARM_SHORT} band shows '
                                                f'the round leg core (not on the real forging)')
        cols['$COMMENT'] = ' | '.join(x_ for x_ in (c0_, ('GEOMETRY CHECK FAILED: ' + '; '.join(chk)) if chk else '', '; '.join(warn)) if x_) or None
        if pn in BRENNAN_NOTES: cols['$COMMENT'] = ' | '.join(x_ for x_ in (cols['$COMMENT'], BRENNAN_NOTES[pn]) if x_)
        cols['$PRP@OMiSKU'] = r.get('$PRP@OMiSKU')
        out.append(dict(cols=cols, legs=legs, AF=AF, BR=BR, AC=AC, chk=chk, warn=warn, pn=pn))
    # 2026-10-01: corner neck trim columns ($STATE + the trim loop) - only for a root where some configuration needs the trim, so every
    # other macro and table stays as released; inserted before the $PRP block
    for i in sorted({i for b in out if not b['chk'] for i, L in enumerate(b['legs'], 1) if L.get('nwo_trim')}):
        for b in out:
            L = b['legs'][i - 1]
            if 'nwo_trim_vals' not in L: continue          # a blocked row whose leg fell back to another module
            new = {f'$STATE@ORBTRIM{i}': 'U' if L['nwo_trim'] else 'S'}
            new.update({f'OT{i}_{k}@ORBTRIM{i}_SK': v for k, v in L['nwo_trim_vals'].items()})
            c_ = b['cols']; keys = list(c_); p_ = keys.index('$PRP@PartNo')
            b['cols'] = {**{k: c_[k] for k in keys[:p_]}, **new, **{k: c_[k] for k in keys[p_:]}}
    return out, skipped


def npsm_bodyface_text(sp, legs):
    """2026-10-02 (1502): how the NPSM swivel body face of this row is sourced - per size (the leg dashes), from SPEC npsm_bodyface
    {(dash, dash): text, 'other': text}; roots without it keep the shared wording"""
    bf = sp.get('npsm_bodyface')
    if not bf: return 'ASSUMED for the elbow forging'
    return bf.get(tuple(L['dash'] for L in legs), bf['other'])


def assume_text(root, legs):
    sp = SPEC[root]; k = {L['kind'] for L in legs}; t = []
    if sp.get('elbow'):
        t.append('forged elbow body per the 2500HX pattern (Brennan 2500-06-06-FG STEP): one hex arm along each leg, A/F = max(Air-Way hex, JIC thread majors), flats normal to Z, '
                 '30deg double-cone corner puck about Z (radius = hex corner, height = flats); hex-end 75deg chamfers and edge fillets NOT modelled')
        if 'NPTFF' in k:
            pass
    else: t.append('forged hex body per the 2603HX pattern (Brennan 2603 + 2650 STEPs): hex bars A/F = max(Air-Way hex, male thread majors), flats normal to Z, '
             + ('two continuous bars (X and Y)' if sp.get('cross') else 'run bar continuous through the branch, branch hex arm') + '; hex-end 75deg chamfers and edge fillets NOT modelled')
    if 'JICM' in k: t.append('JIC legs: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); Thread feature over THDZ')
    if any(L['kind'] in ('JICM', 'JICBH') and G.JIC.get(L['dash'], {}).get('src40') for L in legs): t.append(G.JIC40_ASSUME)   # SIZE-40
    if 'JICBH' in k: t.append('bulkhead leg (Brennan 2701-08-08-FG STEP): hex arm -> round collar of Air-Way dia O (flush with the hex flats where Air-Way prints O = the flats, e.g. 2701 -06/-10/-12; the revolved core under the hex arm is drawn 0.02 inside the flats and is hidden by the hex) -> JIC bulkhead end, relief to tip = Air-Way i2 (STEP 2.11 - 0.86 = 1.25 = i2), JIC thread run from the relief to the land; K1 read as the collar thickness (ASSUMPTION: the STEP collar is 0.875 x 0.125 followed by a 0.125 round shank at the thread dia, not modelled); -LN configs ship with a locknut (separate part, not modelled)')
    if any(L.get('arm_short') for L in legs):
        # 2026-10-02 (BH_ARM_SHORT): on these rows the core under the hex arm is not hidden everywhere - do not claim it is
        j_ = [n_ for n_, x_ in enumerate(t) if x_.startswith('bulkhead leg (Brennan 2701-08-08-FG STEP)')]
        assert len(j_) == 1 and t[j_[0]].count(' and is hidden by the hex)') == 1, j_
        t[j_[0]] = t[j_[0]].replace(' and is hidden by the hex)', f' and shows over the {BH_ARM_SHORT} band where the hex arm ends short of the '
                                    f'collar on this row - see the bulkhead hex arm note)')
    # 2026-10-09 (PERLEGSW): a perleg root names each leg's own columns and, on a tee, the Brennan tee forgings the body face was seen on (shape)
    _pl = [(kd, lc, leg_end(sp, j)) for j, (kd, lc, bc, tc) in enumerate(legs4(sp)) if kd in ('JICSW', 'NPSMSW')] if sp.get('perleg') else []
    _cn = lambda kd, f: ' / '.join(dict.fromkeys(f(lc, e) .split('@')[0] for k_, lc, e in _pl if k_ == kd))
    if 'JICSW' in k:
        _s = G.SWIV_ASSUME.replace('the body hex stops at the measured body-face position of the 6500 forged arm (ASSUMED for a straight body)',
                                   'the forged hex arm stops at the measured body-face position (= the 6500 forged-arm end on all 4 STEPs' + ('' if sp.get('elbow') else '; ASSUMED for a tee') + ')')
        if not sp.get('perleg'): t.append(_s + '; swivel leg length = Air-Way M5 (crossing to the nut face), nose tip at Air-Way M10')
        else:
            if not sp.get('elbow'): _s = _s.replace('; ASSUMED for a tee)', '; on a tee: the library body-face position SWIV_MEAS BODYS, seen on the Brennan 6603-06-06-06-FG / '
                                                    '6606-06-06-06-FG tee forgings - shape only, user decision 2026-10-08 - every swivel there = SWIV_MEAS[6])')
            t.append(_s + '; every swivel leg: leg length = the row ' + _cn('JICSW', lambda lc, e: lc) + ' (crossing to the nut face), nose tip at the row '
                     + _cn('JICSW', lambda lc, e: e[0]) + ', nut hex = the row ' + _cn('JICSW', lambda lc, e: e[1]))
    if 'NPSMSW' in k:
        _w = ('THE ROW ' + _cn('NPSMSW', lambda lc, e: e[0]) + ' AND STEM TIP AT THE ROW ' + _cn('NPSMSW', lambda lc, e: lc) + ' (crossing to the nut face / to the stem tip, per leg)') \
            if sp.get('perleg') else 'AIR-WAY ' + sp['npsm'][0].split('@')[0] + ' AND STEM TIP AT AIR-WAY M1/M (crossing to the stem tip)'
        _b = ('1404 straight body face BODY_TO_TIP; on a tee seen on the Brennan 1601-08-08-08-FG / 1603-08-08-08-FG tee forgings - shape only, every NPSM swivel there = '
              'NPSM_MEAS[8]' if not sp.get('elbow') else 'Brennan 1404 straight body face - ' + npsm_bodyface_text(sp, legs)) if sp.get('perleg') else \
            'Brennan 1404 straight body face - ' + npsm_bodyface_text(sp, legs)
        t.append(G.NPSM_ASSUME.replace('NUT FACE AT AIR-WAY W AND STEM TIP AT AIR-WAY L', 'NUT FACE AT ' + _w)
                 .replace('neck behind the nut, body face at the measured distance behind the stem tip (Brennan)', 'neck behind the nut, the forged hex arm ends at the measured body face behind the stem tip (' + _b + ')'))
    if 'NWO' in k: t.append(NWO_ASSUME)
    if 'HOSEB' in k:
        _hl = [(lc, bc) for kd, lc, bc, tc in legs4(sp) if kd == 'HOSEB'][0]
        _hs = [L.get('hbsrc') for L in legs if L['kind'] == 'HOSEB' and L.get('hbsrc')]      # per-row bore source (hose_dh fallback)
        t.append(HOSEB_ASSUME + f'; hose leg length = the row\'s {_hl[0].split("@")[0]} read as the axis crossing to the hose tip (ASSUMPTION, mapping: Brennan '
                 'TFA p28-p30 drawings L = hose leg, Brennan 4501-08-08-FG STEP hose hex arm 0.555 + stub 1.500 = catalog L 2.055; Air-Way L4 / L5 = Brennan '
                 'L within 0.002 on 4601-06-06 / 4601-32-32)')
        hb_ = _hs[0][0] if _hs else sp.get('hose_bore', 'own')
        if _hs: _hl = (_hl[0], _hs[0][1])
        t.append('hose leg bore = ' + (f"the part's single bore column {_hl[1].split('@')[0]} carried through both legs (ASSUMPTION: the table prints one "
                                       'bore, the adjustable-ORB end drill; Q-HOSEB-BORE option (a), user 2026-10-18 A15)' if hb_ == 'own' else
                                       f"the part's own hose drill column {_hl[1].split('@')[0]} (Brennan TFA B1 DRILL; Q-HOSEB-BORE, user 2026-10-18 A15 'look at "
                                       "Brennan'); the threaded leg keeps its own drill" if hb_ == 'col' else
                                       'the Air-Way 4404 equal-size through bore D3 (hose end library, Q-HOSEB-BORE option (b))'))
    if any(L.get('faceoff') for L in legs): t.append(FACEOFF_ASSUME)
    if any(L.get('nwo_trim') for L in legs): t.append(NWO_TRIM_ASSUME)
    if any(L.get('nwo_src') for L in legs):      # 2026-10-18 (ANGLED): adjustable-ORB end cells transferred from another series
        for L in legs:
            if not L.get('nwo_src'): continue
            i3c, thc, gvc, I3, THDL, GRVD = L['nwo_src']
            t.append(f'adjustable ORB end cells not printed for this series, taken from the Air-Way {i3c[1:]} rows of the same ORB size -{L["dash"]:02d} '
                     f'(Q-TRANSFER-ENDLIB = yes, user 2026-10-08): tip-to-body-face ORB_I3 {I3} (checked = Brennan 6801 STEP)'
                     + (f', thread length ORB_THDL {THDL}' if thc.startswith('=') else '') + (f', O-ring groove dia ORB_GRVDIA {GRVD}' if gvc.startswith('=') else ''))
    if any(L.get('trim') for L in legs): t.append(ANGLED_NECK_ASSUME if sp.get('neck_turn') else NECK_ASSUME)
    t += angled_texts(sp, legs)                 # 2026-10-18 (ANGLED): only a 135 deg leg with a helix / female port / swivel adds text
    for kf_ in FLG_KINDS:
        if kf_ in k: t.append(FLGLEG_ASSUME[kf_])
    if k & set(FLG_KINDS): t.append(FLGLEG_SHAPE)
    if 'NPTFM' in k: t.append('male NPTF legs: ASME B1.20.3 cone + relief to the Brennan-measured 5404 end length; confirmed on a forged tee by Brennan 5600-16-16-16-FG STEP (hex stops at N - 0.94, relief dia 1.315 = pipe OD, 0.001 proud of the 1.3125 flats)')
    if 'NPTFF' in k:
        t.append('female legs: the forged hex arm stops 0.26 short of the port face and the end is a ROUND COLLAR of dia = the hex flats - MEASURED on the '
                 'Brennan 2502-06-04-FG, 5502-04-04/-08-08/-16-16-FG, 5504-08-08-FG and 5605-08-08-08-FG STEPs (collar 0.260 at every size and leg; '
                 'single manufacturer); port-mouth 45deg chamfer and hex chamfers not modelled')
        if sp.get('nptff_text') == 'ANGLED_NPTFF': t.append(angled_nptff_text(sp))     # 2026-10-18 (ANGLED): 1504 / 5503 / 5505
        elif sp.get('nptff_text'): t.append(sp['nptff_text'])        # 2026-10-02 (1502): the root words its own port sentence (source per row)
        elif sp.get('p1'):
            # 2026-10-02 (new masters 2505 / 2606 / 2611): tap drill and port thread length per row, sources named
            # 2026-10-09 (Q-TRANSFER-ENDLIB = yes, user 2026-10-08): the rows take the end-library port values, not their own Brennan file
            t.append("female NPTF legs: tap drill = the row's TAPDRILL (end library: the per-size tap drill every built female pipe port carries = "
                     "Air-Way's per-size value; user 2026-10-08 'reuse end details - yes'), tapered helix over MS51503 P1 max (" + BR5405 + "; the row's "
                     + sp['p1'].split('@')[0] + ' only where the row carries one - said in $COMMENT); connecting drill to the axis crossing = '
                     + sp['conn_src'])
        else: t.append('female NPTF legs: Air-Way tap drill to MS51503 P1 max (' + BR5405 + '), tapered helix over P1; connecting drill to the axis crossing = '
                 + (f"the part's own {sp['conn'].split('@')[0]} column (ASSUMPTION{'; capped at the tap drill where larger' if sp.get('elbow') else ''})" if sp.get('conn') else 'the tap drill carried to the crossing (ASSUMPTION: Air-Way publishes no bore for this part)'))
    t.append('each leg bore runs from its face to the axis crossing')
    # 2026-10-09 (wave 2): every END-LIBRARY token of a leg's own end tuple (5th element), with its source (Q-TRANSFER-ENDLIB = yes, user 2026-10-08)
    _tok = [c_ for l_ in sp['legs'] if len(l_) > 4 for c_ in l_[4] if isinstance(c_, str) and c_.startswith('=')]
    if any(L.get('td_lib') for L in legs): _tok.append('=FPT:TD')
    if _tok: t.append("end-library values (Q-TRANSFER-ENDLIB, user 2026-10-08 'reuse end details - yes'): "
                      + '; '.join(ENDLIB_TEXT.get(c_, f'{c_}: end library') for c_ in dict.fromkeys(_tok)))
    # 2026-10-18 (genfeat PERLEGSW): a perleg root's rows come from several sources (Brennan TFA catalog, OMi drawings, Air-Way - each row
    # names its own in the first part of $PRP@AxialSource): the shared texts that name Air-Way as the row source are worded source-neutrally
    if sp.get('perleg'):
        _jic = any(kd in ('JICM', 'JICBH') for kd, lc, bc, tc in legs4(sp)); _hx = sp['hex'].split('@')[0]
        for a_, b_ in (('hex bars A/F = max(Air-Way hex, male thread majors)', 'hex bars A/F = ' + ('max(the row body hex ' + _hx + ', JIC thread majors)' if _jic else
                                                                                                    'the row body hex ' + _hx + ' (no male JIC leg, so no 2603HX raise)')),
                       ('A/F = max(Air-Way hex, JIC thread majors)', 'A/F = ' + ('max(the row body hex ' + _hx + ', JIC thread majors)' if _jic else
                                                                                 'the row body hex ' + _hx + ' (no male JIC leg, so no 2603HX raise)')),
                       ('nut hex = Air-Way C(2) (must equal the Brennan nut, checked per row)', 'nut hex = the row nut hex (must equal the Brennan nut, checked per row)'),
                       ('swivel nut hex = Air-Way C3', 'swivel nut hex = the row nut hex (must equal the Brennan nut, checked per row)'),
                       ('nose tip at Air-Way L minus the to-seat length (Brennan within 0.01)', 'nose tip at the row nose-tip length (nut face to nose tip compared '
                        'with the Brennan swivel NOSETIP_B per row, a difference is said in $COMMENT)'),
                       (' (user decision 2026-09-24: follow Air-Way - at -08 Air-Way W-L 0.33 vs Brennan 0.28, so the nut sits 0.05 further out than on the Brennan part)',
                        ' (the row is followed; its nut face to stem tip is compared with the Brennan 1404 value TIP_B per row, a difference is said in $COMMENT)'),
                       ('female NPTF legs: Air-Way tap drill to MS51503 P1 max', "female NPTF legs: the row's TAPDRILL (the end-library per-size tap drill) to MS51503 P1 max"),
                       ('(ASSUMPTION: Air-Way publishes no bore for this part)', '(ASSUMPTION: no source prints a connecting bore for this part)')):
            t = [x_.replace(a_, b_) for x_ in t]
    t += sp.get('assume_extra', [])          # 2026-10-02: per-root notes (pilot STEP comparison) - only the new roots carry them
    s_ = '; '.join(t)
    for a_, b_ in sp.get('assume_reps', ()):        # 2026-10-02 (1502): per-root wording of the shared texts (every pair must apply)
        assert a_ in s_, (root, a_); s_ = s_.replace(a_, b_)
    return s_


def write_sw2(root, built):
    sp = SPEC[root]
    ok = [b for b in built if not b['chk']]
    ref = [b for b in ok if b['pn'] == sp['ref']] or ok
    refrow = ref[0]
    ok.sort(key=lambda b: (b['pn'] != refrow['pn'], b['pn']))
    hdr = list(refrow['cols'].keys())
    for b in ok: assert list(b['cols'].keys()) == hdr, (b['pn'], set(b['cols']) ^ set(hdr))
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Sheet1'
    ws.append([None] + hdr)
    for b in ok: ws.append([b['pn']] + [b['cols'][k] for k in hdr])
    p = f'{OUT}/DesignTable_{root}_SW2.xlsx'; wb.save(p)
    return hdr, ok, refrow


# ---------------------------------------------------------------- VBA
def sub(text, name, kind='Sub'):
    i = text.index(f'\n{kind} {name}('); j = text.index(f'\nEnd {kind}', i) + len(f'\nEnd {kind}')
    return text[i + 1:j] + '\n'


HELP = ''
for n in ('DrawProfile', 'Trace', 'Check', 'NameDim', 'NameAng', 'Dim_len', 'Dim_ptline', 'Dim_len2', 'Dim_rad', 'DeleteDisp', 'Collinear', 'BoreCut', 'ThreadCut'):
    HELP += sub(HX2603, n)
HELP += sp3.DIMANG + '\n\n'
for n in ('MakeCut', 'MakeCut2', 'SelectCircEdge', 'SelectEndFace', 'FeatCentreX', 'Volume', 'HexSketch', 'SuppressEverywhere'):
    HELP += sub(HX2603, n, 'Function')
for n in ('HexArm', 'HexRun', 'DimSeg1', 'DimSegOrigin'):
    HELP += sub(HX2603, n)
assert 'Check nm & " suppressed", sup' not in HELP or True
# threads stay LIVE until the final resting-state step (so the table checks and the sweep exercise them)
HELP = HELP.replace('''    sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)
    Check nm & " suppressed", sup''', '''    Trace nm & ": left live until the final suppress step"''')
assert 'Check nm & " suppressed", sup' not in HELP
# helical NPTF thread (straights version: axis-aware via curAxis, explicit profile dims) + helpers
HELP += G.HX
HELP += '''Function ExtremeAlong(dx As Double, dy As Double, dz As Double) As Double
    ' exact extent of the solid along a direction (GetPartBox is loose around helical thread faces)
    On Error Resume Next
    Dim b As Variant, bd As SldWorks.Body2, px As Double, py As Double, pz As Double
    b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(b) Then Exit Function
    Set bd = b(0)
    If bd.GetExtremePoint(dx, dy, dz, px, py, pz) Then ExtremeAlong = px * dx + py * dy + pz * dz
End Function
'''
HELP += '''Function AxisCoveredAx(pos As Double) As Boolean
    ' True when a planar face normal to the current leg axis at 'pos' contains the axis point, i.e. the bore is NOT open there
    On Error Resume Next
    Dim bods As Variant, bd As SldWorks.Body2, faces As Variant, i As Long, fc As SldWorks.Face2, sf As SldWorks.Surface, pp As Variant, cp As Variant, q(2) As Double
    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bods) Then Exit Function
    Set bd = bods(0)
    faces = bd.GetFaces
    q(0) = 0: q(1) = 0: q(2) = 0: q(curAxis) = pos
    For i = LBound(faces) To UBound(faces)
        Set fc = faces(i)
        Set sf = fc.GetSurface
        If sf.IsPlane Then
            pp = sf.PlaneParams
            If Abs(Abs(pp(curAxis)) - 1) < 0.0001 And Abs(pp(3 + curAxis) - pos) < 0.00002 Then
                cp = fc.GetClosestPointOn(q(0), q(1), q(2))
                If Abs(cp(0) - q(0)) < 0.000002 And Abs(cp(1) - q(1)) < 0.000002 And Abs(cp(2) - q(2)) < 0.000002 Then AxisCoveredAx = True: Exit Function
            End If
        End If
    Next i
End Function
'''
for need in ('Sub HelixThread(', 'Sub DimPtOrigin(', 'Function MkLine(', 'Sub HexRun(', 'Sub HexArm(', 'Function HexSketch(', 'Sub BoreCut(', 'Sub ThreadCut(', 'Function SuppressEverywhere(', 'Function SegVertex(', 'Sub DrawProfile('):
    assert need in HELP, need


# 2026-09-24: rename the thread-profile pitch dimension explicitly (library profile of a non-16-tpi reference size keeps "Pitch")
_OLDP = """    Check nm & " profile dims reachable as Profile_Height@" & nm & "_PROF", Not swModel.Parameter("Profile_Height@" & nm & "_PROF") Is Nothing"""
_NEWP = _OLDP + """
    Dim pfq As SldWorks.Feature, pdq As SldWorks.DisplayDimension, pmq As SldWorks.Dimension
    Set pfq = swModel.FeatureByName(nm & "_PROF")
    If Not pfq Is Nothing Then
        Set pdq = pfq.GetFirstDisplayDimension
        Do While Not pdq Is Nothing
            Set pmq = pdq.GetDimension2(0)
            If LCase(pmq.Name) = "pitch" Then pmq.Name = "THDPITCH": Trace nm & ": profile pitch dimension renamed Pitch -> THDPITCH"
            Set pdq = pfq.GetNextDisplayDimension(pdq)
        Loop
    End If
    Check nm & " profile pitch reachable as THDPITCH@" & nm & "_PROF", Not swModel.Parameter("THDPITCH@" & nm & "_PROF") Is Nothing"""
HELP = HELP.replace(_OLDP, _NEWP)
assert 'profile pitch reachable' in HELP
U_HELP = '\n\' ---------------------------------------------------------------- angled-leg helpers (45-deg elbows, 2026-09-24)\n\' The angled leg runs along the unit vector (UX, UY, 0) in the Front Plane. Local leg coordinates (a along the axis from\n\' the crossing, q radial) map to model (a*UX - q*UY, a*UY + q*UX). Sketch coordinates on the Front Plane = model X/Y.\nSub DrawProfileU(hzLen As Double)\n    Dim i As Long\n    ReDim seg(NPTS - 1)\n    swSkMgr.AddToDB = True\n    For i = 0 To NPTS - 2\n        Set seg(i) = swSkMgr.CreateLine(PX(i) * UX - PR(i) * UY, PX(i) * UY + PR(i) * UX, 0, PX(i + 1) * UX - PR(i + 1) * UY, PX(i + 1) * UY + PR(i + 1) * UX, 0)\n    Next i\n    Set seg(NPTS - 1) = swSkMgr.CreateLine(PX(NPTS - 1) * UX, PX(NPTS - 1) * UY, 0, PX(0) * UX, PX(0) * UY, 0)\n    Set axisCL = swSkMgr.CreateCenterLine(0, 0, 0, PX(NPTS - 1) * UX, PX(NPTS - 1) * UY, 0)\n    Set hzCL = swSkMgr.CreateCenterLine(0, 0, 0, hzLen, 0, 0)\n    swSkMgr.AddToDB = False\n    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, cl As SldWorks.SketchLine, hz As SldWorks.SketchLine\n    For i = 0 To NPTS - 1\n        Set ln1 = seg(i): Set ln2 = seg((i + 1) Mod NPTS)\n        swModel.ClearSelection2 True\n        ln1.GetEndPoint2.Select4 False, Nothing\n        ln2.GetStartPoint2.Select4 True, Nothing\n        swModel.SketchAddConstraints "sgMERGEPOINTS"\n    Next i\n    \' axial lines parallel to the leg axis, radial lines perpendicular to it (the closing line lies on the axis itself)\n    For i = 0 To NPTS - 2\n        swModel.ClearSelection2 True\n        If Abs(PR(i) - PR(i + 1)) < 0.000000001 Then\n            seg(i).Select4 False, Nothing: axisCL.Select4 True, Nothing: swModel.SketchAddConstraints "sgPARALLEL"\n        ElseIf Abs(PX(i) - PX(i + 1)) < 0.000000001 Then\n            seg(i).Select4 False, Nothing: axisCL.Select4 True, Nothing: swModel.SketchAddConstraints "sgPERPENDICULAR"\n        End If\n    Next i\n    Set cl = axisCL: Set ln1 = seg(0): Set ln2 = seg(NPTS - 2): Set hz = hzCL\n    swModel.ClearSelection2 True\n    cl.GetStartPoint2.Select4 False, Nothing: ln1.GetStartPoint2.Select4 True, Nothing\n    swModel.SketchAddConstraints "sgCOINCIDENT"\n    swModel.ClearSelection2 True\n    cl.GetEndPoint2.Select4 False, Nothing: ln2.GetEndPoint2.Select4 True, Nothing\n    swModel.SketchAddConstraints "sgCOINCIDENT"\n    swModel.ClearSelection2 True\n    ln1.GetStartPoint2.Select4 False, Nothing\n    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0\n    swModel.SketchAddConstraints "sgCOINCIDENT"\n    \' horizontal reference line from the origin - the leg direction is fixed by ONE angle dimension to it (LEGANGn)\n    swModel.ClearSelection2 True\n    hzCL.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"\n    swModel.ClearSelection2 True\n    hz.GetStartPoint2.Select4 False, Nothing\n    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0\n    swModel.SketchAddConstraints "sgCOINCIDENT"\n    swModel.ClearSelection2 True\n    hzCL.Select4 False, Nothing\n    Dim dd As SldWorks.DisplayDimension\n    Set dd = swModel.AddDimension2(hzLen / 2, -0.004, 0)\n    NameDim dd, "HZREF", hzLen\n    swModel.ClearSelection2 True\nEnd Sub\n\nSub DimAngLeg(nm As String, valRad As Double, tx As Double, ty As Double)\n    \' angle between the leg axis and the horizontal reference line; the text is tried inside the wanted sector first\n    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long, c As Double, s As Double, px As Double, py As Double, f As Double\n    Dim rots As Variant: rots = Array(0#, -0.35, 0.35)\n    For k = 0 To 8\n        f = 1# + 0.5 * (k \\ 3)\n        c = Cos(rots(k Mod 3)): s = Sin(rots(k Mod 3))\n        px = f * (tx * c - ty * s): py = f * (tx * s + ty * c)\n        swModel.ClearSelection2 True\n        axisCL.Select4 False, Nothing\n        hzCL.Select4 True, Nothing\n        Set dd = swModel.AddDimension2(px, py, 0)\n        If Not dd Is Nothing Then\n            v = dd.GetDimension2(0).SystemValue\n            If Abs(v - valRad) < 0.0005 Then Exit For\n            Trace nm & " angle try " & k & ": " & Format(v * 180 / 3.14159265358979, "0.0") & " deg (want " & Format(valRad * 180 / 3.14159265358979, "0.0") & ")"\n            DeleteDisp dd: Set dd = Nothing\n        End If\n    Next k\n    NameAng dd, nm, valRad\nEnd Sub\n\nSub DimLenU(i As Long, nm As String, valM As Double, a As Double, q As Double)\n    \' aligned length of a line along the angled leg (or, i = -1, the distance between the two end lines):\n    \' text candidates on the perpendicular through (a, q); a horizontal/vertical projection is rejected by value\n    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long, f As Double\n    Dim fs As Variant: fs = Array(1#, 1.6, 0.6, -1#, 2.4, -1.6)\n    For k = 0 To 5\n        swModel.ClearSelection2 True\n        If i = -1 Then\n            seg(0).Select4 False, Nothing\n            seg(NPTS - 2).Select4 True, Nothing\n        Else\n            seg(i).Select4 False, Nothing\n        End If\n        f = fs(k)\n        Set dd = swModel.AddDimension2(a * UX - f * q * UY, a * UY + f * q * UX, 0)\n        If Not dd Is Nothing Then\n            v = dd.GetDimension2(0).SystemValue\n            If Abs(v - valM) < 0.000005 Then Exit For\n            Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"\n            DeleteDisp dd: Set dd = Nothing\n        End If\n    Next k\n    NameDim dd, nm, valM\nEnd Sub\n\nSub DimRadU(i As Long, nm As String, valM As Double, a As Double, q As Double)\n    \' line-to-centreline distance (the radius, SP3 behaviour) for a line along the angled leg\n    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long, f As Double\n    Dim fs As Variant: fs = Array(1#, 2#, 3#, -1#)\n    For k = 0 To 3\n        swModel.ClearSelection2 True\n        seg(i).Select4 False, Nothing\n        axisCL.Select4 True, Nothing\n        f = fs(k)\n        Set dd = swModel.AddDimension2(a * UX - f * q * UY, a * UY + f * q * UX, 0)\n        If dd Is Nothing Then Exit For\n        v = dd.GetDimension2(0).SystemValue\n        If Abs(v - valM) < 0.000005 Then Exit For\n        Trace nm & " try " & k & ": value " & Format(v / IN_, "0.0000") & " (want radius " & Format(valM / IN_, "0.0000") & ")"\n        DeleteDisp dd: Set dd = Nothing\n    Next k\n    NameDim dd, nm, valM\nEnd Sub\n\nFunction SelectEndFaceV(fx As Double) As Boolean\n    \' planar face normal to the angled leg axis at signed distance fx along it\n    On Error Resume Next\n    Dim bods As Variant, bd As SldWorks.Body2, faces As Variant, i As Long, fc As SldWorks.Face2, sf As SldWorks.Surface, pp As Variant\n    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)\n    If IsEmpty(bods) Then Exit Function\n    Set bd = bods(0)\n    faces = bd.GetFaces\n    For i = LBound(faces) To UBound(faces)\n        Set fc = faces(i)\n        Set sf = fc.GetSurface\n        If sf.IsPlane Then\n            pp = sf.PlaneParams       \' nx,ny,nz, rx,ry,rz\n            If Abs(Abs(pp(0) * UX + pp(1) * UY) - 1) < 0.0001 And Abs(pp(3) * UX + pp(4) * UY - fx) < 0.00002 Then\n                swModel.ClearSelection2 True\n                SelectEndFaceV = fc.Select4(False, Nothing)\n                Exit Function\n            End If\n        End If\n    Next i\nEnd Function\n\nFunction SelectCircEdgeV(ex As Double, er As Double, mark As Long) As Boolean\n    \' circular edge centred on the angled leg axis at distance ex along it, radius er\n    On Error Resume Next\n    Dim bods As Variant, bd As SldWorks.Body2, edges As Variant, i As Long, e As SldWorks.Edge, cv As SldWorks.Curve, cp As Variant\n    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)\n    If IsEmpty(bods) Then Exit Function\n    Set bd = bods(0)\n    edges = bd.GetEdges\n    For i = LBound(edges) To UBound(edges)\n        Set e = edges(i)\n        Set cv = e.GetCurve\n        If cv.IsCircle Then\n            cp = cv.CircleParams      \' cx,cy,cz, ax,ay,az, radius\n            If Abs(cp(0) - ex * UX) < 0.00002 And Abs(cp(1) - ex * UY) < 0.00002 And Abs(cp(2)) < 0.00002 And Abs(cp(6) - er) < 0.00002 Then\n                Dim sd As SldWorks.SelectData\n                Set sd = swSelMgr.CreateSelectData: sd.Mark = mark\n                swModel.ClearSelection2 True\n                SelectCircEdgeV = e.Select4(False, sd)\n                Exit Function\n            End If\n        End If\n    Next i\nEnd Function\n\nFunction FeatCentreV(f As SldWorks.Feature) As Double\n    \' centre of the feature\'s faces (union of their boxes) projected on the angled leg axis\n    On Error Resume Next\n    Dim faces As Variant, i As Long, bx As Variant, k As Long, lo(2) As Double, hi(2) As Double, n As Long\n    faces = f.GetFaces\n    For k = 0 To 2: lo(k) = 1E+30: hi(k) = -1E+30: Next k\n    If Not IsEmpty(faces) Then\n        For i = LBound(faces) To UBound(faces)\n            bx = faces(i).GetBox\n            For k = 0 To 2\n                If bx(k) < lo(k) Then lo(k) = bx(k)\n                If bx(3 + k) > hi(k) Then hi(k) = bx(3 + k)\n            Next k\n            n = n + 1\n        Next i\n    End If\n    If n = 0 Then FeatCentreV = 0 Else FeatCentreV = ((lo(0) + hi(0)) / 2) * UX + ((lo(1) + hi(1)) / 2) * UY\nEnd Function\n\nFunction AxisCoveredV(pos As Double) As Boolean\n    \' True when a planar face normal to the angled leg axis at \'pos\' contains the axis point (the bore is NOT open there)\n    On Error Resume Next\n    Dim bods As Variant, bd As SldWorks.Body2, faces As Variant, i As Long, fc As SldWorks.Face2, sf As SldWorks.Surface, pp As Variant, cp As Variant, q(2) As Double\n    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)\n    If IsEmpty(bods) Then Exit Function\n    Set bd = bods(0)\n    faces = bd.GetFaces\n    q(0) = pos * UX: q(1) = pos * UY: q(2) = 0\n    For i = LBound(faces) To UBound(faces)\n        Set fc = faces(i)\n        Set sf = fc.GetSurface\n        If sf.IsPlane Then\n            pp = sf.PlaneParams\n            If Abs(Abs(pp(0) * UX + pp(1) * UY) - 1) < 0.0001 And Abs(pp(3) * UX + pp(4) * UY - pos) < 0.00002 Then\n                cp = fc.GetClosestPointOn(q(0), q(1), q(2))\n                If Abs(cp(0) - q(0)) < 0.000002 And Abs(cp(1) - q(1)) < 0.000002 And Abs(cp(2) - q(2)) < 0.000002 Then AxisCoveredV = True: Exit Function\n            End If\n        End If\n    Next i\nEnd Function\n\nFunction MakeLegPlane(nm As String, tipDist As Double) As Boolean\n    \' reference plane through the origin, parallel to the angled leg\'s tip face (= normal to the leg axis)\n    On Error Resume Next\n    Dim ok As Boolean, f As SldWorks.Feature, rp As Object, tf As Object, ad As Variant, dr As Double, dc As Double\n    ok = SelectEndFaceV(tipDist)\n    Check nm & ": leg tip face found " & Format(tipDist / IN_, "0.0000") & " along the leg", ok\n    If Not ok Then Exit Function\n    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 1, Nothing, 0\n    swFeatMgr.InsertRefPlane swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_Parallel, 0, swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_Coincident, 0, 0, 0\n    Trace nm & ": InsertRefPlane " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear\n    Set f = swModel.FeatureByPositionReverse(0)\n    If f Is Nothing Then Check nm & " reference plane created", False: Exit Function\n    Check nm & " reference plane created (" & f.GetTypeName2 & ")", f.GetTypeName2 = "RefPlane"\n    If f.GetTypeName2 <> "RefPlane" Then Exit Function\n    f.Name = nm\n    Set rp = f.GetSpecificFeature2\n    Set tf = rp.Transform\n    ad = tf.ArrayData\n    dr = ad(6) * UX + ad(7) * UY      \' plane z axis as a matrix row\n    dc = ad(2) * UX + ad(5) * UY      \' ... or as a column\n    Trace nm & ": plane z axis (" & Format(ad(6), "0.000") & ", " & Format(ad(7), "0.000") & ", " & Format(ad(8), "0.000") & "), leg axis (" & Format(UX, "0.000") & ", " & Format(UY, "0.000") & ")"\n    Check nm & " is normal to the angled leg", Abs(Abs(dr) - 1) < 0.001 Or Abs(Abs(dc) - 1) < 0.001\n    swModel.ClearSelection2 True\n    MakeLegPlane = True\nEnd Function\n'

def derive(src, name, newname, reps, kind='Sub'):
    t = sub(src, name, kind)
    t = t.replace(f'{kind} {name}(', f'{kind} {newname}(', 1)
    for a_, b_ in reps:
        assert a_ in t, (name, a_)
        t = t.replace(a_, b_)
    return t


HELP += U_HELP
HELP += """Sub Dim_pair(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    ' distance between two parallel sketch lines seg(i) and seg(j) (leg length to a swivel nut face, positions from the nut face)
    swModel.ClearSelection2 True
    seg(i).Select4 False, Nothing
    seg(j).Select4 True, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
End Sub

Sub NutHexCutAx(tp As Double, afM As Double, depthM As Double, skName As String, dimName As String, featName As String)
    ' swivel nut hex: hexagon (across flats afM) sketched on the leg's nut face (normal to the current leg axis at tp), flats
    ' normal to Z (vertex check in model coordinates, both sketch relations tried), OUTSIDE cut blind over depthM into the part
    On Error Resume Next
    Dim tryRel As Long, relName As String, ok As Boolean, k As Long, zmax As Double
    Dim mu As SldWorks.MathUtility: Set mu = swApp.GetMathUtility
    Dim skF As SldWorks.Feature
    For tryRel = 0 To 1
        If tryRel = 0 Then relName = "sgHORIZONTAL" Else relName = "sgVERTICAL"
        ok = SelectEndFace(tp)
        Check skName & ": nut face found at " & Format(tp / IN_, "0.0000") & " on axis " & curAxis, ok
        If Not ok Then Exit Sub
        swSkMgr.InsertSketch True
        Dim poly As Variant, circ As SldWorks.SketchSegment
        poly = swSkMgr.CreatePolygon(0, 0, 0, afM / 2, 0, 0, 6, True)
        For k = LBound(poly) To UBound(poly)
            If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
        Next k
        swModel.ClearSelection2 True
        circ.Select4 False, Nothing
        Dim dd As SldWorks.DisplayDimension
        Set dd = swModel.AddDimension2(afM * 0.7, afM * 0.7, 0)
        If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = afM
        NameDim dd, dimName, afM
        swModel.ClearSelection2 True
        For k = LBound(poly) To UBound(poly)
            If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints relName: Exit For
        Next k
        Dim arc As SldWorks.SketchArc: Set arc = circ
        swModel.ClearSelection2 True
        arc.GetCenterPoint2.Select4 False, Nothing
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        swModel.SketchAddConstraints "sgCOINCIDENT"
        swModel.ClearSelection2 True
        Dim skO As SldWorks.Sketch, xf As SldWorks.MathTransform, mp As SldWorks.MathPoint, arr(2) As Double, pd As Variant, lnq As SldWorks.SketchLine
        Set skO = swSkMgr.ActiveSketch
        Set xf = skO.ModelToSketchTransform: Set xf = xf.Inverse
        zmax = 0
        For k = LBound(poly) To UBound(poly)
            If poly(k).GetType = swSketchSegments_e.swSketchLINE Then
                Set lnq = poly(k)
                arr(0) = lnq.GetStartPoint2.X: arr(1) = lnq.GetStartPoint2.Y: arr(2) = 0
                Set mp = mu.CreatePoint(arr): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData
                If Abs(pd(2)) > zmax Then zmax = Abs(pd(2))
            End If
        Next k
        ok = (Abs(zmax - afM / 2) < 0.0003)
        Trace skName & ": " & relName & " -> vertex |z| max " & Format(zmax / IN_, "0.0000") & " (flats want " & Format(afM / 2 / IN_, "0.0000") & ")"
        swSkMgr.InsertSketch True
        Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
        If ok Then Exit For
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        swModel.Extension.DeleteSelection2 0
        Trace skName & ": sketch removed, retrying with the other relation"
    Next tryRel
    Check skName & " nut flats normal to Z", ok
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long
    v0 = Volume()
    For attempt = 0 To 1
        Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, True, (attempt = 1), 0#, False, featName & " attempt " & attempt)
        If Not cut Is Nothing Then
            v1 = Volume()
            If v1 < v0 - 1E-12 Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next attempt
    Check featName & " created and removed material (attempt " & attempt & ")", Not cut Is Nothing
    If cut Is Nothing Then Exit Sub
    cut.Name = featName
    Check featName & " removed only the nut corners (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.8 * v0)
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = cut.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then dm.Name = "DEPTH"
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = cut.GetNextDisplayDimension(d)
    Loop
    Check featName & " dims: " & names, InStr(names, "DEPTH=") > 0
End Sub
"""
# only macros with an adjustable ORB leg carry this helper (keeps every other macro byte-identical to its release)
NWO_HELP = derive(HELP, 'NutHexCutAx', 'NutHexCutNWO', [
    ('featName As String)', 'featName As String, sg As Double, expRemM3 As Double)'),
    ("    ' swivel nut hex: hexagon (across flats afM) sketched on the leg's nut face (normal to the current leg axis at tp), flats\n    ' normal to Z (vertex check in model coordinates, both sketch relations tried), OUTSIDE cut blind over depthM into the part",
     "    ' ADJUSTABLE ORB LOCKNUT hex (2026-09-25): hexagon (across flats afM) sketched on the nut's inner face (normal to the current leg axis\n    ' at tp), flats normal to Z, OUTSIDE cut blind over depthM toward the tip (sg). The cut direction is accepted only when the cut's own\n    ' faces are centred on the nut (tp + sg*depthM/2) - on an elbow the other direction would also remove material (the other leg's hex)"),
    ('Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long', 'Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long, cxF As Double, cxW As Double'),
    ('            If v1 < v0 - 1E-12 Then Exit For',
     '            cxF = FeatCentreX(cut): cxW = tp + sg * depthM / 2\n'
     '            Trace featName & " attempt " & attempt & ": removed " & Format((v0 - v1) / (IN_ ^ 3), "0.00000") & " in^3 (expect " & Format(expRemM3 / (IN_ ^ 3), "0.00000") & "), cut faces centred at " & Format(cxF / IN_, "0.0000") & " on axis " & curAxis & " (want " & Format(cxW / IN_, "0.0000") & ")"\n'
     '            If v1 < v0 - 1E-12 And Abs(cxF - cxW) < 0.25 * depthM Then Exit For'),
    ('    Check featName & " removed only the nut corners (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.8 * v0)',
     '    Check featName & " removed only the nut corners (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.8 * v0)\n'
     '    Check featName & " removed " & Format((v0 - v1) / (IN_ ^ 3), "0.00000") & " in^3 = the chamfered nut envelope outside the hexagon (expect " & Format(expRemM3 / (IN_ ^ 3), "0.00000") & ")", Abs((v0 - v1) - expRemM3) < 0.02 * expRemM3 + 1E-10'),
    ('Check skName & ": nut face found at "', 'Check skName & ": locknut inner face found at "'),
])
# 2026-10-01: only macros with a corner neck trim (45 deg elbow, adjustable ORB leg) carry these helpers (every other macro stays as released)
ORBTRIM_HELP = """
' ---------------------------------------------------------------- corner neck trim helpers (45-deg elbow, adjustable ORB leg, 2026-10-01)
Sub DrawLoopAx(v As Variant, axLen As Double, nmAx As String)
    ' CLOSED loop for a revolve about the sketch X axis that does not touch the axis (corner neck trim, 2026-10-01): v = x, r pairs in
    ' sketch coordinates (Front Plane = model X/Y). Corners merged, horizontal / vertical relations as drawn; the axis centreline runs from
    ' the origin along +X under the whole loop (horizontal, fixed length axLen named nmAx - it only carries the revolve axis and the radius dimensions).
    Dim i As Long, n As Long
    n = (UBound(v) + 1) \\ 2
    NPTS = n
    ReDim PX(n - 1): ReDim PR(n - 1)
    For i = 0 To n - 1
        PX(i) = v(2 * i): PR(i) = v(2 * i + 1)
    Next i
    ReDim seg(n - 1)
    swSkMgr.AddToDB = True
    For i = 0 To n - 1
        Set seg(i) = swSkMgr.CreateLine(PX(i), PR(i), 0, PX((i + 1) Mod n), PR((i + 1) Mod n), 0)
    Next i
    Set axisCL = swSkMgr.CreateCenterLine(0, 0, 0, axLen, 0, 0)
    swSkMgr.AddToDB = False
    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, cl As SldWorks.SketchLine
    For i = 0 To n - 1
        Set ln1 = seg(i): Set ln2 = seg((i + 1) Mod n)
        swModel.ClearSelection2 True
        ln1.GetEndPoint2.Select4 False, Nothing
        ln2.GetStartPoint2.Select4 True, Nothing
        swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next i
    For i = 0 To n - 1
        swModel.ClearSelection2 True
        If Abs(PR(i) - PR((i + 1) Mod n)) < 0.000000001 Then
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
        ElseIf Abs(PX(i) - PX((i + 1) Mod n)) < 0.000000001 Then
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
        End If
    Next i
    swModel.ClearSelection2 True
    axisCL.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    Set cl = axisCL
    swModel.ClearSelection2 True
    cl.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    Call DimSeg1(axisCL, nmAx, axLen, axLen / 2, -0.004)
End Sub

Sub OrbTrimCut(skName As String, featName As String, live As Boolean, expRemM3 As Double)
    ' CORNER NECK TRIM (2026-10-01): revolve CUT of the closed trim loop about its axis centreline (the adjustable ORB leg's axis, +X).
    ' live = False: the reference size needs no trim. The loop was drawn with its inner radius below the ORB neck, so the cut removes a
    ' ring of the neck (= expRemM3) and is created at all; it is then suppressed in this configuration. The design table sets the neck
    ' radius and $STATE (U where the forged corner stands out of the neck, S elsewhere) in every configuration.
    On Error Resume Next
    Dim v0 As Double, v1 As Double, f As SldWorks.Feature, sd As SldWorks.SelectData, r As Boolean
    v0 = Volume()
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 skName, "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    axisCL.Select4 True, sd
    Set f = swFeatMgr.FeatureRevolve2(True, True, False, True, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Trace featName & ": FeatureRevolve2 (cut) -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    Check featName & " revolve cut created", Not f Is Nothing
    If f Is Nothing Then Exit Sub
    f.Name = featName
    v1 = Volume()
    If live Then
        Check featName & " removed " & Format((v0 - v1) / (IN_ ^ 3), "0.00000") & " in^3 of the forged corner beyond the ORB body face", v1 < v0 - 1E-12
    Else
        Check featName & " (creation only: inner radius below the neck) removed " & Format((v0 - v1) / (IN_ ^ 3), "0.00000") & " in^3 = the neck ring (expect " & Format(expRemM3 / (IN_ ^ 3), "0.00000") & ")", Abs((v0 - v1) - expRemM3) < 0.02 * expRemM3 + 1E-12
        r = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swThisConfiguration, Empty)
        Trace featName & ": SetSuppression2(this configuration) -> " & r
        swModel.ForceRebuild3 False
        Check featName & " suppressed in this configuration (the reference size needs no trim; the design table sets it per configuration)", f.IsSuppressed <> False
        v1 = Volume()
        Check featName & " suppressed: volume back to " & Format(v1 / (IN_ ^ 3), "0.00000") & " in^3 (before the cut " & Format(v0 / (IN_ ^ 3), "0.00000") & ")", Abs(v1 - v0) < 0.000001 * v0 + 1E-12
    End If
    Dim d As SldWorks.DisplayDimension, names As String
    Set d = f.GetFirstDisplayDimension
    Do While Not d Is Nothing
        names = names & d.GetDimension2(0).Name & " "
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Trace featName & " feature dims: " & names
End Sub
"""
# 2026-10-01 (NECK-6502): only macros with a swivel neck turn (6502) carry this helper (keeps every other macro byte-identical)
NECK_HELP = """Function NeckRing(skName As String, pfx As String, a0 As Double, lenM As Double, r0 As Double, r1 As Double, isCut As Boolean) As SldWorks.Feature
    ' swivel neck turn (2026-10-01, NECK-6502): rectangle a0 .. a0 + lenM along leg 1 (+X) and r0 .. r1 (0 < r0 < r1) from its axis on the
    ' Front Plane, revolved 360 deg (cut or boss: a ring) about a centreline from the origin along +X whose end is vertical with the
    ' rectangle's bottom-right corner. Dims: pfx_A0 = origin to the left line (the swivel body face), pfx_LEN = the bottom line,
    ' pfx_RIN = origin to the bottom line, pfx_ROUT = origin to the top line.
    Dim a1 As Double, rm As Double
    a1 = a0 + lenM: rm = (r0 + r1) / 2
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim s0 As SldWorks.SketchSegment, s1 As SldWorks.SketchSegment, s2 As SldWorks.SketchSegment, s3 As SldWorks.SketchSegment, sc As SldWorks.SketchSegment
    Set s0 = swSkMgr.CreateLine(a0, r0, 0, a1, r0, 0)
    Set s1 = swSkMgr.CreateLine(a1, r0, 0, a1, r1, 0)
    Set s2 = swSkMgr.CreateLine(a1, r1, 0, a0, r1, 0)
    Set s3 = swSkMgr.CreateLine(a0, r1, 0, a0, r0, 0)
    Set sc = swSkMgr.CreateCenterLine(0#, 0#, 0, a1, 0#, 0)
    swSkMgr.AddToDB = False
    Dim q0 As SldWorks.SketchLine, q1 As SldWorks.SketchLine, q2 As SldWorks.SketchLine, q3 As SldWorks.SketchLine, qc As SldWorks.SketchLine
    Set q0 = s0: Set q1 = s1: Set q2 = s2: Set q3 = s3: Set qc = sc
    swModel.ClearSelection2 True: q0.GetEndPoint2.Select4 False, Nothing: q1.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: q1.GetEndPoint2.Select4 False, Nothing: q2.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: q2.GetEndPoint2.Select4 False, Nothing: q3.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: q3.GetEndPoint2.Select4 False, Nothing: q0.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: s0.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: s2.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: s1.Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: s3.Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: sc.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: qc.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True: qc.GetEndPoint2.Select4 False, Nothing: q0.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgVERTICALPOINTS"
    Call DimSegOrigin(s3, pfx & "_A0", a0, a0 / 2, rm)
    Call DimSeg1(s0, pfx & "_LEN", lenM, (a0 + a1) / 2, r0 - 0.08 * IN_)
    Call DimSegOrigin(s0, pfx & "_RIN", r0, a1 + 0.15 * IN_, r0 / 2)
    Call DimSegOrigin(s2, pfx & "_ROUT", r1, a1 + 0.3 * IN_, r1 / 2)
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim skF As SldWorks.Feature
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' revolve 360 deg about the centreline; first with automatic feature scope (as PUCK / the leg revolves), then - as MakeCut does for
    ' the extrude cuts - once more with the feature scope off (all bodies) if SolidWorks hands back Nothing
    Dim sdN As SldWorks.SelectData, att As Long
    For att = 0 To 1
        swModel.ClearSelection2 True
        swModel.Extension.SelectByID2 skName, "SKETCH", 0, 0, 0, False, 0, Nothing, 0
        Set sdN = swSelMgr.CreateSelectData: sdN.Mark = 16
        sc.Select4 True, sdN
        Set NeckRing = swFeatMgr.FeatureRevolve2(True, True, False, isCut, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, (att = 0), (att = 0))
        Trace skName & ": FeatureRevolve2 (cut = " & isCut & ", feature scope " & IIf(att = 0, "auto", "off") & ") -> " & (Not NeckRing Is Nothing)
        If Not NeckRing Is Nothing Then Exit For
    Next att
End Function
"""
HELP += derive(HELP, 'ThreadCut', 'ThreadCutV', [('ok = SelectCircEdge(ex, er, 0)', 'ok = SelectCircEdgeV(ex, er, 0)'), ('SelectCircEdge ex, er, 0', 'SelectCircEdgeV ex, er, 0'), ('FeatCentreX(f)', 'FeatCentreV(f)')])
HELP += derive(HELP, 'BoreCut', 'BoreCutV', [('ok = SelectEndFace(faceX)', 'ok = SelectEndFaceV(faceX)'), ('SelectEndFace faceX', 'SelectEndFaceV faceX')])
HELP += derive(HELP, 'HexArm', 'HexArmV', [('cxF = FeatCentreX(ext)', 'cxF = FeatCentreV(ext)')])
assert 'Sub NutHexCutNWO(' in NWO_HELP and 'Sub NutHexCutNWO(' not in HELP
for need in ('Sub ThreadCutV(', 'Sub BoreCutV(', 'Sub HexArmV(', 'Function MakeLegPlane(', 'Sub DrawProfileU(', 'profile pitch reachable'):
    assert need in HELP, need
assert 'SelectCircEdge(' not in derive(HELP, 'ThreadCutV', 'X', []) and 'FeatCentreX' not in derive(HELP, 'ThreadCutV', 'X', [])

SWEEP = HX2603[HX2603.index("    ' ---- all-config rebuild sweep"):HX2603.index("    stepName = \"Save\"")]
assert 'SuppressEverywhere' in SWEEP and 'All-config sweep' in SWEEP


def puck_vba(BR, AC):
    """30 deg double cone about Z at the crossing - the turned hex corner of a forged elbow (2500HX, built and swept clean)."""
    h = BR * IN; r1 = (AC - PUCK_INSET - BR * TAN30) * IN; xc = (AC - PUCK_INSET) * IN; o35 = 0.35 * IN; o70 = 0.70 * IN; o25 = 0.25 * IN
    f = lambda v: f'{v:.9f}'
    return f"""    ' ================= PUCK: 30 deg double cone about Z at the crossing (the turned hex corner, per Brennan) =================
    stepName = "PUCK"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim pA As SldWorks.SketchSegment, pB As SldWorks.SketchSegment, pC As SldWorks.SketchSegment, pD As SldWorks.SketchSegment, pE As SldWorks.SketchSegment, pX As SldWorks.SketchSegment
    Set pA = swSkMgr.CreateLine(0#, {f(-h)}, 0, {f(r1)}, {f(-h)}, 0)
    Set pB = swSkMgr.CreateLine({f(r1)}, {f(-h)}, 0, {f(xc)}, 0#, 0)
    Set pC = swSkMgr.CreateLine({f(xc)}, 0#, 0, {f(r1)}, {f(h)}, 0)
    Set pD = swSkMgr.CreateLine({f(r1)}, {f(h)}, 0, 0#, {f(h)}, 0)
    Set pE = swSkMgr.CreateCenterLine(0#, {f(h)}, 0, 0#, {f(-h)}, 0)
    Set pX = swSkMgr.CreateLine(0#, 0#, 0, {f(xc)}, 0#, 0)
    swSkMgr.AddToDB = False
    pX.ConstructionGeometry = True
    Dim qa As SldWorks.SketchLine, qb As SldWorks.SketchLine, qc As SldWorks.SketchLine, qd As SldWorks.SketchLine, qe As SldWorks.SketchLine, qx As SldWorks.SketchLine
    Set qa = pA: Set qb = pB: Set qc = pC: Set qd = pD: Set qe = pE: Set qx = pX
    swModel.ClearSelection2 True: qa.GetEndPoint2.Select4 False, Nothing: qb.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qb.GetEndPoint2.Select4 False, Nothing: qc.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qc.GetEndPoint2.Select4 False, Nothing: qd.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qd.GetEndPoint2.Select4 False, Nothing: qe.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qe.GetEndPoint2.Select4 False, Nothing: qa.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qx.GetEndPoint2.Select4 False, Nothing: qb.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: pA.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pD.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pX.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pE.Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: qx.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True: pE.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Call DimSegOrigin(pA, "PUCK_HB", {f(h)}, {r1/2:.6f}, {-(h+o35):.6f})
    Call DimSegOrigin(pD, "PUCK_HT", {f(h)}, {r1/2:.6f}, {(h+o35):.6f})
    Call DimSeg1(pA, "PUCK_R1B", {f(r1)}, {r1/2:.6f}, {-(h+o70):.6f})
    Call DimSeg1(pD, "PUCK_R1T", {f(r1)}, {r1/2:.6f}, {(h+o70):.6f})
    Call DimSeg1(pX, "PUCK_XC", {f(xc)}, {xc/2:.6f}, {-o25:.6f})
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0): swFeat.Name = "PUCK"
    Check "PUCK sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "PUCK", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    pE.Select4 True, sd
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "PUCK revolve created", Not rev Is Nothing
    If Not rev Is Nothing Then rev.Name = "PUCK_BODY"
"""


def neck_vba(i, lg):
    """2026-10-01 (NECK-6502): the swivel neck turn on leg i (+X) of a 45 deg elbow, built in the reference configuration."""
    t = lg['trim']; f = lambda v: f'{v * IN:.9f}'
    ring = math.pi * (t['r'] ** 2 - t['rin'] ** 2) * t['len'] * IN ** 3          # the neck ring the cut always takes (m^3)
    # tolerances relative to that ring (0.1 %), not to the part volume: a failed fill shows as -100 % of it, SolidWorks' mass-property
    # accuracy stays far below 0.1 %
    if t['reach'] <= t['r']:
        net = (f'    Check "NECKTRIM{i} + NECKFILL{i} leave the reference configuration unchanged: net " & Format((nk{i}_v2 - nk{i}_v0) / IN_ ^ 3, "0.000000") & " in^3 '
               f'(the corner stays inside the neck here: {t["reach"]:.4f} off the axis vs neck radius {t["r"]:.4f})", Abs(nk{i}_v2 - nk{i}_v0) < {0.001 * ring:.12e}')
    else:
        net = (f'    Check "NECKTRIM{i} + NECKFILL{i} removed the corner outside the neck: net " & Format((nk{i}_v2 - nk{i}_v0) / IN_ ^ 3, "0.000000") & " in^3 '
               f'(the corner stands {t["reach"]:.4f} off the axis vs neck radius {t["r"]:.4f})", nk{i}_v2 < nk{i}_v0 - {0.001 * ring:.12e}')
    return f"""    ' ================= NECKTRIM{i} / NECKFILL{i}: swivel neck turned clear of the forged corner (Brennan 6502-12-12-FG STEP, 2026-10-01) =================
    '  From the swivel body face ({t['a0']:.4f}) to the nut rear face ({t['a0'] + t['len']:.4f}) nothing stands outside the neck (radius {t['r']:.4f}): the cut takes
    '  the ring from {t['rin']:.4f} out to {t['rout']:.4f} (the corner puck and the start corner of the angled hex arm with it), the boss puts the ring
    '  {t['rin']:.4f} .. {t['r']:.4f} back. Both act in every configuration - the cut always takes that (solid) ring, so it never removes nothing.
    stepName = "NECKTRIM{i}"
    Dim nk{i}_v0 As Double, nk{i}_v1 As Double, nk{i}_v2 As Double, nk{i}_f As SldWorks.Feature
    nk{i}_v0 = Volume()
    Set nk{i}_f = NeckRing("NECKTRIM{i}", "TRIM", {f(t['a0'])}, {f(t['len'])}, {f(t['rin'])}, {f(t['rout'])}, True)
    nk{i}_v1 = Volume()
    Check "NECKTRIM{i} revolve cut took " & Format((nk{i}_v0 - nk{i}_v1) / IN_ ^ 3, "0.000000") & " in^3 (at least the neck ring {ring / IN ** 3:.6f})", (Not nk{i}_f Is Nothing) And (nk{i}_v0 - nk{i}_v1 > 0.98 * {ring:.12e})
    If Not nk{i}_f Is Nothing Then nk{i}_f.Name = "NECKTRIM{i}_CUT"
    stepName = "NECKFILL{i}"
    Set nk{i}_f = NeckRing("NECKFILL{i}", "FILL", {f(t['a0'])}, {f(t['len'])}, {f(t['rin'])}, {f(t['r'])}, False)
    nk{i}_v2 = Volume()
    Check "NECKFILL{i} revolve created (neck ring back)", Not nk{i}_f Is Nothing
    If Not nk{i}_f Is Nothing Then nk{i}_f.Name = "NECKFILL{i}_BODY"
{net}
"""


def hoseface_vba(i, lg, e45):
    """2026-10-09 (wave 2, HOSEB, DESIGN 4.6 / 4.7): the face-off of the forged corner at the hose hex face of leg i, in the reference configuration"""
    fo = lg['faceoff']; f = lambda v: f'{v * IN:.9f}'
    ux, uy = (UXV, UYV) if e45 else (1.0, 0.0)
    ring = math.pi * (fo['rS'] ** 2 - fo['rin'] ** 2) * fo['depth']
    reg = (f"ring {fo['rin']:.4f} .. {fo['rout']:.4f} about the hose axis" if e45 else
           f"rectangle y {-fo['ylo']:.4f} .. {fo['ytop']:.4f} (along the other leg, to its hex arm end) x z +-{fo['zh']:.4f} minus the circle {fo['rin']:.4f}")
    what = (f"the corner ({', '.join(fo['past_by'])}) stands up to {fo['past_max_r']:.4f} off the hose axis past the face: net change < 0" if fo['past'] else
            'the corner clears the face here: net change 0')
    return f"""    ' ================= HOSEFACE{i} / STUBFILL{i}: forged corner faced off at the hose hex face (wave 2, HOSEB, 2026-10-09) =================
    '  Plane HFPLN{i} at the hose hex face ({fo['sh']:.4f} along the hose leg); cut {reg} over {fo['depth']:.4f}
    '  away from the crossing (to 0.05 past the corner radius), then the stub ring {fo['rin']:.4f} .. {fo['rS']:.4f} ({ring:.6f} in^3) put back. {what}.
    stepName = "HOSEFACE{i}"
    Call HoseFace({i}, {not e45}, "{'PLN2' if e45 else 'Right Plane'}", {ux:.15f}, {uy:.15f}, {f(fo['sh'])}, {f(fo['depth'])}, {f(fo['rin'])}, {f(fo['rS'])}, {f(fo.get('ylo', 0.0))}, {f(fo.get('ytop', 0.0))}, {f(fo.get('zh', 0.0))}, {f(fo.get('rout', 0.0))}, {fo['past']})
    Check "D1@HFPLN{i} reachable", Not swModel.Parameter("D1@HFPLN{i}") Is Nothing
    Check "DEPTH@HOSEFACE{i} reachable", Not swModel.Parameter("DEPTH@HOSEFACE{i}") Is Nothing
    Check "DEPTH@STUBFILL{i} reachable", Not swModel.Parameter("DEPTH@STUBFILL{i}") Is Nothing
"""


HOSEFACE_HELP = """
' ---------------------------------------------------------------- hose-leg face-off helpers (wave 2, HOSEB, 2026-10-09)
Function FeatCentreU(f As SldWorks.Feature, ux As Double, uy As Double) As Double
    ' centre of the feature's faces (union of their boxes) projected on the leg direction (ux, uy, 0)
    On Error Resume Next
    Dim faces As Variant, i As Long, bx As Variant, k As Long, lo(2) As Double, hi(2) As Double, n As Long
    faces = f.GetFaces
    For k = 0 To 2: lo(k) = 1E+30: hi(k) = -1E+30: Next k
    If Not IsEmpty(faces) Then
        For i = LBound(faces) To UBound(faces)
            bx = faces(i).GetBox
            For k = 0 To 2
                If bx(k) < lo(k) Then lo(k) = bx(k)
                If bx(3 + k) > hi(k) Then hi(k) = bx(3 + k)
            Next k
            n = n + 1
        Next i
    End If
    If n = 0 Then FeatCentreU = 0 Else FeatCentreU = ((lo(0) + hi(0)) / 2) * ux + ((lo(1) + hi(1)) / 2) * uy
End Function

Function HoseFacePlane(nm As String, basePl As String, distM As Double, ux As Double, uy As Double) As Boolean
    ' the hose hex face plane: reference plane parallel to basePl (Right Plane / PLN2: through the origin, normal to the hose leg) at distM along
    ' the leg direction (ux, uy, 0) - not the face itself (it splits differently per configuration). Its side is checked on the plane's own
    ' origin; if SolidWorks put it on the other side it is deleted and made again with the flip option (256). Offset = D1@<nm> (design table).
    On Error Resume Next
    Dim att As Long, f As SldWorks.Feature, rp As Object, ad As Variant, pos As Double, ok As Boolean
    For att = 0 To 1
        swModel.ClearSelection2 True
        ok = swModel.Extension.SelectByID2(basePl, "PLANE", 0, 0, 0, False, 0, Nothing, 0)
        Check nm & ": base plane " & basePl & " selected", ok
        If ok = False Then Exit Function
        swFeatMgr.InsertRefPlane swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_Distance + IIf(att = 1, 256, 0), distM, 0, 0, 0, 0
        Trace nm & ": InsertRefPlane distance " & Format(distM / IN_, "0.0000") & IIf(att = 1, " (flipped)", "") & " " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
        Set f = swModel.FeatureByPositionReverse(0)
        If f Is Nothing Then Exit For
        If f.GetTypeName2 <> "RefPlane" Then Set f = Nothing: Exit For
        Set rp = f.GetSpecificFeature2
        ad = rp.Transform.ArrayData
        pos = ad(9) * ux + ad(10) * uy
        Trace nm & ": plane origin (" & Format(ad(9) / IN_, "0.0000") & ", " & Format(ad(10) / IN_, "0.0000") & ", " & Format(ad(11) / IN_, "0.0000") & ") = " & Format(pos / IN_, "0.0000") & " along the hose leg (want " & Format(distM / IN_, "0.0000") & ")"
        If Abs(pos - distM) < 0.000002 Then Exit For
        swModel.ClearSelection2 True
        f.Select2 False, 0
        swModel.Extension.DeleteSelection2 0
        Set f = Nothing
    Next att
    Check nm & " reference plane at the hose hex face (" & Format(distM / IN_, "0.0000") & " along the hose leg)", Not f Is Nothing
    If f Is Nothing Then Exit Function
    f.Name = nm
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = f.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - distM) < 0.000001 Then dm.Name = "D1"
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check nm & " offset reachable as D1@" & nm & " (" & names & ")", Not swModel.Parameter("D1@" & nm) Is Nothing
    swModel.ClearSelection2 True
    HoseFacePlane = True
End Function

Sub HoseFaceCentre(c As SldWorks.SketchSegment)
    ' circle centre on the projected origin = the hose axis on this plane (as BoreCut does on a face)
    On Error Resume Next
    Dim ca As SldWorks.SketchArc
    Set ca = c
    swModel.ClearSelection2 True
    ca.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
End Sub

Sub HoseFaceDia(c As SldWorks.SketchSegment, nm As String, diaM As Double, tx As Double, ty As Double)
    ' diameter dimension of a circle (as BoreCut); a radius handed back is switched to the diameter display
    On Error Resume Next
    Dim dd As SldWorks.DisplayDimension, v As Double
    swModel.ClearSelection2 True
    c.Select4 False, Nothing
    Set dd = swModel.AddDimension2(tx, ty, 0)
    If Not dd Is Nothing Then
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - diaM / 2) < 0.000005 Then dd.Diametric = True: Trace nm & ": radius dim switched to diameter -> " & Format(dd.GetDimension2(0).SystemValue / IN_, "0.0000")
    End If
    NameDim dd, nm, diaM
End Sub

Function HoseFaceRing(skName As String, pl As String, nmIn As String, nmOut As String, r0 As Double, r1 As Double, sh As Double, ux As Double, uy As Double) As SldWorks.Feature
    ' two circles r0 < r1 about the hose axis on the plane pl (a ring), centres on the projected origin, diameters dimensioned
    On Error Resume Next
    Dim mu As SldWorks.MathUtility, skO As SldWorks.Sketch, xf As SldWorks.MathTransform, mp As SldWorks.MathPoint, arr(2) As Double, pc As Variant
    Dim c0 As SldWorks.SketchSegment, c1 As SldWorks.SketchSegment, skF As SldWorks.Feature
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 pl, "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    Set mu = swApp.GetMathUtility: Set skO = swSkMgr.ActiveSketch
    Set xf = skO.ModelToSketchTransform
    arr(0) = sh * ux: arr(1) = sh * uy: arr(2) = 0
    Set mp = mu.CreatePoint(arr): Set mp = mp.MultiplyTransform(xf): pc = mp.ArrayData
    Trace skName & ": hose axis at sketch (" & Format(pc(0) / IN_, "0.0000") & ", " & Format(pc(1) / IN_, "0.0000") & ", " & Format(pc(2) / IN_, "0.0000") & ")"
    swSkMgr.AddToDB = True
    Set c0 = swSkMgr.CreateCircleByRadius(pc(0), pc(1), 0, r0)
    Set c1 = swSkMgr.CreateCircleByRadius(pc(0), pc(1), 0, r1)
    swSkMgr.AddToDB = False
    Check skName & " circles created", (Not c0 Is Nothing) And (Not c1 Is Nothing)
    If c0 Is Nothing Or c1 Is Nothing Then swSkMgr.InsertSketch True: Exit Function
    HoseFaceCentre c0
    HoseFaceCentre c1
    HoseFaceDia c0, nmIn, 2 * r0, pc(0) + 0.7 * r0, pc(1) + 0.7 * r0
    HoseFaceDia c1, nmOut, 2 * r1, pc(0) + 0.7 * r1, pc(1) - 0.7 * r1
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Set HoseFaceRing = skF
End Function

Function HoseFaceRect(skName As String, pl As String, pfx As String, sh As Double, ylo As Double, ytop As Double, zh As Double, rin As Double) As SldWorks.Feature
    ' 90 deg elbow, hose leg on +X: on the hose hex face plane pl (parallel to the Right Plane) the rectangle y = -ylo .. ytop (model Y, along the
    ' other leg up to its hex arm end), z = -zh .. zh, minus the circle rin about the hose axis. Corners placed through the sketch's
    ' ModelToSketchTransform, sides horizontal / vertical as drawn, each side dimensioned to the projected origin (DimSegOrigin): pfx_ZH (z = -zh),
    ' pfx_YTOP, pfx_ZH2 (z = +zh), pfx_YLO; the region is verified in model space afterwards (as NutHexCutAx verifies the hex flats).
    On Error Resume Next
    Dim mu As SldWorks.MathUtility, skO As SldWorks.Sketch, xf As SldWorks.MathTransform, xi As SldWorks.MathTransform, mp As SldWorks.MathPoint
    Dim arr(2) As Double, pd As Variant, pu(3) As Double, pv(3) As Double, k As Long, ya As Variant, za As Variant, cu As Double, cv As Double, ok As Boolean
    Dim s(3) As SldWorks.SketchSegment, c As SldWorks.SketchSegment, q1 As SldWorks.SketchLine, q2 As SldWorks.SketchLine, skF As SldWorks.Feature
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 pl, "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    Set mu = swApp.GetMathUtility: Set skO = swSkMgr.ActiveSketch
    Set xf = skO.ModelToSketchTransform: Set xi = xf.Inverse
    ya = Array(-ylo, ytop, ytop, -ylo): za = Array(-zh, -zh, zh, zh)
    For k = 0 To 3
        arr(0) = sh: arr(1) = ya(k): arr(2) = za(k)
        Set mp = mu.CreatePoint(arr): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData
        pu(k) = pd(0): pv(k) = pd(1)
    Next k
    arr(0) = sh: arr(1) = 0: arr(2) = 0
    Set mp = mu.CreatePoint(arr): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData
    cu = pd(0): cv = pd(1)
    swSkMgr.AddToDB = True
    For k = 0 To 3
        Set s(k) = swSkMgr.CreateLine(pu(k), pv(k), 0, pu((k + 1) Mod 4), pv((k + 1) Mod 4), 0)
    Next k
    Set c = swSkMgr.CreateCircleByRadius(cu, cv, 0, rin)
    swSkMgr.AddToDB = False
    For k = 0 To 3
        Set q1 = s(k): Set q2 = s((k + 1) Mod 4)
        swModel.ClearSelection2 True: q1.GetEndPoint2.Select4 False, Nothing: q2.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next k
    ok = True
    For k = 0 To 3
        swModel.ClearSelection2 True
        s(k).Select4 False, Nothing
        If Abs(pv(k) - pv((k + 1) Mod 4)) < 0.000000001 Then
            swModel.SketchAddConstraints "sgHORIZONTAL"
        ElseIf Abs(pu(k) - pu((k + 1) Mod 4)) < 0.000000001 Then
            swModel.SketchAddConstraints "sgVERTICAL"
        Else
            ok = False
        End If
    Next k
    Check skName & ": rectangle sides along the sketch axes (plane parallel to the Right Plane)", ok
    HoseFaceCentre c
    Call DimSegOrigin(s(0), pfx & "_ZH", zh, 1.2 * (pu(0) + pu(1)) / 2, 1.2 * (pv(0) + pv(1)) / 2)
    Call DimSegOrigin(s(1), pfx & "_YTOP", ytop, 1.2 * (pu(1) + pu(2)) / 2, 1.2 * (pv(1) + pv(2)) / 2)
    Call DimSegOrigin(s(2), pfx & "_ZH2", zh, 1.2 * (pu(2) + pu(3)) / 2, 1.2 * (pv(2) + pv(3)) / 2)
    Call DimSegOrigin(s(3), pfx & "_YLO", ylo, 1.2 * (pu(3) + pu(0)) / 2, 1.2 * (pv(3) + pv(0)) / 2)
    HoseFaceDia c, pfx & "_DIN", 2 * rin, cu + 0.7 * rin, cv + 0.7 * rin
    swModel.ClearSelection2 True
    Dim ymn As Double, ymx As Double, zmx As Double, xbad As Double, ln As SldWorks.SketchLine
    ymn = 1E+30: ymx = -1E+30: zmx = 0: xbad = 0
    For k = 0 To 3
        Set ln = s(k)
        arr(0) = ln.GetStartPoint2.X: arr(1) = ln.GetStartPoint2.Y: arr(2) = 0
        Set mp = mu.CreatePoint(arr): Set mp = mp.MultiplyTransform(xi): pd = mp.ArrayData
        If pd(1) < ymn Then ymn = pd(1)
        If pd(1) > ymx Then ymx = pd(1)
        If Abs(pd(2)) > zmx Then zmx = Abs(pd(2))
        If Abs(pd(0) - sh) > xbad Then xbad = Abs(pd(0) - sh)
    Next k
    Check skName & ": region in model space y " & Format(ymn / IN_, "0.0000") & " .. " & Format(ymx / IN_, "0.0000") & ", |z| " & Format(zmx / IN_, "0.0000") & " on x " & Format(sh / IN_, "0.0000") & " (want " & Format(-ylo / IN_, "0.0000") & " .. " & Format(ytop / IN_, "0.0000") & ", " & Format(zh / IN_, "0.0000") & ")", Abs(ymn + ylo) < 0.000002 And Abs(ymx - ytop) < 0.000002 And Abs(zmx - zh) < 0.000002 And xbad < 0.000002
    swSkMgr.InsertSketch True
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Set HoseFaceRect = skF
End Function

Sub HoseFaceDepth(f As SldWorks.Feature, depthM As Double)
    ' name the feature's depth dimension DEPTH (identified by value)
    On Error Resume Next
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = f.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then dm.Name = "DEPTH"
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check f.Name & " dims: " & names, InStr(names, "DEPTH=") > 0
End Sub

Sub HoseFace(i As Long, rect As Boolean, basePl As String, ux As Double, uy As Double, sh As Double, depthM As Double, rin As Double, rS As Double, ylo As Double, ytop As Double, zh As Double, rout As Double, past As Boolean)
    ' FACE-OFF of the forged corner at the hose hex face (wave 2, HOSEB, DESIGN 4.6): nothing of the corner stands past the hose hex face outside
    ' the stub (Brennan 4503-08-08-FG / 4603-16-16-NWO-FG). HOSEFACEi = blind cut over depthM from the plane HFPLNi away from the crossing of the
    ' region (90 deg: rectangle minus the circle rin; 45 deg: ring rin .. rout); it always takes the stub ring rin .. rS (never a cut that removes
    ' nothing). STUBFILLi = boss of the ring rin .. rS over the same depth puts the stub back. Both act in every configuration.
    On Error Resume Next
    Dim pl As String, sk As SldWorks.Feature, sk2 As SldWorks.Feature, v0 As Double, v1 As Double, v2 As Double, ring As Double
    Dim cut As SldWorks.Feature, fil As SldWorks.Feature, att As Long, cxF As Double, cxW As Double
    pl = "HFPLN" & i
    ring = 3.14159265358979 * (rS * rS - rin * rin) * depthM
    cxW = sh + depthM / 2
    If HoseFacePlane(pl, basePl, sh, ux, uy) = False Then Exit Sub
    If rect Then
        Set sk = HoseFaceRect("HOSEFACE" & i & "_SK", pl, "HF" & i, sh, ylo, ytop, zh, rin)
    Else
        Set sk = HoseFaceRing("HOSEFACE" & i & "_SK", pl, "HF" & i & "_DIN", "HF" & i & "_DOUT", rin, rout, sh, ux, uy)
    End If
    Check "HOSEFACE" & i & "_SK sketch made", Not sk Is Nothing
    If sk Is Nothing Then Exit Sub
    v0 = Volume()
    For att = 0 To 1
        Set cut = MakeCut(sk, swEndConditions_e.swEndCondBlind, depthM, False, (att = 1), 0#, False, "HOSEFACE" & i & " attempt " & att)
        If Not cut Is Nothing Then
            v1 = Volume(): cxF = FeatCentreU(cut, ux, uy)
            Trace "HOSEFACE" & i & " attempt " & att & ": removed " & Format((v0 - v1) / (IN_ ^ 3), "0.000000") & " in^3, cut faces centred at " & Format(cxF / IN_, "0.0000") & " along the hose leg (want " & Format(cxW / IN_, "0.0000") & ")"
            If v1 < v0 - 1E-12 And Abs(cxF - cxW) < 0.25 * depthM Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next att
    Check "HOSEFACE" & i & " cut made on the tip side of the hose hex face (attempt " & att & ")", Not cut Is Nothing
    If cut Is Nothing Then Exit Sub
    cut.Name = "HOSEFACE" & i
    HoseFaceDepth cut, depthM
    Check "HOSEFACE" & i & " took " & Format((v0 - v1) / (IN_ ^ 3), "0.000000") & " in^3 (at least the stub ring " & Format(ring / (IN_ ^ 3), "0.000000") & ")", v0 - v1 > 0.98 * ring
    Set sk2 = HoseFaceRing("STUBFILL" & i & "_SK", pl, "SF" & i & "_DIN", "SF" & i & "_DOUT", rin, rS, sh, ux, uy)
    Check "STUBFILL" & i & "_SK sketch made", Not sk2 Is Nothing
    If sk2 Is Nothing Then Exit Sub
    ' the boss direction is told by the volume: toward the tip it adds exactly the stub ring, toward the crossing (inside the hex arm) ~nothing
    For att = 0 To 1
        swModel.ClearSelection2 True
        swModel.Extension.SelectByID2 "STUBFILL" & i & "_SK", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
        Set fil = swFeatMgr.FeatureExtrusion3(True, False, (att = 1), swEndConditions_e.swEndCondBlind, 0, depthM, 0, False, False, False, False, 0, 0, False, False, False, False, True, False, False, 0, 0, False)
        Trace "STUBFILL" & i & ": FeatureExtrusion3 dir=" & att & " -> " & (Not fil Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
        If Not fil Is Nothing Then
            v2 = Volume(): cxF = FeatCentreU(fil, ux, uy)
            Trace "STUBFILL" & i & " dir " & att & ": added " & Format((v2 - v1) / (IN_ ^ 3), "0.000000") & " in^3 (ring " & Format(ring / (IN_ ^ 3), "0.000000") & "), faces centred at " & Format(cxF / IN_, "0.0000") & " along the hose leg"
            If Abs((v2 - v1) - ring) < 0.02 * ring Then Exit For
            swModel.ClearSelection2 True
            fil.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set fil = Nothing
        End If
    Next att
    Check "STUBFILL" & i & " boss made on the tip side (attempt " & att & ")", Not fil Is Nothing
    If fil Is Nothing Then Exit Sub
    fil.Name = "STUBFILL" & i
    HoseFaceDepth fil, depthM
    Check "STUBFILL" & i & " put back " & Format((v2 - v1) / (IN_ ^ 3), "0.000000") & " in^3 = the stub ring (expect " & Format(ring / (IN_ ^ 3), "0.000000") & ")", Abs((v2 - v1) - ring) < 0.001 * ring
    If past Then
        Check "HOSEFACE" & i & " + STUBFILL" & i & " removed the forged corner past the hose hex face: net " & Format((v2 - v0) / (IN_ ^ 3), "0.000000") & " in^3 (< 0)", v2 < v0 - 0.001 * ring
    Else
        Check "HOSEFACE" & i & " + STUBFILL" & i & " leave the reference configuration unchanged (the corner clears the face): net " & Format((v2 - v0) / (IN_ ^ 3), "0.000000") & " in^3", Abs(v2 - v0) < 0.001 * ring
    End If
End Sub
"""


def emit_leg_u(i, lg):
    # leg along (UXV, UYV) sketched on the Front Plane with parallel/perpendicular relations to its own axis line
    M = lg.get('Mtip', lg['V'][-1][0]); out = []
    def posU(a, q):
        return (a * UXV - q * UYV, a * UYV + q * UXV)
    out.append(f"    ' ================= LEG {i} ({lg['kind']} -{lg['dash']:02d}, along the 135-deg axis) =================")
    out.append(f'    stepName = "LEG{i} sketch"')
    out.append(f'    tipPos = {M*IN:.9f}')
    out.append(f'    LoadLeg {i}')
    out.append('    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0')
    out.append('    swSkMgr.InsertSketch True')
    out.append(f'    DrawProfileU {0.5*IN:.9f}')
    mid = math.radians(135 / 2)
    out.append(f'    Call DimAngLeg("LEGANG{i}", {math.radians(135):.9f}, {0.16*IN*math.cos(mid):.6f}, {0.16*IN*math.sin(mid):.6f})')
    for d in lg['dims']:
        t = d[0]
        if t == 'len':
            _, s_, nm, val, a, q = d
            out.append(f'    Call DimLenU({s_}, "{nm}", {val*IN:.9f}, {a*IN:.6f}, {q*IN:.6f})')
        elif t == 'rad':
            _, s_, nm, val, a, q = d
            out.append(f'    Call DimRadU({s_}, "{nm}", {val*IN:.9f}, {a*IN:.6f}, {q*IN:.6f})')
        elif t == 'ang':
            _, s_, s2, nm, deg, a, q = d; tx, ty = posU(a, q)
            out.append(f'    Call Dim_ang({s_}, {s2}, "{nm}", {math.radians(deg):.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        elif t == 'ptl':
            _, s_, ue, s2, nm, val, a, q = d; tx, ty = posU(a, q)
            out.append(f'    Call Dim_ptline({s_}, {ue}, {s2}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        elif t == 'col':
            out.append(f'    Call Collinear({d[1]}, {d[2]})')
        elif t == 'pair':           # 2026-10-18 (ANGLED): swivel profiles on the 135 deg leg (positions from the nut face)
            _, s_, s2, nm, val, a, q = d; tx, ty = posU(a, q)
            out.append(f'    Call Dim_pair({s_}, {s2}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    out += ['    swModel.ClearSelection2 True', '    swSkMgr.InsertSketch True', '    Set swFeat = swModel.FeatureByPositionReverse(0)',
            f'    swFeat.Name = "LEG{i}"',
            f'    Check "LEG{i} sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)',
            f'    stepName = "LEG{i} revolve"', '    swModel.ClearSelection2 True',
            f'    swModel.Extension.SelectByID2 "LEG{i}", "SKETCH", 0, 0, 0, False, 0, Nothing, 0',
            '    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16', '    axisCL.Select4 True, sd',
            '    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)',
            f'    Check "LEG{i} revolve created", Not rev Is Nothing', '    If rev Is Nothing Then GoTo Finish', f'    rev.Name = "LEG{i}_BODY"', '']
    return out


def orbtrim_check(trims, ok):
    """2026-10-01: per-configuration check of the corner neck trim ($STATE@ORBTRIMi column): live (with its loop values) in the first
    configuration that needs it, suppressed in the first that does not"""
    if not trims: return []
    out = ['    \' ---- corner neck trim per configuration ($STATE@ORBTRIMi: live where the forged corner stands out of the ORB neck) (2026-10-01)',
           '    stepName = "ORB trim check"', '    Dim ot_f As SldWorks.Feature, ot_p As SldWorks.Dimension']
    for i in trims:
        st = f'$STATE@ORBTRIM{i}'
        on = [b for b in ok if b['cols'][st] == 'U'][:1]; off = [b for b in ok if b['cols'][st] == 'S'][:1]
        for b in on + off:
            pn = b['pn']; live = b['cols'][st] == 'U'
            out += [f'    swModel.ShowConfiguration2 "{pn}"', '    swModel.ForceRebuild3 False', f'    Set ot_f = swModel.FeatureByName("ORBTRIM{i}")',
                    f'    If ot_f Is Nothing Then',
                    f'        Check "{pn}: feature ORBTRIM{i} found", False',
                    '    Else']
            if live:
                out += [f'        Check "{pn}: ORBTRIM{i} live (table $STATE U)", ot_f.IsSuppressed = False',
                        f'        Check "{pn}: ORBTRIM{i} cut faces in this size: " & ot_f.GetFaceCount, ot_f.GetFaceCount > 0']
            else:
                out += [f'        Check "{pn}: ORBTRIM{i} suppressed (table $STATE S)", ot_f.IsSuppressed <> False']
            out.append('    End If')
            if live:
                for k, v in b['legs'][i - 1]['nwo_trim_vals'].items():
                    nm = f'OT{i}_{k}@ORBTRIM{i}_SK'
                    out += [f'    Set ot_p = swModel.Parameter("{nm}")',
                            f'    If ot_p Is Nothing Then Check "{pn} {nm} readable", False Else Check "{pn} {nm} = " & Format(ot_p.SystemValue / IN_, "0.0000") & " (table {v:.4f})", Abs(ot_p.SystemValue / IN_ - {v:.5f}) < 0.0005']
    return out + ['']


# ---------------------------------------------------------------- 2026-10-18 (ANGLED, genfeat): helpers for the 135 deg leg
# Appended to a macro ONLY when its 135 deg leg carries a helical thread (HelixThreadV, HelixUCheck + their dimension helpers) or a swivel nut
# (NutHexCutV) - every released macro stays byte-identical. Design: tools/_out/wave2_shapes_20261008/ANGLED/DESIGN.md 3.4 (+ review fixes 3-5).
ANGLED_HELIX_HELP = '''
' ---------------------------------------------------------------- 135-deg leg thread helpers (ANGLED, 2026-10-18)
Function DimPtLnV(pt As SldWorks.SketchPoint, ln As SldWorks.SketchSegment, nm As String, valM As Double, tx As Double, ty As Double, dx As Double, dy As Double) As Boolean
    ' point-to-line distance (the line may be a construction line), value checked; text tried at (tx, ty), then stepped by (dx, dy) both ways
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double, f As Double
    Dim fs As Variant: fs = Array(0#, 1#, -1#, 2#, -2#, 3#)
    For k = 0 To 5
        f = fs(k)
        swModel.ClearSelection2 True
        pt.Select4 False, Nothing
        ln.Select4 True, Nothing
        Set dd = swModel.AddDimension2(tx + f * dx, ty + f * dy, 0)
        If Not dd Is Nothing Then
            v = dd.GetDimension2(0).SystemValue
            If Abs(v - valM) < 0.000005 Then Exit For
            Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"
            DeleteDisp dd: Set dd = Nothing
        End If
    Next k
    NameDim dd, nm, valM
    DimPtLnV = Not dd Is Nothing
End Function

Function DimSegLenV(ln As SldWorks.SketchSegment, nm As String, valM As Double, tx As Double, ty As Double, dx As Double, dy As Double) As Boolean
    ' aligned length of one (construction) line, value checked (a horizontal / vertical projection is rejected by value and deleted)
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double, f As Double
    Dim fs As Variant: fs = Array(0#, 1#, -1#, 2#, -2#, 3#)
    For k = 0 To 5
        f = fs(k)
        swModel.ClearSelection2 True
        ln.Select4 False, Nothing
        Set dd = swModel.AddDimension2(tx + f * dx, ty + f * dy, 0)
        If Not dd Is Nothing Then
            v = dd.GetDimension2(0).SystemValue
            If Abs(v - valM) < 0.000005 Then Exit For
            Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"
            DeleteDisp dd: Set dd = Nothing
        End If
    Next k
    NameDim dd, nm, valM
    DimSegLenV = Not dd Is Nothing
End Function

Sub HelixThreadV(tipD As Double, rM As Double, heightM As Double, pitchM As Double, thdhM As Double, taperRad As Double, taperOut As Boolean, apexOut As Boolean, sfx As String, nm As String)
    ' Helical thread on the 45-deg elbow's 135-deg leg (axis (UX, UY, 0) through the origin; Q-NEW-ANGLEDHELIX, 2026-10-18) = HelixThread of
    ' the axis legs (helix on the end face + 60 deg tooth swept along it) with every axis-specific step in leg coordinates:
    '  - helix sketch HELIXSK_<sfx> on the leg end face at tipD (tip / port face / nut face), circle HELIXDIA centred on the projected origin;
    '  - helix HELIX_<sfx> (HEIGHT / PITCH, taper per end kind): flags and start angle tried until the curve starts IN THE FRONT PLANE (z = 0)
    '    at the end face on the circle, its far end lies HEIGHT into the part with the radius the taper wants, right hand (read from the curve);
    '  - tooth THDPROF_<sfx> on the Front Plane: base l1 + l1b parallel to a construction axis line (origin, 135 deg to a horizontal reference
    '    line), PROF_AX = distance from a construction line through the origin normal to the axis, PROF_R / APEXR = distances from the axis
    '    line, 60 deg between the sloped sides (the HelixThread relation set with horizontal / vertical replaced by parallel / perpendicular);
    '  - swept cut <nm>, LEFT LIVE: the all-configuration sweep rebuilds it, HelixUCheck reads it per configuration, the final step suppresses it.
    ' SolidWorks' Thread feature is not used here: on an off-axis female edge it crashed SolidWorks 2026 SP4 (2026-10-15, gen_bent HelixThreadY).
    On Error Resume Next
    Dim ok As Boolean, sk As SldWorks.Feature, hx As SldWorks.Feature, pf As SldWorks.Feature, f As SldWorks.Feature, dd As SldWorks.DisplayDimension
    ok = SelectEndFaceV(tipD)
    Check nm & ": end face found " & Format(tipD / IN_, "0.0000") & " along the 135-deg leg", ok
    If ok = False Then Exit Sub
    swSkMgr.InsertSketch True
    Dim c As SldWorks.SketchSegment, ca As SldWorks.SketchArc
    swSkMgr.AddToDB = True
    Set c = swSkMgr.CreateCircleByRadius(0, 0, 0, rM)
    swSkMgr.AddToDB = False
    Set ca = c
    swModel.ClearSelection2 True
    ca.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    c.Select4 False, Nothing
    Set dd = swModel.AddDimension2(rM * 2, rM * 2, 0)
    If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = 2 * rM
    NameDim dd, "HELIXDIA", 2 * rM
    ' start-angle candidates: the angles at which the sketch's X / Y axes (model coords; matrix rows or columns) give a start with z = 0
    Dim xf As SldWorks.MathTransform, ad As Variant, th(7) As Double, k As Long
    Set xf = swSkMgr.ActiveSketch.ModelToSketchTransform: Set xf = xf.Inverse
    ad = xf.ArrayData
    th(0) = Atan2V(-ad(2), ad(5)): th(1) = th(0) + 3.14159265358979
    th(2) = Atan2V(-ad(6), ad(7)): th(3) = th(2) + 3.14159265358979
    For k = 4 To 7: th(k) = (k - 4) * 1.5707963267949: Next k
    For k = 0 To 3
        Do While th(k) < 0: th(k) = th(k) + 6.28318530717959: Loop
        Do While th(k) >= 6.28318530717959: th(k) = th(k) - 6.28318530717959: Loop
    Next k
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set sk = swModel.FeatureByPositionReverse(0): sk.Name = "HELIXSK_" & sfx
    Check nm & " helix sketch made (" & sk.GetTypeName2 & ")", sk.GetTypeName2 = "ProfileFeature"
    Check nm & " helix sketch fully defined", (sk.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' --- helix: the axis legs' flags first (reversed, clockwise, taperOut as given), then the alternatives; every try checked on the curve
    Dim mdLate As Object: Set mdLate = swModel
    Dim t As Long, rv As Boolean, cw As Boolean, tOut As Boolean, egv As Object, cv As Object, cpd As Object, e0 As Variant, e1 As Variant
    Dim fp(2) As Double, fd(2) As Double, fq(2) As Double, afp As Double, afar As Double, rfp As Double, rfar As Double, rWant As Double
    Dim rx As Double, ry As Double, hand As Double, good As Boolean
    good = False
    For t = 0 To 63
        rv = ((t \\ 8) Mod 2 = 0): cw = ((t \\ 16) Mod 2 = 0): tOut = taperOut
        If (t \\ 32) = 1 Then tOut = Not taperOut
        If taperRad <= 0 And (t \\ 32) = 1 Then Exit For
        rWant = rM + IIf(taperOut, 1#, -1#) * heightM * Tan(taperRad)      ' the radius the end kind wants HEIGHT into the part (male grows, female shrinks)
        swModel.ClearSelection2 True
        sk.Select2 False, 0
        Err.Clear
        mdLate.InsertHelix rv, cw, (taperRad > 0), tOut, swHelixDefinedBy_e.swHelixDefinedByHeightAndPitch, heightM, pitchM, 0#, taperRad, th(t Mod 8)
        Set hx = swModel.FeatureByPositionReverse(0)
        If Not hx Is Nothing Then
            If hx.GetTypeName2 <> "Helix" Then Set hx = Nothing
        End If
        Set egv = Nothing
        If Not hx Is Nothing Then Set egv = hx.GetSpecificFeature2.GetFirstSegment
        If Not egv Is Nothing Then
            Set cv = egv.GetCurve
            Set cpd = egv.GetCurveParams3
            e0 = cv.Evaluate2(cpd.UMinValue, 1): e1 = cv.Evaluate2(cpd.UMaxValue, 1)
            If Abs(e0(0) * UX + e0(1) * UY - tipD) < Abs(e1(0) * UX + e1(1) * UY - tipD) Then
                fp(0) = e0(0): fp(1) = e0(1): fp(2) = e0(2): fd(0) = e0(3): fd(1) = e0(4): fd(2) = e0(5): fq(0) = e1(0): fq(1) = e1(1): fq(2) = e1(2)
            Else
                fp(0) = e1(0): fp(1) = e1(1): fp(2) = e1(2): fd(0) = -e1(3): fd(1) = -e1(4): fd(2) = -e1(5): fq(0) = e0(0): fq(1) = e0(1): fq(2) = e0(2)
            End If
            afp = fp(0) * UX + fp(1) * UY: afar = fq(0) * UX + fq(1) * UY
            rfp = Sqr(Abs(fp(0) ^ 2 + fp(1) ^ 2 + fp(2) ^ 2 - afp ^ 2)): rfar = Sqr(Abs(fq(0) ^ 2 + fq(1) ^ 2 + fq(2) ^ 2 - afar ^ 2))
            rx = fp(0) - afp * UX: ry = fp(1) - afp * UY
            ' right hand about the direction of advance w = -U (into the part): (r x t) . w > 0
            hand = -(UX * (ry * fd(2) - fp(2) * fd(1)) + UY * (fp(2) * fd(0) - rx * fd(2)))
            good = Abs(afp - tipD) < 0.00001 And Abs(fp(2)) < 0.00001 And Abs(rfp - rM) < 0.00001 And Abs(afar - (tipD - heightM)) < 0.00001 And Abs(rfar - rWant) < 0.00002 And hand > 0
            Trace nm & ": helix try " & t & " (reversed " & rv & ", clockwise " & cw & ", taper out " & tOut & ", start " & Format(th(t Mod 8) * 57.2957795130823, "0.0") & " deg): face end " & Format(afp / IN_, "0.0000") & " along, z " & Format(fp(2) / IN_, "0.0000") & ", r " & Format(rfp / IN_, "0.0000") & "; far end " & Format(afar / IN_, "0.0000") & ", r " & Format(rfar / IN_, "0.0000") & " (want " & Format(rWant / IN_, "0.0000") & "); " & IIf(hand > 0, "right", "left") & " hand"
        Else
            Trace nm & ": helix try " & t & " made no helix curve" & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "")
        End If
        Err.Clear
        If good Then Exit For
        If Not hx Is Nothing Then
            swModel.ClearSelection2 True: hx.Select2 False, 0: swModel.Extension.DeleteSelection2 0
        End If
        Set hx = Nothing
    Next t
    Check nm & ": helix into the part, right hand, starting in the Front Plane on the end face " & Format(tipD / IN_, "0.0000") & " (radius " & Format(rM / IN_, "0.0000") & ")", good
    If good = False Then Exit Sub
    hx.Name = "HELIX_" & sfx
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = hx.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - heightM) < 0.000001 Then dm.Name = "HEIGHT"
        If Abs(dm.SystemValue - pitchM) < 0.000001 Then dm.Name = "PITCH"
        names = names & dm.Name & " "
        Set d = hx.GetNextDisplayDimension(d)
    Loop
    Check nm & " helix dims named (" & names & ")", InStr(names, "HEIGHT") > 0 And InStr(names, "PITCH") > 0
    ' --- tooth profile on the Front Plane (sketch coords = model X / Y) at the helix start: leg coords (a, q) -> (a*UX - q*UY, a*UY + q*UX)
    Dim a0 As Double, q0 As Double, sRad As Double, sApex As Double, half As Double, ap As Double
    a0 = afp: q0 = -fp(0) * UY + fp(1) * UX
    sRad = IIf(q0 >= 0, 1#, -1#): sApex = IIf(apexOut, sRad, -sRad): half = thdhM * Tan(3.14159265358979 / 6): ap = q0 + sApex * thdhM
    Trace nm & ": profile at a " & Format(a0 / IN_, "0.0000") & ", q " & Format(q0 / IN_, "0.0000") & ", apex " & Format(ap / IN_, "0.0000")
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    Dim hz As SldWorks.SketchSegment, ax As SldWorks.SketchSegment, pz As SldWorks.SketchSegment
    Dim l1 As SldWorks.SketchSegment, l1b As SldWorks.SketchSegment, l2 As SldWorks.SketchSegment, l3 As SldWorks.SketchSegment, lc As SldWorks.SketchSegment
    Dim LH As Double, LA As Double, LP As Double: LH = 0.5 * IN_: LA = 0.25 * IN_: LP = 0.25 * IN_
    swSkMgr.AddToDB = True
    Set hz = swSkMgr.CreateCenterLine(0, 0, 0, LH, 0, 0)
    Set ax = swSkMgr.CreateCenterLine(0, 0, 0, LA * UX, LA * UY, 0)
    Set pz = swSkMgr.CreateCenterLine(0, 0, 0, -LP * UY, LP * UX, 0)
    Set l1 = swSkMgr.CreateLine((a0 - half) * UX - q0 * UY, (a0 - half) * UY + q0 * UX, 0, a0 * UX - q0 * UY, a0 * UY + q0 * UX, 0)
    Set l1b = swSkMgr.CreateLine(a0 * UX - q0 * UY, a0 * UY + q0 * UX, 0, (a0 + half) * UX - q0 * UY, (a0 + half) * UY + q0 * UX, 0)
    Set l2 = swSkMgr.CreateLine((a0 + half) * UX - q0 * UY, (a0 + half) * UY + q0 * UX, 0, a0 * UX - ap * UY, a0 * UY + ap * UX, 0)
    Set l3 = swSkMgr.CreateLine(a0 * UX - ap * UY, a0 * UY + ap * UX, 0, (a0 - half) * UX - q0 * UY, (a0 - half) * UY + q0 * UX, 0)
    Set lc = swSkMgr.CreateLine(a0 * UX - q0 * UY, a0 * UY + q0 * UX, 0, a0 * UX - ap * UY, a0 * UY + ap * UX, 0)
    swSkMgr.AddToDB = False
    lc.ConstructionGeometry = True
    Dim n1 As SldWorks.SketchLine, n1b As SldWorks.SketchLine, n2 As SldWorks.SketchLine, n3 As SldWorks.SketchLine, nc As SldWorks.SketchLine
    Dim nh As SldWorks.SketchLine, na As SldWorks.SketchLine, np As SldWorks.SketchLine
    Set n1 = l1: Set n1b = l1b: Set n2 = l2: Set n3 = l3: Set nc = lc: Set nh = hz: Set na = ax: Set np = pz
    swModel.ClearSelection2 True: n1.GetEndPoint2.Select4 False, Nothing: n1b.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n1b.GetEndPoint2.Select4 False, Nothing: n2.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n2.GetEndPoint2.Select4 False, Nothing: n3.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n3.GetEndPoint2.Select4 False, Nothing: n1.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: nc.GetStartPoint2.Select4 False, Nothing: n1.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: nc.GetEndPoint2.Select4 False, Nothing: n2.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    ' construction frame: the three lines start on the origin; the reference line is horizontal; the axis line is held by its angle to it
    Dim cl3 As Variant, kq As Long: cl3 = Array(nh, na, np)
    For kq = 0 To 2
        swModel.ClearSelection2 True
        cl3(kq).GetStartPoint2.Select4 False, Nothing
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        swModel.SketchAddConstraints "sgCOINCIDENT"
    Next kq
    swModel.ClearSelection2 True: hz.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pz.Select4 False, Nothing: ax.Select4 True, Nothing: swModel.SketchAddConstraints "sgPERPENDICULAR"
    ' tooth: the HelixThread relation set, horizontal -> parallel to the axis line, vertical -> perpendicular to it
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: ax.Select4 True, Nothing: swModel.SketchAddConstraints "sgPARALLEL"
    swModel.ClearSelection2 True: l1b.Select4 False, Nothing: ax.Select4 True, Nothing: swModel.SketchAddConstraints "sgPARALLEL"
    swModel.ClearSelection2 True: lc.Select4 False, Nothing: ax.Select4 True, Nothing: swModel.SketchAddConstraints "sgPERPENDICULAR"
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: l1b.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    swModel.ClearSelection2 True: l2.Select4 False, Nothing: l3.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    ' constant frame dims (not table columns), then the table-driven PROF_AX / PROF_R / APEXR and the 60 deg tooth angle
    Call DimSegLenV(hz, "PHZL", LH, LH / 2, -0.1 * IN_, 0, -0.05 * IN_)
    Call DimSegLenV(ax, "PAXL", LA, LA / 2 * UX - 0.1 * IN_ * UY, LA / 2 * UY + 0.1 * IN_ * UX, -0.05 * IN_ * UY, 0.05 * IN_ * UX)
    Call DimSegLenV(pz, "PPZL", LP, -LP / 2 * UY + 0.1 * IN_ * UX, LP / 2 * UX + 0.1 * IN_ * UY, 0.05 * IN_ * UX, 0.05 * IN_ * UY)
    Set axisCL = ax: Set hzCL = hz
    Call DimAngLeg("PANG", 2.35619449019234, 0.16 * IN_ * Cos(1.17809724509617), 0.16 * IN_ * Sin(1.17809724509617))
    Dim tA As Double, tQ As Double
    tA = a0 - 0.5 * (a0 - 0): tQ = q0 + sRad * 0.15 * IN_
    Call DimPtLnV(n1.GetEndPoint2, pz, "PROF_AX", Abs(a0), tA * UX - tQ * UY, tA * UY + tQ * UX, 0.05 * IN_ * UX, 0.05 * IN_ * UY)
    tA = a0 + 0.12 * IN_: tQ = q0 / 2
    Call DimPtLnV(n1.GetEndPoint2, ax, "PROF_R", Abs(q0), tA * UX - tQ * UY, tA * UY + tQ * UX, 0.05 * IN_ * UX, 0.05 * IN_ * UY)
    tA = a0 - 0.12 * IN_: tQ = ap / 2
    Call DimPtLnV(n2.GetEndPoint2, ax, "APEXR", Abs(ap), tA * UX - tQ * UY, tA * UY + tQ * UX, -0.05 * IN_ * UX, -0.05 * IN_ * UY)
    Dim kk As Long, v As Double, qq As Double, aa As Double
    For kk = 0 To 5
        swModel.ClearSelection2 True
        l2.Select4 False, Nothing: l3.Select4 True, Nothing
        aa = a0 + IIf(kk >= 4, 0.003 * (kk - 4.5), 0): qq = q0 + sApex * thdhM * (1.6 - (kk Mod 2) * 2.4)
        Set dd = swModel.AddDimension2(aa * UX - qq * UY, aa * UY + qq * UX, 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - 3.14159265358979 / 3) < 0.001 Then Exit For
        DeleteDisp dd: Set dd = Nothing
    Next kk
    Check nm & " 60 deg tooth angle placed", (Not dd Is Nothing) And Abs(v - 3.14159265358979 / 3) < 0.001
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set pf = swModel.FeatureByPositionReverse(0): pf.Name = "THDPROF_" & sfx
    Check nm & " profile sketch fully defined", (pf.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' --- swept cut (left live)
    Dim vol0 As Double: vol0 = Volume()
    Dim swd As Object
    Set swd = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmSweepCut)
    If Not swd Is Nothing Then
        Set swd.Profile = pf: Set swd.Path = hx
        swModel.ClearSelection2 True
        pf.Select2 False, 1: hx.Select2 True, 4
        Set f = swFeatMgr.CreateFeature(swd)
        Trace nm & ": sweep CreateFeature -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    End If
    Check nm & " swept cut created", Not f Is Nothing
    If f Is Nothing Then Exit Sub
    f.Name = nm
    Dim vol1 As Double: vol1 = Volume()
    Check nm & " sweep removed material: " & Format((vol0 - vol1) / IN_ ^ 3, "0.00000") & " in^3", vol1 < vol0
    Dim bq As Variant
    bq = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bq) Then Check nm & ": one solid body after the thread", False Else Check nm & ": one solid body after the thread", (UBound(bq) = 0)
    Trace nm & ": left live until the final suppress step"
End Sub

Function Atan2V(ByVal y As Double, ByVal x As Double) As Double
    If Abs(x) < 1E-12 And Abs(y) < 1E-12 Then Atan2V = 0: Exit Function
    If Abs(x) < 1E-12 Then Atan2V = IIf(y > 0, 1.5707963267949, -1.5707963267949): Exit Function
    Atan2V = Atn(y / x)
    If x < 0 Then Atan2V = Atan2V + IIf(y >= 0, 3.14159265358979, -3.14159265358979)
End Function

Sub HelixUCheck(cfg As String, sfx As String, tipIn As Double, rIn As Double)
    ' per configuration: the thread on the 135-deg leg rebuilt live and its helix still starts in the Front Plane on the leg end face (table
    ' PROF_AX) on the thread radius (table HELIXDIA / 2) - a start that drifts out of the Front Plane would leave the tooth beside the helix
    On Error Resume Next
    Dim f As SldWorks.Feature, hx As SldWorks.Feature, egv As Object, cv As Object, cpd As Object, e0 As Variant, e1 As Variant, w As Boolean
    Dim a0 As Double, a1 As Double, fz As Double, af As Double, rf As Double, ec As Long
    swModel.ShowConfiguration2 cfg
    swModel.ForceRebuild3 False
    Set f = swModel.FeatureByName("THD_End" & sfx)
    Set hx = swModel.FeatureByName("HELIX_" & sfx)
    If f Is Nothing Or hx Is Nothing Then Check cfg & ": THD_End" & sfx & " and HELIX_" & sfx & " found", False: Exit Sub
    ec = f.GetErrorCode2(w)
    Check cfg & ": THD_End" & sfx & " live and rebuilt (error code " & ec & ")", (f.IsSuppressed = False) And (ec = 0)
    Set egv = hx.GetSpecificFeature2.GetFirstSegment
    If egv Is Nothing Then Check cfg & ": HELIX_" & sfx & " curve readable", False: Exit Sub
    Set cv = egv.GetCurve: Set cpd = egv.GetCurveParams3
    e0 = cv.Evaluate2(cpd.UMinValue, 0): e1 = cv.Evaluate2(cpd.UMaxValue, 0)
    a0 = e0(0) * UX + e0(1) * UY: a1 = e1(0) * UX + e1(1) * UY
    If Abs(a0 - tipIn * IN_) < Abs(a1 - tipIn * IN_) Then
        af = a0: fz = e0(2): rf = Sqr(Abs(e0(0) ^ 2 + e0(1) ^ 2 + e0(2) ^ 2 - a0 ^ 2))
    Else
        af = a1: fz = e1(2): rf = Sqr(Abs(e1(0) ^ 2 + e1(1) ^ 2 + e1(2) ^ 2 - a1 ^ 2))
    End If
    Check cfg & ": HELIX_" & sfx & " starts in the Front Plane on the end face (z " & Format(fz / IN_, "0.00000") & "; " & Format(af / IN_, "0.0000") & " along the leg, table " & Format(tipIn, "0.0000") & "; r " & Format(rf / IN_, "0.0000") & ", table " & Format(rIn, "0.0000") & ")", Abs(fz) < 0.00001 And Abs(af / IN_ - tipIn) < 0.0005 And Abs(rf / IN_ - rIn) < 0.0005
End Sub
'''
assert '\\\\' not in ANGLED_HELIX_HELP
NUTV_HELP = derive(HELP, 'NutHexCutAx', 'NutHexCutV', [
    ("    ' swivel nut hex: hexagon (across flats afM) sketched on the leg's nut face (normal to the current leg axis at tp), flats\n    ' normal to Z (vertex check in model coordinates, both sketch relations tried), OUTSIDE cut blind over depthM into the part",
     "    ' 2026-10-18 (ANGLED, Q-NEW-ANGLEDNUT): swivel nut hex on the 135-deg leg - hexagon (across flats afM) sketched on the nut face (normal to\n"
     "    ' the leg axis at tp along it), flats normal to Z (vertex check in model coordinates; horizontal, vertical, then a vertex on the Front\n"
     "    ' Plane), OUTSIDE cut blind over depthM into the part, accepted only when the cut's faces are centred on the nut (tp - depthM / 2)"),
    ('Dim tryRel As Long, relName As String, ok As Boolean, k As Long, zmax As Double', 'Dim tryRel As Long, relName As String, ok As Boolean, k As Long, zmax As Double, lnv As SldWorks.SketchLine'),
    ('    For tryRel = 0 To 1\n        If tryRel = 0 Then relName = "sgHORIZONTAL" Else relName = "sgVERTICAL"',
     '    For tryRel = 0 To 2\n        If tryRel = 0 Then relName = "sgHORIZONTAL" Else relName = "sgVERTICAL"\n        If tryRel = 2 Then relName = "vertex on the Front Plane"'),
    ('        ok = SelectEndFace(tp)', '        ok = SelectEndFaceV(tp)'),
    ('" on axis " & curAxis, ok', '" along the 135-deg leg", ok'),
    ('        For k = LBound(poly) To UBound(poly)\n            If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints relName: Exit For\n        Next k',
     '        If tryRel < 2 Then\n'
     '            For k = LBound(poly) To UBound(poly)\n                If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints relName: Exit For\n            Next k\n'
     '        Else\n'
     '            For k = LBound(poly) To UBound(poly)\n                If poly(k).GetType = swSketchSegments_e.swSketchLINE Then\n'
     '                    Set lnv = poly(k)\n                    lnv.GetStartPoint2.Select4 False, Nothing\n'
     '                    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, True, 0, Nothing, 0\n'
     '                    swModel.SketchAddConstraints "sgCOINCIDENT"\n                    Exit For\n                End If\n            Next k\n'
     '        End If'),
    ('Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long', 'Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long, cxF As Double'),
    ('            If v1 < v0 - 1E-12 Then Exit For',
     '            cxF = FeatCentreV(cut)\n'
     '            Trace featName & " attempt " & attempt & ": removed " & Format((v0 - v1) / (IN_ ^ 3), "0.00000") & " in^3, cut faces centred " & Format(cxF / IN_, "0.0000") & " along the 135-deg leg (want " & Format((tp - depthM / 2) / IN_, "0.0000") & ")"\n'
     '            If v1 < v0 - 1E-12 And Abs(cxF - (tp - depthM / 2)) < 0.25 * depthM Then Exit For'),
])
assert 'Sub NutHexCutV(' in NUTV_HELP and 'SelectEndFace(' not in NUTV_HELP.replace('SelectEndFaceV(', '')


def angled_help(sp, legs):
    """the 135 deg leg helpers a macro needs (none for every released root)"""
    if not sp.get('e45'): return ''
    U = [L for i, L in enumerate(legs, 1) if place(sp)[i][0] == 'U']
    out = ''
    if any((L['thread'] or {}).get('type') == 'HELIX' for L in U): out += ANGLED_HELIX_HELP
    if any(L['kind'] in ('JICSW', 'NPSMSW') for L in U): out += NUTV_HELP
    return out


def helixu_check(sp, legs, ok):
    """2026-10-18 (ANGLED, review fix 4): per configuration (every table row; never SolidWorks' Default) - the 135 deg leg's helical thread is live
    and rebuilt, and its helix starts in the Front Plane on the end face at the table's PROF_AX on the table's thread radius"""
    if not sp.get('e45'): return []
    us = [i for i, L in enumerate(legs, 1) if place(sp)[i][0] == 'U' and (L['thread'] or {}).get('type') == 'HELIX']
    if not us: return []
    out = ["    ' ---- 135-deg leg thread per configuration: live, rebuilt, helix start in the Front Plane at the table values (ANGLED 2026-10-18)",
           '    stepName = "135-deg thread check"']
    for i in us:
        for b in ok:
            c = b['cols']
            out.append(f'    Call HelixUCheck("{b["pn"]}", "{i}", {c[f"PROF_AX@THDPROF_{i}"]:.5f}, {c[f"HELIXDIA@HELIXSK_{i}"] / 2:.6f})')
    return out + ['']


def emit(root, hdr, ok, refrow):
    sp = SPEC[root]; legs = refrow['legs']; BR = refrow['BR']; AF = refrow['AF']; AC = refrow['AC']; PN = refrow['pn']
    cross = bool(sp.get('cross')); elbow = bool(sp.get('elbow')); n = len(legs)
    L = []
    # LoadLeg arrays
    ld = ['Sub LoadLeg(i As Long)', '    Dim v As Variant, k As Long']
    for i, lg in enumerate(legs, 1):
        per = 1 if len(lg['V']) <= 24 else 2      # VBA: at most 24 line continuations per statement (see gen_straight2.py)
        pts = ', _\n    '.join(', '.join(f'{x*IN:.9f}, {r*IN:.9f}' for x, r in lg['V'][k:k + per]) for k in range(0, len(lg['V']), per))
        ld.append(f'    If i = {i} Then v = Array( _\n    {pts})')
    ld += ['    NPTS = (UBound(v) + 1) \\ 2', '    ReDim PX(NPTS - 1): ReDim PR(NPTS - 1)', '    For k = 0 To NPTS - 1', '        PX(k) = v(2 * k): PR(k) = v(2 * k + 1)', '    Next k', 'End Sub', '']
    body = []
    e45 = bool(sp.get('e45'))
    if e45: body.append(f"    UX = {UXV:.15f}: UY = {UYV:.15f}      ' angled leg direction (135 deg from +X)")
    for i, lg in enumerate(legs, 1):
        if place(sp)[i][0] == 'U':
            body += emit_leg_u(i, lg); continue
        ax, sg = place(sp)[i]; M = lg.get('Mtip', lg['V'][-1][0]); swap = 'True' if ax == 1 else 'False'
        def pos(a, q):
            return (q, sg * a) if ax == 1 else (sg * a, q)
        body.append(f"    ' ================= LEG {i} ({lg['kind']} -{lg['dash']:02d}, along {'XY'[ax]} {'+' if sg > 0 else '-'}) =================")
        body.append(f'    stepName = "LEG{i} sketch"')
        body.append(f'    curAxis = {ax}: tipPos = {sg*M*IN:.9f}')
        body.append(f'    LoadLeg {i}')
        body.append('    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0')
        body.append('    swSkMgr.InsertSketch True')
        body.append(f'    DrawProfile {swap}, {sg}#')
        for d in lg['dims']:
            t = d[0]
            if t == 'len':
                _, s, nm, val, a, q = d; tx, ty = pos(a, q)
                body.append(f'    Call Dim_len({s}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
            elif t == 'rad':
                _, s, nm, val, a, q = d; tx, ty = pos(a, q)
                body.append(f'    Call Dim_rad({s}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
            elif t == 'ang':
                _, s, s2, nm, deg, a, q = d; tx, ty = pos(a, q)
                body.append(f'    Call Dim_ang({s}, {s2}, "{nm}", {math.radians(deg):.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
            elif t == 'ptl':
                _, s, ue, s2, nm, val, a, q = d; tx, ty = pos(a, q)
                body.append(f'    Call Dim_ptline({s}, {ue}, {s2}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
            elif t == 'col':
                body.append(f'    Call Collinear({d[1]}, {d[2]})')
            elif t == 'pair':
                _, s, s2, nm, val, a, q = d; tx, ty = pos(a, q)
                body.append(f'    Call Dim_pair({s}, {s2}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        body += ['    swModel.ClearSelection2 True', '    swSkMgr.InsertSketch True', '    Set swFeat = swModel.FeatureByPositionReverse(0)',
                 f'    swFeat.Name = "LEG{i}"',
                 f'    Check "LEG{i} sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)',
                 f'    stepName = "LEG{i} revolve"', '    swModel.ClearSelection2 True',
                 f'    swModel.Extension.SelectByID2 "LEG{i}", "SKETCH", 0, 0, 0, False, 0, Nothing, 0',
                 '    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16', '    axisCL.Select4 True, sd',
                 '    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)',
                 f'    Check "LEG{i} revolve created", Not rev Is Nothing', '    If rev Is Nothing Then GoTo Finish', f'    rev.Name = "LEG{i}_BODY"', '']
    # hex bars
    body.append("    ' ================= forged body: hex bars, A/F = 2*BODYR, flats normal to Z =================")
    if elbow:
        body.append('    stepName = "HEX1"')
        body.append(f'    Call HexArm("Right Plane", 0#, 0#, {legs[0]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX1", 0, 1#)')
        if e45:
            body.append('    stepName = "PLN2"')
            body.append(f'    MakeLegPlane "PLN2", {legs[1].get("Mtip", legs[1]["V"][-1][0])*IN:.9f}')     # 2026-10-18: a swivel's planar end is its nut face
            body.append('    stepName = "HEX2"')
            body.append(f'    Call HexArmV("PLN2", 0#, 0#, {legs[1]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX2", 0, 1#)')
        else:
            body.append('    stepName = "HEX2"')
            body.append(f'    Call HexArm("Top Plane", 0#, 0#, {legs[1]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX2", 1, 1#)')
        body.append(puck_vba(BR, AC))
        for i, lg in enumerate(legs, 1):
            if lg.get('trim'): body.append(neck_vba(i, lg))       # 2026-10-01 (NECK-6502)
            if lg.get('faceoff'): body.append(hoseface_vba(i, lg, e45))      # 2026-10-09 (HOSEB): face-off at the hose hex face
    else:
        body.append('    stepName = "RUN"')
        body.append(f'    Call HexRun("Right Plane", 0#, {legs[0]["hexl"]*IN:.9f}, {legs[1]["hexl"]*IN:.9f}, {BR*IN:.9f}, "RUN", 0)')
    if elbow:
        pass
    elif cross:
        body.append('    stepName = "RUN2"')
        body.append(f'    Call HexRun("Top Plane", 0#, {legs[2]["hexl"]*IN:.9f}, {legs[3]["hexl"]*IN:.9f}, {BR*IN:.9f}, "RUN2", 1)')
    else:
        body.append('    stepName = "HEX3"')
        body.append(f'    Call HexArm("Top Plane", 0#, 0#, {legs[2]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX3", 1, 1#)')
    for i, lg in enumerate(legs, 1):
        if lg['kind'] not in ('JICSW', 'NPSMSW'): continue
        ax, sg = place(sp)[i]
        if ax == 'U':
            # 2026-10-18 (ANGLED, Q-NEW-ANGLEDNUT): the swivel nut on the 135 deg leg
            body.append(f"    ' ================= swivel nut hex on leg {i} (135-deg leg): sketched on the nut face, flats normal to Z, cut over the nut hex length =================")
            body.append(f'    stepName = "NUTHEX{i}"')
            body.append(f'    tipPos = {lg["Mtip"]*IN:.9f}')
            body.append(f'    Call NutHexCutV(tipPos, {lg["nut_af"]*IN:.9f}, {lg["m"]["HEXL"]*IN:.9f}, "NUTHEX{i}", "NUTHEX{i}", "NUTCUT{i}")')
            body.append(f'    Check "NUTHEX{i}@NUTHEX{i} reachable", Not swModel.Parameter("NUTHEX{i}@NUTHEX{i}") Is Nothing')
            body.append(f'    Check "DEPTH@NUTCUT{i} reachable", Not swModel.Parameter("DEPTH@NUTCUT{i}") Is Nothing')
            continue
        body.append(f"    ' ================= swivel nut hex on leg {i}: sketched on the nut face, flats normal to Z, cut over the nut hex length =================")
        body.append(f'    stepName = "NUTHEX{i}"')
        body.append(f'    curAxis = {ax}: tipPos = {sg*lg["Mtip"]*IN:.9f}')
        body.append(f'    Call NutHexCutAx(tipPos, {lg["nut_af"]*IN:.9f}, {lg["m"]["HEXL"]*IN:.9f}, "NUTHEX{i}", "NUTHEX{i}", "NUTCUT{i}")')
        body.append(f'    Check "NUTHEX{i}@NUTHEX{i} reachable", Not swModel.Parameter("NUTHEX{i}@NUTHEX{i}") Is Nothing')
        body.append(f'    Check "DEPTH@NUTCUT{i} reachable", Not swModel.Parameter("DEPTH@NUTCUT{i}") Is Nothing')
    for i, lg in enumerate(legs, 1):
        if lg['kind'] != 'NWO': continue
        ax, sg = place(sp)[i]; assert ax != 'U', 'angled adjustable ORB legs not supported yet'
        nut = lg['nut']
        for j_, ov_ in lg.get('nut_overlap', {}).items():      # 2026-10-09 (PERLEGSW, DESIGN_REVIEW P11): the sliver both NUTCUT volume checks see
            assert ov_ < 0.005 * min(nwo_nut_removed(nut), nwo_nut_removed(legs[j_ - 1]['nut'])), (root, PN, f'NUTCUT{i} / NUTCUT{j_} envelope overlap {ov_:.6f} in^3 >= 0.5 %')
        body.append(f"    ' ================= adjustable ORB locknut on leg {i}: hexagon on the nut's inner face, flats normal to Z, cut outside over the nut thickness =================")
        body.append(f'    stepName = "NUTHEX{i}"')
        body.append(f'    curAxis = {ax}: tipPos = {sg*lg["V"][-1][0]*IN:.9f}')
        body.append(f'    Call NutHexCutNWO({sg*nut["n0"]*IN:.9f}, {nut["af"]*IN:.9f}, {nut["dep"]*IN:.9f}, "NUTHEX{i}", "NUTHEX{i}", "NUTCUT{i}", {sg}#, {nwo_nut_removed(nut)*IN**3:.12e})')
        body.append(f'    Check "NUTHEX{i}@NUTHEX{i} reachable", Not swModel.Parameter("NUTHEX{i}@NUTHEX{i}") Is Nothing')
        body.append(f'    Check "DEPTH@NUTCUT{i} reachable", Not swModel.Parameter("DEPTH@NUTCUT{i}") Is Nothing')
    orbtrims = [i for i in range(1, len(legs) + 1) if f'$STATE@ORBTRIM{i}' in refrow['cols']]
    for i in orbtrims:
        # 2026-10-01: corner neck trim (only where the table carries it): closed loop from the ORB body face through the neck and the locknut's
        # inner chamfer to the full nut corner, revolved as a CUT about the leg axis, sketched on the Front Plane. Drawn AFTER the locknut hex
        # cut: NUTCUTi stays sketched on the LEGi nut face (a later cut coincident with that face could take the face over in the trimmed sizes).
        lg = legs[i - 1]; ax, sg = place(sp)[i]
        assert (ax, sg) == (0, 1) and lg['kind'] == 'NWO', 'corner neck trim: adjustable ORB leg on +X only'
        pts, tv, live = lg['nwo_trim_pts'], lg['nwo_trim_vals'], lg['nwo_trim']
        rin = tv['NECKR'] if live else round(tv['NECKR'] - 0.25 * (tv['NECKR'] - lg['bore'] / 2), 5)   # creation only: below the neck
        P_ = [(pts[0][0], rin), (pts[1][0], rin)] + pts[2:]
        (x0, _), (x1, _), (_, rc), (x3, rn), (_, ro), _ = P_
        exp = 0.0 if live else math.pi * (tv['NECKR'] ** 2 - rin ** 2) * tv['NECKL']
        arr = ', '.join(f'{x*IN:.9f}, {r*IN:.9f}' for x, r in P_)
        body += [f"    ' ================= corner neck trim on leg {i} (adjustable ORB, 45-deg elbow): the forged corner beyond the ORB body face is cut back to the",
                 f"    '                   ORB neck and the locknut inner chamfer up to the full nut corner ($STATE@ORBTRIM{i}: {'live in the reference size' if live else 'built with a smaller inner radius, then suppressed - the reference size needs no trim'}) =================",
                 f'    stepName = "ORBTRIM{i} sketch"', '    curAxis = 0',
                 '    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0', '    swSkMgr.InsertSketch True',
                 f'    DrawLoopAx Array({arr}), {round(x3 + 0.1, 3)*IN:.9f}, "OT{i}_AXL"',     # axis centreline under the whole loop (as on the legs)
                 f'    Call DimSegOrigin(seg(5), "OT{i}_X0", {x0*IN:.9f}, {x0/2*IN:.6f}, {(ro+0.35)*IN:.6f})',
                 f'    Call Dim_len(0, "OT{i}_NECKL", {(x1-x0)*IN:.9f}, {(x0+x1)/2*IN:.6f}, {(ro+0.15)*IN:.6f})',
                 f'    Call Dim_rad(0, "OT{i}_NECKR", {rin*IN:.9f}, {(x0+x1)/2*IN:.6f}, {-0.25*IN:.6f})',
                 f'    Call Dim_len(1, "OT{i}_FACEH", {(rc-rin)*IN:.9f}, {(x1-0.12)*IN:.6f}, {(rin+rc)/2*IN:.6f})',
                 f'    Call Dim_pair(1, 3, "OT{i}_CHL", {(x3-x1)*IN:.9f}, {(x1+x3)/2*IN:.6f}, {(ro+0.25)*IN:.6f})',
                 f'    Call Dim_len(3, "OT{i}_TOPH", {(ro-rn)*IN:.9f}, {(x3+0.12)*IN:.6f}, {(rn+ro)/2*IN:.6f})',
                 f'    Call Dim_rad(4, "OT{i}_RO", {ro*IN:.9f}, {(x0+x3)/2*IN:.6f}, {-0.45*IN:.6f})',
                 '    swModel.ClearSelection2 True', '    swSkMgr.InsertSketch True', '    Set swFeat = swModel.FeatureByPositionReverse(0)',
                 f'    swFeat.Name = "ORBTRIM{i}_SK"',
                 f'    Check "ORBTRIM{i}_SK sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)',
                 f'    stepName = "ORBTRIM{i} cut"',
                 f'    Call OrbTrimCut("ORBTRIM{i}_SK", "ORBTRIM{i}", {live}, {exp*IN**3:.12e})',
                 f'    Check "OT{i}_NECKR@ORBTRIM{i}_SK reachable", Not swModel.Parameter("OT{i}_NECKR@ORBTRIM{i}_SK") Is Nothing']
    body += ['    Dim bodies As Variant', '    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)',
             '    If IsEmpty(bodies) Then Check "One solid body after legs+hex", False Else Check "One solid body after legs+hex", (UBound(bodies) = 0)', '']
    # pockets & bores
    body.append("    ' ================= pockets and bores (each from its leg face to the axis crossing) =================")
    body.append('    stepName = "Bores"')
    cols = refrow['cols']
    for i, lg in enumerate(legs, 1):
        ax, sg = place(sp)[i]; M = lg.get('Mtip', lg['V'][-1][0])
        if ax == 'U':
            body.append(f'    tipPos = {M*IN:.9f}')
            if lg['kind'] == 'NPTFF':
                # 2026-10-18 (ANGLED, Q-NEW-ANGLEDFEMALE): female port on the 135 deg leg = the axis-leg pocket / connecting bore, cut from the port face
                body.append(f'    Call BoreCutV("POCKET{i}", "TAPDRILL{i}", {lg["td"]*IN:.9f}, {cols[f"DEPTH@POCKETCUT{i}"]*IN:.9f}, 0#, "POCKETCUT{i}", True, {BR*0.9*IN:.9f})')
                if not lg['to_centre']:
                    body.append(f'    Call BoreCutV("BORE{i}", "D{i}", {lg["conn"]*IN:.9f}, {M*IN:.9f}, 0#, "BORECUT{i}", True, {BR*0.9*IN:.9f})')
                continue
            body.append(f'    Call BoreCutV("BORE{i}", "D{i}", {lg["bore"]*IN:.9f}, {M*IN:.9f}, 0#, "BORECUT{i}", True, {lg["tipR"]*0.9*IN:.9f})')
            continue
        body.append(f'    curAxis = {ax}: tipPos = {sg*M*IN:.9f}')
        if lg['kind'] == 'NPTFF':
            body.append(f'    Call BoreCut("POCKET{i}", "TAPDRILL{i}", {lg["td"]*IN:.9f}, {cols[f"DEPTH@POCKETCUT{i}"]*IN:.9f}, 0#, "POCKETCUT{i}", True, {BR*0.9*IN:.9f})')
            if not lg['to_centre']:
                body.append(f'    Call BoreCut("BORE{i}", "D{i}", {lg["conn"]*IN:.9f}, {M*IN:.9f}, 0#, "BORECUT{i}", True, {BR*0.9*IN:.9f})')
        else:
            body.append(f'    Call BoreCut("BORE{i}", "D{i}", {lg["bore"]*IN:.9f}, {M*IN:.9f}, 0#, "BORECUT{i}", True, {lg["tipR"]*0.9*IN:.9f})')
    for i, lg in enumerate(legs, 1):
        ax, sg = place(sp)[i]; M = lg.get('Mtip', lg['V'][-1][0])
        if ax == 'U':
            body.append(f'    Check "leg {i} bore open on the axis at its face ({M:.4f} along the 135-deg leg)", Not AxisCoveredV({M*IN:.9f})')
            # 2026-10-18 (ANGLED): the same open-axis checks as on the axis legs, along the 135 deg leg
            if lg['kind'] == 'NPSMSW':
                body.append(f'    Check "leg {i} bore runs through the NPSM stem tip (no face across the axis at the stem-tip plane {M - lg["s_tip"]:.4f} along the 135-deg leg)", Not AxisCoveredV({(M - lg["s_tip"])*IN:.9f})')
            if lg['kind'] == 'JICSW':
                body.append(f'    Check "leg {i} bore reaches the swivel seat (no face across the axis at the nose-tip plane {M - lg["s_nt"]:.4f} along the 135-deg leg)", Not AxisCoveredV({(M - lg["s_nt"])*IN:.9f})')
            if lg['kind'] == 'NPTFF' and not lg['to_centre']:
                body.append(f'    Check "leg {i} bore open through the pocket bottom ({M - lg["pocket"]:.4f} along the 135-deg leg)", Not AxisCoveredV({(M - lg["pocket"])*IN:.9f})')
            continue
        body.append(f'    curAxis = {ax}: Check "leg {i} bore open on the axis at its face ({"XY"[ax]}={sg*M:+.4f})", Not AxisCoveredAx({sg*M*IN:.9f})')
        if lg['kind'] == 'NPSMSW':
            xs_ = sg * (M - lg['s_tip'])
            body.append(f'    curAxis = {ax}: Check "leg {i} bore runs through the NPSM stem tip (no face across the axis at the stem-tip plane {"XY"[ax]}={xs_:+.4f})", Not AxisCoveredAx({xs_*IN:.9f})')
        if lg['kind'] == 'JICSW':
            xs_ = sg * (M - lg['s_nt'])
            body.append(f'    curAxis = {ax}: Check "leg {i} bore reaches the swivel seat (no face across the axis at the nose-tip plane {"XY"[ax]}={xs_:+.4f})", Not AxisCoveredAx({xs_*IN:.9f})')
        if lg['kind'] == 'NPTFF' and not lg['to_centre']:
            xb = sg * (M - lg['pocket'])
            body.append(f'    curAxis = {ax}: Check "leg {i} bore open through the pocket bottom ({"XY"[ax]}={xb:+.4f})", Not AxisCoveredAx({xb*IN:.9f})')
    body.append('')
    # threads
    body.append("    ' ================= threads (left live until the final resting-state step) =================")
    body.append('    stepName = "Threads"')
    for i, lg in enumerate(legs, 1):
        ax, sg = place(sp)[i]; M = lg.get('Mtip', lg['V'][-1][0]); t = lg['thread']
        if t is None: continue          # 2026-10-09 (HOSEB): the hose leg carries no thread; 2026-10-18 (flange): flange leg - no thread
        if ax == 'U':
            body.append(f'    tipPos = {M*IN:.9f}')
            if t['type'] == 'HELIX':
                # 2026-10-18 (ANGLED, Q-NEW-ANGLEDHELIX): helical thread about the 135 deg axis (male / female NPTF, swivel-nut thread)
                body.append(f'    Call HelixThreadV({M*IN:.9f}, {t["r"]*IN:.9f}, {t["height"]*IN:.9f}, {t["pitch"]*IN:.9f}, {t["thdh"]*IN:.9f}, {t.get("taper", TAPER):.9f}, {t["taperOut"]}, {t["apexOut"]}, "{i}", "THD_End{i}")')
                continue
            body.append(f'    Call ThreadCutV({t["ex"]*IN:.9f}, {t["er"]*IN:.9f}, {t["depth"]*IN:.9f}, "{t["size"]}", "THD_End{i}", 1#, {t["pitch"]*IN:.9f})')
            continue
        body.append(f'    curAxis = {ax}: tipPos = {sg*M*IN:.9f}')
        if t['type'] == 'CUT':
            body.append(f'    Call ThreadCut({sg*t["ex"]*IN:.9f}, {t["er"]*IN:.9f}, {t["depth"]*IN:.9f}, "{t["size"]}", "THD_End{i}", {sg}#, {t["pitch"]*IN:.9f})')
        else:
            body.append(f'    Call HelixThread({sg*M*IN:.9f}, {t["r"]*IN:.9f}, {t["height"]*IN:.9f}, {t["pitch"]*IN:.9f}, {t["thdh"]*IN:.9f}, {t.get("taper", TAPER):.9f}, {t["taperOut"]}, {t["apexOut"]}, "{i}", "THD_End{i}")')
    body.append('')
    # self-checks
    zexp = BR
    if elbow:
        Mt = lambda lg: lg.get('Mtip', lg['V'][-1][0])
        xmax = Mt(legs[0]); xmin = -AC; ymax = Mt(legs[1]); ymin = -AC
        # a male NPTF end may stand proud of the flats (Brennan 5600-16 STEP) - then it sets the Z extent
        # (2026-09-25: + JICBH - the bulkhead collar stands proud of the hex flats, 2701/2702/2704 Z extent 0.44 vs 0.375)
        zexp = max([BR] + [lg['rmax'] for lg in legs if lg['kind'] in ('NPTFM', 'JICSW', 'NPSMSW', 'NWO', 'JICBH', 'HOSEB')])
        if legs[0]['kind'] == 'HOSEB': ymin = -max(AC, legs[0]['rA'])            # 2026-10-09 (HOSEB): the bead around the +X hose leg
        if legs[1]['kind'] == 'HOSEB' and not e45: xmin = -max(AC, legs[1]['rA'])
        # an adjustable ORB leg's washer / locknut corners reach past the corner puck across the other axis
        if legs[1]['kind'] == 'NWO' and not e45: xmin = -max(AC, nwo_radial(legs[1]))
        if legs[0]['kind'] == 'NWO': ymin = -max(AC, nwo_radial(legs[0]))
        # a swivel nut's hex corners (flats normal to Z) lie on the other in-plane axis (2026-09-25: 6500 X -0.722 vs -0.613)
        if legs[1]['kind'] in ('JICSW', 'NPSMSW') and not e45: xmin = min(xmin, -legs[1]['nut_af'] / math.sqrt(3))
        if legs[0]['kind'] in ('JICSW', 'NPSMSW'): ymin = min(ymin, -legs[0]['nut_af'] / math.sqrt(3))
        # 2026-10-18: a flange head stands past the corner puck across the other in-plane axis, and may stand past the hex flats in Z
        zexp = max([zexp] + [lg['rmax'] for lg in legs if lg['kind'] in FLG_KINDS])
        if legs[0]['kind'] in FLG_KINDS: ymin = min(ymin, -legs[0]['rmax'])
        if legs[1]['kind'] in FLG_KINDS and not e45: xmin = min(xmin, -legs[1]['rmax'])
    else:
        Mt = lambda lg: lg.get('Mtip', lg['V'][-1][0])
        xmax = Mt(legs[0]); xmin = -Mt(legs[1]); ymax = Mt(legs[2]); ymin = -Mt(legs[3]) if cross else -AC
        zexp = max([BR] + [lg['rmax'] for lg in legs if lg['kind'] in ('JICSW', 'NPSMSW', 'NWO', 'JICBH')])
        # a swivel nut on the run: its hex corners lie on +/-Y, below the body (2026-09-25)
        for lg in legs[:2]:
            if lg['kind'] in ('JICSW', 'NPSMSW') and not cross: ymin = min(ymin, -lg['nut_af'] / math.sqrt(3))
        if any(lg['kind'] == 'NWO' for lg in legs[:2]): ymin = -max([ymin * -1] + [nwo_radial(lg) for lg in legs[:2] if lg['kind'] == 'NWO'])
        if len(legs) > 2 and legs[2]['kind'] == 'NWO': xmin = min(xmin, -nwo_radial(legs[2])); xmax = max(xmax, nwo_radial(legs[2]))
    zlab = 'hex flats' if zexp == BR else 'swivel nut flats' if any(lg['kind'] in ('JICSW', 'NPSMSW') and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs) else \
        'adjustable ORB washer' if any(lg['kind'] == 'NWO' and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs) else \
        'bulkhead collar' if any(lg['kind'] == 'JICBH' and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs) else \
        'hose bead' if any(lg['kind'] == 'HOSEB' and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs) else 'male pipe end proud of the flats'
    if zexp != BR and any(lg['kind'] in FLG_KINDS and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs): zlab = 'flange head'     # 2026-10-18
    if e45:
        m1 = legs[0].get('Mtip', legs[0]['V'][-1][0]); m2 = legs[1].get('Mtip', legs[1]['V'][-1][0])
        body += ['    stepName = "Self-checks"', '    Dim bb As Variant, ex1 As Double, ex2 As Double',
                 '    ex1 = ExtremeAlong(1#, 0#, 0#): ex2 = ExtremeAlong(UX, UY, 0#)',
                 f'    Check "leg 1 tip (exact) " & Format(ex1 / IN_, "0.0000") & " along +X (expect {m1:.4f})", Abs(ex1 / IN_ - {m1:.4f}) < 0.001',
                 f'    Check "leg 2 tip (exact) " & Format(ex2 / IN_, "0.0000") & " along the 135-deg leg (expect {m2:.4f})", Abs(ex2 / IN_ - {m2:.4f}) < 0.001',
                 '    Dim zlo As Double, zhi As Double: zhi = ExtremeAlong(0#, 0#, 1#): zlo = -ExtremeAlong(0#, 0#, -1#)',
                 f'    Check "Z extent (exact) " & Format(zlo / IN_, "0.0000") & " .. " & Format(zhi / IN_, "0.0000") & " (expect {-zexp:.4f} .. {zexp:.4f}: {zlab})", Abs(zlo / IN_ + {zexp:.4f}) < 0.001 And Abs(zhi / IN_ - {zexp:.4f}) < 0.001',
                 '    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)',
                 '    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body", (UBound(bodies) = 0)', '']
    else:
      body += ['    stepName = "Self-checks"', '    Dim bb As Variant', '    bb = swModel.GetPartBox(True)',
             f'    Check "X extent " & Format(bb(0) / IN_, "0.000") & " .. " & Format(bb(3) / IN_, "0.000") & " (expect {xmin:.3f} .. {xmax:.3f}; threads may add a little)", Abs(bb(3) / IN_ - {xmax:.4f}) < 0.08 And Abs(bb(0) / IN_ - ({xmin:.4f})) < 0.08',
             f'    Check "Y extent " & Format(bb(1) / IN_, "0.000") & " .. " & Format(bb(4) / IN_, "0.000") & " (expect {ymin:.3f} .. {ymax:.3f})", Abs(bb(4) / IN_ - {ymax:.4f}) < 0.08 And Abs(bb(1) / IN_ - ({ymin:.4f})) < 0.08',
             '    Trace "Bounding box z " & Format(bb(2) / IN_, "0.000") & " .. " & Format(bb(5) / IN_, "0.000") & " (approximate - loose around thread faces)"',
             '    Dim zlo As Double, zhi As Double: zhi = ExtremeAlong(0#, 0#, 1#): zlo = -ExtremeAlong(0#, 0#, -1#)',
             f'    Check "Z extent (exact) " & Format(zlo / IN_, "0.0000") & " .. " & Format(zhi / IN_, "0.0000") & " (expect {-zexp:.4f} .. {zexp:.4f}: {zlab})", Abs(zlo / IN_ + {zexp:.4f}) < 0.001 And Abs(zhi / IN_ - {zexp:.4f}) < 0.001',
             '    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)',
             '    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body", (UBound(bodies) = 0)', '']
    # design table + config check
    params = [c for c in hdr if '@' in c and not c.startswith('$') and c.split('@')[1].startswith(('LEG',))][:6] + \
             [c for c in hdr if c.startswith(('HEXAF@', 'HEXL', 'PUCK_XC@', 'PUCK_R1B@', 'THDPITCH@', 'Profile_Height@', 'PROF_R@', 'DEPTH@BORECUT', 'DEPTH@POCKETCUT', 'TRIM_', 'FILL_'))
              or c.split('@')[-1].startswith(('HFPLN', 'HOSEFACE', 'STUBFILL'))]      # 2026-10-09 (HOSEB): the face-off values land per configuration
    cfgs = [(ok[1]['pn'], [ok[1]['cols'][p] for p in params]), (ok[-1]['pn'], [ok[-1]['cols'][p] for p in params])] if len(ok) > 2 else [(ok[-1]['pn'], [ok[-1]['cols'][p] for p in params])]
    # 2026-10-01 (NECK-6502): also spot-check the configuration where the neck turn takes the most of the corner (if it is not already listed)
    cut_ = [(max(L['trim']['reach'] - L['trim']['r'] for L in b['legs'] if L.get('trim')), b) for b in ok if any(L.get('trim') for L in b['legs'])]
    cut_ = [cb for cb in cut_ if cb[0] > 0 and cb[1]['pn'] not in [c_[0] for c_ in cfgs]]
    if cut_:
        b_ = max(cut_, key=lambda cb: cb[0])[1]
        cfgs.insert(1, (b_['pn'], [b_['cols'][p] for p in params]))
    blk = sp3.check_block(cfgs, params)
    blk = blk.replace('Format(cx_prm.SystemValue / IN_, "0.0000")', 'Format(cx_v, "0.0000")').replace('Abs(cx_prm.SystemValue / IN_ - cx_w(cx_q)(cx_k))', 'Abs(cx_v - cx_w(cx_q)(cx_k))')
    blk = blk.replace('            Else\n                Check cx_c(cx_q)', '            Else\n                cx_v = IIf(InStr(cx_p(cx_k), "TAPER") > 0 Or InStr(cx_p(cx_k), "ANG") > 0 Or InStr(cx_p(cx_k), "SEATB") > 0, cx_prm.SystemValue * 180 / 3.14159265358979, cx_prm.SystemValue / IN_)\n                Check cx_c(cx_q)')
    blk = blk.replace('Dim cx_c As Variant,', 'Dim cx_v As Double, cx_c As Variant,')
    assert 'cx_v = IIf' in blk
    table_path = DEV + f'\\04_DESIGN_TABLES\\DesignTable_{root}_SW2.xlsx'
    body += ['    stepName = "Design table"', '    swModel.ClearSelection2 True', '    Dim ok As Boolean',
             '    ok = swModel.InsertFamilyTableOpen(TABLE_PATH)', '    Check "Design table inserted from " & TABLE_PATH, ok', '    swModel.CloseFamilyTable',
             '    swModel.ForceRebuild3 False', '    Dim cfgs As Variant', '    cfgs = swModel.GetConfigurationNames',
             f'    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect {len(ok) + 1})", (UBound(cfgs) + 1) = {len(ok) + 1}',
             blk] + orbtrim_check(orbtrims, ok) + helixu_check(sp, legs, ok) + [f'    swModel.ShowConfiguration2 "{PN}"', '    swModel.ForceRebuild3 False', '']
    body.append(SWEEP)
    entry = f'Build{root}'
    ranks = ', '.join(f'{lg["kind"]} -{lg["dash"]:02d}' for lg in legs)
    vba = f'''Attribute VB_Name = "Build_{root}_MASTER"
' ============================================================================
'  Build_{root}_MASTER.bas  -  OMi fitting library, generated {TODAY} by gen_tee.py
'  {sp['name']} ({'45-deg elbow' if e45 else 'elbow' if elbow else 'cross' if cross else 'tee'}), forged hex body ({'Brennan 2504 / 2500HX' if e45 else '2500HX' if elbow else '2603HX'} pattern).  Reference config {PN}: {ranks}
'  Entry: Sub {entry}.  {'Leg 1 along +X, leg 2 along the 135-deg direction (45-deg elbow); hex arms HEX1 / HEX2 (on plane PLN2) + 30deg corner PUCK about Z' + (' + swivel neck turn NECKTRIM1 / NECKFILL1' if any(lg.get('trim') for lg in legs) else '') if e45 else 'Leg 1 along +X, leg 2 along +Y; hex arms HEX1/HEX2 + 30deg corner PUCK about Z' if elbow else 'Legs 1/2 along +X/-X, leg 3 along +Y' + (', leg 4 along -Y' if cross else '')}.
'  Builds from DesignTable_{root}_SW2.xlsx, runs self-checks + an all-configuration rebuild sweep with the
'  threads LIVE, then suppresses every THD_ feature in every configuration and saves to 11_MASTERS.
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "{table_path}"
Const SAVE_PATH  As String = "{DEV}\\11_MASTERS\\{root}_MASTER.SLDPRT"
Const REPORT_PATH As String = "{DEV}\\03_SCRIPTS\\Build_{root}_report.txt"
Const SUPPRESS_THREADS As Boolean = False      ' threads stay live through the checks; the final step suppresses them

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim seg() As SldWorks.SketchSegment
Dim axisCL As SldWorks.SketchSegment
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String
Dim curAxis As Long          ' 0 = leg along X, 1 = leg along Y
Dim tipPos As Double         ' signed position of the current leg's tip face on its axis (m)
Dim hexAnchor As SldWorks.SketchPoint
Dim UX As Double, UY As Double   ' direction of an angled leg (45-deg elbows)
Dim hzCL As SldWorks.SketchSegment
Dim NPTS As Long
Dim PX() As Double, PR() As Double

{chr(10).join(ld)}
Sub {entry}()
    Set swApp = Application.SldWorks
    swApp.SetUserPreferenceToggle swUserPreferenceToggle_e.swInputDimValOnCreate, False
    Dim tpl As String
    tpl = swApp.GetUserPreferenceStringValue(swUserPreferenceStringValue_e.swDefaultTemplatePart)
    Set swModel = swApp.NewDocument(tpl, 0, 0, 0)
    If swModel Is Nothing Then MsgBox "Could not create a new part - check the default part template.": Exit Sub
    swModel.Extension.SetUserPreferenceInteger swUserPreferenceIntegerValue_e.swUnitSystem, swUserPreferenceOption_e.swDetailingNoOptionSpecified, swUnitSystem_e.swUnitSystem_IPS
    Set swSkMgr = swModel.SketchManager
    Set swFeatMgr = swModel.FeatureManager
    Set swSelMgr = swModel.SelectionManager
    report = "": nErr = 0
    fnRep = FreeFile
    Open REPORT_PATH For Output As #fnRep
    Print #fnRep, "Build_{root}_MASTER  " & Now
    On Error GoTo Trap
    Dim swFeat As SldWorks.Feature, rev As SldWorks.Feature, sd As SldWorks.SelectData

{chr(10).join(body)}
    stepName = "Save"
    Dim e As Long, w As Long, alt As String
    ok = swModel.Extension.SaveAs(SAVE_PATH, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
    Trace "SaveAs " & SAVE_PATH & " -> " & ok & " (error " & e & ", warning " & w & ")"
    If ok Then
        Check "Saved to " & SAVE_PATH, True
    Else
        ' the fixed name is usually locked by an open copy - never lose the build: save beside it with a time stamp
        alt = Replace(SAVE_PATH, ".SLDPRT", "_" & Format(Now, "hhnnss") & ".SLDPRT")
        ok = swModel.Extension.SaveAs(alt, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
        Check "Saved to " & alt & " (fixed name was locked - close the open copy and rename this file; error " & e & ")", ok
    End If

Finish:
    On Error Resume Next
    Close #fnRep
    MsgBox "Build_{root}_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Full report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
    Exit Sub
Trap:
    Check "RUNTIME ERROR during '" & stepName & "' at line " & Erl & ": " & Err.Number & " - " & Err.Description, False
    Resume Next
End Sub

' ---------------------------------------------------------------- helpers (2603HX library + straights HelixThread)
{HELP}{NWO_HELP if any(lg['kind'] == 'NWO' for lg in legs) else ''}{ORBTRIM_HELP if orbtrims else ''}{NECK_HELP if any(lg.get('trim') for lg in legs) else ''}{HOSEFACE_HELP if any(lg.get('faceoff') for lg in legs) else ''}{angled_help(sp, legs)}'''
    vba = ref_config_at_save(add_progress(vba))      # 2026-09-24: one report/status-bar line per configuration in the sweep; 2026-09-25: saved in the reference configuration (progress_patch.py)
    p = f'{OUT}/Build_{root}_MASTER.bas'; open(p, 'w').write(vba)
    return p


if __name__ == '__main__':
    summary = {}
    for root in sys.argv[1:]:
        built, skipped = build_rows(root)
        if not [b for b in built if not b['chk']]:
            # 2026-10-09 (wave-1 polish): no buildable row - report and go on, as gen_straight2 does (was an IndexError in write_sw2)
            blocked = [b['pn'] + ': ' + '; '.join(b['chk']) for b in built if b['chk']]
            summary[root] = dict(configs=0, ref=None, skipped=skipped, blocked=blocked, warnings=[], cols=0)
            print(f"{root}: 0 configs - nothing to build ({len(skipped)} skipped, {len(blocked)} blocked); no macro / table written")
            for b in blocked: print('   BLOCKED', b)
            continue
        if SPEC[root].get('pilot'): pilot_rows(root, built)        # 2026-10-02 PIPE-TEES: $PRP@AxialSource of the pilot-measured roots
        hdr, ok, refrow = write_sw2(root, built)
        emit(root, hdr, ok, refrow)
        blocked = [b['pn'] + ': ' + '; '.join(b['chk']) for b in built if b['chk']]
        warns = [b['pn'] + ': ' + '; '.join(b['warn']) for b in ok if b['warn']]
        summary[root] = dict(configs=len(ok), ref=refrow['pn'], skipped=skipped, blocked=blocked, warnings=warns, cols=len(hdr))
        print(f"{root}: {len(ok)} configs (ref {refrow['pn']}), {len(skipped)} skipped, {len(blocked)} blocked, {len(hdr)} cols")
        for b in blocked: print('   BLOCKED', b)
        for w in warns: print('   warn', w)
    json.dump(summary, open(f'{OUT}/gen_tee_summary.json', 'w'), indent=1)
