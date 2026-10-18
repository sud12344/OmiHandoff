# OMi dimension audit - 2026-09-25

**Audit only. Nothing in the library was changed.** Task: `00_DOCS/NEXT_SESSION_PROMPT_OMi_dimension_audit.md`.
Workbook: `00_DOCS/OMi_Dimension_Audit_2026-09-25.xlsx` (13 sheets, listed at the end). Scripts, intermediates and the
re-check journals: `tools/_out/omi_audit/` (start with its `HANDOFF.md`). OMi file: the unchanged copy
`07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx` (SHA256 `e5109342...291840`, README next to it).

## 1. In one screen

| | |
|---|---|
| OMi file | sheet `Items`, 7,303 parts (all materials). 3,257 are carbon-steel parts of the 126 topologies (2,300 standard, 499 FS-, 373 C-, 73 LS-, 12 TGT-). **840 of them carry at least one dimension, all standard parts, in 42 topologies.** The other 84 topologies get no dimension from this file. |
| What OMi gives | Overall Length, M 1 / M 2 / L 1 Size (leg lengths), Hex Flat, Nut Hex 1/2, Side 1-3 ID, Body Diameter (8 parts). Inches, text, 2-3 decimals, no tolerances. **No** thread length, port depth, seat / nose / collar geometry, groove or tap drill. |
| Configurations | Every one of the 1,804 BUILD rows is an OMi part (0 extra BUILD rows). 1,801 OMi part numbers match BUILD rows exactly (2408-04 / -06 / -20 each sit on a SOLID and an -H row). 79 OMi parts sit only on DROP rows, 420 standard parts are in no table (30 kits + 390 not in the feed), 957 FS-/C-/LS-/TGT- parts are not tabled yet. 1,426 OMi-file parts are not in the OMi feed. |
| Dimensions, certain mappings (headline) | 2,209 comparisons: **478 equal, 1,139 rounding only, 235 real differences, 357 only OMi has a value.** |
| Dimensions, uncertain mappings | 1,111 comparisons (269 real differences) on the PROVISIONAL sheet - not in the headline. |
| Threads (normalized text) | 852 comparisons: 749 equal, **36 real differences** (24: the OMi callout fits no dash of its own part number; 12: the review text is a known Air-Way misprint and OMi has the right callout), 55 OMi texts unparseable (mostly `1 11-1/2 NPTF`), 12 OMi lists fewer / more threads. |
| Hex A/F | All 669 certain hex comparisons: OMi gives the 1/16-in wrench fraction to 3 decimals every time; in 575 the review value is that fraction rounded to 2 decimals (Air-Way style). 36 are real differences. |
| MISSING rows (727) | OMi has any dimension for **183**; it fills every empty cell of **1** row through certain mappings (6504-06-08, Air-Way bores garbled). 544 get nothing. Details in section 3. |
| Independent re-check | Every item re-derived from the raw files by separate agents with their own code (11 checkers, 2 passes, 5,539 items). **No claim was refuted.** 15 wording corrections they proposed were applied and confirmed in the second pass; 1,739 items are individually confirmed, the other 3,800 (equal / rounding rows, non-difference threads, MISSING rows) were recomputed with no disagreement. |

## 2. Your question during the run: does the OMi file cover the ~700 configurations that were MISSING?

No. Of the 727 BUILD rows that are DataStatus MISSING today:

| OMi file offers | Rows |
|---|---|
| nothing at all (part has no dimension cell) | 544 |
| every empty cell, through certain mappings | 1 (6504-06-08) |
| every empty cell, some only through an uncertain mapping | 5 (6506 L17 via Overall Length) |
| some empty cells; others stay empty | 150 |
| values, but the table is a skeleton with no dimension column (6420 / 6425: OAL + hex) | 8 |
| values that land on no empty cell | 19 |

By coverage code, OMi has any dimension on F1 70 of 260 (report only - you decided to wait for Brennan -FG STEPs),
F2 87 of 281, F3 8 of 138, F4 5 of 14, F5 5 of 5, D-codes 8 of 29. Even where OMi fills cells, the thread,
port-depth, seat and groove cells stay empty, and OMi alone is one source (ASSUMED at best). Sheet `MISSING fill`.

