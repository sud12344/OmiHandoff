# Air-Way first: SolidWorks dry runs on the PC

Nothing here writes to `11_MASTERS` or `03_SCRIPTS`: every macro saves its part and report into `dryrun\<root>\`, and the shipped
masters are opened read-only and closed without saving.

1. SolidWorks 2026 signed in (start SOLIDWORKS Design from 3DEXPERIENCE). Close every master of the 25 roots and any open VBA editor.
2. In `OMi_Handoff` (PowerShell):
   ```
   python tools\_out\airway_first_20261020\scripts\run_dryrun.py g1 g2 g3
   ```
   - g1: 0318 0403 1404 2404 2501 2503 2605 2705 2706
   - g2: 5500 5502 6400 6401 6402 6404 6405 6408
   - g3: 6410 6500 6501 6502 6503 6504 6505 6506
   It stops before a group when SolidWorks uses > 8 GB or free virtual memory is < 6 GB. Then restart SolidWorks and run the
   remaining groups (e.g. `... run_dryrun.py g3`). If Excel crashes during a design-table insert ("Configurations after table: 1"),
   close the leftover Excel window and re-run that group.
3. Verdict:
   ```
   python tools\_out\airway_first_20261020\scripts\verdict.py tools\_out\airway_first_20261020\dryrun\out_g1.txt tools\_out\airway_first_20261020\dryrun\out_g2.txt tools\_out\airway_first_20261020\dryrun\out_g3.txt
   ```
   -> `checks\dryrun_verdict.txt`. PASS = macro ok, 0 FAIL lines, every configuration 1 body, the configuration set equals the staged
   SW2, and every configuration whose table cells did not change has the same volume / size as the shipped master. Configurations with
   reverted Air-Way cells are listed with their volume change (expected).
4. Commit `dryrun\out_*.txt`, the reports and `checks\dryrun_verdict.*` (the `.SLDPRT` files stay out of git), push, and ask for the
   batch-18 ship.

Regenerate the call files (only if the roots change): `python tools\_out\airway_first_20261020\scripts\make_calls.py`.
