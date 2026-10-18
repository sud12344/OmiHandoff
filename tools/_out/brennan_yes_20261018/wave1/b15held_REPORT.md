# Batch-15 HELD rows after Q-BRENNAN-ONLY = YES (2026-10-18)

The user ruled on 2026-10-18: "yes use brennan but still differentiate the two in tables in case i need to change it later". This
report turns the 2026-10-02 proposals for the batch-15 HELD rows into a list of cells for **today's** base tables
(`brennan_yes_20261018/base_root/04_DESIGN_TABLES`). No review table was edited. The main session applies the cells.

**Result:** 25 rows were enumerated (`unblock_20261008/rows.csv`, source == B15-HELD).
- **23 rows are ready.** All 23 became configurations in the generator test, and none was blocked.
- **2 rows stay held:** 2408-14-SOLID and 6801-05-05-NWO-FG. Both are conflicts that need the user, not missing data.
- **0 rows** already had ASSUMED / VERIFIED status with full data, so none was skipped for that reason.

## Files
- `b15held_cells.csv`: 359 cells.
  - 69 `brennan-dim`: a size from the Brennan TFA catalog alone.
  - 174 `endlib`: a thread major, JIC chain, NPTF end or thread text from the generator end libraries (Q-TRANSFER-ENDLIB yes).
  - 116 `other`:
    - 92 are status / marker cells, 4 per ready row: `$PRP@DataStatus` ASSUMED, `$PRP@DimSource` BRENNAN, `$PRP@AxialSource`
      starting with `[BRENNAN-ONLY 2026-10-18]` (old text kept after "| before:"), and `$COMMENT`. These 4 columns are the only
      non-empty base cells in the list.
    - 20 are OMi dimension-file values for the 6504 rows.
    - 4 are 6504 `$PRP@TubeOD` values (OMi Side 1 / Side 2 Size).
- `b15held_rows.csv`: one line per held row (ready, missing columns, conflicts, notes).
- `b15held_test/`:
  - `scripts/make_cells.py`: builds the cell list. It re-reads every value from its source and stops if a 2026-10-02 proposal value
    differs.
  - `scripts/apply_and_test.py`: applies the cells and runs the generators.
  - `root/` (base + cells) and `base_copy/` (untouched base).
  - `gen_base/`, `gen_test/`: macros, SW2 tables, summaries and run logs (batch-16 tools `puckfix_20261009/tools_new`).
  - `compare.txt`, `held_row_results.json`, `applied_cells.txt`, `checks.txt`.

**Apply note:** no base table has a `$PRP@DimSource` column yet. The test appended it at the end of header row 2 in 2406, 5404,
5406P, 5600, 6504 and 6600. Generators ignore the column (marker_test).

## Re-check of the sources
- **Brennan values.** Every one was re-read from `catalog_verified.json`: exactly one catalog row per part number, and no row has a
  parse warning.
- **Agreement with the 2026-10-02 proposals.** Every proposal cell matched today's source, so none was dropped. The one deliberate
  change is 5406P, where the Brennan value as printed (0.562 / 0.438 ...) is used instead of the Air-Way alias value (0.56 / 0.44),
  because the alias is not settled (Q-NEW-AWALIAS). The two agree to rounding.
- **Empty target cells.** Every target cell is empty in today's base, apart from the 4 status / marker columns.
- **Threads.** Catalog thread callouts equal the end-library thread for the part-number dashes on every row.
- **Column mapping.** Checked on the built rows of each table against the catalog:
  - Hex and bore columns match to rounding.
  - 5600 legs match exactly (6 of 6).
  - 6600 M1 / M2 / M5 match exactly.

## Per table
| Table | Rows | Ready / config | Held | Sources |
|---|---|---|---|---|
| 2406 | 2406-04-02, -04-04, -04-08, -06-10, -08-08, -10-16, -12-04, -12-12 | 8 / 8 (40 -> 48) | 0 | L23 / HEXB / D3: TFA p7 TFA-p007-t03 L0 / C HEX / B2 DRILL. JIC: gen_straight2 JIC[d] |
| 5404 | 5404-16-04, -20-12, -24-12, -32-12, -32-16 | 5 / 5 (25 -> 30) | 0 | L / HEXB / D1 / D2: TFA p11 TFA-p011-t04. NPTF ends: ms51500 + ENDL |
| 5406P | 5406-P-02, -04, -06 | 3 / 3 (4 -> 7) | 0 | L2 / C2HEX: TFA p67 TFA-p067-t03 (Air-Way alias rows 5406-02P/-04P/-06P agree to rounding) |
| 5600 | 5600-20-20-20-FG, -24-24-24-FG | 2 / 2 (6 -> 8) | 0 | N1-N3 / Y / D1-D3: TFA p55 TFA-p055-t01. Majors: pipe OD |
| 6504 | 6504-04-06, -06-04, -08-10, -12-16 | 4 / 4 (10 -> 14) | 0 | L14 only from TFA p17 TFA-p017-t05 L. L13 / CHEX / C3HEX / D1 / D2 from OMi Items (= catalog to rounding) |
| 6600 | 6600-24-24-24-FG | 1 / 1 (9 -> 10) | 0 | D3 only: TFA p57 TFA-p057-t01 A3 DRILL 1.312 |
| 2408 | 2408-14-SOLID | 0 | 1 | conflict, see below |
| 6801 | 6801-05-05-NWO-FG | 0 | 1 | question 25, see below |

