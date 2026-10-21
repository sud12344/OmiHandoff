# Group D: bent-tube ("swept") elbows - STAGED 2026-10-21 (cloud), not shipped

**Scope:** 68 OMi parts:
- 1703 / 1704 / 1803 / 1804 -Tube: 61 parts;
- 6701 / 6701-L: 7 parts.

**Masters** (`gen_bent.py`):
- `1704T` (90 deg, code 61 / 62 flange): 1704 + 1804 -Tube;
- `1703T` (45 deg): 1703 + 1803 -Tube;
- `6701` (90 deg, female JIC swivel): 6701 + 6701-L.

**Not touched:** the live `tools/`, `04_DESIGN_TABLES`, `03_SCRIPTS` and `11_MASTERS`. The cloud has no SolidWorks; the dry runs are for
the PC: `dryrun/RUN_DRYRUN.md`.

## 1. Result

**61 of the 68 configurations generate:**

| Master | Rows | Generated | Not generated (reason) |
|---|---|---|---|
| 1704T | 35 (1704 -Tube 19, 1804 -Tube 16) | **33** (18 code 61 + 15 code 62) | 1704-20-12-Tube, 1804-16-24-Tube: Brennan record contradicts itself (s6 Q2) |
| 1703T | 26 (1703 -Tube 13, 1803 -Tube 13) | **26** (13 code 61 + 13 code 62) | - |
| 6701 | 7 | **2** (6701-08-08, -12-12) | -04-04, -06-06: Brennan's tube is wider than the straights' swivel neck (s6 Q4). -20-20: Brennan M conflict (Q3). -16-16, -L-16-16: no record, no STEP (Q5) |

**Data status:**
- The 61 rows are ASSUMED. Their dimensions come from Brennan (`$PRP@DimSource` BRENNAN, `[BRENNAN-CAD 2026-10-21: <cols>]`) or Air-Way.
- The 7 rows not generated are MISSING, with their cells staged and the reason in `$COMMENT`.
- **Code 62 heads:** 28 code 62 configurations (-08 ... -32) build. The -12 ... -32 heads are new, per user Q-CODE62-CAT (s4).

**Checks: all clean** (s5).
- The OCP closed loop against all 5 family STEPs reproduces:
  - both legs;
  - the bend torus (radius, tube dia, centre);
  - the bore;
  - the head and hub.
- The other 101 generator roots are byte-identical.

## 2. Decoding the Brennan CAD records (`data/`, `scripts/dump_step.py`, `scripts/records.py`)

**Records:** 66 of the 68 parts have one (PARTcommunity; Brennan numbers drop "-Tube"). `data/records.csv` holds them.

**Decoding:** the codes were read face by face on the family STEPs (`data/dump_<pn>.txt`, inches). The STEPs are 1704-08-08, 1804-08-08,
1703-08-08, 1803-12-12 and 6701-08-08.

| Gen column | 1704 / 1804 (90 deg) | 1703 / 1803 (45 deg) | 6701 | Evidence on the STEP |
|---|---|---|---|---|
| M1 (JIC tip -> leg-axis crossing) | L1 | L1 - L2 | M | 1704: tip x -0.657, leg-2 axis x 1.663 = 2.320. 1703: face centre (2.063, -0.910) -> 2.72 / 0.91 |
| L1 (crossing -> face / nut face) | L2 | L2 x sqrt2 | L - F - J + LN | 6701: L 1.520 = nose tip. F = nose above the shoulder (0.264), J = shoulder -> nut back (0.155), LN = nut length (0.827). Nut face y 1.928 |
| NOSETIP (nut face -> nose tip) | - | - | LN - F - J | 6701: 1.928 - 1.520 = 0.408 |
| CHEX / HEXL | AF / JT | AF / JT | C1 / THK | Hex planes +-AF/2. Hex x 0 ... 0.394 (JT); 6701 -1.113 ... -0.916 (THK 0.197) |
| TUBEOD / D | TOD / DRILLFL | TOD / DRILLFL | DIA / DIA6 | Tube cylinder + torus tube dia 0.618 / 0.374 (6701 0.549 / 0.374) |
| RB | **0.8 x EXT** | **TOD** | R | 1704 / 1804 torus R 1.0152 = 0.8 x 1.269. 1703 R 0.618, 1803 R 0.800 = TOD. 6701 R 0.827 |
| O / head | AFL, EFL, BFL | same | - | Head cylinder, thickness, groove OD |
| HUBD / HUBL (new) | DFL / FFL | DFL / FFL | - | Hub cylinder 0.945 behind the head. Face -> hub back 0.512 |

