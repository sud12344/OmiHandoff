# Batch 19 group D_geom: geometry / Brennan-cell rows (staged 2026-10-20, NOT shipped)

Nothing live was touched: `04_DESIGN_TABLES`, `03_SCRIPTS`, `11_MASTERS`, `01_MASTER_DATA` and `tools/` are unchanged, and SolidWorks was not
used. Every edit is in the copy `root/04_DESIGN_TABLES` (= live 04_DESIGN_TABLES after batch 18, copied 2026-10-20, plus the cells in
`CHANGES.csv`). The untouched copy is in `orig_tables/` and `orig_root/04_DESIGN_TABLES`.

**Result: 13 of the 14 rows generate. 5503-02-02-FG is still blocked. No generator patch was needed (`patches/` is empty).**

## Rows

| # | Row | Before (live) | What was done | Now |
|---|---|---|---|---|
| 1 | 2406-16-04 | BLOCKED: wall -0.009 between the -16 female JIC port and the -04 male thread root, at 0.550 from the male tip | This is a real geometry clash, not a generator limit. With Air-Way's L23 1.67, the Brennan-measured -16 female port (JICF_MEAS[16]) and its 37 deg seat run into the -04 male end. User rule Q1 applies: **L23 = Brennan 1.840** (TFA p7, TFA-p007-t03 "L0 LGTH"). L23 and L0 are the same overall length: they agree to rounding on 25 of the 56 2406 rows Brennan prints. | generates |
| 2 | 6502-16-12-FG | MISSING, no data | OMi's file prints all 7 sizes (Items row 1969: M2 1.47, M6 1.70, M14 1.14, nut hex 1.25, flats 1.312, bores 0.844 / 0.609). Brennan's TFA p35 row prints the same 7 values. Air-Way has no row. Column mapping Q-B-SWELB, same as the batch-15 row 6502-10-08-FG. Set ASSUMED (OMi = Brennan data, one source). | generates (generator raises the hex 1.312 to the thread major 1.3125, 2603HX rule, as on every 6502 -16 row) |
| 3 | 5501-24-24-FG | MISSING | OMi Items row 1456 (= Brennan TFA p31 on all 5 values). NPTF majors from the end library. The angled-helix gate has been closed since batch 17. Set ASSUMED, DimSource OMI. | generates |
| 4 | 5501-32-32-FG | MISSING | OMi Items row 1457 is the only source (Brennan's catalog table ends at -24). Set ASSUMED, DimSource OMI. | generates |
| 5 | 5503-02-02-FG | BLOCKED: "leg 1: port depth P1 0.46 >= leg length 0.47" | The angled helix is no longer what blocks this row. The block now is the female 1/8 NPTF port: the only depth source is the MS51503 P1 library value, 0.46, which fills the 0.47 female leg (Air-Way N3 0.47 = Brennan N1 0.470). Q-ANGLED-P1 is answered per size from Brennan STEPs (ANGLED_P1_NOTE), but no Brennan STEP on disk has a -02 female NPTF port (checked: 1404-02-02, 2700-02-02, 2701-02-02-FG, 2706-04-02, 6410-04-02-O, 6500-02-02-FG, 6801-04-02-NWO-FG). No sourced value exists, so nothing was changed. | **still BLOCKED.** Needs BRENNAN_5503-02-02-FG.stp, or another Brennan part with a 1/8 female NPTF port such as 5405-02-02. The alternative is for the user to choose the other Q-ANGLED-P1 option, "cap the port at leg - 0.05" (a logged assumption). |
| 6-8 | 1504-08-08-FG, 1504-12-12-FG, 1504-16-16-FG | MISSING (wave 3 had no 1504 SPEC). Values were already staged and equal the Brennan TFA p22 row on every cell. | DataStatus set to ASSUMED. On the first regen, -08 and -16 blocked: "port depth P1 0.9 / 1.14 >= leg length 0.94 / 1.19". Added PORTDEPTH@BORE from Brennan's measured port depths: -08 = 0.75, -16 = 0.94 (ANGLED_P1_NOTE, `genfeat_20261018/angled/scripts/brennan_port_depths_out.txt`; same mechanism as 5503-04-04-FG). -12 fits the library depth and is unchanged. Flag kept: OMi's drawings of sibling sizes print the stem bore 0.01-0.02 below Brennan's drill. | generate |
| 9-10 | 6807-16-16-NWO-FG, 6807-20-20-NWO-FG | MISSING (no 6807 SPEC in wave 3). Values were already staged and equal Brennan TFA p44. | DataStatus set to ASSUMED | generate |
| 11 | 2408-14-SOLID | MISSING (hex conflict) | **HEXB = Brennan 1.250** (TFA p66 "C HEX"; also MS51518D 1 1/4). Air-Way's 1.125 is smaller than the part's own 1 3/16-12 thread. Also repaired the 2026-09 column shift: THDMAJ_B 1.25 -> 1.1875 (JIC[14]), and AxialSource "VERIFIED" replaced by real sources. The unlabeled "RESOLVED 2-1 ... outvoted" note now starts with "SUPERSEDED". DataStatus ASSUMED, as the batch-15 proposal had it. It could be VERIFIED if you count Brennan + MS51518D as two sources. | generates |
| 12 | 1501-24-24-FG | BLOCKED: Air-Way nut 1.88 vs the Brennan -24 NPSM nut 2.125 | **CHEX = Brennan 2.125** (TFA p20 "C HEX"; Air-Way's own non-FG 1501-24-24 prints 2.13) | generates |
| 13 | 6802-04-06-NWO-FG | BLOCKED: locknut 0.56 cannot fit the -06 ORB thread | **HEXB = Brennan 0.688** (TFA p41 "C HEX" as printed; it is within the generator's 0.007 tolerance of the measured 0.6875) | generates |
| 14 | 1501-04-02-FG | BLOCKED: bore 0.23 >= the -02 stem tip (dia 0.234) | **D = Brennan 0.13** (TFA p20 "A2 DRILL"; Air-Way's own non-FG 1501-04-02 prints 0.13) | generates |

## Brennan cells used under user Q1 ("Air-Way value not buildable -> Brennan")

Each value was confirmed in the page-verified catalog extract `tools/_out/brennan_catalog_20261001/catalog_index.json` (every entry `verified=True`).
The cells follow the batch-18 format: `$PRP@DimSource` = BRENNAN (the 2408 and 6802 tables got that column) and
`[BRENNAN-CELL 2026-10-20: <col>]` at the start of `$PRP@AxialSource`.

| Row | Cell | Air-Way | Brennan | Catalog |
|---|---|---|---|---|
| 2406-16-04 | L23@DRIVE | 1.67 | 1.840 | TFA p7 TFA-p007-t03 "L0 LGTH" |
| 2408-14-SOLID | HEXB@HEX | 1.125 | 1.250 | TFA p66 TFA-p066-t05 "C HEX" |
| 1501-24-24-FG | CHEX@HEX | 1.88 | 2.125 | TFA p20 TFA-p020-t01 "C HEX" |
| 6802-04-06-NWO-FG | HEXB@HEX | 0.56 | 0.688 | TFA p41 TFA-p041-t02 "C HEX" |
| 1501-04-02-FG | D@BORE | 0.23 | 0.13 | TFA p20 TFA-p020-t01 "A2 DRILL" |

Other Brennan-sourced values, not Q1 cells:
- The 1504 / 6807 rows were already marked BRENNAN-ONLY / DimSource BRENNAN on 2026-10-18. Only their DataStatus changed.
- The two 1504 PORTDEPTH values come from measured Brennan STEPs (Q-ANGLED-P1).

## Tables changed (in `root/04_DESIGN_TABLES` only)
- DesignTable_1501, 1504, 2406, 2408, 5501, 6502, 6802, 6807.
- 80 cells: `CHANGES.csv` has 82 lines; two 1504 AxialSource cells were edited twice.
- Columns added: `$PRP@DimSource` in 2408 and 6802, `PORTDEPTH@BORE` in 1504.
- The cell-by-cell diff against the live tables (`checks/diff_tables.txt`) shows exactly the CHANGES.csv cells and nothing else.

## Checks (`checks/`)
- `regress.txt`: the live generators on the unedited tables reproduce the shipped `04_DESIGN_TABLES` SW2 tables of all 9 roots (0 changed cells). Edited vs unedited: every old configuration is identical in every column (`diff_base_vs_new.txt` also compares every SW2 row in full). Configurations: 1501 19->21, 1504 3->6, 2406 51->52, 2408 15->16, 5501 7->9, 5503 6, 6502 12->13, 6802 20->21, 6807 1->3 (**+14 configurations, 13 parts**: 2408-14 is one config; 1504-12-12-FG counts here too).
- Macro diffs (`diff_base_vs_new.txt`): only the configuration-count Check line, the extreme-size sample arrays (`cx_c` / `cx_w`), and new `HelixUCheck` lines for the new angled-thread rows (1504, 5501).
- Regen-all (`regen_all_orig_vs_edited.txt`): all 165 roots, live generators, unedited vs edited tables. Exactly the 8 edited roots change; the other 157 are identical: same macro, same SW2 table and byte-identical generator log (roots that write no macro write none either way). So no other root reads these tables as a library.
- `new_dof_*.txt`: dofcheck_straight / dofcheck_tee give every sketch fully defined, output identical to the unedited macros. The 5501 / 5503 THDPROF "redundant 1, same_as_HelixThread" note is in the unedited output too.
- `new_allcfg_*.txt`: every configuration of the 9 roots has a clean outline (0 problems).
- `new_vba_*.txt`: vbacheck OK on all 9 macros.
- The `base_*` files are the same checks on the unedited macros, kept for comparison. Ignore `base_allcfg_*`: allcfg_check rebuilds from the review tables, so it read the edited tables there too.
- Not done: SolidWorks dry runs (not allowed in this session). Before shipping, dry-run 1501, 1504, 2406, 2408, 5501, 6502, 6802, 6807 on the PC (CLAUDE.md verify loop). Look closely at 5501-32-32-FG (first -32 angled helix) and 1504-08-08 / -16-16 (Brennan port depth on the angled female leg).

## Files
- `CHANGES.csv`: root, table, cfg, column, old, new, source, why.
- `root/04_DESIGN_TABLES/`: the edited tables (plus unedited copies of all the others).
- `regen/base` / `regen/new`: the 9 roots on the unedited / edited tables (macros, SW2 tables, summaries, logs).
- `regen_all/live_orig` / `regen_all/live_edited`: all 165 roots both ways.
- `scripts/`:
  - `apply_edits.py`: builds `root/` from `orig_tables/` and writes CHANGES.csv. It can be re-run and gives the same result.
  - `run_gen.py`, `regen_all.py`: generators.
  - `run_checks.py`, `diff_macros.py`, `diff_tables.py`: checks.
  - `show_rows.py`, `brcat.py` (Brennan catalog lookup), `cmp_cat.py`, `omifile.py`: lookups.
- `patches/`: empty. No generator change was needed.

## To ship (batch 19)
1. Copy the 8 tables from `root/04_DESIGN_TABLES`. Re-read the live ones first in case they moved.
2. Regenerate the 8 roots and run the SolidWorks dry runs.
3. Copy the macros and SW2 tables.
4. Tell the user the 5 Brennan cells listed above.
5. Leave 5503-02-02-FG in (a) "Brennan STEP files to download".
