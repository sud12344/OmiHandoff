# Raw Extracts — what each file contains

These are the **primary data**, pulled verbatim from source pages. The workbook is derived
from them. If a value in the workbook is ever in doubt, this is what to check it against.

All `.csv` files here are **pipe-delimited (`|`) with no header row**, one part per line.
Column meanings differ per shape because Air-Way labels dimensions differently for every
family — that is exactly why the workbook uses generic slots.

Every table below was extracted at least **twice independently and reconciled**. Where the
passes disagreed, a third pass broke the tie.

---

## `6400.csv` — Straight Thread Connector, 65 rows

Source: `parts.air-way.com/hydraulic-fittings/jic-and-beaded-hose-fittings/straight/6400-straight-thread-connector-series-89`
Air-Way series 89. Standard cited: SAE J514-1 070120 / MS51525 / MS39324.

```
1  Part #
2  B (1) UN/UNF-2A      thread, end 1
3  B (2) UN/UNF-2A      thread, end 2
4  L5                   overall length          → slot D1
5  C4                   HEX ACROSS FLATS        → slot D2
6  D (1)                bore, end 1             → slot D3
7  D (2)                bore, end 2             → slot D4
```

---

## `6801.csv` — 90° Straight Thread Elbow, 92 rows

Source: `.../jic-and-beaded-hose-fittings/90/6801-90-straight-thread-elbow-series-134`
Air-Way series 134. Standard: SAE J514 070220 / MS51527.

```
1  Part #
2  B (1) UN/UNF-2A
3  B (2) UN/UNF-2A
4  M                    → D1
5  M7                   → D2
6  C4                   NUT HEX (adjustable ORB end)   → D3
7  Y                    BODY WRENCH FLATS              → D4
8  D (1)                → D5
9  D (2)                → D6
```

---

## `6802.csv` — 45° Straight Thread Elbow, 56 rows

Source: `.../jic-and-beaded-hose-fittings/45/6802-45-straight-thread-elbow-series-158`
Air-Way series 158. Standard: SAE J514 070320 / MS51528.

Same column layout as 6801, except column 5 is `M8` rather than `M7`.

---

## `2501.csv` — 90° Male Elbow, 78 rows

Source: `.../jic-and-beaded-hose-fittings/90/2501-90-male-elbow-series-118`
Air-Way series 118. Standard: SAE J514 070202 / MS51504.

```
1  Part #
2  TUBE OD
3  B UN/UNF-2A          JIC 37° end
4  A NPTF               tapered pipe end
5  M    → D1     6  N → D2     7  Y → D3     8  D → D4     9  D1 → D5
```

**Two source anomalies, reproduced as printed rather than corrected:**

- Row order is not sorted. `2501-12-16-FG` appears after `2501-12-20`, and
  `2501-32-24-FG` before `2501-24-24-FG`. All three extraction passes reproduced this
  identically, so it is the page's own ordering.
- `2501-24-24` lists its B thread as **`1 7/8-14`** while every other -24 row, including
  `2501-24-24-FG`, lists `1 7/8-12`. Almost certainly a typo on the source page. **Left as
  printed. Do not silently correct it — confirm with the client.**

Note also that 2501 publishes **no hex column**. Its hex came from distributor data
(PressureConnections), unlike the other three shapes.

---

## `omi_2404.txt`

The 54 SKUs in OM Industrial's carbon steel catalog under root `2404`, one per line. Pulled
from their Shopify feed. **This is the authority on which parts exist** — Air-Way's table is
only the authority on dimensions.

Reconciliation result: 47 in both, 4 Air-Way-only (`DROP`), 7 OMi-only (no dimensional
source yet).

---

## `cs_roots.txt`

Pipe-delimited. First field is the OMi collection handle, remaining fields are the SKU roots
found in it. 206 roots across the six carbon steel subcategories.

## `cs_topologies.txt`

The 126 distinct shapes, one per line, after collapsing seal-family prefixes (`FS`, `C`,
`M`, `MFF`…) and length suffixes (`-L`, `-LL`, `-LN`…). **This is the master-model backlog.**

## `counts.txt` / `counts2.txt`

`SeriesID|VariantCount` for all 402 readable Air-Way series. From the full-catalog survey
that preceded the carbon-steel rescope — retained because it is the only complete picture of
the Air-Way range. 8 accessory series could not be read; their tables render client-side and
never populate for automated fetching.
