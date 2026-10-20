# Next session - start here (written 2026-10-18; sessions of 2026-10-14 to 2026-10-18)

Read `CLAUDE.md`, then this file, then `00_DOCS/PROJECT_STATUS.md` (section 1 top: the catalog-wide count; section 3 item 0: this
work; section 5: the decisions of 2026-10-14 ... 2026-10-18). **Nothing was shipped in these sessions**: everything below is staged
under `tools/_out/` (do not overwrite those folders). SolidWorks was not running at the end; nothing is open in it.

## The whole catalog (2026-10-18)
OMi's website lists 2,535 carbon-steel parts. All are now listed (`07_RAW_EXTRACTS/omi_feed/`: `omi_skus_all.txt` = the old 1,831;
new two-pass lists `omi_skus_orfs.txt` 385, `omi_skus_compression.txt` 230, `omi_skus_testgauge.txt` 12, `omi_skus_cs_adapters_full.txt`
1,672). Count (`tools/_out/adapters77_20261016/scripts/possible_2535.py` -> `possible_2535.json`):

| Status | Parts |
|---|---|
| Built | 1,041 |
| Have dimensions, my work only | 145 |
| Have dimensions, ORFS (waiting on the ORFS model type) | 269 |
| Need only the user's STEP downloads | 75 |
| Need the user's decisions | 142 |
| **= possible under today's rules** | **1,672** |
| Only with Brennan data (catalog 517, 3D file only 53) - Q-BRENNAN-ONLY is NO | 570 |
| No source at all - needs OMi (compression 230, test gauge 12, 4005 9, flareless 3, 6 adapters, 6 ORFS) | 266 |
| Kits, out of scope | 30 |