Two confirmations:
- **EXT = min(L1 - GT - JT, L2 - FFL)** on all 35 records, exactly. That is the shorter of the two runs: hex back face -> leg-2 axis,
  and hub back -> leg-1 axis. The bend radius is 80 % of it, which leaves 0.2 EXT straight on the shorter leg.
- **The records match the libraries and the catalog.**
  - JIC end GT / DT / ET = the generator's JIC library (2403 table) at all six sizes.
  - L1 / L2 / A/F = Brennan's printed catalog on every row.
  - Code 61 head = FLG61_MEAS and Air-Way s61 O. The groove OD of -24 / -32 differs by 0.005, which is rounding.
  - Code 62 head = catalog 3300-62.

  Full list: `stage/checks.txt`.

**The wave-3 mapping error is fixed.** gen_bent's TEST rows had M1 = M3 - O/2; the right reading is M3 = M1 (s115 / record L1 = tip ->
leg-2 axis, confirmed on the STEP).

## 3. Stage tables (`scripts/stage_tables.py` -> `stage/`)

**Files:**
- `DesignTable_1704T.xlsx`, `DesignTable_1703T.xlsx`, `DesignTable_6701T.xlsx`: gen_bent's review tables;
- `cells.csv`: 661 cells, each with its source;
- `rows.csv`;
- `checks.txt`.

**Base:** the brennancad stage (`tools/_out/brennancad_20261021/stage/04_DESIGN_TABLES`). It supplies the OMi rows, the ScopeAction and
the original AxialSource.

**Air-Way first (user rule).** Air-Way s115 (1701-61; two passes identical) gives M3 / N4 / C / D / O for 4 parts: 1704-12-12-Tube,
-16-20-Tube, -24-20-Tube and -24-24-Tube. Those cells are Air-Way; the rest of each row is Brennan.
- This settles the Air-Way-vs-Brennan conflicts there. Air-Way is 0.23 - 0.91 shorter on -16-20 / -24-20 / -24-24, and its bores
  differ (1704-12-12: D 0.61 vs Brennan 0.551).
- RB on these rows = 0.8 x EXT of the row's own (Air-Way) lengths.

**Everything else:** the Brennan record, per the user's 2026-10-21 rule. The A13 caveat applies: 1803-20-12 A/F 1.5 as printed.

## 4. Generator changes (`tools_gd/`)

`tools_gd/` = `tools/_out/airway_first_20261020/tools_af` + two NEW files:
- `generators/gen_bent.py`: from `newtypes_20261014`; the original is in `history/`;
- `checks/dofcheck_bent.py`.

gen_straight2 / gen_tee are not edited (`diff -r` against tools_af: only those 2 files), so the merge with groups B / C is additive.

**gen_bent changes.** All are additive: rows without the new columns build exactly as before.
1. **Path:** `LIVE` = the toolset the file sits in. It is portable; before, it was the user's Windows path.
2. **Code 62 heads.**
   - -12 was measured on BRENNAN_1803-12-12: O 1.625, TH 0.345, groove 0.940 / 1.250, depth 0.110 (= 3300-62-12-12).
   - -16 / -20 / -24 / -32 come from catalog 3300-62 (A = O, D = TH, H = groove OD).
   - The groove I.D. and depth come from the code 61 groove of the same size. This is an ASSUMPTION: the measured code 62 grooves at -08 and
     -12 equal the code 61 grooves, and the catalog groove OD H = 2 x FLG61 GO at every size.
