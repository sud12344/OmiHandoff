# 6810 hex: the data fix + the gen_tee hex-skip (2026-10-21, cloud) - STAGED, not shipped

Problem: in the Brennan CAD stage (`tools/_out/brennancad_20261021/stage/04_DESIGN_TABLES/DesignTable_6810.xlsx`) row
`6810-12-12-NWO-FG` was ASSUMED / DimSource BRENNAN with `Y@HEX` empty -> `gen_tee.py 6810` (tools_af) stopped the whole root at
`AF = max([Y] + maxes); BR = AF / 2` (TypeError; `brennancad_20261021/regen/cmp.txt`: `6810 [tee] rc 0/1`).
Live `tools/` and live `04_DESIGN_TABLES` are NOT touched.

## 1. Data (the stage table)

Why the row was promoted: `apply_cells.py` takes the "required columns" from the table's shipped rows; 6810 has none, so the list was
empty and MISSING -> ASSUMED went through with Y, M19, M20, C3HEX and THDMAJ_B2 empty.

- **Y@HEX = 1.062** (forged body flats), source rule followed:
  - Air-Way: prints only the plain `6810-12-12 NWO` (Y 1.13). The -FG row already says it does not copy plain dims, and the 6807 / 6809 forged
    Y also came from Brennan's catalog (`apply_cells.py` EXPLAINED), so Air-Way gives no value for this part.
  - OMi file (`WebsitePartsInfo2026.xlsx`): 6810 rows carry names / threads only, no dimension.
  - Brennan: printed catalog TFA p44 `6810-NWO-FG` **Y FLATS 1.062** (`brennan_catalog_20261001/catalog_verified.json`, verified table)
    = CAD record Y 1.062 (`partcommunity_20261021/decode/decode_6810_nwo_fg.txt`, AMBIGUOUS there: GAP or CYL_D)
    = `09_STEP_FILES/BRENNAN_6810-12-12-NWO-FG.stp`: three flat pairs 1.062 apart, 60 deg apart around the ORB axis and the 45 deg axis, the same
    pattern as the 1.250 nut hexes (`step_flats_6810.txt`, `scripts/step_flats.py`). All three are Brennan = one source -> ASSUMED, BRENNAN.
- **DataStatus back to MISSING**: with Y filled the generator stops in `leg_JICSW` (`M5 - M10`, None) - M19@DRIVE / M20@DRIVE (swivel nose /
  nut face) have no settled source (catalog M 0.93 / M6 1.50, but which is M19 and which is M20 is uncertain, `brennan_catalog_20261001/impact/F1b.md`);
  C3HEX@HEX also empty (catalog C2 HEX 1.250, not mapped). No value invented; the row waits for that mapping.
- `scripts/fix_6810_row.py` made the edit (Y, DataStatus, AxialSource tag, $COMMENT note); original in `old_files/`.
  **Re-run it after any re-run of `brennancad_20261021/scripts/apply_cells.py`** (that script rebuilds the stage from the Air-Way-first tables).

## 2. Generator: `gen_tee.py` build_rows skips a row with an empty hex cell

+4 lines before `Y = r[sp['hex']]`: `skipped (pn, 'row without Y@HEX', 'needs the cell before the row can build')`, the wording of the existing
flange-leg skip. Staged in two copies (nothing else differs from their source):
- `tools_af/` = `airway_first_20261020/tools_af` + the patch (the toolset the Brennan CAD stage regenerates with) - `gen_tee_af.diff`
- `tools_b19/` = live `tools/` (batch 19) + the patch (same unguarded line, for the next ship) - `gen_tee_b19.diff`

## 3. Evidence

`scripts/regen_all.py <set>`: every gen_tee + gen_straight2 SPEC root, old vs new toolset, same input; .xlsx compared by cell value (zip time
stamps), stdout with the toolset path and line numbers normalised. `regen/<set>/cmp.txt` (full outputs not kept - regenerate).

| set | old -> new | input | result |
|---|---|---|---|
| af_stage | tools_af -> hexskip tools_af | Brennan CAD stage, fixed 6810 | 101 / 101 roots identical (6810: 0 configs, row skipped as MISSING) |
| af_unfixed | same | the stage with the ORIGINAL 6810 table | 100 identical; **6810 rc 1 -> 0**, the row skipped "row without Y@HEX" |
| b19_live | live tools/ -> tools_b19 | repo (live tables) | 135 / 135 identical |

Roots 6566 / 6603 (tools_af) and 2502 (b19, SPEC_WAITING) fail old and new alike (no SPEC). 1803 = 0 configs old and new.
`scripts/run_checks.sh` -> `checks/<set>/`: dofcheck_tee all fully defined (6 x THDPROF_2 redundant 1 = the accepted HelixThread set,
same_as_HelixThread True); allcfg 0 outline problems (57 tee + 42 straight roots; b19 78 + 55); vbacheck 97 / 131 macros OK; regress 99 / 133 roots,
0 changed cells (1803 / 6810 have no table).

## 4. Same flaw, other rows - FOR THE USER (not changed)

`vacuous_promotions.txt` (`scripts/vacuous_promotions.py`): 37 rows apply_cells promoted with an empty required-column list; 36 of them are still
ASSUMED and 33 of those have empty numeric cells: 6801-L-16/-20 (M11, bores), 6805 x9 (M17, N1, Y1), 6809 x4 (C3HEX, C4HEX, bores), 6900-32-32-O
(W4, L2, D), 6901 x14 (N5, M1, W3, hexes, bores), FS2701 / FS2702 (S4HEX), FS2703 (I4, S4HEX). FS0319-24, FS2503-04-02-FG and FS6402-12-12 have no
empty cell. Some empty cells may be end-library (THDMAJ / ORB_*). Fix the promote rule (no shipped rows -> require every numeric column, or the
SPEC's columns) and re-run, or put these back to MISSING: the user decides.
