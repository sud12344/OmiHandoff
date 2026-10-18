# 2404 Master Model — Build Sheet

**Topology 2404 — Male Connector.** Male NPTF taper pipe (End A) × male JIC 37° flare (End B), straight.
**Reference configuration: `2404-08-06`** · SOLIDWORKS 2026 Standard · inches, 4 decimal places
Work from `2404_profile.png`.

---

## Why the 2404 is in much better shape than the 6400

I pulled **MS51500G with Amendment 1** (8 July 2026) from the DoD ASSIST database — the military
drawing Air-Way cites for series 64. It tabulates hex, both bores, overall length **and `S`, the
counter-bore depth**, for 24 of your 58 configurations.

Cross-checked against your Parts sheet: **96 value comparisons, zero disagreements.**

That matters for three reasons.

**One — the bore is fully sourced.** MS51500 Note 5 reads:

> *"At manufacturers option, through passages may conform with the smaller diameter specified or
> the appropriate end may be counter-bored to the larger diameter for depth `S`."*

So the through passage takes the **smaller** of `D`/`D1`, and the end carrying the larger diameter is
counter-bored to it for depth `S`. The 6400's single biggest assumption — where the bore steps —
simply does not exist here. It is published.

**Two — the NPTF end is fully sourced.** ASME B1.20.3 gives the taper (1:16 on diameter), the pitch
diameters and the effective thread length `L2`. I had that cross-checked against seven independent
reproductions; every row satisfies the standard's own identity `E1 = E0 + 0.0625 × L1` exactly.

**Three — it settles your open dash-8 hex conflict.** SKILL.md records Applied/Brennan saying 15/16"
against Parker and PressureConnections at 7/8". **MS51500 A8-8 gives `7/8`.** Parker and
PressureConnections were right.

**What is still assumed: exactly two numbers in the whole part** — a 0.098 thread relief and a 0.094
nose land at the JIC end. Both come from the 6400 work on a ‑08 JIC end, which is the same geometry.
Both are library-wide constants and both are design-table columns.

I sanity-checked them: across all 35 computable configurations the resulting hex length lands at
**0.47 – 0.77 × the hex width, median 0.60**, with no negatives and no outliers. That is a tight,
physically sensible band — reasonable evidence the model is structurally right, though not a source.

---

## Stage 1 — the `DRIVE` sketch

New part, inches, 4dp (**Tools → Options → Document Properties → Units → IPS, 4 decimals**).
Sketch on the **Front plane**; the revolve axis is the **X axis**.

### 1a. Draw 11 lines as a closed loop, then a construction centreline

x runs from the **NPTF pipe tip** at 0 to the **JIC flare tip** at 1.5300. y is radius.

```
V1  (0.0000, 0.0000)   <- ON THE ORIGIN
V2  (0.0000, 0.3282)      NPTF crest, small end
V3  (0.4078, 0.3410)      NPTF crest, large end   <- DERIVED from the taper
V4  (0.4078, 0.4691)      body / hex
V5  (0.8730, 0.4691)
V6  (0.8730, 0.3750)      JIC thread major
V7  (1.2810, 0.3750)
V8  (1.2810, 0.3295)      cone large end
V9  (1.4360, 0.2127)      cone tip        <- DERIVED from the 37 deg
V10 (1.5300, 0.2127)
V11 (1.5300, 0.0000)
back to V1 along the axis
```

Then **Sketch → Centerline** along the axis, **collinear with the X axis**, and add a **Coincident**
relation from each endpoint to **V1** and **V11**.

> **Lock both centreline endpoints.** Collinear removes only 2 of its 4 degrees of freedom; SolidWorks
> counts construction geometry toward Fully Defined, so without this the sketch never closes out.

**Relations:**

