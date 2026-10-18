# OMi Fitting Library — SOP: Adding a New Topology

**Version 2.0 · carbon steel scope · drawing-only helical threads**

**SCOPE: carbon steel only.** 2,535 parts across 126 geometry topologies, taken from the
OM Industrial carbon steel collection — Tube Fittings & Adapters, O-Ring Face Seal,
Compression, Flange Adapters & Accessories, Braze & Beaded Hose, and Test Gauge. Brass,
stainless, international/metric, hose, crimp fittings, live swivels and kits are OUT OF SCOPE.

This is the repeatable procedure for taking any one of those 126 topologies
from catalog page to released drawings and spec sheets. Follow it in order. Every step has
a stop condition — if a stop condition fires, resolve it before continuing rather than
working around it.

---

## Before you start

You need, in one place:

- `OMi_Fitting_Library_MasterData_v1.xlsx` — the single source of truth
- `OMi_SpecSheet_Template.pdf` — the fillable spec sheet
- `OMi_BatchDrawings.bas` — the SolidWorks macro
- `fill_specsheets.py` — the spec sheet fill engine
- Your drawing template `.drwdot`

Directory convention:

```
C:\OMi\
  Masters\      <geometry root>.SLDPRT        one master per GeometryRoot
  Templates\    OMi_Fitting_B.drwdot
                OMi_SpecSheet_Template.pdf
  Data\         OMi_Fitting_Library_MasterData_v1.xlsx
  Output\       <part number>.pdf / .step
  Sheets\       <part number>_SPEC.pdf
  Logs\
```

---

## Step 1 — Pick the topology, not the SKU prefix

Open the **Topologies** sheet. Pick a row with `MasterModelStatus = NOT STARTED`.

A topology spans several SKU prefixes. Topology `2404` covers plain `2404` (JIC/NPTF),
`FS2404` (ORFS), `C2404` (compression), and the `-L` long variant — same geometry, different
seal family and length. **One master per topology, not per prefix.** Seal family, thread
standard and length variant are columns in the Parts sheet, not separate models.

The Topologies sheet shows which families each topology appears in, so you know up front
whether you're building one seal variant or four.

**STOP IF:** the prefixes under one topology are not actually the same geometry. Some numbers
collide without sharing a shape. Check the product names before committing.

---

## Step 2 — Establish the part list, then the dimensions

**Two different sources, and the distinction matters:**

| Question | Authority |
|---|---|
| Which parts exist? | **The OMi catalog.** `omindustrial.com/collections/<handle>/products.json?limit=50&page=N` |
| What are their dimensions? | **Air-Way**, cross-checked against a second manufacturer |

Pull the OMi SKU list for the topology FIRST. That defines scope. Then pull Air-Way's
dimension table and reconcile the two:

- SKU in both → `ScopeAction = BUILD`, dimensions available
- SKU in OMi only → `BUILD`, `DataStatus = MISSING` — needs a dimensional source
- SKU in Air-Way only → `ScopeAction = DROP`, do not model it

The pilot showed this is not a formality: of 51 Air-Way 2404 rows, **4 are not OMi parts**,
and **7 OMi parts are absent from Air-Way's table entirely**.

Use `limit=50` on the JSON feed. Larger page sizes silently truncate and lose ~80% of the
records while appearing to succeed.

**Mandatory reconciliation.** Extraction of these pages self-reports row counts unreliably
— during the pilot the same page reported 54, 55, and 53 rows across three passes while the
actual enumerated rows were byte-identical at 51 every time. So:

1. Extract the table twice, independently.
2. Compare the two **enumerated row sets**, not the stated totals.
3. Only proceed if they match exactly.

**STOP IF:** the two passes disagree. Extract a third time and take the two that agree.

---

## Step 3 — Cross-check against the governing standard

SAE J514/1 **does** specify fitting body dimensions, not just seat and thread — its scope
reads *"general and dimensional specifications for 37 degree flared tube fittings"*, and it
publishes hex-across-flats tolerances. So catalog dimensions are genuinely checkable.

For each root:

