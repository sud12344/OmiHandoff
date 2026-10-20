# ORFS generator end functions (2026-10-20, cloud session) - STAGING, work in progress

**Status:** staged. Nothing is shipped, no SolidWorks dry run has been done, and the live `tools/` is untouched.
- **Toolset:** `tools/` = a copy of the merged batch-17 toolset (`tools/_out/genfeat_20261018/merged/tools`) plus the ORFS additions below.
- **Plan:** `tools/_out/orfs_modeltype_20261016/PLAN.md`.
- **End data:** `tools/_out/orfs_wp2_20261020/end_lib_08.json` (extractors + validation on the Brennan pilots).

## How to run
```
export OMI_ROOT=<repo or the batch-17 stage> OMI_REV_EXTRA=<repo>/tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES GS_OUT=<new folder>
python -I tools/_out/orfs_gen_20261020/tools/generators/gen_straight2.py FS2403 FS6400
```
`OMI_REV_EXTRA` (new in `tools/omi_paths.py`): extra review-table folders, searched only for a table that `04_DESIGN_TABLES` does not have.
When it is unset, the behaviour is unchanged.

## Step 1 (done): male face-seal end + FS2403 / FS6400
- **`gen_straight2.py`:**
  - `FS_THR` (face-seal thread per dash);
  - `FSM_MEAS[8]` (Brennan FS2403-08-08 = FS6400-08-08-O);
  - `end_FSM`: face, rectangular O-ring groove, land, 45 deg nose chamfer, thread, 60 deg flank, relief, end length; the O-ring is not modelled;
  - `end_ORBFS`: the library ORB end with the thread lengthened to Air-Way's stud length (L8 - L9 - groove width), Q-FS-ORBSTUD (a);
  - the FSM dimension block in `emit()`: 10 dimensions + the land collinear with the face;
  - in `build_rows`:
    - the FS thread check;
    - the FS thread labels (an ORB end is labelled from its own dash);
    - the per-end assumption texts;
    - FS rows -> ASSUMED (single-manufacturer end shapes, PLAN R8, until Air-Way's models are measured);
    - a face-land check between the bore and the groove;
  - SPECs `FS2403` and `FS6400`. FS6400-L is not folded in: there is no shape source for where its extra length goes.
- **Rows:** FS2403-08-08; FS6400-08-06 / -08 / -10 / -12-O. Every other FS2403 / FS6400 row skips with the STEP that would fill it
  (`BRENNAN_FS6500-NN-NN-FG` or `FS2403-NN-NN`, STEPS_NEEDED part 2).
- **Checks:**
  - vbacheck: OK.
  - dofcheck_straight: both sketches fully defined, 0 redundant.
  - allcfg_check: 0 outline problems.
  - **Regression** (`scripts/regress_all.py` -> `regress_all.txt`): every root of both generators regenerated with the old (merged batch-17)
    and the new toolset on the same inputs. **99 existing roots identical** (macro, SW2, exit code); only FS2403 / FS6400 are new.
  - **OCP closed loop** (`scripts/closed_loop_fs.py` -> `ocp/closed_loop.txt`):
    - each configuration is rebuilt from the generator's own chain (revolve, hex, bore cuts) and measured with the pilot extractors;
    - **5 configurations, 122 checks, 0 off**;
    - FS2403-08-08 is -0.74 % and FS6400-08-08-O -1.23 % in volume vs the Brennan pilots, which have the O-rings, hex chamfers and tip
      chamfers the model leaves out.
- **Found in passing (not changed here):** SPEC `6400` of the batch-17 toolset labels End A's ORB thread (`$PRP@EndA_Thread`) from the FIRST
  part-number dash, while it builds that end from the second. On unequal-dash 6400 rows the label text is wrong; the geometry is right.

## Next
- the female face-seal swivel end FSSW (straights FS6540 / FS6505 / FS6504 / FS6565);
- the gen_tee legs (FSM on forged legs with the step run-out, FSBH, FSSW, NWO_FS);
- nut / lock nut / sleeve.
