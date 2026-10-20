# Next session - start here (written 2026-10-19; covers the long session of 2026-10-18 / 19)

Read `CLAUDE.md`, then this file, then `00_DOCS/PROJECT_STATUS.md` (section 1 top and section 5, entries of 2026-10-18).
**Nothing has shipped since batch 15** (2026-10-08). Everything below is STAGED under `tools/_out/`.

**SolidWorks is blocked on this PC:** it signs in to 3DEXPERIENCE, fails the license check and closes.
- The roles (CSV, X1W, IFW) and the license servers are unchanged since 10-14.
- Details: the session "Ship batch 16" of 2026-10-18.
- The user has to fix the sign-in before any dry run or ship.

**Cloud sessions** (repo github.com/sud12344/OmiHandoff, private): Python side only, never SolidWorks. See `CLOUD_SETUP.md`.
The user's Claude memory files are NOT in the repo; everything needed is in these docs.

## What was decided on 2026-10-18 (all in PROJECT_STATUS s5 and `00_DOCS/ANSWERS_2026-10-18.md`)
- **Brennan data is ALLOWED** ("yes use brennan but still differentiate the two in tables").
  - Brennan rows: `$PRP@DimSource` = `BRENNAN`, AxialSource prefix `[BRENNAN-ONLY 2026-10-18]`, DataStatus ASSUMED.
  - To undo: `tools/_out/brennan_yes_20261018/scripts/revert_brennan.py`.
- **OMi answered the 2026-10-09 request** (14 Brennan-format drawings, real lengths, typo answers).
  - Staged and marked VERIFIED (A23-1); `tools/_out/omi_answers_20261018/`.
- **Open questions A1-A24 answered** ("do the recommended thing unless I put a caveat"); A9 = wait for BRENNAN_5405-24-24 / -32-32.
  - A19: OMi values on 134 built-configuration cells applied.
  - 5 1404 nut faces kept at Air-Way and reported to OMi.
  - Q-FS-XFER yes.
  - 7 extra pending OMi values applied.
- **OMi-only questions are collected (unsent):** `10_DRAWINGS/for_OMi_LATER/QUESTIONS_FOR_OMi.md`.
- **Still open from the user:**
  - Q-CODE62-CAT: code 62 heads -12..-32 from Brennan catalog table 3300-62?
  - The -40 thread derivation.
  - 6400 rebuild details.
  - Bent-tube tube OD / bend radius / bore source.
  - Q-PLUG-SQHEAD.
  - The flagged shape calls (6902-12-12-NWO-FG composed body, 5505-20-20-FG on the -08 shape).

  The rest is in `OPEN_QUESTIONS_2026-10-18.md` (group A answered; B moved to the OMi file; C / D open).

## Where the work stands
- **The table set for batch 17:** `tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES` = batch-16 staging + OMi answers + Brennan rows (waves
  1-3) + A19-A23 + dropped adapters + the rows of the new generator features.
  - Log of every cell: `stage/CHANGES.csv`.
  - 1,377 BUILD rows with data, 310 VERIFIED, 440 MISSING.
- **The toolset for batch 17:** `tools/_out/genfeat_20261018/merged/tools`. Five features merged and proven:
  - hose barb 4501 / 4503 / 4601 / 4603;
  - flange legs 1703 / 1704 / 1803 / 1804 + 1700RC + 1724 / 1800 / 1824;
  - angled 45 deg legs (1503 1504 5501 5503 5505 6902 6810);
  - per-leg swivels (1601 1602 1603 6606 6807);
  - straights (5404N with OMi names, -40 pipe end, 6400 SPEC with 6400-L, -02 female ORB port).
  - Proof: `merged/MERGE_LOG.txt`, `verify/`, `regen/`.
- **Regeneration of every root** (`tools/_out/brennan_yes_20261018/regen_genfeat/cmp.txt`): **1,357 configurations generate** (1,166 with the
  batch-16 tools; 1,044 built today); 0 existing configurations changed.
- **ORFS:** `tools/_out/brennan_yes_20261018/stage_orfs` - 57 more FS rows complete (326 of 385 with data). There is no ORFS generator
  yet: it waits for the 9 pilot STEPs.
- **Bent tubes:** 338 data cells prepared (`wave3/benttube`); 0 buildable (no source for tube OD / bend radius / bore).
- **Downloads the user owes:** `tools/_out/brennan_yes_20261018/3D_FILES_NEEDED.md`, in this order:
  - 9 ORFS pilots;
  - 5405-24-24 / -32-32 for A9;
  - 10 only-source files;
  - flange-elbow own files;
  - 214 shape files.

## Next steps
1. **The user fixes the SolidWorks sign-in; then the "Ship batch 16" session** re-runs the puck-fix dry runs and ships batch 16 as staged.
2. **Batch 17** = the stage + the merged tools.
   - SolidWorks dry runs: CLAUDE.md verify loop; one root per `run_macro` call where helices are heavy.
   - Never tried in SolidWorks: the hose-barb face-off, threads on 45 deg legs, the NPSM nut on leg 2 of the 160x tees, 5404N -06 threads.
   - Ship per CLAUDE.md with RUN_ME_batch17.
   - Re-word the stale "BUILD-NEAR / MISSING" comments on now-built rows at ship time.
3. **Python work a cloud session can do now:**
   - ~~measure the 1603-08-08-08-FG range bores from its STEP (A14)~~ DONE 2026-10-20: 0.450 / 0.450, row staged
     (`tools/_out/a14_1603bore_20261020/README.md`; 1603 now 6 of 6 -FG rows generate);
   - prepare the 3474 family (toolchain never merged);
   - re-count the whole catalog (`tools/_out/adapters77_20261016/scripts/possible_2535.py` needs updating for today's decisions);
   - stage new data as the user downloads STEPs.