Test (`compare.txt`):
- Each of the 23 ready rows becomes a configuration, and 0 are blocked. The only blocked row in these roots is the old
  2406-16-04, which is blocked in the base generation too (port wall).
- Every configuration that existed before has identical SW2 cells in all columns: 2406 40, 5404 25, 5406P 4, 6504 10, 5600 6,
  6600 9, 2408 15, 6801 35.
- The macros differ only in the configuration-count check and, for 2406 / 5406P / 5600, in the extreme-size sample configurations
  (now 2406-04-02, 5406-P-06 and 5600-24-24-24-FG).
- `checks.txt`: allcfg, vbacheck and dofcheck all pass (0 outline problems; fully defined; 0 redundant).
- Warnings on new configurations:
  - 5600-20-20-20-FG: the male NPTF end stands 0.023 proud of the hex flats.
  - 5600-24-24-24-FG: the same, by 0.018. This is the known class; the 2026-10-02 sandbox gave the same numbers.
  - 2406-12-04: the female port reaches into the male thread zone, with a radial wall of 0.035 (OK).
- 6504 consistency: OMi L13 minus Brennan L14 equals the Brennan-measured swivel NOSETIP within 0.01 (0.38 / 0.34 / 0.50 / 0.59 vs
  0.38 / 0.35 / 0.50 / 0.60), and the nut hex equals SWIV_MEAS AF.

## Conflicts (none picked)
1. **2408-14-SOLID, HEXB@HEX:** the base holds Air-Way 1.125. Brennan TFA p66 C HEX gives 1.250, which equals MS51518D 1 1/4;
   Air-Way's 1.125 is below the 1.1875 thread major. The base cell is not empty, so Brennan's value is not proposed. Row HELD for
   the user (Q-CONFLICT-2408-14-SOLID / Q-NEW-CATRANK). To fix together with the answer:
   - THDMAJ_B@DRIVE = 1.25 is a column-shift error (JIC -14 major = 1.1875).
   - `$PRP@AxialSource` = "VERIFIED" is shifted text.
   - The unlabeled column holds the "RESOLVED 2-1" vote text, which is a majority vote.
2. **6600-24-24-24-FG, M10@DRIVE:** Air-Way 1.86 vs Brennan M4 1.870. Air-Way is kept (OMi / Air-Way ahead of Brennan), the
   difference is written in `$COMMENT`, and the row is still ready. On the other 6600 rows with a catalog match, Air-Way M10 is 0.01
   above Brennan M4 (0.02 on 6600-20-20-20-FG); only this row is below it (-0.01).
3. **6801-05-05-NWO-FG** (not a cell conflict): LEG_ORB 1.13 (Air-Way = Brennan p40 M7 = Brennan STEP) vs MS51527G / 29D / 30D
   1.090. This is question 25 of 2026-09-26. Q-BRENNAN-ONLY = yes does not answer it, and taking 1.13 because two sources agree
   would be a majority vote. The row has no empty cell. HELD.

## Unclear or for the user
- **2406 lengths.** On the built 2406 rows, which are Air-Way, the table L23 equals Brennan L0 on only 16 of 47 rows; the other 31
  differ by -0.38 to +0.24. The 8 new rows are at Brennan's lengths, so siblings from the two sources may look inconsistent. The
  same holds for 6504, where Brennan / OMi lengths run 0.03-0.09 longer than Air-Way on the built rows; the new 6504 rows use the
  consistent OMi L13 + Brennan L14 pair.
- **6504 marking.** These rows mix OMi values with one Brennan-only cell (L14). They are marked `DimSource BRENNAN` because
  without L14 they would be MISSING, so the undo rule (BRENNAN -> MISSING) is correct for them. The AxialSource text names which
  cell is Brennan's.
- **5406-P-02 / -04 / -06.** If the user confirms the Air-Way alias (Q-NEW-AWALIAS), Air-Way + Brennan would make these rows
  VERIFIED candidates. They are staged ASSUMED / BRENNAN.
- **6600-24-24-24-FG D3.** Brennan 1.312 also settles Air-Way's ".31" (Q-GARBLE) as 1.31 for practical purposes. It is marked
  BRENNAN because the Air-Way print itself was not used.
- **Not done:** SolidWorks dry runs of the 6 changed roots.
