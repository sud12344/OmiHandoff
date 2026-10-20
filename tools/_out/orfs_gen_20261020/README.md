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

## Step 2 (done): the forged legs in gen_tee + 12 forged FS masters
- **`gen_tee.py`:**
  - `leg_FSM`: the face-seal end on a forged leg. The thread major runs to the end length, then steps down to the hex flats (= the leg core),
    as measured on the -08 legs of FS6500 / FS6801 / FS2701.
  - `leg_FSBH`: the bulkhead leg (FS2701 pilot): FSM nose, thread to a 60 deg flank, relief, the i4 step, the collar face at Air-Way i2,
    collar d17 x 0.20, then the arm.
  - The FS adjustable stud: the 6801 adjustable-ORB leg with the measured FS values (`NWO_FS[8]`: neck, lock nut 0.41 x row S3, washer,
    undercut). Its washer face sits at Air-Way L11 / L14 (Q-FS-ORBSTUD (a)). On -08 the neck lies AT the flats radius (no body face, as on
    the pilot): `leg_NWO(..., flat_neck=True)` drops the zero-height body face and the NECKR dimension.
  - Review tables are read through `omi_paths.review_table` (OMI_REV_EXTRA); the -LN tables fold in as plain parts (A10).
  - Further hooks:
    - FS rows go to ASSUMED (single source);
    - FS legs are kept out of the 2603HX A/F rule (PLAN R1);
    - the Z-extent self-check counts FS ends proud of the flats;
    - an empty thread-major cell takes the dash thread (PLAN D1).
- **SPECs:** FS2500, FS2501, FS2503, FS2603, FS2701 (+LN), FS2702 (+LN), FS2703 (+LN), FS2704 (+LN), FS6801, FS6802, FS6803, FS6804.
- **16 configurations build:**
  - FS2500-08-08-FG, FS2501-08-06-FG, FS2503-08-06-FG, FS2603-08-08-08-FG;
  - FS2701 / FS2702 -08-08-FG and FS2703 / FS2704 -08-08-08-FG, each also as -LN;
  - FS6801 / FS6802 -08-08-NWO-FG, FS6803 / FS6804 -08-08-08-NWO-FG.
- **3 rows blocked on purpose** (FS2501-08-08 / -08-12, FS2503-08-08): their row flats (0.875 / 1.06) are at or above the 0.8125 thread.
  The forged run-out was only seen where the thread stands proud of the flats, so they need their family pilot (STEPS_NEEDED part 3, F5 / F13).
- **Checks:**
  - vbacheck: 12 / 12 OK;
  - dofcheck_tee: 29 / 29 legs fully defined, 0 redundant;
  - allcfg_check: 0 outline problems;
  - **regression: 99 existing roots identical** (14 FS roots new);
  - **OCP closed loop** (`scripts/closed_loop_fs_tee.py` -> `ocp/closed_loop_tee.txt`):
    - 16 configurations, **484 checks, 0 off**;
    - legs are read in the plane through the flats; a 45 deg leg is read on a turned copy;
    - the stud's washer face is checked against Air-Way L11 / L14;
    - FS2701-08-08-FG is +0.68 % and FS6801-08-08-NWO-FG -1.4 % in volume vs the Brennan pilots.
  - The straight closed loop still passes (122 checks, 0 off).

## Blocked: the female swivel on the STRAIGHTS (FS6540 / FS6504 / FS6505 / FS6565) needs one STEP
- On the forged FS6500-08-08-FG pilot, Air-Way L21 (= Brennan AAA) runs from the crossing to the stem's SEAL face; the nut face is 0.433
  further out. PLAN.md had read the drawings as "to the nut face", for the straights as well.
- On the straights, Air-Way puts the swivel point 0.84 behind the hex face (FS6540-08-08-O: L35 - L37 = 1.39 - 0.55; FS6504-08-08:
  L38 - L39 = 1.24 - 0.40). Two readings fit that number:
  - (a) the nut face: the 0.827 nut then sits 0.013 clear of the hex;
  - (b) the seal face: the same as the forged leg's body face -> seal face of 0.855.
- (b) is the more likely, because the drawing reading was wrong on the elbow, but it is an inference. Not built.
- **Needs BRENNAN_FS6540-08-08-O or BRENNAN_FS6565-08-08** (STEPS_NEEDED part 4 lists FS6565-08-08 as optional; it now decides 20 rows).

## Next
- **SolidWorks dry run of FS2403 / FS6400** (CLAUDE.md verify loop, PC): the first FS masters. Unknowns:
  - the Thread feature on the face-seal end;
  - the bore-cut face pick on the land.
- **SolidWorks dry runs of the 12 forged FS masters.** The open point is PLAN risk R1: the end face where the thread steps down to the flats
  (between the flats and the hex corners) is the shape that broke 2702 / 2703 -16 once.
- **The forged swivel leg FSSW** (FS6500 / FS6600 / FS6602 / FS6809). Its -08 shape is measured (seal-face reference). It needs the swivel
  branches of gen_tee (nut hex cut, puck / neck checks).
- Nut / lock nut / sleeve masters (FS0318 / FS0306 / FS0319).
- the female face-seal swivel end FSSW (straights FS6540 / FS6505 / FS6504 / FS6565);
- the gen_tee legs (FSM on forged legs with the step run-out, FSBH, FSSW, NWO_FS);
- nut / lock nut / sleeve.