| End type | Check against |
|---|---|
| JIC 37° flare | SAE J514/1 |
| NPTF | ASME B1.20.3 |
| ORFS | SAE J1453 |
| Metric stud / port | ISO 6149, ISO 9974 |
| BSPP | ISO 1179 |
| BSPT | ISO 7 |
| DIN 24° cone | ISO 8434-1 |
| **Brass line** | **No standard is cited by the source. See below.** |
| **FLARE-O®** | **Proprietary. No public standard. See below.** |

Record the outcome in `StdCheck_Result`: `MATCH`, `DIVERGENT`, `UNVERIFIABLE`, or `N-A`.

**Two rules that prevent false alarms:**

- Many standard dimensions are **minima or minus-only tolerances**, not exact targets. A
  catalog value inside the envelope is *conforming*, not divergent. Never flag on
  inequality alone.
- **Dimension letters are not portable.** J514's "C" is hex; Parker's "C" is hex; Air-Way's
  "C" is a different value entirely. Confirm what a letter denotes on each source's own
  drawing before comparing anything.

**STOP IF:** `DIVERGENT`. Do not silently pick a value. Escalate the specific dimension,
both numbers, and both sources.

**Brass and FLARE-O have no standard to check against.** For these, substitute a
second-manufacturer cross-check (below) — it is the only verification available.

---

## Step 4 — Second-source the dimensions

This is what made the pilot trustworthy without buying the paywalled standard. 27 of 29
comparable rows matched an independent manufacturer exactly.

Cross-check against at least one of: Parker (Catalog 4300 Triple-Lok), Eaton/Weatherhead,
Brennan (via Applied.com), Gates, Dixon, PressureConnections.

Set `DataStatus`:

| Sources | DataStatus | Releasable? |
|---|---|---|
| 2+ independent sources agree | `VERIFIED` | Yes |
| 1 source only | `ASSUMED` | Sample sheet only — never production |
| No source | `MISSING` | Blocked |
| Sources conflict | `MISSING` + note | Blocked until resolved |

**Do not average conflicting values. Do not pick the majority silently.** Record both,
flag it, escalate.

---

## Step 5 — Fill in what the catalogs never publish

These are absent from every catalog checked and must come from OMi:

- Material and material spec
- Finish / plating and its spec
- Working pressure rating (usually varies by dash size)
- Temperature range

**Hex across flats** is rarely in the source catalog but usually *is* in Parker's or
Brennan's tables. Chase it there before declaring it missing.

**STOP IF:** hex is still missing. A fitting without a hex cannot be modelled.

---

## Step 6 — Build the master model

