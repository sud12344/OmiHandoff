# OMi fitting library: project status and open work (2026-10-20: Air-Way-first stage (OMi's rule); batch 17 shipped - the 2026-10-18 stage + 5 generator features; before: batch 16 2026-10-19)

This is the handover state from the Cowork sessions (2026-09-04 to 2026-09-25), updated after Claude's overnight
SolidWorks build of 2026-09-25 (details: `00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`) and after batch 14 (2026-10-02,
`03_SCRIPTS/RUN_ME_batch14.txt`). Read `CLAUDE.md` first, then `00_DOCS/NEXT_SESSION_PROMPT_2026-10-01.md`. This file is
the detail behind it. Keep it current: update it whenever a batch ships or a decision is made.

## 1. Where things stand

**2026-10-21 (cloud, group B, branch `claude/groupB-specs-20261021`): generator SPECs for the 168 group-B parts STAGED** (`tools\_out\groupB_20261021\README.md`; not shipped, no SolidWorks dry run yet). **127 of 168 generate** + 97 configurations of existing FS roots (FS2403 / FS2404 / FS6400 / FS6403 / FS6801-6804 / FS2701 / FS2702 / FS2704) unlocked by the 12 STEPs the user sent 2026-10-21 (new `FSM_MEAS` -04 ... -20, `NWO_FS` -06 ... -20) and group A's per-size tables (pasted at its request, identical values: + NWO_FS -04 / -24, FSBH_MEAS -04 / -10 / -16): 6900 22, 6901 19, 6805 12, 6806 10, 6809 7, 6815 6 / 6832 4 / 6835 4 (new female ORB port leg `leg_ORBPORT` + ORBMOUTH cut), 6801-L / -LL 12 folded into 6801, 4005 8 (into the 4000 ring master), FS2408 8, FS6402 7, FS6809 7, FS6801-L 1. Regeneration of every root old vs new: 224 new, 0 lost, changed only `$PRP@AxialSource` wording; vbacheck / dofcheck / allcfg / regress clean; OCP closed loops 0 off (FS straights 87 configurations, FS forged 56, ORB ports = the Brennan STEP ports). User 2026-10-21: decisions 1 / 2 ("do the recommended": 6900-05-04-O keeps W4 1.30, L2 = Brennan 1.09; 6805-08-06 N1 = Brennan 1.02) and 5 (6801-LL-08-08 = Brennan record) applied. Open: 6901-10-08 (which Brennan cells), 6901-08-12 (STEP measured, needs an elbow-generator change). Not built (41): 6901-10-08 / -08-12, FS17xx / 18xx / FS2700 / FS6400-L / FS7202 / 6425 / 3051 / 6316 (new end or body shapes), 4005-48 / 6806-12-08 (no data). Next (PC): `dryrun\calls_g1..g4.json`.

**2026-10-21 (cloud, evening): Brennan CAD cells STAGED** (`tools\_out\brennancad_20261021\README.md`; user "stage"). On top of the Air-Way-first stage: 421 verified Brennan CAD cells in 103 rows (`DimSource` BRENNAN), 40 rows MISSING -> ASSUMED -> **8 new configurations** (2408-14-SOLID, 2501-40-40-FG, 2501-LL-08-08-FG, 2706-32-32, 5000-24-20, 5405-16-24, 5406-40-32, 5503-02-02-FG; A9 tap drills applied: -24 1.72 / -32 2.20); 0 lost / changed; dofcheck / allcfg / vbacheck / regress clean. The 63 one-per-family Brennan STEPs arrived (`tools\_out\steps63_20261021`). Still blocking most staged rows: the -24 / -32 tap drill (A9 -> download BRENNAN_5405-24-24 / -32-32), adjustable-family end data, missing generator SPECs. Next: SolidWorks dry runs of the 4 roots.

**2026-10-21 (cloud, later): Brennan CAD portal lookup** (`tools\_out\partcommunity_20261021\README.md`; network: brennaninc.com + *.partcommunity.com allowed). Brennan has a CAD model for 693 of the 1,022 not-ready parts; of the 240 STEP downloads 217 exist, 23 do not (struck in `STEP_CHECKLIST.md`). The records = Brennan's CAD parameters (checked against BRENNAN_FS2403-08-08: bore / thread / hex / length match) - not applied; user decides whether to use them as Brennan values. OMi package rebuilt: 140 parts (compression 70 of 230). Downloads stay with the user (contact form + reCAPTCHA).

