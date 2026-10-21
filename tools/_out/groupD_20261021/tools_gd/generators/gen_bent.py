"""gen_bent.py (2026-10-15; STAGED in tools/_out/newtypes_20261014/generators - not in the live tools/):
review / test table -> SolidWorks build macro + SW2 design table for the BENT-TUBE ("swept") flange elbows:
male JIC end piece  ->  bent tube  ->  SAE code 61 / 62 flange head  (OMi 1703 / 1704 / 1803 / 1804 -Tube).

    python gen_bent.py 1704T 1703T   ->  $GB_OUT (default tools/_out/bent): Build_<root>_MASTER.bas, DesignTable_<root>_SW2.xlsx,
                                          gen_bent_summary_<roots>.json
Tables from $GB_REV (default 04_DESIGN_TABLES; tests: tools/_out/newtypes_20261014/test_tables). DataStatus TEST rows only with
GB_TEST=1 (the macro then says TEST BUILD).  1704T = 90 deg (1704 + 1804 -Tube), 1703T = 45 deg (1703 + 1803 -Tube).

It is the straight 1700 code 61 flange adapter (JIC end + hex + flange head, gen_straight2.py) with a bent tube between the two
ends; the end data come from the same libraries (Q-TRANSFER-ENDLIB = yes): the MS33656J JIC male chain per dash (2403 table) and
the code 61 head (FLG61_MEAS by flange size). Read-only use of the live gen_straight2.py (imported with GS_OUT -> scratch).

Model (Front Plane = the plane of the bend, JIC tip at the origin, JIC axis = +X):
  DRIVE   revolve about X: JIC male chain from the tip + round body BODYR to LJ (= JIC end length + HEXL), hex-cut over the body
          zone (HEXCUT, HEXB across flats) - the end piece, exactly as on the straights.
  PATH    tube centre line: construction line origin -> S (TUBESTART = JIC end length, inside the hex body), line along X to T1
          (T1X), tangent arc RB, tangent line to the flange face point F (FX, FY). Sweep TUBE = circular profile TUBEOD along it.
  HEADSK  flange head half-section about the leg-2 axis (parallel to PATH's last line, face centre on F): face with the O-ring
          groove (FLGB_GRVIR / FLGB_GRVOR / FLGB_GRVD), head radius FLGB_HEADR, thickness FLGB_HEADT; revolved = HEAD.
  PATHX   the same centre line from 0.05 before the JIC tip to 0.05 past the flange face; swept cut BORE = circular TUBEID.
  THD_EndA  JIC thread (Thread feature, suppressed for the save).
  THD_EndB  (6701) female thread in the swivel nut: the straights' HelixThread for an axis parallel to Y - helix on NUTPLN,
          60 deg profile on the Front Plane, swept cut (SolidWorks' Thread feature on that edge crashed SolidWorks, 2026-10-15).
Leg lengths are the library's: M1 = crossing of the two leg axes -> JIC tip, L1 = crossing -> flange face (along leg 2).
Only BUILD rows with DataStatus VERIFIED / ASSUMED (or TEST with GB_TEST=1) and every value pass; geometry checks block the rest."""
import datetime, importlib.util, json, math, os, sys
import openpyxl

# 2026-10-21 (group D): the toolset this file sits in (portable; was the live tools/ on the user's machine, read-only)
LIVE = os.environ.get('GB_TOOLS') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('GS_OUT', os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'omi_gs_scratch'))


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P = _load('omi_paths', os.path.join(LIVE, 'omi_paths.py'))
gs = _load('gen_straight2', os.path.join(P.GENERATORS, 'gen_straight2.py'))      # end libraries + VBA helper library (read-only)
sp3 = gs.sp3

IN = 0.0254
TODAY = datetime.date.today().isoformat()
REV = os.environ.get('GB_REV', P.DESIGN_TABLES)
OUT = os.environ.get('GB_OUT', os.path.join(P.OUT, 'bent'))
TEST = os.environ.get('GB_TEST') == '1'
DEV = P.DEV
BX = 0.05          # PATHX runs this far past the JIC tip and the flange face (bore cut through both ends)

SPEC = {
    '1704T': dict(name='90 deg bent-tube flange elbow (male JIC x SAE code 61 / 62 flange head; 1704 / 1804 -Tube)', bend=90.0,
                  tables=('1704T',), ref='1704-12-12-Tube'),
    '1703T': dict(name='45 deg bent-tube flange elbow (male JIC x SAE code 61 / 62 flange head; 1703 / 1803 -Tube)', bend=45.0,
                  tables=('1703T',), ref='1703-12-12-Tube'),
    '6701': dict(name='90 deg bent-tube swivel elbow (male JIC x female JIC swivel; 6701 / 6701-L)', bend=90.0, tables=('6701T',),
                 ref='6701-08-08', end2='JICSW'),
}
INPUT_SW = ('M1@DRIVE', 'L1@DRIVE', 'CHEX@HEX', 'HEXL@HEX', 'NUTHEX@NUTHEXSK', 'NOSETIP@SWSK', 'D@BORE', 'TUBEOD@TUBE', 'RB@PATH')
# SAE code 62 flange head by flange size - the end data of the new-masters wave-1 FLANGE62 work (tools/_out/newmasters_20261002/work/
# FLANGE62, staged copy of gen_straight2.py line 599, NOTES.md s1-s2): measured with tools/measure/flange62.py on the Brennan 1800-08-08,
# 1824-08 and 1804-08-08-FG STEPs (agree to 0.0002); the extractor returns FLG61_MEAS exactly on the 9 Brennan 1700 STEPs. Only -08 is
# measured; the head OD of a row must agree with it (it is the same standard head). Same head construction as code 61 (thicker, wider).
FLG62_MEAS = {8: dict(O=1.250, TH=0.305, GI=0.345, GO=0.500, GD=0.110)}
FLG62_ASSUME = ('SAE code 62 flange head: thickness and face O-ring groove by flange size measured on the Brennan 1800-08-08 / 1824-08 / '
                '1804-08-08-FG STEPs (wave-1 FLANGE62, flange62.py; single manufacturer - SAE J518 / ISO 6162-2 not in the repo), head OD '
                '= the row (must equal the measured 1.250 at -08); edge chamfers not modelled; -08 only (no STEP with a -12..-32 code 62 head)')
SW_ASSUME = ('6701 leg 2 = the female 37 deg JIC swivel end of the straights (gen_straight2 end_JICSW: SWIV_MEAS by size, nut and nose one '
             'solid), revolved about the leg-2 axis; L1 = crossing -> nut face; the tube ends at the swivel body face (BODYS behind the nut '
             'face); nut hex cut from a plane at the nut face over the measured nut hex length; female UNF-2B nut thread = the straights\' '
             'swivel thread (straight helical thread over the measured length TE from the nut face, base on the ASME B1.1 basic minor, '
             '60 deg, height 0.54127 P; helix on the nut-face plane + swept cut, suppressed for the save)')
ASSUME = ('bent-tube elbow = male JIC end piece (MS33656J chain per dash from the 2403 table, round body BODYR = hex corner radius, '
          'hex HEXB over HEXL behind the JIC end) + tube (circular sweep TUBEOD along line - arc RB - line) + code 61 flange head '
          '(FLG61_MEAS by flange size: thickness, face O-ring groove; head OD = O) + one through bore TUBEID; the tube starts inside '
          'the hex body at the JIC end length and ends at the flange face; braze fillets, chamfers and the head hub NOT modelled')
INPUT = ('M1@DRIVE', 'L1@DRIVE', 'CHEX@HEX', 'HEXL@HEX', 'O@DRIVE', 'D@BORE', 'TUBEOD@TUBE', 'RB@PATH')
# ---- 2026-10-21 (group D, tools/_out/groupD_20261021): additive - rows without the new columns build exactly as before ----------------
# Code 62 heads -12 ... -32 (user 2026-10-21 Q-CODE62-CAT = yes: Brennan Flange catalog table 3300-62 "TUBE BRAZE FLANGE HEAD CONNECTOR -
# CODE 62", tools/_out/brennan_catalog_20261001/catalog_verified.json table FLANGE-p008-t02): head OD = A, thickness = D, groove OD = H.
# -12 is also MEASURED on BRENNAN_1803-12-12.stp (received 2026-10-21; groupD_20261021/data/dump_1803-12-12.txt): O 1.625, TH 0.345,
# groove 0.940 / 1.250, depth 0.110 = 3300-62-12-12. The catalog prints no groove I.D. / depth: they are the code 61 groove of the same
# flange size (FLG61_MEAS) - ASSUMPTION, evidence: the measured code 62 grooves -08 (1800-08-08 / 1824-08 / 1804-08-08-FG) and -12
# (1803-12-12) equal the code 61 grooves in I.D., O.D. and depth, and the catalog groove O.D. H equals 2 x FLG61 GO at -16 / -20 / -24 / -32.
FLG62_MEAS[12] = dict(O=1.625, TH=0.345, GI=0.470, GO=0.625, GD=0.110)
FLG62_CAT = {16: dict(O=1.875, TH=0.375, GO=0.780), 20: dict(O=2.125, TH=0.405, GO=0.875), 24: dict(O=2.500, TH=0.495, GO=1.0575),
             32: dict(O=3.125, TH=0.495, GO=1.245)}
for _k, _v in FLG62_CAT.items():
    _v.update(GI=gs.FLG61_MEAS[_k]['GI'], GD=gs.FLG61_MEAS[_k]['GD'])
FLG62_HEAD = {**FLG62_CAT, **FLG62_MEAS}
FLG62_ASSUME_SZ = {12: ('SAE code 62 flange head -12: head OD / thickness / face O-ring groove measured on BRENNAN_1803-12-12.stp (= Brennan '
                        'catalog 3300-62-12-12 A 1.625 / D 0.345 / H 1.250); single manufacturer - SAE J518 / ISO 6162-2 not in the repo; '
                        'edge chamfers not modelled')}
for _k in FLG62_CAT:
    FLG62_ASSUME_SZ[_k] = (f'SAE code 62 flange head -{_k:02d}: head OD {FLG62_CAT[_k]["O"]} / thickness {FLG62_CAT[_k]["TH"]} / groove OD '
                           f'{2 * FLG62_CAT[_k]["GO"]:.3f} = Brennan Flange catalog table 3300-62 A / D / H (user Q-CODE62-CAT 2026-10-21); groove '
                           f'I.D. {2 * FLG62_CAT[_k]["GI"]:.3f} / depth {FLG62_CAT[_k]["GD"]} = the code 61 -{_k:02d} groove (FLG61_MEAS; ASSUMED: '
                           'measured code 62 grooves -08 / -12 = code 61); edge chamfers not modelled')
# Flange head braze hub (Brennan 1703 / 1704 / 1803 / 1804 CAD and STEPs: a round hub behind the head into which the tube is brazed):
# review columns HUBD@HEAD (hub dia, record DFL) and HUBL@HEAD (flange face -> hub back face, record FFL). With them the tube ends
# HUB_OVL inside the hub (PATH end E) and a construction line FACEEXT continues PATH to the flange face F, where the head sits as before.
HUB = ('HUBD@HEAD', 'HUBL@HEAD')
HUB_OVL = 0.05
HUB_ASSUME = ('flange head with its braze hub (round, dia HUBD, from the head back face to HUBL behind the flange face; Brennan CAD '
              'geometry); the tube ends 0.05 inside the hub; the head bore is the tube bore (Brennan: 7 deg flare at the face, not modelled)')


