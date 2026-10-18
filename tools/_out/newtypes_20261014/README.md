# New model types for O-rings / sleeves / flareless / bent tube (2026-10-14) - STAGED, not shipped

Scope: `00_DOCS/Scope_ORings_BentTube_Flareless_2026-10-14.md`. User 2026-10-14: "start building the new model types on test
rows" and "use airway sizes". Nothing here is in `tools/`, `03_SCRIPTS`, `04_DESIGN_TABLES` or `11_MASTERS` yet.

## Done
| Type | Generator | Rows | SolidWorks dry run |
|---|---|---|---|
| O-ring (4000 + 4001 in ONE master `4000`) | `generators/gen_ring.py` kind ORING | 21 BUILD rows, REAL data: Air-Way s218 (OMi's own part numbers 4000-2 ... / 4001-2 ...), ASSUMED; 5 Air-Way rows not on OMi's website = DROP (4000-05 / -14, 4001-03 / -05 / -14) | `swtest/4000/`: run 1 and run 2 "0 problem(s)", 41 OK / 0 FAIL, 21 configurations 1 body each; sweep_configs 22/22 ok; geometry: torus axis X, 4000-32 I.D. 2.337 / W 0.118, 4000-02 0.239 / 0.064 (= Air-Way), 0 faults. Run 2 = the final macro (axis hidden, save test `ok = False`). |
| Sleeve (closed half-section revolve) | `gen_ring.py` kind SLEEVE | TEST table `test_tables/DesignTable_0319T.xlsx` (0319-08 real Air-Way L / X + OMi bore + Brennan 0319-08 SHAPE; 0319-02 / -32 shape SCALED - TEST only) | `swtest/0319T/`: "0 problem(s)", 32 OK / 0 FAIL, 3 configurations; geometry 0319-08: collar 0.680 / spigot 0.562 / bore 0.505, inner cone 32.99 deg (Brennan 33.0), planes 0 / 0.22 / 0.56 |

- `review_tables/DesignTable_4000.xlsx`, `DesignTable_4001.xlsx` (staged; `scripts/stage_oring_tables.py`) replace the skeleton
  tables in `04_DESIGN_TABLES` at ship time (4005 stays a skeleton: no Air-Way page, OMi asked).
- Air-Way data: `tools/_out/airway_20261014/` (API JSON passes, `parse_series.py`, parsed tables) and, in the usual format,
  `07_RAW_EXTRACTS/airway_passes/4000_p1/_p2.txt` (s218) and `1701_p1/_p2.txt` (s115). Both passes identical.
- `out/ring/` = Build_4000_MASTER.bas + DesignTable_4000_SW2.xlsx (vbacheck OK); `out/sleeve_test/` = the TEST macro (stamped
  "TEST BUILD"). `history/` = the O-ring v1 generator / macro / SW2 - the refactored generator reproduces them byte for byte.
- Gates: only BUILD + VERIFIED / ASSUMED rows; TEST rows only with `GR_TEST=1`; a table with no buildable row writes nothing.
- Lesson: `run_macro` with a missing report folder -> VBA run-time error 76 before the error trap = a modal box that blocks
  SolidWorks (and the MCP retried once). gen_ring macros now check both folders first and exit with a message.

## Done 2026-10-15: bent-tube masters (user: "keep building all of them", "just do the solidworks models" - no drawings now)
New generator `generators/gen_bent.py` (imports the live gen_straight2.py read-only: JIC male chain, code 61 head FLG61_MEAS,
swivel module end_JICSW, VBA helper library). One model type, three masters:

| Master | Covers | TEST rows (dry run) | Result |
|---|---|---|---|
| `1704T` 90 deg MJ x flange | 1704-Tube (code 61) + 1804-Tube (code 62) | 1704-12-12 / -24-24 (Air-Way s115 M3 / N4 / C / D / O) + -08-08 + code 62 1804-08-08; -24-20 and -16-20 BLOCKED by the geometry checks | 0 FAIL / 101 OK (latest run, with the thread check); box = Air-Way M3 / N4 exactly (2.84 / 2.12, 3.67 / 2.75) |
| `1703T` 45 deg MJ x flange | 1703-Tube + 1803-Tube | -08-08 / -12-12 / -24-24 (lengths TEST); code 62 1803-12-12 BLOCKED (no measured -12 code 62 head) | 0 FAIL / 98 OK (latest run) |
| `6701` 90 deg MJ x FJS swivel | 6701 + 6701-L | -08-08 / -12-12 / -16-16 (lengths TEST) | 0 FAIL / 147 OK with the nut thread (run 1 failed: see below) |

2026-10-15 (later), user "do the 6701 nut thread and the code 62 flange heads next":
- **6701 nut thread THD_EndB done**: SolidWorks' Thread feature (Inch Tap) on the nut's minor edge CRASHED SolidWorks (prototype, scratch
  copy), so the nut thread uses the straights' HelixThread method for an axis parallel to Y (`HelixThreadY` in gen_bent): helix sketch on
  NUTPLN (circle HELIXDIA = 2 x basic minor, centre on a construction line HELIXCX = X0 from the projected origin), helix HEIGHT = TE /
  PITCH into the part, right hand (read from the curve), start angle 90 deg = in the Front Plane at x = X0 + r (tried until found);
  60 deg profile THDPROF_B on the Front Plane (PROF_AX = nut face, PROF_R = X0 + r, APEXR = X0 + r + 0.54127 P = the thread major);
  swept cut, suppressed for the save; helix hidden. 7 new table columns. Same thread data as the straights' swivel (end_JICSW).
  Checked: dry run 147 OK / 0 FAIL (`swtest/6701/`), sweep_configs with the threads on 4/4 ok (1 body), geometry 0 faults (-16: minor
  1.2223, countersink mouth 1.3125 = the 1-5/16 major), sections at -08 / -16 looked at.
- **Thread check** (all bent-tube macros): after the all-config sweep every configuration is rebuilt once more with ALL its THD_
  features on (all off -> volume, all on -> no errors, material cut, 1 body) - the sweep skips suppressed features. 1704T / 1703T
  re-run with it (101 / 98 OK, 0 FAIL); previous runs kept as `*_before_threadcheck`, 6701 as `*_before_nutthread` / `*_nutthread_run1`.
- **Code 62 heads**: the -08 head (FLG62_MEAS, wave-1 FLANGE62 measurements of the Brennan 1800-08-08 / 1824-08 / 1804-08-08-FG STEPs)
  builds (1804-08-08-Tube in the 1704T run). Every other code 62 size BLOCKS with its reason: the scope needs code 62 flange -12 (5
  parts), -16 (7), -20 (8), -24 (5), -32 (3) = 28 of the 29 1803 / 1804 -Tube parts; `09_STEP_FILES` has only the three -08 STEPs.
  To unblock: one Brennan STEP with a code 62 head per size (e.g. BRENNAN_1824-12 / -16 / -20 / -24 / -32, the code 62 plugs, or
  1800-NN-NN) - user download - then measure with `tools/_out/newmasters_20261002/work/FLANGE62` (flange62.py) into FLG62_MEAS.
  Code 61 heads are measured at all six sizes the scope needs (-08 / -12 / -16 / -20 / -24 / -32), the swivel at every size.
- Backups: `history/gen_bent_before_nutthread.py`, `history/bent_test_before_nutthread/` (the previous macros / SW2 tables).

Features: DRIVE (JIC end piece = the straights' End A chain + hex body, revolved; HEXCUT) -> PATH (construction line, line, tangent
arc RB, line; fully defined, 17 / 17) -> TUBE (circular-profile sweep TUBEOD; the path must be SELECTED with mark 4 - setting the
definition's Path creates nothing) -> HEADSK / HEAD (code 61 head half-section about the leg-2 axis, face centre on the PATH end,
axis parallel to PATH's last line) or SWSK / SWIVEL + NUTPLN / NUTHEXSK / NUTCUT (6701) -> PATHX / BORE (circular swept cut TUBEID,
0.05 past both ends) -> THD_EndA (suppressed for the save). Geometry checks block a row (reason in the summary) when the bend
starts inside the end piece, reaches the head / swivel body, is tighter than the tube, the tube is wider than the head's O-ring
groove or the swivel neck, the bore leaves no wall or is wider than the JIC tip / the swivel seat mouth.
- 6701 run 1 (`swtest/6701/*run1_fail*`): (a) the swivel was pinned to the tube end that already ran 0.05 into it -> nut 0.05 too
  high; now the swivel axis is collinear with the tube line and the body face sits SWB_TUBEOVL past the tube end; (b) at -12 / -16
  the 37 deg seat apex fell behind the short swivel body -> the seat cone now ends at the bore radius (SWB_SEATENDR = D/2), the
  SEAT_TO_BORE convention of 6565 (Brennan swivel legs: the seat ends at the through-bore).
- Not modelled: the head hub / braze fillets. (The 6701 nut thread and the code 62 -08 head were added later on 2026-10-15 - above;
  code 62 -12 ... -32 heads still need their Brennan STEPs.)
- What the bent tubes still need from a source: tube OD + wall, bend radius, M1 / L1 (Air-Way gives M3 / N4 for four 1704 sizes),
  end-piece hex length - OMi (request drafted) or Air-Way's 3D models of the four 1701-61 sizes.

## Flareless nut 0618 / sleeve 0619
No new model type needed: 0618 = the 0318 JIC tube nut type of gen_straight2 (hex nut, UNF thread, inner shoulder) with its own
inside; 0619 = the SLEEVE type of gen_ring.py with a bite-edge profile. Both wait for OMi's sizes and the shape files V0318-08 /
V0319-08 (user download; not in 09_STEP_FILES on 2026-10-15).

## Regenerate
```
set GR_REV=...\tools\_out\newtypes_20261014\review_tables  &  set GR_OUT=<new folder>
python tools\_out\newtypes_20261014\generators\gen_ring.py 4000
(sleeve test: GR_TEST=1, GR_REV=...\test_tables, gen_ring.py 0319T)
```

## Next
1. **O-ring drawing recipe** (drw3 / geo3 assume fittings): front view = I.D. / O.D. circles, side view = W; title block material
   from `$PRP@Material` (not "Carbon Steel"). Then the O-rings can go to OMi with the other drawings.
2. **4005**: waits for OMi (code 61 / 62 and sizes) - fold into the `4000` master when it comes.
3. **Flareless sleeve 0619**: a new SLEEVE profile (bite edge) in gen_ring once OMi's sizes and the Brennan V0319-08 shape file
   (user download) exist. **0319** (12 JIC sleeves, Air-Way + OMi sizes) could ship on the same type if the user includes it -
   it still needs a per-size rule for collar length / spigot (one Brennan file; MS51533 may give them).
4. **Flareless nut 0618**: a gen_straight2 SPEC next to 0318 (same hex nut, other inside) - needs OMi sizes + the V0318-08 shape.
5. **Bent tube** (68 rows, 3 masters): new generator - tube swept line / bend / line, JIC male end piece (JIC end library),
   code 61 head (`FLG61` module) / code 62 head (wave-1 FLANGE62) / swivel nut (6701). Air-Way s115 (1701-61) gives M3 / N4 / C /
   D / O for 1704-12-12 / -16-20 / -24-20 / -24-24-Tube (drawing: M3 = JIC tip to the far edge of the flange head, N4 = flange
   face to the JIC centre line); bend radius, tube O.D. and wall are NOT printed. Air-Way has 3D models of all four ("Has3DModel")
   - a non-Brennan source for those (user download). Everything else: OMi.

## Ship (when the user says so)
New file `tools/generators/gen_ring.py` (no other generator changes - no regenerate-all needed); staged review tables 4000 / 4001
-> `04_DESIGN_TABLES` (skeletons -> `_to_delete`); macro -> `03_SCRIPTS`, SW2 -> `04_DESIGN_TABLES`; build for real; RUN_ME,
QA_Log, Topologies (4000 TABLED, 4001 folded into the 4000 master), coverage, PROJECT_STATUS; CLAUDE.md "Carbon steel only" gets
the O-ring exception.
