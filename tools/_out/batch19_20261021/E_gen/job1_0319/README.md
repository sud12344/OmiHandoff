# Job 1 - 0319 JIC tube sleeves (12 parts) - STAGED, not shipped (2026-10-20)

User answer A2 (00_DOCS/ANSWERS_2026-10-18.md): the 12 0319 JIC sleeves are included.

## Result
- **12 configurations generate** in a new master `0319` (gen_ring kind SLEEVE): 0319-02 / -03 / -04 / -05 / -06 / -08 / -10 / -12 / -16 /
  -20 / -24 / -32. 0319-14 stays DROP (no OMi SKU). Reference configuration 0319-08.
- Output: `../out/ring/Build_0319_MASTER.bas`, `../out/ring/DesignTable_0319_SW2.xlsx`, `../out/ring/gen_ring_summary_0319.json`.
- No existing configuration changes (0319 had no master; the 0319T TEST root and the 4000 O-ring master regenerate identical).
- Not run in SolidWorks (not allowed in this job): the PC dry run is the next step (below).

## Generator: which one
The sleeve type was already in the live `tools/generators/gen_ring.py` (kind SLEEVE, proven on the TEST root 0319T in
`tools/_out/newtypes_20261014/swtest/0319T/`: 32 OK / 0 FAIL). So the job is a new SPEC in a copy of gen_ring, not a new model type:
`../tools/generators/gen_ring.py`, diff `../patches/gen_ring.py.diff` (+35 lines, nothing else changed):
- `SPEC['0319']` (kind SLEEVE, table 0319, ref 0319-08) with `shape=SLEEVE_SHAPE_0319`;
- `sleeve_from_shape()`: the seven DRIVE values from the row's sizes + the shape rule;
- `build_rows`: a SLEEVE SPEC with `shape` takes its DRIVE values from `sleeve_from_shape` (0319T keeps reading its own columns).
The macro is the 0319T macro with the 0319 names / table (same sketch, revolve, checks; diffed).

