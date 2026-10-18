# Brennan catalogs: extraction, OMi match, impact, final STEP list (2026-10-01)

Written 2026-10-01 23:43 by `tools/_out/brennan_catalog_20261001/steplist/build_catalog_md.py`. The STEP list itself: `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` (data: `tools/_out/brennan_catalog_20261001/steplist/steplist.json`).

**Read this first.**

- The catalog values are the **same source as OMi**. OMi's lengths are Brennan's data and OMi part numbers follow Brennan numbering, so OMi + Brennan catalog count as ONE source. A value from the catalog alone, or the catalog agreeing with OMi, stays **ASSUMED**.
- **Nothing was written into the review tables.** 04_DESIGN_TABLES, 03_SCRIPTS, 11_MASTERS and tools/generators were not touched. All results are files under `tools/_out/brennan_catalog_20261001/` and the two 00_DOCS files.
- The bucket moves in section 4 are proposals. They take effect only when the user accepts them and the tables are edited.

## 1. What was downloaded

The user gave the link https://brennaninc.com/catalogs/ and said "use any needed" (2026-10-01). Seven PDFs are in `07_RAW_EXTRACTS/brennan_catalogs/`. Four are used. The other three are not relevant to a carbon-steel JIC / NPT / ORB library.

| File | Pages | Size (bytes) | sha256 | Used | Content |
|---|---:|---:|---|---|---|
| TFA Catalog.pdf | 72 | 3,499,125 | `c4d050e070829c9597a850b96e40f37af5683c37ba6e6fd74959fe9e31ca61a0` | yes | Tube Fittings & Adapters: NPT, JIC, ORB. Straights p3-18, elbows p19-44, tees p45-59, crosses p60-61, caps / plugs / nuts p62-68, index p69-72 |
| Flange Catalog.pdf | 28 | 2,031,625 | `108614202a670da1f63c8e5f40c968c95793b0ee4ee6d8d9da3569a8afaf1dab` | yes | Code 61 / 62 flange fittings, flange heads, split flanges, kits |
| ORFS Catalog.pdf | 24 | 1,575,808 | `164ec18ffc2e413681320b1a0c22b5eb01c2792c8c26463d97854d2d7fbde41e` | yes | O-ring face seal (FS) fittings |
| Hosetail Catalog.pdf | 24 | 1,392,139 | `ac48d69097caa4f50c3d9df30517c7886930854ef74649b3598d805e40582652` | yes (no match) | Volz stainless hose tails and ferrules, D-numbers, no dimensions |
| Instrumentation Catalog.pdf | 40 | 2,387,667 | `8fb610303d1ae5a8ccecdff7597aa759bfaf7864d0afd8118cb6a4cc77a39cd4` | no | stainless / brass ferrule instrumentation fittings |
| DIN Catalog.pdf | 84 | 4,310,338 | `5c6fc5a0d51af9767df8b8cec52741cfe80e48303cdc0b7d572dc060eff66ee1` | no | DIN metric (Volz) fittings |
| Clamps Catalog.pdf | 52 | 2,784,994 | `ed760a3574ee3602175710af738419e9784096431d52a423a3e36b34b668752b` | no | tube clamps |

The parse recorded the same sha256 for the four used PDFs (`merge/merge_log.txt`).

## 2. How it was extracted and verified

1. **Parse.** `tools/catalog/parse_brennan_catalog.py` reads the PDF text layer with pymupdf. It finds each table heading (series + title), the header row (drawing letter + meaning, e.g. `L LGTH`), and the rows that start with a part number. A table without its own heading continues the one before it ("Continued..."). Values are kept exactly as printed: decimals, fractions, thread callouts, ranges like `.11/.13`. Output: `parsed/catalog_parsed.json`.
2. **Page check.** Every page of the four catalogs was rendered (full page at 200 dpi, table bands / zooms at 300 dpi and more) and compared with the text layer and the parse, in 19 chunks (`verify/*.json`). No chunk failed. **Unverified pages: none.**
3. **Corrections.** The page check found 5 problems, all on the Hosetail catalog. All 5 were confirmed and applied by `merge/apply_corrections.py` (3 table headings, 2 reference charts recorded as non-part tables). No cell value needed a correction.

| # | Page | What | Action |
|---|---|---|---|
| 0 | HOSETAIL p2 | reference chart without a part-number column (no part rows) | recorded as a reference table that is not a part table (0 part rows; no table added) |
| 1 | HOSETAIL p3 | reference chart without a part-number column (no part rows) | recorded as a reference table that is not a part table (0 part rows; no table added) |
| 2 | HOSETAIL p15 | heading parsed as 'Hose Joiner / Hose Joiner', printed 'Hose Joiner' | table title: 'Hose Joiner / Hose Joiner' -> 'Hose Joiner' |
| 3 | HOSETAIL p19 | heading parsed as 'Hose Tail-Code 62 Interlock-45', printed 'HINT CD62-45' | table series: 'Hose Tail-Code 62 Interlock-45' -> 'HINT CD62-45' |
| 4 | HOSETAIL p19 | heading parsed as 'Hose Tail-Code 62 Interlock-45 / HINT CD62-45', printed 'Hose Tail-Code 62 Interlock-45' | table title: 'Hose Tail-Code 62 Interlock-45 / HINT CD62-45' -> 'Hose Tail-Code 62 Interlock-45' |

| Catalog | Tables | Part rows | Pages with tables | Verified | Index entries (printed series index) |
|---|---:|---:|---|---|---:|
| TFA | 210 | 2,965 | 3-68 (64 pages) | all | 179 |
| FLANGE | 79 | 631 | 3-25 (21 pages) | all | 76 |
| ORFS | 63 | 666 | 3-21 (17 pages) | all | 55 |
| HOSETAIL | 75 | 794 | 4-20 (15 pages) | all | 0 |
| **Total** | **427** | **5,056** | | | |

- **Index:** `catalog_index.json` maps 5,033 normalised part numbers (upper case, no spaces) to 5,056 printed rows. 21 part numbers are printed more than once (23 extra entries), all Hosetail D-numbers: 18 in two tables, D114471 / D114472 in three tables (p20), D224136 twice in the same table (p15, two rows with different values).
- **Index cross-check:** every series in the printed index has a table, except TFA 0801 (printed under the heading "05010801" on p19, kept as printed) and Flange 1900-M (metric kit, no table). The printed index page numbers are offset by up to 2 pages from the PDF page (cover pages) - informational only.
- **Not parsed (by design):** Hosetail p2 thread chart and p3 ferrule matrix (no part-number column, no part rows).
- **Printed typos are kept as printed** (e.g. "05010801", L "23620", "136/16-16", "2.2252", ORFS "1/14" for 1-14). Catalog values that look wrong are listed in section 3.4; none was changed.

## 3. Match with the OMi dimension sheet

OMi = `07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx`, sheet Items (sha256 e5109342e141...). Part numbers were matched exactly (after upper-casing and removing spaces); documented variants are listed in each match report. Rule for comparing: **equal after rounding both to the fewer printed decimals = rounding only**; two prints of one exact n/64 fraction (0.812 / 0.813 = 13/16) also count as rounding. Every first-pass "real" difference was re-read on both sides (OMi cell re-read from the xlsx, catalog page re-read at 300 dpi) in a second pass (`match/*_diffcheck.json`).

### 3.1 Dimensions (TFA catalog - the only catalog where OMi has dimensions)

| Group | Catalog rows | Matched to OMi | Cells compared | Equal | Rounding only, first pass | Real, first pass | Real, confirmed | Moved to rounding by the re-check |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TFA straights p3-18 | 1,276 | 808 | 1,642 | 1,523 | 38 | 81 | 63 | 18 |
| TFA elbows p19-44 | 894 | 619 | 1,228 | 1,175 | 5 | 48 | 31 | 17 |
| TFA tees / crosses / caps / plugs / nuts p45-72 | 795 | 466 | 687 | 662 | 17 | 8 | 8 | 0 |
| **TFA total** | **2,965** | **1,893** | **3,557** | **3,360** | **60** | **137** | **102** | **35** |

- After the re-check: **3,557 cells = 3,360 equal + 95 rounding only + 102 real differences** (2.9 %). Straights include 6 cells where the OMi value lies inside a printed catalog range.
- The elbows row count includes the 17 rows of the 6900-O straight table continued on p19; the straights file lists them for information only and does not count them (1,276 + 894 + 795 = 2,965 catalog rows). OMi has no dimension on any 6900 row.
- Catalog rows with no OMi part: straights 468, elbows 275, tees etc. 329. Matched series where OMi has no dimension at all: the catalog is then the only Brennan-side value (1,314 + 951 + 1,863 catalog values; the elbows figure includes 24 on the 6900-O p19 rows).
- OMi 1.000 / 1.320 values (suspected placeholders): every one with a catalog counterpart is printed the same by Brennan (6410-10-08-O 1.320 vs catalog 1.315 is print precision), except **6420-08-08 OAL 1.320 (OMi Items!L1889) = a copy of 6420-08-06; the catalog prints 1.500**. Brennan also prints the impossible 1.000 on 6410-32-12-O / -32-16-O (section 3.4).
- **Warning on "one source":** on the elbows, OMi equals **Air-Way, not the catalog,** on 20 of the 29 confirmed differences that have an Air-Way value. On the 6500 / 6502 swivel noses OMi's M 1 is Air-Way's M10 / M14 almost row for row. For those columns OMi carries Air-Way numbers (TFA_elbows_diffcheck findings).

### 3.2 Other catalogs

| Catalog | Catalog rows | Matched to OMi | Dimension cells compared | Other cells compared | Confirmed differences |
|---|---:|---:|---:|---|---|
| ORFS | 666 | 370 | 0 (OMi has no dimension on any of its 531 FS parts) | threads: 763 compared, 732 equal | 32 (threads, see 3.3) |
| Flange | 631 | 180 | 0 (OMi has no dimension on any flange part) | identity (tube size, thread, flange size): 188 compared, 182 equal | 6 (identity, see 3.3) |
| Hosetail | 794 | 0 | 0 | - | - (Volz stainless, D-numbers, no dimensions printed: not usable) |

