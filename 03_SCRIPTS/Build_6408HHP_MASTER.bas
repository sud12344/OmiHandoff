Attribute VB_Name = "Build_6408HHP_MASTER"
' ============================================================================
'  Build_6408HHP_MASTER.bas  -  OMi fitting library, generated 2026-10-19 by gen_straight2.py
'  ORB Hollow Hex Plug (round head, internal hex socket) - master from reference configuration 6408-HHP-08-O (DesignTable_6408HHP_SW2.xlsx row 2)
'  Ends: A = ORBM  B = PLAIN.  Round body revolved at BODYR (no hex); internal hex socket cut into the head face; SP3 radius dims.
'  Run in SolidWorks: Tools > Macro > Run > Build6408HHP.  Report: 03_SCRIPTS\Build_6408HHP_report.txt
' ============================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const SUPPRESS_THREADS As Boolean = False      ' True = project resting state (threads suppressed); False = threads visible
Const TABLE_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\04_DESIGN_TABLES\DesignTable_6408HHP_SW2.xlsx"
Const SAVE_PATH  As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\6408HHP_MASTER.SLDPRT"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_6408HHP_report.txt"

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

Const NPTS As Long = 8
Dim PX(7) As Double, PR(7) As Double

Sub LoadPoints()
    Dim v As Variant, i As Long
    v = Array( _
    0.000000000, 0.000000000, _
    0.000000000, 0.009525000, _
    0.008737600, 0.009525000, _
    0.008737600, 0.008382000, _
    0.011125200, 0.008382000, _
    0.011125200, 0.011112500, _
    0.014732000, 0.011112500, _
    0.014732000, 0.000000000)
    For i = 0 To NPTS - 1
        PX(i) = v(2 * i): PR(i) = v(2 * i + 1)
    Next i
End Sub

