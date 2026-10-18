You are continuing work on the OMi carbon-steel fitting CAD library in `C:\Users\sudha\OneDrive\Desktop\OMi_Handoff`.
Read first, in this order: `CLAUDE.md`, `00_DOCS/PROJECT_STATUS.md`, `00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`, then load the
`omi-fitting-library` skill. Where the skill or `OMi_SOP_NewSeries.md` disagrees with CLAUDE.md, PROJECT_STATUS or this prompt
(generic D1..D6@DRIVE slots everywhere, the workbook as the design-table source), those three win; the skill's rules on sources,
DataStatus, no majority vote and enumerating rows still apply. CLAUDE.md "Rules that don't bend" apply throughout.

## Task
I am attaching an Excel file with all the dimensions OMi uses: `<PATH TO THE OMi EXCEL FILE>` (if you only see it as an
attachment, ask me for its path). Double-check, against that file, that every configuration and every dimension in the design
tables of the 126 topologies ("the 126 models") is right. This pass is an AUDIT: find and report, change nothing.

## Boundaries for this pass
- Do not modify any existing file. New files only in `07_RAW_EXTRACTS/omi_dimensions/` (an unchanged copy of the OMi file +
  a README with its SHA256; always read the copy), `tools/_out/omi_audit/` (your scripts and intermediates) and the two
  deliverables `00_DOCS/OMi_Dimension_Audit_<date>.xlsx` / `.md`.
- Do not run the generators, `tools/coverage`, `tools/checks`, SolidWorks or any macro, and do not measure STEP files. You may
  import the `SPEC` dicts from `tools/generators/gen_straight2.py` / `gen_tee.py` read-only; the BLOCKED lists are already in
  the `gen_*_summary.json` files. Never write into `tools/_out/tee`, `tools/_out/overnight` or `tools/_out/regen_20260925`.
- Do not move, accept or rebuild anything in `11_MASTERS_NEW` (38 parts = 34 new masters + rebuilds of 0318 0403 6405 6408,
  waiting for my review).
- Parallelise by topology group with subagents or a workflow; give them these rules verbatim; they return data, only you write
  the deliverables. Have every reported difference re-checked independently against both files - a false difference costs me
  more than a missed one. Stop ONCE, at the end.

## What you need to know about the data
- The 126 = sheet `Topologies` of `01_MASTER_DATA/OMi_Fitting_Library_MasterData_v1.xlsx` (= `07_RAW_EXTRACTS/cs_topologies.txt`).
  Its "Master status" column is stale - decide built / macro-ready from the files (`11_MASTERS`, `11_MASTERS_NEW`,
  `03_SCRIPTS/Build_<root>_MASTER.bas`, `tools/_out/overnight`). 118 topologies have a review table; none for the 4 kits
  (1901 1902 1927-61 1927-62, out of scope) and the 4 not started (2402 6316 6540 7202) - report OMi parts for those separately.
- Review tables `04_DESIGN_TABLES/DesignTable_<root>.xlsx` (135 files): row 1 title, row 2 header, column A = configuration name;
  `$PRP@PartNo`, `$PRP@OMiSKU`, `$PRP@ScopeAction` (BUILD/DROP), `$PRP@DataStatus`, `$PRP@AxialSource`, `$COMMENT`, and in 2408
  2501 6801 6802 an UNLABELED column before ScopeAction holding "RESOLVED 2-1" notes - read it. 2404's table is
  `DesignTable_2404_FINAL.xlsx`; ignore `DesignTable_6400_v2.xlsx` (stale copy); 2407 and 6409 are outside the 126 (all DROP).
  Dimension columns are mostly Air-Way catalog letters (`M1@DRIVE`, `L32@DRIVE`, `C1HEX@HEX`, `Y@HEX`, `D1@BORE`, `Y@REF` ...;
  inches, degrees), but 2404 and 6400 use generic slots mapped by the workbook sheet `DimensionMap` (e.g. 2404 D1@DRIVE = L).
  Many columns are not Air-Way at all: thread majors, JIC/NPTF/ORB end geometry come from standards, some values from Brennan
  or distributors - tag every column's source from `$PRP@AxialSource` / the title before comparing.
- Variant tables count toward their base topology in the summary, but not necessarily its master: separate masters 5404N,
  5406C, 5406P; folded into the master 2403LH, 2501L (13b); in no master yet 2404L/LL, 6400L, 6500L, 6801L/LL/LLL, 2501LL/LLL.
