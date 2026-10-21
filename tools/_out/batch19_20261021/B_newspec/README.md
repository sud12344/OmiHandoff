# Batch 19, group B: new review tables / generator SPECs from data in hand (2026-10-20)

Folder `tools/_out/batch19_20261021/B_newspec/`. STAGED, not shipped. No SolidWorks call was made. Nothing outside this folder was written:
not `04_DESIGN_TABLES`, `03_SCRIPTS`, `11_MASTERS`, `01_MASTER_DATA`, or `tools/`. (A `patch --dry-run`-style test ran on a copy in the session
scratchpad.) Python ran with `-I -B`.

Scope: the 14 parts of BLOCKED_NEEDS (d) "New review table / SPEC from data already in hand": 3474 x9, 2613-04-04-04-FG, 6316-08 / -12 / -16,
6420-08-08.

| family | parts | result |
|---|---|---|
| 3474 adjustable male ORB x male ORB straight | 9 | **GENERATES** - 9 configurations, new SPEC + adjustable-ORB end module in gen_straight2 |
| 2613-04-04-04-FG forged MP-FP-MJ tee | 1 | **GENERATES** - 1 configuration, new SPEC in gen_tee (existing leg kinds) |
| 6316 FJS buttweld straight | 3 | **BLOCKED** - new review table staged (MISSING); butt-weld end has no shape source and the catalog's "A Weld" column is ambiguous |
| 6420-08-08 FORB-FP straight | 1 | **BLOCKED** - cells staged (MISSING); at OMi's 1.5 the library ports overlap, and the Brennan STEP is a different body. Needs a user decision plus a small generator mode |

So **10 of the 14 parts now generate** (3474 x9 and 2613-04-04-04-FG). The static checks and the OCP closed loop pass, and the regeneration
of all roots changes nothing else. The SolidWorks dry run is still to do: the kit is in `dryrun/`.

## Files

| path | what |
|---|---|
| `04_DESIGN_TABLES/` | full copy of the live tables. Changed: `DesignTable_3474.xlsx`, `DesignTable_2613.xlsx`, `DesignTable_6420.xlsx`. New: `DesignTable_6316.xlsx` |
| `CHANGES.csv` | every cell written (164: 3474 104, 6316 48, 6420 10, 2613 2), old -> new, with the source |
| `patches/gen_straight2_3474.diff`, `patches/gen_tee_2613.diff` | unified diffs against the live generators |
| `patches/measure_orb_straight.py.diff`, `patches/measure_straight_model.py.diff` | two new measuring files (the 2026-10-02 3474 work, unchanged except one comment) |
| `tools/` / `tools_live/` | the patched toolchain / a byte copy of the live one (sha256 in `checks/patch_apply_test.txt`) |
| `scripts/patch_gen_straight2.py`, `scripts/patch_gen_tee.py` | build `tools/` from `tools_live/`. Every hunk is anchored with `assert count == 1`, so they can be re-run on a merged base if another batch-19 group patches the same generators |
| `scripts/make_tables.py` | builds the four tables from the LIVE tables. It stops if a value it would write differs from a value already in the table |
| `regen/` | all SPEC roots, three sets: `live`, `patched`, and `control` (live tools on the repo tables). `regen/cmp.txt` is the comparison |
| `checks/` | dofcheck, allcfg, vbacheck, regress (`SUMMARY.txt`), `closed_loop_3474.txt`, `patch_apply_test.txt` |
| `evidence/catalog/` | Brennan TFA pages 9, 13, 17 and 53, plus a crop of the 6316 drawing. `evidence/ocp/` = the OCP rebuilds of the 9 3474 configurations |
| `dryrun/sw_calls_3474.json`, `dryrun/sw_calls_2613.json` | SolidWorks dry run for the PC session: `python sw_mcp/call.py @<file>`. It writes only to `dryrun/out` |

## 1. 3474: adjustable male ORB x male ORB straight (9 parts, GENERATES)

**Which parts exist.** `07_RAW_EXTRACTS/omi_feed/omi_skus_all.txt` lists 9 SKUs: 3474-04/-06/-08/-10/-12/-16/-20/-24/-32-NWO, with equal
dashes. All 9 are rows of the table: the 7 original rows plus -08 and -10, which were added on 2026-10-18 (adapters77).

