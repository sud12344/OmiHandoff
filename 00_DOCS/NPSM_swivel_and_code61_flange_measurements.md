# NPSM swivel end (1404/1405) and code 61 flange head (1700): Brennan STEP measurements (2026-09-24)

Method: same as the 6500 swivel. Each Brennan STEP (inch units, one solid) was cut through its axis with OpenCascade, and the exact edges were read off. Solid and air were then checked point by point in the nut region. All values are in inches.

## Female NPSM swivel, size -08 (Brennan 1404-08-08)

Nut values are measured from the **nut face**:

| value | measured |
|---|---|
| nut hex across flats | 1.00 (= Air-Way C(2)) |
| nut hex length | 0.40 |
| 14 deg skirt cone | from dia 1.00 at 0.40 to dia 0.91 at 0.58 |
| lip | dia 0.91, from 0.58 to the nut rear face at 0.72 |
| countersink | 45 deg, from dia 0.823 to the thread minor |
| thread minor | dia 0.759; ASME B1.20.1 NPSM internal minor is 0.7594 min |
| thread | straight 1/2-14 NPSM to 0.388; 45 deg relief to dia 0.823 at 0.42 |
| relief counterbore | dia 0.885, to the lip front face at 0.595 |

Stem values are measured from the **stem tip**:

| value | measured |
|---|---|
| 30 deg male cone | from dia 0.562 at the tip to dia 0.74 at 0.1542 |
| stem OD | 0.74 |
| neck | dia 0.608 |
| body face | 0.48 behind the tip |

Bore:

- 0.531 on the pipe side, 0.46 on the stem side.
- The step is at the body-hex mid-plane, which is the same convention the generator uses.

**Placement (your decision 2026-09-24, follow Air-Way):**

- The stem tip sits at Air-Way L and the nut face at Air-Way W.
- Air-Way W - L = 0.33 at every -08 row, against Brennan's 0.28, so the modelled nut sits 0.05 further out.
- Everything else matched Brennan exactly: L (1.61), the male pipe end (0.75) and the body hex length (0.38).

**Not modelled:**

- the nut/collar joint (the nut and body are one solid, as in the STEP),
- the rear undercut under the nut lip and the 0.005 slot at the collar,
- the chamfers,
- the internal 30 deg chamfer at the male pipe tip.

Only the -08 swivel can be built. Other sizes need their own STEP.

## SAE code 61 flange head (Brennan 1700-08-08, 1700-12-12, 1700-24-24)

| flange | head dia | head thickness | O-ring groove ID / OD | groove depth | bore |
|---|---|---|---|---|---|
| -08 | 1.188 (Air-Way O 1.19) | 0.265 | 0.69 / 1.00 | 0.11 | 0.391 |
| -12 | 1.500 (Air-Way O 1.50) | 0.265 | 0.94 / 1.25 | 0.11 | 0.609 |
| -24 | 2.375 (Air-Way O 2.38) | 0.315 | 1.805 / 2.115 | 0.11 | 1.312 |

The JIC ends of all three STEPs equal the MS33656J chain.

**Your decision 2026-09-24 (follow Air-Way):**

- The overall length is Air-Way L28.
- The body is a hex of Air-Way C over the whole length between the JIC end and the flange head. Air-Way publishes no neck, so the hex runs the full length.

**How Brennan differs:**

- Brennan uses a round collar of dia O with two wrench flats (1.00 / 1.374 / 2.00) plus a neck.
- Brennan's parts are longer: 2.60 / 2.75 / 3.50, against Air-Way 2.36 / 2.63 / 3.02.

SAE J518 is not available, so the head thickness and the groove come from Brennan alone, and every 1700 row is ASSUMED.
