# The 63 "one per family" Brennan STEPs (received 2026-10-21)
The user downloaded the 63 files of `tools/_out/partcommunity_20261021/STEP_MINIMUM.md` from Brennan's PARTcommunity portal (one
briefcase zip, guest download) and uploaded it to the cloud session. Extracted only the `.stp` files (the zip also holds one CADENAS
readme / terms of use per part: cadenas.de/terms-of-use-3d-cad-models) to `09_STEP_FILES/BRENNAN_<pn>.stp` (byte copies; `sha256.txt`).
Checks: 63 of 63 present, no extra, nothing on disk overwritten; each file starts ISO-10303-21 and names its part number in its PRODUCT
entry (`step_checklist.py` arrival check clean); each loads in OCP as 1 solid. Their records: `../partcommunity_20261021/pc_results_repo_steps.csv`.
