"""gen_ring.py (2026-10-14; STAGED in tools/_out/newtypes_20261014/generators - not yet in the live tools/):
review tables -> SolidWorks build macro + SW2 design table for the hexless revolved parts the fitting generators cannot draw
(no hex, no end modules).

Types (SPEC kind):
- ORING  rubber O-rings - 4000 (Buna-N) and 4001 (Viton) folded into ONE master (same shape, same Air-Way sizes; one master
         per shape), 4005 (flange O-rings) to be folded in when its sizes exist.
- SLEEVE a tube sleeve: closed half-section (front collar, rear spigot, through bore, inner front cone), revolved. Proven on a
         TEST row (0319T = 0319-08: Air-Way L / X, OMi I.D., Brennan 0319-08 STEP for the shape) for the flareless sleeve 0619.

    python gen_ring.py 4000     ->  $GR_OUT (default tools/_out/ring): Build_<root>_MASTER.bas, DesignTable_<root>_SW2.xlsx,
                                    gen_ring_summary.json
Review tables come from $GR_REV (default 04_DESIGN_TABLES; while staged: tools/_out/newtypes_20261014/review_tables).
DataStatus TEST rows (geometry tests, never part data) pass the gate only with GR_TEST=1, and the macro then says TEST BUILD.

Axis: every type revolves about RING_AXIS = Front Plane x Top Plane = the part X axis (the axis every straight master uses).
O-ring DRIVE: a vertical construction line from the origin to the centre of the cross-section circle, length RINGR =
(I.D. + W) / 2, and the circle, diameter CSDIA = W. I.D. = 2 RINGR - CSDIA, O.D. = 2 RINGR + CSDIA.
Sleeve DRIVE: seven lines P0..P6 (front face x = 0, collar, step, spigot, rear face x = L, bore, inner cone) + a vertical
construction line from the origin to the collar corner P1; all dimensions linear (no angle dimensions).
No threads, no hex (O-rings and sleeves: SOP step 5 exception, OMi / user 2026-10-14).
Only BUILD rows with DataStatus VERIFIED / ASSUMED and every size enter the SW2 table (the release gates stay on)."""
import datetime, importlib.util, json, math, os, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.environ.get('GR_TOOLS') or os.path.dirname(HERE)      # 2026-10-20 (ORFS staging): the tools/ folder this copy sits in (was the Windows path)


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P = _load('omi_paths', os.path.join(LIVE, 'omi_paths.py'))                         # read-only use of the live toolchain
sp3 = _load('sp3fix', os.path.join(P.GENERATORS, 'sp3fix.py'))                     # config spot-check block
pp = _load('progress_patch', os.path.join(P.GENERATORS, 'progress_patch.py'))     # progress lines + reference config at save

IN = 0.0254
TODAY = datetime.date.today().isoformat()
REV = os.environ.get('GR_REV', P.DESIGN_TABLES)
OUT = os.environ.get('GR_OUT', os.path.join(P.OUT, 'ring'))
TEST = os.environ.get('GR_TEST') == '1'
DEV = P.DEV

SLEEVE_DIMS = ('L', 'COLLARR', 'COLLARL', 'SPIGOTR', 'BORER', 'FRONTIR', 'CONEL')
SPEC = {
    '4000': dict(name='O-Ring (SAE J1926 stud-end O-rings, Buna-N 4000 + Viton 4001; SAE J1453 face-seal O-rings FS4000)', kind='ORING', tables=('4000', '4001', 'FS4000'),
                 ref='4000-08',
                 assume='ring = torus: cross-section circle of diameter W (CSDIA) centred at RINGR = (I.D. + W) / 2 from the ring '
                        'axis, revolved 360 deg; nominal sizes (Air-Way tolerances in $PRP@Tolerance, not modelled); one master for '
                        '4000 + 4001 (same shape and sizes, material per row)'),
    '0319T': dict(name='Tube Sleeve - SLEEVE model-type TEST (0319-08 shape)', kind='SLEEVE', tables=('0319T',), ref='0319-08',
                  desc='JIC Tube Sleeve',
                  assume='sleeve half-section: front face at x = 0 from FRONTIR to COLLARR, collar to COLLARL, step down to the '
                         'spigot SPIGOTR, rear face at x = L, bore BORER, straight inner front cone from FRONTIR at the front face to '
                         'the bore at CONEL; the R0.062 cone-to-bore blend, the 0.010 corner chamfers and the 1 deg collar taper of '
                         'the Brennan 0319-08 STEP are NOT modelled'),
}


