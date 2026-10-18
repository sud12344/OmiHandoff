# Wave 2 brief - Brennan rows in existing families (2026-10-18)

Project: OMi fitting CAD library, `C:\Users\sudha\OneDrive\Desktop\OMi_Handoff`. Read `CLAUDE.md` first. Hard rules: never fabricate a value;
every value has a cited source; never average or majority-vote conflicting sources (list the conflict instead); never delete files (if you
must discard something you created, move it to `_to_delete\<dated reason>\`); never run SolidWorks or macros; do not crawl websites.

## The decision
User 2026-10-18: "yes use brennan but still differentiate the two in tables in case i need to change it later". Brennan's catalogs and
Brennan 3D files may now give sizes. OMi values (07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx, sheet Items) and Air-Way values
already in a table still win; Brennan only fills EMPTY cells. The main session applies your cells with the marking ($PRP@DimSource = BRENNAN,
AxialSource prefix) - you do NOT edit review tables.

## Your rows
`wave2/rows_<group>.csv` (columns group, table, config, how, other_gates, steps). how = 'catalog' (Brennan prints the part) or '3D file'
(only a Brennan STEP has it: `09_STEP_FILES/BRENNAN_<pn>.stp` - if the file is not there, hold the row "needs STEP download").
other_gates = decisions still open for that row (see `00_DOCS/OPEN_QUESTIONS_2026-10-18.md`): you may still prepare its values, but the row
is ready = no with the gate named. Decisions already taken (PROJECT_STATUS.md section 5): Q-TRANSFER-ENDLIB = yes (end details per dash from
the end libraries), the 6 generator capabilities = yes (but only usable if the batch-16 generator already implements them), Brennan = yes.

## Sources
- Brennan catalog parse: `tools/_out/brennan_catalog_20261001/catalog_verified.json` (+ .xlsx, catalog_index.json); PDFs in
  `07_RAW_EXTRACTS/brennan_catalogs/`. Catalog column letters mean different things per series - establish each mapping from the catalog's
  own drawing / header AND confirm it on rows of the same table that have both an Air-Way (or OMi) value and a Brennan value (pairing: they
  should agree to rounding on most rows). Write each mapping with its evidence.
- Earlier work you can reuse (do not copy blindly - re-check): `tools/_out/unblock_20261008/` (rows.csv, bridge.json), the impact / tier-1 /
  batch-15 / wave-1 / wave-2 folders under `tools/_out/` (e.g. `wave2_shapes_20261008`, `wave2_impl_20261009`, `batch15_20261002/work/*/`,
  `newmasters_20261002/work/*`), measuring tools `tools/measure/` (validated scripts only - each must reproduce known sizes first).
- Today's base tables (read-only): `tools/_out/brennan_yes_20261018/base_root/04_DESIGN_TABLES/` (header row 2, part number column A).
- Generators to test: `tools/_out/puckfix_20261009/tools_new/generators/` (gen_straight2.py, gen_tee.py and any other generator there).
  They read OMI_ROOT/04_DESIGN_TABLES, write to GS_OUT / GT_OUT. Run with `python -I`.

## Output (only inside `tools/_out/brennan_yes_20261018/wave2/<group>/`)
1. `cells.csv`: table,config,column,value,source,kind - kind 'brennan-dim' | 'endlib' | 'other' (explain in source). Only cells empty in
   the base. Do not include DataStatus / DimSource / AxialSource cells (the apply script sets them); a `$COMMENT` cell is appended as a note.
   New dimension columns are allowed if the generator needs them (say so in the report).
2. `rows.csv`: table,config,ready(yes/no),missing_columns,gates,conflicts,notes.
3. TEST: copy the whole base 04_DESIGN_TABLES into `<group>/test/root/04_DESIGN_TABLES`, apply your cells there (DataStatus ASSUMED on ready
   rows), regenerate every affected root with OMI_ROOT there and GS_OUT / GT_OUT inside `<group>/test/`; also generate from an untouched base
   copy; compare. Report rows that become configurations, rows that BLOCK (generator reason), and that every pre-existing configuration is
   unchanged. Run the static checks in `tools/_out/puckfix_20261009/tools_new/checks/` (vbacheck, dofcheck_*, allcfg_check `s|t <roots>`).
4. `REPORT.md`: per table ready / blocked / held with reasons, the letter mappings with evidence, conflicts, open points.

Reply when done with: counts (ready, blocked, held), conflicts, and the file paths. Keep the reply short.
