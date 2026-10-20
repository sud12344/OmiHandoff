# Batch 16 - ship plan (2026-10-19, waiting for the user's go-ahead)

Batch 16 = new masters wave 1 + the 8 batch-15 leftovers from OMi + JIC tees with end-library ports + 2404 (two bores) + the 3
unbuilt 5405 configurations + the corner-puck fix (PUCK_INSET 0.0005), re-shipping the 14 affected shipped elbow masters.
NOT in it: `adapters77_20261016` (after batch 16, needs the user's OK), the 2026-10-18 Brennan / OMi-answer rows (batch 17, other
session), wave 2.

## Evidence (all in files)
- Puck-fix dry runs, 17 elbow roots: `puckfix_20261009/DRYRUN_VERDICT_2026-10-19.txt` (cmp_dryrun_resume_out.txt,
  sliver_scaling_out.txt): 0 FAIL, 1 body each, puck present everywhere, 20 configurations got their outer corner back, every
  other old configuration changes by the inset sliver only (dV/AF^2 = -0.000340 on all 177 90-deg ones).
- Other dry runs (2026-10-09): `wave1_ship_20261009/swtest/cmp_out.txt` - 0304 0306 2606 2609 2611 6505 5405 0 FAIL, 1 body,
  6505's 18 old configurations identical to `11_MASTERS`, 5405's 23 old ones identical to a read-only sweep of its master; 2404 57
  configurations 0 FAIL, the 24 kept rows identical to the tier-1 dry run.
- `checks/cmp_ship_out.txt` (scripts/regen_all.py + cmp_ship.py): every root regenerated from the staged review tables
  (`wave1_ship_20261009/scratch_root`) with the staged tools (`puckfix_20261009/tools_new`); the 24 roots batch 16 changes are
  IDENTICAL (macro + SW2, date line aside) to the macros that were dry-run. 5405 ships its live macro / SW2 unchanged (only the master
  is rebuilt). Not shipped although they regenerate differently: 22 roots whose `03_SCRIPTS` macros predate the 2026-09-25 generator
  fixes (5000 5404 2408 0318 5406 5406C 5406P 2700 4404 4604 5404N 2406 1405 1700 2650 2602 2605 5600 5602 2704 6600 6602; SW2 identical; known state) and 0318 5406 2650 2605 5600, whose SW2 differ only in a leading " | " in `$COMMENT` (polish).
- Live `tools/`, `04_DESIGN_TABLES`, `03_SCRIPTS`, `11_MASTERS` unchanged since the staging (2026-10-09).

## What changes
| What | Files |
|---|---|
| Toolchain -> live `tools/` | `puckfix_20261009/tools_new` (= wave-1 merged tools + 2404 + polish + PUCK_INSET): gen_tee.py, gen_straight2.py, checks/allcfg_check.py, checks/dofcheck_straight.py, measure/npsm.py, measure/prof.py changed; 17 new measure scripts |
| Review tables -> `04_DESIGN_TABLES` | 0304 0306 1502 2504 2505 2606 2609 2611 6500 6500L 6501 6505 (12) |
| Macros -> `03_SCRIPTS`, SW2 -> `04_DESIGN_TABLES` | 24 roots: new 0304 0306 1502 2504 2505 2606 2609 2611 2404(macro); replaced 2404(SW2) 6505 6500 6501 + puck 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802 |
| Masters -> `11_MASTERS` | 25: new 0304 0306 1502 2504 2505 2606 2609 2611 2404; replaced 5405 6505 6500 6501 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802 |

New configurations in a master: 0304 12, 0306 11, 2504 4, 1502 1, 2505 1, 2606 5, 2609 1, 2611 2, 6500 +9 (incl. 6500-L x5),
6501 +3, 6505 +1, 5405 +3 = 53; 2404 57 generated configurations replace the hand-built master (48-row SW2).
