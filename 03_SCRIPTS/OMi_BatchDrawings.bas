Attribute VB_Name = "OMi_BatchDrawings"
'==========================================================================================
' OMi HYDRAULIC FITTING LIBRARY - BATCH DRAWING + EXPORT MACRO
'
'   Phase 1c deliverable. Written for SOLIDWORKS 2026 Standard (no Task Scheduler).
'
'   WHAT IT DOES, per configuration of the open master part:
'     1. Activates the configuration
'     2. Creates a drawing from your drawing template
'     3. Inserts standard views (front / top / right / iso per SHOW_* switches below)
'     4. Pushes the config's custom properties onto the DRAWING so title-block and note
'        links resolve
'     5. Exports PDF and STEP using the filename from the design table
'     6. Logs every action, then closes the drawing
'
'   SAFETY DESIGN - read before running:
'     * DRY_RUN = True by default. It walks every configuration and writes a full log
'       WITHOUT creating, saving or exporting a single file. ALWAYS dry-run first.
'     * Nothing is overwritten unless OVERWRITE_EXISTING = True.
'     * Every file operation is wrapped; one bad configuration is logged and skipped,
'       it does not abort the batch.
'     * A row whose DataStatus is not VERIFIED/ASSUMED is skipped unless
'       ALLOW_UNVERIFIED = True. This is the guard that stops a MISSING-data part
'       from silently becoming a released drawing.
'
'   BEFORE FIRST RUN:
'     - Open the master part, with its design table already applied
'     - Set OUTPUT_DIR and DRAWING_TEMPLATE below
'     - Tools > Macro > Run
'==========================================================================================
Option Explicit

'---------------------------- USER SETTINGS -----------------------------------------------
Private Const DRY_RUN            As Boolean = True     ' <<< SET False ONLY AFTER A CLEAN DRY RUN
Private Const OVERWRITE_EXISTING As Boolean = False
Private Const ALLOW_UNVERIFIED   As Boolean = False    ' True = also process MISSING-data configs

Private Const OUTPUT_DIR       As String = "C:\OMi\Output\"
Private Const DRAWING_TEMPLATE As String = "C:\OMi\Templates\OMi_Fitting_B.drwdot"
Private Const LOG_DIR          As String = "C:\OMi\Logs\"

Private Const EXPORT_PDF   As Boolean = True
Private Const EXPORT_STEP  As Boolean = True

'--- HELICAL THREADS: DRAWING-ONLY -------------------------------------------
' Real helical thread geometry appears in the DRAWING but never in the model
' you keep or in the exported STEP.
'
' How it works: model the threads with the SOLIDWORKS Thread feature (real
' helical cut/boss), then leave those features SUPPRESSED. This macro
' unsuppresses them only while the drawing views are being built, and
' re-suppresses them immediately afterwards. STEP export happens while they
' are suppressed.
'
' Why this way and not two configurations: doubling configs would take the
' library from ~2,500 to ~5,000 configs and roughly double rebuild time for
' no benefit. Runtime toggling costs one rebuild per part and keeps a single
' clean config set.
'
' Name every thread feature with the THREAD_PREFIX below (e.g. THD_EndA,
' THD_EndB). The macro finds them by prefix, so a master with one thread or
' four needs no code change.
Private Const HELICAL_THREADS_IN_DRAWINGS As Boolean = True
Private Const THREAD_PREFIX As String = "THD_"
Private Const SUPPRESS_THREADS_FOR_STEP   As Boolean = True

Private Const SHOW_FRONT As Boolean = True
Private Const SHOW_TOP   As Boolean = False
Private Const SHOW_RIGHT As Boolean = True
Private Const SHOW_ISO   As Boolean = True
Private Const VIEW_SCALE As Double = 1#              ' 0 = let the template decide

' Custom properties copied from part configuration -> drawing (for title block / notes)
Private Const PROP_LIST As String = "PartNo|Description|GeometryRoot|EndA_Type|EndA_Thread|" & _
    "EndA_ThreadStd|EndB_Type|EndB_Thread|EndB_ThreadStd|SeatAngle|Material|Finish|" & _
    "PressureRating|DataStatus|SourceURL"
'------------------------------------------------------------------------------------------

Private swApp    As Object
Private logFile  As Integer
Private nOK      As Long, nSkip As Long, nFail As Long

