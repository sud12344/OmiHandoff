"""Writes 03_SCRIPTS/RUN_ME_batch18.txt (LF, as RUN_ME_batch17.txt) from runme_table.txt."""
import os
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
table = open(os.path.join(os.path.dirname(__file__), 'runme_table.txt'), encoding='utf-8').read().replace('\r\n', '\n').rstrip('\n')
TXT = r'''BATCH 18 - AIR-WAY FIRST + ORFS FACE-SEAL MASTERS + O-RINGS + A14 + FIVE HELD ROOTS FIXED (2026-10-20)
=====================================================================================================
NOTHING TO RUN. Batch 18 is ALREADY BUILT: Claude built all 83 masters through the SolidWorks MCP (SolidWorks 2026 SP4) as dry runs
(tools\_out\airway_first_20261020\dryrun\, tools\_out\orfs_dryrun_20261020\, tools\_out\batch18_20261020\dryrun\) on 2026-10-20
and copied them into 11_MASTERS after your "Ship batch 18 as staged, including the 40 cells as Air-Way.". Their macros are in 03_SCRIPTS,
their SW2 tables in 04_DESIGN_TABLES. The reports in 03_SCRIPTS still say "Saved to ...\dryrun\..." (the staging builds); the parts were
copied unchanged (same sha256: tools\_out\batch18_20261020\checks\shipped_files_sha256.txt).

If you ever re-run one: close <root>_MASTER, remove any old module of the same name in the VBA editor first, import the .bas from
03_SCRIPTS, run the entry sub (Sub Build<root>). A good run ends with "finished with 0 problem(s)", "All-config sweep: N configurations
rebuilt, 0 feature/body failures", "Master left in its reference configuration ..." and "Saved to ...\11_MASTERS\...".

83 MASTERS                                          configurations   (before -> after; "rebuilt with Air-Way values" = old
                                                                      configurations whose dimensions changed with their table cells)
@@TABLE@@
                                                  ----------
   Configurations in a master: 1,354 -> 1,534. 151 masters in 11_MASTERS (was 95). BUILD rows 1,874 -> 2,259 (the FS and O-ring review
   tables are now live). OMi's 2,535 carbon-steel parts: 1,531 in a master (was 1,351).

AIR-WAY FIRST (OMi / Triveni 2026-10-20: "prefer Airway over Brennan dimension when Airway has them available", incl. OMi's website file)
  - 320 cells went back from the OMi-website / Brennan value to Air-Way's printed value; 233 configurations rebuilt with them (6565 /
    6504-24-24: source text only). Every reverted cell keeps the old value in $COMMENT / $PRP@AxialSource. Detail:
    tools\_out\airway_first_20261020\revert_list.csv, stage\CHANGES.csv.
  - Air-Way value not buildable -> Brennan (your Q1 "use brennans"): 6405-24-16-O L31 1.75, 6504-24-24 D1 1.312, 6565-10-10 nut hexes
    1.000 - rows marked $PRP@DimSource BRENNAN + [BRENNAN-CELL 2026-10-20: <col>].
  - The 40 cells of the Triveni draft (10_DRAWINGS\for_OMi_2026-10-20\) shipped AS AIR-WAY (your call). If Triveni answers BI for any of
    them, that is a table edit + rebuild in a later batch. The PDF check column is filled; delete it before sending.
  - 6410's reference configuration is now 6410-24-20-O (with Air-Way's bore 0.68 the old reference 6410-12-08-O is a deep-bore port).
  - The dimension-check drawings of these roots (2026-09-26 / 10-09) are now stale.
  - OMi's two "Review of Drawings" PDFs: no AW / BI mark contradicts these values (tools\_out\review_pdfs_20261020\PDF_CHECK.md). OMi
    also wrote "UNPL: mention in notes, do not put in part#" - the 0403 configuration names still carry UNPL (your decision).

ORFS (FACE-SEAL) MASTERS + O-RINGS (the cloud ORFS generator stage, dry runs 2026-10-20: tools\_out\orfs_dryrun_20261020\RESUME.md)
  - 50 FS masters (one per leg-shape variant: N / C / R suffixes), 133 FS configurations; O-ring master 4000 (4000 Buna / 4001 Viton /
    FS4000 face-seal O-rings, 29). Dimensions Air-Way first, end shapes from the Brennan FS STEPs.
  - Noted in the rows: Brennan's FS0306 / FS0318 -10 / -24 thread bores are below the basic minor (modelled at the basic minor); the
    straight swivel body hex is built to Air-Way's printed hex length (your "yes keep airway").
  - The swivel / nut helix curves (HELIX_n) are visible in the saved masters (display only).

HELD ROOTS FIXED (QA #177)
  - 1700RC / 1800: the wrench-flats rectangle had no rectangle relations - it rebuilt skewed in other sizes (1700-24-20: 2.076 across the
    flats instead of 2.000). Now fully defined; flats = table.
  - 1703-24-24-FG: the 45 deg hex arm direction test failed both ways; it now keeps the direction that reaches further along the leg.
  - 4503 / 4603: the 45 deg hose face-off test rejected the right cut; fixed for 45 deg legs only (4501 / 4601 unchanged).
  - A14: 1603-08-08-08-FG added (both bores 0.450 measured on the Brennan STEP).

STILL HELD
  - 5404N: the -06 thread sweeps still fail (QA #178); its 4-configuration master stays; the 18 OMi-name rows wait.

CHECKED BEFORE SHIPPING (tools\_out\batch18_20261020\, README.md)
  - One toolset (tools_b18) on one input set regenerates every root identical to the file its SolidWorks dry run built (cmp.txt).
  - Static checks clean (dofcheck, allcfg, vbacheck; Air-Way and ORFS stages + checks\static_held.txt).
  - SolidWorks dry runs: Air-Way first 26 / 26 PASS (airway_first_20261020\checks\dryrun_verdict.txt: every unchanged configuration
    identical to the master it replaces); ORFS 51 PASS (FS2403 / FS6400 rebuilt from the final macros); 1603 + 5 held roots 0 FAIL.
  - After shipping: the LIVE tools + LIVE tables regenerate exactly the 83 shipped macros + SW2 (checks\verify_b18.txt, 0 BAD).
  - Old files: _to_delete\superseded_20261020\batch18_replaced\ and tools\_out\batch18_20261020\old_files\ (MANIFEST*.txt).

TOOLCHAIN: tools\ now = tools_b18 (gen_straight2.py, gen_tee.py, omi_paths.py, checks\allcfg_check.py changed; generators\gen_ring.py added).

QA_Log #176-#178 (01_MASTER_DATA). Coverage refreshed (00_DOCS\OMi_Coverage_2026-09-24.xlsx): A1 1,339 of the 1,831-part feed (was 1,300).
'''.replace('@@TABLE@@', table)
open(os.path.join(H, '03_SCRIPTS', 'RUN_ME_batch18.txt'), 'w', encoding='utf-8', newline='\n').write(TXT)
print('ok', len(TXT.splitlines()))