## Staged work, by folder
1. **New scope - O-rings / bent tubes / flareless** (OMi said yes 2026-10-14; user: "use airway sizes"; "just do the solidworks
   models", drawings paused). Folder: `tools/_out/newtypes_20261014/` (README.md).
   - O-ring master 4000 (4000 + 4001, 21 configurations, Air-Way s218): dry run 0 FAIL.
   - Sleeve type proven on TEST rows.
   - Bent-tube generator `gen_bent.py` -> 1704T / 1703T / 6701, on TEST rows: dry runs 0 FAIL (101 / 98 / 147 OK). It includes the
     6701 nut thread (`HelixThreadY`), the code 62 -08 head, and a check that rebuilds every configuration with the threads on.
   - Waiting:
     - OMi's sizes for the bent tubes, 4005 and flareless. The request is drafted, not sent: `10_DRAWINGS/for_OMi_2026-10-14/`.
     - Code 62 -12 / -20 / -24 / -32 Brennan files; V0318-08 / V0319-08.
   - Scope doc: `00_DOCS/Scope_ORings_BentTube_Flareless_2026-10-14.md`.
2. **ORFS intake** (user: "use airway dimensions, check brennan too"). Folder: `tools/_out/orfs_airway_20261015/` (README.md); summary
   `00_DOCS/ORFS_Compression_TestGauge_2026-10-15.md` + `.xlsx`.
   - 51 Air-Way ORFS series (double pass) -> 51 staged review tables `DesignTable_FS*.xlsx`.
   - On the website: 269 of 385 have dimensions (216 VERIFIED, 53 ASSUMED).
   - Forged FS parts are VERIFIED only where Air-Way's plain row = Brennan's forged row on every cell (user 2026-10-15).
   - Pair Air-Way and OMi series by connection type, not number: FF6402 = FS6540, FF7504 = FS6504, FF2407 = FS2406, FF7403 = FS6403.
3. **ORFS model type**. Folder: `tools/_out/orfs_modeltype_20261016/`.
   - PLAN.md + STEPS_NEEDED.txt: 31 new FS masters, 32 Brennan STEPs, 9 pilots first.
   - **User 2026-10-18: "yes for all design questions"** (DECISIONS.md; PROJECT_STATUS s5): own master per FS series, ORB_FS / NWO_FS
     studs measured on pilots, Air-Way 3D models as a second shape source for the pilots, FF318 nut hex, FS2406 with its nut, FS2408
     solid until OMi answers.
   - **Next: the user downloads the 9 pilot Brennan files (S1)** and the Air-Way 3D models of the pilots (S2; the 3DContentCentral
     sign-in is the user's). Then: extractors (`tools/measure`), end-library entries (FSM / FSSW / FSBH / ORB_FS / NWO_FS), FS SPECs,
     dry runs - PLAN.md sections 2-6.
4. **77 tube fittings the 2026-09 crawl dropped**. Folder: `tools/_out/adapters77_20261016/` (REPORT_77.md).
   - 37 were Air-Way rows wrongly marked DROP. `CHANGES.csv` (136 lines) turns them BUILD (21 VERIFIED / 14 ASSUMED / 2 special,
     OMi values first, Brennan check).
   - **Apply with `scripts/apply_77.py --apply` only at ship time, after batch 16** (it has its own 2501 / 6500 / 6505 tables).
   - The other 40 have no Air-Way row.
5. **Website listing tools + report**: `tools/_out/omi_enum_20261015/` (REPORT.md). omindustrial.com throttles scripts (HTTP 429,
   at times ~2 requests / hour) - never crawl it from two sessions at once.
6. ~~Still in flight from before: batch 16~~ **BATCH 16 SHIPPED 2026-10-19** (`03_SCRIPTS/RUN_ME_batch16.txt`, QA #170-#172,
   `tools/_out/ship_20261019/`): wave 1, leftovers, JIC tees, 2404, 5405 + the corner-puck fix; 1,103 of 1,804 configurations in a
   master, 71 masters in `11_MASTERS`. The live `tools/` and `04_DESIGN_TABLES` are now the batch-16 state - stage later batches on it.

## Waiting on the user
- Send the OMi size request (`10_DRAWINGS/for_OMi_2026-10-14/`). It could also ask: compression / test-gauge dimensions, the FS2408
  hole, the 40 adapters with no Air-Way row.
- Downloads:
  - ORFS pilots: 9 Brennan + the Air-Way 3D models.
  - Code 62 heads.
  - V0318-08 / V0319-08.
  - 1704-16-16 / 1803-16-16 / 6701-08-08 (bent-tube shape checks).
- Decisions:
  - ~~Ship batch 16~~ (shipped 2026-10-19). Next: OK to apply the 77-adapter changes.
  - The employer's feedback on using Brennan data (up to 570 more parts).
  - The open questions of the 142 rows (`tools/_out/unblock_20261008/rows.csv`, gates re-judged by `possible_2535.py`).

## Gotchas learned 2026-10-14 ... 18
- SolidWorks' Thread feature (Inch Tap) on a female edge off the origin axis CRASHED SolidWorks. Use gen_bent's `HelixThreadY`
  (helix on a plane + 60 deg profile + swept cut).
- After a SolidWorks restart a second instance may show a 3DEXPERIENCE "go to the platform?" dialog. Answer No; never sign in.
- 2026-10-19: "License not granted: X1W ... roles have changed ... (License error 20)" and SolidWorks closing mid-job = the desktop app
  lost its 3DEXPERIENCE sign-in (since 2026-10-15), not a role change: `%APPDATA%\DassaultSystemes\SWXDesktopHelper\<date>_*.log` shows
  the role query answered by the 3DPassport login page ("pageId = \"login\"", "JSON parse error"). The user signs in again and starts
  SOLIDWORKS Design from the platform compass. Never start SLDWORKS.exe yourself (it starts without a license).
- `python sw_mcp/call.py` from the Bash / PowerShell tools can report "SolidWorks is not running" while the MCP tools reach it - use
  the MCP tools then.
- `run_macro` with a missing report / save folder raises VBA error 76: a modal box that blocks SolidWorks. Create the folders first
  (the new macros check this).
- Circular-profile sweep: select the path sketch with mark 4, then CreateDefinition + CircularProfile. Setting `.Path` silently
  creates nothing.
- Air-Way's API `parts.air-way.com/api/series/<id>` returns a whole series table (two fetches = the double pass). Its spec drawings
  give the letter meanings (memory: airway-spec-drawings-and-3d).
- Bash heredocs eat backslashes and quote escapes - write scripts and patches with the Write / Edit tools.
