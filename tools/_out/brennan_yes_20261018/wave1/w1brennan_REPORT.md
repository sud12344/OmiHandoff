# Wave-1 Brennan-only rows: cell list against today's tables (2026-10-18)

Task: turn the 2026-10-02 wave-1 proposal files into one cell list after the user's decision of 2026-10-18 (Q-BRENNAN-ONLY = yes,
"yes use brennan but still differentiate the two in tables in case i need to change it later"). No review table was edited; the
main session applies `w1brennan_cells.csv`.

Files:
- `w1brennan_cells.csv`: 595 cells (`table,config,column,value,source,kind`). Kinds: brennan-dim 246, endlib 166, other 183. Of these,
  339 cells are for ready rows and 256 are for held rows. The held rows' cells can go in now and the rows stay MISSING.
- `w1brennan_rows.csv`: 78 rows (`ready`, missing columns, conflicts, and `GATE ...` notes).
- `w1brennan_test/`: test folder.
  - `scripts/collect.py` builds both CSVs. `scripts/test.py` applies them, regenerates and compares.
  - `root_untouched/`, `root/`, `root_B/` are the table copies. `gen_*/` holds the generator outputs.
  - `compare.txt`, `rows_result.json` and `checks_A/` hold the results. `collect_log.txt` is the collector log.

## Rows

84 WAVE1-BRENNAN-ONLY rows in `unblock_20261008/rows.csv`. 6 were excluded because OMi's drawings already filled them today
(1502-06-06 / -12-08 / -12-12 / -20-20 / -24-24 / -32-32-FG). None of the other 1405 / 1504 / 1602 / 6410 rows in
`omi_answers_20261018/CHANGES.csv` is in this set. That leaves **78 rows: 24 ready, 0 blocked, 54 held.**

| table | rows | ready | held | why held |
|---|---|---|---|---|
| 1502 | 1 | 1 (-16-16-FG) | 0 | |
| 2501LL | 5 | 5 | 0 | |
| 5601 | 4 | 3 (-02, -04, -20) | 1 (-24) | A9: the -24 tap drill (see Conflicts) |
| 5603 | 7 | 6 (-02 ... -20) | 1 (-24) | A9 |
| 5652 | 8 | 6 (-02 ... -20) | 2 | -24: A9. -32: no Brennan catalog row (table p.63 stops at -24), no OMi or Air-Way value. Needs `BRENNAN_5652-32-32-32-32-FG.stp`; A9 applies too |
| 5406 | 15 | 2 (HHP-08, SHP-08 = the pilot sizes) | 13 | HHP-01 ... -32: Q-PLUG-SOCKDEPTH (the socket depth is the pilot's ratio times the row's across-flats: a rule, not a source). HHP-01 also needs Q-NEW-NPT01 (no -01 NPTF entry in the end library). SHP-04 / -06 / -12 / -16: the square-head length is also a pilot-ratio rule, which I call Q-PLUG-SQHEAD here because OPEN_QUESTIONS lists no separate question for it. All of these rows have every table cell sourced |
| 6408 | 5 | 1 (HHP-08-O, pilot) | 4 | HEADDIA@REF has no source for -02 / -03 / -04 / -06: OMi Body Diameter is empty, the catalog has no head column, and there is no STEP. Q-PLUG-SOCKDEPTH applies too |
| 3474 | 7 | 0 | 7 | Every cell is sourced: catalog, own STEP for -12, and the 6801 adjustable-stud end library for the others. Held because the 3474 family toolchain (SPEC 3474 + NWO_3474_TRANSFER) is not in the batch-16 tools, and today's table is the 7-column skeleton |
| 1800 | 13 | 0 | 13 | Toolchain: FLANGE62 is not merged. -08-08 is fully sourced (catalog L and A/F, own STEP for collar / neck / bore). The other 12 have only L and A/F; collar dia, collar length, neck dia and bore need each part's own STEP, plus a measured code 62 head for -12 ... -32 |
| 1824 | 6 | 0 | 6 | Toolchain: FLANGE62 is not merged. -08 is fully sourced from its own STEP. -12 ... -32 have no source (the catalog gives the flange size only). Q-SOP5 probably applies, as on 1724 (to confirm) |
| 1724 | 7 | 0 | 7 | Toolchain: FLANGE61-PLUG is not merged. Q-SOP5. -08 is fully sourced from its own STEP. -12 ... -40 need STEPs, and -40 also needs a code 61 head |

Count of rows held only by a user decision with complete data: 16. These are 5406 x13 and the three -24 tee rows.

## Checks done on every proposed value

