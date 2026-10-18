# Automatic dimension-check drawings from the masters - what was learned (2026-09-26)

Built for the user's request: 20 simple drawings (one -08 configuration from 20 series) for OM Industrial to check
dimensions, no thread callouts, in the style of the user's `om industrial\drawing\6600-04-04-04-FG-assembly-om.SLDDRW`
(B landscape, Top / section / end views, reference dimensions only).

## What was delivered
- `10_DRAWINGS\dimension_check_20260926\<config>.PDF` + `.SLDDRW` (20 parts), combined:
  `10_DRAWINGS\OMi_dimension_check_20_drawings_2026-09-26.pdf` (20 pages).
- Parts: 2403-08-08, 2405-08-08, 5000-08-08, 5404-08-08, 5405-08-08, 6401-08-08-O, 1405-08-08, 2700-08-08, 4404-08-08,
  2501-08-08-FG, 5500-08-08-FG, 5502-08-08-FG, 5504-08-08-FG, 1501-08-08-FG, 6801-08-08-NWO-FG, 2601-08-08-08-FG,
  5600-08-08-08-FG, 6600-08-08-08-FG, 6803-08-08-08-NWO-FG, 2650-08-08-08-08-FG - accepted masters in 11_MASTERS, chosen so
  that no pending Task A / Task B change touches them; one per series; no 45 deg elbows, no legacy HX masters.
- Labelled values per drawing: `10_DRAWINGS\dimension_check_20260926_results.json` (6803 / 2650: `..._last2.json`).
- Independent check (4 agents + summary, `10_DRAWINGS\dimension_check_20260926_REVIEW.md`): **all 106 values equal the SW2
  row each master was built from** (also re-measured from the PDF vectors, within 0.001 in). No wrong numbers.
  Presentation issues it found in the DELIVERED (v1) drawings - see "v2" below for what was changed afterwards:
  grey helix curves of the suppressed threads visible in end views; 6401 pipe end labelled with the 0.39 through-bore
  instead of its 0.53 bore (and female ports 2405/5405/1405 show the through-bore label inside the undimensioned port);
  on 1501/6801/6803 a hex dimension points at a hex hidden under the nut, and nut vs body A/F unlabelled; labels crossing
  the sheet border (1405 1.830, several end-view diameters); long DWG. NO. overlaps the size letter (6801, 6803, 2650);
  title block placeholders (<INSERT COMPANY NAME HERE>, MATERIAL empty); views unlabelled and ~0.6 in out of projection;
  3-place display of 2-place catalog values (0.880 vs OMi 0.875 - rounding only). The user said "it's fine for now".

## The scripts (tools\_out\drawings_20260926\scripts) - run inside the SolidWorks MCP `run_python`
- `geo.py` - reads a master's B-rep in its active configuration: leg end faces (planar, full circles, at the part end in
  +-X / +-Y), hex flat pairs, circles.
