#!/usr/bin/env python3
"""gen_straight2.py - generic STRAIGHT master generator (hex body + two axial ends).

  python3 gen_straight2.py 5000 5404 5405 6401 6405 0403

Per root it writes  DesignTable_<root>_SW2.xlsx  and  Build_<root>_MASTER.bas  (Sub Build<root>).
End modules (profile + thread + bore rules):
   JICM   male 37deg flare : MS33656J chain per dash, copied from DesignTable_2403_SW2 (VERIFIED vs Brennan);
                             -40 measured on the Brennan 2404-40-32 STEP (JIC_MEAS_40, 2026-10-01)
   NPTFM  male NPTF        : ASME B1.20.3 (ms51500.NPTF): tip radius (E0+0.8P)/2, cone L2 at 1.7899deg,
                             relief cylinder to NPTF_ENDL (Brennan-measured per dash, 5404 table)
   NPTFF  female NPTF      : tap-drill pocket depth P1 per pipe dash (MS51503 P1 max, 2405 table), tapered helix
   ORBM   male SAE ORB     : THDMAJ over ORB_THDL, groove ORB_GRVDIA x ORB_GRVW (ORD-5700 / measured), no chamfer
   BRAZE  braze socket     : bore D2 to depth L7 (Air-Way), plain face
Body: revolved at BODYR = HEXB/cos30/2 then hex-cut (2403/2405 pattern).  SP3 rule: all diameters are
RADIUS dims (BODYR, THDMAJR_*, *_CONER, ORB_GRVR, NPTF_MAJR) and the table holds half the catalog value.
Every value in the table is traceable: Air-Way (the review table) + the standard chains above; every
modelling assumption is written into $PRP@AxialSource of every row.
"""
import sys, math, re, os, json, datetime, openpyxl
import sys as _sys, os as _os; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import omi_paths as P          # tools/omi_paths.py - every path of the toolchain (2026-09-25: made portable for Claude Code)
from progress_patch import add_progress, ref_config_at_save
from ms51500 import NPTF
IN = 0.0254
TAN60 = math.tan(math.radians(60)); TAN37 = math.tan(math.radians(37)); TAPER = math.radians(1.7899)
TODAY = datetime.date.today().isoformat()
REV = P.DESIGN_TABLES          # review tables DesignTable_<root>.xlsx: 04_DESIGN_TABLES is the single source of truth
OUT = P.OUT_STRAIGHT; os.makedirs(OUT, exist_ok=True)
DEV = P.DEV                    # the Windows path of OMi_Handoff written into the macros (TABLE_PATH / SAVE_PATH / REPORT_PATH)


FRESH = (   # historical: these review tables were refreshed with ScopeAction / OMiSKU on 2026-09-23 (all now read from 04_DESIGN_TABLES)
    '2408', '6408', '0318', '5406', '5406C', '5406P', '2700', '2705', '2706', '4404', '4604', '5404N', '6404', '6410', '2406', '6504', '6505', '6506', '6402', '6565', '1404', '1405', '1700')


def load_review(root):
    f = P.review_table(root)     # 2026-09-25: one location (the cloud copies used until then were content-identical to 04_DESIGN_TABLES)
    ws = openpyxl.load_workbook(f, read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]
    return h, [dict(zip(h, r)) for r in rows[2:] if r[0]]


def load_sw2(path):
    ws = openpyxl.load_workbook(path, read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0]]


# ---- per-dash end libraries -------------------------------------------------------------
JIC = {}   # dash -> dict(TM, RL, TZ, CD, LL, SL, thr)
for r in load_sw2(os.path.join(P.TEMPLATES, 'DesignTable_2403_SW2.xlsx')):
    a, b = re.findall(r'-(\d\d)', r['$PRP@PartNo'])[:2]
    for d, p, thr in ((int(a), 'JICA_', '$PRP@EndA_Thread'), (int(b), 'JICB_', '$PRP@EndB_Thread')):
        tm = 2 * r['THDMAJR_' + p[3] + '@DRIVE']
        JIC.setdefault(d, dict(TM=tm, RL=r[p + 'RELIEFL@DRIVE'], TZ=r[p + 'THDZ@DRIVE'], CD=2 * r[p + 'CONER@DRIVE'],
                               LL=r[p + 'LANDL@DRIVE'], SL=r[p + 'SEATL@DRIVE'], thr=r[thr]))
# SIZE-40 (2026-10-01): the -40 male JIC end (2-1/2 in tube, 3-12 UN thread). The frozen 2403 table stops at -32.
# MEASURED on the Brennan 2404-40-32 STEP (CADENAS / 3dfindit download 2026-08-11, 2404-40-32.stp, sha256 085b296e...cde9435): plane
# section through the axis with tools/measure/jicm.py. Validation: the same extraction on the Brennan 2404-32-16 STEP of that download
# returns the 2403 -32 chain exactly. Equal to the -40 chain of the user-built 2404 master (DesignTable_2404_SW2, row 2404-40-32).
# Brennan TFA catalog p.66 cross-check: 2408-40 L 2.051 - hex width 0.718 = 1.333 (STEP end length 1.335).
# MS33656J (12 Mar 1987; 03_SCRIPTS/_legacy/ms33656.py) prints a different -40 end (J 1.109, Q 0.125, D 2.380): geometry follows the
# Brennan STEP (project rule); one manufacturer -> ASSUMED; the difference is logged in $PRP@AxialSource of every row using it.
JIC_MEAS_40 = dict(TM=3.0, RL=0.140, TZ=0.7694, CD=2.880, LL=0.0725, SL=0.3185, thr='3-12', src40=True)
if 40 not in JIC: JIC[40] = dict(JIC_MEAS_40)
JIC40_ASSUME = ('-40 JIC END (2-1/2 in tube, 3-12 UN) IS NOT FROM MS33656J / THE 2403 TABLE: measured on the Brennan 2404-40-32 STEP '
                '(tip dia 2.400, 37deg seat 0.3185 to cone dia 2.880, land 0.0725, thread zone 0.7694 incl. the 45deg thread chamfer, '
                '60deg ramp, relief 0.140 at the cone dia; end length 1.335) - single manufacturer, ASSUMED; MS33656J as printed differs '
                '(end length J 1.109, relief Q 0.125, tip D 2.380) - the Brennan geometry is used (project rule: geometry from Brennan STEPs); '
                'the extraction reproduces the 2403 -32 chain on the Brennan 2404-32-16 STEP; Brennan catalog 2408-40 L - hex width = 1.333 agrees')
FPT = {}   # pipe dash -> dict(P1, TD2405, thr)
for r in load_sw2(os.path.join(P.TEMPLATES, 'DesignTable_2405_SW2.xlsx')):
    b = int(re.findall(r'-(\d\d)', r['$PRP@PartNo'])[1])
    FPT.setdefault(b, dict(P1=r['DEPTH@BORECUT_A'], TD=r['TAPDRILL@BORE_A'], thr=r['$PRP@EndA_Thread']))
ENDL = {}  # pipe dash -> male NPTF end length (Brennan-measured, 5404 table)
for r in load_review('5404')[1]:
    dd = [int(x) for x in re.findall(r'-(\d\d)', r['$PRP@PartNo'])[:2]]
    if len(dd) == 2 and r.get('NPTFA_ENDL@DRIVE'):
        ENDL.setdefault(dd[0], r['NPTFA_ENDL@DRIVE']); ENDL.setdefault(dd[1], r['NPTFB_ENDL@DRIVE'])
# 2026-10-18 (genfeat straights, -40 PIPE END): the 2-1/2 NPTF (-40) male and female pipe ends, BRENNAN-MEASURED (user 2026-10-02: "Brennan-
# measured threads accepted" for the -40 sizes instead of the ASME B1.20.1 row, which is not transcribed in the project; threads only need to
# show on drawings). Extractors: tools/measure/nptfm40.py (male end) and tools/measure/fgelbow.py --port (female port); evidence in
# tools/_out/genfeat_20261018/straights/measure_40/.
#  MALE (Brennan 5404-40-40 both ends, 5406-40-32, and the NPT leg of 2501-40-40-FG): 45deg tip chamfer 0.1042, blank cone 1.788deg of dia
#  2.7769 extrapolated to the tip face, end length 1.515 to the hex face (all four ends), collar 2.875 (5406-40-32) / 2.880 (5404-40-40).
#  VALIDATION of the extractor on 22 male NPTF ends of 22 Brennan STEPs (-04 .. -32, 1404 / 2404-L / 2706 / 4404 / 5404 / 5406 / 6404) and the
#  -08 leg of 2501-LL-08-08-FG: end length = ENDL (5404 table) exactly at every size, and the Brennan blank cone at the tip face = ASME E0 + k P
#  with k = 0.4585 .. 0.4595 at all 8 library sizes (3 pitches; mean 0.4589). Hence, at -40:
#    threads per inch 8 = the Brennan TFA catalog callout "2-1/2-8" (5000 / 5404 / 5406 tables, PIPE_THD_NAME);
#    pipe OD D 2.875 = the smaller Brennan collar (the library D at -16 / -24 / -32 equals the smaller of the Brennan collars too);
#    pitch dia at the small end E0 = 2.7769 - 0.4589 / 8 = 2.71954 (ASSUMPTION: Brennan's blank rule of the 8 smaller sizes holds at -40);
#    thread length L2 from the ASME relation D = E0 + 0.8P + (L2 - 2P) / 16 (crest cone meets D at L5 = L2 - 2P; holds to 1e-4 on all 9
#    library sizes) -> L2 = 1.1374;  end length ENDL 1.515 (measured);  E1 / L1 (hand-tight plane) are read by no end module -> None.
#  FEMALE (Brennan 5000-40-40, both ports identical): 45deg mouth chamfer 0.0799, tapered minor 2.7892 -> 2.729 over 1.0443 from the face,
#  then a plain 2.729 bore through between the two ports - NO separate tap drill (as 5406-40-32's -32 port, A9 README). FPT[40]: tap drill
#  2.729, P1 = the taper (thread) depth 1.0443. Validation: the same extractor returns the recorded 5405-08-08 port (drill 0.718 to 0.90 =
#  FPT[8] P1) and the 5405-16-16 port (drill to 1.14 = FPT[16] P1).
NPTF40_MEAS = dict(nps='2-1/2', tpi=8, D=2.875, cone_tip=2.7769, k=0.4589, ENDL=1.515, FPT_P1=1.0443, FPT_TD=2.729)
if 40 not in NPTF:
    _m40 = NPTF40_MEAS; _E0_40 = round(_m40['cone_tip'] - _m40['k'] / _m40['tpi'], 5); _P40 = 1 / _m40['tpi']
    NPTF[40] = (_m40['nps'], _m40['tpi'], _m40['D'], _E0_40, None, None, round(16 * (_m40['D'] - _E0_40 - 0.8 * _P40) + 2 * _P40, 4))
if 40 not in ENDL: ENDL[40] = NPTF40_MEAS['ENDL']
if 40 not in FPT: FPT[40] = dict(P1=NPTF40_MEAS['FPT_P1'], TD=NPTF40_MEAS['FPT_TD'], thr='2 1/2-8 NPTF (female)', src40=True)
NPTF40_ASSUME = ('-40 PIPE END (2-1/2-8 NPTF) IS BRENNAN-MEASURED, NOT ASME B1.20.1 (user 2026-10-02: Brennan-measured threads accepted for -40): '
                 'male end - pitch dia at the tip E0 2.71954 = the Brennan blank cone 2.7769 (5404-40-40 / 5406-40-32 / 2501-40-40-FG STEPs) - 0.4589 P '
                 '(the Brennan blank sits 0.4585-0.4595 P above ASME E0 at all 8 library sizes -04..-32, ASSUMED to hold at -40), crest E0 + 0.8P, '
                 'taper 1.7899deg, thread length L2 1.1374 from D = E0 + 0.8P + (L2 - 2P)/16 with pipe OD D 2.875 (Brennan collar), end length 1.515 '
                 '(measured on all four Brennan -40 male ends); female port - tap drill 2.729 and thread depth 1.0443 = the Brennan 5000-40-40 tapered '
                 'port (no separate drill: the 2.729 bore runs through); 8 threads per inch = Brennan TFA catalog callout 2-1/2-8; single manufacturer, ASSUMED')
ORB = {}   # dash -> dict(TM, THDL, GD, GW)  from 6401 + 6405 + 6410 review tables (ORD-5700 / measured)
for root in ('6401', '6405', '6410'):
    for r in load_review(root)[1]:
        dd = re.findall(r'-(\d\d)', r['$PRP@PartNo'])
        if not dd: continue
        a = int(dd[0])
        tm = r.get('THDMAJ_A@DRIVE') or r.get('THDMAJ_B1@DRIVE')
        if tm and r.get('ORB_GRVW@DRIVE') and r.get('ORB_THDL@DRIVE'):
            ORB.setdefault(a, dict(TM=tm, THDL=r['ORB_THDL@DRIVE'], GD=r['ORB_GRVDIA@DRIVE'], GW=r['ORB_GRVW@DRIVE']))

# SIZE-40 (2026-10-01): library gaps. An end whose dash is missing from an end library is skipped with the document / STEP that would
# fill it - instead of a bare KeyError (here), an uncaught KeyError that stops the whole root (gen_tee), or the old silent fallback of
# the male NPTF end length to the thread length L2 (never used: ENDL covers every NPTF dash). Nothing is invented here.
PIPE_THD_NAME = {1: '1/16-27', 40: '2-1/2-8', 48: '3-8'}   # thread callouts as printed by the OMi dimension file / Brennan TFA catalog
LIB_NEED = {
    'NPTF': 'the ASME B1.20.1 Table 2 / B1.20.3 basic dimensions of the {nps} NPT(F) row (pipe OD D, E0, E1, L1, L2, threads per inch) '
            '-> one line in ms51500.NPTF (question Q-NEW-ASME40 for -40; or Brennan-measured thread geometry)',
    'ENDL': 'the male NPTF end length (thread + relief) of -{d:02d}, measured on a Brennan STEP with a -{d:02d} male NPTF end '
            '(5404-{d:02d}-{d:02d} preferred) -> NPTFA_ENDL / NPTFB_ENDL of that 5404 review row',
    'FPT': 'the female NPTF port drill depth P1 of -{d:02d} (MS51503 / the 2405 table stop at -32), measured on a Brennan STEP with a '
           '-{d:02d} female NPTF port (5000-{d:02d}-{d:02d} preferred) -> a measured FPT entry',
    'JIC': 'the male 37deg JIC chain of -{d:02d} (seat, land, thread zone, relief), measured on a Brennan STEP with a -{d:02d} male JIC end',
    'FSM': 'the male O-ring face-seal end of -{d:02d} (face groove, land, nose chamfer, thread length, relief, end length), measured on '
           'BRENNAN_FS6500-{d:02d}-{d:02d}-FG or BRENNAN_FS2403-{d:02d}-{d:02d} (STEPS_NEEDED part 2) with tools/_out/orfs_wp2_20261020/measure/fsmeasure.py '
           '-> FSM_MEAS[{d}]',
}


def lib_gap(lib, d):
    nps = PIPE_THD_NAME.get(d, f'-{d:02d} pipe-dash')
    return f'no -{d:02d} entry in the {lib} end library; needs ' + LIB_NEED[lib].format(d=d, nps=nps)


def lib_gaps(kinds_dashes):
    """messages for the ends of one part whose dash is missing from the end libraries they read (used by gen_tee before building)"""
    need = {'JICM': ('JIC',), 'JICBH': ('JIC',), 'JICSW': ('JIC',), 'NWO': ('JIC',), 'NPTFM': ('NPTF', 'ENDL'), 'NPTFF': ('FPT', 'NPTF'),
            'NPSMSW': ('NPTF',), 'FSM': ('FSM',), 'FSBH': ('FSM',)}
    libs = dict(JIC=JIC, NPTF=NPTF, ENDL=ENDL, FPT=FPT, FSM=FSM_MEAS)
    out = []
    for kind, d in kinds_dashes:
        for lib in need.get(kind, ()):
            if d not in libs[lib]:
                m = lib_gap(lib, d)
                if m not in out: out.append(m)
    return out


def tpi_of(thr):
    m = re.search(r'-(\d+(?:\s1/2)?)(?!\s*/)', str(thr)); return float(m.group(1).replace(' 1/2', '.5'))


def npt_thr(dash):
    nps, tpi, D, E0, E1, L1, L2 = NPTF[dash]
    return f"{nps.replace('-', ' ')}-{tpi:g}".replace('11.5', '11 1/2')


# ---- end modules: return dict(verts=[(x,r)...from tip inward, ending at (x_end, r_end<rB)], dims=[...], feats=...)
def end_JICM(dash, sfx, ext=None):
    # ext (2026-10-01, SPEC 2404 only): a JIC chain dict(TM, RL, TZ, CD, LL, SL, thr) taken from the part's own review-table row,
    # used ONLY for a dash the JIC library does not carry. Every other call passes no ext and reads the library exactly as before.
    # (integration 2026-10-01: SIZE-40 adds JIC[40] = JIC_MEAS_40 to the library, measured on the Brennan 2404-40-32 STEP and equal to
    # the -40 chain of the hand-made 2404 row, so no current row reaches ext; it stays as the fallback for a future dash.)
    if ext is None and dash not in JIC: raise KeyError(lib_gap('JIC', dash))     # SIZE-40: library gap -> the source that would fill it
    e = JIC[dash] if ext is None else ext; rT = (e['CD'] - 2 * e['SL'] * TAN37) / 2; rC = e['CD'] / 2; rM = e['TM'] / 2
    x = 0.0; V = [(0, rT)]; x += e['SL']; V += [(x, rC)]; x += e['LL']; V += [(x, rC), (x, rM)]; x += e['TZ']; V += [(x, rM)]
    x += (e['TM'] - e['CD']) / 2 / TAN60; V += [(x, rC)]; x += e['RL']; V += [(x, rC)]
    # segment roles by index within this module (segment k = V[k-1]->V[k], with V[-1] = tip axis point (0,0) as seg 0)
    seg = dict(face=0, seat=1, land=2, stepA=3, thd=4, ramp=5, relief=6)
    cols = {f'THDMAJR_{sfx}@DRIVE': e['TM'] / 2, f'JIC{sfx}_RELIEFL@DRIVE': e['RL'], f'JIC{sfx}_THDZ@DRIVE': e['TZ'],
            f'JIC{sfx}_CONER@DRIVE': e['CD'] / 2, f'JIC{sfx}_LANDL@DRIVE': e['LL'], f'JIC{sfx}_SEATL@DRIVE': e['SL'],
            'RELIEFANG@DRIVE': 60, 'SEATB@DRIVE': 37,
            f'THDDIA@THD_End{sfx}': e['TM'], f'THDPITCH@THD_End{sfx}': round(1 / tpi_of(e['thr']), 5), f'DEPTH@THD_End{sfx}': round(e['SL'] + e['LL'] + e['TZ'], 4),
            f'Profile_Height@THD_End{sfx}_PROF': round(0.54127 / tpi_of(e['thr']), 5), f'Profile_Land@THD_End{sfx}_PROF': round(0.25 / tpi_of(e['thr']), 5), f'THDPITCH@THD_End{sfx}_PROF': round(1 / tpi_of(e['thr']), 5)}
    return dict(kind='JICM', V=V, endlen=x, seg=seg, cols=cols, thr=e['thr'], e=e, faceR=rT * 0.5,
                thread=dict(type='CUT', ex=e['SL'] + e['LL'] + e['TZ'], er=rM, depth=e['SL'] + e['LL'] + e['TZ'], size=f"{e['TM']:.4f}-{tpi_of(e['thr']):g}", pitch=1 / tpi_of(e['thr'])))


def end_JICBH(dash, sfx, I1):
    # JIC BULKHEAD end: the MS33656J nose (seat, land) and relief/ramp of the normal JIC end, with the thread zone
    # extended so that the whole end is Air-Way I1 long (Brennan 2705-08-08 STEP: bulkhead thread = the 3/4-16 JIC
    # thread itself, running from the relief to the land; seat 0.1546 / land 0.0984 / relief 0.094 = MS33656J -08)
    E = end_JICM(dash, sfx); e = E['e']
    ramp = (e['TM'] - e['CD']) / 2 / TAN60
    tz = round(I1 - (e['SL'] + e['LL'] + ramp + e['RL']), 4)
    if tz < e['TZ'] + 0.05: raise AssertionError(f'bulkhead length I1 {I1} leaves thread zone {tz} (standard JIC {e["TZ"]})')
    e = dict(e, TZ=tz)
    rT = (e['CD'] - 2 * e['SL'] * TAN37) / 2; rC = e['CD'] / 2; rM = e['TM'] / 2
    x = 0.0; V = [(0, rT)]; x += e['SL']; V += [(x, rC)]; x += e['LL']; V += [(x, rC), (x, rM)]; x += e['TZ']; V += [(x, rM)]
    x += ramp; V += [(x, rC)]; x += e['RL']; V += [(x, rC)]
    E['V'] = V; E['endlen'] = x; E['e'] = e; E['kind'] = 'JICM'; E['bulkhead'] = True
    E['cols'][f'JIC{sfx}_THDZ@DRIVE'] = tz
    E['cols'][f'DEPTH@THD_End{sfx}'] = round(e['SL'] + e['LL'] + tz, 4)
    E['thread'] = dict(E['thread'], ex=e['SL'] + e['LL'] + tz, depth=e['SL'] + e['LL'] + tz)
    E['thr'] = e['thr'] + ' (bulkhead)'
    return E


def end_NPTFM(dash, sfx, endl=None):
    if dash not in NPTF: raise KeyError(lib_gap('NPTF', dash))
    nps, tpi, D, E0, E1, L1, L2 = NPTF[dash]; P = 1 / tpi
    rS = (E0 + 0.8 * P) / 2; rL = rS + L2 * math.tan(TAPER)
    endl = endl or ENDL.get(dash)        # SIZE-40: no silent fallback to L2 (it was never used - ENDL covers every NPTF dash)
    if not endl: raise KeyError(lib_gap('ENDL', dash))
    assert endl >= L2 - 1e-9, (dash, endl, L2)
    V = [(0, rS), (L2, rL)]
    seg = dict(face=0, cone=1); x = L2
    if endl > L2 + 1e-6: V += [(endl, rL)]; seg['rel'] = 2; x = endl
    cols = {f'NPTF{sfx}_MAJR@DRIVE': round(rS, 5), f'NPTF{sfx}_THDL@DRIVE': L2, f'NPTF{sfx}_TAPER@DRIVE': 1.7899}
    if 'rel' in seg: cols[f'NPTF{sfx}_RELL@DRIVE'] = round(endl - L2, 4)
    cols.update({f'HELIXDIA@HELIXSK_{sfx}': round(2 * rS, 5), f'HEIGHT@HELIX_{sfx}': L2, f'PITCH@HELIX_{sfx}': round(P, 5),
                 f'PROF_R@THDPROF_{sfx}': round(rS, 5), f'APEXR@THDPROF_{sfx}': round(rS - 0.8 * P, 5)})
    return dict(kind='NPTFM', V=V, endlen=x, seg=seg, cols=cols, thr=npt_thr(dash) + ' NPTF', faceR=rS * 0.5, rS=rS, rL=rL, n40=(dash == 40),
                thread=dict(type='HELIX', r=rS, height=L2, pitch=P, thdh=0.8 * P, taper=TAPER, taperOut=True, apexOut=False))


def end_NPTFF(dash, sfx, td):
    if dash not in FPT: raise KeyError(lib_gap('FPT', dash))
    f = FPT[dash]; P = 1 / tpi_of(f['thr'])
    cols = {f'TAPDRILL{sfx}@POCKET_{sfx}': td, f'DEPTH@POCKETCUT_{sfx}': f['P1'],
            f'HELIXDIA@HELIXSK_{sfx}': td, f'HEIGHT@HELIX_{sfx}': f['P1'], f'PITCH@HELIX_{sfx}': round(P, 4),
            f'PROF_R@THDPROF_{sfx}': round(td / 2, 4), f'APEXR@THDPROF_{sfx}': round(td / 2 + 0.8 * P, 4)}
    return dict(kind='NPTFF', V=[], endlen=0.0, seg=dict(face=0), cols=cols, thr=f['thr'], faceR=None, td=td, P1=f['P1'], n40=bool(f.get('src40')),
                thread=dict(type='HELIX', r=td / 2, height=f['P1'], pitch=P, thdh=0.8 * P, taper=TAPER, taperOut=False, apexOut=True))


# 2026-09-24: ORB -32 groove width MEASURED on the Brennan 6400-32-32-O STEP (root dia 2.381 = ORD-5700 F, root width 0.125,
# thread length 0.469) - single source (ASSUMED), same value as the measured -16/-20/-24
ORB_GW_MEASURED = {32: 0.125, 14: 0.125}
# 2026-09-25 (batch 13): ORB -14 groove width MEASURED on the Brennan 6400-14-14-O STEP: thread major 1.1875 to 0.469 from the tip (= the
# 6408 review row), groove root dia 1.070 (= the row), groove width 0.125 to the hex face (ORB end 0.594) - single source (ASSUMED)
ORB_GW_SRC = {32: 'Brennan 6400-32-32-O STEP', 14: 'Brennan 6400-14-14-O STEP'}
# 2026-09-24 (batch 11): the ORB-end straights (6401, 6405, ...) take the -32 end from the same sources as the 6408 -32 plug:
# thread 2 1/2-12, thread length 0.469 and groove root dia 2.381 from the 6408 review row (ORD-5700 F / J1926, confirmed on the
# Brennan 6400-32-32-O STEP), groove width 0.125 MEASURED on that STEP - single source (ASSUMED)
for _r in load_review('6408')[1]:
    _dd = re.findall(r'-(\d\d)', str(_r['$PRP@PartNo']))
    if _dd and int(_dd[0]) in ORB_GW_MEASURED and int(_dd[0]) not in ORB and _r.get('ORB_THDL@DRIVE') and _r.get('ORB_GRVDIA@DRIVE') and _r.get('THDMAJ_A@DRIVE'):
        ORB[int(_dd[0])] = dict(TM=_r['THDMAJ_A@DRIVE'], THDL=_r['ORB_THDL@DRIVE'], GD=_r['ORB_GRVDIA@DRIVE'], GW=ORB_GW_MEASURED[int(_dd[0])], src='6408 row + ' + ORB_GW_SRC[int(_dd[0])])
# 2026-10-01 (tier 1, work group ORB-02): the male ORB -02 end (5/16-24) for the ORB-end straights (6405-02-02-O / -02-04-O, ...),
# merged from the 6408 review row like -14 / -32 above - but that row publishes all four values itself, so nothing is measured here:
# thread major 0.3125 (5/16-24), thread length 0.234 = MS51527G / MS51528D J2 (-02), groove root dia 0.250 = Parker ORD-5700 Table 4-4 F
# (O-ring 3-902) = MS51527G G1, groove width 0.063 = ORD-5700 Table 4-4 G (07_RAW_EXTRACTS/Report_ORB_groove_ORD5700.md). Cross-check: the
# Brennan 6801-04-02-NWO-FG STEP (adjustable -02 stud, tools/measure/nwo_run.py) reads thread 0.3126 x 0.234 long, undercut root dia 0.250
# (its undercut LENGTH belongs to the adjustable stud and is not the fixed groove width; at -04 that STEP family also gives 0.265 / 0.364 =
# ORB[4]). Keyed by part number so only this row can feed the dict; 'note' goes into $PRP@AxialSource of every row built with this end.
ORB_FROM_6408_ROW = {'6408-02-O-SOLID': 'male ORB -02 end (5/16-24): thread length 0.234, groove root dia 0.250, groove width 0.063 taken from the 6408-02-O-SOLID review row '
                                        '(MS51527G / MS51528D J2 thread length; Parker ORD-5700 Table 4-4 F / G, O-ring 3-902) - the same fixed ORB stud end on every series, as -03..-32 '
                                        '(ASSUMPTION); thread length and groove root dia = the Brennan 6801-04-02-NWO-FG STEP (adjustable stud); groove width single source (ORD-5700); '
                                        'no Brennan STEP with a fixed -02 ORB end yet'}
for _r in load_review('6408')[1]:
    _pn = str(_r['$PRP@PartNo']); _dd = re.findall(r'-(\d\d)', _pn)
    if _pn in ORB_FROM_6408_ROW and _dd and int(_dd[0]) not in ORB and all(_r.get(_c) for _c in ('THDMAJ_A@DRIVE', 'ORB_THDL@DRIVE', 'ORB_GRVDIA@DRIVE', 'ORB_GRVW@DRIVE')):
        ORB[int(_dd[0])] = dict(TM=_r['THDMAJ_A@DRIVE'], THDL=_r['ORB_THDL@DRIVE'], GD=_r['ORB_GRVDIA@DRIVE'], GW=_r['ORB_GRVW@DRIVE'], src=_pn + ' row',
                                note=ORB_FROM_6408_ROW[_pn])


# 2026-09-25: 6408 cored plug, MEASURED on the Brennan 6408-08-O and 6408-20-O STEPs (user download 2026-09-24):
# dash -> (hole dia, full-diameter depth from the ORB tip, drill-point apex from the tip (120deg point), overall length, hex AF)
PLUG_HOLE_MEAS = {8: (0.422, 0.4582, 0.580, 0.800, 0.875), 20: (1.093, 0.6345, 0.950, 1.200, 1.875)}


def plug_hole_overshoot(dash):
    # how far the full-diameter hole runs past the ORB end into the hex: 0.020 at -08 and 0.040 at -20 (measured), linear in the
    # dash between and beyond (ASSUMPTION for every other size)
    return round(0.020 + (dash - 8) * 0.020 / 12, 4)


def end_ORBM(dash, sfx, row=None):
    o = ORB.get(dash)
    if row is not None and row.get('ORB_THDL@DRIVE') is not None:
        # the part's own review-table ORB columns (6408: SAE J1926 plug end) - blocked when the groove width is unpublished
        gw = row.get('ORB_GRVW@DRIVE')
        if gw is None and dash in ORB_GW_MEASURED: gw = ORB_GW_MEASURED[dash]
        if gw is None or row.get('ORB_GRVDIA@DRIVE') is None: raise KeyError('ORB groove width/diameter not published for this size')
        o = dict(TM=row['THDMAJ_A@DRIVE'], THDL=row['ORB_THDL@DRIVE'], GD=row['ORB_GRVDIA@DRIVE'], GW=gw,
                 src=(ORB_GW_SRC.get(dash, 'Brennan STEP') + ' (groove width)') if row.get('ORB_GRVW@DRIVE') is None else None)   # 2026-09-25: lets the stale 'groove width unmeasured' note be replaced
    if o is None: raise KeyError(f'no ORB end data for -{dash:02d}')
    rM = o['TM'] / 2; rG = o['GD'] / 2
    V = [(0, rM), (o['THDL'], rM), (o['THDL'], rG), (o['THDL'] + o['GW'], rG)]
    seg = dict(face=0, thd=1, stepG=2, grv=3)
    cols = {f'THDMAJR_{sfx}@DRIVE': rM, f'ORB{sfx}_THDL@DRIVE': o['THDL'], f'ORB{sfx}_GRVR@DRIVE': rG, f'ORB{sfx}_GRVW@DRIVE': o['GW'],
            f'THDDIA@THD_End{sfx}': o['TM'], f'THDPITCH@THD_End{sfx}': round(1 / tpi_of(ORB_THR[dash]), 5), f'DEPTH@THD_End{sfx}': o['THDL'],
            f'Profile_Height@THD_End{sfx}_PROF': round(0.54127 / tpi_of(ORB_THR[dash]), 5), f'Profile_Land@THD_End{sfx}_PROF': round(0.25 / tpi_of(ORB_THR[dash]), 5), f'THDPITCH@THD_End{sfx}_PROF': round(1 / tpi_of(ORB_THR[dash]), 5)}
    return dict(kind='ORBM', V=V, endlen=o['THDL'] + o['GW'], seg=seg, cols=cols, thr=None, faceR=rM * 0.5, o=o, dash=dash,
                thread=dict(type='CUT', ex=o['THDL'], er=rM, depth=o['THDL'], size=None, pitch=None))


# MS51531D (Nut, Tube Coupling, 37 Degree Flared, 30 Sep 2021) FIGURE 1, transcribed 3-pass from the ASSIST PDF
# (Report_AN818_MS51531D.md): dash -> (I1 = thread-end face to the internal shoulder, J1 = full thread min, D1 = tube bore, L1, C hex)
MS51531 = {2: (.460, .246, .179, .550, .375), 3: (.506, .277, .241, .610, .4375), 4: (.532, .295, .304, .620, .5625), 5: (.579, .326, .373, .680, .625),
           6: (.603, .328, .439, .730, .6875), 8: (.723, .370, .568, .850, .875), 10: (.817, .456, .696, .980, 1.0), 12: (.868, .464, .832, 1.030, 1.25),
           14: (.914, .511, .959, 1.090, 1.375), 16: (.962, .558, 1.087, 1.130, 1.5), 20: (1.017, .558, 1.344, 1.230, 2.0), 24: (1.170, .656, 1.614, 1.420, 2.25),
           32: (1.462, .839, 2.164, 1.750, 2.875)}


def end_UNFF(dash, sfx, major, thr):
    # female UN/UNF-2B straight thread (JIC nut): pocket = ASME B1.1 basic minor dia (D - 1.082532P) to the MS51531D internal shoulder I1;
    # helical thread (no taper) over MS51531D J1 (full thread min), 60deg V from the minor cylinder to the basic major (height 0.54127P)
    I1, J1, D1, L1, C = MS51531[dash]; P = 1 / tpi_of(thr); td = round(major - 1.082532 * P, 4)
    cols = {f'TAPDRILL{sfx}@POCKET_{sfx}': td, f'DEPTH@POCKETCUT_{sfx}': I1,
            f'HELIXDIA@HELIXSK_{sfx}': td, f'HEIGHT@HELIX_{sfx}': J1, f'PITCH@HELIX_{sfx}': round(P, 5),
            f'PROF_R@THDPROF_{sfx}': round(td / 2, 5), f'APEXR@THDPROF_{sfx}': round(td / 2 + 0.54127 * P, 5)}
    return dict(kind='UNFF', V=[], endlen=0.0, seg=dict(face=0), cols=cols, thr=thr + (' UN-2B' if tpi_of(thr) <= 12 else ' UNF-2B'), faceR=None, td=td, P1=I1, D1=D1,
                thread=dict(type='HELIX', r=td / 2, height=J1, pitch=P, thdh=0.54127 * P, taper=0.0, taperOut=False, apexOut=True))


def frac(t):
    # '1 1/4' -> 1.25 ; '3/8' -> 0.375 ; '1' -> 1.0
    t = str(t).strip(); tot = 0.0
    for part in t.split():
        if '/' in part: n_, d_ = part.split('/'); tot += float(n_) / float(d_)
        else: tot += float(part)
    return tot


# Brennan 4404-08-06 STEP (09_STEP_FILES): 1/2 hose stub OD 0.500, bore 0.406 (= Air-Way D3), bead = torus of section radius
# 0.060 centred 0.251 from the stub tip, bead dia 0.560 (= Air-Way AA), stub 1.500 from the hex face, hex 0.29 x 0.75 A/F
HOSE_STUBL = 1.500; HOSE_BEADC = 0.251; HOSE_BEADRHO = 0.060


def end_HOSEB(sfx, stubOD, bead):
    # beaded hose stub: plain tube OD = the hose size (Air-Way TUBE OD column), one bead of dia AA (Air-Way);
    # stub length, bead position and bead width from the Brennan 4404-08-06 STEP (ASSUMED for the other sizes);
    # the bead's round section is modelled as a flat-topped ring of the Brennan chord width (sqrt(2*rho*h - h^2) * 2)
    rS = stubOD / 2; rA = bead / 2; h = rA - rS
    if h <= 0.005: raise AssertionError(f'bead dia {bead} not above stub OD {stubOD}')
    w = 2 * math.sqrt(max(2 * HOSE_BEADRHO * h - h * h, 0)) if h < HOSE_BEADRHO else 2 * HOSE_BEADRHO
    w = round(w, 4); p1 = round(HOSE_BEADC - w / 2, 4); p2 = round(p1 + w, 4); L = HOSE_STUBL
    V = [(0, rS), (p1, rS), (p1, rA), (p2, rA), (p2, rS), (L, rS)]
    seg = dict(face=0, s1=1, up=2, top=3, dn=4, tail=5)
    cols = {f'HOSE{sfx}_STUBR@DRIVE': round(rS, 5), f'HOSE{sfx}_BEADPOS@DRIVE': p1, f'HOSE{sfx}_BEADR@DRIVE': round(rA, 5),
            f'HOSE{sfx}_BEADW@DRIVE': w, f'HOSE{sfx}_TAILL@DRIVE': round(L - p2, 4)}
    return dict(kind='HOSEB', V=V, endlen=L, seg=seg, cols=cols, thr=f'hose stub {stubOD:g} OD (beaded)', faceR=rS * 0.5, rS=rS, rA=rA,
                w=w, p1=p1, p2=p2, thread=None)


# ---- female ports modelled as a cavity in the DRIVE revolve (2026-09-24, from the Brennan STEP bundle) -------------------
# Female SAE ORB port, measured on BOTH Brennan 6404-08-08 and 6410-12-08-O (they agree): face -> 15deg O-ring chamfer from
# dia 0.813 to dia 0.756 -> 45deg lead-in to the port minor -> minor bore to 0.688 from the face -> 120deg drill point.
ORBF_MEAS = {8: dict(RF=0.4065, RC=0.378, P=0.688, CHANG=15.0),
             # 2026-09-25 (batch 13): Brennan 6404-04-04 / -06-06 / -10-08 / -12-12 / -16-16 / -24-24 and 6410-24-20-O STEPs, measured with
             # tools/measure/ports.py (reproduces the -08 values on both 6404-08-08 and 6410-12-08-O). The O-ring chamfer is 12deg at -04/-06
             # and 15deg from -08 up; the minor-bore depth is 0.906 at -12 and above.
             4: dict(RF=0.245, RC=0.2233, P=0.547, CHANG=12.0), 6: dict(RF=0.309, RC=0.2865, P=0.609, CHANG=12.0),
             10: dict(RF=0.4725, RC=0.4441, P=0.781, CHANG=15.0), 12: dict(RF=0.575, RC=0.538, P=0.906, CHANG=15.0),
             16: dict(RF=0.70, RC=0.663, P=0.906, CHANG=15.0), 20: dict(RF=0.8575, RC=0.8205, P=0.906, CHANG=15.0),
             24: dict(RF=0.983, RC=0.946, P=0.906, CHANG=15.0),
             # 2026-10-18 (genfeat straights): -02 (5/16-24) female ORB port measured on the Brennan 6410-04-02-O STEP with tools/measure/ports.py
             # (same run reproduces the -04 / -08 entries on 6404-04-04 / 6404-08-08 / 6410-12-08-O): O-ring chamfer 12deg from dia 0.360 to 0.3248,
             # minor bore dia 0.270 to 0.468 from the face - single STEP (ASSUMED); no -02 port drill published (OMi / Air-Way / catalog)
             2: dict(RF=0.18, RC=0.1624, P=0.468, CHANG=12.0)}
# Female 37deg JIC port, measured on Brennan 2406-08-08: face -> 45deg countersink from dia 0.755 -> minor bore to 0.375 from
# the face -> 37deg internal seat straight from the minor down to the bore (no flat).
JICF_MEAS = {8: dict(RCS=0.3775, P=0.375),
             # 2026-09-25 (batch 13): Brennan 2406-04-06 / -05-04 / -06-06 / -10-08 / -12-08 / -14-10 / -16-12 / -20-10 / -24-16 / -32-24 STEPs
             # (first dash = the female JIC), measured with tools/measure/ports.py (reproduces the -08 values on 2406-08-08). Same shape at every size:
             # 45deg countersink from RCS, minor bore to P, 37deg seat straight to the bore. (Brennan's minor is 0.002-0.005 above the ASME basic
             # minor at every size, as at -08; the model keeps the basic minor.)
             4: dict(RCS=0.2215, P=0.328), 5: dict(RCS=0.2525, P=0.344), 6: dict(RCS=0.2835, P=0.344), 10: dict(RCS=0.44, P=0.469),
             12: dict(RCS=0.5335, P=0.50), 14: dict(RCS=0.5965, P=0.531), 16: dict(RCS=0.6585, P=0.563), 20: dict(RCS=0.835, P=0.563),
             24: dict(RCS=0.9605, P=0.655), 32: dict(RCS=1.2735, P=0.828),
             # 2026-10-02 (new masters, group NUTS-CAPS): -03 measured on the Brennan 2406-03-04 STEP (user download 2026-10-02) with
             # tools/measure/ports.py (which reproduces every entry above) and the new capnut.py --port walker (same values): 45deg countersink
             # from dia 0.380, minor bore (Brennan 0.334 dia, ASME basic minor 0.3299) to 0.266 from the face, 37deg seat straight to the bore.
             # No 2406 configuration uses it yet (the 2406-03-04 review row is DataStatus MISSING); the 0304-C / 0306 -03 rows do.
             3: dict(RCS=0.19, P=0.266)}


def end_ORBF(dash, sfx, minor, bore=None):
    # minor = Air-Way D3 (the port drill); the chamfers and depth are the Brennan -08 values (ASSUMED single-manufacturer)
    # bore = the through-bore that runs into the port (6410 D / 6404 D1), None = unknown (port keeps its drill point).
    # 2026-10-01 (ORBF-DEEPBORE): on all nine Brennan STEPs with a female ORB port (6404-04-04 / -06-06 / -08-08 / -10-08 / -12-12 / -16-16 /
    # -24-24, 6410-12-08-O / -24-20-O; tools/measure/ports.py + section profile, tools/_out/tier1_20261001/work/ORBF-DEEPBORE/evidence/brennan)
    # the port's minor bore ends at depth P in a 120deg drill point (60deg to the axis) that steps DOWN to a smaller through-bore (bore / minor
    # 0.66 - 0.88): the point is only the step between the two drills. When the through-bore is at least the port minor (Air-Way prints D = D3
    # on 11 6410 rows and D1 = D3 on 6404-06-08) that step has no height: the cavity stops flat at the minor-bore bottom (DRILLANG 90 = no drill
    # point) and the through-bore carries on from there at the same diameter. Brennan does the same on those sizes: its TFA catalog (page 16,
    # 6410-O, column B DRILL) gives the through drill EQUAL to its port minor, e.g. 6410-10-04-O 0.391, -16-08-O 0.689, -20-12-O 0.981,
    # -20-16-O / -24-16-O 1.231, -24-12-O 0.980, -32-24-O 1.794 (minors measured on the Brennan STEPs: 0.389 0.689 0.980 1.231 1.794).
    # Same sketch topology, so it is a per-configuration table value; the 60deg point would have run past the male tip on 6410-20-16-O and to
    # within 0.02 of it on -20-12 / -24-16 (blocked before).
    if dash not in ORBF_MEAS: raise KeyError(f'female ORB port geometry not measured for -{dash:02d} (no Brennan STEP with that port)')
    m = ORBF_MEAS[dash]; thr = ORB_THR[dash]; P_ = 1 / tpi_of(thr); rmin = minor / 2
    if rmin >= m['RC'] - 0.005: raise AssertionError(f'port drill {minor} does not fit inside the O-ring chamfer (dia {2 * m["RC"]:.4f})')
    c1 = (m['RF'] - m['RC']) / math.tan(math.radians(m['CHANG'])); c2 = c1 + (m['RC'] - rmin)
    apex60 = m['P'] + rmin / TAN60                                    # where the 120deg drill point would end on the axis
    deep = bore is not None and bore >= minor - 1e-6
    drill = 90.0 if deep else 60.0; apex = m['P'] if deep else apex60
    VG = [(0, m['RF']), (c1, m['RC']), (c2, rmin), (m['P'], rmin), (apex, 0)]
    cols = {f'ORBF{sfx}_FACER@DRIVE': m['RF'], f'ORBF{sfx}_CHAMANG@DRIVE': m['CHANG'], f'ORBF{sfx}_CHAMR@DRIVE': m['RC'], f'ORBF{sfx}_MINR@DRIVE': round(rmin, 5),
            f'ORBF{sfx}_MINL@DRIVE': round(m['P'] - c2, 4), f'ORBF{sfx}_DRILLANG@DRIVE': drill,
            f'HELIXDIA@HELIXSK_{sfx}': minor, f'HEIGHT@HELIX_{sfx}': m['P'], f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': round(rmin, 5), f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    axnote = (f'female ORB port DEEP BORE (2026-10-01): through-bore {bore} >= port minor {minor} -> port drilled through, NO 120deg drill point '
              f'(ORBF{sfx}_DRILLANG 90): the minor bore ends flat at the measured port depth {m["P"]} and the through-bore carries on at the same diameter; '
              f'thread length unchanged (= the measured port depth) (ASSUMPTION - the nine Brennan STEPs with a female ORB port, 6404-04/-06/-08/-10/-12/-16/-24 '
              f'and 6410-12-08-O / -24-20-O, all have a through-bore SMALLER than the port minor, joined by the 120deg drill point; the Brennan TFA catalog '
              f'p16 (6410-O, B DRILL) gives the through drill = the port minor on the short reducers, i.e. drilled through; no Brennan STEP of such a part yet)') if deep else None
    if dash == 2:
        # 2026-10-18 (genfeat straights): the -02 port is measured on one Brennan STEP and has no published port drill - logged on every row using it
        n02_ = ('female -02 ORB port (5/16-24): O-ring chamfer 12deg from dia 0.360 to 0.3248 and minor-bore depth 0.468 measured on the Brennan '
                '6410-04-02-O STEP only (tools/measure/ports.py; ASSUMED, single STEP); port drill D3 = the minor bore measured there (0.270) - no '
                'OMi / Air-Way / catalog value for the -02 port drill')
        axnote = (axnote + '; ' + n02_) if axnote else n02_
    return dict(kind='ORBF', V=[], VG=VG, cav=True, endlen=0.0, seg=dict(face=0), cols=cols, thr=thr + ' (female ORB port)', faceR=None,
                td=minor, P1=apex, m=m, c1=c1, c2=c2, rmin=rmin, deep=deep, drill=drill, apex60=apex60, axnote=axnote,
                thread=dict(type='HELIX', r=rmin, height=m['P'], pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


def end_JICF(dash, sfx):
    # female 37deg JIC port: thread minor = ASME B1.1 basic minor of the JIC thread; countersink, depth and seat from Brennan 2406-08-08
    if dash not in JICF_MEAS: raise KeyError(f'female JIC port geometry not measured for -{dash:02d} (no Brennan 2406 STEP of that size)')
    m = JICF_MEAS[dash]; e = JIC[dash]; P_ = 1 / tpi_of(e['thr']); rmin = round((e['TM'] - 1.082532 * P_) / 2, 5)
    cs = m['RCS'] - rmin; apex = m['P'] + rmin / TAN37
    VG = [(0, m['RCS']), (cs, rmin), (m['P'], rmin), (apex, 0)]
    cols = {f'JICF{sfx}_CSR@DRIVE': m['RCS'], f'JICF{sfx}_MINR@DRIVE': rmin, f'JICF{sfx}_MINL@DRIVE': round(m['P'] - cs, 4),
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': m['P'], f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    return dict(kind='JICF', V=[], VG=VG, cav=True, endlen=0.0, seg=dict(face=0), cols=cols, thr=e['thr'] + ' (female 37deg JIC)', faceR=None,
                td=2 * rmin, P1=apex, m=m, cs=cs, rmin=rmin,
                thread=dict(type='HELIX', r=rmin, height=m['P'], pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


# Female 37deg JIC SWIVEL end, sectioned (OpenCascade plane section through the leg axis) on the Brennan 6500-04-04-FG,
# 6500-08-08-FG, 6500-12-12-FG and 6500-16-16-FG STEPs (one solid each: nut and body fused).  All axial values are
# measured FROM THE NUT FACE:
#   HEXL  nut hex length (face -> foot of the rear 45deg hex chamfer)      SKF  skirt radius at the front (after the fillet)
#   SKS   end of the 8deg skirt taper                                     SKR  skirt radius behind the taper (crimp zone)
#   NUTL  nut rear face                                                   NECKR body neck radius behind the nut
#   BODYS body face (forged-arm end) = where the body starts behind the nut
#   MINR  thread minor radius (= ASME B1.1 basic minor at all 4 sizes)    TE   end of the thread minor
#   RELR  relief counterbore radius (45deg from the minor)               FLOOR floor of the slot around the nose
#   NOSER nose outer radius   NOSETIP_B Brennan nose tip (seat mouth plane)   SEATR seat mouth radius (37deg seat to the bore)
#   countersink from the thread major at 50deg to the minor (all 4 sizes)
SWIV_MEAS = {
    4:  dict(AF=0.5625, HEXL=0.3268, SKF=0.2796, SKS=0.509, SKR=0.2574, NUTL=0.649, NECKR=0.1465, BODYS=0.685,
             MINR=0.1917, TE=0.2867, RELR=0.235, FLOOR=0.5243, NOSER=0.1845, NOSETIP_B=0.35, SEATR=0.145),
    8:  dict(AF=0.875, HEXL=0.4499, SKF=0.4361, SKS=0.647, SKR=0.4108, NUTL=0.827, NECKR=0.292, BODYS=0.885,
             MINR=0.3412, TE=0.3567, RELR=0.3925, FLOOR=0.6723, NOSER=0.34, NOSETIP_B=0.43, SEATR=0.2825),
    12: dict(AF=1.25, HEXL=0.5998, SKF=0.6237, SKS=0.847, SKR=0.5928, NUTL=1.047, NECKR=0.417, BODYS=1.089,
             MINR=0.4862, TE=0.4851, RELR=0.549, FLOOR=0.8623, NOSER=0.481, NOSETIP_B=0.57, SEATR=0.4225),
    16: dict(AF=1.5, HEXL=0.6564, SKF=0.749, SKS=0.909, SKR=0.727, NUTL=1.139, NECKR=0.5485, BODYS=1.175,
             MINR=0.6112, TE=0.5252, RELR=0.665, FLOOR=0.9544, NOSER=0.604, NOSETIP_B=0.60, SEATR=0.5475),
    # 2026-09-25 (batch 13): Brennan 6500-05-05 / -06-06 / -10-10 / -20-20 / -24-24 / -32-32-FG STEPs (user download 2026-09-25), measured with
    # tools/measure/swiv.py - the same extractor reproduces the -04/-08/-12/-16 rows above exactly (every value). The skirt taper is
    # 6.2deg at -20 and 3.8deg at -32 (8deg at the other sizes); the thread minor = ASME B1.1 basic minor at every size again.
    5:  dict(AF=0.625, HEXL=0.3826, SKF=0.3113, SKS=0.570, SKR=0.2912, NUTL=0.715, NECKR=0.178, BODYS=0.746,
             MINR=0.2229, TE=0.3165, RELR=0.2675, FLOOR=0.5901, NOSER=0.218, NOSETIP_B=0.382, SEATR=0.175),
    6:  dict(AF=0.6875, HEXL=0.3876, SKF=0.3428, SKS=0.590, SKR=0.3224, NUTL=0.735, NECKR=0.206, BODYS=0.785,
             MINR=0.2512, TE=0.3197, RELR=0.2925, FLOOR=0.5953, NOSER=0.246, NOSETIP_B=0.38, SEATR=0.215),
    10: dict(AF=1.0, HEXL=0.5265, SKF=0.4988, SKS=0.754, SKR=0.4758, NUTL=0.944, NECKR=0.347, BODYS=0.985,
             MINR=0.3989, TE=0.4364, RELR=0.4475, FLOOR=0.7794, NOSER=0.394, NOSETIP_B=0.50, SEATR=0.3375),
    20: dict(AF=2.0, HEXL=0.5375, SKF=0.9889, SKS=0.925, SKR=0.949, NUTL=1.145, NECKR=0.68, BODYS=1.26,
             MINR=0.7674, TE=0.4724, RELR=0.88, FLOOR=0.9556, NOSER=0.766, NOSETIP_B=0.64, SEATR=0.7025),
    24: dict(AF=2.25, HEXL=0.7063, SKF=1.1134, SKS=1.09, SKR=1.0504, NUTL=1.32, NECKR=0.776, BODYS=1.41,
             MINR=0.8924, TE=0.5674, RELR=1.01, FLOOR=1.065, NOSER=0.8885, NOSETIP_B=0.72, SEATR=0.81),
    32: dict(AF=2.875, HEXL=0.862, SKF=1.4242, SKS=1.34, SKR=1.3936, NUTL=1.61, NECKR=1.0785, BODYS=1.67,
             MINR=1.2049, TE=0.7399, RELR=1.325, FLOOR=1.4202, NOSER=1.198, NOSETIP_B=0.95, SEATR=1.1175),
}
SW_CSANG = 50.0; SW_RELANG = 45.0; SW_SEATANG = 37.0
SWIV_ASSUME = ('female 37deg JIC SWIVEL end, sectioned on the Brennan 6500-04/-05/-06/-08/-10/-12/-16/-20/-24/-32-FG STEPs (one per swivel size): swivel nut hex = Air-Way C3 over the measured nut hex length, '
               'round skirt (measured radii and taper) to the measured nut rear face, measured neck radius to the body face; nut thread = ASME B1.1 basic minor '
               '(= Brennan at every measured size) with a straight helical UN-2B thread over the measured length, 50deg countersink from the thread major, 45deg relief to the '
               'measured counterbore; nose inside the nut (measured OD and slot-floor depth), nose tip at Air-Way L minus the to-seat length (Brennan within 0.01), '
               '37deg internal seat from the measured mouth dia straight to the bore; NUT AND BODY ARE ONE SOLID (the Brennan STEPs are one solid too) - the '
               'nut/body joint (collar, crimp dimples, rear undercut), hex chamfers and fillets are NOT modelled; the body hex stops at the measured body-face '
               'position of the 6500 forged arm (ASSUMED for a straight body); single manufacturer (Brennan) - every swivel size -04..-32 except -14 measured')


def end_JICSW(dash, sfx, s_nt, nut_af):
    # s_nt = nut face -> nose tip (seat mouth) from Air-Way (L to the nut face minus L to the seat); nut_af = Air-Way C3
    if dash not in SWIV_MEAS: raise KeyError(f'female JIC swivel end not measured for -{dash:02d} (no Brennan 6500 STEP of that size)')
    m = SWIV_MEAS[dash]; e = JIC[dash]; P_ = 1 / tpi_of(e['thr'])
    rmin = round((e['TM'] - 1.082532 * P_) / 2, 5)
    assert abs(rmin - m['MINR']) < 0.002, (dash, rmin, m['MINR'])
    if abs(nut_af - m['AF']) > 0.007: raise AssertionError(f'Air-Way nut hex C3 {nut_af} differs from the Brennan nut {m["AF"]} for -{dash:02d}')
    rcs = e['TM'] / 2; cs = (rcs - rmin) / math.tan(math.radians(SW_CSANG))
    rcb = m['RELR']; scb0 = m['TE'] + (rcb - rmin) / math.tan(math.radians(SW_RELANG))
    Rn = nut_af / math.sqrt(3)
    apex = s_nt + m['SEATR'] / TAN37
    VO = [(0.0, Rn), (m['HEXL'], Rn), (m['HEXL'], m['SKF']), (m['SKS'], m['SKR']), (m['NUTL'], m['SKR']), (m['NUTL'], m['NECKR']), (m['BODYS'], m['NECKR'])]
    VG = [(0.0, rcs), (cs, rmin), (m['TE'], rmin), (scb0, rcb), (m['FLOOR'], rcb), (m['FLOOR'], m['NOSER']), (s_nt, m['NOSER']), (s_nt, m['SEATR']), (apex, 0.0)]
    # geometric sanity (all must hold for the measured sizes)
    assert m['SKF'] < nut_af / 2 and m['SKR'] < nut_af / 2, 'skirt above the nut flats'
    assert m['FLOOR'] > s_nt + 0.05 and m['NUTL'] > m['FLOOR'] + 0.05 and m['BODYS'] > m['NUTL'], 'axial order'
    assert m['SEATR'] < m['NOSER'] < rcb and rmin < rcb, 'radial order'
    cols = {f'SW{sfx}_BODYS@DRIVE': m['BODYS'], f'SW{sfx}_NECKR@DRIVE': m['NECKR'], f'SW{sfx}_NUTL@DRIVE': m['NUTL'],
            f'SW{sfx}_SKIRTR@DRIVE': m['SKR'], f'SW{sfx}_SKIRTL@DRIVE': round(m['NUTL'] - m['SKS'], 4), f'SW{sfx}_SKIRTFR@DRIVE': m['SKF'],
            f'SW{sfx}_NUTHEXL@DRIVE': m['HEXL'], f'SW{sfx}_NUTR@DRIVE': round(Rn, 5), f'SW{sfx}_CSR@DRIVE': round(rcs, 5),
            f'SW{sfx}_MINR@DRIVE': rmin, f'SW{sfx}_THDL@DRIVE': round(m['TE'] - cs, 4), f'SW{sfx}_RELR@DRIVE': rcb,
            f'SW{sfx}_FLOOR@DRIVE': m['FLOOR'], f'SW{sfx}_NOSER@DRIVE': m['NOSER'], f'SW{sfx}_NOSETIP@DRIVE': round(s_nt, 4),
            f'SW{sfx}_SEATR@DRIVE': m['SEATR'],
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': m['TE'], f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    return dict(kind='JICSW', V=[], VO=VO, VG=VG, cav=True, endlen=m['BODYS'], seg=dict(face=0), cols=cols,
                thr=e['thr'] + ' (female 37deg JIC swivel)', faceR=None, td=2 * rmin, P1=apex, m=m, cs=cs, scb0=scb0, rmin=rmin, rcs=rcs,
                Rn=Rn, nut_af=nut_af, s_nt=s_nt, dash=dash, bore_to=s_nt, open_at=s_nt, bore_rmax=m['SEATR'] - 0.01,
                thread=dict(type='HELIX', r=rmin, height=m['TE'], pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


# 2026-10-01 (6565-CAVITY): where TWO female JIC swivel ends face each other (6565), each 37deg seat cone is drawn only down to
# its through-bore radius and closed there by a radial line to the axis, instead of running on to its apex on the axis.
# Brennan 6500-04/-05/-06/-08/-10/-12/-16/-20/-24/-32-FG STEPs (swivel leg sectioned with measure/swiv.py + prof.py, 2026-10-01):
# the 37.00deg seat ends exactly at the through-bore at every size, no flat; the Brennan TFA catalog p.18 (6565 FJS-FJS straight)
# draws the same (seat cones running into one through-bore, B1/B2 DRILL = the 6500 STEP bores). The finished part is unchanged
# (the bore cuts remove the same core as before); only the two apexes no longer need room on the axis - they crossed at
# 6565-20-20 / -24-24 (and -32-32), which blocked those rows.
SEAT_TO_BORE_ASSUME = ('both swivel seats: the 37deg seat cone ends at the through-bore (D1 at End A, D2 at End B) with no flat, as measured on the '
                       'Brennan 6500-04..-32-FG swivel legs (all 10 sizes, 2026-10-01) and as drawn in the Brennan TFA catalog p.18 for 6565 '
                       '(no Brennan 6565 STEP - ASSUMED for the double swivel); the DRIVE sketch draws each seat cone down to the bore radius '
                       '(SWA_SEATENDR / SWB_SEATENDR = D1/2 / D2/2) and closes it radially to the axis; the bore cuts remove the core between the two seats')


def trim_seat_at_bore(E, rb):
    # cut the swivel cavity outline VG at the through-bore radius rb: ... nose tip (s_nt, SEATR) -> (x_end, rb) -> (x_end, 0)
    m = E['m']
    assert E['kind'] == 'JICSW' and 0 < rb < m['SEATR'] and E['VG'][-2] == (E['s_nt'], m['SEATR']) and E['VG'][-1][1] == 0.0, 'not an untrimmed JIC swivel'
    x_end = E['s_nt'] + (m['SEATR'] - rb) / TAN37
    E['VG'] = E['VG'][:-1] + [(x_end, rb), (x_end, 0.0)]
    E['apex'] = E['P1']; E['P1'] = x_end; E['seat_end'] = x_end; E['seat_endr'] = rb
    return x_end


# Female NPSM SWIVEL end (pipe swivel union), sectioned on the Brennan 1404-08-08 STEP (one solid: nut and body fused).
# NUT values are measured from the NUT FACE; STEM values from the STEM TIP (the stem belongs to the body):
#   nut: hex length, 14deg skirt cone from the flats to the lip, lip radius, nut rear face; 45deg countersink, thread minor
#        (= ASME B1.20.1 NPSM internal minor 0.7594 min), thread length, 45deg relief, relief counterbore and its end (lip front face)
#   stem: 30deg male cone to the tip, stem OD, neck radius, body face 0.48 behind the tip
# The nut face sits at Air-Way W and the stem tip at Air-Way L (user decision 2026-09-24: follow Air-Way; Air-Way W - L = 0.33
# at every -08 row, Brennan 0.28 - so the modelled nut sits 0.05 further out than Brennan's).
NPSM_MEAS = {8: dict(AF=1.0, HEXL=0.40, SKF=0.5, SKS=0.58, SKR=0.455, NUTL=0.72, CSR=0.4115, MINR=0.3795, TE=0.388,
                     RELR=0.4115, RB0=0.42, CBR=0.4425, CBEND=0.595, NECKR=0.304, BODY_TO_TIP=0.48, CONEL=0.1542,
                     STEMR=0.37, TIPR=0.281, TIP_B=0.28, thr='1/2-14 NPSM', TPI=14.0),
             # 2026-09-25 (batch 13): Brennan 1404-02-02 / -04-04 / -06-06 / -12-12 / -16-16 / -20-20 / -24-24 / -32-32 STEPs, measured with
             # tools/measure/npsm.py (reproduces every -08 value above exactly). Nut hex = the Brennan nut (Air-Way C(2) must agree, checked
             # per row). The skirt cone is 14deg at -08 and flatter at the large sizes (7.6deg at -20). Thread minor = the Brennan value.
             2: dict(AF=0.5625, HEXL=0.20, SKF=0.281, SKS=0.28, SKR=0.2496, NUTL=0.38, CSR=0.1984, MINR=0.182, TE=0.1736,
                     RELR=0.1984, RB0=0.19, CBR=0.2275, CBEND=0.3066, NECKR=0.129, BODY_TO_TIP=0.28, CONEL=0.0961,
                     STEMR=0.1725, TIPR=0.117, TIP_B=0.14, thr='1/8-27 NPSM', TPI=27.0),
             4: dict(AF=0.6875, HEXL=0.28, SKF=0.345, SKS=0.43, SKR=0.3146, NUTL=0.54, CSR=0.263, MINR=0.2405, TE=0.2875,
                     RELR=0.263, RB0=0.31, CBR=0.29, CBEND=0.4459, NECKR=0.1825, BODY_TO_TIP=0.39, CONEL=0.1325,
                     STEMR=0.225, TIPR=0.1485, TIP_B=0.19, thr='1/4-18 NPSM', TPI=18.0),
             6: dict(AF=0.875, HEXL=0.32, SKF=0.4375, SKS=0.455, SKR=0.4056, NUTL=0.58, CSR=0.331, MINR=0.306, TE=0.29,
                     RELR=0.331, RB0=0.315, CBR=0.36, CBEND=0.4707, NECKR=0.2465, BODY_TO_TIP=0.41, CONEL=0.1429,
                     STEMR=0.2935, TIPR=0.211, TIP_B=0.22, thr='3/8-18 NPSM', TPI=18.0),
             12: dict(AF=1.25, HEXL=0.40, SKF=0.625, SKS=0.61, SKR=0.5694, NUTL=0.745, CSR=0.517, MINR=0.485, TE=0.393,
                      RELR=0.517, RB0=0.425, CBR=0.5625, CBEND=0.6189, NECKR=0.389, BODY_TO_TIP=0.45, CONEL=0.1533,
                      STEMR=0.4635, TIPR=0.375, TIP_B=0.33, thr='3/4-14 NPSM', TPI=14.0),
             16: dict(AF=1.5, HEXL=0.50, SKF=0.75, SKS=0.725, SKR=0.7098, NUTL=0.90, CSR=0.6465, MINR=0.6055, TE=0.469,
                      RELR=0.6465, RB0=0.51, CBR=0.67, CBEND=0.7447, NECKR=0.525, BODY_TO_TIP=0.59, CONEL=0.1827,
                      STEMR=0.59, TIPR=0.4845, TIP_B=0.35, thr='1-11 1/2 NPSM', TPI=11.5),
             20: dict(AF=1.875, HEXL=0.56, SKF=0.9375, SKS=0.805, SKR=0.9048, NUTL=1.00, CSR=0.819, MINR=0.7775, TE=0.5385,
                      RELR=0.819, RB0=0.58, CBR=0.85, CBEND=0.8141, NECKR=0.695, BODY_TO_TIP=0.62, CONEL=0.2208,
                      STEMR=0.768, TIPR=0.6405, TIP_B=0.42, thr='1 1/4-11 1/2 NPSM', TPI=11.5),
             24: dict(AF=2.125, HEXL=0.563, SKF=1.0625, SKS=0.93, SKR=1.027, NUTL=1.125, CSR=0.9385, MINR=0.897, TE=0.5445,
                      RELR=0.9385, RB0=0.586, CBR=0.9675, CBEND=0.9392, NECKR=0.8075, BODY_TO_TIP=0.745, CONEL=0.2234,
                      STEMR=0.879, TIPR=0.75, TIP_B=0.42, thr='1 1/2-11 1/2 NPSM', TPI=11.5),
             32: dict(AF=2.625, HEXL=0.563, SKF=1.31, SKS=0.93, SKR=1.2766, NUTL=1.125, CSR=1.1755, MINR=1.134, TE=0.5435,
                      RELR=1.1755, RB0=0.585, CBR=1.2125, CBEND=0.9385, NECKR=1.0215, BODY_TO_TIP=0.745, CONEL=0.1706,
                      STEMR=1.0985, TIPR=1.0, TIP_B=0.42, thr='2-11 1/2 NPSM', TPI=11.5)}
NPSM_CSANG = 45.0; NPSM_RELANG = 45.0; NPSM_CONEANG = 30.0
NPSM_ASSUME = ('female NPSM SWIVEL end, sectioned on the Brennan 1404 STEPs (one per NPSM size -02/-04/-06/-08/-12/-16/-20/-24/-32): nut hex = Air-Way C(2) (must equal the Brennan nut, checked per row) over the measured hex length, '
               'skirt cone and lip to the measured nut rear face; nut thread = straight NPSM of that size, minor = the Brennan value (-08: 0.759 = ASME B1.20.1 NPSM '
               'internal minor 0.7594 min), helical 60deg thread 0.8P deep over the measured length, 45deg countersink and 45deg relief to the measured counterbore; body stem '
               'with the measured 30deg male cone, OD and tip radius, neck behind the nut, body face at the measured distance behind the stem tip (Brennan); NUT FACE AT AIR-WAY W AND '
               'STEM TIP AT AIR-WAY L (user decision 2026-09-24: follow Air-Way - at -08 Air-Way W-L 0.33 vs Brennan 0.28, so the nut sits 0.05 further out than on the '
               'Brennan part); NUT AND BODY ARE ONE SOLID (Brennan STEPs are one solid too) - the nut/collar joint, the rear undercut under the nut lip, the slot '
               'at the collar, hex chamfers and fillets are NOT modelled; single manufacturer (Brennan)')


def end_NPSMSW(dash, sfx, s_tip, nut_af):
    # s_tip = nut face -> stem tip (Air-Way W - L); nut_af = Air-Way C(2)
    if dash not in NPSM_MEAS: raise KeyError(f'female NPSM swivel end not measured for -{dash:02d} (no Brennan 1404 STEP of that size)')
    m = NPSM_MEAS[dash]; P_ = 1 / m['TPI']
    if abs(nut_af - m['AF']) > 0.007: raise AssertionError(f'Air-Way nut hex C(2) {nut_af} differs from the Brennan nut {m["AF"]} for -{dash:02d}')
    Rn = nut_af / math.sqrt(3); cs = (m['CSR'] - m['MINR']) / math.tan(math.radians(NPSM_CSANG))
    # 2026-09-25: Air-Way prints the nut hex to 2 decimals; where the measured skirt front sits at most 0.002 above the Air-Way flats
    # (-02: skirt 0.281 vs 0.56/2) it is drawn AT the flats radius (the difference is below the print rounding)
    m = dict(m)
    if nut_af / 2 < m['SKF'] <= nut_af / 2 + 0.002: m['SKF'] = round(nut_af / 2, 5)
    s_body = s_tip + m['BODY_TO_TIP']; s_cone = s_tip + m['CONEL']
    VO = [(0.0, Rn), (m['HEXL'], Rn), (m['HEXL'], m['SKF']), (m['SKS'], m['SKR']), (m['NUTL'], m['SKR']), (m['NUTL'], m['NECKR']), (s_body, m['NECKR'])]
    VG = [(0.0, m['CSR']), (cs, m['MINR']), (m['TE'], m['MINR']), (m['RB0'], m['RELR']), (m['RB0'], m['CBR']), (m['CBEND'], m['CBR']),
          (m['CBEND'], m['STEMR']), (s_cone, m['STEMR']), (s_tip, m['TIPR']), (s_tip, 0.0)]
    assert m['SKF'] <= nut_af / 2 + 1e-9 and m['SKR'] < m['SKF'], 'skirt above the nut flats'
    if not (m['RB0'] < m['CBEND'] and s_cone < m['CBEND'] - 0.02 and m['NUTL'] < s_body - 0.02 and m['CBEND'] < m['NUTL'] - 0.02):
        raise AssertionError(f'nut/stem axial order broken for W-L {s_tip}')
    # stem cone must stay inside the thread minor where they overlap axially
    for (a_, r_) in ((s_tip, m['TIPR']), (s_cone, m['STEMR'])):
        if a_ < m['TE'] and r_ >= m['MINR'] - 0.005: raise AssertionError('stem inside the nut thread with no clearance')
    cols = {f'NP{sfx}_BODYS@DRIVE': round(s_body, 4), f'NP{sfx}_NECKR@DRIVE': m['NECKR'], f'NP{sfx}_NUTL@DRIVE': m['NUTL'],
            f'NP{sfx}_LIPR@DRIVE': m['SKR'], f'NP{sfx}_LIPL@DRIVE': round(m['NUTL'] - m['SKS'], 4), f'NP{sfx}_SKIRTFR@DRIVE': m['SKF'],
            f'NP{sfx}_NUTHEXL@DRIVE': m['HEXL'], f'NP{sfx}_NUTR@DRIVE': round(Rn, 5), f'NP{sfx}_CSR@DRIVE': m['CSR'],
            f'NP{sfx}_MINR@DRIVE': m['MINR'], f'NP{sfx}_THDL@DRIVE': round(m['TE'] - cs, 4), f'NP{sfx}_RELR@DRIVE': m['RELR'],
            f'NP{sfx}_CBR@DRIVE': m['CBR'], f'NP{sfx}_CBEND@DRIVE': m['CBEND'], f'NP{sfx}_STEMR@DRIVE': m['STEMR'],
            f'NP{sfx}_TIPR@DRIVE': m['TIPR'], f'NP{sfx}_STEMTIP@DRIVE': round(s_tip, 4),
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * m['MINR'], 5), f'HEIGHT@HELIX_{sfx}': m['TE'], f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': m['MINR'], f'APEXR@THDPROF_{sfx}': round(m['MINR'] + 0.8 * P_, 5)}
    return dict(kind='NPSMSW', V=[], VO=VO, VG=VG, cav=True, endlen=round(s_body, 4), seg=dict(face=0), cols=cols,
                thr=m['thr'] + ' (female swivel)', faceR=None, td=2 * m['MINR'], P1=s_tip, m=m, cs=cs, Rn=Rn, nut_af=nut_af, s_tip=s_tip,
                s_cone=s_cone, dash=dash, bore_to=round(s_tip - 0.02, 4), open_at=s_tip, bore_rmax=m['TIPR'] - 0.03,
                thread=dict(type='HELIX', r=m['MINR'], height=m['TE'], pitch=P_, thdh=0.8 * P_, taper=0.0, taperOut=False, apexOut=True))


# SAE code 61 FLANGE HEAD end (1700), sectioned on the Brennan 1700-08-08, 1700-12-12 and 1700-24-24 STEPs: head thickness,
# face O-ring groove inner/outer radius and depth, by FLANGE size. Head OD = Air-Way O (Brennan agrees: 1.188 / 1.50 / 2.375).
FLG61_MEAS = {8: dict(TH=0.265, GI=0.345, GO=0.5, GD=0.11), 12: dict(TH=0.265, GI=0.47, GO=0.625, GD=0.11), 24: dict(TH=0.315, GI=0.9025, GO=1.0575, GD=0.11),
              # 2026-09-25 (batch 13): Brennan 1700-16-16 / -20-20 / -32-32 STEPs, tools/measure/flange.py (reproduces -08/-12/-24 exactly); head OD 1.75 / 2.00 / 2.812
              16: dict(TH=0.315, GI=0.625, GO=0.78, GD=0.11), 20: dict(TH=0.315, GI=0.72, GO=0.875, GD=0.11), 32: dict(TH=0.375, GI=1.09, GO=1.245, GD=0.11)}
FLG61_ASSUME = ('SAE code 61 flange head: head OD = Air-Way O, head thickness and face O-ring groove (inner/outer dia, depth 0.11) measured on the Brennan '
                '1700-08/-12/-16/-20/-24/-32 STEPs by flange size (single source - SAE J518 not available); body = HEX of Air-Way C over the whole '
                'length between the JIC end and the flange head (ASSUMPTION - user decision 2026-09-24: follow Air-Way; Brennan instead has a round collar of '
                'dia O with two wrench flats and a neck, overall 0.24 longer at -08); bore chamfer at the flange face and hex chamfers NOT modelled; built for '
                'flange sizes -08/-12/-16/-20/-24/-32')


def end_FLG61(dash, sfx, O, neck=None):
    if dash not in FLG61_MEAS: raise KeyError(f'code 61 flange head not measured for -{dash:02d}')
    m = FLG61_MEAS[dash]; rO = O / 2
    if not (m['GO'] < rO - 0.03 and m['GI'] < m['GO'] - 0.05): raise AssertionError(f'O-ring groove does not fit the head (O {O})')
    V = [(0, m['GI']), (m['GD'], m['GI']), (m['GD'], m['GO']), (0, m['GO']), (0, rO), (m['TH'], rO)]
    seg = dict(face=0, gin=1, gbot=2, gout=3, face2=4, head=5)
    cols = {f'FLG{sfx}_GRVIR@DRIVE': m['GI'], f'FLG{sfx}_GRVD@DRIVE': m['GD'], f'FLG{sfx}_GRVOR@DRIVE': m['GO'],
            f'FLG{sfx}_HEADR@DRIVE': round(rO, 5), f'FLG{sfx}_HEADT@DRIVE': m['TH']}
    if neck is not None:
        # 2026-10-18 (A16, genfeat flange): the head on a round neck + 30deg chamfer up to the round collar (the Brennan 1700 / 1800 body)
        return flg_neck_end(dict(kind='FLG61', V=V, endlen=m['TH'], seg=seg, cols=cols, thr=f'SAE code 61 flange -{dash:02d} (O {O:g})',
                                 faceR=(m['GO'] + rO) / 2, m=m, rO=rO, thread=None), sfx, neck)
    return dict(kind='FLG61', V=V, endlen=m['TH'], seg=seg, cols=cols, thr=f'SAE code 61 flange -{dash:02d} (O {O:g})', faceR=(m['GO'] + rO) / 2,
                m=m, rO=rO, thread=None)


# 2026-10-18 (genfeat flange; ported from the unmerged wave-1 group FLANGE62, tools/_out/newmasters_20261002/work/FLANGE62/patch.diff): SAE code 62
# FLANGE HEAD by flange size. GEOMETRY from the Brennan pilot STEPs, measured with tools/measure/flange62.py (validated first: on the Brennan
# 1700-08/-12/-16/-20/-24/-32 STEPs it returns FLG61_MEAS and tools/measure/flange.py exactly): head OD O, head thickness TH, face O-ring groove
# inner / outer radius GI / GO and depth GD. -08: 1800-08-08 (O 1.250, TH 0.305, GI 0.345, GO 0.500, GD 0.110), 1824-08 (1.250 / 0.3051 / 0.3449 /
# 0.500 / 0.1098) and 1804-08-08-FG (1.250 / 0.305 / 0.345 / 0.500 / 0.110) agree to 0.0002 - one manufacturer, so ASSUMED. Only -08 is measured:
# no Brennan STEP with a -12..-32 code 62 head is in 09_STEP_FILES (the Brennan Flange catalog p.8 3300-62 head connector prints those heads, but
# that is another part - Q-TRANSFER-FLG62-HEAD, open).
FLG62_MEAS = {8: dict(O=1.250, TH=0.305, GI=0.345, GO=0.500, GD=0.110)}
FLG62_ASSUME = ('SAE code 62 flange head: head OD, head thickness and face O-ring groove (inner / outer dia, depth) measured by flange size on the Brennan '
                '1800-08-08 / 1824-08 / 1804-08-08-FG STEPs (tools/measure/flange62.py; the three agree to 0.0002; single manufacturer - SAE J518 / ISO 6162-2 '
                'not in the repo); the 0.0088 x 45deg head edge chamfers of 1824-08 and the bore chamfer at the flange face (1800-08-08: 0.0113 x 60deg) are '
                'NOT modelled; built for flange size -08 only (no Brennan STEP with a -12..-32 code 62 head yet)')
# the round collar + two wrench flats + 30deg chamfer + neck body of the Brennan code 61 / code 62 straights (A16 2026-10-18 "do the same as Brennan")
FLG_NECK_ASSUME = ('body behind the JIC end = the Brennan construction (Brennan 1800-08-08 pilot STEP, tools/measure/flange62.py; the Brennan 1700 STEPs '
                   'show the same body): ROUND collar (dia {collar}) carrying TWO wrench flats (across flats {waf}, flats normal to model Y, cut on the '
                   'Right Plane) over the zone {zone} from the collar face, a 30deg chamfer from the collar down to the neck (the flats cut ends where '
                   'the neck starts), the round neck (dia {neckd}) up to the flange head; the neck length is what L leaves (L - JIC end - {zone} - head '
                   'thickness); collar / flats zone / neck / bore from the part\'s own Brennan STEP')
FLG_NECK_CHAMANG = 30      # deg, collar-to-neck chamfer against the neck line: Brennan 1800-08-08 STEP 30.0 (flange62.py); the 1700 own-STEP readings fit it


def flg62_head(dash):
    if dash not in FLG62_MEAS:
        raise KeyError(f'code 62 flange head not measured for -{dash:02d}: needs code 62 head STEP - a Brennan STEP with a -{dash:02d} code 62 head '
                       f'(1824-{dash:02d} plug preferred) measured with tools/measure/flange62.py, or an answer to Q-TRANSFER-FLG62-HEAD (Brennan Flange '
                       f'catalog p.8 3300-62)')
    return FLG62_MEAS[dash]


def flg_neck_end(E, sfx, neck):
    """2026-10-18: append the round neck (radius rN, length NL) and the 30deg chamfer up to the collar radius rB to a flange head end (FLG61 /
    FLG62); the chamfer belongs to this end, so the body line (xa..xb) is the round part of the collar only"""
    rN, NL, rB = neck['rN'], neck['NL'], neck['rB']
    CL = (rB - rN) / math.tan(math.radians(FLG_NECK_CHAMANG)); TH = E['m']['TH']
    E['V'] = E['V'] + [(TH, rN), (TH + NL, rN)]
    E['seg'] = dict(E['seg'], back=6, neck=7, cham=8)
    E['cols'] = dict(E['cols'], **{f'FLG{sfx}_NECKR@DRIVE': round(rN, 5), f'FLG{sfx}_NECKL@DRIVE': round(NL, 8), f'FLG{sfx}_CHAMANG@DRIVE': FLG_NECK_CHAMANG})
    E['endlen'] = TH + NL + CL; E['neck'] = dict(rN=rN, NL=NL, rB=rB, CL=CL)
    return E


def end_FLG62(dash, sfx, neck=None):
    """code 62 flange head end. neck=None: the head steps straight down to the body (plug 1824). neck=dict(rN, NL, rB): head on a round neck that
    rises with a 30deg chamfer to the round collar rB (1800)"""
    m = flg62_head(dash); rO = m['O'] / 2
    if not (m['GO'] < rO - 0.03 and m['GI'] < m['GO'] - 0.05): raise AssertionError(f'O-ring groove does not fit the head (O {m["O"]})')
    V = [(0, m['GI']), (m['GD'], m['GI']), (m['GD'], m['GO']), (0, m['GO']), (0, rO), (m['TH'], rO)]
    seg = dict(face=0, gin=1, gbot=2, gout=3, face2=4, head=5)
    cols = {f'FLG{sfx}_GRVIR@DRIVE': m['GI'], f'FLG{sfx}_GRVD@DRIVE': m['GD'], f'FLG{sfx}_GRVOR@DRIVE': m['GO'],
            f'FLG{sfx}_HEADR@DRIVE': round(rO, 5), f'FLG{sfx}_HEADT@DRIVE': m['TH']}
    E = dict(kind='FLG62', V=V, endlen=m['TH'], seg=seg, cols=cols, thr=f'SAE code 62 flange -{dash:02d} (O {m["O"]:g})', faceR=(m['GO'] + rO) / 2,
             m=m, rO=rO, neck=None, thread=None)
    return flg_neck_end(E, sfx, neck) if neck is not None else E


def flg_neck(r, a, head, L_col, collar_col, zone_col, neck_col, also=()):
    """the neck of a flange end from the row: neck radius, and the neck length L leaves after the JIC end, the flats zone (collar + 30deg
    chamfer) and the head (head = the FLG61_MEAS / FLG62_MEAS entry); the collar radius is the body radius. An empty input cell -> KeyError (row
    skipped with the column named)"""
    for c_ in (L_col, collar_col, zone_col, neck_col) + tuple(also):
        if r.get(c_) is None: raise KeyError(f'row without {c_}')
    je = end_JICM(a, 'A')['endlen']
    # NL to 8 decimals: the neck start (L - TH - NL in the DRIVE sketch) must coincide with the end of the flats cut (START + DEPTH) to 1e-8
    return dict(rN=r[neck_col] / 2, rB=r[collar_col] / 2, NL=round(r[L_col] - je - r[zone_col] - head['TH'], 8))


def end_PLAIN(sfx):
    # plug head: the hex runs to a plain flat face (no port, no thread)
    return dict(kind='PLAIN', V=[], endlen=0.0, seg=dict(face=0), cols={}, thr='plug head', faceR=None, td=0.0, P1=0.0, thread=None)


# ---- 2026-10-02 (new masters, group NUTS-CAPS): JIC CAP NUT 0304-C and JIC BULKHEAD LOCKNUT 0306 -----------------------------------
# Pilots (user downloads, 09_STEP_FILES): Brennan 0304-C-08 and 0306-08, sectioned with tools/measure/capnut.py / locknut.py (walkers
# validated on the twelve Brennan 2406 female JIC ports: they return JICF_MEAS above at every size). Both parts are a hex prism with the
# female JIC thread of their dash; the per-size internal geometry is taken from the Brennan female JIC PORT of the same dash (JICF_MEAS,
# 2406 STEPs) - the pilots show that the cap cavity and the locknut countersinks ARE that port:
#   0304-C-08 cap (L 0.750, hex 0.875): open face -> thread minor 0.6823 (= ASME B1.1 basic minor) to 0.276 -> 0.688 bore to 0.3779 ->
#             37deg seat from r 0.344 down to r 0.1955 at 0.575 -> flat-bottomed pocket dia 0.391 to 0.625 -> flat crown 0.125 thick.
#             Brennan 2406-08-08 port: 0.688 bore to 0.375 -> 37deg seat from r 0.344 down to the 0.391 bore at 0.572 (same seat within
#             0.003; the port has a 45deg countersink, the cap none).
#   0306-08 locknut (W 0.310, hex 1.000): thread minor 0.6824 (basic minor) through, 45deg countersink from dia 0.755 at BOTH faces =
#             the Brennan 2406-08-08 port countersink (dia 0.755) exactly.
#   Both: hex corner chamfers (cap 30deg to the axis from dia 0.86, 0.130 long at each end; locknut 15deg to the face from dia 1.000) and
#   0.002-deep marking recesses on the flats are NOT modelled (library convention: hex end chamfers are not modelled on any master).
CAP_POCKETL = 0.050      # 0304-C-08 STEP: flat-bottomed pocket 0.050 deep below the end of the 37deg seat (one STEP: ASSUMED at every size)
JICBORE = {}             # JIC dash -> the through bore of the matched-dash JIC union 2403-dd-dd (Air-Way D1 == MS51501D, VERIFIED): cap pocket dia
for _r in load_review('2403')[1]:
    _dd = re.findall(r'-(\d\d)', str(_r['$PRP@PartNo']))
    if len(_dd) == 2 and _dd[0] == _dd[1] and _r.get('D1@BORE') is not None: JICBORE.setdefault(int(_dd[0]), _r['D1@BORE'])
# pilot STEP values (capnut.py / locknut.py), compared per row in the generator summary
PILOT_NUTCAP = {'0304-C-08': ('Brennan 0304-C-08 STEP: L 0.750, hex 0.875, thread minor 0.6823 to 0.276 then 0.688 bore to 0.3779, 37deg seat '
                              'to r 0.1955 at 0.575, pocket dia 0.391 to 0.625, crown 0.125; hex corner chamfers 30deg to the axis from dia 0.860 '
                              '(0.130 long) at both ends'),
                '0306-08': ('Brennan 0306-08 STEP: W 0.310, hex 1.000, thread minor 0.6824 through, 45deg countersinks from dia 0.755 (0.036 deep) '
                            'at both faces, hex corner chamfers 15deg to the face from dia 1.000 (0.021 long) at both faces')}
CAP_ASSUME = ('JIC CAP NUT (one piece): L / hex: review table (OMi dimension file = Brennan, one source); closed FLAT crown at End A, hex over '
              'the full length; female 37deg JIC cavity at End B = the Brennan female JIC port of the same dash (JICF_MEAS: minor-bore depth P '
              'measured per size on the Brennan 2406-03..-32 STEPs) WITHOUT its countersink: thread minor = ASME B1.1 basic minor, straight '
              'helical UN-2B thread over P, 37deg seat from the minor at depth P down to the pocket, pocket dia = the bore of the matched-dash '
              'JIC union 2403-dd-dd (Air-Way D1 == MS51501D), flat pocket bottom 0.050 below the seat end, crown = L - pocket bottom '
              '(ASSUMPTION - construction measured on the Brennan 0304-C-08 STEP only: seat start 0.3779 deep vs the 2406-08-08 port 0.375, '
              'pocket 0.391, pocket 0.050, crown 0.125; the 0.688 bore between the thread (to 0.276) and the seat is drawn at the thread '
              'minor, as on every library JIC port); hex corner chamfers (30deg to the axis, 0.130 long at -08) and flats marking NOT modelled')
NUT_ASSUME = ('JIC BULKHEAD LOCKNUT (thin hex nut): thickness / hex: review table (OMi dimension file = Brennan, one source); thread = the JIC '
              'thread of the dash, minor = ASME B1.1 basic minor (= the Brennan 0306-08 STEP), helical UN-2B thread through the whole thickness; '
              '45deg countersink at BOTH faces from the countersink dia of the Brennan female JIC port of the same dash (JICF_MEAS RCS, 2406-03..-32 '
              'STEPs) (ASSUMPTION - equal on the Brennan 0306-08 STEP: dia 0.755 at both faces = 2406-08-08); the DRIVE sketch carries the two '
              'countersinks with a construction core (apex at the End A origin, flat end behind the End B countersink) that the through bore '
              'BORECUT_A (= the thread minor) removes; hex corner chamfers (15deg to the face at -08) and flats marking NOT modelled')


def end_CROWN(sfx):
    # 0304 cap: closed flat crown (a PLAIN end - the hex runs to a flat face); only the thread text differs from a plug head
    return dict(end_PLAIN(sfx), thr='closed cap crown (flat)')


def end_JICCAP(dash, sfx, pkd):
    # female 37deg JIC cap cavity (End B face at x = L): basic-minor thread bore to the port depth P, 37deg seat to the pocket radius,
    # pocket CAP_POCKETL deep, flat bottom on the axis
    if dash not in JICF_MEAS: raise KeyError(f'female JIC port geometry not measured for -{dash:02d}: needs a Brennan STEP with a female -{dash:02d} '
                                             f'JIC thread + seat (BRENNAN_0304-C-{dash:02d} or a 2406-{dash:02d}-xx)')
    if pkd is None: raise KeyError(f'no matched-dash JIC union bore for -{dash:02d} (2403-{dash:02d}-{dash:02d} D1)')
    m = JICF_MEAS[dash]; e = JIC[dash]; P_ = 1 / tpi_of(e['thr']); rmin = round((e['TM'] - 1.082532 * P_) / 2, 5); rpk = round(pkd / 2, 5)
    if not rpk < rmin - 0.02: raise AssertionError(f'cap pocket dia {pkd} not below the thread minor {2 * rmin:.4f}')
    sE = m['P'] + (rmin - rpk) / TAN37; bot = sE + CAP_POCKETL
    VG = [(0.0, rmin), (m['P'], rmin), (sE, rpk), (bot, rpk), (bot, 0.0)]
    cols = {f'JCAP{sfx}_MINR@DRIVE': rmin, f'JCAP{sfx}_MINL@DRIVE': m['P'], f'JCAP{sfx}_PKR@DRIVE': rpk, f'JCAP{sfx}_PKL@DRIVE': CAP_POCKETL,
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': m['P'], f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    return dict(kind='JICCAP', V=[], VG=VG, cav=True, endlen=0.0, seg=dict(face=0), cols=cols, thr=e['thr'] + ' UN-2B (female 37deg JIC cap)',
                faceR=None, td=2 * rmin, P1=bot, m=m, e=e, rmin=rmin, rpk=rpk, seat_end=sE, bottom=bot, dash=dash,
                thread=dict(type='HELIX', r=rmin, height=m['P'], pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


def nut_csk(dash):
    if dash not in JICF_MEAS: raise KeyError(f'female JIC thread countersink not measured for -{dash:02d}: needs a Brennan STEP with a female '
                                             f'-{dash:02d} JIC thread (BRENNAN_0306-{dash:02d} or a 2406-{dash:02d}-xx)')
    e = JIC[dash]; P_ = 1 / tpi_of(e['thr']); rmin = round((e['TM'] - 1.082532 * P_) / 2, 5); rcs = JICF_MEAS[dash]['RCS']
    return e, P_, rmin, rcs, round(rcs - rmin, 5)       # 45deg countersink: axial = radial


def end_NUTCSA(dash, sfx):
    # locknut End A (x = 0): construction core from the origin (axis) to the countersink bottom (cs, rmin), then the 45deg countersink back
    # to the face at (0, rcs); segment 2 = the End A face (the origin lies on it). The through bore removes the core.
    e, P_, rmin, rcs, cs = nut_csk(dash)
    return dict(kind='NUTCSA', V=[(cs, rmin), (0.0, rcs)], endlen=0.0, seg=dict(core=0, csk=1, face=2), faceseg=2,
                cols={f'NUTCS{sfx}_MINR@DRIVE': rmin, f'NUTCS{sfx}_CSR@DRIVE': rcs}, thr=e['thr'] + ' (45deg countersink)', faceR=None,
                td=2 * rmin, P1=cs, e=e, rmin=rmin, rcs=rcs, cs=cs, dash=dash, thread=None)


def end_NUTCSB(dash, sfx, W):
    # locknut End B (x = W): 45deg countersink from the face to the minor, then a flat construction core end down to the axis
    e, P_, rmin, rcs, cs = nut_csk(dash)
    cols = {f'NUTCS{sfx}_CSR@DRIVE': rcs, f'NUTCS{sfx}_MINR@DRIVE': rmin,
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': W, f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    return dict(kind='NUTCSB', V=[], VG=[(0.0, rcs), (cs, rmin), (cs, 0.0)], cav=True, endlen=0.0, seg=dict(face=0), cols=cols,
                thr=e['thr'] + ' UN-2B (locknut thread, through)', faceR=None, td=2 * rmin, P1=cs, e=e, rmin=rmin, rcs=rcs, cs=cs, dash=dash,
                thread=dict(type='HELIX', r=rmin, height=W, pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


def end_BRAZE(sfx, d2, l7):
    return dict(kind='BRAZE', V=[], endlen=0.0, seg=dict(face=0), cols={f'SOCKDIA@POCKET_{sfx}': d2, f'DEPTH@POCKETCUT_{sfx}': l7},
                thr='braze socket', faceR=None, td=d2, P1=l7, thread=None)


ORB_THR = {2: '5/16-24', 3: '3/8-24', 4: '7/16-20', 5: '1/2-20', 6: '9/16-18', 8: '3/4-16', 10: '7/8-14', 12: '1 1/16-12', 14: '1 3/16-12', 16: '1 5/16-12', 20: '1 5/8-12', 24: '1 7/8-12', 32: '2 1/2-12'}

# ---- topology specs ----------------------------------------------------------------------
SPEC = {
 '5000': dict(name='Hexagon Pipe Coupling', L='L@DRIVE', hex='CHEX@HEX',
              A=lambda r, a, b: end_NPTFF(a, 'A', r['TAPDRILL1@BORE']), B=lambda r, a, b: end_NPTFF(b, 'B', r['TAPDRILL2@BORE']),
              bore=('meet', None, None), ref='5000-08-08',
              assume='female NPTF drill depth = MS51503 P1 max per pipe dash (2405 table); Brennan 5405-08-08 STEP (2026-09-23) confirms 1/2 NPTF port drill depth 0.900 = MS51503 P1 max (VERIFIED for -08 only; thread taper depth in that STEP is 0.750, tap drill dia 0.718, drill point 120 deg); the two drill holes are cut to max(P1, L/2+0.005) so the coupling is through (ASSUMPTION); each helical thread is cut to min(P1, L/2) (ASSUMPTION - for -08 this equals the Brennan thread depth 0.75); hex spans the full length'),
 '5404': dict(name='Hexagon Pipe Nipple', L='L@DRIVE', hex='HEXB@HEX',
              A=lambda r, a, b: end_NPTFM(a, 'A', r['NPTFA_ENDL@DRIVE']), B=lambda r, a, b: end_NPTFM(b, 'B', r['NPTFB_ENDL@DRIVE']),
              bore=('mid', 'D1@BORE', 'D2@BORE'), ref='5404-08-08',
              assume='NPTF male ends per ASME B1.20.3 (tip = E0+0.8P, cone L2 at 1.7899 deg) + Brennan-measured end length (5404 table); bore step at the hex mid-plane (ASSUMPTION, as 2403/6400)'),
 '5405': dict(name='Pipe Adapter (male NPTF x female NPTF)', L='L@DRIVE', hex='CHEX@HEX',
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_NPTFF(b, 'B', r['TAPDRILL@BORE']),
              bore=('A_to_pocket', 'D@BORE', None), ref='5405-08-08', bore_step_ok=True,
              assume='NPTF male end per ASME B1.20.3 with the 5404 Brennan-measured end length for the same dash (ASSUMPTION); female drill depth = MS51503 P1 max per pipe dash (2405 table), thread cut to full drill depth (ASSUMPTION); Brennan 5405-08-08 STEP (2026-09-23) confirms 1/2 NPTF port drill depth 0.900 = MS51503 P1 max (VERIFIED for -08 only; thread taper depth in that STEP is 0.750, tap drill dia 0.718, drill point 120 deg); bore D runs from the male tip to the pocket bottom'),
 '6401': dict(name='Straight Thread (ORB) x Male Pipe Adapter', L='L29@DRIVE', hex='HEXB@HEX',
              A=lambda r, a, b: end_ORBM(a, 'A'), B=lambda r, a, b: end_NPTFM(b, 'B', r['NPTF_ENDL@DRIVE']),
              bore=('mid', 'D3@BORE', 'D4@BORE'), ref='6401-08-08-O',
              assume='ORB end: thread length + groove from the 6401 review table (ORD-5700 groove, measured thread length; no tip chamfer modelled); NPTF male per ASME B1.20.3 + measured end length; bore step at hex mid-plane (ASSUMPTION)'),
 '6405': dict(name='Straight Thread (ORB) x Female Pipe Adapter', L='L31@DRIVE', hex='HEXB@HEX',
              A=lambda r, a, b: end_ORBM(a, 'A'), B=lambda r, a, b: end_NPTFF(b, 'B', r['TAPDRILL@BORE_A']),
              bore=('A_to_pocket', 'D3@BORE', None), ref='6405-08-08-O', p1col='FPT_P1@DRIVE',
              assume='ORB end as 6401; female drill depth = FPT_P1 from the review table (MS51503 P1 max), thread cut to full drill depth (ASSUMPTION); Brennan 5405-08-08 STEP (2026-09-23) confirms 1/2 NPTF port drill depth 0.900 = MS51503 P1 max (VERIFIED for -08 only; thread taper depth in that STEP is 0.750, tap drill dia 0.718, drill point 120 deg); bore D3 from the ORB tip to the pocket bottom'),
 '2408': dict(name='Male Plug (37 deg JIC)', L='L3@DRIVE', hex='HEXB@HEX', single=True,
              A=lambda r, a, b: end_PLAIN('A'), B=lambda r, a, b: end_JICM(b, 'B'),
              bore=('B_blind', 'HOLE@BORE', None), ref='2408-08-H', hole_rule=True,
              assume='JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L3/hex: Air-Way == MS51518D; plug head = hex to a plain flat face (Brennan 2408-08 STEP: hex 0.283 long = L3 - JIC end length, 75deg chamfers not modelled); '
                     'HOLLOW (-H) configs: blind hole HOLE from the JIC tip to depth = JIC end length - 0.020 (ASSUMPTION - measured on the Brennan 2408-08 STEP only: 0.391 hole, full diameter to 0.637 = 0.657 - 0.020, 120deg drill point not modelled); SOLID configs: hole feature suppressed'),
 '6408': dict(name='ORB Hex Head Plug', L='L@DRIVE', hex='HEXB@HEX', single=True,
              A=lambda r, a, b: end_ORBM(a, 'A', r), B=lambda r, a, b: end_PLAIN('B'),
              bore=('A_blind', 'HOLE@BORE', None), ref='6408-08-O-H',
              exclude=r'^6408-HHP-', exclude_why='socket-head (hollow hex) ORB plug: built by SPEC 6408HHP (2026-10-02), never as a hex-head plug',
              assume='ORB end: thread length + groove from the 6408 review table (SAE J1926 plug end; no tip chamfer modelled) - Brennan 6408-08-O / 6408-20-O STEPs: identical ORB ends; '
                     'L / hex: Air-Way (Brennan -08 / -20 STEPs agree: L 0.800 / 1.200, hex 0.875 / 1.875); plug head = hex to a plain flat face (hex end chamfers not modelled); '
                     'HOLLOW (-H) configs = the OMi 6408-xx-O cored plug: blind hole HOLE (Air-Way; Brennan 0.422 / 1.093) drilled from the ORB tip, full diameter to the ORB end length + '
                     '0.020 (-08) / 0.040 (-20) MEASURED on the Brennan STEPs, other sizes interpolated in proportion to the dash (ASSUMPTION); 120deg drill point not modelled; '
                     'SOLID configs (-02/-03/-05: the only plug Air-Way lists there; -04: OMi 6408-04-O-SLD): hole feature suppressed'),
 '0318': dict(name='37 deg JIC Tube Nut', L='L1@DRIVE', hex='CHEX@HEX', single=True,
              A=lambda r, a, b: end_UNFF(a, 'A', r['THDMAJ_B@DRIVE'], r['$PRP@Threads'].split(' (')[0]), B=lambda r, a, b: end_PLAIN('B'),
              bore=('A_to_pocket', lambda r, a, b: MS51531[a][2], None), ref='0318-08', nut=True,
              assume='L1 / hex / thread: Air-Way; internal: MS51531D (Nut, Tube Coupling, 37 Degree Flared) - tube bore D1, internal shoulder at I1 from the thread face, thread length J1 (full thread min); '
                     'thread pocket = ASME B1.1 basic minor diameter (D - 1.082532P), helical 60deg thread from the minor to the basic major (no taper); Brennan 0318-08 STEP: shoulder at 0.723 = I1, bore 0.568 = D1, L 0.850 (VERIFIED -08 only); '
                     'hex over the full length, 30deg end chamfers and the 45deg thread countersink NOT modelled; no internal flare cone (none on MS51531D or the Brennan STEP)'),
 '5406': dict(name='Pipe Reducer Bushing (male NPTF x female NPTF)', L='L2@DRIVE', hex='C2HEX@HEX',
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_NPTFF(b, 'B', r['TAPDRILL@BORE']),
              bore=('A_to_pocket', lambda r, a, b: r['TAPDRILL@BORE'], None), ref='5406-16-08', bushing=True,
              exclude=r'^5406-(HHP|SHP)-', exclude_why='hollow-hex / square-head pipe plug: built by SPEC 5406HHP / 5406SHP (2026-10-02), never as a bushing',
              assume='male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length for the same dash (ASSUMPTION), hex head behind it; female NPTF port from the hex face: Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table), helical thread over P1; '
                     'Brennan 5405-08-08 STEP confirms the P1 rule for 1/2 NPTF (VERIFIED -08 only); Air-Way publishes no through-bore for the bushing -> the tap drill is carried through to the male tip (ASSUMPTION, machined-bushing practice); '
                     'wall between the female thread crests and the male thread roots checked per row'),
 '5406C': dict(name='Female Pipe Cap (NPTF)', L='L@DRIVE', hex='C1HEX@HEX', single=True, dashre=r'-(\d+)$',
              A=lambda r, a, b: end_NPTFF(a, 'A', r['TAPDRILL@BORE']), B=lambda r, a, b: end_PLAIN('B'),
              bore=('pocket_only', None, None), ref='5406-C-8',
              assume='female NPTF port: Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table; Brennan 5405-08-08 STEP VERIFIED -08 only), helical thread over P1; closed hex cap, hex over the full length (ASSUMPTION - cap crown shape unpublished), end chamfers NOT modelled'),
 '5406P': dict(name='Male Pipe Plug (NPTF)', L='L2@DRIVE', hex='C2HEX@HEX', single=True,
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_PLAIN('B'),
              bore=('none', None, None), ref='5406-16P',
              assume='male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length for the same dash (ASSUMPTION); solid hex head plug, hex head to a plain flat face, end chamfers NOT modelled'),
 '2700': dict(name='Bulkhead Union (JIC x JIC bulkhead)', L='L4@DRIVE', hex='C2HEX@HEX',
              A=lambda r, a, b: end_JICM(a, 'A'), B=lambda r, a, b: end_JICBH(b, 'B', r['I1@DRIVE']),
              bore=('mid', 'D1@BORE', 'D2@BORE'), ref='2700-08-08', thrchk=(('A', 'THDMAJ_B1@DRIVE'), ('B', 'THDMAJ_B2@DRIVE')), ln=True,
              assume='JIC end A: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); ' + 'JIC bulkhead end: MS33656J nose chain per dash (seat, land, relief, 60deg ramp; 2403 table, VERIFIED vs Brennan) with the JIC thread extended over the full bulkhead length I1 (Air-Way) - construction confirmed on the Brennan 2705-08-08 STEP (thread 0.750-16 from the relief to the land; Brennan I1 from the relief 1.44 = Air-Way); the Brennan 0.04 collar at the hex face and its 0.679 relief (vs the 0.659 cone dia used here) are NOT modelled; -LN configs = the same fitting shipped with a bulkhead locknut (separate part 0306, not modelled)' + '; the bulkhead is the SECOND dash (I1 = the bulkhead length of that dash on 2705/2706, e.g. 2700-06-04 I1 1.20 = -04); bore step at the hex mid-plane (ASSUMPTION, as 2403)'),
 '2705': dict(name='Female Pipe x JIC Bulkhead Connector', L='L24@DRIVE', hex='C5HEX@HEX',
              A=lambda r, a, b: end_NPTFF(a, 'A', r['TAPDRILL@BORE']), B=lambda r, a, b: end_JICBH(b, 'B', r['I1@DRIVE']),
              bore=('A_to_pocket', 'D@BORE', None), ref='2705-08-08-LN', thrchk=(('A', 'THDMAJ_A@DRIVE'), ('B', 'THDMAJ_B@DRIVE')), ln=True,
              assume='female NPTF port: Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table; Brennan 5405-08-08 and 2705-08-08 STEPs), helical thread over P1; ' + 'JIC bulkhead end: MS33656J nose chain per dash (seat, land, relief, 60deg ramp; 2403 table, VERIFIED vs Brennan) with the JIC thread extended over the full bulkhead length I1 (Air-Way) - construction confirmed on the Brennan 2705-08-08 STEP (thread 0.750-16 from the relief to the land; Brennan I1 from the relief 1.44 = Air-Way); the Brennan 0.04 collar at the hex face and its 0.679 relief (vs the 0.659 cone dia used here) are NOT modelled; -LN configs = the same fitting shipped with a bulkhead locknut (separate part 0306, not modelled)' + '; bore D from the bulkhead tip to the pocket bottom; Brennan 2705-08-08: hex 1.13 long carries the port, overall 2.61 (Air-Way L24 2.58)'),
 '2706': dict(name='Male Pipe x JIC Bulkhead Connector', L='L25@DRIVE', hex='C2HEX@HEX',
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_JICBH(b, 'B', r['I1@DRIVE']),
              bore=('mid', 'D1@BORE', 'D@BORE'), ref='2706-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE'), ('B', 'THDMAJ_B@DRIVE')), ln=True,
              assume='male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length for the same dash (ASSUMPTION); ' + 'JIC bulkhead end: MS33656J nose chain per dash (seat, land, relief, 60deg ramp; 2403 table, VERIFIED vs Brennan) with the JIC thread extended over the full bulkhead length I1 (Air-Way) - construction confirmed on the Brennan 2705-08-08 STEP (thread 0.750-16 from the relief to the land; Brennan I1 from the relief 1.44 = Air-Way); the Brennan 0.04 collar at the hex face and its 0.679 relief (vs the 0.659 cone dia used here) are NOT modelled; -LN configs = the same fitting shipped with a bulkhead locknut (separate part 0306, not modelled)' + '; bore step (D1 pipe side / D bulkhead side) at the hex mid-plane (ASSUMPTION)'),
 '4404': dict(name='Male Pipe x Beaded Hose Connector', L='L1@DRIVE', hex='CHEX@HEX',
              A=lambda r, a, b: end_HOSEB('A', frac(r['$PRP@TubeOD']), r['AA@DRIVE']), B=lambda r, a, b: end_NPTFM(b, 'B'),
              bore=('mid', 'D3@BORE', 'D3@BORE'), ref='4404-08-06', thrchk=(('B', 'THDMAJ_A@DRIVE'),),
              assume='beaded hose stub: tube OD = Air-Way TUBE OD (hose size), bead dia = Air-Way AA, through bore D; stub length 1.500 from the hex face, bead centre 0.251 from the stub tip and bead chord width from the bead section radius 0.060 - all three measured on the Brennan 4404-08-06 STEP and ASSUMED for the other sizes (with them, Air-Way L gives hex lengths that grow smoothly with the hex, e.g. 0.29 on 4404-08-06 = Brennan); the round bead section is modelled as a flat-topped ring of the same chord width; hex end chamfers NOT modelled' + '; male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length (Brennan 4404-08-06: 0.56 = the 5404 value for -06)'),
 '4604': dict(name='Male ORB x Beaded Hose Connector', L='L12@DRIVE', hex='C1HEX@HEX',
              A=lambda r, a, b: end_HOSEB('A', frac(r['$PRP@TubeOD']), r['AA@DRIVE']), B=lambda r, a, b: end_ORBM(b, 'B'),
              bore=('mid', 'D@BORE', 'D@BORE'), ref='4604-08-08-O', thrchk=(('B', 'THDMAJ_B@DRIVE'),),
              assume='beaded hose stub: tube OD = Air-Way TUBE OD (hose size), bead dia = Air-Way AA, through bore D; stub length 1.500 from the hex face, bead centre 0.251 from the stub tip and bead chord width from the bead section radius 0.060 - all three measured on the Brennan 4404-08-06 STEP and ASSUMED for the other sizes (with them, Air-Way L gives hex lengths that grow smoothly with the hex, e.g. 0.29 on 4404-08-06 = Brennan); the round bead section is modelled as a flat-topped ring of the same chord width; hex end chamfers NOT modelled' + '; male ORB end: thread length + groove from the 6401/6405/6410 review tables (ORD-5700 groove, measured thread length; no tip chamfer modelled)'),
 '5404N': dict(name='Straight Pipe Nipple (round, NPTF x NPTF)', L='L@DRIVE', hex='COD@REF', round=True, dashre2=r'-N-(\d+)-(\d+)',
              # 2026-10-18 (user A4 "keep OMi's form"): OMi part numbers 5404-N-04X2.500 = one pipe dash (both ends) + the cut length after X;
              # read when the Air-Way form "5404-N-4-4 X 2" (dashre2) does not match; the X length must equal L@DRIVE
              dashre1=r'-N-(\d+)X(\d+(?:\.\d+)?)$',
              A=lambda r, a, b: end_NPTFM(a, 'A', NPTF[a][6]), B=lambda r, a, b: end_NPTFM(b, 'B', NPTF[b][6]),
              bore=('mid', 'D1@BORE', 'D2@BORE'), ref='5404-N-8-8 X 3', thrchk=(('A', 'THDMAJ_A1@DRIVE'), ('B', 'THDMAJ_A2@DRIVE')),
              assume='round bar of Air-Way diameter C (no hex); male NPTF ends per ASME B1.20.3, threaded over L2 only (vanish threads NOT modelled - ASSUMPTION), the small step from the thread to the bar diameter is the difference between C and the pipe OD as printed; bore step at mid-length (ASSUMPTION)'),
 '6404': dict(name='Female ORB Port x Male NPTF Adapter', L='L32@DRIVE', hex='C1HEX@HEX',
              A=lambda r, a, b: end_NPTFM(b, 'A'), B=lambda r, a, b: end_ORBF(a, 'B', r['D3@BORE'], r['D1@BORE']),
              bore=('A_to_pocket', 'D1@BORE', None), ref='6404-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'b'),),
              assume='female SAE ORB port: minor bore = Air-Way D3 (port drill); O-ring chamfer (12deg at -04/-06, 15deg from -08 up), 45deg lead-in, minor-bore depth and 120deg drill point measured per port size on the Brennan 6404-04/-06/-08/-10/-12/-16/-24 and 6410-12-08-O / 6410-24-20-O STEPs (-08 measured twice, agree; single manufacturer); straight helical UN thread over the port depth; hex over the full body length, end chamfers NOT modelled' + '; male NPTF end per ASME B1.20.3 + the 5404 Brennan-measured end length (Brennan 6404-08-08: 0.75 = the 5404 value); bore D1 from the male tip to the port'),
 '6410': dict(name='ORB Reducer/Expander (male ORB x female ORB port)', L='L33@DRIVE', hex='C1HEX@HEX',
              A=lambda r, a, b: end_ORBM(a, 'A'), B=lambda r, a, b: end_ORBF(b, 'B', r['D3@BORE'], r['D@BORE']),
              bore=('A_to_pocket', 'D@BORE', None), ref='6410-12-08-O', thrchk=(('A', 'THDMAJ_B1@DRIVE', 'a'),),
              assume='female SAE ORB port: minor bore = Air-Way D3 (port drill); O-ring chamfer (12deg at -04/-06, 15deg from -08 up), 45deg lead-in, minor-bore depth and 120deg drill point measured per port size on the Brennan 6404-04/-06/-08/-10/-12/-16/-24 and 6410-12-08-O / 6410-24-20-O STEPs (-08 measured twice, agree; single manufacturer); straight helical UN thread over the port depth; hex over the full body length, end chamfers NOT modelled' + '; male ORB end: thread length + groove from the 6401/6405/6410 review tables; bore D from the male tip to the port'),
 '2406': dict(name='Female JIC x Male JIC Reducer/Expander', L='L23@DRIVE', hex='HEXB@HEX',
              A=lambda r, a, b: end_JICM(b, 'A'), B=lambda r, a, b: end_JICF(a, 'B'),
              bore=('A_to_pocket', 'D3@BORE', None), ref='2406-08-06', thrchk=(('A', 'THDMAJ_B@DRIVE', 'b'),),
              assume='female 37deg JIC port (Brennan 2406 STEPs, one per female size -04..-32): thread minor = ASME B1.1 basic minor, 45deg countersink from the measured dia, minor bore to the measured depth, 37deg internal seat from the minor straight down to the bore (no flat) - measured at every size; the round collar at the female end on the STEP is NOT modelled (hex over the full body); male JIC end MS33656J (VERIFIED); bore D3 from the male tip to the seat'),
 '6504': dict(name='Male JIC x Female JIC Swivel Union', L='L13@DRIVE', hex='CHEX@HEX', swivel=True,
              A=lambda r, a, b: end_JICM(a, 'A'), B=lambda r, a, b: end_JICSW(b, 'B', r['L13@DRIVE'] - r['L14@DRIVE'], r['C3HEX@HEX']),
              bore=('sw2', 'D1@BORE', 'D2@BORE'), ref='6504-08-08', thrchk=(('A', 'THDMAJ_B1@DRIVE', 'a'), ('B', 'THDMAJ_B2@DRIVE', 'b')),
              assume='male JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L13 = male tip to the nut face, L14 = male tip to the seat (L13-L14 = nut face to nose tip); body hex C, nut hex C3 (Air-Way); ' + SWIV_ASSUME + '; bore step D1/D2 at the body-hex mid-plane (ASSUMPTION, as 2403)'),
 '6505': dict(name='Male Pipe x Female JIC Swivel Connector', L='L15@DRIVE', hex='CHEX@HEX', swivel=True,
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_JICSW(b, 'B', r['L15@DRIVE'] - r['L16@DRIVE'], r['C3HEX@HEX']),
              bore=('sw2', 'D1@BORE', 'D@BORE'), ref='6505-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_B@DRIVE', 'b')),
              assume='male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length for the same dash (ASSUMPTION); L15 = pipe tip to the nut face, L16 = pipe tip to the seat; body hex C, nut hex C3 (Air-Way); ' + SWIV_ASSUME + '; bore D1 (pipe side, where Air-Way prints one; D where it prints ---) / D (swivel side) stepped at the body-hex mid-plane (ASSUMPTION, as 2403)'),
 '6506': dict(name='Female Pipe x Female JIC Swivel Connector', L='L17@DRIVE', hex='C1HEX@HEX', swivel=True,
              A=lambda r, a, b: end_NPTFF(a, 'A', r['TAPDRILL@BORE']), B=lambda r, a, b: end_JICSW(b, 'B', r['L17@DRIVE'] - r['L18@DRIVE'], r['C3HEX@HEX']),
              bore=('sw1', 'D@BORE', None), ref='6506-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_B@DRIVE', 'b')),
              assume='female NPTF port: Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table; Brennan 5405 STEPs at -04/-08/-12/-16), tapered helical thread over P1; L17 = port face to the nut face, L18 = port face to the seat; body hex C1, nut hex C3 (Air-Way); ' + SWIV_ASSUME + '; bore D from the port bottom to the seat'),
 '6402': dict(name='Male ORB x Female JIC Swivel Adapter', L='L26@DRIVE', hex='C4HEX@HEX', swivel=True,
              A=lambda r, a, b: end_ORBM(a, 'A'), B=lambda r, a, b: end_JICSW(b, 'B', r['L26@DRIVE'] - r['L27@DRIVE'], r['C3HEX@HEX']),
              bore=('sw2', 'D1@BORE', 'D2@BORE'), ref='6402-08-08-O', thrchk=(('A', 'THDMAJ_B1@DRIVE', 'a'), ('B', 'THDMAJ_B2@DRIVE', 'b')),
              assume='male ORB end: thread length + groove from the 6401/6405/6410 review tables (ORD-5700 groove, measured thread length; no tip chamfer modelled); L26 = ORB tip to the nut face, L27 = ORB tip to the seat; body hex C4, nut hex C3 (Air-Way); ' + SWIV_ASSUME + '; bore step D1/D2 at the body-hex mid-plane (ASSUMPTION, as 2403)'),
 '6565': dict(name='Double Female JIC Swivel Union', L='L31@DRIVE', hex='CHEX@HEX', swivel=True,
              A=lambda r, a, b: end_JICSW(a, 'A', (r['L31@DRIVE'] - r['L32@DRIVE']) / 2, r['C3_1HEX@HEX']),
              B=lambda r, a, b: end_JICSW(b, 'B', (r['L31@DRIVE'] - r['L32@DRIVE']) / 2, r['C3_2HEX@HEX']),
              bore=('sw2', 'D1@BORE', 'D2@BORE'), ref='6565-08-08', thrchk=(('A', 'THDMAJ_B1@DRIVE', 'a'), ('B', 'THDMAJ_B2@DRIVE', 'b')),
              assume='BOTH ends female JIC swivel; L31 = nut face to nut face, L32 = seat to seat, (L31-L32)/2 taken as the nut-face-to-seat length of each end (all built rows have equal dashes, so the split is symmetric); body hex C between the two body faces, nut hexes C3(1)/C3(2) (Air-Way); ' + SWIV_ASSUME.replace('the body hex stops at the measured body-face position of the 6500 forged arm (ASSUMED for a straight body)', 'the body hex runs between the two measured body-face positions (6500 forged-arm end, ASSUMED for a straight body)') + '; bore D1/D2 stepped at the body-hex mid-plane (ASSUMPTION, as 2403); ' + SEAT_TO_BORE_ASSUME),
 '1404': dict(name='Male Pipe x Female NPSM Swivel Adapter Union', L='W@HEX', hex='C1HEX@HEX', swivel=True,
              A=lambda r, a, b: end_NPTFM(a, 'A'), B=lambda r, a, b: end_NPSMSW(b, 'B', r['W@HEX'] - r['L@DRIVE'], r['C2HEX@HEX']),
              bore=('sw2', 'D2@BORE', 'D@BORE'), ref='1404-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_A1@DRIVE', 'b')),
              assume='male NPTF end per ASME B1.20.3 with the 5404 Brennan-measured end length (Brennan 1404-08-08: 0.75 = the 5404 value; its internal 30deg tip chamfer NOT modelled); W = pipe tip to the nut face (overall), L = pipe tip to the stem tip; body hex C(1), nut hex C(2) (Air-Way); ' + NPSM_ASSUME + '; bore D2 (pipe side) / D (stem side) stepped at the body-hex mid-plane (Brennan 1404-08-08 step at the hex mid-plane too)'),
 '1405': dict(name='Female Pipe x Female NPSM Swivel Adapter Union', L='W1@HEX', hex='C1HEX@HEX', swivel=True,
              A=lambda r, a, b: end_NPTFF(a, 'A', r['TAPDRILL@BORE']), B=lambda r, a, b: end_NPSMSW(b, 'B', r['W1@HEX'] - r['L1@DRIVE'], r['C2HEX@HEX']),
              bore=('sw1', 'D@BORE', None), ref='1405-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_A1@DRIVE', 'b')),
              assume='female NPTF port: Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table; Brennan 5405 STEPs), tapered helical thread over P1; W1 = port face to the nut face (overall), L1 = port face to the stem tip; body hex C(1), nut hex C(2) (Air-Way); ' + NPSM_ASSUME + '; bore D from the port bottom through the stem tip'),
 '1700': dict(name='Code 61 Flange Adapter (male JIC x SAE code 61 flange head)', L='L28@DRIVE', hex='CHEX@HEX', zonehex=True, dashre2=r'-61-(\d+)-(\d+)',
              A=lambda r, a, b: end_JICM(a, 'A'), B=lambda r, a, b: end_FLG61(b, 'B', r['O@DRIVE']),
              bore=('mid', 'D@BORE', 'D@BORE'), ref='1700-61-08-08', thrchk=(('A', 'THDMAJ_B@DRIVE', 'a'),),
              assume='JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan; the Brennan 1700 STEPs match it at -08/-12/-24); L28 = JIC tip to the flange face (Air-Way); ' + FLG61_ASSUME + '; through bore D (Air-Way; Brennan agrees at -08/-12/-24), cut from both faces to the hex mid-plane'),
 '0403': dict(name='Braze Tube Union (braze socket x male JIC)', L='L3@DRIVE', hex='CHEX@HEX',
              A=lambda r, a, b: end_BRAZE('A', r['D2@BORE'], r['L7@DRIVE']), B=lambda r, a, b: end_JICM(b, 'B'),
              bore=('A_to_pocket', 'D@BORE', None), ref='0403-08-08 UNPL',
              assume='OMi 0403 (plated) parts built from the Air-Way UNPL (unplated) rows of the same size - plating does not change the shape (user decision 2026-09-25, closes QA #123); Air-Way-only UNPL sizes are no longer built; JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); braze socket = plain bore D2 to depth L7 (Air-Way); bore D from the socket bottom to the JIC tip; hex spans socket face to JIC relief'),
}


# ---- 2026-10-01 (tier 1, SPEC-2403 / SPEC-2405 / SPEC-2404): the three masters built so far by the legacy builders
# (03_SCRIPTS/_legacy/gen_2403_sw2.py, gen_2405_sw2.py) and by hand (2404, 00_DOCS/2404_MASTER_BUILD_SHEET.md) get gen_straight2
# SPECs on the existing end modules. Everything below is used by these three SPECs only (options 'load', 'skip_blocked',
# 'step', 'desc', 'carry' and the row keys starting with '_'); every other root is generated exactly as before.
# NOTE: templates/DesignTable_2403_SW2.xlsx and _2405_SW2.xlsx stay FROZEN (they are the JIC / female-pipe end libraries above);
# the tables generated here go to GS_OUT like every other root and must never be copied over the templates.

def _load_table(fname):
    """a review table by file name (same layout as load_review: title row, header row, data rows)"""
    ws = openpyxl.load_workbook(os.path.join(P.DESIGN_TABLES, fname), read_only=True).active
    rows = list(ws.iter_rows(values_only=True)); h = rows[1]
    return h, [dict(zip(h, r)) for r in rows[2:] if r[0]]


LH_ASSUME = ('2403-LH = the LARGE-HEX union (OMi "Straight-Large Hex", Air-Way s63, review table DesignTable_2403LH.xlsx), folded into the 2403 '
             'master as rows of the same shape: same JIC ends per dash, L1 and bores D1 / D2 from the 2403-LH table, hex = its C2 (as the legacy '
             '2403 builder already did, 2026-09-06)')


def load_2403():
    """2403 review rows + the 2403-LH (large hex) rows mapped onto the 2403 columns"""
    h, rows = load_review('2403')
    out = [dict(r) for r in rows]
    for r in _load_table('DesignTable_2403LH.xlsx')[1]:
        n = dict(r)
        n['HEXB@HEX'] = r.get('C2HEX@HEX'); n['THDMAJ_A@DRIVE'] = r.get('THDMAJ_B1@DRIVE'); n['THDMAJ_B@DRIVE'] = r.get('THDMAJ_B2@DRIVE')
        n['_DESCNAME'] = 'Male Union Large Hex'; n['_ASSUME'] = LH_ASSUME
        out.append(n)
    return h, out


L2404_ASSUME = ('2404-L = the LONG male connector (OMi "Straight-Long", Air-Way s65, DesignTable_2404L.xlsx), folded into the 2404 master '
                '(user decision 2026-09-25): overall = Air-Way L20, hex = C, bores D (JIC side) / D1 (pipe side); NPTF end length = the 2404 / 5404 '
                'value for the pipe dash; the hex takes the extra length: hex = L20 - both ends (= Air-Way T20 to within 0.007 on every row; Brennan '
                '2404-L-08-08 STEP: JIC end 0.657, hex 1.633, pipe end 0.750, overall 3.040)')
# review fix F1 (2026-10-01): the bore clauses. The hand-made 2404 table builds ONE bore of the smaller of Air-Way D / D1 wherever MS51500G
# gives no counterbore depth S (24 rows; the 5 2404-L rows likewise). Air-Way and OMi give two different bores on those rows and the Brennan
# 2404 STEPs have two bores stepped at the hex mid-plane (14 of 14 two-bore STEPs, tools/_out/tier1_20261001/integrated/review_fix/
# brennan_2404_bores.txt), so the one-bore rule is a source conflict: such rows are HELD (not built) until the user answers Q-2404-BORE.
# MS51500G Note 5 ("at manufacturers option, through passages may conform with the smaller diameter specified or the appropriate end may be
# counter-bored to the larger diameter for depth S") covers only the sizes MS51500G lists, and Brennan does not use the one-bore option.
ONE_BORE_2404_OK = frozenset()     # Q-2404-BORE answer: the part numbers the user accepts with ONE bore (empty = none accepted; date the decision here)


def hold2404(what, d3, dd, nos, remedy):
    return (f'HELD for the user (Q-2404-BORE): {what} ONE bore {d3} straight through = the smaller of Air-Way D / D1, but Air-Way gives two '
            f'bores{dd} and no counterbore depth ({nos}); the Brennan 2404 STEPs have two bores stepped at the hex mid-plane (OMi Side 1 / 2 ID per '
            f'row: Q-2404-BORE). Built only if the user accepts ONE bore (ONE_BORE_2404_OK){remedy}')


CB2404_ASSUME = ('bore: through passage = the smaller of D / D1, the end carrying the larger counterbored to depth S (MS51500G Note 5 and its S '
                 'column; hand-made 2404 table CBCUT columns)')
CB2404_SRC_ASSUME = ('bore: through passage D3, the end carrying the larger bore counterbored to the depth of the review table, which is NOT an '
                     'MS51500G S value (MS51500G does not list this size): the hand-made 2404 table took it from the Brennan STEP of the part '
                     '(see the row source) - single manufacturer, ASSUMED')
MID2404_ASSUME = ('bore: two bores - the review-table counterbore CBDIA on its end, D3 through the rest - stepped at the HEX MID-PLANE (user '
                  '2026-10-09, Q-2404-BORE: the hole is not the same throughout (from OMi); ASSUMPTION for the step: no depth is published for '
                  'this size - Air-Way prints none, MS51500G does not list it - Air-Way\'s 2404 / 2404-L drawings show the step inside the hex '
                  '(2404-L at its middle), and the 14 two-bore 2404 parts measured 2026-10-01 have it at the hex mid-plane within 0.0005 - ASSUMED)')
MIDL2404_ASSUME = ('bore: two bores - 2404-L table D1 from the pipe end, D from the JIC end - stepped at the HEX MID-PLANE (user 2026-10-09, '
                   'Q-2404-BORE: the hole is not the same throughout; Air-Way publishes no depth for 2404-L and its series-65 drawing shows the '
                   'step in the middle of the hex - ASSUMED)')
THRU2404_ASSUME = ('bore: ONE bore D3 straight through = the smaller of Air-Way D / D1 (hand-made 2404 table rule; MS51500G Note 5 allows a '
                   'smaller-diameter through passage as a manufacturer\'s option on the sizes it lists) - kept by the user\'s answer to Q-2404-BORE '
                   'although Air-Way gives two bores and the Brennan 2404 STEPs have two bores stepped at the hex mid-plane')
THRUL2404_ASSUME = ('bore: ONE bore of the smaller of D / D1 straight through - kept by the user\'s answer to Q-2404-BORE although Air-Way gives two '
                    'bores and publishes no counterbore depth for 2404-L (Brennan 2404-L-08-08 STEP: one 0.391 bore straight through; Brennan TFA '
                    'catalog p.6 prints one drill for 2404-L-06-06 / -08-08 / -12-12 and two drills for -04-04 / -06-04)')
# review fix F2 (2026-10-01): the length / hex clause of the SPEC text depends on the row's source (OMi-only sizes come from the Brennan
# product drawing, not Air-Way); every source of such a row is Brennan's (OMi's data are Brennan's, evidence 2026-09-26) = ONE source.
SRC2404_AIRWAY = 'overall length D1 / hex: review table (Air-Way; == MS51500G on the sizes it lists)'
SRC2404_BRENNAN = ('overall length D1 / hex / bores: review table = OMi WebsitePartsInfo2026 (identical values, checked 2026-10-09; first appended '
                   'from the Brennan product drawing 2026-09-05 - OMi-only size: absent from Air-Way and MS51500G; OMi\'s data are Brennan\'s, '
                   'evidence 2026-09-26 -> one source, ASSUMED)')


def _min2(x, y):
    return None if x is None or y is None else min(x, y)


def _note(n, s):
    n['_NOTE'] = (n['_NOTE'] + '; ' + s) if n.get('_NOTE') else s


def _assumed(n, why):
    """review fixes F1 / F2: a row whose geometry now rests on an assumption or on one source cannot stay VERIFIED"""
    if n.get('$PRP@DataStatus') == 'VERIFIED':
        n['$PRP@DataStatus'] = 'ASSUMED'; _note(n, 'DataStatus VERIFIED -> ASSUMED: ' + why)


def _ms_s(a, b, depth):
    """True when depth is the MS51500G S of the size (JIC dash a, pipe dash b)"""
    from ms51500 import MS
    m = MS.get((a, b))
    return bool(m and m.get('S') is not None and depth is not None and abs(m['S'] - depth) < 1e-6)


def load_2404():
    """2404: the hand-made review table DesignTable_2404_FINAL.xlsx + the 2404-L rows (DesignTable_2404L.xlsx) mapped onto its columns.
    Bores: the hand-made table carries a through bore D3 + a counterbore (CBDIA, DEPTH, $STATE) at End A (pipe) or End B (JIC); it is
    written as the generator's two-bore 'mid' construction: bore A, bore B and the step position from End A (_STEP; None = hex mid-plane).
    Review fixes 2026-10-01: rows with ONE bore where the sources give two are held (_HOLD) unless the user accepted them (F1); a counterbore
    without a depth steps at the hex mid-plane (Brennan-measured rule, F1); the source clause and DataStatus follow the row's source (F2)."""
    h, rows = _load_table('DesignTable_2404_FINAL.xlsx')
    out = []
    for r in rows:
        n = dict(r); L_ = r.get('D1@DRIVE'); pn = str(r['$PRP@PartNo'])
        dd = [int(x) for x in re.findall(r'-(\d\d)', pn)[:2]]; a_, b_ = (dd + [None, None])[:2]
        brennan_only = 'absent from Air-Way' in str(r.get('$PRP@AxialSource') or '')
        n['_SRC'] = SRC2404_BRENNAN if brennan_only else SRC2404_AIRWAY
        if brennan_only: _assumed(n, 'every source of this OMi-only size is Brennan (product drawing, STEP; OMi\'s data are Brennan\'s) = one source')
        if r.get('$STATE@CBCUT_A') == 'U':
            n['_BORE_A'], n['_BORE_B'], n['_STEP'] = r.get('CBDIA@BORE_A'), r.get('D3@BORE_THRU'), r.get('DEPTH@CBCUT_A'); dep_ = r.get('DEPTH@CBCUT_A')
        elif r.get('$STATE@CBCUT_B') == 'U':
            n['_BORE_A'], n['_BORE_B'] = r.get('D3@BORE_THRU'), r.get('CBDIA@BORE_B'); dep_ = r.get('DEPTH@CBCUT_B')
            n['_STEP'] = None if (L_ is None or dep_ is None) else L_ - dep_
        else:
            dep_ = None
            n['_BORE_A'] = n['_BORE_B'] = r.get('D3@BORE_THRU'); n['_STEP'] = None     # one bore through: the step position does not matter
            if pn in ONE_BORE_2404_OK:
                n['_ASSUME'] = THRU2404_ASSUME; _assumed(n, 'ONE bore kept by the user (Q-2404-BORE) although the sources give two')
            else:
                n['_HOLD'] = hold2404('the review table builds', r.get('D3@BORE_THRU'), '', 'MS51500G does not list this size',
                                      ', or gives the review table the counterbore (CBDIA + $STATE U; an empty DEPTH = step at the hex mid-plane)')
            out.append(n); continue
        if dep_ is None:
            n['_ASSUME'] = MID2404_ASSUME; _assumed(n, 'counterbore depth unpublished: step at the hex mid-plane (Brennan-measured rule, single manufacturer)')
        elif a_ is not None and _ms_s(a_, b_, dep_):
            n['_ASSUME'] = CB2404_ASSUME
        else:
            n['_ASSUME'] = CB2404_SRC_ASSUME; _assumed(n, 'counterbore depth from one manufacturer\'s STEP (not an MS51500G S value)')
        out.append(n)
    for r in _load_table('DesignTable_2404L.xlsx')[1]:
        dd = re.findall(r'-(\d\d)', str(r['$PRP@PartNo']))
        D_, D1_ = r.get('D@BORE'), r.get('D1@BORE')
        n = {'$PRP@PartNo': r['$PRP@PartNo'], 'D1@DRIVE': r.get('L20@DRIVE'), 'HEXB@HEX': r.get('CHEX@HEX'),
             'NPTF_ENDL@DRIVE': ENDL.get(int(dd[1])) if len(dd) >= 2 else None, 'PIPEOD@DRIVE': r.get('THDMAJ_A@DRIVE'), 'THDMAJ_B@DRIVE': r.get('THDMAJ_B@DRIVE'),
             '_BORE_A': _min2(D1_, D_), '_BORE_B': _min2(D1_, D_), '_STEP': None, '_T20': r.get('T20REF@REF'),
             '$PRP@DataStatus': r.get('$PRP@DataStatus'), '$PRP@AxialSource': r.get('$PRP@AxialSource'), '$COMMENT': r.get('$COMMENT'),
             '$PRP@ScopeAction': r.get('$PRP@ScopeAction'), '$PRP@OMiSKU': r.get('$PRP@OMiSKU'), '_DESCNAME': 'Male Long Connector', '_ASSUME': L2404_ASSUME,
             '_SRC': SRC2404_AIRWAY}
        if D_ is not None and D1_ is not None and abs(D_ - D1_) > 1e-9:
            if str(r['$PRP@PartNo']) in ONE_BORE_2404_OK:
                n['_ASSUME'] = L2404_ASSUME + '; ' + THRUL2404_ASSUME; _assumed(n, 'ONE bore kept by the user (Q-2404-BORE) although the sources give two')
                _note(n, f"bore: 2404-L table D {D_} / D1 {D1_} (no counterbore depth published) -> one {_min2(D1_, D_)} bore through (user decision Q-2404-BORE)")
            else:      # 2026-10-09 Q-2404-BORE answered (user, from OMi): two bores, stepped at the hex mid-plane (was: HELD)
                n['_BORE_A'], n['_BORE_B'] = D1_, D_
                n['_ASSUME'] = L2404_ASSUME + '; ' + MIDL2404_ASSUME
                _assumed(n, 'two bores stepped at the hex mid-plane (Q-2404-BORE answer 2026-10-09; no published depth)')
                _note(n, f"bore: 2404-L table D {D_} (JIC) / D1 {D1_} (pipe), stepped at the hex mid-plane (user 2026-10-09, Q-2404-BORE)")
        else:
            n['_ASSUME'] = L2404_ASSUME + '; bore: one bore D = D1 straight through (2404-L table)'
        out.append(n)
    return h, out


def jic_row_2404(r, a):
    """JIC chain from the 2404 row - only for a dash the JIC library lacks. (Integration 2026-10-01: SIZE-40 put -40 into the library -
    JIC_MEAS_40, Brennan 2404-40-32 STEP, cell-identical to the 2404-40-32 row chain - so this returns None for every current row.)"""
    if a in JIC: return None
    e = dict(TM=r.get('THDMAJ_B@DRIVE'), RL=r.get('JIC_RELIEFL@DRIVE'), TZ=r.get('JIC_THDZ@DRIVE'), CD=r.get('JIC_CONEDIA@DRIVE'),
             LL=r.get('JIC_LANDL@DRIVE'), SL=r.get('JIC_SEATL@DRIVE'), thr=r.get('$PRP@EndB_Thread'))
    if any(v is None for v in e.values()): raise KeyError(f'no JIC end data for -{a:02d} (not in the MS33656J library, not in the row)')
    return e


SPEC['2403'] = dict(name='Male Union', L='L1@DRIVE', hex='HEXB@HEX', load=load_2403,
                    A=lambda r, a, b: end_JICM(a, 'A'), B=lambda r, a, b: end_JICM(b, 'B'),
                    bore=('mid', 'D1@BORE', 'D2@BORE'), ref='2403-08-08', thrchk=(('A', 'THDMAJ_A@DRIVE', 'a'), ('B', 'THDMAJ_B@DRIVE', 'b')),
                    desc=lambda r, tA, tB: f"{r.get('_DESCNAME') or 'Male Union'}, {tA} x {tB}",
                    assume='JIC ends A and B: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L1 / hex / bores D1, D2: review table (Air-Way; matched-dash rows == MS51501D); '
                           'hex over the whole length between the two JIC ends (legacy 2403 builder); bore step D1/D2 at the hex mid-plane (ASSUMPTION - unsourced, same rule as the legacy 2403 builder and 6400; '
                           'no effect where D1 = D2); hex end chamfers NOT modelled')
SPEC['2405'] = dict(name='Female Connector', L='L2@DRIVE', hex='HEXB@HEX',
                    A=lambda r, a, b: end_NPTFF(b, 'A', r['TAPDRILL@BORE_A']), B=lambda r, a, b: end_JICM(a, 'B'),
                    bore=('A_to_pocket', 'D3@BORE_THRU', None), ref='2405-08-08', thrchk=(('B', 'THDMAJ_B@DRIVE', 'a'),),
                    desc=lambda r, tA, tB: f"Female Connector, {tB} JIC x {tA}",
                    assume='female NPTF port (End A): Air-Way tap drill to MS51503 P1 max per pipe dash (2405 table; Brennan 5405 STEPs confirm P1 = the port drill depth), tapered helical thread over P1; '
                           'JIC end (End B): MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L2 / hex: review table (Air-Way; matched rows == MS51503D); hex from the port face to the JIC end '
                           '(legacy 2405 builder); through bore D3 (Air-Way) from the JIC tip to the port bottom; hex end chamfers and the port countersink NOT modelled')
SPEC['2404'] = dict(name='Male Connector', L='D1@DRIVE', hex='HEXB@HEX', load=load_2404, skip_blocked=True,
                    A=lambda r, a, b: end_NPTFM(b, 'A', r['NPTF_ENDL@DRIVE']), B=lambda r, a, b: end_JICM(a, 'B', jic_row_2404(r, a)),
                    bore=('mid', lambda r, a, b: r['_BORE_A'], lambda r, a, b: r['_BORE_B']), step=lambda r, EA, EB, L, body: r.get('_STEP'),
                    ref='2404-08-08', thrchk=(('A', 'PIPEOD@DRIVE', 'b'), ('B', 'THDMAJ_B@DRIVE', 'a')),
                    carry=('$PRP@Material', '$PRP@Finish', '$PRP@PressureRating'),
                    desc=lambda r, tA, tB: f"{r.get('_DESCNAME') or 'Male Connector'}, Male 37 deg Flare (JIC) x Male Pipe NPTF, {tB} x {tA.replace(' NPTF', '')}",
                    # review fix F2 (2026-10-01): a callable - the length / hex clause is the row's own source (_SRC: Air-Way, or Brennan for OMi-only sizes)
                    assume=lambda r: ('male NPTF end (End A) per ASME B1.20.3 (tip major E0+0.8P, cone over L2 at 1.7899 deg, then a plain relief to the end length) with the end length NPTF_ENDL of the 2404 table '
                           '(= the 5404 Brennan-measured value of the pipe dash); this REPLACES the hand-built pipe end (plain cylinder of pipe OD, taper left to the SolidWorks pipe-thread feature) by the library '
                           'NPTF end of 5404 / 6401 / 2706; JIC end (End B): MS33656J chain per dash (2403 table, VERIFIED vs Brennan; -40: JIC_MEAS_40 measured on the Brennan 2404-40-32 STEP, equal to the -40 chain of the hand-made 2404 table row); '
                           + r.get('_SRC', SRC2404_AIRWAY) + '; hex over the whole length between the two ends; hex end chamfers NOT modelled'))


# 2026-10-02 (new masters, group NUTS-CAPS): JIC cap nut and JIC bulkhead locknut - see CAP_ASSUME / NUT_ASSUME and the end modules above.
# Review columns: 0304 L (cap length) / CHEX (hex) / THDMAJ_B (thread major); 0306 h2 (nut thickness) / S4 (hex) / THDMAJ_d (thread major)
# - the existing review-table headers (the DROP rows carry Air-Way's tube nut 304 / ORFS locknut FF306 under the same letters).
SPEC['0304'] = dict(name='JIC Cap Nut', L='L@DRIVE', hex='CHEX@HEX', single=True,
                    A=lambda r, a, b: end_CROWN('A'), B=lambda r, a, b: end_JICCAP(a, 'B', JICBORE.get(a)),
                    bore=('cav_only', None, None), ref='0304-C-08', thrchk=(('B', 'THDMAJ_B@DRIVE', 'a'),), assume=CAP_ASSUME)
SPEC['0306'] = dict(name='JIC Bulkhead Locknut', L='h2@DRIVE', hex='S4@DRIVE', single=True,
                    A=lambda r, a, b: end_NUTCSA(a, 'A'), B=lambda r, a, b: end_NUTCSB(a, 'B', r['h2@DRIVE']),
                    bore=('nut_thru', None, None), ref='0306-08', thrchk=(('B', 'THDMAJ_d@DRIVE', 'a'),),
                    desc=lambda r, tA, tB: f"JIC Bulkhead Locknut, {tB.split(' (')[0]}, thread through, 45 deg countersink both faces", assume=NUT_ASSUME)


# ---- 2026-10-18 (genfeat straights, user A6 "rebuild 6400 with the generator, fold 6400-L in"): SPEC 6400 = male 37deg JIC x male SAE ORB
# straight thread connector, until now the hand-made master (DesignTable_6400_SW2.xlsx; the master file is not in the repo). Built from the
# existing END LIBRARIES only: End A = the male ORB end of the SECOND part-number dash (ORB library: 6401 / 6405 / 6410 rows + the 6408 -02 /
# -14 / -32 merges, groove width 0.125 at -14 / -32 measured on the Brennan 6400-14-14-O / -32-32-O STEPs = A18), End B = the male JIC end of
# the FIRST dash (MS33656J chain, 2403 table). The review table's own ORB / JIC columns are not read for geometry; they are cross-checked
# against the libraries (equal on every 6400 row today, the empty -14 / -32 groove width excepted) and a difference blocks the row.
# Body: hex over the whole length between the two ends, bores D4 (ORB side, End A) / D3 (JIC side, End B) stepped at the hex mid-plane - the
# hand-made table's own rule (its DEPTH@BORECUT_A = ORB end + half the hex at every row).
# 6400-L (DesignTable_6400L.xlsx, Air-Way s90) folds in as rows: the Brennan 6400-L-08-08-O STEP (tools/measure, section through the axis) has the
# 6400 ORB end (0.438), a hex 0.382 long (6400-08-08-O: 0.385) and a LONG JIC end: seat 0.1546 / land 0.0984 = MS33656J -08, then the 3/4-16
# thread cylinder straight to the hex face at 1.880 from the tip (no relief), overall 2.700 = Air-Way L6. Modelled as the library JIC end with
# its thread zone extended (end_JICBH, as the bulkhead unions 2700 / 2705 / 2706) so that the JIC end is L6 - ORB end - the hex length of the
# 6400 row of the same dashes long (6400-L-08-08-O: 2.70 - 1.48 + 0.657 = 1.877 vs Brennan 1.880).
L6400_ASSUME = ('6400-L = the LONG straight thread connector (OMi "Straight Thread Connector Long", Air-Way s90, review table DesignTable_6400L.xlsx), '
                'folded into the 6400 master (user A6 2026-10-18): overall = Air-Way L6, hex = C4, bores D2 (ORB side) / D1 (JIC side) stepped at the hex '
                'mid-plane, same ORB end per dash; the extra length is a LONG JIC THREAD: the library JIC end with its thread zone extended (bulkhead '
                'construction of 2700 / 2705 / 2706) so that the hex keeps the length of the 6400 row of the same dashes (ASSUMPTION - measured on the '
                'Brennan 6400-L-08-08-O STEP only: JIC end 1.880 from the tip to the hex face, hex 0.382 (6400-08-08-O model 0.385), ORB end 0.438, overall '
                '2.700; Brennan runs the thread cylinder straight into the hex face, the model keeps the library 60deg ramp + relief there)')
S6400_ASSUME = ('End A male SAE ORB end of the second dash and End B male 37deg JIC end of the first dash from the END LIBRARIES (ORB: thread major / length, '
                'groove dia / width of the 6401 / 6405 / 6410 review rows + the 6408 -02 / -14 / -32 rows, groove width 0.125 at -14 / -32 measured on the '
                'Brennan 6400-14-14-O / 6400-32-32-O STEPs (A18 2026-10-18); JIC: MS33656J chain per dash, 2403 table, VERIFIED vs Brennan; no tip chamfers) - '
                'equal to the ORB / JIC columns of the 6400 review table (cross-checked per row); D1 overall / hex / bores D4 (ORB side) and D3 (JIC side): '
                'review table (Air-Way; OMi = Air-Way on the A23 rows); hex over the whole length between the two ends; bore step D4 / D3 at the hex mid-plane '
                '(ASSUMPTION - the rule of the hand-made 6400 table, as 2403); hex end chamfers NOT modelled; rebuilt by the generator 2026-10-18 (user A6), '
                'replaces the hand-made 6400 master')
ROW6400_LIBCHK = (('THDMAJ_A@DRIVE', 'ORB', 'TM'), ('ORB_THDL@DRIVE', 'ORB', 'THDL'), ('ORB_GRVDIA@DRIVE', 'ORB', 'GD'), ('ORB_GRVW@DRIVE', 'ORB', 'GW'),
                  ('THDMAJ_B@DRIVE', 'JIC', 'TM'), ('JIC_RELIEFL@DRIVE', 'JIC', 'RL'), ('JIC_THDZ@DRIVE', 'JIC', 'TZ'), ('JIC_CONEDIA@DRIVE', 'JIC', 'CD'),
                  ('JIC_LANDL@DRIVE', 'JIC', 'LL'), ('JIC_SEATL@DRIVE', 'JIC', 'SL'))
BRENNAN_6400L = {'6400-L-08-08-O': 'Brennan 6400-L-08-08-O STEP: overall 2.700, JIC end 1.880 (thread cylinder 0.750 to the hex face, no relief), hex 0.382 '
                                   '(A/F 0.875), ORB end 0.438, bore 0.391 through'}


def _libchk_6400(n, a, b):
    """the 6400 review row's own ORB / JIC columns against the end libraries the SPEC builds from: a difference > 0.0005 holds the row"""
    bad = []
    for col, lib, k in ROW6400_LIBCHK:
        v = n.get(col)
        if v is None: continue                       # empty column: the library value is used (ORB_GRVW at -14 / -32 = A18)
        src = (ORB.get(b) if lib == 'ORB' else JIC.get(a)) or {}
        if k in src and abs(v - src[k]) > 5e-4: bad.append(f'{col} {v} vs the {lib} library {src[k]}')
    if bad: n['_HOLD'] = ('HELD: the 6400 row\'s own end columns differ from the end library the generator builds from (' + '; '.join(bad) +
                          ') - settle which is right before building')


def end_JICLONG(dash, sfx, I1):
    """6400-L long JIC end: the library JIC end with its thread zone extended to the end length I1 (end_JICBH construction), labelled long"""
    E = end_JICBH(dash, sfx, I1)
    E['thr'] = E['e']['thr'] + ' (long thread)'; E['long'] = True
    return E


def load_6400():
    """6400 review rows + the 6400-L rows (DesignTable_6400L.xlsx) mapped onto the 6400 columns; the long JIC end length _I1 per 6400-L row"""
    h, rows = load_review('6400')
    out, std = [], {}
    for r in rows:
        n = dict(r); dd = [int(x) for x in re.findall(r'-(\d\d)', str(r['$PRP@PartNo']))[:2]]
        if len(dd) == 2:
            std.setdefault(tuple(dd), r)
            if dd[1] in ORB and dd[0] in JIC: _libchk_6400(n, dd[0], dd[1])
        c_ = str(n.get('$COMMENT') or '')
        if len(dd) == 2 and dd[1] in ORB_GW_MEASURED and c_.startswith('BLOCKED - ORB groove width unpublished'):
            # the -14 / -32 rows' hand-made-table note: settled by A18 (2026-10-18) - the ORB library carries the measured groove width
            n['$COMMENT'] = (f'RESOLVED 2026-10-18 (A18: ORB -{dd[1]:02d} groove width {ORB[dd[1]]["GW"]} measured on the {ORB_GW_SRC[dd[1]]}, ORB library) (was: '
                             + c_[len('BLOCKED - '):] + ')')
        out.append(n)
    for r in _load_table('DesignTable_6400L.xlsx')[1]:
        pn = str(r['$PRP@PartNo']); dd = [int(x) for x in re.findall(r'-(\d\d)', pn)[:2]]
        n = {'$PRP@PartNo': pn, 'D1@DRIVE': r.get('L6@DRIVE'), 'HEXB@HEX': r.get('C4HEX@HEX'), 'D4@BORE_A': r.get('D2@BORE'), 'D3@BORE_B': r.get('D1@BORE'),
             'THDMAJ_A@DRIVE': r.get('THDMAJ_B2@DRIVE'), 'THDMAJ_B@DRIVE': r.get('THDMAJ_B1@DRIVE'), 'ORB_GRVDIA@DRIVE': r.get('ORB_GRVDIA@DRIVE'),
             'ORB_GRVW@DRIVE': r.get('ORB_GRVW@DRIVE'), '$PRP@DataStatus': r.get('$PRP@DataStatus'), '$PRP@AxialSource': r.get('$PRP@AxialSource'),
             '$COMMENT': r.get('$COMMENT'), '$PRP@ScopeAction': r.get('$PRP@ScopeAction'), '$PRP@OMiSKU': r.get('$PRP@OMiSKU'),
             '_DESCNAME': 'Straight Thread Connector Long', '_ASSUME': L6400_ASSUME, '_LONG': True}
        if len(dd) == 2 and dd[1] in ORB and dd[0] in JIC:
            _libchk_6400(n, dd[0], dd[1])
            s_ = std.get(tuple(dd))
            if s_ is None or s_.get('D1@DRIVE') is None or n['D1@DRIVE'] is None:
                n.setdefault('_HOLD', f'HELD: no 6400-{dd[0]:02d}-{dd[1]:02d}-O row with an overall length - the hex length of the long variant is taken from it')
            else:
                jl_ = end_JICM(dd[0], 'B')['endlen']; ol_ = end_ORBM(dd[1], 'A')['endlen']
                hexl_ = s_['D1@DRIVE'] - ol_ - jl_
                n['_I1'] = round(n['D1@DRIVE'] - ol_ - hexl_, 4)
                _note(n, f"6400-L: JIC end {n['_I1']} long = L6 {n['D1@DRIVE']} - ORB end {ol_:.4f} - the hex length {hexl_:.4f} of {s_['$PRP@PartNo']} (D1 {s_['D1@DRIVE']})")
                if pn in BRENNAN_6400L: _note(n, BRENNAN_6400L[pn] + f" - model: JIC end {n['_I1']}, hex {hexl_:.4f}, ORB end {ol_:.4f}, overall {n['D1@DRIVE']}")
                _assumed(n, 'the long JIC end length rests on the hex-length rule measured on one Brennan STEP (6400-L-08-08-O)')
        out.append(n)
    return h, out


SPEC['6400'] = dict(name='Straight Thread Connector (male JIC x male ORB)', L='D1@DRIVE', hex='HEXB@HEX', load=load_6400,
                    A=lambda r, a, b: end_ORBM(b, 'A'),
                    B=lambda r, a, b: end_JICLONG(a, 'B', r['_I1']) if r.get('_LONG') else end_JICM(a, 'B'),
                    bore=('mid', 'D4@BORE_A', 'D3@BORE_B'), ref='6400-08-08-O', thrchk=(('A', 'THDMAJ_A@DRIVE', 'b'), ('B', 'THDMAJ_B@DRIVE', 'a')),
                    carry=('$PRP@Material', '$PRP@Finish', '$PRP@PressureRating'),
                    desc=lambda r, tA, tB: f"{r.get('_DESCNAME') or 'Straight Thread Connector'}, Male 37 deg Flare (JIC) x Male SAE ORB, {tB} x {tA.replace(' (male ORB)', '')}",
                    assume=S6400_ASSUME)


# ---- 2026-10-02 (work group PLUGS): three new plug masters - socket-head ORB plug 6408HHP, hollow-hex pipe plug 5406HHP, square-head
# pipe plug 5406SHP. One master per shape: their rows stay in the 6408 / 5406 review tables (OMi part numbers 6408-HHP-nn-O, 5406-HHP-nn,
# 5406-SHP-nn; Brennan numbers 6408-Hnn-O, 5406-HP-nn, 5406-SHP-nn), the loaders below pick them out, and SPECs 6408 / 5406 skip them
# ('exclude'), so a filled HHP / SHP row can never be built as a hex-head plug or a bushing.
# GEOMETRY measured on the Brennan pilot STEPs (09_STEP_FILES) with tools/measure/plugs.py. The extractor was validated first: it reproduces
# PLUG_HOLE_MEAS -08 / -20 (hole 0.422 / 1.093, full-diameter depth 0.4582 / 0.6345, drill apex 0.580 / 0.950, L 0.800 / 1.200, hex 0.875 /
# 1.875), the ORB library ORB[8] / ORB[20] (thread length 0.344 / 0.469, groove dia 0.660 / 1.507, groove width 0.094 / 0.125) and the
# 5404 end length ENDL[8] = 0.750 (Brennan 5406-08-04) exactly.
#   BRENNAN_6408-H08-O: L 0.580; round head dia 0.875, 0.142 long (= L - the -08 ORB end 0.344 + 0.094), 45deg x 0.0087 chamfers at both
#     head edges; hex socket A/F 0.313 (corner radius 0.1807), 0.188 deep, FLAT bottom, 45deg countersink to dia 0.375 at the face; ORB end
#     = ORB[8] (thread 0.750 to 0.344, groove 0.660 x 0.094) with a 0.0475 x 45deg tip chamfer; O-ring (3-908 section) fused into the solid.
#   BRENNAN_5406-HP-08: L 0.610; hex socket A/F 0.375 (corner radius 0.2165), 0.250 deep, flat bottom, 45deg countersink to dia 0.438;
#     outside: 0.0626 x 45deg tip chamfer, a 1.788deg cone (dia 0.7952 -> 0.8254) to 0.549 from the tip, then a plain dia 0.840 (= pipe OD D)
#     collar 0.061 long to the face.
#   BRENNAN_5406-SHP-08: L 1.020; square head A/F 0.563, SHARP corners (corner radius 0.3981 = 0.563 / sqrt 2), 0.440 long, flat end face,
#     no chamfers; thread end 0.580 to the shoulder: the same tip chamfer / 1.788deg cone (to 0.529) / dia 0.840 collar (0.051 long).
#   The Brennan male NPTF blank (tip chamfer, cone dia 0.7912 extrapolated to the tip, D collar) is the same on all three -08 STEPs and on
#   the bushing 5406-08-04; only where the cone stops differs. The models keep the project's ASME crest cone (end_NPTFMC below).
# DIMENSIONS per row: 6408HHP from the OMi dimension file (Overall Length, Body Diameter = round head, Hex Flat = socket A/F); 5406HHP / 5406SHP
# rows have no OMi / Air-Way dimension - their Brennan catalog values wait in the proposal file (Q-BRENNAN-ONLY) and the rows stay MISSING.
PLUG_PILOT = {
    '6408HHP': dict(step='BRENNAN_6408-H08-O.stp', pn='6408-HHP-08-O', L=0.580, head_dia=0.875, head_len=0.142, sock_af=0.313, sock_depth=0.188, csk_dia=0.375, vol=0.26307),
    '5406HHP': dict(step='BRENNAN_5406-HP-08.stp', pn='5406-HHP-08', L=0.610, sock_af=0.375, sock_depth=0.250, csk_dia=0.438, collar_dia=0.840, cone_end=0.549, vol=0.28030),
    '5406SHP': dict(step='BRENNAN_5406-SHP-08.stp', pn='5406-SHP-08', L=1.020, sq_af=0.563, head_len=0.440, shoulder=0.580, collar_dia=0.840, cone_end=0.529, vol=0.43435),
}


def sock_depth(root, af):
    """hex socket depth: the pilot's depth / across-flats ratio applied to the row's socket A/F (6408HHP 0.188 / 0.313, 5406HHP 0.250 / 0.375).
    ASSUMPTION for every size but the pilot (hex-key engagement taken to scale with the key size); exact for the pilot size."""
    m = PLUG_PILOT[root]
    return round(af * m['sock_depth'] / m['sock_af'], 4)


def sq_head_len(af):
    """square head length: the pilot's head length / across-flats ratio 0.440 / 0.563 applied to the row's A/F (ASSUMPTION except -08)"""
    m = PLUG_PILOT['5406SHP']
    return round(af * m['head_len'] / m['sq_af'], 4)


def end_NPTFMC(dash, sfx, rcap):
    """male NPTF end of a pipe PLUG turned from a blank of the pipe OD: the ASME B1.20.3 crest cone of end_NPTFM (major E0+0.8P at the tip,
    1.7899deg) runs from the tip until it meets the blank radius rcap (= D/2), and the blank carries on from there as the round body - the cone's
    last point lies ON the body line (cap=True: emit() adds no separate body start point and no cone-length dimension; the cone length is driven
    by MAJR, TAPER and BODYR). The crest cone at L2 (E0+0.8P+L2/16) is above D at every size, so the helical thread still runs over L2 and its
    last turns are truncated by the blank (vanish threads), as on a plug turned from D bar. Brennan pilots: blank (collar) dia 0.840 = D."""
    if dash not in NPTF: raise KeyError(lib_gap('NPTF', dash))
    nps, tpi, D, E0, E1, L1, L2 = NPTF[dash]; P = 1 / tpi
    rS = (E0 + 0.8 * P) / 2; xc = (rcap - rS) / math.tan(TAPER)
    if not (0.05 < xc < L2): raise AssertionError(f'crest cone meets the blank radius {rcap} at {xc:.4f} from the tip (expected between 0.05 and L2 {L2})')
    cols = {f'NPTF{sfx}_MAJR@DRIVE': round(rS, 5), f'NPTF{sfx}_TAPER@DRIVE': 1.7899,
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rS, 5), f'HEIGHT@HELIX_{sfx}': L2, f'PITCH@HELIX_{sfx}': round(P, 5),
            f'PROF_R@THDPROF_{sfx}': round(rS, 5), f'APEXR@THDPROF_{sfx}': round(rS - 0.8 * P, 5)}
    return dict(kind='NPTFM', cap=True, V=[(0, rS), (xc, rcap)], endlen=xc, seg=dict(face=0, cone=1), cols=cols, thr=npt_thr(dash) + ' NPTF', faceR=rS * 0.5,
                rS=rS, rL=rcap, L2=L2, P=P, thread=dict(type='HELIX', r=rS, height=L2, pitch=P, thdh=0.8 * P, taper=TAPER, taperOut=True, apexOut=False))


def end_PLAINSOCK(sfx, af, depth):
    """plug head face (plain in the DRIVE profile) with an internal hex socket: across flats af, depth deep, flat bottom (Brennan pilots).
    The socket is its own cut (VBA SocketCut: sketch SOCKET on the face, dimension SOCKAF, blind cut SOCKETCUT); the mouth countersink is not modelled."""
    E = end_PLAIN(sfx)
    E.update(socket=dict(af=af, depth=depth, rc=af / math.sqrt(3)), thr=f'plug head, internal hex socket {af:g} A/F',
             cols={'SOCKAF@SOCKET': af, 'DEPTH@SOCKETCUT': depth})
    return E


def end_SQHEAD(sfx, af, H):
    """square head at End B: revolved at the square's corner radius af / sqrt 2 (rounded UP to 1e-5 so the cylinder never clips the sharp
    corners - Brennan 5406-SHP-08 has sharp corners), then cut to the square over the head length H by ZoneSquareCut (sketch SQUARE,
    dimension SQAF, feature SQCUT); the head end face is plain (no chamfer on the pilot)."""
    rH = math.ceil(af / math.sqrt(2) * 1e5) / 1e5
    cols = {f'SQ{sfx}_HEADR@DRIVE': rH, f'SQ{sfx}_HEADL@DRIVE': H, 'SQAF@SQUARE': af, 'DEPTH@SQCUT': H}
    return dict(kind='SQHEAD', V=[(0, rH), (H, rH)], endlen=H, seg=dict(face=0, top=1), cols=cols, thr=f'square head {af:g} A/F', faceR=rH * 0.5,
                rH=rH, af=af, H=H, thread=None)


def _load_family(root, pat):
    """the rows of one shape family kept in another root's review table (6408-HHP rows in DesignTable_6408, 5406-HHP / -SHP in DesignTable_5406)"""
    h, rows = load_review(root)
    return h, [r for r in rows if re.search(pat, str(r['$PRP@PartNo']))]


PLUG_SOCK_NOTE = ('internal hex socket: one flat horizontal, FLAT bottom, sharp edges (the 45deg mouth countersink of the Brennan pilots NOT modelled); '
                  'depth = the pilot depth / A/F ratio x the row A/F (ASSUMPTION for every size but the pilot)')
SPEC['6408HHP'] = dict(name='ORB Hollow Hex Plug (round head, internal hex socket)', L='L@DRIVE', hex='HEADDIA@REF', round=True, single=True,
                       load=lambda: _load_family('6408', r'^6408-HHP-'),
                       A=lambda r, a, b: end_ORBM(a, 'A'),
                       B=lambda r, a, b: end_PLAINSOCK('B', r['SOCKAF@SOCKET'], sock_depth('6408HHP', r['SOCKAF@SOCKET'])),
                       bore=('socket', None, None), ref='6408-HHP-10-O',
                       assume='GEOMETRY from the Brennan pilot 6408-H08-O STEP (tools/measure/plugs.py): male ORB end from the ORB library (thread major / length, groove dia / width: '
                              '6401 / 6405 / 6410 review tables; -32 from the 6408-32-O-SOLID row + groove width measured on the Brennan 6400-32-32-O STEP) - the pilot carries exactly the '
                              '-08 library end (thread 0.750 to 0.344, groove 0.660 x 0.094); as on 6408: no tip chamfer, the 60deg thread run-out drawn as a step, O-ring not modelled; '
                              'round head (no hex) from the ORB end to L, head dia = OMi "Body Diameter" (column meaning: the pilot head 0.875 equals the -08 hex A/F, and OMi Body Diameter '
                              'equals the 6408 hex A/F at all seven sizes - open question Q-B-OTHER-6408HHP), head edge chamfers (45deg x 0.0087 on the pilot) NOT modelled; '
                              'socket A/F = OMi "Hex Flat" (= Brennan TFA catalog p67 6408-H-O C5 HEX); ' + PLUG_SOCK_NOTE + ' - 6408HHP ratio 0.188 / 0.313 = 0.6006')
SPEC['5406HHP'] = dict(name='Hollow Hex Pipe Plug (NPTF, internal hex socket)', L='L2@DRIVE', hex=lambda r, a, b: NPTF[a][2] if a in NPTF else None, round=True, single=True,
                       load=lambda: _load_family('5406', r'^5406-HHP-'),
                       A=lambda r, a, b: end_NPTFMC(a, 'A', NPTF[a][2] / 2 if a in NPTF else None),
                       B=lambda r, a, b: end_PLAINSOCK('B', r['SOCKAF@SOCKET'], sock_depth('5406HHP', r['SOCKAF@SOCKET'])),
                       bore=('socket', None, None), ref='5406-HHP-08',
                       assume='GEOMETRY from the Brennan pilot 5406-HP-08 STEP (tools/measure/plugs.py): male NPTF per ASME B1.20.3 - crest cone (major E0+0.8P at the tip, 1.7899deg) up to '
                              'where it meets the pipe OD D (ASME B1.20.1), then a round blank of dia D to the head face (the pilot blank / collar is dia 0.840 = D); helical thread over '
                              'L2, its last turns truncated by the D blank (vanish threads); the pilot\'s 45deg tip chamfer and its simplified thread cone (dia 0.791 -> 0.825, then the D collar '
                              '0.061 long) NOT copied - the project\'s ASME crest cone is used as on every male NPTF end (ASSUMPTION); L2 = overall length; socket A/F = Brennan TFA catalog p67 '
                              '5406-HP C HEX; ' + PLUG_SOCK_NOTE + ' - 5406HHP ratio 0.250 / 0.375 = 0.6667')
SPEC['5406SHP'] = dict(name='Square Head Pipe Plug (NPTF)', L='L2@DRIVE', hex=lambda r, a, b: NPTF[a][2] if a in NPTF else None, round=True, single=True,
                       load=lambda: _load_family('5406', r'^5406-SHP-'),
                       A=lambda r, a, b: end_NPTFMC(a, 'A', NPTF[a][2] / 2 if a in NPTF else None),
                       B=lambda r, a, b: end_SQHEAD('B', r['SQAF@SQUARE'], sq_head_len(r['SQAF@SQUARE'])),
                       bore=('none', None, None), ref='5406-SHP-08',
                       assume='GEOMETRY from the Brennan pilot 5406-SHP-08 STEP (tools/measure/plugs.py): male NPTF end as 5406HHP (ASME crest cone capped at the pipe OD D, round D blank up to the '
                              'head shoulder, helical thread over L2, the pilot\'s tip chamfer / simplified cone NOT copied - ASSUMPTION); square head with SHARP corners (pilot: corner radius 0.3981 = '
                              '0.563 / sqrt 2), flat end face, no chamfers, square cut over the head length only (the D collar stays round); L2 = overall length; square A/F = Brennan TFA catalog p67 '
                              '5406-SHP Y FLATS; head length = the pilot ratio 0.440 / 0.563 = 0.7815 x the row A/F (ASSUMPTION except -08)')


# overall lengths measured on the Brennan STEP bundle (inch files, vertex bounding box along the fitting axis)
BRENNAN_OAL = {'6410-12-08-O': (1.480, 'Brennan: male -12 ORB end 0.594 + hex 0.886 carrying the whole -08 port; Air-Way puts the port inside the male end'),
               '6404-08-08': (1.650, 'Brennan: male NPTF end 0.75 + hex 0.90')}


# Brennan 1700 STEPs (JIC tip to flange face; wrench flats on the round collar) for the flagged comparison
BRENNAN_1700 = {'1700-61-08-08': (2.600, 1.000), '1700-61-12-12': (2.750, 1.374), '1700-61-24-24': (3.500, 2.000)}


# ---- 2026-10-18 (genfeat flange): flange straights / plugs with the Brennan body. A16 (user 2026-10-18, Q-NEW-1700BODY "do the same as Brennan"):
# the 1700 rows named without '-61-' (1700-20-16 / -24-20 / -32-24, Brennan catalog + own STEP values) get Brennan's round collar with two wrench
# flats, 30deg chamfer and neck. That is a different DRIVE sketch (collar + chamfer + neck instead of a hex running to the head), so those rows
# cannot share the hex-body 1700 design table: SPEC 1700RC builds them as their own master from DesignTable_1700.xlsx; SPEC 1700 skips them
# (and keeps every Air-Way row exactly as built). Wave-1 groups FLANGE62 (1800 / 1824) and FLANGE61-PLUG (1724), never merged, are merged here
# (their SPECs and gates ported onto the batch-16 toolchain; FLANGE62's 'flats' option now also serves 1700RC).
def flg_cell(r, col):
    if r.get(col) is None: raise KeyError(f'row without {col}')
    return r[col]


def flg61_head(dash):
    if dash not in FLG61_MEAS: raise KeyError(f'code 61 flange head not measured for -{dash:02d}: needs a FLG61_MEAS[{dash}] entry (head thickness, face '
                                              f'groove) measured with tools/measure/flange.py on a Brennan STEP with a -{dash:02d} code 61 head')
    return FLG61_MEAS[dash]


SPEC['1700'].update(exclude=r'^1700-\d\d-\d\d$', exclude_why='round collar with two wrench flats (A16 2026-10-18): built in master 1700RC (other DRIVE sketch)')
SPEC['1700RC'] = dict(name='Code 61 Flange Adapter, round collar (male JIC x SAE code 61 flange head)', L='L28@DRIVE', hex='CHEX@HEX',
                      load=lambda: load_review('1700'), exclude=r'-61-', exclude_why='hex-body 1700 row: built in master 1700',
                      dashre2=r'^1700-(\d\d)-(\d\d)$', flats=dict(collar='COLLARD@DRIVE', zone='FLATL@DRIVE'),
                      A=lambda r, a, b: end_JICM(a, 'A'),
                      B=lambda r, a, b: end_FLG61(b, 'B', flg_cell(r, 'O@DRIVE'), neck=flg_neck(r, a, flg61_head(b), 'L28@DRIVE', 'COLLARD@DRIVE', 'FLATL@DRIVE', 'NECKD@DRIVE',
                                                                                                             also=('CHEX@HEX', 'D@BORE'))),
                      bore=('mid', 'D@BORE', 'D@BORE'), ref='1700-20-16', thrchk=(('A', 'THDMAJ_B@DRIVE', 'a'),),
                      assume='JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan); L28 = JIC tip to the flange face; '
                             + FLG_NECK_ASSUME.format(collar='COLLARD', waf='CHEX', zone='FLATL', neckd='NECKD')
                             + '; neck dia below the wrench flats on these rows, so the flats run out in the 30deg chamfer as on the Brennan 1700 STEPs (the '
                               'flats cut takes nothing below the flats there); SAE code 61 flange head: head thickness and face O-ring groove = FLG61_MEAS by '
                               'flange size (Brennan 1700-08/-12/-16/-20/-24/-32 STEPs, tools/measure/flange.py), head OD = the row O (end library: the head OD '
                               'of that flange size as built in the 1700 master, Q-TRANSFER-ENDLIB 2026-10-08); one through bore D (the smaller bore where the '
                               'own STEP is stepped) cut from both faces to the middle of the round collar; bore chamfer at the flange face and the collar / head '
                               'edge chamfers NOT modelled; single manufacturer (Brennan) -> ASSUMED at most')
SPEC['1800'] = dict(name='Code 62 Flange Adapter (male JIC x SAE code 62 flange head)', L='L@DRIVE', hex='WAF@DRIVE',
                    flats=dict(collar='COLLARD@DRIVE', zone='COLLARL@DRIVE'),
                    A=lambda r, a, b: end_JICM(a, 'A'),
                    B=lambda r, a, b: end_FLG62(b, 'B', neck=flg_neck(r, a, flg62_head(b), 'L@DRIVE', 'COLLARD@DRIVE', 'COLLARL@DRIVE', 'NECKD@DRIVE',
                                                                                     also=('WAF@DRIVE', 'D@BORE'))),
                    bore=('mid', 'D@BORE', 'D@BORE'), ref='1800-08-08', thrchk=(('A', 'THDMAJ_B@DRIVE', 'a'),),
                    assume='JIC end: MS33656J chain per dash (2403 table, VERIFIED vs Brennan; tools/measure/jicm.py on the Brennan 1800-08-08 STEP returns the -08 '
                           'chain exactly); L = JIC tip to the flange face; ' + FLG_NECK_ASSUME.format(collar='COLLARD', waf='WAF', zone='COLLARL', neckd='NECKD')
                           + '; ' + FLG62_ASSUME + '; one through bore D cut from both faces to the middle of the round collar (as the STEP); single manufacturer '
                           '(Brennan) -> ASSUMED at most')
SPEC['1824'] = dict(name='Code 62 Flange Plug (SAE code 62 flange head, solid)', L='L@DRIVE', hex='STUBD@DRIVE', round=True, dashre=r'^1824-(\d\d)',
                    A=lambda r, a, b: (flg_cell(r, 'L@DRIVE'), flg_cell(r, 'STUBD@DRIVE'), end_FLG62(a, 'A'))[-1], B=lambda r, a, b: end_PLAIN('B'),
                    bore=('none', None, None), ref='1824-08',
                    assume='solid plug = the Brennan 1824-08 STEP construction: code 62 flange head (End A = the flange face) on a round stub of dia STUBD to the plain back '
                           'face; L = flange face to the back face; ' + FLG62_ASSUME + '; the 0.0088 x 45deg chamfer at the stub back edge NOT modelled; no thread (no THD_ feature); '
                           'single manufacturer (Brennan) -> ASSUMED at most')
FLG61PLUG_ASSUME = ('code 61 O-ring face FLANGE PLUG (Brennan Flange catalog p.7 drawing + Brennan 1724-08 STEP: solid of revolution, 9 faces): '
                    'End B = SAE code 61 flange head - head thickness and face O-ring groove (inner/outer dia, depth 0.11) per flange size from FLG61_MEAS '
                    '(measured on the Brennan 1700-08/-12/-16/-20/-24/-32 STEPs; the Brennan 1724-08 STEP agrees within 0.0002: TH 0.2650, groove 0.3449 / 0.5000 radius x 0.1098 deep), '
                    'head OD O from the row; body = plain ROUND shank of the row dia SHANKD from the back face to the head (no hex, no wrench flats - as the 1724-08 STEP; '
                    'SOP step 5 exception, question Q-SOP5), L = back face to the flange face; End A = plain flat back face; solid (no bore, no port); '
                    'edge chamfers and the O-ring NOT modelled (the 1724-08 STEP has no chamfers); single manufacturer (Brennan) -> ASSUMED at most')
FLGPLUG_SHOULDER_MIN = 0.03     # 1724: the flange head must stand at least this much (radius) above the round shank - the split flange clamps on that shoulder


def flgplug_row(r, b):
    # 1724: a row that is not MISSING must carry all three of its own values (a partly filled row is skipped with the reason, never half-built); a
    # flange size without FLG61_MEAS (-40) reports that gap first
    flg61_head(b)
    miss = [c for c in ('L@DRIVE', 'SHANKD@REF', 'O@DRIVE') if r.get(c) is None]
    if miss: raise KeyError('1724 row without ' + ' / '.join(miss) + ' (L, shank dia and head OD are all needed)')
    return r['O@DRIVE']


SPEC['1724'] = dict(name='O-Ring Face Code 61 Flange Plug', L='L@DRIVE', hex='SHANKD@REF', round=True, single=True, flgplug=True,
                    A=lambda r, a, b: dict(end_PLAIN('A'), thr='plain back face (solid plug)'), B=lambda r, a, b: end_FLG61(b, 'B', flgplug_row(r, b)),
                    bore=('none', None, None), ref='1724-08', assume=FLG61PLUG_ASSUME)


# ---- 2026-10-20 (ORFS WP2, staging tools/_out/orfs_gen_20261020; plan tools/_out/orfs_modeltype_20261016/PLAN.md, decisions DECISIONS.md):
# SAE J1453 O-ring face-seal (OMi FS...) straights. Every FS series has its own master (Q-FS-MASTER). Review tables: the staged FS tables
# (OMI_REV_EXTRA=tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES). End shapes measured on the Brennan pilots with
# tools/_out/orfs_wp2_20261020/measure/fsmeasure.py (validation: checks.txt there, 0 FAIL; entries: end_lib_08.json).
# Face-seal thread per dash = Air-Way's callout on the FS rows of that dash (680 of the 699 thread cells of the 51 tables; = the Brennan ORFS
# catalog; PLAN section 2 FS_THR).
FS_THR = {4: '9/16-18', 6: '11/16-16', 8: '13/16-16', 10: '1-14', 12: '1 3/16-12', 16: '1 7/16-12', 20: '1 11/16-12', 24: '2-12', 32: '2 1/2-12'}
# MALE FACE-SEAL END (FSM), from the face: flat face from the bore to the groove inner radius GI, rectangular O-ring groove GI -> GO, depth GD
# (the corner under the fused O-ring taken as sharp), land to FR, 45deg nose chamfer to the thread major, thread major to THDS from the face,
# 60deg flank down to the relief RELR, relief to the hex face at the end length ENDL. -08: BRENNAN_FS2403-08-08 (both ends; = the male ends of
# FS6400-08-08-O, and the nose of the forged FS6500 / FS6801 / FS2701 -08 legs, whose run-out differs - gen_tee). The fused O-ring = Air-Way
# FS4000-08 (I.D. 0.489, W 0.070) and is not modelled (as the ORB / NWO ends).
FSM_MEAS = {8: dict(GI=0.2125, GO=0.3145, GD=0.052, FR=0.3595, THDS=0.383, RELR=0.3595, ENDL=0.504)}
FSM_SRC = {8: 'Brennan FS2403-08-08 (both ends) = FS6400-08-08-O (fsmeasure.measure_fsm, orfs_wp2_20261020 checks (1))'}
FSM_CHANG = 45.0; FSM_FLANKANG = 60.0
FSM_ASSUME = ('male O-ring face-seal end (SAE J1453): thread = the face-seal thread of the dash (Air-Way callout = Brennan ORFS catalog); face '
              'O-ring groove (inner / outer dia, depth), land, 45deg nose chamfer, thread length, 60deg flank, relief and end length measured on the '
              'Brennan pilot of that dash ({src}; single manufacturer - Air-Way 3D models not yet measured, Q-FS-2NDSHAPE); groove drawn rectangular '
              '(its outer bottom corner is hidden under the O-ring Brennan fuses into the solid - ASSUMPTION); O-ring not modelled (separate FS4000 part)')


def fs_major(d):
    return frac(FS_THR[d].rsplit('-', 1)[0])


def end_FSM(dash, sfx):
    if dash not in FSM_MEAS: raise KeyError(lib_gap('FSM', dash))
    m = FSM_MEAS[dash]; thr = FS_THR[dash]; TM = fs_major(dash); P_ = 1 / tpi_of(thr); rM = TM / 2
    ch = round(rM - m['FR'], 5)                          # 45deg nose chamfer from the land to the thread major (-08: 0.0468, measured 0.0467)
    fl = (rM - m['RELR']) / TAN60
    if not (m['GI'] < m['GO'] < m['FR'] < rM and m['RELR'] < rM and m['GD'] < m['THDS']): raise AssertionError(f'FSM -{dash:02d} radial / axial order')
    rell = round(m['ENDL'] - m['THDS'] - fl, 5)
    if rell < 0.02: raise AssertionError(f'FSM -{dash:02d}: relief {rell}')
    V = [(0, m['GI']), (m['GD'], m['GI']), (m['GD'], m['GO']), (0, m['GO']), (0, m['FR']), (ch, rM), (m['THDS'], rM), (m['THDS'] + fl, m['RELR']),
         (m['ENDL'], m['RELR'])]
    seg = dict(face=0, gin=1, gbot=2, gout=3, land=4, cham=5, thd=6, flank=7, rel=8)
    cols = {f'FSM{sfx}_GRVIR@DRIVE': m['GI'], f'FSM{sfx}_GRVD@DRIVE': m['GD'], f'FSM{sfx}_GRVOR@DRIVE': m['GO'], f'FSM{sfx}_FACER@DRIVE': m['FR'],
            'FSMCHANG@DRIVE': FSM_CHANG, f'THDMAJR_{sfx}@DRIVE': rM, f'FSM{sfx}_THDL@DRIVE': round(m['THDS'] - ch, 5), 'RELIEFANG@DRIVE': FSM_FLANKANG,
            f'FSM{sfx}_RELR@DRIVE': m['RELR'], f'FSM{sfx}_RELL@DRIVE': rell,
            f'THDDIA@THD_End{sfx}': TM, f'THDPITCH@THD_End{sfx}': round(P_, 5), f'DEPTH@THD_End{sfx}': m['THDS'],
            f'Profile_Height@THD_End{sfx}_PROF': round(0.54127 * P_, 5), f'Profile_Land@THD_End{sfx}_PROF': round(0.25 * P_, 5), f'THDPITCH@THD_End{sfx}_PROF': round(P_, 5)}
    return dict(kind='FSM', V=V, endlen=m['ENDL'], seg=seg, cols=cols, thr=thr + ' UN (male O-ring face seal, SAE J1453)', faceR=(m['GO'] + m['FR']) / 2,
                m=m, rM=rM, ch=ch, rell=rell, dash=dash, assume=FSM_ASSUME.format(src=FSM_SRC[dash]),
                thread=dict(type='CUT', ex=m['THDS'], er=rM, depth=m['THDS'], size=f'{TM:.4f}-{tpi_of(thr):g}', pitch=P_))


# STRAIGHT-THREAD STUD ON AN FS PART (ORB_FS, Q-FS-ORBSTUD (a) "follow Air-Way"): the library ORB end of the dash (thread major, groove dia
# and width) with the thread lengthened so that the stud (tip -> hex face) is Air-Way's length: THDL = stud - groove width. BRENNAN_FS6400-08-08-O:
# undercut 0.660 x 0.094 = ORB[8], tip -> 60deg flank end 0.457 (= Air-Way L8 - L9 0.55 - 0.094 = 0.456; the ORB library -08 thread is 0.344),
# so the extra length is thread, no plain shank (orfs_wp2_20261020 checks); its 0.0475 x 45deg tip chamfer is not modelled (as the ORB end).
ORBFS_ASSUME = ('male SAE ORB stud on an FS part: thread major, groove dia and width = the ORB end library of the dash (6401 / 6405 / 6410 rows); '
                'stud length tip -> hex face = Air-Way ({lcols}) and the extra length over the library end is THREAD (measured on the Brennan '
                'FS6400-08-08-O pilot: undercut 0.660 x 0.094 = ORB -08, thread to 0.457 from the tip; single size - ASSUMED for the other dashes); '
                'tip chamfer and O-ring not modelled')


def end_ORBFS(dash, sfx, stud, lcols):
    if dash not in ORB: raise KeyError(f'no ORB end data for -{dash:02d}')
    o = ORB[dash]
    thdl = round(stud - o['GW'], 4)
    if thdl < o['THDL'] - 0.005: raise AssertionError(f'Air-Way stud {stud} is shorter than the ORB library end {o["THDL"] + o["GW"]:.3f} of -{dash:02d}')
    E = end_ORBM(dash, sfx, row={'THDMAJ_A@DRIVE': o['TM'], 'ORB_THDL@DRIVE': thdl, 'ORB_GRVDIA@DRIVE': o['GD'], 'ORB_GRVW@DRIVE': o['GW']})
    E['thr_note'] = ' (SAE J1926 stud, FS part)'; E['assume'] = ORBFS_ASSUME.format(lcols=lcols); E['lib_thdl'] = o['THDL']
    return E


FS_DIM_SRC = 'review table (Air-Way, staged FS table; OMi website list decides the parts)'
SPEC['FS2403'] = dict(name='ORFS Male Union (male face seal x male face seal)', L='L6@DRIVE', hex='S1HEX@HEX',
                      A=lambda r, a, b: end_FSM(a, 'A'), B=lambda r, a, b: end_FSM(b, 'B'),
                      bore=('mid', 'D1_1@BORE', 'D1_2@BORE'), ref='FS2403-08-08', thrchk=(('A', 'THDMAJ_D_1@DRIVE', 'a'), ('B', 'THDMAJ_D_2@DRIVE', 'b')),
                      fs=True, assume='L6 face -> face, hex S1, bores D1 (both sides): ' + FS_DIM_SRC + '; hex over the whole length between the two ends; '
                                      'bore step at the hex mid-plane (ASSUMPTION, as 2403; no effect where the two bores are equal); hex end chamfers NOT modelled')
SPEC['FS6400'] = dict(name='ORFS Straight Thread Connector (male face seal x male ORB)', L='L8@DRIVE', hex='S5HEX@HEX',
                      A=lambda r, a, b: end_ORBFS(b, 'A', round(r['L8@DRIVE'] - r['L9@DRIVE'], 4), 'L8 - L9'), B=lambda r, a, b: end_FSM(a, 'B'),
                      bore=('mid', 'D20@BORE', 'D1@BORE'), ref='FS6400-08-08-O', thrchk=(('A', 'THDMAJ_N@DRIVE', 'b'), ('B', 'THDMAJ_D@DRIVE', 'a')),
                      fs=True, assume='L8 face -> ORB tip, L9 face -> hex ORB-side face, hex S5, bores D20 (ORB side) / D1 (face-seal side): ' + FS_DIM_SRC +
                                      '; hex = L9 - the face-seal end; bore step at the hex mid-plane (ASSUMPTION, as 2403 / 6400); hex end chamfers NOT modelled; '
                                      'FS6400-L (long, Air-Way L32 / L31) not folded in yet: no shape source for where the extra length goes (needs '
                                      'BRENNAN_FS6400-L-08-08-O)')


# ---- 2026-10-20 (ORFS, staging): loose face-seal parts, -08 measured on the Brennan pilots (tools/_out/orfs_wp2_20261020 end_lib_08.json).
# Other sizes need their own STEP (one pilot gives no per-size rule; the JIC locknut countersink is also measured per size, JICF_MEAS).
# FS0306 bulkhead LOCKNUT (BRENNAN_FS0306-08): face-seal thread through, 45deg countersink on both faces from the minor to FSLOCK_RCS.
FSLOCK_RCS = {8: 0.4095}
# FS0318 NUT (BRENNAN_FS0318-08): thread from the open face to TE, a 0.0046 radial relief (not modelled: the pocket stays at the minor), the
# inner lip face at LIP from the open face, the lip bore through the back face.
FSNUT_MEAS = {8: dict(TE=0.47, LIP=0.63, LIPD=0.652)}
FSLOOSE_ASSUME = {
    'FS0319': ('face-seal braze sleeve (Brennan FS0319-08): length L / collar OD d8 = Air-Way; the shape measured on the -08 pilot (other sizes need '
               'their own STEP): tube-side face r 0.2975, 15deg taper to the spigot r 0.321, collar 0.197 long behind the flat seal face, braze bore '
               'dia 0.506 (1/2 tube + 0.006 braze clearance) to the tube-stop face 0.040 below the seal face, tube-stop bore dia 0.378 - collar length and '
               'stop-lip length held from the seal face, so Air-Way L 0.37 vs the pilot 0.374 shortens the spigot; NOT modelled: the 45deg inner chamfers '
               '(0.005 at the tube-side bore, 0.016 on both stop-lip corners), the 0.006 fillet at the spigot / collar step; single manufacturer'),
    'FS0306': ('face-seal bulkhead locknut (Brennan FS0306-08): hex S4 / thickness h2 = Air-Way; thread = the face-seal thread of the dash through, minor = '
               'ASME B1.1 basic minor; 45deg countersink on both faces from the minor to r 0.4095 measured on the -08 pilot (other sizes need their own '
               'STEP); hex end chamfers (75deg) NOT modelled; single manufacturer'),
    'FS0318': ('face-seal tube nut (Brennan FS0318-08): hex S / length h = Air-Way; thread = the face-seal thread of the dash from the open face over 0.47, '
               'minor = ASME B1.1 basic minor, the thread pocket to the inner lip face at 0.63, lip bore 0.652 through the back face (measured on the -08 '
               'pilot; other sizes need their own STEP); the 0.0046 radial thread relief, the 45deg mouth countersink and the 75deg hex end chamfers NOT '
               'modelled (as the 0318 nut); single manufacturer')}


def fs_nut_csk(dash):
    if dash not in FSLOCK_RCS: raise KeyError(f'face-seal locknut countersink not measured for -{dash:02d}: needs BRENNAN_FS0306-{dash:02d}')
    thr = FS_THR[dash]; TM = fs_major(dash); P_ = 1 / tpi_of(thr); rmin = round((TM - 1.082532 * P_) / 2, 5); rcs = FSLOCK_RCS[dash]
    return dict(TM=TM, thr=thr), P_, rmin, rcs, round(rcs - rmin, 5)


def end_FSNUTCSA(dash, sfx):
    e, P_, rmin, rcs, cs = fs_nut_csk(dash)
    return dict(kind='NUTCSA', V=[(cs, rmin), (0.0, rcs)], endlen=0.0, seg=dict(core=0, csk=1, face=2), faceseg=2,
                cols={f'NUTCS{sfx}_MINR@DRIVE': rmin, f'NUTCS{sfx}_CSR@DRIVE': rcs}, thr=e['thr'] + ' UN (45deg countersink)', faceR=None,
                td=2 * rmin, P1=cs, e=e, rmin=rmin, rcs=rcs, cs=cs, dash=dash, thread=None)


def end_FSNUTCSB(dash, sfx, W):
    e, P_, rmin, rcs, cs = fs_nut_csk(dash)
    cols = {f'NUTCS{sfx}_CSR@DRIVE': rcs, f'NUTCS{sfx}_MINR@DRIVE': rmin,
            f'HELIXDIA@HELIXSK_{sfx}': round(2 * rmin, 5), f'HEIGHT@HELIX_{sfx}': W, f'PITCH@HELIX_{sfx}': round(P_, 5),
            f'PROF_R@THDPROF_{sfx}': rmin, f'APEXR@THDPROF_{sfx}': round(rmin + 0.54127 * P_, 5)}
    return dict(kind='NUTCSB', V=[], VG=[(0.0, rcs), (cs, rmin), (cs, 0.0)], cav=True, endlen=0.0, seg=dict(face=0), cols=cols,
                thr=e['thr'] + ' UN-2B (face-seal locknut thread, through)', faceR=None, td=2 * rmin, P1=cs, e=e, rmin=rmin, rcs=rcs, cs=cs, dash=dash,
                thread=dict(type='HELIX', r=rmin, height=W, pitch=P_, thdh=0.54127 * P_, taper=0.0, taperOut=False, apexOut=True))


def end_FSNUTF(dash, sfx):
    """the FS0318 nut thread end (kind UNFF: thread pocket at the basic minor to the lip face, helical thread over TE)"""
    if dash not in FSNUT_MEAS: raise KeyError(f'face-seal nut not measured for -{dash:02d}: needs BRENNAN_FS0318-{dash:02d}')
    m = FSNUT_MEAS[dash]; thr = FS_THR[dash]; TM = fs_major(dash); P = 1 / tpi_of(thr); td = round(TM - 1.082532 * P, 4)
    cols = {f'TAPDRILL{sfx}@POCKET_{sfx}': td, f'DEPTH@POCKETCUT_{sfx}': m['LIP'],
            f'HELIXDIA@HELIXSK_{sfx}': td, f'HEIGHT@HELIX_{sfx}': m['TE'], f'PITCH@HELIX_{sfx}': round(P, 5),
            f'PROF_R@THDPROF_{sfx}': round(td / 2, 5), f'APEXR@THDPROF_{sfx}': round(td / 2 + 0.54127 * P, 5)}
    return dict(kind='UNFF', V=[], endlen=0.0, seg=dict(face=0), cols=cols, thr=thr + ' UN-2B (face-seal nut)', faceR=None, td=td, P1=m['LIP'], D1=m['LIPD'],
                thread=dict(type='HELIX', r=td / 2, height=m['TE'], pitch=P, thdh=0.54127 * P, taper=0.0, taperOut=False, apexOut=True))


SPEC['FS0306'] = dict(name='ORFS Bulkhead Locknut', L='H2@DRIVE', hex='S4HEX@HEX', single=True, fs=True,
                      A=lambda r, a, b: end_FSNUTCSA(a, 'A'), B=lambda r, a, b: end_FSNUTCSB(a, 'B', r['H2@DRIVE']),
                      bore=('nut_thru', None, None), ref='FS0306-08', thrchk=(('B', 'THDMAJ_D@DRIVE', 'a'),),
                      desc=lambda r, tA, tB: f"ORFS Bulkhead Locknut, {tB.split(' UN')[0]} UN-2B, thread through, 45 deg countersink both faces",
                      assume=FSLOOSE_ASSUME['FS0306'])
SPEC['FS0318'] = dict(name='ORFS Tube Nut', L='H@DRIVE', hex='SHEX@HEX', single=True, fs=True,
                      A=lambda r, a, b: end_FSNUTF(a, 'A'), B=lambda r, a, b: end_PLAIN('B'),
                      bore=('A_to_pocket', lambda r, a, b: FSNUT_MEAS[a]['LIPD'], None), ref='FS0318-08', thrchk=(('A', 'THDMAJ_D@DRIVE', 'a'),),
                      desc=lambda r, tA, tB: f"ORFS Tube Nut, {tA.split(' UN')[0]} UN-2B, lip bore {FSNUT_MEAS[dashes(r['$PRP@PartNo'])[0]]['LIPD']:.3f}", fsnut=True,
                      assume=FSLOOSE_ASSUME['FS0318'])

# 2026-10-20 (ORFS staging): FS0319 braze sleeve = a round straight: End A = tube side (face, 15deg taper, spigot, step up to the collar) with the
# braze bore as its pocket (kind BRAZE), End B = the flat seal face (PLAIN), BORE_B = the tube-stop bore from the seal face to the pocket bottom.
# Shape measured on BRENNAN_FS0319-08 (fsmeasure.measure_sleeve; end_lib_08.json FSSLEEVE_MEAS[8]); radii and the taper angle are shape, the collar
# length and the stop-lip length are held from the seal face (the length L is the Air-Way row input).
FSSLEEVE_MEAS = {8: dict(RT=0.2975, TAPANG=15.0, RS=0.321, COLLARL=0.197, LIPL=0.040, BORER=0.253, STOPR=0.189)}


def end_FSSLV(dash, sfx, L):
    if dash not in FSSLEEVE_MEAS: raise KeyError(f'face-seal braze sleeve not measured for -{dash:02d}: needs BRENNAN_FS0319-{dash:02d}')
    m = FSSLEEVE_MEAS[dash]
    xT = round((m['RS'] - m['RT']) / math.tan(math.radians(m['TAPANG'])), 5); xS = round(L - m['COLLARL'], 5)
    cols = {f'FSSLV{sfx}_FACER@DRIVE': m['RT'], f'FSSLV{sfx}_TAPANG@DRIVE': m['TAPANG'], f'FSSLV{sfx}_SPIGOTR@DRIVE': m['RS'], f'FSSLV{sfx}_SPIGOTL@DRIVE': xS,
            f'SOCKDIA@POCKET_{sfx}': round(2 * m['BORER'], 5), f'DEPTH@POCKETCUT_{sfx}': round(L - m['LIPL'], 5)}
    return dict(kind='BRAZE', fsslv=True, V=[(0.0, m['RT']), (xT, m['RS']), (xS, m['RS'])], endlen=xS, seg=dict(face=0, taper=1, spigot=2, step=3),
                cols=cols, thr=f'braze bore {2 * m["BORER"]:.3f}', faceR=None, td=round(2 * m['BORER'], 5), P1=round(L - m['LIPL'], 5), m=m, xT=xT, xS=xS,
                dash=dash, thread=None)


SPEC['FS0319'] = dict(name='ORFS Braze Sleeve', L='L@DRIVE', hex='D8@DRIVE', round=True, single=True, fs=True,
                      A=lambda r, a, b: end_FSSLV(a, 'A', r['L@DRIVE']), B=lambda r, a, b: end_PLAIN('B'),
                      bore=('A_to_pocket', lambda r, a, b: round(2 * FSSLEEVE_MEAS[a]['STOPR'], 5), None), ref='FS0319-08',
                      desc=lambda r, tA, tB: f"ORFS Braze Sleeve, {tA} x flat seal face (for {r.get('$PRP@TubeOD') or '?'} tube)",
                      thrB_fix=lambda r, a, bv: f'flat seal face (SAE J1453), tube-stop bore {bv:.3f}', assume=FSLOOSE_ASSUME['FS0319'])

def cav_r(E, d):
    # radius of a female port cavity at depth d from its face (piecewise linear over VG; 0 beyond the drill point)
    VG = E['VG']; best = 0.0
    for (x1, r1), (x2, r2) in zip(VG, VG[1:]):
        if x1 - 1e-9 <= d <= x2 + 1e-9:
            rr = max(r1, r2) if x2 - x1 < 1e-9 else r1 + (r2 - r1) * (d - x1) / (x2 - x1)
            best = max(best, rr)
    if E['thread'] and d <= E['thread']['height'] + 1e-9: best = max(best, E['thread']['r'] + E['thread']['thdh'])   # female thread major
    return best


def male_root_r(E, x):
    # smallest material radius of a male end at x from its tip: profile radius, minus the thread depth inside the threaded zone
    V = E['V']; best = None
    for (x1, r1), (x2, r2) in zip(V, V[1:]):
        if x1 - 1e-9 <= x <= x2 + 1e-9:
            rr = min(r1, r2) if x2 - x1 < 1e-9 else r1 + (r2 - r1) * (x - x1) / (x2 - x1)
            best = rr if best is None else min(best, rr)
    if best is None: return None
    t = E.get('thread')
    if t:
        if t['type'] == 'CUT':
            P = t.get('pitch') or (1 / tpi_of(ORB_THR[E['dash']]) if E.get('dash') else None)
            if P and x <= t['depth'] + 1e-9: best = min(best, t['er'] - 0.61343 * P)
        elif t['type'] == 'HELIX' and x <= t['height'] + 1e-9: best = min(best, best - t['thdh'])
    return best


def cav_wall(EP, other, L, rbore):
    # min radial wall between a female port cavity at the End B face and the End A (male) end, where the cavity is wider than the bore
    wmin = None; xw = None
    n = 400
    for i in range(n + 1):
        x = other['endlen'] * i / n                   # End A coordinate
        d = L - x                                    # depth from the port face
        if d > EP['P1'] + 1e-9: continue
        rc = cav_r(EP, d)
        if rc <= rbore + 1e-6: continue
        ro = male_root_r(other, x)
        if ro is None: continue
        w = ro - rc
        if wmin is None or w < wmin: wmin, xw = w, x
    return wmin, xw


def dashes(pn):
    return [int(x) for x in re.findall(r'-(\d\d)', pn)[:2]]


# 2026-10-01 (work group 5404N-06, deployed 2026-10-18 by genfeat straights): smallest radial step allowed between an end's outermost radius
# and a ROUND bar body. A hex body keeps the 0.005 margin below its corner radius (the hex cut must not leave a sliver at the end step). A round
# bar has no hex cut: its body radius is the real outer surface, so the step only has to be real. 0.0025 = half the 0.01 print step of Air-Way's
# bar diameter C (C 0.69 means 0.685..0.695): with at least this step the bar stays above the end's crest cone even if the true C is 0.005
# smaller. 5404N -06: ASME B1.20.3 3/8 NPTF crest cone at L2 = E0 + 0.8P + L2/16 = 0.6819 dia vs C 0.69 -> step 0.0040 (built, with a
# warning); -12: 1.0589 vs 1.06 -> 0.0005 and -16: 1.3259 vs 1.31 -> negative stay BLOCKED. Rows with a step >= 0.005 (every built 5404N
# configuration) are untouched. (tools/_out/tier1_20261001/work/5404N-06/NOTES.md; QA #163: the SolidWorks dry run of 2026-10-01 built the
# -06 bodies but THD_EndA / THD_EndB failed to rebuild in the -06 configurations - the -06 rows carry NEEDS SOLIDWORKS CHECK in $COMMENT.)
ROUND_STEP_MIN = 0.0025
ROUND_STEP_SWCHECK = ('NEEDS SOLIDWORKS CHECK: on 2026-10-01 (QA #163) the thread features THD_EndA / THD_EndB failed to rebuild in every '
                      'configuration with a round-bar step below 0.005 (5404N -06 TEST rows; bodies built) - dry-run and sweep the threads live '
                      'before shipping')


def build_rows(root):
    sp = SPEC[root]; h, rows = sp['load']() if sp.get('load') else load_review(root)     # 2026-10-01: 'load' = a root with folded tables (2403 + 2403-LH, 2404 + 2404-L)
    out = []; skipped = []
    for r in rows:
        pn = r['$PRP@PartNo']
        if (r.get('$PRP@ScopeAction') == 'DROP' and not sp.get('include_drop')) or r.get('$PRP@DataStatus') == 'MISSING': skipped.append((pn, r.get('$PRP@ScopeAction'), r.get('$PRP@DataStatus'))); continue
        if sp.get('exclude') and re.search(sp['exclude'], str(pn)):
            # 2026-10-02 (PLUGS): a row of another shape family kept in this review table (6408-HHP -> SPEC 6408HHP; 5406-HHP / -SHP -> 5406HHP / 5406SHP)
            skipped.append((pn, 'other shape family', sp['exclude_why'])); continue
        if sp.get('skip_blocked') and str(r.get('$COMMENT') or '').startswith('BLOCKED'):
            # 2026-10-01 (2404): rows the review table itself marks BLOCKED (placeholder counterbore depth / unmeasured -40 / -48 pipe end)
            skipped.append((pn, 'BLOCKED in the review table', r.get('$COMMENT'))); continue
        if r.get('_HOLD'):
            # review fix F1 (2026-10-01, SPEC 2404 loader only): a row held for a user decision; the reason names the question
            skipped.append((pn, 'HELD for a user decision', r['_HOLD'])); continue
        if sp.get('solid_only') and r.get('HOLE@BORE') is not None:
            skipped.append((pn, 'hollow variant', 'hole depth unpublished - not built')); continue
        try:
            xlen_ = None
            if sp.get('dashre2'):
                m = re.search(sp['dashre2'], pn)
                m1_ = re.search(sp['dashre1'], pn) if (not m and sp.get('dashre1')) else None
                if m1_:
                    # 2026-10-18 (5404N, user A4): OMi form 5404-N-04X2.500 - one dash for both ends, the cut length after X
                    a = b = int(m1_.group(1)); xlen_ = float(m1_.group(2))
                elif not m: raise KeyError('part number has no dash pair')
                else: a, b = int(m.group(1)), int(m.group(2))
            elif sp.get('dashre'):
                m = re.search(sp['dashre'], pn)
                if not m: raise KeyError('part number has no dash')
                a = b = int(m.group(1))
            elif sp.get('single'):
                if not dashes(pn): raise KeyError('part number has no dash')
                a = b = dashes(pn)[0]
            else:
                if len(dashes(pn)) < 2: raise KeyError('part number has no dash pair')
                a, b = dashes(pn)
            L = r[sp['L']]; hexb = sp['hex'](r, a, b) if callable(sp['hex']) else r[sp['hex']]     # 2026-10-02: callable (PLUGS: pipe OD of the dash)
            EA = sp['A'](r, a, b); EB = sp['B'](r, a, b)
        except (KeyError, AssertionError) as ex:
            skipped.append((pn, 'no end data', repr(ex))); continue
        chk0 = []
        for tc_ in sp.get('thrchk', ()):
            sfx_, col_ = tc_[0], tc_[1]
            E_ = EA if sfx_ == 'A' else EB
            if len(tc_) > 2: d_ = a if tc_[2] == 'a' else b     # explicit: which part-number dash that end is built from
            else: d_ = a if sfx_ == 'A' else b
            if E_['kind'] == 'FSM' or (sp.get('fs') and E_['kind'] in ('NUTCSA', 'NUTCSB', 'UNFF')):      # 2026-10-20 (ORFS): face-seal thread of the dash
                want_ = fs_major(d_)
                if r.get(col_) is None or abs(r[col_] - want_) > 1e-3: chk0.append(f'{col_} {r.get(col_)} does not match the End {sfx_} -{d_:02d} FSM thread ({want_})')
                continue
            if E_['kind'] not in ('JICM', 'JICSW', 'JICF', 'ORBM', 'JICCAP', 'NUTCSB') and d_ not in NPTF: chk0.append(lib_gap('NPTF', d_)); continue
            want_ = (JIC[d_]['TM'] if d_ in JIC else E_['e']['TM']) if E_['kind'] in ('JICM', 'JICSW', 'JICF', 'JICCAP', 'NUTCSB') else ORB[d_]['TM'] if E_['kind'] == 'ORBM' else NPTF[d_][2]   # (d_ not in JIC: a row-supplied JIC chain, SPEC 2404 -40)
            if r.get(col_) is None or abs(r[col_] - want_) > 1e-3: chk0.append(f'{col_} {r.get(col_)} does not match the End {sfx_} -{d_:02d} {E_["kind"]} thread ({want_})')
        if sp.get('p1col') and EB['kind'] == 'NPTFF':
            EB['P1'] = r[sp['p1col']]; EB['cols'][f'DEPTH@POCKETCUT_B'] = EB['P1']; EB['cols']['HEIGHT@HELIX_B'] = EB['P1']; EB['thread']['height'] = EB['P1']
        if EB['thread'] and EB['thread']['type'] == 'HELIX': EB['cols']['PROF_AX@THDPROF_B'] = L
        body = L - EA['endlen'] - EB['endlen']
        rB = hexb / 2 if sp.get('round') else hexb / math.cos(math.radians(30)) / 2
        if sp.get('flats'): rB = r[sp['flats']['collar']] / 2     # 2026-10-18 (1700RC / 1800): round collar - the body radius is the collar, the A/F cuts two flats
        chk = list(chk0); warn = []
        if body < 0.05: chk.append(f'hex length {body:.3f}')
        if xlen_ is not None and (L is None or abs(xlen_ - L) > 1e-6): chk.append(f'length {xlen_:g} in the part number differs from {sp["L"].split("@")[0]} {L}')
        if sp.get('flgplug') and EB['rO'] - rB < FLGPLUG_SHOULDER_MIN:
            # 2026-10-18 (1724, FLANGE61-PLUG): round shank behind the flange head - the head must stand above it (the split flange clamps on that shoulder)
            chk.append(f'flange head dia {2 * EB["rO"]:.4f} is not at least {2 * FLGPLUG_SHOULDER_MIN:.3f} above the shank dia {2 * rB:.4f} (no clamping shoulder)')
        if r.get('_NOTE'): warn.append(r['_NOTE'])
        if r.get('_T20') is not None:
            # 2026-10-01 (2404-L rows): the hex length follows from L20 and the two ends; Air-Way T20 (= hex length) is the cross-check
            dT_ = body - r['_T20']
            if abs(dT_) > 0.02: chk.append(f'hex length {body:.4f} (L20 - both ends) differs from Air-Way T20 {r["_T20"]} by {dT_:+.4f}')
            else: warn.append(f'hex length {body:.4f} (L20 - both ends) vs Air-Way T20 {r["_T20"]}: {"agree" if abs(dT_) <= 0.005 else "differ by %+.4f (L20 printed to 2 decimals)" % dT_}')
        for E in (EA, EB):
            if E['kind'] == 'FLG61': continue          # flange head: its own zone, not hex-cut
            if E['kind'] == 'FLG62' or sp.get('flats'): continue      # 2026-10-18: code 62 head; flats body (the flats zone starts at the collar face)
            for (x, rr) in E['V']:
                if not sp.get('round') and rr > hexb / 2 - 0.002 and rr < rB - 0.005: warn.append(f'{E["kind"]} radius {rr:.4f} is above the hex flats {hexb/2:.4f} - the hex cut will flat it'); break
        model_extra = []    # 2026-10-01 (5404N-06): modelling assumptions that apply to this row only (appended to its $PRP@AxialSource)
        for E in (EA, EB):
            if E['kind'] in ('FLG61', 'FLG62') and (E['kind'] == 'FLG62' or E.get('neck')):
                # 2026-10-18 (FLANGE62 gates, also the 1700RC code 61 head on a neck): the head steps down to the neck (1700RC / 1800) or straight to the
                # body (1824 stub)
                nk_ = E.get('neck')
                if abs(E['rO'] - (nk_['rN'] if nk_ else rB)) < 0.003: chk.append(f'flange head radius {E["rO"]:.4f} equals the {"neck" if nk_ else "body"} radius (zero-height step)')
                if nk_:
                    if nk_['NL'] < 0.02: chk.append(f'neck length {nk_["NL"]:.4f} (L - JIC end - flats zone - head thickness)')
                    if nk_['rN'] > rB - 0.01: chk.append(f'neck dia {2 * nk_["rN"]:.4f} not below the collar dia {2 * rB:.4f} (no 30deg chamfer)')
                    bd_ = r.get(sp['bore'][1]) if isinstance(sp['bore'][1], str) else None
                    if bd_ is not None and nk_['rN'] - bd_ / 2 < 0.03: chk.append(f'neck wall {nk_["rN"] - bd_ / 2:.4f} (neck dia {2 * nk_["rN"]:.4f}, bore {bd_})')
                continue
            if E['kind'] == 'FLG61':
                if abs(E['rO'] - rB) < 0.003: chk.append(f'flange head radius {E["rO"]:.4f} equals the hex corner radius {rB:.4f} (zero-height step)')
                continue
            for (x, rr) in E['V']:
                if E.get('cap') and abs(rr - rB) < 1e-9: continue      # 2026-10-02 (PLUGS): the capped NPTF crest cone ends ON the body (blank) line
                if E['kind'] == 'SQHEAD':
                    # 2026-10-02 (PLUGS): square head corners below the round D collar - its own zone cut, so only a real step is needed (no hex-cut margin)
                    if rr >= rB - 0.001: chk.append(f'square head corner radius {rr:.4f} not below the body radius {rB:.4f} (step < 0.001)')
                    continue
                if rr >= rB - 0.005:
                    if sp.get('round') and rB - rr >= ROUND_STEP_MIN - 1e-9:
                        # round bar (5404N): a small real step from the end of the thread cone to the bar (see ROUND_STEP_MIN)
                        sfx_ = 'A' if E is EA else 'B'
                        msg_ = (f'ROUND-BAR STEP End {sfx_}: bar dia {2 * rB:.4f} (Air-Way C) is only {rB - rr:.4f} (radius) above the '
                                f'{E["kind"]} end at {x:.4f} from its tip (dia {2 * rr:.4f}' + (' = ASME B1.20.3 crest cone E0 + 0.8P + L2/16' if E['kind'] == 'NPTFM' else '') +
                                f') - built with that step (round bar: allowed down to {ROUND_STEP_MIN}, half the 0.01 print step of C; a hex body needs 0.005)')
                        if msg_ not in warn: warn.append(msg_)
                        if ROUND_STEP_SWCHECK not in warn: warn.append(ROUND_STEP_SWCHECK)
                        if not model_extra:
                            model_extra.append(f'round bar only {rB - rr:.4f} (radius) above the {E["kind"]} crest cone at the end of the thread: modelled as that small '
                                               f'step, as at every 5404N size - the vanish threads of the real part (crest cone running on into the bar) are NOT '
                                               f'modelled (ASSUMPTION); allowed because the step is at least {ROUND_STEP_MIN} = half the 0.01 print step of Air-Way C, '
                                               f'so the bar stays above the crest cone even if the true C is 0.005 smaller')
                    else:
                        chk.append(f'{E["kind"]} radius {rr:.3f} >= body radius {rB:.3f}')
        cols = dict(); cols[sp['L'].split('@')[0] + '@DRIVE'] = L; cols['BODYR@DRIVE'] = round(rB, 5)
        if sp.get('flats'):
            # 2026-10-18 (FLANGE62 'flats', 1700RC / 1800): two wrench flats on the round collar, cut outside a centre rectangle (height = A/F, width =
            # collar dia + 0.25) sketched on the Right Plane, blind from the middle of the JIC relief (radius below the flats: nothing is cut there, so the
            # flats begin exactly at the collar face without a coincident start plane) to the neck start = collar face + the flats zone; DEPTH to 8
            # decimals so the cut ends on the neck start of the DRIVE sketch (L - head thickness - NECKL, NECKL to 8 decimals)
            if EA['kind'] != 'JICM': raise ValueError(f'{root}: the flats option needs a male JIC End A (the flats cut starts in its relief)')
            fz_ = r[sp['flats']['zone']]; nk_ = EB.get('neck') or {}
            st_ = round(EA['endlen'] - EA['e']['RL'] / 2, 4)
            cols['WAF@FLATS'] = hexb; cols['FLATW@FLATS'] = round(2 * rB + 0.25, 4)
            cols['START@FLATCUT'] = st_; cols['DEPTH@FLATCUT'] = round(EA['endlen'] + fz_ - st_, 8)
            if hexb / 2 < EA['e']['CD'] / 2 + 0.01: chk.append(f'wrench flats {hexb} reach into the JIC relief (dia {EA["e"]["CD"]}) where the flats cut starts')
            if hexb / 2 > rB - 0.005: chk.append(f'wrench flats {hexb} do not cut the collar (dia {2 * rB:.4f})')
            if nk_ and fz_ - nk_['CL'] < 0.02: chk.append(f'flats zone {fz_} leaves no round collar before the 30deg chamfer ({nk_["CL"]:.4f} long)')
            if abs(cols['START@FLATCUT'] - cols['DEPTH@FLATCUT']) < 1e-4: chk.append('flats cut start offset equals its depth (dimension naming would be ambiguous)')
            bd_ = r.get(sp['bore'][1])
            if bd_ is not None and hexb / 2 - bd_ / 2 < 0.05: chk.append(f'wall under the wrench flats {hexb / 2 - bd_ / 2:.4f}')
            if nk_ and abs(nk_['rN'] - hexb / 2) < 0.003: chk.append(f'neck dia {2 * nk_["rN"]:.4f} equals the wrench flats {hexb} (flats end tangent to the neck)')
        elif not sp.get('round'): cols['HEXB@HEX'] = hexb
        cols.update(EA['cols']); cols.update(EB['cols'])
        # bores
        mode, cA, cB = sp['bore']
        if sp.get('zonehex'):
            cols['DEPTH@HEXCUT'] = round(L - EB['endlen'], 4)
        if mode == 'mid':
            # 2026-10-01: cA / cB may be callables (SPEC 2404 bores from the counterbore columns) and sp['step'] may give the step position
            # from End A (SPEC 2404: MS51500 S); without them this is the unchanged hex mid-plane rule
            bA_ = cA(r, a, b) if callable(cA) else r[cA]; bB_ = cB(r, a, b) if callable(cB) else r[cB]
            st_ = sp['step'](r, EA, EB, L, body) if sp.get('step') else None
            step = round(EA['endlen'] + body / 2, 4) if st_ is None else round(st_, 4)
            cols['DA@BORE_A'] = bA_; cols['DEPTH@BORECUT_A'] = step
            cols['DB@BORE_B'] = bB_; cols['DEPTH@BORECUT_B'] = round(L - step, 4)
            if bA_ / 2 >= EA['V'][0][1] or bB_ / 2 >= EB['V'][0][1]: chk.append('bore >= tip radius')
            for E_, b_ in ((EA, bA_), (EB, bB_)):
                # 2026-10-20 (ORFS): the inner face land between the bore and the O-ring groove (Brennan -08: 0.0235; Air-Way D1 0.37: 0.0275)
                if E_['kind'] == 'FSM' and E_['m']['GI'] - b_ / 2 < 0.01: chk.append(f'bore {b_} leaves {E_["m"]["GI"] - b_ / 2:.4f} of face inside the O-ring groove (dia {2 * E_["m"]["GI"]})')
            if sp.get('step'):
                if not (0.05 < step < L - 0.05): chk.append(f'bore step {step} outside the part (L {L})')
                # radial wall between each bore and the thread root of the male end it runs under (sampled; seat / land / tip excluded)
                wmin_, xw_ = None, None
                for k_ in range(401):
                    x_ = L * k_ / 400; rb_ = (bA_ if x_ < step else bB_) / 2
                    for E_, xe_ in ((EA, x_), (EB, L - x_)):
                        if xe_ > E_['endlen'] + 1e-9: continue
                        rp_ = male_root_r(dict(E_, thread=None), xe_); rr_ = male_root_r(E_, xe_)
                        if rr_ is None or rp_ is None or rr_ >= rp_ - 1e-9: continue      # no thread at this x
                        if wmin_ is None or rr_ - rb_ < wmin_: wmin_, xw_ = rr_ - rb_, x_
                if wmin_ is not None:
                    if wmin_ < 0.015: chk.append(f'wall between a bore and the thread root only {wmin_:.3f} at x={xw_:.3f}')
                    elif wmin_ < 0.03: warn.append(f'thin wall {wmin_:.3f} between a bore and the thread root at x={xw_:.3f}')
        elif mode == 'A_to_pocket':
            bv = cA(r, a, b) if callable(cA) else r[cA]
            EP = EB if EB['kind'] in ('NPTFF', 'BRAZE', 'UNFF', 'ORBF', 'JICF') else EA      # the pocketed end
            if EP is EA:   # pocket at End A -> bore is sketched on the End B face and cut back to the socket bottom
                cols['DB@BORE_B'] = bv; cols['DEPTH@BORECUT_B'] = round(L - EP['P1'], 4)
            else:
                if EP.get('cav'):
                    # female port cavity: run the bore to the bottom of the port's minor bore (depth P from the face), NOT to the drill
                    # point apex - the bore end disk then lies inside the port void and the bore breaks through the drill point / seat
                    # cone where the cone radius equals the bore radius (an apex-deep bore would only touch the cone at one point)
                    cols['DA@BORE_A'] = bv; cols['DEPTH@BORECUT_A'] = round(L - EP['m']['P'], 4)
                    if bv / 2 > EP['rmin'] + 1e-6: chk.append(f'bore {bv} wider than the port minor {2 * EP["rmin"]:.4f}')
                    if EP.get('deep'):   # 2026-10-01 (ORBF-DEEPBORE): bore = port minor -> no drill point, the port ends flat where the bore takes over
                        warn.append(f'DEEP BORE: through-bore {bv} = port minor {2 * EP["rmin"]:.4f} -> port drilled through, no drill point (flat at the minor-bore bottom {EP["m"]["P"]} from the port face; '
                                    f'the 120deg point would have ended {EP["apex60"]:.3f} deep, {L - EP["apex60"]:.3f} from the End A tip)')
                else:
                    cols['DA@BORE_A'] = bv; cols['DEPTH@BORECUT_A'] = round(L - EP['P1'], 4)
            if bv > EP['td'] + 1e-6:
                if sp.get('bore_step_ok') and EP['kind'] == 'NPTFF':
                    warn.append(f'ASSUMPTION: Air-Way bore D {bv} is wider than the port tap drill {EP["td"]} - the bore stops at the port bottom, leaving a {(bv - EP["td"]) / 2:.3f} internal step there (real part unconfirmed)')
                else: chk.append(f'bore {bv} > pocket {EP["td"]}')
            other = EA if EP is EB else EB
            if L - EP['P1'] < 0.02: chk.append(f'pocket depth P1 {EP["P1"]} >= Air-Way L {L}: no room for a bore - page value cannot be right for this size')
            elif sp.get('bushing'):
                nps_, tpi_, D_, E0_, E1_, L1_, L2_ = NPTF[a]
                rootM = E0_ / 2 - 0.4 / tpi_                     # male thread root radius at the tip (smallest)
                crestF = EB['td'] / 2 + 0.8 * EB['thread']['pitch']   # female thread apex radius
                if L - EP['P1'] < L2_:
                    wall = rootM - crestF
                    if wall < 0.015: chk.append(f'wall between female thread ({2*crestF:.3f}) and male thread root ({2*rootM:.3f}) only {wall:.3f}')
                    elif wall < 0.03: warn.append(f'thin wall {wall:.3f} between the female thread and the male thread root (as printed)')
            elif EP.get('cav'):
                # female port cavity: real radial wall between the port (thread major / chamfers / drill point, wherever it is
                # wider than the through bore) and the other end's thread root or groove, sampled along the axis
                wmin, xw = cav_wall(EP, other, L, bv / 2)
                if wmin is not None:
                    if wmin < 0.015: chk.append(f'wall between the female port and the End A thread root/groove only {wmin:.3f} at {xw:.3f} from the End A tip')
                    else: warn.append(f'female port reaches {L - EP["P1"]:.3f} from the End A tip, inside the End A thread/groove zone ({other["endlen"]:.3f}); radial wall there min {wmin:.3f} at {xw:.3f} from the tip' + (' (THIN)' if wmin < 0.03 else ' (OK)'))
            elif EP.get('fsslv'): pass      # 2026-10-20 (ORFS staging, FS0319): the braze bore ends on the tube-stop lip by design (the far end is the plain seal face)
            elif L - EP['P1'] < other['endlen'] + 0.05: warn.append(f'AS-PRINTED WARNING: port drill depth P1 {EP["P1"]} leaves only {L - EP["P1"]:.3f} to the far tip, inside the other end\'s thread/groove region ({other["endlen"]:.3f}) - Air-Way L {L} looks suspect for this size (built as printed)')
            if pn in BRENNAN_OAL:
                bl, bnote = BRENNAN_OAL[pn]
                if abs(bl - L) > 0.10: warn.append(f'DIVERGENT LENGTH: Brennan {pn} STEP overall {bl:.3f} vs Air-Way {sp["L"].split("@")[0]} {L} ({bnote}) - built to Air-Way per the project rule; confirm with OMi')
                else: warn.append(f'Brennan {pn} STEP overall {bl:.3f} vs Air-Way {L}: close (difference {abs(bl - L):.3f}, normal between manufacturers)')
            if EA['V'] and bv / 2 >= EA['V'][0][1]: chk.append('bore >= tip radius')
            if EB['V'] and bv / 2 >= EB['V'][0][1] - 0.002: chk.append(f'bore {bv} >= End B tip dia {2*EB["V"][0][1]:.3f}')
            if sp.get('nut'):
                I1, J1, D1, L1ms, Cms = MS51531[a]
                agree = abs(L - L1ms) <= 0.020 + 1e-9 and abs(hexb - Cms) <= 0.006
                warn.append(f'MS51531D L1 {L1ms:.3f} (+/-.020) / hex {Cms:.4f} vs Air-Way {L} / {hexb}: ' + ('AGREE' if agree else 'DIFFER'))
        elif mode in ('sw1', 'sw2'):
            # swivel End B: the bore(s) run from End A to the nose-tip plane (inside the seat mouth), breaking through the 37deg seat
            # (NPSM swivel: 0.02 past the stem tip, inside the nut cavity)
            sw_ = EB; seat_x = round(L - sw_['bore_to'], 4)
            bB = r[cA] if mode == 'sw1' else r[cB]
            bA = None if mode == 'sw1' else (r.get(cA) if r.get(cA) is not None else bB)
            if bB is None: chk.append('swivel-side bore not published')
            elif mode == 'sw1':
                cols['DA@BORE_A'] = bB; cols['DEPTH@BORECUT_A'] = seat_x
                if EA['kind'] == 'NPTFF' and seat_x <= EA['P1'] + 0.05: chk.append(f'port depth P1 {EA["P1"]} reaches the swivel seat plane {seat_x}')
            else:
                step = round(EA['endlen'] + body / 2, 4)
                cols['DA@BORE_A'] = bA; cols['DEPTH@BORECUT_A'] = step
                cols['DB@BORE_B'] = bB; cols['DEPTH@BORECUT_B'] = round(seat_x - step, 4); cols['START@BORECUT_B'] = step
                if EA['V'] and bA / 2 >= EA['V'][0][1] - 0.002: chk.append(f'bore {bA} >= End A tip dia {2*EA["V"][0][1]:.3f}')
                if r.get(cA) is None: warn.append(f'End A bore not printed by Air-Way (---): D {bB} used through')
            for sw2_, bb_ in ((sw_, bB), (EA, bA)):
                if sw2_['kind'] not in ('JICSW', 'NPSMSW') or bb_ is None: continue
                m_ = sw2_['m']
                if bb_ / 2 >= sw2_['bore_rmax']: chk.append(f'bore {bb_} too large for the swivel {"seat mouth" if sw2_["kind"] == "JICSW" else "stem tip"} (max dia {2*sw2_["bore_rmax"]:.3f})')
                if m_['NECKR'] - bb_ / 2 < 0.03: chk.append(f'neck wall {m_["NECKR"] - bb_ / 2:.3f} (neck dia {2*m_["NECKR"]:.3f}, bore {bb_})')
                if sw2_['kind'] == 'JICSW' and abs(sw2_['s_nt'] - m_['NOSETIP_B']) > 0.02: warn.append(f'Air-Way nut-face-to-seat {sw2_["s_nt"]:.3f} vs Brennan {m_["NOSETIP_B"]:.3f}')
                if sw2_['kind'] == 'NPSMSW' and abs(sw2_['s_tip'] - m_['TIP_B']) > 0.02: warn.append(f'Air-Way nut face to stem tip (W-L) {sw2_["s_tip"]:.3f} vs Brennan {m_["TIP_B"]:.3f}: nut placed at Air-Way W (user decision 2026-09-24)')
                if sw2_['kind'] == 'NPSMSW' and m_['STEMR'] - bb_ / 2 < 0.05: chk.append(f'stem wall {m_["STEMR"] - bb_ / 2:.3f}')
                if m_['NECKR'] >= hexb / 2 - 0.02: chk.append(f'neck dia {2*m_["NECKR"]:.3f} not below the body hex flats {hexb}')
            if EA['kind'] == 'JICSW' and sw_['kind'] == 'JICSW':
                # 2026-10-01 (6565-CAVITY): two JIC swivel seats face each other - each seat cone ends at its own through-bore
                # (trim_seat_at_bore); the bore between the two seat ends must exist, and each seat must end inside the zone of
                # the bore cut that has its diameter (BORE_A: End A face .. bore step, BORE_B: bore step .. End B nose-tip plane)
                rbA_ = round(bA / 2, 5) if bA is not None else None; rbB_ = round(bB / 2, 5) if bB is not None else None
                if rbA_ is None or rbB_ is None or rbA_ >= EA['m']['SEATR'] or rbB_ >= sw_['m']['SEATR'] or mode != 'sw2':
                    chk.append(f'the swivel seat cones cannot end at the through-bore (bores {bA} / {bB} not published or not below the seat mouths)')
                else:
                    xa_ = trim_seat_at_bore(EA, rbA_); xb_ = L - trim_seat_at_bore(sw_, rbB_)
                    step_ = cols['START@BORECUT_B']
                    if xb_ - xa_ < 0.04: chk.append(f'the two swivel seats meet above the through-bore (seat A ends at x={xa_:.3f}, seat B at x={xb_:.3f})')
                    elif xa_ > step_ - 0.02 or xb_ < step_ + 0.02: chk.append(f'a swivel seat ends past the bore step x={step_:.3f} (seat A ends at x={xa_:.3f}, seat B at x={xb_:.3f})')
                    cols['SWA_SEATENDR@DRIVE'] = rbA_; cols['SWB_SEATENDR@DRIVE'] = rbB_
            elif EA['kind'] in ('JICSW', 'NPSMSW') and EA['P1'] > L - EB['P1'] - 0.02: chk.append(f'the two swivel seat cones meet on the axis (apex A {EA["P1"]:.3f}, apex B {L - EB["P1"]:.3f})')
            if bB is not None:
                m_ = sw_['m']
                wmin, xw = cav_wall(sw_, EA, L, bB / 2) if EA['V'] else (None, None)
                if wmin is not None:
                    if wmin < 0.015: chk.append(f'wall between the swivel cavity and the End A thread root only {wmin:.3f} at {xw:.3f}')
                    elif wmin < 0.03: warn.append(f'thin wall {wmin:.3f} between the swivel cavity and the End A thread root at {xw:.3f}')
            if EA['kind'] == 'NPTFF':
                # End A female port vs the swivel neck: the port (thread major) must stay clear of the neck step behind the body hex
                xbody_ = L - sw_['endlen']; rmaj_ = EA['td'] / 2 + 0.8 * EA['thread']['pitch']; m_ = sw_['m']
                dx_ = xbody_ - EA['P1']; dr_ = rmaj_ - m_['NECKR']
                if dr_ > 0:
                    gap_ = math.hypot(max(dx_, 0), dr_) if dx_ > 0 else -1
                    if gap_ < 0.02: chk.append(f'End A port (P1 {EA["P1"]}, thread major dia {2*rmaj_:.3f}) runs into the swivel neck (dia {2*m_["NECKR"]:.3f}) behind the body hex at x={xbody_:.3f}')
                    elif gap_ < 0.04: warn.append(f'thin corner {gap_:.3f} between the End A port bottom and the swivel neck step')
            cols['DEPTH@HEXCUT'] = round(L - sw_['endlen'] - (EA['endlen'] if EA['kind'] == 'JICSW' else 0), 4)
            if EA['kind'] == 'JICSW':
                cols['START@HEXCUT'] = EA['endlen']; cols['NUTHEXA@NUTHEXA'] = EA['nut_af']; cols['DEPTH@NUTCUTA'] = EA['m']['HEXL']
                if abs(cols['START@HEXCUT'] - cols['DEPTH@HEXCUT']) < 1e-4: chk.append('body hex start offset equals its length (dimension naming would be ambiguous)')
            cols['NUTHEX@NUTHEX'] = sw_['nut_af']; cols['DEPTH@NUTCUT'] = sw_['m']['HEXL']
        elif mode == 'B_blind':
            # plug: optional blind hole from the End B tip; $STATE suppresses it on the solid configs
            hole = r[cA]
            if hole is not None:
                dep = round(EB['endlen'] - 0.020, 4)
                cols['DB@BORE_B'] = hole; cols['DEPTH@BORECUT_B'] = dep; cols['$STATE@BORECUT_B'] = 'U'
                if hole / 2 >= EB['V'][0][1] - 0.002: chk.append(f'hole {hole} >= JIC tip dia {2*EB["V"][0][1]:.3f}')
                if dep < 0.1: chk.append(f'hole depth {dep}')
                warn.append('HOLE DEPTH single-source (JIC end length - 0.020, measured on the Brennan 2408-08 STEP only) -> DataStatus ASSUMED')
                r = dict(r); r['$PRP@DataStatus'] = 'ASSUMED'
            else:
                cols['DB@BORE_B'] = None; cols['DEPTH@BORECUT_B'] = None; cols['$STATE@BORECUT_B'] = 'S'
        elif mode == 'A_blind':
            # 2026-09-25 (6408 cored plug): optional blind hole drilled from the End A (ORB) tip; $STATE suppresses it on the solid configs.
            # Brennan 6408-08-O / 6408-20-O STEPs: hole = Air-Way HOLE (0.422 / 1.093), full diameter to 0.020 / 0.040 past the hex face
            # (= ORB end length + e), then a 120deg drill point (not modelled, as on 2408). e interpolated in proportion to the dash.
            hole = r[cA]
            if hole is not None:
                e_ = plug_hole_overshoot(a)
                dep = round(EA['endlen'] + e_, 4)
                cols['DA@BORE_A'] = hole; cols['DEPTH@BORECUT_A'] = dep; cols['$STATE@BORECUT_A'] = 'U'
                rootw = min(male_root_r(EA, EA['endlen'] * k / 50) for k in range(51)) - hole / 2
                apex = dep + hole / 2 / TAN60
                if rootw < 0.05: chk.append(f'hole {hole} leaves {rootw:.3f} under the ORB thread root / groove')
                if L - dep < 0.10: chk.append(f'hole depth {dep} leaves {L - dep:.3f} at the plug head')
                if L - apex < 0.15: chk.append(f'with the 120deg drill point the hole would leave only {L - apex:.3f} at the plug head')
                m_ = PLUG_HOLE_MEAS.get(a)
                if m_:
                    warn.append(f'Brennan 6408-{a:02d}-O STEP: hole {m_[0]:.3f} (Air-Way {hole}), full diameter to {m_[1]:.4f} from the tip (model {dep}), drill-point apex {m_[2]:.3f} -> head wall {L - m_[2]:.3f}; L {m_[3]:.3f}, hex {m_[4]:.3f} (Air-Way {L} / {hexb})')
                else:
                    warn.append(f'HOLE DEPTH interpolated: ORB end {EA["endlen"]:.3f} + {e_:.4f} (Brennan measured 0.020 at -08, 0.040 at -20) -> {dep}; radial wall under the thread root / groove {rootw:.3f}; '
                                f'with a 120deg drill point the head would keep {L - apex:.3f} (Brennan: 0.220 at -08, 0.250 at -20)')
                r = dict(r); r['$PRP@DataStatus'] = 'ASSUMED'
            else:
                cols['DA@BORE_A'] = None; cols['DEPTH@BORECUT_A'] = None; cols['$STATE@BORECUT_A'] = 'S'
        elif mode in ('none', 'pocket_only'):
            if mode == 'pocket_only' and L - EA['P1'] < 0.05: chk.append(f'port depth P1 {EA["P1"]} leaves < 0.05 end wall in L {L}')
        elif mode == 'cav_only':
            # 2026-10-02 (0304 cap): closed crown at End A, female JIC cap cavity at End B, no bore
            crown_ = L - EB['bottom']
            if crown_ < 0.05: chk.append(f'crown {crown_:.4f} thick (L {L} - pocket bottom {EB["bottom"]:.4f}) - below 0.05')
            else: warn.append(f'cap cavity: thread / seat start {EB["m"]["P"]} deep, seat end {EB["seat_end"]:.4f}, pocket dia {2 * EB["rpk"]:.4f} to {EB["bottom"]:.4f} -> crown {crown_:.4f}' + (' (THIN)' if crown_ < 0.08 else ''))
        elif mode == 'nut_thru':
            # 2026-10-02 (0306 locknut): through bore = the thread minor, cut from the End A face over the whole thickness; it removes the
            # construction core of the DRIVE sketch (apex at the origin, flat end behind the End B countersink)
            cols['DA@BORE_A'] = round(2 * EA['rmin'], 5); cols['DEPTH@BORECUT_A'] = L
            thd_ = L - EA['cs'] - EB['cs']
            if thd_ < 0.05: chk.append(f'thread zone between the two countersinks only {thd_:.4f} (W {L})')
        elif mode == 'socket':
            # 2026-10-02 (PLUGS): internal hex socket in the End B (head) face, flat bottom; the plug is solid otherwise
            so_ = EB['socket']; dep_ = so_['depth']; rc_ = so_['rc']
            if dep_ > L - 0.10: chk.append(f'socket depth {dep_} leaves {L - dep_:.3f} (< 0.10) to the End A tip')
            if rc_ > rB - 0.03: chk.append(f'socket corner radius {rc_:.4f} leaves {rB - rc_:.4f} (< 0.03) to the body radius {rB:.4f}')
            wmin_, xw_ = None, None
            for k_ in range(201):
                x_ = L - dep_ + dep_ * k_ / 200
                if x_ <= EA['endlen'] + 1e-9: ro_ = male_root_r(EA, x_)
                elif EA['thread'] and EA['thread']['type'] == 'HELIX' and x_ <= EA['thread']['height'] + 1e-9:
                    ro_ = min(rB, EA['thread']['r'] + x_ * math.tan(EA['thread']['taper'])) - EA['thread']['thdh']   # thread root beyond a capped cone
                else: ro_ = rB
                if ro_ is not None and (wmin_ is None or ro_ - rc_ < wmin_): wmin_, xw_ = ro_ - rc_, x_
            if wmin_ is not None:
                if wmin_ < 0.015: chk.append(f'wall between the socket corners and the End A thread root / groove only {wmin_:.3f} at x={xw_:.3f}')
                elif wmin_ < 0.03: warn.append(f'thin wall {wmin_:.3f} between the socket corners and the End A thread root / groove at x={xw_:.3f}')
            pil_ = PLUG_PILOT.get(root)
            if pil_ and abs(so_['af'] - pil_['sock_af']) > 1e-9:
                warn.append(f'SOCKET DEPTH by the pilot rule: {dep_} = A/F {so_["af"]} x {pil_["sock_depth"]} / {pil_["sock_af"]} (Brennan {pil_["step"][8:-4]}; no source for this size)')
                EB['axnote'] = f'socket depth {dep_} = the {pil_["step"][8:-4]} pilot ratio {pil_["sock_depth"]} / {pil_["sock_af"]} x A/F {so_["af"]} (ASSUMPTION - no published / measured depth for this size)'
            elif pil_:
                warn.append(f'socket depth {dep_} = the Brennan {pil_["step"][8:-4]} pilot (measured)')
        elif mode == 'meet':
            dep = max(EA['P1'], L / 2 + 0.005); cols['DEPTH@POCKETCUT_A'] = round(dep, 4)
            dep = max(EB['P1'], L / 2 + 0.005); cols['DEPTH@POCKETCUT_B'] = round(dep, 4)
            # coupling: the drill holes meet (through), the two helical threads are cut to min(P1, L/2) so they cannot cross each other
            for E, sfx in ((EA, 'A'), (EB, 'B')):
                h = round(min(E['P1'], L / 2), 4); E['cols'][f'HEIGHT@HELIX_{sfx}'] = h; E['thread']['height'] = h
                cols[f'HEIGHT@HELIX_{sfx}'] = h
        for E_ in (EA, EB):
            if E_['kind'] in ('JICCAP', 'NUTCSB'):
                # 2026-10-02: wall between the female thread major (basic major = the JIC thread size) and the hex flats
                w_ = hexb / 2 - E_['e']['TM'] / 2
                if w_ < 0.03: chk.append(f'wall between the thread major dia {E_["e"]["TM"]} and the hex flats {hexb} only {w_:.4f}')
        if pn in PILOT_NUTCAP:
            warn.append(PILOT_NUTCAP[pn] + f' - model: {sp["L"].split("@")[0]} {L}, hex {hexb}' + (
                f', thread minor {2 * EB["rmin"]:.4f} to the seat start {EB["m"]["P"]} (2406 port depth), seat to dia {2 * EB["rpk"]:.4f} at {EB["seat_end"]:.4f}, '
                f'pocket to {EB["bottom"]:.4f}, crown {L - EB["bottom"]:.4f}' if EB['kind'] == 'JICCAP' else
                f', thread minor {2 * EA["rmin"]:.4f} through, countersinks from dia {2 * EA["rcs"]:.4f} ({EA["cs"]:.4f} deep) at both faces') + '; chamfers / marking not modelled')
        if EB['kind'] == 'SQHEAD':
            # 2026-10-02 (PLUGS): the helical NPTF thread must end before the square-head shoulder; head length by the pilot rule
            sh_ = L - EB['endlen']
            if EA['thread'] and EA['thread']['height'] > sh_ - 0.02: chk.append(f'thread length L2 {EA["thread"]["height"]} reaches the square-head shoulder at {sh_:.4f} (< 0.02 left)')
            if sh_ < EA['endlen'] + 0.02: chk.append(f'square head shoulder at {sh_:.4f} is not past the end of the thread cone {EA["endlen"]:.4f}')
            pil_ = PLUG_PILOT['5406SHP']
            if abs(EB['af'] - pil_['sq_af']) > 1e-9:
                warn.append(f'SQUARE HEAD LENGTH by the pilot rule: {EB["H"]} = A/F {EB["af"]} x {pil_["head_len"]} / {pil_["sq_af"]} (Brennan 5406-SHP-08; no source for this size)')
                EB['axnote'] = f'square head length {EB["H"]} = the 5406-SHP-08 pilot ratio {pil_["head_len"]} / {pil_["sq_af"]} x A/F {EB["af"]} (ASSUMPTION - no published / measured length for this size)'
            else:
                warn.append(f'square head length {EB["H"]} = the Brennan 5406-SHP-08 pilot (measured)')
        for E in (EA, EB):
            if E['kind'] in ('NPTFF', 'BRAZE', 'UNFF') and E['td'] >= hexb - 0.05: chk.append(f'pocket {E["td"]} too close to hex {hexb}')
            if E.get('fsslv'):    # 2026-10-20 (ORFS staging, FS0319): walls of the sleeve's own shape at this row's length
                if E['m']['RT'] - E['m']['BORER'] < 0.03: chk.append(f'sleeve wall at the tube-side face {E["m"]["RT"] - E["m"]["BORER"]:.4f}')
                if E['xS'] - E['xT'] < 0.02: chk.append(f'spigot length {E["xS"] - E["xT"]:.4f} (L {L} - collar {E["m"]["COLLARL"]} - taper {E["xT"]})')
                if E['m']['STOPR'] >= E['m']['BORER'] - 0.01: chk.append('tube-stop bore not below the braze bore')
            if E.get('cav') and 2 * E['VG'][0][1] >= (E['nut_af'] if E['kind'] in ('JICSW', 'NPSMSW') else hexb) - 0.05: chk.append(f'port face dia {2*E["VG"][0][1]:.3f} too close to hex {E.get("nut_af", hexb)}')
            if E.get('cav') and E['P1'] >= L - 0.05: chk.append(f'port (apex {E["P1"]:.3f}) runs through the part (L {L})')
        thrA = EA['thr'] or ORB_THR.get(a, '?') + ' ORB'; thrB = EB['thr'] or ORB_THR.get(b, '?') + ' ORB'
        if EA['kind'] == 'ORBM': thrA = ORB_THR[EA['dash'] if sp.get('fs') else a] + ' (male ORB)' + EA.get('thr_note', '')
        if EB['kind'] == 'ORBM': thrB = ORB_THR[EB['dash'] if sp.get('fs') else b] + ' (male ORB)' + EB.get('thr_note', '')
        desc = f"{sp['name']}, {thrA} x {thrB}"
        if sp.get('desc'): desc = sp['desc'](r, thrA, thrB)     # 2026-10-01: SPECs 2403 / 2404 / 2405 keep the description text of their earlier tables
        if EA['kind'] == 'PLAIN': desc = f"{sp['name']}, {thrB}" + (' (hollow)' if cols.get('$STATE@BORECUT_B') == 'U' else ' (solid)' if '$STATE@BORECUT_B' in cols else '')
        if EB['kind'] == 'PLAIN': desc = f"{sp['name']}, {thrA}" + (' (hollow)' if cols.get('$STATE@BORECUT_A') == 'U' else ' (solid)' if ('$STATE@BORECUT_A' in cols or sp.get('solid_only')) else '')
        if sp.get('nut'): thrB = f'tube bore {bv:.3f} (MS51531D D1)'
        if sp.get('fsnut'):   # 2026-10-20 (ORFS staging): the FS0318 tube nut - End B is the lip bore, not a plug head (the PLAIN label above)
            thrB = f'lip bore {bv:.3f} (tube stop, measured on BRENNAN_FS0318-08)'; desc = sp['desc'](r, thrA, thrB)
        if sp.get('thrB_fix'):   # 2026-10-20 (ORFS staging): the FS0319 sleeve - End B is the seal face, not a plug head
            thrB = sp['thrB_fix'](r, a, bv); desc = sp['desc'](r, thrA, thrB)
        if sp.get('ln') and pn.endswith('-LN'): desc += ' (with bulkhead locknut - locknut not modelled)'
        cols['$PRP@PartNo'] = pn; cols['$PRP@Description'] = desc; cols['$PRP@GeometryRoot'] = root
        cols['$PRP@EndA_Thread'] = thrA; cols['$PRP@EndB_Thread'] = thrB
        st_ = r['$PRP@DataStatus']
        if st_ == 'VERIFIED' and any((E_.get('e') or {}).get('src40') for E_ in (EA, EB)):
            # review fix F2 (2026-10-01, SIZE-40): the -40 JIC end is measured on ONE Brennan STEP (JIC40_ASSUME says ASSUMED) - the row cannot stay VERIFIED
            st_ = 'ASSUMED'; warn.append('DataStatus VERIFIED -> ASSUMED: the -40 JIC end (JIC_MEAS_40) is measured on one Brennan STEP - single manufacturer')
        if st_ == 'VERIFIED' and any(E_.get('n40') for E_ in (EA, EB)):
            # 2026-10-18: the -40 pipe end is Brennan-measured (one manufacturer) - the row cannot stay VERIFIED
            st_ = 'ASSUMED'; warn.append('DataStatus VERIFIED -> ASSUMED: the -40 pipe end is measured on Brennan STEPs - single manufacturer')
        if sp.get('fs') and st_ == 'VERIFIED':
            # 2026-10-20 (ORFS, PLAN R8): the face-seal end shapes are measured on Brennan pilots only (Air-Way's own 3D models not yet measured,
            # Q-FS-2NDSHAPE) - single manufacturer, so the row is written ASSUMED; the review table keeps VERIFIED for the dimensions
            st_ = 'ASSUMED'; warn.append('DataStatus VERIFIED -> ASSUMED: the face-seal end shapes are measured on Brennan STEPs only (Air-Way 3D models not yet measured)')
        cols['$PRP@DataStatus'] = 'BLOCKED' if chk else st_
        asm_ = sp['assume'](r) if callable(sp['assume']) else sp['assume']     # review fix F2: SPEC 2404 words its source clause per row
        if sp.get('fs'): asm_ = asm_ + ''.join('; ' + E_['assume'] for E_ in (EA, EB) if E_.get('assume'))
        cols['$PRP@AxialSource'] = (r.get('$PRP@AxialSource') or '') + ' | MODEL: ' + asm_ + ''.join('; ' + m_ for m_ in model_extra)
        # 2026-10-01 (ORB-02): an ORB end merged from another series' row carries its own source note (empty for every older ORB size)
        cols['$PRP@AxialSource'] += ''.join('; ' + E_['o']['note'] for E_ in (EA, EB) if E_.get('kind') == 'ORBM' and E_.get('o', {}).get('note'))
        for E_ in (EA, EB):
            if E_.get('axnote'): cols['$PRP@AxialSource'] += '; ' + E_['axnote']     # per-row modelling assumption (2026-10-01: deep-bore ORB port)
        if r.get('_ASSUME'): cols['$PRP@AxialSource'] += '; ' + r['_ASSUME']     # 2026-10-01: assumptions that touch only some rows (folded 2403-LH / 2404-L rows, 2404 counterbores)
        if any((E_.get('e') or {}).get('src40') for E_ in (EA, EB)): cols['$PRP@AxialSource'] += '; ' + JIC40_ASSUME   # SIZE-40
        if any(E_.get('n40') for E_ in (EA, EB)): cols['$PRP@AxialSource'] += '; ' + NPTF40_ASSUME   # 2026-10-18: -40 pipe end (Brennan-measured)
        if pn in BRENNAN_1700:
            bl_, bf_ = BRENNAN_1700[pn]
            warn.append(f'Brennan {pn.replace("-61", "")} STEP: overall {bl_:.3f} (Air-Way L28 {L}), round collar dia O with wrench flats {bf_:.3f} (Air-Way hex C {hexb}) - built to Air-Way (user decision 2026-09-24)')
        c0 = r.get('$COMMENT') or ''
        for E_ in (EA, EB):
            if E_.get('kind') == 'ORBM' and E_.get('o', {}).get('src') and 'groove width unmeasured' in c0:
                c0 = re.sub(r'(male-)?ORB -32 groove width (UNPUBLISHED and )?unmeasured[^|;]*', 'ORB -32 groove width MEASURED 0.125 on the Brennan 6400-32-32-O STEP (2026-09-24, single source)', c0)
                c0 = re.sub(r'(male-)?ORB -14 groove width (UNPUBLISHED and )?unmeasured[^|;]*', 'ORB -14 groove width MEASURED 0.125 on the Brennan 6400-14-14-O STEP (2026-09-25, single source)', c0)
        if 'defer to MS51520' in c0: c0 += ' -> RESOLVED 2026-09-24 by the Brennan 2705-08-08 STEP: bulkhead thread = the JIC thread of that dash, run over the bulkhead length I1'
        if EB.get('cav') and c0.startswith('BLOCKED: female-JIC internal end geometry'):
            c0 = 'RESOLVED 2026-09-24 for female -08 ports (was: ' + c0[len('BLOCKED: '):] + ') -> port measured on the Brennan 2406-08-08 STEP'
        cols['$COMMENT'] = ' | '.join(x_ for x_ in (c0, ('GEOMETRY CHECK FAILED: ' + '; '.join(chk)) if chk else '', '; '.join(warn)) if x_) or None
        cols['$PRP@OMiSKU'] = r.get('$PRP@OMiSKU')
        for c_ in sp.get('carry', ()): cols[c_] = r.get(c_)     # 2026-10-01 (2404): properties the hand-made table carried (material / finish / pressure)
        out.append((cols, EA, EB, L, hexb, rB, body, chk))
    return out, skipped


def write_sw2(root, built):
    sp = SPEC[root]
    ok = [b for b in built if not b[7]]
    ref = [b for b in ok if b[0]['$PRP@PartNo'] == sp['ref']] or [b for b in ok if b[0]['$PRP@PartNo'] == sp['ref'] + ' TEST'] or ok   # 2026-10-02: a TEST row of the reference size (scratch roots)
    refrow = ref[0]
    ok.sort(key=lambda b: (b[0]['$PRP@PartNo'] != refrow[0]['$PRP@PartNo'], b[0]['$PRP@PartNo']))
    hdr = list(refrow[0].keys())
    for b in ok: assert list(b[0].keys()) == hdr, (b[0]['$PRP@PartNo'], set(b[0].keys()) ^ set(hdr))
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Sheet1'
    ws.append([None] + hdr)
    for b in ok: ws.append([b[0]['$PRP@PartNo']] + [b[0][k] for k in hdr])
    p = f'{OUT}/DesignTable_{root}_SW2.xlsx'; wb.save(p)
    return p, hdr, ok, refrow


# ---- VBA emitter --------------------------------------------------------------------------
HELPERS_SRC = open(os.path.join(P.TEMPLATES, 'Build_2405_MASTER.bas')).read()      # frozen VBA helper library (2405 macro)
GEN_V1 = open(os.path.join(P.TEMPLATES, 'gen_macro_straight_v1.py.txt')).read()   # source text of the v1 generator (HelixThread/MkLine VBA are cut from it)
import importlib.util
spec_ = importlib.util.spec_from_file_location('sp3fix', os.path.join(P.GENERATORS, 'sp3fix.py')); sp3 = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(sp3)


def sub(text, name, kind='Sub'):
    i = text.index(f'\n{kind} {name}('); j = text.index(f'\nEnd {kind}', i) + len(f'\nEnd {kind}')
    return text[i + 1:j] + '\n'


HELP = ''.join(sub(HELPERS_SRC, n) for n in ('Trace', 'Check', 'NameDim', 'NameAng', 'Dim_len', 'Dim_ptline', 'Dim_len2', 'Dim_rad', 'DeleteDisp', 'Collinear', 'BoreCut', 'ThreadCut'))
HELP += '''Sub Dim_pair(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    ' distance between two parallel sketch lines seg(i) and seg(j) (overall length when End B is a port cavity)
    swModel.ClearSelection2 True
    seg(i).Select4 False, Nothing
    seg(j).Select4 True, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
End Sub
'''
HELP = HELP.replace('''        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check nm & " dims: " & names, InStr(names, "DEPTH=") > 0 And InStr(names, "THDDIA=") > 0 And InStr(names, "THDPITCH=") > 0''', '''        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Trace nm & ": dim full name " & dm.FullName
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check nm & " dims: " & names, InStr(names, "DEPTH=") > 0 And InStr(names, "THDDIA=") > 0 And InStr(names, "THDPITCH=") > 0
    Dim sf As SldWorks.Feature: Set sf = f.GetFirstSubFeature
    Do While Not sf Is Nothing
        If Left(sf.Name, 14) = "Thread Profile" Then sf.Name = nm & "_PROF": Trace nm & ": profile sketch " & IIf(Err.Number <> 0, "rename FAILED " & Err.Description, "renamed to " & sf.Name): Err.Clear
        Set sf = sf.GetNextSubFeature
    Loop
    Check nm & " profile dims reachable as Profile_Height@" & nm & "_PROF", Not swModel.Parameter("Profile_Height@" & nm & "_PROF") Is Nothing''')
assert 'dim full name' in HELP
HELP += sp3.DIMANG + '\n\n'
HELP += ''.join(sub(HELPERS_SRC, n, 'Function') for n in ('MakeCut', 'MakeCut2', 'SelectCircEdge', 'SelectEndFace', 'FeatCentreX', 'Volume'))

DIMPT = """Sub DimPtOrigin(pt As SldWorks.SketchPoint, nm As String, expectM As Double, axialIsX As Boolean, axialDim As Boolean, u0 As Double, v0 As Double, ou As Double, ov As Double)
    ' point-to-origin dimension with an EXPLICIT type (horizontal = sketch X, vertical = sketch Y).
    ' v1 used AddDimension2 and let SolidWorks pick the type from the text position; that only worked when the
    ' point sat on the origin's X (End A, tipAx = 0) - at End B it produced aligned dims and the profile stayed under-defined.
    On Error Resume Next
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double, tx As Double, ty As Double, wantX As Boolean
    wantX = (axialDim = axialIsX)
    For k = 0 To 3
        tx = (u0 + ou) / 2: ty = (v0 + ov) / 2
        If wantX Then ty = ty + IIf(k Mod 2 = 0, 1, -1) * 0.02 * (1 + k \\ 2) Else tx = tx + IIf(k Mod 2 = 0, 1, -1) * 0.02 * (1 + k \\ 2)
        swModel.ClearSelection2 True
        pt.Select4 False, Nothing
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        Err.Clear
        If wantX Then
            Set dd = swModel.AddHorizontalDimension2(tx, ty, 0)
        Else
            Set dd = swModel.AddVerticalDimension2(tx, ty, 0)
        End If
        If dd Is Nothing Then
            Trace nm & ": try " & k & " explicit " & IIf(wantX, "horizontal", "vertical") & " dim returned Nothing" & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "") & " - falling back to AddDimension2"
            Err.Clear
            swModel.ClearSelection2 True
            pt.Select4 False, Nothing
            swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
            Set dd = swModel.AddDimension2(tx, ty, 0)
        End If
        If dd Is Nothing Then
            Trace nm & ": try " & k & " no dimension created (selection count " & swSelMgr.GetSelectedObjectCount2(-1) & ")"
        Else
            v = dd.GetDimension2(0).SystemValue
            Trace nm & ": try " & k & " value " & Format(v / IN_, "0.0000") & " (want " & Format(expectM / IN_, "0.0000") & ")"
            If Abs(v - expectM) < 0.000005 Then Exit For
            DeleteDisp dd: Set dd = Nothing
        End If
    Next k
    NameDim dd, nm, expectM
End Sub
"""

HX = sub(GEN_V1, 'HelixThread') + sub(GEN_V1, 'MkLine', 'Function') + DIMPT
HX = HX.replace('taperRad As Double, apexOut As Boolean', 'taperRad As Double, taperOut As Boolean, apexOut As Boolean')
HX = HX.replace('mdLate.InsertHelix True, True, (taperRad > 0), False,', 'mdLate.InsertHelix True, True, (taperRad > 0), taperOut,')
HX = HX.replace('\\"', '"')
HELP += HX

AXISCOV = """Function AxisCovered(fx As Double) As Boolean
    ' True when a planar face normal to X at x = fx contains the axis point (fx, 0, 0), i.e. the bore is NOT open there
    On Error Resume Next
    Dim bods As Variant, bd As SldWorks.Body2, faces As Variant, i As Long, fc As SldWorks.Face2, sf As SldWorks.Surface, pp As Variant, cp As Variant
    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bods) Then Exit Function
    Set bd = bods(0)
    faces = bd.GetFaces
    For i = LBound(faces) To UBound(faces)
        Set fc = faces(i)
        Set sf = fc.GetSurface
        If sf.IsPlane Then
            pp = sf.PlaneParams
            If Abs(Abs(pp(0)) - 1) < 0.0001 And Abs(pp(3) - fx) < 0.00002 Then
                cp = fc.GetClosestPointOn(fx, 0#, 0#)
                If Abs(cp(1)) < 0.000002 And Abs(cp(2)) < 0.000002 Then AxisCovered = True: Exit Function
            End If
        End If
    Next i
End Function
"""
HELP += AXISCOV

SUPPEV = """Function SuppressEverywhere(ft As SldWorks.Feature) As Long
    ' suppress one feature in every configuration; returns the number of configurations where it is still live
    On Error Resume Next
    Dim names As Variant, i As Long, r As Boolean, st As Variant, live As Long, msg As String
    names = swModel.GetConfigurationNames
    Err.Clear
    r = ft.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)
    msg = ft.Name & ": SetSuppression2(all configs) -> " & r & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "")
    Err.Clear
    For i = LBound(names) To UBound(names)
        r = ft.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swSpecifyConfiguration, Array(names(i)))
    Next i
    st = ft.IsSuppressed2(swInConfigurationOpts_e.swAllConfiguration, Empty)
    live = 0
    If IsArray(st) Then
        For i = LBound(st) To UBound(st)
            If Not st(i) Then live = live + 1
        Next i
        msg = msg & "; per-config check: " & (UBound(st) - LBound(st) + 1) & " configs, " & live & " still live"
    Else
        If Not ft.IsSuppressed Then live = 1
        msg = msg & "; IsSuppressed2 unavailable, active config " & IIf(ft.IsSuppressed, "suppressed", "LIVE")
    End If
    Trace msg
    SuppressEverywhere = live
End Function
"""
HELP += SUPPEV
ZONEHEX = """Function ZoneHexCut(onEndB As Boolean, faceXM As Double, afM As Double, startM As Double, depthM As Double, wantCxM As Double, skName As String, dimName As String, featName As String) As SldWorks.Feature
    ' hex prism cut limited to one axial zone: sketch a hexagon (across flats afM) on the Right Plane (End A tip) or on the
    ' End B face, cut the OUTSIDE of it blind over depthM into the part (direction tried both ways, kept where it removes material)
    On Error Resume Next
    Dim ok As Boolean
    swModel.ClearSelection2 True
    If onEndB Then
        ok = SelectEndFace(faceXM)
    Else
        ok = swModel.Extension.SelectByID2("Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    End If
    Check skName & ": sketch plane selected (" & IIf(onEndB, "End B face", "Right Plane") & ")", ok
    swSkMgr.InsertSketch True
    Dim poly As Variant, k As Long, circ As SldWorks.SketchSegment
    poly = swSkMgr.CreatePolygon(0, 0, 0, afM / 2, 0, 0, 6, True)
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
    Next k
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(afM * 0.7, afM * 0.7, 0)
    If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = afM
    NameDim dd, dimName, afM
    swModel.ClearSelection2 True
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL": Exit For
    Next k
    swModel.ClearSelection2 True
    Dim arc As SldWorks.SketchArc
    Set arc = circ
    arc.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim skF As SldWorks.Feature
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long, fLo As Double, fHi As Double, okPos As Boolean, startZ As Double
    ' the zone this cut must stay in (x from the End A tip): [startM, startM + depth] from End A, [faceX - depth, faceX] from the End B face
    startZ = IIf(onEndB, faceXM - depthM, startM)
    v0 = Volume()
    For attempt = 0 To IIf(startM > 0, 3, 1)
        Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, True, (attempt Mod 2 = 1), startM, (attempt >= 2), featName & " attempt " & attempt)
        If Not cut Is Nothing Then
            v1 = Volume()
            FeatSpanX cut, fLo, fHi
            okPos = (fLo > startZ - 0.0005) And (fHi < startZ + depthM + 0.0005) And (fHi > fLo)
            Trace featName & " attempt " & attempt & ": removed " & Format((v0 - v1) / IN_ ^ 3, "0.00000") & " in^3, new faces span x=" & Format(fLo / IN_, "0.0000") & ".." & Format(fHi / IN_, "0.0000") & " (zone " & Format(startZ / IN_, "0.0000") & ".." & Format((startZ + depthM) / IN_, "0.0000") & ")"
            If v1 < v0 - 1E-12 And okPos Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next attempt
    Check featName & " created in the right zone and removed material (attempt " & attempt & ")", Not cut Is Nothing
    If cut Is Nothing Then Exit Function
    cut.Name = featName
    Check featName & " removed only the corners (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.6 * v0)
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = cut.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then
            dm.Name = "DEPTH"
        ElseIf startM > 0 And Abs(dm.SystemValue - startM) < 0.000001 Then
            dm.Name = "START"
        End If
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = cut.GetNextDisplayDimension(d)
    Loop
    Check featName & " dims: " & names, InStr(names, "DEPTH=") > 0 And (startM = 0 Or InStr(names, "START=") > 0)
    Set ZoneHexCut = cut
End Function
"""
HELP += ZONEHEX
# 2026-10-18 (genfeat flange; FLANGE62 1800, now also 1700RC): two wrench flats on a round collar. Appended ONLY to macros of a SPEC with 'flats' (emit),
# so every other macro text stays as it was. Same cut logic as ZoneHexCut (blind cut with a start offset from the Right Plane, both directions tried,
# kept where it removes material inside the zone); the sketch is a centre rectangle instead of a hexagon. Ported verbatim from FLANGE62/patch.diff.
FLATSCUT = """
Function FlatsCut(afM As Double, wM As Double, startM As Double, depthM As Double, skName As String, dimAF As String, dimW As String, featName As String) As SldWorks.Feature
    ' two wrench flats across afM on a round collar: a centre rectangle (height afM = across the flats, width wM wider than the collar)
    ' sketched on the Right Plane (the End A tip plane), its OUTSIDE cut blind over depthM, starting startM from the sketch plane
    On Error Resume Next
    Dim ok As Boolean
    swModel.ClearSelection2 True
    ok = swModel.Extension.SelectByID2("Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
    Check skName & ": sketch plane selected (Right Plane)", ok
    swSkMgr.InsertSketch True
    Dim fcR As Variant, fcK As Long, fcSg As SldWorks.SketchSegment, fcLn As SldWorks.SketchLine, fcNs As Long
    Dim fcV As SldWorks.SketchSegment, fcH As SldWorks.SketchSegment, fcD As SldWorks.SketchSegment
    fcR = swSkMgr.CreateCenterRectangle(0, 0, 0, wM / 2, afM / 2, 0)
    If IsEmpty(fcR) Then
        Check skName & ": centre rectangle created", False
        swSkMgr.InsertSketch True
        Exit Function
    End If
    fcNs = 0
    For fcK = LBound(fcR) To UBound(fcR)
        Set fcSg = fcR(fcK)
        If fcSg.GetType = swSketchSegments_e.swSketchLINE Then
            Set fcLn = fcSg
            If fcSg.ConstructionGeometry Then
                If fcD Is Nothing Then Set fcD = fcSg
            Else
                fcNs = fcNs + 1
                If Abs(fcLn.GetStartPoint2.X - fcLn.GetEndPoint2.X) < 0.0000001 Then
                    Set fcV = fcSg
                ElseIf Abs(fcLn.GetStartPoint2.Y - fcLn.GetEndPoint2.Y) < 0.0000001 Then
                    Set fcH = fcSg
                End If
            End If
        End If
    Next fcK
    Trace skName & ": centre rectangle -> " & (UBound(fcR) - LBound(fcR) + 1) & " segments, " & fcNs & " sides, construction diagonal " & IIf(fcD Is Nothing, "none", "found")
    Check skName & ": rectangle has a vertical and a horizontal side", (Not fcV Is Nothing) And (Not fcH Is Nothing)
    If fcV Is Nothing Or fcH Is Nothing Then
        swSkMgr.InsertSketch True
        Exit Function
    End If
    ' across flats = the length of a vertical side (sketch Y = model Y on the Right Plane); width = the length of a horizontal side
    Dim dd As SldWorks.DisplayDimension
    swModel.ClearSelection2 True
    fcV.Select4 False, Nothing
    Set dd = swModel.AddDimension2(0, 0, wM * 0.7)
    NameDim dd, dimAF, afM
    swModel.ClearSelection2 True
    fcH.Select4 False, Nothing
    Set dd = swModel.AddDimension2(0, afM * 0.7, 0)
    NameDim dd, dimW, wM
    ' centre the rectangle on the axis: the origin at the middle of the construction diagonal; fallback = the centre point on the origin
    Dim fcSk As SldWorks.Sketch
    Set fcSk = swSkMgr.ActiveSketch
    Trace skName & ": constrained status after the two dimensions = " & fcSk.GetConstrainedStatus
    If fcSk.GetConstrainedStatus <> swConstrainedStatus_e.swFullyConstrained And Not fcD Is Nothing Then
        swModel.ClearSelection2 True
        fcD.Select4 False, Nothing
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        swModel.SketchAddConstraints "sgATMIDDLE"
        Trace skName & ": origin at the middle of the diagonal -> status " & fcSk.GetConstrainedStatus
    End If
    If fcSk.GetConstrainedStatus <> swConstrainedStatus_e.swFullyConstrained Then
        Dim fcPts As Variant, fcP As SldWorks.SketchPoint
        fcPts = fcSk.GetSketchPoints2
        If Not IsEmpty(fcPts) Then
            For fcK = LBound(fcPts) To UBound(fcPts)
                Set fcP = fcPts(fcK)
                If Abs(fcP.X) < 0.0000001 And Abs(fcP.Y) < 0.0000001 Then
                    swModel.ClearSelection2 True
                    fcP.Select4 False, Nothing
                    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
                    swModel.SketchAddConstraints "sgCOINCIDENT"
                    Trace skName & ": centre point made coincident with the origin -> status " & fcSk.GetConstrainedStatus
                    Exit For
                End If
            Next fcK
        End If
    End If
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim skF As SldWorks.Feature
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim v0 As Double, v1 As Double, cut As SldWorks.Feature, attempt As Long, fLo As Double, fHi As Double, okPos As Boolean
    v0 = Volume()
    For attempt = 0 To 3
        Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, True, (attempt Mod 2 = 1), startM, (attempt >= 2), featName & " attempt " & attempt)
        If Not cut Is Nothing Then
            v1 = Volume()
            FeatSpanX cut, fLo, fHi
            okPos = (fLo > startM - 0.0005) And (fHi < startM + depthM + 0.0005) And (fHi > fLo)
            Trace featName & " attempt " & attempt & ": removed " & Format((v0 - v1) / IN_ ^ 3, "0.00000") & " in^3, new faces span x=" & Format(fLo / IN_, "0.0000") & ".." & Format(fHi / IN_, "0.0000") & " (zone " & Format(startM / IN_, "0.0000") & ".." & Format((startM + depthM) / IN_, "0.0000") & ")"
            If v1 < v0 - 1E-12 And okPos Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next attempt
    Check featName & " created in the flats zone and removed material (attempt " & attempt & ")", Not cut Is Nothing
    If cut Is Nothing Then Exit Function
    cut.Name = featName
    Check featName & " removed only the two collar segments (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.6 * v0)
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = cut.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then
            dm.Name = "DEPTH"
        ElseIf Abs(dm.SystemValue - startM) < 0.000001 Then
            dm.Name = "START"
        End If
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = cut.GetNextDisplayDimension(d)
    Loop
    Check featName & " dims: " & names, InStr(names, "DEPTH=") > 0 And InStr(names, "START=") > 0
    Set FlatsCut = cut
End Function
"""
HELP += """Sub FeatSpanX(f As SldWorks.Feature, lo As Double, hi As Double)
    ' x-range (along the straight's axis) of the faces a feature created
    On Error Resume Next
    Dim faces As Variant, i As Long, bx As Variant
    lo = 1E+30: hi = -1E+30
    faces = f.GetFaces
    If IsEmpty(faces) Then lo = 0: hi = 0: Exit Sub
    For i = LBound(faces) To UBound(faces)
        bx = faces(i).GetBox
        If bx(0) < lo Then lo = bx(0)
        If bx(3) > hi Then hi = bx(3)
    Next i
End Sub
"""
# 2026-10-02 (PLUGS): helpers emitted ONLY into the macros that use them (every other macro stays byte-identical):
# SocketCut - the internal hex socket of the 6408HHP / 5406HHP plugs; ZoneSquareCut - the square head of 5406SHP (ZoneHexCut with 4 sides)
SOCKETCUT = """
Function SocketCut(faceXM As Double, afM As Double, depthM As Double, skName As String, dimName As String, featName As String) As SldWorks.Feature
    ' 2026-10-02 (PLUGS): internal hex socket in the plug head face (End B, x = faceXM): a hexagon of across flats afM (dimension on the
    ' polygon's construction circle, one side horizontal, centre on the axis) sketched ON that face and cut blind depthM INTO the part
    ' (both directions tried; kept where it removes material between faceX - depth and faceX). Flat bottom, as on the Brennan pilot STEPs.
    On Error Resume Next
    Dim ok As Boolean
    swModel.ClearSelection2 True
    ok = SelectEndFace(faceXM)
    Check skName & ": head face selected at x=" & Format(faceXM / IN_, "0.0000"), ok
    swSkMgr.InsertSketch True
    Dim poly As Variant, k As Long, circ As SldWorks.SketchSegment
    poly = swSkMgr.CreatePolygon(0, 0, 0, afM / 2, 0, 0, 6, True)
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
    Next k
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(afM * 0.7, afM * 0.7, 0)
    If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = afM
    NameDim dd, dimName, afM
    swModel.ClearSelection2 True
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL": Exit For
    Next k
    swModel.ClearSelection2 True
    Dim arc As SldWorks.SketchArc
    Set arc = circ
    arc.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim skF As SldWorks.Feature
    Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
    Check skName & " sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim v0 As Double, v1 As Double, vexp As Double, cut As SldWorks.Feature, attempt As Long, fLo As Double, fHi As Double, okPos As Boolean
    vexp = Sqr(3#) / 2# * afM * afM * depthM
    v0 = Volume()
    For attempt = 0 To 1
        Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, False, (attempt = 1), 0#, False, featName & " attempt " & attempt)
        If Not cut Is Nothing Then
            v1 = Volume()
            FeatSpanX cut, fLo, fHi
            okPos = (fLo > faceXM - depthM - 0.0005) And (fHi < faceXM + 0.0005) And (fHi > fLo)
            Trace featName & " attempt " & attempt & ": removed " & Format((v0 - v1) / IN_ ^ 3, "0.00000") & " in^3 (hex prism " & Format(vexp / IN_ ^ 3, "0.00000") & "), new faces span x=" & Format(fLo / IN_, "0.0000") & ".." & Format(fHi / IN_, "0.0000")
            If v1 < v0 - 1E-12 And okPos Then Exit For
            swModel.ClearSelection2 True
            cut.Select2 False, 0
            swModel.Extension.DeleteSelection2 0
            Set cut = Nothing
        End If
    Next attempt
    Check featName & " created in the head and removed material (attempt " & attempt & ")", Not cut Is Nothing
    If cut Is Nothing Then Exit Function
    cut.Name = featName
    Check featName & " removed the hex prism volume (" & Format((v0 - v1) / IN_ ^ 3, "0.00000") & " vs " & Format(vexp / IN_ ^ 3, "0.00000") & " in^3)", Abs((v0 - v1) - vexp) < 0.01 * vexp
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = cut.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then dm.Name = "DEPTH"
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = cut.GetNextDisplayDimension(d)
    Loop
    Check featName & " dims: " & names, InStr(names, "DEPTH=") > 0
    Set SocketCut = cut
End Function
"""
ZONESQ = ZONEHEX
for _o, _n in (('Function ZoneHexCut(', 'Function ZoneSquareCut('), ('Set ZoneHexCut = cut', 'Set ZoneSquareCut = cut'),
               ('CreatePolygon(0, 0, 0, afM / 2, 0, 0, 6, True)', 'CreatePolygon(0, 0, 0, afM / 2, 0, 0, 4, True)'),
               ("    ' hex prism cut limited to one axial zone: sketch a hexagon (across flats afM)",
                "    ' 2026-10-02 (PLUGS): ZoneHexCut with 4 sides - SQUARE prism cut limited to one axial zone: sketch a square (across flats afM)")):
    assert ZONESQ.count(_o) == 1, _o
    ZONESQ = ZONESQ.replace(_o, _n)
ZONESQ = '\n' + ZONESQ

# threads: suppression governed by one constant
HELP = HELP.replace('sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)\n    Check nm & " suppressed", sup',
                    'If SUPPRESS_THREADS Then\n        sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)\n        Check nm & " suppressed (resting state)", sup\n    Else\n        Trace nm & ": left UNSUPPRESSED (SUPPRESS_THREADS = False)"\n    End If')
assert HELP.count('SUPPRESS_THREADS') >= 2, HELP.count('SUPPRESS_THREADS')

# 2026-09-24: rename the thread-profile pitch dimension explicitly (library profile of a non-16-tpi reference size keeps "Pitch")
_OLDP = """    Check nm & " profile dims reachable as Profile_Height@" & nm & "_PROF", Not swModel.Parameter("Profile_Height@" & nm & "_PROF") Is Nothing"""
_NEWP = _OLDP + """
    Dim pfq As SldWorks.Feature, pdq As SldWorks.DisplayDimension, pmq As SldWorks.Dimension
    Set pfq = swModel.FeatureByName(nm & "_PROF")
    If Not pfq Is Nothing Then
        Set pdq = pfq.GetFirstDisplayDimension
        Do While Not pdq Is Nothing
            Set pmq = pdq.GetDimension2(0)
            If LCase(pmq.Name) = "pitch" Then pmq.Name = "THDPITCH": Trace nm & ": profile pitch dimension renamed Pitch -> THDPITCH"
            Set pdq = pfq.GetNextDisplayDimension(pdq)
        Loop
    End If
    Check nm & " profile pitch reachable as THDPITCH@" & nm & "_PROF", Not swModel.Parameter("THDPITCH@" & nm & "_PROF") Is Nothing"""
HELP = HELP.replace(_OLDP, _NEWP)
assert 'profile pitch reachable' in HELP



def emit(root, hdr, ok, refrow, table_path):
    sp = SPEC[root]; cols, EA, EB, L, hexb, rB, body, _ = refrow; PN = cols['$PRP@PartNo']
    # ---- vertex chain: End A tip at x=0, End B tip at x=L
    swA = EA['kind'] == 'JICSW'
    if swA:
        V = [(x, r) for (x, r) in EA['VG'][::-1]]   # apex A (on the axis) -> seat -> nose -> slot -> relief -> thread -> countersink edge (0, rcs)
        faceA = len(V) - 1                            # segment (0, rcs) -> (0, Rn) = the End A NUT FACE
        V += [(x, r) for (x, r) in EA['VO']]          # (0, Rn) -> nut hex zone -> skirt -> nut rear -> neck -> (BODYS, NECKR)
        xa = EA['endlen']; V += [(xa, rB)]
    else:
        faceA = EA.get('faceseg', 0)     # 2026-10-02 (0306 locknut): segment 2 - segments 0 / 1 are the construction core and the End A countersink
        V = [(0.0, 0.0)]
        V += EA['V'] if EA['V'] else []
        xa = EA['endlen']
        if not EA.get('cap'): V += [(xa, rB)]      # 2026-10-02 (PLUGS): a capped NPTF crest cone already ends on the body line
    xb = L - EB['endlen']; V += [(xb, rB)]
    bodyseg = len(V) - 2          # segment index of the body top line (V[k]->V[k+1])
    if EB.get('cav') and EB['kind'] in ('JICSW', 'NPSMSW'):
        kb = len(V) - 1                          # index of (xb, rB); segment kb = body face
        V += [(L - x, r) for (x, r) in EB['VO'][::-1]]   # body face bottom -> neck -> nut rear -> skirt -> nut hex -> (L, Rn)
        faceB = len(V) - 1                       # segment (L, Rn) -> countersink outer edge = the NUT FACE
        V += [(L - x, r) for (x, r) in EB['VG']]  # countersink -> thread minor -> relief -> slot -> nose -> seat -> apex
    elif EB.get('cav'):
        faceB = len(V) - 1                       # segment (L, rB) -> port face inner edge
        V += [(L - x, r) for (x, r) in EB['VG']]  # face -> port cavity -> apex on the axis
    else:
        VB = [(L - x, r) for (x, r) in EB['V']][::-1]
        V += VB; V += [(L, 0.0)]
    n = len(V)
    # segment index helpers: module A seg k (as defined in end_*) == global seg k ; module B seg k == global (n-2) - k
    def gA(k): return k
    def gB(k): return (n - 2) - k
    axis = n - 1
    D = []; REL = []
    def dl(seg, nm, val, tx, ty): D.append(f'    Call Dim_len({seg}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def dr(seg, nm, val, tx, ty): D.append(f'    Call Dim_rad({seg}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def da(seg, seg2, nm, deg, tx, ty): D.append(f'    Call Dim_ang({seg}, {seg2}, "{nm}", {math.radians(deg):.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def dp(segPt, useEnd, segLine, nm, val, tx, ty): D.append(f'    Call Dim_ptline({segPt}, {useEnd}, {segLine}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
    def mid(k): return (V[k][0] + V[k + 1][0]) / 2
    Lname = sp['L'].split('@')[0]
    if EB.get('cav'):
        D.append(f'    Call Dim_pair({faceA}, {faceB}, "{Lname}", {L*IN:.9f}, {L/2*IN:.6f}, {(max(rB, EB.get("Rn", 0), EA.get("Rn", 0))+0.9)*IN:.6f})')
    else:
        dl(-1, Lname, L, L / 2, rB + 0.6)
    dr(bodyseg, 'BODYR', rB, mid(bodyseg), -0.45)
    seen_angle = False; seen_seat = False; seen_fsch = False
    for E, g, sfx, side in ((EA, gA, 'A', +1), (EB, gB, 'B', -1)):
        s = E['seg']; k = E['kind']
        if k == 'JICM':
            e = E['e']
            dr(g(s['thd']), f'THDMAJR_{sfx}', e['TM'] / 2, mid(g(s['thd'])), -0.3)
            dl(g(s['relief']), f'JIC{sfx}_RELIEFL', e['RL'], mid(g(s['relief'])), rB + 0.25)
            da(g(s['ramp']), g(s['thd']), 'RELIEFANG' if not seen_angle else f'RELIEFANG_{sfx}_plain', 60, V[g(s['ramp'])][0] + 0.1 * side, rB + 0.1); seen_angle = True
            dl(g(s['thd']), f'JIC{sfx}_THDZ', e['TZ'], mid(g(s['thd'])), rB + 0.35)
            dr(g(s['land']), f'JIC{sfx}_CONER', e['CD'] / 2, mid(g(s['land'])), -0.2)
            dl(g(s['land']), f'JIC{sfx}_LANDL', e['LL'], mid(g(s['land'])), rB + 0.15)
            # seat axial length: the seat line's tip-side point to the end face line
            if side > 0: dp(g(s['seat']), 'True', g(s['face']), f'JIC{sfx}_SEATL', e['SL'], mid(g(s['seat'])), rB + 0.45)
            else: dp(g(s['seat']), 'False', g(s['face']), f'JIC{sfx}_SEATL', e['SL'], mid(g(s['seat'])), rB + 0.45)
            da(g(s['seat']), axis, 'SEATB' if not seen_seat else f'SEATB_{sfx}_plain', 37, V[g(s['seat'])][0] + 0.05 * side, -0.15); seen_seat = True
            REL.append(f'    Call Collinear({g(s["relief"])}, {g(s["land"])})')
        elif k == 'NPTFM':
            dl(g(s['face']), f'NPTF{sfx}_MAJR', E['rS'], V[g(s['face'])][0] - 0.15 * side, E['rS'] / 2)
            if E.get('cap'): pass      # 2026-10-02 (PLUGS): capped cone - its length is driven (MAJR, TAPER and BODYR fix where it meets the blank)
            elif side > 0: dp(g(s['cone']), 'True', g(s['face']), f'NPTF{sfx}_THDL', E['cols'][f'NPTF{sfx}_THDL@DRIVE'], mid(g(s['cone'])), rB + 0.25)
            else: dp(g(s['cone']), 'False', g(s['face']), f'NPTF{sfx}_THDL', E['cols'][f'NPTF{sfx}_THDL@DRIVE'], mid(g(s['cone'])), rB + 0.25)
            da(g(s['cone']), axis, f'NPTF{sfx}_TAPER', 1.7899, mid(g(s['cone'])), E['rS'] * 0.5)
            if 'rel' in s: dl(g(s['rel']), f'NPTF{sfx}_RELL', E['cols'][f'NPTF{sfx}_RELL@DRIVE'], mid(g(s['rel'])), rB + 0.15)
        elif k == 'HOSEB':
            dr(g(s['s1']), f'HOSE{sfx}_STUBR', E['rS'], mid(g(s['s1'])), -0.25)
            dl(g(s['s1']), f'HOSE{sfx}_BEADPOS', E['p1'], mid(g(s['s1'])), rB + 0.25)
            dr(g(s['top']), f'HOSE{sfx}_BEADR', E['rA'], mid(g(s['top'])), -0.35)
            dl(g(s['top']), f'HOSE{sfx}_BEADW', E['w'], mid(g(s['top'])), rB + 0.35)
            dl(g(s['tail']), f'HOSE{sfx}_TAILL', E['endlen'] - E['p2'], mid(g(s['tail'])), rB + 0.15)
            REL.append(f'    Call Collinear({g(s["s1"])}, {g(s["tail"])})')
        elif k in ('FLG61', 'FLG62'):
            m = E['m']
            dr(g(s['head']), f'FLG{sfx}_HEADR', E['rO'], mid(g(s['head'])), -0.35)
            dl(g(s['head']), f'FLG{sfx}_HEADT', m['TH'], mid(g(s['head'])), E['rO'] + 0.3)
            dr(g(s['gin']), f'FLG{sfx}_GRVIR', m['GI'], mid(g(s['gin'])), -0.15)
            dl(g(s['gin']), f'FLG{sfx}_GRVD', m['GD'], mid(g(s['gin'])), E['rO'] + 0.45)
            dr(g(s['gout']), f'FLG{sfx}_GRVOR', m['GO'], mid(g(s['gout'])), -0.25)
            REL.append(f'    Call Collinear({g(s["face2"])}, {g(s["face"])})')
            if E.get('neck'):
                # 2026-10-18 (FLANGE62 neck, also the 1700RC code 61 head): neck radius and length, and the 30deg chamfer from the neck up to the round collar
                nk = E['neck']
                dr(g(s['neck']), f'FLG{sfx}_NECKR', nk['rN'], mid(g(s['neck'])), -0.55)
                dl(g(s['neck']), f'FLG{sfx}_NECKL', nk['NL'], mid(g(s['neck'])), E['rO'] + 0.6)
                da(g(s['cham']), g(s['neck']), f'FLG{sfx}_CHAMANG', FLG_NECK_CHAMANG, mid(g(s['cham'])), nk['rB'] + 0.12)
        elif k == 'NUTCSA':
            # 2026-10-02 (0306 locknut End A): core apex at the origin -> countersink bottom (cs, rmin) -> 45deg countersink -> face (0, rcs).
            # The origin also lies on the End A face line (segment 2), which puts that face at x = 0 (the core apex alone would not).
            dp(g(s['core']), 'True', axis, f'NUTCS{sfx}_MINR', E['rmin'], E['cs'] + 0.05, E['rmin'] * 0.5)
            da(g(s['csk']), axis, f'NUTCS{sfx}_CSANG', 45, E['cs'] / 2, E['rcs'] + 0.1)
            dp(g(s['csk']), 'True', axis, f'NUTCS{sfx}_CSR', E['rcs'], -0.1, E['rcs'] / 2)
            REL.append(f'''    ' ORIGIN-ON-LINE seg({g(s['face'])}) (0306 locknut: the End A face line passes through the origin)
    swModel.ClearSelection2 True
    seg({g(s['face'])}).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True''')
        elif k == 'SQHEAD':      # 2026-10-02 (PLUGS): square head revolved at its corner radius, cut to the square by ZoneSquareCut
            dr(g(s['top']), f'SQ{sfx}_HEADR', E['rH'], mid(g(s['top'])), -0.3)
            dl(g(s['top']), f'SQ{sfx}_HEADL', E['H'], mid(g(s['top'])), rB + 0.25)
        elif k == 'FSM':
            # 2026-10-20 (ORFS): face (axis -> GI) | groove inner wall | groove bottom | groove outer wall | land (-> FR) | 45deg chamfer |
            # thread major | 60deg flank | relief | (shoulder up to the body, added by the chain). 10 dimensions + the land collinear with the face.
            m = E['m']; ue = 'True' if side > 0 else 'False'
            dr(g(s['gin']), f'FSM{sfx}_GRVIR', m['GI'], mid(g(s['gin'])), -0.15)
            dl(g(s['gin']), f'FSM{sfx}_GRVD', m['GD'], mid(g(s['gin'])), rB + 0.45)
            dr(g(s['gout']), f'FSM{sfx}_GRVOR', m['GO'], mid(g(s['gout'])), -0.25)
            dp(g(s['land']), ue, axis, f'FSM{sfx}_FACER', m['FR'], V[g(s['land'])][0] - 0.12 * side, m['FR'] * 0.8)
            da(g(s['cham']), axis, 'FSMCHANG' if not seen_fsch else f'FSMCHANG_{sfx}_plain', FSM_CHANG, mid(g(s['cham'])), E['rM'] + 0.1); seen_fsch = True
            dr(g(s['thd']), f'THDMAJR_{sfx}', E['rM'], mid(g(s['thd'])), -0.3)
            dl(g(s['thd']), f'FSM{sfx}_THDL', E['cols'][f'FSM{sfx}_THDL@DRIVE'], mid(g(s['thd'])), rB + 0.35)
            da(g(s['flank']), g(s['thd']), 'RELIEFANG' if not seen_angle else f'RELIEFANG_{sfx}_plain', FSM_FLANKANG, V[g(s['flank'])][0] + 0.1 * side, rB + 0.1); seen_angle = True
            dr(g(s['rel']), f'FSM{sfx}_RELR', m['RELR'], mid(g(s['rel'])), -0.2)
            dl(g(s['rel']), f'FSM{sfx}_RELL', E['rell'], mid(g(s['rel'])), rB + 0.15)
            REL.append(f'    Call Collinear({g(s["land"])}, {g(s["face"])})')
        elif k == 'BRAZE' and E.get('fsslv'):
            # 2026-10-20 (ORFS staging, FS0319 sleeve End A): tube-side face (origin -> FACER) | 15deg taper | spigot | step up to the collar (chain)
            dp(g(s['face']), 'True', axis, f'FSSLV{sfx}_FACER', E['m']['RT'], -0.1, E['m']['RT'] / 2)
            da(g(s['taper']), axis, f'FSSLV{sfx}_TAPANG', E['m']['TAPANG'], mid(g(s['taper'])), E['m']['RS'] + 0.1)
            dr(g(s['spigot']), f'FSSLV{sfx}_SPIGOTR', E['m']['RS'], mid(g(s['spigot'])), -0.2)
            dp(g(s['spigot']), 'True', g(s['face']), f'FSSLV{sfx}_SPIGOTL', E['xS'], mid(g(s['spigot'])), rB + 0.3)
        elif k == 'ORBM':
            o = E['o']
            dr(g(s['thd']), f'THDMAJR_{sfx}', o['TM'] / 2, mid(g(s['thd'])), -0.3)
            dl(g(s['thd']), f'ORB{sfx}_THDL', o['THDL'], mid(g(s['thd'])), rB + 0.25)
            dr(g(s['grv']), f'ORB{sfx}_GRVR', o['GD'] / 2, mid(g(s['grv'])), -0.2)
            dl(g(s['grv']), f'ORB{sfx}_GRVW', o['GW'], mid(g(s['grv'])), rB + 0.15)
    if swA:
        E = EA; m = E['m']; kfa = faceA
        o = 1 if 'seat_end' in E else 0    # 2026-10-01 (6565-CAVITY): segment 0 = radial line at the seat end (bore radius), the seat cone is segment 1
        def dpairA(i, nm, val, tx, ty): D.append(f'    Call Dim_pair({i}, {kfa}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        topA = max(rB, E['Rn'])
        if o: dp(0, 'True', axis, 'SWA_SEATENDR', E['seat_endr'], E['seat_end'] + 0.08, E['seat_endr'] * 0.6)
        da(o + 0, axis, 'SWA_SEATANG', SW_SEATANG, E['s_nt'] + 0.1, m['SEATR'] * 0.3)
        dp(o + 0, 'True', axis, 'SWA_SEATR', m['SEATR'], E['s_nt'] + 0.05, m['SEATR'] / 2)
        dpairA(o + 1, 'SWA_NOSETIP', E['s_nt'], E['s_nt'] / 2, topA + 0.75)
        dr(o + 2, 'SWA_NOSER', m['NOSER'], (E['s_nt'] + m['FLOOR']) / 2, -0.9)
        dpairA(o + 3, 'SWA_FLOOR', m['FLOOR'], m['FLOOR'] / 2, topA + 0.65)
        dr(o + 4, 'SWA_RELR', m['RELR'], (m['FLOOR'] + E['scb0']) / 2, -0.75)
        da(o + 5, axis, 'SWA_RELANG', SW_RELANG, (m['TE'] + E['scb0']) / 2, E['rmin'] + 0.05)
        dr(o + 6, 'SWA_MINR', E['rmin'], (E['cs'] + m['TE']) / 2, -0.6)
        dl(o + 6, 'SWA_THDL', m['TE'] - E['cs'], (E['cs'] + m['TE']) / 2, topA + 0.1)
        da(o + 7, axis, 'SWA_CSANG', SW_CSANG, E['cs'] / 2, E['rcs'] + 0.08)
        dp(o + 7, 'True', axis, 'SWA_CSR', E['rcs'], -0.1, E['rcs'] / 2)
        dr(o + 9, 'SWA_NUTR', E['Rn'], m['HEXL'] / 2, -0.45)
        dl(o + 9, 'SWA_NUTHEXL', m['HEXL'], m['HEXL'] / 2, topA + 0.3)
        dp(o + 11, 'False', axis, 'SWA_SKIRTFR', m['SKF'], m['HEXL'] + 0.05, m['SKF'] / 2)
        dr(o + 12, 'SWA_SKIRTR', m['SKR'], (m['SKS'] + m['NUTL']) / 2, -0.3)
        dl(o + 12, 'SWA_SKIRTL', m['NUTL'] - m['SKS'], (m['SKS'] + m['NUTL']) / 2, topA + 0.2)
        dpairA(o + 13, 'SWA_NUTL', m['NUTL'], m['NUTL'] / 2, topA + 0.45)
        dr(o + 14, 'SWA_NECKR', m['NECKR'], (m['NUTL'] + m['BODYS']) / 2, -0.15)
        dpairA(o + 15, 'SWA_BODYS', m['BODYS'], m['BODYS'] / 2, topA + 0.55)
        assert faceA == 8 + o and bodyseg == 16 + o, (faceA, bodyseg)
    if EB.get('cav') and EB['kind'] == 'NPSMSW':
        E = EB; sfx = 'B'; m = E['m']; kf = faceB
        def dpairN(i, nm, val, tx, ty): D.append(f'    Call Dim_pair({i}, {kf}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        top = max(rB, E['Rn'])
        dpairN(kb, f'NP{sfx}_BODYS', E['endlen'], L - E['endlen'] / 2, top + 0.55)
        dr(kb + 1, f'NP{sfx}_NECKR', m['NECKR'], mid(kb + 1), -0.15)
        dpairN(kb + 2, f'NP{sfx}_NUTL', m['NUTL'], L - m['NUTL'] / 2, top + 0.45)
        dr(kb + 3, f'NP{sfx}_LIPR', m['SKR'], mid(kb + 3), -0.3)
        dl(kb + 3, f'NP{sfx}_LIPL', m['NUTL'] - m['SKS'], mid(kb + 3), top + 0.2)
        dp(kb + 5, 'False', axis, f'NP{sfx}_SKIRTFR', m['SKF'], L - m['HEXL'] - 0.05, m['SKF'] / 2)
        dl(kb + 6, f'NP{sfx}_NUTHEXL', m['HEXL'], mid(kb + 6), top + 0.3)
        dr(kb + 6, f'NP{sfx}_NUTR', E['Rn'], mid(kb + 6), -0.45)
        dp(kb + 8, 'False', axis, f'NP{sfx}_CSR', m['CSR'], L + 0.1, m['CSR'] / 2)
        da(kb + 8, axis, f'NP{sfx}_CSANG', NPSM_CSANG, L - E['cs'] / 2, m['CSR'] + 0.08)
        dr(kb + 9, f'NP{sfx}_MINR', m['MINR'], mid(kb + 9), -0.6)
        dl(kb + 9, f'NP{sfx}_THDL', m['TE'] - E['cs'], mid(kb + 9), top + 0.1)
        da(kb + 10, axis, f'NP{sfx}_RELANG', NPSM_RELANG, L - (m['TE'] + m['RB0']) / 2, m['MINR'] + 0.05)
        dp(kb + 11, 'False', axis, f'NP{sfx}_RELR', m['RELR'], L - m['RB0'] + 0.03, m['RELR'] / 2)
        dr(kb + 12, f'NP{sfx}_CBR', m['CBR'], mid(kb + 12), -0.75)
        dpairN(kb + 13, f'NP{sfx}_CBEND', m['CBEND'], L - m['CBEND'] / 2, top + 0.65)
        dr(kb + 14, f'NP{sfx}_STEMR', m['STEMR'], mid(kb + 14), -0.9)
        da(kb + 15, axis, f'NP{sfx}_CONEANG', NPSM_CONEANG, L - E['s_tip'] - 0.08, m['TIPR'] * 0.3)
        dp(kb + 16, 'False', axis, f'NP{sfx}_TIPR', m['TIPR'], L - E['s_tip'] - 0.05, m['TIPR'] / 2)
        dpairN(kb + 16, f'NP{sfx}_STEMTIP', E['s_tip'], L - E['s_tip'] / 2, top + 0.75)
    elif EB.get('cav') and EB['kind'] == 'JICSW':
        E = EB; sfx = 'B'; m = E['m']; kf = faceB
        def dpair(i, nm, val, tx, ty): D.append(f'    Call Dim_pair({i}, {kf}, "{nm}", {val*IN:.9f}, {tx*IN:.6f}, {ty*IN:.6f})')
        top = max(rB, E['Rn'])
        dpair(kb, f'SW{sfx}_BODYS', m['BODYS'], L - m['BODYS'] / 2, top + 0.55)
        dr(kb + 1, f'SW{sfx}_NECKR', m['NECKR'], mid(kb + 1), -0.15)
        dpair(kb + 2, f'SW{sfx}_NUTL', m['NUTL'], L - m['NUTL'] / 2, top + 0.45)
        dr(kb + 3, f'SW{sfx}_SKIRTR', m['SKR'], mid(kb + 3), -0.3)
        dl(kb + 3, f'SW{sfx}_SKIRTL', m['NUTL'] - m['SKS'], mid(kb + 3), top + 0.2)
        dp(kb + 5, 'False', axis, f'SW{sfx}_SKIRTFR', m['SKF'], L - m['HEXL'] - 0.05, m['SKF'] / 2)
        dl(kb + 6, f'SW{sfx}_NUTHEXL', m['HEXL'], mid(kb + 6), top + 0.3)
        dr(kb + 6, f'SW{sfx}_NUTR', E['Rn'], mid(kb + 6), -0.45)
        dp(kb + 8, 'False', axis, f'SW{sfx}_CSR', E['rcs'], L + 0.1, E['rcs'] / 2)
        da(kb + 8, axis, f'SW{sfx}_CSANG', SW_CSANG, L - E['cs'] / 2, E['rcs'] + 0.08)
        dr(kb + 9, f'SW{sfx}_MINR', E['rmin'], mid(kb + 9), -0.6)
        dl(kb + 9, f'SW{sfx}_THDL', m['TE'] - E['cs'], mid(kb + 9), top + 0.1)
        da(kb + 10, axis, f'SW{sfx}_RELANG', SW_RELANG, L - (m['TE'] + E['scb0']) / 2, E['rmin'] + 0.05)
        dr(kb + 11, f'SW{sfx}_RELR', m['RELR'], mid(kb + 11), -0.75)
        dpair(kb + 12, f'SW{sfx}_FLOOR', m['FLOOR'], L - m['FLOOR'] / 2, top + 0.65)
        dr(kb + 13, f'SW{sfx}_NOSER', m['NOSER'], mid(kb + 13), -0.9)
        dpair(kb + 14, f'SW{sfx}_NOSETIP', E['s_nt'], L - E['s_nt'] / 2, top + 0.75)
        dp(kb + 15, 'False', axis, f'SW{sfx}_SEATR', m['SEATR'], L - E['s_nt'] - 0.05, m['SEATR'] / 2)
        da(kb + 15, axis, f'SW{sfx}_SEATANG', SW_SEATANG, L - E['s_nt'] - 0.1, m['SEATR'] * 0.3)
        if 'seat_end' in E:   # 2026-10-01 (6565-CAVITY): the seat cone ends at the bore radius, segment kb+16 = radial line down to the axis
            dp(kb + 16, 'False', axis, f'SW{sfx}_SEATENDR', E['seat_endr'], L - E['seat_end'] - 0.08, E['seat_endr'] * 0.6)
            assert kb + 17 == axis, (kb, axis)
    elif EB.get('cav'):
        k = faceB; E = EB; sfx = 'B'
        if E['kind'] == 'ORBF':
            m = E['m']
            dp(k + 1, 'False', axis, f'ORBF{sfx}_FACER', m['RF'], L + 0.1, m['RF'] / 2)
            da(k + 1, axis, f'ORBF{sfx}_CHAMANG', m['CHANG'], L - E['c1'] / 2, m['RF'] + 0.1)
            dp(k + 2, 'False', axis, f'ORBF{sfx}_CHAMR', m['RC'], L - E['c1'], m['RC'] / 2)
            da(k + 2, axis, f'ORBF{sfx}_LEADANG', 45, L - (E['c1'] + E['c2']) / 2, m['RC'] + 0.1)
            dr(k + 3, f'ORBF{sfx}_MINR', E['rmin'], L - (E['c2'] + m['P']) / 2, -0.25)
            dl(k + 3, f'ORBF{sfx}_MINL', m['P'] - E['c2'], L - (E['c2'] + m['P']) / 2, rB + 0.3)
            # 2026-10-01: the drill angle is a table column (60 = 120deg drill point, 90 = deep bore, no point). The reference configuration
            # must have the point: a 90deg line would be drawn vertical and get an automatic Vertical relation on top of this angle.
            assert not E['deep'], f'reference configuration {PN} has a deep-bore ORB port (flat bottom) - choose a reference with a drill point'
            da(k + 4, axis, f'ORBF{sfx}_DRILLANG', E['drill'], L - m['P'] - 0.05, E['rmin'] * 0.4)
        elif E['kind'] == 'JICCAP':
            # 2026-10-02 (0304 cap): face -> thread minor (k+1) -> 37deg seat (k+2) -> pocket (k+3) -> flat pocket bottom (k+4, vertical) -> axis
            m = E['m']
            dr(k + 1, f'JCAP{sfx}_MINR', E['rmin'], L - m['P'] / 2, -0.25)
            dl(k + 1, f'JCAP{sfx}_MINL', m['P'], L - m['P'] / 2, rB + 0.3)
            da(k + 2, axis, f'JCAP{sfx}_SEATANG', 37, L - m['P'] - 0.05, E['rmin'] * 0.6)
            dr(k + 3, f'JCAP{sfx}_PKR', E['rpk'], L - (E['seat_end'] + E['bottom']) / 2, -0.4)
            dl(k + 3, f'JCAP{sfx}_PKL', CAP_POCKETL, L - (E['seat_end'] + E['bottom']) / 2, rB + 0.45)
            assert k + 5 == axis, (k, axis)
        elif E['kind'] == 'NUTCSB':
            # 2026-10-02 (0306 locknut End B): face -> 45deg countersink (k+1) -> flat core end (k+2, vertical) -> axis
            dp(k + 1, 'False', axis, f'NUTCS{sfx}_CSR', E['rcs'], L + 0.1, E['rcs'] / 2)
            da(k + 1, axis, f'NUTCS{sfx}_CSANG', 45, L - E['cs'] / 2, E['rcs'] + 0.1)
            dp(k + 1, 'True', axis, f'NUTCS{sfx}_MINR', E['rmin'], L - E['cs'] - 0.05, E['rmin'] * 0.5)
            assert k + 3 == axis, (k, axis)
        else:
            m = E['m']
            dp(k + 1, 'False', axis, f'JICF{sfx}_CSR', m['RCS'], L + 0.1, m['RCS'] / 2)
            da(k + 1, axis, f'JICF{sfx}_CSANG', 45, L - E['cs'] / 2, m['RCS'] + 0.1)
            dr(k + 2, f'JICF{sfx}_MINR', E['rmin'], L - (E['cs'] + m['P']) / 2, -0.25)
            dl(k + 2, f'JICF{sfx}_MINL', m['P'] - E['cs'], L - (E['cs'] + m['P']) / 2, rB + 0.3)
            da(k + 3, axis, f'JICF{sfx}_SEATANG', 37, L - m['P'] - 0.05, E['rmin'] * 0.4)
    # ---- features
    F = []
    def facepick(E, side):
        if E['faceR'] is not None: return E['faceR']
        return (E['td'] / 2 + hexb / 2) / 2 * 0.98   # on the flat face, between the pocket rim and the hex
    fA = facepick(EA, 1); fB = facepick(EB, -1)
    mode, cA, cB = sp['bore']
    for E, sfx, fromB, fr in ((EA, 'A', 'False', fA), (EB, 'B', 'True', fB)):
        if E['kind'] in ('NPTFF', 'BRAZE', 'UNFF'):
            nm = 'TAPDRILL' + sfx if E['kind'] in ('NPTFF', 'UNFF') else 'SOCKDIA'
            F.append(f'    Call BoreCut("POCKET_{sfx}", "{nm}", {E["td"]*IN:.9f}, {cols[f"DEPTH@POCKETCUT_{sfx}"]*IN:.9f}, 0#, "POCKETCUT_{sfx}", {fromB}, {fr*IN:.9f})')
    if EB.get('socket'):
        # 2026-10-02 (PLUGS): internal hex socket in the End B (head) face
        so_ = EB['socket']
        F += ['    Dim sockcut As SldWorks.Feature',
              f'    Set sockcut = SocketCut({L*IN:.9f}, {so_["af"]*IN:.9f}, {so_["depth"]*IN:.9f}, "SOCKET", "SOCKAF", "SOCKETCUT")',
              '    Check "SOCKAF@SOCKET reachable", Not swModel.Parameter("SOCKAF@SOCKET") Is Nothing',
              '    Check "DEPTH@SOCKETCUT reachable", Not swModel.Parameter("DEPTH@SOCKETCUT") Is Nothing']
    if mode == 'mid':
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
        F.append(f'    Call BoreCut("BORE_B", "DB", {cols["DB@BORE_B"]*IN:.9f}, {cols["DEPTH@BORECUT_B"]*IN:.9f}, 0#, "BORECUT_B", True, {fB*IN:.9f})')
    elif mode == 'B_blind':
        F.append(f'    Call BoreCut("BORE_B", "DB", {cols["DB@BORE_B"]*IN:.9f}, {cols["DEPTH@BORECUT_B"]*IN:.9f}, 0#, "BORECUT_B", True, {fB*IN:.9f})')
    elif mode == 'A_blind':
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
    elif mode == 'sw1':
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
    elif mode == 'sw2':
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
        F.append(f'    Call BoreCut("BORE_B", "DB", {cols["DB@BORE_B"]*IN:.9f}, {cols["DEPTH@BORECUT_B"]*IN:.9f}, {cols["START@BORECUT_B"]*IN:.9f}, "BORECUT_B", False, {fA*IN:.9f})')
    elif mode == 'nut_thru':     # 2026-10-02 (0306 locknut): the thread-minor bore through the whole nut, removing the DRIVE construction core
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
    elif mode == 'A_to_pocket':
        if EA['kind'] in ('NPTFF', 'BRAZE', 'UNFF'):   # 0403: pocket at End A -> bore from the End B face back to the socket bottom (v1 used a start offset; bore did not reach End B)
            F.append(f'    Call BoreCut("BORE_B", "DB", {cols["DB@BORE_B"]*IN:.9f}, {cols["DEPTH@BORECUT_B"]*IN:.9f}, 0#, "BORECUT_B", True, {fB*IN:.9f})')
        else:
            F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
    # bore-open checks (the 0403 v1 bore stopped short of End B - nothing caught it)
    if mode == 'B_blind':
        OPEN = [f'    Check "plug head closed on the axis at End A (x=0)", AxisCovered(0#)',
                f'    Check "hole open on the axis at End B (x={L:.4f})", Not AxisCovered({L*IN:.9f})',
                f'    Check "hole bottom present at x={L - cols["DEPTH@BORECUT_B"]:.4f}", AxisCovered({(L - cols["DEPTH@BORECUT_B"])*IN:.9f})']
    elif mode == 'A_blind':
        OPEN = [f'    Check "hole open on the axis at the ORB tip (x=0)", Not AxisCovered(0#)',
                f'    Check "hole bottom present at x={cols["DEPTH@BORECUT_A"]:.4f}", AxisCovered({cols["DEPTH@BORECUT_A"]*IN:.9f})',
                f'    Check "plug head closed on the axis at End B (x={L:.4f})", AxisCovered({L*IN:.9f})']
    elif mode == 'pocket_only':
        OPEN = [f'    Check "port open on the axis at End A (x=0)", Not AxisCovered(0#)',
                f'    Check "port bottom present at x={cols["DEPTH@POCKETCUT_A"]:.4f}", AxisCovered({cols["DEPTH@POCKETCUT_A"]*IN:.9f})',
                f'    Check "cap closed on the axis at End B (x={L:.4f})", AxisCovered({L*IN:.9f})']
    elif mode == 'cav_only':     # 2026-10-02 (0304 cap)
        OPEN = [f'    Check "cap crown closed on the axis at End A (x=0)", AxisCovered(0#)',
                f'    Check "cap cavity open on the axis at End B (x={L:.4f})", Not AxisCovered({L*IN:.9f})',
                f'    Check "cap pocket bottom present at x={L - EB["bottom"]:.4f} (crown {L - EB["bottom"]:.4f})", AxisCovered({(L - EB["bottom"])*IN:.9f})']
    elif mode == 'nut_thru':     # 2026-10-02 (0306 locknut): the bore must have removed the whole construction core
        OPEN = [f'    Check "locknut bore open on the axis at End A (x=0)", Not AxisCovered(0#)',
                f'    Check "locknut bore open on the axis at End B (x={L:.4f})", Not AxisCovered({L*IN:.9f})',
                f'    Check "construction core end removed (no face across the axis at x={L - EB["cs"]:.4f})", Not AxisCovered({(L - EB["cs"])*IN:.9f})']
    elif mode == 'socket':
        dso_ = EB['socket']['depth']
        OPEN = [f'    Check "socket plug: End A (thread tip) closed on the axis (x=0)", AxisCovered(0#)',
                f'    Check "socket open on the axis at the head face (x={L:.4f})", Not AxisCovered({L*IN:.9f})',
                f'    Check "socket bottom present at x={L - dso_:.4f}", AxisCovered({(L - dso_)*IN:.9f})']
    elif mode == 'none':
        OPEN = [f'    Check "solid plug: End A face closed on the axis (x=0)", AxisCovered(0#)',
                f'    Check "solid plug: End B face closed on the axis (x={L:.4f})", AxisCovered({L*IN:.9f})']
    else:
        OPEN = [f'    Check "bore open on the axis at End A (x=0)", Not AxisCovered(0#)',
                f'    Check "bore open on the axis at End B (x={L:.4f})", Not AxisCovered({L*IN:.9f})']
    if mode in ('sw1', 'sw2') and EA['kind'] == 'JICSW':
        OPEN.append(f'    Check "bore reaches the End A swivel seat (no bore bottom at the nose-tip plane x={EA["s_nt"]:.4f})", Not AxisCovered({EA["s_nt"]*IN:.9f})')
    if mode in ('sw1', 'sw2'):
        xs_ = L - EB['open_at']
        OPEN.append(f'    Check "bore reaches the swivel {"seat (no bore bottom at the nose-tip plane" if EB["kind"] == "JICSW" else "stem tip (no face across the axis at the stem-tip plane"} x={xs_:.4f})", Not AxisCovered({xs_*IN:.9f})')
        if mode == 'sw2':
            OPEN.append(f'    Check "bore step open (no face across the axis at x={cols["START@BORECUT_B"]:.4f})", Not AxisCovered({cols["START@BORECUT_B"]*IN:.9f})')
        if 'seat_end' in EA:   # 2026-10-01 (6565-CAVITY): the bore cuts must remove the core disc closing each trimmed seat cone
            OPEN.append(f'    Check "bore open through the End A seat end (no face across the axis at x={EA["seat_end"]:.4f})", Not AxisCovered({EA["seat_end"]*IN:.9f})')
            OPEN.append(f'    Check "bore open through the End B seat end (no face across the axis at x={L - EB["seat_end"]:.4f})", Not AxisCovered({(L - EB["seat_end"])*IN:.9f})')
    for E, sfx in ((EA, 'A'), (EB, 'B')):
        if E['kind'] in ('NPTFF', 'BRAZE', 'UNFF') and mode not in ('meet', 'pocket_only'):
            xb = cols[f'DEPTH@POCKETCUT_{sfx}'] if sfx == 'A' else L - cols[f'DEPTH@POCKETCUT_{sfx}']
            OPEN.append(f'    Check "bore open through the End {sfx} pocket bottom (x={xb:.4f})", Not AxisCovered({xb*IN:.9f})')
    # threads
    T = []
    for E, sfx, tip, side in ((EA, 'A', 0.0, +1), (EB, 'B', L, -1)):
        t = E['thread']
        if not t: continue
        if t['type'] == 'CUT':
            ex = tip + side * t['ex']
            if E['kind'] == 'ORBM':
                d = dashes(PN)[0 if sfx == 'A' else 1]; size = f"{E['o']['TM']:.4f}-{tpi_of(ORB_THR[d]):g}"; pitch = 1 / tpi_of(ORB_THR[d])
            else: size, pitch = t['size'], t['pitch']
            T.append(f'    Call ThreadCut({ex*IN:.9f}, {t["er"]*IN:.9f}, {t["depth"]*IN:.9f}, "{size}", "THD_End{sfx}", {-side}#, {pitch*IN:.9f})')
        else:
            T.append(f'    Call HelixThread({tip*IN:.9f}, {t["r"]*IN:.9f}, {t["height"]*IN:.9f}, {t["pitch"]*IN:.9f}, {t["thdh"]*IN:.9f}, {t["taper"]:.9f}, {str(t["taperOut"])}, {str(t["apexOut"])}, "{sfx}", "THD_End{sfx}")')
    # ---- config spot check: smallest and largest config, key params
    params = [c for c in hdr if '@' in c and not c.startswith('$') and c.split('@')[1] in ('DRIVE', 'HEX')][:8] + [c for c in hdr if c.startswith(('THDPITCH@', 'Profile_Height@', 'PROF_R@', 'DEPTH@BORECUT', 'DEPTH@POCKETCUT', 'SWA_SEATENDR@', 'SWB_SEATENDR@', 'SOCKAF@', 'DEPTH@SOCKETCUT', 'SQAF@', 'DEPTH@SQCUT'))]
    if sp.get('flats'):     # 2026-10-18 (FLANGE62 review): the wrench flats cut and the flange neck are table-driven too - spot-check them
        params += [c for c in hdr if c.startswith(('WAF@FLATS', 'FLATW@FLATS', 'START@FLATCUT', 'DEPTH@FLATCUT', 'FLGB_NECKR@', 'FLGB_NECKL@')) and c not in params]
    names = [b[0]['$PRP@PartNo'] for b in ok]
    chk_rows = [ok[1], ok[-1]] if len(ok) > 2 else [ok[-1]]
    params = [p for p in params if all(b[0][p] is not None for b in chk_rows)]
    cfgs = [(b[0]['$PRP@PartNo'], [b[0][p] for p in params]) for b in chk_rows]
    blk = sp3.check_block(cfgs, params)
    holechk = ''
    if sp['bore'][0] == 'A_blind':
        # 2026-09-25 (6408 cored plug): the hollow / solid switch is a $STATE column - check that it and the hole depth land per configuration
        hol_ = [b for b in ok if b[0].get('$STATE@BORECUT_A') == 'U' and b[0]['$PRP@PartNo'] != PN]
        sol_ = [b for b in ok if b[0].get('$STATE@BORECUT_A') == 'S']
        hl_ = ["    ' ---- hollow / solid switch ($STATE@BORECUT_A column) and the hole depth, per configuration (2026-09-25)", '    stepName = "Hollow/solid check"']
        if hol_:
            c_ = max(hol_, key=lambda b: b[0]['DA@BORE_A'])[0]; nm_ = c_['$PRP@PartNo']
            hl_ += [f'    swModel.ShowConfiguration2 "{nm_}"', '    swModel.ForceRebuild3 False',
                    f'    Check "{nm_}: hole open on the axis at the ORB tip (x=0)", Not AxisCovered(0#)',
                    f'    Check "{nm_}: hole bottom at x={c_["DEPTH@BORECUT_A"]:.4f} (hole {c_["DA@BORE_A"]})", AxisCovered({c_["DEPTH@BORECUT_A"]*IN:.9f})',
                    f'    Check "{nm_}: plug head closed on the axis (x={c_[sp["L"]]:.4f})", AxisCovered({c_[sp["L"]]*IN:.9f})']
        if sol_:
            nm_ = sol_[0][0]['$PRP@PartNo']
            hl_ += [f'    swModel.ShowConfiguration2 "{nm_}"', '    swModel.ForceRebuild3 False',
                    f'    Check "{nm_}: solid plug - ORB tip closed on the axis (hole feature suppressed)", AxisCovered(0#)']
        holechk = '\n'.join(hl_) + '\n'
    if EB.get('socket'):
        # 2026-10-02 (PLUGS): in EVERY configuration the socket must be open at the head face, end in its flat bottom at L - depth, and leave
        # the thread tip closed (the socket depth / A/F are table columns; a cut that went the wrong way would still give one body)
        sk_ = ["    ' ---- hex socket in every configuration (2026-10-02, PLUGS): open at the head face, flat bottom at L - depth, thread tip closed",
               '    stepName = "Socket check"']
        for b_ in ok:
            nm_ = b_[0]['$PRP@PartNo']; L_ = b_[3]; so_ = b_[2]['socket']
            sk_ += [f'    swModel.ShowConfiguration2 "{nm_}"', '    swModel.ForceRebuild3 False',
                    f'    Check "{nm_}: socket open on the axis at the head face (x={L_:.4f})", Not AxisCovered({L_*IN:.9f})',
                    f'    Check "{nm_}: socket bottom at x={L_ - so_["depth"]:.4f} (depth {so_["depth"]}, A/F {so_["af"]})", AxisCovered({(L_ - so_["depth"])*IN:.9f})',
                    f'    Check "{nm_}: End A tip closed on the axis (x=0)", AxisCovered(0#)']
        holechk += '\n'.join(sk_) + '\n'
    deepchk = ''
    if EB['kind'] == 'ORBF':
        # 2026-10-01 (ORBF-DEEPBORE): ORBFB_DRILLANG is a table column - 60 (120deg drill point) or 90 (through-bore = port minor: flat port bottom,
        # no point). In EVERY configuration check that the column drives the angle and that bore and port meet with no face across the axis at the
        # minor-bore bottom: a drill point flipped toward the port face after a 90 -> 60 change would close the bore there (one body, no rebuild
        # error - the all-config sweep would not see it). One element per statement: no line continuations, short lines.
        nq_ = len(ok)
        dl_ = ["    ' ---- female ORB port bottom, every configuration (2026-10-01): ORBFB_DRILLANG 60 = 120deg drill point, 90 = deep bore (no point)",
               '    stepName = "ORB port bottom check"',
               '    Dim db_p As SldWorks.Dimension, db_i As Long, db_c() As String, db_x() As Double, db_a() As Double, db_v As Double',
               f'    ReDim db_c({nq_ - 1}): ReDim db_x({nq_ - 1}): ReDim db_a({nq_ - 1})']
        for i_, b in enumerate(ok):
            dl_.append(f'    db_c({i_}) = "{b[0]["$PRP@PartNo"]}": db_x({i_}) = {(b[3] - b[2]["m"]["P"]) * IN:.9f}: db_a({i_}) = {b[2]["drill"]:g}')
        dl_ += [f'    For db_i = 0 To {nq_ - 1}',
                '        swModel.ShowConfiguration2 db_c(db_i)',
                '        swModel.ForceRebuild3 False',
                '        Set db_p = swModel.Parameter("ORBFB_DRILLANG@DRIVE")',
                '        If db_p Is Nothing Then',
                '            Check db_c(db_i) & ": ORBFB_DRILLANG@DRIVE readable", False',
                '        Else',
                '            db_v = db_p.SystemValue * 180 / 3.14159265358979',
                '            Check db_c(db_i) & ": ORBFB_DRILLANG@DRIVE = " & Format(db_v, "0.00") & " deg (table " & db_a(db_i) & ")", Abs(db_v - db_a(db_i)) < 0.01',
                '        End If',
                '        Check db_c(db_i) & ": bore meets the port - no face across the axis at the minor-bore bottom x=" & Format(db_x(db_i) / IN_, "0.0000"), Not AxisCovered(db_x(db_i))',
                '    Next db_i']
        deepchk = '\n'.join(dl_) + '\n'
    if 'seat_end' in EA:
        # 2026-10-01 (6565-CAVITY): each seat cone ends at the bore radius and is closed by a core disc there - in EVERY configuration
        # the bore cuts must have removed both discs (no planar face across the axis at either seat-end plane); ~1 s per configuration
        sl_ = ["    ' ---- seat-end planes open on the axis, every configuration (2026-10-01, 6565-CAVITY)", '    stepName = "Seat-end check"']
        for b_ in ok:
            nm_ = b_[0]['$PRP@PartNo']; xa_ = b_[1]['seat_end']; xb_ = b_[3] - b_[2]['seat_end']
            sl_ += [f'    swModel.ShowConfiguration2 "{nm_}"', '    swModel.ForceRebuild3 False',
                    f'    Check "{nm_}: bore open through the End A seat end (x={xa_:.4f}, seat cone ends at r={b_[0]["SWA_SEATENDR@DRIVE"]:.4f})", Not AxisCovered({xa_*IN:.9f})',
                    f'    Check "{nm_}: bore open through the End B seat end (x={xb_:.4f}, seat cone ends at r={b_[0]["SWB_SEATENDR@DRIVE"]:.4f})", Not AxisCovered({xb_*IN:.9f})']
        holechk += '\n'.join(sl_) + '\n'
    blk = blk.replace('Format(cx_prm.SystemValue / IN_, "0.0000")', 'Format(cx_v, "0.0000")').replace('Abs(cx_prm.SystemValue / IN_ - cx_w(cx_q)(cx_k))', 'Abs(cx_v - cx_w(cx_q)(cx_k))')
    blk = blk.replace('            Else\n                Check cx_c(cx_q)', '            Else\n                cx_v = IIf(InStr(cx_p(cx_k), "TAPER") > 0 Or InStr(cx_p(cx_k), "ANG") > 0 Or InStr(cx_p(cx_k), "SEATB") > 0, cx_prm.SystemValue * 180 / 3.14159265358979, cx_prm.SystemValue / IN_)\n                Check cx_c(cx_q)')
    blk = blk.replace('Dim cx_c As Variant,', 'Dim cx_v As Double, cx_c As Variant,')
    assert 'cx_v = IIf' in blk
    # VBA allows at most 24 line continuations in one statement ("v = Array( _" + one per point line): above 24 points
    # two points go on each line (2026-09-25: 6504 had 26 points, 6565 had 34 - neither macro compiled)
    per = 1 if n <= 24 else 2
    pts = ', _\n'.join('    ' + ', '.join(f'{x*IN:.9f}, {r*IN:.9f}' for x, r in V[k:k + per]) for k in range(0, len(V), per))
    _vol = 0.0
    for i in range(n - 1):
        (x1, r1), (x2, r2) = V[i], V[i + 1]; hgt = (x2 - x1) * IN; a_, b_ = r1 * IN, r2 * IN
        _vol += math.pi * hgt * (a_ * a_ + a_ * b_ + b_ * b_) / 3
    _vol = abs(_vol)
    entry = f'Build{root}'
    vba = f'''Attribute VB_Name = "Build_{root}_MASTER"
' ============================================================================
'  Build_{root}_MASTER.bas  -  OMi fitting library, generated {TODAY} by gen_straight2.py
'  {sp['name']} - master from reference configuration {PN} (DesignTable_{root}_SW2.xlsx row 2)
'  Ends: A = {EA['kind']}  B = {EB['kind']}.  Body revolved at BODYR then hex-cut; SP3 radius dims.
'  Run in SolidWorks: Tools > Macro > Run > {entry}.  Report: 03_SCRIPTS\\Build_{root}_report.txt
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
    stepName = "DRIVE sketch"

    ' ================= 1. DRIVE sketch =================
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
    Dim swFeat As SldWorks.Feature
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
    Check "Revolve created", Not rev Is Nothing
    If rev Is Nothing Then GoTo Finish
    rev.Name = "BODY"
    Dim vrev As Double: vrev = Volume()
    Check "Revolved volume " & Format(vrev / IN_ ^ 3, "0.0000") & " in^3 (expect {_vol/IN**3:.4f})", Abs(vrev - {_vol:.12e}) < {_vol:.12e} * 0.002

    stepName = "HEX cut"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    Dim poly As Variant
    poly = swSkMgr.CreatePolygon(0, 0, 0, {hexb/2*IN:.9f}, 0, 0, 6, True)
    Dim circ As SldWorks.SketchSegment, k As Long
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
    Next k
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2({hexb*0.7*IN:.6f}, {hexb*0.7*IN:.6f}, 0)
    If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = {hexb*IN:.9f}
    NameDim dd, "HEXB", {hexb*IN:.9f}
    swModel.ClearSelection2 True
    For k = LBound(poly) To UBound(poly)
        If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL": Exit For
    Next k
    swModel.ClearSelection2 True
    Dim arc As SldWorks.SketchArc
    Set arc = circ
    arc.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0): swFeat.Name = "HEX"
    Check "hex sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Dim hexcut As SldWorks.Feature, v0 As Double, v1 As Double
    v0 = Volume()
    Set hexcut = MakeCut2(swFeat, True, {L*IN*1.5:.6f}, "HEXCUT flip")
    If hexcut Is Nothing Then
        Set hexcut = MakeCut2(swFeat, False, {L*IN*1.5:.6f}, "HEXCUT plain (to flip)")
        If Not hexcut Is Nothing Then
            Dim xd2 As SldWorks.ExtrudeFeatureData2
            Set xd2 = hexcut.GetDefinition
            xd2.AccessSelections swModel, Nothing
            xd2.FlipSideToCut = True
            Check "HEXCUT flipped via definition", hexcut.ModifyDefinition(xd2, swModel, Nothing)
        End If
    End If
    Check "HEXCUT created", Not hexcut Is Nothing
    If Not hexcut Is Nothing Then
        hexcut.Name = "HEXCUT"
        v1 = Volume()
        Check "HEXCUT removed only the corners (" & Format(100 * (v0 - v1) / v0, "0.0") & "% of volume)", (v1 < v0) And (v1 > 0.6 * v0)
    End If

    stepName = "Pockets and bores"
{chr(10).join(F)}
{chr(10).join(OPEN)}
    stepName = "Threads"
    curAxis = 0
{chr(10).join(T)}
    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
    Trace "Bounding box length " & Format(lenX, "0.0000") & " (nominal {L:.4f}; loose around thread faces, informational)"
    Check "End A face present at x=0", SelectEndFace(0#)
    Check "End B face present at x={L:.4f}", SelectEndFace({L*IN:.9f})
    Check "Body within nominal length +0.15 (threads loosen the box)", Abs(lenX - {L}) < 0.15
    Check "Hex across flats " & Format(dY, "0.0000") & " / corners " & Format(dZ, "0.0000") & " (expect {hexb:.4f} / {2*rB:.4f})", (Abs(dY - {hexb}) < 0.01 And Abs(dZ - {2*rB}) < 0.01) Or (Abs(dZ - {hexb}) < 0.01 And Abs(dY - {2*rB}) < 0.01)
    Dim bodies As Variant
    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body", (UBound(bodies) = 0)

    stepName = "Design table"
    swModel.ClearSelection2 True
    Dim ok As Boolean
    ok = swModel.InsertFamilyTableOpen(TABLE_PATH)
    Check "Design table inserted from " & TABLE_PATH, ok
    swModel.CloseFamilyTable
    swModel.ForceRebuild3 False
    Dim cfgs As Variant
    cfgs = swModel.GetConfigurationNames
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect {len(ok)+1})", (UBound(cfgs) + 1) >= {len(ok)}
{blk}{holechk}{deepchk}
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
    swModel.ShowConfiguration2 sw_names(LBound(sw_names) + IIf(sw_names(LBound(sw_names)) = "Default", 1, 0))

    ' ---- resting state (project rule): every THD_* feature suppressed in EVERY configuration before the save.
    '      Threads stay live through the build, table insert, config checks and sweep so they are verified;
    '      OMi_SeriesDrawings / OMi_BatchDrawings unsuppress them for drawing views and put them back.
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
{{THDCHK}}

    stepName = "Save"
    Dim e As Long, w As Long, t0 As Date, fdt As Date
    t0 = Now
    ok = swModel.Extension.SaveAs(SAVE_PATH, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
    Trace "SaveAs " & SAVE_PATH & " returned " & ok & " (error " & e & ", warning " & w & ")"
    If Not ok Then
        ' SolidWorks can return False (error 0) although it wrote the file: trust the file on disk when it is fresh
        On Error Resume Next
        fdt = FileDateTime(SAVE_PATH)
        If Err.Number = 0 Then
            If DateDiff("s", t0, fdt) >= -5 Then ok = True: Trace "  file on disk written " & fdt & " - saved (SaveAs return value ignored)"
        End If
        Err.Clear
        On Error GoTo Trap
    End If
    If Not ok Then
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

' ---------------------------------------------------------------- helpers (shared library, SP3-validated on 2403/2405/2502HX)
{HELP}'''
    if sp.get('swivel') or sp.get('zonehex'):
        i0 = vba.index('    stepName = "HEX cut"'); i1 = vba.index('    stepName = "Pockets and bores"')
        xbody = L - EB['endlen']; xs0 = EA['endlen'] if swA else 0.0
        nutB = EB['kind'] in ('JICSW', 'NPSMSW')
        blkA = ''
        blkB = ''
        if nutB:
            blkB = f'''    ' swivel nut hex: sketched on the nut face (End B), cut back over the nut hex length
    Set nutcut = ZoneHexCut(True, {L*IN:.9f}, {EB['nut_af']*IN:.9f}, 0#, {EB['m']['HEXL']*IN:.9f}, {(L - EB['m']['HEXL']/2)*IN:.9f}, "NUTHEX", "NUTHEX", "NUTCUT")
    Check "NUTHEX@NUTHEX reachable", Not swModel.Parameter("NUTHEX@NUTHEX") Is Nothing
    Check "DEPTH@NUTCUT reachable", Not swModel.Parameter("DEPTH@NUTCUT") Is Nothing
'''
        if swA:
            blkA = f'''    ' End A swivel nut hex: sketched on the Right Plane (= the End A nut face), cut over the nut hex length
    Set nutcutA = ZoneHexCut(False, 0#, {EA['nut_af']*IN:.9f}, 0#, {EA['m']['HEXL']*IN:.9f}, {EA['m']['HEXL']/2*IN:.9f}, "NUTHEXA", "NUTHEXA", "NUTCUTA")
    Check "NUTHEXA@NUTHEXA reachable", Not swModel.Parameter("NUTHEXA@NUTHEXA") Is Nothing
    Check "DEPTH@NUTCUTA reachable", Not swModel.Parameter("DEPTH@NUTCUTA") Is Nothing
    Check "START@HEXCUT reachable", Not swModel.Parameter("START@HEXCUT") Is Nothing
'''
        vba = vba[:i0] + f'''    stepName = "HEX cuts (body hex + swivel nut hex)"
    Dim hexcut As SldWorks.Feature, nutcut As SldWorks.Feature, nutcutA As SldWorks.Feature
    ' body hex: only between {'the two body faces' if swA else 'the End A tip and the body face behind the nut' if nutB else 'the End A tip and the flange head'} - NOT through all
    Set hexcut = ZoneHexCut(False, 0#, {hexb*IN:.9f}, {xs0*IN:.9f}, {(xbody - xs0)*IN:.9f}, {(xs0 + xbody)/2*IN:.9f}, "HEX", "HEXB", "HEXCUT")
{blkB}{blkA}    Check "HEXB@HEX reachable", Not swModel.Parameter("HEXB@HEX") Is Nothing
    Check "DEPTH@HEXCUT reachable", Not swModel.Parameter("DEPTH@HEXCUT") Is Nothing

''' + vba[i1:]
        if swA:
            o0 = '''    Set ln1 = seg(0)
    ln1.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"'''
            assert vba.count(o0) == 1
            vba = vba.replace(o0, f'''    ' End A is a swivel nut face, not a point on the axis: the origin lies on the End A nut face line AND on the axis line
    seg({faceA}).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    seg(NPTS - 1).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"''')
        i0 = vba.index('    Check "Hex across flats'); i1 = vba.index('\n', i0)
        big = max(hexb, EB.get('nut_af', 0), EA.get('nut_af', 0), 2 * EB.get('rO', 0)); bigc = max(2 * rB, 2 * EB.get('Rn', 0), 2 * EA.get('Rn', 0), 2 * EB.get('rO', 0))
        lab_ = f"nut hex {EB['nut_af']:.4f}" if nutB else f"flange head dia {2*EB['rO']:.4f}"
        vba = vba[:i0] + f'    Check "Across flats / corners " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (body hex {hexb:.4f}, {lab_}{"/" + format(EA["nut_af"], ".4f") if swA else ""}: expect between {big:.4f} and {bigc:.4f})", dY > {big - 0.01:.4f} And dZ > {big - 0.01:.4f} And dY < {bigc + 0.01:.4f} And dZ < {bigc + 0.01:.4f}' + vba[i1:]
        vba = vba.replace("Body revolved at BODYR then hex-cut; SP3 radius dims.", "Body revolved at BODYR (body hex) " + ("/ the nut radius (swivel nut hex), each hex cut over its own zone" if nutB else "then hex-cut between the JIC end and the flange head only") + "; SP3 radius dims.")
        assert ('ZoneHexCut(True' in vba) == nutB
        if swA: vba = vba.replace('Ends: A = JICSW  B = JICSW.', 'Ends: A = JICSW  B = JICSW (both ends swivel; the origin sits on the End A nut face' + ('; each seat cone ends at the through-bore' if 'seat_end' in EA else '') + ').')
    if sp.get('round'):
        i0 = vba.index('    stepName = "HEX cut"'); i1 = vba.index('    stepName = "Pockets and bores"')
        vba = vba[:i0] + "    ' (round bar - no hex cut)\n\n" + vba[i1:]
        i0 = vba.index('    Check "Hex across flats'); i1 = vba.index('\n', i0)
        rF_ = max([E_['rO'] for E_ in (EA, EB) if E_['kind'] in ('FLG61', 'FLG62')] + [0.0])
        if rF_ > rB:   # 2026-10-18 (1724 / 1824, FLANGE62 / FLANGE61-PLUG): a flange head wider than the round body sets the box
            vba = vba[:i0] + f'    Check "Outer diameter " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect the flange head {2*rF_:.4f}; round body {2*rB:.4f})", Abs(dY - {2*rF_:.4f}) < 0.01 And Abs(dZ - {2*rF_:.4f}) < 0.01' + vba[i1:]
            vba = vba.replace("Body revolved at BODYR then hex-cut; SP3 radius dims.", "Body revolved at BODYR (round stub, no hex cut) behind the flange head; SP3 radius dims.")
        else:
            vba = vba[:i0] + f'    Check "Body diameter " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect {2*rB:.4f})", Abs(dY - {2*rB:.4f}) < 0.01 And Abs(dZ - {2*rB:.4f}) < 0.01' + vba[i1:]
        assert 'HEXCUT' not in vba.split('Sub Build')[1].split('End Sub')[0]
        k_ = vba.index('    Check "Body within nominal length +0.15 (threads loosen the box)", Abs(lenX - ')     # the box check must follow the intact length check line
        assert vba[vba.index('\n', k_) + 1:].startswith(('    Check "Outer diameter ', '    Check "Body diameter ')), 'round-body box check spliced at stale offsets'
    if sp.get('flats'):
        # 2026-10-18 (FLANGE62 'flats', 1700RC / 1800): two wrench flats on the round collar instead of the hex cut (FlatsCut, appended to the helpers)
        i0 = vba.index('    stepName = "HEX cut"'); i1 = vba.index('    stepName = "Pockets and bores"')
        st_, dp_ = cols['START@FLATCUT'], cols['DEPTH@FLATCUT']
        vba = vba[:i0] + f'''    stepName = "Wrench flats cut"
    Dim hexcut As SldWorks.Feature
    ' two wrench flats (A/F {hexb:.4f}) on the round collar (dia {2*rB:.4f}): outside a centre rectangle on the Right Plane, cut from the
    ' middle of the JIC relief (x={st_:.4f}, relief below the flats - nothing cut there) to the neck start (x={st_ + dp_:.4f}); the neck is not touched
    Set hexcut = FlatsCut({hexb*IN:.9f}, {cols['FLATW@FLATS']*IN:.9f}, {st_*IN:.9f}, {dp_*IN:.9f}, "FLATS", "WAF", "FLATW", "FLATCUT")
    Check "WAF@FLATS reachable", Not swModel.Parameter("WAF@FLATS") Is Nothing
    Check "FLATW@FLATS reachable", Not swModel.Parameter("FLATW@FLATS") Is Nothing
    Check "START@FLATCUT reachable", Not swModel.Parameter("START@FLATCUT") Is Nothing
    Check "DEPTH@FLATCUT reachable", Not swModel.Parameter("DEPTH@FLATCUT") Is Nothing

''' + vba[i1:]
        i0 = vba.index('    Check "Hex across flats'); i1 = vba.index('\n', i0)
        rF_ = max([E_['rO'] for E_ in (EA, EB) if E_['kind'] in ('FLG61', 'FLG62')] + [0.0])
        lo_, hi_ = max(hexb, 2 * rF_), max(2 * rB, 2 * rF_)
        vba = vba[:i0] + f'    Check "Across the flats / across the round " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (flats {hexb:.4f}, collar {2*rB:.4f}, flange head {2*rF_:.4f}: expect {lo_:.4f} and {hi_:.4f})", (Abs(dY - {lo_:.4f}) < 0.01 And Abs(dZ - {hi_:.4f}) < 0.01) Or (Abs(dZ - {lo_:.4f}) < 0.01 And Abs(dY - {hi_:.4f}) < 0.01)' + vba[i1:]
        vba = vba.replace("Body revolved at BODYR then hex-cut; SP3 radius dims.", "Body revolved at BODYR (round collar) then two wrench flats cut on the collar; SP3 radius dims.")
        assert 'HEXCUT' not in vba.split('Sub Build')[1].split('End Sub')[0] and 'FlatsCut(' in vba
        k_ = vba.index('    Check "Body within nominal length +0.15 (threads loosen the box)", Abs(lenX - ')
        assert vba[vba.index('\n', k_) + 1:].startswith('    Check "Across the flats / across the round '), 'flats box check spliced at stale offsets'
    if T:
        vba = vba.replace('{THDCHK}', '    Check "Threads suppressed in all configurations before save (" & st_n & " THD_ features)", st_n > 0 And st_bad = 0')
    else:   # 2026-10-18 (1724 / 1824 plugs): no threaded end - there is no THD_ feature to suppress
        vba = vba.replace('{THDCHK}', '    Check "No threaded end: no THD_ feature to suppress before save (" & st_n & " found)", st_n = 0')
    if sp.get('flats'): vba += FLATSCUT      # 2026-10-18: the wrench-flats cut helper, only in macros that use it
    if EB['kind'] == 'SQHEAD':
        # 2026-10-02 (PLUGS): the square head - the OUTSIDE of a square sketched on the End B face, cut back over the head length only
        i1 = vba.index('    stepName = "Pockets and bores"')
        vba = vba[:i1] + f'''    stepName = "Square head cut"
    Dim sqcut As SldWorks.Feature
    ' square head: sketched on the End B face, the outside of the square cut over the head length only (the round D collar is not touched)
    Set sqcut = ZoneSquareCut(True, {L*IN:.9f}, {EB['af']*IN:.9f}, 0#, {EB['H']*IN:.9f}, {(L - EB['H'] / 2)*IN:.9f}, "SQUARE", "SQAF", "SQCUT")
    Check "SQAF@SQUARE reachable", Not swModel.Parameter("SQAF@SQUARE") Is Nothing
    Check "DEPTH@SQCUT reachable", Not swModel.Parameter("DEPTH@SQCUT") Is Nothing

''' + vba[i1:]
    if EB.get('socket') or EB['kind'] == 'SQHEAD':
        o_ = "Body revolved at BODYR then hex-cut; SP3 radius dims."
        assert vba.count(o_) == 1
        vba = vba.replace(o_, 'Round body revolved at BODYR (no hex)' + ('; square head cut to the square over its length' if EB['kind'] == 'SQHEAD' else '')
                          + ('; internal hex socket cut into the head face' if EB.get('socket') else '') + '; SP3 radius dims.')
        vba += (SOCKETCUT if EB.get('socket') else '') + (ZONESQ if EB['kind'] == 'SQHEAD' else '')
    vba = ref_config_at_save(add_progress(vba))      # 2026-09-24: one report/status-bar line per configuration in the sweep; 2026-09-25: saved in the reference configuration (progress_patch.py)
    p = f'{OUT}/Build_{root}_MASTER.bas'; open(p, 'w').write(vba)
    return p, n, V


if __name__ == '__main__':
    summary = {}
    for root in sys.argv[1:]:
        built, skipped = build_rows(root)
        if not [b for b in built if not b[7]]:
            # 2026-10-02 (PLUGS): no buildable row (every row MISSING / DROP / skipped / blocked) - no macro or SW2 table; the summary says why
            blocked = [b[0]['$PRP@PartNo'] + ': ' + '; '.join(b[7]) for b in built if b[7]]
            summary[root] = dict(configs=0, ref=None, skipped=skipped, blocked=blocked, verts=0, cols=0)
            print(f"{root}: 0 configs - nothing to build ({len(skipped)} skipped (DROP/MISSING/no data), {len(blocked)} geometry-blocked); no macro / table written")
            for b in blocked: print('   BLOCKED', b)
            for s in skipped[:6]: print('   skipped', s)
            continue
        table, hdr, ok, refrow = write_sw2(root, built)
        macro, n, V = emit(root, hdr, ok, refrow, table)
        blocked = [b[0]['$PRP@PartNo'] + ': ' + '; '.join(b[7]) for b in built if b[7]]
        summary[root] = dict(configs=len(ok), ref=refrow[0]['$PRP@PartNo'], skipped=skipped, blocked=blocked, verts=n, cols=len(hdr))
        print(f"{root}: {len(ok)} configs (ref {refrow[0]['$PRP@PartNo']}), {len(skipped)} skipped (DROP/MISSING/no data), {len(blocked)} geometry-blocked, {n} profile points, {len(hdr)} table cols")
        for b in blocked: print('   BLOCKED', b)
        for s in skipped[:6]: print('   skipped', s)
    json.dump(summary, open(f'{OUT}/gen_straight2_summary.json', 'w'), indent=1)
