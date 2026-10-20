# ORFS WP2: extractors for the new end types, validated on the 8 Brennan pilots (2026-10-20, cloud session)

**Status:** staging. No generator, review table or live `tools/` file changed. The plan is `tools/_out/orfs_modeltype_20261016/PLAN.md`;
the decisions are in its `DECISIONS.md`.

## Files
- `measure/fsmeasure.py`: the extractors. It imports the live `tools/measure` helpers (prof / swiv). Each reader takes the leg's half
  section (the half away from the other legs) and walks the outline edge by edge from the bore / end-face corner:
  - `measure_fsm`: male face-seal end FSM; `bulkhead=True` = the bulkhead end FSBH;
  - `measure_fssw`: female face-seal swivel;
  - `measure_stud`: fixed / adjustable ORB stud on an FS part;
  - `measure_nut`: FS0318 nut / FS0306 lock nut;
  - `measure_sleeve`: FS0319 sleeve.
- `validate_pilots.py` -> `pilot_meas.json` (every reading) + `checks.txt` (46 checks: **0 FAIL**).
- `build_endlib.py` -> `end_lib_08.json`: the proposed -08 end entries, each with its STEP. Shape only: what the rows give (legs, hexes,
  nut, collar dia, stud lengths) stays a row input. A few shape values in it (nut chamfer / relief / lip radii, lock-nut chamfer, washer,
  lock-nut thickness and neck of the adjustable stud, sleeve spigot) are typed from the raw chains in `pilot_meas.json`, and each was
  checked against them.
- `profiles/`: the raw half-section edge lists the extractors were written against.

## Brennan models the O-rings into the solid
- The face-seal O-ring sits in every FSM groove: W 0.070 on centreline dia 0.559, so I.D. 0.489 = Air-Way FS4000-08.
- The ORB O-ring (W 0.087) sits in every stud undercut.
- The extractors read the O-rings as checks and take the walls they hide as straight, with the groove corner sharp (ASSUMPTION: the
  corner is hidden under the O-ring). Our ends do not model O-rings, as the existing ORB / NWO ends.

## Results (checks.txt)

**(1) Male face-seal end: one shape everywhere.** Seven readings agree within 0.0015: both FS2403 ends, the male legs of FS6400 / FS6500 /
FS6801 / FS2701, and the FS2701 bulkhead nose.
- Bore r 0.189.
- Groove 0.425 / 0.629 dia, 0.052 deep.
- Land to r 0.3595, then a 45 deg chamfer x 0.0467.
- Thread major 0.8125 (13/16-16).
- End length 0.504.
- The run-out depends on the body:
  - straights: thread to 0.383, a 60 deg flank, relief r 0.3595 x 0.094 to the hex face;
  - forged legs: thread to 0.504, then a radial step down to the flats radius (0.375 = S2 0.75 / 2) and a 75 deg chamfer to the hex
    corners. That is how Brennan lets the end stand proud of the flats (PLAN risk R1).

**(2) Nuts.**
- The swivel nut and the loose FS0318-08 agree on hex 0.938 (Air-Way 0.94), length 0.827 (Air-Way 0.83), thread minor, mouth
  countersink and lip start (0.63 from the face).
- They differ outside and in the relief:
  - swivel nut: 30 deg chamfers, a 12.3 deg rear skirt with a groove, thread minor over 0.406;
  - loose nut: 75 deg chamfers, thread minor over 0.470.
- So the loose nut keeps its own entry. PLAN's shortcut "FSNUT from FSSW" does not apply.

**(3) O-ring.** The groove's outer wall = the FS4000-08 O.D. (0.629), and the groove I.D. 0.425 is inside the O-ring I.D. 0.489. Depth 0.052
gives 26 % squeeze on W 0.070.

**Threads.**
- FSM major 0.8125.
- FSSW / nut minor 0.7448 = the 13/16-16 basic minor.
- Stud major 0.750 (3/4-16).

**Air-Way rows vs the STEPs.** All within rounding:
- FS2403 L6, S1;
- FS6500 L7, L21, SHEX;
- FS2701 L16, L17, i2, d17;
- FS6400 L8, L9;
- FS6801 L7, L10, L11, S3;
- FS0318 S / h, FS0319 L / d8, FS0306 S4 / h2.

## Findings that change the plan
1. **R3, the swivel reference, is settled the other way.** Air-Way L21 1.49 (and Brennan AAA 1.49) = crossing -> the stem's flat SEAL
   FACE. The swivel nut face is 0.433 further out (1.923). PLAN section 2 FSSW takes the leg input to the nut face; it must be the seal
   face, with the nut face = seal + 0.433 at -08.
2. **i4 is not the collar thickness.**
   - Air-Way i4 0.06 = a dia 0.801 step in front of the collar.
   - The collar (d17 1.00) is 0.20 thick: from i2 = 1.44 to 1.64 from the tip, then the flats.
   - The collar thickness is a shape value with no Air-Way column. It needs a rule or the family pilots for the other sizes.
3. **Studs (Q-FS-ORBSTUD (a)).** The extra length is thread, not a plain shank:
   - the fixed stud has the ORB[8] undercut 0.660 x 0.094 and a thread 0.113 longer;
   - the adjustable stud has the NWO_MEAS[8] undercut 0.146 and washer 0.505 x 0.041, a thread 0.050 longer, and a bigger lock nut
     (0.938 x 0.41 vs 0.875 x 0.31).
4. **The FS0319 sleeve's collar (dia 0.745 x 0.197, seal face flat) = the swivel stem head behind its seal face** (r 0.3725 x 0.197). Also:
   - the sleeve's braze bore = 1/2 tube + 0.006;
   - its tube stop = the fittings' 0.378 bore.

## Not done yet (next)
- **Generator end functions + OCP closed loop (PLAN validation (4)):** `end_FSM` / `leg_FSM`, `end_FSSW` / `leg_FSSW`, FSBH, ORB_FS / NWO_FS,
  the nut / lock nut / sleeve profiles. Each one rebuilt in OCP -> measured with these extractors -> must return `end_lib_08.json`.
  That is the next work package.
- **Per-dash files E1-E8 and the family pilots F1-F15** (STEPS_NEEDED parts 2 / 3). The pilots pass, so they can be downloaded now. The
  extractors read E1-E6 (FS6500-NN-NN-FG: FSM + FSSW per dash), E7 (FS2403-24-24) and E8 (FS6400-32-32-O) without change.
- **Air-Way's own models of the pilots** (S2 / Q-FS-2NDSHAPE yes): not downloaded. They are measured with the same extractors when they
  come.
- **FS2406** (P9, no Brennan file): see `tools/_out/orfs_pilots_20261020/README.md`.
