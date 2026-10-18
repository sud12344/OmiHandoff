# O-rings, bent-tube elbows, flareless nut + sleeve: scope (2026-10-14)

## 1. What OMi said
2026-10-14 (user, from OMi's answer to question 8 of `10_DRAWINGS/for_OMi_2026-10-09/Email_to_OMi_2026-10-09.txt`): **"Yes we
need drawings of ORings, Bent Tube, and Flareless nuts and sleeves."** Our drawings are made from the 3D masters, so this means
new masters for these three families first, then dimension-check drawings like the 62 of 2026-10-09.

Settled by it (keys of `tools/_out/questions_20261008/merged.json`): `scope-o-rings` (Q-SCOPE-ORING, Q36-20) = yes;
`scope-bent-tubes` (Q-SCOPE-TUBE, Q36-21) = yes, now, own masters; `scope-flareless` (Q-NEW-FLARELESS-N3) = now.
My reading, to confirm with the user: for these families only it also settles SOP step 5 ("a fitting without a hex cannot be
modelled" - an O-ring or a sleeve has no hex) and the carbon-steel-only rule (O-rings are Buna-N / Viton rubber). `Q-SOP5` for
plugs, collars etc. stays open.

## 2. The parts
Enumerated from OMi's parts file (`WebsitePartsInfo2026.xlsx` Items) and the website feed (`07_RAW_EXTRACTS/omi_feed/omi_skus_all.txt`
= the review tables); list: `tools/_out/omi_request_20261014/scope_parts.csv` (`build_request.py`).

| Family | Series | On OMi's website (review-table rows) | Only in OMi's parts file |
|---|---|---|---|
| O-rings | 4000 Buna | 11 (-02 -03 -04 -06 -08 -10 -12 -16 -20 -24 -32) | 2 (-05 -14) |
| | 4001 Viton | 10 (-02 -04 -06 -08 -10 -12 -16 -20 -24 -32) | 3 (-03 -05 -14) |
| | 4005 flange O-ring | 9 (-08 -10 -12 -16 -20 -24 -32 -40 -48) | - |
| Bent-tube ("swept") elbows | 1703-..-Tube, MJ x code 61 flange, 45 deg | 13 | 4 (08-12, 12-08, 16-12, 32-24) |
| | 1704-..-Tube, MJ x code 61 flange, 90 deg | 19 | - |
| | 1803-..-Tube, MJ x code 62 flange, 45 deg | 13 | - |
| | 1804-..-Tube, MJ x code 62 flange, 90 deg | 16 | - |
| | 6701, MJ x FJS swivel, 90 deg (+ 6701-L-16-16) | 7 | 3 (10-10, 24-24, 32-32) |
| Flareless | 0618 JIC flareless tube nut | 1 (0618-08) | 1 (0618-06) |
| | 0619 JIC flareless tube sleeve | 2 (0619-06, -08) | - |
| **Total** | | **101** (30 O-rings, 68 bent tube, 3 flareless) | **13** (question 28: do they sell them? asked in the request) |

All 101 review-table rows are BUILD / MISSING (skeleton tables; 1703 / 1704 also hold their forged -FG rows, which are not part
of this scope).

## 2a. Update 2026-10-14 (later): "use airway sizes" + first model types built (staged)
- User: **"use airway sizes"** - Air-Way is the source wherever it has these parts (OMi first, Air-Way fills, as everywhere).
  Air-Way s218 lists OMi's own part numbers 4000-2 ... -32 (Buna-N) and 4001-2 ... -32 (Viton) with I.D., W, hardness 90:
  **the 21 website O-rings 4000 / 4001 now have sizes** (ASSUMED). Air-Way s115 (1701-61, code 61 bent-tube flange elbow) has
  4 sizes = 1704-12-12 / -16-20 / -24-20 / -24-24-Tube (lengths M3 / N4, hex, bore, head dia; no bend radius or tube size).
  No Air-Way page for 4005, the other bent tubes or 0618 / 0619. Section 3 below is the earlier picture.
- Built and dry-run in SolidWorks (`tools/_out/newtypes_20261014/README.md`): O-ring master 4000 (21 configurations, 0 FAIL);
  sleeve model type on TEST rows (0319T, 0 FAIL). The OMi request no longer asks for the 4000 / 4001 sizes.

## 3. Where the sizes can come from
- **OMi's parts file:** names and threads only - no size for any of the 114.
- **Air-Way:** no page for any of these series.
- **Brennan:** the catalogs print some values (TFA p38 6701 / 6701-L M, L, hexes; Flange p4-6 swept 1703 / 1704 / 1803 / 1804
  L1, L2, A/F; TFA p68 V0318 nut length / hex, V0319 sleeve length) - **not usable** ("You cannot use Brennan data as your own",
  2026-10-08). Bend radius, tube OD and wall are not printed anyway. Brennan 3D files may give the SHAPE ("shape is fine");
  none of these parts' files is in `09_STEP_FILES` (there: 0319-08 = the JIC sleeve, and forged 1703 / 1704 / 1804 -FG).
- **O-rings: the AS568 standard.** O-ring sizes are an industry standard, not a supplier's design. OMi's 4000 / 4001 dash
  numbers (-02 -03 -04 -05 -06 -08 -10 -12 -14 -16 -20 -24 -32 in their file) are exactly the 13 O-ring-boss sizes AS568 -902 ...
  -932 (Parker ORD 5700 table 4-4, already in `07_RAW_EXTRACTS/Report_ORB_groove_ORD5700.md`). If OMi confirms each part's
  size number and the user allows the standard table as the source (Q-NEW-ORINGSRC), the inside diameter and cross-section
  come from the published AS568 table. 4005: code 61 or 62 must come from OMi (Q-NEW-4005CODE; -40 / -48 suggest code 61 -
  code 62 flanges stop at 2 in, also in Brennan's tables - but OMi decides).
- **Everything else must come from OMi** (request drafted, section 5).

## 4. What has to be built (none of it exists yet)
| Model type | Parts | Masters | Reuses | New work | Size |
|---|---|---|---|---|---|
| O-ring | 30 (+5) | 1 (4000 + 4001 + 4005; material per row) | - | ring of round section (revolved circle); material Buna-N / Viton, not carbon steel | small |
| Flareless nut 0618 | 1 (+1) | 1 | `gen_straight2.py` 0318 JIC tube nut (UNFF end, hex, MS51531 inside) | inside seat for the sleeve (shape from a Brennan V0318 file) | small |
| Flareless sleeve 0619 | 2 | 1 | - | hexless sleeve module: revolved profile with the cutting edge (shape from V0319) | small-medium |
| Bent-tube elbows | 68 (+7) | 3: 45 deg MJ x flange (1703T + 1803T), 90 deg MJ x flange (1704T + 1804T), 6701 (+ 6701-L) | JIC male end library; code 61 head (`FLG61` module of 1700); code 62 head (wave-1 FLANGE62, unmerged); swivel-nut end (6500 family) - Q-TRANSFER-ENDLIB = yes | new generator: tube swept along line - bend - line, end pieces joined to it; dofcheck / allcfg / drawing logic for a curved part | large |
| Drawings | about 10 pages (one per series) | - | `tools/_out/drawings_20261008/scripts` drw3 / geo3 | new recipes: ring (ID, OD, section), sleeve, bent tube (centre-line legs, bend radius, tube OD); title block material for rubber | medium |

Optional, recommended: **0319 JIC tube sleeve** (12 parts, not flareless but the same kind of part as 0619). Its sizes exist
(Air-Way s48 length + OD, OMi file length + ID, `DesignTable_0319.xlsx` ASSUMED) and its shape file `BRENNAN_0319-08.stp` is in
the repo; it waits only for the no-hex exception. With the sleeve module built for 0619 it comes almost free.

## 5. What is needed
**From OMi** (drafted 2026-10-14, NOT sent - the user sends it): `10_DRAWINGS/for_OMi_2026-10-14/Email_to_OMi_2026-10-14.txt` +
`OMi_sizes_Orings_BentTube_Flareless_2026-10-14.xlsx` (tabs O-rings / Bent-tube elbows / Flareless nut + sleeve / What the columns
mean; built by `tools/_out/omi_request_20261014/build_request.py`):
- O-rings: the AS568 number of each part (our guess -9xx printed for 4000 / 4001, to confirm) or ID + cross-section; material +
  hardness; 4005 code 61 or 62.
- Bent tubes: tube OD + wall, bend radius, M 1 / L 1 (crossing of the centre lines to the JIC end / to the flange face or
  swivel end), JIC end-piece hex, 6701 swivel nut hex, flange head diameter + thickness - or the supplier drawing per series.
- Flareless: length, hex, inside / outside diameters, shape of the nut's inside and the sleeve's front edge (drawing / photo).
- Whether they sell the 13 parts that are only in their parts file; one drawing per series or one per part number.

**From the user:**
1. Send the request.
2. Decide Q-NEW-ORINGSRC: O-ring sizes from the published AS568 table once OMi confirms each part's size number (recommended:
   it is the industry standard, not Brennan's data) - or OMi must send every inside diameter and cross-section.
3. Download 5 Brennan 3D files, for SHAPE only (Brennan numbers - the swept parts have no "-Tube" suffix there): 1704-16-16
   (swept 90 deg, code 61), 1803-16-16 (swept 45 deg, code 62), 6701-08-08, V0318-08, V0319-08 (STEP-STAGE-S-PILOT,
   Q-NEW-F3-FLARELESS-ALIAS now only "is V0318 / V0319 the same kind of part" - same description and threads).
   2026-10-15: plus one Brennan file with a code 62 flange head per flange size -12 / -20 / -24 / -32 (e.g. the code 62 plugs
   1824-12 / -20 / -24 / -32), SHAPE only (head thickness, O-ring groove): -08 is on disk, -16 comes with 1803-16-16. Without them
   28 of the 29 1803 / 1804 -Tube parts stay blocked (the model type itself works: the code 62 -08 head builds).
4. Include 0319 (optional, above)?

**My work** (no OMi data needed to start): build the three new model types on TEST rows (never shipped) with SolidWorks dry
runs - O-ring first (smallest), then sleeve + nut, then the bent-tube generator - and the drawing recipes. When OMi's sizes
arrive: fill the review tables (sources cited in `$PRP@AxialSource`, ASSUMED), generate, run the checks, dry-run, stage in
`11_MASTERS_NEW`, ship as a batch on "ship batch", then the drawings for OMi.

## 6. Not to forget
- Batch 16 is still waiting (staged 2026-10-09: wave 1, batch-15 leftovers, JIC tees, 2404, 5405 + the corner-puck fix; the
  puck-fix dry runs were interrupted - `00_DOCS/NEXT_SESSION_PROMPT_2026-10-10.md`).
- The forged 1703 / 1704 / 1803 / 1804 -FG rows are a different job (FLG61LEG / FLANGE62; they need OMi sizes too - most are
  already on the 2026-10-09 list of 226).
