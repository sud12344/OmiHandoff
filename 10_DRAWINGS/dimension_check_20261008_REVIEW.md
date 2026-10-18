# Dimension-check drawings 2026-10-08: review (for you, not for OM Industrial)

The task was one drawing for each of the 62 masters in `11_MASTERS`. **Only 6 were drawn.** SolidWorks ran out of
memory headroom after them: it reached 12.9 GB and free commit dropped to 6.25 GB, below the 6 GB-plus-one-drawing
stop line. It has to be restarted before the other 56 can be made. Only you can restart it, because it is the
3DEXPERIENCE launch.

**Bottom line:**
- All 31 values on the 6 drawings equal the design-table row of the configuration drawn. An independent check also
  measured every drawn value from the PDF vectors, and each one agreed with its label to within 0.002 in.
- One drawing shows the wrong part. **2502-08-08 is a DROP row**: OMi does not sell it, and OMi sells 2502-08-08-FG.
  That drawing is left out of the combined PDF and has to be redrawn.
- 2 more masters in the plan (2500HX, 2603HX) had the same wrong pick. Their -FG rows are now named for the next run.
- Most of the presentation problems from 2026-09-26 are fixed. Three small layout issues remain on the drawn sheets
  (section 4).

## Files

- `dimension_check_20261008\<config>.PDF` + `.SLDDRW`: the 6 drawings, including the wrong 2502-08-08. It is kept, but
  is not in the combined PDF.
- `OMi_dimension_check_all_masters_2026-10-08.pdf`: 6 pages.
  - Page 1 is a cover. It lists the 5 drawings in the set (part number, description, page) and the 57 series not drawn
    yet, with the configuration to be drawn for each.
  - Pages 2-6 hold 1405, 1501, 2650, 6401 and 6802. The text on each page is identical to its single PDF.
  - Bookmarks are set.
