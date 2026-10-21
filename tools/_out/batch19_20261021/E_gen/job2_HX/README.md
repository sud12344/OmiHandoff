# Job 2 - 2500HX / 2502HX / 2603HX moved to the generator (user A7) - STAGED, not shipped (2026-10-20)

User A7 (00_DOCS/ANSWERS_2026-10-18.md): "Move 2500HX / 2502HX / 2603HX to the generator later (no hand typing)". 9 OMi rows waited for it.

## Assessment: can gen_tee build these shapes? Yes, as they are
gen_tee was written FROM these three hand macros (its docstring: "Geometry = the proven 2603HX pattern"; elbows: "2500HX pattern (two hex
arms + 30deg double-cone corner puck)"), and 2502 (male JIC x female pipe 90 deg) is the 5502 / 2505 forged body with the library JIC and
female-NPTF legs. No new geometry code: three SPECs in a copy of gen_tee (`../patches/gen_tee.py.diff`, block "2026-10-20 (batch 19 E_gen,
user A7 ...)"):

| SPEC | body | legs (columns of the live review table) | hex |
|---|---|---|---|
| `2500` 90 deg Union Elbow | elbow (hex arm per leg + corner puck) | JICM M1 / D1 / THDMAJ_B1 (+X), JICM M2 / D2 / THDMAJ_B2 (+Y) | Y@REF |
| `2502` 90 deg Male JIC x Female Pipe Elbow | elbow; port = library NPTFF leg (collar COLLAR_L, pocket to MS51503 P1), connecting drill = D@BORE | JICM M1 / D / THDMAJ_B (+X), NPTFF N1 / TAPDRILL / THDMAJ_A (+Y) | Y1@DRIVE |
| `2603` Union Tee | run bar through the crossing + branch hex arm | JICM LEG1 / LEG2 (run), LEG3 (branch); D1..D3, THDMAJ_1..3 | Y@REF |

Plus `row_hex_src` / `assume_reps`: these tables mix Air-Way rows with OMi / Brennan rows, so the generated text names "the row hex A/F
(its source: the start of this AxialSource)" instead of "Air-Way hex" (text only). Masters are named after the root: **2500_MASTER /
2502_MASTER / 2603_MASTER** (the GeometryRoot the HX tables already carried); the HX macros, SW2 tables and masters retire at ship.

## Parts now generating: 41 configurations (32 existing OMi rows + the 9 rows)
| Root | configurations | new rows (A7) |
|---|---|---|
| 2500 | 15 | 2500-06-04-FG, 2500-08-06-FG, 2500-12-08-FG, 2500-12-10-FG |
| 2502 | 14 | 2502-04-06-FG, 2502-05-04-FG, 2502-06-08-FG, 2502-16-20-FG |
| 2603 | 12 | 2603-02-02-02-FG |

Output: `../out/tee/Build_{2500,2502,2603}_MASTER.bas` + `DesignTable_{2500,2502,2603}_SW2.xlsx`.

## Table edits for the 9 rows (`../CHANGES.csv`, tables in `../root/04_DESIGN_TABLES`; 89 cells)
Order: Air-Way first, then OMi's file, then Brennan (marked). Air-Way prints none of these -FG part numbers.
- **2500-06-04 / -08-06 / -12-08 / -12-10-FG**: Air-Way s117 prints only the NON-forged twins (e.g. 2500-06-04 M1 1.08 / M2 0.95 / Y 0.63
  vs Brennan -FG 1.06 / 1.05 / 0.562) - the forged rule keeps them out; OMi Items rows 641 / 643 / 647 / 648 have no dimensions -> **Brennan
  TFA catalog p.22** (TFA-p022-t02), `$PRP@DimSource` BRENNAN (column added), `[BRENNAN-ONLY 2026-10-20]` at the start of AxialSource.
- **2502-06-08 / -16-20-FG**: OMi Items rows 736 / 745 (= Brennan TFA p.25, one source), DimSource OMI; tap drill = Air-Way per size (A1);
  thread majors / pipe OD = end library.