- SW2 tables (what the masters were built from; row 1 header): 53 in `04_DESIGN_TABLES` are generated (SPEC roots); 2403 2404
  2405 2500HX 2502HX 2603HX 6400 are older hand-made ones - read their columns from `03_SCRIPTS/Build_<root>_MASTER.bas`, and
  they cannot be regenerated. Which SW2 belongs to which built part: `11_MASTERS` -> `04_DESIGN_TABLES`; `11_MASTERS_NEW` 2501
  6801 6802 6803 6804 -> `tools/_out/tee`; 6404 6504 6565 -> `tools/_out/regen_20260925/straight`; held-back 2702 2703 ->
  `tools/_out/overnight`. 2404 and 6400 are hand-built masters whose files are not in the repo. Do not open SolidWorks: the
  configuration list of a master = the row set of the SW2 it was built from.
- SW2 value conventions: only columns whose name ends in R before the @ are radius-like (BODYR = hex corner radius A/F/sqrt3 on
  straights, = HEXAF/2 on gen_tee legs; THDMAJR = major/2; *_CONER, *_GRVR, *_MAJR) - check the generator code for each such
  column. Lengths, bores (`D*@BORE*`), tap drills, `HEXB@HEX`, `HEXAF@*`, HELIXDIA are full values; 2404/6400 SW2 are full
  values. In gen_tee SW2 tables `M<i>@LEG<i>`, `D<i>@BORE<i>`, `THD_End<i>` are leg slots in SPEC['legs'] order (swapped for the
  45 deg elbows 2503 6502 6802), not Air-Way letters, and `HEXAF` = max(catalog hex, thread majors, male NPTF OD) on every gen_tee
  root and on 2500HX/2502HX/2603HX: compare OMi's hex with the review value and show the SW2 value only as "raised by rule".
- Generated SW2 tables leave out DROP rows, DataStatus MISSING rows (727 of the 1,804 BUILD rows are MISSING) and BLOCKED rows.
- Part numbers: match the OMi file EXACTLY against `$PRP@OMiSKU`, which is in the OMi web-feed format (`2701-LN-06-06-FG`,
  `1700-08-08`, `5406-P-16`, `5404-N-04X2.000`, `6408-02-O`); `$PRP@PartNo` is Air-Way style and differs on 128 BUILD rows. If
  the OMi file's format differs, write the normalization rule down and list every part it touched. Never fuzzy-match. One OMi part
  can map to several rows (2408 SOLID / H) - compare each. The OMi feed `07_RAW_EXTRACTS/omi_feed/omi_skus_all.txt` (1,831 SKUs,
  part numbers only) is the current existence list; `00_DOCS/OMi_Coverage_2026-09-24.xlsx` maps every feed SKU to a table and a
  code (F1-F5, N1-N4 on its Summary sheet).
- Air-Way printed values: `07_RAW_EXTRACTS/<series>.csv` (formats vary - some without a header row, some comma- instead of
  pipe-delimited, dashes unpadded; `README_column_definitions.md` covers only 4 series and is stale on format). No CSV for 2403
  2405 2406 2408 5404 6401 6405 6408 6500 6803 6804: write "no raw extract in repo - review value shown"; do not unpack `_archive`.

## Steps (one stop, at the end)
1. Read the OMi file: every sheet incl. hidden sheets and rows, multi-row / merged headers, units (inch / mm, fractions vs
   decimals), min/max or tolerance columns (a value inside the envelope is conforming, not a difference). Read it once with
   data_only=True and once with False: a formula cell without a cached value is a finding. If it is .xls/.xlsb, convert a copy
   and keep both hashes. Enumerate what it covers (topologies, part count, dimensions offered).
2. Configuration audit per topology (no column mapping needed): OMi parts vs BUILD rows - missing configurations (in OMi, absent or
   DROP in the table), extra BUILD rows (table, not OMi), OMi parts not in the feed, ORFS (FS-, coverage N2), compression (C-, N3)
   and test-gauge (TGT-, N4) parts (not tabled yet; they fold into existing topologies as rows). For every root with an SW2: join
   SW2 rows to review rows (SW2 `$PRP@OMiSKU` if present, else column A / `$PRP@PartNo`) and report BUILD rows missing from the
   SW2 with the reason (MISSING-skip or BLOCKED from `gen_*_summary.json`; "no summary" for the 7 hand-made tables) and SW2
   configurations that are DROP, absent or renamed in the review table (a master modelling a part OMi may not sell).
3. Column mapping per topology: OMi column -> review column -> SW2 column. A mapping is certain only when the OMi header names the
   same feature as the Air-Way letter on both sources' drawings (letters are not portable between sources); value agreement alone
   does NOT prove a mapping. Sources for letter meanings: the CSV header row, SPEC 'assume' texts, the review-table title and
   AxialSource, `DimensionMap` (2404/2501/6400/6801/6802 only). Compare thread callouts as normalized strings with `$PRP@Threads`
   / `$PRP@EndX_Thread`, not with THDMAJ numbers.
