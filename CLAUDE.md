# OMi fitting library - read at the start of every session

Carbon-steel hydraulic fitting CAD library for OM Industrial: 2,535 parts -> 126 parametric
masters driven by design tables. Background: `README_START_HERE.md` (background and conventions only - its
status, open items, build order and next actions are from August and stale), `OMi_SOP_NewSeries.md`, and the
`omi-fitting-library` skill (`.claude/skills/omi-fitting-library`; load it for any topology / design table / drawing /
spec-sheet work).

**Current state, open work, user decisions: `00_DOCS/PROJECT_STATUS.md` - read it before starting
anything, update it when a batch ships or the user decides something.**
**2026-10-21: BATCH 20 SHIPPED** (`03_SCRIPTS/RUN_ME_batch20.txt`, QA #182): 5404N -06 thread fix + 4 long nipples -> 1,632 configurations,
1,629 of 2,535 OMi parts. Only 2502 is still parked (QA #180); user questions QA #181.
**2026-10-21: BATCH 19 SHIPPED** (`03_SCRIPTS/RUN_ME_batch19.txt`, QA #179-#181, `tools/_out/batch19_20261021/merge/`): the no-input
parts (answered rows, own-STEP rows, Brennan cells, new masters 0319 2500 2603 2613 3474 6603 FS2500N1; 2500HX / 2603HX retired) -> 1,610
configurations in a master, 156 masters; 1,607 of 2,535 OMi parts. Live `tools/` = `merge/tools_b19`. 2502 parked (QA #180). Rows needing the
user: QA #181 / PROJECT_STATUS s1.
**2026-10-20 (night): BATCH 18 SHIPPED** (`03_SCRIPTS/RUN_ME_batch18.txt`, QA #176-#178, `tools/_out/batch18_20261020/` README.md): Air-Way
first (incl. the 40 Triveni cells as Air-Way) + 50 ORFS masters + O-ring master 4000 + A14 + held roots 1700RC 1800 1703 4503 4603 fixed ->
1,534 configurations in a master, 151 masters; 1,531 of 2,535 OMi parts. Live `tools/` = `batch18_20261020/tools_b18`. Still held: 5404N
(QA #178). What the other ~1,000 parts need: `tools/_out/blocked_needs_20261020/BLOCKED_NEEDS.md`. Supersedes the Air-Way-first / ORFS
"staged" lines below.
**2026-10-20 (later): AIR-WAY FIRST - OMi's rule** (Triveni: Air-Way over Brennan, incl. OMi's own website file). STAGED, not shipped:
`tools/_out/airway_first_20261020/README.md` - 320 OMi-file cells back to Air-Way + 4 unbuildable Air-Way cells -> Brennan (user Q1) (236 configurations,
26 roots, 0 lost; static checks clean; 6410 reference -> 6410-24-20-O in `tools_af`), 43 cells to look at; PC dry-run kit in `dryrun/`. Next on the PC: read the
two "Review of Drawings" PDFs (being committed by the local session), SolidWorks dry runs, ship as batch 18.
**2026-10-20: BATCH 17 SHIPPED** (`03_SCRIPTS/RUN_ME_batch17.txt`, QA #173-#175, `tools/_out/batch17_20261019/` - RESUME.md is the run
log): the 2026-10-18 stage incl. the 37 adapters (apply_77.py never run - done) + the 5 generator features -> 1,354 of 1,874 configurations in a
master, 95 masters. Live `tools/` = `batch17_20261019/tools_b17` (Atan2V ByVal fix). Held for generator work: 4503 4603 1703 1700RC 1800 5404N.
Excel can crash during a design-table insert and leave a window open that breaks every later insert ("Configurations after table: 1") - close
it and re-run. Supersedes the 2026-10-19 lines below.

**2026-10-20 (cloud, branch `claude/pensive-planck-t9i90d`): READ `00_DOCS/NEXT_SESSION_PROMPT_2026-10-20.md` too** - ORFS generator staged
(`tools/_out/orfs_gen_20261020/`: 133 FS configurations in 50 masters + 8 FS4000 O-rings, all checks clean, no SolidWorks dry run yet; 29 more
Brennan STEPs measured in `tools/_out/orfs_steps2_20261020/`); branch rebased on batch 17 (fb1d145), staging tools = live tools + ORFS (Atan2V
fix ported; 99 / 99 roots identical to live). A14 (1603-08-08-08-FG) is staged only - not in batch 17. 1,351 shipped + 197 ready after
SolidWorks = 1,548 of 2,535. The ORFS work is not shipped.
**2026-10-19: START WITH `00_DOCS/NEXT_SESSION_PROMPT_2026-10-19.md`** (everything staged on 2026-10-18: Brennan data allowed and
marked, OMi answers, A1-A24 answers, the batch-17 stage + merged generator tools, 1,357 configurations generate; SolidWorks sign-in is
broken; nothing shipped since batch 15). The pointers below are older background.
**2026-10-19: BATCH 16 SHIPPED** (`03_SCRIPTS/RUN_ME_batch16.txt`, QA #170-#172, `tools/_out/ship_20261019/`): wave 1, leftovers,
JIC tees, 2404 (generated, two bores), 5405 + the corner-puck fix (`PUCK_INSET` in the live gen_tee.py) -> 1,103 of 1,804
configurations in a master, 71 masters in `11_MASTERS`. Live `tools/` + `04_DESIGN_TABLES` = the batch-16 state. Next: adapters77
(user OK), then batch 17. SolidWorks "License not granted ... License error 20" = lost 3DEXPERIENCE sign-in: the user signs in and
starts SOLIDWORKS Design from the platform; never start SLDWORKS.exe yourself.
**2026-10-18 (night): the folder is a git repo (branch main, `.gitignore` keeps it ~70 MB: no SolidWorks parts, old staging copies,
_to_delete, _archive) for Claude Code cloud sessions - see `CLOUD_SETUP.md` (the cloud runs the Python side only, never SolidWorks).
Commit new staging work you want in the cloud.**
**2026-10-18 (later): OMi answered the 2026-10-09 request - staged in `tools/_out/omi_answers_20261018/` (README.md; do not
overwrite): 15 rows MISSING -> ASSUMED from OMi's drawings / real lengths, not shipped; open: VERIFIED or ASSUMED, and whether
Brennan's catalog may now be used (PROJECT_STATUS s5).**
**2026-10-18: START WITH `00_DOCS/NEXT_SESSION_PROMPT_2026-10-18.md`** (whole-catalog count, all staged work of 2026-10-14 ... 18,
what waits on the user; nothing shipped since batch 15). The bold pointers below are the background it summarizes.
**2026-10-14: OMi said YES to O-rings / bent-tube elbows / flareless nut + sleeve - scope and what is needed:
`00_DOCS/Scope_ORings_BentTube_Flareless_2026-10-14.md` (size request for OMi drafted in `10_DRAWINGS/for_OMi_2026-10-14/`, not
sent). User: "use airway sizes"; 2026-10-15 "just do the solidworks models" (no drawings now). New model types STAGED in
`tools/_out/newtypes_20261014/` (README.md: O-ring master 4000 from Air-Way s218, sleeve type, bent-tube masters 1704T / 1703T / 6701
from the new `gen_bent.py` - all SolidWorks dry runs clean, bent tubes on TEST rows, incl. the 6701 nut thread and the code 62 -08 head;
Air-Way data in `tools/_out/airway_20261014/`) - do not overwrite either folder. SolidWorks' Thread feature (Inch Tap) on a female
edge off the origin axis CRASHED SolidWorks (2026-10-15): use gen_bent's `HelixThreadY` (helix + swept cut) instead.
2026-10-15 (evening): ORFS / compression / test-gauge intake ("use airway dimensions, check brennan too"): STAGED in
`tools/_out/orfs_airway_20261015/` (do not overwrite; summary `00_DOCS/ORFS_Compression_TestGauge_2026-10-15.md`) - 51 FS review
tables; on OMi's website 269 of 385 ORFS parts have dimensions (216 VERIFIED / 53 ASSUMED; forged FS parts VERIFIED only where Air-Way
plain = Brennan forged on every cell, user 2026-10-15). Website lists: `tools/_out/omi_enum_20261015/` (OMi's store allows ~2
requests/h - don't crawl it from a second session). ORFS model-type plan + STEP list: `tools/_out/orfs_modeltype_20261016/`.
The 77 adapters the 2026-09 crawl dropped: 37 wrongly-DROP rows staged to BUILD in `tools/_out/adapters77_20261016/` (do not
overwrite; apply with `apply_77.py --apply` only at ship time, after batch 16 - batch 16 shipped 2026-10-19).**
**2026-10-09: START WITH `00_DOCS/NEXT_SESSION_PROMPT_2026-10-09.md`** (drawings + OMi email done; 2404 / wave 1 / leftovers / JIC tees
staged and checked, SolidWorks dry runs next). The pointers below are older background.
**START WITH `00_DOCS/NEXT_SESSION_PROMPT_2026-10-01.md`** (2026-10-01 / 02), then `00_DOCS/NEXT_SESSION_PROMPT_2026-09-26.md`
(its 36 questions are still open except 1, 4 and 24 - see PROJECT_STATUS section 3). **Batch 15 SHIPPED 2026-10-08**
(`03_SCRIPTS/RUN_ME_batch15.txt`, QA #167-#169): 52 new configurations in 18 masters (OMi values + 5 -FG rows from their own
STEPs) -> 1,044 of 1,804 configurations in a master; 25 rows held for Q-BRENNAN-ONLY / conflicts. Batch 14b (2702 / 2703) shipped
2026-10-02 (QA #165-#166). New masters wave 1 is PAUSED (not merged; rebase its 2501 FOLDS table on the batch-15 table).
**Batch 14 SHIPPED 2026-10-02**
(`03_SCRIPTS/RUN_ME_batch14.txt`, QA #159-#164): Task A (OMi values, 18 roots) accepted, the tier-1 generator fixes
deployed in `tools/` (not 5404N-06), 22 masters replaced in `11_MASTERS` (6502 6802 6565 6404 6410 2403 2405 built for real
through the MCP, the 15 other Task A builds moved in from staging). Held: 2404 / 2404-L until OMi clarifies the bores,
2702 / 2703 = batch 14b, 5404N-06 (failed in SolidWorks). In progress: new masters wave 1 (`tools/_out/newmasters_20261002/`).
SolidWorks is now 2026 SP4 (since 2026-10-01; the control rebuilds showed SP4 = SP3).
Earlier (still valid): 20 dimension-check drawings (`10_DRAWINGS/`, how: `00_DOCS/DRAWING_AUTOMATION_NOTES.md`), overnight
build of 2026-09-25 accepted into `11_MASTERS` (`00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`), OMi dimension audit
(`00_DOCS/OMi_Dimension_Audit_2026-09-25.md`), batch 13b shipped (QA #156). User decision 2026-09-25: OMi's dimension file
outranks Air-Way for dimensions, Brennan for geometry, rounding-only differences are fine, rows taking an OMi value stay
ASSUMED. Evidence 2026-09-26: OMi's lengths are Brennan's data - OMi + Brennan count as ONE source.**

## Folders
- `01_MASTER_DATA` - MasterData workbook, the single source of truth (Parts, Topologies, QA_Log ...)
- `03_SCRIPTS` - the VBA build macros `Build_<root>_MASTER.bas` + their `Build_<root>_report.txt`
  (the macros write the reports here), drawing macros `OMi_*.bas`, and `RUN_ME_batch*.txt` = exactly
  what went to the user per batch; spec-sheet / drawing-template scripts `fill_specsheets.py`,
  `fill_drawing.py`, `make_*template.py`. `03_SCRIPTS/_legacy/` = superseded python and old batch zips.
- `04_DESIGN_TABLES` - `DesignTable_<root>.xlsx` = review tables (Air-Way rows reconciled with the
  OMi catalog: ScopeAction BUILD/DROP, DataStatus) = the generators' ONLY data input;
  `DesignTable_<root>_SW2.xlsx` = generated tables the build macros read
- `tools/` - the portable Python toolchain (see `tools/README.md`): `generators/` (gen_straight2.py,
  gen_tee.py -> macro + SW2 table), `checks/`, `measure/` (Brennan STEP measuring, OCP),
  `coverage/`, `omi_paths.py` (all paths). Output goes to `tools/_out/` (scratch) - except, until the user
  decides: `overnight/` (the only builds of the held-back 2702/2703), `regen_20260925/` (all macros with the
  2026-09-25 generator fixes - dry-run a root before re-shipping it unless PROJECT_STATUS lists it as built), `tee/`
  (13b as built), `omi_apply_20260925/` (Task A: before/after macros + SW2, the originals of the edited review tables,
  dry-run comparisons, Task B / Task C results), `drawings_20260926/` (drawing scripts), `tier1_20261001/` (tier-1 fixes:
  the SolidWorks dry runs batch 14 was checked against - `integrated/sw_tests/`, `regen/after/`, `swtest/` - and the
  held-out 5404N-06 fix, `work/5404N-06/`) and `ship_20261002/` (batch 14: build plan, build outputs, `old_files/` = the
  second copy of every file batch 14 replaced), `fix2702_20261002/` + `ship_20261002b/` (batch 14b), `batch15_20261002/`
  (batch 15 staging: CHANGES.csv per group, staged tables, the macros that built the parts, dry runs, held-row proposals),
  `ship_20261008/` (batch 15 ship: checks, scripts, `old_files/`), `newmasters_20261002/` (wave 1 history), and the batch-16
  folders `wave1_ship_20261009/`, `r2404_20261009/`, `puckfix_20261009/` (staging, the dry-run parts) + `ship_20261019/` (ship:
  checks, scripts, `old_files/`).
  Do not overwrite those: point env vars `GS_OUT` / `GT_OUT` at a new folder.
- `09_STEP_FILES` - Brennan reference STEPs `BRENNAN_<part number>.stp`; `11_MASTERS` - built masters;
  `11_MASTERS_NEW` - STAGING for builds waiting for the user's review (empty since batch 15 shipped on 2026-10-08: its 18
  dry-run masters moved to `11_MASTERS`); also the old screenshots and `fixed_macros/` (history).
- `10_DRAWINGS` - the 20 dimension-check drawings (2026-09-26) and their check review.
- `00_DOCS` - status, coverage workbook, measurement notes; `05_DIAGRAMS` - model-vs-Brennan sections
- `sw_mcp` - the SolidWorks MCP server (`server.py` tools, `swcom.py` COM layer, `call.py` CLI)
- `_archive/` - full snapshot of the Cowork workspace (history, all generator versions, transcript)
- `_to_delete/` - superseded files; nothing is ever deleted, it is moved here with a dated reason. The USER empties this
  folder into the Recycle Bin from time to time (7 times so far) - keep backups that open work depends on ALSO under
  `tools/_out/<task>/`.

## Toolchain (Python, `python -m pip install -r tools/requirements.txt`)
- Installed on this machine (`python` 3.14, cadquery-ocp 8.0.1 validated). On Windows the generators write CRLF,
  the shipped macros are LF: diff ignoring line endings.
- Regenerate a master: set `GT_OUT` (tees) / `GS_OUT` (straights) to a new folder, then
  `python tools/generators/gen_tee.py 6801` (or `gen_straight2.py <root>`) -> `<out>/Build_6801_MASTER.bas` +
  `DesignTable_6801_SW2.xlsx` + summary json (BLOCKED rows and warnings with reasons). Without them the output goes to
  `tools/_out/tee` / `straight` - never while `tools/_out/tee` is protected (above). Per-root definitions: `SPEC` at the
  top of each generator.
- Before anything ships: `tools/checks/dofcheck_*.py` (sketches exactly defined), `allcfg_check.py`
  (every configuration's outline), `vbacheck.py` (also > 24 line continuations = VBA will not compile),
  `regress.py` (old configurations unchanged); for a new end shape also a closed loop with `tools/measure`
  (rebuild -> measure -> must return the source).
- Changing a generator, template or `sp3fix.py` touches every macro: back it up to `_to_delete/superseded_<date>/`,
  regenerate ALL roots with old and new (`GS_OUT` / `GT_OUT` -> separate folders) and diff (only the intended lines
  change, SW2 tables identical), then build the affected roots in SolidWorks and compare every configuration's
  `sweep_configs` volume/size with the previous build. VBA traps there: `Annotation.Select3(False, Nothing)` selects
  nothing in an open sketch (use `Select2` + `EditDelete`); SolidWorks returns True as 1, so test `x = False`,
  never `Not x`.
- Ship = copy macro -> `03_SCRIPTS`, SW2 -> `04_DESIGN_TABLES` (old ones -> `_to_delete/superseded_<date>/`),
  write `03_SCRIPTS/RUN_ME_batch<N>.txt` (format: RUN_ME_batch13a.txt), QA_Log rows (next # = last row + 1),
  Topologies note, coverage refresh (`tools/coverage`), update `00_DOCS/PROJECT_STATUS.md`. Keep the evidence (check outputs,
  dry-run comparisons) as files, e.g. `tools/_out/ship_20260925_checks/`, `tools/_out/ship_20260925_dryrun/<root>/cmp_out.txt`.

## SolidWorks MCP (server `solidworks`, registered in `.mcp.json`)
SolidWorks 2026 SP4 must be running. Tools: sw_status, open_doc, close_doc, save_doc, doc_info,
list_features, rebuild, sweep_configs, get_dimensions, set_dimensions, mass_properties, geometry,
screenshot, activate_config, set_suppression, run_macro, run_python.

Verify loop for a new or changed master - do this before calling anything done:
1. Generate the `.bas` as usual.
2. `run_macro` with `const_overrides` `SAVE_PATH` + `REPORT_PATH` -> a scratch folder (dry run,
   `11_MASTERS` untouched; add `TABLE_PATH` when the SW2 table is not in `04_DESIGN_TABLES`, e.g. `tools/_out/tee`).
   Check `report.fail` / `fail_lines` and `msgbox`.
3. `sweep_configs` with the key `dims` -> every config rebuilds, 1 solid body, sizes plausible.
4. `geometry` on reference + extreme sizes -> cylinder dias, cone angles, plane offsets vs workbook.
5. `screenshot` (several views + a `section_plane`) -> actually look at it.
6. Only then build for real (no overrides) or hand the macro to the user.

Gotchas
- Tools report inches (units='mm' available); the raw API in `run_python` is metres/radians.
- Inspecting switches configs and marks docs dirty: close with `discard_unsaved=True`; never save a
  master from an inspection session.
- Masters are saved with `THD_*` suppressed. `set_suppression` to view threads, then put them back.
- Every master has SolidWorks' own "Default" configuration: not a table row, stale values - ignore it in checks.
- A running macro blocks SolidWorks; other calls queue (sw_status shows the job).
- Restart SolidWorks every ~40 builds: its memory only grows (11 GB after ~60) until a modal "critically low on
  committed memory" dialog (class #32770) silently blocks every call - if calls hang, look for it and answer No.
  Before restarting, check for the user's open documents and VBA editor windows (one called "test" was open).
  Making drawings leaks faster (~0.5 GB each): restart every ~10 drawings. Other programs count too (Firefox held 10 GB
  on 2026-09-26) - check committed memory (`Get-CimInstance Win32_OperatingSystem` FreeVirtualMemory) when it hangs.
- The MCP client aborts a call after 1800 s without output (the SolidWorks side keeps running) - keep calls shorter.
- Generating drawings through the API: read `00_DOCS/DRAWING_AUTOMATION_NOTES.md` first (typed VARIANT arrays for
  points / view positions, section views do not cut these masters, sheet scale reset after the first view, ...).
- Two parts with the same file name cannot be open at once (OpenDoc6 error 65536): open / close them in turn.
- Close a master before running its macro: if the file is locked, the macro (not 2500HX / 2603HX) saves
  `<root>_MASTER_hhnnss.SLDPRT` instead - the report's "Saved to ..._hhnnss" line tells.
- Tools not loaded in this session? `python sw_mcp/call.py <tool> '<json>'` or `@calls.json` - write that JSON with
  Python or the Write tool (PowerShell adds a BOM or writes ANSI, Bash heredocs eat backslashes).
- `run_python`: SolidWorks constants are attributes of `C` (`dir(C)`); wrap returned objects with `W(obj, 'IFace2')`.
- makepy wrappers live in `%TEMP%\gen_py` and regenerate on their own (~30 s).
- Stale-module trap (only when the user imports a macro by hand - `run_macro` compiles the `.bas` on disk): VBA
  keeps the old module if it was not removed before File > Import and runs it. Generated macros (not 2500HX /
  2502HX / 2603HX) trace "Master left in its reference configuration ..." - a report without it means an old module ran.
- Reports of macros from before the 2026-09-25 generator fixes (every `03_SCRIPTS` macro except the 22 batch-14 macros
  (RUN_ME_batch14.txt) and 6801-6804, plus `tools/_out/tee` and `11_MASTERS_NEW/fixed_macros` 6504 / 6565):
  the "N problem(s)" pop-up can exceed the FAIL lines - trust the FAIL lines. "angle try" / "angle ... was not
  created" = the named angle is DRIVEN and its table column is dead (harmless if the column is constant; it broke
  6404 -04/-06).
- A driving `<name>_SUPPL` angle (e.g. `SW2_CSANG_SUPPL` = 130) is intentional: the two sketch lines do not meet, so
  SolidWorks can only dimension the supplement (text position does not matter).

## Rules that don't bend
- Never fabricate a dimension, thread spec, tolerance, material or part number: every value has a
  cited source; no source -> empty cell + DataStatus MISSING. DataStatus / ScopeAction gates stay on.
- DataStatus: VERIFIED = 2+ independent sources agree, ASSUMED = 1 source, MISSING = none/conflict.
  Never average or majority-vote conflicting sources - ask the user.
- The OMi catalog decides which parts EXIST. DIMENSIONS (lengths, legs, hex, bores): **Air-Way first** wherever it prints a
  value (OMi / Triveni 2026-10-20: "prefer Airway over Brennan dimension when Airway has them available" - and yes, that
  includes the numbers of OMi's own website file `07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx`, which are
  Brennan's data); the OMi file / OMi's answers fill what Air-Way does not give, then Brennan (marked `$PRP@DimSource` BRENNAN).
  Supersedes the 2026-09-25 order (OMi > Air-Way). Rounding-only differences are not changes; an Air-Way value that cannot
  be built takes Brennan's value, marked BRENNAN (user 2026-10-20, Q1 "use brennans") - tell the user which cells. GEOMETRY (end shapes, forged bodies, seats, nuts, ports):
  Brennan STEPs, which also cross-check (differences: note in `$COMMENT`, tell the user). Enumerate rows; never trust a
  stated count.
- Log every modelling assumption (it goes into `$PRP@AxialSource` of every row it touches).
- One master per shape (2404 / C2404 / 2404-L share one; long variants fold in as rows). Exception, user 2026-10-18
  (Q-FS-MASTER): ORFS (FS...) series get their own masters - a face-seal end is a different sketch than a JIC end; their long /
  -LN variants fold in as rows.
- Carbon steel only. Threads are modelled but suppressed in saved models and STEP; drawings toggle them.
- Part number `{shape}-{JIC dash}-{NPTF dash}`, zero-padded (`2404-08-06`).
- Never delete files: move them to `_to_delete/<dated reason>/`. Never overwrite a file the user
  edited without re-reading it first.
- The user runs (or approves running) every macro; never save over a built master from an
  inspection. Never enter credentials or log into supplier sites; the user downloads STEPs.