Sub main()
    Dim swPart As Object, swDraw As Object
    Dim cfgNames As Variant, cfg As Variant
    Dim t0 As Double: t0 = Timer

    Set swApp = Application.SldWorks
    If swApp Is Nothing Then MsgBox "Cannot attach to SOLIDWORKS.", vbCritical: Exit Sub

    Set swPart = swApp.ActiveDoc
    If swPart Is Nothing Then
        MsgBox "Open the master PART first, then run this macro.", vbExclamation: Exit Sub
    End If
    If swPart.GetType <> 1 Then           ' 1 = swDocPART
        MsgBox "Active document must be a PART, not a drawing or assembly.", vbExclamation: Exit Sub
    End If

    If Not OpenLog(swPart.GetTitle) Then Exit Sub

    LogLine "=========================================================="
    LogLine "OMi BATCH DRAWING RUN"
    LogLine "Master part   : " & swPart.GetPathName
    LogLine "Mode          : " & IIf(DRY_RUN, "*** DRY RUN - NOTHING WILL BE WRITTEN ***", "LIVE")
    LogLine "Overwrite     : " & OVERWRITE_EXISTING
    LogLine "Allow unverif.: " & ALLOW_UNVERIFIED
    LogLine "Output dir    : " & OUTPUT_DIR
    LogLine "=========================================================="

    If Not DRY_RUN Then
        If Not EnsureDir(OUTPUT_DIR) Then
            LogLine "FATAL: output directory unavailable: " & OUTPUT_DIR
            CloseLog: MsgBox "Output directory unavailable. See log.", vbCritical: Exit Sub
        End If
        If Dir(DRAWING_TEMPLATE) = "" Then
            LogLine "FATAL: drawing template not found: " & DRAWING_TEMPLATE
            CloseLog: MsgBox "Drawing template not found. See log.", vbCritical: Exit Sub
        End If
    End If

    cfgNames = swPart.GetConfigurationNames
    If IsEmpty(cfgNames) Then
        LogLine "FATAL: master part reports no configurations. Is the design table applied?"
        CloseLog: MsgBox "No configurations found.", vbCritical: Exit Sub
    End If
    LogLine "Configurations found: " & (UBound(cfgNames) - LBound(cfgNames) + 1)
    LogLine ""

    For Each cfg In cfgNames
        ProcessOne swPart, CStr(cfg)
    Next cfg

    LogLine ""
    LogLine "=========================================================="
    LogLine "DONE in " & Format(Timer - t0, "0.0") & "s   OK=" & nOK & "  SKIPPED=" & nSkip & "  FAILED=" & nFail
    LogLine "=========================================================="
    CloseLog

    MsgBox "Batch complete." & vbCrLf & vbCrLf & _
           IIf(DRY_RUN, "DRY RUN - no files were written." & vbCrLf & vbCrLf, "") & _
           "Succeeded: " & nOK & vbCrLf & "Skipped:   " & nSkip & vbCrLf & _
           "Failed:    " & nFail & vbCrLf & vbCrLf & "Log: " & LOG_DIR, _
           IIf(nFail > 0, vbExclamation, vbInformation)
End Sub

