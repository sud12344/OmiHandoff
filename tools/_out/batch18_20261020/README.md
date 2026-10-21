# Batch 18 candidate (2026-10-20, PC) - NOT shipped

One toolset and one set of inputs for everything staged on 2026-10-20 (`scripts/prep_b18.py`, result `cmp.txt`):
- `tools_b18/` = the ORFS staging toolset (`orfs_gen_20261020/tools`, incl. the 5 dry-run fixes and gen_ring) + the Air-Way-first 6410
  reference line (`ref='6410-24-20-O'`, = `airway_first_20261020/tools_af`).
- `root18/04_DESIGN_TABLES` = the Air-Way-first stage (full copy of the live tables + 26 edited review tables) + A14's
  `DesignTable_1603.xlsx` (`brennan_yes_20261018/stage`; differs from live in 1603-08-08-08-FG only). FS review tables: `OMI_REV_EXTRA` =
  `brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES`; O-ring tables `GR_REV` = `newtypes_20261014/review_tables`.

## Regeneration check (every root of gen_straight2 / gen_tee + gen_ring 4000)
- Air-Way-first roots: identical to `airway_first_20261020/regen/stage` (= the files in the SolidWorks dry run of 2026-10-20 evening).
- All 51 FS roots: identical to `orfs_gen_20261020/out` (= the dry-run-tested files, all PASS). Ring 4000: identical to `out/ring` (29 rows).
- Every other root: identical to the shipped 03_SCRIPTS / 04_DESIGN_TABLES, except
  - 2408 4404 4604 1700 5602 2704: they still ship pre-2026-09-25 macros; the LIVE tools regenerate them exactly as tools_b18 does
    (`control/`), so tools_b18 changes nothing there;
  - 1603: only the A14 row 1603-08-08-08-FG is added (macro: "expect 7" configurations) - **needs a SolidWorks dry run**;
  - held roots 5404N 1700RC 1800 4503 4603 1703 (QA #175): not shippable until their generator problems are fixed.

## SolidWorks dry runs (2026-10-20 evening, `dryrun/`)
- Air-Way-first 26 roots: **26 PASS** (`airway_first_20261020/checks/dryrun_verdict.txt`; 233 configurations change, each with its own
  table cells; every other configuration identical to the shipped master).
- 1603 (A14): PASS - 225 OK / 0 FAIL, 7 configurations, 1603-08-08-08-FG 1 body, the 5 old ones identical to the shipped master.

## Held roots fixed in tools_b18 (QA #175) - backups `backup_20261020/`
| Root | Fault | Fix | Dry run |
|---|---|---|---|
| 1700RC (3), 1800 (1) | FLATS centre rectangle came WITHOUT its rectangle relations: status 2, rebuilt skewed in other configurations (1700-24-20 A/F measured 2.076 vs 2.000) | FlatsCut: centre point at the middle of the 2nd diagonal + one horizontal + one vertical side, each only while under-defined (gen_straight2; only flats macros change) | 0 FAIL, fully defined, A/F = table |
| 1703 (1) | 45-deg HEX2 arm (0.697 long, AF 1.875) mostly inside HEX1: face-box centre negative in both directions | SPEC `hexarm_fb=True` -> HexArmVS keeps the direction further along the leg (gen_tee; only 1703's macro changes) | 0 FAIL, 1 body; looked at |
| 4503 (7), 4603 (5) | 45-deg hose face-off: the ring's faces lie mostly IN the plane, so the right cut (tip side) was rejected | HOSEFACE45_HELP: took >= the stub ring and faces not behind the plane (only 45-deg face-off macros; 4501 / 4601 byte-identical) | 0 FAIL (the D2 FAIL went too), net corner removal < 0, 1 body each |
| 5404N (18) | -06 thread sweeps fail (error 1) | NOT fixed: insensitive to bar radius, thread radius, thread length; needs a real look + Brennan has no -06 STEP; bar OD Air-Way 0.69 vs pipe 0.675 | - |
Regeneration after the fixes (`cmp.txt`): every root as before except the held roots - no shipped / tested macro changes.

## Ship content when the user says go
51 FS masters + O-ring master 4000 (162 OMi parts new), 1603 (+1), the held roots 1700RC 1800 1703 4503 4603 (+17), the 26 Air-Way-first
roots (dry runs PASS; the user's call on the 40 cells for Triveni: ship as Air-Way, or wait). Masters = the dry-run parts in `dryrun/`,
`airway_first_20261020/dryrun/`, `orfs_dryrun_20261020/`. Deploy `tools_b18` to `tools/` (back up first).
