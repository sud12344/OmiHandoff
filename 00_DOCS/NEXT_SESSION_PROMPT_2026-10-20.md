# Next session - start here (written 2026-10-20, cloud session "ship batch 17")

Read `CLAUDE.md`, then `tools/_out/batch17_rebase_20261020/SHIP_PLAN.md`, then `00_DOCS/PROJECT_STATUS.md` section 1 (top entry).
Older background: `NEXT_SESSION_PROMPT_2026-10-19.md` (what the stage contains, the decisions of 2026-10-18).

## State
- **Batch 16 is live** (2026-10-19). **Batch 17 is rebased, regenerated and statically checked, but NOT shipped.** The cloud has no SolidWorks.
- adapters77 is part of batch 17: the 37 rows are already in the stage. **Never run `tools/_out/adapters77_20261016/apply_77.py`.**
- The batch-17 candidate files are in `tools/_out/batch17_rebase_20261020/regen/b17/{straight,tee}`: 80 changed roots, 1,357 configurations.
  They were generated from live `04_DESIGN_TABLES` + the stage review tables, with `genfeat_20261018/merged/tools` (= live tools + features).

## Next (on the PC, SolidWorks signed in)
1. `git pull`.
2. Run the 80 dry-run call files in `tools/_out/batch17_rebase_20261020/dryrun/calls/`, in the order of `dryrun/ORDER.txt`. The features
   never tried in SolidWorks come first: hose-barb face-off, threads on 45° legs, per-leg swivels, 5404N, flanges, 6400.
3. Run `scripts/cmp_dryrun_b17.py` to get `dryrun/VERDICT.txt`, then look at screenshots / section views of the new-feature roots.
4. Hold out what fails, then ship per SHIP_PLAN section 5 (RUN_ME_batch17, QA_Log #173+). This needs the user's go-ahead, as every batch did.
5. If the stage or the live tables change before the ship, re-run `scripts/threeway.py`, `cmp_stage_live.py`, `regen_b17.py`,
   `changeset.py` and the checks first. The kit is only valid for today's state.
