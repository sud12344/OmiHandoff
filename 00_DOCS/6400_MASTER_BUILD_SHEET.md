# 6400 Master Model — Build Sheet (restart from scratch)

**Reference configuration: `6400-08-08-O`** · SOLIDWORKS 2026 Standard · inches, 4 decimal places
**Supersedes** `05_DIAGRAMS/6400_final_profile.png` and README §9. Work from
`6400_rebuild_profile.png`.

---

## What changed from the previous plan, and why

**1. The bore comes out of the DRIVE sketch.** The 6400 has *two* bore diameters —
Air-Way publishes `D(1)` at the JIC end and `D(2)` at the ORB end — and **50 of the 65
configurations have D(1) ≠ D(2)**. The old profile drew a single through-bore, which is
correct only for the 15 configs where they happen to be equal. `6400-08-08-O` is one of
those 15, which is exactly why the error was invisible.

A step drawn as sketch geometry breaks on those 15: the step's vertical line becomes
zero-length and the sketch fails. So the profile now revolves to a **solid bar** and the
bore is cut afterwards as **two blind cuts** that meet at the step plane. That construction
is correct whether D3 is larger or smaller than D4, and degenerates cleanly to a plain
through-hole when they are equal.

**2. README §9's "do not put the profile corner on the origin" no longer applies.** That
warning existed because the bore was the bottom edge of the profile, so a corner on the
origin collapsed the hole. The profile is now solid and its bottom edge *belongs* on the
axis. **Put the bottom-left corner on the origin.** Ignore the old note.

**3. Five diameters in the sketch, not six.** The sixth (the bore) has moved to the cut
features.

---

## Sourcing — I went back and checked this properly

You asked whether Air-Way just gives the measurements. Short answer: **no, and neither does
anyone else — but chasing it hard turned up a much better source and corrected two numbers
in your model.**

### What Air-Way actually publishes

I re-fetched the Air-Way series 89 page myself rather than trusting the previous session's
extract. The extract was **complete and correct** — Air-Way publishes exactly seven columns:

```
Part #  |  B (1) UN/UNF-2A  |  B (2) UN/UNF-2A  |  L5  |  C4  |  D (1)*  |  D (2)*
```

That is: two thread callouts, overall length, hex across flats, two bore diameters. No hex
length, no thread lengths, no cone or nose dimensions.

**And it is not an Air-Way shortcoming.** Parker's Catalog 4300 publishes the same two
dimensions using the *same letters* — `C4` hex, `L5` length. So do Gates, Aeroquip/Eaton, QC
Hydraulics and every distributor I checked. Fitting catalogs print what a *buyer* needs to
select a part, not what a *machinist* needs to cut one.

### The much better source: MS51525 Rev D

The Air-Way page cites **MS51525** as its governing drawing. I pulled the current revision
(Rev D, 30 September 2021) from the DoD ASSIST database. It is a real, text-bearing military
standard drawing for exactly this fitting — "ADAPTER, STRAIGHT, TUBE TO BOSS, O-RING, 37
DEGREE FLARED" — and it tabulates hex across flats (`C1`), bore (`D`) and overall length
(`L`) for 23 of your 65 configurations.

**I cross-checked all 23 against Air-Way: 69 value comparisons, zero disagreements.** Every
Air-Way number is a correct two-decimal rounding of the MS51525 value.

That is a significant upgrade. Under your own rule — two independent sources agreeing —
**Air-Way's `L5`, `C4` and `D(1)` are now `VERIFIED`, not `ASSUMED`.** And MS51525 gives
exact values where Air-Way rounds.

### Two numbers in your model were wrong because of that rounding

| | was | **is** | why |
|---|---|---|---|
| Hex across flats | 0.880 | **0.875** | MS51525 gives `7/8` exactly. Air-Way prints 0.88. |
| `BODYDIA` | 1.0161 | **1.0104** | follows: 7/8 ÷ cos30° |
| Bore | 0.390 | **0.391** | MS51525 `D` = .391. Air-Way prints 0.39. |

Modelling 0.880 would have made every hex 0.005" oversize. I've corrected the build sheet and
the diagram. For the 42 configurations MS51525 doesn't cover, every one of Air-Way's 18
distinct hex values resolves to exactly one standard wrench fraction with no ambiguity — so I
can supply exact hex for all 65 when I build the design table.

