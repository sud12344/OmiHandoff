# OMi fitting library: project status and open work (2026-10-08: batch 15 shipped - 52 new configurations in 18 masters; before: batch 14 / 14b 2026-10-02)

This is the handover state from the Cowork sessions (2026-09-04 to 2026-09-25), updated after Claude's overnight
SolidWorks build of 2026-09-25 (details: `00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`) and after batch 14 (2026-10-02,
`03_SCRIPTS/RUN_ME_batch14.txt`). Read `CLAUDE.md` first, then `00_DOCS/NEXT_SESSION_PROMPT_2026-10-01.md`. This file is
the detail behind it. Keep it current: update it whenever a batch ships or a decision is made.

## 1. Where things stand

**2026-10-08: BATCH 15 SHIPPED (`03_SCRIPTS\RUN_ME_batch15.txt`, QA #167-#169; user: "ship batch").** 52 new configurations in 18
existing masters: 1501 2501 2503 2601 2701 2706 5500 5604 5605 6401 6500 6501 6502 6504 6505 6506 6801 6802 (272 -> 324
configurations). 47 rows from the OMi dimension file (the Brennan catalog only paired OMi's leg columns), 5 forged rows from their own
Brennan STEPs; all ASSUMED. The parts are the 2026-10-02 SolidWorks dry-run builds from `11_MASTERS_NEW`, moved unchanged (sha256);
macros (LF) + reports -> `03_SCRIPTS`, SW2 + 19 review tables (incl. `DesignTable_2501L.xlsx`) -> `04_DESIGN_TABLES`. Checks
(`tools\_out\ship_20261008\checks\`): regenerating the 18 roots from the staged tables with the live tools reproduces the staged
macros + SW2 (date line aside); regress 0 changed old cells; dry runs 0 FAIL, 1 body each; old configurations = the accepted masters
266 / 266 (257 vs the sweeps recorded at their builds, 9 of 2601 vs a read-only sweep 2026-10-08). **5604 / 5605:** the replaced
user-built parts predated the QA #144 round collar; the shipped ones carry it (old configurations -1.8 to -5.8 % volume, sizes
unchanged - QA #168). 2602 / 5602 still have their 2026-09-24 builds. Old files: `_to_delete\superseded_20261008\batch15_replaced\`
+ `tools\_out\ship_20261008\old_files\` (MANIFEST*.txt). 25 rows held MISSING (QA #169; 24 build with Q-BRENNAN-ONLY = yes).
**Now: 1,044 of 1,804 configurations in a master** (943 in `11_MASTERS` + 3 unbuilt 5405 + 98 hand-built 2404 / 6400); 672 BUILD
rows MISSING, 88 with data but no master configuration; 62 masters in `11_MASTERS`; 16 topologies fully modelled. Coverage
refreshed (A1 943, A2 98, D 111, E 1, F1 232, F2 266, F3 138, F4 11, F5 1, X 30). `11_MASTERS_NEW` is empty again (README,
screenshots, fixed_macros). **Wave-1 FOLDS (2501-LL) staged its own `DesignTable_2501.xlsx` before batch 15: rebase it on the
shipped table before it ships.**

**2026-10-02: BATCH 14 BUILT AND SHIPPED (`03_SCRIPTS\RUN_ME_batch14.txt`, QA #159-#164; user: "yes to all").** 22 roots:
- **7 real SolidWorks builds** (2026 SP4, through the MCP, deployed tier-1 toolchain): 6502 6802 6565 6404 6410 2403 2405.
  Each: "finished with 0 problem(s)", report 0 FAIL lines, saved to `11_MASTERS`, every configuration one body and identical
  (volume + size) to its 2026-10-02 dry run (`tools\_out\ship_20261002\build_out\<root>.txt`, `ship_log.txt`).
- **15 Task A masters** (OMi values, built as dry runs on 2026-09-25 night) moved `11_MASTERS_NEW` -> `11_MASTERS` unchanged
  (sha256), reports -> `03_SCRIPTS`: 0403 1404 2705 2706 6401 6402 6405 6408 6504 6505 2501 2503 5500 5502 6500. The staged
  6404 / 6410 / 6565 were superseded by the tier-1 builds (to `_to_delete`).
- Configurations of the 22 roots: 429 -> 425. +15 new: 6502-05-05-FG / -12-12-FG, 6802-20-16 / -20-20 / -24-24-NWO-FG,
  6565-10-10 / -20-20 / -24-24, 6410-20-12-O / -20-16-O / -24-16-O, 6401-32-32-O, 6405-24-16-O, 6504-24-24, 2501-32-32-FG.
  -19: the DROP configurations of 2403 (15) and 2405 (4), Q-SPECS-1. Task A changed 138 configurations on purpose
  (`tools\_out\omi_apply_20260925\TaskA_result.md`); 6410-12-08-O is now OMi 1.480.
- **Toolchain:** the tier-1 generator fixes are DEPLOYED in the live `tools/` (10 files; NOT the 5404N-06 fix). Record and
  undo: `tools\_out\ship_20261002\PREP.md`, `deploy.diff`, backup `tools_before\`. What each fix does:
  `00_DOCS\Tier1_Fixes_2026-10-01.md`. **Since 2026-10-02 12:21 the live `gen_tee.py` also carries the batch-14b change**
  (`bh_short`, 2702 / 2703 only - below): it no longer matches `ship_20261002\live_tools_after_sha256.txt` (the batch-14
  state), reversing `deploy.diff` fails 1 gen_tee.py hunk, and `tools_before\` would drop 14b too. To undo batch 14's tools:
  undo 14b first (`gen_tee.py` from `tools\_out\ship_20261002b\old_files\tools\generators\` = the batch-14 deploy,
  sha256 646d9da2...), then `deploy.diff` reverses cleanly (tested: `ship_20261002\paperwork\fix\undo_test.txt`).
- Plan, expected values per configuration, file inventory: `tools\_out\ship_20261002\BUILD_PLAN.md`. The paperwork (RUN_ME,
  QA_Log, Topologies, coverage, this file, CLAUDE.md) with sha256 before / after: `tools\_out\ship_20261002\PAPERWORK.md`.
  Old files: `_to_delete\superseded_20261002\batch14_replaced\` AND `tools\_out\ship_20261002\old_files\` (MANIFEST.txt and
  MANIFEST_paperwork.txt in both; the user empties `_to_delete`).
- **Not in batch 14:** 2404 / 2404-L (held until OMi clarifies the bores), 5404N-06 (failed in SolidWorks), 2702 / 2703
  (batch 14b), the 3 unbuilt 5405 configurations.

**`11_MASTERS` holds 60 masters** (batch 14 replaced 22 and added no new name); 2404 / 6400 are hand-built (files not in
the repo), 2702 / 2703 are held back (`tools\_out\overnight\`). `11_MASTERS_NEW` keeps only `screenshots\`, `fixed_macros\`,
an empty `reports\` and its README. **`03_SCRIPTS` rebuilds exactly what is in `11_MASTERS`** for the 22 batch-14 roots and
6801 6803 6804.

**Configurations (BUILD rows) of the 126 topologies, counted 2026-10-02 after batch 14**
(`tools\_out\ship_20261002\paperwork\count_configs.py`; on the pre-batch-14 SW2 tables it reproduces the 2026-09-25 numbers
exactly): 1,804 in all. **990 are in a master** (was 976): 868 in `11_MASTERS` with the current configuration set (was 853),
3 in the current 5405 macro but not yet in its built file (5405-12-08 / -16-08 / -16-12 - re-run Build_5405), 98 in the
hand-built 2404 / 6400, 21 in the held-back 2702 / 2703 (990 configurations = 987 OMi part numbers; 2408-04 / -06 / -20 are
built SOLID and -H). 88 have dimensions but no master configuration (was 101): 12 blocked in roots that have a master
(1501-04-02-FG / -24-24-FG, 2406-16-04, 2702-12-12-FG-LN, 6405-32-24-O, 6802-04-06-NWO-FG and 6 2404 rows), 76 in tables
without a master. 726 are DataStatus MISSING (727 until Task A made 2501-32-32-FG ASSUMED). Topologies: 116 of the 126 have
BUILD rows, 61 have a master, 10 are fully modelled (0318 0403 1404 2605 2650 2704 4404 4604 6402 6602) - unchanged.
**Coverage by OMi part number** refreshed 2026-10-02 (`00_DOCS/OMi_Coverage_2026-09-24.xlsx`, in place): A1 built 868 (was
854; the 14 new: 2501-32-32-FG, 6405-24-16-O, 6410-20-12-O / -20-16-O / -24-16-O, 6502-05-05-FG / -12-12-FG, 6504-24-24,
6565-10-10 / -20-20 / -24-24, 6802-20-16 / -20-20 / -24-24-NWO-FG), A2 98, B 21 (2702 / 2703), D 111, E 1, F 702, X 30 (A1
counts the 3 unbuilt 5405 configurations as built: the tool reads the SW2 tables).

**Masters in `11_MASTERS` by builder (60):**
- built by the user (18): 2500HX 2502HX 2601 2602 2603HX 2605 2650 5000 5404 5405 5406 5406C 5406P 5504 5600 5602 5604 5605
  (0318 0403 6405 6408 were replaced on 2026-09-25, 2403 2405 5502 6401 by batch 14);
- built by Claude through the SolidWorks MCP for batch 14 (22, 2026-10-02): real builds 6502 6802 6565 6404 6410 2403 2405;
  Task A dry-run builds of 2026-09-25 night 0403 1404 2705 2706 6401 6402 6405 6408 6504 6505 2501 2503 5500 5502 6500;
- built by Claude overnight on 2026-09-25, accepted that evening and unchanged since (20): 0318 1405 1501 1700 2406 2408 2700
  2701 2704 4404 4604 5404N 6501 6503 6506 6600 6602 6801 6803 6804.
Overnight-build reports (`00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`): 16 carried FAIL lines, all explained ([A] leftover angle
dimension, [C] Default-configuration HELIXDIA, [D] extent-check bug, [E] 5404N threads-live box); the 22 batch-14 reports
have none.

**2702, 2703: BATCH 14b BUILT AND SHIPPED 2026-10-02** (`03_SCRIPTS\RUN_ME_batch14b.txt`, QA #165-#166): 2702 11 + 2703 12
configurations, 0 FAIL, identical to the dry runs (`tools\_out\ship_20261002b\build_out\`), now in `11_MASTERS`; new rows
2702-20-20-FG (own Brennan STEP) and 2703-08-08-08-FG-LN. **Configurations in a master: 992.** History of the fix below.
(Was: held back, builds in `tools\_out\overnight\`.) At -16 (-FG and -LN) the bulkhead-leg hex arm does not
rebuild: it ends exactly on the collar face and the collar radius lies between the hex flats and corners. User 2026-10-02:
OK to stop the arm 0.001 in short of the collar. The fix (`gen_tee.py`, SPEC key `bh_short`) was prepared in
`tools\_out\fix2702_20261002\` (SolidWorks dry runs of 2702 / 2703: 0 problems, `sw_dryrun2_2702_out.txt` / `_2703_out.txt`)
and **deployed 2026-10-02 12:21 by the batch-14b prep** (`tools\_out\ship_20261002b\PREP.md`): the live `gen_tee.py` and the
review tables `04_DESIGN_TABLES\DesignTable_2702.xlsx` / `2703.xlsx` are the 14b versions (old ones in
`_to_delete\superseded_20261002\batch14b_replaced\` and `ship_20261002b\old_files\`); regenerating every root changes only
2702 / 2703. Built and shipped the same afternoon (above).

**Macros.** The `03_SCRIPTS` macros of the 22 batch-14 roots and of 6801 / 6803 / 6804 carry the overnight generator fixes;
the 22 also carry the tier-1 fixes where they apply. Still broken: Build_2702 / 2703 at -16 (batch 14b). The other
accepted masters were built from older `03_SCRIPTS` macros (from before the 2026-09-25 fixes; harmless while their angle
columns stay constant - section 6). Before re-shipping any of them: regenerate with the deployed tools into a new
`GS_OUT` / `GT_OUT` folder, check, and dry-run (`tools\_out\regen_20260925` holds the 2026-09-25 regeneration).
`11_MASTERS_NEW\fixed_macros` keeps the macros that built 6404 / 6504 / 6565 on 2026-09-25 (history).

**Proven in SolidWorks on 2026-09-25:** the swivel-nut hex cut (`NutHexCutAx`), `ZoneHexCut` (straights), the 45 deg leg
helpers and the adjustable-ORB module, at every size. The NUTCUT revolve radius still equals the hex corner radius
exactly; if a new swivel size ever fails there, add a margin as `NWO_RN_MARGIN` does. The 6500 swivel section through
the nut flats lies within 0.003 in of the Brennan STEPs over nut hex, skirt and neck (nose tip ~0.01, per Air-Way).
**Proven on 2026-10-02 (SP4):** the first revolve cuts of the library (6502 NECKTRIM1 / NECKFILL1 in every size; 6802
ORBTRIM on a TEST row), the 6565 seat cones ending at the bore, the female ORB deep-bore port (ORBFB_DRILLANG 60 / 90,
flip-tested), the generated 2403 / 2405 (same volume as the user-built parts). SolidWorks is 2026 SP4 since 2026-10-01;
the control rebuilds showed SP4 = SP3 for these macros.

Each `RUN_ME_batch*.txt` in `03_SCRIPTS` says what a batch contains and what to look for in the reports.

## 2. Batch 13b: built, checked, ACCEPTED into 11_MASTERS and SHIPPED (2026-09-25, RUN_ME_batch13b.txt, QA #156)

Shipped from `tools/_out/regen_20260925/tee` (macros + SW2); all five dry-run in SolidWorks from that set on 2026-09-25
with every configuration identical (volume + size) to the accepted parts. To regenerate: set `GT_OUT` to a new folder first,
then `python tools/generators/gen_tee.py 2501 6801 6802 6803 6804` (never into `tools/_out/tee`, the overnight build inputs).

| Root | Configs | Status |
|---|---|---|
| 2501 | 32 | Folds in the 2501-L rows (user decision 2026-09-25). Brennan 2501-L-06-04-FG STEP: the forged NPTF hex arm simply runs to N3. Built clean in SolidWorks. Ready to release. |
| 6801 | 33 | New adjustable ORB module ("NWO": neck, locknut with 15 deg chamfers, backup washer, O-ring undercut, ORB thread). Static checks pass (sketches fully defined, clean outline for every configuration, static VBA check). OCP: every configuration rebuilt, one solid each, nut cut volume = the analytic integral; `measure/nwo_closedloop.py` on the OCP rebuild of 6801-08-08 / -04-02 / -32-32 returns the Brennan values. SolidWorks: built clean (all 33 configurations); its STEP exports measured with the NWO extractor equal Brennan at 9 sizes except the two Air-Way findings below and the cosmetic NWO_CH_DR (+0.0025 on the nut chamfer start). Ready to release. |
| 6802 | 16 (+4 blocked) | 45 deg elbow, ORB leg along +X. Static checks pass; built clean in SolidWorks; no OCP / Brennan geometry check. 6802-04-06 is blocked by Air-Way data (nut hex 0.56 for a -06 ORB, which needs 0.6875). 6802-20-16, -20-20 and -24-24 are blocked by a check that is too conservative: for e45 it counts the angled JIC leg's thread radius. Fix the check, don't change the geometry. |
| 6803 | 5 | Branch tee, ORB branch. Static checks pass; built clean in SolidWorks. ASSUMPTION: Air-Way prints no I3 for 6803, so the 6801 ORB_I3 of the same ORB size is used (equal to Brennan). Ask for a Brennan 6803-08-08-08-NWO-FG STEP. |
| 6804 | 8 | Run tee, ORB on the run (leg 2, -X). Static checks pass; built clean in SolidWorks. Same I3 assumption. Ask for Brennan 6804-08-08-08-NWO-FG. |

**13b shipping: done 2026-09-25** (RUN_ME_batch13b.txt, QA_Log #153-#158, Topologies notes, coverage refresh).

**6801 findings to report to OMi:**
- 6801-04-02: Air-Way LEG_ORB is 1.03, Brennan is 0.92.
- 6801-12-12: Air-Way ORB_THDL is 0.469, Brennan is 0.410.
- Both are built to Air-Way and noted in `$COMMENT` (BRENNAN_NOTES in gen_tee.py).
- Every other matched size agrees with Air-Way on leg lengths, I3, thread length, nut hex, body hex and undercut.

**Open question for the user: 6801-05-05.** It is MISSING in the review table ("CONFLICT vs MS51527"). Brennan
6801-05-05-NWO-FG matches Air-Way on every dimension. Ask whether to build it to Air-Way + Brennan. Don't decide alone.

**Brennan detail not modelled on any elbow:** the bores meet in a sphere of the bore radius at the crossing. Our bores
stop flat at the crossing. At -32 this is 0.75 in^3.

**Since batch 14 (2026-10-02):** 6802 has 19 configurations (the too-strict 45 deg check is fixed: tier-1 6802-E45, -20-16 /
-20-20 / -24-24 built) and 2501 has 33 (+2501-32-32-FG, Task A).

## 3. Open work (priority order)

0. **2026-10-14: NEW SCOPE - O-rings, bent-tube elbows, flareless nut + sleeve (OMi said yes, s5).** Write-up:
   `00_DOCS\Scope_ORings_BentTube_Flareless_2026-10-14.md`. 101 website part numbers (30 O-rings 4000 / 4001 / 4005, 68 bent tube
   1703 / 1704 / 1803 / 1804 -Tube + 6701, 3 flareless 0618 / 0619) + 13 only in OMi's parts file; all MISSING - OMi's file has no
   sizes, Air-Way no page, Brennan values not usable. Size request for OMi DRAFTED, not sent: `10_DRAWINGS\for_OMi_2026-10-14\`
   (`build_request.py` + `scope_parts.csv` in `tools\_out\omi_request_20261014\`). Needs: Q-NEW-ORINGSRC (AS568 table once OMi
   confirms each size number?), 5 Brennan shape files (1704-16-16, 1803-16-16, 6701-08-08, V0318-08, V0319-08), optional 0319.
   New model types to build (none exists): O-ring, sleeve, flareless nut (0318 SPEC), bent-tube generator (3 masters), drawing recipes.
   **2026-10-09 (later): staged, NOT shipped, SolidWorks dry runs pending.**
   - **2404 (Q-2404-BORE answered, s5):** LIVE `04_DESIGN_TABLES\DesignTable_2404_FINAL.xlsx` edited (29 rows: two bores from OMi, 2404-24-20
     from Air-Way, step at the hex mid-plane, the 4 "CB depth unsourced" rows released, 2404-40-32's Brennan depth dropped, question-26
     lengths 2404-10-04 1.69 / 2404-20-32 2.74) and LIVE `tools\generators\gen_straight2.py` (2404-L two bores, texts). Old files:
     `tools\_out\r2404_20261009\old_files\` + `_to_delete\superseded_20261009\2404_bore_answer\`. Generated: `r2404_20261009\regen\after`
     (57 configurations; checks pass; all other straight roots regenerate identically). Q-SPECS-2 = yes (library NPTF cone).
   - **Wave 1 ship workspace `tools\_out\wave1_ship_20261009\`** (= wave-1 merged tools + the 2404 diff + polish): polish done (gen_tee
     0-row guard, 2504 hex wording, 1502 stale texts, shape notes - text cells only); + the 8 batch-15 leftovers from OMi (6500 x4, 6501 x3,
     6505-12-08; `scripts\apply_leftovers.py`); + JIC tees with end-library ports (2505-12-12, 2606 x5 incl. the pilot, 2609-08 (new SPEC),
     2611 x2 incl. the pilot; `scripts\apply_jictees.py`; 2505-08-08 / -16-16 BLOCKED: library port depth deeper than the short leg).
     Regenerations + checks: `regen\after` (polish), `regen\leftovers`, `regen\jictees`, `checks_*.txt`. Next: SolidWorks dry runs into
     `swtest\<root>\` (2404 into `r2404_20261009\swtest\`), then stage for review.
   - Wave 2 (designs in `tools\_out\wave2_shapes_20261008\`): under the 2026-10-08 ruling only HOSEB 10 + PERLEGSW 1 rows are buildable;
     ANGLED's design review FAILED (2 blocking items); FLG61LEG 0 rows until OMi sends sizes.
   **2026-10-09: DRAWINGS DONE + EMAIL PACKAGE FOR OMi READY (not sent - the user sends it).** All 62 masters drawn
   (`10_DRAWINGS\dimension_check_20261009\`, 60 new + 1405 / 2650 copied from 10-08), every labelled value = its SW2 row
   (finalize.py, all_match on 62), sheets looked at (contact sheets `tools\_out\drawings_20261008\renders\cs1-8.png`).
   Script fixes (drw3 / geo3 / prep_jobs, before-copies `*_before_20261009*`): DROP picks 2500HX / 2502HX / 2603HX -> their
   -FG rows; body hex never dimensioned in a view that looks down a nut (1501 / 6500 / 6503 / 6600 / 6801 / 6803 / 6501 now in
   the right view); nut = NUT-feature flats in 2+ directions (6501's body arm was called NUT); title shrinks when it needs 3
   lines (2701 / 2702); note lines wrap at 92 characters; 5502 top-view label moved off the hex dimension; 2502 title
   "90 DEG MALE JIC X FEMALE PIPE ELBOW" (OMi's "MJ - FP Elbow"). Package in `10_DRAWINGS\for_OMi_2026-10-09\`:
   `OMi_dimension_check_drawings_2026-10-09.pdf` (cover + 62 pages, `combine\combine_omi.py`), `Email_to_OMi_2026-10-09.txt`
   (8 plain questions incl. the forged own-file question the user was waiting to ask; the 2404 bore question was removed 2026-10-09 - answered by the user, section 5), `OMi_missing_sizes_and_typos_2026-10-09.xlsx`
   (226 configurations only OMi can supply, 29 thread callouts that contradict the part number + NPFT / "Metric" ORB / NPTF
   swivel notes, 14 filler lengths; `tools\_out\omi_email_20261009\build_attachment.py`). Left out of the email on purpose
   (user / technical): bores wider than the port, 6801-04-02 / -12-12 (Air-Way vs Brennan), the 167 forged rows that need
   OMi data only if the own-file rule falls. Next: wave-1 polish and dry runs (below) - SolidWorks is free now.
   **2026-10-08 evening - (was) RESUME HERE (user near the usage limit; work paused / running in the background).**
   Workflow scripts: `C:\Users\sudha\.claude\projects\C--Users-sudha-OneDrive-Desktop-OMi-Handoff\3b57a418-fb1d-4dc6-b317-eef6cf16a081\workflows\scripts\`;
   resume = Workflow({scriptPath, resumeFromRunId}) - finished agents replay from cache. Same session only; in a new session
   read each workspace's own record instead.
   - **Usage limit hit 2026-10-08:** drawings STOPPED for a SolidWorks restart after the toolsmith - script v3 ready
     (`tools\_out\drawings_20261008\scripts\` geo3 / drw3 / run3 + finalize.py; how to run: the workflow result / scripts),
     6 of 62 drawn and checked (6401 1405 1501 2502HX 2650 6802 - re-run 6401 and 6802 with the final script), 56 left:
     restart SolidWorks, then batches of ~10 via run_jobs([...]) + finalize.py, read each PNG. Questions run STOPPED in its
     merge step (extracts cached in `tools\_out\questions_20261008\extract_*.json`) - resume wf_c765c441-402.
   - **Drawings of all 62 masters** (for the employer) - run wf_c5be84f9-caf (`dimension-drawings-all-masters-*.js`),
     workspace `tools\_out\drawings_20261008\` (plan\masters.json, scripts v3, results, renders), output
     `10_DRAWINGS\dimension_check_20261008\` -> combined `10_DRAWINGS\OMi_dimension_check_all_masters_2026-10-08.pdf`.
     SolidWorks leaks ~1 GB per drawing (12 GB after the toolsmith's ~10); a batch stops with needs_restart below 6 GB free
     commit - the user restarts SolidWorks, then resume.
   - **Open-questions doc for the employer** - RUNNING, run wf_c765c441-402 (`open-questions-plain-english-*.js`), output
     `tools\_out\questions_20261008\` (questions_final.json / .md). The doc: https://claude.ai/code/artifact/9d7f6978-ffb5-48d5-8076-16fd12b8dbb9
     (chart + "where things stand" filled; the other sections pending - fill one per update from questions_final.json). The
     run predates the user's ENDLIB = yes / 6 capabilities = yes: show those as decided 2026-10-08 and recount.
   - **Wave 1 (new masters)** - merged + audited, 33 configurations ready (`tools\_out\wave1_integrate_20261008\`, INTEGRATION.md,
     run wf_9db9f737-19f): next = the polish run (PAUSED, run wf_86d1cc10-86c `wave1-polish-*.js`: 2504 hex wording, stale
     rule texts, gen_tee crash on 0-row roots) -> then resume wf_9db9f737-19f with args {sw:true} for the SolidWorks dry runs
     AFTER the drawings are done (one SolidWorks job at a time) -> stage for review.
   - **Wave 2 (the 6 new shapes)** - PAUSED in design, run wf_8c9b56e4-1de (`wave2-new-shapes-*.js`, workspace
     `tools\_out\wave2_shapes_20261008\`); resume after the wave-1 polish, then args {impl:true}, later {impl:true, sw:true}.
   **2026-10-08:** batch 15 SHIPPED (section 1). Still open from the 2026-10-02 plan: **new masters wave 1 is PAUSED** (~48
   configurations built and statically checked per family in `tools\_out\newmasters_20261002\work\<family>\`, not merged, no
   SolidWorks dry runs yet - `sw_calls_*.json` + `EXPECTED.md` per family; its FOLDS 2501 table must be rebased on the batch-15
   table first). Below: the 2026-10-02 state as it was written (batch 14b and the clean-up are done).
   **Running on 2026-10-02** (overnight plan; user: "keep running"):
   - **Batch 14b = 2702 / 2703** (bulkhead hex arm 0.001 in short of the collar at -16, approved):
     `tools\_out\fix2702_20261002\` (fix + SolidWorks dry runs, 0 problems); prep 2026-10-02 12:15-12:45
     (`tools\_out\ship_20261002b\PREP.md`): fix and 2702 / 2703 review tables deployed live, ship-ready files, build calls,
     BUILD_PLAN.md. Next: the real builds, then ship like batch 14. Its paperwork must say that undoing batch 14's tools now
     needs 14b undone first (section 1, Toolchain) and add `fix2702_20261002/` / `ship_20261002b/` to the CLAUDE.md protected list.
   - **New masters, wave 1** (user: "yes, go ahead", largest family first, from the Brennan pilot STEPs; 21 families with a
     pilot and no new generator capability): `tools\_out\newmasters_20261002\`, write-up to come in
     `00_DOCS\NewMasters_Wave1_2026-10-02.md`. Built into STAGING for review; rows whose body values exist only at Brennan
     are prepared but stay MISSING until Q-BRENNAN-ONLY.
   - Also planned for the morning review: batch 15 (72 catalog-settled OMi rows + 5 -FG STEP rows) staged; then the folder
     clean-up the user asked for ("get rid of things not needed" = move to `_to_delete\<dated reason>\`, never delete; keep
     the protected / referenced folders, incl. `tools\_out\ship_20261002\` with its `old_files\`, `tools\_out\tier1_20261001\`
     (the SolidWorks dry runs batch 14 was checked against, the held-out 5404N-06 fix) and the batch-14b folders
     `tools\_out\fix2702_20261002\` / `ship_20261002b\`).
1. **Questions waiting for the user.** Unblock analysis 2026-10-08 (`tools\_out\unblock_20261008\`: `summary.txt`, `rows.csv` = every
   unbuilt BUILD row with its user gates and my work; `unblock.py` re-runs it): 763 rows not in a built file (760 + the 3 unbuilt
   5405). No user action needed: 51 (48 wave 1 + 3). Q-BRENNAN-ONLY = yes alone frees 76 more (24 of the 25 batch-15 held rows,
   37 prepared wave-1 sizes); it is a gate of ~435 rows. Greedy order after it: STEP downloads (~78 files, +89), Q-TRANSFER-ENDLIB
   (+54), capabilities Q-NEW-HOSEB (+39) / Q-NEW-ANGLEDHELIX (+37) / Q-NEW-PERLEGSW (+32), Q-SCOPE-TUBE (68 rows), Q-SOP5 (+48),
   Q-TRANSFER-TAPDRILL (+31), then ~15 small questions (~+90); ~127 stay (5404N bundle, O-rings, 1703 / 1704 flange legs, blocked).
   Counts rest on the 2026-10-01 catalog impact files + the wave-1 / batch-15 notes - approximate.
   - The 36 questions of `00_DOCS/NEXT_SESSION_PROMPT_2026-09-26.md`. Answered so far: 1 (ship Task A: yes = batch 14),
     4 (6410-12-08-O 1.480: shipped with Task A), 24 (2702 / 2703 offset: yes). **Q-31 (1404 bores) is still open:** batch
     14 shipped OMi's 17 bore cells; if the answer is Air-Way, revert them from
     `tools\_out\omi_apply_20260925\originals_before_apply\`, regenerate 1404, dry-run, rebuild. Q-32: 6404-10-08 shipped at
     OMi 1.750 (Brennan 1.740) - note Brennan in `$COMMENT` once answered. Q-2: the 10 held OMi bores.
   - Tier-1 questions (`00_DOCS/Tier1_Fixes_2026-10-01.md` section 3): Q-SPECS-5, Q-THREAD (6565-32-32), Q-BOREWIDE
     (6410-32-24-O), Q-PLACEHOLDER, Q-TRANSFER-5404N, Q-NEW-5404N-NAME, Q-SIZE40-JIC, Q-B-ELBOW, Q-B-SWELB, the -02 swivel
     bodies. Q-NEW-ASME40 is answered: Brennan-measured -40 threads (section 5). Q-SPECS-2 / Q-2404-BORE wait for OMi.
   - **Q-BRENNAN-ONLY** (~70 rows: may a row be built from Brennan alone, catalog or STEP, as ASSUMED?) - user: "later". It
     gates the open 2403 / 2405 / 2404-L rows, 6405 -02, 2406-03-04, the wave-1 Brennan-only rows and others.
   - Hex A/F: Air-Way 2-decimal values vs the wrench fraction (question 23).
   - The catalog questions in `00_DOCS/Brennan_Catalog_2026-10-01.md` (e.g. Q-NEW-F3-FLARELESS-ALIAS: 0618-08 / 0619-08 ->
     V0318-08 / V0319-08?).
2. **Brennan data (2026-10-01 / 02):**
   - Catalogs: 7 PDFs in `07_RAW_EXTRACTS/brennan_catalogs/` (user: "use any needed"), parsed and checked page by page in
     `tools/_out/brennan_catalog_20261001/` (427 tables, 5,056 rows; `catalog_verified.json` / `.xlsx`). Catalog values are
     the same source as OMi (Brennan) -> ASSUMED. Report: `00_DOCS/Brennan_Catalog_2026-10-01.md`.
   - **STEP list FINAL:** `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` / `.md`: Download now 96 (incl. 5404-N-06X2.000),
     Later 283, Conditional-Optional 57, Replaced by catalog 125, Already in repo 64.
   - **57 STEPs received 2026-10-02** (in `09_STEP_FILES`; manifest `tools/_out/step_ingest_20261002/MANIFEST_sha256.txt`):
     the 4 tier-1 geometry STEPs (6500-02-02-FG, 6506-12-14, 2406-03-04, 6410-04-02-O - MEASURED-ENDS can start: validate
     `swiv.py` / `ports.py` first), 33 pilots, 2501-40-40-FG / 5000-40-40 / 5404-40-40 / 5406-40-32, 2404-L-32-32,
     6565-32-32, 6802-32-32, 6410-32-12 / -16, 1700 x3, 2700-02-02, 2701-02-02 / -05-05, 2702-20-20, 2706-04-02,
     6801-16-08 / -24-32 (+ 2406-12-06 by mistake, kept).
   - **15 more STEPs coming** when the user's download limit resets: the 6801-L / -LL, 6805 6806 6807 6809 6810 6815 6832
     6835 6901 6902 pilots.
   - **No Brennan file for 26 part numbers** (user, 2026-10-02): 1405-20-24, 2403-06-02, 2502-20-16-FG, 2700-04 / -08 / -10 /
     -12 small, 2705-04-02, 6500-20-16 / -24-20 / -32-24-FG, 6501-16-12-FG, 6502-06-04 / -12-10-FG, 6802-04-02-NWO-FG,
     1602-08-08-08-FG, 1803-08-08-FG, 2406-06-12, 5404-L-04X2.000, 5404-N-06X2.000, 5404-R-04-04-047, 6425-08-08,
     6500-04-02-FG, 6502-04-02-FG, 6505-04-02, 6566-06-06-FG - the user will ask OMi for drawings.
3. **Tier-1 rows still waiting** (code ready and TEST-proven unless noted; `Tier1_Fixes` section 1): 6565-32-32 (Q-THREAD;
   STEP received), 6410-32-24-O (Q-BOREWIDE), 6802-32-32-NWO-FG (measure the received STEP), 6502-16-12-FG (Q-B-SWELB),
   6405-02-02-O / -02-04-O (data; Q-BRENNAN-ONLY), the -40 rows 2501-40-40-FG / 5000-40-40 / 5404-40-40 / 5406-40-32
   (Brennan-measured threads accepted; measure the received STEPs), the MEASURED-ENDS rows 6505-04-02, 2406-03-04,
   6410-04-02-O, 6506-12-14 (STEPs received) and 6500-04-02-FG / 6502-04-02-FG (no Brennan file, no dimensions anywhere).
4. **5404N-06** (8 rows, QA #163): the round-bar fix builds bodies, but its threads fail at -06 in SolidWorks; held out of
   the deploy. Brennan has no file for 5404-N-06X2.000. Needs a new look at the thread end.
5. **2404 / 2404-L: held until OMi clarifies the bores** (user 2026-10-02, QA #164). Then Q-SPECS-2, Q-2404-BORE, the 2404-L
   fold (Brennan 2404-L-08-08 and -32-32 STEPs are in the repo) and question 26 (10 OMi differences on 2404 / 6400). Leave
   2404 out of any "regenerate all" ship until then. **6400-L:** own master or a new feature? (ask the user).
6. **Re-run Build_5405** for 5405-12-08 / -16-08 / -16-12 (in its table since batch 11, not in the built file; question 30:
   dry-run into staging).
7. **6801-L / 6801-LL** (one topology with 6801). Air-Way gives only the long ORB leg (M11/M12), with no I3. The Brennan
   6801-L / -LL pilots are among the 15 STEPs coming; then fold them in (as 2501L). Note: the 6801-LL-08-08-NWO-FG Air-Way
   row looks like a -10 row.
8. **Other adjustable-ORB families**, whose tables exist: 6805 (x female NPTF), 6806 (x male NPTF), 6807 (ORB x ORB),
   6901/6902 (x NPSM swivel), 4601/4603 (hose barb). They need I3, THDL and groove dia (6801 values per ORB size, logged
   as an assumption) and more leg kinds. The NWO module is proven in SolidWorks; their pilots are coming.
9. **Blocked configurations still out** (6502-05/-12, 6565-20/-24, 6504-24-24 and 6410-20-12/-20-16/-24-16 are built since
   batch 14):
   - 1501-04-02-FG: bore vs the -02 stem tip.
   - 1501-24-24-FG: Air-Way nut 1.88 vs Brennan 2.125. Ask the user.
   - 2406-16-04: the port wall.
   - 6802-04-06-NWO-FG: Air-Way nut hex 0.56 for a -06 ORB, which needs 0.6875.
   - 6405-32-24-O: Air-Way D3 2.38 misprint (needs a STEP).
   - 6801-05-05 (question 25).
   - The 10 held OMi bores wider than the female port (question 2) and 6405-20-16-O (OMi length 1.000 = placeholder).
10. **1503**, and later 5503/5505: the angled leg needs a pipe (helix) thread helper. `gen_tee.py 1503` stops with
    "angled leg must carry a Thread-feature (JIC) end".
11. **-FG (forged) parts with only non-forged Air-Way rows (about 260).** Wait for Brennan -FG STEPs; do not build them
    from the non-forged dimensions (the user agreed). The coverage workbook lists the STEPs needed per series.
12. Smaller items:
    - `tools/README.md`: add the tier-1 tools (`measure/jicm.py`, `neck45.py`, `e45_model.py`, `swiv.py --model`) and
      `JIC_MEAS_40` / `ORB_FROM_6408_ROW` under "Measured end data" (`Tier1_Fixes` section 7 step 8) - not done with batch 14.
    - Copy the Brennan 2404 STEPs that tier 1 measured into `09_STEP_FILES` (15 ready-named files in
      `tools/_out/tier1_20261001/integrated/review_fix/steps/`; the user's folder).
    - 0306 bulkhead locknut, 0304-C cap nut, 6408-HHP: in new masters wave 1 (groups NUTS-CAPS, PLUGS).
    - Optional port countersink.
    - Series with no Air-Way page (6815, 6832, 6835 and others) need a dimensional source (pilots coming).
    - 45 deg elbows (2503, 6502, 6802) leave the leg plane `PLN2` and an axis sketch line visible - hide them.
    - Helix curves of suppressed threads show (blue) in saved parts - cosmetic.
    - SolidWorks volumes of the JIC -06 configurations are smaller than the OCP rebuild (6802-06-04 / -06-06 and
      6502-06-06-FG by 0.0136 in^3, 6801-06-xx by 0.0272) - compare sections some time.
    - Report to OMi (question 29): wrong thread callouts, 1.000 placeholders, reducer bores wider than the port, the 6801
      findings, OMi file typos.

## 4. Housekeeping

**SolidWorks** ended the overnight build at 11 GB after a "critically low on committed memory" warning (answered No).
Restart it before the next MCP build; a VBA editor window "test" was open - check it is not the user's unsaved work.

**0318.** DONE 2026-09-25: the overnight rebuild (opens in 0318-08) is now `11_MASTERS\0318_MASTER.SLDPRT`. The user
had run the stale 0318 module from the VBA editor twice (01:19 and again 20:08 on 2026-09-25 - reports without the
"Master left in its reference configuration" line); those builds, their report and the duplicate saves `_011925` /
`_200845` are in `_to_delete\superseded_20260925\`. **Remove the old Build_0318 module from the VBA editor before any
manual re-run** (it is still loaded there - that is what ran at 20:08).

**VBA import trap.** If the old module is not removed first, importing a `.bas` whose `Attribute VB_Name` already
exists creates `..._MASTER1`, and running the entry sub may run the OLD module. RUN_ME files always say "remove any old
module of the same name first". Builds through the MCP `run_macro` cannot hit this (it compiles the `.bas` on disk).

**The root folder** holds a 6-byte stale SolidWorks owner file, `~$2403_MASTER_macro_153206.SLDPRT` (2026-09-16). It is
harmless; move it to `_to_delete` when SolidWorks is closed.

## 5. User decisions on record

- ~~6410-12-08-O stays at Air-Way 1.09.~~ Superseded 2026-10-02: shipped at OMi 1.480 (= Brennan) with Task A ("yes to
  all", question 4 of 2026-09-26).
- 1404 / 1405: the swivel nut face sits at Air-Way W (Air-Way over Brennan). 1700 follows Air-Way.
- 0403: OMi's plated parts are built from the Air-Way UNPL rows of the same size ("Yes, map them").
- 2404-L, 6400-L and 2501-L are folded into their base masters ("Yes, all three"); regenerating the hand-built 2404/6400
  is allowed. (2501-L: folded, batch 13b. 2404 / 2404-L: on hold since 2026-10-02 until OMi clarifies the bores.)
- -FG parts that exist only as non-forged Air-Way rows: wait for Brennan -FG STEPs. Do not build shapes from the
  non-forged dimensions.
- The 5504 collar "looks too big" question: it matches Brennan. The real cause was the master opening in its smallest
  size, so every macro now saves in its reference configuration.
- 2026-09-25 (night): build every not-yet-built macro for real in SolidWorks and save the good parts in a separate
  folder "just like masters" for review in the morning (done: `11_MASTERS_NEW`).
- 2026-09-25 (evening): "accept the overnight build masters into 11_MASTERS" - done (38 parts, section 1). Then "yes
  ship": batch 13b + the regenerated 6404 / 6504 / 6565 shipped (QA #156).
- 2026-09-25 (evening): **OMi dimensions rank ABOVE Air-Way** ("OMi is more important than airway dimensions"), and
  **rounding-only differences are fine** (no change where OMi only differs by rounding to Air-Way's printed decimals, incl.
  the exact-fraction cases and the 15 differences that match when OMi is cut to Air-Way's decimals - QA #158). This changes
  the source order in CLAUDE.md ("Air-Way decides DIMENSIONS"): where both give a value, OMi's is used; Air-Way fills what OMi
  does not give. User, same evening: "OMi is only in charge of dimensions, for geometry use Brennan" (end shapes, forged
  bodies, seats, nuts, ports stay Brennan-derived). Evidence for the user's question to OMi: OMi's overall length equals the
  Brennan STEP length on 20 of 22 straights (Air-Way on 5) and the 6500 legs on 10/10 - OMi very likely uses Brennan's data. APPLIED since as Task A (173 of the 184 phase-A cells in 18 review
  tables, 11 held; shipped in batch 14 on 2026-10-02) - of the 220 real differences on certain mappings
  (00_DOCS/OMi_Dimension_Audit_2026-09-25.xlsx). Open at the time: (a) confirm the two earlier decisions it reverses -
  6410-12-08-O at Air-Way 1.09 (OMi 1.480) and the 1404 / 1405 nut face at Air-Way W; (b) does it cover the -FG rows (F1: OMi
  has data for 70 of 260; 46 have a master and all end modules)? (c) the uncertain leg mappings on elbows / tees (OMi M 1 / M 2
  / L 1 in side order) - without them no leg length comes from OMi; (d) DataStatus: OMi alone = ASSUMED; OMi + Air-Way
  agreeing = VERIFIED? (is OMi independent - audit section 3.6).
- 2026-10-01: Brennan catalogs (https://brennaninc.com/catalogs/): **"use any needed"**. Catalog values are the same source
  as OMi (Brennan) -> ASSUMED (Q-NEW-BRENNANCAT treated as yes).
- 2026-10-01: **"do the tier one fixes"** (the 14 tier-1 work groups of Task C; `00_DOCS/Tier1_Fixes_2026-10-01.md`).
- 2026-10-02: **"yes to all"** = ship batch 14: Task A (18 roots; question 1 of 2026-09-26) + the tier-1 fixes 6502 6802
  6404 6410 6565 + the new SPECs 2403 / 2405 (2404 then excluded, next item); **Q-SPECS-1 yes** (2403 / 2405 drop their
  15 / 4 DROP configurations). Task A shipped as staged: 6410-12-08-O at OMi 1.480 (question 4), the 1404 bores at OMi
  (Q-31 still open), 6404-10-08 at OMi 1.750 (Q-32). Built and shipped the same day (QA #159-#164).
- 2026-10-02: **2404 held: "keep 2404 exactly as it is"** until OMi clarifies the bores - hand-built master and tables
  untouched (incl. 2404-40-32's VERIFIED); Q-SPECS-2 / Q-2404-BORE on hold; the 2404-L rows wait with it.
- 2026-10-02: **-40 sizes: Brennan-measured threads are accepted** (the answer to "ASME B1.20.1 row or Brennan-measured?");
  threads only need to show on drawings.
- 2026-10-02: **Q-BRENNAN-ONLY: "later".** Rows whose values exist only at Brennan stay MISSING (values may be prepared in
  proposal files).
- 2026-10-02: parts with no Brennan file (26, section 3): the user will ask OMi.
- 2026-10-02: **2702 / 2703: stop the bulkhead hex arm 0.001 in short of the collar** at -16 ("okay"; question 24) ->
  batch 14b.
- 2026-10-02: **new masters: "yes, go ahead"**, largest family first, from the Brennan pilot STEPs (wave 1); build into
  staging for review.
- 2026-10-02 (night): "keep running": ship batch 14 (+ 2702 / 2703), stage wave 1 + batch 15 for the morning review, then
  clean up the folder ("get rid of things not needed" = move to `_to_delete\<dated reason>\`, never delete).
- 2026-10-08: **"ship batch"** = ship batch 15 as staged (done; QA #167-#169). The 5604 / 5605 collar re-run (QA #144) went with it.
- 2026-10-08: **Q-BRENNAN-ONLY = NO: "You cannot use Brennan data as your own."** No dimension may come from Brennan alone
  (catalog or 3D file). Rows whose values exist only at Brennan stay MISSING and need OMi's own dimensions / drawings (or
  Air-Way). The prepared Brennan-only proposals (batch-15 held rows, wave-1 PROPOSAL files) are NOT to be applied. Asked the
  same day about the "forged -FG part from its own Brennan 3D file" rule: **"keep for now until I send the pdfs to my employer
  so they can look at it and give feedback"** = the 6 shipped own-file configurations (2702-20-20-FG, 2701-02-02-FG,
  2701-05-05-FG, 6801-16-08-NWO-FG, 6801-24-32-NWO-FG, 6802-32-32-NWO-FG) stay as built; no NEW size from a Brennan file (the 7
  wave-1 pilots stay held) until the employer's feedback on the drawings. **Brennan 3D files for SHAPE only** (end forms, body
  form; sizes from OMi / Air-Way): **"Yes, shape is fine"** (re-confirmed 2026-10-08). Same day: "finish the new masters that
  need no decision" = wave 1 minus every Brennan-only row (~41 configurations).
- 2026-10-08: **Q-TRANSFER-ENDLIB = YES** ("Reuse already-measured end details - yes"): new masters take their end details
  (thread majors, tap drills, JIC / pipe / NPSM / swivel / adjustable-ORB / flange end data, female ORB port shape) from the
  existing end libraries, as on the built masters, instead of measuring each part's own 3D file. Sizes of the part body still
  only from OMi / Air-Way.
- 2026-10-08: **the 6 new generator capabilities = YES, "go ahead"**: Q-NEW-ANGLEDHELIX (thread on a 45 deg leg: 1503 1504
  5501 5503 5505 6810 6902), Q-NEW-HOSEB (hose-barb elbow leg: 4501 4503 4601 4603), Q-NEW-PERLEGSW (several swivel /
  adjustable-ORB legs on one part: 1601 1602 1603 6603 6606 6807 6566), Q-NEW-ANGLEDFEMALE (female pipe port on a 45 deg leg:
  5505 1504), Q-NEW-FLG61LEG (code 61 flange leg on elbows: 1703 1704), Q-NEW-ANGLEDNUT (swivel nut on a 45 deg leg: 6810 6902).
  Work = wave 2 (`tools\_out\wave2_shapes_20261008\`), built on the wave-1 merged toolchain, staged for review.
- 2026-10-09: **Q-2404-BORE answered by the user (from talking with OMi): the 2404 hole "isn't the same throughout"** = two
  bores, a larger one stepping down to a smaller one (option (b) of `00_DOCS\Tier1_Fixes_2026-10-01.md` s3), not one straight
  hole. Removed from the OMi email. Releases the 2404 hold of 2026-10-02 for the bores: the 24 HELD rows (now built with ONE bore
  in the hand-made master) get the step, + 2404-L x5 and the 4 "CB depth unsourced" rows (2404-02-04 / -08-02 / -16-32 / -32-20)
  become buildable; 2404-32-48 / 2404-40-40 still wait for the -48 / -40 pipe-end lengths. Still open before 2404 can be
  regenerated: where the step sits on sizes MS51500G does not list (default proposed: the hex mid-plane, Brennan's construction
  = shape), Q-SPECS-2 (library NPTF cone instead of the plain pipe end) and 2404-24-20 (OMi lists 1.25 / 1.25, Air-Way 1.31 / 1.25).

- 2026-10-14: **OMi answered question 8 of the 2026-10-09 email: "Yes we need drawings of ORings, Bent Tube, and Flareless nuts
  and sleeves."** = Q-SCOPE-ORING / Q36-20 yes, Q-SCOPE-TUBE / Q36-21 yes (now, own masters), Q-NEW-FLARELESS-N3 now. Drawings come
  from masters, so: new masters for 4000 / 4001 / 4005, the -Tube rows of 1703 / 1704 / 1803 / 1804 + 6701 (6701-L folded in),
  0618 / 0619, then dimension-check drawings. Read as also settling, for these families only, SOP step 5 (no hex) and
  carbon-steel-only (O-rings are rubber) - to confirm with the user; Q-SOP5 for plugs / collars stays open. Sizes still need
  OMi (request drafted 2026-10-14) - the 2026-10-08 Brennan rule stands. Scope: `00_DOCS\Scope_ORings_BentTube_Flareless_2026-10-14.md`.

## 6. Conventions that grew during the build (keep them)

**Sources and data status:**
- Dimensions (lengths, legs, hexes, bores): the OMi dimension file first, Air-Way fills what OMi does not give (user
  2026-09-25; rounding-only differences are no change). Geometry (end shapes: swivel nut, ports, NPSM, flange head,
  adjustable ORB; forged bodies, seats): Brennan STEPs, which also cross-check the dimensions.
- OMi and Brennan count as ONE source (OMi's lengths are Brennan's data, evidence 2026-09-26); Brennan catalog values are
  the same source. A row taking an OMi or catalog value is ASSUMED, with the cell, the old value and the decision in
  `$PRP@AxialSource` (Task A form: "<col>: OMi WebsitePartsInfo2026.xlsx Items!<cell> <header> = <v> (table had <old>)
  [user 2026-09-25: OMi dims > Air-Way, ASSUMED]").
- A shape from one manufacturer makes the row ASSUMED. Differences between the dimension source and Brennan are built to
  the dimension source and written in `$COMMENT`; an OMi value that cannot be built (e.g. a bore wider than the port it
  drills into) is held at the old value with the reason in `$COMMENT`.
- Measuring scripts are validated first: each must reproduce the sizes already measured before it is used on new ones.
- Every modelling assumption goes into `$PRP@AxialSource` of each row. Blocked configurations stay out of the table,
  with the reason in the generator summary and the RUN_ME.

**Macros:**
- Threads stay live through all checks and the all-configuration sweep, then every `THD_*` is suppressed before the save.
- The master is saved in its reference configuration (`progress_patch.ref_config_at_save`).
- The save step trusts the file date when SaveAs returns False.
- One report line per configuration comes from `progress_patch.add_progress`.
- Since the overnight generator fixes (regenerated set): a rejected sketch dimension is really deleted; an angle whose
  two lines do not meet is held by a driving `<name>_SUPPL` (its supplement); the helix start is read from the helix
  curve; the problem count only counts real FAIL lines.
- A master built from a pre-fix macro whose report shows "angle try" lines has a named angle that is DRIVEN (its table
  column does nothing - harmless while the column is constant, e.g. RELIEFANG 60 in 0403 2502HX 2601 2602 2605 2650 and
  most overnight parts). Rebuild it from a regenerated macro before that angle ever changes in a table.
- Since tier 1 (2026-10-02): revolve cuts are used where a forged corner must be turned clear (6502 NECKTRIM1 + NECKFILL1
  in every configuration; 6802 ORBTRIM only where a configuration needs it); the report gives the API return of each.
  Construction margins are check values only, never part dimensions.
- The live toolchain carries an unused 2404 SPEC (since 2026-10-02): leave 2404 out of every ship until the user answers.

**Shipping a batch:**
- A shipped batch contains the macros, the SW2 tables, `RUN_ME_batch<N>.txt`, QA_Log rows (numbered, next is #170),
  Topologies notes, a coverage refresh and this file.
- Superseded files go to `_to_delete\superseded_<date>\<reason>` AND a copy under `tools\_out\<ship folder>\old_files\`
  (sha256 MANIFEST in both; the user empties `_to_delete`). Never delete files.
- Before shipping: every old configuration is unchanged (`checks/regress.py`), every configuration's outline is clean
  (`checks/allcfg_check.py`), the sketches are fully defined (`checks/dofcheck_*.py`), and the static VBA check passes
  (`checks/vbacheck.py`, which now also rejects more than 24 line continuations). New or changed masters also go
  through the SolidWorks verify loop in `CLAUDE.md`.
- A real build through the MCP (only with the user's approval): close the old master, move the old files out, copy the
  checked macro + SW2 in, `run_macro` with no overrides, then `sweep_configs` of the saved part and `sweep_cmp.py` against
  its dry run - every configuration must be identical (1e-5).
- A part built by a dry run into staging may ship unchanged (moved, same sha256) when the shipped macro + SW2 are the ones
  that built it (a regeneration may differ only in the date line); its report keeps the staging "Saved to" line.
- A fix that fails in SolidWorks is held out of a deploy by reverting only its hunks, with an attribution check that every
  other fix keeps every line (5404N-06, 2026-10-02).
- MasterData workbook edits: back it up twice, edit with openpyxl (the file is an openpyxl 3.1.5 file), then prove that only
  the intended cells and XML parts changed (`tools\_out\ship_20261002\paperwork\update_masterdata.py`).

## 7. History

The complete Cowork workspace (generators with every intermediate version, all batch packages, regression outputs,
Brennan STEP measuring scratch, the conversation transcript and the skill) is archived in
`_archive\cloud_workspace_2026-09-25_part{1,2,3}of3.zip`. It unpacks to one folder `cloud_workspace_2026-09-25\` with a
MANIFEST_sha256.txt. The coverage scripts, previously held only inside the Cowork VM, are in
`_archive\device_vm_enum_2026-09-25` and, made portable, in `tools\coverage`.

2026-09-25 night: Claude's overnight SolidWorks build - write-up `00_DOCS\OVERNIGHT_BUILD_2026-09-25.md`. The files
changed overnight (generators, templates, sp3fix, vbacheck) and in the follow-up the same day (CLAUDE.md, this file,
tools/README.md)
have their previous versions in `_to_delete\superseded_20260925\`.

2026-10-02: batch 14. The toolchain before the tier-1 deploy is in `_to_delete\superseded_20261002\tier1_toolchain_before\`
and `tools\_out\ship_20261002\tools_before\`. The replaced macros, reports, SW2 tables and masters, and the previous
versions of this file, `CLAUDE.md`, the MasterData workbook, the coverage workbook (and its `tools\coverage\work` json) and
`11_MASTERS_NEW\README.txt` are in `_to_delete\superseded_20261002\batch14_replaced\` and
`tools\_out\ship_20261002\old_files\` (MANIFEST.txt, MANIFEST_paperwork.txt). Later that day the batch-14b prep replaced the
live `gen_tee.py` and the 2702 / 2703 review tables (old versions: `_to_delete\superseded_20261002\batch14b_replaced\`,
`tools\_out\ship_20261002b\old_files\`), and the fix of the batch-14 paperwork changed this file and `CLAUDE.md` again (old
versions in `paperwork_fix\` under both batch-14 folders, MANIFEST_paperwork_fix.txt).

2026-10-08: batch 15 (`tools\_out\ship_20261008\`: `scripts\` verify / compare / ship scripts, `checks\` evidence, `paperwork\`
MasterData + coverage + counts). The replaced masters, macros, reports, SW2 and review tables are in
`_to_delete\superseded_20261008\batch15_replaced\` and `tools\_out\ship_20261008\old_files\` (MANIFEST.txt, MANIFEST_5604_5605.txt,
MANIFEST_2601.txt); the paperwork files before the edit (MasterData, coverage workbook + `tools\coverage\work`, this file, CLAUDE.md,
the 11_MASTERS_NEW README, NEXT_SESSION_PROMPT_2026-10-01.md) in `paperwork\` under both (MANIFEST_paperwork.txt).
