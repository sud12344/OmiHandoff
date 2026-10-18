# F1a - what the Brennan catalogs change (Task C group F1, first half by config)

Created 2026-10-01T23:06:46 by `tools/_out/brennan_catalog_20261001/impact/work_F1a/build_F1a.py` - data: `impact/F1a.json`. Read-only on every source.

Scope: Task C rows with group F1, sorted by config, first half: 130 rows (1501-16-20-FG ... 5504-24-24-FG). Premises: Q-NEW-BRENNANCAT = YES (user: "use any needed" catalogs); Q-BRENNAN-ONLY formally open (the standing F1 decision already accepts Brennan alone for -FG parts); OMi + Brennan = one source, so every catalog value stays **ASSUMED**; rounding-only differences are not differences.

## Headline

23 of 130 F1a rows change bucket: 17 DECIDE -> NOW (2501 x9, 2501-L x4, 2503-20-24-FG, 2601-24-24-24-FG, 5500 x2: the catalog's own column letters answer Q-B-ELBOW / Q-B-TEE / Q-B-5500 and its -FG values equal the OMi fills, which makes Q-F1 moot), 2 STEP -> NOW (1501-16-20-FG, 1501-20-16-FG: all 7 body cells printed), 4 STEP -> DECIDE (2500 x4: dimensions printed, Q-HX left). Unchanged: 6 STEP (2702-20-20-FG needs the bulkhead collar i2/K1/O; 5504 x5 need only their tap drills - new question Q-NEW-F1A-5504TAP), 10 DECIDE (2502 x5 keep Q-HX / Q-TRANSFER-TAPDRILL / the MS51506 conflict; 2602-08-08-08-FG and 5502 x4 keep Q-TRANSFER-TAPDRILL), 91 WORK (generator work; the catalog supplies their dimensions). The catalog prints 713 of the 807 body cells the 130 rows need (167 with a likely pairing), every one of the 226 OMi values compared equals it, and every Task C library fill compared (thread sizes, NPSM nut hexes) agrees. Of the 102 required STEP downloads touching F1a: 36 replaced by the catalog, 65 partly (pilot geometry, tap drills, hose beads, flange bore / head, bulkhead collar), 1 not replaced (1602-08-08-08-FG is not in the catalog); all 27 conditional STEPs of the DECIDE rows are replaced.

| old -> new bucket | rows |
|---|---|
| WORK->WORK | 91 |
| DECIDE->NOW | 17 |
| DECIDE->DECIDE | 10 |
| STEP->STEP | 6 |
| STEP->DECIDE | 4 |
| STEP->NOW | 2 |

New buckets: DECIDE 14, NOW 19, STEP 6, WORK 91 (old: DECIDE 27, STEP 12, WORK 91).

Cells: 546 body cells printed with a certain pairing, 167 with a likely pairing, 2 printed only as a range, 82 not printed (end library: 76, STEP only: 6), 10 with no catalog row; 249 thread callouts (all name the same size as the Task C fill where one exists). OMi: 226 cells compared, 226 equal / rounding, 0 differ. Air-Way: no F1a row has its own value; plain twins (evidence only) match 383, differ 323.

## Per table

| table | rows | old -> new | catalog | gives | not printed | note |
|---|---|---|---|---|---|---|
| 1501 | 2 | STEP->NOW 2 | TFA p20 1501-FG | C1HEX@HEX, CHEX@HEX, D2@BORE, D@BORE, M1@DRIVE, N1@DRIVE, W3@HEX | - | master + SPEC exist; M = stem tip / M1 = nut face (TIP_B offsets, 1503 STEPs) |
| 1502 | 7 | WORK->WORK 7 | TFA p21 1502-FG | C1HEX@HEX, CHEX@HEX, D@BORE, M1@DRIVE, N3@DRIVE, W3@HEX | TAPDRILL@BORE | new root; pilot 1502-08-08-FG |
| 1503 | 5 | WORK->WORK 5 | TFA p21 1503-FG | C1HEX@HEX, CHEX@HEX, D2@BORE, D@BORE, M@DRIVE, N@DRIVE, W2@HEX | - | SPEC exists; legs proven on the in-repo 1503 STEPs |
| 1504 | 2 | WORK->WORK 2 | TFA p22 1504-FG | C1HEX@HEX, CHEX@HEX, D@BORE, M@DRIVE, N2@DRIVE, W2@HEX | TAPDRILL@BORE | new root; pilot 1504-06-06-FG |
| 1601 | 6 | WORK->WORK 6 | TFA p47 1601-FG | C1HEX@HEX, C2HEX@HEX, C3HEX@HEX, D2@BORE, D3@BORE, D_2@BORE, M1_2@DRIVE, M1_3@DRIVE, N1@DRIVE, W3_2@HEX, W3_3@HEX | - | swivel legs: nut face M (A2 side) / stem tip M1 (A3 side), the other leg by symmetry |
| 1602 | 3 | WORK->WORK 3 | TFA p48 1602-FG | C1HEX@HEX, C2HEX@HEX, C3HEX@HEX, D2@BORE, D3@BORE, M1_2@DRIVE, M1_3@DRIVE, N3@DRIVE, W3_2@HEX, W3_3@HEX | TAPDRILL@BORE | 1602-08-08-08-FG (pilot) is NOT in the catalog |
| 1603 | 6 | WORK->WORK 6 | TFA p48 1603-FG | C1HEX@HEX, C2HEX@HEX, C3HEX@HEX, C_1HEX@HEX, D1@BORE, D2@BORE, M1@DRIVE, M2_2@DRIVE, M2_3@DRIVE, W3@HEX, W5_2@HEX, W5_3@HEX | - | same-dash rows: all three legs alike; 1603-08-08-08 drills printed as a range |
| 1703 | 1 | WORK->WORK 1 | FLANGE p4 1703-FG | CHEX@HEX, M2@DRIVE, N3@DRIVE | D@BORE, O@DRIVE | Flange p4; flange bore not printed, head OD from FLG61 library |
| 1704 | 2 | WORK->WORK 2 | FLANGE p5 1704-FG | M@DRIVE, N2@DRIVE, Y@HEX | D@BORE, O@DRIVE | Flange p5; flange bore not printed, head OD from FLG61 library |
| 2500 | 4 | STEP->DECIDE 4 | TFA p22 2500-FG | D1@BORE, D2@BORE, M1@DRIVE, M2@DRIVE, Y@REF | - | legacy 2500HX: Q-HX left |
| 2501 | 9 | DECIDE->NOW 9 | TFA p23 2501-FG | D1@DRILL, D@BORE, M@DRIVE, N@DRIVE, Y@REF | - | Q-B-ELBOW + Q-F1 answered |
| 2501L | 4 | DECIDE->NOW 4 | TFA p24 2501-L-FG | D1@BORE, D@BORE, M@DRIVE, N3@DRIVE, Y@REF | - | folded into 2501; Q-B-ELBOW + Q-F1 answered |
| 2501LL | 7 | WORK->WORK 7 | TFA p24 2501-LL-FG | D1@BORE, D@BORE, M@DRIVE, N4@DRIVE, Y@REF | - | fold work; pilot proves the fold shape only |
| 2502 | 5 | DECIDE->DECIDE 5 | TFA p25 2502-FG | D@BORE, M1@DRIVE, N1@DRIVE, Y1@DRIVE | TAPDRILL@BORE | legacy 2502HX: Q-HX, tap drill, MS51506 conflict left |
| 2503 | 1 | DECIDE->NOW 1 | TFA p26 2503-FG | D1@BORE, D@BORE, M2@DRIVE, N2@DRIVE, Y@REF | - | Q-B-ELBOW + Q-F1 answered |
| 2504 | 4 | WORK->WORK 4 | TFA p26 2504-FG | D1@BORE, D2@BORE, M2_1@DRIVE, M2_2@DRIVE, Y@HEX | - | pilot STEP in repo; Q-B-OTHER-2504 answered |
| 2505 | 3 | WORK->WORK 3 | TFA p27 2505-FG | D@BORE, M2@DRIVE, N6@DRIVE, Y1@HEX | TAPDRILL@BORE | Q-B-OTHER-2505 answered |
| 2601 | 1 | DECIDE->NOW 1 | TFA p49 2601-FG | D1@BORE, D2@BORE, DDRILL@BORE, M1@DRIVE, M2@DRIVE, N@DRIVE, Y@REF | - | Q-B-TEE + Q-F1 answered |
| 2602 | 1 | DECIDE->DECIDE 1 | TFA p49 2602-FG | D1@BORE, D2@BORE, M1_1@DRIVE, M1_2@DRIVE, N1@DRIVE, Y1@DRIVE | TAPDRILL@BORE | Q-B-TEE / Y1 answered; tap drill left |
| 2606 | 4 | WORK->WORK 4 | TFA p51 2606-FG | D1@BORE, D3@BORE, M1_1@DRIVE, M1_3@DRIVE, N1@DRIVE, Y1@HEX | TAPDRILL@BORE | Q-B-OTHER-TEE2 answered |
| 2611 | 2 | WORK->WORK 2 | TFA p52 2611-FG | D1@BORE, D@BORE, M1@DRIVE, N1@DRIVE, N5@DRIVE, Y1@HEX | TAPDRILL@BORE | Q-B-OTHER-TEE2 answered |
| 2702 | 1 | STEP->STEP 1 | TFA p27 2702-FG | D1@BORE, D2@BORE, M2@DRIVE, M9@DRIVE, Y@HEX | K1@DRIVE, O@DRIVE, i2@DRIVE | bulkhead collar not printed; Q-NEW-2702HOLD |
| 4501 | 11 | WORK->WORK 11 | TFA p28 4501-FG | D1@BORE, L4@DRIVE, N@DRIVE, Y@HEX | AA@DRIVE | hose bead AA not printed |
| 4503 | 7 | WORK->WORK 7 | TFA p29 4503-FG | CHEX@HEX, D1@BORE, L5@DRIVE, N2@DRIVE | AA@DRIVE | hose bead AA not printed |
| 4601 | 9 | WORK->WORK 9 | TFA p29 4601-NWO-FG | C4HEX@HEX, D@BORE, L4@DRIVE, M7@DRIVE, Y@HEX | AA@DRIVE | hose bead AA not printed; catalog gives the locknut hex |
| 4603 | 1 | WORK->WORK 1 | TFA p30 4603-NWO-FG | C4HEX@HEX, CHEX@HEX, D@BORE, L5@DRIVE, M8@DRIVE | AA@DRIVE | hose bead AA not printed |
| 5500 | 2 | DECIDE->NOW 2 | TFA p30 5500-FG | D1@BORE, D2@BORE, N1@DRIVE, N2@DRIVE, Y@REF | - | Q-B-5500 + Q-F1 answered |
| 5501 | 7 | WORK->WORK 7 | TFA p31 5501-FG | D1@BORE, D2@BORE, N4@DRIVE, N6@DRIVE, Y@HEX | - | Q-B-OTHER-5501 answered |
| 5502 | 4 | DECIDE->DECIDE 4 | TFA p31 5502-FG | D@BORE, N1@DRIVE, N@DRIVE, W@REF | TAPDRILL@BORE | tap drill left |
| 5503 | 4 | WORK->WORK 4 | TFA p32 5503-FG | D@BORE, N3@DRIVE, N4@DRIVE, W@HEX | TAPDRILL@BORE | tap drill not printed |
| 5504 | 5 | STEP->STEP 5 | TFA p32 5504-FG | N1_1@DRIVE, N1_2@DRIVE, W@REF | TAPDRILL1@BORE, TAPDRILL2@BORE | only the tap drills left (Q-NEW-F1A-5504TAP) |

## Rows

| config | old -> new | catalog | cells given (review <- catalog = value) | not printed (or range) | questions answered | STEP verdict |
|---|---|---|---|---|---|---|
| 1501-16-20-FG | STEP -> NOW | TFA p20 | N1<-L=2.350; M1<-M=1.730; W3<-M1=2.150; CHEX<-C HEX=1.875; C1HEX<-Y FLATS=1.625; D2<-A1 DRILL=0.938; D<-A2 DRILL=1.010 | - | - | own: replaced_by_catalog |
| 1501-20-16-FG | STEP -> NOW | TFA p20 | N1<-L=2.380; M1<-M=1.700; W3<-M1=2.050; CHEX<-C HEX=1.500; C1HEX<-Y FLATS=1.625; D2<-A1 DRILL=1.250; D<-A2 DRILL=0.830 | - | - | own: replaced_by_catalog |
| 1502-06-06-FG | WORK -> WORK | TFA p21 | N3<-L=1.02*; M1<-M=1.06; W3<-M1=1.27; CHEX<-C HEX=0.875; C1HEX<-Y FLATS=0.875; D<-A2 DRILL=0.340 | TAPDRILL | - | own: partly |
| 1502-08-08-FG | WORK -> WORK | TFA p21 | N3<-L=1.23*; M1<-M=1.24; W3<-M1=1.52; CHEX<-C HEX=1.000; C1HEX<-Y FLATS=1.062; D<-A2 DRILL=0.460 | TAPDRILL | - | own: partly |
| 1502-12-12-FG | WORK -> WORK | TFA p21 | N3<-L=1.360*; M1<-M=1.470; W3<-M1=1.820; CHEX<-C HEX=1.250; C1HEX<-Y FLATS=1.312; D<-A2 DRILL=0.620 | TAPDRILL | - | own: partly |
| 1502-16-16-FG | WORK -> WORK | TFA p21 | N3<-L=1.620*; M1<-M=1.730; W3<-M1=2.080; CHEX<-C HEX=1.500; C1HEX<-Y FLATS=1.625; D<-A2 DRILL=0.780 | TAPDRILL | - | own: partly |
| 1502-20-20-FG | WORK -> WORK | TFA p21 | N3<-L=1.70*; M1<-M=1.83; W3<-M1=2.25; CHEX<-C HEX=1.875; C1HEX<-Y FLATS=1.875; D<-A2 DRILL=1.03 | TAPDRILL | - | own: partly |
| 1502-24-24-FG | WORK -> WORK | TFA p21 | N3<-L=2.080*; M1<-M=2.410; W3<-M1=2.830; CHEX<-C HEX=2.125; C1HEX<-Y FLATS=2.562; D<-A2 DRILL=1.250 | TAPDRILL | - | own: partly |
| 1502-32-32-FG | WORK -> WORK | TFA p21 | N3<-L=2.39*; M1<-M=2.57; W3<-M1=2.99; CHEX<-C HEX=2.625; C1HEX<-Y FLATS=2.812; D<-A2 DRILL=1.720 | TAPDRILL | - | own: partly |
| 1503-04-02-FG | WORK -> WORK | TFA p21 | N<-L=0.860; M<-M1=0.630; W2<-M=0.770; CHEX<-C HEX=0.562; C1HEX<-Y FLATS=0.562; D2<-A1 DRILL=0.281; D<-A2 DRILL=0.120 | - | - | own: replaced_by_catalog |
| 1503-04-06-FG | WORK -> WORK | TFA p21 | N<-L=0.950; M<-M1=0.810; W2<-M=1.020; CHEX<-C HEX=0.875; C1HEX<-Y FLATS=0.750; D2<-A1 DRILL=0.281; D<-A2 DRILL=0.330 | - | - | own: replaced_by_catalog |
| 1503-06-04-FG | WORK -> WORK | TFA p21 | N<-L=0.95; M<-M1=0.79; W2<-M=0.98; CHEX<-C HEX=0.688; C1HEX<-Y FLATS=0.750; D2<-A1 DRILL=0.406; D<-A2 DRILL=0.220 | - | - | own: replaced_by_catalog |
| 1503-06-08-FG | WORK -> WORK | TFA p21 | N<-L=0.980; M<-M1=0.880; W2<-M=1.160; CHEX<-C HEX=1.000; C1HEX<-Y FLATS=0.875; D2<-A1 DRILL=0.406; D<-A2 DRILL=0.440 | - | - | own: replaced_by_catalog |
| 1503-08-12-FG | WORK -> WORK | TFA p21 | N<-L=1.200; M<-M1=1.020; W2<-M=1.370; CHEX<-C HEX=1.250; C1HEX<-Y FLATS=1.062; D2<-A1 DRILL=0.531; D<-A2 DRILL=0.630 | - | - | own: replaced_by_catalog |
| 1504-06-06-FG | WORK -> WORK | TFA p22 | N2<-L=0.750*; M<-M1=0.770; W2<-M=0.980; CHEX<-C HEX=0.875; C1HEX<-Y FLATS=0.875; D<-A2 DRILL=0.320 | TAPDRILL | - | own: partly |
| 1504-24-24-FG | WORK -> WORK | TFA p22 | N2<-L=1.46*; M<-M1=1.46; W2<-M=1.88; CHEX<-C HEX=2.125; C1HEX<-Y FLATS=2.562; D<-A2 DRILL=1.260 | TAPDRILL | - | own: partly |
| 1601-02-02-02-FG | WORK -> WORK | TFA p47 | N1<-L=0.720; W3_2<-M=0.840; W3_3<-M=0.840*; M1_3<-M1=0.700; M1_2<-M1=0.700*; C3HEX<-C HEX=0.562; C2HEX<-C HEX=0.562*; C1HEX<-Y FLATS=0.438; D2<-A1 DRILL=0.188; D_2<-A2 DRILL=0.120; D3<-A3 DRILL=0.120 | - | - | own: replaced_by_catalog |
| 1601-04-04-04-FG | WORK -> WORK | TFA p47 | N1<-L=1.090; W3_2<-M=1.070; W3_3<-M=1.070*; M1_3<-M1=0.880; M1_2<-M1=0.880*; C3HEX<-C HEX=0.688; C2HEX<-C HEX=0.688*; C1HEX<-Y FLATS=0.562; D2<-A1 DRILL=0.281; D_2<-A2 DRILL=0.220; D3<-A3 DRILL=0.220 | - | - | own: replaced_by_catalog |
| 1601-06-06-06-FG | WORK -> WORK | TFA p47 | N1<-L=1.22; W3_2<-M=1.20; W3_3<-M=1.20*; M1_3<-M1=0.99; M1_2<-M1=0.99*; C3HEX<-C HEX=0.875; C2HEX<-C HEX=0.875*; C1HEX<-Y FLATS=0.750; D2<-A1 DRILL=0.406; D_2<-A2 DRILL=0.340; D3<-A3 DRILL=0.340 | - | - | own: replaced_by_catalog |
| 1601-08-08-08-FG | WORK -> WORK | TFA p47 | N1<-L=1.470; W3_2<-M=1.390; W3_3<-M=1.390*; M1_3<-M1=1.110; M1_2<-M1=1.110*; C3HEX<-C HEX=1.000; C2HEX<-C HEX=1.000*; C1HEX<-Y FLATS=0.875; D2<-A1 DRILL=0.531; D_2<-A2 DRILL=0.460; D3<-A3 DRILL=0.460 | - | - | own: partly |
| 1601-12-12-12-FG | WORK -> WORK | TFA p47 | N1<-L=1.590; W3_2<-M=1.650; W3_3<-M=1.650*; M1_3<-M1=1.300; M1_2<-M1=1.300*; C3HEX<-C HEX=1.250; C2HEX<-C HEX=1.250*; C1HEX<-Y FLATS=1.062; D2<-A1 DRILL=0.719; D_2<-A2 DRILL=0.620; D3<-A3 DRILL=0.620 | - | - | own: replaced_by_catalog |
| 1601-16-16-16-FG | WORK -> WORK | TFA p47 | N1<-L=1.970; W3_2<-M=1.890; W3_3<-M=1.890*; M1_3<-M1=1.540; M1_2<-M1=1.540*; C3HEX<-C HEX=1.500; C2HEX<-C HEX=1.500*; C1HEX<-Y FLATS=1.312; D2<-A1 DRILL=0.938; D_2<-A2 DRILL=0.800; D3<-A3 DRILL=0.800 | - | - | own: replaced_by_catalog |
| 1602-06-06-06-FG | WORK -> WORK | TFA p48 | N3<-L=0.940*; W3_2<-M=1.200; W3_3<-M=1.200*; M1_3<-M1=0.990; M1_2<-M1=0.990*; C3HEX<-C HEX=0.875; C2HEX<-C HEX=0.875*; C1HEX<-Y FLATS=0.875; D2<-A2 DRILL=0.340; D3<-A3 DRILL=0.340 | TAPDRILL | - | own: partly |
| 1602-08-08-08-FG | WORK -> WORK | not in catalog | - | TAPDRILL | - | own: not_replaced |
| 1602-12-12-12-FG | WORK -> WORK | TFA p48 | N3<-L=1.360*; W3_2<-M=1.820; W3_3<-M=1.820*; M1_3<-M1=1.470; M1_2<-M1=1.470*; C3HEX<-C HEX=1.250; C2HEX<-C HEX=1.250*; C1HEX<-Y FLATS=1.312; D2<-A2 DRILL=0.630; D3<-A3 DRILL=0.630 | TAPDRILL | - | own: partly |
| 1603-02-02-02-FG | WORK -> WORK | TFA p48 | W3<-L=0.840*; M1<-M2=0.700*; M2_2<-M1=0.700*; W5_2<-M=0.840*; M2_3<-M2=0.700; W5_3<-M=0.840; C_1HEX<-C HEX=0.562; C3HEX<-C1 HEX=0.562*; C2HEX<-C1 HEX=0.562*; C1HEX<-Y Flats=0.438; D1<-A1 DRILL=0.110*; D2<-A2 DRILL=0.110* | - | - | own: replaced_by_catalog |
| 1603-04-04-04-FG | WORK -> WORK | TFA p48 | W3<-L=1.070*; M1<-M2=0.880*; M2_2<-M1=0.880*; W5_2<-M=1.070*; M2_3<-M2=0.880; W5_3<-M=1.070; C_1HEX<-C HEX=0.688; C3HEX<-C1 HEX=0.688*; C2HEX<-C1 HEX=0.688*; C1HEX<-Y Flats=0.562; D1<-A1 DRILL=0.220*; D2<-A2 DRILL=0.220* | - | - | own: replaced_by_catalog |
| 1603-06-06-06-FG | WORK -> WORK | TFA p48 | W3<-L=1.200*; M1<-M2=0.990*; M2_2<-M1=0.990*; W5_2<-M=1.200*; M2_3<-M2=0.990; W5_3<-M=1.200; C_1HEX<-C HEX=0.875; C3HEX<-C1 HEX=0.875*; C2HEX<-C1 HEX=0.875*; C1HEX<-Y Flats=0.750; D1<-A1 DRILL=0.340*; D2<-A2 DRILL=0.340* | - | - | own: replaced_by_catalog |
| 1603-08-08-08-FG | WORK -> WORK | TFA p48 | W3<-L=1.390*; M1<-M2=1.110*; M2_2<-M1=1.110*; W5_2<-M=1.390*; M2_3<-M2=1.110; W5_3<-M=1.390; C_1HEX<-C HEX=1.000; C3HEX<-C1 HEX=1.000*; C2HEX<-C1 HEX=1.000*; C1HEX<-Y Flats=0.875 | D1 (range 0.44/0.46), D2 (range 0.44/0.46) | - | own: partly |
| 1603-12-12-12-FG | WORK -> WORK | TFA p48 | W3<-L=1.650*; M1<-M2=1.300*; M2_2<-M1=1.300*; W5_2<-M=1.650*; M2_3<-M2=1.300; W5_3<-M=1.650; C_1HEX<-C HEX=1.250; C3HEX<-C1 HEX=1.250*; C2HEX<-C1 HEX=1.250*; C1HEX<-Y Flats=1.062; D1<-A1 DRILL=0.620*; D2<-A2 DRILL=0.620* | - | - | own: replaced_by_catalog |
| 1603-16-16-16-FG | WORK -> WORK | TFA p48 | W3<-L=1.890*; M1<-M2=1.540*; M2_2<-M1=1.540*; W5_2<-M=1.890*; M2_3<-M2=1.540; W5_3<-M=1.890; C_1HEX<-C HEX=1.500; C3HEX<-C1 HEX=1.500*; C2HEX<-C1 HEX=1.500*; C1HEX<-Y Flats=1.312; D1<-A1 DRILL=0.780*; D2<-A2 DRILL=0.780* | - | - | own: replaced_by_catalog |
| 1703-24-24-FG | WORK -> WORK | FLANGE p4 | M2<-L1=1.78*; N3<-L2=2.38*; CHEX<-A/F=1 7/8 | O, D | - | own: partly |
| 1704-24-24-FG | WORK -> WORK | FLANGE p5 | M<-L1=2.330*; N2<-L2=3.150*; Y<-A/F=1.875 | O, D | - | own: partly |
| 1704-32-32-FG | WORK -> WORK | FLANGE p5 | M<-L1=3.06*; N2<-L2=4.25*; Y<-A/F=2.500 | O, D | - | own: partly |
| 2500-06-04-FG | STEP -> DECIDE | TFA p22 | M1<-M1=1.06; M2<-M2=1.05; Y<-Y FLATS=0.562; D1<-B1 DRILL=0.297; D2<-B2 DRILL=0.172 | - | - | own: replaced_by_catalog |
| 2500-08-06-FG | STEP -> DECIDE | TFA p22 | M1<-M1=1.25; M2<-M2=1.14; Y<-Y FLATS=0.750; D1<-B1 DRILL=0.391; D2<-B2 DRILL=0.297 | - | - | own: replaced_by_catalog |
| 2500-12-08-FG | STEP -> DECIDE | TFA p22 | M1<-M1=1.660; M2<-M2=1.420; Y<-Y FLATS=1.062; D1<-B1 DRILL=0.609; D2<-B2 DRILL=0.391 | - | - | own: replaced_by_catalog |
| 2500-12-10-FG | STEP -> DECIDE | TFA p22 | M1<-M1=1.66; M2<-M2=1.54; Y<-Y FLATS=1.062; D1<-B1 DRILL=0.609; D2<-B2 DRILL=0.484 | - | - | own: replaced_by_catalog |
| 2501-04-12-FG | DECIDE -> NOW | TFA p23 | M<-M=1.35; N<-L=1.59; Y<-Y FLATS=1.062; D<-B1 DRILL=0.172; D1<-A2 DRILL=0.719 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-05-06-FG | DECIDE -> NOW | TFA p23 | M<-M=1.120; N<-L=1.220; Y<-Y FLATS=0.750; D<-B1 DRILL=0.234; D1<-A2 DRILL=0.406 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-06-12-FG | DECIDE -> NOW | TFA p23 | M<-M=1.31; N<-L=1.59; Y<-Y FLATS=1.062; D<-B1 DRILL=0.297; D1<-A2 DRILL=0.719 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-08-16-FG | DECIDE -> NOW | TFA p23 | M<-M=1.520; N<-L=1.970; Y<-Y FLATS=1.312; D<-B1 DRILL=0.391; D1<-A2 DRILL=0.938 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-12-06-FG | DECIDE -> NOW | TFA p23 | M<-M=1.66; N<-L=1.40; Y<-Y FLATS=1.062; D<-B1 DRILL=0.609; D1<-A2 DRILL=0.406 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-12-20-FG | DECIDE -> NOW | TFA p23 | M<-M=1.97; N<-L=2.38; Y<-Y FLATS=1.625; D<-B1 DRILL=0.609; D1<-A2 DRILL=1.250 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-16-08-FG | DECIDE -> NOW | TFA p23 | M<-M=1.81; N<-L=1.78; Y<-Y FLATS=1.312; D<-B1 DRILL=0.844; D1<-A2 DRILL=0.531 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-16-24-FG | DECIDE -> NOW | TFA p23 | M<-M=2.16; N<-L=2.64; Y<-Y FLATS=1.875; D<-B1 DRILL=0.844; D1<-A2 DRILL=1.500 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-24-16-FG | DECIDE -> NOW | TFA p23 | M<-M=2.330; N<-L=2.580; Y<-Y FLATS=1.875; D<-B1 DRILL=1.312; D1<-A2 DRILL=0.938 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-L-04-04-FG | DECIDE -> NOW | TFA p24 | M<-MLGTH=1.05; N3<-L=1.58; Y<-Y FLATS=0.562; D<-B1 DRILL=0.172; D1<-A2 DRILL=0.281 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-L-08-08-FG | DECIDE -> NOW | TFA p24 | M<-MLGTH=1.33; N3<-L=2.17; Y<-Y FLATS=0.875; D<-B1 DRILL=0.391; D1<-A2 DRILL=0.531 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-L-12-12-FG | DECIDE -> NOW | TFA p24 | M<-MLGTH=1.66; N3<-L=2.44; Y<-Y FLATS=1.062; D<-B1 DRILL=0.609; D1<-A2 DRILL=0.719 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-L-16-16-FG | DECIDE -> NOW | TFA p24 | M<-MLGTH=1.81; N3<-L=3.01; Y<-Y FLATS=1.312; D<-B1 DRILL=0.844; D1<-A2 DRILL=0.938 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2501-LL-04-02-FG | WORK -> WORK | TFA p24 | M<-M=0.890; N4<-L=1.560; Y<-Y FLATS=0.438; D<-B1 DRILL=0.172; D1<-A2 DRILL=0.188 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2501-LL-04-04-FG | WORK -> WORK | TFA p24 | M<-M=1.050; N4<-L=2.070; Y<-Y FLATS=0.562; D<-B1 DRILL=0.172; D1<-A2 DRILL=0.281 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2501-LL-06-04-FG | WORK -> WORK | TFA p24 | M<-M=1.06; N4<-L=2.07; Y<-Y FLATS=0.562; D<-B1 DRILL=0.297; D1<-A2 DRILL=0.281 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2501-LL-06-06-FG | WORK -> WORK | TFA p24 | M<-M=1.14; N4<-L=2.42; Y<-Y FLATS=0.750; D<-B1 DRILL=0.297; D1<-A2 DRILL=0.406 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2501-LL-08-08-FG | WORK -> WORK | TFA p24 | M<-M=1.330; N4<-L=2.870; Y<-Y FLATS=0.875; D<-B1 DRILL=0.391; D1<-A2 DRILL=0.531 | - | Q-NEW-FOLD-2501LL (partly) | own: partly |
| 2501-LL-12-12-FG | WORK -> WORK | TFA p24 | M<-M=1.660; N4<-L=3.280; Y<-Y FLATS=1.062; D<-B1 DRILL=0.609; D1<-A2 DRILL=0.719 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2501-LL-16-16-FG | WORK -> WORK | TFA p24 | M<-M=1.81; N4<-L=4.05; Y<-Y FLATS=1.312; D<-B1 DRILL=0.844; D1<-A2 DRILL=0.938 | - | Q-NEW-FOLD-2501LL (partly) | own: replaced_by_catalog |
| 2502-06-08-FG | DECIDE -> DECIDE | TFA p25 | M1<-M=1.41; N1<-L=1.23; Y1<-Y FLATS=1.062; D<-B1 DRILL=0.297 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2502-08-04-FG | DECIDE -> DECIDE | TFA p25 | M1<-M=1.42; N1<-L=1.01; Y1<-Y FLATS=0.750; D<-B1 DRILL=0.391 | TAPDRILL | Q-B-ELBOW, Q-CONFLICT-2502-MS51506 (partly), Q-F1 | own: replaced_by_catalog |
| 2502-12-08-FG | DECIDE -> DECIDE | TFA p25 | M1<-M=1.89; N1<-L=1.35; Y1<-Y FLATS=1.062; D<-B1 DRILL=0.609 | TAPDRILL | Q-B-ELBOW, Q-CONFLICT-2502-MS51506 (partly), Q-F1 | own: replaced_by_catalog |
| 2502-16-20-FG | DECIDE -> DECIDE | TFA p25 | M1<-M=2.28; N1<-L=1.70; Y1<-Y FLATS=1.875; D<-B1 DRILL=0.844 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2502-24-24-FG | DECIDE -> DECIDE | TFA p25 | M1<-M=2.89; N1<-L=2.08; Y1<-Y FLATS=2.562; D<-B1 DRILL=1.312 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2503-20-24-FG | DECIDE -> NOW | TFA p26 | M2<-M=1.65; N2<-L=1.77; Y<-Y FLATS=1.875; D<-B1 DRILL=1.078; D1<-A2 DRILL=1.500 | - | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 2504-04-04-FG | WORK -> WORK | TFA p26 | M2_1<-M1=0.72*; M2_2<-M2=0.72*; Y<-Y FLATS=0.438; D1<-B1 DRILL=0.172; D2<-B2 DRILL=0.172 | - | Q-F1, Q-B-OTHER-2504 | own: replaced_by_catalog |
| 2504-06-06-FG | WORK -> WORK | TFA p26 | M2_1<-M1=0.83*; M2_2<-M2=0.83*; Y<-Y FLATS=0.562; D1<-B1 DRILL=0.297; D2<-B2 DRILL=0.297 | - | Q-F1, Q-B-OTHER-2504 | own: replaced_by_catalog |
| 2504-08-08-FG | WORK -> WORK | TFA p26 | M2_1<-M1=0.98*; M2_2<-M2=0.98*; Y<-Y FLATS=0.750; D1<-B1 DRILL=0.391; D2<-B2 DRILL=0.391 | - | Q-B-OTHER-2504, Q-F1 | - |
| 2504-12-12-FG | WORK -> WORK | TFA p26 | M2_1<-M1=1.28*; M2_2<-M2=1.28*; Y<-Y FLATS=1.062; D1<-B1 DRILL=0.609; D2<-B2 DRILL=0.609 | - | Q-F1, Q-B-OTHER-2504 | own: replaced_by_catalog |
| 2505-08-08-FG | WORK -> WORK | TFA p27 | M2<-M=1.04; N6<-N=0.94; Y1<-Y FLATS=1.062; D<-B1 DRILL=0.391 | TAPDRILL | Q-F1, Q-B-OTHER-2505 | own: partly |
| 2505-12-12-FG | WORK -> WORK | TFA p27 | M2<-M=1.42; N6<-N=1.00; Y1<-Y FLATS=1.312; D<-B1 DRILL=0.609 | TAPDRILL | Q-F1, Q-B-OTHER-2505 | own: partly |
| 2505-16-16-FG | WORK -> WORK | TFA p27 | M2<-M=1.54; N6<-N=1.12; Y1<-Y FLATS=1.625; D<-B1 DRILL=0.844 | TAPDRILL | Q-F1, Q-B-OTHER-2505 | own: partly |
| 2601-24-24-24-FG | DECIDE -> NOW | TFA p49 | M1<-M1=2.330; M2<-M2=2.330; N<-L=2.640; Y<-Y FLATS=1.875; D1<-B1 DRILL=1.312; D2<-B2 DRILL=1.312; DDRILL<-A3 DRILL=1.500 | - | Q-B-TEE, Q-F1 | own: replaced_by_catalog |
| 2602-08-08-08-FG | DECIDE -> DECIDE | TFA p49 | M1_1<-M1=1.520; M1_2<-M2=1.520; N1<-N=1.230; Y1<-Y FLATS=1.062; D1<-B1 DRILL=0.391; D2<-B2 DRILL=0.391 | TAPDRILL | Q-B-OTHER-2602Y1, Q-B-TEE, Q-F1 | own: replaced_by_catalog |
| 2606-04-04-04-FG | WORK -> WORK | TFA p51 | M1_1<-M=1.22; N1<-L=0.88; M1_3<-N=1.22; Y1<-Y FLATS=0.750; D1<-B1 DRILL=0.172; D3<-B3 DRILL=0.172 | TAPDRILL | Q-F1, Q-B-OTHER-TEE2 | own: partly |
| 2606-06-06-06-FG | WORK -> WORK | TFA p51 | M1_1<-M=1.310; N1<-L=1.020; M1_3<-N=1.310; Y1<-Y FLATS=0.875; D1<-B1 DRILL=0.297; D3<-B3 DRILL=0.297 | TAPDRILL | Q-F1, Q-B-OTHER-TEE2 | own: partly |
| 2606-08-08-08-FG | WORK -> WORK | TFA p51 | M1_1<-M=1.520; N1<-L=1.230; M1_3<-N=1.520; Y1<-Y FLATS=1.062; D1<-B1 DRILL=0.391; D3<-B3 DRILL=0.391 | TAPDRILL | Q-F1, Q-B-OTHER-TEE2 | own: partly |
| 2606-16-16-16-FG | WORK -> WORK | TFA p51 | M1_1<-M=2.170; N1<-L=1.620; M1_3<-N=2.170; Y1<-Y FLATS=1.625; D1<-B1 DRILL=0.844; D3<-B3 DRILL=0.844 | TAPDRILL | Q-F1, Q-B-OTHER-TEE2 | own: partly |
| 2611-06-06-06-FG | WORK -> WORK | TFA p52 | M1<-M=1.310; N5<-L=1.220; N1<-L1=1.020; Y1<-Y FLATS=0.875; D<-B1 DRILL=0.297; D1<-A2 DRILL=0.406 | TAPDRILL | Q-F1, Q-B-OTHER-TEE2 | own: partly |
| 2611-12-12-12-FG | WORK -> WORK | TFA p52 | M1<-M=1.890; N5<-L=1.590; N1<-L1=1.360; Y1<-Y FLATS=1.312; D<-B1 DRILL=0.609; D1<-A2 DRILL=0.719 | TAPDRILL | - | own: partly |
| 2702-20-20-FG | STEP -> STEP | TFA p27 | M2<-M=1.590; M9<-L=2.650; Y<-Y FLATS=1.625; D1<-B1 DRILL=1.078; D2<-B2 DRILL=1.078 | i2, K1, O | - | own: partly |
| 4501-06-04-FG | WORK -> WORK | TFA p28 | L4<-L=1.870*; N<-N=1.090; Y<-Y FLATS=0.562; D1<-A2 DRILL=0.281* | AA | - | own: partly |
| 4501-06-06-FG | WORK -> WORK | TFA p28 | L4<-L=2.040*; N<-N=1.220; Y<-Y FLATS=0.750; D1<-A2 DRILL=0.406* | AA | - | own: partly |
| 4501-08-06-FG | WORK -> WORK | TFA p28 | L4<-L=2.040*; N<-N=1.220; Y<-Y FLATS=0.750; D1<-A2 DRILL=0.406* | AA | - | own: partly |
| 4501-08-08-FG | WORK -> WORK | TFA p28 | L4<-L=2.055*; N<-N=1.470; Y<-Y FLATS=0.875; D1<-A2 DRILL=0.531* | AA | - | own: partly |
| 4501-08-12-FG | WORK -> WORK | TFA p28 | L4<-L=2.232*; N<-N=1.594; Y<-Y FLATS=1.062; D1<-A2 DRILL=0.719* | AA | - | own: partly |
| 4501-10-08-FG | WORK -> WORK | TFA p28 | L4<-L=2.055*; N<-N=1.470; Y<-Y FLATS=0.875; D1<-A2 DRILL=0.531* | AA | - | own: partly |
| 4501-12-08-FG | WORK -> WORK | TFA p28 | L4<-L=2.060*; N<-N=1.470; Y<-Y FLATS=0.875; D1<-A2 DRILL=0.531* | AA | - | own: partly |
| 4501-12-12-FG | WORK -> WORK | TFA p28 | L4<-L=2.232*; N<-N=1.595; Y<-Y FLATS=1.062; D1<-A2 DRILL=0.719* | AA | - | own: partly |
| 4501-16-12-FG | WORK -> WORK | TFA p28 | L4<-L=2.360*; N<-N=1.780; Y<-Y FLATS=1.312; D1<-A2 DRILL=0.719* | AA | - | own: partly |
| 4501-16-16-FG | WORK -> WORK | TFA p28 | L4<-L=2.320*; N<-N=1.970; Y<-Y FLATS=1.312; D1<-A2 DRILL=0.938* | AA | - | own: partly |
| 4501-20-20-FG | WORK -> WORK | TFA p28 | L4<-L=2.570*; N<-N=2.375; Y<-Y FLATS=1.625; D1<-A2 DRILL=1.250* | AA | - | own: partly |
| 4503-04-04-FG | WORK -> WORK | TFA p29 | L5<-L=1.810*; N2<-N=0.830; CHEX<-Y FLATS=0.625*; D1<-A2 DRILL=0.281* | AA | - | own: partly |
| 4503-08-08-FG | WORK -> WORK | TFA p29 | L5<-L=1.830*; N2<-N=1.170; CHEX<-Y FLATS=0.875*; D1<-A2 DRILL=0.531* | AA | - | own: partly |
| 4503-12-12-FG | WORK -> WORK | TFA p29 | L5<-L=1.894*; N2<-N=1.200; CHEX<-Y FLATS=1.062*; D1<-A2 DRILL=0.709* | AA | - | own: partly |
| 4503-16-12-FG | WORK -> WORK | TFA p29 | L5<-L=1.930*; N2<-N=1.290; CHEX<-Y FLATS=1.312*; D1<-A2 DRILL=0.719* | AA | - | own: partly |
| 4503-16-16-FG | WORK -> WORK | TFA p29 | L5<-L=1.930*; N2<-N=1.480; CHEX<-Y FLATS=1.312*; D1<-A2 DRILL=0.938* | AA | - | own: partly |
| 4503-20-20-FG | WORK -> WORK | TFA p29 | L5<-L=2.060*; N2<-N=1.670; CHEX<-Y FLATS=1.625*; D1<-A2 DRILL=1.250* | AA | - | own: partly |
| 4503-24-24-FG | WORK -> WORK | TFA p29 | L5<-L=2.146*; N2<-N=1.770; CHEX<-Y FLATS=1.875*; D1<-A2 DRILL=1.500* | AA | - | own: partly |
| 4601-04-04-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=1.750*; M7<-M=1.030; C4HEX<-C HEX=0.563; Y<-Y FLATS=0.438; D<-B2 DRILL=0.172 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-08-06-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=1.980*; M7<-M=1.250; C4HEX<-C HEX=0.688; Y<-Y FLATS=0.750; D<-B2 DRILL=0.297 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-12-10-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.060*; M7<-M=1.700; C4HEX<-C HEX=1.000; Y<-Y FLATS=1.062; D<-B2 DRILL=0.484 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-16-16-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.394*; M7<-M=2.039; C4HEX<-C HEX=1.500; Y<-Y FLATS=1.312; D<-B2 DRILL=0.844 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-16-20-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.450*; M7<-M=2.230; C4HEX<-C HEX=1.875; Y<-Y FLATS=1.625; D<-B2 DRILL=1.078 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-20-16-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.450*; M7<-M=2.250; C4HEX<-C HEX=1.500; Y<-Y FLATS=1.625; D<-B2 DRILL=0.844 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-20-20-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.375*; M7<-M=2.250; C4HEX<-C HEX=1.875; Y<-Y FLATS=1.750; D<-B2 DRILL=1.078 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-24-20-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.700*; M7<-M=2.380; C4HEX<-C HEX=1.875; Y<-Y FLATS=1.875; D<-B2 DRILL=1.078 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4601-24-24-NWO-FG | WORK -> WORK | TFA p29 | L4<-L=2.697*; M7<-M=2.382; C4HEX<-C HEX=2.125; Y<-Y FLATS=1.875; D<-B2 DRILL=1.312 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 4603-16-16-NWO-FG | WORK -> WORK | TFA p30 | L5<-L=1.960*; M8<-M=1.850; C4HEX<-C HEX=1.500; CHEX<-Y FLATS=1.312*; D<-B2 DRILL=0.844 | AA | Q-NEW-PARKER4300 (partly) | own: partly |
| 5500-08-04-FG | DECIDE -> NOW | TFA p30 | N1<-N1=1.470; N2<-N=1.280; Y<-Y FLATS=0.875; D1<-A1 DRILL=0.531; D2<-A2 DRILL=0.281 | - | Q-B-5500, Q-F1 | own: replaced_by_catalog |
| 5500-24-24-FG | DECIDE -> NOW | TFA p31 | N1<-N1=2.640; N2<-N=2.640; Y<-Y FLATS=1.875; D1<-A1 DRILL=1.500; D2<-A2 DRILL=1.500 | - | Q-B-5500, Q-F1 | own: replaced_by_catalog |
| 5501-02-02-FG | WORK -> WORK | TFA p31 | N4<-N=0.64*; N6<-N1=0.64*; Y<-Y FLATS=0.438; D1<-A1 DRILL=0.188; D2<-A2 DRILL=0.188 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5501-04-04-FG | WORK -> WORK | TFA p31 | N4<-N=0.86*; N6<-N1=0.86*; Y<-Y FLATS=0.562; D1<-A1 DRILL=0.281; D2<-A2 DRILL=0.281 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5501-06-06-FG | WORK -> WORK | TFA p31 | N4<-N=0.95*; N6<-N1=0.95*; Y<-Y FLATS=0.750; D1<-A1 DRILL=0.406; D2<-A2 DRILL=0.406 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5501-08-08-FG | WORK -> WORK | TFA p31 | N4<-N=1.17*; N6<-N1=1.17*; Y<-Y FLATS=0.875; D1<-A1 DRILL=0.531; D2<-A2 DRILL=0.531 | - | Q-F1, Q-B-OTHER-5501 | own: partly |
| 5501-12-12-FG | WORK -> WORK | TFA p31 | N4<-N=1.20*; N6<-N1=1.20*; Y<-Y FLATS=1.062; D1<-A1 DRILL=0.719; D2<-A2 DRILL=0.719 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5501-16-16-FG | WORK -> WORK | TFA p31 | N4<-N=1.480*; N6<-N1=1.480*; Y<-Y FLATS=1.312; D1<-A1 DRILL=0.938; D2<-A2 DRILL=0.938 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5501-20-20-FG | WORK -> WORK | TFA p31 | N4<-N=1.67*; N6<-N1=1.67*; Y<-Y FLATS=1.625; D1<-A1 DRILL=1.250; D2<-A2 DRILL=1.250 | - | Q-F1, Q-B-OTHER-5501 | own: replaced_by_catalog |
| 5502-02-04-FG | DECIDE -> DECIDE | TFA p31 | N<-N=0.900; N1<-N1=0.880; W<-Y FLATS=0.750; D<-A1 DRILL=0.188 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 5502-06-08-FG | DECIDE -> DECIDE | TFA p31 | N<-N=1.280; N1<-N1=1.230; W<-Y FLATS=1.062; D<-A1 DRILL=0.406 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 5502-12-08-FG | DECIDE -> DECIDE | TFA p31 | N<-N=1.590; N1<-N1=1.230; W<-Y FLATS=1.062; D<-A1 DRILL=0.719 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 5502-20-16-FG | DECIDE -> DECIDE | TFA p31 | N<-N=2.380; N1<-N1=1.620; W<-Y FLATS=1.625; D<-A1 DRILL=1.250 | TAPDRILL | Q-B-ELBOW, Q-F1 | own: replaced_by_catalog |
| 5503-16-16-FG | WORK -> WORK | TFA p32 | N4<-N=1.72; N3<-N1=1.12; W<-Y FLATS=1.625; D<-A1 DRILL=0.938* | TAPDRILL | - | own: partly |
| 5503-20-20-FG | WORK -> WORK | TFA p32 | N4<-N=1.80; N3<-N1=1.63; W<-Y FLATS=1.875; D<-A1 DRILL=1.250* | TAPDRILL | - | own: partly |
| 5503-24-24-FG | WORK -> WORK | TFA p32 | N4<-N=2.06; N3<-N1=1.69; W<-Y FLATS=2.562; D<-A1 DRILL=1.500* | TAPDRILL | - | own: partly |
| 5503-32-32-FG | WORK -> WORK | TFA p32 | N4<-N=2.150; N3<-N1=2.190; W<-Y FLATS=2.812; D<-A1 DRILL=1.938* | TAPDRILL | - | own: partly |
| 5504-06-04-FG | STEP -> STEP | TFA p32 | N1_1<-N=1.020; N1_2<-N1=1.010; W<-Y FLATS=0.875 | TAPDRILL1, TAPDRILL2 | - | own: partly |
| 5504-06-06-FG | STEP -> STEP | TFA p32 | N1_1<-N=1.020; N1_2<-N1=1.020; W<-Y FLATS=0.875 | TAPDRILL1, TAPDRILL2 | - | own: partly |
| 5504-08-06-FG | STEP -> STEP | TFA p32 | N1_1<-N=1.230; N1_2<-N1=1.010; W<-Y FLATS=1.062 | TAPDRILL1, TAPDRILL2 | - | own: partly |
| 5504-20-20-FG | STEP -> STEP | TFA p32 | N1_1<-N=1.70; N1_2<-N1=1.70; W<-Y FLATS=1.875 | TAPDRILL1, TAPDRILL2 | - | own: partly |
| 5504-24-24-FG | STEP -> STEP | TFA p32 | N1_1<-N=2.08; N1_2<-N1=2.08; W<-Y FLATS=2.562 | TAPDRILL1, TAPDRILL2 | - | own: partly |

`*` = likely pairing (value carried, flagged). Full per-cell detail (catalog column, pairing reason, OMi cell and comparison, plain-twin evidence, thread callouts) is in `F1a.json`.

## Column pairings (review column <- catalog column)

**1501** (1501-FG, drawing TFA p20 (img1))

- `N1@DRIVE` <- L LGTH - **certain**: drawing p20: L = A1 (male NPTF) tip to the A2 swivel axis; gen_tee SPEC 1501: N1@DRIVE = NPTFM leg, axis crossing to the pipe tip; review rows of the same -FG part number holding a value (Air-Way): 16/22 agree (equal 16, rounding 0); differ: 1501-02-04-FG cat 0.900 vs 1.06; 1501-04-06-FG cat 1.220 vs 1.09; 1501-06-08-FG cat 1.28 vs 1.22 ...
- `M1@DRIVE` <- M LGTH - **certain**: gen_tee SPEC 1501: M1@DRIVE = axis crossing to the NPSM stem tip; catalog M is the shorter swivel-leg column: the two swivel-leg columns differ by the nut-face-to-stem-tip offset TIP_B measured on the in-repo Brennan 1404 STEPs (gen_straight2 NPSM_MEAS: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20/-24/-32 0.42; catalog 0.14/0.19/0.21/0.28/0.35/0.35/0.42/0.42/0.42), and the 45 deg sibling 1503 proves the pair on the in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs (stem tip 0.880 / 1.050 = catalog M1, nut face 1.160 / 1.330 = catalog M); Air-Way 1501 -FG legs are another maker's: review rows of the same -FG part number holding a value (Air-Way): 3/22 agree (equal 1, rounding 2); differ: 1501-02-04-FG cat 0.880 vs 0.79; 1501-04-04-FG cat 0.880 vs 0.79; 1501-04-06-FG cat 0.990 vs 0.95 ...
- `W3@HEX` <- M1 LGTH - **certain**: drawing p20: M1 = A1 axis to the swivel nut face; gen_tee npsm W3@HEX = axis to the nut face; see M1@DRIVE; review rows of the same -FG part number holding a value (Air-Way): 3/22 agree (equal 3, rounding 0); differ: 1501-02-02-FG cat 0.840 vs 0.85; 1501-02-04-FG cat 1.070 vs 0.98; 1501-04-04-FG cat 1.070 vs 0.98 ...
- `CHEX@HEX` <- C HEX - **certain**: drawing: C HEX points at the swivel nut; gen_tee npsm CHEX@HEX = nut hex (must equal NPSM_MEAS AF of the Brennan 1404 STEPs); review rows of the same -FG part number holding a value (Air-Way): 21/22 agree (equal 9, rounding 12); differ: 1501-24-24-FG cat 2.125 vs 1.88
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats (drawing; = OMi Hex Flat on every elbow series with OMi data); gen_tee hex = C1HEX@HEX; review rows of the same -FG part number holding a value (Air-Way): 18/22 agree (equal 4, rounding 14); differ: 1501-02-04-FG cat 0.562 vs 0.5; 1501-04-02-FG cat 0.562 vs 0.5; 1501-04-04-FG cat 0.562 vs 0.5 ...
- `D2@BORE` <- A1 DRILL - **certain**: A1 = the male NPTF end; gen_tee D2@BORE = NPTFM leg bore; review rows of the same -FG part number holding a value (Air-Way): 22/22 agree (equal 2, rounding 20)
- `D@BORE` <- A2 DRILL - **certain**: A2 = the NPSM swivel end; gen_tee D@BORE = NPSMSW leg bore; review rows of the same -FG part number holding a value (Air-Way): 15/22 agree (equal 5, rounding 10); differ: 1501-04-02-FG cat 0.13 vs 0.23; 1501-06-08-FG cat 0.46/0.48 vs 0.45; 1501-08-12-FG cat 0.61 vs 0.63 ... (Air-Way differs by maker; some catalog rows print a range)
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1@DRIVE` <- A2 NPSM

**1502** (1502-FG, drawing TFA p21 (img1))

- `N3@DRIVE` <- L LGTH - **likely**: drawing p21: L = A1 female NPTF port face to the A2 axis; N3 is the table's only pipe-leg column (Air-Way N letters = pipe legs); no SPEC and Air-Way's 1502 legs are another maker's: review rows of the same -FG part number holding a value (Air-Way): 0/2 agree (equal 0, rounding 0); differ: 1502-02-02-FG cat 0.660 vs 0.75; 1502-04-04-FG cat 0.880 vs 0.94; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/13 agree (equal 0, rounding 1); differ: 1502-02-02 cat 0.660 vs 0.69; 1502-04-04 cat 0.880 vs 0.94; 1502-04-06 cat 0.88 vs 1.06 ...
- `M1@DRIVE` <- M LGTH - **certain**: same Air-Way letters and W3-M1 offset as the 1501 table (gen_tee: M1 = stem tip); catalog M = stem tip: the two swivel-leg columns differ by the nut-face-to-stem-tip offset TIP_B measured on the in-repo Brennan 1404 STEPs (gen_straight2 NPSM_MEAS: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20/-24/-32 0.42; catalog 0.14/0.19/0.21/0.28/0.35/0.35/0.42/0.42/0.42), and the 45 deg sibling 1503 proves the pair on the in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs (stem tip 0.880 / 1.050 = catalog M1, nut face 1.160 / 1.330 = catalog M); review rows of the same -FG part number holding a value (Air-Way): 0/2 agree (equal 0, rounding 0); differ: 1502-02-02-FG cat 0.800 vs 0.74; 1502-04-04-FG cat 0.990 vs 0.78
- `W3@HEX` <- M1 LGTH - **certain**: drawing p21: M1 = A1 axis to the nut face; 1501 analogue (W3 = nut face); review rows of the same -FG part number holding a value (Air-Way): 0/2 agree (equal 0, rounding 0); differ: 1502-02-02-FG cat 0.940 vs 0.89; 1502-04-04-FG cat 1.180 vs 0.97
- `CHEX@HEX` <- C HEX - **certain**: drawing: C HEX on the swivel nut; = NPSM_MEAS AF at the same size; review rows of the same -FG part number holding a value (Air-Way): 2/2 agree (equal 0, rounding 2)
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats (1501 analogue C1HEX = body hex); review rows of the same -FG part number holding a value (Air-Way): 1/2 agree (equal 0, rounding 1); differ: 1502-04-04-FG cat 0.750 vs 0.69
- `D@BORE` <- A2 DRILL - **certain**: A2 = the NPSM end, the only drill printed; Air-Way D = the NPSM bore as in 1501; review rows of the same -FG part number holding a value (Air-Way): 1/2 agree (equal 1, rounding 0); differ: 1502-02-02-FG cat 0.110 vs 0.13
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1@DRIVE` <- A2 NPSM

**1503** (1503-FG, drawing TFA p21 (img3))

- `N@DRIVE` <- L LGTH - **certain**: in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs: male pipe leg 1.170 / 1.200 = catalog L; gen_tee SPEC 1503 N@DRIVE = NPTFM leg; review rows of the same -FG part number holding a value (Air-Way): 2/14 agree (equal 0, rounding 2); differ: 1503-02-02-FG cat 0.520 vs 0.63; 1503-04-04-FG cat 0.86 vs 0.91; 1503-06-06-FG cat 0.950 vs 1.12 ...
- `M@DRIVE` <- M1 LGTH - **certain**: in-repo STEPs: stem tip 0.880 / 1.050 = catalog M1; gen_tee SPEC 1503 M@DRIVE = NPSMSW stem tip; review rows of the same -FG part number holding a value (Air-Way): 2/14 agree (equal 0, rounding 2); differ: 1503-04-04-FG cat 0.73 vs 0.72; 1503-06-06-FG cat 0.810 vs 0.95; 1503-08-06-FG cat 0.810 vs 0.88 ...
- `W2@HEX` <- M LGTH - **certain**: in-repo STEPs: nut face 1.160 / 1.330 = catalog M; gen_tee npsm W2@HEX = nut face; review rows of the same -FG part number holding a value (Air-Way): 1/14 agree (equal 0, rounding 1); differ: 1503-02-02-FG cat 0.760 vs 0.75; 1503-04-04-FG cat 0.92 vs 0.91; 1503-06-06-FG cat 1.020 vs 1.2 ...
- `CHEX@HEX` <- C HEX - **certain**: drawing: C HEX on the swivel nut; review rows of the same -FG part number holding a value (Air-Way): 14/14 agree (equal 7, rounding 7)
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats; gen_tee hex = C1HEX@HEX; review rows of the same -FG part number holding a value (Air-Way): 14/14 agree (equal 2, rounding 12)
- `D2@BORE` <- A1 DRILL - **certain**: A1 = male NPTF end; review rows of the same -FG part number holding a value (Air-Way): 14/14 agree (equal 3, rounding 11)
- `D@BORE` <- A2 DRILL - **certain**: A2 = NPSM end; review rows of the same -FG part number holding a value (Air-Way): 1/14 agree (equal 1, rounding 0); differ: 1503-02-02-FG cat 0.150 vs 0.13; 1503-06-06-FG cat 0.340 vs 0.33; 1503-08-06-FG cat 0.340 vs 0.33 ... (Air-Way differs by 0.01-0.02 - another maker)
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1@DRIVE` <- A2 NPSM

**1504** (1504-FG, drawing TFA p22 (img1))

- `N2@DRIVE` <- L LGTH - **likely**: drawing p22: L = A1 female NPTF port face to the 45 deg axis crossing; N2 is the only pipe-leg column; Air-Way's 1504 legs are much longer (another maker): review rows of the same -FG part number holding a value (Air-Way): 0/1 agree (equal 0, rounding 0); differ: 1504-04-04-FG cat 0.69 vs 0.91; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 0/10 agree (equal 0, rounding 0); differ: 1504-02-02 cat 0.470 vs 0.67; 1504-04-04 cat 0.69 vs 0.91; 1504-06-04 cat 0.75 vs 1.06 ...
- `M@DRIVE` <- M1 LGTH - **certain**: same Air-Way letters as the 1503 SPEC (M = stem tip, W2 = nut face); catalog M1 = stem tip (drawing p22, as 1503): the two swivel-leg columns differ by the nut-face-to-stem-tip offset TIP_B measured on the in-repo Brennan 1404 STEPs (gen_straight2 NPSM_MEAS: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20/-24/-32 0.42; catalog 0.14/0.19/0.21/0.28/0.35/0.35/0.42/0.42/0.42), and the 45 deg sibling 1503 proves the pair on the in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs (stem tip 0.880 / 1.050 = catalog M1, nut face 1.160 / 1.330 = catalog M)
- `W2@HEX` <- M LGTH - **certain**: catalog M = axis crossing to the nut face (drawing p22, as 1503); 1503 analogue W2 = nut face
- `CHEX@HEX` <- C HEX - **certain**: drawing: C HEX on the swivel nut; review rows of the same -FG part number holding a value (Air-Way): 1/1 agree (equal 0, rounding 1)
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats; review rows of the same -FG part number holding a value (Air-Way): 0/1 agree (equal 0, rounding 0); differ: 1504-04-04-FG cat 0.750 vs 0.69
- `D@BORE` <- A2 DRILL - **certain**: A2 = NPSM end, the only drill printed; review rows of the same -FG part number holding a value (Air-Way): 1/1 agree (equal 1, rounding 0)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1@DRIVE` <- A2 NPSM

**1601** (1601-FG, drawing TFA p47 (img7))

- `N1@DRIVE` <- L LGTH - **certain**: drawing p47: L = A1 male NPTF branch tip to the run axis; the 1601 L values equal the 1501-FG L values size for size and Air-Way 1601 N1 equals Air-Way plain 1501 N1 (same leg in both families); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 2/9 agree (equal 0, rounding 2); differ: 1601-02-02-02 cat 0.720 vs 0.94; 1601-04-04-04 cat 1.090 vs 1.19; 1601-06-04-04 cat 1.220 vs 1.5 ...
- `W3_2@HEX` <- M LGTH - **certain**: drawing p47: M = A2 swivel nut face to the branch axis; values = 1501 M1 (nut face) size for size; M - M1 = TIP_B
- `W3_3@HEX` <- M LGTH - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature (nut face printed on the A2 side only)
- `M1_3@DRIVE` <- M1 LGTH - **certain**: drawing p47: M1 = branch axis to the A3 stem tip (inside the nut); values = 1501 M (stem tip) size for size; the two swivel-leg columns differ by the nut-face-to-stem-tip offset TIP_B measured on the in-repo Brennan 1404 STEPs (gen_straight2 NPSM_MEAS: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20/-24/-32 0.42; catalog 0.14/0.19/0.21/0.28/0.35/0.35/0.42/0.42/0.42), and the 45 deg sibling 1503 proves the pair on the in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs (stem tip 0.880 / 1.050 = catalog M1, nut face 1.160 / 1.330 = catalog M)
- `M1_2@DRIVE` <- M1 LGTH - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature (stem tip printed on the A3 side only)
- `C3HEX@HEX` <- C HEX - **certain**: drawing p47: C HEX labels the A3 swivel nut; = NPSM_MEAS AF at the same size on every F1a row
- `C2HEX@HEX` <- C HEX - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats; Air-Way C1HEX = body hex (plain 1601-06-04-04: C1HEX 0.88, nut hexes 0.69)
- `D2@BORE` <- A1 DRILL - **certain**: A1 = male NPTF end; Air-Way D2 = the pipe bore (plain rows 0.19/0.28/0.41/0.53 vs A1 DRILL 0.188/0.281/0.406/0.531)
- `D_2@BORE` <- A2 DRILL - **certain**: A2 = NPSM end; Air-Way D_2 = NPSM bore
- `D3@BORE` <- A3 DRILL - **certain**: A3 = NPSM end; Air-Way D3 = NPSM bore
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1_2@DRIVE` <- A2 NPSM, `THDMAJ_A1_3@DRIVE` <- A3 NPSM

**1602** (1602-FG, drawing TFA p48 (img1))

- `N3@DRIVE` <- L LGTH - **likely**: drawing p48: L = A1 female NPTF port face to the run axis; L values equal the 1502-FG L values size for size; N3 = the only pipe-leg column (as 1502)
- `W3_2@HEX` <- M LGTH - **certain**: drawing p48: M = A2 nut face to the branch axis; values = 1502 M1 (nut face) size for size; M - M1 = TIP_B
- `W3_3@HEX` <- M LGTH - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature (nut face printed on the A2 side only)
- `M1_3@DRIVE` <- M1 LGTH - **certain**: drawing p48: M1 = branch axis to the A3 stem tip; values = 1502 M (stem tip) size for size; the two swivel-leg columns differ by the nut-face-to-stem-tip offset TIP_B measured on the in-repo Brennan 1404 STEPs (gen_straight2 NPSM_MEAS: -02 0.14, -04 0.19, -06 0.22, -08 0.28, -12 0.33, -16 0.35, -20/-24/-32 0.42; catalog 0.14/0.19/0.21/0.28/0.35/0.35/0.42/0.42/0.42), and the 45 deg sibling 1503 proves the pair on the in-repo Brennan 1503-08-08-FG / 1503-12-08-FG STEPs (stem tip 0.880 / 1.050 = catalog M1, nut face 1.160 / 1.330 = catalog M)
- `M1_2@DRIVE` <- M1 LGTH - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature (stem tip printed on the A3 side only)
- `C3HEX@HEX` <- C HEX - **certain**: drawing p48: C HEX labels the A3 swivel nut; = NPSM_MEAS AF at the same size
- `C2HEX@HEX` <- C HEX - **likely**: symmetry: A2 = A3 on every catalog row of this table and the catalog prints one value per feature
- `C1HEX@HEX` <- Y FLATS - **certain**: Y FLATS = forged body flats (Air-Way C1HEX = body hex, as 1601)
- `D2@BORE` <- A2 DRILL - **certain**: A2 = NPSM end; Air-Way D2 = swivel bore (plain 1602-06-06-06: D2 0.33, tap drill 0.57)
- `D3@BORE` <- A3 DRILL - **certain**: A3 = NPSM end; Air-Way D3 = swivel bore
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A1 NPTF, `THDMAJ_A1_2@DRIVE` <- A2 NPSM, `THDMAJ_A1_3@DRIVE` <- A3 NPSM

**1603** (1603-FG, drawing TFA p48 (img3))

- `W3@HEX` <- L LGTH - **likely**: drawing p48: L = A1 (branch) nut face to the run axis (1603-08-06-06: L 1.39 = the -08 nut face of 1501-08-08-FG); every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `M1@DRIVE` <- M2 LGTH - **likely**: leg-1 stem tip is not printed; taken from the A3 stem tip M2 by symmetry: every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `M2_2@DRIVE` <- M1 LGTH - **likely**: drawing p48: M1 = run axis to the A2 stem tip (inner dimension); every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `W5_2@HEX` <- M LGTH - **likely**: leg-2 nut face is not printed; taken from the A3 nut face M by symmetry: every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `M2_3@DRIVE` <- M2 LGTH - **certain**: drawing p48: M2 = run axis to the A3 stem tip (inside M); M - M2 = TIP_B (1603-06-06-08: 1.39 - 1.11 = 0.28 = -08)
- `W5_3@HEX` <- M LGTH - **certain**: drawing p48: M = run axis to the A3 nut face
- `C_1HEX@HEX` <- C HEX - **certain**: drawing p48: C HEX labels the A1 (branch) nut; 1603-06-06-08 / -08-06-06 rows: C HEX = the A1 NPSM nut size
- `C3HEX@HEX` <- C1 HEX - **likely**: drawing p48: C 1HEX labels the A3 nut (1603-06-06-08: C1 HEX 1.000 = the -08 A3 nut; but 1603-16-12-16 prints the -12 nut) - same value on the F1a rows
- `C2HEX@HEX` <- C1 HEX - **likely**: every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `C1HEX@HEX` <- Y Flats - **certain**: Y Flats = forged body flats (Air-Way C1HEX = body hex, as 1601)
- `D1@BORE` <- A1 DRILL - **likely**: Air-Way 1603 has two bore columns (D1, D2) for three ends; every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- `D2@BORE` <- A2 DRILL - **likely**: every same-dash 1603 catalog row prints L = M, M1 = M2, C HEX = C1 HEX and three equal drills, so all three swivel legs are alike and the reading of Air-Way's leg numbers (un-suffixed = leg 1, _2 / _3 = legs 2 / 3) changes no value
- thread callouts (size check only): `THDMAJ_A1_1@DRIVE` <- A1 NPSM, `THDMAJ_A1_2@DRIVE` <- A2 NPSM, `THDMAJ_A1_3@DRIVE` <- A3 NPSM

**1703** (1703-FG, drawing Flange p4 (forged 1703-FG drawing))

- `M2@DRIVE` <- L1 (in.) - **likely**: Flange drawing p4: L1 = end-1 (JIC) tip to the flange-leg axis crossing; Air-Way M letters are the male JIC legs in every other Air-Way elbow table (2501 M, 2503 M2, 2702 M2); no Air-Way or OMi value exists in this table to test it
- `N3@DRIVE` <- L2 (in.) - **likely**: Flange drawing p4: L2 = flange face to the JIC-leg axis crossing; N3 = the table's other (flange) leg column; Air-Way M letters are the male JIC legs in every other Air-Way elbow table (2501 M, 2503 M2, 2702 M2); no Air-Way or OMi value exists in this table to test it
- `CHEX@HEX` <- A/F (in.) - **certain**: A/F = forged body across flats (drawing p4); CHEX is the table's only hex column (1700 SPEC: CHEX@HEX = body hex)
- `O@DRIVE` - not printed (end_library): code 61 flange head OD: not in the Flange catalog tables; source = FLG61 end library (in-repo Brennan 1700 STEPs: head OD by flange size; Q-TRANSFER-ENDLIB)
- `D@BORE` - not printed (step): through bore: the Flange catalog prints no bore for the forged elbows - only a STEP (pilot) gives it
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- 1 THREAD

**1704** (1704-FG, drawing Flange p5 (forged 1704-FG drawing))

- `M@DRIVE` <- L1 (in.) - **likely**: Flange drawing p5: L1 = end-1 (JIC) tip to the flange-leg axis; Air-Way M letters are the male JIC legs in every other Air-Way elbow table (2501 M, 2503 M2, 2702 M2); no Air-Way or OMi value exists in this table to test it
- `N2@DRIVE` <- L2 (in.) - **likely**: Flange drawing p5: L2 = flange face to the JIC-leg axis; N2 = the other (flange) leg column; Air-Way M letters are the male JIC legs in every other Air-Way elbow table (2501 M, 2503 M2, 2702 M2); no Air-Way or OMi value exists in this table to test it
- `Y@HEX` <- A/F (in.) - **certain**: A/F = forged body across flats (drawing p5); Y is the table's only hex column
- `O@DRIVE` - not printed (end_library): code 61 flange head OD: not in the Flange catalog tables; source = FLG61 end library (in-repo Brennan 1700 STEPs: head OD by flange size; Q-TRANSFER-ENDLIB)
- `D@BORE` - not printed (step): through bore: the Flange catalog prints no bore for the forged elbows - only a STEP (pilot) gives it
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- 1 THREAD

**2500** (2500-FG, drawing TFA p22 (img3))

- `M1@DRIVE` <- M1 LGTH - **certain**: drawing p22: M1 = B1 tip to the B2 axis; in-repo Brennan 2500-06-06-FG STEP 1.06; review rows of the same -FG part number holding a value (Air-Way): 11/11 agree (equal 11, rounding 0) (incl. the unequal 2500-10-08-FG / -16-12-FG)
- `M2@DRIVE` <- M2 LGTH - **certain**: drawing p22: M2 = B2 tip to the B1 axis; STEP 1.06; review rows of the same -FG part number holding a value (Air-Way): 11/11 agree (equal 11, rounding 0)
- `Y@REF` <- Y FLATS - **certain**: body flats; STEP flats 0.5626 = 0.562; review rows of the same -FG part number holding a value (Air-Way): 11/11 agree (equal 2, rounding 9)
- `D1@BORE` <- B1 DRILL - **certain**: B1 end drill; review rows of the same -FG part number holding a value (Air-Way): 11/11 agree (equal 0, rounding 11)
- `D2@BORE` <- B2 DRILL - **certain**: B2 end drill; review rows of the same -FG part number holding a value (Air-Way): 11/11 agree (equal 0, rounding 11)
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_B2@DRIVE` <- B2 SAE 37Deg

**2501** (2501-FG, drawing TFA p23)

- `M@DRIVE` <- M LGTH - **certain**: drawing p23: M = male JIC (B1) tip to the A2-leg axis; catalog M = OMi M 1 Size certain 44/44 (M1) (OMi M1 -> M@DRIVE = mapping M071); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 33/34 agree (equal 33, rounding 0); differ: 2501-20-24-FG cat 2.20 vs 2.3
- `N@DRIVE` <- L LGTH - **certain**: drawing p23: L = male pipe (A2) tip to the B1-leg axis; catalog L = OMi L 1 Size certain 44/44 (L1) (M072); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 33/34 agree (equal 33, rounding 0); differ: 2501-04-02-FG cat 0.78 vs 0.76
- `Y@REF` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 44/44 (HexFlat) (M073); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 34/34 agree (equal 7, rounding 27)
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; = OMi Side 1 ID certain 44/44 (S1ID) (M074); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 34/34 agree (equal 0, rounding 34)
- `D1@DRILL` <- A2 DRILL - **certain**: pipe end drill; = OMi Side 2 ID certain 43/44 (S2ID) (M075); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 34/34 agree (equal 7, rounding 27)
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- B1 SAE 37Deg, `PIPEOD@DRIVE` <- A2 NPTF

**2501L** (2501-L-FG, drawing TFA p24 (img1))

- `M@DRIVE` <- MLGTH - **certain**: drawing p24: same letters as 2501 (M = JIC leg); in-repo Brennan 2501-L-06-04-FG STEP 1.06; = OMi M 1 certain 13/13 (M1) (M076); review rows of the same -FG part number holding a value (Air-Way): 3/3 agree (equal 3, rounding 0)
- `N3@DRIVE` <- L LGTH - **certain**: drawing p24: L = long pipe leg; STEP 1.58; = OMi L 1 certain 12/13 (L1) (M077); gen_tee fold 2501L N3 -> N; review rows of the same -FG part number holding a value (Air-Way): 2/3 agree (equal 2, rounding 0); differ: 2501-L-04-02-FG cat 1.170 vs 1.19
- `Y@REF` <- Y FLATS - **certain**: body flats; STEP flats 0.5626; = OMi Hex Flat certain 13/13 (HexFlat); review rows of the same -FG part number holding a value (Air-Way): 3/3 agree (equal 1, rounding 2)
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; = OMi Side 1 ID certain 13/13 (S1ID); review rows of the same -FG part number holding a value (Air-Way): 3/3 agree (equal 0, rounding 3)
- `D1@BORE` <- A2 DRILL - **certain**: pipe end drill; = OMi Side 2 ID certain 13/13 (S2ID); review rows of the same -FG part number holding a value (Air-Way): 3/3 agree (equal 0, rounding 3)
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF

**2501LL** (2501-LL-FG, drawing TFA p24 (img3))

- `M@DRIVE` <- M LGTH - **certain**: drawing p24: same letters as 2501 / 2501-L (M = JIC leg); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 11/14 agree (equal 11, rounding 0); differ: 2501-LL-04-04 cat 1.050 vs 0.95; 2501-LL-06-06 cat 1.14 vs 1.16; 2501-LL-08-08 cat 1.330 vs 1.31
- `N4@DRIVE` <- L LGTH - **certain**: drawing p24: L = extra-long pipe leg; Air-Way N4 = the 2501-LL long leg (2501L analogue N3 = L, STEP-proven); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 9/14 agree (equal 9, rounding 0); differ: 2501-LL-05-02 cat 1.56 vs 1.59; 2501-LL-06-08 cat 2.870 vs 2.88; 2501-LL-08-08 cat 2.870 vs 2.88 ...
- `Y@REF` <- Y FLATS - **certain**: body flats; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/14 agree (equal 0, rounding 1); differ: 2501-LL-04-02 cat 0.438 vs 0.5; 2501-LL-04-04 cat 0.562 vs 0.63; 2501-LL-06-04 cat 0.562 vs 0.63 ...
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 14/14 agree (equal 0, rounding 14)
- `D1@BORE` <- A2 DRILL - **certain**: pipe end drill; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 14/14 agree (equal 1, rounding 13)
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF

**2502** (2502-FG, drawing TFA p25 (img3))

- `M1@DRIVE` <- M LGTH - **certain**: drawing p25: M = male JIC tip to the A2 axis; in-repo Brennan 2502-06-04-FG STEP 1.23; = OMi M 1 certain 20/20 (M1) (M081); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 10, rounding 0)
- `N1@DRIVE` <- L LGTH - **certain**: drawing p25: L = female pipe port face to the B1 axis; STEP 0.88; = OMi L 1 certain 20/20 (L1) (M082); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 10, rounding 0)
- `Y1@DRIVE` <- Y FLATS - **certain**: body flats; STEP flats 0.750; = OMi Hex Flat certain 20/20 (HexFlat) (M083); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 2, rounding 8)
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; = OMi Side 1 ID certain 20/20 (S1ID) (M084); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 0, rounding 10)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF

