Attribute VB_Name = "Build_2502HX_MASTER"
' ============================================================================
'  Build_2502HX_MASTER.bas  -  OMi fitting library, generated 2026-09-16
'  2502 90 deg female pipe elbow (JIC 37 male x NPTF female) from DesignTable_2502HX_SW2.xlsx row 2 (2502-08-08).
'  Origin = centre of the NPTF end face.  LEGP revolve about X (boss, x 0..N1), LEGJ revolve about Y at x=N1 (JIC, y 0..M1),
'  CORNER sphere at (N1,0), tap-drill pocket + two bores, THD_EndB Thread feature, THD_EndA NPTF helix sweep (2405 routine),
'  design table, config spot-check, save.
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\04_DESIGN_TABLES\DesignTable_2502HX_SW2.xlsx"
Const SAVE_PATH  As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\2502HX_MASTER.SLDPRT"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_2502HX_report.txt"

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
Dim curAxis As Long          ' 0 = leg along X, 1 = leg along Y
Dim tipPos As Double         ' distance of the current leg's tip face from the origin along its axis (m)
Dim axisOff As Double        ' the leg axis' offset on the other in-plane coordinate (JIC leg: x = N1)
Dim boreCtr As SldWorks.SketchPoint   ' sketch point the next bore circle is centred on (Nothing = origin)
Dim anchorPt As SldWorks.SketchPoint  ' sketch point the next profile's axis start is pinned to (Nothing = origin)
Dim hexAnchor As SldWorks.SketchPoint ' sketch point a hex arm centre is pinned to
Dim NPTS As Long
Dim PX() As Double, PR() As Double

Sub LoadLeg(i As Long)
    Dim v As Variant, k As Long
    If i = 1 Then v = Array( _
    0.000000000, 0.000000000, _
    0.000000000, 0.014351000, _
    0.031242000, 0.014351000, _
    0.031242000, 0.000000000)
    If i = 2 Then v = Array( _
    0.000000000, 0.000000000, _
    0.000000000, 0.010287000, _
    0.022682976, 0.010287000, _
    0.022682976, 0.008369300, _
    0.025070576, 0.008369300, _
    0.025737820, 0.009525000, _
    0.032943800, 0.009525000, _
    0.032943800, 0.008369300, _
    0.035443160, 0.008369300, _
    0.039370000, 0.005410214, _
    0.039370000, 0.000000000)
    NPTS = (UBound(v) + 1) \ 2
    ReDim PX(NPTS - 1): ReDim PR(NPTS - 1)
    For k = 0 To NPTS - 1
        PX(k) = v(2 * k): PR(k) = v(2 * k + 1)
    Next k
End Sub

' draw the closed half-profile PX/PR in the active sketch; swap = True puts the axis along sketch Y at x = offX
Sub DrawProfile(swap As Boolean, offX As Double)
    Dim i As Long
    ReDim seg(NPTS - 1)
    swSkMgr.AddToDB = True
    For i = 0 To NPTS - 2
        If swap Then
            Set seg(i) = swSkMgr.CreateLine(offX + PR(i), PX(i), 0, offX + PR(i + 1), PX(i + 1), 0)
        Else
            Set seg(i) = swSkMgr.CreateLine(PX(i), PR(i), 0, PX(i + 1), PR(i + 1), 0)
        End If
    Next i
    If swap Then
        Set seg(NPTS - 1) = swSkMgr.CreateLine(offX, PX(NPTS - 1), 0, offX, PX(0), 0)
        Set axisCL = swSkMgr.CreateCenterLine(offX, 0, 0, offX, PX(NPTS - 1), 0)
    Else
        Set seg(NPTS - 1) = swSkMgr.CreateLine(PX(NPTS - 1), 0, 0, PX(0), 0, 0)
        Set axisCL = swSkMgr.CreateCenterLine(0, 0, 0, PX(NPTS - 1), 0, 0)
    End If
    swSkMgr.AddToDB = False
    Dim ln1 As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, cl As SldWorks.SketchLine
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
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints IIf(swap, "sgVERTICAL", "sgHORIZONTAL")
        ElseIf Abs(x1 - x2) < 0.000000001 Then
            seg(i).Select4 False, Nothing: swModel.SketchAddConstraints IIf(swap, "sgHORIZONTAL", "sgVERTICAL")
        End If
    Next i
    Set cl = axisCL: Set ln1 = seg(0): Set ln2 = seg(NPTS - 2)
    swModel.ClearSelection2 True
    cl.GetStartPoint2.Select4 False, Nothing: ln1.GetStartPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    cl.GetEndPoint2.Select4 False, Nothing: ln2.GetEndPoint2.Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    ln1.GetStartPoint2.Select4 False, Nothing
    If anchorPt Is Nothing Then
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Else
        anchorPt.Select4 True, Nothing
    End If
    Trace "profile axis start pinned to " & IIf(anchorPt Is Nothing, "origin", "previous leg axis point") & " (" & swSelMgr.GetSelectedObjectCount2(-1) & " selected)"
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
End Sub

