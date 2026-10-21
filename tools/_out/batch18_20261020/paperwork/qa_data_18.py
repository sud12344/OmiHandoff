# Batch 18 (2026-10-20): data block for update_masterdata_18.py (QA_Log rows, Topologies notes, master status changes).
# Notes per shipped root from checks/shipped_files_sha256.txt and old_files/MANIFEST.txt (exec'd by the updater).
import json as _json, os as _os, re as _re
_B18 = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\batch18_20261020'
_AF = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\airway_first_20261020'
_shipped = sorted(set(_re.findall(r'  11_MASTERS/(\w+)_MASTER\.SLDPRT', open(_os.path.join(_B18, 'checks', 'shipped_files_sha256.txt'), encoding='utf-8').read())))
_old = set(_re.findall(r'11_MASTERS/(\w+)_MASTER\.SLDPRT', open(_os.path.join(_B18, 'old_files', 'MANIFEST.txt'), encoding='utf-8').read()))
_af = set(_json.load(open(_os.path.join(_AF, 'dryrun', 'roots.json'))))
_held = {'1700RC': 'FLATS rectangle relations (FlatsCut)', '1800': 'FLATS rectangle relations (FlatsCut)', '1703': '45 deg HEX2 direction (HexArmVS)',
         '4503': '45 deg hose face-off test (HOSEFACE45)', '4603': '45 deg hose face-off test (HOSEFACE45)'}
_chg = {}
_cur = None
for _l in open(_os.path.join(_AF, 'checks', 'dryrun_verdict.txt'), encoding='utf-8'):
    _m = _re.match(r'(\S+)\s+(PASS|CHECK)', _l)
    if _m:
        _cur = _m.group(1)
    elif 'CHANGED (table cells changed)' in _l:
        _chg[_cur] = _chg.get(_cur, 0) + 1
assert len(_shipped) == 83, len(_shipped)

