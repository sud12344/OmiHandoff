Attribute VB_Name = "OMi_SeriesDrawings"
'==========================================================================================
'  OMi_SeriesDrawings.bas   -   one drawing sheet per SERIES (the five built masters).
'
'  For each series it finds the newest <series>_MASTER*.SLDPRT in the handoff folder,
'  opens it, activates the reference configuration, unsuppresses the THD_ thread features
'  so real threads show in the views, lays out Front / Right / Isometric views, inserts the
'  model dimensions and prunes them to the envelope set, adds a note block with the part
'  number, threads, material and data status, then writes a PDF and a SLDDRW.
'
'  Nothing is modified in the master parts: threads are put back to suppressed and the
'  parts are closed WITHOUT saving.
'
'  Run: open the VBA editor, import this file, run Sub SeriesDrawings.  No part need be open.
'  Report: 03_SCRIPTS\Build_SeriesDrawings_report.txt
'==========================================================================================
Option Explicit

Const IN_ As Double = 0.0254
Const ROOT As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\"
Const OUT_DIR As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\10_DRAWINGS\"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\Build_SeriesDrawings_report.txt"

' series | reference configuration.  2502 picks up the square-body part if one exists.
Const SERIES_LIST As String = "2403:2403-08-08|2405:2405-08-08|2500:2500-08-08|2502:2502-08-08|2603:2603-08-08-08"

' base drawing: your 6600 sheet (B size, OMi title block).  Opened, saved under the series name, its views removed, ours added.
' Leave blank to fall back to the SolidWorks default template.
Const BASE_DRAWING As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\02_TEMPLATES\OMi_SheetFormat_B_6600.SLDDRW"
Const SHOW_THREADS As Boolean = True      ' unsuppress THD_* for the views (slower, but real threads)
Const THREAD_PREFIX As String = "THD_"

' dimensions kept on the sheet - the envelope ones.  Everything else (the JIC end chain:
' relief, thread zone, land, seat, cone) is pruned so the sheet stays readable.
Const KEEP As String = "|L1|L2|M1|M2|M3|N1|HEXB|C2HEX|TAPDRILL|D|D1|D2|D3|WIDTH|ARMW|XEND|YTOP|CORNERR|BODYR|BODYDIA|BOSSR|HALFW_B|HALFW_T|"
' of those, the ones that are radii in the model but read better as diameters on a drawing
Const AS_DIA As String = "|BODYR|BODYDIA|BOSSR|CORNERR|THDMAJR_A|THDMAJR_B|JIC_CONER|"

Dim swApp As SldWorks.SldWorks
Dim fnRep As Integer
Dim nOK As Long, nFail As Long

Sub Say(s As String)
    ' write-through: open/append/close every line so the report survives a hang or a kill
    Dim fn As Integer: fn = FreeFile
    Open REPORT_PATH For Append As #fn
    Print #fn, s
    Close #fn
End Sub

Sub Chk(what As String, passed As Boolean)
    If passed Then Say "OK    " & what Else Say "FAIL  " & what: nFail = nFail + 1
End Sub

' newest file matching ROOT & pat
Function NewestPart(pat As String) As String
    Dim f As String, best As String, bestT As Date, t As Date
    f = Dir(ROOT & pat)
    Do While f <> ""
        If Left(f, 2) <> "~$" Then
            t = FileDateTime(ROOT & f)
            If best = "" Or t > bestT Then best = f: bestT = t
        End If
        f = Dir()
    Loop
    If best <> "" Then NewestPart = ROOT & best
End Function

Function Pick(series As String) As String
    ' prefer the forged hex-body master (<series>HX) when one has been built
    Dim p As String
    p = NewestPart(series & "HX_MASTER*.SLDPRT")
    If p = "" Then p = NewestPart(series & "_MASTER*.SLDPRT")
    Pick = p
End Function

Function Prop(swModel As SldWorks.ModelDoc2, cfg As String, nm As String) As String
    On Error Resume Next
    Dim ext As SldWorks.ModelDocExtension, cpm As SldWorks.CustomPropertyManager
    Dim v As String, r As String
    Set ext = swModel.Extension
    Set cpm = ext.CustomPropertyManager(cfg)
    cpm.Get4 nm, False, v, r
    If r <> "" Then Prop = r Else Prop = v
End Function

