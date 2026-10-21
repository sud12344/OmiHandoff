# Job 3 - FS2500-12-08-FG / FS2500-16-12-FG (mixed face-seal legs) - STAGED, not shipped (2026-10-20)

## The two rows
Both are Brennan-only rows of the live FS2500 table (ASSUMED, DimSource BRENNAN, ORFS catalog p7) - no table edit in this job.

| Row | flats S2 | leg 1 thread major | leg 2 thread major | leg 1 | leg 2 |
|---|---|---|---|---|---|
| FS2500-12-08-FG | 1.188 | -12: 1.1875 (= flats within FSM_NOSTEP_TOL 0.003) | -08: 0.8125 | no step | stepped (thread below the flats) |
| FS2500-16-12-FG | 1.438 | -16: 1.4375 (= flats) | -12: 1.1875 | no step | stepped |

The live gen_tee gave them leg-shape code `X` ("mixed legs: no master yet (one sketch per master)"): its per-master flag `nostep` is all
face-seal legs or none.

## Decision: one more master per pattern, built by the existing per-leg machinery
Both rows have the SAME pattern (leg 1 no-step, leg 2 stepped) -> one DRIVE sketch -> one new master **`FS2500N1`** ("N" + the numbers of the
no-step legs, next to the existing FS2500 / FS2500N), reading the FS2500 review table. Each leg is drawn by the existing `leg_FSM` (the
no-step branch for leg 1, the stepped branch for leg 2); nothing new in the leg geometry or the VBA.

Patch (`../patches/gen_tee.py.diff`, same copy as job 2):
- `fs_code`: a mixed row gets `N<no-step legs>` (was `X`) - `X` stays for mixed NWO necks / swivel mouths;
- `sp_code` / `fs_suffix`: read `nostep_legs` / keep the digits;
- `FS_MIXED = {'FS2500': [(1,)]}` declares the masters that rows need (scan of all 17 forged FS base roots with the live tables:
  only these 2 rows are mixed - `../scripts/fs_mixed_scan.py`), so no empty masters appear;
- `leg_FSM` is called per leg with `nostep = leg in nostep_legs`;
- skip messages: `fs_code_why` (same words as before for every old code); a mixed code without a declared master still says "no master
  yet".

## Result
- **FS2500N1: 2 configurations** (ref FS2500-12-08-FG): `../out/tee/Build_FS2500N1_MASTER.bas`, `DesignTable_FS2500N1_SW2.xlsx`.
- FS2500 (5) and FS2500N (3): macro and SW2 identical to the live generator; only their summary skip text for the two rows changes
  ("X ... no master yet" -> "N1 ... built in master FS2500N1", `../checks/job3/regress_summary_diff_FS2500.txt`).
- No existing configuration changes.

## Checks
- `../checks/static_checks.txt`: vbacheck OK; dofcheck_tee FS2500N1 LEG 1 (no-step, 9 points) and LEG 2 (stepped, 11 points) fully defined;
  allcfg_check 2 configurations, 0 outline problems.
- `../checks/job3/ocp/closed_loop_tee.txt` (the ORFS closed loop `closed_loop_fs_tee.py`, copied and pointed at this tools copy; checks
  unchanged): FS2500 5 + FS2500N 3 + FS2500N1 2 = **10 configurations, 264 checks, 0 off** - the no-step leg's thread line runs into the
  body, the stepped leg's run-out reads the forged step, no hex material over either thread, 1 solid.
- Regenerate-all: `../regress_all.txt`.

## For the user
- Name OK (`FS2500N1`)? No Brennan STEP of either row exists; the leg shapes are the measured FSMF -08 / -12 / -16 legs (as FS2500 / FS2500N).
- PC: SolidWorks dry run of FS2500N1 (both configurations; the reference row has no thread proud of the flats, so the write_sw2 reference
  rule does not apply).
