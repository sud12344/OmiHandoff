# Open questions for you - 2026-10-18

Everything that still waits on your answer, in one place. Answer in any order; "yes to the recommendations" is a valid answer
for a whole group.

Already applied (not asked again here):
- **Q-BRENNAN-ONLY = YES** today: Brennan catalogs and 3D files may give sizes, marked `BRENNAN` in the tables so it can be undone.
  This also closes Q-NEW-CATRANK, Q-SPECS-5, Q36-17 and the forged "own Brennan 3D file" rule (Q-FG-OWNSTEP).
- **ORFS design questions Q-FS-*** all yes today.
- **OMi's answers today**: the 1.000 placeholder lengths (6410 / 6405 / 6420) and the typo list. 6405-20-16-O is closed.

Conflicts between sources are still never picked silently: they stay below.

How the row counts were made:
- "rows" = unbuilt configurations in `tools/_out/unblock_20261008/rows.csv` (763 rows, gates of 2026-10-08).
- Re-judged for this file with every decision up to today, Brennan = yes included. Result: 288 need no decision (my work),
  233 need only STEP downloads, 224 need a decision below, 12 need OMi, 6 are internal.
- "frees N" = rows this answer alone makes buildable (downloads allowed). "touches N" = rows that name it at all.
- Approximate: they rest on the 2026-10-08 gates.

---

## If you only answer five

1. **C1 - Ship batch 16?** It has been staged since 10-09. The 77-adapter fix (37 rows) and OMi's answers (9 rows) ship after it.
   The ORFS work builds on its toolchain.
2. **C6 / S1 - Download the 9 ORFS pilot STEPs.** 269 ORFS parts already have dimensions and wait only on these files.
3. **A1 - Q-TRANSFER-TAPDRILL: use Air-Way's tap drill per pipe size?** Recommended yes. Frees about 49 rows.
4. **A2 - Q-SOP5: model parts without a wrench hex (bent tubes, sleeves), and include 0319?** Recommended yes. Frees about 48 rows.
5. **C5 - Send the OMi size request** (`10_DRAWINGS/for_OMi_2026-10-14/`). 266 parts have no source but OMi (compression 230,
   test gauge 12 and others).

---

## A. Decisions that free the most parts

> **ANSWERED 2026-10-18 (A1-A8, A10-A24; A9 still open): see `00_DOCS/ANSWERS_2026-10-18.md`.** Group B moved to
> `10_DRAWINGS/for_OMi_LATER/QUESTIONS_FOR_OMi.md` (to send later).

### A1 - Q-TRANSFER-TAPDRILL (also Q-NEW-F1B-TAPDRILL-SCOPE, Q-NEW-F1A-5504TAP, Q36-19)
- Ask: female pipe ports where OMi gives no tap drill: use Air-Way's per-size value on existing families too?
  (-02 0.33, -04 0.43, -06 0.57, -08 0.70, -12 0.91, -16 1.14, -20 1.48)
- Options: yes, Air-Way per size / no, a value per part from OMi.
- **Recommended: yes.**
- Rows: touches 60, frees 49 (5405 x8, 5602 x7, 5504 x6, 5604, 5605, 5406, 5502, 6405, 6503, 6506 ...).
- Source: `tools/_out/questions_20261008/merged.json` (tap-drill-per-size).

### A2 - Q-SOP5: parts without a hex (+ the 0319 sleeves)
- Ask: SOP step 5 says a fitting without a hex cannot be modelled. Allow the exception?
- OMi's "yes, we need O-rings, bent tubes, flareless" (10-14) was read as settling it for those families. Please confirm.
  Same for the carbon-steel-only rule: O-rings are rubber.
- Also: include the 12 JIC tube sleeves 0319? They have Air-Way + OMi sizes and a shape file; only the no-hex rule holds them.
- Options: yes / no (leave hexless parts out).
- **Recommended: yes** (merged.json); include 0319 is left open (the scope doc says "optional, recommended").
- Rows: touches 50, frees 48 (1803 / 1804 -Tube 29, 0319 12, 6701 7, 0619 2).
- Sources: `merged.json` (hexless-parts-sop5); `00_DOCS/Scope_ORings_BentTube_Flareless_2026-10-14.md` s1, s4, s5 item 4;
  PROJECT_STATUS s5 (2026-10-14).