## 3. Findings (facts; nothing decided)

### 3.1 Real differences on certain mappings (235)

| Review table | OMi column | Review column | Real / compared |
|---|---|---|---|
| 6405 | Overall Length | L31@DRIVE | 29 of 40 |
| 6410 | Overall Length | L33@DRIVE | 26 of 36 |
| 2706 | Overall Length | L25@DRIVE | 19 of 23 |
| 1404 | Side 2 ID | D@BORE | 18 of 23 |
| 2705 | Overall Length | L24@DRIVE | 17 of 19 |
| 6401 | Overall Length | L29@DRIVE | 16 of 21 |
| 6410 | Side 1 ID | D@BORE | 16 of 36 |
| 6404 | Overall Length | L32@DRIVE | 14 of 16 |
| 6405 | Side 1 ID | D3@BORE | 12 of 40 |
| 2706 | Side 1 ID | D1@BORE | 8 of 23 |
| hexes (6400 5, 6505 5, 5502 4, 6404 4, 6410 4, 2501 2, 2705 2, 6401 2, 6500 2, 5500 / 6402 / 6405 / 6504 1 each) | Hex Flat | - | 34 |
| other bores / lengths / nut hexes (6565 8, 0403 2, 2404 2, 2706 2, 6400 3, 6408 2, 6402 2, 1404 / 2501 / 2503 / 6504 / 6505 1 each) | | | 26 |

- Size: 46 are 0.010 in or less, 26 up to 0.020, 25 up to 0.050, 74 up to 0.100, 64 above 0.100.
- 15 of them equal the review value if OMi is **cut** (not rounded) to Air-Way's decimals (6410 bores 0.386 / 0.38,
  0.508 / 0.50 ...; 6565 bores 0.297 / 0.29 ...; 6500-20-20-FG hex 1.625 / 1.62). Air-Way may truncate there. They stay
  real differences under the half-up rule (column "OMi cut to Air-Way's decimals = review").
- Where the parts stand: 11_MASTERS_NEW 138, both folders (0318 0403 6405 6408) 42, 11_MASTERS 22, hand-built 2404 /
  6400 10, not in a master (MISSING / BLOCKED / DROP rows) 23. 202 are on BUILD ASSUMED rows.
- The overall-length columns are not one fixed datum offset: every one has exact matches plus scattered differences of
  both signs. OMi's 6410 Overall Length is exactly `1.000` on 12 parts: Air-Way agrees on 2 (12-04, 16-06), differs on 5, and 5 are
  MISSING rows where `1.000` would be OMi's only length (16-04, 20-06, 20-08, 32-12, 32-16) - looks like a placeholder.
  6405 L31 was already flagged "Air-Way L31 suspect" (03_SCRIPTS/RUN_ME_straights.txt).
- OMi's bores often follow a dash lookup rather than the part: 1404 Side 2 ID is 0.21 / 0.32 / 0.44 / 0.61 / 0.78
  per second dash; on some reducers OMi gives the same bore on both sides (6402-06-04-O, 6402-08-10-O, 6505-12-16;
  2706 on 8 rows).
- SW2: in every certain-mapped column the SW2 value equals the review value, except where the gen_tee A/F rule raised a
  hex (27 rows, shown "raised by rule") and 10 6505 rows where the generator puts D@BORE into DA@BORE_A (D1 printed
  "---"). No master uses a value different from its review table in these columns.

- Smaller observations from the checkers (details in the sheets): OMi 1404 Hex Flat is the integer text `1` on two rows
  (read as 1.000, a real difference against Air-Way 0.94, uncertain mapping); 2503-04-08-FG and 2503-10-12-FG OMi M 1 / L 1
  look swapped against Air-Way M2 / N2 (uncertain); 2605-06-06-06-FG OMi legs 1.140 vs Air-Way -FG 1.06 (non-FG 1.16);
  0403-24-24 / -32-32 are in the OMi file (OAL 1.840 / 2.160) on DROP rows whose Air-Way L3 is 1.65 / 2.05.

### 3.2 Rounding (1,139, kept visible)
- 1,120: OMi's 3-decimal value rounded half-up to Air-Way's 2 printed decimals equals the review value (e.g. 0.562 ->
  0.56).
