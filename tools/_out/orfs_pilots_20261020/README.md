# ORFS pilot STEPs received (2026-10-20, cloud session)

**Status:** received and filed, not yet measured with extractors. Nothing in any table changed.

## What came in
- **Files:** 8 of the 9 ORFS pilots (`orfs_modeltype_20261016/STEPS_NEEDED.txt` part 1). The user downloaded them from Brennan's
  PARTcommunity / CADENAS portal and uploaded one zip to the cloud session.
- **Missing:** P9 **FS2406-08-06**. User: "this one didnt have a CAD file available".
- **Filed as** `09_STEP_FILES/BRENNAN_<part number>.stp` (byte copies; `sha256.txt`). The portal's readme is
  `cadenas_readme_example.txt` (terms of use: cadenas.de/terms-of-use-3d-cad-models).
- **Checks:** every file names its part number in its STEP PRODUCT entry, and every file loads in OCP as 1 solid, in inches. The sizes
  match Air-Way's printed values where Air-Way gives them.

| Pilot | File | Solids | Bounding box (in) | Volume (in^3) | Quick check |
|---|---|---|---|---|---|
| P1 | BRENNAN_FS2403-08-08 | 1 | 1.426 x 1.011 x 1.011 | 0.5865 | see below |
| P2 | BRENNAN_FS6500-08-08-FG | 1 | 1.660 x 2.356 x 1.083 | 1.0723 | |
| P3 | BRENNAN_FS2701-08-08-FG | 1 | 1.657 x 2.630 x 1.000 | 1.3269 | |
| P4 | BRENNAN_FS6400-08-08-O | 1 | 1.459 x 1.011 x 1.011 | 0.5825 | |
| P5 | BRENNAN_FS6801-08-08-NWO-FG | 1 | 1.660 x 2.033 x 1.083 | 1.1026 | |
| P6 | BRENNAN_FS0318-08 | 1 | 0.827 x 1.083 x 1.083 | 0.2856 | length 0.827 and hex corners 1.083 (= 0.94 A/F) vs Air-Way FF318-8: length 0.83, hex 0.94 |
| P7 | BRENNAN_FS0319-08 | 1 | 0.374 x 0.745 x 0.745 | 0.0692 | Air-Way: length 0.37, OD 0.75 |
| P8 | BRENNAN_FS0306-08 | 1 | 0.350 x 1.299 x 1.299 | 0.2263 | Air-Way: thickness 0.35; hex 1.13 A/F -> corners 1.30 |

## First look at P1 (male face-seal end -08)
Read from `survey/BRENNAN_FS2403-08-08_cyl.txt` / `_plane.txt`. These are face listings only; the FSM extractor (`fsm.py`, PLAN.md) is
not written yet.
- The two ends are identical: seal faces at x = +-0.695.
- **Thread:** major dia 0.8125 = 13/16-16, the -08 ORFS thread.
- **Bore:** 0.378 through.
- **O-ring groove in the seal face:** 0.052 deep (planes at +-0.643), between dia 0.425 and dia 0.629. 0.629 = the OD of the Air-Way
  FS4000-08 O-ring (I.D. 0.489 + 2 x W 0.070), so the O-ring sits on the groove's outer wall.

## P9 FS2406-08-06 has no file: what it was for
- **Purpose:** the FS2406 tube-end reducer (13 rows): collar, seal face and neck of the new FFS tube end, and whether the nut is part of
  the model (Q-FS2406-NUT is answered: reducer + nut, one solid).
- **Also:** an FSM -06 cross-check of E2.
- **Options:**
  - (a) Another Brennan FS2406 size with the same -08 tube end: **FS2406-08-04** (in Brennan's catalog and on OMi's site). If it has no
    file either, FS2406-12-08 or FS2406-10-06.
  - (b) The Air-Way model A9 FF2407-8-6-O (3DContentCentral; the reducer body only, with a crimp nut).
  - (c) Leave FS2406 until a file exists. The other 8 pilots do not depend on it.

## Next
1. Write and validate the new extractors on these files (PLAN.md):
   - fsm.py (P1; must read P2 / P5 the same);
   - fssw.py (P2);
   - the FSBH bulkhead end (P3);
   - the stud readings (P4 / P5, Q-FS-ORBSTUD);
   - fsnut.py (P6);
   - the sleeve (P7);
   - the lock nut (P8).
2. Then the ORFS generator / masters. The per-dash files E1-E8 and the family pilots F1-F15 come after the pilots pass.