### A3 - Q-6900-IDENT
- Ask: the 6900 table calls these "female JIC union". They are male O-ring boss x female NPSM swivel straights. Correct the table?
- **Recommended: yes.**
- Rows: touches 22, frees 21.
- Source: `merged.json` (6900-identity).

### A4 - 5404-N long nipples: Q-TRANSFER-5404N + Q-NEW-5404N-NAME (+ Q-NEW-AWALIAS)
- Q-TRANSFER-5404N: length from the part number (the X value), bar diameter and bore from Air-Way's nipple of the same size,
  for every length? **Recommended: yes.**
- Q-NEW-5404N-NAME: keep OMi's part numbers (5404-N-06X2.000) or rename? **Recommended: keep OMi's form.**
- Q-NEW-AWALIAS: treat Air-Way's other names as the same parts (5406-2P = 5406-P-02, "5404-N-8-8 X 2 1/2" = 5404-N-08X2.500)?
  **Recommended: yes.**
- Rows: the three together free 21. None of them frees anything alone. The -06 sizes also need a fix of the thread end (my work).
- Source: `merged.json` (5404N-transfer, 5404N-naming, 5406P-alias).

### A5 - Q-NEW-F1B-ORBEND
- Ask: built 6801 ... 6804 elbows: copy the adjustable O-ring end values (thread length, groove, I3) from the table's own rows
  of the same O-ring size?
- **Recommended: yes.**
- Rows: touches 11, frees 11.
- Source: `merged.json` (orb-end-from-same-size-rows).

### A6 - Q-HANDMADE (rebuild 6400)
- Ask: the hand-made 2404 / 6400 model files are not in the project. Rebuild 6400 with the generator and fold 6400-L in,
  or will you send the old file?
- **Recommended: rebuild with the generator.**
- Rows: touches 13, frees 9.
- Source: `merged.json` (rebuild-6400); PROJECT_STATUS s3 item 5.

### A7 - Q-HX (old 2500HX / 2502HX / 2603HX models)
- Ask: these hand-made masters need 12 new sizes. Type them in by hand now, or move the families to the generator later?
- **Recommended: move to the generator later.**
- Rows: touches 12, frees 8 (once it is done).
- Source: `merged.json` (hx-masters-to-generator).

### A8 - Q-TRANSFER-I1
- Ask: bulkhead length I1 on 2700 / 2705 / 2706: use Air-Way's per-size value (-04 1.20, -06 1.28, -08 1.44, -10 1.58,
  -32 2.09) for every part of that size?
- **Recommended: yes.**
- Rows: touches 11, frees 7.
- Source: `merged.json` (bulkhead-I1-per-size).

### A9 - Q-CONFLICT-TAPDRILL-24 / -32 (Q36-33)
- Ask: Air-Way prints two tap drills for one pipe size. Which one per size?
  - -24: 1.72 (34 cells) or 1.70 (5505-24-24-FG)
  - -32: 2.19 (16 cells) or 2.20 (5000-32-24, 5405-32-32, 5502-32-32-FG)
- Options: 1.72 / 2.19, or 1.70 / 2.20.
- Recommendation: your call (2026-09-26 said: wait for one Brennan STEP each).
- Rows: touches 11. Frees 9 once A1 is answered.
- Source: `merged.json` (tap-drill-24-32); `00_DOCS/NEXT_SESSION_PROMPT_2026-09-26.md` q33.

### A10 - Q-TRANSFER-LN
- Ask: bulkhead parts sold with a locknut (-LN): model them exactly like the plain part, without the locknut?
- **Recommended: yes.** (Also asked OMi on 10-09, question 6. No answer recorded.)
- Rows: touches 7, frees 3 (7 together with A8).
- Source: `merged.json` (LN-equals-plain); `10_DRAWINGS/for_OMi_2026-10-09/Email_to_OMi_2026-10-09.txt` q6.

