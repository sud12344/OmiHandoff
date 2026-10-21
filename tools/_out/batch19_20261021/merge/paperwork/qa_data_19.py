# Batch 19 (2026-10-21): data block for update_masterdata_19.py (QA_Log rows, Topologies notes, master status changes).
import json as _json, os as _os, re as _re
_M = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\batch19_20261021\merge'
_ship = _json.load(open(_os.path.join(_M, 'ship_roots.json')))
_res = _json.load(open(_os.path.join(_M, 'regen_cmp.json')))
_old = set(_re.findall(r'11_MASTERS/(\w+)_MASTER\.SLDPRT', open(_os.path.join(_M, 'old_files', 'MANIFEST.txt'), encoding='utf-8').read()))
assert len(_ship) == 31

QA = [
    ('179',
     'Batch 19 shipped - RUN_ME_batch19.txt: the "(d) generator / table work only" list of BLOCKED_NEEDS (2026-10-20), user 2026-10-21 "finish the 94 parts that need no input from me": answered-question rows (A1 / A8 / A10 / A11 / A12 / A18), own-STEP rows measured on their Brennan STEPs, Air-Way-not-buildable -> Brennan cells (Q1), new masters 3474 / 2613 / 6603 / 0319 / FS2500N1, 2500 / 2603 moved from the hand-built HX macros to gen_tee (A7)',
     'Five staging agents (tools/_out/batch19_20261021/A_answered, B_newspec, C_ownstep, D_geom, E_gen; README + CHANGES.csv each), merged in merge/ (tools_b19 = live tools + their generator patches; root19 = live tables + 34 edited / new review tables, no table edited twice). regen19.py: every root regenerated - 0 old configurations changed in any SW2 (only new configurations; the 6 pre-2026-09-25 / held roots differ as before). Static checks clean (dofcheck, allcfg, vbacheck; merge/checks). SolidWorks 2026 SP4 dry runs of 32 roots: 31 PASS - 0 FAIL, 1 body per configuration, every old configuration identical to a read-only sweep of the master it replaces (2500: corner puck inset 0.0005 = the batch-16 fix, -0.014 ... -0.032 % volume; 2500 / 2603: 16 + 30 non-OMi / DROP configurations of the HX masters dropped); 2502 FAILED (QA #180) and was parked. Post-ship: live tools + live tables regenerate the 31 shipped macros + SW2 (checks/verify_b19.txt, 0 BAD; 2408 now matches too).',
     'tools_b19 deployed (gen_straight2.py: 3474 adjustable-ORB straight; gen_tee.py: SPECs 2613 / 2500 / 2603 / FS2500N1 (FS_MIXED, leg_FSM per leg), 6603 out of SPEC_WAITING, 2502 parked in SPEC_WAITING; gen_ring.py: SPEC 0319 sleeves; measure/orb_straight.py + straight_model.py added). 31 masters -> 11_MASTERS (7 new: 0319 2500 2603 2613 3474 6603 FS2500N1; 24 replaced), hand-built 2500HX / 2603HX master + macro + report + SW2 RETIRED (A7). BUILD rows in a master 1,534 -> 1,610; 156 masters; OMi parts 1,531 -> 1,607 of 2,535. Brennan cells under Q1: 2406-16-04 L23 1.840, 2408-14 HEXB 1.250, 1501-24-24-FG CHEX 2.125, 6802-04-06-NWO-FG HEXB 0.688, 1501-04-02-FG D 0.13, 1502-04-04-FG M1 0.99 / W3 1.18. Assumptions logged per row: 0319 shape scaled from BRENNAN_0319-08 (collar 0.220 / 0.560 of L, cone 33 deg); 6504 swivel offset = SWIV_MEAS NOSETIP_B (A12 "end library value per size"); 3474 adjustable thread length = Air-Way 6801 0.469 (Brennan STEP 0.410); 2613 branch M1 = Brennan forged 1.22 (Air-Way prints the plain part 1.01). Old files -> _to_delete/superseded_20261021/batch19_replaced/ + merge/old_files/ (MANIFEST*.txt).',
     'INFO',
     'Next: QA #181 (the rows that need the user / files).'),
    ('180',
     '2502 (90 deg male JIC x female pipe elbow) NOT moved to the generator: 2502-20-20-FG POCKETCUT2 fails in SolidWorks',
     'Dry run of the generated 2502 master (merge/dryrun/2502): the MS51503 P1 tap-drill pocket (1.16 deep in the 1.70 port leg) ends 0.54 from the crossing = exactly the run bore radius (D 1.08 / 2) - its floor is tangent to the cross bore; POCKETCUT2 rebuild error 1, +15.6 % volume. The hand-built 2502HX used 1.14 (0.02 short of its own thread P1), which cleared it.',
     '2502 parked in SPEC_WAITING (gen_tee); 2502HX master / macro / SW2 unchanged; its 2 new rows 2502-06-08-FG / 2502-16-20-FG (table filled, ASSUMED) wait. Needs: how the pocket meets the cross bore when they touch (e.g. run the pocket into the crossing, or keep P1 short by a set margin) - a modelling decision.',
     'MEDIUM',
     'Follow-up.'),
    ('181',
     'Batch-19 rows that still need the user or files (from the (d) list)',
     'Staging reports (A_answered, B_newspec, C_ownstep, D_geom README.md).',
     '2404-40-40: ONE_BORE_2404_OK is the user\'s list - every source gives one bore 2.318 (Brennan TFA p6, OMi row 531): accept? | 2705-04-02 / 2705-LN-04-02: -02 bulkhead I1 - Brennan 2700-02-02 1.07 vs 2706-04-02 1.11: pick or new source | 5503-02-02-FG: 1/8 NPTF port fills the 0.47 leg: BRENNAN_5503-02-02-FG.stp or "cap at leg - 0.05" | 6420-08-08: ports overlap at OMi 1.5: shorten the pipe drill to 0.812 (as 5000-08-08) or build the Brennan 1.62 body (same as open 6420-12-12) | 6316-08 / -12 / -16: butt-weld end has no shape source: BRENNAN_6316-08 / -12 / -16.stp | 6506-12-14: no -14 swivel in SWIV_MEAS (swiv.py needs a straight-body mode) + L17 / L18 (OMi / Brennan 2.34 / 1.75 or Air-Way L18 + offset) | 5404-N long nipples (4) wait for the 5404N -06 fix (QA #178).',
     'INFO',
     'Ask the user.'),
]

NOTES = {}
for _r in sorted(_ship):
    _v = _res[_r]
    if _v['status'] == 'NEW':
        NOTES[_r] = f'2026-10-21 BATCH 19 SHIPPED (QA #179): NEW master ({_v.get("n")} configurations)' + (' - replaces the hand-built ' + _r + 'HX (A7)' if _r in ('2500', '2603') else '')
    else:
        NOTES[_r] = f'2026-10-21 BATCH 19 SHIPPED (QA #179): +{len(_v["new"])} configuration(s) ({", ".join(_v["new"][:6])}); old configurations unchanged; master replaced'
NOTES['2502'] = '2026-10-21 BATCH 19: generator move parked (QA #180, 2502-20-20-FG pocket tangent to the cross bore); 2502HX master stays'
STATUS = {}
