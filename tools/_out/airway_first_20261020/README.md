# Air-Way first (OMi, 2026-10-20) - STAGED, not shipped

## The decision
- OMi (Triveni, email 2026-10-20, with the "Review of Drawings" / "Review of Drawings #2" PDFs): "AW means Airway. BI means Brennan
  Industries. We will prefer to use Airway over Brennan dimension when Airway has them available."
- Asked the same day: "Should Air-Way also replace the numbers on your own website parts file, which match Brennan's, or only values we
  took straight from Brennan's catalogs and 3D files?" - **Triveni: yes** (the website file too).
- New source order for DIMENSIONS: **Air-Way first** where it prints a value; then OMi's website file / OMi's own answers; then Brennan
  (catalog / 3D file, marked `$PRP@DimSource` BRENNAN). Reverses the 2026-09-25 order (OMi file > Air-Way). Geometry (end shapes, forged
  bodies, nuts, ports) still from the Brennan STEPs (shape only).
- The two review PDFs themselves are NOT in the repo yet (they are on the PC, `Downloads`). Their AW / BI marks per dimension still have
  to be read against this stage.

## What this stage does
Every review-table cell that holds an OMi-file value where Air-Way prints a different value goes back to Air-Way.

| | |
|---|---|
| Cells reverted | **319** in 26 review tables, 235 rows (`revert_list.csv`, log `stage/CHANGES.csv`) |
| Configurations whose SW2 row changes | **233** (built masters) |
| Roots to rebuild | 25: 0318 0403 1404 2404 2501 (+2501L rows) 2503 2605 2705 2706 5500 5502 6400 6401 6402 6404 6405 6408 6410 6500 6501 6502 6503 6504 6505 6506 |
| Configurations lost | 0 |
| Held (kept at the OMi value, user decision) | 7 cells (`revert_excluded.csv`) |

Sources of the list (`scripts/build_revert_list.py`):
1. `checks/aw_audit.csv` (`scripts/audit_vs_airway.py`): every BUILD cell compared with Air-Way's raw extract `07_RAW_EXTRACTS/<root>.csv`
   by column name; 264 cells differ where the row's source note names OMi / A19 / A20 (259 reverted after the exclusions below). The revert
   value is the raw Air-Way value (cross-check: the 239 cells whose "(table had X)" log has a raw extract all equal it).
2. 6401 / 6405 / 6408 / 6500 have no Air-Way raw extract in the repo: the value comes from the change log ("(table had X)",
   "A19...: COL X -> Y"). **Re-check those 58 cells against the Air-Way pages on the PC.**
3. 2404 (table `2404_FINAL`): 2 overall lengths (question 26).
- Not reverted: cells OMi filled where Air-Way has no value (180), rounding-only differences (<= 0.005 in), the 2 garbled Air-Way bores of
  6504-06-08 (".030" / ".039"), Brennan-only rows (Air-Way has nothing there).

DataStatus: unchanged (rows go back to their Air-Way state; VERIFIED-LEGS / -CORE rows were verified on their Air-Way values), except
6500-08-06-FG, whose logged OMi downgrade is undone (back to VERIFIED). Task A (2026-09-25) rows stay ASSUMED: their status before Task A
is only on the PC (`tools\_out\omi_apply_20260925\originals_before_apply`). Every reverted cell carries the OMi / Brennan value in
`$COMMENT` and `$PRP@AxialSource`.

## Held for the user (`revert_excluded.csv`) - Air-Way's value cannot be built
- **6405-24-16-O** L31: Air-Way L 1.00 is shorter than the 1-NPTF pocket (1.14) - the generator blocks it (it was blocked before Task A
  too). Its D3 is held with it.