Sub Build6408HHP()
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
    Print #fnRep, "Build_6408HHP_MASTER  " & Now
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

    Call Dim_len(-1, "L", 0.014732000, 0.007366, 0.026353)
    Call Dim_rad(5, "BODYR", 0.011112500, 0.012929, -0.011430)
    Call Dim_rad(1, "THDMAJR_A", 0.009525000, 0.004369, -0.007620)
    Call Dim_len(1, "ORBA_THDL", 0.008737600, 0.004369, 0.017462)
    Call Dim_rad(3, "ORBA_GRVR", 0.008382000, 0.009931, -0.005080)
    Call Dim_len(3, "ORBA_GRVW", 0.002387600, 0.009931, 0.014923)
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
    Check "Revolved volume " & Format(vrev / IN_ ^ 3, "0.0000") & " in^3 (expect 0.2695)", Abs(vrev - 4.416662440994e-06) < 4.416662440994e-06 * 0.002

    ' (round bar - no hex cut)

    stepName = "Pockets and bores"
    Dim sockcut As SldWorks.Feature
    Set sockcut = SocketCut(0.014732000, 0.007950200, 0.004775200, "SOCKET", "SOCKAF", "SOCKETCUT")
    Check "SOCKAF@SOCKET reachable", Not swModel.Parameter("SOCKAF@SOCKET") Is Nothing
    Check "DEPTH@SOCKETCUT reachable", Not swModel.Parameter("DEPTH@SOCKETCUT") Is Nothing
    Check "socket plug: End A (thread tip) closed on the axis (x=0)", AxisCovered(0#)
    Check "socket open on the axis at the head face (x=0.5800)", Not AxisCovered(0.014732000)
    Check "socket bottom present at x=0.3920", AxisCovered(0.009956800)
    stepName = "Threads"
    curAxis = 0
    Call ThreadCut(0.008737600, 0.009525000, 0.008737600, "0.7500-16", "THD_EndA", -1#, 0.001587500)
    stepName = "Self-checks"
    Dim bb As Variant
    bb = swModel.GetPartBox(True)
    Dim lenX As Double, dY As Double, dZ As Double
    lenX = (bb(3) - bb(0)) / IN_: dY = (bb(4) - bb(1)) / IN_: dZ = (bb(5) - bb(2)) / IN_
    Trace "Bounding box length " & Format(lenX, "0.0000") & " (nominal 0.5800; loose around thread faces, informational)"
    Check "End A face present at x=0", SelectEndFace(0#)
    Check "End B face present at x=0.5800", SelectEndFace(0.014732000)
    Check "Body within nominal length +0.15 (threads loosen the box)", Abs(lenX - 0.58) < 0.15
    Check "Body diameter " & Format(dY, "0.0000") & " / " & Format(dZ, "0.0000") & " (expect 0.8750)", Abs(dY - 0.8750) < 0.01 And Abs(dZ - 0.8750) < 0.01
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
    Check "Configurations after table: " & (UBound(cfgs) + 1) & " (expect 2)", (UBound(cfgs) + 1) >= 1
    ' ---- config spot check: do the table values actually land in the model? (SP3 lesson)
    stepName = "Config check"
    Dim cx_v As Double, cx_c As Variant, cx_p As Variant, cx_w As Variant, cx_prm As SldWorks.Dimension, cx_bx As Variant, cx_nb As Long, cx_q As Long, cx_k As Long, cx_b As Variant, cx_f As SldWorks.Feature
    cx_c = Array("6408-HHP-08-O")
    cx_p = Array("L@DRIVE", "BODYR@DRIVE", "THDMAJR_A@DRIVE", "ORBA_THDL@DRIVE", "ORBA_GRVR@DRIVE", "ORBA_GRVW@DRIVE", "THDPITCH@THD_EndA", "Profile_Height@THD_EndA_PROF", "THDPITCH@THD_EndA_PROF", "SOCKAF@SOCKET", "DEPTH@SOCKETCUT")
    cx_w = Array(Array(0.58000, 0.43750, 0.37500, 0.34400, 0.33000, 0.09400, 0.06250, 0.03383, 0.06250, 0.31300, 0.18800))
    For cx_q = 0 To 0
        Progress "config check " & (cx_q + 1) & ": " & cx_c(cx_q)
        swModel.ShowConfiguration2 cx_c(cx_q)
        swModel.ForceRebuild3 False
        For cx_k = 0 To 10
            Set cx_prm = swModel.Parameter(cx_p(cx_k))
            If cx_prm Is Nothing Then
                Check cx_c(cx_q) & " " & cx_p(cx_k) & " readable", False
            Else
                cx_v = IIf(InStr(cx_p(cx_k), "TAPER") > 0 Or InStr(cx_p(cx_k), "ANG") > 0 Or InStr(cx_p(cx_k), "SEATB") > 0, cx_prm.SystemValue * 180 / 3.14159265358979, cx_prm.SystemValue / IN_)
                Check cx_c(cx_q) & " " & cx_p(cx_k) & " = " & Format(cx_v, "0.0000") & " (table " & Format(cx_w(cx_q)(cx_k), "0.0000") & ")", Abs(cx_v - cx_w(cx_q)(cx_k)) < 0.0005
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
    ' ---- hex socket in every configuration (2026-10-02, PLUGS): open at the head face, flat bottom at L - depth, thread tip closed
    stepName = "Socket check"
    swModel.ShowConfiguration2 "6408-HHP-08-O"
    swModel.ForceRebuild3 False
    Check "6408-HHP-08-O: socket open on the axis at the head face (x=0.5800)", Not AxisCovered(0.014732000)
    Check "6408-HHP-08-O: socket bottom at x=0.3920 (depth 0.188, A/F 0.313)", AxisCovered(0.009956800)
    Check "6408-HHP-08-O: End A tip closed on the axis (x=0)", AxisCovered(0#)

    swModel.ShowConfiguration2 "6408-HHP-08-O"
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
    ' 2026-09-25: leave the master in its reference configuration (6408-HHP-08-O) - SolidWorks opens a part in the configuration that is active when it is saved;
    ' before this the master was left in the first name of the list (the smallest size)
    swModel.ShowConfiguration2 "6408-HHP-08-O"
    Trace "Master left in its reference configuration 6408-HHP-08-O for the save (it opens in this size)"

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
    MsgBox "Build_6408HHP_MASTER finished with " & nErr & " problem(s)." & vbCrLf & "Report: " & REPORT_PATH & vbCrLf & vbCrLf & Left(report, 600), vbInformation
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
Sub NameAng(dd As SldWorks.DisplayDimension, nm As String, valRad As Double)
    If dd Is Nothing Then Check "angle " & nm & " was not created", False: Exit Sub
    Dim d As SldWorks.Dimension
    Set d = dd.GetDimension2(0)
    d.Name = nm
    Dim v As Double: v = d.SystemValue
    Check "angle " & nm & " = " & Format(v * 180 / 3.14159265358979, "0.00") & " deg", Abs(v - valRad) < 0.0005
End Sub
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
Sub Dim_len2(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    Dim_len i, nm, valM, tx, ty
End Sub
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
    If dd.GetAnnotation.Select2(False, 0) Then     ' Select3(False, Nothing) selects nothing in an open sketch (2026-09-25)
        If swSelMgr.GetSelectedObjectCount2(-1) = 1 Then swModel.EditDelete
    End If
    swModel.ClearSelection2 True
End Sub
Sub Collinear(i As Long, j As Long)
    swModel.ClearSelection2 True
    seg(i).Select4 False, Nothing
    seg(j).Select4 True, Nothing
    swModel.SketchAddConstraints "sgCOLINEAR"
    swModel.ClearSelection2 True
End Sub
Sub BoreCut(skName As String, dimName As String, diaM As Double, depthM As Double, startOff As Double, featName As String, fromEndB As Boolean, faceR As Double)
    On Error GoTo BErr
1000 Dim faceX As Double
1010 faceX = IIf(fromEndB, PX(NPTS - 1), 0#)
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
1290 swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
1300 swModel.SketchAddConstraints "sgCOINCIDENT"
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
        Trace nm & ": dim full name " & dm.FullName
        Set d = f.GetNextDisplayDimension(d)
    Loop
    Check nm & " dims: " & names, InStr(names, "DEPTH=") > 0 And InStr(names, "THDDIA=") > 0 And InStr(names, "THDPITCH=") > 0
    Dim sf As SldWorks.Feature: Set sf = f.GetFirstSubFeature
    Do While Not sf Is Nothing
        If Left(sf.Name, 14) = "Thread Profile" Then sf.Name = nm & "_PROF": Trace nm & ": profile sketch " & IIf(Err.Number <> 0, "rename FAILED " & Err.Description, "renamed to " & sf.Name): Err.Clear
        Set sf = sf.GetNextSubFeature
    Loop
    Check nm & " profile dims reachable as Profile_Height@" & nm & "_PROF", Not swModel.Parameter("Profile_Height@" & nm & "_PROF") Is Nothing
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
    If SUPPRESS_THREADS Then
        sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)
        Check nm & " suppressed (resting state)", sup
    Else
        Trace nm & ": left UNSUPPRESSED (SUPPRESS_THREADS = False)"
    End If
End Sub
Sub Dim_pair(i As Long, j As Long, nm As String, valM As Double, tx As Double, ty As Double)
    ' distance between two parallel sketch lines seg(i) and seg(j) (overall length when End B is a port cavity)
    swModel.ClearSelection2 True
    seg(i).Select4 False, Nothing
    seg(j).Select4 True, Nothing
    Dim dd As SldWorks.DisplayDimension
    Set dd = swModel.AddDimension2(tx, ty, 0)
    NameDim dd, nm, valM
End Sub
Sub Dim_ang(i As Long, j As Long, nm As String, valRad As Double, tx As Double, ty As Double)
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
End Function

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
            If Abs(cp(0) - ex) < 0.00002 And Abs(cp(1)) < 0.00002 And Abs(cp(2)) < 0.00002 And Abs(cp(6) - er) < 0.00002 Then
                Dim sd As SldWorks.SelectData
                Set sd = swSelMgr.CreateSelectData: sd.Mark = mark
                swModel.ClearSelection2 True
                SelectCircEdge = e.Select4(False, sd)
                Exit Function
            End If
        End If
    Next i
End Function
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
            If Abs(Abs(pp(0)) - 1) < 0.0001 And Abs(pp(3) - fx) < 0.00002 Then
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
            If bx(0) < lo Then lo = bx(0)
            If bx(3) > hi Then hi = bx(3)
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
Sub HelixThread(tipAx As Double, rM As Double, heightM As Double, pitchM As Double, thdhM As Double, taperRad As Double, taperOut As Boolean, apexOut As Boolean, sfx As String, nm As String)
    On Error Resume Next
    Dim ok As Boolean, f As SldWorks.Feature, sk As SldWorks.Feature, hx As SldWorks.Feature, dd As SldWorks.DisplayDimension
    ' --- helix sketch on the end face
    ok = SelectEndFace(tipAx)
    Check nm & ": end face found at " & Format(tipAx / IN_, "0.0000"), ok
    If Not ok Then Exit Sub
    swSkMgr.InsertSketch True
    Dim c As SldWorks.SketchSegment, ca As SldWorks.SketchArc
    swSkMgr.AddToDB = True           ' no inference: the circle must not snap to a nearby edge (nose OD, 2026-09-25)
    Set c = swSkMgr.CreateCircleByRadius(0, 0, 0, rM)
    swSkMgr.AddToDB = False
    Set ca = c
    swModel.ClearSelection2 True
    ca.GetCenterPoint2.Select4 False, Nothing
    swModel.Extension.SelectByID2 "Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, True, 0, Nothing, 0
    swModel.SketchAddConstraints "sgCOINCIDENT"
    swModel.ClearSelection2 True
    c.Select4 False, Nothing
    Set dd = swModel.AddDimension2(rM * 2, rM * 2, 0)
    If Not dd Is Nothing Then dd.GetDimension2(0).SystemValue = 2 * rM
    NameDim dd, "HELIXDIA", 2 * rM
    ' sketch X axis of this face sketch, in model coords (= helix start direction, start angle 0)
    Dim skc As SldWorks.Sketch, xf As SldWorks.MathTransform, ad As Variant, xd(2) As Double, au(2) As Double
    Set skc = swSkMgr.ActiveSketch
    Set xf = skc.ModelToSketchTransform: Set xf = xf.Inverse
    ad = xf.ArrayData
    xd(0) = ad(0): xd(1) = ad(1): xd(2) = ad(2)
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Set sk = swModel.FeatureByPositionReverse(0): sk.Name = "HELIXSK_" & sfx
    Check nm & " helix sketch made (" & sk.GetTypeName2 & ")", sk.GetTypeName2 = "ProfileFeature"
    ' --- helix (into the part)
    swModel.ClearSelection2 True
    sk.Select2 False, 0
    Dim mdLate As Object: Set mdLate = swModel
    mdLate.InsertHelix True, True, (taperRad > 0), taperOut, swHelixDefinedBy_e.swHelixDefinedByHeightAndPitch, heightM, pitchM, 0#, taperRad, 0#
    Trace nm & ": InsertHelix " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    Set hx = swModel.FeatureByPositionReverse(0)
    If hx.GetTypeName2 <> "Helix" Then Set hx = Nothing
    Check nm & " helix created", Not hx Is Nothing
    If hx Is Nothing Then Exit Sub
    hx.Name = "HELIX_" & sfx
    Dim d As SldWorks.DisplayDimension, dm As SldWorks.Dimension, names As String
    Set d = hx.GetFirstDisplayDimension
    Do While Not d Is Nothing
        Set dm = d.GetDimension2(0)
        If Abs(dm.SystemValue - heightM) < 0.000001 Then dm.Name = "HEIGHT"
        If Abs(dm.SystemValue - pitchM) < 0.000001 Then dm.Name = "PITCH"
        names = names & dm.Name & " "
        Set d = hx.GetNextDisplayDimension(d)
    Loop
    Check nm & " helix dims named (" & names & ")", InStr(names, "HEIGHT") > 0 And InStr(names, "PITCH") > 0
    ' --- helix start point in model coords
    au(0) = 0: au(1) = 0: au(2) = 0: au(curAxis) = 1
    Dim sp(2) As Double, k As Long
    For k = 0 To 2: sp(k) = au(k) * tipAx + xd(k) * rM: Next k
    ' the helix start is READ from the helix curve: the face sketch's X axis does not always give it (2026-09-25:
    ' 6565 had it 90 deg off - the thread profile then sat beside the helix and the swept cut failed)
    Dim rcv As Object, egv As Object, vxa As Object, vxb As Object, pa As Variant, pb As Variant
    Set rcv = hx.GetSpecificFeature2
    If Not rcv Is Nothing Then Set egv = rcv.GetFirstSegment
    If Not egv Is Nothing Then
        Set vxa = egv.GetStartVertex: Set vxb = egv.GetEndVertex
        If Not vxa Is Nothing Then
            pa = vxa.GetPoint
            If Not vxb Is Nothing Then
                pb = vxb.GetPoint
                If Abs(pb(curAxis) - tipAx) < Abs(pa(curAxis) - tipAx) Then pa = pb
            End If
            If Abs(pa(curAxis) - tipAx) < 0.00001 Then
                Trace nm & ": helix start from the curve (" & Format(pa(0) / IN_, "0.0000") & ", " & Format(pa(1) / IN_, "0.0000") & ", " & Format(pa(2) / IN_, "0.0000") & ")"
                For k = 0 To 2: sp(k) = pa(k): xd(k) = (pa(k) - au(k) * tipAx) / rM: Next k
            End If
        End If
    End If
    Err.Clear
    Trace nm & ": helix start = (" & Format(sp(0) / IN_, "0.0000") & ", " & Format(sp(1) / IN_, "0.0000") & ", " & Format(sp(2) / IN_, "0.0000") & ")"
    ' --- profile plane = principal plane containing the axis and the start point
    Dim nrm(2) As Double, plane As String, pinPlane As String
    nrm(0) = au(1) * xd(2) - au(2) * xd(1): nrm(1) = au(2) * xd(0) - au(0) * xd(2): nrm(2) = au(0) * xd(1) - au(1) * xd(0)
    If Abs(nrm(2)) >= Abs(nrm(0)) And Abs(nrm(2)) >= Abs(nrm(1)) Then
        plane = "Front Plane"
    ElseIf Abs(nrm(1)) >= Abs(nrm(0)) Then
        plane = "Top Plane"
    Else
        plane = "Right Plane"
    End If
    pinPlane = IIf(curAxis = 0, "Right Plane", "Top Plane")
    Trace nm & ": profile on " & plane
    swModel.ClearSelection2 True
    swModel.Extension.SelectByID2 plane, "PLANE", 0, 0, 0, False, 0, Nothing, 0
    swSkMgr.InsertSketch True
    ' sketch coords of start point, origin and an axial probe
    Dim mu As SldWorks.MathUtility, mp As SldWorks.MathPoint, xf2 As SldWorks.MathTransform, pd As Variant
    Set mu = swApp.GetMathUtility
    Set xf2 = swSkMgr.ActiveSketch.ModelToSketchTransform
    Set mp = mu.CreatePoint(sp): Set mp = mp.MultiplyTransform(xf2): pd = mp.ArrayData
    Dim u0 As Double, v0 As Double: u0 = pd(0): v0 = pd(1)
    Dim oz(2) As Double: Set mp = mu.CreatePoint(oz): Set mp = mp.MultiplyTransform(xf2): pd = mp.ArrayData
    Dim ou As Double, ov As Double: ou = pd(0): ov = pd(1)
    Set mp = mu.CreatePoint(au): Set mp = mp.MultiplyTransform(xf2): pd = mp.ArrayData
    Dim axialIsX As Boolean: axialIsX = (Abs(pd(0) - ou) > Abs(pd(1) - ov))
    Dim sRad As Double     ' +1/-1: direction "away from the axis" along the radial sketch axis
    If axialIsX Then sRad = IIf(v0 - ov >= 0, 1#, -1#) Else sRad = IIf(u0 - ou >= 0, 1#, -1#)
    Dim sApex As Double: sApex = IIf(apexOut, sRad, -sRad)
    Dim half As Double: half = thdhM * Tan(3.14159265358979 / 6)
    Trace nm & ": sketch start (" & Format(u0 / IN_, "0.0000") & "," & Format(v0 / IN_, "0.0000") & ") axialIsX=" & axialIsX & " apex dir " & sApex
    ' local (a = axial, q = radial) -> sketch (u, v)
    Dim a0 As Double, q0 As Double: If axialIsX Then a0 = u0: q0 = v0 Else a0 = v0: q0 = u0
    swSkMgr.AddToDB = True
    Dim l1 As SldWorks.SketchSegment, l1b As SldWorks.SketchSegment, l2 As SldWorks.SketchSegment, l3 As SldWorks.SketchSegment, lc As SldWorks.SketchSegment
    Set l1 = MkLine(axialIsX, a0 - half, q0, a0, q0)
    Set l1b = MkLine(axialIsX, a0, q0, a0 + half, q0)
    Set l2 = MkLine(axialIsX, a0 + half, q0, a0, q0 + sApex * thdhM)
    Set l3 = MkLine(axialIsX, a0, q0 + sApex * thdhM, a0 - half, q0)
    Set lc = MkLine(axialIsX, a0, q0, a0, q0 + sApex * thdhM)
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
    Dim baseRel As String, perpRel As String
    baseRel = IIf(axialIsX, "sgHORIZONTAL", "sgVERTICAL"): perpRel = IIf(axialIsX, "sgVERTICAL", "sgHORIZONTAL")
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: swModel.SketchAddConstraints baseRel
    swModel.ClearSelection2 True: l1b.Select4 False, Nothing: swModel.SketchAddConstraints baseRel
    swModel.ClearSelection2 True: lc.Select4 False, Nothing: swModel.SketchAddConstraints perpRel
    swModel.ClearSelection2 True: l1.Select4 False, Nothing: l1b.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    swModel.ClearSelection2 True: l2.Select4 False, Nothing: l3.Select4 True, Nothing: swModel.SketchAddConstraints "sgSAMELENGTH"
    ' axial pin of the centre point P
    If Abs(tipAx) < 0.0000001 Then
        swModel.ClearSelection2 True: ln1.GetEndPoint2.Select4 False, Nothing
        swModel.Extension.SelectByID2 pinPlane, "PLANE", 0, 0, 0, True, 0, Nothing, 0
        swModel.SketchAddConstraints "sgCOINCIDENT"
        Trace nm & ": P on " & pinPlane & " " & IIf(Err.Number <> 0, "[err " & Err.Description & "]", "ok"): Err.Clear
    Else
        Call DimPtOrigin(ln1.GetEndPoint2, "PROF_AX", Abs(tipAx), axialIsX, True, u0, v0, ou, ov)
    End If
    Call DimPtOrigin(ln1.GetEndPoint2, "PROF_R", Abs(q0 - IIf(axialIsX, ov, ou)), axialIsX, False, u0, v0, ou, ov)
    Call DimPtOrigin(ln2.GetEndPoint2, "APEXR", Abs(q0 + sApex * thdhM - IIf(axialIsX, ov, ou)), axialIsX, False, u0, v0, ou, ov)
    ' 60 deg between the sloped sides
    Dim kk As Long, v As Double
    For kk = 0 To 5
        swModel.ClearSelection2 True
        l2.Select4 False, Nothing: l3.Select4 True, Nothing
        If axialIsX Then
            Set dd = swModel.AddDimension2(a0 + IIf(kk >= 4, 0.003 * (kk - 4.5), 0), q0 + sApex * thdhM * (1.6 - (kk Mod 2) * 2.4), 0)
        Else
            Set dd = swModel.AddDimension2(q0 + sApex * thdhM * (1.6 - (kk Mod 2) * 2.4), a0 + IIf(kk >= 4, 0.003 * (kk - 4.5), 0), 0)
        End If
        If dd Is Nothing Then Exit For
        v = dd.GetDimension2(0).SystemValue
        If Abs(v - 3.14159265358979 / 3) < 0.001 Then Exit For
        DeleteDisp dd: Set dd = Nothing
    Next kk
    Check nm & " 60 deg tooth angle placed", (Not dd Is Nothing) And Abs(v - 3.14159265358979 / 3) < 0.001
    swModel.ClearSelection2 True
    swSkMgr.InsertSketch True
    Dim pf As SldWorks.Feature
    Set pf = swModel.FeatureByPositionReverse(0): pf.Name = "THDPROF_" & sfx
    Check nm & " profile sketch fully defined", (pf.GetSpecificFeature2.GetConstrainedStatus = swConstrainedStatus_e.swFullyConstrained)
    ' --- swept cut
    Dim vol0 As Double: vol0 = Volume()
    Dim swd As Object
    Set swd = swFeatMgr.CreateDefinition(swFeatureNameID_e.swFmSweepCut)
    If Not swd Is Nothing Then
        Set swd.Profile = pf: Set swd.Path = hx
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
    If SUPPRESS_THREADS Then
        sup = f.SetSuppression2(swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swAllConfiguration, Empty)
        Check nm & " suppressed (resting state)", sup
    Else
        Trace nm & ": left UNSUPPRESSED (SUPPRESS_THREADS = False)"
    End If
End Sub
Function MkLine(axialIsX As Boolean, a1 As Double, q1 As Double, a2 As Double, q2 As Double) As SldWorks.SketchSegment
    If axialIsX Then
        Set MkLine = swSkMgr.CreateLine(a1, q1, 0, a2, q2, 0)
    Else
        Set MkLine = swSkMgr.CreateLine(q1, a1, 0, q2, a2, 0)
    End If
End Function
Sub DimPtOrigin(pt As SldWorks.SketchPoint, nm As String, expectM As Double, axialIsX As Boolean, axialDim As Boolean, u0 As Double, v0 As Double, ou As Double, ov As Double)
    ' point-to-origin dimension with an EXPLICIT type (horizontal = sketch X, vertical = sketch Y).
    ' v1 used AddDimension2 and let SolidWorks pick the type from the text position; that only worked when the
    ' point sat on the origin's X (End A, tipAx = 0) - at End B it produced aligned dims and the profile stayed under-defined.
    On Error Resume Next
    Dim dd As SldWorks.DisplayDimension, k As Long, v As Double, tx As Double, ty As Double, wantX As Boolean
    wantX = (axialDim = axialIsX)
    For k = 0 To 3
        tx = (u0 + ou) / 2: ty = (v0 + ov) / 2
        If wantX Then ty = ty + IIf(k Mod 2 = 0, 1, -1) * 0.02 * (1 + k \ 2) Else tx = tx + IIf(k Mod 2 = 0, 1, -1) * 0.02 * (1 + k \ 2)
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
Function AxisCovered(fx As Double) As Boolean
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
Function ZoneHexCut(onEndB As Boolean, faceXM As Double, afM As Double, startM As Double, depthM As Double, wantCxM As Double, skName As String, dimName As String, featName As String) As SldWorks.Feature
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
Sub FeatSpanX(f As SldWorks.Feature, lo As Double, hi As Double)
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
