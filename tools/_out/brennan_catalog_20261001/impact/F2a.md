# F2a - what the Brennan catalogs change (Task C group F2, first half)

Created 2026-10-01T23:10:23 by `tools/_out/brennan_catalog_20261001/impact/build_F2a.py` (read-only on every input). Full detail per row and cell: `F2a.json`.

Scope: the 281 Task C rows of group F2 sorted by config, first half = 141 rows (`0304-C-02` ... `5404-L-04X3.000`; the boundary row `5404-L-04X3.000` is also in F2b). Rules: Q-NEW-BRENNANCAT treated as YES; Q-BRENNAN-ONLY still formally open; OMi + Brennan catalog = one source (a value from either is ASSUMED); OMi file first where both print; rounding-only differences are not differences; a printed range is never reduced to one value.

## Result

- 141 F2a rows: 121 have a catalog row (85 exact, 36 documented variants). Moves: DECIDE->DECIDE 7, DECIDE->NOW 3, SCOPE->SCOPE 32, STEP->DECIDE 5, STEP->NOW 12, STEP->STEP 22, WORK->WORK 60. 15 rows become NOW (2406 x8 incl. 2406-08-08, 5404 x5, 2501-24-32-FG, 2503-24-20-FG), 5 STEP rows become DECIDE (only tap drills / a drill range left: 1405-04-06, 1405-08-12, 5000-06-02 / -16-08 / -24-20). The catalog answers Q-B-ELBOW, Q-B-TEE, Q-B-OTHER-0304 / -0306 / -TEE2 and confirms the 0304-C / 0306 / 2403-LH part numbers; it shows Brennan sells the swept -Tube elbows. Step list (98 items): not_replaced 18, partly 44, replaced_by_catalog 36.
- Cells listed: 856. The catalog gives a usable dimension for 321 of them (244 with a certain pairing, 77 likely) plus 99 thread designations; 96 swept-elbow cells are printed but not paired (uncertain); 1 drill is printed as a range; 257 cells have no catalog column (tap drills, bulkhead I1, flange head O, bores of the flange parts, JIC / NPTF end geometry, hex length T20, bulkhead collar); 82 cells belong to the 20 rows without a catalog row.
- OMi: 112 cells compared, 108 agree, 4 REAL differences (2501-24-32-FG D1, 2706-LN-08-06 L25 and D, 0304-C-32 hex) - OMi kept, reported in Q-NEW-F2A-OMIvsCAT. Air-Way: 18 cells compared (per-size NPSM nut-hex context and the 2706-08-06 twin row), 17 agree, 1 differs (2706-LN-08-06 L: Air-Way 2.34 vs catalog 2.410 vs OMi 2.400). None of the F2a parts has an Air-Way row of its own.
- Every catalog table used is `verified: true` in catalog_verified.json. No part number was guessed: hits are exact, LN_form (TFA_straights.json pn rule) or R1 swept = -Tube (Flange.json pn rule).

## Bucket moves

| move | rows | configs |
|---|---|---|
| DECIDE->DECIDE | 7 | 2502-32-32-FG, 2603-02-02-02-FG, 2705-LN-06-04, 2706-06-04, 2706-32-32, 2706-LN-06-04, 2706-LN-08-06 |
| DECIDE->NOW | 3 | 2406-08-08, 2501-24-32-FG, 2503-24-20-FG |
| SCOPE->SCOPE | 32 | 1703-08-08-Tube, 1703-12-12-Tube, 1703-12-16-Tube, 1703-16-16-Tube, 1703-16-20-Tube, 1703-16-24-Tube, 1703-20-16-Tube, 1703-20-20-Tube, 1703-20-24-Tube, 1703-24-20-Tube, 1703-24-24-Tube, 1703-24-32-Tube ... (32 rows) |
| STEP->DECIDE | 5 | 1405-04-06, 1405-08-12, 5000-06-02, 5000-16-08, 5000-24-20 |
| STEP->NOW | 12 | 2406-04-02, 2406-04-04, 2406-04-08, 2406-06-10, 2406-10-16, 2406-12-04, 2406-12-12, 5404-16-04, 5404-20-12, 5404-24-12, 5404-32-12, 5404-32-16 |
| STEP->STEP | 22 | 1405-20-24, 1700-20-16, 1700-24-20, 1700-32-24, 2406-06-12, 2502-20-16-FG, 2700-02-02, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-02-02, 2700-LN-04-02, 2700-LN-08-06, 2700-LN-10-08, 2700-LN-12-10, 2701-02-02-FG, 2701-05-05-FG, 2705-04-02, 2705-LN-04-02, 2706-04-02, 2706-LN-04-02 |
| WORK->WORK | 60 | 0304-C-02, 0304-C-03, 0304-C-04, 0304-C-05, 0304-C-06, 0304-C-08, 0304-C-10, 0304-C-12, 0304-C-14, 0304-C-16, 0304-C-20, 0304-C-24 ... (60 rows) |

New buckets: DECIDE 12, NOW 15, SCOPE 32, STEP 22, WORK 60 (old: DECIDE 10, SCOPE 32, STEP 39, WORK 60).

Why the moves:

- **STEP -> NOW (12)**: 2406-04-02 / -04-04 / -04-08 / -06-10 / -10-16 / -12-04 / -12-12 and 5404-16-04 / -20-12 / -24-12 / -32-12 / -32-16. Their STEP was only for L, hex and bore(s); TFA p7 / p11 print all of them (pairings certain: drawing letters + Air-Way agreement 45-46 of 47 resp. 23-25 of 25 rows + the in-repo 2406-08-08 STEP = catalog). The in-memory generator paper check builds every one (2406-12-04: the female -12 port reaches into the -04 male thread zone, radial wall 0.035 - the generator says OK).
- **DECIDE -> NOW (3)**: 2406-08-08 (its only gate was Q-BRENNAN-ONLY; catalog = the in-repo STEP reading), 2501-24-32-FG and 2503-24-20-FG (only gate Q-B-ELBOW, answered YES by the catalog letters; catalog = OMi on every leg / hex / bore except 2501-24-32-FG D1 1.938 vs OMi 1.940, OMi kept).
- **STEP -> DECIDE (5)**: 1405-04-06, 1405-08-12, 5000-06-02, 5000-16-08, 5000-24-20 - the catalog gives everything except the female pipe tap drills (no tap column on TFA p4 / p10) and, on 1405-04-06, the bore (printed as the range .32/.34). Gates: Q-TRANSFER-TAPDRILL (+ Q-CONFLICT-TAPDRILL-24 on 5000-24-20, + Q-NEW-F2A-DRILLRANGE on 1405-04-06). If the user says no, they go back to STEP. The paper check builds all five with the Air-Way per-size tap drills.
- **STEP stays STEP (22)**: 12 parts are not in the catalog (1405-20-24, 2406-06-12, 2502-20-16-FG, 2700-04-02 / -08-06 / -10-08 / -12-10 and their -LN rows, 2705-04-02, 2705-LN-04-02); the other 10 still need a cell no catalog prints: 1700 x3 (head O, bore D; Q-NEW-1700BODY), 2700-02-02 / 2700-LN-02-02 / 2706-04-02 / 2706-LN-04-02 (I1 at the -02 bulkhead), 2701-02-02-FG / -05-05-FG (bulkhead i2, collar K1 / O).
- **DECIDE stays DECIDE (7)**: 2502-32-32-FG (Q-HX, tap drill -32), 2603-02-02-02-FG (Q-HX), 2705-LN-06-04 (I1 + tap drill transfers), 2706-06-04 / 2706-32-32 / 2706-LN-06-04 / 2706-LN-08-06 (Q-TRANSFER-I1). The catalog prints no I1 and no tap drill; where it has the part it equals OMi (2706-LN-08-06: two small REAL differences). Q-B-ELBOW / Q-B-TEE on these rows are answered.
- **WORK (60) / SCOPE (32)** unchanged - code or a scope answer is still needed; the catalog supplies the data (see the per-row table).

## Questions the catalog answers

