Attribute VB_Name = "Build_0319_MASTER"
' ============================================================================
'  Build_0319_MASTER.bas  -  OMi fitting library, generated 2026-10-21 by gen_ring.py
'  JIC Tube Sleeve - master from reference configuration 0319-08 (DesignTable_0319_SW2.xlsx row 2)
'  Axis = X (RING_AXIS); DRIVE = closed half-section P0..P6 (front face x = 0, collar, step, spigot, rear face x = L, bore,
'  inner front cone) + construction line origin -> collar corner; revolved 360 deg. No hex, no threads.
'  Run in SolidWorks: Tools > Macro > Run > Build0319.  Report: 03_SCRIPTS\Build_0319_report.txt
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const TABLE_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\04_DESIGN_TABLES\DesignTable_0319_SW2.xlsx"
Const SAVE_PATH  As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\0319_MASTER.SLDPRT"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_0319_report.txt"

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swSkMgr As SldWorks.SketchManager
Dim swFeatMgr As SldWorks.FeatureManager
Dim swSelMgr As SldWorks.SelectionMgr
Dim report As String
Dim nErr As Long
Dim fnRep As Integer
Dim stepName As String

Sub Build0319()
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
    Print #fnRep, "Build_0319_MASTER  " & Now
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

    ' ================= 1. DRIVE sketch: closed half-section P0..P6 + construction line origin -> collar corner P1 =================
    stepName = "DRIVE sketch"
    swModel.Extension.SelectByID2 "Front Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    swSkMgr.AddToDB = True
    Dim seg(6) As SldWorks.SketchSegment, cl As SldWorks.SketchSegment, i As Long
    Set seg(0) = swSkMgr.CreateLine(0.000000000, 0.007480300, 0, 0.000000000, 0.008636000, 0)
    Set seg(1) = swSkMgr.CreateLine(0.000000000, 0.008636000, 0, 0.005588000, 0.008636000, 0)
    Set seg(2) = swSkMgr.CreateLine(0.005588000, 0.008636000, 0, 0.005588000, 0.007137400, 0)
    Set seg(3) = swSkMgr.CreateLine(0.005588000, 0.007137400, 0, 0.014224000, 0.007137400, 0)
    Set seg(4) = swSkMgr.CreateLine(0.014224000, 0.007137400, 0, 0.014224000, 0.006413500, 0)
    Set seg(5) = swSkMgr.CreateLine(0.014224000, 0.006413500, 0, 0.001643380, 0.006413500, 0)
    Set seg(6) = swSkMgr.CreateLine(0.001643380, 0.006413500, 0, 0.000000000, 0.007480300, 0)
    Set cl = swSkMgr.CreateLine(0, 0, 0, 0, 0.008636000, 0)
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
    Set dd = swModel.AddDimension2(-0.007620, 0.004318, 0)
    NameDim dd, "COLLARR", 0.008636000
    ' L = front face to rear face
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    seg(4).Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.007112, 0.020066, 0)
    NameDim dd, "L", 0.014224000
    ' COLLARL = front face to the step face
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    seg(2).Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.002794, 0.012446, 0)
    NameDim dd, "COLLARL", 0.005588000
    ' SPIGOTR / BORER = origin to the spigot line / the bore line
    swModel.ClearSelection2 True
    seg(3).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.021844, 0.003569, 0)
    NameDim dd, "SPIGOTR", 0.007137400
    swModel.ClearSelection2 True
    seg(5).Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddDimension2(0.028194, 0.003207, 0)
    NameDim dd, "BORER", 0.006413500
    ' FRONTIR = origin to P0 (vertical), CONEL = front face to P6 (where the cone meets the bore)
    Set ln1 = seg(0)
    swModel.ClearSelection2 True
    ln1.GetStartPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    Set dd = swModel.AddVerticalDimension2(-0.013970, 0.003740, 0)
    NameDim dd, "FRONTIR", 0.007480300
    Set ln1 = seg(6)
    swModel.ClearSelection2 True
    seg(0).Select4 False, Nothing
    ln1.GetStartPoint2.Select4 True, Nothing
    Set dd = swModel.AddDimension2(0.000822, 0.002603, 0)
    NameDim dd, "CONEL", 0.001643380
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
    Check "Sleeve volume " & Format(vrev / IN_ ^ 3, "0.00000") & " in^3 (revolved half-section 0.04980)", Abs(vrev - 8.160356608896e-07) < 8.160356608896e-07 * 0.002

    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
    Check "Sleeve length along the axis " & Format(lenX, "0.0000") & " (expect L 0.5600)", Abs(lenX - 0.56) < 0.005
    Check "Sleeve O.D. " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect collar 0.6800)", Abs(dY - 0.680000) < 0.005 And Abs(dZ - 0.680000) < 0.005
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
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect 13)", (UBound(cfgs) + 1) >= 12
    ' ---- config spot check: do the table values actually land in the model? (SP3 lesson)
    stepName = "Config check"
    Dim cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature
    cx_c = Array("0319-02", "0319-32")
    cx_p = Array("L@DRIVE", "COLLARR@DRIVE", "BORER@DRIVE", "CONEL@DRIVE")
    cx_w = Array(Array(0.34000, 0.13500, 0.06500, 0.05180), Array(1.19000, 1.20500, 1.00700, 0.14640))
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
    ReDim rb_c(11): ReDim rb_w(11): ReDim rb_o(11)
    rb_c(0) = "0319-08": rb_w(0) = 0.560000: rb_o(0) = 0.680000
    rb_c(1) = "0319-02": rb_w(1) = 0.340000: rb_o(1) = 0.270000
    rb_c(2) = "0319-03": rb_w(2) = 0.340000: rb_o(2) = 0.330000
    rb_c(3) = "0319-04": rb_w(3) = 0.410000: rb_o(3) = 0.380000
    rb_c(4) = "0319-05": rb_w(4) = 0.440000: rb_o(4) = 0.440000
    rb_c(5) = "0319-06": rb_w(5) = 0.500000: rb_o(5) = 0.500000
    rb_c(6) = "0319-10": rb_w(6) = 0.660000: rb_o(6) = 0.800000
    rb_c(7) = "0319-12": rb_w(7) = 0.680000: rb_o(7) = 0.970000
    rb_c(8) = "0319-16": rb_w(8) = 0.780000: rb_o(8) = 1.220000
    rb_c(9) = "0319-20": rb_w(9) = 0.910000: rb_o(9) = 1.530000
    rb_c(10) = "0319-24": rb_w(10) = 1.120000: rb_o(10) = 1.780000
    rb_c(11) = "0319-32": rb_w(11) = 1.190000: rb_o(11) = 2.410000
    For rb_i = 0 To 11
        swModel.ShowConfiguration2 rb_c(rb_i)
        swModel.ForceRebuild3 False
        rb_b = swModel.GetPartBox(True)
        rb_x = (rb_b(3) - rb_b(0)) / IN_: rb_y = (rb_b(4) - rb_b(1)) / IN_: rb_z = (rb_b(5) - rb_b(2)) / IN_
        Check rb_c(rb_i) & ": length " & Format(rb_x, "0.0000") & " (L " & Format(rb_w(rb_i), "0.0000") & "), O.D. " & Format(rb_y, "0.0000") & " / " & Format(rb_z, "0.0000") & " (expect " & Format(rb_o(rb_i), "0.0000") & ")", Abs(rb_x - rb_w(rb_i)) < 0.005 And Abs(rb_y - rb_o(rb_i)) < 0.005 And Abs(rb_z - rb_o(rb_i)) < 0.005
    Next rb_i

    swModel.ShowConfiguration2 "0319-08"
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
    ' 2026-09-25: leave the master in its reference configuration (0319-08) - SolidWorks opens a part in the configuration that is active when it is saved;
    ' before this the master was left in the first name of the list (the smallest size)
    swModel.ShowConfiguration2 "0319-08"
    Trace "Master left in its reference configuration 0319-08 for the save (it opens in this size)"
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
    MsgBox "Build_0319_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
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

