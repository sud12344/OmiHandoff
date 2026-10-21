# What the 987 not-yet parts need (2026-10-20)

Read-only analysis (no file changed except this one). Universe and "ready" exactly as `tools/_out/count_20261020/count_ready.py`: 2,535 OMi parts, 1,351 shipped + 197 generated = 1,548 ready, **987 not yet**. The 987 were taken from the same sets (OMi website lists in `07_RAW_EXTRACTS/omi_feed` minus the shipped SW2 configurations in `04_DESIGN_TABLES`, minus `tools/_out/orfs_gen_20261020/regen/new/*/*_SW2.xlsx`, minus the O-ring table) and every one was looked up in the review tables (`04_DESIGN_TABLES`, the ORFS stage `tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES`), the Brennan wave notes (`tools/_out/brennan_yes_20261018/wave1-3/*/rows.csv`) and the docs cited per group.

Each part is counted once, under the FIRST thing that has to happen (a download, an OMi answer, a decision, or only my work). The "also" notes name what comes after. Where a reason is my reading and not written in a doc it says "inference".
Caveat: many review-table `$COMMENT`s (BUILD-NEAR / BUILD-MISSING) predate Brennan = yes (2026-10-18) and batch 17; the wave notes refer to the batch-16 generators. Where batch 17 added the capability (flange legs, 45 deg legs, per-leg swivels, hose barb, 6400) the toolchain gate is treated as closed.

## Summary

| Category | OMi parts |
|---|---|
| (a) Brennan STEP files to download | 449 |
| (b) Dimensions missing everywhere - ask OMi | 291 |
| (c) User decision | 123 |
| (d) Generator / table work only (no new data) | 94 |
| (e) Out of scope | 30 |
| **Total not yet** | **987** |
| Counted "ready" but HELD (generator work only, separate list below) | 35 |

Of (b), 242 are compression (230) + test gauge (12). (a) needs 240 distinct Brennan files (list below); the 2 A9 files, the 6 FS2403 straights, the 5 FS2701 bulkheads, the 7 FS6801 studs, FS2406-08-04, FS0304-C-08, the 5 code 62 heads 1824-NN and the 9 adjustable-family pilots each free a whole group.

## Held: counted ready, need generator work only (35)