- The values the drawer placed: `tools\_out\drawings_20261008\results\<root>.json`. Renders: `...\renders\<root>.png`.
- The independent check: `tools\_out\drawings_20261008\check\toolsmith.md`, with crops in `check\tk\`.
- The pick-versus-ScopeAction check for all 62 masters: `check\pick_scope.json` (script `check\pick_scope.py`).
- Combine and verify scripts: `tools\_out\drawings_20261008\combine\`, including page renders `page01-06.png`.

## 1. Per drawing

Values are in inches.
- "Table" = the SW2 row plus the review-table column.
- "OMi" = sheet Items of `WebsitePartsInfo2026.xlsx`.
- "Measured" = taken from the PDF vectors by the checker.

| Page | Drawing | Shown | Table | Measured | OMi |
|---|---|---|---|---|---|
| 2 | 1405-08-08 | length 1.83, body hex 1.00, nut 1.00, tap drill 0.70 + bore 0.45 (female pipe end) | all match | all within 0.001 | row 120 has no dimensions |
| 3 | 1501-08-08-FG | legs 1.47 / 1.34 (to nut face), body hex 0.88, nut 1.00, bores 0.45 (swivel) / 0.53 (pipe) | all match | all within 0.002 | row 140 has no dimensions |
| 4 | 2650-08-08-08-08-FG | legs 1.25 x4, hex 0.75, bores 0.39 x4 (every end labelled) | all match | all within 0.001 | row 907 has no dimensions |
| 5 | 6401-08-08-O | length 1.55, hex 0.88, bores 0.39 (ORB) / 0.53 (pipe) | all match | all within 0.001 | L 1.550 / hex 0.875 / IDs 0.391 and 0.531: **same, or rounding only** |
| 6 | 6802-08-08-NWO-FG | legs 1.30 (ORB) / 0.98 (45 deg JIC), body hex 0.75, locknut 0.88, bores 0.39 x2 | all match | all within 0.001 | row 2223 has no dimensions |
| - | 2502-08-08 (**not in the combined PDF**) | legs 1.23 / 1.55, hex 1.13, tap drill 0.70, bores 0.39 / 0.39 | match the row, but the **row is DROP** | all within 0.002 | OMi sells 2502-08-08-FG instead: M 1.520 / L 1.230 / hex 1.062 / ID 0.391. The SW2 -FG row has 1.52 / 1.23 / 1.06 / 0.39, the same to rounding. |

- **No drawn value differs from its table.**
- Where OMi gives numbers (6401 only), the model differs only by rounding.
- On the other 4 parts in the set, OM Industrial's check will be the first independent source for those numbers.

## 2. What the check found, and what was fixed

The independent check ran after the drawings were made. No fix round followed it, so **nothing it found has been
fixed yet.** It found:

1. **2502HX: wrong configuration.** The plan picked the master's reference configuration, 2502-08-08. In the review
   table that row is "DROP: no matching OMi SKU in catalog feed".
   - Action taken: the sheet is left out of the combined PDF.
   - Still to do: redraw it as 2502-08-08-FG.
   - I then checked every pick in the plan against ScopeAction. Two more were DROP rows: **2500HX** (pick 2500-08-08,
     to be drawn as 2500-08-08-FG) and **2603HX** (pick 2603-08-08-08, to be drawn as 2603-08-08-08-FG). The other 59
     picks are BUILD rows. 5404N and 5406C are listed under their part-number spelling, and their rows are BUILD.
     `masters.json` was not edited; fix those three picks before the next run.
2. **1501: the HEX 0.88 dimension is attached to the hex hidden under the swivel nut.** The value is still right,
   because both hexes are 0.88. In the top view, though, its extension lines end inside the nut outline. It should be
   attached to the visible hex arm. The same rule probably affects 6801, 6803 and the other nut tees, which are not
   drawn yet.
3. **6802: the last note line runs into the title block.** "...VIEW A LOOKS ALONG THE 45 DEG LEG." crosses the frame
   line. The drawer's own layout check flagged this, but the sheet was not regenerated.
4. **Labels touching the part outline:**
   - 2502 left view: "BORE" sits on the body edge, and "Ø0" crosses an edge.
   - 2650 left and right views: the Ø touches the hex corner.
5. **Two wordings of the decimals note.** 6401 and 6802 say "VALUES ARE SHOWN WITH THE DECIMALS..." and the other 4
   sheets say "VALUES CARRY THE DECIMALS...". The meaning is the same.

**Fixed since 2026-09-26** (confirmed on all 6 sheets):
- 2 decimals. 0.88 no longer looks like a 0.005 error against OMi's 0.875.
- No grey thread-helix circles.
- No text over the sheet border.
- The 6401 pipe end is now labelled 0.53. This was the misleading 0.39 label from 09-26.
- 2650 has a view of every end.
- Every view is labelled.
- The nut and body hex are labelled NUT / HEX, and the two dimensions no longer cross.
- The title block is filled: title, DWG NO = configuration, CARBON STEEL, OM INDUSTRIAL in the notice. The long DWG NO
  shrinks to fit its cell.
- No thread callouts.

## 3. Masters not drawn, and why

56 of the 62 masters are not drawn. 2502 needs a redraw. Reasons:

- **9 tried, then stopped:** 0318, 0403, 1404, 1700, 2403, 2405, 2406, 2408 and 2500HX.
  - These were stopped before drawing. The sldworks.exe process (PID 29240, started 2026-10-08 7:18 PM) held 12.9 GB,
    and free commit was 6.25 GB. One drawing uses 0.4 to 1 GB, so the next drawing would have crossed the 6 GB stop
    line.
- **47 not reached**, for the same reason:
  - 2501, 2503, 2601, 2602, 2603HX, 2605
  - 2700-2706 (7 masters)
  - 4404, 4604, 5000, 5404N, 5404, 5405, 5406C, 5406P, 5406
  - 5500, 5502, 5504, 5600, 5602, 5604, 5605
  - 6402, 6404, 6405, 6408, 6410, 6500-6506 (7 masters), 6565
  - 6600, 6602, 6801, 6803, 6804
- **Next step:**
  1. Restart SolidWorks.
  2. Fix the three DROP picks: 2500HX, 2502HX and 2603HX, to their -FG rows.
  3. Apply the 1501 hex-attachment fix and the note wrap.
  4. Draw the rest in batches of about 5, checking memory between batches. At ~0.5 GB each, 57 drawings need at least
     one more restart along the way.

The cover page of the combined PDF lists every series not drawn yet, with the configuration that will be drawn.

## 4. Presentation notes

- **Ready to show:** 1405, 2650 and 6401.
- **Show with a remark, or wait for the fix:**
  - 1501: the hex dimension points under the nut.
  - 6802: the note line touches the title block.
- **Minor, all sheets:**
  - The template's tolerance block still shows "±" with no values, next to the note "NO TOLERANCES".
  - DRAWN, DATE, FINISH, WEIGHT and REV are empty.
  - There is no projection symbol.
- **Minor, per sheet:**
  - 1405: the swivel-end view has no bore label. It is the same 0.45 through-bore.
  - 1405: the two left-view leaders cross at the centre.
  - 6802: the VIEW A arrow sits on the JIC hex.
- **Data notes for you, not drawing problems:**
  - The SW2 description of 2502 reads "90 deg Female Pipe Elbow" and leaves out the male JIC end. OMi calls it
    "MJ - FP Elbow Forged". The sheet title follows the description.
  - OMi row 2223 (6802) says "Male **Metric** O-Ring Boss" with a 3/4-16 UNF thread, the same typo as on 6801.
  - OMi row 120 (1405) gives the swivel thread as NPTF where the model and row 140 say NPSM. This was already reported
    on 09-26.
