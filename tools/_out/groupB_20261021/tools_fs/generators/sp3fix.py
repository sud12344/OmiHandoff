"""SolidWorks 2026 SP3 fix: diameter sketch dims -> radius dims (+ table halved), config spot-check."""
import re, openpyxl, sys
def tpi(t): return float(re.search(r'-(\d+(?:\s1/2)?)(?!\s*/)',t).group(1).replace(' 1/2','.5'))
REN_RE=[(r'^BODYDIA$','BODYR'),(r'^THDMAJ_(\w+)$',r'THDMAJR_\1'),(r'^JIC(\w*)_CONEDIA$',r'JIC\1_CONER')]
def ren(nm):
    for p,r in REN_RE:
        if re.match(p,nm): return re.sub(p,r,nm)
    return None
DIMRAD='''Sub Dim_rad(i As Long, nm As String, valM As Double, tx As Double, ty As Double)
    ' SolidWorks 2026 SP3: a line-to-centreline dimension is created as the RADIUS (distance to axis) and a
    ' diametric-display flip is not driven by the design table.  So the master carries radius dims
    ' (BODYR, THDMAJR_*, JIC*_CONER) and the SW2 table columns hold half the catalog diameter.
    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long
    For k = 1 To 3
        swModel.ClearSelection2 True
        seg(i).Select4 False, Nothing
        axisCL.Select4 True, Nothing
        Set dd = swModel.AddDimension2(tx, ty * k, 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - valM) < 0.000005 Then Exit For
        Trace nm & " try " & k & ": value " & Format(v / IN_, "0.0000") & " (want radius " & Format(valM / IN_, "0.0000") & ")"
        DeleteDisp dd: Set dd = Nothing
    Next k
    NameDim dd, nm, valM
End Sub'''
def check_block(cfgs, params):
    # cfgs: list of (name, [want...]) ; params: list of 'NAME@SKETCH'
    L=['    \' ---- config spot check: do the table values actually land in the model? (SP3 lesson)',
       '    stepName = "Config check"',
       '    Dim cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature',
       '    cx_c = Array(' + ', '.join(f'"{n}"' for n,_ in cfgs) + ')',
       '    cx_p = Array(' + ', '.join(f'"{p}"' for p in params) + ')',
       '    cx_w = Array(' + ', '.join('Array(' + ', '.join(f'{v:.5f}' for v in w) + ')' for _,w in cfgs) + ')',
       f'    For cx_q = 0 To {len(cfgs)-1}',
       '        swModel.ShowConfiguration2 cx_c(cx_q)',
       '        swModel.ForceRebuild3 False',
       f'        For cx_k = 0 To {len(params)-1}',
       '            Set cx_prm = swModel.Parameter(cx_p(cx_k))',
       '            If cx_prm Is Nothing Then',
       '                Check cx_c(cx_q) & " " & cx_p(cx_k) & " readable", False',
       '            Else',
       '                Check cx_c(cx_q) & " " & cx_p(cx_k) & " = " & Format(cx_prm.SystemValue / IN_, "0.0000") & " (table " & Format(cx_w(cx_q)(cx_k), "0.0000") & ")", Abs(cx_prm.SystemValue / IN_ - cx_w(cx_q)(cx_k)) < 0.0005',
       '            End If',
       '        Next cx_k',
       '        cx_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)',
       '        cx_nb = IIf(IsEmpty(cx_b), 0, UBound(cx_b) + 1)',
       '        Check cx_c(cx_q) & " one solid body (found " & cx_nb & ")", cx_nb = 1',
       '        Set cx_f = swModel.FirstFeature',
       '        Do While Not cx_f Is Nothing',
       '            If cx_f.GetErrorCode2(True) <> 0 And Not cx_f.IsSuppressed Then Check cx_c(cx_q) & " feature " & cx_f.Name & " rebuilds (error code " & cx_f.GetErrorCode2(True) & ")", False',
       '            Set cx_f = cx_f.GetNextFeature',
       '        Loop',
       '        cx_bx = swModel.GetPartBox(True)',
       '        Trace cx_c(cx_q) & " box x " & Format(cx_bx(0) / IN_, "0.000") & ".." & Format(cx_bx(3) / IN_, "0.000") & "  y " & Format(cx_bx(1) / IN_, "0.000") & ".." & Format(cx_bx(4) / IN_, "0.000")',
       '    Next cx_q',
       '']
    return '\n'.join(L)