- `V1` **coincident** with the **origin**
- **vertical** on V1‑V2, V3‑V4, V5‑V6, V7‑V8, V10‑V11
- **horizontal** on V4‑V5, V6‑V7, V9‑V10, V11‑V1
- **leave V2‑V3 and V8‑V9 free** — those are the two cones, driven by their angles

### 1b. Apply the 11 dimensions in this order

Rename each one immediately after creating it (double-click → the top box under "Primary Value").
Creating the overall last is what frees up the name `D1`.

| # | Select | Type | Value | Rename to |
|---|---|---|---|---|
| 1 | line V1‑V2 → line V3‑V4 | horizontal | `0.4078` | `NPTF_THDL` |
| 2 | line V5‑V6 → line V7‑V8 | horizontal | `0.408` | `JIC_CYL` |
| 3 | line V7‑V8 → **point V9** | horizontal | `0.155` | `JIC_SEATL` |
| 4 | **point V9** → line V10‑V11 | horizontal | `0.094` | `JIC_NOSEL` |
| 5 | line V1‑V2 + **centreline** | diameter | `0.6565` | `NPTF_MAJ` |
| 6 | line V4‑V5 + **centreline** | diameter | `0.9382` | `BODYDIA` |
| 7 | line V6‑V7 + **centreline** | diameter | `0.750` | `THDMAJ_B` |
| 8 | **point V8** + **centreline** | diameter | `0.659` | `JIC_CONEDIA` |
| 9 | line V2‑V3 + **centreline** | angle | `1.7899` | `NPTFTAPER` |
| 10 | line V8‑V9 + **centreline** | angle | `37` | `SEATB` |
| 11 | line V1‑V2 → line V10‑V11 | horizontal | `1.5300` | `D1` |

For a **diameter** dimension: select the profile line *and* the centreline, then drag across to the far
side of the centreline before clicking. If it reads as a radius you placed it on the near side.

For **#9 and #10**, both angles are measured **from the axis**, not from the vertical. If #9 comes up
as 88.21° you have picked the complement — take the other quadrant.

**Do NOT dimension:** the hex length (0.4652), the nose diameter (Ø0.4254), or the NPTF large-end
diameter (Ø0.6819). All three are derived and dimensioning any of them over-defines the sketch.

### 1c. Check

Status bar must read **Fully Defined**. 11 lines + centreline gives 22 vertex DOF, minus 2 for the
origin, minus 5 vertical and 4 horizontal relations = 11 remaining, consumed by exactly 11 dimensions.

If **Under Defined**, check the centreline endpoints first — that is the usual culprit.
If **Over Defined**, you have dimensioned one of the three derived values.

Rename the sketch **`DRIVE`**.

---

## Stage 2 — Revolve

**Insert → Boss/Base → Revolve.** Axis = the centreline. 360°. The result is a **solid bar** — no hole
yet, which is correct. Rename the feature `BODY`.

---

## Stage 3 — the hex

Sketch on the **Right plane** (at x = 0, normal to the axis).

**Tools → Sketch Entities → Polygon.** 6 sides, centre on the origin, **Inscribed circle** — *not*
circumscribed. Inscribed gives across-flats, which is what MS51500's `C1` publishes.

Dimension the construction circle to **Ø0.8125** — that is 13/16 exactly — and rename it **`HEXB`**.
Add a **Horizontal** relation to the construction line from centre to vertex to lock the rotation
(clocking is cosmetic, but it must be locked).

Rename the sketch **`HEX`**.

**Insert → Cut → Extrude.** Direction 1 = **Through All**, tick **Direction 2 = Through All**, and tick
**Flip side to cut**. Rename the feature **`HEXCUT`**.

> **Why Through-All-Both is safe here.** The cut only bites where the part is wider than the hex flats.
> The hex flat radius exceeds every other radius on the part — the largest competitor is the JIC thread
> major at 0.375 against a flat radius of 0.4063. I verified the same margin holds on all 45 emitted
> configurations. So you never need a length dimension on this cut.

---