'------------------------------------------------------------------------------------------
Private Sub ProcessOne(swPart As Object, cfgName As String)
    Dim swDraw As Object, swModel As Object, swView As Object
    Dim baseName As String, status As String, pdfPath As String, stepPath As String
    Dim errs As Long, warns As Long, n As Long
    Dim ok As Boolean

    On Error GoTo Fail

    ' ---- gate on DataStatus -------------------------------------------------
    status = UCase$(Trim$(GetCfgProp(swPart, cfgName, "DataStatus")))
    If status <> "VERIFIED" And status <> "ASSUMED" Then
        If Not ALLOW_UNVERIFIED Then
            LogLine "SKIP  " & cfgName & "  (DataStatus=" & IIf(status = "", "<blank>", status) & ")"
            nSkip = nSkip + 1: Exit Sub
        End If
    End If

    baseName = Trim$(GetCfgProp(swPart, cfgName, "PartNo"))
    If baseName = "" Then baseName = cfgName
    baseName = SafeName(baseName)
    pdfPath = OUTPUT_DIR & baseName & ".pdf"
    stepPath = OUTPUT_DIR & baseName & ".step"

    If Not OVERWRITE_EXISTING Then
        If (EXPORT_PDF And Dir(pdfPath) <> "") Or (EXPORT_STEP And Dir(stepPath) <> "") Then
            LogLine "SKIP  " & cfgName & "  (output exists, OVERWRITE_EXISTING=False)"
            nSkip = nSkip + 1: Exit Sub
        End If
    End If

    If DRY_RUN Then
        LogLine "DRY   " & cfgName & "  status=" & status & "  -> " & baseName & ".pdf/.step"
        nOK = nOK + 1: Exit Sub
    End If

    ' ---- activate configuration --------------------------------------------
    If Not swPart.ShowConfiguration2(cfgName) Then
        LogLine "FAIL  " & cfgName & "  could not activate configuration"
        nFail = nFail + 1: Exit Sub
    End If
    swPart.EditRebuild3

    ' ---- STEP export from the PART -----------------------------------------
    ' Threads stay suppressed here, so the exported solid is the clean
    ' manufacturing geometry with no helical faces.
    If SUPPRESS_THREADS_FOR_STEP Then SetThreads swPart, True
    If EXPORT_STEP Then
        If swPart.Extension.SaveAs(stepPath, 0, 1, Nothing, errs, warns) Then
            LogLine "  step  " & baseName & ".step"
        Else
            LogLine "  WARN  STEP export failed (err=" & errs & ") for " & cfgName
        End If
    End If

    ' ---- drawing ------------------------------------------------------------
    ' Unsuppress the helical threads so the drawing views show real thread
    ' geometry. They go back to suppressed at the end of this routine.
    If HELICAL_THREADS_IN_DRAWINGS Then
        n = SetThreads(swPart, False)
        LogLine "  thd   " & n & " thread feature(s) unsuppressed for drawing"
        If n = 0 Then LogLine "  WARN  no features named " & THREAD_PREFIX & _
                              "* found in " & cfgName & " - drawing will show no threads"
    End If

    Set swDraw = swApp.NewDocument(DRAWING_TEMPLATE, 0, 0, 0)
    If swDraw Is Nothing Then
        LogLine "FAIL  " & cfgName & "  could not create drawing from template"
        nFail = nFail + 1: Exit Sub
    End If
    swApp.ActivateDoc3 swDraw.GetTitle, False, 0, errs

    Set swView = swDraw.CreateDrawViewFromModelView3(swPart.GetPathName, "*Front", 0.1, 0.15, 0)
    If swView Is Nothing Then
        LogLine "FAIL  " & cfgName & "  view insertion failed"
        swApp.CloseDoc swDraw.GetTitle
        nFail = nFail + 1: Exit Sub
    End If
    swView.ReferencedConfiguration = cfgName
    If VIEW_SCALE > 0 Then swView.ScaleDecimal = VIEW_SCALE

    If SHOW_RIGHT Then swDraw.CreateDrawViewFromModelView3 swPart.GetPathName, "*Right", 0.25, 0.15, 0
    If SHOW_TOP Then swDraw.CreateDrawViewFromModelView3 swPart.GetPathName, "*Top", 0.1, 0.25, 0
    If SHOW_ISO Then swDraw.CreateDrawViewFromModelView3 swPart.GetPathName, "*Isometric", 0.25, 0.25, 0

    CopyProps swPart, cfgName, swDraw
    swDraw.ForceRebuild3 False

    If EXPORT_PDF Then
        If swDraw.Extension.SaveAs(pdfPath, 0, 1, Nothing, errs, warns) Then
            LogLine "OK    " & cfgName & "  -> " & baseName & ".pdf"
            nOK = nOK + 1
        Else
            LogLine "FAIL  " & cfgName & "  PDF export failed (err=" & errs & ")"
            nFail = nFail + 1
        End If
    Else
        nOK = nOK + 1
    End If

    swApp.CloseDoc swDraw.GetTitle
    If HELICAL_THREADS_IN_DRAWINGS Then SetThreads swPart, True
    Exit Sub

Fail:
    LogLine "FAIL  " & cfgName & "  UNHANDLED: " & Err.Number & " - " & Err.Description
    nFail = nFail + 1
    On Error Resume Next
    If Not swDraw Is Nothing Then swApp.CloseDoc swDraw.GetTitle
    If HELICAL_THREADS_IN_DRAWINGS Then SetThreads swPart, True   ' never leave threads live