### A11 - Q-BOREWIDE + Q-TRANSFER-D3 (6404 / 6410 reducers)
- Q-BOREWIDE (Q36-2): OMi lists inside holes wider than the threaded port they run into. Cap them at the port drill, keep the
  built values, and report it to OMi?
  - Options: cap / keep and report; use OMi's values (some cannot be built); wait for OMi.
  - **Recommended: keep / cap, and report to OMi.**
  - Today: OMi's answers filled 6410-20-06-O / -20-08-O / -32-12-O / -32-16-O, but they stay held because of this question.
- Q-TRANSFER-D3: female O-ring ports on 6404 / 6410: use Air-Way's per-size port drill where the row has none (and instead of
  the impossible 1.72 on 6410-32-20-O)? **Recommended: yes.**
- Rows: together they free 7. Alone: 1 each.
- Sources: `merged.json` (bores-wider-than-port, orb-port-drill-per-size); `tools/_out/omi_answers_20261018/README.md`.

### A12 - Swivel offsets: Q-TRANSFER-SWOFFSET + Q-CONFLICT-SWOFFSET
- Q-TRANSFER-SWOFFSET: swivel straights 6504 / 6506 with only one length: derive the other from the swivel's nut-face-to-seat
  offset for that size? **Recommended: yes.**
- Q-CONFLICT-SWOFFSET: Air-Way prints two offsets at some sizes (-04 0.34 / 0.35, -06 0.37 / 0.38 ...). Which?
  **Recommended: the end library's value per size.**
- Rows: touches 6. Together they free 6.
- Source: `merged.json` (swivel-offset-transfer, swivel-offset-conflict).

### A13 - Q-NEW-F3-CODE62LEN (now relevant again: Brennan = yes)
- Ask: most Brennan 1803-FG / 1804-FG catalog rows print exactly the L1 / L2 / A/F of the code 61 row of the same size. Use them
  as printed (ASSUMED) and let the pilot STEP confirm?
- No recommendation in the docs. (check)
- Rows: 8 (1803-12 / -16 / -20 / -24, 1804-12 / -16 / -24 / -32 -FG).
- Source: `tools/_out/brennan_catalog_20261001/impact/F3.md`.

### A14 - Q-NEW-F1B-RANGE (now relevant again: Brennan = yes)
- Ask: for some 6901 / 6902 swivel bores Brennan prints a range (e.g. 0.44 / 0.46), not one drill. Model the min, the max, or
  measure the STEP? (Never averaged.)
- No recommendation in the docs. (check)
- Rows: 7 (6901-06-08, -12-06, -12-16, -16-12, -16-16, 6902-06-06, -08-08 -NWO-FG). They also need STEP downloads.
- Source: `tools/_out/brennan_catalog_20261001/impact/F1b.md`.

### A15 - Wave-2 shape questions (45 deg legs, hose barbs)
- **Q-ANGLED-P1**: the library port depth does not fit the short female legs of 45 deg elbows. Cap the port at leg - 0.05
  (logged assumption), or wait for OMi port data? No recommendation. Rows: 2 (5503-06-06-FG, 5505-04-04-FG), +3 later.
- **Q-ANGLED-NECKNPSM**: confirm the NPSM neck turn as on 6502 (shape from the Brennan 1503 / 1504 STEPs). Rows: 8 of the 14
  1503 rows + 1504-04-04-FG.
- **Q-ANGLED-5503D**: Air-Way's printed male bore on 5503-02 / -04 / -08 / -12-FG is not a bore. Ask OMi? Rows: 4.
  (check: Brennan = yes may now give these bores.)
- **Q-HOSEB-BORE**: no source prints the hose-barb drill. (a) the part's own Air-Way bore, (b) the Air-Way 4404 bore of that
  size, (c) MISSING until OMi.
  - **Recommended: (a) for 4601 / 4603** (staged that way). For 4501 it is your pick of (b) or (c).
  - Rows: 1 blocked (4501-32-32-FG); 10 staged 4601 / 4603 rows rest on (a).
