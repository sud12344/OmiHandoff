# OMi Hydraulic Fitting CAD Library — Project Handoff

**Client:** OM Industrial Products Corp. (omindustrial.com), Houston TX
**Handoff date:** 2026-08-07
**Purpose of this folder:** everything needed to resume the project in a fresh session with no loss of context.

> **If you are an AI assistant picking this up:** read this file completely, then
> `08_SKILL/unpacked/SKILL.md`, then `OMi_SOP_NewSeries.md`. Install the skill in
> `08_SKILL/` if you can — it encodes the conventions so they don't drift.

---

## 1. What the project is

Build a CAD library for OM Industrial's **carbon steel hydraulic fitting** range:
**2,535 parts**. For every part the client needs a 3D model, a 2D drawing, and a
populated spec document.

Doing that part-by-part is impossible. The strategy is to build a small number of
**parametric master models**, drive them from **one spreadsheet**, and generate everything
else automatically.

### The single most important fact

**2,535 parts collapse to 126 distinct shapes.**

The catalog has 206 SKU roots, but `2404`, `FS2404` (O-ring face seal), `C2404`
(compression) and `2404-L` (long) are the *same geometry* — they differ only in seal family
and length. Those are **columns in a spreadsheet**, not separate models.

So: **126 master models → 2,535 parts.** About 20 parts per master.

**If anyone starts building a second master for the same shape, stop them.**

---

## 2. Current status

| | |
|---|---|
| Shapes with dimensional data | **5 of 126** (2404, 6400, 6801, 6802, 2501) |
| Parts with dimensions captured | **345 of 2,535** |
| Master models built | **0 — the 6400 is in progress, client-side** |
| Pipeline built and proven | **Yes** — drawings and spec sheets generated end to end |

**The bottleneck is no longer tooling. It is (a) data entry across 121 more shapes, and
(b) the client building master models in SolidWorks.**

---

## 3. Client environment and confirmed decisions

- **SOLIDWORKS 2026 Standard.** No Task Scheduler — all batching must be pure VBA.
- **DriveWorksXpress** is available but deliberately **not used**. It is a one-off
  configurator, not a batch generator.
- **Part number format:** `{shape}-{JIC dash}-{NPTF dash}`, each zero-padded to two digits
  → `2404-08-06`. **Confirmed by client.**
- **`D` belongs to the JIC end, `D1` to the NPTF end.** **Confirmed by client.**
- **Threads:** real helical geometry must appear **in drawings**, but must NOT be in the
  saved model or the exported STEP. Solved by suppressing thread features and having the
  macro toggle them. **Client requirement, confirmed.**
- **Scope:** carbon steel only. Brass, stainless, international/metric, hose, crimp
  fittings, live swivels and kits are **out of scope**.

---

## 4. Where the data comes from — two authorities, never confuse them

| Question | Source |
|---|---|
| **Which parts exist?** | The **OMi catalog** — `omindustrial.com/collections/<handle>/products.json?limit=50&page=N` |
| **What are their dimensions?** | **Air-Way Manufacturing** (`parts.air-way.com`), cross-checked against a second manufacturer |

Air-Way is used because OMi's range mirrors it dimensionally. But the two catalogs are
**not identical**. On the 2404 pilot: 4 Air-Way parts are not OMi products, and 7 OMi
products are absent from Air-Way's table entirely.

Every part row therefore carries a `ScopeAction` of `BUILD` or `DROP`.

### Extraction warnings, learned the hard way

- **The Air-Way pages misreport their own row counts.** The same 51-row table was variously
  reported as 54, 55 and 53. The *enumerated rows* were byte-identical every time.
  **Always extract twice and compare the row sets, never the stated total.**
- Counts above ~20 rows are **systematically overcounted** on a single pass.
- **The Shopify JSON feed silently truncates.** At `limit=250` it returns ~27% of records
  while appearing to succeed. **Use `limit=50`.** Even then it drops 1–5 records per page
  deterministically — about 76 of 1,672 adapter SKUs were never captured.
- **The clean fix for the SKU gap:** ask the client to export their product list from
  Shopify Admin as CSV. Two minutes of their time, and it is authoritative.

---

## 5. The files in this folder

### `01_MASTER_DATA/`

**`OMi_Fitting_Library_MasterData_v1.xlsx` — the single source of truth.** Everything else
reads from it. Sheets:

| Sheet | What it holds |
|---|---|
| `_README` | Legend, colour conventions, data-status meanings |
| `CarbonSteel_Scope` | The 2,535-part scope, by subcategory |
| `Parts_v2` | **The live parts table.** 291 rows across 6400/6801/6802/2501 |
| `Topologies` | All 126 shapes with a build-status column — the backlog |
| `DimensionMap` | Which generic slot holds which catalog letter, per shape |
| `StandardsData` | Pressure, material, finish, temperature — with every source cited |
| `EndGeometry` | O-ring groove and flare cone dimensions by dash size |
| `Parts` | The original 2404 pilot, on the older schema (see §8) |
| `Scope` | Variant counts across all 410 Air-Way series |
| `DashSizes`, `PipeThreads` | Thread lookups |
| `Standards` | Standards register, with what each does and does not govern |
| `QA_Log` | Every cross-check performed, with severity and action |
| `Series` | All 410 Air-Way series, source URLs, variant counts |

