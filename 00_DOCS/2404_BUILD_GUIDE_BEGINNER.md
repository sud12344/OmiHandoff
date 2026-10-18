# Building the 2404 Master Model — Step-by-Step Guide (no experience assumed)

You are going to build **one** 3D model of the 2404 fitting. Later, a spreadsheet will drive
this one model to produce all 45 sizes automatically. So it pays to go slowly and get this
one right.

We build the size called **2404-04-04**, because we have its complete measured geometry.

**The idea in one sentence:** draw the part's outline (half of its cross-section), spin that
outline around its centerline to get a solid, cut the hex flats, drill the holes, add the
threads, done.

Every number you will type is listed in the tables below — you never have to calculate
anything.

---

## Before you start (2 minutes)

1. Open SOLIDWORKS. **File → New → Part → OK.**
2. Set the units: **Tools → Options → Document Properties tab → Units.**
   Click **IPS (inch, pound, second)**. In the Length row, set **Decimals = .1234** (four
   places). Click OK.

> **Why:** the part is dimensioned in inches to 4 decimal places. If you skip this you'll
> fight the software all day.

---

## Stage 1 — Draw the outline (the `DRIVE` sketch)

### 1a. Start the sketch

1. In the tree on the left, click **Front Plane** once.
2. A small popup of icons appears — click the **Sketch** icon (a pencil over a square).
   The screen rotates to face you and the top toolbar changes: you're now "in" a sketch.
3. You should see a small **red/orange dot** in the middle of the screen. That is the
   **origin** — the anchor point everything hangs off. Everything below assumes it's visible.
   If you can't see it: **View → Hide/Show → Origins**.

### 1b. Draw the shape — rough first, exact later

This is the most important habit in SOLIDWORKS: **draw sloppy, then let the dimensions make
it exact.** You do NOT need to click precise points.

1. Press **L** (or click the **Line** tool).
2. Click once **on the origin dot** to start.
3. Now click, click, click to make the chain of lines below. Go roughly to the right shape —
   up, across, up, across, down… Each click ends one line and starts the next.
   The shape you're tracing (left = pipe-thread end, right = flare end):

```
        ┌────────────┐                                  the tall box = body (hex-to-be)
   ┌────┘            │      ┌─────────┐
   │                 │  ╱───┘         └──╲               two slopes = the 60° ramp (left)
   │                 └──┘                 ╲──┐           and the 37° cone (right)
   │                                         │
   ●─────────────────────────────────────────┘          bottom edge sits ON the centerline
   ^origin
```

   In words, from the origin: **up** (pipe end face) → **right** (long pipe section) → **up**
   (step to the body) → **right** (body) → **down** (other body face) → **right** (short flat) →
   **up-right slope** (the 60° ramp) → **right** (thread section) → **down** (small step) →
   **right** (short flat) → **down-right slope** (the 37° cone) → **right** (short tip) →
   **down** to the axis → **left all the way back** to the origin. That last long line closes
   the loop.
4. Press **Esc** to put the Line tool away.
5. Count: you should have **13 lines around the outside plus the long bottom line** = a
   closed loop. If a line is missing the shape won't shade in — add it.

Don't worry if it looks lumpy. That's expected.

### 1c. Add the centerline

1. Click the little arrow under the Line tool → choose **Centerline**.
2. Draw it **along the bottom edge**, from just left of the origin to just past the right end.
   Press **Esc**.
3. Now tell SOLIDWORKS it lies exactly on the horizontal axis: click the centerline, then in
   the left panel click **Horizontal** under "Add Relations". 
4. **Pin its two ends down** (critical, easy to miss):
   - Hold **Ctrl**, click the centerline's **left endpoint** and the **origin**. In the left
     panel click **Coincident**. 
   - Hold **Ctrl**, click the centerline's **right endpoint** and the **bottom-right corner**
     of your outline. Click **Coincident**.

> **Why this matters:** without step 4 the sketch will *never* say "Fully Defined" no matter
> what you do, and you'll have no idea why. This is the number-one time-waster in this build.

### 1d. Straighten the lines (relations)

