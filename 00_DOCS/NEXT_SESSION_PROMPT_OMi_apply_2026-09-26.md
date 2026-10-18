You are continuing work on the OMi carbon-steel fitting CAD library in `C:\Users\sudha\OneDrive\Desktop\OMi_Handoff`.
Read first, in this order: `CLAUDE.md`, `00_DOCS/PROJECT_STATUS.md` (sections 1, 3, 5 were updated on 2026-09-25 evening),
this file, then `00_DOCS/OMi_Dimension_Audit_2026-09-25.md`. Load the `omi-fitting-library` skill for table / master work.
CLAUDE.md "Rules that don't bend" apply throughout, except where the user decisions below change the source order.

## What happened on 2026-09-25 (evening session) - all done and recorded
1. **OMi dimension audit** finished: `00_DOCS/OMi_Dimension_Audit_2026-09-25.xlsx` / `.md` (scripts + intermediates in
   `tools/_out/omi_audit/`, independently re-checked, 0 refuted). QA #157.
2. **Overnight build ACCEPTED** by the user: the 38 parts moved `11_MASTERS_NEW` -> `11_MASTERS` (now 60 masters), reports ->
   `03_SCRIPTS`; replaced 0318/0403/6405/6408 + the 0318 duplicate saves -> `_to_delete/superseded_20260925/` (sha256
   manifests). QA #154/#155. A stale 0318 VBA module is still loaded in the SolidWorks VBA editor (it ran at 20:08) - tell the
   user to remove it before any manual run.
3. **Batch 13b + regenerated 6404/6504/6565 SHIPPED** (`03_SCRIPTS/RUN_ME_batch13b.txt`, QA #156): macros 6404 6504 6565 2501
   6801 6802 6803 6804 in `03_SCRIPTS` (LF), SW2 2501 (32 rows) + 6801-6804 in `04_DESIGN_TABLES`, old files in
   `_to_delete/superseded_20260925/reshipped_regen_20260925/`. Checks clean; SolidWorks dry runs identical (volume + size of
   every configuration) to the accepted parts (`tools/_out/ship_20260925_dryrun/`, compare script `cmp_sweeps.py` there).
   MasterData: QA_Log #153-#158 appended, Topologies notes for the accepted roots (backup in
   `_to_delete/superseded_20260925/masterdata_before_qa153/`). Coverage refreshed (A1 built = 854 OMi parts).
4. Coverage now: of 1,804 BUILD configurations, 976 are in a master (853 in `11_MASTERS` current), 101 have data but no
   master configuration, **727 are DataStatus MISSING**.

## User decisions (2026-09-25 evening, in chat - recorded in PROJECT_STATUS s5 and QA #158)
- **OMi's dimension file ranks ABOVE Air-Way for dimensions**: "OMi is only in charge of dimensions, for geometry use
  Brennan". Air-Way fills what OMi does not give; Brennan sets end shapes / forged bodies / seats / nuts / ports.
- **Rounding-only differences are fine** (no change): OMi half-up to Air-Way's printed decimals = table; the table's exact
  fraction rounded or cut to OMi's 3 decimals; the 15 real differences that equal the table when OMi is cut to Air-Way's
  decimals (treated as rounding - the user may object).
- **"Just build it using OMi's excel file for now; keep it ASSUMED; I'll ask OMi later"** (whether OMi's data is independent
  of Brennan is unknown - the user will ask OMi). So every row that takes an OMi value is DataStatus ASSUMED.
- Earlier decisions this reverses (applied under the new rule, flag them in the report): 6410-12-08-O length Air-Way 1.09 ->
  OMi 1.480 (= Brennan); 1404/1405 nut face at Air-Way W (only if the 1404 Overall Length -> W mapping is accepted).
- Standing: F1 (-FG rows with only non-forged Air-Way rows) = wait for Brennan -FG STEPs. Whether OMi-first also covers F1
  is NOT decided - evidence is mixed (OMi -FG legs equal the non-forged Air-Way value in 88 of 171 cells; hexes differ in
  61 of 94). Ask before using OMi on F1 rows.

