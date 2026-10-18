# Dimension-check drawings 2026-09-26: review (for you, not for OM Industrial)

Four checkers each reviewed 5 of the 20 drawings. I re-checked their main points myself: the OMi rows for all 20,
the 6401 table, and renders of 6401, 1405 and 6803.

**Bottom line:** all 106 values on the 20 drawings match the tables the masters were built from. Where OMi has a
number, the model agrees with it or differs only by rounding. Nothing is dimensionally wrong. Before sending, fix one
misleading label on 6401, and a set of presentation problems: the template title block, text running over the sheet
border, the grey thread-helix circles and the 3-decimal display.

Files: `dimension_check_20260926\<config>.PDF` and the combined PDF (20 pages, text identical to the single PDFs).
The values the macro placed are in `dimension_check_20260926_results.json`; the final 6803 and 2650 versions are in
`_last2.json`. The checkers' evidence (renders, crops, scripts) is under `tools\_out\drawings_20260926\check_*\`.

## 1. Per drawing

"Table" = the SW2 row plus the review-table column. "OMi" = the Items sheet of `WebsitePartsInfo2026.xlsx`.
Values are in inches.

| # | Drawing | Shown | Table | OMi |
|---|---|---|---|---|
| 1 | 2403-08-08 | L 1.62, hex 0.81, bores 0.39 / 0.39 | match | no values |
| 2 | 2405-08-08 | L 1.79, hex 1.13, bores 0.39 / 0.39 (female end: through-bore, not the 0.70 port) | match | no values |
| 3 | 5000-08-08 | L 1.50, hex 1.13, bores 0.70 / 0.70 | match | no values |
| 4 | 5404-08-08 | L 1.89, hex 0.88, bores 0.53 / 0.53 | match | no values |
| 5 | 5405-08-08 | L 1.87, hex 1.13, bores 0.53 / 0.53 (female end: through-bore) | match | no values |
| 6 | 6401-08-08-O | L 1.55, hex 0.88, bores 0.39 / 0.39 | match | L 1.550 same; hex 0.875 and ORB ID 0.391 are rounding; **pipe-end label, see 3a** |
| 7 | 1405-08-08 | W1 1.83, hex 1.00, bores 0.45 / 0.45 | match | no values |
| 8 | 2700-08-08 | L 2.44, hex 1.00, bores 0.39 / 0.39 | match | no values |
| 9 | 4404-08-08 | L 2.60, hex 0.94, bores 0.43 / 0.43 | match | no values |
| 10 | 2501-08-08-FG | legs 1.33 / 1.47, hex 0.88, bores 0.39 / 0.53 | match | legs same; hex 0.875, IDs 0.391 / 0.531 = rounding |
| 11 | 5500-08-08-FG | legs 1.47 / 1.47, hex 0.88, bores 0.53 / 0.53 | match | legs same; hex 0.875, IDs 0.531 = rounding |
| 12 | 5502-08-08-FG | legs 1.47 / 1.23, hex 1.06, bores 0.53 / 0.53 | match | legs same; hex 1.062, ID 0.531 = rounding |
| 13 | 5504-08-08-FG | legs 1.23 / 1.23, hex 1.06, bores 0.70 / 0.70 (tap drill run to the centre: logged assumption) | match | no values |
| 14 | 1501-08-08-FG | legs 1.47 / 1.34 (to nut face), nut hex 1.00, body hex 0.88, bores 0.53 / 0.45 | match | no values |
| 15 | 6801-08-08-NWO-FG | legs 1.25 / 1.45, nut hex 0.88, body hex 0.75, bores 0.39 / 0.39 | match | no values |
| 16 | 2601-08-08-08-FG | legs 1.33 / 1.33 / 1.47, hex 0.88, bores 0.39 / 0.39 / 0.53 | match | legs same; hex 0.875, IDs 0.391 / 0.531 = rounding |
| 17 | 5600-08-08-08-FG | legs 1.47 x3, hex 0.88, bores 0.53 x3 | match | no values |
| 18 | 6600-08-08-08-FG | legs 1.25 / 1.25 / 1.38, nut hex 0.88, body hex 0.75, bores 0.39 x3 | match | no values |
| 19 | 6803-08-08-08-NWO-FG | legs 1.25 / 1.25 / 1.45, nut hex 0.88, body hex 0.75, bores 0.39 x3 | match | no values |
| 20 | 2650-08-08-08-08-FG | legs 1.25 x4, hex 0.75, bores 0.39 x3 (the -Y bore has no view) | match | no values |

## 2. Drawing value different from its table

**None.** All 106 values equal the SW2 row and the review-table column. The checkers verified this twice: once from the
label text, and once by measuring the drawn geometry in the PDF vectors (arrow spacing divided by the view scale, and
circle chords). Every measurement came within 0.001 in.

## 3. Model versus OMi's own numbers

