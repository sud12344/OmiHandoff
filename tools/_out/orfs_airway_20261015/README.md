# ORFS / compression / test-gauge intake (2026-10-15) - STAGED, nothing shipped

User 2026-10-15: "use airway dimensions, check brennan too" (for the ~704 OMi carbon-steel parts that were never in our part list:
ORFS 385, compression 230, test gauge 12, ~77 dropped adapters). Readable summary: `00_DOCS/ORFS_Compression_TestGauge_2026-10-15.md`;
every part: `00_DOCS/ORFS_AirWay_Brennan_2026-10-15.xlsx`.

| Path | What |
|---|---|
| `raw/series_<id>_pass1/2.json` | Air-Way API responses, 51 ORFS series, two fetches (identical) |
| `airway_orfs_summary.json` | per series: rows, columns, passes identical, pass files written |
| `compare_orfs.json` / `.csv` | every OMi FS part (OMi parts file, 499): Air-Way row, Brennan row, thread / dimension check, status + reason |
| `forged_info.json` | INFORMATION ONLY: Air-Way non-forged vs Brennan -FG agreement (669 / 770 cells) |
| `review_tables/DesignTable_FS*.xlsx` | 51 staged review tables, one per OMi FS series (Air-Way values, Brennan check per row); `review_tables_summary.json` |
| `scripts/` | `fetch_orfs.py` (pass1 / pass2 / compare), `load.py`, `compare_orfs.py`, `forged_info.py`, `build_tables.py`, `make_report.py` |

Pass files (new, the usual format): `07_RAW_EXTRACTS/airway_passes/FF*_p1.txt` / `_p2.txt` (+ `AWs40` / `AWs41` / `AWs218`).

Rules applied: Air-Way = the source; Brennan = the check only (Q-BRENNAN-ONLY = no); Air-Way = Brennan -> VERIFIED, Air-Way only ->
ASSUMED, differ -> built to Air-Way, ASSUMED, Brennan's value in `$COMMENT` (PROJECT_STATUS s6 convention), no Air-Way row -> MISSING;
forged parts (user 2026-10-15): the Air-Way non-forged row only where Brennan's forged row matches every compared cell ->
VERIFIED, else MISSING (`FORGED_BR` / `FORGED_PAIRS` / `forged_check` in compare_orfs.py); rounding rule = match_ORFS.py `cmp_num`.
Result (OMi parts file, 499 FS, 51 tables): 229 VERIFIED (106 plain + 123 forged), 59 ASSUMED (44 of them Brennan differs),
211 MISSING (70 plain with no Air-Way row + 141 forged). Pairing by connection type (FF6402 = OMi FS6540, FF7504 = FS6504,
FF2407 = FS2406, FF7403 = FS6403; OMi FS6402 / FS2405 / FS0304-C / FS1700 / FS1800 have no Air-Way series).

**Scope (2026-10-16):** BUILD = on OMi's website ORFS list - the two-pass `07_RAW_EXTRACTS/omi_feed/omi_skus_orfs.txt` published by the
listing session (`tools/_out/omi_enum_20261015/`), 385 SKUs = the published count = the earlier single-pass copy
`omi_orfs_website_passA.txt` (identical; the tables were re-run on the published list, counts unchanged). The 114 parts-file rows not on the website are DROP. On the website: 216 VERIFIED, 53 ASSUMED, 116 MISSING.
Plan fixes (orfs_modeltype_20261016/PLAN.md s8) in compare_orfs.py `HOLD` / `CAP` / `NOTES` and build_tables.py `thread_typos`
(`thread_slips.json`). Re-run all four scripts when the two-pass list appears.

Regenerate (read-only on all sources): `python -I scripts/compare_orfs.py; python -I scripts/forged_info.py; python -I scripts/build_tables.py;
python -I scripts/make_report.py` (`fetch_orfs.py pass1|pass2` only refetches missing raw files).

Not done here: the ORFS end type in the generators, masters, drawings; compression / test gauge have no dimension source.
