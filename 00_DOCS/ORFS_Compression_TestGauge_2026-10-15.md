# ORFS, compression and test-gauge parts: Air-Way dimensions, Brennan check (2026-10-15)

You asked (2026-10-15): **"use airway dimensions, check brennan too"**, for the ~704 carbon-steel parts on OMi's website that
were never in our part list: O-ring face seal (ORFS) 385, compression 230, test gauge 12, and ~77 tube fittings the September
crawl dropped. Nothing was built or shipped. The review tables are staged in `tools/_out/orfs_airway_20261015/review_tables/`.
Spreadsheet with every part: `00_DOCS/ORFS_AirWay_Brennan_2026-10-15.xlsx`.

## How it was done
- **Air-Way (the source):** all 51 Air-Way ORFS series (FF...) were fetched twice from `parts.air-way.com/api/series/<id>`. Both
  passes are identical: 673 rows, saved as `07_RAW_EXTRACTS/airway_passes/FF*_p1.txt` / `_p2.txt` (new files).
- **Brennan (the check only):** the verified parse of Brennan's ORFS catalog (2026-10-01, 666 rows). Brennan values are never
  used as data ("You cannot use Brennan data as your own").
- **OMi (which parts exist):** OMi's website ORFS collection, read by the listing session on 2026-10-16. Two crawl passes agree
  exactly, giving the 385 SKUs OMi publishes; the list is `07_RAW_EXTRACTS/omi_feed/omi_skus_orfs.txt`. All 385 are in OMi's parts
  file (`WebsitePartsInfo2026.xlsx`). That file has 114 more FS rows that are not on the website; they are DROP rows now.
- **Parts were paired by connection type, not by series number.** Three Air-Way numbers point at a different part:
  - Air-Way FF6402 (ORB × female ORFS swivel) is OMi **FS6540**.
  - OMi FS6402 (male face seal × female JIC swivel) has no Air-Way series.
  - OMi FS6504 (female ORFS swivel × male JIC) is Air-Way **FF7504**, not FF6504.

  Also: OMi FS2406 = Air-Way FF2407, and OMi FS6403 = Air-Way FF7403.
- **Status per part:**
  - Air-Way = Brennan on every compared cell → **VERIFIED**. Rounding-only differences count as equal, by your 2026-09-25 rule.
  - Air-Way only → **ASSUMED**.
  - Air-Way and Brennan differ → **built to Air-Way (ASSUMED)**, with Brennan's value written in the row. This is the project's
    standing convention (PROJECT_STATUS section 6, as on 6801).
  - No Air-Way row → MISSING.
- **Air-Way thread typos don't block a part.** 16 Air-Way rows print a thread wrongly ("9/19-18", "13/16-12", "17/16-12" ...),
  found by checking Air-Way against its own other rows of the same dash. Their thread-major cells are left empty, with a note.
  Threads come from the end library by dash anyway.

## Results on OMi's website (385 ORFS parts)

| Status | Plain | Forged (-FG) | Total |
|---|---|---|---|
| VERIFIED: Air-Way = Brennan (forged: Air-Way's plain row = Brennan's forged row on every cell, your decision below) | 99 | 117 | **216** |
| ASSUMED: Air-Way only, or built to Air-Way where Brennan differs | 53 | - | **53** |
| MISSING | 44 | 72 | 116 |

So **269 of OMi's 385 ORFS parts have dimensions.**
- The 53 ASSUMED include 41 where Brennan differs: 22 by 0.02 in or less, 19 by more.
- Of the 44 plain MISSING, 24 are in series Air-Way doesn't make (below); the rest are sizes Air-Way doesn't print, plus FS0319-24,
  held.
- Over all 499 rows of OMi's parts file (website or not): 226 VERIFIED, 61 ASSUMED, 212 MISSING.
- Fixes on 2026-10-16, from the ORFS model-type plan (`tools/_out/orfs_modeltype_20261016/PLAN.md` section 8):
  - FS0319-24 is held: Air-Way contradicts itself (sleeve OD 1.71 here, 2.00 on its own matching reducer collar; Brennan 1.910).
  - FS6504's VERIFIED rows are now ASSUMED: only the length could be compared.
  - The 16 thread typos above.
- Best agreement with Brennan: FS2403 (15 of 17 VERIFIED), FS6400 (21 of 32), FS2406 (11 of 19), FS2700 / FS2700-LN (7 of 8
  each), FS0318 (8 of 9), FS0306 and FS0319 (6 of 9 each), FS6540 (5 of 6).
- Least: FS2404, where Air-Way and Brennan print different lengths on most sizes (1 of 24 VERIFIED, 21 built to Air-Way), and
  FS6505 (0 of 6).

The per-series table is the Summary sheet.