- **2502-04-06 / -05-04-FG**: values already in the live table (OMi Items, wave 3); only DataStatus MISSING -> ASSUMED (the gate was "no
  2502 SPEC").
- **2603-02-02-02-FG**: OMi Items row 821 (legs 0.770 x 3, hex 0.438, bores 0.062; = Brennan TFA p.49), DimSource OMI (column added).
- All 9: DataStatus ASSUMED (one source). The values are the ones wave 2 / wave 3 had staged (`tools/_out/brennan_yes_20261018/wave2/tee_elbow`,
  `wave3/adapters`), with the OMi file now cited first where it has them.

## Existing configurations: what changes (`../checks/job2/cmp_hx_vs_generator.txt`, `cmp_2502_port_columns.txt`)
Every column of the HX SW2 tables compared with the generated table for every configuration both hold (2502: columns paired by meaning).

**2500** (2500HX: 27 configurations)
- 11 OMi configurations kept. Lengths, hex arms, A/F, JIC chain, bores: identical. Changes:
  - corner puck equator 0.0005 inside the hex corner (`PUCK_R1B / R1T / XC` -0.0005, PUCK_HB / HT +0.00005 at 4 sizes = rounding): the
    batch-16 puck fix (`PUCK_INSET`: with the equator ON the corner SolidWorks silently dropped the puck in some configurations). A
    construction margin, invisible.
  - thread pitch / profile values to 5 decimals instead of 4 (e.g. 0.0556 -> 0.05556; THD_ features are suppressed in the saved masters).
  - `$PRP@End1/2_Thread` "3/4-16" -> "3/4-16 JIC" (text).
- 16 configurations leave the master: the non-forged Air-Way rows (2500-04-04, -05-05, -06-04 ... -24-24; all ScopeAction DROP, no OMi SKU).

**2603** (2603HX: 41 configurations)
- 11 OMi configurations kept: identical except the thread-pitch rounding and the "JIC" property text (no puck on tees).
- 30 leave: 25 non-forged rows + 5 -FG rows that are DROP (no OMi SKU): 2603-08-08-10-FG, -10-10-08-FG, -12-10-12-FG, -14-14-14-FG,
  -32-32-32-FG.

**2502** (2502HX: 29 configurations) - the hand macro differed from the generator pattern in four places:
- 10 OMi configurations kept, with these geometry changes:
  1. **Placement**: 2502HX had its origin on the NPTF port face (pipe leg along X, JIC leg along +Y at x = N1); the generator puts the origin
     at the axis crossing, JIC leg +X, port +Y (the part turned -90 deg about Z and moved by N1). Same solid, different model coordinates -
     the existing 2502HX dimension-check drawing (10_DRAWINGS) must be re-made.
  2. **Port collar length**: 2502HX 0.30 x N1 (its own logged assumption) -> **0.26 at every size** (COLLAR_L, measured on Brennan
     2502-06-04-FG - re-read today: collar 0.260, `../checks/job2/brennan_fgelbow_2502-06-04_2500-06-06.json` - and the 5502 / 5504 / 5605
     STEPs; = every other forged female port). The pipe-side hex arm grows by the difference:

     | config | collar HX -> new | pipe hex arm HX -> new |
     |---|---|---|
     | 2502-04-02-FG | 0.20 -> 0.26 | 0.46 -> 0.40 |
     | 2502-04-04-FG, -06-04-FG | 0.26 -> 0.26 | unchanged |
     | 2502-06-06-FG, -08-06-FG | 0.31 -> 0.26 | 0.71 -> 0.76 |
     | 2502-08-08-FG, -10-08-FG | 0.37 -> 0.26 | 0.86 -> 0.97 |
     | 2502-12-12-FG | 0.41 -> 0.26 | 0.95 -> 1.10 |
     | 2502-16-16-FG | 0.49 -> 0.26 | 1.13 -> 1.36 |
     | 2502-20-20-FG | 0.51 -> 0.26 | 1.19 -> 1.44 |
  3. 2502-20-20-FG: tap-drill pocket 1.14 -> 1.16 deep (= the MS51503 P1 the HX thread helix already used; the HX pocket was 0.02 short of
     its own thread).
  4. JIC-leg revolved core radius (`BODYR@LEGJ`): 2500-table values (HX assumption) -> the row's flats / 2. The core lies inside the hex
     arm in both, so the solid does not change. Plus the puck inset and pitch rounding as on 2500.
  -> **8 of the 10 kept configurations change visible geometry (collar / hex arm)**, all 10 change placement.
- 19 configurations leave (non-forged Air-Way rows, DROP).

Totals: 32 existing OMi configurations kept (8 with a real geometry change, all 2502), 65 non-OMi configurations dropped from the masters,
9 new rows. Volumes vs Brennan STEPs of the same part number (model has no fillets / chamfers / port taper): 2500-06-06-FG -2.73 %,
2502-06-04-FG +6.38 % (Brennan's port drill 0.437 runs to 0.07 from the crossing; the library port stops the tap drill at P1 and continues
with the bore D - the same as every built female port), 2603-06-06-06-FG -4.08 %.

## Checks (`../checks/`)
- `static_checks.txt`: vbacheck 3 / 3 OK; dofcheck_tee every LEG sketch fully defined (2500 2 / 2, 2502 2 / 2, 2603 3 / 3); allcfg_check
  2500 15 / 2502 14 / 2603 12 configurations, 0 leg outline problems.
- `job2/ocp/closed_loop_job2.txt` (`../scripts/closed_loop_job2.py`): every configuration rebuilt in OCP from the generator's legs + SW2 row
  (as the macro), read back with tools/measure/forged.py (the Brennan-validated extractor): tip, hex face, end length, A/F, JIC chain, bores,
  port face / collar / pocket - **41 configurations, 804 checks, 0 off**, 1 solid each.
- Regenerate-all (`../regress_all.txt`): every existing gen_tee root identical (macro, SW2, summary); 2500 / 2502 / 2603 NEW.

## For the user
1. OK to **rename the masters 2500HX / 2502HX / 2603HX -> 2500 / 2502 / 2603** and drop the 65 non-OMi configurations from them?
2. OK for the **2502 collar change** (0.30 x N1 assumption -> the Brennan-measured 0.26) on 8 shipped configurations, and the new placement
   (origin at the crossing)?
3. The 4 Brennan-only 2500 rows: Air-Way's non-forged twins differ (lengths up to 0.10, hex up to 0.07) - the forged rule keeps Brennan's
   -FG values (marked BRENNAN).

## Ship (when the user says so)
gen_tee patch -> tools/ (backup to `_to_delete/superseded_<date>/`); the 2500 / 2502 / 2603 rows of `../CHANGES.csv` -> 04_DESIGN_TABLES;
dry runs on the PC (`TABLE_PATH` -> out/tee), then macros -> 03_SCRIPTS, SW2 -> 04_DESIGN_TABLES; retire Build_2500HX / 2502HX / 2603HX
macros + reports, DesignTable_*HX_SW2.xlsx and 11_MASTERS/*HX_MASTER.SLDPRT to `_to_delete/<date> replaced by generator/` (keep
`tools/generators/templates/Build_2603HX_MASTER.bas`: it is gen_tee's VBA helper library); re-make the 2500HX / 2502HX / 2603HX drawings;
Topologies note, coverage (master names change), PROJECT_STATUS.
