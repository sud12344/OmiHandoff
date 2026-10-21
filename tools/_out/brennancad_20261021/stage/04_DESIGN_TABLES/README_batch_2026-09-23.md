# Design tables generated 2026-09-23 (batch: all remaining Air-Way-covered topologies)

62 roots from Air-Way carbon-steel series pages (double-pass extraction, values as printed, single-source => DataStatus ASSUMED)
plus 18 SKELETON tables (roots with OMi SKUs but no Air-Way page => every row MISSING, no dimensions).

Columns: <catalog letter>@DRIVE (lengths), <letter>@HEX (W/Y wrench flats, C-family hex as CnHEX), D*@BORE, TAPDRILL*@BORE,
THDMAJ_<threadcol>@DRIVE (major dia, only for recognised standard callouts), $PRP@TubeOD, $PRP@PartNo (zero-padded),
$PRP@Threads (as printed), $PRP@DataStatus, $PRP@AxialSource, $COMMENT, $PRP@ScopeAction (BUILD/DROP vs OMi feed), $PRP@OMiSKU.

Rows appended after the Air-Way rows are OMi SKUs with no Air-Way row: DataStatus MISSING, no dimensions.
"BUILD-NEAR" in $COMMENT = the only Air-Way row of that size differs by the -FG (or UNPL) suffix; its dims were NOT copied (client decision pending).

Sources of truth: 07_RAW_EXTRACTS/<root>.csv (as printed), 07_RAW_EXTRACTS/airway_passes/ (both fetch passes),
07_RAW_EXTRACTS/airway_anomalies_2026-09-23.txt, 07_RAW_EXTRACTS/omi_feed/ (SKU crawl), 07_RAW_EXTRACTS/scope_report_2026-09-23.json.
Generator: 03_SCRIPTS/gen_tables.py -> scope.py -> update_wb.py (QA_Log #116-123).
