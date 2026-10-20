# Batch 17 - rebased on batch 16 as shipped (cloud session 2026-10-20)

User 2026-10-20: "can you ship batch 17?" with the hand-over notes "it must build on what's live now ... compare its staged copies against
the live ones and regenerate from the live state, not ship old copies" and "decide where adapters77 goes ... fold them into batch 17 or do
them first; just don't stage both in parallel".

**Status: REBASED, REGENERATED, STATIC CHECKS CLEAN, NOT SHIPPED.** A cloud session cannot run SolidWorks (CLOUD_SETUP.md). The CLAUDE.md
verify loop (dry run, sweep, look) has to run on the PC before anything goes into `03_SCRIPTS` / `04_DESIGN_TABLES` / `11_MASTERS`.
Nothing live changed in this session: `tools/`, `04_DESIGN_TABLES`, `03_SCRIPTS` and the MasterData workbook are untouched.

## 1. Decision: adapters77 is IN batch 17 (folded, already applied to the stage)
- The 37 wrongly-DROP adapters were rebased onto the stage on 2026-10-18 (`brennan_yes_20261018/wave3/adapters`, `scripts/apply_adapters.py`,
  `edits_77.csv`). The old `adapters77_20261016/apply_77.py` was **never run and must not be run**: it targets the pre-batch-16 tables and
  would apply the same rows a second time.
- Checked today: all 37 rows are `BUILD` in the stage (20 VERIFIED, 17 ASSUMED). Every edits_77 cell holds its new value; the 38
  "(append)" notes went in with apply_adapters' own wording. 34 of them generate a configuration. 2502-04-04-FG and 2502-06-04-FG belong to
  the hand-built 2502HX, and 6901-08-08 NWO-FG has no generator root.
- So adapters77 does not run as a separate step before batch 17. It ships inside batch 17, in the same 2501 / 6500 / 6505 tables as the
  other batch-17 rows. Only one set of those tables is staged.

## 2. The stage is on top of batch 16 (evidence in this folder)
| Check | Result | File |
|---|---|---|
| The 12 review tables batch 16 changed (0304 0306 1502 2504 2505 2606 2609 2611 6500 6500L 6501 6505): pre-batch-16 (git 974c8bd) vs live (d63e1a6) vs stage, cell by cell | every batch-16 change is already in the stage (0 stale cells). 2611-12-12-12-FG `$COMMENT` / AxialSource = the live text + the batch-17 note appended | `threeway_12tables.txt`, `scripts/threeway.py` |
| Every stage-vs-live review-table difference, all 200 tables | each one is a logged edit (`stage/CHANGES.csv`, `omi_answers_20261018/CHANGES.csv`), a new row, or a `$COMMENT` / AxialSource note. The rest are 2 renames with unchanged values (`6807-06-06 NWO-FG` -> `-NWO-FG`, `6902-12-12 NWO-FG` -> `-NWO-FG`, OMi part-number form) | `cmp_stage_live.txt`, `scripts/cmp_stage_live.py` |
| Merged toolset vs live `tools/` (with PUCK_INSET) | `patch_merged.diff` applies cleanly to the live tools and reproduces `genfeat_20261018/merged/tools` byte for byte | (command in the session log; repeat: copy `tools/`, `patch -p1 < patch_merged.diff`, `diff -r`) |
| Cloud regeneration fidelity: live tools on live tables vs the shipped `03_SCRIPTS` macros + `04_DESIGN_TABLES` SW2 | identical (date line aside) for every batch-14/15/16 root. Known exceptions only: the 22 roots with pre-2026-09-25 macros, 5405 (live macro kept in batch 16), 0318 2605 2650 5406 5600 (`$COMMENT` polish) | `cmp_b17.txt` column (1) |

The stage's own `*_SW2.xlsx` copies are pre-batch-16 and were **not used**. Every SW2 and macro here is regenerated.

## 3. What was regenerated
- `root/04_DESIGN_TABLES` = live `04_DESIGN_TABLES` overlaid with the stage's review tables. The SW2 files in it are the live ones and are
  not read by the generators.
- `regen/b17/{straight,tee}` = `genfeat_20261018/merged/tools` on that root (`scripts/regen_b17.py`): **the batch-17 candidate macros + SW2**.
  `regen/live/` = the control (live tools, live tables). Per-root summaries (BLOCKED rows, skips) are in `regen/b17_summaries.json`.
  The per-root rerun is content-identical (determinism).
- **Change set** (`changeset.txt` / `.json`, against batch 16 as shipped): **80 roots change**, 17 unchanged.
  - 28 new roots: 1503 1504 1601 1602 1603 1700RC 1703 1704 1724 1800 1804 1824 4501 4503 4601 4603 5406HHP 5406SHP 5501 5503 5505
    5601 5603 5652 6408HHP 6606 6807 6902.
  - 45 roots with macro + table changes.
  - 7 roots with table changes only: 0403 6401 6404 6408 2503 2601 2605. Mostly A23 VERIFIED marks; 2503 / 2605 also take A19 values.