- **Catalog cells.** I re-read each value from `catalog_verified.json` myself, by table, row and column, and compared it with the
  2026-10-02 proposal value. All values agree. Every cited table is page-verified (`verified: true`).
- **STEP cells.** Each value is taken from its measuring evidence file:
  - 1800-08-08 and 1724-08 / 1824-08: FLANGE62 `flange62_straight.jsonl` and `flange62_plug.jsonl`. For 1724-08 / 1824-08 the hash
    also appears in FLANGE61-PLUG `measure_evidence.txt`.
  - 3474-12-12: `pilot_measurement.txt` (I3 1.1401, THDL 0.4101, root radius 0.4725 -> dia 0.945).
  - 6408-H08-O: PLUGS `plugs_measure_v3.jsonl` (head dia 0.875).

  The sha256 of each STEP was recomputed. For 1724-08, 1824-08 and 3474-12-12 it equals the hash written in the evidence. For
  1800-08-08 and 6408-H08-O it equals the hash in the 2026-10-02 PIPE-TEES live-file manifest. I did not re-run the measurement scripts.
- **End-library cells.** I recomputed these from the batch-16 generator libraries (gen_straight2 imported on the base root):
  - tap drills: FPT from the 2405 template;
  - pipe ODs: ms51500 NPTF;
  - JIC thread majors: the 2403 template;
  - ORB thread majors: the ORB dictionary, cross-checked against the catalog's printed ORB thread callout;
  - 3474 adjustable-stud end data: `DesignTable_6801.xlsx` rows 6801-dd-dd-NWO-FG in today's base.

  I classed the tap drills of these new masters as Q-TRANSFER-ENDLIB, because the 2026-10-08 decision names tap drills explicitly.
  The broader Q-TRANSFER-TAPDRILL (A1) is still open for existing families.
- **Base and OMi.** Every proposed dimension cell is empty in today's base. OMi's `WebsitePartsInfo2026` Items has no dimension for any
  of the 78 parts; it gives thread callouts only. None of the 78 has its own Air-Way row.
- **Marking (PROJECT_STATUS s5, 2026-10-18).**
  - Every row with a Brennan cell gets `$PRP@DimSource = BRENNAN`. This is a new column; the CSV source says "add it".
  - Ready rows also get:
    - `$PRP@AxialSource` replaced by `[BRENNAN-ONLY 2026-10-18] ` + the old text + a list of their sources;
    - `$PRP@DataStatus` set to ASSUMED;
    - a line added to `$COMMENT`.

  These three are the only non-empty cells the CSV overwrites (kind `other`).
- **Columns added.** 5406 needs `SOCKAF@SOCKET` / `SQAF@SQUARE`. 6408 needs `HEADDIA@REF` / `SOCKAF@SOCKET`. The skeleton tables need
  the family columns (1724, 1800, 1824, 3474). The column names match the family staged tables and the batch-16 SPECs.

## Test

I regenerated every SPEC root of the batch-16 gen_straight2 and gen_tee (`puckfix_20261009/tools_new`, `python -I`, one process per
root) on three table sets:
- **untouched:** a copy of the base;
- **A:** the CSV applied;
- **B:** A plus ASSUMED on the 16 rows that are held only by a decision. B is for information only and is not proposed.

- **Scenario A: all 24 ready rows become configurations, and none is blocked.**
  - 1502: +1 (7 -> 8).
  - 2501: +5 (48 -> 53). The 2501-LL rows fold in.
  - 5601: +3. 5603: +6. 5652: +6. Today these three have no configurations.
  - 5406HHP: +1. 5406SHP: +1. 6408HHP: +1. These are new SPECs that had 0 configurations.
- **Existing configurations are unchanged.**
  - Every other root regenerates identically: same macro apart from the date line, every SW2 cell the same, same return code.
    6408, 5406 and all other straights are included, even though they read the changed 6408 / 5406 tables when the module loads.
    1503 stops in both runs, which is a known problem.
  - In 1502 and 2501 no cell of any old configuration changed (`checks_A/regress.txt`).
  - Their macros differ only in the configuration-count check. 2501's macro also changes its spot-check row from 2501-L-16-16-FG to
    2501-LL-16-16-FG.
- **Static checks on scenario A** (`checks_A/`):
  - vbacheck: all OK;
  - dofcheck tee and straight: every sketch fully defined, 0 redundant;
  - allcfg_check: 0 outline problems in 1502, 2501, 5601, 5603, 5652, 5406HHP, 5406SHP, 6408HHP.
