

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