**This also settles an open item.** SKILL.md records an unresolved dash-8 hex conflict —
Applied said 15/16", Parker and PressureConnections said 7/8". MS51525 says **7/8**. Parker
and PressureConnections were right; Applied's figure is wrong for this fitting.

### What is still genuinely missing, and why

MS51525 does not carry hex length either. Its **Note 4** says why, explicitly:

> *"Dimensions and tolerances not shown shall be in accordance with SAE-J514 for 37° flared
> fittings."*

So the axial breakdown — hex length, thread lengths, cone and nose-land lengths — lives in
**SAE J514/1**, and nowhere else. That document is paywalled, and per your own notes the
monolithic J514 was cancelled in November 2024 and split into J514/1, /2 and /3, so every free
copy online is the superseded edition.

I also swept CAD repositories, McMaster, and a dozen manufacturer catalogs. Nobody publishes
hex length. The closest was Topa, a Chinese maker of the equivalent fitting, whose table
carries `L1` and `L2` columns — but with **no legend defining them**, so I will not build on
it.

### One warning from that Topa data

Reading `L1` as the JIC-end length, its value for a ‑08 is 16.7 mm = **0.657"** — which
matches the previous session's JIC-end figure exactly. That is mild corroboration.

But its `L2` for a ‑08 ORB end is 11.13 mm = **0.438"**, against the previous session's
**0.560"**. If Topa's reading is right, the hex would be ~0.385 long, not 0.263, and the whole
hex would sit about 0.12" further toward the ORB end than the current numbers put it.

I am **not** telling you Topa is right — one unlabelled table is not a source. But it is
positive evidence that the 0.466 / 0.263 / 0.560 split may be wrong, where before I could only
say it was unsupported. Treat the hex position as genuinely unknown, not as "probably fine".

### What I recommend

**Buy SAE J514/1.** It is on the order of $100 from SAE. It is the only document that carries
these dimensions, it is the standard your drawings already cite, and it unblocks the axial
geometry of *every* 37° flared topology in the library — not just the 6400. Against 126
masters, that is the highest-leverage hundred dollars in this project.

**In the meantime, two caliper readings** on one physical ‑08 part — hex length and
hex-face-to-tip — pin the pilot immediately.

**Build the master now regardless.** The sketch *structure* is correct and fully sourced at
both ends; only three axial values are soft, and all three are design-table columns. When the
standard or the calipers arrive, you regenerate the table and every configuration updates. No
geometry gets re-cut. But score the topology `ASSUMED` and do not release it.

---

## Naming — settled, don't change it

Your workbook mostly resolves this. I checked `DimensionNaming`, `DimensionMap` and
`EndGeometry`; the scheme below follows them, with **three deliberate departures** called out
at the end of this section.

| Kind of value | Naming | Why |
|---|---|---|
| Per-part Air-Way catalog values | generic slots `D1`…`D6` | the catalog letter differs per topology |
| Dash-size-keyed end geometry | semantic (`ORB_GRVDIA`, `JIC_SEATL`…) | `EndGeometry`: *"Model them as named dimensions (not generic slots) because the meaning IS universal"* |

For the 6400, `DimensionMap` fixes: **D1 = L5** (overall), **D2 = C4** (hex),
**D3 = D(1)** (JIC-end bore), **D4 = D(2)** (ORB-end bore).

**Three departures from the documented convention, all deliberate:**

1. **Not every driving dimension lives in `DRIVE` any more.** `HEXB` is in `HEX`, `D3` is in
   `BORE_B`, `D4` is in `BORE_A`. This is forced — a hexagon and two end circles cannot live
   in the revolve profile. Your previous session had already accepted the `DRIVE` + `HEX`
   split; this adds two more sketches. To keep headers uniform across all 126 masters, the
   sketch names `BORE_A` / `BORE_B` must be used verbatim on every master.
2. **No `D2` dimension.** D2 = C4 = hex, and `HEXB` already carries it. Carrying it twice
   invites the two copies to drift apart.
3. **No `BEND`.** `DimensionNaming` says every master carries it, and the existing
   `DesignTable_6400.xlsx` has it populated with 0 on all 65 rows. Dropping it on straights
   was already agreed in README §8 item 4. Say the word if you'd rather keep it for
   uniformity — it costs one column and one dummy dimension.

