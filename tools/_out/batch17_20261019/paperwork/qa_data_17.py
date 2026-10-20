# Batch 17 (2026-10-20): data block for update_masterdata_17.py (QA_Log rows, Topologies notes, master status changes).
# Notes are generated per shipped root from checks/b17_roots.json, checks/verdict.txt and old_files/MANIFEST.txt (exec'd by the updater).
import json as _json, os as _os, re as _re
_B17 = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\batch17_20261019'
_info = _json.load(open(_os.path.join(_B17, 'checks', 'b17_roots.json')))
_ship = open(_os.path.join(_B17, 'checks', 'ship_plan.txt'), encoding='utf-8').read().split('SHIP ', 1)[1].split('\n', 1)[0].split()
_old_masters = set(_re.findall(r'11_MASTERS/(\w+)_MASTER\.SLDPRT', open(_os.path.join(_B17, 'old_files', 'MANIFEST.txt'), encoding='utf-8').read()))
_chg = {}
_cur = None
for _l in open(_os.path.join(_B17, 'checks', 'verdict.txt'), encoding='utf-8'):
    _m = _re.match(r'(\S+)\s+(PASS|CHECK)', _l)
    if _m:
        _cur = _m.group(1)
    elif 'CHANGED (table cells changed)' in _l:
        _chg[_cur] = _chg.get(_cur, 0) + 1

