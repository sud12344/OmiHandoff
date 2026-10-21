# ORFS generator end functions (2026-10-20, cloud session) - STAGING, work in progress

**Status:** staged (steps 1-7 done). Nothing is shipped, and the live `tools/` is untouched.
- **2026-10-20 (PC): SolidWorks dry runs done. All 51 masters in `out/` PASS** after 5 generator fixes made here; the `out/` files are the
  tested ones. Run log and the fixes: `tools/_out/orfs_dryrun_20261020/RESUME.md`.
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

## Step 5 (done): the 29 per-size Brennan STEPs of 2026-10-20 (`tools/_out/orfs_steps2_20261020/`: sha256, surveys, swivel table)
- **Extractors** (`orfs_wp2_20261020/measure/fsmeasure.py`, the 8 pilots re-validated after every change: 0 FAIL, readings unchanged):
  - forged run-out `step_up` (flats above the thread: FS6500-06 / -10, FS2501-08-08-FG) and `none` (flats = thread: FS6500-04 / -12 / -16);
  - swivel mouth `cb` (counterbore + 60deg countersink, -10 up), the neck without a lip bore (-04 / -06), the nut rear face below the stem
    head (the -20 skirt groove); `partial` read for the closed loop of a no-step leg.
- **Loose parts at every size:** FS0306 / FS0318 -04 ... -24 (8 + 8), FS0319 -04 / -06 / -08 (3) and the coned-collar sleeves -12 / -16 / -20 as
  master **FS0319C** (one more profile point). Brennan's FS0306 / FS0318 -10 and -24 thread bores (dia 0.892 / 1.817) are smaller than the basic
  minor of 1-14 / 2-12: the model keeps the basic minor, each row's `$COMMENT` says BRENNAN DIFFERS (tell the user).
- **Male face-seal ends:** `FSMF_MEAS` (forged legs -04 ... -20, from the FS6500-NN male legs; -08 = FSM_MEAS[8]) and `FSM_MEAS` -24 / -32 for
  the straights (FS2403-24-24, FS6400-32-32-O). Straights at -04 ... -20 still need straight STEPs (FS2403-NN-NN): a forged leg has no flank /
  relief.
- **Swivels:** `FSSW_MEAS` -04 ... -20 from the FS6500-NN swivel legs (fssw_table.txt; -08 identical to the old entry); leg_FSSW draws the
  counterbore mouth from -10 up; the nut-wall check at the relief replaces the old radius-order test.
- **Masters - one sketch per master** (gen_tee `fs_code`): step S / N (flats = thread within 0.003: no step), adjustable-stud neck F / R
  (flush with / below the flats), swivel mouth K / C. Base = S F K; variants `<root>N / R / C / NR / NC` read the root's review table. Mixed rows
  (FS2500 x2) have no master yet. The no-step hex arm ends at the thread end.
- **FS6565-08-08 decides the straight swivel reference:** Air-Way L45 2.12 = Brennan seal face to seal face (0.855 + 0.41 + 0.855); nut face to nut
  face is 2.986 -> Air-Way's straight swivel lengths run to the stem SEAL face, as on the forged legs. The straight swivel end is not written yet.
- **Checks:** vbacheck 31 / 31 forged + 6 straight macros; dofcheck_tee 76 / 76 legs; allcfg 0; OCP closed loops: forged 72 configurations /
  2,034 checks, straights 7 / 175, loose 22 / 427 - all 0 off; volumes vs the new pilots FS6500-04 ... -20 -1.4 % ... +3.5 %, FS2403-24-24 -0.39 %,
  FS2501-08-08-FG +3.46 %; a new hex-over-thread check (point in the hex corner direction) proven on the unfixed no-step arm; regression 99 / 99
  identical (regress_all now also lists the derived roots).
- **ORFS total now: 101 configurations** in 37 masters (6 straight + 31 forged) + 8 FS4000 O-rings in the 4000 master; count: 1,517 of 2,535 ready after SolidWorks.
- **Still needs files:** FS2701-NN-NN-FG (bulkhead legs -04 ... -16), FS6801-NN-NN-NWO-FG (adjustable studs -04 ... -24), FS2403-NN-NN (straight
  male ends -04 ... -20), FS6500-24-24-FG (-24 swivel / forged leg), FS2406-08-04.

## Step 6 (done): the straight face-seal swivels FS6565 / FS6540 / FS6504 / FS6505 (20 rows)
- **Reference** (FS6565-08-08, step 5): Air-Way's lengths L45 / L34 / L40 / L16 run to the stem SEAL face; the model length `LNUT` = that
  length + the measured seal -> nut face distance SEAL (SPEC `Lfun`).