**2503** (2503-FG, drawing TFA p26 (img1))

- `M2@DRIVE` <- M LGTH - **certain**: drawing p26: M = B1 (JIC) leg to the axis crossing; = OMi M 1 certain 31/31 (M1) (M085); gen_tee SPEC 2503 M2@DRIVE = JICM leg; review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 26/30 agree (equal 26, rounding 0); differ: 2503-04-08-FG cat 0.870 vs 1.17; 2503-06-06-FG cat 0.870 vs 0.91; 2503-08-08-FG cat 0.99 vs 1.11 ...
- `N2@DRIVE` <- L LGTH - **certain**: drawing p26: L = A2 (pipe) leg along the 45 deg axis; = OMi L 1 certain 31/31 (L1) (M086); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 26/30 agree (equal 26, rounding 0); differ: 2503-04-08-FG cat 1.170 vs 0.89; 2503-05-04-FG cat 0.860 vs 0.88; 2503-10-12-FG cat 1.20 vs 1.16 ...
- `Y@REF` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 31/31 (HexFlat); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 30/30 agree (equal 5, rounding 25)
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; = OMi Side 1 ID certain 31/31 (S1ID); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 30/30 agree (equal 0, rounding 30)
- `D1@BORE` <- A2 DRILL - **certain**: pipe end drill; = OMi Side 2 ID certain 31/31 (S2ID); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 30/30 agree (equal 4, rounding 26)
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF

