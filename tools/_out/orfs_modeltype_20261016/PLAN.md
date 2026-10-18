# ORFS (O-ring face seal, OMi FS...) model type - plan (2026-10-16)

PLAN ONLY - nothing was built, generated or changed. Input: the 51 staged review tables
`tools/_out/orfs_airway_20261015/review_tables/DesignTable_FS*.xlsx` (288 FS parts with dimensions: 229 VERIFIED, 59 ASSUMED; the
211 MISSING stay out). Read-only on everything else: no SolidWorks; `tools/`, `04_DESIGN_TABLES`, `11_MASTERS`, PROJECT_STATUS and
CLAUDE.md untouched. The STEP list is `STEPS_NEEDED.txt` in this folder. Scope stays PROVISIONAL until OMi's website list is read
(`tools/_out/omi_enum_20261015/`).

## Questions for you (answer before the generator work starts)

**Q-FS-MASTER - one master per FS series (required).** CLAUDE.md and the skill say "one master per shape: 2404 / FS2404 / C2404 / 2404-L
share one". That cannot hold for ORFS. A face-seal end (flat face with an O-ring groove, straight UN thread) is a different DRIVE sketch
from a 37 deg JIC end: different segments, different dimension names, a different thread length. One master would need both end
sketches, switched by configuration. Proposal:
- each FS series gets its own master (`FS2403_MASTER.SLDPRT`, macro `Build_FS2403_MASTER.bas`, entry `BuildFS2403`). That is 31 new
  masters for the 288 parts (table in section 1).
- the long and lock-nut variants fold in as rows of their base master:
  - FS2700-LN -> FS2700, FS2701-LN -> FS2701, FS2702-LN -> FS2702, FS2703-LN -> FS2703, FS2704-LN -> FS2704
  - FS6400-L -> FS6400 (Style A rows), FS6801-L -> FS6801
- FS4000 (face-seal O-rings) folds into the staged `4000` O-ring master: same torus, other sizes.
- At ship time the rule in CLAUDE.md and the skill becomes "one master per shape **and end family**", and the skill line
  "2404 / FS2404 / C2404 share one" is corrected.

-> Recommended: yes.