- **gen_straight2:** `FSSW_MEAS` moved here (gen_tee reads `G.FSSW_MEAS`; its 31 forged masters regenerate identical); `end_FSSW` (kind FSSW: nut
  outside VO + cavity VG, as end_JICSW) with the End A (double swivel) and End B dimension blocks, the swivel kind lists `SW_KINDS` / `SWA_KINDS`,
  the nut-hex zone cut, the seal-face bore check (the bore runs 0.02 past the seal face into the nut cavity).
  - nut hex per Q-FS-NUT (user yes): the row's column where it equals Air-Way FF318 S, else FF318 S (FS6504's S is not a nut hex: FF318 S at
    every size; FS6505-16-16 1.61 -> 1.63) - noted in `$COMMENT`;
  - **body hex end = Air-Way where it prints the hex length** (FS6540 L37, FS6504 L39: the swivel-side hex face at L35 - L37 / L38 - L39 before
    the seal face); FS6565 / FS6505 print none: the measured swivel body face (= Brennan FS6565-08-08). Air-Way is 0.015 ... 0.09 shorter than the
    Brennan swivel at -04 ... -16 (each row's `$COMMENT`: tell the user).
  - masters FS6565 / FS6540 / FS6504 / FS6505 (countersunk mouth, -04 ... -08) and **...C** (counterbored mouth, -10 up).
- **Checks** (`checks/static_checks_sw.txt`): vbacheck 8 / 8, dofcheck_straight 8 / 8 fully defined, allcfg 0; forged masters unchanged;
  regression 99 / 99 identical.
- **OCP closed loop** (`scripts/closed_loop_fs_sw.py` -> `ocp/closed_loop_sw.txt`): zone hex cuts and stepped bores as the macro, each swivel read
  with measure_fssw (End A on a turned copy), the FS6540 stud with measure_stud: 20 configurations, 482 checks, 0 off; FS6565-08-08 vs Brennan:
  seal -> seal 2.12 / 2.12, volume +3.31 %.
- **ORFS total now: 121 configurations** in 45 masters (14 straight + 31 forged) + 8 FS4000 O-rings; count 1,537 of 2,535.

## Step 7 (done): FS2404 / FS6403 / FS2601 / FS6502 (user "keep airway and go on with those")
- **FS2404** (male face seal x male pipe, gen_straight2): -08-04 / -08-06 / -08-08 / -08-12 / -24-24 (the straight FSM end exists at -08 / -24 /
  -32 only; the other 16 rows need BRENNAN_FS2403-NN-NN). FS2404-08-06's empty thread cell takes the -08 face-seal thread (PLAN D1, now also
  in gen_straight2).
- **FS6403** (male face seal x male JIC): -08-08 only (same reason).
- **FS2601** (forged branch tee, male face-seal run x male pipe branch, Brennan-catalog rows): 5 rows in FS2601 + FS2601N (no-step legs).
- **FS6502** (45deg forged elbow, male face seal x female face-seal swivel): -08-08 builds; L2 read as the crossing -> seal face (ASSUMPTION
  logged, `fs_assume`; no FS6502 STEP). -06 / -10 / -12 / -16 are blocked by the generator's own corner-puck check (the 45deg body's corner
  reaches past the swivel body face outside the neck) - they need BRENNAN_FS6502-NN-NN-FG to show where the swivel sits on a 45deg body.
- **FS0304-C** (cap assembly, insert + nut): no Air-Way source and no shape STEP - not built (needs BRENNAN_FS0304-C-08 or similar).
- **Checks** (`checks/static_checks_new4.txt`): vbacheck 5 / 5, dofcheck 2 / 2 straights + 8 / 8 legs, allcfg 0; OCP closed loops
  (`ocp/closed_loop.txt` 13 straights / 271 checks, `ocp/closed_loop_tee_new4.txt` 6 / 161) 0 off; regression 99 / 99 identical.
- **ORFS total now: 133 configurations**; count 1,549 of 2,535.

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
- **SolidWorks dry runs on the PC** (CLAUDE.md verify loop; `TABLE_PATH` -> `out/`, `out/tee/`, `out/ring/`): first FS2403 / FS6400, one forged
  stepped (FS2500), one no-step (FS2500N), one counterbore swivel (FS6500C), one straight swivel each (FS6565, FS6540C), then the rest.
- FS2700 (bulkhead union) once the bulkhead files exist; FS2406 once FS2406-08-04 arrives; FS2408 after the hole decision.