| question (level) | answer from the catalog | rows | evidence |
|---|---|---|---|
| (no Task C id) "confirm Brennan lists 2403-LH-24-24" (answered) | CONFIRMED - TFA p5 table 2403-LH prints 2403-LH-24-24 | 1: 2403-LH-24-24 | catalog_index.json |
| Q-B-ELBOW (answered) | YES - settled by the catalog's own letters: OMi 'M 1 Size' = M = the JIC (1st-dash) leg, 'L 1 Size' = L = the pipe (2nd-dash) leg | 4: 2501-24-32-FG, 2501-40-40-FG, 2502-32-32-FG, 2503-24-20-FG | TFA p23 / p25 / p26 drawings; match/TFA_elbows.json column_maps: 2501-FG M -> M1 44/44, L -> L1 44/44; 2502-FG 20/20, 20/20; 2503-FG 31/31, 31/31 (all certain); this part: catalog M / L = OMi M 1 / L 1 |
| Q-B-OTHER-0304 (answered) | YES - OMi Overall Length = the cap length (catalog L LGTH) and Hex Flat = the cap hex (catalog C HEX) | 13: 0304-C-02, 0304-C-03, 0304-C-04, 0304-C-05, 0304-C-06 ... | TFA p65 0304-C drawing (L = overall cap length, C HEX); match/TFA_tees_caps.json column_maps 0304-C: L LGTH -> Overall Length 13/13 certain, C HEX -> Hex Flat 12/13 certain (-32: 2.880 vs 2.875) |
| Q-B-OTHER-0306 (answered) | YES - OMi Overall Length = the nut thickness (catalog W WIDTH) and Hex Flat = the nut hex (catalog C HEX) | 12: 0306-02, 0306-03, 0306-04, 0306-05, 0306-06 ... | TFA p65 0306 drawing (W = width, C HEX); match/TFA_tees_caps.json: W WIDTH -> Overall Length 13/13, C HEX -> Hex Flat 13/13 (both certain). The thickness also equals Brennan 0306-N (NWO nut) W at every size - Brennan uses one thickness for both nuts, which explains the Task C observation |
| Q-B-OTHER-TEE2 (answered) | YES - OMi M 1 / M 2 / L 1 = legs of ends 1 / 2 / 3, Hex Flat = body flats, Side n ID = drill of end n; this part's catalog values equal OMi | 3: 2606-12-12-12-FG, 2609-08-08-08-FG, 2611-08-08-08-FG | match/TFA_tees_caps.json (2606 L LGTH = OMi M 2 certain; 2609 M LGTH = M 1 certain; 2611 M / L / L1 = M 1 / M 2 / L 1 certain; ties only on symmetric pairs, numerically irrelevant); TFA p51-52 drawings |
| Q-B-TEE (answered) | YES for this part - the branch leg is OMi 'L 1 Size' = catalog M3 (certain on the 2 discriminating rows); M 1 / M 2 order cannot be tested (always equal) and is irrelevant here (all three legs 0.77) | 1: 2603-02-02-02-FG | match/TFA_tees_caps.json 2603-FG column_maps; TFA p49-50 |
| Q-BRENNAN-ONLY (not_needed) | NOT NEEDED for this row: every dimension it needed comes from the catalog (Q-NEW-BRENNANCAT treated as yes); no STEP is the sole source any more | 36: 0304-C-04, 0304-C-05, 0304-C-06, 0304-C-10, 0304-C-12 ... | cells |
| Q-BRENNAN-ONLY (partly) | PARTLY - not needed for the cells the catalog gives; it gates this row only if the user rejects Q-TRANSFER-TAPDRILL / Q-NEW-F2A-DRILLRANGE (then the STEP is the sole source of those cells) | 5: 1405-04-06, 1405-08-12, 5000-06-02, 5000-16-08, 5000-24-20 | cells |
| Q-NEW-5404L-XLEN (partly) | SUPPORTED, not settled: in Brennan's own long-nipple numbering the X-number is the overall length (5404-N-04X2.000 L 2.000, 5404-N-04X3.000 L 3.000, every 5404-N row L = X), the same as the Air-Way 5404N convention; but Brennan prints no 5404-L (with hex), so the reading for 5404-L stays the user's call | 2: 5404-L-04X2.000, 5404-L-04X3.000 | TFA p11-12 table 5404-N (85 rows, L LGTH = X-number on every row) |
| Q-NEW-BRENNANPN (answered) | CONFIRMED for 0304-C: Brennan lists the JIC cap nut under this exact number | 25: 0304-C-02, 0304-C-03, 0304-C-04, 0304-C-05, 0304-C-06 ... | TFA p65 table 0304-C (0304-C-02 ... -40, -48 printed blank) |
| Q-NEW-BRENNANPN (partly) | PARTLY - NOT in the TFA catalog: Brennan prints no 5404-L long HEX nipple; its long nipples are 5404-N (round, no hex column). Still open: check brennaninc.com or get a drawing from OMi's supplier | 2: 5404-L-04X2.000, 5404-L-04X3.000 | TFA p11-12 tables 5404 (hex nipple, standard lengths) and 5404-N (MP-MP straight nipple long: PIPE O.D., A1/A2 NPTF, A1/A2 DRILL, L LGTH - no C HEX) |
| Q-SCOPE-TUBE (informs_only) | NOT answered (scope is the user's call) - but the premise "no source of any kind / no Brennan equivalent known" is outdated: Brennan sells this swept elbow as 1703-08-08 (Flange p4) and prints L1 / L2 / A/F; bend radius, tube OD and wall are still unprinted (a Brennan STEP of the swept part could give them) | 32: 1703-08-08-Tube, 1703-12-12-Tube, 1703-12-16-Tube, 1703-16-16-Tube, 1703-16-20-Tube ... | match/Flange.json pn rule R1 (certain); Flange p4-5 swept tables 1703 / 1704 |
| Q-TRANSFER-NUTHEX (not_needed) | NOT NEEDED for this part - the catalog prints its own swivel-nut hex (C HEX), equal to the Air-Way per-size value after rounding and to the Brennan-measured NPSM_MEAS AF; accepting the transfer would only add Air-Way as a second source (route to VERIFIED for that cell) | 6: 1502-12-08-FG, 1504-20-20-FG, 1601-20-20-20-FG, 1602-04-04-04-FG, 1602-16-16-16-FG, 1602-20-20-20-FG | see the nut-hex cells (airway_compare) |

Levels: answered = settled by the catalog; not_needed = the question no longer gates the row; partly = evidence, still the user's call; informs_only = premise corrected, question still open.

Not answered by the catalog (no such column printed, or a process decision): Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24 / -32, Q-TRANSFER-I1, Q-TRANSFER-LN (evidence only: the TFA catalog prints no -LN rows, OMi -LN body values equal the plain catalog row on 90 of 95 LN cells (87 equal, 3 rounding-only, 5 real - TFA_straights.json summary LN_duplicate_cells)), Q-TRANSFER-FLG61-O, Q-NEW-1700BODY, Q-HX, Q-HANDMADE, Q-NEW-ASME40, Q-NEWMASTER-*, Q-NEW-FLG61LEG / -ANGLEDHELIX / -ANGLEDFEMALE / -PERLEGSW, Q-TRANSFER-5404L-X3, Q-SCOPE-TUBE; optional Q-CALIPER / Q-NEW-STDBUY / Q-MS-FG unaffected (catalog = OMi = MS on 2502-32-32-FG and 2603-02-02-02-FG).

## New questions

- **Q-NEW-F2A-DRILLRANGE** - The catalog prints some drills as a range (1405-04-06 A2 DRILL ".32/.34"). The review needs one number and values are never averaged: use the lower bound, the upper bound, or measure the STEP? Rows: 1405-04-06. Recommendation: measure the STEP only if the user wants it; otherwise the user picks a bound (paper check builds with both).
- **Q-NEW-F2A-OMIvsCAT** - Where OMi and the Brennan catalog (one source) print different numbers, keep OMi (standing rule: OMi dimension file first) and note the catalog value in $COMMENT? 2501-24-32-FG D1 1.940 vs 1.938; 2706-LN-08-06 L25 2.400 vs 2.410 and D 0.295 vs 0.297 (the same OMi values sit on the plain twin 2706-08-06, taken by Task A - staged, not accepted); 0304-C-32 CHEX 2.875 vs 2.880. Rows: 2501-24-32-FG, 2706-LN-08-06, 0304-C-32. Recommendation: keep OMi (no bucket depends on it); 2.880 / 1.940 look like 2-place prints of 2-7/8 / 1-15/16 padded with a zero.
- **Q-NEW-F2A-NOTINCAT** - These parts need a Brennan STEP (step list) but are not in Brennan's catalogs, so the STEP may not exist: 1405-20-24, 1504-32-32-FG, 1703-08-08-FG, 2403-06-02, 2406-06-12, 2502-20-16-FG, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-04-02, 2700-LN-08-06, 2700-LN-10-08, 2700-LN-12-10, 2705-04-02, 2705-LN-04-02, 5404-L-04X2.000, 5404-L-04X3.000 (the -LN rows use the plain body). Check brennaninc.com before downloading; if Brennan does not make one, a drawing from OMi's supplier is the only source. Rows: 1405-20-24, 1504-32-32-FG, 1703-08-08-FG, 2403-06-02, 2406-06-12, 2502-20-16-FG, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-04-02, 2700-LN-08-06, 2700-LN-10-08, 2700-LN-12-10, 2705-04-02, 2705-LN-04-02, 5404-L-04X2.000, 5404-L-04X3.000. Recommendation: check the website first (the user downloads).

## OMi / Air-Way vs catalog differences (REAL under the strict rule)

| config | review cell | catalog | other source |
|---|---|---|---|
| 0304-C-32 | CHEX@HEX | 2.880 | OMi Items!R16 = 2.875 (M010 (uncertain/keep_uncertain)): REAL difference |
| 2501-24-32-FG | D1@DRILL | 1.938 | OMi Items!X699 = 1.940 (M075 (certain)): REAL difference |
| 2706-LN-08-06 | L25@DRIVE | 2.410 | OMi Items!L1091 = 2.400 (M059 (certain)): REAL difference |
| 2706-LN-08-06 | D@BORE | 0.297 | OMi Items!X1091 = 0.295 (M062 (certain)): REAL difference |
| 2706-LN-08-06 | L25@DRIVE | 2.410 | Air-Way 2706.csv 2706-8-6 (the plain twin) L25 before Task A (DesignTable_2706 row 2706-08-06 $PRP@AxialSource "table had 2.34") = 2.34: REAL difference (twin row, context) |

## Column pairings used (catalog column -> review column)

certain = drawing letter + the column's generator / Air-Way meaning + data agreement (Air-Way rows of the series, OMi matches, Brennan STEP measurements); likely = meaning clear but not data-confirmed (or a symmetric tie); uncertain = shown as printed, not carried forward; "-" = the catalog prints no such column.

| table | review column | catalog column | pairing | reason |
|---|---|---|---|---|
| 0304 | L@DRIVE | L LGTH | certain | drawing TFA p65: L = overall cap length; OMi 'Overall Length' = catalog L LGTH on 13/13 parts (match/TFA_tees_caps.json, certain); mapping_final M009 maps OMi Overall Length -> L@DRIVE |
| 0304 | CHEX@HEX | C HEX | certain | C HEX = hex across flats (p65); OMi 'Hex Flat' = catalog C HEX on 12/13 (certain; the 13th is 0304-C-32 2.875/2.880); mapping_final M010 maps OMi Hex Flat -> CHEX@HEX |
| 0304 | THDMAJ_B@DRIVE | B1 THREAD | certain (thread) | B1 THREAD = the female JIC thread of the cap; the review value is its nominal major diameter |
| 0306 | h2@DRIVE | W WIDTH | certain | drawing TFA p65: W = nut width (thickness); OMi 'Overall Length' = catalog W WIDTH on 13/13 (match/TFA_tees_caps.json, certain); mapping_final M011 maps OMi Overall Length -> h2@DRIVE |
| 0306 | S4@DRIVE | C HEX | certain | C HEX = hex across flats (p65 end view); OMi 'Hex Flat' = catalog C HEX on 13/13 (certain); mapping_final M012 maps OMi Hex Flat -> S4@DRIVE |
| 0306 | THDMAJ_d@DRIVE | B1 THREAD | certain (thread) | B1 THREAD = the nut thread; the review value is its nominal major diameter |
| 1405 | W1@HEX | L LGTH | certain | drawing TFA p4: L = A1 port face to the swivel nut face (overall); gen_straight2 SPEC 1405: W1 = port face to the nut face (overall); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-0 |
| 1405 | L1@DRIVE | L1 LGTH | certain | drawing TFA p4: L1 = A1 port face to the stem tip inside the nut; SPEC 1405: L1 = port face to the stem tip; Air-Way L1 equal on 9/17 shared rows |
| 1405 | C1HEX@HEX | C HEX | certain | drawing TFA p4: C HEX = body hex on the A1 (female pipe) side; SPEC 1405 hex = C1HEX (body hex C(1)); Air-Way agrees 16/17 |
| 1405 | C2HEX@HEX | C1 HEX | certain | drawing TFA p4: C1 HEX = swivel nut hex; SPEC 1405 nut hex = C2HEX (C(2)); Air-Way agrees 17/17; = Brennan NPSM_MEAS nut AF of that size |
| 1405 | D@BORE | A2 DRILL | likely | A2 = the NPSM swivel end; A2 DRILL = the bore through the stem; SPEC 1405: bore D from the port bottom through the stem tip; Air-Way equal on 3/17 and inside the printed range on 5 more (8/17) |
| 1405 | TAPDRILL@BORE | - | not printed | the 1405 table prints no drill for the A1 female pipe port (columns A1 NPTF, A2 NPSM, A2 DRILL, L1, L, C, C1) |
| 1405 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF port |
| 1405 | THDMAJ_A1@DRIVE | A2 NPSM | certain (thread) | A2 = NPSM swivel thread |
| 1502 | N3@DRIVE | L LGTH | likely | drawing TFA p21: L = A1 female pipe port face to the A2 (swivel) axis = the pipe leg; Air-Way 1502 header A/A1/N3/W3/M1/... - N3 is the only pipe-leg column; the two Air-Way -FG rows (1502-2-2-FG 0.75 vs 0.660, 1502-4-4-FG 0.94 vs 0.880) differ - Air-Way and Brennan forgings differ |
| 1502 | M1@DRIVE | M LGTH | certain | M = the shorter swivel leg = A1 axis to the stem tip; gen_tee NPSM construction: stem tip at Air-Way M1 (1501 SPEC legs NPSMSW M1@DRIVE); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502- |
| 1502 | W3@HEX | M1 LGTH | certain | drawing TFA p21: M1 = A1 axis to the swivel nut face (the longer leg); gen_tee 1501 SPEC npsm nut-face column W3@HEX; the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503 |
| 1502 | CHEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17 |
| 1502 | C1HEX@HEX | Y FLATS | certain | Y FLATS = across flats of the forged body (drawings); gen_tee 1501/1503 SPEC hex = C1HEX@HEX (body flats); sibling 1501-FG/1503-FG: catalog Y FLATS = Air-Way C1HEX on 22/24 and 15/17 |
| 1502 | D@BORE | A2 DRILL | likely | A2 DRILL = drill at the NPSM swivel end (stem bore); gen_tee 1501 SPEC NPSMSW leg bore = D@BORE; sibling 1501-FG: A2 DRILL = Air-Way D on 16/24 |
| 1502 | TAPDRILL@BORE | - | not printed | the 1502-FG table prints no A1 (female pipe) drill/tap column |
| 1502 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF port |
| 1502 | THDMAJ_A1@DRIVE | A2 NPSM | certain (thread) | A2 = NPSM swivel thread |
| 1504 | N2@DRIVE | L LGTH | likely | drawing TFA p22: L = A1 female pipe port face to the 45 deg leg axis crossing = the pipe leg; Air-Way 1504 header A/A1/N2/W2/M/... - N2 is the only pipe-leg column (gen_tee 1503 SPEC: pipe leg N); Air-Way has no -FG row at this size |
| 1504 | M@DRIVE | M1 LGTH | certain | M1 = the shorter swivel leg (axis crossing to the stem tip); gen_tee 1503 SPEC legs NPSMSW M@DRIVE = stem-tip leg; the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08 |
| 1504 | W2@HEX | M LGTH | certain | drawing TFA p22: M = axis crossing to the swivel nut face (the longer leg); gen_tee 1503 SPEC npsm nut-face column W2@HEX; the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = |
| 1504 | CHEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17 |
| 1504 | C1HEX@HEX | Y FLATS | certain | Y FLATS = across flats of the forged body (drawings); gen_tee 1501/1503 SPEC hex = C1HEX@HEX (body flats); sibling 1501-FG/1503-FG: catalog Y FLATS = Air-Way C1HEX on 22/24 and 15/17 |
| 1504 | D@BORE | A2 DRILL | likely | A2 DRILL = drill at the NPSM swivel end (stem bore); gen_tee 1503 SPEC NPSMSW leg bore = D@BORE |
| 1504 | TAPDRILL@BORE | - | not printed | the 1504-FG table prints no A1 (female pipe) drill/tap column |
| 1504 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF port |
| 1504 | THDMAJ_A1@DRIVE | A2 NPSM | certain (thread) | A2 = NPSM swivel thread |
| 1601 | N1@DRIVE | L LGTH | likely | drawing TFA p47: L = A1 male pipe tip to the run axis = branch leg; Air-Way 1601 header A/A1_2/A1_3/N1/W3_2/M1_2/... - N1 is the only pipe-leg column |
| 1601 | M1_2@DRIVE | M1 LGTH | likely | M1 = run axis to the stem tip (shorter leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on the A2  |
| 1601 | M1_3@DRIVE | M1 LGTH | likely | M1 = run axis to the stem tip (shorter leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on the A2  |
| 1601 | W3_2@HEX | M LGTH | likely | M = run axis to the swivel nut face (longer leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on th |
| 1601 | W3_3@HEX | M LGTH | likely | M = run axis to the swivel nut face (longer leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on th |
| 1601 | C2HEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17; both swivel nuts are the same size on this part |
| 1601 | C3HEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17; both swivel nuts are the same size on this part |
| 1601 | C1HEX@HEX | Y FLATS | certain | Y FLATS = across flats of the forged body (drawings); gen_tee 1501/1503 SPEC hex = C1HEX@HEX (body flats); sibling 1501-FG/1503-FG: catalog Y FLATS = Air-Way C1HEX on 22/24 and 15/17 |
| 1601 | D2@BORE | A1 DRILL | likely | A1 = male pipe branch; Air-Way 1601 D2 = branch drill (0.19/0.28/0.41 by pipe size); catalog A1 DRILL = Air-Way D2 on 3/3 shared rows |
| 1601 | D_2@BORE | A2 DRILL | likely | A2 = swivel side 2; Air-Way 1601 D_2 = side-2 stem bore |
| 1601 | D3@BORE | A3 DRILL | likely | A3 = swivel side 3; Air-Way 1601 D3 = side-3 stem bore |
| 1601 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = male NPTF branch |
| 1601 | THDMAJ_A1_2@DRIVE | A2 NPSM | certain (thread) | A2 = NPSM swivel side 2 |
| 1601 | THDMAJ_A1_3@DRIVE | A3 NPSM | certain (thread) | A3 = NPSM swivel side 3 |
| 1602 | N3@DRIVE | L LGTH | likely | drawing TFA p48: L = A1 female pipe port face to the run axis = branch leg; Air-Way 1602 header A/A1_2/A1_3/N3/W3_2/M1_2/... - N3 is the only pipe-leg column |
| 1602 | M1_2@DRIVE | M1 LGTH | likely | M1 = run axis to the stem tip (shorter leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on the A2  |
| 1602 | M1_3@DRIVE | M1 LGTH | likely | M1 = run axis to the stem tip (shorter leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on the A2  |
| 1602 | W3_2@HEX | M LGTH | likely | M = run axis to the swivel nut face (longer leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on th |
| 1602 | W3_3@HEX | M LGTH | likely | M = run axis to the swivel nut face (longer leg); the longer catalog leg minus the shorter = the Brennan-measured nut-face-to-stem-tip distance TIP_B of that NPSM swivel size on every row (gen_straight2 NPSM_MEAS, Brennan 1404 STEPs: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20 0.42; e.g. 1404-08-08 L-L1 = 1502-12-08-FG M1-M = 1503-08-08-FG M-M1 = 0.28); the drawing (TFA p47/p48) dimensions M on th |
| 1602 | C2HEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17; both swivel nuts are the same size on this part |
| 1602 | C3HEX@HEX | C HEX | certain | C HEX is drawn on the swivel nut (TFA p21/p22/p47/p48 drawings) and equals Brennan NPSM_MEAS nut AF at every size; gen_tee 1501/1503 SPEC npsm nut hex = CHEX@HEX; sibling 1501-FG/1503-FG: catalog C HEX = Air-Way CHEX on 23/24 and 17/17; both swivel nuts are the same size on this part |
| 1602 | C1HEX@HEX | Y FLATS | certain | Y FLATS = across flats of the forged body (drawings); gen_tee 1501/1503 SPEC hex = C1HEX@HEX (body flats); sibling 1501-FG/1503-FG: catalog Y FLATS = Air-Way C1HEX on 22/24 and 15/17 |
| 1602 | D2@BORE | A2 DRILL | likely | A2 = swivel side 2; Air-Way 1602 header .../TAPDRILL/D2/D3: D2/D3 = side-2/side-3 stem bores |
| 1602 | D3@BORE | A3 DRILL | likely | A3 = swivel side 3 (Air-Way D3) |
| 1602 | TAPDRILL@BORE | - | not printed | the 1602-FG table prints no A1 (female pipe) drill/tap column |
| 1602 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF branch |
| 1602 | THDMAJ_A1_2@DRIVE | A2 NPSM | certain (thread) | A2 = NPSM swivel side 2 |
| 1602 | THDMAJ_A1_3@DRIVE | A3 NPSM | certain (thread) | A3 = NPSM swivel side 3 |
| 1700 | L28@DRIVE | L (in.) | certain | drawing Flange p3: L = JIC tip to the flange face; gen_straight2 SPEC 1700: L28 = JIC tip to the flange face; the Brennan 1700 STEPs (gen_straight2 BRENNAN_1700 2.600 / 2.750 / 3.500) = catalog L of 1700-08-08 / -12-12 / -24-24; Air-Way L28 differs on every shared row (Brennan bodies are longer, 00_DOCS/NPSM_swivel_and_code61_flange_measurements.md) |
| 1700 | CHEX@HEX | A/F (in.) | likely | A/F = wrench flats behind the JIC end (p3); Brennan bodies are a round collar with two flats (BRENNAN_1700 flats 1.000 / 1.374 / 2.000 = catalog A/F 1.000 / 1.375 / 2.000) while the master models a full hex of CHEX - whether the flats width goes into CHEX is Q-NEW-1700BODY; Air-Way CHEX equal on 6/13 |
| 1700 | O@DRIVE | - | not printed | the catalog prints only the nominal flange size ('2 FLANGE'), not the head diameter O |
| 1700 | D@BORE | - | not printed | the 1700 table prints no bore / drill column |
| 1700 | THDMAJ_B@DRIVE | 1 THREAD | certain (thread) | 1 THREAD = the JIC thread |
| 1703 | M2@DRIVE | L1 (in.) | likely | drawing Flange p4 (1703-FG): L1 = JIC (end 1) tip to the flange (end 2) axis = JIC leg; the one Air-Way row 1703-61-24-24 (DROP, non-forged) M2 1.78 = catalog 1703-24-24-FG L1 1.78 |
| 1703 | N3@DRIVE | L2 (in.) | likely | drawing: L2 = flange face to the JIC (end 1) axis = flange leg; the only other leg column of the table (Air-Way 1703-61-24-24 N3 1.98 vs forged 2.38 - that Air-Way part is not forged) |
| 1703 | CHEX@HEX | A/F (in.) | likely | A/F = across flats of the forged body (p4); the table has one hex column (Air-Way 1703-61-24-24 CHEX 2.00 vs 1 7/8 forged - non-forged part) |
| 1703 | O@DRIVE | - | not printed | only the nominal flange size is printed ('2 FLANGE'), not the head diameter O |
| 1703 | D@BORE | - | not printed | the 1703 / 1703-FG tables print no bore column |
| 1703 | THDMAJ_B@DRIVE | 1 THREAD | certain (thread) | 1 THREAD = the JIC thread |
| 1703_TUBE | M2@DRIVE | L1 (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow L1 is JIC tip to the OUTSIDE of the bend along the JIC axis (Flange.md) - not the forged-master feature, so not paired |
| 1703_TUBE | N3@DRIVE | L2 (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow L2 is flange face to the JIC axis (Flange.md) - not the forged-master feature, so not paired |
| 1703_TUBE | CHEX@HEX | A/F (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow A/F is the hex behind the JIC thread - not the forged-master feature, so not paired |
| 1703_TUBE | O@DRIVE | - | not printed | only the nominal flange size is printed, not the head diameter O |
| 1703_TUBE | D@BORE | - | not printed | no bore column |
| 1703_TUBE | THDMAJ_B@DRIVE | 1 THREAD | certain (thread) | 1 THREAD = the JIC thread |
| 1703_TUBE | (no column yet) bend radius | - | not printed | not printed |
| 1703_TUBE | (no column yet) tube OD | - | not printed | not printed ('TUBE O.D.' is the JIC end's tube size of the dash, not shown to be the bent tube's OD) |
| 1703_TUBE | (no column yet) tube wall | - | not printed | not printed |
| 1704 | M@DRIVE | L1 (in.) | certain | drawing Flange p5 (1704-FG): L1 = JIC (end 1) tip to the flange axis = JIC leg; both Air-Way rows equal the forged catalog L1: 1704-61-24-24 M 2.33 = 1704-24-24-FG 2.330, 1704-61-32-32 M 3.06 = 1704-32-32-FG 3.06 |
| 1704 | N2@DRIVE | L2 (in.) | likely | drawing: L2 = flange face to the JIC (end 1) axis = flange leg; the only other leg column of the table (Air-Way N2 2.75 / 3.25 vs forged 3.150 / 4.25 - the Air-Way parts are not forged) |
| 1704 | Y@HEX | A/F (in.) | likely | A/F = across flats of the forged body (p5); the table has one hex column (Air-Way Y 2.00 / 2.63 vs forged 1.875 / 2.500 - non-forged parts) |
| 1704 | O@DRIVE | - | not printed | only the nominal flange size is printed ('2 FLANGE'), not the head diameter O |
| 1704 | D@BORE | - | not printed | the 1704 / 1704-FG tables print no bore column |
| 1704 | THDMAJ_B@DRIVE | 1 THREAD | certain (thread) | 1 THREAD = the JIC thread |
| 1704_TUBE | M@DRIVE | L1 (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow L1 is JIC tip to the OUTSIDE of the bend along the JIC axis (Flange.md) - not the forged-master feature, so not paired |
| 1704_TUBE | N2@DRIVE | L2 (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow L2 is flange face to the JIC axis (Flange.md) - not the forged-master feature, so not paired |
| 1704_TUBE | Y@HEX | A/F (in.) | uncertain | swept (bent-tube) part: no master and no column set exists for this shape (one master per shape); the catalog swept-elbow A/F is the hex behind the JIC thread - not the forged-master feature, so not paired |
| 1704_TUBE | O@DRIVE | - | not printed | only the nominal flange size is printed, not the head diameter O |
| 1704_TUBE | D@BORE | - | not printed | no bore column |
| 1704_TUBE | THDMAJ_B@DRIVE | 1 THREAD | certain (thread) | 1 THREAD = the JIC thread |
| 1704_TUBE | (no column yet) bend radius | - | not printed | not printed |
| 1704_TUBE | (no column yet) tube OD | - | not printed | not printed ('TUBE O.D.' is the JIC end's tube size of the dash, not shown to be the bent tube's OD) |
| 1704_TUBE | (no column yet) tube wall | - | not printed | not printed |
| 2403 | L1@DRIVE | L LGTH | certain | drawing TFA p5: L = overall; Air-Way L1 equal on 33/33 shared rows |
| 2403 | HEXB@HEX | C HEX | certain | C HEX = body hex; Air-Way HEXB equal on 33/33 |
| 2403 | D1@BORE | B1 DRILL | certain | B1 = first-dash JIC end (End A); Air-Way D1 equal on 30/33 |
| 2403 | D2@BORE | B2 DRILL | certain | B2 = second-dash JIC end (End B); Air-Way D2 equal on 32/33 |
| 2403 | THDMAJ_A@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = End A JIC thread |
| 2403 | THDMAJ_B@DRIVE | B2 SAE 37Deg | certain (thread) | B2 = End B JIC thread |
| 2403LH | L1@DRIVE | L LGTH | certain | L = overall (TFA p5); Air-Way L1 equal on 16/16 |
| 2403LH | C2HEX@HEX | C HEX | certain | C HEX = body hex; Air-Way C2HEX equal on 16/16 |
| 2403LH | D1@BORE | B1 DRILL | certain | Air-Way D1 equal on 16/16 |
| 2403LH | D2@BORE | B2 DRILL | certain | Air-Way D2 equal on 16/16 |
| 2403LH | THDMAJ_B1@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2403LH | THDMAJ_B2@DRIVE | B2 SAE 37Deg | certain (thread) | B2 thread |
| 2404L | L20@DRIVE | L LGTH | certain | drawing TFA p6: L = overall; Air-Way L20 equal on 6/8, the other 2 within 0.01 |
| 2404L | CHEX@HEX | C HEX | certain | C HEX = body hex; Air-Way CHEX equal/rounding on 7/8 |
| 2404L | D@BORE | B1 DRILL | certain | B1 = JIC end drill; Air-Way D (JIC-side bore) equal/rounding on 8/8 |
| 2404L | D1@BORE | A2 DRILL | likely | A2 = male NPTF end, its drill = the pipe-side bore (Air-Way D1 0.28 / 0.41 / 0.53 / 0.72 / 0.94 by pipe size); equal on 3/8 - Brennan drills the pipe end of -06-06 / -08-08 / -12-12 at the smaller tube drill |
| 2404L | T20REF@REF | - | not printed | hex length (T20) is not printed |
| 2404L | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = JIC thread |
| 2404L | THDMAJ_A@DRIVE | A2 NPTF | certain (thread) | A2 = male NPTF |
| 2405 | L2@DRIVE | L LGTH | certain | drawing TFA p7: L = overall; OMi Overall Length = catalog L (match likely) and mapping_final M163 OMi Overall Length -> L2; Air-Way L2 equal on 28/32 |
| 2405 | HEXB@HEX | C HEX | certain | C HEX = body hex; M164; Air-Way equal on 32/32 |
| 2405 | D3@BORE_THRU | B1 DRILL | certain | B1 DRILL = JIC end drill = through bore; M165; Air-Way equal on 32/32 |
| 2405 | TAPDRILL@BORE_A | - | not printed | the 2405 table prints no drill for the A2 female pipe port |
| 2405 | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = JIC thread |
| 2406 | L23@DRIVE | L0 LGTH | certain | drawing TFA p7: the length dimension spans the whole part (female face to male tip); gen_straight2 SPEC 2406: L23 overall; the in-repo Brennan 2406-08-08 STEP read 1.410 = catalog L0 1.41 (Task C fill); Air-Way L23 equal on 19/47 (Air-Way 2406 lengths differ from Brennan) |
| 2406 | HEXB@HEX | C HEX | certain | C HEX = 'BODY HEX' (p7); Air-Way equal on 46/47; STEP 2406-08-08 0.875 = catalog |
| 2406 | D3@BORE | B2 DRILL | certain | B2 = male JIC end (second dash); SPEC 2406: bore D3 from the male tip to the seat; Air-Way equal on 45/47; STEP 2406-08-08 0.391 = catalog |
| 2406 | THDMAJ_A@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = female JIC (first dash) |
| 2406 | THDMAJ_B@DRIVE | B2 SAE 37Deg | certain (thread) | B2 = male JIC (second dash) |
| 2501 | M@DRIVE | M LGTH | certain | drawing TFA p23: M = male JIC (B1) tip to the A2-leg axis; catalog M = OMi 'M 1 Size' on 44/44 (TFA_elbows.json certain); gen_tee 2501 JICM leg = M@DRIVE; Air-Way equal on 35/38 |
| 2501 | N@DRIVE | L LGTH | certain | drawing p23: L = male pipe (A2) tip to the B1-leg axis; catalog L = OMi 'L 1 Size' 44/44; gen_tee 2501 NPTFM leg = N@DRIVE; Air-Way 35/38 |
| 2501 | Y@REF | Y FLATS | certain | Y FLATS = forged body flats; = OMi Hex Flat 44/44; M073; Air-Way 34/38 |
| 2501 | D@BORE | B1 DRILL | certain | B1 DRILL = OMi Side 1 ID 44/44; M074; Air-Way 38/38 |
| 2501 | D1@DRILL | A2 DRILL | certain | A2 DRILL = OMi Side 2 ID 43/44; M075; Air-Way 38/38 |
| 2501 | THDMAJ_A@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = JIC thread |
| 2501 | PIPEOD@DRIVE | A2 NPTF | certain (thread) | A2 = male NPTF |
| 2501 | NPTF_E0@DRIVE | - | not printed | NPTF gauge diameters are not printed (ASME B1.20.3 library) |
| 2501 | NPTF_E1@DRIVE | - | not printed | not printed (ASME library) |
| 2501 | NPTF_L2@DRIVE | - | not printed | not printed (ASME library) |
| 2501 | JIC_RELIEFL@DRIVE | - | not printed | JIC end chain is not printed (MS33656J library) |
| 2501 | RELIEFANG@DRIVE | - | not printed | not printed (JIC library constant) |
| 2501 | JIC_THDZ@DRIVE | - | not printed | not printed (MS33656J library) |
| 2501 | JIC_CONEDIA@DRIVE | - | not printed | not printed (MS33656J library) |
| 2501 | JIC_LANDL@DRIVE | - | not printed | not printed (MS33656J library) |
| 2501 | JIC_SEATL@DRIVE | - | not printed | not printed (MS33656J library) |
| 2501 | SEATB@DRIVE | - | not printed | not printed (JIC library constant) |
| 2502 | M1@DRIVE | M LGTH | certain | drawing TFA p25: M = male JIC (B1) tip to the A2 axis; catalog M = OMi 'M 1 Size' 20/20 (TFA_elbows.json certain); Air-Way M1 10/14 |
| 2502 | N1@DRIVE | L LGTH | certain | drawing p25: L = female pipe (A2) port face to the B1 axis; catalog L = OMi 'L 1 Size' 20/20; Air-Way N1 13/14 |
| 2502 | Y1@DRIVE | Y FLATS | certain | Y FLATS = OMi Hex Flat 20/20; M083; Air-Way 11/14 |
| 2502 | D@BORE | B1 DRILL | certain | B1 DRILL = OMi Side 1 ID 20/20; M084; Air-Way 14/14 |
| 2502 | TAPDRILL@BORE | - | not printed | the 2502-FG table prints no drill for the A2 female pipe port |
| 2502 | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = JIC thread |
| 2502 | THDMAJ_A@DRIVE | A2 NPTF | certain (thread) | A2 = female NPTF |
| 2503 | M2@DRIVE | M LGTH | certain | drawing TFA p26: M = B1 (JIC) leg to the axis crossing; catalog M = OMi 'M 1 Size' 31/31 (TFA_elbows.json certain); gen_tee 2503 JICM leg = M2@DRIVE; Air-Way 27/32 |
| 2503 | N2@DRIVE | L LGTH | certain | drawing p26: L = A2 (pipe) leg along the 45 deg axis; catalog L = OMi 'L 1 Size' 31/31; gen_tee 2503 NPTFM leg = N2@DRIVE; Air-Way 28/32 |
| 2503 | Y@REF | Y FLATS | certain | = OMi Hex Flat 31/31; M087; Air-Way 30/32 |
| 2503 | D@BORE | B1 DRILL | certain | = OMi Side 1 ID 31/31; M088; Air-Way 32/32 |
| 2503 | D1@BORE | A2 DRILL | certain | = OMi Side 2 ID 31/31; M089; Air-Way 32/32 |
| 2503 | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 = JIC thread |
| 2503 | THDMAJ_A@DRIVE | A2 NPTF | certain (thread) | A2 = male NPTF |
| 2603 | LEG1@DRIVE | M1 LGTH | likely | side order (TFA_tees_caps.json: catalog M1 = OMi 'M 1 Size', tie with M2 on symmetric parts - numerically irrelevant here); Air-Way LEG1 20/25 |
| 2603 | LEG2@DRIVE | M2 LGTH | likely | side order (tie with M1 on symmetric parts); Air-Way LEG2 18/25 |
| 2603 | LEG3@DRIVE | M3 LGTH | certain | M3 = branch (3rd dash) leg = OMi 'L 1 Size' (certain on the 2 discriminating rows); Air-Way LEG3 21/25 |
| 2603 | Y@REF | Y FLATS | certain | = OMi Hex Flat 14/14 (certain); M182 (Air-Way Y@REF equal on 15/25 only: the hand-made 2603HX table carries its own A/F rule) |
| 2603 | D1@BORE | B1 DRILL | certain | = OMi Side 1 ID; M183; Air-Way 25/25 |
| 2603 | D2@BORE | B2 DRILL | certain | = OMi Side 2 ID; M184; Air-Way 25/25 |
| 2603 | D3@BORE | B3 DRILL | certain | = OMi Side 3 ID (certain); M185; Air-Way 25/25 |
| 2603 | THDMAJ_1@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2603 | THDMAJ_2@DRIVE | B2 SAE 37Deg | certain (thread) | B2 thread |
| 2603 | THDMAJ_3@DRIVE | B3 SAE 37Deg | certain (thread) | B3 thread |
| 2606 | M1_1@DRIVE | M LGTH | likely | side-1 JIC leg; catalog M = OMi 'M 1 Size' 10/10, tie with N on symmetric parts (numerically irrelevant on 2606-12-12-12); mapping_final M193 (uncertain) assumed side 1 - confirmed |
| 2606 | N1@DRIVE | L LGTH | certain | side-2 (female pipe) leg; catalog L = OMi 'M 2 Size' 10/10 on discriminating rows (certain); M194 assumed side 2 - confirmed |
| 2606 | M1_3@DRIVE | N LGTH | likely | side-3 JIC leg (2606 heads it 'N'); = OMi 'L 1 Size' (tie with M); M195 - confirmed |
| 2606 | Y1@HEX | Y FLATS | certain | = OMi Hex Flat 10/10 (certain); M196 |
| 2606 | D1@BORE | B1 DRILL | likely | = OMi Side 1 ID (tie with B3 on symmetric parts); M197 |
| 2606 | D3@BORE | B3 DRILL | likely | = OMi Side 3 ID (tie with B1); M198 |
| 2606 | TAPDRILL@BORE | - | not printed | the 2606-FG table prints no drill for the A2 female pipe port |
| 2606 | THDMAJ_B1@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2606 | THDMAJ_A@DRIVE | A2 NPTF | certain (thread) | A2 = female NPTF |
| 2606 | THDMAJ_B3@DRIVE | BE SAE 37Deg | certain (thread) | side-3 JIC thread (header printed 'BE SAE 37Deg' - typo for B3) |
| 2609 | M1@DRIVE | M LGTH | certain | side-1 JIC leg; catalog M = OMi 'M 1 Size' 4/4 on discriminating rows (certain); M199 - confirmed |
| 2609 | N1_2@DRIVE | L1 LGTH | likely | side-2 female pipe leg; = OMi 'M 2 Size' (tie with L on symmetric parts - numerically irrelevant: both 1.230 here); M200 |
| 2609 | N1_3@DRIVE | L LGTH | likely | side-3 female pipe leg; = OMi 'L 1 Size' (tie); M201 |
| 2609 | Y1@HEX | Y FLATS | certain | = OMi Hex Flat (certain); M202 |
| 2609 | D@BORE | B1 DRILL | certain | = OMi Side 1 ID (certain); M203 |
| 2609 | TAPDRILL2@BORE | - | not printed | no drill printed for the female pipe ports |
| 2609 | TAPDRILL3@BORE | - | not printed | no drill printed for the female pipe ports |
| 2609 | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2609 | THDMAJ_A2@DRIVE | A2 NPTF | certain (thread) | A2 = female NPTF |
| 2609 | THDMAJ_A3@DRIVE | A3 NPTF | certain (thread) | A3 = female NPTF |
| 2611 | M1@DRIVE | M LGTH | certain | side-1 JIC leg; = OMi 'M 1 Size' 5/5 discriminating (certain); M204 - confirmed |
| 2611 | N5@DRIVE | L LGTH | certain | side-2 male pipe leg; = OMi 'M 2 Size' 5/5 (certain); M205 - confirmed |
| 2611 | N1@DRIVE | L1 LGTH | certain | side-3 female pipe leg; = OMi 'L 1 Size' 5/5 (certain); M206 - confirmed |
| 2611 | Y1@HEX | Y FLATS | certain | = OMi Hex Flat 5/5 (certain); M207 |
| 2611 | D@BORE | B1 DRILL | certain | = OMi Side 1 ID 5/5 (certain); M208 |
| 2611 | D1@BORE | A2 DRILL | certain | = OMi Side 2 ID 5/5 (certain); M209 |
| 2611 | TAPDRILL@BORE | - | not printed | no drill printed for the A3 female pipe port |
| 2611 | THDMAJ_B@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2611 | THDMAJ_A2@DRIVE | A2 NPTF | certain (thread) | A2 = male NPTF |
| 2611 | THDMAJ_A3@DRIVE | A3 NPTF | certain (thread) | A3 = female NPTF |
| 2700 | L4@DRIVE | L LGTH | certain | drawing TFA p8: L = overall; Air-Way L4 equal on 13/13 |
| 2700 | C2HEX@HEX | C HEX | certain | C HEX = the hex; Air-Way equal on 12/13 |
| 2700 | D1@BORE | B1 DRILL | certain | B1 = first-dash (short) JIC end; Air-Way D1 equal on 13/13 |
| 2700 | D2@BORE | B2 DRILL | certain | B2 = bulkhead (second dash) end; Air-Way D2 equal on 13/13 |
| 2700 | I1@DRIVE | - | not printed | the bulkhead length is not printed |
| 2700 | THDMAJ_B1@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2700 | THDMAJ_B2@DRIVE | B2 SAE 37Deg | certain (thread) | B2 thread |
| 2701 | M3@DRIVE | M LGTH | certain | drawing TFA p27: M = B1 (straight JIC) tip to the B2 axis; gen_tee 2701 JICM leg = M3@DRIVE; Air-Way equal on 8/8 |
| 2701 | M4@DRIVE | L LGTH | certain | drawing p27: L = B2 (bulkhead) tip to the B1 axis; gen_tee 2701 JICBH leg = M4@DRIVE; Air-Way equal on 8/8 |
| 2701 | Y@HEX | Y FLATS | certain | Y FLATS = forged body flats; Air-Way equal on 8/8 |
| 2701 | D1@BORE | B1 DRILL | likely | B1 = JIC leg drill (gen_tee 2701 JICM bore D1); Air-Way 8/8 but tied with D2 (all shared rows equal-dash) |
| 2701 | D2@BORE | B2 DRILL | likely | B2 = bulkhead leg drill (JICBH bore D2); tied with D1 on equal-dash rows |
| 2701 | i2@DRIVE | - | not printed | bulkhead relief length not printed |
| 2701 | K1@DRIVE | - | not printed | collar length not printed |
| 2701 | O@DRIVE | - | not printed | collar diameter not printed |
| 2701 | THDMAJ_B1@DRIVE | B1 SAE 37Deg | certain (thread) | B1 thread |
| 2701 | THDMAJ_B2@DRIVE | B2 SAE 37Deg | certain (thread) | B2 thread |
| 2705 | L24@DRIVE | L LGTH | certain | drawing TFA p8: L = overall; = OMi Overall Length 11/13 (certain, TFA_straights.json); M056 (certain) |
| 2705 | C5HEX@HEX | C1 HEX | certain | C1 HEX = the only hex; = OMi Hex Flat 12/13; M057; Air-Way 11/11 |
| 2705 | D@BORE | B2 DRILL | certain | B2 = bulkhead JIC end drill; = OMi Side 2 ID 13/13; M058; Air-Way 11/11 |
| 2705 | I1@DRIVE | - | not printed | the bulkhead length is not printed |
| 2705 | TAPDRILL@BORE | - | not printed | no drill printed for the A1 female pipe port |
| 2705 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF |
| 2705 | THDMAJ_B@DRIVE | B2 SAE 37Deg | certain (thread) | B2 = JIC bulkhead thread |
| 2706 | L25@DRIVE | L LGTH | certain | drawing TFA p9: L = overall; = OMi Overall Length 13/14 (certain); M059; Air-Way 12/13 |
| 2706 | C2HEX@HEX | C1 HEX | certain | C1 HEX = the only hex; = OMi Hex Flat 14/14; M060; Air-Way 13/13 |
| 2706 | D1@BORE | A1 DRILL | certain | A1 = male pipe end drill; = OMi Side 1 ID 14/14; M061; Air-Way 13/13 |
| 2706 | D@BORE | B2 DRILL | certain | B2 = bulkhead JIC end drill; = OMi Side 2 ID 13/14; M062; Air-Way 13/13 |
| 2706 | I1@DRIVE | - | not printed | the bulkhead length is not printed |
| 2706 | THDMAJ_A@DRIVE | A1 NPTF | certain (thread) | A1 = male NPTF |
| 2706 | THDMAJ_B@DRIVE | B2 SAE 37Deg | certain (thread) | B2 = JIC bulkhead thread |
| 5000 | L@DRIVE | L LGTH | certain | drawing TFA p10: L = overall; Air-Way L equal on 19/19 |
| 5000 | CHEX@HEX | C HEX | certain | C HEX = the hex; Air-Way equal on 19/19 |
| 5000 | TAPDRILL1@BORE | - | not printed | the 5000 table prints no drill/tap column |
| 5000 | TAPDRILL2@BORE | - | not printed | the 5000 table prints no drill/tap column |
| 5000 | THDMAJ_A1@DRIVE | A1 NPTF | certain (thread) | A1 = female NPTF |
| 5000 | THDMAJ_A2@DRIVE | A2 NPTF | certain (thread) | A2 = female NPTF |
| 5404 | L@DRIVE | L LGTH | certain | drawing TFA p11: L = overall; Air-Way L equal on 23/25 |
| 5404 | HEXB@HEX | C HEX | certain | C HEX = the hex; Air-Way equal on 25/25 |
| 5404 | D1@BORE | A1 DRILL | certain | A1 = first-dash end; Air-Way D1 equal on 24/25 |
| 5404 | D2@BORE | A2 DRILL | certain | A2 = second-dash end; Air-Way D2 equal on 24/25 |
| 5404 | NPTFA_ENDL@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFA_E0@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFA_E1@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFA_L2@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFB_ENDL@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFB_E0@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFB_E1@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | NPTFB_L2@DRIVE | - | not printed | male NPTF end geometry is not printed (ASME B1.20.3 / Brennan-measured ENDL library) |
| 5404 | PIPEODA@DRIVE | A1 NPTF | certain (thread) | A1 = male NPTF (first dash) |
| 5404 | PIPEODB@DRIVE | A2 NPTF | certain (thread) | A2 = male NPTF (second dash) |

## Rows

| config | old -> new | catalog hit | catalog gives (review cell = printed value) | still not printed / gate | note |
|---|---|---|---|---|---|
| 0304-C-02 | WORK -> **WORK** | TFA p65 0304-C-02 | L=0.500, CHEX=0.375 | - | Catalog TFA p65 0304-C 0304-C-02: gives L@DRIVE=0.500, CHEX@HEX=0.375. OMi: 2/2 compared cells agree. |
| 0304-C-03 | WORK -> **WORK** | TFA p65 0304-C-03 | L=0.562, CHEX=0.438 | - | Catalog TFA p65 0304-C 0304-C-03: gives L@DRIVE=0.562, CHEX@HEX=0.438. OMi: 2/2 compared cells agree. |
| 0304-C-04 | WORK -> **WORK** | TFA p65 0304-C-04 | L=0.594, CHEX=0.562 | - | Catalog TFA p65 0304-C 0304-C-04: gives L@DRIVE=0.594, CHEX@HEX=0.562. OMi: 2/2 compared cells agree. |
| 0304-C-05 | WORK -> **WORK** | TFA p65 0304-C-05 | L=0.609, CHEX=0.625 | - | Catalog TFA p65 0304-C 0304-C-05: gives L@DRIVE=0.609, CHEX@HEX=0.625. OMi: 2/2 compared cells agree. |
| 0304-C-06 | WORK -> **WORK** | TFA p65 0304-C-06 | L=0.625, CHEX=0.687 | - | Catalog TFA p65 0304-C 0304-C-06: gives L@DRIVE=0.625, CHEX@HEX=0.687. OMi: 2/2 compared cells agree. |
| 0304-C-08 | WORK -> **WORK** | TFA p65 0304-C-08 | L=0.750, CHEX=0.875 | - | Catalog TFA p65 0304-C 0304-C-08: gives L@DRIVE=0.750, CHEX@HEX=0.875. OMi: 2/2 compared cells agree. |
| 0304-C-10 | WORK -> **WORK** | TFA p65 0304-C-10 | L=0.844, CHEX=1.000 | - | Catalog TFA p65 0304-C 0304-C-10: gives L@DRIVE=0.844, CHEX@HEX=1.000. OMi: 2/2 compared cells agree. |
| 0304-C-12 | WORK -> **WORK** | TFA p65 0304-C-12 | L=0.906, CHEX=1.250 | - | Catalog TFA p65 0304-C 0304-C-12: gives L@DRIVE=0.906, CHEX@HEX=1.250. OMi: 2/2 compared cells agree. |
| 0304-C-14 | WORK -> **WORK** | TFA p65 0304-C-14 | L=0.969, CHEX=1.375 | - | Catalog TFA p65 0304-C 0304-C-14: gives L@DRIVE=0.969, CHEX@HEX=1.375. OMi: 2/2 compared cells agree. |
| 0304-C-16 | WORK -> **WORK** | TFA p65 0304-C-16 | L=1.016, CHEX=1.500 | - | Catalog TFA p65 0304-C 0304-C-16: gives L@DRIVE=1.016, CHEX@HEX=1.500. OMi: 2/2 compared cells agree. |
| 0304-C-20 | WORK -> **WORK** | TFA p65 0304-C-20 | L=1.062, CHEX=2.000 | - | Catalog TFA p65 0304-C 0304-C-20: gives L@DRIVE=1.062, CHEX@HEX=2.000. OMi: 2/2 compared cells agree. |
| 0304-C-24 | WORK -> **WORK** | TFA p65 0304-C-24 | L=1.188, CHEX=2.250 | - | Catalog TFA p65 0304-C 0304-C-24: gives L@DRIVE=1.188, CHEX@HEX=2.250. OMi: 2/2 compared cells agree. |
| 0304-C-32 | WORK -> **WORK** | TFA p65 0304-C-32 | L=1.440, CHEX=2.880 | - | Catalog TFA p65 0304-C 0304-C-32: gives L@DRIVE=1.440, CHEX@HEX=2.880. OMi: 1/2 compared cells agree (differ: CHEX@HEX). Catalog C HEX 2.880 vs OMi Hex Flat 2.875 (Items!R16): REAL under the strict rule (both print 3 places), 0.005 (match/TFA_tees_caps_diffcheck.json idx 5). The catalog's other -32 nut hexes print 2.875 (0304-32, 0318-32), so 2.880 is most likely 2.88 = 2-7/8 padded. OMi kept (OMi file first); difference -> $COMMENT (Q-NEW-F2A-OMIvsCAT). |
| 0306-02 | WORK -> **WORK** | TFA p65 0306-02 | h2=0.22, S4=0.562 | - | Catalog TFA p65 0306 0306-02: gives h2@DRIVE=0.22, S4@DRIVE=0.562. OMi: 2/2 compared cells agree. |
| 0306-03 | WORK -> **WORK** | TFA p65 0306-03 | h2=0.22, S4=0.625 | - | Catalog TFA p65 0306 0306-03: gives h2@DRIVE=0.22, S4@DRIVE=0.625. OMi: 2/2 compared cells agree. |
| 0306-04 | WORK -> **WORK** | TFA p65 0306-04 | h2=0.28, S4=0.687 | - | Catalog TFA p65 0306 0306-04: gives h2@DRIVE=0.28, S4@DRIVE=0.687. OMi: 2/2 compared cells agree. |
| 0306-05 | WORK -> **WORK** | TFA p65 0306-05 | h2=0.280, S4=0.750 | - | Catalog TFA p65 0306 0306-05: gives h2@DRIVE=0.280, S4@DRIVE=0.750. OMi: 2/2 compared cells agree. |
| 0306-06 | WORK -> **WORK** | TFA p65 0306-06 | h2=0.27, S4=0.812 | - | Catalog TFA p65 0306 0306-06: gives h2@DRIVE=0.27, S4@DRIVE=0.812. OMi: 2/2 compared cells agree. |
| 0306-08 | WORK -> **WORK** | TFA p65 0306-08 | h2=0.31, S4=1.000 | - | Catalog TFA p65 0306 0306-08: gives h2@DRIVE=0.31, S4@DRIVE=1.000. OMi: 2/2 compared cells agree. |
| 0306-10 | WORK -> **WORK** | TFA p65 0306-10 | h2=0.36, S4=1.125 | - | Catalog TFA p65 0306 0306-10: gives h2@DRIVE=0.36, S4@DRIVE=1.125. OMi: 2/2 compared cells agree. |
| 0306-12 | WORK -> **WORK** | TFA p65 0306-12 | h2=0.41, S4=1.375 | - | Catalog TFA p65 0306 0306-12: gives h2@DRIVE=0.41, S4@DRIVE=1.375. OMi: 2/2 compared cells agree. |
| 0306-16 | WORK -> **WORK** | TFA p65 0306-16 | h2=0.41, S4=1.625 | - | Catalog TFA p65 0306 0306-16: gives h2@DRIVE=0.41, S4@DRIVE=1.625. OMi: 2/2 compared cells agree. |
| 0306-20 | WORK -> **WORK** | TFA p65 0306-20 | h2=0.41, S4=1.875 | - | Catalog TFA p65 0306 0306-20: gives h2@DRIVE=0.41, S4@DRIVE=1.875. OMi: 2/2 compared cells agree. |
| 0306-24 | WORK -> **WORK** | TFA p65 0306-24 | h2=0.41, S4=2.125 | - | Catalog TFA p65 0306 0306-24: gives h2@DRIVE=0.41, S4@DRIVE=2.125. OMi: 2/2 compared cells agree. |
| 0306-32 | WORK -> **WORK** | TFA p65 0306-32 | h2=0.410, S4=2.750 | - | Catalog TFA p65 0306 0306-32: gives h2@DRIVE=0.410, S4@DRIVE=2.750. OMi: 2/2 compared cells agree. |
| 1405-04-06 | STEP -> **DECIDE** | TFA p4 1405-04-06 | L1=1.270, W1=1.480, C1HEX=0.688, C2HEX=0.875, D=0.32/0.34 (range) | TAPDRILL / gate: Q-TRANSFER-TAPDRILL, Q-NEW-F2A-DRILLRANGE | Catalog TFA p4 1405 1405-04-06: gives L1@DRIVE=1.270, W1@HEX=1.480, C1HEX@HEX=0.688, C2HEX@HEX=0.875. Range print: D@BORE 0.32/0.34. Catalog A2 DRILL is printed as a range .32/.34 - not used as one number (never averaged). L - L1 = 0.21 vs the Brennan-measured -06 NPSM TIP_B 0.22 (0.01). Paper check builds with either end of the range and the Air-Way tap drill 0.43. |
| 1405-08-12 | STEP -> **DECIDE** | TFA p4 1405-08-12 | L1=1.62, W1=1.97, C1HEX=1.250, C2HEX=1.250, D=0.635 | TAPDRILL / gate: Q-TRANSFER-TAPDRILL | Catalog TFA p4 1405 1405-08-12: gives L1@DRIVE=1.62, W1@HEX=1.97, C1HEX@HEX=1.250, C2HEX@HEX=1.250, D@BORE=0.635. L - L1 = 0.35 vs the Brennan-measured -12 NPSM TIP_B 0.33 (0.02; the model puts the nut face at W1 and the stem tip at L1 as given). Paper check builds with the Air-Way tap drill 0.70. |
| 1405-20-24 | STEP -> **STEP** | none | - | no catalog row: L1, W1, C1HEX, C2HEX, D, TAPDRILL | No catalog row for this part. |
| 1502-12-08-FG | WORK -> **WORK** | TFA p21 1502-12-08-FG | N3=1.36, M1=1.47, W3=1.75, CHEX=1.000, C1HEX=1.312, D=0.460 | TAPDRILL | Catalog TFA p21 1502-FG 1502-12-08-FG: gives N3@DRIVE=1.36, M1@DRIVE=1.47, W3@HEX=1.75, CHEX@HEX=1.000, C1HEX@HEX=1.312, D@BORE=0.460. |
| 1504-20-20-FG | WORK -> **WORK** | TFA p22 1504-20-20-FG | N2=1.440, M=1.350, W2=1.770, CHEX=1.875, C1HEX=1.875, D=1.020 | TAPDRILL | Catalog TFA p22 1504-FG 1504-20-20-FG: gives N2@DRIVE=1.440, M@DRIVE=1.350, W2@HEX=1.770, CHEX@HEX=1.875, C1HEX@HEX=1.875, D@BORE=1.020. |
| 1504-32-32-FG | WORK -> **WORK** | none | - | no catalog row: N2, M, W2, CHEX, C1HEX, D, TAPDRILL, THDMAJ_A, THDMAJ_A1 | No catalog row for this part. |
| 1601-20-20-20-FG | WORK -> **WORK** | TFA p47 1601-20-20-20-FG | N1=2.38, M1_2=1.73, M1_3=1.73, W3_2=2.15, W3_3=2.15, C2HEX=1.875, C3HEX=1.875, C1HEX=1.625, D2=1.250, D_2=1.020, D3=1.020 | - | Catalog TFA p47 1601-FG 1601-20-20-20-FG: gives N1@DRIVE=2.38, M1_2@DRIVE=1.73, M1_3@DRIVE=1.73, W3_2@HEX=2.15, W3_3@HEX=2.15, C2HEX@HEX=1.875, C3HEX@HEX=1.875, C1HEX@HEX=1.625, D2@BORE=1.250, D_2@BORE=1.020, D3@BORE=1.020. |
| 1602-02-02-02-FG | WORK -> **WORK** | TFA p48 1602-02-02-02-FG | N3=0.660, M1_2=0.800, M1_3=0.800, W3_2=0.940, W3_3=0.940, C2HEX=0.562, C3HEX=0.562, C1HEX=0.562, D2=0.120, D3=0.120 | TAPDRILL | Catalog TFA p48 1602-FG 1602-02-02-02-FG: gives N3@DRIVE=0.660, M1_2@DRIVE=0.800, M1_3@DRIVE=0.800, W3_2@HEX=0.940, W3_3@HEX=0.940, C2HEX@HEX=0.562, C3HEX@HEX=0.562, C1HEX@HEX=0.562, D2@BORE=0.120, D3@BORE=0.120. The catalog prints this part's own -02 nut hex 0.562 (= Brennan NPSM_MEAS -02 AF 0.5625): the Air-Way 0.56 vs 0.69 conflict that made Task C send the nut hexes to the STEP no longer matters for this row (it concerned a transfer). |
| 1602-04-04-04-FG | WORK -> **WORK** | TFA p48 1602-04-04-04-FG | N3=0.880, M1_2=0.990, M1_3=0.990, W3_2=1.180, W3_3=1.180, C2HEX=0.688, C3HEX=0.688, C1HEX=0.750, D2=0.220, D3=0.220 | TAPDRILL | Catalog TFA p48 1602-FG 1602-04-04-04-FG: gives N3@DRIVE=0.880, M1_2@DRIVE=0.990, M1_3@DRIVE=0.990, W3_2@HEX=1.180, W3_3@HEX=1.180, C2HEX@HEX=0.688, C3HEX@HEX=0.688, C1HEX@HEX=0.750, D2@BORE=0.220, D3@BORE=0.220. |
| 1602-16-16-16-FG | WORK -> **WORK** | TFA p48 1602-16-16-16-FG | N3=1.62, M1_2=1.73, M1_3=1.73, W3_2=2.08, W3_3=2.08, C2HEX=1.500, C3HEX=1.500, C1HEX=1.625, D2=0.800, D3=0.800 | TAPDRILL | Catalog TFA p48 1602-FG 1602-16-16-16-FG: gives N3@DRIVE=1.62, M1_2@DRIVE=1.73, M1_3@DRIVE=1.73, W3_2@HEX=2.08, W3_3@HEX=2.08, C2HEX@HEX=1.500, C3HEX@HEX=1.500, C1HEX@HEX=1.625, D2@BORE=0.800, D3@BORE=0.800. |
| 1602-20-20-20-FG | WORK -> **WORK** | TFA p48 1602-20-20-20-FG | N3=1.700, M1_2=1.830, M1_3=1.830, W3_2=2.250, W3_3=2.250, C2HEX=1.875, C3HEX=1.875, C1HEX=1.875, D2=1.020, D3=1.020 | TAPDRILL | Catalog TFA p48 1602-FG 1602-20-20-20-FG: gives N3@DRIVE=1.700, M1_2@DRIVE=1.830, M1_3@DRIVE=1.830, W3_2@HEX=2.250, W3_3@HEX=2.250, C2HEX@HEX=1.875, C3HEX@HEX=1.875, C1HEX@HEX=1.875, D2@BORE=1.020, D3@BORE=1.020. |
| 1700-20-16 | STEP -> **STEP** | FLANGE p3 1700-20-16 | L28=2.800, CHEX=1.625 | O, D | Catalog FLANGE p3 1700 1700-20-16: gives L28@DRIVE=2.800, CHEX@HEX=1.625. |
| 1700-24-20 | STEP -> **STEP** | FLANGE p3 1700-24-20 | L28=3.40, CHEX=2 | O, D | Catalog FLANGE p3 1700 1700-24-20: gives L28@DRIVE=3.40, CHEX@HEX=2. |
| 1700-32-24 | STEP -> **STEP** | FLANGE p3 1700-32-24 | L28=4.20, CHEX=2.622 | O, D | Catalog FLANGE p3 1700 1700-32-24: gives L28@DRIVE=4.20, CHEX@HEX=2.622. Catalog A/F prints 2.622 (1700-32-32 prints 2.625; 2.622 is not a print of a 64th) - possible catalog misprint, flagged. |
| 1703-08-08-FG | WORK -> **WORK** | none | - | no catalog row: N3, M2, O, CHEX, D, THDMAJ_B | No catalog row for this part. No forged 1703-08-08-FG in Brennan's Flange catalog (p4 1703-FG table: -12, -16, -20, -24, -32 only); 1703-08-08 is printed only as the swept elbow (different construction, not used). The required STEP download may not exist (Q-NEW-F2A-NOTINCAT). |
| 1703-08-08-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-08-08 (R1) | uncertain (printed, not carried): N3~0.91, M2~2.72, CHEX~7/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-08-08 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-08-08 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-08-08 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-12-12-FG | WORK -> **WORK** | FLANGE p4 1703-12-12-FG | N3=1.580, M2=1.280, CHEX=1.0625 | O, D | Catalog FLANGE p4 1703-FG 1703-12-12-FG: gives N3@DRIVE=1.580, M2@DRIVE=1.280, CHEX@HEX=1.0625. |
| 1703-12-12-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-12-12 (R1) | uncertain (printed, not carried): N3~1.02, M2~3.15, CHEX~1 1/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-12-12 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-12-12 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-12-12 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-12-16-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-12-16 (R1) | uncertain (printed, not carried): N3~1.02, M2~3.15, CHEX~1 1/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-12-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-12-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-12-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-16-16-FG | WORK -> **WORK** | FLANGE p4 1703-16-16-FG | N3=1.850, M2=1.470, CHEX=1.3125 | O, D | Catalog FLANGE p4 1703-FG 1703-16-16-FG: gives N3@DRIVE=1.850, M2@DRIVE=1.470, CHEX@HEX=1.3125. |
| 1703-16-16-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-16-16 (R1) | uncertain (printed, not carried): N3~1.18, M2~3.66, CHEX~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-16-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-16-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-16-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-16-20-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-16-20 (R1) | uncertain (printed, not carried): N3~1.18, M2~3.66, CHEX~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-16-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-16-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-16-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-16-24-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-16-24 (R1) | uncertain (printed, not carried): N3~1.26, M2~3.74, CHEX~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-16-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-16-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-16-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-20-16-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-20-16 (R1) | uncertain (printed, not carried): N3~1.22, M2~3.86, CHEX~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-20-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-20-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-20-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-20-20-FG | WORK -> **WORK** | FLANGE p4 1703-20-20-FG | N3=2.040, M2=1.590, CHEX=1.625 | O, D | Catalog FLANGE p4 1703-FG 1703-20-20-FG: gives N3@DRIVE=2.040, M2@DRIVE=1.590, CHEX@HEX=1.625. |
| 1703-20-20-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-20-20 (R1) | uncertain (printed, not carried): N3~1.38, M2~4.21, CHEX~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-20-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-20-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-20-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-20-24-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-20-24 (R1) | uncertain (printed, not carried): N3~1.42, M2~4.25, CHEX~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-20-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-20-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-20-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-24-20-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-24-20 (R1) | uncertain (printed, not carried): N3~1.46, M2~4.70, CHEX~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-24-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-24-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-24-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-24-24-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-24-24 (R1) | uncertain (printed, not carried): N3~1.69, M2~4.96, CHEX~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-24-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-24-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-24-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-24-32-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-24-32 (R1) | uncertain (printed, not carried): N3~1.81, M2~5.12, CHEX~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-24-32 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-24-32 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-24-32 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1703-32-32-FG | WORK -> **WORK** | FLANGE p4 1703-32-32-FG | N3=3.000, M2=2.220, CHEX=2.500 | O, D | Catalog FLANGE p4 1703-FG 1703-32-32-FG: gives N3@DRIVE=3.000, M2@DRIVE=2.220, CHEX@HEX=2.500. |
| 1703-32-32-Tube | SCOPE -> **SCOPE** | FLANGE p4 1703-32-32 (R1) | uncertain (printed, not carried): N3~2.17, M2~6.22, CHEX~2 3/4 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p4 1703 1703-32-32 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1703-32-32 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1703-32-32 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-08-08-FG | WORK -> **WORK** | FLANGE p5 1704-08-08-FG | N2=2.050, M=1.460, Y=0.875 | O, D | Catalog FLANGE p5 1704-FG 1704-08-08-FG: gives N2@DRIVE=2.050, M@DRIVE=1.460, Y@HEX=0.875. |
| 1704-08-08-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-08-08 (R1) | uncertain (printed, not carried): N2~1.81, M~2.32, Y~7/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-08-08 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-08-08 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-08-08 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-08-12-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-08-12 (R1) | uncertain (printed, not carried): N2~1.85, M~2.32, Y~7/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-08-12 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-08-12 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-08-12 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-12-12-FG | WORK -> **WORK** | FLANGE p5 1704-12-12-FG | N2=2.130, M=1.660, Y=1.0625 | O, D | Catalog FLANGE p5 1704-FG 1704-12-12-FG: gives N2@DRIVE=2.130, M@DRIVE=1.660, Y@HEX=1.0625. |
| 1704-12-12-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-12-12 (R1) | uncertain (printed, not carried): N2~2.13, M~2.83, Y~1 1/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-12-12 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-12-12 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-12-12 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-12-16-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-12-16 (R1) | uncertain (printed, not carried): N2~2.13, M~2.83, Y~1 1/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-12-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-12-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-12-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-16-12-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-16-12 (R1) | uncertain (printed, not carried): N2~2.13, M~2.95, Y~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-16-12 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-16-12 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-16-12 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-16-16-FG | WORK -> **WORK** | FLANGE p5 1704-16-16-FG | N2=2.370, M=1.811, Y=1.3125 | O, D | Catalog FLANGE p5 1704-FG 1704-16-16-FG: gives N2@DRIVE=2.370, M@DRIVE=1.811, Y@HEX=1.3125. |
| 1704-16-16-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-16-16 (R1) | uncertain (printed, not carried): N2~2.60, M~3.39, Y~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-16-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-16-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-16-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-16-20-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-16-20 (R1) | uncertain (printed, not carried): N2~2.60, M~3.39, Y~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-16-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-16-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-16-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-16-24-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-16-24 (R1) | uncertain (printed, not carried): N2~2.66, M~3.39, Y~1 3/8 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-16-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-16-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-16-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-20-12-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-20-12 (R1) | uncertain (printed, not carried): N2~2.26, M~3.052, Y~1.6875 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-20-12 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-20-12 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-20-12 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-20-16-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-20-16 (R1) | uncertain (printed, not carried): N2~2.60, M~3.54, Y~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-20-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-20-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-20-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-20-20-FG | WORK -> **WORK** | FLANGE p5 1704-20-20-FG | N2=2.620, M=2.060, Y=1.625 | O, D | Catalog FLANGE p5 1704-FG 1704-20-20-FG: gives N2@DRIVE=2.620, M@DRIVE=2.060, Y@HEX=1.625. |
| 1704-20-20-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-20-20 (R1) | uncertain (printed, not carried): N2~3.03, M~3.98, Y~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-20-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-20-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-20-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-20-24-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-20-24 (R1) | uncertain (printed, not carried): N2~3.11, M~3.98, Y~1 11/16 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-20-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-20-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-20-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-20-32-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-20-32 (R1) | uncertain (printed, not carried): N2~3.504, M~3.976, Y~1.688 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-20-32 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-20-32 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-20-32 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-24-16-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-24-16 (R1) | uncertain (printed, not carried): N2~2.849, M~4.039, Y~2.000 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-24-16 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-24-16 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-24-16 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-24-20-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-24-20 (R1) | uncertain (printed, not carried): N2~3.03, M~4.21, Y~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-24-20 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-24-20 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-24-20 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-24-24-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-24-24 (R1) | uncertain (printed, not carried): N2~3.66, M~4.57, Y~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-24-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-24-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-24-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-24-32-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-24-32 (R1) | uncertain (printed, not carried): N2~3.86, M~4.57, Y~2 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-24-32 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-24-32 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-24-32 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-32-24-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-32-24 (R1) | uncertain (printed, not carried): N2~3.66, M~5.04, Y~2 3/4 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-32-24 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-32-24 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-32-24 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 1704-32-32-Tube | SCOPE -> **SCOPE** | FLANGE p5 1704-32-32 (R1) | uncertain (printed, not carried): N2~4.84, M~5.79, Y~2 3/4 | O, D, (no column yet) bend radius, (no column yet) tube OD, (no column yet) tube wall | Catalog FLANGE p5 1704 1704-32-32 (R1 swept): gives no usable body dimension. Brennan sells this swept (bent-tube) elbow as 1704-32-32 (match/Flange.json rule R1); its L1 / L2 / A/F are shown as printed but not paired - no swept master or column set exists yet (one master per shape). Bend radius, tube OD and wall are not printed; a Brennan STEP of 1704-32-32 could give them if the user puts the swept elbows in scope (no such download is on the step list). |
| 2403-04-02 | WORK -> **WORK** | TFA p5 2403-04-02 | L1=1.270, HEXB=0.500, D1=0.172, D2=0.062 | - | Catalog TFA p5 2403 2403-04-02: gives L1@DRIVE=1.270, HEXB@HEX=0.500, D1@BORE=0.172, D2@BORE=0.062. |
| 2403-06-02 | WORK -> **WORK** | none | - | no catalog row: L1, HEXB, D1, D2 | No catalog row for this part. |
| 2403-10-04 | WORK -> **WORK** | TFA p5 2403-10-04 | L1=1.67, HEXB=0.937, D1=0.484, D2=0.172 | - | Catalog TFA p5 2403 2403-10-04: gives L1@DRIVE=1.67, HEXB@HEX=0.937, D1@BORE=0.484, D2@BORE=0.172. |
| 2403-16-10 | WORK -> **WORK** | TFA p5 2403-16-10 | L1=2.10, HEXB=1.375, D1=0.844, D2=0.484 | - | Catalog TFA p5 2403 2403-16-10: gives L1@DRIVE=2.10, HEXB@HEX=1.375, D1@BORE=0.844, D2@BORE=0.484. |
| 2403-24-16 | WORK -> **WORK** | TFA p5 2403-24-16 | L1=2.580, HEXB=2.000, D1=1.312, D2=0.844 | - | Catalog TFA p5 2403 2403-24-16: gives L1@DRIVE=2.580, HEXB@HEX=2.000, D1@BORE=1.312, D2@BORE=0.844. |
| 2403-LH-24-24 | WORK -> **WORK** | TFA p5 2403-LH-24-24 | L1=2.75, C2HEX=2.125, D1=1.312, D2=1.312 | - | Catalog TFA p5 2403-LH 2403-LH-24-24: gives L1@DRIVE=2.75, C2HEX@HEX=2.125, D1@BORE=1.312, D2@BORE=1.312. |
| 2404-L-32-32 | WORK -> **WORK** | TFA p6 2404-L-32-32 | L20=5.620, CHEX=2.625, D=1.781, D1=1.938 | T20REF | Catalog TFA p6 2404-L 2404-L-32-32: gives L20@DRIVE=5.620, CHEX@HEX=2.625, D@BORE=1.781, D1@BORE=1.938. |
| 2405-10-06 | WORK -> **WORK** | TFA p7 2405-10-06 | L2=1.670, HEXB=0.938, D3=0.484 | TAPDRILL | Catalog TFA p7 2405 2405-10-06: gives L2@DRIVE=1.670, HEXB@HEX=0.938, D3@BORE_THRU=0.484. |
| 2405-14-12 | WORK -> **WORK** | TFA p7 2405-14-12 | L2=2.06, HEXB=1.375, D3=0.719 | TAPDRILL | Catalog TFA p7 2405 2405-14-12: gives L2@DRIVE=2.06, HEXB@HEX=1.375, D3@BORE_THRU=0.719. |
| 2406-03-04 | WORK -> **WORK** | TFA p7 2406-03-04 | L23=0.980, HEXB=0.500, D3=0.125 | - | Catalog TFA p7 2406 2406-03-04: gives L23@DRIVE=0.980, HEXB@HEX=0.500, D3@BORE=0.125. |
| 2406-04-02 | STEP -> **NOW** | TFA p7 2406-04-02 | L23=1.04, HEXB=0.563, D3=0.062 | - | Catalog TFA p7 2406 2406-04-02: gives L23@DRIVE=1.04, HEXB@HEX=0.563, D3@BORE=0.062. |
| 2406-04-04 | STEP -> **NOW** | TFA p7 2406-04-04 | L23=1.15, HEXB=0.562, D3=0.172 | - | Catalog TFA p7 2406 2406-04-04: gives L23@DRIVE=1.15, HEXB@HEX=0.562, D3@BORE=0.172. |
| 2406-04-08 | STEP -> **NOW** | TFA p7 2406-04-08 | L23=1.25, HEXB=0.812, D3=0.172 | - | Catalog TFA p7 2406 2406-04-08: gives L23@DRIVE=1.25, HEXB@HEX=0.812, D3@BORE=0.172. |
| 2406-06-10 | STEP -> **NOW** | TFA p7 2406-06-10 | L23=1.38, HEXB=0.937, D3=0.297 | - | Catalog TFA p7 2406 2406-06-10: gives L23@DRIVE=1.38, HEXB@HEX=0.937, D3@BORE=0.297. |
| 2406-06-12 | STEP -> **STEP** | none | - | no catalog row: L23, HEXB, D3 | No catalog row for this part. |
| 2406-08-08 | DECIDE -> **NOW** | TFA p7 2406-08-08 | L23=1.41, HEXB=0.875, D3=0.391 | - | Catalog TFA p7 2406 2406-08-08: gives L23@DRIVE=1.41, HEXB@HEX=0.875, D3@BORE=0.391. |
| 2406-10-16 | STEP -> **NOW** | TFA p7 2406-10-16 | L23=1.76, HEXB=1.375, D3=0.484 | - | Catalog TFA p7 2406 2406-10-16: gives L23@DRIVE=1.76, HEXB@HEX=1.375, D3@BORE=0.484. |
| 2406-12-04 | STEP -> **NOW** | TFA p7 2406-12-04 | L23=1.50, HEXB=1.250, D3=0.172 | - | Catalog TFA p7 2406 2406-12-04: gives L23@DRIVE=1.50, HEXB@HEX=1.250, D3@BORE=0.172. Paper check: the female -12 port reaches 0.355 from the male tip, inside the -04 male thread zone; the generator reports a radial wall of 0.035 there (OK) - thin but buildable. |
| 2406-12-12 | STEP -> **NOW** | TFA p7 2406-12-12 | L23=1.77, HEXB=1.250, D3=0.609 | - | Catalog TFA p7 2406 2406-12-12: gives L23@DRIVE=1.77, HEXB@HEX=1.250, D3@BORE=0.609. |
| 2501-24-32-FG | DECIDE -> **NOW** | TFA p23 2501-24-32-FG | Y=2.500, D=1.312, D1=1.938, M=2.81, N=3.00 | - | Catalog TFA p23 2501-FG 2501-24-32-FG: gives Y@REF=2.500, D@BORE=1.312, D1@DRILL=1.938, M@DRIVE=2.81, N@DRIVE=3.00. OMi: 4/5 compared cells agree (differ: D1@DRILL). OMi Side 2 ID 1.940 (Items!X699) vs catalog A2 DRILL 1.938 (= 1-15/16): REAL under the strict rule (0.002); OMi's own 2501-32-32-FG and 5500-32-32-FG print 1.938. OMi kept by the standing rule; difference -> $COMMENT (Q-NEW-F2A-OMIvsCAT). |
| 2501-40-40-FG | WORK -> **WORK** | TFA p23 2501-40-40-FG | Y=3.234, D=2.318, D1=2.318, M=3.25, N=3.95 | JIC_RELIEFL, RELIEFANG, JIC_THDZ, JIC_CONEDIA, JIC_LANDL, JIC_SEATL, SEATB, NPTF_E0, NPTF_E1, NPTF_L2 | Catalog TFA p23 2501-FG 2501-40-40-FG: gives Y@REF=3.234, D@BORE=2.318, D1@DRILL=2.318, M@DRIVE=3.25, N@DRIVE=3.95. OMi: 5/5 compared cells agree. |
| 2502-20-16-FG | STEP -> **STEP** | none | - | no catalog row: M1, N1, Y1, D, TAPDRILL | No catalog row for this part. |
| 2502-32-32-FG | DECIDE -> **DECIDE** | TFA p25 2502-32-32-FG | Y1=2.812, D=1.781, M1=3.30, N1=2.39 | TAPDRILL / gate: Q-CONFLICT-TAPDRILL-32, Q-HX, Q-TRANSFER-TAPDRILL | Catalog TFA p25 2502-FG 2502-32-32-FG: gives Y1@DRIVE=2.812, D@BORE=1.781, M1@DRIVE=3.30, N1@DRIVE=2.39. OMi: 4/4 compared cells agree. Catalog equals OMi (= MS51506F A32) on M1 3.30, N1 2.39, Y1 2.812, D 1.781; Q-B-ELBOW answered; the tap drill is not printed (Q-TRANSFER-TAPDRILL / Q-CONFLICT-TAPDRILL-32 stay) and Q-HX stays. |
| 2503-24-20-FG | DECIDE -> **NOW** | TFA p26 2503-24-20-FG | Y=1.875, D=1.312, D1=1.250, M2=1.78, N2=1.74 | - | Catalog TFA p26 2503-FG 2503-24-20-FG: gives Y@REF=1.875, D@BORE=1.312, D1@BORE=1.250, M2@DRIVE=1.78, N2@DRIVE=1.74. OMi: 5/5 compared cells agree. Catalog equals OMi on all five values (M 1.78, L 1.74, flats 1.875, drills 1.312 / 1.250) - this size is not one of the two OMi M1/L1 swaps the audit found. |
| 2603-02-02-02-FG | DECIDE -> **DECIDE** | TFA p49 2603-02-02-02-FG | Y=0.438, D1=0.062, D2=0.062, D3=0.062, LEG1=0.77, LEG2=0.77, LEG3=0.77 | - / gate: Q-HX | Catalog TFA p49 2603-FG 2603-02-02-02-FG: gives Y@REF=0.438, D1@BORE=0.062, D2@BORE=0.062, D3@BORE=0.062, LEG1@DRIVE=0.77, LEG2@DRIVE=0.77, LEG3@DRIVE=0.77. OMi: 7/7 compared cells agree. Catalog equals OMi (= MS51510E) on every value: legs 0.77, flats 0.438, drills 0.062. Q-HX (hand-append to 2603HX vs port to the generator) is a process decision the catalog cannot answer. |
| 2606-12-12-12-FG | WORK -> **WORK** | TFA p51 2606-12-12-12-FG | M1_1=1.81, N1=1.36, M1_3=1.81, Y1=1.312, D1=0.609, D3=0.609 | TAPDRILL | Catalog TFA p51 2606-FG 2606-12-12-12-FG: gives M1_1@DRIVE=1.81, N1@DRIVE=1.36, M1_3@DRIVE=1.81, Y1@HEX=1.312, D1@BORE=0.609, D3@BORE=0.609. OMi: 6/6 compared cells agree. |
| 2609-08-08-08-FG | WORK -> **WORK** | TFA p52 2609-08-08-08-FG | M1=1.520, N1_2=1.230, N1_3=1.230, Y1=1.062, D=0.391 | TAPDRILL2, TAPDRILL3 | Catalog TFA p52 2609-FG 2609-08-08-08-FG: gives M1@DRIVE=1.520, N1_2@DRIVE=1.230, N1_3@DRIVE=1.230, Y1@HEX=1.062, D@BORE=0.391. OMi: 5/5 compared cells agree. |
| 2611-08-08-08-FG | WORK -> **WORK** | TFA p52 2611-08-08-08-FG | M1=1.52, N5=1.47, N1=1.23, Y1=1.062, D=0.391, D1=0.531 | TAPDRILL | Catalog TFA p52 2611-FG 2611-08-08-08-FG: gives M1@DRIVE=1.52, N5@DRIVE=1.47, N1@DRIVE=1.23, Y1@HEX=1.062, D@BORE=0.391, D1@BORE=0.531. OMi: 6/6 compared cells agree. |
| 2700-02-02 | STEP -> **STEP** | TFA p8 2700-02-02 | L4=1.870, C2HEX=0.562, D1=0.062, D2=0.062 | I1 | Catalog TFA p8 2700 2700-02-02: gives L4@DRIVE=1.870, C2HEX@HEX=0.562, D1@BORE=0.062, D2@BORE=0.062. |
| 2700-04-02 | STEP -> **STEP** | none | - | no catalog row: L4, I1, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-08-06 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-10-08 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-12-10 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-LN-02-02 | STEP -> **STEP** | TFA p8 2700-02-02 (LN_form) | L4=1.870, C2HEX=0.562, D1=0.062, D2=0.062 | I1 | Catalog TFA p8 2700 2700-02-02 (LN_form): gives L4@DRIVE=1.870, C2HEX@HEX=0.562, D1@BORE=0.062, D2@BORE=0.062. |
| 2700-LN-04-02 | STEP -> **STEP** | none | - | no catalog row: L4, I1, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-LN-08-06 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-LN-10-08 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2700-LN-12-10 | STEP -> **STEP** | none | - | no catalog row: L4, C2HEX, D1, D2 | No catalog row for this part. |
| 2701-02-02-FG | STEP -> **STEP** | TFA p27 2701-02-02-FG | M3=0.88, M4=1.50, Y=0.438, D1=0.062, D2=0.062 | i2, K1, O | Catalog TFA p27 2701-FG 2701-02-02-FG: gives M3@DRIVE=0.88, M4@DRIVE=1.50, Y@HEX=0.438, D1@BORE=0.062, D2@BORE=0.062. |
| 2701-05-05-FG | STEP -> **STEP** | TFA p27 2701-05-05-FG | M3=1.06, M4=1.72, Y=0.562, D1=0.234, D2=0.234 | i2, K1, O | Catalog TFA p27 2701-FG 2701-05-05-FG: gives M3@DRIVE=1.06, M4@DRIVE=1.72, Y@HEX=0.562, D1@BORE=0.234, D2@BORE=0.234. |
| 2705-04-02 | STEP -> **STEP** | none | - | no catalog row: I1 | No catalog row for this part. |
| 2705-LN-04-02 | STEP -> **STEP** | none | - | no catalog row: I1 | No catalog row for this part. |
| 2705-LN-06-04 | DECIDE -> **DECIDE** | TFA p8 2705-06-04 (LN_form) | L24=2.190, C5HEX=0.875, D=0.172 | - / gate: Q-TRANSFER-I1, Q-TRANSFER-TAPDRILL | Catalog TFA p8 2705 2705-06-04 (LN_form): gives L24@DRIVE=2.190, C5HEX@HEX=0.875, D@BORE=0.172. OMi: 3/3 compared cells agree. Catalog 2705-06-04 (LN_form) equals OMi on length 2.190, hex 0.875 and bore 0.172 (same source). I1 and the tap drill are not printed - the transfer questions stay. |
| 2706-04-02 | STEP -> **STEP** | TFA p9 2706-04-02 | L25=1.980, C2HEX=0.625, D1=0.281, D=0.062 | I1 | Catalog TFA p9 2706 2706-04-02: gives L25@DRIVE=1.980, C2HEX@HEX=0.625, D1@BORE=0.281, D@BORE=0.062. OMi: 4/4 compared cells agree. |
| 2706-06-04 | DECIDE -> **DECIDE** | none | - | no catalog row / gate: Q-TRANSFER-I1 | No catalog row for this part. |
| 2706-32-32 | DECIDE -> **DECIDE** | TFA p9 2706-32-32 | L25=3.91, C2HEX=2.750, D1=1.938, D=1.781 | - / gate: Q-TRANSFER-I1 | Catalog TFA p9 2706 2706-32-32: gives L25@DRIVE=3.91, C2HEX@HEX=2.750, D1@BORE=1.938, D@BORE=1.781. OMi: 4/4 compared cells agree. Catalog equals OMi on all four values (3.91 / 2.750 / 1.938 / 1.781). I1 is not printed - Q-TRANSFER-I1 stays. |
| 2706-LN-04-02 | STEP -> **STEP** | TFA p9 2706-04-02 (LN_form) | L25=1.980, C2HEX=0.625, D1=0.281, D=0.062 | I1 | Catalog TFA p9 2706 2706-04-02 (LN_form): gives L25@DRIVE=1.980, C2HEX@HEX=0.625, D1@BORE=0.281, D@BORE=0.062. OMi: 4/4 compared cells agree. |
| 2706-LN-06-04 | DECIDE -> **DECIDE** | none | - | no catalog row / gate: Q-TRANSFER-I1 | No catalog row for this part. |
| 2706-LN-08-06 | DECIDE -> **DECIDE** | TFA p9 2706-08-06 (LN_form) | L25=2.410, C2HEX=0.875, D1=0.531, D=0.297 | - / gate: Q-TRANSFER-I1 | Catalog TFA p9 2706 2706-08-06 (LN_form): gives L25@DRIVE=2.410, C2HEX@HEX=0.875, D1@BORE=0.531, D@BORE=0.297. OMi: 2/4 compared cells agree (differ: L25@DRIVE, D@BORE). Catalog 2706-08-06 (LN_form) vs OMi Items!L1091 / X1091: L 2.410 vs 2.400 (REAL 0.010) and B2 DRILL 0.297 (= 19/64) vs 0.295 (REAL 0.002) - match/TFA_straights_diffcheck.json idx 19-20 (same on the plain twin Items!L1076 / X1076); Air-Way 2706-8-6 had L 2.34. Three makers' prints of one length disagree: OMi kept by the standing rule, the difference |
| 5000-06-02 | STEP -> **DECIDE** | TFA p10 5000-06-02 | L=1.130, CHEX=0.875 | TAPDRILL1, TAPDRILL2 / gate: Q-TRANSFER-TAPDRILL | Catalog TFA p10 5000 5000-06-02: gives L@DRIVE=1.130, CHEX@HEX=0.875. |
| 5000-16-08 | STEP -> **DECIDE** | TFA p10 5000-16-08 | L=1.890, CHEX=1.625 | TAPDRILL1, TAPDRILL2 / gate: Q-TRANSFER-TAPDRILL | Catalog TFA p10 5000 5000-16-08: gives L@DRIVE=1.890, CHEX@HEX=1.625. |
| 5000-24-20 | STEP -> **DECIDE** | TFA p10 5000-24-20 | L=1.930, CHEX=2.375 | TAPDRILL1, TAPDRILL2 / gate: Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24 | Catalog TFA p10 5000 5000-24-20: gives L@DRIVE=1.930, CHEX@HEX=2.375. |
| 5000-40-40 | WORK -> **WORK** | TFA p10 5000-40-40 | L=2.670, CHEX=3.500 | TAPDRILL1, TAPDRILL2 | Catalog TFA p10 5000 5000-40-40: gives L@DRIVE=2.670, CHEX@HEX=3.500. |
| 5404-16-04 | STEP -> **NOW** | TFA p11 5404-16-04 | L=1.960, HEXB=1.375, D1=0.938, D2=0.281 | - | Catalog TFA p11 5404 5404-16-04: gives L@DRIVE=1.960, HEXB@HEX=1.375, D1@BORE=0.938, D2@BORE=0.281. |
| 5404-20-12 | STEP -> **NOW** | TFA p11 5404-20-12 | L=2.260, HEXB=1.750, D1=1.250, D2=0.719 | - | Catalog TFA p11 5404 5404-20-12: gives L@DRIVE=2.260, HEXB@HEX=1.750, D1@BORE=1.250, D2@BORE=0.719. |
| 5404-24-12 | STEP -> **NOW** | TFA p11 5404-24-12 | L=2.380, HEXB=2.000, D1=1.500, D2=0.719 | - | Catalog TFA p11 5404 5404-24-12: gives L@DRIVE=2.380, HEXB@HEX=2.000, D1@BORE=1.500, D2@BORE=0.719. |
| 5404-32-12 | STEP -> **NOW** | TFA p11 5404-32-12 | L=2.540, HEXB=2.500, D1=1.938, D2=0.719 | - | Catalog TFA p11 5404 5404-32-12: gives L@DRIVE=2.540, HEXB@HEX=2.500, D1@BORE=1.938, D2@BORE=0.719. |
| 5404-32-16 | STEP -> **NOW** | TFA p11 5404-32-16 | L=2.630, HEXB=2.500, D1=1.938, D2=0.938 | - | Catalog TFA p11 5404 5404-32-16: gives L@DRIVE=2.630, HEXB@HEX=2.500, D1@BORE=1.938, D2@BORE=0.938. |
| 5404-40-40 | WORK -> **WORK** | TFA p11 5404-40-40 | L=3.950, HEXB=3.000, D1=2.318, D2=2.318 | NPTFA_ENDL, NPTFA_E0, NPTFA_E1, NPTFA_L2, NPTFB_ENDL, NPTFB_E0, NPTFB_E1, NPTFB_L2 | Catalog TFA p11 5404 5404-40-40: gives L@DRIVE=3.950, HEXB@HEX=3.000, D1@BORE=2.318, D2@BORE=2.318. |
| 5404-L-04X2.000 | WORK -> **WORK** | none | - | no catalog row: L, HEXB, D1, D2 | No catalog row for this part. |
| 5404-L-04X3.000 | WORK -> **WORK** | none | - | no catalog row: L, HEXB, D1, D2 | No catalog row for this part. Boundary row: index 140 of the 281 F2 rows sorted by config - also in F2b (both halves include it). |

## Step list items touching F2a rows

| pn | stage | in repo | F2a rows (required / conditional / reference) | verdict | still needed for |
|---|---|---|---|---|---|
| 1405-04-06 | 1A | no | req 1405-04-06 | partly | bore D (catalog prints the A2 drill as a range .32/.34) and the female -04 tap drill (not printed; Q-TRANSFER-TAPDRILL 0.43 or the STEP) |
| 1405-08-12 | 1A | no | req 1405-08-12 | partly | the female -08 tap drill only (not printed; Q-TRANSFER-TAPDRILL 0.70 or the STEP) |
| 1405-20-24 | 1A | no | req 1405-20-24 | not_replaced | part not in the catalog (TFA p4 1405 table has no 1405-20-24): every body dimension |
| 1700-20-16 | 1A | no | req 1700-20-16 | partly | head diameter O, bore D and the round collar / neck geometry (Q-NEW-1700BODY); L and the wrench-flat A/F now come from the catalog |
| 1700-24-20 | 1A | no | req 1700-24-20 | partly | head diameter O, bore D and the round collar / neck geometry (Q-NEW-1700BODY); L and the wrench-flat A/F now come from the catalog |
| 1700-32-24 | 1A | no | req 1700-32-24 | partly | head diameter O, bore D and the round collar / neck geometry (Q-NEW-1700BODY); L and the wrench-flat A/F now come from the catalog |
| 2406-04-02 | 1A | no | req 2406-04-02 | replaced_by_catalog | - |
| 2406-04-04 | 1A | no | req 2406-04-04 | replaced_by_catalog | - |
| 2406-04-08 | 1A | no | req 2406-04-08 | replaced_by_catalog | - |
| 2406-06-10 | 1A | no | req 2406-06-10 | replaced_by_catalog | - |
| 2406-06-12 | 1A | no | req 2406-06-12 | not_replaced | part not in the catalog (TFA p7-8 2406 table): L23, hex, bore D3 |
| 2406-10-16 | 1A | no | req 2406-10-16 | replaced_by_catalog | - |
| 2406-12-04 | 1A | no | req 2406-12-04 | replaced_by_catalog | - |
| 2406-12-12 | 1A | no | req 2406-12-12 | replaced_by_catalog | - |
| 2502-20-16-FG | 1A | no | req 2502-20-16-FG | not_replaced | part not in the catalog (TFA p25 2502-FG table has 20-20 but no 20-16): legs M1/N1, hex Y1, bore D, tap drill |
| 2700-02-02 | 1A | no | req 2700-02-02, 2700-LN-02-02 | partly | bulkhead length I1 at -02 only (not printed; no Air-Way -02 bulkhead); L4 / hex / bores now from the catalog |
| 2700-04-02 | 1A | no | req 2700-04-02, 2700-LN-04-02 | not_replaced | part not in the catalog (TFA p8 2700 table: equal sizes plus 04-06 / 06-04 / 16-12 only): L4, hex, bores, I1 at -02 |
| 2700-08-06 | 1A | no | req 2700-08-06, 2700-LN-08-06 | not_replaced | part not in the catalog (TFA p8 2700 table: equal sizes plus 04-06 / 06-04 / 16-12 only): L4, hex, bores |
| 2700-10-08 | 1A | no | req 2700-10-08, 2700-LN-10-08 | not_replaced | part not in the catalog (TFA p8 2700 table: equal sizes plus 04-06 / 06-04 / 16-12 only): L4, hex, bores |
| 2700-12-10 | 1A | no | req 2700-12-10, 2700-LN-12-10 | not_replaced | part not in the catalog (TFA p8 2700 table: equal sizes plus 04-06 / 06-04 / 16-12 only): L4, hex, bores |
| 2701-02-02-FG | 1A | no | req 2701-02-02-FG | partly | bulkhead relief length i2, collar length K1 and collar diameter O (not printed); legs / hex / bores now from the catalog |
| 2701-05-05-FG | 1A | no | req 2701-05-05-FG | partly | bulkhead relief length i2, collar length K1 and collar diameter O (not printed); legs / hex / bores now from the catalog |
| 2705-04-02 | 1A | no | req 2705-04-02, 2705-LN-04-02 | not_replaced | part not in the catalog (TFA p8 2705 table has 02-04 / 04-04 / 04-06 but no 04-02): I1 at -02 (and the cross-check of the OMi values) |
| 2706-04-02 | 1A | no | req 2706-04-02, 2706-LN-04-02 | partly | bulkhead length I1 at -02 only (not printed); the cross-check of the OMi length / hex / bores is done by the catalog (same source, all equal) |
| 5000-06-02 | 1A | no | req 5000-06-02 | partly | the two tap drills only (not printed; Q-TRANSFER-TAPDRILL, else the STEP) |
| 5000-16-08 | 1A | no | req 5000-16-08 | partly | the two tap drills only (not printed; Q-TRANSFER-TAPDRILL, else the STEP) |
| 5000-24-20 | 1A | no | req 5000-24-20 | partly | the two tap drills only (not printed; -20 by Q-TRANSFER-TAPDRILL, -24 by Q-CONFLICT-TAPDRILL-24 1.72 / 1.70, else the STEP) |
| 5404-16-04 | 1A | no | req 5404-16-04 | replaced_by_catalog | - |
| 5404-20-12 | 1A | no | req 5404-20-12 | replaced_by_catalog | - |
| 5404-24-12 | 1A | no | req 5404-24-12 | replaced_by_catalog | - |
| 5404-32-12 | 1A | no | req 5404-32-12 | replaced_by_catalog | - |
| 5404-32-16 | 1A | no | req 5404-32-16 | replaced_by_catalog | - |
| 2403-04-02 | 1B | no | req 2403-04-02 | replaced_by_catalog | - |
| 2403-06-02 | 1B | no | req 2403-06-02 | not_replaced | part not in the catalog (TFA p5 2403 table has 06-04 / 06-05 / 06-06 but no 06-02): length, hex, bores |
| 2403-10-04 | 1B | no | req 2403-10-04 | replaced_by_catalog | - |
| 2403-16-10 | 1B | no | req 2403-16-10 | replaced_by_catalog | - |
| 2403-24-16 | 1B | no | req 2403-24-16 | replaced_by_catalog | - |
| 2403-LH-24-24 | 1B | no | req 2403-LH-24-24 | replaced_by_catalog | - |
| 2404-L-32-32 | 1B | no | req 2404-L-32-32 | partly | hex length T20 (T20REF@REF) - not printed; L20 / hex / bores now from the catalog |
| 2405-10-06 | 1B | no | req 2405-10-06 | partly | tap drill (not printed; Q-TRANSFER-TAPDRILL -06 0.57) and the port depth check (FPT_P1 = MS51503 library value) |
| 2405-14-12 | 1B | no | req 2405-14-12 | partly | tap drill (not printed; Q-TRANSFER-TAPDRILL -12 0.91) and the port depth check (FPT_P1 = MS51503 library value) |
| 2406-03-04 | 1B | no | req 2406-03-04 | partly | the female -03 JIC port geometry (JICF_MEAS has no -03; tools/measure/ports.py); L23 / hex / bore now from the catalog |
| 2501-40-40-FG | 1B | no | req 2501-40-40-FG | partly | -40 end geometry (MS33656J -40 JIC chain, ASME 2-1/2 NPTF row: Q-NEW-ASME40), port depth / tap drill; legs / hex / bores now from the catalog (= OMi) |
| 5000-40-40 | 1B | no | req 5000-40-40 | partly | -40 female NPTF port geometry and tap drills (Q-NEW-ASME40); L and hex now from the catalog |
| 5404-40-40 | 1B | no | req 5404-40-40 | partly | -40 male NPTF end geometry (end length, E0 / E1 / L2, pipe OD; Q-NEW-ASME40); L, hex and bores now from the catalog |
| 0304-C-08 | 2 | no | req 0304-C-08 | partly | cap crown shape (family construction sample); length + hex + part number now from the catalog |
| 0306-08 | 2 | no | req 0306-08 | partly | chamfers / faces (family construction sample); thickness + hex + part number now from the catalog |
| 5404-L-04X2.000 | 2 | no | req 5404-L-04X2.000 | not_replaced | Brennan prints no 5404-L long HEX nipple (TFA p11-12 list only the round 5404-N long nipples, no hex): hex A/F, hex length / position, bore, overall length - confirm the part first (Q-NEW-BRENNANPN) |
| 0304-C-02 | 3 | no | req 0304-C-02 | partly | female JIC -02 port geometry (not in JICF_MEAS); length + hex + part number now from the catalog |
| 0304-C-03 | 3 | no | req 0304-C-03 | partly | female JIC -03 port geometry (not in JICF_MEAS); length + hex + part number now from the catalog |
| 0306-02 | 3 | no | req 0306-02 | partly | chamfers / faces (family construction sample); thickness + hex + part number now from the catalog |
| 0306-32 | 3 | no | req 0306-32 | partly | chamfers / faces (family construction sample); thickness + hex + part number now from the catalog |
| 1502-12-08-FG | 3 | no | req 1502-12-08-FG | partly | forged-body geometry (new 1502 SPEC) and the female -12 tap drill (Q-TRANSFER-TAPDRILL 0.91); legs / hexes / bore now from the catalog |
| 1504-20-20-FG | 3 | no | req 1504-20-20-FG | partly | forged-body geometry (new 1504 SPEC, angled helix) and the female -20 tap drill (Q-TRANSFER-TAPDRILL 1.48); legs / hexes / bore now from the catalog |
| 1504-32-32-FG | 3 | no | req 1504-32-32-FG | not_replaced | part not in the catalog (TFA p22 1504-FG table stops at 24-24): every body dimension and the forged geometry |
| 1601-20-20-20-FG | 3 | no | req 1601-20-20-20-FG | partly | forged-body geometry (new 1601 SPEC, two swivel legs); legs / hexes / bores now from the catalog |
| 1602-02-02-02-FG | 3 | no | req 1602-02-02-02-FG | partly | forged-body geometry (new 1602 SPEC, two swivel legs) and the female branch tap drill (Q-TRANSFER-TAPDRILL); legs / hexes / bores now from the catalog |
| 1602-04-04-04-FG | 3 | no | req 1602-04-04-04-FG | partly | forged-body geometry (new 1602 SPEC, two swivel legs) and the female branch tap drill (Q-TRANSFER-TAPDRILL); legs / hexes / bores now from the catalog |
| 1602-16-16-16-FG | 3 | no | req 1602-16-16-16-FG | partly | forged-body geometry (new 1602 SPEC, two swivel legs) and the female branch tap drill (Q-TRANSFER-TAPDRILL); legs / hexes / bores now from the catalog |
| 1602-20-20-20-FG | 3 | no | req 1602-20-20-20-FG | partly | forged-body geometry (new 1602 SPEC, two swivel legs) and the female branch tap drill (Q-TRANSFER-TAPDRILL); legs / hexes / bores now from the catalog |
| 1703-08-08-FG | 3 | no | req 1703-08-08-FG | not_replaced | no forged 1703-08-08-FG in the catalog (Flange p4 1703-FG table: 12-12 / 16-16 / 20-20 / 24-24 / 32-32 only; 1703-08-08 is printed only as the swept elbow): every body dimension and the forged geometry |
| 1703-12-12-FG | 3 | no | req 1703-12-12-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1703-16-16-FG | 3 | no | req 1703-16-16-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1703-20-20-FG | 3 | no | req 1703-20-20-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1703-32-32-FG | 3 | no | req 1703-32-32-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1704-08-08-FG | 3 | no | req 1704-08-08-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1704-12-12-FG | 3 | no | req 1704-12-12-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1704-16-16-FG | 3 | no | req 1704-16-16-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 1704-20-20-FG | 3 | no | req 1704-20-20-FG | partly | bore D (not printed), head diameter O (not printed; Q-TRANSFER-FLG61-O) and the forged-body geometry; legs and A/F now from the catalog |
| 0304-C-04 | CONDITIONAL | no | cond 0304-C-04 | replaced_by_catalog | - |
| 0304-C-05 | CONDITIONAL | no | cond 0304-C-05 | replaced_by_catalog | - |
| 0304-C-06 | CONDITIONAL | no | cond 0304-C-06 | replaced_by_catalog | - |
| 0304-C-10 | CONDITIONAL | no | cond 0304-C-10 | replaced_by_catalog | - |
| 0304-C-12 | CONDITIONAL | no | cond 0304-C-12 | replaced_by_catalog | - |
| 0304-C-14 | CONDITIONAL | no | cond 0304-C-14 | replaced_by_catalog | - |
| 0304-C-16 | CONDITIONAL | no | cond 0304-C-16 | replaced_by_catalog | - |
| 0304-C-20 | CONDITIONAL | no | cond 0304-C-20 | replaced_by_catalog | - |
| 0304-C-24 | CONDITIONAL | no | cond 0304-C-24 | replaced_by_catalog | - |
| 0304-C-32 | CONDITIONAL | no | cond 0304-C-32 | partly | only if the user wants the hex settled by a measurement: catalog C HEX 2.880 vs OMi Hex Flat 2.875 (Items!R16) is a REAL difference under the strict rule (likely 2.88 = 2-7/8 padded); the cap length 1.440 = OMi |
| 0306-03 | CONDITIONAL | no | cond 0306-03 | replaced_by_catalog | - |
| 0306-04 | CONDITIONAL | no | cond 0306-04 | replaced_by_catalog | - |
| 0306-05 | CONDITIONAL | no | cond 0306-05 | replaced_by_catalog | - |
| 0306-06 | CONDITIONAL | no | cond 0306-06 | replaced_by_catalog | - |
| 0306-10 | CONDITIONAL | no | cond 0306-10 | replaced_by_catalog | - |
| 0306-12 | CONDITIONAL | no | cond 0306-12 | replaced_by_catalog | - |
| 0306-16 | CONDITIONAL | no | cond 0306-16 | replaced_by_catalog | - |
| 0306-20 | CONDITIONAL | no | cond 0306-20 | replaced_by_catalog | - |
| 0306-24 | CONDITIONAL | no | cond 0306-24 | replaced_by_catalog | - |
| 2606-12-12-12-FG | CONDITIONAL | no | cond 2606-12-12-12-FG | partly | tap drill only, and only if Q-TRANSFER-TAPDRILL = no: Q-B-OTHER-TEE2 is answered yes by the catalog and the catalog legs / hex / bores equal OMi |
| 2609-08-08-08-FG | CONDITIONAL | no | cond 2609-08-08-08-FG | partly | tap drill only, and only if Q-TRANSFER-TAPDRILL = no: Q-B-OTHER-TEE2 is answered yes by the catalog and the catalog legs / hex / bores equal OMi |
| 2611-08-08-08-FG | CONDITIONAL | no | cond 2611-08-08-08-FG | partly | tap drill only, and only if Q-TRANSFER-TAPDRILL = no: Q-B-OTHER-TEE2 is answered yes by the catalog and the catalog legs / hex / bores equal OMi |
| 5404-L-04X3.000 | CONDITIONAL | no | cond 5404-L-04X3.000 | not_replaced | as 5404-L-04X2.000: no 5404-L in the catalog |
| 1503-08-08-FG | IN_REPO | yes | ref 1504-20-20-FG, 1504-32-32-FG | not_replaced | in repo (no download): closed loop for the angled-leg helix thread helper - geometry the catalog cannot give |
| 1503-12-08-FG | IN_REPO | yes | ref 1504-20-20-FG, 1504-32-32-FG | not_replaced | in repo (no download): closed loop for the angled-leg helix thread helper - geometry the catalog cannot give |
| 2404-L-08-08 | IN_REPO | yes | ref 2404-L-32-32 | not_replaced | in repo (no download): long-variant construction reference, hex length T20 - not printed |
| 2406-08-08 | IN_REPO | yes | ref 2406-08-08 | replaced_by_catalog | - |
| 2502-06-04-FG | IN_REPO | yes | ref 2502-32-32-FG | not_replaced | in repo (no download): forged 2502 shape reference - geometry |
| 2603-06-06-06-FG | IN_REPO | yes | ref 2603-02-02-02-FG | not_replaced | in repo (no download): forged 2603 tee construction reference - geometry |

Counts: not_replaced 18, partly 44, replaced_by_catalog 36 (of 98); items with F2a rows in required_by: not_replaced 12, partly 40, replaced_by_catalog 17.

## Paper check (gen_straight2.build_rows in memory, nothing written)

| config | status | body / hex length | generator comment |
|---|---|---|---|
| 1405-04-06 | BUILT  | 0.86 | BUILD-MISSING: part exists in OMi catalog but Air-Way s-page has no row; needs a second dimensional source |
| 1405-08-12 | BUILT  | 1.17 | BUILD-MISSING: part exists in OMi catalog but Air-Way s-page has no row; needs a second dimensional source |
| 2406-04-02 | BUILT  | 0.592 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-04-04 | BUILT  | 0.6 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-04-08 | BUILT  | 0.593 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-06-10 | BUILT  | 0.622 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-08-08 | BUILT  | 0.753 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-10-16 | BUILT  | 0.849 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 2406-12-04 | BUILT  | 0.95 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source / female port reaches 0.355 from the End A tip, inside the End A thread/groove zone (0.550); radial wall there min 0.035 at 0.550 from the tip (OK) |
| 2406-12-12 | BUILT  | 0.906 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5000-06-02 | BUILT  | 1.13 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5000-16-08 | BUILT  | 1.89 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5000-24-20 | BUILT  | 1.93 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5404-16-04 | BUILT  | 0.46 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5404-20-12 | BUILT  | 0.54 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5404-24-12 | BUILT  | 0.63 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5404-32-12 | BUILT  | 0.76 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |
| 5404-32-16 | BUILT  | 0.66 | BUILD-MISSING: part exists in OMi catalog but the Air-Way page has no row; needs a second dimensional source |

The 1405 / 5000 checks use the Air-Way per-size tap drills of Q-TRANSFER-TAPDRILL (both ends of the 1405-04-06 drill range, both -24 options 1.72 / 1.70 on 5000-24-20) only to show the rows would build; they are not proposed values.

## Catalog and OMi issues seen

- catalog: 0304-C-32 C HEX 2.880 (other -32 nut hexes print 2.875) - likely 2.88 padded
- catalog: 1700-32-24 A/F 2.622 (1700-32-32 2.625; not a print of a 64th) - possible misprint
- catalog: 2606-FG header prints 'BE SAE 37Deg' for the side-3 JIC thread (B3)
- catalog: 0304-C-48 row printed blank
- catalog: 1405-04-06 A2 DRILL printed as a range .32/.34 (several 1405 rows print ranges)
- catalog: 1405-08-12 L - L1 = 0.35 vs Brennan-measured -12 NPSM nut-face-to-stem-tip 0.33; 1405-04-06 0.21 vs 0.22 (-06)
- OMi: 2501-24-32-FG Items!X699 Side 2 ID 1.940 vs catalog 1.938; OMi 2501-32-32-FG / 5500-32-32-FG print 1.938
- OMi: 2706-LN-08-06 Items!L1091 2.400 / X1091 0.295 (and plain twin L1076 / X1076) vs catalog 2706-08-06 2.410 / 0.297
- OMi: 0304-C-32 Items!R16 2.875 vs catalog 2.880 (catalog more likely the odd one)

## Files

- `impact/F2a.json` - per row: config, old / new bucket + reason, catalog_hit (catalog, page, series, pn, table, match rule, printed values), cells (review_col, catalog_col, value as printed, value_in, pairing + reason, agrees_with_omi / omi_compare, agrees_with_airway / airway_compare), questions_answered (id, answer_from_catalog, evidence, level), questions_still_open, steps (pn, verdict, still_needed_for), paper_check, note; top level: summary, new_questions, differences, step_list_verdicts.
- `impact/build_F2a.py` (builds both files); `impact/_F2a_work/`: colmaps.py (pairings and reasons), write_md.py, dump_rows.py, matrix.py / pairdiff.py (Air-Way agreement), paper_check.py + harness.py (copied from Task C), render.py / render_heads.py + png/ (drawings looked at).