**Shape.** Brennan TFA p.9, "MAORB-ORB STRAIGHT" (`evidence/catalog/TFA_p9.png`):

- **End A** (first dash) is an adjustable male ORB: thread, O-ring undercut, back-up washer, and a locknut with 15 deg chamfers on both faces,
  then a neck.
- The **body** is a hex (C2).
- **End B** is a fixed male ORB: thread, groove, against the hex face.
- One drill runs straight through.

No existing straight master has an adjustable end, so this is a new master. The end is the gen_tee `leg_NWO` module (built clean on 6801-6804
in batch 13b), ported to gen_straight2. This port is the 2026-10-02 design (`tools/_out/newmasters_20261002/work/3474/NOTES.md`), applied to
the batch-18 generator.

**Sources per column** (every row; the full citation is in `$PRP@AxialSource`):

| column | source |
|---|---|
| L1@DRIVE, C1HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE | Brennan TFA p.9, table 3474-NWO (`catalog_verified.json` TFA-p009-t06), columns L1 LGTH / C1 HEX / C2 HEX / B1 DRILL / B2 DRILL. **DimSource BRENNAN** (Brennan allowed and marked, user 2026-10-18). Air-Way prints no 3474 page. OMi's file gives names only (Items rows 1105-1113) |
| ORB_I3@DRIVE, ORB_THDL@DRIVE, ORB_GRVDIA@DRIVE | end library: the `DesignTable_6801.xlsx` row 6801-dd-dd-NWO-FG of the same ORB size (Air-Way; I3 = the Brennan 6801 STEP). Q-TRANSFER-ENDLIB = yes (2026-10-08) |
| THDMAJ_A / THDMAJ_B | SAE J1926 dash -> UN thread (standard), which matches the catalog B1 AORB / B2 ORB |
| stud geometry (washer, neck, nut thickness) | -12: measured on the part's own STEP `BRENNAN_3474-12-12-NWO.stp` (`NWO_MEAS_3474`). All other sizes: transferred from the Brennan 6801 STEP of the same ORB size (gen_tee `NWO_MEAS`, Q-TRANSFER-ENDLIB) |
| fixed ORB end (End B) | the ORB end dict (6401 / 6405 / 6410 / 6408 rows). At -12 it equals the own STEP |

