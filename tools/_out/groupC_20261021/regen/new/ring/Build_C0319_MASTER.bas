Attribute VB_Name = "Build_C0319_MASTER"
' ============================================================================
'  Build_C0319_MASTER.bas  -  OMi fitting library, generated 2026-10-21 by gen_ring.py
'  Compression Sleeve (Ferrule), bite type - master from reference configuration C0319-08 (DesignTable_C0319_SW2.xlsx row 2)
'  Axis = X (RING_AXIS); DRIVE = closed half-section P0..P13 (compression sleeve: front face, nose, groove, collar, spigot, tail
'  chamfer, rear face, rear bore, inner step, front bore) + construction line origin -> nose top P1; all dimensions linear;
'  revolved 360 deg. No hex, no threads.
'  Run in SolidWorks: Tools > Macro > Run > BuildC0319.  Report: 03_SCRIPTS\Build_C0319_report.txt
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\04_DESIGN_TABLES\DesignTable_C0319_SW2.xlsx"
Const SAVE_PATH  As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\C0319_MASTER.SLDPRT"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_C0319_report.txt"

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String

Sub BuildC0319()
    ' a missing report / save folder raised run-time error 76 before the error trap and left a modal VBA box (2026-10-14)
    Dim fld As String
    fld = Left(REPORT_PATH, InStrRev(REPORT_PATH, "\"))
    If Dir(fld, vbDirectory) = "" Then MsgBox "Report folder missing: " & fld & " - nothing built.": Exit Sub
    fld = Left(SAVE_PATH, InStrRev(SAVE_PATH, "\"))
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
    Print #fnRep, "Build_C0319_MASTER  " & Now
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

    ' ================= 1. DRIVE sketch: closed half-section P0..P13 + construction line origin -> nose top P1 =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim seg(13) As SldWorks.SketchSegment, cl As SldWorks.SketchSegment, i As Long
    Set seg(0) = swSkMgr.CreateLine(0.000000000, 0.006413500, 0, 0.000000000, 0.006794500, 0)
    Set seg(1) = swSkMgr.CreateLine(0.000000000, 0.006794500, 0, 0.000856234, 0.007512812, 0)
    Set seg(2) = swSkMgr.CreateLine(0.000856234, 0.007512812, 0, 0.001124204, 0.007048500, 0)
    Set seg(3) = swSkMgr.CreateLine(0.001124204, 0.007048500, 0, 0.001727200, 0.007048500, 0)
    Set seg(4) = swSkMgr.CreateLine(0.001727200, 0.007048500, 0, 0.001727200, 0.008243824, 0)
    Set seg(5) = swSkMgr.CreateLine(0.001727200, 0.008243824, 0, 0.001937258, 0.008420100, 0)
    Set seg(6) = swSkMgr.CreateLine(0.001937258, 0.008420100, 0, 0.003581400, 0.008420100, 0)
    Set seg(7) = swSkMgr.CreateLine(0.003581400, 0.008420100, 0, 0.004546600, 0.007454900, 0)
    Set seg(8) = swSkMgr.CreateLine(0.004546600, 0.007454900, 0, 0.010146284, 0.007454900, 0)
    Set seg(9) = swSkMgr.CreateLine(0.010146284, 0.007454900, 0, 0.010896600, 0.007322566, 0)
    Set seg(10) = swSkMgr.CreateLine(0.010896600, 0.007322566, 0, 0.010896600, 0.006616700, 0)
    Set seg(11) = swSkMgr.CreateLine(0.010896600, 0.006616700, 0, 0.006781800, 0.006616700, 0)
    Set seg(12) = swSkMgr.CreateLine(0.006781800, 0.006616700, 0, 0.006023356, 0.006413500, 0)
    Set seg(13) = swSkMgr.CreateLine(0.006023356, 0.006413500, 0, 0.000000000, 0.006413500, 0)
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, 0.006794500, 0)
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
    swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: seg(3).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: seg(4).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: seg(6).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: seg(8).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: seg(10).Select4 False, Nothing: swModel.SketchAddConstraints "sgVERTICAL"
    swModel.ClearSelection2 True: seg(11).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
    swModel.ClearSelection2 True: seg(13).Select4 False, Nothing: swModel.SketchAddConstraints "sgHORIZONTAL"
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
    swModel.ClearSelection2 True: cl.Select4 False, Nothing
    Set dd = swModel.AddDimension2(-0.007620, 0.003397, 0)
    NameDim dd, "NOSER", 0.006794500
    swModel.ClearSelection2 True: seg(13).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.020295, 0.003207, 0)
    NameDim dd, "BORER", 0.006413500
    swModel.ClearSelection2 True: seg(3).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.023343, 0.003524, 0)
    NameDim dd, "GROOVER", 0.007048500
    swModel.ClearSelection2 True: seg(6).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.026391, 0.004210, 0)
    NameDim dd, "COLLARR", 0.008420100
    swModel.ClearSelection2 True: seg(8).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.029439, 0.003727, 0)
    NameDim dd, "SPIGOTR", 0.007454900
    swModel.ClearSelection2 True: seg(11).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.017247, 0.003308, 0)
    NameDim dd, "REARIR", 0.006616700
    Set ln = seg(2): swModel.ClearSelection2 True: ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2(-0.017526, 0.003756, 0)
    NameDim dd, "APEXR", 0.007512812
    Set ln = seg(5): swModel.ClearSelection2 True: ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2(-0.020574, 0.004122, 0)
    NameDim dd, "STEPR", 0.008243824
    Set ln = seg(10): swModel.ClearSelection2 True: ln.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2(-0.011430, 0.003661, 0)
    NameDim dd, "TAILR", 0.007322566
    Set ln = seg(2): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.000428, 0.016802, 0)
    NameDim dd, "APEXX", 0.000856234
    Set ln = seg(3): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.000562, 0.018326, 0)
    NameDim dd, "GROOVEX", 0.001124204
    Set ln = seg(6): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.000969, 0.019850, 0)
    NameDim dd, "CHAMX", 0.001937258
    Set ln = seg(7): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.001791, 0.012230, 0)
    NameDim dd, "COLLARX", 0.003581400
    Set ln = seg(8): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.002273, 0.013754, 0)
    NameDim dd, "SPIGOTX", 0.004546600
    Set ln = seg(9): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.005073, 0.015278, 0)
    NameDim dd, "TAILX", 0.010146284
    Set ln = seg(12): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.003391, 0.016802, 0)
    NameDim dd, "REARIX", 0.006781800
    Set ln = seg(13): swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: ln.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.003012, 0.018326, 0)
    NameDim dd, "BOREX", 0.006023356
    swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: seg(4).Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.000864, 0.022390, 0)
    NameDim dd, "STEPX", 0.001727200
    swModel.ClearSelection2 True: seg(0).Select4 False, Nothing: seg(10).Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.005448, 0.022390, 0)
    NameDim dd, "L", 0.010896600
    swModel.ClearSelection2 True
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
    Check "Sleeve volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (revolved half-section 0.03300)", Abs(vrev - 5.407395240835e-07) < 5.407395240835e-07 * 0.002

    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
    Check "Sleeve length along the axis " & Format(lenX, "0.0000") & " (expect L 0.4290)", Abs(lenX - 0.429) < 0.005
    Check "Sleeve O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect collar 0.6630)", Abs(dY - 0.663000) < 0.005 And Abs(dZ - 0.663000) < 0.005
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
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect 10)", (UBound(cfgs) + 1) >= 9
    ' ---- config spot check: do the table values actually land in the model? (SP3 lesson)
    stepName = "Config check"
    Dim cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature
    cx_c = Array("C0319-04", "C0319-32")
    cx_p = Array("L@DRIVE", "COLLARR@DRIVE", "BORER@DRIVE", "REARIX@DRIVE")
    cx_w = Array(Array(0.36300, 0.18350, 0.12750, 0.25400), Array(0.50900, 1.10500, 1.00700, 0.32200))
    For cx_q = 0 To 1
        Progress "config check " & (cx_q + 1) & ": " & cx_c(cx_q)
        swModel.ShowConfiguration2 cx_c(cx_q)
        swModel.ForceRebuild3 False
        For cx_k = 0 To 3
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
    ' ---- every configuration: length L along the axis and the collar O.D. across
    stepName = "Sleeve size check"
    Dim rb_c() As String, rb_w() As Double, rb_o() As Double, rb_i As Long, rb_b As Variant, rb_x As Double, rb_y As Double, rb_z As Double
    ReDim rb_c(8): ReDim rb_w(8): ReDim rb_o(8)
    rb_c(0) = "C0319-08": rb_w(0) = 0.429000: rb_o(0) = 0.663000
    rb_c(1) = "C0319-04": rb_w(1) = 0.363000: rb_o(1) = 0.367000
    rb_c(2) = "C0319-06": rb_w(2) = 0.393000: rb_o(2) = 0.492000
    rb_c(3) = "C0319-10": rb_w(3) = 0.442000: rb_o(3) = 0.780000
    rb_c(4) = "C0319-12": rb_w(4) = 0.475000: rb_o(4) = 0.925000
    rb_c(5) = "C0319-16": rb_w(5) = 0.475000: rb_o(5) = 1.187000
    rb_c(6) = "C0319-20": rb_w(6) = 0.475000: rb_o(6) = 1.446000
    rb_c(7) = "C0319-24": rb_w(7) = 0.475000: rb_o(7) = 1.694000
    rb_c(8) = "C0319-32": rb_w(8) = 0.509000: rb_o(8) = 2.210000
    For rb_i = 0 To 8
        swModel.ShowConfiguration2 rb_c(rb_i)
        swModel.ForceRebuild3 False
        rb_b = swModel.GetPartBox(True)
        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_
        Check rb_c(rb_i) & ": length " & Format(rb_x, "0.0000") & " (L " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005
    Next rb_i

    swModel.ShowConfiguration2 "C0319-08"
    swModel.ForceRebuild3 False

    ' ---- all-config rebuild sweep (2026-09-23, QA #124): every configuration, every feature must rebuild
    stepName = "All-config rebuild sweep"
    Dim sw_names As Variant, sw_i As Long, sw_f As SldWorks.Feature, sw_bad As Long, sw_n As Long, sw_b As Variant, sw_nb As Long
    sw_names = swModel.GetConfigurationNames
    sw_bad = 0: sw_n = 0
    Dim sw_t0 As Single, sw_tot As Long
    sw_tot = 0
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then sw_tot = sw_tot + 1
    Next sw_i
    Progress "All-config sweep: rebuilding " & sw_tot & " configurations one at a time with the threads live. SolidWorks does not redraw until it is done - one line per configuration follows."
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then
            sw_t0 = Timer
            swModel.ShowConfiguration2 sw_names(sw_i)
            swModel.ForceRebuild3 False
            sw_n = sw_n + 1
            Progress "sweep " & sw_n & "/" & sw_tot & "  " & sw_names(sw_i) & "  rebuilt in " & Format(Timer - sw_t0, "0.0") & " s"
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
    ' 2026-09-25: leave the master in its reference configuration (C0319-08) - SolidWorks opens a part in the configuration that is active when it is saved;
    ' before this the master was left in the first name of the list (the smallest size)
    swModel.ShowConfiguration2 "C0319-08"
    Trace "Master left in its reference configuration C0319-08 for the save (it opens in this size)"
    Trace "No THD_ features in this master (sleeves carry no threads)"

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
    MsgBox "Build_C0319_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
    Exit Sub
