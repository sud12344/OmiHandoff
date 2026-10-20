# BATCH 17 SHIPPED 2026-10-20 ~01:30 - this file is now the run log (03_SCRIPTS/RUN_ME_batch17.txt, QA #173-#175, PROJECT_STATUS s1).
74 roots shipped by scripts/ship_b17.py go (checks/shipped_files_sha256.txt, old_files/MANIFEST.txt); post-ship verify 0 BAD
(checks/verify_b17.txt); workbook QA_Log + Topologies (paperwork/update_masterdata_17.py, masterdata_check.txt); counts paperwork/count_now.txt;
coverage paperwork/coverage_run.txt. Held: 4503 4603 1703 1700RC 1800 5404N (QA #175).

# Batch 17 ship - progress note (2026-10-19; updated 23:15 - the laptop stayed on, groups 5-7 running through scripts/run_groups.py)

Nothing is shipped. `11_MASTERS`, `03_SCRIPTS`, `04_DESIGN_TABLES`, live `tools/` are untouched. Everything is in this folder.

## Done
- **Rebased on live:** stage review tables = live `04_DESIGN_TABLES` + logged batch-17 edits, 0 stale cells (`checks/cmp3_full.txt`,
  `scripts/cmp3.py`; the only live-vs-fork-base differences are the 269 OMi-answer cells). `root/04_DESIGN_TABLES` = live + the stage's 135
  review tables.
- **adapters77:** already folded into the stage (wave 3, `brennan_yes_20261018/scripts/apply_adapters.py`); `apply_77.py` NOT run - never run it.
- **Regenerated** (`scripts/regen_b17.py`): control (live tools, live tables) reproduces the shipped files (known pre-2026-09-25 macro
  roots aside); `regen/b17` = merged tools on `root/`. 80 roots change (`checks/b17_roots.json`, `checks/detail_cmp.txt`); 98 old
  configurations change, all on rows with a logged edit (A19 / A20 / A21 / A23).
- **Static checks** clean on the 80 roots (`checks/allcfg.txt`, `dofcheck_*.txt`, `vbacheck.txt`, `regress.txt`).
- **Generator fix:** the 6 angled macros (1503 1504 5501 5503 5505 6902) did not compile: `Atan2V(y As Double, x As Double)` got Variant
  array elements ByRef. `tools_b17` = merged tools + `ByVal` on that line (only diff). `regen/b17v2` (`scripts/regen_b17v2.py`) = b17 except
  1 line in those 6 macros; all SW2 identical. **b17v2 is the ship source.**
- SolidWorks crashed once (21:28, my bisect loading ~40 test macros) - harmless; `bisect/` = the test modules.

## Dry runs (`sw_dryrun/<root>/`, logs `out_g*.txt`, verdict `python -I scripts/verdict.py out_g1.txt ... out_g7.txt` -> `checks/verdict.txt`)
- Finished (34): 0318 0403 1404 1405 1503 1504 1601 1602 1603 1700RC 1703 1704 1724 1800 1804 1824 2403 2405 2406 2700 2705 2706
  4501 4503 4601 4603 5404N 5501 5503 5505 6400 6606 6807 6902 - all PASS except the HOLD list (old configurations either identical to
  the live master or changed with their table cells; check 2403-2706 in the verdict, they finished last).
- **HOLD** (in `scripts/ship_b17.py`): 4503 4603 (hose face-off on the hose leg), 1703 (HEX2 direction), 1700RC 1800 (FLATS sketch not
  fully defined), 5404N (-06 threads, QA #163).
- Group 4 complete 23:00 (5000 5404 5405 + 2403-2706 PASS, old configurations identical). **Still to run:** groups 5-7 (run_groups_log.txt says which started). Old text: rest of group 4 = 5000 5404 5405 (check `out_g4.txt`: a root without "Saved to" in its report must be re-run), then
  groups 5-7: `python -I scripts/run_groups.py g5 g6 g7` waits for out_g4 to be complete - if g4 was cut off, make a new call file for the
  missing roots instead: `python -I -B scripts/make_calls.py g4b 5000 5404 5405` then `python -u sw_mcp/call.py @.../calls_g4b.json`.
  Each call file: run_macro (scratch SAVE/REPORT/TABLE paths) -> sweep_configs -> close; if the root has a live master, open it read-only ->
  sweep_configs -> close (old-configuration comparison).
- SolidWorks: restart every ~40 builds (the user restarts it from 3DEXPERIENCE; never start SLDWORKS.exe).

## 23:16 - 23:45 incidents (2026-10-19)
- 23:16:42 SolidWorks went down right after building 6401 (Windows logged ViewServerV6.exe, no sldworks crash record); a new SolidWorks
  started 23:16:46. The rest of group 5 and all of group 6 ran against no SolidWorks -> logs in `_failed_runs/`.
- 23:22 EXCEL.EXE crashed while SolidWorks inserted 5601's design table; its window ("DesignTable_5601_SW2 - Excel") stayed open and every
  later design-table insert failed (5652 6500 6501 6502: 1 configuration). Stopped the runners, closed my 6503 scratch part and that Excel
  instance, closed a 6401_MASTER SolidWorks had reopened from the 3DEXPERIENCE cache (unmodified); 5601 re-run alone = 0 problems.
  Bad dry runs moved to `_failed_runs/excel_crash_2322/`.
- `run_groups.py` now stops after a group whose log shows SolidWorks down (AFTER=<log> picks the log to wait for).
- Re-running: `AFTER=out_t5601.txt run_groups.py g5b g6 g7b` -> run_groups_log3.txt (g5b = 6401..2404, g7b = all of group 7 except 5601).
- Verdict logs to pass, in order: out_g1 out_g2 out_g3 out_g4 out_g5 (5406 .. 5406SHP valid) out_g5b out_g6 out_t5601 out_g7b.
- 5406HHP / 5406SHP "Body diameter" FAIL = loose GetPartBox around the live helix (exact sweep size = table): ACCEPTED in verdict.py.

## Then
1. `python -I scripts/verdict.py out_g1.txt out_g2.txt out_g3.txt out_g4.txt [out_g4b.txt] out_g5.txt out_g6.txt out_g7.txt` - every
   non-HOLD root PASS; read every "DIFFERS" line.
2. `python -I scripts/ship_b17.py` (plan) then `... go`.
3. Paperwork as batch 16 (`tools/_out/ship_20261019/paperwork`, `RUN_ME_batch16.txt` format): RUN_ME_batch17.txt, QA_Log (next # = last + 1),
   Topologies notes, post-ship verify (live tools + live tables regenerate the shipped files), coverage refresh, PROJECT_STATUS, CLAUDE.md.
   Note in RUN_ME: 6902-12-12-NWO-FG (composed shape) and 5505-20-20-FG (on the -08 shape) ship with their assumption in AxialSource -
   still open user calls; the stale "BUILD-NEAR / MISSING" $COMMENT texts on built rows were not re-worded.
