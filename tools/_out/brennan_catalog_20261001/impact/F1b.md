# F1b - what the Brennan catalog changes (Task C group F1, second half by config)

Created 2026-10-01T23:04:19 by `tools/_out/brennan_catalog_20261001/impact/F1b_work/build_F1b.py (+ pairs_F1b.py)`. Data: `impact/F1b.json` (per row: cells, pairings, OMi / Air-Way comparison, questions, steps).

**Catalog hit on 129 of 130 F1b rows (no Brennan part: 6503-16-16-FG). It gives 795 of the 828 dimension cells these rows still need (legs, hexes, bores; the rest: uncertain 45 deg pairings, printed ranges, 2 suspect noses, the missing part); it prints no tap drill, no ORB end detail and no thread major. 9 DECIDE rows move to NOW (Q-B-SWELB / Q-B-6501 settled by the catalog letters, Q-F1 superseded because OMi = Brennan's -FG row); 10 stay DECIDE (OMi/catalog differences, 6503 tap drill, 6503-16-16 not in the catalog). All 28 STEP rows stay STEP but only for tap drills (17) or ORB end cells (11): one answer each (Q-NEW-F1B-TAPDRILL-SCOPE / Q-NEW-F1B-ORBEND) would make them NOW without a download. All 83 WORK rows stay WORK. Step list: 1 not_replaced, 116 partly, 15 replaced_by_catalog.**

Scope: Task C rows with group F1 sorted by config, second half (rows 131..260 of 260): 5504-32-32-FG .. 6902-16-16-NWO-FG.

## Rules applied
- Q-NEW-BRENNANCAT treated as YES (user: 'use any needed' catalogs); Q-BRENNAN-ONLY formally open
- OMi + Brennan catalog = ONE source: a value from either alone, or both agreeing, is ASSUMED
- rounding-only differences are not differences: equal after half-up rounding both to the fewer printed decimals (a 3-decimal print ending in 0 counts as 2 decimals), a print cut to fewer decimals (QA_Log #158) and two prints of one n/64 fraction count as rounding
- the -FG parts have no Air-Way row of their own: agrees_with_airway compares with the plain (non-forged) Air-Way row of the same dashes, named in airway_row - context, not a second source for this part
- pairings: certain = catalog drawing letter (looked at) + the generator SPEC / Air-Way / OMi mapping and agreement on rows that hold values; likely = drawing letter + convention, value test only against other parts; uncertain = not paired, no value carried forward
- a catalog range (min/max drill) is never turned into one value
- THDMAJ cells: the catalog prints only the thread callout (UN callout checked against the basic major); the major itself comes from the thread standard / generator end data
- a STEP row moves to NOW only when every cell it still needs is given by the catalog; DECIDE -> NOW only when every gating question is answered by the catalog and OMi equals the catalog on every cell

## Buckets

| move | rows |
|---|---|
| DECIDE->DECIDE | 10 |
| DECIDE->NOW | 9 |
| STEP->STEP | 28 |
| WORK->WORK | 83 |

New buckets: DECIDE 10, NOW 9, STEP 28, WORK 83.

Cells the rows still need: 828 dimension cells (legs, hexes, bores) - the catalog gives 795; 307 thread-major cells and 265 end cells (tap drills, ORB end details, JIC chain constants) - the catalog gives none (it prints thread callouts only; every UN callout was checked against the basic major). Dimension cells not taken: uncertain pairing 18, catalog range 7, no catalog row 6, suspect catalog value 2.

## What the catalog settles

- **Q-B-SWELB** (5 rows, 6500) and **Q-B-6501** (14 rows, 6501 / 6503): answered by the catalog's own column letters - OMi L 1 = the pipe / male-JIC leg (catalog M / N / M2), M 2 = the swivel-nut face (catalog M6), M 1 = the swivel nose / seat (catalog M4). The p34 / p35 / p38 drawings and 14 to 22 rows per series back it (match/TFA_elbows.json).
- **Q-F1** (23 rows): the standing F1 decision waited for Brennan's -FG data; the catalog prints it. Where OMi equals the catalog on every cell the question is no longer needed (ASSUMED: OMi + Brennan = one source); where a cell differs it moves to Q-NEW-F1B-CATDIFF; 6503-16-16-FG is not in the catalog, so Q-F1 stays open there.
- **Q-B-OTHER-6500L** (5 rows): the OMi side is settled (M 1 = M4 nose, M 2 = M6 nut face, L 1 = M male JIC leg; OMi's 3-decimal M 1 is cut to 2 decimals by the catalog). Air-Way's s131 letters M9 / M12 stay undocumented; their values fit nut face / nose.
- **6801-LL-08-08 Air-Way row** (critic's open point on the fold-reference STEP): it is the -08-10 row (M 1.31, M12 3.25, C4HEX 1, D2 0.48); Brennan's -08-08 prints M 1.250, M7 2.480, C HEX 0.875, B2 DRILL 0.391.
- **Q-MS-FG evidence**: on 6802-32-32, 6803-24-24-24 and 6804-24-24-24 the catalog legs equal the MS51528 / MS51529D / MS51530D legs. If you say yes to Q-MS-FG, MS + Brennan catalog are two independent sources, so those legs become VERIFIED.
- Not settled by the catalog: Q-NEWMASTER-*, Q-TRANSFER-ENDLIB, Q-NEW-PERLEGSW / ANGLED*, Q-NEW-6802E45CHECK (it gets the -32 data for the re-run: Y 2.500, legs 2.220 / 1.860), the fold questions (shape; the catalog only shows that the whole extra length is in the swivel / ORB leg), Q-TRANSFER-TAPDRILL, Q-NEW-PARKER4300, Q-NEW-MS51531NUT and Q-CALIPER (optional).

## New questions for the user

### Q-NEW-F1B-CATDIFF (7 rows)

OMi and Brennan's catalog print different values for the same -FG part (both one source). Which value goes into the table for each cell below? Default by the standing rule (OMi first, 2026-09-25) is OMi with a $COMMENT; evidence per cell is given.

| part | review cell | catalog | OMi (cell) | plain Air-Way |
|---|---|---|---|---|
| 6500-04-06-FG | LEG_M10@DRIVE | M4 LGTH 0.87 | 0.88 (Items!N1913 ('M 1 Size')) | 0.88 |
| 6500-12-08-FG | LEG_M10@DRIVE | M4 LGTH 1.120 | 1.13 (Items!N1925 ('M 1 Size')) | 1.11 |
| 6500-12-16-FG | LEG_M@DRIVE | M LGTH 1.81 | 1.76 (Items!P1927 ('L 1 Size')) | 1.78 |
| 6500-12-16-FG | LEG_M10@DRIVE | M4 LGTH 1.40 | 1.41 (Items!N1927 ('M 1 Size')) | 1.41 |
| 6500-16-12-FG | LEG_M5@DRIVE | M6 LGTH 1.91 | 1.95 (Items!O1928 ('M 2 Size')) | 1.88 |
| 6500-16-12-FG | LEG_M10@DRIVE | M4 LGTH 1.34 | 1.39 (Items!N1928 ('M 1 Size')) | 1.31 |
| 6501-06-06-FG | M10@DRIVE | M4 LGTH 0.90 | 0.910 (Items!N1944 ('M 1 Size')) | 0.97 |
| 6501-12-12-FG | M10@DRIVE | M4 LGTH 1.180 | 1.190 (Items!N1950 ('M 1 Size')) | 1.19 |
| 6503-06-06-FG | M10@DRIVE | M4 LGTH 1.040 | 1.005 (Items!N1977 ('M 1 Size')) | 1.00 |

- Swivel nose cells (LEG_M10 / M10), -08 / -12 / -16 swivels: the Brennan 6500 STEP nose depth NOSETIP_B (00_DOCS/Swivel_end_Brennan6500_measurements.md: -04 0.35, -08 0.43, -12 0.57, -16 0.60 from the nut face) gives catalog M6 - NOSETIP_B = catalog M4 on 6500-12-08 (1.55 - 0.43 = 1.12), 6500-12-16 (2.00 - 0.60 = 1.40), 6500-16-12 (1.91 - 0.57 = 1.34) and 6501-12-12 (1.75 - 0.57 = 1.18). OMi M 1 is 0.01 longer on 6500-12-08 / 6500-12-16 / 6501-12-12 (= Air-Way M10, TFA_elbows_diffcheck finding 1) and 0.05 longer on 6500-16-12, where OMi's nut face M 2 (1.95) also differs from the catalog M6 (1.91); OMi 1.95 - 0.57 = 1.38, not OMi's own 1.39.
- -06 swivel noses (6500-04-06, 6501-06-06): no -06 STEP was measured. The catalog's -06 nose depth M6 - M4 is 0.375 where it prints 3 decimals (6501-04-06 1.250 - 0.875, 6501-08-06 1.420 - 1.045); 6500-04-06 M6 1.25 - 0.375 = 0.875 and 6501-06-06 1.28 - 0.375 = 0.905: the catalog prints them cut (0.87 / 0.90), OMi half-up (0.88 / 0.910). If you accept the 3-decimal value, both are rounding-only prints of it (QA_Log #158) - no source prints that value for these two parts.
- 6503-06-06-FG: the catalog M4 1.040 gives a nose depth of 1.380 - 1.040 = 0.34, unlike every other -06 swivel (0.375); OMi 1.005 gives 0.375 (diffcheck idx 42: the catalog value looks wrong).
- 6500-12-16-FG LEG_M (OMi 1.76 / catalog 1.81 / plain Air-Way 1.78) and 6500-16-12-FG LEG_M5 (OMi 1.95 / catalog 1.91 / plain Air-Way 1.88): no tie-breaker in the repo - the conditional STEPs 6500-12-16-FG / 6500-16-12-FG would settle them.

Recommendation: Nose cells at -08 / -12 / -16 (6500-12-08, 6500-12-16, 6500-16-12, 6501-12-12): the catalog value (it equals Brennan's measured nose geometry; the nose is swivel-end geometry, where Brennan outranks); 6503-06-06: OMi (1.005); -06 noses 6500-04-06 / 6501-06-06: treat as rounding of the 3-decimal value (either print). LEG_M 6500-12-16 and LEG_M5 6500-16-12: OMi per the standing rule with a $COMMENT, or download those two conditional STEPs if you want them measured.

### Q-NEW-F1B-TAPDRILL-SCOPE (17 rows)

These STEP rows of the built masters 5504 / 5602 / 5604 / 5605 now get every body cell from the catalog; only the female-port tap drill is missing (the catalog prints none). May Q-TRANSFER-TAPDRILL (Air-Way's per-size tap drill: -02 0.33, -04 0.43, -06 0.57, -08 0.70, -12 0.91, -16 1.14, -20 1.48; -24 / -32 per Q-CONFLICT-TAPDRILL-24 / -32) also cover them? Yes = these rows move to NOW without a download (the built -FG rows of these tables already use Air-Way tap drills); No = one STEP per part for the tap drill.

Rows: 5504-32-32-FG, 5602-02-02-02-FG, 5602-06-06-06-FG, 5602-12-12-12-FG, 5602-16-16-16-FG, 5602-20-20-20-FG, 5602-24-24-24-FG, 5602-32-32-32-FG, 5604-02-02-02-FG, 5604-12-12-12-FG, 5604-16-16-16-FG, 5604-20-20-20-FG, 5605-02-02-02-FG, 5605-12-12-12-FG, 5605-16-16-16-FG, 5605-20-20-20-FG, 5605-32-32-32-FG.

### Q-NEW-F1B-ORBEND (11 rows)

These STEP rows of the built masters 6801 / 6802 / 6803 / 6804 now get legs, body hex, bores (and confirm the locknut hex) from the catalog; only the ORB end cells ORB_THDL / ORB_GRVDIA / ORB_GRVW (+ ORB_I3 on 6801 / 6802) are missing. Every built row of each table carries the same values for the same ORB dash (MS51527 J2 thread length, ORD-5700 groove, Air-Way I3). May they be copied from the table's own rows of the same ORB dash? Yes = these rows move to NOW without a download; No = one STEP per part.

Rows: 6801-08-04-NWO-FG, 6801-08-16-NWO-FG, 6801-12-20-NWO-FG, 6801-16-24-NWO-FG, 6801-24-16-NWO-FG, 6802-06-10-NWO-FG, 6802-08-12-NWO-FG, 6803-08-08-06-NWO-FG, 6803-08-08-10-NWO-FG, 6803-24-24-24-NWO-FG, 6804-24-24-24-NWO-FG.

### Q-NEW-F1B-RANGE (7 rows)

For these 6901 / 6902 NPSM swivel bores the catalog prints a min/max range (e.g. 0.44/0.46) instead of one drill. Which value is modelled (min, max, or measured on the STEP)? No value is taken from a range without your answer (never average).

| part | review cell | catalog prints | plain Air-Way |
|---|---|---|---|
| 6901-06-08-NWO-FG | D@BORE | 0.44/0.46 | 0.45 |
| 6901-12-06-NWO-FG | D@BORE | 0.320/0.360 | 0.33 |
| 6901-12-16-NWO-FG | D@BORE | .78/.80 | 0.84 |
| 6901-16-12-NWO-FG | D@BORE | 0.610/0.630 | 0.63 |
| 6901-16-16-NWO-FG | D@BORE | 0.78/0.88 | 0.84 |
| 6902-06-06-NWO-FG | D@BORE | 0.32/0.36 | 0.33 |
| 6902-08-08-NWO-FG | D@BORE | 0.44/0.46 | 0.45 |

## Column pairings (review table -> catalog), per table

certain = drawing letter + generator SPEC / OMi mapping + agreement on rows that hold values; likely = drawing letter + convention, tested only against other parts; uncertain = not paired (value not used). Agreement counts are in each cell's `pairing` text in the JSON.

**5504** - TFA p32 5504-FG drawing: N = port A1 face to the A2 axis, N1 = port A2 face to the A1 axis, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1_1@DRIVE | N LGTH | certain | drawing p32: N = the A1 (1st dash) leg; gen_tee SPEC 5504 leg 1 = N1_1@DRIVE |
| N1_2@DRIVE | N1 LGTH | certain | drawing p32: N1 = the A2 (2nd dash) leg; gen_tee SPEC 5504 leg 2 = N1_2@DRIVE |
| W@REF | Y FLATS | certain | drawing p32: Y FLATS = body hex; gen_tee SPEC 5504 hex = W@REF |
| TAPDRILL1@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of port A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5505** - TFA p32 5505-FG drawing: N = port A1 face to the leg crossing (along A1), N1 = port A2 face to the crossing (along the 45 deg A2 axis), Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N2_1@DRIVE | N LGTH | certain | drawing p32: N = the A1 leg; review N2_1 = Air-Way N2 of leg 1 |
| N2_2@DRIVE | N1 LGTH | certain | drawing p32: N1 = the A2 (45 deg) leg; review N2_2 = Air-Way N2 of leg 2 |
| W@HEX | Y FLATS | certain | drawing p32: Y FLATS = body hex |
| TAPDRILL1@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of port A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5601** - TFA p55 5601-FG drawing: both male run legs dimensioned to the branch axis (table N1 = A1, N2 = A2), N3 = female branch A3 port face to the run axis, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N_1@DRIVE | N1 LGTH | certain | drawing p55: run leg A1 (male); the F1b rows are same-dash, N1 = N2 printed equal, so the A1/A2 pick cannot change a value |
| N2@DRIVE | N2 LGTH | certain | drawing p55: run leg A2 (male); same-dash rows, N1 = N2 |
| N1@DRIVE | N3 LGTH | certain | drawing p55: N3 = female branch A3 leg; Air-Way 5601 N1@DRIVE is the branch (plain rows: N1@DRIVE = catalog N3) |
| W@HEX | Y FLATS | certain | drawing p55: Y FLATS = body hex |
| D1@BORE | A1 DRILL | certain | A1 DRILL = through drill of the male A1 end |
| D2@BORE | A2 DRILL | certain | A2 DRILL = through drill of the male A2 end |
| TAPDRILL@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of end A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of end A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | A3 NPTF | callout | catalog "A3 NPTF" is the thread callout of port A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5602** - TFA p55 5602-FG drawing: N = male A1 leg, N1 = female run A2 port face, N2 = female branch A3 port face, Y FLATS = body hex (header prints "N1 LGBTH")

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N@DRIVE | N LGTH | certain | drawing p55: N = male A1 leg; gen_tee SPEC 5602 leg 1 (NPTFM) = N@DRIVE |
| N1_2@DRIVE | N1 LGBTH | certain | drawing p55: N1 = female run A2 leg (header typo "LGBTH"); SPEC leg 2 = N1_2@DRIVE |
| N1_3@DRIVE | N2 LGTH | certain | drawing p55: N2 = female branch A3 leg; SPEC leg 3 = N1_3@DRIVE |
| WY@REF | Y FLATS | certain | drawing p55: Y FLATS = body hex; SPEC hex = WY@REF |
| D@BORE | A1 DRILL | certain | A1 DRILL = through drill of the male A1 end; SPEC conn = D@BORE |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL3@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of end A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | A3 NPTF | callout | catalog "A3 NPTF" is the thread callout of port A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5603** - TFA p55 5603-FG drawing: N1 = male run A1 leg, N = female run A2 port face, N2 = male branch A3 leg, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1@DRIVE | N1 LGTH | certain | drawing p55: N1 = male A1 run leg (Task C SPEC plan: NPTFM +X); same-dash rows print N1 = N2 |
| N1_2@DRIVE | N LGTH | certain | drawing p55: N = female A2 run leg; plain Air-Way rows: N1_2@DRIVE = catalog N 5/5 |
| N3@DRIVE | N2 LGTH | certain | drawing p55: N2 = male A3 branch leg; same-dash rows print N1 = N2 |
| W@REF | Y FLATS | certain | drawing p55: Y FLATS = body hex |
| D1_1@BORE | A1 DRILL | certain | A1 DRILL = through drill of the male A1 end |
| D1_3@BORE | A3 DRILL | certain | A3 DRILL = through drill of the male A3 end |
| TAPDRILL@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of end A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | A3 NPTF | callout | catalog "A3 NPTF" is the thread callout of end A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5604** - TFA p56 5604-FG drawing: N = male branch A3 leg to the run axis, N1 / N2 = female run ports A1 / A2, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1_1@DRIVE | N1 LGTH | certain | female run A1 leg; gen_tee SPEC 5604 leg 1 = N1_1@DRIVE |
| N1_2@DRIVE | N2 LGTH | certain | female run A2 leg; SPEC leg 2 = N1_2@DRIVE |
| N@DRIVE | N LGTH | certain | drawing p56: N = male branch A3 leg; SPEC leg 3 (NPTFM) = N@DRIVE |
| W@HEX | Y FLATS | certain | drawing p56: Y FLATS = body hex; SPEC hex = W@HEX |
| D@BORE | A3 DRILL | certain | A3 DRILL = through drill of the male A3 end; SPEC conn = D@BORE |
| TAPDRILL1@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of port A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | A3 NPTF | callout | catalog "A3 NPTF" is the thread callout of end A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5605** - TFA p56 5605-FG drawing: N1 = port A1, N2 = port A2 (run), N3 = branch port A3, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1_1@DRIVE | N1 LGTH | certain | drawing p56: N1 = A1 leg; gen_tee SPEC 5605 leg 1 = N1_1@DRIVE |
| N1_2@DRIVE | N2 LGTH | certain | drawing p56: N2 = A2 leg; SPEC leg 2 |
| N1_3@DRIVE | N3 LGTH | certain | drawing p56: N3 = A3 branch leg; SPEC leg 3 |
| W@HEX | Y FLATS | certain | drawing p56: Y FLATS = body hex; SPEC hex = W@HEX |
| TAPDRILL1@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL3@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of port A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | A3 NPTF | callout | catalog "A3 NPTF" is the thread callout of port A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**5652** - TFA p63 5652-FG drawing: every leg dimensioned N (port face to the crossing), one N column; Y FLATS = body hex; the 3rd thread column is printed "AD NPTF"

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1_1@DRIVE | N LGTH | certain | drawing p63: all four legs are dimensioned N (one printed length per row) |
| N1_2@DRIVE | N LGTH | certain | drawing p63: all four legs are dimensioned N |
| N1_3@DRIVE | N LGTH | certain | drawing p63: all four legs are dimensioned N |
| N1_4@DRIVE | N LGTH | certain | drawing p63: all four legs are dimensioned N |
| W@HEX | Y FLATS | certain | drawing p63: Y FLATS = body hex |
| TAPDRILL1@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL2@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL3@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| TAPDRILL4@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A1@DRIVE | A1 NPTF | callout | catalog "A1 NPTF" is the thread callout of port A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A2@DRIVE | A2 NPTF | callout | catalog "A2 NPTF" is the thread callout of port A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A3@DRIVE | AD NPTF | callout | catalog "AD NPTF" is the thread callout of port A3 (header printed "AD"): it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A4@DRIVE | A4 NPTF | callout | catalog "A4 NPTF" is the thread callout of port A4: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6500** - TFA p34 6500-FG drawing: M = male JIC (B1) tip to the swivel-leg axis, M4 = B1 axis to the swivel nose / seat (inside the nut), nut-face length labelled M5 in the drawing and printed "M6 LGTH" in the header, C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| LEG_M@DRIVE | M LGTH | certain | drawing p34: M = male JIC leg; OMi L 1 = catalog M (certain 21/22, match/TFA_elbows.json); review exact -FG rows |
| LEG_M5@DRIVE | M6 LGTH | certain | drawing p34: nut-face length (drawn "M5", header "M6"); OMi M 2 = catalog M6 (certain 21/22); Air-Way M5 = nut face (Brennan 6500 STEPs, 00_DOCS/Swivel_end_Brennan6500_measurements.md) |
| LEG_M10@DRIVE | M4 LGTH | likely | drawing p34: M4 = axis to the swivel nose / seat = Air-Way M10 feature (gen_tee SPEC 6500 sw nose = LEG_M10@DRIVE); OMi M 1 / Air-Way M10 are usually 0.01 longer than the printed M4, while M6 - NOSETIP_B (Brennan STEP, -04/-08/-12/-16) equals the printed M4 |
| HEXB@HEX | C HEX | certain | drawing p34: C HEX = swivel nut; OMi Nut Hex 1 = C HEX 22/22; SPEC sw nut = HEXB@HEX |
| Y@REF | Y FLATS | certain | drawing p34: Y FLATS = body hex; OMi Hex Flat = Y FLATS 22/22; SPEC hex = Y@REF |
| D1@BORE | B1 DRILL | certain | B1 = male JIC end; OMi Side 1 ID = B1 DRILL 22/22 |
| D2@BORE | B2 DRILL | certain | B2 = swivel end; OMi Side 2 ID = B2 DRILL 22/22 |
| THDMAJ_A@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the male JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B2 SAE 37Deg | callout | catalog "B2 SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6500L** - TFA p34 6500-L-FG drawing: M = male JIC (B1) leg, M4 = to the swivel nose / seat, M6 = to the swivel-nut face, C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M@DRIVE | M LGTH | certain | drawing p34: M = male JIC leg; OMi L 1 = catalog M 5/5 (certain); mapping_final M122 |
| M9@DRIVE | M6 LGTH | likely | catalog M6 = nut face (drawing p34), OMi M 2 = M6 5/5 (certain); Air-Way s131 letter M9 is undocumented (mapping_final M121 uncertain) - it is the longer of the two swivel lengths and within 0.06 of M6 on the plain Air-Way rows, as a nut-face length must be |
| M12@DRIVE | M4 LGTH | likely | catalog M4 = swivel nose / seat (drawing p34), OMi M 1 = M4 + 0.003..0.008 (3-decimal values cut to 2 by the catalog, QA_Log #158); Air-Way M12 undocumented (mapping_final M120) - the shorter swivel length, within 0.07 of M4 on the plain rows |
| CHEX@HEX | C HEX | certain | drawing: C HEX = swivel nut; OMi Nut Hex 1 = C HEX 5/5 |
| Y@REF | Y FLATS | certain | drawing: Y FLATS = body hex; OMi Hex Flat = Y FLATS 5/5 |
| D1@BORE | B1 DRILL | certain | B1 = male JIC end (B1 DRILL = OMi Side 1 ID 5/5; certain on 6500) |
| D2@BORE | B2 DRILL | certain | B2 = swivel end (B2 DRILL = OMi Side 2 ID 5/5; certain on 6500) |
| THDMAJ_B1@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the male JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE 37Deg | callout | catalog "B2 SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6501** - TFA p35 6501-FG drawing: N = male pipe (A) leg, M4 = to the swivel nose / seat, M6 = to the swivel-nut face, C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N@DRIVE | N LGTH | certain | drawing p35: N = male pipe leg; OMi L 1 = N 14/14 (certain); SPEC 6501 leg 1 = N@DRIVE |
| M5@DRIVE | M6 LGTH | certain | drawing p35: M6 = nut face; OMi M 2 = M6 12/14 (certain); SPEC 6501 JICSW leg = M5@DRIVE |
| M10@DRIVE | M4 LGTH | likely | drawing p35: M4 = nose / seat = Air-Way M10 feature (SPEC sw nose = M10@DRIVE); OMi M 1 equal on 8/14, otherwise 0.01 longer (likely) |
| C3HEX@HEX | C HEX | certain | drawing: C HEX = swivel nut; OMi Nut Hex 1 = C HEX 14/14 |
| Y@HEX | Y FLATS | certain | drawing: Y FLATS = body hex; OMi Hex Flat 14/14; SPEC hex = Y@HEX |
| D1@BORE | A DRILL | certain | A = male pipe end; OMi Side 1 ID = A DRILL 14/14 |
| D@BORE | B DRILL | certain | B = swivel end; OMi Side 2 ID = B DRILL 14/14 |
| THDMAJ_A@DRIVE | A NPTF | callout | catalog "A NPTF" is the thread callout of the male pipe end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B SAE 37Deg | callout | catalog "B SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6503** - TFA p38 6503-FG drawing: M2 = female pipe (A) port face to the swivel axis, M4 = to the swivel nose / seat, M6 = to the nut face, C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N1@DRIVE | M2 LGTH | certain | drawing p38: M2 = female pipe leg; OMi L 1 = M2 6/6 (certain) |
| M5@DRIVE | M6 LGTH | likely | drawing p38: M6 = nut face; OMi M 2 = M6 4/6 (other 2 within 0.05) |
| M10@DRIVE | M4 LGTH | likely | drawing p38: M4 = nose / seat; OMi M 1 within 0.05 on 5/5 numeric rows (3-decimal OMi vs 2-decimal catalog) |
| C3HEX@HEX | C HEX | certain | drawing: C HEX = swivel nut; OMi Nut Hex 1 6/6 |
| Y1@HEX | Y FLATS | certain | drawing: Y FLATS = body hex; OMi Hex Flat 6/6 |
| D@BORE | B DRILL | certain | B = swivel end; OMi Side 2 ID = B DRILL 6/6 |
| TAPDRILL@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| THDMAJ_A@DRIVE | A NPTF | callout | catalog "A NPTF" is the thread callout of the female pipe port: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B SAE 37Deg | callout | catalog "B SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6603** - TFA p58 6603-FG drawing (300 dpi clip): M4 = A3 axis to the A1 swivel nose / seat (extension line inside the A1 nut), M2 = A3 axis to the A2 swivel-nut face, M = male JIC A3 leg, C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M5_1@DRIVE | M2 LGTH | likely | drawing p58: M2 = run-swivel nut face (drawn on A2; the F1b rows are same-dash, both swivels identical); values = the 6500 nut-face M6 of the same dash; plain Air-Way M5 = M2 5/5 |
| M10_1@DRIVE | M4 LGTH | likely | drawing p58: M4 ends inside the A1 nut = nose / seat; values = the 6500 nose M4 of the same dash; Air-Way M10 0.01 longer, as on 6500 |
| M5_2@DRIVE | M2 LGTH | likely | drawing p58: M2 = A2 swivel nut face (same-dash swivels) |
| M10_2@DRIVE | M4 LGTH | likely | M4 = swivel nose / seat (same-dash swivels: printed once) |
| M@DRIVE | M LGTH | certain | drawing p58: M = male JIC A3 leg |
| C3_1HEX@HEX | C HEX | certain | drawing p58: C HEX = swivel nut (same-dash swivels) |
| C3_2HEX@HEX | C HEX | certain | drawing p58: C HEX = swivel nut |
| Y@HEX | Y FLATS | certain | drawing p58: Y FLATS = body hex |
| D1@BORE | A1 DRILL | certain | A1 swivel end drill |
| D2@BORE | A2 DRILL | certain | A2 swivel end drill |
| D3@BORE | A3 DRILL | certain | A3 male JIC end drill |
| THDMAJ_B1@DRIVE | A1 SAE 37Deg | callout | catalog "A1 SAE 37Deg" is the thread callout of swivel A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | A2 SAE 37Deg | callout | catalog "A2 SAE 37Deg" is the thread callout of swivel A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B3@DRIVE | A3 SAE 37Deg | callout | catalog "A3 SAE 37Deg" is the thread callout of male JIC A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6606** - TFA p58 6606-FG drawing: M6 = crossing to a swivel-nut face (A1 / A3), M = crossing to a swivel nose / seat (A2), C HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M5_1@DRIVE | M6 LGTH | likely | drawing p58: M6 = nut face; values = the 6500 M6 of the same dash; plain Air-Way M5 = M6 2/2 (same-dash swivels: printed once) |
| M10_1@DRIVE | M LGTH | likely | drawing p58: M = to the nose / seat; values = the 6500 nose M4 of the same dash; Air-Way M10 0.01 longer |
| M5_2@DRIVE | M6 LGTH | likely | nut face (same-dash swivels) |
| M10_2@DRIVE | M LGTH | likely | nose / seat (same-dash swivels) |
| M5_3@DRIVE | M6 LGTH | likely | nut face (same-dash swivels) |
| M10_3@DRIVE | M LGTH | likely | nose / seat (same-dash swivels) |
| C3_1HEX@HEX | C HEX | certain | drawing p58: C HEX = swivel nut |
| C3_2HEX@HEX | C HEX | certain | swivel nut (same dash) |
| C3_3HEX@HEX | C HEX | certain | swivel nut (same dash) |
| Y@HEX | Y FLATS | certain | drawing p58: Y FLATS = body hex |
| D1@BORE | A1 DRILL | certain | swivel end drill (A1 = A2 = A3 on these same-dash rows) |
| THDMAJ_B1@DRIVE | A1 SAE 37Deg | callout | catalog "A1 SAE 37Deg" is the thread callout of swivel A1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | A2 SAE 37Deg | callout | catalog "A2 SAE 37Deg" is the thread callout of swivel A2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B3@DRIVE | A3 SAE 37Deg | callout | catalog "A3 SAE 37Deg" is the thread callout of swivel A3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6801** - TFA p40 6801-NWO-FG drawing: M = male JIC (B1) leg, M7 = ORB (B2) tip to the B1 axis, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| LEG_JIC@DRIVE | M LGTH | certain | drawing: M = JIC leg; gen_tee SPEC 6801 leg 1 |
| LEG_ORB@DRIVE | M7 LGTH | certain | drawing: M7 = ORB tip to the JIC axis; SPEC 6801 NWO leg |
| HEXB@HEX | C HEX | certain | drawing: C HEX = locknut; SPEC nwo locknut = HEXB@HEX |
| Y@REF | Y FLATS | certain | drawing: Y FLATS = body hex; SPEC hex = Y@REF |
| D1@BORE | B1 DRILL | certain | B1 = JIC end drill |
| D2@BORE | B2 DRILL | certain | B2 = ORB end drill |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_I3@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| JIC_RELIEFL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| RELIEFANG@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_THDZ@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_CONEDIA@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_LANDL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_SEATL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| SEATB@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| THDMAJ_A@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6801L** - TFA p39 6801-L-NWO-FG drawing: M = male JIC (B1) leg, M7 = ORB (B2) tip to the B1 axis, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M@DRIVE | M LGTH | certain | drawing p39: M = JIC leg |
| M11@DRIVE | M7 LGTH | likely | drawing p39: M7 = the long ORB leg; Air-Way M11 = the long ORB leg (Task C fold plan: M11 -> LEG_ORB); Air-Way -FG rows -04-04 / -08-08 / -12-12 print shorter values, the plain -16-16 / -20-20 rows equal the catalog |
| C4HEX@HEX | C HEX | certain | drawing p39: C HEX = locknut |
| Y@REF | Y FLATS | certain | drawing p39: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 = JIC end |
| D2@BORE | B2 DRILL | certain | B2 = ORB end |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_B1@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6801LL** - TFA p39 6801-LL-NWO-FG drawing: M = male JIC (B1) leg, M7 = ORB (B2) tip to the B1 axis, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M@DRIVE | M LGTH | certain | drawing p39: M = JIC leg |
| M12@DRIVE | M7 LGTH | likely | drawing p39: M7 = the extra-long ORB leg; Air-Way M12 = that leg (Task C fold plan: M12 -> LEG_ORB); plain Air-Way -12-12 / -16-16 / -20-20 rows equal the catalog; the Air-Way LL-08-08 -FG row is a copy of the -08-10 row (see note) |
| C4HEX@HEX | C HEX | certain | drawing p39: C HEX = locknut |
| Y@REF | Y FLATS | certain | drawing p39: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 = JIC end |
| D2@BORE | B2 DRILL | certain | B2 = ORB end |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_B1@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6802** - TFA p41 6802-NWO-FG (45 deg): M2 = male JIC (B1) leg, M8 = ORB (B2) leg, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| LEG_JIC@DRIVE | M2 LGTH | certain | JIC leg (SPEC 6802 JICM leg) |
| LEG_ORB@DRIVE | M8 LGTH | certain | ORB leg (SPEC 6802 NWO leg) |
| HEXB@HEX | C HEX | certain | C HEX = locknut |
| Y@REF | Y FLATS | certain | Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | JIC end |
| D2@BORE | B2 DRILL | certain | ORB end |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_I3@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| JIC_RELIEFL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| RELIEFANG@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_THDZ@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_CONEDIA@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_LANDL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| JIC_SEATL@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| SEATB@DRIVE | - | n/a | JIC end geometry (MS33656J chain constant, Task C fill) - the catalog prints only the thread callout |
| THDMAJ_A@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of the JIC end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6803** - TFA p59 6803-NWO-FG drawing: M1 = JIC run B1 leg, M2 = JIC run B2 leg, M7 = ORB branch (B3) tip to the run axis, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| LEG1@DRIVE | M1 LGTH | certain | drawing p59: M1 = B1 leg; SPEC 6803 leg 1 |
| LEG2@DRIVE | M2 LGTH | certain | drawing p59: M2 = B2 leg; SPEC leg 2 |
| LEG3@DRIVE | M7 LGTH | certain | drawing p59: M7 = ORB branch tip to the run axis; SPEC NWO leg 3 |
| HEXB@HEX | C HEX | certain | drawing p59: C HEX = locknut |
| Y@REF | Y FLATS | certain | drawing p59: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 |
| D2@BORE | B2 DRILL | certain | B2 |
| D3@BORE | B3 DRILL | certain | B3 (ORB) |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_1@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of JIC B1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_2@DRIVE | B2 SAE 37Deg | callout | catalog "B2 SAE 37Deg" is the thread callout of JIC B2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_3@DRIVE | B3 SAE ORB | callout | catalog "B3 SAE ORB" is the thread callout of ORB B3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6804** - TFA p60 6804-NWO-FG drawing: M1 = JIC B1 leg, M7 = ORB run (B2) tip to the branch axis, M2 = JIC branch B3 leg, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| LEG1@DRIVE | M1 LGTH | certain | drawing p60: M1 = B1 JIC leg; SPEC 6804 leg 1 |
| LEG2@DRIVE | M7 LGTH | certain | drawing p60: M7 = ORB run leg; SPEC NWO leg 2 |
| LEG3@DRIVE | M2 LGTH | certain | drawing p60: M2 = JIC branch B3 leg; SPEC leg 3 |
| HEXB@HEX | C HEX | certain | drawing p60: C HEX = locknut |
| Y@REF | Y FLATS | certain | drawing p60: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 |
| D2@BORE | B2 DRILL | certain | B2 (ORB) |
| D3@BORE | B3 DRILL | certain | B3 |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_1@DRIVE | B1 SAE 37Deg | callout | catalog "B1 SAE 37Deg" is the thread callout of JIC B1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_2@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of ORB B2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_3@DRIVE | B3 SAE 37Deg | callout | catalog "B3 SAE 37Deg" is the thread callout of JIC B3: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6805** - TFA p42 6805-NWO-FG drawing (300 dpi clip): M7 = ORB (B) tip to the pipe axis, N = female pipe (A) port face to the ORB axis, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M17@DRIVE | M7 LGTH | likely | drawing p42: M7 = ORB leg; Air-Way M17 is the table's only ORB-leg column; plain rows -08 and up mostly within 0.01, -04/-05 plain rows 0.05-0.10 shorter |
| N1@DRIVE | N LGTH | certain | drawing p42: N = female pipe leg |
| C4HEX@HEX | C HEX | certain | drawing p42: C HEX = locknut |
| Y1@REF | Y FLATS | certain | drawing p42: Y FLATS = body hex |
| D@BORE | B DRILL | certain | B = ORB end drill |
| TAPDRILL@BORE | - | n/a | the catalog prints no tap drill for a female NPTF port (only DRILL columns of male / tube ends) |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_A@DRIVE | A NPTF | callout | catalog "A NPTF" is the thread callout of the female pipe port: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B SAE ORB | callout | catalog "B SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6806** - TFA p43 6806-NWO-FG drawing: M7 = ORB (B) leg, N = male pipe (A) leg, C HEX = locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M7@DRIVE | M7 LGTH | certain | drawing p43: M7 = ORB leg (same letter in Air-Way) |
| N@DRIVE | N LGTH | certain | drawing p43: N = male pipe leg |
| C4HEX@HEX | C HEX | certain | drawing p43: C HEX = locknut |
| Y@REF | Y FLATS | certain | drawing p43: Y FLATS = body hex |
| D@BORE | B DRILL | certain | B = ORB end drill |
| D1@BORE | A DRILL | certain | A = male pipe end drill |
| ORB_THDL@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVDIA@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| ORB_GRVW@DRIVE | - | n/a | ORB end detail (thread length / O-ring groove / I3): the catalog prints only the ORB thread callout |
| THDMAJ_A@DRIVE | A NPTF | callout | catalog "A NPTF" is the thread callout of the male pipe end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B@DRIVE | B SAE ORB | callout | catalog "B SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6807** - TFA p43 6807-NWO-FG drawing: M1 = B1 ORB leg, M2 = B2 ORB leg, C HEX = B1 locknut, C2 HEX = B2 locknut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M7_1@DRIVE | M1 LGTH | certain | drawing p43: M1 = B1 leg |
| M7_2@DRIVE | M2 LGTH | certain | drawing p43: M2 = B2 leg |
| C4_1HEX@HEX | C HEX | certain | drawing p43: C HEX = B1 locknut |
| C4_2HEX@HEX | C2 HEX | certain | drawing p43: C2 HEX = B2 locknut |
| Y@HEX | Y FLATS | certain | drawing p43: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 |
| D2@BORE | B2 DRILL | certain | B2 |
| THDMAJ_B1@DRIVE | B1 SAE ORB | callout | catalog "B1 SAE ORB" is the thread callout of ORB B1: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE ORB | callout | catalog "B2 SAE ORB" is the thread callout of ORB B2: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6809** - TFA p44 6809-NWO-FG drawing: M7 = ORB (B1) tip to the swivel axis, M = B1 axis to the swivel nose / seat, M6 = to the swivel-nut face, C1 HEX = locknut, C2 HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M7@DRIVE | M7 LGTH | certain | drawing p44: M7 = ORB leg (same letter in Air-Way) |
| M5@DRIVE | M6 LGTH | certain | drawing p44: M6 = swivel-nut face = Air-Way M5 feature (6500 convention) |
| M10@DRIVE | M LGTH | likely | drawing p44: M = to the swivel nose / seat = Air-Way M10 feature; Air-Way M10 within 0.04 of M except -12-12 (catalog 1.370 suspect, see catalog issues) |
| C3HEX@HEX | C2 HEX | certain | drawing p44: C2 HEX = swivel nut (Air-Way C3) |
| C4HEX@HEX | C1 HEX | certain | drawing p44: C1 HEX = locknut (Air-Way C4) |
| Y@HEX | Y FLATS | certain | drawing p44: Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 = ORB end |
| D2@BORE | B2 DRILL | certain | B2 = swivel end |
| THDMAJ_B1@DRIVE | B1 SAE ORB | callout | catalog "B1 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE 37Deg | callout | catalog "B2 SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6810** - TFA p44 6810-NWO-FG (45 deg) drawing: M8 = ORB (B1) leg, M / M6 = swivel nose / nut face along the 45 deg B2 axis, C HEX = locknut, C2 HEX = swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| M8@DRIVE | M8 LGTH | likely | M8 = ORB leg (same letter in Air-Way, = 6802 M8 ORB leg); plain Air-Way M8 = catalog 2/2 |
| M19@DRIVE | M6 LGTH | uncertain | Air-Way M19 (undocumented letter) is 0.12 shorter than catalog M6 on both plain rows (1.16 / 1.28, 1.38 / 1.50): a different reference point on the 45 deg leg - not paired |
| M20@DRIVE | M LGTH | uncertain | Air-Way M20 (undocumented letter) is 0.11-0.12 shorter than catalog M on both plain rows: different reference point - not paired |
| C3HEX@HEX | C2 HEX | certain | drawing p44: C2 HEX = swivel nut |
| C4HEX@HEX | C HEX | certain | drawing p44: C HEX = locknut |
| Y@HEX | Y FLATS | certain | Y FLATS = body hex |
| D1@BORE | B1 DRILL | certain | B1 = ORB end |
| D2@BORE | B2 DRILL | certain | B2 = swivel end |
| THDMAJ_B1@DRIVE | B1 SAE ORB | callout | catalog "B1 SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_B2@DRIVE | B2 SAE 37Deg | callout | catalog "B2 SAE 37Deg" is the thread callout of the swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6901** - TFA p45 6901-NWO-FG drawing: M7 = ORB (B) tip to the NPSM axis, M = B axis to the NPSM swivel seat / stem tip, M6 = to the NPSM nut face, C HEX = locknut, C1 HEX = NPSM swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N5@DRIVE | M7 LGTH | likely | drawing p45: M7 = ORB leg; Air-Way N5 is the table's only ORB-leg column; Air-Way -FG rows equal on 2/4 |
| M1@DRIVE | M LGTH | likely | drawing p45: M = to the NPSM seat / stem tip; gen_tee NPSM convention (1501): M1 = crossing to the stem tip |
| W3@HEX | M6 LGTH | likely | drawing p45: M6 = NPSM nut face; gen_tee NPSM convention (1501, line 688): nut face at Air-Way W3 |
| CHEX@HEX | C1 HEX | certain | drawing p45: C1 HEX = NPSM swivel nut; plain Air-Way CHEX = C1 HEX 25/25 |
| C4HEX@HEX | C HEX | certain | drawing p45: C HEX = locknut; plain Air-Way C4HEX = C HEX 25/25 |
| C1HEX@HEX | Y FLATS | likely | body hex: gen_tee SPEC 1501 hex = C1HEX@HEX and the built 1501 -FG rows print C1HEX = catalog Y FLATS on most sizes; the four Air-Way 6901 -FG rows print larger values (0.75 / 0.75 / 0.88 / 1.11 vs 0.562 / 0.562 / 0.750 / 0.875) |
| D1@BORE | B DRILL | certain | B = ORB end drill (plain 25/25) |
| D@BORE | A DRILL | likely | A = NPSM swivel end drill; several sizes print a range (min/max) |
| THDMAJ_B@DRIVE | B SAE ORB | callout | catalog "B SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A1@DRIVE | A NPSM | callout | catalog "A NPSM" is the thread callout of the NPSM swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

**6902** - TFA p46 6902-NWO-FG (45 deg) drawing: M8 = ORB (B) leg, M / M6 = NPSM seat / nut face along the 45 deg A axis, C HEX = locknut, C1 HEX = NPSM swivel nut, Y FLATS = body hex

| review column | catalog column | pairing | reason |
|---|---|---|---|
| N4@DRIVE | M8 LGTH | likely | M8 = ORB leg (6802 / 6810 letter); Air-Way 6902-12-12-NWO-FG N4 1.73 = catalog M8 1.730 |
| M@DRIVE | M LGTH | uncertain | NPSM stem-tip length on the 45 deg leg: Air-Way -FG 6902-12-12 1.06 vs catalog M 1.020, and the sister 45 deg NPSM elbow 1503 shows Air-Way and catalog 45 deg legs differing by up to 0.15 - reference point not established; not paired |
| W2@HEX | M6 LGTH | uncertain | NPSM nut face on the 45 deg leg (1503 convention W2 = nut face): Air-Way -FG 6902-12-12 1.39 vs catalog M6 1.370 - reference point not established; not paired |
| CHEX@HEX | C1 HEX | certain | C1 HEX = NPSM swivel nut; plain Air-Way CHEX = C1 HEX 17/17 |
| C4HEX@HEX | C HEX | certain | C HEX = locknut; plain 16/17 |
| C1HEX@HEX | Y FLATS | likely | body hex (1501/1503 convention hex = C1HEX@HEX); Air-Way 6902-12-12-NWO-FG C1HEX 1.06 = Y FLATS 1.062 |
| D1@BORE | B DRILL | certain | B = ORB end drill (plain 17/17) |
| D@BORE | A DRILL | likely | A = NPSM swivel end drill; some sizes print a range |
| THDMAJ_B@DRIVE | B SAE ORB | callout | catalog "B SAE ORB" is the thread callout of the ORB end: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |
| THDMAJ_A1@DRIVE | A NPSM | callout | catalog "A NPSM" is the thread callout of the NPSM swivel nut: it confirms the thread size; the major diameter itself is not printed (it comes from the thread standard / generator end data) |

## Rows

### Old bucket DECIDE (19 rows)

| part | new bucket | catalog | catalog gives | still missing | questions answered / new | note |
|---|---|---|---|---|---|---|
| 6500-04-06-FG | DECIDE | TFA p34 6500-FG | LEG_M=1.05, LEG_M5=1.25, LEG_M10=0.87, HEXB=0.688, Y=0.562, D1=0.172, D2=0.297 |  | Q-B-SWELB; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on LEG_M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-SWELB, Q-F1) |
| 6500-06-04-FG | NOW | TFA p34 6500-FG | LEG_M=1.060, LEG_M5=1.240, LEG_M10=0.900, HEXB=0.563, Y=0.562, D1=0.297, D2=0.172 |  | Q-B-SWELB; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-SWELB, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator ... |
| 6500-12-08-FG | DECIDE | TFA p34 6500-FG | LEG_M=1.660, LEG_M5=1.550, LEG_M10=1.120, HEXB=0.875, Y=1.062, D1=0.609, D2=0.391 |  | Q-B-SWELB; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on LEG_M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-SWELB, Q-F1) |
| 6500-12-16-FG | DECIDE | TFA p34 6500-FG | LEG_M=1.81, LEG_M5=2.00, LEG_M10=1.40, HEXB=1.500, Y=1.312, D1=0.609, D2=0.844 |  | Q-B-SWELB; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on LEG_M@DRIVE, LEG_M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-SWELB, Q-F1) |
| 6500-16-12-FG | DECIDE | TFA p34 6500-FG | LEG_M=1.81, LEG_M5=1.91, LEG_M10=1.34, HEXB=1.250, Y=1.312, D1=0.844, D2=0.609 |  | Q-B-SWELB; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on LEG_M5@DRIVE, LEG_M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-SWELB, Q-F1) |
| 6501-04-06-FG | NOW | TFA p35 6501-FG | N=1.090, M5=1.250, M10=0.875, C3HEX=0.688, Y=0.562, D1=0.281, D=0.297 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-06-06-FG | DECIDE | TFA p35 6501-FG | N=1.22, M5=1.28, M10=0.90, C3HEX=0.688, Y=0.750, D1=0.406, D=0.297 |  | Q-B-6501; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-6501, Q-F1) |
| 6501-06-08-FG | NOW | TFA p35 6501-FG | N=1.220, M5=1.380, M10=0.958, C3HEX=0.875, Y=0.750, D1=0.406, D=0.391 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-08-06-FG | NOW | TFA p35 6501-FG | N=1.470, M5=1.420, M10=1.045, C3HEX=0.688, Y=0.875, D1=0.531, D=0.297 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-08-08-FG | NOW | TFA p35 6501-FG | N=1.47, M5=1.52, M10=1.09, C3HEX=0.875, Y=0.875, D1=0.531, D=0.391 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-08-10-FG | NOW | TFA p35 6501-FG | N=1.47, M5=1.62, M10=1.12, C3HEX=1.000, Y=0.875, D1=0.531, D=0.484 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-12-12-FG | DECIDE | TFA p35 6501-FG | N=1.590, M5=1.750, M10=1.180, C3HEX=1.250, Y=1.062, D1=0.719, D=0.609 |  | Q-B-6501; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on M10@DRIVE (Q-NEW-F1B-CATDIFF). The catalog settles the rest (Q-B-6501, Q-F1) |
| 6501-16-16-FG | NOW | TFA p35 6501-FG | N=1.970, M5=2.010, M10=1.410, C3HEX=1.500, Y=1.312, D1=0.938, D=0.844 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-20-20-FG | NOW | TFA p35 6501-FG | N=2.380, M5=2.310, M10=1.670, C3HEX=2.000, Y=1.625, D1=1.250, D=1.078 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6501-24-24-FG | NOW | TFA p35 6501-FG | N=2.640, M5=2.590, M10=1.856, C3HEX=2.250, Y=1.875, D1=1.500, D=1.312 |  | Q-B-6501; Q-F1 | DECIDE -> NOW: the catalog answers Q-B-6501, Q-F1; every body cell = Brennan's -FG catalog row = OMi (rounding-only where marked) - build with the Task C fills (OMi first, user rule 2026-09-25), ends from the generator l... |
| 6503-04-04-FG | DECIDE | TFA p38 6503-FG | N1=0.88, M5=1.18, M10=0.83, C3HEX=0.563, Y1=0.750, D=0.172 |  | Q-B-6501; Q-F1 | stays DECIDE: Q-TRANSFER-TAPDRILL (tap drill; not in the catalog). The catalog settles the rest (Q-B-6501, Q-F1) |
| 6503-06-06-FG | DECIDE | TFA p38 6503-FG | N1=1.020, M5=1.380, M10=1.040, C3HEX=0.688, Y1=0.875, D=0.297 |  | Q-B-6501; Q-F1; new: Q-NEW-F1B-CATDIFF | stays DECIDE: OMi and the catalog differ on M10@DRIVE (Q-NEW-F1B-CATDIFF); Q-TRANSFER-TAPDRILL (tap drill; not in the catalog). The catalog settles the rest (Q-B-6501, Q-F1) |
| 6503-12-12-FG | DECIDE | TFA p38 6503-FG | N1=1.360, M5=1.860, M10=1.300, C3HEX=1.250, Y1=1.312, D=0.609 |  | Q-B-6501; Q-F1 | stays DECIDE: Q-TRANSFER-TAPDRILL (tap drill; not in the catalog). The catalog settles the rest (Q-B-6501, Q-F1) |
| 6503-16-16-FG | DECIDE | not in catalog |  |  | Q-B-6501 | stays DECIDE: no catalog row (Q-F1 stays open); Q-TRANSFER-TAPDRILL (tap drill; not in the catalog). The catalog settles the rest (Q-B-6501) |

### Old bucket STEP (28 rows)

| part | new bucket | catalog | catalog gives | still missing | questions answered / new | note |
|---|---|---|---|---|---|---|
| 5504-32-32-FG | STEP | TFA p32 5504-FG | N1_1=2.39, N1_2=2.39, W=2.812 | TAPDRILL1@BORE, TAPDRILL2@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, W@REF); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row) and Q-CONFLICT-TAPDRILL-32 (Air-Way prints 2.19 and 2.20) answered. |
| 5602-02-02-02-FG | STEP | TFA p55 5602-FG | N=0.78, N1_2=0.66, N1_3=0.66, WY=0.562, D=0.188 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5602-06-06-06-FG | STEP | TFA p55 5602-FG | N=1.22, N1_2=1.02, N1_3=1.02, WY=0.875, D=0.406 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5602-12-12-12-FG | STEP | TFA p55 5602-FG | N=1.590, N1_2=1.360, N1_3=1.360, WY=1.312, D=0.719 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5602-16-16-16-FG | STEP | TFA p55 5602-FG | N=1.970, N1_2=1.620, N1_3=1.620, WY=1.625, D=0.938 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5602-20-20-20-FG | STEP | TFA p55 5602-FG | N=2.38, N1_2=1.70, N1_3=1.70, WY=1.875, D=1.25 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5602-24-24-24-FG | STEP | TFA p55 5602-FG | N=2.64, N1_2=2.08, N1_3=2.08, WY=2.562, D=1.5 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row) and Q-CONFLICT-TAPDRILL-24 (Air-Way prints 1.72 and 1.70) answered. |
| 5602-32-32-32-FG | STEP | TFA p55 5602-FG | N=3.000, N1_2=2.390, N1_3=2.390, WY=2.812, D=1.938 | TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N@DRIVE, N1_2@DRIVE, N1_3@DRIVE, WY@REF, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row) and Q-CONFLICT-TAPDRILL-32 (Air-Way prints 2.19 and 2.20) answered. |
| 5604-02-02-02-FG | STEP | TFA p56 5604-FG | N1_1=0.660, N1_2=0.660, N=0.780, W=0.562, D=0.188 | TAPDRILL1@BORE, TAPDRILL2@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N@DRIVE, W@HEX, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5604-12-12-12-FG | STEP | TFA p56 5604-FG | N1_1=1.36, N1_2=1.36, N=1.59, W=1.312, D=0.719 | TAPDRILL1@BORE, TAPDRILL2@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N@DRIVE, W@HEX, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5604-16-16-16-FG | STEP | TFA p56 5604-FG | N1_1=1.620, N1_2=1.620, N=1.970, W=1.625, D=0.938 | TAPDRILL1@BORE, TAPDRILL2@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N@DRIVE, W@HEX, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5604-20-20-20-FG | STEP | TFA p56 5604-FG | N1_1=1.700, N1_2=1.700, N=2.380, W=1.875, D=1.250 | TAPDRILL1@BORE, TAPDRILL2@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N@DRIVE, W@HEX, D@BORE); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5605-02-02-02-FG | STEP | TFA p56 5605-FG | N1_1=0.66, N1_2=0.66, N1_3=0.66, W=0.562 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N1_3@DRIVE, W@HEX); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5605-12-12-12-FG | STEP | TFA p56 5605-FG | N1_1=1.36, N1_2=1.36, N1_3=1.36, W=1.312 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N1_3@DRIVE, W@HEX); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5605-16-16-16-FG | STEP | TFA p56 5605-FG | N1_1=1.620, N1_2=1.620, N1_3=1.620, W=1.625 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N1_3@DRIVE, W@HEX); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5605-20-20-20-FG | STEP | TFA p56 5605-FG | N1_1=1.70, N1_2=1.70, N1_3=1.70, W=1.875 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N1_3@DRIVE, W@HEX); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row). |
| 5605-32-32-32-FG | STEP | TFA p56 5605-FG | N1_1=2.39, N1_2=2.39, N1_3=2.39, W=2.812 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE |  | stays STEP: the catalog gives every body cell (N1_1@DRIVE, N1_2@DRIVE, N1_3@DRIVE, W@HEX); the STEP is now needed only for the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, which the catalog does not print. Becomes NOW if Q-NEW-F1B-TAPDRILL-SCOPE = yes (Q-TRANSFER-TAPDRILL's Air-Way per-size tap drill also for this row) and Q-CONFLICT-TAPDRILL-32 (Air-Way prints 2.19 and 2.20) answered. |
| 6801-08-04-NWO-FG | STEP | TFA p40 6801-NWO-FG | LEG_JIC=1.25, LEG_ORB=1.26, HEXB=0.563, D1=0.391, D2=0.172, Y=0.750 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6801-08-16-NWO-FG | STEP | TFA p41 6801-NWO-FG | LEG_JIC=1.52, LEG_ORB=2.05, HEXB=1.500, D1=0.391, D2=0.844, Y=1.312 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6801-12-20-NWO-FG | STEP | TFA p41 6801-NWO-FG | LEG_JIC=1.97, LEG_ORB=2.25, HEXB=1.875, D1=0.609, D2=1.078, Y=1.625 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6801-16-24-NWO-FG | STEP | TFA p41 6801-NWO-FG | LEG_JIC=2.16, LEG_ORB=2.39, HEXB=2.125, D1=0.844, D2=1.312, Y=1.875 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6801-24-16-NWO-FG | STEP | TFA p41 6801-NWO-FG | LEG_JIC=2.33, LEG_ORB=2.39, HEXB=1.500, D1=1.312, D2=0.844, Y=1.875 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6802-06-10-NWO-FG | STEP | TFA p41 6802-NWO-FG | LEG_JIC=0.880, LEG_ORB=1.520, HEXB=1.000, D1=0.297, D2=0.484, Y=0.875 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6802-08-12-NWO-FG | STEP | TFA p42 6802-NWO-FG | LEG_JIC=1.04, LEG_ORB=1.73, HEXB=1.250, D1=0.391, D2=0.609, Y=1.062 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | stays STEP: the catalog gives every body cell (LEG_JIC@DRIVE, LEG_ORB@DRIVE, HEXB@HEX, D1@BORE, D2@BORE, Y@REF); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6803-08-08-06-NWO-FG | STEP | TFA p59 6803-NWO-FG | LEG1=1.25, LEG2=1.25, LEG3=1.32, HEXB=0.688, Y=0.750, D1=0.391, D2=0.391, D3=0.297 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | stays STEP: the catalog gives every body cell (LEG1@DRIVE, LEG2@DRIVE, LEG3@DRIVE, HEXB@HEX, Y@REF, D1@BORE, D2@BORE, D3@BORE); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6803-08-08-10-NWO-FG | STEP | TFA p59 6803-NWO-FG | LEG1=1.33, LEG2=1.33, LEG3=1.70, HEXB=1.000, Y=0.875, D1=0.391, D2=0.391, D3=0.484 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | stays STEP: the catalog gives every body cell (LEG1@DRIVE, LEG2@DRIVE, LEG3@DRIVE, HEXB@HEX, Y@REF, D1@BORE, D2@BORE, D3@BORE); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6803-24-24-24-NWO-FG | STEP | TFA p59 6803-NWO-FG | LEG1=2.33, LEG2=2.33, LEG3=2.39, HEXB=2.125, Y=1.875, D1=1.312, D2=1.312, D3=1.312 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | stays STEP: the catalog gives every body cell (LEG1@DRIVE, LEG2@DRIVE, LEG3@DRIVE, HEXB@HEX, Y@REF, D1@BORE, D2@BORE, D3@BORE); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |
| 6804-24-24-24-NWO-FG | STEP | TFA p60 6804-NWO-FG | LEG1=2.330, LEG2=2.390, LEG3=2.330, HEXB=2.125, Y=1.875, D1=1.312, D2=1.312, D3=1.312 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | stays STEP: the catalog gives every body cell (LEG1@DRIVE, LEG2@DRIVE, LEG3@DRIVE, HEXB@HEX, Y@REF, D1@BORE, D2@BORE, D3@BORE); the STEP is now needed only for the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW.... Becomes NOW if Q-NEW-F1B-ORBEND = yes (ORB end cells from the table's own rows of the same ORB dash). |

### Old bucket WORK (83 rows)

| part | new bucket | catalog | catalog gives | still missing | questions answered / new | note |
|---|---|---|---|---|---|---|
| 5505-02-02-FG | WORK | TFA p32 5505-FG | N2_1=0.50, N2_2=0.50, W=0.562 | TAPDRILL1@BORE, TAPDRILL2@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a) a tapered NPTF HelixThread on the 135 deg leg AND (c) a female NPTF port on the 135 deg leg (2 x NPTFF, so one port must be angled... |
| 5505-06-06-FG | WORK | TFA p32 5505-FG | N2_1=0.75, N2_2=0.75, W=0.875 | TAPDRILL1@BORE, TAPDRILL2@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a) a tapered NPTF HelixThread on the 135 deg leg AND (c) a female NPTF port on the 135 deg leg (2 x NPTFF, so one port must be angled... |
| 5505-08-08-FG | WORK | TFA p32 5505-FG | N2_1=0.940, N2_2=0.940, W=1.062 | TAPDRILL1@BORE, TAPDRILL2@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a) a tapered NPTF HelixThread on the 135 deg leg AND (c) a female NPTF port on the 135 deg leg (2 x NPTFF, so one port must be angled... |
| 5505-12-12-FG | WORK | TFA p33 5505-FG | N2_1=1.00, N2_2=1.00, W=1.312 | TAPDRILL1@BORE, TAPDRILL2@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a) a tapered NPTF HelixThread on the 135 deg leg AND (c) a female NPTF port on the 135 deg leg (2 x NPTFF, so one port must be angled... |
| 5505-16-16-FG | WORK | TFA p33 5505-FG | N2_1=1.19, N2_2=1.19, W=1.625 | TAPDRILL1@BORE, TAPDRILL2@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a) a tapered NPTF HelixThread on the 135 deg leg AND (c) a female NPTF port on the 135 deg leg (2 x NPTFF, so one port must be angled... |
| 5601-04-04-04-FG | WORK | TFA p55 5601-FG | N_1=1.09, N2=1.09, N1=0.88, W=0.750, D1=0.281, D2=0.281 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5601' (tee: NPTFM, NPTFM run, NPTFF branch; hex W) + new master 5601. Prerequisite (Claude tooling, no user decision): a forged-body extr... |
| 5601-06-06-06-FG | WORK | TFA p55 5601-FG | N_1=1.220, N2=1.220, N1=1.020, W=0.875, D1=0.406, D2=0.406 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5601' (tee: NPTFM, NPTFM run, NPTFF branch; hex W) + new master 5601. Prerequisite (Claude tooling, no user decision): a forged-body extr... |
| 5603-04-04-04-FG | WORK | TFA p55 5603-FG | N1=1.09, N1_2=0.88, N3=1.09, W=0.750, D1_1=0.281, D1_3=0.281 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5603' (tee: NPTFM +X, NPTFF -X, NPTFM branch; hex W@REF) + new master 5603. Prerequisite (Claude tooling, no user decision): a forged-bod... |
| 5603-06-06-06-FG | WORK | TFA p56 5603-FG | N1=1.220, N1_2=1.020, N3=1.220, W=0.875, D1_1=0.406, D1_3=0.406 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5603' (tee: NPTFM +X, NPTFF -X, NPTFM branch; hex W@REF) + new master 5603. Prerequisite (Claude tooling, no user decision): a forged-bod... |
| 5603-08-08-08-FG | WORK | TFA p56 5603-FG | N1=1.470, N1_2=1.230, N3=1.470, W=1.062, D1_1=0.531, D1_3=0.531 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5603' (tee: NPTFM +X, NPTFF -X, NPTFM branch; hex W@REF) + new master 5603. Prerequisite (Claude tooling, no user decision): a forged-bod... |
| 5603-16-16-16-FG | WORK | TFA p56 5603-FG | N1=1.970, N1_2=1.620, N3=1.970, W=1.625, D1_1=0.938, D1_3=0.938 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5603' (tee: NPTFM +X, NPTFF -X, NPTFM branch; hex W@REF) + new master 5603. Prerequisite (Claude tooling, no user decision): a forged-bod... |
| 5603-20-20-20-FG | WORK | TFA p56 5603-FG | N1=2.38, N1_2=1.70, N3=2.38, W=1.875, D1_1=1.250, D1_3=1.250 | TAPDRILL@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5603' (tee: NPTFM +X, NPTFF -X, NPTFM branch; hex W@REF) + new master 5603. Prerequisite (Claude tooling, no user decision): a forged-bod... |
| 5652-02-02-02-02-FG | WORK | TFA p63 5652-FG | N1_1=0.66, N1_2=0.66, N1_3=0.66, N1_4=0.66, W=0.562 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-04-04-04-04-FG | WORK | TFA p63 5652-FG | N1_1=0.88, N1_2=0.88, N1_3=0.88, N1_4=0.88, W=0.750 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-06-06-06-06-FG | WORK | TFA p63 5652-FG | N1_1=1.020, N1_2=1.020, N1_3=1.020, N1_4=1.020, W=0.875 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-08-08-08-08-FG | WORK | TFA p63 5652-FG | N1_1=1.23, N1_2=1.23, N1_3=1.23, N1_4=1.23, W=1.062 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-12-12-12-12-FG | WORK | TFA p63 5652-FG | N1_1=1.360, N1_2=1.360, N1_3=1.360, N1_4=1.360, W=1.312 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-16-16-16-16-FG | WORK | TFA p63 5652-FG | N1_1=1.62, N1_2=1.62, N1_3=1.62, N1_4=1.62, W=1.625 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-20-20-20-20-FG | WORK | TFA p63 5652-FG | N1_1=1.70, N1_2=1.70, N1_3=1.70, N1_4=1.70, W=1.875 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 5652-24-24-24-24-FG | WORK | TFA p63 5652-FG | N1_1=2.08, N1_2=2.08, N1_3=2.08, N1_4=2.08, W=2.561 | TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE, TAPDRILL4@BORE, THDMAJ_A1@DRIVE, THDMAJ_A2@DRIVE, THDMAJ_A3@DRIVE, THDMAJ_A4@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '5652' (cross=True, 4 x NPTFF, conn None like 5605; hex W) + new master 5652. Prerequisite (Claude tooling, no user decision): a forged-bo... |
| 6500-L-04-04-FG | WORK | TFA p34 6500-L-FG | M=0.89, M9=2.16, M12=1.81, CHEX=0.562, Y=0.438, D1=0.172, D2=0.172 |  | Q-B-OTHER-6500L; Q-F1 | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6500': add fold ('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX', 'THDMA... |
| 6500-L-06-06-FG | WORK | TFA p34 6500-L-FG | M=1.06, M9=2.54, M12=2.16, CHEX=0.688, Y=0.562, D1=0.297, D2=0.297 |  | Q-B-OTHER-6500L; Q-F1 | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6500': add fold ('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX', 'THDMA... |
| 6500-L-08-08-FG | WORK | TFA p34 6500-L-FG | M=1.25, M9=2.81, M12=2.38, CHEX=0.875, Y=0.750, D1=0.391, D2=0.391 |  | Q-B-OTHER-6500L; Q-F1 | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6500': add fold ('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX', 'THDMA... |
| 6500-L-12-12-FG | WORK | TFA p34 6500-L-FG | M=1.66, M9=4.30, M12=3.73, CHEX=1.250, Y=1.062, D1=0.609, D2=0.609 |  | Q-B-OTHER-6500L; Q-F1 | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6500': add fold ('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX', 'THDMA... |
| 6500-L-16-16-FG | WORK | TFA p34 6500-L-FG | M=1.81, M9=5.00, M12=4.40, CHEX=1.500, Y=1.312, D1=0.844, D2=0.844 |  | Q-B-OTHER-6500L; Q-F1 | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6500': add fold ('6500L', {'M@DRIVE': 'LEG_M@DRIVE', 'M9@DRIVE': 'LEG_M5@DRIVE', 'M12@DRIVE': 'LEG_M10@DRIVE', 'CHEX@HEX': 'HEXB@HEX', 'THDMA... |
| 6603-06-06-06-FG | WORK | TFA p58 6603-FG | M5_1=1.250, M10_1=0.870, M5_2=1.250, M10_2=0.870, M=1.060, C3_1HEX=0.688, C3_2HEX=0.688, Y=0.562, D1=0.297, D2=0.297, D3=0.297 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE, THDMAJ_B3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg sw / npsm / nwo column tuples + new SPEC '6603' (JICSW x2 run, JICM branch) + new master 6603. That is a gen_tee code change tou... |
| 6603-16-16-16-FG | WORK | TFA p58 6603-FG | M5_1=2.00, M10_1=1.40, M5_2=2.00, M10_2=1.40, M=1.81, C3_1HEX=1.500, C3_2HEX=1.500, Y=1.312, D1=0.844, D2=0.844, D3=0.844 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE, THDMAJ_B3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg sw / npsm / nwo column tuples + new SPEC '6603' (JICSW x2 run, JICM branch) + new master 6603. That is a gen_tee code change tou... |
| 6606-06-06-06-FG | WORK | TFA p58 6606-FG | M5_1=1.250, M10_1=0.870, M5_2=1.250, M10_2=0.870, M5_3=1.250, M10_3=0.870, C3_1HEX=0.688, C3_2HEX=0.688, C3_3HEX=0.688, Y=0.562, D1=0.297 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE, THDMAJ_B3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg sw / npsm / nwo column tuples + new SPEC '6606' (3 x JICSW) + new master 6606. That is a gen_tee code change touching every macr... |
| 6606-12-12-12-FG | WORK | TFA p58 6606-FG | M5_1=1.750, M10_1=1.180, M5_2=1.750, M10_2=1.180, M5_3=1.750, M10_3=1.180, C3_1HEX=1.250, C3_2HEX=1.250, C3_3HEX=1.250, Y=1.062, D1=0.609 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE, THDMAJ_B3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg sw / npsm / nwo column tuples + new SPEC '6606' (3 x JICSW) + new master 6606. That is a gen_tee code change touching every macr... |
| 6801-L-16-16-NWO-FG | WORK | TFA p39 6801-L-NWO-FG | M=1.810, M11=3.060, C4HEX=1.500, Y=1.312, D1=0.844, D2=0.844 | ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6801': add folds ('6801L', M11 -> LEG_ORB) and ('6801LL', M12 -> LEG_ORB), C4HEX -> HEXB, plus ORB_I3 / ORB_THDL columns filled from the STEP... |
| 6801-L-20-20-NWO-FG | WORK | TFA p39 6801-L-NWO-FG | M=2.06, M11=3.48, C4HEX=1.875, Y=1.625, D1=1.078, D2=1.078 | ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6801': add folds ('6801L', M11 -> LEG_ORB) and ('6801LL', M12 -> LEG_ORB), C4HEX -> HEXB, plus ORB_I3 / ORB_THDL columns filled from the STEP... |
| 6801-LL-12-12-NWO-FG | WORK | TFA p39 6801-LL-NWO-FG | M=1.660, M12=3.340, C4HEX=1.250, Y=1.062, D1=0.609, D2=0.609 | ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6801': add folds ('6801L', M11 -> LEG_ORB) and ('6801LL', M12 -> LEG_ORB), C4HEX -> HEXB, plus ORB_I3 / ORB_THDL columns filled from the STEP... |
| 6801-LL-16-16-NWO-FG | WORK | TFA p40 6801-LL-NWO-FG | M=1.81, M12=3.72, C4HEX=1.500, Y=1.312, D1=0.844, D2=0.844 | ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6801': add folds ('6801L', M11 -> LEG_ORB) and ('6801LL', M12 -> LEG_ORB), C4HEX -> HEXB, plus ORB_I3 / ORB_THDL columns filled from the STEP... |
| 6801-LL-20-20-NWO-FG | WORK | TFA p40 6801-LL-NWO-FG | M=2.060, M12=4.410, C4HEX=1.875, Y=1.625, D1=1.078, D2=1.078 | ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee SPEC '6801': add folds ('6801L', M11 -> LEG_ORB) and ('6801LL', M12 -> LEG_ORB), C4HEX -> HEXB, plus ORB_I3 / ORB_THDL columns filled from the STEP... |
| 6802-32-32-NWO-FG | WORK | TFA p42 6802-NWO-FG | LEG_JIC=2.220, LEG_ORB=1.860, HEXB=2.750, D1=1.781, D2=1.781, Y=2.500 | ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee: (1) relax the over-conservative e45 locknut-reach check (for e45 it counts the angled JIC leg's thread radius; PROJECT_STATUS s2: 'fix the check, ... |
| 6805-04-02-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.190, N1=0.660, C4HEX=0.563, Y1=0.562, D=0.172 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-04-04-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.24, N1=0.88, C4HEX=0.563, Y1=0.750, D=0.172 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-06-06-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.41, N1=1.02, C4HEX=0.688, Y1=0.875, D=0.297 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-08-08-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.620, N1=1.230, C4HEX=0.875, Y1=1.062, D=0.391 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-10-08-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.780, N1=1.230, C4HEX=1.000, Y1=1.062, D=0.484 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-12-08-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=1.94, N1=1.23, C4HEX=1.250, Y1=1.062, D=0.609 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-16-12-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=2.050, N1=1.360, C4HEX=1.500, Y1=1.312, D=0.844 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-16-16-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=2.25, N1=1.62, C4HEX=1.500, Y1=1.625, D=0.844 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6805-20-20-NWO-FG | WORK | TFA p42 6805-NWO-FG | M17=2.390, N1=1.700, C4HEX=1.875, Y1=1.875, D=1.078 | TAPDRILL@BORE, THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6805' (90 deg elbow: NWO + NPTFF) + new master 6805. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-06-04-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.250, N=1.090, C4HEX=0.688, Y=0.562, D=0.297, D1=0.281 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-06-06-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.320, N=1.220, C4HEX=0.688, Y=0.750, D=0.297, D1=0.406 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-08-06-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.450, N=1.220, C4HEX=0.875, Y=0.750, D=0.391, D1=0.406 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-08-08-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.540, N=1.470, C4HEX=0.875, Y=0.875, D=0.391, D1=0.531 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-10-08-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.700, N=1.470, C4HEX=1.000, Y=0.875, D=0.484, D1=0.531 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-12-12-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=1.940, N=1.590, C4HEX=1.250, Y=1.062, D=0.609, D1=0.719 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-16-16-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=2.050, N=1.970, C4HEX=1.500, Y=1.312, D=0.844, D1=0.938 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-20-20-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=2.250, N=2.380, C4HEX=1.875, Y=1.625, D=1.078, D1=1.250 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6806-24-24-NWO-FG | WORK | TFA p43 6806-NWO-FG | M7=2.390, N=2.640, C4HEX=2.125, Y=1.875, D=1.312, D1=1.500 | THDMAJ_B@DRIVE, THDMAJ_A@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6806' (90 deg elbow: NWO + NPTFM) + new master 6806. Review-table columns to add for the NWO leg: ORB_I3 (the table has ORB_THDL / ORB_GR... |
| 6807-04-04-NWO-FG | WORK | TFA p43 6807-NWO-FG | M7_1=1.030, M7_2=1.030, C4_1HEX=0.563, C4_2HEX=0.563, Y=0.438, D1=0.172, D2=0.172 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg nwo column tuples + new SPEC '6807' (90 deg elbow: NWO + NWO; both locknut cuts must clear) + new master 6807. That is a gen_tee... |
| 6807-08-06-NWO-FG | WORK | TFA p43 6807-NWO-FG | M7_1=1.450, M7_2=1.340, C4_1HEX=0.875, C4_2HEX=0.688, Y=0.750, D1=0.391, D2=0.297 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg nwo column tuples + new SPEC '6807' (90 deg elbow: NWO + NWO; both locknut cuts must clear) + new master 6807. That is a gen_tee... |
| 6807-08-08-NWO-FG | WORK | TFA p43 6807-NWO-FG | M7_1=1.450, M7_2=1.450, C4_1HEX=0.875, C4_2HEX=0.875, Y=0.750, D1=0.391, D2=0.391 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg nwo column tuples + new SPEC '6807' (90 deg elbow: NWO + NWO; both locknut cuts must clear) + new master 6807. That is a gen_tee... |
| 6807-12-12-NWO-FG | WORK | TFA p43 6807-NWO-FG | M7_1=1.940, M7_2=1.940, C4_1HEX=1.250, C4_2HEX=1.250, Y=1.062, D1=0.609, D2=0.609 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee extension: per-leg nwo column tuples + new SPEC '6807' (90 deg elbow: NWO + NWO; both locknut cuts must clear) + new master 6807. That is a gen_tee... |
| 6809-10-10-NWO-FG | WORK | TFA p44 6809-NWO-FG | M7=1.700, M5=1.620, M10=1.120, C3HEX=1.000, C4HEX=1.000, Y=0.875, D1=0.484, D2=0.484 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6809' (90 deg elbow: NWO + JICSW; first root with both the 'nwo' and 'sw' keys - confirm the elbow clearance code (legs[0] NWO -> ymin, l... |
| 6809-12-12-NWO-FG | WORK | TFA p44 6809-NWO-FG | M7=1.940, M5=1.750, C3HEX=1.250, C4HEX=1.250, Y=1.062, D1=0.609, D2=0.609 | M10@DRIVE, THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6809' (90 deg elbow: NWO + JICSW; first root with both the 'nwo' and 'sw' keys - confirm the elbow clearance code (legs[0] NWO -> ymin, l... |
| 6809-16-16-NWO-FG | WORK | TFA p44 6809-NWO-FG | M7=2.05, M5=2.00, C3HEX=1.500, C4HEX=1.500, Y=1.312, D1=0.844, D2=0.844 | M10@DRIVE, THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6809' (90 deg elbow: NWO + JICSW; first root with both the 'nwo' and 'sw' keys - confirm the elbow clearance code (legs[0] NWO -> ymin, l... |
| 6809-20-20-NWO-FG | WORK | TFA p44 6809-NWO-FG | M7=2.250, M5=2.310, M10=1.680, C3HEX=2.000, C4HEX=1.875, Y=1.625, D1=1.078, D2=1.078 | THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6809' (90 deg elbow: NWO + JICSW; first root with both the 'nwo' and 'sw' keys - confirm the elbow clearance code (legs[0] NWO -> ymin, l... |
| 6810-12-12-NWO-FG | WORK | TFA p44 6810-NWO-FG | M8=1.73, C3HEX=1.250, C4HEX=1.250, Y=1.062, D1=0.609, D2=0.609 | M19@DRIVE, M20@DRIVE, THDMAJ_B1@DRIVE, THDMAJ_B2@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical thread on the 135 deg axis (critic: the JICSW end is a HELIX thread too and the NWO leg must stay on +X) and (... |
| 6901-04-04-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.19, M1=0.79, W3=0.98, CHEX=0.688, C4HEX=0.563, C1HEX=0.562, D1=0.172, D=0.220 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-04-06-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.26, M1=0.99, W3=1.20, CHEX=0.875, C4HEX=0.563, C1HEX=0.750, D1=0.172, D=0.320 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-06-08-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.320, M1=1.040, W3=1.320, CHEX=1.000, C4HEX=0.688, C1HEX=0.750, D1=0.297 | D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-10-12-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.780, M1=1.270, W3=1.620, CHEX=1.250, C4HEX=1.000, C1HEX=1.062, D1=0.484, D=0.620 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-12-06-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.94, M1=1.26, W3=1.47, CHEX=0.875, C4HEX=1.250, C1HEX=1.062, D1=0.609 | D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-12-08-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.94, M1=1.30, W3=1.58, CHEX=1.000, C4HEX=1.250, C1HEX=1.062, D1=0.609, D=0.460 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-12-12-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=1.940, M1=1.300, W3=1.650, CHEX=1.250, C4HEX=1.250, C1HEX=1.062, D1=0.609, D=0.620 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-12-16-NWO-FG | WORK | TFA p45 6901-NWO-FG | N5=2.050, M1=1.540, W3=1.890, CHEX=1.500, C4HEX=1.250, C1HEX=1.312, D1=0.609 | D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-16-12-NWO-FG | WORK | TFA p46 6901-NWO-FG | N5=2.050, M1=1.400, W3=1.750, CHEX=1.250, C4HEX=1.500, C1HEX=1.312, D1=0.844 | D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-16-16-NWO-FG | WORK | TFA p46 6901-NWO-FG | N5=2.05, M1=1.54, W3=1.89, CHEX=1.500, C4HEX=1.500, C1HEX=1.312, D1=0.844 | D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-20-16-NWO-FG | WORK | TFA p46 6901-NWO-FG | N5=2.25, M1=1.70, W3=2.05, CHEX=1.500, C4HEX=1.875, C1HEX=1.625, D1=1.078, D=0.831 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-20-20-NWO-FG | WORK | TFA p46 6901-NWO-FG | N5=2.25, M1=1.73, W3=2.15, CHEX=1.875, C4HEX=1.875, C1HEX=1.625, D1=1.078, D=1.087 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6901-24-24-NWO-FG | WORK | TFA p46 6901-NWO-FG | N5=2.39, M1=1.89, W3=2.31, CHEX=2.125, C4HEX=2.125, C1HEX=1.875, D1=1.312, D=1.317 | THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: New gen_tee SPEC '6901' (90 deg elbow: NWO + NPSMSW; 'nwo' + 'npsm' keys in one root - confirm the clearance code covers both special legs, else gen_tee co... |
| 6902-04-04-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.05, CHEX=0.688, C4HEX=0.563, C1HEX=0.438, D1=0.172, D=0.22 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-06-04-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.14, CHEX=0.688, C4HEX=0.688, C1HEX=0.562, D1=0.297, D=0.22 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-06-06-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.14, CHEX=0.875, C4HEX=0.688, C1HEX=0.562, D1=0.297 | M@DRIVE, W2@HEX, D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-08-06-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.300, CHEX=0.875, C4HEX=0.875, C1HEX=0.750, D1=0.391, D=0.320 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-08-08-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.300, CHEX=1.000, C4HEX=0.875, C1HEX=0.750, D1=0.391 | M@DRIVE, W2@HEX, D@BORE, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-10-08-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.52, CHEX=1.000, C4HEX=1.000, C1HEX=0.875, D1=0.484, D=0.46 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-10-12-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.570, CHEX=1.250, C4HEX=1.000, C1HEX=1.062, D1=0.484, D=0.635 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |
| 6902-16-16-NWO-FG | WORK | TFA p46 6902-NWO-FG | N4=1.860, CHEX=1.500, C4HEX=1.500, C1HEX=1.312, D1=0.844, D=0.780 | M@DRIVE, W2@HEX, THDMAJ_B@DRIVE, THDMAJ_A1@DRIVE |  | unchanged: generator / module code is still needed (Task C work: gen_tee capabilities (a') a straight helical (NPSM) thread on the 135 deg axis (critic) and (b) the NPSM nut hex cut on the angled leg (NWO leg on +X) + ne... |

### DECIDE rows: OMi vs catalog, cell by cell

| part | cell | catalog | OMi | result |
|---|---|---|---|---|
| 6500-04-06-FG | LEG_M10@DRIVE | 0.87 | 0.88 | differ (real; TFA_elbows_diffcheck idx 6) |
| 6500-06-04-FG | HEXB@HEX | 0.563 | 0.562 | rounding (same n/64 fraction) |
| 6500-12-08-FG | LEG_M10@DRIVE | 1.120 | 1.13 | differ (real; TFA_elbows_diffcheck idx 11) |
| 6500-12-16-FG | LEG_M@DRIVE | 1.81 | 1.76 | differ (real; TFA_elbows_diffcheck idx 4) |
| 6500-12-16-FG | LEG_M10@DRIVE | 1.40 | 1.41 | differ (real; TFA_elbows_diffcheck idx 12) |
| 6500-16-12-FG | LEG_M5@DRIVE | 1.91 | 1.95 | differ (real; TFA_elbows_diffcheck idx 18) |
| 6500-16-12-FG | LEG_M10@DRIVE | 1.34 | 1.39 | differ (real; TFA_elbows_diffcheck idx 13) |
| 6501-04-06-FG | M10@DRIVE | 0.875 | 0.880 | rounding (half-up after trailing-zero padding (exact fraction 7/8); TFA_elbows_diffcheck idx 24) |
| 6501-06-06-FG | M10@DRIVE | 0.90 | 0.910 | differ (real; TFA_elbows_diffcheck idx 25) |
| 6501-06-08-FG | M10@DRIVE | 0.958 | 0.960 | rounding (half-up after trailing-zero padding; TFA_elbows_diffcheck idx 26) |
| 6501-08-06-FG | M10@DRIVE | 1.045 | 1.050 | rounding (half-up after trailing-zero padding; TFA_elbows_diffcheck idx 27) |
| 6501-12-12-FG | M10@DRIVE | 1.180 | 1.190 | differ (real; TFA_elbows_diffcheck idx 28) |
| 6501-12-12-FG | Y@HEX | 1.062 | 1.063 | rounding (same n/64 fraction) |
| 6501-24-24-FG | M10@DRIVE | 1.856 | 1.860 | rounding (half-up after trailing-zero padding; TFA_elbows_diffcheck idx 29) |
| 6503-04-04-FG | M10@DRIVE | 0.83 | 0.836 | rounding (cut to 2 decimals (QA_Log #158); TFA_elbows_diffcheck idx 40) |
| 6503-06-06-FG | M10@DRIVE | 1.040 | 1.005 | differ (real; TFA_elbows_diffcheck idx 42) |
| 6503-12-12-FG | M10@DRIVE | 1.300 | 1.298 | rounding (half-up after trailing-zero padding (catalog side); TFA_elbows_diffcheck idx 45) |
| 6503-16-16-FG | N1@DRIVE | - | 1.622 |  |
| 6503-16-16-FG | M5@DRIVE | - | 2.248 |  |
| 6503-16-16-FG | M10@DRIVE | - | 1.654 |  |
| 6503-16-16-FG | C3HEX@HEX | - | 1.500 |  |
| 6503-16-16-FG | Y1@HEX | - | 1.625 |  |
| 6503-16-16-FG | D@BORE | - | 0.844 |  |

(cells not listed are equal; 6503-16-16-FG has no catalog row)

## STEP list items that touch F1b rows

Verdicts: not_replaced 1, partly 116, replaced_by_catalog 15 (of 132 download items; 25 in-repo references unchanged).

| pn | stage | F1b rows | verdict | still needed for |
|---|---|---|---|---|
| 5504-32-32-FG | 1A | 5504-32-32-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-02-02-02-FG | 1A | 5602-02-02-02-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-06-06-06-FG | 1A | 5602-06-06-06-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-12-12-12-FG | 1A | 5602-12-12-12-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-16-16-16-FG | 1A | 5602-16-16-16-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-20-20-20-FG | 1A | 5602-20-20-20-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-24-24-24-FG | 1A | 5602-24-24-24-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5602-32-32-32-FG | 1A | 5602-32-32-32-FG | partly | the tap drill(s) TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5604-02-02-02-FG | 1A | 5604-02-02-02-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5604-12-12-12-FG | 1A | 5604-12-12-12-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5604-16-16-16-FG | 1A | 5604-16-16-16-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5604-20-20-20-FG | 1A | 5604-20-20-20-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5605-02-02-02-FG | 1A | 5605-02-02-02-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5605-12-12-12-FG | 1A | 5605-12-12-12-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5605-16-16-16-FG | 1A | 5605-16-16-16-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5605-20-20-20-FG | 1A | 5605-20-20-20-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 5605-32-32-32-FG | 1A | 5605-32-32-32-FG | partly | the tap drill(s) TAPDRILL1@BORE, TAPDRILL2@BORE, TAPDRILL3@BORE only - legs, hex and bore now come from the catalog; not needed at all if Q-NEW-F1B-TAPDRILL-SCOPE = yes |
| 6801-08-04-NWO-FG | 1A | 6801-08-04-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6801-08-16-NWO-FG | 1A | 6801-08-16-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6801-12-20-NWO-FG | 1A | 6801-12-20-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6801-16-24-NWO-FG | 1A | 6801-16-24-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6801-24-16-NWO-FG | 1A | 6801-24-16-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6802-06-10-NWO-FG | 1A | 6802-06-10-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6802-08-12-NWO-FG | 1A | 6802-08-12-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE, ORB_I3@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6803-08-08-06-NWO-FG | 1A | 6803-08-08-06-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6803-08-08-10-NWO-FG | 1A | 6803-08-08-10-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6803-24-24-24-NWO-FG | 1A | 6803-24-24-24-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6804-24-24-24-NWO-FG | 1A | 6804-24-24-24-NWO-FG | partly | the ORB end cells ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE only - legs, body hex, bores (and the locknut hex check) now come from the catalog; not needed at all if Q-NEW-F1B-ORBEND = yes |
| 6802-32-32-NWO-FG | 1B | 6802-32-32-NWO-FG | partly | ORB end cells (ORB_THDL / ORB_GRVDIA / ORB_GRVW / ORB_I3 at -32) and the shape behind Q-NEW-6802E45CHECK (e45 locknut reach, corner neck trim); legs (= MS51528), body hex and locknut hex, bores now from the catalog |
| 5505-08-08-FG | 2 | 5505-08-08-FG | partly | pilot of the new 45 deg female pipe elbow: forged body shape (forged-body extractor / OCP closed loop), the angled female NPTF port and its helix (Q-NEW-ANGLEDFEMALE / Q-NEW-ANGLEDHELIX), the tap drills unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 5601-06-06-06-FG | 2 | 5601-06-06-06-FG | partly | pilot of the new female-branch pipe tee: forged body shape (extractor / closed loop), the female branch tap drill unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 5603-08-08-08-FG | 2 | 5603-08-08-08-FG | partly | pilot of the new female-run pipe tee: forged body shape (extractor / closed loop), the female run tap drill unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 5652-08-08-08-08-FG | 2 | 5652-08-08-08-08-FG | partly | pilot of the new female pipe cross: forged cross body (extractor / closed loop), the four tap drills unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 6500-L-08-08-FG | 2 | 6500-L-08-08-FG | partly | fold shape: whether the extra length is the forged swivel arm (Q-NEW-FOLD-6500L); the catalog gives every dimension of this part and the OMi column reading (Q-B-OTHER-6500L), not the shape |
| 6603-06-06-06-FG | 2 | 6603-06-06-06-FG | partly | pilot of the new two-swivel tee: forged body, two swivel legs on one part (Q-NEW-PERLEGSW), swivel end check against SWIV_MEAS; this part's own dimensions now come from the catalog |
| 6606-06-06-06-FG | 2 | 6606-06-06-06-FG | partly | pilot of the new three-swivel tee: forged body, three swivel legs (Q-NEW-PERLEGSW), swivel end check against SWIV_MEAS; this part's own dimensions now come from the catalog |
| 6801-L-08-08-NWO-FG | 2 | 6801-L-16-16-NWO-FG, 6801-L-20-20-NWO-FG | partly | fold shape (where the extra ORB-leg length goes, Q-NEW-FOLD-6801L) and the ORB_I3 / ORB_THDL values the fold needs (not in the 6801-L table, not in the catalog); the catalog now gives Brennan's -08-08 values (M 1.25, M7 1.97, C HEX 0.875, Y FLATS 0.750) |
| 6801-L-16-16-NWO-FG | 2 | 6801-L-16-16-NWO-FG | partly | fold shape (where the extra ORB-leg length goes, Q-NEW-FOLD-6801L) and the ORB_I3 / ORB_THDL values the fold needs (not in the 6801-L table, not in the catalog); this part's own dimensions now come from the catalog |
| 6801-LL-08-08-NWO-FG | 2 | 6801-LL-12-12-NWO-FG, 6801-LL-16-16-NWO-FG, 6801-LL-20-20-NWO-FG | partly | fold shape (where the extra ORB-leg length goes, Q-NEW-FOLD-6801L) and the ORB_I3 / ORB_THDL values the fold needs (not in the 6801-LL table, not in the catalog); the catalog now gives Brennan's -08-08 values (M 1.250, M7 2.480, C HEX 0.875, Y FLATS 0.750) and shows the Air-Way 6801-LL-08-08-NWO-FG row is the -08-10 row (the critic's open point) |
| 6801-LL-12-12-NWO-FG | 2 | 6801-LL-12-12-NWO-FG | partly | fold shape (where the extra ORB-leg length goes, Q-NEW-FOLD-6801L) and the ORB_I3 / ORB_THDL values the fold needs (not in the 6801-LL table, not in the catalog); this part's own dimensions now come from the catalog |
| 6805-08-08-NWO-FG | 2 | 6805-08-08-NWO-FG | partly | pilot of the new ORB x female pipe elbow: forged body, adjustable-ORB end (thread length / groove / I3) and the tap drill unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 6806-08-08-NWO-FG | 2 | 6806-08-08-NWO-FG | partly | pilot of the new ORB x male pipe elbow: forged body, adjustable-ORB end (thread length / groove / I3) unless Q-TRANSFER-ENDLIB = yes; this part's own dimensions now come from the catalog |
| 6807-08-08-NWO-FG | 2 | 6807-08-08-NWO-FG | partly | pilot of the new ORB x ORB elbow: forged body, two adjustable-ORB legs on one part (Q-NEW-PERLEGSW), ORB end details; this part's own dimensions now come from the catalog |
| 6809-10-10-NWO-FG | 2 | 6809-10-10-NWO-FG | partly | pilot of the new ORB x JIC swivel elbow: forged body, ORB end and swivel end checks; this part's own dimensions now come from the catalog |
| 6810-12-12-NWO-FG | 2 | 6810-12-12-NWO-FG | partly | pilot of the new 45 deg ORB x JIC swivel: forged 45 deg body, swivel nut and helix on the 45 deg leg (Q-NEW-ANGLEDNUT / Q-NEW-ANGLEDHELIX), the 45 deg swivel reference point (M19 / M20 pairing uncertain); this part's own dimensions now come from the catalog |
| 6901-06-08-NWO-FG | 2 | 6901-06-08-NWO-FG | partly | pilot of the new ORB x NPSM swivel elbow: forged body, NPSM swivel end, ORB end; this size prints the NPSM bore as a range (0.44/0.46); this part's own dimensions now come from the catalog |
| 6902-08-08-NWO-FG | 2 | 6902-08-08-NWO-FG | partly | pilot of the new 45 deg ORB x NPSM swivel: forged 45 deg body, NPSM nut / helix on the 45 deg leg (Q-NEW-ANGLEDNUT / Q-NEW-ANGLEDHELIX), the 45 deg reference point of M@DRIVE / W2@HEX (pairing uncertain); this size prints the NPSM bore as a range (0.44/0.46); this part's own dimensions now come from the catalog |
| 5505-02-02-FG | 3 | 5505-02-02-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5505-06-06-FG | 3 | 5505-06-06-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5505-12-12-FG | 3 | 5505-12-12-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5505-16-16-FG | 3 | 5505-16-16-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5601-04-04-04-FG | 3 | 5601-04-04-04-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5603-04-04-04-FG | 3 | 5603-04-04-04-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5603-06-06-06-FG | 3 | 5603-06-06-06-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5603-16-16-16-FG | 3 | 5603-16-16-16-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5603-20-20-20-FG | 3 | 5603-20-20-20-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-02-02-02-02-FG | 3 | 5652-02-02-02-02-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-04-04-04-04-FG | 3 | 5652-04-04-04-04-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-06-06-06-06-FG | 3 | 5652-06-06-06-06-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-12-12-12-12-FG | 3 | 5652-12-12-12-12-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-16-16-16-16-FG | 3 | 5652-16-16-16-16-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-20-20-20-20-FG | 3 | 5652-20-20-20-20-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 5652-24-24-24-24-FG | 3 | 5652-24-24-24-24-FG | partly | end details only (tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6603-16-16-16-FG | 3 | 6603-16-16-16-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6606-12-12-12-FG | 3 | 6606-12-12-12-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6801-L-20-20-NWO-FG | 3 | 6801-L-20-20-NWO-FG | partly | the ORB end cells ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE (and ORB_I3 / ORB_THDL for the fold) - not in the catalog; all body cells now from the catalog |
| 6801-LL-16-16-NWO-FG | 3 | 6801-LL-16-16-NWO-FG | partly | the ORB end cells ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE (and ORB_I3 / ORB_THDL for the fold) - not in the catalog; all body cells now from the catalog |
| 6801-LL-20-20-NWO-FG | 3 | 6801-LL-20-20-NWO-FG | partly | the ORB end cells ORB_GRVDIA@DRIVE, ORB_GRVW@DRIVE (and ORB_I3 / ORB_THDL for the fold) - not in the catalog; all body cells now from the catalog |
| 6805-04-02-NWO-FG | 3 | 6805-04-02-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-04-04-NWO-FG | 3 | 6805-04-04-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-06-06-NWO-FG | 3 | 6805-06-06-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-10-08-NWO-FG | 3 | 6805-10-08-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-12-08-NWO-FG | 3 | 6805-12-08-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-16-12-NWO-FG | 3 | 6805-16-12-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-16-16-NWO-FG | 3 | 6805-16-16-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6805-20-20-NWO-FG | 3 | 6805-20-20-NWO-FG | partly | end details only (ORB end, tap drill, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-06-04-NWO-FG | 3 | 6806-06-04-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-06-06-NWO-FG | 3 | 6806-06-06-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-08-06-NWO-FG | 3 | 6806-08-06-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-10-08-NWO-FG | 3 | 6806-10-08-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-12-12-NWO-FG | 3 | 6806-12-12-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-16-16-NWO-FG | 3 | 6806-16-16-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-20-20-NWO-FG | 3 | 6806-20-20-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6806-24-24-NWO-FG | 3 | 6806-24-24-NWO-FG | partly | end details only (ORB end, thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6807-04-04-NWO-FG | 3 | 6807-04-04-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6807-08-06-NWO-FG | 3 | 6807-08-06-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6807-12-12-NWO-FG | 3 | 6807-12-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6809-12-12-NWO-FG | 3 | 6809-12-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also M10@DRIVE (catalog value suspect - see catalog issues; with Q-TRANSFER-ENDLIB = yes the nose follows from the nut face M5 and the swivel end library) |
| 6809-16-16-NWO-FG | 3 | 6809-16-16-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also M10@DRIVE (catalog value suspect - see catalog issues; with Q-TRANSFER-ENDLIB = yes the nose follows from the nut face M5 and the swivel end library) |
| 6809-20-20-NWO-FG | 3 | 6809-20-20-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-04-04-NWO-FG | 3 | 6901-04-04-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-04-06-NWO-FG | 3 | 6901-04-06-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-10-12-NWO-FG | 3 | 6901-10-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-12-06-NWO-FG | 3 | 6901-12-06-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also D@BORE (catalog prints a min/max range) |
| 6901-12-08-NWO-FG | 3 | 6901-12-08-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-12-12-NWO-FG | 3 | 6901-12-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-12-16-NWO-FG | 3 | 6901-12-16-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also D@BORE (catalog prints a min/max range) |
| 6901-16-12-NWO-FG | 3 | 6901-16-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also D@BORE (catalog prints a min/max range) |
| 6901-16-16-NWO-FG | 3 | 6901-16-16-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also D@BORE (catalog prints a min/max range) |
| 6901-20-16-NWO-FG | 3 | 6901-20-16-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-20-20-NWO-FG | 3 | 6901-20-20-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6901-24-24-NWO-FG | 3 | 6901-24-24-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog |
| 6902-04-04-NWO-FG | 3 | 6902-04-04-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6902-06-04-NWO-FG | 3 | 6902-06-04-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6902-06-06-NWO-FG | 3 | 6902-06-06-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX; D@BORE (catalog prints a min/max range) |
| 6902-08-06-NWO-FG | 3 | 6902-08-06-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6902-10-08-NWO-FG | 3 | 6902-10-08-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6902-10-12-NWO-FG | 3 | 6902-10-12-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6902-16-16-NWO-FG | 3 | 6902-16-16-NWO-FG | partly | end details only (thread majors) - from the end libraries if Q-TRANSFER-ENDLIB = yes, then this download is not needed; legs, hexes and bores now from the catalog; also the uncertain-pairing cells M@DRIVE, W2@HEX |
| 6500-04-06-FG | CONDITIONAL | 6500-04-06-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on LEG_M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6500-06-04-FG | CONDITIONAL | 6500-06-04-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6500-FG p34, which OMi equals |
| 6500-12-08-FG | CONDITIONAL | 6500-12-08-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on LEG_M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6500-12-16-FG | CONDITIONAL | 6500-12-16-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on LEG_M@DRIVE, LEG_M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6500-16-12-FG | CONDITIONAL | 6500-16-12-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on LEG_M5@DRIVE, LEG_M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6500-L-04-04-FG | CONDITIONAL | 6500-L-04-04-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6500-L-FG p34, which OMi equals |
| 6500-L-06-06-FG | CONDITIONAL | 6500-L-06-06-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6500-L-FG p34, which OMi equals |
| 6500-L-12-12-FG | CONDITIONAL | 6500-L-12-12-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6500-L-FG p34, which OMi equals |
| 6500-L-16-16-FG | CONDITIONAL | 6500-L-16-16-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6500-L-FG p34, which OMi equals |
| 6501-04-06-FG | CONDITIONAL | 6501-04-06-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-06-06-FG | CONDITIONAL | 6501-06-06-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6501-06-08-FG | CONDITIONAL | 6501-06-08-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-08-06-FG | CONDITIONAL | 6501-08-06-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-08-08-FG | CONDITIONAL | 6501-08-08-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-08-10-FG | CONDITIONAL | 6501-08-10-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-12-12-FG | CONDITIONAL | 6501-12-12-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6501-16-16-FG | CONDITIONAL | 6501-16-16-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-20-20-FG | CONDITIONAL | 6501-20-20-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6501-24-24-FG | CONDITIONAL | 6501-24-24-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6501-FG p35, which OMi equals |
| 6503-04-04-FG | CONDITIONAL | 6503-04-04-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6503-FG p38, which OMi equals; caveat: if Q-TRANSFER-TAPDRILL = no, the row's tap drill would still have to be measured on a STEP (not a stated purpose of this item) |
| 6503-06-06-FG | CONDITIONAL | 6503-06-06-FG | partly | only as a tie-breaker if the user wants the OMi / catalog difference on M10@DRIVE measured (Q-NEW-F1B-CATDIFF); every other cell is settled by the catalog |
| 6503-12-12-FG | CONDITIONAL | 6503-12-12-FG | replaced_by_catalog | its purpose (Brennan -FG dimensions if Q-F1 = no; otherwise a cross-check) is met by the catalog row 6503-FG p38, which OMi equals; caveat: if Q-TRANSFER-TAPDRILL = no, the row's tap drill would still have to be measured on a STEP (not a stated purpose of this item) |
| 6503-16-16-FG | CONDITIONAL | 6503-16-16-FG | not_replaced | Brennan prints no 6503-16-16-FG - the catalog cannot stand in for this -FG STEP if Q-F1 = no |

## Issues found

Catalog:
- 6809-12-12-NWO-FG (TFA p44) M LGTH 1.370: nose depth M6 - M = 1.75 - 1.37 = 0.38, while the -12 swivel nose depth is 0.57 everywhere else (6500-12-12 / 6501-12-12 catalog, Brennan STEP NOSETIP_B 0.57); Air-Way plain 6809-12-12 M10 1.19 - probable catalog error (WORK row; the value is not usable as printed)
- 6809-16-16-NWO-FG (TFA p44) M LGTH 1.45: nose depth 2.00 - 1.45 = 0.55 vs 0.60 measured on the Brennan -16 swivel (6500-16-16 catalog M4 1.40) - doubtful
- 6503-06-06-FG (TFA p38) M4 LGTH 1.040: nose depth 1.380 - 1.040 = 0.34 vs 0.375 on every other -06 swivel the catalog prints with 3 decimals; OMi 1.005 gives 0.375 (already in TFA_elbows_diffcheck idx 42)
- 5652-24-24-24-24-FG (TFA p63) Y FLATS printed 2.561; 2-9/16 prints 2.562 elsewhere (5604-24-24-24-FG, 5605-24-24-24-FG) - probable typo, kept as printed
- 6603-04-04-04-FG (TFA p58, not an F1b row) M2 LGTH printed 1.0029 - typo (1.00); header typos kept as printed: 5602 'N1 LGBTH', 5652 'AD NPTF' (= A3)
- 6500-FG drawing p34 labels the nut-face length M5 while the header prints M6 (already in the match file)

Air-Way:
- Air-Way 6801-LL-08-08-NWO-FG (review DesignTable_6801LL, a BUILD row) holds the -08-10 values (M 1.31, M12 3.25, C4HEX 1, D2 0.48 = Air-Way 6801-LL-08-10-NWO); Brennan 6801-LL-08-08-NWO-FG prints M 1.250, M7 2.480, C HEX 0.875, B2 DRILL 0.391
- Air-Way's own -FG rows of 6901 print a larger body hex C1HEX than Brennan's Y FLATS (0.75 / 0.75 / 0.88 / 1.11 vs 0.562 / 0.562 / 0.750 / 0.875) and other N5 / M1 / W3 values - Air-Way's forging is not Brennan's

OMi:
- OMi M 1 (swivel nose) equals Air-Way M10, not the Brennan catalog M4, on the 6500 / 6501 noses (TFA_elbows_diffcheck finding 1) - in F1b: 6500-04-06, -12-08, -12-16, -16-12, 6501-06-06, -12-12
- 6503-16-16-FG: OMi part (Items row 1981, with dimensions) that Brennan's catalog does not list (also 6503-20-20 / -24-24 / -32-32, outside F1b)

Outside this task (observation only): 51 cells of BUILD rows that are not F1b rows (Air-Way values) differ from the catalog, e.g. 5604-06-06-06-FG W@HEX 0.81 vs catalog Y FLATS 0.875; 5604-24-24-24-FG D@BORE 1.68 vs catalog A3 DRILL 1.500; 5605-06-06-06-FG W@HEX 0.75 vs catalog Y FLATS 0.875; 6801-04-02-NWO-FG LEG_ORB@DRIVE 1.03 vs catalog M7 LGTH 0.92; 6801-10-08-NWO-FG LEG_ORB@DRIVE 1.60 vs catalog M7 LGTH 1.54. The largest groups are 6500 LEG_M10@DRIVE x11, 6801L M11@DRIVE x3, 6805 M17@DRIVE x3, 6901 M1@DRIVE x3. They are listed in `built_rows_differing_from_catalog`.

## Files

- `tools/_out/brennan_catalog_20261001/impact/F1b.json` - the full result
- `tools/_out/brennan_catalog_20261001/impact/F1b_work/build_F1b.py`, `pairs_F1b.py`, `make_md_F1b.py` - scripts (read-only on every source)
- `tools/_out/brennan_catalog_20261001/impact/F1b_work/png/` - the catalog drawings that were looked at (clip_p*.png)
- inputs with sha256: see `inputs` in the JSON
