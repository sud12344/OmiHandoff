# Validation of forged.py (2026-10-02): before it is used on the new pilots (2504 / 2505 / 2606 / 2611), the extractor must reproduce the
# values measured EARLIER on other Brennan forged STEPs (each reference is cited where it was recorded):
#   2650-08-08-08-08-FG : hex shoulders 0.593 on every leg, A/F 0.750, bore 0.392  (gen_tee.py docstring, 2603HX pattern)
#   5605-08-08-08-FG    : female port round collar 0.260 long on all 3 legs, dia = the hex flats  (gen_tee.py COLLAR_L comment)
#   5600-16-16-16-FG    : hex stops at N - 0.94 (= the 5404 end length), relief dia 1.315 = pipe OD, flats 1.3125  (gen_tee.py build_rows)
#   6502-08-08-FG       : JIC hex arm to 0.323, JIC tip 0.98, body hex 0.75, corner radius 0.433  (gen_tee.py BRENNAN_NOTES)
#   2403 -08 JIC chain  : TM 0.75, CD 0.659, SL 0.1546, LL 0.0984, end length 0.657  (templates/DesignTable_2403_SW2.xlsx, gen_straight2.JIC)
#   python tools/measure/forged_validate.py   -> PASS/FAIL per value; exit code 1 on any FAIL
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, json
import forged as F

fails = 0


def chk(what, got, want, tol):
    global fails
    ok = got is not None and abs(got - want) <= tol
    fails += not ok
    print(f'{"PASS" if ok else "FAIL"}  {what}: measured {got} vs recorded {want} (tol {tol})')


S = lambda pn: OP.step(pn)
for th in (0, 90, 180, 270):
    R = F.jicm(S('2650-08-08-08-08-FG'), th, 1)
    chk(f'2650-08 leg {th:3d} deg hex shoulder', R['hex_face'], 0.593, 0.0005)
    chk(f'2650-08 leg {th:3d} deg A/F', R['AF_flats'], 0.750, 0.0005)
    chk(f'2650-08 leg {th:3d} deg bore', R['bore_dia'], 0.392, 0.0015)
    chk(f'2650-08 leg {th:3d} deg corner radius (A/F / sqrt 3)', R['corner_r'], 0.750 / 3 ** 0.5, 0.0005)
    for k, v in dict(TM=0.75, CD=0.659, SL=0.1546, LL=0.0984).items():
        chk(f'2650-08 leg {th:3d} deg JIC chain {k} = 2403 -08', R['chain'][k], v, 0.0005)
    chk(f'2650-08 leg {th:3d} deg JIC end length = 2403 -08 (RL + ramp + TZ + LL + SL)', R['end_length'], 0.657, 0.0005)
for th, sd in ((0, -1), (90, 1), (180, 1)):
    R = F.nptff(S('5605-08-08-08-FG'), th, sd)
    chk(f'5605-08 leg {th:3d} deg collar length', R['collar_len'], 0.260, 0.0005)
    chk(f'5605-08 leg {th:3d} deg collar dia = flats', 2 * R['collar_r'], R['AF_flats'], 0.0005)
for th in (0, 90, 180):
    R = F.nptfm(S('5600-16-16-16-FG'), th, -1)
    chk(f'5600-16 leg {th:3d} deg end length (hex stops at N - 0.94)', R['end_length'], 0.94, 0.0005)
    chk(f'5600-16 leg {th:3d} deg relief dia', R['relief_dia'], 1.315, 0.0005)
    chk(f'5600-16 leg {th:3d} deg flats', R['flats_at_face'], 1.3125, 0.0005)
R = F.jicm(S('6502-08-08-FG'), 180, -1)
chk('6502-08 JIC leg hex arm end', R['hex_face'], 0.323, 0.0005)
chk('6502-08 JIC leg tip', R['tip'], 0.98, 0.0005)
chk('6502-08 A/F', R['AF_flats'], 0.75, 0.0005)
chk('6502-08 corner radius', R['corner_r'], 0.433, 0.0005)
chk('6502-08 corner puck arc (z = 0 section)', max(F.corner_arcs(S('6502-08-08-FG'))), 0.433, 0.0005)
print('FAILS', fails)
sys.exit(1 if fails else 0)