`AirWay_Series_Survey.xlsx` is the raw 410-series survey that preceded the rescope.

### `02_TEMPLATES/`

- `OMi_DrawingTemplate_A4.pdf` — **client's original**, unmodified
- `OMi_DrawingTemplate_Pro_A4.pdf` — same border, logo and title block, extended with a
  document-control strip, tolerance block, third-angle symbol, tabulated dimension table.
  **144 named form fields.**
- `OMi_SpecSheet_Template.pdf` — 41 form fields, named identically to spreadsheet columns

### `03_SCRIPTS/`

- **`OMi_BatchDrawings.bas`** — the SolidWorks macro. Per configuration: activates it,
  exports STEP with threads suppressed, unsuppresses threads, builds the drawing, exports
  PDF, re-suppresses. `DRY_RUN = True` by default.
- `fill_specsheets.py` — one spec sheet per part
- `fill_drawing.py` — one tabulated drawing per shape, auto-splits past 18 rows
- `mkdt.py` — generates SolidWorks design tables from the workbook
- `make_template.py`, `make_drawing_template.py` — rebuild the PDF templates
- `build_v2.py` — how `Parts_v2` was constructed

### `04_DESIGN_TABLES/`

`DesignTable_6400.xlsx` — 65 configurations, zero blocked rows. Ready to insert.
**Note:** needs regenerating to match the client's final dimension names (see §8).

### `05_DIAGRAMS/`

**`6400_final_profile.png` is the current, correct one.** Full sketch profile with every
dimension and its SolidWorks name. The others are earlier, superseded versions.

### `06_SAMPLE_OUTPUT/`

Real generated output, proving the pipeline works.

### `07_RAW_EXTRACTS/`

Verbatim dimension tables as pulled from Air-Way, plus SKU lists and variant counts. These
are the primary data — the workbook is derived from them.

### `08_SKILL/`

`omi-fitting-library.skill` — install this. It carries the conventions between sessions.
`unpacked/` is the same content readable directly.

---

## 6. The conventions (do not change these casually)

### Dimension naming

Every driving dimension lives in **one sketch named exactly `DRIVE`**.

```
D1 … D6      generic slots — hold Air-Way catalog letters, which
             mean different things on different shapes
HEXA HEXB    hex across flats
SEATB        seat angle
THD_EndA     thread features — named by prefix, kept SUPPRESSED
THD_EndB
```

**Why generic slots:** Air-Way uses a different letter set for every family — 2404 is
L/C/D/D1, 6801 is M/M7/C4/Y/D(1)/D(2), 6400 is L5/C4/D(1)/D(2). Naming SolidWorks
dimensions after catalog letters would require a different design table and macro for
roughly every third shape. Generic slots mean all 126 masters expose an identical header
set. `DimensionMap` records what each slot means.

**Exception:** dimensions that depend only on dash size — O-ring groove, flare cone — get
**semantic names** (`ORB_GRVDIA`, `JIC_CONEDIA`, …) because their meaning genuinely is
universal.

### The two release gates

Both are enforced by the macro **and** the Python scripts. **Do not disable them.**

```
ScopeAction = DROP        →  never emitted, not an OMi product
DataStatus  = MISSING     →  blocked, no source for the data
DataStatus  = ASSUMED     →  single source; auto-stamped "not released for production"
DataStatus  = VERIFIED    →  2+ independent sources agree
```

### Never fabricate

No dimension, thread spec, tolerance, material or part number enters the dataset without a
cited source. If there is no source, the cell stays empty and the row is `MISSING`. Every
value in the workbook is labelled as verified fact, assumption, or looked-up with its
source.

---

## 7. Key findings worth not rediscovering

**Air-Way publishes hex sizes — under the letter `C` or `C4`.** This was missed initially
and a whole research pass was spent sourcing hex from distributors. The distributor data
then *matched* the `C4` column, which is how it was caught. **Use the catalog column** — it
is per-part, so it is correct on mismatched sizes where a dash-keyed lookup table is wrong.

**SAE J514/1 does fix body dimensions**, not just thread and seat. Its scope reads *"general
and dimensional specifications for 37 degree flared tube fittings"* and it publishes hex
tolerances. Catalog dimensions are genuinely checkable against it.

**Monolithic SAE J514 was cancelled 2024-11-22**, split into J514/1 (37° flared), /2
(flareless), /3 (NPTF adapters). Every free copy online is the superseded edition.

**Air-Way's L values are independently corroborated.** 27 of 29 comparable 2404 rows match
Parker's Catalog 4300 exactly. Two differ by 0.01".