def load_review(root):
    ws = openpyxl.load_workbook(os.path.join(REV, f'DesignTable_{root}.xlsx'), data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = list(rows[1])
    return [dict(zip(hdr, r)) for r in rows[2:] if r[0]]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def geom(c, th):
    """leg / path points (inches) of one row: X0 crossing, T1 / T2 tangent points, F face centre, Fx = PATHX end, Cb bend centre"""
    u = (math.cos(math.radians(th)), math.sin(math.radians(th)))
    X0 = c['M1']
    t = c['RB'] * math.tan(math.radians(th) / 2)
    T1 = (X0 - t, 0.0)
    T2 = (X0 + t * u[0], t * u[1])
    F = (X0 + c['L1'] * u[0], c['L1'] * u[1])
    FX = (F[0] + BX * u[0], F[1] + BX * u[1])
    return dict(u=u, n=(u[1], -u[0]), X0=X0, t=t, T1=T1, T2=T2, F=F, FX=FX, Cb=(T1[0], c['RB']))


def expected_box(c, g, lib, sw=None):
    """xmax / ymax / ymin / zmax of the solid (inches), by sampling every piece's surface (sw = the swivel module for 6701)"""
    rt = c['TUBEOD'] / 2
    C = c['CHEX']
    xs, ys = [c['LJ']], [C / 2, -C / 2]
    u, n = g['u'], g['n']
    if sw is not None:                                              # swivel nut on the vertical leg: corners along X, flats in Z
        xs.append(g['X0'] + sw['Rn']); ys.append(g['F'][1])
        zmax = max(C / math.sqrt(3), sw['nut_af'] / 2, rt)
    else:
        rO, TH = c['O'] / 2, lib['TH']
        zmax = max(C / math.sqrt(3), rO, rt)
        for k in range(361):                                        # flange head: face circle and back circle
            a = math.radians(k)
            for base in (g['F'], (g['F'][0] - TH * u[0], g['F'][1] - TH * u[1])):
                p = (base[0] + rO * math.cos(a) * n[0], base[1] + rO * math.cos(a) * n[1])
                xs.append(p[0]); ys.append(p[1])
            if 'HUBD' in c:                                         # hub back circle (2026-10-21)
                base, rH = (g['F'][0] - c['HUBL'] * u[0], g['F'][1] - c['HUBL'] * u[1]), c['HUBD'] / 2
                xs.append(base[0] + rH * math.cos(a) * n[0]); ys.append(base[1] + rH * math.cos(a) * n[1])
    for k in range(91):                                             # tube along the bend (in-plane extremes of the section)
        a = math.radians(-90 + c['BEND'] * k / 90)
        for rr in (c['RB'] - rt, c['RB'] + rt):
            xs.append(g['Cb'][0] + rr * math.cos(a)); ys.append(g['Cb'][1] + rr * math.sin(a))
    for s_ in (-1, 1):                                              # straight leg 2 up to the face
        xs.append(g['F'][0] + s_ * rt * n[0]); ys.append(g['F'][1] + s_ * rt * n[1])
    return dict(xmax=max(xs), ymax=max(ys), ymin=min(ys), zmax=zmax)


def build_rows(root):
    sp = SPEC[root]
    th = sp['bend']
    built, skipped = [], []
    gate = ('VERIFIED', 'ASSUMED') + (('TEST',) if TEST else ())
    for t in sp['tables']:
        for r in load_review(t):
            pn = r['$PRP@PartNo']
            if r.get('$PRP@ScopeAction') != 'BUILD':
                skipped.append(f'{pn}: ScopeAction {r.get("$PRP@ScopeAction")}'); continue
            if r.get('$PRP@DataStatus') not in gate:
                skipped.append(f'{pn}: DataStatus {r.get("$PRP@DataStatus")}'); continue
            swv = sp.get('end2') == 'JICSW'
            inp = INPUT_SW if swv else INPUT
            miss = [k for k in inp if not num(r.get(k))]
            if miss:
                skipped.append(f'{pn}: no {" / ".join(miss)}'); continue
            a, b = (int(x) for x in pn.replace('-L-', '-').split('-')[1:3])
            code = str(r.get('$PRP@FlangeCode') or ('61' if pn.startswith('17') else '62'))
            why = []
            if a not in gs.JIC:
                why.append(f'no JIC -{a:02d} end in the library'); built.append(({'$PRP@PartNo': pn}, why)); continue
            c = {k.split('@')[0]: float(r[k]) for k in inp}
            hub = (not swv) and all(num(r.get(k)) for k in HUB)          # 2026-10-21: flange head with braze hub
            if hub:
                c['HUBD'], c['HUBL'] = float(r['HUBD@HEAD']), float(r['HUBL@HEAD'])
            S, lib = None, None
            if swv:
                try:
                    S = gs.end_JICSW(b, 'B', c['NOSETIP'], c['NUTHEX'])
                except (KeyError, AssertionError) as ex:
                    why.append(f'female JIC swivel -{b:02d}: {ex}'); built.append(({'$PRP@PartNo': pn}, why)); continue
            elif code == '62':
                if b not in FLG62_HEAD:
                    why.append(f'code 62 -{b:02d} flange head not in the library (measured -08 / -12, catalog 3300-62 -16 / -20 / -24 / -32)')
                    built.append(({'$PRP@PartNo': pn}, why)); continue
                lib = FLG62_HEAD[b]
                if abs(c['O'] - lib['O']) > 0.01:
                    why.append(f'head OD {c["O"]} differs from the {"measured" if b in FLG62_MEAS else "catalog 3300-62"} code 62 -{b:02d} head {lib["O"]} - ask before building')
            elif code != '61' or b not in gs.FLG61_MEAS:
                why.append(f'no code {code} -{b:02d} flange head in the end library (code 61 heads measured: {sorted(gs.FLG61_MEAS)})')
                built.append(({'$PRP@PartNo': pn}, why)); continue
            else:
                lib = gs.FLG61_MEAS[b]
            J = gs.end_JICM(a, 'A')
            c['BEND'] = th
            c['LJ'] = round(J['endlen'] + c['HEXL'], 6)
            c['S'] = J['endlen']
            g = geom(c, th)
            rt = c['TUBEOD'] / 2
            tipr = J['V'][0][1]
            # the tube ends at the flange face (inside the head) or, on a swivel, at the swivel body face behind the nut
            back = S['m']['BODYS'] if swv else (c['HUBL'] if hub else lib['TH'])
            if swv:      # the tube runs 0.05 into the solid swivel body (never into the seat: apex = seat cone tip on the axis)
                ov = 0.05
                g['E'] = (g['X0'] + (c['L1'] - back + ov) * g['u'][0], (c['L1'] - back + ov) * g['u'][1])
            elif hub:    # the tube runs HUB_OVL into the hub; PATH's construction line FACEEXT reaches on to the flange face F
                g['E'] = (g['X0'] + (c['L1'] - back + HUB_OVL) * g['u'][0], (c['L1'] - back + HUB_OVL) * g['u'][1])
            else:
                g['E'] = g['F']
            if g['T1'][0] < c['LJ'] + 0.02:
                why.append(f'the bend starts at x {g["T1"][0]:.4f}, inside the JIC end piece (ends at LJ {c["LJ"]:.4f}): M1 / RB / HEXL do not fit')
            if c['L1'] - back < g['t'] + 0.02:
                why.append(f'the bend reaches the {"swivel body" if swv else "flange head"} (leg 2 straight {c["L1"] - back - g["t"]:.4f})')
            if c['RB'] < rt + 0.05:
                why.append(f'bend radius {c["RB"]} too small for the {c["TUBEOD"]} tube')
            if c['TUBEOD'] > c['CHEX'] - 0.05:
                why.append(f'tube {c["TUBEOD"]} not inside the end-piece hex {c["CHEX"]}')
            if c['D'] > c['TUBEOD'] - 0.04:
                why.append(f'bore {c["D"]} leaves no tube wall ({c["TUBEOD"]} tube)')
            if c['D'] / 2 > tipr - 0.005:          # the -08 JIC tip face is 0.018 wide around a 0.39 bore on the shipped 1700-61-8-8
                why.append(f'bore {c["D"]} wider than the JIC tip face (tip dia {2 * tipr:.3f})')
            if swv:
                m = S['m']
                if rt > m['NECKR'] - 0.005:     # 2026-10-21: was 0.02 - Brennan's own 6701-08-08 has 0.019 (tube 0.549 into the 0.587 neck)
                    why.append(f'tube {c["TUBEOD"]} wider than the swivel neck (dia {2 * m["NECKR"]:.3f})')
                seat_end = S['s_nt'] + (m['SEATR'] - c['D'] / 2) / gs.TAN37
                if seat_end > m['BODYS'] - ov - 0.02:
                    why.append(f'the 37 deg seat (ends {seat_end:.4f} from the nut face) reaches the tube end ({m["BODYS"] - ov:.4f})')
                if c['D'] / 2 > m['SEATR'] - 0.01:
                    why.append(f'bore {c["D"]} wider than the swivel seat mouth (dia {2 * m["SEATR"]:.3f})')
            else:
                rO = c['O'] / 2
                if hub:
                    rH = c['HUBD'] / 2
                    if c['HUBL'] < lib['TH'] + 0.02:
                        why.append(f'hub length {c["HUBL"]} (face -> hub back) not behind the {lib["TH"]} head')
                    if rH > rO - 0.02:
                        why.append(f'hub dia {c["HUBD"]} not inside the head OD {c["O"]}')
                    if rH < rt + 0.005:
                        why.append(f'tube {c["TUBEOD"]} does not fit into the hub (dia {c["HUBD"]})')
                elif rt > lib['GI'] - 0.02:
                    why.append(f'tube {c["TUBEOD"]} wider than the -{b:02d} flange O-ring groove (inner dia {2 * lib["GI"]:.3f}): the tube cannot meet this head as modelled')
                if not (lib['GO'] < rO - 0.03 and lib['GI'] < lib['GO'] - 0.05):
                    why.append(f'O-ring groove does not fit the head (O {c["O"]})')
            cols = {'LJ@DRIVE': c['LJ'], 'BODYR@DRIVE': round(c['CHEX'] / math.sqrt(3), 6)}
            for k_, v_ in J['cols'].items():
                cols[k_] = round(v_, 6) if isinstance(v_, float) else v_
            cols.update({'HEXB@HEX': c['CHEX'], 'START@HEXCUT': round(J['endlen'], 6), 'DEPTH@HEXCUT': c['HEXL'],
                         'TUBESTART@PATH': round(c['S'], 6), 'T1X@PATH': round(g['T1'][0], 6), 'RB@PATH': c['RB'],
                         'FX@PATH': round(g['E'][0], 6), 'FY@PATH': round(g['E'][1], 6), 'TUBEOD@TUBE': c['TUBEOD']})
            if swv:
                for k_, v_ in S['cols'].items():                       # SWB_* of the straights' swivel module, on the SWSK sketch
                    if k_.endswith('@DRIVE'):
                        cols[k_.replace('@DRIVE', '@SWSK')] = round(v_, 6) if isinstance(v_, float) else v_
                cols.update({'SWB_SEATENDR@SWSK': round(c['D'] / 2, 6), 'SWB_TUBEOVL@SWSK': ov,
                             'OFFSET@NUTPLN': c['L1'], 'NUTCX@NUTHEXSK': round(g['X0'], 6), 'NUTHEX@NUTHEXSK': c['NUTHEX'],
                             'DEPTH@NUTCUT': S['m']['HEXL']})
                # nut thread (HelixThreadY): the straights' swivel thread (end_JICSW thread: r = basic minor, height TE, pitch,
                # thdh 0.54127 P) about the leg-2 axis x = X0; the profile sits at the helix start (X0 + r, nut face) in the Front Plane
                t_ = S['thread']
                assert th == 90.0, 'the swivel nut plane NUTPLN (Top Plane offset) and HelixThreadY assume a vertical leg 2'
                cols.update({'HELIXCX@HELIXSK_B': round(g['X0'], 6), 'HELIXDIA@HELIXSK_B': round(2 * t_['r'], 5),
                             'HEIGHT@HELIX_B': t_['height'], 'PITCH@HELIX_B': round(t_['pitch'], 5),
                             'PROF_AX@THDPROF_B': round(g['F'][1], 6), 'PROF_R@THDPROF_B': round(g['X0'] + t_['r'], 6),
                             'APEXR@THDPROF_B': round(g['X0'] + t_['r'] + t_['thdh'], 6)})
            else:
                cols.update({'FLGB_GRVIR@HEADSK': lib['GI'], 'FLGB_GRVOR@HEADSK': lib['GO'], 'FLGB_GRVD@HEADSK': lib['GD'],
                             'FLGB_HEADR@HEADSK': round(c['O'] / 2, 6), 'FLGB_HEADT@HEADSK': lib['TH']})
                if hub:
                    cols.update({'FLGB_HUBR@HEADSK': round(c['HUBD'] / 2, 6), 'FLGB_HUBL@HEADSK': c['HUBL'],
                                 'FACEEXT@PATH': round(c['HUBL'] - HUB_OVL, 6)})
            cols.update({'BSTART@PATHX': BX, 'BT1X@PATHX': round(g['T1'][0], 6), 'BRB@PATHX': c['RB'],
                         'BFX@PATHX': round(g['FX'][0], 6), 'BFY@PATHX': round(g['FX'][1], 6), 'TUBEID@BORE': c['D']})
            thr = J['thr']
            cols.update({'$PRP@PartNo': pn,
                         '$PRP@Description': (f'{th:g} deg Bent-Tube Swivel Elbow, male JIC -{a:02d} x female JIC swivel -{b:02d}' if swv else
                                              f'{th:g} deg Bent-Tube Flange Elbow, male JIC -{a:02d} x code {code} flange -{b:02d}'),
                         '$PRP@GeometryRoot': root,
                         '$PRP@EndA_Thread': f'{thr} (male JIC 37 deg)',
                         '$PRP@EndB_Thread': (S['thr'] if swv else f'SAE code {code} flange head -{b:02d} (O {c["O"]:g})'),
                         '$PRP@M1': f'{c["M1"]:.3f}', '$PRP@L1': f'{c["L1"]:.3f}', '$PRP@BendRadius': f'{c["RB"]:.3f}',
                         '$PRP@TubeOD': f'{c["TUBEOD"]:.3f}',
                         '$PRP@DataStatus': r['$PRP@DataStatus'],
                         '$PRP@AxialSource': (f'{r["$PRP@AxialSource"]} | MODEL: {ASSUME.replace(" + code 61 flange head", " + female JIC swivel end")}; {SW_ASSUME}' if swv else
                                              f'{r["$PRP@AxialSource"]} | MODEL: {(ASSUME.replace("code 61 flange head (FLG61_MEAS", "code 62 flange head (FLG62_MEAS") if code == "62" else ASSUME).replace("ends at the flange face; braze fillets, chamfers and the head hub NOT", "ends in the hub; braze fillets and chamfers NOT") if hub else (ASSUME.replace("code 61 flange head (FLG61_MEAS", "code 62 flange head (FLG62_MEAS") if code == "62" else ASSUME)}; '
                                              f'{(FLG62_ASSUME_SZ.get(b, FLG62_ASSUME)) if code == "62" else gs.FLG61_ASSUME.split("; body =")[0]}'
                                              + (f'; {HUB_ASSUME}' if hub else '')),
                         '$COMMENT': r.get('$COMMENT'), '$PRP@OMiSKU': r.get('$PRP@OMiSKU')})
            built.append((cols, why, dict(c=c, g=g, J=J, lib=lib, S=S, ov=(ov if swv else None), box=expected_box(c, g, lib, S))))
    return built, skipped


def write_sw2(root, built):
    sp = SPEC[root]
    ok = [b for b in built if not b[1]]
    ref = [b for b in ok if b[0]['$PRP@PartNo'] == sp['ref']] or ok
    refrow = ref[0]
    ok.sort(key=lambda b: (b[0]['$PRP@PartNo'] != refrow[0]['$PRP@PartNo'], b[0]['$PRP@PartNo']))
    hdr = list(refrow[0].keys())
    for b in ok:
        assert list(b[0].keys()) == hdr, b[0]['$PRP@PartNo']
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sheet1'
    ws.append([None] + hdr)
    for b in ok:
        ws.append([b[0]['$PRP@PartNo']] + [b[0][k] for k in hdr])
    p = os.path.join(OUT, f'DesignTable_{root}_SW2.xlsx')
    wb.save(p)
    return p, hdr, ok, refrow


def end1_profile(c, J):
    """END1 vertex chain (inches): tip on the axis, JIC chain, body at BODYR to LJ, rear face down to the axis"""
    rB = c['CHEX'] / math.sqrt(3)
    V = [(0.0, 0.0)] + list(J['V']) + [(J['endlen'], rB), (c['LJ'], rB), (c['LJ'], 0.0)]
    return V, rB


def poly_volume(V):
    v = 0.0
    for i in range(len(V)):
        (x1, r1), (x2, r2) = V[i], V[(i + 1) % len(V)]
        a, b = r1 * IN, r2 * IN
        v += math.pi * (x2 - x1) * IN * (a * a + a * b + b * b) / 3
    return abs(v)


def vba_path(name, vals, T1, Cb, T2, E, S, ty, ext=None):
    """PATH / PATHX sketch: construction line origin -> S, line S -> T1 (X axis), tangent arc (centre Cb) -> T2, tangent line -> E.
    vals = (start name, T1X name, RB name, end-x name, end-y name). Fully defined: 17 unknowns, 17 constraints.
    ext = (F, length) (2026-10-21, hub heads): + construction line pe E -> F parallel to the last line, length FACEEXT (21 / 21)."""
    nS, nT, nR, nX, nY = vals
    q = lambda v: f'{v * IN:.9f}'
    X = ''
    if ext is not None:
        Fp, el = ext
        X = f'''    ' face extension (hub heads): construction line from the tube end E to the flange face centre F, parallel to leg 2
    swSkMgr.AddToDB = True
    Set pe = swSkMgr.CreateLine({q(E[0])}, {q(E[1])}, 0, {q(Fp[0])}, {q(Fp[1])}, 0)
    swSkMgr.AddToDB = False
    Check "{name}: face extension line created", Not pe Is Nothing
    pe.ConstructionGeometry = True
    PathExtension p2, pe, "FACEEXT", {q(el)}, {q(ty)}
'''
    return f'''    ' ================= {name}: tube centre line {'(boss)' if name == 'PATH' else '(bore, 0.05 past both ends)'} =================
    stepName = "{name} sketch"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Set pc = swSkMgr.CreateLine(0, 0, 0, {q(S)}, 0, 0)
    pc.ConstructionGeometry = True
    Set p1 = swSkMgr.CreateLine({q(S)}, 0, 0, {q(T1[0])}, 0, 0)
    Set pa = swSkMgr.CreateArc({q(Cb[0])}, {q(Cb[1])}, 0, {q(T1[0])}, 0, 0, {q(T2[0])}, {q(T2[1])}, 0, 1)
    Set p2 = swSkMgr.CreateLine({q(T2[0])}, {q(T2[1])}, 0, {q(E[0])}, {q(E[1])}, 0)
    swSkMgr.AddToDB = False
    Check "{name}: construction line, two lines and the bend arc created", (Not pc Is Nothing) And (Not p1 Is Nothing) And (Not pa Is Nothing) And (Not p2 Is Nothing)
    PathRelations pc, p1, pa, p2
    PathDims pc, p1, pa, p2, "{nS}", {q(abs(S))}, "{nT}", {q(T1[0])}, "{nR}", {q(Cb[1])}, "{nX}", {q(E[0])}, "{nY}", {q(E[1])}, {q(ty)}
{X}    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "{name}"
    Check "{name} sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
'''


PATH_SUBS = '''Sub PathRelations(pc As SldWorks.SketchSegment, p1 As SldWorks.SketchSegment, pa As SldWorks.SketchSegment, p2 As SldWorks.SketchSegment)
    ' construction line from the origin, horizontal; chain construction end = line 1 start, line 1 end = arc start, arc end =
    ' line 2 start; line 1 horizontal; arc tangent to both lines
    Dim lc As SldWorks.SketchLine, l1 As SldWorks.SketchLine, l2 As SldWorks.SketchLine, ar As SldWorks.SketchArc
    Set lc = pc: Set l1 = p1: Set l2 = p2: Set ar = pa
    swModel.ClearSelection2 True
    lc.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    pc.Select4 False, Nothing
    swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True
    lc.GetEndPoint2.Select4 False, Nothing
    l1.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True
    l1.GetEndPoint2.Select4 False, Nothing
    ar.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True
    ar.GetEndPoint2.Select4 False, Nothing
    l2.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True
    p1.Select4 False, Nothing
    swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True
    p1.Select4 False, Nothing
    pa.Select4 True, Nothing
    swModel.SketchAddConstraints "sgTANGENT"
    swModel.ClearSelection2 True
    pa.Select4 False, Nothing
    p2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgTANGENT"
    swModel.ClearSelection2 True
End Sub

Sub PathDims(pc As SldWorks.SketchSegment, p1 As SldWorks.SketchSegment, pa As SldWorks.SketchSegment, p2 As SldWorks.SketchSegment, nS As String, vS As Double, nT As String, vT As Double, nR As String, vR As Double, nX As String, vX As Double, nY As String, vY As Double, ty As Double)
    ' start = construction line length; T1X = origin to the bend start (horizontal); RB = arc radius; end point x / y from the origin
    Dim dd As SldWorks.DisplayDimension, l1 As SldWorks.SketchLine, l2 As SldWorks.SketchLine
    Set l1 = p1: Set l2 = p2
    swModel.ClearSelection2 True
    pc.Select4 False, Nothing
    Set dd = swModel.AddDimension2(0, -ty, 0)
    NameDim dd, nS, vS
    swModel.ClearSelection2 True
    l1.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddHorizontalDimension2(vT / 2, -2 * ty, 0)
    NameDim dd, nT, vT
    swModel.ClearSelection2 True
    pa.Select4 False, Nothing
    Set dd = swModel.AddDimension2(vT - vR, vR * 1.5, 0)
    NameDim dd, nR, vR
    swModel.ClearSelection2 True
    l2.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddHorizontalDimension2(vX / 2, vY + ty, 0)
    NameDim dd, nX, vX
    swModel.ClearSelection2 True
    l2.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2(vX + ty, vY / 2, 0)
    NameDim dd, nY, vY
    swModel.ClearSelection2 True
End Sub

Function CircularSweep(pathName As String, diaM As Double, isCut As Boolean, featName As String, dimName As String) As SldWorks.Feature
    ' sweep / swept cut with a circular profile along a path sketch: the path is selected with mark 4 (2026-10-15 prototype:
    ' setting the definition's Path property creates nothing); the profile diameter is a dimension of the feature (renamed)
    Dim sd As Object, f As SldWorks.Feature, d As SldWorks.DisplayDimension, dm As SldWorks.Dimension
    swModel.ClearSelection2 True
    Check featName & ": path " & pathName & " selected", swModel.Extension.SelectByID2(pathName, "SKETCH", 0, 0, 0, False, 4, Nothing, 0)
    Set sd = swFeatMgr.CreateDefinition(IIf(isCut, swFeatureNameID_e.swFmSweepCut, swFeatureNameID_e.swFmSweep))
    sd.CircularProfile = True
    sd.CircularProfileDiameter = diaM
    Set f = swFeatMgr.CreateFeature(sd)
    swModel.ClearSelection2 True
    Check featName & " created (circular " & IIf(isCut, "swept cut", "sweep") & " " & Format(diaM / IN_, "0.0000") & " along " & pathName & ")", Not f Is Nothing
    If f Is Nothing Then Exit Function
    f.Name = featName
    Set d = f.GetFirstDisplayDimension
    If Not d Is Nothing Then
        Set dm = d.GetDimension2(0)
        dm.Name = dimName
        Check dimName & "@" & featName & " = " & Format(dm.SystemValue / IN_, "0.0000") & " (expect " & Format(diaM / IN_, "0.0000") & ")", Abs(dm.SystemValue - diaM) < 0.000005
    Else
        Check featName & ": profile diameter dimension found", False
    End If
    Set CircularSweep = f
End Function
'''


def vba_head(g, lib, rO, hub=None):
    """HEADSK: closed half-section of the flange head in leg-2 coordinates (a from the face toward the bend, r from the axis):
    A0 face centre = PATH end point F (external), A1 (0, GI), A2 (GD, GI), A3 (GD, GO), A4 (0, GO), A5 (0, rO), A6 (TH, rO),
    A7 (TH, 0); centreline A7 -> A0. 16 unknowns: A0 on F (2), axis parallel to PATH's last line (1), 3 perpendicular + 4 parallel
    + face collinear (2) + 5 distances.
    hub = (rH, HL) (2026-10-21): A6 (TH, rO), A7 (TH, rH), A8 (HL, rH), A9 (HL, 0); centreline A9 -> A0; + hub OD parallel, hub back
    perpendicular, FLGB_HUBR, FLGB_HUBL = 20 / 20. The face centre then sits on the end of PATH's face extension pe (not p2)."""
    F, u, n = g['F'], g['u'], g['n']
    A = lambda a, r: (F[0] - a * u[0] + r * n[0], F[1] - a * u[1] + r * n[1])
    pts = [A(0, 0), A(0, lib['GI']), A(lib['GD'], lib['GI']), A(lib['GD'], lib['GO']), A(0, lib['GO']), A(0, rO), A(lib['TH'], rO)]
    pts += [A(lib['TH'], hub[0]), A(hub[1], hub[0]), A(hub[1], 0)] if hub else [A(lib['TH'], 0)]
    N = len(pts); ax = N - 1
    q = lambda v: f'{v * IN:.9f}'
    T = lambda a, r: f'{q(A(a, r)[0])}, {q(A(a, r)[1])}'
    lines = '\n'.join(f'    Set hs({i}) = swSkMgr.CreateLine({q(pts[i][0])}, {q(pts[i][1])}, 0, {q(pts[(i + 1) % N][0])}, {q(pts[(i + 1) % N][1])}, 0)' for i in range(N))
    HX = ''
    if hub:
        HX = (f'''    ' braze hub: hub OD parallel to the axis, hub back face perpendicular; hub radius, face -> hub back
    HRel 7, {ax}, "sgPARALLEL"
    HRel 8, {ax}, "sgPERPENDICULAR"
    HDist 7, {ax}, "FLGB_HUBR", {q(hub[0])}, {T(lib['TH'] + (hub[1] - lib['TH']) / 2, hub[0] + 0.15)}
    HDist 8, 0, "FLGB_HUBL", {q(hub[1])}, {T(hub[1] / 2, -0.35)}
''')
    return f'''    ' ================= HEADSK: flange head half-section about the leg-2 axis =================
    stepName = "HEAD sketch"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
{lines}
    Set hcl = swSkMgr.CreateCenterLine({q(pts[ax][0])}, {q(pts[ax][1])}, 0, {q(pts[0][0])}, {q(pts[0][1])}, 0)
    swSkMgr.AddToDB = False
    Check "HEADSK: {'ten' if hub else 'eight'} lines and the leg-2 centre line created", (Not hs({ax}) Is Nothing) And (Not hcl Is Nothing)
    Dim hl1 As SldWorks.SketchLine, hl2 As SldWorks.SketchLine, hcc As SldWorks.SketchLine, pl2 As SldWorks.SketchLine
    For i = 0 To {N - 1}
        Set hl1 = hs(i): Set hl2 = hs((i + 1) Mod {N})
        swModel.ClearSelection2 True
        hl1.GetEndPoint2.Select4 False, Nothing
        hl2.GetStartPoint2.Select4 True, Nothing
        swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next i
    Set hcc = hcl: Set hl1 = hs({ax})
    swModel.ClearSelection2 True
    hcc.GetStartPoint2.Select4 False, Nothing
    hl1.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True
    hcc.GetEndPoint2.Select4 False, Nothing
    hl1.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    ' face centre A0 on the PATH end point F{" (the end of the face extension pe)" if hub else ""}; the axis parallel to PATH's last line (leg 2)
    Set pl2 = {"pe" if hub else "p2"}: Set hl1 = hs(0)
    swModel.ClearSelection2 True
    hl1.GetStartPoint2.Select4 False, Nothing
    pl2.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    hs({ax}).Select4 False, Nothing
    p2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgPARALLEL"
    ' face A0-A1 perpendicular to the axis, A4-A5 on the face; groove walls and rim parallel; groove bottom and back face perpendicular
    HRel 0, {ax}, "sgPERPENDICULAR"
    HRel 4, 0, "sgCOLINEAR"
    HRel 1, {ax}, "sgPARALLEL"
    HRel 3, {ax}, "sgPARALLEL"
    HRel 5, {ax}, "sgPARALLEL"
    HRel 2, {ax}, "sgPERPENDICULAR"
    HRel 6, {ax}, "sgPERPENDICULAR"
    HDist 1, {ax}, "FLGB_GRVIR", {q(lib['GI'])}, {T(lib['GD'] / 2, lib['GI'] - 0.12)}
    HDist 3, {ax}, "FLGB_GRVOR", {q(lib['GO'])}, {T(lib['GD'] / 2 + 0.25, lib['GO'] + 0.05)}
    HDist 5, {ax}, "FLGB_HEADR", {q(rO)}, {T(lib['TH'] / 2 + 0.45, rO + 0.1)}
    HDist 2, 0, "FLGB_GRVD", {q(lib['GD'])}, {T(lib['GD'] / 2, (lib['GI'] + lib['GO']) / 2 + 0.3)}
    HDist 6, 0, "FLGB_HEADT", {q(lib['TH'])}, {T(lib['TH'] / 2, rO + 0.35)}
{HX}    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "HEADSK"
    Check "HEADSK sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    stepName = "HEAD revolve"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "HEADSK", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set hsd = swSelMgr.CreateSelectData: hsd.Mark = 16
    hcl.Select4 True, hsd
    Set hrev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "HEAD revolve created (flange head about the leg-2 axis)", Not hrev Is Nothing
    If Not hrev Is Nothing Then hrev.Name = "HEAD"
'''


HUB_SUBS = '''Sub PathExtension(p2 As SldWorks.SketchSegment, pe As SldWorks.SketchSegment, nm As String, vM As Double, ty As Double)
    ' 2026-10-21 (hub heads): pe starts at the end of the last path line, parallel to it, length nm (tube end in the hub -> flange face)
    Dim l2 As SldWorks.SketchLine, le As SldWorks.SketchLine, dd As SldWorks.DisplayDimension
    Set l2 = p2: Set le = pe
    swModel.ClearSelection2 True
    l2.GetEndPoint2.Select4 False, Nothing
    le.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True
    pe.Select4 False, Nothing
    p2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgPARALLEL"
    swModel.ClearSelection2 True
    pe.Select4 False, Nothing
    Set dd = swModel.AddDimension2(le.GetEndPoint2.X + ty, le.GetEndPoint2.Y + ty, 0)
    NameDim dd, nm, vM
    swModel.ClearSelection2 True
End Sub

'''


HEAD_SUBS = '''Sub HRel(i As Long, j As Long, rel As String)
    swModel.ClearSelection2 True
    hs(i).Select4 False, Nothing
    hs(j).Select4 True, Nothing
    swModel.SketchAddConstraints rel
    swModel.ClearSelection2 True
End Sub

Sub HDist(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    ' distance between two parallel lines of the head sketch
    swModel.ClearSelection2 True
    hs(i).Select4 False, Nothing
    hs(j).Select4 True, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
    swModel.ClearSelection2 True
End Sub
'''


def vba_swivel(g, S, rb, ov):
    """SWSK: the straights' female JIC swivel end (nut + nose one solid) as a closed half-section about the vertical leg-2 axis.
    W0 seat end on the axis, W1 seat end at the bore radius rb (the 37 deg seat cone ends at the through-bore, as on the 6565
    double swivel - SEAT_TO_BORE_ASSUME: on the short bent-tube body the cone apex would fall behind the body face at -12 / -16),
    W2 seat mouth ... W9 nut-face mouth ... W16 neck, W17 body face on the axis. Anchor: the axis line collinear with PATH's last
    line, W17 at SWB_TUBEOVL (= ov) from the PATH end (the tube runs ov into the swivel body). 18 points, 36 unknowns:
    collinear (2) + overlap (1) + 7 horizontal + 6 vertical + 20 dimensions."""
    m = S['m']
    F, u, n = g['F'], g['u'], g['n']
    P = lambda a, r: (F[0] - a * u[0] + r * n[0], F[1] - a * u[1] + r * n[1])
    seat_end = S['s_nt'] + (m['SEATR'] - rb) / gs.TAN37
    Wl = [(seat_end, 0.0), (seat_end, rb), (S['s_nt'], m['SEATR']), (S['s_nt'], m['NOSER']), (m['FLOOR'], m['NOSER']),
          (m['FLOOR'], m['RELR']), (S['scb0'], m['RELR']), (m['TE'], S['rmin']), (S['cs'], S['rmin']), (0.0, S['rcs']), (0.0, S['Rn']),
          (m['HEXL'], S['Rn']), (m['HEXL'], m['SKF']), (m['SKS'], m['SKR']), (m['NUTL'], m['SKR']), (m['NUTL'], m['NECKR']),
          (m['BODYS'], m['NECKR']), (m['BODYS'], 0.0)]
    pts = [P(a, r) for a, r in Wl]
    N = len(pts)
    ax = N - 1
    q = lambda v: f'{v * IN:.9f}'
    L = ['    ' + "' ================= SWSK: female JIC swivel end (nut + nose, one solid) about the leg-2 axis =================",
         '    stepName = "SWIVEL sketch"', '    swModel.ClearSelection2 True',
         '    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0',
         '    swSkMgr.InsertSketch True', '    swSkMgr.AddToDB = True', f'    ReDim seg({N - 1})']
    for i in range(N):
        a_, b_ = pts[i], pts[(i + 1) % N]
        L.append(f'    Set seg({i}) = swSkMgr.CreateLine({q(a_[0])}, {q(a_[1])}, 0, {q(b_[0])}, {q(b_[1])}, 0)')
    L += [f'    Set axisCL = swSkMgr.CreateCenterLine({q(pts[N - 1][0])}, {q(pts[N - 1][1])}, 0, {q(pts[0][0])}, {q(pts[0][1])}, 0)',
          '    swSkMgr.AddToDB = False',
          f'    Check "SWSK: {N} lines and the leg-2 centre line created", (Not seg({N - 1}) Is Nothing) And (Not axisCL Is Nothing)',
          '    Dim sl1 As SldWorks.SketchLine, sl2 As SldWorks.SketchLine, scl As SldWorks.SketchLine, spl As SldWorks.SketchLine',
          '    Dim dsw As SldWorks.DisplayDimension',
          f'    For i = 0 To {N - 1}',
          f'        Set sl1 = seg(i): Set sl2 = seg((i + 1) Mod {N})',
          '        swModel.ClearSelection2 True', '        sl1.GetEndPoint2.Select4 False, Nothing', '        sl2.GetStartPoint2.Select4 True, Nothing',
          '        swModel.SketchAddConstraints "sgMERGEPOINTS"', '    Next i',
          f'    Set scl = axisCL: Set sl1 = seg({ax})',
          '    swModel.ClearSelection2 True', '    scl.GetStartPoint2.Select4 False, Nothing', '    sl1.GetStartPoint2.Select4 True, Nothing',
          '    swModel.SketchAddConstraints "sgMERGEPOINTS"',
          '    swModel.ClearSelection2 True', '    scl.GetEndPoint2.Select4 False, Nothing', '    sl1.GetEndPoint2.Select4 True, Nothing',
          '    swModel.SketchAddConstraints "sgMERGEPOINTS"',
          "    ' the swivel axis on the tube centre line (collinear with PATH's last line), the body face SWB_TUBEOVL past the tube end",
          f'    swModel.ClearSelection2 True: seg({ax}).Select4 False, Nothing: p2.Select4 True, Nothing: swModel.SketchAddConstraints "sgCOLINEAR"',
          f'    Set spl = p2: Set sl1 = seg({ax})',
          '    swModel.ClearSelection2 True', '    sl1.GetStartPoint2.Select4 False, Nothing', '    spl.GetEndPoint2.Select4 True, Nothing',
          f'    Set dsw = swModel.AddVerticalDimension2({q(pts[ax][0] - 0.35)}, {q(pts[ax][1] - ov / 2)}, 0)',
          f'    NameDim dsw, "SWB_TUBEOVL", {q(ov)}']
    for i in range(N - 1):                      # the axis line gets its direction from the collinear relation
        a_, b_ = pts[i], pts[(i + 1) % N]
        if abs(a_[1] - b_[1]) < 1e-9:
            L.append(f'    swModel.ClearSelection2 True: seg({i}).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"')
        elif abs(a_[0] - b_[0]) < 1e-9:
            L.append(f'    swModel.ClearSelection2 True: seg({i}).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"')
    mid = lambda k: ((pts[k][0] + pts[(k + 1) % N][0]) / 2, (pts[k][1] + pts[(k + 1) % N][1]) / 2)
    side = S['Rn'] + 0.35

    def at(k, dx=0.0, dy=0.0):
        mx, my = mid(k)
        return f'{q(mx + dx)}, {q(my + dy)}'
    L += [f'    Call Dim_pair(2, 9, "SWB_NOSETIP", {q(S["s_nt"])}, {at(2, side, 0)})',
          f'    Call Dim_ptline(1, False, {ax}, "SWB_SEATENDR", {q(rb)}, {at(0, 0.05, -0.08)})',
          f'    Call Dim_ptline(1, True, {ax}, "SWB_SEATR", {q(m["SEATR"])}, {at(1, 0.1, 0.05)})',
          f'    Call Dim_ang(1, {ax}, "SWB_SEATANG", {math.radians(37):.9f}, {at(1, 0.05, -0.1)})',
          f'    Call Dim_rad(3, "SWB_NOSER", {q(m["NOSER"])}, {at(3, 0.1, 0)})',
          f'    Call Dim_pair(4, 9, "SWB_FLOOR", {q(m["FLOOR"])}, {at(4, side + 0.2, 0)})',
          f'    Call Dim_rad(5, "SWB_RELR", {q(m["RELR"])}, {at(5, 0.15, 0)})',
          f'    Call Dim_ang(6, {ax}, "SWB_RELANG", {math.radians(45):.9f}, {at(6, 0.05, 0.05)})',
          f'    Call Dim_rad(7, "SWB_MINR", {q(S["rmin"])}, {at(7, 0.2, 0)})',
          f'    Call Dim_len(7, "SWB_THDL", {q(m["TE"] - S["cs"])}, {at(7, -0.15, 0)})',
          f'    Call Dim_ang(8, {ax}, "SWB_CSANG", {math.radians(50):.9f}, {at(8, 0.05, 0.08)})',
          f'    Call Dim_ptline(8, True, {ax}, "SWB_CSR", {q(S["rcs"])}, {at(8, 0, 0.25)})',
          f'    Call Dim_rad(10, "SWB_NUTR", {q(S["Rn"])}, {at(10, 0.3, 0)})',
          f'    Call Dim_len(10, "SWB_NUTHEXL", {q(m["HEXL"])}, {at(10, side, 0)})',
          f'    Call Dim_ptline(11, True, {ax}, "SWB_SKIRTFR", {q(m["SKF"])}, {at(11, 0.2, -0.05)})',
          f'    Call Dim_rad(13, "SWB_SKIRTR", {q(m["SKR"])}, {at(13, 0.3, 0)})',
          f'    Call Dim_len(13, "SWB_SKIRTL", {q(m["NUTL"] - m["SKS"])}, {at(13, side, 0)})',
          f'    Call Dim_pair(14, 9, "SWB_NUTL", {q(m["NUTL"])}, {at(14, side + 0.4, 0)})',
          f'    Call Dim_rad(15, "SWB_NECKR", {q(m["NECKR"])}, {at(15, 0.35, 0)})',
          f'    Call Dim_pair(16, 9, "SWB_BODYS", {q(m["BODYS"])}, {at(16, side + 0.6, 0)})']
    L += ['    swModel.ClearSelection2 True', '    swSkMgr.InsertSketch True', '    Set swFeat = swModel.FeatureByPositionReverse(0)',
          '    swFeat.Name = "SWSK"',
          '    Check "SWSK sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)',
          '    stepName = "SWIVEL revolve"', '    swModel.ClearSelection2 True',
          '    swModel.Extension.SelectByID2 "SWSK", "SKETCH", 0, 0, 0, False, 0, Nothing, 0',
          '    Set hsd = swSelMgr.CreateSelectData: hsd.Mark = 16', '    axisCL.Select4 True, hsd',
          '    Set hrev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)',
          '    Check "SWIVEL revolve created (female JIC swivel end about the leg-2 axis)", Not hrev Is Nothing',
          '    If Not hrev Is Nothing Then hrev.Name = "SWIVEL"',
          '    stepName = "Swivel nut hex"',
          f'    Set hexcut = NutHexCutY({q(g["X0"])}, {q(F[1])}, {q(S["nut_af"])}, {q(m["HEXL"])})', '']
    return '\n'.join(L), seat_end


SW_SUBS = '''Function NutHexCutY(cxM As Double, yFaceM As Double, afM As Double, depthM As Double) As SldWorks.Feature
    ' swivel nut hex on the vertical leg 2 (6701): reference plane NUTPLN at the nut face (Top Plane + OFFSET), hexagon centred on
    ' the leg-2 axis (construction line from the projected origin, length NUTCX), cut OUTSIDE it over depthM into the part (-Y);
    ' the direction is tried both ways and kept where the cut removes material only in the nut zone
    On Error Resume Next
    Dim pl As SldWorks.Feature, ok As Boolean, d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, flip As Long
    Dim mu As SldWorks.MathUtility, xf As SldWorks.MathTransform, mp As SldWorks.MathPoint, rp As Object, td As Variant
    Set mu = swApp.GetMathUtility
    For flip = 0 To 1
        swModel.ClearSelection2 True
        ok = swModel.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
        Set pl = swFeatMgr.InsertRefPlane(swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_Distance + IIf(flip = 1, swRefPlaneReferenceConstraints_e.swRefPlaneReferenceConstraint_OptionFlip, 0), yFaceM, 0, 0, 0, 0)
        If pl Is Nothing Then Exit For
        ' where did it go? the plane's own transform carries its origin (translation = ArrayData 9..11)
        Set rp = pl.GetSpecificFeature2
        td = rp.Transform.ArrayData
        Trace "NUTPLN try " & flip & ": plane origin y = " & Format(td(10) / IN_, "0.0000") & " (want " & Format(yFaceM / IN_, "0.0000") & ")"
        If Abs(td(10) - yFaceM) < 0.000005 Then Exit For
        swModel.ClearSelection2 True
        pl.Select2 False, 0
        swModel.Extension.DeleteSelection2 0
        Set pl = Nothing
    Next flip
    Check "NUTPLN at the nut face (Top Plane offset " & Format(yFaceM / IN_, "0.0000") & ")", Not pl Is Nothing
    If pl Is Nothing Then Exit Function
    pl.Name = "NUTPLN"
    Set d = pl.GetFirstDisplayDimension
    If Not d Is Nothing Then
        Set dm = d.GetDimension2(0): dm.Name = "OFFSET"
        Check "OFFSET@NUTPLN = " & Format(dm.SystemValue / IN_, "0.0000"), Abs(dm.SystemValue - yFaceM) < 0.000005
    End If
    swModel.ClearSelection2 True
    pl.Select2 False, 0
    swSkMgr.InsertSketch True
    Set xf = swSkMgr.ActiveSketch.ModelToSketchTransform
    Dim pa(2) As Double, ps As Variant
    pa(0) = cxM: pa(1) = yFaceM: pa(2) = 0
    Set mp = mu.CreatePoint(pa): Set mp = mp.MultiplyTransform(xf): ps = mp.ArrayData
    swSkMgr.AddToDB = True
    Dim cl As SldWorks.SketchSegment, poly As Variant, k As Long, circ As SldWorks.SketchSegment
    Set cl = swSkMgr.CreateLine(0, 0, 0, ps(0), ps(1), 0)
    cl.ConstructionGeometry = True
    poly = swSkMgr.CreatePolygon(ps(0), ps(1), 0, ps(0) + afM / 2, ps(1), 0, 6, True)
    swSkMgr.AddToDB = False
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
    Next k
    Dim lc As SldWorks.SketchLine, ac As SldWorks.SketchArc
    Set lc = cl: Set ac = circ
    swModel.ClearSelection2 True
    lc.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True
    lc.GetEndPoint2.Select4 False, Nothing
    ac.GetCenterPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    Set d = swModel.AddDimension2(ps(0) / 2, ps(1) - 0.3 * IN_, 0)
    NameDim d, "NUTCX", Abs(ps(0))
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Set d = swModel.AddDimension2(ps(0) + afM * 0.7, ps(1) + afM * 0.7, 0)
    If Not d Is Nothing Then d.GetDimension2(0).SystemValue = afM
    NameDim d, "NUTHEX", afM
    swModel.ClearSelection2 True
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL": Exit For
    Next k
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim skF As SldWorks.Feature
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = "NUTHEXSK"
    Check "NUTHEXSK sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long, lo As Double, hi As Double
    v0 = Volume()
    For attempt = 0 To 1
        Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, True, (attempt = 1), 0, False, "NUTCUT attempt " & attempt)
        If Not cut Is Nothing Then
            v1 = Volume()
            FeatSpanY cut, lo, hi
            Trace "NUTCUT attempt " & attempt & ": removed " & Format((v0 - v1) / IN_ ^ 3, "0.00000") & " in^3, new faces y " & Format(lo / IN_, "0.0000") & ".." & Format(hi / IN_, "0.0000") & " (zone " & Format((yFaceM - depthM) / IN_, "0.0000") & ".." & Format(yFaceM / IN_, "0.0000") & ")"
            If v1 < v0 - 1E-12 And lo > yFaceM - depthM - 0.0005 And hi < yFaceM + 0.0005 And hi > lo Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next attempt
    Check "NUTCUT created in the nut zone and removed material", Not cut Is Nothing
    If cut Is Nothing Then Exit Function
    cut.Name = "NUTCUT"
    Set d = cut.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then dm.Name = "DEPTH"
        Set d = cut.GetNextDisplayDimension(d)
    Loop
    Check "DEPTH@NUTCUT reachable", Not swModel.Parameter("DEPTH@NUTCUT") Is Nothing
    ' the plane stays in the tree (it carries the nut hex sketch) but is hidden in the saved part
    swModel.ClearSelection2 True
    pl.Select2 False, 0
    swModel.BlankRefGeom
    swModel.ClearSelection2 True
    Set NutHexCutY = cut
End Function

Sub FeatSpanY(f As SldWorks.Feature, lo As Double, hi As Double)
    ' y-range of the faces a feature created
    On Error Resume Next
    Dim faces As Variant, i As Long, bx As Variant
    lo = 1E+30: hi = -1E+30
    faces = f.GetFaces
    If IsEmpty(faces) Then lo = 0: hi = 0: Exit Sub
    For i = LBound(faces) To UBound(faces)
        bx = faces(i).GetBox
        If bx(1) < lo Then lo = bx(1)
        If bx(4) > hi Then hi = bx(4)
    Next i
End Sub

Sub HelixThreadY(cxM As Double, yFaceM As Double, rM As Double, heightM As Double, pitchM As Double, thdhM As Double, nm As String)
    ' female thread in the swivel nut on the vertical leg 2 (6701) = the straights' HelixThread (helix + 60 deg profile + swept cut)
    ' for an axis parallel to Y through x = cxM: helix sketch on NUTPLN (circle HELIXDIA, centre on a construction line HELIXCX from
    ' the projected origin), helix HEIGHT / PITCH into the part, right hand, start in the Front Plane at x = cx + r; profile THDPROF_B
    ' on the Front Plane at the helix start (base on the thread minor, apex outward, 60 deg); swept cut, suppressed.
    ' SolidWorks' own Thread feature (Inch Tap) on the nut's minor edge crashed SolidWorks 2026 SP4 (2026-10-15) - not used here.
    On Error Resume Next
    Dim ok As Boolean, sk As SldWorks.Feature, hx As SldWorks.Feature, pf As SldWorks.Feature, f As SldWorks.Feature
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension
    Dim mu As SldWorks.MathUtility, xf As SldWorks.MathTransform, mp As SldWorks.MathPoint, ps As Variant
    Set mu = swApp.GetMathUtility
    ' --- helix sketch on the nut-face plane
    swModel.ClearSelection2 True
    ok = swModel.Extension.SelectByID2("NUTPLN", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    Check nm & ": NUTPLN selected for the helix sketch", ok
    If ok = False Then Exit Sub
    swSkMgr.InsertSketch True
    Set xf = swSkMgr.ActiveSketch.ModelToSketchTransform
    Dim pa(2) As Double
    pa(0) = cxM: pa(1) = yFaceM: pa(2) = 0
    Set mp = mu.CreatePoint(pa): Set mp = mp.MultiplyTransform(xf): ps = mp.ArrayData
    swSkMgr.AddToDB = True
    Dim cl As SldWorks.SketchSegment, cc As SldWorks.SketchSegment
    Set cl = swSkMgr.CreateLine(0, 0, 0, ps(0), ps(1), 0)
    cl.ConstructionGeometry = True
    Set cc = swSkMgr.CreateCircleByRadius(ps(0), ps(1), 0, rM)
    swSkMgr.AddToDB = False
    Dim lc As SldWorks.SketchLine, ac As SldWorks.SketchArc
    Set lc = cl: Set ac = cc
    swModel.ClearSelection2 True
    lc.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True: cl.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True
    lc.GetEndPoint2.Select4 False, Nothing: ac.GetCenterPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True: cl.Select4 False, Nothing
    Set d = swModel.AddDimension2(ps(0) / 2, ps(1) - 0.3 * IN_, 0)
    NameDim d, "HELIXCX", Abs(ps(0))
    swModel.ClearSelection2 True: cc.Select4 False, Nothing
    Set d = swModel.AddDimension2(ps(0) + 1.5 * rM, ps(1) + 1.5 * rM, 0)
    If Not d Is Nothing Then d.GetDimension2(0).SystemValue = 2 * rM
    NameDim d, "HELIXDIA", 2 * rM
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set sk = swModel.FeatureByPositionReverse(0): sk.Name = "HELIXSK_B"
    Check nm & ": HELIXSK_B fully defined", (sk.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' --- helix: into the part (-Y), right hand, start in the Front Plane at x = cx + r. Start angle 90 deg first (a 0 deg helix
    ' starts on +Z here, 2026-10-15), then the other quarters and the other direction / hand; the hand is read from the curve:
    ' at the face end, (r x t) . (0, -1, 0) = rx * tz - rz * tx > 0 = right hand (t = tangent from the face into the part)
    Dim mdLate As Object: Set mdLate = swModel
    Dim k As Long, rv As Boolean, cw As Boolean, ang As Double, egv As Object, cv As Object, cpd As Object, e0 As Variant, e1 As Variant
    Dim fp(2) As Double, fd(2) As Double, oy As Double, hand As Double, good As Boolean
    good = False
    For k = 0 To 15
        Select Case Int(k / 4)
            Case 0: rv = True: cw = True
            Case 1: rv = False: cw = False
            Case 2: rv = True: cw = False
            Case Else: rv = False: cw = True
        End Select
        ang = ((k + 1) Mod 4) * 1.5707963267949
        swModel.ClearSelection2 True
        sk.Select2 False, 0
        Err.Clear
        mdLate.InsertHelix rv, cw, False, False, swHelixDefinedBy_e.swHelixDefinedByHeightAndPitch, heightM, pitchM, 0#, 0#, ang
        Set hx = swModel.FeatureByPositionReverse(0)
        If Not hx Is Nothing Then
            If hx.GetTypeName2 <> "Helix" Then Set hx = Nothing
        End If
        Set egv = Nothing
        If Not hx Is Nothing Then Set egv = hx.GetSpecificFeature2.GetFirstSegment
        If Not egv Is Nothing Then
            Set cv = egv.GetCurve
            Set cpd = egv.GetCurveParams3
            e0 = cv.Evaluate2(cpd.UMinValue, 1): e1 = cv.Evaluate2(cpd.UMaxValue, 1)
            If Abs(e0(1) - yFaceM) < Abs(e1(1) - yFaceM) Then
                fp(0) = e0(0): fp(1) = e0(1): fp(2) = e0(2): fd(0) = e0(3): fd(1) = e0(4): fd(2) = e0(5): oy = e1(1)
            Else
                fp(0) = e1(0): fp(1) = e1(1): fp(2) = e1(2): fd(0) = -e1(3): fd(1) = -e1(4): fd(2) = -e1(5): oy = e0(1)
            End If
            hand = (fp(0) - cxM) * fd(2) - fp(2) * fd(0)
            good = Abs(fp(0) - (cxM + rM)) < 0.00001 And Abs(fp(1) - yFaceM) < 0.00001 And Abs(fp(2)) < 0.00001 And Abs(oy - (yFaceM - heightM)) < 0.00001 And hand > 0
            Trace nm & ": helix try " & k & " (reversed " & rv & ", clockwise " & cw & ", start " & Format(ang * 57.2957795130823, "0") & " deg): face end (" & Format(fp(0) / IN_, "0.0000") & ", " & Format(fp(1) / IN_, "0.0000") & ", " & Format(fp(2) / IN_, "0.0000") & "), other end y " & Format(oy / IN_, "0.0000") & ", " & IIf(hand > 0, "right", "left") & " hand"
        Else
            Trace nm & ": helix try " & k & " made no helix curve" & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "")
        End If
        Err.Clear
        If good Then Exit For
        If Not hx Is Nothing Then
            swModel.ClearSelection2 True: hx.Select2 False, 0: swModel.Extension.DeleteSelection2 0
        End If
        Set hx = Nothing
    Next k
    Check nm & ": helix into the part, right hand, starting in the Front Plane at x = " & Format((cxM + rM) / IN_, "0.0000") & ", y = " & Format(yFaceM / IN_, "0.0000"), good
    If good = False Then Exit Sub
    hx.Name = "HELIX_B"
    Dim names As String
    Set d = hx.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - heightM) < 0.000001 Then dm.Name = "HEIGHT"
        If Abs(dm.SystemValue - pitchM) < 0.000001 Then dm.Name = "PITCH"
        names = names & dm.Name & " "
        Set d = hx.GetNextDisplayDimension(d)
    Loop
    Check nm & " helix dims named (" & names & ")", InStr(names, "HEIGHT") > 0 And InStr(names, "PITCH") > 0
    ' --- profile on the Front Plane (the plane of the bend holds the leg-2 axis) at the helix start
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    Set xf = swSkMgr.ActiveSketch.ModelToSketchTransform
    Dim q3(2) As Double, pd As Variant, u0 As Double, v0 As Double, ou As Double, ov As Double, ua As Double, va As Double, axialIsX As Boolean
    Set mp = mu.CreatePoint(fp): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData: u0 = pd(0): v0 = pd(1)
    q3(0) = 0: q3(1) = 0: q3(2) = 0
    Set mp = mu.CreatePoint(q3): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData: ou = pd(0): ov = pd(1)
    q3(0) = cxM: q3(1) = yFaceM: q3(2) = 0
    Set mp = mu.CreatePoint(q3): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData: ua = pd(0): va = pd(1)
    q3(1) = yFaceM - heightM
    Set mp = mu.CreatePoint(q3): Set mp = mp.MultiplyTransform(xf): pd = mp.ArrayData
    axialIsX = (Abs(pd(0) - ua) > Abs(pd(1) - va))
    Dim sRad As Double, half As Double, a0 As Double, q0 As Double
    If axialIsX Then sRad = IIf(v0 - va >= 0, 1#, -1#) Else sRad = IIf(u0 - ua >= 0, 1#, -1#)     ' away from the axis = apex side (female)
    half = thdhM * Tan(3.14159265358979 / 6)
    If axialIsX Then a0 = u0: q0 = v0 Else a0 = v0: q0 = u0
    Trace nm & ": profile start (" & Format(u0 / IN_, "0.0000") & ", " & Format(v0 / IN_, "0.0000") & ") axialIsX=" & axialIsX & " apex dir " & sRad
    swSkMgr.AddToDB = True
    Dim l1 As SldWorks.SketchSegment, l1b As SldWorks.SketchSegment, l2 As SldWorks.SketchSegment, l3 As SldWorks.SketchSegment, lq As SldWorks.SketchSegment
    Set l1 = MkLine(axialIsX, a0 - half, q0, a0, q0)
    Set l1b = MkLine(axialIsX, a0, q0, a0 + half, q0)
    Set l2 = MkLine(axialIsX, a0 + half, q0, a0, q0 + sRad * thdhM)
    Set l3 = MkLine(axialIsX, a0, q0 + sRad * thdhM, a0 - half, q0)
    Set lq = MkLine(axialIsX, a0, q0, a0, q0 + sRad * thdhM)
    swSkMgr.AddToDB = False
    lq.ConstructionGeometry = True
    Dim n1 As SldWorks.SketchLine, n1b As SldWorks.SketchLine, n2 As SldWorks.SketchLine, n3 As SldWorks.SketchLine, nq As SldWorks.SketchLine
    Set n1 = l1: Set n1b = l1b: Set n2 = l2: Set n3 = l3: Set nq = lq
    swModel.ClearSelection2 True: n1.GetEndPoint2.Select4 False, Nothing: n1b.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n1b.GetEndPoint2.Select4 False, Nothing: n2.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n2.GetEndPoint2.Select4 False, Nothing: n3.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: n3.GetEndPoint2.Select4 False, Nothing: n1.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: nq.GetStartPoint2.Select4 False, Nothing: n1.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: nq.GetEndPoint2.Select4 False, Nothing: n2.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    Dim baseRel As String, perpRel As String
    baseRel = IIf(axialIsX, "sgHORIZONTAL", "sgVERTICAL"): perpRel = IIf(axialIsX, "sgVERTICAL", "sgHORIZONTAL")
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: swModel.SketchAddConstraints baseRel
    swModel.ClearSelection2 True: l1b.Select4 False, Nothing: swModel.SketchAddConstraints baseRel
    swModel.ClearSelection2 True: lq.Select4 False, Nothing: swModel.SketchAddConstraints perpRel
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: l1b.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    swModel.ClearSelection2 True: l2.Select4 False, Nothing: l3.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    ' base centre P (= helix start): axial and radial distance from the origin; apex: radial distance from the origin (table-driven)
    Call DimPtOrigin(n1.GetEndPoint2, "PROF_AX", Abs(a0 - IIf(axialIsX, ou, ov)), axialIsX, True, u0, v0, ou, ov)
    Call DimPtOrigin(n1.GetEndPoint2, "PROF_R", Abs(q0 - IIf(axialIsX, ov, ou)), axialIsX, False, u0, v0, ou, ov)
    Call DimPtOrigin(n2.GetEndPoint2, "APEXR", Abs(q0 + sRad * thdhM - IIf(axialIsX, ov, ou)), axialIsX, False, u0, v0, ou, ov)
    Dim kk As Long, v As Double
    For kk = 0 To 5
        swModel.ClearSelection2 True
        l2.Select4 False, Nothing: l3.Select4 True, Nothing
        If axialIsX Then
            Set d = swModel.AddDimension2(a0 + IIf(kk >= 4, 0.003 * (kk - 4.5), 0), q0 + sRad * thdhM * (1.6 - (kk Mod 2) * 2.4), 0)
        Else
            Set d = swModel.AddDimension2(q0 + sRad * thdhM * (1.6 - (kk Mod 2) * 2.4), a0 + IIf(kk >= 4, 0.003 * (kk - 4.5), 0), 0)
        End If
        If d Is Nothing Then Exit For
        v = d.GetDimension2(0).SystemValue
        If Abs(v - 3.14159265358979 / 3) < 0.001 Then Exit For
        DeleteDisp d: Set d = Nothing
    Next kk
    Check nm & " 60 deg tooth angle placed", (Not d Is Nothing) And Abs(v - 3.14159265358979 / 3) < 0.001
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set pf = swModel.FeatureByPositionReverse(0): pf.Name = "THDPROF_B"
    Check nm & " profile sketch THDPROF_B fully defined", (pf.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' --- swept cut: profile mark 1, helix mark 4 (the 2026-10-15 prototype; the definition's Profile / Path are not set)
    Dim vol0 As Double: vol0 = Volume()
    Dim swd As Object
    Set swd = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmSweepCut)
    If Not swd Is Nothing Then
        swModel.ClearSelection2 True
        pf.Select2 False, 1: hx.Select2 True, 4
        Set f = swFeatMgr.CreateFeature(swd)
        Trace nm & ": sweep CreateFeature -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    End If
    Check nm & " swept cut created", Not f Is Nothing
    If f Is Nothing Then Exit Sub
    f.Name = nm
    Dim vol1 As Double: vol1 = Volume()
    Check nm & " sweep removed material: " & Format((vol0 - vol1) / IN_ ^ 3, "0.00000") & " in^3", vol1 < vol0
    ' the helix curve stays in the tree (the cut needs it) but is hidden in the saved part
    swModel.ClearSelection2 True: hx.Select2 False, 0: swModel.BlankRefGeom: swModel.ClearSelection2 True
    Dim sup As Boolean
    sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)
    Check nm & " suppressed", sup
End Sub
'''


def emit(root, hdr, ok, refrow):
    sp = SPEC[root]
    cols, _, X = refrow
    c, g, J, lib = X['c'], X['g'], X['J'], X['lib']
    swv = sp.get('end2') == 'JICSW'
    PN = cols['$PRP@PartNo']
    V, rB = end1_profile(c, J)
    n = len(V)
    L = c['LJ']
    s = J['seg']
    bodyseg = n - 3
    axis = n - 1
    D, REL = [], []
    def dl(seg_, nm, val, tx, ty): D.append(f'    Call Dim_len({seg_}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def dr(seg_, nm, val, tx, ty): D.append(f'    Call Dim_rad({seg_}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def da(seg_, seg2, nm, deg, tx, ty): D.append(f'    Call Dim_ang({seg_}, {seg2}, "{nm}", {math.radians(deg):.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def dp(segPt, useEnd, segLine, nm, val, tx, ty): D.append(f'    Call Dim_ptline({segPt}, {useEnd}, {segLine}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def mid(k): return (V[k][0] + V[k + 1][0]) / 2
    # END1 dimensions = the straights' JICM End A set (gen_straight2.emit) + overall LJ + BODYR
    e = J['e']
    dl(-1, 'LJ', L, L / 2, rB + 0.6)
    dr(bodyseg, 'BODYR', rB, mid(bodyseg), -0.45)
    dr(s['thd'], 'THDMAJR_A', e['TM'] / 2, mid(s['thd']), -0.3)
    dl(s['relief'], 'JICA_RELIEFL', e['RL'], mid(s['relief']), rB + 0.25)
    da(s['ramp'], s['thd'], 'RELIEFANG', 60, V[s['ramp']][0] + 0.1, rB + 0.1)
    dl(s['thd'], 'JICA_THDZ', e['TZ'], mid(s['thd']), rB + 0.35)
    dr(s['land'], 'JICA_CONER', e['CD'] / 2, mid(s['land']), -0.2)
    dl(s['land'], 'JICA_LANDL', e['LL'], mid(s['land']), rB + 0.15)
    dp(s['seat'], 'True', s['face'], 'JICA_SEATL', e['SL'], mid(s['seat']), rB + 0.45)
    da(s['seat'], axis, 'SEATB', 37, V[s['seat']][0] + 0.05, -0.15)
    REL.append(f'    Call Collinear({s["relief"]}, {s["land"]})')
    vol1 = poly_volume(V)
    per = 1 if n <= 24 else 2
    pts = ', _\n'.join('    ' + ', '.join(f'{x*IN:.9f}, {r*IN:.9f}' for x, r in V[k:k + per]) for k in range(0, n, per))
    t = J['thread']
    thd = f'    Call ThreadCut({t["ex"]*IN:.9f}, {t["er"]*IN:.9f}, {t["depth"]*IN:.9f}, "{t["size"]}", "THD_EndA", -1#, {t["pitch"]*IN:.9f})'
    if swv:
        tb = X['S']['thread']
        thd += ('\n    stepName = "Nut thread"\n'
                f'    Call HelixThreadY({g["X0"]*IN:.9f}, {g["F"][1]*IN:.9f}, {tb["r"]*IN:.9f}, {tb["height"]*IN:.9f}, {tb["pitch"]*IN:.9f}, '
                f'{tb["thdh"]*IN:.9f}, "THD_EndB")')
    hub = (c['HUBD'] / 2, c['HUBL']) if 'HUBD' in c else None          # 2026-10-21: flange head with braze hub
    path = vba_path('PATH', ('TUBESTART', 'T1X', 'RB', 'FX', 'FY'), g['T1'], g['Cb'], g['T2'], g['E'], c['S'], 0.35,
                    ext=((g['F'], c['HUBL'] - HUB_OVL) if hub else None))
    pathx = vba_path('PATHX', ('BSTART', 'BT1X', 'BRB', 'BFX', 'BFY'), g['T1'], g['Cb'], g['T2'], g['FX'], -BX, 0.55)
    head = vba_swivel(g, X['S'], c['D'] / 2, X['ov'])[0] if swv else vba_head(g, lib, c['O'] / 2, hub)
    # config spot check + per-configuration box (the head and the end piece set it - expected_box samples every piece)
    params = ['LJ@DRIVE', 'BODYR@DRIVE', 'T1X@PATH', 'RB@PATH', 'FX@PATH', 'FY@PATH', 'TUBEOD@TUBE', 'TUBEID@BORE',
              'SWB_NUTR@SWSK' if swv else 'FLGB_HEADR@HEADSK', 'HEXB@HEX'] + (['OFFSET@NUTPLN', 'NUTCX@NUTHEXSK', 'HELIXCX@HELIXSK_B',
                                                                                'HEIGHT@HELIX_B', 'PROF_R@THDPROF_B', 'APEXR@THDPROF_B'] if swv else [])
    if 'HUBD' in c:                                                   # 2026-10-21: hub heads
        params += ['FLGB_HUBR@HEADSK', 'FLGB_HUBL@HEADSK', 'FACEEXT@PATH']
    chk = [ok[1], ok[-1]] if len(ok) > 2 else [ok[-1]]
    blk = sp3.check_block([(b[0]['$PRP@PartNo'], [b[0][p] for p in params]) for b in chk], params)
    nq = len(ok)
    bx = ["    ' ---- every configuration: the box = the flange head (x max, y max), the end-piece flats (y min), head / hex corners (z)",
          '    stepName = "Box check"',
          '    Dim bk_c() As String, bk_v() As Variant, bk_i As Long, bk_b As Variant',
          f'    ReDim bk_c({nq - 1}): ReDim bk_v({nq - 1})']
    for i, b in enumerate(ok):
        e_ = b[2]['box']
        bx.append(f'    bk_c({i}) = "{b[0]["$PRP@PartNo"]}": bk_v({i}) = Array({e_["xmax"]:.6f}, {e_["ymax"]:.6f}, {e_["ymin"]:.6f}, {e_["zmax"]:.6f})')
    bx += [f'    For bk_i = 0 To {nq - 1}',
           '        swModel.ShowConfiguration2 bk_c(bk_i)',
           '        swModel.ForceRebuild3 False',
           '        bk_b = swModel.GetPartBox(True)',
           '        Check bk_c(bk_i) & ": box x max " & Format(bk_b(3) / IN_, "0.0000") & " / y max " & Format(bk_b(4) / IN_, "0.0000") & " / y min " & Format(bk_b(1) / IN_, "0.0000") & " / z max " & Format(bk_b(5) / IN_, "0.0000") & " (expect " & Format(bk_v(bk_i)(0), "0.0000") & " / " & Format(bk_v(bk_i)(1), "0.0000") & " / " & Format(bk_v(bk_i)(2), "0.0000") & " / " & Format(bk_v(bk_i)(3), "0.0000") & ")", Abs(bk_b(3) / IN_ - bk_v(bk_i)(0)) < 0.01 And Abs(bk_b(4) / IN_ - bk_v(bk_i)(1)) < 0.01 And Abs(bk_b(1) / IN_ - bk_v(bk_i)(2)) < 0.01 And Abs(bk_b(5) / IN_ - bk_v(bk_i)(3)) < 0.01',
           '        Check bk_c(bk_i) & ": bore open at the JIC tip", Not AxisCovered(0#)',
           '    Next bk_i', '']
    box0 = X['box']
    entry = f'Build{root}'
    testline = ("\n'  TEST BUILD: DataStatus TEST rows - geometry test of the model type only, never part data; never ship this macro."
                if any(b[0]['$PRP@DataStatus'] == 'TEST' for b in ok) else '')
    vba = f'''Attribute VB_Name = "Build_{root}_MASTER"
' ============================================================================
'  Build_{root}_MASTER.bas  -  OMi fitting library, generated {TODAY} by gen_bent.py
'  {sp['name']} - master from reference configuration {PN} (DesignTable_{root}_SW2.xlsx row 2)
'  DRIVE (JIC end piece, revolved about X, hex-cut) + PATH / TUBE (circular sweep) + {'SWSK / SWIVEL (female JIC swivel end) + NUTPLN /' if swv else 'HEADSK / HEAD (flange head about the leg-2'}
'  {'NUTHEXSK / NUTCUT (nut hex)' if swv else 'axis)'} + PATHX / BORE (circular swept cut) + THD_EndA{' + THD_EndB (nut thread: helix + swept cut)' if swv else ''}.  Bend {sp['bend']:g} deg.
'  Run in SolidWorks: Tools > Macro > Run > {entry}.  Report: 03_SCRIPTS\\Build_{root}_report.txt{testline}
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const SUPPRESS_THREADS As Boolean = False      ' True = project resting state (threads suppressed); False = threads visible
Const TABLE_PATH As String = "{DEV}\\04_DESIGN_TABLES\\DesignTable_{root}_SW2.xlsx"
Const SAVE_PATH  As String = "{DEV}\\11_MASTERS\\{root}_MASTER.SLDPRT"
Const REPORT_PATH As String = "{DEV}\\03_SCRIPTS\\Build_{root}_report.txt"

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim seg() As SldWorks.SketchSegment
Dim axisCL As SldWorks.SketchSegment
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String
Dim curAxis As Long
Dim hs({9 if hub else 7}) As SldWorks.SketchSegment{chr(10) + "Dim pe As SldWorks.SketchSegment" if hub else ""}

Const NPTS As Long = {n}
Dim PX({n-1}) As Double, PR({n-1}) As Double

Sub LoadPoints()
    Dim v As Variant, i As Long
    v = Array( _
{pts})
    For i = 0 To NPTS - 1
        PX(i) = v(2 * i): PR(i) = v(2 * i + 1)
    Next i
End Sub

Sub {entry}()
    ' a missing report / save folder raised run-time error 76 before the error trap and left a modal VBA box (2026-10-14)
    Dim fld As String
    fld = Left(REPORT_PATH, InStrRev(REPORT_PATH, "\\"))
    If Dir(fld, vbDirectory) = "" Then MsgBox "Report folder missing: " & fld & " - nothing built.": Exit Sub
    fld = Left(SAVE_PATH, InStrRev(SAVE_PATH, "\\"))
    If Dir(fld, vbDirectory) = "" Then MsgBox "Save folder missing: " & fld & " - nothing built.": Exit Sub
    Set swApp = Application.SldWorks
    swApp.SetUserPreferenceToggle swUserPreferenceToggle_e.swInputDimValOnCreate, False
    Dim tpl As String
    tpl = swApp.GetUserPreferenceStringValue(swUserPreferenceStringValue_e.swDefaultTemplatePart)
    Set swModel = swApp.NewDocument(tpl, 0, 0, 0)
    If swModel Is Nothing Then MsgBox "Could not create a new part - check the default part template.": Exit Sub
    swModel.Extension.SetUserPreferenceInteger swUserPreferenceIntegerValue_e.swUnitSystem, swUserPreferenceOption_e.swDetailingNoOptionSpecified, swUnitSystem_e.swUnitSystem_IPS
    Set swSkMgr = swModel.SketchManager
    Set swFeatMgr = swModel.FeatureManager
    Set swSelMgr = swModel.SelectionManager
    LoadPoints
    report = "": nErr = 0
    fnRep = FreeFile
    Open REPORT_PATH For Output As #fnRep
    Print #fnRep, "Build_{root}_MASTER  " & Now
    On Error GoTo Trap
    Dim swFeat As SldWorks.Feature
    Dim ok As Boolean
    Dim pc As SldWorks.SketchSegment, p1 As SldWorks.SketchSegment, pa As SldWorks.SketchSegment, p2 As SldWorks.SketchSegment
    Dim hcl As SldWorks.SketchSegment, hsd As SldWorks.SelectData, hrev As SldWorks.Feature
    Dim tube As SldWorks.Feature, bore As SldWorks.Feature, hexcut As SldWorks.Feature
    stepName = "DRIVE sketch"

    ' ================= 1. DRIVE: JIC end piece (straights' End A chain + round body to LJ) =================
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    ReDim seg(NPTS - 1)
    Dim i As Long
    For i = 0 To NPTS - 2
        Set seg(i) = swSkMgr.CreateLine(PX(i), PR(i), 0, PX(i + 1), PR(i + 1), 0)
    Next i
    Set seg(NPTS - 1) = swSkMgr.CreateLine(PX(NPTS - 1), 0, 0, PX(0), 0, 0)
    Set axisCL = swSkMgr.CreateCenterLine(0, 0, 0, PX(NPTS - 1), 0, 0)
    swSkMgr.AddToDB = False
    swModel.ClearSelection2 True
    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine
    For i = 0 To NPTS - 1
        Set ln1 = seg(i): Set ln2 = seg((i + 1) Mod NPTS)
        swModel.ClearSelection2 True
        ln1.GetEndPoint2.Select4 False, Nothing
        ln2.GetStartPoint2.Select4 True, Nothing
        swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next i
    For i = 0 To NPTS - 1
        Dim x1 As Double, y1 As Double, x2 As Double, y2 As Double
        If i < NPTS - 1 Then
            x1 = PX(i): y1 = PR(i): x2 = PX(i + 1): y2 = PR(i + 1)
        Else
            x1 = PX(NPTS - 1): y1 = 0: x2 = PX(0): y2 = 0
        End If
        swModel.ClearSelection2 True
        If Abs(y1 - y2) < 0.000000001 Then
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
        ElseIf Abs(x1 - x2) < 0.000000001 Then
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
        End If
    Next i
    Dim cl As SldWorks.SketchLine
    Set cl = axisCL: Set ln1 = seg(0): Set ln2 = seg(NPTS - 2)
    swModel.ClearSelection2 True
    cl.GetStartPoint2.Select4 False, Nothing: ln1.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.GetEndPoint2.Select4 False, Nothing: ln2.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    Set ln1 = seg(0)
    ln1.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
{chr(10).join(REL)}
{chr(10).join(D)}
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "DRIVE"
    Check "DRIVE sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)

    stepName = "Revolve"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "DRIVE", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Dim sd As SldWorks.SelectData
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    axisCL.Select4 True, sd
    Dim rev As SldWorks.Feature
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "Revolve created (JIC end piece)", Not rev Is Nothing
    If rev Is Nothing Then GoTo Finish
    rev.Name = "BODY"
    Dim vrev As Double: vrev = Volume()
    Check "End-piece volume " & Format(vrev / IN_ ^ 3, "0.0000") & " in^3 (expect {vol1/IN**3:.4f})", Abs(vrev - {vol1:.12e}) < {vol1:.12e} * 0.002

    stepName = "HEX cut (end piece)"
    ' end-piece hex: from the end of the JIC chain over HEXL (the zone hex of the straights, 1700)
    Set hexcut = ZoneHexCut(False, 0#, {c['CHEX']*IN:.9f}, {J['endlen']*IN:.9f}, {c['HEXL']*IN:.9f}, {(J['endlen'] + c['HEXL']/2)*IN:.9f}, "HEX", "HEXB", "HEXCUT")
    Check "HEXB@HEX reachable", Not swModel.Parameter("HEXB@HEX") Is Nothing
    Check "DEPTH@HEXCUT reachable", Not swModel.Parameter("DEPTH@HEXCUT") Is Nothing
    Check "START@HEXCUT reachable", Not swModel.Parameter("START@HEXCUT") Is Nothing

{path}
    stepName = "TUBE sweep"
    Set tube = CircularSweep("PATH", {c['TUBEOD']*IN:.9f}, False, "TUBE", "TUBEOD")

{head}
{pathx}
    stepName = "BORE swept cut"
    Dim vb0 As Double: vb0 = Volume()
    Set bore = CircularSweep("PATHX", {c['D']*IN:.9f}, True, "BORE", "TUBEID")
    Check "BORE removed material (" & Format((vb0 - Volume()) / IN_ ^ 3, "0.0000") & " in^3)", Volume() < vb0
    Check "bore open on the axis at the JIC tip (x=0)", Not AxisCovered(0#)

    stepName = "Threads"
    curAxis = 0
{thd}
    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Check "Box x max " & Format(bb(3) / IN_, "0.0000") & " (expect {box0['xmax']:.4f}), y max " & Format(bb(4) / IN_, "0.0000") & " (expect {box0['ymax']:.4f}), y min " & Format(bb(1) / IN_, "0.0000") & " (expect {box0['ymin']:.4f})", Abs(bb(3) / IN_ - {box0['xmax']:.6f}) < 0.01 And Abs(bb(4) / IN_ - {box0['ymax']:.6f}) < 0.01 And Abs(bb(1) / IN_ - {box0['ymin']:.6f}) < 0.01
    Dim bodies As Variant
    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body (end piece + tube + head merged)", (UBound(bodies) = 0)

    stepName = "Design table"
    swModel.ClearSelection2 True
    ok = swModel.InsertFamilyTableOpen(TABLE_PATH)
    Check "Design table inserted from " & TABLE_PATH, ok
    swModel.CloseFamilyTable
    swModel.ForceRebuild3 False
    Dim cfgs As Variant
    cfgs = swModel.GetConfigurationNames
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect {len(ok) + 1})", (UBound(cfgs) + 1) >= {len(ok)}
{blk}{chr(10).join(bx)}
    swModel.ShowConfiguration2 "{PN}"
    swModel.ForceRebuild3 False

    ' ---- all-config rebuild sweep (2026-09-23, QA #124): every configuration, every feature must rebuild
    stepName = "All-config rebuild sweep"
    Dim sw_names As Variant, sw_i As Long, sw_f As SldWorks.Feature, sw_bad As Long, sw_n As Long, sw_b As Variant, sw_nb As Long
    sw_names = swModel.GetConfigurationNames
    sw_bad = 0: sw_n = 0
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then
            swModel.ShowConfiguration2 sw_names(sw_i)
            swModel.ForceRebuild3 False
            sw_n = sw_n + 1
            Set sw_f = swModel.FirstFeature
            Do While Not sw_f Is Nothing
                If sw_f.GetErrorCode2(True) <> 0 And Not sw_f.IsSuppressed Then
                    Check sw_names(sw_i) & " feature " & sw_f.Name & " rebuilds (error code " & sw_f.GetErrorCode2(True) & ")", False
                    sw_bad = sw_bad + 1
                End If
                Set sw_f = sw_f.GetNextFeature
            Loop
            sw_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
            sw_nb = IIf(IsEmpty(sw_b), 0, UBound(sw_b) + 1)
            If sw_nb <> 1 Then Check sw_names(sw_i) & " one solid body (found " & sw_nb & ")", False: sw_bad = sw_bad + 1
        End If
    Next sw_i
    Check "All-config sweep: " & sw_n & " configurations rebuilt, " & sw_bad & " feature/body failures", sw_bad = 0

    ' ---- every configuration once more with ALL its threads on (THD_EndB is suppressed when made, so the sweep above skips it;
    ' ThreadCut leaves THD_EndA on): all off -> volume, all on -> each THD_ feature must rebuild, the threads must cut material,
    ' one solid body (2026-10-15, bent tubes)
    stepName = "Thread check"
    Dim tc_i As Long, tc_f As SldWorks.Feature, tc_v0 As Double, tc_b As Variant, tc_nb As Long, tc_bad As Long, tc_n As Long
    tc_bad = 0: tc_n = 0
    For tc_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(tc_i) <> "Default" Then
            swModel.ShowConfiguration2 sw_names(tc_i)
            Set tc_f = swModel.FirstFeature
            Do While Not tc_f Is Nothing
                If Left(tc_f.Name, 4) = "THD_" Then tc_f.SetSuppression2 swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swThisConfiguration, Empty
                Set tc_f = tc_f.GetNextFeature
            Loop
            swModel.ForceRebuild3 False
            tc_v0 = Volume()
            Set tc_f = swModel.FirstFeature
            Do While Not tc_f Is Nothing
                If Left(tc_f.Name, 4) = "THD_" Then tc_f.SetSuppression2 swFeatureSuppressionAction_e.swUnSuppressFeature, swInConfigurationOpts_e.swThisConfiguration, Empty
                Set tc_f = tc_f.GetNextFeature
            Loop
            swModel.ForceRebuild3 False
            Set tc_f = swModel.FirstFeature
            Do While Not tc_f Is Nothing
                If Left(tc_f.Name, 4) = "THD_" Then
                    tc_n = tc_n + 1
                    If tc_f.IsSuppressed Or tc_f.GetErrorCode2(True) <> 0 Then
                        Check sw_names(tc_i) & " " & tc_f.Name & " rebuilds with the threads on (error code " & tc_f.GetErrorCode2(True) & ", suppressed " & tc_f.IsSuppressed & ")", False
                        tc_bad = tc_bad + 1
                    End If
                End If
                Set tc_f = tc_f.GetNextFeature
            Loop
            tc_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
            tc_nb = IIf(IsEmpty(tc_b), 0, UBound(tc_b) + 1)
            Check sw_names(tc_i) & ": threads on - " & Format((tc_v0 - Volume()) / IN_ ^ 3, "0.00000") & " in^3 cut, " & tc_nb & " solid body", tc_nb = 1 And Volume() < tc_v0
        End If
    Next tc_i
    Check "Thread check: " & tc_n & " thread features rebuilt over " & sw_n & " configurations, " & tc_bad & " failures", tc_bad = 0 And tc_n > 0
    swModel.ShowConfiguration2 sw_names(LBound(sw_names) + IIf(sw_names(LBound(sw_names)) = "Default", 1, 0))

    ' ---- resting state (project rule): every THD_* feature suppressed in EVERY configuration before the save
    stepName = "Suppress threads for save"
    Dim st_f As SldWorks.Feature, st_n As Long, st_bad As Long
    st_n = 0: st_bad = 0
    Set st_f = swModel.FirstFeature
    Do While Not st_f Is Nothing
        If Left(st_f.Name, 4) = "THD_" Then
            st_n = st_n + 1
            st_bad = st_bad + SuppressEverywhere(st_f)
        End If
        Set st_f = st_f.GetNextFeature
    Loop
    swModel.ForceRebuild3 False
    Check "Threads suppressed in all configurations before save (" & st_n & " THD_ features)", st_n > 0 And st_bad = 0

    stepName = "Save"
    Dim e As Long, w As Long, t0 As Date, fdt As Date
    t0 = Now
    ok = swModel.Extension.SaveAs(SAVE_PATH, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
    Trace "SaveAs " & SAVE_PATH & " returned " & ok & " (error " & e & ", warning " & w & ")"
    If ok = False Then          ' not 'If Not ok': SolidWorks returns True as 1 and Not 1 = -2 (CLAUDE.md VBA trap)
        On Error Resume Next
        fdt = FileDateTime(SAVE_PATH)
        If Err.Number = 0 Then
            If DateDiff("s", t0, fdt) >= -5 Then ok = True: Trace "  file on disk written " & fdt & " - saved (SaveAs return value ignored)"
        End If
        Err.Clear
        On Error GoTo Trap
    End If
    If ok = False Then
        Dim alt As String: alt = Replace(SAVE_PATH, ".SLDPRT", "_" & Format(Now, "hhnnss") & ".SLDPRT")
        ok = swModel.Extension.SaveAs(alt, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
        Check "Saved to " & alt & " (first name was locked, error " & e & ")", ok
    Else
        Check "Saved to " & SAVE_PATH, ok
    End If

Finish:
    On Error Resume Next
    Close #fnRep
    MsgBox "Build_{root}_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
    Exit Sub
Trap:
    Check "RUNTIME ERROR during '" & stepName & "' at line " & Erl & ": " & Err.Number & " - " & Err.Description, False
    Resume Next
End Sub

' ---------------------------------------------------------------- bent-tube helpers (gen_bent.py)
{PATH_SUBS}
{HUB_SUBS if hub else ''}{HEAD_SUBS}
{SW_SUBS}
' ---------------------------------------------------------------- helpers (shared library, SP3-validated on 2403/2405/2502HX)
{gs.HELP}'''
    vba = gs.ref_config_at_save(gs.add_progress(vba))
    p = os.path.join(OUT, f'Build_{root}_MASTER.bas')
    open(p, 'w').write(vba)
    return p, n


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    summary = {}
    for root in sys.argv[1:]:
        built, skipped = build_rows(root)
        good = [b for b in built if not b[1]]
        blocked = [b[0]['$PRP@PartNo'] + ': ' + '; '.join(b[1]) for b in built if b[1]]
        if not good:
            summary[root] = dict(configs=0, skipped=skipped, blocked=blocked, review=REV, test=TEST)
            print(f'{root}: 0 buildable rows - no macro written ({len(skipped)} skipped, {len(blocked)} blocked)')
            for x in blocked + skipped:
                print('   ', x)
            continue
        table, hdr, ok, refrow = write_sw2(root, built)
        macro, n = emit(root, hdr, ok, refrow)
        summary[root] = dict(configs=len(ok), ref=refrow[0]['$PRP@PartNo'], skipped=skipped, blocked=blocked, cols=len(hdr), verts=n,
                             review=REV, test=TEST, names=[b[0]['$PRP@PartNo'] for b in ok],
                             boxes={b[0]['$PRP@PartNo']: {k: round(v, 4) for k, v in b[2]['box'].items()} for b in ok})
        print(f'{root}: {len(ok)} configs (ref {refrow[0]["$PRP@PartNo"]}), {len(skipped)} skipped, {len(blocked)} blocked, {len(hdr)} table cols, {n} end-piece points')
        for x in blocked:
            print('   BLOCKED', x)
        for x in skipped:
            print('   skipped', x)
    json.dump(summary, open(os.path.join(OUT, f'gen_bent_summary_{"_".join(sys.argv[1:])}.json'), 'w'), indent=1)
