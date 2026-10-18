# The 77 tube fittings the September crawl dropped (2026-10-16) - STAGED, nothing applied

OMi's tube fittings collection has 1,672 SKUs; our list `omi_skus_all.txt` (2026-09-23) has 1,595. The old crawl's fetch layer dropped
77, page by page; none of them is new on the site (listing session: `tools/_out/omi_enum_20261015/REPORT.md` section 3). User
2026-10-15: "use airway dimensions, check brennan too"; standing rule 2026-09-25: OMi's dimension file first, Air-Way fills.

## 37 already have an Air-Way row, wrongly marked DROP
The reconciliation could not see the dropped SKU, so these Air-Way rows got `ScopeAction` DROP. Proposed (`CHANGES.csv`, 136 lines):
- `ScopeAction` DROP -> BUILD and `$PRP@OMiSKU` = the SKU. The `$COMMENT` gets a note that the old DROP text is void.
- **OMi values first** (certain column mappings of the 2026-09-25 audit, `tools/_out/omi_audit/mapping_final.json`, Task A form): 9 rows
  take an OMi value and become ASSUMED. For example 2705-06-06 / -06-08 / -08-08 length (2.18 -> 2.220 ...), 6410-08-04-O length
  0.8 -> 1.100, 6405-16-08-O length 1.47 -> 1.720, 5502-16-12-FG flats 1.63 -> 1.312, 6505-32-32 hex 2.50 -> 2.625.
- **Brennan check** (TFA catalog, 2026-10-01 parse; only columns with the same letter or an unambiguous meaning):
  - Air-Way = Brennan on every compared cell, length and hex included, with no OMi value taken -> VERIFIED.
  - A difference stays at the dimension source and is noted (PROJECT_STATUS s6): 2406-20-12 / -20-16 length 2.02 / 2.01 vs Brennan
    2.000, 5502-16-12-FG N1 1.39 vs 1.360, 6410-08-04-O bore 0.38 vs 0.391, 6901-08-08 bore 0.45 vs 0.460.
- Result: **21 VERIFIED, 14 ASSUMED, 2 keep "ASSUMED (hex/legs single-source for unequal-dash)"** (6801-16-12 / -16-16). Before:
  7 VERIFIED-type rows and 30 ASSUMED.

| Table | Rows |
|---|---|
| 2403 | 1 |
| 2406 | 2 |
| 2501 | 2 |
| 2502 | 2 |
| 2650 | 1 |
| 2701 | 1 |
| 2705 | 3 |
| 5406 | 2 |
| 5502 | 3 |
| 6400 | 4 |
| 6405 | 2 |
| 6410 | 2 |
| 6500 | 2 |
| 6502 | 1 |
| 6505 | 2 |
| 6602 | 1 |
| 6801 | 3 |
| 6803 | 2 |
| 6901 | 1 |

**Apply only at ship time:** `python -I scripts/apply_77.py` is a dry run (136 changes, 0 guard failures on 2026-10-16); `--apply`
writes, after copying every touched table to `old_files/` and `_to_delete/`. Batch 16 (staged 2026-10-09, not shipped) carries its
own copies of the 2501, 6500 and 6505 tables: apply after batch 16 ships, or re-run `stage_77.py` against its tables first. Then
regenerate the touched roots and dry-run them as for any batch. 6400 is the hand-built master; regenerating it is allowed (s5).

## 40 have no row
Air-Way does not print these sizes; every review table holds all of its Air-Way series' rows. Breakdown:
- Brennan's catalog prints 34 of them (check only).
- OMi's parts file has some values for 9: 2404-14-12, 2404-16-08, 2502-04-06-FG, 2502-05-04-FG, 2504-16-16-FG, 2505-04-04-FG,
  2505-06-06-FG, 2705-06-04 and 6402-12-10-O. They are partial: lengths / hex / bores, no end details.
- The other 31 have no dimension source we may use.
- Not added to any table. A new row needs its table's end-library columns (the tabling step), and each row would be MISSING unless
  OMi's values cover it.
- They include 0618-06 (flareless nut, in the 2026-10-14 scope), 2613 x2 and 6316 x3 (6316 has no review table at all).
- Per-row detail: `rows77.json`.

## Effect on the counts (after apply + regeneration)
- BUILD rows 1,804 -> 1,841 (the 37, all with dimensions). The 40 would add 40 MISSING BUILD rows when tabled.