QA = [
    ('176',
     'Batch 18 shipped - RUN_ME_batch18.txt: Air-Way first (OMi / Triveni 2026-10-20: Air-Way over Brennan incl. the OMi website file; 320 cells back to Air-Way + 4 unbuildable cells Brennan, 26 roots; the 40 cells of the Triveni draft shipped as Air-Way, user 2026-10-20 "Ship batch 18 as staged, including the 40 cells as Air-Way"), the ORFS generator stage (50 FS masters, 133 FS configurations) + O-ring master 4000 (4000 / 4001 / FS4000), A14 1603-08-08-08-FG, and the held roots of QA #175 fixed (1700RC 1800 1703 4503 4603)',
     'One toolset tools_b18 (ORFS staging tools + the 6410 reference 6410-24-20-O + the QA #177 fixes) on one input set (Air-Way stage + A14 + the FS / O-ring review tables): every root regenerates identical to the file its SolidWorks dry run built (tools/_out/batch18_20261020/cmp.txt; the 6 pre-2026-09-25 macro roots = live-tools control). Static checks clean (Air-Way: airway_first_20261020/checks; ORFS: orfs_gen_20261020/checks; held roots + 1603: batch18 checks/static_held.txt). SolidWorks 2026 SP4 dry runs: Air-Way first 26 / 26 PASS (233 configurations change, each with its own reverted cells; every other configuration identical to a read-only sweep of the master it replaces); ORFS 49 + FS2403 / FS6400 rebuilt from the final macros; 1603 + the 5 held roots 0 FAIL, 1 body per configuration. Review PDFs (07_RAW_EXTRACTS/omi_review_drawings_20261020): no AW / BI mark contradicts the stage (tools/_out/review_pdfs_20261020/PDF_CHECK.md). Post-ship: live tools + live tables regenerate all 83 shipped macros + SW2 (checks/verify_b18.txt, 0 BAD).',
     'tools_b18 deployed to tools/ (gen_straight2.py, gen_tee.py, omi_paths.py (OMI_REV_EXTRA), checks/allcfg_check.py changed; gen_ring.py added; 57 files differing only in line endings kept). 83 masters -> 11_MASTERS (56 new, 27 replaced), 83 macros (LF) + 83 reports -> 03_SCRIPTS, 83 SW2 + 81 review tables (27 Air-Way / A14, 51 FS, 4000 / 4001 replacing the 2026-09-23 skeletons) -> 04_DESIGN_TABLES. BUILD rows 1,874 -> 2,259 (FS + O-ring tables now live); configurations in a master 1,354 -> 1,534; 151 masters in 11_MASTERS. Old files -> _to_delete/superseded_20261020/batch18_replaced/ + tools/_out/batch18_20261020/old_files/ (MANIFEST*.txt). The dimension-check drawings of the Air-Way-first roots (2026-09-26 / 10-09) are stale.',
     'INFO',
     'Next: 5404N (QA #178); the BLOCKED_NEEDS list (tools/_out/blocked_needs_20261020/BLOCKED_NEEDS.md); send Triveni the 40-row list (10_DRAWINGS/for_OMi_2026-10-20) - an answer that differs from Air-Way is a later table edit.'),
    ('177',
     'Held roots of QA #175 fixed in the generators (tools_b18, now live): 1700RC / 1800 FLATS sketch, 1703 HEX2 direction, 4503 / 4603 hose face-off',
     'SolidWorks inspection of the batch-17 dry-run parts: (1) FlatsCut - CreateCenterRectangle here gives NO rectangle relations (only the 2 distances, the midpoint of one diagonal, the centre coincident): status 2, the 1700RC master rebuilt skewed in other configurations (1700-24-20 across flats 2.076 vs 2.000); H / V on all four sides over-defines it (status 6); the centre point at the middle of the SECOND diagonal + one horizontal + one vertical side -> status 3 (tested by hand on the 1800 dry-run part). (2) 1703-24-24-FG: the 0.697-long 45 deg HEX2 arm lies mostly inside HEX1 (AF 1.875): face-box centre -0.111 / -0.713 in for the two directions - neither positive. (3) 4503 / 4603: the 45 deg face-off ring faces lie mostly in the plane HFPLN2, so the tip-side cut (centre 0.330 / 0.245 = at the plane) failed the plane + depth / 2 test; the crossing-side cut went into the hex (0.163 / -0.000).',
     'gen_straight2 FlatsCut: 2nd-diagonal midpoint + one H + one V, each only while under-defined (only flats macros change: 1700RC, 1800). gen_tee: SPEC 1703 hexarm_fb=True -> HexArmVS keeps the direction further along the leg when neither passes (only 1703 changes); HOSEFACE45_HELP: cut took >= the stub ring and its faces are not behind the plane (only 45 deg face-off macros: 4503, 4603; 4501 / 4601 byte-identical). Dry runs 0 FAIL, flats = table, 4503 / 4603 net corner removal < 0 and the D2 bore FAIL gone; screenshots looked at. 17 configurations built.',
     'INFO',
     'Done (shipped in batch 18).'),
    ('178',
     '5404N -06 thread sweeps still fail (error 1 on THD_EndA / THD_EndB in every -06 configuration; QA #163, #175)',
     'SolidWorks probe 2026-10-20 on the batch-17 dry-run part (5404-N-06X3.000): helix and profile agree (HELIXDIA 0.6565 = 2 x PROF_R); the sweep keeps failing with the bar radius (0.33 ... 0.40), the thread radius (0.30 ... 0.34, helix / profile / major together) and the thread length (0.38 ... 0.42) changed - not an end or radius coincidence. -04 / -08 build with the same construction.',
     '18 rows (5404-N-04 / -06 / -08 OMi names) stay unbuilt; the old 4-configuration master stays. Needs a deeper look (sweep path / profile plane at -06) and ideally a Brennan -06 STEP (none on Brennan\'s site); bar OD Air-Way 0.69 vs pipe OD 0.675 still open.',
     'MEDIUM',
     'Follow-up session.'),
]

NOTES = {}
for _r in _shipped:
    if _r in _af:
        NOTES[_r] = f'2026-10-20 BATCH 18 SHIPPED (QA #176): Air-Way first - {_chg.get(_r, 0)} configuration(s) rebuilt with Air-Way values (were OMi website / Brennan); master replaced'
    elif _r in _held:
        NOTES[_r] = f'2026-10-20 BATCH 18 SHIPPED (QA #176/#177): NEW master - held root fixed ({_held[_r]})'
    elif _r == '1603':
        NOTES[_r] = '2026-10-20 BATCH 18 SHIPPED (QA #176): A14 1603-08-08-08-FG added (bores 0.450 measured on the Brennan STEP); master replaced'
    elif _r not in _old:
        NOTES[_r] = '2026-10-20 BATCH 18 SHIPPED (QA #176): NEW master (ORFS / O-ring generator stage)'
    else:
        NOTES[_r] = '2026-10-20 BATCH 18 SHIPPED (QA #176): master replaced'
NOTES['5404N'] = '2026-10-20 BATCH 18: still held (QA #178, -06 thread sweeps)'
STATUS = {}   # filled by the updater from the live sheet: TABLED / SKELETON-MISSING / TABLED - master not built -> BUILT for new masters