# ==== GROUP C (2026-10-21): CSLEEVE = the compression (bite-type) sleeve C0319 (STAGED, tools/_out/groupC_20261021) ====
# Shape measured on the nine Brennan C0319 STEPs (-04 ... -32; groupC scripts/measure_c0319.py -> measure/c0319_profile.csv): a closed
# 14-line half-section P0..P13, chained from the front bore corner (x = 0, bore radius) along the outside - front face, 40deg nose, 60deg back
# of the nose to the groove, groove, step up, 40deg chamfer, collar, 45deg chamfer, spigot, 10deg tail chamfer, rear face, rear inner bore,
# 15deg inner step, front bore. The six angles are the same on all nine STEPs; the DRIVE sketch carries only linear dimensions (each point
# by its own x / r), so no angle dimension can flip to its supplement. Every value of a row = its own Brennan STEP (single manufacturer).
CSLEEVE_HV = {0: 'V', 3: 'H', 4: 'V', 6: 'H', 8: 'H', 10: 'V', 11: 'H', 13: 'H'}    # segment i = P_i -> P_(i+1)
CSLEEVE_DIMS = [   # (kind, name, index)   cl: construction line origin -> P1 (its length = r1); lineo: horizontal segment to the origin (r);
                   # pto: point to the origin, vertical (r); ptx: front face (segment 0) to a point, horizontal (x); linex: segment 0 to a vertical segment (x)
    ('cl', 'NOSER', 1), ('lineo', 'BORER', 13), ('lineo', 'GROOVER', 3), ('lineo', 'COLLARR', 6), ('lineo', 'SPIGOTR', 8), ('lineo', 'REARIR', 11),
    ('pto', 'APEXR', 2), ('pto', 'STEPR', 5), ('pto', 'TAILR', 10),
    ('ptx', 'APEXX', 2), ('ptx', 'GROOVEX', 3), ('ptx', 'CHAMX', 6), ('ptx', 'COLLARX', 7), ('ptx', 'SPIGOTX', 8), ('ptx', 'TAILX', 9),
    ('ptx', 'REARIX', 12), ('ptx', 'BOREX', 13), ('linex', 'STEPX', 4), ('linex', 'L', 10)]
CSLEEVE_ANG = (None, 40, 60, None, None, 40, None, 45, None, 10, None, None, 15, None)    # measured on every STEP (checked per row, not dimensioned)


def csleeve_points(c):
    """P0..P13 (inches) from the DRIVE values of one row"""
    g = lambda k: c[f'{k}@DRIVE']
    return [(0.0, g('BORER')), (0.0, g('NOSER')), (g('APEXX'), g('APEXR')), (g('GROOVEX'), g('GROOVER')), (g('STEPX'), g('GROOVER')),
            (g('STEPX'), g('STEPR')), (g('CHAMX'), g('COLLARR')), (g('COLLARX'), g('COLLARR')), (g('SPIGOTX'), g('SPIGOTR')),
            (g('TAILX'), g('SPIGOTR')), (g('L'), g('TAILR')), (g('L'), g('REARIR')), (g('REARIX'), g('REARIR')), (g('BOREX'), g('BORER'))]


def csleeve_why(c):
    V = csleeve_points(c); why = []
    for i, a in enumerate(CSLEEVE_ANG):
        if a is None: continue
        (x1, r1), (x2, r2) = V[i], V[(i + 1) % 14]
        got = math.degrees(math.atan2(abs(r2 - r1), abs(x2 - x1)))
        if abs(got - a) > 0.6: why.append(f'segment {i} at {got:.1f} deg (the Brennan STEPs: {a})')
    xs = [p[0] for p in V[:11]]
    if any(xs[k + 1] < xs[k] - 1e-9 for k in range(10)): why.append('outer profile not monotonic along the axis')
    if not (V[0][1] < V[1][1] < V[2][1] and V[3][1] < V[5][1] < V[6][1] and V[11][1] < V[10][1] < V[9][1]): why.append('radii out of order')
    if not (V[0][1] < V[11][1] < V[8][1]): why.append('bore / rear bore / spigot radii out of order')
    return why