3. **Braze hub on the flange head.** New review columns `HUBD@HEAD` / `HUBL@HEAD`.
   - HEADSK has 10 lines (`FLGB_HUBR`, `FLGB_HUBL`).
   - The tube ends 0.05 inside the hub.
   - PATH gets a construction line `FACEEXT` (`PathExtension`) from the tube end to the face centre, where the head is anchored as before.
     Its dimension text sits on the line's normal, so the dimension is aligned on the 45 deg leg too.
   - The tube-vs-groove check applies only without a hub.
   - New hub checks: hub behind the head, inside the head OD, and the tube fits into it.
4. **6701 neck margin 0.02 -> 0.005.** Brennan's own 6701-08-08 has 0.019: tube 0.549 into the 0.587 neck.
5. **Box check (the macro's per-configuration check).** It now includes the JIC chain radius: 1803-20-12's -20 thread (r 0.8125) is wider
   than its 1.5 hex flats. The old check would have FAILED that configuration in SolidWorks; the OCP all-configuration check found it.

**Regression** (CLAUDE.md "changing a generator").
- The old gen_bent (`history/`) and the new one were both run on the 2026-10-15 TEST tables (`regen/test_baseline` vs `regen/test_new`).
  Macros and SW2 are identical. The only difference is the summary's block reason for the 1803-12-12 TEST row: now "head OD 1.5 differs
  from the measured code 62 -12 head 1.625" instead of "not measured".
- All 101 gen_straight2 / gen_tee roots were regenerated with tools_af and with tools_gd on the brennancad stage:
  **101 / 101 byte-identical** (`regen/all_cmp.txt`, `scripts/regen_all.py`).

## 5. Checks (`checks/`, `closedloop/`)

- **dofcheck_bent:** DRIVE, PATH (22 / 22 with FACEEXT), PATHX and HEADSK (44 / 44 with the hub) are fully defined, with 0 redundant
  constraints, in all 3 masters.
  - The same checker passes the 2026-10-15 TEST macros, which SolidWorks confirmed fully defined.
  - SWSK (6701) is not covered: its code is unchanged.
- **vbacheck:** OK on all 6 macros (stage + TEST).
- **regress:** the TEST configurations are unchanged. No bent configuration has shipped yet.
- **OCP closed loop** (`closedloop/bent_ocp.py` -> `closedloop.txt`). It rebuilds a configuration from gen_bent's own numbers, then compares
  it with its family STEP, moved into the model frame.
  - **Matches exactly:** 1704-08-08, 1804-08-08, 1703-08-08, 1803-12-12 and 6701-08-08 all match the STEP in:
    - the bend torus: R, tube dia, centre;
    - the box: x, y max and z;
    - the cylinders: bore, tube, head, hub, groove.
  - **Volume:** -1.3 ... -3.3 %. Symmetric difference 4 - 5 % (6701: 10 %). This comes from what is not modelled:
    - the end-piece hex: gen_bent has its flats normal to Y with sharp corners; Brennan has its flats normal to Z, turned to dia IT;
    - 0.02 fillets;
    - the 7 deg bore flare at the flange face;
    - on the 6701, the straights' swivel shape instead of the 6701's own.
- **All-configuration check** (`closedloop/allcfg_bent_ocp.py` -> `allcfg.txt`, `dryrun/expected_ocp.json`): **61 / 61 OK**. Each
  configuration:
  - builds as one valid solid;
  - has outlines that do not self-intersect;
  - has a box equal to the macro's own box check.

## 6. Assumptions, all logged in `$PRP@AxialSource` / `$COMMENT`

1. **90 deg bend radius = 0.8 x EXT.** Decoded on one STEP size (-08, the 1704 and 1804 STEPs). EXT's own rule holds on all 35 records.
2. **45 deg bend radius = tube OD,** from two STEP sizes (-08, -12).
3. **Code 62 groove I.D. / depth** = the code 61 groove (s4.2).
4. **6701 swivel = the straights' SWIV_MEAS shape** (Q-TRANSFER-ENDLIB); the nose tip comes from the record.
5. **Not modelled:**
   - the turned hex corners and the hex rotation;
   - braze fillets;
   - the bore flare at the flange face;
   - edge chamfers.

## 7. User decisions (real ones only)

- **Q1 (recommended, not blocking): confirm the 90 deg bend rule.**
  - 33 configurations use it, and it rests on one STEP size.
  - One more 90 deg STEP would confirm it, e.g. BRENNAN_1704-16-16 (on the 2026-10-14 shape-file list) or 1804-24-24. Ship without
    it = accept the rule as decoded.
- **Q2 (Q-GD-1804-16-24, Q-GD-1704-20-12): two Brennan records contradict themselves.** Both rows are held MISSING. Get the part's own
  STEP, or decide.
  - **1804-16-24:** tube 0.800 with bore 0.740, a 0.030 wall. The other -16 rows have tube 1.043.
  - **1704-20-12:** tube 1.339 is wider than its hub 1.260.
- **Q3 (Q-GD-6701-20): 6701-20-20 M - CAD record 3.260 vs TFA catalog 2.750.** L is 3.750 in both, and the -16 has M 3.10. Which one?
  The record value fits the size series.
- **Q4: 6701-04-04 / -06-06.** Brennan's tube (0.315 / 0.413) is wider than the -04 / -06 neck of the straights' swivel (0.293 /
  0.412), and Brennan's records show no separate neck there (DIA7 = 0). Either get BRENNAN_6701-04-04 / -06-06 for the real body, or
  allow the neck to follow the tube on these two sizes.
- **Q5: 6701-16-16 / 6701-L-16-16 have no source** for the tube, bore, bend or nut position. Brennan's CAD portal has no record. Needs
  BRENNAN_6701-16-16 / 6701-L-16-16.

## 8. To ship (after the dry run passes and the user says so)

1. **Tools:**
   - `tools_gd/generators/gen_bent.py` -> `tools/generators/` (new file);
   - `tools_gd/checks/dofcheck_bent.py` -> `tools/checks/`.
2. **Review tables:** `stage/DesignTable_1704T.xlsx`, `DesignTable_1703T.xlsx` and `DesignTable_6701T.xlsx` -> `04_DESIGN_TABLES`.
3. **The -Tube rows in the old tables** (DesignTable_1703 / 1704 / 1803 / 1804) and the skeleton DesignTable_6701 stay MISSING, so the
   forged 1703 / 1704 SPECs keep skipping them. Add a `$COMMENT` "built in master 1704T / 1703T / 6701 (gen_bent)".
4. **Macros and SW2:**
   - `regen/stage/Build_*_MASTER.bas` -> `03_SCRIPTS`;
   - `DesignTable_*_SW2.xlsx` -> `04_DESIGN_TABLES`;
   - build for real.
5. **Records:** RUN_ME, QA_Log, Topologies (1704T / 1703T / 6701 masters), a coverage refresh (count the new tables), and
   PROJECT_STATUS.

## Regenerate

```
set OMI_ROOT=...\tools\_out\brennancad_20261021\stage   &   set GS_OUT=<scratch>
python tools\_out\groupD_20261021\scripts\records.py           (records.csv from pc_final.csv)
python tools\_out\groupD_20261021\scripts\stage_tables.py      (stage tables)
set GB_REV=tools\_out\groupD_20261021\stage  &  set GB_OUT=tools\_out\groupD_20261021\regen\stage
python tools\_out\groupD_20261021\tools_gd\generators\gen_bent.py 1704T 1703T 6701
python tools\_out\groupD_20261021\tools_gd\checks\dofcheck_bent.py tools\_out\groupD_20261021\regen\stage\Build_*.bas
python tools\_out\groupD_20261021\closedloop\bent_ocp.py  /  allcfg_bent_ocp.py    (OCP; same env)
python tools\_out\groupD_20261021\scripts\make_calls.py        (dryrun\calls_bent.json)
```
