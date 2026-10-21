Attribute VB_Name = "Build_4000_MASTER"
' ============================================================================
'  Build_4000_MASTER.bas  -  OMi fitting library, generated 2026-10-20 by gen_ring.py
'  O-Ring (SAE J1926 stud-end O-rings, Buna-N 4000 + Viton 4001; SAE J1453 face-seal O-rings FS4000) - master from reference configuration 4000-08 (DesignTable_4000_SW2.xlsx row 2)
'  Ring axis = X (RING_AXIS); DRIVE = cross-section circle CSDIA at RINGR from the axis; revolved 360 deg. No hex, no threads.
'  Run in SolidWorks: Tools > Macro > Run > Build4000.  Report: 03_SCRIPTS\Build_4000_report.txt
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\04_DESIGN_TABLES\DesignTable_4000_SW2.xlsx"
Const SAVE_PATH  As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\4000_MASTER.SLDPRT"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_4000_report.txt"

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String

Sub Build4000()
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
    Print #fnRep, "Build_4000_MASTER  " & Now
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

    ' ================= 1. DRIVE sketch: construction line origin -> section centre (RINGR) + section circle (CSDIA) =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim cl As SldWorks.SketchSegment, circ As SldWorks.SketchSegment
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, 0.009283700, 0)
    cl.ConstructionGeometry = True
    Set circ = swSkMgr.CreateCircleByRadius(0, 0.009283700, 0, 0.001104900)
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
    Set dd = swModel.AddDimension2(-0.007455, 0.004642, 0)
    NameDim dd, "RINGR", 0.009283700
    swModel.ClearSelection2 True
    circ.Select4 False, Nothing
    Set dd = swModel.AddDimension2(0.008725, 0.015469, 0)
    NameDim dd, "CSDIA", 0.002209800
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
    Check "Ring volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (torus 2 pi^2 R r^2 = 0.01365)", Abs(vrev - 2.237158663216e-07) < 2.237158663216e-07 * 0.002

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
    Check "volume unchanged by the split lines", Abs(Volume() - vrev) < 2.237158663216e-07 * 0.000001

    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
    Check "Ring thickness along the axis " & Format(lenX, "0.0000") & " (expect W 0.0870)", Abs(lenX - 0.087) < 0.005
    Check "Ring O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect 0.8180 = I.D. 0.6440 + 2 W)", Abs(dY - 0.818000) < 0.005 And Abs(dZ - 0.818000) < 0.005
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
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect 30)", (UBound(cfgs) + 1) >= 29
    ' ---- config spot check: do the table values actually land in the model? (SP3 lesson)
    stepName = "Config check"
    Dim cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature
    cx_c = Array("4000-02", "4001-32")
    cx_p = Array("RINGR@DRIVE", "CSDIA@DRIVE")
    cx_w = Array(Array(0.15150, 0.06400), Array(1.22750, 0.11800))
    For cx_q = 0 To 1
        Progress "config check " & (cx_q + 1) & ": " & cx_c(cx_q)
        swModel.ShowConfiguration2 cx_c(cx_q)
        swModel.ForceRebuild3 False
        For cx_k = 0 To 1
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
    ' ---- every configuration: the ring is W thick along its axis and O.D. across (I.D. = O.D. - 2 W)
    stepName = "Ring size check"
    Dim rb_c() As String, rb_w() As Double, rb_o() As Double, rb_i As Long, rb_b As Variant, rb_x As Double, rb_y As Double, rb_z As Double
    ReDim rb_c(28): ReDim rb_w(28): ReDim rb_o(28)
    rb_c(0) = "4000-08": rb_w(0) = 0.087000: rb_o(0) = 0.818000
    rb_c(1) = "4000-02": rb_w(1) = 0.064000: rb_o(1) = 0.367000
    rb_c(2) = "4000-03": rb_w(2) = 0.064000: rb_o(2) = 0.429000
    rb_c(3) = "4000-04": rb_w(3) = 0.072000: rb_o(3) = 0.495000
    rb_c(4) = "4000-06": rb_w(4) = 0.078000: rb_o(4) = 0.624000
    rb_c(5) = "4000-10": rb_w(5) = 0.097000: rb_o(5) = 0.949000
    rb_c(6) = "4000-12": rb_w(6) = 0.116000: rb_o(6) = 1.156000
    rb_c(7) = "4000-16": rb_w(7) = 0.116000: rb_o(7) = 1.403000
    rb_c(8) = "4000-20": rb_w(8) = 0.118000: rb_o(8) = 1.711000
    rb_c(9) = "4000-24": rb_w(9) = 0.118000: rb_o(9) = 1.956000
    rb_c(10) = "4000-32": rb_w(10) = 0.118000: rb_o(10) = 2.573000
    rb_c(11) = "4001-02": rb_w(11) = 0.064000: rb_o(11) = 0.367000
    rb_c(12) = "4001-04": rb_w(12) = 0.072000: rb_o(12) = 0.495000
    rb_c(13) = "4001-06": rb_w(13) = 0.078000: rb_o(13) = 0.624000
    rb_c(14) = "4001-08": rb_w(14) = 0.087000: rb_o(14) = 0.818000
    rb_c(15) = "4001-10": rb_w(15) = 0.097000: rb_o(15) = 0.949000
    rb_c(16) = "4001-12": rb_w(16) = 0.116000: rb_o(16) = 1.156000
    rb_c(17) = "4001-16": rb_w(17) = 0.116000: rb_o(17) = 1.403000
    rb_c(18) = "4001-20": rb_w(18) = 0.118000: rb_o(18) = 1.711000
    rb_c(19) = "4001-24": rb_w(19) = 0.118000: rb_o(19) = 1.956000
    rb_c(20) = "4001-32": rb_w(20) = 0.118000: rb_o(20) = 2.573000
    rb_c(21) = "FS4000-04": rb_w(21) = 0.070000: rb_o(21) = 0.441000
    rb_c(22) = "FS4000-06": rb_w(22) = 0.070000: rb_o(22) = 0.504000
    rb_c(23) = "FS4000-08": rb_w(23) = 0.070000: rb_o(23) = 0.629000
    rb_c(24) = "FS4000-10": rb_w(24) = 0.070000: rb_o(24) = 0.754000
    rb_c(25) = "FS4000-12": rb_w(25) = 0.070000: rb_o(25) = 0.879000
    rb_c(26) = "FS4000-16": rb_w(26) = 0.070000: rb_o(26) = 1.066000
    rb_c(27) = "FS4000-20": rb_w(27) = 0.070000: rb_o(27) = 1.316000
    rb_c(28) = "FS4000-24": rb_w(28) = 0.070000: rb_o(28) = 1.629000
    For rb_i = 0 To 28
        swModel.ShowConfiguration2 rb_c(rb_i)
        swModel.ForceRebuild3 False
        rb_b = swModel.GetPartBox(True)
        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_
        Check rb_c(rb_i) & ": thickness " & Format(rb_x, "0.0000") & " (W " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005
        rb_b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
        Check rb_c(rb_i) & ": split lines present (8 faces, found " & rb_b(0).GetFaceCount & ")", rb_b(0).GetFaceCount = 8
    Next rb_i

    swModel.ShowConfiguration2 "4000-08"
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
    ' 2026-09-25: leave the master in its reference configuration (4000-08) - SolidWorks opens a part in the configuration that is active when it is saved;
    ' before this the master was left in the first name of the list (the smallest size)
    swModel.ShowConfiguration2 "4000-08"
    Trace "Master left in its reference configuration 4000-08 for the save (it opens in this size)"
    Trace "No THD_ features in this master (O-rings carry no threads)"

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
    MsgBox "Build_4000_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
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