Sub Build2502HX()
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
    Print #fnRep, "Build_2502HX_MASTER  " & Now
    On Error GoTo Trap
    Dim swFeat As SldWorks.Feature, rev As SldWorks.Feature, sd As SldWorks.SelectData
    Dim pipeAxisEnd As SldWorks.SketchPoint, jicAxisStart As SldWorks.SketchPoint, jicAxisEnd As SldWorks.SketchPoint

    ' ================= COLLAR: round pipe-end collar, revolve about X, x = 0 .. N1 (inside the hex where they overlap) =================
    stepName = "COLLAR sketch"
    curAxis = 0: tipPos = 0#: axisOff = 0#
    Set anchorPt = Nothing
    LoadLeg 1
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    DrawProfile False, 0#
    Call Dim_len2(-1, 3, "N1", 0.031242000, 0.015621, 0.027051)
    Call Dim_rad(1, "COLLARR", 0.014351000, 0.015621, -0.010160)
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "COLLAR"
    Check "COLLAR sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Set pipeAxisEnd = axisCL.GetEndPoint2
    Set hexAnchor = pipeAxisEnd
    stepName = "COLLAR revolve"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "COLLAR", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    axisCL.Select4 True, sd
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "COLLAR revolve created", Not rev Is Nothing
    If rev Is Nothing Then GoTo Finish
    rev.Name = "COLLAR_BODY"

    ' ================= LEGJ: JIC male, revolve about Y at x = N1, y = 0 .. M1 =================
    stepName = "LEGJ sketch"
    curAxis = 1: tipPos = 0.039370000: axisOff = 0.031242000
    Set anchorPt = pipeAxisEnd
    LoadLeg 2
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    DrawProfile True, 0.031242000
    Call Dim_len2(-1, 10, "M1", 0.039370000, 0.056769, 0.019685)
    Call Dim_rad(1, "BODYR", 0.010287000, 0.021082, 0.011341)
    Call Dim_rad(5, "THDMAJR_B", 0.009525000, 0.023622, 0.029341)
    Call Dim_len(3, "JIC_RELIEFL", 0.002387600, 0.047879, 0.023877)
    Call Dim_ang(4, 5, "RELIEFANG", 1.047197551, 0.044069, 0.022531)
    Call Dim_len(5, "JIC_THDZ", 0.007205980, 0.050419, 0.029341)
    Call Dim_rad(7, "JIC_CONER", 0.008369300, 0.026162, 0.034193)
    Call Dim_len(7, "JIC_LANDL", 0.002499360, 0.045339, 0.034193)
    Call Dim_ptline(8, False, 9, "JIC_SEATL", 0.003926840, 0.052959, 0.037407)
    Call Dim_ang(8, 10, "SEATB", 0.645771823, 0.027432, 0.034173)
    Call Collinear(3, 7)
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0)
    swFeat.Name = "LEGJ"
    Check "LEGJ sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Set jicAxisStart = axisCL.GetStartPoint2: Set jicAxisEnd = axisCL.GetEndPoint2
    stepName = "LEGJ revolve"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "LEGJ", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    axisCL.Select4 True, sd
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "LEGJ revolve created", Not rev Is Nothing
    If rev Is Nothing Then GoTo Finish
    rev.Name = "LEGJ_BODY"

    ' ================= HEXP: pipe hex arm along X, from x = COLLARL to N1 =================
    stepName = "HEXP"
    Call HexArm("Right Plane", 0#, 0.009398000, 0.021844000, 0.014351000, "HEXP", 0)
    ' ================= HEXJ: JIC hex arm along Y at x = N1, from y = 0 to YTOP =================
    stepName = "HEXJ"
    Call HexArm("Top Plane", 0.031242000, 0#, 0.022682200, 0.014351000, "HEXJ", 1)
    ' ================= PUCK: 30 deg double cone about Z at the crossing (the turned hex corner) =================
    stepName = "PUCK"
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim pA As SldWorks.SketchSegment, pB As SldWorks.SketchSegment, pC As SldWorks.SketchSegment, pD As SldWorks.SketchSegment, pE As SldWorks.SketchSegment, pX As SldWorks.SketchSegment
    '  A(N1,-h) B(N1+R1,-h) C(N1+AC,0) D(N1+R1,h) E(N1,h); E->A is the revolve centreline; origin->C construction line carries PUCK_XC
    Set pA = swSkMgr.CreateLine(0.031242000, -0.014351000, 0, 0.039527480, -0.014351000, 0)
    Set pB = swSkMgr.CreateLine(0.039527480, -0.014351000, 0, 0.047812960, 0#, 0)
    Set pC = swSkMgr.CreateLine(0.047812960, 0#, 0, 0.039527480, 0.014351000, 0)
    Set pD = swSkMgr.CreateLine(0.039527480, 0.014351000, 0, 0.031242000, 0.014351000, 0)
    Set pE = swSkMgr.CreateCenterLine(0.031242000, 0.014351000, 0, 0.031242000, -0.014351000, 0)
    Set pX = swSkMgr.CreateLine(0#, 0#, 0, 0.047812960, 0#, 0)
    swSkMgr.AddToDB = False
    pX.ConstructionGeometry = True
    Dim qa As SldWorks.SketchLine, qb As SldWorks.SketchLine, qc As SldWorks.SketchLine, qd As SldWorks.SketchLine, qe As SldWorks.SketchLine, qx As SldWorks.SketchLine
    Set qa = pA: Set qb = pB: Set qc = pC: Set qd = pD: Set qe = pE: Set qx = pX
    swModel.ClearSelection2 True: qa.GetEndPoint2.Select4 False, Nothing: qb.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qb.GetEndPoint2.Select4 False, Nothing: qc.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qc.GetEndPoint2.Select4 False, Nothing: qd.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qd.GetEndPoint2.Select4 False, Nothing: qe.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qe.GetEndPoint2.Select4 False, Nothing: qa.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: qx.GetEndPoint2.Select4 False, Nothing: qb.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: pA.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pD.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pX.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: pE.Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: qx.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Call DimSegOrigin(pE, "PUCK_X", 0.031242000, 0.015621, 0.027051)
    Call DimSegOrigin(pA, "PUCK_HB", 0.014351000, 0.035385, -0.023241)
    Call DimSegOrigin(pD, "PUCK_HT", 0.014351000, 0.035385, 0.023241)
    Call DimSeg1(pA, "PUCK_R1B", 0.008285480, 0.035385, -0.032131)
    Call DimSeg1(pD, "PUCK_R1T", 0.008285480, 0.035385, 0.032131)
    Call DimSeg1(pX, "PUCK_XC", 0.047812960, 0.023906, -0.006350)
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set swFeat = swModel.FeatureByPositionReverse(0): swFeat.Name = "PUCK"
    Check "PUCK sketch fully defined", (swFeat.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 "PUCK", "SKETCH", 0, 0, 0, False, 0, Nothing, 0
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 16
    pE.Select4 True, sd
    Set rev = swFeatMgr.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 6.28318530717959, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    Check "PUCK revolve created", Not rev Is Nothing
    If Not rev Is Nothing Then rev.Name = "PUCK_BODY"
    Dim bodies As Variant
    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bodies) Then Check "One solid body after collar+hex+puck", False Else Check "One solid body after collar+hex+puck", (UBound(bodies) = 0)

    ' ================= Bores =================
    stepName = "Bores"
    curAxis = 0: tipPos = 0#: axisOff = 0#: Set boreCtr = Nothing
    Call BoreCut("BORE_A", "TAPDRILL", 0.017780000, 0.022860000, 0#, "BORECUT_A", False, 0.014351000)
    Call BoreCut("BORE_P", "D", 0.009906000, 0.031242000, 0#, "BORECUT_P", False, 0.014351000)
    curAxis = 1: tipPos = 0.039370000: axisOff = 0.031242000: Set boreCtr = jicAxisEnd
    Call BoreCut("BORE_J", "D", 0.009906000, 0.039370000, 0#, "BORECUT_J", True, 0.005410214)
    Set boreCtr = Nothing

    ' ================= Threads =================
    stepName = "Threads"
    curAxis = 1: tipPos = 0.039370000: axisOff = 0.031242000
    Call ThreadCut(0.025737820, 0.009525000, 0.007205980, "0.7500-16", "THD_EndB", 1#, 0.001587500)
    curAxis = 0: tipPos = 0#: axisOff = 0#
    Call NptfThread(0.017780000, 0.022860000, 0.001813560, 0.001450340, 0.031239648, 0.014351000, "THD_EndA")

    ' ================= Self-checks =================
    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Check "X extent " & Format(bb(0) / IN_, "0.000") & " .. " & Format(bb(3) / IN_, "0.000") & " (expect 0.000 .. 1.882)", Abs(bb(0) / IN_) < 0.005 And Abs(bb(3) / IN_ - 1.8824) < 0.005
    Check "Y extent " & Format(bb(1) / IN_, "0.000") & " .. " & Format(bb(4) / IN_, "0.000") & " (expect -0.652 .. 1.550)", Abs(bb(1) / IN_ - -0.6524) < 0.005 And Abs(bb(4) / IN_ - 1.5500) < 0.005
    Check "Z extent " & Format(bb(2) / IN_, "0.000") & " .. " & Format(bb(5) / IN_, "0.000") & " (expect -0.565 .. 0.565)", Abs(bb(2) / IN_ - -0.5650) < 0.005 And Abs(bb(5) / IN_ - 0.5650) < 0.005
    bodies = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bodies) Then Check "One solid body", False Else Check "One solid body", (UBound(bodies) = 0)

    ' ================= Design table =================
    stepName = "Design table"
    swModel.ClearSelection2 True
    Dim ok As Boolean
    ok = swModel.InsertFamilyTableOpen(TABLE_PATH)
    Check "Design table inserted from " & TABLE_PATH, ok
    swModel.CloseFamilyTable
    swModel.ForceRebuild3 False
    Dim cfgs As Variant
    cfgs = swModel.GetConfigurationNames
    Check "Configurations after table: " & (UBound(cfgs) + 1), (UBound(cfgs) + 1) >= 2
    ' ---- config spot check: do the table values actually land in the model? (SP3 lesson)
    stepName = "Config check"
    Dim cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature
    cx_c = Array("2502-20-20-FG", "2502-24-24")
    cx_p = Array("N1@COLLAR", "HEXAF@HEXP", "COLLARL@HEXP_BODY", "HEXL@HEXP_BODY", "HEXAF@HEXJ", "HEXL@HEXJ_BODY", "PUCK_XC@PUCK", "M1@LEGJ", "BODYR@LEGJ", "TAPDRILL@BORE_A", "DEPTH@BORECUT_A")
    cx_w = Array(Array(1.70000, 1.88000, 0.51000, 1.19000, 1.88000, 1.37200, 2.78540, 2.33000, 0.87500, 1.48000, 1.14000), Array(2.08000, 2.50000, 0.61000, 1.47000, 2.50000, 1.80700, 3.52340, 2.89000, 1.00000, 1.72000, 1.16000))
    For cx_q = 0 To 1
        swModel.ShowConfiguration2 cx_c(cx_q)
        swModel.ForceRebuild3 False
        For cx_k = 0 To 10
            Set cx_prm = swModel.Parameter(cx_p(cx_k))
            If cx_prm Is Nothing Then
                Check cx_c(cx_q) & " " & cx_p(cx_k) & " readable", False
            Else
                Check cx_c(cx_q) & " " & cx_p(cx_k) & " = " & Format(cx_prm.SystemValue / IN_, "0.0000") & " (table " & Format(cx_w(cx_q)(cx_k), "0.0000") & ")", Abs(cx_prm.SystemValue / IN_ - cx_w(cx_q)(cx_k)) < 0.0005
            End If
        Next cx_k
        cx_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
        cx_nb = IIf(IsEmpty(cx_b), 0, UBound(cx_b) + 1)
        Check cx_c(cx_q) & " one solid body (found " & cx_nb & ")", cx_nb = 1
        Set cx_f = swModel.FirstFeature
        Do While Not cx_f Is Nothing
            If cx_f.GetErrorCode2(True) <> 0 And Not cx_f.IsSuppressed Then Check cx_c(cx_q) & " feature " & cx_f.Name & " rebuilds (error code " & cx_f.GetErrorCode2(True) & ")", False
            Set cx_f = cx_f.GetNextFeature
        Loop
        cx_bx = swModel.GetPartBox(True)
        Trace cx_c(cx_q) & " box x " & Format(cx_bx(0) / IN_, "0.000") & ".." & Format(cx_bx(3) / IN_, "0.000") & "  y " & Format(cx_bx(1) / IN_, "0.000") & ".." & Format(cx_bx(4) / IN_, "0.000")
    Next cx_q
    swModel.ShowConfiguration2 "2502-08-08"
    swModel.ForceRebuild3 False

    ' ================= Save (fixed name; timestamped fallback) =================
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
    Check "Threads suppressed in all configurations before save (" & st_n & " THD_ features)", st_n > 0 And st_bad = 0

    stepName = "Save"
    Dim e As Long, w As Long
    ok = swModel.Extension.SaveAs(SAVE_PATH, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
    If Not ok Then
        Dim alt As String: alt = Replace(SAVE_PATH, ".SLDPRT", "_" & Format(Now, "hhnnss") & ".SLDPRT")
        ok = swModel.Extension.SaveAs(alt, swSaveAsVersion_e.swSaveAsCurrentVersion, swSaveAsOptions_e.swSaveAsOptions_Silent, Nothing, e, w)
        Check "Saved to " & alt & " (first name was locked, error " & e & ")", ok
    Else
        Check "Saved to " & SAVE_PATH, ok
    End If
    GoTo Finish
Trap:
    Check "RUNTIME ERROR in step '" & stepName & "': " & Err.Description & " (" & Err.Number & ")", False
    Resume Finish
Finish:
    Close #fnRep
    MsgBox "Build_2502HX_MASTER finished: " & nErr & " problem(s). Report: " & REPORT_PATH
End Sub

' ---------------------------------------------------------------- helpers
Sub Trace(what As String)
    Debug.Print "      " & what
    On Error Resume Next
    Print #fnRep, "      " & what
End Sub

Sub Check(what As String, passed As Boolean)
    Dim line As String
    line = IIf(passed, "OK    ", "FAIL  ") & what
    report = report & line & vbCrLf
    If Not passed Then nErr = nErr + 1
    Debug.Print line
    On Error Resume Next
    Print #fnRep, line
End Sub

Sub NameDim(dd As SldWorks.DisplayDimension, nm As String, valMetres As Double)
    If dd Is Nothing Then Check "dimension " & nm & " was not created", False: Exit Sub
    Dim d As SldWorks.Dimension
    Set d = dd.GetDimension2(0)
    d.Name = nm
    Dim v As Double: v = d.SystemValue
    Check "dim " & nm & " = " & Format(v / IN_, "0.0000") & " in (expect " & Format(valMetres / IN_, "0.0000") & ")", Abs(v - valMetres) < 0.000005
End Sub

Sub NameAng(dd As SldWorks.DisplayDimension, nm As String, valRad As Double)
    If dd Is Nothing Then Check "angle " & nm & " was not created", False: Exit Sub
    Dim d As SldWorks.Dimension
    Set d = dd.GetDimension2(0)
    d.Name = nm
    Dim v As Double: v = d.SystemValue
    Check "angle " & nm & " = " & Format(v * 180 / 3.14159265358979, "0.00") & " deg", Abs(v - valRad) < 0.0005
End Sub

' length of one line: select the line, dimension it
Sub Dim_len(i As Long, nm As String, valM As Double, tx As Double, ty As Double)
    swModel.ClearSelection2 True
    If i = -1 Then      ' overall: between the two end faces (segment 0 and the last profile line)
        seg(0).Select4 False, Nothing
        seg(NPTS - 2).Select4 True, Nothing
    Else
        seg(i).Select4 False, Nothing
    End If
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
End Sub
' horizontal length of a slanted line = distance from one of its endpoints to a vertical line (end face)
Sub Dim_ptline(segPt As Long, useEnd As Boolean, segLine As Long, nm As String, valM As Double, tx As Double, ty As Double)
    Dim lp As SldWorks.SketchLine
    Set lp = seg(segPt)
    swModel.ClearSelection2 True
    If useEnd Then lp.GetEndPoint2.Select4 False, Nothing Else lp.GetStartPoint2.Select4 False, Nothing
    seg(segLine).Select4 True, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
End Sub
' overload signature used by the generator for the overall length (extra arg ignored)
Sub Dim_len2(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    Dim_len i, nm, valM, tx, ty
End Sub

' diameter: select the line and the centerline, place text on the far side of the axis.
' If SolidWorks made a radius dimension instead, delete it and retry further out.
Sub Dim_rad(i As Long, nm As String, valM As Double, tx As Double, ty As Double)
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
End Sub

Sub DeleteDisp(dd As SldWorks.DisplayDimension)
    swModel.ClearSelection2 True
    If dd.GetAnnotation.Select3(False, Nothing) Then
        If swSelMgr.GetSelectedObjectCount2(-1) = 1 Then swModel.Extension.DeleteSelection2 0
    End If
    swModel.ClearSelection2 True
End Sub

' angle between two lines
Sub Dim_ang(i As Long, j As Long, nm As String, valRad As Double, tx As Double, ty As Double)
    ' Placement candidates: the caller's point first (unchanged behaviour), then the four quadrants
    ' around the vertex the two lines share.  Mirroring through the ORIGIN only works when the leg
    ' axis passes through it (2403/2500/2603); on 2502 the JIC leg axis is at x = N1, so the
    ' vertex-relative candidates are what find the 60 deg side.
    Dim dd As SldWorks.DisplayDimension, v As Double, k As Long, nC As Long
    Dim cand(11) As Double, candy(11) As Double
    cand(0) = tx: candy(0) = ty
    cand(1) = tx: candy(1) = -ty
    cand(2) = -tx: candy(2) = ty
    cand(3) = -tx: candy(3) = -ty
    cand(4) = tx + 0.003: candy(4) = 0.002
    cand(5) = tx - 0.003: candy(5) = 0.002
    nC = 5
    Dim px As Double, py As Double, dq As Double
    If SegVertex(i, j, px, py) Then
        dq = 0.0025
        cand(6) = px + dq: candy(6) = py + dq
        cand(7) = px + dq: candy(7) = py - dq
        cand(8) = px - dq: candy(8) = py + dq
        cand(9) = px - dq: candy(9) = py - dq
        cand(10) = px + 3 * dq: candy(10) = py
        cand(11) = px - 3 * dq: candy(11) = py
        nC = 11
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

Sub Collinear(i As Long, j As Long)
    swModel.ClearSelection2 True
    seg(i).Select4 False, Nothing
    seg(j).Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOLINEAR"
    swModel.ClearSelection2 True
End Sub

' Bore: circle on an end face, blind cut. fromEndB = sketch on the End B tip face instead of End A.
' startOff > 0 -> From: Offset (cut starts startOff into the part from the sketch face).
' Direction is found by trial: the cut must REDUCE the volume; otherwise it is flipped.
Sub BoreCut(skName As String, dimName As String, diaM As Double, depthM As Double, startOff As Double, featName As String, fromEndB As Boolean, faceR As Double)
    On Error GoTo BErr
1000 Dim faceX As Double
1010 faceX = IIf(fromEndB, tipPos, 0#)
1020 swModel.ClearSelection2 True
    ' pick the end face by a point on it, near its outer rim (so it still hits after an earlier bore)
1030 Dim ok As Boolean
1040 ok = SelectEndFace(faceX)
1050 Check "select end face for " & skName & " at x=" & Format(faceX / IN_, "0.0000"), ok
1060 Trace "selected object type = " & swSelMgr.GetSelectedObjectType3(1, -1) & " (2 = face), count = " & swSelMgr.GetSelectedObjectCount2(-1)
1070 Trace "ok = " & ok
1080 Trace "about to InsertSketch on the face"
1090 swSkMgr.InsertSketch True
1100 Trace "returned from InsertSketch"
1110 Dim ask As SldWorks.Sketch
1120 Set ask = swSkMgr.ActiveSketch
1130 Trace "ActiveSketch fetched"
1140 If ask Is Nothing Then
1150 Trace "no active sketch - trying ModelDoc2.InsertSketch2"
1160 SelectEndFace faceX
1170 swModel.InsertSketch2 True
1180 Set ask = swSkMgr.ActiveSketch
1190 End If
1200 Check skName & " sketch opened (active sketch exists)", Not ask Is Nothing
1210 Dim c As SldWorks.SketchSegment
1220 Set c = swSkMgr.CreateCircleByRadius(0, 0, 0, diaM / 2)
1230 Check skName & " circle created", Not c Is Nothing
1240 If c Is Nothing Then swSkMgr.InsertSketch True: Exit Sub
1250 swModel.ClearSelection2 True
1260 Dim ca As SldWorks.SketchArc
1270 Set ca = c
1280 ca.GetCenterPoint2.Select4 False, Nothing
1290 If boreCtr Is Nothing Then swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0 Else boreCtr.Select4 True, Nothing
1300 swModel.SketchAddConstraints "sgCOINCIDENT"
1305 Trace skName & " centre pinned to " & IIf(boreCtr Is Nothing, "origin", "leg axis point") & " (" & swSelMgr.GetSelectedObjectCount2(-1) & " selected before constraint)"
1310 swModel.ClearSelection2 True
1320 c.Select4 False, Nothing
1330 Dim dd As SldWorks.DisplayDimension
1340 Set dd = swModel.AddDimension2(diaM, diaM, 0)
1350 NameDim dd, dimName, diaM
1360 swModel.ClearSelection2 True
1370 swSkMgr.InsertSketch True
1380 Dim skF As SldWorks.Feature
1390 Set skF = swModel.FeatureByPositionReverse(0): skF.Name = skName
1400 Check skName & " sketch closed and named (" & skF.GetTypeName2 & ")", skF.GetTypeName2 = "ProfileFeature"

1410 Dim vol0 As Double, vol1 As Double
1420 vol0 = Volume()
1430 Dim cut As SldWorks.Feature
1440 Dim flipDir As Boolean, flipOff As Boolean, attempt As Long
1450 For attempt = 0 To 3
1460 flipDir = (attempt Mod 2 = 1): flipOff = (attempt >= 2)
1470 Set cut = MakeCut(skF, swEndConditions_e.swEndCondBlind, depthM, False, flipDir, startOff, flipOff, featName & " attempt " & attempt)
1480 If Not cut Is Nothing Then
1490 vol1 = Volume()
1500 If vol1 < vol0 - 1E-12 Then Exit For
            ' wrong direction: remove and retry
1510 swModel.ClearSelection2 True
1520 cut.Select2 False, 0
1530 swModel.Extension.DeleteSelection2 0      ' keep the sketch
1540 Set cut = Nothing
1550 End If
1560 If startOff = 0 And attempt = 1 Then Exit For
1570 Next attempt
1580 Check featName & " cut removes material (attempt " & attempt & ")", Not cut Is Nothing
1590 If cut Is Nothing Then Exit Sub
1600 cut.Name = featName
    ' name the feature dimensions: depth -> DEPTH, start offset -> START (identified by value)
1610 Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension
1620 Set d = cut.GetFirstDisplayDimension
1630 Do While Not d Is Nothing
1640 Set dm = d.GetDimension2(0)
1650 If Abs(dm.SystemValue - depthM) < 0.000001 And dm.Name <> "DEPTH" And (startOff = 0 Or Abs(depthM - startOff) > 0.000001 Or dm.Name = "D1") Then
1660 dm.Name = "DEPTH"
1670 ElseIf startOff > 0 And Abs(dm.SystemValue - startOff) < 0.000001 Then
1680 dm.Name = "START"
1690 End If
1700 Set d = cut.GetNextDisplayDimension(d)
1710 Loop
1720 Dim names As String: names = ""
1730 Set d = cut.GetFirstDisplayDimension
1740 Do While Not d Is Nothing
1750 names = names & d.GetDimension2(0).Name & "=" & Format(d.GetDimension2(0).SystemValue / IN_, "0.0000") & " "
1760 Set d = cut.GetNextDisplayDimension(d)
1770 Loop
1780 Check featName & " dims: " & names, InStr(names, "DEPTH=") > 0 And (startOff = 0 Or InStr(names, "START=") > 0)
1790 Exit Sub
BErr:
1800 Check "RUNTIME ERROR in BoreCut(" & skName & ") at line " & Erl & ": " & Err.Number & " - " & Err.Description, False
1810 Resume Next
End Sub

' Create an extruded cut from an (unselected) sketch feature. Tries the definition route first,
' then FeatureCut4 with feature scope off, then FeatureCut4 as recorded macros use it.
Function MakeCut(skF As SldWorks.Feature, endType As Long, depthM As Double, flipSide As Boolean, rev As Boolean, startOff As Double, flipOff As Boolean, tag As String) As SldWorks.Feature
    On Error Resume Next
    Dim f As SldWorks.Feature
    Dim xd As SldWorks.ExtrudeFeatureData2
    Set xd = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmCut)
    If Not xd Is Nothing Then
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        xd.SetEndCondition True, endType
        If endType = swEndConditions_e.swEndCondBlind Then xd.SetDepth True, depthM
        xd.FlipSideToCut = flipSide
        xd.ReverseDirection = rev
        If startOff > 0 Then
            xd.StartCondition = swStartConditions_e.swStartOffset
            xd.StartOffset = startOff
            xd.FlipStartOffset = flipOff
        End If
        Set f = swFeatMgr.CreateFeature(xd)
        Trace tag & ": definition route -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, "  [err " & Err.Number & " " & Err.Description & "]", "")
        Err.Clear
    Else
        Trace tag & ": CreateDefinition returned Nothing"
    End If
    If f Is Nothing Then
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        Set f = swFeatMgr.FeatureCut4(True, flipSide, rev, endType, 0, depthM, 0, False, False, False, False, 0, 0, False, False, False, False, False, False, False, False, False, False, IIf(startOff > 0, swStartConditions_e.swStartOffset, swStartConditions_e.swStartSketchPlane), startOff, flipOff, False)
        Trace tag & ": FeatureCut4 scope off -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, "  [err " & Err.Number & " " & Err.Description & "]", "")
        Err.Clear
    End If
    If f Is Nothing Then
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        Set f = swFeatMgr.FeatureCut4(True, flipSide, rev, endType, 0, depthM, 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, IIf(startOff > 0, swStartConditions_e.swStartOffset, swStartConditions_e.swStartSketchPlane), startOff, flipOff, False)
        Trace tag & ": FeatureCut4 scope on -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, "  [err " & Err.Number & " " & Err.Description & "]", "")
        Err.Clear
    End If
    Set MakeCut = f
End Function

' Two-direction cut (Direction 1 and 2), feature scope off. Used for the hex: ThroughAll both ways,
' falling back to Blind both ways with a generous depth.
Function MakeCut2(skF As SldWorks.Feature, flipSide As Boolean, bigDepth As Double, tag As String) As SldWorks.Feature
    On Error Resume Next
    Dim f As SldWorks.Feature
    swModel.ClearSelection2 True
    skF.Select2 False, 0
    Set f = swFeatMgr.FeatureCut4(False, flipSide, False, swEndConditions_e.swEndCondThroughAll, swEndConditions_e.swEndCondThroughAll, 0, 0, False, False, False, False, 0, 0, False, False, False, False, False, False, False, False, False, False, 0, 0, False, False)
    Trace tag & ": two-dir ThroughAll/ThroughAll -> " & (Not f Is Nothing): Err.Clear
    If f Is Nothing Then
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        Set f = swFeatMgr.FeatureCut4(False, flipSide, False, swEndConditions_e.swEndCondBlind, swEndConditions_e.swEndCondBlind, bigDepth, bigDepth, False, False, False, False, 0, 0, False, False, False, False, False, False, False, False, False, False, 0, 0, False, False)
        Trace tag & ": two-dir Blind/Blind " & Format(bigDepth / IN_, "0.0") & " in -> " & (Not f Is Nothing): Err.Clear
    End If
    If f Is Nothing Then
        swModel.ClearSelection2 True
        skF.Select2 False, 0
        Set f = swFeatMgr.FeatureCut4(True, flipSide, False, swEndConditions_e.swEndCondBlind, 0, bigDepth, 0, False, False, False, False, 0, 0, False, False, False, False, False, False, False, False, False, False, 0, 0, False, False)
        Trace tag & ": one-dir Blind " & Format(bigDepth / IN_, "0.0") & " in -> " & (Not f Is Nothing): Err.Clear
        If f Is Nothing Then
            swModel.ClearSelection2 True
            skF.Select2 False, 0
            Set f = swFeatMgr.FeatureCut4(True, flipSide, True, swEndConditions_e.swEndCondBlind, 0, bigDepth, 0, False, False, False, False, 0, 0, False, False, False, False, False, False, False, False, False, False, 0, 0, False, False)
            Trace tag & ": one-dir Blind reversed -> " & (Not f Is Nothing): Err.Clear
        End If
    End If
    Set MakeCut2 = f
End Function

' Thread feature via IThreadFeatureData (feature id swFmSweepThread). Late-bound property sets are
' traced so any name this version rejects is reported. Feature is suppressed on success.
Sub ThreadCut(ex As Double, er As Double, depthM As Double, sizeStr As String, nm As String, wantDir As Double, pitchM As Double)
    On Error Resume Next
    Dim td As Object, f As SldWorks.Feature, ok As Boolean, edg As Object
    Set td = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmSweepThread)
    Trace nm & ": CreateDefinition(swFmSweepThread) -> " & (Not td Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    If td Is Nothing Then Check nm & " thread definition not available", False: Exit Sub
    ok = SelectCircEdge(ex, er, 0)
    Check nm & ": anchor edge found at x=" & Format(ex / IN_, "0.0000") & " r=" & Format(er / IN_, "0.0000"), ok
    If Not ok Then Exit Sub
    Set edg = swSelMgr.GetSelectedObject6(1, -1)
    Set td.Edge = edg: Trace nm & ": Edge " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.Type = "Inch Die": Trace nm & ": Type=Inch Die " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.Size = sizeStr: Trace nm & ": Size=" & sizeStr & " " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.ThreadMethod = swThreadMethod_e.swThreadMethod_Cut: Trace nm & ": ThreadMethod=Cut " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.EndCondition = swThreadEndCondition_e.swThreadEndCondition_Blind: Trace nm & ": EndCondition=Blind " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.BlindDepth = depthM: Trace nm & ": BlindDepth=" & Format(depthM / IN_, "0.0000") & " " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.RightHanded = True: Err.Clear
    td.DiameterOverride = True: Trace nm & ": DiameterOverride " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.Diameter = 2 * er: Trace nm & ": Diameter " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.PitchOverride = True: Trace nm & ": PitchOverride " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    td.Pitch = pitchM: Trace nm & ": Pitch " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    Trace nm & ": readback Type=" & td.Type & " Size=" & td.Size & " Dia=" & Format(td.Diameter / IN_, "0.0000") & " Pitch=" & Format(td.Pitch / IN_, "0.0000"): Err.Clear
    SelectCircEdge ex, er, 0
    Set f = swFeatMgr.CreateFeature(td)
    Trace nm & ": CreateFeature -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    If f Is Nothing Then
        ' retry with the thread running the other way along the edge
        td.ReverseDirection = True: Err.Clear
        SelectCircEdge ex, er, 0
        Set f = swFeatMgr.CreateFeature(td)
        Trace nm & ": CreateFeature (reversed) -> " & (Not f Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    End If
    Check nm & " thread feature created", Not f Is Nothing
    If f Is Nothing Then Exit Sub
    f.Name = nm
    ' which way did it run? centre of the thread faces relative to the anchor edge
    Dim cx As Double: cx = FeatCentreX(f)
    Trace nm & ": thread centre x = " & Format(cx / IN_, "0.0000") & " in, anchor " & Format(ex / IN_, "0.0000") & ", wanted " & IIf(wantDir > 0, "+X", "-X")
    If (cx - ex) * wantDir < 0 Then
        Dim tdf As Object
        Set tdf = f.GetDefinition
        tdf.AccessSelections swModel, Nothing
        tdf.ReverseDirection = Not tdf.ReverseDirection
        ok = f.ModifyDefinition(tdf, swModel, Nothing)
        Trace nm & ": direction flipped -> " & ok & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
        cx = FeatCentreX(f)
        Trace nm & ": thread centre x now " & Format(cx / IN_, "0.0000") & " in"
    End If
    Check nm & " runs along the thread flat (away from the hex)", (cx - ex) * wantDir > 0
    Check nm & " rebuilds without error (code " & f.GetErrorCode2(True) & ")", f.GetErrorCode2(True) = 0
    ' name the thread dims by value: depth -> DEPTH, diameter -> THDDIA, pitch -> THDPITCH
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = f.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - depthM) < 0.000001 Then dm.Name = "DEPTH"
        If Abs(dm.SystemValue - 2 * er) < 0.000001 Then dm.Name = "THDDIA"
        If Abs(dm.SystemValue - pitchM) < 0.000001 Then dm.Name = "THDPITCH"
        names = names & dm.Name & "=" & Format(dm.SystemValue / IN_, "0.0000") & " "
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check nm & " dims: " & names, InStr(names, "DEPTH=") > 0 And InStr(names, "THDDIA=") > 0 And InStr(names, "THDPITCH=") > 0
    ' 2026-09-23 fix (QA #124): the Thread feature keeps its tooth in a sub-sketch "Thread ProfileN" whose dims stay at the
    ' 16-tpi size when the pitch is overridden -> overlapping turns on 20/24-tpi configs. Rename it so the table can drive them.
    Dim sf As SldWorks.Feature: Set sf = f.GetFirstSubFeature
    Do While Not sf Is Nothing
        If Left(sf.Name, 14) = "Thread Profile" Then sf.Name = nm & "_PROF": Trace nm & ": profile sketch " & IIf(Err.Number <> 0, "rename FAILED " & Err.Description, "renamed to " & sf.Name): Err.Clear
        Set sf = sf.GetNextSubFeature
    Loop
    Check nm & " profile dims reachable as Profile_Height@" & nm & "_PROF", Not swModel.Parameter("Profile_Height@" & nm & "_PROF") Is Nothing
    ' 2026-09-24: the profile sketch's pitch dimension is only renamed THDPITCH (by value, above) when the library
    ' profile of the reference size has the same pitch; for other sizes (e.g. 0.5625-18) it stays "Pitch" and the
    ' THDPITCH@..._PROF table column drives nothing. Rename it explicitly.
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
    Check nm & " profile pitch reachable as THDPITCH@" & nm & "_PROF", Not swModel.Parameter("THDPITCH@" & nm & "_PROF") Is Nothing
    Err.Clear
    Dim sup As Boolean
    ' 2026-09-24: left LIVE here so the design-table checks and the all-config sweep exercise the thread;
    ' the final "Suppress threads for save" step puts every THD_ feature to rest before the save.
    Trace nm & ": left live until the final suppress step"
End Sub

' ---- female NPTF thread: helix sketch (HELIXDIA@HELIXSK_A) -> tapered helix (HEIGHT/PITCH@HELIX_A)
'      -> equilateral V profile (THDH@THDPROF_A, pierced to the helix start) -> swept cut THD_EndA (suppressed)


' Select the circular edge whose centre is at x = ex (on the axis) with radius er. View-independent.
Function SelectCircEdge(ex As Double, er As Double, mark As Long) As Boolean
    On Error Resume Next
    Dim bods As Variant, bd As SldWorks.Body2, edges As Variant, i As Long, e As SldWorks.Edge, cv As SldWorks.Curve, cp As Variant
    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bods) Then Exit Function
    Set bd = bods(0)
    edges = bd.GetEdges
    For i = LBound(edges) To UBound(edges)
        Set e = edges(i)
        Set cv = e.GetCurve
        If cv.IsCircle Then
            cp = cv.CircleParams      ' cx,cy,cz, ax,ay,az, radius
            If Abs(cp(curAxis) - ex) < 0.00002 And Abs(cp(1 - curAxis) - axisOff) < 0.00002 And Abs(cp(2)) < 0.00002 And Abs(cp(6) - er) < 0.00002 Then
                Dim sd As SldWorks.SelectData
                Set sd = swSelMgr.CreateSelectData: sd.Mark = mark
                swModel.ClearSelection2 True
                SelectCircEdge = e.Select4(False, sd)
                Exit Function
            End If
        End If
    Next i
End Function

' Select the planar face perpendicular to the axis at x = fx. View-independent.
Function SelectEndFace(fx As Double) As Boolean
    On Error Resume Next
    Dim bods As Variant, bd As SldWorks.Body2, faces As Variant, i As Long, fc As SldWorks.Face2, sf As SldWorks.Surface, pp As Variant
    bods = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
    If IsEmpty(bods) Then Exit Function
    Set bd = bods(0)
    faces = bd.GetFaces
    For i = LBound(faces) To UBound(faces)
        Set fc = faces(i)
        Set sf = fc.GetSurface
        If sf.IsPlane Then
            pp = sf.PlaneParams       ' nx,ny,nz, rx,ry,rz
            If Abs(Abs(pp(curAxis)) - 1) < 0.0001 And Abs(pp(3 + curAxis) - fx) < 0.00002 Then
                swModel.ClearSelection2 True
                SelectEndFace = fc.Select4(False, Nothing)
                Exit Function
            End If
        End If
    Next i
End Function

Function FeatCentreX(f As SldWorks.Feature) As Double
    On Error Resume Next
    Dim faces As Variant, i As Long, bx As Variant, lo As Double, hi As Double, n As Long
    faces = f.GetFaces
    lo = 1E+30: hi = -1E+30
    If Not IsEmpty(faces) Then
        For i = LBound(faces) To UBound(faces)
            bx = faces(i).GetBox
            If bx(curAxis) < lo Then lo = bx(curAxis)
            If bx(3 + curAxis) > hi Then hi = bx(3 + curAxis)
            n = n + 1
        Next i
    End If
    If n = 0 Then FeatCentreX = 0 Else FeatCentreX = (lo + hi) / 2
End Function

Function Volume() As Double
    Dim mp As SldWorks.MassProperty
    Set mp = swModel.Extension.CreateMassProperty
    Volume = mp.Volume
End Function

Sub DimSeg1(s1 As SldWorks.SketchSegment, nm As String, valM As Double, tx As Double, ty As Double)
    ' one entity: a line's length, or an arc's radius (SP3 hands back a diameter for some arcs - flip it)
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double
    For k = 0 To 3
        swModel.ClearSelection2 True
        s1.Select4 False, Nothing
        Set dd = swModel.AddDimension2(tx * IIf(k >= 2, -1#, 1#), ty * IIf(k Mod 2 = 1, -1#, 1#), 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - 2 * valM) < 0.000005 Then
            Err.Clear
            dd.Diametric = False
            v = dd.GetDimension2(0).SystemValue
            Trace nm & ": diameter dim flipped to radius -> " & Format(v / IN_, "0.0000")
        End If
        If Abs(v - valM) < 0.000005 Then Exit For
        Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"
        DeleteDisp dd: Set dd = Nothing
    Next k
    NameDim dd, nm, valM
End Sub

Sub DimSegOrigin(s1 As SldWorks.SketchSegment, nm As String, valM As Double, tx As Double, ty As Double)
    ' perpendicular distance from a line to the sketch origin
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double
    For k = 0 To 3
        swModel.ClearSelection2 True
        s1.Select4 False, Nothing
        swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        Set dd = swModel.AddDimension2(tx * IIf(k >= 2, -1#, 1#), ty * IIf(k Mod 2 = 1, -1#, 1#), 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - valM) < 0.000005 Then Exit For
        Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"
        DeleteDisp dd: Set dd = Nothing
    Next k
    NameDim dd, nm, valM
End Sub

Sub DimSegSeg(s1 As SldWorks.SketchSegment, s2 As SldWorks.SketchSegment, nm As String, valM As Double, tx As Double, ty As Double)
    ' distance between two parallel lines
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double
    For k = 0 To 3
        swModel.ClearSelection2 True
        s1.Select4 False, Nothing
        s2.Select4 True, Nothing
        Set dd = swModel.AddDimension2(tx * IIf(k >= 2, -1#, 1#), ty * IIf(k Mod 2 = 1, -1#, 1#), 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - valM) < 0.000005 Then Exit For
        Trace nm & " try " & k & ": " & Format(v / IN_, "0.0000") & " (want " & Format(valM / IN_, "0.0000") & ")"
        DeleteDisp dd: Set dd = Nothing
    Next k
    NameDim dd, nm, valM
End Sub

' hex prism, across flats 2*hIn, sketched on plane pl centred at cx along the sketch X axis, extruded
' from offset off0 by depth dep along the plane normal.  ax = 0: arm along X (Right Plane), 1: along Y (Top Plane).
' The flats must end up normal to Z; checked by the part's Z extent, rebuilt with the other relation if not.
Sub HexArm(pl As String, cx As Double, off0 As Double, dep As Double, hIn As Double, nm As String, ax As Long)
    Dim tryRel As Long, relName As String, ok As Boolean
    For tryRel = 0 To 1
        relName = IIf(tryRel = 0, "sgHORIZONTAL", "sgVERTICAL")
        swModel.ClearSelection2 True
        swModel.Extension.SelectByID2 pl, "PLANE", 0, 0, 0, False, 0, Nothing, 0
        swSkMgr.InsertSketch True
        Dim poly As Variant, k As Long, circ As SldWorks.SketchSegment
        poly = swSkMgr.CreatePolygon(cx, 0, 0, cx + hIn, 0, 0, 6, True)      ' inscribed circle = across flats
        For k = LBound(poly) To UBound(poly)
            If poly(k).GetType = swSketchSegments_e.swSketchARC Then Set circ = poly(k)
        Next k
        swModel.ClearSelection2 True
        circ.Select4 False, Nothing
        Dim dd As SldWorks.DisplayDimension
        Set dd = swModel.AddDimension2(cx + hIn * 1.4, hIn * 1.4, 0)
        If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = 2 * hIn
        NameDim dd, "HEXAF", 2 * hIn
        swModel.ClearSelection2 True
        For k = LBound(poly) To UBound(poly)
            If poly(k).GetType = swSketchSegments_e.swSketchLINE Then poly(k).Select4 False, Nothing: swModel.SketchAddConstraints relName: Exit For
        Next k
        Dim arc As SldWorks.SketchArc: Set arc = circ
        swModel.ClearSelection2 True
        arc.GetCenterPoint2.Select4 False, Nothing
        If cx = 0 Then
            swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
        Else
            hexAnchor.Select4 True, Nothing
        End If
        swModel.SketchAddConstraints "sgCOINCIDENT"
        swModel.ClearSelection2 True
        swSkMgr.InsertSketch True
        Dim skF As SldWorks.Feature
        Set skF = swModel.FeatureByPositionReverse(0): skF.Name = nm
        Check nm & " hex sketch fully defined", (skF.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
        Dim ext As SldWorks.Feature, flp As Long, bb As Variant, grew As Boolean
        For flp = 0 To 1
            swModel.ClearSelection2 True
            swModel.Extension.SelectByID2 nm, "SKETCH", 0, 0, 0, False, 0, Nothing, 0
            On Error Resume Next
            Set ext = swFeatMgr.FeatureExtrusion3(True, (flp = 1), False, swEndConditions_e.swEndCondBlind, 0, dep, 0, False, False, False, False, 0, 0, False, False, False, False, True, False, False, IIf(off0 > 0, 3, 0), off0, False)
            Trace nm & ": FeatureExtrusion3 flip=" & flp & " -> " & (Not ext Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
            On Error GoTo 0
            If ext Is Nothing Then Exit For
            bb = swModel.GetPartBox(True)
            If ax = 0 Then grew = (bb(0) > -0.0002) Else grew = (bb(4) > dep - 0.0002)
            Trace nm & ": box x " & Format(bb(0) / IN_, "0.000") & ".." & Format(bb(3) / IN_, "0.000") & "  y " & Format(bb(1) / IN_, "0.000") & ".." & Format(bb(4) / IN_, "0.000") & "  z " & Format(bb(2) / IN_, "0.000") & ".." & Format(bb(5) / IN_, "0.000")
            If grew Then Exit For
            swModel.ClearSelection2 True
            ext.Select2 False, 0
            swModel.Extension.DeleteSelection2 0        ' wrong way: remove the extrude (sketch stays) and flip
            Set ext = Nothing
        Next flp
        Check nm & " extruded the right way", grew
        If ext Is Nothing Then Exit Sub
        ext.Name = nm & "_BODY"
        bb = swModel.GetPartBox(True)
        ok = (Abs(bb(5) - hIn) < 0.0003)
        Trace nm & ": z extent " & Format(bb(5) / IN_, "0.0000") & " (flats want " & Format(hIn / IN_, "0.0000") & ")"
        If ok Then
            Dim d2 As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
            names = ""
            Set d2 = ext.GetFirstDisplayDimension
            Do While Not d2 Is Nothing
                Set dm = d2.GetDimension2(0)
                If Left(dm.Name, 1) = "D" And IsNumeric(Mid(dm.Name, 2)) Then
                    If Abs(dm.SystemValue - dep) < 0.000001 Then dm.Name = "HEXL"
                    If off0 > 0 And Abs(dm.SystemValue - off0) < 0.000001 Then dm.Name = "COLLARL"
                End If
                names = names & dm.Name & " "
                Set d2 = ext.GetNextDisplayDimension(d2)
            Loop
            Check nm & " dims named (" & names & ")", InStr(names, "HEXL") > 0
            Exit Sub
        End If
        Trace nm & ": flats not normal to Z with " & relName & " - rebuilding with the other relation"
        swModel.ClearSelection2 True
        ext.Select2 False, 0
        swModel.Extension.DeleteSelection2 swDeleteSelectionOptions_e.swDelete_Absorbed
    Next tryRel
    Check nm & " hex flats normal to Z", ok
End Sub


Sub NptfThread(diaM As Double, heightM As Double, pitchM As Double, thdhM As Double, taperRad As Double, faceR As Double, nm As String)
    On Error Resume Next
    Dim ok As Boolean, f As SldWorks.Feature, sk As SldWorks.Feature, hx As SldWorks.Feature
    ' --- helix sketch on the End A face
    ok = SelectEndFace(0#)
    Trace nm & ": End A face selected -> " & ok
    swSkMgr.InsertSketch True
    Dim c As SldWorks.SketchSegment, ca As SldWorks.SketchArc
    Set c = swSkMgr.CreateCircleByRadius(0, 0, 0, diaM / 2)
    Set ca = c
    swModel.ClearSelection2 True
    ca.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    c.Select4 False, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(diaM, diaM, 0)
    NameDim dd, "HELIXDIA", diaM
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set sk = swModel.FeatureByPositionReverse(0): sk.Name = "HELIXSK_A"
    Check nm & " helix sketch made (" & sk.GetTypeName2 & ")", sk.GetTypeName2 = "ProfileFeature"
    ' --- helix feature via ModelDoc2.InsertHelix (no CreateDefinition id exists for helices)
    swModel.ClearSelection2 True
    sk.Select2 False, 0
    Dim mdLate As Object: Set mdLate = swModel
    ' Sub InsertHelix(Reversed, Clockwised, Tapered, Outward, Helixdef, Height, Pitch, Revolution, TaperAngle, Startangle)
    mdLate.InsertHelix True, True, True, False, swHelixDefinedBy_e.swHelixDefinedByHeightAndPitch, heightM, pitchM, 0#, taperRad, 0#
    Trace nm & ": InsertHelix called " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    Set hx = swModel.FeatureByPositionReverse(0)
    Trace nm & ": last feature = " & hx.Name & " (" & hx.GetTypeName2 & ")"
    If hx.GetTypeName2 <> "Helix" Then Set hx = Nothing
    Check nm & " helix created", Not hx Is Nothing
    If hx Is Nothing Then Exit Sub
    hx.Name = "HELIX_A"
    ' name the helix dims by value
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = hx.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - heightM) < 0.000001 Then dm.Name = "HEIGHT"
        If Abs(dm.SystemValue - pitchM) < 0.000001 Then dm.Name = "PITCH"
        names = names & dm.Name & "=" & Format(dm.SystemValue, "0.00000") & " "
        Set d = hx.GetNextDisplayDimension(d)
    Loop
    Check nm & " helix dims: " & names, InStr(names, "HEIGHT=") > 0 And InStr(names, "PITCH=") > 0
    ' --- where does the helix start? (a) reference curve, (b) fallback: circle radius along the sketch X axis
    Dim rcv As Object, cv As Object, ep As Variant, p0 As Variant
    Dim sx As Double, sy As Double, sz As Double, useFront As Boolean, radial As Double, gotStart As Boolean
    Set rcv = hx.GetSpecificFeature2
    Set cv = rcv.GetCurve
    Trace nm & ": ReferenceCurve.GetCurve -> " & (Not cv Is Nothing) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", ""): Err.Clear
    If Not cv Is Nothing Then
        ep = cv.GetEndParams
        p0 = cv.Evaluate2(ep(0), 0)
        If Err.Number = 0 Then sx = p0(0): sy = p0(1): sz = p0(2): gotStart = True
        Err.Clear
        If gotStart Then
            ' helix runs into the part (+X); the end at x~0 is the start we want
            Dim p1 As Variant: p1 = cv.Evaluate2(ep(1), 0)
            If Abs(p1(0)) < Abs(sx) Then sx = p1(0): sy = p1(1): sz = p1(2)
        End If
    End If
    If Not gotStart Then
        Dim skc As SldWorks.Sketch, xf As SldWorks.MathTransform, ad As Variant
        Set skc = sk.GetSpecificFeature2
        Set xf = skc.ModelToSketchTransform
        Set xf = xf.Inverse
        ad = xf.ArrayData          ' rows 0..2 = rotation, sketch X axis in model coords = (ad(0), ad(1), ad(2))
        sx = 0: sy = ad(1) * diaM / 2: sz = ad(2) * diaM / 2
        gotStart = (Err.Number = 0): Err.Clear
        Trace nm & ": start from sketch transform"
    End If
    Trace nm & ": helix start = (" & Format(sx / IN_, "0.0000") & ", " & Format(sy / IN_, "0.0000") & ", " & Format(sz / IN_, "0.0000") & ") in"
    useFront = (Abs(sz) < 0.00001)
    radial = IIf(useFront, sy, sz)
    Check nm & " helix starts on the End A face at the pocket radius", Abs(sx) < 0.00005 And Abs(Abs(radial) - diaM / 2) < 0.00005
    If Not (Abs(sx) < 0.00005 And Abs(Abs(radial) - diaM / 2) < 0.00005) Then Exit Sub
    ' --- V profile on the plane through the start point, located by dimensions (no pierce)
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 IIf(useFront, "Front Plane", "Top Plane"), "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    ' exact sketch coords of the helix start via the sketch transform
    Dim mu As SldWorks.MathUtility, mp As SldWorks.MathPoint, xf2 As SldWorks.MathTransform, pd As Variant
    Set mu = swApp.GetMathUtility
    Dim arr(2) As Double: arr(0) = sx: arr(1) = sy: arr(2) = sz
    Set mp = mu.CreatePoint(arr)
    Set xf2 = swSkMgr.ActiveSketch.ModelToSketchTransform
    Set mp = mp.MultiplyTransform(xf2)
    pd = mp.ArrayData
    Dim u0 As Double, v0 As Double, sv As Double, half As Double
    u0 = pd(0): v0 = pd(1): sv = IIf(v0 >= 0, 1#, -1#)
    half = thdhM * Tan(3.14159265358979 / 6)
    Trace nm & ": profile centre in sketch coords = (" & Format(u0 / IN_, "0.0000") & ", " & Format(v0 / IN_, "0.0000") & ")"
    swSkMgr.AddToDB = True
    Dim l1 As SldWorks.SketchSegment, l1b As SldWorks.SketchSegment, l2 As SldWorks.SketchSegment, l3 As SldWorks.SketchSegment, lc As SldWorks.SketchSegment
    Set l1 = swSkMgr.CreateLine(u0 - half, v0, 0, u0, v0, 0)
    Set l1b = swSkMgr.CreateLine(u0, v0, 0, u0 + half, v0, 0)
    Set l2 = swSkMgr.CreateLine(u0 + half, v0, 0, u0, v0 + sv * thdhM, 0)
    Set l3 = swSkMgr.CreateLine(u0, v0 + sv * thdhM, 0, u0 - half, v0, 0)
    Set lc = swSkMgr.CreateLine(u0, v0, 0, u0, v0 + sv * thdhM, 0)
    swSkMgr.AddToDB = False
    lc.ConstructionGeometry = True
    Dim ln1 As SldWorks.SketchLine, ln1b As SldWorks.SketchLine, ln2 As SldWorks.SketchLine, ln3 As SldWorks.SketchLine, lnc As SldWorks.SketchLine
    Set ln1 = l1: Set ln1b = l1b: Set ln2 = l2: Set ln3 = l3: Set lnc = lc
    swModel.ClearSelection2 True: ln1.GetEndPoint2.Select4 False, Nothing: ln1b.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: ln1b.GetEndPoint2.Select4 False, Nothing: ln2.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: ln2.GetEndPoint2.Select4 False, Nothing: ln3.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: ln3.GetEndPoint2.Select4 False, Nothing: ln1.GetStartPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: lnc.GetStartPoint2.Select4 False, Nothing: ln1.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: lnc.GetEndPoint2.Select4 False, Nothing: ln2.GetEndPoint2.Select4 True, Nothing: swModel.SketchAddConstraints "sgMERGEPOINTS"
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: l1b.Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: lc.Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: l1b.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    swModel.ClearSelection2 True: l2.Select4 False, Nothing: l3.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    ' centre point on the End A face (x = 0): coincident with the Right Plane
    swModel.ClearSelection2 True: ln1.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Right Plane", "PLANE", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    Trace nm & ": P on Right Plane " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    Trace nm & ": profile relations " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    ' radial position = pocket radius, table-driven (PROF_R)
    swModel.ClearSelection2 True: ln1.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(u0 - 6 * half, v0 / 2, 0)
    NameDim dd, "PROF_R", Abs(v0)
    ' 60 deg between the sloped sides (retry placement until the value is 60, not 120)
    Dim kk As Long, v As Double
    For kk = 0 To 3
        swModel.ClearSelection2 True
        l2.Select4 False, Nothing: l3.Select4 True, Nothing
        Set dd = swModel.AddDimension2(u0, v0 + sv * thdhM * (1.6 - kk * 0.8), 0)
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - 3.14159265358979 / 3) < 0.001 Then Exit For
        DeleteDisp dd: Set dd = Nothing
    Next kk
    Trace nm & ": 60 deg dim " & IIf(dd Is Nothing, "MISSING", Format(v * 180 / 3.14159265358979, "0.0"))
    ' apex radial position from the origin (unambiguous side): APEXR = PROF_R + THDH
    swModel.ClearSelection2 True
    ln2.GetEndPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(u0 + 6 * half, (v0 + sv * thdhM) / 2, 0)
    NameDim dd, "APEXR", Abs(v0) + thdhM
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim pf As SldWorks.Feature
    Set pf = swModel.FeatureByPositionReverse(0): pf.Name = "THDPROF_A"
    Check nm & " profile sketch fully defined", (pf.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    Trace nm & ": segment status (3=fully) base-left " & l1.ConstrainedStatus & ", base-right " & l1b.ConstrainedStatus & ", side2 " & l2.ConstrainedStatus & ", side3 " & l3.ConstrainedStatus
    Trace nm & ": pierce point status " & ln1.GetEndPoint2.ConstrainedStatus & ", apex " & ln2.GetEndPoint2.ConstrainedStatus & ", left " & ln1.GetStartPoint2.ConstrainedStatus & ", right " & ln1b.GetEndPoint2.ConstrainedStatus
    ' --- swept cut: profile mark 1, path mark 4
    Dim vol0 As Double: vol0 = Volume()
    Dim sd As SldWorks.SelectData
    swModel.ClearSelection2 True
    Set sd = swSelMgr.CreateSelectData: sd.Mark = 1: pf.Select2 False, 1
    hx.Select2 True, 4
    Dim swd As Object
    Set swd = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmSweepCut)
    Trace nm & ": CreateDefinition(swFmSweepCut) -> " & (Not swd Is Nothing): Err.Clear
    If Not swd Is Nothing Then
        Set swd.Profile = pf: Trace nm & ": swd.Profile " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
        Set swd.Path = hx: Trace nm & ": swd.Path " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
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
    Dim sup As Boolean
    ' 2026-09-24: left LIVE here so the design-table checks and the all-config sweep exercise the thread;
    ' the final "Suppress threads for save" step puts every THD_ feature to rest before the save.
    Trace nm & ": left live until the final suppress step"
End Sub

Function SuppressEverywhere(ft As SldWorks.Feature) As Long
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
