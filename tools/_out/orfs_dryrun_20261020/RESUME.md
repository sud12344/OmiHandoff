# ORFS SolidWorks dry runs (PC, 2026-10-20) - run log

Staged ORFS macros: `tools/_out/orfs_gen_20261020/out/` (+ `tee/`, `ring/`). These dry runs write only here (SAVE / REPORT overrides); `11_MASTERS`
is untouched. Nothing is shipped.

## Tools in this folder
- `make_calls.py <group> <roots>` -> `calls_<group>.json`. Each root gets:
  - run_macro (dry run);
  - sweep_configs;
  - a thread check: every configuration must give 1 body with THD_* off and on, each THD_ live without error and removing material;
  - a section screenshot;
  - close (discard).
- Run a group: `python sw_mcp/call.py @tools/_out/orfs_dryrun_20261020/calls_<group>.json > .../out_<group>.txt`.
- `verdict.py` -> `VERDICT.txt`: one PASS / CHECK line per root.
- `regen_fs.py`: regenerate the FS roots with the staging tools and diff against a backup (`REGEN_BEFORE` / `REGEN_AFTER`).
- The `thdcheck` in run_python must re-read the features after every configuration switch. Feature handles taken in another
  configuration silently ignore SetSuppression2, which made a false "thread cuts nothing" report on FS6400.

## Results
- FS2403, FS6400: PASS. Done by hand through the MCP; reports in `FS2403/`, `FS6400/`.
- Group 1 (FS2500, FS2500N, FS6500C, FS6801R): PASS after the two fixes below.
  - FS6500C now passes when built at -20. Its first run (built at -10) is in `FS6500C/run1_built_at_10/`.
  - The fixed-macro test run is in `exp_ref/`; its macro is identical to the staged one.
- Groups 2-4 (`out_g2` ... `out_g4`), the reruns of the 13 no-step masters (`out_g5`) and of the 4 -10 swivel masters (`out_g6`).
- **FINAL: all 51 PASS.** `VERDICT.txt` = 49 from the logs (the latest run of each root counts) + FS2403 / FS6400.
- FS6500, FS6502, FS6600 and FS6602 ran with tables that still had the dead FSW_CSANG column; the staged tables only lack that column.
- `contact_sheet.png`: section views of 12 of the new types.

## Generator fixes (staging toolset `orfs_gen_20261020/tools`; originals in `backup_20261020/`)
1. **`gen_straight2.py` FSSW_MEAS[10] TE 0.484 -> 0.4993.**
   - The STEP's TE sits on Brennan's undersized -10 minor (dia 0.892). The model keeps the ASME basic minor (0.9227).
   - With the measured relief point (RELS 0.548, RELR 0.51), that made a 37.2deg relief, so FSW_RELANG (45) could not be placed.
   - Every other size's TE = RELS - (RELR - rmin), i.e. a 45deg relief that meets the basic minor. -10 now follows the same rule.
   - Changed: FS6500C, FS6600C, FS6602C, FS6504C. 2 cells each (FSW_THDL, HELIX HEIGHT) + the matching macro lines; all other FS roots
     identical (`regen_fs_diff.txt`). Checks: `static_checks_te10.txt`.
2. **`gen_tee.py` write_sw2: reference row of FS masters.**
   - Problem: if the reference row has a face-seal male leg whose thread is BELOW the flats, and another row has that leg PROUD of them,
     the Thread feature loses its edge in the proud row. FS6500C built at -10 gave the THD_End1 error on -20.
   - Building at a proud row works the other way round (FS2500: -08 -> -06 / -10; FS6500C: -20 -> -10).
   - Rule: such a master is built at its first row with no leg below the flats.
   - Changed: FS2501 (ref -> 08-06), FS2503 (-> 08-06), FS6500C (-> 20-20), FS6602C (-> 20-20-20). All other FS roots are identical
     (`regen_fs_diff_ref.txt`). Checks: `static_checks_ref.txt`.
