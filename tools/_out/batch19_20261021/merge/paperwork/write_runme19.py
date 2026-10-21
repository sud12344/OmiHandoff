"""Writes 03_SCRIPTS/RUN_ME_batch19.txt (LF) from ship_roots.json / regen_cmp.json / old_files SW2 counts."""
import json, os, openpyxl
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
M = os.path.join(H, 'tools', '_out', 'batch19_20261021', 'merge')
ship = json.load(open(os.path.join(M, 'ship_roots.json'))); res = json.load(open(os.path.join(M, 'regen_cmp.json')))


def n(p):
    if not os.path.exists(p): return None
    return sum(1 for r in openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0].iter_rows(min_row=2, values_only=True) if r and r[0])


rows = []
for r in sorted(ship):
    new = n(os.path.join(H, '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
    old = n(os.path.join(M, 'old_files', '04_DESIGN_TABLES', f'DesignTable_{r}_SW2.xlsx'))
    hx = {'2500': '2500HX', '2603': '2603HX'}.get(r)
    if hx:
        old = n(os.path.join(M, 'old_files', '04_DESIGN_TABLES', f'DesignTable_{hx}_SW2.xlsx'))
        rows.append(f'   Build_{r}_MASTER.bas'.ljust(36) + f'{old:>4} -> {new:>4}   NEW generated master, replaces the hand-built {hx} (non-OMi rows dropped)')
    elif old is None:
        rows.append(f'   Build_{r}_MASTER.bas'.ljust(36) + f'{new:>4} configurations   NEW master')
    else:
        rows.append(f'   Build_{r}_MASTER.bas'.ljust(36) + f'{old:>4} -> {new:>4}  +{new - old}   ' + ', '.join(res[r]['new'][:4]) + (' ...' if len(res[r]['new']) > 4 else ''))
TXT = r'''BATCH 19 - THE "NO INPUT NEEDED" PARTS: ANSWERED ROWS, OWN-STEP ROWS, BRENNAN CELLS, NEW MASTERS, 2500 / 2603 ON THE GENERATOR (2026-10-21)
=========================================================================================================================================
NOTHING TO RUN. Batch 19 is ALREADY BUILT: Claude built all 31 masters through the SolidWorks MCP (SolidWorks 2026 SP4) as dry runs into
tools\_out\batch19_20261021\merge\dryrun\ and copied them into 11_MASTERS after your "finish the 94 parts that need no input from me". Their
macros are in 03_SCRIPTS, their SW2 tables in 04_DESIGN_TABLES (same sha256 as built: tools\_out\batch19_20261021\merge\checks\
shipped_files_sha256.txt). The reports in 03_SCRIPTS still say "Saved to ...\dryrun\...".

31 MASTERS                                          configurations (before -> after, new configurations)
@@TABLE@@
                                                  ----------
   Configurations in a master: 1,534 -> 1,610; 156 masters in 11_MASTERS. OMi's 2,535 parts: 1,607 in a master (was 1,531).
   NO old configuration changed in any table. 2500: every kept configuration differs from 2500HX only by the 0.0005 corner-puck inset
   (the batch-16 fix, -0.01 ... -0.03 % volume).

WHERE THE NEW VALUES COME FROM (every cell + source: tools\_out\batch19_20261021\<A_answered|B_newspec|C_ownstep|D_geom|E_gen>\CHANGES.csv)
  - Your 2026-10-18 answers applied: A1 tap drill, A8 / A10 2705 / 2706 I1 and -LN rows, A11 / A18 6410 bores and -32 groove, A12 6504
    swivel offset (read as the end library's swivel nose value per size, SWIV_MEAS NOSETIP_B).
  - Own Brennan STEPs measured (1502 2501-LL 2505 5505 5601 5603 5652 6603 6606 -FG rows, 2404-L-32-32): DimSource BRENNAN, ASSUMED.
  - Air-Way value not buildable -> Brennan (your Q1 "use brennans"), rows marked [BRENNAN-CELL]:
      2406-16-04 L23 1.67 -> 1.840; 2408-14 hex 1.125 -> 1.250; 1501-24-24-FG nut 1.88 -> 2.125; 6802-04-06-NWO-FG locknut 0.56 -> 0.688;
      1501-04-02-FG bore 0.23 -> 0.13; 1502-04-04-FG M1 0.78 -> 0.99 and W3 0.97 -> 1.18.
  - New masters: 3474 (adjustable ORB x ORB straight, Brennan TFA p9 + the 6801 end), 2613 (forged tee, Brennan p53), 6603, 0319 sleeves
    (Air-Way s48 + OMi bore; the shape SCALED from BRENNAN_0319-08 - an assumption written into every row), FS2500N1 (the two mixed-leg
    FS2500 rows).
  - Values worth knowing: 3474 adjustable thread length = Air-Way's 6801 0.469 (Brennan's own STEP measures 0.410); 2613 branch length =
    Brennan's forged 1.22 (Air-Way prints only the plain part, 1.01).

MOVED TO THE GENERATOR (your A7): 2500 and 2603 are now generated masters; the hand-built 2500HX / 2603HX files are retired (old files below).
  2502 is NOT moved: in the generated 2502, 2502-20-20-FG's tap-drill pocket (the MS51503 depth 1.16) ends exactly on the cross bore and the cut
  fails in SolidWorks (QA #180). 2502HX stays as it was; its 2 new rows (2502-06-08-FG, 2502-16-20-FG) wait.

STILL NEED YOU (QA #181)
  - 2404-40-40: every source gives ONE bore 2.318 - accept it as a one-bore 2404?
  - 2705-04-02 / 2705-LN-04-02: the -02 bulkhead length - Brennan 2700-02-02 says 1.07, 2706-04-02 says 1.11. Which?
  - 5503-02-02-FG: the 1/8 pipe port fills the leg - download BRENNAN_5503-02-02-FG.stp, or cap the port 0.05 short of the leg end?
  - 6420-08-08: the ports overlap at OMi's 1.5 length - shorten the pipe drill (as 5000-08-08) or build Brennan's 1.62 body?
  - 6316-08 / -12 / -16: download BRENNAN_6316-08 / -12 / -16 (butt-weld end shape).
  - 6506-12-14: L17 / L18 (OMi / Brennan 2.34 / 1.75, or Air-Way L18 + a -14 offset); also needs a measuring-tool fix.
  - 5404-N long nipples: wait for the 5404N -06 thread fix (QA #178).

CHECKED BEFORE SHIPPING (tools\_out\batch19_20261021\merge\)
  - Every root regenerated with the merged tools on the merged tables: 0 old configurations changed (regen_cmp.txt).
  - Static checks clean (checks\: dofcheck, allcfg, vbacheck).
  - SolidWorks dry runs: 31 / 31 PASS, 0 FAIL lines, 1 body per configuration, every old configuration identical to the master it replaces
    (2500: the puck inset only) - checks\dryrun_verdict.txt.
  - After shipping: the LIVE tools + LIVE tables regenerate exactly the 31 shipped macros + SW2 (checks\verify_b19.txt, 0 BAD).
  - Old files: _to_delete\superseded_20261021\batch19_replaced\ and tools\_out\batch19_20261021\merge\old_files\ (MANIFEST*.txt).

TOOLCHAIN: tools\ now = merge\tools_b19 (gen_straight2.py, gen_tee.py, gen_ring.py changed; measure\orb_straight.py + straight_model.py added).

QA_Log #179-#181 (01_MASTER_DATA). Coverage refreshed (00_DOCS\OMi_Coverage_2026-09-24.xlsx): A1 1,405 of the 1,831-part feed (was 1,339).
'''.replace('@@TABLE@@', '\n'.join(rows))
open(os.path.join(H, '03_SCRIPTS', 'RUN_ME_batch19.txt'), 'w', encoding='utf-8', newline='\n').write(TXT)
print('ok', len(TXT.splitlines()))
