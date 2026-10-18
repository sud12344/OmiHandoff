# F2b - what the Brennan catalog changes (Task C group F2, second half: 141 rows)

Written 2026-10-01T23:07:09 by `tools/_out/brennan_catalog_20261001/impact/build_F2b.py` (read-only on every input; full data in `F2b.json`). Rows = the 281 Task C F2 rows sorted by config, rows 141-281 (`5404-L-04X3.000` .. `6902-24-24-NWO-FG`).

Rules: a catalog value alone is ASSUMED (OMi + Brennan catalog = one source); rounding-only differences are not differences; Q-NEW-BRENNANCAT treated as yes, Q-BRENNAN-ONLY formally open; pairings: *certain* = catalog letter/drawing + data, *likely* = drawing/role without exact data agreement, *uncertain* = listed, never used for a bucket change. Conflicts are never voted - they are new questions below. Nothing was written to 04_DESIGN_TABLES / 03_SCRIPTS / 11_MASTERS / tools/generators.

## Headline

141 F2b rows: 111 have a catalog row (89 exact, 22 documented variants 5406-HHP->5406-HP / 6408-HHP->6408-H..-O); 27 rows change bucket: STEP->NOW 2 (5600 -20/-24 tees), STEP->DECIDE 12 (5405 x7, 5406-32-04, 5406-C x3, 5604-32 - only a female-port tap drill left, Q-TRANSFER-TAPDRILL), DECIDE->NOW 13 (5406-P x3, 5500-16-08, 6501-06-04/-32-32, 6502-10-08, 6504 x4, 6505-06-04/-16-12). The catalog answers Q-B-5500, Q-B-6501, Q-B-SWELB, Q-B-SWSTR, Q-B-OTHER-6504, Q-B-OTHER-6404D (D1), Q-B-OTHER-5501, Q-NEW-6408H-IDENT, Q-6900-IDENT and Q-NEW-BRENNANPN for 5406-HHP/-SHP from its own drawing letters; Q-PLACEHOLDER only partly (Brennan prints the 1.000s too; -32-12/-32-16 stay impossible). New conflicts inside the one Brennan source: 6405-32-16 D3, 6410-16-04 D, 6501-12-08 M5, 6505-12-08 D1, 6506-32-32 L17, 6504-32-32 (misprinted row), 6408-HHP-12/-16 L, 5404-N bores vs the Air-Way transfer. WORK rows stay WORK (code), 88 step-list items: not_replaced 27, partly 57, replaced_by_catalog 4.

## Buckets

| bucket | before | after |
|---|---|---|
| NOW | 3 | 18 |
| DECIDE | 44 | 43 |
| STEP | 25 | 11 |
| WORK | 69 | 69 |

Moves: DECIDE->DECIDE 31, DECIDE->NOW 13, NOW->NOW 3, STEP->DECIDE 12, STEP->NOW 2, STEP->STEP 11, WORK->WORK 69

### Rows that change bucket

| config | old -> new | catalog row | why |
|---|---|---|---|
| 5405-04-02 | STEP -> DECIDE | TFA p12 5405-04-02 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL supplies (no download needed if yes) |
| 5405-04-12 | STEP -> DECIDE | TFA p12 5405-04-12 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL supplies (no download needed if yes) |
| 5405-08-04 | STEP -> DECIDE | TFA p12 5405-08-04 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL supplies (no download needed if yes) |
| 5405-16-24 | STEP -> DECIDE | TFA p12 5405-16-24 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-24 supplies (no download needed if yes) |
| 5405-20-20 | STEP -> DECIDE | TFA p12 5405-20-20 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL supplies (no download needed if yes) |
| 5405-20-32 | STEP -> DECIDE | TFA p12 5405-20-32 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-32 supplies (no download needed if yes) |
| 5405-24-20 | STEP -> DECIDE | TFA p12 5405-24-20 | STEP -> DECIDE: the catalog gives L, hex and bore; the only open cell is the female-port tap drill, which Q-TRANSFER-TAPDRILL supplies (no download needed if yes) |
| 5406-32-04 | STEP -> DECIDE | TFA p13 5406-32-04 | STEP -> DECIDE: the catalog gives L2 and hex; the tap drill needs Q-TRANSFER-TAPDRILL (-04 0.43) - or accepting the catalog A1 DRILL 0.431 as the carried-through tap drill (same value at 2 decimals); no download needed either way |
| 5406-C-20 | STEP -> DECIDE | TFA p67 5406-C-20 | STEP -> DECIDE: the catalog gives L and hex; the tap drill needs Q-TRANSFER-TAPDRILL |
| 5406-C-24 | STEP -> DECIDE | TFA p67 5406-C-24 | STEP -> DECIDE: the catalog gives L and hex; the tap drill needs Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-24 |
| 5406-C-32 | STEP -> DECIDE | TFA p67 5406-C-32 | STEP -> DECIDE: the catalog gives L and hex; the tap drill needs Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-32 |
| 5406-P-02 | DECIDE -> NOW | TFA p67 5406-P-02 | DECIDE -> NOW: the catalog gives L2 and hex directly (ASSUMED); Q-NEW-AWALIAS becomes optional (only for VERIFIED) |
| 5406-P-04 | DECIDE -> NOW | TFA p67 5406-P-04 | DECIDE -> NOW: the catalog gives L2 and hex directly (ASSUMED); Q-NEW-AWALIAS becomes optional (only for VERIFIED) |
| 5406-P-06 | DECIDE -> NOW | TFA p67 5406-P-06 | DECIDE -> NOW: the catalog gives L2 and hex directly (ASSUMED); Q-NEW-AWALIAS becomes optional (only for VERIFIED) |
| 5500-16-08-FG | DECIDE -> NOW | TFA p30 5500-16-08-FG | DECIDE -> NOW: Q-B-5500 is answered by the catalog drawing; every cell = OMi = catalog |
| 5600-20-20-20-FG | STEP -> NOW | TFA p55 5600-20-20-20-FG | STEP -> NOW: all 7 missing cells are printed (SPEC 5600 + end libraries exist); ASSUMED (catalog = Brennan) |
| 5600-24-24-24-FG | STEP -> NOW | TFA p55 5600-24-24-24-FG | STEP -> NOW: all 7 missing cells are printed (SPEC 5600 + end libraries exist); ASSUMED (catalog = Brennan) |
| 5604-32-32-32-FG | STEP -> DECIDE | TFA p56 5604-32-32-32-FG | STEP -> DECIDE: legs/hex/bore printed; tap drills need Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-32 (or the STEP) |
| 6501-06-04-FG | DECIDE -> NOW | TFA p35 6501-06-04-FG | DECIDE -> NOW: Q-B-6501 answered by the catalog drawing; all 7 cells OMi = catalog |
| 6501-32-32-FG | DECIDE -> NOW | TFA p35 6501-32-32-FG | DECIDE -> NOW: Q-B-6501 answered by the catalog drawing; all 7 cells OMi = catalog |
| 6502-10-08-FG | DECIDE -> NOW | TFA p35 6502-10-08-FG | DECIDE -> NOW: Q-B-SWELB answered by the catalog drawing; all 7 cells OMi = catalog |
| 6504-04-06 | DECIDE -> NOW | TFA p17 6504-04-06 | DECIDE -> NOW: Q-B-OTHER-6504 answered by the drawing and L14 is printed, so no offset transfer is needed |
| 6504-06-04 | DECIDE -> NOW | TFA p17 6504-06-04 | DECIDE -> NOW: Q-B-OTHER-6504 answered by the drawing and L14 is printed, so no offset transfer is needed |
| 6504-08-10 | DECIDE -> NOW | TFA p17 6504-08-10 | DECIDE -> NOW: Q-B-OTHER-6504 answered by the drawing and L14 is printed, so no offset transfer is needed |
| 6504-12-16 | DECIDE -> NOW | TFA p17 6504-12-16 | DECIDE -> NOW: Q-B-OTHER-6504 answered by the drawing and L14 is printed, so no offset transfer is needed |
| 6505-06-04 | DECIDE -> NOW | TFA p18 6505-06-04 | DECIDE -> NOW: Q-B-SWSTR answered by the drawing; all cells OMi = catalog |
| 6505-16-12 | DECIDE -> NOW | none (series-level answer) | DECIDE -> NOW: its only gate Q-B-SWSTR is answered by the catalog drawing (series level); values from OMi |

## Questions the catalog answers (fully, partly, or makes unnecessary for a row)

