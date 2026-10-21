# Brennan CAD cells - STAGED 2026-10-21 (user: "stage"), not shipped

Base: the Air-Way-first stage (`tools/_out/airway_first_20261020/stage/04_DESIGN_TABLES`, the batch-18 candidate) and the ORFS stage
tables (`tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES`), copied to `stage/04_DESIGN_TABLES` and `stage/orfs_tables`.
Live `04_DESIGN_TABLES`, `03_SCRIPTS`, `11_MASTERS` and both base stages are untouched.

Source: Brennan's CAD parameter records (PARTcommunity / CADENAS), user 2026-10-21 "yes you can use them following my rule" - Air-Way
first, then OMi's file / answers, then Brennan. Cells: `tools/_out/partcommunity_20261021/decode/verify.csv` (427: each column mapped to a
Brennan code per table AND Brennan family on rows whose values are known; checked against Brennan's printed catalog, the Air-Way row of the
same size and the neighbouring sizes; the 4 flagged cells explained in `scripts/apply_cells.py`).

## What the stage does (`scripts/apply_cells.py` -> `CHANGES.csv`, `rows.csv`; `scripts/promote_test.py` -> `promote.csv`)
- **421 empty cells written** (none of the targets was filled), **6 skipped** as library-driven: the ORB -32 / -14 groove width 0.125 is the
  generator's measured value when the cell is empty (writing it moved the shared ORB library's -32 entry and dropped the "MEASURED on the
  Brennan STEP" note from 6405's -32 rows - found by the regen trace, fixed).
- **103 rows** touched: `$PRP@DimSource` = BRENNAN, `$PRP@AxialSource` prefixed `[BRENNAN-CAD 2026-10-21: <columns>]`, `$COMMENT` names
  the Brennan record and codes.
- MISSING -> ASSUMED (single source) only when every required column is filled (39 rows), or when the generator itself builds the row
  cleanly with nothing else changing (`promote_test.py`, one row at a time: +1, 2501-40-40-FG). 61 rows stay MISSING: their cells are
  staged as data; what still blocks them is not a Brennan cell (below).

## Result (`scripts/regen.py` -> `regen/cmp.txt`; tools_af for non-FS roots, the ORFS staging tools for FS roots; control = the base stage)
- **8 new configurations** (after the A9 tap drills, below): 2408-14-SOLID, 2501-40-40-FG, 2501-LL-08-08-FG, 2706-32-32, 5000-24-20,
  5405-16-24, 5406-40-32, 5503-02-02-FG.
- 0 configurations lost, 0 changed in any root; every new configuration traces to a touched row.
- Checks (`checks/`): dofcheck straight / tee fully defined, 0 redundant (5503 THDPROF_2: 1 redundant = same in control, the helix-thread
  profile); allcfg 0 outline problems (2408 16, 2706 26, 2501 58, 5503 7); vbacheck 34 / 34 macros OK; regress 34 roots, 0 changed cells
  in old configurations.
- Roots with no generator SPEC (cells staged as data only): 2500 2502 2603 (hand-made HX masters, A7), 6805 6809 6900 6901, FS6402 FS6809.

## What still blocks the 61 MISSING rows (promote.csv)
- -24 / -32 female pipe tap drill (A9: "wait for a brennan step") - 5000, 5405, 5406 (incl. 5406-C), 6405, 6506 and the 55xx / 56xx
  forgings: download BRENNAN_5405-24-24 and 5405-32-32 (the two "maybe" files of STEP_MINIMUM.md are needed).
- 6801 / 6802 / 6803 / 6807 / 6606 rows: still skipped by the generator for end data of their own (adjustable-family work, PC list (a)).
- 1502 / 1504 / 2404-L-32-32 / 6404-08-12 / 6502-16-12-FG: generator end-library gaps for those sizes (see the tracebacks in promote.csv).

## To ship (after the user's go)
SolidWorks dry runs of 2408 2501 2706 5503 on the PC (`run_macro` with SAVE_PATH / REPORT_PATH + TABLE_PATH = `regen/stage/...`), then
ship together with (or after) batch 18 - the stage contains the Air-Way-first tables.

## 2026-10-21 (later): A9 tap drills + user decisions
- BRENNAN_5405-24-24 / -32-32 received and measured (`tools/_out/brennan_yes_20261018/a9_tapdrill/measure_5405_20261021.txt`; the -08 check
  reproduces 0.718 / 0.75 / 0.90): -24 tap drill 1.734 (taper 0.94, drill depth 1.16), -32 2.218 (0.97, 1.18). A9: the nearest Air-Way
  value -> -24 1.72, -32 2.20 (PROJECT_STATUS s5).
- `scripts/apply_tapdrill.py` (after apply_cells.py): 116 empty tap-drill cells in 77 not-ready rows = Air-Way per-size value (A1 / A9);
  each table's TAPDRILL column is tied to the dash position its filled rows follow (2609 TAPDRILL2 / 3: no clear position, left alone).
- `map_columns.py`: a code named like the column (L = L@DRIVE) is mapped at >= 75 % agreement (its misses are Air-Way-vs-Brennan
  differences - 5405 L 27/32); other codes keep 90 %. 430 cells verified (426 OK + the 4 explained), 424 written.
- promote_test: 4 rows promoted by the generator; checks over all 39 regenerated roots clean (allcfg 0 problems; dofcheck fully defined,
  only the known 135-deg THDPROF helix redundancy; vbacheck OK; regress 0 changed cells in old configurations).
- Still blocking most of the 79 MISSING rows: single gaps the records do not fill under the mapping rules (e.g. 5504 / 5601 body flats
  W, 6506 L17), the -24 / -32 female-port drill depth P1 in the generator's FPT library (measurable: 1.16 / 1.18 from the two 5405 STEPs -
  a generator change), the adjustable-family end data (6801 ...), and the roots with no generator SPEC.
