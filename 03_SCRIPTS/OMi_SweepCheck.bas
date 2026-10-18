Attribute VB_Name = "OMi_SweepCheck"
' OMi_SweepCheck - verify every master in 11_MASTERS with its THREADS LIVE, in EVERY configuration.
'   For each part: each configuration is shown, every THD_ feature is unsuppressed in that configuration,
'   the part is rebuilt, and the macro checks: every feature rebuilds (error code 0), one solid body,
'   and the threads removed material (volume with threads < volume without). Threads are put back to
'   suppressed and the part is closed WITHOUT saving - nothing in 11_MASTERS is modified.
' Run with SolidWorks open and no documents open.  Entry: Sub SweepAllMasters.
' Writes 03_SCRIPTS\SweepCheck_report.txt.  Expect several minutes (helical threads rebuild slowly).
Option Explicit
Const MASTER_DIR As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\11_MASTERS\"
Const REPORT_PATH As String = "C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\03_SCRIPTS\SweepCheck_report.txt"
Dim swApp As SldWorks.SldWorks
Dim fnRep As Integer

Sub SweepAllMasters()
    Set swApp = Application.SldWorks
    fnRep = FreeFile: Open REPORT_PATH For Output As #fnRep
    Print #fnRep, "OMi_SweepCheck  " & Now
    Dim f As String, nParts As Long, nBadParts As Long
    f = Dir(MASTER_DIR & "*.SLDPRT")
    Do While f <> ""
        If Left(f, 1) <> "~" Then
            nParts = nParts + 1
            If Not SweepOne(MASTER_DIR & f, f) Then nBadParts = nBadParts + 1
        End If
        f = Dir
    Loop
    Print #fnRep, "SUMMARY: " & nParts & " master(s) swept, " & nBadParts & " with failures"
    Close #fnRep
    MsgBox nParts & " master(s) swept, " & nBadParts & " with failures - see SweepCheck_report.txt", vbInformation, "OMi_SweepCheck"
End Sub

Private Function SweepOne(path As String, shortName As String) As Boolean
    On Error Resume Next
    Dim swModel As SldWorks.ModelDoc2, e As Long, w As Long
    Set swModel = swApp.OpenDoc6(path, swDocumentTypes_e.swDocPART, swOpenDocOptions_e.swOpenDocOptions_Silent, "", e, w)
    If swModel Is Nothing Then
        Print #fnRep, "FAIL  " & shortName & ": could not be opened (error " & e & ")"
        Exit Function
    End If
    Dim names As Variant, i As Long, ft As SldWorks.Feature, nThd As Long, nCfg As Long, nBad As Long
    Dim v0 As Double, v1 As Double, b As Variant, nb As Long, msg As String
    names = swModel.GetConfigurationNames
    For i = LBound(names) To UBound(names)
        If names(i) <> "Default" Then
            nCfg = nCfg + 1
            swModel.ShowConfiguration2 names(i)
            swModel.ForceRebuild3 False
            v0 = PartVolume(swModel)
            nThd = 0
            Set ft = swModel.FirstFeature
            Do While Not ft Is Nothing
                If Left(ft.Name, 4) = "THD_" Then
                    ft.SetSuppression2 swFeatureSuppressionAction_e.swUnSuppressFeature, swInConfigurationOpts_e.swThisConfiguration, Empty
                    nThd = nThd + 1
                End If
                Set ft = ft.GetNextFeature
            Loop
            swModel.ForceRebuild3 False
            v1 = PartVolume(swModel)
            msg = ""
            Set ft = swModel.FirstFeature
            Do While Not ft Is Nothing
                If Not ft.IsSuppressed Then
                    If ft.GetErrorCode2(True) <> 0 Then msg = msg & " " & ft.Name & "(err " & ft.GetErrorCode2(True) & ")"
                ElseIf Left(ft.Name, 4) = "THD_" Then
                    msg = msg & " " & ft.Name & "(still suppressed)"
                End If
                Set ft = ft.GetNextFeature
            Loop
            b = swModel.GetBodies2(swBodyType_e.swSolidBody, True)
            nb = IIf(IsEmpty(b), 0, UBound(b) + 1)
            If nb <> 1 Then msg = msg & " bodies=" & nb
            If nThd > 0 And Not (v1 < v0 - 1E-12) Then msg = msg & " threads removed no material"
            If msg <> "" Then
                Print #fnRep, "FAIL  " & shortName & " | " & names(i) & " |" & msg
                nBad = nBad + 1
            End If
            Set ft = swModel.FirstFeature
            Do While Not ft Is Nothing
                If Left(ft.Name, 4) = "THD_" Then ft.SetSuppression2 swFeatureSuppressionAction_e.swSuppressFeature, swInConfigurationOpts_e.swThisConfiguration, Empty
                Set ft = ft.GetNextFeature
            Loop
        End If
    Next i
    Print #fnRep, IIf(nBad = 0, "OK    ", "FAIL  ") & shortName & ": " & nCfg & " configurations swept with " & nThd & " thread feature(s) live, " & nBad & " failing"
    swApp.QuitDoc swModel.GetTitle       ' close WITHOUT saving
    SweepOne = (nBad = 0)
End Function

Private Function PartVolume(swModel As SldWorks.ModelDoc2) As Double
    On Error Resume Next
    Dim mp As Object
    Set mp = swModel.Extension.CreateMassProperty
    If Not mp Is Nothing Then PartVolume = mp.Volume
End Function