def fix_table(path, ends):
    """ends: list of (sfx, tm_col, tz_col, thr_col) for Thread-feature ends (THD_End<sfx>); helix *_sfx cols dropped."""
    wb=openpyxl.load_workbook(path); ws=wb.active
    h=[c.value for c in ws[1]]; rows=[[c.value for c in r] for r in ws.iter_rows(min_row=2)]
    # 1) drop helix columns of thread-feature ends
    drop=set()
    for sfx,*_ in ends:
        drop|={i for i,c in enumerate(h) if c in (f'HELIXDIA@HELIXSK_{sfx}',f'HEIGHT@HELIX_{sfx}',f'PITCH@HELIX_{sfx}',f'PROF_R@THDPROF_{sfx}',f'APEXR@THDPROF_{sfx}',f'PROF_AX@THDPROF_{sfx}')}
    keep=[i for i in range(len(h)) if i not in drop]; h=[h[i] for i in keep]; rows=[[r[i] for i in keep] for r in rows]
    # 2) rename + halve diameter columns
    conv={}
    for i,c in enumerate(h):
        if c and '@' in c:
            nm,sk=c.split('@'); r=ren(nm)
            if r: h[i]=f'{r}@{sk}'; conv[i]=c
    for r in rows:
        for i in conv: r[i]=round(r[i]/2,5)
    # 3) thread-feature columns before $PRP
    pi=h.index('$PRP@PartNo'); new=[]; 
    for sfx,tm,tz,thr in ends: new+=[f'THDDIA@THD_End{sfx}',f'THDPITCH@THD_End{sfx}',f'DEPTH@THD_End{sfx}']
    d0=dict(zip(h,rows[0]))
    out=[]
    for r in rows:
        d=dict(zip(h,r)); vals=[]
        for sfx,tm,tz,thr in ends:
            rtm=ren(tm.split('@')[0])+'@'+tm.split('@')[1]
            vals+=[round(d[rtm]*2,5), round(1/tpi(str(d[thr])),4), d[tz]]
        out.append(r[:pi]+vals+r[pi:])
    h2=h[:pi]+new+h[pi:]
    nb=openpyxl.Workbook(); s=nb.active; s.title='Sheet1'; s.append(h2)
    for r in out: s.append(r)
    nb.save(path)
    return h2, out, [conv[i] for i in sorted(conv)]

def fix_macro(src, dst, ref, cfg_names, params, table_h, table_rows):
    s=open(src).read()
    def sub(m):
        idx,nm,val,rest=m.group(1),m.group(2),float(m.group(3)),m.group(4)
        r=ren(nm); assert r, nm
        return f'Call Dim_rad({idx}, "{r}", {val/2:.9f},{rest})'
    s,n=re.subn(r'Call Dim_dia\((\d+), "(\w+)", ([\d.]+),([^)]*)\)', sub, s)
    i=s.index('Sub Dim_dia('); j=s.index('End Sub',i)+len('End Sub'); s=s[:i]+DIMRAD+s[j:]
    assert 'Dim_dia' not in s
    pn=table_h.index('$PRP@PartNo')
    cfgs=[]
    for cn in cfg_names:
        row=[r for r in table_rows if r[pn]==cn][0]; d=dict(zip(table_h,row))
        cfgs.append((cn,[d[p] for p in params]))
    blk=check_block(cfgs, params)
    anchor=f'    swModel.ShowConfiguration2 "{ref}"\n'
    assert s.count(anchor)==1, s.count(anchor)
    s=s.replace(anchor, blk+anchor+'    swModel.ForceRebuild3 False\n')
    open(dst,'w').write(s); return n