**2504** (2504-FG, drawing TFA p26 (img3))

- `M2_1@DRIVE` <- M1 LGTH - **likely**: drawing p26: M1 = B1 leg; in-repo Brennan 2504-08-08-FG STEP: both legs 0.980 = catalog; = OMi M 1 likely 6/6 (M1) (M090); the Air-Way M2(1) datum is undocumented (mapping_final M090); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/6 agree (equal 6, rounding 0)
- `M2_2@DRIVE` <- M2 LGTH - **likely**: drawing p26: M2 = B2 leg (45 deg); STEP 0.980; = OMi M 2 likely 6/6 (M2) (M091); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/6 agree (equal 1, rounding 0); differ: 2504-04-04 cat 0.72 vs 0.8; 2504-06-06 cat 0.83 vs 0.88; 2504-08-08 cat 0.98 vs 1.1 ...
- `Y@HEX` <- Y FLATS - **certain**: body flats; STEP flats 0.750; = OMi Hex Flat certain 6/6 (HexFlat) (M092); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 0/6 agree (equal 0, rounding 0); differ: 2504-04-04 cat 0.438 vs 0.5; 2504-06-06 cat 0.562 vs 0.63; 2504-08-08 cat 0.750 vs 0.81 ...
- `D1@BORE` <- B1 DRILL - **certain**: B1 end drill; = OMi Side 1 ID likely 6/6 (S1ID) (M093); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/6 agree (equal 0, rounding 6)
- `D2@BORE` <- B2 DRILL - **certain**: B2 end drill; = OMi Side 2 ID likely 6/6 (S2ID) (M094); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/6 agree (equal 0, rounding 6)
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_B2@DRIVE` <- B2 SAE 37Deg

**2505** (2505-FG, drawing TFA p27 (img1))

- `M2@DRIVE` <- M LGTH - **certain**: drawing p27: M = B1 (male JIC) leg; = OMi M 1 certain 8/8 (M1); OMi M1 -> M2@DRIVE (M095); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 0/5 agree (equal 0, rounding 0); differ: 2505-04-04 cat 0.870 vs 0.88; 2505-06-06 cat 0.88 vs 1.06; 2505-08-08 cat 1.04 vs 1.28 ...
- `N6@DRIVE` <- N LGTH - **certain**: drawing p27: N = A2 female pipe port face along the 45 deg axis; = OMi M 2 certain 8/8 (M2); OMi M2 -> N6@DRIVE (M096); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/5 agree (equal 0, rounding 1); differ: 2505-04-04 cat 0.620 vs 0.63; 2505-06-06 cat 0.75 vs 0.72; 2505-08-08 cat 0.94 vs 0.91 ...
- `Y1@HEX` <- Y FLATS - **certain**: body flats (only hex); = OMi Hex Flat certain 8/8 (HexFlat) (M097); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 3/5 agree (equal 1, rounding 2); differ: 2505-08-08 cat 1.062 vs 1.13; 2505-12-12 cat 1.312 vs 1.38
- `D@BORE` <- B1 DRILL - **certain**: JIC end drill; = OMi Side 1 ID certain 8/8 (S1ID) (M098); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/5 agree (equal 0, rounding 5)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF

**2601** (2601-FG, drawing TFA p48 (img5))

- `M1@DRIVE` <- M1 LGTH - **certain**: drawing p48: M1 = B1 run leg; gen_tee SPEC 2601 leg 1 JICM M1@DRIVE; = OMi M 1 likely 14/14 (M1) (M166); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 10, rounding 0)
- `M2@DRIVE` <- M2 LGTH - **certain**: drawing p48: M2 = B2 run leg; = OMi M 2 likely 14/14 (M2) (M167); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 10, rounding 0)
- `N@DRIVE` <- L LGTH - **certain**: drawing p48: L = A3 male pipe branch tip to the run axis; SPEC NPTFM N@DRIVE; = OMi L 1 certain 14/14 (L1) (M168); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 10, rounding 0)
- `Y@REF` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 14/14 (HexFlat) (M169); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 2, rounding 8)
- `D1@BORE` <- B1 DRILL - **certain**: = OMi Side 1 ID likely 14/14 (S1ID) (M170); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 0, rounding 10)
- `D2@BORE` <- B2 DRILL - **certain**: = OMi Side 2 ID likely 14/14 (S2ID) (M171); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 0, rounding 10)
- `DDRILL@BORE` <- A3 DRILL - **certain**: pipe branch drill; = OMi Side 3 ID certain 14/14 (S3ID) (M172); review rows of the same -FG part number holding a value (Air-Way): 10/10 agree (equal 1, rounding 9)
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_B2@DRIVE` <- B2 SAE 37Deg, `THDMAJ_A@DRIVE` <- A3 NPTF

