# Running this project in a Claude Code cloud session (2026-10-18)

The cloud runs on a Linux machine. It can do the **Python side**:
- filling and checking review tables;
- generators, regeneration and regression;
- static checks and OCP closed loops;
- STEP measuring.

It **cannot** run SolidWorks: no macros, no dry runs, no shipping. Those stay on the Windows PC. The `solidworks` server in `.mcp.json`
points at Windows paths and will simply not start in the cloud.

## What is in the repo (see `.gitignore`)
- **Main folders:** `tools/` (live toolchain), `04_DESIGN_TABLES/` (live tables), `00_DOCS/`, `01_MASTER_DATA/`, `03_SCRIPTS/` (shipped
  macros), `07_RAW_EXTRACTS/` (OMi file, Air-Way passes, Brennan TFA / ORFS / Flange catalogs), `09_STEP_FILES/` (Brennan STEPs).
- **Current work (2026-10-18):**
  - `tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES` = batch 16 + OMi answers + Brennan rows + A19-A23 + adapters + the
    generator-feature rows. This is the table set for batch 17.
  - `tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES` = the ORFS tables (not part of a generator yet).
  - `tools/_out/genfeat_20261018/merged/tools` = the merged toolset for batch 17.
  - `tools/_out/puckfix_20261009/tools_new` = the batch-16 toolset (control).
- **Not included:** SolidWorks masters (`11_MASTERS*`), old staging copies, `_to_delete`, `_archive`, drawing PDFs.

## Environment setup script (cloud environment settings)
```
pip install openpyxl numpy cadquery-ocp
```
cadquery-ocp is large. If the setup script does not finish in about 5 minutes it is not cached; then install it in the session when an
OCP step needs it. Untested in the cloud so far.

## Running the generators (portable: paths come from tools/omi_paths.py + environment variables)
```
export OMI_ROOT=$PWD/tools/_out/brennan_yes_20261018/stage      # the table set to read (must contain 04_DESIGN_TABLES)
export GS_OUT=/tmp/gen/straight GT_OUT=/tmp/gen/tee
python -I tools/_out/genfeat_20261018/merged/tools/generators/gen_straight2.py 6400
python -I tools/_out/genfeat_20261018/merged/tools/generators/gen_tee.py 4601
```
`OMI_DEV` (default: the Windows path) is only the text written into the macros. Keep the default, so the macros still work on the PC.

## Known limits
- Many one-off staging scripts under `tools/_out/brennan_yes_20261018/scripts/` and the wave folders have the Windows project path
  hard-coded (`C:\Users\sudha\...`). In the cloud, adapt `ROOT` at the top of a script before running it.
- Generated macros, reports and table copies written in the cloud must be committed and pulled back to the PC before they can be dry-run
  in SolidWorks.
- The project folder lives in OneDrive. OneDrive syncing the `.git` folder can conflict while git is writing. If that happens, pause
  OneDrive sync during git operations.
