# Group B - generator SPECs for the series without one (2026-10-21, cloud) - STAGED, nothing shipped

Branch `claude/groupB-specs-20261021` (from `claude/ecstatic-hopper-fk5p40` @ a38c414). One of three parallel sessions (group C compression,
group D bent tubes edit other copies of the same generators). Live `04_DESIGN_TABLES`, `03_SCRIPTS`, `tools/`, `11_MASTERS` and every older
stage are untouched. The cloud cannot run SolidWorks: the dry runs are the PC's job (below).

**Result: 109 of the 168 group B parts generate** (+5 configurations of group-A FS roots unlocked by the new `NWO_FS[6]`, +0 changed / lost
anywhere). 59 parts still need a STEP, a new end shape or a user decision (section 4).

## 1. What is here
| Path | What |
|---|---|
| `tools_af/` | copy of `airway_first_20261020/tools_af` + the group B additions (non-FS roots) |
| `tools_fs/` | copy of `orfs_gen_20261020/tools` + the group B additions (FS roots, the ring generator) |
| `stage/04_DESIGN_TABLES`, `stage/orfs_tables` | copy of the Brennan-CAD stage (`brennancad_20261021/stage`); only the group B tables are edited |
| `scripts/apply_all.py` | re-creates every group B table edit from the Brennan-CAD stage (edit_6900, edit_elbows, edit_6801L, edit_fs6809, edit_fs6402, edit_4005, edit_orbport; helper `tabedit.py`) -> `CHANGES.csv` (871 cell writes, 281 of them Brennan CAD-record cells, each with its source) |
| `scripts/regen_all.py` | every SPEC root of both toolsets regenerated with the OLD and the NEW toolset and diffed -> `regen/cmp.txt` |
| `scripts/run_checks.py` | vbacheck / dofcheck / allcfg / regress on every added or changed master -> `checks/*.txt`; copies them to `out/` |
| `scripts/closed_loop_*.py` | OCP closed loops (`ocp/*/closed_loop*.txt`) |
| `scripts/summary.py` | per series: configurations / not generated with the reason -> `checks/series_summary.txt` |
| `out/af`, `out/fs` | the 18 macros + SW2 tables for the dry runs |
| `dryrun/calls_g1..g3.json` | the dry-run call files (`scripts/make_calls.py`) |

Generator edits are ADDITIVE (new SPEC entries, new functions, guarded branches); every existing root regenerates byte-identical
(`regen/cmp.txt`: 0 lost, 0 changed configurations; the only macros that differ are the four whose masters gain configurations - 6801,
FS6801, FS6801R, 4000 - and there only the configuration-count / spot-check lines).

