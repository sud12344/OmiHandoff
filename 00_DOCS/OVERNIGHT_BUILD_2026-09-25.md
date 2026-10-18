# Overnight build, 2026-09-25 (Claude, SolidWorks MCP, 02:30 - 05:00)

You asked me (before bed) to build every macro that had not been made yet and park the good parts next to the
masters. **`11_MASTERS` and `03_SCRIPTS` were not touched. Nothing is released.** (PROJECT_STATUS.md, CLAUDE.md and
tools/README.md were updated from this write-up in the follow-up the same day; their previous versions are in
`_to_delete\superseded_20260925\`.)

## Result in one screen

- **38 parts built and reviewed -> `11_MASTERS_NEW\`** (part + `reports\` + `screenshots\`): 29 delivered macros (all
  31 except 2702 / 2703; the old 2501 is superseded by 13b), the five 13b candidates (2501 6801 6802 6803 6804), and the re-runs 0403 6405 6408 0318. Every
  configuration of every one rebuilds with 1 solid body (checked twice: the macro's own threads-live sweep and an
  independent `sweep_configs`), and I looked at every screenshot.
- **2 held back: 2702, 2703** (hex arm fails at -16; cause proven, 0.001" fix needs your OK) - builds in `tools\_out\overnight\`.
- **2 delivered macros did not compile at all: 6504 and 6565** (more than 24 VBA line continuations). **6565 also had
  no threads** (its helix start was predicted 90 deg wrong). Both fixed in the generators, rebuilt, in `11_MASTERS_NEW`.
- **One real geometry error found in a delivered macro: 6404** - the -04/-06 port O-ring chamfer came out 15 deg where
  the table says 12 deg (a leftover angle dimension froze the table column - bug [A] below). Fixed in the generators;
  the 6404 in `11_MASTERS_NEW` is the corrected build (from the regenerated macro). Checked every other build and the 26
  existing masters: nothing else is affected.
- The never-run code paths are proven: swivel-nut hex cut (`NutHexCutAx`, 7 macros), `ZoneHexCut` (8 straights),
  the 45 deg leg helpers and the 13b adjustable-ORB module all work in SolidWorks at every size.
- **SolidWorks needs a restart before more work**: it holds 11 GB after ~60 builds and at 04:45 warned "critically low
  on committed memory". I answered **No** (cancel) - no document was open - and stopped. I did not close SolidWorks:
  a VBA editor window "test" is open and might be yours.

To accept a part: follow `PROJECT_STATUS.md` section 1 (existing master + report -> `_to_delete` first for 0318 0403
6405 6408, then part -> `11_MASTERS`, report -> `03_SCRIPTS`; 6404 / 6504 / 6565 also need their regen macro shipped).
0318: the new build opens in its reference configuration, which settles that housekeeping item (the duplicate
`11_MASTERS\0318_MASTER_011925.SLDPRT` can go to `_to_delete` - I did not move it).

## Per-macro results

| Root | Source | Configs | Build | FAIL lines (explained below) | In 11_MASTERS_NEW |
|---|---|---|---|---|---|
| 0318 | 03_SCRIPTS | 12 | 34 s | - | yes |
| 0403 | 03_SCRIPTS | 7 | 27 s | - | yes |
| 1404 | 03_SCRIPTS | 24 | 217 s | - | yes |
| 1405 | 03_SCRIPTS | 15 | 53 s | - | yes |
| 1501 | 03_SCRIPTS | 16 | 43 s | - | yes |
| 1700 | 03_SCRIPTS | 10 | 32 s | - | yes |
| 2406 | 03_SCRIPTS | 40 | 79 s | [A] angle JICFB_CSANG | yes |
| 2408 | 03_SCRIPTS | 15 | 36 s | - | yes |
| 2501 | 13b candidate | 32 | 64 s | - | yes |
| 2503 | 03_SCRIPTS | 27 | 60 s | - | yes |
| 2700 | 03_SCRIPTS | 24 | 78 s | - | yes |
| 2701 | 03_SCRIPTS | 13 | 51 s | [D] Z extent (bulkhead collar) | yes |
| 2702 | 03_SCRIPTS | 10 | 51 s | [D]; **HEX2_BODY fails in 2702-16-16-FG and -LN** | **held back** |
| 2703 | 03_SCRIPTS | 11 | 59 s | [D]; **HEX3_BODY fails in 2703-16-16-16-FG and -LN** | **held back** |
| 2704 | 03_SCRIPTS | 12 | 61 s | [D] Z extent (bulkhead collar) | yes |
| 2705 | 03_SCRIPTS | 14 | 60 s | - | yes |
| 2706 | 03_SCRIPTS | 22 | 189 s | - | yes |
| 4404 | 03_SCRIPTS | 13 | 112 s | - | yes |
| 4604 | 03_SCRIPTS | 14 | 33 s | - | yes |
| 5404N | 03_SCRIPTS | 4 | 61 s | [E] body diameter from the loose threads-live box | yes |
| 5500 | 03_SCRIPTS | 13 | 38 s | - | yes |
| 6402 | 03_SCRIPTS | 15 | 47 s | [A] [C] | yes |
| 6404 | **regenerated macro** | 14 | 127 s | - (the 03_SCRIPTS build had [A] + wrong -04/-06 chamfer + a 06-08 thread failure) | yes |
| 6405 | 03_SCRIPTS | 39 | 97 s | - | yes |
| 6408 | 03_SCRIPTS | 14 | 35 s | - | yes |
| 6410 | 03_SCRIPTS | 27 | 62 s | [A] angle ORBFB_LEADANG | yes |
| 6500 | 03_SCRIPTS | 14 | 47 s | [A] [C] [D] X extent (swivel nut corners) | yes |
| 6501 | 03_SCRIPTS | 1 | 25 s | [A] | yes |
| 6502 | 03_SCRIPTS | 8 | 41 s | [A] [C] | yes |
| 6503 | 03_SCRIPTS | 1 | 27 s | [A] [C] | yes |
| 6504 | **fixed macro** | 8 | 37 s | [A] | yes |
| 6505 | 03_SCRIPTS | 16 | 148 s | [A] [C] | yes |
| 6506 | 03_SCRIPTS | 10 | 44 s | [A] | yes |
| 6565 | **fixed macro** | 5 | 34 s | [A] x2 | yes |
| 6600 | 03_SCRIPTS | 9 | 49 s | [A] [C] | yes |
| 6602 | 03_SCRIPTS | 9 | 49 s | [A] [C] | yes |
| 6801 | 13b candidate | 33 | 78 s | - | yes |
| 6802 | 13b candidate | 16 | 56 s | - | yes |
| 6803 | 13b candidate | 5 | 42 s | - | yes |
| 6804 | 13b candidate | 8 | 49 s | - | yes |

13b candidates were built from `tools\_out\tee` with their own SW2 tables (TABLE_PATH redirected), i.e. from the
pre-fix 13b macros. 13b will now ship from `tools\_out\regen_20260925\tee` (same SW2 tables, only helper code differs;
dry-run 6801-6804 from it first - PROJECT_STATUS section 2). 6802 still has the 3 configurations the over-strict e45
check blocks.
Parts from "03_SCRIPTS" are exactly what the shipped macros produce; the ones marked [A]/[C] are geometrically correct
(proven below) - only their sketches carry the leftover dimensions described in [A].

### What the FAIL lines mean
- **[A] "angle ..._CSANG / _LEADANG was not created"** - `DeleteDisp` never deleted a rejected angle dimension
  (`Annotation.Select3(False, Nothing)` selects nothing in an open sketch). The first, wrong-quadrant try stays DRIVING;
  the named dimension created after it becomes DRIVEN, so **its design-table column is dead**. Where that column is
  constant this is harmless: every retried angle that has a design-table column, in tonight's builds and in the 26
  existing masters, is a constant 60 deg RELIEFANG, except **6404 ORBFB_CHAMANG (12 deg for -04/-06, 15 deg above) -> 5 configurations of 6404 were
  wrong** (found by comparing volumes of every configuration with the fixed build: 9 of 11 parts identical, 2406 differs
  by 1e-6, 6404 differs exactly in those 5 configurations; SolidWorks confirms the 15 vs 12 deg cones).
  For CSANG / LEADANG no placement can give the wanted angle at all: the two segments do not meet, and SolidWorks then
  dimensions the directed angle whatever the text position (probed: 24 positions, all 130 deg).
  **Fixed** in the generators (below): working delete + bisector placement + the supplement kept as `<name>_SUPPL`.
- **[C] "HELIXDIA = 0.6800 (expect 0.6823)"** - the helix circle snapped to the nose OD at build time. The table sets
  the right value in every product configuration (checked all configs of 6402 6502 6503 6505 6600 6602 6500); only the
  unused "Default" configuration keeps 0.680. **Fixed** in the generator.
- **[D] extent checks** - the self-check forgot the swivel nut hex corners on +/-X (6500: -0.722 vs -0.613) and the
  bulkhead collar (2701-2704: 0.44 vs hex flats 0.375). Check bug only. **Fixed**.
- **[E] 5404N body diameter** - measured on the loose threads-live bounding box; exactly 0.8800 with threads suppressed.
- The "N problem(s)" pop-up counted 0-2 more than the FAIL lines (`If Not passed` with SolidWorks' True = 1: `Not 1`
  = -2; it depends on which checks get a raw COM boolean - not only HelixThread's). **Fixed**: `If passed = False Then`.

## The 2 held-back parts - cause (proven in SolidWorks) and proposed fix (your call)
**2702-16-16 and 2703-16-16-16 (and -LN): the bulkhead-leg hex arm does not rebuild.** By design the hex arm ends
exactly at the bulkhead collar face (true for every bulkhead configuration). At -16 in these two the collar radius
(0.72) lies between the hex flats (0.656) and corners (0.758); SolidWorks' boss merge then fails on the shared plane.
Proof: HEXL 0.870 fails, 0.869 and 0.871 rebuild (2703: 1.110 fails, 1.109 / 1.111 rebuild). Proposal: end the hex
arm 0.001 short of the collar (log it as a modelling assumption, like NWO_RN_MARGIN), or 0.001 into the collar.
(6404's 06-08 thread failure seen in the first build is gone with the HelixThread fix - the regenerated build rebuilds
all 14 configurations with threads live. The row is still odd: 6404-06-08 is 1.10 long, shorter than 6404-06-06 at
1.38, and its bore equals the port minor - worth a look at the Air-Way row.)

## Generator changes I made (each backed up first in `_to_delete\superseded_20260925\`)
All verified by regenerating all 57 roots with the old and new generators and diffing (SW2 tables unchanged):
1. **Line continuations** (`gen_straight2.py`; guard also in `gen_tee.py`): above 24 profile points, two points per
   line. Changes only 6504 and 6565 (identical numbers). `checks/vbacheck.py` now fails any statement with more than 24
   continuations - it flags the shipped 6504/6565 and passes the fixed ones.
2. **HelixThread** (`templates\gen_macro_straight_v1.py.txt`): `AddToDB` around the helix circle + explicit
   `SystemValue` (HELIXDIA right at build time); the helix start point is read from the helix curve instead of predicted
   from the face sketch's X axis (6565: 90 deg off, no threads; 6404-06-08 thread now builds too).
3. **False FAIL lines** (check text only): `Check` counter; gen_tee extent checks include the bulkhead collar and the
   swivel-nut hex corners. Every former extent FAIL passes against tonight's measured extents; nothing new fails.
4. **Angle dimensions** (`sp3fix.py` Dim_ang + `DeleteDisp` in the three templates): working delete (`Select2` +
   `EditDelete`, tested), first candidates on the bisector of the wanted sector, and when no placement can give the
   angle, the supplement is kept and named `<name>_SUPPL` (driving, same line, no table column can drive it wrongly).

**Proof in SolidWorks** (dry runs into scratch of the regenerated 6500 2406 6404 6410 6402 6565 6502 6600 + 1404 2501
2701): **all 11 build with 0 FAIL lines**; every angle in every leg sketch is named and DRIVING (RELIEFANG1 60,
SEATB 37, RELANG 45, SW*_CSANG_SUPPL 130, ORBFB_LEADANG_SUPPL 135 ...), no leftover D-dimensions; volumes and sizes of
every configuration identical to tonight's builds except 6404's 5 corrected configurations.

**Full regenerated set with all of the above: `tools\_out\regen_20260925\` (57 macros + SW2 tables, vbacheck all OK).**
Ship from there when you re-ship (6404, 6504, 6565 must be replaced). `11_MASTERS_NEW\fixed_macros\` holds the macros
that built those three parts: 6404 = the final regenerated one; 6504 / 6565 = an intermediate version (fixes 1 and 2
only) - ship the regen versions instead (the regen 6565 was dry-run clean with identical volumes; the regen 6504 has not
been built yet). `tools\_out\tee` still holds the 13b candidates exactly as I built them. Caveat: for 0318 2408
2503 2601 2605 2650 2700 2705 2706 4404 4604 5000 5404 5404N 5406 5406C 5406P 5500 5600 (and 2501) the regenerated macro
also carries older, never-shipped generator changes, so dry-run any root that was not among the 11 above before
re-shipping it (details: PROJECT_STATUS section 1).

QA_Log check (openpyxl now works): last row is #152, so the next is #153 (as PROJECT_STATUS says).

## Verification beyond the build reports
- **6500 swivel vs Brennan** (`screenshots\6500_swivel_vs_brennan.png`): SolidWorks STEP exports, one per swivel size
  -04 ... -32, sectioned through the swivel axis and overlaid on the Brennan 6500 STEPs: through the flats within
  0.003 over nut hex, skirt and neck at every size. Differences = documented unmodelled details (hex corner chamfers,
  nut/body lip, nose tip ~0.01 per Air-Way).
- **6801 built in SolidWorks vs Brennan** (same extractor as `measure/nwo_closedloop.py`, 9 sizes): I3, thread length,
  undercut, washer OD/thickness, locknut size/thickness, neck, 15 deg chamfers all equal Brennan, except the documented
  6801-04-02 leg (1.03 Air-Way vs 0.92) and 6801-12-12 thread length (0.469 vs 0.410), and the cosmetic NWO_CH_DR
  (+0.0025 on the nut chamfer start).
- Toolchain (step 0): requirements installed (openpyxl 3.1.5, cadquery-ocp 8.0.1; numpy 2.4.4 was already there - I
  said earlier it was missing, it was not). 13b regenerates identically (only LF vs CRLF line endings differ). OCP 8
  reproduces SWIV_MEAS on all 10 Brennan 6500 STEPs and the 6801-08-08 closed loop.

## Decisions for you
1. **Hex A/F: Air-Way 2-decimal vs the real fraction.** The model follows Air-Way, Brennan has the wrench size:
   swivel nuts -04 0.56 (9/16), -05 0.63 (5/8), -06 0.69 (11/16), -08 0.88 (7/8), -32 2.88 (2-7/8); 6801 body hex
   -10 0.88, -20 1.63, -24 1.88. A 0.63 hex does not take a 5/8 wrench. Snap to the fraction (like the 2603HX rule)?
2. 2702/2703 -16: accept the 0.001 hex-arm offset?
3. Re-ship the regenerated macros (at least 6404/6504/6565)? Ship 13b? All five 13b parts build clean in SolidWorks
   (6801 also matches Brennan); the rest of the 13b ship list is unchanged.
4. Still open from before: 6801-05-05, 1501-24-24-FG nut, 6400-L master, Brennan STEP downloads, the OMi report items.

## Smaller things noticed
- 45 deg elbows (2503, 6502, 6802) show the leg plane `PLN2` and an axis sketch line in the saved part (hide them).
- Helix curves of suppressed threads are visible (blue) in the saved parts - cosmetic.
- The "Default" configuration exists in every master (SolidWorks' own) and is not in the tables.
- CLAUDE.md's gotcha "NutHexCutAx has not run - verify 6500 first" was out of date - removed in the follow-up.