- Sources: `tools/_out/wave2_shapes_20261008/ANGLED/DESIGN.md` s5 (last section), `HOSEB/DESIGN.md` s5;
  `00_DOCS/NEXT_SESSION_PROMPT_2026-10-10.md`.

### A16 - Q-NEW-1700BODY
- Ask: three big 1700 flange straights have a round collar with two wrench flats, not a full hex. Model the real collar, or use
  the full-hex model?
- **Recommended: model the round collar.**
- Rows: 3 (1700-20-16, -24-20, -32-24).
- Source: `merged.json` (1700-round-collar).

### A17 - Q-NEW-FLG62LEG
- Ask: approve the code 62 flange leg for the forged 1803 / 1804 elbows - the same work as the code 61 leg you approved?
- **Recommended: yes.** (check: not in the 6 capabilities approved on 10-08.)
- Rows: touches 6.
- Source: `merged.json` (flange-62-leg).

### A18 - Q-TRANSFER-ORBGW
- Ask: O-ring groove width at -14 and -32: the only number is 0.125, measured on Brennan's 6400-14-14-O / -32-32-O. Accept it as
  an end detail, or ask OMi? (check: Brennan = yes may settle it.)
- Recommendation: your call.
- Rows: touches 4 (merged.json says 10), frees 4 after A6.
- Source: `merged.json` (orb-groove-14-32).

### Rules that change many rows but free few

### A19 - Update built parts to OMi's values (Q36-5 ... 10, 13, 14)
- Ask: about 95 configurations built earlier still carry Air-Way numbers where OMi differs. Update them to OMi (rebuild + re-check)?
- Options: update all / update some families / keep.
- **Recommended: update all.**
- Rows: 96 built configurations change, none freed.
- Source: `merged.json` (omi-values-on-built-parts); `NEXT_SESSION_PROMPT_2026-09-26.md` q5-14.

### A20 - Q36-12: 1404 nut face
- Ask: put the 1404 swivel nut face at OMi's overall length? All 23 built sizes move -0.07 to +0.14 in. This reverses your
  "nut face at Air-Way W".
- **Recommended: use OMi.**
- Rows: 23 built.
- Source: `merged.json` (1404-nut-face).

### A21 - Q36-31: 1404 bores
- Ask: keep OMi's 17 bores (shipped in batch 14) or go back to Air-Way? OMi's are 0.01-0.05 in below Brennan's files on 8 of 8.
- **Recommended: Air-Way.**
- Rows: 17 built cells.
- Source: `merged.json` (1404-bores); PROJECT_STATUS s3 item 1.

### A22 - Q36-11: 6565 lengths
- Ask: OMi's 6565 body is 0.12-0.55 in shorter than Air-Way's and leaves no room for the hex at -04 to -16. Keep the 8 built
  sizes until OMi (or Brennan 6565-08-08) confirms?
- **Recommended: keep as built until checked.**
- Rows: 9.
- Source: `merged.json` (6565-omi-lengths).

### A23 - VERIFIED or ASSUMED for OMi's data
- (1) The 15 rows filled today from OMi's drawings: you called the data "verified". The rule says VERIFIED needs 2 independent
  sources, and OMi's data is Brennan's. Staged as ASSUMED. Mark them VERIFIED?
- (2) When OMi and Air-Way give the same number, may it count as VERIFIED? **Recommended: yes** (merged.json). Today 8 rows
  have OMi's real length = Air-Way's.
- Rows: 15 staged + the OMi = Air-Way rows. Status only, nothing freed.
- Sources: PROJECT_STATUS s5 (2026-10-18 later, open item 1); `merged.json` (omi-plus-airway-verified);
  `tools/_out/omi_answers_20261018/README.md`.

### A24 - Q36-28: parts only in OMi's parts file (check)
- Ask: OMi's dimension file lists parts that are not on OMi's website (e.g. 0306-14, 3474-08-08-NWO, 6420-04-02). Add them?
- **Recommended: no, the website list decides.** CLAUDE.md and the 10-16 ORFS work (114 FS rows -> DROP) already follow it.
- Rows: touches 469. Nothing freed.
- Source: `merged.json` (scope-omi-file-only-parts).