- 8: the review holds the exact fraction and OMi rounds it (0.4375 -> 0.438).
- 11: the review holds the exact fraction and OMi **cuts** it (0.5625 -> 0.562, 0.9375 -> 0.937; 2404 / 6400 hexes). A new
  class, not in your prompt's list; kept apart so you can set the threshold.

### 3.3 Threads
- 24 OMi callouts fit no dash of their own part number (e.g. 2706-08-08 `7/8-14` for a -08 JIC; 2404-16-24
  `1/2- 14 NPFT` for a -24 pipe; 6504 / 6505 / 6506 -06 swivels `1/2-20`). Candidates for a report to OMi.
- 12 review `$PRP@Threads` texts keep an Air-Way misprint (all already flagged in `$COMMENT`); OMi has the right callout,
  and the SW2 / masters already use the dash-correct thread (checked on 6410-16-16-O, 2503-16-20-FG, 5500-20-20-FG).
- OMi writes NPTF as `NPFT` in 188 cells and `1-11 1/2` as `1 11-1/2` (55 unparseable). Series words are not compared:
  e.g. OMi calls the NPSM swivel end of 1504-04-04-FG `1/4-18 NPTF` (Air-Way: NPSM).

### 3.4 Configurations and SW2 rows
- 79 OMi-file parts sit only on DROP rows whose `$COMMENT` says "no matching OMi SKU in catalog feed"; 48 of them carry
  OMi dimensions. None is in the feed. 87 more standard OMi parts with dimensions are in no table and not in the feed.
- 318 BUILD rows are not in the SW2 their master was built from: 267 skipped as DataStatus MISSING, 18 BLOCKED, 1 skipped
  (no end data), 32 in hand-made SW2 tables (no summary).
- 94 SW2 configurations are DROP in the review table (masters modelling parts the feed does not list): 2603HX 30, 2502HX 21,
  2500HX 16, 2403 15, 6400 8, 2405 4. 8 SW2 names differ from the review / OMi names (5404N `5404-N-8-8 X 3` vs
  `5404-N-08-08-X3`, 5406C `5406-C-8` vs `5406-C-08`).
- The 11_MASTERS builds of 0403, 5405, 6401, 6405, 6408 predate their current SW2 (report configuration counts differ).

### 3.5 Known items (sheet `Known items`, 77 rows; OMi's value next to each)
- **Majority-vote resolutions are listed as open conflicts.** Where OMi has a value on the disputed dimension:
  2404-16-24 L 2.51 and 2404-24-20 L 2.65 = Air-Way (+Brennan), not Parker; 2501-32-32-FG drill 1.938 = MS51504+Brennan,
  not Air-Way 1.86 (certain); 2501-04-02-FG N 0.78 = MS51504+Brennan (uncertain mapping). 2408-14, 5404-32-20,
  6801-05-05, 6802-14-14, 6803/6804 dash-5: OMi has no dimension.
