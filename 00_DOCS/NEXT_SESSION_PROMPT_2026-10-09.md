# Next session - start here (written 2026-10-09)

Read `CLAUDE.md`, then `00_DOCS/PROJECT_STATUS.md` section 3 item 0 (the 2026-10-09 entries). Keep usage low (user's request): work
directly, few agents, no workflows unless the user asks.

## Done on 2026-10-09
- All 62 dimension-check drawings: `10_DRAWINGS/dimension_check_20261009/`. Email package for OMi (the user sends it):
  `10_DRAWINGS/for_OMi_2026-10-09/` (drawings PDF, `Email_to_OMi_2026-10-09.txt` with 8 plain questions, fill-in spreadsheet).
- User answers (PROJECT_STATUS s5): 2404 hole is stepped (Q-2404-BORE), step position "look at Air-Way" (= inside the hex -> hex
  mid-plane), Q-SPECS-2 = yes, 2404-24-20 = Air-Way 1.31 / 1.25.
- STAGED, not shipped, all generated + statically checked (dofcheck / allcfg / vbacheck / regress):
  - 2404: live review table + live gen_straight2.py already changed; output `tools/_out/r2404_20261009/regen/after` (57 configs).
  - `tools/_out/wave1_ship_20261009/` (toolchain = wave-1 merged + 2404 + polish + SPEC 2609; tables in `scratch_root`):
    wave 1 (33 configs), 8 batch-15 leftovers (6500 x4, 6501 x3, 6505-12-08), JIC tees 2505 x1 / 2606 x5 / 2609 x1 / 2611 x2.

## Next: SolidWorks dry runs (the user must start SolidWorks first)
The first 2404 attempt hit "Path not found" (scratch folder missing - every folder exists now). For each macro: `run_macro` with
`const_overrides` SAVE_PATH / REPORT_PATH (+ TABLE_PATH = the SW2 next to the macro), then report FAIL lines, `sweep_configs`, `geometry`
spot checks, `screenshot`. Restart SolidWorks every ~40 builds.

| root | macro + SW2 folder | SAVE / REPORT folder |
|---|---|---|
| 2404 | `tools/_out/r2404_20261009/regen/after` | `tools/_out/r2404_20261009/swtest` |
| 0304, 0306 | `tools/_out/wave1_ship_20261009/regen/after/straight` | `tools/_out/wave1_ship_20261009/swtest/<root>` |
| 2504, 1502 | `.../wave1_ship_20261009/regen/after/tee` | same pattern |
| 6500, 6501 | `.../wave1_ship_20261009/regen/leftovers/tee` | same pattern |
| 6505 | `.../wave1_ship_20261009/regen/leftovers/straight` | same pattern |
| 2505, 2606, 2609, 2611 | `.../wave1_ship_20261009/regen/jictees` | same pattern |
| 5405 | `03_SCRIPTS/Build_5405_MASTER.bas` (live table; adds 5405-12-08 / -16-08 / -16-12) | `.../swtest/5405` |

Old configurations of 6500 / 6501 / 6505 / 2404 must match the accepted masters (2404's hand-built master is NOT in the repo - compare
against the tier-1 dry runs in `tools/_out/tier1_20261001/` and check the stepped bores with `geometry`).

## Then
1. Stage the passing builds in `11_MASTERS_NEW` for the user's review; ship only on "ship batch" (copy the wave1_ship tools over live
   `tools/` after a backup, the changed scratch tables to `04_DESIGN_TABLES`, macros + SW2, RUN_ME_batch16.txt, QA_Log, coverage,
   PROJECT_STATUS).
2. Wave 2 (`tools/_out/wave2_shapes_20261008/`): HOSEB first (10 rows); ANGLED's design review FAILED (fix the 2 blocking items first);
   PERLEGSW 1 row; FLG61LEG 0 rows until OMi sends sizes.
3. Tell the user: 2505-08-08-FG / -16-16-FG stay blocked (the library port depth is deeper than their short female leg).