So for ORFS and flange parts the catalog is the **only** dimension source (ASSUMED). It cannot settle any OMi column question there.

### 3.3 Confirmed real differences (both values, cell addresses)

TFA dimensions. "Diff" = OMi minus catalog. Notes are shortened from the re-check files.

| # | Part | Catalog (page, column = value) | OMi (cell, column = value) | Diff | Note |
|---:|---|---|---|---:|---|
| 1 | 0403-12-12 | p3 B BORE = 0.756 | Items!S58 Side 1 ID = 0.757 | +0.001 | 0.001 in the 3rd decimal, no padding involved. |
| 2 | 0403-20-20 | p3 B BORE = 1.256 | Items!S60 Side 1 ID = 1.257 | +0.001 | 0.001 in the 3rd decimal. Catalog prints 1.257 for the 1-1/4 bore on 0403-20-16 and 1.256 here; OMi 1.257. |
| 3 | 0403-24-24 | p3 B BORE = 1.507 | Items!S61 Side 1 ID = 1.506 | -0.001 | 0.001 in the 3rd decimal. Catalog prints 1.506 on 0403-24-20 and 1.507 here; OMi 1.506. |
| 4 | 1404-04-02 | p4 L LGTH = 1.320 | Items!L90 Overall Length = 1.33 | +0.010 | 0.010: catalog 1.320 = 1.32 at 2 dp vs OMi 1.33 (OMi 1404 lengths are all 2 dp). Not rounding. |
| 5 | 1404-04-04 | p4 A2 DRILL = 0.220 | Items!X91 Side 2 ID = 0.21 | -0.010 | 0.010. Catalog prints a single 0.220 here; for the same -04 NPSM drill it prints the range '0.21/0.23' on 1404-02-04 and 1405-06-04. |
| 6 | 1404-06-04 | p4 A2 DRILL = 0.220 | Items!X94 Side 2 ID = 0.21 | -0.010 | 0.010. Same as idx 4: catalog 0.220 inside its own '0.21/0.23' range for -04 NPSM; OMi = low end 0.21. |
| 7 | 1404-06-06 | p4 A2 DRILL = 0.340 | Items!X95 Side 2 ID = 0.32 | -0.020 | 0.020. Catalog 0.340 = high end of its own '0.32/0.34' (1405-04-06) / '0.320/0.340' (1404-16-06) range for -06 NPSM; OMi = low end 0.32. |
| 8 | 1404-06-08 | p4 A2 DRILL = 0.460 | Items!X96 Side 2 ID = 0.44 | -0.020 | 0.020. Catalog 0.460; its own -08 NPSM range is '0.44/0.48' (1404-12-08) and it prints 0.440 on 1404-04-08; OMi = 0.44 on every -08 NPSM row. |
| 9 | 1404-08-06 | p4 A2 DRILL = 0.340 | Items!X97 Side 2 ID = 0.32 | -0.020 | 0.020. As idx 6 (-06 NPSM: catalog 0.340, OMi low end 0.32). |
| 10 | 1404-08-08 | p4 A2 DRILL = 0.460 | Items!X98 Side 2 ID = 0.44 | -0.020 | 0.020. As idx 7 (-08 NPSM: catalog 0.460, OMi 0.44). |
| 11 | 1404-08-12 | p4 A2 DRILL = 0.620 | Items!X99 Side 2 ID = 0.61 | -0.010 | 0.010. Catalog 0.620; its own -12 NPSM range is '.61/.63' (1405-16-12) and it prints 0.610 on 1404-16-12; OMi = 0.61. |
| 12 | 1404-12-12 | p4 A1 DRILL = 0.63 | Items!S101 Side 1 ID = 0.610 | -0.020 | 0.020. Catalog prints 0.63 for BOTH drills on 1404-12-12 (every other 1404-12-xx row: A1 = 0.719); OMi 0.610 (also off its own 0.719 on ... |
| 13 | 1404-12-12 | p4 A2 DRILL = 0.63 | Items!X101 Side 2 ID = 0.61 | -0.020 | 0.020. Catalog 0.63 = high end of its '.61/.63' -12 NPSM range; OMi 0.61 = low end. |
| 14 | 1404-12-12 | p4 L LGTH = 2.08 | Items!L101 Overall Length = 2.10 | +0.020 | 0.020: catalog 2.08 vs OMi 2.10 (both 2 dp). |
| 15 | 2404-08-06 | p6 A2 DRILL = 0.391 | Items!X494 Side 2 ID = 0.406 | +0.015 | 0.015. Catalog prints 0.391 (= the row's B1 JIC drill) as A2 drill; on the other 2404-xx-06 rows (02-06, 04-06, 05-06, 10-06, 12-06, 16-06) it prints ... |
| 16 | 2404-20-12 | p6 C HEX = 1.625 | Items!R516 Hex Flat = 1.688 | +0.063 | 0.063. Catalog 1.625 (= the 1-5/8 JIC thread major diameter) vs 1.688 printed on every other 2404-20-xx row; OMi 1.688. |
| 17 | 2705-12-14 | p8 L LGTH = 2.99 | Items!L1051 Overall Length = 2.920 | -0.070 | 0.070. Catalog 2.99 repeats the row above (2705-12-12 = 2.99) - the copy-down suspicion here points at the catalog, not OMi; OMi 2.920. |
| 18 | 2705-12-14 | p8 C1 HEX = 1.500 | Items!R1051 Hex Flat = 1.375 | -0.125 | 0.125. OMi 1.375 repeats the row above (2705-12-12); catalog 1.500. Same on Items!R1065. |
| 19 | 2705-20-20 | p8 L LGTH = 3.38 | Items!L1053 Overall Length = 3.310 | -0.070 | 0.070: catalog 3.38 vs OMi 3.310 (= 3.31). Same on Items!L1067. |
| 20 | 2706-08-06 | p9 B2 DRILL = 0.297 | Items!X1076 Side 2 ID = 0.295 | -0.002 | 0.002. Catalog 0.297 is the 3-dp print of 19/64 (0.296875); OMi 0.295 is not a print of it. Same on Items!X1091. |
| 21 | 2706-08-06 | p9 L LGTH = 2.410 | Items!L1076 Overall Length = 2.400 | -0.010 | 0.010: catalog 2.410 = 2.41 vs OMi 2.400 = 2.40 at 2 dp. Same on Items!L1091. |
| 22 | 6400-10-08-O | p14 B1 DRILL = 0.391 | Items!S1652 Side 1 ID = 0.484 | +0.093 | 0.093. Catalog prints 0.391 for both B1 and B2 drills on 6400-10-08-O (the -08 ORB through drill); OMi Side 1 = 0.484 (the -10 JIC drill the catalog ... |
| 23 | 6401-04-04-O | p14 B DRILL = 0.172 | Items!S1701 Side 1 ID = 0.173 | +0.001 | 0.001. Catalog 0.172 = 11/64 (0.171875) print; OMi 0.173 is not a print of 11/64 (OMi's own 6401-04-02-O has 0.172). |
| 24 | 6401-04-04-O | p14 L LGTH = 1.230 | Items!L1701 Overall Length = 1.250 | +0.020 | 0.020: catalog 1.230 vs OMi 1.250 (1.23 vs 1.25 at 2 dp). |
| 25 | 6401-12-12-O | p15 L LGTH = 1.86 | Items!L1714 Overall Length = 1.730 | -0.130 | 0.130: catalog 1.86 vs OMi 1.730. |
| 26 | 6402-04-04-O | p15 L LGTH = 0.96 | Items!P1724 L 1 Size = 0.970 | +0.010 | 0.010: catalog 0.96 vs OMi 0.970 (= 0.97). |
| 27 | 6402-06-04-O | p15 L LGTH = 1.060 | Items!P1726 L 1 Size = 1.070 | +0.010 | 0.010: catalog 1.060 vs OMi 1.070 (1.06 vs 1.07 at 2 dp). |
| 28 | 6404-20-16 | p15 L LGTH = 2.16 | Items!L1757 Overall Length = 2.310 | +0.150 | 0.150: catalog 2.16 vs OMi 2.310. |
| 29 | 6405-24-12-O | p16 B DRILL = 0.854 | Items!S1801 Side 1 ID = 0.907 | +0.053 | 0.053. Catalog 0.854 (same as its 6405-20-12-O, -12 NPTF through drill); OMi 0.907. |
| 30 | 6405-24-16-O | p16 B DRILL = 1.312 | Items!S1802 Side 1 ID = 1.080 | -0.232 | 0.232. Catalog 1.312 (the -24 ORB drill); OMi 1.080. |
| 31 | 6405-32-16-O | p16 B DRILL = 1.156 | Items!S1805 Side 1 ID = 1.080 | -0.076 | 0.076. Catalog 1.156; OMi 1.080 (same OMi value as 6405-24-16-O). |
| 32 | 6410-08-04-O | p16 B DRILL = 0.391 | Items!S1844 Side 1 ID = 0.386 | -0.005 | 0.005. Catalog 0.391 (the -08 ORB drill, printed on every 6410-08-xx-O row); OMi 0.386. |
| 33 | 6410-10-06-O | p16 B DRILL = 0.502 | Items!S1850 Side 1 ID = 0.508 | +0.006 | 0.006. Catalog 0.502; OMi 0.508 (both sources print 0.508 for 6410-16-06-O). |
| 34 | 6410-12-10-O | p16 L LGTH = 1.57 | Items!L1857 Overall Length = 1.480 | -0.090 | 0.090. OMi 1.480 repeats the row above (6410-12-08-O, where catalog also prints 1.48): suspected OMi copy-down; catalog 1.57. |
| 35 | 6410-16-04-O | p16 B DRILL = 0.389 | Items!S1862 Side 1 ID = 0.368 | -0.021 | 0.021. Catalog 0.389 (same as its 6410-12-04-O / 20-04-O); OMi 0.368. |
| 36 | 6410-24-24-O | p16 B DRILL = 1.312 | Items!S1878 Side 1 ID = 1.311 | -0.001 | 0.001. 1.312 is the truncated print of 1-5/16 (1.3125); OMi 1.311 is not a print of it (OMi's own 6410-24-20-O has 1.312). |
| 37 | 6420-08-08 | p17 L LGTH = 1.500 | Items!L1889 Overall Length = 1.320 | -0.180 | 0.180. Catalog 1.500; OMi 1.320 repeats the row above (6420-08-06, catalog 1.320 there): suspected OMi copy-down/placeholder. |
| 38 | 6420-12-12 | p17 C4 HEX = 1.375 | Items!R1891 Hex Flat = 1.374 | -0.001 | 0.001. Catalog 1.375 = 1-3/8 exact; OMi 1.374 is not a print of it. |
| 39 | 6504-10-10 | p17 L5 LGTH = 2.07 | Items!L1995 Overall Length = 2.170 | +0.100 | 0.100. Catalog 2.07 (same as its 6504-08-10 2.070); OMi 2.170. |
| 40 | 6504-16-12 | p17 L5 LGTH = 2.450 | Items!L2001 Overall Length = 2.430 | -0.020 | 0.020. Catalog 2.450 (same as its 6504-12-16); OMi 2.430. |
| 41 | 6504-16-12 | p17 C1 HEX = 1.500 | Items!V2001 Nut Hex 1 = 1.250 | -0.250 | 0.250. Catalog 1.500 repeats 6504-12-16 (whose B2 is the -16 swivel); this row's B2 is 1-1/16-12 (-12 swivel) whose nut the catalog prints 1.250 on ... |
| 42 | 6504-32-32 | p17 L5 LGTH = 2.862 | Items!L2007 Overall Length = 3.800 | +0.938 | OMi 3.800 differs from both catalog lengths of the row (L5 2.862 by 0.938, L 3.700 by 0.100); the catalog row is itself inconsistent (L > L5), so no ... |
| 43 | 6505-02-02 | p18 L5 LGTH = 1.300 | Items!L2008 Overall Length = 1.29 | -0.010 | 0.010: catalog 1.300 = 1.30 vs OMi 1.29. |
| 44 | 6505-02-04 | p18 L5 LGTH = 1.350 | Items!L2009 Overall Length = 1.36 | +0.010 | 0.010: catalog 1.350 = 1.35 vs OMi 1.36. |
| 45 | 6505-04-04 | p18 L LGTH = 1.20 | Items!P2011 L 1 Size = 1.21 | +0.010 | 0.010: catalog 1.20 vs OMi 1.21. |
| 46 | 6505-04-04 | p18 L5 LGTH = 1.54 | Items!L2011 Overall Length = 1.56 | +0.020 | 0.020: catalog 1.54 vs OMi 1.56. |
| 47 | 6505-12-08 | p18 A DRILL = 0.609 | Items!S2021 Side 1 ID = 0.719 | +0.110 | 0.110. Catalog 0.609 departs from its own 0.719 for the -12 NPTF A drill on 6505-12-10/12-12/12-16; OMi 0.719 (consistent with those). |
| 48 | 6505-12-16 | p18 B DRILL = 0.844 | Items!X2024 Side 2 ID = 0.719 | -0.125 | 0.125. Catalog 0.844 (the -16 JIC drill, as on 6505-16-16); OMi 0.719 (= this row's -12 NPTF A drill). |
| 49 | 6505-12-16 | p18 L LGTH = 1.77 | Items!P2024 L 1 Size = 1.79 | +0.020 | 0.020: catalog 1.77 vs OMi 1.79. |
| 50 | 6505-20-20 | p18 L5 LGTH = 2.85 | Items!L2028 Overall Length = 2.84 | -0.010 | 0.010: catalog 2.85 vs OMi 2.84. |
| 51 | 6505-24-24 | p18 L5 LGTH = 2.99 | Items!L2029 Overall Length = 3.00 | +0.010 | 0.010: catalog 2.99 vs OMi 3.00. |
| 52 | 6506-02-02 | p18 L5 LGTH = 1.232 | Items!L2031 Overall Length = 1.250 | +0.018 | 0.018: catalog 1.232 = 1.23 at 2 dp vs OMi 1.250 = 1.25. |
| 53 | 6506-12-12 | p18 L5 LGTH = 2.29 | Items!L2044 Overall Length = 2.280 | -0.010 | 0.010: catalog 2.29 vs OMi 2.280 (= 2.28). |
| 54 | 6506-12-14 | p18 L5 LGTH = 2.33 | Items!L2045 Overall Length = 2.340 | +0.010 | 0.010: catalog 2.33 vs OMi 2.340 (= 2.34). |
| 55 | 6506-24-24 | p18 L5 LGTH = 2.990 | Items!L2049 Overall Length = 3.000 | +0.010 | 0.010: catalog 2.990 = 2.99 vs OMi 3.000 = 3.00. |
| 56 | 6506-32-32 | p18 L5 LGTH = 3.12 | Items!L2050 Overall Length = 3.200 | +0.080 | 0.080: catalog 3.12 vs OMi 3.200. |
| 57 | 6565-04-04 | p18 L1 LGTH = 0.65 | Items!P2052 L 1 Size = 0.700 | +0.050 | 0.050: catalog 0.65 vs OMi 0.700. |
| 58 | 6565-04-04 | p18 L5 LGTH = 1.33 | Items!L2052 Overall Length = 1.390 | +0.060 | 0.060: catalog 1.33 vs OMi 1.390. |
| 59 | 6565-08-06 | p18 L5 LGTH = 1.600 | Items!L2055 Overall Length = 1.630 | +0.030 | 0.030: catalog 1.600 vs OMi 1.630. |
| 60 | 6565-08-08 | p18 L5 LGTH = 1.80 | Items!L2056 Overall Length = 1.740 | -0.060 | 0.060: catalog 1.80 vs OMi 1.740. |
| 61 | 6565-10-10 | p18 L5 LGTH = 2.00 | Items!L2057 Overall Length = 1.970 | -0.030 | 0.030: catalog 2.00 vs OMi 1.970. |
| 62 | 6565-12-12 | p18 L5 LGTH = 2.21 | Items!L2058 Overall Length = 2.160 | -0.050 | 0.050: catalog 2.21 vs OMi 2.160. |
| 63 | 6565-20-20 | p18 L5 LGTH = 2.56 | Items!L2060 Overall Length = 2.590 | +0.030 | 0.030: catalog 2.56 vs OMi 2.590. |
| 64 | 2501-24-32-FG | p23 A2 DRILL = 1.938 | Items!X699 Side 2 ID = 1.940 | +0.002 | Both read correctly (OMi X699 text '1.940'; catalog p23 prints 1.938 = 1-15/16). |
| 65 | 2501-L-24-24-FG | p24 L LGTH = 4.10 | Items!P715 L 1 Size = 4.110 | +0.010 | Both read correctly (OMi P715 '4.110' = 4.11, OMi's 2501-L leg column is 2-decimal data padded with a zero, 13/13; catalog p24 prints 4.10). 0.01 at ... |
| 66 | 5502-04-02-FG | p31 N1 LGTH = 0.660 | Items!P1461 L 1 Size = 0.670 | +0.010 | Both read correctly (OMi P1461 '0.670'; catalog p31 prints 0.660). 0.01 at 2 decimals. |
| 67 | 6500-12-16-FG | p34 M LGTH = 1.81 | Items!P1927 L 1 Size = 1.76 | -0.050 | Both read correctly (OMi P1927 '1.76'; catalog p34 6500-12-16-FG M LGTH 1.81). |
| 68 | 6500-04-04-FG | p34 M4 LGTH = 0.65 | Items!N1912 M 1 Size = 0.66 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). 0.01 at 2 decimals is not rounding. |
| 69 | 6500-04-06-FG | p34 M4 LGTH = 0.87 | Items!N1913 M 1 Size = 0.88 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 70 | 6500-06-06-FG | p34 M4 LGTH = 0.87 | Items!N1916 M 1 Size = 0.88 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 71 | 6500-06-08-FG | p34 M4 LGTH = 0.950 | Items!N1917 M 1 Size = 0.96 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 72 | 6500-08-08-FG | p34 M4 LGTH = 0.95 | Items!N1919 M 1 Size = 0.96 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). 0.01 at 2 decimals is not rounding. |
| 73 | 6500-08-12-FG | p34 M4 LGTH = 1.180 | Items!N1921 M 1 Size = 1.19 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 74 | 6500-12-08-FG | p34 M4 LGTH = 1.120 | Items!N1925 M 1 Size = 1.13 | +0.010 | Both read correctly (OMi N1925 '1.13'; catalog 1.120). 0.01 at 2 decimals. Pairing right. Air-Way's plain 6500-12-08 M10 = 1.11: neither. |
| 75 | 6500-12-16-FG | p34 M4 LGTH = 1.40 | Items!N1927 M 1 Size = 1.41 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 76 | 6500-16-12-FG | p34 M4 LGTH = 1.34 | Items!N1928 M 1 Size = 1.39 | +0.050 | Both read correctly (OMi N1928 '1.39'; catalog p34 6500-16-12-FG M4 1.34). |
| 77 | 6500-16-16-FG | p34 M4 LGTH = 1.40 | Items!N1929 M 1 Size = 1.41 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). 0.01 at 2 decimals is not rounding. |
| 78 | 6500-20-20-FG | p34 M4 LGTH = 1.670 | Items!N1931 M 1 Size = 1.69 | +0.020 | Both read correctly; pairing right (M4 = swivel nose). |
| 79 | 6500-24-24-FG | p34 M4 LGTH = 1.870 | Items!N1933 M 1 Size = 1.86 | -0.010 | Both read correctly (OMi N1933 '1.86'; catalog 1.870). -0.01 at 2 decimals: real. |
| 80 | 6500-32-32-FG | p34 M4 LGTH = 2.43 | Items!N1935 M 1 Size = 2.44 | +0.010 | Both read correctly; pairing right (M4 = swivel nose). |
| 81 | 6500-16-12-FG | p34 M6 LGTH = 1.91 | Items!O1928 M 2 Size = 1.95 | +0.040 | Both read correctly (OMi O1928 '1.95'; catalog p34 6500-16-12-FG M6 1.91). |
| 82 | 6501-06-06-FG | p35 M4 LGTH = 0.90 | Items!N1944 M 1 Size = 0.910 | +0.010 | Both read correctly (OMi N1944 '0.910' = 0.91 padded; catalog 0.90). 0.01 at 2 decimals: real. Air-Way 6501-6-6 M10 0.97: neither. |
| 83 | 6501-12-12-FG | p35 M4 LGTH = 1.180 | Items!N1950 M 1 Size = 1.190 | +0.010 | Both read correctly (OMi N1950 '1.190' = 1.19; catalog 1.180). 0.01 at 2 decimals: real. OMi equals Air-Way 6501-12-12 M10 1.19. |
| 84 | 6501-12-08-FG | p35 M6 LGTH = 1.612 | Items!O1949 M 2 Size = 1.540 | -0.072 | Both read correctly (OMi O1949 '1.540'; catalog p35 6501-12-08-FG M6 1.612). |
| 85 | 6502-04-04-FG | p35 M LGTH = 0.59 | Items!N1958 M 1 Size = 0.600 | +0.010 | Both read correctly (OMi 3-decimal text in a column that is 2-decimal data padded with a zero, 14/14); pairing right (6502 M = nose along the 45 deg ... |
| 86 | 6502-05-05-FG | p35 M LGTH = 0.620 | Items!N1959 M 1 Size = 0.630 | +0.010 | Both read correctly (OMi 3-decimal text in a column that is 2-decimal data padded with a zero, 14/14); pairing right (6502 M = nose along the 45 deg ... |
| 87 | 6502-08-08-FG | p35 M LGTH = 0.85 | Items!N1963 M 1 Size = 0.860 | +0.010 | Both read correctly (OMi 3-decimal text in a column that is 2-decimal data padded with a zero, 14/14); pairing right (6502 M = nose along the 45 deg ... |
| 88 | 6502-16-16-FG | p35 M LGTH = 1.15 | Items!N1970 M 1 Size = 1.160 | +0.010 | Both read correctly (OMi 3-decimal text in a column that is 2-decimal data padded with a zero, 14/14); pairing right (6502 M = nose along the 45 deg ... |
| 89 | 6502-24-24-FG | p35 M LGTH = 1.53 | Items!N1973 M 1 Size = 1.520 | -0.010 | Both read correctly (OMi N1973 '1.520' = 1.52; catalog 1.53). -0.01 at 2 decimals: real. OMi equals Air-Way 6502-24-24-FG M14 1.52. |
| 90 | 6502-32-32-FG | p35 M LGTH = 1.960 | Items!N1974 M 1 Size = 1.970 | +0.010 | Both read correctly (OMi 3-decimal text in a column that is 2-decimal data padded with a zero, 14/14); pairing right (6502 M = nose along the 45 deg ... |
| 91 | 6503-06-06-FG | p38 M4 LGTH = 1.040 | Items!N1977 M 1 Size = 1.005 | -0.035 | Both read correctly (OMi N1977 '1.005'; catalog p38 1.040). -0.035: real. |
| 92 | 6503-08-10-FG | p38 M4 LGTH = 1.16 | Items!N1979 M 1 Size = 1.130 | -0.030 | Both read correctly (OMi 1.130 / 1.630 on 6503-08-10-FG; catalog p38 M4 1.16 / M6 1.66). |
| 93 | 6503-04-06-FG | p38 M6 LGTH = 1.29 | Items!O1976 M 2 Size = 1.283 | -0.007 | Both read correctly (OMi O1976 '1.283'; catalog p38 M6 1.29). 1.283 half-up = 1.28 and cut = 1.28, neither is 1.29: -0.007, real (small). |
| 94 | 6503-08-10-FG | p38 M6 LGTH = 1.66 | Items!O1979 M 2 Size = 1.630 | -0.030 | Both read correctly (OMi 1.130 / 1.630 on 6503-08-10-FG; catalog p38 M4 1.16 / M6 1.66). |
| 95 | 2605-12-12-12-FG | p50 A2 DRILL = 0.609 | Items!X841 Side 2 ID = 0.719 | +0.110 | Both read correctly, not rounding (0.609 vs 0.719 = 0.110). |
| 96 | 2607-12-12-12-FG | p51 A2 DRILL = 0.719 | Items!X860 Side 2 ID = 0.609 | -0.110 | Both read correctly, not rounding (0.110). |
| 97 | 2608-16-16-16-FG | p51 L LGTH = 1.70 | Items!P870 L 1 Size = 1.970 | +0.270 | Both read correctly, not rounding (0.27). |
| 98 | 2608-12-12-12-FG | p51 Y FLATS = 1.312 | Items!R869 Hex Flat = 1.311 | -0.001 | Both read correctly. Real only under the strict rule: both print 3 places and 1.311 is not a rendering of 1-5/16 (1.3125 gives 1.312 or 1.313), so ... |
| 99 | 2610-06-06-06-FG | p52 L1 LGTH = 1.22 | Items!O878 M 2 Size = 1.200 | -0.020 | Both read correctly, not rounding (1.22 vs 1.20 at 2 places). |
| 100 | 0304-C-32 | p65 C HEX = 2.880 | Items!R16 Hex Flat = 2.875 | -0.005 | Both read correctly. Real only under the strict rule (both print 3 places; 2.880 is not a 3-place rendering of 2-7/8 = 2.875); difference 0.005. |
| 101 | 6408-H12-O (OMi 6408-HHP-12-O) | p67 L LGTH = 0.77 | Items!L1830 Overall Length = 0.780 | +0.010 | Both read correctly, not rounding (0.77 vs 0.78 at 2 places, 0.01). |
| 102 | 6408-H16-O (OMi 6408-HHP-16-O) | p67 L LGTH = 0.775 | Items!L1832 Overall Length = 0.780 | +0.005 | Both read correctly. Real only under the strict rule (both print 3 places; 0.005). |

102 confirmed TFA differences; 30 of them exceed 0.03 in (5 more are exactly 0.030). None is changed here. Where both print a value, the standing rule keeps OMi and notes the catalog value in `$COMMENT`. The impact groups raised the ones that touch a MISSING row as questions (Q-NEW-F1B-CATDIFF, Q-NEW-F2A-OMIvsCAT, the Q-CAT-* questions; section 4.2).

ORFS threads (not dimensions) - 32 confirmed:

| Kind | n | Cells |
|---|---:|---|
| OMi 1-7/8-12 UN on a -24 face-seal end, catalog 2-12 | 26 | FS6400-24-20-O (Items!U5549 '1-7/8-12 UN' vs p5 A THREAD '2-12'); FS6400-24-24-O (Items!U5550 '1-7/8-12 UN' vs p5 A THREAD '2-12'); FS2500-24-20-FG (Items!U5360 '1-7/8-12 UN' vs p7 A1 THREAD '2-12'); FS2500-24-24-FG (Items!U5361 '1-7/8-12 UN' vs p7 A1 THREAD '2-12'); FS2500-24-24-FG (Items!AA5361 '1-7/8-12 UN' vs p7 A2 THREAD '2-12'); FS2501-24-24-FG (Items!U5376 '1-7/8-12 UN' vs p8 A THREAD '2-12'); ... (20 more in match/ORFS_diffcheck.json) |
| catalog typo 1/14 (OMi right) | 3 | FS6502-10-10-FG (Items!AA5588 '1-14 UNS' vs p9 B THREAD '1/14'); FS6600-10-10-10-FG (Items!AA5627 '1-14 UNS' vs p16 A2 THREAD '1/14'); FS6602-10-10-10-FG (Items!AE5634 '1-14 UNS' vs p17 A2 THREAD '1/14') |
| OMi thread contradicts its own part number | 2 | FS2503-08-06-FG (Items!AA5383 '1/2- 14 NPTF' vs p8 B THREAD '3/8-18'); FS6801-12-08-NWO-FG (Items!AA5654 '3/8-24 UNF' vs p10 B THREAD '3/4-16') |
| end-type conflict (same part number, different part) | 1 | FS6503-06-06-FG (Items!U5594 '11/16-16 UNF' vs p9 A THREAD '3/8-18') |

Flange identity check (not dimensions) - 6 confirmed:

| Part | Catalog | OMi | Note |
|---|---|---|---|
| 1700-32-32 | p3 2 FLANGE = 2 | Items!Z226 S2Size (Z) = 2 1/2 | Both read correctly. Pairing right: catalog '2 FLANGE' = flange end; OMi Side 1 = Male JIC (T = tube 2), Side 2 = the flange. |
| 1700-40-40 | p3 2 FLANGE = 2 1/2 | Items!Z227 S2Size (Z) = 2.0 | Both read correctly, pairing right (as idx 0). |
| FS1700-24-24 | p4 1 THREAD = 2-12 | Items!U5245 S1Thread (U) = 1-7/8-12 UN | Pairing right: catalog column '1 THREAD' is end 1 = the MFS (O-ring face seal) end - the drawing labels '1' at the O-ring threaded end, and ... |
| FS1800-24-24 | p4 1 THREAD = 2-12 | Items!U5253 S1Thread (U) = 1-7/8-12 UN | Pairing right: catalog column '1 THREAD' is end 1 = the MFS (O-ring face seal) end - the drawing labels '1' at the O-ring threaded end, and ... |
| FS1704-24-24-FG | p6 1 THREAD = 2-12 | Items!U5249 S1Thread (U) = 1-7/8-12 UN | Pairing right: catalog column '1 THREAD' is end 1 = the MFS (O-ring face seal) end - the drawing labels '1' at the O-ring threaded end, and ... |
| FS1804-24-24-FG | p7 1 THREAD = 2-12 | Items!U5257 S1Thread (U) = 1-7/8-12 UN | Pairing right: catalog column '1 THREAD' is end 1 = the MFS (O-ring face seal) end - the drawing labels '1' at the O-ring threaded end, and ... |

### 3.4 Catalog values that look wrong (kept as printed)

- [F1a] NPSM swivel -12: the catalog's nut-face-to-stem-tip offset is 0.35 (1501-12-12-FG 1.65 - 1.30; 1601-12-12-12-FG; 1602-12-12-12-FG 1.82 - 1.47; 1603-12-12-12-FG 1.65 - 1.30) while the in-repo Brennan 1404-12-12 STEP gives TIP_B 0.33 (NPSM_MEAS[12]); every ...
- [F1a] 1603-FG heading on TFA p48 prints "FP-FPS-FPS TEE" but all three thread columns are NPSM (A1/A2/A3 NPSM = FPS-FPS-FPS) - kept as printed.
- [F1a] 1603-08-08-08-FG prints all three drills as a range "0.44/0.46" - no single bore value (its pilot STEP gives it).
- [F1a] 1603-16-12-16-FG prints C1 HEX 1.25 (the -12 A2 nut) although the drawing puts "C 1HEX" on the A3 (-16) nut; on the F1a same-dash rows C HEX = C1 HEX, so no F1a value depends on it.
- [F1a] 1601-FG reducer rows print C HEX at an end size that is not the NPSM nut (06-04-04: 0.875, 08-06-06: 1.000, 12-08-08: 1.250, 04-06-06: 0.688); on every same-dash F1a row C HEX equals the NPSM nut of NPSM_MEAS - the pairing C HEX = nut hex is only claimed for ...
- [F1a] 2606-FG header prints "BE SAE 37Deg" for the third (branch JIC) thread column - read as B3 (the drawing labels the branch end B3).
- [F1a] 1703-24-24-FG (Flange p4) prints A/F as the fraction "1 7/8" (= 1.875) where the other rows print decimals.
- [F1b] 6809-12-12-NWO-FG (TFA p44) M LGTH 1.370: nose depth M6 - M = 1.75 - 1.37 = 0.38, while the -12 swivel nose depth is 0.57 everywhere else (6500-12-12 / 6501-12-12 catalog, Brennan STEP NOSETIP_B 0.57); Air-Way plain 6809-12-12 M10 1.19 - probable catalog ...
- [F1b] 6809-16-16-NWO-FG (TFA p44) M LGTH 1.45: nose depth 2.00 - 1.45 = 0.55 vs 0.60 measured on the Brennan -16 swivel (6500-16-16 catalog M4 1.40) - doubtful
- [F1b] 6503-06-06-FG (TFA p38) M4 LGTH 1.040: nose depth 1.380 - 1.040 = 0.34 vs 0.375 on every other -06 swivel the catalog prints with 3 decimals; OMi 1.005 gives 0.375 (already in TFA_elbows_diffcheck idx 42)
- [F1b] 5652-24-24-24-24-FG (TFA p63) Y FLATS printed 2.561; 2-9/16 prints 2.562 elsewhere (5604-24-24-24-FG, 5605-24-24-24-FG) - probable typo, kept as printed
- [F1b] 6603-04-04-04-FG (TFA p58, not an F1b row) M2 LGTH printed 1.0029 - typo (1.00); header typos kept as printed: 5602 'N1 LGBTH', 5652 'AD NPTF' (= A3)
- [F1b] 6500-FG drawing p34 labels the nut-face length M5 while the header prints M6 (already in the match file)
- [F2a] 0304-C-32 C HEX 2.880 (other -32 nut hexes print 2.875) - likely 2.88 padded
- [F2a] 1700-32-24 A/F 2.622 (1700-32-32 2.625; not a print of a 64th) - possible misprint
- [F2a] 2606-FG header prints 'BE SAE 37Deg' for the side-3 JIC thread (B3)
- [F2a] 0304-C-48 row printed blank
- [F2a] 1405-04-06 A2 DRILL printed as a range .32/.34 (several 1405 rows print ranges)
- [F2a] 1405-08-12 L - L1 = 0.35 vs Brennan-measured -12 NPSM nut-face-to-stem-tip 0.33; 1405-04-06 0.21 vs 0.22 (-06)
- [F2b] TFA p12 5404-N-06X3.500 / -06X7.000 / -12X8.000 (rows appended after 5404-N-24X6.000): the A1/A2 DRILL cells print the length in inch and mm (3.500 / 88.90, 7.000 / 165.10, 8.000 / 190.50) - no drill printed; the parse keeps them as printed ...
- [F2b] 5406-C pipe caps: Brennan caps (TFA p66-67) are 0.11-0.36 shorter than the Air-Way caps of the same size already built in 5406C (-02 0.563 vs 0.69 ... -16 1.250 vs 1.61) and 3 hexes differ (-06 0.812 vs 0.88, -08 1.000 vs 1.13, -12 1.188 vs 1.25): the new ...
- [F2b] TFA p16 6410-32-12-O / -32-16-O print L 1.000, impossible with a -12 / -16 female ORB port in a 2-1/2 in male body (the port depth + drill point > L): catalog value wrong or a placeholder in Brennan's own table
- [F2b] TFA p35 6501-12-08-FG M6 1.612: the same -08 swivel on the -12 body prints M6 1.550 on 6500-12-08-FG; OMi has 1.540 - likely a catalog slip
- [F2b] TFA p17 6504-32-32 prints L 3.700 > L5 2.862 (match/TFA_straights.json swivel_catalog_anomalies) - columns swapped or misprinted; OMi 3.800; Task C derived L14 2.86 (3.80 - Air-Way 0.94) happens to equal the catalog L5
- [F2b] TFA p18 6505-12-08 A DRILL 0.609 departs from the catalog's own 0.719 for the -12 NPTF drill (6505-12-10/-12-12/-12-16); OMi 0.719
- [F3] V0319-06 prints TUBE O.D. 1/4 (dash -06 = 3/8) - typo kept as printed
- [F3] 1803-FG / 1804-FG rows mostly identical to the code 61 rows of the same size (see Q-NEW-F3-CODE62LEN)
- [F45D] 6410-32-20-O L 1.00 (TFA p16): the -20 female ORB port measured on Brennan's own 6410-24-20-O STEP reaches 1.348 to the drill apex - does not fit (OMi copied the 1.000)
- [F45D] 6900-O L - L1 on 6900-06-04 / -08-06 / -08-08 / -10-08-O (0.12 / 0.17 / 0.25 / 0.21) does not match the Brennan 1404 nut-face-to-stem-tip of that NPSM size (0.19 / 0.22 / 0.28 / 0.28); the other 17 rows agree within 0.02
- [F45D] 6506-12-12 L5 2.29 vs OMi 2.280 and 6506-12-14 L5 2.33 vs OMi 2.340 (0.01 inside the one source; OMi-first keeps OMi)
- [match] 6504-32-32 (TFA p17): seat length L 3.700 printed longer than the nut-face length L5 2.862 - misprint or swapped columns.
- [match] 1803-20-24-FG (Flange p5): L1 / L2 / A/F identical to the swept 1803-20-24 row - looks copied.

### 3.5 Column pairings - what the catalog settles about OMi M 1 / M 2 / L 1

The catalog's drawings name each length by a letter. Matching those letters to OMi's values on the rows where the legs differ shows what OMi's columns hold:

| Family | OMi Overall Length | OMi M 1 Size | OMi M 2 Size | OMi L 1 Size |
|---|---|---|---|---|
| Swivel straights (6402, 6504, 6505, 6506, 6565, 1404) | tip to the **swivel-nut face** (Brennan L1 / L5 / L - the letter changes per table) | not used | not used | tip to the **37 deg seat / stem nose** (Brennan L / L2 / L1) |
| Plain elbows 2501, 2501-L, 2502, 2503, 5500, 5502 | - | **side-1 leg** (1st dash; Brennan M, or N1 on 5500, N on 5502) | - | **side-2 leg** (2nd dash; Brennan L, or N on 5500, N1 on 5502) |
| 2505 (JIC x female pipe 45) | - | side-1 (JIC) leg | **side-2 (female pipe) leg** | empty |
| Swivel elbows 6500, 6500-L, 6501, 6502, 6503 | - | axis to the swivel nose / seat (Brennan M4; M on 6502) - but usually 0.01 longer, and on 6500 / 6502 equal to Air-Way M10 / M14 | axis to the **swivel-nut face** (Brennan M6) | **side-1 (male JIC) leg** (Brennan M / N / M2) |
| Tees 2601-2611 | - | leg of the **1st dash** | leg of the **2nd dash**, whatever its end type | leg of the **3rd dash (branch)**, whatever its end type |
| ORFS, flange, hose families | blank in OMi | blank | blank | blank - nothing to settle |

- OMi's header letter is not the end type: 'L 1' is a JIC leg on 2603 / 2605 / 2606 / 2610, 'M 2' a pipe leg on 2605 / 2606 / 2608 / 2611.
- The bores follow the same order: OMi 'Side n ID' = the catalog drill of end n ('B<n>' / 'A<n> DRILL').
- Earlier OMi -> Air-Way mappings (`tools/_out/omi_audit/mapping_final.json`): the catalog **confirms** the uncertain leg mappings of 2501 (M071 / M072), 2501-L (M076 / M077), 2601 (M166-M168), 2602 (M173-M175), 2603 (M179-M181) and the swivel straights 6402 / 6504 / 6505 / 6506 / 6565 (M020-M044). It does **not** support M050 (1404 OAL is to the nut face, not the tip-to-stem length) and M070 (6404 Side 1 ID is the pipe-end drill, not the ORB port drill).
- 2504 and 5501 (only same-dash rows) cannot tell M 1 from M 2 / L 1 by value; the values are the same either way.

## 4. Impact on the 727 MISSING rows

Six impact groups re-checked every Task C row (`tools/_out/omi_apply_20260925/taskC/taskC_merged.json`, 727 rows) against the verified catalog: F1a / F1b (forged -FG rows), F2a / F2b, F3 (new-root skeleton tables), F45D (Task C groups F4F5 + D). Results: `tools/_out/brennan_catalog_20261001/impact/*.json` and `.md`. Rules: Q-NEW-BRENNANCAT treated as yes (the user said "use any needed"); Q-BRENNAN-ONLY stays formally open; OMi + catalog = one source (ASSUMED); a STEP row moves to NOW only when every cell it still needs is printed with a certain / likely column pairing; WORK rows stay WORK (code is still needed).

| Bucket | Before (Task C) | After the catalog | After, if Q-NEW-CATRANK = no |
|---|---:|---:|---:|
| NOW | 4 | 74 | 72 |
| STEP | 105 | 67 | 67 |
| DECIDE | 120 | 88 | 90 |
| WORK | 399 | 399 | 399 |
| SCOPE | 98 | 98 | 98 |
| RESOLVED-A | 1 | 1 | 1 |
| Total | 727 | 727 | 727 |

Moves: DECIDE -> NOW 54, STEP -> DECIDE 22, STEP -> NOW 16. Unchanged: 635 rows. The one row in two groups (5404-L-04X3.000, F2a and F2b) has the same bucket in both (WORK); only its Q-NEW-5404L-XLEN level differs (partly in F2a, answered in F2b). In the question table below each row is counted once (critic 2026-10-01; before, this row was counted in both groups).

| Group | Rows | Catalog hit | Bucket moves (unchanged rows not listed) | STEP verdicts of the group |
|---|---:|---:|---|---|
| F1a | 130 | 129 | DECIDE -> NOW 17, STEP -> DECIDE 4, STEP -> NOW 2 | partly 65, replaced_by_catalog 63, in_repo 20, not_replaced 1 |
| F1b | 130 | 129 | DECIDE -> NOW 9 | partly 116, replaced_by_catalog 15, not_replaced 1 |
| F2a | 141 | 121 | STEP -> NOW 12, STEP -> DECIDE 5, DECIDE -> NOW 3 | partly 44, replaced_by_catalog 36, not_replaced 18 |
| F2b | 141 | 111 | DECIDE -> NOW 13, STEP -> DECIDE 12, STEP -> NOW 2 | partly 57, not_replaced 27, replaced_by_catalog 4 |
| F3 | 138 | 101 | none | partly 88, not_replaced 50 |
| F45D | 48 | 48 | DECIDE -> NOW 12, STEP -> DECIDE 1 | not_replaced 22, replaced_by_catalog 8, partly 5 |

- **Q-NEW-CATRANK** (F45D): may a catalog value take OMi's place where OMi is blank (over Air-Way / a standard)? It decides 2408-14-SOLID and 6801-05-05-NWO-FG (NOW if yes, DECIDE if no).
- **Built rows:** F1b found 51 cells on built (ASSUMED) -FG rows where the review value differs from the catalog (`impact/F1b.json` built_rows_differing_from_catalog). They are reported, not changed.

### 4.1 Questions the catalog answers

Rows per question and how far the catalog answers it (answered / partly / not needed any more). Answers are proposals for the user.

| Question | Rows | Catalog answer (shortened) |
|---|---|---|
| Q-F1 | answered 62, partly 7 | settled for every body cell: the catalog prints this -FG part and its values equal OMi's, so OMi or the awaited Brennan data give the same numbers (ASSUMED, one source) |
| Q-NEW-BRENNANPN | answered 40, partly 4 | CONFIRMED for 0304-C: Brennan lists the JIC cap nut under this exact number |
| Q-BRENNAN-ONLY | not needed 37, partly 5 | NOT NEEDED for this row: every dimension it needed comes from the catalog (Q-NEW-BRENNANCAT treated as yes); no STEP is the sole source any more |
| Q-SCOPE-TUBE | informs only 32 | NOT answered (scope is the user's call) - but the premise "no source of any kind / no Brennan equivalent known" is outdated: Brennan sells this swept elbow as 1703-08-08 (Flange p4) and prints L1 / ... |
| (no Task C id) step_list purpose "confirm Brennan's part number for the swept -Tube parts" | answered 29 | Brennan part number = 1803-12-12 (no suffix) |
| Q-B-ELBOW | answered 28 | YES - OMi "M 1" is the first-dash (side-1) leg and "L 1" the second-dash leg, by the catalog's own column letters |
| Q-6900-IDENT | answered 22 | YES - Brennan titles 6900-O "MORB-FPS STRAIGHT" (TFA p18-19): male ORB B1 x female pipe swivel with an NPSM thread on A2 (drawing: swivel nut C HEX on the A2 end); not a female JIC union |
| Q-TRANSFER-5404N | partly 19 | PARTLY - the catalog gives this part's own length and bore (A1/A2 DRILL 0.281, the same at every length of the dash, which supports length-independence) but no bar diameter, so COD@REF still needs ... |
| Q-B-6501 | answered 17 | yes - same reading as 6500, now tested on the catalog rows (no longer 1 row each) |
| (no Task C id) leg placement - still_missing "which leg carries the MAORB" | answered 14 | MAORB on the horizontal leg B1 (M8), female ORB port on the other leg B2 (M6) |
| Q-B-OTHER-0304 | answered 13 | YES - OMi Overall Length = the cap length (catalog L LGTH) and Hex Flat = the cap hex (catalog C HEX) |
| Q-B-SWSTR | answered 13 | YES (series level, from the drawing) - TFA p18 6505: L5 = pipe tip to swivel-nut face = L15, L = pipe tip to stem nose (seat) = L16 (SPEC 6505 definitions); OMi Overall Length = L5 15/20, OMi L 1 = L ... |
| Q-B-OTHER-0306 | answered 12 | YES - OMi Overall Length = the nut thickness (catalog W WIDTH) and Hex Flat = the nut hex (catalog C HEX) |
| Q-TRANSFER-NUTHEX | not needed 12 | NOT NEEDED for this part - the catalog prints its own swivel-nut hex (C HEX), equal to the Air-Way per-size value after rounding and to the Brennan-measured NPSM_MEAS AF; accepting the transfer would ... |
| Q-NEW-6408H-IDENT | answered 12 | YES - Brennan prints the family as 6408-H<dash>-O "MORB HOLLOW HEX PLUG" (TFA p67, 13 sizes incl. all 12 OMi sizes); OMi "MORB Hollow Hex Plug" values agree (socket hex 8/8, length 6/8); download ... |
| Q-B-OTHER-6408HHP | partly 12 | PARTLY - the drawing confirms OMi "Overall Length" = L (overall) and "Hex Flat" = C5 HEX (the socket across flats); OMi "Body Diameter" (round head) has no catalog column, so that part stays open |
| Q-NEW-PARKER4300 | answered 10 | not answered (Parker is a second source); the Brennan catalog itself prints the locknut hex (C HEX) of this part |
| Q-B-OTHER-6504 | answered 10 | YES (series level, from the drawing) - TFA p17: L5 = male JIC tip to the swivel-nut face = SPEC 6504 L13; OMi Overall Length = L5 (9/15 exact + 3 rounding-only; real: 6504-10-10 +0.10, 6504-16-12 ... |
| Q-CONFLICT-SWOFFSET | not needed 6, answered 4 | NOT NEEDED for this row - L14 is printed (L5 - L = 0.380) |
| Q-B-OTHER-5501 | answered 9 | YES - OMi M 1 = N4 (side-1 leg), L 1 = N6 (side-2 leg), Hex Flat = Y (M104-M106); the repeated OMi leg is Brennan's value |
| Q-TRANSFER-SWOFFSET | not needed 9 | NOT NEEDED for this row - the catalog prints L14 itself (L 1.210) |
| Q-B-OTHER-TEE2 | answered 8 | YES for 2606 - OMi M 1 = side-1 JIC run leg (M1_1), M 2 = side-2 female pipe run leg (N1), L 1 = side-3 JIC branch leg (M1_3), Hex Flat = Y1, Side 1 / 3 ID = D1 / D3 (M193-M198) |
| Q-B-OTHER-6420 | answered 8 | Yes - OMi "Overall Length" is the face-to-face length (catalog L LGTH) and "Hex Flat" is the body hex (catalog C4 HEX) |
| Q-NEW-FOLD-2501LL | answered 7 | drawing evidence only: the p24 2501-LL drawing shows the forged hex arm running up the long pipe leg exactly as on 2501-L (fold shape); the pilot STEP still proves it |
| Q-B-SWELB | answered 7 | yes - the catalog's own column letters settle the leg reading (OMi M 1 = nose / seat M4, M 2 = nut face M6, L 1 = male JIC leg M) |
| Q-PLACEHOLDER | answered 4, partly 3 | REAL as far as the catalog goes - Brennan prints 1.00 (TFA p16), so OMi's 1.000 is the catalog value, not an OMi entry placeholder; the part builds at 1.000 (Task C paper check). |
| Q-NEW-6407SIB | not needed 7 | Not needed for OAL / hexes / drills: the catalog prints the 3474's own L1, C1 (lock nut), C2 (body) and B1/B2 DRILL. |
| Q-THREAD | not needed 7 | not needed for this row: the catalog prints 1/8-27 for 1501-02-04-FG -> THDMAJ_A 0.405; quote Air-Way's "1/8-24" in $COMMENT |
| Q-B-OTHER-6500L | partly 5 | partly - OMi side settled: M 1 = catalog M4 (nose / seat), M 2 = M6 (nut face), L 1 = M (male JIC leg), Hex Flat = Y FLATS, Nut Hex 1 = C HEX, Side 1 / 2 ID = B1 / B2 DRILL; the Air-Way side (M12 = ... |
| Q-B-OTHER-2504 | answered 4 | YES - OMi M 1 / M 2 / Hex Flat / Side 1 ID / Side 2 ID = legs of ends 1 / 2, body hex, bores (M090-M094); the repeated OMi leg is Brennan's value |
| Q-NEW-AWALIAS | answered 3, partly 1 | PARTLY (supports yes for the naming) - Brennan numbers the 1/2-14 x 2.500 in nipple "5404-N-08X2.500" (TFA p12): the same size/length as Air-Way "5404-N-8-8 X 2 1/2" (L 2.50 = 2.500); but the catalog ... |
| Q-B-OTHER-2505 | answered 3 | YES - OMi M 1 = M2 (JIC leg), M 2 = N6 (female pipe leg), Hex Flat = Y1, Side 1 ID = D (M095-M098) |
| Q-B-TEE | answered 3 | YES - M 1 / M 2 / L 1 = the legs of ends 1 / 2 / 3 |
| Q-B-5500 | answered 3 | YES - OMi "M 1" = side-1 (A1) leg, "L 1" = side-2 (A2) leg |
| (critic, step 6801-LL-08-08-NWO-FG) is the Air-Way 6801-LL-08-08-NWO-FG row really a -10 row? | answered 3 | yes - Brennan 6801-LL-08-08-NWO-FG prints M 1.250 / M7 2.480 / C HEX 0.875 / B2 DRILL 0.391; the Air-Way -FG row (M 1.31, M12 3.25, C4HEX 1, D2 0.48) equals the Air-Way 6801-LL-08-10-NWO row value ... |
| Q-NEW-5404L-XLEN | partly 2, answered 1 | SUPPORTED, not settled: in Brennan's own long-nipple numbering the X-number is the overall length (5404-N-04X2.000 L 2.000, 5404-N-04X3.000 L 3.000, every 5404-N row L = X), the same as the Air-Way ... |
| Q-CONFLICT-2502-MS51506 | answered 2 | the catalog gives Brennan's -FG legs (the "wait for the Brennan STEP" option) = OMi; the conflict with MS51506 stays a two-source conflict for the user |
| Q-HEXSNAP (non-gating note in the row) | answered 2 | the catalog prints the locknut as 0.625 (5/8); Air-Way 0.63 is its 2-decimal print - rounding only, no change |
| Q-B-OTHER-2602Y1 | answered 1 | YES - OMi Hex Flat is the forged body hex Y1, not a boss diameter |
| Q-B-OTHER-6404D | answered 1 | D1 - the catalog letters settle it: OMi Side 1 ID 0.689 equals the catalog "A DRILL", and A is the male pipe end on the p15 drawing; Brennan prints no ORB-port drill at all (so M070 / D3 is not ... |
| Q-HEXSNAP | answered 1 | Brennan prints 1.375 (1-3/8) for the hex; OMi 1.374 is not a print of it (0.001 off) - snap to 1.375 = the catalog value |
| Q-CONFLICT-6801-05-05-NWO-FG | answered 1 | answered: 1.13 (build as tabled, MS 1.090 quoted in $COMMENT) - by the OMi-first rule with the catalog in OMi's place (Q-NEW-CATRANK); without that reading it stays your call |
| Q-CONFLICT-2408-14-SOLID | answered 1 | answered: 1.25 - catalog C HEX 1.250 in OMi's place outranks Air-Way 1.125 (Q-NEW-CATRANK); it also equals MS51518D 1 1/4 and Air-Way's own -14 male hexes. |
| Q-CONFLICT-2501-04-02-FG | not needed 1 | not needed: with Q-B-ELBOW = yes OMi gives N 0.78 (= catalog L 0.78 = MS51504 .780) |
| Q-B-OTHER-6504 (not gating here) | answered 1 | answered by the catalog's letters: OMi "Overall Length" = catalog L5 = JIC tip to swivel-nut face = the L13 feature (6504 table: OMi = L5 on 12 of 15 rows within 0.004, equal on 9). |
| Q-GARBLE | not needed 1 | not needed: catalog A3 DRILL 1.312 fills D3 (the ".31"-as-1.31 reading agrees after rounding) |
| Q-BRENNAN-ONLY (for L17) | not needed 1 | not needed for L17 (the catalog / OMi give it); still the route for the -14 swivel end geometry |
| Q-CONFLICT-6900-05-04-O | partly 1 | a third option without a download: the catalog prints L 1.280 / L1 1.090 (nut face to stem tip 0.19 = the Brennan -04 NPSM nut, sandbox: builds); neither Air-Way pick (keep W4 -> L2 1.11, keep L2 -> ... |

Not answered by the catalog: Q-SCOPE-TUBE (scope is the user's call; the catalog only shows Brennan sells the swept -Tube parts), Q-BRENNAN-ONLY for cells only a STEP gives, every Q-NEWMASTER-*, and the transfer questions for values the catalog does not print (tap drills Q-TRANSFER-TAPDRILL, ORB end detail, flange head O Q-TRANSFER-FLG61-O, hose bead Q-NEW-HOSEB).

### 4.2 New questions raised by the catalog

| Id | Rows | Question (shortened) |
|---|---:|---|
| Q-NEW-F1A-1602PILOT | 1 | 1602-08-08-08-FG - the planned pilot of the new 1602 master - is not in Brennan's TFA catalog (the p48 1602-FG table prints -02, -04, -06, -12, -16, -20 and the reducers 06-04-04, 08-06-06, 12-08-08 only). |
| Q-NEW-F1A-5504TAP | 5 | 5504-06-04 / -06-06 / -08-06 / -20-20 / -24-24-FG: the catalog (TFA p32) now gives both legs and the hex; only the two port tap drills are left, which Task C planned to measure on each STEP. |
| Q-NEW-F1B-CATDIFF | 7 | OMi and Brennan's catalog print different values for the same -FG part (both one source). Which value goes into the table for each cell below? Default by the standing rule (OMi first, 2026-09-25) is OMi with a $COMMENT; evidence per cell is given. |
| Q-NEW-F1B-TAPDRILL-SCOPE | 17 | These STEP rows of the built masters 5504 / 5602 / 5604 / 5605 now get every body cell from the catalog; only the female-port tap drill is missing (the catalog prints none). |
| Q-NEW-F1B-ORBEND | 11 | These STEP rows of the built masters 6801 / 6802 / 6803 / 6804 now get legs, body hex, bores (and confirm the locknut hex) from the catalog; only the ORB end cells ORB_THDL / ORB_GRVDIA / ORB_GRVW (+ ORB_I3 on 6801 / 6802) are missing. |
| Q-NEW-F1B-RANGE | 7 | For these 6901 / 6902 NPSM swivel bores the catalog prints a min/max range (e.g. 0.44/0.46) instead of one drill. Which value is modelled (min, max, or measured on the STEP)? No value is taken from a range without your answer (never average). |
| Q-NEW-F2A-DRILLRANGE | 1 | The catalog prints some drills as a range (1405-04-06 A2 DRILL ".32/.34"). The review needs one number and values are never averaged: use the lower bound, the upper bound, or measure the STEP? |
| Q-NEW-F2A-OMIvsCAT | 3 | Where OMi and the Brennan catalog (one source) print different numbers, keep OMi (standing rule: OMi dimension file first) and note the catalog value in $COMMENT? 2501-24-32-FG D1 1.940 vs 1.938; 2706-LN-08-06 L25 2.400 vs 2.410 and D 0.295 vs 0.297 (the same ... |
| Q-NEW-F2A-NOTINCAT | 18 | These parts need a Brennan STEP (step list) but are not in Brennan's catalogs, so the STEP may not exist: 1405-20-24, 1504-32-32-FG, 1703-08-08-FG, 2403-06-02, 2406-06-12, 2502-20-16-FG, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-04-02, ... |
| (new) Q-CAT-5404N-BORE | 19 | 5404-N long nipples: Brennan prints the through drill -04 0.281 / -06 0.406 / -08 0.531 on every length; Air-Way prints bores 0.30 / 0.39 / 0.48 (the Task C transfer). |
| (new) Q-CAT-6405-32-16-D3 | 1 | 6405-32-16-O bore D3: OMi Side 1 ID 1.080 (Items!S1805, the same value OMi gives 6405-24-16-O) vs Brennan TFA p16 B DRILL 1.156. |
| (new) Q-CAT-6408HHP-L | 2 | 6408-HHP-12-O / -16-O overall length: OMi 0.780 vs Brennan TFA p67 0.77 / 0.775 (real under the strict rule; -16 may be a padded 0.78). Which? |
| (new) Q-CAT-6410-16-04-D | 1 | 6410-16-04-O through bore D: OMi Side 1 ID 0.368 (Items!S1862) vs Brennan TFA p16 B DRILL 0.389 (the catalog's value for every -04 port reducer: 6410-12-04-O, -20-04-O). |
| (new) Q-CAT-6501-12-08-M5 | 1 | 6501-12-08-FG nut-face leg M5: OMi M 2 1.540 (Items!O1949) vs Brennan TFA p35 M6 1.612. Which? (The catalog's sister 6500-12-08-FG prints M6 1.550 = OMi's 1.55; 1.612 may be a catalog slip.) |
| (new) Q-CAT-6504-32-32-L | 1 | 6504-32-32 lengths: OMi L13 3.800; Brennan TFA p17 prints L 3.700 / L5 2.862 (inconsistent: seat beyond the nut face). Keep OMi 3.800 + Q-TRANSFER-SWOFFSET (L14 2.86), or get the STEP? |
| (new) Q-CAT-6505-12-08-D1 | 1 | 6505-12-08 pipe-end bore D1: OMi Side 1 ID 0.719 (Items!S2021) vs Brennan TFA p18 A DRILL 0.609. The catalog prints 0.719 for the -12 NPTF drill on 6505-12-10/-12-12/-12-16 (0.609 is the -12 JIC drill) - likely a catalog slip. Which? |
| (new) Q-CAT-6506-32-32-L17 | 1 | 6506-32-32 L17: OMi Overall Length 3.200 (Items!L2050) vs Brennan TFA p18 L5 3.12. Which? |
| Q-NEW-F3-FLARELESS-ALIAS | 3 | Is OMi 0618 (JIC flareless tube nut) = Brennan V0318 and OMi 0619 (JIC flareless sleeve) = Brennan V0319? Same descriptions and dashes; V0318-08 thread 3/4-16 = OMi 0618-08. |
| Q-NEW-F3-6420-0808-OAL | 1 | 6420-08-08 overall length: catalog 1.500 vs OMi 1.320 (OMi repeats 6420-08-06). Take 1.500? |
| Q-NEW-F3-1803PILOT | 2 | 1803-08-08-FG and 1803-32-32-FG are not in Brennan's Flange catalog (only the swept 1803-08-08 / 1803-32-32). Move the 1803 forged pilot to 1803-12-12-FG and check brennaninc.com for the two missing forged sizes? |
| Q-NEW-F3-6566 | 2 | No 6566 (FJS x FJS forged 90 deg elbow) in the TFA catalog: does Brennan sell 6566-06-06-FG / 6566-16-16-FG (STEP available)? If not, the two rows have no source at all. |
| Q-NEW-F3-CODE62LEN | 8 | Most 1803-FG / 1804-FG rows print exactly the L1 / L2 / A/F of the code 61 1703-FG / 1704-FG row of the same size. Use them as printed (ASSUMED) and let the pilot STEP confirm? |
| Q-NEW-CATRANK | 2 | Where OMi gives no value, may a Brennan catalog value take OMi's place in the OMi-first rule (over Air-Way, and over a standard such as MS)? OMi's dimensions are Brennan's data, and you said to use the catalogs. |
| Q-NEW-6900-LEN | 21 | 6900 lengths: Brennan's catalog (TFA p18-19: L = ORB end face to nut face, L1 = ORB end face to stem nose) differs from Air-Way W4 / L2 on most of the 21 rows (up to 0.18 in). |

## 5. The STEP list: before and after

Every Task C STEP item appears once (623), plus **1 added item: 6500-02-02-FG**. The tier-1 MEASURED-ENDS work found that the three rows needing a -02 swivel (6505-04-02, 6500-04-02-FG, 6502-04-02-FG) are not Brennan catalog parts; 6500-02-02-FG (TFA p34) carries the same -02 swivel on the forged 6500 body swiv.py is validated on (`tools/_out/tier1_20261001/work/MEASURED-ENDS/STEPS_NEEDED.txt`).

**Before** - Task C step list (2026-09-26) and the preliminary list of this morning (unverified parse):

| Task C stage | 1A | 1B | 2 | 3 | S-PILOT | S-REST | CONDITIONAL | OPTIONAL | IN_REPO | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Items | 98 | 23 | 55 | 256 | 3 | 33 | 87 | 4 | 64 | 623 |

Preliminary list (00_DOCS/Brennan_STEP_downloads_START_2026-10-01.xlsx): get now 82, later 68, skip (catalog) 267, check 15, only if 127, already have 64 = 623.

**After** - `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx`:

| Sheet | Files | Meaning |
|---|---:|---|
| Download now | 95 | priority 1: unlocks rows on existing masters / tier-1 fixes, or validates a pilot |
| Later | 283 | priority 2: after its pilot and your approval of the master, after your answer to a question, or after you confirm a Brennan number |
| Conditional-Optional | 57 | priority 3: only if bent tubes come into scope, a question is answered no, or an optional check |
| Replaced by catalog | 125 | no download: the catalog prints every value it was for, or answers its condition |
| Already in repo | 64 | in 09_STEP_FILES |
| Total | 624 | 623 Task C + 1 added |

| Task C stage -> sheet | Files |
|---|---:|
| 1A -> Download now | 27 |
| 1A -> Later | 51 |
| 1A -> Replaced by catalog | 20 |
| 1B -> Download now | 15 |
| 1B -> Later | 4 |
| 1B -> Replaced by catalog | 5 |
| 2 -> Download now | 53 |
| 2 -> Later | 2 |
| 3 -> Later | 226 |
| 3 -> Replaced by catalog | 30 |
| S-PILOT -> Conditional-Optional | 3 |
| S-REST -> Conditional-Optional | 33 |
| CONDITIONAL -> Conditional-Optional | 20 |
| CONDITIONAL -> Replaced by catalog | 67 |
| OPTIONAL -> Conditional-Optional | 1 |
| OPTIONAL -> Replaced by catalog | 3 |
| IN_REPO -> Already in repo | 64 |

Catalog verdicts over all 624 items: replaced 126, partly 375, not replaced 123, not assessed 0. The impact groups gave a verdict on 622 of the 623 Task C items. 8 in-repo items they only marked 'in repo', 6502-08-08-FG (an in-repo reference no group listed) and the added item were assessed here with the same rule as F3 / F45D: an in-repo STEP is a geometry reference the catalog cannot print -> not replaced.

Notes on the lists:

- **Download now = 95.** 53 stage-2 pilots, 27 stage-1A STEPs and 15 stage-1B STEPs (14 Task C + the added 6500-02-02-FG). The catalog replaces none of them, and no pending transfer question can stand in for them. Some rows still need a decision before they build (e.g. Q-NEW-2702HOLD, Q-NEW-1700BODY, Q-NEW-ASME40, the Q-NEWMASTER-* of each pilot).
- **24 of them are in no Brennan catalog** (column 'In catalog' = NO, sorted to the end of the sheet). All 94 Brennan STEPs already in 09_STEP_FILES are catalog parts, so these may not exist on brennaninc.com. Try them; if a part is not there, tell Claude - the row then needs another source or a DROP (Q-NEW-F2A-NOTINCAT, Q-NEW-F1A-1602PILOT, Q-NEW-F3-1803PILOT, Q-NEW-F3-6566). Fallbacks are in the 'Warning / fallback' column (1602 -> 1602-12-12-12-FG, 1803 -> 1803-12-12-FG).
- **Later = 283:** 226 stage-3 STEPs that wait for their pilot; 55 stage-1A / 1B STEPs now needed only for a tap drill, an ORB end detail or a printed range - each skips if you answer the question in column 'Skip if' (mostly Q-TRANSFER-TAPDRILL, Q-NEW-F1B-TAPDRILL-SCOPE, Q-NEW-F1B-ORBEND, Q-NEW-F1A-5504TAP), and is downloaded only if the answer is no; 2 pilots whose Brennan number must be confirmed first (0618-08 -> V0318-08, 0619-08 -> V0319-08, Q-NEW-F3-FLARELESS-ALIAS).
- **Stage 1B (23 items) = "needed for the tier-1 generator fixes"** (column Tier-1 fix). SWIV-02, SWIV-14, JICF-03 and ORBF-02 need geometry from a STEP (6505-04-02, 6500-04-02-FG, 6502-04-02-FG + the added 6500-02-02-FG; 6506-12-14; 2406-03-04; 6410-04-02-O). The others need the part's dimensions: the catalog replaces 5 of them (2403-04-02, -10-04, -16-10, -24-16, 2403-LH-24-24); 2405-10-06 / -14-12 and 6405-02-02-O / -02-04-O now wait only for Q-TRANSFER-TAPDRILL (Later); 2403-06-02 is not in the catalog; 2404-L-32-32 (hex length T20), the four -40 parts (end geometry) and 6565-32-32 / 6802-32-32-NWO-FG (closed-loop shape) stay Download now.
- **in_repo re-checked** against 09_STEP_FILES: 94 Brennan STEP files; 0 Task C flags were wrong. None of today's downloads had landed when the list was built. The folder also holds 30 Brennan STEPs that no Task C item needs, and two zips with 5 more 6400 STEPs (6400-08-04-O, -24-16-O, -12-24-O, -20-12-O, -32-20-O) - none of them is on the list.

**The 61 STEPs the user is downloading now** (prelim group 1 = the 55 pilots + the 6 tier-1 geometry STEPs):

- 59 stay on Download now.
- 0618-08 -> Later, 0619-08 -> Later: Brennan has no such part number; confirm the V-numbers first.
- 5406-HHP-08: save as BRENNAN_5406-HP-08.stp (Brennan number).
- Not in any catalog (may not exist): 0618-08, 0619-08, 1602-08-08-08-FG, 1803-08-08-FG, 5404-L-04X2.000, 5404-R-04-04-047, 6500-04-02-FG, 6502-04-02-FG, 6505-04-02, 6566-06-06-FG.
- Add **6500-02-02-FG** (the -02 swivel source for SWIV-02).

## 6. Files

| File | What |
|---|---|
| `tools/catalog/parse_brennan_catalog.py` | the parser (pymupdf text layer) |
| `tools/_out/brennan_catalog_20261001/parsed/catalog_parsed.json` | raw parse |
| `tools/_out/brennan_catalog_20261001/verify/*.json` | page-check chunks (300 dpi image vs text vs parse) |
| `tools/_out/brennan_catalog_20261001/merge/apply_corrections.py, merge_log.txt` | corrections and counts |
| `tools/_out/brennan_catalog_20261001/catalog_verified.json / .xlsx` | the verified catalog (427 tables, 5,056 rows) |
| `tools/_out/brennan_catalog_20261001/catalog_index.json` | part number -> catalog rows |
| `tools/_out/brennan_catalog_20261001/match/*.json, *.md, *_diffcheck.json` | catalog vs OMi per group, and the re-check of every difference |
| `tools/_out/brennan_catalog_20261001/impact/*.json, *.md` | catalog vs the 727 MISSING rows (bucket moves, cells, questions, STEP verdicts) |
| `tools/_out/brennan_catalog_20261001/steplist/build_steplist.py, steplist.json` | the final STEP list (this file's section 5) |
| `tools/_out/brennan_catalog_20261001/steplist/build_catalog_md.py` | writes this report |
| `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` | the STEP list workbook (Download now / Later / Conditional-Optional / Replaced by catalog / Already in repo / All / Copy list / Summary) |
| `00_DOCS/Brennan_STEP_downloads_START_2026-10-01.xlsx / .md` | the preliminary list of this morning (superseded by the final list) |