Relations are little rules like "this line is exactly vertical". Many get added automatically
while you draw (you'll see tiny green symbols). Check each line and add what's missing:

- Click a line once. The left panel shows its existing relations.
- To add one: with the line selected, click **Horizontal** or **Vertical** in the left panel.

Make **vertical**: the pipe-end face (leftmost), both body faces, the small step after the
thread section, and the tip face (rightmost).
Make **horizontal**: the pipe section, the body top, the short flat before the ramp, the
thread section, the short flat after the step, the tip flat, and the long bottom line.

**Leave the two slopes alone** — the 60° ramp and the 37° cone stay tilted. Their angles get
dimensioned in the next step.

### 1e. Make it exact (dimensions)

1. Press **S** then click **Smart Dimension** (or find it on the toolbar — it looks like a
   dimension line with arrows).
2. To dimension a **length**: click the first line, click the second line, move the mouse and
   click to place the number, type the value, press **Enter**.
3. To dimension a **diameter**: click the outline line, then click the **centerline**, then —
   before placing it — **drag the cursor to below the centerline** and click. The number
   doubles (it becomes a diameter, not a radius). This to-the-far-side drag is the trick.
4. To dimension an **angle**: click the sloped line, then the centerline, place the number.
5. **Rename every dimension right after you create it:** double-click the dimension number; in
   the panel on the left there's a **name box** at the top of "Primary Value" (it says
   something like `D1@Sketch1`). Select just the part before the `@` and type the new name.

> **Why rename:** the spreadsheet that will drive all 45 sizes finds each dimension **by
> name**. Wrong name = broken automation.

Apply these 13, in this order:

| # | What to click | Kind | Type this | Name it |
|---|---|---|---|---|
| 1 | pipe-end face line + centerline | diameter | `0.540` | `PIPEOD` |
| 2 | pipe-end face line → first body face | length | `0.560` | `NPTF_ENDL` |
| 3 | body top line + centerline | diameter | `0.6495` | `BODYDIA` |
| 4 | the short flat right after the body | length | `0.075` | `JIC_RELIEFL` |
| 5 | the 60° ramp + centerline | angle | `60` | `RELIEFANG` |
| 6 | thread section line + centerline | diameter | `0.4375` | `THDMAJ_B` |
| 7 | thread section line (its length) | length | `0.2608` | `JIC_THDZ` |
| 8 | the flat after the small step + centerline | diameter | `0.364` | `JIC_CONEDIA` |
| 9 | that same flat (its length) | length | `0.0795` | `JIC_LANDL` |
| 10 | the 37° cone + centerline | angle | `37` | `SEATB` |
| 11 | the 37° cone's flat neighbour → tip face (the cone's length along the axis) | length | `0.1135` | `JIC_SEATL` |
| 12 | pipe-end face → tip face | length | `1.4200` | `D1` |

**One more rule (not a number):** the first short flat (step 4's line) and the flat in
step 8/9 both sit at Ø0.364, but do NOT give the first one a diameter and do NOT use
Equal (Equal makes line LENGTHS match — wrong here, the two flats are different lengths).
Instead: hold **Ctrl**, click **both** flat lines, and click **Collinear** in the left
panel — that puts them at the same height, and the relief flat inherits Ø0.364 from
`JIC_CONEDIA` automatically while keeping its own length.

If an angle comes out as 143° or 88°: you dimensioned to the wrong side. Delete it (click it,
press Delete) and pick the other opening between the two lines.

**Deliberately NOT dimensioned** (the software works these out):
the hex section's length (comes out 0.310), the tip diameter (comes out 0.1929 — catalogs
say 0.193, and that near-match is your proof the sketch is right), and the 60° ramp's
length (0.0212). If you dimension any of these the sketch turns Over Defined.

**A companion picture of all of this** — every dimension drawn on the part, colour-coded —
is in `2404_master_dimensions.png`. Keep it open on a second window while you work.

### 1f. The finish line

Look at the **bottom-right corner of the screen**. It should say **Fully Defined**, and every
line should have turned **black** (blue = still loose).

- Says **Under Defined?** → 90% of the time it's the centerline endpoints from step 1c-4.
  Otherwise a missing vertical/horizontal from 1d.
- Says **Over Defined?** → you dimensioned one of the "deliberately not dimensioned" items,
  or added a duplicate. Delete the extra.

Finally: in the tree, slow-double-click the sketch's name (probably `Sketch1`) and rename it
exactly **`DRIVE`** — capitals matter.

Click the **exit-sketch icon** at the top-right corner of the drawing area.

---

## Stage 2 — Spin it into a solid (30 seconds)

1. Click `DRIVE` in the tree.
2. **Insert → Boss/Base → Revolve.**
3. It will ask for an axis — click your **centerline**. A preview of the round part appears.
4. Make sure it says **360deg**, click the green ✓.

You now have a solid, round part with no hole. Rename the feature (slow-double-click in the
tree) to **`BODY`**.

---

## Stage 3 — Cut the hex (the wrench flats)

