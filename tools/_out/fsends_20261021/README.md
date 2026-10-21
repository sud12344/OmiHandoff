# Per-size face-seal end tables (2026-10-21) - STAGED, not shipped

The 18 Brennan STEPs the user downloaded 2026-10-21 (`09_STEP_FILES/BRENNAN_FS2403-NN-NN`, `FS2701-NN-NN-FG`, `FS6801-NN-NN-NWO-FG`;
checksums `tools/_out/steps63_20261021/sha256_fs18.txt`; each 1 solid, names its part) give the ORFS generator the end detail it measured
only at -08 (and -24 / -32 for the straight end).

## Measured (`scripts/survey.py` -> `survey.json`, `scripts/build_entries.py` -> `entries.json`)
- Validated extractors (tools/_out/orfs_wp2_20261020/measure/fsmeasure.py), same orientation calls as the -08 pilots. The -08 pilots are
  re-read and reproduce the generator's FSM_MEAS[8], FSBH_MEAS[8] and NWO_FS[8] exactly; both ends of every FS2403 agree.
- FSM_MEAS (male face-seal end on a straight) -04 -06 -10 -12 -16 -20: groove ID / OD / depth, face, thread start, relief, end length.
- FSBH_MEAS (bulkhead leg) -04 -10 -16. NOT -06 / -12: the collar radius equals the forged flats radius (0.435 / 0.433, 0.685 / 0.686), the
  collar runs into the body with no face - a zero-height face; needs a leg variant (like the stud's flat_neck).
- NWO_FS (FS adjustable stud) -04 -06 -10 -12 -16 -20 -24: washer, lock nut thickness and A/F (hex corners x 2 cos 30, 3 decimals), neck,
  undercut.

## Generator change (`tools/` = copy of tools/_out/orfs_gen_20261020/tools + the entries; additive)
gen_straight2: FSM_MEAS / FSM_SRC entries. gen_tee: FSBH_MEAS / NWO_FS entries; FSBH_ASSUME / NWOFS_ASSUME now say "measured on the
Brennan ... of the size" (was "on the -08 pilot") - the only change to existing configurations ($PRP@AxialSource text).

## Checks
- `scripts/regen_all.py` -> `regen/cmp.txt`: all 156 roots (+ the FS leg-shape sibling masters) regenerated with the old and the new tools on the
  brennancad stage tables: 134 identical; 22 FS masters change: **97 new configurations**, 0 lost; old configurations change only in the
  AxialSource text. New masters: FS6802R, FS2701N, FS2702N, FS2704N, FS6803NR, FS6804R, FS6804NR.
- `checks/`: dofcheck straight / tee fully defined, 0 redundant; allcfg 0 outline problems; vbacheck OK (22 macros).
- OCP closed loop (`scripts/closed_loop_fs.py`, `closed_loop_fs_tee.py`, copies of the ORFS staging scripts reading these tools):
  straights 72 configurations, 1,565 checks, 1 off = FS6400-04-10-O: the ORB-stud reader fails on the model (a -10 ORB stud on a -04 body;
  the FS end of that part passes) - look at it in the SolidWorks dry run; tees / elbows 56 configurations, 1,680 checks, 0 off.
- Volume vs the Brennan STEPs (FS2403-NN-NN model vs file): -0.45 % ... -3.91 % (-08 = -0.74 % as for the pilot) - the Brennan files carry
  the O-rings and the hex / tip chamfers the masters leave out.

## Next
- SolidWorks dry runs of the 22 FS masters (macro + SW2 table per master in `out/<root>/`; TABLE_PATH = that folder). `regen/` and the
  closed-loop model STEPs are not committed (reproduce with the scripts).
- Merge with the group B session's ORFS tool copy (it adds FS SPECs) - both are additive.