Trap:
    Check "RUNTIME ERROR during '" & stepName & "' at line " & Erl & ": " & Err.Number & " - " & Err.Description, False
    Resume Next
End Sub

' ---------------------------------------------------------------- helpers (shared library, SP3-validated on 2403/2405/2502HX)
Sub Trace(what As String)
    Debug.Print "      " & what
    On Error Resume Next
    Print #fnRep, "      " & what
End Sub
Sub Progress(what As String)
    ' progress line: written to the report at once (close + reopen - VBA otherwise writes the file in 512-byte blocks),
    ' shown in the SolidWorks status bar, and Windows gets a chance to repaint (do not click in SolidWorks meanwhile)
    Trace what
    On Error Resume Next
    Close #fnRep
    Open REPORT_PATH For Append As #fnRep
    Dim fr As Object
    Set fr = swApp.Frame
    fr.SetStatusBarText "OMi build: " & what
    DoEvents
End Sub

Sub Check(what As String, passed As Boolean)
    Dim line As String
    line = IIf(passed, "OK    ", "FAIL  ") & what
    report = report & line & vbCrLf
    If passed = False Then nErr = nErr + 1      ' not 'If Not passed': SolidWorks returns True as 1 and Not 1 = -2 (2026-09-25)
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

Function Volume() As Double
    Dim mp As SldWorks.MassProperty
    Set mp = swModel.Extension.CreateMassProperty
    Volume = mp.Volume
End Function