## Stage 4 — the bore

Both bore sketches go on the **Right plane**. No face references — those break when a design table
drives 45 configurations.

**BORE_THRU — the through passage**

1. Sketch on the Right plane: one **circle**, centre on the origin, **Ø0.391**. Rename the diameter
   dimension `D3`. Rename the sketch **`BORE_THRU`**.
2. **Insert → Cut → Extrude**, Direction 1 = **Through All**. Rename the feature **`THRUCUT`**.

**CBCUT_A — the counterbore at the NPTF end**

3. Sketch on the Right plane: one **circle**, centre on the origin, **Ø0.406**. Rename it `CBDIA`.
   Rename the sketch **`BORE_A`**.
4. **Insert → Cut → Extrude**, Direction 1 = **Blind**, depth **0.680**, pointing *into* the part.
   Rename the depth dimension **`DEPTH`**. Rename the feature **`CBCUT_A`**.

**CBCUT_B — the counterbore at the JIC end**

5. Same again, but sketch on the Right plane with **From → Offset = 0.8500** (that is `D1 − DEPTH`),
   circle **Ø0.391**, Blind depth **0.680**, cutting *toward the JIC end*.
   Rename the sketch **`BORE_B`**, the feature **`CBCUT_B`**.
6. **Right-click `CBCUT_B` → Suppress.** On this configuration the counterbore is at the NPTF end.

> **Why two counterbore features.** Which end gets counter-bored depends on whether `D` or `D1` is
> larger, and **it flips**: on 16 of the 45 configurations it is the NPTF end, on 7 it is the JIC end,
> and on 22 there is no counterbore at all. A feature cannot change ends from a design table, so the
> table carries `$STATE@CBCUT_A` and `$STATE@CBCUT_B` and switches whichever one is wrong to `S`.

---

## Stage 5 — threads

**Insert → Features → Thread.**

| | `THD_EndA` (NPTF) | `THD_EndB` (JIC) |
|---|---|---|
| Start edge | circular edge at x = 0, the small end of the taper | circular edge at x = 1.281, where Ø0.750 steps down to the cone |
| Type | **Inch Tapered Pipe** | Inch Die |
| Size | 3/8‑18 NPTF | 0.7500‑16 |
| Method | Cut thread | Cut thread |
| End condition | Blind, **0.4078** | Blind, **0.310** |
| Direction | into the part (+X) | *toward the hex* (−X) |

> **Watch for double taper on `THD_EndA`.** Your `DRIVE` profile already models the crest cone, so the
> blank is correctly tapered. If SolidWorks' tapered-pipe thread profile *also* applies its own taper
> you will get roughly twice the intended taper. Check it: measure the crest diameter at both ends of
> the thread — it should grow by 0.0625 in per inch of length, i.e. 0.0255 over the 0.4078 length. If it
> grows by about double that, switch `THD_EndA` to a straight die profile, since the cone is already in
> the geometry. **Tell me what you see and I'll adjust the build sheet.**

**Then right-click each thread feature → Suppress.** Save the master with both suppressed. That is the
resting state; the macro unsuppresses them only while drawing views are built.

---

## Stage 6 — save and check

Save as `C:\OMi\Masters\2404.SLDPRT`.

- [ ] `DRIVE` reads **Fully Defined**
- [ ] Tree reads `DRIVE` → `BODY` → `HEXCUT` → `THRUCUT` → `CBCUT_A` → `CBCUT_B` → `THD_EndA` → `THD_EndB`
- [ ] `CBCUT_B` suppressed, both `THD_` features suppressed
- [ ] **Measure**: overall length **1.5300**
- [ ] **Measure**: hex across flats **0.8125** (flat-to-flat, not corner-to-corner)
- [ ] **Measure**: bore at the JIC end **0.3910**, at the NPTF end **0.4060**
- [ ] Section view: the counterbore steps down at **0.680** from the NPTF face
- [ ] **Measure**: NPTF crest diameter **0.6565** at the tip, **0.6819** at 0.4078
- [ ] **Tools → Evaluate → Check**: a single solid body

