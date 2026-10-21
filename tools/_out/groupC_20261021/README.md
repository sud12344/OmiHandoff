# Group C: compression (bite-type, SAE J514/2 flareless) parts made generatable - STAGED 2026-10-21 (cloud), not shipped

Branch `claude/groupC-compression-20261021` (from `claude/ecstatic-hopper-fk5p40` @ a38c414). Live `04_DESIGN_TABLES`, `03_SCRIPTS`,
`tools/`, `11_MASTERS` and every other staging folder are untouched. Nothing was built in SolidWorks (the cloud cannot): the laptop does
the dry runs (`dryrun/RUN_DRYRUN.md`).

## Result

OMi's 230 compression part numbers (`07_RAW_EXTRACTS/omi_feed/omi_skus_compression.txt`) are in 11 review tables; **151 configurations
generate** in 9 new masters, 0 blocked; 70 rows are MISSING (no source), 9 sleeve rows wait for a sleeve model type.

| Series | OMi parts | Brennan record (cells) | Configurations | Not generated (why) |
|---|---|---|---|---|
| C0318 nut | 9 | 9 | 9 | - |
| C0319 sleeve | 9 | 9 | 0 | no sleeve model type for this shape yet (data staged; see decision 4) |
| C2402 bite x male JIC | 14 | 12 | 12 | -10-10 + -M1: no Brennan record (MISSING) |
| C2403 union | 18 | 18 | 18 | - |
| C2404 bite x male pipe | 32 | 0 | 0 | all 32: Brennan has no C2404 model at all (MISSING, in the Triveni package) |
| C2405 bite x female pipe | 32 | 24 | 24 | -16-12 -20-16 -24-20 -32-32 + their -M1 (MISSING) |
| C2500 union elbow -FG | 10 | 10 | 10 | - |
| C2501 male pipe elbow -FG | 34 | 30 | 30 | -20-16 -24-20 + -M1 (MISSING) |
| C2502 female pipe elbow -FG | 32 | 20 | 20 | -12-08 -16-12 -20-16 -24-20 -24-24 -32-32 + -M1 (MISSING) |
| C2601 branch tee -FG | 10 | 8 | 8 | -06-06-06 + -M1 (MISSING) |
| C6801 adj. ORB elbow -FG | 30 | 20 | 20 | -04-02 -20-16 -24-20 -32-24 -32-32 + -M1 (MISSING) |
| **Total** | **230** | **160** (89 fittings + 71 -M1) | **151** | 70 MISSING + 9 sleeves |

151 = 80 complete fittings / nuts + 71 "-M1" body-only part numbers. Count against the catalog: the 151 are new (no compression
part was in any master before).

## Master choice (one master per shape)

The skill says C2404 shares a topology with 2404 ("one master per shape"). Read against the masters as they are built, it cannot:
a master's DRIVE sketch has a fixed set of segments, and the bite-type end has different ones from a 37 deg JIC end - no seat cone, no
land, no 60 deg relief ramp; instead a relief NECK behind the thread, a 45 deg ramp and a TUBE SOCKET at the tip (the tube stop). A design
table can change values and suppression, not the segment list of a sketch. That is the user's own reasoning of 2026-10-18 for ORFS
(Q-FS-MASTER: "a face-seal end is a different sketch than a JIC end" -> FS series get their own masters, long variants fold in). The same
holds here, so: **one master per compression series** (C2402, C2403, C2404, C2405, C2500, C2501, C2502, C2601, C6801; nut C0318);
the "-M1" body-only numbers **fold into the same master as rows** (same body). The nut C0318 and the sleeve C0319 are different shapes
from the JIC nut 0318 (MS51531 shoulder, no cone) and the JIC sleeve 0319, so they get their own masters too. Decision 1 asks the user to
confirm that the Q-FS-MASTER exception extends to compression.

## Sources (rule: Air-Way first, then OMi's file / answers, then Brennan - user 2026-10-21)

- Air-Way: no compression series. OMi's website file (`WebsitePartsInfo2026.xlsx`, Items): thread callouts only ("Side n Thread"), copied
  to `$PRP@Threads`; they agree with Brennan's B1 callouts.
- Brennan CAD parameter records (`tools/_out/partcommunity_20261021/pc_final.csv`, exact / alias matches) for 89 fittings: every
  dimension cell, `$PRP@DimSource` BRENNAN, `$PRP@BrennanRecord`, DataStatus **ASSUMED** (one source), `$PRP@AxialSource` starts
  `[BRENNAN-CAD 2026-10-21: every dimension cell]`, `$COMMENT` = the raw record. 70 parts without a record: empty cells, **MISSING**.
- "-M1" (OMi "(Body)" = sold without nut and sleeve): the cells of the complete fitting of the same size, ASSUMED, the assumption in
  `$PRP@AxialSource` (OMi question in the unsent Triveni email). Decision 2.