| question | verdict | rows | answer (first row) / evidence |
|---|---|---|---|
| Q-6900-IDENT | YES | 1: 6900-32-32-O | Brennan titles 6900-O "MORB-FPS STRAIGHT" (TFA p18-19): male ORB B1 x female pipe swivel with an NPSM thread on A2 (drawing: swivel nut C HEX on the A2 end); not a female JIC union (evidence: TFA p18 heading + drawing (render clip_p18_6900draw.png), p19 table continuation) |
| Q-B-5500 | YES (settled by the catalog's own letters) | 1: 5500-16-08-FG | drawing p30 letters the A1 (first-dash) leg N1 and the A2 leg N; OMi M 1 = N1 (16/17) and L 1 = N (17/17), so M 1 = first-dash leg, L 1 = second-dash leg; on this row 1.970 / 1.780 both equal the catalog (evidence: TFA p30 5500-FG drawing + table; match/TFA_elbows.json mapping_final_comparison M099/M100) |
| Q-B-6501 | YES (settled by the catalog letters, not by the 1-row test) | 3: 6501-06-04-FG, 6501-12-08-FG, 6501-32-32-FG | drawing p35: N = pipe leg, M4 = to the swivel nose, M6 = to the nut face; OMi L 1 = N 14/14, M 2 = M6 12/14, M 1 = M4 (8/14 exact, otherwise +0.01) - the same reading as 6500 (Q-B-SWELB) (evidence: TFA p35 6501-FG drawing/table; match/TFA_elbows.json leg_columns_finding + mapping_final_comparison M127-M129; match/TFA_elbows_diffcheck.json idx 24-31) |
| Q-B-OTHER-5501 | YES (series level) | 2: 5501-24-24-FG, 5501-32-32-FG | drawing TFA p31 (5501-FG): N = axis crossing to the A1 tip, N1 = along the 45 deg leg to the A2 tip, Y FLATS = body flats; OMi M 1 = N, L 1 = N1, Hex Flat = Y on 8/8 rows; the datum (axis crossing) is the one the plain Air-Way 5501 rows use (near-match N->N4 6/7) (evidence: TFA p31; match/TFA_elbows.json mapping_final_comparison M104-M106 (8/8); alias_scores 5501) |
| Q-B-OTHER-6404D | D1 | 1: 6404-08-12 | the catalog letters settle it: OMi Side 1 ID 0.689 equals the catalog "A DRILL", and A is the male pipe end on the p15 drawing; Brennan prints no ORB-port drill at all (so M070 / D3 is not supported) (evidence: TFA p15 6404 drawing + row 6404-08-12; match/TFA_straights.json prior_mapping_check M069/M070) |
| Q-B-OTHER-6408HHP | PARTLY | 12: 6408-HHP-02-O, 6408-HHP-03-O, 6408-HHP-04-O, 6408-HHP-05-O, 6408-HHP-06-O, 6408-HHP-08-O ... | the drawing confirms OMi "Overall Length" = L (overall) and "Hex Flat" = C5 HEX (the socket across flats); OMi "Body Diameter" (round head) has no catalog column, so that part stays open (evidence: TFA p67 drawing; match/TFA_tees_caps.json column_maps 6408-H-O) |
| Q-B-OTHER-6504 | YES (series level, from the drawing) | 10: 6504-04-06, 6504-06-04, 6504-08-10, 6504-08-12, 6504-10-08, 6504-10-12 ... | TFA p17: L5 = male JIC tip to the swivel-nut face = SPEC 6504 L13; OMi Overall Length = L5 (9/15 exact + 3 rounding-only; real: 6504-10-10 +0.10, 6504-16-12 -0.02 and the misprinted -32 row); L = JIC tip to the stem nose (seat) = L14, which OMi leaves blank (evidence: TFA p17 6504 drawing (render F2b_work/png/clip_p17_6504draw.png); match/TFA_straights.json prior_mapping_check M026; gen_straight2 SPEC 6504 "L13 = male tip to the nut face, L14 = male tip to the seat") |
| Q-B-SWELB | YES (settled by the catalog letters) | 2: 6502-10-08-FG, 6502-16-12-FG | drawing p35: M2 = JIC leg, M = 45 deg leg to the swivel nose, M6 = to the nut face; OMi L 1 = M2 14/14, M 2 = M6 14/14, M 1 = M (6/14 exact, otherwise +0.01); this row: all three equal the catalog (evidence: TFA p35 6502-FG; match/TFA_elbows.json M134-M136; match/TFA_elbows_diffcheck.json idx 32-39) |
| Q-B-SWSTR | YES (series level, from the drawing) | 8: 6505-04-02, 6505-06-04, 6505-12-08, 6505-16-12, 6506-06-04, 6506-06-10 ... | TFA p18 6505: L5 = pipe tip to swivel-nut face = L15, L = pipe tip to stem nose (seat) = L16 (SPEC 6505 definitions); OMi Overall Length = L5 15/20, OMi L 1 = L 18/20: OMi's two lengths are the same two features Air-Way prints (Brennan's body length) (evidence: TFA p18 6505 drawing; match/TFA_straights.json prior_mapping_check M031/M032) |
| Q-CONFLICT-SWOFFSET | NOT ANSWERED | 4: 6504-08-12, 6504-10-12, 6504-12-10, 6504-16-20 | Brennan's own L5 - L varies by the same 0.01-0.02 per swivel size (-06 0.37/0.375/0.38, -10 0.46-0.507, -12 0.56/0.57/0.58 over 6504/6505/6506), so the catalog cannot pick between Air-Way's two values (evidence: TFA p17-18 6504/6505/6506 tables (L5 - L / L5 - L2)) |
| Q-CONFLICT-SWOFFSET | NOT NEEDED for this row | 3: 6504-04-06, 6504-06-04, 6504-08-10 | L14 is printed (L5 - L = 0.380) (evidence: TFA p17 row 6504-04-06) |
| Q-NEW-5404L-XLEN | SUPPORTING EVIDENCE ONLY (not an answer) | 2: 5404-L-04X3.000, 5404-L-04X4.000 | in Brennan's own Xn.nnn numbering of the 5404-N long nipples the X-number equals the printed L LGTH on 85 of 85 rows; 5404-L itself is not printed (evidence: TFA p11-12 table 5404-N (e.g. 5404-N-04X3.000 L 3.000)) |
| Q-NEW-6408H-IDENT | YES | 12: 6408-HHP-02-O, 6408-HHP-03-O, 6408-HHP-04-O, 6408-HHP-05-O, 6408-HHP-06-O, 6408-HHP-08-O ... | Brennan prints the family as 6408-H<dash>-O "MORB HOLLOW HEX PLUG" (TFA p67, 13 sizes incl. all 12 OMi sizes); OMi "MORB Hollow Hex Plug" values agree (socket hex 8/8, length 6/8); download 6408-H02-O (evidence: TFA p67 table 6408-H-O; match/TFA_tees_caps.json pn_match_rules series_alias + column_maps) |
| Q-NEW-AWALIAS | PARTLY (supports yes for the naming) | 1: 5404-N-08X2.500 | Brennan numbers the 1/2-14 x 2.500 in nipple "5404-N-08X2.500" (TFA p12): the same size/length as Air-Way "5404-N-8-8 X 2 1/2" (L 2.50 = 2.500); but the catalog drill 0.531 differs from Air-Way's bore 0.48, so the two makers' parts are not identical in the bore; the alias is still what gives COD@REF (Air-Way C 0.88) (evidence: TFA p12 row 5404-N-08X2.500; review row 5404-N-08-08-X21o2 (Air-Way s84)) |
| Q-NEW-AWALIAS | SUPPORTS YES and makes it non-gating | 3: 5406-P-02, 5406-P-04, 5406-P-06 | Brennan 5406-P-02 (TFA p67) prints L 0.562 / hex 0.438, Air-Way 5406-2P prints L2 0.56 / C2 0.44 (equal or rounding-only): the alias identity is supported, and the catalog gives the row its own values, so the row no longer needs the alias to build; the alias only adds Air-Way as a second (independent) source -> VERIFIED candidate (evidence: TFA p67 table 5406-P; review rows 5406-02P/-04P/-06P (Air-Way s88); alias_scores 5406P) |
| Q-NEW-BRENNANPN | PARTLY | 3: 5404-L-04X3.000, 5404-L-04X4.000, 5404-R-04-04-047 | 5404-L is not printed in Brennan's TFA catalog under any number (no 5404-L / 5404-R table, not in the p69-72 index); whether Brennan sells it at all stays open (OMi supplier drawing branch) (evidence: TFA p11 tables 5404 / 5404-N; p69 index "5404 MP-MP HEX NIPPLE PAGE 11", "5404-N MP-MP STRAIGHT NIPPLE LONG PAGE 11"; text search of all four catalog PDFs for "5404-L", "5404-R", "RESTRICT", "ORIFICE": no hit) |
| Q-NEW-BRENNANPN | YES for 5406-HHP | 10: 5406-HHP-01, 5406-HHP-02, 5406-HHP-04, 5406-HHP-06, 5406-HHP-08, 5406-HHP-12 ... | Brennan sells the hollow hex pipe plug as 5406-HP-<dash> (TFA p67 "HOLLOW HEX PIPE PLUG", all 10 OMi sizes 01/02/04/06/08/12/16/20/24/32 printed); download 5406-HP-01, not 5406-HHP-01 (evidence: TFA p67 table 5406-HP; match/TFA_tees_caps.json pn_match_rules series_alias (10 rows)) |
| Q-NEW-BRENNANPN | YES for 5406-SHP | 5: 5406-SHP-04, 5406-SHP-06, 5406-SHP-08, 5406-SHP-12, 5406-SHP-16 | Brennan prints the square head pipe plug under the same numbers 5406-SHP-02..-32 (TFA p67), incl. all 5 OMi sizes 04/06/08/12/16 (evidence: TFA p67 table 5406-SHP; match/TFA_tees_caps.json matches (exact)) |
| Q-PLACEHOLDER | PARTLY | 2: 6410-32-12-O, 6410-32-16-O | Brennan prints the same 1.000 (TFA p16), so it is not an OMi entry placeholder; but 1.000 is physically impossible here (Task C paper check: the -12 port runs through), so the printed value is itself wrong and the real length still needs the STEP (evidence: TFA p16 6410-O row 6410-32-12-O; match/TFA_straights.json placeholder_watch_1000_1320) |
| Q-PLACEHOLDER | REAL as far as the catalog goes | 3: 6410-16-04-O, 6410-20-06-O, 6410-20-08-O | Brennan prints 1.00 (TFA p16), so OMi's 1.000 is the catalog value, not an OMi entry placeholder; the part builds at 1.000 (Task C paper check). Only the STEP could show that Brennan's own print is wrong (evidence: TFA p16 row 6410-16-04-O; match/TFA_straights.json placeholder_watch_1000_1320 verdict) |
| Q-TRANSFER-5404N | PARTLY | 19: 5404-N-04X2.500, 5404-N-04X3.500, 5404-N-04X4.000, 5404-N-04X4.500, 5404-N-04X5.000, 5404-N-04X5.500 ... | the catalog gives this part's own length and bore (A1/A2 DRILL 0.281, the same at every length of the dash, which supports length-independence) but no bar diameter, so COD@REF still needs the transfer; the catalog drill DIFFERS from the Air-Way bore the transfer would use (0.281 vs 0.30) - the user picks, no vote (evidence: TFA p11 5404-N row 5404-N-04X2.500; alias_scores 5404N same_part A1 DRILL->D1@BORE 0/14) |
| Q-TRANSFER-NUTHEX | NOT NEEDED for this row | 6: 6606-04-04-04-FG, 6606-08-08-08-FG, 6606-16-16-16-FG, 6900-32-32-O, 6901-32-32-NWO-FG, 6902-24-24-NWO-FG | the catalog prints the part's own nut hex C HEX 0.563 (= the transfer value) (evidence: TFA p58 row 6606-04-04-04-FG) |
| Q-TRANSFER-SWOFFSET | NOT NEEDED for this row | 4: 6504-04-06, 6504-06-04, 6504-08-10, 6504-12-16 | the catalog prints L14 itself (L 1.210) (evidence: TFA p17 row 6504-04-06) |

## New questions (two prints of the one Brennan source disagree, or catalog vs the Air-Way transfer)

