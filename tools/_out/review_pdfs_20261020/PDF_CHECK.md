# OMi "Review of Drawings" PDFs vs the Air-Way-first stage (2026-10-20)

Source: `07_RAW_EXTRACTS/omi_review_drawings_20261020/` (scanned, handwritten - page images in `png/`).
- `Review of Drawings.pdf` (20 pages): the 2026-09-26 dimension-check drawings, each dimension marked "AW = <Air-Way letter> <value>" /
  "BI = <Brennan value>".
- `Review of Drawings #2.pdf` (5 pages): 0318-08, 0403-08-08-UNPL, 1404-08-08, 1501-08-08-FG, 1405-08-08 - questions, no AW / BI table.

## Result: no AW / BI mark contradicts the stage
None of the 320 reverted cells and none of the 40 rows of the Triveni draft is on a drawn configuration (the drawings are -08 sizes). The
marks confirm the rule (Air-Way wins) and the -08 values:

| Drawing | Mark | Stage / table | Verdict |
|---|---|---|---|
| 1404-08-08 | "Brennan overall length is 1.89 - big difference" (drawing 1.94) | live 1.89 (OMi) -> stage **1.94** (Air-Way W) | stage = Air-Way, agrees |
| 1404-08-08 | "bore on both sides: MNPT .53, FP .45" | live D 0.45 / D2 0.53; stage C1 hex 1.00 -> 0.94 (Air-Way) | agrees (drawing showed the old 0.44) |
| 0318-08 | length 0.84 checked | live 0.85 (OMi) -> stage **0.84** | agrees |
| 1501-08-08-FG | "Brennan is 1.39, significant difference" (W3 1.34) | Air-Way -FG row W3 1.34 | Air-Way, agrees |
| 2501-08-08-FG | "AW M 1.31, BI 1.33" (drawing 1.33) | Air-Way prints **1.33 on the -FG row**, 1.31 on the plain 2501-8-8 row | drawing right - Triveni read the plain row |
| 5502-08-08-FG | "AW W 1.13, BI 1.062" (drawing 1.06) | Air-Way -FG row W 1.06, plain row 1.13 | drawing right - plain row read |
| 0403-08-08-UNPL | "D2 on AW is listed as 0.497 - double check" (drawing 0.504) | Air-Way 0403-8-8 UNPL D2 0.504; 0.497 = the "PF UNPL" row | drawing right |
| 5500-08-08-FG | "BI .875 ??" hex (drawing 0.88) | Air-Way Y 0.88 | rounding only |
| all others (2405 5000 5404 5405 6401 1405 2700 4404 5504 6801 2601 5600 6600 6803 2650 2403) | AW = BI = drawing | - | agree |

So: when OMi checks against Air-Way they sometimes read the plain row for a -FG part - say so in the email to Triveni.

## Drawing / naming feedback (not dimensions - for when drawings resume; user 2026-10-15 "no drawings now")
- Show the thread callout (e.g. 3/4-16 UNF-2B) and the cone angle (37 deg) on every drawing; 0318, 0403, 1404, 1405, 1501.
- 1404 / 1405: dimension both bores, one per end view; an L (thread / body) dimension is missing. 1501: M1 and C1 missing.
- 0318: "where did bore 0.568 & tap drill 0.6823 come from? Not on Air-Way or BI drawings" - they come from the thread standard /
  Brennan-measured nut, not from a table column: either drop them from the drawing or cite the source.
- 0403-08-08-UNPL: **"You can mention [unplated] in notes. Do not put in part#."** -> OMi wants the part number without UNPL. Affects the
  0403 configuration names (user / OMi decision before renaming; the OMi website list carries UNPL).
- 0403: Air-Way has an L7 dimension (Brennan does not) - not dimensioned on the drawing.
- 5000: "need a better diagram"; Air-Way lists a tap drill 0.70 (drawn as the bore). 5405: Air-Way tap drill 0.70; "BI only shows one".
- 2650: the right view is "missing the 4th side".

## The 40-row draft
`10_DRAWINGS/for_OMi_2026-10-20/AirWay_values_to_confirm_2026-10-20.xlsx` column I filled: all 40 rows "not settled by the PDFs" -> all
40 stay in the request. Delete column I before sending.