## Checks finished at the end of the session (results saved in `tools/_out/omi_audit/saved_workflow_results/`)
- **Ship audit** (`ship_verify_journal.jsonl`): all 86 acceptance moves, the 8 shipped macros, 5 SW2 tables, QA rows,
  Topologies notes and coverage PASS. The paperwork issues it found were fixed the same night (stale "not shipped" text in
  PROJECT_STATUS / CLAUDE.md; QA #156 said 116 configurations - it is 121; RUN_ME "byte-for-byte" -> "apart from line
  endings"; the 6504/6565 dry-run comparisons and the static-check outputs are now stored in
  `tools/_out/ship_20260925_dryrun/` and `tools/_out/ship_20260925_checks/`). Still open from it: coverage counts the 4
  un-rebuilt 5405/6401 configurations as built (tool limitation); RUN_ME_batch13a.txt points to a non-existent
  `_to_delete/superseded_20260925/pre_b13`; Topologies 5502/5504 still say "MACRO READY - re-run" although their masters exist
  (built 2026-09-24, before the batch-11e macros).
- **Leg-column verification** (`legmap_verify_journal.jsonl`; the recount reproduced `legmap.json` with 0 differences):
  two-leg elbows 2501/2502/2503/5502 SUPPORTED (M 1 = Side-1 leg, L 1 = Side-2 leg; the swapped reading fits 0 rows; the
  exceptions are Air-Way anomalies); 5500 supported but weak (3 reducer rows); tees: the odd leg is SUPPORTED by side
  (L 1 = branch on 2601/2602/2603, M 2 = the Side-2 pipe leg on 2605) - M 1 vs M 2 cannot be tested (always equal legs, so it
  does not matter); swivel elbows 6500/6502 SUPPORTED (M 1 = nose tip, M 2 = nut face, L 1 = the other leg; also equal to the
  Brennan STEPs on 10/10); 6501/6503 undecidable (1 row each, consistent with 6500, 0.03 high); straights: Overall Length =
  the overall letter holds; swivel straights 6402/6505/6506 SUPPORTED as "same features, different body length"; **6565 is the
  same features too** (datum hypothesis REJECTED: OMi OL - L 1 = Air-Way L31 - L32 at all 9 sizes; OMi's body is 0.12-0.89
  shorter); 1404 Overall Length = W-like (= the Brennan overall length on 7 of 8 STEPs). `legmap.json`'s "best" field is a
  tie artifact where every column scores 0 (1404, 6402 L1, 6565 L1, 6501/6503) - use the critic's nearest column.