- **(new) Q-CAT-5404N-BORE** (19 rows: 5404-N-04X2.500, 5404-N-04X3.500, 5404-N-04X4.000, 5404-N-04X4.500, 5404-N-04X5.000 ...) - 5404-N long nipples: Brennan prints the through drill -04 0.281 / -06 0.406 / -08 0.531 on every length; Air-Way prints bores 0.30 / 0.39 / 0.48 (the Task C transfer). Which bore for the new 5404-N rows (catalog = the part's own value, ASSUMED; Air-Way = transfer from other lengths)? Recommendation: catalog drill (it is the part's own printed value; already flagged in 00_DOCS/NEXT_SESSION_PROMPT_2026-10-01.md item 3)
- **(new) Q-CAT-6405-32-16-D3** (1 rows: 6405-32-16-O) - 6405-32-16-O bore D3: OMi Side 1 ID 1.080 (Items!S1805, the same value OMi gives 6405-24-16-O) vs Brennan TFA p16 B DRILL 1.156. Which? Note 1.156 is wider than the -16 port tap drill 1.14 the row would get from Q-TRANSFER-TAPDRILL (bore-wider-than-port, as Q-BOREWIDE). Recommendation: OMi 1.080 for the build (fits inside the 1.14 tap drill); the catalog 1.156 only with the STEP
- **(new) Q-CAT-6408HHP-L** (2 rows: 6408-HHP-12-O, 6408-HHP-16-O) - 6408-HHP-12-O / -16-O overall length: OMi 0.780 vs Brennan TFA p67 0.77 / 0.775 (real under the strict rule; -16 may be a padded 0.78). Which? Recommendation: catalog value (0.77 at -12 matches the -14/-20/-24/-32 sizes; at -16 0.775 and 0.78 are the same to 2 places)
- **(new) Q-CAT-6410-16-04-D** (1 rows: 6410-16-04-O) - 6410-16-04-O through bore D: OMi Side 1 ID 0.368 (Items!S1862) vs Brennan TFA p16 B DRILL 0.389 (the catalog's value for every -04 port reducer: 6410-12-04-O, -20-04-O). Which? 0.389 is wider than the -04 port drill 0.38 (Q-TRANSFER-D3) - it would join Q-BOREWIDE. Recommendation: OMi 0.368 builds (inside the 0.38 port drill); catalog 0.389 needs Q-BOREWIDE
- **(new) Q-CAT-6501-12-08-M5** (1 rows: 6501-12-08-FG) - 6501-12-08-FG nut-face leg M5: OMi M 2 1.540 (Items!O1949) vs Brennan TFA p35 M6 1.612. Which? (The catalog's sister 6500-12-08-FG prints M6 1.550 = OMi's 1.55; 1.612 may be a catalog slip.) Recommendation: OMi 1.540 (consistent with the catalog's own 6500-12-08-FG); or the STEP
- **(new) Q-CAT-6504-32-32-L** (1 rows: 6504-32-32) - 6504-32-32 lengths: OMi L13 3.800; Brennan TFA p17 prints L 3.700 / L5 2.862 (inconsistent: seat beyond the nut face). Keep OMi 3.800 + Q-TRANSFER-SWOFFSET (L14 2.86), or get the STEP? Recommendation: STEP (no consistent printed pair exists)
- **(new) Q-CAT-6505-12-08-D1** (1 rows: 6505-12-08) - 6505-12-08 pipe-end bore D1: OMi Side 1 ID 0.719 (Items!S2021) vs Brennan TFA p18 A DRILL 0.609. The catalog prints 0.719 for the -12 NPTF drill on 6505-12-10/-12-12/-12-16 (0.609 is the -12 JIC drill) - likely a catalog slip. Which? Recommendation: OMi 0.719 (consistent with the catalog's own sister rows)
- **(new) Q-CAT-6506-32-32-L17** (1 rows: 6506-32-32) - 6506-32-32 L17: OMi Overall Length 3.200 (Items!L2050) vs Brennan TFA p18 L5 3.12. Which? Recommendation: user picks (L18 2.26 agrees; 3.20 - 2.26 = 0.94 = the Air-Way -32 offset, 3.12 - 2.26 = 0.86)

## Step-list items touching F2b (88)

Verdicts: not_replaced 27, partly 57, replaced_by_catalog 4

| step pn | verdict | rows | still needed for | download as |
|---|---|---|---|---|
| 5501-24-24-FG | replaced_by_catalog | 5501-24-24-FG | nothing for dimensions: the download was required only if Q-B-OTHER-5501 = no; the catalog answers it (yes) and prints the row; stays an optional cross-check |  |
| 5501-32-32-FG | replaced_by_catalog | 5501-32-32-FG | nothing for dimensions: the download was required only if Q-B-OTHER-5501 = no; the catalog answers it (yes); stays an optional cross-check |  |
| 5600-20-20-20-FG | replaced_by_catalog | 5600-20-20-20-FG | nothing: legs, hex and bores (all stated purposes) are printed on TFA p55 |  |
| 5600-24-24-24-FG | replaced_by_catalog | 5600-24-24-24-FG | nothing: legs, hex and bores (all stated purposes) are printed on TFA p55 |  |
| 5405-04-02 | partly | 5405-04-02 | tap drill of the female -02 port only (not printed); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 5405-04-12 | partly | 5405-04-12 | tap drill of the female -12 port only (not printed); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 5405-08-04 | partly | 5405-08-04 | tap drill of the female -04 port only (not printed); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 5405-16-24 | partly | 5405-16-24 | tap drill of the female -24 port only (not printed); nothing if Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-24 = yes |  |
| 5405-20-20 | partly | 5405-20-20 | tap drill of the female -20 port only (not printed); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 5405-20-32 | partly | 5405-20-32 | tap drill of the female -32 port only (not printed); nothing if Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-32 = yes |  |
| 5405-24-20 | partly | 5405-24-20 | tap drill of the female -20 port only (not printed); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 5406-32-04 | partly | 5406-32-04 | tap drill only, and only if neither Q-TRANSFER-TAPDRILL nor the catalog A1 DRILL 0.431 (as the carried-through tap drill) is accepted |  |
| 5406-40-32 | partly | 5406-40-32 | -40 male end length / thread geometry (or the ASME row), port depth and the -32 tap drill (2.19/2.20); the catalog gives L 2.370 and hex 3.000 only |  |
| 5406-C-20 | partly | 5406-C-20 | tap drill (not printed; Q-TRANSFER-TAPDRILL); also the port depth if the build refuses the thin end wall (catalog L 1.250 - P1 1.16 = 0.09) |  |
| 5406-C-24 | partly | 5406-C-24 | tap drill (not printed; Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-24); also the port depth if the build refuses the thin end wall (catalog L 1.540 - P1 1.16 = 0.38) |  |
| 5406-C-32 | partly | 5406-C-32 | tap drill (not printed; Q-TRANSFER-TAPDRILL + Q-CONFLICT-TAPDRILL-32); also the port depth if the build refuses the thin end wall (catalog L 1.370 - P1 1.18 = 0.19) |  |
| 5406-HHP-01 | partly | 5406-HHP-01 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-01 |
| 5406-HHP-02 | partly | 5406-HHP-02 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-02 |
| 5406-HHP-04 | partly | 5406-HHP-04 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-04 |
| 5406-HHP-06 | partly | 5406-HHP-06 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-06 |
| 5406-HHP-08 | partly | 5406-HHP-08 | pilot of the new 5406HHP shape: socket depth, socket bottom/chamfer, face geometry (catalog gives L + socket A/F only) | 5406-HP-08 |
| 5406-HHP-12 | partly | 5406-HHP-12 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-12 |
| 5406-HHP-16 | partly | 5406-HHP-16 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-16 |
| 5406-HHP-20 | partly | 5406-HHP-20 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-20 |
| 5406-HHP-24 | partly | 5406-HHP-24 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-24 |
| 5406-HHP-32 | partly | 5406-HHP-32 | socket depth (catalog gives L + socket A/F); could follow the pilot by rule only with a new transfer decision | 5406-HP-32 |
| 5406-SHP-04 | partly | 5406-SHP-04 | square head length and head/end geometry (catalog gives L + square A/F) |  |
| 5406-SHP-06 | partly | 5406-SHP-06 | square head length and head/end geometry (catalog gives L + square A/F) |  |
| 5406-SHP-08 | partly | 5406-SHP-08 | pilot of the new 5406SHP shape: square head length and head/end geometry (catalog gives L + square A/F) |  |
| 5406-SHP-12 | partly | 5406-SHP-12 | square head length and head/end geometry (catalog gives L + square A/F) |  |
| 5406-SHP-16 | partly | 5406-SHP-16 | square head length and head/end geometry (catalog gives L + square A/F) |  |
| 5505-20-20-FG | partly | 5505-20-20-FG | tap drills (or Q-TRANSFER-TAPDRILL) and the forged 45 deg body geometry of the new master; legs + flats come from the catalog |  |
| 5601-02-02-02-FG | partly | 5601-02-02-02-FG | branch tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats and run bores come from TFA p55 |  |
| 5601-20-20-20-FG | partly | 5601-20-20-20-FG | branch tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats and run bores come from TFA p55 |  |
| 5601-24-24-24-FG | partly | 5601-24-24-24-FG | branch tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats and run bores come from TFA p55 |  |
| 5603-02-02-02-FG | partly | 5603-02-02-02-FG | A2 tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats, bores come from TFA p55-56 |  |
| 5603-12-12-12-FG | partly | 5603-12-12-12-FG | A2 tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats, bores come from TFA p55-56 |  |
| 5603-24-24-24-FG | partly | 5603-24-24-24-FG | A2 tap drill (or Q-TRANSFER-TAPDRILL) and the forged-body geometry of the new master; legs, flats, bores come from TFA p55-56 |  |
| 5604-32-32-32-FG | partly | 5604-32-32-32-FG | the two -32 tap drills only (2.19 vs 2.20, Q-CONFLICT-TAPDRILL-32 - Task C wanted the STEP to settle it); legs, hex and bore are printed |  |
| 6405-02-02-O | partly | 6405-02-02-O | tap drill only (L31, hex, D3 are printed; the -02 ORB end comes from the 6408 row, not the STEP); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 6405-02-04-O | partly | 6405-02-04-O | tap drill only (L31, hex, D3 are printed; the -02 ORB end comes from the 6408 row, not the STEP); nothing if Q-TRANSFER-TAPDRILL = yes |  |
| 6408-H02-O | partly | 6408-HHP-02-O | socket depth and head dia (OMi gives none); overall length and socket A/F are printed | 6408-H02-O |
| 6408-H03-O | partly | 6408-HHP-03-O | socket depth and head dia (OMi gives none); overall length and socket A/F are printed | 6408-H03-O |
| 6408-H04-O | partly | 6408-HHP-04-O | socket depth and head dia (OMi gives none); overall length and socket A/F are printed | 6408-H04-O |
| 6408-H05-O | partly | 6408-HHP-05-O | socket depth; overall length and socket A/F are printed | 6408-H05-O |
| 6408-H06-O | partly | 6408-HHP-06-O | socket depth and head dia (OMi gives none); overall length and socket A/F are printed | 6408-H06-O |
| 6408-H10-O | partly | 6408-HHP-10-O | socket depth; overall length and socket A/F are printed | 6408-H10-O |
| 6408-H12-O | partly | 6408-HHP-12-O | socket depth; overall length and socket A/F are printed | 6408-H12-O |
| 6408-H16-O | partly | 6408-HHP-16-O | socket depth; overall length and socket A/F are printed | 6408-H16-O |
| 6408-H20-O | partly | 6408-HHP-20-O | socket depth; overall length and socket A/F are printed | 6408-H20-O |
| 6408-H24-O | partly | 6408-HHP-24-O | socket depth; overall length and socket A/F are printed | 6408-H24-O |
| 6408-H32-O | partly | 6408-HHP-32-O | socket depth; overall length and socket A/F are printed | 6408-H32-O |
| 6606-04-04-04-FG | partly | 6606-04-04-04-FG | forged-body geometry / pilot of the new triple-swivel tee; every body dimension (legs, hexes, bore) is printed on TFA p58 |  |
| 6606-08-08-08-FG | partly | 6606-08-08-08-FG | forged-body geometry / pilot of the new triple-swivel tee; every body dimension (legs, hexes, bore) is printed on TFA p58 |  |
| 6606-10-10-10-FG | partly | 6606-10-10-10-FG | forged-body geometry / pilot of the new triple-swivel tee; every body dimension (legs, hexes, bore) is printed on TFA p58 |  |
| 6606-16-16-16-FG | partly | 6606-16-16-16-FG | forged-body geometry / pilot of the new triple-swivel tee; every body dimension (legs, hexes, bore) is printed on TFA p58 |  |
| 6801-16-08-NWO-FG | partly | 6801-16-08-NWO-FG | I3 / ORB thread length / undercut (nwo.py) - the adjustable-end geometry; legs, hexes and bores are printed |  |
| 6801-24-32-NWO-FG | partly | 6801-24-32-NWO-FG | I3 / ORB thread length / undercut (nwo.py) - the adjustable-end geometry; legs, hexes and bores are printed |  |
| 6900-32-32-O | partly | 6900-32-32-O | body/stem geometry and the pilot of the new 6900 SPEC (closed loop); all body dimensions (L, L1, hexes, bores) are printed on TFA p19 |  |
| 6901-32-32-NWO-FG | partly | 6901-32-32-NWO-FG | forged-body geometry / pilot of the new 6901 master; body dimensions printed on TFA p46 (two NPSM-leg lengths have an uncertain Air-Way pairing) |  |
| 6902-24-24-NWO-FG | partly | 6902-24-24-NWO-FG | forged-body geometry / pilot of the new 6902 master; body dimensions printed on TFA p46 (two NPSM-leg lengths have an uncertain Air-Way pairing) |  |
| 1503-08-08-FG | not_replaced | 5501-24-24-FG, 5501-32-32-FG, 5503-04-02-FG, 5503-06-04-FG ... | in repo already: construction reference / closed loop for the angled-leg helix thread helper (geometry) |  |
| 1503-12-08-FG | not_replaced | 5501-24-24-FG, 5501-32-32-FG, 5503-04-02-FG, 5503-06-04-FG ... | in repo already: construction reference / closed loop for the angled-leg helix thread helper (geometry) |  |
| 5404-L-04X3.000 | not_replaced | 5404-L-04X3.000 | part not in the catalog: every body value (length, hex, bore, hex zone) still needs the STEP or a supplier drawing |  |
| 5404-L-04X4.000 | not_replaced | 5404-L-04X4.000 | part not in the catalog: every body value (length, hex, bore, hex zone) still needs the STEP or a supplier drawing |  |
| 5404-R-04-04-047 | not_replaced | 5404-R-04-04-047 | part not in the catalog: every body value (length, hex, bore, orifice dia/length/position) still needs the STEP or a supplier drawing |  |
| 5503-04-02-FG | not_replaced | 5503-04-02-FG | part not in the catalog: every body value + forged-body geometry |  |
| 5503-06-04-FG | not_replaced | 5503-06-04-FG | part not in the catalog: every body value + forged-body geometry |  |
| 5503-08-06-FG | not_replaced | 5503-08-06-FG | part not in the catalog: every body value + forged-body geometry |  |
| 5503-12-08-FG | not_replaced | 5503-12-08-FG | part not in the catalog: every body value + forged-body geometry |  |
| 5503-16-12-FG | not_replaced | 5503-16-12-FG | part not in the catalog: every body value + forged-body geometry |  |
| 5652-32-32-32-32-FG | not_replaced | 5652-32-32-32-32-FG | part not in the catalog: every body value + forged-body geometry |  |
| 6408-H08-O | not_replaced | 6408-HHP-02-O, 6408-HHP-03-O, 6408-HHP-04-O, 6408-HHP-05-O ... | in repo already: pilot geometry of the hollow hex plug (head, socket depth, O-ring) |  |
| 6410-04-02-O | not_replaced | 6410-04-02-O | the female -02 ORB port geometry (ports.py) and its drill D3 - geometry the catalog does not print |  |
| 6410-32-12-O | not_replaced | 6410-32-12-O | real overall length L33 (the catalog repeats the impossible 1.000) and the port drill D3 / bore vs port |  |
| 6410-32-16-O | not_replaced | 6410-32-16-O | real overall length L33 (the catalog repeats the impossible 1.000) and the port drill D3 / bore vs port |  |
| 6500-04-02-FG | not_replaced | 6500-04-02-FG | part not in the catalog: legs, body hex, nut hex, bores and the -02 swivel end |  |
| 6500-20-16-FG | not_replaced | 6500-20-16-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6500-24-20-FG | not_replaced | 6500-24-20-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6500-32-24-FG | not_replaced | 6500-32-24-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6501-16-12-FG | not_replaced | 6501-16-12-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6502-04-02-FG | not_replaced | 6502-04-02-FG | part not in the catalog: legs, body hex, nut hex, bores and the -02 swivel end |  |
| 6502-06-04-FG | not_replaced | 6502-06-04-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6502-12-10-FG | not_replaced | 6502-12-10-FG | part not in the catalog: legs, body hex, nut hex, bores |  |
| 6502-12-12-FG | not_replaced | 6502-16-12-FG | in repo already: neck-trim geometry evidence for the gen_tee work |  |
| 6505-04-02 | not_replaced | 6505-04-02 | the -02 JIC swivel end (nut, nose, seat) for SWIV_MEAS - geometry; part not in the catalog |  |
| 6802-04-02-NWO-FG | not_replaced | 6802-04-02-NWO-FG | part not in the catalog |  |
| 6806-12-08-NWO-FG | not_replaced | 6806-12-08-NWO-FG | part not in the catalog: every body value + forged-body geometry |  |

## Catalog issues found

- TFA p12 5404-N-06X3.500 / -06X7.000 / -12X8.000 (rows appended after 5404-N-24X6.000): the A1/A2 DRILL cells print the length in inch and mm (3.500 / 88.90, 7.000 / 165.10, 8.000 / 190.50) - no drill printed; the parse keeps them as printed (catalog_verified.json TFA-p012-t01)
- 5406-C pipe caps: Brennan caps (TFA p66-67) are 0.11-0.36 shorter than the Air-Way caps of the same size already built in 5406C (-02 0.563 vs 0.69 ... -16 1.250 vs 1.61) and 3 hexes differ (-06 0.812 vs 0.88, -08 1.000 vs 1.13, -12 1.188 vs 1.25): the new -20/-24/-32 rows would be Brennan bodies next to Air-Way bodies in one master
- TFA p16 6410-32-12-O / -32-16-O print L 1.000, impossible with a -12 / -16 female ORB port in a 2-1/2 in male body (the port depth + drill point > L): catalog value wrong or a placeholder in Brennan's own table
- TFA p35 6501-12-08-FG M6 1.612: the same -08 swivel on the -12 body prints M6 1.550 on 6500-12-08-FG; OMi has 1.540 - likely a catalog slip
- TFA p17 6504-32-32 prints L 3.700 > L5 2.862 (match/TFA_straights.json swivel_catalog_anomalies) - columns swapped or misprinted; OMi 3.800; Task C derived L14 2.86 (3.80 - Air-Way 0.94) happens to equal the catalog L5
- TFA p18 6505-12-08 A DRILL 0.609 departs from the catalog's own 0.719 for the -12 NPTF drill (6505-12-10/-12-12/-12-16); OMi 0.719

## OMi issues found

- 6405-32-16-O Side 1 ID 1.080 (Items!S1805) differs from Brennan B DRILL 1.156 (TFA p16) and repeats OMi's 6405-24-16-O value - possible copy-down
- 6410-16-04-O Side 1 ID 0.368 (Items!S1862) differs from Brennan B DRILL 0.389 (TFA p16; the catalog prints 0.389 for every -04 port reducer)

## Agreement checks

- OMi vs catalog: 149 cells compared, 142 equal / rounding-only, 7 real differences (6405-32-16-O D3@BORE, 6408-HHP-12-O L@DRIVE, 6408-HHP-16-O L@DRIVE, 6410-16-04-O D@BORE, 6501-12-08-FG M5@DRIVE, 6505-12-08 D1@BORE, 6506-32-32 L17@DRIVE) - each is a new question above.
- Air-Way (Task C transfer / alias / derived fills) vs catalog: 44 cells compared, 8 agree (5406-P alias rows, 5404-N-08X2.500 length, 6504-12-16 derived L14); the 36 differences are all 5404-N bores (catalog drill -04 0.281 / -06 0.406 / -08 0.531 vs Air-Way 0.30 / 0.39 / 0.48).
- Cells listed: 744; with a usable catalog value: 432; pairing uncertain: 7 (6901/6902 NPSM-leg lengths, 6901 body flats, 5404-N-06X3.500 misprinted drills).

## All rows

| config | old | new | catalog row | cells given by the catalog | still open |
|---|---|---|---|---|---|
| 5404-L-04X3.000 | WORK | WORK | - | - | Q-NEWMASTER-5404L, Q-BRENNAN-ONLY, Q-NEW-BRENNANPN, Q-NEW-5404L-XLEN, Q-TRANSFER-5404L-X3 |
| 5404-L-04X4.000 | WORK | WORK | - | - | Q-NEWMASTER-5404L, Q-BRENNAN-ONLY, Q-NEW-BRENNANPN, Q-NEW-5404L-XLEN |
| 5404-N-04X2.500 | DECIDE | DECIDE | p11 5404-N-04X2.500 | L=2.500, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X3.500 | DECIDE | DECIDE | p11 5404-N-04X3.500 | L=3.500, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X4.000 | DECIDE | DECIDE | p11 5404-N-04X4.000 | L=4.000, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X4.500 | DECIDE | DECIDE | p11 5404-N-04X4.500 | L=4.500, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X5.000 | DECIDE | DECIDE | p11 5404-N-04X5.000 | L=5.000, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X5.500 | DECIDE | DECIDE | p11 5404-N-04X5.500 | L=5.500, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-04X6.000 | DECIDE | DECIDE | p11 5404-N-04X6.000 | L=6.000, D1=0.281, D2=0.281 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X2.000 | WORK | WORK | p11 5404-N-06X2.000 | L=2.000, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X2.500 | WORK | WORK | p11 5404-N-06X2.500 | L=2.500, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X3.000 | WORK | WORK | p11 5404-N-06X3.000 | L=3.000, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X3.500 | WORK | WORK | p12 5404-N-06X3.500 | L=3.500 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X4.000 | WORK | WORK | p11 5404-N-06X4.000 | L=4.000, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X4.500 | WORK | WORK | - | - | Q-TRANSFER-5404N, Q-NEW-5404N-NAME |
| 5404-N-06X5.000 | WORK | WORK | p11 5404-N-06X5.000 | L=5.000, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-06X6.000 | WORK | WORK | p11 5404-N-06X6.000 | L=6.000, D1=0.406, D2=0.406 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-08X2.500 | DECIDE | DECIDE | p12 5404-N-08X2.500 | L=2.500, D1=0.531, D2=0.531 | Q-NEW-AWALIAS, (new) Q-CAT-5404N-BORE |
| 5404-N-08X3.500 | DECIDE | DECIDE | p12 5404-N-08X3.500 | L=3.500, D1=0.531, D2=0.531 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-08X4.500 | DECIDE | DECIDE | p12 5404-N-08X4.500 | L=4.500, D1=0.531, D2=0.531 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-08X5.000 | DECIDE | DECIDE | p12 5404-N-08X5.000 | L=5.000, D1=0.531, D2=0.531 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-N-08X5.500 | DECIDE | DECIDE | - | - | Q-TRANSFER-5404N, Q-NEW-5404N-NAME |
| 5404-N-08X6.000 | DECIDE | DECIDE | p12 5404-N-08X6.000 | L=6.000, D1=0.531, D2=0.531 | Q-TRANSFER-5404N, Q-NEW-5404N-NAME, (new) Q-CAT-5404N-BORE |
| 5404-R-04-04-047 | WORK | WORK | - | - | Q-NEWMASTER-5404R, Q-BRENNAN-ONLY, Q-TRANSFER-5404R-BODY, Q-NEW-BRENNANPN |
| 5405-04-02 | STEP | DECIDE | p12 5405-04-02 | L=1.220, CHEX=0.625, D=0.281 | Q-TRANSFER-TAPDRILL |
| 5405-04-12 | STEP | DECIDE | p12 5405-04-12 | L=1.74, CHEX=1.375, D=0.281 | Q-TRANSFER-TAPDRILL |
| 5405-08-04 | STEP | DECIDE | p12 5405-08-04 | L=1.640, CHEX=0.875, D=0.531 | Q-TRANSFER-TAPDRILL |
| 5405-16-24 | STEP | DECIDE | p12 5405-16-24 | L=2.460, CHEX=2.375, D=0.938 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24 |
| 5405-20-20 | STEP | DECIDE | p12 5405-20-20 | L=2.49, CHEX=2.000, D=1.250 | Q-TRANSFER-TAPDRILL |
| 5405-20-32 | STEP | DECIDE | p12 5405-20-32 | L=2.600, CHEX=2.875, D=1.250 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-32 |
| 5405-24-20 | STEP | DECIDE | p12 5405-24-20 | L=2.540, CHEX=2.000, D=1.500 | Q-TRANSFER-TAPDRILL |
| 5406-32-04 | STEP | DECIDE | p13 5406-32-04 | L2=1.750, C2HEX=2.500, TAPDRILL=0.431? | Q-TRANSFER-TAPDRILL |
| 5406-40-32 | WORK | WORK | p13 5406-40-32 | L2=2.370, C2HEX=3.000, TAPDRILL=2.172? | Q-BRENNAN-ONLY, Q-NEW-ASME40, Q-CONFLICT-TAPDRILL-32 |
| 5406-C-20 | STEP | DECIDE | p67 5406-C-20 | L=1.250, C1HEX=2.000 | Q-TRANSFER-TAPDRILL |
| 5406-C-24 | STEP | DECIDE | p67 5406-C-24 | L=1.540, C1HEX=2.375 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24 |
| 5406-C-32 | STEP | DECIDE | p67 5406-C-32 | L=1.370, C1HEX=2.875 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-32 |
| 5406-HHP-01 | WORK | WORK | p67 5406-HP-01 | L2=0.300, (no column yet) so=0.156 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-NEW-NPT01 |
| 5406-HHP-02 | WORK | WORK | p67 5406-HP-02 | L2=0.30, (no column yet) so=0.188 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-04 | WORK | WORK | p67 5406-HP-04 | L2=0.46, (no column yet) so=0.250 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-06 | WORK | WORK | p67 5406-HP-06 | L2=0.46, (no column yet) so=0.312 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-08 | WORK | WORK | p67 5406-HP-08 | L2=0.610, (no column yet) so=0.375 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-12 | WORK | WORK | p67 5406-HP-12 | L2=0.620, (no column yet) so=0.562 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-16 | WORK | WORK | p67 5406-HP-16 | L2=0.79, (no column yet) so=0.625 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-20 | WORK | WORK | p67 5406-HP-20 | L2=0.770, (no column yet) so=0.750 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-24 | WORK | WORK | p67 5406-HP-24 | L2=0.83, (no column yet) so=1.00 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-HHP-32 | WORK | WORK | p67 5406-HP-32 | L2=0.87, (no column yet) so=0.75 | Q-NEWMASTER-5406HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-P-02 | DECIDE | NOW | p67 5406-P-02 | L2=0.562, C2HEX=0.438, (no column) hex he=0.170 | - |
| 5406-P-04 | DECIDE | NOW | p67 5406-P-04 | L2=0.750, C2HEX=0.562, (no column) hex he=0.170 | - |
| 5406-P-06 | DECIDE | NOW | p67 5406-P-06 | L2=0.780, C2HEX=0.688, (no column) hex he=0.22 | - |
| 5406-SHP-04 | WORK | WORK | p67 5406-SHP-04 | L2=0.750, (no column yet) sq=0.375 | Q-NEWMASTER-5406SHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-SHP-06 | WORK | WORK | p67 5406-SHP-06 | L2=0.780, (no column yet) sq=0.437 | Q-NEWMASTER-5406SHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-SHP-08 | WORK | WORK | p67 5406-SHP-08 | L2=1.020, (no column yet) sq=0.563 | Q-NEWMASTER-5406SHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-SHP-12 | WORK | WORK | p67 5406-SHP-12 | L2=1.100, (no column yet) sq=0.625 | Q-NEWMASTER-5406SHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5406-SHP-16 | WORK | WORK | p67 5406-SHP-16 | L2=1.300, (no column yet) sq=0.812 | Q-NEWMASTER-5406SHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 5500-16-08-FG | DECIDE | NOW | p30 5500-16-08-FG | N1=1.970, N2=1.780, Y=1.312, D1=0.938, D2=0.531 | - |
| 5501-24-24-FG | WORK | WORK | p31 5501-24-24-FG | N4=1.770?, N6=1.770?, Y=1.875?, D1=1.500, D2=1.500 | Q-NEWMASTER-5501, Q-NEW-ANGLEDHELIX |
| 5501-32-32-FG | WORK | WORK | - | - | Q-NEWMASTER-5501, Q-NEW-ANGLEDHELIX |
| 5503-04-02-FG | WORK | WORK | - | - | Q-NEWMASTER-5503, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX |
| 5503-06-04-FG | WORK | WORK | - | - | Q-NEWMASTER-5503, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX |
| 5503-08-06-FG | WORK | WORK | - | - | Q-NEWMASTER-5503, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX |
| 5503-12-08-FG | WORK | WORK | - | - | Q-NEWMASTER-5503, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX |
| 5503-16-12-FG | WORK | WORK | - | - | Q-NEWMASTER-5503, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX |
| 5505-20-20-FG | WORK | WORK | p33 5505-20-20-FG | N2_1=1.44?, N2_2=1.44?, W=1.875? | Q-NEWMASTER-5505, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL, Q-NEW-ANGLEDHELIX, Q-NEW-ANGLEDFEMALE |
| 5600-20-20-20-FG | STEP | NOW | p55 5600-20-20-20-FG | N1=2.380, N2=2.380, N3=2.380, Y=1.625, D1=1.250, D2=1.250, D3=1.250 | - |
| 5600-24-24-24-FG | STEP | NOW | p55 5600-24-24-24-FG | N1=2.640, N2=2.640, N3=2.640, Y=1.875, D1=1.500, D2=1.500, D3=1.500 | - |
| 5601-02-02-02-FG | WORK | WORK | p55 5601-02-02-02-FG | N_1=0.780?, N2=0.780?, N1=0.660, W=0.562?, D1=0.188, D2=0.188 | Q-NEWMASTER-5601, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL |
| 5601-20-20-20-FG | WORK | WORK | p55 5601-20-20-20-FG | N_1=2.38?, N2=2.38?, N1=1.70, W=1.875?, D1=1.250, D2=1.250 | Q-NEWMASTER-5601, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL |
| 5601-24-24-24-FG | WORK | WORK | p55 5601-24-24-24-FG | N_1=2.64?, N2=2.64?, N1=2.08, W=2.562?, D1=1.500, D2=1.500 | Q-NEWMASTER-5601, Q-BRENNAN-ONLY |
| 5603-02-02-02-FG | WORK | WORK | p55 5603-02-02-02-FG | N1=0.780?, N1_2=0.660, N3=0.780?, W=0.562?, D1_1=0.188, D1_3=0.188 | Q-NEWMASTER-5603, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL |
| 5603-12-12-12-FG | WORK | WORK | p56 5603-12-12-12-FG | N1=1.590?, N1_2=1.360, N3=1.590?, W=1.312?, D1_1=0.719, D1_3=0.719 | Q-NEWMASTER-5603, Q-BRENNAN-ONLY, Q-TRANSFER-TAPDRILL |
| 5603-24-24-24-FG | WORK | WORK | p56 5603-24-24-24-FG | N1=2.64?, N1_2=2.08, N3=2.64?, W=2.562?, D1_1=1.500, D1_3=1.500 | Q-NEWMASTER-5603, Q-BRENNAN-ONLY |
| 5604-32-32-32-FG | STEP | DECIDE | p56 5604-32-32-32-FG | N1_1=2.390, N1_2=2.390, N=3.000, W=2.812, D=1.938 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-32 |
| 5652-32-32-32-32-FG | WORK | WORK | - | - | Q-NEWMASTER-5652, Q-BRENNAN-ONLY |
| 6401-16-20-O | NOW | NOW | p15 6401-16-20-O | L29=2.290, HEXB=1.688, D3=0.844, D4=1.250 | - |
| 6401-20-16-O | NOW | NOW | p15 6401-20-16-O | L29=2.150, HEXB=1.875, D3=1.078, D4=0.938 | - |
| 6401-24-20-O | NOW | NOW | p15 6401-24-20-O | L29=2.25, HEXB=2.125, D3=1.312, D4=1.250 | - |
| 6404-08-12 | DECIDE | DECIDE | p15 6404-08-12 | L32=1.690, C1HEX=1.125, D1=0.689 | Q-TRANSFER-D3, Q-CONFLICT-6404-D3-08, Q-BOREWIDE |
| 6405-02-02-O | WORK | WORK | p15 6405-02-02-O | L31=0.950, HEXB=0.562, D3=0.062 | Q-TRANSFER-TAPDRILL |
| 6405-02-04-O | WORK | WORK | p15 6405-02-04-O | L31=1.240, HEXB=0.750, D3=0.062 | Q-TRANSFER-TAPDRILL |
| 6405-16-24-O | DECIDE | DECIDE | p16 6405-16-24-O | L31=2.280, HEXB=2.375, D3=0.844 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24 |
| 6405-32-16-O | DECIDE | DECIDE | p16 6405-32-16-O | L31=1.430, HEXB=2.750, D3=1.156 | Q-TRANSFER-TAPDRILL, (new) Q-CAT-6405-32-16-D3 |
| 6408-HHP-02-O | WORK | WORK | p67 6408-H02-O | L=0.400, (no column yet) so=0.125 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 6408-HHP-03-O | WORK | WORK | p67 6408-H03-O | L=0.40, (no column yet) so=0.125 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 6408-HHP-04-O | WORK | WORK | p67 6408-H04-O | L=0.47, (no column yet) so=0.188 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 6408-HHP-05-O | WORK | WORK | p67 6408-H05-O | L=0.47, (no column yet) so=0.188 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP |
| 6408-HHP-06-O | WORK | WORK | p67 6408-H06-O | L=0.50, (no column yet) so=0.250 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 6408-HHP-08-O | WORK | WORK | p67 6408-H08-O | L=0.58, (no column yet) so=0.313 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5 |
| 6408-HHP-10-O | WORK | WORK | p67 6408-H10-O | L=0.65, (no column yet) so=0.375 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP |
| 6408-HHP-12-O | WORK | WORK | p67 6408-H12-O | L=0.77, (no column yet) so=0.562 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP, (new) Q-CAT-6408HHP-L |
| 6408-HHP-16-O | WORK | WORK | p67 6408-H16-O | L=0.775, (no column yet) so=0.625 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP, (new) Q-CAT-6408HHP-L |
| 6408-HHP-20-O | WORK | WORK | p67 6408-H20-O | L=0.77, (no column yet) so=0.750 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP |
| 6408-HHP-24-O | WORK | WORK | p67 6408-H24-O | L=0.770, (no column yet) so=0.750 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP |
| 6408-HHP-32-O | WORK | WORK | p67 6408-H32-O | L=0.77, (no column yet) so=0.750 | Q-NEWMASTER-6408HHP, Q-BRENNAN-ONLY, Q-SOP5, Q-B-OTHER-6408HHP |
| 6410-04-02-O | WORK | WORK | p16 6410-04-02-O | L33=1.100, C1HEX=0.562, D=0.172 | Q-BRENNAN-ONLY |
| 6410-16-04-O | DECIDE | DECIDE | p16 6410-16-04-O | L33=1.00, C1HEX=1.500, D=0.389 | Q-TRANSFER-D3, (new) Q-CAT-6410-16-04-D |
| 6410-20-06-O | DECIDE | DECIDE | p16 6410-20-06-O | L33=1.000, C1HEX=1.875, D=0.509 | Q-TRANSFER-D3, Q-BOREWIDE |
| 6410-20-08-O | DECIDE | DECIDE | p16 6410-20-08-O | L33=1.000, C1HEX=1.875, D=0.689 | Q-TRANSFER-D3, Q-BOREWIDE |
| 6410-32-12-O | STEP | STEP | p16 6410-32-12-O | L33=1.000, C1HEX=2.750, D=0.980 | Q-PLACEHOLDER, Q-TRANSFER-D3, Q-BOREWIDE, Q-BRENNAN-ONLY |
| 6410-32-16-O | STEP | STEP | p16 6410-32-16-O | L33=1.000, C1HEX=2.750, D=1.231 | Q-PLACEHOLDER, Q-TRANSFER-D3, Q-BOREWIDE, Q-BRENNAN-ONLY |
| 6500-04-02-FG | WORK | WORK | - | - | Q-BRENNAN-ONLY |
| 6500-20-16-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6500-24-20-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6500-32-24-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6501-06-04-FG | DECIDE | NOW | p35 6501-06-04-FG | N=1.220, M5=1.170, M10=0.830?, C3HEX=0.562, Y=0.750, D1=0.406, D=0.172 | - |
| 6501-12-08-FG | DECIDE | DECIDE | p35 6501-12-08-FG | N=1.590, M5=1.612, M10=1.120?, C3HEX=0.875, Y=1.062, D1=0.719, D=0.391 | (new) Q-CAT-6501-12-08-M5 |
| 6501-16-12-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6501-32-32-FG | DECIDE | NOW | p35 6501-32-32-FG | N=3.000, M5=3.380, M10=2.440?, C3HEX=2.875, Y=2.500, D1=1.938, D=1.781 | - |
| 6502-04-02-FG | WORK | WORK | - | - | Q-BRENNAN-ONLY |
| 6502-06-04-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6502-10-08-FG | DECIDE | NOW | p35 6502-10-08-FG | M2=1.11, M6=1.33, M14=0.91?, C3HEX=0.875, Y=0.875, D1=0.484, D2=0.391 | - |
| 6502-12-10-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6502-16-12-FG | WORK | WORK | p35 6502-16-12-FG | M2=1.47, M6=1.70, M14=1.14?, C3HEX=1.250, Y=1.312, D1=0.844, D2=0.609 | - |
| 6504-04-06 | DECIDE | NOW | p17 6504-04-06 | L13=1.590, L14=1.210?, CHEX=0.562, C3HEX=0.688, D1=0.172, D2=0.297 | - |
| 6504-06-04 | DECIDE | NOW | p17 6504-06-04 | L13=1.504, L14=1.160?, CHEX=0.625, C3HEX=0.563, D1=0.297, D2=0.172 | - |
| 6504-08-10 | DECIDE | NOW | p17 6504-08-10 | L13=2.070, L14=1.570?, CHEX=0.938, C3HEX=1.000, D1=0.391, D2=0.484 | - |
| 6504-08-12 | DECIDE | DECIDE | - | - | Q-TRANSFER-SWOFFSET, Q-CONFLICT-SWOFFSET |
| 6504-10-08 | DECIDE | DECIDE | - | - | Q-TRANSFER-SWOFFSET |
| 6504-10-12 | DECIDE | DECIDE | - | - | Q-TRANSFER-SWOFFSET, Q-CONFLICT-SWOFFSET |
| 6504-12-10 | DECIDE | DECIDE | - | - | Q-TRANSFER-SWOFFSET, Q-CONFLICT-SWOFFSET |
| 6504-12-16 | DECIDE | NOW | p17 6504-12-16 | L13=2.450, L14=1.860?, CHEX=1.375, C3HEX=1.500, D1=0.609, D2=0.844 | - |
| 6504-16-20 | DECIDE | DECIDE | - | - | Q-TRANSFER-SWOFFSET, Q-CONFLICT-SWOFFSET |
| 6504-32-32 | DECIDE | DECIDE | p17 6504-32-32 | CHEX=2.625, C3HEX=2.875, D1=1.781, D2=1.781 | Q-TRANSFER-SWOFFSET, (new) Q-CAT-6504-32-32-L |
| 6505-04-02 | WORK | WORK | - | - | - |
| 6505-06-04 | DECIDE | NOW | p18 6505-06-04 | L15=1.570, L16=1.230, CHEX=0.750, C3HEX=0.563, D1=0.406, D=0.172 | - |
| 6505-12-08 | DECIDE | DECIDE | p18 6505-12-08 | L15=2.09, L16=1.67, CHEX=1.125, C3HEX=0.875, D1=0.609, D=0.391 | (new) Q-CAT-6505-12-08-D1 |
| 6505-16-12 | DECIDE | NOW | - | - | - |
| 6506-06-04 | DECIDE | DECIDE | p18 6506-06-04 | L17=1.59?, L18=1.24, C1HEX=0.875, C3HEX=0.563, D=0.172 | Q-TRANSFER-TAPDRILL |
| 6506-06-10 | DECIDE | DECIDE | p18 6506-06-10 | L17=1.900?, L18=1.400, C1HEX=0.938, C3HEX=1.000, D=0.484 | Q-TRANSFER-TAPDRILL |
| 6506-12-08 | DECIDE | DECIDE | - | - | Q-TRANSFER-TAPDRILL |
| 6506-32-32 | DECIDE | DECIDE | p18 6506-32-32 | L17=3.12?, L18=2.26, C1HEX=2.875, C3HEX=2.875, D=1.781 | Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-32, (new) Q-CAT-6506-32-32-L17 |
| 6606-04-04-04-FG | WORK | WORK | p58 6606-04-04-04-FG | M5_1=1.00, M10_1=0.65?, C3_1HEX=0.563, M5_2=1.00, M10_2=0.65?, C3_2HEX=0.563, M5_3=1.00, M10_3=0.65?, C3_3HEX=0.563, Y=0.438?, D1=0.172 | Q-NEWMASTER-6606, Q-BRENNAN-ONLY, Q-NEW-PERLEGSW |
| 6606-08-08-08-FG | WORK | WORK | p58 6606-08-08-08-FG | M5_1=1.380, M10_1=0.950?, C3_1HEX=0.875, M5_2=1.380, M10_2=0.950?, C3_2HEX=0.875, M5_3=1.380, M10_3=0.950?, C3_3HEX=0.875, Y=0.750?, D1=0.391 | Q-NEWMASTER-6606, Q-BRENNAN-ONLY, Q-NEW-PERLEGSW |
| 6606-10-10-10-FG | WORK | WORK | p58 6606-10-10-10-FG | M5_1=1.620, M10_1=1.120?, C3_1HEX=1.000, M5_2=1.620, M10_2=1.120?, C3_2HEX=1.000, M5_3=1.620, M10_3=1.120?, C3_3HEX=1.000, Y=0.875?, D1=0.484 | Q-NEWMASTER-6606, Q-BRENNAN-ONLY, Q-NEW-PERLEGSW |
| 6606-16-16-16-FG | WORK | WORK | p58 6606-16-16-16-FG | M5_1=2.00, M10_1=1.40?, C3_1HEX=1.500, M5_2=2.00, M10_2=1.40?, C3_2HEX=1.500, M5_3=2.00, M10_3=1.40?, C3_3HEX=1.500, Y=1.312?, D1=0.844 | Q-NEWMASTER-6606, Q-BRENNAN-ONLY, Q-NEW-PERLEGSW |
| 6801-16-08-NWO-FG | STEP | STEP | p41 6801-16-08-NWO-FG | LEG_JIC=1.81, LEG_ORB=1.73, HEXB=0.875, Y=1.312, D1=0.844, D2=0.391 | Q-BRENNAN-ONLY |
| 6801-24-32-NWO-FG | STEP | STEP | p41 6801-24-32-NWO-FG | LEG_JIC=2.810, LEG_ORB=2.890, HEXB=2.750, Y=2.500, D1=1.312, D2=1.781 | Q-BRENNAN-ONLY |
| 6802-04-02-NWO-FG | STEP | STEP | - | - | Q-BRENNAN-ONLY |
| 6806-12-08-NWO-FG | WORK | WORK | - | - | Q-NEWMASTER-6806, Q-BRENNAN-ONLY, Q-TRANSFER-NUTHEX |
| 6900-32-32-O | WORK | WORK | p19 6900-32-32-O | W4=2.420?, L2=2.000?, C2HEX=2.750, CHEX=2.625, D1=1.781, D=1.781? | Q-NEWMASTER-6900, Q-BRENNAN-ONLY |
| 6901-32-32-NWO-FG | WORK | WORK | p46 6901-32-32-NWO-FG | N5=2.890?, M1=2.430??, W3=2.850??, CHEX=2.625, C4HEX=2.750, C1HEX=2.500??, D1=1.781, D=1.720? | Q-NEWMASTER-6901, Q-BRENNAN-ONLY |
| 6902-24-24-NWO-FG | WORK | WORK | p46 6902-24-24-NWO-FG | N4=1.910?, M=1.350??, W2=1.770??, CHEX=2.125, C4HEX=2.125, C1HEX=1.875?, D1=1.312, D=1.250? | Q-NEWMASTER-6902, Q-BRENNAN-ONLY, Q-NEW-ANGLEDHELIX, Q-NEW-ANGLEDNUT |

`?` = pairing likely, `??` = uncertain (see `F2b.json` cells[].pairing). Every cell with its pairing reason, OMi / Air-Way comparison and the step verdicts are in `F2b.json`. Drawings looked at: `impact/F2b_work/png/`.

## Notes per row

- **5404-L-04X3.000** (WORK -> WORK): No Brennan catalog row. 5404-L-04X3.000 stays WORK.
- **5404-L-04X4.000** (WORK -> WORK): No Brennan catalog row. 5404-L-04X4.000 stays WORK.
- **5404-N-04X2.500** (DECIDE -> DECIDE): Catalog row 5404-N-04X2.500 p11 (L 2.500, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X3.500** (DECIDE -> DECIDE): Catalog row 5404-N-04X3.500 p11 (L 3.500, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X4.000** (DECIDE -> DECIDE): Catalog row 5404-N-04X4.000 p11 (L 4.000, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X4.500** (DECIDE -> DECIDE): Catalog row 5404-N-04X4.500 p11 (L 4.500, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X5.000** (DECIDE -> DECIDE): Catalog row 5404-N-04X5.000 p11 (L 5.000, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X5.500** (DECIDE -> DECIDE): Catalog row 5404-N-04X5.500 p11 (L 5.500, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-04X6.000** (DECIDE -> DECIDE): Catalog row 5404-N-04X6.000 p11 (L 6.000, drills 0.281/0.281). Bucket stays DECIDE.
- **5404-N-06X2.000** (WORK -> WORK): Catalog row 5404-N-06X2.000 p11 (L 2.000, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-06X2.500** (WORK -> WORK): Catalog row 5404-N-06X2.500 p11 (L 2.500, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-06X3.000** (WORK -> WORK): Catalog row 5404-N-06X3.000 p11 (L 3.000, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-06X3.500** (WORK -> WORK): Catalog row 5404-N-06X3.500 p12 (L 3.500, drills 3.500/88.90). The catalog row is misprinted in the DRILL columns (3.500 / 88.90 = the length in inch / mm). Bucket stays WORK.
- **5404-N-06X4.000** (WORK -> WORK): Catalog row 5404-N-06X4.000 p11 (L 4.000, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-06X4.500** (WORK -> WORK): No Brennan row for this cut length (catalog has no 5404-N-06X4.500). Bucket stays WORK.
- **5404-N-06X5.000** (WORK -> WORK): Catalog row 5404-N-06X5.000 p11 (L 5.000, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-06X6.000** (WORK -> WORK): Catalog row 5404-N-06X6.000 p11 (L 6.000, drills 0.406/0.406). Bucket stays WORK.
- **5404-N-08X2.500** (DECIDE -> DECIDE): Catalog row 5404-N-08X2.500 p12 (L 2.500, drills 0.531/0.531). Bucket stays DECIDE.
- **5404-N-08X3.500** (DECIDE -> DECIDE): Catalog row 5404-N-08X3.500 p12 (L 3.500, drills 0.531/0.531). Bucket stays DECIDE.
- **5404-N-08X4.500** (DECIDE -> DECIDE): Catalog row 5404-N-08X4.500 p12 (L 4.500, drills 0.531/0.531). Bucket stays DECIDE.
- **5404-N-08X5.000** (DECIDE -> DECIDE): Catalog row 5404-N-08X5.000 p12 (L 5.000, drills 0.531/0.531). Bucket stays DECIDE.
- **5404-N-08X5.500** (DECIDE -> DECIDE): No Brennan row for this cut length (catalog has no 5404-N-08X5.500). Bucket stays DECIDE.
- **5404-N-08X6.000** (DECIDE -> DECIDE): Catalog row 5404-N-08X6.000 p12 (L 6.000, drills 0.531/0.531). Bucket stays DECIDE.
- **5404-R-04-04-047** (WORK -> WORK): No Brennan catalog row. 5404-R-04-04-047 stays WORK.
- **5405-04-02** (STEP -> DECIDE): Catalog row 5405-04-02 TFA p12. paper check (catalog L vs male end ENDL[4] 0.56 + female port P1[2] 0.46 = 1.02): clear by 0.20.
- **5405-04-12** (STEP -> DECIDE): Catalog row 5405-04-12 TFA p12. paper check (catalog L vs male end ENDL[4] 0.56 + female port P1[12] 0.91 = 1.47): clear by 0.27.
- **5405-08-04** (STEP -> DECIDE): Catalog row 5405-08-04 TFA p12. paper check (catalog L vs male end ENDL[8] 0.75 + female port P1[4] 0.67 = 1.42): clear by 0.22.
- **5405-16-24** (STEP -> DECIDE): Catalog row 5405-16-24 TFA p12. paper check (catalog L vs male end ENDL[16] 0.94 + female port P1[24] 1.16 = 2.10): clear by 0.36.
- **5405-20-20** (STEP -> DECIDE): Catalog row 5405-20-20 TFA p12. paper check (catalog L vs male end ENDL[20] 0.97 + female port P1[20] 1.16 = 2.13): clear by 0.36.
- **5405-20-32** (STEP -> DECIDE): Catalog row 5405-20-32 TFA p12. paper check (catalog L vs male end ENDL[20] 0.97 + female port P1[32] 1.18 = 2.15): clear by 0.45.
- **5405-24-20** (STEP -> DECIDE): Catalog row 5405-24-20 TFA p12. paper check (catalog L vs male end ENDL[24] 1.00 + female port P1[20] 1.16 = 2.16): clear by 0.38.
- **5406-32-04** (STEP -> DECIDE): Catalog row 5406-32-04 TFA p13 (L 1.750, hex 2.500, A1 DRILL 0.431). Paper check: hex length = L - ENDL[32] 1.03 = 0.72 (positive); female -04 port P1 0.67 sits inside the 2-in male end (wall checked by the generator).
- **5406-40-32** (WORK -> WORK): Catalog row 5406-40-32 TFA p13: L 2.370, hex 3.000, A1 DRILL 2.172 (not the -32 tap drill 2.19/2.20 - shows that A1 DRILL is not a tap drill column). Stays WORK.
- **5406-C-20** (STEP -> DECIDE): Catalog row 5406-C-20 TFA p67. Paper check: closed end wall = L 1.250 - female port P1 (MS51503 max, 2405 table) 1.16 = 0.09 - THIN: SPEC 5406C assumes the MS51503 P1-max drill depth, which a short Brennan cap may not use; if the build refuses it, the port depth needs the STEP.
- **5406-C-24** (STEP -> DECIDE): Catalog row 5406-C-24 TFA p67. Paper check: closed end wall = L 1.540 - female port P1 (MS51503 max, 2405 table) 1.16 = 0.38.
- **5406-C-32** (STEP -> DECIDE): Catalog row 5406-C-32 TFA p67. Paper check: closed end wall = L 1.370 - female port P1 (MS51503 max, 2405 table) 1.18 = 0.19.
- **5406-HHP-01** (WORK -> WORK): Documented variant: OMi 5406-HHP-01 = Brennan 5406-HP-01 (TFA p67: L 0.300, socket hex 0.156). OMi gives no dimension. Stays WORK.
- **5406-HHP-02** (WORK -> WORK): Documented variant: OMi 5406-HHP-02 = Brennan 5406-HP-02 (TFA p67: L 0.30, socket hex 0.188). OMi gives no dimension. Stays WORK.
- **5406-HHP-04** (WORK -> WORK): Documented variant: OMi 5406-HHP-04 = Brennan 5406-HP-04 (TFA p67: L 0.46, socket hex 0.250). OMi gives no dimension. Stays WORK.
- **5406-HHP-06** (WORK -> WORK): Documented variant: OMi 5406-HHP-06 = Brennan 5406-HP-06 (TFA p67: L 0.46, socket hex 0.312). OMi gives no dimension. Stays WORK.
- **5406-HHP-08** (WORK -> WORK): Documented variant: OMi 5406-HHP-08 = Brennan 5406-HP-08 (TFA p67: L 0.610, socket hex 0.375). OMi gives no dimension. Stays WORK.
- **5406-HHP-12** (WORK -> WORK): Documented variant: OMi 5406-HHP-12 = Brennan 5406-HP-12 (TFA p67: L 0.620, socket hex 0.562). OMi gives no dimension. Stays WORK.
- **5406-HHP-16** (WORK -> WORK): Documented variant: OMi 5406-HHP-16 = Brennan 5406-HP-16 (TFA p67: L 0.79, socket hex 0.625). OMi gives no dimension. Stays WORK.
- **5406-HHP-20** (WORK -> WORK): Documented variant: OMi 5406-HHP-20 = Brennan 5406-HP-20 (TFA p67: L 0.770, socket hex 0.750). OMi gives no dimension. Stays WORK.
- **5406-HHP-24** (WORK -> WORK): Documented variant: OMi 5406-HHP-24 = Brennan 5406-HP-24 (TFA p67: L 0.83, socket hex 1.00). OMi gives no dimension. Stays WORK.
- **5406-HHP-32** (WORK -> WORK): Documented variant: OMi 5406-HHP-32 = Brennan 5406-HP-32 (TFA p67: L 0.87, socket hex 0.75). OMi gives no dimension. Stays WORK.
- **5406-P-02** (DECIDE -> NOW): Catalog row 5406-P-02 TFA p67. Status if built from the catalog: ASSUMED; VERIFIED if the user accepts the Air-Way alias (Air-Way = catalog on both cells).
- **5406-P-04** (DECIDE -> NOW): Catalog row 5406-P-04 TFA p67. Status if built from the catalog: ASSUMED; VERIFIED if the user accepts the Air-Way alias (Air-Way = catalog on both cells).
- **5406-P-06** (DECIDE -> NOW): Catalog row 5406-P-06 TFA p67. Status if built from the catalog: ASSUMED; VERIFIED if the user accepts the Air-Way alias (Air-Way = catalog on both cells).
- **5406-SHP-04** (WORK -> WORK): Catalog row 5406-SHP-04 TFA p67 (L 0.750, square 0.375). OMi gives no dimension. Stays WORK.
- **5406-SHP-06** (WORK -> WORK): Catalog row 5406-SHP-06 TFA p67 (L 0.780, square 0.437). OMi gives no dimension. Stays WORK.
- **5406-SHP-08** (WORK -> WORK): Catalog row 5406-SHP-08 TFA p67 (L 1.020, square 0.563). OMi gives no dimension. Stays WORK.
- **5406-SHP-12** (WORK -> WORK): Catalog row 5406-SHP-12 TFA p67 (L 1.100, square 0.625). OMi gives no dimension. Stays WORK.
- **5406-SHP-16** (WORK -> WORK): Catalog row 5406-SHP-16 TFA p67 (L 1.300, square 0.812). OMi gives no dimension. Stays WORK.
- **5500-16-08-FG** (DECIDE -> NOW): Catalog row 5500-16-08-FG TFA p30; all 5 OMi values equal the catalog.
- **5501-24-24-FG** (WORK -> WORK): Catalog row 5501-24-24-FG TFA p31 = OMi on all 5 values. Stays WORK.
- **5501-32-32-FG** (WORK -> WORK): No catalog row (table ends at -24); OMi values used via the series-level answer to Q-B-OTHER-5501. Stays WORK.
- **5503-04-02-FG** (WORK -> WORK): No Brennan catalog row (Brennan 5503-02-04-FG is MP 1/8 x FP 1/4 - a different part from OMi 5503-04-02-FG). Stays WORK.
- **5503-06-04-FG** (WORK -> WORK): No Brennan catalog row (Brennan 5503-02-04-FG is MP 1/8 x FP 1/4 - a different part from OMi 5503-06-04-FG). Stays WORK.
- **5503-08-06-FG** (WORK -> WORK): No Brennan catalog row (Brennan 5503-02-04-FG is MP 1/8 x FP 1/4 - a different part from OMi 5503-08-06-FG). Stays WORK.
- **5503-12-08-FG** (WORK -> WORK): No Brennan catalog row (Brennan 5503-02-04-FG is MP 1/8 x FP 1/4 - a different part from OMi 5503-12-08-FG). Stays WORK.
- **5503-16-12-FG** (WORK -> WORK): No Brennan catalog row (Brennan 5503-02-04-FG is MP 1/8 x FP 1/4 - a different part from OMi 5503-16-12-FG). Stays WORK.
- **5505-20-20-FG** (WORK -> WORK): Catalog row 5505-20-20-FG TFA p33 (N = N1 1.44, Y 1.875). OMi gives no dimension. Stays WORK.
- **5600-20-20-20-FG** (STEP -> NOW): Catalog row 5600-20-20-20-FG TFA p55. Check at build: the male NPTF pipe OD 1.660 exceeds the flats 1.625 by 0.035 (thread proud of the flats) - the kind of warning Task C accepted on 5500-16-08-FG / 5600-16-16-16-FG (0.007), here larger.
- **5600-24-24-24-FG** (STEP -> NOW): Catalog row 5600-24-24-24-FG TFA p55. Check at build: the male NPTF pipe OD 1.900 exceeds the flats 1.875 by 0.025 (thread proud of the flats) - the kind of warning Task C accepted on 5500-16-08-FG / 5600-16-16-16-FG (0.007), here larger.
- **5601-02-02-02-FG** (WORK -> WORK): Catalog row 5601-02-02-02-FG TFA p55. OMi gives no dimension. Stays WORK.
- **5601-20-20-20-FG** (WORK -> WORK): Catalog row 5601-20-20-20-FG TFA p55. OMi gives no dimension. Stays WORK.
- **5601-24-24-24-FG** (WORK -> WORK): Catalog row 5601-24-24-24-FG TFA p55. OMi gives no dimension. Stays WORK.
- **5603-02-02-02-FG** (WORK -> WORK): Catalog row 5603-02-02-02-FG TFA p55 (symmetric dashes: N1 = N2, so the N1/N3 pairing question does not change any value). OMi gives no dimension. Stays WORK.
- **5603-12-12-12-FG** (WORK -> WORK): Catalog row 5603-12-12-12-FG TFA p56 (symmetric dashes: N1 = N2, so the N1/N3 pairing question does not change any value). OMi gives no dimension. Stays WORK.
- **5603-24-24-24-FG** (WORK -> WORK): Catalog row 5603-24-24-24-FG TFA p56 (symmetric dashes: N1 = N2, so the N1/N3 pairing question does not change any value). OMi gives no dimension. Stays WORK.
- **5604-32-32-32-FG** (STEP -> DECIDE): Catalog row 5604-32-32-32-FG TFA p56. Paper check: male -32 pipe OD 2.375 < flats 2.812.
- **5652-32-32-32-32-FG** (WORK -> WORK): No Brennan catalog row for -32 (5652-FG table p63 ends at -24). Stays WORK.
- **6401-16-20-O** (NOW -> NOW): Catalog row 6401-16-20-O TFA p15 confirms every OMi value (expected: one source).
- **6401-20-16-O** (NOW -> NOW): Catalog row 6401-20-16-O TFA p15 confirms every OMi value (expected: one source).
- **6401-24-20-O** (NOW -> NOW): Catalog row 6401-24-20-O TFA p15 confirms every OMi value (expected: one source).
- **6404-08-12** (DECIDE -> DECIDE): Catalog row 6404-08-12 TFA p15 = OMi on all 3 values.
- **6405-02-02-O** (WORK -> WORK): Catalog row 6405-02-02-O TFA p15 (L 0.950, hex 0.562, D3 0.062). OMi gives no dimension. With the catalog no download is needed if Q-TRANSFER-TAPDRILL = yes. Stays WORK.
- **6405-02-04-O** (WORK -> WORK): Catalog row 6405-02-04-O TFA p15 (L 1.240, hex 0.750, D3 0.062). OMi gives no dimension. With the catalog no download is needed if Q-TRANSFER-TAPDRILL = yes. Stays WORK.
- **6405-16-24-O** (DECIDE -> DECIDE): Catalog row 6405-16-24-O TFA p16.
- **6405-32-16-O** (DECIDE -> DECIDE): Catalog row 6405-32-16-O TFA p16. D3 conflict OMi 1.080 vs catalog 1.156 (diffcheck: real).
- **6408-HHP-02-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-02-O = Brennan 6408-H02-O (TFA p67: L 0.400, socket 0.125). Stays WORK.
- **6408-HHP-03-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-03-O = Brennan 6408-H03-O (TFA p67: L 0.40, socket 0.125). Stays WORK.
- **6408-HHP-04-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-04-O = Brennan 6408-H04-O (TFA p67: L 0.47, socket 0.188). Stays WORK.
- **6408-HHP-05-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-05-O = Brennan 6408-H05-O (TFA p67: L 0.47, socket 0.188). Stays WORK.
- **6408-HHP-06-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-06-O = Brennan 6408-H06-O (TFA p67: L 0.50, socket 0.250). Stays WORK.
- **6408-HHP-08-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-08-O = Brennan 6408-H08-O (TFA p67: L 0.58, socket 0.313). Stays WORK.
- **6408-HHP-10-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-10-O = Brennan 6408-H10-O (TFA p67: L 0.65, socket 0.375). Stays WORK.
- **6408-HHP-12-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-12-O = Brennan 6408-H12-O (TFA p67: L 0.77, socket 0.562). Length differs from OMi (diffcheck: real). Stays WORK.
- **6408-HHP-16-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-16-O = Brennan 6408-H16-O (TFA p67: L 0.775, socket 0.625). Length differs from OMi (diffcheck: real). Stays WORK.
- **6408-HHP-20-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-20-O = Brennan 6408-H20-O (TFA p67: L 0.77, socket 0.750). Stays WORK.
- **6408-HHP-24-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-24-O = Brennan 6408-H24-O (TFA p67: L 0.770, socket 0.750). Stays WORK.
- **6408-HHP-32-O** (WORK -> WORK): Documented variant: OMi 6408-HHP-32-O = Brennan 6408-H32-O (TFA p67: L 0.77, socket 0.750). Stays WORK.
- **6410-04-02-O** (WORK -> WORK): Catalog row 6410-04-02-O TFA p16 = OMi on L/hex/bore. Stays WORK.
- **6410-16-04-O** (DECIDE -> DECIDE): Catalog row 6410-16-04-O TFA p16 (L 1.00). Bore conflict OMi 0.368 vs catalog 0.389 (diffcheck: real).
- **6410-20-06-O** (DECIDE -> DECIDE): Catalog row 6410-20-06-O TFA p16 (L 1.000) = OMi on L, hex and bore.
- **6410-20-08-O** (DECIDE -> DECIDE): Catalog row 6410-20-08-O TFA p16 (L 1.000) = OMi on L, hex and bore.
- **6410-32-12-O** (STEP -> STEP): Catalog row 6410-32-12-O TFA p16 repeats OMi (L 1.000 impossible). Stays STEP. Bore: catalog 0.980 vs OMi 0.981 (diffcheck: rounding-only).
- **6410-32-16-O** (STEP -> STEP): Catalog row 6410-32-16-O TFA p16 repeats OMi (L 1.000 impossible). Stays STEP.
- **6500-04-02-FG** (WORK -> WORK): No Brennan catalog row (6500-FG p34 has no 6500-04-02-FG). Stays WORK.
- **6500-20-16-FG** (STEP -> STEP): No Brennan catalog row (6500-FG p34 has no 6500-20-16-FG). Stays STEP.
- **6500-24-20-FG** (STEP -> STEP): No Brennan catalog row (6500-FG p34 has no 6500-24-20-FG). Stays STEP.
- **6500-32-24-FG** (STEP -> STEP): No Brennan catalog row (6500-FG p34 has no 6500-32-24-FG). Stays STEP.
- **6501-06-04-FG** (DECIDE -> NOW): Catalog row 6501-06-04-FG TFA p35 = OMi on all 7 values.
- **6501-12-08-FG** (DECIDE -> DECIDE): Catalog row 6501-12-08-FG TFA p35; M5 conflict (diffcheck idx 31: real, -0.072).
- **6501-16-12-FG** (STEP -> STEP): No Brennan catalog row and no OMi value. Stays STEP.
- **6501-32-32-FG** (DECIDE -> NOW): Catalog row 6501-32-32-FG TFA p35 = OMi on all 7 values.
- **6502-04-02-FG** (WORK -> WORK): No Brennan catalog row and no OMi value. Stays WORK.
- **6502-06-04-FG** (STEP -> STEP): No Brennan catalog row and no OMi value. Stays STEP.
- **6502-10-08-FG** (DECIDE -> NOW): Catalog row 6502-10-08-FG TFA p35 = OMi on all 7 values.
- **6502-12-10-FG** (STEP -> STEP): No Brennan catalog row and no OMi value. Stays STEP.
- **6502-16-12-FG** (WORK -> WORK): Catalog row 6502-16-12-FG TFA p35 = OMi on all 7 values. Stays WORK.
- **6504-04-06** (DECIDE -> NOW): Catalog row 6504-04-06 TFA p17: L5 = OMi Overall Length, L gives L14; hexes and bores = OMi. Nut-face-to-seat L5 - L = 0.380 for swivel -06 (Brennan 6504 rows at this size: 0.37/0.38) = one of the Air-Way offsets Task C paper-checked this row with (clean).
- **6504-06-04** (DECIDE -> NOW): Catalog row 6504-06-04 TFA p17: L5 = OMi Overall Length, L gives L14; hexes and bores = OMi. Nut-face-to-seat L5 - L = 0.344 for swivel -04 (Brennan 6504 rows at this size: 0.344/0.351) = one of the Air-Way offsets Task C paper-checked this row with (clean).
- **6504-08-10** (DECIDE -> NOW): Catalog row 6504-08-10 TFA p17: L5 = OMi Overall Length, L gives L14; hexes and bores = OMi. Nut-face-to-seat L5 - L = 0.500 for swivel -10 (Brennan 6504 rows at this size: 0.46/0.50) = one of the Air-Way offsets Task C paper-checked this row with (clean).
- **6504-08-12** (DECIDE -> DECIDE): No Brennan catalog row; OMi gives L13 2.100, hexes and bores.
- **6504-10-08** (DECIDE -> DECIDE): No Brennan catalog row; OMi gives L13 1.970, hexes and bores.
- **6504-10-12** (DECIDE -> DECIDE): No Brennan catalog row; OMi gives L13 2.320, hexes and bores.
- **6504-12-10** (DECIDE -> DECIDE): No Brennan catalog row; OMi gives L13 2.210, hexes and bores.
- **6504-12-16** (DECIDE -> NOW): Catalog row 6504-12-16 TFA p17: L5 = OMi Overall Length, L gives L14; hexes and bores = OMi. Nut-face-to-seat L5 - L = 0.590 for swivel -16 (Brennan 6504 rows at this size: 0.59) = one of the Air-Way offsets Task C paper-checked this row with (clean).
- **6504-16-20** (DECIDE -> DECIDE): No Brennan catalog row; OMi gives L13 2.610, hexes and bores.
- **6504-32-32** (DECIDE -> DECIDE): Catalog row 6504-32-32 TFA p17: hexes/bores = OMi; lengths inconsistent.
- **6505-04-02** (WORK -> WORK): No Brennan catalog row; Q-B-SWSTR answered at series level (OMi lengths usable). Stays WORK.
- **6505-06-04** (DECIDE -> NOW): Catalog row 6505-06-04 TFA p18 = OMi on all 6 values (nut hex 0.563 vs 0.562 = 9/16, rounding-only).
- **6505-12-08** (DECIDE -> DECIDE): Catalog row 6505-12-08 TFA p18; lengths/hexes = OMi; D1 conflict (diffcheck idx 59: real).
- **6505-16-12** (DECIDE -> NOW): No Brennan catalog row; OMi values (L15 2.48, L16 1.91, hexes, bores) become usable.
- **6506-06-04** (DECIDE -> DECIDE): Catalog row 6506-06-04 TFA p18 = OMi on L17, L18, both hexes and the bore; the female-port tap drill is the open cell.
- **6506-06-10** (DECIDE -> DECIDE): Catalog row 6506-06-10 TFA p18 = OMi on L17, L18, both hexes and the bore; the female-port tap drill is the open cell.
- **6506-12-08** (DECIDE -> DECIDE): No Brennan catalog row (6506-08-12 exists, not -12-08).
- **6506-32-32** (DECIDE -> DECIDE): Catalog row 6506-32-32 TFA p18; the female-port tap drill is the open cell. L17 conflict OMi 3.200 vs catalog 3.12 (diffcheck idx 73: real).
- **6606-04-04-04-FG** (WORK -> WORK): Catalog row 6606-04-04-04-FG TFA p58. OMi gives no dimension. Stays WORK.
- **6606-08-08-08-FG** (WORK -> WORK): Catalog row 6606-08-08-08-FG TFA p58. OMi gives no dimension. Stays WORK.
- **6606-10-10-10-FG** (WORK -> WORK): Catalog row 6606-10-10-10-FG TFA p58. OMi gives no dimension. Stays WORK.
- **6606-16-16-16-FG** (WORK -> WORK): Catalog row 6606-16-16-16-FG TFA p58. OMi gives no dimension. Stays WORK.
- **6801-16-08-NWO-FG** (STEP -> STEP): Catalog row 6801-16-08-NWO-FG TFA p41 gives 6 of the 10 missing cells. Stays STEP (download still needed for the ORB end).
- **6801-24-32-NWO-FG** (STEP -> STEP): Catalog row 6801-24-32-NWO-FG TFA p41 gives 6 of the 10 missing cells. Stays STEP (download still needed for the ORB end).
- **6802-04-02-NWO-FG** (STEP -> STEP): No Brennan catalog row. Stays STEP.
- **6806-12-08-NWO-FG** (WORK -> WORK): No Brennan catalog row. Stays WORK.
- **6900-32-32-O** (WORK -> WORK): Catalog row 6900-32-32-O TFA p19. OMi gives no dimension. Stays WORK.
- **6901-32-32-NWO-FG** (WORK -> WORK): Catalog row 6901-32-32-NWO-FG TFA p46. OMi gives no dimension. Stays WORK.
- **6902-24-24-NWO-FG** (WORK -> WORK): Catalog row 6902-24-24-NWO-FG TFA p46. OMi gives no dimension. Stays WORK.
