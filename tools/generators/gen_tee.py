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
    '1503': dict(name='45 deg Male Pipe x Female NPSM Swivel Elbow', hex='C1HEX@HEX', elbow=True, e45=True, dmap=(1, 0), ref='1503-08-08-FG', npsm=('W2@HEX', 'CHEX@HEX'),
                 legs=[('NPSMSW', 'M@DRIVE', 'D@BORE', 'THDMAJ_A1@DRIVE'), ('NPTFM', 'N@DRIVE', 'D2@BORE', 'THDMAJ_A@DRIVE')]),
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


def neck_trim_leg(sp, i, L):
    """legs that carry the NECKTRIM / NECKFILL turn: a female JIC swivel on the +X leg of a 45 deg elbow (6502)"""
    return bool(sp.get('e45')) and L['kind'] == 'JICSW' and place(sp)[i] == (0, +1)


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
        pn = r['$PRP@PartNo']
        if r.get('$PRP@ScopeAction') != 'BUILD' or r['$PRP@DataStatus'] == 'MISSING':
            skipped.append((pn, r.get('$PRP@ScopeAction'), r['$PRP@DataStatus'])); continue
        dd = dashes(pn)
        if sp.get('dmap') and len(dd) == len(sp['dmap']): dd = [dd[k] for k in sp['dmap']]
        chk, warn = [], []
        if len(dd) != nleg: skipped.append((pn, 'dash count', dd)); continue
        swd = [d for (kind, lc, bc, tc), d in zip(sp['legs'], dd) if kind == 'JICSW']
        # 2026-10-01: the measured sizes are read from the tables (the fixed texts "-04/-08/-12/-16 only" / "-08 only" were stale since batch 13)
        _have = lambda tab: '/'.join(f'-{k:02d}' for k in sorted(tab))
        if swd and swd[0] not in G.SWIV_MEAS:
            skipped.append((pn, 'no end data', f'female JIC swivel end not measured for -{swd[0]:02d} (SWIV_MEAS has {_have(G.SWIV_MEAS)}; needs a Brennan STEP carrying a -{swd[0]:02d} JIC swivel)')); continue
        npd = [d for (kind, lc, bc, tc), d in zip(sp['legs'], dd) if kind == 'NPSMSW']
        if npd and npd[0] not in G.NPSM_MEAS:
            skipped.append((pn, 'no end data', f'female NPSM swivel end not measured for -{npd[0]:02d} (NPSM_MEAS has {_have(G.NPSM_MEAS)})')); continue
        nwd = [d for (kind, lc, bc, tc), d in zip(sp['legs'], dd) if kind == 'NWO' and d not in NWO_MEAS]
        if nwd:
            skipped.append((pn, 'no end data', f'adjustable ORB end not measured for -{nwd[0]:02d}')); continue
        # SIZE-40 (2026-10-01): a leg dash missing from an end library (e.g. -40 NPTF) -> skip the row with the source that would fill it
        # (until now an uncaught KeyError here stopped the whole root)
        gaps = G.lib_gaps([(kind, d) for (kind, lc, bc, tc), d in zip(sp['legs'], dd)])
        if gaps:
            skipped.append((pn, 'no end data', '; '.join(gaps))); continue
        # the leg threads must be the ones the part number says
        for (kind, lc, bc, tc), d in zip(sp['legs'], dd):
            if tc is None: continue
            tm = r[tc]
            want = G.JIC[d]['TM'] if kind in ('JICM', 'JICBH', 'JICSW', 'NWO') else G.NPTF[d][2]
            if tm is None or abs(tm - want) > 1e-3: chk.append(f'{tc} {tm} does not match the -{d:02d} end ({want})')
        Y = r[sp['hex']]
        # 2603HX rule: A/F = max(Air-Way hex, JIC thread majors) - the JIC nipple keeps its relief below the flats
        maxes = [G.JIC[d]['TM'] for (kind, lc, bc, tc), d in zip(sp['legs'], dd) if kind in ('JICM', 'JICBH')]
        AF = max([Y] + maxes); BR = AF / 2
        if AF > Y + 1e-9: warn.append(f'hex A/F raised from Air-Way {Y} to {AF:.4f} (JIC thread major; 2603HX rule)')
        # male NPTF: the thread cylinder at its vanish point (radius rL) must sit inside the hex flats with a real shoulder
        for i, ((kind, lc, bc, tc), d) in enumerate(zip(sp['legs'], dd), 1):
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
        for i, ((kind, lc, bc, tc), d) in enumerate(zip(sp['legs'], dd), 1):
            M = r[lc]
            if kind == 'JICM': L = leg_JICM(i, d, M, BR)
            elif kind == 'JICBH':
                try: L = leg_JICBH(i, d, M, BR, r[sp['bh'][0]], r[sp['bh'][1]], r[sp['bh'][2]])
                except AssertionError as ex: chk.append(f'leg {i} bulkhead: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind == 'NPTFM': L = leg_NPTFM(i, d, M, BR)
            elif kind == 'JICSW':
                try: L = leg_JICSW(i, d, M, BR, r[sp['sw'][0]], r[sp['sw'][1]])
                except AssertionError as ex: chk.append(f'leg {i} swivel: {ex}'); L = leg_JICM(i, d, M, BR)
            elif kind == 'NPSMSW':
                try: L = leg_NPSMSW(i, d, M, BR, r[sp['npsm'][0]], r[sp['npsm'][1]])
                except (AssertionError, KeyError) as ex: chk.append(f'leg {i} NPSM swivel: {ex}'); L = leg_NPTFM(i, d, M, BR)
            elif kind == 'NWO':
                try:
                    i3c = sp['nwo'][0]
                    I3 = nwo_i3_from(i3c[1:], d) if i3c.startswith('=') else r[i3c]
                    if i3c.startswith('='): warn.append(f'leg {i}: adjustable ORB tip-to-body-face {I3} = Air-Way {i3c[1:]} ORB_I3 for -{d:02d} (= Brennan 6801 STEP; not printed for this series - ASSUMPTION)')
                    L = leg_NWO(i, d, M, BR, I3, r[sp['nwo'][1]], r[sp['nwo'][2]], r[sp['nwo'][3]])
                except (AssertionError, KeyError, TypeError) as ex: chk.append(f'leg {i} adjustable ORB: {ex}'); L = leg_JICM(i, d, M, BR)
            elif sp.get('p1'):
                # 2026-10-02: the row's own measured port thread length where it has one, else the MS51503 P1 library value (said in $COMMENT)
                p1_ = r.get(sp['p1'])
                if p1_ is None: warn.append(f'leg {i}: female port thread length = MS51503 P1 {G.FPT[d]["P1"]} (library) - the row has no measured {sp["p1"]}')
                L = leg_NPTFF(i, d, M, BR, r[bc], conn, split=bool(sp.get('elbow')), p1=p1_)
            else: L = leg_NPTFF(i, d, M, BR, r[bc], conn, split=bool(sp.get('elbow')))
            L['bore'] = r[bc] if kind != 'NPTFF' else None
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
                    if AC > slot_a - 0.02:
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
                elif L['hexl'] < AC + 0.03:
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
                if L['kind'] not in ('JICSW', 'NPSMSW'): continue
                oth_ = [o for o in legs if o is not L][0]; nr_ = L['m']['NECKR']; h_ = AC - L['hexl']
                if h_ > 1e-4 and oth_['hexl'] > nr_:
                    chk.append(f'leg {i}: the other leg\'s hex arm corner (hex corner radius {AC:.4f}) stands {h_:.4f} beyond the swivel body face '
                               f'({L["hexl"]:.4f}) OUTSIDE the neck (radius {nr_:.4f}), from the neck out to the arm end {oth_["hexl"]:.3f} along the other '
                               f'leg (ridge {2 * h_ / TAN30:.4f} wide) - Brennan faces it off at the body face (6500-05-05-FG STEP: body face 0.314 inside '
                               f'the corner radius 0.3245, nothing outside the neck beyond it); the 90 deg elbow has no facing cut')
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
                        if n0_ < oth + 0.003: chk.append(f'leg {i}: locknut starts {n0_:.3f} from the crossing, inside the reach of the other legs / corner ({oth:.3f})')
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
    if 'JICSW' in k: t.append(G.SWIV_ASSUME.replace('the body hex stops at the measured body-face position of the 6500 forged arm (ASSUMED for a straight body)',
                                     'the forged hex arm stops at the measured body-face position (= the 6500 forged-arm end on all 4 STEPs' + ('' if sp.get('elbow') else '; ASSUMED for a tee') + ')') + '; swivel leg length = Air-Way M5 (crossing to the nut face), nose tip at Air-Way M10')
    if 'NPSMSW' in k: t.append(G.NPSM_ASSUME.replace('NUT FACE AT AIR-WAY W AND STEM TIP AT AIR-WAY L', 'NUT FACE AT AIR-WAY ' + sp['npsm'][0].split('@')[0] + ' AND STEM TIP AT AIR-WAY M1/M (crossing to the stem tip)')
                                .replace('neck behind the nut, body face at the measured distance behind the stem tip (Brennan)', 'neck behind the nut, the forged hex arm ends at the measured body face behind the stem tip (Brennan 1404 straight body face - ' + npsm_bodyface_text(sp, legs) + ')'))
    if 'NWO' in k: t.append(NWO_ASSUME)
    if any(L.get('nwo_trim') for L in legs): t.append(NWO_TRIM_ASSUME)
    if any(L.get('trim') for L in legs): t.append(NECK_ASSUME)
    if 'NPTFM' in k: t.append('male NPTF legs: ASME B1.20.3 cone + relief to the Brennan-measured 5404 end length; confirmed on a forged tee by Brennan 5600-16-16-16-FG STEP (hex stops at N - 0.94, relief dia 1.315 = pipe OD, 0.001 proud of the 1.3125 flats)')
    if 'NPTFF' in k:
        t.append('female legs: the forged hex arm stops 0.26 short of the port face and the end is a ROUND COLLAR of dia = the hex flats - MEASURED on the '
                 'Brennan 2502-06-04-FG, 5502-04-04/-08-08/-16-16-FG, 5504-08-08-FG and 5605-08-08-08-FG STEPs (collar 0.260 at every size and leg; '
                 'single manufacturer); port-mouth 45deg chamfer and hex chamfers not modelled')
        if sp.get('nptff_text'): t.append(sp['nptff_text'])        # 2026-10-02 (1502): the root words its own port sentence (source per row)
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
            body.append(f'    MakeLegPlane "PLN2", {legs[1]["V"][-1][0]*IN:.9f}')
            body.append('    stepName = "HEX2"')
            body.append(f'    Call HexArmV("PLN2", 0#, 0#, {legs[1]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX2", 0, 1#)')
        else:
            body.append('    stepName = "HEX2"')
            body.append(f'    Call HexArm("Top Plane", 0#, 0#, {legs[1]["hexl"]*IN:.9f}, {BR*IN:.9f}, "HEX2", 1, 1#)')
        body.append(puck_vba(BR, AC))
        for i, lg in enumerate(legs, 1):
            if lg.get('trim'): body.append(neck_vba(i, lg))       # 2026-10-01 (NECK-6502)
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
        ax, sg = place(sp)[i]; assert ax != 'U', 'angled swivel legs not supported'
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
            assert lg['kind'] != 'NPTFF', 'angled female legs not supported yet'
            body.append(f'    tipPos = {M*IN:.9f}')
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
        if ax == 'U':
            assert t['type'] == 'CUT', 'angled leg must carry a Thread-feature (JIC) end'
            body.append(f'    tipPos = {M*IN:.9f}')
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
        zexp = max([BR] + [lg['rmax'] for lg in legs if lg['kind'] in ('NPTFM', 'JICSW', 'NPSMSW', 'NWO', 'JICBH')])
        # an adjustable ORB leg's washer / locknut corners reach past the corner puck across the other axis
        if legs[1]['kind'] == 'NWO' and not e45: xmin = -max(AC, nwo_radial(legs[1]))
        if legs[0]['kind'] == 'NWO': ymin = -max(AC, nwo_radial(legs[0]))
        # a swivel nut's hex corners (flats normal to Z) lie on the other in-plane axis (2026-09-25: 6500 X -0.722 vs -0.613)
        if legs[1]['kind'] in ('JICSW', 'NPSMSW') and not e45: xmin = min(xmin, -legs[1]['nut_af'] / math.sqrt(3))
        if legs[0]['kind'] in ('JICSW', 'NPSMSW'): ymin = min(ymin, -legs[0]['nut_af'] / math.sqrt(3))
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
        'bulkhead collar' if any(lg['kind'] == 'JICBH' and abs(lg['rmax'] - zexp) < 1e-9 for lg in legs) else 'male pipe end proud of the flats'
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
             [c for c in hdr if c.startswith(('HEXAF@', 'HEXL', 'PUCK_XC@', 'PUCK_R1B@', 'THDPITCH@', 'Profile_Height@', 'PROF_R@', 'DEPTH@BORECUT', 'DEPTH@POCKETCUT', 'TRIM_', 'FILL_'))]
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
             blk] + orbtrim_check(orbtrims, ok) + [f'    swModel.ShowConfiguration2 "{PN}"', '    swModel.ForceRebuild3 False', '']
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
{HELP}{NWO_HELP if any(lg['kind'] == 'NWO' for lg in legs) else ''}{ORBTRIM_HELP if orbtrims else ''}{NECK_HELP if any(lg.get('trim') for lg in legs) else ''}'''
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