---

### New after the answers (2026-10-18, from the Brennan staging)
- **Q-CODE62-CAT:** take the code 62 flange heads -12 to -32 (OD, thickness, groove OD) from Brennan's catalog table 3300-62 instead of
  waiting for 5 STEPs? Frees the 1803 / 1804 / FS1800 / FS1804 rows that only wait on heads. (`wave3/benttube/REPORT.md`)
- **Q-FS-XFER: ANSWERED YES 2026-10-18** (applied: `tools/_out/brennan_yes_20261018/stage_orfs`). ORFS rows - take per-dash bores and stud lengths (L9 / L11 / L14 / L31) from Air-Way's rows of the same end where they
  agree unanimously (154 cells, `tools/_out/brennan_yes_20261018/wave3/orfs/cells_proposed.csv`)? Like A1 / A8 / A11 (per-size transfers).
  Makes 45 more ORFS rows complete.
- **Bent-tube sizes:** tube OD, wall / bore, bend radius and end-hex length have no source for any of the 68 bent tubes. Options: OMi (in
  the OMi questions file), Air-Way's own 3D models, or each part's own Brennan STEP (Brennan = yes).
- **Q-PLUG-SQHEAD:** 5406-SHP square-head length from a pilot-ratio rule (4 rows) - from the wave-1 rebase.

## B. Things only OMi can answer (for the email)

**Already in the drafted request** `10_DRAWINGS/for_OMi_2026-10-14/` (not sent):
- **Q-NEW-4005CODE**: 4005 flange O-rings - code 61 or 62? AS568 size or I.D. + cross-section, material, hardness. Rows: 9.
- **Bent-tube sizes**: tube OD + wall, bend radius, legs, hexes for 1703 / 1704 / 1803 / 1804 -Tube and 6701. Rows: 68.
  (check) The draft predates Brennan = yes: the 68 are now on the Brennan list (`tools/_out/brennan_yes_20261018/brennan_rows.csv`).
  Keep this item, trim it, or keep it as a cross-check?
- **Flareless 0618 / 0619 sizes** and shapes. Rows: 3.
- **13 parts only in OMi's parts file** (e.g. 4000-05, 6701-10-10, 0618-06): do they sell them?
- **One drawing per series, or one per part number?**

**Not in the draft yet** (the 10-18 hand-over suggests adding them):
- **Compression (230) and test-gauge (12) dimensions.** No Air-Way series. Source: `00_DOCS/NEXT_SESSION_PROMPT_2026-10-18.md`.
- **Q-FS2408-HOLE**: is the FS2408 plug solid or does it have Air-Way's blind hole? Built solid meanwhile (your decision today).
  Source: `tools/_out/orfs_modeltype_20261016/DECISIONS.md`.
- **FS0319-24 collar**: Air-Way 1.71 vs Brennan 1.910, and Air-Way's own FF2407-24 collar is 2.00. "Worth holding until OMi
  confirms." Source: `orfs_modeltype_20261016/PLAN.md` D5; PROJECT_STATUS s3 item 0.
- **The dropped adapters with no Air-Way row**: 40. Brennan prints 34 (now usable), so 6 still need OMi.
  Source: `tools/_out/adapters77_20261016/possible_2535.json`, REPORT_77.md.
- **6 ORFS parts with no source.** Source: `possible_2535.json`.
- **6420-12-12**: OMi's length 1.730 does not fit the library ports - which body? (check)
  Source: `merged.json` (answered list, 6420-12-12-PORTS).
- **The rest of the 226 "sizes we need"** (OMi sent 14). Re-ask only for what Brennan cannot cover now (my work to re-count).
  (check) Source: `tools/_out/omi_answers_20261018/README.md`.

