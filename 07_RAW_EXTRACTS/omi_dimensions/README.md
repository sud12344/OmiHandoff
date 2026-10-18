# OMi dimensions file (received 2026-09-25)

`WebsitePartsInfo2026.xlsx` is an unchanged copy of the file the user provided on 2026-09-25 as "an Excel file with all the
dimensions OMi uses". The original is at `OMi_Handoff\WebsitePartsInfo2026.xlsx`. The copy was made with its timestamp kept.
Always read this copy.

| | |
|---|---|
| SHA256 (original and copy, identical) | `e5109342e1411300a1cd85d790ab8f1a022f8d83c772508e63af37d4ad291840` |
| Size | 1,373,387 bytes |
| Format | .xlsx; no conversion needed |

## Contents, as read on 2026-09-25 (openpyxl, data_only True and False)

- **Sheet `Items`**, range A1:BE7306. Row 1 is the header: 39 named columns A..AM, and AN..BE are empty. Row 2 is a note
  ("Need drawings done first") and row 3 is blank. Rows 4..7306 hold 7,303 items (all materials: carbon steel, stainless
  `SS-`, brass `B-`).
  - No hidden rows or columns and no merged cells. Panes are frozen at B3.
  - Dimension cells are TEXT (number format `@`), e.g. `"0.438"`: Overall Length, Body Diameter, M 1 Size, M 2 Size,
    L 1 Size, L 2 Size (empty), Hex Flat, Side 1..4 ID, Nut Hex 1/2.
  - Units are inches, as decimals; no min/max or tolerance columns.
  - 13,760 formula cells, every one with a cached value. Most are Google-Sheets exports (`__xludf.DUMMYFUNCTION`). They
    fill Series, Series Description, Shape, Shape Type, Side 1 Connection Type, Side 1..4 Size (= the n-th dash of the part
    number / 16) and the Aeroquip / Parker / SAE cross references. None of the dimension columns is a formula.
  - 150 cells hold dates instead of text (Excel turned fractions like `3/4` into dates). 108 of them are in Side 2 Size and
    38 in Cross Reference Parker.
- **Sheet `Sheet1`**: a 95-row lookup table of end type -> nominal size -> thread callout (female/male pipe, Komatsu, JIS,
  BSPT/BSPP, metric bite type). It has no part numbers and no dimensions.

The audit that uses this file is `00_DOCS/OMi_Dimension_Audit_2026-09-25.md` / `.xlsx`. Its scripts and intermediates are
in `tools/_out/omi_audit/`.