End Sub

'------------------------------------------------------------------------------------------
' Suppress / unsuppress every feature whose name begins with THREAD_PREFIX.
' Returns how many features were toggled. Walks the whole tree including
' folders, so threads nested in a feature folder are still found.
Private Function SetThreads(swPart As Object, suppress As Boolean) As Long
    Dim feat As Object, cnt As Long
    On Error Resume Next
    Set feat = swPart.FirstFeature
    Do While Not feat Is Nothing
        If Left$(feat.Name, Len(THREAD_PREFIX)) = THREAD_PREFIX Then
            If suppress Then
                feat.SetSuppression2 0, 2, Empty      ' 0=Suppress, 2=this configuration
            Else
                feat.SetSuppression2 1, 2, Empty      ' 1=Unsuppress
            End If
            cnt = cnt + 1
        End If
        Set feat = feat.GetNextFeature
    Loop
    If cnt > 0 Then swPart.EditRebuild3
    SetThreads = cnt
    On Error GoTo 0
End Function

'------------------------------------------------------------------------------------------
Private Function GetCfgProp(swPart As Object, cfgName As String, propName As String) As String
    Dim mgr As Object, valOut As String, resolved As String, wasRes As Boolean, link As Boolean
    On Error Resume Next
    Set mgr = swPart.Extension.CustomPropertyManager(cfgName)
    mgr.Get5 propName, False, valOut, resolved, wasRes
    If Trim$(resolved) <> "" Then GetCfgProp = resolved Else GetCfgProp = valOut
    If Trim$(GetCfgProp) = "" Then                     ' fall back to file-level property
        Set mgr = swPart.Extension.CustomPropertyManager("")
        mgr.Get5 propName, False, valOut, resolved, wasRes
        If Trim$(resolved) <> "" Then GetCfgProp = resolved Else GetCfgProp = valOut
    End If
    On Error GoTo 0
End Function

Private Sub CopyProps(swPart As Object, cfgName As String, swDraw As Object)
    Dim names As Variant, i As Long, v As String, mgr As Object
    On Error Resume Next
    Set mgr = swDraw.Extension.CustomPropertyManager("")
    names = Split(PROP_LIST, "|")
    For i = LBound(names) To UBound(names)
        v = GetCfgProp(swPart, cfgName, CStr(names(i)))
        If v <> "" Then mgr.Add3 CStr(names(i)), 30, v, 1   ' 30=swCustomInfoText, 1=overwrite
    Next i
    mgr.Add3 "ConfigName", 30, cfgName, 1
    On Error GoTo 0
End Sub

'------------------------------------------------------------------------------------------
Private Function SafeName(s As String) As String
    Dim bad As Variant, b As Variant
    bad = Array("\", "/", ":", "*", "?", """", "<", ">", "|")
    SafeName = s
    For Each b In bad
        SafeName = Replace(SafeName, CStr(b), "_")
    Next b
    SafeName = Trim$(SafeName)
End Function

Private Function EnsureDir(p As String) As Boolean
    On Error Resume Next
    If Dir(p, vbDirectory) = "" Then MkDir p
    EnsureDir = (Dir(p, vbDirectory) <> "")
    On Error GoTo 0
End Function

Private Function OpenLog(tag As String) As Boolean
    Dim p As String
    On Error GoTo NoLog
    If Dir(LOG_DIR, vbDirectory) = "" Then MkDir LOG_DIR
    p = LOG_DIR & "OMi_batch_" & SafeName(tag) & "_" & Format(Now, "yyyymmdd_hhnnss") & ".log"
    logFile = FreeFile
    Open p For Output As #logFile
    OpenLog = True
    Exit Function
NoLog:
    MsgBox "Cannot write log to " & LOG_DIR & vbCrLf & Err.Description, vbCritical
    OpenLog = False
End Function

Private Sub LogLine(s As String)
    Debug.Print s
    On Error Resume Next
    If logFile > 0 Then Print #logFile, Format(Now, "hh:nn:ss") & "  " & s
End Sub

Private Sub CloseLog()
    On Error Resume Next
    If logFile > 0 Then Close #logFile
    logFile = 0
End Sub