## Sources (every value)
| Value | Source |
|---|---|
| L (overall length) | Air-Way s48 `L` (`07_RAW_EXTRACTS/airway_passes/0319_p1.txt` / `_p2.txt`; = OMi "Overall Length" on all 12 rows) |
| collar O.D. | Air-Way s48 `X` (the table's note: "X = sleeve OD as printed"; = the collar dia of BRENNAN_0319-08, 0.6816 vs 0.68) |
| bore | OMi `WebsitePartsInfo2026.xlsx` Items "Side 1 ID", rows 42-53 (Air-Way prints no bore) - NEW table column `D@BORE` (`../CHANGES.csv`) |
| collar length, spigot, front-face inner radius, inner cone | SHAPE of `09_STEP_FILES/BRENNAN_0319-08.stp`, re-read with `tools/_out/newtypes_20261014/scripts/probe_sleeve.py` (`../checks/job1/probe_BRENNAN_0319-08.txt`): L 0.560, collar 0.6816, bore 0.505, collar length 0.220, spigot r 0.2810, front-face r 0.2945, cone 33.0 deg (slope 0.6491), R0.062 blend |

DataStatus stays ASSUMED (one source per value). The review table copy is `../root/04_DESIGN_TABLES/DesignTable_0319.xlsx` (24 cells:
12 bores + 12 AxialSource notes).

## Modelling assumption (written into every row's `$PRP@AxialSource`, "SHAPE_RULE")
One Brennan sleeve file exists (-08). The other sizes take the -08 SHAPE, carried by:
- collar length = 0.220 / 0.560 of L;
- spigot radius = bore + 0.3257 x collar wall (wall = collar radius - bore radius; the -08 fraction);
- front-face inner radius = bore + 0.4800 x collar wall;
- inner front cone at **33.0 deg to the axis at every size** (cone length from the two radii).
At -08 the rule returns the Brennan shape exactly. **Difference from the 2026-10-14 TEST**: the TEST scaled the cone LENGTH with L, which
makes the cone angle drift from 33 to 40.5 deg across the sizes; here the angle is kept (an angle is shape, not size). Same at -08.
Not modelled (as in the TEST): R0.062 cone-to-bore blend, 0.010 corner chamfers, 1 deg collar taper.

| Config | L | collar dia | bore | collar L | spigot r | front r | cone end |
|---|---|---|---|---|---|---|---|
| 0319-02 | 0.34 | 0.270 | 0.130 | 0.1336 | 0.0878 | 0.0986 | 0.0518 |
| 0319-03 | 0.34 | 0.330 | 0.193 | 0.1336 | 0.1188 | 0.1294 | 0.0507 |
| 0319-04 | 0.41 | 0.380 | 0.255 | 0.1611 | 0.1479 | 0.1575 | 0.0462 |
| 0319-05 | 0.44 | 0.440 | 0.318 | 0.1729 | 0.1789 | 0.1883 | 0.0451 |
| 0319-06 | 0.50 | 0.500 | 0.380 | 0.1964 | 0.2095 | 0.2188 | 0.0444 |
| 0319-08 | 0.56 | 0.680 | 0.505 | 0.2200 | 0.2810 | 0.2945 | 0.0647 |
| 0319-10 | 0.66 | 0.800 | 0.631 | 0.2593 | 0.3430 | 0.3561 | 0.0625 |
| 0319-12 | 0.68 | 0.970 | 0.756 | 0.2671 | 0.4129 | 0.4294 | 0.0791 |
| 0319-16 | 0.78 | 1.220 | 1.006 | 0.3064 | 0.5379 | 0.5544 | 0.0791 |
| 0319-20 | 0.91 | 1.530 | 1.260 | 0.3575 | 0.6740 | 0.6948 | 0.0998 |
| 0319-24 | 1.12 | 1.780 | 1.510 | 0.4400 | 0.7990 | 0.8198 | 0.0998 |
| 0319-32 | 1.19 | 2.410 | 2.014 | 0.4675 | 1.0715 | 1.1020 | 0.1464 |

## Checks (`../checks/`)
- `static_checks.txt`: vbacheck Build_0319_MASTER.bas 6 procedures OK.
- `job1/sleeve_checks.txt` (`../scripts/sleeve_checks.py`): every configuration - outline (no zero segment / self-intersection, the
  generator's radius / axial order), DRIVE sketch DOF (18 unknowns, rank 18 = fully defined, no redundancy; the macro's constraint set),
  OCP closed loop (half-section revolved, STEP written and read back with the probe_sleeve reader: L, collar, bore, collar length, spigot,
  front face, cone end, cone 33.0 deg, volume = the generator's frustum sum, 1 solid): **12 configurations, 144 checks, 0 off**.
  0319-08 vs BRENNAN_0319-08: volume +1.41 % (the model has no blend / chamfers).
- dofcheck_straight / allcfg_check do not read gen_ring macros (hence the own DOF / outline check).
- Regenerate-all (`../regress_all.txt`): gen_ring 4000 and 0319T identical, 0319 NEW.

## For the user
1. **Accept the shape rule** (one Brennan file, -08 shape carried to 11 other sizes, cone angle kept) - or download per-size shape files
   (BRENNAN_0319-02 ... -32, 11 files) and the rule is replaced by measured values. MS51533 (not on disk) may also give collar / spigot.
2. Small sizes: Air-Way's X equals or nearly equals L at -03 / -05 / -06 (0.33 / 0.34, 0.44 / 0.44, 0.50 / 0.50). X is read as the collar
   O.D. (true at -08, Brennan); worth a look on Air-Way's s48 drawing that X is the collar O.D. at every size.

## Next (PC)
Dry run (CLAUDE.md verify loop): `run_macro` on `out/ring/Build_0319_MASTER.bas` with `TABLE_PATH` -> `out/ring/DesignTable_0319_SW2.xlsx`,
`SAVE_PATH` / `REPORT_PATH` -> a scratch folder; sweep_configs (12 + Default), geometry at -02 / -08 / -32, screenshots. Ship = gen_ring
patch -> tools/, the review table edit -> 04_DESIGN_TABLES (CHANGES.csv rows of table 0319), macro -> 03_SCRIPTS, SW2 -> 04_DESIGN_TABLES.