**The pressure tables disagree.** Parker's run 30–50% higher than the generic SAE-style
table at every size. The workbook uses the **generic, conservative** figures — two
independent sources agree on them and they are not tied to a competitor's product. Both
tables are in `StandardsData`. **This is a business decision the client may want to revisit.**

**Fitting shape does not change the pressure rating; end type does.** On a two-end fitting
the lower-rated end governs.

---

## 8. Open items — read before continuing

### Blocking

1. **121 of 126 shapes have no dimensional data.** This is the bulk of the remaining work.
2. **ORB thread length is unsourced.** No manufacturer publishes it — Parker's drawing says
   only "full threads to this point." The value in use (0.466 for a -08) is back-derived
   from the overall length. It corroborates against the published port thread depth (0.560
   vs 0.562) but **should be checked against a physical sample.**
3. **No ORB temperature limit found.** The −65°F/+400°F figure applies to the metal flare
   joint only. An O-ring joint is limited by the elastomer. Needs the client's seal supplier.

### Needs tidying

4. **`DesignTable_6400.xlsx` needs regenerating** once the client's master is finished — to
   match their final dimension names, drop the `BEND` column (straights don't need it), and
   add the end-geometry columns.
5. **2404 is still on the old schema** in the `Parts` sheet while the other four shapes are
   on `Parts_v2`. Migrate it.
6. **~76 adapter SKUs never captured.** Fixed by a Shopify CSV export from the client.
7. **13 parts have no hex** — odd dash sizes (-3, -5, -14) that distributors don't stock.
8. **-20, -24, -32 flare cone data is thin.** Cone diameter comes from an ISO metric table
   converted to inches; seat and thread lengths for those sizes were not found at all.
9. **Phase 3 batch plan and QA checklist not written.**

---

## 9. Where the client got to

They are **part-way through building the 6400 master model** in SolidWorks.

Completed: the profile sketch with all five length dimensions applied and the overall
1.480. Not yet applied: the six diameter dimensions and the 37° angle.

**Two corrections were issued after they started, prompted by the client comparing the model
against a product photo. `05_DIAGRAMS/6400_final_profile.png` reflects both.**

The corrected geometry is **7 sections**, not 5:

```
1  ORB thread      0.466   Ø0.750      ORB_THDL
2  O-ring groove   0.094   Ø0.660      ORB_GRVW / ORB_GRVDIA
3  body → hex      0.263   Ø1.0162     DERIVED / BODYDIA
4  JIC cylinder    0.408   Ø0.750      JIC_CYL / THDMAJ_B
5  cone            0.155   Ø0.659→Ø0.426  JIC_SEATL / JIC_CONEDIA
6  nose land       0.094   Ø0.426      JIC_NOSEL / derived from the 37°
                   ─────
                   1.480               D1
   bore, through   Ø0.390              D3
   hex across flats Ø0.880             HEXB (separate sketch named HEX)
```

**Only 0.310 of the 0.408 JIC cylinder is threaded**, leaving 0.098 bare against the hex —
thread runout relief, visible on the product photo. There is a matching relief at the ORB
end that is not yet quantified.

The **nose land** was confirmed by arithmetic: `0.094 + 0.155 + 0.310 + 0.098 = 0.657`,
exactly the published hex-face-to-tip length for a -08.

### Corrections already issued to the client — don't re-issue the old advice

- Do **not** make the corner of the profile coincident with the origin. That would put the
  bore on the centreline and produce a solid part with no hole. Lock the **left vertical
  line** to the Y axis instead.
- The SolidWorks polygon must use **Inscribed circle**, not circumscribed. Inscribed gives
  across-flats.
- Do **not** use an equation to drive `BODYDIA` from `HEXB`. `DRIVE` rebuilds before the
  `HEX` sketch exists, so it is a forward reference and SolidWorks rejects it. Supply both
  as design-table columns instead.
- Do **not** add a `BEND` dimension to straight fittings. A 0° angle is awkward to create
  and unnecessary — only elbows need it.

---

## 10. Recommended build order

```
6400   straight, one hex, ORB end        ← in progress
6801   same ORB end + 90° bend
6802   6801 with the bend changed to 45  ← nearly free
2501   NPTF end instead of ORB
2404   simplest, but its data is on the old schema
```

The ORB end modelled once in the 6400 reappears in 6401, 6402, 6405, 6408, 6410, 6500,
6801, 6802, 6803, 6804, 6900, 6901, 6902 — a large share of the catalog.

---

## 11. Immediate next actions

**Client:**
1. Finish the 6400 master using `05_DIAGRAMS/6400_final_profile.png`
2. Measure thread runout at both ends off a physical part
3. Export the Shopify product CSV
4. Get the ORB temperature limit from their seal supplier

**Assistant:**
1. Regenerate `DesignTable_6400.xlsx` once the master is done
2. Extract data for the next shapes — 6801 and 6802 have dimensions already; they need SKU
   reconciliation against the OMi catalog
3. Migrate 2404 to the `Parts_v2` schema
4. Write the Phase 3 batch plan and QA checklist
