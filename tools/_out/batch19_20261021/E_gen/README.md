# Batch 19 E_gen - three generator jobs (23 parts) - STAGED, not shipped (2026-10-20)

Nothing in 04_DESIGN_TABLES, 03_SCRIPTS, 11_MASTERS, 01_MASTER_DATA or tools/ was changed; no SolidWorks. Everything is here.

| Job | README | Parts now generating | Existing configurations that change |
|---|---|---|---|
| 1. 0319 JIC tube sleeves (A2) | `job1_0319/README.md` | 12 (new master 0319, gen_ring SLEEVE) | none |
| 2. 2500HX / 2502HX / 2603HX -> gen_tee (A7) | `job2_HX/README.md` | 9 new rows + the 32 OMi rows of the HX masters (41) | 2502: 8 of 10 (port collar 0.30 x N1 -> 0.26 Brennan-measured) + placement of all 10; 2500: puck inset 0.0005 only; 2603: none (thread-pitch rounding / text); 65 non-OMi configurations leave the HX masters |
| 3. FS2500-12-08-FG / -16-12-FG | `job3_FS2500N1/README.md` | 2 (new master FS2500N1, mixed legs) | none |

## Layout
- `tools/` - copy of the live tools/ (generators, checks, measure); changed: `generators/gen_tee.py` (jobs 2 + 3), `generators/gen_ring.py`
  (job 1). Unified diffs against the live files: `patches/gen_tee.py.diff`, `patches/gen_ring.py.diff`. gen_straight2.py unchanged.
- `root/04_DESIGN_TABLES/` - copy of the live 04_DESIGN_TABLES with the table edits of `CHANGES.csv` (113 cells: 0319 24, 2500 48, 2502 26,
  2603 15), made by `scripts/stage_tables.py` (re-runnable from the live tables). Use as `OMI_ROOT=<E_gen>\root`.
- `out/ring/`, `out/tee/` - the generated macros + SW2 tables + summaries (0319; 2500 2502 2603 FS2500 FS2500N FS2500N1).
- `checks/` - `static_checks.txt` (vbacheck, dofcheck_tee, allcfg_check), `job1/` (sleeve outline / DOF / OCP closed loop, Brennan -08 probe),
  `job2/` (HX vs generator comparison, OCP closed loop, Brennan 2502-06-04 / 2500-06-06 measurements), `job3/` (OCP closed loop, summary diff).
- `regress_all.txt` (+ `regen/old|new/{tee,ring}`) - `scripts/regress_all.py`: every root of gen_tee and gen_ring regenerated with the
  live tools/ and the patched copy, same inputs (`root/`): **107 existing roots identical** (macro, SW2, summary); FS2500 / FS2500N differ
  in the summary skip text only (the 2 mixed rows now name FS2500N1); new roots 2500 2502 2603 FS2500N1 (gen_tee) and 0319 (gen_ring).
  gen_ring 0319T shows rc 1 on both sides: its TEST table lives in tools/_out/newtypes_20261014/test_tables, not in 04_DESIGN_TABLES.
- `scripts/` - every script used; `work/` - scratch.

## Regenerate
```
set OMI_ROOT=...\E_gen\root
set GR_OUT=<new folder>  &  python -I -B E_gen\tools\generators\gen_ring.py 0319
set GT_OUT=<new folder>  &  python -I -B E_gen\tools\generators\gen_tee.py 2500 2502 2603 FS2500N1
```

## Waits on the user
1. Job 1: accept the -08 SHAPE rule for the 11 other sleeve sizes (cone angle kept at 33 deg) or download per-size BRENNAN_0319-NN files;
   a look at Air-Way s48 that X is the collar O.D. at the small sizes.
2. Job 2: rename the HX masters to 2500 / 2502 / 2603 and drop their 65 non-OMi configurations; the 2502 collar change on 8 shipped
   configurations and its new placement (drawing to re-make); the 4 Brennan-only 2500 rows (Air-Way prints only non-forged twins).
3. Job 3: the master name FS2500N1.
4. PC: SolidWorks dry runs of 0319, 2500, 2502, 2603, FS2500N1 (CLAUDE.md verify loop, TABLE_PATH -> out/...), then ship.