---

## The data, and what it unblocks

Two files come with this sheet.

**`2404_Parts_v2.xlsx`** — all 58 rows re-scored on the `Parts_v2` schema.

| | before | after |
|---|---|---|
| VERIFIED | 11 | **24** |
| ASSUMED | 17 | **25** |
| MISSING | 30 | **9** |

The jump is mostly one correction. **23 rows were scored `MISSING` for want of a hex that was already
in the data.** SKILL.md records the lesson — *"Air-Way publishes hex, just not under an obvious name;
the catalog `C`/`C4` column is hex across flats"* — but the `Parts` sheet was never updated to match.
I checked it rather than assuming: on the 28 rows carrying both the Air-Way `C` value and the
separately-sourced `HEXB`, the two agree on **all 28** once you account for `C` being printed to two
decimals (0.63↔0.625, 1.13↔1.125, 2.63↔2.625 — the same rounding pattern MS51500 exposed on the 6400).

The 9 that remain `MISSING` are genuinely blocked:

- **7 OMi-only SKUs** with no Air-Way row at all — `2404-02-04`, `2404-08-02`, `2404-16-32`,
  `2404-32-20`, `2404-32-48`, `2404-40-32`, `2404-40-40`. They need a dimensional source.
- **2 escalated conflicts** — `2404-16-24` (your 2.51 vs Parker's 2.50) and `2404-24-20` (2.65 vs
  2.66). Both are `DIVERGENT` per SOP Step 3, neither is in MS51500, and I am not picking between
  them. **These need your call.**

**`DesignTable_2404_v2.xlsx`** — 45 configurations, on the v2 generic-slot naming.

Three defects in the old `DesignTable_2404.xlsx` are fixed:

1. **All 4 `DROP` rows were being emitted** — `2404-14-08`, `2404-14-12`, `2404-16-08`, `2404-24-12`
   are Air-Way parts OM Industrial does not sell, and the old table would have produced drawings and
   STEP files for them. That is SOP failure mode zero. They are now gated out.
2. **`Material`, `Finish` and `PressureRating` were blank on all 51 rows**, so every spec sheet would
   have come out with those fields empty. Now populated from `StandardsData`.
3. **Old v1 catalog-letter naming** (`L@DRIVE`, `C@DRIVE`, `D@DRIVE`, `TUBEOD@DRIVE`) — superseded by
   `DimensionNaming`. Now on the v2 scheme.

**10 of the 45 still carry a `BLOCKED` comment and are shaded red.** They are the JIC ‑20, ‑24 and ‑32
sizes, where `EndGeometry` has no seat length or thread length — the same gap already on your open-items
list. Do not insert those rows; everything else is clean.

---

## What is genuinely left on this topology

1. **SAE J514/1** would replace the two assumed constants and fill the ‑20/‑24/‑32 gap. Same
   recommendation as the 6400: it is the highest-leverage purchase in the project, because it unblocks
   every 37° flared topology, not just this one.
2. **The two DIVERGENT lengths** need your decision.
3. **7 OMi SKUs** need a dimensional source.
4. **No `2404.csv` in `07_RAW_EXTRACTS`.** Every other captured topology has its verbatim Air-Way
   extract; the 2404 does not. So there is no primary source to re-check the workbook against, and the
   SOP's mandatory double-extraction cannot be repeated. I would re-pull series 64 and store it.
5. **The topology is wider than the 58 rows.** `Topologies` marks 2404 as present in CS Adapters, ORFS
   *and* Compression, and Air-Way carries `FF2404` (ORFS, 24 variants), `2404-L` (8) and `2404-LL` (7)
   under the same geometry — all in scope, none captured yet. The master you are about to build serves
   all of them.
