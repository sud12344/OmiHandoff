# tools/: the OMi toolchain (portable Python)

Everything here runs from any working directory. All paths come from `tools/omi_paths.py` and are relative to the
OMi_Handoff root.

```
python -m pip install -r tools/requirements.txt        # openpyxl, numpy; cadquery-ocp only for measure/
```

On 2026-09-25 the portable generators were checked against the Cowork originals: they produce byte-identical macros and
content-identical SW2 tables for all 29 straight and 28 tee/elbow roots.

## generators/: review table -> SolidWorks build macro + SW2 design table

```
python tools/generators/gen_straight2.py 6404 6410          # straights  -> tools/_out/straight/ (or $GS_OUT)
python tools/generators/gen_tee.py 2501 6801                # tees, crosses, 90/45 deg elbows -> tools/_out/tee/ (or $GT_OUT)
```

Until the user has reviewed the 2026-09-25 overnight build, `tools/_out/tee` is protected (see `_out/` below): set the
environment variables `GS_OUT` / `GT_OUT` to a new folder before running a generator.

Each root writes three files:
- `Build_<root>_MASTER.bas` (entry `Sub Build<root>`)
- `DesignTable_<root>_SW2.xlsx`
- `gen_*_summary.json` (configurations, skipped rows, BLOCKED rows with reasons, warnings)

**Only input:** `04_DESIGN_TABLES/DesignTable_<root>.xlsx`, the review tables. Air-Way rows are reconciled with the OMi
catalog through `$PRP@ScopeAction` (BUILD/DROP), and `$PRP@DataStatus` acts as the release gate.

**Frozen inputs in `templates/`:**
- the VBA helper libraries (2405 and 2603HX macros)
- the v1 generator text (HelixThread)
- the JIC and female pipe end libraries: the SW2 tables of the built 2403/2405 masters (VERIFIED against Brennan)

**Per-root definitions:** `SPEC` near the top of each generator.

**Measured end data** is kept in these tables, each commented with its Brennan STEP source and the script that measured it:
- `SWIV_MEAS`, `ORBF_MEAS`, `JICF_MEAS`, `NPSM_MEAS`, `FLG61_MEAS`, `ORB_GW_MEASURED`, `PLUG_HOLE_MEAS` in `gen_straight2.py`
- `NWO_MEAS` and the chamfer constants in `gen_tee.py`

**The macros themselves:**
- The macro text contains the Windows path of OMi_Handoff (`omi_paths.DEV`); set `OMI_DEV` if the folder moves.
- Macros write their report to `03_SCRIPTS\Build_<root>_report.txt` and save to `11_MASTERS\<root>_MASTER.SLDPRT`.

**Known limit:** `gen_tee.py 1503` stops with "angled leg must carry a Thread-feature (JIC) end". No angled pipe
thread yet.

## checks/: run before anything ships

| Script | What it proves |
|---|---|
| `dofcheck_straight.py <bas>` / `dofcheck_tee.py <bas>` | every leg / DRIVE sketch is exactly defined (Jacobian rank = unknowns, no redundancy) |
| `allcfg_check.py s\|t <roots>` | the outline of EVERY configuration is clean (no self-intersection, no zero segment); the macro itself only draws the reference size |
| `vbacheck.py <bas>` | static check of the macro text (procedure structure, keywords, calls) |
| `regress.py <old_dir> <new_dir> <roots>` | configurations that existed before keep identical values |

## measure/: Brennan STEP measuring (OCP)

Each script cuts a section through a leg axis and walks the outline, using `section.py` and `prof.py`.
- Run one on a STEP from `09_STEP_FILES` (`BRENNAN_<pn>.stp`), for example `python tools/measure/swiv.py 09_STEP_FILES/BRENNAN_6500-10-10-FG.stp`.
- Every extractor was validated on the sizes measured before it was used on new ones.

| Script | Measures |
|---|---|
| `swiv.py` | female JIC swivel nut and nose |
| `ports.py` | female ORB / JIC ports |
| `npsm.py` | NPSM swivel |
| `flange.py` | code 61 flange head |
| `nwo.py`, `nwo_run.py`, `nwo_chamfer.py` | adjustable ORB end and nut chamfers |
| `nwo_cmp.py` | Brennan 6801 vs Air-Way comparison, written to `tools/_out/scratch/cmp6801.json` |
| `nwo_model.py <root> <pn...>` | rebuilds configurations as solids from the generator's own geometry and writes STEPs to `_out/scratch` |
| `nwo_closedloop.py <pn>` | measures that rebuild with the Brennan extractor |
| `nwo_allcfg_ocp.py <root>` | builds every configuration as one solid and checks the nut cut volume |

## coverage/: OMi catalog coverage workbook

```
python tools/coverage/omi_enum.py && python tools/coverage/coverage.py && python tools/coverage/write_cov.py
```

This reads the OMi SKU feed (`07_RAW_EXTRACTS/omi_feed`), the review and SW2 tables, and `need_compact.txt` (Brennan
STEPs still needed). It writes `00_DOCS/OMi_Coverage_2026-09-24.xlsx`, with intermediates in `coverage/work/`.

## _out/

This is scratch output; everything in it can be regenerated - EXCEPT, until the user has decided on the 2026-09-25
overnight build, these folders (do not overwrite or clean them):
- `_out/tee` - the batch 13b candidates (2501, 6801, 6802, 6803, 6804) exactly as built in SolidWorks.
- `_out/overnight` - the overnight builds, incl. the only builds of the held-back 2702 / 2703.
- `_out/regen_20260925` - all 57 macros regenerated with the overnight generator fixes (the set to ship from).
See `00_DOCS/PROJECT_STATUS.md` and `00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`.