1. In the tree click **Right Plane** → **Sketch**. (Right Plane faces down the axis, so
   you're looking at the round end of the part.)
2. **Tools → Sketch Entities → Polygon.** In the left panel set sides = **6** and make sure
   **Inscribed circle** is selected — *not* circumscribed. (Inscribed makes the number you
   type the distance across the FLATS, which is what a wrench grabs and what catalogs list.)
3. Click on the **origin**, drag outward a bit, click again. A hexagon appears with a dashed
   circle inside it.
4. Smart Dimension → click the **dashed circle** → type **`0.5625`** → rename it **`HEXB`**.
5. The hexagon can still spin. Click the dashed construction line that runs from its centre
   to one corner, and add a **Horizontal** relation. Now: Fully Defined.
6. Rename the sketch **`HEX`**. Exit the sketch.
7. **Insert → Cut → Extrude.** In the left panel:
   - Direction 1: choose **Through All - Both** from the dropdown (cuts both ways).
   - Tick **☑ Flip side to cut** — you want to cut *outside* the hexagon, shaving the round
     body down to flats, not punch a hexagonal hole.
   - The preview arrows should point **outward**. Green ✓.
8. Rename the feature **`HEXCUT`**.

The middle of your part is now a hex. The ends are untouched — the hex flats
(radius 0.2813) sit farther out than anything on the ends, so the cut can't reach them.

---

## Stage 4 — The holes

**Hole 1 — straight through:**

1. Right Plane → Sketch. Draw a **Circle** centred on the origin.
2. Smart Dimension the circle → **`0.172`** → rename the dim **`D3`**. Rename the sketch
   **`BORE_THRU`**. Exit.
3. **Insert → Cut → Extrude** → Direction 1 = **Through All - Both** → ✓.
   Rename **`THRUCUT`**.

**Hole 2 — the wider counterbore at the pipe end:**

4. Right Plane → Sketch → Circle on the origin → **`0.281`**, rename dim **`CBDIA`**,
   sketch name **`BORE_A`**. Exit.
5. **Insert → Cut → Extrude** → Direction 1 = **Blind**, depth **`0.690`**. Look at the
   preview arrow — it must point **into the pipe end** (the left/NPTF end). If it points the
   wrong way click the little reverse-direction button next to the depth box. Green ✓.
   Rename the depth dimension **`DEPTH`**, the feature **`CBCUT_A`**.
6. Repeat 4–5 as a mirror-image for the other end (circle `0.172`, sketch **`BORE_B`**,
   blind cut toward the JIC end, feature **`CBCUT_B`**) — then **right-click `CBCUT_B` in
   the tree → Suppress** (it goes grey). On this size the counterbore belongs to the pipe
   end only; other sizes flip it, and the spreadsheet will do the flipping by
   suppressing/unsuppressing these two features.

---

## Stage 5 — Threads (then switch them off)

Threads are heavy geometry, so the master keeps them **suppressed** (dormant); the drawing
macro wakes them only while making drawings.

1. **Insert → Features → Thread.** (If a warning about decorative vs cut threads pops up,
   just OK it.)
2. **Pipe end:** click the circular **edge** of the pipe-end face.
   - Type: **Inch Tapered Pipe** · Size: **1/4-18** · Method: **Cut thread**
   - End condition: **Blind**, **0.4018**, threading **into** the part. Green ✓.
   - Rename **`THD_EndA`**.
3. **Flare end:** Insert → Features → Thread again; click the circular edge where the Ø0.4375
   thread section begins (at the top of the 60° ramp).
   - Type: **Inch Die** · Size: **0.4375-20** · Method: **Cut thread**
   - Blind, **0.2608**, toward the tip. Green ✓. Rename **`THD_EndB`**.
4. **Right-click each thread feature → Suppress.** Both grey. That is their normal state.

> The pipe end of the blank is a plain cylinder on purpose — the tapered-pipe thread feature
> supplies the taper itself. (Modelling the taper *and* using a tapered thread doubles it.)

---

## Stage 6 — Check your work (5 minutes, worth it)

**File → Save As** → `C:\OMi\Masters\2404.SLDPRT`.

Use **Tools → Evaluate → Measure** and click the faces/edges to check:

| Measure | Must read |
|---|---|
| End to end | **1.4200** |
| Across the hex flats (flat to flat, not corner to corner) | **0.5625** |
| Hex section length | **0.3100** |
| Hole at the flare end | **0.1720** |
| Hole at the pipe end | **0.2810** (and it steps down 0.690 deep) |
| Flare tip diameter | **0.1929** |

Tree should read: `DRIVE → BODY → HEXCUT → THRUCUT → CBCUT_A → CBCUT_B (grey) → THD_EndA
(grey) → THD_EndB (grey)`.

If all six numbers check out, the master is right, and every one of the measured numbers in
`DesignTable_2404_v3.xlsx` will drop straight onto it. Tell me and we'll do the design-table
insertion together — that step has its own gotchas and I'd rather walk it with you live.
