# Female 37deg JIC swivel end - measured on the Brennan 6500-FG STEPs (2026-09-24)

Method: each Brennan STEP (inch units, one solid per file) was sectioned with a plane through both leg axes (OpenCascade `BRepAlgoAPI_Section`), and the swivel-leg edges were read as exact lines, cones and arcs. All axial values are measured **from the nut face**. Radii are in inches. The same numbers are in `SWIV_MEAS` in gen_straight2.py; gen_tee.py reuses them.

| value | meaning | -04 | -08 | -12 | -16 |
|---|---|---|---|---|---|
| AF | nut hex across flats (Brennan = Air-Way C3) | 0.5625 | 0.875 | 1.25 | 1.5 |
| HEXL | nut hex length, face -> foot of the rear 45deg chamfer | 0.3268 | 0.4499 | 0.5998 | 0.6564 |
| SKF | skirt radius at the front | 0.2796 | 0.4361 | 0.6237 | 0.749 |
| SKS | end of the 8deg skirt taper (from the nut face) | 0.509 | 0.647 | 0.847 | 0.909 |
| SKR | skirt radius behind the taper | 0.2574 | 0.4108 | 0.5928 | 0.727 |
| NUTL | nut rear face (from the nut face) | 0.649 | 0.827 | 1.047 | 1.139 |
| NECKR | body neck radius behind the nut | 0.1465 | 0.292 | 0.417 | 0.5485 |
| BODYS | body face = end of the forged arm (from the nut face) | 0.685 | 0.885 | 1.089 | 1.175 |
| MINR | thread minor radius (= ASME B1.1 basic minor) | 0.1917 | 0.3412 | 0.4862 | 0.6112 |
| TE | end of the thread minor (from the nut face) | 0.2867 | 0.3567 | 0.4851 | 0.5252 |
| RELR | relief counterbore radius (45deg from the minor) | 0.235 | 0.3925 | 0.549 | 0.665 |
| FLOOR | floor of the slot around the nose (from the nut face) | 0.5243 | 0.6723 | 0.8623 | 0.9544 |
| NOSER | nose outer radius | 0.1845 | 0.34 | 0.481 | 0.604 |
| NOSETIP_B | nose tip = seat mouth plane (from the nut face); Air-Way M5-M10 is 0.01 less | 0.35 | 0.43 | 0.57 | 0.6 |
| SEATR | seat mouth radius (37deg seat down to the bore) | 0.145 | 0.2825 | 0.4225 | 0.5475 |

Constant at all four sizes:

- countersink from the thread major down to the minor at **50 deg**,
- relief cone from the minor up to the counterbore at **45 deg**,
- seat at **37 deg**.

Air-Way cross-checks at all four sizes:

- the nut hex equals C3,
- the nut face equals M5 (6500) or L (straights),
- the nose tip equals M10 within 0.01,
- the straights' nut-face-to-seat length (L to the nut face minus L to the seat) equals M5 - M10 of the 6500 at every size (0.34 / 0.42 / 0.56 / 0.59).

**Not modelled:**

- the nut/body joint (collar, 9 crimp dimples, the rear undercut behind the nut lip),
- the hex chamfers and the fillets.

The nut and the body are one solid, as they are in the Brennan STEP.

**Single source (Brennan):** every row built with these values is ASSUMED.

**Still to measure:** other swivel sizes (-05, -06, -10, -20, -24, -32) each need their own STEP.
