---
name: omi-fitting-library
description: Conventions and guardrails for the OM Industrial CARBON STEEL fitting CAD library — 2,535 parts across 126 geometry topologies, built with SolidWorks design tables, a batch VBA macro, and fillable PDF templates. Use when working on any fitting topology, master model, design table, drawing macro, spec sheet, or the master data workbook. Triggers on mentions of a topology or SKU root (2404, 6801, FS6400, C2501…), GeometryRoot, DRIVE sketch, THD_ thread features, design table, DataStatus, ScopeAction, StdCheck, spec sheet fill, tabulated drawing, or JIC/ORFS/NPTF/compression carbon steel fittings.
---

# OMi Hydraulic Fitting Library

Project conventions for OM Industrial Products Corp. Read this before touching any topology.

## Scope — carbon steel only

**2,535 parts, 126 geometry topologies.** From the OM Industrial carbon steel collection:
Tube Fittings & Adapters (1,672), O-Ring Face Seal (385), Compression (230), Flange Adapters
& Accessories (163), Braze & Beaded Hose (73), Test Gauge (12).

**OUT OF SCOPE:** brass, stainless, international/metric, hose, hose crimp fittings, live
swivels, kits. Do not model them, do not add them to the workbook.

## The one architectural fact

**206 SKU roots collapse to 126 topologies. One master model per topology.** `2404`,
`FS2404` (ORFS), `C2404` (compression) and `2404-L` are the same geometry — different seal
family and length. Seal family, thread standard and length variant are **columns in the
Parts sheet**, never separate models. If you find yourself creating a second master for the
same topology, stop.

## Two authorities, never confused

| Question | Source |
|---|---|
| Which parts exist? | **OMi catalog** — `omindustrial.com/collections/<handle>/products.json?limit=50&page=N` |
| What are the dimensions? | **Air-Way**, cross-checked against a second manufacturer |

Reconcile them into `ScopeAction`: `BUILD` if the SKU is in the OMi catalog, `DROP` if it is
Air-Way-only. An OMi SKU with no Air-Way row is `BUILD` + `DataStatus = MISSING`.

On the 2404 pilot: 4 Air-Way rows were not OMi parts, and 7 OMi parts were absent from
Air-Way entirely. This reconciliation is not a formality.

Use `limit=50` on the JSON feed — larger pages silently truncate and lose ~80% of records
while appearing to succeed.

## Non-negotiable rules

1. **Never fabricate a dimension, thread spec, tolerance, material, or part number.** No
   value enters the dataset without a cited source. If there's no source, the cell stays
   empty and `DataStatus` becomes `MISSING`.
2. **Label everything** as verified fact, assumption, or looked-up value with its source.
3. **Stop and ask** rather than guessing. Especially on `DIVERGENT` standards checks — never
   silently pick between a catalog value and a standard value.
4. **Enumerate, never trust a stated count.** Catalog page extraction reports row totals
   unreliably (observed: 54/55/53 for the same 51-row table across three passes) while the
   enumerated rows were byte-identical every time. Extract twice, compare row sets.
5. **Everything traces to the workbook.** `OMi_Fitting_Library_MasterData_v1.xlsx` is the
   single source of truth for design tables, drawing notes, and spec sheets alike.

## Part numbers

`{topology}-{JIC dash:02d}-{NPTF dash:02d}` → `2404-08-06`. **Confirmed by the client.**

Roots shorter than 4 digits are zero-padded: `304-C` → `0304-C`. `PartNumber_OMi` is a
formula in the workbook — never typed.

## Dimension naming — generic slots, not catalog letters

**Every driving dimension lives in one sketch named exactly `DRIVE`.**

| Purpose | Name | Design-table header |
|---|---|---|
| Generic slots 1-6 | `D1` … `D6` | `D1@DRIVE` … `D6@DRIVE` |
| Hex across flats | `HEXA` `HEXB` | `HEXA@DRIVE` `HEXB@DRIVE` |
| Bend angle | `BEND` | `BEND@DRIVE` |
| Seat angle | `SEATB` | `SEATB@DRIVE` |

**Never name a dimension after a catalog letter.** Air-Way uses a different letter set per
family: 2404 = L/C/D/D1, 6801 = M/M7/C4/Y/D(1)/D(2), 6400 = L5/C4/D(1)/D(2),
2501 = M/N/Y/D/D1. Catalog-letter names would force a separate design table and macro for
roughly every third topology.

Generic slots mean all 126 masters expose an identical header set. The **DimensionMap** sheet
records which catalog letter each slot carries per topology — the letter lives in data, never
in geometry names.

`BEND@DRIVE` exists in every master, set to 0 on straights, so one macro serves all shapes
with no special-casing.

## Threads — helical in drawings, absent from the model

Drawings show **real helical threads**. The saved model and the exported STEP do not.

- Model threads with the SOLIDWORKS **Thread feature** (real helical geometry).
- Name every one with the prefix **`THD_`** (`THD_EndA`, `THD_EndB`).
- **Save the master with them SUPPRESSED.** That is the resting state.

`OMi_BatchDrawings.bas` unsuppresses `THD_*` only while drawing views are built, then
re-suppresses — including from its error handler, so a crash never leaves threads live.
STEP export runs while suppressed.

Rejected: two configurations per part (threaded/unthreaded). It would double the config
count to ~5,070 and roughly double rebuild time for no benefit.

Helical threads are expensive. Time a ten-part live run before releasing a full topology.

