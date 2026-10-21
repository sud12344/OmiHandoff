# Brennan CAD portal lookup (2026-10-21, cloud)

Brennan's product pages ask CADENAS PARTcommunity whether a CAD model exists (`webapi.partcommunity.com/service/reversemap?catalog=brennan
&part=<pn>` - public, no login; the same call Brennan's own site makes). The answer is the model's parameter record: the values Brennan's
CAD is generated from. Downloading the STEP itself goes through a contact form + reCAPTCHA on brennaninc.com and an emailed zip - that
stays with the user.

| File | What |
|---|---|
| `pc_lookup.py` | the lookup (1 request / s, cached); variants: OMi number, known Brennan aliases, pass 2 also -FG / -NWO swapped |
| `cache.json` | every raw answer |
| `pc_results_pass1.csv` / `pc_results_pass2.csv` | per pass |
| `merge_results.py` -> `pc_final.csv` | one row per not-ready OMi part: match exact / alias / other part (forged <-> plain swap, not counted) / none, the CAD family, the parameter record |

## Result (1,022 not-ready parts)
- 612 exact + 81 alias = **693 have a Brennan CAD model**; 3 only as a different part (1703-08-08-FG / 1803-08-08-FG / 1803-32-32-FG:
  Brennan has the swept bent-tube 1703 / 1803, not a forged one); 326 none (incl. the 30 kits, 111 compression -M1 body-only numbers).
- The PC's 240-file download list: **217 exist, 23 do not** (struck through in `tools/_out/sources_20261021/STEP_CHECKLIST.md`).
- Compression: 89 complete fittings modelled (all C0318 / C0319 / C2403 / C2500, most C2405 / C2501 / C2502 / C6801; no C2404 at all).
- 4005 flange O-rings: 8 of 9 (I.D., W, material). Bent tubes: 66 of 68 (1704 family: TOD = tube OD?; 6701: R = bend radius?, THK).

## Checked
`BRENNAN_FS2403-08-08.stp` vs its record: A1D 0.378 = bore 0.378, A1THD 0.8125 = thread major, H 0.875 = hex (corners 1.011), FF 1.390 =
seal faces +-0.695. FS6400-08-08-O: L 1.441 vs STEP 1.459 = + the O-ring standing proud, as on FS2403.

## Not done (needs the user's yes)
Nothing here is written into a review table. Using the parameter records as a dimension source = Brennan data (`$PRP@DimSource` BRENNAN,
Air-Way first). The letter codes differ per CAD family and must be mapped against a real STEP of that family first (as above).

## Decoding (2026-10-21, user: "yes start decoding the 58 families") - `decode/`
- `decode_families.py` -> `decode_<family>.txt`, `family_codes.csv`: every record code vs the features measured on the family's STEPs on
  disk (84 families, 188 STEPs; OCP). With a chance test (the value shifted by +0.037 / -0.029 in must not match too): 1,193 of 1,544 codes
  DECODED, 159 ambiguous, 192 partial / no match.
- `catalog_match.py` -> `catalog_codes.csv`: 628 codes equal a named Brennan PDF-catalog column on the family's printed sizes.
- `map_columns.py` -> `column_map.csv`, `proposals.csv`, `differences.csv`: code -> review-table column, calibrated on the rows whose values
  are known (records of 1,315 of the 1,416 shipped parts fetched: `pc_results_shipped.csv`): 536 of 1,239 columns MAPPED (>= 3 rows,
  >= 90 % agree; a 2-decimal Air-Way value agrees with its Brennan rounding). Proposals = EMPTY cells of not-ready BUILD rows only.
- `review_pack.py` -> `BRENNAN_CELLS_for_review.xlsx`: **506 cells in 132 not-ready parts; 30 parts dimension-complete** (thread / port /
  seat columns from the end library by thread size, as on every built row); 64 still miss a bore / hex / leg whose mapping is a tie or weak;
  **61 differences** with filled cells (Air-Way stays; for information / OMi).
- Self-check: the differences reproduce the two known by hand (6801-04-02 leg 1.03 vs 0.92, 6801-12-12 ORB thread length 0.469 vs 0.410).
- FS2403 end (vs gen_straight2 FSM_MEAS -08 / -24): record EL = groove OD, DL = face dia, CL = relief dia, AL = end length; groove ID / depth
  not in the record but constant on all 10 measured dashes (0.102 / 0.052); thread start THDS not in the record -> the only reason left
  for the 6 FS2403 per-dash downloads.
- Not yet covered: families whose review table has no calibration rows (compression, bent tubes, most new FS tables) - map by hand from
  `decode_<family>.txt` + `catalog_codes.csv`.