def parts_csleeve(ok, refrow):
    c = refrow[0]; V = csleeve_points(c); L, Rc = c['L@DRIVE'], c['COLLARR@DRIVE']; vol = poly_volume(V)
    head = ("'  Axis = X (RING_AXIS); DRIVE = closed half-section P0..P13 (compression sleeve: front face, nose, groove, collar, spigot, tail"
            "\n'  chamfer, rear face, rear bore, inner step, front bore) + construction line origin -> nose top P1; all dimensions linear;"
            "\n'  revolved 360 deg. No hex, no threads.")
    pts = '\n'.join(f'    Set seg({i}) = swSkMgr.CreateLine({V[i][0] * IN:.9f}, {V[i][1] * IN:.9f}, 0, {V[(i + 1) % 14][0] * IN:.9f}, {V[(i + 1) % 14][1] * IN:.9f}, 0)'
                    for i in range(14))
    hv = '\n'.join(f'    swModel.ClearSelection2 True: seg({i}).Select4 False, Nothing: swModel.SketchAddConstraints "{"sgVERTICAL" if t == "V" else "sgHORIZONTAL"}"'
                   for i, t in CSLEEVE_HV.items())
    top = Rc + 0.15; D = []
    for n_, (kind, nm, i) in enumerate(CSLEEVE_DIMS):
        val = c[f'{nm}@DRIVE']; ty = top + 0.06 * (n_ % 6)
        if kind == 'cl':
            D.append(f"    swModel.ClearSelection2 True: cl.Select4 False, Nothing\n    Set dd = swModel.AddDimension2({-0.3 * IN:.6f}, {val / 2 * IN:.6f}, 0)\n    NameDim dd, \"{nm}\", {val * IN:.9f}")
        elif kind == 'lineo':
            D.append(f"    swModel.ClearSelection2 True: seg({i}).Select4 False, Nothing\n    swModel.Extension.SelectByID2 \"Point1@Origin\", \"EXTSKETCHPOINT\", 0, 0, 0, True, 0, Nothing, 0\n"
                     f"    Set dd = swModel.AddDimension2({(L + 0.25 + 0.12 * (n_ % 5)) * IN:.6f}, {val / 2 * IN:.6f}, 0)\n    NameDim dd, \"{nm}\", {val * IN:.9f}")
        elif kind == 'pto':
            D.append(f"    Set ln = seg({i}): swModel.ClearSelection2 True: ln.GetStartPoint2.Select4 False, Nothing\n"
                     f"    swModel.Extension.SelectByID2 \"Point1@Origin\", \"EXTSKETCHPOINT\", 0, 0, 0, True, 0, Nothing, 0\n"
                     f"    Set dd = swModel.AddVerticalDimension2({(-0.45 - 0.12 * (n_ % 4)) * IN:.6f}, {val / 2 * IN:.6f}, 0)\n    NameDim dd, \"{nm}\", {val * IN:.9f}")
        elif kind == 'ptx':
            D.append(f"    Set ln = seg({i}): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing\n"
                     f"    Set dd = swModel.AddDimension2({val / 2 * IN:.6f}, {ty * IN:.6f}, 0)\n    NameDim dd, \"{nm}\", {val * IN:.9f}")
        else:   # linex
            D.append(f"    swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: seg({i}).Select4 True, Nothing\n"
                     f"    Set dd = swModel.AddDimension2({val / 2 * IN:.6f}, {(top + 0.4) * IN:.6f}, 0)\n    NameDim dd, \"{nm}\", {val * IN:.9f}")
    dims = '\n'.join(D)
    drive = f"""    ' ================= 1. DRIVE sketch: closed half-section P0..P13 + construction line origin -> nose top P1 =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim seg(13) As SldWorks.SketchSegment, cl As SldWorks.SketchSegment, i As Long
{pts}
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, {V[1][1] * IN:.9f}, 0)
    cl.ConstructionGeometry = True
    swSkMgr.AddToDB = False
    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, ln As SldWorks.SketchLine
    For i = 0 To 13
        Set ln1 = seg(i): Set ln2 = seg((i + 1) Mod 14)
        swModel.ClearSelection2 True
        ln1.GetEndPoint2.Select4 False, Nothing
        ln2.GetStartPoint2.Select4 True, Nothing
        swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next i
{hv}
    ' construction line: from the origin, vertical, ending on the nose top P1 - puts the front face on x = 0
    Set ln = cl
    swModel.ClearSelection2 True
    ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    swModel.SketchAddConstraints "sgVERTICAL"
    Set ln1 = seg(0)
    swModel.ClearSelection2 True
    ln.GetEndPoint2.Select4 False, Nothing
    ln1.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Check "fourteen profile lines and the construction line created", (Not seg(13) Is Nothing) And (Not cl Is Nothing)
    Dim dd As SldWorks.DisplayDimension
{dims}
"""
    volchk = f'''    Check "Sleeve volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (revolved half-section {vol / IN ** 3:.5f})", Abs(vrev - {vol:.12e}) < {vol:.12e} * 0.002'''
    selfchk = f'''    Check "Sleeve length along the axis " & Format(lenX, "0.0000") & " (expect L {L:.4f})", Abs(lenX - {L}) < 0.005
    Check "Sleeve O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect collar {2 * Rc:.4f})", Abs(dY - {2 * Rc:.6f}) < 0.005 And Abs(dZ - {2 * Rc:.6f}) < 0.005'''
    nq = len(ok)
    bx = ["    ' ---- every configuration: length L along the axis and the collar O.D. across",
          '    stepName = "Sleeve size check"',
          '    Dim rb_c() As String, rb_w() As Double, rb_o() As Double, rb_i As Long, rb_b As Variant, rb_x As Double, rb_y As Double, rb_z As Double',
          f'    ReDim rb_c({nq - 1}): ReDim rb_w({nq - 1}): ReDim rb_o({nq - 1})']
    for i, b in enumerate(ok):
        cc = b[0]
        bx.append(f'    rb_c({i}) = "{cc["$PRP@PartNo"]}": rb_w({i}) = {cc["L@DRIVE"]:.6f}: rb_o({i}) = {2 * cc["COLLARR@DRIVE"]:.6f}')
    bx += [f'    For rb_i = 0 To {nq - 1}',
           '        swModel.ShowConfiguration2 rb_c(rb_i)',
           '        swModel.ForceRebuild3 False',
           '        rb_b = swModel.GetPartBox(True)',
           '        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_',
           '        Check rb_c(rb_i) & ": length " & Format(rb_x, "0.0000") & " (L " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005',
           '    Next rb_i', '']
    return dict(head=head, drive=drive, volchk=volchk, selfchk=selfchk, sizechk='\n'.join(bx),
                params=['L@DRIVE', 'COLLARR@DRIVE', 'BORER@DRIVE', 'REARIX@DRIVE'])


SPEC['C0319'] = dict(name='Compression Sleeve (Ferrule), bite type', kind='CSLEEVE', tables=('C0319',), ref='C0319-08', desc='Compression Sleeve (Ferrule)',
                     assume='COMPRESSION SLEEVE half-section = the Brennan C0319 STEP of the size (14 lines, measured by groupC scripts/measure_c0319.py): '
                            'front face, 40deg nose, 60deg back of the nose, groove, step, 40deg chamfer, collar, 45deg chamfer, spigot, 10deg tail '
                            'chamfer, rear face, rear bore, 15deg inner step, front bore - the six angles equal on all nine STEPs; single manufacturer '
                            '(ASSUMED); no threads, no hex (SOP step-5 exception for sleeves, OMi / user 2026-10-14)')
# ==== end GROUP C ====