**D3 is the JIC end, D4 is the ORB end. `DataStatus = VERIFIED`.**

I first claimed this was verified when it wasn't — the bore data alone can't tell a JIC end
from an ORB end, because `EndGeometry` publishes no ORB bore column and both ends of a 6400
carry the same UN/UNF thread for a given dash. So I went and sourced it properly. Three
independent sources, all agreeing that **the first dash is the JIC 37° end and the second is
the SAE ORB end**:

| Source | Evidence |
|---|---|
| **OM Industrial's own catalog** — `6400-05-04-O` | description reads *"05 MJ - 04 MORB Straight"*. `MJ` = male JIC, `MORB` = male O-ring boss. Authoritative for your own numbering. |
| **Brennan, via Hose Warehouse** — `6400-08-06-O` | titled *"-08 Male JIC x -06 Male O-Ring Boss"*. Independent manufacturer, same part-number family. |
| **Brennan, via ARG Industrial** — `6400-20-24-O` | JIC thread 1‑5/8‑12 (a ‑20, the first dash), ORB thread 1‑7/8‑12 (a ‑24, the second dash). |

> **QA note worth logging.** The ARG page's *prose* reads "1‑1/2 in Male SAE ORB x 1‑1/4 in
> Male SAE 37 deg JIC Flare" — i.e. it names the ORB end first, which reads as though the
> first dash were the ORB. Its own thread data says otherwise. This is the "letters and order
> are not portable between sources" trap from SOP Step 3, live in the wild. Read the threads,
> not the word order.

So `D3 = D(1) = JIC-end bore` and `D4 = D(2) = ORB-end bore`, exactly as the build sheet has
it. Nothing to change — but it's now sourced rather than assumed.

---

## Stage 1 — the `DRIVE` sketch

New part, inches, 4dp (**Tools → Options → Document Properties → Units → IPS, 4 decimals**).

Sketch on the **Front plane**. The revolve axis is the **X axis**.

### 1a. Draw the shape first, dimension it second

Draw 13 lines as a closed loop, roughly to shape, then one construction centreline.
Approximate target vertices — draw roughly to these, the dimensions in 1b set the exact
values (x = along the axis from the ORB face, y = radius):

```
V1  (0.0000, 0.0000)   <- ON THE ORIGIN
V2  (0.0000, 0.3750)
V3  (0.4660, 0.3750)
V4  (0.4660, 0.3300)
V5  (0.5600, 0.3300)
V6  (0.5600, 0.5052)
V7  (0.8230, 0.5052)
V8  (0.8230, 0.3750)
V9  (1.2310, 0.3750)
V10 (1.2310, 0.3295)
V11 (1.3860, 0.2127)    <- cone small end; DERIVED from SEATB, do not dimension
V12 (1.4800, 0.2127)
V13 (1.4800, 0.0000)
back to V1 along the axis
```

Then: **Sketch → Centerline** along the axis. Make it **collinear with the X axis**, then
add a **Coincident** relation from its left endpoint to **V1** and from its right endpoint to
**V13**. This is what turns your diameter dimensions into diameters and what the revolve
uses as its axis.

> **Lock both endpoints or the sketch will never read Fully Defined.** Collinear alone
> removes only 2 of the centreline's 4 degrees of freedom — the endpoints stay free to slide
> along the axis, and SolidWorks counts construction geometry toward Fully Defined. This is
> the single easiest thing to get stuck on in this build.

**Relations to add (most will snap automatically — verify each one):**

- `V1` **coincident** with the **origin**
- **horizontal** on V2‑V3, V4‑V5, V6‑V7, V8‑V9, V11‑V12, V13‑V1
- **vertical** on V1‑V2, V3‑V4, V5‑V6, V7‑V8, V9‑V10, V12‑V13
- **leave V10‑V11 free** — that is the cone, and the 37° drives it

### 1b. Apply the 12 dimensions in this order

Rename each one *immediately* after you create it: double-click the dimension, and in the
PropertyManager the **top box under "Primary Value"** is the name. Renaming as you go is
what frees up the name `D1` for the last dimension.