**DataStatus:** MISSING -> **ASSUMED** on all 9 rows. The dimensions have one source (Brennan's catalog). The generator would also demote
VERIFIED to ASSUMED, because the stud is single-source.

**Modelling assumptions.** These are written into every row's `$PRP@AxialSource` (MODEL part):

- The locknut is a revolved envelope cut to its hexagon. The chamfer starts 0.005 outside the flats circle (cosmetic).
- The nut sits backed off against the washer. Nut, washer and body are one solid.
- Not modelled:
  - the O-rings;
  - the tip chamfers and thread run-outs;
  - the body-hex end chamfers;
  - the 0.002 marking recesses.
- The body hex and the locknut are each cut over their own zone (two `ZoneHexCut`s). The round washer is never cut.
- Bore step at the body-hex mid-plane. This has no effect, because D1 = D2 on every size.
- -04 rows also carry a note: the Brennan 6410-04-02-O STEP has a 0.285 fixed -04 thread, against 0.265 in the dict.

**Generator patch** (`patches/gen_straight2_3474.diff`, 301 lines, touches only code reached by SPEC 3474 / kind NWO):

- New constants and functions:
  - constants `NWO_CHANG`, `NWO_CH_DR`, `NWO_RN_MARGIN`, `NWO_MEAS_3474`, `ORB_FIXED_OWNSTEP_3474`;
  - `NWO_3474_TRANSFER = True`, dated to the 2026-10-08 Q-TRANSFER-ENDLIB answer;
  - functions `assume_3474`, `nwo_stud`, `end_ORBM_3474`, `end_NWO`, `end_NWO_row`, `nwo_nut_removed`.
- `SPEC['3474']`.
- In `build_rows`:
  - the thread check accepts NWO;
  - the adjustable end skips the "radius above the hex" checks and gets its own neck, wall and source-difference checks;
  - zone-cut columns `START@HEXCUT` / `DEPTH@HEXCUT`;
  - VERIFIED -> ASSUMED.
- In `emit`:
  - the `NWA_*` DRIVE dimensions (20 points, rank 40 = 40, 0 redundant);
  - the two zone hex cuts, with a check that NUTCUTA removes exactly the analytic nut-envelope volume.

The 2026-10-02 "no buildable row" branch of `__main__` is already live, so it was not re-added.

**For the user:**

- **3474-12-12-NWO adjustable thread length.** Built to Air-Way's 6801-12 value, 0.469, under the 2026-10-20 Air-Way-first rule. The own
  Brennan STEP measures 0.410. This was open as Q-CONFLICT-ORBTHDL-12. The `$COMMENT` of the generated row says "DIFFERS ... built to the row".
- **Necks on the other sizes.** These are transferred from the 6801 stud. At -12, the 3474 neck (0.945) differs from the 6801 neck (1.000),
  so the transfer is an assumption at every other size.
- **Air-Way 6407 page.** The "6407 Straight Thread Adjustable Union" page (series 96, `AirWay_Series_Survey.xlsx`) was never retrieved. If it
  covers these sizes, the Air-Way-first rule would put its values ahead of Brennan's (Q-NEW-6407SIB, open). It was not fetched.

## 2. 2613-04-04-04-FG: forged male pipe run x female pipe run x male JIC branch tee (GENERATES)

**Which parts exist.** OMi lists 2613-04-04-04-FG and 2613-08-08-08-FG. The second has no Air-Way row, no catalog row and no STEP, so it
belongs to BLOCKED_NEEDS (b) and is not in this task. The 4 plain Air-Way rows stay DROP.

**Shape.** Brennan TFA p.53, "MP-FP-MJ TEE"; OMi: "04 MP - 04 FP - 04 MJ Tee Forged":

- A1 male NPTF run on +X;
- A2 female NPTF run on -X;
- B3 male JIC branch on +Y.

These are the gen_tee leg kinds NPTFM / NPTFF / JICM and the forged-tee body of the built 2611 / 5603 masters, in another order. A new SPEC
is enough and no code changed (`patches/gen_tee_2613.diff`, 23 lines). It is its own master: no existing tee has this leg arrangement.

**Sources:**

- The row was staged on 2026-10-18 and was already in the live table. Every value was re-checked against the catalog:

  | column | catalog column | value |
  |---|---|---|
  | N5 | L | 1.090 |
  | N1 | L1 | 0.880 |
  | M1 | M | 1.220 |
  | Y1 | Y FLATS | 0.750 |
  | D1 | A1 DRILL | 0.281 |
  | D | B3 DRILL | 0.172 |

- TAPDRILL 0.43 is Air-Way s181's per-size value (A1).
- Thread majors are standard.
- DimSource BRENNAN.
- DataStatus MISSING (toolchain gate) -> **ASSUMED**.

**Assumptions** (`assume_extra`):

- There is no Brennan 2613 STEP. The body pattern (hex run bar, branch arm, 0.26 female collar) is the one measured on the Brennan 2611 / 2606 /
  5603 STEPs.
- The female port's connecting drill is the tap drill carried to the crossing (the existing library rule).

**For the user:** Air-Way s181 prints the PLAIN 2613-04-04-04, which is a different part. It agrees on N5, N1, Y1, D1, D and TAPDRILL, but its
M1 is 1.01 against Brennan's forged 1.22. The model uses Brennan's -FG value, and this is noted in `$COMMENT`. If you read Air-Way's plain row
as "Air-Way prints a value", M1 would be 1.01. Both values build.

## 3. 6316-08 / -12 / -16: FJS buttweld straight (BLOCKED, new table staged)

OMi Items rows 1620-1622 ("08 / 12 / 16 FJS Buttweld") give only names and tube sizes, and there is no Air-Way series. The data comes from
Brennan TFA p.13, "FJS-WELD STRAIGHT" (`catalog_verified.json` TFA-p013-t04).

The new `DesignTable_6316.xlsx` holds the 3 OMi rows:

| column | catalog column / source |
|---|---|
| L@DRIVE | L |
| L1@DRIVE | L1 |
| C3HEX@HEX (swivel nut) | C HEX |
| C4HEX@HEX (body) | C4 HEX |
| D@BORE | B DRILL |
| THDMAJ_B@DRIVE | SAE J514, standard |
| WELDA@REF | A Weld |

The rows are ScopeAction BUILD, DimSource BRENNAN, **DataStatus MISSING**.

**Column meaning (inference).** The catalog drawing is cut off before the length arrows. Evidence that L runs from the weld face to the nut face
and L1 from the weld face to the 37 deg seat:

- L - L1 = 0.422 / 0.569 / 0.594, which matches the Brennan 6500 nut-face-to-nose-tip NOSETIP_B of 0.43 / 0.57 / 0.60.
- C HEX = the measured swivel nut (SWIV_MEAS AF 0.875 / 1.25 / 1.5).

The female JIC swivel end is ready: `end_JICSW`, and `SWIV_MEAS` has -08, -12 and -16.

**What is missing:**

1. **The butt-weld end shape.** Needed: stub OD, the weld taper / bevel (the catalog photo shows a tapered stub), the stub length to the body
   hex, and the bore at the weld end. No source prints any of these, and there is no Brennan 6316 STEP on disk.
   - Needs: `09_STEP_FILES/BRENNAN_6316-08.stp`, `-12.stp` and `-16.stp`.
   - Then: measure them, add a new end module `end_WELD` to gen_straight2, and add `SPEC['6316']` (End A weld x End B `end_JICSW`).
2. **What catalog column "A Weld" means.** It is 0.500 = tube OD at -08 and 1.000 at -16, but 0.609 at -12, which equals that row's B DRILL
   (also -06 0.297 = drill, -10 0.609). It cannot be used as the weld OD or bore until the STEP or the user settles it.

## 4. 6420-08-08: female ORB x female NPTF straight (BLOCKED, cells staged)

**Data** (staged in `DesignTable_6420.xlsx`; DataStatus stays **MISSING**):

| column | value | source |
|---|---|---|
| L@DRIVE | 1.5 | OMi answer 2026-10-18 ("Lengths to check"!E16); equals Brennan TFA p.17 L 1.500 |
| C4HEX@HEX | 1.000 | OMi Items!R1889; equals catalog C4 HEX |
| D3@BORE | 0.68 | ORB -08 port drill, end library (Air-Way 6404-08-08) |
| TAPDRILL@BORE | 0.70 | -08 NPTF tap drill, Air-Way per size |
| thread majors | standard | - |

DimSource OMI.

**Why it does not build:**

1. **The ports do not fit OMi's length.** At 1.5 the library ports overlap:
   - female ORB -08 port: 0.688 deep (`ORBF_MEAS`, Brennan 6404 / 6410 STEPs);
   - female NPTF -08 tap drill: 0.900 deep (MS51503 P1 max, Brennan 5405-08-08);
   - 0.688 + 0.900 = 1.588 > 1.5, so the 0.70 drill would run 0.088 into the ORB port (minor 0.68).
2. **The Brennan STEP is a different body.** I measured `09_STEP_FILES/BRENNAN_6420-08-08.stp` with `tools/measure/prof.py`:
   - overall 1.620 and hex 1.125, not 1.500 / 1.000;
   - exactly the library ports: ORB face 0.813 dia, 15 deg chamfer, minor 0.689 to 0.688; NPTF tapered 0.75 deep, 0.718 drill to 0.900;
   - the two 120 deg drill points meet.
   This is the same question already asked for 6420-12-12 (`QUESTIONS_FOR_OMi.md` item 7).
3. **No generator path for two female ports.** gen_straight2 has no mode that pairs a female ORB cavity with a female NPTF pocket. The 6404
   pattern has one female port; 5000 has two NPTF pockets.

**Options:**

- (a) **Build OMi's 1.5 x 1.000 (recommended).** Shorten the NPTF drill so it meets the ORB port bottom: 0.812, with the thread 0.75 as on the
  Brennan STEP. The 1.5-long 5000-08-08 coupling, whose drills are cut to meet, is the precedent. Logged as an assumption. Needs a small
  bore mode in gen_straight2 (End A NPTFF pocket to L - P, End B deep ORBF cavity) and `SPEC['6420']`.
- (b) **Build the Brennan STEP body, 1.620 x 1.125.** This is not OMi's length.

## 5. Regeneration of all roots (`regen/cmp.txt`)

All SPEC roots were regenerated, one process per root:

- `live` = byte copy of the live tools;
- `patched` = live tools + these patches;
- both on this folder's tables.

| generator | live | patched | result |
|---|---|---|---|
| gen_straight2 | 58 SPEC roots | 59 (new: 3474) | the other 58 roots identical: macro, SW2 cells, summary |
| gen_tee | 107 SPEC roots | 108 (new: 2613) | the other 107 roots identical |

In total 165 roots are SAME and 2 are DIFF (the new ones). Live has no SPEC for 3474 or 2613 (rc 1). Patched gives 9 and 1 configurations.

**Control** (live tools on the repo tables) reproduces the shipped SW2 tables of every root except 5404N, which is held. The macros differ from
the shipped `03_SCRIPTS` text for 1700, 2408, 4404, 4604, 5404N, 2704 and 5602. These differences already exist and are unrelated: those
shipped macros predate later generator text changes. For example 2408 still has `If Not passed` where the generator now writes
`If passed = False`, and 2704 has the bulkhead Z-extent check text.

## 6. Checks (`checks/SUMMARY.txt`)

| check | result |
|---|---|
| dofcheck_straight, 59 patched macros | all fully defined, 0 redundant. 3474: 20 points, rank 40 = 40, apex on the axis |
| dofcheck_tee, 90 macros (the 108 tee SPEC roots that produce a macro; the other 18 have 0 buildable rows, the same in live) | all fully defined. 2613: 3 legs at 14 / 8 / 22 rank = unknowns, 0 redundant. The only "redundant 1" lines are the 135 deg THDPROF_2 sketches of 1503 / 1504 / 5501 / 5503 / 5505 / 6902 (`same_as_HelixThread: True`); these already exist and are identical in live |
| allcfg_check, every root with a macro (59 straight + 90 tee) | 0 outline problems. 3474: 9 configurations; 2613: 1 |
| vbacheck, 149 macros | all OK |
| regress live -> patched | 0 changed cells in old configurations in every root. 3474 / 2613 have no old configuration |
| patch apply | `patches/*.diff` applied with `patch -p1` to a fresh copy of the live `tools/` give byte-identical files (`checks/patch_apply_test.txt`) |

**OCP closed loop for the new end** (`checks/closed_loop_3474.txt`): **PASS.**

1. All 9 configurations were rebuilt in OCP (`tools/measure/straight_model.py`): 1 solid each. Volumes, in in^3:

   | -04 | -06 | -08 | -10 | -12 | -16 | -20 | -24 | -32 |
   |---|---|---|---|---|---|---|---|---|
   | 0.26869 | 0.38481 | 0.61765 | 1.07224 | 1.83014 | 2.45941 | 3.61604 | 4.64172 | 8.29472 |

   The locknut cut equals the generator integral at every size.
2. `tools/measure/orb_straight.py` was run on each rebuild. That extractor was validated 2026-10-02 on 12 Brennan 6801 STEPs and 8 fixed-ORB
   STEPs. It returns every generator input within 0.0015, including both 15 deg nut chamfers.
3. Pilot comparison, the same extractor on `BRENNAN_3474-12-12-NWO.stp` against the -12 rebuild:
   - every quantity agrees except the adjustable thread length (0.469 Air-Way against 0.4101 Brennan; see section 1);
   - volume: model 1.83014 against Brennan 1.87751 in^3 (-2.52 %). The 2026-10-02 attribution covers it (O-rings, tip chamfers, run-outs,
     hex chamfers), plus the longer thread.

## 7. To ship (main session, on the PC)

1. Apply the patches: `patch -p1 < patches/<x>.diff` from the repo root. If another batch-19 group has changed the generators, re-run
   `scripts/patch_gen_*.py` against the merged base instead. Copy `tools/measure/orb_straight.py` and `straight_model.py`.
2. Copy `04_DESIGN_TABLES/DesignTable_3474.xlsx`, `_2613.xlsx`, `_6316.xlsx` and `_6420.xlsx` into `04_DESIGN_TABLES`. Re-read the live ones
   first in case they changed. 6316 / 6420 build nothing and only carry status.
3. Regenerate 3474 and 2613 with `GS_OUT` / `GT_OUT` pointed at a new folder.
4. Run the SolidWorks dry runs `dryrun/sw_calls_3474.json` and `dryrun/sw_calls_2613.json`. Expected 3474 volumes are the OCP values in
   section 6, with threads suppressed. These are the first SolidWorks builds of the straight NWO end and of the 2613 leg order.
5. Ship as usual: QA_Log, coverage, PROJECT_STATUS. Tell the user about the 3474-12 thread length and the 2613 M1 note.