- **6504-24-24** D1: Air-Way bore 1.38 >= the -24 JIC tip diameter 1.381 - blocked.
- **6565-10-10** C3 nut hexes: Air-Way 0.94 vs the Brennan -10 swivel nut (1.000) the nut shape is measured from - no end data.
- 6504-06-08 D1 / D2: Air-Way prints ".030" / ".039" (garbled).
These three configurations exist only because Task A gave them OMi values. Options: keep them at OMi (as staged), or drop them back to
MISSING / blocked.

## Look at before shipping (`checks/look_at.csv`, 42 cells)
Air-Way values that move by more than 0.15 in or that the tables already flagged:
- 6405: 12 cells where the table says "D equals tap drill ... column bleed suspected, as-printed" (Air-Way's bore column probably holds
  the tap drill), and L31 values the 2026-09 build flagged "Air-Way L31 suspect" (e.g. 6405-32-20-O / -32-24-O 2.00 -> 1.43).
- 5502-20-20-FG / -24-24-FG N 2.38 -> 2.75 / 2.64 -> 3.05 (Air-Way's -FG row is longer than its non-FG row, "unusual").
- 6410-12-08-O L33 1.48 -> 1.09 (the user had approved OMi 1.480 on 2026-10-02 - superseded by OMi's rule), 6410-16-10-O 1.57 -> 1.12,
  6404-06-08 L32 1.58 -> 1.10, 6410-16-16-O L33 1.81 -> 1.97 ("as-printed, likely typo").
These are Air-Way's printed values; the rule says Air-Way wins. Ask OMi about the flagged ones if in doubt.

## Generator change (6410 only)
With Air-Way's bore 0.68 the 6410 reference configuration 6410-12-08-O becomes a deep-bore port (bore >= port minor), which the generator
refuses as a reference. `tools_af/` = the live `tools/` with ONE line changed: `gen_straight2.py` SPEC 6410 `ref='6410-24-20-O'` (also a
measured Brennan STEP). `regen/af_control` proves it changes nothing else: on the live tables every root regenerates identically except 6410,
whose SW2 holds the same 34 rows (reference row first) and whose macro changes only in the reference-geometry block. Deploy `tools_af`
to `tools/` with the ship (back up first).

## Checks (`checks/`)
- `regen/cmp.txt`: the live tools on the live tables reproduce the shipped `03_SCRIPTS` macro and `04_DESIGN_TABLES` SW2 of every root
  (control); stage = `tools_af` on `stage/`.
- `trace.txt`: every changed SW2 configuration is in the revert list (UNTRACED 0); 6405-32-24-O and 6410-32-24-O are reverted but stay
  unbuilt (blocked / held as before).
- `dofcheck_straight.txt` / `dofcheck_tee.txt`: every sketch exactly defined; `allcfg_*.txt`: 0 outline problems; `vbacheck.txt`: all OK;
  `regress.txt`: the old-configuration changes, each one a reverted cell or its derived columns.

## Next (on the PC - SolidWorks)
1. Read the two review PDFs against `revert_list.csv` / `look_at.csv` (any AW / BI mark that disagrees with this stage).
2. Re-check the 58 log-sourced cells (6401 / 6405 / 6408 / 6500) on the Air-Way pages.
3. User: the 3 held configurations; the look-at list (ask OMi or accept).
4. SolidWorks dry runs of the 25 roots (`regen/stage/{straight,tee}/Build_<root>_MASTER.bas` + SW2, `TABLE_PATH` to the regen folder),
   sweep every configuration, compare with the current masters (unchanged configurations identical).
5. Ship as batch 18: macros + SW2 + the 26 review tables from `stage/04_DESIGN_TABLES`, deploy `tools_af`, RUN_ME_batch18.txt, QA_Log,
   coverage, PROJECT_STATUS. The 2026-10-09 / 10-08 dimension-check drawings of these roots go stale (6401 drawing: 16 cells).

Scripts (run from the repo root, Linux or Windows): `audit_vs_airway.py <outdir>`, `build_revert_list.py`, `apply_airway_first.py`
(rebuilds `stage/` from the live tables), `regen.py`, `run_checks.py`, `flag_suspect.py`.