- Column shift, reported, not moved: 2408-14-SOLID THDMAJ_B holds the voted hex 1.25; 2501-04-02-FG THDMAJ_A holds the
  voted N 0.78; 2501-32-32-FG Y@REF holds the voted drill 1.938 (OMi hex 2.500 = Air-Way's printed Y 2.50);
  `$PRP@AxialSource` reads "VERIFIED" on all three.
- 2408 duplicate OMiSKUs (2408-04 / -06 / -20 on SOLID + -H rows): OMi has no 2408 dimension, so it cannot say which.
- 6404-06-08: OMi Overall Length 1.580 (Air-Way 1.10, 6404-06-06 1.38) and Side 1 ID 0.531 (Air-Way 0.50, uncertain
  mapping) - OMi does
  not reproduce the suspicious Air-Way row.
- Hex A/F items (PROJECT_STATUS s3): OMi gives 0.562 / 0.625 / 0.688 / 0.875 / 2.875 for the swivel nuts Air-Way prints
  0.56 / 0.63 / 0.69 / 0.88 / 2.88 - on all 63 such nut-hex comparisons (1404, 6402, 6500-6506, 6565; sheet
  `Hex AF evidence`). 6801 (body hex -10 / -20 / -24), 1501-24-24-FG nut,
  6801-05-05, 6801-04-02 leg, 6801-12-12 thread length: the OMi file has no dimension for any 6801 or 1501 part.
- Air-Way anomaly rows: OMi reproduces **none** of the Air-Way misprints it could see: every thread typo in these rows
  (OMi has the corrected callout each time), 6504-06-08 bores (0.297 / 0.391, not ".030" / ".039"), 6504-24-24 D(1)
  (1.312, not 1.38; it equals D(2) 1.31 after rounding).
  OMi's bores and nut hex on 1404-16-20 / -20-16 fit the row order that was kept (pass 1).
- 6408 plugs: OMi gives a Side 1 ID for 6408-02-O, -03-O, -05-O and the "Solid" 6408-04-O-SLD (0.205 = the cored -04),
  which the review builds solid.

### 3.6 Is OMi independent of Air-Way? (evidence only)
- Against: 478 OMi values equal the review exactly, some written with Air-Way's 2 decimals (6500 / 6505 lengths); on 4 of the 2503 / 2502 leg conflicts (AW vs MS51508 /
  MS51506) and both 2404 L conflicts OMi carries the Air-Way value.
- For: OMi prints wrench fractions to 3 decimals where Air-Way prints 2 (1,139 rounding-only rows); it reproduces none of
  the 15 Air-Way misprints it covers (12 thread callouts, the two garbled 6504-06-08 bores, 6504-24-24 D(1)); on
  2501-32-32-FG, 2503-06-06 / -08-08 / -05-04 (uncertain) it carries the MS value instead of Air-Way's (2501-04-02-FG N as well, uncertain mapping); its 2602 / 2603 tee values equal the MS51506F /
  MS51510E values transcribed in `03_SCRIPTS/_legacy/ms_2503family.py` (mapper observation); its 0318 lengths equal the MS51531D
  nominals (Air-Way 0.01 shorter, uncertain mapping); its 6565-10-10 nut hex 1.000 equals Brennan (Air-Way 0.94).
- OMi also has its own errors: 24 thread callouts that contradict the part number, the 6410 `1.000` lengths, reducers
  with the same bore on both sides.

## 4. Questions for you
1. **Ranking.** Does OMi override Air-Way where they differ (235 real differences, section 3.1), and does OMi + Air-Way
   agreeing make a row VERIFIED (section 3.6)?
2. **Rounding threshold.** Accept the 1,120 half-up roundings and the 8 + 11 exact-fraction cases as agreement? What about the
   15 real differences that match if Air-Way truncated (section 3.1)?
3. **Hex A/F.** Snap Air-Way's 2-decimal hexes to the wrench fraction OMi gives (575 of 669 fit that pattern)?
4. **The 100 uncertain mappings** (sheet `Column mappings`, certainty "uncertain"; their comparisons are on PROVISIONAL):
   - leg lengths on the elbows and tees: OMi M 1 / M 2 / L 1 follow OMi's side order, the Air-Way letters differ per page
     (2501-2505, 2601-2611, 5500-5502, 6500-6503, 6500L);
   - overall lengths on the swivel straights and nuts: 6402 L26/L27, 6504 L13, 6505 L15/L16, 6506 L17/L18, 6565 L31/L32,
     0318 L1, 0319 L, 0403 L3 (datum not documented; the swivel ones agree with Air-Way on only 8 of 124 pairs);
   - 1404: Overall Length -> W or L (two candidates); Hex Flat -> body hex C(1) (the nut is in Nut Hex 1, so by elimination);
   - 2404: Side 1/2 ID on counterbored ends (counterbore or through passage?); 6404 Side 1 ID -> D1 or D3;
   - 6400L D1/D2, 2602 Y1 (hex or boss?), 0304 (OMi sells a JIC **cap** nut, Air-Way 304 is a tube nut), 0306 (ORFS rows),
     2504 / 2505 / 2606 / 2609 / 2611 / 5501 (table only, all MISSING).
   Which of these do you accept as certain?