**Q-FS-ORBSTUD - the straight-thread studs on FS parts are longer than our ORB ends.**
- Air-Way prints where the body starts behind the stud (read off Air-Way's spec drawings, section 9):
  - FF6400 L9 / FF6400-L L31 / FF6402 L35: face-seal face -> the hex's ORB-side face
  - FF6801 L11, FF6802 L14, FF6801-L L51: crossing -> the adjustable stud's washer face
- On the 80 FS rows with dimensions that have such a stud, Air-Way's stud (tip -> shoulder) is the same per ORB dash:

  | ORB dash | -04 / -05 | -06 | -08 | -10 | -12 to -32 |
  |---|---|---|---|---|---|
  | Air-Way stud (tip -> shoulder) | 0.43 | 0.47 / 0.48 | 0.54 / 0.55 | 0.63 | 0.73 |
  | Our ORB end library (thread + groove; Brennan 6400/6401/6405/6410) | 0.340 | 0.395 | 0.438 | 0.498 | 0.594 |
  | Our adjustable stud, tip -> washer face (NWO_MEAS, Brennan 6801) | 0.386 | 0.433 | 0.490 | 0.560 | 0.653 |

  Two exceptions: FS6540-10-10-O 0.72 and FS6400-24-24-O 0.82.
- So the fixed stud on FS parts is 0.08 - 0.14 longer than our library end, and the adjustable stud 0.04 - 0.08 longer. Probably the
  heavy-duty SAE J1926-2 stud that ORFS fittings carry, where our library comes from J1926-3-style JIC parts. Not confirmed: J1926 is
  not in the repo.
- (a) Recommended: follow Air-Way (the dimension source). The hex and the washer face sit where Air-Way puts them. The stud's own
  shape (thread length, undercut, any plain shank) is measured on the pilots FS6400-08-08-O and FS6801-08-08-NWO-FG and becomes new
  end entries `ORB_FS` / `NWO_FS`.
- (b) Reuse the existing ORB / NWO ends as Q-TRANSFER-ENDLIB says, and keep L9 / L11 as cross-checks only. The hex would then be
  0.08 - 0.14 longer than Air-Way's on every FS6400 / FS6540 row, and the washer 0.04 - 0.08 off on every FS68xx row.

**Q-FS-2NDSHAPE - Air-Way's own 3D models as a second shape source?**
- The generators write a row ASSUMED when one of its end shapes comes from a single manufacturer's STEP. That is how every JIC swivel,
  NPSM swivel and adjustable-ORB row is written today (gen_tee.py lines 927-941).
- The new ORFS ends would come from Brennan STEPs only. Every FS row would then be written ASSUMED in its SW2 table, all 229 VERIFIED
  included; the review tables keep VERIFIED. The 42 FS68xx rows are ASSUMED anyway through the adjustable-stud rule.
- Air-Way publishes its own 3D model of nearly every ORFS part: `Has3DModel` = true on all products of FF2403, FF6500, FF318, FF319,
  FF6400, FF6801 ... (3DContentCentral). If the pilot ends are measured on Air-Way's file too, the end shapes have two independent
  manufacturers. Where they agree, the end library is VERIFIED and the rows can stay VERIFIED. Air-Way is also the accepted dimension
  source, so its model is not "Brennan data".
- Cost: about 10 extra downloads (STEPS_NEEDED part 5). The 3DContentCentral sign-in is yours to do.

-> Recommended: yes, for the pilots. "No" is also fine: then the rows ship ASSUMED.

**Q-FS-NUT - take the swivel nut hex from Air-Way's FF318 nut where the row's own column cannot be used?**
- The female swivel nut is the FS0318 nut. Air-Way FF318 gives its hex S and length h, = Brennan on every compared size. Air-Way's
  own swivel rows show the nut right behind the body hex: hex face -> nut face = FF318 h -0.01 to +0.05 on FS6504 and FS6540.
- FS6504 (Air-Way FF7504): its "S" column (0.40 ... 1.46) cannot be a nut hex. It is smaller than the nut's own thread.
- FS6505-16-16: prints 1.61 where FF318-16 is 1.63 (Brennan 1.625).
- Proposal: nut hex = the row's column where it agrees with FF318 S to the rounding. Otherwise use FF318 S of the same dash and write
  the row's printed value in `$COMMENT`. The staged FS2406 table already takes its nut from FF318.

-> Recommended: yes.

**Q-FS2406-NUT - FS2406 "Tube End Reducer": with or without its nut?**
- The reducer itself is a round body with no hex: collar d8 with the flat seal face, a neck, then a male face-seal end.
- Air-Way sells FF2407 "W/FF318-n NUT", and Brennan's FS2406 table prints the nut hex. Choices:
  - model the reducer + nut as one solid, as every swivel nut is modelled, or
  - model the reducer alone.

-> Recommended: reducer + nut. The nut is the FS0318 of the first dash.

**Q-FS2408-HOLE - FS2408 plug: solid, or with Air-Way's hole?**
- Every Air-Way FF2408 row is "-O-W/HOLE": a blind hole d1 "OPT" from the face, column W/HOLE. OMi's part numbers carry no hole suffix.
- Choices: build solid, or with the hole (feature suppressed per row, as on 2408 -H).

-> Recommended: ask OMi. Until then build solid, with the hole column kept and the feature suppressed.

**Stated so you can object (no answer needed):**
- forged FS bodies use the existing gen_tee body patterns, with Air-Way legs and flats; the shape is confirmed by one Brennan pilot per
  family.
- -LN kits model the fitting only; the lock nut is a separate part and is not modelled (as on 2700 / 2705 / 2706 -LN).
- Air-Way thread typos never block a row: threads come from the end library by part-number dash (section 8).

## 1. What gets modelled: 31 new masters + 1 fold, 288 configurations

| Master | Folds in | Buildable (V + A) | MISSING (out) | Generator | Pattern copied | Ends (part-number order) |
|---|---|---|---|---|---|---|
| FS2403 | - | 15 (15 + 0) | 2 | gen_straight2 | 2403 | FSM x FSM |
| FS2404 | - | 22 (1 + 21) | 2 | gen_straight2 | 2404 / 6401 | FSM x male NPTF |
| FS2406 | - | 13 (11 + 2) | 6 | gen_straight2, round body | 5404N `round` + new FFS end | FFS tube end (+ nut, Q) x FSM |
| FS2408 | - | 8 (5 + 3) | 1 | gen_straight2 | 2408 | FSM, plug head (hole: Q) |
| FS2700 | FS2700-LN | 16 (14 + 2) | 0 | gen_straight2 | 2700 | FSM x FSBH (thread over i2) |
| FS6400 | FS6400-L | 32 (24 + 8) | 4 | gen_straight2 | 6401 | FSM x ORB stud (Q-FS-ORBSTUD) |
| FS6403 | - | 7 (4 + 3) | 1 | gen_straight2 | 2403 | FSM x male JIC |
| FS6504 | - | 7 (3 + 4) | 0 | gen_straight2 | 6504 | FSSW x male JIC |
| FS6505 | - | 3 (0 + 3) | 3 | gen_straight2 | 6505 | FSSW x male NPTF |
| FS6540 | - | 6 (5 + 1) | 0 | gen_straight2 | 6402 | FSSW x ORB stud |
| FS6565 | - | 4 (4 + 0) | 2 | gen_straight2 | 6565 | FSSW x FSSW |
| FS0318 | - | 9 (8 + 1) | 0 | gen_straight2 | 0318 (nut) | FS nut: thread + inner lip |
| FS0306 | - | 6 (6 + 0) | 3 | gen_straight2 | wave-1 0306 (locknut) | FS thread through, face chamfers |
| FS6801 | FS6801-L | 22 (22 + 0) | 8 | gen_tee | 6801 | FSM x adjustable stud (90 deg) |
| FS2701 | FS2701-LN | 12 | 9 | gen_tee | 2701 | FSM x FSBH with collar (90 deg) |
| FS2704 | FS2704-LN | 12 | 6 | gen_tee | 2704 | FSM / FSBH / FSM (run tee) |
| FS2702 | FS2702-LN | 10 | 8 | gen_tee | 2702 (e45) | FSM x FSBH (45 deg) |
| FS2703 | FS2703-LN | 8 | 8 | gen_tee | 2703 | FSM / FSM / FSBH (branch tee) |
| FS2500 | - | 7 | 9 | gen_tee | 2501 elbow body (2500HX pattern) | FSM x FSM (90 deg) |
| FS2501 | - | 7 | 8 | gen_tee | 2501 | FSM x male NPTF (90 deg) |
| FS6802 | - | 7 | 10 | gen_tee | 6802 (e45, dmap) | FSM x adjustable stud (45 deg) |
| FS6804 | - | 7 | 0 | gen_tee | 6804 | FSM / adjustable / FSM |
| FS2603 | - | 6 | 5 | gen_tee | 2603HX bars | FSM x 3 |
| FS6600 | - | 6 | 1 | gen_tee | 6600 | FSM / FSM / FSSW |
| FS6500 | - | 5 | 8 | gen_tee | 6500 | FSM x FSSW (90 deg) |
| FS6602 | - | 5 | 2 | gen_tee | 6602 | FSM / FSSW / FSM |
| FS6803 | - | 3 | 2 | gen_tee | 6803 | FSM / FSM / adjustable |
| FS6809 | - | 3 | 4 | gen_tee (new: swivel + adjustable on one part) | 6500 + 6801 | FSSW x adjustable (90 deg) |
| FS2503 | - | 2 | 10 | gen_tee | 2503 (e45, dmap) | FSM x male NPTF (45 deg) |
| FS2650 | - | 1 | 8 | gen_tee | 2650 | FSM x 4 (cross) |
| FS0319 | - | 8 (6 + 2) | 1 | gen_ring SLEEVE (new profile) | 0319T test type | collar d8, spigot, bore |
| (staged) 4000 | + FS4000 | 9 (0 + 9) | 0 | gen_ring ORING | 4000 | torus I.D. / W |

All forged rows are VERIFIED (123): the user's forged rule of 2026-10-15. Totals:

| Generator | Masters | Configurations |
|---|---|---|
| gen_straight2 | 13 | 148 |
| gen_tee | 17 | 123 |
| gen_ring | 1 + the FS4000 fold | 17 |
| **All** | **31 + fold** | **288** (229 V + 59 A) |

The **12 series with no dimensions at all** (80 rows) get no master now. When data come, they would be built as follows:

| Series | Generator, pattern | Needs |
|---|---|---|
| FS2405 | gen_straight2, FSM x female NPTF, 2405 | |
| FS6402 | gen_straight2, FSM x JIC swivel, 6402 / 6504 | |
| FS1700 / FS1800 | gen_straight2, FSM x code 61 / 62 head, 1700 | FLG62 measured at -08 only |
| FS1704 / FS1804 -FG | gen_tee + the wave-2 FLG61LEG capability | |
| FS2502 / FS2601 / FS6503 / FS6502 -FG | gen_tee, NPTFF / NPTFM / FSSW legs | FS6502: the L52 meaning, Air-Way drawing s30 |
| FS0304-C cap assembly | wave-1 0304 cap-nut pattern + an insert | OMi data |
| FS7202 | | BSPP stud: international thread, probably out of scope by the skill's rule; ask when it has data |

Correction to the task wording: **gen_straight2 builds no elbows.** Every forged elbow and tee goes to gen_tee, as 2501 / 6500 / 6801
do. gen_bent has no FS use (no bent-tube FS series); its read-only import of the live gen_straight2 is the pattern for staging this work
(section 5).

## 2. End shapes needed (new end-library entries)

### Data tables (no STEP needed)

| Entry | Content | Source |
|---|---|---|
| `FS_THR[dash]` | face-seal thread per dash: -04 9/16-18, -06 11/16-16, -08 13/16-16, -10 1-14, -12 1 3/16-12, -16 1 7/16-12, -20 1 11/16-12, -24 2-12, -32 2 1/2-12 | Air-Way's callout on the FS rows of that dash (680 of the 699 thread cells in the 51 tables; the other 19 are typos or callouts of DROP rows, section 8) = Brennan catalog |
| `FSNUT[dash]` | nut hex S / nut length h: -04 0.69 / 0.58, -06 0.81 / 0.67, -08 0.94 / 0.83, -10 1.13 / 0.93, -12 1.38 / 1.02, -16 1.63 / 1.10, -20 1.88 / 1.10, -24 2.25 / 1.10, -32 2.88 / 1.30 | Air-Way FF318 (staged FS0318 table; VERIFIED -04 ... -24) |
| `FS_ORING[dash]` | face-seal O-ring I.D. / W (0.070 to -24, 0.103 at -32) | Air-Way s40 (staged FS4000 table); used only to cross-check the measured groove |

### Shape entries (measured on Brennan pilots, shape only; Q-TRANSFER-ENDLIB = yes)

**FSM - male face-seal end** (SAE J1453 male end; `end_FSM` in gen_straight2, `leg_FSM` in gen_tee).
- Profile from the face inward, as `end_JICM` builds its V list:
  1. flat face from the bore to the groove inner radius GI;
  2. O-ring groove GI -> GO, depth GD, drawn rectangular as `end_FLG61`'s face groove (proven in SolidWorks on 1700 and the gen_bent
     flange heads). If the pilot shows a dovetail, it is noted and still drawn rectangular;
  3. outer land to the face radius FR, edge chamfer if the pilot shows one;
  4. thread major (FS_THR) over THDL, as a Thread feature `THD_End<x>`, male, like JICM;
  5. thread run-out / relief (radius RR, length RL) to the shoulder at the end length ENDL.