## 2. Per series (configurations generated / not generated) - `checks/series_summary.txt`
| Series | Built | How | Not generated |
|---|---|---|---|
| **6900** male ORB x female NPSM swivel straight | **22 / 22** | new SPEC (gen_straight2) from the existing ORBM + NPSMSW ends. A3 (2026-10-18): table identity corrected ("female JIC union" was wrong), the bogus BLOCKED note removed, Air-Way rows MISSING -> ASSUMED. Brennan 6900-08-08-O STEP: W4 = ORB tip -> nut face (1.550 = record L), L2 = ORB tip -> stem tip (1.270 = L1), the 1404-08 swivel end. 6900-32-32-O: W4 / L2 / D from the record (BRENNAN). | - |
| **6901** 90deg adj. ORB x female NPSM swivel | **19 / 21** | SPEC = the 6902 one at 90deg; -FG rows filled from the records (M7 / M / M6 / Y / C1 / BD / AD placed on BRENNAN_6901-06-08-NWO-FG: nut face 1.320, stem tip 1.040, body face 0.560 = the 1404-08 end; A14 settled for these rows: the record bore = the CAD value) | 6901-10-08 (Air-Way -FG row: hex 1.11 vs leg -> the corner puck reaches outside the neck - decision 3); 6901-08-12 (record W-L 0.31 does not fit the 1404-12 swivel - decision 4) |
| **6805** 90deg adj. ORB x female NPTF | **12 / 12** | new SPEC (NWO + NPTFF legs; Brennan 6805-08-08-NWO-FG STEP: collar 0.26, 0.718 tap drill to the crossing); legs / hex from the records (M7, N, Y) | (6805-08-06: Air-Way N1 0.63 cannot be built -> Brennan 1.02, Q1 - decision 2) |
| **6806** 90deg adj. ORB x male NPTF | **10 / 10** | new SPEC (NWO + NPTFM); every -FG row from its record | 6806-12-08 has no record (not in the 168) |
| **6809** 90deg adj. ORB x female JIC swivel | **7 / 7** | SPEC = the 6810 one at 90deg; record codes on BRENNAN_6809-10-10-NWO-FG (nut face 1.620 = M6, nose tip 1.120 = M; C1 = locknut, C2 = swivel nut) | - |
| **6815** adj. ORB x female ORB elbow | **6 / 6** | NEW leg module `leg_ORBPORT` (section 3) | - |
| **6832** female ORB run x adj. ORB branch tee | **4 / 4** | `leg_ORBPORT` | - |
| **6835** adj. ORB x female ORB x female ORB tee | **4 / 4** | `leg_ORBPORT` (+Y port: DrawPortLoop with a vertical axis) | - |
| **6801-L / 6801-LL** | **6 / 6, 5 / 6** | folded into the 6801 master (user 2026-10-21; SPEC['6801']['fold']). Measured: BRENNAN_6801 / -L / -LL-08-08: ORB tip 1.45 / 1.97 / 2.48, ORB body face 0.59 / 1.11 / 1.62 -> tip-to-body-face 0.86 on all three, JIC leg 1.25 on all three: only the ORB leg's forged hex arm is longer. ORB_I3 / ORB_THDL / ORB_GRVDIA = the 6801 table's own Air-Way rows of the size (A5). | 6801-LL-08-08 held: Air-Way prints exactly its -08-10 row (open question D) - decision 5 |
| **4005** flange O-rings | **8 / 9** | records (I.D., W, Buna-N) checked on BRENNAN_4005-08 (I.D. 0.734 / O.D. 1.014 / W 0.140); folded into the 4000 ring master (gen_ring SPEC 4000 tables + '4005'). The code 61 and code 62 face grooves are the same at every measured size, so Q-NEW-4005CODE does not change the ring. | 4005-48 (no record) |
| **FS2408** face-seal plug | **2 / 8** | new SPEC; built the way Brennan builds it (BRENNAN_FS2408-08: blind hole 0.378, full dia to 0.391, 120deg point to 0.500 of the 0.504 end length) -> rule "full dia to end length - 0.004 - drill-point height" (= the STEP at -08, ASSUMED at -24) | -04 / -06 / -10 / -12 / -16 / -20: the STRAIGHT male face-seal end (FSM_MEAS) exists only at -08 / -24 / -32 -> BRENNAN_FS2403-NN-NN |
| **FS6402** male FS x female JIC swivel | **1 / 7** | new SPEC (FSM + JICSW); nose = the record CC (0.422 measured on BRENNAN_FS6402-08-08) in a new column SNT | the other sizes: same FSM gap |
| **FS6809** FS swivel x FS adj. stud elbow | **2 / 7** | new SPEC (FSSW + FS stud); NEW `NWO_FS[6]` measured on BRENNAN_FS6809-06-06-NWO-FG (neck 0.300 x 0.058, nut 0.33 / AF 0.75, washer 0.397 x 0.035, undercut 0.103; tip -> washer 0.457 = record DT) | -04 / -10 / -12 / -16 / -20: no NWO_FS (needs BRENNAN_FS6801-NN-NN-NWO-FG or another FS part with that stud) |
| **FS6801-L** | **1 / 1** | folded into FS6801 (all fs_code variants); BRENNAN_FS6801-L-08-08 vs FS6801-08-08: only the stud's hex arm is longer (tip -> washer 0.540 on both) | - |
| FS1700 / FS1704 / FS1800 / FS1804 | 0 / 16 | - | straights: the FSM straight end exists only at -24 (FS1700-24 / FS1800-24 also need their collar / neck body: own STEP); forged FS1704 / FS1804: the FS leg on BRENNAN_FS1704-12-12-FG ends in a 45deg chamfer to a round NECK (dia 1.068 = record W1) before the hex - a run-out the forged FS leg module does not have yet (new variant + closed loop). Code 62 heads are ready: BRENNAN_FS1800-12-12 measured (O 1.625, TH 0.345, GI 0.47, GO 0.625, GD 0.11 = catalog 3300-62 A / D / H on the -12 row), the -16 / -20 / -24 heads = catalog 3300-62 A / D / H + the code-61 groove ID / depth (Q-CODE62-CAT) - NOT written into FLG62_MEAS here (no consumer in group B; group D may need the same lines) |
| FS2700 bulkhead union | 0 / 7 | - | needs a STRAIGHT face-seal bulkhead end (BRENNAN_FS2700-08-08 measured: hex 0..0.356, step r 0.4005 x 0.06, relief 0.094, thread to the face 1.796; = FS2701's FSBH leg without the collar) - new end + emit block; only -08 (+LN) would build (FSM gap) |
| FS6400-L | 0 / 3 | - | not a plain fold: BRENNAN_FS6400-L-08-08-O has a ROUND SHANK dia 0.829 from the face-seal thread to the hex (no flank / relief) -> its own end; only -08 would build (FSM gap) |
| FS7202 | 0 / 1 | - | BSPP stud (new end type) |
| 6425 FORB-FORB straight | 0 / 5 | - | needs a female ORB port at End A of the straight generator (emit block); BRENNAN_6425-06-06: hex bar, both ports = ORBF_MEAS, the port drill runs through. 6425-08-08: catalog C4 1.000 vs CAD record 1.062 (held) |
| 3051 low-profile street elbow | 0 / 4 | - | square BLOCK body (BRENNAN_3051-08-08: 1.125 cube, male pipe leg on -X, female port in a face) - a new body type |
| 6316 FJS x weld | 0 / 3 | - | weld stub end (new end type) |

## 3. Generator additions (all additive)
- `tools_af/generators/gen_straight2.py`: `SPEC['6900']`.
- `tools_af/generators/gen_tee.py`: `SPEC['6901'/'6805'/'6806'/'6809'/'6815'/'6832'/'6835']`, `SPEC['6801']['fold']`, `assume_reps_opt` (optional
  wording pairs; a blocked row's leg can fall back), **`leg_ORBPORT`** + SPEC key `orbport` (legs listed there are female ORB ports, kind NPTFF
  so the proven collar / pocket / bore / helix machinery applies; port drill, P, chamfer = the straight ORBF end library), the **ORBMOUTHi**
  mouth cut (closed loop: drill -> 45deg lead-in -> O-ring chamfer -> 0.02 past the face, revolved about the leg axis; new VBA `DrawPortLoop`
  (= DrawLoopAx with the axis direction as a parameter, so a +Y port works) and `PortMouthCut` (volume check against the generator's ring
  volume, 2 %), emitted only in macros that have a port).
- `tools_af/checks`: `dofcheck_tee.py` checks the ORBMOUTH sketches (16 unknowns, 16 constraints, rank 16, 0 redundant; the drawn loop carries
  every value), `allcfg_check.py` checks every configuration's mouth loop (no self-intersection, off the axis, inside the drill, above the pocket bottom).
- `tools_fs/generators/gen_straight2.py`: `SPEC['FS2408']` (+ `hole_dep` hook in the B_blind bore), `SPEC['FS6402']`.
- `tools_fs/generators/gen_tee.py`: `NWO_FS[6]`, `SPEC['FS6809']` (+ fs_code variants), FS6801-L fold on every FS6801 variant, FS6801R keeps its
  dry-run reference configuration.
- `tools_fs/generators/gen_ring.py`: 4005 table folded into SPEC 4000, its description text.

## 4. Assumptions (each in the rows' `$PRP@AxialSource`)
- Brennan CAD record values fill only EMPTY cells (Air-Way first); codes placed on the family STEP (each script's docstring lists the readings).
  Rows complete from one source -> ASSUMED; `$PRP@DimSource` BRENNAN where a record / catalog value is used.
- Adjustable-ORB end cells not printed: I3 = Air-Way 6801 ORB_I3 (= Brennan), thread length / undercut = the ORB end library ('=6801', '=ORB:*').
- Thread-major cells left empty: the thread the part number names (end library), as every built row.
- 6801-L / -LL: extra length = the ORB leg's hex arm (measured at -08-08 only). FS6801-L the same (stud leg).
- ORB port legs: ORBF_MEAS port geometry (6404 / 6410 STEPs) = the 6815 / 6832 / 6835 -08 STEP ports; port drill = Air-Way per size (A11);
  6815 port ends flat at P (Brennan: drill point) + the stud drill to the crossing; tee ports drill to the crossing (as the STEPs); the 0.003
  radial step at the chamfer foot not modelled; the collar is shortened to clear the corner puck by 0.03 where the generator rule says so.
- FS2408 hole depth rule measured at -08 only; FS6402 nose from the record; NWO_FS[6] from one STEP (FS6809-06-06).
- 4005: ring = torus I.D. x W from the record.

## 5. Checks (all clean)
- `regen/cmp.txt`: every root of both toolsets, old vs new: **NEW only** (114 configurations), **0 lost, 0 changed**.
- `checks/vbacheck.txt` 18 / 18 OK; `checks/dofcheck_tee.txt` 36 / 36 sketches fully defined, 0 redundant (incl. 8 ORBMOUTH sketches);
  `checks/dofcheck_straight.txt` 3 / 3; `checks/allcfg.txt` 0 outline problems (22 mouth loops); `checks/regress.txt` 0 changed cells in old
  configurations (6801 39 -> 50, FS6801 3 -> 4, FS6801R 1 -> 2, 4000 29 -> 37).
- OCP closed loops (rebuild from the generator chain, measure with the extractors that read the Brennan STEPs):
  - `ocp/orbport/closed_loop_orbport.txt`: 14 configurations, 163 checks, 0 off; the model ports read the same as the Brennan 6815 / 6832 /
    6835-08 STEP ports (face, RF, RC, 15deg, minor within the 0.68 / 0.682 rounding); volumes vs Brennan +0.65 % / -0.01 % / +1.44 %.
  - `ocp/tee/closed_loop_tee.txt` (FS6801 / FS6801R / FS6802R / FS6804R / FS6809 / FS6809R): 12 configurations, 294 checks, 0 off; FS6809-06-06
    -2.08 %, FS6801-L-08-08 -1.6 %, FS6802-08-06 -4.11 % vs their Brennan STEPs (the Brennan FS6802 stud sits on the 45deg axis).
  - `ocp/straight/closed_loop.txt` (FS2408 + FS2403 / FS6400 regression): 9 configurations, 207 checks, 0 off; FS2408-08 +2.0 %.
    `ocp/straight6402/closed_loop.txt`: FS6402-08-08 16 checks, 0 off, +1.48 %.
- The non-FS elbows (6901 / 6805 / 6806 / 6809) and 6900 use only accepted leg modules (no new end shape).

## 6. RUN_DRYRUN (PC)
1. SolidWorks 2026 signed in (3DEXPERIENCE), no master of these roots open, no VBA editor open.
2. In `OMi_Handoff`: `python sw_mcp\call.py @tools\_out\groupB_20261021\dryrun\calls_g1.json > tools\_out\groupB_20261021\dryrun\out_g1.txt`
   then `calls_g2.json`, `calls_g3.json` (restart SolidWorks between groups if memory > 8 GB).
   - g1: 6900 6901 6805 6806 6809 6801 (6801 also sweeps the shipped 11_MASTERS part: its 39 old configurations must keep volume / size)
   - g2: 6815 6832 6835 (NEW: ORBMOUTH sketch + cut - look at the `ORBMOUTHi` trace lines and a section screenshot of one port) FS2408 FS6402 FS6809 FS6809R
   - g3: FS6801 FS6801R FS6802R FS6804R 4000
   Each `run_macro` uses `TABLE_PATH` = `tools\_out\groupB_20261021\out\<af|fs>\DesignTable_<root>_SW2.xlsx`, `SAVE_PATH` / `REPORT_PATH` =
   `tools\_out\groupB_20261021\dryrun\<root>\` (11_MASTERS / 03_SCRIPTS untouched).
3. PASS = 0 FAIL lines, every configuration 1 body, configuration set = the SW2; for 6815 / 6832 / 6835 also "ORBMOUTHi_SK sketch fully
   defined" and "ORBMOUTHi removed ... = the port mouth ring" in every report.

## 7. For the user (decisions; nothing asked that the rules settle)
1. **6900-05-04-O**: Air-Way W4 1.30 / L2 1.19 cannot be built (nut face 0.11 from the stem tip) -> applied Q1 ("use brennans"): both cells =
   the record L 1.280 / L1 1.090 (BRENNAN-CELL). The 2026-10-18 list had recommended "keep W4" (group D, unanswered) - OK?
2. **6805-08-06-NWO-FG**: Air-Way N1 0.63 (Air-Way's own note "likely typo") cannot be built -> Brennan 1.02 (Q1, = Air-Way's non-FG row). OK?
3. **6901-10-08-NWO-FG** (Air-Way -FG row): hex 1.11 with stem tip 0.98 puts the forged corner outside the swivel neck. Brennan's record: hex
   0.875, stem tip 1.11, nut face 1.39. Which cells to take from Brennan (Q1 does not say which of the two)? Held.
4. **6901-08-12-NWO-FG**: its record (stem tip 1.27 / nut face 1.58) does not fit the measured -12 NPSM swivel (1404-12). Download
   BRENNAN_6901-08-12-NWO-FG to measure its swivel, or leave it out. Held.
5. **6801-LL-08-08-NWO-FG**: Air-Way prints the -08-10 row's values (open question D "ignore it?"). Ignore Air-Way and take the Brennan record
   (M 1.25 / M7 2.48 = the STEP)? Held.
6. 6801-L / -LL: Air-Way's long leg differs a lot from Brennan on some sizes (e.g. 6801-L-04-04 1.19 vs 1.54) - built to Air-Way, noted in
   `$COMMENT` (tell OMi).
7. 6425-08-08: Brennan catalog hex 1.000 vs CAD record 1.062 (not built yet anyway).
8. 6900: Brennan's records differ from Air-Way on 19 of the 21 Air-Way rows (W4 / L2 by 0.02 - 0.18, some bores); built to Air-Way,
   each row's `$COMMENT` lists the differences (tell OMi).
9. Downloads that unlock the rest: BRENNAN_FS2403-04-04 / -06 / -10 / -12 / -16 / -20 (straight FSM ends: FS2408, FS6402, FS2700, FS1700 /
   FS1800 and group-A FS straights), BRENNAN_FS6801-NN-NN-NWO-FG -04 / -10 / -12 / -16 / -20 (FS studs: FS6809 and FS6801 / FS6802 / FS6804).

## 8. Merge notes (for whoever merges groups B / C / D)
- Every generator edit is a new SPEC / function / guarded branch; regenerate all roots after the merge and diff against `regen/cmp.txt`.
- `ORBPORT_HELP` is appended to the macro header only when a leg has a port mouth; `assume_reps_opt` is a new optional SPEC key.
- The code 62 head values (section 2, FS18xx) are NOT in FLG62_MEAS here; if group D adds them, the -12 row must equal the FS1800-12-12 STEP.
- `regen_all.py` FS env: `GR_REV` = the newtypes review tables (4000 / 4001 as the ORFS README runs the ring generator).
