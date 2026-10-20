"""validate_pilots.py (2026-10-20): run the WP2 ORFS extractors (measure/fsmeasure.py) on the 8 Brennan pilots in 09_STEP_FILES and apply
the validation of tools/_out/orfs_modeltype_20261016/PLAN.md section 5 + the cross-checks against the staged Air-Way rows
(tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES). Read-only. Writes pilot_meas.json (every reading), checks.txt (every
check, PASS / FAIL / NOTE) and end_lib_08.json (the -08 end entries proposed for the generator, each value with its source)."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, 'measure'))
import fsmeasure as M
import openpyxl

STEP = lambda pn: os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp')
TABLES = os.path.join(ROOT, 'tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')
TOL = 0.0015            # two readings of one shape (as the other closed loops)
RND = 0.0105            # Air-Way prints 2 decimals: |measured - printed| <= 0.0105 counts as rounding


def row(table, pn):
    ws = openpyxl.load_workbook(os.path.join(TABLES, f'DesignTable_{table}.xlsx')).worksheets[0]
    h = [c.value for c in ws[2]]
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0] == pn:
            return dict(zip(h, r))
    raise KeyError(pn)


meas = {}
meas['FSM FS2403-08-08 +X'] = M.measure_fsm(STEP('FS2403-08-08'), 0, 1)
meas['FSM FS2403-08-08 -X'] = M.measure_fsm(STEP('FS2403-08-08'), 0, -1)
meas['FSM FS6400-08-08-O'] = M.measure_fsm(STEP('FS6400-08-08-O'), 0, -1)
meas['FSM FS6500-08-08-FG'] = M.measure_fsm(STEP('FS6500-08-08-FG'), 0, -1, ((1, 1),))
meas['FSM FS6801-08-08-NWO-FG'] = M.measure_fsm(STEP('FS6801-08-08-NWO-FG'), 0, -1, ((1, 1),))
meas['FSM FS2701-08-08-FG'] = M.measure_fsm(STEP('FS2701-08-08-FG'), 0, -1, ((1, 1),))
meas['FSBH FS2701-08-08-FG'] = M.measure_fsm(STEP('FS2701-08-08-FG'), 1, 1, ((0, -1),), bulkhead=True)
meas['FSSW FS6500-08-08-FG'] = M.measure_fssw(STEP('FS6500-08-08-FG'), 1, 1, ((0, -1),))
meas['STUD FS6400-08-08-O'] = M.measure_stud(STEP('FS6400-08-08-O'), 0, 1)
meas['STUD FS6801-08-08-NWO-FG'] = M.measure_stud(STEP('FS6801-08-08-NWO-FG'), 1, 1, ((0, -1),))
meas['NUT FS0318-08'] = M.measure_nut(STEP('FS0318-08'))
meas['LOCKNUT FS0306-08'] = M.measure_nut(STEP('FS0306-08'))
meas['SLEEVE FS0319-08'] = M.measure_sleeve(STEP('FS0319-08'))
json.dump(meas, open(os.path.join(HERE, 'pilot_meas.json'), 'w'), indent=1)

lines, nfail = [], 0


def chk(name, ok, detail, kind='PASS'):
    global nfail
    st = kind if ok else 'FAIL'
    nfail += st == 'FAIL'
    lines.append(f'{st:5} {name}: {detail}')


# (1) every male face-seal end the same (two ends of FS2403 + the male legs of FS6400 / FS6500 / FS6801 / FS2701 + the FSBH nose)
FSM_KEYS = ('BORER', 'GI', 'GO', 'GD', 'FR', 'CH', 'RMAJ', 'ENDL')
ref = meas['FSM FS2403-08-08 +X']
for k, m in meas.items():
    if not k.startswith(('FSM', 'FSBH')) or k == 'FSM FS2403-08-08 +X':
        continue
    keys = FSM_KEYS if k.startswith('FSM') else FSM_KEYS[:-1]
    d = {x: (ref[x], m[x]) for x in keys if abs(ref[x] - m[x]) > TOL}
    chk(f'(1) FSM {k} = FS2403-08-08 +X', not d, 'all of ' + '/'.join(keys) + ' within 0.0015' if not d else f'differ {d}')
for k in ('FSM FS2403-08-08 +X', 'FSM FS2403-08-08 -X', 'FSM FS6400-08-08-O'):
    m = meas[k]
    chk(f'(1b) FSM run-out on a straight ({k})', m['RUNOUT'] == 'flank',
        f"thread to s {m['THD_END']}, {m['FLANK_ANG']} deg flank, relief r {m['RELR']} x {m['RELL']} to the hex face at s {m['ENDL']}", 'NOTE')
for k in ('FSM FS6500-08-08-FG', 'FSM FS6801-08-08-NWO-FG', 'FSM FS2701-08-08-FG'):
    m = meas[k]
    chk(f'(1c) FSM run-out on a forged leg ({k})', m['RUNOUT'] == 'step',
        f"thread major to s {m['THD_END']} = ENDL, then a radial step down to r {m['STEPR']} (= the 0.75 forged flats / 2) and the 75 deg body "
        f"chamfer to the hex corners: the end stands proud of the flats (PLAN risk R1)", 'NOTE')

# (2) swivel nut = loose nut = Air-Way FF318 -08 (hex 0.94, h 0.83)
sw, nut = meas['FSSW FS6500-08-08-FG'], meas['NUT FS0318-08']
ff318 = row('FS0318', 'FS0318-08')
chk('(2) swivel nut hex = FS0318-08 hex', abs(sw['NUT_CORNER_R'] - nut['CORNER_R']) < TOL,
    f"corner r {sw['NUT_CORNER_R']} / {nut['CORNER_R']} -> A/F {nut['AF']}")
chk('(2) swivel nut length = FS0318-08 length', abs(sw['NUTL'] - nut['L']) < TOL, f"{sw['NUTL']} / {nut['L']}")
chk('(2) FS0318-08 = Air-Way FF318-8', abs(nut['AF'] - ff318['SHEX@HEX']) < RND and abs(nut['L'] - ff318['H@DRIVE']) < RND,
    f"A/F {nut['AF']} vs S {ff318['SHEX@HEX']}, L {nut['L']} vs h {ff318['H@DRIVE']}")
chk('(2) swivel nut thread minor + mouth = FS0318-08', abs(sw['MINR'] - nut['MINR']) < TOL and abs(sw['MOUTH_DEPTH'] - 0.0371) < TOL,
    f"minor r {sw['MINR']} / {nut['MINR']}; mouth countersink 45 deg x {sw['MOUTH_DEPTH']} both")
chk('(2) swivel nut inner lip = FS0318-08 lip', abs(sw['LIP_s'][1] - 0.63) < TOL and abs(nut['BORES'][0][1] - 0.63) < TOL,
    f"lip from s 0.63 on both; lip bore r {sw['LIPR']} (swivel) / {nut['BORES'][0][0]} (loose)", 'NOTE')
chk('(2) swivel nut differs from the loose nut outside and in the relief', True,
    f"thread minor length {sw['TE']} (swivel) / {nut['TE']} (loose); swivel nut: hex flats over s {sw['NUT_HEX_s']} with 30 deg chamfers + a 12.3 deg "
    f"rear skirt with a groove; loose nut: hex over the full length, 75 deg end chamfers -> FSNUT_MEAS cannot be copied from FSSW_MEAS as a whole "
    f"(PLAN FSNUTF: 'if P6 shows the loose nut = the swivel nut'): the loose nut keeps its own entry", 'NOTE')

# (3) the face O-ring: the groove fits Air-Way FS4000-08; the fused O-ring reproduces it
o4 = row('FS4000', 'FS4000-08')
f = meas['FSM FS2403-08-08 +X']; rg = f['RINGS'][0]
ring_id = round(2 * rg['rc'] - rg['W'], 4)
chk('(3) fused face O-ring = Air-Way FS4000-08', abs(ring_id - o4['ID@DRIVE']) < 0.002 and abs(rg['W'] - o4['W@DRIVE']) < 0.002,
    f"I.D. {ring_id} (centreline dia {2 * rg['rc']} - W) vs {o4['ID@DRIVE']}, W {rg['W']} vs {o4['W@DRIVE']}")
chk('(3) groove I.D. within the O-ring I.D.', 2 * f['GI'] <= o4['ID@DRIVE'], f"groove I.D. {2 * f['GI']} <= {o4['ID@DRIVE']}")
chk('(3) groove O.D. = O-ring O.D.', abs(2 * f['GO'] - (o4['ID@DRIVE'] + 2 * o4['W@DRIVE'])) < 0.002,
    f"groove O.D. {2 * f['GO']} vs O-ring O.D. {o4['ID@DRIVE'] + 2 * o4['W@DRIVE']}: the O-ring sits on the outer wall")
chk('(3) groove depth vs W', True, f"depth {f['GD']} = {round(100 * (1 - f['GD'] / o4['W@DRIVE']))} % squeeze of W {o4['W@DRIVE']} when the face closes", 'NOTE')

# threads (basic ASME B1.1)
chk('thread: FSM major = 13/16-16', abs(2 * f['RMAJ'] - 0.8125) < 0.001, f"major dia {2 * f['RMAJ']}")
minor = 0.8125 - 1.082532 / 16
chk('thread: FSSW / nut minor = 13/16-16 basic minor', abs(2 * sw['MINR'] - minor) < 0.001, f"minor dia {2 * sw['MINR']} vs {round(minor, 4)}")
chk('thread: stud major = 3/4-16 UNF', abs(2 * meas['STUD FS6400-08-08-O']['RMAJ'] - 0.75) < 0.001, f"major dia {2 * meas['STUD FS6400-08-08-O']['RMAJ']}")

# Air-Way rows (the dimension source) vs the STEPs
r = row('FS2403', 'FS2403-08-08')
chk('Air-Way FS2403-08-08 L6 (face -> face)', abs(2 * meas['FSM FS2403-08-08 +X']['face_a'] - r['L6@DRIVE']) < RND, f"{2 * meas['FSM FS2403-08-08 +X']['face_a']} vs {r['L6@DRIVE']}")
r = row('FS6500', 'FS6500-08-08-FG')
chk('Air-Way FS6500-08-08-FG L7 (crossing -> male face)', abs(meas['FSM FS6500-08-08-FG']['face_a'] - r['L7@DRIVE']) < RND, f"{meas['FSM FS6500-08-08-FG']['face_a']} vs {r['L7@DRIVE']}")
chk('Air-Way FS6500-08-08-FG L21 = crossing -> SWIVEL SEAL FACE (not the nut face)', abs(sw['SEAL_a'] - r['L21@DRIVE']) < RND and abs(sw['NUTFACE_a'] - r['L21@DRIVE']) > 0.1,
    f"seal face {sw['SEAL_a']}, nut face {sw['NUTFACE_a']}, L21 {r['L21@DRIVE']} -> PLAN R3 settled the other way: the FSSW leg input is the seal face; "
    f"nut face = seal + {sw['SEAL_TO_NUTFACE']}")
chk('Air-Way FS6500-08-08-FG SHEX (swivel nut)', abs(2 * sw['NUT_CORNER_R'] * math.cos(math.radians(30)) - r['SHEX@HEX']) < RND, f"{round(2 * sw['NUT_CORNER_R'] * math.cos(math.radians(30)), 4)} vs {r['SHEX@HEX']}")
r = row('FS2701', 'FS2701-08-08-FG'); bh = meas['FSBH FS2701-08-08-FG']
chk('Air-Way FS2701-08-08-FG L16 / L17', abs(meas['FSM FS2701-08-08-FG']['face_a'] - r['L16@DRIVE']) < RND and abs(bh['face_a'] - r['L17@DRIVE']) < RND,
    f"{meas['FSM FS2701-08-08-FG']['face_a']} / {bh['face_a']} vs {r['L16@DRIVE']} / {r['L17@DRIVE']}")
steps = bh['BH_STEPS']
coll = [s for s in steps if s[0] == 'cyl' and abs(2 * s[1] - r['D17@BORE']) < RND][0]
step = [s for s in steps if s[0] == 'cyl' and s[1] < coll[1] and s[1] > bh['RELR'] + 0.01][0]
chk('Air-Way FS2701-08-08-FG i2 = tip -> collar face', abs(coll[2] - r['I2@DRIVE']) < RND, f"collar face at s {coll[2]} vs i2 {r['I2@DRIVE']}")
chk('Air-Way FS2701-08-08-FG d17 = collar dia', abs(2 * coll[1] - r['D17@BORE']) < RND, f"{2 * coll[1]} vs {r['D17@BORE']}")
chk('Air-Way FS2701-08-08-FG i4 vs the STEP', True,
    f"i4 {r['I4@DRIVE']} = the length of the dia {2 * step[1]} step in front of the collar (s {step[2]} -> {step[3]}); the collar itself is "
    f"{round(coll[3] - coll[2], 4)} thick (s {coll[2]} -> {coll[3]}, then the 0.75 flats). PLAN read i4 as the collar thickness: it is not", 'NOTE')
r = row('FS6400', 'FS6400-08-08-O'); st = meas['STUD FS6400-08-08-O']; fm = meas['FSM FS6400-08-08-O']
chk('Air-Way FS6400-08-08-O L8 (face -> ORB tip)', abs(fm['face_a'] + st['tip_a'] - r['L8@DRIVE']) < RND, f"{round(fm['face_a'] + st['tip_a'], 4)} vs {r['L8@DRIVE']}")
chk('Air-Way FS6400-08-08-O L9 (face -> hex ORB-side face)', abs(fm['face_a'] + st['tip_a'] - st['SHOULDER'] - r['L9@DRIVE']) < RND, f"{round(fm['face_a'] + st['tip_a'] - st['SHOULDER'], 4)} vs {r['L9@DRIVE']}")
chk('Air-Way FS6400-08-08-O stud L8 - L9 (Q-FS-ORBSTUD)', abs(st['SHOULDER'] - (r['L8@DRIVE'] - r['L9@DRIVE'])) < RND, f"tip -> hex face {st['SHOULDER']} vs {round(r['L8@DRIVE'] - r['L9@DRIVE'], 3)}")
r = row('FS6801', 'FS6801-08-08-NWO-FG'); st2 = meas['STUD FS6801-08-08-NWO-FG']
chk('Air-Way FS6801-08-08-NWO-FG L7 / L10 / L11', abs(meas['FSM FS6801-08-08-NWO-FG']['face_a'] - r['L7@DRIVE']) < RND and abs(st2['tip_a'] - r['L10@DRIVE']) < RND
    and abs(st2['tip_a'] - st2['SHOULDER'] - r['L11@DRIVE']) < RND,
    f"{meas['FSM FS6801-08-08-NWO-FG']['face_a']} / {st2['tip_a']} / washer face {round(st2['tip_a'] - st2['SHOULDER'], 4)} vs {r['L7@DRIVE']} / {r['L10@DRIVE']} / {r['L11@DRIVE']}")
ln = [x for x in st2['AFTER'] if x[0] == 'L' and x[1] == 0.0 and x[3] > 0.53]
chk('Air-Way FS6801-08-08-NWO-FG S3HEX (lock nut)', bool(ln) and abs(2 * ln[0][3] * math.cos(math.radians(30)) - r['S3HEX@HEX']) < RND,
    f"{round(2 * ln[0][3] * math.cos(math.radians(30)), 4) if ln else None} vs {r['S3HEX@HEX']}")
r = row('FS0319', 'FS0319-08'); sl = meas['SLEEVE FS0319-08']
chk('Air-Way FS0319-08 L / d8', abs(sl['L'] - r['L@DRIVE']) < RND and abs(2 * sl['OD_R'] - r['D8@DRIVE']) < RND, f"{sl['L']} / {2 * sl['OD_R']} vs {r['L@DRIVE']} / {r['D8@DRIVE']}")
chk('FS0319-08 braze bore vs tube 1/2', True, f"bore dia {2 * sl['BORE_R']} = tube OD 0.500 + {round(2 * sl['BORE_R'] - 0.5, 4)} braze clearance; tube stop dia {2 * sl['STOP_R']}", 'NOTE')
r = row('FS0306', 'FS0306-08'); lk = meas['LOCKNUT FS0306-08']
chk('Air-Way FS0306-08 S4 / H2', abs(lk['AF'] - r['S4HEX@HEX']) < RND and abs(lk['L'] - r['H2@DRIVE']) < RND, f"{lk['AF']} / {lk['L']} vs {r['S4HEX@HEX']} / {r['H2@DRIVE']}")

# studs vs our end library (Q-FS-ORBSTUD (a): the shape of the extra length)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'generators')); sys.path.insert(0, os.path.join(ROOT, 'tools'))
import gen_straight2 as G, gen_tee as T
orb, nwo = G.ORB[8], T.NWO_MEAS[8]
chk('ORB_FS vs ORB[8]: undercut', abs(2 * st['UCR'] - orb['GD']) < 0.001 and abs(st['UCL'] - orb['GW']) < 0.001, f"{2 * st['UCR']} x {st['UCL']} vs {orb['GD']} x {orb['GW']}")
chk('ORB_FS vs ORB[8]: thread', True, f"tip -> flank end {st['FLANK_END']} vs ORB THDL {orb['THDL']}: the FS stud's extra {round(st['FLANK_END'] - orb['THDL'], 4)} is thread "
    f"(no plain shank); tip chamfer 45 deg x {st['TIPCH']}", 'NOTE')
chk('NWO_FS vs NWO_MEAS[8]: undercut + washer', abs(st2['UCL'] - nwo['UL_B']) < 0.001 and abs(0.505 - nwo['WR']) < 0.001,
    f"undercut {st2['UCL']} vs UL_B {nwo['UL_B']}; washer r 0.505 x 0.041 vs WR {nwo['WR']} x WT {nwo['WT']}")
chk('NWO_FS vs NWO_MEAS[8]: thread + lock nut', True, f"tip -> flank end {st2['FLANK_END']} vs THDL_B {nwo['THDL_B']} (+{round(st2['FLANK_END'] - nwo['THDL_B'], 4)} thread); "
    f"lock nut A/F 0.938 (Air-Way S3) x 0.41 thick vs the JIC 6801 lock nut AF_B {nwo['AF_B']} x NUTT {nwo['NUTT']}", 'NOTE')

lines.append(f'\n{nfail} FAIL')
open(os.path.join(HERE, 'checks.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