- SAE J514/2 is not available as a citable source in the project - nothing is taken from it.

### Record letters, decoded on the ten Brennan -08 STEPs (`measure/measure_c.txt`, `scripts/records.py`)
Each Brennan compression STEP is ONE fused solid: body + nut(s), no sleeve, no 24 deg cone, no threads.
- Bite end (letters `<L>B1`, `<L>B2` on bite-x-bite parts): **AB** tube socket dia, **KB** socket depth from the body tip, **CB** / **EB**
  relief neck length / dia, **BB** hex face to nut face, **MB** nut face to body tip (assembled), so BB + MB = tip to hex face; **B1THD**
  thread major; **B1D** through bore; DB / FB / ODB = the nut's length / hex / tube hole (= the C0318 record). -08: socket 0.514 x 0.305,
  thread 0.750 to 0.423 from the tip, 45 deg ramp, neck 0.660 x 0.094, hex face 0.562 - identical on all ten STEPs.
- **The bite chain is a per-tube-dash library**: identical on every record of a dash, 71 records, 0 disagreements (`records.py bite_lib()`)
  -> `BITE_MEAS` in gen_straight2 (like the JIC chain from the 2403 table); the row cells are checked against it.
- Body: **L** body tip to far tip / port face (C2402 1.500, C2403 1.422, C2405 1.470 = the STEPs); **C** hex; **M / M1 / M2** crossing
  to bite tip, **N** crossing to pipe tip / port face, **Y** forged hex, **M7** ORB leg (C6801 = the 6801-08-08-NWO-FG row: 1.45, nut
  0.88, I3 0.86), **CA2** tap drill, **EA2** drill depth (straight C2405), **BA2** port thread length (C2502 PORTDEPTH), **DA2**
  countersink, **A2D / A3D** pipe drill.
- Nut C0318: **L**, **C** hex, **BTHD** major, **F** thread length, **E** cone start, **D** tube hole, **B** countersink dia, **A** hex
  chamfer dia (not modelled). Sleeve C0319: H length, C collar, A bore, B nose, N groove dia, G groove start, M collar start, D spigot,
  D1 tail, K tail chamfer, E inner step dia; L / PMIN / PMAX not decoded.

## Generator changes (`tools_c` = `airway_first_20261020/tools_af` + these; additive)
- `omi_paths.py`: `OMI_REV_EXTRA` (verbatim port from the ORFS staging toolset) - the C tables are read from `stage/04_DESIGN_TABLES`.
- `gen_straight2.py`: one block before `def dashes` (BITE_MEAS, `end_BITEM`, `bite_checks`, `bite_rowcheck`, C0318 ends `end_CNUTA` /
  `end_CNUTB`, SPECs C2402 C2403 C2404 C2405 C0318) + 7 inserted hooks in build_rows / emit (`scripts/patches/patch_gs2.py`): bite
  thread check, bite / nut gates, the `cnut_thru` bore, the BITEM DRIVE dimensions, the CNUTB cavity dimensions, the tube-socket pocket
  (`BoreCut POCKET_<end> SOCKDIA`, as the 0403 braze socket), open-axis checks. No existing line changed.
- `gen_tee.py`: `leg_BITEM` (the socket drawn inside the revolved leg profile), SPECs C2500 C2501 C2502 C2601 C6801 (before
  `SPEC_WAITING`), 4 inserted hooks (`scripts/patches/patch_gt.py`); `load_review` reads through `P.review_table` (the ORFS-toolset line,
  verbatim).
- Merge note for groups B / D: all group C text is between `GROUP C` markers or in lines tagged `# GROUP C`.

## Modelling assumptions (each in `$PRP@AxialSource` of every row it touches)
- Bite end per BITE_MEAS (Brennan, ASSUMED); 45 deg ramp measured at -08 only (all ten STEPs), ASSUMED at the other dashes.
- **NOT modelled:** the 24 deg sleeve cone (Brennan's CAD has a plain counterbore socket - decision 3), the tip chamfer (hidden in the
  fused nut; starts at dia 0.676 on the -08 tip face), hex end chamfers (library convention), the nut / sleeve in the body masters (as the
  2700-LN locknut).