- **OMi vs Brennan (the user's independence question)**: the leg-column critic measured 49 Brennan STEP bounding boxes: OMi
  Overall Length = the Brennan length on 20 of 22 straights, = Air-Way on only 5 (exactly where Brennan = Air-Way); 6500 OMi
  L 1 / M 2 = Brennan on 10/10. OMi's numbers are very likely Brennan's data (or OMi sells Brennan parts) - consistent with
  keeping OMi-sourced rows ASSUMED. A dedicated tally, run `wf_8892ea30-fa7`, was still running at the end; its journal is
  `C:\Users\sudha\.claude\projects\C--Users-sudha-OneDrive-Desktop-OMi-Handoff\51887e3d-9cd2-4265-8f91-c4047ab7998c\subagents\workflows\wf_8892ea30-fa7\journal.jsonl`
  - read it if it has a result, otherwise skip it (the evidence above is enough for now).

## Next task A - apply OMi values where the column mapping is CERTAIN (the user said "just build it")
Change list ready: `tools/_out/omi_audit/omi_apply/phaseA_changes.json` - 184 cells on BUILD rows of 18 generator series
(6405 38, 6410 30, 2706 29, 1404 18 bores, 6401 18, 6404 14, 2705 13, 6505 5, 2501 3, 5502 3, 6402 3, 0403 2, 6504 2,
6565 2, 2503 1, 5500 1, 6408 1, 6500 1), each with the review cell, old value and OMi value; plus the 51 skipped cells with the
reason (rounding-type 15, 6410 `1.000` placeholders 5, DROP rows 21, hand-made tables 10: 2404 2 + 6400 8 - list those for the
user, do not edit hand-made tables without asking).
Procedure (CLAUDE.md): back up every review table you touch to `_to_delete/superseded_<date>/omi_apply/`; write the OMi value
into the review cell; append to `$PRP@AxialSource` the source ("<col>: OMi WebsitePartsInfo2026.xlsx <cell> (was Air-Way <v>),
user 2026-09-25 OMi dims > Air-Way") and set `$PRP@DataStatus` ASSUMED; regenerate the 18 roots into a NEW folder
(`GS_OUT` / `GT_OUT` = e.g. `tools/_out/omi_apply_<date>`; never into tools/_out/tee, overnight or regen_20260925); run
dofcheck / allcfg / vbacheck / regress (regress must show ONLY the intended cells changed); watch the generator summaries for
newly BLOCKED or newly UNBLOCKED rows (6405-24-16-O was blocked by Air-Way L 1.00; OMi gives 1.750); SolidWorks dry runs
with SAVE_PATH / REPORT_PATH -> `11_MASTERS_NEW\` (staging, like the overnight build - the user's rule is not to overwrite
`11_MASTERS` directly), compare every configuration with the current master (unchanged configurations must be identical;
changed ones differ only where expected), screenshots of changed configurations; then report and let the user accept, and ship
macros + SW2 + RUN_ME + QA_Log + Topologies + coverage as tonight. SolidWorks: restart every ~40 builds; before restarting
check for open documents / VBA editor windows and ask.

## Next task B - the uncertain column mappings (verification DONE, see above: show the user, apply what they accept)
Cross-series test (`tools/_out/omi_audit/s13_legmap.py` -> `legmap.json`), awaiting the critic:
- two-leg elbows 2501/2502/2503/5500/5502: OMi M 1 = Side-1 leg, L 1 = Side-2 leg (2501 32/33 + 32/33, 0 fit the swapped
  reading; 2502 10/10; 2503 25/29; 5502 14/17; 5500 11/13 incl. the flagged swapped 5500-16-12-FG);
- tees 2601/2602/2603/2605: M 1 / M 2 / L 1 = legs of Sides 1 / 2 / 3;
- swivel elbows 6500/6502: M 1 = swivel leg to the nose tip (M10/M14), M 2 = to the nut face (M5/M6), L 1 = the other leg;
  6501/6503 have one comparable row each (L 1 fits; M 1/M 2 0.03 high);
- straights: Overall Length = the overall letter (0319, 6408, 6400L, 0403); swivel straights 6402/6505/6506: OMi OAL and
  L 1 differ from Air-Way by the SAME amount per row (varying, not per swivel size) -> same features, different body length;
  6565: same features as Air-Way (the different-datum idea was rejected by the check above); OMi's body is 0.12-0.89 shorter; 1404 OMi
  Overall Length tracks W (not L).
Show the user the verified evidence; the user decides (their earlier rule: value agreement alone does not prove a mapping -
they asked for this cross-series test to settle it). Then apply like task A.

## Next task C - the 727 MISSING configurations
Plan (5 group plans + 5 adversarial critiques, all done): `tools/_out/omi_audit/saved_workflow_results/plan727_summary.txt`
(readable) and `plan727_results.json` (full). Apply every critic correction. Headlines: D-codes 29 (26 fillable from data already
in the repo - 6900 blocker note is stale; 6400 -14/-32 groove data measured), F4/F5 19 (mostly fixable now; some are user
decisions), F3 138 (no Air-Way page: O-ring tables for 4000/4001/4005 from published tables; the rest need a Brennan STEP per
part + new modules: code 62 flanges, bent-tube elbows, flareless nut/sleeve), F1 260 (forged; wait for Brennan -FG STEPs unless
the user extends OMi-first to them; many need new generator modules), F2 281 (see the F2 plan). Re-bucket every row under the
new rules (OMi dimensions first, Brennan geometry, ASSUMED) and give the user: how many become buildable now, what each of the
rest needs (exact Brennan STEP part numbers), and the questions.

## Open questions for the user (collect, ask once)
- Is OMi's data independent of Brennan? (user will ask OMi; until then ASSUMED)
- Accept the leg-column readings (task B), the swivel-straight readings (incl. 6565) and 1404 Overall Length = W?
- Does OMi-first cover the -FG (F1) rows?
- 6408 small plugs: cored (OMi gives a bore) or solid (as built)?
- The 2404 / 6400 changes (hand-made masters, files not in the repo).
- The remaining audit questions (00_DOCS/OMi_Dimension_Audit_2026-09-25.md section 4) not answered above: hex A/F snap
  (rounding is fine -> presumably no snap; confirm), scope of the 79 OMi-file parts on DROP rows, majority-vote conflicts,
  2702/2703 -16 offset, 5405/6401 re-run for 4 configurations.
