# OMi's answers of 2026-10-18 - staged into review tables (NOT shipped)

The user's employer (OMi) answered our 2026-10-09 request (`10_DRAWINGS/for_OMi_2026-10-09/`). The user, 2026-10-18: "i attached
everything my employer sent this is verified information, use it to fill out more tables". Do not overwrite this folder.

## What OMi sent (unpacked unchanged in `07_RAW_EXTRACTS/omi_answers_20261018/`)
- `zip_a/OMi_missing_sizes_and_typos_2026-10-09.xlsx` = our workbook returned (saved 2026-10-14 by "Administrator"). Filled in:
  - "Lengths to check" column E "Real length" - all 14 rows.
  - "Possible typos" column F - all 32 rows (answers below).
  - "Sizes we need" - nothing typed in; answered with the drawings instead.
- 14 one-page PDF drawings (raster images; Brennan-format sheets = OMi's supplier) for 14 of the 226 "Sizes we need" parts:
  1405-04-06, 1405-08-12, 1502-06-06-FG, -12-08-FG, -12-12-FG, -20-20-FG, -24-24-FG, -32-32-FG, 1504-20-20-FG,
  1602-02-02-02-FG, -04-04-04-FG, -08-08-08-FG, -16-16-16-FG, -20-20-20-FG.
  Every value read by eye: `source/drawings_transcribed.csv` (part, feature, value, printed text, meaning, file).
  Asked but not sent: 1502-16-16-FG (row 7), and the other 211 rows.

## What was staged (`scratch_root/04_DESIGN_TABLES/`, base = batch-16 staging `wave1_ship_20261009/scratch_root`)
`scripts/stage_answers.py` -> `CHANGES.csv` (273 cells, each with its source). Only empty cells were filled (asserted).
- **14 rows from the drawings, MISSING -> ASSUMED**: 1405 x2, 1502 x6, 1504 x1, 1602 x5 - every size from the drawing; tap drill and
  thread majors from the end library (Q-TRANSFER-ENDLIB yes); the non-forged Air-Way rows were NOT used for the -FG parts.
  Column reading: 1405 W1 = overall, L1 = port face to stem tip (gen_straight2 SPEC); 1502 / 1602 N3 = axis crossing to the pipe
  port face, M1 = to the stem tip, W3 = to the nut face (gen_tee SPEC 1502 + the Brennan-letter pairing noted on 1502-02-02-FG);
  1504 N2 / M / W2 read the same way (no 1504 SPEC yet; the drawing measures all three from the axis crossing).
- **6410-16-04-O, MISSING -> ASSUMED**: OMi's real length 1.0 + hex / Side 1 ID from OMi's website file + ORB end values per dash.
- **6410-20-06-O / -20-08-O / -32-12-O / -32-16-O**: length, hex, end values filled, but they STAY MISSING: OMi's Side 1 ID is
  wider than the female port drill (0.509 > 0.50, 0.689 > 0.68, 0.981 > 0.97, 1.231 > 1.22) = the open Q-BOREWIDE (question 2 of
  2026-09-26, the 10 held rows); -32 also lacks the male ORB groove width.
- **8 rows where OMi's real length = the Air-Way length already in the table** (6405-20-16-O, 6410-12-04 / -16-06 / -16-08 /
  -20-12 / -24-12 / -24-16 / -32-20-O): no value change; note appended. Air-Way and OMi now agree on those lengths. 6405-20-16-O's
  "1.000 placeholder" question is closed (it was already built at the Air-Way 1.2).
- **6420-08-08**: real length 1.5 noted; still MISSING (6420 has no Air-Way series and no generator SPEC).

DataStatus: OMi alone = ASSUMED by the project rule (VERIFIED needs 2 independent sources; OMi's data is Brennan's, evidence
2026-09-26). The user called the data "verified" - asked whether to mark these rows VERIFIED anyway (PROJECT_STATUS s5).

## Ready to build vs waiting
- Generator-ready now (static checks clean, `checks.txt`): 1405 +2, 1502 +6, 6410 +1 = 9 configurations. Next: SolidWorks dry runs
  (1405, 1502, 6410), then ship with / after batch 16 (1502 is new in batch 16 - ship them together or after it).
- 1504-20-20-FG and the 5 1602 rows have their sizes now but no master: they need the approved wave-2 generator work
  (Q-NEW-ANGLEDHELIX / ANGLEDFEMALE for 1504, Q-NEW-PERLEGSW for 1602; stopped part-way in `tools/_out/wave2_impl_20261009/`).

## OMi's answers on the "Possible typos" sheet
- 29 thread-size typos: OMi confirmed every proposed correction ("Yes it should be 1/2-14", etc.). `scripts/typo_check.py`: all 28
  of them that are in a live review table already carry the corrected thread (2501-LL-24-24-FG is only in the wave-1 FOLDS staging)
  - nothing to change; OMi's website file is what is wrong.
- "NPFT" written 234 times - OMi: "Why is this an issue?" (answer for the user: NPFT is not a thread name; customers and search
  filters looking for NPTF miss those parts. Cosmetic for the CAD library.)
- "Male Metric O-Ring Boss" with inch threads on 186 rows - OMi: "Okay".
- Pipe swivel ends written as NPTF (229 rows) - OMi: "Not sure, what does this mean". OMi's own drawings for 1405 / 1502 / 1504 /
  1602 now call the swivel thread NPSM (e.g. "3/8-18 NPSM"), so for those families the website "NPTF" on the swivel side is the typo;
  the tables already model NPSM.