| Root | Parts | Why held (batch 17, QA #175, `tools/_out/batch17_20261019/RESUME.md`) | Part numbers |
|---|---|---|---|
| 5404N | 18 | -06 threads fail in SolidWorks again (QA #163); old master stays | 5404-N-04X2.500, 5404-N-04X3.500, 5404-N-04X4.000, 5404-N-04X4.500, 5404-N-04X5.000, 5404-N-04X5.500, 5404-N-04X6.000, 5404-N-06X2.000, 5404-N-06X2.500, 5404-N-06X3.000, 5404-N-06X3.500, 5404-N-06X4.000, 5404-N-06X5.000, 5404-N-06X6.000, 5404-N-08X3.500, 5404-N-08X4.500, 5404-N-08X5.000, 5404-N-08X6.000 |
| 4503 | 7 | hose face-off on the hose leg | 4503-04-04-FG, 4503-08-08-FG, 4503-12-12-FG, 4503-16-12-FG, 4503-16-16-FG, 4503-20-20-FG, 4503-24-24-FG |
| 4603 | 5 | hose face-off on the hose leg | 4603-04-04-NWO-FG, 4603-06-06-NWO-FG, 4603-08-08-NWO-FG, 4603-12-12-NWO-FG, 4603-16-16-NWO-FG |
| 1700RC | 3 | FLATS sketch not fully defined | 1700-20-16, 1700-24-20, 1700-32-24 |
| 1800 | 1 | FLATS sketch not fully defined | 1800-08-08 |
| 1703 | 1 | HEX2 direction | 1703-24-24-FG |

## (a) Brennan STEP files to download - 449 parts

| Group | Parts | What unblocks it | Source |
|---|---|---|---|
| Adjustable-ORB families 6805 / 6806 / 6807 / 6809 / 6815 / 6832 / 6835 / 6901 / 6902 | 78 | The 15 pilots promised 2026-10-02 never arrived; the forged (-FG) rows need their own file (forged rule: no build from non-forged Air-Way rows). 6805 / 6806 / 6809 / 6815 / 6832 / 6835 / 6901 also need a new generator SPEC; 6901 / 6902 range bores are measured on the STEP (A14). | 3DF s3 + s4; BSL (pilot list); PS3 item 8 / 11; ANS18 A14 |
| ORFS straights FS2403 / FS2404 / FS6400 / FS6403 at -04 ... -20 | 59 | The male face-seal end on a STRAIGHT is measured only at -08 / -24 / -32 (FSM_MEAS); a forged leg has no flank / relief, so the FS6500 files do not cover it. One straight file per face-seal dash. | NSP20 "Downloads"; ORFSRM step 5 / step 7; gen_straight2 LIB_NEED["FSM"] |
| Forged (-FG) rows that need their own Brennan file | 45 | Forged parts with only non-forged Air-Way rows wait for their own Brennan -FG STEP (shape, and since Brennan = yes the sizes). | 3DF s2 / s3; PS3 item 11; RT "BUILD-NEAR" |
| ORFS adjustable-stud elbows / tees FS6801 / FS6802 / FS6803 / FS6804 | 34 | FS adjustable stud NWO_FS measured only at -08: one FS6801-NN-NN-NWO-FG per stud dash (the stud is dash 2 on FS6801 / FS6802 / FS6804, dash 3 on FS6803 - gen_tee SPEC legs). A -24 face-seal leg also needs FS6500-24-24-FG. | NSP20 "Downloads"; ORFSRM step 2 / 5; gen_tee NWO_FS |
| ORFS bulkhead elbows / tees FS2701 / FS2702 / FS2703 / FS2704 (+ -LN) at -04 ... -16 | 32 | Bulkhead leg FSBH_MEAS exists only at -08. One bulkhead file per dash. | NSP20 "Downloads"; ORFSRM step 5; gen_tee FSBH_MEAS |
| 6900 male ORB x female NPSM swivel straights | 21 | A3 answered (correct the table); lengths = Air-Way (Q-NEW-6900-LEN). No 6900 SPEC; 3DF s3 asks for the shape files 6900-08-08-O and 6900-32-32-O (-32: Brennan TFA p19 sizes). | ANS18 A3; 3DF s3; W2ST |
| -24 / -32 female pipe ports (tap drill, A9) | 18 | A9 answered "wait for a brennan step": BRENNAN_5405-24-24 and 5405-32-32 settle the -24 (1.72 / 1.70) and -32 (2.19 / 2.20) tap drill for all of these. 5406-C-24 / -C-32 are also on the shape list; 5652-32-32-32-32-FG / 5504-32-32-FG need their own file too; 5406-40-32 also needs its -40 male end measured (file on disk). | ANS18 A9; W2ST / W2TE rows.csv |
| ORFS flange straights / elbows FS1700 / FS1704 / FS1800 / FS1804 | 16 | Brennan Flange catalog sizes staged, bores (and code 62 head O on FS1800 / FS1804) missing -> own file per part; straight FS end via FS2403-NN-NN; code 62 heads via 1824-NN; new FS flange SPECs. | W3ORFS; STEPS16 "What is not in this list" |
| ORFS tube-end reducer FS2406 | 15 | Pilot FS2406-08-06 has no CAD at Brennan; FS2406-08-04 is the stand-in. FS2406-12-16 / -16-20 also lack collar D8 + bore (own file). The male end likely also needs the FS2403-NN-NN straight end of its dash (inference from the FSM rule). | NSP20; ORFSRM "Next"; W3ORFS |
| ORFS straight bulkhead union FS2700 (+ -LN) | 14 | Waits for the bulkhead files (as FS2701) and a new straight FS2700 SPEC; FS2700-08-08 = optional family pilot F15. FS2700-20-20: no OMi FS2701 size at -20 - its own file would be the source (inference). | ORFSRM "Next"; STEPS16 part 3 F15 |
| 6801-L / 6801-LL long adjustable elbows | 12 | Pilots 6801-L-08-08 / 6801-LL-08-08-NWO-FG (where the extra length goes, Q-NEW-FOLD-6801L) + own files of the MISSING sizes; then fold into 6801. | BSL; 3DF s3 / s4; PS3 item 7 |
| Code 62 flange straights 1800 | 12 | Collar dia / length, neck dia, bore only on each part's own file; code 62 head -12 ... -32 (1824-NN or Q-CODE62-CAT). (1800-08-08 is held for the FLATS sketch, below.) | W2FH rows.csv |
| Flange plugs 1724 (code 61) / 1824 (code 62) | 11 | Flange catalog prints the flange size only; length / shank / stub from each own file. The 1824 files also give the code 62 heads for 1800 / 1803 / 1804 / FS1800 / FS1804. | W2FH rows.csv |
| 6408-HHP hex-socket plugs | 11 | Head diameter has no source (OMi Body Diameter empty, no catalog column); socket depth Q-PLUG-SOCKDEPTH open. Own files named as wave 2 writes them (6408-H<dash>-O; 6408-H08-O is on disk) - confirm the Brennan part number. | W2ST rows.csv; OQ18 D |
| Forged code 61 flange elbows 1703 / 1704 -FG | 10 | Brennan catalog prints no bores; only the own file gives them (flange leg is in the batch-17 generator). 1703-08-08-FG / -32-32-FG: not in the catalog at all -> every size from the file. | W2FH rows.csv; 3DF s3 |
| Forged code 62 flange elbows 1803 / 1804 -FG | 10 | Own file (bores) + a code 62 head of that size (only -08 measured: FLG62_MEAS[8]) - the 1824-NN plugs, or Q-CODE62-CAT instead of the head files. | W2FH rows.csv; 3DF s3 / s4; OQ18 "New after the answers" |
| ORFS cap assembly FS0304-C-xx-ASY | 8 | No Air-Way source, no shape file; Brennan sells it as FS0304-C-08 (insert + nut); then a new SPEC. | ORFSRM step 7; NSP20; W3ORFS (FS0304-C-xx-ASY = Brennan FS0304-C-xx) |
| ORFS FS6402 (male face seal x female JIC swivel) | 7 | No Air-Way series; Brennan catalog sizes staged but bores D1 / D2 not printed; no SPEC; FS6402-12-12 L misprinted ("0.609"). Needs the FS2403 straight end of its dash + bores (own files or a per-dash bore transfer like Q-FS-XFER). | W3ORFS; OCT "No dimension source" (FS6402 Brennan only) |
| 6425 ORB x ORB unions | 6 | Brennan TFA p17 + OMi give length and hex; no SPEC, no dimension columns; one file per size (6425-08-08 has no Brennan file - shape from a sibling, inference). | W2ST rows.csv; 3DF "not to ask for" |
| ORFS rows with a missing cell only its own file has | 5 | FS6400-10-06-O / -12-20-O (stud length L9 + bores), FS6565-10-10 / -16-16 (swivel bores), FS7202-06-04-NWO-FG (BSPP thread, stud length, bores; new end type). Inference: Brennan = yes allows measuring the part's own STEP; else OMi. | W3ORFS rows.csv (missing_columns) |
| ORFS 45 deg swivel elbow FS6502 -06 / -10 / -12 / -16 | 4 | Generator corner-puck check blocks them; a FS6502 STEP shows where the swivel sits on a 45 deg body. | ORFSRM step 7; NSP20 |
| 3051 | 4 | ASSUMED rows waiting for a shape file; 3DF s3 lists "3051" without a size. | 3DF s3; unblock rows.csv |
| ORFS FS6809 (90 deg swivel x adjustable stud) | 3 | No SPEC yet ("no -08 row, not given a SPEC"); family pilot F12 FS6809-06-06-NWO-FG + the stud files. | ORFSRM step 3; STEPS16 F12 |
| ORFS -24 forged leg / swivel (FS6500-24-24-FG, FS2500-24-xx-FG) | 3 | FSMF / FSSW measured -04 ... -20 only. | NSP20 "Downloads"; ORFSRM step 5 |
| ORFS FS2503-08-08-FG / -10-08-FG | 2 | Flats at / above the thread: need the family pilot F13 FS2503-08-06-FG ("blocked on purpose"). (-10-08: same reason assumed - check.) | ORFSRM step 2; STEPS16 F13 |
| 0304-C-02 / 0306-02 (-02 JIC cap / locknut) | 2 | Data complete (OMi = Brennan catalog); the generator has no female -02 JIC geometry - needs the own file. | W2ST rows.csv |
| Air-Way misprints a STEP settles | 2 | 6405-32-24-O: Air-Way D3 2.38 misprint; 5405-08-16: row contradicts its part number ("Brennan tiebreak"). | PS3 item 9; RT $COMMENT |
| 5404-L-04X3.000 / X4.000 | 2 | Their own Brennan file is the only size source. | 3DF s2 |
| 6420-12-12 | 1 | OMi length 1.730 does not fit the library ports (also OMi question 7); its own file settles the body. | QOMI 1.7; merged.json 6420-12-12-PORTS |
| 2404-32-48 | 1 | NPTF -48 end length unmeasured (no -48 male end in the library). Inference: its own file. | RT $COMMENT; PS5 2026-10-09 |
| 2505-16-16-FG (port deeper than the short leg) | 1 | Generator blocks: port depth 1.14 >= leg 1.12 (Q-ANGLED-P1). A15: settle from Brennan where it answers -> its own file (3DF s3). | ANS18 A15; W2TE rows.csv |

## (b) Dimensions missing everywhere - ask OMi - 291 parts

| Group | Parts | What unblocks it | Source |
|---|---|---|---|
| Compression (bite type) C0318 C0319 C2402 C2403 C2404 C2405 C2500 C2501 C2502 C2601 C6801 (incl. -M1 body-only) | 230 | No Air-Way series; Brennan prints only V0318 / V0319. OMi drawings or another source. | OCT "No dimension source at all"; QOMI 1.3; P2535 D_compression |
| Parts with no Air-Way row, no Brennan catalog row and no Brennan file | 29 | Brennan has no file (user 2026-10-02: "will ask OMi for drawings") or the dropped-adapter rows with no source; OMi drawings / dimensions needed. 2700 / 2700-LN: Air-Way, Brennan and OMi give nothing. | PS3 item 2; 3DF "Not to ask for"; R77 "no source"; W2ST / W3AD rows.csv |
| Test gauge TGT-6504 / TGT-FS2406 | 12 | Swivel unions with a -04 test port; Air-Way's test points are a different (metric) part. | OCT; QOMI 1.3 |
| 4005 flange O-rings | 9 | Q-NEW-4005CODE: code 61 or 62? AS568 size or I.D. x cross-section, material, hardness. | QOMI 1.1; OQ18 B |
| ORFS parts with no usable source | 7 | FS6403-24-24, FS6505-06-06 / -10-08, FS2406-06-08 / -10-10: no Air-Way row and Brennan does not print them; FS0304-C-32-ASY: no source; FS0319-24: Air-Way contradicts itself (1.71 vs its FF2407-24 2.00; Brennan 1.910) - OMi question 6. | RT $COMMENT (stage_orfs); QOMI 1.4 / 1.6; W3ORFS |
| Flareless nut 0618 / sleeve 0619 | 4 | Sizes and shape from OMi; is it Brennan V0318 / V0319 (Q-NEW-F3-FLARELESS-ALIAS)? Shape files V0318-08 / V0319-08 (user download). 0618-06 is also one of the 6 "no source" adapters. | QOMI 1.2; NT "Flareless"; R77 |

## (c) User decision - 123 parts

| Group | Parts | What unblocks it | Source |
|---|---|---|---|
| Bent-tube elbows 1703 / 1704 / 1803 / 1804 -TUBE and 6701 | 68 | No source for tube OD, wall / bore, bend radius, end-hex length (Brennan prints only the two lengths + hex). Open: which source - OMi, Air-Way's 3D models, or each part's own Brennan STEP? 1803 / 1804 also need code 62 heads -12 ... -32 (1824 files or Q-CODE62-CAT); 3 1704 rows conflict (Air-Way M3 / N4 vs Brennan); gen_bent is staged, not merged. | W3BT REPORT; NSP19 "Still open"; OQ18 "New after the answers"; QOMI 1.9 |
| Forged ORFS rows where Air-Way's plain row differs from Brennan's forged row | 21 | User 2026-10-15: those "stay MISSING"; since Brennan = yes (2026-10-18) Brennan's forged catalog values could fill them, but wave 3 did not use them. Question (not yet asked in the docs): use Brennan's forged values for these 21 rows? Then the missing stud lengths / bulkhead cells come from the STEPs listed. | PS5 2026-10-15; W3ORFS "Conflicts" (36 forged rows) |
| 5406-HHP / 5406-SHP plugs | 13 | Q-PLUG-SOCKDEPTH (socket depth from the Brennan pilot ratio, or OMi) and Q-PLUG-SQHEAD (square-head length rule); 5406-HHP-01 also Q-NEW-NPT01. | OQ18 D; NSP19; W2ST rows.csv |
| ORFS plug FS2408 | 8 | Q-FS2408-HOLE: solid or with Air-Way's blind hole (OMi question 5; "built solid meanwhile", README: "FS2408 after the hole decision"). Go ahead solid now? Then a SPEC (and likely the FS2403 straight end per dash - inference). | QOMI 1.5; ORFSRM "Next"; STEPS16 S3 |
| FS6400-L / FS6801-L long variants | 4 | No shape source for where the extra length goes - listed as still open. | NSP20 "Still open"; ORFSRM step 1 |
| 2502-08-04-FG / -12-08-FG | 2 | Legs OMi / Brennan vs MS51506 - your call; also needs the 2502 generator SPEC (A7). | OQ18 D; W3AD |
| 2505-04-04-FG (port deeper than the short leg) | 1 | Generator blocks: port depth 0.67 >= leg 0.62 (Q-ANGLED-P1); no Brennan file listed for it -> cap the port at leg - 0.05 (logged assumption) or wait for OMi port data? | OQ18 A15; W3AD rows.csv |
| 6801-05-05-NWO-FG | 1 | Air-Way + Brennan 1.13 vs MS51527 1.090 (recommended 1.13). | OQ18 D |
| 2501-40-40-FG | 1 | -40 JIC end like Brennan (1.335 / 0.140) or the standard (recommended Brennan). | OQ18 D |
| 6565-32-32 | 1 | Air-Way thread "2 1/2-2 1/2": use the part number's thread (recommended yes). STEP on disk. | OQ18 D; PS3 item 3 |
| 6404-08-12 | 1 | Port drill 0.68 or 0.97 (recommended 0.68). | OQ18 D |
| 6900-05-04-O | 1 | Air-Way W4 1.30 vs L2 1.19 (recommended keep W4; Brennan prints a third option). | OQ18 D |
| 2702-LN-12-12-FG | 1 | Air-Way -LN row prints -16-looking values ("flag for review"); with A10 (LN = plain part) model it as the built 2702-12-12-FG? (inference) | RT $COMMENT; ANS18 A10 |

## (d) Generator / table work only (no new data) - 94 parts

| Group | Parts | What unblocks it | Source |
|---|---|---|---|
| Rows whose question was answered on 2026-10-18 - apply and regenerate | 25 | 2705 / 2706: A8 I1 per size (+ A10 -LN); 6504: A12 swivel offset; 6506 / 6503-04-04 / -12-12 / 6405-32-16-O: A1 tap drill; 6410: A11 cap the bore + D3 per size (edits listed in wave2 straight test/edits_A11.csv), A18 groove 0.125. | ANS18; W2ST rows.csv; unblock rows.csv gates |
| New review table / SPEC from data already in hand | 14 | 3474 (family staged in newmasters_20261002/work/3474, never merged; Brennan TFA p9), 2613-04-04-04-FG (Brennan TFA p53), 6316 x3 (Brennan TFA p13; no table), 6420-08-08 (OMi real length 1.5, STEP on disk). | W2ST / W3AD rows.csv; NSP19 "prepare the 3474 family" |
| 0319 JIC tube sleeves | 12 | A2: included; sleeve type proven on TEST rows, BRENNAN_0319-08 on disk; other sizes were shape-SCALED in the test - per-size files only if that is not accepted. | ANS18 A2; NT |
| Own Brennan file already in 09_STEP_FILES - measure and fill | 11 | 5601-06-06-06, 5603-08-08-08, 5652-08-08-08-08, 6603-06-06-06, 6606-06-06-06, 1502-08-08, 2501-LL-08-08, 2505-08-08, 5505-08-08 (-FG), 2404-L-32-32 (values prepared; held by Q-HANDMADE, which looks moot now that 2404 is generated - inference), 6506-12-14 (L17 blank on Air-Way). | 09_STEP_FILES listing; W2ST / W2TE rows.csv |
| 2500 / 2502 / 2603 rows that need the hand-made HX masters moved to the generator | 9 | A7: "move 2500HX / 2502HX / 2603HX to the generator later". | ANS18 A7; W3AD rows.csv |
| Generator geometry blocks / capabilities now merged | 6 | 1502-04-04-FG (body face inside the hex corner), 2406-16-04 (port wall), 6502-16-12-FG (generator work), 5501-24-24 / -32-32-FG and 5503-02-02-FG (gate was the angled-helix capability, merged in batch 17 - regenerate and check). | PS3 item 9; unblock rows.csv; B17 |
| Rows staged with Brennan catalog sizes but still MISSING | 5 | 1504-08-08 / -12-12 / -16-16-FG, 6807-16-16 / -20-20-NWO-FG: wave 3 had no generator for them; batch 17 has 1504 / 6807 SPECs - set ASSUMED (marked BRENNAN) and generate (check). | W3AD rows.csv |
| 5404-N long nipples in OMi's part-number form | 4 | A4 answered; generator reads only the Air-Way "5404-N-6-6 X 1" form (KeyError "no dash pair") + the 5404N -06 thread fix (held root). | W3AD rows.csv; ANS18 A4; B17 |
| Air-Way value not buildable -> Brennan (user Q1 2026-10-20) | 4 | 2408-14 hex 1.125 < its thread (Brennan 1.25), 1501-24-24-FG nut 1.88 (2.125), 6802-04-06-NWO-FG locknut 0.56 (0.6875), 1501-04-02-FG bore vs -02 stem tip - apply the rule and tell the user the cells. | CLAUDE.md rule (Q1); OQ18 D; PS3 item 9 |
| FS2500-12-08-FG / -16-12-FG | 2 | Mixed leg-shape rows have no master yet (one sketch per master). | ORFSRM step 5 |
| 2404-40-40 | 1 | -40 NPTF end length: Brennan-measured -40 threads accepted (Q-NEW-ASME40); 5404-40-40 / 5000-40-40 / 2501-40-40-FG files on disk. | PS5; 09_STEP_FILES |
| 1603-08-08-08-FG | 1 | A14 bores staged (tools/_out/a14_1603bore_20261020/) - ships with the next batch. | NSP20 item 1 |

## (e) Out of scope - 30 parts

| Group | Parts | What unblocks it | Source |
|---|---|---|---|
| Kits 1901 / 1902 / 1927 | 30 | Out of scope (kits). | P2535 F_kits; NSP18 table |

## STEP download list (save as `09_STEP_FILES/BRENNAN_<part number>.stp`)

Not on disk today (checked against `09_STEP_FILES`). "Parts" = not-yet parts that name the file (a part can need several files). Files Brennan does not have (3D_FILES_NEEDED "not to ask for") are not listed.

### A9 tap drill -24 / -32 (frees the whole A9 group) - 2 files

| File (Brennan part number) | Parts it is needed for |
|---|---|
| 5405-24-24 | 10: 2502-24-24-FG, 5000-24-20, 5405-16-24, 5406-C-24, 5503-24-24-FG, 5504-24-24-FG ... |
| 5405-32-32 | 8: 2502-32-32-FG, 5405-20-32, 5406-40-32, 5406-C-32, 5503-32-32-FG, 5504-32-32-FG ... |

### ORFS - 47 files

| File (Brennan part number) | Parts it is needed for |
|---|---|
| FS2403-12-12 | 16: FS1700-12-12, FS1800-12-12, FS2403-12-08, FS2403-12-10, FS2403-12-12, FS2403-16-12 ... |
| FS2406-08-04 | 15: FS2406-06-04, FS2406-08-04, FS2406-08-06, FS2406-10-06, FS2406-10-08, FS2406-12-06 ... |
| FS2403-06-06 | 13: FS2403-06-04, FS2403-06-06, FS2403-08-06, FS2404-06-04, FS2404-06-06, FS2404-06-08 ... |
| FS2403-16-16 | 13: FS1700-16-16, FS1800-16-16, FS2403-16-12, FS2403-16-16, FS2403-20-16, FS2404-16-12 ... |
| FS2403-04-04 | 12: FS2403-04-04, FS2403-06-04, FS2404-04-02, FS2404-04-04, FS2404-04-06, FS6400-04-04-O ... |
| FS2403-20-20 | 12: FS1700-20-20, FS1800-20-20, FS2403-20-16, FS2403-20-20, FS2403-24-20, FS2404-20-16 ... |
| FS2403-10-10 | 11: FS2403-10-08, FS2403-10-10, FS2403-12-10, FS2404-10-08, FS2404-10-12, FS6400-10-06-O ... |
| FS2701-06-06-FG | 11: FS2700-06-06, FS2700-08-06, FS2700-LN-06-06, FS2701-06-06-FG, FS2701-LN-06-06-FG, FS2702-06-06-FG ... |
| FS2701-04-04-FG | 10: FS2700-04-04, FS2700-LN-04-04, FS2701-04-04-FG, FS2701-LN-04-04-FG, FS2702-04-04-FG, FS2702-LN-04-04-FG ... |
| FS2701-12-12-FG | 10: FS2700-12-12, FS2700-LN-12-12, FS2701-12-12-FG, FS2701-LN-12-12-FG, FS2702-12-12-FG, FS2702-LN-12-12-FG ... |
| FS2701-16-16-FG | 10: FS2700-16-16, FS2700-LN-16-16, FS2701-16-16-FG, FS2701-LN-16-16-FG, FS2702-16-16-FG, FS2702-LN-16-16-FG ... |
| FS6801-06-06-NWO-FG | 10: FS6801-04-06-NWO-FG, FS6801-06-06-NWO-FG, FS6801-08-06-NWO-FG, FS6802-04-06-NWO-FG, FS6802-06-06-NWO-FG, FS6802-08-06-NWO-FG ... |
| FS6801-12-12-NWO-FG | 10: FS6801-08-12-NWO-FG, FS6801-10-12-NWO-FG, FS6801-12-12-NWO-FG, FS6801-16-12-NWO-FG, FS6802-08-12-NWO-FG, FS6802-12-12-NWO-FG ... |
| FS0304-C-08 | 8: FS0304-C-04-ASY, FS0304-C-06-ASY, FS0304-C-08-ASY, FS0304-C-10-ASY, FS0304-C-12-ASY, FS0304-C-16-ASY ... |
| FS2701-10-10-FG | 8: FS2700-10-10, FS2700-LN-10-10, FS2701-10-10-FG, FS2701-LN-10-10-FG, FS2702-10-10-FG, FS2702-LN-10-10-FG ... |
| FS6801-10-10-NWO-FG | 8: FS6801-06-10-NWO-FG, FS6801-08-10-NWO-FG, FS6801-10-10-NWO-FG, FS6801-12-10-NWO-FG, FS6802-06-10-NWO-FG, FS6802-08-10-NWO-FG ... |
| FS6801-16-16-NWO-FG | 8: FS6801-12-16-NWO-FG, FS6801-16-16-NWO-FG, FS6801-20-16-NWO-FG, FS6802-12-16-NWO-FG, FS6802-16-16-NWO-FG, FS6803-16-16-16-NWO-FG ... |
| FS6801-04-04-NWO-FG | 7: FS6801-04-04-NWO-FG, FS6801-06-04-NWO-FG, FS6802-04-04-NWO-FG, FS6802-06-04-NWO-FG, FS6803-04-04-04-NWO-FG, FS6804-04-04-04-NWO-FG ... |
| FS6809-06-06-NWO-FG | 7: FS6809-04-04-NWO-FG, FS6809-06-06-NWO-FG, FS6809-08-08-NWO-FG, FS6809-10-10-NWO-FG, FS6809-12-12-NWO-FG, FS6809-16-16-NWO-FG ... |
| FS6500-24-24-FG | 6: FS1704-24-24-FG, FS1804-24-24-FG, FS2500-24-20-FG, FS2500-24-24-FG, FS6500-24-24-FG, FS6801-24-24-NWO-FG |
| FS6502-06-06-FG | 5: FS6502-04-04-FG, FS6502-06-06-FG, FS6502-10-10-FG, FS6502-12-12-FG, FS6502-16-16-FG |
| FS6801-20-20-NWO-FG | 4: FS6801-16-20-NWO-FG, FS6801-20-20-NWO-FG, FS6802-20-20-NWO-FG, FS6809-20-20-NWO-FG |
| FS2503-08-06-FG | 2: FS2503-08-08-FG, FS2503-10-08-FG |
| FS1700-12-12 | 1: FS1700-12-12 |
| FS1700-16-16 | 1: FS1700-16-16 |
| FS1700-20-20 | 1: FS1700-20-20 |
| FS1700-24-24 | 1: FS1700-24-24 |
| FS1704-12-12-FG | 1: FS1704-12-12-FG |
| FS1704-16-16-FG | 1: FS1704-16-16-FG |
| FS1704-20-20-FG | 1: FS1704-20-20-FG |
| FS1704-24-24-FG | 1: FS1704-24-24-FG |
| FS1800-12-12 | 1: FS1800-12-12 |
| FS1800-16-16 | 1: FS1800-16-16 |
| FS1800-20-20 | 1: FS1800-20-20 |
| FS1800-24-24 | 1: FS1800-24-24 |
| FS1804-12-12-FG | 1: FS1804-12-12-FG |
| FS1804-16-16-FG | 1: FS1804-16-16-FG |
| FS1804-20-20-FG | 1: FS1804-20-20-FG |
| FS1804-24-24-FG | 1: FS1804-24-24-FG |
| FS2406-12-16 | 1: FS2406-12-16 |
| FS2406-16-20 | 1: FS2406-16-20 |
| FS6400-10-06-O | 1: FS6400-10-06-O |
| FS6400-12-20-O | 1: FS6400-12-20-O |
| FS6565-10-10 | 1: FS6565-10-10 |
| FS6565-16-16 | 1: FS6565-16-16 |
| FS6801-24-24-NWO-FG | 1: FS6801-24-24-NWO-FG |
| FS7202-06-04-NWO-FG | 1: FS7202-06-04-NWO-FG |

### Code 62 heads = the 1824 flange plugs - 5 files

| File (Brennan part number) | Parts it is needed for |
|---|---|
| 1824-16 | 16: 1800-16-12, 1800-16-16, 1800-16-20, 1800-16-24, 1803-16-12-TUBE, 1803-16-16-FG ... |
| 1824-20 | 15: 1800-20-16, 1800-20-20, 1800-20-24, 1803-20-12-TUBE, 1803-20-16-TUBE, 1803-20-20-FG ... |
| 1824-12 | 13: 1800-12-12, 1800-12-16, 1803-12-12-FG, 1803-12-12-TUBE, 1803-12-16-TUBE, 1803-12-20-TUBE ... |
| 1824-24 | 13: 1800-24-20, 1800-24-24, 1803-24-20-TUBE, 1803-24-24-FG, 1803-24-24-TUBE, 1804-24-16-TUBE ... |
| 1824-32 | 6: 1800-32-32, 1803-32-32-FG, 1803-32-32-TUBE, 1804-32-32-FG, 1804-32-32-TUBE, 1824-32 |

### Other (own forged files, pilots, flange parts, plugs) - 184 files

| File (Brennan part number) | Parts it is needed for |
|---|---|
| 6900-08-08-O | 21: 6900-04-02-O, 6900-04-04-O, 6900-04-06-O, 6900-06-04-O, 6900-06-06-O, 6900-06-08-O ... |
| 6901-06-08-NWO-FG | 21: 6901-04-04-NWO-FG, 6901-04-06-NWO-FG, 6901-06-04-NWO-FG, 6901-06-06-NWO-FG, 6901-06-08-NWO-FG, 6901-08-06-NWO-FG ... |
| 6805-08-08-NWO-FG | 12: 6805-04-02-NWO-FG, 6805-04-04-NWO-FG, 6805-06-04-NWO-FG, 6805-06-06-NWO-FG, 6805-08-06-NWO-FG, 6805-08-08-NWO-FG ... |
| 6806-08-08-NWO-FG | 11: 6806-04-04-NWO-FG, 6806-06-04-NWO-FG, 6806-06-06-NWO-FG, 6806-08-06-NWO-FG, 6806-08-08-NWO-FG, 6806-10-08-NWO-FG ... |
| 6902-08-08-NWO-FG | 9: 6902-04-04-NWO-FG, 6902-06-04-NWO-FG, 6902-06-06-NWO-FG, 6902-08-06-NWO-FG, 6902-08-08-NWO-FG, 6902-10-08-NWO-FG ... |
| 6809-10-10-NWO-FG | 7: 6809-04-04-NWO-FG, 6809-06-06-NWO-FG, 6809-08-08-NWO-FG, 6809-10-10-NWO-FG, 6809-12-12-NWO-FG, 6809-16-16-NWO-FG ... |
| 6801-L-08-08-NWO-FG | 6: 6801-L-04-04-NWO-FG, 6801-L-06-06-NWO-FG, 6801-L-08-08-NWO-FG, 6801-L-12-12-NWO-FG, 6801-L-16-16-NWO-FG, 6801-L-20-20-NWO-FG |
| 6801-LL-08-08-NWO-FG | 6: 6801-LL-04-04-NWO-FG, 6801-LL-06-06-NWO-FG, 6801-LL-08-08-NWO-FG, 6801-LL-12-12-NWO-FG, 6801-LL-16-16-NWO-FG, 6801-LL-20-20-NWO-FG |
| 6815-08-08-NWO-FG | 6: 6815-04-04-NWO-FG, 6815-06-06-NWO-FG, 6815-08-08-NWO-FG, 6815-10-10-NWO-FG, 6815-12-12-NWO-FG, 6815-16-16-NWO-FG |
| 6807-08-08-NWO-FG | 4: 6807-04-04-NWO-FG, 6807-08-06-NWO-FG, 6807-08-08-NWO-FG, 6807-12-12-NWO-FG |
| 6832-08-08-08-NWO-FG | 4: 6832-04-04-04-NWO-FG, 6832-06-06-06-NWO-FG, 6832-08-08-08-NWO-FG, 6832-16-16-16-NWO-FG |
| 6835-08-08-08-NWO-FG | 4: 6835-04-04-04-NWO-FG, 6835-06-06-06-NWO-FG, 6835-08-08-08-NWO-FG, 6835-12-12-12-NWO-FG |
| 0304-C-02 | 1: 0304-C-02 |
| 0306-02 | 1: 0306-02 |
| 1504-24-24-FG | 1: 1504-24-24-FG |
| 1504-32-32-FG | 1: 1504-32-32-FG |
| 1703-08-08-FG | 1: 1703-08-08-FG |
| 1703-12-12-FG | 1: 1703-12-12-FG |
| 1703-16-16-FG | 1: 1703-16-16-FG |
| 1703-20-20-FG | 1: 1703-20-20-FG |
| 1703-32-32-FG | 1: 1703-32-32-FG |
| 1704-08-08-FG | 1: 1704-08-08-FG |
| 1704-12-12-FG | 1: 1704-12-12-FG |
| 1704-16-16-FG | 1: 1704-16-16-FG |
| 1704-20-20-FG | 1: 1704-20-20-FG |
| 1704-32-32-FG | 1: 1704-32-32-FG |
| 1724-12 | 1: 1724-12 |
| 1724-16 | 1: 1724-16 |
| 1724-20 | 1: 1724-20 |
| 1724-24 | 1: 1724-24 |
| 1724-32 | 1: 1724-32 |
| 1724-40 | 1: 1724-40 |
| 1800-12-12 | 1: 1800-12-12 |
| 1800-12-16 | 1: 1800-12-16 |
| 1800-16-12 | 1: 1800-16-12 |
| 1800-16-16 | 1: 1800-16-16 |
| 1800-16-20 | 1: 1800-16-20 |
| 1800-16-24 | 1: 1800-16-24 |
| 1800-20-16 | 1: 1800-20-16 |
| 1800-20-20 | 1: 1800-20-20 |
| 1800-20-24 | 1: 1800-20-24 |
| 1800-24-20 | 1: 1800-24-20 |
| 1800-24-24 | 1: 1800-24-24 |
| 1800-32-32 | 1: 1800-32-32 |
| 1803-12-12-FG | 1: 1803-12-12-FG |
| 1803-16-16-FG | 1: 1803-16-16-FG |
| 1803-20-20-FG | 1: 1803-20-20-FG |
| 1803-24-24-FG | 1: 1803-24-24-FG |
| 1803-32-32-FG | 1: 1803-32-32-FG |
| 1804-12-12-FG | 1: 1804-12-12-FG |
| 1804-16-16-FG | 1: 1804-16-16-FG |
| 1804-20-20-FG | 1: 1804-20-20-FG |
| 1804-24-24-FG | 1: 1804-24-24-FG |
| 1804-32-32-FG | 1: 1804-32-32-FG |
| 2404-32-48 (inferred: a Brennan file with a -48 male NPTF end) | 1: 2404-32-48 |
| 2505-16-16-FG | 1: 2505-16-16-FG |
| 3051 (one pilot; 3DF lists "3051" without a size) | 1: 3051-04-04 |
| 5404-L-04X3.000 | 1: 5404-L-04X3.000 |
| 5404-L-04X4.000 | 1: 5404-L-04X4.000 |
| 5405-08-16 | 1: 5405-08-16 |
| 5503-04-02-FG | 1: 5503-04-02-FG |
| 5503-06-04-FG | 1: 5503-06-04-FG |
| 5503-08-06-FG | 1: 5503-08-06-FG |
| 5503-12-08-FG | 1: 5503-12-08-FG |
| 5503-16-12-FG | 1: 5503-16-12-FG |
| 5504-32-32-FG | 1: 5504-32-32-FG |
| 5505-02-02-FG | 1: 5505-02-02-FG |
| 5505-06-06-FG | 1: 5505-06-06-FG |
| 5505-12-12-FG | 1: 5505-12-12-FG |
| 5505-16-16-FG | 1: 5505-16-16-FG |
| 5602-02-02-02-FG | 1: 5602-02-02-02-FG |
| 5602-06-06-06-FG | 1: 5602-06-06-06-FG |
| 5602-12-12-12-FG | 1: 5602-12-12-12-FG |
| 5602-16-16-16-FG | 1: 5602-16-16-16-FG |
| 5602-20-20-20-FG | 1: 5602-20-20-20-FG |
| 5602-24-24-24-FG | 1: 5602-24-24-24-FG |
| 5602-32-32-32-FG | 1: 5602-32-32-32-FG |
| 5604-02-02-02-FG | 1: 5604-02-02-02-FG |
| 5604-12-12-12-FG | 1: 5604-12-12-12-FG |
| 5604-16-16-16-FG | 1: 5604-16-16-16-FG |
| 5604-20-20-20-FG | 1: 5604-20-20-20-FG |
| 5604-32-32-32-FG | 1: 5604-32-32-32-FG |
| 5605-02-02-02-FG | 1: 5605-02-02-02-FG |
| 5605-12-12-12-FG | 1: 5605-12-12-12-FG |
| 5605-16-16-16-FG | 1: 5605-16-16-16-FG |
| 5605-20-20-20-FG | 1: 5605-20-20-20-FG |
| 5605-32-32-32-FG | 1: 5605-32-32-32-FG |
| 5652-32-32-32-32-FG | 1: 5652-32-32-32-32-FG |
| 6405-32-24-O | 1: 6405-32-24-O |
| 6408-H02-O | 1: 6408-HHP-02-O |
| 6408-H03-O | 1: 6408-HHP-03-O |
| 6408-H04-O | 1: 6408-HHP-04-O |
| 6408-H05-O | 1: 6408-HHP-05-O |
| 6408-H06-O | 1: 6408-HHP-06-O |
| 6408-H10-O | 1: 6408-HHP-10-O |
| 6408-H12-O | 1: 6408-HHP-12-O |
| 6408-H16-O | 1: 6408-HHP-16-O |
| 6408-H20-O | 1: 6408-HHP-20-O |
| 6408-H24-O | 1: 6408-HHP-24-O |
| 6408-H32-O | 1: 6408-HHP-32-O |
| 6420-12-12 | 1: 6420-12-12 |
| 6425-04-04 | 1: 6425-04-04 |
| 6425-06-06 | 1: 6425-06-06 |
| 6425-10-10 | 1: 6425-10-10 |
| 6425-12-12 | 1: 6425-12-12 |
| 6425-16-16 | 1: 6425-16-16 |
| 6503-06-06-FG | 1: 6503-06-06-FG |
| 6503-16-16-FG | 1: 6503-16-16-FG |
| 6566-16-16-FG | 1: 6566-16-16-FG |
| 6603-16-16-16-FG | 1: 6603-16-16-16-FG |
| 6606-12-12-12-FG | 1: 6606-12-12-12-FG |
| 6801-08-04-NWO-FG | 1: 6801-08-04-NWO-FG |
| 6801-08-16-NWO-FG | 1: 6801-08-16-NWO-FG |
| 6801-12-20-NWO-FG | 1: 6801-12-20-NWO-FG |
| 6801-16-24-NWO-FG | 1: 6801-16-24-NWO-FG |
| 6801-24-16-NWO-FG | 1: 6801-24-16-NWO-FG |
| 6801-L-16-16-NWO-FG | 1: 6801-L-16-16-NWO-FG |
| 6801-L-20-20-NWO-FG | 1: 6801-L-20-20-NWO-FG |
| 6801-LL-12-12-NWO-FG | 1: 6801-LL-12-12-NWO-FG |
| 6801-LL-16-16-NWO-FG | 1: 6801-LL-16-16-NWO-FG |
| 6801-LL-20-20-NWO-FG | 1: 6801-LL-20-20-NWO-FG |
| 6802-06-10-NWO-FG | 1: 6802-06-10-NWO-FG |
| 6802-08-12-NWO-FG | 1: 6802-08-12-NWO-FG |
| 6803-08-08-06-NWO-FG | 1: 6803-08-08-06-NWO-FG |
| 6803-08-08-10-NWO-FG | 1: 6803-08-08-10-NWO-FG |
| 6803-24-24-24-NWO-FG | 1: 6803-24-24-24-NWO-FG |
| 6804-24-24-24-NWO-FG | 1: 6804-24-24-24-NWO-FG |
| 6805-04-02-NWO-FG | 1: 6805-04-02-NWO-FG |
| 6805-04-04-NWO-FG | 1: 6805-04-04-NWO-FG |
| 6805-06-06-NWO-FG | 1: 6805-06-06-NWO-FG |
| 6805-10-08-NWO-FG | 1: 6805-10-08-NWO-FG |
| 6805-12-08-NWO-FG | 1: 6805-12-08-NWO-FG |
| 6805-16-12-NWO-FG | 1: 6805-16-12-NWO-FG |
| 6805-16-16-NWO-FG | 1: 6805-16-16-NWO-FG |
| 6805-20-20-NWO-FG | 1: 6805-20-20-NWO-FG |
| 6806-06-04-NWO-FG | 1: 6806-06-04-NWO-FG |
| 6806-06-06-NWO-FG | 1: 6806-06-06-NWO-FG |
| 6806-08-06-NWO-FG | 1: 6806-08-06-NWO-FG |
| 6806-10-08-NWO-FG | 1: 6806-10-08-NWO-FG |
| 6806-12-08-NWO-FG | 1: 6806-12-08-NWO-FG |
| 6806-12-12-NWO-FG | 1: 6806-12-12-NWO-FG |
| 6806-16-16-NWO-FG | 1: 6806-16-16-NWO-FG |
| 6806-20-20-NWO-FG | 1: 6806-20-20-NWO-FG |
| 6806-24-24-NWO-FG | 1: 6806-24-24-NWO-FG |
| 6807-04-04-NWO-FG | 1: 6807-04-04-NWO-FG |
| 6807-08-06-NWO-FG | 1: 6807-08-06-NWO-FG |
| 6807-12-12-NWO-FG | 1: 6807-12-12-NWO-FG |
| 6809-12-12-NWO-FG | 1: 6809-12-12-NWO-FG |
| 6809-16-16-NWO-FG | 1: 6809-16-16-NWO-FG |
| 6809-20-20-NWO-FG | 1: 6809-20-20-NWO-FG |
| 6810-12-12-NWO-FG | 1: 6810-12-12-NWO-FG |
| 6815-04-04-NWO-FG | 1: 6815-04-04-NWO-FG |
| 6815-06-06-NWO-FG | 1: 6815-06-06-NWO-FG |
| 6815-10-10-NWO-FG | 1: 6815-10-10-NWO-FG |
| 6815-12-12-NWO-FG | 1: 6815-12-12-NWO-FG |
| 6815-16-16-NWO-FG | 1: 6815-16-16-NWO-FG |
| 6832-04-04-04-NWO-FG | 1: 6832-04-04-04-NWO-FG |
| 6832-06-06-06-NWO-FG | 1: 6832-06-06-06-NWO-FG |
| 6832-16-16-16-NWO-FG | 1: 6832-16-16-16-NWO-FG |
| 6835-04-04-04-NWO-FG | 1: 6835-04-04-04-NWO-FG |
| 6835-06-06-06-NWO-FG | 1: 6835-06-06-06-NWO-FG |
| 6835-12-12-12-NWO-FG | 1: 6835-12-12-12-NWO-FG |
| 6900-32-32-O | 1: 6900-32-32-O |
| 6901-04-04-NWO-FG | 1: 6901-04-04-NWO-FG |
| 6901-04-06-NWO-FG | 1: 6901-04-06-NWO-FG |
| 6901-10-12-NWO-FG | 1: 6901-10-12-NWO-FG |
| 6901-12-06-NWO-FG | 1: 6901-12-06-NWO-FG |
| 6901-12-08-NWO-FG | 1: 6901-12-08-NWO-FG |
| 6901-12-12-NWO-FG | 1: 6901-12-12-NWO-FG |
| 6901-12-16-NWO-FG | 1: 6901-12-16-NWO-FG |
| 6901-16-12-NWO-FG | 1: 6901-16-12-NWO-FG |
| 6901-16-16-NWO-FG | 1: 6901-16-16-NWO-FG |
| 6901-20-16-NWO-FG | 1: 6901-20-16-NWO-FG |
| 6901-20-20-NWO-FG | 1: 6901-20-20-NWO-FG |
| 6901-24-24-NWO-FG | 1: 6901-24-24-NWO-FG |
| 6901-32-32-NWO-FG | 1: 6901-32-32-NWO-FG |
| 6902-04-04-NWO-FG | 1: 6902-04-04-NWO-FG |
| 6902-06-04-NWO-FG | 1: 6902-06-04-NWO-FG |
| 6902-06-06-NWO-FG | 1: 6902-06-06-NWO-FG |
| 6902-08-06-NWO-FG | 1: 6902-08-06-NWO-FG |
| 6902-10-08-NWO-FG | 1: 6902-10-08-NWO-FG |
| 6902-10-12-NWO-FG | 1: 6902-10-12-NWO-FG |
| 6902-16-16-NWO-FG | 1: 6902-16-16-NWO-FG |
| 6902-24-24-NWO-FG | 1: 6902-24-24-NWO-FG |

### Flareless shape (with OMi sizes) - 2 files

| File (Brennan part number) | Parts it is needed for |
|---|---|
| V0318-08 | 2: 0618-06, 0618-08 |
| V0319-08 | 2: 0619-06, 0619-08 |

Optional, from the docs: Air-Way 3D models of the ORFS pilots (S2, `AIRWAY_<item>.stp`, your 3DContentCentral sign-in); 1704-16-16 / 1803-16-16 / 6701-08-08 (bent-tube shape checks, 3D_FILES_NEEDED s4); FS6565-08-08 already received.

## Questions for OMi (from `10_DRAWINGS/for_OMi_LATER/QUESTIONS_FOR_OMi.md`, still unsent, + this count)

1. Compression C... (230 parts, incl. -M1 body-only) and test gauge TGT (12): dimensions or supplier drawings (QOMI 1.3).
2. 4005 flange O-rings (9): code 61 or 62, AS568 size or I.D. x cross-section, material, hardness (QOMI 1.1).
3. Flareless 0618 / 0619 (4): sizes and shape; same part as Brennan V0318 / V0319? (QOMI 1.2).
4. Drawings / dimensions for the parts Brennan has no file for and nobody prints: 1405-20-24, 1803-08-08-FG, 2403-06-02, 2406-06-12, 2502-20-16-FG, 2613-08-08-08-FG, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-04-02, 2700-LN-08-06, 2700-LN-10-08, 2700-LN-12-10, 5404-L-04X2.000, 5404-R-04-04-047, 6500-04-02-FG, 6500-20-16-FG, 6500-24-20-FG, 6500-32-24-FG, 6501-16-12-FG, 6502-04-02-FG, 6502-06-04-FG, 6502-12-10-FG, 6502-20-16-FG, 6505-04-02, 6566-06-06-FG, 6802-04-02-NWO-FG, 6803-02-02-02-NWO-FG (QOMI 1.4; PROJECT_STATUS s3 item 2).
5. ORFS with no source: FS0304-C-32-ASY, FS0319-24, FS2406-06-08, FS2406-10-10, FS6403-24-24, FS6505-06-06, FS6505-10-08; FS0319-24 collar 1.71 / 1.910 / 2.00 - which? (QOMI 1.4 / 1.6).
6. FS2408 plug: solid or with the blind hole (QOMI 1.5).
7. 6420-12-12: which body for the 1.730 length (QOMI 1.7).
8. Optional cross-check: bent-tube tube OD / wall / bend radius (QOMI 1.9) - needed if you pick OMi as the bent-tube source.
9. Chase from 2026-10-09: wrong numbers on the 62 drawings? title block? small 6408 plugs hollow or solid? (QOMI 2).

## Questions for you

1. Bent tubes (68): source for tube OD / wall / bend radius / end-hex length - OMi, Air-Way 3D models, or each part's own Brennan STEP? (wave3 benttube REPORT; NSP19 "still open").
2. Q-CODE62-CAT: take code 62 heads -12 ... -32 from Brennan catalog table 3300-62 instead of downloading 1824-12 ... -32? (OPEN_QUESTIONS_2026-10-18 "New after the answers").
3. Forged ORFS rows where Air-Way's plain row differs from Brennan's forged row (21): keep MISSING (2026-10-15) or use Brennan's forged values now that Brennan = yes? (not yet asked; inference from wave3 orfs REPORT).
4. FS6400-L / FS6801-L long variants: shape source (a Brennan long-variant file?) (NSP20 "still open").
5. FS2408: build solid now, or wait for OMi?
6. Q-PLUG-SOCKDEPTH / Q-PLUG-SQHEAD / Q-NEW-NPT01: 5406-HHP / -SHP / 6408-HHP plug rules (OPEN_QUESTIONS D).
7. Group D one-liners still open: Q36-25 (6801-05-05), Q-SIZE40-JIC (2501-40-40-FG), Q-THREAD (6565-32-32), Q-CONFLICT-6404-D3-08, Q-CONFLICT-2502-MS51506, Q-CONFLICT-6900-05-04-O, Q-ANGLED-P1 (2505-04-04-FG), 2702-LN-12-12-FG misprint.
8. Still open from NSP20: sleeve length FS0319 (Air-Way L 0.37 vs STEP 0.374), one master per leg shape (FS...N / R / C) OK, Q-FS-ORBSTUD, Q-FS2406-NUT.

## Appendix: every not-yet part by category and group

**a / Adjustable-ORB families 6805 / 6806 / 6807 / 6809 / 6815 / 6832 / 6835 / 6901 / 6902** (78): 6805-04-02-NWO-FG, 6805-04-04-NWO-FG, 6805-06-04-NWO-FG, 6805-06-06-NWO-FG, 6805-08-06-NWO-FG, 6805-08-08-NWO-FG, 6805-10-08-NWO-FG, 6805-12-08-NWO-FG, 6805-12-12-NWO-FG, 6805-16-12-NWO-FG, 6805-16-16-NWO-FG, 6805-20-20-NWO-FG, 6806-04-04-NWO-FG, 6806-06-04-NWO-FG, 6806-06-06-NWO-FG, 6806-08-06-NWO-FG, 6806-08-08-NWO-FG, 6806-10-08-NWO-FG, 6806-12-08-NWO-FG, 6806-12-12-NWO-FG, 6806-16-16-NWO-FG, 6806-20-20-NWO-FG, 6806-24-24-NWO-FG, 6807-04-04-NWO-FG, 6807-08-06-NWO-FG, 6807-08-08-NWO-FG, 6807-12-12-NWO-FG, 6809-04-04-NWO-FG, 6809-06-06-NWO-FG, 6809-08-08-NWO-FG, 6809-10-10-NWO-FG, 6809-12-12-NWO-FG, 6809-16-16-NWO-FG, 6809-20-20-NWO-FG, 6815-04-04-NWO-FG, 6815-06-06-NWO-FG, 6815-08-08-NWO-FG, 6815-10-10-NWO-FG, 6815-12-12-NWO-FG, 6815-16-16-NWO-FG, 6832-04-04-04-NWO-FG, 6832-06-06-06-NWO-FG, 6832-08-08-08-NWO-FG, 6832-16-16-16-NWO-FG, 6835-04-04-04-NWO-FG, 6835-06-06-06-NWO-FG, 6835-08-08-08-NWO-FG, 6835-12-12-12-NWO-FG, 6901-04-04-NWO-FG, 6901-04-06-NWO-FG, 6901-06-04-NWO-FG, 6901-06-06-NWO-FG, 6901-06-08-NWO-FG, 6901-08-06-NWO-FG, 6901-08-08-NWO-FG, 6901-08-12-NWO-FG, 6901-10-06-NWO-FG, 6901-10-08-NWO-FG, 6901-10-12-NWO-FG, 6901-12-06-NWO-FG, 6901-12-08-NWO-FG, 6901-12-12-NWO-FG, 6901-12-16-NWO-FG, 6901-16-12-NWO-FG, 6901-16-16-NWO-FG, 6901-20-16-NWO-FG, 6901-20-20-NWO-FG, 6901-24-24-NWO-FG, 6901-32-32-NWO-FG, 6902-04-04-NWO-FG, 6902-06-04-NWO-FG, 6902-06-06-NWO-FG, 6902-08-06-NWO-FG, 6902-08-08-NWO-FG, 6902-10-08-NWO-FG, 6902-10-12-NWO-FG, 6902-16-16-NWO-FG, 6902-24-24-NWO-FG

**a / ORFS straights FS2403 / FS2404 / FS6400 / FS6403 at -04 ... -20** (59): FS2403-04-04, FS2403-06-04, FS2403-06-06, FS2403-08-06, FS2403-10-08, FS2403-10-10, FS2403-12-08, FS2403-12-10, FS2403-12-12, FS2403-16-12, FS2403-16-16, FS2403-20-16, FS2403-20-20, FS2403-24-20, FS2404-04-02, FS2404-04-04, FS2404-04-06, FS2404-06-04, FS2404-06-06, FS2404-06-08, FS2404-10-08, FS2404-10-12, FS2404-12-08, FS2404-12-12, FS2404-12-16, FS2404-16-12, FS2404-16-16, FS2404-16-20, FS2404-20-16, FS2404-20-20, FS6400-04-04-O, FS6400-04-05-O, FS6400-04-06-O, FS6400-04-08-O, FS6400-04-10-O, FS6400-06-04-O, FS6400-06-05-O, FS6400-06-06-O, FS6400-06-08-O, FS6400-06-10-O, FS6400-10-08-O, FS6400-10-10-O, FS6400-10-12-O, FS6400-12-08-O, FS6400-12-10-O, FS6400-12-12-O, FS6400-12-16-O, FS6400-16-12-O, FS6400-16-16-O, FS6400-16-20-O, FS6400-20-16-O, FS6400-20-20-O, FS6400-20-24-O, FS6403-04-04, FS6403-06-06, FS6403-10-10, FS6403-12-12, FS6403-16-16, FS6403-20-20

**a / Forged (-FG) rows that need their own Brennan file** (45): 1504-24-24-FG, 1504-32-32-FG, 5503-04-02-FG, 5503-06-04-FG, 5503-08-06-FG, 5503-12-08-FG, 5503-16-12-FG, 5505-02-02-FG, 5505-06-06-FG, 5505-12-12-FG, 5505-16-16-FG, 5602-02-02-02-FG, 5602-06-06-06-FG, 5602-12-12-12-FG, 5602-16-16-16-FG, 5602-20-20-20-FG, 5602-24-24-24-FG, 5602-32-32-32-FG, 5604-02-02-02-FG, 5604-12-12-12-FG, 5604-16-16-16-FG, 5604-20-20-20-FG, 5604-32-32-32-FG, 5605-02-02-02-FG, 5605-12-12-12-FG, 5605-16-16-16-FG, 5605-20-20-20-FG, 5605-32-32-32-FG, 6503-06-06-FG, 6503-16-16-FG, 6566-16-16-FG, 6603-16-16-16-FG, 6606-12-12-12-FG, 6801-08-04-NWO-FG, 6801-08-16-NWO-FG, 6801-12-20-NWO-FG, 6801-16-24-NWO-FG, 6801-24-16-NWO-FG, 6802-06-10-NWO-FG, 6802-08-12-NWO-FG, 6803-08-08-06-NWO-FG, 6803-08-08-10-NWO-FG, 6803-24-24-24-NWO-FG, 6804-24-24-24-NWO-FG, 6810-12-12-NWO-FG
  - also: pilot of 6810 (BSL)

**a / ORFS adjustable-stud elbows / tees FS6801 / FS6802 / FS6803 / FS6804** (34): FS6801-04-04-NWO-FG, FS6801-06-04-NWO-FG, FS6801-06-10-NWO-FG, FS6801-08-06-NWO-FG, FS6801-08-12-NWO-FG, FS6801-10-10-NWO-FG, FS6801-10-12-NWO-FG, FS6801-12-10-NWO-FG, FS6801-12-12-NWO-FG, FS6801-12-16-NWO-FG, FS6801-16-12-NWO-FG, FS6801-16-16-NWO-FG, FS6801-16-20-NWO-FG, FS6801-20-16-NWO-FG, FS6801-24-24-NWO-FG, FS6802-04-04-NWO-FG, FS6802-04-06-NWO-FG, FS6802-06-04-NWO-FG, FS6802-06-06-NWO-FG, FS6802-06-10-NWO-FG, FS6802-08-06-NWO-FG, FS6802-08-10-NWO-FG, FS6802-08-12-NWO-FG, FS6802-12-12-NWO-FG, FS6802-16-12-NWO-FG, FS6803-04-04-04-NWO-FG, FS6803-12-12-12-NWO-FG, FS6803-16-16-16-NWO-FG, FS6804-04-04-04-NWO-FG, FS6804-06-06-06-NWO-FG, FS6804-08-06-08-NWO-FG, FS6804-10-10-10-NWO-FG, FS6804-12-12-12-NWO-FG, FS6804-16-16-16-NWO-FG

**a / ORFS bulkhead elbows / tees FS2701 / FS2702 / FS2703 / FS2704 (+ -LN) at -04 ... -16** (32): FS2701-04-04-FG, FS2701-06-06-FG, FS2701-10-10-FG, FS2701-12-12-FG, FS2701-LN-04-04-FG, FS2701-LN-06-06-FG, FS2701-LN-10-10-FG, FS2701-LN-12-12-FG, FS2702-04-04-FG, FS2702-06-06-FG, FS2702-10-10-FG, FS2702-12-12-FG, FS2702-LN-04-04-FG, FS2702-LN-06-06-FG, FS2702-LN-10-10-FG, FS2702-LN-12-12-FG, FS2703-04-04-04-FG, FS2703-06-06-06-FG, FS2703-12-12-12-FG, FS2703-LN-04-04-04-FG, FS2703-LN-06-06-06-FG, FS2703-LN-12-12-12-FG, FS2704-04-04-04-FG, FS2704-06-06-06-FG, FS2704-10-10-10-FG, FS2704-12-12-12-FG, FS2704-16-16-16-FG, FS2704-LN-04-04-04-FG, FS2704-LN-06-06-06-FG, FS2704-LN-10-10-10-FG, FS2704-LN-12-12-12-FG, FS2704-LN-16-16-16-FG

**a / 6900 male ORB x female NPSM swivel straights** (21): 6900-04-02-O, 6900-04-04-O, 6900-04-06-O, 6900-06-04-O, 6900-06-06-O, 6900-06-08-O, 6900-08-04-O, 6900-08-06-O, 6900-08-08-O, 6900-08-12-O, 6900-10-06-O, 6900-10-08-O, 6900-10-12-O, 6900-12-08-O, 6900-12-12-O, 6900-12-16-O, 6900-16-12-O, 6900-16-16-O, 6900-20-20-O, 6900-24-24-O, 6900-32-32-O
  - also: d: new SPEC 6900 (A3: male ORB x female NPSM swivel straight; Air-Way lengths, Q-NEW-6900-LEN)

**a / -24 / -32 female pipe ports (tap drill, A9)** (18): 2502-24-24-FG, 2502-32-32-FG, 5000-24-20, 5405-16-24, 5405-20-32, 5406-40-32, 5406-C-24, 5406-C-32, 5503-24-24-FG, 5503-32-32-FG, 5504-24-24-FG, 5504-32-32-FG, 5601-24-24-24-FG, 5603-24-24-24-FG, 5652-24-24-24-24-FG, 5652-32-32-32-32-FG, 6405-16-24-O, 6506-32-32
  - also: d: measure the -40 male NPTF end on BRENNAN_5406-40-32 (on disk) | legs + hex only on its own STEP | own STEP (3DF s3)

**a / ORFS flange straights / elbows FS1700 / FS1704 / FS1800 / FS1804** (16): FS1700-12-12, FS1700-16-16, FS1700-20-20, FS1700-24-24, FS1704-12-12-FG, FS1704-16-16-FG, FS1704-20-20-FG, FS1704-24-24-FG, FS1800-12-12, FS1800-16-16, FS1800-20-20, FS1800-24-24, FS1804-12-12-FG, FS1804-16-16-FG, FS1804-20-20-FG, FS1804-24-24-FG
  - also: d: new FS flange SPECs

**a / ORFS tube-end reducer FS2406** (15): FS2406-06-04, FS2406-08-04, FS2406-08-06, FS2406-10-06, FS2406-10-08, FS2406-12-06, FS2406-12-08, FS2406-12-10, FS2406-12-16, FS2406-16-08, FS2406-16-12, FS2406-16-20, FS2406-20-16, FS2406-20-24, FS2406-24-20
  - also: collar D8 + bore missing: own STEP

**a / ORFS straight bulkhead union FS2700 (+ -LN)** (14): FS2700-04-04, FS2700-06-06, FS2700-08-06, FS2700-08-08, FS2700-10-10, FS2700-12-12, FS2700-16-16, FS2700-20-20, FS2700-LN-04-04, FS2700-LN-06-06, FS2700-LN-08-08, FS2700-LN-10-10, FS2700-LN-12-12, FS2700-LN-16-16
  - also: d: new SPEC FS2700 (straight bulkhead end)

**a / 6801-L / 6801-LL long adjustable elbows** (12): 6801-L-04-04-NWO-FG, 6801-L-06-06-NWO-FG, 6801-L-08-08-NWO-FG, 6801-L-12-12-NWO-FG, 6801-L-16-16-NWO-FG, 6801-L-20-20-NWO-FG, 6801-LL-04-04-NWO-FG, 6801-LL-06-06-NWO-FG, 6801-LL-08-08-NWO-FG, 6801-LL-12-12-NWO-FG, 6801-LL-16-16-NWO-FG, 6801-LL-20-20-NWO-FG
  - also: d: fold 6801-L / -LL into 6801 (PS3 item 7)

**a / Code 62 flange straights 1800** (12): 1800-12-12, 1800-12-16, 1800-16-12, 1800-16-16, 1800-16-20, 1800-16-24, 1800-20-16, 1800-20-20, 1800-20-24, 1800-24-20, 1800-24-24, 1800-32-32
  - also: c (alternative for the heads): Q-CODE62-CAT

**a / Flange plugs 1724 (code 61) / 1824 (code 62)** (11): 1724-12, 1724-16, 1724-20, 1724-24, 1724-32, 1724-40, 1824-12, 1824-16, 1824-20, 1824-24, 1824-32
  - also: the same files give the code 62 heads

**a / 6408-HHP hex-socket plugs** (11): 6408-HHP-02-O, 6408-HHP-03-O, 6408-HHP-04-O, 6408-HHP-05-O, 6408-HHP-06-O, 6408-HHP-10-O, 6408-HHP-12-O, 6408-HHP-16-O, 6408-HHP-20-O, 6408-HHP-24-O, 6408-HHP-32-O
  - also: c: Q-PLUG-SOCKDEPTH (rule vs. per-part files)

**a / Forged code 61 flange elbows 1703 / 1704 -FG** (10): 1703-08-08-FG, 1703-12-12-FG, 1703-16-16-FG, 1703-20-20-FG, 1703-32-32-FG, 1704-08-08-FG, 1704-12-12-FG, 1704-16-16-FG, 1704-20-20-FG, 1704-32-32-FG

**a / Forged code 62 flange elbows 1803 / 1804 -FG** (10): 1803-12-12-FG, 1803-16-16-FG, 1803-20-20-FG, 1803-24-24-FG, 1803-32-32-FG, 1804-12-12-FG, 1804-16-16-FG, 1804-20-20-FG, 1804-24-24-FG, 1804-32-32-FG
  - also: c (alternative to the 1824 files): Q-CODE62-CAT

**a / ORFS cap assembly FS0304-C-xx-ASY** (8): FS0304-C-04-ASY, FS0304-C-06-ASY, FS0304-C-08-ASY, FS0304-C-10-ASY, FS0304-C-12-ASY, FS0304-C-16-ASY, FS0304-C-20-ASY, FS0304-C-24-ASY
  - also: d: new SPEC (cap insert + nut)

**a / ORFS FS6402 (male face seal x female JIC swivel)** (7): FS6402-04-04, FS6402-06-06, FS6402-08-08, FS6402-10-10, FS6402-12-12, FS6402-16-16, FS6402-20-20
  - also: d: new SPEC FS6402; bores D1/D2 missing (catalog prints none)

**a / 6425 ORB x ORB unions** (6): 6425-04-04, 6425-06-06, 6425-08-08, 6425-10-10, 6425-12-12, 6425-16-16
  - also: d: new SPEC 6425

**a / ORFS rows with a missing cell only its own file has** (5): FS6400-10-06-O, FS6400-12-20-O, FS6565-10-10, FS6565-16-16, FS7202-06-04-NWO-FG
  - also: BSPP thread + stud length + bores missing (W3ORFS); new end type | stud length L9 + bores missing (W3ORFS) | swivel bores D19 missing (W3ORFS: catalog prints bores only on FS6505 / FS6809)

**a / ORFS 45 deg swivel elbow FS6502 -06 / -10 / -12 / -16** (4): FS6502-06-06-FG, FS6502-10-10-FG, FS6502-12-12-FG, FS6502-16-16-FG

**a / 3051** (4): 3051-04-04, 3051-06-06, 3051-08-08, 3051-12-12

**a / ORFS FS6809 (90 deg swivel x adjustable stud)** (3): FS6809-06-06-NWO-FG, FS6809-16-16-NWO-FG, FS6809-20-20-NWO-FG
  - also: d: new SPEC FS6809 (swivel x adjustable stud)

**a / ORFS -24 forged leg / swivel (FS6500-24-24-FG, FS2500-24-xx-FG)** (3): FS2500-24-20-FG, FS2500-24-24-FG, FS6500-24-24-FG

**a / ORFS FS2503-08-08-FG / -10-08-FG** (2): FS2503-08-08-FG, FS2503-10-08-FG

**a / 0304-C-02 / 0306-02 (-02 JIC cap / locknut)** (2): 0304-C-02, 0306-02

**a / Air-Way misprints a STEP settles** (2): 5405-08-16, 6405-32-24-O

**a / 5404-L-04X3.000 / X4.000** (2): 5404-L-04X3.000, 5404-L-04X4.000

**a / 6420-12-12** (1): 6420-12-12

**a / 2404-32-48** (1): 2404-32-48

**a / 2505-16-16-FG (port deeper than the short leg)** (1): 2505-16-16-FG

**b / Compression (bite type) C0318 C0319 C2402 C2403 C2404 C2405 C2500 C2501 C2502 C2601 C6801 (incl. -M1 body-only)** (230): C0318-04, C0318-06, C0318-08, C0318-10, C0318-12, C0318-16, C0318-20, C0318-24, C0318-32, C0319-04, C0319-06, C0319-08, C0319-10, C0319-12, C0319-16, C0319-20, C0319-24, C0319-32, C2402-04-04, C2402-04-04-M1, C2402-06-06, C2402-06-06-M1, C2402-08-08, C2402-08-08-M1, C2402-10-10, C2402-10-10-M1, C2402-12-12, C2402-12-12-M1, C2402-16-16, C2402-16-16-M1, C2402-20-20, C2402-20-20-M1, C2403-04-04, C2403-04-04-M1, C2403-06-06, C2403-06-06-M1, C2403-08-08, C2403-08-08-M1, C2403-10-10, C2403-10-10-M1, C2403-12-12, C2403-12-12-M1, C2403-16-16, C2403-16-16-M1, C2403-20-20, C2403-20-20-M1, C2403-24-24, C2403-24-24-M1, C2403-32-32, C2403-32-32-M1, C2404-04-02, C2404-04-02-M1, C2404-04-04, C2404-04-04-M1, C2404-06-02, C2404-06-02-M1, C2404-06-04, C2404-06-04-M1, C2404-06-06, C2404-06-06-M1, C2404-08-06, C2404-08-06-M1, C2404-08-08, C2404-08-08-M1, C2404-10-08, C2404-10-08-M1, C2404-12-08, C2404-12-08-M1, C2404-12-12, C2404-12-12-M1, C2404-16-12, C2404-16-12-M1, C2404-16-16, C2404-16-16-M1, C2404-20-16, C2404-20-16-M1, C2404-20-20, C2404-20-20-M1, C2404-24-24, C2404-24-24-M1, C2404-32-32, C2404-32-32-M1, C2405-04-02, C2405-04-02-M1, C2405-04-04, C2405-04-04-M1, C2405-06-04, C2405-06-04-M1, C2405-06-06, C2405-06-06-M1, C2405-08-06, C2405-08-06-M1, C2405-08-08, C2405-08-08-M1, C2405-10-08, C2405-10-08-M1, C2405-12-08, C2405-12-08-M1, C2405-12-12, C2405-12-12-M1, C2405-16-12, C2405-16-12-M1, C2405-16-16, C2405-16-16-M1, C2405-20-16, C2405-20-16-M1, C2405-20-20, C2405-20-20-M1, C2405-24-20, C2405-24-20-M1, C2405-24-24, C2405-24-24-M1, C2405-32-32, C2405-32-32-M1, C2500-04-04-FG, C2500-04-04-FG-M1, C2500-06-06-FG, C2500-06-06-FG-M1, C2500-08-08-FG, C2500-08-08-FG-M1, C2500-12-12-FG, C2500-12-12-FG-M1, C2500-16-16-FG, C2500-16-16-FG-M1, C2501-04-02-FG, C2501-04-02-FG-M1, C2501-04-04-FG, C2501-04-04-FG-M1, C2501-06-02-FG, C2501-06-02-FG-M1, C2501-06-04-FG, C2501-06-04-FG-M1, C2501-06-06-FG, C2501-06-06-FG-M1, C2501-08-06-FG, C2501-08-06-FG-M1, C2501-08-08-FG, C2501-08-08-FG-M1, C2501-10-08-FG, C2501-10-08-FG-M1, C2501-12-08-FG, C2501-12-08-FG-M1, C2501-12-12-FG, C2501-12-12-FG-M1, C2501-16-12-FG, C2501-16-12-FG-M1, C2501-16-16-FG, C2501-16-16-FG-M1, C2501-20-16-FG, C2501-20-16-FG-M1, C2501-20-20-FG, C2501-20-20-FG-M1, C2501-24-20-FG, C2501-24-20-FG-M1, C2501-24-24-FG, C2501-24-24-FG-M1, C2501-32-32-FG, C2501-32-32-FG-M1, C2502-04-02-FG, C2502-04-02-FG-M1, C2502-04-04-FG, C2502-04-04-FG-M1, C2502-06-04-FG, C2502-06-04-FG-M1, C2502-06-06-FG, C2502-06-06-FG-M1, C2502-08-06-FG, C2502-08-06-FG-M1, C2502-08-08-FG, C2502-08-08-FG-M1, C2502-10-08-FG, C2502-10-08-FG-M1, C2502-12-08-FG, C2502-12-08-FG-M1, C2502-12-12-FG, C2502-12-12-FG-M1, C2502-16-12-FG, C2502-16-12-FG-M1, C2502-16-16-FG, C2502-16-16-FG-M1, C2502-20-16-FG, C2502-20-16-FG-M1, C2502-20-20-FG, C2502-20-20-FG-M1, C2502-24-20-FG, C2502-24-20-FG-M1, C2502-24-24-FG, C2502-24-24-FG-M1, C2502-32-32-FG, C2502-32-32-FG-M1, C2601-04-04-04-FG, C2601-04-04-04-FG-M1, C2601-06-06-06-FG, C2601-06-06-06-FG-M1, C2601-08-08-08-FG, C2601-08-08-08-FG-M1, C2601-12-12-12-FG, C2601-12-12-12-FG-M1, C2601-16-16-16-FG, C2601-16-16-16-FG-M1, C6801-04-02-NWO-FG, C6801-04-02-NWO-FG-M1, C6801-04-04-NWO-FG, C6801-04-04-NWO-FG-M1, C6801-06-04-NWO-FG, C6801-06-04-NWO-FG-M1, C6801-06-06-NWO-FG, C6801-06-06-NWO-FG-M1, C6801-08-08-NWO-FG, C6801-08-08-NWO-FG-M1, C6801-12-08-NWO-FG, C6801-12-08-NWO-FG-M1, C6801-12-12-NWO-FG, C6801-12-12-NWO-FG-M1, C6801-16-12-NWO-FG, C6801-16-12-NWO-FG-M1, C6801-16-16-NWO-FG, C6801-16-16-NWO-FG-M1, C6801-20-16-NWO-FG, C6801-20-16-NWO-FG-M1, C6801-20-20-NWO-FG, C6801-20-20-NWO-FG-M1, C6801-24-20-NWO-FG, C6801-24-20-NWO-FG-M1, C6801-24-24-NWO-FG, C6801-24-24-NWO-FG-M1, C6801-32-24-NWO-FG, C6801-32-24-NWO-FG-M1, C6801-32-32-NWO-FG, C6801-32-32-NWO-FG-M1

**b / Parts with no Air-Way row, no Brennan catalog row and no Brennan file** (29): 1405-20-24, 1803-08-08-FG, 2403-06-02, 2406-06-12, 2502-20-16-FG, 2613-08-08-08-FG, 2700-04-02, 2700-08-06, 2700-10-08, 2700-12-10, 2700-LN-04-02, 2700-LN-08-06, 2700-LN-10-08, 2700-LN-12-10, 5404-L-04X2.000, 5404-R-04-04-047, 6500-04-02-FG, 6500-20-16-FG, 6500-24-20-FG, 6500-32-24-FG, 6501-16-12-FG, 6502-04-02-FG, 6502-06-04-FG, 6502-12-10-FG, 6502-20-16-FG, 6505-04-02, 6566-06-06-FG, 6802-04-02-NWO-FG, 6803-02-02-02-NWO-FG

**b / Test gauge TGT-6504 / TGT-FS2406** (12): TGT-6504-04-04-04, TGT-6504-06-06-04, TGT-6504-08-08-04, TGT-6504-10-10-04, TGT-6504-12-12-04, TGT-6504-16-16-04, TGT-6504-24-24-04, TGT-FS2406-04-04-04, TGT-FS2406-06-06-04, TGT-FS2406-08-08-04, TGT-FS2406-10-10-04, TGT-FS2406-12-12-04

**b / 4005 flange O-rings** (9): 4005-08, 4005-10, 4005-12, 4005-16, 4005-20, 4005-24, 4005-32, 4005-40, 4005-48

**b / ORFS parts with no usable source** (7): FS0304-C-32-ASY, FS0319-24, FS2406-06-08, FS2406-10-10, FS6403-24-24, FS6505-06-06, FS6505-10-08

**b / Flareless nut 0618 / sleeve 0619** (4): 0618-06, 0618-08, 0619-06, 0619-08
  - also: a: V0318-08 / V0319-08 shape files; c: Q-NEW-F3-FLARELESS-ALIAS

**c / Bent-tube elbows 1703 / 1704 / 1803 / 1804 -TUBE and 6701** (68): 1703-08-08-TUBE, 1703-12-12-TUBE, 1703-12-16-TUBE, 1703-16-16-TUBE, 1703-16-20-TUBE, 1703-16-24-TUBE, 1703-20-16-TUBE, 1703-20-20-TUBE, 1703-20-24-TUBE, 1703-24-20-TUBE, 1703-24-24-TUBE, 1703-24-32-TUBE, 1703-32-32-TUBE, 1704-08-08-TUBE, 1704-08-12-TUBE, 1704-12-12-TUBE, 1704-12-16-TUBE, 1704-16-12-TUBE, 1704-16-16-TUBE, 1704-16-20-TUBE, 1704-16-24-TUBE, 1704-20-12-TUBE, 1704-20-16-TUBE, 1704-20-20-TUBE, 1704-20-24-TUBE, 1704-20-32-TUBE, 1704-24-16-TUBE, 1704-24-20-TUBE, 1704-24-24-TUBE, 1704-24-32-TUBE, 1704-32-24-TUBE, 1704-32-32-TUBE, 1803-12-12-TUBE, 1803-12-16-TUBE, 1803-12-20-TUBE, 1803-16-12-TUBE, 1803-16-16-TUBE, 1803-16-20-TUBE, 1803-20-12-TUBE, 1803-20-16-TUBE, 1803-20-20-TUBE, 1803-20-24-TUBE, 1803-24-20-TUBE, 1803-24-24-TUBE, 1803-32-32-TUBE, 1804-08-08-TUBE, 1804-12-12-TUBE, 1804-12-16-TUBE, 1804-12-20-TUBE, 1804-16-12-TUBE, 1804-16-16-TUBE, 1804-16-20-TUBE, 1804-16-24-TUBE, 1804-20-16-TUBE, 1804-20-20-TUBE, 1804-20-24-TUBE, 1804-24-16-TUBE, 1804-24-20-TUBE, 1804-24-24-TUBE, 1804-24-32-TUBE, 1804-32-32-TUBE, 6701-04-04, 6701-06-06, 6701-08-08, 6701-12-12, 6701-16-16, 6701-20-20, 6701-L-16-16
  - also: then the source chosen (OMi / Air-Way 3D models / own Brennan STEPs); 1803/1804: code 62 heads

**c / Forged ORFS rows where Air-Way's plain row differs from Brennan's forged row** (21): FS2501-04-02-FG, FS2503-04-02-FG, FS2701-16-16-FG, FS2701-LN-16-16-FG, FS2702-16-16-FG, FS2702-LN-16-16-FG, FS2703-16-16-16-FG, FS2703-LN-16-16-16-FG, FS6502-04-04-FG, FS6801-04-06-NWO-FG, FS6801-06-06-NWO-FG, FS6801-08-10-NWO-FG, FS6801-20-20-NWO-FG, FS6802-12-16-NWO-FG, FS6802-16-16-NWO-FG, FS6802-20-20-NWO-FG, FS6803-06-06-06-NWO-FG, FS6809-04-04-NWO-FG, FS6809-08-08-NWO-FG, FS6809-10-10-NWO-FG, FS6809-12-12-NWO-FG
  - also: a: the STEPs listed; then measure the missing cells

**c / 5406-HHP / 5406-SHP plugs** (13): 5406-HHP-01, 5406-HHP-02, 5406-HHP-04, 5406-HHP-06, 5406-HHP-12, 5406-HHP-16, 5406-HHP-20, 5406-HHP-24, 5406-HHP-32, 5406-SHP-04, 5406-SHP-06, 5406-SHP-12, 5406-SHP-16

**c / ORFS plug FS2408** (8): FS2408-04, FS2408-06, FS2408-08, FS2408-10, FS2408-12, FS2408-16, FS2408-20, FS2408-24

**c / FS6400-L / FS6801-L long variants** (4): FS6400-L-06-06-O, FS6400-L-08-08-O, FS6400-L-12-10-O, FS6801-L-08-08-NWO-FG

**c / 2502-08-04-FG / -12-08-FG** (2): 2502-08-04-FG, 2502-12-08-FG

**c / 2505-04-04-FG (port deeper than the short leg)** (1): 2505-04-04-FG

**c / 6801-05-05-NWO-FG** (1): 6801-05-05-NWO-FG

**c / 2501-40-40-FG** (1): 2501-40-40-FG

**c / 6565-32-32** (1): 6565-32-32

**c / 6404-08-12** (1): 6404-08-12

**c / 6900-05-04-O** (1): 6900-05-04-O

**c / 2702-LN-12-12-FG** (1): 2702-LN-12-12-FG

**d / Rows whose question was answered on 2026-10-18 - apply and regenerate** (25): 2705-04-02, 2705-LN-04-02, 2705-LN-06-04, 2706-06-04, 2706-32-32, 2706-LN-06-04, 2706-LN-08-06, 6405-32-16-O, 6410-20-06-O, 6410-20-08-O, 6410-32-12-O, 6410-32-16-O, 6410-32-20-O, 6410-32-24-O, 6503-04-04-FG, 6503-12-12-FG, 6504-08-12, 6504-10-08, 6504-10-12, 6504-12-10, 6504-16-20, 6504-32-32, 6506-06-04, 6506-06-10, 6506-12-08

**d / New review table / SPEC from data already in hand** (14): 2613-04-04-04-FG, 3474-04-04-NWO, 3474-06-06-NWO, 3474-08-08-NWO, 3474-10-10-NWO, 3474-12-12-NWO, 3474-16-16-NWO, 3474-20-20-NWO, 3474-24-24-NWO, 3474-32-32-NWO, 6316-08, 6316-12, 6316-16, 6420-08-08

**d / 0319 JIC tube sleeves** (12): 0319-02, 0319-03, 0319-04, 0319-05, 0319-06, 0319-08, 0319-10, 0319-12, 0319-16, 0319-20, 0319-24, 0319-32

**d / Own Brennan file already in 09_STEP_FILES - measure and fill** (11): 1502-08-08-FG, 2404-L-32-32, 2501-LL-08-08-FG, 2505-08-08-FG, 5505-08-08-FG, 5601-06-06-06-FG, 5603-08-08-08-FG, 5652-08-08-08-08-FG, 6506-12-14, 6603-06-06-06-FG, 6606-06-06-06-FG

**d / 2500 / 2502 / 2603 rows that need the hand-made HX masters moved to the generator** (9): 2500-06-04-FG, 2500-08-06-FG, 2500-12-08-FG, 2500-12-10-FG, 2502-04-06-FG, 2502-05-04-FG, 2502-06-08-FG, 2502-16-20-FG, 2603-02-02-02-FG

**d / Generator geometry blocks / capabilities now merged** (6): 1502-04-04-FG, 2406-16-04, 5501-24-24-FG, 5501-32-32-FG, 5503-02-02-FG, 6502-16-12-FG

**d / Rows staged with Brennan catalog sizes but still MISSING** (5): 1504-08-08-FG, 1504-12-12-FG, 1504-16-16-FG, 6807-16-16-NWO-FG, 6807-20-20-NWO-FG

**d / 5404-N long nipples in OMi's part-number form** (4): 5404-N-06X4.500, 5404-N-06X5.500, 5404-N-08X2.500, 5404-N-08X5.500

**d / Air-Way value not buildable -> Brennan (user Q1 2026-10-20)** (4): 1501-04-02-FG, 1501-24-24-FG, 2408-14, 6802-04-06-NWO-FG

**d / FS2500-12-08-FG / -16-12-FG** (2): FS2500-12-08-FG, FS2500-16-12-FG

**d / 2404-40-40** (1): 2404-40-40

**d / 1603-08-08-08-FG** (1): 1603-08-08-08-FG

**e / Kits 1901 / 1902 / 1927** (30): 1901-08-KIT, 1901-12-KIT, 1901-16-KIT, 1901-16-M10-KIT, 1901-20-KIT, 1901-20-M10-KIT, 1901-24-KIT, 1901-32-KIT, 1901-40-KIT, 1901-48-KIT, 1902-08-KIT, 1902-12-KIT, 1902-16-KIT, 1902-16-M12-KIT, 1902-20-KIT, 1902-20-M14-KIT, 1902-24-KIT, 1902-32-KIT, 1927-61-08-08-KIT, 1927-61-12-12-KIT, 1927-61-16-16-KIT, 1927-61-20-20-KIT, 1927-61-24-24-KIT, 1927-61-32-32-KIT, 1927-62-08-08-KIT, 1927-62-12-12-KIT, 1927-62-16-16-KIT, 1927-62-20-20-KIT, 1927-62-24-24-KIT, 1927-62-32-32-KIT

## Source keys

- NSP20 = `00_DOCS/NEXT_SESSION_PROMPT_2026-10-20.md`
- NSP19 = `00_DOCS/NEXT_SESSION_PROMPT_2026-10-19.md`
- NSP18 = `00_DOCS/NEXT_SESSION_PROMPT_2026-10-18.md`
- ORFSRM = `tools/_out/orfs_gen_20261020/README.md`
- STEPS16 = `tools/_out/orfs_modeltype_20261016/STEPS_NEEDED.txt`
- W3ORFS = `tools/_out/brennan_yes_20261018/wave3/orfs/`
- W3BT = `tools/_out/brennan_yes_20261018/wave3/benttube/`
- W3AD = `tools/_out/brennan_yes_20261018/wave3/adapters/`
- W2FH = `tools/_out/brennan_yes_20261018/wave2/flange_hose/`
- W2ST = `tools/_out/brennan_yes_20261018/wave2/straight/`
- W2TE = `tools/_out/brennan_yes_20261018/wave2/tee_elbow/`
- 3DF = `tools/_out/brennan_yes_20261018/3D_FILES_NEEDED.md`
- OQ18 = `00_DOCS/OPEN_QUESTIONS_2026-10-18.md`
- ANS18 = `00_DOCS/ANSWERS_2026-10-18.md`
- QOMI = `10_DRAWINGS/for_OMi_LATER/QUESTIONS_FOR_OMi.md`
- PS3 = `00_DOCS/PROJECT_STATUS.md s3`
- PS5 = `00_DOCS/PROJECT_STATUS.md s5`
- P2535 = `tools/_out/adapters77_20261016/possible_2535.json`
- R77 = `tools/_out/adapters77_20261016/REPORT_77.md`
- OCT = `00_DOCS/ORFS_Compression_TestGauge_2026-10-15.md`
- NT = `tools/_out/newtypes_20261014/README.md`
- RT = `the review table ($COMMENT)`
- B17 = `tools/_out/batch17_20261019/RESUME.md`
- BSL = `00_DOCS/Brennan_STEP_list_2026-10-01.md`
- unblock rows.csv = `tools/_out/unblock_20261008/rows.csv`
- unblock rows.csv = `tools/_out/unblock_20261008/rows.csv`; merged.json = `tools/_out/questions_20261008/merged.json`; gen_* = `tools/_out/orfs_gen_20261020/tools/generators/`