**2602** (2602-FG, drawing TFA p49 (img1))

- `M1_1@DRIVE` <- M1 LGTH - **certain**: drawing p49: M1 = B1 run leg; = OMi M 1 likely 10/10 (M1) (M173); review rows of the same -FG part number holding a value (Air-Way): 8/8 agree (equal 8, rounding 0)
- `M1_2@DRIVE` <- M2 LGTH - **certain**: drawing p49: M2 = B2 run leg; = OMi M 2 likely 10/10 (M2) (M174); review rows of the same -FG part number holding a value (Air-Way): 8/8 agree (equal 8, rounding 0)
- `N1@DRIVE` <- N LGTH - **certain**: drawing p49: N = A3 female branch port face to the run axis; = OMi L 1 certain 10/10 (L1) (M175); review rows of the same -FG part number holding a value (Air-Way): 8/8 agree (equal 8, rounding 0)
- `Y1@DRIVE` <- Y FLATS - **certain**: drawing p49: Y FLATS labels the forged body; = OMi Hex Flat certain 10/10 (HexFlat) (M176); review rows of the same -FG part number holding a value (Air-Way): 7/8 agree (equal 2, rounding 5); differ: 2602-24-24-24-FG cat 2.562 vs 2.57
- `D1@BORE` <- B1 DRILL - **certain**: = OMi Side 1 ID likely 10/10 (S1ID) (M177); review rows of the same -FG part number holding a value (Air-Way): 8/8 agree (equal 0, rounding 8)
- `D2@BORE` <- B2 DRILL - **certain**: = OMi Side 2 ID likely 10/10 (S2ID) (M178); review rows of the same -FG part number holding a value (Air-Way): 8/8 agree (equal 0, rounding 8)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_B2@DRIVE` <- B2 SAE 37Deg, `THDMAJ_A@DRIVE` <- A3 NPTF

**2606** (2606-FG, drawing TFA p51 (img1))

- `M1_1@DRIVE` <- M LGTH - **certain**: drawing p51: M = B1 (side-1 JIC run) tip to the branch axis; = OMi M 1 likely 10/10 (M1) (M193); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/7 agree (equal 4, rounding 1); differ: 2606-04-04-04 cat 1.22 vs 1.02; 2606-08-08-08 cat 1.520 vs 1.55
- `N1@DRIVE` <- L LGTH - **certain**: drawing p51: L = A2 (side-2 female pipe run) port face to the branch axis; = OMi M 2 certain 10/10 (M2) (M194, discriminating rows); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/7 agree (equal 7, rounding 0)
- `M1_3@DRIVE` <- N LGTH - **certain**: drawing p51: N = B3 (side-3 JIC branch) tip to the run axis; = OMi L 1 likely 10/10 (L1) (M195); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/7 agree (equal 4, rounding 1); differ: 2606-04-04-04 cat 1.22 vs 1.02; 2606-08-08-08 cat 1.520 vs 1.55
- `Y1@HEX` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 10/10 (HexFlat) (M196); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/7 agree (equal 2, rounding 4); differ: 2606-08-08-08 cat 1.062 vs 1.13
- `D1@BORE` <- B1 DRILL - **certain**: = OMi Side 1 ID likely 10/10 (S1ID) (M197); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/7 agree (equal 0, rounding 7)
- `D3@BORE` <- B3 DRILL - **certain**: = OMi Side 3 ID likely 10/10 (S3ID) (M198); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/7 agree (equal 0, rounding 7)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A@DRIVE` <- A2 NPTF, `THDMAJ_B3@DRIVE` <- BE SAE 37Deg