def load_review(root):
    # 2026-10-20 (ORFS staging): a table missing from GR_REV is looked up in OMI_REV_EXTRA (the staged FS tables, e.g. FS4000)
    f = os.path.join(REV, f'DesignTable_{root}.xlsx')
    if not os.path.exists(f):
        for d in [d for d in os.environ.get('OMI_REV_EXTRA', '').split(os.pathsep) if d]:
            if os.path.exists(os.path.join(d, f'DesignTable_{root}.xlsx')): f = os.path.join(d, f'DesignTable_{root}.xlsx'); break
    ws = openpyxl.load_workbook(f, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = list(rows[1])
    return [dict(zip(hdr, r)) for r in rows[2:] if r[0]]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def sleeve_points(c):
    """P0..P6 of the sleeve half-section (inches), from the DRIVE values of one row"""
    L, Rc, Lc, Rs, Rb, Rf, Lk = (c[f'{k}@DRIVE'] for k in SLEEVE_DIMS)
    return [(0.0, Rf), (0.0, Rc), (Lc, Rc), (Lc, Rs), (L, Rs), (L, Rb), (Lk, Rb)]


def sleeve_why(c):
    L, Rc, Lc, Rs, Rb, Rf, Lk = (c[f'{k}@DRIVE'] for k in SLEEVE_DIMS)
    why = []
    if not (0 < Rb < Rf < Rc):
        why.append(f'radii must rise bore {Rb} < front-face inner {Rf} < collar {Rc}')
    if not (Rb < Rs < Rc):
        why.append(f'spigot radius {Rs} must lie between the bore {Rb} and the collar {Rc}')
    if not (0 < Lk < Lc < L):
        why.append(f'axial order cone {Lk} < collar {Lc} < length {L} broken')
    return why


def build_rows(root):
    sp = SPEC[root]
    built, skipped = [], []
    gate = ('VERIFIED', 'ASSUMED') + (('TEST',) if TEST else ())
    for t in sp['tables']:
        for r in load_review(t):
            pn = r['$PRP@PartNo']
            if r.get('$PRP@ScopeAction') != 'BUILD':
                skipped.append(f'{pn}: ScopeAction {r.get("$PRP@ScopeAction")}')
                continue
            if r.get('$PRP@DataStatus') not in gate:
                skipped.append(f'{pn}: DataStatus {r.get("$PRP@DataStatus")}')
                continue
            if sp['kind'] == 'ORING':
                idv, w = r.get('ID@DRIVE'), r.get('W@DRIVE')
                if not num(idv) or not num(w):
                    skipped.append(f'{pn}: no I.D. / W')
                    continue
                why = []
                if idv <= 0 or w <= 0:
                    why.append(f'I.D. {idv} / W {w} not positive')
                elif w > idv:
                    why.append(f'cross-section W {w} larger than the I.D. {idv} - check the source row')
                dash = int(pn.split('-')[1])
                mat = str(r.get('$PRP@Material') or '')
                mshort = mat.split(' (')[0].split(',')[0]
                cols = {'RINGR@DRIVE': round((idv + w) / 2, 6), 'CSDIA@DRIVE': round(w, 6),
                        '$PRP@PartNo': pn,
                        '$PRP@Description': (f'{mshort} O-Ring, for -{dash:02d} SAE J1453 O-ring face-seal ends' if t == 'FS4000' else
                                             f'{mshort} O-Ring, for -{dash:02d} SAE J1926 straight-thread stud ends'),     # 2026-10-20: FS4000 folded in (Q-FS-MASTER)
                        '$PRP@GeometryRoot': root,
                        '$PRP@Material': mat,
                        '$PRP@Hardness': r.get('$PRP@Hardness'),
                        '$PRP@ID': f'{idv:.3f}', '$PRP@W': f'{w:.3f}', '$PRP@OD': f'{idv + 2 * w:.3f}',
                        '$PRP@Tolerance': r.get('$PRP@Tolerance'),
                        '$PRP@DataStatus': r['$PRP@DataStatus'],
                        '$PRP@AxialSource': f'{r["$PRP@AxialSource"]} | MODEL: {sp["assume"]}',
                        '$COMMENT': r.get('$COMMENT'),
                        '$PRP@OMiSKU': r.get('$PRP@OMiSKU')}
            elif sp['kind'] == 'CSLEEVE':     # GROUP C (compression sleeve C0319)
                names = [nm for _, nm, _ in CSLEEVE_DIMS]
                vals = {k: r.get(f'{k}@DRIVE') for k in names}
                miss = [k for k, v in vals.items() if not num(v)]
                if miss:
                    skipped.append(f'{pn}: no {"/".join(miss)}')
                    continue
                cols = {f'{k}@DRIVE': round(v, 6) for k, v in vals.items()}
                why = csleeve_why(cols)
                cols.update({'$PRP@PartNo': pn, '$PRP@Description': f'{sp["desc"]}, {r.get("$PRP@TubeOD") or ""} in tube'.replace(',  in tube', ''),
                             '$PRP@GeometryRoot': root, '$PRP@OD': f'{2 * vals["COLLARR"]:.3f}', '$PRP@ID': f'{2 * vals["BORER"]:.3f}',
                             '$PRP@Length': f'{vals["L"]:.3f}', '$PRP@DataStatus': r['$PRP@DataStatus'],
                             '$PRP@AxialSource': f'{r["$PRP@AxialSource"]} | MODEL: {sp["assume"]}', '$COMMENT': r.get('$COMMENT'),
                             '$PRP@OMiSKU': r.get('$PRP@OMiSKU')})
            else:
                vals = {k: r.get(f'{k}@DRIVE') for k in SLEEVE_DIMS}
                miss = [k for k, v in vals.items() if not num(v)]
                if miss:
                    skipped.append(f'{pn}: no {"/".join(miss)}')
                    continue
                cols = {f'{k}@DRIVE': round(v, 6) for k, v in vals.items()}
                why = sleeve_why(cols)
                cols.update({'$PRP@PartNo': pn,
                             '$PRP@Description': f'{sp["desc"]}, {r.get("$PRP@TubeOD") or ""} in tube'.replace(',  in tube', ''),
                             '$PRP@GeometryRoot': root,
                             '$PRP@OD': f'{2 * vals["COLLARR"]:.3f}', '$PRP@ID': f'{2 * vals["BORER"]:.3f}',
                             '$PRP@Length': f'{vals["L"]:.3f}',
                             '$PRP@DataStatus': r['$PRP@DataStatus'],
                             '$PRP@AxialSource': f'{r["$PRP@AxialSource"]} | MODEL: {sp["assume"]}',
                             '$COMMENT': r.get('$COMMENT'),
                             '$PRP@OMiSKU': r.get('$PRP@OMiSKU')})
            built.append((cols, why))
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


HELPERS_SRC = open(os.path.join(P.TEMPLATES, 'Build_2405_MASTER.bas')).read()       # frozen VBA helper library (2405 macro)


def sub(text, name, kind='Sub'):
    i = text.index(f'\n{kind} {name}(')
    j = text.index(f'\nEnd {kind}', i) + len(f'\nEnd {kind}')
    return text[i + 1:j] + '\n\n'


HELP = ''.join(sub(HELPERS_SRC, n) for n in ('Trace', 'Check', 'NameDim')) + sub(HELPERS_SRC, 'Volume', 'Function')


def parts_oring(ok, refrow):
    c = refrow[0]
    R, D = c['RINGR@DRIVE'], c['CSDIA@DRIVE']
    r = D / 2
    vol = 2 * math.pi ** 2 * (R * IN) * (r * IN) ** 2              # torus volume, m^3
    od = 2 * R + D
    idv = 2 * R - D
    head = "'  Ring axis = X (RING_AXIS); DRIVE = cross-section circle CSDIA at RINGR from the axis; revolved 360 deg. No hex, no threads."
    drive = f'''    ' ================= 1. DRIVE sketch: construction line origin -> section centre (RINGR) + section circle (CSDIA) =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim cl As SldWorks.SketchSegment, circ As SldWorks.SketchSegment
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, {R * IN:.9f}, 0)
    cl.ConstructionGeometry = True
    Set circ = swSkMgr.CreateCircleByRadius(0, {R * IN:.9f}, 0, {r * IN:.9f})
    swSkMgr.AddToDB = False
    Check "construction line and section circle created", (Not cl Is Nothing) And (Not circ Is Nothing)
    Dim ln As SldWorks.SketchLine, arc As SldWorks.SketchArc
    Set ln = cl: Set arc = circ
    swModel.ClearSelection2 True
    ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True
    ln.GetEndPoint2.Select4 False, Nothing
    arc.GetCenterPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Dim dd As SldWorks.DisplayDimension
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    Set dd = swModel.AddDimension2({-(r + 0.25) * IN:.6f}, {R / 2 * IN:.6f}, 0)
    NameDim dd, "RINGR", {R * IN:.9f}
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Set dd = swModel.AddDimension2({(r + 0.3) * IN:.6f}, {(R + r + 0.2) * IN:.6f}, 0)
    NameDim dd, "CSDIA", {D * IN:.9f}
'''
    volchk = f'''    Check "Ring volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (torus 2 pi^2 R r^2 = {vol / IN ** 3:.5f})", Abs(vrev - {vol:.12e}) < {vol:.12e} * 0.002

    ' ---- 2026-10-15: a torus has no edges, so a drawing has nothing to dimension. Split its face along the silhouettes seen
    '      along X (-> circles at the I.D. and O.D., x = 0) and along Z (-> the pitch circles at x = +-W/2 and the two cross-section
    '      circles in the Front Plane). Before the design table, so the splits exist in every configuration; volume unchanged.
    stepName = "Split lines"
    Dim sl_b As Variant, sl_f As Variant, sl_i As Long, sl_sd As SldWorks.SelectData, sl_ent As SldWorks.Entity, sl_n As Long
    Dim sl_names As Variant, sl_k As Long
    sl_names = Array("SPLIT_AXIAL", "SPLIT_SIDE")
    For sl_k = 0 To 1
        swModel.ClearSelection2 True
        sl_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
        sl_f = sl_b(0).GetFaces
        For sl_i = LBound(sl_f) To UBound(sl_f)
            Set sl_sd = swSelMgr.CreateSelectData: sl_sd.Mark = 1
            Set sl_ent = sl_f(sl_i)
            sl_ent.Select4 True, sl_sd
        Next sl_i
        swModel.Extension.SelectByID2 IIf(sl_k = 0, "Right Plane", "Front Plane"), "PLANE", 0, 0, 0, True, 2, Nothing, 0
        swModel.InsertSplitLineSil
        Set swFeat = swModel.FeatureByPositionReverse(0)
        If swFeat.GetTypeName2 = "PLine" Then swFeat.Name = sl_names(sl_k)
        Check "split line " & sl_names(sl_k) & " created (silhouette seen along " & IIf(sl_k = 0, "X", "Z") & ")", swFeat.GetTypeName2 = "PLine"
    Next sl_k
    swModel.ClearSelection2 True
    sl_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    sl_n = sl_b(0).GetFaceCount
    Check "ring face split into 8 faces (found " & sl_n & ")", sl_n = 8
    Check "volume unchanged by the split lines", Abs(Volume() - vrev) < {vol:.12e} * 0.000001'''
    selfchk = f'''    Check "Ring thickness along the axis " & Format(lenX, "0.0000") & " (expect W {D:.4f})", Abs(lenX - {D}) < 0.005
    Check "Ring O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect {od:.4f} = I.D. {idv:.4f} + 2 W)", Abs(dY - {od:.6f}) < 0.005 And Abs(dZ - {od:.6f}) < 0.005'''
    # every configuration: box = W along the axis and O.D. across it (the sweep proves each rebuilds; this proves each size)
    nq = len(ok)
    bx = ["    ' ---- every configuration: the ring is W thick along its axis and O.D. across (I.D. = O.D. - 2 W)",
          '    stepName = "Ring size check"',
          '    Dim rb_c() As String, rb_w() As Double, rb_o() As Double, rb_i As Long, rb_b As Variant, rb_x As Double, rb_y As Double, rb_z As Double',
          f'    ReDim rb_c({nq - 1}): ReDim rb_w({nq - 1}): ReDim rb_o({nq - 1})']
    for i, b in enumerate(ok):
        cc = b[0]
        bx.append(f'    rb_c({i}) = "{cc["$PRP@PartNo"]}": rb_w({i}) = {cc["CSDIA@DRIVE"]:.6f}: rb_o({i}) = {2 * cc["RINGR@DRIVE"] + cc["CSDIA@DRIVE"]:.6f}')
    bx += [f'    For rb_i = 0 To {nq - 1}',
           '        swModel.ShowConfiguration2 rb_c(rb_i)',
           '        swModel.ForceRebuild3 False',
           '        rb_b = swModel.GetPartBox(True)',
           '        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_',
           '        Check rb_c(rb_i) & ": thickness " & Format(rb_x, "0.0000") & " (W " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005',
           '        rb_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)',
           '        Check rb_c(rb_i) & ": split lines present (8 faces, found " & rb_b(0).GetFaceCount & ")", rb_b(0).GetFaceCount = 8',
           '    Next rb_i', '']
    return dict(head=head, drive=drive, volchk=volchk, selfchk=selfchk, sizechk='\n'.join(bx), params=['RINGR@DRIVE', 'CSDIA@DRIVE'])


def poly_volume(V):
    """volume (m^3) of the closed polygon V (inches, (x, r)) revolved about the x axis - sum of signed frusta"""
    v = 0.0
    for i in range(len(V)):
        (x1, r1), (x2, r2) = V[i], V[(i + 1) % len(V)]
        a, b = r1 * IN, r2 * IN
        v += math.pi * (x2 - x1) * IN * (a * a + a * b + b * b) / 3
    return abs(v)


def parts_sleeve(ok, refrow):
    c = refrow[0]
    V = sleeve_points(c)
    L, Rc = c['L@DRIVE'], c['COLLARR@DRIVE']
    vol = poly_volume(V)
    head = ("'  Axis = X (RING_AXIS); DRIVE = closed half-section P0..P6 (front face x = 0, collar, step, spigot, rear face x = L, bore,"
            "\n'  inner front cone) + construction line origin -> collar corner; revolved 360 deg. No hex, no threads.")
    pts = '\n'.join(f'    Set seg({i}) = swSkMgr.CreateLine({V[i][0] * IN:.9f}, {V[i][1] * IN:.9f}, 0, {V[(i + 1) % 7][0] * IN:.9f}, {V[(i + 1) % 7][1] * IN:.9f}, 0)'
                    for i in range(7))
    # dimension text positions (inches): above the collar, left of the front face, right of the rear face
    top = Rc + 0.15
    drive = f'''    ' ================= 1. DRIVE sketch: closed half-section P0..P6 + construction line origin -> collar corner P1 =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim seg(6) As SldWorks.SketchSegment, cl As SldWorks.SketchSegment, i As Long
{pts}
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, {Rc * IN:.9f}, 0)
    cl.ConstructionGeometry = True
    swSkMgr.AddToDB = False
    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, ln As SldWorks.SketchLine
    For i = 0 To 6
        Set ln1 = seg(i): Set ln2 = seg((i + 1) Mod 7)
        swModel.ClearSelection2 True
        ln1.GetEndPoint2.Select4 False, Nothing
        ln2.GetStartPoint2.Select4 True, Nothing
        swModel.SketchAddConstraints "sgMERGEPOINTS"
    Next i
    ' P0-P1 front face, P2-P3 step, P4-P5 rear face vertical; P1-P2 collar, P3-P4 spigot, P5-P6 bore horizontal; P6-P0 = the cone
    For i = 0 To 5
        swModel.ClearSelection2 True
        seg(i).Select4 False, Nothing
        If i Mod 2 = 0 Then swModel.SketchAddConstraints "sgVERTICAL" Else swModel.SketchAddConstraints "sgHORIZONTAL"
    Next i
    ' construction line: from the origin, vertical, ending on the collar corner P1 - puts the front face on x = 0
    Set ln = cl
    swModel.ClearSelection2 True
    ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    swModel.SketchAddConstraints "sgVERTICAL"
    Set ln1 = seg(0)
    swModel.ClearSelection2 True
    ln.GetEndPoint2.Select4 False, Nothing
    ln1.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Check "seven profile lines and the construction line created", (Not seg(6) Is Nothing) And (Not cl Is Nothing)
    Dim dd As SldWorks.DisplayDimension
    ' COLLARR = construction line length (origin to the collar corner)
    swModel.ClearSelection2 True
    cl.Select4 False, Nothing
    Set dd = swModel.AddDimension2({-0.3 * IN:.6f}, {Rc / 2 * IN:.6f}, 0)
    NameDim dd, "COLLARR", {Rc * IN:.9f}
    ' L = front face to rear face
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    seg(4).Select4 True, Nothing
    Set dd = swModel.AddDimension2({L / 2 * IN:.6f}, {(top + 0.3) * IN:.6f}, 0)
    NameDim dd, "L", {L * IN:.9f}
    ' COLLARL = front face to the step face
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    seg(2).Select4 True, Nothing
    Set dd = swModel.AddDimension2({V[2][0] / 2 * IN:.6f}, {top * IN:.6f}, 0)
    NameDim dd, "COLLARL", {V[2][0] * IN:.9f}
    ' SPIGOTR / BORER = origin to the spigot line / the bore line
    swModel.ClearSelection2 True
    seg(3).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2({(L + 0.3) * IN:.6f}, {V[3][1] / 2 * IN:.6f}, 0)
    NameDim dd, "SPIGOTR", {V[3][1] * IN:.9f}
    swModel.ClearSelection2 True
    seg(5).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2({(L + 0.55) * IN:.6f}, {V[5][1] / 2 * IN:.6f}, 0)
    NameDim dd, "BORER", {V[5][1] * IN:.9f}
    ' FRONTIR = origin to P0 (vertical), CONEL = front face to P6 (where the cone meets the bore)
    Set ln1 = seg(0)
    swModel.ClearSelection2 True
    ln1.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2({-0.55 * IN:.6f}, {V[0][1] / 2 * IN:.6f}, 0)
    NameDim dd, "FRONTIR", {V[0][1] * IN:.9f}
    Set ln1 = seg(6)
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    ln1.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2({V[6][0] / 2 * IN:.6f}, {(V[6][1] - 0.15) * IN:.6f}, 0)
    NameDim dd, "CONEL", {V[6][0] * IN:.9f}
'''
    volchk = f'''    Check "Sleeve volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (revolved half-section {vol / IN ** 3:.5f})", Abs(vrev - {vol:.12e}) < {vol:.12e} * 0.002'''
    selfchk = f'''    Check "Sleeve length along the axis " & Format(lenX, "0.0000") & " (expect L {L:.4f})", Abs(lenX - {L}) < 0.005
    Check "Sleeve O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect collar {2 * Rc:.4f})", Abs(dY - {2 * Rc:.6f}) < 0.005 And Abs(dZ - {2 * Rc:.6f}) < 0.005'''
    nq = len(ok)
    bx = ["    ' ---- every configuration: length L along the axis and the collar O.D. across",
          '    stepName = "Sleeve size check"',
          '    Dim rb_c() As String, rb_w() As Double, rb_o() As Double, rb_i As Long, rb_b As Variant, rb_x As Double, rb_y As Double, rb_z As Double',
          f'    ReDim rb_c({nq - 1}): ReDim rb_w({nq - 1}): ReDim rb_o({nq - 1})']
    for i, b in enumerate(ok):
        cc = b[0]
        bx.append(f'    rb_c({i}) = "{cc["$PRP@PartNo"]}": rb_w({i}) = {cc["L@DRIVE"]:.6f}: rb_o({i}) = {2 * cc["COLLARR@DRIVE"]:.6f}')
    bx += [f'    For rb_i = 0 To {nq - 1}',
           '        swModel.ShowConfiguration2 rb_c(rb_i)',
           '        swModel.ForceRebuild3 False',
           '        rb_b = swModel.GetPartBox(True)',
           '        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_',
           '        Check rb_c(rb_i) & ": length " & Format(rb_x, "0.0000") & " (L " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005',
           '    Next rb_i', '']
    return dict(head=head, drive=drive, volchk=volchk, selfchk=selfchk, sizechk='\n'.join(bx),
                params=['L@DRIVE', 'COLLARR@DRIVE', 'BORER@DRIVE', 'CONEL@DRIVE'])


def emit(root, hdr, ok, refrow):
    sp = SPEC[root]
    PN = refrow[0]['$PRP@PartNo']
    k = parts_csleeve(ok, refrow) if sp['kind'] == 'CSLEEVE' else (parts_oring if sp['kind'] == 'ORING' else parts_sleeve)(ok, refrow)     # GROUP C: CSLEEVE
    params = k['params']
    chk = [ok[1], ok[-1]] if len(ok) > 2 else [ok[-1]]
    if sp['kind'] == 'ORING' and len(ok) > 2:   # 2026-10-20 (ORFS staging): the FS4000 rows come last - keep the spot check on the largest ring
        chk = [ok[1], max(ok[1:][::-1], key=lambda b: b[0][params[0]])]   # the last of equal sizes, as before
    blk = sp3.check_block([(b[0]['$PRP@PartNo'], [b[0][p] for p in params]) for b in chk], params)
    entry = f'Build{root}'
    testline = ("\n'  TEST BUILD: DataStatus TEST rows - geometry test of the model type only, never part data; never ship this macro."
                if any(b[0]['$PRP@DataStatus'] == 'TEST' for b in ok) else '')
    vba = f'''Attribute VB_Name = "Build_{root}_MASTER"
' ============================================================================
'  Build_{root}_MASTER.bas  -  OMi fitting library, generated {TODAY} by gen_ring.py
'  {sp['name']} - master from reference configuration {PN} (DesignTable_{root}_SW2.xlsx row 2)
{k['head']}
'  Run in SolidWorks: Tools > Macro > Run > {entry}.  Report: 03_SCRIPTS\\Build_{root}_report.txt{testline}
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "{DEV}\\04_DESIGN_TABLES\\DesignTable_{root}_SW2.xlsx"
Const SAVE_PATH  As String = "{DEV}\\11_MASTERS\\{root}_MASTER.SLDPRT"
Const REPORT_PATH As String = "{DEV}\\03_SCRIPTS\\Build_{root}_report.txt"

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String

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
    report = "": nErr = 0
    fnRep = FreeFile
    Open REPORT_PATH For Output As #fnRep
    Print #fnRep, "Build_{root}_MASTER  " & Now
    On Error GoTo Trap
    Dim swFeat As SldWorks.Feature
    Dim ok As Boolean

    ' ================= 0. ring axis = part X axis (Front Plane x Top Plane) =================
    stepName = "Ring axis"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swModel.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, True, 0, Nothing, 0
    ok = swModel.InsertAxis2(True)
    Check "RING_AXIS inserted (Front Plane x Top Plane = X axis)", ok
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "RING_AXIS"
    swModel.ClearSelection2 True

{k['drive']}    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "DRIVE"
    Check "DRIVE sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)

    ' ================= 2. revolve 360 deg about RING_AXIS =================
    stepName = "Revolve"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "DRIVE", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    swModel.Extension.SelectByID2 "RING_AXIS", "AXIS", 0, 0, 0, True, 16, Nothing, 0
    Dim rev As SldWorks.Feature
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "Revolve created", Not rev Is Nothing
    If rev Is Nothing Then GoTo Finish
    rev.Name = "BODY"
    ' the reference axis stays in the tree (it carries the revolve) but is hidden in the saved part
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "RING_AXIS", "AXIS", 0, 0, 0, False, 0, Nothing, 0
    swModel.BlankRefGeom
    swModel.ClearSelection2 True
    Dim vrev As Double: vrev = Volume()
{k['volchk']}

    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
{k['selfchk']}
    Dim bodies As Variant
    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body", (UBound(bodies) = 0)

    stepName = "Design table"
    swModel.ClearSelection2 True
    ok = swModel.InsertFamilyTableOpen(TABLE_PATH)
    Check "Design table inserted from " & TABLE_PATH, ok
    swModel.CloseFamilyTable
    swModel.ForceRebuild3 False
    Dim cfgs As Variant
    cfgs = swModel.GetConfigurationNames
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect {len(ok) + 1})", (UBound(cfgs) + 1) >= {len(ok)}
{blk}{k['sizechk']}
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
    Trace "No THD_ features in this master ({'O-rings' if sp['kind'] == 'ORING' else 'sleeves'} carry no threads)"

    stepName = "Save"
    Dim e As Long, w As Long, t0 As Date, fdt As Date
    t0 = Now
    ok = swModel.Extension.SaveAs(SAVE_PATH, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
    Trace "SaveAs " & SAVE_PATH & " returned " & ok & " (error " & e & ", warning " & w & ")"
    If ok = False Then          ' not 'If Not ok': SolidWorks returns True as 1 and Not 1 = -2 (CLAUDE.md VBA trap)
        ' SolidWorks can return False (error 0) although it wrote the file: trust the file on disk when it is fresh
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

' ---------------------------------------------------------------- helpers (shared library, SP3-validated on 2403/2405/2502HX)
{HELP}'''
    vba = pp.ref_config_at_save(pp.add_progress(vba))
    p = os.path.join(OUT, f'Build_{root}_MASTER.bas')
    open(p, 'w').write(vba)
    return p


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    summary = {}
    for root in sys.argv[1:]:
        built, skipped = build_rows(root)
        if not [b for b in built if not b[1]]:
            # nothing passes the gates (e.g. TEST rows without GR_TEST=1): write no macro / table, say why
            summary[root] = dict(configs=0, skipped=skipped, blocked=[b[0]['$PRP@PartNo'] + ': ' + '; '.join(b[1]) for b in built], review=REV, test=TEST)
            print(f'{root}: 0 buildable rows - no macro written ({len(skipped)} skipped, {len(built)} blocked)')
            for s in skipped:
                print('   skipped', s)
            continue
        table, hdr, ok, refrow = write_sw2(root, built)
        macro = emit(root, hdr, ok, refrow)
        blocked = [b[0]['$PRP@PartNo'] + ': ' + '; '.join(b[1]) for b in built if b[1]]
        summary[root] = dict(configs=len(ok), ref=refrow[0]['$PRP@PartNo'], skipped=skipped, blocked=blocked, cols=len(hdr),
                             review=REV, test=TEST, names=[b[0]['$PRP@PartNo'] for b in ok])
        print(f'{root}: {len(ok)} configs (ref {refrow[0]["$PRP@PartNo"]}), {len(skipped)} skipped, {len(blocked)} blocked, {len(hdr)} table cols')
        for b in blocked:
            print('   BLOCKED', b)
        for s in skipped:
            print('   skipped', s)
    json.dump(summary, open(os.path.join(OUT, f'gen_ring_summary_{"_".join(sys.argv[1:])}.json'), 'w'), indent=1)
