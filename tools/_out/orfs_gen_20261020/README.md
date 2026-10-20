# ORFS generator end functions (2026-10-20, cloud session) - STAGING, work in progress

**Status:** staged (steps 1-4 done). Nothing is shipped, no SolidWorks dry run has been done, and the live `tools/` is untouched.
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

## Step 3 (done): the forged face-seal swivel leg + FS6500 / FS6600 / FS6602
- **`gen_tee.py` `leg_FSSW`** (Brennan FS6500-08-08-FG swivel leg, `FSSW_MEAS[8]`):
  - **Leg length = the row L21, crossing -> the stem's flat SEAL face.** The nut face is 0.433 further out (`Mtip`).
  - **Nut:** hex = the row SHEX (Q-FS-NUT, |row - Brennan| <= 0.007) over 0.482, the 12.3 deg rear skirt, the rear face at 0.827.
  - **Neck and body face:** neck 0.321, body face 1.288 behind the nut face (= Brennan 0.635 from the crossing).
  - **Cavity:**
    - 45 deg mouth countersink, then the 13/16-16 basic minor over 0.406;
    - 45 deg relief to 0.4165, then a cone to the stem head (0.3725 x 0.197);
    - the seal face, then the bore.
  - **Not modelled:** nut hex chamfers, the skirt groove, the 0.0025 nut / stem clearance (one solid, as every swivel here), the O-ring.
  - **Sketch:** 17 points, 19 dimensions, fully defined.
  - **Thread:** helical (never SolidWorks' Thread feature on a female edge).
- **Wiring:** the face-seal swivel joins every generic swivel branch of gen_tee:
  - nut hex cut (NutHexCutAx from the nut face);
  - nut slab / reach, the corner-puck / neck checks (cavity end = the relief cone end);
  - the Z extent and the nut-corner extents of the self-checks;
  - the bore-through-the-seal-face check.
  - Plus its own neck-wall and seal-face-width checks, the DataStatus rule (ASSUMED) and the assumption text.
- **SPECs:** FS6500 (elbow), FS6600 (swivel branch tee), FS6602 (swivel on the run).
- **Rows:** FS6500-08-08-FG, FS6600-08-08-08-FG and FS6602-08-08-08-FG build. FS6500-08-06-FG waits for the -06 swivel (BRENNAN_FS6500-06-06-FG).
- **Checks:**
  - vbacheck: 15 / 15 forged macros OK;
  - dofcheck_tee: 37 / 37 legs fully defined, 0 redundant;
  - allcfg_check: 0 outline problems;
  - regression: 99 / 99 existing roots identical;
  - **OCP closed loop:**
    - the swivel is read with `fsmeasure.measure_fssw(model=True)`, the nut hex cut is rebuilt as the macro does it;
    - all 19 forged configurations: 589 checks, 0 off;
    - FS6500-08-08-FG is +2.07 % in volume vs the Brennan pilot (the unmodelled nut chamfers, groove and clearance);
    - the straights: 122 checks, 0 off.
- **ORFS total now:** 24 configurations: 5 straights + 19 forged in 17 masters.
- **FS6809** (face-seal swivel + adjustable stud) has no -08 row yet and is not given a SPEC.

## Step 4 (done): loose -08 parts - face-seal O-rings FS4000, nuts FS0306 / FS0318, braze sleeve FS0319
- **`gen_ring.py`** (new staging copy of `tools/_out/newtypes_20261014/generators/gen_ring.py`):
  - `LIVE` = the tools/ folder it sits in (was the Windows path; `GR_TOOLS` overrides);
  - a table missing from `GR_REV` is looked up in `OMI_REV_EXTRA`; SPEC 4000 reads `4000`, `4001` and `FS4000`;
  - the O-ring spot check keeps the largest ring (the FS rows come last in the table).
  - Run: `GR_REV=tools/_out/newtypes_20261014/review_tables OMI_REV_EXTRA=... python -I tools/generators/gen_ring.py 4000` -> `out/ring/`.
  - 29 configurations: the 21 rows 4000 / 4001 cell-identical to the old generator, + FS4000-04 ... -24 (SAE J1453 face-seal O-rings, all 8
    sizes: the O-ring needs no STEP). The sleeve TEST root 0319T is identical too.
- **`gen_straight2.py`** (loose nuts and the sleeve, -08 only - every other size needs its own STEP, see below):
  - `FSLOCK_RCS` / `FSNUT_MEAS` / `FSSLEEVE_MEAS` (measured on BRENNAN_FS0306-08 / FS0318-08 / FS0319-08);
  - `end_FSNUTCSA` / `end_FSNUTCSB` (locknut countersinks + the through thread), `end_FSNUTF` (tube-nut thread pocket to the lip face),
    `end_FSSLV` (sleeve: tube-side face, 15 deg taper, spigot, step up to the collar; the braze bore is its pocket) + its dimension block;
  - SPECs FS0306 (hex S4 / thickness h2), FS0318 (hex S / length h, lip bore 0.652 through the back face), FS0319 (round, L / d8; the
    tube-stop bore 0.378 from the seal face to the braze-bore bottom);
  - the FS thread check covers the nut ends; FS0318 / FS0319 End B labels name the lip bore / seal face (not "plug head"); the sleeve's own wall
    checks; the generic "port drill depth near the far tip" warning is off for the sleeve (the stop lip is by design).
  - Not modelled (in each row's `$PRP@AxialSource`): threads (suppressed as always), hex end chamfers, the FS0318 thread relief + mouth
    countersink, the FS0319 inner chamfers + spigot fillet. FS0319: collar length and stop lip held from the seal face (Air-Way L 0.37 vs pilot 0.374).
- **Checks** (`checks/static_checks_loose.txt`): vbacheck 4 / 4 OK; dofcheck_straight 3 / 3 fully defined, 0 redundant; allcfg 0 problems;
  regression 99 / 99 existing roots identical.
- **OCP closed loop** (`scripts/closed_loop_fs_loose.py` -> `ocp/closed_loop_loose.txt`): 3 configurations, 59 checks, 0 off - each rebuild
  read with the same extractor as its pilot (`measure_nut` / `measure_sleeve`) returns the row and the pilot (hex and length within the
  Air-Way rounding); volumes vs the Brennan pilots +2.18 % / +2.9 % / +1.34 % (the unmodelled chamfers).
- **ORFS total now:** 27 configurations in 20 masters + 8 FS4000 O-rings in the 4000 master = **35**; `count_20261020`: 1,443 of 2,535 ready
  after SolidWorks (was 1,432).
- **Other sizes of FS0306 / FS0318 / FS0319 need their own STEP** (BRENNAN_FS0306-NN, FS0318-NN, FS0319-NN): the -08 countersink / lip / sleeve
  shapes are not scaled to other sizes (the JIC 0306 precedent was measured per size). FS0319-24 stays held (Air-Way / Brennan OD conflict, D5).

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
- **SolidWorks dry runs on the PC** (CLAUDE.md verify loop; `TABLE_PATH` -> this `out/` folder), in this order:
  - FS2403 / FS6400 (the first FS masters: the Thread feature on the face-seal end, the bore-cut face pick on the land);
  - the 15 forged FS masters in `out/tee/` (PLAN risk R1: the end face where the thread steps down to the flats);
  - FS0306 / FS0318 / FS0319 (`out/`) and the O-ring master 4000 (`out/ring/`, 29 configurations; the 21 old rows dry-ran clean 2026-10-14).
- The female face-seal swivel on the straights (FS6540 / FS6505 / FS6504 / FS6565): needs the STEP above.
- More sizes: per-size Brennan STEPs (STEPS_NEEDED part 4, E1-E8) for the male end, the swivel, the nuts and the sleeve.