**2611** (2611-FG, drawing TFA p52 (img5))

- `M1@DRIVE` <- M LGTH - **certain**: drawing p52: M = B1 (side-1 JIC run) tip to the branch axis; = OMi M 1 certain 5/5 (M1) (M204); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/5 agree (equal 1, rounding 0); differ: 2611-04-04-04 cat 1.220 vs 1.01; 2611-06-06-06 cat 1.310 vs 1.19; 2611-08-06-06 cat 1.42 vs 1.28 ...
- `N5@DRIVE` <- L LGTH - **certain**: drawing p52: L = A2 (side-2 male pipe run) tip to the branch axis; = OMi M 2 certain 5/5 (M2) (M205); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 3/5 agree (equal 3, rounding 0); differ: 2611-06-06-06 cat 1.220 vs 1.25; 2611-08-06-06 cat 1.22 vs 1.25
- `N1@DRIVE` <- L1 LGTH - **certain**: drawing p52: L1 = A3 (side-3 female branch) port face to the run axis; = OMi L 1 certain 5/5 (L1) (M206); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/5 agree (equal 5, rounding 0)
- `Y1@HEX` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 5/5 (HexFlat) (M207); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 4/5 agree (equal 1, rounding 3); differ: 2611-12-12-12 cat 1.312 vs 1.38
- `D@BORE` <- B1 DRILL - **certain**: = OMi Side 1 ID certain 5/5 (S1ID) (M208); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/5 agree (equal 0, rounding 5)
- `D1@BORE` <- A2 DRILL - **certain**: = OMi Side 2 ID certain 5/5 (S2ID) (M209); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/5 agree (equal 0, rounding 5)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B1 SAE 37Deg, `THDMAJ_A2@DRIVE` <- A2 NPTF, `THDMAJ_A3@DRIVE` <- A3 NPTF

