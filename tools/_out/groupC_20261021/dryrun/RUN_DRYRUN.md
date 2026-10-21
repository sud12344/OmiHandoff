# Group C (compression): SolidWorks dry runs on the PC

Nothing here writes to `11_MASTERS`, `03_SCRIPTS` or `04_DESIGN_TABLES`: every macro reads its SW2 table from
`tools\_out\groupC_20261021\regen\new\...` (TABLE_PATH override) and saves its part + report into `dryrun\<root>\`
(SAVE_PATH / REPORT_PATH overrides). The cloud could not run SolidWorks - none of the 9 macros has been built yet.

1. SolidWorks 2026 SP4 signed in (start SOLIDWORKS Design from 3DEXPERIENCE). Close any open VBA editor.
2. In `OMi_Handoff` (PowerShell):
   ```
   python tools\_out\groupC_20261021\scripts\run_dryrun.py g1 g2
   ```
   - g1 (gen_straight2): C2402 (12 configurations), C2403 (18), C2405 (24), C0318 (9)
   - g2 (gen_tee, forged -FG): C2500 (10), C2501 (30), C2502 (20), C2601 (8), C6801 (20)
   Per root: `run_macro` (overrides above) -> `sweep_configs` -> `geometry` (reference configuration) -> two screenshots
   (isometric + top; front with a section through the axis) -> `close_doc` without saving. It stops before a group when SolidWorks
   uses > 8 GB or free virtual memory is < 6 GB (restart SolidWorks, run the rest). Excel crash during the design-table insert
   ("Configurations after table: 1"): close the leftover Excel window and re-run that group.
   By hand instead: `python sw_mcp\call.py @tools\_out\groupC_20261021\dryrun\calls_g1.json` (same calls).
3. Look at (`dryrun\out_g1.txt` / `out_g2.txt`):
   - report: 0 FAIL lines, "Master left in its reference configuration", the checks "End A/B tube socket bottom open to the bore",
     "construction core removed" (C0318), "bore open on the axis at End A / End B";
   - sweep: every configuration rebuilds, 1 solid body;
   - geometry (reference -08): socket cylinder 0.514 dia x 0.305 deep at each bite tip, thread major 0.750 to 0.423 from the tip, 45 deg
     cone (ramp), neck 0.660 to the hex face at 0.562; C0318-08: countersink 0.755, minor 0.6823 to 0.599, 45 deg cone, hole 0.505,
     L 0.840. The OCP closed loop (`closed_loop\closed_loop.txt`) already checked every configuration's outline against these values;
     the dry run checks what only SolidWorks can: the features (pocket / bore / Thread-feature / helix on the nut) and the design table.
   - threads: `set_suppression` THD_* off on the reference and one extreme size (-04, -32), rebuild, 1 body, threads cut material,
     then put them back (masters are saved with THD_* suppressed).
4. Commit `dryrun\out_*.txt` and the reports (`.SLDPRT` stay out of git), push to `claude/groupC-compression-20261021`.

Regenerate the call files (only if the roots change): `python tools\_out\groupC_20261021\scripts\make_calls.py`.