' every named dimension in the part, filtered by KEEP, as "NAME = value in" lines
Function KeyDims(swModel As SldWorks.ModelDoc2) As String
    On Error Resume Next
    Dim f As SldWorks.Feature, dd As SldWorks.DisplayDimension, dm As SldWorks.Dimension
    Dim seen As String, out As String, nm As String
    Set f = swModel.FirstFeature
    Do While Not f Is Nothing
        Set dd = f.GetFirstDisplayDimension
        Do While Not dd Is Nothing
            Set dm = dd.GetDimension2(0)
            nm = dm.Name
            If InStr(1, KEEP, "|" & nm & "|", vbTextCompare) > 0 And InStr(1, seen, "|" & nm & "|") = 0 Then
                seen = seen & "|" & nm & "|"
                out = out & nm & " = " & Format(dm.SystemValue / IN_, "0.000") & """" & vbLf
            End If
            Set dd = f.GetNextDisplayDimension(dd)
        Loop
        Set f = f.GetNextFeature
    Loop
    KeyDims = out
End Function

Function MarkAllDims(swModel As SldWorks.ModelDoc2) As Long
    On Error Resume Next
    Dim f As SldWorks.Feature, dd As SldWorks.DisplayDimension, n As Long
    Set f = swModel.FirstFeature
    Do While Not f Is Nothing
        Set dd = f.GetFirstDisplayDimension
        Do While Not dd Is Nothing
            dd.MarkedForDrawing = True: n = n + 1
            Set dd = f.GetNextDisplayDimension(dd)
        Loop
        Set f = f.GetNextFeature
    Loop
    MarkAllDims = n
End Function

Function SetThreads(swModel As SldWorks.ModelDoc2, suppress As Boolean) As Long
    On Error Resume Next
    Dim f As SldWorks.Feature, n As Long
    Set f = swModel.FirstFeature
    Do While Not f Is Nothing
        If Left(f.Name, Len(THREAD_PREFIX)) = THREAD_PREFIX Then
            f.SetSuppression2 IIf(suppress, swFeatureSuppressionAction_e.swSuppressFeature, swFeatureSuppressionAction_e.swUnSuppressFeature), _
                              swInConfigurationOpts_e.swThisConfiguration, Empty
            n = n + 1
        End If
        Set f = f.GetNextFeature
    Loop
    swModel.EditRebuild3
    SetThreads = n
End Function

Sub AddNote(swDraw As SldWorks.DrawingDoc, txt As String, x As Double, y As Double, h As Double)
    On Error Resume Next
    Dim nt As SldWorks.Note, an As SldWorks.Annotation
    swDraw.ClearSelection2 True
    Set nt = swDraw.InsertNote(txt)
    If nt Is Nothing Then Exit Sub
    Set an = nt.GetAnnotation
    If Not an Is Nothing Then an.SetPosition x, y, 0
End Sub

Sub SeriesDrawings()
    Dim i As Long, parts As Variant, one As Variant
    Dim t0 As Double: t0 = Timer
    Set swApp = Application.SldWorks
    fnRep = FreeFile
    Open REPORT_PATH For Output As #fnRep: Close #fnRep      ' truncate
    Say "OMi_SeriesDrawings  " & Now
    Say ""
    If Dir(OUT_DIR, vbDirectory) = "" Then MkDir OUT_DIR
    Say "output folder: " & OUT_DIR

    Dim tpl As String
    tpl = swApp.GetUserPreferenceStringValue(swUserPreferenceStringValue_e.swDefaultTemplateDrawing)
    Say "drawing template: " & tpl
    If BASE_DRAWING <> "" Then Say "base drawing: " & BASE_DRAWING & IIf(Dir(BASE_DRAWING) = "", "  (NOT FOUND - using the template)", "")
    Chk "a default drawing template is configured", tpl <> "" And Dir(tpl) <> ""
    If tpl = "" Or Dir(tpl) = "" Then
        Say "Set one in Tools > Options > System Options > File Locations > Document Templates, then re-run."
        MsgBox "No default drawing template found - see report.", vbExclamation
        Exit Sub
    End If

    parts = Split(SERIES_LIST, "|")
    For i = 0 To UBound(parts)
        one = Split(CStr(parts(i)), ":")
        MakeSheet CStr(one(0)), CStr(one(1)), tpl
    Next i

    Say ""
    Say "done in " & Format(Timer - t0, "0.0") & "s   sheets ok = " & nOK & "   problems = " & nFail
    MsgBox "Series drawings: " & nOK & " sheet(s) written, " & nFail & " problem(s)." & vbCrLf & OUT_DIR, vbInformation
End Sub

Sub MakeSheet(series As String, refCfg As String, tpl As String)
    On Error GoTo Fail
    Dim path As String, errs As Long, warns As Long
    Say ""
    Say "===== " & series & " ====="
    path = Pick(series)
    Chk series & ": master part found (" & path & ")", path <> ""
    If path = "" Then Exit Sub

    Dim swPart As SldWorks.ModelDoc2
    Set swPart = swApp.OpenDoc6(path, swDocumentTypes_e.swDocPART, swOpenDocOptions_e.swOpenDocOptions_Silent, "", errs, warns)
    Chk series & ": part opened (err " & errs & ")", Not swPart Is Nothing
    If swPart Is Nothing Then Exit Sub

    ' reference configuration
    Dim cfg As String
    cfg = refCfg
    If Not swPart.ShowConfiguration2(cfg) Then
        cfg = swPart.ConfigurationManager.ActiveConfiguration.Name
        Say "  " & refCfg & " not found, using the active configuration " & cfg
    End If
    swPart.EditRebuild3

    Dim nMk As Long: nMk = MarkAllDims(swPart)
    Say "  " & nMk & " model dimension(s) marked for drawing"
    Dim nThd As Long
    If SHOW_THREADS Then
        nThd = SetThreads(swPart, False)
        Say "  " & nThd & " thread feature(s) unsuppressed for the views"
    End If

    ' sheet size, so the views land on the paper whatever template is in use
    Dim swDraw As SldWorks.DrawingDoc, swModelDraw As SldWorks.ModelDoc2
    Dim base As String, drwPath As String, pdfPath As String
    base = OUT_DIR & series & "_SERIES": drwPath = base & ".SLDDRW": pdfPath = base & ".PDF"
    If BASE_DRAWING <> "" And Dir(BASE_DRAWING) <> "" Then
        Set swModelDraw = swApp.OpenDoc6(BASE_DRAWING, swDocumentTypes_e.swDocDRAWING, swOpenDocOptions_e.swOpenDocOptions_Silent, "", errs, warns)
        Chk series & ": base drawing opened (err " & errs & ")", Not swModelDraw Is Nothing
        If swModelDraw Is Nothing Then GoTo CloseP
        swApp.ActivateDoc3 swModelDraw.GetTitle, False, 0, errs
        ' save under the series name FIRST so the original sheet is never touched
        Chk series & ": saved as " & drwPath, swModelDraw.Extension.SaveAs(drwPath, 0, 1, Nothing, errs, warns)
        Set swDraw = swModelDraw
        ' remove the 6600 views (and everything attached to them)
        Dim vSheet As SldWorks.View, vNext As SldWorks.View, nDel As Long
        Set vSheet = swDraw.GetFirstView       ' the sheet itself
        Set vNext = vSheet.GetNextView
        Do While Not vNext Is Nothing
            Dim vDel As SldWorks.View: Set vDel = vNext
            Set vNext = vNext.GetNextView
            swDraw.ClearSelection2 True
            If swDraw.Extension.SelectByID2(vDel.GetName2, "DRAWINGVIEW", 0, 0, 0, False, 0, Nothing, 0) Then
                swDraw.Extension.DeleteSelection2 0: nDel = nDel + 1
            End If
        Loop
        Say "  " & nDel & " view(s) removed from the base sheet"
        swDraw.ClearSelection2 True
    Else
        Set swModelDraw = swApp.NewDocument(tpl, 0, 0, 0)
        Chk series & ": drawing created from the template", Not swModelDraw Is Nothing
        If swModelDraw Is Nothing Then GoTo CloseP
        Set swDraw = swModelDraw
        swApp.ActivateDoc3 swModelDraw.GetTitle, False, 0, errs
    End If

    Dim W As Double, H As Double, pr As Variant
    W = 0.297: H = 0.21
    On Error Resume Next
    Dim shO As Object: Set shO = swDraw.GetCurrentSheet
    pr = shO.GetProperties2
    If IsArray(pr) Then
        If UBound(pr) >= 6 Then
            If pr(5) > 0.05 And pr(6) > 0.05 Then W = pr(5): H = pr(6)
        End If
    End If
    On Error GoTo Fail
    Say "  sheet " & Format(W * 1000, "0") & " x " & Format(H * 1000, "0") & " mm"

    ' scale so the part fills about a third of the sheet
    Dim bb As Variant, dx As Double, dy As Double, sc As Double
    bb = swPart.GetPartBox(True)
    dx = Abs(bb(3) - bb(0)): dy = Abs(bb(4) - bb(1))
    sc = 1#
    If dx > 0 And dy > 0 Then
        sc = 0.3 * W / dx
        If 0.33 * H / dy < sc Then sc = 0.33 * H / dy
    End If
    If sc > 1 Then sc = 1
    If sc < 0.1 Then sc = 0.1
    Say "  part " & Format(dx / IN_, "0.00") & " x " & Format(dy / IN_, "0.00") & " in, view scale " & Format(sc, "0.000")

    Dim vF As SldWorks.View, vR As SldWorks.View, vI As SldWorks.View
    Set vF = swDraw.CreateDrawViewFromModelView3(path, "*Front", 0.3 * W, 0.55 * H, 0)
    Chk series & ": front view", Not vF Is Nothing
    If vF Is Nothing Then GoTo CloseD
    vF.ReferencedConfiguration = cfg
    vF.ScaleDecimal = sc
    Set vR = swDraw.CreateDrawViewFromModelView3(path, "*Right", 0.62 * W, 0.55 * H, 0)
    If Not vR Is Nothing Then vR.ReferencedConfiguration = cfg: vR.ScaleDecimal = sc
    Set vI = swDraw.CreateDrawViewFromModelView3(path, "*Isometric", 0.85 * W, 0.78 * H, 0)
    If Not vI Is Nothing Then vI.ReferencedConfiguration = cfg: vI.ScaleDecimal = sc
    Say "  views: front " & (Not vF Is Nothing) & ", right " & (Not vR Is Nothing) & ", iso " & (Not vI Is Nothing)

    ' ---- model dimensions: rebuild the new views, import marked dims into all views, prune to the envelope set
    swModelDraw.ForceRebuild3 False
    Dim nIns As Long, kept As Long, cut As Long
    Say "  enum check: source=" & swImportModelItemsSource_e.swImportModelItemsFromEntireModel & " types=" & swInsertAnnotation_e.swInsertDimensionsMarkedForDrawing
    swDraw.ClearSelection2 True
    On Error Resume Next
    Dim vAnn As Variant
    vAnn = swDraw.InsertModelAnnotations3(swImportModelItemsSource_e.swImportModelItemsFromEntireModel, swInsertAnnotation_e.swInsertDimensionsMarkedForDrawing, True, True, False, True)
    Say "  InsertModelAnnotations3 (early bound, all views) -> " & TypeName(vAnn) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "")
    Err.Clear
    If IsArray(vAnn) Then nIns = UBound(vAnn) - LBound(vAnn) + 1
    If nIns = 0 Then
        vAnn = swDraw.InsertModelAnnotations3(swImportModelItemsSource_e.swImportModelItemsFromEntireModel, swInsertAnnotation_e.swInsertDimensionsMarkedForDrawing + swInsertAnnotation_e.swInsertDimensionsNotMarkedForDrawing, True, True, False, True)
        Say "  ... marked + unmarked -> " & TypeName(vAnn) & IIf(Err.Number <> 0, " [err " & Err.Description & "]", "")
        Err.Clear
        If IsArray(vAnn) Then nIns = UBound(vAnn) - LBound(vAnn) + 1
    End If
    On Error GoTo Fail
    Say "  annotations returned: " & nIns
    ' prune straight from the returned annotation array: keep the envelope dims, delete the rest
    Dim ia As Long, an As SldWorks.Annotation, dd As SldWorks.DisplayDimension, dm As SldWorks.Dimension, nm As String, other As Long
    If IsArray(vAnn) Then
        For ia = LBound(vAnn) To UBound(vAnn)
            On Error Resume Next
            Set an = vAnn(ia)
            Set dd = Nothing
            Set dd = an.GetSpecificAnnotation
            If TypeName(dd) = "IDisplayDimension" Or TypeName(dd) = "DisplayDimension" Then
                Set dm = dd.GetDimension2(0): nm = dm.Name
                If InStr(1, KEEP, "|" & nm & "|", vbTextCompare) > 0 Then
                    kept = kept + 1
                    If InStr(1, AS_DIA, "|" & nm & "|", vbTextCompare) > 0 Then dd.Diametric = True
                Else
                    swDraw.ClearSelection2 True
                    If an.Select3(False, Nothing) Then swDraw.Extension.DeleteSelection2 0
                    cut = cut + 1
                End If
            Else
                other = other + 1
                If ia = LBound(vAnn) Then Say "  first annotation type: " & TypeName(dd) & " / " & an.GetType
            End If
            Err.Clear
            On Error GoTo Fail
        Next ia
    End If
    If other > 0 Then Say "  " & other & " annotation(s) were not display dimensions"
    Say "  dimensions kept " & kept & ", pruned " & cut
    Chk series & ": envelope dimensions on the sheet", kept > 0

    Say "  adding notes"
    ' ---- note block: what the sheet is, and the honest data status
    Dim pn As String, ds As String, de As String, ta As String, tb As String, mt As String
    pn = Prop(swPart, cfg, "PartNo"): If pn = "" Then pn = cfg
    de = Prop(swPart, cfg, "Description")
    ta = Prop(swPart, cfg, "EndA_Thread"): If ta = "" Then ta = Prop(swPart, cfg, "End1_Thread")
    tb = Prop(swPart, cfg, "EndB_Thread"): If tb = "" Then tb = Prop(swPart, cfg, "End2_Thread")
    ds = Prop(swPart, cfg, "DataStatus")
    mt = Prop(swPart, cfg, "Material"): If mt = "" Then mt = "Carbon steel"

    Dim cfgs As Variant, nCfg As Long
    cfgs = swPart.GetConfigurationNames
    nCfg = UBound(cfgs) + 1

    AddNote swDraw, "OM INDUSTRIAL PRODUCTS CORP." & vbLf & "SERIES " & series & "  -  " & de, 0.04 * W, 0.94 * H, 0.005
    AddNote swDraw, "DRAWN SIZE: " & pn & vbLf & _
                    "END A: " & ta & vbLf & "END B: " & tb & vbLf & _
                    "MATERIAL: " & mt & vbLf & _
                    "DATA STATUS: " & ds & vbLf & _
                    "SIZES IN THIS SERIES: " & nCfg, 0.04 * W, 0.86 * H, 0.004
    AddNote swDraw, "KEY DIMENSIONS (" & pn & ")" & vbLf & KeyDims(swPart), 0.04 * W, 0.42 * H, 0.004
    AddNote swDraw, "Dimensions in inches. Thread callouts nominal. Geometry per Air-Way catalog with " & _
                    "JIC 37 deg ends per SAE J514 / MS33656J." & vbLf & _
                    "ASSUMED rows are catalog-accurate but not independently standards-verified - not released for production.", _
                    0.04 * W, 0.06 * H, 0.0035

    Say "  saving"
    ' ---- save
    Dim okDrw As Boolean
    okDrw = swModelDraw.Extension.SaveAs(drwPath, 0, 1, Nothing, errs, warns)
    Chk series & ": SLDDRW written" & IIf(okDrw, "", " (err " & errs & ")"), okDrw
    Dim okPdf As Boolean
    okPdf = swModelDraw.Extension.SaveAs(pdfPath, 0, 1, Nothing, errs, warns)
    Chk series & ": PDF written " & pdfPath & IIf(okPdf, "", " (err " & errs & ")"), okPdf
    If okPdf Then nOK = nOK + 1

CloseD:
    swApp.CloseDoc swModelDraw.GetTitle
CloseP:
    If SHOW_THREADS And nThd > 0 Then SetThreads swPart, True
    swApp.QuitDoc swPart.GetTitle        ' close WITHOUT saving - the master is untouched
    Exit Sub
Fail:
    Say "FAIL  " & series & ": runtime error " & Err.Number & " - " & Err.Description
    nFail = nFail + 1
    On Error Resume Next
    If Not swModelDraw Is Nothing Then swApp.CloseDoc swModelDraw.GetTitle
    If Not swPart Is Nothing Then swApp.QuitDoc swPart.GetTitle
End Sub