| # | Select | Type | Value | Rename to |
|---|---|---|---|---|
| 1 | line V1‑V2 → line V3‑V4 | horizontal | `0.466` | `ORB_THDL` |
| 2 | line V3‑V4 → line V5‑V6 | horizontal | `0.094` | `ORB_GRVW` |
| 3 | line V7‑V8 → line V9‑V10 | horizontal | `0.408` | `JIC_CYL` |
| 4 | line V9‑V10 → **point V11** | horizontal | `0.155` | `JIC_SEATL` |
| 5 | **point V11** → line V12‑V13 | horizontal | `0.094` | `JIC_NOSEL` |
| 6 | line V2‑V3 + **centreline** | diameter | `0.750` | `THDMAJ_A` |
| 7 | line V4‑V5 + **centreline** | diameter | `0.660` | `ORB_GRVDIA` |
| 8 | line V6‑V7 + **centreline** | diameter | `1.0104` | `BODYDIA` |
| 9 | line V8‑V9 + **centreline** | diameter | `0.750` | `THDMAJ_B` |
| 10 | **point V10** + **centreline** | diameter | `0.659` | `JIC_CONEDIA` |
| 11 | line V10‑V11 + **centreline** | angle | `37` | `SEATB` |
| 12 | line V1‑V2 → line V12‑V13 | horizontal | `1.480` | `D1` |

For a **diameter** dimension: select the profile line *and* the centreline, then drag the
dimension across to the far side of the centreline before you click to place it. If it
reads as a radius, you placed it on the near side — undo and drag further.

For **#11**, if the angle comes up as 143° instead of 37°, pick the other pair of
quadrants; the value you want is measured **from the axis**, not from the vertical.

**Do NOT dimension:** the body length (0.263) or the nose diameter. Both are derived. The body length falls out of `D1` minus the right-hand chain; the nose diameter
falls out of `SEATB` acting on `JIC_CONEDIA` over `JIC_SEATL`.

### 1c. Check before you exit

The status bar must read **Fully Defined**. If it says **Under Defined**, check in this
order: (1) both **centreline endpoints** coincident with V1 and V13 — this is the most likely
culprit; (2) a missing horizontal or vertical relation. The cone line V10‑V11 is the only
profile entity that should have any freedom, and the 37° removes it.

If it says **Over Defined**, you have most likely dimensioned the body length or the nose
diameter as well. Delete that one.

**Expected outcome:** the nose land will land at **Ø0.4254**, against the published tip
diameter of 0.426. That 0.0006" difference is rounding in the 37° — it is the correct
consequence of driving the nose from the angle rather than dimensioning it, and it is why
the diagram marks Ø0.426 as derived.

Rename the sketch **`DRIVE`** in the tree.

---

## Stage 2 — Revolve

**Insert → Boss/Base → Revolve.** Axis = the centreline. 360°. Result is a **solid bar** —
no hole yet. That is correct.

Rename the feature `BODY`.

---

## Stage 3 — the hex

**Sketch on the Right plane** (the Right plane is at x = 0, normal to the axis).

**Tools → Sketch Entities → Polygon.** 6 sides. Centre **on the origin**. Choose
**Inscribed circle** — *not* circumscribed. Inscribed gives across-flats, which is what
`C4` publishes.

Dimension the polygon's construction circle to **Ø0.875** and rename that dimension
**`HEXB`**. That is 7/8 exactly — see the sourcing section above; Air-Way's printed 0.88 is a
two-decimal rounding, and modelling 0.880 would make every hex 0.005 oversize.

Add a **Horizontal** relation to the construction line running from the centre to a vertex,
to lock the rotation. (Which way you clock the hex is cosmetic — it changes nothing
dimensionally — but it must be locked or the sketch stays under-defined.)

Rename the sketch **`HEX`**.

**Insert → Cut → Extrude.** Direction 1 = **Through All**, tick **Direction 2 = Through
All** as well, and tick **Flip side to cut** so the material *outside* the hexagon is
removed. Rename the feature **`HEXCUT`**.

> **Why Through-All-Both is safe.** The cut only bites where the part is wider than the hex
> flats. I re-checked this across all 65 configurations using the exact MS51525 hex fractions:
> the hex flat radius exceeds the largest thread-major radius on every single one, worst case
> **+0.030"** on `6400-05-04-O`. Nothing outside the body section is ever touched, so you
> never need a length dimension on this cut.

---

## Stage 4 — the stepped bore