- **Generator warnings on new rows:** only rounding of the hex across-flats on 2501-LL-06-04 / -12-12 / -16-16
  (0.562 -> 0.5625, 1.062 -> 1.0625, 1.312 -> 1.3125, which is the existing 2603HX rule). The usual "male NPTF end slightly proud of or
  flush with the flats" note appears on 2501-LL-12-12 / -16-16.
- **Scenario B (if the decisions were answered as the rules now stand):**
  - The three -24 tee rows build.
  - 5406HHP builds 9 of 10. -01 is skipped because there is no -01 NPTF entry (Q-NEW-NPT01).
  - 5406SHP builds 4 of 5. **5406-SHP-16 blocks:** under the ratio rule, the thread length L2 0.6828 runs into the square-head shoulder
    at 0.6654. So the head-length rule does not fit -16.
- **Not done:** no SolidWorks dry run, no OCP closed loop.

## Conflicts

**No conflict between Brennan and any OMi or Air-Way value on these 78 rows.** Every target cell was empty, and none of these parts has
OMi dimensions or its own Air-Way row. Points for the user:

1. **A9: Q-CONFLICT-TAPDRILL-24 / -32.** It holds 5601-24, 5603-24, 5652-24 and 5652-32.
   - The end library (FPT, from the 2405 template) carries 1.72 for -24 and 2.20 for -32.
   - Air-Way also prints 1.70 for -24 and 2.19 for -32.
   - The CSV lists the library value, kind endlib. I did not mark these rows ready.
   - Related: today's OMi-answers staging put **2.19** in 1502-32-32-FG's TAPDRILL. That does not match the 2.20 the end library and
     generator carry. Please make the two consistent when A9 is answered.
2. **OMi's drawings vs the Brennan catalog on 1502 (information).** On the six 1502-FG parts OMi drew today, OMi's stem bore D is 0.01-0.02
   smaller than the catalog's A2 DRILL on four of them: 0.32 / 0.34, 0.44 / 0.46, 0.61 / 0.62, 1.01 / 1.03. The 1502-24 body hex is
   2.559 vs 2.562. Every length and the nut hex agree. So the catalog D of 0.78 proposed for 1502-16-16-FG may be slightly larger than a
   drawing would show.
3. **Air-Way plain twins (information, different parts).** These are the DROP rows without -FG; under the 2026-09-23 rule they are not
   used for -FG parts. The forged Brennan rows differ from them:
   - 1502-16-16: N3 1.62 vs 1.75, M1 1.73 vs 1.40, W3 2.08 vs 1.77, body hex 1.625 vs 1.50, D 0.78 vs 0.84.
   - 2501-LL -FG: the forged body hex is about 0.06 smaller at every size, and M differs by 0.10 at -04-04.
   - 5652 / 5603: the hex is smaller at -02, -12, -20 and -24, and the 5652-24 legs are 2.08 vs 2.14.

   Each pair is a different part, so nothing was picked.
4. **3474-12-12 thread length.** The adjustable thread length 0.410 comes from the part's own STEP. Air-Way prints 0.469 on 6801-12-12,
   which is another part. The open Q-CONFLICT-ORBTHDL-12 concerns the 6801 transfer, not this part.

## Unclear / for the main session

- **Q-SOP5 for 1824.** The FLANGE62 notes do not name Q-SOP5, but 1824 is a hexless code 62 flange plug like 1724. I listed the gate.
- **The square-head length on 5406-SHP.** OPEN_QUESTIONS_2026-10-18 lists only Q-PLUG-SOCKDEPTH. The square-head length rule is the same
  kind of question; I named it Q-PLUG-SQHEAD. Scenario B shows it fails at -16.
- **The 33 rows of 1724 / 1800 / 1824 / 3474 need their family toolchains merged before they can build.** Those toolchains are
  `newmasters_20261002/work/FLANGE61-PLUG`, `FLANGE62` and `3474`, which are not in batch 16. The cells can still go into the tables
  now: 10 of the 33 rows have complete data (1724-08, 1800-08-08, 1824-08 and the 7 3474 rows).
- **Pilots and the generator constants.** For the pilot sizes 5406-HHP-08, 5406-SHP-08 and 6408-HHP-08-O, the socket depth and head length
  come from the generator constant PLUG_PILOT, which was measured on each part's own STEP. That is exact for these sizes, so there is no
  table cell for them.
- **Scratch folders deleted.** I deleted two scratch folders I had created during this run inside `w1brennan_test` (`_libimport`, empty
  folders from the library import; `_checkscratch`, allcfg scratch). Re-running the scripts recreates them.