One `.SLDPRT` per GeometryRoot, in `C:\OMi\Masters\`.

**The naming rule that makes everything else work:** every driving dimension lives in a
single sketch named exactly **`DRIVE`**.

| Dimension | Name | Design-table header |
|---|---|---|
| Generic slots 1-6 | `D1` … `D6` | `D1@DRIVE` … `D6@DRIVE` |
| Hex, end A | `HEXA` | `HEXA@DRIVE` |
| Hex, end B | `HEXB` | `HEXB@DRIVE` |
| Bend angle | `BEND` | `BEND@DRIVE` |
| Seat angle, end B | `SEATB` | `SEATB@DRIVE` |

**Do NOT name dimensions after catalog letters.** Air-Way uses a different letter set for
every family — 2404 is L/C/D/D1, 6801 is M/M7/C4/Y/D(1)/D(2), 6400 is L5/C4/D(1)/D(2),
2501 is M/N/Y/D/D1. Naming geometry after them would mean a different design table and macro
for roughly every third topology.

Generic slots mean **all 126 masters expose the identical header set**. Check the
**DimensionMap** sheet to see which catalog letter each slot carries for your topology, then
assign `D1`…`D6` in that order.

`BEND@DRIVE` exists in **every** master, set to 0 for straights. This is deliberate — one
macro then serves elbows and straights with no special-casing.

### Threads — real helical geometry, suppressed by default

Drawings must show **real helical threads**; the model you keep and the exported STEP must
not carry them.

1. Model each thread with the SOLIDWORKS **Thread feature** (real helical cut/boss).
2. Name every thread feature with the prefix **`THD_`** — e.g. `THD_EndA`, `THD_EndB`.
3. **Leave them suppressed.** That is the saved state of the master.

The macro unsuppresses `THD_*` only while drawing views are being built, then re-suppresses
immediately — including from its error handler, so a crash never leaves threads live. STEP
export happens while they are suppressed, so customers get clean manufacturing geometry.

Rejected alternative: two configurations per part (threaded / unthreaded). That would take
the library from ~2,535 to ~5,070 configs and roughly double rebuild time for no benefit.

**Time it before you trust it.** Helical threads are expensive to rebuild. Run ten parts
live and measure before turning a full topology loose.

**Confirmed mapping:** `D` belongs to the JIC (End B) side, `D1` to the NPTF (End A) side.
Verified by the client — no longer an inference.

**Part number format, confirmed:** `{topology}-{JIC dash}-{NPTF dash}`, each dash
zero-padded to two digits → `2404-08-06`.

---

## Step 7 — Generate the design table

Export from the Parts sheet, filtered to the root. Column A = `PartNumber_OMi`
(which is also the configuration name). Then the `@DRIVE` columns, then `$PRP@` property
columns, then `$COMMENT`.

Insert into the master: **Insert → Tables → Design Table → From file**, linked.

**STOP IF:** any row has a blank `@DRIVE` value. SolidWorks will inherit the previous
configuration's value and produce a wrong model that looks perfectly fine. The generator
shades these rows red — do not insert a table with red rows.

---

## Step 8 — Batch drawings and exports

1. Open the master part with the design table applied.
2. Open `OMi_BatchDrawings.bas`, set `OUTPUT_DIR` and `DRAWING_TEMPLATE`.
3. **Run with `DRY_RUN = True` first.** Always. It walks every configuration and writes a
   full log without creating a single file.
4. Read the log. Confirm the config count, the skips, and the filenames.
5. Set `DRY_RUN = False` and run.

The macro skips any configuration whose `DataStatus` is not `VERIFIED` or `ASSUMED`. That
gate is what stops incomplete data becoming a released drawing. Leave
`ALLOW_UNVERIFIED = False`.

---

## Step 9 — Spec sheets

```bash
python fill_specsheets.py --dry-run          # always first
python fill_specsheets.py                    # then live
```

Same `DataStatus` gate. `ASSUMED` rows are auto-stamped with a "NOT STANDARDS-VERIFIED /
not released for production" note in the Notes field — do not remove it manually.

---

## Step 10 — QA spot-check

Pull **3 configurations at random** plus the **largest and smallest** dash sizes. For each:

- [ ] Part number on the drawing matches the Parts sheet
- [ ] Thread callouts match `EndA_Thread` / `EndB_Thread` exactly
- [ ] Overall length measured on the model equals `D_L`
- [ ] Hex measures equal to `D_HEXA` / `D_HEXB`
- [ ] Seat angle is 37° (or the root's correct value), not the default
- [ ] Bend angle correct — and genuinely 0 on straights, not merely unconstrained
- [ ] STEP opens cleanly and is a single solid body
- [ ] Spec sheet fields all populated; no stray placeholder text
- [ ] `ASSUMED` rows carry the not-for-production note
- [ ] Filename matches `FileName_Base`

**STOP IF:** any check fails. One failure in a spot-check means the whole batch is suspect —
fix the cause and regenerate the batch, don't patch the individual file.

---

## Step 11 — Close out

Update the **Series** sheet: set `MasterModelStatus` to `COMPLETE` for every series under
the root, and fill `VariantCount`. Append anything surprising to `QA_Log`.

---

## The five failure modes that cost the most

1. **Silent design-table inheritance** — a blank cell doesn't error, it inherits. Always
   check for blanks before inserting.
0. **Modelling a part OMi doesn't sell** — always reconcile against the OMi SKU list first.
   Air-Way's catalog is broader than yours in some places and narrower in others.
2. **Letter-mapping errors** — assuming one source's `C` means another's `C`. Verify per source.
3. **Trusting a stated row count** — enumerate, always.
4. **Leaving threads unsuppressed** — the master must be saved with `THD_*` suppressed.
   An unsuppressed master makes every downstream rebuild slow.
5. **Releasing `ASSUMED` data** — the gate exists for this. Don't switch it off to
   "just get the batch out."
