# Next session - start here (written 2026-10-01; supersedes nothing in NEXT_SESSION_PROMPT_2026-09-26.md - its 36 questions are still open)

Read `CLAUDE.md`, then this file, then `00_DOCS/NEXT_SESSION_PROMPT_2026-09-26.md` (open questions 1-36, Task A staged, not accepted).

## 1. What happened on 2026-10-01 (nothing shipped; tools/generators, 04_DESIGN_TABLES, 03_SCRIPTS, 11_MASTERS untouched)

**SolidWorks is now 2026 SP4** (was SP3). Control dry runs of the CURRENT macros on SP4 vs the reference masters: 6802 16/16,
6502 8/8, 6565 6/6, 5404N 4/4 (+ the known [E] body-box FAIL line), 6410 27/27, 6405 40/40 identical (volume + size). 6410 / 6405 /
6565 were compared with the Task A staged parts in `11_MASTERS_NEW` (so those staged builds reproduce on SP4). Files:
`tools/_out/tier1_20261001/swtest/` (before_gen = macros, before_sw = parts + reports, sweeps/*.txt, sweep_cmp.py).

**Brennan catalogs** (user gave https://brennaninc.com/catalogs/ and said "use any needed"): 7 PDFs in
`07_RAW_EXTRACTS/brennan_catalogs/` (sha256 in the workflow output). Useful: TFA, Flange, Hosetail, ORFS. Not relevant:
Instrumentation (stainless/brass ferrule fittings), DIN (Volz metric), Clamps. Parser `tools/catalog/parse_brennan_catalog.py`
-> `tools/_out/brennan_catalog_20261001/` (427 tables, 5,056 rows, every page checked against its image, 5 corrections;
catalog_verified.json / .xlsx; match/*.json = catalog vs OMi WebsitePartsInfo2026.xlsx). Catalog values = SAME source as OMi
(Brennan) -> ASSUMED. User treats Q-NEW-BRENNANCAT as yes; Q-BRENNAN-ONLY formally open.

**STEP list FINAL (catalog workflow done, critic ok):** `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` / `.md` + report
`00_DOCS/Brennan_Catalog_2026-10-01.md`: Download now 95 (= the user's 61 minus 0618-08 / 0619-08, which Brennan does not sell -
candidates V0318-08 / V0319-08, question Q-NEW-F3-FLARELESS-ALIAS - plus 36), Later 283, Conditional-Optional 57, Replaced by
catalog 125, Already in repo 64. MISSING-row buckets if the user accepts catalog values: NOW 4 -> 74, STEP 105 -> 67, DECIDE
120 -> 88 (WORK 399, SCOPE 98 unchanged). The catalog answers several Task C questions (Q-B-ELBOW, Q-B-TEE, Q-B-5500, Q-F1 moot ...;
list in the report). The preliminary list (superseded; in `_to_delete/superseded_20261001/` and
`tools/_out/brennan_catalog_20261001/prelim/superseded/`) was `00_DOCS/Brennan_STEP_downloads_START_2026-10-01.xlsx` / `.md` (script
`tools/_out/brennan_catalog_20261001/prelim/build_step_workbook.py`, uses the unverified parse): 82 get now, 68 later, 267 skip
(catalog gives the dims), 15 check, 127 only-if, 64 have. **The user is downloading the 61 group-1 STEPs** (pilots + tier-1
geometry) into 09_STEP_FILES. The final list `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` + `00_DOCS/Brennan_Catalog_2026-10-01.md`
come from the catalog workflow (resumed after the usage limit - check they exist; if not, re-run the impact / STEP list / critic
stages: workflow script `brennan-catalog-vs-omi`, run wf_600d9c11-55d).

**Tier 1 generator fixes** (user: "do the tier one fixes"), staged in `tools/_out/tier1_20261001/` (work/<id>/patch.diff +
NOTES.md; integrated/ after the merge). Status: SPECS done (2403 incl. 2403-LH = large-hex union, 2405, 2404 + 2404-L fold; 2404
pipe end becomes the library cone = volume change on all 48 built 2404 configs), 5404N-06 done (round-bar step min 0.0025),
ORB-02 done, 6565-CAVITY done, ORBF-DEEPBORE done (also changes 6404 macro: new column + step, no geometry change), 6802-E45 done
(first revolve cut in the library), NECK-6502 done (revolve cut too), SIZE-40 partial (-40 JIC staged; rows blocked: no 2-1/2 NPT
ASME row in the repo), MEASURED-ENDS blocked (needs STEPs 6506-12-14, 6500-02-02-FG, 2406-03-04, 6410-04-02-O).
Configs with data that become buildable once tested: 2404-L-04-04/-06-04/-06-06/-08-08/-12-12, 6565-20-20/-24-24,
6410-20-12-O/-20-16-O/-24-16-O, 6802-20-16/-20-20/-24-24-NWO-FG, 6502-05-05-FG/-12-12-FG (15).
Integration / review / write-up DONE (`00_DOCS/Tier1_Fixes_2026-10-01.md`; full record `tools/_out/tier1_20261001/integrated/
INTEGRATION.md`, patch `integrated/patch.diff`): 61 roots regenerated, 796 -> 921 configs, 0 unexplained changes, all static checks
pass. Review fixes: 2404 "one bore" rows (24 + 5 2404-L) HELD for question Q-2404-BORE (Brennan STEPs show two bores, step at the
hex mid-plane); 2404-40-32 VERIFIED -> ASSUMED (Brennan-only); 6410's tier-1 macro only ships WITH Task A. SolidWorks tests:
`sh tools/_out/tier1_20261001/integrated/sw_tests/run_sw_tests.sh test` (started 2026-10-02; outputs `sw_tests/out/`, reports
`sw_tests/dryrun/`; pass criteria INTEGRATION.md section 7). New user questions: Q-SPECS-1 (2403 / 2405 drop 15 / 4 DROP-row
configurations the built masters have), Q-SPECS-2 (2404 pipe end -> ASME cone), Q-2404-BORE.

**SolidWorks tests of the tier-1 fixes DONE 2026-10-02** (results at the top of `00_DOCS/Tier1_Fixes_2026-10-01.md`): everything
passes except 5404N-06 (thread features fail at -06 -> hold that fix; Brennan 5404-N-06X2.000 added to Download now = 96 files).
Ready to ship once the user answers: 6502 + 6802 (no precondition); 6404 / 6565 (Q-TASKA); 6410 (only with Task A); 2403 / 2405
(Q-SPECS-1); 2404 (Q-SPECS-2 + Q-2404-BORE).

**2026-10-02 user: "yes to all"** = ship batch 14 (Task A 18 roots + tier-1 6502 6802 6404 6410 6565 + new SPECs 2403 2405 2404),
Q-SPECS-1 yes. **2404 EXCLUDED from batch 14 (user, later on 2026-10-02): keep 2404 exactly as it is (hand-built master and
table untouched, incl. 2404-40-32's VERIFIED) until OMi clarifies the bores** - Q-SPECS-2 / Q-2404-BORE on hold. 2404-L rows wait
with it. Other answers 2026-10-02: Q-BRENNAN-ONLY "later"; -40 sizes: Brennan-measured threads accepted (threads only need to show
on drawings); no-file parts: user will ask OMi. Batch-14 prep workflow (deploy toolchain minus
5404N-06, 2404 table edit, regen, checks, BUILD_PLAN) -> `tools/_out/ship_20261002/`. Then: real SolidWorks builds of the 8 roots,
move the 15 other Task A masters, RUN_ME_batch14, QA_Log #159+, Topologies, coverage, PROJECT_STATUS.
**57 Brennan STEPs received 2026-10-02** (now in 09_STEP_FILES; manifest `tools/_out/step_ingest_20261002/MANIFEST_sha256.txt`):
all 4 tier-1 geometry STEPs (6500-02-02-FG, 6506-12-14, 2406-03-04, 6410-04-02-O), 33 pilots, 2501-40-40-FG / 5000-40-40 /
5404-40-40 / 5406-40-32, 2404-L-32-32, 6565-32-32, 6802-32-32, 6410-32-12/-16, 1700 x3, 2700-02-02, 2701-02-02/-05-05,
2702-20-20, 2706-04-02, 6801-16-08/-24-32 (+ 2406-12-06 by mistake, kept). The user reports NO file for 26 part numbers (list in
the 2026-10-02 chat: 1405-20-24, 2403-06-02, 2502-20-16-FG, 2700-04/-08/-10/-12 small, 2705-04-02, 6500-20-16/-24-20/-32-24-FG,
6501-16-12-FG, 6502-06-04/-12-10-FG, 6802-04-02-NWO-FG, 1602-08-08-08-FG, 1803-08-08-FG, 2406-06-12, 5404-L-04X2.000,
5404-N-06X2.000, 5404-R-04-04-047, 6425-08-08, 6500-04-02-FG, 6502-04-02-FG, 6505-04-02, 6566-06-06-FG) and will send 15 more
(6801-L/-LL, 6805 6806 6807 6809 6810 6815 6832 6835 6901 6902 pilots) after the download limit resets. Open asks to the user:
Q-BRENNAN-ONLY (~70 rows), -40 thread source (ASME row or Brennan-measured), OMi drawings for the no-file parts.

**2026-10-02 later:** user approved 2702/2703 hex-arm 0.001 in short of the collar (fix workflow -> `tools/_out/fix2702_20261002/`)
and "yes, go ahead" with new masters largest-first from the pilots (wave 1 = 21 families with pilot + no new capability ->
`tools/_out/newmasters_20261002/`, write-up `00_DOCS/NewMasters_Wave1_2026-10-02.md`; build into STAGING for review, Brennan-only
rows prepared but MISSING until Q-BRENNAN-ONLY). User went to bed: "keep running"; overnight plan = ship batch 14 (+2702/2703),
stage wave 1 + batch 15 (72 catalog-settled OMi rows + 5 -FG STEP rows) for morning review, then CLEAN UP the folder (user asked:
"get rid of things not needed" = move to `_to_delete/<dated reason>/`, never delete; keep protected / referenced folders).

**STATE 2026-10-02 morning (session hit its usage limit here):**
- **Batch 14 SHIPPED + BUILT:** toolchain deployed (tier-1 minus 5404N-06; backups `_to_delete/superseded_20261002/tier1_toolchain_before/`
  + `tools/_out/ship_20261002/tools_before/`); real SolidWorks builds 6502 (10) 6802 (19) 6565 (8) 6404 (14) 6410 (30) 2403 (34)
  2405 (28) all PASS, identical to the dry runs (`tools/_out/ship_20261002/build_out/`, `ship_log.txt`); 15 Task A masters moved
  11_MASTERS_NEW -> 11_MASTERS (`scripts/move_taskA.py`). Old files: `_to_delete/superseded_20261002/batch14_replaced/` + `ship_20261002/old_files/`.
- Paperwork workflow (RUN_ME_batch14, QA_Log #159+, Topologies, coverage, PROJECT_STATUS, 11_MASTERS_NEW README, CLAUDE.md SP4) was
  RUNNING - check `tools/_out/ship_20261002/PAPERWORK.md`; if missing, redo it (workflow script ship-batch14-paperwork).
- **2702/2703 (batch 14b) READY TO SHIP:** SolidWorks dry runs PASS (0 FAIL, every configuration incl. new 2702-20-20-FG and
  2703-08-08-08-FG-LN rebuilds; -20 needs NO offset): `tools/_out/fix2702_20261002/sw_dryrun2_*_out.txt`, FOLLOWUP.md section 6.
  To ship: fix 3 low wording notes (2703-08-08-08-FG-LN cite OMi Items row 1016 'Side 3 Thread' 3/4-16 too; remove the dry-run FLAG
  from 2702-20-20-FG $COMMENT; add 'hex' to the 2702-20-20-FG AxialSource clarifier), back up + apply patch.diff to live gen_tee.py,
  copy the staged DesignTable_2702/2703.xlsx (scratch_root) to 04_DESIGN_TABLES (backup first), regenerate, compare with sw_dryrun2,
  copy macros (LF) + SW2, real-build both (no overrides; no old masters in 11_MASTERS - the held builds are in tools/_out/overnight),
  RUN_ME_batch14b + QA_Log + PROJECT_STATUS. 12 + 13 configurations.
- New masters wave 1 workflow was RUNNING (resumed; `tools/_out/newmasters_20261002/`); 3 groups done before (PIPE-TEES 5652/5603/5601
  = pilot row only each; 6420 = 6420-12-12 only, 6420-08-08 has 3 conflicting lengths -> user; 1724 = 0 rows, all Brennan-only).
  Most new-master rows wait for Q-BRENNAN-ONLY. Then SolidWorks dry runs into staging.
- Still to do overnight-plan items: batch 15 (72 catalog-settled OMi rows + 5 -FG STEP rows) staging; folder clean-up (user asked;
  move to `_to_delete/<dated reason>/`, never delete); morning summary for the user.

**2026-10-02 midday:** batch-14 paperwork WRITTEN (`tools/_out/ship_20261002/PAPERWORK.md`; RUN_ME_batch14, QA #159-#164,
coverage 990 configurations in a master, PROJECT_STATUS, CLAUDE.md SP4) - its independent check re-running. Running workflows (resume
with these scripts + run ids if interrupted): wave 1 `tools/_out/newmasters_20261002/new-masters-wave1.js` (wf_662bd69d-7b7; 10 groups
built - e.g. 0304 12 configs + 0306 11 configs from OMi values, 6408HHP 7, 1800/1824 generator done but 0 rows (Brennan-only), 1804
needs a flange-leg capability); batch 14b prep `tools/_out/fix2702_20261002/ship-batch14b-prep.js` (wf_4de4ba81-057, output
`tools/_out/ship_20261002b/`); batch 15 staging `tools/_out/batch15_20261002/batch15-stage.js` (wf_bf5cb03b-dc4); paperwork check
`tools/_out/ship_20261002/ship-batch14-paperwork.js` (wf_ff28924e-b0a).

**2026-10-02 afternoon:** batch 14b BUILT (2702 11 + 2703 12 configurations, PASS, `tools/_out/ship_20261002b/build_out/`) -> 992
configurations in a master. Resumed: batch-14b paperwork (`tools/_out/ship_20261002b/ship-batch14b-paperwork.js`, wf_94bb4560-cf0),
batch 15 (52 rows filled, 25 held - verify 2 groups + integrate), wave 1 (~50 new configurations staged - fixes + integrate + write-up).
CAUTION: wave-1 FOLDS (2501-LL) and batch-15 TEE-2501 both edit DesignTable_2501 in their own staging - merge them before shipping.

**2026-10-02 evening (ultracode off now - work directly, avoid workflows):** batch 14b paperwork DONE (RUN_ME_batch14b, QA
#165-#166, coverage A1 891, PROJECT_STATUS, 11_MASTERS README). Batch 15 merged (`tools/_out/batch15_20261002/integrated/`),
regress 0 changed old cells, checks clean, 18 SolidWorks dry runs 0 FAIL -> staged in 11_MASTERS_NEW, awaiting "ship batch 15".
Wave 1 PAUSED (user: save usage). Clean-up done (`_to_delete/cleanup_20261002/`). Summary for the user: `00_DOCS/SUMMARY_2026-10-02.md`.

**2026-10-08:** user "ship batch" -> **batch 15 SHIPPED** (`03_SCRIPTS/RUN_ME_batch15.txt`, QA #167-#169, evidence
`tools/_out/ship_20261008/`): all 18 masters moved 11_MASTERS_NEW -> 11_MASTERS; 1,044 of 1,804 configurations in a master
(672 MISSING, 88 with data but no master). 5604 / 5605 now carry the QA #144 collar. Wave 1 still PAUSED (rebase its 2501
FOLDS table on the batch-15 table; then SolidWorks dry runs per family from `sw_calls_*.json`). The user asked what they must do
to finish the remaining configurations - answer = the unblock breakdown written that day (see PROJECT_STATUS section 3).

## 2. Next steps
1. If integration is done: SolidWorks dry runs of every changed root from `tools/_out/tier1_20261001/regen/after` (TABLE_PATH =
   after SW2, SAVE/REPORT -> swtest/after_sw), sweep, `sweep_cmp.py` vs `sweeps/bef_<root>.txt` (existing configs must be identical
   except 2404 = intended pipe-end change), geometry + section screenshots on the 15 new configs. Roots: 2403 2404 2405 5404N 6404
   6405 6410 6502 6565 6802 (+ any the integrator lists). 2403/2405/2404 have no generator "before": compare with 11_MASTERS.
2. When the user's 61 STEPs land: MEASURED-ENDS (swiv.py / ports.py, validate first), pilots per new master.
3. Ask again: the 36 questions (2026-09-26 file), Q-BRENNAN-ONLY, Q-TRANSFER-5404N (new finding: Brennan drills differ from
   Air-Way bores on 5404-N: -04 0.281 vs 0.30, -06 0.406 vs 0.39, -08 0.531 vs 0.48), the ASME B1.20.1 2-1/2 row for -40.