5. **Real differences:** for each column in section 3.1, build Air-Way, OMi, or ask for a Brennan STEP?
6. **Scope:** the OMi file lists 79 parts that the review tables DROP ("no matching OMi SKU in catalog feed") and 390
   standard parts that are in no table, none of them in the feed. Is the OMi file an existence source, or does the feed
   stay the only one?
7. **6408 small plugs:** cored (OMi gives a bore) or solid (as built)?
8. **6410 `1.000` lengths (12 parts, 5 of them MISSING rows):** treat as placeholders?
9. **MISSING rows:** fill F2 / F3 rows from OMi alone (ASSUMED), or keep waiting for a second source? (F1 stays as you
   decided.)
10. **The open majority-vote conflicts** (section 3.5): decide each.
11. **Report to OMi:** the 24 wrong thread callouts, the 6410 `1.000` lengths and the same-bore reducers - together with the
    6801 findings already on the list?
12. **Masters:** the 94 SW2 configurations that are DROP (2603HX, 2502HX, 2500HX, 2403, 6400, 2405), the 5404N / 5406C
    configuration names, and the 11_MASTERS builds from older SW2 tables (0403 5405 6401 6405 6408).

## 5. Method
1. **OMi file.** Read twice (data_only True / False): 13,760 formula cells, all with cached values (none in a dimension
   column); 150 cells Excel turned into dates (Side 2 Size, Parker cross reference - no dimension column); no hidden rows or
   columns, no merged cells; row 2 is a note, row 3 blank; `Sheet1` is a thread lookup without part numbers.
2. **Configurations.** OMi part numbers matched EXACTLY on `$PRP@OMiSKU` (BUILD) and on OMiSKU / column A / `$PRP@PartNo`
   (DROP). No normalization was needed or applied. SW2 rows joined by SW2 OMiSKU, else column A, else PartNo; the SW2 of
   each master comes from its build report. Re-checked independently: 3,257 / 3,257 parts agree; 58 of 64 masters agree,
   the other 6 are the 6404 SW2 path (fixed: built from `tools/_out/regen_20260925/straight`) and the 5 11_MASTERS builds
   from older SW2 tables (reported).
3. **Column mapping.** 8 mapper agents + 8 challenger agents over the 42 topologies with OMi dimensions. Certain only when
   documents on both sides name the same feature (value agreement never promotes). 209 mappings: 109 certain, 100
   uncertain; 1 rejected (1404 Hex Flat -> nut hex). Row filters where a feature applies to some rows only (2404 bore
   states, 6408 not the HHP plugs, 6505 D1 printed / "---").
4. **Compare.** Exact fractions from the printed strings, never floats. Classes: equal; rounding only (OMi half-up to
   Air-Way's printed decimals, else to max(2, the review's decimals)); rounding only (review has more decimals); rounding
   only (OMi cut the review value) - new, kept apart; real difference; only one source. OMi text with fewer than 2 decimals
   is read as exact. Air-Way printed values come from `07_RAW_EXTRACTS/<series>.csv` (column found by value; part numbers
   zero-padded, also before a suffix such as `4 UNPL`); "no raw extract in repo - review value shown" where none exists.
   SW2 values converted per column (full, x2 for radii, sums for derived nose-tip lengths, A/F "raised by rule").
5. **Threads** as normalized text (collapse spaces, `1-1/16-12` = `1 1/16-12`, size-pitch tokens as multisets). The
   "which side fits the part number" note uses the generator's own dash tables (`gen_straight2.JIC`, `ORB_THR`, `npt_thr`),
   imported read-only.
6. **Independent re-check.** Pass 1: 9 agents by topology group recomputed every item (5,539: dimensions, threads, known
   items, MISSING rows) with their own scripts, reading the claims only afterwards. Pass 2: 2 agents on the 310 claims that
   changed after pass 1. Results per item in the workbook ("Independent re-check"); checker notes on sheet `Re-check`.

## 6. Workbook sheets
Summary (per topology) - Config differences - SW2 row differences - Dimension differences (certain) - PROVISIONAL -
Column mappings (evidence, challenger verdicts) - Unmapped OMi columns - OMi parts not in feed-tables - Known items -
Thread callouts - MISSING fill - Hex AF evidence - Re-check.
