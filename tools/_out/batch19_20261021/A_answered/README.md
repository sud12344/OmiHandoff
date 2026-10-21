# Batch 19, group A: rows whose question was answered on 2026-10-18 (STAGED, not shipped)

26 rows (BLOCKED_NEEDS 2026-10-20 section (d), 25 rows, plus 6506-12-14). Base = the live batch-18 state (`04_DESIGN_TABLES`, `tools/`).
Nothing in `04_DESIGN_TABLES`, `03_SCRIPTS`, `11_MASTERS`, `01_MASTER_DATA` or `tools/` was changed. SolidWorks was not used.

**Result: 23 of the 26 rows now generate. 3 stay blocked (2705-04-02, 2705-LN-04-02, 6506-12-14). No old configuration changed.**

## Why the rows did not generate (live generator on an unedited copy, `gen_before/`)
All 26 were skipped by the same gate: `$PRP@DataStatus` = MISSING (`gen_straight2.build_rows` / `gen_tee` skip MISSING rows before they
look at any cell). Behind that status:
- 2705 / 2706 / 6504 / 6506 / 6503-FG / 6405-32-16-O: the rows were empty (no Air-Way row). The OMi website file has the sizes; what was
  missing was the per-size transfer (I1 = A8, tap drill = A1, swivel offset = A12, -LN = A10).
- 6410-20-06 / -20-08 / -32-12 / -32-16-O: OMi's 2026-10-18 answer had filled them, but they were held for Q-BOREWIDE (D@BORE empty: OMi's
  bore is wider than the port drill) and, at -32, the groove width.
- 6410-32-20-O / -32-24-O: every cell was there already (the A11 edits from `edits_A11.csv` were in the live table); only the status was
  still MISSING.

## What was changed (`CHANGES.csv`: 251 cells in 23 rows, 7 review tables; `checks/table_diff.txt`: nothing else differs)
Edited copies are in `root/04_DESIGN_TABLES/` (DesignTable_2705 / 2706 / 6405 / 6410 / 6503 / 6504 / 6506.xlsx). The other files there are
plain copies of the live folder. Script: `scripts/apply_edits.py`. It asserts that every value cell was empty before. Text cells are only
appended to. DataStatus changes only from MISSING.