**2702** (2702-FG, drawing TFA p27 (img5))

- `M2@DRIVE` <- M LGTH - **certain**: drawing p27: M = B1 JIC leg; gen_tee SPEC 2702 leg 1 JICM M2@DRIVE; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 6, rounding 0)
- `M9@DRIVE` <- L LGTH - **certain**: drawing p27: L = B2 bulkhead leg along the 45 deg axis; SPEC JICBH M9@DRIVE; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 6, rounding 0)
- `Y@HEX` <- Y FLATS - **certain**: body flats; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 1, rounding 5)
- `D1@BORE` <- B1 DRILL - **certain**: review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 0, rounding 6)
- `D2@BORE` <- B2 DRILL - **certain**: review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 0, rounding 6)
- `i2@DRIVE` - not printed (step): bulkhead collar / relief (Air-Way i2 / K1 / O): not printed in the TFA catalog - only the STEP gives them
- `K1@DRIVE` - not printed (step): bulkhead collar / relief (Air-Way i2 / K1 / O): not printed in the TFA catalog - only the STEP gives them
- `O@DRIVE` - not printed (step): bulkhead collar / relief (Air-Way i2 / K1 / O): not printed in the TFA catalog - only the STEP gives them
- thread callouts (size check only): `THDMAJ_B1@DRIVE` <- B1 SAE 37Deg, `THDMAJ_B2@DRIVE` <- B2 SAE 37Deg

**4501** (4501-FG, drawing TFA p28 (img3))

- `L4@DRIVE` <- L LGTH - **likely**: drawing p28: L = B1 hose-barb tip to the A2 axis; L4 = the table's hose-leg column; Air-Way plain legs run 0.04-0.2 shorter: plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 1/28 agree (equal 1, rounding 0); differ: 4501-04-02 cat 1.810 vs 1.75; 4501-04-04 cat 1.850 vs 1.81; 4501-05-02-SHORT cat 1.750 vs 1 ...
- `N@DRIVE` <- N LGTH - **certain**: drawing p28: N = A2 male pipe tip to the B1 axis; review rows of the same -FG part number holding a value (Air-Way): 1/1 agree (equal 1, rounding 0); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 17/28 agree (equal 11, rounding 6); differ: 4501-04-02 cat 0.750 vs 0.78; 4501-06-02 cat 0.900 vs 0.78; 4501-08-04 cat 1.220 vs 1.09 ...
- `Y@HEX` <- Y FLATS - **certain**: body flats (only hex); review rows of the same -FG part number holding a value (Air-Way): 1/1 agree (equal 1, rounding 0); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 3/28 agree (equal 0, rounding 3); differ: 4501-04-02 cat 0.438 vs 0.5; 4501-05-02 cat 0.437 vs 0.5; 4501-05-02-SHORT cat 0.437 vs 0.5 ...
- `D1@BORE` <- A2 DRILL - **likely**: Air-Way D1 equals the pipe-end drill A2 (not the barb drill B1) on the plain twins: plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 27/28 agree (equal 5, rounding 22); differ: 4501-10-12 cat 0.709 vs 0.72
- `AA@DRIVE` - not printed (end_library): hose bead diameter: the catalog prints only the hose size (B1 TUBE O.D.); source = the hose-barb end library (Air-Way AA per hose size, 4404 end_HOSEB; Q-NEW-HOSEB / Q-TRANSFER-ENDLIB) or the part STEP
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A2 NPTF

**4503** (4503-FG, drawing TFA p29 (img1))

- `L5@DRIVE` <- L LGTH - **likely**: drawing p29: L = B1 hose-barb tip to the 45 deg axis crossing; L5 = the hose-leg column; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 2/19 agree (equal 1, rounding 1); differ: 4503-04-02 cat 1.562 vs 1.68; 4503-04-04 cat 1.810 vs 1.7; 4503-08-06 cat 1.687 vs 1.74 ...
- `N2@DRIVE` <- N LGTH - **certain**: drawing p29: N = A2 male pipe leg along the 45 deg axis; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 14/19 agree (equal 13, rounding 1); differ: 4503-04-04 cat 0.830 vs 0.86; 4503-10-06 cat 0.980 vs 0.95; 4503-16-12 cat 1.290 vs 1.75 ...
- `CHEX@HEX` <- Y FLATS - **likely**: CHEX is the table's only hex column; Y FLATS = forged body flats; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/19 agree (equal 4, rounding 3); differ: 4503-06-04 cat 0.562 vs 0.63; 4503-08-08 cat 0.875 vs 0.94; 4503-10-06 cat 0.875 vs 0.81 ...
- `D1@BORE` <- A2 DRILL - **likely**: Air-Way D1 = the pipe-end drill on the plain twins: plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 15/19 agree (equal 3, rounding 12); differ: 4503-10-12 cat 0.719 vs 0.64; 4503-12-12 cat 0.709 vs 0.64; 4503-16-12 cat 0.719 vs 0.64 ...
- `AA@DRIVE` - not printed (end_library): hose bead diameter: the catalog prints only the hose size (B1 TUBE O.D.); source = the hose-barb end library (Air-Way AA per hose size, 4404 end_HOSEB; Q-NEW-HOSEB / Q-TRANSFER-ENDLIB) or the part STEP
- thread callouts (size check only): `THDMAJ_A@DRIVE` <- A2 NPTF

**4601** (4601-NWO-FG, drawing TFA p29 (img3))

- `L4@DRIVE` <- L LGTH - **likely**: drawing p29: L = B1 hose-barb tip to the B2 axis; L4 = hose-leg column; Air-Way's own " NWO-FG" rows differ on this leg: review rows of the same -FG part number holding a value (Air-Way): 2/7 agree (equal 0, rounding 2); differ: 4601-08-08 NWO-FG cat 1.980 vs 1.91; 4601-10-08 NWO-FG cat 1.980 vs 1.91; 4601-10-10 NWO-FG cat 2.055 vs 1.97 ...; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/27 agree (equal 4, rounding 2); differ: 4601-05-04 NWO cat 1.810 vs 1.75; 4601-06-04 NWO cat 1.810 vs 1.75; 4601-06-08 NWO cat 1.980 vs 1.91 ...
- `M7@DRIVE` <- M LGTH - **certain**: drawing p29: M = B2 adjustable-ORB tip to the B1 axis; review rows of the same -FG part number holding a value (Air-Way): 5/7 agree (equal 2, rounding 3); differ: 4601-06-06 NWO-FG cat 1.240 vs 1.25; 4601-16-12 NWO-FG cat 2.051 vs 2.04; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 10/27 agree (equal 7, rounding 3); differ: 4601-04-06 NWO cat 1.270 vs 1.25; 4601-05-06 NWO cat 1.240 vs 1.25; 4601-06-04 NWO cat 1.190 vs 1.03 ...
- `C4HEX@HEX` <- C HEX - **certain**: drawing p29: C HEX = the ORB locknut; review rows of the same -FG part number holding a value (Air-Way): 6/7 agree (equal 4, rounding 2); differ: 4601-10-08 NWO-FG cat 0.750 vs 0.88; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 26/27 agree (equal 11, rounding 15); differ: 4601-10-08 NWO cat 0.750 vs 0.88
- `Y@HEX` <- Y FLATS - **certain**: body flats; review rows of the same -FG part number holding a value (Air-Way): 3/7 agree (equal 0, rounding 3); differ: 4601-08-08 NWO-FG cat 0.750 vs 0.81; 4601-10-10 NWO-FG cat 0.875 vs 0.94; 4601-16-12 NWO-FG cat 1.312 vs 1.06 ...; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/27 agree (equal 2, rounding 3); differ: 4601-04-04 NWO cat 0.438 vs 0.5; 4601-05-04 NWO cat 0.562 vs 0.5; 4601-05-06 NWO cat 0.562 vs 0.63 ...
- `D@BORE` <- B2 DRILL - **certain**: Air-Way D = the ORB-end drill B2: review rows of the same -FG part number holding a value (Air-Way): 7/7 agree (equal 0, rounding 7); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 27/27 agree (equal 0, rounding 27)
- `AA@DRIVE` - not printed (end_library): hose bead diameter: the catalog prints only the hose size (B1 TUBE O.D.); source = the hose-barb end library (Air-Way AA per hose size, 4404 end_HOSEB; Q-NEW-HOSEB / Q-TRANSFER-ENDLIB) or the part STEP
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B2 AORB

**4603** (4603-NWO-FG, drawing TFA p30 (img1))