QA = [
    ('173',
     'Batch 17 shipped - RUN_ME_batch17.txt: the 2026-10-18 stage (OMi answers, Brennan rows waves 1-3 marked $PRP@DimSource BRENNAN, A19-A23, the 37 wrongly-DROP adapters + wave-3 adapter rows, the rows of the 5 new generator features) + the merged generator features (hose barb, flange legs, 45 deg angled legs, per-leg swivels, straights) (user "can you ship batch 17?", 2026-10-19)',
     'Rebased on the live state after batch 16: stage review tables = live 04_DESIGN_TABLES + logged batch-17 edits, 0 stale cells (tools/_out/batch17_20261019/checks/cmp3_full.txt). adapters77 already inside the stage (apply_77.py never run). Regenerated every root: control = live tools + live tables reproduces 03_SCRIPTS / 04 SW2 (known pre-2026-09-25 macros aside); batch 17 = tools_b17 (merged tools + the Atan2V fix, QA #174) on the stage -> 80 roots change (regen/cmp.txt, checks/detail_cmp.txt); 98 old configurations change, every one on a row with a logged edit. Static checks clean (allcfg, dofcheck, vbacheck, regress). SolidWorks 2026 SP4 dry runs of all 80 (sw_dryrun/, out_g*.txt, checks/verdict.txt): 74 PASS - 0 FAIL lines (5406HHP / 5406SHP: 1 accepted extent-check FAIL each, loose GetPartBox around the live helix, exact size = table), 1 body per configuration, every old configuration identical to a read-only sweep of the live master or changed together with its own table cells (A19 / A20 / A21 / A23; 92). Post-ship: live tools + live tables regenerate the shipped macros + SW2 (checks/verify_b17.txt).',
     'Toolchain tools_b17 deployed to tools/ (gen_tee.py, gen_straight2.py, checks/allcfg_check.py, checks/dofcheck_tee.py, measure/npsm.py changed; 8 measure scripts added). 74 masters -> 11_MASTERS (24 new, 50 replaced; the hand-built 6400 replaced by the generated one, A6), 74 macros (LF) + 74 reports -> 03_SCRIPTS, 74 SW2 + 88 review tables -> 04_DESIGN_TABLES. BUILD rows 1,804 -> 1,874; configurations in a master 1,103 -> 1,354; 95 masters in 11_MASTERS; MISSING 619 -> 440; VERIFIED 169 -> 336. Old files -> _to_delete/superseded_20261019b/batch17_replaced/ + tools/_out/batch17_20261019/old_files/ (MANIFEST*.txt). Incidents during the dry runs (no effect on the shipped files): SolidWorks closed twice (21:28 during my VBA bisect, 23:16 together with ViewServerV6.exe); Excel crashed at 23:22 during a design-table insert and left SolidWorks unable to insert tables - those dry runs were discarded and re-run.',
     'INFO',
     'None. Brennan-only rows are reversible (revert_brennan.py). Open user calls shipped with their assumption in AxialSource: 6902-12-12-NWO-FG composed shape, 5505-20-20-FG on the -08 shape.'),
    ('174',
     'Generator fix: the 45 deg angled-leg macros did not compile in SolidWorks (Atan2V ByRef argument type mismatch)',
     'All 6 angled roots (1503 1504 5501 5503 5505 6902) failed to load in 0.6 s ("macro did not load/compile"); found by loading half-stubbed test modules (tools/_out/batch17_20261019/bisect): HelixThreadV passes elements of a Variant array (xf.ArrayData) to Atan2V(y As Double, x As Double) ByRef = compile error. Fix in gen_tee.py: Function Atan2V(ByVal y As Double, ByVal x As Double). Regenerating every root changes exactly that line in the 6 angled macros, all SW2 identical (regen/b17v2). The 6 then built with 0 FAIL lines.',
     'Static checks (vbacheck) cannot see VBA type errors; the angled feature had never run in SolidWorks.',
     'INFO',
     'None.'),
    ('175',
     'Batch 17: held back on purpose (data stays in the review tables; no master change)',
     '4503 (7 rows) and 4603 (5): the hose face-off on the hose leg (HOSEFACE2 / STUBFILL2) cuts on the wrong side, 4503 bore D2 also picks the face-off circle - the hose-barb notes foresaw this (fallback: block the rows whose corner stands past the hose hex face). 1703-24-24-FG: the leg-2 hex arm (HEX2) extrudes the wrong way in both directions. 1700RC (3 rows, in DesignTable_1700.xlsx) and 1800-08-08: the FLATS sketch is not fully defined in SolidWorks (static dofcheck said fully defined; the cut itself is right). 5404N: the -06 thread sweeps fail again (QA #163) + body-diameter check; its 4-configuration master and macro stay, the 18 OMi-name rows wait.',
     'Dry-run reports in tools/_out/batch17_20261019/sw_dryrun/<root>/; HOLD list in scripts/ship_b17.py.',
     'MEDIUM',
     'Generator work per root (follow-up session): HOSEFACE on the 135 deg / second hose leg, HEX2 direction on 1703 -24, FLATS sketch relations, 5404N -06 thread ends.'),
]
_B17N = 'BATCH 17 2026-10-20: {what}; dry-run build moved into 11_MASTERS (0 FAIL, 1 body per configuration); RUN_ME_batch17.txt; QA #173'
NOTES = {}
for _r in _ship:
    _i = _info[_r]
    if _r not in _old_masters:
        _w = f'NEW master {_r} ({_i["b17"]} configurations)'
    else:
        _w = f'{_i["control"]} -> {_i["b17"]} configurations' + (f' (+{len(_i["new"])})' if _i['new'] else '')
        _n = _chg.get(_r, 0)
        _w += f'; {_n} old configuration(s) changed with their table cells (A19 / A20 / A21 OMi values)' if _n else '; old configurations identical to the previous master'
        if _i['prpchg']:
            _w += '; properties updated (DataStatus / DimSource / AxialSource)'
    if _r == '6400':
        _w = 'generated master (66 configurations, 6400-L folded) replaces the hand-built one (A6); the hand-built master\'s 8 DROP configurations are not generated'
    if _r in ('1503', '1504', '5501', '5503', '5505', '6902'):
        _w += ' - 45 deg angled legs (helical thread on the 135 deg leg, HelixThreadV; QA #174 fix)'
    NOTES[_r] = _B17N.format(what=_w)
_HOLDN = 'BATCH 17 2026-10-20: HELD (QA #175) - {why}; rows stay in the review table'
NOTES.update({'4503': _HOLDN.format(why='hose face-off on the 135 deg hose leg fails in SolidWorks'),
              '4603': _HOLDN.format(why='hose face-off on the hose leg fails in SolidWorks'),
              '1703': _HOLDN.format(why='HEX2 extrudes the wrong way at -24'),
              '1800': _HOLDN.format(why='FLATS sketch not fully defined in SolidWorks')})
STATUS = {}   # filled by the updater from the live sheet: TABLED / SKELETON-MISSING / TABLED - master not built -> BUILT for new masters