- `drw.py` - `make_drawing(part_path, cfg, out_dir, title, name)`. NOTE: the file now holds **v2** (rewritten after the
  check: opening + through-bore per end, PORT / THRU / NUT labels, visible-edge filter for hexes, labels clamped inside the
  border, view labels, company / material filled, curves hidden, end views aligned). v2 was run once on 6401 / 1501 / 1405
  (`trial_v2\`): bores and title block right, but the first visible-edge filter rejected every hex; it was changed to match
  edges by end-point coordinates and that version is **untested**. The delivered v1 drawings came from the earlier
  version of the file (same approach without those fixes).
- `run.py` - loops over jobs, closes only the documents it opened (never the user's).
- Job list with the design-table descriptions: `tools\_out\drawings_20260926\jobs_raw.json`.

## Layout used
B landscape (17 x 11 in, `C:\ProgramData\SolidWorks\SOLIDWORKS 2026\lang\english\sheetformat\b - landscape.slddrt`,
template `...\templates\Drawing.DRWDOT`). Main view top centre (Front for straights, Top for elbows / tees / crosses) with
lengths and hex A/F; below it the Front view with hidden lines shown (replaces a section, see gotcha 3); Right end view
right, Left end view left, with the bore diameters. Scale picked from {4, 3, 2, 3/2, 1, 3/4, 1/2} to fit.

## Model orientation of the generated masters (what the dimensions rely on)
- Straights: axis along +X from x = 0 to L; the body hex has a flat pair at +-Y (edge-on in the Front view).
- Elbows / tees / crosses: legs along +X, +Y (and -X, -Y) from the axis crossing at the origin; forged body flats at +-Z
  (edge-on in the Top view). A leg length = dimension from the face-on end circle of the other leg (its centre is the
  crossing) to the edge-on end circle of this leg.

## SolidWorks API gotchas found (Python / pywin32 through the MCP)
1. Arrays: `IMathUtility.CreatePoint` and `IView.Position` need a typed array,
   `VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, ...])`. A plain Python list is shifted (x lands in y) - views end
   up off the sheet, model-to-sheet points are wrong.
2. `IView.ModelToViewTransform` + `MultiplyTransform` (with typed points) gives sheet coordinates in metres - correct.
3. Section views: with a view active, `SketchManager.CreateLine` takes coordinates in the view's sketch space = MODEL
   units relative to the model origin (not sheet coordinates) - check with `IView.GetSectionLineInfo2` (first six numbers
   are the line in model inches x 39.37). Even with the line correctly on the axis, `CreateSectionViewAt4/5` and
   `CreateSectionView` produced a section view with NO cut on these masters (`GetFaceHatchCount` = 0, `SectionDepth` stuck at
   0.25 in) - unresolved. The user's own hand-made section (assembly) reports 5 hatches. Workaround used: Front view with
   hidden lines (`swHIDDEN_GREYED`).
4. `SetupSheet5` scale arguments must be floats (ints give 2:1), and SolidWorks auto-scales the sheet when the first view
   is inserted - call `ISheet.SetScale(num, den, True, False)` after inserting the views, then rebuild.
5. `IBody2.GetBodyBox` is loose (0.0025 in on 2405): find end faces from the planar faces themselves, with a tolerance.
6. Hex across flats: pair only opposite flats at the SAME distance from the axis - otherwise a 0.750 body flat and a 0.880
   nut flat make a fake (0.75 + 0.88) / 2 = 0.815 "hex" (happened on 6600 / 6801 / 6803; 1501 gave a fake 0.940).
7. End faces: require full circles (start = end point) and legs only along X / Y - the forged +-Z flats carry partial
   corner arcs and were mistaken for leg ends when the tolerance was loosened.
8. Dimensions: `IView.SelectEntity(edge, append)` with IEdge objects taken from the part document works;
   `AddHorizontalDimension2 / AddVerticalDimension2 / AddDiameterDimension2(x, y, 0)` at sheet coordinates; suffix / prefix
   with `IDisplayDimension.SetText(swDimensionTextSuffix / Prefix, text)`. Comparing edges with `ISldWorks.IsSame` against
   `IView.GetVisibleEntities2` did not match - compare end-point coordinates instead.
9. Title block: TITLE is linked to the model Description (long, overflows) - in `IDrawingDoc.EditTemplate()` walk the
   sheet-view notes and set `PropertyLinkedText`; DWG. NO. = file name (`SetHeightInPoints` 11-14 for long numbers).
   The description column holds thread sizes - use the name before the first comma (the user wants no thread callouts).
10. `IModelDoc2.InsertNote` for extra notes: activate the sheet first; a note inserted right after EditSheet may not
    appear (the v1 "HIDDEN LINES SHOWN" label never made it onto the sheet).
11. Hide thread helixes in drawings: document toggles `swDisplayCurves`, `swDisplaySketches`, ... = False and
    `swViewDisplayHideAllTypes` = True (added in v2, not yet verified in a PDF).

## Running it safely
- SolidWorks leaks about 0.5 GB per generated drawing: after ~15-20 drawings the modal "critically low on committed
  memory" dialog appears and every MCP call hangs (check `Get-Process sldworks` -> Responding False). Do batches of about 10
  and restart SolidWorks between batches (close without saving the scratch drawings; the user's documents stay untouched).
  Close Firefox etc. if committed memory is short (it was the main memory user on 2026-09-26).
- The MCP client aborts a `run_python` call after 1800 s without output - keep each call under that (10 drawings ~ 10 min).
- Render PDFs for checking with PyMuPDF (`import pymupdf`, installed 2026-09-26 with pypdf).