**Where Brennan differs by more than 0.02 in** (Brennan differs sheet). Built to Air-Way; tell me if any should be held instead:
- FS0319-24 sleeve OD: 1.71 vs 1.910. Now held, because Air-Way contradicts itself (above).
- FS2406-20-16 length: 1.34 vs 1.514.
- FS6505-08-08 length: 1.99 vs 2.150.
- FS2404 lengths on 9 sizes.
- Different hex sizes: FS6400-20-16 1.75 vs 1.875, FS6400-06-10 / -08-10 1.00 vs 1.062.

## The forged ORFS parts (264): your decision of 2026-10-15
You decided: **"Yes - use Air-Way's sizes for the 121 forged ORFS parts where Brennan's forged row matches on every cell
(VERIFIED); the rest stay MISSING."**

Brennan's catalog prints the real forged parts under OMi's own part numbers, but its numbers may only check ours. So a forged part
takes the Air-Way plain row of the same size only where Brennan's forged row prints the same value in every compared cell: legs,
body flats and nut hex.

- **Over all 264 forged rows of OMi's parts file:**
  - **123 VERIFIED.** That is the 121 counted before, plus FS6801-L-06-06 and -08-08: once the FS6801-L parts were paired with
    Brennan's FS6801-L table, they also match on every cell.
  - **On the website:** 117 of OMi's 189 forged ORFS parts are VERIFIED and 72 stay MISSING.
- **The 141 forged rows that stay MISSING (parts file):**
  - 59: Air-Way's plain row differs from Brennan's forged row (mostly the forged body flats).
  - 29: Brennan prints the part but Air-Way has no plain row.
  - 26: Brennan prints no forged row of that size.
  - 27: neither source covers the series (FS1704 / FS1804 flange -FG, FS2502, FS2601, FS6503, FS7202).
- FS6502's 8 sizes all count as "differs" because its second leg (Brennan L2, Air-Way L52) seems to be measured to a different
  point. Settling that needs the Air-Way drawing.
- The forged body shape will come from Brennan 3D files (shape only); none of the ORFS ones are downloaded yet.

## No dimension source at all
- **Compression (C..., "bite type"), 230 website parts** (373 rows in OMi's file, incl. body-only "-M1" items). Air-Way has no
  compression series. Brennan prints only the flareless nut and sleeve (V0318 / V0319), and Brennan alone may not be used. These
  need OMi's drawings or another source.
- **Test gauge (TGT-6504 / TGT-FS2406), 12 parts:** swivel unions with a -04 pipe test port. Air-Way's two test-point series are
  metric test points, a different part.
- **ORFS series Air-Way doesn't make (45 rows in OMi's parts file, 24 of them on the website; Brennan only):**
  - FS0304-C cap insert assembly: Air-Way's FF304-C is a plain cap nut.
  - FS1700 / FS1800 flange straights.
  - FS2405 (male face seal × female pipe).
  - FS6402 (male face seal × female JIC swivel).

## Still open
- **The website lists are complete** (2026-10-16, two passes each, every count = the website's): ORFS 385, compression 230, test
  gauge 12, tube fittings 1,672, all in `07_RAW_EXTRACTS/omi_feed/`.
- **The 77 dropped tube fittings:** 37 already sit in our review tables as Air-Way rows wrongly marked DROP. They are staged to
  become BUILD (21 VERIFIED, 14 ASSUMED, 2 special), with OMi values first and a Brennan check: `tools/_out/adapters77_20261016/REPORT_77.md`,
  applied at ship time. The other 40 have no Air-Way row: Brennan prints 34, and OMi has partial values for 9.
- **Before any of this can be modelled:** the ORFS model-type plan is written (`tools/_out/orfs_modeltype_20261016/PLAN.md` +
  `STEPS_NEEDED.txt`):
  - 31 new FS masters, plus the FS4000 O-rings folded into the 4000 master.
  - New end shapes: the male face-seal end, the female face-seal swivel nut, and longer ORB studs.
  - 32 Brennan files to download (shape only), 9 pilots first.
  - It waits on your answers to its questions (Q-FS-MASTER, Q-FS-ORBSTUD, Q-FS-2NDSHAPE, Q-FS-NUT, Q-FS2406-NUT, Q-FS2408-HOLE,
    S1-S3), each with a recommendation.
- **What it adds** (out of the 2,535): 269 ORFS parts on OMi's website have dimensions now (216 VERIFIED, 53 ASSUMED). All of
  them still need the ORFS model type before they count as built.

## Files
| What | Where |
|---|---|
| Staged review tables (51 series, every OMi FS series) | `tools/_out/orfs_airway_20261015/review_tables/DesignTable_FS*.xlsx` |
| Every part, Brennan differences, forged, compression | `00_DOCS/ORFS_AirWay_Brennan_2026-10-15.xlsx` |
| Air-Way passes | `07_RAW_EXTRACTS/airway_passes/FF*_p1.txt` / `_p2.txt`, raw JSON in `tools/_out/orfs_airway_20261015/raw/` |
| Scripts | `tools/_out/orfs_airway_20261015/scripts/` (`fetch_orfs.py`, `compare_orfs.py`, `forged_info.py`, `build_tables.py`, `make_report.py`) |