- **Configurations: 1,357 generate** (1,081 in the shipped SW2s; 6400's hand-built SW2 counted) **-> +280 new.** 4 are lost:
  6400-05-08-O, -08-05-O, -14-12-O and -14-16-O, configurations of the hand-built 6400 SW2 that are not BUILD rows (A6: the generator
  replaces it).
- **Old configurations whose values change: 92 outside 6400, all from your approved answers.** Each changed configuration has a logged
  numeric review edit: A19 group 2 settled / group 3 open, A20 nut face, A21 1404 bores (`dimchg_cells.csv`, `checks/regress.txt`).
  6400 changes everywhere (A6 rebuild). Any other old configuration is unchanged.
- **BLOCKED, so out of the SW2s** (reasons in the summaries): 1501-04-02-FG, 1501-24-24-FG, 1502-04-04-FG, 2406-16-04, 2505-08-08-FG,
  2505-16-16-FG, 2702-12-12-FG-LN, 6405-32-24-O and 6802-04-06-NWO-FG were already held; **5503-02-02-FG is new** (port depth 0.46 ≥ leg
  length 0.47).

## 4. Static checks (merged tools, `checks/`)
- vbacheck: 97 macros OK (incl. the 24-continuation limit).
- dofcheck_straight: 42 macros, every DRIVE sketch fully defined, 0 redundant.
- dofcheck_tee: every leg fully defined. The 135° thread sketches of 1503 1504 5501 5503 5505 6902 have 1 redundant relation, the same
  as the proven HelixThread set (`same_as_HelixThread: True`, intended per MERGE_LOG).
- allcfg_check: 0 outline problems in every configuration (straights and tees, incl. the hose face-offs).
- regress vs the shipped SW2: as in section 3 (only the approved changes and the VERIFIED marks).

## 5. What the PC still has to do before batch 17 ships
1. `git pull` on the PC (this folder). SolidWorks 2026 SP4 running and signed in.
2. **Dry runs**: `dryrun/ORDER.txt` lists 80 call files `dryrun/calls/NN_<root>.json`, one root per `python sw_mcp/call.py @...`, output to
   `dryrun/out/NN_<root>.txt`.
   - Order: the features never tried in SolidWorks first: hose-barb face-off (4501 4503 4601 4603), threads on 45° legs (1503 1504 5501
     5503 5505 6902), per-leg swivels / NPSM nut on leg 2 (1601 1602 1603 6606 6807), 5404N, flange legs / collars, 6400.
   - Each file sweeps the existing `11_MASTERS` part read-only first, then dry-runs into `dryrun/<root>/` (`11_MASTERS` untouched), then
     sweeps the dry-run part.
   - Restart SolidWorks every ~40 builds.
3. `python tools/_out/batch17_rebase_20261020/scripts/cmp_dryrun_b17.py` -> `dryrun/VERDICT.txt`.
   - Per root: 0 FAIL, the reference-configuration trace, every configuration 1 body.
   - Old configurations must be identical unless batch 17 changes them on purpose.
   - The 22 roots with pre-fix macros are flagged REVIEW on any difference.
   - Then the screenshots / section views of the new feature roots (CLAUDE.md step 5): look at them.
4. If a root fails, hold it out (move its rows / hunks out, regenerate, re-check), as with 5404N-06 in batch 14.
5. **Ship** (CLAUDE.md, format of RUN_ME_batch16):
   - Deploy `genfeat_20261018/merged/tools` -> `tools/`, old files -> `_to_delete/superseded_<date>/` + `ship_<date>/old_files/`.
   - Stage review tables -> `04_DESIGN_TABLES`.
   - The dry-run parts -> `11_MASTERS` (sha256).
   - Macros (LF) + reports -> `03_SCRIPTS`, SW2 -> `04_DESIGN_TABLES`.
   - `RUN_ME_batch17.txt`, QA_Log #173+, Topologies notes, coverage refresh, PROJECT_STATUS.
   - Re-word the stale "BUILD-NEAR / MISSING" comments on rows that now build.
   - Retire `adapters77_20261016/apply_77.py` (superseded by section 1).
   - Then regenerate from the live state once more and compare it to the shipped files (as `ship_20261019/checks/verify_b16.txt`).

## Files
`scripts/` (all re-runnable: `python -I scripts/<x>.py <repo root>`), `threeway_12tables.txt`, `cmp_stage_live.txt`, `cmp_b17.txt`,
`changeset.txt/.json`, `dimchg_cells.csv`, `checks/`, `regen/b17/` + `regen/b17_summaries.json` + `regen/regen_log.txt`, `root/04_DESIGN_TABLES`,
`dryrun/` (calls, ORDER.txt, empty per-root folders). Not committed (reproducible): `regen/live/`, `regen/b17_per_root/`, `checks/_scratch/`.