Both bore sketches go on the **Right plane** (x = 0). No face references, no reference
planes — those are what break when a design table drives 65 configurations.

**BORE_A — the ORB-end bore**

1. Sketch on the Right plane: one **circle**, centre on the origin, **Ø0.391**.
   Rename the diameter dimension `D4`. Rename the sketch **`BORE_A`**.
2. **Insert → Cut → Extrude.** Direction 1 = **Blind**, depth **0.6915**, pointing *into*
   the part. Rename the depth dimension **`DEPTH`**. Rename the feature **`BORECUT_A`**.

**BORE_B — the JIC-end bore**

3. Sketch on the Right plane: one **circle**, centre on the origin, **Ø0.391**.
   Rename the diameter dimension `D3`. Rename the sketch **`BORE_B`**.
4. **Insert → Cut → Extrude.** In the PropertyManager, open the **"From"** panel at the top
   and change **Sketch Plane** to **Offset**, value **0.6915**. Then Direction 1 =
   **Blind**, depth **0.7885** ( = 1.480 − 0.6915 ).
   Rename the offset dimension **`START`** and the depth dimension **`DEPTH`**.
   Rename the feature **`BORECUT_B`**.

The two cuts meet exactly at x = 0.6915, so there is never a web between them and never an
overlap.

> **If the "From → Offset" value won't take a name** in your SW2026 dialog, stop and tell
> me — I'll switch `BORE_B` to a reference-plane construction instead. I'd rather you not
> improvise this one, because it has to survive 65 design-table rebuilds.

### About that 0.6915 — this is an assumption, and I want it on the record

`BORESTEPL` is **not a catalog value**. No manufacturer publishes where the bore steps.
I've set it to the **mid-plane of the hex**: the hex spans 0.560 → 0.823, so
0.560 + 0.263/2 = **0.6915**.

Why I'm comfortable proposing it rather than blocking on it: the step location sits entirely
inside the fitting and affects **no released dimension**. It changes nothing on the
tabulated drawing, nothing on the spec sheet, and nothing about how the part fits or seals.
It shows up only in a section view and in the internal geometry of the STEP file. It is also
a design-table column, so if you ever measure a real one and it differs, the whole library
corrects without anyone re-cutting geometry.

If you'd rather not carry even that, say so and I'll leave `BORESTEPL` empty and gate those
rows `MISSING` instead.

---

## Stage 5 — threads

**Insert → Features → Thread.**

| | `THD_EndA` (ORB) | `THD_EndB` (JIC) |
|---|---|---|
| Start edge | circular edge at x = 0, on the Ø0.750 cylinder | circular edge at x = 1.231, where Ø0.750 steps down to the cone |
| Type | Inch Die | Inch Die |
| Size | 0.7500‑16 | 0.7500‑16 |
| Method | Cut thread | Cut thread |
| End condition | Blind, **0.466** | Blind, **0.310** |
| Direction | into the part (+X) | *toward the hex* (−X) |

`THD_EndB` runs 0.310 of the 0.408 cylinder, leaving **0.098 bare against the hex** — that
is the runout relief visible on the product photo.

**Then right-click each thread feature → Suppress.** Save the master with both suppressed.
That is the resting state; the macro unsuppresses them only while drawing views are built,
and re-suppresses from its error handler so a crash never leaves them live.

> **`THD_EndA` runs the full 0.466, which assumes zero runout relief at the ORB end.**
> README §9 notes there *is* a relief there and that nobody has quantified it. Modelling it as
> zero is a choice, not a measurement.
>
> **And `THD_EndA`'s 0.466 length is itself an assumption.** No source publishes ORB thread length —
> Parker's drawing says only "full threads to this point". The 0.466 is back-derived from
> the overall length, and there is a runout relief at the ORB end that nobody has quantified.
> Measuring runout at both ends off a physical part is already on your open-items list; until
> then this is `ASSUMED`, not `VERIFIED`.

---

## Stage 6 — save and check

Save as `C:\OMi\Masters\6400.SLDPRT`.