DIMANG = """Sub Dim_ang(i As Long, j As Long, nm As String, valRad As Double, tx As Double, ty As Double)
    ' Placement candidates (2026-09-25): first on the bisector of the sector that has the wanted angle, around the two
    ' lines' intersection (the older candidates never found 50 deg for the swivel countersink); then the caller's point
    ' first (the old behaviour), then the four quadrants around the vertex the two lines share.  Mirroring through the
    ' ORIGIN only works when the leg axis passes through it (2403/2500/2603); on 2502 the JIC leg axis is at x = N1, so
    ' the vertex-relative candidates are what find the 60 deg side.  A rejected try is deleted (DeleteDisp works since
    ' 2026-09-25); if no try gives the wanted angle, the first placement is re-created and kept UNNAMED: its
    ' supplementary angle fixes the same line, and a named supplement would be driven the wrong way by the table.
    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long, nC As Long, nI As Long
    Dim cand(15) As Double, candy(15) As Double
    Dim ix As Double, iy As Double, wx As Double, wy As Double
    nI = 0
    If AngleBisector(i, j, valRad, ix, iy, wx, wy) Then
        cand(0) = ix + 0.004 * wx: candy(0) = iy + 0.004 * wy
        cand(1) = ix - 0.004 * wx: candy(1) = iy - 0.004 * wy
        cand(2) = ix + 0.008 * wx: candy(2) = iy + 0.008 * wy
        cand(3) = ix - 0.008 * wx: candy(3) = iy - 0.008 * wy
        nI = 4
    End If
    cand(nI) = tx: candy(nI) = ty
    cand(nI + 1) = tx: candy(nI + 1) = -ty
    cand(nI + 2) = -tx: candy(nI + 2) = ty
    cand(nI + 3) = -tx: candy(nI + 3) = -ty
    cand(nI + 4) = tx + 0.003: candy(nI + 4) = 0.002
    cand(nI + 5) = tx - 0.003: candy(nI + 5) = 0.002
    nC = nI + 5
    Dim px As Double, py As Double, dq As Double
    If SegVertex(i, j, px, py) Then
        dq = 0.0025
        cand(nC + 1) = px + dq: candy(nC + 1) = py + dq
        cand(nC + 2) = px + dq: candy(nC + 2) = py - dq
        cand(nC + 3) = px - dq: candy(nC + 3) = py + dq
        cand(nC + 4) = px - dq: candy(nC + 4) = py - dq
        cand(nC + 5) = px + 3 * dq: candy(nC + 5) = py
        cand(nC + 6) = px - 3 * dq: candy(nC + 6) = py
        nC = nC + 6
    Else
        Trace nm & ": the two lines share no endpoint - vertex candidates unavailable"
    End If
    For k = 0 To nC
        swModel.ClearSelection2 True
        seg(i).Select4 False, Nothing
        If j = NPTS - 1 Then axisCL.Select4 True, Nothing Else seg(j).Select4 True, Nothing
        Set dd = swModel.AddDimension2(cand(k), candy(k), 0)
        If Not dd Is Nothing Then
            v = dd.GetDimension2(0).SystemValue
            If Abs(v - valRad) < 0.0005 Then Exit For
            Trace nm & " angle try " & k & " at (" & Format(cand(k) / IN_, "0.000") & ", " & Format(candy(k) / IN_, "0.000") & "): " & Format(v * 180 / 3.14159265358979, "0.0") & " deg (want " & Format(valRad * 180 / 3.14159265358979, "0.0") & ")"
            DeleteDisp dd: Set dd = Nothing
        End If
    Next k
    If dd Is Nothing Then
        ' When the two segments do not meet (swivel countersink vs the axis centreline) SolidWorks dimensions the
        ' directed angle between them whatever the text position (probed 2026-09-25: 24 positions, all 130 deg).
        ' Keep that supplement: it fixes the same line.  It is named <nm>_SUPPL so a table column <nm> can never
        ' drive it the wrong way.
        swModel.ClearSelection2 True
        seg(i).Select4 False, Nothing
        If j = NPTS - 1 Then axisCL.Select4 True, Nothing Else seg(j).Select4 True, Nothing
        Set dd = swModel.AddDimension2(cand(0), candy(0), 0)
        If Not dd Is Nothing Then v = dd.GetDimension2(0).SystemValue
        If Not dd Is Nothing And Abs(v - (3.14159265358979 - valRad)) < 0.0005 Then
            dd.GetDimension2(0).Name = nm & "_SUPPL"
            Check "angle " & nm & " held by its supplement " & nm & "_SUPPL = " & Format(v * 180 / 3.14159265358979, "0.00") & " deg (same line; the segments do not meet)", True
        Else
            Check nm & ": no placement gave " & Format(valRad * 180 / 3.14159265358979, "0.0") & " deg - kept an unnamed " & Format(v * 180 / 3.14159265358979, "0.0") & " deg", False
        End If
        Exit Sub
    End If
    If Right(nm, 6) = "_plain" Then
        Check "plain angle " & Left(nm, Len(nm) - 6) & " placed = " & Format(v * 180 / 3.14159265358979, "0.0") & " deg", (Not dd Is Nothing) And Abs(v - valRad) < 0.0005
    Else
        NameAng dd, nm, valRad
    End If
End Sub

Function SegVertex(i As Long, j As Long, ByRef px As Double, ByRef py As Double) As Boolean
    ' the sketch point shared by seg(i) and seg(j) (or the centreline), in sketch coordinates
    On Error Resume Next
    Dim a As SldWorks.SketchLine, b As SldWorks.SketchLine
    Set a = seg(i)
    If j = NPTS - 1 Then Set b = axisCL Else Set b = seg(j)
    If a Is Nothing Or b Is Nothing Then Exit Function
    Dim ax(1) As Double, ay(1) As Double, bx(1) As Double, by(1) As Double, m As Long, n As Long
    ax(0) = a.GetStartPoint2.X: ay(0) = a.GetStartPoint2.Y
    ax(1) = a.GetEndPoint2.X: ay(1) = a.GetEndPoint2.Y
    bx(0) = b.GetStartPoint2.X: by(0) = b.GetStartPoint2.Y
    bx(1) = b.GetEndPoint2.X: by(1) = b.GetEndPoint2.Y
    If Err.Number <> 0 Then Err.Clear: Exit Function
    For m = 0 To 1
        For n = 0 To 1
            If Abs(ax(m) - bx(n)) < 0.000001 And Abs(ay(m) - by(n)) < 0.000001 Then
                px = ax(m): py = ay(m): SegVertex = True: Exit Function
            End If
        Next n
    Next m
End Function

Function AngleBisector(i As Long, j As Long, valRad As Double, ByRef ix As Double, ByRef iy As Double, ByRef wx As Double, ByRef wy As Double) As Boolean
    ' intersection of the two (extended) lines seg(i), seg(j)/centreline and the unit bisector of the sector whose
    ' angle is valRad, in sketch coordinates (2026-09-25)
    On Error Resume Next
    Dim a As SldWorks.SketchLine, b As SldWorks.SketchLine
    Set a = seg(i)
    If j = NPTS - 1 Then Set b = axisCL Else Set b = seg(j)
    If a Is Nothing Or b Is Nothing Then Exit Function
    Dim ax0 As Double, ay0 As Double, ax1 As Double, ay1 As Double, bx0 As Double, by0 As Double, bx1 As Double, by1 As Double
    ax0 = a.GetStartPoint2.X: ay0 = a.GetStartPoint2.Y: ax1 = a.GetEndPoint2.X: ay1 = a.GetEndPoint2.Y
    bx0 = b.GetStartPoint2.X: by0 = b.GetStartPoint2.Y: bx1 = b.GetEndPoint2.X: by1 = b.GetEndPoint2.Y
    If Err.Number <> 0 Then Err.Clear: Exit Function
    Dim ux As Double, uy As Double, vx As Double, vy As Double, la As Double, lb As Double, den As Double, t As Double, c As Double, lw As Double
    ux = ax1 - ax0: uy = ay1 - ay0: la = Sqr(ux * ux + uy * uy)
    vx = bx1 - bx0: vy = by1 - by0: lb = Sqr(vx * vx + vy * vy)
    If la < 0.0000001 Or lb < 0.0000001 Then Exit Function
    ux = ux / la: uy = uy / la: vx = vx / lb: vy = vy / lb
    den = ux * vy - uy * vx
    If Abs(den) < 0.000001 Then Exit Function
    t = ((bx0 - ax0) * vy - (by0 - ay0) * vx) / den
    ix = ax0 + t * ux: iy = ay0 + t * uy
    c = ux * vx + uy * vy
    If Abs(ACosSafe(-c) - valRad) < Abs(ACosSafe(c) - valRad) Then vx = -vx: vy = -vy
    wx = ux + vx: wy = uy + vy: lw = Sqr(wx * wx + wy * wy)
    If lw < 0.000001 Then Exit Function
    wx = wx / lw: wy = wy / lw
    AngleBisector = True
End Function

Function ACosSafe(x As Double) As Double
    If x >= 1 Then ACosSafe = 0: Exit Function
    If x <= -1 Then ACosSafe = 3.14159265358979: Exit Function
    ACosSafe = Atn(-x / Sqr(1 - x * x)) + 2 * Atn(1)
End Function"""