4. Dimension audit for every BUILD row - and every DROP row that the OMi file lists - and every certainly-mapped dimension: review
   value, OMi value, SW2 value where one exists (converted as above). Compare in exact arithmetic (fractions.Fraction /
   decimal.Decimal, never floats). Classes: equal / rounding only (OMi's value rounded half-up to the decimals Air-Way printed
   equals the Air-Way value - keep these rows visible, they answer the open hex A/F question) / real difference / only one source
   has a value. For each real difference: Air-Way printed value, a Brennan value only if already recorded (`BRENNAN_NOTES`,
   `$COMMENT`, `$PRP@AxialSource`, `00_DOCS` measurement notes; else "STEP available, not measured" if a
   `09_STEP_FILES/BRENNAN_*` file exists), the column's source tag, and where the part stands: 11_MASTERS | 11_MASTERS_NEW |
   both (0318 0403 6405 6408) | hand-built, file not in repo (2404 6400) | held back (2702 2703) | macro only | table only.
   Comparisons that rest on an uncertain mapping go to a separate PROVISIONAL sheet, not into the headline numbers.
5. Known items - give OMi's value for each, decide nothing:
   - every row whose text says RESOLVED / 2-1 / outvoted (read the unlabeled column; at least 2404-16-24, 2404-24-20,
     2408-14-SOLID, 2501-04-02-FG, 2501-32-32-FG, 5404-32-20, 6801-05-05-NWO-FG, and the DROP rows 2501-14-12-FG,
     6801-05-05-NWO, 6802-14-14-NWO). These are majority-vote resolutions, which CLAUDE.md forbids - treat them as open
     conflicts. In 2408-14-SOLID, 2501-04-02-FG and 2501-32-32-FG the voted value sits one column to the right (THDMAJ_B /
     THDMAJ_A / Y@REF hold 1.25 / 0.78 / 1.938) and "VERIFIED" landed in AxialSource: report it, do not move it;
   - 2408 duplicate OMiSKUs (2408-04, -06, -20); 6404-06-08 length 1.10 vs 6404-06-06 1.38;
   - PROJECT_STATUS sections 2 and 3: hex A/F Air-Way 2-decimal vs wrench fraction, 1501-24-24-FG nut 1.88 vs 2.125,
     6801-05-05, and the OMi findings 6801-04-02 leg / 6801-12-12 thread length;
   - the row-level entries of `07_RAW_EXTRACTS/airway_anomalies_2026-09-23.txt` (skip the "(table)" lines; one line can name
     several cells);
   - rows that are MISSING today (727 BUILD rows; coverage codes F1-F5, the 18 SKELETON-MISSING topologies): which ones the OMi
     file could fill. For F1 (BUILD-NEAR -FG rows) only report - using OMi instead of waiting for Brennan -FG STEPs reverses a
     decision of mine (PROJECT_STATUS section 5);
   - independence evidence for my ranking decision: on the Air-Way misprints and the 3-way conflict rows, does OMi reproduce the
     Air-Way value? Count rows where OMi equals Air-Way to the printed decimals vs where it differs.
6. Deliverables: `00_DOCS/OMi_Dimension_Audit_<date>.xlsx` (Summary per topology; Config differences; SW2 row differences;
   Dimension differences; PROVISIONAL; Column mappings with evidence; Unmapped OMi columns; OMi parts not in feed/tables; Known
   items) and `00_DOCS/OMi_Dimension_Audit_<date>.md` (headline numbers, method, and every question for me). Then stop.

## Decisions that are mine
How OMi ranks against Air-Way and Brennan (does OMi override Air-Way? is OMi + Air-Way agreeing VERIFIED - is OMi independent?),
the rounding threshold, every uncertain mapping, anything the SOP marks STOP.

## Later, only after I approve
Follow CLAUDE.md: back up each table to `_to_delete/superseded_<date>/`, edit review tables with sources in `$PRP@AxialSource`,
regenerate into a NEW `GS_OUT` / `GT_OUT` folder, run `tools/checks`, and do the SolidWorks verify loop as a DRY RUN into scratch
only - never overwrite `11_MASTERS` or `11_MASTERS_NEW`. SolidWorks was left at 11 GB: before restarting it, if any document or
VBA editor window is open, stop and ask me; never kill the process. For 2403 2404 2405 2500HX 2502HX 2603HX 6400 (no generator)
propose the change and ask. Then update PROJECT_STATUS.md and QA_Log (next # = last row + 1).