- `L5@DRIVE` <- L LGTH - **likely**: drawing p30: L = B1 hose-barb tip to the 45 deg crossing; L5 = hose-leg column; review rows of the same -FG part number holding a value (Air-Way): 1/6 agree (equal 0, rounding 1); differ: 4603-06-06 NWO-FG cat 1.681 vs 1.69; 4603-08-06 NWO-FG cat 1.760 vs 1.61; 4603-08-08 NWO-FG cat 1.625 vs 1.69 ...; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 2/21 agree (equal 1, rounding 1); differ: 4603-06-04 NWO cat 1.681 vs 1.61; 4603-06-06 NWO cat 1.681 vs 1.69; 4603-08-06 NWO cat 1.760 vs 1.61 ...
- `M8@DRIVE` <- M LGTH - **certain**: drawing p30: M = B2 adjustable-ORB leg along the 45 deg axis; review rows of the same -FG part number holding a value (Air-Way): 2/6 agree (equal 0, rounding 2); differ: 4603-06-06 NWO-FG cat 1.146 vs 1.14; 4603-08-06 NWO-FG cat 1.300 vs 1.14; 4603-12-10 NWO-FG cat 1.530 vs 1.52 ...; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/21 agree (equal 3, rounding 4); differ: 4603-06-04 NWO cat 1.100 vs 1.05; 4603-06-06 NWO cat 1.146 vs 1.14; 4603-08-06 NWO cat 1.300 vs 1.14 ...
- `C4HEX@HEX` <- C HEX - **certain**: drawing p30: C HEX = the ORB locknut; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 2, rounding 4); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 21/21 agree (equal 10, rounding 11)
- `CHEX@HEX` <- Y FLATS - **likely**: CHEX = the body hex column (C4HEX is the locknut); Y FLATS = body flats; review rows of the same -FG part number holding a value (Air-Way): 2/6 agree (equal 0, rounding 2); differ: 4603-06-06 NWO-FG cat 0.562 vs 0.63; 4603-08-06 NWO-FG cat 0.750 vs 0.63; 4603-08-08 NWO-FG cat 0.812 vs 0.75 ...; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 2/21 agree (equal 0, rounding 2); differ: 4603-04-04 NWO cat 0.438 vs 0.5; 4603-06-04 NWO cat 0.562 vs 0.5; 4603-06-06 NWO cat 0.562 vs 0.63 ...
- `D@BORE` <- B2 DRILL - **certain**: Air-Way D = the ORB-end drill B2: review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 0, rounding 6); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 21/21 agree (equal 0, rounding 21)
- `AA@DRIVE` - not printed (end_library): hose bead diameter: the catalog prints only the hose size (B1 TUBE O.D.); source = the hose-barb end library (Air-Way AA per hose size, 4404 end_HOSEB; Q-NEW-HOSEB / Q-TRANSFER-ENDLIB) or the part STEP
- thread callouts (size check only): `THDMAJ_B@DRIVE` <- B2 AORB

**5500** (5500-FG, drawing TFA p30 (img3))

- `N1@DRIVE` <- N1 LGTH - **certain**: drawing p30: N1 = A1 (side-1) leg; gen_tee SPEC 5500 leg 1 = A1; = OMi M 1 certain 16/17 (M1) (M099); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 11/13 agree (equal 11, rounding 0); differ: 5500-02-02-FG cat 0.780 vs 0.72; 5500-16-12-FG cat 1.97 vs 1.78
- `N2@DRIVE` <- N LGTH - **certain**: drawing p30: N = A2 (side-2) leg; = OMi L 1 certain 17/17 (L1) (M100); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 11/13 agree (equal 11, rounding 0); differ: 5500-02-02-FG cat 0.780 vs 0.72; 5500-16-12-FG cat 1.78 vs 1.97
- `Y@REF` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 17/17 (HexFlat); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 13/13 agree (equal 3, rounding 10)
- `D1@BORE` <- A1 DRILL - **certain**: = OMi Side 1 ID certain 17/17 (S1ID); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 13/13 agree (equal 1, rounding 12)
- `D2@BORE` <- A2 DRILL - **certain**: = OMi Side 2 ID certain 17/17 (S2ID); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 13/13 agree (equal 1, rounding 12)
- thread callouts (size check only): `THDMAJ_A1@DRIVE` <- A1 NPTF, `THDMAJ_A2@DRIVE` <- A2 NPTF

**5501** (5501-FG, drawing TFA p31 (img1))

- `N4@DRIVE` <- N LGTH - **likely**: drawing p31: N = A1 (side-1) leg (letters the other way round from 5500); = OMi M 1 likely 8/8 (M1) (M104); same-dash rows only; plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 6/7 agree (equal 6, rounding 0); differ: 5501-02-02 cat 0.64 vs 0.63
- `N6@DRIVE` <- N1 LGTH - **likely**: drawing p31: N1 = A2 (side-2) leg; = OMi L 1 likely 8/8 (L1) (M105); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 3/7 agree (equal 1, rounding 2); differ: 5501-02-02 cat 0.64 vs 0.66; 5501-04-04 cat 0.86 vs 0.91; 5501-08-08 cat 1.17 vs 1.22 ...
- `Y@HEX` <- Y FLATS - **certain**: body flats; = OMi Hex Flat certain 8/8 (HexFlat) (M106); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 0/7 agree (equal 0, rounding 0); differ: 5501-02-02 cat 0.438 vs 0.5; 5501-04-04 cat 0.562 vs 0.63; 5501-06-06 cat 0.750 vs 0.81 ...
- `D1@BORE` <- A1 DRILL - **certain**: = OMi Side 1 ID likely 8/8 (S1ID) (M107); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/7 agree (equal 1, rounding 6)
- `D2@BORE` <- A2 DRILL - **certain**: = OMi Side 2 ID likely 8/8 (S2ID) (M108); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 7/7 agree (equal 1, rounding 6)
- thread callouts (size check only): `THDMAJ_A1@DRIVE` <- A1 NPTF, `THDMAJ_A2@DRIVE` <- A2 NPTF

**5502** (5502-FG, drawing TFA p31 (img3))

- `N@DRIVE` <- N LGTH - **certain**: drawing p31: N = A1 male pipe leg; in-repo Brennan 5502-04/-08/-16 STEPs 1.09/1.47/1.97 = N; = OMi M 1 certain 25/25 (M1) (M109); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 14/17 agree (equal 14, rounding 0); differ: 5502-02-02-FG cat 0.780 vs 0.89; 5502-20-20-FG cat 2.380 vs 2.75; 5502-24-24-FG cat 2.640 vs 3.05
- `N1@DRIVE` <- N1 LGTH - **certain**: drawing p31: N1 = A2 female port face to the A1 axis; STEPs 0.88/1.23/1.62 = N1; = OMi L 1 certain 24/25 (L1) (M110); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 14/17 agree (equal 13, rounding 1); differ: 5502-04-02-FG cat 0.660 vs 0.67; 5502-08-06-FG cat 1.020 vs 1.01; 5502-16-12-FG cat 1.360 vs 1.39
- `W@REF` <- Y FLATS - **certain**: body flats; STEP flats 0.750/1.062/1.625; = OMi Hex Flat certain 25/25 (HexFlat) (M111); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 16/17 agree (equal 4, rounding 12); differ: 5502-16-12-FG cat 1.312 vs 1.63
- `D@BORE` <- A1 DRILL - **certain**: male end drill; = OMi Side 1 ID certain 25/25 (S1ID) (M112); review rows of the same -FG part number holding a value (Air-Way, some cells Task-A OMi values): 17/17 agree (equal 3, rounding 14)
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A1@DRIVE` <- A1 NPTF, `THDMAJ_A2@DRIVE` <- A2 NPTF

**5503** (5503-FG, drawing TFA p32 (img1))

- `N4@DRIVE` <- N LGTH - **certain**: drawing p32: N = A1 male pipe tip to the 45 deg crossing; review rows of the same -FG part number holding a value (Air-Way): 5/5 agree (equal 5, rounding 0); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 10/10 agree (equal 9, rounding 1)
- `N3@DRIVE` <- N1 LGTH - **certain**: drawing p32: N1 = A2 female port face along the 45 deg axis; review rows of the same -FG part number holding a value (Air-Way): 5/5 agree (equal 5, rounding 0); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 10/10 agree (equal 10, rounding 0)
- `W@HEX` <- Y FLATS - **certain**: body hex (the drawing labels it "C HEX", the table column is Y FLATS); review rows of the same -FG part number holding a value (Air-Way): 5/5 agree (equal 1, rounding 4); plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 5/10 agree (equal 2, rounding 3); differ: 5503-02-02 cat 0.562 vs 0.63; 5503-08-08 cat 1.062 vs 1.13; 5503-12-12 cat 1.312 vs 1.38 ...
- `D@BORE` <- A1 DRILL - **likely**: A1 = the male end; Air-Way plain rows D = A1 DRILL (plain Air-Way twins vs the catalog -FG row (different parts - column-meaning evidence only): 10/10 agree (equal 2, rounding 8)) but Air-Way's -FG rows print 0.83/1.19/1.54/1.64 (not a drill): review rows of the same -FG part number holding a value (Air-Way): 1/5 agree (equal 0, rounding 1); differ: 5503-02-02-FG cat 0.188 vs 0.83; 5503-04-04-FG cat 0.281 vs 1.19; 5503-08-08-FG cat 0.531 vs 1.54 ...
- `TAPDRILL@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A1@DRIVE` <- A1 NPTF, `THDMAJ_A2@DRIVE` <- A2 NPTF

**5504** (5504-FG, drawing TFA p32 (img3))

- `N1_1@DRIVE` <- N LGTH - **certain**: drawing p32: N = A1 port face to the A2 axis; gen_tee SPEC 5504 leg 1 = first dash; in-repo Brennan 5504-08-08-FG STEP 1.23; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 6, rounding 0)
- `N1_2@DRIVE` <- N1 LGTH - **certain**: drawing p32: N1 = A2 port face to the A1 axis; STEP 1.23; review rows of the same -FG part number holding a value (Air-Way): 5/6 agree (equal 5, rounding 0); differ: 5504-04-02-FG cat 0.88 vs 0.72
- `W@REF` <- Y FLATS - **certain**: body flats; STEP flats 1.062; review rows of the same -FG part number holding a value (Air-Way): 6/6 agree (equal 2, rounding 4)
- `TAPDRILL1@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- `TAPDRILL2@BORE` - not printed (end_library): female NPTF tap drill: the catalog prints no female-port drill; source = Air-Way per-size tap drill (Q-TRANSFER-TAPDRILL on built masters, Q-TRANSFER-ENDLIB on new roots) or the part STEP
- thread callouts (size check only): `THDMAJ_A1@DRIVE` <- A1 NPTF, `THDMAJ_A2@DRIVE` <- A2 NPTF

## Questions the catalog answers

- Q-B-5500 (answered): 2 rows
- Q-B-ELBOW (answered): 23 rows
- Q-B-OTHER-2504 (answered): 4 rows
- Q-B-OTHER-2505 (answered): 3 rows
- Q-B-OTHER-2602Y1 (answered): 1 rows
- Q-B-OTHER-5501 (answered): 7 rows
- Q-B-OTHER-TEE2 (answered): 5 rows
- Q-B-TEE (answered): 2 rows
- Q-CONFLICT-2502-MS51506 (partly): 2 rows
- Q-F1 (answered): 46 rows
- Q-NEW-FOLD-2501LL (partly): 7 rows
- Q-NEW-PARKER4300 (partly): 10 rows

- **Q-B-ELBOW** - YES - OMi "M 1" is the first-dash (side-1) leg and "L 1" the second-dash leg, by the catalog's own column letters. Evidence: catalog p23 letters: M = B1 (first-dash, male JIC) leg, L = A2 (second-dash, male pipe) leg; OMi M 1 = catalog M 44/44 and L 1 = L 44/44 (match/TFA_elbows.json, certain) (per-row evidence in F1a.json). Rows: 2501-04-12-FG, 2501-05-06-FG, 2501-06-12-FG, 2501-08-16-FG ... (23 rows)
- **Q-F1** - settled for every body cell: the catalog prints this -FG part and its values equal OMi's, so OMi or the awaited Brennan data give the same numbers (ASSUMED, one source). Evidence: Q-NEW-BRENNANCAT treated as YES: the catalog page replaces the -FG STEP the standing F1 decision waits for; 5 of 5 OMi-filled body cells equal the catalog (TFA p23) (per-row evidence in F1a.json). Rows: 2501-04-12-FG, 2501-05-06-FG, 2501-06-12-FG, 2501-08-16-FG ... (46 rows)
- **Q-NEW-FOLD-2501LL** - drawing evidence only: the p24 2501-LL drawing shows the forged hex arm running up the long pipe leg exactly as on 2501-L (fold shape); the pilot STEP still proves it. Evidence: TFA p24 drawings of 2501-L-FG and 2501-LL-FG (work_F1a/png/grid_B.png). Rows: 2501-LL-04-02-FG, 2501-LL-04-04-FG, 2501-LL-06-04-FG, 2501-LL-06-06-FG ... (7 rows)
- **Q-CONFLICT-2502-MS51506** - the catalog gives Brennan's -FG legs (the "wait for the Brennan STEP" option) = OMi; the conflict with MS51506 stays a two-source conflict for the user. Evidence: catalog p25: 2502-08-04-FG M 1.42 / L 1.01 = OMi (same source); MS51506 per Q-CONFLICT-2502-MS51506: 1.250 / 0.890; the catalog is the Brennan data point the conflict waited for and it sides with OMi, so it stays Brennan/OMi vs MS51506 - the user picks (never majority-vote) | catalog p25: 2502-12-08-FG M 1.89 / L 1.35 = OMi (same source); MS51506 per Q-CONFLICT-2502-MS51506: 1.660 / 1.230; the catalog is the Brennan data point the conflict waited for and it sides with OMi, so it stays Brennan/OMi vs MS51506 - the user picks (never majority-vote). Rows: 2502-08-04-FG, 2502-12-08-FG
- **Q-B-OTHER-2504** - YES - OMi M 1 / M 2 / Hex Flat / Side 1 ID / Side 2 ID = legs of ends 1 / 2, body hex, bores (M090-M094); the repeated OMi leg is Brennan's value. Evidence: catalog p26: M1 = B1 leg, M2 = B2 leg, Y FLATS = body; OMi = catalog 6/6 on every column; in-repo Brennan 2504-08-08-FG STEP: both legs 0.980, flats 0.750 = catalog - the forged -FG union has equal legs, the plain Air-Way parts are another design. Rows: 2504-04-04-FG, 2504-06-06-FG, 2504-08-08-FG, 2504-12-12-FG
- **Q-B-OTHER-2505** - YES - OMi M 1 = M2 (JIC leg), M 2 = N6 (female pipe leg), Hex Flat = Y1, Side 1 ID = D (M095-M098). Evidence: catalog p27: M = B1 male JIC leg = OMi M 1 (8/8), N = A2 female pipe leg along the 45 deg axis = OMi M 2 (8/8), Y FLATS = Hex Flat (8/8), B1 DRILL = Side 1 ID (8/8), all certain. Rows: 2505-08-08-FG, 2505-12-12-FG, 2505-16-16-FG
- **Q-B-TEE** - YES - M 1 / M 2 / L 1 = the legs of ends 1 / 2 / 3. Evidence: catalog p48 letters: M1 = B1, M2 = B2 run legs, L = A3 branch tip to the run axis; OMi L 1 = L 14/14 (certain); M 1 / M 2 tie on the symmetric rows (order untestable, values equal on every printed row) | catalog p49 letters: M1 = B1, M2 = B2 run legs, N = A3 female branch port face to the run axis; OMi L 1 = N 10/10 (certain); M 1 / M 2 tie on the symmetric rows. Rows: 2601-24-24-24-FG, 2602-08-08-08-FG
- **Q-B-OTHER-2602Y1** - YES - OMi Hex Flat is the forged body hex Y1, not a boss diameter. Evidence: catalog p49 drawing labels "Y FLATS" on the forged body; OMi Hex Flat = Y FLATS 10/10 (certain, match/TFA_tees_caps.json). Rows: 2602-08-08-08-FG
- **Q-B-OTHER-TEE2** - YES for 2606 - OMi M 1 = side-1 JIC run leg (M1_1), M 2 = side-2 female pipe run leg (N1), L 1 = side-3 JIC branch leg (M1_3), Hex Flat = Y1, Side 1 / 3 ID = D1 / D3 (M193-M198). Evidence: catalog p51 drawing: M = B1 run leg, L = A2 female run port face, N = B3 branch leg; OMi M 2 = L 10/10 (certain, discriminating rows), M 1 / L 1 = M / N (tie on the symmetric rows, the drawing fixes them). Rows: 2606-04-04-04-FG, 2606-06-06-06-FG, 2606-08-08-08-FG, 2606-16-16-16-FG
- **Q-B-OTHER-TEE2** - YES for 2611 - OMi M 1 = side-1 JIC leg (M1), M 2 = side-2 male pipe leg (N5), L 1 = side-3 female branch leg (N1), Hex Flat = Y1, Side 1 / 2 ID = D / D1 (M204-M209). Evidence: catalog p52 drawing: M = B1 run leg, L = A2 male pipe run leg, L1 = A3 female branch port face; OMi = catalog 5/5 on each, all discriminating rows (certain). Rows: 2611-06-06-06-FG
- **Q-NEW-PARKER4300** - not answered (Parker is a second source); the Brennan catalog itself prints the locknut hex (C HEX) of this part. Evidence: TFA p29-30 4601-NWO-FG / 4603-NWO-FG tables, column C HEX (= the ORB locknut in the drawing). Rows: 4601-04-04-NWO-FG, 4601-08-06-NWO-FG, 4601-12-10-NWO-FG, 4601-16-16-NWO-FG ... (10 rows)
- **Q-B-5500** - YES - OMi "M 1" = side-1 (A1) leg, "L 1" = side-2 (A2) leg. Evidence: catalog p30 letters: N1 = A1 (horizontal, side-1) leg, N = A2 leg; OMi M 1 = N1 16/17, L 1 = N 17/17 (certain; the one miss 5500-20-16-FG 2.380 vs 2.382 is a print difference). Rows: 5500-08-04-FG, 5500-24-24-FG
- **Q-B-OTHER-5501** - YES - OMi M 1 = N4 (side-1 leg), L 1 = N6 (side-2 leg), Hex Flat = Y (M104-M106); the repeated OMi leg is Brennan's value. Evidence: catalog p31: N = A1 leg, N1 = A2 leg, Y FLATS = body; OMi = catalog 8/8 (same-dash rows); the catalog prints N = N1 on every same-dash 5501 row. Rows: 5501-02-02-FG, 5501-04-04-FG, 5501-06-06-FG, 5501-08-08-FG ... (7 rows)

