"""build_endlib.py (2026-10-20): the -08 ORFS end entries proposed for the generator, from pilot_meas.json (validate_pilots.py).
Shape values only (Q-TRANSFER-ENDLIB / "Brennan 3D files for SHAPE only"): lengths the rows give (legs, hexes, nut, collar dia, stud
lengths) stay row inputs. Every entry names its STEP. Nothing is written into a generator or table. Output: end_lib_08.json."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(HERE, 'pilot_meas.json')))
f, bh, sw, st, st2, nut, lk, sl = (m[k] for k in ('FSM FS2403-08-08 +X', 'FSBH FS2701-08-08-FG', 'FSSW FS6500-08-08-FG', 'STUD FS6400-08-08-O',
                                                  'STUD FS6801-08-08-NWO-FG', 'NUT FS0318-08', 'LOCKNUT FS0306-08', 'SLEEVE FS0319-08'))
fg = m['FSM FS6500-08-08-FG']
coll = [s for s in bh['BH_STEPS'] if s[0] == 'cyl' and abs(s[1] - 0.5) < 0.002][0]
step = [s for s in bh['BH_STEPS'] if s[0] == 'cyl' and bh['RELR'] + 0.01 < s[1] < coll[1]][0]
lib = {
  'FSM_MEAS[8]': dict(
      src='BRENNAN_FS2403-08-08 (both ends), = FS6400-08-08-O, FS6500-08-08-FG, FS6801-08-08-NWO-FG, FS2701-08-08-FG male legs (checks.txt (1))',
      GI=f['GI'], GO=f['GO'], GD=f['GD'], FR=f['FR'], CH=f['CH'], CH_ANG=f['CH_ANG'], ENDL=f['ENDL'],
      straight=dict(THD_END=f['THD_END'], FLANK_ANG=f['FLANK_ANG'], RELR=f['RELR'], RELL=f['RELL'],
                    note='thread major from CH to THD_END, 60 deg flank to the relief, relief to the hex face at ENDL'),
      forged=dict(THD_END=fg['THD_END'], note='thread major from CH to ENDL, then a radial step down to the forged flats radius (row S2 / 2) and '
                                              'the body chamfer (75 deg) to the hex corners'),
      oring_check=dict(ID=0.489, W=0.07, src='fused O-ring in the groove = Air-Way FS4000-08; not modelled (as the ORB / NWO ends)'),
      thread='FS_THR[8] 13/16-16 UN (major 0.8125); bore from the row'),
  'FSBH_MEAS[8]': dict(
      src='BRENNAN_FS2701-08-08-FG bulkhead leg; nose = FSM_MEAS[8] (checks.txt (1))',
      THD_END=bh['THD_END'], RELR=bh['RELR'], RELL=bh['RELL'], REL_END=bh['REL_END'],
      STEPR=step[1], STEPL=round(step[3] - step[2], 4), COLLARL=round(coll[3] - coll[2], 4),
      note='from the tip: FSM nose, thread major to THD_END, 60 deg flank, relief RELR to REL_END, step STEPR over STEPL (= Air-Way i4) to the collar '
           'face at i2 (row), collar d17 (row) over COLLARL, then the forged body. REL_END = i2 - i4 on the pilot.'),
  'FSSW_MEAS[8]': dict(
      src='BRENNAN_FS6500-08-08-FG swivel leg; nut outside / thread / lip = FS0318-08 where marked (checks.txt (2))',
      reference='the row leg (Air-Way L21 / Brennan AAA) = crossing -> the stem SEAL FACE (not the nut face)',
      SEAL_TO_NUTFACE=sw['SEAL_TO_NUTFACE'], STEMR=sw['STEMR'], HEADL=round(sw['SEAL_a'] - sw['HEAD_REAR_a'], 4),
      NECKR=sw['NECKR'], SEAL_TO_BODYFACE=round(sw['SEAL_a'] - sw['BODYFACE_a'], 4),
      NUTL=sw['NUTL'], NUT_AF='row SHEX (= FS0318-08 0.938)', NUT_HEX_s=sw['NUT_HEX_s'], NUT_CHAMFER_ANG=30,
      NUT_SKIRT=dict(note='from the rear hex chamfer foot (s 0.482, r 0.46) a 12.3 deg cone to r 0.419 at s 0.67, a groove r 0.4022 over s 0.685 - 0.812, '
                          'r 0.419 to the rear face at s 0.827', raw=sw['NUT_OUTSIDE']),
      MOUTH_R=sw['MOUTH_R'], MOUTH_DEPTH=sw['MOUTH_DEPTH'], MINR=sw['MINR'], TE=sw['TE'],
      CAV_REL=dict(note='45 deg up to r 0.4165 at s 0.45, then a 13 deg cone down to r 0.375 at s 0.63 (= the stem head rear)', raw=sw['CAV_REL']),
      LIPR=sw['LIPR'], LIP_s=sorted(sw['LIP_s']),
      thread='HELIX (helix + swept cut), FS_THR[8] minor 0.7448 - never SolidWorks Thread on a female edge'),
  'FSNUT_MEAS[8]': dict(
      src='BRENNAN_FS0318-08 (loose nut; its outside differs from the swivel nut, checks.txt (2))',
      AF=nut['AF'], L=nut['L'], END_CHAMFER_ANG=75, END_CHAMFER_R=0.469, MOUTH_DEPTH=0.0371, MINR=nut['MINR'], TE=nut['TE'],
      RELR=0.377, LIP_START=0.63, LIPR=0.326, note='A/F and length are row inputs (Air-Way S / h); the rest is shape'),
  'FSLOCKNUT_MEAS[8]': dict(src='BRENNAN_FS0306-08', AF=lk['AF'], H=lk['L'], END_CHAMFER_ANG=75, END_CHAMFER_R=0.5625,
                            COUNTERSINK='45 deg x 0.0371 both faces to r 0.4095', MINR=lk['MINR'], note='A/F and thickness are row inputs (Air-Way S4 / h2)'),
  'FSSLEEVE_MEAS[8]': dict(src='BRENNAN_FS0319-08', L=sl['L'], COLLAR_R=sl['OD_R'], COLLARL=sl['COLLARL'], SPIGOT_R=0.321, TAPER='15 deg from r 0.2975 at the '
                           'tube-side face to r 0.321 at 0.0877', BORE_R=sl['BORE_R'], BRAZE_CLEAR=round(2 * sl['BORE_R'] - 0.5, 4), STOP_R=sl['STOP_R'],
                           note='seal face at the collar end (flat, r 0.2047 - 0.3725); L and d8 are row inputs; per-size rule: R7 / STEPS_NEEDED part 4'),
  'ORB_FS[8]': dict(src='BRENNAN_FS6400-08-08-O', TIPCH=st['TIPCH'], RMAJ=st['RMAJ'], THD_END=st['THD_END'], FLANK_END=st['FLANK_END'], UCR=st['UCR'],
                    UCL=st['UCL'], SHOULDER=st['SHOULDER'], note='= ORB[8] undercut 0.660 x 0.094; the thread is longer (tip -> flank end 0.457 vs '
                    'ORB THDL 0.344); the tip -> hex face length is the row input (Air-Way L8 - L9, Q-FS-ORBSTUD (a))'),
  'NWO_FS[8]': dict(src='BRENNAN_FS6801-08-08-NWO-FG', TIPCH=st2['TIPCH'], RMAJ=st2['RMAJ'], THD_END=st2['THD_END'], FLANK_END=st2['FLANK_END'],
                    UCR=st2['UCR'], UCL=st2['UCL'], WASHER_R=0.505, WASHER_T=0.041, LOCKNUT_T=0.41, LOCKNUT_AF='row S3HEX (0.938)',
                    LOCKNUT_CHAMFER='75 deg to r 0.469 both faces', NECKR=0.375, NECKL=0.039,
                    note='= NWO_MEAS[8] undercut 0.146 + washer 0.505 x 0.041; thread longer (+0.050); lock nut bigger than the JIC 6801 one (0.938 x 0.41 '
                         'vs 0.875 x 0.31); the tip -> washer face length is the row input (Air-Way L10 - L11)'),
}
json.dump(lib, open(os.path.join(HERE, 'end_lib_08.json'), 'w'), indent=1)
print(json.dumps({k: {x: y for x, y in v.items() if not isinstance(y, (dict, list))} for k, v in lib.items()}, indent=1)[:3000])
