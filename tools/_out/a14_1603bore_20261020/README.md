# A14: 1603-08-08-08-FG bores measured on the Brennan STEP and staged (2026-10-20, cloud session)

**Status:** staged in the batch-17 table set. Not shipped. No SolidWorks dry run yet (the cloud cannot run SolidWorks).

## Why
- The Brennan TFA catalog (p.48, table 1603-FG) prints the A1 / A2 drills of 1603-08-08-08-FG as a range, "0.44/0.46". A range is never
  averaged.
- User, A14 (2026-10-18): **"Measure the STEP"**.
- The 2026-10-18 stage held the WHOLE row as a result (every cell empty, MISSING). It was the only one of the six 1603 -FG rows that did
  not generate (genfeat perlegsw: "1603 5/6").

## Measurement (`scripts/cyl_survey.py` -> `cyl_survey.txt`, `scripts/plane_survey.py` -> `plane_survey.txt`)
File: `09_STEP_FILES/BRENNAN_1603-08-08-08-FG.stp` (1 solid). Run = X axis, branch = +Y, crossing at the origin.

| Item | STEP | Catalog (staged cell) |
|---|---|---|
| Run bore (A2 / A3) -> `D2@BORE` | cylinder **dia 0.4500**, x = -1.11 .. +1.11 (stem tip to stem tip) | "0.44/0.46" (range) |
| Branch bore (A1) -> `D1@BORE` | cylinder **dia 0.4500**, y = 0 .. 1.11 (crossing to stem tip) | "0.44/0.46" (range) |
| Stem tips -> M1 / M2_2 / M2_3 | planes at 1.11 on all three legs | 1.110 |
| Nut faces -> W3 / W5_2 / W5_3 | planes at 1.39 (countersink dia 0.823 = NPSM_MEAS[8] CSR 0.4115) | 1.390 |
| Nut hex -> C_1HEX / C2HEX / C3HEX | flats at +-0.500 -> 1.000 | 1.000 |
| Body flats -> C1HEX | flats at +-0.4375 -> 0.875 | 0.875 |

Both bores = **0.450**, inside the printed range. Every other catalog value of the row is confirmed on the same STEP.
(A 0.24 x 0.002 recess at z = 0.4355 and many small faces near it are the stamped marking. They are ignored.)

## What was staged (`scripts/stage_1603_08.py tools/_out/brennan_yes_20261018/stage`)
- **Table:** `tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES/DesignTable_1603.xlsx`, row 13 (1603-08-08-08-FG).
- **Log:** 20 lines appended to `stage/CHANGES.csv`.
- **Original table:** `old_files/DesignTable_1603.xlsx`.
- **Cells filled** (only empty cells; this is asserted):
  - the row's 15 prepared cells from `brennan_yes_20261018/wave2/tee_elbow/cells.csv`: catalog sizes, end-library thread majors 0.84,
    the thread text and the note. These are the same source the -02 / -04 / -06 / -12 / -16 siblings were staged from by
    `apply_genfeat.py`.
  - `D1@BORE` = `D2@BORE` = 0.45 (STEP).
- **Marking** (as its siblings):
  - `$PRP@DimSource` = BRENNAN;
  - the AxialSource is prefixed `[BRENNAN-ONLY 2026-10-18]` and names the STEP bores;
  - DataStatus MISSING -> **ASSUMED**. The catalog and the STEP are the same supplier, so they count as one source. Air-Way's plain
    1603-08-08-08 also has a 0.45 bore, but its lengths differ (M1 1.00 vs 1.11, W3 1.33 / W5 1.44 vs 1.39, body flats 1.000 vs 0.875), so the row stays ASSUMED.
- **To undo:** copy `old_files/DesignTable_1603.xlsx` back, or clear the row's cells, set it MISSING and remove the 20 CHANGES.csv lines
  dated by this README.

## Proof (merged batch-17 tools `tools/_out/genfeat_20261018/merged/tools`, `OMI_ROOT` = the stage)
- **Regeneration** (`regen/before`, `regen/after`; before = the stage with the old 1603 table):
  - 1603: 5 -> **6 configurations**, 0 blocked.
  - The only macro line that changes is the expected-configurations count, 6 -> 7 (incl. Default) (`regen/macro_diff.txt`).
  - The SW2 header is identical. The 5 old configurations are unchanged, cell for cell (`regen/sw2_cmp.txt`).
  - The new row has BORE1 / 2 / 3 = 0.45.
- **Generator warnings:** the 08 row gets no nut-face / stem-tip warning (1.39 - 1.11 = 0.28 = the Brennan -08 swivel). The existing
  -06 / -12 warnings are unchanged.
- **Static checks** (`checks/`):
  - vbacheck: 51 procedures OK.
  - dofcheck_tee: legs 1-3 fully defined, 0 redundant.
  - allcfg_check: 6 configurations, 0 outline problems.
- **OCP closed loop** (`ocp/closed_loop.txt`, `ocp/results_1603.json`): **PASS**.
  - 6 configurations x 70 checks, 0 off, each 1 solid.
  - 1603-08-08-08-FG volume 1.6896 in^3. The Brennan STEP is 1.6245 in^3 (+4 %): the model uses the generic perleg tee body
    (2603HX-style), not the exact forging. This is the shape assumption already logged on every 1603 row.
  - The OCP model STEPs (`ocp/1603/`, 4.7 MB) are not committed.

## Still to do
- **SolidWorks dry run** of 1603 with the batch-17 set (CLAUDE.md verify loop). 1603 has never been dry-run in SolidWorks.
- **A14's other 7 rows** (6901-06-08, -12-06, -12-16, -16-12, -16-16, 6902-06-06, -08-08 -NWO-FG) need their Brennan STEPs.
  None is in `09_STEP_FILES` (3D_FILES_NEEDED.md).