3. **No `FSW*_CSANG` table column** (`gen_tee.py` leg_FSSW, `gen_straight2.py` FSSW end).
   - The macro can only hold the swivel countersink angle by its supplement (named `<nm>_SUPPL`), so the column was dead.
   - On every insert of such a table, SolidWorks stopped with a modal "parameters not found" task dialog that waited for OK. That is the
     user's "it keeps stopping", and the reason for the 2 - 7 minute builds.
   - The angle is constant per master (45, C masters 60) and stays in the sketch, as the JIC swivel's SW_CSANG (no column there either).
   - Changed: the SW2 tables of the 21 swivel roots, which lose only that column (checked column by column); 0 macro lines changed
     (`regen_fs_diff_csang.txt`). All 50 staged tables were refreshed from `regen_after_csang/` (29 of them identical).
4. **No-step face-seal threads anchored at the nose** (`gen_tee.py`: leg_FSM nostep thread `nose=True` + the ThreadCut / ThreadCutV
   emit).
   - Problem: in a no-step leg (flats = thread major within FSM_NOSTEP_TOL) the anchor circle at the hex end is split into 6 arcs by the
     flats.
   - With face-seal legs on both run ends of a tee, SolidWorks refused the Thread feature there in both directions. This hit FS2601N,
     FS2603N and FS6600N. Reproduced through the API on FS2601N.
   - The fix: anchor at the nose circle (thread major meets the 45deg chamfer = ex + depth, always a whole circle) and run back towards
     the hex. Same length.
   - Changed: the 13 no-step masters, only their ThreadCut lines; 0 table cells (`regen_fs_diff_nose.txt`). All 13 re-run: PASS
     (`out_g5.txt`). The threads cut on every leg; the fixed ones went from partial to full.
   - FS2501N's Z-extent FAIL is gone too: the thread at the old hex-end anchor had left a sliver.
5. **-10 swivel helix = the STEP's measured thread end** (`FSSW_MEAS[10]` HTE 0.484; leg_FSSW / end_FSSW use `m.get('HTE', m['TE'])`
   for the helix only).
   - Problem: with the helix running to TE 0.4993, the tooth touches the relief cone. The swept cut failed in FS6602C -10 (swivel on -X,
     built at -20); it builds at <= 0.49.
   - The cavity keeps TE.
   - Changed: FS6500C, FS6600C, FS6602C, FS6504C. One cell each (HEIGHT@HELIX), plus the helix call where -10 is the reference row
     (`regen_fs_diff_hte.txt`).
- The staged `out/` files of the changed roots were replaced; the previous copies are in `backup_20261020/out_before*`.

## Dialog watcher
- `dialog_watch.ps1` runs during the batches. It answers OK ONLY on that design-table warning: a #32770 dialog with a single OK button, text
  listing name@feature parameters, and a "Copy all to Clipboard" link.
- It logs every dialog to `dialogs_log.txt`. Anything else is logged as SEEN and left alone.
- Stop it by creating `dialog_watch.stop` in this folder.
- A failed thread feature still produces the same warning: its THD_ columns are dead. So the watcher stays on until the thread failures
  below are fixed.

## Open after the runs
- **FS2601N, FS2603N, FS6600N:** THD_End1 / THD_End2 (SolidWorks Thread feature on the two run legs) refused:
  - CreateFeature -> False on the -04 reference row. The anchor edge at x 0.464 / r 0.28125 is found.
  - Common factor: a "no step" tee with face-seal legs on BOTH run ends, under one run hex (HEXAF@RUN 0.56 / 0.562 vs thread 0.5625).
  - Not affected: FS6602N (one face-seal run leg), FS2500N / FS2501N (elbows). The branch leg (helix sweep) works.
- **FS2501N:** Z extent -0.2826 .. 0.2813 vs expected +-0.2812, on one side only. So it is not the revolve; suspect the hex cut or the
  corner puck. Look in SolidWorks.
- The live `tools/` is NOT changed. Both fixes go in with the ORFS merge (back up, regenerate all roots old / new, diff).

## Noticed, not fixed
- The swivel nut's helix curve (HELIX_n) is visible in the saved FS6500C master (blue rings). Display only.
- FS6500C built at -20 took 445 s in SolidWorks (vs ~40 s for the others).
