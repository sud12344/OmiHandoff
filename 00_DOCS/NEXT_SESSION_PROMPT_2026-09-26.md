# Next session - start here (written 2026-09-26 ~03:15, end of the Task A / B / C + drawings session)

Read `CLAUDE.md`, then this file, then `00_DOCS/PROJECT_STATUS.md` (section 3 item 0 and section 5). The previous handoff
`00_DOCS/NEXT_SESSION_PROMPT_OMi_apply_2026-09-26.md` is DONE except where this file says otherwise.

## 1. What happened this session (nothing shipped, 11_MASTERS untouched)

**Task A - OMi values applied (user decision 2026-09-25: OMi dims > Air-Way, Brennan geometry, rounding-only = no change,
OMi rows ASSUMED).** Details + tables: `tools/_out/omi_apply_20260925/TaskA_result.md`.
- The review tables `04_DESIGN_TABLES/DesignTable_<root>.xlsx` of 18 roots ARE EDITED: 173 of the 184 phaseA cells written
  (source in `$PRP@AxialSource`, DataStatus ASSUMED); 2501-32-32-FG MISSING -> ASSUMED (drill conflict settled by OMi-first).
  11 cells HELD (value kept, reason in `$COMMENT`, `held.json`): 10 OMi bores wider than the female port / pocket
  (6405-12-04 / -12-06 / -32-20 / -32-24, 6410-10-04 / -12-06 / -20-12 / -20-16 / -24-12 / -24-16) and 6405-20-16-O OMi
  length 1.000 (placeholder). Originals + sha256: `tools/_out/omi_apply_20260925/originals_before_apply/` (the copy in
  `_to_delete` went to the Recycle Bin with the user's clean-up at 23:03).
- Regenerated macros + SW2: `tools/_out/omi_apply_20260925/after/{straight,tee}` (baseline from the unedited tables:
  `before/`). Static checks clean (`checks/`), `diff_report.txt` proves only the intended cells changed; independent
  re-check 184/184 confirmed (`verifyA_cells/`, `verifyA_completeness/`).
- **SolidWorks dry runs STAGED in `11_MASTERS_NEW`** (18 parts `<root>_MASTER.SLDPRT` + `reports/`), 0 FAIL lines,
  324 -> 329 configurations: 138 changed as intended, 186 identical to 11_MASTERS, 5 new (6405-24-16-O, 6504-24-24,
  6565-10-10, 2501-32-32-FG unblocked by OMi; 6401-32-32-O finally rebuilt). Compare: `dryrun/compare_all.txt`.
- Found by the completeness check, NOT yet noted in `$COMMENT` (waiting for questions 31 / 32): 1404 OMi bores are
  0.01-0.05 smaller than Brennan on all 8 parts with a STEP; 6404-10-08 OMi 1.750 vs Brennan 1.740.
- Reversed earlier decision (question 4): 6410-12-08-O length 1.09 -> 1.480 (= Brennan).

**Task B - leg-column readings:** evidence per reading (cells changed / filled) in `tools/_out/omi_apply_20260925/taskB/`
(`readings.txt`, `readings.json`); Brennan 1404 STEPs have ONE hex size = OMi Hex Flat (`scripts/b2_hex1404.py`).
Nothing applied - waiting for the user (questions 5-15).

**Task C - the 727 MISSING configurations re-sorted** (6 groups + 6 independent checkers + merge):
`tools/_out/omi_apply_20260925/taskC/TaskC_resort.md` (readable) and `taskC_merged.json` (rows, questions, staged Brennan
STEP list with exact part numbers, work groups). Counts: RESOLVED tonight 1, NOW 4 (6401-16-20-O, -20-16-O, -24-20-O,
6504-06-08), DECIDE 120 (no downloads, just answers), STEP 105 (98 downloads, stage 1a), WORK 399, SCOPE 98.

**OMi vs Brennan tally** (previous session's workflow, finished 22:45): OMi lengths are Brennan's (14/14 clean cells;
part numbers = Brennan numbering). OMi + Brennan = ONE source.

**20 dimension-check drawings for the user's employer** - DONE, user said "fine for now":
`10_DRAWINGS/OMi_dimension_check_20_drawings_2026-09-26.pdf` (+ per-part PDF / SLDDRW in `10_DRAWINGS/dimension_check_20260926/`).
All 106 values = design tables (independent check, `10_DRAWINGS/dimension_check_20260926_REVIEW.md`); cosmetic issues
listed there. How it was done + SolidWorks API traps: `00_DOCS/DRAWING_AUTOMATION_NOTES.md` (scripts in
`tools/_out/drawings_20260926/scripts`; `drw.py` now holds an untested v2).

**Other:** `07_RAW_EXTRACTS` OMi file stays the source; the user's `WebsitePartsInfo2026.xlsx` in the project root is their
Excel copy (differs only in "Side 3 Thread" of 507 metric/BSP parts - out of scope). pypdf + pymupdf installed.
SolidWorks was stuck at 13 GB at the end (a scratch test drawing "Draw88"): the user was told to answer No, close without
saving Draw88, and restart.

## 2. Open questions - ASKED on 2026-09-26, NOT ANSWERED YET (ask again if the user has not replied; recommendation in [])
Task A
1. Move the 18 staged masters `11_MASTERS_NEW` -> `11_MASTERS` and ship (macros from `after/`, SW2, RUN_ME batch14, QA_Log
   #159+, Topologies, coverage)? [yes]
2. The 10 held OMi bores (wider than the female port): keep current values / use OMi (7 configs drop out) / Brennan STEPs?
   [keep, report to OMi; 6405-32-24-O's Air-Way D3 2.38 is wrong too - needs a STEP]
3. Every OMi overall length of exactly 1.000 = placeholder? [yes]
4. 6410-12-08-O 1.09 -> 1.480 (= Brennan) OK? [yes]
Task B (changes / fills from `taskB/readings.txt`)
5. Two-leg elbows 2501/2502/2503/5502: M 1 = first-dash leg, L 1 = second (14 cells / 12 configs; fills 54) [accept]
6. 5500 same (weak, 3 rows) [accept]   7. Tees: M 1 / M 2 / L 1 = sides 1/2/3 [accept]
8. Swivel elbows 6500/6502 (= Brennan 10/10) [accept]   9. 6501/6503 by extension (fills 51) [accept]
10. Swivel straights 6402/6505/6506 (74 cells / 38 configs, +-0.18) [accept + spot-check STEP 6505-08-08]
11. 6565 (OMi body 0.12-0.55 shorter; 16 cells) [accept + STEP 6565-08-08]
12. 1404 OL = W (all 23 configs, -0.07..+0.14; replaces "nut face at Air-Way W") [accept]
13. 1404 Hex Flat = body hex (Brennan 1404 STEPs: one hex size = OMi) (15 cells +0.06..+0.13) [accept]
14. 6504 OL = L13; 0318 L1; 0403 L3; 6404 Side 1 ID = D1 through-bore (only 6404-06-08 0.50 -> 0.531) [accept]
15. Tables with no Air-Way row (0304, 0306, 2504, 2505, 2606, 2609, 2611, 5501, 6500L): OMi by family reading (fills 191) [accept]
Task C rules
16. OMi-first also for -FG parts whose only Air-Way row is non-forged (F1)? [yes where the master models the forged
    shape; wait for STEPs where a new forged shape is needed]
17. Brennan STEP as the only source where OMi and Air-Way are silent (ASSUMED) [yes]
18. Air-Way thread callout contradicting its own part number -> dash-correct thread [yes]
19. Copied values logged as assumptions (tap drill per size, swivel nut hex per size, bulkhead I1, -LN = plain, 5404-N
    lengths from the part number) [yes]
20. O-rings 4000/4001/4005 in scope? [no]   21. Bent-tube -Tube elbows [later, own masters]
22. Caliper readings (`00_DOCS/OMi_Caliper_SpotCheck.xlsx`) as a source [yes]
Leftovers
23. Snap 2-decimal hexes to the wrench fraction (~575 cells) [not now]
24. 2702/2703 -16: bulkhead hex arm 0.001 in short of the collar [yes]
25. 6801-05-05: build to Air-Way + Brennan 1.13 (MS says 1.090) [yes]
26. The 10 OMi differences on the hand-made 2404/6400 tables (2404-10-04 1.70->1.69, 2404-20-32 2.73->2.74, 6400 hexes
    08-04 / 10-06 / 10-08 / 24-16 / 24-20, bores 06-08 / 10-12, length 06-16) [apply when regenerating 2404/6400 for the
    2404-L / 6400-L fold]
27. 6408 small plugs cored or solid [solid until a Brennan STEP shows a bore]
28. OMi file as an existence source (79 DROP-row parts, 390 in no table) [no; the feed stays]
29. Report to OMi (24 wrong thread callouts, 1.000 placeholders, reducer bores wider than the port, 6801 findings,
    OMi file typos in rows 803 / 1154 / 120 / 2160) [yes - draft it]
30. Dry-run 5405's 3 unbuilt configurations into staging with the rest [yes]
31. 1404 bores: keep OMi (17 cells applied; OMi 0.01-0.05 below Brennan on 8/8 STEPs) or go back to Air-Way [Air-Way]
32. 6404-10-08 length: keep OMi 1.750 (Brennan 1.740, Air-Way 1.81) and note Brennan [keep OMi, note]
33. Air-Way tap drill conflicts -24 (1.70 vs 1.72) and -32 (2.19 vs 2.20) [wait for one Brennan STEP each]
34. Aliases 5406-P-02 = 5406-2P etc., 5404-N-08X2.500 = "5404-N-8-8 X 2 1/2" [yes]
35. Legacy HX masters 2500HX/2502HX/2603HX: hand-append rows or port to gen_tee [port later]
36. Brennan catalog pages instead of per-part STEP downloads (still one source) [yes if obtainable]

## 3. What to do once the user answers
- Q1 yes: ship Task A exactly like batch 13b (CLAUDE.md "Ship"): macros from `tools/_out/omi_apply_20260925/after/`,
  SW2 tables from there, staged parts `11_MASTERS_NEW` -> `11_MASTERS` (old ones -> `_to_delete/superseded_<date>/` AND a copy
  under `tools/_out/omi_apply_20260925/` because the user empties `_to_delete`), reports -> `03_SCRIPTS`, RUN_ME_batch14.txt,
  QA_Log (next # = last row + 1, was #159), Topologies notes, coverage refresh, PROJECT_STATUS. If Q31 = Air-Way: revert the
  17 1404 bore cells first (originals in `originals_before_apply/`), regenerate 1404, dry-run again.
- Accepted Task B readings: apply like Task A (new GS_OUT/GT_OUT folder, backups, checks, dry runs into staging, compare).
- Then Task C in the order of `taskC_merged.json` "cumulative_unlock_in_list_order" (answers unlock up to 120 rows); give the
  user the stage-1a STEP download list (98 part numbers, `step_list`).
- SolidWorks: restart before any build batch; builds of drawings leak ~0.5 GB each (restart every ~10), macro builds every ~40.
