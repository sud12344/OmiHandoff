# OMi values vs the current tables - A19 / A20 / A21 / A23 (2026-10-18)

Read-only check, saved by the main session from the agent's report. Inputs:
- OMi `07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx` (sha256 e5109342...; the same file the audit used).
- Current values: `tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES`.
- "Built" = present in a live `04_DESIGN_TABLES/DesignTable_*_SW2.xlsx`.
- Mappings: `tools/_out/omi_audit/mapping_final.json`.
- Rounding rule of 2026-09-25 (QA #158).
- Script: `a19_diff.py`.

## A19 - built configurations where OMi differs

**Certain mappings: 8 cells / 8 configurations, all 6400** (+0.010 to +0.129). Task A already applied every other certain difference.
- 4 hexes:
  - -08-04: 0.8125 -> 0.875
  - -10-06 / -10-08: 0.9375 -> 1.000
  - -24-16 / -24-20: 2.000 -> 2.125
- 2 ORB-side bores:
  - -06-08: 0.30 -> 0.391
  - -10-12: 0.48 -> 0.609
- 1 length: -06-16 1.68 -> 1.69.
- 6400 is to be rebuilt by the generator (A6).

**Uncertain readings (not counted above): 141 cells / 98 configurations** (`A19_uncertain_readings.csv`).

(a) Settled since, by the Brennan catalog drawing letters in batch 15: **74 cells / 48 configurations**.

| Table | Configs | Change (in) | Note |
|---|---|---|---|
| 6505 | 13 | ±0.18 | L15 and L16 move together |
| 6506 | 10 | -0.01 to +0.17 | L17 and L18 |
| 6504 | 9 | +0.01 to +0.10 | L13 only. OMi gives no L14, so the swivel nose would move against the nut face |
| 2503 | 5 | -0.30 to +0.28 | 2503-04-08-FG / -10-12-FG look leg-swapped |
| 5500 | 2 | ±0.19 | 5500-16-12-FG is exactly swapped |
| 6500 | 3 | -0.01 | |
| 6502 | 3 | -0.01 to +0.03 | |
| 6501 | 1 | +0.03 | |
| 2501 / 2501L | 2 | -0.10 / -0.02 | |

(b) Still open (Q36-5 / 7 / 9 / 10 / 13 / 14 readings): **67 cells / 50 configurations**.

| Table | Configs | Change (in) | Note |
|---|---|---|---|
| 6402 | 15 | -0.12 to +0.14 | L26 + L27 |
| 1404 | 15 | +0.058 to +0.125 | body hex. The Brennan STEPs show OMi's hex |
| 0318 | 11 | +0.01 each | L1. OMi = MS51531D nominal |
| 5502 | 5 | -0.41 to +0.01 | -24-24-FG 3.05 -> 2.64, -20-20-FG 2.75 -> 2.38 |
| 2605 | 1 | +0.08 | |
| 6503 | 1 | +0.03 | |
| 0403 | 1 | -0.01 | |
| 6404 | 1 | +0.031 | |

**Excluded: 57 cells** (`A19_excluded.csv`):
- 2404 held: 27.
- 6565 lengths: 16 (A22 keep).
- Held in Task A: 10. Of these, 9 bores are wider than their port (A11), plus the 6405-20-16-O 1.000 placeholder.
- 6410 OMi length exactly 1.000: 4 (the placeholder pattern; OMi has since given the real lengths, which equal Air-Way).

## A20 - 1404 nut face = OMi overall length (W@HEX)
- 23 built configurations change, by -0.07 to +0.14.
- Biggest: 1404-24-24 2.55 -> 2.69, 1404-02-02 1.15 -> 1.08, 1404-24-20 2.61 -> 2.54.
- File: `A20_1404_nutface.csv`.

## A21 - 1404 bores back to Air-Way
- 18 cells in 17 configurations change, by -0.16 to +0.11. 1404-12-12 changes both D and D2.
- The values come from `omi_apply_20260925/originals_before_apply/DesignTable_1404.xlsx`, and all of them equal `07_RAW_EXTRACTS/1404.csv`.
- File: `A21_1404_bores.csv`.

## A23 - OMi = Air-Way, so the row can become VERIFIED
- 582 rows compared. 284 agree on every compared cell:
  - 81 are already VERIFIED.
  - 28 are 2404 (held).
  - 7 stay MISSING.
- That leaves **168 ASSUMED candidates: 131 clean**, plus 37 that have one cell on an unsettled reading.
- OMi covers 1-7 cells per row; the other cells stay single-source.
- File: `A23_verified_candidates.csv`.
