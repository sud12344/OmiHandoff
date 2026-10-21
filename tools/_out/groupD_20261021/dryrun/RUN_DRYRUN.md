# Group D bent tubes: SolidWorks dry runs on the PC

Nothing here writes to `11_MASTERS`, `03_SCRIPTS` or `04_DESIGN_TABLES`. Each macro saves its part and report into `dryrun\<root>\`,
and reads its SW2 table from `regen\stage\`. 3 masters, 66 configurations: 1704T 35, 1703T 26, 6701 5.

1. Get SolidWorks ready:
   - SolidWorks 2026 SP4 signed in: start SOLIDWORKS Design from 3DEXPERIENCE (never start SLDWORKS.exe directly).
   - No part called `1704T_MASTER`, `1703T_MASTER` or `6701_MASTER` open.
   - No VBA editor window open.
2. In `OMi_Handoff` (PowerShell):
   ```
   python sw_mcp\call.py @tools\_out\groupD_20261021\dryrun\calls_bent.json > tools\_out\groupD_20261021\dryrun\out_bent.txt
   ```
   The call file does this for each root:
   - `run_macro` with these overrides:
     - `TABLE_PATH` = `tools\_out\groupD_20261021\regen\stage\DesignTable_<root>_SW2.xlsx`
     - `SAVE_PATH` = `dryrun\<root>\<root>_MASTER.SLDPRT`
     - `REPORT_PATH` = `dryrun\<root>\Build_<root>_report.txt`
   - `sweep_configs` with the key dims.
   - `geometry` on the smallest and the largest configuration.
   - `close_doc` with `discard_unsaved`.

   Each macro runs its own checks:
   - sketches fully defined;
   - one box check per configuration;
   - the all-configuration rebuild sweep;
   - a thread check: every configuration with its `THD_` features on.

   If Excel crashes during the design-table insert ("Configurations after table: 1"), close the leftover Excel window and run again.
3. Verdict:
   ```
   python tools\_out\groupD_20261021\scripts\verdict.py tools\_out\groupD_20261021\dryrun\out_bent.txt
   ```
   It writes `checks\dryrun_verdict.txt`. A master PASSES when all of these hold:
   - the macro ran OK, with 0 FAIL lines in its report;
   - every configuration rebuilds to 1 body;
   - the configuration set equals the SW2 table;
   - each configuration's volume and box size match the OCP rebuild of the same numbers (`dryrun\expected_ocp.json`, from
     `closedloop\allcfg_bent_ocp.py`) within 0.3 % and 0.005 in.
4. Look at it (CLAUDE.md verify loop, step 5): take a `screenshot` of `1704-12-12-Tube`, `1703-12-12-Tube`, `1803-32-32-Tube`,
   `1704-20-12-Tube` (tube wider than the hub), `6701-04-04` (own neck) and `6701-08-08`, with views `front` / `isometric` and `section_plane` "Front Plane". Check:
   - the bend;
   - the hub behind the flange head;
   - the O-ring groove;
   - the bore running through.
5. Commit and push these files:
   - `dryrun\out_bent.txt`;
   - the three reports;
   - `checks\dryrun_verdict.txt`.

   The `.SLDPRT` files stay out of git.

**What is new and not yet run in SolidWorks:**
- The hub heads: a 10-line HEADSK, plus PATH's construction line `FACEEXT`, `PathExtension`, and `Dim pe`.
- The code 62 heads -12 ... -32.

The checks that cover them:
- In the cloud, `checks\dofcheck_bent.txt` says these sketches are fully defined with 0 redundant constraints.
- In SolidWorks, the macro checks "HEADSK sketch fully defined", "PATH sketch fully defined" and `dim FACEEXT = ...`. `NameDim` compares
  the measured value, so a dimension of the wrong type fails here.

**Unchanged since the clean 2026-10-15 dry runs:** the end piece, the tube sweep, the bore and the 6701 swivel / nut thread.