- C2402: one through bore = the JIC bore D2 (the STEP shows 0.391 from the JIC tip to the socket; the record's B1D 0.422 is not on it);
  a 0.505 x 0.013 ring between bore and socket on the STEP is not modelled.
- C2403 / C2404: bore step at the hex mid-plane (library rule; no effect on C2403, D1 = D2 on every record).
- C2405: drill depth = record EA2, thread over the drill depth (end-library rule; Brennan's thread length BA2 kept as `PORTTHDL@REF`).
- C0318: the 0.005 radial counterbore step between F and E on the -08 STEP is not in the record - drawn at the minor; the thread minor
  bore is cut from End A to E and removes the DRIVE construction core (the 0306 locknut pattern). **C0318-24:** the record's BTHD 1.750
  contradicts its own callout 1 7/8-12, its countersink 1.880, OMi's file and the bite library -> built at 1.875 (flagged in `$COMMENT`).
- C6801: the adjustable ORB leg = the 6801 end library (I3 = Air-Way 6801 ORB_I3, thread length / undercut = ORB library;
  Q-TRANSFER-ENDLIB = yes) - Brennan's C6801-08-08 STEP and record agree with the 6801-08-08 row.
- Forged: Brennan Y printed to 3 decimals (1.062 / 1.312) vs the thread major 1.0625 / 1.3125 - the thread lies beyond the hex arm,
  no A/F raise (no warning needed).

## Checks (`checks/`, `closed_loop/`, `regen/cmp.txt`)
- **regen_all** (`scripts/regen_all.py`, base = tools_af, same tables): **101 existing roots identical** (macro text + SW2 content), 0
  different, 10 new (the C roots; C2404 writes nothing - all rows MISSING). 6566 / 6603 (SPEC_WAITING) and 6810 (empty hex cell in the
  stage tables) fail identically with both toolsets - pre-existing, not touched.
- **regress**: 97 roots, 0 changed cells in old configurations (`checks/regress.txt`).
- **dofcheck**: straight DRIVE sketches and every tee leg fully defined, 0 redundant (`checks/dofcheck_*.txt`).
- **allcfg**: 0 outline problems in all 151 configurations (`checks/allcfg_*.txt`).
- **vbacheck**: 9 / 9 macros OK.
- **OCP closed loop** (`scripts/closed_loop_c.py` -> `closed_loop/closed_loop.txt`): every configuration rebuilt from the generator's own
  vertex chains + pockets + bores, read back with point-membership probes (independent extractor; the ramp read at two levels, its angle
  measured): CLOSEDLOOP_RESULT. The same extractor on the ten Brennan -08 STEPs returns the library chain at every bite end (socket, bore, thread
  major, thread end 0.423, ramp 45.0 deg, neck, hex face 0.562) and the C0318-08 nut (countersink, minor, cone start 0.599, 45 deg, hole,
  L) - the only difference is the known C2402 ring.

## RUN_DRYRUN (laptop) - `dryrun/RUN_DRYRUN.md`
`python tools\_out\groupC_20261021\scripts\run_dryrun.py g1 g2` -> `run_macro` with SAVE_PATH / REPORT_PATH -> `dryrun\<root>\` and
TABLE_PATH -> `regen\new\...\DesignTable_<root>_SW2.xlsx`, then sweep_configs, geometry, screenshots, close without saving.
g1: C2402 C2403 C2405 C0318 (gen_straight2); g2: C2500 C2501 C2502 C2601 C6801 (gen_tee).

## Decisions for the user
1. **Masters:** extend the Q-FS-MASTER exception to compression (own master per C series, -M1 rows folded in) - recommended, the end is a
   different sketch - or keep C2404 etc. in the JIC masters (needs a second sketch per master, suppressed per row: not built anywhere yet).
2. **-M1 body-only numbers (71 configurations):** generate now as the same body (staged so, ASSUMED) or hold them until OMi answers the
   "(Body)" question in the Triveni email.
3. **24 deg cone:** Brennan's CAD has none (plain socket = tube stop). Build as Brennan (staged) or wait for a citable J514/2 copy /
   OMi drawing for the cone.
4. **C0319 sleeve (9 parts):** the record leaves three positions of the -08 shape unexplained (collar end 0.141, step radius 0.3246,
   inner step 0.267). Either download BRENNAN_C0319-04 / -06 / -10 / -12 / -16 / -20 / -24 / -32 (8 files) so they can be measured per
   size, or allow scaling them from -08 (an assumption per row). Then a sleeve model type (gen_ring SLEEVE has 7 segments; this shape
   needs ~14).

## Files
| Path | What |
|---|---|
| `stage/04_DESIGN_TABLES/DesignTable_C*.xlsx` | the 11 review tables (230 rows) |
| `rows.csv` | per part: root, DataStatus, source, Brennan record |
| `scripts/records.py`, `build_tables.py` | record parsing + bite library, table builder |
| `scripts/patches/` | the generator additions as applied (`gs2_block.py`, `patch_gs2.py`, `patch_gt.py`) |
| `scripts/env.sh` | OMI_ROOT = the Brennan-CAD stage, OMI_REV_EXTRA = this stage |
| `tools_c/` | the staged toolset |
| `regen/` | `cmp.txt` + the run logs of every root (the old / new outputs of the 101 unchanged roots were compared, then not kept - `scripts/regen_all.py` recreates them); `regen/new/{straight,tee}/Build_C*_MASTER.bas` + SW2 = the dry-run inputs |
| `measure/measure_c.txt` | sections of the ten Brennan STEPs |
| `closed_loop/` | closed-loop result |
| `dryrun/` | RUN_DRYRUN.md, call files |