Not answered by the catalog (still open on F1a rows): Q-HX, Q-TRANSFER-TAPDRILL, Q-CONFLICT-TAPDRILL-24, Q-TRANSFER-ENDLIB, Q-NEW-2702HOLD, every Q-NEWMASTER-* and generator-capability question (Q-NEW-ANGLEDHELIX, Q-NEW-HOSEB, Q-NEW-PERLEGSW, Q-NEW-FLG61LEG, Q-NEW-ANGLEDFEMALE); optional Q-CALIPER / Q-MS-FG unchanged.

## New questions

- **Q-NEW-F1A-1602PILOT** (1602-08-08-08-FG): 1602-08-08-08-FG - the planned pilot of the new 1602 master - is not in Brennan's TFA catalog (the p48 1602-FG table prints -02, -04, -06, -12, -16, -20 and the reducers 06-04-04, 08-06-06, 12-08-08 only). Check that Brennan sells it before the download; if it does not, move the 1602 pilot to 1602-06-06-06-FG or 1602-12-12-12-FG (both printed) and 1602-08-08-08-FG has no dimension source at all.
- **Q-NEW-F1A-5504TAP** (5504-06-04-FG, 5504-06-06-FG, 5504-08-06-FG, 5504-20-20-FG, 5504-24-24-FG): 5504-06-04 / -06-06 / -08-06 / -20-20 / -24-24-FG: the catalog (TFA p32) now gives both legs and the hex; only the two port tap drills are left, which Task C planned to measure on each STEP. Use Air-Way's per-size tap drill instead (the Q-TRANSFER-TAPDRILL rule that every built 5504 row already follows: -04 0.43, -06 0.57, -20 1.48; -08 0.70 on the built rows; -24 per Q-CONFLICT-TAPDRILL-24) and build them now, or keep the 5 downloads? If yes: the 5 rows move STEP -> NOW (the 5 Stage-1A downloads drop)

## STEP downloads (step_list items whose required_by touches F1a)

Required: replaced_by_catalog 36, partly 65, not_replaced 1. Conditional (DECIDE rows, needed only if Q-F1 = no): replaced_by_catalog 27. In-repo references (no download): 20.

| pn | stage | pilot of | verdict | still needed for |
|---|---|---|---|---|
| 1501-16-20-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p20) |
| 1501-20-16-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p20) |
| 1502-06-06-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-08-08-FG | 2 | 1502 | partly | pilot geometry of the new root 1502 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-12-12-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-16-16-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-20-20-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-24-24-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1502-32-32-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE rest on a likely pairing (see cells)) |
| 1503-04-02-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p21) |
| 1503-04-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p21) |
| 1503-06-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p21) |
| 1503-06-08-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p21) |
| 1503-08-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p21) |
| 1504-06-06-FG | 2 | 1504 | partly | pilot geometry of the new root 1504 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE (caveat: values of N2@DRIVE rest on a likely pairing (see cells)) |
| 1504-24-24-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N2@DRIVE rest on a likely pairing (see cells)) |
| 1601-02-02-02-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p47) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1601-04-04-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p47) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1601-06-06-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p47) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1601-08-08-08-FG | 2 | 1601 | partly | pilot geometry of the new root 1601 (forged body shape and end details to validate the master) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1601-12-12-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p47) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1601-16-16-16-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p47) (caveat: values of W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1602-06-06-06-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE, W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1602-08-08-08-FG | 2 | 1602 | not_replaced | the part is not in the Brennan catalogs - the STEP (if Brennan sells it) is the only dimension source |
| 1602-12-12-12-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of N3@DRIVE, W3_3@HEX, M1_2@DRIVE, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1603-02-02-02-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p48) (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE rest on a likely pairing (see cells)) |
| 1603-04-04-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p48) (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE rest on a likely pairing (see cells)) |
| 1603-06-06-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p48) (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE rest on a likely pairing (see cells)) |
| 1603-08-08-08-FG | 2 | 1603 | partly | pilot geometry of the new root 1603 (forged body shape and end details to validate the master); printed as a range: D1@BORE, D2@BORE (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX rest on a likely pairing (see cells)) |
| 1603-12-12-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p48) (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE rest on a likely pairing (see cells)) |
| 1603-16-16-16-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p48) (caveat: values of W3@HEX, M1@DRIVE, M2_2@DRIVE, W5_2@HEX, C3HEX@HEX, C2HEX@HEX, D1@BORE, D2@BORE rest on a likely pairing (see cells)) |
| 1703-24-24-FG | 2 | 1703 | partly | pilot geometry of the new root 1703 (forged body shape and end details to validate the master); cells not printed: D@BORE; end-library cells (or measure on this STEP): O@DRIVE (caveat: values of M2@DRIVE, N3@DRIVE rest on a likely pairing (see cells)) |
| 1704-24-24-FG | 2 | 1704 | partly | pilot geometry of the new root 1704 (forged body shape and end details to validate the master); cells not printed: D@BORE; end-library cells (or measure on this STEP): O@DRIVE (caveat: values of M@DRIVE, N2@DRIVE rest on a likely pairing (see cells)) |
| 1704-32-32-FG | 3 |  | partly | cells not printed: D@BORE; not printed, end-library alternative: O@DRIVE (caveat: values of M@DRIVE, N2@DRIVE rest on a likely pairing (see cells)) |
| 2500-06-04-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p22) |
| 2500-08-06-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p22) |
| 2500-12-08-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p22) |
| 2500-12-10-FG | 1A |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p22) |
| 2501-LL-04-02-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2501-LL-04-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2501-LL-06-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2501-LL-06-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2501-LL-08-08-FG | 2 | 2501LL | partly | fold-shape proof for Q-NEW-FOLD-2501LL (that the forged hex arm simply runs on, as on 2501-L) - the catalog gives every dimension |
| 2501-LL-12-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2501-LL-16-16-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p24) |
| 2504-04-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p26) (caveat: values of M2_1@DRIVE, M2_2@DRIVE rest on a likely pairing (see cells)) |
| 2504-06-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p26) (caveat: values of M2_1@DRIVE, M2_2@DRIVE rest on a likely pairing (see cells)) |
| 2504-12-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p26) (caveat: values of M2_1@DRIVE, M2_2@DRIVE rest on a likely pairing (see cells)) |
| 2505-08-08-FG | 2 | 2505 | partly | pilot geometry of the new root 2505 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE |
| 2505-12-12-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2505-16-16-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2606-04-04-04-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2606-06-06-06-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2606-08-08-08-FG | 2 | 2606 | partly | pilot geometry of the new root 2606 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE |
| 2606-16-16-16-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2611-06-06-06-FG | 2 | 2611 | partly | pilot geometry of the new root 2611 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE |
| 2611-12-12-12-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE |
| 2702-20-20-FG | 1A |  | partly | cells not printed: i2@DRIVE, K1@DRIVE, O@DRIVE |
| 4501-06-04-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-06-06-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-08-06-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-08-08-FG | 2 | 4501 | partly | pilot geometry of the new root 4501 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-08-12-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-10-08-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-12-08-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-12-12-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-16-12-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-16-16-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4501-20-20-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE, D1@BORE rest on a likely pairing (see cells)) |
| 4503-04-04-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-08-08-FG | 2 | 4503 | partly | pilot geometry of the new root 4503 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-12-12-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-16-12-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-16-16-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-20-20-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4503-24-24-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX, D1@BORE rest on a likely pairing (see cells)) |
| 4601-04-04-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-08-06-NWO-FG | 2 | 4601 | partly | pilot geometry of the new root 4601 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-12-10-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-16-16-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-16-20-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-20-16-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-20-20-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-24-20-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4601-24-24-NWO-FG | 3 |  | partly | not printed, end-library alternative: AA@DRIVE (caveat: values of L4@DRIVE rest on a likely pairing (see cells)) |
| 4603-16-16-NWO-FG | 2 | 4603 | partly | pilot geometry of the new root 4603 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): AA@DRIVE (caveat: values of L5@DRIVE, CHEX@HEX rest on a likely pairing (see cells)) |
| 5501-02-02-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-04-04-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-06-06-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-08-08-FG | 2 | 5501 | partly | pilot geometry of the new root 5501 (forged body shape and end details to validate the master) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-12-12-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-16-16-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5501-20-20-FG | 3 |  | replaced_by_catalog | nothing - every dimension it was to give is printed (TFA p31) (caveat: values of N4@DRIVE, N6@DRIVE rest on a likely pairing (see cells)) |
| 5503-16-16-FG | 2 | 5503 | partly | pilot geometry of the new root 5503 (forged body shape and end details to validate the master); end-library cells (or measure on this STEP): TAPDRILL@BORE (caveat: values of D@BORE rest on a likely pairing (see cells)) |
| 5503-20-20-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of D@BORE rest on a likely pairing (see cells)) |
| 5503-24-24-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of D@BORE rest on a likely pairing (see cells)) |
| 5503-32-32-FG | 3 |  | partly | not printed, end-library alternative: TAPDRILL@BORE (caveat: values of D@BORE rest on a likely pairing (see cells)) |
| 5504-06-04-FG | 1A |  | partly | not printed, end-library alternative: TAPDRILL1@BORE, TAPDRILL2@BORE |
| 5504-06-06-FG | 1A |  | partly | not printed, end-library alternative: TAPDRILL1@BORE, TAPDRILL2@BORE |
| 5504-08-06-FG | 1A |  | partly | not printed, end-library alternative: TAPDRILL1@BORE, TAPDRILL2@BORE |
| 5504-20-20-FG | 1A |  | partly | not printed, end-library alternative: TAPDRILL1@BORE, TAPDRILL2@BORE |
| 5504-24-24-FG | 1A |  | partly | not printed, end-library alternative: TAPDRILL1@BORE, TAPDRILL2@BORE |
| 2501-04-12-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-05-06-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-06-12-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-08-16-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-12-06-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-12-20-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-16-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-16-24-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-24-16-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p23) |
| 2501-L-04-04-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p24) |
| 2501-L-08-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p24) |
| 2501-L-12-12-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p24) |
| 2501-L-16-16-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p24) |
| 2502-06-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p25) |
| 2502-08-04-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p25) |
| 2502-12-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p25) |
| 2502-16-20-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p25) |
| 2502-24-24-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p25) |
| 2503-20-24-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p26) |
| 2601-24-24-24-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p49) |
| 2602-08-08-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p49) |
| 5500-08-04-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p30) |
| 5500-24-24-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p31) |
| 5502-02-04-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p31) |
| 5502-06-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p31) |
| 5502-12-08-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p31) |
| 5502-20-16-FG | CONDITIONAL |  | replaced_by_catalog | nothing for its stated purpose (Brennan -FG data if Q-F1 = no): the catalog prints this -FG part (TFA p31) |

## Catalog observations

- NPSM swivel -12: the catalog's nut-face-to-stem-tip offset is 0.35 (1501-12-12-FG 1.65 - 1.30; 1601-12-12-12-FG; 1602-12-12-12-FG 1.82 - 1.47; 1603-12-12-12-FG 1.65 - 1.30) while the in-repo Brennan 1404-12-12 STEP gives TIP_B 0.33 (NPSM_MEAS[12]); every other size agrees within 0.01. The generator derives the stem tip from W - M, so check the -12 rows at build time (affects 1502-12-12-FG, 1601-12-12-12-FG, 1602-12-12-12-FG, 1603-12-12-12-FG).
- 1603-FG heading on TFA p48 prints "FP-FPS-FPS TEE" but all three thread columns are NPSM (A1/A2/A3 NPSM = FPS-FPS-FPS) - kept as printed.
- 1603-08-08-08-FG prints all three drills as a range "0.44/0.46" - no single bore value (its pilot STEP gives it).
- 1603-16-12-16-FG prints C1 HEX 1.25 (the -12 A2 nut) although the drawing puts "C 1HEX" on the A3 (-16) nut; on the F1a same-dash rows C HEX = C1 HEX, so no F1a value depends on it.
- 1601-FG reducer rows print C HEX at an end size that is not the NPSM nut (06-04-04: 0.875, 08-06-06: 1.000, 12-08-08: 1.250, 04-06-06: 0.688); on every same-dash F1a row C HEX equals the NPSM nut of NPSM_MEAS - the pairing C HEX = nut hex is only claimed for those rows.
- 2606-FG header prints "BE SAE 37Deg" for the third (branch JIC) thread column - read as B3 (the drawing labels the branch end B3).
- 1703-24-24-FG (Flange p4) prints A/F as the fraction "1 7/8" (= 1.875) where the other rows print decimals.

## Side findings

- 2502-08-08-FG (ASSUMED, not an F1a row): its review $COMMENT says "legs diverge from MS51506 A8-8: AW M1=1.52/N1=1.23 vs MS 1.38/1.23 - AW stands, Brennan tiebreak pending". The catalog (TFA p25) prints 2502-08-08-FG M 1.52 / L 1.23 / Y 1.062 - the pending Brennan data point, on Air-Way's side. Same for 2602-08-08-08-FG (M1 / M2 1.520, N 1.230), whose conditional STEP was to inform that conflict.
- Air-Way: no F1a row has an Air-Way value of its own (every F1a review cell is empty), so agrees_with_airway is null on every cell. Against the plain (non -FG) Air-Way twins - different parts, evidence only - the catalog value matches on 383 cells and differs on 323, which supports the standing F1 rule not to copy plain-part values onto -FG parts.