**Dimension letters are not portable.** J514's `C` is hex; Parker's `C` is hex; Air-Way's
`C` is something else. Always confirm what a letter denotes on each source's own drawing.

## DataStatus — the release gate

Two gates, both enforced by the macro AND the Python fillers:
`ScopeAction = DROP` → never emitted. `DataStatus` → as below.

| Sources | DataStatus | Releasable |
|---|---|---|
| 2+ independent agree | `VERIFIED` | Yes |
| 1 source | `ASSUMED` | Sample only, never production |
| None, or sources conflict | `MISSING` | Blocked |

Both the VBA macro and `fill_specsheets.py` enforce this gate. **Do not disable it.**
`ASSUMED` rows are auto-stamped "NOT STANDARDS-VERIFIED — not released for production."

## Standards cross-check

SAE J514/1 **does** fix body dimensions, not just seat and thread — scope: *"general and
dimensional specifications for 37 degree flared tube fittings"*, and it publishes hex
tolerances. Catalog dimensions are genuinely checkable.

| End type | Standard |
|---|---|
| JIC 37° | SAE J514/1 |
| NPTF | ASME B1.20.3 |
| ORFS | SAE J1453 |
| SAE straight thread / ORB | SAE J1926 |
| Compression / flareless | SAE J514/2 |
| Code 61 / 62 flange | SAE J518 / ISO 6162 |

Two traps: many standard dimensions are **minima or minus-only tolerances** — a value inside
the envelope is conforming, not divergent; and dimension letters are **not portable** between
sources (J514's `C` is hex, Air-Way's `C` is not).

Monolithic SAE J514 was **canceled 2024-11-22**, split into J514/1 (37° flared), /2
(flareless), /3 (NPTF adapters). Every free copy online is the superseded edition.

## Second-sourcing

Cross-check dimensions against Parker (Catalog 4300 Triple-Lok), Eaton/Weatherhead, Brennan
(via Applied.com), Gates, Dixon, or PressureConnections. This is what validated the pilot
without buying the paywalled standard — 27 of 29 comparable rows matched Parker exactly.

Never average conflicting values. Never resolve a conflict by majority vote silently.

## Hex across flats — it IS in the Air-Way data

**Air-Way publishes hex, just not under an obvious name.** The catalog `C` / `C4` column is
hex across flats. Confirmed by matching it against PressureConnections and Purvis on every
matched-size row of 2404, 6400, 6801 and 6802.

On elbows there are two: `C4` = nut hex (adjustable ORB end), `Y` = body wrench flats.
Straight fittings (6400, 2404) have a single body hex that follows the larger end.

**Use the catalog column, not a lookup table keyed by dash size.** The catalog value is
per-part-number and therefore correct on mismatched combinations (a -4 JIC x -2 ORB has a
smaller hex than a -4 x -4). A dash-keyed table gets those wrong.

2501 is the exception found so far — it publishes no hex column; use distributor data.

## Spec values from industry standards

| Field | Value | Basis |
|---|---|---|
| Material | Carbon Steel, ASTM A108 12L14 | J514 mandates "carbon steel" class only; grade is Parker's published choice |
| Finish | Trivalent Cr3 Zinc, ASTM B633 Type V/VI | RoHS-compliant current mainstream |
| Pressure | Generic SAE-style table | Ham-Let + hoseandfittings agree; Parker's run 30-50% higher |
| Temperature | -65F to +400F | Metal flare joint ONLY. No ORB limit found - elastomer governs there. |

Rules: working pressure at 4:1 burst; fitting SHAPE does not change the rating but END TYPE
does; on a two-end fitting the LOWER-rated end governs. Full sourcing on the StandardsData
sheet.

## Macro conventions

Defensive by default: `DRY_RUN = True`, `OVERWRITE_EXISTING = False`,
`ALLOW_UNVERIFIED = False`, per-config error trapping so one bad config never aborts a
batch, timestamped logs. **Always dry-run first and read the log before going live.**

SolidWorks 2026 **Standard** — no Task Scheduler. All batching is pure VBA.

## Files

| File | Role |
|---|---|
| `OMi_Fitting_Library_MasterData_v1.xlsx` | Source of truth. Parts, Series, lookups, Standards, QA_Log |
| `OMi_SpecSheet_Template.pdf` | 41 AcroForm fields, named identically to Parts columns |
| `OMi_DrawingTemplate_Pro_A4.pdf` | Client drawing border + 144 fields, tabulated dimension table |
| `fill_specsheets.py` | Per-part spec sheet fill engine |
| `fill_drawing.py` | Per-topology tabulated drawing fill, auto-splits past 18 rows |
| `OMi_BatchDrawings.bas` | Batch drawing + PDF/STEP export macro |
| `OMi_SOP_NewSeries.md` | Step-by-step procedure per root |

## Open items carried between sessions

- `D`↔JIC (End B) and `D1`↔NPTF (End A) — **confirmed by the client**, no longer inferred.
- ~76 of 1,672 Tube Fittings & Adapters SKUs not yet captured (95%); the JSON feed drops
  1-5 records per page deterministically. Topologies and counts are unaffected.
- Dash **-8 hex conflict**: Applied says 15/16", Parker and PressureConnections say 7/8".
  Unresolved.
- Dash **-14** appears in Air-Way but in no other 2404 table. May not exist in this style.
- **MS51500** is free on everyspec but scanned images only — no text layer. Must be read
  by eye.
- **VOSS DIN compression** category is PDF-catalog only, not in the 410-series count.