- [ ] `DRIVE` reads **Fully Defined**
- [ ] Feature tree reads: `DRIVE` → `BODY` → `HEXCUT` → `BORECUT_A` → `BORECUT_B` → `THD_EndA` → `THD_EndB`
- [ ] Both `THD_` features **suppressed**
- [ ] **Evaluate → Measure**: overall length **1.4800**
- [ ] **Measure**: hex across flats **0.8750** (measure flat-to-flat, not corner-to-corner)
- [ ] **Measure**: body diameter across the hex corners **1.0104** (self-fulfilling — BODYDIA is *defined* as hex/cos30, not published — so it checks your entry, not the part)
- [ ] **Measure**: bore **0.3910** at both ends, continuous, no step visible (correct for this size)
- [ ] Section view down the axis: one clean through-passage, no web at x ≈ 0.69
- [ ] **Tools → Evaluate → Check** reports a single solid body

---

## Open item you'll hit at batch time — flagging it now, not solving it here

`OMi_BatchDrawings.bas` finds thread features by the `THD_` prefix and suppresses or
unsuppresses them **per configuration**. That part works. But **nothing sets the thread
*size* per configuration** — the SolidWorks Thread feature takes its size from a dropdown,
not from a driving dimension, so a design table can't reach it the way it reaches
`D1@DRIVE`.

For the `6400-08-08-O` pilot this is a non-issue: one size, one thread. It becomes real the
moment you drive all 65 configs, where thread sizes run from 5/16‑24 to 2½‑12.

I have not solved this and I'm not going to guess at it. It needs settling before the first
full-topology batch. Tell me when you want me to take it on and I'll work out what the API
actually exposes.

---

## What I'll build once the master rebuilds cleanly

Design table header set for the regenerated `DesignTable_6400.xlsx`:

```
A                 config name = PartNumber_OMi
D1@DRIVE          overall length          Air-Way L5 = MS51525 L   VERIFIED
ORB_THDL@DRIVE    ORB thread length       UNSOURCED — see below
ORB_GRVW@DRIVE    O-ring groove width     EndGeometry
JIC_CYL@DRIVE     JIC cylinder length     UNSOURCED — see below
JIC_SEATL@DRIVE   seat length             EndGeometry
JIC_NOSEL@DRIVE   nose land               UNSOURCED — see below
THDMAJ_A@DRIVE    ORB thread major        from the thread callout
ORB_GRVDIA@DRIVE  groove root dia         EndGeometry
BODYDIA@DRIVE     body dia                = hex / cos30 (definition, not published)
THDMAJ_B@DRIVE    JIC thread major        from the thread callout
JIC_CONEDIA@DRIVE cone major dia          EndGeometry
SEATB@DRIVE       37                      constant
HEXB@HEX          hex across flats        MS51525 C1 exact fraction  VERIFIED
D4@BORE_A         ORB-end bore            Air-Way D(2)               ASSUMED (MS51525 tabulates only the JIC-side bore)
DEPTH@BORECUT_A   = BORESTEPL             ASSUMED
D3@BORE_B         JIC-end bore            Air-Way D(1) = MS51525 D   VERIFIED
START@BORECUT_B   = BORESTEPL             ASSUMED
DEPTH@BORECUT_B   = D1 − BORESTEPL        ASSUMED
$PRP@…            properties as before
$COMMENT
```

`BEND` is gone — straights don't need it, and a 0° angle is awkward to create. That drops
README §8 item 4.

**Coverage warning for that table:** **38 of the 65** configurations are clear of the
*EndGeometry* gaps. The other 27 are blocked — ORB groove width is
unpublished for ‑14/‑16/‑20/‑24/‑32, and JIC seat and thread length are unpublished for
‑20/‑24/‑32. `Parts_v2` currently scores the 6400 as 10 VERIFIED / 55 ASSUMED, but that was
scored against the old four-dimension model and is now optimistic. I'll re-score it when I
regenerate the table, and those 27 rows will come out `MISSING` and shaded, not silently
filled.

**And note the harder limit above it:** because `ORB_THDL`, `JIC_CYL` and `JIC_NOSEL` are
unsourced at *every* dash size, on the strict reading of your own rule **no** 6400
configuration is fully `VERIFIED` today — not even the 38. The 38/27 split is the count of
rows blocked *only* by the `EndGeometry` gaps. What MS51525 did buy us is that the overall
length, hex and JIC-side bore are now `VERIFIED` rather than `ASSUMED`; the remaining block is
purely the axial breakdown, and it clears the moment SAE J514/1 arrives or you measure a part.