Source order used (CLAUDE.md, 2026-10-20): Air-Way first. Air-Way prints none of these 23 parts except the plain twin of 2706-LN-08-06. So
the sizes come from OMi's website file (`07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx`, sheet Items, row numbers below). Then
come the user's 2026-10-18 per-size transfers. End details (thread majors, ORB / pipe / swivel ends) come from the generator end libraries
(Q-TRANSFER-ENDLIB). The Brennan TFA catalog (`tools/_out/brennan_catalog_20261001/parsed/catalog_TFA.csv`) is used only as a cross-check.
No cell takes a Brennan-only value, so no row is marked BRENNAN. Where the table has a `$PRP@DimSource` column, rows filled from OMi get
`OMI` (as on 2705-06-04). 6503 / 6506 have no such column, and none was added; their source is written in `$PRP@AxialSource`.
DataStatus: every generated row is **ASSUMED** (OMi = Brennan's data = one source, plus transfers).

| Row | Generated | Edits and sources |
|---|---|---|
| 2705-LN-06-04 | yes | L24 2.19 / hex 0.875 / D 0.172 = OMi Items row 1059 (its own -LN row, equal to the plain 2705-06-04 row 1045). I1 1.20 = Air-Way -04 bulkhead (A8). Tap drill 0.57 = Air-Way -06 (A1). Thread majors from the end library. Modelled as the plain part, no locknut (A10). |
| 2706-06-04 | yes | L25 2.19 / hex 0.75 / D1 0.406 / D 0.172 = OMi row 1073. I1 1.20 (A8). Not in the Brennan catalog. |
| 2706-LN-06-04 | yes | Same as 2706-06-04, from OMi row 1088 (equal values). A10. |
| 2706-32-32 | yes | L25 3.91 / hex 2.75 / D1 1.938 / D 1.781 = OMi row 1083 (= Brennan TFA p9, all equal). I1 2.09 = Air-Way -32 bulkhead (2700-32-32, the only Air-Way -32 bulkhead; A8). |
| 2706-LN-08-06 | yes | **Copy of the plain twin 2706-08-06 (A10). Its values are Air-Way's** (2706.csv line 12): L25 2.34, I1 1.28, hex 0.88, D1 0.53, D 0.30. OMi's own -LN row (2.400 / 0.875 / 0.531 / 0.295) and Brennan's L 2.410 are not used, because Air-Way prints the part (Air-Way first), the same as on the plain twin. No DimSource mark (Air-Way). |
| 6405-32-16-O | yes | L31 1.43 / hex 2.75 / D3 1.08 = OMi row 1805 (L and hex = Brennan p16). Tap drill 1.14 = Air-Way -16 (A1). FPT_P1 1.14, and the -32 ORB end (2.5 / 0.469 / 2.381) from the end library, as on 6405-32-24-O. ORB_GRVW left empty on purpose (see below). **D3: OMi 1.080 vs Brennan B DRILL 1.156 (Q-CAT-6405-32-16-D3). OMi kept by the source order.** Generator note: "AS-PRINTED WARNING: port drill depth P1 1.14 leaves only 0.290 to the far tip" (OMi's L = Brennan's L 1.430). It builds as printed. |
| 6410-20-06-O / -20-08-O | yes | D@BORE = the port drill D3 0.50 / 0.68 (A11 cap; OMi 0.509 / 0.689 is wider; report to OMi). MISSING -> ASSUMED. |
| 6410-32-12-O / -32-16-O | yes | D@BORE = D3 0.97 / 1.22 (A11 cap; OMi 0.981 / 1.231). The -32 groove width 0.125 comes from the generator library (A18). MISSING -> ASSUMED. |
| 6410-32-20-O / -32-24-O | yes | Status only: MISSING -> ASSUMED. The A11 cells were already in the live table. The groove comes from the library (A18). 6410-32-24-O: deep bore, radial wall 0.255 at the port bottom (generator: OK). |
| 6503-04-04-FG | yes | N1 0.88 / M5 1.18 / M10 0.836 / nut 0.563 / Y1 0.75 / D 0.172 = OMi row 1975. The column reading (L 1 / M 2 / M 1) is the one the user accepted on 6503-08-08-FG (A19 group 3). Brennan p38 is equal or differs by rounding only. Tap drill 0.43 (A1). The plain Air-Way 6503-4-4 is not used for the forged part. |
| 6503-12-12-FG | yes | N1 1.36 / M5 1.86 / M10 1.298 / nut 1.25 / Y1 1.312 / D 0.609 = OMi row 1980 (Brennan p38 is equal or differs by rounding only). Tap drill 0.91 (A1). gen_tee warning: "leg 2 hex arm 0.771 barely clears the corner puck (0.757)". It is the same kind of warning as on the built 6503-08-08-FG. |
| 6504-08-12 / -10-08 / -10-12 / -12-10 / -16-20 | yes | L13 / hex / nut hex / D1 / D2 = OMi rows 1993 / 1994 / 1996 / 1998 / 2003. **L14 = L13 - the swivel offset (A12)**. The offset is the end library's value per size, gen_straight2 `SWIV_MEAS[dash]['NOSETIP_B']` (Brennan 6500-FG STEPs): -08 0.43, -10 0.50, -12 0.57, -20 0.64. Air-Way prints 0.42 / 0.49-0.50 / 0.56-0.57 / 0.62-0.63. So L14 = 1.53 / 1.54 / 1.75 / 1.71 / 1.97. |
| 6504-32-32 | yes | L13 3.80 / hex 2.625 / nut 2.875 / bores 1.781 = OMi row 2007. L14 = 3.80 - 0.95 = 2.85 (A12; Air-Way 0.94). **The Brennan catalog row is inconsistent** (L 3.700 / L5 2.862, seat beyond the nut face; Q-CAT-6504-32-32-L). It is not used. OMi is kept by the source order, and OMi's L13 minus the offset agrees with the catalog's 2.862 within 0.012. |
| 6506-06-04 / -06-10 / -12-08 | yes | L17 / L18 / hex / nut hex / D = OMi rows 2035 / 2038 / 2042. The reading is Q-B-SWSTR, settled by the Brennan p18 letters in batch 15. -06-04 and -06-10 are equal to Brennan p18. Tap drill 0.57 / 0.57 / 0.91 (A1). **6506-06-10: OMi's thread text says "1/2- 14 NPTF", a misprint.** OMi's own Side 1 Size (3/8), the part number and Brennan p18 all give 3/8-18, so that thread is used. |
| **2705-04-02** | **no** | Needs a user decision (or a new source) for I1 at the -02 bulkhead. Air-Way has no -02 bulkhead (A8 cannot apply). OMi gives none. Brennan has no file for this part. The two Brennan -02 bulkhead STEPs disagree: 2700-02-02 = 1.07 (built in 2700), 2706-04-02 = 1.11 (built in 2706). Picking one is a choice between sources. The other cells are ready, unchanged here, in `tools/_out/brennan_yes_20261018/wave2/straight/cells.csv`: L24 2.0 / hex 0.75 / D 0.062 (OMi row 1042), tap drill 0.43, THDMAJ 0.54 / 0.3125. |
| **2705-LN-04-02** | **no** | Same blocker (A10: = the plain 2705-04-02; OMi row 1056 gives the same sizes). |
| **6506-12-14** | **no** | (1) **Generator data change needed**: there is no -14 female JIC swivel in `SWIV_MEAS` (KeyError "female JIC swivel end not measured for -14"). The part's own `09_STEP_FILES/BRENNAN_6506-12-14.stp` is on disk. But `tools/measure/swiv.py` fails on it: "swivel chain not found ... no body face / neck pair behind the nut". The extractor finds the chain on the 6500 elbows only (control: 6500-12-12-FG = SWIV_MEAS[12], ALL MATCH; `measure_6506-12-14/swiv_out.txt`). It needs a straight-body mode before `SWIV_MEAS[14]` can be added. (2) **Then a decision on L17 / L18**: Air-Way prints L18 1.51 and leaves L17 blank. OMi gives 2.340 / 1.750 (= Brennan p18 L5 2.33 / L2 1.75). Air-Way-first L18 1.51 with OMi L17 2.34 puts the nose 0.83 inside the nut, a shape no source has. The options are Air-Way L18 + the -14 offset (A12, from the new SWIV_MEAS[14] or Air-Way's own 0.56 / 0.58), or the OMi / Brennan pair (Air-Way's 1.51 treated as unbuildable, user Q1). No cell was edited. |

### Logged assumptions (in `$PRP@AxialSource` of the rows)
- A12 "the end library's value per size" is read as `SWIV_MEAS NOSETIP_B` (Brennan-measured nose tip from the nut face). It is the only
  single per-size offset the library holds. The 2026-10-01 catalog notes call it that ("Brennan STEP NOSETIP_B 0.57"). Air-Way's
  offsets differ by 0.00-0.02. **Please confirm this reading.** The other reading would be one of Air-Way's printed offsets.
- -LN rows keep OMi's part-number form in `$PRP@PartNo` (2705-LN-06-04, 2706-LN-06-04, 2706-LN-08-06), as on the shipped 2706-LN-04-02.
  Because of this, the generator does not add "(with bulkhead locknut - locknut not modelled)" to their Description (it tests
  `pn.endswith('-LN')`). This changes the description text only. A one-line generator change, matching `-LN-` too, would fix it and the shipped
  2706-LN-04-02. It was not made.
- ORB_GRVW stays empty on 6405-32-16-O and the four 6410 -32 rows. Filling it would make the row feed `ORB[32]` and change the source
  text of the other -32 configurations. The generator applies the library 0.125 (A18) and writes it into SW2.

## Verification (`checks/`)
- Control (`gen_before`, unedited copy): every one of the 7 roots reproduces the live SW2 (all cells) and the live `03_SCRIPTS` macro
  exactly, ignoring line endings and "generated" lines (`compare.txt`).
- After (`gen_after`, edited copy): configurations 2705 18->19, 2706 25->29, 6405 44->45, 6410 34->40, 6503 1->3, 6504 14->20,
  6506 14->17 (+23). **Every old configuration is identical in every SW2 cell, with the same columns and order** (`compare.txt`,
  `regress.txt`). The macro differences are only the expected configuration count, the extreme-size check rows (`cx_c` / `cx_w`), and for
  6410 the deep-bore list `db_*` with the 6 new rows. The old rows keep their values.
- `dofcheck_straight.txt` / `dofcheck_tee.txt`: every sketch exactly defined, 0 redundant. `allcfg_s.txt` / `allcfg_t.txt` (OMI_ROOT =
  `root`): 0 outline problems in every configuration. `vbacheck.txt`: all 7 macros OK.
- Cross-root effects: no other generator root reads these 7 review tables, except the ORB library loop over 6401 / 6405 / 6410, which
  needs ORB_GRVW and is untouched. So no other macro changes.

## Not done / next
- SolidWorks dry runs of the 7 roots (`run_macro` with SAVE_PATH / REPORT_PATH overrides, then sweep_configs and geometry). Watch these:
  6503-12-12-FG (corner puck), 6405-32-16-O (short port wall), 6410-32-24-O (deep bore, thin wall), 6504-32-32.
- Ship: copy the 7 review tables, the regenerated SW2 and the macros (`gen_after/`), then QA_Log and PROJECT_STATUS.
- Tell the user / OMi: D3 1.080 vs Brennan 1.156 on 6405-32-16-O; 6504-32-32 catalog row; the OMi 6506-06-10 thread misprint; the A11 caps
  (6410 x4: OMi bore wider than the port drill); the A12 offset reading.
- User decisions: I1 at the -02 bulkhead (2705-04-02 / -LN-04-02); 6506-12-14 L17 / L18, after the SWIV_MEAS[14] measuring work.