- Table `FSM_MEAS[dash]` = dict(FR, GI, GO, GD, CH, THDL, RR, RL, ENDL) for -04 ... -32. Columns `FSM<x>_GRVIR / _GRVOR / _GRVD /
  _FACER / _THDL / _RELR / _RELL` + the Thread-feature columns of `end_JICM`.
- Checks:
  - bore radius < GI - 0.03;
  - groove I.D. within the FS4000 O-ring I.D. (warn otherwise);
  - end length < leg length;
  - shoulder vs forged flats (risk R1).

**FSBH - male bulkhead end.**
- FSM nose + the face-seal thread run from the tip to Air-Way i2.
- On forged legs, a collar of Air-Way d17 x i4 behind it. This is `leg_JICBH`'s signature with (i2, i4, d17) in place of (i2, K1, O).
- On the straight FS2700 there is no collar: the thread runs from the hex face, as `end_JICBH` does. Air-Way drawing s13 shows no
  collar there.

**FSSW - female face-seal swivel** (`end_FSSW` / `leg_FSSW`, the `end_JICSW` structure: outside VO + cavity VG, nut and body one solid).
- Outside (VO), from the nut face: nut hex (FSNUT S or the row's column, Q-FS-NUT) over the nut hex length; nut rear face at FSNUT h;
  neck; body face.
- Cavity (VG): mouth chamfer, thread minor (ASME B1.1 basic minor of FS_THR) over TE, relief, then the flat seal face at SEAL from the
  nut face, closing radially to the bore.
- Leg input = crossing (or tip) -> nut face, from Air-Way: L21 / L40 / L34 / L16 / L45. The line positions on Air-Way's drawings are
  ambiguous, but Brennan's drawings dimension these lengths to the nut face and print the same numbers, and Air-Way's own FS6504 / FS6540
  rows put the nut face h -0.01 ... +0.05 past the body hex. The pilot FS6500-08-08-FG confirms: crossing -> nut face = 1.49?
- Air-Way also prints the swivel body length on FS6504 (L38 - L39) and FS6540 (L35 - L37): 0.61 / 0.66 - 0.69 / 0.84 / 0.94 / 1.03 /
  1.11 / 1.15 for -04 ... -20. That is an Air-Way value for the body face, used as input where printed and as a cross-check elsewhere.
- Table `FSSW_MEAS[dash]` (-04 ... -20; -24 once a -24 swivel row has dimensions): HEXL, NECKR, BODYS, MINR, TE, RELR, SEAL,
  mouth chamfer.
- Thread: HELIX type (helix + swept cut) as on JICSW. Never SolidWorks' Thread feature on a female edge: it crashed SolidWorks on
  2026-10-15.

**FFS - tube end of FS2406.** Collar of Air-Way d8 with the flat seal face at x = 0, then a neck. Optional nut (Q-FS2406-NUT) drawn as
FSSW's outside VO, at the measured offset. Neck radius and collar length come from the pilot FS2406-08-06; other sizes use a ratio rule
(ASSUMPTION, written in `$PRP@AxialSource`).

**FSNUTF - inside of the FS0318 nut.** The thread from the open face over TE, a relief, then the inner lip (holds the sleeve or swivel
body) with its bore. Same topology as `end_UNFF`: pocket + through bore. The per-dash values come from `FSNUT_MEAS` instead of MS51531.
If pilot P6 shows the loose nut = the swivel nut, `FSNUT_MEAS` is filled from the `FSSW_MEAS` nut values and needs no STEP per size.

**FS locknut (FS0306).** Wave-1 `end_NUTCSA` / `end_NUTCSB` (`nut_thru`) with the FS thread. Face chamfer or countersink from the pilot
FS0306-08 as a rule per dash (e.g. countersink to the thread major; ASSUMPTION).

**FS sleeve (FS0319, gen_ring).**
- A SLEEVE profile variant: flat seal face, collar d8 (Air-Way), spigot, bore = tube OD (+ braze clearance from the pilot), no inner
  37 deg cone. The current SLEEVE check `bore < FRONTIR` must allow "no cone".
- Collar length and spigot come from the pilot FS0319-08 and a per-size rule (ASSUMPTION), or from per-size STEPs (STEPS_NEEDED
  part 4).

**ORB_FS / NWO_FS - straight-thread studs on FS parts.** Only if Q-FS-ORBSTUD (a). Thread length and undercut come from the existing
ORB / NWO data per dash. The stud length up to the shoulder or washer face comes from Air-Way (L8-L9, L34-L35, L10-L11, L13-L14,
L50-L51). The shape of the extra length (plain shank or longer undercut) comes from the pilots FS6400-08-08-O / FS6801-08-08-NWO-FG.

**Reused unchanged:** JICM (FS6403, FS6504; Air-Way's FF7504 tip -> hex = 0.55 / 0.56 / 0.66 / 0.76 / 0.86 / 0.91 / 0.96 = our
MS33656J end lengths 0.550 / 0.556 / 0.657 / 0.758 / 0.864 / 0.911 / 0.958 exactly), NPTFM (FS2404, FS2501, FS2503, FS6505), the forged
body patterns (2500HX elbow, 2603HX bars, 2504 45 deg, 2701 bulkhead), and `PUCK_INSET` (batch-16 puck fix).

## 3. Review-table columns -> generator inputs

Meanings were read off Air-Way's spec drawings (section 9) and cross-read with the Brennan column each one was checked against
(`compare_orfs.py` PAIRS / FORGED_PAIRS). INPUT = drives the model, CHECK = compared only, - = not used. In every table:
- `THDMAJ_*@DRIVE` is a thread check against FS_THR, JIC or ORB by dash (typo rows warn, section 8);
- `$PRP@Thread_*` keeps Air-Way's printed callout;
- `$PRP@TubeOD` is a property.

**Straights (gen_straight2):**

| Series (Air-Way) | Length L | Hex | Other columns | Bores |
|---|---|---|---|---|
| FS2403 (FF2403) | L6 face -> face | S1HEX | - | D1_1 / D1_2, step at the hex mid-plane (2403 rule) |
| FS2404 (FF2404) | L face -> pipe tip | S1HEX | - | D1 (FS) / D2 (pipe), mid step |
| FS2406 (FF2407) | L36 collar face -> male face | none (round) | D8@DRIVE collar dia (INPUT); NUTHEX@HEX = FF318 S (INPUT if Q-FS2406-NUT) | D1 through |
| FS2408 (FF2408) | L24 face -> plug back | S1HEX | WHOLE@BORE hole dia (Q-FS2408-HOLE) | - |
| FS2700 (+LN) (FF2700) | L15 face -> bulkhead tip | S4_1HEX (body) | I2@DRIVE bulkhead length, hex face -> tip (INPUT); S4_2HEX = lock nut (-, not modelled) | D1_1 / D1_2 |
| FS6400 (+L: L32->L8, L31->L9) (FF6400) | L8 face -> ORB tip | S5HEX | L9 face -> hex ORB-side face (INPUT if Q-FS-ORBSTUD (a), else CHECK); Style (only A builds) | D1 (FS) / D20 (ORB) |
| FS6403 (FF7403) | L41 face -> JIC tip | S1HEX | - | D1 / D |
| FS6504 (FF7504) | L40 JIC tip -> nut face | C2HEX body hex (INPUT; differs from Brennan H HEX on 6 of 7 sizes, ASSUMED) | L38 hex JIC side -> nut face, L39 hex length (CHECK / body-face INPUT); SHEX (-: not a nut hex, Q-FS-NUT) | D2 (JIC) / D19 (swivel) |
| FS6505 (FF6505) | L16 pipe tip -> nut face | S1HEX | SHEX nut (INPUT, Q-FS-NUT at -16) | D2 / D19 |
| FS6540 (FF6402) | L34 ORB tip -> nut face | S5HEX | SHEX nut (INPUT); L35 hex ORB side -> nut face, L37 hex length (Q-FS-ORBSTUD / body-face CHECK) | D20 / D19 |
| FS6565 (FF6565) | L45 nut face -> nut face | S1HEX | S_1HEX / S_2HEX nuts (INPUT) | D19_1 / D19_2 |
| FS0318 (FF318) | H nut length | SHEX | - | lip bore from FSNUT_MEAS |
| FS0306 (FF306) | H2 thickness | S4HEX | - | thread minor through |

**Forged (gen_tee).**
- Body hex for all forged series: `S2HEX@HEX` = forged flats (= Brennan JJ FLATS on every VERIFIED row).
- Leg tuples are (kind, length, bore, thread-major) as in gen_tee's SPEC.

| Series | Legs | Extra SPEC keys |
|---|---|---|
| FS2500 | (FSM, L7_1, D1_1, THDMAJ_D_1), (FSM, L7_2, D1_2, THDMAJ_D_2); elbow | - |
| FS2501 | (FSM, L7, D1, THDMAJ_D), (NPTFM, N, D2, -); elbow | the NPTF thread is checked from `$PRP@Thread_A` (no PIPEOD column) |
| FS2503 | (NPTFM, N2, D2, -), (FSM, L12, D1, THDMAJ_D); e45, dmap (1, 0) | - |
| FS2603 | (FSM, L7_1), (FSM, L7_2), (FSM, L7_3); tee | - |
| FS2650 | four FSM legs L7_1 ... L7_4; cross | - |
| FS2701 (+LN) | (FSM, L16), (FSBH, L17); elbow | `bh=('I2@DRIVE','I4@DRIVE','D17@BORE')`; S4HEX = lock nut (-) |
| FS2702 (+LN) | (FSM, L12), (FSBH, L18); e45 | bh as FS2701 |
| FS2703 (+LN) | (FSM, L16_1), (FSM, L16_2), (FSBH, L7); tee | bh |
| FS2704 (+LN) | (FSM, L16_1), (FSBH, L17), (FSM, L16_3); tee, bulkhead on the run like 2704 | bh |
| FS6500 | (FSM, L7, D1), (FSSW, L21, D19); elbow | `fssw=('SHEX@HEX',)` |
| FS6600 | (FSM, L7_1), (FSM, L7_2), (FSSW, L21); tee | fssw |
| FS6602 | (FSM, L7_1), (FSSW, L21), (FSM, L7); tee | fssw |
| FS6801 (+L: L50->L10, L51->L11) | (FSM, L7, D1), (NWO, L10, D20); elbow | `nwo` (below); L11 = washer face |
| FS6802 | (NWO, L13, D20), (FSM, L12, D1); e45, dmap (1, 0) | nwo; L14 = washer face |
| FS6803 | (FSM, L7_1), (FSM, L7_2), (NWO, L10); tee | nwo; L11 |
| FS6804 | (FSM, L7_1), (NWO, L10), (FSM, L7_3); tee | nwo; L11 |
| FS6809 | (FSSW, L21, D19), (NWO, L10, D20); elbow | fssw and nwo together (no JIC precedent); SHEX = nut (= Brennan C1 HEX), S3HEX = lock nut (= Brennan C2 HEX), L11 = washer face |

The `nwo` key and two column fixes:
- `nwo=(I3, locknut hex, thread length, groove dia)`. The FS tables print none of I3, thread length or groove; only the lock-nut hex
  `S3HEX@HEX` (= Brennan C HEX). Plan:
  - I3 '=6801': the JIC 6801 value of the same ORB size (= Brennan), as 6803 / 6804 already do;
  - thread length and groove dia from the ORB library ('=ORB', a small gen_tee extension);
  - under Q-FS-ORBSTUD (a), the washer face instead from Air-Way L11 / L14 / L51.
- `D17@BORE` is **not a bore**: it is the bulkhead collar diameter (Air-Way drawings s23 / s29). The SPEC reads it as the collar; rename
  it `D17@DRIVE` when the tables move to `04_DESIGN_TABLES`.
- `I4@DRIVE` = collar thickness (0.06 on most rows).

**Rings (gen_ring):**
- FS0319: L@DRIVE -> L, D8@DRIVE -> 2 x COLLARR, TubeOD -> BORER.
- FS4000: ID@DRIVE / W@DRIVE -> RINGR / CSDIA. The fold adds 'FS4000' to `SPEC['4000']['tables']`. The row description becomes "for -NN
  SAE J1453 face-seal ends" for FS rows; the current text says J1926.

## 4. Risks found while planning (geometry)

**R1 - FS ends proud of the forged flats.**
- On forged legs the face-seal thread major exceeds the body flats S2 (VERIFIED = Brennan JJ FLATS):

  | Dash | Thread major | Flats S2 | Hex corners | Position |
  |---|---|---|---|---|
  | -08 | 0.8125 | 0.75 | 0.866 | between flats and corners |
  | -20 | 1.6875 | 1.63 | 1.882 | between flats and corners |
  | -24 | 2.000 | 1.87 / 1.88 | 2.16 | between flats and corners |
  | -12 | 1.1875 | 1.18 (FS2501, FS2603, FS2703 + LN, FS2704-LN) or 1.19 (the rest) | 1.36 / 1.37 | 0.0075 above / 0.0025 below the flats |
  | -04 / -16 | 0.5625 / 1.4375 | 0.56 / 1.44 | - | within 0.0025 of the flats |

- JIC never had this: there gen_tee's 2603HX rule raises A/F to the thread major. Raising S2 would change a VERIFIED dimension, so:
  - FS legs are kept out of that max;
  - an FS end may stand proud of the arm, as the male NPTF end does on Brennan 5600-16-16-16-FG.
- Where the end's first radius lies between flats and corners, the arm's end face has crossing outlines. That is the geometry that broke
  2702 / 2703 -16 (BH_ARM_SHORT).
- The pilots show how Brennan forms that shoulder: a relief below the flats, or a round boss. The SolidWorks dry run of every size
  decides whether an offset is needed.

**R2 - bulkhead collar near the hex corners.** Collar radius d17/2 vs corner radius S2/sqrt3:

| Dash | Collar radius | Flats radius | Corner radius | Position |
|---|---|---|---|---|
| -06 | 0.435 | - | 0.433 | near-tangent |
| -10 | 0.595 | 0.530 | 0.612 | crossing |
| -12 | 0.685 | - | 0.687 / 0.681 | near-tangent |
| -16 | 0.810 | 0.720 | 0.831 | crossing |

The 2026-10-02 "stop the arm 0.001 short" approval covers 2702 / 2703 -16 only. Extending `bh_short` to FS sizes needs your OK when a
dry run fails.

**R3 - swivel reference point.** Taken as the nut face (section 2, FSSW). The pilot measurement settles it before any swivel master is
generated.

**R4 - the ORB / adjustable studs:** Q-FS-ORBSTUD.

**R5 - puck defect.** Every forged FS elbow uses the corner puck, so the batch-16 `PUCK_INSET` fix is required. That is a reason to build
on the batch-16 toolchain (section 5).

**R6 - 45 deg legs.** swiv.py cannot section a 45 deg leg (MEASURED-ENDS note, 2026-10-01). Swivels are therefore measured on 90 deg
parts only (FS6500 per dash), and the 45 deg families take the ends from the library.

**R7 - FS0319 per-size shape.** One pilot gives -08. The other sizes need a rule (ASSUMPTION) or per-size STEPs.

**R8 - single-source end shapes downgrade VERIFIED rows to ASSUMED** (Q-FS-2NDSHAPE).

## 5. Toolchain plan (where the code goes)

- **Base:** the batch-16 toolchain `tools/_out/puckfix_20261009/tools_new` (= wave-1 merged tools + `PUCK_INSET`), copied to a new
  staging folder `tools/_out/orfs_<date>/tools/`. The live `tools/` lacks the wave-1 lock-nut ends, the forged extractors (`forged.py`,
  `fgelbow.py`, `elbow90.py`, `tee_model.py`, `nutprof.py`, `locknut.py`) and the puck fix. If batch 16 ships first, branch from the
  live tools instead.
- **Review-table location:** gen_straight2 / gen_tee read only `04_DESIGN_TABLES` (`REV = P.DESIGN_TABLES`). Add an env override
  `GS_REV` / `GT_REV` (as gen_ring `GR_REV` / gen_bent `GB_REV`) so the staged FS tables are read where they are. Work on copies of the
  staged tables carrying the section-8 fixes; never the originals.
- **New code only** (no existing path changes):
  - gen_straight2:
    - `end_FSM`, `end_FSBH`, `end_FSSW`, `end_FFS`, `end_FSNUTF` (+ `ORB_FS` under Q-FS-ORBSTUD (a));
    - their dimension blocks in `emit()`: FSM = FLG61 groove dims + JICM thread dims, FSSW = the JICSW block pattern;
    - `lib_gaps` messages that name the missing STEP;
    - `thrchk` for FS kinds against FS_THR, with the known-typo list -> warn;
    - `ln` detection for '-LN-' inside the part number.
  - gen_tee:
    - `leg_FSM`, `leg_FSBH`, `leg_FSSW` + dispatch in `build_rows`;
    - FS legs out of the A/F max (R1);
    - fssw and nwo in one SPEC (FS6809);
    - '=ORB' for the stud data;
    - the FS legs in the single-source DataStatus rule (lines 927-941), with a text naming the ORFS STEPs;
    - fold maps for -LN / -L.
  - gen_ring: the FS4000 table + description, and the SLEEVE profile variant.
- **Every new SPEC root starts with "FS".**
  - `Sub BuildFS2403` and `Build_FS2403_MASTER.bas` are valid names.
  - Check that sp3fix / progress_patch / vbacheck / coverage do not assume a numeric root.
  - gen_straight2's `dashes()` (`-(\d\d)`) already reads FS2700-LN-04-04 and FS6400-L-04-04-O correctly.
- **Rule from CLAUDE.md:** changing a generator touches every macro. Regenerate ALL existing roots with the old and the new toolchain:
  every existing macro and SW2 must be byte-identical (CRLF / LF aside), and only the new FS roots appear. Then, per FS root: dofcheck,
  allcfg_check, vbacheck, regress; then the SolidWorks verify loop of CLAUDE.md (dry runs into staging, sweep_configs, geometry,
  screenshots). Nothing goes to `11_MASTERS` before you review it.
- **Measuring (tools/measure, new):**
  - `fsm.py`: male end; reuses `flange.py`'s groove finder and `jicm.py`'s line walker.
  - `fssw.py`: swivel; the `swiv.py` structure.
  - `fsnut.py`: on `nutprof.py`.
  - the FS sleeve: in gen_ring's test scripts' manner.
  - the FS leg kinds added to `forged.py` / `fgelbow.py` for the forged pilots.
  - Validation before use, since no earlier measurement exists for these ends:
    - (1) the two FSM ends of FS2403-08-08 agree, and agree with the male leg of FS6500-08-08-FG;
    - (2) the swivel nut of FS6500-08-08-FG = the FS0318-08 nut = Air-Way FF318 -08 (hex 0.94, h 0.83);
    - (3) the groove I.D. fits the FS4000-08 O-ring (I.D. 0.489);
    - (4) closed loop: OCP rebuild of the generator's own end (as `nwo_model.py` / `nwo_closedloop.py`) -> measure -> returns the table.

## 6. Build order (work packages)

1. **WP0 - before anything:** your answers above; the OMi website list (sets BUILD / DROP); the batch-16 base; working copies of the
   staged tables with the section-8 fixes, the D17 rename and the fold maps.
2. **WP1 - no STEP needed:**
   - FS4000 into the staged 4000 master (gen_ring, staging dry run);
   - FS_THR / FSNUT / FS_ORING in the generator;
   - all 31 FS SPECs written. Rows skip with "no end data - needs BRENNAN_<pn>" until the measured tables exist.
3. **WP2 - pilots** (STEPS_NEEDED part 1): the extractors, their validation, the -08 entries of FSM / FSSW / FSBH / nut / sleeve /
   locknut / FFS, and the stud decision. First dry runs on the -08 rows: FS2403-08-08, FS6500-08-08-FG, FS2701-08-08-FG, FS0318-08 ...
4. **WP3 - end library per dash** (STEPS_NEEDED part 2): FSM -04 ... -32, FSSW -04 ... -20. Then, in this order:
   - the straights, largest first: FS6400 (32), FS2404 (22), FS2700 (16), FS2403 (15), FS2406 (13), FS0318 (9), FS2408 (8), FS6403 (7),
     FS6504 (7), FS0306 (6), FS6540 (6), FS6565 (4), FS6505 (3);
   - the sleeve FS0319 (8).
5. **WP4 - forged families**, one pilot each (part 3), largest first: FS6801 (22), FS2701 (12), FS2704 (12), FS2702 (10), FS2703 (8),
   FS2500 / FS2501 / FS6802 / FS6804 (7 each), FS2603 / FS6600 (6), FS6500 / FS6602 (5), FS6803 / FS6809 (3), FS2503 (2), FS2650 (1).
6. **WP5 - ship** when you say so, as a batch:
   - RUN_ME, QA_Log;
   - Topologies: 31 new topologies; the "126 topologies" count changes;
   - coverage, PROJECT_STATUS;
   - the CLAUDE.md / skill one-master text.

## 7. Counts that depend on the open points
- If Q-FS-2NDSHAPE = no: every FS row is ASSUMED in its SW2 table (288).
- If yes and the Air-Way models agree: the 187 VERIFIED rows without an adjustable stud stay VERIFIED. The 42 FS68xx rows also need
  the stud to agree with Air-Way's FF68xx model.
- Rows blocked by data until fixed: none of the 288. The 5 rows with a wrong thread-major cell build with the dash thread (section 8).
  Rows that may block on geometry: R1 / R2 sizes, known only after the dry runs.

## 8. Data issues in the staged tables (found 2026-10-16; no file edited)

**D1 - Air-Way thread typos in 9 BUILD rows.** All build with the dash thread.
- Five also carry a wrong `THDMAJ` cell, which the thread check would block:
  - FS2501-08-12-FG "3/16-16" (0.1875)
  - FS2700-LN-04-04 "9/19-18" (0.4737)
  - FS2704-LN-12-12-12-FG "1. 3/16-12" (empty)
  - FS2704-LN-16-16-16-FG "1 /16-12" (empty)
  - FS6809-16-16-NWO-FG "17/16-12" (1.0625), and its ORB thread "15/16-12" (0.9375 for 1 5/16-12)
- Callout only, cell right:
  - FS2404-08-06 "13/16-12"
  - FS2704-06-06-06-FG "11/16-18" (x3)
  - FS6400-L-06-06-O "11/16-18"
  - FS6801-06-08-NWO-FG "11/16-18"
- Proposal: fix the cell from the dash in the working copy and keep the printed callout in `$COMMENT`.

**D2 - FS2704-LN-04-04-04-FG S4 ".081"** (0.81 on FS2704-04-04-04-FG). It is the lock nut, not modelled; fix the cell.

**D3 - FS6504:** "S" is not a nut hex (Q-FS-NUT). C2 equals Brennan's H HEX only at -08. The 3 VERIFIED rows are VERIFIED on L40 only.

**D4 - FS6505-16-16:** nut 1.61 vs FF318 1.63 / Brennan 1.625.

**D5 - FS0319-24 d8 1.71** vs Brennan 1.910, while Air-Way's own FF2407-24 collar is 2.00. Built to Air-Way (ASSUMED) under the
2026-10-15 rule; worth holding until OMi confirms.

**D6 - small Air-Way inconsistencies on the bulkheads** (built as printed, noted in `$COMMENT`):
- FS2704-06-06-06-FG i2 1.30 (1.34 elsewhere);
- FS2704(-LN)-12 i2 1.63 vs 1.64;
- FS2702-08-08 d17 0.97 vs 1.00;
- i4 0.10 (FS2704 -08) and 0.13 (FS2703 -12) vs 0.06 elsewhere.

**D7 - the forged compare checked legs, flats and nut hex only.** On the VERIFIED bulkhead rows, i2 / i4 / d17 / S4 are Air-Way-only
values. That is per your 2026-10-15 rule, but worth knowing.

**D8 - FS2406 collar d8 = FS0319 sleeve d8** except -16-08 (1.32 / 1.35), -20-16 (1.57 / 1.60), -24-20 (2.00 / 1.71, see D5) and
-32-24 (2.37 / 2.40).

**D9 - FS6400-24-24-O and FS6540-10-10-O** are the only stud-length outliers (0.82 / 0.72); see Q-FS-ORBSTUD.

## 9. Evidence (how the letter meanings were read)

**Air-Way spec drawings**, public catalog images, viewed 2026-10-16 in the browser:
`https://parts.air-way.com/Assets/Catalog/Images/Series/Catalog.Category.Series.Spec.<sid>.jpg`, for sid 3 (FF306), 5 (FF318),
6 (FF319), 9 (FF2403), 10 (FF2404), 11 (FF2407), 12 (FF2408), 13 (FF2700), 14 (FF6400), 15 (FF6400-L), 16 (FF6402), 19 (FF7504),
23 (FF2701), 24 (FF6500), 25 (FF6801), 29 (FF2702), 31 (FF6802), 485 (FF6505). What they show:

| Letters | Meaning |
|---|---|
| L6 / L / L36 / L24 / L8 / L41 / L32 | overall (straights) |
| L16 (FF6505) / L34 (FF6402) / L40 (FF7504) / L45 (FF6565) | overall to the swivel nut face |
| L9 / L31 | face-seal face -> the hex's ORB-side face |
| L35 (FF6402) | the hex's ORB-side face -> swivel nut face |
| L38 (FF7504) | the hex's JIC-side face -> swivel nut face |
| L37 / L39 | hex length |
| L7 / L12 / L16 (elbows, tees) | face-seal legs from the crossing |
| L21 | swivel legs, crossing -> nut face |
| L10 / L13 / L50 | stud legs |
| L11 / L14 / L51 | crossing -> washer face |
| L17 / L18 | bulkhead legs to the tip |
| i2 | bulkhead thread length, tip -> collar |
| i4 | collar thickness |
| d17 | collar diameter |
| S2 | forged flats |
| S3 / S4 | lock nut |
| S / S(n) | swivel nut |
| S1 / S5 / C2 | straight body hex |
| d8 | sleeve / collar OD |
| h / h2 / L | nut length, lock-nut thickness, sleeve length |
| W/HOLE | optional blind hole in the plug face |

**Brennan ORFS catalog** (`07_RAW_EXTRACTS/brennan_catalogs/ORFS Catalog.pdf`, pages 6 and 9 rendered locally): L LGTH (FS6504 / FS6540 /
FS6565 / FS6505) and AAA (FS6500) are drawn to the swivel nut's outer face.

**Numbers:** computed from the staged tables (read-only):
- the ORB stud lengths (Q-FS-ORBSTUD);
- FF7504 tip -> hex = the MS33656J JIC end length at all 7 sizes;
- hex -> nut face = FF318 h -0.01 ... +0.05;
- `Has3DModel` on the Air-Way products (`tools/_out/orfs_airway_20261015/raw/series_<sid>_pass1.json`).