**Asked on 10-09, no answer recorded - chase** (check against OMi's reply):
- q1: does any number on the 62 drawings look wrong?
- q2 (DRW-TITLE-BLOCK): what goes in the title block (logo, material, finish, tolerances, drawn by)?
- q4 (Q36-27): small 6408 plugs (-02, -03, -05, -04-O-SLD) - hollow or solid? **Recommended meanwhile: solid.** Rows: 4.
- q6 (Q-TRANSFER-LN): -LN parts without the locknut OK? (You can also just decide it: A10.)
- q7 (6 parts from Brennan files) is overtaken by your Brennan = yes.
- Source: `10_DRAWINGS/for_OMi_2026-10-09/Email_to_OMi_2026-10-09.txt`; `tools/_out/omi_answers_20261018/README.md`
  (OMi filled the lengths and typo sheets only).

**Replies OMi asked for** (their notes on the typo sheet):
- "NPFT - why is this an issue?" Suggested reply: NPFT is not a thread name; customers and search filters looking for NPTF miss
  those 234 parts.
- Pipe swivel ends written NPTF (229 rows) - "not sure what this means". Suggested reply: their own drawings call the swivel
  thread NPSM (e.g. "3/8-18 NPSM"), so the website "NPTF" on the swivel side is the typo.
- Source: `tools/_out/omi_answers_20261018/README.md`.

**Findings to report** (left out of the 10-09 email on purpose; Q36-29):
- Bores wider than the port they drill into (A11).
- 6801-04-02: Air-Way leg 1.03, Brennan 0.92. 6801-12-12: Air-Way thread length 0.469, Brennan 0.410.
- 4601-16-12-NWO-FG: Air-Way's -FG row differs strongly from Brennan and from Air-Way's own plain row.
- 1704 rows 260-272 of OMi's file say "45° Elbow".
- Sources: PROJECT_STATUS s2 + s3 item 12; `wave2_shapes_20261008/HOSEB/DESIGN.md` s5; `FLG61LEG/DESIGN.md` s7.

---

## C. Ship / go-ahead approvals and your actions

### C1 - Ship batch 16
- Contents: wave 1 (33 configurations), 8 batch-15 leftovers, JIC tees (2505 x1, 2606 x5, 2609 x1, 2611 x2), 2404 (57
  configurations, stepped bores), 5405 (+3), and the corner-puck fix (re-ships the 14 shipped elbow masters that lost the
  corner on 16 configurations).
- Before: I re-run the interrupted puck-fix dry runs, and rebase wave 1's 2501 table on the batch-15 table.
- Recommended in the docs: ask you once the puck dry runs pass.
- Sources: `00_DOCS/NEXT_SESSION_PROMPT_2026-10-10.md`, `-10-09.md`, `-10-18.md` item 6.

### C2 - Apply the 77-adapter changes after batch 16
- 37 Air-Way rows wrongly marked DROP turn BUILD (21 VERIFIED / 14 ASSUMED / 2 special). `apply_77.py --apply` at ship time.
- Source: `tools/_out/adapters77_20261016/REPORT_77.md`.

### C3 - Ship OMi's answers with / after batch 16
- 9 configurations generator-ready (1405 +2, 1502 +6, 6410 +1). SolidWorks dry runs first. 1502 is new in batch 16.
- Source: `tools/_out/omi_answers_20261018/README.md`.

### C4 - Ship the O-ring master 4000 (4000 + 4001, 21 configurations)
- Adds `gen_ring.py`; CLAUDE.md "Carbon steel only" gets the O-ring exception. Dry run 0 FAIL.
- Waits for your "ship". (check: you may want it together with the bent tubes later.)
- Source: `tools/_out/newtypes_20261014/README.md` (Ship section).

### C5 - Send the OMi size request
- Draft: `10_DRAWINGS/for_OMi_2026-10-14/` (email + spreadsheet). Add the B items "not in the draft yet" if you want.
- Source: `00_DOCS/NEXT_SESSION_PROMPT_2026-10-18.md` ("Waiting on the user").

### C6 - Your downloads (save as `09_STEP_FILES/BRENNAN_<part number>.stp`)
- **S1 - ORFS pilots, first (9 files)**: FS2403-08-08, FS6500-08-08-FG, FS2701-08-08-FG, FS6400-08-08-O, FS6801-08-08-NWO-FG,
  FS0318-08, FS0319-08, FS0306-08, FS2406-08-06. Then 8 per-dash + 15 family files after the pilots pass.
  **Recommended: pilots first.** 269 ORFS parts wait.
- **S2 - Air-Way's own 3D models of the pilots** (A1-A9, 3DContentCentral; the sign-in is yours). You said yes to using them
  (Q-FS-2NDSHAPE); the download is still open.
- **S3 - BRENNAN_FS2408-08**: only if the plug gets the hole (B, Q-FS2408-HOLE).
- **Code 62 flange heads -12 / -16 / -20 / -24 / -32** (e.g. 1824-12 ... -32): 28 of the 29 1803 / 1804 -Tube parts block without them.
- **V0318-08 / V0319-08** (flareless shape) and **1704-16-16, 1803-16-16, 6701-08-08** (bent-tube shape checks).
- **15 pilots promised on 10-02**: 6801-L / -LL, 6805, 6806, 6807, 6809, 6810, 6815, 6832, 6835, 6901, 6902.
- **New since Brennan = yes**: 10 files that are the ONLY size source of their part (1504-32-32-FG, 5404-L-04X3.000 / X4.000,
  5503 x5, 6566-16-16-FG, 6806-12-08-NWO-FG) and 214 shape files for parts that have sizes.
- Rows: about 233 rows need nothing but downloads.
- Sources: `tools/_out/orfs_modeltype_20261016/STEPS_NEEDED.txt`; `tools/_out/brennan_yes_20261018/3D_FILES_NEEDED.md`.

---

## D. Small / cosmetic

Conflicts and misprints (1-2 rows each):
- **Q36-25 - 6801-05-05**: Air-Way + Brennan 1.13 vs the military standard 1.090. **Recommended: 1.13**, note 1.090.
- **Q-CONFLICT-2408-14-SOLID**: hex Air-Way 1.125 vs MS51518D (and Brennan) 1.25. **Recommended: 1.25.**
- **1501-24-24-FG nut**: Air-Way 1.88 is smaller than its 1-1/2 NPSM thread. **Recommended: end library 2.125.**
- **6802-04-06-NWO-FG locknut**: Air-Way 0.56 cannot fit a -06 thread. **Recommended: end library 0.6875.**
- **Q-GARBLE**: read Air-Way's ".31" on 6600-24-24-24-FG as 1.31? **Recommended: yes.**
- **Q-CONFLICT-6404-D3-08**: 6404-08-12 port drill 0.68 or 0.97? **Recommended: 0.68.**
- **Q-CONFLICT-6900-05-04-O**: Air-Way W4 1.30 and L2 1.19 cannot both be right. **Recommended: keep W4.** (Brennan prints a
  third option: L 1.280 / L1 1.090.)
- **Q-CONFLICT-2502-MS51506**: 2502-08-04-FG / -12-08-FG legs, OMi vs MS51506. Your call. Rows: 2.
- **6801-LL-08-08 Air-Way row** equals its -08-10 row. Ignore it? **Recommended: yes.**
- **Q-THREAD / Q36-18**: where Air-Way's thread contradicts the part number, use the part number's thread and note the
  misprint? **Recommended: yes.** (6565-32-32; also the 16 ORFS thread slips, PLAN.md D1.)

Shape details:
- **Facing cut** on 90 deg swivel elbows (1502-04-04-FG, 6500-05-05-FG ridge). **Recommended: yes.** Rows: 1.
- **Q-SIZE40-JIC**: -40 JIC end like Brennan's part (1.335 / 0.140) or the standard (1.109 / 0.125)? **Recommended: Brennan's.** Rows: 1.
- **Q-NEW-NPT01**: 1/16-27 NPT for 5406-HHP-01 - Brennan-measured or ASME row? **Recommended: Brennan-measured.**
- **Q-B-OTHER-6408HHP**: read OMi's "Body Diameter" as the socket plug's round head? **Recommended: yes.** Rows: 7.
- **Q-PLUG-SOCKDEPTH**: socket depth from the Brennan sample's ratio, or ask OMi? Your call. (check: Brennan = yes changes it.)
- **Q-NEW-F3-FLARELESS-ALIAS**: is Brennan V0318 / V0319 the same part as OMi 0618 / 0619? No recommendation. Rows: 3. (check)
- **JIC-RELIEF-A1**: keep the military thread relief on forged JIC legs (Brennan 2504 / 2606 / 2611 have none)? **Recommended: keep.**
- **PORT-COUNTERSINK**: model the small countersink at port mouths? Your call.
- **Hex arm 0.001 short on FS bulkheads** (PLAN R2) and on flange legs (Q-FLG61-SHORT): only if a dry run fails. Decide then.
- **FS0319 sleeves**: a per-size rule from the -08 pilot, or one STEP per size (STEPS_NEEDED part 4)? No recommendation.
- **Wave-2 flange-leg details** (check whether answered): Q-FLG61-O24 (-24 head 2.38, rounding-only - recommended 2.38),
  Q-FLG61-NECK (keep the hex to the head - recommended keep), Q-FLG61-SCOPEROWS (add the 15 missing OMi -FG numbers as MISSING
  rows - recommended yes). Source: `wave2_shapes_20261008/FLG61LEG/DESIGN.md` s7.

Rules and sources:
- **Q-F1 / Q36-16**: forged parts whose only Air-Way row is the plain part may use OMi's own values (as batch 15 did)?
  **Recommended: yes.** Rows: 1.
- **Q-NEW-6407SIB**: fetch Air-Way's 6407 page for the 3474 adjustable unions? Your call. (check: Brennan = yes now covers 7 rows.)
- **Optional second sources** (Q-CALIPER / Q36-22, Parker 4300, MS51531, MS on forged rows, published standards): which may
  upgrade ASSUMED to VERIFIED? **Recommended: caliper readings yes**; the rest your call.
- **Q36-23**: round 2-decimal hexes to the wrench fraction (~575 cells)? **Recommended: not now.**
- **2404-32-48 / 2404-40-40**: still wait for the -48 / -40 pipe-end lengths. (check whether a source exists now.)
  Source: PROJECT_STATUS s5 (2026-10-09).

Sources for D unless noted: `tools/_out/questions_20261008/merged.json`; `NEXT_SESSION_PROMPT_2026-09-26.md`;
`orfs_modeltype_20261016/PLAN.md` s4 / s8; `brennan_catalog_20261001/impact/F45D.md`.

---

## Closed since the older lists (for the record)
- Today: Q-BRENNAN-ONLY, Q-NEW-CATRANK, Q-SPECS-5, Q36-17, Q-FG-OWNSTEP (yes). Q-FS-MASTER / -ORBSTUD / -2NDSHAPE / -NUT,
  Q-FS2406-NUT, Q-FS2408-HOLE (yes / ask OMi). Q-PLACEHOLDER / Q36-3 (OMi answered; 6420-08-08 = 1.5 noted).
- Moot with Brennan = yes (check): catalog-as-evidence (Q-CATALOG-PAIRING, Q-B-*, Q36-14 / 15 reading part);
  Q-NEW-F2A-NOTINCAT, -F3-1803PILOT, -F3-6566, -F1A-1602PILOT, Q-CAT-5404N-BORE (Brennan routes now allowed;
  OMi / Air-Way stay ahead where they give a value); Q-FLG61-AWNEAR (the own files are allowed now);
  Q-NEW-F2A-DRILLRANGE (1405-04-06 has OMi's drawing).
- Earlier: Q-SPECS-2 and Q-2404-BORE (10-09), Q-SCOPE-ORING / -TUBE, Q-NEW-ORINGSRC, Q-NEW-FLARELESS-N3 (10-14),
  Q-TRANSFER-ENDLIB and the 6 capabilities (10-08), Q36-1 / 4 / 24 / 29 (the error report went with the 10-09 email).
