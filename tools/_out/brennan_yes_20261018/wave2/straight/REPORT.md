# Wave 2 straight - report (saved by the main session from the agent's hand-back, 2026-10-18)

87 rows: **23 ready** (all became configurations; applied to the stage), **18 blocked**, **46 held**.

**Ready (23)**
- 2403-04-02 / -10-04 / -16-10 / -24-16, 2403-LH-24-24
- 2405-10-06 / -14-12
- 2406-03-04
- 2700-02-02 / -LN-02-02
- 2706-04-02 / -LN-04-02
- 5000-06-02 / -16-08
- 5405-04-02 / -04-12 / -08-04 / -20-20 / -24-20
- 5406-32-04, 5406-C-20
- 6405-02-02-O / -02-04-O

**Blocked (18), all 5404-N.** The data is complete:
- L from the part number (= Brennan).
- Bar diameter and bores from the Air-Way nipple of the same size (A4).

SPEC 5404N only reads "5404-N-4-4 X 2"-style part numbers, so the OMi form fails with "no dash pair". Generator work needed.

**Held (46)**
- 15 have no source: 3D-file rows with no STEP on disk.
- 2705-04-02 and -LN: the -02 bulkhead I1 has no source.
  - The two measured Brennan -02 parts differ (1.07 / 1.11).
- 6 wait on A9: 5000-24-20, 5405-16-24, 5405-20-32, 5406-C-24, 5406-C-32, 5406-40-32.
- 3 need a -40 pipe-thread end in the generator: 5000-40-40, 5404-40-40, 5406-40-32 (STEPs on disk).
- 0304-C-02 and 0306-02: there is no female -02 JIC shape.
- 6410-04-02-O: no -02 port drill or female ORB port.
- 6400 x6: no SPEC yet (A6).
- 2404-L-32-32: held by Q-HANDMADE.
- 6410-32-20-O / -32-24-O: the A11 caps are now applied (`test/edits_A11.csv`), but the groove width at -32 is still empty (see the
  library side effect below).
- 6420 x2, 6425 x6, 6900 x1: no SPEC and no dimension columns; values are in the rows.csv notes only.

**Test** (batch-16 tools, every straight and tee root)
- Only the 23 target rows are added; every existing SW2 cell is unchanged; regress 0.
- Checks OK: vbacheck, dofcheck 34 / 34, allcfg 18 roots 0 problems.
- Side effect found: the generator builds its ORB end library from ANY 6401 / 6405 / 6410 row that has a groove width, whatever its
  status. Filling those columns on unbuilt rows changed the `$COMMENT` of 3 built configurations, so those cells were dropped.
- 5405-08-04 / -24-20: the Brennan bore is wider than the tap drill (0.051 / 0.010 step). The generator note calls it an Air-Way bore;
  it is Brennan's.

**Conflicts (none picked)**
- 6410-32-20-O length: Air-Way = OMi 1.43, Brennan 1.00 -> kept 1.43.
- 5404-N bores: Air-Way transfer 0.30 / 0.39 / 0.48 used (A4); Brennan prints 0.281 / 0.406 / 0.531.
- 6420-08-08: four different lengths - 1.320 / 1.5 / 1.500 / its own STEP 1.620 (Q-NEW-F3-6420-0808-OAL).
- -02 bulkhead I1: each part uses its own STEP value (2700-02-02 1.07, 2706-04-02 1.11; measured with `scripts/measure_bulkhead.py`,
  validated on 2705-08-08 = 1.44).

**Mapping notes**
- Good agreement: 2403, 2403LH, 2700, 5000, 5404, 2405, 2706.
- 2406 length matches Air-Way 16 / 47 (different bodies).
- 5406-C length 0 / 6 (Brennan caps are shorter).
- 6900: nothing proposed (does not pair).

**Generator work to schedule:** 5404N reading the OMi part-number form (+ the -06 thread-end fix); a -40 pipe-thread end; a -02 female
ORB port.