**2026-10-21 (cloud): not-ready parts sorted by source + OMi package drafted (not sent).** `tools\_out\sources_20261021\README.md`: the 1,022 not-ready parts (PC's 987 + 35 held) checked against Air-Way / Brennan catalogs + STEPs / OMi file; agrees with the PC's `blocked_needs_20261020\BLOCKED_NEEDS.md` except 6505-04-02 (OMi file prints it) and 11 download-list parts no catalog prints. `STEP_CHECKLIST.md` = the 240 Brennan files as exact names + arrival check. `10_DRAWINGS\for_OMi_2026-10-21\` = PDF + fill-in workbook + email to Triveni for the 290 parts no source prints (compression 230, test gauge 12, 34 single sizes, 4005, 0618 / 0619, FS0319-24) - user to review and send.

**2026-10-20 (later): AIR-WAY FIRST - STAGED (cloud session), not shipped.** Branch `claude/review-drawings-update-eflmmf` also carries the
merged ORFS / A14 branch (`claude/pensive-planck-t9i90d`); `claude/quirky-sagan-ajqv46` (cloud batch-17 rebase, 01:32) is superseded by the
batch-17 ship - do not merge it. OMi's rule (section 5): Air-Way over Brennan wherever Air-Way
prints a value, including the numbers of OMi's website file. Stage + evidence: `tools\_out\airway_first_20261020\` (README.md).
- **319 cells** in 26 review tables (235 rows) go back from the OMi-file value to Air-Way: Task A (2026-09-25), batch-15 OMi values, A19,
  the A19-style "7 pending", A20 (1404 nut faces), 2404-10-04 / -20-32 lengths (question 26). 261 checked against Air-Way's raw extract;
  58 (6401 / 6405 / 6408 / 6500, no raw extract in the repo) from the change logs - re-check on the Air-Way pages.
- Regenerated (live tools + one SPEC line): **233 configurations change in 25 roots, 0 lost**; control reproduces every shipped macro / SW2;
  dofcheck / allcfg / vbacheck clean; every change traced to a reverted cell (`checks\trace.txt`).
- **6410 reference configuration -> 6410-24-20-O** (`tools_af\generators\gen_straight2.py`, 1 line): with Air-Way's bore 0.68 the old
  reference 6410-12-08-O is a deep-bore port. Deploy with the ship.
- **Air-Way not buildable -> Brennan (user Q1 2026-10-20: "use brennans"; `brennan_cells.csv`, 4 cells):** 6405-24-16-O L31 1.75 (Air-Way L
  1.00 < pocket), 6504-24-24 D1 1.312 (Air-Way 1.38 >= tip 1.381), 6565-10-10 nut hexes 1.000 (Air-Way 0.94 vs the Brennan nut) - Brennan TFA
  catalog values = the values built now; rows marked `$PRP@DimSource` BRENNAN + `[BRENNAN-CELL 2026-10-20: <col>]`. 6405-24-16-O D3 follows
  the rule (Air-Way 1.14). Kept at OMi: 6504-06-08 bores (Air-Way garbled). Now 320 cells to Air-Way, 236 configurations, 26 roots (+6565).
- **Q2 (user 2026-10-20: option C):** check the look-at cells against the two review PDFs first, then send Triveni the rest. Drafted (not
  sent): `10_DRAWINGS\for_OMi_2026-10-20\` - `AirWay_values_to_confirm_2026-10-20.xlsx` (40 rows: AW / BI per row; column I "PDF check" is
  internal - fill it from the PDFs, delete the settled rows and the column) + `Email_to_Triveni_2026-10-20.txt`. None of these cells is on a
  configuration that was in the dimension-check drawings (one -08 size per series), so the PDFs will mostly tell the rule, not the cells.
  Batch 18 waits for the answer on these cells (or ships them as staged = Air-Way, if the user decides so).
- **Look at (43 cells, `checks\look_at.csv`):** 6405 bores where Air-Way's D equals the tap drill ("column bleed"), 6405 L31 values flagged
  suspect in 2026-09, 5502-20-20-FG / -24-24-FG N, 6410-12-08-O 1.48 -> 1.09 and other moves > 0.15 in.
- DataStatus unchanged (6500-08-06-FG back to VERIFIED: its logged OMi downgrade undone).
- **Next (PC):** read the two "Review of Drawings" PDFs (not in the repo) against the stage; SolidWorks dry runs of the 25 roots
  (ready: `tools\_out\airway_first_20261020\dryrun\RUN_DRYRUN.md` - 3 groups, memory check, verdict script); ship as
  batch 18 (macros + SW2 + review tables + `tools_af`). The dimension-check drawings of these roots go stale.

**2026-10-20 (PC, evening): ORFS SolidWorks dry runs - ALL 51 staged ORFS masters PASS** (50 FS masters + the O-ring master 4000 with
FS4000).
- **Run log:** `tools\_out\orfs_dryrun_20261020\RESUME.md`. Evidence: `VERDICT.txt`, `out_g*.txt`, the per-root reports and dry-run parts.
- **What was checked:** the CLAUDE.md verify loop, plus a thread check. Every configuration must give 1 body with THD_* off and on, and every
  thread must be live, error-free and removing material.
- **5 staging-generator fixes** (`orfs_gen_20261020\tools`; backups `orfs_dryrun_20261020\backup_20261020\`). Each was regenerated and
  diffed to the intended lines only, and the changed roots were re-run.
  1. FSSW -10 TE 0.484 -> 0.4993: where the measured 45deg relief meets the basic minor, as on every other size. The STEP's 0.484 sits on
     Brennan's undersized -10 minor.
  2. FS masters with a face-seal leg below the flats in one row and proud of them in another are built at a proud row. Affects FS2501,
     FS2503, FS6500C, FS6602C.
  3. No `FSW*_CSANG` table column. It was dead (the angle is held by its supplement) and stopped every insert with a modal "parameters not
     found" dialog.
  4. No-step face-seal threads are anchored at the nose circle; the hex-end circle is split by the flats. This fixed FS2601N, FS2603N and
     FS6600N.
  5. -10 swivel helix = the STEP's measured thread end 0.484 (HTE); the cavity keeps TE. A helix to TE touched the relief, and the swept
     cut failed in FS6602C.
- **Status:** nothing shipped. The live `tools\` and `04_DESIGN_TABLES` are untouched. The staged `out\` files = the tested ones.
- **Ship needs:**
  - the user's review;
  - the FS review tables moved into `04_DESIGN_TABLES`;
  - the staging generators merged into the live `tools\` (back up, regenerate all roots old / new, diff).
- **Noticed, not fixed:**
  - the swivel / nut helix curves (HELIX_n) are visible in the saved masters (display only);
  - SolidWorks shows the same modal dialog for ANY dead table column. That stopped the batches until `dialog_watch.ps1` answered it.

**2026-10-20: BATCH 17 SHIPPED (`03_SCRIPTS\RUN_ME_batch17.txt`, QA #173-#175; user: "can you ship batch 17?").** Evidence and scripts:
`tools\_out\batch17_20261019\` (RESUME.md = the run log, checks\, scripts\ship_b17.py, old_files\ + MANIFEST*.txt; second copy
`_to_delete\superseded_20261019b\batch17_replaced\`).
- **Content:** the 2026-10-18 stage (`brennan_yes_20261018\stage`: OMi answers, Brennan rows waves 1-3 marked `$PRP@DimSource` BRENNAN,
  A19-A23, the 37 wrongly-DROP adapters + wave-3 adapter rows - adapters77 went in HERE, `apply_77.py` was never run) + the five merged
  generator features (hose barb, flange legs, 45 deg angled legs, per-leg swivels, straights incl. 6400 generated per A6).
- **Rebased on live first:** stage review tables = live tables after batch 16 + logged batch-17 edits, 0 stale cells (`checks\cmp3_full.txt`);
  regenerated from live (control = live tools + live tables reproduces batch 16).
- **Generator fix (QA #174):** the angled macros did not compile (Atan2V got Variant elements ByRef) -> `ByVal`; changes exactly that line in
  the 6 angled macros. Live `tools\` = `batch17_20261019\tools_b17` (gen_tee.py, gen_straight2.py, allcfg_check.py, dofcheck_tee.py, npsm.py
  changed; 8 measure scripts added). Undo = `old_files\tools\`.
- **74 masters -> `11_MASTERS`** (24 new, 50 replaced) = the SolidWorks dry-run parts (sha256 `checks\shipped_files_sha256.txt`), 74 macros
  (LF) + reports -> `03_SCRIPTS`, 74 SW2 + 88 review tables -> `04_DESIGN_TABLES`. Dry runs: 0 FAIL (5406HHP / SHP: 1 accepted extent-check
  FAIL), 1 body each; old configurations identical to read-only sweeps of the replaced masters, or changed with their own table cells (92:
  A19 / A20 / A21 / A23). Post-ship: live tools + tables regenerate the shipped files (`checks\verify_b17.txt`, 0 BAD).
- **Held (QA #175):** 4503 / 4603 (hose face-off on the hose leg), 1703-24-24-FG (HEX2 direction), 1700RC / 1800 (FLATS sketch
  under-defined), 5404N (-06 threads again, QA #163; old master stays). Rows stay in the tables; generator work needed.
- **Shipped with an open user call in AxialSource:** 6902-12-12-NWO-FG composed shape, 5505-20-20-FG on the -08 shape.
- **Now: 1,354 of 1,874 BUILD rows in a master** (1,103 of 1,804 before), 95 masters in `11_MASTERS`, 440 MISSING, 336 VERIFIED, 79 with
  data and no master configuration (`batch17_20261019\paperwork\count_now.txt`). Coverage refreshed: A1 1,300 OMi part numbers.
- SolidWorks incidents during the dry runs (no effect on the shipped files): it closed at 21:28 (my VBA bisect loading ~40 test modules)
  and 23:16 (with ViewServerV6.exe); Excel crashed at 23:22 during a design-table insert and left an Excel window that broke every later
  insert - those dry runs were discarded and re-run after closing it.

**2026-10-20 (cloud): ORFS branch rebased on batch 17 (fb1d145)** - conflicts only in `.gitignore` / this file / CLAUDE.md (both sides kept);
the batch-17 generator fix (Atan2V ByVal, QA #174) ported into the staging gen_tee; `regress_all.py` now compares against the LIVE tools on the
LIVE tables: 99 / 99 roots identical, no FS macro changed. A14 (1603-08-08-08-FG, MISSING in the live table) is staged only - batch 17 did not
take it; it ships with the next batch. Count: **1,351 shipped + 197 waiting for SolidWorks = 1,548 of 2,535** (ORFS 133 configurations staged).

**2026-10-20 (cloud): ORFS step 7 - FS2404 / FS6403 / FS2601 / FS6502** (README step 7; staged): 12 configurations (FS2404 5 at -08 / -24, FS6403
-08-08, FS2601 5, FS6502-08-08); FS2404 / FS6403 other sizes need straight STEPs (FS2403-NN-NN), FS6502 -06 / -10 / -12 / -16 need
BRENNAN_FS6502-NN-NN-FG (corner-puck check), FS0304-C needs a shape STEP; checks clean, closed loops 0 off, regression 99 / 99;
count **1,549 of 2,535**.

**2026-10-20 (user decision): straight FS swivel body hex = Air-Way** ("yes keep airway"): where Air-Way prints the hex length (FS6540 L37,
FS6504 L39) the body hex is built to it; Brennan's swivel body face stays a note in `$COMMENT`. Then: "go on with" FS2404 / FS6403 / FS0304-C /
FS6502 / FS2601.

**2026-10-20 (cloud): ORFS step 6 - the straight face-seal swivels** (user "yes start on the straight swivels"; README step 6; staged):
- FS6565 / FS6540 / FS6504 / FS6505 + counterbored-mouth masters ...C: 20 configurations; length to the seal face (FS6565-08-08), nut hex per
  Q-FS-NUT; body hex built to Air-Way's printed hex length (FS6540 L37 / FS6504 L39) - 0.015 ... 0.09 shorter than the Brennan swivel: tell the user;
- static checks clean, OCP closed loop 482 checks 0 off, FS6565-08-08 seal -> seal = Brennan 2.12; regression 99 / 99;
- count: **1,537 of 2,535** ready after SolidWorks (ORFS 121 configurations).

**2026-10-20 (cloud): ORFS step 5 - 29 per-size Brennan STEPs (user upload)** (`tools\_out\orfs_gen_20261020\README.md` step 5; staged, not shipped):
- loose parts at every size (FS0306 / FS0318 -04 ... -24, FS0319 + coned-collar master FS0319C); forged male legs -04 ... -20 and swivels -04 ... -20
  from FS6500-NN; straights -24 (FS2403-24-24); one master per leg-shape variant (`<root>N / R / C`);
- Brennan's FS0306 / FS0318 -10 / -24 thread bores are smaller than the basic minor: modelled at the basic minor, noted per row (tell the user);
- FS6565-08-08: Air-Way's straight swivel lengths run to the stem seal face (L45 = Brennan seal to seal) - the straight swivel end is next;
- checks: all static checks clean, OCP closed loops 2,636 checks 0 off, regression 99 / 99;
- count: 1,106 shipped + 411 waiting for SolidWorks = **1,517 of 2,535** (was 1,443); ORFS 101 configurations.

**2026-10-20 (cloud): ORFS generator step 4 - loose -08 parts** (`tools\_out\orfs_gen_20261020\README.md` step 4; staged, not shipped):
- FS4000-04 ... -24 face-seal O-rings folded into the O-ring master 4000 (staging `gen_ring.py` -> `out/ring/`, 29 configurations, the 21
  old rows cell-identical); FS0306-08 locknut, FS0318-08 tube nut, FS0319-08 braze sleeve in the staging `gen_straight2.py` (`out/`);
- vbacheck 4 / 4, dofcheck 3 / 3, allcfg 0, regression 99 / 99; OCP closed loop 59 checks, 0 off, against the rows and the Brennan pilots;
- other FS0306 / FS0318 / FS0319 sizes need their own Brennan STEP; FS0319-24 held (D5);
- count (`tools/_out/count_20261020/count_ready.py`): 1,106 shipped + 337 waiting for SolidWorks = 1,443 of 2,535 (was 1,432); 1,092 not yet.

**2026-10-20 (cloud): ORFS generator step 3 - forged face-seal swivel leg** (FS6500 / FS6600 / FS6602 -08 build):
- leg length = Air-Way L21 to the seal face, nut face +0.433;
- regression 99 / 99; dofcheck 37 / 37 legs; OCP closed loop 589 + 122 checks, 0 off;
- ORFS: 24 configurations in 17 staged masters;
- count: 1,432 of 2,535 ready after SolidWorks (1,106 shipped + 326 waiting).

**2026-10-20 (cloud): ORFS generator step 2 - forged legs** (`tools\_out\orfs_gen_20261020\README.md`):
- gen_tee: face-seal leg, bulkhead leg, FS adjustable stud; 12 forged FS SPECs -> 16 configurations (+5 straights = 21 FS configurations);
- regression 99 / 99 identical; dofcheck 29 / 29 legs; OCP closed loop 484 checks, 0 off;
- 3 FS2501 / FS2503 rows held: their flats are above the thread (needs the family pilot).
**Count** (`tools\_out\count_20261020\count_ready.py`): of the 2,535 OMi parts:
- 1,106 are in a shipped master;
- 323 more are generated and wait only for the SolidWorks dry runs + ship (batch 17 + 21 ORFS + 21 O-rings);
- = 1,429 ready after SolidWorks; 1,106 still need data, STEPs, decisions or OMi.

**2026-10-20 (cloud): ORFS generator step 1 staged** (`tools\_out\orfs_gen_20261020\README.md`; toolset = merged batch-17 + ORFS):
- male face-seal end `end_FSM` + ORB stud `end_ORBFS`; SPECs FS2403 / FS6400 (5 configurations: FS2403-08-08, FS6400-08-06/-08/-10/-12-O;
  the rest wait for per-dash STEPs);
- regression 99 / 99 existing roots identical; dofcheck / allcfg / vbacheck clean; OCP closed loop 122 checks, 0 off;
- SolidWorks dry run of FS2403 / FS6400 next (PC);
- straight swivels blocked on BRENNAN_FS6540-08-08-O or FS6565-08-08 (seal face vs nut face);
- found: SPEC 6400 (batch-17 tools) labels End A's ORB thread from the wrong dash on unequal-dash rows (text only).

**2026-10-20 (cloud): ORFS WP2 extractors written and validated on the 8 pilots** (`tools\_out\orfs_wp2_20261020\README.md`;
46 checks, 0 FAIL; -08 end entries proposed in `end_lib_08.json`). The male face-seal end is one shape on all 7 copies. The swivel nut
and FS0318 agree on hex / length / thread / lip. The fused O-ring = FS4000-08. Air-Way rows match the STEPs. Plan changes:
- Air-Way L21 = crossing -> swivel SEAL face (nut face +0.433), not the nut face;
- i4 = a 0.06 step, the bulkhead collar is 0.20 thick;
- the FS studs = library undercut + a longer thread.
Next: generator end functions + OCP closed loop; E1-E8 / F1-F15 can be downloaded now.

**2026-10-20 (cloud): 8 of the 9 ORFS pilot STEPs received** (user download, Brennan PARTcommunity) -> `09_STEP_FILES/BRENNAN_FS*.stp`:
FS2403-08-08, FS6500-08-08-FG, FS2701-08-08-FG, FS6400-08-08-O, FS6801-08-08-NWO-FG, FS0318-08, FS0319-08, FS0306-08 (each 1 solid;
sizes match Air-Way). **FS2406-08-06 has no CAD file at Brennan** -> stand-in FS2406-08-04 proposed. Extractors / ORFS generator not
started. `tools\_out\orfs_pilots_20261020\README.md`.

**2026-10-20 (cloud): batch-17 work rebased on batch 16 (d63e1a6) and the 24 batch-16 roots regenerated from the new state**
(`tools\_out\rebase_b16_20261020\README.md`):
- live tools + shipped tables reproduce the shipped macros / SW2 24 / 24;
- the merged batch-17 tools change nothing on them;
- the 12 shipped review tables = their batch-17 stage copies minus logged batch-17 changes (0 unexplained);
- batch-17 data: 372 -> 417 configurations (+45); 32 built configurations change geometry, all from A19 (rebuild in batch 17);
- vbacheck / dofcheck / allcfg clean.

**2026-10-20 (cloud): A14 done for 1603-08-08-08-FG** - both bores measured on `BRENNAN_1603-08-08-08-FG.stp` = 0.450 (catalog prints
"0.44/0.46"); the whole row staged in `tools\_out\brennan_yes_20261018\stage` (15 prepared Brennan-catalog / end-library cells + the 2
bores, DimSource BRENNAN, MISSING -> ASSUMED; every catalog value confirmed on the STEP). 1603 now generates 6 of 6 -FG rows with the
merged tools; old 5 unchanged; vbacheck / dofcheck / allcfg / OCP closed loop pass. Not shipped, not dry-run in SolidWorks.
Evidence: `tools\_out\a14_1603bore_20261020\README.md`. A14's 7 6901 / 6902 rows still wait for their STEPs.

**2026-10-19: BATCH 16 SHIPPED (`03_SCRIPTS\RUN_ME_batch16.txt`, QA #170-#172; user: "Yes, ship batch 16 as planned.").** Plan +
evidence: `tools\_out\ship_20261019\` (SHIP_PLAN.md, checks\, scripts\ship_b16.py, old_files\ + MANIFEST*.txt; second copy
`_to_delete\superseded_20261019\batch16_replaced\`).
- **25 masters -> `11_MASTERS`** (the SolidWorks dry-run parts, copied unchanged - sha256): NEW 0304 (JIC cap nut, 12) 0306 (bulkhead
  locknut, 11) 1502 (1) 2504 (4) 2505 (1) 2606 (5) 2609 (1) 2611 (2) and 2404 (57, generated: two bores, 2404-L folded, replaces the
  hand-built master); more sizes 6500 15 -> 24 (4 OMi leftovers + 6500-L x5), 6501 11 -> 14, 6505 18 -> 19, 5405 rebuilt (its 3 unbuilt
  configurations now in the file); the corner-puck fix re-ships 2501 2503 2701 2702 5500 5502 5504 6502 6503 1501 6801 6802 (+ 6500 /
  6501 / 2504). 24 macros (LF) + 25 reports -> `03_SCRIPTS`, 24 SW2 + 12 review tables (0304 0306 1502 2504 2505 2606 2609 2611 6500
  6500L 6501 6505) -> `04_DESIGN_TABLES`. All new rows ASSUMED.
- **Toolchain:** `tools\_out\puckfix_20261009\tools_new` deployed to the live `tools\` (wave-1 merged generators + 2404 + polish +
  `PUCK_INSET`; gen_tee.py, gen_straight2.py, checks\allcfg_check.py, checks\dofcheck_straight.py, measure\npsm.py, measure\prof.py
  changed, 17 measure scripts added). Undo = the files in `ship_20261019\old_files\tools\`.
- **Corner-puck defect (QA #171):** the elbow corner puck sat exactly on the hex corner radius and SolidWorks silently dropped it in
  20 configurations (16 shipped + 4 staged; list in RUN_ME). Now 0.0005 in inside (`PUCK_INSET`): all 20 have their corner, every
  other configuration of the 17 elbow roots changes by that sliver only (dV / AF^2 = -0.000340 on 90 deg elbows). The 2026-10-09
  dimension-check drawings predate the fix (dimensions unchanged).
- **Checks** (`ship_20261019\checks`): every root regenerated from the staged tables with the staged tools - the 24 changed roots
  identical to the macros that were dry-run (cmp_ship_out.txt); dry runs 0 FAIL, 1 body each
  (`puckfix_20261009\DRYRUN_VERDICT_2026-10-19.txt`, `wave1_ship_20261009\swtest\cmp_out.txt`); old configurations identical or
  changed by the puck inset only; after shipping the live tools + tables regenerate the shipped files exactly (verify_b16.txt, 0 BAD).
- **Not re-shipped on purpose (QA #172):** 2505-08-08 / -16-16-FG and 1502-04-04-FG blocked; 0318 5406 2650 2605 5600 regenerate
  with a cosmetic `$COMMENT` change only; 22 roots keep their pre-2026-09-25 macros (5000 5404 2408 0318 5406 5406C 5406P 2700 4404
  4604 5404N 2406 1405 1700 2650 2602 2605 5600 5602 2704 6600 6602 - dry-run before re-shipping any).
- **Now: 1,103 of 1,804 configurations in a master** (1,053 in `11_MASTERS` + 50 in the hand-built 6400); 619 BUILD rows MISSING,
  82 with data but no master configuration; **71 masters in `11_MASTERS`**; 19 topologies fully modelled
  (`ship_20261019\paperwork\count_now.txt`). Coverage refreshed: A1 1,050, A2 50 (6400), D 105, E 1, F1 208, F2 236, F3 138, F4 11,
  F5 2, X 30.
- SolidWorks: the 2026-10-09 dry-run session stopped when SolidWorks closed; on 2026-10-18 it kept closing with "License not granted:
  X1W ... (License error 20)" = the desktop app had lost its 3DEXPERIENCE sign-in since 2026-10-15 (SWXDesktopHelper logs: the role
  query answered by the login page). The user signed in again on 2026-10-19; the 9 remaining roots were dry-run then.
- **Next:** the 37 wrongly-DROP adapters (`tools\_out\adapters77_20261016`, `apply_77.py --apply`, needs the user's OK), then batch 17
  (Brennan / OMi-answer rows staged by another session on top of this state).

**2026-10-18 (later): OMi's answers staged** - 15 more rows have dimensions (`tools\_out\omi_answers_20261018\README.md`,
section 5). Not in the count below.

**2026-10-18: the whole catalog counted** (all 2,535 OMi carbon-steel parts listed since 2026-10-16;
`tools\_out\adapters77_20261016\scripts\possible_2535.py` -> `possible_2535.json`, the 2026-10-08 unblock gates re-judged with the
decisions since). Built 1,041. Possible under today's rules 1,672: built + 414 with dimensions (145 my work only: staged / to
generate, incl. the 37 wrongly-DROP adapters and the 21 O-rings; 269 ORFS waiting on the ORFS model type) + 75 needing only your
STEP downloads + 142 needing your decisions (accepting the recommendations). Only with Brennan data as a source (Q-BRENNAN-ONLY is
NO): 517 printed in Brennan's catalogs + 53 only in a Brennan 3D file -> 2,242 in theory. No source at all (OMi's data needed):
266 - compression 230, test gauge 12, 4005 9, flareless 3, 6 adapters, 6 ORFS. Kits (out of scope) 30.

**2026-10-08: BATCH 15 SHIPPED (`03_SCRIPTS\RUN_ME_batch15.txt`, QA #167-#169; user: "ship batch").** 52 new configurations in 18
existing masters: 1501 2501 2503 2601 2701 2706 5500 5604 5605 6401 6500 6501 6502 6504 6505 6506 6801 6802 (272 -> 324
configurations). 47 rows from the OMi dimension file (the Brennan catalog only paired OMi's leg columns), 5 forged rows from their own
Brennan STEPs; all ASSUMED. The parts are the 2026-10-02 SolidWorks dry-run builds from `11_MASTERS_NEW`, moved unchanged (sha256);
macros (LF) + reports -> `03_SCRIPTS`, SW2 + 19 review tables (incl. `DesignTable_2501L.xlsx`) -> `04_DESIGN_TABLES`. Checks
(`tools\_out\ship_20261008\checks\`): regenerating the 18 roots from the staged tables with the live tools reproduces the staged
macros + SW2 (date line aside); regress 0 changed old cells; dry runs 0 FAIL, 1 body each; old configurations = the accepted masters
266 / 266 (257 vs the sweeps recorded at their builds, 9 of 2601 vs a read-only sweep 2026-10-08). **5604 / 5605:** the replaced
user-built parts predated the QA #144 round collar; the shipped ones carry it (old configurations -1.8 to -5.8 % volume, sizes
unchanged - QA #168). 2602 / 5602 still have their 2026-09-24 builds. Old files: `_to_delete\superseded_20261008\batch15_replaced\`
+ `tools\_out\ship_20261008\old_files\` (MANIFEST*.txt). 25 rows held MISSING (QA #169; 24 build with Q-BRENNAN-ONLY = yes).
**Now: 1,044 of 1,804 configurations in a master** (943 in `11_MASTERS` + 3 unbuilt 5405 + 98 hand-built 2404 / 6400); 672 BUILD
rows MISSING, 88 with data but no master configuration; 62 masters in `11_MASTERS`; 16 topologies fully modelled. Coverage
refreshed (A1 943, A2 98, D 111, E 1, F1 232, F2 266, F3 138, F4 11, F5 1, X 30). `11_MASTERS_NEW` is empty again (README,
screenshots, fixed_macros). **Wave-1 FOLDS (2501-LL) staged its own `DesignTable_2501.xlsx` before batch 15: rebase it on the
shipped table before it ships.**

**2026-10-02: BATCH 14 BUILT AND SHIPPED (`03_SCRIPTS\RUN_ME_batch14.txt`, QA #159-#164; user: "yes to all").** 22 roots:
- **7 real SolidWorks builds** (2026 SP4, through the MCP, deployed tier-1 toolchain): 6502 6802 6565 6404 6410 2403 2405.
  Each: "finished with 0 problem(s)", report 0 FAIL lines, saved to `11_MASTERS`, every configuration one body and identical
  (volume + size) to its 2026-10-02 dry run (`tools\_out\ship_20261002\build_out\<root>.txt`, `ship_log.txt`).
- **15 Task A masters** (OMi values, built as dry runs on 2026-09-25 night) moved `11_MASTERS_NEW` -> `11_MASTERS` unchanged
  (sha256), reports -> `03_SCRIPTS`: 0403 1404 2705 2706 6401 6402 6405 6408 6504 6505 2501 2503 5500 5502 6500. The staged
  6404 / 6410 / 6565 were superseded by the tier-1 builds (to `_to_delete`).
- Configurations of the 22 roots: 429 -> 425. +15 new: 6502-05-05-FG / -12-12-FG, 6802-20-16 / -20-20 / -24-24-NWO-FG,
  6565-10-10 / -20-20 / -24-24, 6410-20-12-O / -20-16-O / -24-16-O, 6401-32-32-O, 6405-24-16-O, 6504-24-24, 2501-32-32-FG.
  -19: the DROP configurations of 2403 (15) and 2405 (4), Q-SPECS-1. Task A changed 138 configurations on purpose
  (`tools\_out\omi_apply_20260925\TaskA_result.md`); 6410-12-08-O is now OMi 1.480.
- **Toolchain:** the tier-1 generator fixes are DEPLOYED in the live `tools/` (10 files; NOT the 5404N-06 fix). Record and
  undo: `tools\_out\ship_20261002\PREP.md`, `deploy.diff`, backup `tools_before\`. What each fix does:
  `00_DOCS\Tier1_Fixes_2026-10-01.md`. **Since 2026-10-02 12:21 the live `gen_tee.py` also carries the batch-14b change**
  (`bh_short`, 2702 / 2703 only - below): it no longer matches `ship_20261002\live_tools_after_sha256.txt` (the batch-14
  state), reversing `deploy.diff` fails 1 gen_tee.py hunk, and `tools_before\` would drop 14b too. To undo batch 14's tools:
  undo 14b first (`gen_tee.py` from `tools\_out\ship_20261002b\old_files\tools\generators\` = the batch-14 deploy,
  sha256 646d9da2...), then `deploy.diff` reverses cleanly (tested: `ship_20261002\paperwork\fix\undo_test.txt`).
- Plan, expected values per configuration, file inventory: `tools\_out\ship_20261002\BUILD_PLAN.md`. The paperwork (RUN_ME,
  QA_Log, Topologies, coverage, this file, CLAUDE.md) with sha256 before / after: `tools\_out\ship_20261002\PAPERWORK.md`.
  Old files: `_to_delete\superseded_20261002\batch14_replaced\` AND `tools\_out\ship_20261002\old_files\` (MANIFEST.txt and
  MANIFEST_paperwork.txt in both; the user empties `_to_delete`).
- **Not in batch 14:** 2404 / 2404-L (held until OMi clarifies the bores), 5404N-06 (failed in SolidWorks), 2702 / 2703
  (batch 14b), the 3 unbuilt 5405 configurations.

**`11_MASTERS` holds 60 masters** (batch 14 replaced 22 and added no new name); 2404 / 6400 are hand-built (files not in
the repo), 2702 / 2703 are held back (`tools\_out\overnight\`). `11_MASTERS_NEW` keeps only `screenshots\`, `fixed_macros\`,
an empty `reports\` and its README. **`03_SCRIPTS` rebuilds exactly what is in `11_MASTERS`** for the 22 batch-14 roots and
6801 6803 6804.

**Configurations (BUILD rows) of the 126 topologies, counted 2026-10-02 after batch 14**
(`tools\_out\ship_20261002\paperwork\count_configs.py`; on the pre-batch-14 SW2 tables it reproduces the 2026-09-25 numbers
exactly): 1,804 in all. **990 are in a master** (was 976): 868 in `11_MASTERS` with the current configuration set (was 853),
3 in the current 5405 macro but not yet in its built file (5405-12-08 / -16-08 / -16-12 - re-run Build_5405), 98 in the
hand-built 2404 / 6400, 21 in the held-back 2702 / 2703 (990 configurations = 987 OMi part numbers; 2408-04 / -06 / -20 are
built SOLID and -H). 88 have dimensions but no master configuration (was 101): 12 blocked in roots that have a master
(1501-04-02-FG / -24-24-FG, 2406-16-04, 2702-12-12-FG-LN, 6405-32-24-O, 6802-04-06-NWO-FG and 6 2404 rows), 76 in tables
without a master. 726 are DataStatus MISSING (727 until Task A made 2501-32-32-FG ASSUMED). Topologies: 116 of the 126 have
BUILD rows, 61 have a master, 10 are fully modelled (0318 0403 1404 2605 2650 2704 4404 4604 6402 6602) - unchanged.
**Coverage by OMi part number** refreshed 2026-10-02 (`00_DOCS/OMi_Coverage_2026-09-24.xlsx`, in place): A1 built 868 (was
854; the 14 new: 2501-32-32-FG, 6405-24-16-O, 6410-20-12-O / -20-16-O / -24-16-O, 6502-05-05-FG / -12-12-FG, 6504-24-24,
6565-10-10 / -20-20 / -24-24, 6802-20-16 / -20-20 / -24-24-NWO-FG), A2 98, B 21 (2702 / 2703), D 111, E 1, F 702, X 30 (A1
counts the 3 unbuilt 5405 configurations as built: the tool reads the SW2 tables).

**Masters in `11_MASTERS` by builder (60):**
- built by the user (18): 2500HX 2502HX 2601 2602 2603HX 2605 2650 5000 5404 5405 5406 5406C 5406P 5504 5600 5602 5604 5605
  (0318 0403 6405 6408 were replaced on 2026-09-25, 2403 2405 5502 6401 by batch 14);
- built by Claude through the SolidWorks MCP for batch 14 (22, 2026-10-02): real builds 6502 6802 6565 6404 6410 2403 2405;
  Task A dry-run builds of 2026-09-25 night 0403 1404 2705 2706 6401 6402 6405 6408 6504 6505 2501 2503 5500 5502 6500;
- built by Claude overnight on 2026-09-25, accepted that evening and unchanged since (20): 0318 1405 1501 1700 2406 2408 2700
  2701 2704 4404 4604 5404N 6501 6503 6506 6600 6602 6801 6803 6804.
Overnight-build reports (`00_DOCS/OVERNIGHT_BUILD_2026-09-25.md`): 16 carried FAIL lines, all explained ([A] leftover angle
dimension, [C] Default-configuration HELIXDIA, [D] extent-check bug, [E] 5404N threads-live box); the 22 batch-14 reports
have none.

**2702, 2703: BATCH 14b BUILT AND SHIPPED 2026-10-02** (`03_SCRIPTS\RUN_ME_batch14b.txt`, QA #165-#166): 2702 11 + 2703 12
configurations, 0 FAIL, identical to the dry runs (`tools\_out\ship_20261002b\build_out\`), now in `11_MASTERS`; new rows
2702-20-20-FG (own Brennan STEP) and 2703-08-08-08-FG-LN. **Configurations in a master: 992.** History of the fix below.
(Was: held back, builds in `tools\_out\overnight\`.) At -16 (-FG and -LN) the bulkhead-leg hex arm does not
rebuild: it ends exactly on the collar face and the collar radius lies between the hex flats and corners. User 2026-10-02:
OK to stop the arm 0.001 in short of the collar. The fix (`gen_tee.py`, SPEC key `bh_short`) was prepared in
`tools\_out\fix2702_20261002\` (SolidWorks dry runs of 2702 / 2703: 0 problems, `sw_dryrun2_2702_out.txt` / `_2703_out.txt`)
and **deployed 2026-10-02 12:21 by the batch-14b prep** (`tools\_out\ship_20261002b\PREP.md`): the live `gen_tee.py` and the
review tables `04_DESIGN_TABLES\DesignTable_2702.xlsx` / `2703.xlsx` are the 14b versions (old ones in
`_to_delete\superseded_20261002\batch14b_replaced\` and `ship_20261002b\old_files\`); regenerating every root changes only
2702 / 2703. Built and shipped the same afternoon (above).

**Macros.** The `03_SCRIPTS` macros of the 22 batch-14 roots and of 6801 / 6803 / 6804 carry the overnight generator fixes;
the 22 also carry the tier-1 fixes where they apply. Still broken: Build_2702 / 2703 at -16 (batch 14b). The other
accepted masters were built from older `03_SCRIPTS` macros (from before the 2026-09-25 fixes; harmless while their angle
columns stay constant - section 6). Before re-shipping any of them: regenerate with the deployed tools into a new
`GS_OUT` / `GT_OUT` folder, check, and dry-run (`tools\_out\regen_20260925` holds the 2026-09-25 regeneration).
`11_MASTERS_NEW\fixed_macros` keeps the macros that built 6404 / 6504 / 6565 on 2026-09-25 (history).

**Proven in SolidWorks on 2026-09-25:** the swivel-nut hex cut (`NutHexCutAx`), `ZoneHexCut` (straights), the 45 deg leg
helpers and the adjustable-ORB module, at every size. The NUTCUT revolve radius still equals the hex corner radius
exactly; if a new swivel size ever fails there, add a margin as `NWO_RN_MARGIN` does. The 6500 swivel section through
the nut flats lies within 0.003 in of the Brennan STEPs over nut hex, skirt and neck (nose tip ~0.01, per Air-Way).
**Proven on 2026-10-02 (SP4):** the first revolve cuts of the library (6502 NECKTRIM1 / NECKFILL1 in every size; 6802
ORBTRIM on a TEST row), the 6565 seat cones ending at the bore, the female ORB deep-bore port (ORBFB_DRILLANG 60 / 90,
flip-tested), the generated 2403 / 2405 (same volume as the user-built parts). SolidWorks is 2026 SP4 since 2026-10-01;
the control rebuilds showed SP4 = SP3 for these macros.

Each `RUN_ME_batch*.txt` in `03_SCRIPTS` says what a batch contains and what to look for in the reports.

## 2. Batch 13b: built, checked, ACCEPTED into 11_MASTERS and SHIPPED (2026-09-25, RUN_ME_batch13b.txt, QA #156)

Shipped from `tools/_out/regen_20260925/tee` (macros + SW2); all five dry-run in SolidWorks from that set on 2026-09-25
with every configuration identical (volume + size) to the accepted parts. To regenerate: set `GT_OUT` to a new folder first,
then `python tools/generators/gen_tee.py 2501 6801 6802 6803 6804` (never into `tools/_out/tee`, the overnight build inputs).

| Root | Configs | Status |
|---|---|---|
| 2501 | 32 | Folds in the 2501-L rows (user decision 2026-09-25). Brennan 2501-L-06-04-FG STEP: the forged NPTF hex arm simply runs to N3. Built clean in SolidWorks. Ready to release. |
| 6801 | 33 | New adjustable ORB module ("NWO": neck, locknut with 15 deg chamfers, backup washer, O-ring undercut, ORB thread). Static checks pass (sketches fully defined, clean outline for every configuration, static VBA check). OCP: every configuration rebuilt, one solid each, nut cut volume = the analytic integral; `measure/nwo_closedloop.py` on the OCP rebuild of 6801-08-08 / -04-02 / -32-32 returns the Brennan values. SolidWorks: built clean (all 33 configurations); its STEP exports measured with the NWO extractor equal Brennan at 9 sizes except the two Air-Way findings below and the cosmetic NWO_CH_DR (+0.0025 on the nut chamfer start). Ready to release. |
| 6802 | 16 (+4 blocked) | 45 deg elbow, ORB leg along +X. Static checks pass; built clean in SolidWorks; no OCP / Brennan geometry check. 6802-04-06 is blocked by Air-Way data (nut hex 0.56 for a -06 ORB, which needs 0.6875). 6802-20-16, -20-20 and -24-24 are blocked by a check that is too conservative: for e45 it counts the angled JIC leg's thread radius. Fix the check, don't change the geometry. |
| 6803 | 5 | Branch tee, ORB branch. Static checks pass; built clean in SolidWorks. ASSUMPTION: Air-Way prints no I3 for 6803, so the 6801 ORB_I3 of the same ORB size is used (equal to Brennan). Ask for a Brennan 6803-08-08-08-NWO-FG STEP. |
| 6804 | 8 | Run tee, ORB on the run (leg 2, -X). Static checks pass; built clean in SolidWorks. Same I3 assumption. Ask for Brennan 6804-08-08-08-NWO-FG. |

**13b shipping: done 2026-09-25** (RUN_ME_batch13b.txt, QA_Log #153-#158, Topologies notes, coverage refresh).

**6801 findings to report to OMi:**
- 6801-04-02: Air-Way LEG_ORB is 1.03, Brennan is 0.92.
- 6801-12-12: Air-Way ORB_THDL is 0.469, Brennan is 0.410.
- Both are built to Air-Way and noted in `$COMMENT` (BRENNAN_NOTES in gen_tee.py).
- Every other matched size agrees with Air-Way on leg lengths, I3, thread length, nut hex, body hex and undercut.

**Open question for the user: 6801-05-05.** It is MISSING in the review table ("CONFLICT vs MS51527"). Brennan
6801-05-05-NWO-FG matches Air-Way on every dimension. Ask whether to build it to Air-Way + Brennan. Don't decide alone.

**Brennan detail not modelled on any elbow:** the bores meet in a sphere of the bore radius at the crossing. Our bores
stop flat at the crossing. At -32 this is 0.75 in^3.

**Since batch 14 (2026-10-02):** 6802 has 19 configurations (the too-strict 45 deg check is fixed: tier-1 6802-E45, -20-16 /
-20-20 / -24-24 built) and 2501 has 33 (+2501-32-32-FG, Task A).

## 3. Open work (priority order)

0. **2026-10-14: NEW SCOPE - O-rings, bent-tube elbows, flareless nut + sleeve (OMi said yes, s5).** Write-up:
   `00_DOCS\Scope_ORings_BentTube_Flareless_2026-10-14.md`. 101 website part numbers (30 O-rings 4000 / 4001 / 4005, 68 bent tube
   1703 / 1704 / 1803 / 1804 -Tube + 6701, 3 flareless 0618 / 0619) + 13 only in OMi's parts file; all MISSING - OMi's file has no
   sizes, Air-Way no page, Brennan values not usable. Size request for OMi DRAFTED, not sent: `10_DRAWINGS\for_OMi_2026-10-14\`
   (`build_request.py` + `scope_parts.csv` in `tools\_out\omi_request_20261014\`). Needs: Q-NEW-ORINGSRC (AS568 table once OMi
   confirms each size number?), 5 Brennan shape files (1704-16-16, 1803-16-16, 6701-08-08, V0318-08, V0319-08), optional 0319.
   New model types to build (none exists): O-ring, sleeve, flareless nut (0318 SPEC), bent-tube generator (3 masters), drawing recipes.
   **2026-10-14 (later), staged in `tools\_out\newtypes_20261014\` (README.md):** new generator `gen_ring.py` (not in live tools).
   O-ring master `4000` = 4000 + 4001, 21 configurations from Air-Way s218 (ASSUMED), SolidWorks dry run 0 FAIL, sizes checked per
   configuration and by geometry. Sleeve type proven on a TEST table (0319T, 3 rows: 0 FAIL). Request for OMi updated (no O-ring
   sizes asked for 4000 / 4001; 1704-12-12 / -16-20 / -24-20 / -24-24-Tube prefilled from Air-Way 1701-61). Next: O-ring drawing
   recipe, bent-tube generator (needs bend radius / tube size: OMi, or Air-Way's 3D models of the four 1701-61 sizes).
   **2026-10-15 (user: "keep building all of them", "just do the solidworks models"):** O-ring master now splits its face along the
   silhouettes (real I.D. / O.D. / W edges, dry run 0 FAIL / 66 OK). New generator `gen_bent.py` (staged): bent-tube masters 1704T
   (90 deg MJ x flange: 1704 + 1804 -Tube), 1703T (45 deg: 1703 + 1803 -Tube), 6701 (90 deg MJ x FJS swivel) - SolidWorks dry runs on
   TEST rows 0 FAIL (94 / 94 / 121 OK); with Air-Way s115 values the solid's box equals Air-Way M3 / N4. Open: code 62 heads (not in the
   end library), the 6701 female thread, and every bent-tube size (OMi). 0618 / 0619 reuse the 0318 nut / sleeve types - wait for OMi
   sizes + V0318 / V0319 shape files. Drawings paused (user).
   **2026-10-15 (later; user: "do the 6701 nut thread and the code 62 flange heads next"):** 6701 female nut thread THD_EndB modelled
   (helix on the nut-face plane + 60 deg profile + swept cut = the straights' swivel thread about the vertical leg; SolidWorks' Thread
   feature on that edge crashed SolidWorks, so it is not used): dry run 0 FAIL / 147 OK, every configuration rebuilt with the threads on.
   All bent-tube macros now rebuild every configuration with its threads on (1704T 101 OK, 1703T 98 OK, 0 FAIL). Code 62 heads: -08
   builds (1804-08-08-Tube TEST row); -12 / -16 / -20 / -24 / -32 (28 of the 29 1803 / 1804 -Tube parts) BLOCK until a Brennan STEP with
   a code 62 head of that size exists (e.g. BRENNAN_1824-12 ... -32; user download; only the three -08 STEPs are in 09_STEP_FILES).
   **2026-10-15 (evening): the ~704 parts never in our part list.** OMi's site shows 2,535 carbon-steel parts; our list
   (`omi_skus_all.txt`) has 1,831 - ORFS (385), compression (230) and test gauge (12) were never fetched, ~77 adapters dropped. User:
   **"use airway dimensions, check brennan too"**. Staged in `tools\_out\orfs_airway_20261015\` (README.md), summary
   `00_DOCS\ORFS_Compression_TestGauge_2026-10-15.md` + `.xlsx`: 51 Air-Way ORFS series double-pass (673 rows, identical); every OMi FS
   part of OMi's parts file (499) checked against the Brennan ORFS catalog: plain parts 106 VERIFIED, 59 ASSUMED (15 Air-Way only +
   44 built to Air-Way where Brennan differs, s6 convention, Brennan value in `$COMMENT`; 21 of them by > 0.02 in), 70 MISSING (no
   Air-Way row); forged parts (user decision s5, 2026-10-15) 123 VERIFIED (Air-Way plain = Brennan forged on every cell: the 121 shown
   + FS6801-L-06-06 / -08-08 after a pairing fix), 141 MISSING. Total 229 VERIFIED + 59 ASSUMED = 288 with dimensions.
   **2026-10-16:** OMi's website ORFS collection read (two passes agree, 385 = the published count; `07_RAW_EXTRACTS\omi_feed\omi_skus_orfs.txt`): the 114 FS
   rows of the parts file not on the website -> DROP. Fixes from the model-type plan (PLAN.md s8): FS0319-24 held (Air-Way
   contradicts itself), FS6504 capped at ASSUMED (length only compared), 16 Air-Way thread slips (THDMAJ empty, noted). **On the
   website: 269 of 385 ORFS parts have dimensions (216 VERIFIED = 99 plain + 117 forged, 53 ASSUMED), 116 MISSING.** ORFS model-type
   plan: `tools\_out\orfs_modeltype_20261016\PLAN.md` + `STEPS_NEEDED.txt` (31 new FS masters + FS4000 fold, 32 Brennan STEPs, 9
   pilots first; questions Q-FS-MASTER / -ORBSTUD / -2NDSHAPE / -NUT / FS2406-NUT / FS2408-HOLE, S1-S3 open for the user).
   **2026-10-16 (later): the 77 dropped tube fittings** (all four website lists now in `07_RAW_EXTRACTS\omi_feed\`, two passes agree;
   listing report `tools\_out\omi_enum_20261015\REPORT.md`): 37 are Air-Way rows of existing review tables wrongly marked DROP (the
   crawl had dropped the SKU). STAGED in `tools\_out\adapters77_20261016\` (REPORT_77.md, CHANGES.csv 136 lines, `apply_77.py` dry run
   0 guard failures): DROP -> BUILD, 9 take OMi values (Task A form), Brennan TFA check -> 21 VERIFIED / 14 ASSUMED / 2 special. Apply
   at ship time - after batch 16 (it carries its own 2501 / 6500 / 6505 tables). 40 have no Air-Way row (Brennan prints 34, OMi has
   partial values for 9): not tabled yet.
   51 staged review tables `DesignTable_FS*.xlsx` (scope: the ORFS website list; the listing session
   `tools\_out\omi_enum_20261015\` hit OMi's store rate limit). Compression and test gauge: no Air-Way source (Brennan only V0318 /
   V0319) -> MISSING. Needed before models: an ORFS end type (male face
   seal + O-ring groove, female face-seal swivel nut) - FS series need their own masters (a different end sketch than JIC).
   **2026-10-09 (later): staged** - **SHIPPED 2026-10-19 as batch 16 (section 1)**; the items below are the staging history.
   - **2404 (Q-2404-BORE answered, s5):** LIVE `04_DESIGN_TABLES\DesignTable_2404_FINAL.xlsx` edited (29 rows: two bores from OMi, 2404-24-20
     from Air-Way, step at the hex mid-plane, the 4 "CB depth unsourced" rows released, 2404-40-32's Brennan depth dropped, question-26
     lengths 2404-10-04 1.69 / 2404-20-32 2.74) and LIVE `tools\generators\gen_straight2.py` (2404-L two bores, texts). Old files:
     `tools\_out\r2404_20261009\old_files\` + `_to_delete\superseded_20261009\2404_bore_answer\`. Generated: `r2404_20261009\regen\after`
     (57 configurations; checks pass; all other straight roots regenerate identically). Q-SPECS-2 = yes (library NPTF cone).
   - **Wave 1 ship workspace `tools\_out\wave1_ship_20261009\`** (= wave-1 merged tools + the 2404 diff + polish): polish done (gen_tee
     0-row guard, 2504 hex wording, 1502 stale texts, shape notes - text cells only); + the 8 batch-15 leftovers from OMi (6500 x4, 6501 x3,
     6505-12-08; `scripts\apply_leftovers.py`); + JIC tees with end-library ports (2505-12-12, 2606 x5 incl. the pilot, 2609-08 (new SPEC),
     2611 x2 incl. the pilot; `scripts\apply_jictees.py`; 2505-08-08 / -16-16 BLOCKED: library port depth deeper than the short leg).
     Regenerations + checks: `regen\after` (polish), `regen\leftovers`, `regen\jictees`, `checks_*.txt`. Next: SolidWorks dry runs into
     `swtest\<root>\` (2404 into `r2404_20261009\swtest\`), then stage for review.
   - Wave 2 (designs in `tools\_out\wave2_shapes_20261008\`): under the 2026-10-08 ruling only HOSEB 10 + PERLEGSW 1 rows are buildable;
     ANGLED's design review FAILED (2 blocking items); FLG61LEG 0 rows until OMi sends sizes.
   **2026-10-09: DRAWINGS DONE + EMAIL PACKAGE FOR OMi READY (not sent - the user sends it).** All 62 masters drawn
   (`10_DRAWINGS\dimension_check_20261009\`, 60 new + 1405 / 2650 copied from 10-08), every labelled value = its SW2 row
   (finalize.py, all_match on 62), sheets looked at (contact sheets `tools\_out\drawings_20261008\renders\cs1-8.png`).
   Script fixes (drw3 / geo3 / prep_jobs, before-copies `*_before_20261009*`): DROP picks 2500HX / 2502HX / 2603HX -> their
   -FG rows; body hex never dimensioned in a view that looks down a nut (1501 / 6500 / 6503 / 6600 / 6801 / 6803 / 6501 now in
   the right view); nut = NUT-feature flats in 2+ directions (6501's body arm was called NUT); title shrinks when it needs 3
   lines (2701 / 2702); note lines wrap at 92 characters; 5502 top-view label moved off the hex dimension; 2502 title
   "90 DEG MALE JIC X FEMALE PIPE ELBOW" (OMi's "MJ - FP Elbow"). Package in `10_DRAWINGS\for_OMi_2026-10-09\`:
   `OMi_dimension_check_drawings_2026-10-09.pdf` (cover + 62 pages, `combine\combine_omi.py`), `Email_to_OMi_2026-10-09.txt`
   (8 plain questions incl. the forged own-file question the user was waiting to ask; the 2404 bore question was removed 2026-10-09 - answered by the user, section 5), `OMi_missing_sizes_and_typos_2026-10-09.xlsx`
   (226 configurations only OMi can supply, 29 thread callouts that contradict the part number + NPFT / "Metric" ORB / NPTF
   swivel notes, 14 filler lengths; `tools\_out\omi_email_20261009\build_attachment.py`). Left out of the email on purpose
   (user / technical): bores wider than the port, 6801-04-02 / -12-12 (Air-Way vs Brennan), the 167 forged rows that need
   OMi data only if the own-file rule falls. Next: wave-1 polish and dry runs (below) - SolidWorks is free now.
   **2026-10-08 evening - (was) RESUME HERE (user near the usage limit; work paused / running in the background).**
   Workflow scripts: `C:\Users\sudha\.claude\projects\C--Users-sudha-OneDrive-Desktop-OMi-Handoff\3b57a418-fb1d-4dc6-b317-eef6cf16a081\workflows\scripts\`;
   resume = Workflow({scriptPath, resumeFromRunId}) - finished agents replay from cache. Same session only; in a new session
   read each workspace's own record instead.
   - **Usage limit hit 2026-10-08:** drawings STOPPED for a SolidWorks restart after the toolsmith - script v3 ready
     (`tools\_out\drawings_20261008\scripts\` geo3 / drw3 / run3 + finalize.py; how to run: the workflow result / scripts),
     6 of 62 drawn and checked (6401 1405 1501 2502HX 2650 6802 - re-run 6401 and 6802 with the final script), 56 left:
     restart SolidWorks, then batches of ~10 via run_jobs([...]) + finalize.py, read each PNG. Questions run STOPPED in its
     merge step (extracts cached in `tools\_out\questions_20261008\extract_*.json`) - resume wf_c765c441-402.
   - **Drawings of all 62 masters** (for the employer) - run wf_c5be84f9-caf (`dimension-drawings-all-masters-*.js`),
     workspace `tools\_out\drawings_20261008\` (plan\masters.json, scripts v3, results, renders), output
     `10_DRAWINGS\dimension_check_20261008\` -> combined `10_DRAWINGS\OMi_dimension_check_all_masters_2026-10-08.pdf`.
     SolidWorks leaks ~1 GB per drawing (12 GB after the toolsmith's ~10); a batch stops with needs_restart below 6 GB free
     commit - the user restarts SolidWorks, then resume.
   - **Open-questions doc for the employer** - RUNNING, run wf_c765c441-402 (`open-questions-plain-english-*.js`), output
     `tools\_out\questions_20261008\` (questions_final.json / .md). The doc: https://claude.ai/code/artifact/9d7f6978-ffb5-48d5-8076-16fd12b8dbb9
     (chart + "where things stand" filled; the other sections pending - fill one per update from questions_final.json). The
     run predates the user's ENDLIB = yes / 6 capabilities = yes: show those as decided 2026-10-08 and recount.
   - **Wave 1 (new masters)** - merged + audited, 33 configurations ready (`tools\_out\wave1_integrate_20261008\`, INTEGRATION.md,
     run wf_9db9f737-19f): next = the polish run (PAUSED, run wf_86d1cc10-86c `wave1-polish-*.js`: 2504 hex wording, stale
     rule texts, gen_tee crash on 0-row roots) -> then resume wf_9db9f737-19f with args {sw:true} for the SolidWorks dry runs
     AFTER the drawings are done (one SolidWorks job at a time) -> stage for review.
   - **Wave 2 (the 6 new shapes)** - PAUSED in design, run wf_8c9b56e4-1de (`wave2-new-shapes-*.js`, workspace
     `tools\_out\wave2_shapes_20261008\`); resume after the wave-1 polish, then args {impl:true}, later {impl:true, sw:true}.
   **2026-10-08:** batch 15 SHIPPED (section 1). Still open from the 2026-10-02 plan: **new masters wave 1 is PAUSED** (~48
   configurations built and statically checked per family in `tools\_out\newmasters_20261002\work\<family>\`, not merged, no
   SolidWorks dry runs yet - `sw_calls_*.json` + `EXPECTED.md` per family; its FOLDS 2501 table must be rebased on the batch-15
   table first). Below: the 2026-10-02 state as it was written (batch 14b and the clean-up are done).
   **Running on 2026-10-02** (overnight plan; user: "keep running"):
   - **Batch 14b = 2702 / 2703** (bulkhead hex arm 0.001 in short of the collar at -16, approved):
     `tools\_out\fix2702_20261002\` (fix + SolidWorks dry runs, 0 problems); prep 2026-10-02 12:15-12:45
     (`tools\_out\ship_20261002b\PREP.md`): fix and 2702 / 2703 review tables deployed live, ship-ready files, build calls,
     BUILD_PLAN.md. Next: the real builds, then ship like batch 14. Its paperwork must say that undoing batch 14's tools now
     needs 14b undone first (section 1, Toolchain) and add `fix2702_20261002/` / `ship_20261002b/` to the CLAUDE.md protected list.
   - **New masters, wave 1** (user: "yes, go ahead", largest family first, from the Brennan pilot STEPs; 21 families with a
     pilot and no new generator capability): `tools\_out\newmasters_20261002\`, write-up to come in
     `00_DOCS\NewMasters_Wave1_2026-10-02.md`. Built into STAGING for review; rows whose body values exist only at Brennan
     are prepared but stay MISSING until Q-BRENNAN-ONLY.
   - Also planned for the morning review: batch 15 (72 catalog-settled OMi rows + 5 -FG STEP rows) staged; then the folder
     clean-up the user asked for ("get rid of things not needed" = move to `_to_delete\<dated reason>\`, never delete; keep
     the protected / referenced folders, incl. `tools\_out\ship_20261002\` with its `old_files\`, `tools\_out\tier1_20261001\`
     (the SolidWorks dry runs batch 14 was checked against, the held-out 5404N-06 fix) and the batch-14b folders
     `tools\_out\fix2702_20261002\` / `ship_20261002b\`).
1. **Questions waiting for the user.** Unblock analysis 2026-10-08 (`tools\_out\unblock_20261008\`: `summary.txt`, `rows.csv` = every
   unbuilt BUILD row with its user gates and my work; `unblock.py` re-runs it): 763 rows not in a built file (760 + the 3 unbuilt
   5405). No user action needed: 51 (48 wave 1 + 3). Q-BRENNAN-ONLY = yes alone frees 76 more (24 of the 25 batch-15 held rows,
   37 prepared wave-1 sizes); it is a gate of ~435 rows. Greedy order after it: STEP downloads (~78 files, +89), Q-TRANSFER-ENDLIB
   (+54), capabilities Q-NEW-HOSEB (+39) / Q-NEW-ANGLEDHELIX (+37) / Q-NEW-PERLEGSW (+32), Q-SCOPE-TUBE (68 rows), Q-SOP5 (+48),
   Q-TRANSFER-TAPDRILL (+31), then ~15 small questions (~+90); ~127 stay (5404N bundle, O-rings, 1703 / 1704 flange legs, blocked).
   Counts rest on the 2026-10-01 catalog impact files + the wave-1 / batch-15 notes - approximate.
   - The 36 questions of `00_DOCS/NEXT_SESSION_PROMPT_2026-09-26.md`. Answered so far: 1 (ship Task A: yes = batch 14),
     4 (6410-12-08-O 1.480: shipped with Task A), 24 (2702 / 2703 offset: yes). **Q-31 (1404 bores) is still open:** batch
     14 shipped OMi's 17 bore cells; if the answer is Air-Way, revert them from
     `tools\_out\omi_apply_20260925\originals_before_apply\`, regenerate 1404, dry-run, rebuild. Q-32: 6404-10-08 shipped at
     OMi 1.750 (Brennan 1.740) - note Brennan in `$COMMENT` once answered. Q-2: the 10 held OMi bores.
   - Tier-1 questions (`00_DOCS/Tier1_Fixes_2026-10-01.md` section 3): Q-SPECS-5, Q-THREAD (6565-32-32), Q-BOREWIDE
     (6410-32-24-O), Q-PLACEHOLDER, Q-TRANSFER-5404N, Q-NEW-5404N-NAME, Q-SIZE40-JIC, Q-B-ELBOW, Q-B-SWELB, the -02 swivel
     bodies. Q-NEW-ASME40 is answered: Brennan-measured -40 threads (section 5). Q-SPECS-2 / Q-2404-BORE wait for OMi.
   - **Q-BRENNAN-ONLY** (~70 rows: may a row be built from Brennan alone, catalog or STEP, as ASSUMED?) - user: "later". It
     gates the open 2403 / 2405 / 2404-L rows, 6405 -02, 2406-03-04, the wave-1 Brennan-only rows and others.
   - Hex A/F: Air-Way 2-decimal values vs the wrench fraction (question 23).
   - The catalog questions in `00_DOCS/Brennan_Catalog_2026-10-01.md` (e.g. Q-NEW-F3-FLARELESS-ALIAS: 0618-08 / 0619-08 ->
     V0318-08 / V0319-08?).
2. **Brennan data (2026-10-01 / 02):**
   - Catalogs: 7 PDFs in `07_RAW_EXTRACTS/brennan_catalogs/` (user: "use any needed"), parsed and checked page by page in
     `tools/_out/brennan_catalog_20261001/` (427 tables, 5,056 rows; `catalog_verified.json` / `.xlsx`). Catalog values are
     the same source as OMi (Brennan) -> ASSUMED. Report: `00_DOCS/Brennan_Catalog_2026-10-01.md`.
   - **STEP list FINAL:** `00_DOCS/Brennan_STEP_list_2026-10-01.xlsx` / `.md`: Download now 96 (incl. 5404-N-06X2.000),
     Later 283, Conditional-Optional 57, Replaced by catalog 125, Already in repo 64.
   - **57 STEPs received 2026-10-02** (in `09_STEP_FILES`; manifest `tools/_out/step_ingest_20261002/MANIFEST_sha256.txt`):
     the 4 tier-1 geometry STEPs (6500-02-02-FG, 6506-12-14, 2406-03-04, 6410-04-02-O - MEASURED-ENDS can start: validate
     `swiv.py` / `ports.py` first), 33 pilots, 2501-40-40-FG / 5000-40-40 / 5404-40-40 / 5406-40-32, 2404-L-32-32,
     6565-32-32, 6802-32-32, 6410-32-12 / -16, 1700 x3, 2700-02-02, 2701-02-02 / -05-05, 2702-20-20, 2706-04-02,
     6801-16-08 / -24-32 (+ 2406-12-06 by mistake, kept).
   - **15 more STEPs coming** when the user's download limit resets: the 6801-L / -LL, 6805 6806 6807 6809 6810 6815 6832
     6835 6901 6902 pilots.
   - **No Brennan file for 26 part numbers** (user, 2026-10-02): 1405-20-24, 2403-06-02, 2502-20-16-FG, 2700-04 / -08 / -10 /
     -12 small, 2705-04-02, 6500-20-16 / -24-20 / -32-24-FG, 6501-16-12-FG, 6502-06-04 / -12-10-FG, 6802-04-02-NWO-FG,
     1602-08-08-08-FG, 1803-08-08-FG, 2406-06-12, 5404-L-04X2.000, 5404-N-06X2.000, 5404-R-04-04-047, 6425-08-08,
     6500-04-02-FG, 6502-04-02-FG, 6505-04-02, 6566-06-06-FG - the user will ask OMi for drawings.
3. **Tier-1 rows still waiting** (code ready and TEST-proven unless noted; `Tier1_Fixes` section 1): 6565-32-32 (Q-THREAD;
   STEP received), 6410-32-24-O (Q-BOREWIDE), 6802-32-32-NWO-FG (measure the received STEP), 6502-16-12-FG (Q-B-SWELB),
   6405-02-02-O / -02-04-O (data; Q-BRENNAN-ONLY), the -40 rows 2501-40-40-FG / 5000-40-40 / 5404-40-40 / 5406-40-32
   (Brennan-measured threads accepted; measure the received STEPs), the MEASURED-ENDS rows 6505-04-02, 2406-03-04,
   6410-04-02-O, 6506-12-14 (STEPs received) and 6500-04-02-FG / 6502-04-02-FG (no Brennan file, no dimensions anywhere).
4. **5404N-06** (8 rows, QA #163): the round-bar fix builds bodies, but its threads fail at -06 in SolidWorks; held out of
   the deploy. Brennan has no file for 5404-N-06X2.000. Needs a new look at the thread end.
5. **2404 / 2404-L: held until OMi clarifies the bores** (user 2026-10-02, QA #164). Then Q-SPECS-2, Q-2404-BORE, the 2404-L
   fold (Brennan 2404-L-08-08 and -32-32 STEPs are in the repo) and question 26 (10 OMi differences on 2404 / 6400). Leave
   2404 out of any "regenerate all" ship until then. **6400-L:** own master or a new feature? (ask the user).
6. **Re-run Build_5405** for 5405-12-08 / -16-08 / -16-12 (in its table since batch 11, not in the built file; question 30:
   dry-run into staging).
7. **6801-L / 6801-LL** (one topology with 6801). Air-Way gives only the long ORB leg (M11/M12), with no I3. The Brennan
   6801-L / -LL pilots are among the 15 STEPs coming; then fold them in (as 2501L). Note: the 6801-LL-08-08-NWO-FG Air-Way
   row looks like a -10 row.
8. **Other adjustable-ORB families**, whose tables exist: 6805 (x female NPTF), 6806 (x male NPTF), 6807 (ORB x ORB),
   6901/6902 (x NPSM swivel), 4601/4603 (hose barb). They need I3, THDL and groove dia (6801 values per ORB size, logged
   as an assumption) and more leg kinds. The NWO module is proven in SolidWorks; their pilots are coming.
9. **Blocked configurations still out** (6502-05/-12, 6565-20/-24, 6504-24-24 and 6410-20-12/-20-16/-24-16 are built since
   batch 14):
   - 1501-04-02-FG: bore vs the -02 stem tip.
   - 1501-24-24-FG: Air-Way nut 1.88 vs Brennan 2.125. Ask the user.
   - 2406-16-04: the port wall.
   - 6802-04-06-NWO-FG: Air-Way nut hex 0.56 for a -06 ORB, which needs 0.6875.
   - 6405-32-24-O: Air-Way D3 2.38 misprint (needs a STEP).
   - 6801-05-05 (question 25).
   - The 10 held OMi bores wider than the female port (question 2) and 6405-20-16-O (OMi length 1.000 = placeholder).
10. **1503**, and later 5503/5505: the angled leg needs a pipe (helix) thread helper. `gen_tee.py 1503` stops with
    "angled leg must carry a Thread-feature (JIC) end".
11. **-FG (forged) parts with only non-forged Air-Way rows (about 260).** Wait for Brennan -FG STEPs; do not build them
    from the non-forged dimensions (the user agreed). The coverage workbook lists the STEPs needed per series.
12. Smaller items:
    - `tools/README.md`: add the tier-1 tools (`measure/jicm.py`, `neck45.py`, `e45_model.py`, `swiv.py --model`) and
      `JIC_MEAS_40` / `ORB_FROM_6408_ROW` under "Measured end data" (`Tier1_Fixes` section 7 step 8) - not done with batch 14.
    - Copy the Brennan 2404 STEPs that tier 1 measured into `09_STEP_FILES` (15 ready-named files in
      `tools/_out/tier1_20261001/integrated/review_fix/steps/`; the user's folder).
    - 0306 bulkhead locknut, 0304-C cap nut, 6408-HHP: in new masters wave 1 (groups NUTS-CAPS, PLUGS).
    - Optional port countersink.
    - Series with no Air-Way page (6815, 6832, 6835 and others) need a dimensional source (pilots coming).
    - 45 deg elbows (2503, 6502, 6802) leave the leg plane `PLN2` and an axis sketch line visible - hide them.
    - Helix curves of suppressed threads show (blue) in saved parts - cosmetic.
    - SolidWorks volumes of the JIC -06 configurations are smaller than the OCP rebuild (6802-06-04 / -06-06 and
      6502-06-06-FG by 0.0136 in^3, 6801-06-xx by 0.0272) - compare sections some time.
    - Report to OMi (question 29): wrong thread callouts, 1.000 placeholders, reducer bores wider than the port, the 6801
      findings, OMi file typos.

## 4. Housekeeping

**SolidWorks** ended the overnight build at 11 GB after a "critically low on committed memory" warning (answered No).
Restart it before the next MCP build; a VBA editor window "test" was open - check it is not the user's unsaved work.

**0318.** DONE 2026-09-25: the overnight rebuild (opens in 0318-08) is now `11_MASTERS\0318_MASTER.SLDPRT`. The user
had run the stale 0318 module from the VBA editor twice (01:19 and again 20:08 on 2026-09-25 - reports without the
"Master left in its reference configuration" line); those builds, their report and the duplicate saves `_011925` /
`_200845` are in `_to_delete\superseded_20260925\`. **Remove the old Build_0318 module from the VBA editor before any
manual re-run** (it is still loaded there - that is what ran at 20:08).

**VBA import trap.** If the old module is not removed first, importing a `.bas` whose `Attribute VB_Name` already
exists creates `..._MASTER1`, and running the entry sub may run the OLD module. RUN_ME files always say "remove any old
module of the same name first". Builds through the MCP `run_macro` cannot hit this (it compiles the `.bas` on disk).

**The root folder** holds a 6-byte stale SolidWorks owner file, `~$2403_MASTER_macro_153206.SLDPRT` (2026-09-16). It is
harmless; move it to `_to_delete` when SolidWorks is closed.

## 5. User decisions on record

- ~~6410-12-08-O stays at Air-Way 1.09.~~ Superseded 2026-10-02: shipped at OMi 1.480 (= Brennan) with Task A ("yes to
  all", question 4 of 2026-09-26).
- 1404 / 1405: the swivel nut face sits at Air-Way W (Air-Way over Brennan). 1700 follows Air-Way.
- 0403: OMi's plated parts are built from the Air-Way UNPL rows of the same size ("Yes, map them").
- 2404-L, 6400-L and 2501-L are folded into their base masters ("Yes, all three"); regenerating the hand-built 2404/6400
  is allowed. (2501-L: folded, batch 13b. 2404 / 2404-L: on hold since 2026-10-02 until OMi clarifies the bores.)
- -FG parts that exist only as non-forged Air-Way rows: wait for Brennan -FG STEPs. Do not build shapes from the
  non-forged dimensions.
- The 5504 collar "looks too big" question: it matches Brennan. The real cause was the master opening in its smallest
  size, so every macro now saves in its reference configuration.
- 2026-09-25 (night): build every not-yet-built macro for real in SolidWorks and save the good parts in a separate
  folder "just like masters" for review in the morning (done: `11_MASTERS_NEW`).
- 2026-09-25 (evening): "accept the overnight build masters into 11_MASTERS" - done (38 parts, section 1). Then "yes
  ship": batch 13b + the regenerated 6404 / 6504 / 6565 shipped (QA #156).
- 2026-09-25 (evening): **OMi dimensions rank ABOVE Air-Way** ("OMi is more important than airway dimensions"), and
  **rounding-only differences are fine** (no change where OMi only differs by rounding to Air-Way's printed decimals, incl.
  the exact-fraction cases and the 15 differences that match when OMi is cut to Air-Way's decimals - QA #158). This changes
  the source order in CLAUDE.md ("Air-Way decides DIMENSIONS"): where both give a value, OMi's is used; Air-Way fills what OMi
  does not give. User, same evening: "OMi is only in charge of dimensions, for geometry use Brennan" (end shapes, forged
  bodies, seats, nuts, ports stay Brennan-derived). Evidence for the user's question to OMi: OMi's overall length equals the
  Brennan STEP length on 20 of 22 straights (Air-Way on 5) and the 6500 legs on 10/10 - OMi very likely uses Brennan's data. APPLIED since as Task A (173 of the 184 phase-A cells in 18 review
  tables, 11 held; shipped in batch 14 on 2026-10-02) - of the 220 real differences on certain mappings
  (00_DOCS/OMi_Dimension_Audit_2026-09-25.xlsx). Open at the time: (a) confirm the two earlier decisions it reverses -
  6410-12-08-O at Air-Way 1.09 (OMi 1.480) and the 1404 / 1405 nut face at Air-Way W; (b) does it cover the -FG rows (F1: OMi
  has data for 70 of 260; 46 have a master and all end modules)? (c) the uncertain leg mappings on elbows / tees (OMi M 1 / M 2
  / L 1 in side order) - without them no leg length comes from OMi; (d) DataStatus: OMi alone = ASSUMED; OMi + Air-Way
  agreeing = VERIFIED? (is OMi independent - audit section 3.6).
- 2026-10-01: Brennan catalogs (https://brennaninc.com/catalogs/): **"use any needed"**. Catalog values are the same source
  as OMi (Brennan) -> ASSUMED (Q-NEW-BRENNANCAT treated as yes).
- 2026-10-01: **"do the tier one fixes"** (the 14 tier-1 work groups of Task C; `00_DOCS/Tier1_Fixes_2026-10-01.md`).
- 2026-10-02: **"yes to all"** = ship batch 14: Task A (18 roots; question 1 of 2026-09-26) + the tier-1 fixes 6502 6802
  6404 6410 6565 + the new SPECs 2403 / 2405 (2404 then excluded, next item); **Q-SPECS-1 yes** (2403 / 2405 drop their
  15 / 4 DROP configurations). Task A shipped as staged: 6410-12-08-O at OMi 1.480 (question 4), the 1404 bores at OMi
  (Q-31 still open), 6404-10-08 at OMi 1.750 (Q-32). Built and shipped the same day (QA #159-#164).
- 2026-10-02: **2404 held: "keep 2404 exactly as it is"** until OMi clarifies the bores - hand-built master and tables
  untouched (incl. 2404-40-32's VERIFIED); Q-SPECS-2 / Q-2404-BORE on hold; the 2404-L rows wait with it.
- 2026-10-02: **-40 sizes: Brennan-measured threads are accepted** (the answer to "ASME B1.20.1 row or Brennan-measured?");
  threads only need to show on drawings.
- 2026-10-02: **Q-BRENNAN-ONLY: "later".** Rows whose values exist only at Brennan stay MISSING (values may be prepared in
  proposal files).
- 2026-10-02: parts with no Brennan file (26, section 3): the user will ask OMi.
- 2026-10-02: **2702 / 2703: stop the bulkhead hex arm 0.001 in short of the collar** at -16 ("okay"; question 24) ->
  batch 14b.
- 2026-10-02: **new masters: "yes, go ahead"**, largest family first, from the Brennan pilot STEPs (wave 1); build into
  staging for review.
- 2026-10-02 (night): "keep running": ship batch 14 (+ 2702 / 2703), stage wave 1 + batch 15 for the morning review, then
  clean up the folder ("get rid of things not needed" = move to `_to_delete\<dated reason>\`, never delete).
- 2026-10-08: **"ship batch"** = ship batch 15 as staged (done; QA #167-#169). The 5604 / 5605 collar re-run (QA #144) went with it.
- 2026-10-08: **Q-BRENNAN-ONLY = NO: "You cannot use Brennan data as your own."** No dimension may come from Brennan alone
  (catalog or 3D file). Rows whose values exist only at Brennan stay MISSING and need OMi's own dimensions / drawings (or
  Air-Way). The prepared Brennan-only proposals (batch-15 held rows, wave-1 PROPOSAL files) are NOT to be applied. Asked the
  same day about the "forged -FG part from its own Brennan 3D file" rule: **"keep for now until I send the pdfs to my employer
  so they can look at it and give feedback"** = the 6 shipped own-file configurations (2702-20-20-FG, 2701-02-02-FG,
  2701-05-05-FG, 6801-16-08-NWO-FG, 6801-24-32-NWO-FG, 6802-32-32-NWO-FG) stay as built; no NEW size from a Brennan file (the 7
  wave-1 pilots stay held) until the employer's feedback on the drawings. **Brennan 3D files for SHAPE only** (end forms, body
  form; sizes from OMi / Air-Way): **"Yes, shape is fine"** (re-confirmed 2026-10-08). Same day: "finish the new masters that
  need no decision" = wave 1 minus every Brennan-only row (~41 configurations).
- 2026-10-08: **Q-TRANSFER-ENDLIB = YES** ("Reuse already-measured end details - yes"): new masters take their end details
  (thread majors, tap drills, JIC / pipe / NPSM / swivel / adjustable-ORB / flange end data, female ORB port shape) from the
  existing end libraries, as on the built masters, instead of measuring each part's own 3D file. Sizes of the part body still
  only from OMi / Air-Way.
- 2026-10-08: **the 6 new generator capabilities = YES, "go ahead"**: Q-NEW-ANGLEDHELIX (thread on a 45 deg leg: 1503 1504
  5501 5503 5505 6810 6902), Q-NEW-HOSEB (hose-barb elbow leg: 4501 4503 4601 4603), Q-NEW-PERLEGSW (several swivel /
  adjustable-ORB legs on one part: 1601 1602 1603 6603 6606 6807 6566), Q-NEW-ANGLEDFEMALE (female pipe port on a 45 deg leg:
  5505 1504), Q-NEW-FLG61LEG (code 61 flange leg on elbows: 1703 1704), Q-NEW-ANGLEDNUT (swivel nut on a 45 deg leg: 6810 6902).
  Work = wave 2 (`tools\_out\wave2_shapes_20261008\`), built on the wave-1 merged toolchain, staged for review.
- 2026-10-09: **Q-2404-BORE answered by the user (from talking with OMi): the 2404 hole "isn't the same throughout"** = two
  bores, a larger one stepping down to a smaller one (option (b) of `00_DOCS\Tier1_Fixes_2026-10-01.md` s3), not one straight
  hole. Removed from the OMi email. Releases the 2404 hold of 2026-10-02 for the bores: the 24 HELD rows (now built with ONE bore
  in the hand-made master) get the step, + 2404-L x5 and the 4 "CB depth unsourced" rows (2404-02-04 / -08-02 / -16-32 / -32-20)
  become buildable; 2404-32-48 / 2404-40-40 still wait for the -48 / -40 pipe-end lengths. Still open before 2404 can be
  regenerated: where the step sits on sizes MS51500G does not list (default proposed: the hex mid-plane, Brennan's construction
  = shape), Q-SPECS-2 (library NPTF cone instead of the plain pipe end) and 2404-24-20 (OMi lists 1.25 / 1.25, Air-Way 1.31 / 1.25).

- 2026-10-14: **OMi answered question 8 of the 2026-10-09 email: "Yes we need drawings of ORings, Bent Tube, and Flareless nuts
  and sleeves."** = Q-SCOPE-ORING / Q36-20 yes, Q-SCOPE-TUBE / Q36-21 yes (now, own masters), Q-NEW-FLARELESS-N3 now. Drawings come
  from masters, so: new masters for 4000 / 4001 / 4005, the -Tube rows of 1703 / 1704 / 1803 / 1804 + 6701 (6701-L folded in),
  0618 / 0619, then dimension-check drawings. Read as also settling, for these families only, SOP step 5 (no hex) and
  carbon-steel-only (O-rings are rubber) - to confirm with the user; Q-SOP5 for plugs / collars stays open. Sizes still need
  OMi (request drafted 2026-10-14) - the 2026-10-08 Brennan rule stands. Scope: `00_DOCS\Scope_ORings_BentTube_Flareless_2026-10-14.md`.
- 2026-10-14 (later): **"use airway sizes"** (user, right after first allowing the AS568 table once OMi confirms each size) = Air-Way is the
  source for these families wherever it has them, as for every other series (OMi first, Air-Way fills). Air-Way s218 (O-rings for SAE J1926
  stud ends) lists OMi's own part numbers 4000-2 ... -32 (Buna-N) and 4001-2 ... -32 (Viton) with I.D., W, hardness, temperature -> 4000 /
  4001 build from Air-Way (ASSUMED). Air-Way s115 (1701-61 code 61 bent-tube flange elbow, 4 sizes) matches 1704-12-12 / -16-20 / -24-20 /
  -24-24-Tube (M3, N4, C, D, O; no bend radius or tube size). No Air-Way page found for 4005, 1703 / 1803 / 1804 -Tube, 6701, 0618 / 0619.
  Q-NEW-ORINGSRC settled (Air-Way); "start building the new model types on test rows" (staging `tools\_out\newtypes_20261014\`).
- 2026-10-15: **"i dont need drawings rn just do the soldiworks models"** (drawings of the new scope paused) and, for the ~704 parts never
  in our part list (ORFS / compression / test gauge / dropped adapters): **"use airway dimensions, check brennan too"** = Air-Way is the
  dimension source, Brennan's catalog only checks it (agree -> VERIFIED; differ -> built to Air-Way with Brennan in `$COMMENT`, s6).
- 2026-10-15: **forged ORFS parts: "Yes - use Air-Way's sizes for the 121 forged ORFS parts where Brennan's forged row matches on every
  cell (VERIFIED); the rest stay MISSING."** = an ORFS-only exception to the -FG rule above: a forged FS part takes the Air-Way
  non-forged row of the same size only where Brennan's catalog row of the forged part itself prints the same value in every compared
  cell (legs, body flats, nut hex); every other forged FS part stays MISSING. Shape of the forged body: Brennan (shape only).
- 2026-10-18: **ORFS model-type plan (`tools\_out\orfs_modeltype_20261016\PLAN.md`): "yes for all design questions"** =
  - **Q-FS-MASTER:** each FS series gets its own master (31 new + the FS4000 O-rings folded into the 4000 master). Long / -LN
    variants fold in as rows (FS2700-LN -> FS2700 ... FS6400-L -> FS6400, FS6801-L -> FS6801). "One master per shape" becomes "per
    shape and end family" (CLAUDE.md amended; correct the skill's "2404 / FS2404 / C2404 share one" line at ship time).
  - **Q-FS-ORBSTUD (a):** follow Air-Way for where the hex / washer face sits; measure the longer ORB stud on the pilots
    FS6400-08-08-O and FS6801-08-08-NWO-FG -> new end entries ORB_FS / NWO_FS.
  - **Q-FS-2NDSHAPE:** yes, for the pilots - measure the pilot end shapes on Air-Way's own 3D models too (the user signs in to
    3DContentCentral), so the new ORFS ends can be VERIFIED by two manufacturers.
  - **Q-FS-NUT:** yes - swivel-nut hex = the row's column where it agrees with Air-Way FF318 S, else FF318 S of the same dash (row's
    printed value in `$COMMENT`).
  - **Q-FS2406-NUT:** model the reducer + its nut as one solid (the nut = FS0318 of the first dash).
  - **Q-FS2408-HOLE:** ask OMi; until then build the plug solid, with the hole column kept and its feature suppressed.
  The download questions S1-S3 (STEPS_NEEDED.txt) are the user's actions: 9 Brennan pilots first, then the rest; Air-Way 3D models
  of the pilots; FS2408-08 only if the plug gets the hole.
- 2026-10-18 (later): **OMi answered the 2026-10-09 request** (two zips from the user's employer, unpacked in
  `07_RAW_EXTRACTS\omi_answers_20261018\`). User: **"this is verified information, use it to fill out more tables"**. OMi returned our
  workbook with the 14 real lengths ("Lengths to check") and answers to the typo list, and sent 14 drawings (Brennan-format sheets) for
  1405-04-06 / -08-12, 1502-06-06 / -12-08 / -12-12 / -20-20 / -24-24 / -32-32-FG, 1504-20-20-FG, 1602-02 / -04 / -08 / -16 / -20-FG.
  STAGED (not shipped) in `tools\_out\omi_answers_20261018\` (README.md, CHANGES.csv 273 cells, checks.txt): 15 rows MISSING ->
  ASSUMED (the 14 drawn parts + 6410-16-04-O); 4 more 6410 rows filled but held on Q-BOREWIDE; OMi's real length = the Air-Way length
  already in the table on all 8 rows that have one (6405-20-16-O's "1.000 placeholder" item is closed). 9 configurations are
  generator-ready (1405 +2, 1502 +6, 6410 +1; static checks clean, no SolidWorks dry run yet); 1504 / 1602 wait on the wave-2
  generator work. Read as: OMi supplying its supplier's (Brennan) drawings as its own answer makes those values OMi's data - used
  ONLY for the parts OMi sent; Q-BRENNAN-ONLY = NO stands for everything else. **Open: (1) mark these rows VERIFIED as the user
  said, or ASSUMED by the 2-source rule (staged ASSUMED)? (2) does OMi sending Brennan drawings mean Brennan's catalog may now be used
  for the other missing parts (the 517 / 570 of the 2026-10-18 count)?**
- 2026-10-18 (evening): **Q-BRENNAN-ONLY = YES** (reverses 2026-10-08): **"yes use brennan but still differentiate the two in tables in
  case i need to change it later"**. Brennan's catalogs and 3D files may now be a dimension source (the 570 parts of the count: 305 +
  53 in existing tables, 68 bent tubes / 6701, 34 dropped adapters, 110 ORFS - `tools\_out\brennan_yes_20261018\brennan_rows.csv`).
  The own-file -FG hold (2026-10-08) is lifted with it. **Marking (reversible):** every row whose size comes from Brennan alone gets
  `$PRP@DimSource` = `BRENNAN` (new review-table column; tested: generators write identical macros / SW2 with it -
  `tools\_out\brennan_yes_20261018\marker_test`) and `$PRP@AxialSource` starts with `[BRENNAN-ONLY 2026-10-18]` (that text reaches
  the built part's AxialSource property). DataStatus ASSUMED (one source). Rows taking OMi's own values keep `OMI`; Air-Way `AIRWAY`;
  OMi's 2026-10-18 Brennan-sheet drawings `OMI-DRAWING`. To undo: set every `BRENNAN` row to MISSING and regenerate. Conflicts between
  sources still go to the user (never picked silently); OMi / Air-Way stay ahead of Brennan where they give a value.
- 2026-10-18 (night): **open questions A1-A8, A10-A24 answered** ("do the recommended thing unless I put a caveat") - table with the
  caveats in `00_DOCS\ANSWERS_2026-10-18.md`. Highlights: tap drill per size yes (A1; -24 / -32 = A9 still OPEN), hexless parts + 0319
  yes (A2), 6400 rebuilt by the generator (A6), 1404 nut face at OMi (A20) but 1404 bores back to Air-Way (A21), 6565 kept (A22), OMi data
  VERIFIED - the 15 OMi-answer rows and OMi = Air-Way cells (A23), website list decides scope (A24). A19 (OMi values on ~96 built
  configurations): list the differences first, update only after the user approves. OMi-only questions -> `10_DRAWINGS\for_OMi_LATER\`.
  A9: "wait for a brennan step" (BRENNAN_5405-24-24 / -32-32). A19 approved: "apply groups 1, 2 and 3 ..., skipping 6504 L13 and holding
  the 3 swapped rows" -> 134 cells staged. 5 1404 nut faces held at Air-Way (A20 breaks the swivel there). Everything is in the stage
  `tools\_out\brennan_yes_20261018\stage` (= batch 16 + OMi answers + Brennan rows + A19-A23), to ship as batch 17 after batch 16.
  **Brennan rows staged (2026-10-18): 83** - wave 1 (batch-15 held 23, wave-1 proposals 24) + wave 2 (tees / elbows 13, straights 23); each
  regenerates with the batch-16 tools, old configurations unchanged (static checks clean; NO SolidWorks dry run yet - SolidWorks is used by the
  batch-16 ship session). Reports: `brennan_yes_20261018\wave1\*_REPORT.md`, `wave2\<group>\REPORT.md`. Held for generator work (data complete):
  ~100 rows - hose barbs 27, flange legs / 1700 collar, angled-helix / per-leg-swivel families, 5404-N 18 (OMi part-number form), -40 NPT
  end, 6400 / 6420 / 6425 / 6900 / 6815 / 6832 / 6835 SPECs. Not started: dropped adapters 34, bent tubes / 6701 68, ORFS 110.
  **Later 2026-10-18:**
  - **Dropped adapters applied to the stage** (`brennan_yes_20261018\wave3\adapters`, `scripts\apply_adapters.py`): the 37 wrongly-DROP rows
    rebased (old `apply_77.py` NOT run), 5406-P-08 / -12 alias rows, 31 new rows, + the 7 pending OMi values (user "yes, apply ... like A19",
    6500-08-06-FG ASSUMED). 45 more configurations generate; trial regeneration = the agent's test (only the approved OMi rows differ).
  - **Stage now:** 1,818 BUILD rows, 1,278 with data, 310 VERIFIED.
  - **ORFS stage:** `stage_orfs` (Q-FS-XFER yes) - 57 FS rows complete.
  - **Bent tubes:** 338 data cells prepared (`wave3\benttube`), 0 buildable (tube OD / bend radius / bore have no source).
  - **Generator features:** 5 built and proven separately in `tools\_out\genfeat_20261018\<hoseb|perlegsw|angled|flange|straights>`.
  - **MERGED** into `tools\_out\genfeat_20261018\merged\tools` = the toolset for batch 17 (MERGE_LOG.txt, verify\, regen\).
    - Each feature reproduced exactly; everything else is identical to batch 16.
    - New roots: 1504 1601 1602 1603 1700RC 1703 1704 1724 1800 1804 1824 4501 4503 4601 4603 5501 5503 5505 6400 6606 6807 6902 (+ 1503 now
      builds, 5404N reads OMi names, -40 pipe end, -02 ORB port).
  - **Their data rows applied to the stage** (`scripts\apply_genfeat.py`).
  - Regeneration of every root (`regen_genfeat\cmp.txt`): **1,357 configurations generate** with the merged tools on the stage, against
    1,166 with the batch-16 tools (+191); 0 existing configurations changed (1503 aside: never built, the old tools fail on it).
  - Stage: 1,377 BUILD rows with data, 310 VERIFIED, 440 MISSING.
  - **NOT YET:** SolidWorks dry runs (license), the ship of batch 16, then batch 17.

- 2026-10-20: **AIR-WAY FIRST (OMi's rule).** OMi (Triveni) returned the drawings with "Review of Drawings" / "Review of Drawings #2"
  (PDFs, on the PC): "AW means Airway. BI means Brennan Industries. We will prefer to use Airway over Brennan dimension when Airway has
  them available." Asked whether that also covers the numbers of OMi's own website parts file (= Brennan's data, evidence 2026-09-26):
  **Triveni said yes.** = Air-Way is the first dimension source wherever it prints a value; OMi's file / OMi's answers fill what Air-Way
  does not give; Brennan last (marked BRENNAN). **Reverses the 2026-09-25 order** (OMi dims > Air-Way) and with it the 6410-12-08-O
  1.480 answer (question 4), A19 / A20 and Task A where OMi differed from Air-Way. Staged: section 1 (`tools\_out\airway_first_20261020\`).
  Unchanged: ORFS (already Air-Way first), Brennan 3D files for shape, the 2-source VERIFIED rule, conflicts that cannot be built go to the
  user. Still to read: the AW / BI marks in the two PDFs.
- 2026-10-20 (Q1): **an Air-Way value that cannot be built -> Brennan's value** ("use brennans"): 6405-24-16-O L31, 6504-24-24 D1,
  6565-10-10 nut hexes; marked `$PRP@DimSource` BRENNAN.
- 2026-10-21: **Brennan's CAD parameter records may be used as Brennan values, following the rule** ("yes you can use them following my rule"): the records Brennan's CAD portal returns (`tools\_out\partcommunity_20261021`, PARTcommunity reversemap) count as Brennan data - Air-Way first, then OMi's file / answers, then Brennan; cells taken from a record are marked `$PRP@DimSource` BRENNAN. A family's letter codes are mapped against a real Brennan STEP of that family before its records are used.
- 2026-10-21: **Q-CODE62-CAT = yes** ("do the recommended"): code 62 flange heads -12 ... -32 come from Brennan's Flange catalog table
  3300-62 (head OD, thickness, groove OD) instead of downloading 1824-12 ... -32; for the 1803 / 1804 -Tube bent tubes and FS1800 / FS1804.
- 2026-10-21: **FS2408 plug: built the way Brennan builds it** ("build it however brennan builds it"; Q-FS2408-HOLE): solid or blind
  hole as in BRENNAN_FS2408-08.stp (received 2026-10-21).
- 2026-10-21: **6801-L / 6801-LL: as the earlier long variants** ("keep it the same as that"): folded into the 6801 master as rows,
  like 2501-L / 2501-LL (gen_tee SPEC 'fold'); where the extra length goes is measured on BRENNAN_6801-L-08-08-NWO-FG /
  6801-LL-08-08-NWO-FG (received 2026-10-21) - Q-NEW-FOLD-6801L.
- 2026-10-21: **A9 settled by the Brennan STEPs** (user 2026-10-18 "wait for a brennan step"; files received 2026-10-21):
  BRENNAN_5405-24-24 / -32-32 measured (puckfix fgelbow.py --port, -08 check reproduces 0.718 / 0.75 / 0.90): -24 tap drill 1.734, taper
  0.94, drill depth 1.16; -32 tap drill 2.218, taper 0.97, drill depth 1.18. The Air-Way value nearest Brennan is used (Air-Way first):
  **-24 = 1.72, -32 = 2.20** for empty tap-drill cells (A1 per-size transfer); rows with their own Air-Way value keep it. (Brennan's
  1.734 / 2.218 is the alternative if the user prefers.)

## 6. Conventions that grew during the build (keep them)

**Sources and data status:**
- Dimensions (lengths, legs, hexes, bores): **Air-Way first** wherever it prints a value, then the OMi dimension file / OMi's answers,
  then Brennan (OMi 2026-10-20, section 5; before: OMi file first, user 2026-09-25; rounding-only differences are no change). Geometry (end shapes: swivel nut, ports, NPSM, flange head,
  adjustable ORB; forged bodies, seats): Brennan STEPs, which also cross-check the dimensions.
- OMi and Brennan count as ONE source (OMi's lengths are Brennan's data, evidence 2026-09-26); Brennan catalog values are
  the same source. A row taking an OMi or catalog value is ASSUMED, with the cell, the old value and the decision in
  `$PRP@AxialSource` (Task A form: "<col>: OMi WebsitePartsInfo2026.xlsx Items!<cell> <header> = <v> (table had <old>)
  [user 2026-09-25: OMi dims > Air-Way, ASSUMED]").
- A shape from one manufacturer makes the row ASSUMED. Differences between the dimension source and Brennan are built to
  the dimension source and written in `$COMMENT`; an OMi value that cannot be built (e.g. a bore wider than the port it
  drills into) is held at the old value with the reason in `$COMMENT`.
- Measuring scripts are validated first: each must reproduce the sizes already measured before it is used on new ones.
- Every modelling assumption goes into `$PRP@AxialSource` of each row. Blocked configurations stay out of the table,
  with the reason in the generator summary and the RUN_ME.

**Macros:**
- Threads stay live through all checks and the all-configuration sweep, then every `THD_*` is suppressed before the save.
- The master is saved in its reference configuration (`progress_patch.ref_config_at_save`).
- The save step trusts the file date when SaveAs returns False.
- One report line per configuration comes from `progress_patch.add_progress`.
- Since the overnight generator fixes (regenerated set): a rejected sketch dimension is really deleted; an angle whose
  two lines do not meet is held by a driving `<name>_SUPPL` (its supplement); the helix start is read from the helix
  curve; the problem count only counts real FAIL lines.
- A master built from a pre-fix macro whose report shows "angle try" lines has a named angle that is DRIVEN (its table
  column does nothing - harmless while the column is constant, e.g. RELIEFANG 60 in 0403 2502HX 2601 2602 2605 2650 and
  most overnight parts). Rebuild it from a regenerated macro before that angle ever changes in a table.
- Since tier 1 (2026-10-02): revolve cuts are used where a forged corner must be turned clear (6502 NECKTRIM1 + NECKFILL1
  in every configuration; 6802 ORBTRIM only where a configuration needs it); the report gives the API return of each.
  Construction margins are check values only, never part dimensions.
- The live toolchain carries an unused 2404 SPEC (since 2026-10-02): leave 2404 out of every ship until the user answers.

**Shipping a batch:**
- A shipped batch contains the macros, the SW2 tables, `RUN_ME_batch<N>.txt`, QA_Log rows (numbered, next is #170),
  Topologies notes, a coverage refresh and this file.
- Superseded files go to `_to_delete\superseded_<date>\<reason>` AND a copy under `tools\_out\<ship folder>\old_files\`
  (sha256 MANIFEST in both; the user empties `_to_delete`). Never delete files.
- Before shipping: every old configuration is unchanged (`checks/regress.py`), every configuration's outline is clean
  (`checks/allcfg_check.py`), the sketches are fully defined (`checks/dofcheck_*.py`), and the static VBA check passes
  (`checks/vbacheck.py`, which now also rejects more than 24 line continuations). New or changed masters also go
  through the SolidWorks verify loop in `CLAUDE.md`.
- A real build through the MCP (only with the user's approval): close the old master, move the old files out, copy the
  checked macro + SW2 in, `run_macro` with no overrides, then `sweep_configs` of the saved part and `sweep_cmp.py` against
  its dry run - every configuration must be identical (1e-5).
- A part built by a dry run into staging may ship unchanged (moved, same sha256) when the shipped macro + SW2 are the ones
  that built it (a regeneration may differ only in the date line); its report keeps the staging "Saved to" line.
- A fix that fails in SolidWorks is held out of a deploy by reverting only its hunks, with an attribution check that every
  other fix keeps every line (5404N-06, 2026-10-02).
- MasterData workbook edits: back it up twice, edit with openpyxl (the file is an openpyxl 3.1.5 file), then prove that only
  the intended cells and XML parts changed (`tools\_out\ship_20261002\paperwork\update_masterdata.py`).

## 7. History

The complete Cowork workspace (generators with every intermediate version, all batch packages, regression outputs,
Brennan STEP measuring scratch, the conversation transcript and the skill) is archived in
`_archive\cloud_workspace_2026-09-25_part{1,2,3}of3.zip`. It unpacks to one folder `cloud_workspace_2026-09-25\` with a
MANIFEST_sha256.txt. The coverage scripts, previously held only inside the Cowork VM, are in
`_archive\device_vm_enum_2026-09-25` and, made portable, in `tools\coverage`.

2026-09-25 night: Claude's overnight SolidWorks build - write-up `00_DOCS\OVERNIGHT_BUILD_2026-09-25.md`. The files
changed overnight (generators, templates, sp3fix, vbacheck) and in the follow-up the same day (CLAUDE.md, this file,
tools/README.md)
have their previous versions in `_to_delete\superseded_20260925\`.

2026-10-02: batch 14. The toolchain before the tier-1 deploy is in `_to_delete\superseded_20261002\tier1_toolchain_before\`
and `tools\_out\ship_20261002\tools_before\`. The replaced macros, reports, SW2 tables and masters, and the previous
versions of this file, `CLAUDE.md`, the MasterData workbook, the coverage workbook (and its `tools\coverage\work` json) and
`11_MASTERS_NEW\README.txt` are in `_to_delete\superseded_20261002\batch14_replaced\` and
`tools\_out\ship_20261002\old_files\` (MANIFEST.txt, MANIFEST_paperwork.txt). Later that day the batch-14b prep replaced the
live `gen_tee.py` and the 2702 / 2703 review tables (old versions: `_to_delete\superseded_20261002\batch14b_replaced\`,
`tools\_out\ship_20261002b\old_files\`), and the fix of the batch-14 paperwork changed this file and `CLAUDE.md` again (old
versions in `paperwork_fix\` under both batch-14 folders, MANIFEST_paperwork_fix.txt).

2026-10-08: batch 15 (`tools\_out\ship_20261008\`: `scripts\` verify / compare / ship scripts, `checks\` evidence, `paperwork\`
MasterData + coverage + counts). The replaced masters, macros, reports, SW2 and review tables are in
`_to_delete\superseded_20261008\batch15_replaced\` and `tools\_out\ship_20261008\old_files\` (MANIFEST.txt, MANIFEST_5604_5605.txt,
MANIFEST_2601.txt); the paperwork files before the edit (MasterData, coverage workbook + `tools\coverage\work`, this file, CLAUDE.md,
the 11_MASTERS_NEW README, NEXT_SESSION_PROMPT_2026-10-01.md) in `paperwork\` under both (MANIFEST_paperwork.txt).