**No difference beyond rounding.** OMi's file has dimensions for only 5 of the 20 parts: 6401, 2501, 5500, 5502 and
2601. For the other 15 the OMi row holds no numbers, so OM Industrial's check will be the first independent source. That
matters most for 5000, 5404 and 5405, which are ASSUMED (Air-Way only).

Things OM Industrial will probably query anyway:

- **a. 6401-08-08-O, pipe (NPTF) end: the drawing says Ø0.390, OMi Side 2 ID says 0.531.** The model is right: it has
  the 0.53 pipe-end bore, 0.931 deep (SW2 `DB@BORE_B` = 0.53, review D4 = 0.53). The macro's rule, "dimension the
  smallest bore seen from each end", put the label on the 0.39 through-bore behind it, and the 0.53 bore has no
  dimension. **Fix:** dimension the 0.53 pipe-end bore. The same label pattern appears on 2405, 5405 and 1405 (female
  ports; OMi has no value there) and on 5502, where the arrow does sit on the bore but a larger 0.70 circle surrounds
  it. A checker could read any of these as the port size.
- **b. Three decimals.** The drawings print 0.880, 1.060, 0.390 and 0.530, but the sources have 2 decimals. Next to
  OMi's 0.875 (7/8), 1.062, 0.391 and 0.531 these look like 0.005 errors, although by your rule they are rounding
  (affects 6401, 2501, 5500, 5502 and 2601). **Fix:** print 2 decimals, or add a note: "values from 2-place catalog
  data".
- **c. Typos in OMi's own file** (not in the drawings; worth telling them):
  - Row 803 (2601): the branch thread is `1/2-18 NPTF`. It should be 1/2-14.
  - Row 1154 (4404): Side 2 thread is `3/8-18 NPTF` on a 1/2 end.
  - Row 120 (1405): the swivel end says `1/2-14 NPTF`. The model and row 140 say NPSM.
  - Row 2160 (6801): "Male **Metric** O-Ring Boss" with a 3/4-16 UNF thread.
  - Rows 120 and 140: Excel turned the Side 2 Size `1/2` and a Parker cross-reference into dates.

## 4. Visual issues worth fixing (most important first)

1. **Title block is still the template, on all 20 sheets.** "<INSERT COMPANY NAME HERE>" appears twice in the
   proprietary notice. MATERIAL, FINISH, DRAWN, DATE, WEIGHT and REV are empty, and the tolerance lines show "±" with no
   value. There is no projection symbol, and the reference dimensions have no parentheses.
2. **Text over lines.**
   - 1405: the top border strikes through "1.830".
   - The left end-view bore label crosses the left border on 5404 (worst, 0.19 in over), 2403, 6401 and 1405. It
     touches the border on 2405, 5000 and 5405. On 1405 the right label crosses the right border too.
   - The DWG. NO. is too wide for its cell on 6803 (it overlaps the size letter "B"), 2650 and 6801.
3. **Grey circles from the suppressed thread helixes** show in the end views of 2405, 5000, 5404, 5405, 6401, 1405, 4404
   and 2501. They are probably also on 5502 and 5504, where the 0.70 port circle is drawn grey. On 2405 and 5405 they look like real edges (a counterbore or chamfer that does not exist), which
   contradicts "THREADS NOT SHOWN". **Fix:** hide curves in the views, or hide the helix features.
4. **Hex dimensions on the parts with a nut:**
   - 1501, 6801 and 6803: the dimension points at a hex that is hidden under the nut or washer in that view.
   - 1501, 6801, 6600 and 6803: two A/F dimensions with no "nut" or "body" label, and the smaller one sits outside the
     larger, so their extension lines cross.
   - 6600, 6803 and 2650: the 0.750 A/F lines up with the 3/4-16 thread OD and can be read as that.
5. **Ambiguous bore arrows:** see 3a. On 2403, 2700, 2501 and 6801 the arrow also lands where the 0.39 bore circle and
   the roughly 0.43 JIC nose circle almost touch. The leaders are long diagonals across the whole part.
6. **Layout (all 20):**
   - The end and side views sit about 0.6 in out of projection alignment, and no view has a label.
   - The straights carry an unlabelled second side view with hidden lines.
   - On the elbows, tees and cross the front view (the one showing the shape) has no dimensions.
   - The elbows' Left view shows only a grey tangent circle, which looks like a port.
   - 2650 has no view of the -Y bore.
7. **Minor:** the title-block title and the note line use different names on about 12 sheets (e.g. "HEX" / "HEXAGON",
   "90 DEG SWIVEL ELBOW" / the full description).

Key dimensions OM Industrial may miss (optional additions):

- hex lengths and end lengths
- female port tap drill 0.70 and depth 0.90
- ORB groove 0.66 x 0.094
- 1405 L1 1.50
- 1501 M1 1.01 (axis to stem tip)
- 6600 M10 0.96
- overall run length on the tees and cross
